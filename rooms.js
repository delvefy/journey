/* ==========================================================================
   JOURNEY — door logic, shared by every room.

   Each room links its four doors to neighbour coordinate files. On load we
   probe each link:
     - exists (HTTP 200)  -> "open": the door glows and reveals the room's name
     - missing (HTTP 404) -> "unwritten": a dashed door that, when chosen,
                             says the way has not been dreamt yet (no 404 page)
     - cannot probe (e.g. opened from file://, fetch throws) -> left as a plain
                             link so navigation still works offline.

   No build step, no dependencies. Include with:  <script src="../rooms.js"></script>
   ========================================================================== */
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
