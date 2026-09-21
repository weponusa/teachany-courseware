# -*- coding: utf-8 -*-
"""初中信息科技 · 人工智能典型应用（G9）—— 补齐课标「人工智能与智慧社会」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-m-ai-applications-fig1.webp'
F2 = './assets/it-m-ai-applications-fig2.webp'

TTS = {
    "hero": "先看一个现象。有个小组做了一个识别装置，在教室里演示时几乎次次都对，搬到走廊上用却频频出错。他们检查了程序，一行都没改；又检查了镜头，也没有脏。问题出在没人注意的地方：模型是从数据里学出来的，数据里没有出现过走廊那种光线和角度，它自然就认不准。这节课我们看看人工智能的几类典型应用，把数据、模型和结果之间的这条链弄清楚。",
    "problem-anchor": "开始之前，先挑一个你最想弄明白的问题。是想知道人工智能到底和普通程序差在哪里，还是想知道识别一张图、框出一个物体、描出一片区域这三种任务有什么不同，又或者你想弄明白为什么演示时很准、实际用起来却常出错。选好以后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说清机器学习和传统程序的区别：规则是人写死的，还是从数据里学出来的。第二，能用数据、特征、标签、模型、预测、评价这六个词，拆解一个典型的人工智能应用。第三，能区分图像分类、目标检测、图像分割三类计算机视觉任务，并说出它们输出形式的差别。第四，能判断一个模型为什么在演示时表现好、在实际场景里表现差，并指出数据构成和评价方式上的问题。",
    "pretest": "先做三道小题，凭现在的想法选就行，选错了也没关系，正好能看出哪里需要重点听。选完会立刻出现解释。",
    "module-1": "先分清一件事：人工智能和普通程序，差别不在代码长短，而在规则是从哪里来的。普通程序把规则写死在代码里，人告诉它什么情况该做什么。机器学习不一样，人给的是大量带答案的样本，规则由模型从数据里总结出来。所以这类应用的六个要素是数据、特征、标签、模型、预测、评价。特征是我们挑出来给模型看的可测量信息，标签是样本的标准答案，评价则要用没见过的新数据来做，否则测出来的只是记忆力。",
    "lab-1": "我们来亲手训出一个最简单的分类器。屏幕上是一条数轴，上面摆着两批样本，一批是正常消息，一批是可疑消息，横坐标是消息里可疑链接的个数。你要拖动一根判定线，把两类尽量分开。拖动的时候盯住三个数字：准确率、误报数、漏报数。你会看到一件有意思的事：最好的成绩往往不止一根线能达到，但它们的风险并不一样。",
    "module-2": "计算机视觉的三类典型任务，区别就在输出的形式上。图像分类给整张图一个标签，回答这是哪一类。目标检测不但要说出是什么，还要给出位置，输出是一串带坐标的矩形框、类别和置信度。图像分割更细，它给每一个像素都归类，输出是一张掩码图。输出的形式决定了能支撑什么应用：分类用于初筛，检测用于计数和定位，分割用于精确测量面积。选任务之前，先想清楚你到底需要什么样的输出。",
    "lab-2": "现在你来对比这三种任务。屏幕上是一个简单的场景示意图，里面有物体。切换任务类型，看输出怎么变：分类只在整张图上给一个结论；检测会给每个物体加上矩形框、类别和置信度；分割会把物体的轮廓整片标出来。再拖动置信度阈值，看着没把握的目标被挡在门外——那正是漏检。",
    "worked-example": "我们分析一个真实的落差：模型在教室演示时几乎次次正确，到了走廊却频频出错。第一步，看数据是从哪来的，结果发现训练样本几乎全是在教室里、在固定光线下采集的。第二步，看数据里各类样本的数量，发现有一类样本只占很小一部分。第三步，看评价方式，他们只用整体准确率来衡量，而这个数字会被样本多的那一类拉高，把样本少的那一类的糟糕表现盖住。第四步，给出改进：补充不同光线和角度的样本，把样本少的那一类补齐，并且评价时按类别分别看，不要只看一个总数。",
    "conceptest-1": "现在用三个容易弄错的说法考考你。请仔细读每一个选项，选出你认为正确的那个，然后看解释。",
    "synthesis": "学到这里，请你当一次模型评估员。屏幕上是一个已经训好的模型，它在真实场景里的表现取决于训练数据的构成。你可以调训练样本的总数，也可以调某一类样本在训练数据里占的比例，看整体准确率和各个类别准确率怎么变。你会看到一个很值得警惕的现象：整体数字看着还行，可是某个类别几乎不合格——平均数把这个大问题盖住了。",
    "posttest": "最后换两个情境检验一下。这次出现了任务选型和数据不足的问题，看看你能不能把任务的输出形式和分类别看结果这两件事用上去。",
    "summary": "这节课我们弄清楚了三件事。第一，机器学习与普通程序的区别在规则的来源：规则是人写死的，还是从数据里学出来的。第二，一个典型应用的六个要素是数据、特征、标签、模型、预测、评价，其中评价必须用没见过的新数据来做。第三，计算机视觉的三类任务输出形式不同：分类给一个标签，检测给带位置的框，分割给像素级掩码，输出形式决定了它适合什么应用。还有一个最容易被忽略的结论：只看整体准确率会掩盖弱势类别的问题，这正是模型从演示走向实际时最常见的落差来源。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出机器学习和传统程序的区别，并列出这类应用的六个要素。第二层能力应用，动手做：为一个真实需求选择任务类型，说明需要什么数据、标签和输出形式，并写出评价方式。第三层迁移挑战，选做：找一个人工智能应用，分析它的训练数据可能缺什么、会造成什么影响，并提出两条改进建议。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 规则从数据里学出来", "lab-1": "实验室一 阈值分类器训练台",
    "module-2": "概念二 视觉任务的三层输出", "lab-2": "实验室二 视觉任务层次分解台",
    "worked-example": "例题讲解", "conceptest-1": "概念测试",
    "synthesis": "综合任务 模型评价与数据偏差诊断台", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

LAB_CSS = """
<style>
.ta-face { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px; }
.ta-face .choice { flex: 1; min-width: 150px; text-align: center; }
.ta-struct { margin-top: 12px; padding: 12px 14px; border-radius: 12px; font-size: 14px;
  background: var(--bg-subtle); border: 1px solid var(--line-subtle); }
.ta-struct code { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 13px;
  background: var(--brand-soft); padding: 2px 6px; border-radius: 6px; }
