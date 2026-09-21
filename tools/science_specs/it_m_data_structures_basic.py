# -*- coding: utf-8 -*-
"""初中信息科技 · 数据结构基础（列表/字典）（G8）—— 补齐课标「数据与算法」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-m-data-structures-basic-fig1.webp'
F2 = './assets/it-m-data-structures-basic-fig2.webp'

TTS = {
    "hero": "先看一个真实会遇到的麻烦。一个班四十个人，如果给每个人单独起一个变量名来存成绩，那要写四十行，问「谁的分数最高」还得再逐行比一遍。数据一多，这种写法立刻撑不住。所以我们需要一种办法，把一组相关的数据装进一个整体里，按位置或者按名字去拿。这就是数据结构要解决的问题：同样的数据，组织方式不同，能做的事和付出的代价完全不同。",
    "problem-anchor": "在开始之前，先选出你最想弄明白的那个问题。是想知道列表里的下标为什么从零开始，还是想知道字典凭什么不用一个个比就能直接找到，又或者你想亲手给一份真实的数据选一种合适的组织方式。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能用列表保存一组有序数据，说清下标从零开始、长度与元素位置的关系。第二，能说出按下标访问与按值查找在代价上的区别，并解释为什么一个与数据量无关、另一个会随数据量增长。第三，能用字典按键保存和取出数据，说清键的唯一性以及它与列表的区别。第四，能针对一个真实需求，在列表与字典之间做出选择并说明理由。",
    "pretest": "先做三道小题，凭你现在的想法选就行，选错了也没关系，正好能看出哪里需要重点听。选完会立刻出现解释。",
    "module-1": "列表是一种按顺序排列的数据结构，用从零开始的整数下标定位每一个元素。它的操作很直白：按下标读取、按下标修改、在末尾追加、在指定位置插入、删除某个元素，还有从头到尾遍历。这里要特别留意代价的差别：按下标读取是一次直接定位，第 0 个和第 999 个花的时间一样多；而按值查找只能从第一个开始逐个比对，最坏情况下要把全部元素都比一遍。也就是说，同样的列表，换一种用法，代价就从「与数据量无关」变成了「随数据量增长」。",
    "lab-1": "光听结论不如自己动手。这是一个列表操作台，五个名字排成一排，每个格子上面标着下标。你可以按下标读取、按值查找、在末尾追加、在中间插入、删除某个元素。请盯住两个数字：本次比较次数和累计比较次数。你会发现，按下标读取永远是 1 次，按值查找却会随着目标位置往后而变多；插入和删除虽然不比较，却要把后面的元素依次挪动。",
    "module-2": "字典用键来定位值，键和值成对出现，同一个字典里键是唯一的。它的用法是：把键放进方括号，直接取出对应的值。和列表相比，列表靠位置，字典靠名字——问「第三个是什么」用列表，问「学号是二五零一的那个人是谁」用字典。为什么字典快？因为它不是一个个比过去，而是根据键直接算出该去哪里拿。代价是它需要额外的空间来记录这些对应关系，这就是典型的用空间换时间。两种结构也不是二选一：把字典放进列表，就能既保留先后顺序，又能按学号直接查人。",
    "lab-2": "现在来一次正面对比。同样二十条学生记录，用列表存在一个按顺序排列的整体里，用字典存成学号到姓名的对应关系。你只需要拖动查询次数，然后点开始，看两种结构分别比较了多少次。多跑几次你会发现：列表的比较次数会随着被查的位置上下波动，而字典每次都只有一次定位。结论很清楚，但也要记住它的前提——我们查的字段正好是字典的键。",
    "worked-example": "我们一起处理一份原始记录：一列「学号 姓名 成绩」，比如二五零一 张明 九十二。第一个需求是按学号快速查出成绩，这就要用字典，把学号当键、成绩当值，一次定位拿到结果。第二个需求是把全班成绩从高到低排名，这要用列表，因为要反复比较和交换位置，顺序本身就是结果的一部分。第三个需求是统计每个分数段有多少人，还是字典，只不过这次键换成了分数段，值换成了人数，每读到一条记录就把对应分数段的计数加一。你看，同一份原始数据，三个需求对应三种组织方式——所以先问清「要拿它做什么」，再决定怎么存。",
    "conceptest-1": "现在用三个容易弄错的说法考考你。请仔细读每一个选项，选出你认为正确的那个，然后看解释。",
    "synthesis": "学到这里，请你当一次数据组织的决策者。左边是四个真实需求，右边给你三种选择：用列表、用字典，或者把两者配合起来。请逐条判断，然后运行检查。要特别留意的是：没有哪种结构天生更好，只有和需求对不对得上——选错了不是程序执行不了，而是要付出多得多的代价。",
    "posttest": "最后用新情境检验一下。这次出现了图书馆的借阅记录和连续采集的温度读数，看看你能不能把下标、键和两种代价的区别用上去。",
    "summary": "这节课我们弄明白了三件事。第一，列表按下标保存有序数据，下标从零开始，按下标访问是一次直接定位，按值查找要逐个比对。第二，字典用键定位值，键在同一个字典里唯一，它用额外的空间换来了更快的查找。第三，选择哪一种结构，取决于你打算怎么用它：问位置用列表，问名字用字典，两者还能组合成列表套字典。回到开头那个班：把四十条记录装进一个列表，再建一个学号到位置的字典，既能整体遍历，又能按学号直接取——麻烦就消失了。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出列表与字典各自的取值写法，并说明下标从几开始、键有什么限制。第二层能力应用，动手做：给出五条学生记录，分别用列表和字典各组织一次，并写出「按学号查成绩」的两段伪代码。第三层迁移挑战，选做：为自己的一个真实需求（比如管理自己的错题、记录运动数据）设计数据组织方式，说明为什么这样选，以及数据量变大会发生什么变化。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 列表与两种访问代价", "lab-1": "实验室一 列表操作台", "module-2": "概念二 字典与选择依据",
    "lab-2": "实验室二 两种查找的对比台", "worked-example": "例题讲解", "conceptest-1": "概念测试",
    "synthesis": "综合任务 数据组织选择器", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

LAB_CSS = """
<style>
.ta-log { list-style: none; margin: 0; padding: 0; font-size: 14px; }
.ta-log li { padding: 8px 10px; margin-bottom: 6px; border-radius: 10px;
  background: var(--bg-subtle); border: 1px solid var(--line-subtle); white-space: pre-wrap; }
