/* ==========================================================================
   JOURNEY — shared room script. Two independent pieces, both keyed off the
   single <script src="../../rooms.js"> every room includes:

   1. PALETTE ENGINE. The world is a plane: x = NATURAL(-) .. WROUGHT(+),
      y = TANGIBLE(-) .. INTANGIBLE(+), each running -150..+150 (see tools/write.txt).
      A room's colours are not authored — they are interpolated from its
      coordinates between four corner palettes and a CENTRE that holds near the
      origin. So the look drifts a hair with every room, and the four corners
      feel like four kinds of answer.

   2. RIDDLE LOGIC. Each room has four .riddle-box <form>s, one per wall. Each
      box carries the neighbour it leads to (data-href) and that neighbour's
      name (data-answer) — the single word/number that opens the wall. On load
      we probe each neighbour file so its little wall-marker can show:
        - exists (HTTP 200)  -> "open": the wall glows
        - missing (HTTP 404) -> "undreamt": a dashed, not-yet-written wall
      On submit we compare the typed word to data-answer; a match walks you
      through, a miss leaves the room shut. Answers are plaintext on purpose.

   No build step, no dependencies. The palette degrades gracefully: with JS off
   every page simply keeps the medieval :root base in style.css.
   ========================================================================== */

/* -------------------------------------------------------------------------
   1. PALETTE ENGINE
   ------------------------------------------------------------------------- */
(function () {
  "use strict";

  // Themeable tokens, each an [r,g,b] (--glow is [r,g,b,a]) at five anchors:
  // the four corners of the natural(-x)..wrought(+x) by tangible(-y)..intangible(+y)
  // plane, plus CENTRE (held near the origin). To retune a region, edit here.
  var ANCHOR = {
    //               paper          paper-raised   paper-edge     ink              ink-dim         ink-faint     amber           amber-bright     amber-deep    rule           rule-strong   glow
    // SW: natural + tangible — stone, root, river, earth (warm umber ground)
    sw: { paper:[22,20,15],  raised:[32,29,22],  edge:[12,11,8],  ink:[201,196,181], dim:[138,133,120], faint:[85,81,74],  amber:[154,142,116], bright:[179,169,140], deep:[91,84,68],  rule:[44,42,35],  strong:[65,61,51],  glow:[154,142,116,0.07] },
    // SE: wrought + tangible — bell, key, coin, blade (forge green-gold)
    se: { paper:[18,24,15],  raised:[27,36,22],  edge:[10,14,7],  ink:[232,237,202], dim:[169,180,135], faint:[105,115,78], amber:[216,185,74],  bright:[240,213,106], deep:[74,125,66], rule:[44,58,34],  strong:[66,84,49],  glow:[116,196,116,0.20] },
    // NW: natural + intangible — wind, frost, tide, dusk (pale cold air)
    nw: { paper:[14,16,20],  raised:[23,26,33],  edge:[8,9,12],   ink:[221,228,236], dim:[147,157,171], faint:[86,94,110], amber:[142,166,187], bright:[183,202,219], deep:[65,80,95],  rule:[34,38,46],  strong:[52,59,70],  glow:[142,166,187,0.13] },
    // NE: wrought + intangible — name, hour, debt, secret (deep arcane ink)
    ne: { paper:[10,11,18],  raised:[18,19,32],  edge:[5,5,9],    ink:[217,232,242], dim:[130,143,176], faint:[76,85,120], amber:[60,224,200],  bright:[120,242,221], deep:[224,168,50], rule:[26,32,50],  strong:[43,53,86],  glow:[60,224,200,0.22] },
    // CENTRE: the threshold at the origin — matches style.css :root exactly
    c:  { paper:[28,22,16],  raised:[37,30,21],  edge:[21,16,11], ink:[231,220,195], dim:[168,152,118], faint:[111,98,72], amber:[224,168,50],  bright:[240,188,78],  deep:[156,114,24], rule:[70,58,39],  strong:[93,77,51],  glow:[224,168,50,0.18] }
  };

  // token key in ANCHOR -> CSS custom property name
  var VARS = {
    paper: "--paper", raised: "--paper-raised", edge: "--paper-edge",
    ink: "--ink", dim: "--ink-dim", faint: "--ink-faint",
    amber: "--amber", bright: "--amber-bright", deep: "--amber-deep",
    rule: "--rule", strong: "--rule-strong", glow: "--glow"
  };

  var SPAN = 150;        // axes run -SPAN..+SPAN
  var CORE = 30;         // within this radius the medieval centre dominates

  function clamp01(t) { return t < 0 ? 0 : t > 1 ? 1 : t; }
  function lerp(a, b, t) { return a + (b - a) * t; }

  function mix(a, b, t) {
    var out = [];
    for (var i = 0; i < a.length; i++) out[i] = lerp(a[i], b[i], t);
    return out;
  }

  function toCss(c) {
    var r = Math.round(c[0]), g = Math.round(c[1]), b = Math.round(c[2]);
    if (c.length > 3) return "rgba(" + r + "," + g + "," + b + "," + (Math.round(c[3] * 1000) / 1000) + ")";
    return "rgb(" + r + "," + g + "," + b + ")";
  }

  // (x,y) from the sharded path "rooms/<x>/<y>.html" (the canonical coordinate):
  // x is the parent folder, y is the file basename. Fall back to the
  // ".room-coord" text "X : Y" (file://, odd paths); give up (cover) -> null.
  function readCoords() {
    var segs = (location.pathname || "").split("/").filter(Boolean);
    if (segs.length >= 2) {
      var xs = segs[segs.length - 2];
      var ys = segs[segs.length - 1].replace(/\.html?$/i, "");
      if (/^-?\d+$/.test(xs) && /^-?\d+$/.test(ys)) {
        return [parseInt(xs, 10), parseInt(ys, 10)];
      }
    }
    var el = document.querySelector(".room-coord");
    if (el) {
      var m = /(-?\d+)\s*:\s*(-?\d+)/.exec(el.textContent || "");
      if (m) return [parseInt(m[1], 10), parseInt(m[2], 10)];
    }
    return null;
  }

  var coords = readCoords();
  if (!coords) return; // cover / unknown: keep the medieval :root base

  var x = coords[0], y = coords[1];
  var tx = clamp01((x + SPAN) / (2 * SPAN));   // 0 = west/natural,  1 = east/wrought
  var ty = clamp01((y + SPAN) / (2 * SPAN));   // 0 = south/tangible, 1 = north/intangible
  var cw = clamp01(1 - Math.max(Math.abs(x), Math.abs(y)) / CORE); // centre weight

  var root = document.documentElement;
  var body = document.body;
  // suppress the body colour transition for this initial set, so each room
  // loads already in its palette rather than fading up from medieval.
  var savedTransition = body ? body.style.transition : "";
  if (body) body.style.transition = "none";

  Object.keys(VARS).forEach(function (k) {
    var south = mix(ANCHOR.sw[k], ANCHOR.se[k], tx);  // y low
    var north = mix(ANCHOR.nw[k], ANCHOR.ne[k], tx);  // y high
    var corner = mix(south, north, ty);
    var color = mix(corner, ANCHOR.c[k], cw);         // pull toward medieval near origin
    root.style.setProperty(VARS[k], toCss(color));
  });

  if (body) {
    void body.offsetHeight;            // force a reflow before re-enabling
    body.style.transition = savedTransition; // restore stylesheet transition
  }
})();

