/* Theme toggle. The initial theme is set inline in <head> (see build.py's
   THEME_INIT) to avoid a flash; this only wires up the toggle button and
   persists the choice. */
(function () {
  var root = document.documentElement;
  var btn = document.querySelector(".theme-toggle");
  if (!btn) return;

  function apply(theme) {
    root.setAttribute("data-theme", theme);
    try { localStorage.setItem("theme", theme); } catch (e) {}
    btn.textContent = theme === "dark" ? "☀" : "☾";
    btn.setAttribute("aria-label", "Switch to " + (theme === "dark" ? "light" : "dark") + " theme");
  }

  // sync the icon with whatever the inline script already set
  apply(root.getAttribute("data-theme") || "light");

  btn.addEventListener("click", function () {
    apply(root.getAttribute("data-theme") === "dark" ? "light" : "dark");
  });
})();
