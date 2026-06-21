#!/usr/bin/env python3
"""hoard.py — authoring tool for The Riddle-Hoard (see write.txt, same folder).

The whole point of this tool is to stay NEIGHBOUR-LOCAL: it never scans the
whole grid. Every command reads only the cells that touch the room you are
about to write, so the cost is O(1), not O(rooms). That keeps the
work cheap whether the hoard has 90 rooms or 90,000.

WORKFLOW — ONE ROOM AT A TIME (never in batches). Repeat this loop per room:

  1. python3 tools/hoard.py next
        -> the next unwritten coord in writing order (closest-first, ties
           clockwise from north). Pure maths + file-existence; no reads.
           (next N previews the upcoming order; it does NOT let you write ahead.)

  2. python3 tools/hoard.py plan           (or: plan -1:-5)
        -> the briefing for THAT ONE room: its COMMITTED name (what written
           neighbours already call it), and for each of its 4 walls the exact
           answer to write (a written neighbour's name, or an unwritten cell
           already fixed by some other room, or "NAME IT" + the quadrant).
           Reads only that room's neighbours (and their neighbours). This is
           all you need to author the riddle correctly.

  3. Author the ONE room as JSON (see the schema printed by `plan --schema`) and:
     python3 tools/hoard.py render room.json
        -> renders the room with the canonical skeleton, writes
           rooms/<x>/<y>.html, advances the LAST ROOM line in rooms-map.txt, and
           runs a local crossword check. render takes ONE room and REJECTS a file
           holding more than one — that is the one-at-a-time rhythm, enforced.

  4. python3 tools/hoard.py verify         (or: verify -1:-5 / room.json)
        -> re-checks that room (the frontier, if no arg) + its neighbours:
           answers match neighbour names, facing pairs agree both ways, answers
           distinct, 4 walls each.

  Then return to step 1 for the next room. Saving and tracking each room before
  starting the next is what makes the work safe to interrupt.

Coords are written "x:y" (e.g. -1:-5). The grid is bounded -150..+150.

Duplicate names are allowed but policed (see write.txt section 5): render refuses a
twin (same name as any of the 8 neighbours), a clone (same name + same 4 neighbours),
or a same-name room closer than D_MIN. The check uses tools/names.json, a coord-keyed
index render maintains incrementally. Extra commands:
  reindex  -> rebuild names.json from disk (the one full scan; run once to bootstrap)
  stats    -> per-band vocabulary usage (how close a band is to exhausting its words)
"""

import os, re, sys, math, json, textwrap

HERE = os.path.dirname(os.path.abspath(__file__))      # tools/
REPO = os.path.dirname(HERE)
ROOMS = os.path.join(REPO, "rooms")
MAP = os.path.join(HERE, "rooms-map.txt")              # tracker lives beside this script
NAMES = os.path.join(HERE, "names.json")               # duplicate-name index (incremental sidecar)
SPAN = 150
D_MIN = 15           # min Euclidean gap between two rooms sharing a name (small at first; raise as bands fill)

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

# ---------------------------------------------------------------- name index (duplicate policy)
# Duplicate room names are ALLOWED (a band's vocabulary is finite over tens of thousands of
# cells, so reuse is unavoidable) and runtime-safe. What is forbidden, to keep the puzzle honest:
#   Tier 1  no TWIN     — a name differs from all 8 surrounding cells (a twin's answer would be
#                         the current room's own visible <h1>). Checked neighbour-locally.
#   Tier 2  no CLONE    — no two rooms share a name AND the same multiset of 4 neighbour names
#                         ("identical cycle of neighbours"). Distance-independent.
#   Tier 3  MIN GAP     — two rooms sharing a name must be >= D_MIN apart.
#   (near-clone: same name + >=3 of 4 neighbours shared -> warning only.)
# names.json is a coord-keyed sidecar maintained incrementally by render; it is an ACCELERATOR,
# every conflict it flags is confirmed against the real file, so a stale index never false-rejects.
_NAME_INDEX = None
_NAME_VIEW = None

def room_signature(answers):
    """Stable signature of a room's neighbour set: its answers, sorted, lowercased, '|'-joined."""
    return "|".join(sorted(str(a).strip().lower() for a in answers.values()))

def coord_key(c):
    return "%d:%d" % (c[0], c[1])

def parse_coord_key(s):
    a, b = s.split(":")
    return (int(a), int(b))

