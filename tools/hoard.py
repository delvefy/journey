#!/usr/bin/env python3
"""hoard.py — authoring tool for The Riddle-Hoard (see write.txt, same folder).

The whole point of this tool is to stay NEIGHBOUR-LOCAL: it never scans the
whole grid. Every command reads only the cells that touch the batch you are
about to write, so the cost is O(batch size), not O(rooms). That keeps the
work cheap whether the hoard has 90 rooms or 90,000.

WORKFLOW for a batch (the user hands you a count or a list of coords):

  1. python3 tools/hoard.py next 8
        -> the next 8 unwritten coords in writing order (closest-first,
           ties clockwise from north). Pure maths + file-existence; no reads.

  2. python3 tools/hoard.py plan 8         (or: plan -1:-5 -5:-1 ...)
        -> a per-room briefing: each room's COMMITTED name (what written
           neighbours already call it), and for each of its 4 walls the exact
           answer to write (a written neighbour's name, or an unwritten cell
           already fixed by some other room, or "NAME IT" + the quadrant).
           Reads only the batch's neighbours (and their neighbours). This is
           all you need to author the riddles correctly.

  3. Author the batch as JSON (see the schema printed by `plan --schema`) and:
     python3 tools/hoard.py render batch.json
        -> renders each room with the canonical skeleton, writes
           rooms/<x>/<y>.html in writing order, advances the LAST ROOM line in
           rooms-map.txt after EACH save (interruption-safe), and runs a local
           crossword check on every room as it lands.

  4. python3 tools/hoard.py verify 8       (or: verify batch.json / coords)
        -> re-checks the batch + its neighbours: answers match neighbour names,
           facing pairs agree both ways, answers distinct, 4 walls each.

Coords are written "x:y" (e.g. -1:-5). The grid is bounded -150..+150.
"""

import os, re, sys, math, json, textwrap

HERE = os.path.dirname(os.path.abspath(__file__))      # tools/
REPO = os.path.dirname(HERE)
ROOMS = os.path.join(REPO, "rooms")
MAP = os.path.join(HERE, "rooms-map.txt")              # tracker lives beside this script
SPAN = 150

DELTA = {"top": (0, 1), "right": (1, 0), "bottom": (0, -1), "left": (-1, 0)}
OPP = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}
NESW = {"N": "top", "E": "right", "S": "bottom", "W": "left"}     # author keys -> dir
LABEL = {"top": "North", "right": "East", "bottom": "South", "left": "West"}
IID = {"top": "ans-top", "right": "ans-right", "bottom": "ans-bottom", "left": "ans-left"}

# ---------------------------------------------------------------- geometry / bands
def band(d):
    if d == 0: return "Threshold"
    if d <= 100: return "Approach"
    if d <= 120: return "Near Hoard"
    if d <= 140: return "Deep Hoard"
    if d <= 149: return "Far Reaches"
    if d < 212: return "Rim"
    return "Apex (corner)"

def quadrant(x, y):
    qx = "wrought" if x > 0 else "natural" if x < 0 else "axis"
    qy = "intangible" if y > 0 else "tangible" if y < 0 else "axis"
    return qx + "+" + qy

def bearing(x, y):
    a = math.atan2(x, y)          # 0 = north(+y), clockwise; matches N,NE,E,SE,S,SW,W,NW
    return a if a >= 0 else a + 2 * math.pi

def order_key(c):
    x, y = c
    return (x * x + y * y, bearing(x, y))

def iter_order():
    """Yield every in-bounds cell in writing order, by increasing distance."""
    k = 0
    maxk = 2 * SPAN * SPAN
    while k <= maxk:
        cells = []
        r = math.isqrt(k)
        for x in range(-r, r + 1):
            y2 = k - x * x
            if y2 < 0: continue
            y = math.isqrt(y2)
            if y * y != y2: continue
            for yy in ({y, -y}):
                if -SPAN <= x <= SPAN and -SPAN <= yy <= SPAN:
                    cells.append((x, yy))
        cells.sort(key=lambda c: bearing(*c))
        for c in cells:
            yield c
        k += 1

# ---------------------------------------------------------------- file access (cached)
_CACHE = {}
def cell_path(x, y):
    return os.path.join(ROOMS, str(x), "%d.html" % y)

def exists(c):
    return os.path.isfile(cell_path(*c))

