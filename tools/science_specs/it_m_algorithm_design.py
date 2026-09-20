# -*- coding: utf-8 -*-
"""初中信息科技 · 算法设计与程序实现（G7）—— 补齐课标「数据与算法」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-m-algorithm-design-fig1.webp'
F2 = './assets/it-m-algorithm-design-fig2.webp'

TTS = {
    "hero": "先看一个真实的问题。一个班五十名同学交上来的体测数据，要找出其中最高的一项。如果一个人一个人地用眼睛比，很容易看漏、看错。计算机最擅长做这种重复又怕出错的事，可它自己并不会思考——你得先想清楚每一步怎么做，再写成它能执行的指令。这节课我们就来学这件事：先设计算法，再用程序把它实现出来。",
    "problem-anchor": "在开始之前，先选出你最想弄明白的那个问题。是想知道算法和程序到底有什么区别，还是想知道怎样把一个真实问题拆成一步接一步的步骤，又或者你想亲手把一段算法写成能跑出结果的程序。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出算法的基本特征，分清算法与程序的区别。第二，能把一个真实问题分解成有输入、有处理、有输出的步骤。第三，能用变量和顺序、分支、循环三种结构把算法写成伪代码。第四，能运行自己的算法并检查结果，发现错误后知道从哪里改。",
    "pretest": "先做三道小题，凭你现在的想法选就行，选错了也没关系，正好能看出哪里需要重点听。选完会立刻出现解释。",
    "module-1": "算法是解决一个问题的一套明确步骤。它必须满足三个条件：每一步的含义都是确定的，不能有歧义；步骤是有限的，执行完一定要能停下来；每一步都真的做得到。算法还要交代清楚两件事：输入是什么，输出是什么。这里有最容易搞混的一点：算法是思路，程序是这个思路在某一种程序语言里写出来的具体实现。同一个算法，可以写成不同的程序；反过来，没有算法，程序就是一堆没有目标的指令。",
    "lab-1": "光说不够，我们把算法跑起来看。屏幕上是一段用伪代码写成的算法，任务是找出数据表里的最大值。点单步执行，你会看到高亮的行一步一步往下走，右边的变量盒里，最大值、下标、比较次数会跟着变。走完之后想一想：比较次数和数据的个数是什么关系？如果数据表变成十个数，比较次数会变成多少？",
    "module-2": "要让算法真的跑起来，需要两样东西：一个是变量，一个是控制结构。变量就像一个贴了标签的盒子，用来存放数据；给它一个新值，盒子里的内容就变了，这就是赋值。控制结构有三种：顺序，就是一步一步往下做；分支，就是先判断条件，再决定走哪条路；循环，就是条件还成立的时候，把同一段步骤反复执行。三种结构写得对，算法才跑得对。",
    "lab-2": "现在来比较两种查找算法。数据已经从大到小排好了队，要在里面找一个目标值。顺序查找是从头一个一个比；二分查找每次都从中间切一刀，判断目标在前半段还是后半段，再在剩下的一半里继续切。拖动滑块改一改数据个数，分别跑一遍，看看比较次数差多少。数据越多，差距会越明显。",
    "worked-example": "我们一起分析一个典型错误。有人说，算最大值只要写最大值等于第一个数，然后循环比较就行了。听起来没问题，但漏了两处。第一处，如果最大值一开始没有赋初值，第一次比较时它就是一个空盒子，程序没法比较。第二处，循环里的比较写成了大于等于，遇到两个相同的最大值时，会多更新一次。正确的四步是：看清问题、确定输入输出、写出每步做什么、再逐行检查循环的次数和边界。",
    "conceptest-1": "现在用三个容易弄错的说法考考你。请仔细读每一个选项，选出你认为正确的那个，然后看解释。",
    "synthesis": "学到这里，请你当一次算法设计师。手头有一周的用电量数据和一个阈值，要找出超过阈值的那些天，并统计一共有几天。屏幕上给了九个步骤卡片，其中有一张是别的问题里混进来的，先把它找出来，再把剩下的按正确顺序拼成算法，然后运行看看结果对不对。",
    "posttest": "最后用新情境检验一下。这次出现了成绩统计和猜数字，看看你能不能把变量、分支、循环用上去。",
    "summary": "这节课我们弄明白了三件事。第一，算法是一套明确、有限、能做得到的步骤，它必须有输入和输出，而程序是算法在某种语言里的实现。第二，变量是存放数据的盒子，赋值会改变它的值；顺序、分支、循环是三种最基本的控制结构。第三，一个算法跑得对不对，要看它的循环次数、边界条件和结果，出了问题就从这三处去查。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出算法的三个基本特征，并写出求最小值算法的伪代码。第二层能力应用，动手做：把自己写的伪代码逐行跟踪一遍，记录每一步变量的值。第三层迁移挑战，选做：给一个真实的小问题设计算法，写出两种不同的做法，比较它们各要执行多少步。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 算法与程序", "lab-1": "实验室一 伪代码执行器", "module-2": "概念二 变量与控制结构",
    "lab-2": "实验室二 查找算法对比", "worked-example": "例题讲解", "conceptest-1": "概念测试",
    "synthesis": "综合任务 拼装算法", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

LAB_CSS = """
<style>
.ta-code { list-style: none; margin: 0; padding: 0; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 13.5px; }
.ta-code li { padding: 5px 10px; border-radius: 8px; color: var(--text-secondary); white-space: pre-wrap; transition: background .2s ease, color .2s ease; }
.ta-code li.on { background: var(--brand-soft); color: var(--text-strong); font-weight: 700; box-shadow: inset 3px 0 0 var(--brand); }
.ta-bars { display: flex; gap: 8px; flex-wrap: wrap; }
.ta-bar { flex: 1; min-width: 46px; text-align: center; padding: 10px 4px; border-radius: 10px;
  background: var(--bg-subtle); border: 1px solid var(--line-subtle); font-weight: 700; font-variant-numeric: tabular-nums; }
