# -*- coding: utf-8 -*-
"""小学信息科技 · 程序调试与迭代（G5）—— 补齐知识树「算法与程序」空缺

学科语气：信息科技 = 概念 + 动手并重。
本课只做三件真能上手的事：
  ① 读懂报错信息：点报错里的三块线索卡 → 程序里对应的那一行亮起来 +
     告诉你「这句话在说什么」→ 再判断真正要改的是哪一行
  ② 核心模拟：给一段有 bug 的伪代码 → 学生点选有问题的那一行 → 即时给错因 →
     点修正 → 重新运行 → 一行一行跑通并输出正确结果（两关：名字写错 / 语句放错位置）
  ③ 综合任务：一段「不报错但结果不对」的程序，先手工验算小数据再定位边界 bug，
     修好重跑通过；最后想一想改动怎样才能最小

说明：课件中的伪代码、报错文字与运行面板均为教学示意图，不涉及任何真实软件界面、截图或商标。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-e-debugging-fig1.webp'
F2 = './assets/it-e-debugging-fig2.webp'

TTS = {
    "hero": "先请你想象一件事。你照着食谱做一道菜，结果端出来太咸了。这时候你会怎么办？你不会把整锅倒掉，也不会怪锅不好。你会回想每一步：盐是不是放多了？是不是放了两次？这就是调试。程序写错了也一样：它要么在运行时停下来告诉你哪里出了问题，要么安安静静地跑完，却给你一个不对的结果。今天这节课，我们要学会看懂它给你的提示，亲手找出那一行，改好，再跑一遍。",
    "problem-anchor": "开始之前，先选一个你最想弄明白的问题。是想知道那一段报错信息到底在说什么，还是想知道程序不报错但结果不对时该从哪里查，又或者你想弄明白为什么说「慢一点、看一步」比「全部重写」更管用，再或者你想学会改完以后怎么确认真的改对了。选好了，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能读懂一段报错信息，说出它指的是哪一行、出了什么事。第二，能在一段有问题的程序里点出出错的那一行，并说出可能的原因。第三，能改掉出错的地方，然后重新运行一遍，确认这一次真的跑通了。第四，能在一段不报错但结果不对的程序里，用小手算一遍的方法找出问题，并试着用改动最小的办法修好它。",
    "pretest": "先做三道小题，用你现在的想法选就行。选完马上能看到解释，选错了也没关系，正好知道该重点听哪里。",
    "module-1": "先学会看报错信息。程序出错的时候，它其实很愿意帮你：它会告诉你停在了哪一行，会告诉你它看到了一个不认识的名字，有时候还会告诉你它在哪一步卡住了。读报错要按顺序读三件事：第一，看它说的行号，这是出事的位置；第二，看它说的那句话，那是它在抱怨什么；第三，想一想它抱怨的那个东西，第一次出现是在哪一行。要特别记住：报错指出的行号，是出事的位置，不一定就是根因所在——真正要改的地方，常常要往前对齐一下名字。",
    "lab-1": "光看还不够，我们自己来读一遍。下面是一段记录跑步总分的程序，它跑不动了，并且给出了一条报错信息。请你点一点报错信息里的三块线索卡，看看程序里对应的那一行会怎么亮起来，再读一读每句话在说什么。最后判断一下：真正要改的，到底是哪一行。",
    "module-2": "报错信息能帮我们，可它只帮一半忙。程序里的问题分两种：一种是看得见的，程序会停下来告诉你；另一种是看不见的，它安安静静跑完，只是结果不对。看不见的那种最麻烦，也最需要方法。方法就是一句话：先自己用小手算一遍。拿一个小一点的数据，自己算出答案，再和程序给的结果对一对，对不上就说明某一步多做了或者少做了。然后按这个圈走：运行、发现问题、定位到那一行、改好、再运行一遍。这个圈要一直转到结果对为止，这就是调试，也就是一遍一遍地改进。",
    "lab-2": "现在轮到你动手了。下面有两关，每一关都给你一段跑不通的程序，还有它给出的报错信息。请你点一点你认为出问题的那一行：点对了，它会告诉你错在哪里，并且出现一个修正按钮；点错了也没关系，它会提示你再想想。改好以后，点重新运行，看着程序一行一行跑通。",
    "worked-example": "我们一起来看一段「能跑，但结果不对」的程序。它要把三天的跳绳个数加起来，程序给的结果是二百七十。第一步，先自己用小手算一遍：一百二十加一百五十再加一百三十，等于四百。第二步，两个数对不上，二百七十比四百少了整整一天，说明它少加了一天。第三步，数一数它转了几圈：条件写的是「天数 小于 3」，天数从 1 开始，只能转两圈；要加三天，应该转三圈。第四步，把「小于」改成「小于等于」，让它把第三天也算进去，再跑一遍，结果正好四百。",
    "conceptest-1": "接下来用三个容易弄错的说法考考你。请仔细读每一个选项，选完再看解释。",
    "synthesis": "最后一个任务交给你。这段程序能跑完，也不报错，可总数就是少了一天的量。请你先点「我自己先算一遍」，用小手算出正确答案；接着点单步执行，看程序到底转了几圈；然后点出你认为出问题的那一行，把它改好，再重新运行一次，看结果对不对得上。改完以后还有一个小问题等你：如果以后要统计五天，这个程序要改几处？",
    "posttest": "最后一轮，换几个新情境来考考你。这次会出现自动售货机、体温登记表和一段改了三次才对的程序，看看你能不能把学到的办法用上去。",
    "summary": "这节课我们记住三句话。第一句，报错信息要读三件事：停在第几行、它在抱怨什么、那个名字第一次出现在哪里。第二句，程序的问题分两种，报错能指出看得见的那种，看不见的那种要靠自己用小手算一遍去发现。第三句，调试就是一个圈：运行、找出那一行、改好、再运行一遍，一直转到结果对上为止；而且每次只改该改的地方，不要整段重写。回到开头那锅太咸的菜：你尝一口、想一想、少放一点盐再尝一口，就是调试。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：把你今天在课上见过的两条报错信息抄下来，各写一句它到底在说什么。第二层能力应用，动手做：找一段能跑但结果不对的小程序，用小手算一遍找出问题，把修改前后运行的结果都记下来。第三层迁移挑战，选做：给自己的程序写一份「出错记录」，写明出过什么问题、你是怎么找到的、最后改了什么，下星期再看一遍。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是学它之前要先会的，右边是学会之后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续学的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 报错信息读三件事", "lab-1": "动手一 读一条报错信息",
    "module-2": "概念二 两种错误与调试循环", "lab-2": "动手二 找出那一行并改好重跑",
    "worked-example": "例题讲解 先自己算一遍", "conceptest-1": "概念测试",
    "synthesis": "综合任务 不报错但结果不对", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

CUSTOM_JS = r"""
/* ============================================================
   it-e-debugging 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) renderCode()：伪代码行渲染 + 高亮 + 可点选 + 已修正标记
   3) 动手一：读报错信息（点线索卡 → 高亮对应行 → 判断真正要改哪一行）
   4) 动手二（核心模拟）：点选问题行 → 即时错因 → 修正 → 重新运行跑通（两关）
   5) 综合任务：不报错但结果不对 → 手工验算 → 定位边界 bug → 修正重跑 + 迭代提问
   ============================================================ */