def load_index():
    """Load names.json (cached). Fail-open: missing/corrupt -> empty index (advisory only)."""
    global _NAME_INDEX
    if _NAME_INDEX is not None:
        return _NAME_INDEX
    try:
        idx = json.load(open(NAMES, encoding="utf-8"))
        if not isinstance(idx.get("rooms"), dict):
            raise ValueError("missing rooms map")
        _NAME_INDEX = idx
    except FileNotFoundError:
        _NAME_INDEX = {"version": 1, "rooms": {}}
    except Exception as e:
        sys.stderr.write("warning: names.json unreadable (%s); run `hoard.py reindex`.\n" % e)
        _NAME_INDEX = {"version": 1, "rooms": {}}
    return _NAME_INDEX

def save_index(idx):
    tmp = NAMES + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(idx, f, indent=1, sort_keys=True)
    os.replace(tmp, NAMES)

def name_view(idx):
    """name -> [coord_key, ...] built once per process from the coord-keyed index."""
    global _NAME_VIEW
    if _NAME_VIEW is None:
        v = {}
        for k, e in idx["rooms"].items():
            v.setdefault(e["name"], []).append(k)
        _NAME_VIEW = v
    return _NAME_VIEW

def index_put(idx, c, name, sig):
    global _NAME_VIEW
    idx["rooms"][coord_key(c)] = {"name": name.strip().lower(), "sig": sig}
    _NAME_VIEW = None

def names_within(idx, c, radius):
    """Set of names sitting strictly within `radius` of c (excludes c). Box scan, O(radius^2)."""
    x, y = c; r = int(math.ceil(radius)); rooms = idx["rooms"]; out = set()
    for dx in range(-r, r + 1):
        for dy in range(-r, r + 1):
            if dx == 0 and dy == 0:
                continue
            e = rooms.get("%d:%d" % (x + dx, y + dy))
            if e and math.hypot(dx, dy) < radius:
                out.add(e["name"])
    return out

def _overlap(a, b):
    from collections import Counter
    return sum((Counter(a) & Counter(b)).values())

def policy_violations(c, name, sig, idx, d_min):
    """(hard_errors, warnings) for placing name/sig at c. Every index hit is confirmed on disk."""
    hard, warn = [], []
    x, y = c; lname = name.strip().lower(); mine = sig.split("|")
    twin = set()
    # Tier 1: twin among the 8 surrounding cells (authoritative neighbour reads; index-independent).
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            oc = (x + dx, y + dy)
            nr = read_room(oc)
            if nr and nr[0] == lname:
                kind = "orthogonal" if dx == 0 or dy == 0 else "diagonal"
                hard.append("twin: %s neighbour %d:%d also named %r" % (kind, oc[0], oc[1], lname))
                twin.add(oc)
    # Tier 2/3 via the index, each candidate CONFIRMED against the real file (no false rejects).
    for k in name_view(idx).get(lname, []):
        if k == coord_key(c):
            continue
        oc = parse_coord_key(k); e = idx["rooms"][k]
        rr = read_room(oc)
        if not rr or rr[0] != lname:
            continue                                   # stale index entry — ignore
        rsig = room_signature(rr[1])
        if rsig == sig:
            hard.append("clone of %d:%d (same name + identical neighbours %r)" % (oc[0], oc[1], sig))
            continue
        dist = math.hypot(oc[0] - x, oc[1] - y)
        if dist >= 2 and dist < d_min and oc not in twin:
            hard.append("too close: %r also at %d:%d (dist %.2f < D_min %g)" % (lname, oc[0], oc[1], dist, d_min))
        if _overlap(mine, rsig.split("|")) >= 3:
            warn.append("near-clone of %d:%d (3+ of 4 neighbours shared)" % (oc[0], oc[1]))
    return hard, warn