def read_room(c):
    """Return (name_lowercase, {dir: answer}) for a written cell, or None."""
    if c in _CACHE:
        return _CACHE[c]
    p = cell_path(*c)
    if not os.path.isfile(p):
        _CACHE[c] = None
        return None
    t = open(p, encoding="utf-8").read()
    m = re.search(r'room-name">([^<]*)', t)
    name = m.group(1).strip().lower() if m else None
    answers = {}
    for mm in re.finditer(r'data-dir="([^"]*)" data-href="[^"]*" data-answer="([^"]*)"', t):
        answers[mm.group(1)] = mm.group(2)
    _CACHE[c] = (name, answers)
    return _CACHE[c]

def href(x, y, d):
    if d == "top":    return "%d.html" % (y + 1)
    if d == "bottom": return "%d.html" % (y - 1)
    if d == "right":  return "../%d/%d.html" % (x + 1, y)
    if d == "left":   return "../%d/%d.html" % (x - 1, y)

def committed_name(c, ignore=None):
    """What WRITTEN neighbours of cell c already call it. Returns (name|None, sources, conflict)."""
    x, y = c
    votes = {}
    for d, (dx, dy) in DELTA.items():
        n = (x + dx, y + dy)
        if n == ignore:
            continue
        r = read_room(n)
        if r:
            a = r[1].get(OPP[d])           # neighbour's wall facing back at c
            if a:
                votes.setdefault(a, []).append("%d:%d %s->%s" % (n[0], n[1], OPP[d], a))
    if not votes:
        return (None, [], False)
    best = max(votes, key=lambda k: len(votes[k]))
    return (best, votes[best], len(votes) > 1)

# ---------------------------------------------------------------- commands
def parse_coords(args):
    out = []
    for a in args:
        m = re.fullmatch(r"(-?\d+):(-?\d+)", a)
        if not m:
            sys.exit("bad coord %r (want x:y)" % a)
        out.append((int(m.group(1)), int(m.group(2))))
    return out

def next_unwritten(n):
    out = []
    for c in iter_order():
        if not exists(c):
            out.append(c)
            if len(out) >= n:
                break
    return out

def targets_from_args(args):
    """A bare integer = next N; otherwise an explicit coord list."""
    if len(args) == 1 and re.fullmatch(r"\d+", args[0]):
        return next_unwritten(int(args[0]))
    return parse_coords(args)

def cmd_next(args):
    n = int(args[0]) if args else 1
    for i, c in enumerate(next_unwritten(n)):
        d = math.hypot(*c)
        print("%2d. %d:%d   d=%.3f  %s" % (i + 1, c[0], c[1], d, band(d)))

def cmd_plan(args):
    if "--schema" in args:
        print(SCHEMA); return
    for c in targets_from_args(args):
        x, y = c
        d = math.hypot(x, y)
        cn, src, conflict = committed_name(c)
        tag = "" if cn else "  (no inward neighbour written — you choose the name)"
        print("== %d:%d   d=%.3f  band=%s  quadrant=%s%s" % (x, y, d, band(d), quadrant(x, y), tag))
        if cn:
            warn = "  *** CONFLICT ***" if conflict else ""
            print("   name MUST be: %-10s [%s]%s" % (cn, ", ".join(src), warn))
        for k in ("N", "E", "S", "W"):
            dr = NESW[k]; dx, dy = DELTA[dr]; nc = (x + dx, y + dy)
            h = href(x, y, dr)
            r = read_room(nc)
            if r:
                back = r[1].get(OPP[dr])
                flag = "" if back == cn else "  (!! faces back %r, expected %r)" % (back, cn)
                print("   %s %d:%d  WRITTEN %-9s answer=%-10s href=%s%s"
                      % (k, nc[0], nc[1], r[0], r[0], h, flag))
            else:
                fixed, fsrc, _ = committed_name(nc, ignore=c)
                if fixed:
                    print("   %s %d:%d  unwritten, FIXED answer=%-10s (by %s) href=%s"
                          % (k, nc[0], nc[1], fixed, fsrc[0], h))
                else:
                    print("   %s %d:%d  unwritten, NAME IT  quadrant=%-18s href=%s"
                          % (k, nc[0], nc[1], quadrant(*nc), h))
        print()

# ---------------------------------------------------------------- render
def enc(s):
    return s.replace("—", "&mdash;")

def dec(s):
    return s.replace("&mdash;", "—")

def wrap_prose(text):
    # Match the corpus house style: <p> wrapped at width 98, 4-space indent,
    # em-dashes encoded. break_on_hyphens/long_words off so words stay whole.
    body = textwrap.fill(enc(text), width=98, initial_indent="    <p>",
                         subsequent_indent="    ", break_long_words=False,
                         break_on_hyphens=False)
    return body + "</p>"

