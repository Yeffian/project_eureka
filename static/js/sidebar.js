// Foldable sidebar: toggles data-sidebar on <html>, persists in localStorage.
(function () {
  const html = document.documentElement;
  const toggle = document.getElementById("sidebar-toggle");
  if (!toggle) return;

  const saved = localStorage.getItem("eureka-sidebar");
  if (saved === "collapsed") {
    html.setAttribute("data-sidebar", "collapsed");
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Expand menu");
  }

  toggle.addEventListener("click", () => {
    const collapsed = html.getAttribute("data-sidebar") === "collapsed";
    if (collapsed) {
      html.removeAttribute("data-sidebar");
      toggle.setAttribute("aria-expanded", "true");
      toggle.setAttribute("aria-label", "Collapse menu");
      localStorage.setItem("eureka-sidebar", "expanded");
    } else {
      html.setAttribute("data-sidebar", "collapsed");
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Expand menu");
      localStorage.setItem("eureka-sidebar", "collapsed");
    }
  });
})();
