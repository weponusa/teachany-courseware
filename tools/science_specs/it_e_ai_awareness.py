# -*- coding: utf-8 -*-
"""小学信息科技 · 人工智能初识（G6）—— 补齐知识树「互联网与人工智能」空缺

学科语气：信息科技 = 概念 + 动手并重。
本课不解释算法术语，只把一件事讲透：
  机器不是在「看懂」，它是在大量带标签的例子里找出一条规律，再照着规律猜。
两个动手实验室都真的能操作：
  ① 喂样本训练器（Canvas 二维散点图 + 最近邻）：
     在图上点一下就能加一个带标签的样本，机器立刻重画它的判断区域；
     鼠标挪到哪儿，就显示它此刻会把这里判成什么。
  ② 样本偏了，结论就偏（一维数轴 + 两类之间的分界线）：
     先用一组「成熟的全是大果」的样本训练，再看它怎么把一个小果品种判错；
     补进几个「小果但成熟」的样本，分界线移动之后，判断跟着改了。
最后收口到一句话：
  机器只会它见过的样子。样本里没有的，它就学不会。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-e-ai-awareness-fig1.webp'
F2 = './assets/it-e-ai-awareness-fig2.webp'

TTS = {
    "hero": "先问你一件事。你手机里的相册，为什么能自己认出照片里的猫？你打错一个字，它为什么能猜到你想打什么？很多人说，这是人工智能。可是它没有眼睛，也没有上过一天学，它凭什么会？答案其实很朴素：它看过非常非常多的例子，从例子里找到了一条规律。今天这节课，我们就亲手喂它几个例子，看它怎么学，也看它什么时候会学错。",
    "problem-anchor": "开始之前，先选一个你最想弄明白的问题。是想知道人工智能到底是怎么学会的，还是想知道它为什么有时候会判断错，又或者你想弄清楚它到底算不算真的聪明，再或者你想知道，如果让你来训练它，你会怎么做。选好了，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能用自己的话说出，人工智能是靠看大量带标签的例子来找规律的。第二，能在一个训练模拟里，通过添加和删除样本，让机器的判断跟着改变。第三，能说出样本偏了会带来什么后果，并举出一个例子。第四，能说清楚人工智能擅长什么、不擅长什么，不会把它当成什么都会的魔法。",
    "pretest": "先做三道小题，用你现在的想法选就行。选完马上能看到解释，选错了也没关系，正好知道该重点听哪里。",
    "module-1": "先把这件事说清楚。人工智能不是被谁一条一条写好了规则，而是我们先给它看一大批已经标好答案的例子，它自己从这些例子里找出规律来。这个过程分三步。第一步是喂例子，每个例子都带着一个标签，比如这张是苹果，那张是橙子。第二步是找规律，它在这些例子里找出一个能分开两类的办法。第三步是做判断，遇到一个没见过的新东西，它就照着找到的规律猜一个答案。这里要注意最后一句：它给出的是猜，是按规律算出来的最可能的那个答案，不是它真的看懂了。",
    "lab-1": "现在轮到你了。右边是一张图，横着是果实的大小，竖着是它偏红还是偏黄。你先选好这一颗要标成苹果还是橙子，然后在图上点一下，就喂给机器一个带标签的例子。机器每收到一个例子，都会重新画一遍它现在的判断。鼠标挪到哪儿，它就把那儿判成什么，还会画一条虚线连到离它最近的那个例子。先什么都不放试试看，你会发现没有例子的机器，什么也说不出来。",
    "module-2": "第二个问题：机器到底能学会什么？答案是，它只能学会你教过的那部分。三件事要记住。第一件，样本要够多，只见过三五个例子的机器，判断会非常随便。第二件，样本要够全，真实世界里会遇到的各种样子，都得让它在例子里见过。第三件，样本不能偏，如果你给它的例子里只有一种样子，它就会把这种样子当成全部的规律。一句话总结：样本里没有的，它就学不会；样本偏了，结论就偏。",
    "lab-2": "我们来做一个会出错的实验。先看上面这台分拣机，它是照着十二个例子学出来的。下面有三个果子，请你一个一点一下，让机器来判。判到第三个的时候，你会发现它出了错。错在哪里，先别急着看答案，自己想一想。想明白之后，点一下补充样本，再回来重新判一次，看看它的判断有没有改。",
    "worked-example": "我们一起把一道题想完整。学校想做一个识别垃圾信息的小助手，让它帮忙挡住班级群里的广告。第一步，先想清楚它要学会什么：把每一条消息分成广告和不是广告两类。第二步，准备例子：收集一千条消息，每一条都由人来标好答案。第三步，让它从这些例子里找规律。第四步，也是最重要的一步，检查一件事：如果这一千条例子里，广告全都是卖文具的，那遇到一条卖课程的广告，它还认得出来吗？很可能认不出来。因为它见过的广告只有一种样子。所以训练完之后，不能只看它答对了多少，还要专门去看那些它没见过的例子答得怎么样。",
    "conceptest-1": "接下来用三个容易弄错的说法考考你。请仔细读每一个选项，选完再看解释。",
    "synthesis": "最后一件事交给你。学校想做一个校园植物识别助手，请你来帮它准备训练样本。下面有十条候选做法，勾出你认为该用的那些，再点检查。做完之后你会发现，准备样本这件事，比想象中讲究得多。",
    "posttest": "最后一轮，换几个新的情境来考考你。这次会出现一个只认识自家小区里那种猫的识别器、一份全是某种车型的样本，还有一次「把机器当成什么都会」的提问。看看你能不能把样本和结论之间的关系用上去。",
    "summary": "这节课我们记住三件事。第一件，人工智能是在大量带标签的例子里找规律，再照着规律猜答案，它给出的是猜，不是看懂。第二件，样本要够多、够全、不能偏，样本里没有的样子，它就是学不会。第三件，样本偏了，结论就偏。回到开头那个问题——相册能认出猫，是因为它见过成千上万张被标好的猫的照片；换一只它从没见过的样子，它一样会认错。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：用自己的话说一说，机器学会一件事要经过哪三步，每一步在做什么。第二层能力应用，动手做：找一个你身边「会认东西」的功能，写出它可能是拿什么例子学出来的，再写出一个它可能会认错的情况。第三层迁移挑战，选做：给学校的植物识别助手设计一份训练样本清单，写清楚你会拍哪些植物、在什么时间拍、从什么角度拍，并说服同学为什么要这么麻烦。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是学它之前要先会的，右边是学会之后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续学的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 机器怎么学会一件事", "lab-1": "动手一 喂样本训练器", "module-2": "概念二 样本决定它能学会什么",
    "lab-2": "动手二 样本偏了结论就偏", "worked-example": "例题讲解 广告识别助手", "conceptest-1": "概念测试",
    "synthesis": "综合任务 植物识别助手的样本清单", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# 综合任务：10 条候选做法（good=1 该用 / 0 不该用）
SAMPLE_ITEMS = [
    ("g1", "同一种植物，在早晨、中午、树荫下都各拍一些照片", 1,
     "光线不一样，照片看起来差别很大。都拍过，机器才不会把「阴天的样子」当成「另一种植物」。"),
    ("g2", "同一种植物，正面、侧面、背面、叶子特写都拍一些", 1,
     "真实拍摄时的角度是随机的。角度覆盖得越全，实际用起来越稳。"),
    ("g3", "同一种植物，春夏秋冬各拍一些", 1,
     "植物会随季节变样子。只拍一个季节，换个季节它就认不出来了。"),
    ("g4", "让不同年级的同学，用不同的手机各拍一些", 1,
     "不同手机拍出来的颜色、清晰度都不一样。换一台设备就认错，说明样本太单一。"),
    ("g5", "校园里不同位置（花坛、操场边、教学楼后）的同一种植物都拍", 1,
     "同一种植物在哪儿长，背景就不一样。背景见得多了，机器才不会被背景带偏。"),
    ("g6", "每种植物都要拍够数量，不能有的几十张、有的只有两张", 1,
     "样本太少的类别，机器几乎学不到它的规律，判断会明显偏向样本多的那一类。"),
    ("b1", "只在晴天中午那一个时间去拍", 0,
     "样本偏了，结论就偏。只见过晴天中午的样子，阴天或傍晚拍的照片它就可能认不出。"),
    ("b2", "只用自己班窗台上那一盆植物拍", 0,
     "一盆植物只有一种长势、一种背景，机器会把「这盆花的样子」错当成「这种植物的样子」。"),
    ("b3", "每种植物只挑一张最漂亮的照片放进去", 0,
     "一张照片说明不了一种植物的变化。样本太少，机器等于没学到。"),
    ("b4", "只拍校园里最常见的三种植物，其他的先不管", 0,
     "训练时没见过的类别，机器就会硬把它塞进见过的某一类里，结果错得很自信。"),
]

CUSTOM_JS = r"""
/* ============================================================
   it-e-ai-awareness 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 动手一：喂样本训练器
      —— Canvas 二维散点 + 最近邻判断，实时重画判断区域
   3) 动手二：样本偏了，结论就偏
      —— 一维数轴 + 两类之间最大间隔中点作为分界线
   4) 综合任务：植物识别助手的样本清单（10 条候选勾选 → 检查）
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

  /* ---------- 2. 动手一：喂样本训练器 ---------- */
  var aiCv = document.getElementById('ai-canvas');
  if (aiCv) {
    var actx = aiCv.getContext('2d');
    var L = 62, R = 596, T = 30, B = 306;
    var X0 = 3, X1 = 12, Y0 = 0, Y1 = 100;
    var COL = {
      apple:  { fill: '#ef5350', soft: 'rgba(239,83,80,.17)',  name: '苹果' },
      orange: { fill: '#f5a623', soft: 'rgba(245,166,35,.17)', name: '橙子' }
    };
    var samples = [];
    var curLabel = 'apple';
    var hover = null;

    function toPx(x, y) {
      return [L + (x - X0) / (X1 - X0) * (R - L), B - (y - Y0) / (Y1 - Y0) * (B - T)];
    }
    function toData(px, py) {
      return [X0 + (px - L) / (R - L) * (X1 - X0), Y0 + (B - py) / (B - T) * (Y1 - Y0)];
    }
    function nearestOf(px, py) {
      var best = null, bd = Infinity;
      samples.forEach(function (s) {
        var p = toPx(s.x, s.y);
        var d = Math.sqrt((p[0] - px) * (p[0] - px) + (p[1] - py) * (p[1] - py));
        if (d < bd) { bd = d; best = s; }
      });
      return best ? { s: best, d: bd } : null;
    }
    function farWord(d) {
      if (d < 45) return '很近';
      if (d < 120) return '有点远';
      return '很远';
    }

    function draw1() {
      var w = aiCv.width, h = aiCv.height;
      actx.clearRect(0, 0, w, h);

      // 判断区域（最近邻）
      if (samples.length) {
        for (var px = L; px < R; px += 9) {
          for (var py = T; py < B; py += 9) {
            var n = nearestOf(px + 4, py + 4);
            if (!n) continue;
            actx.fillStyle = COL[n.s.lab].soft;
            actx.fillRect(px, py, 9, 9);
          }
        }
      } else {
        actx.fillStyle = 'rgba(150,140,120,.08)';
        actx.fillRect(L, T, R - L, B - T);
      }

      // 坐标轴
      actx.strokeStyle = 'rgba(150,140,120,.45)';
      actx.lineWidth = 1;
      actx.beginPath(); actx.moveTo(L, B); actx.lineTo(R, B); actx.moveTo(L, T); actx.lineTo(L, B); actx.stroke();

      actx.fillStyle = 'rgba(120,112,96,.95)';
      actx.font = '12px sans-serif';
      actx.textAlign = 'center';
      [3, 6, 9, 12].forEach(function (v) {
        var p = toPx(v, Y0);
        actx.beginPath(); actx.moveTo(p[0], B); actx.lineTo(p[0], B + 5); actx.stroke();
        actx.fillText(v + ' 厘米', p[0], B + 20);
      });
      actx.textAlign = 'right';
      ['偏黄', '中间', '偏红'].forEach(function (t, i) {
        var py = B - (B - T) * (i / 2);
        actx.fillText(t, L - 8, py + 4);
      });
      actx.textAlign = 'left';
      actx.fillStyle = 'rgba(120,112,96,.8)';
      actx.fillText('果实直径 →', L, B + 40);
      actx.save();
      actx.translate(16, T + 6);
      actx.fillText('颜色偏红 ↑', 0, 0);
      actx.restore();

      if (!samples.length) {
        actx.fillStyle = 'rgba(120,112,96,.75)';
        actx.font = '15px sans-serif';
        actx.textAlign = 'center';
        actx.fillText('还没有任何例子，机器现在什么也说不出来', (L + R) / 2, (T + B) / 2);
      }

      // 样本点
      samples.forEach(function (s) {
        var p = toPx(s.x, s.y);
        actx.beginPath();
        actx.arc(p[0], p[1], 7, 0, Math.PI * 2);
        actx.fillStyle = COL[s.lab].fill;
        actx.fill();
        actx.lineWidth = 2;
        actx.strokeStyle = '#fff';
        actx.stroke();
      });

      // 鼠标悬停
      if (hover) {
        var n2 = nearestOf(hover[0], hover[1]);
        actx.beginPath();
        actx.arc(hover[0], hover[1], 10, 0, Math.PI * 2);
        actx.lineWidth = 2.5;
        actx.strokeStyle = n2 ? COL[n2.s.lab].fill : 'rgba(120,112,96,.6)';
        actx.stroke();
        if (n2) {
          var np = toPx(n2.s.x, n2.s.y);
          actx.setLineDash([4, 4]);
          actx.lineWidth = 1.5;
          actx.beginPath(); actx.moveTo(hover[0], hover[1]); actx.lineTo(np[0], np[1]); actx.stroke();
          actx.setLineDash([]);
        }
      }
    }

    function paint1() {
      var a = samples.filter(function (s) { return s.lab === 'apple'; }).length;
      var o = samples.length - a;
      document.getElementById('ai-n-apple').textContent = a + ' 个';
      document.getElementById('ai-n-orange').textContent = o + ' 个';
      var vEl = document.getElementById('ai-verdict');
      var dEl = document.getElementById('ai-dist');
      if (!samples.length) {
        vEl.textContent = '—';
        dEl.textContent = '—';
      } else if (hover) {
        var n = nearestOf(hover[0], hover[1]);
        if (n) {
          vEl.textContent = '这是' + COL[n.s.lab].name;
          dEl.textContent = '离最近的例子：' + farWord(n.d);
        }
      } else {
        vEl.textContent = '把鼠标移到图上';
        dEl.textContent = '—';
      }
      document.querySelectorAll('[data-ai-label]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.aiLabel === curLabel);
      });
      draw1();
    }

    var STARTER = {
      apple: [[6, 80], [7, 86], [8, 88], [5.5, 74], [7.5, 82]],
      orange: [[9, 54], [10, 60], [9.5, 50], [10.5, 57], [9, 46]]
    };

    document.querySelectorAll('[data-ai-label]').forEach(function (b) {
      b.addEventListener('click', function () { curLabel = b.dataset.aiLabel; paint1(); });
    });
    document.getElementById('ai-load').addEventListener('click', function () {
      samples = [];
      Object.keys(STARTER).forEach(function (k) {
        STARTER[k].forEach(function (pt) { samples.push({ x: pt[0], y: pt[1], lab: k }); });
      });
      paint1();
      document.getElementById('ai-tip').className = 'result';
      document.getElementById('ai-tip').innerHTML =
        '<strong>一组例子喂进去了。</strong>现在图上出现了两块颜色：偏红的那一片被判成苹果，偏橙的那一片被判成橙子。' +
        '这就是机器从这十个例子里找出来的规律——它没有真的「看见」苹果，它只是照着离得最近的例子说话。';
    });
    document.getElementById('ai-clear').addEventListener('click', function () {
      samples = []; hover = null; paint1();
      document.getElementById('ai-tip').className = 'result warn';
      document.getElementById('ai-tip').textContent = '例子清空了。机器又变回什么都不会的状态——它脑子里本来就是空的。';
    });
    aiCv.addEventListener('click', function (e) {
      var rect = aiCv.getBoundingClientRect();
      var px = (e.clientX - rect.left) * (aiCv.width / rect.width);
      var py = (e.clientY - rect.top) * (aiCv.height / rect.height);
      if (px < L || px > R || py < T || py > B) return;
      var d = toData(px, py);
      samples.push({ x: Math.round(d[0] * 10) / 10, y: Math.round(d[1] / 5) * 5, lab: curLabel });
      hover = [px, py];
      paint1();
    });
    aiCv.addEventListener('mousemove', function (e) {
      var rect = aiCv.getBoundingClientRect();
      var px = (e.clientX - rect.left) * (aiCv.width / rect.width);
      var py = (e.clientY - rect.top) * (aiCv.height / rect.height);
      if (px < L || px > R || py < T || py > B) { hover = null; } else { hover = [px, py]; }
      paint1();
    });
    aiCv.addEventListener('mouseleave', function () { hover = null; paint1(); });
    paint1();
  }

  /* ---------- 3. 动手二：样本偏了，结论就偏 ---------- */
  var mixCv = document.getElementById('mix-canvas');
  if (mixCv) {
    var mctx = mixCv.getContext('2d');
    var ML = 62, MR = 596, MT = 34, MB = 132;
    var V0 = 3, V1 = 12;

    var BIG = [8.0, 9.0, 9.5, 10.5, 11.0];
    var SMALL = [3.0, 3.5, 4.0, 4.5, 5.0];
    var EXTRA = [5.5, 6.0, 6.5];
    var extraOn = false;

    var TESTS = [
      { v: 8.5, truth: 1, note: '大果品种，确实已经成熟' },
      { v: 4.0, truth: 0, note: '还很小，确实没熟' },
      { v: 6.2, truth: 1, note: '这是小果品种，个头虽小但已经成熟了' }
    ];
    var cur = 0;

    function vx(v) { return ML + (v - V0) / (V1 - V0) * (MR - ML); }
    function trainSets() {
      var ripe = BIG.slice();
      if (extraOn) ripe = ripe.concat(EXTRA);
      return { ripe: ripe, unripe: SMALL.slice() };
    }
    function boundary() {
      var t = trainSets();
      return (Math.min.apply(null, t.ripe) + Math.max.apply(null, t.unripe)) / 2;
    }

    function draw2() {
      var w = mixCv.width, h = mixCv.height;
      mctx.clearRect(0, 0, w, h);
      var bd = boundary();

      // 两种判断区域的底色
      mctx.fillStyle = 'rgba(245,166,35,.14)';
      mctx.fillRect(ML, MT, vx(bd) - ML, MB - MT);
      mctx.fillStyle = 'rgba(34,197,94,.14)';
      mctx.fillRect(vx(bd), MT, MR - vx(bd), MB - MT);

      // 分界线
      mctx.strokeStyle = '#4ecdc4';
      mctx.lineWidth = 3;
      mctx.beginPath(); mctx.moveTo(vx(bd), MT - 6); mctx.lineTo(vx(bd), MB + 6); mctx.stroke();
      mctx.fillStyle = '#14897f';
      mctx.font = 'bold 13px sans-serif';
      mctx.textAlign = 'center';
      mctx.fillText('分界线 ' + bd.toFixed(2), vx(bd), MT - 12);

      // 轴
      mctx.strokeStyle = 'rgba(150,140,120,.5)';
      mctx.lineWidth = 1;
      mctx.beginPath(); mctx.moveTo(ML, MB); mctx.lineTo(MR, MB); mctx.stroke();
      mctx.fillStyle = 'rgba(120,112,96,.95)';
      mctx.font = '12px sans-serif';
      [3, 5, 7, 9, 12].forEach(function (v) {
        mctx.beginPath(); mctx.moveTo(vx(v), MB); mctx.lineTo(vx(v), MB + 5); mctx.stroke();
        mctx.fillText(v + ' 厘米', vx(v), MB + 20);
      });
      mctx.textAlign = 'left';
      mctx.fillStyle = 'rgba(120,112,96,.75)';
      mctx.fillText('果实直径 →', MR - 78, MB + 20);

      // 训练样本
      function dot(v, kind, y) {
        mctx.beginPath();
        mctx.arc(vx(v), y, 6.5, 0, Math.PI * 2);
        mctx.fillStyle = kind === 'ripe' ? '#22c55e' : '#f59e0b';
        mctx.fill();
        mctx.lineWidth = 1.5; mctx.strokeStyle = '#fff'; mctx.stroke();
      }
      var t = trainSets();
      t.ripe.forEach(function (v) { dot(v, 'ripe', MT + 26); });
      t.unripe.forEach(function (v) { dot(v, 'unripe', MT + 26); });

      // 当前测试果实
      var tv = TESTS[cur].v;
      var px = vx(tv);
      mctx.beginPath();
      mctx.moveTo(px, MT + 40); mctx.lineTo(px - 7, MT + 54); mctx.lineTo(px + 7, MT + 54);
      mctx.closePath();
      mctx.fillStyle = '#ef5350';
      mctx.fill();
      mctx.fillStyle = '#b3261e';
      mctx.font = 'bold 12px sans-serif';
      mctx.textAlign = 'center';
      mctx.fillText(tv.toFixed(1) + ' 厘米', px, MT + 70);
    }

    function paint2() {
      var bd = boundary();
      var tv = TESTS[cur].v;
      var guess = tv >= bd ? 1 : 0;
      var t = TESTS[cur];
      document.getElementById('mix-boundary').textContent = bd.toFixed(2) + ' 厘米';
      document.getElementById('mix-guess').textContent = guess ? '可以装箱' : '再等等';
      document.getElementById('mix-truth').textContent = t.truth ? '其实已经成熟' : '确实还没熟';
      var out = document.getElementById('mix-verdict');
      var ok = guess === t.truth;
      out.className = 'result ' + (ok ? '' : 'error');
      out.innerHTML = '<strong>这颗 ' + t.v.toFixed(1) + ' 厘米的果子：机器判它「' +
        (guess ? '可以装箱' : '再等等') + '」，' + t.note + '。</strong>' +
        (ok
          ? '<br>这次判对了。'
          : '<br>判错了。机器看到的分界线是 ' + bd.toFixed(2) + ' 厘米，比它小的它一律当成「再等等」——' +
            '因为在它见过的例子里，<strong>成熟的全是大果</strong>。它把「大」当成了「熟」的规律。') +
        '<br><span style="color:var(--muted)">当前训练样本：可装箱 ' + trainSets().ripe.length +
        ' 个，再等等 ' + trainSets().unripe.length + ' 个。</span>';
      document.querySelectorAll('[data-mix-test]').forEach(function (b, i) {
        b.classList.toggle('selected', i === cur);
      });
      document.getElementById('mix-add').disabled = extraOn;
      document.getElementById('mix-add').textContent = extraOn
        ? '已经补充过样本了' : '补充样本：加入 3 个「小果但已经成熟」的例子';
      draw2();
    }

    document.querySelectorAll('[data-mix-test]').forEach(function (b, i) {
      b.addEventListener('click', function () { cur = i; paint2(); });
    });
    document.getElementById('mix-add').addEventListener('click', function () {
      extraOn = true;
      var before = boundary();
      paint2();
      var after = boundary();
      var out = document.getElementById('mix-verdict');
      out.className = 'result';
      out.innerHTML = '<strong>补进三个「小果但已经成熟」的例子之后，分界线从 ' + before.toFixed(2) +
        ' 厘米挪到了 ' + after.toFixed(2) + ' 厘米。</strong>' +
        '机器学到了新东西：小果也可能已经成熟。现在再点一遍那三个果子看看。' +
        '<br><span style="color:var(--muted)">样本变了，规律就变了，结论也跟着变——这就是训练。</span>';
    });
    document.getElementById('mix-reset').addEventListener('click', function () {
      extraOn = false; cur = 0; paint2();
    });
    paint2();
  }

  /* ---------- 4. 综合任务：样本清单 ---------- */
  var sPool = document.getElementById('sample-pool');
  if (sPool) {
    var ITEMS = [
      ['g1', '同一种植物，在早晨、中午、树荫下都各拍一些照片',
        '光线不一样，照片看起来差别很大。都拍过，机器才不会把「阴天的样子」当成另一种植物。'],
      ['g2', '同一种植物，正面、侧面、背面、叶子特写都拍一些',
        '真实拍摄时的角度是随机的。角度覆盖得越全，实际用起来越稳。'],
      ['g3', '同一种植物，春夏秋冬各拍一些',
        '植物会随季节变样子。只拍一个季节，换个季节它就认不出来了。'],
      ['g4', '让不同年级的同学，用不同的手机各拍一些',
        '不同手机拍出来的颜色和清晰度都不一样。换一台设备就认错，说明样本太单一。'],
      ['g5', '校园里不同位置（花坛、操场边、教学楼后）的同一种植物都拍',
        '同一种植物长在不同地方，背景就不一样。背景见得多了，机器才不会被背景带偏。'],
      ['g6', '每种植物都要拍够数量，不能有的几十张、有的只有两张',
        '样本太少的类别，机器几乎学不到它的规律，判断会明显偏向样本多的那一类。'],
      ['b1', '只在晴天中午那一个时间去拍',
        '样本偏了，结论就偏。只见过晴天中午的样子，阴天或傍晚拍的照片它就可能认不出。'],
      ['b2', '只用自己班窗台上那一盆植物拍',
        '一盆植物只有一种长势、一种背景，机器会把「这盆花的样子」错当成「这种植物的样子」。'],
      ['b3', '每种植物只挑一张最漂亮的照片放进去',
        '一张照片说明不了一种植物的变化。样本太少，机器等于没学到。'],
      ['b4', '只拍校园里最常见的三种植物，其他的先不管',
        '训练时没见过的类别，机器就会硬把它塞进见过的某一类里，结果错得很自信。']
    ];
    var GOOD = {};
    ['g1', 'g2', 'g3', 'g4', 'g5', 'g6'].forEach(function (k) { GOOD[k] = 1; });
    var picked = {}, locked = false, cards = [];
    var out4 = document.getElementById('sample-verdict');

    ITEMS.forEach(function (it) {
      var b = document.createElement('button');
      b.className = 'sort-item';
      b.textContent = it[1];
      b.addEventListener('click', function () {
        if (locked) return;
        if (picked[it[0]]) { delete picked[it[0]]; b.classList.remove('selected'); }
        else { picked[it[0]] = 1; b.classList.add('selected'); }
        document.getElementById('sample-count').textContent = Object.keys(picked).length + ' 条';
        out4.className = 'result warn';
        out4.textContent = '已经选了 ' + Object.keys(picked).length + ' 条。选完点「检查我的清单」。';
      });
      sPool.appendChild(b);
      cards.push({ id: it[0], el: b });
    });

    document.getElementById('sample-check').addEventListener('click', function () {
      locked = true;
      var right = 0, wrong = [];
      cards.forEach(function (c) {
        var should = !!GOOD[c.id], did = !!picked[c.id];
        c.el.classList.remove('selected');
        if (should === did) { c.el.classList.add('correct'); right++; }
        else { c.el.classList.add('wrong'); wrong.push(c.id); }
      });
      var why = wrong.map(function (id) {
        var it = ITEMS.filter(function (x) { return x[0] === id; })[0];
        return '<br>· 「' + it[1] + '」——' + (GOOD[id] ? '这一条<strong>该</strong>用，但你没选：' : '这一条<strong>不该</strong>用，但你选了：') + it[2];
      }).join('');
      out4.className = 'result' + (wrong.length ? ' warn' : '');
      out4.innerHTML = '<strong>对 ' + right + ' 条，需要再想想 ' + wrong.length + ' 条。</strong>' + why +
        (wrong.length ? '' : '<br>六条该用的你都挑出来了。它们说的其实是同一件事：<strong>样本要够多、够全、不能偏</strong>。') +
        '<br><br><span style="color:var(--muted)">常见错误：误认为「随便拍几张丢进去，机器就能学会」。' +
        '机器只会它见过的样子——你给它看的世界有多窄，它知道的世界就有多窄。</span>';
    });

    document.getElementById('sample-reset').addEventListener('click', function () {
      locked = false; picked = {};
      cards.forEach(function (c) { c.el.className = 'sort-item'; });
      document.getElementById('sample-count').textContent = '0 条';
      out4.className = 'result warn';
      out4.textContent = '先点卡片，把你认为该用的做法选出来。';
    });
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：机器是怎么「会」的？", TTS["pretest"], [
        {"q": "相册能自己认出照片里的猫，最接近下面哪种说法？",
         "options": [("它看过很多张被标好的猫的照片，从里面找到了猫的共同点", True),
                     ("有人把全世界每一只猫的样子都一条条写进了程序", False),
                     ("它天生就认识猫，不用人教", False)],
         "explain": "机器是从大量带标签的例子里找规律。一条条写死规则是不现实的——猫的样子太多，写不完。"
                    "<strong>错因提醒：</strong>常见错误是误认为「工程师把规则一条条写好了」。"
                    "真正的做法是给它例子，让它自己找。"},
        {"q": "一个识别水果的机器，只在例子里见过红色的苹果。给它一个青色的苹果，会怎样？",
         "options": [("很可能认不出来，因为它的例子里没有青色的样子", True),
                     ("它一定能认出来，因为都是苹果", False),
                     ("它会自动上网去查什么是青苹果", False)],
         "explain": "机器只会它见过的样子。样本里没有青苹果，它就没有依据把青苹果判成苹果。"
                    "<strong>错因提醒：</strong>容易误认为「机器自己会举一反三」。"
                    "举一反三要靠样本覆盖到，不会凭空发生。"},
        {"q": "关于机器给出的判断，下面哪句话更准确？",
         "options": [("它是照着学到的规律算出来最可能的答案，本质上是一次猜测", True),
                     ("它和人一样，是真的看懂了才回答", False),
                     ("它每次都一定正确，错了就是坏了", False)],
         "explain": "机器给的是按规律算出的最可能答案，所以样本变了、规律变了，判断就会跟着变。"
                    "<strong>错因提醒：</strong>这里最容易搞混的是「算得快」和「看得懂」。"
                    "算得快不等于真的理解了，出了错也不一定是坏了——多半是它见过的例子不够。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "机器不是在「看懂」，它是在例子里找规律", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们身边已经有很多「会认东西」「会猜你想打什么」的功能（And）；可它有时候答得离谱，让人摸不着头脑，是因为我们不知道它是怎么得出结论的（But）；所以要看清楚它的三步走——喂例子、找规律、做判断（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">把这件事拆开，其实只有三步：</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>喂例子：</strong>给它一大批已经标好答案的例子。每张例子都带着一个标签——这张是苹果，那张是橙子。</div></div>
          <div class="step"><span class="n">2</span><div><strong>找规律：</strong>它自己在这批例子里找出一个能分开两类的办法。这个办法不一定是人想让它的那个。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>做判断：</strong>遇到没见过的新东西，它就照着找到的规律猜一个最可能的答案。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="机器学会一件事的三个步骤示意图：喂带标签的例子、从例子里找出分界线、用分界线判断新样本">
          <figcaption>喂例子 → 找规律 → 做判断：第三步给出的永远是<strong>猜</strong>，是按规律算出来的最可能答案，不是它真的看懂了</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🤖</span><div><strong>换个说法：</strong>机器像一个从没见过水果的小朋友。你给它看十个苹果、十个橙子，它就能猜出第十一个是什么；可你给它的例子里如果全是红的，那它见到青苹果时，只能硬猜。</div></div>
{insight_box([
    {"lens": "拆开它", "text": "把「人工智能」这四个字拆掉，剩下的其实是：一大堆带答案的例子，加一条从例子里找出来的规律。两样都离不开人。"},
    {"lens": "比较它", "text": "人认识一只猫，看两眼就够了；机器要看成千上万张。它靠的不是聪明，是数量。"},
    {"lens": "迁移它", "text": "以后遇到一个新功能，先问一句：它可能是拿什么例子学出来的？想得出例子，就大致想得到它在什么情况下会出错。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：喂样本训练器，看机器怎么学", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先在下面选好这一颗要标成什么，再到图上点一下，就喂给机器一个带标签的例子。鼠标在图上移动，还能看到它此刻会把那儿判成什么。</p>
        <div class="lab-panel">
          <div class="flex-row" style="margin-top:0">
            <button class="choice" data-ai-label="apple" style="text-align:center">这一颗标成 🍎 苹果</button>
            <button class="choice" data-ai-label="orange" style="text-align:center">这一颗标成 🍊 橙子</button>
          </div>
          <canvas id="ai-canvas" width="620" height="360" style="display:block;width:100%;border:1px solid var(--line-subtle);border-radius:14px;background:var(--card);margin-top:12px"></canvas>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">苹果例子</span><span class="v" id="ai-n-apple">0 个</span></div>
            <div class="readout-cell"><span class="k">橙子例子</span><span class="v" id="ai-n-orange">0 个</span></div>
            <div class="readout-cell"><span class="k">鼠标处机器判成</span><span class="v green" id="ai-verdict">—</span></div>
            <div class="readout-cell"><span class="k">最近例子离得多远</span><span class="v" id="ai-dist">—</span></div>
          </div>
          <div class="flex-row">
            <button class="choice" id="ai-load" style="text-align:center">载入一组例子</button>
            <button class="choice" id="ai-clear" style="text-align:center">清空全部例子</button>
          </div>
          <p class="result warn" id="ai-tip" style="margin-top:12px">先在图上点几下试试。一开始机器没有例子，什么也说不出来。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧪</span><div><strong>发现了什么：</strong>图上的两块颜色，就是机器此刻的「想法」。你每加一个例子，这两块颜色就会重新划分一次。想一想：如果只在右上角放苹果、只在左下角放橙子，中间那一大片它判得准吗？</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "样本要够多、够全、不能偏，机器才学得对", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">机器能学会的东西，<strong>不会超过你给它的例子</strong>。所以准备例子要守住三条。</p>
        <div class="grid grid-3">
          <div class="inner-card"><p><strong>① 要够多</strong></p><p style="color:var(--muted)">只见过三五个例子，它的判断会非常随便——离哪个例子近，就听哪个的。</p></div>
          <div class="inner-card"><p><strong>② 要够全</strong></p><p style="color:var(--muted)">真实世界里会遇到的各种样子，都得让它在例子里见过，不然就是没见过。</p></div>
          <div class="inner-card"><p><strong>③ 不能偏</strong></p><p style="color:var(--muted)">例子里只有一种样子，它就会把这种样子当成全部的规律——这是最容易出大错的一条。</p></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="样本偏了结论就偏示意图：训练样本里成熟的全是大果，机器把大当成熟的规律，于是把小果品种误判成没熟">
          <figcaption>样本偏了，结论就偏：成熟的全是大果 → 机器把「大」当成「熟」→ 小果品种被误判</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有同学会想：「先随便拍几张，不够再加。」可问题是，你<strong>根本不知道哪里不够</strong>——机器不会告诉你「我没见过这种」。它只会照着自己那点经验，自信地给出一个答案。所以准备样本这件事，要在训练<strong>之前</strong>就想清楚。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">📦</span><div><strong>记住这句话：</strong>你给它的世界有多窄，它知道的世界就有多窄。样本里没有的，它就学不会。</div></div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：样本偏了，结论就偏", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">上面这台分拣机，是照着十二个例子学出来的。下面三个果子，点一下就让机器判一次。注意看第三个。</p>
        <div class="lab-panel">
          <canvas id="mix-canvas" width="620" height="190" style="display:block;width:100%;border:1px solid var(--line-subtle);border-radius:14px;background:var(--card)"></canvas>
          <div style="font-size:13px;color:var(--muted);margin-top:8px">🟢 例子：已经成熟、可以装箱　　🟠 例子：还没熟、再等等　　🔺 现在要判的果子</div>
          <div class="flex-row">
            <button class="choice" data-mix-test="0" style="text-align:center">判第 1 个：8.5 厘米</button>
            <button class="choice" data-mix-test="1" style="text-align:center">判第 2 个：4.0 厘米</button>
            <button class="choice" data-mix-test="2" style="text-align:center">判第 3 个：6.2 厘米</button>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">机器找到的分界线</span><span class="v green" id="mix-boundary">—</span></div>
            <div class="readout-cell"><span class="k">机器判断</span><span class="v" id="mix-guess">—</span></div>
            <div class="readout-cell"><span class="k">真实情况</span><span class="v" id="mix-truth">—</span></div>
          </div>
          <div class="flex-row">
            <button class="choice" id="mix-add" style="text-align:center">补充样本：加入 3 个「小果但已经成熟」的例子</button>
            <button class="choice" id="mix-reset" style="text-align:center">重置实验</button>
          </div>
          <p class="result warn" id="mix-verdict" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>想清楚再补样本：</strong>机器为什么把 6.2 厘米的果子判错了？不是它坏了，是它见过的例子里，<strong>成熟的全是大果</strong>。补进几个「小果但成熟」的例子之后，分界线往左挪了，它的判断也跟着改了。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：训练一个广告识别助手，要注意什么？", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>学校想做一个识别广告的小助手。请说明它要学会哪件事、需要准备什么，并指出一个最容易被忽略的风险。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先想清楚它要学会什么：</strong>把每一条消息分成「广告」和「不是广告」两类。任务越具体，越容易准备例子。</div></div>
          <div class="step"><span class="n">2</span><div><strong>准备例子：</strong>收集一大批消息，每一条都由人来标好答案。这就是「带标签的例子」。</div></div>
          <div class="step"><span class="n">3</span><div><strong>让它找规律：</strong>它自己从这些例子里找出一条能把两类分开的办法，人不需要替它写规则。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>检查最容易被忽略的风险：</strong>如果这一批例子里，广告全都是卖文具的，那遇到一条卖课程的广告，它很可能认不出来——因为它见过的广告只有一种样子。所以训练完之后，要专门拿一批<strong>没给它看过的</strong>例子来考它。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">只统计「它在训练时答对了多少」。这个数字好看<strong>不代表它学会了</strong>——如果考它的题目和它见过的例子几乎一样，它当然答得对。真正要看的是：换一批它没见过的新例子，它还答得对吗？</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，错在哪里", TTS["conceptest-1"], [
        {"q": "有同学说：「机器出错，说明这个机器坏了。」这个说法的问题在哪？",
         "options": [("机器给的本来就是按规律算出的猜测，出错往往是它见过的例子不够全", True),
                     ("机器不应该出错，出错一定是坏了", False),
                     ("机器出错是因为我们忘了给它充电", False)],
         "explain": "机器是照着学到的规律猜答案。遇到规律没覆盖到的情况，它只能硬猜，所以会出错。"
                    "<strong>错因提醒：</strong>最常见的错误是误认为「出错＝故障」。"
                    "大部分时候不是坏了，是训练时没见过这一类例子。"},
        {"q": "要让一个识别水果的机器认得青苹果，最直接的办法是：",
         "options": [("在它的例子里补进一些标好的青苹果", True),
                     ("把它的运行速度调快一些", False),
                     ("告诉它「青苹果也是苹果」这句话", False)],
         "explain": "机器靠例子学规律，不是靠听人讲道理。补进青苹果的例子，它才有可能学到这一种。"
                    "<strong>错因提醒：</strong>容易把「跟人讲道理」和「给机器喂例子」搞混。"
                    "机器听不懂道理，它只从例子里总结。"},
        {"q": "一批训练例子全是「晴天中午拍的花」，会带来什么问题？",
         "options": [("阴天或傍晚拍的花，机器很可能认不出来", True),
                     ("照片太多，机器学不完", False),
                     ("不会有什么问题，晴天拍的最清楚", False)],
         "explain": "样本偏了，结论就偏。只用一种光照条件下的例子训练，它就只认得那种样子。"
                    "<strong>错因提醒：</strong>这里最容易犯的是误认为「越清楚越好」——"
                    "清楚当然好，但只有一种清楚，还不如各种条件都有一点。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：给植物识别助手准备样本", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">下面有十条候选做法。点一下卡片就能选上或者取消，把你认为该用的挑出来，再点「检查我的清单」。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">十条候选做法</div>
          <div class="sort-bank" id="sample-pool"></div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">已选</span><span class="v" id="sample-count">0 条</span></div>
          </div>
          <div class="flex-row">
            <button class="choice" id="sample-check" style="text-align:center">检查我的清单</button>
            <button class="choice" id="sample-reset" style="text-align:center">重新来</button>
          </div>
          <p class="result warn" id="sample-verdict" style="margin-top:12px">先点卡片，把你认为该用的做法选出来。</p>
        </div>
        <div class="inner-card">
          <p><strong>检查完以后想一想，说给同桌听：</strong></p>
          <p style="color:var(--muted)">十条里有四条是<strong>不该</strong>用的。它们看着都很省事，可每一种都会让样本变偏。你能说清楚每一条会让机器「偏」在哪里吗？</p>
          <textarea id="syn-answer" rows="3" placeholder="第一条会让样本偏在……第二条会让样本偏在……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个情境，样本和结论还在不在", TTS["posttest"], [
        {"q": "有个识别器只见过自家小区里的那几只猫。换一只从没见过的品种，它多半会怎样？",
         "options": [("很可能判错，因为新品种的样子它没见过", True),
                     ("照样能认出来，猫都长得一样", False),
                     ("它会自动去网上搜这只猫的品种", False)],
         "explain": "样本覆盖不到的样子，机器就没有依据。它只会把新东西硬塞进它见过的某一类里。"
                    "<strong>错因提醒：</strong>常见错误想法是「都是猫，应该没问题」。"
                    "对机器来说，它比的不是「像不像猫」，而是「像不像它见过的那些猫」。"},
        {"q": "一份训练样本里，九成照片都是同一个车型。这样做出的识别器最可能的问题是：",
         "options": [("换一个车型就容易认错，判断明显偏向它见过的那种", True),
                     ("识别速度会变慢", False),
                     ("照片太多会占地方，对判断没有影响", False)],
         "explain": "类别之间样本数量悬殊，机器会明显偏向样本多的那一类。这是「样本偏了，结论就偏」最典型的样子。"
                    "<strong>错因提醒：</strong>容易把「样本数量」当成和判断无关的事。"
                    "数量也是样本的一部分，不均衡就是偏。"},
        {"q": "下面哪句话，最准确地说明了机器和例子的关系？",
         "options": [("给它看的世界有多窄，它知道的世界就有多窄", True),
                     ("只要算得够快，它迟早什么都能知道", False),
                     ("它自己会慢慢长大，不用再给新例子", False)],
         "explain": "机器的「知识」几乎全部来自它见过的例子。样本窄，它的世界就窄；样本变了，它的结论就跟着变。"
                    "<strong>错因提醒：</strong>这里最容易搞混的是「快」和「会」。"
                    "算得快只是算得快，它并不会因为算得快就多懂一点。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把人工智能这件事说清楚", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>它怎么学会：</strong>喂带标签的例子 → 从例子里找规律 → 照着规律猜答案。它给的是猜，不是看懂。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>样本要三条：</strong>够多、够全、不能偏。样本里没有的样子，它就是学不会。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>样本偏了就出错：</strong>成熟的全是大果，它就把「大」当成「熟」；换一批没见过的例子考它，才知道它到底行不行。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那个问题：</strong>相册能认出猫，是因为它见过成千上万张被标好的猫的照片。它没有变聪明，它只是见得足够多。而换一只它从没见过的样子，它一样会认错——所以现在我们知道了：<strong>它的本事，是我们用例子喂出来的</strong>。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「喂例子、找规律、猜答案」这三步，说清楚相册为什么能认出猫。</p>
          <p style="color:var(--muted)">再动一动手：<strong>找一找</strong>——你身边还有哪三个功能可能是这样学出来的？各写下一个它可能会认错的情况。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "用自己的话说一说，机器学会一件事要经过哪三步，每一步在做什么。",
            "写出样本的三条要求：要够多、要够全，还有一条是什么？",
        ],
        [
            "找一个你身边「会认东西」的功能，写出它可能是拿什么例子学出来的，再写出一个它可能会认错的情况。",
            "把动手二里的实验重做一遍：先不补样本，记下机器判错的第 3 个果子；补完样本再判一次，记下变化。",
        ],
        [
            "给学校的植物识别助手设计一份样本清单：拍哪些植物、什么时间拍、从什么角度拍，并说明为什么要这么麻烦。",
            "想一想：如果让你给一个「识别校园里不文明行为」的机器准备样本，你会担心出现什么问题？把理由写清楚。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-e-ai-awareness",
    "node_id": "it-e-ai-awareness",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 小学",
    "title": "人工智能初识",
    "name_en": "Getting to Know AI: Learning from Examples",
    "grade": 6,
    "grade_cn": "六年级",
    "domain": "internet-ai",
    "domain_cn": "互联网与人工智能",
    "lesson_type": "concept-experiment",
    "version": "1.0.0",
    "description": "面向小学六年级：通过亲手训练一个分类模拟，理解人工智能是在大量带标签的例子里找规律、再照着规律猜答案，认识到样本要够多、够全、不能偏，并能说出样本偏了会带来什么后果。",
    "tags": ["人工智能", "训练样本", "找规律", "样本偏差", "辩证看待技术"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》小学「互联网与人工智能」——了解人工智能的典型应用，辩证看待其影响。",
    "hero_question": "机器没有眼睛，也没上过一天学，它凭什么能认出照片里的猫？",
    "hero_alt": "人工智能初识知识结构图：机器从例子里找规律、样本决定它能学会什么、样本偏了结论就偏",
    "hero_caption": "三步走：喂例子 · 找规律 · 猜答案　|　样本三条：够多 · 够全 · 不能偏　|　样本里没有的，它就是学不会",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的动手实验都会围着它转。",
    "anchor_choices": [
        {"t": "机器到底是怎么「学会」一件事的？", "d": "想知道它凭什么会认、会猜", "v": "机器到底是怎么学会一件事的"},
        {"t": "它为什么有时候会判断错？", "d": "想知道出错的原因在哪里", "v": "它为什么有时候会判断错"},
        {"t": "它算不算真的「聪明」？", "d": "想知道该不该把它当成什么都会", "v": "它算不算真的聪明"},
        {"t": "如果让我来训练它，我会怎么做？", "d": "想亲手喂它一些例子看看", "v": "如果让我来训练它会怎么做"},
    ],
    "objectives": [
        "能用自己的话说出，人工智能是靠看大量带标签的例子来找规律，再照着规律给出猜测",
        "能在训练模拟里通过添加和删除样本，让机器的判断区域与结论跟着改变",
        "能说出样本偏了会带来什么后果，并举出一个具体的例子",
        "能说清楚人工智能擅长什么、不擅长什么，不把它当成什么都会的魔法",
    ],
    "objectives_plain": [
        "能用自己的话说出，人工智能是靠看大量带标签的例子来找规律，再照着规律给出猜测",
        "能在训练模拟里通过添加和删除样本，让机器的判断区域与结论跟着改变",
        "能说出样本偏了会带来什么后果，并举出一个具体的例子",
        "能说清楚人工智能擅长什么、不擅长什么，不把它当成什么都会的魔法",
    ],
    "standards": [
        {"content": "了解人工智能的典型应用，辩证看待其影响",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 互联网与人工智能"},
        {"content": "在亲手训练简单分类模型的过程中，理解数据与结论之间的关系，初步形成对技术结论保持审慎判断的意识",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 互联网与人工智能 / 信息社会责任"},
    ],
    "prereqs": [],
    "prereqs_name": "本课是信息科技小学段「互联网与人工智能」中人工智能部分的第一课，不需要先修节点",
    "prereqs_meta": "",
    "leads_to": ["it-e-ai-ethics", "it-m-ai-applications"],
    "next_meta": "it-e-ai-ethics",
    "section_images": ["assets/it-e-ai-awareness-fig1.webp", "assets/it-e-ai-awareness-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "机器没眼睛也没上过学，它凭什么认得出猫？带着这个疑问开始。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能亲手教机器一件事，也能说清它为什么会出错。",
        "objectives": "看清四件事：它怎么学、训练怎么改变它、样本偏了会怎样、它到底擅长什么。",
        "pretest": "凭现在的想法选就好，错了不扣分——前测是帮你看清自己站在哪里。",
        "module-1": "三步走：喂带标签的例子、从例子里找规律、照着规律猜答案。它给的是猜。",
        "lab-1": "在图上点一下就是喂一个例子。先什么都不放试试，看看没有例子的机器能说什么。",
        "module-2": "样本要够多、够全、不能偏。样本里没有的样子，它就是学不会。",
        "lab-2": "三个果子依次点一遍，第三个它会判错。想清楚为什么，再点补充样本。",
        "worked-example": "四步走：想清楚任务、准备带标签的例子、让它找规律、拿没见过的例子考它。",
        "conceptest-1": "三个说法里藏着高频错误，选完把解释读一遍。",
        "synthesis": "只有六条该用。另外四条看着省事，每一种都会让样本变偏。",
        "posttest": "只认识自家小区的猫、九成样本一个车型——样本窄了，它会窄成什么样？",
        "summary": "三句话：它怎么学会、样本要什么、样本偏了会怎样。",
        "homework": "三层小任务，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学信息科技「互联网与人工智能」里人工智能部分的第一课。六年级学生对人工智能最常见的两种误解：一是把它当成「什么都会」的魔法，二是把它的出错当成「坏了」。这两种误解的根源，都是不知道它的结论从哪里来。所以全课只讲透一句话——机器是在大量带标签的例子里找规律，再照着规律猜。围绕这句话做了两个真能操作的实验室：动手一是一个二维散点训练器，学生在图上点一下就是喂一个带标签的例子，机器用最近邻规则实时重画它的判断区域，鼠标移到哪儿就显示它此刻会判成什么；先让学生看到「一个例子都没有时，机器什么也说不出来」，再载入一组例子看到判断区域自然浮现，亲手体会到规律是从例子长出来的。动手二是一个一维分拣模拟：预设的训练样本里成熟的全是大果，机器因此把「大」当成「熟」的规律，把 6.2 厘米的小果品种判成「再等等」；学生想清楚之后点一下补充样本，分界线从 6.5 厘米挪到 5.25 厘米，判断随之改变——「样本偏了，结论就偏」在这里被看见，而不是被背诵。综合任务让学生反过来给植物识别助手挑样本，十条候选里有四条是「看着省事但会让样本变偏」的做法。全课不出现任何真实产品或品牌。",
    "plan_table": """| 1 | cover | 人工智能初识 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：机器是怎么「会」的？ | 起·前测（暴露直觉） |
| 5 | concept | 机器不是在「看懂」，它是在例子里找规律 | 承·概念一（三步走 + 类比 + 五镜头） |
| 6 | interactive | 动手一：喂样本训练器，看机器怎么学 | 承·动手模拟（Canvas 散点最近邻，判断区域实时重画） |
| 7 | concept | 样本要够多、够全、不能偏，机器才学得对 | 承·概念二（三条要求 + 常见错误） |
| 8 | interactive | 动手二：样本偏了，结论就偏 | 承·偏样本实验（分界线随样本移动，含误判陷阱） |
| 9 | concept | 例题示范：训练一个广告识别助手，要注意什么？ | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：三个说法，错在哪里 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：给植物识别助手准备样本 | 合·迁移应用（10 条候选勾选，含 4 条会让样本变偏的做法） |
| 12 | quiz | 后测：换几个情境，样本和结论还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把人工智能这件事说清楚 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：机器从例子里找规律 / 样本决定它能学会什么 / 样本偏了结论就偏 三栏\n- P5 训练三步示意图（已生成）：喂例子 → 找规律 → 做判断\n- P7 偏样本示意图（已生成）：成熟样本全是大果 → 把「大」当成「熟」→ 小果品种误判\n- 三张图均为教学示意图，画面中不出现任何真实产品、应用或品牌\n- 若需补充：学生动手训练时的课堂实拍照片（需获得授权后使用）",
}
