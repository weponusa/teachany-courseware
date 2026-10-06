/* TeachAny v2 — Slide Controller (shared) */
(function () {
  'use strict';
  const container = document.getElementById('slide-container');
  if (!container) return;
  const pages = Array.from(container.querySelectorAll('.slide-page'));
  const totalPages = pages.length;
  if (!totalPages) return;

  let currentPage = 0;
  let isPlayMode = false;
  let isAutoPlay = false;
  let autoPlayTimer = null;

  const progressBar = document.getElementById('slide-progress-bar');
  const sidenav = document.getElementById('slide-sidenav');
  const fab = document.getElementById('play-mode-fab');
  const fabPlay = document.getElementById('fab-icon-play');
  const fabBrowse = document.getElementById('fab-icon-browse');
  const tbPrev = document.getElementById('tb-prev');
  const tbNext = document.getElementById('tb-next');
  const tbPageInfo = document.getElementById('tb-page-info');
  const tbProgressFill = document.getElementById('tb-progress-fill');
  const tbProgress = document.getElementById('tb-progress');
  const tbAutoplay = document.getElementById('tb-autoplay');
  const tbFullscreen = document.getElementById('tb-fullscreen');

  function buildSidenav() {
    if (!sidenav) return;
    sidenav.innerHTML = '';
    const counter = document.createElement('div');
    counter.className = 'sidenav-counter';
    counter.id = 'sidenav-counter';
    counter.textContent = '1/' + totalPages;
    sidenav.appendChild(counter);
    pages.forEach((p, i) => {
      const d = document.createElement('button');
      d.className = 'sidenav-dot' + (i === 0 ? ' active' : '');
      const tip = p.dataset.tsh || p.id || ('第' + (i + 1) + '页');
      d.setAttribute('aria-label', tip);
      d.setAttribute('data-tooltip', tip.split(' - ')[0].slice(0, 24));
      d.addEventListener('click', () => goToPage(i));
      sidenav.appendChild(d);
    });
  }

  function updateUI() {
    const prog = totalPages > 1 ? (currentPage / (totalPages - 1)) * 100 : 100;
    if (progressBar) progressBar.style.width = prog + '%';
    if (tbProgressFill) tbProgressFill.style.width = prog + '%';
    if (tbPageInfo) tbPageInfo.textContent = currentPage + 1 + ' / ' + totalPages;
    if (sidenav) {
      sidenav.querySelectorAll('.sidenav-dot').forEach((d, i) => d.classList.toggle('active', i === currentPage));
    }
    const counterEl = document.getElementById('sidenav-counter');
    if (counterEl) counterEl.textContent = currentPage + 1 + '/' + totalPages;
    if (tbPrev) tbPrev.style.opacity = currentPage === 0 ? '0.3' : '1';
    if (tbNext) tbNext.style.opacity = currentPage === totalPages - 1 ? '0.3' : '1';
  }

  function goToPage(i) {
    if (i < 0 || i >= totalPages) return;
    currentPage = i;
    pages[currentPage].scrollIntoView({ behavior: 'smooth', block: 'start' });
    updateUI();
    document.dispatchEvent(new CustomEvent('teachany-slide-change', { detail: { index: currentPage } }));
  }

  function nextPage() { if (currentPage < totalPages - 1) goToPage(currentPage + 1); }
  function prevPage() { if (currentPage > 0) goToPage(currentPage - 1); }

  let scrollTimeout;
  function onScroll() {
    clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(() => {
      const st = isPlayMode ? container.scrollTop : window.scrollY;
      let closest = 0;
      let minD = Infinity;
      pages.forEach((p, i) => {
        const top = isPlayMode ? p.offsetTop : p.getBoundingClientRect().top + window.scrollY;
        const d = Math.abs(top - st - 100);
        if (d < minD) { minD = d; closest = i; }
      });
      if (closest !== currentPage) { currentPage = closest; updateUI(); }
    }, 120);
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  container.addEventListener('scroll', onScroll, { passive: true });

  function togglePlayMode() {
    isPlayMode = !isPlayMode;
    document.body.classList.toggle('play-mode', isPlayMode);
    document.body.classList.toggle('toolbar-visible', isPlayMode);
    if (fabPlay) fabPlay.style.display = isPlayMode ? 'none' : 'block';
    if (fabBrowse) fabBrowse.style.display = isPlayMode ? 'block' : 'none';
    if (isPlayMode) {
      container.style.height = '100dvh';
      container.style.overflowY = 'auto';
      container.style.scrollSnapType = 'y mandatory';
      goToPage(currentPage);
      setTimeout(function () {
        document.dispatchEvent(new CustomEvent('teachany-slide-change', { detail: { index: currentPage } }));
      }, 280);
    } else {
      container.style.height = '';
      container.style.overflowY = '';
      container.style.scrollSnapType = '';
    }
  }

  if (fab) fab.addEventListener('click', togglePlayMode);
  if (tbPrev) tbPrev.addEventListener('click', prevPage);
  if (tbNext) tbNext.addEventListener('click', nextPage);
  if (tbProgress) {
    tbProgress.addEventListener('click', (e) => {
      const r = tbProgress.getBoundingClientRect();
      const ratio = (e.clientX - r.left) / r.width;
      goToPage(Math.round(ratio * (totalPages - 1)));
    });
  }
  if (tbAutoplay) {
    tbAutoplay.addEventListener('click', () => {
      isAutoPlay = !isAutoPlay;
      tbAutoplay.classList.toggle('active', isAutoPlay);
      if (isAutoPlay) {
        autoPlayTimer = setInterval(() => {
          if (currentPage < totalPages - 1) nextPage();
          else { clearInterval(autoPlayTimer); isAutoPlay = false; tbAutoplay.classList.remove('active'); }
        }, 8000);
      } else if (autoPlayTimer) clearInterval(autoPlayTimer);
    });
  }
  if (tbFullscreen) {
    tbFullscreen.addEventListener('click', () => {
      if (!document.fullscreenElement) document.documentElement.requestFullscreen?.();
      else document.exitFullscreen?.();
    });
  }

  document.addEventListener('keydown', (e) => {
    if (['INPUT', 'TEXTAREA', 'SELECT'].includes(e.target.tagName)) return;
    if (!isPlayMode) return;
    switch (e.key) {
      case 'ArrowRight': case 'ArrowDown': case ' ':
        e.preventDefault(); nextPage(); break;
      case 'ArrowLeft': case 'ArrowUp':
        e.preventDefault(); prevPage(); break;
      case 'Escape':
        togglePlayMode(); break;
    }
  });
  document.addEventListener('keydown', (e) => {
    if ((e.key === 'f' || e.key === 'F') && !e.ctrlKey && !e.metaKey && e.target.tagName !== 'INPUT') togglePlayMode();
  });

  buildSidenav();
  updateUI();
  document.body.classList.add('toolbar-visible');
  setTimeout(() => { if (!isPlayMode) document.body.classList.remove('toolbar-visible'); }, 3000);
})();
