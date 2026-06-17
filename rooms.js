/* ==========================================================================
   JOURNEY — shared room script. Two independent pieces, both keyed off the
   single <script src="../../rooms.js"> every room includes:

   1. PALETTE ENGINE. The world is a plane: y = TECH, x = MAGIC, each running
      -150..+150 (see write.txt). A room's colours are not authored — they are
      interpolated from its coordinates between four corner palettes (the genre
      poles) and a medieval CENTRE that holds near the origin. So the look
      drifts a hair with every door, and the four corners feel like four worlds.

   2. DOOR LOGIC. Each room links its four doors to neighbour coordinate files.
      On load we probe each link:
        - exists (HTTP 200)  -> "open": the door glows and reveals the room name
        - missing (HTTP 404) -> "unwritten": a dashed door that, when chosen,
                                says the way has not been dreamt yet
        - cannot probe (file://, fetch throws) -> left a plain navigable link

   No build step, no dependencies. The palette degrades gracefully: with JS off
   every page simply keeps the medieval :root base in style.css.
   ========================================================================== */

/* -------------------------------------------------------------------------
   1. PALETTE ENGINE
   ------------------------------------------------------------------------- */
(function () {
  "use strict";

  // Themeable tokens, each an [r,g,b] (--glow is [r,g,b,a]) at five anchors:
  // the four corners of the tech(y) x magic(x) plane, plus CENTRE (= the
  // medieval :root base, held near the origin). To retune a region, edit here.
  var ANCHOR = {
    //               paper          paper-raised   paper-edge     ink              ink-dim         ink-faint     amber           amber-bright     amber-deep    rule           rule-strong   glow
    // SW: low tech, no magic — The Waste (ash, ruin, the mundane void)
    sw: { paper:[22,20,15],  raised:[32,29,22],  edge:[12,11,8],  ink:[201,196,181], dim:[138,133,120], faint:[85,81,74],  amber:[154,142,116], bright:[179,169,140], deep:[91,84,68],  rule:[44,42,35],  strong:[65,61,51],  glow:[154,142,116,0.07] },
    // SE: low tech, high magic — The Wyld (myth, age of wonders, no gear)
    se: { paper:[18,24,15],  raised:[27,36,22],  edge:[10,14,7],  ink:[232,237,202], dim:[169,180,135], faint:[105,115,78], amber:[216,185,74],  bright:[240,213,106], deep:[74,125,66], rule:[44,58,34],  strong:[66,84,49],  glow:[116,196,116,0.20] },
    // NW: high tech, no magic — The Chrome (sterile, dead neon, cold machine)
    nw: { paper:[14,16,20],  raised:[23,26,33],  edge:[8,9,12],   ink:[221,228,236], dim:[147,157,171], faint:[86,94,110], amber:[142,166,187], bright:[183,202,219], deep:[65,80,95],  rule:[34,38,46],  strong:[52,59,70],  glow:[142,166,187,0.13] },
    // NE: high tech, high magic — The Lumen (magitech, arcane engines of light)
    ne: { paper:[10,11,18],  raised:[18,19,32],  edge:[5,5,9],    ink:[217,232,242], dim:[130,143,176], faint:[76,85,120], amber:[60,224,200],  bright:[120,242,221], deep:[224,168,50], rule:[26,32,50],  strong:[43,53,86],  glow:[60,224,200,0.22] },
    // CENTRE: the medieval Antechamber — matches style.css :root exactly
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
  var tx = clamp01((x + SPAN) / (2 * SPAN));   // 0 = west/no-magic, 1 = east/high-magic
  var ty = clamp01((y + SPAN) / (2 * SPAN));   // 0 = south/no-tech,  1 = north/high-tech
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
   2. DOOR LOGIC
   ------------------------------------------------------------------------- */
(function () {
  "use strict";

  var DIR = { top: "North", right: "East", bottom: "South", left: "West" };

  var doors = Array.prototype.slice.call(document.querySelectorAll(".door[href]"));
  var readout = document.querySelector(".door-readout");

  function setReadout(text) { if (readout) readout.textContent = text || ""; }

  function dirOf(door) {
    for (var i = 0; i < door.classList.length; i++) {
      var m = /^door-(top|right|bottom|left)$/.exec(door.classList[i]);
      if (m) return m[1];
    }
    return null;
  }

  // pull the neighbour's name out of fetched HTML, so an open door can name it
  function extractName(html) {
    var m = /<h1[^>]*class="[^"]*room-name[^"]*"[^>]*>([\s\S]*?)<\/h1>/i.exec(html);
    if (m) return m[1].replace(/<[^>]+>/g, "").trim();
    var t = /<title>([\s\S]*?)<\/title>/i.exec(html);
    if (t) return t[1].replace(/\s*[—\-]\s*Journey\s*$/i, "").trim();
    return "";
  }

  doors.forEach(function (door) {
    var dir = dirOf(door);
    var label = dir ? DIR[dir] : "";
    door.setAttribute("aria-label", label + " door");

    function readoutFor() {
      if (door.classList.contains("is-unwritten")) {
        setReadout(label + " — undreamt");
      } else {
        setReadout(label + (door.dataset.name ? " — " + door.dataset.name : ""));
      }
    }
    door.addEventListener("mouseenter", readoutFor);
    door.addEventListener("focus", readoutFor);
    door.addEventListener("mouseleave", function () { setReadout(""); });
    door.addEventListener("blur", function () { setReadout(""); });

    fetch(door.getAttribute("href"), { cache: "no-store" })
      .then(function (res) {
        if (res.ok) return res.text();
        if (res.status === 404) {
          door.classList.add("is-unwritten");
          door.addEventListener("click", function (e) {
            e.preventDefault();
            setReadout("Beyond the " + label.toLowerCase() + " door, nothing has been dreamt yet.");
          });
        }
        return null; // other statuses: leave as a plain link
      })
      .then(function (html) {
        if (!html) return;
        door.classList.add("is-open");
        var name = extractName(html);
        if (name) {
          door.dataset.name = name;
          door.title = name;
          door.setAttribute("aria-label", label + " door — " + name);
        }
      })
      .catch(function () { /* cannot probe — leave navigable */ });
  });
})();
