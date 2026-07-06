/**
 * 修正导航中指向 TeachAny 引擎的链接（/pbl-map/ 下为站点根，本地为 ./engine/）
 */
(function () {
  function apply() {
    if (typeof pblMapEngineUrl !== 'function') return;
    document.querySelectorAll('[data-pblmap-engine]').forEach((el) => {
      const page = el.getAttribute('data-pblmap-engine') || 'index.html';
      el.setAttribute('href', pblMapEngineUrl(page));
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', apply);
  } else {
    apply();
  }
})();