.ta-meter { display: flex; align-items: center; gap: 10px; margin-top: 10px; }
.ta-meter .lbl { flex: 0 0 92px; font-size: 13px; font-weight: 700; }
.ta-meter .bar { flex: 1; height: 12px; border-radius: 999px; background: var(--bg-subtle); overflow: hidden; }
.ta-meter .fill { height: 100%; width: 0; background: linear-gradient(90deg, var(--brand), var(--brand-2)); transition: width .35s ease; }
.ta-meter .val { flex: 0 0 56px; text-align: right; font-weight: 800; font-variant-numeric: tabular-nums; font-size: 14px; }
.ta-legend { display: flex; gap: 14px; flex-wrap: wrap; margin-top: 8px; font-size: 13px; color: var(--muted); }
.ta-legend span .dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 5px; }
</style>
"""

CUSTOM_JS = r"""
/* ============================================================
   it-m-ai-applications 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 阈值分类器训练台：拖动判定线，观察准确率 / 误报 / 漏报的此消彼长
   3) 视觉任务层次分解台：分类 / 检测 / 分割三种输出形式 + 置信度阈值
   4) 模型评价与数据偏差诊断台：训练构成 → 整体与分类别准确率
   ============================================================ */
(function () {
  'use strict';

  function themeColor(name, fb) {
    try {
      var v = getComputedStyle(document.body).getPropertyValue(name).trim();
      return v || fb;
    } catch (e) { return fb; }
  }
  function rr(ctx, x, y, w, h, r) {
    if (w < 2 * r) r = w / 2;
    if (h < 2 * r) r = h / 2;
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
  }
  function font(weight, size) {
    return weight + ' ' + size + 'px -apple-system, "PingFang SC", "Source Han Sans SC", sans-serif';
  }

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

  /* ---------- 2. 阈值分类器训练台 ---------- */
  /* 特征：一条消息里可疑链接的个数（0–8）。标签：1 = 可疑，0 = 正常。 */
  var SAMP = [
    { x: 0, y: 0 }, { x: 0, y: 0 }, { x: 0, y: 0 },
    { x: 1, y: 0 }, { x: 1, y: 0 }, { x: 1, y: 0 }, { x: 1, y: 0 },
    { x: 2, y: 0 }, { x: 2, y: 0 }, { x: 2, y: 0 },
    { x: 3, y: 0 }, { x: 3, y: 0 },
    { x: 6, y: 0 },
    { x: 1, y: 1 }, { x: 2, y: 1 },
    { x: 3, y: 1 }, { x: 3, y: 1 }, { x: 4, y: 1 },
    { x: 5, y: 1 }, { x: 5, y: 1 }, { x: 6, y: 1 },
    { x: 6, y: 1 }, { x: 7, y: 1 }, { x: 7, y: 1 }, { x: 8, y: 1 }
  ];

  var stageA = document.getElementById('ai1-stage');
  if (stageA) {
    var eTh = document.getElementById('ai1-th');
    var eThV = document.getElementById('ai1-th-val');
    var eAcc = document.getElementById('ai1-acc');
    var eFp = document.getElementById('ai1-fp');
    var eFn = document.getElementById('ai1-fn');
    var eOutA = document.getElementById('ai1-out');

    function statAt(t) {
      var tp = 0, tn = 0, fp = 0, fn = 0;
      SAMP.forEach(function (s) {
        var pred = s.x >= t ? 1 : 0;
        if (s.y === 1 && pred === 1) tp++;
        else if (s.y === 1 && pred === 0) fn++;
        else if (s.y === 0 && pred === 1) fp++;
        else tn++;
      });
      return { tp: tp, tn: tn, fp: fp, fn: fn, acc: (tp + tn) / SAMP.length };
    }

    function drawLine(t) {
      var cv = document.getElementById('ai-line');
      if (!cv || !cv.getContext) return;
      var ctx = cv.getContext('2d');
      var W = cv.width, H = cv.height;
      ctx.clearRect(0, 0, W, H);
      var L = 80, R = W - 26, rowN = 46, rowS = 106, axisY = 146;
      function px(x) { return L + (x / 9) * (R - L); }

      ctx.fillStyle = themeColor('--brand-soft', 'rgba(59,130,246,.10)');
      ctx.fillRect(px(t), 18, R - px(t), axisY - 30);

      ctx.strokeStyle = themeColor('--line', '#e2e8f0');
      ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(L - 14, axisY); ctx.lineTo(R, axisY); ctx.stroke();

      ctx.font = font('600', 12);
      ctx.fillStyle = themeColor('--muted', '#64748b');
      ctx.textAlign = 'center';
      for (var x = 0; x <= 9; x++) {
        ctx.beginPath(); ctx.moveTo(px(x), axisY - 4); ctx.lineTo(px(x), axisY + 4); ctx.stroke();
        ctx.fillText(String(x), px(x), axisY + 20);
      }

      ctx.textAlign = 'right';
      ctx.font = font('700', 13);
      ctx.fillStyle = themeColor('--brand', '#3b82f6');
      ctx.fillText('正常消息', L - 20, rowN + 5);
      ctx.fillStyle = themeColor('--warm-deep', '#b45309');
      ctx.fillText('可疑消息', L - 20, rowS + 5);

      ctx.strokeStyle = themeColor('--brand', '#3b82f6');
      ctx.lineWidth = 3;
      ctx.beginPath(); ctx.moveTo(px(t), 18); ctx.lineTo(px(t), axisY); ctx.stroke();
      ctx.textAlign = 'left';
      ctx.font = font('700', 13);
      ctx.fillStyle = themeColor('--brand', '#3b82f6');
      ctx.fillText('判定线 ' + t, Math.min(px(t) + 7, R - 72), 34);

      SAMP.forEach(function (s) {
        var wrong = (s.y === 1 && s.x < t) || (s.y === 0 && s.x >= t);
        var cy = s.y === 1 ? rowS : rowN;
        ctx.beginPath();
        ctx.arc(px(s.x), cy, 7, 0, Math.PI * 2);
        ctx.fillStyle = s.y === 1 ? themeColor('--warm', '#f59e0b') : themeColor('--brand', '#3b82f6');
        ctx.fill();
        if (wrong) {
          ctx.strokeStyle = themeColor('--danger', '#ef4444');
          ctx.lineWidth = 3;
          ctx.beginPath(); ctx.arc(px(s.x), cy, 12, 0, Math.PI * 2); ctx.stroke();
        }
      });

      ctx.font = font('500', 12);
      ctx.fillStyle = themeColor('--muted', '#64748b');
      ctx.textAlign = 'left';
      ctx.fillText('红圈＝判错的样本　竖线右侧判为「可疑」　横轴＝消息里可疑链接的个数（特征）', 16, H - 10);
    }

    function renderA() {
      var t = Number(eTh.value);
      var st = statAt(t);
      var accPct = Math.round(st.acc * 1000) / 10;
      eThV.textContent = '≥ ' + t;
      eAcc.textContent = accPct + ' %';
      eFp.textContent = st.fp + ' 条';
      eFn.textContent = st.fn + ' 条';
      drawLine(t);

      var best = -1, bestTs = [];
      for (var k = 0; k <= 9; k++) {
        var a = statAt(k).acc;
        if (a > best + 1e-9) { best = a; bestTs = [k]; }
        else if (Math.abs(a - best) < 1e-9) bestTs.push(k);
      }
      var bestPct = Math.round(best * 1000) / 10;

      var parts = [];
      parts.push('<strong>判定线放在 ' + t + '：准确率 ' + accPct + '%，误报 ' + st.fp + ' 条、漏报 ' + st.fn +
        ' 条（共 ' + SAMP.length + ' 条样本）。</strong>');
      parts.push('规则很简单：可疑链接个数大于等于 ' + t + ' 就判为可疑。这根线的位置不是随便定的，' +
        '它应该让判错的数量最少——这就是「从数据里学出规则」的意思。');

      if (bestTs.indexOf(t) >= 0) {
        parts.push('<strong>这是最好成绩：</strong>错误最少，准确率 ' + bestPct + '%。注意最好不要的那根线不止一根（' +
          bestTs.map(function (k) { return k; }).join('、') + '），说明这条边界有一个可以接受的区间。');
      } else {
        parts.push('离最好成绩还差一点：错误最少的判定线在 ' + bestTs.join('、') + ' 的位置，准确率 ' + bestPct + '%。');
      }

      if (st.fp > st.fn) {
        parts.push('<strong>当前的偏向：</strong>误报比漏报多。把真正的正常消息拦成可疑，用户会被打扰。' +
          '如果这个环节是自动拦截，误报的代价很高，就应该把判定线往右移。');
      } else if (st.fn > st.fp) {
        parts.push('<strong>当前的偏向：</strong>漏报比误报多。真正的可疑消息被判成正常，风险被放过去了。' +
          '如果这个环节是安全提醒，漏报的代价很高，就应该把判定线往左移。');
      } else if (st.fp + st.fn === 0) {
        parts.push('<strong>这一步是理想情况：</strong>两类样本完全分开了。真实的场景里很少这么干净——' +
          '特征重叠、样本噪声都会让错误不可避免。');
      } else {
        parts.push('<strong>当前的偏向：</strong>误报和漏报一样多，说明判定线正好卡在两类重叠的地方。');
      }

      parts.push('<strong>易错点：</strong>常见错误是误认为「准确率高就等于模型好」。' +
        '同一个准确率可以对应完全不同的风险——误报多还是漏报多，要由实际场景来决定取舍。' +
        '而准确率本身也会骗人：如果样本里绝大多数都是正常消息，一个永远说「正常」的模型也能拿到很高的准确率。');

      eOutA.className = 'result ' + (bestTs.indexOf(t) >= 0 ? '' : 'warn');
      eOutA.innerHTML = parts.join('<br>');
    }
    eTh.addEventListener('input', renderA);
    renderA();
  }

  /* ---------- 3. 视觉任务层次分解台 ---------- */
  var OBJ = [
    { name: '书', conf: 0.94, kind: 'rect',   x: 66,  y: 66,  w: 158, h: 108 },
    { name: '杯', conf: 0.61, kind: 'circle', cx: 396, cy: 122, r: 58 },
    { name: '尺', conf: 0.38, kind: 'tri',    x1: 516, y1: 174, x2: 648, y2: 174, x3: 582, y3: 62 }
  ];
  function bbox(o) {
    if (o.kind === 'rect') return [o.x, o.y, o.w, o.h];
    if (o.kind === 'circle') return [o.cx - o.r, o.cy - o.r, o.r * 2, o.r * 2];
    return [Math.min(o.x1, o.x2, o.x3), Math.min(o.y1, o.y2, o.y3),
            Math.max(o.x1, o.x2, o.x3) - Math.min(o.x1, o.x2, o.x3),
            Math.max(o.y1, o.y2, o.y3) - Math.min(o.y1, o.y2, o.y3)];
  }

  var stageB = document.getElementById('ai2-stage');
  if (stageB) {
    var mode = 'det';
    var eConf = document.getElementById('ai2-conf');
    var eConfV = document.getElementById('ai2-conf-val');
    var eOutB = document.getElementById('ai2-out');

    function shapePath(ctx, o) {
      if (o.kind === 'rect') { ctx.beginPath(); ctx.rect(o.x, o.y, o.w, o.h); }
      else if (o.kind === 'circle') { ctx.beginPath(); ctx.arc(o.cx, o.cy, o.r, 0, Math.PI * 2); }
      else {
        ctx.beginPath();
        ctx.moveTo(o.x1, o.y1); ctx.lineTo(o.x2, o.y2); ctx.lineTo(o.x3, o.y3); ctx.closePath();
      }
    }

    function drawVision() {
      var cv = document.getElementById('ai-vision');
      if (!cv || !cv.getContext) return;
      var ctx = cv.getContext('2d');
      var W = cv.width, H = cv.height;
      var th = Number(eConf.value) / 100;
      ctx.clearRect(0, 0, W, H);

      ctx.fillStyle = themeColor('--bg-subtle', '#f1f5f9');
      ctx.fillRect(0, 0, W, H);
      ctx.strokeStyle = themeColor('--line', '#e2e8f0');
      ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(22, 206); ctx.lineTo(W - 22, 206); ctx.stroke();

      /* 画面里的物体 */
      OBJ.forEach(function (o) {
        shapePath(ctx, o);
        ctx.fillStyle = themeColor('--card', '#ffffff');
        ctx.fill();
        ctx.strokeStyle = themeColor('--muted', '#64748b');
        ctx.lineWidth = 2;
        ctx.stroke();
        var b = bbox(o);
        ctx.font = font('700', 15);
        ctx.fillStyle = themeColor('--text-secondary', '#475569');
        ctx.textAlign = 'center';
        ctx.fillText(o.name, b[0] + b[2] / 2, b[1] + b[3] / 2 + 6);
      });

      var hidden = 0;
      if (mode === 'cls') {
        ctx.setLineDash([8, 6]);
        ctx.strokeStyle = themeColor('--brand', '#3b82f6');
        ctx.lineWidth = 3;
        rr(ctx, 14, 14, W - 28, 196, 14);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.font = font('700', 15);
        ctx.fillStyle = themeColor('--brand', '#3b82f6');
        ctx.textAlign = 'center';
        ctx.fillText('整张图 → 1 个标签：桌面静物（置信度 0.94）', W / 2, 240);
      } else if (mode === 'det') {
        OBJ.forEach(function (o) {
          var b = bbox(o), show = o.conf >= th;
          if (!show) hidden++;
          ctx.setLineDash([7, 5]);
          ctx.strokeStyle = show ? themeColor('--brand', '#3b82f6') : themeColor('--muted', '#94a3b8');
          ctx.lineWidth = show ? 3 : 2;
          ctx.strokeRect(b[0] - 8, b[1] - 8, b[2] + 16, b[3] + 16);
          ctx.setLineDash([]);
          ctx.font = font('700', 13);
          ctx.textAlign = 'left';
          ctx.fillStyle = show ? themeColor('--brand', '#3b82f6') : themeColor('--muted', '#94a3b8');
          ctx.fillText(o.name + ' ' + o.conf.toFixed(2) + (show ? '' : '（未报出）'),
            b[0] - 8, b[1] - 14);
        });
        ctx.font = font('600', 14);
        ctx.fillStyle = themeColor('--text-secondary', '#475569');
        ctx.textAlign = 'center';
        ctx.fillText('每个物体一条记录：类别 + 位置框 + 置信度', W / 2, 240);
      } else {
        var cols = ['--brand', '--brand-2', '--warm'];
        OBJ.forEach(function (o, i) {
          shapePath(ctx, o);
          ctx.globalAlpha = 0.34;
          ctx.fillStyle = themeColor(cols[i % 3], '#3b82f6');
          ctx.fill();
          ctx.globalAlpha = 1;
          ctx.strokeStyle = themeColor(cols[i % 3], '#3b82f6');
          ctx.lineWidth = 3;
          ctx.stroke();
        });
        ctx.font = font('600', 14);
        ctx.fillStyle = themeColor('--text-secondary', '#475569');
        ctx.textAlign = 'center';
        ctx.fillText('一张与画面同尺寸的掩码图：每个像素都标上类别编号', W / 2, 240);
      }

      /* 输出结构说明 */
      var box = document.getElementById('ai2-struct');
      if (mode === 'cls') {
        box.innerHTML = '<strong>输出形式：</strong>一条记录 —— <code>{ 类别: "桌面静物", 置信度: 0.94 }</code><br>' +
          '<span style="color:var(--muted)">能支撑：相册自动归类、内容初筛这类「只要一个结论」的场景。' +
          '做不到：说不出是什么东西在哪里，也数不出画面里有几个物体。</span>';
      } else if (mode === 'det') {
        box.innerHTML = '<strong>输出形式：</strong>若干条记录 —— <code>{ 类别, 左上角坐标, 宽, 高, 置信度 }</code><br>' +
          '<span style="color:var(--muted)">当前阈值下报出 ' + (3 - hidden) + ' / 3 个物体。' +
          '能支撑：车流计数、货架缺货检查这类「要位置、要数量」的场景。' +
          '注意：阈值调高会把没把握的目标挡在门外，那就是漏检。</span>';
      } else {
        box.innerHTML = '<strong>输出形式：</strong>一张与画面同尺寸的掩码图，每个像素都被标上类别编号。<br>' +
          '<span style="color:var(--muted)">能支撑：测量面积、勾出轮廓这类「要精细边界」的场景。' +
          '代价：这种标注做起来最费工，计算开销也最大。</span>';
      }

      document.querySelectorAll('[data-ai2-mode]').forEach(function (b) {
        b.classList.toggle('selected', b.getAttribute('data-ai2-mode') === mode);
      });

      var parts = [];
      if (mode === 'cls') {
        parts.push('<strong>图像分类：</strong>整张图进去，一个标签出来。输出的信息最少，' +
          '所以它适合做第一道筛选，不适合做计数和定位。');
      } else if (mode === 'det') {
        parts.push('<strong>目标检测：</strong>每个被报出的物体都带着位置和置信度。' +
          (hidden > 0
            ? '当前置信度阈值 ' + th.toFixed(2) + ' 把 ' + hidden + ' 个目标挡在了门外——它们确实在画面里，模型却没报出来，这就是漏检。'
            : '当前置信度阈值 ' + th.toFixed(2) + ' 下，三个物体都被报出来了；把阈值往上拖，就能看到漏检是怎么出现的。'));
        parts.push('<strong>易错点：</strong>常见错误是误认为「模型没报出来就等于画面里没有」。' +
          '置信度阈值是可调的：调低一点漏检少、误报多，调高一点反过来——取舍要看这个应用更怕哪一种错。');
      } else {
        parts.push('<strong>图像分割：</strong>输出精细到像素。它给出的信息最多，代价也最大：' +
          '需要逐像素的标注数据，算力开销也最高。');
      }
      parts.push('<strong>三者的关系：</strong>分类、检测、分割不是三种不同的技术，而是同一条链上越来越细的输出。' +
        '选哪一种，取决于你的应用到底需要什么样的输出——先想清楚输出，再选任务。');
      eOutB.className = 'result';
      eOutB.innerHTML = parts.join('<br>');
    }

    document.querySelectorAll('[data-ai2-mode]').forEach(function (b) {
      b.addEventListener('click', function () { mode = b.getAttribute('data-ai2-mode'); drawVision(); });
    });
    eConf.addEventListener('input', drawVision);
    drawVision();
  }

  /* ---------- 4. 模型评价与数据偏差诊断台 ---------- */
  /* 现场真实数据里，类别甲占 60%、类别乙占 40%（固定不变）。
     模型对某一类的表现，取决于这一类在训练数据里占的比例；数据量本身另有一个折扣。 */
  var FIELD_A = 0.60, FIELD_B = 0.40;

  var stageC = document.getElementById('ai3-stage');
  if (stageC) {
    var eN = document.getElementById('ai3-n');
    var eP = document.getElementById('ai3-p');
    var eNV = document.getElementById('ai3-n-val');
    var ePV = document.getElementById('ai3-p-val');
    var eOutC = document.getElementById('ai3-out');

    function quality(share, n) {
      var base = share >= 0.40 ? 0.93 : share >= 0.25 ? 0.80 : share >= 0.12 ? 0.62 : 0.40;
      var q = n >= 400 ? 1.0 : n >= 200 ? 0.94 : n >= 100 ? 0.86 : 0.74;
      return Math.min(0.97, base * q);
    }

    function bar(id, v) {
      var el = document.getElementById(id);
      if (el) el.style.width = Math.round(v * 100) + '%';
    }

    function renderC() {
      var n = Number(eN.value);
      var shareA = Number(eP.value) / 100;
      var shareB = 1 - shareA;
      var accA = quality(shareA, n);
      var accB = quality(shareB, n);
      var overall = FIELD_A * accA + FIELD_B * accB;
      var worst = Math.min(accA, accB);

      eNV.textContent = n + ' 条';
      ePV.textContent = Math.round(shareA * 100) + ' %';
      document.getElementById('ai3-acc-a').textContent = Math.round(accA * 1000) / 10 + ' %';
      document.getElementById('ai3-acc-b').textContent = Math.round(accB * 1000) / 10 + ' %';
      document.getElementById('ai3-acc-all').textContent = Math.round(overall * 1000) / 10 + ' %';
      bar('ai3-fill-a', accA);
      bar('ai3-fill-b', accB);
      bar('ai3-fill-all', overall);

      var weak = accA < accB ? '类别甲' : '类别乙';
      var weakAcc = Math.round(worst * 1000) / 10;
      var parts = [];

      parts.push('<strong>整体准确率 ' + Math.round(overall * 1000) / 10 + '%，最弱的类别只有 ' + weakAcc + '%。</strong>' +
        '整体这个数字是按现场真实分布加权算出来的：类别甲占六成、类别乙占四成。');

      if (worst < 0.6) {
        parts.push('<strong>有类别几乎不合格：</strong>' + weak + ' 在训练数据里占的比例太低，模型几乎没有机会学好它，' +
          '可是它在现场占了相当大的比重。整体准确率把这个问题盖住了。');
      } else if (worst < 0.8) {
        parts.push('<strong>有类别明显偏弱：</strong>' + weak + ' 的样本在训练数据里偏少，模型对它不够熟。' +
          '它在现场的表现会明显拖后腿，而这个差距从整体数字上看不出来。');
      } else if (n < 200) {
        parts.push('<strong>各类别比较均衡，但数据量偏少：</strong>样本太少时，模型学到的东西不够稳，' +
          '换一批数据表现就可能明显波动。');
      } else {
        parts.push('<strong>各类别表现均衡：</strong>训练数据里两类的比例接近现场分布，数据量也够，' +
          '每一类都学到了比较稳的规则。');
      }

      parts.push('把训练里某一类占比拖到很低，就会看到整体数字还行、那一类却掉下去的组合——' +
        '这就是「模型在演示时很好、换到现场就频频出错」最常见的来源之一。');

      parts.push('<strong>易错点：</strong>常见错误是误认为「整体准确率九成就说明模型可用」。' +
        '整体准确率是一个平均数，平均数会把弱势的那一类藏起来。正确做法是：' +
        '按类别分别看准确率，并且评价要用没参与训练的新数据来做。' +
        '改进的方向也很直接——补齐弱势类别的样本、让训练数据的构成更接近现场的真实分布。');

      var state = worst < 0.6 ? 'error' : (worst < 0.8 || n < 200) ? 'warn' : '';
      eOutC.className = 'result ' + state;
      eOutC.innerHTML = parts.join('<br>');
    }
    eN.addEventListener('input', renderC);
    eP.addEventListener('input', renderC);
    renderC();
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：演示时很准，换个地方怎么就失灵了？", TTS["pretest"], [
        {"q": "人工智能应用与普通程序最本质的区别是：",
         "options": [("规则是从大量带答案的样本里学出来的，不是人事先写死的", True),
                     ("代码写得更长、运行得更快", False),
                     ("它不需要任何数据就能工作", False)],
         "explain": "规则由数据学出来，是这类应用的根基；数据里没有的情况，它多半也处理不好。<strong>错因提醒：</strong>常见错误是误认为「模型自己会想」——它的全部依据都来自训练数据。"},
        {"q": "一个模型在教室里演示几乎次次正确，搬到走廊上却频频出错。最该先查的是：",
         "options": [("训练数据是不是几乎都来自同一个光线和角度", True),
                     ("程序的变量名是不是起得不好", False),
                     ("设备的运行速度是不是不够快", False)],
         "explain": "模型只见过训练数据里的情形；数据没覆盖的光线、角度、背景，它就没有依据。<strong>错因提醒：</strong>容易搞混的是把这类问题当成程序缺陷——现象出在现场，根源往往在数据。"},
        {"q": "要统计画面里有几个人，并给出每个人的位置，应该选哪类任务？",
         "options": [("目标检测，输出带坐标的框和类别", True),
                     ("图像分类，整张图给一个标签", False),
                     ("图像分割，把每个人描成一片区域", False)],
         "explain": "计数和定位都需要位置信息，检测的输出形式正好对应。<strong>错因提醒：</strong>许多同学误认为「越精细的任务越合适」——分割也能用，但标注与计算代价最高，需求只要位置就不必用分割。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "规则是人写死的，还是从数据里学出来的？", TTS["module-1"], f'''
        <div class="inner-card">
          <p><strong>为什么要学这一课？</strong>你已经知道互联网服务怎么工作，也见过不少会「认图」「会说话」的应用。但它们为什么有时准、有时不准，靠猜是猜不出来的，<strong>所以</strong>我们要先弄清一个应用是由哪些要素搭起来的。</p>
        </div>
        <p style="font-size:17px;margin:12px 0">普通程序是<strong>把规则写死</strong>：人告诉它，什么情况该做什么。机器学习是<strong>把规则学出来</strong>：人给一批带答案的样本，模型自己去总结其中的规律。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>数据与标签：</strong>一批样本，每条都带着标准答案。标签的质量直接决定模型能学到什么。</div></div>
          <div class="step"><span class="n">2</span><div><strong>特征：</strong>从样本里挑出来、交给模型看的可测量信息。挑错了特征，模型再强也没有依据。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>模型与预测：</strong>模型把学到的规律固定下来，对新样本给出预测结果。</div></div>
          <div class="step"><span class="n">4</span><div><strong>评价：</strong>用没参与训练的新数据检验，才能看出它是学会了规律，还是只记住了答案。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="人工智能应用六要素链路图：数据、特征、标签、模型、预测、评价">
          <figcaption>六个要素串成一条链：数据与标签进入训练，特征决定模型看得到什么，评价用新数据检验结果</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🧠</span><div><strong>记忆锚点：</strong>把这六个要素想成一次做饭。数据是食材，标签是菜谱上的成品照片，特征是刀工和火候，模型是掌勺的过程，预测是端上桌的那盘菜，评价是别人尝一口。食材里没有的东西，端上桌也不会有。</div></div>
{insight_box([
    {"lens": "看见它", "text": "同一个需求可以用不同特征来描述。用「可疑链接个数」和用「发信时间」识别的可疑消息，表现和误判类型完全不同。"},
    {"lens": "拆开它", "text": "任何一个人工智能应用都能拆成这六步。哪一步含糊，最终效果就无法解释，也无法改进。"},
    {"lens": "迁移它", "text": "这种「给样本、学规律、用新数据检验」的做法，也是人学习的常见路径：练习、反馈、再检验。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "阈值分类器训练台：判定线该放在哪里？", TTS["lab-1"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">拖动判定线，把两类样本尽量分开，看准确率、误报数和漏报数怎么此消彼长。</p>
        <div class="lab-panel">
          <div id="ai1-stage">
            <div class="slider-row">
              <label for="ai1-th">判定线位置</label>
              <input type="range" id="ai1-th" min="0" max="9" step="1" value="3">
              <span class="readout-cell" style="flex:0 0 96px"><span class="k">判为可疑</span><span class="v" id="ai1-th-val">≥ 3</span></span>
            </div>
          </div>
          <canvas id="ai-line" width="680" height="210" aria-label="阈值分类器样本分布图" style="display:block;width:100%;border-radius:12px;background:var(--card);"></canvas>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">准确率</span><span class="v green" id="ai1-acc">—</span></div>
            <div class="readout-cell"><span class="k">误报（正常判成可疑）</span><span class="v" id="ai1-fp">—</span></div>
            <div class="readout-cell"><span class="k">漏报（可疑判成正常）</span><span class="v" id="ai1-fn">—</span></div>
          </div>
          <p class="result warn" id="ai1-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">⚖️</span><div><strong>动手找一找：</strong>把判定线在 3 和 4 之间来回挪。你会发现准确率一样，可误报和漏报的数量换了位置——同一个成绩，风险完全不同。这就是「阈值要按场景选」，而不是按分数选。</div></div>
    ''', tag="动手实验室", bloom="apply"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "视觉任务分三层：输出形式决定它能做什么", TTS["module-2"], f'''
        <div class="inner-card">
          <p><strong>同一张图，三种任务。</strong>图像分类、目标检测、图像分割，差别不在「谁更先进」，而在<strong>输出的形式</strong>：一个标签、一串位置框、还是一张逐像素的掩码图。</p>
        </div>
        <div class="grid grid-3">
          <div class="inner-card">
            <p><strong>图像分类</strong></p>
            <p style="color:var(--muted)">整张图给一个标签。</p>
          </div>
          <div class="inner-card">
            <p><strong>目标检测</strong></p>
            <p style="color:var(--muted)">每个物体带位置框和置信度。</p>
          </div>
          <div class="inner-card">
            <p><strong>图像分割</strong></p>
            <p style="color:var(--muted)">每个像素都归到某一类。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="计算机视觉三类任务输出形式对比图：图像分类、目标检测、图像分割">
          <figcaption>分类给一个标签 · 检测给带位置的框 · 分割给逐像素掩码：信息越细，标注与计算代价越高</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">最容易搞混的是<strong>把检测当成「更准的分类」</strong>。它们解决的不是同一件事：分类回答「这是什么」，检测还回答「在哪里、有几个」。另一个常见错误是<strong>忽略置信度阈值</strong>——检测器报出的每个目标都带一个置信度，调高阈值会漏检，调低阈值会误报。误认为「模型没报出来就是画面里没有」，是这一课最容易踩的坑。</p>
        </div>
{insight_box([
    {"lens": "比较它", "text": "三类任务是同一条链上越来越细的输出。信息越多，需要的数据标注越贵、算力开销越大，并不是越细越好。"},
    {"lens": "迁移它", "text": "「先想清楚需要什么输出，再决定用什么方法」这条判断在这里成立，在其他问题的解决里同样成立。"},
])}
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "视觉任务层次分解台：同一张图，三种输出", TTS["lab-2"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">切换任务类型，看同一张画面上的标注怎么变；再拖动置信度阈值，观察漏检是怎么出现的。</p>
        <div class="lab-panel">
          <div id="ai2-stage">
            <div class="ta-face">
              <button class="choice" data-ai2-mode="cls" style="text-align:center">图像分类</button>
              <button class="choice selected" data-ai2-mode="det" style="text-align:center">目标检测</button>
              <button class="choice" data-ai2-mode="seg" style="text-align:center">图像分割</button>
            </div>
            <div class="slider-row">
              <label for="ai2-conf">置信度阈值</label>
              <input type="range" id="ai2-conf" min="0" max="95" step="5" value="50">
              <span class="readout-cell" style="flex:0 0 96px"><span class="k">阈值</span><span class="v" id="ai2-conf-val">0.50</span></span>
            </div>
          </div>
          <canvas id="ai-vision" width="680" height="258" aria-label="视觉任务输出形式示意图" style="display:block;width:100%;border-radius:12px;background:var(--card);"></canvas>
          <div class="ta-struct" id="ai2-struct"></div>
          <p class="result" id="ai2-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔎</span><div><strong>试出边界：</strong>在检测模式下把置信度阈值从 0.50 拖到 0.95，看着那个没把握的目标消失；再拖到 0.30，看它回来。画面里它一直在，变的只是「模型敢不敢报」。</div></div>
    ''', tag="动手实验室", bloom="analyze"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：从「演示很准」到「现场失灵」，问题出在哪？", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:var(--warm)">
          <p style="margin:0"><strong>题目：</strong>某小组的识别装置在教室演示时几乎次次正确，到走廊使用却频频出错。程序一行没改，镜头也干净。请分析原因并给出改进方案。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先看数据从哪来：</strong>训练样本几乎全是在教室、固定光线下采集的。走廊的光线和角度没出现过，模型就没有依据。</div></div>
          <div class="step"><span class="n">2</span><div><strong>再看各类样本的数量：</strong>其中一类样本只占很小一部分，模型几乎没有机会学好它。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>然后看评价方式：</strong>他们只看整体准确率。样本多的那一类会把平均数拉高，样本少的那一类的糟糕表现被盖住了。</div></div>
          <div class="step"><span class="n">4</span><div><strong>给出改进：</strong>补充不同光线与角度的样本；把样本少的那一类补齐；评价时按类别分别看，并且只用没参与训练的新数据来测。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">很多同学误认为<strong>「换个更好的模型就能解决」</strong>，于是不停换方法。可问题出在数据没有覆盖现场的情形——换模型只是把同一份偏差学得更牢。另一处容易搞混的是<strong>用整体准确率下结论</strong>：一个永远回答「都是多数类」的模型，在样本极不均衡时也能拿到很高的准确率，但它对少数类几乎毫无用处。</p>
        </div>
    ''', tag="例题示范", bloom="evaluate"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "下面哪句话是正确的？",
         "options": [("评价模型必须用没参与训练的新数据", True),
                     ("在训练数据上表现好，就说明模型学得好", False),
                     ("模型越复杂，现场表现一定越好", False)],
         "explain": "在训练数据上表现好，可能只是把答案记住了，所以要留一部分数据专门用来检验。<strong>错因提醒：</strong>常见错误是误认为「训练时分数高就能用」——这叫把记忆力当成了能力。"},
        {"q": "一个检测器把画面里的三个物体只报出了两个。最恰当的解释是：",
         "options": [("第三个目标的置信度低于当前阈值，被挡在门外了，属于漏检", True),
                     ("画面里本来就只有两个物体", False),
                     ("模型坏了，必须重新训练一次", False)],
         "explain": "报不报由置信度阈值决定，阈值是可调的。<strong>错因提醒：</strong>容易搞混的是把「没报出来」直接当成「不存在」——先看阈值，再谈模型好坏。"},
        {"q": "训练数据里甲类占九成、乙类占一成，而现场两者各占一半。下面哪个判断最站得住脚？",
         "options": [("整体准确率可能还看得过去，但乙类的表现会明显偏弱，需要补齐乙类样本", True),
                     ("只要整体准确率超过九成，这个模型就可以直接用", False),
                     ("把模型换成更复杂的一种，乙类的问题就会自动消失", False)],
         "explain": "训练数据的构成决定了模型对每一类的熟练程度；整体准确率会掩盖弱势类别。<strong>错因提醒：</strong>许多同学误认为「一个数字就能代表模型好坏」——按类别分开看，才看得到真正的问题。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：当一次模型评估员，把平均数背后的问题挖出来", TTS["synthesis"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">拖动两个滑块改变训练数据的构成，看整体准确率和各个类别准确率怎么变。现场的真实分布固定为：类别甲六成、类别乙四成。</p>
        <div class="lab-panel">
          <div id="ai3-stage">
            <div class="slider-row">
              <label for="ai3-n">训练样本总数</label>
              <input type="range" id="ai3-n" min="40" max="800" step="40" value="400">
              <span class="readout-cell" style="flex:0 0 110px"><span class="k">样本</span><span class="v" id="ai3-n-val">400 条</span></span>
            </div>
            <div class="slider-row">
              <label for="ai3-p">类别甲在训练数据中的占比</label>
              <input type="range" id="ai3-p" min="5" max="95" step="5" value="50">
              <span class="readout-cell" style="flex:0 0 110px"><span class="k">甲占比</span><span class="v" id="ai3-p-val">50 %</span></span>
            </div>
          </div>
          <div class="ta-meter"><span class="lbl">整体准确率</span><span class="bar"><span class="fill" id="ai3-fill-all"></span></span><span class="val" id="ai3-acc-all">—</span></div>
          <div class="ta-meter"><span class="lbl">类别甲</span><span class="bar"><span class="fill" id="ai3-fill-a"></span></span><span class="val" id="ai3-acc-a">—</span></div>
          <div class="ta-meter"><span class="lbl">类别乙</span><span class="bar"><span class="fill" id="ai3-fill-b"></span></span><span class="val" id="ai3-acc-b">—</span></div>
          <div class="ta-legend">
            <span><span class="dot" style="background:var(--brand)"></span>整体准确率按现场真实分布加权</span>
            <span><span class="dot" style="background:var(--brand-2)"></span>各类别表现由训练数据构成决定</span>
          </div>
          <p class="result" id="ai3-out" style="margin-top:12px"></p>
        </div>
        <div class="inner-card">
          <p><strong>写下来，说给同桌听：</strong>为什么一个模型的整体准确率看着还可以，却在实际使用中频频出错？</p>
          <textarea id="syn-answer" rows="3" placeholder="因为整体准确率是平均数，当某一类在训练数据里占比太低时，模型学不好它，可是它在现场占的比重并不小，所以……"></textarea>
        </div>
    ''', tag="综合任务", bloom="evaluate"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换一个情境，看看规律还在不在", TTS["posttest"], [
        {"q": "要在一块地里按作物长势把农田分成几片区域，并量出每片的面积。最合适的任务是：",
         "options": [("图像分割，输出逐像素的区域掩码，便于计算面积", True),
                     ("图像分类，整张图给一个「长势良好」的标签", False),
                     ("目标检测，给每株作物画一个矩形框", False)],
         "explain": "要按区域量面积，就需要精确的边界，只有分割的输出形式对得上。<strong>错因提醒：</strong>常见错误是只要「识别出来就行」，忽略了需求里的「量面积」这一步，矩形框量不准不规则边界。"},
        {"q": "一个识别应用只收集到 60 条训练样本，两类各占一半。最该先做的事是：",
         "options": [("补充样本，尤其是补充更多样、更接近现场情况的样本", True),
                     ("把判定阈值调到极限，先把准确率拉上去", False),
                     ("换更复杂的模型，让它自己补齐缺失的部分", False)],
         "explain": "样本太少，学到的规律不稳，换一批数据表现就变。数据的量和多样性是第一位的。<strong>错因提醒：</strong>容易搞混的是把调参当成万能药——参数只能调整已有的信息，变不出数据里没有的东西。"},
        {"q": "某应用只看整体准确率，报告写着 92%。下面哪种做法最能发现隐藏的问题？",
         "options": [("按类别分别统计准确率，并检查各类样本在训练数据里的占比", True),
                     ("把整体准确率再算一遍，确认算得没错", False),
                     ("把准确率的目标从 92% 提高到 95%", False)],
         "explain": "整体数字是平均数，分类别统计才能看出弱势类别。<strong>错因提醒：</strong>许多同学误认为「一个数字就够用」——平均数最容易掩盖的，正是最需要被看见的那一类。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把自己讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>规则从哪来</strong>：普通程序把规则写死，机器学习从带答案的样本里把规则学出来。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>六个要素</strong>：数据、特征、标签、模型、预测、评价；评价必须用没参与训练的新数据。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>输出决定任务</strong>：分类给一个标签，检测给带位置的框，分割给逐像素掩码；按需要的输出选任务。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>别只看平均数</strong>：整体准确率会掩盖弱势类别，按类别分别看，才能发现真正的问题。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:var(--warm)">
          <p style="margin:0"><strong>回到开头那台装置：</strong>它并不是坏了，而是数据里没有走廊那种光线与角度，训练数据里又有一类样本太少。补上多样化的样本、把弱势类别补齐、评价改成按类别看，同一套流程就能在现场站住脚。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「数据、特征、标签、评价」这四个词，把一个识别应用从收集数据到投入使用的过程讲清楚，并说明哪一步最容易出问题。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "说出机器学习和普通程序在「规则来源」上的区别，并各举一个例子。",
            "列出这类人工智能应用的六个要素，并说明「评价」为什么必须用新数据。",
            "说明图像分类、目标检测、图像分割在输出形式上的差别。",
        ],
        [
            "为「校园里统计每天有多少辆自行车停在指定区域」选择任务类型，写出需要的特征、标签与输出形式，并说明评价方式。",
            "某模型整体准确率 90%，但某一类只有 55%。分析最可能的原因，并给出两条改进办法。",
        ],
        [
            "找一个人工智能应用，分析它的训练数据可能缺少哪一类情形，会造成什么实际影响。",
            "为上面那个应用写一份评价方案：按类别统计哪些指标，用什么样的新数据来测，为什么这样测更可靠。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-m-ai-applications",
    "node_id": "it-m-ai-applications",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "middle",
    "stage_cn": "初中",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 初中",
    "title": "人工智能典型应用",
    "name_en": "Typical Applications of Artificial Intelligence",
    "grade": 9,
    "grade_cn": "九年级",
    "domain": "ai-society",
    "domain_cn": "人工智能与智慧社会",
    "lesson_type": "concept-application",
    "version": "1.0.0",
    "description": "从一个「演示很准、现场失灵」的识别装置出发，理解机器学习与普通程序在规则来源上的区别，用数据、特征、标签、模型、预测、评价六个词拆解典型应用，区分图像分类、目标检测、图像分割三类计算机视觉任务的输出形式，并学会按类别评价模型、识别数据构成带来的偏差。",
    "tags": ["人工智能应用", "机器学习", "特征与标签", "计算机视觉", "图像分类", "目标检测", "图像分割", "模型评价", "数据偏差"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》初中「人工智能与智慧社会」——了解机器学习、计算机视觉等典型应用场景。",
    "hero_question": "一个应用演示时很准，换到现场就失灵——问题到底出在哪一环？",
    "hero_alt": "人工智能典型应用知识结构图：规则从数据里学出来、视觉任务的三层输出、数据构成与模型评价三栏",
    "hero_caption": "规则从数据里学出来 · 输出形式决定任务 · 数据构成决定表现 · 评价要分类别看",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的实验都会围着它转。",
    "anchor_choices": [
        {"t": "人工智能和普通程序差在哪里？", "d": "规则是人写的，还是学出来的", "v": "人工智能和普通程序差在哪里"},
        {"t": "认出一张图、框出一个物体，是同一件事吗？", "d": "三类视觉任务的输出形式", "v": "认出一张图、框出一个物体，是同一件事吗"},
        {"t": "为什么整体准确率好看，实际却常出错？", "d": "平均数会把弱势的那一类盖住", "v": "为什么整体准确率好看，实际却常出错"},
        {"t": "模型没报出来的目标，是不是就不存在？", "d": "置信度阈值与漏检的关系", "v": "模型没报出来的目标，是不是就不存在"},
    ],
    "objectives": [
        "能说清机器学习和传统程序的区别：规则是人写死的，还是从数据里学出来的",
        "能用数据、特征、标签、模型、预测、评价六个要素拆解一个典型的人工智能应用",
        "能区分图像分类、目标检测、图像分割三类计算机视觉任务，并说出它们输出形式的差别",
        "能判断模型为什么在演示时表现好、在现场表现差，并指出数据构成与评价方式上的问题",
    ],
    "objectives_plain": [
        "能说清机器学习和传统程序的区别：规则是人写死的，还是从数据里学出来的",
        "能用数据、特征、标签、模型、预测、评价六个要素拆解一个典型的人工智能应用",
        "能区分图像分类、目标检测、图像分割三类计算机视觉任务，并说出它们输出形式的差别",
        "能判断模型为什么在演示时表现好、在现场表现差，并指出数据构成与评价方式上的问题",
    ],
    "standards": [
        {"content": "了解机器学习、计算机视觉等典型应用场景。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》人工智能与智慧社会 · 初中"},
        {"content": "在真实情境中认识数据与模型的关系，理解数据质量与构成对结果的影响，负责任地使用智能技术。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》数据与编码 / 信息社会责任 · 初中"},
    ],
    "prereqs": [],
    "prereqs_name": "",
    "prereqs_meta": "",
    "leads_to": ["it-m-ai-modeling"],
    "next_meta": "it-m-ai-modeling",
    "section_images": ["assets/it-m-ai-applications-fig1.webp", "assets/it-m-ai-applications-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "一台「演示很准、现场失灵」的装置，问题往往在数据上，而不在程序里。带着它开始。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能拆开一个智能应用，也能看出它的短板在哪。",
        "objectives": "看清四件事：规则从哪来、六个要素、三类视觉任务的输出、按类别评价模型。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "六个要素串成一条链：数据、特征、标签、模型、预测、评价。数据里没有的情形，模型也答不出来。",
        "lab-1": "把判定线在 3 和 4 之间来回挪：准确率一样，误报和漏报的数量却换了位置。",
        "module-2": "分类给一个标签、检测给带位置的框、分割给逐像素掩码。先想清楚需要什么输出，再选任务。",
        "lab-2": "检测模式下把置信度阈值从 0.50 拖到 0.95，看没把握的目标消失；拖到 0.30 再让它回来。",
        "worked-example": "四步走：数据从哪来、各类样本多少、评价怎么看、怎么改进。改数据比换模型更对症。",
        "conceptest-1": "干扰项里藏着最常见的那几个错误想法，选完看清每一个解释。",
        "synthesis": "把「甲占比」拖到 90%，看整体数字还行、乙类却掉下去——平均数最容易盖住这件事。",
        "posttest": "换了面积测量和样本不足的新情境，看看你还能不能用上输出形式与分类别评价。",
        "summary": "用「数据、特征、标签、评价」四个词，把一个识别应用从采数据到投入使用的过程讲清楚。",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课是「人工智能与智慧社会」领域的典型应用课，承接小学阶段的人工智能初识，为后续的模型体验课做铺垫。设计上不引入任何品牌、产品与在线服务，全部用可计算、可观察的模拟来承载概念：用阈值分类器训练台把「从数据里学出规则」变成可以拖动的一根判定线，并让准确率、误报、漏报同时可见，引出「同一成绩、不同风险」的工程判断；用视觉任务层次分解台把分类、检测、分割三种输出形式并排对比，并用置信度阈值解释漏检；用模型评价与数据偏差诊断台把训练数据构成与分类别准确率连起来，让学生亲眼看到整体平均数如何掩盖弱势类别。价值取向上强调数据质量与样本均衡的重要性，以及负责任地看待和使用智能技术的态度。",
    "plan_table": """| 1 | cover | 人工智能典型应用 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：演示时很准，换个地方怎么就失灵了？ | 起·前测（暴露直觉） |
| 5 | concept | 规则是人写死的，还是从数据里学出来的？ | 承·概念一 |
| 6 | interactive | 阈值分类器训练台：判定线该放在哪里？ | 承·实验室一（准确率与误报漏报可观察） |
| 7 | concept | 视觉任务分三层：输出形式决定它能做什么 | 承·概念二 |
| 8 | interactive | 视觉任务层次分解台：同一张图，三种输出 | 承·实验室二（输出结构与漏检可见） |
| 9 | concept | 例题示范：从「演示很准」到「现场失灵」，问题出在哪？ | 转·重难点突破（分步示范 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：当一次模型评估员，把平均数背后的问题挖出来 | 合·迁移应用 |
| 12 | quiz | 后测：换一个情境，看看规律还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把自己讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：规则从数据里学出来 / 视觉任务的三层输出 / 数据构成与模型评价三栏\n- P5 六要素链路图（已生成）：数据 → 特征 → 标签 → 模型 → 预测 → 评价\n- P7 三类视觉任务输出对比图（已生成）：分类给标签 · 检测给位置框 · 分割给逐像素掩码\n- 若需补充：不含任何品牌与在线服务界面的通用示意图（不出现真实产品名称与商标文字）",
}
