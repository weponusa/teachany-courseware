/* TeachAny — 共享交互兜底库（ta-interactions.js）
 * -------------------------------------------------------------------------
 * 背景：全库 277 门课件存在 4325 个「死按钮」——HTML 里的 onclick 引用了
 * 从未定义的 JS 函数（历史生成时 JS 块丢失）。2026-10-10 盘点：
 *   checkAnswer 96 门、各学科 *DepthCheck 合计约 100 门、answerQ/Pre/Post/Quiz
 *   约 46 门、goTo/showTab/selectOpt 约 33 门——这些是**跨课件通用**的判分、
 *   导航、选择题行为，占全部死按钮的 76%。
 *
 * 本文件为它们提供自适应的通用实现：从按钮自身的参数与最近的容器结构推断
 * 选项组、反馈容器，不依赖任何课件特定 DOM。由 scripts/fix-dead-buttons.py
 * 按每门课的实际缺失清单注入引用；*DepthCheck 一类的学科变体在内联别名块里
 * 指到 __taDepthCheck。
 *
 * 注意：这里**不做**课程特化的交互（画图、生长动画、拖拽判分、流程演示），
 * 那些需要按课件语义单独实现，见剩余清单 /tmp/onclick-special.json。
 */
(function () {
  'use strict';
  if (window.__taInteractions) return;
  window.__taInteractions = true;

  var css = document.createElement('style');
  css.textContent =
    '.ta-int-ok{outline:2px solid #16a34a!important;background:rgba(22,163,74,.12)!important}' +
    '.ta-int-no{outline:2px solid #dc2626!important;background:rgba(220,38,38,.10)!important}' +
    '.ta-int-fb{margin-top:10px;padding:10px 14px;border-radius:8px;font-size:14px;line-height:1.7}' +
    '.ta-int-fb.ok{background:rgba(22,163,74,.10);color:#166534}' +
    '.ta-int-fb.no{background:rgba(220,38,38,.08);color:#991b1b}' +
    '.ta-int-locked{pointer-events:none;opacity:.72}' +
    '@keyframes taFlash{0%{background:rgba(59,130,246,.22)}100%{background:transparent}}' +
    '.ta-int-flash{animation:taFlash 1.2s ease}';
  document.head.appendChild(css);

  function paint(el, ok) {
    el.classList.remove('ta-int-ok', 'ta-int-no');
    el.classList.add(ok ? 'ta-int-ok' : 'ta-int-no');
  }

  function boxOf(el) {
    return el.closest('.quiz-card,.practice-block,.card,.panel,.section,.tu-inquiry') ||
           el.closest('section') || el.parentNode || document.body;
  }

  /* 反馈容器：先按 id 找（fbId / fbId-feedback / fb-fbId），再在容器里找现成的
     反馈类元素，都不在就动态补一条。 */
  function feedbackOf(el, fbId) {
    if (fbId) {
      var a = document.getElementById(fbId) ||
              document.getElementById(fbId + '-feedback') ||
              document.getElementById('fb-' + fbId);
      if (a) return a;
    }
    var box = boxOf(el);
    var f = box.querySelector('.feedback,.quiz-explain,.dd-feedback,.ta-int-fb');
    if (f) return f;
    var d = document.createElement('div');
    d.className = 'ta-int-fb';
    (el.closest('.quiz-opts') || el.parentNode).insertAdjacentElement('afterend', d);
    return d;
  }

  function showFeedback(fb, ok, msg) {
    fb.classList.remove('ta-int-fb', 'ok', 'no');
    fb.classList.add('ta-int-fb', ok ? 'ok' : 'no');
    if (msg) fb.innerHTML = msg;
    fb.style.display = '';
  }

  /* checkAnswer(el, isCorrect, fbId) —— 对错按钮：高亮本钮 + 反馈条 */
  window.checkAnswer = function (el, ok, fbId) {
    paint(el, ok);
    var fb = feedbackOf(el, fbId || '');
    showFeedback(fb, ok, ok ? '✅ 答对了。' : '❌ 不对，再想一想。');
  };
  window.answerTF = window.checkAnswer;

  /* answerQ —— 两种签名兼容：
     A) answerQ(n, 'B', el, 'C')            旧式：题号数字 + 字母选项 + 元素
     B) answerQ('mod1-q1', 2, 'mod1', 2, '解析…') 新式：qid + 索引 + section + 正确索引 + 解析 */
  window.answerQ = function (a, b, c, d, e) {
    if (typeof a === 'string' && typeof d !== 'undefined') {
      var head = "answerQ('" + a + "'";
      var groupB = [].filter.call(document.querySelectorAll('[onclick]'), function (x) {
        return x.getAttribute('onclick').indexOf(head) === 0;
      });
      var rightB = Number(b) === Number(d);
      groupB.forEach(function (btn, i) {
        btn.classList.add('ta-int-locked');
        if (i === Number(d)) paint(btn, true);
        else if (i === Number(b)) paint(btn, false);
      });
      var fbB = feedbackOf(groupB[0] || document.body, c);
      showFeedback(fbB, rightB, (rightB ? '✅ ' : '❌ ') + (e || ''));
      return;
    }
    var n = a, chosen = b, el = c, correct = d;
    var group = (el.closest('.quiz-opts,.quiz-opts,.card,.section') || document)
      .querySelectorAll('[onclick^="answerQ(' + n + ',');
    var right = String(correct).toUpperCase() === String(chosen).toUpperCase();
    group.forEach(function (btn) {
      btn.classList.add('ta-int-locked');
      var cc = (btn.getAttribute('onclick').match(/'([^']*)'\)\s*$/) || [])[1];
      if (cc && cc.toUpperCase() === String(correct).toUpperCase()) paint(btn, true);
    });
    if (!right) paint(el, false);
    var fb = feedbackOf(el, 'qe' + n);
    showFeedback(fb, right, right ? '✅ 答对了。' : '❌ 正确答案是 ' + String(correct).toUpperCase() + '。');
  };

  /* answerPre —— 三签名兼容：
     A) answerPre(el, qid, isCorrect)                     旧式：元素 + 容器 id
     B) answerPre(qid, chosenIdx, correctIdx, explain)    新式：同 answerPost
     C) answerPre(n, 'B', 'B')                            题号 + 字母选择 + 字母正确 */
  window.answerPre = function (a, b, c, d) {
    if (typeof a === 'string' && typeof c !== 'undefined') {
      return window.answerPost(a, b, c, d);
    }
    if (typeof a === 'number' && typeof b === 'string') {
      var rightC = String(b).toUpperCase() === String(c).toUpperCase();
      var grpC = document.querySelectorAll('[onclick^="answerPre(' + a + ',');
      grpC.forEach(function (btn) {
        btn.classList.add('ta-int-locked');
        var m2 = btn.getAttribute('onclick').match(/,\s*'([^']*)'\s*,\s*'([^']*)'\s*\)/);
        if (m2 && m2[2].toUpperCase() === String(c).toUpperCase()) paint(btn, true);
      });
      var fbC = feedbackOf(grpC[0] || document.body, 'qe' + a);
      showFeedback(fbC, rightC, rightC ? '✅ 答对了。' : '❌ 正确答案是 ' + String(c).toUpperCase() + '。');
      return;
    }
    window.checkAnswer(a, c, b);
  };

  /* answerQuiz(qid, chosen, correct, fbId, explain) —— 带解析的选择题。
     注意：组内查找用 getAttribute 过滤，不拼引号选择器——onclick 属性里的
     引号转义极易写坏（首版就栽在这里，整个文件语法错误、库从未执行）。 */
  function groupFor(fnName, qid) {
    var head = fnName + "('" + qid + "'";
    return [].filter.call(document.querySelectorAll('[onclick]'), function (b) {
      return b.getAttribute('onclick').indexOf(head) === 0;
    });
  }
  function chosenOf(onclick) {
    var m = onclick.match(/,\s*'([^']*)'/);
    return m ? m[1] : null;
  }
  window.answerQuiz = function (qid, chosen, correct, fbId, explain) {
    var group = groupFor('answerQuiz', qid);
    var right = String(chosen).toUpperCase() === String(correct).toUpperCase();
    group.forEach(function (b) {
      b.classList.add('ta-int-locked');
      var c = chosenOf(b.getAttribute('onclick'));
      if (c && c.toUpperCase() === String(correct).toUpperCase()) paint(b, true);
    });
    if (!right) {
      var hit = [].filter.call(group, function (b) {
        return chosenOf(b.getAttribute('onclick')) === chosen;
      })[0];
      if (hit) paint(hit, false);
    }
    var fb = feedbackOf(group[0] || document.body, fbId);
    showFeedback(fb, right, (right ? '✅ ' : '❌ 正确答案是 ' + correct + '。') + (explain || ''));
  };

  /* answerPost(qid, chosen, correct, explain) —— 后测，选项为索引号 */
  window.answerPost = function (qid, chosen, correct, explain) {
    var group = groupFor('answerPost', qid);
    var right = Number(chosen) === Number(correct);
    group.forEach(function (b, i) {
      b.classList.add('ta-int-locked');
      if (i === Number(correct)) paint(b, true);
      else if (i === Number(chosen)) paint(b, false);
    });
    var fb = feedbackOf(group[0] || document.body, qid);
    showFeedback(fb, right, (right ? '✅ ' : '❌ ') + (explain || ''));
  };

  /* __taDepthCheck(el, isCorrect, feedbackId, tip) —— 深度检查（各学科变体共用） */
  window.__taDepthCheck = function (el, ok, fbId, tip) {
    paint(el, ok);
    var fb = feedbackOf(el, fbId || '');
    showFeedback(fb, ok, (ok ? '✅ ' : '💡 ') + (tip || ''));
  };

  /* goTo(id) —— 平滑滚动到目标模块并短暂高亮 */
  window.goTo = function (id) {
    var t = document.getElementById(id);
    if (!t) return;
    t.scrollIntoView({ behavior: 'smooth', block: 'start' });
    t.classList.remove('ta-int-flash');
    void t.offsetWidth;
    t.classList.add('ta-int-flash');
  };

  /* showTab(id) —— 有 data-tab 组则切面板，否则退化为滚动定位 */
  window.showTab = function (id) {
    var t = document.getElementById(id);
    if (!t) return;
    var groupKey = t.getAttribute('data-tab');
    if (groupKey) {
      document.querySelectorAll('[data-tab="' + groupKey + '"]').forEach(function (p) {
        p.style.display = p === t ? '' : 'none';
      });
    }
    t.scrollIntoView({ behavior: 'smooth', block: 'start' });
    t.classList.remove('ta-int-flash');
    void t.offsetWidth;
    t.classList.add('ta-int-flash');
  };

  /* selectOpt(el) —— 单选组样式切换 */
  window.selectOpt = function (el) {
    var group = (el.closest('.quiz-opts,.card,.section') || document)
      .querySelectorAll('[onclick^="selectOpt"]');
    group.forEach(function (b) { b.classList.remove('ta-int-ok', 'selected', 'active'); });
    el.classList.add('selected', 'ta-int-ok');
  };

  /* 学科变体注册器：内联别名块调用，把 enghDepthCheck 这类名字挂到通用实现 */
  window.__taRegisterDepthCheck = function (names) {
    names.forEach(function (n) {
      if (typeof window[n] !== 'function') {
        window[n] = function (el, ok, fbId, tip) {
          return window.__taDepthCheck(el, ok, fbId, tip);
        };
      }
    });
  };
})();
