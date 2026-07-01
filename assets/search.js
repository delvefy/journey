/* Homepage search. Loads search-index.json (emitted by build.py) and filters
   it live in the browser. No dependencies; scores by field weight so title
   and tag hits rank above summary hits. */
(function () {
  var input = document.getElementById("search-input");
  var results = document.getElementById("search-results");
  if (!input || !results) return;

  var docs = [];
  var active = -1;

  fetch("search-index.json")
    .then(function (r) { return r.json(); })
    .then(function (data) { docs = data; })
    .catch(function () { /* index missing — search stays inert */ });

  function score(doc, q) {
    var s = 0;
    var title = (doc.title || "").toLowerCase();
    var uni = (doc.universe || "").toLowerCase();
    var type = (doc.type || "").toLowerCase();
    var summary = (doc.summary || "").toLowerCase();
    var tags = (doc.tags || []).join(" ").toLowerCase();

    if (title === q) s += 100;
    if (title.indexOf(q) === 0) s += 40;
    if (title.indexOf(q) !== -1) s += 20;
    if (tags.indexOf(q) !== -1) s += 12;
    if (uni.indexOf(q) !== -1) s += 8;
    if (type.indexOf(q) !== -1) s += 6;
    if (summary.indexOf(q) !== -1) s += 4;
    return s;
  }

  function render(matches) {
    if (!matches.length) {
      results.innerHTML = '<li class="r-empty">No articles found.</li>';
      results.hidden = false;
      return;
    }
    results.innerHTML = matches.map(function (m, i) {
      return '<li><a class="' + (i === active ? "active" : "") + '" href="' + m.url + '">' +
        '<span class="r-title">' + esc(m.title) + '</span>' +
        '<span class="r-meta">' + esc(m.universe) + (m.type ? " · " + esc(m.type) : "") + '</span>' +
        '</a></li>';
    }).join("");
    results.hidden = false;
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function run() {
    var q = input.value.trim().toLowerCase();
    active = -1;
    if (!q) { results.hidden = true; results.innerHTML = ""; return; }
    var matches = docs
      .map(function (d) { return { doc: d, s: score(d, q) }; })
      .filter(function (x) { return x.s > 0; })
      .sort(function (a, b) { return b.s - a.s || a.doc.title.localeCompare(b.doc.title); })
      .slice(0, 10)
      .map(function (x) { return x.doc; });
    render(matches);
  }

  input.addEventListener("input", run);

  input.addEventListener("keydown", function (e) {
    var items = results.querySelectorAll("a");
    if (!items.length) return;
    if (e.key === "ArrowDown") { e.preventDefault(); active = Math.min(active + 1, items.length - 1); }
    else if (e.key === "ArrowUp") { e.preventDefault(); active = Math.max(active - 1, 0); }
    else if (e.key === "Enter") { if (active >= 0) { e.preventDefault(); items[active].click(); } return; }
    else if (e.key === "Escape") { results.hidden = true; return; }
    else return;
    items.forEach(function (a, i) { a.classList.toggle("active", i === active); });
  });

  document.addEventListener("click", function (e) {
    if (!results.contains(e.target) && e.target !== input) results.hidden = true;
  });
  input.addEventListener("focus", function () { if (input.value.trim()) run(); });
})();