FORM = '''    <form class="riddle-box box-{d}" data-dir="{d}" data-href="{href}" data-answer="{a}" novalidate>
      <p class="riddle-dir">{label}</p>
      <p class="riddle-text">{riddle}</p>
      <label class="riddle-label" for="{iid}">Your answer</label>
      <div class="riddle-row">
        <input class="riddle-input" id="{iid}" name="{iid}" type="text" inputmode="{im}"
               autocomplete="off" autocorrect="off" autocapitalize="none" spellcheck="false"
               enterkeyhint="go" placeholder="speak the name&hellip;">
        <button class="riddle-go" type="submit">Pass</button>
      </div>
      <p class="riddle-status" role="status" aria-live="polite"></p>
    </form>'''

PAGE = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name} — Journey</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=IM+Fell+English:ital@0;1&family=IM+Fell+English+SC&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../style.css">
</head>
<body class="room">
<div class="wrap">

  <p class="room-coord">{x} : {y}</p>
  <h1 class="room-name">{name}</h1>

  <div class="prose">
{prose}
  </div>

  <div class="fleuron" role="presentation"><span>&#10086;</span></div>

  <nav class="hoard" aria-label="The four riddles of this room">
    <p class="hoard-title">four ways out &middot; speak the name to pass</p>

    <div class="room-square" aria-hidden="true">
      <span class="wall wall-top"></span>
      <span class="wall wall-right"></span>
      <span class="wall wall-bottom"></span>
      <span class="wall wall-left"></span>
      <span class="room-center">&#10086;</span>
    </div>

{forms}

    <p class="door-readout" aria-live="polite"></p>

    <noscript>
      <p class="riddle-status">The riddles need JavaScript to test your answers. The four ways:
        <a href="{ht}">north</a>, <a href="{hr}">east</a>,
        <a href="{hb}">south</a>, <a href="{hl}">west</a>.</p>
    </noscript>
  </nav>

