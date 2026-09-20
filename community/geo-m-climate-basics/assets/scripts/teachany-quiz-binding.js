/* teachany-quiz-binding.js — 课件 quiz 交互统一绑定引擎
 *
 * 背景：大批课件的选项按钮引用了未定义的 JS 函数/未绑定事件，导致"题目不能选择"。
 * 本脚本统一接管三类 DOM 形态 + 七类 onclick 函数签名兜底，全部只在缺失时生效，
 * 不覆盖课件自带实现。
 *
 * 覆盖：
 *  形态A  .tu-q[data-answer] > .tu-opt[data-choice][data-diagnosis] + .tu-fb
 *  形态B  .quiz-option[onclick="selectOpt(this)"]（data-q/data-correct + #{q}Feedback/#{q}Error）
 *  形态C  .choice[data-diagnosis]（data-answer="correct|wrong" 或 data-correct）
 *  兜底函数 selectOpt / checkAnswer / answerQ / answerPre / answerPost
 *           answerQuiz / answerModule / biomDepthCheck / phymDepthCheck
 *  导航安全兜底 goTo / goSection / showSection / startCourse / showTab
 */
(function () {
  'use strict';

  /* ---------- 兜底样式（课件未定义 correct/wrong 时也能看见反馈） ---------- */
  var css =
    '.ta-quiz-correct{outline:2px solid #22c55e !important;background:rgba(34,197,94,.16) !important;border-radius:10px;}' +
    '.ta-quiz-wrong{outline:2px solid #ef4444 !important;background:rgba(239,68,68,.12) !important;border-radius:10px;}' +
    '.ta-quiz-done{opacity:.92;}' +
    '.tu-fb{display:block;margin-top:10px;padding:10px 14px;border-radius:10px;font-size:14px;line-height:1.6;}' +
    '.tu-fb.ta-fb-correct{background:rgba(34,197,94,.12);color:#15803d;}' +
    '.tu-fb.ta-fb-wrong{background:rgba(239,68,68,.1);color:#b91c1c;}';
  var st = document.createElement('style');
  st.setAttribute('data-ta-quiz-binding', '');
  st.textContent = css;
  document.head.appendChild(st);

  /* ---------- 工具 ---------- */
  function freezeGroup(btns) {
    btns.forEach(function (b) {
      b.disabled = true;
      b.style.pointerEvents = 'none';
      b.classList.add('ta-quiz-done');
    });
  }
  function mark(el, ok) {
    el.classList.add(ok ? 'correct' : 'wrong');
    el.classList.add(ok ? 'ta-quiz-correct' : 'ta-quiz-wrong');
  }
  function revealRight(btns, isRightFn) {
    btns.forEach(function (x) {
      if (isRightFn(x)) x.classList.add('correct', 'ta-quiz-correct');
    });
  }
  function showFb(fb, ok, text) {
    if (!fb) return;
    fb.hidden = false;
    fb.style.display = 'block';
    fb.classList.add('show');
    fb.classList.remove('correct', 'wrong', 'ta-fb-correct', 'ta-fb-wrong');
    fb.classList.add(ok ? 'correct' : 'wrong');
    fb.classList.add(ok ? 'ta-fb-correct' : 'ta-fb-wrong');
    if (text) fb.textContent = text;
  }
  function toArr(list) { return Array.prototype.slice.call(list); }

  /* ---------- 形态A：.tu-opt ---------- */
  toArr(document.querySelectorAll('.tu-q[data-answer]')).forEach(function (q) {
    if (q.dataset.taQuizBound) return;
    q.dataset.taQuizBound = '1';
    var answer = q.dataset.answer;
    var opts = toArr(q.querySelectorAll('.tu-opt'));
    var fb = q.querySelector('.tu-fb');
    opts.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var ok = btn.dataset.choice === answer;
        freezeGroup(opts);
        mark(btn, ok);
        revealRight(opts, function (x) { return x.dataset.choice === answer; });
        showFb(fb, ok, ok ? '✅ 回答正确！' : '❌ ' + (btn.dataset.diagnosis || '再想一想。'));
      });
    });
  });

  /* ---------- 形态C：.choice[data-diagnosis] ---------- */
  var choiceGroups = [];
  toArr(document.querySelectorAll('.choice[data-diagnosis]')).forEach(function (btn) {
    var scope = btn.closest('.grid, .tu-opts, .quiz-options, .slide-inner, .card, section') || btn.parentElement;
    var g = null;
    for (var i = 0; i < choiceGroups.length; i++) {
      if (choiceGroups[i].scope === scope) { g = choiceGroups[i]; break; }
    }
    if (!g) { g = { scope: scope, btns: [] }; choiceGroups.push(g); }
    g.btns.push(btn);
  });
  choiceGroups.forEach(function (g) {
    g.btns.forEach(function (btn) {
      if (btn.dataset.taQuizBound) return;
      btn.dataset.taQuizBound = '1';
      btn.addEventListener('click', function () {
        var ok = btn.dataset.answer === 'correct' || btn.dataset.correct === 'true' || btn.dataset.correct === '1';
        freezeGroup(g.btns);
        mark(btn, ok);
        revealRight(g.btns, function (x) {
          return x.dataset.answer === 'correct' || x.dataset.correct === 'true' || x.dataset.correct === '1';
        });
        var scope = btn.closest('.card, .slide-inner, .slide-page, section') || document;
        var fb = scope.querySelector('[data-feedback-for], .tu-fb, .quiz-fb') ||
                 (g.scope !== scope ? g.scope.querySelector('.result.warn, .result') : null) ||
                 scope.querySelector('.result.warn, .result');
        showFb(fb, ok, btn.dataset.diagnosis || (ok ? '✅ 回答正确！' : '❌ 再想一想。'));
      });
    });
  });

  /* ---------- 形态B：selectOpt（data-q + data-correct + #{q}Feedback/#{q}Error） ---------- */
  if (typeof window.selectOpt !== 'function') {
    window.selectOpt = function (el) {
      var q = el.dataset.q || '';
      var group = el.closest('.quiz-options') || el.parentElement;
      var opts = toArr(group.querySelectorAll('.quiz-option'));
      var ok = el.dataset.correct === 'true' || el.dataset.correct === '1';
      freezeGroup(opts);
      mark(el, ok);
      revealRight(opts, function (x) { return x.dataset.correct === 'true' || x.dataset.correct === '1'; });
      var fb = document.getElementById(q + 'Feedback');
      if (fb) showFb(fb, ok, ok ? '✅ 回答正确！' : '❌ 答错了，看看下面的诊断。');
      if (!ok) {
        var err = document.getElementById(q + 'Error');
        if (err) { err.style.display = 'block'; err.classList.add('show'); }
      }
    };
  }

  /* ---------- checkAnswer(el, ok, target)：反馈到 #target-feedback / FEEDBACK[target] ---------- */
  if (typeof window.checkAnswer !== 'function') {
    window.checkAnswer = function (btn, ok, target) {
      var scope = btn.parentElement;
      var opts = toArr(scope.querySelectorAll('.quiz-option, button'));
      freezeGroup(opts);
      mark(btn, !!ok);
      revealRight(opts, function (x) {
        var oc = x.getAttribute('onclick') || '';
        return /checkAnswer\(\s*this\s*,\s*true/.test(oc);
      });
      var fb = document.getElementById(target + '-feedback') || document.getElementById(target);
      var msg = '';
      try {
        if (typeof FEEDBACK !== 'undefined' && FEEDBACK && FEEDBACK[target]) msg = FEEDBACK[target];
      } catch (e) { /* ignore */ }
      showFb(fb, !!ok, (ok ? '✅ ' : '❌ ') + (msg || (ok ? '回答正确！' : '再想想，对照上面的讲解检查一下。')));
    };
  }

  /* ---------- answerQ(n, choice, el, correctChoice) ---------- */
  if (typeof window.answerQ !== 'function') {
    window.answerQ = function (n, choice, el, correct) {
      var ok = choice === correct;
      var group = el.closest('.quiz-opts, .quiz-options, .q-block, div');
      var opts = group ? toArr(group.querySelectorAll('.quiz-opt, .quiz-option')) : [el];
      freezeGroup(opts);
      mark(el, ok);
      revealRight(opts, function (x) {
        var oc = x.getAttribute('onclick') || '';
        return oc.indexOf("'" + correct + "'") > -1 && /answerQ\(\s*\d+\s*,\s*'/.test(oc) &&
               new RegExp("answerQ\\(\\s*" + n + "\\s*,\\s*'" + correct + "'").test(oc);
      });
      var scope = el.closest('.card, section, div');
      var fb = scope ? scope.querySelector('.feedback, .quiz-fb, [data-feedback-for]') : null;
      showFb(fb, ok, ok ? '✅ 回答正确！' : '❌ 再想想，回到上面的讲解找依据。');
    };
  }

  /* ---------- answerPre / answerPost：两种签名
       签名1 (el, qid, ok)  如 answerPre(this,'pre-q1',true)
       签名2 (n, choice, correctChoice) 如 answerPost(1,'A','D') ---------- */
  function makeDualSigQuiz(name) {
    if (typeof window[name] === 'function') return;
    window[name] = function (a, b, c) {
      if (a && a.nodeType === 1) {
        // 签名1：(el, qid, ok)
        var el = a, ok = !!c;
        var group = el.closest('.quiz-options, .quiz-opts, .q-block, div');
        var opts = group ? toArr(group.querySelectorAll('.quiz-option, .quiz-opt, button')) : [el];
        freezeGroup(opts);
        mark(el, ok);
        revealRight(opts, function (x) {
          return new RegExp(name + "\\(\\s*this\\s*,[^)]*,\\s*true\\s*\\)").test(x.getAttribute('onclick') || '');
        });
        var scope = el.closest('.card, section, div');
        var fb = scope ? scope.querySelector('.feedback, .quiz-fb, [data-feedback-for]') : null;
        showFb(fb, ok, ok ? '✅ 回答正确！' : '❌ 再想想。');
      } else {
        // 签名2：(n, choice, correctChoice)
        var correct = c, ok2 = b === c;
        var el2 = (window.event && window.event.target) ? window.event.target : null;
        if (el2) {
          var group2 = el2.closest('.options, .quiz-options, .q-block, div');
          var opts2 = group2 ? toArr(group2.querySelectorAll('.option-btn, .quiz-option, button')) : [el2];
          freezeGroup(opts2);
          mark(el2, ok2);
          revealRight(opts2, function (x) {
            return new RegExp(name + "\\(\\s*\\d+\\s*,\\s*'" + correct + "'\\s*,\\s*'" + correct + "'").test(x.getAttribute('onclick') || '');
          });
          var scope2 = el2.closest('.card, section, div');
          var fb2 = scope2 ? scope2.querySelector('.feedback, .quiz-fb, [data-feedback-for]') : null;
          showFb(fb2, ok2, ok2 ? '✅ 回答正确！' : '❌ 再想想，回到讲解找依据。');
        }
      }
    };
  }
  makeDualSigQuiz('answerPre');
  makeDualSigQuiz('answerPost');

  /* ---------- answerModule(n, choice, correctChoice) ---------- */
  if (typeof window.answerModule !== 'function') {
    window.answerModule = function (n, choice, correct) {
      var ok = choice === correct;
      var el = (window.event && window.event.target) ? window.event.target : null;
      if (!el) return;
      var group = el.closest('.options, .quiz-options, .q-block, div');
      var opts = group ? toArr(group.querySelectorAll('.option-btn, .quiz-option, button')) : [el];
      freezeGroup(opts);
      mark(el, ok);
      revealRight(opts, function (x) {
        return new RegExp("answerModule\\(\\s*" + n + "\\s*,\\s*'" + correct + "'\\s*,\\s*'" + correct + "'").test(x.getAttribute('onclick') || '');
      });
      var scope = el.closest('.card, section, div');
      var fb = scope ? scope.querySelector('.feedback, .quiz-fb, [data-feedback-for]') : null;
      showFb(fb, ok, ok ? '✅ 回答正确！' : '❌ 再想想。');
    };
  }

  /* ---------- answerQuiz(qid, choice, correctChoice, fbId, text) ---------- */
  if (typeof window.answerQuiz !== 'function') {
    window.answerQuiz = function (qid, choice, correct, fbId, text) {
      var ok = choice === correct;
      var el = (window.event && window.event.target) ? window.event.target : null;
      if (el) {
        var group = el.closest('.quiz-opts, .quiz-options, .q-block, div');
        var opts = group ? toArr(group.querySelectorAll('.quiz-opt, .quiz-option, button')) : [el];
        freezeGroup(opts);
        mark(el, ok);
        revealRight(opts, function (x) {
          return new RegExp("answerQuiz\\(\\s*'" + qid + "'\\s*,\\s*'" + correct + "'").test(x.getAttribute('onclick') || '');
        });
      }
      var fb = fbId ? document.getElementById(fbId) : null;
      showFb(fb, ok, text || (ok ? '✅ 回答正确！' : '❌ 再想想。'));
    };
  }

  /* ---------- biomDepthCheck / phymDepthCheck(el, ok, fbId, text) ---------- */
  function makeDepthCheck(name) {
    if (typeof window[name] === 'function') return;
    window[name] = function (btn, ok, fbId, text) {
      var scope = btn.parentElement;
      var opts = toArr(scope.querySelectorAll('button'));
      freezeGroup(opts);
      mark(btn, !!ok);
      revealRight(opts, function (x) { return x.dataset.correct === '1' || x.dataset.correct === 'true'; });
      var fb = document.getElementById(fbId);
      showFb(fb, !!ok, text || (ok ? '✅ 回答正确！' : '❌ 再想想。'));
    };
  }
  makeDepthCheck('biomDepthCheck');
  makeDepthCheck('phymDepthCheck');

  /* ---------- 导航安全兜底（避免 ReferenceError；只做无害动作） ---------- */
  function safeScroll(target) {
    var el = typeof target === 'string' ? document.getElementById(target) : target;
    if (el && el.scrollIntoView) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  if (typeof window.goTo !== 'function') window.goTo = safeScroll;
  if (typeof window.goSection !== 'function') window.goSection = safeScroll;
  if (typeof window.showSection !== 'function') window.showSection = safeScroll;
  if (typeof window.startCourse !== 'function') {
    window.startCourse = function () {
      var first = document.querySelector('section.slide-page, section.section');
      safeScroll(first);
    };
  }
  if (typeof window.showTab !== 'function') {
    window.showTab = function (name) {
      // 通用 tab：尝试切换 data-tab / id 匹配面板的显示
      var panels = document.querySelectorAll('[data-tab-panel], .tab-panel');
      panels.forEach(function (p) {
        var match = p.dataset.tabPanel === name || p.id === name || p.id === 'tab-' + name;
        p.style.display = match ? '' : 'none';
      });
      safeScroll(document.getElementById(name) || document.getElementById('tab-' + name));
    };
  }
})();
