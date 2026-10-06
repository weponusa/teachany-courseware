# -*- coding: utf-8 -*-
"""小学信息科技 · 分支与循环结构（G5）—— 补齐知识树「算法与程序」空缺

学科语气：信息科技 = 概念 + 动手并重。
本课只做三件真能上手的事：
  ① 核心模拟 A（分支）：选一个分数当输入 → 一行一行点着走 → 高亮当前行 + 条件判真假 +
     输出哪一条路，并让学生亲眼看到 59 和 60 只差一分却走完全不同的路（边界陷阱）
  ② 核心模拟 B（循环）：改「起始值 / 比较符 / 上界」三个开关 → 单步走 →
     高亮当前行 + 变量表实时变化 + 累计循环次数；把 ≤ 改成 < 就少跑一圈，
     起始值从 1 改成 0 就多跑一圈（边界值多跑一次）
  ③ 综合任务：循环里套分支，数出及格人数；把 ≥ 改成 > 再看一次（边界值算不算）

说明：课件中的伪代码、程序行与运行面板均为教学示意图，不涉及任何真实软件界面、截图或商标。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-e-branch-loop-fig1.webp'
F2 = './assets/it-e-branch-loop-fig2.webp'

TTS = {
    "hero": "先请你想象一件事。妈妈让你写一张便条：如果明天下雨，就带伞；否则，就戴帽子。你写下的这句话，里面其实藏着程序里最重要的一种结构。程序不是只会从上往下一行行做，它还会根据条件挑一条路走，也会照着同一个条件把一件事做上好几遍。今天这节课，我们要把这两种结构拆开来看清楚：一种叫分支，一种叫循环；还要亲手点着走一遍，看看程序到底走了哪条路、转了几圈。",
    "problem-anchor": "开始之前，先选一个你最想弄明白的问题。是想知道程序怎么根据条件挑一条路走，还是想知道循环为什么能一遍一遍重复做同一件事，又或者你想弄明白为什么改成小于号就少跑了一圈，再或者你想学会在程序绕个不停的时候找出原因。选好了，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出分支就是一问两路：条件成立走一条，不成立走另一条，两条路只走一条。第二，能说出循环是三件事：从哪儿开始、什么时候停、每转一圈怎么变。第三，能在伪代码里一行一行看程序怎么走，说出每一步变量的值，并数出循环一共转了几圈。第四，能发现把小于等于改成小于、或者把起始值从一改成零，结果就会差一次，并能说出差在哪里。",
    "pretest": "先做三道小题，用你现在的想法选就行。选完马上能看到解释，选错了也没关系，正好知道该重点听哪里。",
    "module-1": "先看分支。生活里我们常常要按条件做决定：如果下雨就带伞，否则就戴帽子。写进程序里就是一句话：如果条件成立，做这一件事；否则，做另一件事。要记住三点。第一，条件必须是一句能判真假的话，比如分数大于或等于六十——这句话要么成立，要么不成立，没有第三种。第二，成立走「则」那一条，不成立走「否则」那一条。第三，两条路只会走一条，绝不会都走，也不会都不走。还有一点特别要紧：分界线上的那个数常常最会骗人，五十九和六十只差一分，走的路却完全不同。",
    "lab-1": "光看还不够，我们自己动手走一遍。下面是一段判断分数是否及格的伪代码。请你先选一个分数，再点单步执行，一行一行看着程序往下走。走到判断那一行，程序会告诉你条件成立不成立；亮起来的那一行，就是它正在做的那一步。请你特别试一下五十九分和六十分：只差一分，程序走的路完全不一样。",
    "module-2": "接下来看循环。循环就是把同一件事一遍一遍做，直到条件不再成立。写循环要想清楚三件事：第一，循环变量从哪儿开始；第二，什么时候停，也就是那个条件；第三，每转一圈它怎么变。第三件事最容易被忘掉——如果每圈都不变，条件永远成立，程序就会一直转下去，停不下来。另外，停下来那一刻的审查最要紧：用小于等于三，循环转三圈；改成小于三，就只转两圈；起始值从一改成零，又会多转一圈。一个符号、一个数，差的就是一整圈。",
    "lab-2": "现在请你当一次程序执行器。下面这段循环程序，它的起始值、比较符和上界都可以改。请你点单步执行，一次一行，看着变量表里的总数和次数跟着变；右边的循环圈数会一圈一圈累加。改一改那三个开关，再走一遍，看看循环圈数会怎么变。",
    "worked-example": "我们一起来读一段循环里套着分支的程序。第一步，先把程序里会变的量都列出来：及格人数和次数。第二步，一圈一圈地走：先看循环条件成立不成立，成立才进圈里。第三步，进了圈里再看分支：这个成绩够不够六十，够就加一，不够就不加，两条路只走一条。第四步，走完一圈别忘了做最后那件事——把次数加一，不然就出不来了。走完四圈，把每一步的及格人数连起来看：零、一、一、二，最后一个数就是答案。",
    "conceptest-1": "接下来用三个容易弄错的说法考考你。请仔细读每一个选项，选完再看解释。",
    "synthesis": "最后一个任务交给你。这段程序要做两件事叠在一起：一边数圈，一边在每一圈里判断这个成绩够不够六十。请你点单步执行，一行一行走完，看及格人数怎么从零变成三。走完以后，把判断里的「大于或等于」改成「大于」，再重新走一遍——你会发现六十分那个同学从及格变成了不及格。想一想，为什么会少一个人。",
    "posttest": "最后一轮，换几个新情境来考考你。这次会出现体温报警、跳绳计数、还有一段总是多跑一圈的程序，看看你能不能把学到的规则用上去。",
    "summary": "这节课我们记住三句话。第一句，分支是一问两路：条件成立走一条，不成立走另一条，两条路只走一条。第二句，循环要三件事：从哪儿开始、什么时候停、每圈怎么变；少一件就会转不停。第三句，分界线上的数最会骗人——小于等于和小于差一圈，起始值一和零差一圈，看到结果差一点，先去检查那个符号和那个数。回到开头那张便条：下雨带伞、否则戴帽子，是分支；每天看一眼天气预报，就是循环。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出一句生活中的如果否则，再写出一件每天重复做、并且知道什么时候停的事，把循环的三件事标出来。第二层能力应用，动手做：给一段循环程序，先在纸上走一遍、写出每一圈里变量的值，再上机运行验证。第三层迁移挑战，选做：设计一个需要循环里套分支的任务，写清条件，并说明你为什么要用小于等于而不是小于。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是学它之前要先会的，右边是学会之后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续学的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 分支：一问两路", "lab-1": "动手一 一行一行走一遍分支",
    "module-2": "概念二 循环：三件事与边界", "lab-2": "动手二 改开关看循环转几圈",
    "worked-example": "例题讲解 循环里套分支", "conceptest-1": "概念测试",
    "synthesis": "综合任务 数出及格人数", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

CUSTOM_JS = r"""
/* ============================================================
   it-e-branch-loop 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) blRunner()：伪代码执行器工厂
      —— 高亮当前行、变量面板实时变化、累计循环圈数
   3) 动手一：分支执行器（选分数 → 单步 → 条件判真假 → 输出哪条路）
   4) 动手二：循环执行器（起始值/比较符/上界三开关 → 累计循环圈数）
   5) 综合任务：循环里套分支，数出及格人数（含 ≥ 改成 > 的边界对比）
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
    '.bl-wrap{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(230px,0.9fr);gap:14px;align-items:start;}' +
    '@media(max-width:760px){.bl-wrap{grid-template-columns:1fr;}}' +
    '.bl-code{display:flex;flex-direction:column;gap:4px;padding:10px;border-radius:12px;' +
    'background:var(--bg-subtle);border:1px solid var(--line-subtle);}' +
    '.bl-line{display:flex;align-items:flex-start;gap:9px;padding:7px 10px;border-radius:8px;' +
    'background:var(--card);border:1px solid transparent;font-size:14px;' +
    'font-family:ui-monospace,SFMono-Regular,Menlo,monospace;transition:all .2s ease;}' +
    '.bl-line .bl-n{flex-shrink:0;width:20px;height:20px;border-radius:5px;display:grid;place-items:center;' +
    'background:rgb(var(--paper-rgb) / 20%);color:var(--muted);font-size:11px;font-weight:800;}' +
    '.bl-line .bl-c{flex:1;min-width:0;word-break:break-word;}' +
    '.bl-line.run{border-color:var(--brand);background:var(--brand-soft);' +
    'box-shadow:0 0 0 3px rgb(var(--brand-rgb) / 16%);}' +
    '.bl-line.run .bl-n{background:var(--brand);color:#fff;}' +
    '.bl-line.fixed{border-color:var(--brand-2);background:var(--accent-soft);}' +
    '.bl-side{display:flex;flex-direction:column;gap:10px;}' +
    '.bl-pick{text-align:center;font-weight:700;}' +
    '.bl-pick.on{border-color:var(--brand);background:var(--brand-soft);box-shadow:0 0 0 3px rgb(var(--brand-rgb) / 16%);}' +
    '.bl-ctl{display:flex;align-items:center;gap:8px;flex-wrap:wrap;}' +
    '.bl-ctl label{font-size:13px;font-weight:700;min-width:62px;}' +
    '.bl-ctl select{flex:1;min-width:78px;border-radius:10px;border:1px solid var(--line);' +
    'background:var(--card);color:var(--text);padding:8px 10px;font-size:14px;font-weight:700;}' +
    '.bl-loopbar{display:flex;gap:5px;flex-wrap:wrap;margin-top:4px;}' +
    '.bl-dot{width:22px;height:22px;border-radius:50%;display:grid;place-items:center;font-size:11px;' +
    'font-weight:800;background:rgb(var(--paper-rgb) / 18%);color:var(--muted);border:1px solid var(--line-subtle);}' +
    '.bl-dot.on{background:var(--brand-2);color:#fff;border-color:var(--brand-2);}' +
    '.bl-read{padding:10px 12px;border-radius:12px;background:var(--bg-subtle);' +
    'border:1px solid var(--line-subtle);font-size:14px;line-height:1.7;}' +
    '.bl-read b{color:var(--link);}' +
    '.choice{border:1.5px solid rgb(var(--brand-rgb) / 32%);background:var(--card);}' +
    '.choice:hover{background:var(--brand-soft);border-color:rgb(var(--brand-rgb) / 55%);}' +
    '.choice.selected{border-color:var(--brand);background:rgb(var(--brand-rgb) / 13%);}' +
    '.kid-note{border-color:rgb(var(--warm-rgb) / 80%);}';
  document.head.appendChild(st);

  /* ---------- 2. 伪代码执行器工厂 ---------- */
  function blRunner(cfg) {
    var codeEl = document.getElementById(cfg.codeId);
    var outEl = document.getElementById(cfg.outId);
    if (!codeEl || !outEl) return null;
    var st = { trace: [], i: -1, timer: null };

    function lines() { return typeof cfg.lines === 'function' ? cfg.lines() : cfg.lines; }

    function paint() {
      var cur = (st.i >= 0 && st.i < st.trace.length) ? st.trace[st.i] : null;
      var ls = lines();
      codeEl.innerHTML = '';
      ls.forEach(function (txt, k) {
        var row = document.createElement('div');
        row.className = 'bl-line' + (cur && cur.line === k + 1 ? ' run' : '') +
          (cfg.fixedLines && cfg.fixedLines.indexOf(k + 1) >= 0 ? ' fixed' : '');
        var n = document.createElement('span');
        n.className = 'bl-n';
        n.textContent = (k + 1);
        var c = document.createElement('span');
        c.className = 'bl-c';
        c.textContent = txt;
        row.appendChild(n);
        row.appendChild(c);
        codeEl.appendChild(row);
      });
      if (cur && cfg.onStep) cfg.onStep(cur, st.i);
      else if (cfg.onIdle) cfg.onIdle();
    }

    function rebuild() { st.trace = cfg.build(); st.i = -1; paint(); }
    function stop() { if (st.timer !== null) { clearInterval(st.timer); st.timer = null; } }
    function last() { return st.i >= st.trace.length - 1; }

    function advance() {
      if (last()) return false;
      st.i++;
      paint();
      return !last();
    }

    function runAll() {
      stop();
      rebuild();
      outEl.className = 'result warn';
      outEl.textContent = '正在一行一行执行……亮起来的那一行，就是程序正在做的这一步。';
      st.timer = setInterval(function () {
        if (!advance()) { stop(); if (cfg.onDone) cfg.onDone(); }
      }, 640);
    }

    function stepOnce() {
      if (st.timer !== null) return;
      if (st.trace.length === 0) rebuild();
      if (last()) { if (cfg.onDone) cfg.onDone(); return; }
      advance();
      if (last() && cfg.onDone) cfg.onDone();
    }

    return {
      reset: function () { stop(); rebuild(); },
      step: stepOnce,
      run: runAll,
      refresh: function () { stop(); rebuild(); },
      stop: stop
    };
  }

  /* ---------- 3. 动手一：分支执行器 ---------- */
  (function () {
    var CODE1 = [
      '输入 分数',
      '如果 分数 >= 60 则',
      '    说「及格了，继续加油」',
      '否则',
      '    说「还没到 60，再练一练」',
      '结束'
    ];
    var out1 = document.getElementById('bl1-out');
    if (!out1) return;
    var elScore = document.getElementById('bl1-score');
    var elCond = document.getElementById('bl1-cond');
    var elLines = document.getElementById('bl1-lines');
    var score1 = 60;

    function trace1() {
      var s = score1, ok = s >= 60, t = [];
      t.push({ line: 1, v: { '分数': s }, cond: '—',
        note: '把选好的数据放进来，起名叫「分数」：分数 = ' + s + '。' });
      t.push({ line: 2, v: { '分数': s }, cond: ok ? '真' : '假',
        note: '检查条件：' + s + ' >= 60 吗？——' + (ok ? '成立，走「则」这条路。' : '不成立，走「否则」这条路。') });
      if (ok) {
        t.push({ line: 3, v: { '分数': s }, cond: '真', note: '说了「及格了，继续加油」。' });
      } else {
        t.push({ line: 5, v: { '分数': s }, cond: '假', note: '说了「还没到 60，再练一练」。' });
      }
      t.push({ line: 6, v: { '分数': s }, cond: '—',
        note: '程序结束。整段只走了' + (ok ? '「则」' : '「否则」') + '这一条路——两条路不会都走。' });
      return t;
    }

    var r1 = blRunner({
      codeId: 'bl1-code', outId: 'bl1-out', lines: CODE1, build: trace1,
      onStep: function (s, i) {
        elCond.textContent = s.cond;
        elLines.textContent = (i + 1) + ' 行';
      },
      onIdle: function () { elCond.textContent = '—'; elLines.textContent = '0 行'; },
      onDone: function () {
        var ok = score1 >= 60;
        out1.className = 'result ' + (ok ? '' : 'warn');
        out1.innerHTML = '<strong>走完了：分数 ' + score1 + '，走了' + (ok ? '「则」' : '「否则」') +
          '这一条路。</strong>输出是「' + (ok ? '及格了，继续加油' : '还没到 60，再练一练') + '」。<br>' +
          '<span style="color:var(--muted)">再看一眼条件：' + score1 + ' >= 60 —— ' + (ok ? '成立' : '不成立') +
          '。条件里的符号决定了走哪条路；' +
          (score1 === 59 || score1 === 60
            ? '59 和 60 只差一分，走的路却完全不同——分界线上的数一定要单独试一次。'
            : '换成 59 分或 60 分再走一遍，看看差别在哪里。') + '</span>';
      }
    });
    if (!r1) return;

    document.querySelectorAll('[data-bl1-score]').forEach(function (b) {
      b.addEventListener('click', function () {
        document.querySelectorAll('[data-bl1-score]').forEach(function (x) { x.classList.remove('on'); });
        b.classList.add('on');
        score1 = parseInt(b.dataset.bl1Score, 10);
        elScore.textContent = score1 + ' 分';
        r1.refresh();
        out1.className = 'result warn';
        out1.textContent = '已经换成 ' + score1 + ' 分了。点「单步执行」，一行一行看它走哪条路。';
      });
    });
    document.getElementById('bl1-step').addEventListener('click', function () { r1.step(); });
    document.getElementById('bl1-run').addEventListener('click', function () { r1.run(); });
    document.getElementById('bl1-reset').addEventListener('click', function () {
      r1.reset();
      out1.className = 'result warn';
      out1.textContent = '回到开头了。再点「单步执行」走一遍。';
    });

    elScore.textContent = '60 分';
    document.querySelector('[data-bl1-score="60"]').classList.add('on');
    r1.reset();
  })();

  /* ---------- 4. 动手二：循环执行器（累计循环圈数） ---------- */
  (function () {
    var out2 = document.getElementById('bl2-out');
    if (!out2) return;
    var selStart = document.getElementById('bl2-start');
    var selOp = document.getElementById('bl2-op');
    var selBound = document.getElementById('bl2-bound');
    var elTotal = document.getElementById('bl2-total');
    var elK = document.getElementById('bl2-k');
    var elLoops = document.getElementById('bl2-loops');
    var elDots = document.getElementById('bl2-dots');
    var cache2 = null;

    function st2() { return parseInt(selStart.value, 10); }
    function bd2() { return parseInt(selBound.value, 10); }
    function sym2() { return selOp.value === 'le' ? '<=' : '<'; }
    function cmp2(v) { return selOp.value === 'le' ? v <= bd2() : v < bd2(); }

    function lines2() {
      return [
        '总数 = 0',
        '次数 = ' + st2(),
        '当 次数 ' + sym2() + ' ' + bd2() + ' 时',
        '    总数 = 总数 + 2',
        '    次数 = 次数 + 1',
        '结束（回到第 3 行）',
        '输出 总数'
      ];
    }

    function build2() {
      var total = 0, k = st2(), loops = 0, guard = 0, t = [];
      function V() { return { '总数': total, '次数': k, '圈数': loops }; }
      t.push({ line: 1, v: V(), note: '先把总数设成 0，准备开始累加。' });
      t.push({ line: 2, v: V(), note: '次数从 ' + st2() + ' 开始数。' });
      while (cmp2(k) && guard++ < 20) {
        loops++;
        t.push({ line: 3, v: V(), cond: '真',
          note: '检查：次数 ' + k + ' ' + sym2() + ' ' + bd2() + ' 成立 —— 进圈里，这是第 ' + loops + ' 圈。' });
        total = total + 2;
        t.push({ line: 4, v: V(), note: '总数加上 2，变成 ' + total + '。' });
        k = k + 1;
        t.push({ line: 5, v: V(), note: '次数加 1，变成 ' + k + '。' });
      }
      t.push({ line: 3, v: V(), cond: '假',
        note: '检查：次数 ' + k + ' ' + sym2() + ' ' + bd2() + ' 不成立 —— 走出循环，一共转了 ' + loops + ' 圈。' });
      t.push({ line: 7, v: V(), cond: '—', note: '输出结果：总数 = ' + total + '。' });
      cache2 = { total: total, loops: loops };
      return t;
    }

    function dots(n) {
      elDots.innerHTML = '';
      for (var i = 1; i <= Math.max(n, 1); i++) {
        var d = document.createElement('span');
        d.className = 'bl-dot' + (i <= n ? ' on' : '');
        d.textContent = i;
        elDots.appendChild(d);
      }
    }

    var r2 = blRunner({
      codeId: 'bl2-code', outId: 'bl2-out', lines: lines2, build: build2,
      onStep: function (s) {
        elTotal.textContent = s.v['总数'];
        elK.textContent = s.v['次数'];
        elLoops.textContent = s.v['圈数'];
        dots(s.v['圈数']);
      },
      onIdle: function () {
        elTotal.textContent = '0';
        elK.textContent = st2();
        elLoops.textContent = '0';
        dots(0);
      },
      onDone: function () {
        var tip = '边界提醒：条件写「<= 上界」时，圈数 = 上界 − 起始值 + 1。' +
          '把「<=」改成「<」就少一圈；把起始值从 1 改成 0 就多一圈。';
        if (selOp.value === 'lt') {
          tip = '你刚把「小于等于」改成了「小于」，所以圈数正好少了一圈——常见错误就是把这两个符号当成一回事。' + tip;
        } else if (selStart.value === '0') {
          tip = '你把起始值从 1 改成了 0，所以圈数多了一圈——起始值和上界一起决定了要转几次。' + tip;
        }
        out2.className = 'result warn';
        out2.innerHTML = '<strong>这一遍：条件「次数 ' + sym2() + ' ' + bd2() + '」，起始值 ' + st2() +
          '，循环一共转了 ' + cache2.loops + ' 圈，最后总数是 ' + cache2.total + '。</strong><br>' +
          '<span style="color:var(--muted)">' + tip + '</span>';
      }
    });
    if (!r2) return;

    [selStart, selOp, selBound].forEach(function (el) {
      el.addEventListener('change', function () {
        r2.refresh();
        out2.className = 'result warn';
        out2.textContent = '参数换好了（条件：次数 ' + sym2() + ' ' + bd2() + '，起始值 ' + st2() +
          '）。点「单步执行」走一遍，看循环圈数怎么变。';
      });
    });
    document.getElementById('bl2-step').addEventListener('click', function () { r2.step(); });
    document.getElementById('bl2-run').addEventListener('click', function () { r2.run(); });
    document.getElementById('bl2-reset').addEventListener('click', function () {
      r2.reset();
      out2.className = 'result warn';
      out2.textContent = '回到开头了。再点「单步执行」走一遍。';
    });
    r2.reset();
  })();

  /* ---------- 5. 综合任务：循环里套分支，数出及格人数 ---------- */
  (function () {
    var out3 = document.getElementById('bl3-out');
    if (!out3) return;
    var SC = [72, 45, 88, 60];
    var selOp3 = document.getElementById('bl3-op');
    var elPass = document.getElementById('bl3-pass');
    var elK3 = document.getElementById('bl3-k');
    var elLoops3 = document.getElementById('bl3-loops');
    var elDots3 = document.getElementById('bl3-dots');
    var elRead = document.getElementById('bl3-read');
    var cache3 = null;

    function sym3() { return selOp3.value === 'ge' ? '>=' : '>'; }
    function cmp3(sc) { return selOp3.value === 'ge' ? sc >= 60 : sc > 60; }

    function lines3() {
      return [
        '及格人数 = 0',
        '次数 = 1',
        '当 次数 <= 4 时',
        '    如果 成绩[次数] ' + sym3() + ' 60 则',
        '        及格人数 = 及格人数 + 1',
        '    否则',
        '        说「第 次数 个还没到 60」',
        '    结束（分支）',
        '    次数 = 次数 + 1',
        '结束（循环，回到第 3 行）',
        '输出 及格人数'
      ];
    }

    function build3() {
      var pass = 0, k = 1, loops = 0, t = [];
      function V(sc) { return { '及格人数': pass, '次数': k, '圈数': loops, '成绩': sc === undefined ? '—' : sc }; }
      t.push({ line: 1, v: V(), note: '先把及格人数设成 0。' });
      t.push({ line: 2, v: V(), note: '次数从 1 开始。' });
      while (k <= 4 && loops < 10) {
        loops++;
        var sc = SC[k - 1];
        t.push({ line: 3, v: V(), cond: '真',
          note: '第 ' + loops + ' 圈：次数 ' + k + ' <= 4 成立，进圈里。' });
        var hit = cmp3(sc);
        t.push({ line: 4, v: V(sc), cond: hit ? '真' : '假',
          note: '看第 ' + k + ' 个成绩：' + sc + ' ' + sym3() + ' 60 吗？——' + (hit ? '成立。' : '不成立。') });
        if (hit) {
          pass = pass + 1;
          t.push({ line: 5, v: V(sc), note: '及格人数加 1，变成 ' + pass + '。' });
        } else {
          t.push({ line: 7, v: V(sc), note: '说一句「第 ' + k + ' 个还没到 60」，这一圈不加。' });
        }
        t.push({ line: 8, v: V(sc), note: '分支结束——两条路只走了一条。' });
        k = k + 1;
        t.push({ line: 9, v: V(), note: '次数加 1，变成 ' + k + '，准备下一圈。' });
      }
      t.push({ line: 3, v: V(), cond: '假',
        note: '次数 ' + k + ' <= 4 不成立 —— 走出循环，一共转了 ' + loops + ' 圈。' });
      t.push({ line: 11, v: V(), cond: '—', note: '输出结果：及格人数 = ' + pass + '。' });
      cache3 = { pass: pass, loops: loops };
      return t;
    }

    function dots3(n) {
      elDots3.innerHTML = '';
      for (var i = 1; i <= Math.max(n, 1); i++) {
        var d = document.createElement('span');
        d.className = 'bl-dot' + (i <= n ? ' on' : '');
        d.textContent = i;
        elDots3.appendChild(d);
      }
    }

    var r3 = blRunner({
      codeId: 'bl3-code', outId: 'bl3-out', lines: lines3, build: build3,
      onStep: function (s, i) {
        elPass.textContent = s.v['及格人数'];
        elK3.textContent = s.v['次数'];
        elLoops3.textContent = s.v['圈数'];
        dots3(s.v['圈数']);
        var extra = (s.v['成绩'] === '—') ? '' : '　（正在看第 ' + s.v['次数'] + ' 个成绩：' + s.v['成绩'] + '）';
        elRead.textContent = '第 ' + (i + 1) + ' 步：' + s.note + extra;
      },
      onIdle: function () {
        elPass.textContent = '0';
        elK3.textContent = '1';
        elLoops3.textContent = '0';
        dots3(0);
        elRead.textContent = '每走完一圈，这里会告诉你圈里判断的结果。';
      },
      onDone: function () {
        var ge = selOp3.value === 'ge';
        out3.className = ge ? 'result' : 'result warn';
        out3.innerHTML = '<strong>走完了：一共转了 ' + cache3.loops + ' 圈，及格人数是 ' +
          cache3.pass + ' 人。</strong><br>' +
          '<span style="color:var(--muted)">' + (ge
            ? '注意最后那个 60 分：条件是 >= 60，正好等于也算及格，所以它被数进去了。把上面的比较符改成「大于 >」，再走一遍看看。'
            : '你把 >= 改成了 >，60 分那位同学就不算及格了，所以正好少一个人。分界线上的数就是这样：一个符号，差一个人。')
          + '</span>';
      }
    });
    if (!r3) return;

    selOp3.addEventListener('change', function () {
      r3.refresh();
      out3.className = 'result warn';
      out3.textContent = '比较符换成「' + sym3() + ' 60」了。点「单步执行」重走一遍，看及格人数变成几。';
    });
    document.getElementById('bl3-step').addEventListener('click', function () { r3.step(); });
    document.getElementById('bl3-run').addEventListener('click', function () { r3.run(); });
    document.getElementById('bl3-reset').addEventListener('click', function () {
      r3.reset();
      out3.className = 'result warn';
      out3.textContent = '回到开头了。再点「单步执行」走一遍。';
    });
    r3.reset();
  })();
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：程序会怎么挑路、怎么转圈？", TTS["pretest"], [
        {"q": "程序里的「如果……则……否则……」，最后的执行方式是：",
         "options": [("条件成立走「则」那条，不成立走「否则」那条，两条只走一条", True),
                     ("两条路都走一遍", False),
                     ("两条路都不走，等别人告诉它选哪条", False)],
         "explain": "分支的本质就是一问两路，条件决定走哪一条，而且只走一条。"
                    "<strong>错因提醒：</strong>常见错误是以为「否则」也要做一遍——"
                    "其实它只是备用的那条路，条件成立时根本不会碰到它。"},
        {"q": "写一个循环，下面哪一件事不做，程序就会一直转下去停不下来？",
         "options": [("每转一圈，让控制循环的那个量变化一下", True),
                     ("给循环起一个好听的名字", False),
                     ("把循环里的动作写得再详细一点", False)],
         "explain": "循环变量不变化，条件就永远成立，程序就出不来了。"
                    "<strong>错因提醒：</strong>不少同学误认为循环只要写上「重复」两个字就够了——"
                    "「什么时候停」和「每圈怎么变」才是关键。"},
        {"q": "循环条件是「次数 ≤ 3」，次数从 1 开始。这个循环会转几圈？",
         "options": [("3 圈", True), ("2 圈", False), ("4 圈", False)],
         "explain": "次数依次是 1、2、3 时条件都成立，一共转 3 圈；到 4 才停下来。"
                    "<strong>错因提醒：</strong>容易把「小于等于」当成「小于」来数，少算一圈；"
                    "也容易把从 0 开始当成从 1 开始，多算一圈。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "分支：一问两路，只走一条", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">前面我们已经会让程序一行一行按顺序做事了（And）；可生活里的事常常要看情况——下雨才带伞，成绩够了才算及格，一句话说不清楚（But）；所以程序里要有一种会「自己挑路」的结构，那就是分支（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">分支就是<strong>一问两路</strong>：先问一句能判真假的话，成立走一条，不成立走另一条。</p>
        <div class="grid grid-3">
          <div class="inner-card"><p><strong>① 条件能判真假</strong></p><p style="color:var(--muted)">「分数 ≥ 60」这种话，要么成立，要么不成立，没有第三种。</p></div>
          <div class="inner-card"><p><strong>② 成立走「则」</strong></p><p style="color:var(--muted)">条件成立，就做「则」下面那件事，做完跳出去。</p></div>
          <div class="inner-card"><p><strong>③ 两条只走一条</strong></p><p style="color:var(--muted)">「否则」是备用路：成立时根本不碰它，不成立时才走。</p></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="分支结构示意图：一个条件判断分成上下两条路，成立走上面一条，不成立走下面一条，两条路只走一条">
          <figcaption>示意图：一句话问出两条路——条件成立走上面那条，不成立走下面那条；两条路永远不会同时走</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">把条件的<strong>方向写反</strong>：本来想说「分数不够就再练一练」，却写成「分数 ≥ 60 则再练一练」。条件本身没错，但它代表的意思反了。写完条件，一定要问自己一句：<strong>这句话成立的时候，我希望它做什么？</strong></p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>一句话问真假，两条路只走一头；分界线上那一个数，最会把人骗回头。</div></div>
{insight_box([
    {"lens": "看见它", "text": "分支的样子就是岔路口的两块路牌。程序走到这里会停下来问一句，然后只往一个方向去。"},
    {"lens": "解释它", "text": "为什么一定要「只走一条」？因为两条路做的事常常是互相矛盾的——既说及格又说没及格，那就乱套了。"},
    {"lens": "迁移它", "text": "生活的规则大多是这个形状：如果体温超过三十七度三就报告老师，否则正常上课。看懂了形状，规则就好读了。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：一行一行走一遍这段分支", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先选一个分数当输入，再点「单步执行」，一行一行看程序走。走到判断那一行，它会告诉你条件成立不成立。</p>
        <div class="lab-panel">
          <div class="bl-wrap">
            <div>
              <div style="font-weight:700;font-size:14px;margin-bottom:6px">程序（伪代码）</div>
              <div class="bl-code" id="bl1-code"></div>
              <div class="flex-row" style="margin-top:10px">
                <button class="choice" id="bl1-run" style="text-align:center">▶ 一次跑完</button>
                <button class="choice" id="bl1-step" style="text-align:center">单步执行</button>
                <button class="choice" id="bl1-reset" style="text-align:center">回到开头</button>
              </div>
            </div>
            <div class="bl-side">
              <div style="font-weight:700;font-size:14px">① 选一个分数（这就是「输入数据」）</div>
              <div class="flex-row" style="margin-top:0">
                <button class="choice bl-pick" data-bl1-score="59">59 分</button>
                <button class="choice bl-pick" data-bl1-score="60">60 分</button>
                <button class="choice bl-pick" data-bl1-score="88">88 分</button>
              </div>
              <div class="lab-readout">
                <div class="readout-cell"><span class="k">分数</span><span class="v" id="bl1-score">—</span></div>
                <div class="readout-cell"><span class="k">条件真假</span><span class="v green" id="bl1-cond">—</span></div>
                <div class="readout-cell"><span class="k">已走行数</span><span class="v" id="bl1-lines">0 行</span></div>
              </div>
            </div>
          </div>
          <p class="result warn" id="bl1-out" style="margin-top:12px">先选一个分数，再点「单步执行」，看程序走哪一条路。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>看仔细：</strong>换成 59 分再走一遍，你会发现程序走的路完全不一样。分界线上的两个数只差一分，结果却差一整条路——这就是条件写「≥」还是写「&gt;」时最要小心的地方。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "循环：三件事想清楚，还要盯住分界线", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">循环就是<strong>条件还成立，就再转一圈</strong>。写循环必须想清楚三件事，缺一件就会转不停。</p>
        <div class="step-grid">
          <div class="step"><span class="n">始</span><div><strong>从哪儿开始：</strong>循环变量第一次取什么值。从 0 开始还是从 1 开始，最后的结果会差一次。</div></div>
          <div class="step"><span class="n">停</span><div><strong>什么时候停：</strong>条件写成小于等于还是小于，直接决定它转几圈。</div></div>
          <div class="step"><span class="n green">变</span><div><strong>每圈怎么变：</strong>每转一圈，循环变量必须变一下。忘了这一件，条件永远成立，就出不来了。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="循环结构示意图：判断条件成立就回到上面再转一圈并累计圈数，条件不成立才向下走出循环">
          <figcaption>示意图：条件成立就绕着圈再走一遍，每转一圈计数器加一；条件不成立才往下走出循环</figcaption>
        </figure>
        <div class="inner-card">
          <p><strong>分界线上的三个数，最容易骗人：</strong></p>
          <p style="color:var(--muted)">① 条件写「次数 ≤ 3」转 3 圈，写「次数 &lt; 3」只转 2 圈——差一个符号，少一整圈。<br>② 起始值从 1 改成 0，同一个条件就会<strong>多转一圈</strong>。<br>③ 所以程序结果比预期差一点时，先回去看那个符号和那个起始值。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">以为「条件不成立」就是出错。其实条件不成立只是<strong>该停了</strong>——它不是失败，而是循环正常的出口。真正的问题是条件<strong>永远成立</strong>：那才会让程序绕个不停。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>从哪儿开始、何时停、每圈怎么变；小于等于和小于，差的就是一整圈。</div></div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：改三个开关，看循环转几圈", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">下面是一段循环程序。起始值、比较符、上界都可以改。点「单步执行」，一次一行，看变量表怎么变、循环圈数怎么累加。</p>
        <div class="lab-panel">
          <div class="bl-wrap">
            <div>
              <div style="font-weight:700;font-size:14px;margin-bottom:6px">程序（伪代码）</div>
              <div class="bl-code" id="bl2-code"></div>
              <div class="flex-row" style="margin-top:10px">
                <button class="choice" id="bl2-run" style="text-align:center">▶ 一次跑完</button>
                <button class="choice" id="bl2-step" style="text-align:center">单步执行</button>
                <button class="choice" id="bl2-reset" style="text-align:center">回到开头</button>
              </div>
            </div>
            <div class="bl-side">
              <div style="font-weight:700;font-size:14px">三个开关（改完请重新走一遍）</div>
              <div class="bl-ctl"><label for="bl2-start">起始值</label>
                <select id="bl2-start"><option value="1">次数 = 1</option><option value="0">次数 = 0</option></select></div>
              <div class="bl-ctl"><label for="bl2-op">比较符</label>
                <select id="bl2-op"><option value="le">小于等于 ≤</option><option value="lt">小于 &lt;</option></select></div>
              <div class="bl-ctl"><label for="bl2-bound">上界</label>
                <select id="bl2-bound"><option value="3">3</option><option value="4">4</option><option value="5">5</option></select></div>
              <div class="lab-readout">
                <div class="readout-cell"><span class="k">总数</span><span class="v" id="bl2-total">0</span></div>
                <div class="readout-cell"><span class="k">次数</span><span class="v" id="bl2-k">1</span></div>
                <div class="readout-cell"><span class="k">循环圈数</span><span class="v green" id="bl2-loops">0</span></div>
              </div>
              <div style="font-size:13px;color:var(--muted)">每一圈亮一个点：</div>
              <div class="bl-loopbar" id="bl2-dots"></div>
            </div>
          </div>
          <p class="result warn" id="bl2-out" style="margin-top:12px">先点「单步执行」，看它一圈一圈怎么走。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💡</span><div><strong>试一试：</strong>把「≤ 3」改成「&lt; 3」，再看圈数——少了一整圈！再把起始值从 1 改成 0，圈数又多了一圈。所以程序结果差一次的时候，先回来检查这个符号和这个起始值。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：读一段循环里套着分支的程序", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>成绩依次是 72、45、88、60，要数出及格（≥ 60）的人数。程序是：① 及格人数 = 0 ② 次数 = 1 ③ 当 次数 ≤ 4 时 ④ 如果 成绩[次数] ≥ 60 则 ⑤ 及格人数 = 及格人数 + 1 ⑥ 结束分支 ⑦ 次数 = 次数 + 1 ⑧ 结束循环 ⑨ 输出 及格人数。结果是多少？</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先列出会变的量：</strong>「及格人数」和「次数」两个。给它们各写一列，后面每走一步就把新值记上去。</div></div>
          <div class="step"><span class="n">2</span><div><strong>看循环条件：</strong>次数从 1 开始，≤ 4 成立，所以进圈里；一圈走完次数加一，变成 2，再回来问一次。</div></div>
          <div class="step"><span class="n">3</span><div><strong>圈里先判分支：</strong>72 够 60，及格人数加一；45 不够，这一圈不加。两条路只走一条。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>走完四圈再收尾：</strong>及格人数依次是 0、1、1、2、3——最后一个 3 就是答案，也就是有 3 个人及格。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">最容易忘的是<strong>第 ⑦ 步</strong>——把「次数 = 次数 + 1」忘在循环体外面，或者干脆漏掉。少了这一步，次数永远是 1，条件永远成立，程序就绕个不停。第二容易错的是把最后一个 60 分当成不及格：条件是「≥ 60」，60 正好算进去。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三种说法，错在哪里", TTS["conceptest-1"], [
        {"q": "「如果 分数 ≥ 60 则 说「及格」 否则 说「再练一练」」，当分数是 60 时，程序会：",
         "options": [("说「及格」——条件成立，只走「则」那一条", True),
                     ("两条都说一遍", False),
                     ("说「再练一练」，因为 60 不算过", False)],
         "explain": "≥ 的意思是「大于或等于」，60 正好等于 60，条件成立。"
                    "<strong>错因提醒：</strong>常见错误是把 ≥ 和 &gt; 搞混，以为必须超过才算——"
                    "分界线上的那个数永远要单独试一次。"},
        {"q": "循环条件是「当 次数 ≤ 5 时」，次数从 1 开始，每次加一。循环转几圈？",
         "options": [("5 圈", True), ("4 圈", False), ("6 圈", False)],
         "explain": "次数是 1、2、3、4、5 时都成立，共 5 圈；变成 6 时才停下来。"
                    "<strong>错因提醒：</strong>把 ≤ 当成 &lt; 就会少数一圈。数不清的时候，"
                    "把次数一个个写下来最稳。"},
        {"q": "写了一段循环，运行后程序一直没有停下来。最可能的原因是：",
         "options": [("圈里没有让循环变量变化，条件永远成立", True),
                     ("循环里的动作写得太复杂", False),
                     ("循环写得不够漂亮", False)],
         "explain": "循环必须有出口：条件迟早要不成立。让循环变量每圈变化，才能走到那一步。"
                    "<strong>错因提醒：</strong>别误认为「转不停」是电脑坏了——"
                    "先回去看那三件事，特别是「每圈怎么变」。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：一边数圈，一边数及格人数", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">这段程序把循环和分支叠在一起：一边数圈，一边在每一圈里判断这个成绩够不够 60。请点「单步执行」一行一行走完。</p>
        <div class="lab-panel">
          <div class="bl-wrap">
            <div>
              <div style="font-weight:700;font-size:14px;margin-bottom:6px">程序（伪代码）</div>
              <div class="bl-code" id="bl3-code"></div>
              <div class="flex-row" style="margin-top:10px">
                <button class="choice" id="bl3-run" style="text-align:center">▶ 一次跑完</button>
                <button class="choice" id="bl3-step" style="text-align:center">单步执行</button>
                <button class="choice" id="bl3-reset" style="text-align:center">回到开头</button>
              </div>
            </div>
            <div class="bl-side">
              <div style="font-weight:700;font-size:14px">判断里的比较符（改完请重新走一遍）</div>
              <div class="bl-ctl"><label for="bl3-op">成绩比较</label>
                <select id="bl3-op"><option value="ge">大于等于 ≥ 60</option><option value="gt">大于 &gt; 60</option></select></div>
              <div class="lab-readout">
                <div class="readout-cell"><span class="k">及格人数</span><span class="v" id="bl3-pass">0</span></div>
                <div class="readout-cell"><span class="k">次数</span><span class="v" id="bl3-k">1</span></div>
                <div class="readout-cell"><span class="k">循环圈数</span><span class="v green" id="bl3-loops">0</span></div>
              </div>
              <div style="font-size:13px;color:var(--muted)">成绩依次是 72、45、88、60</div>
              <div class="bl-loopbar" id="bl3-dots"></div>
              <div class="bl-read" id="bl3-read">每走完一圈，这里会告诉你圈里判断的结果。</div>
            </div>
          </div>
          <p class="result warn" id="bl3-out" style="margin-top:12px">先点「单步执行」，看及格人数怎么从 0 变成 3。</p>
        </div>
        <div class="inner-card">
          <p><strong>走完以后说给同桌听：</strong></p>
          <p style="color:var(--muted)">把「≥ 60」改成「&gt; 60」再走一遍，及格人数少了一个——少的那个是谁？为什么？如果把开始那句话改成「次数 = 0」，结果又会变成几个人？</p>
          <textarea id="syn-answer" rows="3" placeholder="少的是六十分那个同学，因为……如果次数从 0 开始，会……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个情境，规则还在不在", TTS["posttest"], [
        {"q": "体温报警程序写的是「如果 体温 ≥ 37.3 则 报警 否则 正常」。体温正好 37.3 度时会：",
         "options": [("报警——分界线上的数算在里面", True),
                     ("正常，要超过 37.3 才报警", False),
                     ("先报警再取消", False)],
         "explain": "≥ 包含等于，37.3 正好成立。"
                    "<strong>错因提醒：</strong>现实里这类边界特别要紧，规则写 ≥ 还是 &gt; 必须问清楚。"},
        {"q": "跳绳计数程序是「当 天数 ≤ 3 时 加一次个数」，如果改成「当 天数 &lt; 3 时」，会发生什么？",
         "options": [("少算一天，总数变少", True),
                     ("结果完全一样", False),
                     ("多算一天，总数变多", False)],
         "explain": "≤ 3 转 3 圈，&lt; 3 只转 2 圈，正好少一天。"
                    "<strong>错因提醒：</strong>常见错误是以为「小于」和「小于等于」差不多——它们差一整圈。"},
        {"q": "一段循环程序每次的结果都比答案多一次，你最该先检查的是：",
         "options": [("比较符是不是该用小于、以及循环变量的起始值", True),
                     ("把程序整段删掉重写", False),
                     ("把循环里的动作换一个顺序", False)],
         "explain": "多一次或少一次，几乎都出在分界线上：符号和起始值。"
                    "<strong>错因提醒：</strong>别急着重写——先动那一个符号、那一个数，"
                    "然后重新运行一次验证。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把分支和循环讲清楚", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>分支是一问两路：</strong>条件成立走「则」，不成立走「否则」，两条路只走一条。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>循环要三件事：</strong>从哪儿开始、什么时候停、每圈怎么变；少一件就转不停。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>分界线上最会出错：</strong>≤ 和 &lt; 差一圈，起始值 1 和 0 差一圈；结果差一次，先查符号和起始值。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那张便条：</strong>下雨带伞、否则戴帽子——这是分支；每天早上看一眼天气预报，一直看到出门为止——这是循环。程序世界里最常出现的两种走路方式，你今天都认出来了。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「条件、两条路、只走一条」说清楚什么是分支；再用「开始、停、变化」说清楚循环要注意什么。</p>
          <p style="color:var(--muted)">再动一动手：<strong>画出来</strong>——在纸上画一个循环的圈，把「成立就回去、不成立就出去」两个箭头都标上去。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写出一句生活中的「如果……则……否则……」，并说出条件成立时做什么、不成立时做什么。",
            "找出家里一件每天重复做、并且知道什么时候停的事，把循环的三件事（开始、停、变化）写出来。",
        ],
        [
            "给一段循环程序，先在纸上走一遍，写出每一圈里变量的值，再上机运行验证，看看和你写的一样不一样。",
            "用两三句话记下你一次把「≤」写成「&lt;」的经历：结果差了多少，你后来是怎么发现并改好的。",
        ],
        [
            "设计一个需要「循环里套分支」的任务（比如统计一周里每天有没有完成阅读），写清条件和比较符。",
            "同一个任务，用「≤ 5」和用「&lt; 6」，转的圈数一样吗？说说你的想法，并动手验证一下。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-e-branch-loop",
    "node_id": "it-e-branch-loop",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 小学",
    "title": "分支与循环结构",
    "name_en": "Branching and Loops",
    "grade": 5,
    "grade_cn": "五年级",
    "domain": "algorithm-programming",
    "domain_cn": "算法与程序",
    "lesson_type": "concept-practice",
    "version": "1.0.0",
    "description": "面向小学五年级：能说出分支是一问两路、条件成立走「则」不成立走「否则」且两条只走一条；能说出循环的三件事（从哪儿开始、什么时候停、每圈怎么变）；能在伪代码里一行一行跟读，说出每一步变量的值并数出循环转了几圈；能发现把「≤」改成「<」少转一圈、把起始值从 1 改成 0 多转一圈，并在结果差一次时先检查分界线上的符号与起始值。",
    "tags": ["分支结构", "循环结构", "伪代码执行", "边界值", "计算思维"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》小学「算法与程序」——在程序中运用顺序、分支、循环结构解决简单问题。",
    "hero_question": "一张「下雨带伞、否则戴帽子」的便条里，藏着程序里最重要的两种走路方式——你分得清吗？",
    "hero_alt": "分支与循环结构知识结构图：分支结构、循环结构与边界值检查三栏",
    "hero_caption": "分支与循环：一问两路只走一条 · 循环三件事 · 分界线上先查符号",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的动手活动都会围着它转。",
    "anchor_choices": [
        {"t": "程序怎么根据条件挑一条路走？", "d": "一句话问出两条路，为什么只走一条", "v": "程序怎么根据条件挑一条路走"},
        {"t": "循环为什么能一遍遍重复做？", "d": "它靠什么停下来，又靠什么继续", "v": "循环为什么能一遍遍重复做"},
        {"t": "为什么改成小于号就少跑一圈？", "d": "一个符号怎么就能差出一整圈", "v": "为什么改成小于号就少跑一圈"},
        {"t": "程序绕来绕去停不下来，怎么办？", "d": "想学会自己找出那个出问题的地方", "v": "程序绕来绕去停不下来怎么办"},
    ],
    "objectives": [
        "能说出分支是一问两路：条件成立走「则」，不成立走「否则」，两条路只走一条",
        "能说出循环的三件事：从哪儿开始、什么时候停、每圈怎么变，并知道少了第三件会停不下来",
        "能在伪代码里一行一行跟读，说出每一步变量的值，并数出循环一共转了几圈",
        "能发现把「≤」改成「<」少转一圈、把起始值从 1 改成 0 多转一圈，并在结果差一次时优先检查这两处",
    ],
    "objectives_plain": [
        "能说出分支是一问两路：条件成立走「则」，不成立走「否则」，两条路只走一条",
        "能说出循环的三件事：从哪儿开始、什么时候停、每圈怎么变，并知道少了第三件会停不下来",
        "能在伪代码里一行一行跟读，说出每一步变量的值，并数出循环一共转了几圈",
        "能发现把「≤」改成「<」少转一圈、把起始值从 1 改成 0 多转一圈，并在结果差一次时优先检查这两处",
    ],
    "standards": [
        {"content": "在程序中运用顺序、分支、循环结构解决简单问题",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 算法与程序"},
        {"content": "在逐行跟读与动手调整中体会边界值的影响，养成「结果不对先查分界线」的验证习惯",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 计算思维"},
    ],
    "prereqs": ["it-e-block-programming"],
    "prereqs_name": "积木式程序设计",
    "prereqs_meta": "it-e-block-programming",
    "leads_to": ["it-e-debugging"],
    "next_meta": "it-e-debugging",
    "section_images": ["assets/it-e-branch-loop-fig1.webp", "assets/it-e-branch-loop-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "一张便条里有两种结构：下雨带伞是分支，每天看一眼是循环。今天把它们拆开看清楚。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能一行一行跟读一段程序，说出它走了哪条路、转了几圈。",
        "objectives": "看清四件事：分支怎么挑路、循环哪三件事、怎么逐行跟读、结果差一次去哪查。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "分支是一问两路；条件只判真假；两条路只走一条；分界线上的数最会骗人。",
        "lab-1": "先选分数再单步走。试试 59 和 60——只差一分，走的路完全不同。",
        "module-2": "循环三件事：开始、停、变化。≤ 和 < 差一圈；起始值 1 和 0 差一圈。",
        "lab-2": "改三个开关后一定要重新走一遍；看循环圈数怎么变，别只看结果。",
        "worked-example": "四步：列出会变的量、看循环条件、圈里先判分支、走完再收尾。",
        "conceptest-1": "三个说法里都藏着高频错误，选完把解释读一遍。",
        "synthesis": "循环里套分支，及格人数从 0 数到 3；再把 ≥ 改成 > 看看少了谁。",
        "posttest": "体温报警、跳绳计数、总多跑一圈的程序，看看你还能不能用上同一套办法。",
        "summary": "三句话：分支怎么走、循环哪三件事、结果差一次先查哪里。",
        "homework": "三层小任务，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学信息科技「算法与程序」在积木编程之后、程序调试之前的一课。五年级学生的难点有两个：一是以为「否则」也要做一遍，二是把「小于等于」当成「小于」来数，于是结果总差一次。所以全课做成一个可以一行一行点着走的伪代码执行器：左边的程序行会被逐行高亮，右边的变量表跟着变，循环圈数一圈一圈累加。动手一用分支判断分数是否及格，59 与 60 分只差一分却走完全不同的路，边界意识从这里长出；动手二把循环的「起始值 / 比较符 / 上界」做成三个开关，学生亲眼看到把 ≤ 改成 < 就少转一圈、把 1 改成 0 就多转一圈。概念页把结论收成两句口诀，例题页示范「列变量—看条件—判分支—收尾」四步读法，综合任务把循环与分支叠在一起数及格人数，再通过把 ≥ 改成 > 复现一次边界少算。全课收口到一条可带走的检查习惯：结果差一次，先回去看分界线上的那个符号和那个起始值。",
    "plan_table": """| 1 | cover | 分支与循环结构 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预设答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：程序会怎么挑路、怎么转圈？ | 起·前测（暴露直觉） |
| 5 | concept | 分支：一问两路，只走一条 | 承·概念一（分支 + 边界意识） |
| 6 | interactive | 动手一：一行一行走一遍这段分支 | 承·核心模拟 A（逐行高亮 + 条件真假 + 路径输出） |
| 7 | concept | 循环：三件事想清楚，还要盯住分界线 | 承·概念二（循环三件事 + ≤/< 差异） |
| 8 | interactive | 动手二：改三个开关，看循环转几圈 | 承·核心模拟 B（逐行高亮 + 变量变化 + 累计圈数） |
| 9 | concept | 例题示范：读一段循环里套着分支的程序 | 转·重难点突破（四步读法 + 纠错） |
| 10 | quiz | 概念测试：三种说法，错在哪里 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：一边数圈，一边数及格人数 | 合·迁移应用（循环套分支 + ≥/> 边界对比） |
| 12 | quiz | 后测：换几个情境，规则还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把分支和循环讲清楚 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：分支结构 / 循环结构 / 边界值检查 三栏\n- P5 分支结构示意图（已生成）：一句话问出上下两条路，只走一条\n- P7 循环结构示意图（已生成）：条件成立绕圈回去并累计圈数，不成立才向下走出\n- 三张图均为教学示意图，不出现任何真实软件界面、截图或商标\n- 若需补充：学生手绘的循环圈与箭头标注（需获得授权后使用）",
}