</div>
<script src="../../rooms.js"></script>
</body>
</html>
'''

SCHEMA = '''render JSON schema — a list of rooms. Hrefs/labels/ids are computed for you.
[
  {
    "x": -1, "y": -5,
    "name": "Berry",
    "desc": "one-line hook for <meta description>.",
    "prose": "50-90 words, second person, present tense. Use - for em dashes.",
    "N": { "a": "acorn",   "lines": ["line 1", "line 2", "line 3", "line 4"] },
    "E": { "a": "sugar",   "lines": ["...", "..."] },
    "S": { "a": "honey",   "lines": ["...", "..."] },
    "W": { "a": "thistle", "lines": ["...", "..."] }
  }
]
"a" is the neighbour's name (lowercase) = the answer that opens that wall.
A numeric "a" (e.g. "7") auto-sets inputmode="numeric".'''

def render_room(rm):
    x, y = rm["x"], rm["y"]
    forms, hrefs = [], {}
    for k in ("N", "E", "S", "W"):
        dr = NESW[k]; w = rm[k]
        h = href(x, y, dr); hrefs[dr] = h
        a = str(w["a"]).strip().lower()
        im = "numeric" if a.lstrip("-").isdigit() else "text"
        riddle = "<br>\n      ".join(enc(l) for l in w["lines"])
        forms.append(FORM.format(d=dr, href=h, a=a, label=LABEL[dr], riddle=riddle, iid=IID[dr], im=im))
    return PAGE.format(name=rm["name"], desc=rm["desc"], x=x, y=y, prose=wrap_prose(rm["prose"]),
                       forms="\n\n".join(forms),
                       ht=hrefs["top"], hr=hrefs["right"], hb=hrefs["bottom"], hl=hrefs["left"])

LAST_RE = re.compile(r"^( {2})(-?\d+):(-?\d+)( {2}— {2}).*$", re.M)
def advance_tracker(x, y, name):
    txt = open(MAP, encoding="utf-8").read()
    txt2, n = LAST_RE.subn(lambda m: "%s%d:%d%s%s" % (m.group(1), x, y, m.group(4), name), txt, count=1)
    if n:
        open(MAP, "w", encoding="utf-8").write(txt2)
    return n

def check_room(c):
    """Local crossword check for one written cell. Returns list of error strings."""
    x, y = c; errs = []
    r = read_room(c)
    if not r:
        return ["%d:%d not written" % c]
    name, answers = r
    if len(set(answers.values())) != len(answers):
        errs.append("%d:%d duplicate answers %s" % (x, y, list(answers.values())))
    if not (abs(x) == 150 and abs(y) == 150) and len(answers) != 4:
        errs.append("%d:%d has %d walls" % (x, y, len(answers)))
    for d, a in answers.items():
        dx, dy = DELTA[d]; nc = (x + dx, y + dy)
        nr = read_room(nc)
        if nr:
            if nr[0] != a:
                errs.append("%d:%d %s->%s but %d:%d is named %s" % (x, y, d, a, nc[0], nc[1], nr[0]))
            back = nr[1].get(OPP[d])
            if back != name:
                errs.append("%d:%d %s->%s ; %d:%d %s->%s (want %s)" % (x, y, d, a, nc[0], nc[1], OPP[d], back, name))
    return errs

def cmd_render(args):
    track = "--no-track" not in args            # re-render a single room without moving the frontier
    args = [a for a in args if a != "--no-track"]
    if not args:
        sys.exit("usage: render batch.json [--no-track]")
    rooms = json.load(open(args[0], encoding="utf-8"))
    rooms.sort(key=lambda r: order_key((r["x"], r["y"])))   # write closest-first
    total = 0
    for rm in rooms:
        x, y = rm["x"], rm["y"]
        d = os.path.join(ROOMS, str(x))
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "%d.html" % y), "w", encoding="utf-8").write(render_room(rm))
        _CACHE.pop((x, y), None)
        n = advance_tracker(x, y, rm["name"]) if track else 1
        errs = check_room((x, y))
        flag = "  !! " + "; ".join(errs) if errs else ""
        note = "" if n else "  (tracker line not found!)"
        print("wrote rooms/%d/%d.html  %s%s%s" % (x, y, rm["name"], note, flag))
        total += 1
    print("\nrendered %d rooms; frontier now %d:%d %s" % (total, rooms[-1]["x"], rooms[-1]["y"], rooms[-1]["name"]))

DIR2K = {v: k for k, v in NESW.items()}     # dir -> author key (top->N, ...)
def parse_room(c):
    """Read a written room back into render-data (for re-rendering / normalising)."""
    t = open(cell_path(*c), encoding="utf-8").read()
    name = re.search(r'room-name">([^<]*)', t).group(1).strip()
    desc = dec(re.search(r'name="description" content="([^"]*)"', t).group(1))
    pm = re.search(r'<div class="prose">\s*<p>(.*?)</p>', t, re.S).group(1)
    prose = dec(re.sub(r"\s+", " ", pm).strip())
    rm = {"x": c[0], "y": c[1], "name": name, "desc": desc, "prose": prose}
    for fm in re.finditer(r'data-dir="([^"]*)"[^>]*data-answer="([^"]*)".*?riddle-text">(.*?)</p>', t, re.S):
        d, a, body = fm.group(1), fm.group(2), fm.group(3)
        lines = [dec(re.sub(r"\s+", " ", p).strip()) for p in body.split("<br>")]
        rm[DIR2K[d]] = {"a": a, "lines": lines}
    return rm

def cmd_normalize(args):
    """Re-render existing rooms in canonical form (fixes whitespace/entity drift).
    Does NOT touch the tracker. Use on tool-made rooms; hand-wrapped prose may re-flow."""
    coords = targets_from_args(args)
    for c in coords:
        if not exists(c):
            print("skip %d:%d (not written)" % c); continue
        rm = parse_room(c)
        open(cell_path(*c), "w", encoding="utf-8").write(render_room(rm))
        _CACHE.pop(c, None)
        errs = check_room(c)
        print("normalized %d:%d  %s%s" % (c[0], c[1], rm["name"], "  !! " + "; ".join(errs) if errs else ""))

def cmd_verify(args):
    if len(args) == 1 and args[0].endswith(".json"):
        coords = [(r["x"], r["y"]) for r in json.load(open(args[0], encoding="utf-8"))]
    else:
        coords = targets_from_args(args)
    errs = []
    for c in coords:
        errs += check_room(c)
    for e in errs:
        print("ERROR:", e)
    print("checked %d rooms; %d errors" % (len(coords), len(errs)))
    sys.exit(1 if errs else 0)

CMDS = {"next": cmd_next, "plan": cmd_plan, "render": cmd_render,
        "normalize": cmd_normalize, "verify": cmd_verify}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        sys.exit(__doc__)
    CMDS[sys.argv[1]](sys.argv[2:])