def audit_index(idx):
    """List existing twin/clone/close-pair violations across the whole index (used by reindex)."""
    out = []
    byname = {}
    for k, e in idx["rooms"].items():
        byname.setdefault(e["name"], []).append((parse_coord_key(k), e["sig"]))
    for name, lst in byname.items():
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                (c1, s1), (c2, s2) = lst[i], lst[j]
                dist = math.hypot(c1[0] - c2[0], c1[1] - c2[1])
                if s1 == s2:
                    out.append("CLONE %r %d:%d == %d:%d" % (name, c1[0], c1[1], c2[0], c2[1]))
                if dist < 2:
                    out.append("TWIN  %r %d:%d ~ %d:%d (dist %.2f)" % (name, c1[0], c1[1], c2[0], c2[1], dist))
                elif dist < D_MIN:
                    out.append("CLOSE %r %d:%d ~ %d:%d (dist %.2f < %g)" % (name, c1[0], c1[1], c2[0], c2[1], dist, D_MIN))
    return out

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
    idx = load_index()
    for c in (targets_from_args(args) or next_unwritten(1)):
        x, y = c
        d = math.hypot(x, y)
        cn, src, conflict = committed_name(c)
        tag = "" if cn else "  (no inward neighbour written — you choose the name)"
        print("== %d:%d   d=%.3f  band=%s  quadrant=%s%s" % (x, y, d, band(d), quadrant(x, y), tag))
        if cn:
            warn = "  *** CONFLICT ***" if conflict else ""
            print("   name MUST be: %-10s [%s]%s" % (cn, ", ".join(src), warn))
            others = [parse_coord_key(k) for k in name_view(idx).get(cn, []) if k != coord_key(c)]
            if others:
                nr = min(others, key=lambda o: math.hypot(o[0] - x, o[1] - y))
                print("     (name %r already used %d place(s); nearest %d:%d, dist %.1f)"
                      % (cn, len(others), nr[0], nr[1], math.hypot(nr[0] - x, nr[1] - y)))
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
                    taken = names_within(idx, nc, D_MIN)
                    if taken:
                        print("        avoid here (names within D_min=%g): %s"
                              % (D_MIN, ", ".join(sorted(taken))))
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

SCHEMA = '''render JSON schema — ONE room object (write rooms one at a time, never in batches).
Hrefs/labels/input ids are computed for you; you supply only the content.
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
"a" is the neighbour's name (lowercase) = the answer that opens that wall.
A numeric "a" (e.g. "7") auto-sets inputmode="numeric".
(A one-element list is also accepted; a file holding more than one room is rejected.)'''

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

def tracker_frontier():
    """The LAST ROOM coord recorded in the tracker (the room just written), or None."""
    m = LAST_RE.search(open(MAP, encoding="utf-8").read())
    return (int(m.group(2)), int(m.group(3))) if m else None

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
    for dx in (-1, 0, 1):                       # Tier 1: no twin among the 8 surrounding cells
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nr = read_room((x + dx, y + dy))
            if nr and nr[0] == name:
                kind = "orthogonal" if dx == 0 or dy == 0 else "diagonal"
                errs.append("%d:%d twin: %s neighbour %d:%d also named %s" % (x, y, kind, x + dx, y + dy, name))
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
    track = "--no-track" not in args            # re-render one room without moving the frontier
    args = [a for a in args if a != "--no-track"]
    d_min = D_MIN
    if "--d-min" in args:                       # tune the same-name minimum gap for this render
        i = args.index("--d-min"); d_min = float(args[i + 1]); del args[i:i + 2]
    if not args:
        sys.exit("usage: render room.json [--no-track] [--d-min N]   (one room at a time)")
    data = json.load(open(args[0], encoding="utf-8"))
    rooms = data if isinstance(data, list) else [data]
    if len(rooms) != 1:                         # the rule, enforced: never write in batches
        sys.exit("render writes ONE room at a time, never in batches — found %d rooms in %s.\n"
                 "Author, render, save and track each room on its own, then go to the next.\n"
                 "(Write rooms one at a time — see write.txt section 2.)" % (len(rooms), args[0]))
    rm = rooms[0]
    x, y = rm["x"], rm["y"]
    # Duplicate-name policy gate — runs BEFORE writing, so disk/tracker/index never hold a known
    # twin/clone/too-close room. Signature is computed from the authored answers (all known now).
    name = str(rm["name"]).strip().lower()
    ans = {NESW[k]: str(rm[k]["a"]).strip().lower() for k in ("N", "E", "S", "W") if k in rm}
    sig = room_signature(ans)
    idx = load_index()
    hard, warn = policy_violations((x, y), name, sig, idx, d_min)
    for w in warn:
        print("WARN:", w)
    if hard:
        for h in hard:
            print("!!", h)
        sys.exit("render aborted: duplicate-name policy (%d issue%s) — nothing written, tracker unchanged.\n"
                 "Rename this cell, or pass --d-min to relax the gap. See write.txt section 5."
                 % (len(hard), "" if len(hard) == 1 else "s"))
    d = os.path.join(ROOMS, str(x))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "%d.html" % y), "w", encoding="utf-8").write(render_room(rm))
    _CACHE.pop((x, y), None)
    index_put(idx, (x, y), name, sig); save_index(idx)
    n = advance_tracker(x, y, rm["name"]) if track else 1
    errs = check_room((x, y))
    flag = "  !! " + "; ".join(errs) if errs else ""
    note = "" if n else "  (tracker line not found!)"
    print("wrote rooms/%d/%d.html  %s%s%s" % (x, y, rm["name"], note, flag))
    print("tracker not advanced (--no-track)" if not track else
          "frontier now %d:%d %s" % (x, y, rm["name"]))

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
    idx = load_index()
    for c in coords:
        if not exists(c):
            print("skip %d:%d (not written)" % c); continue
        rm = parse_room(c)
        open(cell_path(*c), "w", encoding="utf-8").write(render_room(rm))
        _CACHE.pop(c, None)
        r = read_room(c)                        # keep the name index consistent (no policy gate here)
        if r:
            index_put(idx, c, r[0], room_signature(r[1]))
        errs = check_room(c)
        print("normalized %d:%d  %s%s" % (c[0], c[1], rm["name"], "  !! " + "; ".join(errs) if errs else ""))
    save_index(idx)

