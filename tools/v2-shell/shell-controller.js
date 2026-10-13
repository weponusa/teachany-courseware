

(function() {
  'use strict';
  const container = document.getElementById('slide-container');
  const pages = Array.from(document.querySelectorAll('.slide-page'));
  const totalPages = pages.length;
  let currentPage = 0, isPlayMode = false, isAutoPlay = false, autoPlayTimer = null;

  const progressBar = document.getElementById('slide-progress-bar');
  const sidenav = document.getElementById('slide-sidenav');
  const fab = document.getElementById('play-mode-fab');
  const fabIconPlay = document.getElementById('fab-icon-play');
  const fabIconBrowse = document.getElementById('fab-icon-browse');
  const tbPrev = document.getElementById('tb-prev');
  const tbNext = document.getElementById('tb-next');
  const tbPageInfo = document.getElementById('tb-page-info');
  const tbProgressFill = document.getElementById('tb-progress-fill');
  const tbProgress = document.getElementById('tb-progress');
  const tbAutoplay = document.getElementById('tb-autoplay');
  const tbFullscreen = document.getElementById('tb-fullscreen');

  function buildSidenav() {
    sidenav.innerHTML = '';
    const counter = document.createElement('div');
    counter.className = 'sidenav-counter';
    counter.id = 'sidenav-counter';
    counter.textContent = '1/' + totalPages;
    sidenav.appendChild(counter);
    pages.forEach((page, i) => {
      const dot = document.createElement('button');
      dot.className = 'sidenav-dot' + (i === 0 ? ' active' : '');
      dot.setAttribute('data-tooltip', (page.dataset.tsh || '').split(' - ')[0] || ('第' + (i + 1) + '页'));
      dot.setAttribute('aria-label', '跳转到第' + (i + 1) + '页');
      dot.addEventListener('click', () => goToPage(i));
      sidenav.appendChild(dot);
    });
  }

  function updateUI() {
    const progress = totalPages > 1 ? (currentPage / (totalPages - 1)) * 100 : 100;
    progressBar.style.width = progress + '%';
    tbProgressFill.style.width = progress + '%';
    tbPageInfo.textContent = (currentPage + 1) + ' / ' + totalPages;
    sidenav.querySelectorAll('.sidenav-dot').forEach((dot, i) => dot.classList.toggle('active', i === currentPage));
    const counterEl = document.getElementById('sidenav-counter');
    if (counterEl) counterEl.textContent = (currentPage + 1) + '/' + totalPages;
    tbPrev.style.opacity = currentPage === 0 ? '0.3' : '1';
    tbNext.style.opacity = currentPage === totalPages - 1 ? '0.3' : '1';
  }

  function goToPage(index) {
    if (index < 0 || index >= totalPages) return;
    currentPage = index;
    if (isPlayMode) pages[currentPage].scrollIntoView({ behavior: 'smooth', block: 'start' });
    else container.scrollTo({ top: pages[currentPage].offsetTop, behavior: 'smooth' });
    updateUI();
    dispatchPageAudio();
  }
  function nextPage() { if (currentPage < totalPages - 1) goToPage(currentPage + 1); }
  function prevPage() { if (currentPage > 0) goToPage(currentPage - 1); }

  let scrollTimeout;
  container.addEventListener('scroll', () => {
    if (isPlayMode) return;
    clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(() => {
      const scrollTop = container.scrollTop;
      let closest = 0, minDist = Infinity;
      pages.forEach((page, i) => {
        const dist = Math.abs(page.offsetTop - scrollTop);
        if (dist < minDist) { minDist = dist; closest = i; }
      });
      if (closest !== currentPage) { currentPage = closest; updateUI(); }
    }, 100);
  }, { passive: true });

  function togglePlayMode() {
    isPlayMode = !isPlayMode;
    document.body.classList.toggle('play-mode', isPlayMode);
    document.body.classList.toggle('toolbar-visible', isPlayMode);
    fabIconPlay.style.display = isPlayMode ? 'none' : 'block';
    fabIconBrowse.style.display = isPlayMode ? 'block' : 'none';
    if (isPlayMode) goToPage(currentPage);
  }
  fab.addEventListener('click', togglePlayMode);
  tbPrev.addEventListener('click', prevPage);
  tbNext.addEventListener('click', nextPage);
  tbProgress.addEventListener('click', (e) => {
    const rect = tbProgress.getBoundingClientRect();
    goToPage(Math.round(((e.clientX - rect.left) / rect.width) * (totalPages - 1)));
  });
  tbAutoplay.addEventListener('click', () => {
    isAutoPlay = !isAutoPlay;
    tbAutoplay.classList.toggle('active', isAutoPlay);
    if (isAutoPlay) {
      stopAutoPlay();
      autoPlayTimer = setInterval(() => {
        if (currentPage < totalPages - 1) nextPage();
        else { stopAutoPlay(); isAutoPlay = false; tbAutoplay.classList.remove('active'); }
      }, 9000);
    } else stopAutoPlay();
  });
  function stopAutoPlay() { if (autoPlayTimer) { clearInterval(autoPlayTimer); autoPlayTimer = null; } }
  tbFullscreen.addEventListener('click', () => {
    if (!document.fullscreenElement) document.documentElement.requestFullscreen?.();
    else document.exitFullscreen?.();
  });

  document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    switch (e.key) {
      case 'ArrowRight': case 'ArrowDown': case ' ': e.preventDefault(); nextPage(); break;
      case 'ArrowLeft': case 'ArrowUp': e.preventDefault(); prevPage(); break;
      case 'f': case 'F': if (!e.ctrlKey && !e.metaKey) togglePlayMode(); break;
      case 'Escape': if (isPlayMode) togglePlayMode(); break;
    }
  });

  function dispatchPageAudio() {
    const page = pages[currentPage];
    const ttsId = page.dataset.tts;
    if (ttsId && window.__TEACHANY_AUDIO_PLAYER__) window.__TEACHANY_AUDIO_PLAYER__.playSection(ttsId);
  }
  document.addEventListener('teachany-audio-ended', () => {
    if (isAutoPlay && currentPage < totalPages - 1) setTimeout(nextPage, 1000);
  });

  window.__TEACHANY_LEARNER_QUESTION__ = '';
  window.__TEACHANY_TUTOR_CONFIG__ = {
    courseId: 'sci-e-buoyancy',
    courseTitle: '浮力：为什么有的东西浮在水上？',
    subject: 'science',
    grade: '5',
    nodeId: 'sci-e-buoyancy',
    lessonType: 'experiment-inquiry',
    getLearnerQuestion: () => window.__TEACHANY_LEARNER_QUESTION__ || '',
    getContext: () => ((pages[currentPage] || document.body).innerText || '').slice(0, 3000)
  };

  function setLearnerQuestion(q) {
    window.__TEACHANY_LEARNER_QUESTION__ = q || '';
    const fb = document.getElementById('anchor-feedback');
    if (fb) fb.textContent = q ? '你的问题：' + q : '选择或输入后，这节课会围绕你的问题展开。';
  }
  document.querySelectorAll('[data-anchor-choice]').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('[data-anchor-choice]').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      setLearnerQuestion(btn.getAttribute('data-anchor-choice') || btn.textContent.trim());
    });
  });
  document.getElementById('learner-question-input')?.addEventListener('input', (e) => setLearnerQuestion(e.target.value.trim()));

  buildSidenav();
  updateUI();
  document.body.classList.add('toolbar-visible');
  setTimeout(() => { if (!isPlayMode) document.body.classList.remove('toolbar-visible'); }, 3000);

  document.addEventListener('DOMContentLoaded', () => {
    const cv = document.querySelector('meta[name="course-version"]')?.content;
    const sv = document.querySelector('meta[name="teachany-version"]')?.content;
    // 旧课件品牌栏可能没有这两个 span —— 必须同时判元素存在，否则整段脚本崩
    const cvEl = document.getElementById('course-version-display');
    const svEl = document.getElementById('skill-version-display');
    if (cv && cvEl) cvEl.textContent = cv;
    if (sv && svEl) svEl.textContent = sv.replace(/^v/, '');
  });

  if (location.hostname === 'localhost' || location.search.includes('debug')) {
    const checks = [
      ['slide-pages', () => pages.length >= 8],
      ['course-id meta', () => !!document.querySelector('meta[name="course-id"]')?.content],
      ['template-version meta', () => document.querySelector('meta[name="teachany-template-version"]')?.content === '2.0'],
      ['side-navigation', () => sidenav.children.length > 0],
      ['audio playlist', () => !!document.querySelector('[data-teachany-audio-playlist]')],
      ['AI tutor card', () => !!document.querySelector('[data-teachany-tutor-card]')],
      ['knowledge graph', () => !!document.querySelector('[data-teachany-kg]')]
    ];
    checks.forEach(([name, fn]) => console[fn() ? 'log' : 'warn']('[TeachAny v2] ' + (fn() ? 'PASS' : 'MISSING') + ' ' + name));
  }
})();