.ta-bar.cur { border-color: var(--brand); background: var(--brand-soft); }
.ta-bar.best { border-color: var(--brand-2); background: var(--brand-2-soft); }
.ta-bar.done { opacity: .4; }
.ta-cells { display: flex; gap: 4px; flex-wrap: wrap; }
.ta-cell { width: 30px; height: 30px; display: grid; place-items: center; border-radius: 7px; font-size: 12px;
  background: var(--bg-subtle); border: 1px solid var(--line-subtle); font-variant-numeric: tabular-nums; }
.ta-cell.range { background: var(--brand-soft); border-color: var(--brand); font-weight: 700; }
.ta-cell.probe { background: var(--warm-soft); border-color: var(--warm); font-weight: 800; }
.ta-cell.hit { background: var(--brand-2-soft); border-color: var(--brand-2); font-weight: 800; }
.ta-cell.out { opacity: .3; }
.ta-slots { min-height: 120px; border: 2px dashed var(--line-subtle); border-radius: 12px; padding: 10px; background: var(--bg-subtle); }
.ta-slot { display: flex; align-items: center; gap: 8px; padding: 7px 10px; margin-bottom: 6px; border-radius: 9px;
  background: var(--card); border: 1px solid var(--line-subtle); font-size: 14px; }
.ta-slot .idx { flex-shrink: 0; width: 22px; height: 22px; display: grid; place-items: center; border-radius: 50%;
  background: var(--brand); color: #fff; font-size: 12px; font-weight: 800; }
.ta-slot.bad { border-color: var(--danger); background: rgba(239, 68, 68, .08); }
.ta-slot.good { border-color: var(--ok); background: rgba(34, 197, 94, .08); }
</style>
"""

CUSTOM_JS = r"""
/* ============================================================
   it-m-algorithm-design 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 伪代码单步执行器：求最大值（变量盒实时状态）
   3) 查找算法对比器：顺序查找 vs 二分查找（比较步数）
   4) 算法拼装工作台：步骤卡片排序 + 运行校验
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

  /* ---------- 2. 伪代码单步执行器 ---------- */
  var L1_DATA = [12, 7, 25, 9, 18];
  var l1Code = document.getElementById('lab1-code');

  function buildTrace() {
    var d = L1_DATA, n = d.length, out = [];
    var best = d[0], i = 1, cmp = 0;
    out.push({ line: 2, best: best, i: 1, cmp: cmp, cur: -1, bestAt: 0,
      msg: '把第 1 个数 12 作为最大值的最初猜测，放进「最大值」这个变量盒。' });
    out.push({ line: 3, best: best, i: 2, cmp: cmp, cur: -1, bestAt: 0,
      msg: '下标指向第 2 个位置，准备从第二个数开始逐个比较。' });
    while (i < n) {
      out.push({ line: 4, best: best, i: i + 1, cmp: cmp, cur: -1, bestAt: -1,
        msg: '判断循环条件：下标 ' + (i + 1) + ' 还没有超过数据个数 ' + n + '，条件成立，进入循环。' });
      cmp = cmp + 1;
      var willUpdate = d[i] > best;
      out.push({ line: 5, best: best, i: i + 1, cmp: cmp, cur: i, bestAt: -1,
        msg: '比较 d[' + (i + 1) + '] = ' + d[i] + ' 和当前最大值 ' + best + '，' +
             (willUpdate ? '它更大。' : '它不更大。') });
      if (willUpdate) {
        best = d[i];
        out.push({ line: 6, best: best, i: i + 1, cmp: cmp, cur: i, bestAt: i,
          msg: '执行赋值：最大值 ← ' + best + '，变量盒里的数字被更新了。' });
      }
      i = i + 1;
      out.push({ line: 7, best: best, i: i + 1, cmp: cmp, cur: -1, bestAt: -1,
        msg: '执行 下标 ← 下标 + 1，下标变成 ' + (i + 1) + '，回到循环开头。' });
    }
    out.push({ line: 4, best: best, i: i + 1, cmp: cmp, cur: -1, bestAt: -1,
      msg: '再判断循环条件：下标 ' + (i + 1) + ' 已经超过数据个数 ' + n + '，条件不成立，循环结束。' });
    out.push({ line: 8, best: best, i: i + 1, cmp: cmp, cur: -1, bestAt: -1, done: true,
      msg: '输出最大值 ' + best + '。算法结束，一共做了 ' + cmp + ' 次比较。' });
    return out;
  }

  if (l1Code) {
    var trace = buildTrace();
    var pos = 0;
    var eBest = document.getElementById('l1-best');
    var eI = document.getElementById('l1-i');
    var eCmp = document.getElementById('l1-cmp');
    var eLab1Out = document.getElementById('l1-out');
    var eBars = document.getElementById('lab1-bars');
    var eStep = document.getElementById('l1-step');
    var eAuto = document.getElementById('l1-auto');
    var timer = null;

    function renderBars(frame) {
      eBars.innerHTML = '';
      L1_DATA.forEach(function (v, k) {
        var div = document.createElement('div');
        div.className = 'ta-bar';
        if (frame.cur === k) div.className += ' cur';
        else if (frame.bestAt === k) div.className += ' best';
        else if (frame.done && k !== L1_DATA.indexOf(frame.best)) div.className += ' done';
        div.textContent = v;
        eBars.appendChild(div);
      });
    }

    function render1() {
      var f = trace[pos];
      l1Code.querySelectorAll('li').forEach(function (li) {
        li.classList.toggle('on', Number(li.dataset.line) === f.line);
      });
      eBest.textContent = f.best;
      eI.textContent = f.i <= L1_DATA.length ? f.i : '越界';
      eCmp.textContent = f.cmp;
      renderBars(f);
      eLab1Out.className = 'result' + (f.done ? '' : ' warn');
      eLab1Out.innerHTML = '<strong>第 ' + (pos + 1) + ' / ' + trace.length + ' 步：</strong>' + f.msg;
      eStep.textContent = pos >= trace.length - 1 ? '已执行结束' : '单步执行';
      eStep.disabled = pos >= trace.length - 1;
    }

    function advance() {
      if (pos >= trace.length - 1) { stopAuto(); return; }
      pos = pos + 1;
      render1();
      if (pos >= trace.length - 1) stopAuto();
    }
    function stopAuto() {
      if (timer) { clearInterval(timer); timer = null; }
      eAuto.textContent = '自动运行';
    }

    eStep.addEventListener('click', function () { stopAuto(); advance(); });
    eAuto.addEventListener('click', function () {
      if (timer) { stopAuto(); return; }
      if (pos >= trace.length - 1) { pos = 0; render1(); }
      eAuto.textContent = '暂停';
      timer = setInterval(advance, 1100);
    });
    document.getElementById('l1-reset').addEventListener('click', function () {
      stopAuto(); pos = 0; render1();
    });
    render1();
  }

  /* ---------- 3. 查找算法对比器 ---------- */
  var L2_N = 16;
  var L2_TARGET = 13;
  var l2Body = document.getElementById('lab2-stage');

  function seqTrace(n, t) {
    var out = [];
    for (var i = 1; i <= n; i++) {
      out.push({ probe: i, lo: 1, hi: n, found: i === t, cnt: i, msg: i === t
        ? '第 ' + i + ' 次比较就找到了 ' + t + '，顺序查找一共比了 ' + i + ' 次。'
        : '第 ' + i + ' 次比较：' + i + ' 不等于 ' + t + '，继续往后比。' });
      if (i === t) break;
    }
    return out;
  }

  function binTrace(n, t) {
    var out = [], lo = 1, hi = n, cnt = 0;
    while (lo <= hi) {
      cnt = cnt + 1;
      var mid = Math.floor((lo + hi) / 2);
      if (mid === t) {
        out.push({ probe: mid, lo: lo, hi: hi, found: true, cnt: cnt,
          msg: '第 ' + cnt + ' 次：中间位置是 ' + mid + '，正好就是目标值，查找结束。' });
        break;
      }
      if (mid < t) {
        out.push({ probe: mid, lo: lo, hi: hi, found: false, cnt: cnt,
          msg: '第 ' + cnt + ' 次：中间位置是 ' + mid + '，比目标值小，目标一定在右半段，把左边界挪到 ' + (mid + 1) + '。' });
        lo = mid + 1;
      } else {
        out.push({ probe: mid, lo: lo, hi: hi, found: false, cnt: cnt,
          msg: '第 ' + cnt + ' 次：中间位置是 ' + mid + '，比目标值大，目标一定在左半段，把右边界挪到 ' + (mid - 1) + '。' });
        hi = mid - 1;
      }
    }
    return out;
  }

  if (l2Body) {
    var eCells = document.getElementById('l2-cells');
    var eInfo = document.getElementById('l2-info');
    var eN = document.getElementById('l2-n');
    var eT = document.getElementById('l2-target');
    var eNv = document.getElementById('l2-n-val');
    var eTv = document.getElementById('l2-target-val');
    var seqSteps = 0, binSteps = 0;

    function clampTarget() {
      if (L2_TARGET > L2_N) L2_TARGET = L2_N;
      eT.max = String(L2_N);
      eT.value = String(L2_TARGET);
      eTv.textContent = String(L2_TARGET);
    }

    function drawCells(frame, mode) {
      eCells.innerHTML = '';
      for (var i = 1; i <= L2_N; i++) {
        var d = document.createElement('div');
        d.className = 'ta-cell';
        d.textContent = String(i);
        if (frame) {
          if (frame.found && frame.probe === i) d.className += ' hit';
          else if (frame.probe === i) d.className += ' probe';
          else if (mode === 'bin') {
            if (i >= frame.lo && i <= frame.hi) d.className += ' range';
            else d.className += ' out';
          } else if (i < frame.probe) d.className += ' out';
        }
        eCells.appendChild(d);
      }
    }

    function summary() {
      if (seqSteps === 0 && binSteps === 0) {
        eInfo.className = 'result warn';
        eInfo.textContent = '先点一个按钮跑一遍，看看两种查找各要比较多少次。';
        return;
      }
      eInfo.className = 'result';
      var faster = binSteps && seqSteps ? Math.round(seqSteps / binSteps * 10) / 10 : 0;
      eInfo.innerHTML = '<strong>顺序查找 ' + (seqSteps || '—') + ' 次 ｜ 二分查找 ' + (binSteps || '—') + ' 次</strong><br>' +
        '在 ' + L2_N + ' 个已经排好序的数据里，二分查找大约只要顺序查找的 1/' + (faster || '—') + '。' +
        '数据量越大，这个差距越明显——这就是好的算法带来的效率提升。';
    }

    var seqTimer = null, binTimer = null, posSeq = 0, posBin = 0, trSeq = [], trBin = [];

    function stopTimers() {
      if (seqTimer) { clearInterval(seqTimer); seqTimer = null; }
      if (binTimer) { clearInterval(binTimer); binTimer = null; }
    }

    document.getElementById('l2-seq').addEventListener('click', function () {
      stopTimers();
      trSeq = seqTrace(L2_N, L2_TARGET);
      posSeq = 0;
      seqTimer = setInterval(function () {
        drawCells(trSeq[posSeq], 'seq');
        eInfo.className = 'result warn';
        eInfo.innerHTML = '<strong>顺序查找：</strong>' + trSeq[posSeq].msg;
        if (posSeq >= trSeq.length - 1) {
          clearInterval(seqTimer); seqTimer = null;
          seqSteps = trSeq.length; binSteps = 0; summary();
          return;
        }
        posSeq = posSeq + 1;
      }, 420);
    });

    document.getElementById('l2-bin').addEventListener('click', function () {
      stopTimers();
      trBin = binTrace(L2_N, L2_TARGET);
      posBin = 0;
      binTimer = setInterval(function () {
        drawCells(trBin[posBin], 'bin');
        eInfo.className = 'result warn';
        eInfo.innerHTML = '<strong>二分查找：</strong>' + trBin[posBin].msg;
        if (posBin >= trBin.length - 1) {
          clearInterval(binTimer); binTimer = null;
          binSteps = trBin.length; seqSteps = 0; summary();
          return;
        }
        posBin = posBin + 1;
      }, 700);
    });

    eN.addEventListener('input', function () {
      L2_N = Number(eN.value);
      eNv.textContent = String(L2_N);
      clampTarget();
      stopTimers(); seqSteps = 0; binSteps = 0;
      drawCells(null, 'seq'); summary();
    });
    eT.addEventListener('input', function () {
      L2_TARGET = Number(eT.value);
      eTv.textContent = String(L2_TARGET);
      stopTimers(); seqSteps = 0; binSteps = 0;
      drawCells(null, 'seq'); summary();
    });

    clampTarget();
    drawCells(null, 'seq');
    summary();
  }

  /* ---------- 4. 算法拼装工作台 ---------- */
  var CARD_POOL = [
    { id: 'a', text: '输入 每天的用电量 d[1..7]，以及阈值 t' },
    { id: 'b', text: '超标天数 ← 0' },
    { id: 'c', text: '下标 ← 1' },
    { id: 'd', text: '当 下标 ≤ 7 时，重复执行：' },
    { id: 'e', text: '　　如果 d[下标] > t 则' },
    { id: 'f', text: '　　　　超标天数 ← 超标天数 + 1' },
    { id: 'g', text: '　　下标 ← 下标 + 1' },
    { id: 'h', text: '输出 超标天数' },
    { id: 'x', text: '输出 最大值' },
  ];
  var CARD_ORDER = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
  var SYN_DATA = [31, 12, 8, 27, 45, 19, 10];
  var SYN_T = 25;
  var synPool = document.getElementById('syn-pool');

  if (synPool) {
    var chosen = [];
    var eSlots = document.getElementById('syn-slots');
    var eSynOut = document.getElementById('syn-out');
    var eRun = document.getElementById('syn-run');

    function poolCards() {
      synPool.innerHTML = '';
      CARD_POOL.forEach(function (c) {
        if (chosen.indexOf(c.id) >= 0) return;
        var b = document.createElement('button');
        b.className = 'choice';
        b.style.cssText = 'text-align:left;font-size:14px;padding:10px 12px';
        b.textContent = c.text;
        b.addEventListener('click', function () {
          chosen.push(c.id);
          renderSyn();
        });
        synPool.appendChild(b);
      });
      if (synPool.children.length === 0) {
        var tip = document.createElement('p');
        tip.style.cssText = 'color:var(--muted);margin:0;font-size:14px';
        tip.textContent = '卡片都用完了，点「运行算法」看看结果。';
        synPool.appendChild(tip);
      }
    }

    function renderSyn() {
      eSlots.innerHTML = '';
      if (chosen.length === 0) {
        var empty = document.createElement('p');
        empty.style.cssText = 'color:var(--muted);margin:0;font-size:14px';
        empty.textContent = '从这里开始拼：先点左边第一张卡片。';
        eSlots.appendChild(empty);
      }
      chosen.forEach(function (id, k) {
        var card = CARD_POOL.filter(function (c) { return c.id === id; })[0];
        var row = document.createElement('div');
        row.className = 'ta-slot';
        row.innerHTML = '<span class="idx">' + (k + 1) + '</span><span>' + card.text + '</span>';
        var del = document.createElement('button');
        del.className = 'toolbar-btn';
        del.style.cssText = 'margin-left:auto;width:28px;height:28px;font-size:14px';
        del.textContent = '×';
        del.title = '移除这张卡片';
        del.addEventListener('click', function () {
          chosen.splice(k, 1);
          if (eRun.disabled) { eRun.disabled = false; eRun.textContent = '运行算法'; }
          renderSyn();
        });
        row.appendChild(del);
        eSlots.appendChild(row);
      });
      poolCards();
      if (!eRun.disabled) {
        eSynOut.className = 'result warn';
        eSynOut.textContent = '把步骤按顺序拼好，再点「运行算法」。';
      }
    }

    eRun.addEventListener('click', function () {
      var wrongAt = -1;
      chosen.forEach(function (id, k) {
        if (wrongAt < 0 && CARD_ORDER[k] !== id) wrongAt = k;
      });
      if (chosen.length < CARD_ORDER.length) {
        eSynOut.className = 'result error';
        eSynOut.innerHTML = '<strong>还没有拼完：</strong>一共需要 ' + CARD_ORDER.length +
          ' 步，现在只放了 ' + chosen.length + ' 步。想一想，统计数据之前，是不是要先准备一个从 0 开始的计数器？';
        return;
      }
      if (wrongAt >= 0) {
        var bad = CARD_POOL.filter(function (c) { return c.id === chosen[wrongAt]; })[0];
        var rows = eSlots.querySelectorAll('.ta-slot');
        if (rows[wrongAt]) rows[wrongAt].className = 'ta-slot bad';
        var rest = rows[wrongAt + 1];
        if (rest) rest.className = 'ta-slot bad';
        eSynOut.className = 'result error';
        eSynOut.innerHTML = '<strong>第 ' + (wrongAt + 1) + ' 步有问题：</strong>「' + bad.text +
          '」放在这个位置跑不通。<br><strong>错因提醒：</strong>这是在真实数据上运行，程序会照着顺序执行。先检查三件事——变量有没有先赋初值、循环是不是在初始化之后、输出是不是放在循环外面。';
        return;
      }
      var over = [];
      SYN_DATA.forEach(function (v, k) { if (v > SYN_T) over.push('第 ' + (k + 1) + ' 天（用电量 ' + v + '）'); });
      var bars = '';
      SYN_DATA.forEach(function (v) {
        var hit = v > SYN_T;
        bars += '<span class="ta-cell' + (hit ? ' hit' : ' out') + '" style="width:auto;min-width:34px;padding:0 6px">' + v + '</span>';
      });
      eSlots.querySelectorAll('.ta-slot').forEach(function (r) { r.className = 'ta-slot good'; });
      eSynOut.className = 'result';
      eSynOut.innerHTML = '<strong>运行成功！</strong>阈值是 ' + SYN_T + '，逐天比较后得到：' + bars +
        '<br>超标的是：' + over.join('、') +
        '，一共 <strong>' + over.length + ' 天</strong>。算法输出：超标天数 = ' + over.length + '。';
      eRun.disabled = true;
      eRun.textContent = '运行完成';
    });

    renderSyn();
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：算法到底是什么？", TTS["pretest"], [
        {"q": "下面关于「算法」和「程序」的说法，正确的是：",
         "options": [("算法是解决问题的思路，程序是这种思路在某种程序语言里的实现", True),
                     ("算法就是程序，两个词说的是同一件事", False),
                     ("有了程序就不需要再想算法了", False)],
         "explain": "算法是思路，程序是具体的实现。同一个算法可以写成不同的程序。<strong>错因提醒：</strong>把算法和程序搞混，是这一课最常见的错误，请记住一个在前、一个在后。"},
        {"q": "一段算法必须有输入和输出吗？",
         "options": [("要有明确的输入是什么、输出是什么，过程才说得清楚", True),
                     ("不需要，只要能算出结果就行", False),
                     ("只有很长的算法才需要", False)],
         "explain": "说清楚输入和输出，才能判断算法到底解决了什么问题，也才能检验它算得对不对。"},
        {"q": "一个算法在数据不断变化时，只要能算出正确答案就可以了，步数多少无所谓。这句话：",
         "options": [("不准确，步数会影响算法跑得快不快", True),
                     ("完全正确", False),
                     ("只对特别大的数据才不准确", False)],
         "explain": "同样能算对的两个算法，执行步数可能差很多。这个问题先记在心里，等下做查找实验时会看得很清楚。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "算法是明确有限的步骤，程序是它在语言里的实现", TTS["module-1"], f'''
        <div class="inner-card">
          <p><strong>为什么要学这一课？</strong>你已经会用流程图描述生活里的做事顺序了，但真实的计算任务动辄几十万条数据，靠人一步一步盯着做根本做不完。<strong>所以</strong>我们需要把解决问题的步骤写成计算机能照着执行的算法，再用程序把它实现出来。</p>
        </div>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>算法要满足的三个条件</strong></p>
            <p style="color:var(--muted)">① 确定性：每一步的含义唯一，不能有歧义；② 有穷性：步骤有限，执行完能停下来；③ 可行性：每一步都真的做得到。</p>
          </div>
          <div class="inner-card">
            <p><strong>算法与程序的关系</strong></p>
            <p style="color:var(--muted)">算法是思路，程序是这个思路在某种程序语言里的具体实现。同一个算法，可以写成不同的程序。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="算法与程序的关系示意图：真实问题经过算法设计再写成程序">
          <figcaption>从真实问题到能运行的方案：先有算法（输入 → 处理步骤 → 输出），再把算法翻译成程序</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🧭</span><div><strong>记忆锚点：</strong>算法像「菜谱」，程序像「照着菜谱做出来的那道菜」。菜谱可以抄进不同的厨房，菜可以做出不同的样子，但火候和顺序不能乱。</div></div>
{insight_box([
    {"lens": "看见它", "text": "同一份数据，同一件事，不同的算法会走不同的路，用的步数可能差几十倍。"},
    {"lens": "拆开它", "text": "任何一个算法都能拆成三段：从哪里拿数据（输入）、中间怎么处理（步骤）、最后给出什么（输出）。"},
    {"lens": "解释它", "text": "为什么要求确定性？因为计算机不会猜你的心思。一句有歧义的指令，它就不知道该怎么执行。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "伪代码执行器：一步一步看变量的值怎么变", TTS["lab-1"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">点「单步执行」，高亮行会一行一行往下走，右边的变量盒会同步变化。留意比较次数是怎么累加的。</p>
        <div class="lab-panel">
          <div class="grid grid-2">
            <div class="inner-card" style="margin:0">
              <p style="margin:0 0 8px"><strong>伪代码：找出数据表里的最大值</strong></p>
              <ol class="ta-code" id="lab1-code">
                <li data-line="1">输入 数据表 d[1..5]</li>
                <li data-line="2">最大值 ← d[1]</li>
                <li data-line="3">下标 ← 2</li>
                <li data-line="4">当 下标 ≤ 5 时，重复执行：</li>
                <li data-line="5">　　如果 d[下标] &gt; 最大值 则</li>
                <li data-line="6">　　　　最大值 ← d[下标]</li>
                <li data-line="7">　　下标 ← 下标 + 1</li>
                <li data-line="8">输出 最大值</li>
              </ol>
            </div>
            <div class="inner-card" style="margin:0">
              <p style="margin:0 0 8px"><strong>变量盒（实时状态）</strong></p>
              <div class="lab-readout" style="margin-top:0">
                <div class="readout-cell"><span class="k">最大值</span><span class="v" id="l1-best">—</span></div>
                <div class="readout-cell"><span class="k">下标</span><span class="v" id="l1-i">—</span></div>
                <div class="readout-cell"><span class="k">比较次数</span><span class="v green" id="l1-cmp">0</span></div>
              </div>
              <p style="margin:14px 0 6px"><strong>数据表 d</strong></p>
              <div class="ta-bars" id="lab1-bars"></div>
            </div>
          </div>
          <p class="result warn" id="l1-out" style="margin-top:12px">点「单步执行」开始。</p>
          <div class="flex-row">
            <button class="choice" id="l1-step" style="text-align:center;flex:1">单步执行</button>
            <button class="choice" id="l1-auto" style="text-align:center;flex:1">自动运行</button>
            <button class="choice" id="l1-reset" style="text-align:center;flex:1">重新开始</button>
          </div>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">📊</span><div><strong>数一数：</strong>5 个数据一共比较了几次？如果数据变成 10 个，比较次数会变成多少？你会发现，比较次数正好等于「数据个数减 1」——这就是算法的规律，不用一个个数。</div></div>
    ''', tag="程序实验室", bloom="apply"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "变量是装数据的盒子，三种结构决定走的路线", TTS["module-2"], f'''
        <div class="inner-card">
          <p><strong>变量：贴了标签的盒子。</strong>给它一个新值，盒子里的内容就变了，这个动作叫做<strong>赋值</strong>。写程序时最容易出错的地方，就是忘了先给盒子放一个初值——空盒子没法参与比较。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>顺序结构：</strong>一步一步往下做，前一步做完才做后一步。</div></div>
          <div class="step"><span class="n">2</span><div><strong>分支结构：</strong>先判断条件，成立走一条路，不成立走另一条路。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>循环结构：</strong>条件还成立时，把同一段步骤反复执行，直到条件不成立才往下走。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="顺序、分支、循环三种基本控制结构的流程图对照">
          <figcaption>三种基本控制结构：顺序（一条直线）、分支（条件分叉）、循环（回到前面的箭头）</figcaption>
        </figure>
        <div class="inner-card">
          <p><strong>易错点：循环的边界。</strong>「下标 ≤ 数据个数」和「下标 &lt; 数据个数」只差一个符号，执行结果却完全不同：前者会处理到最后一个数据，后者会漏掉它。写完循环，一定要拿最小的数据和最大的数据各试一遍。</p>
        </div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "查找算法对比器：同样是找，步数差多少？", TTS["lab-2"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">数据已经按 1、2、3…… 的顺序排好。先选数据个数和目标值，再分别跑一次两种查找，比较步数。</p>
        <div class="lab-panel">
          <div class="slider-row">
            <label for="l2-n">数据个数</label>
            <input type="range" id="l2-n" min="8" max="64" step="8" value="16">
            <span class="readout-cell" style="flex:0 0 84px"><span class="k">个数</span><span class="v" id="l2-n-val">16</span></span>
          </div>
          <div class="slider-row">
            <label for="l2-target">目标值</label>
            <input type="range" id="l2-target" min="1" max="16" step="1" value="13">
            <span class="readout-cell" style="flex:0 0 84px"><span class="k">找它</span><span class="v" id="l2-target-val">13</span></span>
          </div>
          <div id="lab2-stage" style="margin-top:14px">
            <div class="ta-cells" id="l2-cells"></div>
          </div>
          <div class="flex-row">
            <button class="choice" id="l2-seq" style="text-align:center;flex:1">顺序查找：从头一个一个比</button>
            <button class="choice" id="l2-bin" style="text-align:center;flex:1">二分查找：每次切掉一半</button>
          </div>
          <p class="result warn" id="l2-info" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">⚡</span><div><strong>试一试：</strong>把数据个数拖到 64，目标值选大一点，两种查找的步数会拉开很大。为什么二分查找能这么快？因为它每一步都排除掉一半的可能——这就是好算法的价值。</div></div>
    ''', tag="程序实验室", bloom="analyze"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：一个错误算法是怎么被改对的", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>有同学这样写「找最大值」的算法：直接循环比较，遇到更大的就更新最大值。这段算法哪里有问题？请说明理由并改正。</p>
        </div>
        <div class="inner-card">
          <p style="margin:0 0 6px"><strong>第一步　看清问题：</strong>输入是一组数据，输出是其中最大的那个数。</p>
          <p style="margin:0 0 6px"><strong>第二步　找漏洞一：</strong>最大值这个变量没有赋初值，第一次比较时它是一个空盒子，没法比。改正：先让它等于第一个数据。</p>
          <p style="margin:0 0 6px"><strong>第三步　找漏洞二：</strong>循环的结束条件写得不清楚，容易漏掉最后一个数据。改正：写成「下标 ≤ 数据个数」，保证每个数据都被看到。</p>
          <p style="margin:0"><strong>第四步　逐行自查：</strong>用最小的那一组数据试一遍，再用最大的那一组试一遍，结果都对，算法才算改好了。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">最容易出错的是「忘了赋初值」。不少同学误认为变量一写出来就自动是 0，其实没有赋值的变量是空的，拿它去比较，程序的行为就不确定了。第二常见的错误是把循环边界写成「下标 &lt; 数据个数」，结果永远是最后一个数没被比较到。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "下面哪句话是正确的？",
         "options": [("算法是解决问题的思路，程序是它在某种程序语言里的实现", True),
                     ("算法越短，程序跑得一定越快", False),
                     ("只要程序能跑出结果，就不需要算法了", False)],
         "explain": "算法和程序是两个层次：先有思路，再有实现。<strong>错因提醒：</strong>把这两个词搞混，是这一课最高频的常见错误。写得短不等于跑得快，步数多少才是关键。"},
        {"q": "要统计一组数据里有多少个数大于 60，下面哪一步必不可少？",
         "options": [("先让「计数器 ← 0」给变量一个初值", True),
                     ("先输出结果", False),
                     ("先把数据从小到大排序", False)],
         "explain": "计数器必须从 0 开始，否则加的基数就是错的。<strong>错因提醒：</strong>很多同学误认为变量不赋值也自动是 0，实际上没有赋初值的变量是空的，统计结果一定不对。"},
        {"q": "在「找最大值」的算法里，把判断条件写成「如果 d[下标] ≥ 最大值」，最可能出现的问题是：",
         "options": [("遇到相同的最大值时会多更新一次，虽然结果一样但白白多做了一步", True),
                     ("最大值一定会算错", False),
                     ("循环会永远停不下来", False)],
         "explain": "≥ 和 &gt; 在结果上常常一致，但条件越精确，多做的无用步骤越少。<strong>错因提醒：</strong>不要以为「结果对就等于算法对」，还要看执行了多少步。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：把一段算法拼装出来并运行", TTS["synthesis"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">需求：读入一周的用电量和一个阈值，找出超过阈值的天数。左边有九张卡片，其中一张是别的问题里混进来的，先把它排除掉。</p>
        <div class="lab-panel">
          <div class="grid grid-2">
            <div>
              <p style="margin:0 0 8px"><strong>步骤卡片池</strong></p>
              <div id="syn-pool" class="flex-row" style="display:block;margin-top:0"></div>
            </div>
            <div>
              <p style="margin:0 0 8px"><strong>我的算法（按顺序）</strong></p>
              <div class="ta-slots" id="syn-slots"></div>
            </div>
          </div>
          <p class="result warn" id="syn-out" style="margin-top:12px"></p>
          <div class="flex-row">
            <button class="choice" id="syn-run" style="text-align:center;flex:1">运行算法</button>
          </div>
        </div>
        <div class="inner-card">
          <p><strong>写下来，说给同桌听：</strong>为什么计数器必须在循环之前初始化？如果把「超标天数 ← 0」放在循环里面，会发生什么？</p>
          <textarea id="syn-answer" rows="3" placeholder="因为……如果放在循环里面，就会……"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换一个情境，看看规律还在不在", TTS["posttest"], [
        {"q": "要在一份成绩单里找出最高分，最合适的写法是：",
         "options": [("把最高分先设为第一个成绩，再依次和后面的成绩比较，更大就更新", True),
                     ("把最高分先设为 0，再比较", False),
                     ("把最高分先设为 100，再比较", False)],
         "explain": "初值设为第一个数据最稳妥。设成 0 在全是负分时就会出错；设成 100 在满分超过 100 时也会出错。<strong>错因提醒：</strong>初值选得随意，是结果不对的常见原因。"},
        {"q": "玩「猜数字」时，范围是 1 到 100。每猜一次都会告诉你「大了」或「小了」，最有效的策略是：",
         "options": [("每次都猜当前范围正中间的那个数，把范围缩掉一半", True),
                     ("从 1 开始一个一个往上猜", False),
                     ("随机猜一个数，碰运气", False)],
         "explain": "这就是二分法的思路：每猜一次排除一半的可能，100 以内最多 7 次就能猜到。顺序猜最坏要 100 次。<strong>错因提醒：</strong>很多同学误认为随机猜比较快，其实随机猜的最坏情况比顺序猜还慢。"},
        {"q": "一段程序跑出来的结果和预期不一样。按照这节课学到的方法，最先该检查的是：",
         "options": [("变量的初值和循环的边界条件", True),
                     ("把整段程序重新写一遍", False),
                     ("换一台更快的电脑", False)],
         "explain": "绝大多数算法的错误都出在这两处：变量没有正确初始化、循环少走或多走了一次。先查这两处，再谈重写。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把自己讲明白", TTS["summary"], f'''
        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>算法</strong>：一套明确、有限、做得到的步骤，必须交代清楚输入和输出；程序是它在某种语言里的实现。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>变量与结构</strong>：变量是装数据的盒子，赋值会改变它的值；顺序、分支、循环是三种最基本的控制结构。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>检验</strong>：看结果对不对、看步数多不多、看边界有没有走漏——出了问题就从这三处查。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那份体测数据：</strong>五十条数据用眼睛比很容易看漏，写成算法之后，程序会老老实实从头比到尾，一次不漏。而且换一批数据，算法完全不用改——这就是「先设计算法、再写程序」的价值。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「输入、变量、循环、输出」这四个词，说清楚你是怎么从一组数据里找出最大值的。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "说出算法的三个基本特征，并用自己的话说明算法和程序的区别。",
            "写出「找出一组数据里的最小值」的伪代码，标出输入和输出分别是什么。",
            "画出循环结构的流程图，标出「条件判断」和「回到前面」这两处箭头。",
        ],
        [
            "把自己的伪代码逐行跟踪一遍，用「变量盒」的形式记录每一步下标和最小值的变化。",
            "把查找算法的数据个数从 16 改成 32，分别跑一次顺序查找和二分查找，记录比较次数并说明差距变大了还是变小了。",
        ],
        [
            "为身边的一个小问题（比如统计一周的作业用时、找出跳远成绩的第一名）设计算法，写出两种做法，并比较它们各要执行多少步。",
            "找一段你写过的程序或流程图，检查里面有没有「变量没有赋初值」或「循环边界写错」的问题，改好之后说明你改了什么。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-m-algorithm-design",
    "node_id": "it-m-algorithm-design",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "middle",
    "stage_cn": "初中",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 初中",
    "title": "算法设计与程序实现",
    "name_en": "Algorithm Design and Program Implementation",
    "grade": 7,
    "grade_cn": "七年级",
    "domain": "data-algorithms",
    "domain_cn": "数据与算法",
    "lesson_type": "design-implementation",
    "version": "1.0.0",
    "description": "从真实的数据处理需求出发，理解算法的基本特征与算法和程序的区别，掌握变量、赋值与顺序/分支/循环三种控制结构，能设计并逐步跟踪一段算法，并能比较不同算法的执行步数。",
    "tags": ["算法", "程序实现", "伪代码", "变量", "循环", "算法效率"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》初中「数据与算法」——分析实际问题，设计算法并用程序语言实现；能对算法进行验证与优化。",
    "hero_question": "一个必须反复做、又不能出错的任务，怎样变成计算机能照着执行的方案？",
    "hero_alt": "算法设计与程序实现知识结构图：算法设计、程序实现、检验优化三栏",
    "hero_caption": "算法设计 → 程序实现 → 检验与优化：说清输入输出 · 用好变量与三种结构 · 用结果和步数检验算法",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的实验都会围着它转。",
    "anchor_choices": [
        {"t": "算法和程序到底有什么区别？", "d": "为什么说先有思路再写代码", "v": "算法和程序到底有什么区别"},
        {"t": "怎么把一个真实问题拆成一步一步的步骤？", "d": "拿到题目不知道从哪写起", "v": "怎么把一个真实问题拆成一步一步的步骤"},
        {"t": "为什么我的程序跑出来的结果总是差一点？", "d": "初值和边界到底怎么定", "v": "为什么我的程序跑出来的结果总是差一点"},
        {"t": "两个算法都能算对，怎么知道哪个更好？", "d": "步数多少能说明什么问题", "v": "两个算法都能算对怎么知道哪个更好"},
    ],
    "objectives": [
        "能说出算法的三个基本特征，分清算法与程序的区别",
        "能把一个真实问题分解成有输入、有处理、有输出的步骤",
        "能用变量和顺序、分支、循环三种结构，把算法写成可执行的伪代码",
        "能逐步跟踪并检验自己的算法，从初值、边界和结果三处定位错误",
    ],
    "objectives_plain": [
        "能说出算法的三个基本特征，分清算法与程序的区别",
        "能把一个真实问题分解成有输入、有处理、有输出的步骤",
        "能用变量和顺序、分支、循环三种结构，把算法写成可执行的伪代码",
        "能逐步跟踪并检验自己的算法，从初值、边界和结果三处定位错误",
    ],
    "standards": [
        {"content": "分析实际问题，设计算法并用程序语言实现。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》数据与算法 · 初中"},
        {"content": "能用变量、顺序、分支、循环等基本要素描述解决问题的过程，并对算法进行验证。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》数据与算法 · 初中"},
    ],
    "prereqs": [],
    "prereqs_name": "无（初中算法起点）",
    "prereqs_meta": "无",
    "leads_to": ["it-m-data-structures-basic"],
    "next_meta": "it-m-data-structures-basic",
    "section_images": ["assets/it-m-algorithm-design-fig1.webp", "assets/it-m-algorithm-design-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "一个必须反复做又不能出错的任务，怎样变成计算机能执行的方案？带着这个问题开始。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能自己设计一段算法并让它跑出正确结果。",
        "objectives": "看清四件事：说出算法特征、分解真实问题、用变量和三种结构写伪代码、检验自己的算法。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "算法是思路，程序是实现；算法要满足确定性、有穷性、可行性，还要说清输入和输出。",
        "lab-1": "点单步执行，盯住三个变量盒：最大值、下标、比较次数。比较次数和数据个数是什么关系？",
        "module-2": "变量是装数据的盒子，赋值会改变它的值；顺序、分支、循环，三种结构决定程序走哪条路。",
        "lab-2": "两种查找都跑一遍，把数据个数拖大，看看步数的差距怎么变化。",
        "worked-example": "四步走：看清问题、找漏洞、改正、逐行自查。重点查初值和循环边界。",
        "conceptest-1": "干扰项里藏着最常见的那几个错误想法，选完看清每一个解释。",
        "synthesis": "先挑出混进来的那张干扰卡片，再按「初始化 → 循环 → 判断计数 → 输出」的顺序拼。",
        "posttest": "换了成绩单和猜数字的新情境，看看你还能不能用上变量、分支和循环。",
        "summary": "用「输入、变量、循环、输出」四个词，把找最大值的算法讲给同桌听。",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是初中「数据与算法」领域长期空缺的入门一课。设计上不引入任何具体编程语言与产品，只用伪代码，把力气花在三件可操作的事上：用单步执行器把「变量的值会变化」这件事变成看得见的实时状态，用两种查找的步数对比把「算法有效率差异」变成可测量的数据，用拼装工作台让学生亲手把一段算法排出来再运行。价值取向上，全课以真实的数据处理需求驱动，强调算法先行、验证随后。",
    "plan_table": """| 1 | cover | 算法设计与程序实现 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：算法到底是什么？ | 起·前测（暴露直觉） |
| 5 | concept | 算法是明确有限的步骤，程序是它在语言里的实现 | 承·概念一 |
| 6 | interactive | 伪代码执行器：一步一步看变量的值怎么变 | 承·实验室一（变量与循环，状态可观察） |
| 7 | concept | 变量是装数据的盒子，三种结构决定走的路线 | 承·概念二 |
| 8 | interactive | 查找算法对比器：同样是找，步数差多少？ | 承·实验室二（算法效率可测量） |
| 9 | concept | 例题示范：一个错误算法是怎么被改对的 | 转·重难点突破（分步示范 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：把一段算法拼装出来并运行 | 合·迁移应用 |
| 12 | quiz | 后测：换一个情境，看看规律还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把自己讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：算法设计 / 程序实现 / 检验优化三栏标注\n- P5 算法与程序关系图（已生成）：真实问题 → 算法（输入·处理·输出）→ 程序\n- P7 三种基本控制结构对比图（已生成）：顺序 / 分支 / 循环的流程图\n- 若需补充：班级真实测量数据表的照片（用于情境引入）",
}