(function () {
  'use strict';

  /* ---------- 1. 选择题 ---------- */
  document.querySelectorAll('[data-quiz-block]').forEach(function (block) {
    block.querySelectorAll('.choice').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (block.dataset.answered === '1') return;
        block.dataset.answered = '1';
        var ok = btn.dataset.correct === '1';
        btn.classList.add(ok ? 'correct' : 'wrong');
        block.querySelectorAll('.choice').forEach(function (b) {
          if (b.dataset.correct === '1') b.classList.add('correct');
          b.disabled = true;
        });
        var ex = block.querySelector('[data-explain]');
        if (ex) ex.style.display = 'block';
      });
    });
  });

  /* ---------- 通用样式（走主题变量，不写死颜色） ---------- */
  var st = document.createElement('style');
  st.textContent =
    '.dg-wrap{display:grid;grid-template-columns:minmax(0,1.08fr) minmax(230px,0.92fr);gap:14px;align-items:start;}' +
    '@media(max-width:760px){.dg-wrap{grid-template-columns:1fr;}}' +
    '.dg-code{display:flex;flex-direction:column;gap:4px;padding:10px;border-radius:12px;' +
    'background:var(--bg-subtle);border:1px solid var(--line-subtle);}' +
    '.dg-line{display:flex;align-items:flex-start;gap:9px;padding:7px 10px;border-radius:8px;' +
    'background:var(--card);border:1px solid transparent;font-size:14px;' +
    'font-family:ui-monospace,SFMono-Regular,Menlo,monospace;transition:all .2s ease;}' +
    '.dg-line .dg-n{flex-shrink:0;width:20px;height:20px;border-radius:5px;display:grid;place-items:center;' +
    'background:rgb(var(--paper-rgb) / 20%);color:var(--muted);font-size:11px;font-weight:800;}' +
    '.dg-line .dg-c{flex:1;min-width:0;word-break:break-word;}' +
    '.dg-line.pickable{cursor:pointer;}' +
    '.dg-line.pickable:hover{border-color:rgb(var(--brand-rgb) / 45%);background:var(--brand-soft);}' +
    '.dg-line.run{border-color:var(--brand);background:var(--brand-soft);' +
    'box-shadow:0 0 0 3px rgb(var(--brand-rgb) / 16%);}' +
    '.dg-line.run .dg-n{background:var(--brand);color:#fff;}' +
    '.dg-line.check{border-color:var(--warn);background:rgb(var(--warm-rgb) / 20%);}' +
    '.dg-line.tried{border-color:rgba(239,68,68,.45);background:rgba(239,68,68,.07);}' +
    '.dg-line.ok{border-color:var(--brand-2);background:var(--accent-soft);}' +
    '.dg-line.ok .dg-n{background:var(--brand-2);color:#fff;}' +
    '.dg-side{display:flex;flex-direction:column;gap:10px;}' +
    '.dg-err{padding:12px 14px;border-radius:12px;background:rgba(239,68,68,.08);' +
    'border:1px solid rgba(239,68,68,.3);font-family:ui-monospace,SFMono-Regular,Menlo,monospace;' +
    'font-size:13px;line-height:1.75;}' +
    '.dg-err .dg-errlab{display:block;font-family:-apple-system,"PingFang SC",sans-serif;' +
    'font-weight:800;font-size:12px;color:#c2410c;margin-bottom:4px;}' +
    '.dg-clue{width:100%;text-align:left;font-size:13px;font-weight:700;}' +
    '.dg-clue:hover{background:var(--brand-soft);}' +
    '.dg-read{padding:10px 12px;border-radius:12px;background:var(--bg-subtle);' +
    'border:1px solid var(--line-subtle);font-size:14px;line-height:1.7;min-height:56px;}' +
    '.dg-tabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;}' +
    '.dg-tab{text-align:center;font-weight:800;font-size:14px;}' +
    '.dg-tab.on{border-color:var(--brand);background:var(--brand-soft);box-shadow:0 0 0 3px rgb(var(--brand-rgb) / 16%);}' +
    '.lab-readout{display:flex;gap:10px;flex-wrap:wrap;margin-top:10px;}' +
    '.readout-cell{flex:1;min-width:104px;background:var(--bg-subtle);border:1px solid var(--line-subtle);' +
    'border-radius:12px;padding:9px 11px;text-align:center;}' +
    '.readout-cell .k{display:block;font-size:12px;color:var(--muted);}' +
    '.readout-cell .v{font-size:19px;font-weight:800;color:var(--link);font-variant-numeric:tabular-nums;}' +
    '.readout-cell .v.green{color:var(--accent-deep);}' +
    '.choice{border:1.5px solid rgb(var(--brand-rgb) / 32%);background:var(--card);}' +
    '.choice:hover{background:var(--brand-soft);border-color:rgb(var(--brand-rgb) / 55%);}' +
    '.kid-note{border-color:rgb(var(--warm-rgb) / 80%);}';
  document.head.appendChild(st);

  /* ---------- 2. 代码行渲染 ---------- */
  function renderCode(el, lines, cur, marks, pickable) {
    if (!el) return;
    el.innerHTML = '';
    lines.forEach(function (txt, k) {
      var row = document.createElement('div');
      var cls = 'dg-line';
      if (pickable) cls += ' pickable';
      if (cur === k + 1) cls += ' run';
      if (marks && marks[k + 1]) cls += ' ' + marks[k + 1];
      row.className = cls;
      var n = document.createElement('span');
      n.className = 'dg-n';
      n.textContent = (k + 1);
      var c = document.createElement('span');
      c.className = 'dg-c';
      c.textContent = txt;
      row.appendChild(n);
      row.appendChild(c);
      el.appendChild(row);
    });
  }

  function lineIndex(el, node) {
    while (node && node.parentNode !== el) node = node.parentNode;
    if (!node) return 0;
    return Array.prototype.indexOf.call(el.children, node) + 1;
  }

  /* ---------- 3. 动手一：读一条报错信息 ---------- */
  (function () {
    var out = document.getElementById('dg1-out');
    if (!out) return;
    var code = document.getElementById('dg1-code');
    var LINES = [
      '跑步次数 = 0',
      '总分 = 0',
      '当 跑步次数 <= 3 时',
      '    总分 = 总分 + 距离[跑步次数]',
      '    次数 = 次数 + 1',
      '结束',
      '输出 总分'
    ];
    var CLUES = {
      c1: { line: 5, cls: 'run',
        head: '线索一：「程序停在第 5 行」。',
        text: '报错里的行号，就是在告诉你出事的位置。程序里第 5 行已经亮起来了——它就是程序停下来的那一行，后面的「结束」和「输出」都没有机会做。' },
      c2: { line: 5, cls: 'run',
        head: '线索二：「名字「次数」还没有出现过」。',
        text: '这是报错里最有用的一句。程序看到了「次数」这个名字，可是前面从没在哪一行给它起过名字。它不认识这个名字，所以停住了。' },
      c3: { line: 1, cls: 'check',
        head: '线索三：回到第 1 行对一对名字。',
        text: '第 1 行已经亮起来了。看仔细：那里起名字用的是「跑步次数」，不是「次数」。两处名字对不上——这才是真正的原因。报错指的行是「出事的位置」，根因往往要往前对一下名字。' }
    };
    var pickLine = 5, pickCls = 'run', judged = false;

    function paint() {
      var marks = {};
      if (pickLine > 0) marks[pickLine] = pickCls;
      renderCode(code, LINES, -1, marks, false);
    }

    document.querySelectorAll('[data-dg1-clue]').forEach(function (b) {
      b.addEventListener('click', function () {
        var c = CLUES[b.dataset.dg1Clue];
        if (!c) return;
        pickLine = c.line;
        pickCls = c.cls;
        paint();
        out.className = 'result warn';
        out.innerHTML = '<strong>' + c.head + '</strong>' + c.text;
      });
    });

    document.querySelectorAll('[data-dg1-judge]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (judged) return;
        judged = true;
        var ok = b.dataset.dg1Judge === '5';
        pickLine = ok ? 5 : 1;
        pickCls = 'run';
        paint();
        b.classList.add(ok ? 'correct' : 'wrong');
        out.className = 'result ' + (ok ? '' : 'warn');
        out.innerHTML = ok
          ? '<strong>对了，要改的就是第 5 行。</strong>把它写成「次数 = 跑步次数 + 1」，两处的名字就一致了，程序就能接着往下走。' +
            '<br><span style="color:var(--muted)">记住这个顺序：先看它停在哪一行，再看它抱怨什么，最后回到那个名字第一次出现的地方对一对。</span>'
          : '<strong>再想一想。</strong>第 1 行没有错——它给变量起名字起得很对。'
            + '<br><span style="color:var(--muted)">错因提醒：常见错误是看到报错就回头改第一行。'
            + '报错说的是「这个名字没出现过」，所以要改的是那个把名字写错的地方，也就是第 5 行。</span>';
      });
    });
    paint();
  })();

  /* ---------- 4. 动手二（核心模拟）：点出问题行 → 修正 → 重新运行跑通 ---------- */
  function makeRound(prefix, R) {
    var codeEl = document.getElementById(prefix + '-code');
    var outEl = document.getElementById(prefix + '-out');
    var readEl = document.getElementById(prefix + '-read');
    var fixBtn = document.getElementById(prefix + '-fix');
    if (!codeEl || !outEl || !fixBtn) return;
    var state = { fixed: false, cur: -1, timer: null, trace: [], picked: [] };

    function paint() {
      var cur = (state.cur >= 0 && state.cur < state.trace.length) ? state.trace[state.cur].line : -1;
      var marks = {};
      if (state.fixed) marks[R.bugLine] = 'ok';
      state.picked.forEach(function (n) { if (n !== R.bugLine) marks[n] = 'tried'; });
      renderCode(codeEl, R.lines(state.fixed), cur, marks, !state.fixed);
      if (state.cur >= 0 && state.cur < state.trace.length) {
        var s = state.trace[state.cur];
        readEl.textContent = '第 ' + (state.cur + 1) + ' 步（第 ' + s.line + ' 行）：' + s.note;
      } else {
        readEl.textContent = state.fixed
          ? '改好了，点「重新运行」看看这一次能不能跑通。'
          : '先点一点你认为出问题的那一行。';
      }
    }

    function build(fixed) { state.trace = R.build(fixed); state.cur = -1; }

    function advance() {
      if (state.cur >= state.trace.length - 1) return false;
      state.cur++;
      paint();
      return state.cur < state.trace.length - 1;
    }

    function notFixedMsg() {
      outEl.className = 'result error';
      outEl.innerHTML = '<strong>还是同样的毛病：' + R.errShort + '</strong><br>' +
        '<span style="color:var(--muted)">先在上面那段程序里点一点你认为出问题的那一行，找到以后把它改好，再来运行。</span>';
      paint();
    }

    codeEl.addEventListener('click', function (e) {
      if (state.fixed || state.timer !== null) return;
      var idx = lineIndex(codeEl, e.target);
      if (!idx) return;
      if (state.picked.indexOf(idx) < 0) state.picked.push(idx);
      if (idx === R.bugLine) {
        fixBtn.style.display = '';
        fixBtn.textContent = '🔧 ' + R.fixLabel;
        outEl.className = 'result';
        outEl.innerHTML = '<strong>找到了！就是第 ' + idx + ' 行。</strong>' + R.why +
          '<br><span style="color:var(--muted)">错因提醒：' + R.errWhy + '</span>' +
          '<br><span style="color:var(--muted)">下一步：点下面的修正按钮把它改掉，然后重新运行一次。</span>';
      } else {
        outEl.className = 'result warn';
        outEl.innerHTML = '<strong>第 ' + idx + ' 行看着是对的。</strong>' + R.hint +
          '<br><span style="color:var(--muted)">错因提醒：常见错误是凭感觉乱点一行就动手改——' +
          '先回到报错信息，看它到底在抱怨什么。</span>';
      }
      paint();
    });

    fixBtn.addEventListener('click', function () {
      if (state.fixed) return;
      state.fixed = true;
      fixBtn.style.display = 'none';
      build(true);
      paint();
      outEl.className = 'result';
      outEl.innerHTML = '<strong>已经改好了。</strong>' + R.fixedNote +
        '<br><span style="color:var(--muted)">现在点「重新运行」，一行一行看着它跑完。</span>';
    });

    document.getElementById(prefix + '-run').addEventListener('click', function () {
      if (state.timer !== null) return;
      if (!state.fixed) { notFixedMsg(); return; }
      build(true);
      paint();
      outEl.className = 'result warn';
      outEl.textContent = '正在一行一行跑……亮起来的那一行就是程序正在做的这一步。';
      state.timer = setInterval(function () {
        if (!advance()) {
          clearInterval(state.timer);
          state.timer = null;
          paint();
          outEl.className = 'result';
          outEl.innerHTML = '<strong>🎉 这一遍跑通了，结果也对上了。</strong>' + R.okNote;
        }
      }, 580);
    });

    document.getElementById(prefix + '-step').addEventListener('click', function () {
      if (state.timer !== null) return;
      if (!state.fixed) { notFixedMsg(); return; }
      if (state.trace.length === 0) build(true);
      if (state.cur >= state.trace.length - 1) {
        outEl.className = 'result';
        outEl.innerHTML = '<strong>这一遍已经走完了。</strong>' +
          '<br><span style="color:var(--muted)">想再看一次，点「复位」回到开头，再单步执行。</span>';
        return;
      }
      advance();
    });

    document.getElementById(prefix + '-reset').addEventListener('click', function () {
      if (state.timer !== null) { clearInterval(state.timer); state.timer = null; }
      state.fixed = false;
      state.picked = [];
      fixBtn.style.display = 'none';
      build(false);
      paint();
      outEl.className = 'result warn';
      outEl.textContent = '程序复位了。点一点你认为出问题的那一行。';
    });

    build(false);
    paint();
    return { reset: function () { build(false); paint(); } };
  }

  /* 第一关：名字写错（报错能定位到行） */
  (function () {
    var L1 = [
      '及格人数 = 0',
      '次数 = 1',
      '当 次数 <= 3 时',
      '    如果 成绩[次序] >= 60 则',
      '        及格人数 = 及格人数 + 1',
      '    结束（分支）',
      '    次数 = 次数 + 1',
      '结束（循环，回到第 3 行）',
      '输出 及格人数'
    ];
    var SC = [72, 45, 88];
    makeRound('dg2a', {
      bugLine: 4,
      errShort: '第 4 行：名字「次序」还没有出现过',
      why: '程序看到的「次序」这个名字，前面从没哪一行给它起过名字。第 2 行起名字用的是「次数」，第 4 行却写成了「次序」——两个字颠倒了一下，程序就不认识了。',
      errWhy: '常见错误是把名字里的两个字写颠倒、多写一个字，自己读着挺顺，程序却完全不认识。写完名字，回头看一眼前面那一行是怎么起的。',
      fixLabel: '把第 4 行的「次序」改成「次数」',
      fixedNote: '第 4 行现在写成「如果 成绩[次数] >= 60 则」，和第 2 行的名字一模一样了。',
      hint: '再看一眼报错信息：它抱怨的那个名字，是「次序」还是「次数」？回到第 2 行，看看那个名字本来是怎么起的。',
      lines: function (fixed) {
        if (!fixed) return L1.slice();
        var a = L1.slice();
        a[3] = '    如果 成绩[次数] >= 60 则';
        return a;
      },
      build: function (fixed) {
        var t = [];
        if (!fixed) {
          t.push({ line: 1, note: '及格人数设成 0。' });
          t.push({ line: 2, note: '次数从 1 开始。' });
          t.push({ line: 3, note: '次数 1 <= 3 成立，进圈里。' });
          t.push({ line: 4, note: '程序走到这里，看到了一个不认识的名字「次序」——它停下来，不再往下走了。' });
          return t;
        }
        var pass = 0, k = 1, loops = 0;
        t.push({ line: 1, note: '及格人数设成 0。' });
        t.push({ line: 2, note: '次数从 1 开始。' });
        while (k <= 3) {
          loops++;
          var sc = SC[k - 1];
          t.push({ line: 3, note: '第 ' + loops + ' 圈：次数 ' + k + ' <= 3 成立，进圈里。' });
          var hit = sc >= 60;
          t.push({ line: 4, note: '看第 ' + k + ' 个成绩：' + sc + ' >= 60 吗？——' + (hit ? '成立。' : '不成立。') });
          if (hit) { pass++; t.push({ line: 5, note: '及格人数加 1，变成 ' + pass + '。' }); }
          else { t.push({ line: 6, note: '这一圈不加，走出分支。' }); }
          k++;
          t.push({ line: 7, note: '次数加 1，变成 ' + k + '。' });
        }
        t.push({ line: 3, note: '次数 ' + k + ' <= 3 不成立，走出循环，一共转了 ' + loops + ' 圈。' });
        t.push({ line: 9, note: '输出结果：及格人数 = ' + pass + '。' });
        return t;
      },
      okNote: '<br><span style="color:var(--muted)">这一次程序一路跑到最后，输出「及格人数 = 2」——' +
        '72 和 88 及格，45 不及格，正好两个人。常犯的错误就是把名字写错、两个相近的字颠倒，' +
        '而报错信息其实已经把行号告诉你了。</span>'
    });
  })();

  /* 第二关：语句放错位置（报错只说"停不下来"） */
  (function () {
    var L2 = [
      '总分 = 0',
      '次数 = 1',
      '当 次数 <= 3 时',
      '    总分 = 总分 + 成绩[次数]',
      '结束（循环，回到第 3 行）',
      '次数 = 次数 + 1',
      '输出 总分'
    ];
    var SC2 = [72, 45, 88];
    makeRound('dg2b', {
      bugLine: 6,
      errShort: '程序一直在转圈，停不下来',
      why: '「次数 = 次数 + 1」被放在了循环外面。圈里没有人去改变次数，条件就永远成立——循环找不到出口，只好一直转下去。',
      errWhy: '常见错误是以为「少放一句不要紧」——恰恰是这一句让循环有出口。以后写完循环，先问自己一句：谁让它迟早停下来？',
      fixLabel: '把第 6 行移进循环里（放到「结束」之前）',
      fixedNote: '「次数 = 次数 + 1」现在被放进了循环里，就在第 5 行「结束」的前面。',
      hint: '报错说它停不下来，那就去找「谁该让次数变大」——那件事现在在圈里还是圈外？',
      lines: function (fixed) {
        if (!fixed) return L2.slice();
        return [
          '总分 = 0',
          '次数 = 1',
          '当 次数 <= 3 时',
          '    总分 = 总分 + 成绩[次数]',
          '    次数 = 次数 + 1',
          '结束（循环，回到第 3 行）',
          '输出 总分'
        ];
      },
      build: function (fixed) {
        var t = [];
        if (!fixed) {
          t.push({ line: 1, note: '总分设成 0。' });
          t.push({ line: 2, note: '次数从 1 开始。' });
          var k = 1, n = 0;
          while (n < 3) {
            n++;
            t.push({ line: 3, note: '第 ' + n + ' 圈：次数 ' + k + ' <= 3 成立，进圈里。' });
            t.push({ line: 4, note: '总分加上第 ' + k + ' 个成绩。' });
            t.push({ line: 5, note: '这一圈走完了，回到第 3 行——可是次数还是 ' + k + '，一点没变。' });
          }
          t.push({ line: 6, note: '你看：转了三圈，次数还是 ' + k + '，第 6 行那句「次数 = 次数 + 1」永远排不上。它一直在转圈，停不下来。' });
          return t;
        }
        var total = 0, k2 = 1, loops = 0;
        t.push({ line: 1, note: '总分设成 0。' });
        t.push({ line: 2, note: '次数从 1 开始。' });
        while (k2 <= 3) {
          loops++;
          var sc = SC2[k2 - 1];
          t.push({ line: 3, note: '第 ' + loops + ' 圈：次数 ' + k2 + ' <= 3 成立，进圈里。' });
          total += sc;
          t.push({ line: 4, note: '总分加上 ' + sc + '，变成 ' + total + '。' });
          k2++;
          t.push({ line: 5, note: '次数加 1，变成 ' + k2 + '——这一回它在圈里，所以条件迟早会不成立。' });
        }
        t.push({ line: 3, note: '次数 ' + k2 + ' <= 3 不成立，走出循环，一共转了 ' + loops + ' 圈。' });
        t.push({ line: 7, note: '输出结果：总分 = ' + total + '。' });
        return t;
      },
      okNote: '<br><span style="color:var(--muted)">这一次它转了三圈就出来了，输出「总分 = 205」。' +
        '记住这个道理：循环必须有一个出口，而出口靠的是「圈里有人让条件迟早不成立」。</span>'
    });
  })();

  /* 页签切换 */
  document.querySelectorAll('[data-dg-tab]').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('[data-dg-tab]').forEach(function (x) { x.classList.remove('on'); });
      b.classList.add('on');
      var t = b.dataset.dgTab;
      document.querySelectorAll('[data-dg-pane]').forEach(function (p) {
        p.style.display = (p.dataset.dgPane === t) ? '' : 'none';
      });
    });
  });

  /* ---------- 5. 综合任务：不报错但结果不对 ---------- */
  (function () {
    var out = document.getElementById('dg3-out');
    if (!out) return;
    var code = document.getElementById('dg3-code');
    var read = document.getElementById('dg3-read');
    var fixBtn = document.getElementById('dg3-fix');
    var calcBtn = document.getElementById('dg3-calc');
    var CNT = [120, 150, 130];
    var LINES = [
      '跳绳总数 = 0',
      '天数 = 1',
      '当 天数 < 3 时',
      '    跳绳总数 = 跳绳总数 + 每次个数[天数]',
      '    天数 = 天数 + 1',
      '结束（循环，回到第 3 行）',
      '输出 跳绳总数'
    ];
    var state = { fixed: false, cur: -1, timer: null, trace: [], tried: {} };

    function lines() {
      if (!state.fixed) return LINES.slice();
      var a = LINES.slice();
      a[2] = '当 天数 <= 3 时';
      return a;
    }

    function build() {
      var total = 0, k = 1, loops = 0, t = [];
      t.push({ line: 1, note: '跳绳总数设成 0。' });
      t.push({ line: 2, note: '天数从 1 开始。' });
      while (state.fixed ? (k <= 3) : (k < 3)) {
        loops++;
        t.push({ line: 3, note: '第 ' + loops + ' 圈：天数 ' + k + (state.fixed ? ' <= 3' : ' < 3') + ' 成立，进圈里。' });
        total += CNT[k - 1];
        t.push({ line: 4, note: '加上第 ' + k + ' 天的 ' + CNT[k - 1] + ' 个，跳绳总数变成 ' + total + '。' });
        k++;
        t.push({ line: 5, note: '天数加 1，变成 ' + k + '。' });
      }
      t.push({ line: 3, note: '天数 ' + k + (state.fixed ? ' <= 3' : ' < 3') + ' 不成立 —— 走出循环，只转了 ' + loops + ' 圈。' });
      t.push({ line: 7, note: '输出结果：跳绳总数 = ' + total + '。' + (state.fixed ? '' : '（应该转 3 圈才对，少转了 1 圈。）') });
      return t;
    }

    function paint() {
      var cur = (state.cur >= 0 && state.cur < state.trace.length) ? state.trace[state.cur].line : -1;
      var marks = {};
      if (state.fixed) marks[3] = 'ok';
      Object.keys(state.tried).forEach(function (n) { if (Number(n) !== 3) marks[n] = 'tried'; });
      renderCode(code, lines(), cur, marks, !state.fixed);
      if (state.cur >= 0 && state.cur < state.trace.length) {
        read.textContent = '第 ' + (state.cur + 1) + ' 步（第 ' + state.trace[state.cur].line + ' 行）：' + state.trace[state.cur].note;
      } else {
        read.textContent = state.fixed
          ? '改好了，点「重新运行」看看这一回对不对得上。'
          : '先点「我自己先算一遍」算出正确答案，再点单步执行看程序转了几圈。';
      }
    }

    function rebuild() { state.trace = build(); state.cur = -1; }
    function advance() {
      if (state.cur >= state.trace.length - 1) return false;
      state.cur++;
      paint();
      return state.cur < state.trace.length - 1;
    }

    code.addEventListener('click', function (e) {
      if (state.fixed || state.timer !== null) return;
      var idx = lineIndex(code, e.target);
      if (!idx) return;
      state.tried[idx] = 1;
      if (idx === 3) {
        fixBtn.style.display = '';
        out.className = 'result';
        out.innerHTML = '<strong>找到了，就是第 3 行的条件。</strong>' +
          '程序写的是「天数 &lt; 3」，天数从 1 开始，只有 1 和 2 满足条件，所以只加了两天，140 加 130 得 270，第三天的 120 被漏掉了。' +
          '<br><span style="color:var(--muted)">错因提醒：这类错误程序不会报错——它只是老老实实按你写的条件执行。' +
          '要靠自己先算一遍答案，才能发现它少做了一轮。</span>' +
          '<br><span style="color:var(--muted)">下一步：点下面的修正按钮，把条件改成「小于等于」，再重新运行一次。</span>';
      } else {
        out.className = 'result warn';
        out.innerHTML = '<strong>第 ' + idx + ' 行看着没问题。</strong>' +
          '再看一眼：程序只转了 2 圈，可三天都要加。是哪一行的条件决定了转几圈？' +
          '<br><span style="color:var(--muted)">错因提醒：常见错误是从「输出」那一行开始怀疑——' +
          '输出本身没错，是它拿到的数就少了一天。</span>';
      }
      paint();
    });

    calcBtn.addEventListener('click', function () {
      out.className = 'result';
      out.innerHTML = '<strong>你自己算一遍：' + CNT[0] + ' + ' + CNT[1] + ' + ' + CNT[2] +
        ' = ' + (CNT[0] + CNT[1] + CNT[2]) + '。</strong>' +
        '<br><span style="color:var(--muted)">这就是正确答案。程序给出的却是 270，比它少了整整一天——' +
        '现在你知道该去查什么了：查它到底加了几天的。</span>';
    });

    fixBtn.addEventListener('click', function () {
      if (state.fixed) return;
      state.fixed = true;
      fixBtn.style.display = 'none';
      rebuild();
      paint();
      out.className = 'result';
      out.innerHTML = '<strong>已经改好了。</strong>第 3 行现在是「当 天数 &lt;= 3 时」，会转到第 3 天。' +
        '<br><span style="color:var(--muted)">现在点「重新运行」，看这一次输出对不对得上你算的答案。</span>';
    });

    document.getElementById('dg3-run').addEventListener('click', function () {
      if (state.timer !== null) return;
      if (!state.fixed) {
        out.className = 'result warn';
        out.innerHTML = '<strong>不着急运行。</strong>这段程序不报错，跑完只会给你一个错的答案。' +
          '<br><span style="color:var(--muted)">先点「我自己先算一遍」，再点单步执行，看看它转了几圈。</span>';
        return;
      }
      rebuild();
      paint();
      out.className = 'result warn';
      out.textContent = '正在一行一行跑……';
      state.timer = setInterval(function () {
        if (!advance()) {
          clearInterval(state.timer);
          state.timer = null;
          paint();
          out.className = 'result';
          out.innerHTML = '<strong>🎉 这一遍输出「跳绳总数 = 400」，和你算的一模一样。</strong>' +
            '<br><span style="color:var(--muted)">回顾一下这次调试的路：先自己算一遍答案 → 发现程序少做了一轮 → ' +
            '数了数它转了几圈 → 定位到条件那一行 → 改成「小于等于」→ 重新运行验证。</span>';
        }
      }, 580);
    });

    document.getElementById('dg3-step').addEventListener('click', function () {
      if (state.timer !== null) return;
      if (state.trace.length === 0) rebuild();
      if (state.cur >= state.trace.length - 1) {
        out.className = 'result';
        out.innerHTML = '<strong>这一遍已经走完了。</strong>' +
          '<br><span style="color:var(--muted)">想再看一次，点「复位」回到开头，再单步执行。</span>';
        return;
      }
      advance();
    });

    document.getElementById('dg3-reset').addEventListener('click', function () {
      if (state.timer !== null) { clearInterval(state.timer); state.timer = null; }
      state.fixed = false;
      state.tried = {};
      fixBtn.style.display = 'none';
      rebuild();
      paint();
      out.className = 'result warn';
      out.textContent = '程序复位了。先点「我自己先算一遍」，再单步执行看看它转了几圈。';
    });

    document.querySelectorAll('[data-dg3-iter]').forEach(function (b) {
      b.addEventListener('click', function () {
        var ok = b.dataset.dg3Iter === 'a';
        b.classList.add(ok ? 'correct' : 'wrong');
        out.className = 'result ' + (ok ? '' : 'warn');
        out.innerHTML = ok
          ? '<strong>对。</strong>要动的地方其实只有两处：第 3 行里的那个 3 改成 5，再把第 4 天、第 5 天的个数补进数据里。' +
            '其它行都不用碰。<br><span style="color:var(--muted)">这就是「迭代优化」的意思：' +
            '每次只改动该改的地方，然后重新运行验证一遍——小步改、小步验，比推倒重来稳得多。</span>'
          : '<strong>再想一想。</strong>整段重写一遍要多花很多时间，还容易带进新的错误。' +
            '<br><span style="color:var(--muted)">错因提醒：不少同学误认为「改动越彻底越保险」——' +
            '其实恰好相反，改动越小越容易检查出问题。想一想：控制「统计几天」的那个数，程序里出现在哪一行？</span>';
      });
    });

    rebuild();
    paint();
  })();
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：程序出错的时候，你会怎么做？", TTS["pretest"], [
        {"q": "程序运行时停下来，并且显示了一行报错信息。最该先做的是：",
         "options": [("读一读它说的行号和那句话，弄清它在抱怨什么", True),
                     ("把整段程序删掉重写一遍", False),
                     ("随便改一处再看看能不能跑", False)],
         "explain": "报错信息是程序在帮你：它告诉你停在哪一行、抱怨的是什么。"
                    "<strong>错因提醒：</strong>常见错误是一看到报错就整段重写——"
                    "其实问题常常只在某一行的某几个字上。"},
        {"q": "程序跑完了，也没有报错，可是给你的结果不对。这说明：",
         "options": [("程序里的某一步多做或少做了一次，得靠自己算一遍去发现", True),
                     ("电脑坏了", False),
                     ("这种错误没办法发现", False)],
         "explain": "不报错的错误是逻辑错，要靠自己用小手算一遍答案再去对照。"
                    "<strong>错因提醒：</strong>别误认为「不报错就是对的」——"
                    "跑得通和算得对，是两回事。"},
        {"q": "把程序改好以后，为什么一定要重新运行一遍？",
         "options": [("确认这一次真的跑通、结果也对上了", True),
                     ("让程序看起来新一点", False),
                     ("帮电脑记住这次修改", False)],
         "explain": "改完不跑，就等于没改——验证是调试里少不了的最后一步。"
                    "<strong>错因提醒：</strong>不少同学改完就交上去了，"
                    "结果同一个错误又出现了。改一次、跑一次，最稳。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "报错信息不是坏消息：它在告诉你三件事", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们已经能让程序走分支、转循环了（And）；可一旦程序停下来，很多同学的第一反应是「整段重写」，改了半天又踩进新的坑（But）；其实程序停下来的时候，它会把线索一起交给你，只要会读就能省下大半力气（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">报错信息要<strong>按顺序读三件事</strong>——读对了顺序，一半的问题当场就清楚了。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>停在哪一行：</strong>报错里的行号，就是出事的位置。先去那一行看一眼，后面的行还没轮到做。</div></div>
          <div class="step"><span class="n">2</span><div><strong>它在抱怨什么：</strong>是看到一个不认识的名字，还是条件写得不完整？这句话说清了症状。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>那个名字第一次出现在哪里：</strong>回到前面去对一对名字、对一对写法——根因常常在更前面的那一行。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="报错信息拆解示意图：一条报错信息被拆成「在哪一行」「出了什么事」「去看看前面怎么写的」三块">
          <figcaption>示意图：一条报错信息可以拆成三块来读——位置、症状、线索；读了这三块，再动手改</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">以为<strong>报错的行号就是要改的行</strong>，于是只看那一行。多数时候那一行确实是改动的落点，但有时它只是「被绊倒的地方」——比如前面起的名字和这里用的名字不一样。所以读完报错，要回到那个名字第一次出现的地方对一对。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>先看停在哪一行，再看它在怨什么，回头对一对名字，最后才动手改。</div></div>
{insight_box([
    {"lens": "看见它", "text": "报错信息的样子其实三行就够：一个位置、一句抱怨、偶尔加一句建议。看清三块，剩下的就是照着一行行对。"},
    {"lens": "拆开它", "text": "为什么程序能指出位置？因为它是照着顺序一行一行做的，走到哪一行做不下去，它自己最清楚。"},
    {"lens": "迁移它", "text": "这份读法放到生活里也好用：机器报的错、老师改的红笔、同学说的「看不懂」，都是线索，不是责怪。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：读一条报错信息，找出要改的那一行", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">这段记录跑步总分的程序跑不动了。请你点一点报错信息里的三块线索卡，看程序里哪一行会亮起来、每句话在说什么；最后判断真正要改的是哪一行。</p>
        <div class="lab-panel">
          <div class="dg-wrap">
            <div>
              <div style="font-weight:700;font-size:14px;margin-bottom:6px">程序（伪代码）</div>
              <div class="dg-code" id="dg1-code"></div>
            </div>
            <div class="dg-side">
              <div class="dg-err"><span class="dg-errlab">程序给出的报错信息（示意图）</span>程序停在第 5 行<br>名字「次数」还没有出现过</div>
              <div style="font-weight:700;font-size:14px;margin-top:4px">点一点这三块线索，看看各是什么意思</div>
              <button class="choice dg-clue" data-dg1-clue="c1">线索一：先看它说停在了哪一行</button>
              <button class="choice dg-clue" data-dg1-clue="c2">线索二：它在抱怨哪一个名字</button>
              <button class="choice dg-clue" data-dg1-clue="c3">线索三：回到那个名字第一次出现的地方</button>
              <div style="font-weight:700;font-size:14px;margin-top:4px">你的判断：真正要改的是哪一行？</div>
              <div class="flex-row" style="margin-top:0">
                <button class="choice" data-dg1-judge="1" style="text-align:center">第 1 行</button>
                <button class="choice" data-dg1-judge="5" style="text-align:center">第 5 行</button>
              </div>
            </div>
          </div>
          <p class="result warn" id="dg1-out" style="margin-top:12px">先点一张线索卡，看看对应的那一行怎么亮起来。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>看仔细：</strong>线索三亮起来的是第 1 行，可第 1 行并没有写错。它亮起来只是提醒你——回到这里对一对名字。「出事的位置」和「要改的位置」有时候不是同一行。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "两种错误与调试循环：跑得通不等于算得对", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">程序里的问题分<strong>两种</strong>：一种看得见，一种看不见。看不见的那一种，才最需要方法。</p>
        <div class="grid grid-2">
          <div class="inner-card"><p><strong>看得见的错：程序会停下来</strong></p><p style="color:var(--muted)">名字写错、语句放错位置、条件没写完……程序做不下去了，它会停下来，并把行号和抱怨一起告诉你。按概念一的三步就能读。</p></div>
          <div class="inner-card"><p><strong>看不见的错：跑完但结果不对</strong></p><p style="color:var(--muted)">程序一路做到底，没有一点抱怨，只是给你的答案不对。它不吭声，只能靠你自己去发现——这是最容易漏掉的一种。</p></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="调试循环示意图：运行、发现问题、定位到那一行、改好、再运行一遍，形成一个不断转动的圈">
          <figcaption>示意图：调试就是一个圈——运行、发现问题、定位到那一行、改好、再运行一遍，一直转到结果对上为止</figcaption>
        </figure>
        <div class="inner-card">
          <p><strong>看不见的错，靠这一招：先自己用小手算一遍。</strong></p>
          <p style="color:var(--muted)">挑一个小一点的数据，自己把答案算出来（比如三天的个数加起来是多少），再和程序给的结果对一对。对不上，就去数它<strong>转了几圈</strong>——多半是某一步多做了一次，或者少做了一次。这一步一用到，看不见的错也就看得见了。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">以为「程序跑完了就是对的」。跑得通，只说明它没被绊倒；算得对，才算真的对。另一个常见错误是改完就交——<strong>改一次、跑一次</strong>，确认这一次真的对上了，这一步不能省。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>跑通不等于算对，先自己算一遍；小步改、小步验，改完记得再跑一遍。</div></div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：点出问题行，改好，再跑一遍", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">两个关卡，每关都有一段跑不通的程序和它的报错信息。请点一点你认为出问题的那一行：点对了会告诉你错在哪里，还会出现一个修正按钮。</p>
        <div class="dg-tabs">
          <button class="choice dg-tab on" data-dg-tab="a" style="flex:1">第 1 关：名字对不上</button>
          <button class="choice dg-tab" data-dg-tab="b" style="flex:1">第 2 关：它停不下来了</button>
        </div>
        <div class="lab-panel" data-dg-pane="a">
          <div class="dg-wrap">
            <div>
              <div style="font-weight:700;font-size:14px;margin-bottom:6px">程序（点一行选它）</div>
              <div class="dg-code" id="dg2a-code"></div>
            </div>
            <div class="dg-side">
              <div class="dg-err"><span class="dg-errlab">报错信息（示意图）</span>程序停在第 4 行<br>名字「次序」还没有出现过</div>
              <div class="dg-read" id="dg2a-read">先点一点你认为出问题的那一行。</div>
              <button class="choice" id="dg2a-fix" style="display:none;text-align:center">🔧 修正</button>
              <div class="flex-row" style="margin-top:0">
                <button class="choice" id="dg2a-run" style="text-align:center">▶ 重新运行</button>
                <button class="choice" id="dg2a-step" style="text-align:center">单步执行</button>
                <button class="choice" id="dg2a-reset" style="text-align:center">复位</button>
              </div>
            </div>
          </div>
          <p class="result warn" id="dg2a-out" style="margin-top:12px">点一点你认为出问题的那一行。</p>
        </div>
        <div class="lab-panel" data-dg-pane="b" style="display:none">
          <div class="dg-wrap">
            <div>
              <div style="font-weight:700;font-size:14px;margin-bottom:6px">程序（点一行选它）</div>
              <div class="dg-code" id="dg2b-code"></div>
            </div>
            <div class="dg-side">
              <div class="dg-err"><span class="dg-errlab">报错信息（示意图）</span>程序一直在转圈<br>停不下来</div>
              <div class="dg-read" id="dg2b-read">先点一点你认为出问题的那一行。</div>
              <button class="choice" id="dg2b-fix" style="display:none;text-align:center">🔧 修正</button>
              <div class="flex-row" style="margin-top:0">
                <button class="choice" id="dg2b-run" style="text-align:center">▶ 重新运行</button>
                <button class="choice" id="dg2b-step" style="text-align:center">单步执行</button>
                <button class="choice" id="dg2b-reset" style="text-align:center">复位</button>
              </div>
            </div>
          </div>
          <p class="result warn" id="dg2b-out" style="margin-top:12px">点一点你认为出问题的那一行。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🛠️</span><div><strong>注意这个顺序：</strong>先看懂报错 → 再点出那一行 → 再改 → <strong>最后一定要重新运行</strong>。跳过最后一步，你其实并不知道自己改对了没有。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：跑得通但算错了，怎么查？", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>三天的跳绳个数是 120、150、130，要把它们加起来。程序的循环条件是「当 天数 &lt; 3 时」，天数从 1 开始，最后输出 270。它错在哪里？</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先自己用小手算一遍：</strong>120 加 150 再加 130，等于 400。这是正确答案，先把它写在纸上。</div></div>
          <div class="step"><span class="n">2</span><div><strong>和程序的结果对一对：</strong>400 和 270 差得很远，正好差 130——也就是整整一天的量。说明有某一天没被加进去。</div></div>
          <div class="step"><span class="n">3</span><div><strong>数一数它转了几圈：</strong>「天数 &lt; 3」，天数是 1 和 2 时成立，只转了两圈；要加三天，应该转三圈。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>回去改那一处再跑一遍：</strong>把条件改成「天数 ≤ 3」，让它把第三天也算进去；重新运行，输出正好 400，对上了。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">先去看最后那个「输出」那一行——以为打印的方式有问题。其实输出的写法没有错，是它拿到的数字本身就少了一天。另一个常见错误是<strong>跳过第 1 步</strong>：不先算一遍正确答案，就不知道程序该给多少，自然也就发现不了它错了。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三种说法，错在哪里", TTS["conceptest-1"], [
        {"q": "报错信息说「第 6 行：名字「结杲」还没有出现过」。最该先看的是：",
         "options": [("第 6 行里那个名字，和前面某一行起的名字是不是对得上", True),
                     ("直接把第 6 行整行删掉", False),
                     ("从第 1 行开始把所有行都改一遍", False)],
         "explain": "报错说它不认识这个名字，那就回去找这个名字该在哪一行被起过。"
                    "<strong>错因提醒：</strong>常见错误是删行或全改——"
                    "名字对不上只是几个字的问题，改对那几个字就够了。"},
        {"q": "程序跑完了，也没有报错，但答案明显偏小。可能性最大的是：",
         "options": [("循环多做或少做了一次，某一步没有算进去", True),
                     ("显示器显示不准", False),
                     ("程序跑得太快了", False)],
         "explain": "答案差一份，通常是「轮次」差了一圈——去数它转了几圈。"
                    "<strong>错因提醒：</strong>这类错误不会报错，"
                    "要先自己算一遍答案，才知道它差了多少。"},
        {"q": "改好一处之后，最好怎么做？",
         "options": [("重新运行一次，确认这一次跑通、结果也对上了", True),
                     ("赶紧把文件关掉，免得又出错", False),
                     ("继续往下改好几处，最后一起运行", False)],
         "explain": "改一次、跑一次，出问题也能马上知道是哪一处带来的。"
                    "<strong>错因提醒：</strong>一次性改很多处再运行，"
                    "万一还是不对，就分不清是哪一处没改好了。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：不报错、但结果不对的一段程序", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">这段程序能一路跑到底，也不报错，可是跳绳总数就是少了一天的量。请先自己算一遍，再单步执行看它转了几圈，最后把出问题的那一处改好、重新运行。</p>
        <div class="lab-panel">
          <div class="dg-wrap">
            <div>
              <div style="font-weight:700;font-size:14px;margin-bottom:6px">程序（点一行选它）</div>
              <div class="dg-code" id="dg3-code"></div>
              <div class="flex-row" style="margin-top:8px">
                <button class="choice" id="dg3-calc" style="text-align:center">🧮 我自己先算一遍</button>
                <button class="choice" id="dg3-run" style="text-align:center">▶ 重新运行</button>
                <button class="choice" id="dg3-step" style="text-align:center">单步执行</button>
                <button class="choice" id="dg3-reset" style="text-align:center">复位</button>
              </div>
            </div>
            <div class="dg-side">
              <div class="inner-card" style="margin:0">
                <p style="margin:0"><strong>数据（三天的跳绳个数）</strong></p>
                <p style="color:var(--muted);margin:6px 0 0">第一天 120 个 · 第二天 150 个 · 第三天 130 个</p>
              </div>
              <div class="dg-read" id="dg3-read">先点「我自己先算一遍」算出正确答案，再点单步执行看程序转了几圈。</div>
              <button class="choice" id="dg3-fix" style="display:none;text-align:center">🔧 修正</button>
            </div>
          </div>
          <p class="result warn" id="dg3-out" style="margin-top:12px">先点「我自己先算一遍」，再点单步执行。</p>
        </div>
        <div class="inner-card">
          <p><strong>再想一想（改动怎样才能最小）：</strong>如果以后要统计五天，这个程序需要改几处？</p>
          <div class="flex-row" style="margin-top:8px">
            <button class="choice" data-dg3-iter="a" style="text-align:center">只改控制天数的那个数和数据</button>
            <button class="choice" data-dg3-iter="b" style="text-align:center">整段程序全部重写一遍</button>
          </div>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个情境，办法还在不在", TTS["posttest"], [
        {"q": "自动售货机程序报错：「第 7 行：名字「找零」还没有出现过」。最合理的下一步是：",
         "options": [("看第 7 行用到的这个名字，前面哪一行该给它起名字", True),
                     ("把售货机拆开看看", False),
                     ("把第 7 行以后的行全部删掉", False)],
         "explain": "还是那条老规矩：报错说名字不认识，就回去对一对名字。"
                    "<strong>错因提醒：</strong>别一看到报错就删代码——"
                    "删掉之后原来的功能也没了。"},
        {"q": "体温登记表程序把同一个人的记录打印了两次，但它没有报错。最该先做的是：",
         "options": [("自己数一遍应该打印几条，再看程序实际打了几条", True),
                     ("换一台电脑再试", False),
                     ("把打印出来的纸撕掉重打", False)],
         "explain": "先算清楚「应该几条」，才知道「多了几条」，问题就好找了。"
                    "<strong>错因提醒：</strong>不报错的错误，"
                    "永远靠「先自己算一遍」才抓得住。"},
        {"q": "一段程序你改了三次才对。关于这三次修改，下面说法正确的是：",
         "options": [("每改一次就跑一次，是小步改进，比一次全改更容易查", True),
                     ("改三次说明你不适合写程序", False),
                     ("应该一开始就把整段推倒重写，省时间", False)],
         "explain": "小步改、小步验，是经验丰富的做法；一次改太多，出错时反而分不清原因。"
                    "<strong>错因提醒：</strong>别误认为「改了很多次」是笨——"
                    "能一步步收敛到正确结果，正是调试的本事。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把调试讲清楚", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>报错信息读三件事：</strong>停在第几行、它在抱怨什么、那个名字第一次出现在哪里。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>两种错误要分清：</strong>停得下来的那种照着报错读；停不下来的那种先自己用小数据算一遍。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>调试是一个圈：</strong>运行、找那一行、改好、再运行一遍；每次只改该改的地方，不要整段重写。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那锅太咸的菜：</strong>你尝一口、想一想、少放一点盐，再尝一口——这就是调试。程序出错不是坏事，它只是还没被调好；而你已经有了一套能一遍遍用下去的办法。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「报错、两种错、再跑一遍」这三个词，说清楚你会怎么处理一段出问题的程序。</p>
          <p style="color:var(--muted)">再动一动手：<strong>写下来</strong>——给今天课上遇到的两次错误各写一行「出错记录」：错在哪一行、为什么错、最后怎么改的。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "把课上见过的两条报错信息抄下来，各写一句「它到底在说什么」。",
            "说出两种错误的区别：哪一种程序会停下来告诉你，哪一种只能靠自己算一遍才发现。",
        ],
        [
            "找一段能跑但结果不对的小程序（也可以自己写一段），先手工算出正确答案，再找出是哪一步多做或少做了一次，把修改前后两次运行的结果都记下来。",
            "用两三句话记下你一次「一次改太多、结果查不出来」的经历，说说后来你改成了什么做法。",
        ],
        [
            "给自己的程序写一份「出错记录」：写明出过什么问题、你是怎么找到的、最后改了什么；下星期再拿出来看一遍。",
            "如果一段程序里有三个地方要改，你会一次全改完再运行，还是改一处跑一次？说说你的理由，并动手试试两种做法。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-e-debugging",
    "node_id": "it-e-debugging",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 小学",
    "title": "程序调试与迭代",
    "name_en": "Debugging and Iteration",
    "grade": 5,
    "grade_cn": "五年级",
    "domain": "algorithm-programming",
    "domain_cn": "算法与程序",
    "lesson_type": "concept-practice",
    "version": "1.0.0",
    "description": "面向小学五年级：能按「位置—症状—线索」三步读懂一段报错信息；能在有问题的伪代码里点出出错的那一行并说出原因；能改好之后重新运行、确认这一次真的跑通且结果对得上；能在一段不报错但结果不对的程序里，先用小数据手工验算再定位到出问题的一处，并用改动最小的办法修好。",
    "tags": ["程序调试", "报错信息", "迭代优化", "错误定位", "计算思维"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》小学「算法与程序」——能发现程序错误并尝试修改，体验迭代优化。",
    "hero_question": "做菜太咸了，你会尝一口、想一想、少放一点盐——程序出了错，你也会这么做吗？",
    "hero_alt": "程序调试与迭代知识结构图：读懂报错、找到那一行、改好再跑一遍三栏",
    "hero_caption": "程序调试：读懂报错三件事 · 找那一行 · 改好再跑一遍",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的动手活动都会围着它转。",
    "anchor_choices": [
        {"t": "那一段报错信息到底在说什么？", "d": "从哪里开始读，读哪几个字最有用", "v": "那一段报错信息到底在说什么"},
        {"t": "程序不报错，但结果不对，从哪查？", "d": "它一声不吭，我怎么知道哪里做多了", "v": "程序不报错但结果不对从哪查"},
        {"t": "为什么说慢一点、看一步更好？", "d": "为什么一次全改完反而更慢", "v": "为什么说慢一点看一步更好"},
        {"t": "改完以后怎么知道真的改对了？", "d": "想学会自己验证、自己收尾", "v": "改完以后怎么知道真的改对了"},
    ],
    "objectives": [
        "能按「停在第几行、它在抱怨什么、那个名字第一次出现在哪里」三步读懂一段报错信息",
        "能在有问题的伪代码里点出出错的那一行，并说出可能的原因",
        "能改掉出错的地方并重新运行，确认这一次真的跑通、结果也对得上",
        "能在一段不报错但结果不对的程序里，先用小数据手工验算，再定位到出问题的一处，并用改动最小的办法修好",
    ],
    "objectives_plain": [
        "能按「停在第几行、它在抱怨什么、那个名字第一次出现在哪里」三步读懂一段报错信息",
        "能在有问题的伪代码里点出出错的那一行，并说出可能的原因",
        "能改掉出错的地方并重新运行，确认这一次真的跑通、结果也对得上",
        "能在一段不报错但结果不对的程序里，先用小数据手工验算，再定位到出问题的一处，并用改动最小的办法修好",
    ],
    "standards": [
        {"content": "能发现程序错误并尝试修改，体验迭代优化",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 算法与程序"},
        {"content": "养成「改一次、跑一次」的验证习惯，体会小步改进比推倒重来更稳",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 计算思维"},
    ],
    "prereqs": ["it-e-branch-loop"],
    "prereqs_name": "分支与循环结构",
    "prereqs_meta": "it-e-branch-loop",
    "leads_to": ["it-e-input-output"],
    "next_meta": "it-e-input-output",
    "section_images": ["assets/it-e-debugging-fig1.webp", "assets/it-e-debugging-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "程序出错不是坏事：它要么把线索交给你，要么安安静静给你一个错答案。两种都要会对付。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能自己读报错、自己找出那一行、自己改好再跑一遍。",
        "objectives": "看清四件事：报错怎么读、不报错的错怎么查、为什么小步改更好、怎么确认真的对了。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "读报错三步：停在哪一行、在抱怨什么、那个名字第一次出现在哪里。",
        "lab-1": "三张线索卡各点一下，看哪一行亮起来、每句在说什么，最后再判断改哪一行。",
        "module-2": "两种错误：停得下来的照着报错读；停不下来的先自己用小数据算一遍。",
        "lab-2": "顺序别乱：看懂报错 → 点出那一行 → 改 → 一定要重新运行。",
        "worked-example": "四步：自己算一遍、和结果对一对、数它转了几圈、改那一处再跑一遍。",
        "conceptest-1": "三个说法里都藏着高频错误，选完把解释读一遍。",
        "synthesis": "这段程序不报错却少算一天；先自己算，再数圈数，再定位到条件那一行。",
        "posttest": "自动售货机、体温登记表、改了三次才对的程序，看看你还能不能用上同一套办法。",
        "summary": "三句话：报错读三件事、两种错误怎么分、调试是一个圈。",
        "homework": "三层小任务，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学信息科技「算法与程序」在分支循环之后的收口课。五年级学生的两个真实困难是：看到报错就想整段重写，以及以为「程序跑完没报错就是对的」。所以全课围绕一个可反复操作的调试台展开。动手一只练「读报错」：报错信息里放三块可点的线索卡，每点一块，程序里对应的那一行就会亮起来并告诉你这句话在说什么，最后让学生判断真正要改的是哪一行——把「出事的位置」和「要改的位置」分开看。动手二是核心模拟，两个关卡：第一关名字写错（报错能给出行号），第二关「次数 = 次数 + 1」被放到循环外面导致停不下来（报错只说症状）；两关都是「点出错的那一行 → 即时给错因 → 点修正 → 重新运行，一行一行跑通并输出正确结果」。综合任务换成看不见的错：一段跑得通却少算一天的程序，学生先点「我自己先算一遍」得到 400，再单步看它只转了两圈，然后定位到条件那一行改成「小于等于」，重跑得到 400；最后用一个迭代问题收口——要统计五天只需改那个控制天数的数，改动越小越容易验。概念页把结论收成两句口诀，例题页示范「自己先算一遍」的四步查错法。全课收口到一条可带走的习惯：改一次、跑一次，改完一定要重新运行验证。",
    "plan_table": """| 1 | cover | 程序调试与迭代 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预设答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：程序出错的时候，你会怎么做？ | 起·前测（暴露直觉） |
| 5 | concept | 报错信息不是坏消息：它在告诉你三件事 | 承·概念一（读报错三步 + 逐块拆解图） |
| 6 | interactive | 动手一：读一条报错信息，找出要改的那一行 | 承·报错解读（点线索卡 → 对应行亮起 → 判断改哪行） |
| 7 | concept | 两种错误与调试循环：跑得通不等于算得对 | 承·概念二（看得见/看不见 + 调试循环圈） |
| 8 | interactive | 动手二：点出问题行，改好，再跑一遍 | 承·核心模拟（点选问题行 → 错因 → 修正 → 重跑通过，两关） |
| 9 | concept | 例题示范：跑得通但算错了，怎么查？ | 转·重难点突破（自己先算一遍四步法） |
| 10 | quiz | 概念测试：三种说法，错在哪里 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：不报错、但结果不对的一段程序 | 合·迁移应用（手工验算 + 边界 bug 定位 + 修正重跑 + 迭代提问） |
| 12 | quiz | 后测：换几个情境，办法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把调试讲清楚 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：读懂报错 / 找到那一行 / 改好再跑一遍 三栏\n- P5 报错信息拆解示意图（已生成）：一条报错拆成位置、症状、线索三块\n- P7 调试循环示意图（已生成）：运行→发现问题→定位→改好→再运行 的循环圈\n- 三张图均为教学示意图，不出现任何真实软件界面、截图或商标\n- 若需补充：学生手写的「出错记录」卡片（需获得授权后使用）",
}