/* -------------------------------------------------------------------------
   2. RIDDLE LOGIC
   ------------------------------------------------------------------------- */
(function () {
  "use strict";

  var DIR = { top: "North", right: "East", bottom: "South", left: "West" };
  var MISSES = [
    "The wall does not stir.",
    "Not the word the hoard wants.",
    "The lock holds. Try the name again.",
    "That is not its name."
  ];

  var boxes = Array.prototype.slice.call(document.querySelectorAll(".riddle-box"));
  if (!boxes.length) return;            // no riddles here (e.g. the 404 page)

  var square = document.querySelector(".room-square"); // absent on the cover
  var readout = document.querySelector(".door-readout");
  var missAt = 0;

  function setReadout(text) { if (readout) readout.textContent = text || ""; }

  // DOOR-SELECT MODE. A real room (it has the .room-square) shows ONE riddle at
  // a time: the four walls become doors, and tapping a door reveals just that
  // wall's riddle, highlights the door, and hides the rest. Tap the open door
  // again to close it. Undreamt doors (neighbour 404) are disabled. The cover
  // has no square, so it keeps its single, always-shown riddle.
  var interactive = !!square;
  var byDir = {};               // dir -> { box, wall, input, undreamt }
  var selectedDir = null;
  var PROMPT = "Choose a door to face its riddle.";

  if (interactive) {
    var hoard = document.querySelector(".hoard");
    if (hoard) hoard.classList.add("is-interactive");
    square.classList.add("is-interactive");
    square.removeAttribute("aria-hidden");      // the doors are now operable
    square.setAttribute("role", "group");
    square.setAttribute("aria-label", "The four doors of this room — choose one to face its riddle");
    var center = square.querySelector(".room-center");
    if (center) center.setAttribute("aria-hidden", "true");
    setReadout(PROMPT);
  }

  function reflectSelection() {
    Object.keys(byDir).forEach(function (d) {
      var e = byDir[d], on = d === selectedDir;
      if (e.wall) {
        e.wall.classList.toggle("is-selected", on);
        e.wall.setAttribute("aria-pressed", on ? "true" : "false");
      }
      if (e.box) e.box.classList.toggle("is-selected", on);
    });
  }

  function selectDoor(dir) {
    var entry = byDir[dir];
    if (!entry) return;
    if (entry.undreamt) { setReadout("That way is not yet dreamt."); return; }
    if (selectedDir === dir) {            // tap the open door again -> close it
      selectedDir = null;
      reflectSelection();
      setReadout(PROMPT);
      if (entry.wall) entry.wall.focus();
      return;
    }
    selectedDir = dir;
    reflectSelection();
    setReadout("");
    if (entry.input) entry.input.focus();
  }

  // SIMPLEST normalisation: case, trim, and inner whitespace only — nothing
  // fancier (no accent folding, no punctuation stripping). Answers are authored
  // lowercase so the comparison is symmetric.
  function normalize(s) {
    return (s || "").toLowerCase().trim().replace(/\s+/g, " ");
  }

  function setStatus(box, state, text) {
    var el = box.querySelector(".riddle-status");
    box.classList.remove("is-wrong", "is-correct");
    if (state) box.classList.add(state);
    if (el) el.textContent = text || "";
  }

  boxes.forEach(function (box) {
    var dir = box.getAttribute("data-dir");
    var label = DIR[dir] || "";
    var href = box.getAttribute("data-href");
    var answer = normalize(box.getAttribute("data-answer"));
    var input = box.querySelector(".riddle-input");
    var wall = square && dir ? square.querySelector(".wall-" + dir) : null;

    // make the wall a tappable door (real rooms only; the cover has no square)
    if (interactive && dir) {
      byDir[dir] = { box: box, wall: wall, input: input, undreamt: false };
      if (wall) {
        wall.classList.add("door");
        wall.setAttribute("role", "button");
        wall.setAttribute("tabindex", "0");
        wall.setAttribute("aria-pressed", "false");
        wall.setAttribute("aria-label", (label || "This") + " door");
        wall.addEventListener("click", function () { selectDoor(dir); });
        wall.addEventListener("keydown", function (e) {
          if (e.key === "Enter" || e.key === " " || e.key === "Spacebar") {
            e.preventDefault();
            selectDoor(dir);
          }
        });
      }
    }

    // probe the neighbour file so the wall-marker can show written vs undreamt
    if (href) {
      fetch(href, { cache: "no-store" })
        .then(function (res) {
          if (res.ok) {
            box.classList.add("neighbor-written");
            if (wall) wall.classList.add("is-open");
          } else if (res.status === 404) {
            box.classList.add("neighbor-undreamt");
            if (wall) wall.classList.add("is-undreamt");
            if (interactive && byDir[dir]) {
              byDir[dir].undreamt = true;        // this door is now disabled
              if (wall) {
                wall.classList.add("is-disabled");
                wall.setAttribute("aria-disabled", "true");
                wall.setAttribute("tabindex", "-1");
                wall.setAttribute("aria-label", (label || "This") + " door — not yet dreamt");
              }
              if (selectedDir === dir) {         // open when we learned it's undreamt
                selectedDir = null;
                reflectSelection();
                setReadout("That way is not yet dreamt.");
              }
            }
          }
        })
        .catch(function () { /* file:// or offline — leave neutral, still solvable */ });
    }

    box.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!input) return;
      var guess = normalize(input.value);
      if (!guess) { setStatus(box, "", "…the box waits for a word."); return; }

      if (guess === answer) {
        var opening = label ? "The " + label.toLowerCase() + " way opens…" : "The way opens…";
        setStatus(box, "is-correct", "Correct. " + opening);
        if (wall) wall.classList.add("is-open");
        input.setAttribute("readonly", "");
        if (box.classList.contains("neighbor-undreamt")) {
          setReadout(label + " — the name is true, but that room is not yet dreamt");
        }
        if (href) window.location.assign(href);   // 404.html catches the undreamt case
      } else {
        setStatus(box, "is-wrong", MISSES[missAt++ % MISSES.length]);
        input.select();
        // clear the wrong-cue as soon as they start typing again
        input.addEventListener("input", function () {
          box.classList.remove("is-wrong");
        }, { once: true });
      }
    });
  });
})();
