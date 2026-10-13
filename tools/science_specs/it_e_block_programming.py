# -*- coding: utf-8 -*-
"""小学信息科技 · 积木式程序设计（G4）—— 补齐知识树「算法与程序」空缺

学科语气：信息科技 = 概念 + 动手并重。
本课只做两件真能上手的事：
  ① 核心模拟：把指令积木拼成一段程序 → 点运行 → 小角色一格一格走过去
     （每一步都高亮正在执行的那块积木；走不到终点/走出格子都会给出错因）
  ② 参数台：改「向前走几格」「向右转几次」，看同两块积木走出完全不同的路线
最后收口到一条可带走的规则：积木搭顺序，数字管多少，转身看自己，一步不能少。

说明：课件中的网格与积木均为教学示意图，不涉及任何真实软件界面、截图或商标。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-e-block-programming-fig1.webp'
F2 = './assets/it-e-block-programming-fig2.webp'

TTS = {
    "hero": "先请你想象一件事。屏幕左下角站着一个小角色，它看不见你，也猜不到你的想法；右上角插着一面小旗。你要怎么告诉它，才能让它走到小旗那里？你只能一块积木一块积木地告诉它：先向前走，再向左转，再向前走。像这样按顺序排好的一串指令，就叫程序。今天这节课，我们要亲手把积木拼起来，看着小角色一格一格走过去。",
    "problem-anchor": "在开始之前，先选一个你最想弄明白的问题。是想知道积木要按什么顺序拼，还是想知道同样的指令为什么换一下顺序就走不到，又或者你想弄明白积木上的数字有什么用，再或者你想学会在小角色走不到终点的时候，找出是哪一块积木放错了。选好了，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出程序就是一串有先后顺序的指令，计算机会从第一块开始，一块一块执行。第二，能把向前走、向左转、向右转这三类积木拼成一段程序。第三，能通过改积木上的数字，让小角色走出不一样的路线。第四，能在小角色走不到终点的时候，找出哪一块积木放错了，并把它改过来。",
    "pretest": "先做三道小题，用你现在的想法选就行。选完马上能看到解释，选错了也没关系，正好知道该重点听哪里。",
    "module-1": "先说什么叫程序。你想让小角色走到小旗那里，就把要做的事一块积木一块积木排起来：向前走一格，再向前走一格，然后向左转，再向前走。这一串排好的积木，就是一段程序。要记住三件事：第一，一块积木就是一个动作；第二，计算机从最上面一块开始，一块接一块往下做；第三，顺序一旦变了，小角色走到的地方就变了。计算机不会看着办，它只会严格按顺序执行。",
    "lab-1": "光看还不够，我们自己动手拼一次。小角色站在左下角，头朝着右边；小旗在它的右上方。请在下面点积木，把程序拼出来，然后点运行，看它一格一格走过去。每走一步，正在执行的那块积木会亮起来，你可以清清楚楚看到，它走的每一步，都对应程序里的一块积木。",
    "module-2": "接下来看看积木上的数字。有的积木上写着向前走三格，那个三就是参数；有的积木上写着向右转两次，那个二也是参数。参数一变，走出来的路线就完全不一样。还要特别记住转向：向左转和向右转，都是在它自己现在朝向的基础上转九十度，不是转到屏幕的左边或者右边。它头朝下的时候向右转，转完就朝左了。",
    "lab-2": "现在请你当一次小驾驶员。下面有两个滑块，一个控制向前走几格，一个控制向右转几次。请你调一调，让小角色正好站在小旗上，而且头朝上。调的时候注意：这两块积木的参数要一起配，只改一个常常到不了。",
    "worked-example": "我们一起来读一段程序。起点是左下角，头朝右。程序是：向前走一格，向前走一格，向左转，向前走一格，向前走一格。第一步，先看清起点在哪、头朝哪边。第二步，一块一块顺着走：前两块都朝右，它就向右挪了两格。第三步，遇到转向要停下来想一想：向左转以后，它朝上了。第四步，把结果说出来：它最后停在起点右上方两格的地方，头朝上；再跟小旗比一比，就知道到没到。",
    "conceptest-1": "接下来用三个容易弄错的说法考考你。请仔细读每一个选项，选完再看解释。",
    "synthesis": "最后一个任务交给你。这段程序本来走不到小旗：前三块是向前走一格，接着是向右转，再向前走两格。请你点一下那块转向的积木，把它换成向左转，再点运行看看。只换了一块积木，小角色走出来的路线就完全不同了。想一想，这是为什么。",
    "posttest": "最后一轮，换几个新的小情境来考考你。这次会出现扫地机器人、遥控小车，还有一段总是差一点的程序，看看你能不能把学到的规则用上去。",
    "summary": "这节课我们记住三句话。第一句，程序就是一串有先后顺序的指令，计算机从第一块开始，一块一块执行。第二句，积木上的数字是参数，参数改了，路线就变了；转向是相对它自己朝哪边。第三句，走不到终点的时候，先数一数前进的格数够不够，再看转向对不对，然后只改那一块错的积木。回到开头那个问题：小角色猜不到你的心思，但只要你把积木排对、数字填对，它就会一格一格走到你要的地方。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：在方格纸上画出起点、小旗和一条路线，再写出对应的积木程序，至少六块。第二层能力应用，动手做：先自己在纸上走一遍一段程序的路线，再上机运行验证，看看和你画的一样不一样。第三层迁移挑战，选做：设计一个需要绕过障碍的任务，写出程序，并说明你为什么把转向的积木放在那一步。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是学它之前要先会的，右边是学会之后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续学的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 程序就是一串指令积木", "lab-1": "动手一 拼程序让小角色走起来",
    "module-2": "概念二 参数与转向", "lab-2": "动手二 调参数看路线",
    "worked-example": "例题讲解 读出程序走到哪", "conceptest-1": "概念测试",
    "synthesis": "综合任务 只换一块积木", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

CUSTOM_JS = r"""
/* ============================================================
   it-e-block-programming 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 网格舞台工厂 bpScene()：铺格子 + 终点小旗 + 可旋转的小角色
   3) 动手一：拼积木程序 → 运行 / 单步 → 小角色一格一格走（逐步高亮）
   4) 动手二：参数滑块（走几格 / 转几次）→ 实时位置与朝向
   5) 综合任务：点一下转向积木换方向，再运行验证
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
    '.bp-wrap{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(210px,0.85fr);gap:14px;align-items:start;}' +
    '@media(max-width:760px){.bp-wrap{grid-template-columns:1fr;}}' +
    '.bp-stage{position:relative;width:100%;aspect-ratio:5/4;border-radius:14px;border:1px solid var(--line);' +
    'background-color:var(--card);' +
    'background-image:linear-gradient(to right, rgb(var(--paper-rgb) / 45%) 1px, transparent 1px),' +
    'linear-gradient(to bottom, rgb(var(--paper-rgb) / 45%) 1px, transparent 1px);' +
    'background-size:20% 100%, 100% 25%;overflow:hidden;}' +
    '.bp-goal{position:absolute;display:grid;place-items:center;font-size:26px;background:var(--warm-soft);' +
    'box-shadow:inset 0 0 0 2px rgb(var(--warm-rgb) / 75%);border-radius:6px;}' +
    '.bp-goal.bp-hit{box-shadow:inset 0 0 0 3px var(--brand-2);background:var(--accent-soft);}' +
    '.bp-actor{position:absolute;display:grid;place-items:center;width:34px;height:34px;border-radius:50%;' +
    'background:var(--brand);color:#fff;font-size:17px;line-height:1;' +
    'transition:left .38s cubic-bezier(.34,1.2,.5,1),top .38s cubic-bezier(.34,1.2,.5,1),transform .3s ease;' +
    'box-shadow:0 3px 10px rgb(var(--brand-rgb) / 35%);}' +
    '.bp-side{display:flex;flex-direction:column;gap:10px;}' +
    '.bp-prog{display:flex;flex-direction:column;gap:6px;min-height:64px;padding:10px;border-radius:12px;' +
    'background:var(--bg-subtle);border:1px dashed rgb(var(--paper-rgb) / 40%);}' +
    '.bp-row{display:flex;align-items:center;gap:8px;padding:8px 10px;border-radius:9px;background:var(--card);' +
    'border:1px solid var(--line-subtle);font-size:14px;}' +
    '.bp-row.run{border-color:var(--brand);background:var(--brand-soft);box-shadow:0 0 0 3px rgb(var(--brand-rgb) / 16%);}' +
    '.bp-row .bp-n{flex-shrink:0;width:20px;height:20px;border-radius:50%;display:grid;place-items:center;' +
    'background:var(--brand);color:#fff;font-size:11px;font-weight:800;}' +
    '.bp-row .bp-t{flex:1;min-width:0;}' +
    '.bp-del{border:none;background:transparent;color:var(--muted);cursor:pointer;font-size:13px;padding:2px 6px;}' +
    '.bp-empty{color:var(--muted);font-size:13px;margin:2px 0;}' +
    '.bp-block{width:100%;text-align:left;font-size:14px;font-weight:700;}' +
    /* 补齐可点控件的边框与选中态：库内部分颜色写法会被浏览器整条丢弃 */
    '.choice{border:1.5px solid rgb(var(--brand-rgb) / 32%);background:var(--card);}' +
    '.choice:hover{background:var(--brand-soft);border-color:rgb(var(--brand-rgb) / 55%);}' +
    '.choice.selected{border-color:var(--brand);background:rgb(var(--brand-rgb) / 13%);box-shadow:0 0 0 3px rgb(var(--brand-rgb) / 16%);}' +
    '.sort-item{border:1.5px solid rgb(var(--brand-rgb) / 30%);background:var(--card);}' +
    '.kid-note{border-color:rgb(var(--warm-rgb) / 80%);}';
  document.head.appendChild(st);

  /* ---------- 2. 网格舞台工厂 ---------- */
  var DIRV = [[1, 0], [0, 1], [-1, 0], [0, -1]];   /* 0 右 / 1 上 / 2 左 / 3 下 */
  var DIRN = ['朝右', '朝上', '朝左', '朝下'];

  function bpScene(o) {
    var stage = document.getElementById(o.stageId);
    if (!stage) return null;
    var COLS = o.cols, ROWS = o.rows;
    var gc = document.createElement('div');
    gc.className = 'bp-goal';
    gc.style.left = (o.goal.x * 100 / COLS) + '%';
    gc.style.top = ((ROWS - 1 - o.goal.y) * 100 / ROWS) + '%';
    gc.style.width = (100 / COLS) + '%';
    gc.style.height = (100 / ROWS) + '%';
    gc.textContent = '🏁';
    stage.appendChild(gc);
    var act = document.createElement('div');
    act.className = 'bp-actor';
    act.textContent = '➤';
    stage.appendChild(act);
    var api = {
      cols: COLS, rows: ROWS, goal: o.goal,
      place: function (x, y, dir) {
        act.style.left = ((x + 0.5) * 100 / COLS) + '%';
        act.style.top = ((ROWS - 1 - y + 0.5) * 100 / ROWS) + '%';
        act.style.transform = 'translate(-50%,-50%) rotate(' +
          (dir === 1 ? -90 : dir === 2 ? 180 : dir === 3 ? 90 : 0) + 'deg)';
      },
      hit: function (flag) { gc.classList.toggle('bp-hit', !!flag); }
    };
    api.place(o.start ? o.start.x : 0, o.start ? o.start.y : 0, o.start ? o.start.dir : 0);
    return api;
  }

  /* 差多少格的一句人话 */
  function gapText(pos, goal) {
    var dx = goal.x - pos.x, dy = goal.y - pos.y, parts = [];
    if (dx > 0) parts.push('向右走 ' + dx + ' 格');
    if (dx < 0) parts.push('向左走 ' + (-dx) + ' 格');
    if (dy > 0) parts.push('向上走 ' + dy + ' 格');
    if (dy < 0) parts.push('向下走 ' + (-dy) + ' 格');
    return parts.length ? ('它还差：' + parts.join('，再') + '。') : '';
  }

  /* ---------- 3. 动手一：拼程序 → 一格一格走 ---------- */
  var sc1 = bpScene({ stageId: 'bp1-stage', cols: 5, rows: 4, goal: { x: 3, y: 2 } });
  if (sc1) {
    var K1 = { F: '向前走 1 格', L: '向左转', R: '向右转' };
    var P1 = [], pos1 = { x: 0, y: 0, dir: 0 }, idx1 = 0, act1 = -1, t1 = null;
    var prog1 = document.getElementById('bp1-prog');
    var out1 = document.getElementById('bp1-out');
    var cnt1 = document.getElementById('bp1-count');

    function render1() {
      prog1.innerHTML = '';
      if (!P1.length) {
        var e = document.createElement('p');
        e.className = 'bp-empty';
        e.textContent = '程序还是空的。点左边的积木，把它加进来。';
        prog1.appendChild(e);
      }
      P1.forEach(function (k, i) {
        var row = document.createElement('div');
        row.className = 'bp-row' + (i === act1 ? ' run' : '');
        var n = document.createElement('span');
        n.className = 'bp-n'; n.textContent = (i + 1);
        var tt = document.createElement('span');
        tt.className = 'bp-t'; tt.textContent = K1[k];
        var d = document.createElement('button');
        d.className = 'bp-del'; d.textContent = '✕';
        d.setAttribute('aria-label', '删掉第 ' + (i + 1) + ' 块积木');
        d.addEventListener('click', function () {
          if (t1 !== null) return;
          P1.splice(i, 1); reset1(); render1();
        });
        row.appendChild(n); row.appendChild(tt); row.appendChild(d);
        prog1.appendChild(row);
      });
      cnt1.textContent = P1.length + ' 块';
    }

    function reset1() {
      pos1 = { x: 0, y: 0, dir: 0 };
      idx1 = 0; act1 = -1;
      sc1.place(0, 0, 0); sc1.hit(false);
    }

    function step1() {
      if (idx1 >= P1.length) return false;
      var k = P1[idx1];
      if (k === 'L') pos1.dir = (pos1.dir + 1) % 4;
      else if (k === 'R') pos1.dir = (pos1.dir + 3) % 4;
      else {
        var d = DIRV[pos1.dir], nx = pos1.x + d[0], ny = pos1.y + d[1];
        if (nx < 0 || nx >= sc1.cols || ny < 0 || ny >= sc1.rows) {
          act1 = idx1; idx1++;
          sc1.place(pos1.x, pos1.y, pos1.dir); render1();
          out1.className = 'result error';
          out1.innerHTML = '<strong>小角色走出格子了。</strong>它现在' + DIRN[pos1.dir] +
            '，再往前一步就没有格子了。<br><span style="color:var(--muted)">常见错误：把转向的那块积木放错了位置，' +
            '或者前进的块数多了一块——它就会朝一个方向一直走，越走越偏。</span>';
          return false;
        }
        pos1.x = nx; pos1.y = ny;
      }
      act1 = idx1; idx1++;
      sc1.place(pos1.x, pos1.y, pos1.dir); render1();
      if (idx1 >= P1.length) { finish1(); return false; }
      return true;
    }

    function finish1() {
      stop1();
      if (pos1.x === sc1.goal.x && pos1.y === sc1.goal.y) {
        sc1.hit(true);
        out1.className = 'result';
        out1.innerHTML = '<strong>🎉 走到小旗啦！</strong>你一共用了 ' + P1.length +
          ' 块积木。再回头看一遍程序：小角色走的每一步，都对应里面的一块积木，一块都没有跳过。';
      } else {
        sc1.hit(false);
        out1.className = 'result warn';
        out1.innerHTML = '<strong>程序执行完了，小角色没有到小旗那里。</strong>' + gapText(pos1, sc1.goal) +
          '<br><span style="color:var(--muted)">常见错误：只数了「向前走」的块数，忘了转向已经让它换了一个方向。</span>';
      }
    }

    function stop1() { if (t1 !== null) { clearInterval(t1); t1 = null; } }

    document.querySelectorAll('[data-bp-add]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (t1 !== null) return;
        P1.push(b.dataset.bpAdd);
        if (idx1 > 0) { reset1(); }
        render1();
      });
    });
    document.getElementById('bp1-run').addEventListener('click', function () {
      if (t1 !== null) { stop1(); return; }
      if (!P1.length) {
        out1.className = 'result warn';
        out1.textContent = '程序里还没有积木，先加几块再运行。';
        return;
      }
      reset1();
      out1.className = 'result warn';
      out1.textContent = '正在一块一块执行……注意看哪块积木亮起来了。';
      t1 = setInterval(function () { if (!step1()) stop1(); }, 520);
    });
    document.getElementById('bp1-step').addEventListener('click', function () {
      if (t1 !== null) return;
      if (!P1.length) {
        out1.className = 'result warn';
        out1.textContent = '程序里还没有积木，先加几块。';
        return;
      }
      if (idx1 >= P1.length) reset1();
      out1.className = 'result warn';
      out1.textContent = '单步执行：亮起来的那一块，就是刚刚执行过的。';
      step1();
    });
    document.getElementById('bp1-clear').addEventListener('click', function () {
      stop1(); P1 = []; reset1(); render1();
      out1.className = 'result warn';
      out1.textContent = '程序清空了。重新来一遍吧。';
    });
    render1();
  }

  /* ---------- 4. 动手二：参数滑块 ---------- */
  var sc2 = bpScene({ stageId: 'bp2-stage', cols: 5, rows: 4, goal: { x: 3, y: 0 } });
  if (sc2) {
    var rN = document.getElementById('bp2-n');
    var rT = document.getElementById('bp2-t');
    var vN = document.getElementById('bp2-nv');
    var vT = document.getElementById('bp2-tv');
    var vP = document.getElementById('bp2-pos');
    var vD = document.getElementById('bp2-dir');
    var out2 = document.getElementById('bp2-out');

    function render2() {
      var n = parseInt(rN.value, 10), t = parseInt(rT.value, 10);
      var x = n, y = 0, dir = (0 + 3 * t) % 4;
      vN.textContent = n + ' 格';
      vT.textContent = t + ' 次';
      sc2.place(x, y, dir);
      vP.textContent = '（' + x + '，' + y + '）';
      vD.textContent = DIRN[dir];
      var atGoal = (x === sc2.goal.x && y === sc2.goal.y);
      sc2.hit(atGoal && dir === 1);
      out2.className = 'result ' + ((atGoal && dir === 1) ? '' : 'warn');
      out2.innerHTML = '<strong>现在两块积木的参数是：向前走 ' + n + ' 格，向右转 ' + t + ' 次。</strong>' +
        '小角色停在 ' + vP.textContent + '，' + DIRN[dir] + '。<br>' +
        ((atGoal && dir === 1)
          ? '🎉 正好站在小旗上，而且头朝上——两个参数一起配对了！'
          : (atGoal
            ? '<span style="color:var(--muted)">位置对了，但它的头还' + DIRN[dir] +
              '。再改一改「向右转」的次数试试。</span>'
            : '<span style="color:var(--muted)">还没站到小旗上。常见错误：只调一个滑块就下结论——' +
              '这两块积木的参数要一起配。</span>'));
    }
    rN.addEventListener('input', render2);
    rT.addEventListener('input', render2);
    render2();
  }

  /* ---------- 5. 综合任务：换一块积木 ---------- */
  var sc3 = bpScene({ stageId: 'bp3-stage', cols: 5, rows: 4, goal: { x: 3, y: 2 } });
  if (sc3) {
    var K3 = { F: '向前走 1 格', L: '向左转', R: '向右转' };
    var P3 = ['F', 'F', 'F', 'R', 'F', 'F'];
    var pos3 = { x: 0, y: 0, dir: 0 }, idx3 = 0, act3 = -1, t3 = null;
    var prog3 = document.getElementById('bp3-prog');
    var out3 = document.getElementById('bp3-out');

    function render3() {
      prog3.innerHTML = '';
      P3.forEach(function (k, i) {
        var row = document.createElement('div');
        row.className = 'bp-row' + (i === act3 ? ' run' : '');
        var n = document.createElement('span');
        n.className = 'bp-n'; n.textContent = (i + 1);
        var tt = document.createElement('span');
        tt.className = 'bp-t'; tt.textContent = K3[k];
        row.appendChild(n); row.appendChild(tt);
        if (k === 'L' || k === 'R') {
          var sw = document.createElement('button');
          sw.className = 'bp-del';
          sw.textContent = (k === 'R' ? '换成向左转' : '换成向右转');
          sw.style.fontSize = '12px';
          sw.addEventListener('click', function () {
            if (t3 !== null) return;
            P3[i] = (k === 'R' ? 'L' : 'R');
            reset3(); render3();
            out3.className = 'result warn';
            out3.textContent = '已经换好了。点「运行这段程序」看看小角色这回走到哪里。';
          });
          row.appendChild(sw);
        }
        prog3.appendChild(row);
      });
    }

    function reset3() {
      pos3 = { x: 0, y: 0, dir: 0 };
      idx3 = 0; act3 = -1;
      sc3.place(0, 0, 0); sc3.hit(false);
    }

    function step3() {
      if (idx3 >= P3.length) return false;
      var k = P3[idx3];
      if (k === 'L') pos3.dir = (pos3.dir + 1) % 4;
      else if (k === 'R') pos3.dir = (pos3.dir + 3) % 4;
      else {
        var d = DIRV[pos3.dir], nx = pos3.x + d[0], ny = pos3.y + d[1];
        if (nx < 0 || nx >= sc3.cols || ny < 0 || ny >= sc3.rows) {
          act3 = idx3; idx3++;
          sc3.place(pos3.x, pos3.y, pos3.dir); render3();
          out3.className = 'result error';
          out3.innerHTML = '<strong>小角色走出格子了。</strong>它现在' + DIRN[pos3.dir] +
            '。<br><span style="color:var(--muted)">常见错误：转向的积木方向反了——' +
            '「向右转」和「向左转」只差一个字，走出来的路线却完全相反。</span>';
          return false;
        }
        pos3.x = nx; pos3.y = ny;
      }
      act3 = idx3; idx3++;
      sc3.place(pos3.x, pos3.y, pos3.dir); render3();
      if (idx3 >= P3.length) { finish3(); return false; }
      return true;
    }

    function finish3() {
      stop3();
      if (pos3.x === sc3.goal.x && pos3.y === sc3.goal.y) {
        sc3.hit(true);
        out3.className = 'result';
        out3.innerHTML = '<strong>🎉 到小旗了！</strong>和刚才比一比：只有那<strong>一块</strong>转向积木换了方向，' +
          '整条路线就完全不同了。可见转向积木摆在哪一步、朝哪边转，都要想清楚。';
      } else {
        sc3.hit(false);
        out3.className = 'result warn';
        out3.innerHTML = '<strong>还是没到小旗。</strong>' + gapText(pos3, sc3.goal) +
          '<br><span style="color:var(--muted)">常见错误：只盯着「向前走」的块数，忘了转向决定的是它往哪边走。' +
          '先看它每一步朝哪边，再数格数。</span>';
      }
    }

    function stop3() { if (t3 !== null) { clearInterval(t3); t3 = null; } }

    document.getElementById('bp3-run').addEventListener('click', function () {
      if (t3 !== null) { stop3(); return; }
      reset3();
      out3.className = 'result warn';
      out3.textContent = '正在一块一块执行……';
      t3 = setInterval(function () { if (!step3()) stop3(); }, 520);
    });
    document.getElementById('bp3-reset').addEventListener('click', function () {
      stop3(); reset3(); render3();
      out3.className = 'result warn';
      out3.textContent = '小角色回到起点了。';
    });
    render3();
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：程序里的指令，是怎么被执行的？", TTS["pretest"], [
        {"q": "积木程序里的指令，计算机是怎么执行的？",
         "options": [("从最上面一块开始，一块接一块按顺序执行", True),
                     ("看哪一块重要就先执行哪一块", False),
                     ("所有积木同时一起执行", False)],
         "explain": "按顺序一块接一块执行，是程序最基本的工作方式。"
                    "<strong>错因提醒：</strong>常见错误是以为计算机能自己挑重点——它不会看着办，"
                    "只会严格按你排好的顺序来。"},
        {"q": "小角色头朝右边站着，执行「向右转」以后，它朝哪边？",
         "options": [("朝下", True), ("朝左", False), ("还是朝右", False)],
         "explain": "转向是在它自己现在朝向的基础上转九十度：头朝右向右转，就变成朝下。"
                    "<strong>错因提醒：</strong>容易把你自己面朝的方向和它的方向搞混——"
                    "它转的是自己，不是你的左右。"},
        {"q": "积木上写着「向前走 3 格」，把它改成 2 会怎么样？",
         "options": [("走得短一些，最后停的位置不一样了", True),
                     ("走得慢一些，停的位置还是一样", False),
                     ("什么都不会改变", False)],
         "explain": "数字是这块积木的参数，参数一变，效果就变。"
                    "<strong>错因提醒：</strong>不少同学误认为这个数字只管快慢——"
                    "它决定的是走多少格，不是走多快。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "程序：一串按顺序排好的指令积木", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们平时请别人帮忙，说一句「把书递过来」就够了（And）；可计算机不会猜，也看不见你的表情，它只认一条一条写清楚的指令（But）；所以我们要学会把动作拼成积木、按顺序排好，这就叫程序（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">把要做的事，一块积木一块积木按顺序排起来，计算机就从最上面一块开始，<strong>一块接一块地做下去</strong>。</p>
        <div class="grid grid-3">
          <div class="inner-card"><p><strong>① 一块积木一个动作</strong></p><p style="color:var(--muted)">「向前走」「向左转」「向右转」，各是一块积木。</p></div>
          <div class="inner-card"><p><strong>② 从上到下执行</strong></p><p style="color:var(--muted)">计算机从第一块开始，做完一块才做下一块。</p></div>
          <div class="inner-card"><p><strong>③ 顺序变了结果就变</strong></p><p style="color:var(--muted)">同样几块积木，换一下顺序，走到的地方完全不同。</p></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="积木指令序列与小角色按格行走示意图：三块积木依次执行，小角色在方格地图上走到终点小旗">
          <figcaption>示意图：左边一串积木从上到下执行，右边小角色一格一格走过去——每一步都对应上面的一块积木</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🤖</span><div><strong>小提示：</strong>计算机不会「看着办」。排好的积木，它一定照做；没排的，它一定不做。所以想让小角色走到小旗那里，每一步都要你自己写清楚。</div></div>
{insight_box([
    {"lens": "看见它", "text": "程序的样子很朴素：一列积木，从上往下。可小角色走的每一格，都能在里头找到对应的一块。"},
    {"lens": "解释它", "text": "为什么顺序这么要紧？因为每一块积木都改变了小角色的状态——位置或者朝向。前一块变了，后一块的结果自然跟着变。"},
    {"lens": "迁移它", "text": "生活里的很多事也是这样排的：洗衣机先注水再转桶，如果先转桶，衣服还是干的。顺序，就是事情能不能做成的关键。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：拼出积木程序，让小角色走到小旗", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">小角色站在左下角、头朝右边，小旗在它的右上方。点积木加入程序，再点「运行」，看它一格一格走过去。</p>
        <div class="lab-panel">
          <div class="bp-wrap">
            <div>
              <div class="bp-stage" id="bp1-stage"></div>
              <div class="lab-readout">
                <div class="readout-cell"><span class="k">已用积木</span><span class="v" id="bp1-count">0 块</span></div>
              </div>
              <div class="flex-row" style="margin-top:8px">
                <button class="choice" id="bp1-run" style="text-align:center">▶ 运行程序</button>
                <button class="choice" id="bp1-step" style="text-align:center">单步执行</button>
                <button class="choice" id="bp1-clear" style="text-align:center">清空重来</button>
              </div>
            </div>
            <div class="bp-side">
              <div style="font-weight:700;font-size:14px">① 点积木，加进程序</div>
              <button class="choice bp-block" data-bp-add="F">➤ 向前走 1 格</button>
              <button class="choice bp-block" data-bp-add="L">↰ 向左转</button>
              <button class="choice bp-block" data-bp-add="R">↱ 向右转</button>
              <div style="font-weight:700;font-size:14px;margin-top:4px">② 你排出来的程序</div>
              <div class="bp-prog" id="bp1-prog"></div>
            </div>
          </div>
          <p class="result warn" id="bp1-out" style="margin-top:12px">先加一块积木，再点运行试试。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>看仔细：</strong>执行到哪一块，哪一块就会亮起来。小角色走的每一步，都能在程序里找到那张亮起来的积木——这就是「顺序执行」。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "积木上的数字是参数，转向看的是它自己", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">同一块积木，上面填的数字不一样，效果就完全不同。这个数字叫<strong>参数</strong>。</p>
        <div class="step-grid">
          <div class="step"><span class="n">数</span><div><strong>向前走 N 格</strong>：参数是「走多少格」。填 1 和填 3，走出来的距离不一样。</div></div>
          <div class="step"><span class="n">转</span><div><strong>向左转 / 向右转</strong>：一块积木转一次九十度。转两次，就是又转了一次。</div></div>
          <div class="step"><span class="n green">己</span><div><strong>转向是「相对自己」</strong>：以它现在头的朝向为准，不是屏幕的左右。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="同样的积木、不同的顺序与参数带来的两种结果对照示意图：一边到达终点，一边走偏出格">
          <figcaption>示意图：同样几块积木，只是换了顺序或多走了一格，一边走到小旗，一边走偏出了格子</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">以为「向右转」就是<strong>转到屏幕的右边</strong>。其实小角色头朝下的时候向右转，转完是朝左——它转的永远是自己。判断时先看它的头朝哪边，再想往哪边转。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>积木搭顺序，数字管多少，转身看自己，一步不能少。</div></div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：调一调参数，看路线怎么变", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">现在程序里只有两块积木：一块「向前走 N 格」，一块「向右转 X 次」。拖动滑块，看小角色停在哪里、头朝哪边。</p>
        <div class="lab-panel">
          <div class="bp-wrap">
            <div>
              <div class="bp-stage" id="bp2-stage"></div>
              <div class="lab-readout">
                <div class="readout-cell"><span class="k">最后位置</span><span class="v" id="bp2-pos">（0，0）</span></div>
                <div class="readout-cell"><span class="k">头的朝向</span><span class="v green" id="bp2-dir">朝右</span></div>
              </div>
            </div>
            <div class="bp-side">
              <div class="slider-row" style="margin-top:0">
                <label for="bp2-n">向前走</label>
                <input type="range" id="bp2-n" min="1" max="4" step="1" value="1">
                <span style="font-weight:800;min-width:52px;text-align:right" id="bp2-nv">1 格</span>
              </div>
              <div class="slider-row" style="margin-top:0">
                <label for="bp2-t">向右转</label>
                <input type="range" id="bp2-t" min="0" max="3" step="1" value="0">
                <span style="font-weight:800;min-width:52px;text-align:right" id="bp2-tv">0 次</span>
              </div>
              <div class="inner-card" style="margin:0">
                <p style="margin:0"><strong>小挑战</strong></p>
                <p style="color:var(--muted);margin:6px 0 0">调出两个参数，让小角色正好站在小旗上，而且头朝上。</p>
              </div>
            </div>
          </div>
          <p class="result warn" id="bp2-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💡</span><div><strong>想一想：</strong>向右转 3 次，和向左转 1 次，转出来的朝向一样吗？动手试出来以后，你就明白了转向是「一圈一圈绕着转」的。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：读出这段程序，它会走到哪里？", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>小角色在左下角，头朝右。程序是：① 向前走 1 格 ② 向前走 1 格 ③ 向左转 ④ 向前走 1 格 ⑤ 向前走 1 格。它会走到哪里？头朝哪边？</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先看清起点：</strong>找到它站在哪一格、头朝哪边——左下角，朝右。转向的积木怎么转，全看这一步。</div></div>
          <div class="step"><span class="n">2</span><div><strong>一块一块顺着走：</strong>前两块都是「向前走」，它头朝右，所以是向右挪两格。</div></div>
          <div class="step"><span class="n">3</span><div><strong>遇到转向就停下来想：</strong>「向左转」以后，它由朝右变成了朝上，方向变了，后面两块走的就不是横的，而是竖的。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>说出结果，再和终点比一比：</strong>它最后停在起点右上方两格的位置，头朝上。心里有这个点，就知道小旗在不在那里了。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">只数了「向前走」的块数，算出「一共走了四格」，却忘了中间那块转向积木已经让它换了方向。最常见的做法是：<strong>一边走一边在心里画</strong>，或者干脆在方格纸上画一遍。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三种说法，错在哪里", TTS["conceptest-1"], [
        {"q": "小角色在起点、头朝右，小旗在它右边 3 格。下面哪段程序能让它走到小旗？",
         "options": [("向前走 1 格，向前走 1 格，向前走 1 格", True),
                     ("向左转，再向前走 3 格", False),
                     ("向右转 3 次", False)],
         "explain": "它本来就朝右，直接向前走三格就到了。"
                    "<strong>错因提醒：</strong>常见错误是习惯性先加一块转向积木——方向没搞清，越转越偏。"},
        {"q": "「向左转」和「向右转」这两块积木的意思是：",
         "options": [("在它自己现在朝向的基础上转九十度，一个往左一个往右", True),
                     ("转到屏幕的左边或者右边", False),
                     ("只有头朝右的时候才管用", False)],
         "explain": "转向参照的是它自己的头朝哪边，跟屏幕的左右无关。"
                    "<strong>错因提醒：</strong>把它当成「转到屏幕某一边」，是这一课最容易搞混的地方。"},
        {"q": "程序运行时，小角色走出格子了。最可能的原因是：",
         "options": [("转向的积木放错位置，或者前进的格数太多，它朝一个方向一直走", True),
                     ("计算机坏了", False),
                     ("积木的颜色选错了", False)],
         "explain": "走出格子说明它在某个方向走过头了，回到程序里数一数格数、看一眼转向就能找到。"
                    "<strong>错因提醒：</strong>别急着把程序全删掉——错通常只在一块积木上。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：只换一块积木，让它走到小旗", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">下面这段程序走不到小旗。请你点一下那块转向积木，把它换成另一个方向，再运行看看。</p>
        <div class="lab-panel">
          <div class="bp-wrap">
            <div>
              <div class="bp-stage" id="bp3-stage"></div>
              <div class="flex-row" style="margin-top:8px">
                <button class="choice" id="bp3-run" style="text-align:center">▶ 运行这段程序</button>
                <button class="choice" id="bp3-reset" style="text-align:center">回到起点</button>
              </div>
            </div>
            <div class="bp-side">
              <div style="font-weight:700;font-size:14px">这段程序（点转向积木可以换方向）</div>
              <div class="bp-prog" id="bp3-prog"></div>
            </div>
          </div>
          <p class="result warn" id="bp3-out" style="margin-top:12px">先点「运行这段程序」，看看它现在走到哪里。</p>
        </div>
        <div class="inner-card">
          <p><strong>改完以后，说给同桌听：</strong></p>
          <p style="color:var(--muted)">为什么只换了一块积木，走出来的路线就完全不一样了？如果换成「向左转」还是走不到，你会先检查哪一块？</p>
          <textarea id="syn-answer" rows="3" placeholder="因为转向决定了它后面往哪边走……我会先检查……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个情境，规则还在不在", TTS["posttest"], [
        {"q": "扫地机器人的程序是「向前走 5 格，向右转，向前走 5 格」。它总撞到同一面墙，最要紧的是改哪里？",
         "options": [("先数一数前进的格数是不是太多，再看转向放的位置对不对", True),
                     ("把它的速度调快一点", False),
                     ("把程序全部删掉重写一遍", False)],
         "explain": "走过头或转向不对，都会让它一头撞上去。回到程序里数格数、看转向就能改对。"
                    "<strong>错因提醒：</strong>遇到不对就全部重写，是常见错误——程序调试只要改动那一块。"},
        {"q": "遥控小车的程序是「向前走 3 格，向左转，向前走 2 格」。如果把「向左转」这一块删掉，小车会：",
         "options": [("一直朝原来的方向走，去不了原来的那个地方", True),
                     ("照样能到原来那里", False),
                     ("立刻停下来不动", False)],
         "explain": "少了转向，后面那块「向前走」就变成朝原来的方向走，位置全变了。"
                    "<strong>错因提醒：</strong>别误认为「少一块没多大关系」——程序里少一块，结果往往就不同了。"},
        {"q": "你排的程序每次都让小角色停在离小旗差一格的地方。最好的下一步是：",
         "options": [("单步执行，一块一块看它在哪一步走偏了，再改那一块", True),
                     ("随便再加一块积木试试运气", False),
                     ("把积木的顺序全部颠倒过来", False)],
         "explain": "单步执行能让每一步都看得见，最容易找出是哪一块的问题。"
                    "<strong>错因提醒：</strong>「碰运气改一改」听起来省事，其实更慢——先看清在哪一步出错，再动手。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把积木程序讲清楚", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>程序是什么：</strong>一串有先后顺序的指令积木，计算机从第一块开始，一块一块执行。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>参数与转向：</strong>积木上的数字管「多少」；转向是在它自己现在朝向的基础上转九十度。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>走不到怎么办：</strong>先数格数，再看转向，找到那一块错的积木改掉——不要全部重写。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那个小角色：</strong>它猜不到你的心思，却也从不偷懒。你把积木排对、数字填对，它就一格一格，走到你要它去的地方——这就是程序。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「积木、顺序、参数」这三个词，说清楚你是怎么让小角色走到小旗那里的。</p>
          <p style="color:var(--muted)">再动一动手：<strong>画出来</strong>——在方格纸上画出一条路线，在每一步旁边写上对应的积木。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "在方格纸上画出起点、小旗和一条路线，再写出对应的积木程序，至少六块。",
            "说出「向前走 N 格」里的 N 是什么意思，并解释为什么改了它，路线就变了。",
        ],
        [
            "读一段别人写的程序，先在纸上走一遍、画出它会走到哪一格，再上机运行验证，看看和你画的一样不一样。",
            "用两三句话记下你一次走不到终点的经历：错在哪一块积木上，你后来是怎么改的。",
        ],
        [
            "设计一个需要绕过障碍物的任务：画出地图，写出程序，并说明你为什么把转向的积木放在那一步。",
            "如果想让它「一直往前走，直到碰到墙才停」，现在的积木够用吗？说说你的想法。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-e-block-programming",
    "node_id": "it-e-block-programming",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 小学",
    "title": "积木式程序设计",
    "name_en": "Block-Based Programming",
    "grade": 4,
    "grade_cn": "四年级",
    "domain": "algorithm-programming",
    "domain_cn": "算法与程序",
    "lesson_type": "concept-practice",
    "version": "1.0.0",
    "description": "面向小学四年级：知道程序就是一串有先后顺序的指令积木、计算机按顺序一块一块执行；能把前进与转向积木拼成程序并运行；能通过修改参数改变小角色走的路线；能在走不到终点时找到那一块错放的积木并改正。",
    "tags": ["积木编程", "顺序执行", "指令积木", "参数", "图形化编程"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》小学「算法与程序」——使用图形化编程工具实现简单算法。",
    "hero_question": "小角色看不见你，也猜不到你的想法——你该怎么让它走到小旗那里？",
    "hero_alt": "积木式程序设计知识结构图：指令积木、按顺序执行、参数与调试修正三栏",
    "hero_caption": "积木式程序设计：积木搭顺序 · 数字管多少 · 转身看自己 · 一步不能少",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的动手活动都会围着它转。",
    "anchor_choices": [
        {"t": "积木要按什么顺序拼？", "d": "为什么排队一样，一块都不能少", "v": "积木要按什么顺序拼"},
        {"t": "为什么换一下顺序就走不到了？", "d": "同样几块积木，结果真的会变吗", "v": "为什么换一下顺序就走不到了"},
        {"t": "积木上的数字有什么用？", "d": "「走 3 格」和「转 2 次」里的数字是什么意思", "v": "积木上的数字有什么用"},
        {"t": "走不到终点时，怎么找出错的那一块？", "d": "想学会自己检查、自己改", "v": "走不到终点时怎么找出错的那一块"},
    ],
    "objectives": [
        "能说出程序就是一串有先后顺序的指令，计算机会一块一块按顺序执行",
        "能把「向前走、向左转、向右转」三类积木拼成一段程序并运行",
        "能通过修改积木上的参数改变小角色走的路线，并说出转向是相对它自己的朝向",
        "能在小角色走不到终点或走出格子时，找出放错的那一块积木并改正过来",
    ],
    "objectives_plain": [
        "能说出程序就是一串有先后顺序的指令，计算机会一块一块按顺序执行",
        "能把「向前走、向左转、向右转」三类积木拼成一段程序并运行",
        "能通过修改积木上的参数改变小角色走的路线，并说出转向是相对它自己的朝向",
        "能在小角色走不到终点或走出格子时，找出放错的那一块积木并改正过来",
    ],
    "standards": [
        {"content": "使用图形化编程工具实现简单算法",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 算法与程序"},
        {"content": "在动手拼搭与调试中体验「顺序执行」的含义，养成一步步说清、一步步验证的习惯",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 计算思维"},
    ],
    "prereqs": ["it-e-algorithm-steps"],
    "prereqs_name": "算法步骤与流程图",
    "prereqs_meta": "it-e-algorithm-steps",
    "leads_to": ["it-e-branch-loop"],
    "next_meta": "it-e-branch-loop",
    "section_images": ["assets/it-e-block-programming-fig1.webp", "assets/it-e-block-programming-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "小角色看不见你、猜不到你的想法。把动作拼成积木、排好顺序，它才动得起来。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能亲手拼出一段程序，让小角色走到小旗那里。",
        "objectives": "看清四件事：程序是什么、积木怎么拼、数字管什么、走错了怎么改。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "一块积木一个动作；从上到下执行；顺序一变，走到的地方就变。",
        "lab-1": "先加积木再点运行。执行到哪一块，哪一块就亮起来——对照着看它走的每一格。",
        "module-2": "积木上的数字是参数；转向看的是它自己头朝哪边，不是屏幕的左右。",
        "lab-2": "两个滑块要一起配：位置对了还不够，还要让它头朝上。",
        "worked-example": "四步走：看清起点、顺着走、遇到转向停一停、把结果说出来跟终点比。",
        "conceptest-1": "三个说法里都藏着高频错误，选完把解释读一遍。",
        "synthesis": "只换一块转向积木，就能改掉整条路线——想想为什么它这么要紧。",
        "posttest": "扫地机器人、遥控小车、总差一格的程序，看看你还能不能用上同一套办法。",
        "summary": "三句话：程序是什么、参数与转向怎么看、走不到时怎么改。",
        "homework": "三层小任务，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学信息科技「算法与程序」在流程图之后、分支循环之前的一课。四年级学生的难点有两个：一是把心里想好的路线说成一条条清楚的指令，二是以为「转向」是转到屏幕的左边或右边。所以全课做成一个可以一直动手的小剧场：网格舞台上站着一个小角色和一面临终点的小旗，学生点积木拼出程序、点运行，小角色就一格一格走过去，执行到哪一块积木哪一块就亮起来——顺序执行这件事因此变得看得见；走不到终点或者走出格子，反馈里点明是转向放错了位置还是格数多了。第二个动手台把参数单独拎出来：拖动「向前走几格」「向右转几次」两个滑块，同两块积木走出完全不同的落点和朝向。概念页把结论收成一句可带走的规则与口诀（积木搭顺序，数字管多少，转身看自己，一步不能少），例题页示范「读程序、画路线」的四步，综合任务只让学生换一块积木，亲手体会转向积木有多关键。",
    "plan_table": """| 1 | cover | 积木式程序设计 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：程序里的指令，是怎么被执行的？ | 起·前测（暴露直觉） |
| 5 | concept | 程序：一串按顺序排好的指令积木 | 承·概念一（顺序执行 + 口诀铺垫） |
| 6 | interactive | 动手一：拼出积木程序，让小角色走到小旗 | 承·核心模拟（拼积木 → 运行 → 逐格执行并高亮） |
| 7 | concept | 积木上的数字是参数，转向看的是它自己 | 承·概念二（参数 + 相对转向 + 反例） |
| 8 | interactive | 动手二：调一调参数，看路线怎么变 | 承·参数台（双滑块 + 落点与朝向实时变化） |
| 9 | concept | 例题示范：读出这段程序，它会走到哪里？ | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：三种说法，错在哪里 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：只换一块积木，让它走到小旗 | 合·迁移应用（换转向积木并验证） |
| 12 | quiz | 后测：换几个情境，规则还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把积木程序讲清楚 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：指令积木 / 按顺序执行 / 参数与调试修正 三栏\n- P5 积木序列与小角色行走示意图（已生成）：一串积木 + 方格地图上的行走路线\n- P7 顺序与参数改变结果对照图（已生成）：一边到达小旗、一边走偏出格\n- 三张图均为教学示意图，不出现任何真实软件界面、截图或商标\n- 若需补充：学生手绘的路线草图与积木程序（需获得授权后使用）",
}