.ta-log li .tag { display: inline-block; margin-right: 8px; padding: 1px 8px; border-radius: 999px;
  font-size: 12px; font-weight: 700; background: var(--brand-soft); color: var(--brand); }
.ta-log li.bad { border-color: var(--danger); }
.ta-log li.ok { border-color: var(--ok); }
.ta-slots { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
.ta-slot { min-width: 74px; border-radius: 10px; border: 1px solid var(--line-subtle);
  background: var(--bg-subtle); text-align: center; padding: 6px 4px 8px; transition: all .2s; }
.ta-slot .idx { display: block; font-size: 11px; color: var(--muted); font-variant-numeric: tabular-nums; }
.ta-slot .val { display: block; font-size: 15px; font-weight: 700; }
.ta-slot.hit { border-color: var(--brand); background: var(--brand-soft); }
.ta-slot.cmp { border-color: var(--warm); background: var(--warm-soft); }
.ta-slot.dup { border-style: dashed; opacity: .55; }
.ta-key { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 13px; }
.bar-row { display: flex; align-items: center; gap: 10px; font-size: 13px; margin-top: 8px; }
.bar-row .lab { flex: 0 0 108px; color: var(--muted); }
.bar-track { flex: 1; height: 12px; border-radius: 999px; background: rgb(var(--paper-rgb) / .18); overflow: hidden; }
.bar-fill { display: block; height: 100%; width: 0%; border-radius: 999px; background: linear-gradient(90deg, var(--brand), var(--brand-2)); transition: width .35s ease; }
.bar-fill.alt { background: var(--warm); }
.bar-row .val { flex: 0 0 96px; text-align: right; font-variant-numeric: tabular-nums; font-weight: 700; }
select { width: 100%; border-radius: 12px; border: 1px solid var(--line); background: var(--card);
  color: var(--text); padding: 12px 14px; font-size: 15px; }
.pick { display: grid; grid-template-columns: 1fr; gap: 8px; }
</style>
"""

CUSTOM_JS = r"""
/* ============================================================
   it-m-data-structures-basic 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 列表操作台：按下标读 / 按值查 / 追加 / 插入 / 删除，比较次数可观察
   3) 两种查找对比台：列表线性查找 vs 字典按键定位
   4) 数据组织选择器：四个需求 × 三种选择 → 逐条判定与理由
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

  /* ---------- 2. 列表操作台 ---------- */
  var POOL = ['张明', '李平', '王芳', '赵磊', '陈静', '刘洋', '孙悦', '周航'];
  var s1 = document.getElementById('s1-stage');
  if (s1) {
    var data = ['张明', '李平', '王芳', '赵磊', '陈静'];
    var lastCmp = 0, totalCmp = 0, ops = 0, hitIdx = -1, cmpSet = [];

    var eSlots = document.getElementById('s1-slots');
    var eIdx = document.getElementById('s1-idx');
    var eIdxVal = document.getElementById('s1-idx-val');
    var eTarget = document.getElementById('s1-target');
    var eLen = document.getElementById('s1-len');
    var eLast = document.getElementById('s1-last');
    var eTotal = document.getElementById('s1-total');
    var eOps = document.getElementById('s1-ops');
    var eOut = document.getElementById('s1-out');

    function render1() {
      eSlots.innerHTML = '';
      data.forEach(function (v, i) {
        var d = document.createElement('div');
        d.className = 'ta-slot' + (i === hitIdx ? ' hit' : (cmpSet.indexOf(i) >= 0 ? ' cmp' : ''));
        d.innerHTML = '<span class="idx">下标 ' + i + '</span><span class="val">' + v + '</span>';
        eSlots.appendChild(d);
      });
      eLen.textContent = data.length + ' 个元素';
      eLast.textContent = lastCmp + ' 次';
      eTotal.textContent = totalCmp + ' 次';
      eOps.textContent = ops + ' 次操作';
      eIdxVal.textContent = '下标 ' + eIdx.value;
      if (eIdx.value >= data.length) eIdxVal.textContent = '下标 ' + eIdx.value + '（越界）';
    }

    function say(html, bad) {
      eOut.className = 'result ' + (bad ? 'error' : '');
      eOut.innerHTML = html;
    }

    function record(cmp, html, bad) {
      lastCmp = cmp; totalCmp += cmp; ops += 1;
      render1();
      say(html, bad);
    }

    function freeName() {
      for (var i = 0; i < POOL.length; i++) { if (data.indexOf(POOL[i]) < 0) return POOL[i]; }
      return '新同学';
    }

    eIdx.addEventListener('input', function () { hitIdx = -1; cmpSet = []; render1(); });

    document.getElementById('s1-read').addEventListener('click', function () {
      var i = Number(eIdx.value);
      if (i >= data.length) {
        hitIdx = -1; cmpSet = [];
        record(0, '<strong>下标越界。</strong>这个列表只有 ' + data.length + ' 个元素，合法下标是 0 到 ' + (data.length - 1) +
          '。<strong>错因提醒：</strong>最容易误认为「长度是几，下标就能取到几」，忽略了下标从 0 开始，所以最大下标永远比长度小 1。', true);
        return;
      }
      hitIdx = i; cmpSet = [];
      record(1, '<strong>按下标读取只花了 1 步。</strong>读「' + data[i] + '」和读第 0 个元素一样快——因为这一步是直接定位，' +
        '不需要和谁比较。因此它的代价与列表长度无关，这正是列表最擅长的事。');
    });

    document.getElementById('s1-find').addEventListener('click', function () {
      var t = eTarget.value, steps = 0, found = -1;
      var marks = [];
      for (var i = 0; i < data.length; i++) {
        steps += 1;
        marks.push(i);
        if (data[i] === t) { found = i; break; }
      }
      hitIdx = found; cmpSet = marks;
      record(steps, '<strong>按值查找「' + t + '」一共比较了 ' + steps + ' 次。</strong>' +
        (found >= 0
          ? '目标在下标 ' + found + '，也就是说前面的 ' + found + ' 个元素都白比了一遍。'
          : '列表里没有这个名字，所以把全部 ' + data.length + ' 个元素都比完了才知道不在——这就是最坏情况。') +
        '<br><strong>易错点：</strong>把「按下标读」和「按值找」当成同一件事，是最常见的错误。' +
        '前者是一次直接定位，后者只能从头逐个比对，代价会随数据量增长。');
    });

    document.getElementById('s1-append').addEventListener('click', function () {
      if (data.length >= 8) { say('<strong>这个操作台最多放 8 个元素。</strong>真实程序里列表可以更长，但「追加」始终是在末尾接上一个，不需要挪动别人。', true); return; }
      var nm = freeName();
      data.push(nm); hitIdx = data.length - 1; cmpSet = [];
      record(0, '<strong>在末尾追加「' + nm + '」，没有发生任何比较。</strong>新元素直接接在最后一个位置之后，' +
        '已有元素的位置全都不变——这是最省事的一种写法。');
    });

    document.getElementById('s1-insert').addEventListener('click', function () {
      var i = Number(eIdx.value);
      if (i > data.length) { say('<strong>插入位置越界。</strong>插到下标 ' + i + ' 之前是做不到的，允许的范围是 0 到 ' + data.length + '。', true); return; }
      if (data.length >= 8) { say('<strong>这个操作台最多放 8 个元素。</strong>先删掉一个再试。', true); return; }
      var nm = freeName();
      data.splice(i, 0, nm); hitIdx = i; cmpSet = [];
      record(0, '<strong>在下标 ' + i + ' 处插入「' + nm + '」，比较次数是 0，但它并不省钱。</strong>' +
        '原来下标 ' + i + ' 及之后的 ' + (data.length - i - 1) + ' 个元素都要依次往后挪一格。' +
        '所以列表擅长「在末尾加」，不擅长「在中间插」。');
    });

    document.getElementById('s1-del').addEventListener('click', function () {
      var i = Number(eIdx.value);
      if (i >= data.length) { say('<strong>删除位置越界。</strong>合法下标是 0 到 ' + (data.length - 1) + '。', true); return; }
      var gone = data[i];
      data.splice(i, 1); hitIdx = -1; cmpSet = [];
      record(0, '<strong>删除下标 ' + i + ' 的「' + gone + '」，比较次数是 0。</strong>' +
        '和插入一样，后面的元素要依次往前补位。删除不改变剩余元素的相对顺序，这一点是列表的重要性质。');
    });

    document.getElementById('s1-reset').addEventListener('click', function () {
      data = ['张明', '李平', '王芳', '赵磊', '陈静'];
      lastCmp = 0; totalCmp = 0; ops = 0; hitIdx = -1; cmpSet = [];
      render1();
      say('已恢复到最初的五个元素，计数器也清零了。');
    });

    render1();
    say('列表已就绪，共 5 个元素。先点「按下标读取」，再点「按值查找」，比较一下两者的比较次数。');
  }

  /* ---------- 3. 两种查找对比台 ---------- */
  var IDS = [], RECS = [];
  for (var k = 1; k <= 20; k++) {
    IDS.push('2025' + (k < 10 ? '00' : '0') + k);
  }
  var NMS = ['张明', '李平', '王芳', '赵磊', '陈静', '刘洋', '孙悦', '周航', '吴迪', '郑凯',
             '冯雪', '许阳', '何静', '马超', '曹雨', '邓婷', '蒋鹏', '谢楠', '韩磊', '唐可'];
  IDS.forEach(function (id, i) { RECS.push({ id: id, name: NMS[i] }); });

  var s2 = document.getElementById('s2-stage');
  if (s2) {
    var eQ = document.getElementById('s2-q');
    var eQVal = document.getElementById('s2-q-val');
    var eOut2 = document.getElementById('s2-out');
    var eBarL = document.getElementById('s2-bar-list');
    var eBarD = document.getElementById('s2-bar-dict');
    var eValL = document.getElementById('s2-val-list');
    var eValD = document.getElementById('s2-val-dict');

    function run2() {
      var q = Number(eQ.value);
      eQVal.textContent = q + ' 次';
      var listCmp = 0, dictCmp = 0, rows = [], worst = 0;
      for (var i = 0; i < q; i++) {
        var pos = Math.floor(Math.random() * RECS.length);
        var rec = RECS[pos];
        var lc = pos + 1;                 // 列表：从头逐个比对，命中位置越靠后比得越多
        var dc = 1;                        // 字典：按键直接定位
        listCmp += lc; dictCmp += dc;
        if (lc > worst) worst = lc;
        rows.push('<li><span class="tag">第 ' + (i + 1) + ' 次</span>查 ' + rec.id + '（' + rec.name +
          '）：列表比较 ' + lc + ' 次，字典比较 ' + dc + ' 次。</li>');
      }
      var avgL = listCmp / q, avgD = dictCmp / q;
      var maxBar = Math.max(listCmp, dictCmp, 1);
      eBarL.style.width = (listCmp / maxBar * 100).toFixed(1) + '%';
      eBarD.style.width = (dictCmp / maxBar * 100).toFixed(1) + '%';
      eValL.textContent = listCmp + ' 次';
      eValD.textContent = dictCmp + ' 次';

      rows.push('<li class="ok"><span class="tag">汇总</span>查询 ' + q + ' 次：列表共比较 ' + listCmp +
        ' 次（平均 ' + avgL.toFixed(1) + ' 次，最坏的一次 ' + worst + ' 次）；字典共比较 ' + dictCmp +
        ' 次（平均 ' + avgD.toFixed(1) + ' 次）。</li>');
      rows.push('<li><span class="tag">看懂它</span>列表的比较次数会随着被查记录在列表中的位置上下波动，' +
        '因为它只能从头一个个比过去；字典每次都是一次定位，与数据量无关。' +
        '<strong>易错点：</strong>不要把字典的快理解成「更聪明」——它是用额外的空间把「学号到姓名」的对应关系事先记了下来，' +
        '换来的时间优势，这是典型的用空间换时间。</li>');
      rows.push('<li class="ok"><span class="tag">前提</span>字典能一键定位，前提是<strong>我们查的字段正好就是它的键</strong>。' +
        '如果这次要查的是「分数是 92 分的人」，而字典的键是学号，那就退回到一个个比过去了。</li>');
      eOut2.className = 'result';
      eOut2.innerHTML = '<ul class="ta-log">' + rows.join('') + '</ul>';
    }

    eQ.addEventListener('input', run2);
    document.getElementById('s2-run').addEventListener('click', run2);
    run2();
  }

  /* ---------- 4. 数据组织选择器 ---------- */
  var NEEDS = {
    n1: { q: '记录一列按先后到达的测量值，之后要按顺序逐个处理',
          best: 'list',
          why: '顺序本身就是这份数据要保留的信息，而且处理方式是「从头到尾」——按下标依次读正好是列表最擅长的事。' },
    n2: { q: '用学号直接查出某个学生的姓名',
          best: 'dict',
          why: '这是典型的「按名字找」的需求，把学号作为键，一次定位就能拿到，不需要逐个比对。' },
    n3: { q: '保存全班学生记录：既要整体遍历，又要按学号查单个',
          best: 'both',
          why: '外层用一个列表保留全班记录的先后顺序，内层每条记录用字典把字段名和值对应起来，于是「遍历」和「按学号查」两件事都做得成。' },
    n4: { q: '统计每个分数段各有多少人',
          best: 'dict',
          why: '把分数段当作键、人数当作值，每读到一条记录就把对应分数段的计数加一——这正是「按名字定位并累加」。' }
  };
  var LABELS = { list: '用列表', dict: '用字典', both: '列表套字典' };
  var syn = document.getElementById('syn-stage');
  if (syn) {
    var pick = { n1: 'list', n2: 'list', n3: 'list', n4: 'list' };

    function renderSyn() {
      Object.keys(NEEDS).forEach(function (k) {
        Object.keys(LABELS).forEach(function (o) {
          var b = document.querySelector('[data-syn="' + k + '"][data-opt="' + o + '"]');
          if (b) b.classList.toggle('selected', pick[k] === o);
        });
      });
    }
    document.querySelectorAll('[data-syn]').forEach(function (b) {
      b.addEventListener('click', function () {
        pick[b.dataset.syn] = b.dataset.opt;
        renderSyn();
        var out = document.getElementById('syn-out');
        out.className = 'result warn';
        out.textContent = '都选好之后，点「检查这份设计」。';
      });
    });

    document.getElementById('syn-run').addEventListener('click', function () {
      var rows = [], score = 0;
      Object.keys(NEEDS).forEach(function (k) {
        var N = NEEDS[k], ok = pick[k] === N.best;
        if (ok) score += 1;
        rows.push('<li' + (ok ? ' class="ok"' : ' class="bad"') + '><span class="tag">需求</span>' + N.q +
          '<br>你的选择：' + LABELS[pick[k]] + '；合适的做法：' + LABELS[N.best] +
          (ok ? '。<strong>判断成立。</strong>' + N.why
              : '。<strong>不太合适。</strong>' + N.why + '按现在的选法，也能勉强做出来，但代价会明显更大。') + '</li>');
      });
      rows.push('<li class="' + (score === 4 ? 'ok' : 'bad') + '"><span class="tag">总评</span>四题中 ' + score +
        ' 题选得合适。记住判断的窍门：<strong>问「第几个」用列表，问「叫什么」用字典</strong>；' +
        '两种需求同时存在时，就把它们组合起来。</li>');
      var out = document.getElementById('syn-out');
      out.className = 'result ' + (score === 4 ? '' : (score >= 2 ? 'warn' : 'error'));
      out.innerHTML = '<ul class="ta-log">' + rows.join('') + '</ul>';
    });

    document.getElementById('syn-reset').addEventListener('click', function () {
      pick = { n1: 'list', n2: 'list', n3: 'list', n4: 'list' };
      renderSyn();
      var out = document.getElementById('syn-out');
      out.className = 'result warn';
      out.textContent = '都选好之后，点「检查这份设计」。';
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

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：一组数据该怎么装起来？", TTS["pretest"], [
        {"q": "一个列表里有 6 个元素，下面哪个说法是正确的？",
         "options": [("合法下标是 0 到 5，最大下标比长度小 1", True),
                     ("合法下标是 1 到 6，正好和长度对应", False),
                     ("合法下标是 0 到 6，一共 7 个位置", False)],
         "explain": "下标从 0 开始，所以长度为 6 的列表，下标是 0 到 5。<strong>错因提醒：</strong>同学最容易误认为「长度为几、下标就能取到几」，多算了一个位置——这是写程序时最常见的越界来源。"},
        {"q": "在一个有一千个元素的列表里，下面哪一种操作花的时间基本不受数据量影响？",
         "options": [("按下标读取第 500 个元素", True),
                     ("查找名字为「张明」的元素在第几个", False),
                     ("把列表里所有元素逐个检查一遍", False)],
         "explain": "按下标读取是一次直接定位，数据再多也是同样一步。<strong>错因提醒：</strong>容易把「按下标读」和「按值找」搞混——后者必须从头逐个比对，代价会随数据量增长。"},
        {"q": "要用学号直接查出某个学生的姓名，最合适的组织方式是：",
         "options": [("把学号当键、姓名当值，存成字典", True),
                     ("把所有学号按顺序放进一个列表，查找时从头比对", False),
                     ("给每个学生单独起一个变量名，分别记住", False)],
         "explain": "这是「按名字找」的需求，是字典最擅长的场景。<strong>错因提醒：</strong>常见错误是认为列表什么都能干，于是明明知道学号，还要从头一个个比过去，白白付出成倍的代价。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "列表：一组有序数据，用下标定位", TTS["module-1"], f'''
        <div class="inner-card">
          <p><strong>为什么要学这一课？</strong>你已经会用变量保存单个数据，也采集过一组一组的观测值。但当数据变成几十条、上千条时，给每个数据单独起名字就撑不住了。<strong>所以</strong>我们需要把一组相关数据装进一个整体——这个整体就是数据结构，而列表是其中最基本的一种。</p>
        </div>
        <p style="font-size:17px;margin:12px 0">列表是<strong>按顺序排列</strong>的一组数据，每个元素有一个整数下标，<strong>下标从 0 开始</strong>。常用操作有：按下标读取、按下标修改、在末尾追加、在指定位置插入、删除某个元素、从头到尾遍历。</p>
        <div class="grid grid-3">
          <div class="inner-card">
            <p><strong>① 按下标读取</strong></p>
            <p style="color:var(--muted)">一次直接定位，第 0 个和第 999 个一样快。</p>
          </div>
          <div class="inner-card">
            <p><strong>② 按值查找</strong></p>
            <p style="color:var(--muted)">从头逐个比对，最坏要把全部比一遍。</p>
          </div>
          <div class="inner-card">
            <p><strong>③ 中间插删</strong></p>
            <p style="color:var(--muted)">不比较，但后面的元素要依次挪位。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="列表结构示意图，一排带下标的格子以及按下标读取与按值查找两条路径的对比">
          <figcaption>列表按下标定位：按下标读取是一次直接定位，按值查找只能从头逐个比对</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🗂️</span><div><strong>记忆锚点：</strong>把列表想象成一排带编号的储物柜——柜门上的号码就是下标，号码从 <strong>0</strong> 开始。<strong>知道柜号</strong>就直接开那一格；<strong>只知道里面放着什么</strong>，就只能从第一格开始依次打开看。这一个差别，决定了后面所有的性能讨论。</div></div>
{insight_box([
    {"lens": "看见它", "text": "同一组名字，装进列表之后就能整体传递、整体遍历，还能用长度描述它的规模——数据一旦有了结构，才有了「操作」的可能。"},
    {"lens": "比较它", "text": "按下标读的第 0 个和第 999 个一样快，按值查找却会随位置往后而变慢。同一个列表，换一种用法，代价就从「与数据量无关」变成「随数据量增长」。"},
    {"lens": "迁移它", "text": "排队、编号货架、座位表都是列表的思想：位置固定、可以按号直接找，但要在中间插一个人，后面所有人都得往后退一步。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "列表操作台：哪种用法要比较很多次？", TTS["lab-1"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">五个名字排成一排，每个格子上标着下标。逐个试一遍五种操作，盯住下面的比较次数。</p>
        <div class="lab-panel">
          <div id="s1-stage">
            <div class="ta-slots" id="s1-slots"></div>
            <div class="lab-readout">
              <div class="readout-cell"><span class="k">列表长度</span><span class="v" id="s1-len">—</span></div>
              <div class="readout-cell"><span class="k">本次比较次数</span><span class="v" id="s1-last">—</span></div>
              <div class="readout-cell"><span class="k">累计比较次数</span><span class="v green" id="s1-total">—</span></div>
              <div class="readout-cell"><span class="k">已执行操作</span><span class="v" id="s1-ops">—</span></div>
            </div>
            <div class="slider-row">
              <label for="s1-idx">操作的下标</label>
              <input type="range" id="s1-idx" min="0" max="7" step="1" value="2">
              <span class="readout-cell" style="flex:0 0 110px"><span class="k">当前</span><span class="v" id="s1-idx-val">下标 2</span></span>
            </div>
            <label style="display:block;margin-top:12px;font-weight:700;font-size:14px">按值查找的目标
              <select id="s1-target" style="margin-top:6px">
                <option value="张明">张明（在下标 0）</option>
                <option value="王芳">王芳（在下标 2）</option>
                <option value="陈静">陈静（在下标 4）</option>
                <option value="周航">周航（不在列表里）</option>
              </select>
            </label>
          </div>
          <div class="flex-row">
            <button class="choice" id="s1-read" style="text-align:center">按下标读取</button>
            <button class="choice" id="s1-find" style="text-align:center">按值查找</button>
            <button class="choice" id="s1-append" style="text-align:center">末尾追加</button>
          </div>
          <div class="flex-row" style="margin-top:8px">
            <button class="choice" id="s1-insert" style="text-align:center">在指定下标插入</button>
            <button class="choice" id="s1-del" style="text-align:center">删除指定下标</button>
            <button class="choice" id="s1-reset" style="text-align:center">重置</button>
          </div>
          <p class="result warn" id="s1-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>动手比一比：</strong>把下标调到 4，先点「按下标读取」，再选「陈静」点「按值查找」。同样拿到同一个元素，一次是 1 步，一次是 5 步。<strong>易错点：</strong>插入和删除的比较次数是 0，但它们并不便宜——后面的元素要依次挪位，这个代价没有记在计数器里。</div></div>
    ''', tag="列表实验室", bloom="apply"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "字典：用键定位值，用空间换时间", TTS["module-2"], f'''
        <div class="inner-card">
          <p><strong>列表靠位置，字典靠名字。</strong>当你手上拿的是「某个标识」而不是「第几个」的时候，列表就只能一个个比过去——字典正是为这件事准备的。</p>
        </div>
        <p style="font-size:17px;margin:12px 0">字典用<strong>键</strong>来定位<strong>值</strong>，键与值成对出现，且<strong>同一个字典里的键是唯一的</strong>。取值时把键放进方括号即可，例如：<span class="ta-key">成绩表["2025001"]</span>。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>它是怎么快的：</strong>字典不是从第一个比过去，而是根据键直接算出该去哪个位置取，所以数据再多也只是一次定位。</div></div>
          <div class="step"><span class="n">2</span><div><strong>代价是什么：</strong>它需要额外的空间来保存「键到值」的对应关系。用空间换时间，这是数据结构里非常常见的一种取舍。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>怎么选：</strong>问「第几个」用列表，问「叫什么」用字典。两种需求同时存在时，把字典放进列表，就能两者兼得。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="字典键值映射示意图，以及列表与字典按不同需求选择的对照">
          <figcaption>字典把「学号」这种标识当成键，一次算出位置；列表则靠先后顺序保存</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">最容易犯的两个错：一是<strong>误认为字典一定比列表好</strong>——如果需求本身是「按先后顺序处理」，字典反而丢掉了顺序这个信息，用列表才对；二是<strong>以为键可以是任意重复的值</strong>——同一个键只能对应一个值，重复的键会把原来的值覆盖掉。还要注意：字典的快是有前提的，<strong>只有查的字段正好是键</strong>，一次定位才成立；换个字段去查，代价照样会变大。</p>
        </div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "两种查找的对比台：到底差多少次比较？", TTS["lab-2"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">同一批二十条学生记录，分别用列表和字典存起来。拖一下查询次数，看看两种结构各比较了多少次。</p>
        <div class="lab-panel">
          <div id="s2-stage">
            <div class="slider-row" style="margin-top:0">
              <label for="s2-q">查询次数</label>
              <input type="range" id="s2-q" min="1" max="10" step="1" value="5">
              <span class="readout-cell" style="flex:0 0 96px"><span class="k">次数</span><span class="v" id="s2-q-val">5 次</span></span>
            </div>
            <div class="bar-row">
              <span class="lab">列表（逐个比）</span>
              <span class="bar-track"><span class="bar-fill" id="s2-bar-list"></span></span>
              <span class="val" id="s2-val-list">0 次</span>
            </div>
            <div class="bar-row">
              <span class="lab">字典（按键定位）</span>
              <span class="bar-track"><span class="bar-fill alt" id="s2-bar-dict"></span></span>
              <span class="val" id="s2-val-dict">0 次</span>
            </div>
          </div>
          <div class="flex-row">
            <button class="choice" id="s2-run" style="text-align:center;flex:1">再跑一次</button>
          </div>
          <p class="result warn" id="s2-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">⚖️</span><div><strong>动手比一比：</strong>查询次数越多，两条柱子的差距拉得越开。多跑几次，注意列表那边每次的汇总数字都不一样，而字典永远是「次数 × 1」——这个波动本身就说明列表在赌运气，字典则是稳定的。</div></div>
    ''', tag="对比实验室", bloom="analyze"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：同一份数据，三种需求三种组织", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:var(--warm)">
          <p style="margin:0"><strong>题目：</strong>手上有一份原始记录，每行是「学号 姓名 成绩」，例如：二五零一 张明 九十二。现在有三个需求：①按学号查出成绩；②把全班成绩从高到低排名；③统计每个分数段有多少人。请分别说明该用什么结构，并写出关键步骤。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看清需求问的是什么。</strong>①问的是「某个标识对应的值」，②问的是「第几个」，③问的是「某个类别累计多少」。需求一换，合适的结构就跟着换。</div></div>
          <div class="step"><span class="n">2</span><div><strong>需求①用字典。</strong>把学号当键、成绩当值：<span class="ta-key">成绩表["2025001"]</span> 一次定位就能拿到分数，不需要逐个比对。</div></div>
          <div class="step"><span class="n">3</span><div><strong>需求②用列表。</strong>排名要反复比较、交换位置，而且顺序本身就是结果的一部分，所以把成绩装进列表做排序，最后按下标依次输出。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>需求③还是字典，只是键换了。</strong>这次键是分数段，值是人数：每读到一条记录，就把该分数段的计数加一，例如 <span class="ta-key">人数["九十到一百"] = 人数["九十到一百"] + 1</span>。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">不少同学的第一反应是「全都用列表就行」，于是为了按学号查成绩，写下从头逐个比对的伪代码。它确实能跑通，但当数据量涨到几千条，每次查询都要比几千次——这不是程序写错了，而是<strong>结构选错了</strong>。另一处容易搞混的是<strong>把排名的结果和排名的过程混在一起</strong>：列表保存的是排好序的结果，比较与交换发生在过程中，两者都要用列表来承载顺序。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "下面哪句话是正确的？",
         "options": [("字典用键定位值，同一个字典里的键不能重复", True),
                     ("字典的键可以重复，取到的会是最后一个值", False),
                     ("字典里的元素可以像列表一样用下标 0、1、2 来取", False)],
         "explain": "键是唯一的标识，重复的键会把先前的值覆盖掉，所以它不能当「第几个」来用。<strong>错因提醒：</strong>最容易误认为字典就是「带名字的列表」，于是尝试用下标去取，或者以为重复键会并存。"},
        {"q": "有一万条记录，要按学号查人，也可以按姓名查人。下面哪种设计最站得住脚？",
         "options": [("用学号当键建一个字典，另外用一个列表保留原始顺序，需要时再按姓名过滤", True),
                     ("全部用一个列表存，任何查询都从头比对", False),
                     ("只用字典，因为字典一定比列表快", False)],
         "explain": "键只能选一个字段，另一个字段的查询要靠遍历，所以常常是「字典 + 列表」配合使用。<strong>错因提醒：</strong>常见错误是误认为字典在所有场合都更快，忽略了它的快只对「键」这一列成立。"},
        {"q": "关于「按值查找」和「按下标读取」，下面哪种判断最站得住脚？",
         "options": [("前者要逐个比对，代价随数据量增长；后者是一次定位，与数据量无关", True),
                     ("两者的比较次数差不多，只是写法不同", False),
                     ("按下标读取更慢，因为要先数到那个位置", False)],
         "explain": "两者的本质差别就是「要不要一个个比过去」。<strong>错因提醒：</strong>容易把按下标读取想象成「从头数过去」，其实它是一次直接定位——正是这个差别，让同一个列表在不同用法下性能天差地别。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：给四个需求各配一种结构", TTS["synthesis"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">为下面四个需求各选一种组织方式。没有哪种结构天生更好，关键是和需求对不对得上。</p>
        <div class="lab-panel">
          <div id="syn-stage">
            <div class="inner-card">
              <p><strong>需求一：</strong>记录一列按先后到达的测量值，之后要按顺序逐个处理。</p>
              <div class="flex-row" style="margin-top:8px">
                <button class="choice" data-syn="n1" data-opt="list" style="text-align:center">用列表</button>
                <button class="choice" data-syn="n1" data-opt="dict" style="text-align:center">用字典</button>
                <button class="choice" data-syn="n1" data-opt="both" style="text-align:center">列表套字典</button>
              </div>
            </div>
            <div class="inner-card">
              <p><strong>需求二：</strong>用学号直接查出某个学生的姓名。</p>
              <div class="flex-row" style="margin-top:8px">
                <button class="choice" data-syn="n2" data-opt="list" style="text-align:center">用列表</button>
                <button class="choice" data-syn="n2" data-opt="dict" style="text-align:center">用字典</button>
                <button class="choice" data-syn="n2" data-opt="both" style="text-align:center">列表套字典</button>
              </div>
            </div>
            <div class="inner-card">
              <p><strong>需求三：</strong>保存全班学生记录：既要整体遍历，又要按学号查单个。</p>
              <div class="flex-row" style="margin-top:8px">
                <button class="choice" data-syn="n3" data-opt="list" style="text-align:center">用列表</button>
                <button class="choice" data-syn="n3" data-opt="dict" style="text-align:center">用字典</button>
                <button class="choice" data-syn="n3" data-opt="both" style="text-align:center">列表套字典</button>
              </div>
            </div>
            <div class="inner-card">
              <p><strong>需求四：</strong>统计每个分数段各有多少人。</p>
              <div class="flex-row" style="margin-top:8px">
                <button class="choice" data-syn="n4" data-opt="list" style="text-align:center">用列表</button>
                <button class="choice" data-syn="n4" data-opt="dict" style="text-align:center">用字典</button>
                <button class="choice" data-syn="n4" data-opt="both" style="text-align:center">列表套字典</button>
              </div>
            </div>
          </div>
          <p class="result warn" id="syn-out" style="margin-top:12px"></p>
          <div class="flex-row">
            <button class="choice" id="syn-run" style="text-align:center;flex:1">检查这份设计</button>
            <button class="choice" id="syn-reset" style="text-align:center;flex:1">重置</button>
          </div>
        </div>
        <div class="inner-card">
          <p><strong>写下来，说给同桌听：</strong>如果需求三的数据量从四十条涨到四万条，你的设计会有什么变化？哪一步的代价会明显上升？</p>
          <textarea id="syn-answer" rows="3" placeholder="数据变多之后，……这一步的代价会上升，因为……所以我打算……"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换一个情境，看看规律还在不在", TTS["posttest"], [
        {"q": "图书馆要管理借阅记录：一条记录里有借书证号、书名、借出日期。要按借书证号快速查出这个人借了哪些书，最合适的做法是：",
         "options": [("把借书证号当作键，值是这个人借的书，存成字典", True),
                     ("把所有记录按借出时间排成一个列表，查找时从头比对", False),
                     ("给每个借书证号单独起一个变量名，分别记住", False)],
         "explain": "需求问的是「某个标识对应什么」，键恰好就是这个标识，字典一次定位即可。<strong>错因提醒：</strong>第二个选项不是做不到，而是每次都要比过全部记录；把「能实现」当成「合适」，是这一课最需要纠正的判断。"},
        {"q": "一个采集设备连续记录温度读数，每分钟一条，事后要按时间顺序画出变化曲线。这份数据最应该用：",
         "options": [("列表保存，因为先后顺序本身就是这份数据要保留的信息", True),
                     ("字典保存，因为字典查找更快", False),
                     ("字典保存，键为温度值、值为出现次数", False)],
         "explain": "这里的需求是「按顺序处理」，字典反而会丢掉顺序。<strong>错因提醒：</strong>常见错误是误认为字典处处更好、无脑选字典；结构的选择依据是需求，不是「谁听起来更高级」。"},
        {"q": "一个列表有 500 个元素，另一个字典有 500 个键值对。要判断「里面有没有某个值」，下面哪种说法是对的？",
         "options": [("在列表里按值查找最坏要比较 500 次；在字典里按键查找只需一次定位，前提是查的正好是键", True),
                     ("两者都只要一次，因为规模一样大", False),
                     ("字典一定更快，不管查的是键还是值", False)],
         "explain": "字典的优势只作用在「键」上，换一个字段去查，仍然要逐个比过去。<strong>错因提醒：</strong>把字典当成「无条件更快」，忽略了这个前提，是很容易犯的错误。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把自己讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>列表</strong>：按顺序保存一组数据，下标从 0 开始；按下标访问是一次定位，按值查找要逐个比对，中间插删要挪位。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>字典</strong>：用键定位值，键在同一个字典里唯一；它靠额外空间记下键与值的对应关系，换来一次定位的查找速度。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>选择的依据</strong>：问「第几个」用列表，问「叫什么」用字典；两种需求同时存在时，把字典放进列表，两者兼得。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:var(--warm)">
          <p style="margin:0"><strong>回到开头那个班：</strong>把四十条记录装进一个列表按座位顺序保存，另外建一个「学号到位置」的字典。要整体遍历就顺着列表走，要按学号找人就直接查字典——同一个班的数据，两种结构各管一件事，麻烦就不见了。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「下标、键、逐个比对、一次定位」这四个词，说清楚列表和字典分别在什么场合更合适。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "写出列表与字典各一条取值写法，并说明列表的下标从几开始、字典的键有什么限制。",
            "列举列表的四种常用操作，并各写一句它会不会发生比较、要不要挪动其他元素。",
            "说明「按下标读取」与「按值查找」在比较次数上的差别，并各举一个适合它们的场景。",
        ],
        [
            "给出五条学生记录（学号、姓名、成绩），分别用列表和字典各组织一次，并写出「按学号查成绩」的两段伪代码。",
            "画出自己设计的列表结构：标出每个元素的下标，并画出在中间插入一个元素之后，哪些元素的位置发生了变化。",
        ],
        [
            "为自己的一个真实需求（管理错题、记录运动数据、整理阅读清单）设计数据组织方式，说明为什么这样选。",
            "在上一题基础上推算：数据量从几十条涨到几万条时，哪一步的代价会明显上升？你会怎样改造这份设计？",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-m-data-structures-basic",
    "node_id": "it-m-data-structures-basic",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "middle",
    "stage_cn": "初中",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 初中",
    "title": "数据结构基础（列表/字典）",
    "name_en": "Data Structures: Lists and Dictionaries",
    "grade": 8,
    "grade_cn": "八年级",
    "domain": "data-algorithms",
    "domain_cn": "数据与算法",
    "lesson_type": "concept-inquiry",
    "version": "1.0.0",
    "description": "从「四十条成绩无法用四十个变量保存」的真实麻烦出发，学会用列表保存有序数据并理解下标从 0 开始，掌握按下标访问与按值查找在代价上的差别，学会用字典按键定位值并理解键的唯一性与以空间换时间，能针对真实需求在列表与字典之间做出选择并说明理由。",
    "tags": ["数据结构", "列表", "字典", "下标", "键值对", "查找代价", "数据组织"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》初中「数据与算法」——运用列表、字典等结构组织与管理数据。",
    "hero_question": "一个班四十个人的成绩，如果每人一个变量，还能问出「谁最高」这个问题吗？",
    "hero_alt": "数据结构基础知识结构图：需求、列表、字典三栏",
    "hero_caption": "先问需求（要第几个·要叫什么）→ 列表（下标·顺序·逐个比对）→ 字典（键·对应关系·一次定位）",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的实验都会围着它转。",
    "anchor_choices": [
        {"t": "列表的下标为什么从 0 开始？", "d": "从 1 开始不是更顺吗", "v": "列表的下标为什么从 0 开始"},
        {"t": "字典凭什么不用一个个比就能找到？", "d": "它的快是从哪里来的", "v": "字典凭什么不用一个个比就能找到"},
        {"t": "同样的数据，为什么换个存法代价差很多？", "d": "按下标读和按值找到底差在哪", "v": "同样的数据，为什么换个存法代价差很多"},
        {"t": "面对一个真实需求，我该选列表还是字典？", "d": "有没有可操作的判断依据", "v": "面对一个真实需求，我该选列表还是字典"},
    ],
    "objectives": [
        "能用列表保存一组有序数据，说清下标从 0 开始以及合法下标的范围",
        "能说明按下标访问与按值查找在比较次数上的差别，并解释代价与数据量的关系",
        "能用字典按键保存与取出数据，说清键的唯一性以及它相对列表的取舍",
        "能针对真实需求在列表与字典之间做出选择并说明理由，必要时把两者组合使用",
    ],
    "objectives_plain": [
        "能用列表保存一组有序数据，说清下标从 0 开始以及合法下标的范围",
        "能说明按下标访问与按值查找在比较次数上的差别，并解释代价与数据量的关系",
        "能用字典按键保存与取出数据，说清键的唯一性以及它相对列表的取舍",
        "能针对真实需求在列表与字典之间做出选择并说明理由，必要时把两者组合使用",
    ],
    "standards": [
        {"content": "运用列表、字典等结构组织与管理数据。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》数据与算法 · 初中"},
        {"content": "在真实情境中组织数据，理解不同组织方式在效率上的差异，形成用数据解决问题的意识。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》数据与算法 / 数据与编码 · 初中"},
    ],
    "prereqs": [],
    "prereqs_name": "无（初中数据与算法起点）",
    "prereqs_meta": "无",
    "leads_to": ["it-m-data-analysis"],
    "next_meta": "it-m-data-analysis",
    "section_images": ["assets/it-m-data-structures-basic-fig1.webp", "assets/it-m-data-structures-basic-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "四十条成绩，每人一个变量就撑不住了——把一组数据装进一个整体，是这一课要解决的事。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能为任何一个需求说出该用列表还是字典，并讲清理由。",
        "objectives": "看清四件事：下标从 0 开始、两种访问代价不同、键的唯一性与取舍、按需求选结构。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "下标从 0 开始；按下标读取是一次定位，按值查找要逐个比对，中间插删要挪位。",
        "lab-1": "同一个元素，按下标读是 1 步，按值找可能要 5 步。插入删除比较次数是 0，但元素要挪位。",
        "module-2": "字典用键定位值，键唯一；它靠额外的空间换来更快的查找，但只有查的字段正好是键时才成立。",
        "lab-2": "多跑几次：列表的汇总数字每次都不一样，字典永远是「次数 × 1」。",
        "worked-example": "同一份数据三种需求：按学号查用字典，排名用列表，统计分数段还是字典——先问需求再定结构。",
        "conceptest-1": "干扰项里藏着最常见的那几个错误想法，选完看清每一个解释。",
        "synthesis": "先问一句：这个需求问的是「第几个」还是「叫什么」？两者都有就组合起来。",
        "posttest": "换了借阅记录和温度读数的新情境，看看你还能不能用上下标、键和两种代价的知识。",
        "summary": "用「下标、键、逐个比对、一次定位」四个词，把两种结构讲给同桌听。",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是初中「数据与算法」领域的结构基础课。设计上不引入任何真实产品与品牌，伪代码一律使用中文关键字（如「按下标读取」「人数[分数段] = 人数[分数段] + 1」），把力气花在三件可操作、可观察的事上：用列表操作台把「按下标读取」与「按值查找」的差别变成实时跳动的比较次数与累计计数，让学生自己发现同样是列表、换一种用法代价就完全不同；用两种查找的对比台把「逐个比对」与「一次定位」变成同一批数据上的两组可比较数字，并暴露列表每次波动、字典始终稳定的差别；用数据组织选择器让学生为四个真实需求各选一种结构，并从「能实现但不合适」这类选项里理解结构选择依据的是需求而不是喜好。价值取向上强调数据组织方式的选择直接关系到效率与资源消耗，也提示字典的优势有其前提，不是无条件的更快。",
    "plan_table": """| 1 | cover | 数据结构基础（列表/字典） | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：一组数据该怎么装起来？ | 起·前测（暴露直觉） |
| 5 | concept | 列表：一组有序数据，用下标定位 | 承·概念一 |
| 6 | interactive | 列表操作台：哪种用法要比较很多次？ | 承·实验室一（比较次数可观察） |
| 7 | concept | 字典：用键定位值，用空间换时间 | 承·概念二 |
| 8 | interactive | 两种查找的对比台：到底差多少次比较？ | 承·实验室二（两种代价可对比） |
| 9 | concept | 例题示范：同一份数据，三种需求三种组织 | 转·重难点突破（分步示范 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：给四个需求各配一种结构 | 合·迁移应用（按需求选结构） |
| 12 | quiz | 后测：换一个情境，看看规律还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把自己讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：需求 / 列表 / 字典三栏标注\n- P5 列表结构图（已生成）：带下标的格子，以及按下标读取与按值查找两条路径\n- P7 字典键值映射图（已生成）：学号到姓名的对应关系，以及两种结构的选择对照\n- 若需补充：不含任何品牌标识的储物柜、座位表等生活类比示意图",
}
