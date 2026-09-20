# -*- coding: utf-8 -*-
"""小学信息科技 · 数据可视化表达（G4）—— 补齐知识树「数据与编码」空缺

学科语气：信息科技 = 概念 + 动手并重。
本课只做两件真能上手的事：
  ① 核心模拟：同一份数据，切换柱状图 / 折线图 / 饼图 → 现场用画布重画，
     并且每次都告诉你这种配法合不合适、为什么（比多少 / 看变化 / 看占比）
  ② 挑图台：六张「想说明什么」的卡片，放进比多少 / 看变化 / 看占比三个筐里
最后收口到一条可带走的规则：看清数据 → 想说明什么 → 选图；
比多少用柱子，看变化用折线，看占比用饼图。

说明：课件里的图表都由本页绘图程序现场画出，属教学示意图；不涉及任何真实软件界面、截图或商标。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-e-data-visualization-fig1.webp'
F2 = './assets/it-e-data-visualization-fig2.webp'

TTS = {
    "hero": "先请你想象一件事。老师让你统计班上同学最喜欢的运动，你问了一圈，记下四个数字：篮球十二人，足球九人，跳绳十五人，乒乓球六人。数字是记下来了，可同学们盯着这四个数字，还是说不清喜欢跳绳的到底算多还是算少。这时候，只要把它们画成一张图，柱子一根根立起来，谁多谁少一眼就看出来了。今天这节课，我们就来学怎么把数据画成图，还要弄明白什么样的数据该配什么样的图。",
    "problem-anchor": "在开始之前，先选一个你最想弄明白的问题。是想知道表格里的数字怎么变成一张图，还是想知道柱状图、折线图和饼图分别在什么时候用，又或者你想弄明白同一份数据换成不同的图，说出来的话会不会不一样，再或者你想学会把一张图看懂，用一句话把结论说出来。选好了，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出把数据画成图表，比一堆数字更容易看出多少和变化。第二，能认出柱状图、折线图和饼图，并说出各自适合的场合：比多少用柱子，看变化用折线，看占比用饼图。第三，能根据自己想说明的问题，给一份数据挑一种合适的图，并能说出理由。第四，能读出一张图讲的事情，用一句话说出结论，并知道图上要有标题和单位。",
    "pretest": "先做三道小题，用你现在的想法选就行。选完马上能看到解释，选错了也没关系，正好知道该重点听哪里。",
    "module-1": "我们先看看数据是怎么变成图的。你统计出来的四个数字，写在纸上就是一行数字；可把它们画成四根柱子，从高到矮排在一起，谁多谁少立刻就看出来了。把数据画成图，就叫数据可视化。它能办三件事：第一，比多少，谁多谁少，柱子的高矮直接说；第二，看变化，一段时间里是怎么变的，用一条线说得清清楚楚；第三，看占比，一部分占整体的多少，用一整块分成几份来表示。",
    "lab-1": "现在轮到你自己动手了。下面有三份不同的数据，还有三种图。你可以随便换：换一份数据，再换一种图，看看画出来的样子有什么不一样。每换一次，下面都会告诉你这种配法合不合适、为什么。多试几组，你会发现一件有意思的事：同一份数据换成不同的图，你能看出来的东西真的不一样。",
    "module-2": "接下来把选图的窍门说清楚。三种图各有一件最拿手的事。柱状图拿手的是比多少，几根柱子站在一起，谁高谁多。折线图拿手的是看变化，把各个点连成线，往上走就是变多；不过它只适合有先后顺序的数据，比如时间。饼图拿手的是看占比，整个圆是一个整体，每一块扇形是其中的一部分。选图只要走三步：先看清数据是什么样子，再想清楚自己想说明什么，最后挑一种图，别忘了写上标题和单位。",
    "lab-2": "下面请你当一次小编辑。这里有六张卡片，每一张写的都是一个人想说明的问题。请你读一读，然后把它放进你认为最合适的那个筐里：是想比多少，想看变化，还是想看占比。放对了会告诉你理由，放错了也会提醒你哪里想偏了。",
    "worked-example": "我们一起来分析一道题。这是四（1）班一周的借书量：周一十二本，周二十五本，周三二十本，周四十六本，周五十本。第一步，先看清数据：这是五天里每天的借书量，按周一到周五排的，有时间先后。第二步，想清楚要说明什么：想说周三借得最多，从周三以后一天比一天少。第三步，选图：有先后、要看变化，折线图最合适；柱状图也能比出高矮，但折线更容易看出往上还是往下。第四步，把结论写成一句话：周三借书最多，有二十本；从周三到周五一天比一天少。",
    "conceptest-1": "接下来用三个容易弄错的说法考考你。请仔细读每一个选项，选完再看解释。",
    "synthesis": "最后一个任务交给你。学校四个年级的图书角藏书量分别是：一年级一百二十本，二年级一百五十本，三年级一百八十本，四年级二百一十本。你要用一张图说明，四年级的藏书最多。请你自己选一种图，还可以把标题和单位关掉、再打开，看看有什么不一样，然后把你想说的那句话写在下面。",
    "posttest": "最后一轮，换几个新的情境来考考你。这次会出现运动会成绩、每月气温和一张画错了的图，看看你能不能把学到的规则用上去。",
    "summary": "这节课我们记住三句话。第一句，把数据画成图，就叫数据可视化，它让多少和变化变得看得见。第二句，选图三步：看清数据，想清楚要说明什么，再选图；比多少用柱子，看变化用折线，看占比用饼图。第三句，一张好图要让人看得懂：有标题、有单位、类别名字写清楚，读完能说出一句结论。回到开头那四个数字：画成图以后，同学们一眼就看出喜欢跳绳的人最多，这就是图的力量。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出柱状图、折线图、饼图各拿手一件事。第二层能力应用，动手做：统计你家里一周每天的用水量，用一张图把它画出来，并写明这张图想说明什么。第三层迁移挑战，选做：找一个你在新闻或者课本上看到的数据图表，说说它选了什么图、想说明什么问题，再想一想，如果换成另一种图，会丢掉什么信息。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是学它之前要先会的，右边是学会之后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续学的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 数据画成图就看得见", "lab-1": "动手一 同一份数据换三种图",
    "module-2": "概念二 三种图各拿手什么", "lab-2": "动手二 给数据挑一张合适的图",
    "worked-example": "例题讲解 一周借书量怎么说", "conceptest-1": "概念测试",
    "synthesis": "综合任务 四个年级的藏书量", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# 动手二：六张「想说明什么」的卡片 → 比多少 / 看变化 / 看占比
ASK_CARDS = [
    ("c1", "想说明这一周里气温一天比一天高", "trend",
     "按周一到周日排下来，说的是随时间变多变少——这是「看变化」，用折线图。"),
    ("c2", "想说明最喜欢的运动里，跳绳占了全班的三分之一", "share",
     "全班人数是一个整体，跳绳是其中一份——这是「看占比」，用饼图。"),
    ("c3", "想说明四个年级的图书角里哪个年级的书最多", "compare",
     "四个年级是并列的，比的是谁多谁少——这是「比多少」，用柱状图。"),
    ("c4", "想说明从一月到六月，每月的用水量越来越少", "trend",
     "从一月到六月有时间先后，想说的是「越来越少」——这是「看变化」，用折线图。"),
    ("c5", "想说明一袋混合糖果里，五种口味各占多少", "share",
     "一整袋糖果是一个整体，五种口味是其中的几份——这是「看占比」，用饼图。"),
    ("c6", "想说明三家文具店里，哪一家的笔记本最便宜", "compare",
     "三家店是并列的，比的是谁贵谁便宜——这是「比多少」，用柱状图。"),
]

BINS = [
    ("compare", "🟦 比多少（谁多谁少）"),
    ("trend", "🔺 看变化（随时间变多变少）"),
    ("share", "🟡 看占比（一部分占整体多少）"),
]

CUSTOM_JS = r"""
/* ============================================================
   it-e-data-visualization 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) dvDraw()：用画布现场画出 柱状图 / 折线图 / 饼图
      （颜色一律取自主题变量；标题、单位可以开关）
   3) 动手一：三份数据 × 三种图 → 实时重绘 + 是否合适的解释
   4) 动手二：六张卡片放进 比多少 / 看变化 / 看占比 三个筐
   5) 综合任务：换图 + 开关标题与单位
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

  /* ---------- 2. 画布绘图器 ---------- */
  var FONT = '-apple-system, BlinkMacSystemFont, "PingFang SC", "Source Han Sans SC", sans-serif';

  /* 补齐可点控件的边框与选中态：库内部分颜色写法会被浏览器整条丢弃 */
  var st = document.createElement('style');
  st.textContent =
    '.choice{border:1.5px solid rgb(var(--brand-rgb) / 32%);background:var(--card);}' +
    '.choice:hover{background:var(--brand-soft);border-color:rgb(var(--brand-rgb) / 55%);}' +
    '.choice.selected{border-color:var(--brand);background:rgb(var(--brand-rgb) / 13%);box-shadow:0 0 0 3px rgb(var(--brand-rgb) / 16%);}' +
    '.sort-item{border:1.5px solid rgb(var(--brand-rgb) / 30%);background:var(--card);}' +
    '.sort-item:hover{box-shadow:0 4px 12px rgb(var(--paper-rgb) / 22%);}' +
    '.sort-bin{border-color:rgb(var(--paper-rgb) / 50%);}' +
    '.kid-note{border-color:rgb(var(--warm-rgb) / 80%);}' +
    '.canvas-wrap{border-color:rgb(var(--paper-rgb) / 22%);}';
  document.head.appendChild(st);

  function theme() {
    var cs = getComputedStyle(document.body);
    function v(k, d) { var x = cs.getPropertyValue(k).trim(); return x || d; }
    return {
      brand: v('--brand', '#ff6b6b'), brand2: v('--brand-2', '#4ecdc4'), warm: v('--warm', '#ffd166'),
      muted: v('--muted', '#94866c'), text: v('--text-strong', '#3a3126'), line: v('--line', '#f2e3c9')
    };
  }

  function dvDraw(cv, type, ds, opts) {
    if (!cv) return;
    opts = opts || {};
    var T = theme();
    var PAL = [T.brand, T.brand2, T.warm, '#a78bfa', '#7fc8f8', '#c99a5b', '#f0a4a4'];
    var W = Math.max(300, Math.round(cv.clientWidth || 600));
    var H = 320;
    var dpr = window.devicePixelRatio || 1;
    cv.width = Math.round(W * dpr);
    cv.height = Math.round(H * dpr);
    cv.style.height = H + 'px';
    var g = cv.getContext('2d');
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.clearRect(0, 0, W, H);
    g.textBaseline = 'middle';
    var LAB = '13px ' + FONT, LABB = 'bold 14px ' + FONT;
    var vals = ds.values, names = ds.labels, n = vals.length;
    var showTitle = opts.showTitle !== false, showUnit = opts.showUnit !== false;
    var padT = showTitle ? 50 : 24;

    if (showTitle) {
      g.font = LABB; g.fillStyle = T.text; g.textAlign = 'center';
      g.fillText(ds.name + (showUnit ? '（单位：' + ds.unit + '）' : ''), W / 2, 20);
    }

    if (type === 'pie') {
      var total = vals.reduce(function (a, b) { return a + b; }, 0);
      var cy = padT + (H - padT - 24) / 2;
      var R = Math.min(W * 0.2, (H - padT - 24) / 2 - 8);
      var cx = Math.max(R + 24, W * 0.28);
      var ang = -Math.PI / 2;
      vals.forEach(function (v, i) {
        var a2 = ang + v / total * Math.PI * 2;
        g.beginPath(); g.moveTo(cx, cy); g.arc(cx, cy, R, ang, a2); g.closePath();
        g.fillStyle = PAL[i % PAL.length]; g.fill();
        g.strokeStyle = '#ffffff'; g.lineWidth = 2; g.stroke();
        var mid = (ang + a2) / 2, pct = Math.round(v / total * 100);
        if (pct >= 8) {
          g.fillStyle = '#ffffff'; g.font = LABB; g.textAlign = 'center';
          g.fillText(pct + '%', cx + Math.cos(mid) * R * 0.62, cy + Math.sin(mid) * R * 0.62);
        }
        ang = a2;
      });
      var lx = cx + R + 34;
      vals.forEach(function (v, i) {
        var ly = padT + 20 + i * 26;
        if (ly > H - 20) return;
        g.fillStyle = PAL[i % PAL.length];
        g.fillRect(lx, ly - 7, 14, 14);
        g.fillStyle = T.text; g.font = LAB; g.textAlign = 'left';
        g.fillText(names[i] + ' ' + v + (showUnit ? ' ' + ds.unit : ''), lx + 22, ly);
      });
      return;
    }

    /* 柱状图 / 折线图共用坐标轴 */
    var padL = 56, padR = 26, padB = 56;
    var pw = W - padL - padR, ph = H - padT - padB;
    var maxV = Math.max.apply(null, vals);
    var top = maxV * 1.18;
    var x0 = padL, y0 = padT + ph;
    g.strokeStyle = T.line; g.lineWidth = 1;
    g.beginPath(); g.moveTo(x0, padT); g.lineTo(x0, y0); g.lineTo(x0 + pw, y0); g.stroke();
    g.font = LAB; g.textAlign = 'right';
    [0, Math.round(maxV / 2), maxV].forEach(function (v) {
      var y = y0 - (v / top) * ph;
      g.strokeStyle = T.line;
      g.beginPath(); g.moveTo(x0, y); g.lineTo(x0 + pw, y); g.stroke();
      g.fillStyle = T.muted; g.fillText(String(v), x0 - 8, y);
    });
    if (showUnit) {
      g.fillStyle = T.muted; g.font = LAB; g.textAlign = 'left';
      g.fillText(ds.unit, 6, padT - 10);
    }
    var slot = pw / n;

    if (type === 'bar') {
      var bw = Math.min(66, slot * 0.56);
      vals.forEach(function (v, i) {
        var cx = x0 + slot * (i + 0.5), bh = (v / top) * ph;
        g.fillStyle = PAL[i % PAL.length];
        g.fillRect(cx - bw / 2, y0 - bh, bw, bh);
        g.fillStyle = T.text; g.font = LABB; g.textAlign = 'center';
        g.fillText(String(v), cx, y0 - bh - 13);
        g.fillStyle = T.muted; g.font = LAB;
        g.fillText(names[i], cx, y0 + 18);
      });
      return;
    }

    var pts = vals.map(function (v, i) {
      return [x0 + slot * (i + 0.5), y0 - (v / top) * ph];
    });
    g.strokeStyle = T.brand; g.lineWidth = 3; g.lineJoin = 'round';
    g.beginPath();
    pts.forEach(function (p, i) { if (i) g.lineTo(p[0], p[1]); else g.moveTo(p[0], p[1]); });
    g.stroke();
    pts.forEach(function (p, i) {
      g.fillStyle = T.brand2;
      g.beginPath(); g.arc(p[0], p[1], 5.5, 0, Math.PI * 2); g.fill();
      g.fillStyle = T.text; g.font = LABB; g.textAlign = 'center';
      g.fillText(String(vals[i]), p[0], p[1] - 17);
      g.fillStyle = T.muted; g.font = LAB;
      g.fillText(names[i], p[0], y0 + 18);
    });
  }

  /* ---------- 数据与配图评价 ---------- */
  var DS = {
    week: {
      name: '一周借书量', unit: '本',
      labels: ['周一', '周二', '周三', '周四', '周五'], values: [12, 15, 20, 16, 10],
      desc: '这一周五天的借书量，按时间先后排的。'
    },
    sport: {
      name: '全班最喜欢的运动', unit: '人',
      labels: ['篮球', '足球', '跳绳', '乒乓球'], values: [12, 9, 15, 6],
      desc: '把全班同学按四种运动分成四份，合起来就是全班人数。'
    },
    grade: {
      name: '四个年级图书角藏书量', unit: '本',
      labels: ['一年级', '二年级', '三年级', '四年级'], values: [120, 150, 180, 210],
      desc: '四个年级各自的数量，年级之间是并列的。'
    }
  };

  var CT = {
    bar: '柱状图', line: '折线图', pie: '饼图'
  };

  var RATE = {
    week: {
      line: { lv: 'good', t: '折线图最合适。线往上走就是变多、往下走就是变少——周三以后一天比一天少，这个趋势一眼就看出来了。' },
      bar: { lv: 'ok', t: '柱状图也可以用：能比出哪一天柱子最高。但它不容易看出「一天比一天多还是少」，变化要靠你自己一根一根去比。' },
      pie: { lv: 'bad', t: '不太合适。饼图讲的是「五天各占一周总量的多少」，你想说的「哪天最多、后来变少了」它就说不清楚了。' }
    },
    sport: {
      pie: { lv: 'good', t: '饼图很合适。整个圆就是全班人数，哪一块大就说明喜欢的人多，跳绳占了多少一眼可见。' },
      bar: { lv: 'good', t: '柱状图同样合适：四根柱子站在一起，谁多谁少立刻看出来，比饼图更容易比出高矮。' },
      line: { lv: 'bad', t: '不合适。四种运动之间没有先后顺序，把它们连成线没有意义——线往上走并不代表「这项运动变多了」。' }
    },
    grade: {
      bar: { lv: 'good', t: '柱状图最合适。四个年级的藏书量放在一起，谁高谁多，比得清清楚楚。' },
      pie: { lv: 'ok', t: '也可以用：能看出哪个年级占的比例大。不过要说明「四年级最多」，柱状图的高低差别看起来更直接。' },
      line: { lv: 'bad', t: '不合适。年级之间没有时间先后，连成折线会让人误以为「从一年级到四年级数字在变大」，其实它们只是四个并列的年级。' }
    }
  };

  /* ---------- 3. 动手一：换数据 / 换图 ---------- */
  var cv1 = document.getElementById('dv1-canvas');
  if (cv1) {
    var ds1 = 'week', ct1 = 'bar';
    var out1 = document.getElementById('dv1-out');
    var cap1 = document.getElementById('dv1-cap');

    function render1() {
      dvDraw(cv1, ct1, DS[ds1]);
      var r = RATE[ds1][ct1];
      out1.className = 'result ' + (r.lv === 'good' ? '' : (r.lv === 'ok' ? 'warn' : 'error'));
      out1.innerHTML = '<strong>' + DS[ds1].name + '　×　' + CT[ct1] + '：</strong>' + r.t;
      cap1.textContent = '正在看：' + DS[ds1].name + '（' + DS[ds1].desc + '）画成' + CT[ct1] + '。';
      document.querySelectorAll('[data-dv-ds]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.dvDs === ds1);
      });
      document.querySelectorAll('[data-dv-ct]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.dvCt === ct1);
      });
    }
    document.querySelectorAll('[data-dv-ds]').forEach(function (b) {
      b.addEventListener('click', function () { ds1 = b.dataset.dvDs; render1(); });
    });
    document.querySelectorAll('[data-dv-ct]').forEach(function (b) {
      b.addEventListener('click', function () { ct1 = b.dataset.dvCt; render1(); });
    });
    render1();
  }

  /* ---------- 4. 动手二：给数据挑一张合适的图 ---------- */
  var bank = document.getElementById('dv-bank');
  if (bank) {
    var picked = null, done = 0;
    var out2 = document.getElementById('dv-out');
    bank.querySelectorAll('.sort-item').forEach(function (card) {
      card.addEventListener('click', function () {
        if (card.classList.contains('done')) return;
        bank.querySelectorAll('.sort-item').forEach(function (c) { c.style.outline = 'none'; });
        card.style.outline = '3px solid var(--brand)';
        picked = card;
        out2.className = 'result warn';
        out2.textContent = '已选中「' + card.textContent.trim() + '」，现在点下面你认为对的那个筐。';
      });
    });
    document.querySelectorAll('[data-dv-bin]').forEach(function (bin) {
      bin.addEventListener('click', function () {
        if (!picked) {
          out2.className = 'result warn';
          out2.textContent = '先点上面的一张卡片，再点筐。';
          return;
        }
        var want = picked.dataset.kind, got = bin.dataset.dvBin;
        picked.style.outline = 'none';
        if (want === got) {
          var tag = document.createElement('span');
          tag.className = 'tag';
          tag.textContent = picked.textContent.trim() + ' ✓';
          bin.querySelector('.bin-body').appendChild(tag);
          picked.classList.add('done');
          picked.disabled = true;
          done++;
          out2.className = 'result';
          out2.innerHTML = '<strong>放对了！</strong>' + picked.dataset.why;
          picked = null;
          if (done === 6) {
            out2.innerHTML = '<strong>六张卡片全部归位。</strong>判断的窍门就一句话：先看数据是不是<strong>按时间排</strong>的——' +
              '是，就看变化，用折线图；不是，再看你要说的是<strong>「谁多谁少」</strong>还是<strong>「占整体多少」</strong>——' +
              '前者用柱状图，后者用饼图。';
          }
        } else {
          out2.className = 'result error';
          out2.innerHTML = '<strong>再想一下：「' + picked.textContent.trim() + '」</strong>' +
            '先问自己两句话：这里的数字是<strong>按时间排</strong>的吗？我想说的是<strong>谁多谁少</strong>，还是<strong>一部分占整体多少</strong>？<br>' +
            '<span style="color:var(--muted)">常见错误：把「谁多谁少」和「占整体多少」搞混——' +
            '柱子的高矮比的是多少，扇形的大小比的是占比。</span>';
          picked.style.outline = '3px dashed rgb(239 68 68 / 70%)';
        }
      });
    });
  }

  /* ---------- 5. 综合任务：换图 + 开关标题与单位 ---------- */
  var cv3 = document.getElementById('dv3-canvas');
  if (cv3) {
    var ct3 = 'line';
    var ckT = document.getElementById('dv3-title');
    var ckU = document.getElementById('dv3-unit');
    var out3 = document.getElementById('dv3-out');
    var SYN = {
      bar: { ok: true, t: '选得对！四个年级是并列的，要比的就是谁多谁少；柱子一高一低，四年级最高一眼就看出来。' },
      pie: { ok: false, t: '可以用，但不是最好：饼图讲的是「每个年级占全校藏书多少」，要看出「四年级最多」还得多看两眼比例。' },
      line: { ok: false, t: '不太合适：年级之间没有时间先后，连成折线会让人以为「数字在从一年级往四年级变」，其实它们只是并排的四个年级。' }
    };
    function render3() {
      dvDraw(cv3, ct3, DS.grade, { showTitle: ckT.checked, showUnit: ckU.checked });
      var r = SYN[ct3];
      var warn = (!ckT.checked || !ckU.checked);
      out3.className = 'result ' + (r.ok && !warn ? '' : 'warn');
      out3.innerHTML = '<strong>' + CT[ct3] + '：</strong>' + r.t +
        (warn ? '<br><span style="color:var(--muted)">再看一眼你的图：标题或者单位关掉以后，别人还看得懂吗？' +
          '不知道单位，就分不清柱子高矮说的是「本」还是「人」。</span>' : '');
      document.querySelectorAll('[data-dv-ct3]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.dvCt3 === ct3);
      });
    }
    document.querySelectorAll('[data-dv-ct3]').forEach(function (b) {
      b.addEventListener('click', function () { ct3 = b.dataset.dvCt3; render3(); });
    });
    ckT.addEventListener('change', render3);
    ckU.addEventListener('change', render3);
    render3();
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：这些数字，该配哪张图？", TTS["pretest"], [
        {"q": "想知道「这一周每天的气温是怎么变的」，用哪种图最合适？",
         "options": [("折线图", True), ("饼图", False), ("三种都一样，随便选", False)],
         "explain": "有时间先后、想看变化，折线图最合适：线往上就是变高，往下就是变低。"
                    "<strong>错因提醒：</strong>常见错误是觉得「有数字就能画饼图」——"
                    "饼图讲的是占比，看不出「一天天在变热还是变冷」。"},
        {"q": "班上有四个小组，想说明「第三组的人数最多」，用哪种图最容易一眼看出来？",
         "options": [("柱状图", True), ("饼图", False), ("折线图", False)],
         "explain": "四个小组是并排的，比的是谁多谁少，柱子一高一低最直接。"
                    "<strong>错因提醒：</strong>有同学误认为「只要是几比几就用饼图」——"
                    "饼图比的是「占整体多少」，要比多少还是柱子清楚。"},
        {"q": "一张图上有柱子、有数字，却没有写标题和单位。会有什么问题？",
         "options": [("别人不知道这张图在说什么，也不知道数字代表多少本还是多少人", True),
                     ("没有关系，图好看就行", False),
                     ("只要柱子画得准，不写也能看懂", False)],
         "explain": "标题说明这张图在讲什么，单位说明数字代表什么。少了它们，图就讲不清楚事情。"
                    "<strong>错因提醒：</strong>很多同学把力气都花在把图配色画漂亮上，"
                    "却忘了<strong>标题和单位</strong>才是别人看懂这张图的前提。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "一堆数字看不出门道，画成图就一眼看到", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们收集数据时，记下来的是一行一行的数字（And）；可数字要一个一个读、一个一个比，看半天也说不清谁多谁少（But）；把数字画成图，高矮长短直接摆在眼前，一眼就能看出来（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">把数据画成图，就叫<strong>数据可视化</strong>。它让「多少」和「变化」变成看得见的高矮、长短和走向。</p>
        <div class="grid grid-3">
          <div class="inner-card"><p><strong>① 比多少</strong></p><p style="color:var(--muted)">谁多谁少，柱子的高矮直接告诉你。</p></div>
          <div class="inner-card"><p><strong>② 看变化</strong></p><p style="color:var(--muted)">一段时间里怎么变的，看线条往上还是往下。</p></div>
          <div class="inner-card"><p><strong>③ 看占比</strong></p><p style="color:var(--muted)">一部分占整体的多少，看扇形有多大。</p></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="示意图：柱状图比多少、折线图看变化、饼图看占比，三种图表各自适合的场合">
          <figcaption>示意图：三种图表各拿手一件事——比多少用柱子，看变化用折线，看占比用饼图</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">📊</span><div><strong>举个例子：</strong>四个数字「篮球十二人、足球九人、跳绳十五人、乒乓球六人」，一眼看去分不清；画成四根柱子，谁最多立刻就看出来了。</div></div>
{insight_box([
    {"lens": "看见它", "text": "同样是四个数字，写在纸上是一行字，画成图却变成有高有矮的柱子——数字没变，你看到的东西变了。"},
    {"lens": "解释它", "text": "为什么图更容易看懂？因为眼睛比大小特别快：两根柱子谁高，你几乎不用想；两个数字谁大，还要读一遍再比。"},
    {"lens": "比较它", "text": "数据没变，换成不同的图，你注意到的重点就不一样：柱子让你比高低，折线让你看走向，饼图让你看比例。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：同一份数据，换三种图画画看", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先选一份数据，再选一种图，图会立刻重画一遍。多试几组，看看同一份数据换成不同的图，你能看出什么不一样。</p>
        <div class="lab-panel">
          <div class="slider-row" style="margin-top:0;display:block">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 选一份数据</div>
            <div class="flex-row" style="margin-top:0">
              <button class="choice" data-dv-ds="week" style="text-align:center">一周借书量</button>
              <button class="choice" data-dv-ds="sport" style="text-align:center">最喜欢的运动</button>
              <button class="choice" data-dv-ds="grade" style="text-align:center">四个年级藏书量</button>
            </div>
          </div>
          <div class="slider-row" style="margin-top:12px;display:block">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">② 选一种图</div>
            <div class="flex-row" style="margin-top:0">
              <button class="choice" data-dv-ct="bar" style="text-align:center">柱状图</button>
              <button class="choice" data-dv-ct="line" style="text-align:center">折线图</button>
              <button class="choice" data-dv-ct="pie" style="text-align:center">饼图</button>
            </div>
          </div>
          <div class="canvas-wrap" style="margin-top:12px">
            <canvas id="dv1-canvas" style="display:block;width:100%;border-radius:12px;" aria-label="图表互动画布"></canvas>
          </div>
          <p style="color:var(--muted);font-size:13px;margin:10px 0 0" id="dv1-cap"></p>
          <p class="result warn" id="dv1-out" style="margin-top:10px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>试一试：</strong>把「一周借书量」分别画成折线图和饼图，比一比——哪种图让你更快看出「周三以后一天比一天少」？（图由本页现场画出，为教学示意图）</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "三种图各拿手一件事，选图只要走三步", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">三种图没有谁更好，只有<strong>谁更合适</strong>。看清楚数据长什么样，再决定用哪一种。</p>
        <div class="step-grid">
          <div class="step"><span class="n">柱</span><div><strong>柱状图 · 比多少</strong>：几根柱子站在一起，谁高谁多。适合几个并列的类别互相比较。</div></div>
          <div class="step"><span class="n">线</span><div><strong>折线图 · 看变化</strong>：把各个点连成线，往上走就是变多。只适合<strong>有先后顺序</strong>的数据，比如时间。</div></div>
          <div class="step"><span class="n">圆</span><div><strong>饼图 · 看占比</strong>：整个圆是一个整体，每一块扇形是其中一部分。适合「一共就这些，分成几份」的数据。</div></div>
          <div class="step"><span class="n green">三</span><div><strong>选图三步</strong>：① 看清数据是什么样子 ② 想清楚要说明什么 ③ 选一种图，写上标题和单位。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="示意图：同一份一周借书量数据，分别画成柱状图、折线图与饼图的对照">
          <figcaption>示意图：同一份数据，三种画法——柱状图比高低，折线图看走向，饼图看每部分占多少</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">把<strong>没有先后顺序</strong>的数据连成折线。比如把「四种运动的人数」连成线，线往上走并不代表「运动变多了」——它们只是四个并排的类别。反过来，把有时间先后的数据画成饼图，也看不出「在变多还是变少」。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>比多少用柱子，看变化用折线，看占比用饼图；标题单位别忘记。</div></div>
    ''', tag="概念二"))

    card_btns = "\n".join(
        f'          <button class="sort-item" data-kind="{kind}" data-why="{why}">{t}</button>'
        for _k, t, kind, why in ASK_CARDS
    )
    bin_html = "\n".join(f'''            <div class="sort-bin" data-dv-bin="{k}">
              <h4>{label}</h4>
              <div class="bin-body"></div>
            </div>''' for k, label in BINS)
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：给每句话，挑一张合适的图", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一张卡片，再点你认为对的那个筐。每放一次都会立刻告诉你理由。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">待归位的六张卡片（每张是一句「我想说明什么」）</div>
          <div class="sort-bank" id="dv-bank">
{card_btns}
          </div>
          <div class="sort-bins" style="grid-template-columns:repeat(3,1fr)">
{bin_html}
          </div>
          <p class="result warn" id="dv-out" style="margin-top:12px">点一张卡片开始归位。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💡</span><div><strong>一个最快的判断办法：</strong>先看数据是不是按时间排的。是——想在时间里看变化，就用折线图；不是——再看你要说的是「谁多谁少」还是「一部分占整体多少」。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：一周借书量，怎么用图说明问题", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>四（1）班一周的借书量是：周一 12 本、周二 15 本、周三 20 本、周四 16 本、周五 10 本。请选一种合适的图，说明「周三借得最多，以后一天比一天少」。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看清数据：</strong>这是五天里每天的借书量，按周一到周五排的——它<strong>有时间先后</strong>，不是几个并排的类别。</div></div>
          <div class="step"><span class="n">2</span><div><strong>想清楚要说明什么：</strong>要说的是「哪天最多」和「后来在变少」，也就是<strong>变化</strong>。</div></div>
          <div class="step"><span class="n">3</span><div><strong>选图：</strong>有时间先后、要看变化，选<strong>折线图</strong>；柱状图也能比出高矮，但折线更容易看出往上还是往下。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>读出结论，写成一句话：</strong>「周三借书最多，有 20 本；从周三到周五，一天比一天少。」——图上还要写上标题和单位「本」。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">把这个数据画成饼图。五天的借书量加起来并不是「一整个整体分成的五份」，饼图只能告诉你哪天占得多，却说不出「一天比一天少」。另外，图上不写「单位：本」，别人就不知道柱子的高矮说的是本数还是人数。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三种说法，错在哪里", TTS["conceptest-1"], [
        {"q": "想说明「班上同学最喜欢的运动里，每种各占全班多少」，最合适的图是：",
         "options": [("饼图", True), ("折线图", False), ("柱状图都行，饼图完全没必要", False)],
         "explain": "全班人数是一个整体，每种运动是其中一份，看占比用饼图最直接。"
                    "<strong>错因提醒：</strong>柱状图也能比出多少，但要说「占了多少」，饼图的扇形大小更好懂。"},
        {"q": "下面哪一组数据，适合画成折线图？",
         "options": [("一天中每两小时记录一次的气温", True),
                     ("四种水果每斤的价格", False),
                     ("一袋糖果里五种口味的颗数", False)],
         "explain": "气温是随时间一个点一个点记录的，有时间先后，能看变化。"
                    "<strong>错因提醒：</strong>水果价格和糖果颗数都是并排的类别，没有先后顺序，连成折线毫无意义——"
                    "这是把折线图用错的最常见情形。"},
        {"q": "有同学说：「图只要画得漂亮就行，标题和单位写不写没关系。」这句话的问题是：",
         "options": [("别人不知道这张图在讲什么，也不知道数字代表什么", True),
                     ("没有关系，看图的人自己能猜", False),
                     ("只要颜色好看，信息少一点也没事", False)],
         "explain": "标题说清这张图在讲什么，单位说明数字是「本」还是「人」。缺了它们，图就讲不清楚事情。"
                    "<strong>错因提醒：</strong>很多同学误认为「图好看就够了」——可视化的目的是把事说清楚，不是比谁好看。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：让「四年级藏书最多」一眼看出来", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">数据：一年级 120 本、二年级 150 本、三年级 180 本、四年级 210 本。请挑一种图，让「四年级最多」一眼看得出来；再试试把标题和单位关掉会怎样。</p>
        <div class="lab-panel">
          <div class="flex-row" style="margin-top:0">
            <button class="choice" data-dv-ct3="bar" style="text-align:center">柱状图</button>
            <button class="choice" data-dv-ct3="line" style="text-align:center">折线图</button>
            <button class="choice" data-dv-ct3="pie" style="text-align:center">饼图</button>
          </div>
          <div class="canvas-wrap" style="margin-top:12px">
            <canvas id="dv3-canvas" style="display:block;width:100%;border-radius:12px;" aria-label="图表互动画布"></canvas>
          </div>
          <div class="flex-row" style="margin-top:8px">
            <label style="display:flex;align-items:center;gap:8px;font-size:14px;font-weight:700">
              <input type="checkbox" id="dv3-title" checked style="width:auto;min-height:auto"> 显示标题
            </label>
            <label style="display:flex;align-items:center;gap:8px;font-size:14px;font-weight:700">
              <input type="checkbox" id="dv3-unit" checked style="width:auto;min-height:auto"> 显示单位
            </label>
          </div>
          <p class="result warn" id="dv3-out" style="margin-top:12px"></p>
        </div>
        <div class="inner-card">
          <p><strong>选好以后，把结论写成一句话：</strong></p>
          <p style="color:var(--muted)">你选的是哪种图？为什么？图上写了标题和单位以后，这句话是不是更容易让别人看懂？</p>
          <textarea id="syn-answer" rows="3" placeholder="我选的是……因为……从图上可以看出……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个情境，规则还在不在", TTS["posttest"], [
        {"q": "运动会结束，体育老师想说明「四（2）班在六个项目上的得分，哪个项目最高」。最合适的图是：",
         "options": [("柱状图", True), ("折线图", False), ("饼图", False)],
         "explain": "六个项目是并列的，比的是谁高谁低，柱子最直接。"
                    "<strong>错因提醒：</strong>别一看到「六个数字」就想连成折线——项目之间没有先后顺序，连成线看不出任何趋势。"},
        {"q": "新闻里想说明「今年上半年每个月的气温是怎么变的」，画成饼图行不行？",
         "options": [("不行，饼图看不出「变高还是变低」，应该用折线图", True),
                     ("行，饼图也能看出哪个月最热", False),
                     ("行，只要把数字标上去就行", False)],
         "explain": "饼图讲的是占比，六个月的占比加起来是一整年——你想说的「变化」它讲不出来。"
                    "<strong>错因提醒：</strong>以为「饼图能看出哪个月最热」就够了的同学，忘了题目要说明的是「怎么变的」。"},
        {"q": "小华把「四种运动各自的人数」画成了折线图，还标出了每个点。这张图最大的问题是：",
         "options": [("四种运动没有先后顺序，那条线并不能说明「运动在变多」", True),
                     ("颜色不够好看", False),
                     ("点的位置画错了一个", False)],
         "explain": "折线只在数据有先后顺序时才有意义；四种运动是并排的类别，用柱状图或饼图才对。"
                    "<strong>错因提醒：</strong>「数字标对了」不等于「图选对了」——先想清楚数据长什么样，再决定画什么图。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把数据讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>数据可视化的作用：</strong>把数字画成图，让「多少」和「变化」变成看得见的高矮和走向。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>怎么选图：</strong>看清数据 → 想说明什么 → 选图；比多少用柱子，看变化用折线，看占比用饼图。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>一张好图的样子：</strong>有标题、有单位、类别名字写清楚，读完能说出一句结论。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那四个数字：</strong>篮球十二人、足球九人、跳绳十五人、乒乓球六人。写在纸上是一行数字，画成四根柱子，「喜欢跳绳的人最多」一眼就看出来了——数据没变，看懂它容易多了。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「比多少、看变化、看占比」这三个词，说清楚你在什么情况下会选哪种图。</p>
          <p style="color:var(--muted)">再动一动手：<strong>画出来</strong>——把你自己统计的一份数据画成图，写上标题和单位，并写一句话说出结论。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "说出柱状图、折线图、饼图各拿手一件事：比多少、看变化，还是看占比。",
            "写出一张图不能缺少的两样东西，并说说少了它们会有什么麻烦。",
        ],
        [
            "统计你家里一周每天的用水量，选一种合适的图把它画出来，并写明这张图想说明什么。",
            "找一张你见过的图（课本、新闻、墙上都行），说出它选了什么图、想说明什么问题。",
        ],
        [
            "把同一份数据画成两种不同的图，比较一下：哪一种更能说明问题？另一种丢掉了什么信息？写下来。",
            "设计一份自己的小调查（比如同学上下学的交通方式），收集数据、选图、画图，并写一句结论。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-e-data-visualization",
    "node_id": "it-e-data-visualization",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 小学",
    "title": "数据可视化表达",
    "name_en": "Data Visualization",
    "grade": 4,
    "grade_cn": "四年级",
    "domain": "data-encoding",
    "domain_cn": "数据与编码",
    "lesson_type": "concept-practice",
    "version": "1.0.0",
    "description": "面向小学四年级：知道把数据画成图比一堆数字更容易看出多少和变化；能认出柱状图、折线图与饼图并说出各自适合的场合；能根据想说明的问题给数据挑一种合适的图并说出理由；能读出一张图讲的事情，用一句话说出结论，并知道图上要有标题和单位。",
    "tags": ["数据可视化", "柱状图", "折线图", "饼图", "用图说话"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》小学「数据与编码」——用图表等方式呈现数据，辅助说明问题。",
    "hero_question": "同一份数据，为什么换一张图，别人看到的东西就完全不一样？",
    "hero_alt": "数据可视化表达知识结构图：收集到的数据、三种图表的拿手场合、用图说出一句结论",
    "hero_caption": "数据可视化：看清数据 · 选对图表 · 说出结论——比多少用柱子，看变化用折线，看占比用饼图",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的动手活动都会围着它转。",
    "anchor_choices": [
        {"t": "表格里一大堆数字，怎么才能一眼看出谁多谁少？", "d": "数字和图表到底差在哪里", "v": "表格里一大堆数字怎么才能一眼看出谁多谁少"},
        {"t": "柱状图、折线图、饼图，分别在什么时候用？", "d": "三种图各拿手什么", "v": "柱状图折线图饼图分别在什么时候用"},
        {"t": "同一份数据画成不同的图，说出来的话会不一样吗？", "d": "换图真的会改变结论吗", "v": "同一份数据画成不同的图说出来的话会不一样吗"},
        {"t": "一张图要画成什么样，别人才看得懂？", "d": "标题、单位和类别名字有什么用", "v": "一张图要画成什么样别人才看得懂"},
    ],
    "objectives": [
        "能说出把数据画成图表，比一堆数字更容易看出多少和变化",
        "能认出柱状图、折线图和饼图，并说出各自适合的场合",
        "能根据想说明的问题给一份数据挑一种合适的图，并说出理由",
        "能读出一张图讲的事情，用一句话说出结论，并知道图上要有标题和单位",
    ],
    "objectives_plain": [
        "能说出把数据画成图表，比一堆数字更容易看出多少和变化",
        "能认出柱状图、折线图和饼图，并说出各自适合的场合",
        "能根据想说明的问题给一份数据挑一种合适的图，并说出理由",
        "能读出一张图讲的事情，用一句话说出结论，并知道图上要有标题和单位",
    ],
    "standards": [
        {"content": "用图表等方式呈现数据，辅助说明问题",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 数据与编码"},
        {"content": "在真实的小调查中经历「收集数据—选择图表—说明问题」的过程，初步形成用数据说话的意识",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 数据与编码"},
    ],
    "prereqs": ["it-e-data-collection"],
    "prereqs_name": "数据收集与记录",
    "prereqs_meta": "it-e-data-collection",
    "leads_to": ["it-m-data-analysis"],
    "next_meta": "it-m-data-analysis",
    "section_images": ["assets/it-e-data-visualization-fig1.webp", "assets/it-e-data-visualization-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "四个数字摆在眼前，说不清谁多谁少；画成图，一眼就看出来了。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能给一份数据挑一张合适的图，并说出一句结论。",
        "objectives": "看清四件事：为什么画图、三种图各拿手什么、怎么选图、好图要有标题和单位。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "数据可视化能办三件事：比多少、看变化、看占比。",
        "lab-1": "换数据、换图，图会立刻重画。每换一次，读一读下面那句「合不合适、为什么」。",
        "module-2": "比多少用柱子，看变化用折线，看占比用饼图；折线只给有先后顺序的数据用。",
        "lab-2": "最快的判断办法：先看是不是按时间排的，再看你要说的是谁多谁少还是占整体多少。",
        "worked-example": "四步走：看清数据、想说明什么、选图、把结论写成一句话。",
        "conceptest-1": "三个说法里都藏着高频错误，选完把解释读一遍。",
        "synthesis": "四个年级是并排的，先想清楚你要说明的是「谁最多」还是「占多少」。",
        "posttest": "运动会成绩、每月气温、一张画错的图，看看你还能不能用上同一套规则。",
        "summary": "三句话：可视化有什么用、怎么选图、一张好图要有哪些东西。",
        "homework": "三层小任务，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学信息科技「数据与编码」在数据收集之后的一课。四年级学生的难点不在绘图技巧，而在两件事：一是不知道图表到底比数字好在哪，二是以为「有数字就能随便画一种图」。所以全课围绕一个可以一直动手的图画台展开：三份真实感的数据（一周借书量、全班最喜欢的运动、四个年级藏书量）配三种图，学生每换一次，画布就用程序现场重画一次，下面立刻说明「合不合适、为什么」——「一周借书量」配折线图最合适而配饼图说不了变化，「最喜欢的运动」配饼图或柱状图都行但折线毫无意义，这样三种图各自的拿手场合就被亲手试出来了。第二个动手台把六张「想说明什么」的卡片分进比多少、看变化、看占比三个筐，把选图从「看图形」拉回到「先想清楚要说明什么」。概念页收成一句口诀（比多少用柱子，看变化用折线，看占比用饼图；标题单位别忘记），例题页示范「看清数据—想说明什么—选图—写结论」四步，综合任务让学生自己换图并亲手把标题与单位关掉再打开，体会一张图为什么必须让人看懂。",
    "plan_table": """| 1 | cover | 数据可视化表达 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：这些数字，该配哪张图？ | 起·前测（暴露直觉） |
| 5 | concept | 一堆数字看不出门道，画成图就一眼看到 | 承·概念一（可视化的三个作用） |
| 6 | interactive | 动手一：同一份数据，换三种图画画看 | 承·核心模拟（三份数据 × 三种图，实时重绘 + 合适度解释） |
| 7 | concept | 三种图各拿手一件事，选图只要走三步 | 承·概念二（三图分工 + 选图三步 + 反例 + 口诀） |
| 8 | interactive | 动手二：给每句话，挑一张合适的图 | 承·挑图台（六张「想说明什么」卡片三分类） |
| 9 | concept | 例题示范：一周借书量，怎么用图说明问题 | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：三种说法，错在哪里 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：让「四年级藏书最多」一眼看出来 | 合·迁移应用（换图 + 标题/单位开关） |
| 12 | quiz | 后测：换几个情境，规则还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把数据讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：数据、三种图表、说出结论 三栏\n- P5 三种图表各拿手什么示意图（已生成）：比多少 / 看变化 / 看占比\n- P7 同一份数据三种画法对照图（已生成）：柱状图、折线图、饼图并列\n- 课件内的图表均由本页绘图程序现场画出，为教学示意图；不出现任何真实软件界面、截图或商标\n- 若需补充：学生自己统计并手绘的图表照片（需获得授权后使用）",
}
