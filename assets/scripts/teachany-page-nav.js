/*! TeachAny 页内导航行为 · v1.0
 *  容器：<nav class="ta-pagenav" data-teachany-page-nav>
 *        内含 <ol> 目录（<a href="#id">）与 [data-pagenav-prev]/[data-pagenav-next] 按钮。
 *  职责：滚动时高亮当前章节 + 上一节/下一节跳转。不改动页面原有结构。
 */
(function () {
  "use strict";
  if (window.__teachAnyPageNav) return;
  window.__teachAnyPageNav = true;

  function init() {
    var navs = document.querySelectorAll("[data-teachany-page-nav]");
    Array.prototype.forEach.call(navs, function (nav) {
      if (nav.dataset.taNavReady === "1") return;
      var links = Array.prototype.slice.call(nav.querySelectorAll("ol a[href^='#']"));
      var targets = links
        .map(function (a) {
          var id = decodeURIComponent(a.getAttribute("href").slice(1));
          var el = id ? document.getElementById(id) : null;
          return el ? { a: a, el: el } : null;
        })
        .filter(Boolean);
      if (!targets.length) return;
      nav.dataset.taNavReady = "1";

      targets.forEach(function (t) { t.el.classList.add("ta-pagenav-target"); });

      var prev = nav.querySelector("[data-pagenav-prev]");
      var next = nav.querySelector("[data-pagenav-next]");
      var status = nav.querySelector("[data-pagenav-status]");

      function goto(i) {
        if (i < 0 || i >= targets.length) return;
        var t = targets[i];
        t.el.scrollIntoView({ behavior: "smooth", block: "start" });
        t.a.setAttribute("aria-current", "true");
        sync(i);
      }
      function sync(i) {
        if (prev) prev.disabled = i <= 0;
        if (next) next.disabled = i >= targets.length - 1;
        if (status) status.textContent = (i + 1) + " / " + targets.length;
      }
      links.forEach(function (a, i) {
        a.addEventListener("click", function () {
          targets.forEach(function (t) { t.a.removeAttribute("aria-current"); });
          a.setAttribute("aria-current", "true");
          sync(i);
        });
      });
      if (prev) prev.addEventListener("click", function () { goto(current - 1); });
      if (next) next.addEventListener("click", function () { goto(current + 1); });

      var current = 0;
      if ("IntersectionObserver" in window) {
        var io = new IntersectionObserver(
          function (entries) {
            entries.forEach(function (en) {
              if (!en.isIntersecting) return;
              var idx = targets.findIndex(function (t) { return t.el === en.target; });
              if (idx < 0) return;
              current = idx;
              targets.forEach(function (t, i) {
                if (i === idx) t.a.setAttribute("aria-current", "true");
                else t.a.removeAttribute("aria-current");
              });
              sync(idx);
            });
          },
          { rootMargin: "-72px 0px -62% 0px", threshold: 0 }
        );
        targets.forEach(function (t) { io.observe(t.el); });
      } else {
        window.addEventListener("scroll", function () {
          var best = 0;
          targets.forEach(function (t, i) {
            if (t.el.getBoundingClientRect().top < 140) best = i;
          });
          current = best;
          sync(best);
        }, { passive: true });
      }
      sync(0);
      if (status && !status.textContent) status.textContent = "1 / " + targets.length;
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