def cmd_verify(args):
    if len(args) == 1 and args[0].endswith(".json"):
        data = json.load(open(args[0], encoding="utf-8"))
        rooms = data if isinstance(data, list) else [data]
        coords = [(r["x"], r["y"]) for r in rooms]
    else:
        coords = targets_from_args(args)
    if not coords:                                  # no arg -> the room you just wrote
        f = tracker_frontier()
        coords = [f] if f else []
    errs = []
    for c in coords:
        errs += check_room(c)
    for e in errs:
        print("ERROR:", e)
    print("checked %d rooms; %d errors" % (len(coords), len(errs)))
    sys.exit(1 if errs else 0)

def cmd_reindex(args):
    """Rebuild names.json from every room on disk — the ONE sanctioned full scan (bootstrap/repair)."""
    global _NAME_INDEX, _NAME_VIEW
    idx = {"version": 1, "rooms": {}}
    count = 0
    for root, _dirs, files in os.walk(ROOMS):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            try:
                cx = int(os.path.basename(root)); cy = int(fn[:-5])
            except ValueError:
                continue
            r = read_room((cx, cy))
            if not r or not r[0]:
                continue
            idx["rooms"][coord_key((cx, cy))] = {"name": r[0], "sig": room_signature(r[1])}
            count += 1
    save_index(idx)
    _NAME_INDEX, _NAME_VIEW = idx, None
    distinct = len({e["name"] for e in idx["rooms"].values()})
    print("reindexed %d rooms; %d distinct names -> %s" % (count, distinct, os.path.relpath(NAMES, REPO)))
    issues = audit_index(idx)
    if issues:
        print("policy issues found (%d):" % len(issues))
        for s in issues:
            print("  " + s)
    else:
        print("no twin / clone / too-close violations.")

def cmd_stats(args):
    """Per-band vocabulary telemetry from the index: how saturated each band's word-supply is."""
    idx = load_index()
    bands = {}
    for k, e in idx["rooms"].items():
        x, y = parse_coord_key(k)
        b = bands.setdefault(band(math.hypot(x, y)), {})
        b[e["name"]] = b.get(e["name"], 0) + 1
    for b in ("Threshold", "Approach", "Near Hoard", "Deep Hoard", "Far Reaches", "Rim", "Apex (corner)"):
        if b not in bands:
            continue
        names = bands[b]; total = sum(names.values())
        reused = sorted((n for n in names if names[n] > 1), key=lambda n: -names[n])
        top = "  top: " + ", ".join("%s x%d" % (n, names[n]) for n in reused[:5]) if reused else ""
        print("%-14s rooms=%-6d distinct=%-6d max-reuse=%-3d%s"
              % (b, total, len(names), max(names.values()), top))

CMDS = {"next": cmd_next, "plan": cmd_plan, "render": cmd_render,
        "normalize": cmd_normalize, "verify": cmd_verify,
        "reindex": cmd_reindex, "stats": cmd_stats}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        sys.exit(__doc__)
    CMDS[sys.argv[1]](sys.argv[2:])
