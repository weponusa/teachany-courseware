# -*- coding: utf-8 -*-
"""初中信息科技 · 简单 AI 模型体验（G9）—— 补齐课标「人工智能与智慧社会」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-m-ai-modeling-fig1.webp'
F2 = './assets/it-m-ai-modeling-fig2.webp'

TTS = {
    "hero": "先看一个现象。有个小组想做一个「根据每周练习时长预测测试得分」的模型。他们在自己班收集了三十条记录，训练之后在训练记录上拟合得很好；可拿到隔壁班去用，误差大得离谱。程序一行没改，方法也没换。问题出在两件事上：模型的参数是从数据里调出来的，而数据只覆盖了他们班那点情况。这节课我们亲手训一个最简单的模型，把它拆成可以看见的四个量——参数、损失、梯度、学习率，看清参数到底是怎么被数据一次次调出来的，也看清数据为什么决定了模型的上限。",
    "problem-anchor": "开始之前，先挑一个你最想弄明白的问题。是想知道模型里的参数到底是怎么被调出来的，还是想知道学习率这个数为什么调大调小都不行，又或者你想弄明白为什么在训练数据上表现很好、换一批数据就差很多。选好以后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出模型是一个带参数的函数，训练就是用数据把参数自动调到合适的位置。第二，能读出并能写出训练循环的四步伪代码：预测、算损失、算梯度、更新参数。第三，能通过实验说明学习率过大、过小和适中的三种后果，并给出调参方向。第四，能用训练误差和测试误差判断模型是欠拟合、合适还是过拟合，并说清数据覆盖范围对模型的影响。",
    "pretest": "先做三道小题，凭现在的想法选就行，选错了也没关系，正好能看出哪里需要重点听。选完会立刻出现解释。",
    "module-1": "先把模型这个词落地。在这节课里，模型就是一个带参数的函数：输入乘一个权重、再加一个偏置，写成 y 等于 w 乘 x 加 b。这里的 w 和 b 就叫参数，也常叫权重和偏置。训练的意思不是人去猜参数，而是用一套固定的流程把参数自动调到合适的位置。这套流程只有四步：先用当前参数做一次预测，再把预测和真实答案的差距算成一个数，这个数叫损失；然后算出损失对每个参数的梯度，也就是往哪个方向调能让损失下降；最后沿着梯度的反方向把参数挪一小步。重复这几步，损失就会一路往下走。",
    "lab-1": "我们来亲手把参数调出来。屏幕左边是一批样本点，右边是损失随训练轮次变化的曲线。你要拖的是学习率——也就是每一步把参数挪多大。按一次训练一步，看 w、b 和损失怎么变。你会发现三种典型情况：学习率取小一点，损失稳稳地往下掉，但走得慢；取到中间一段，几步就压到最低；再往上调，损失开始上下震荡，最后会被推得越来越大，这叫发散，也就是我们常说的跑飞。",
    "module-2": "现在我们看第二个因素：数据。模型能学到的东西，全部来自它见过的数据，所以有三个限制绕不开。第一是覆盖范围：训练数据里只出现过练习时长半小时以内的记录，模型对两小时的情形就只能靠外推，而外推是没有依据的猜测。第二是数据量：样本太少时，参数会被个别样本带着跑，换一批数据结果就变。第三是数据质量：一条明显录错的记录会把参数和损失都带偏。还有一条最容易忽略的：训练损失小不等于模型好，因为模型可能只是记住了答案。要判断它是不是学到了规律，只能用一批没参与训练的新数据来测，这叫做留出法。",
    "lab-2": "现在你来亲手验证覆盖范围这件事。屏幕上的曲线是这批数据的真实规律，样本点只落在左边一段区间里，这段区间由你拖动。拖动覆盖范围，关注三个数字：覆盖区内的误差、覆盖区外的误差，以及在区间最右端那个点上的预测值和真实值差了多少。你会发现一件很值得警惕的事：覆盖区内的误差一直很小，看起来模型挺好；可训练数据没铺到的地方，模型的输出和真实规律越差越远。",
    "worked-example": "我们分析一个具体现象：学习率调大了，损失为什么反而会越来越大。第一步，看清更新公式，参数的新值等于旧值减去学习率乘梯度，梯度告诉方向，学习率决定步子大小。第二步，看一步之内参数被推了多远。设当前 w 等于零，算出这批数据的梯度后你会发现，一步就跳过了最好的位置。第三步，看第二步为什么会放大：跳过之后预测偏差换了个方向，梯度也跟着换方向，如果步子还是那么大，参数就会在好位置两侧来回越跳越远。第四步，给出判断和处置：损失不降反升、而且越来越大，就是学习率过大，应该把它往小调；反过来，训练很多轮损失还在缓慢下降，那是走得慢，可以适当调大一点。顺序永远是先让损失稳稳下降，再去追求更快。",
    "conceptest-1": "现在用三个容易弄错的说法考考你。请仔细读每一个选项，选出你认为正确的那个，然后看解释。",
    "synthesis": "学到这里，请你当一次模型体检员。屏幕上是一个模型，它的复杂度由阶数决定，也就是多项式的次数；训练数据量由你拖动。每一组设置，系统都会重新用训练数据把参数拟合一遍，然后在训练数据和一批没参与训练的新数据上分别测误差，给出两个数字。你会看到两个方向的毛病：阶数太低时，两条误差都压不下去，模型连训练数据都拟合不好，这叫欠拟合；阶数太高而数据太少时，训练误差小到接近零、测试误差却明显涨上去，两条误差分叉了，这叫过拟合，模型把数据里的抖动当成了规律记住。",
    "posttest": "最后换两个情境检验一下。这次出现了调参诊断和数据覆盖不足的问题，看看你能不能把训练循环的四步、学习率的三种后果，以及训练误差和测试误差的对比用上去。",
    "summary": "这节课我们弄清楚了三件事。第一，模型是一个带参数的函数，参数就是权重和偏置；训练是一套固定流程把参数自动调好，四步循环是预测、算损失、算梯度、更新参数。第二，学习率决定每一步挪多大：太小走得慢，太大震荡甚至发散跑飞，适中的时候又快又稳，所以调参要先稳住再求快。第三，数据决定了模型的上限：训练数据没覆盖的情形只能靠没有依据的外推，数据太少会让参数不稳；而判断模型好不好，不能看训练损失，要看它在没参与训练的新数据上的测试误差，两个误差一对比，欠拟合和过拟合就分得清了。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出训练循环的四步伪代码，并解释损失、梯度、学习率各起什么作用。第二层能力应用，动手做：拿一张表记录一次训练实验，固定数据、改变学习率，记录每次最终损失的变化趋势，给出三档结论。第三层迁移挑战，选做：为一个真实需求设计一次训练实验，说明训练数据要覆盖哪些情形、用哪一批新数据来做测试、两个误差差多少你会判定为过拟合，并写出你的判断依据。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 参数与训练循环", "lab-1": "实验室一 梯度下降训练台",
    "module-2": "概念二 数据决定模型的上限", "lab-2": "实验室二 覆盖范围与外推检验台",
    "worked-example": "例题讲解", "conceptest-1": "概念测试",
    "synthesis": "综合任务 模型体检台", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

LAB_CSS = """
<style>
.ta-code { margin: 12px 0; padding: 14px 16px; border-radius: 12px; background: var(--bg-subtle);
  border: 1px solid var(--line-subtle); font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 13.5px; line-height: 1.85; white-space: pre; overflow-x: auto; color: var(--text-secondary); }
.ta-code b { color: var(--brand); }
.ta-stage { margin-top: 12px; }
.ta-meter { display: flex; align-items: center; gap: 10px; margin-top: 10px; }
.ta-meter .lbl { flex: 0 0 108px; font-size: 13px; font-weight: 700; }
.ta-meter .bar { flex: 1; height: 12px; border-radius: 999px; background: var(--bg-subtle); overflow: hidden; }
.ta-meter .fill { height: 100%; width: 0; background: linear-gradient(90deg, var(--brand), var(--brand-2)); transition: width .35s ease; }
.ta-meter .val { flex: 0 0 66px; text-align: right; font-weight: 800; font-variant-numeric: tabular-nums; font-size: 14px; }
.ta-btns { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px; }
.ta-btns .choice { flex: 1; min-width: 104px; text-align: center; padding: 12px 14px; }
.ta-legend { display: flex; gap: 14px; flex-wrap: wrap; margin-top: 8px; font-size: 13px; color: var(--muted); }
.ta-legend .dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 5px; }
</style>
"""

CUSTOM_JS = r"""
/* ============================================================
   it-m-ai-modeling 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 梯度下降训练台：学习率 → 参数与损失的三种后果（收敛 / 震荡 / 发散）
   3) 覆盖范围与外推检验台：训练数据覆盖区间 → 区内误差与区外误差
   4) 模型体检台：阶数 × 数据量 → 训练误差与测试误差（欠拟合 / 合适 / 过拟合）
   ============================================================ */
(function () {
  'use strict';

  function themeColor(name, fb) {
    try {
      var v = getComputedStyle(document.body).getPropertyValue(name).trim();
      return v || fb;
    } catch (e) { return fb; }
  }
  function font(weight, size) {
    return weight + ' ' + size + 'px -apple-system, "PingFang SC", "Source Han Sans SC", sans-serif';
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
  function fixed(v, n) {
    if (!isFinite(v)) return '—';
    var a = Math.abs(v);
    if (a >= 1e6) return (v / 1e6).toFixed(2) + '×10^6';
    if (a >= 1e4) return (v / 1e3).toFixed(1) + '×10^3';
    return v.toFixed(n === undefined ? 2 : n);
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

  /* ---------- 2. 梯度下降训练台 ---------- */
  /* 固定的 11 条样本：输入是每周练习时长（小时），答案是测试得分。
     真实关系大致是 y = 2x + 1，带一点不可避免的抖动。 */
  var DATA = [
    [0, 1.4], [1, 3.4], [2, 4.4], [3, 7.6], [4, 8.4], [5, 11.6],
    [6, 12.4], [7, 15.5], [8, 16.3], [9, 19.4], [10, 21.7]
  ];
  var LOSS_FLOOR = 0.31;   /* 这批固定数据的最小损失：由样本自身的抖动决定 */

  var stageA = document.getElementById('aim1-stage');
  if (stageA) {
    var eLr = document.getElementById('aim1-lr');
    var eLrV = document.getElementById('aim1-lr-val');
    var eW = document.getElementById('aim1-w');
    var eB = document.getElementById('aim1-b');
    var eL = document.getElementById('aim1-loss');
    var eEp = document.getElementById('aim1-ep');
    var eOutA = document.getElementById('aim1-out');
    var timer = null;

    var st = { w: 0, b: 0, ep: 0, hist: [], flying: false };

    function mse(w, b) {
      var s = 0;
      for (var i = 0; i < DATA.length; i++) {
        var d = (w * DATA[i][0] + b) - DATA[i][1];
        s += d * d;
      }
      return s / DATA.length;
    }
    function grad(w, b) {
      var gw = 0, gb = 0;
      for (var i = 0; i < DATA.length; i++) {
        var d = (w * DATA[i][0] + b) - DATA[i][1];
        gw += 2 * DATA[i][0] * d;
        gb += 2 * d;
      }
      return [gw / DATA.length, gb / DATA.length];
    }
    function doStep(lr) {
      if (st.flying) return;
      var g = grad(st.w, st.b);
      st.w -= lr * g[0];
      st.b -= lr * g[1];
      st.ep++;
      var L = mse(st.w, st.b);
      if (!isFinite(L) || L > 1e8) { st.flying = true; L = Math.min(L, 1e9); }
      st.hist.push(L);
      if (st.hist.length > 600) st.hist.shift();
    }
    function reset() {
      st = { w: 0, b: 0, ep: 0, hist: [], flying: false };
      st.hist.push(mse(0, 0));
    }

    function drawFit() {
      var cv = document.getElementById('aim1-fit');
      if (!cv || !cv.getContext) return;
      var ctx = cv.getContext('2d');
      var W = cv.width, H = cv.height;
      var L = 56, R = W - 22, T = 22, Bm = H - 34;
      ctx.clearRect(0, 0, W, H);
      var yMax = 24;
      function px(x) { return L + (x / 10) * (R - L); }
      function py(y) { return Bm - (y / yMax) * (Bm - T); }

      ctx.fillStyle = themeColor('--brand-soft', 'rgba(59,130,246,.10)');
      ctx.fillRect(L, T, R - L, (Bm - T) * 0.5);

      ctx.strokeStyle = themeColor('--line', '#e2e8f0');
      ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(L, Bm); ctx.lineTo(R, Bm); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(L, T); ctx.lineTo(L, Bm); ctx.stroke();

      ctx.font = font('600', 11);
      ctx.fillStyle = themeColor('--muted', '#64748b');
      ctx.textAlign = 'center';
      for (var x = 0; x <= 10; x += 2) {
        ctx.beginPath(); ctx.moveTo(px(x), Bm); ctx.lineTo(px(x), Bm + 4); ctx.stroke();
        ctx.fillText(String(x), px(x), Bm + 17);
      }
      ctx.textAlign = 'right';
      for (var y = 0; y <= 24; y += 6) ctx.fillText(String(y), L - 8, py(y) + 4);
      ctx.textAlign = 'left';
      ctx.fillText('每周练习时长（小时）', L, H - 6);
      ctx.save(); ctx.translate(14, T + 6); ctx.fillText('预测得分', 0, 0); ctx.restore();

      /* 拟合直线（裁剪在坐标区内） */
      ctx.save();
      ctx.beginPath(); ctx.rect(L - 1, T - 1, R - L + 2, Bm - T + 2); ctx.clip();
      ctx.strokeStyle = themeColor('--brand-2', '#06b6d4');
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(px(0), py(st.w * 0 + st.b));
      ctx.lineTo(px(10), py(st.w * 10 + st.b));
      ctx.stroke();
      ctx.restore();

      /* 样本点 */
      DATA.forEach(function (p) {
        ctx.beginPath();
        ctx.arc(px(p[0]), py(p[1]), 5.5, 0, Math.PI * 2);
        ctx.fillStyle = themeColor('--brand', '#3b82f6');
        ctx.fill();
      });

      ctx.font = font('700', 13);
      ctx.fillStyle = themeColor('--brand-2', '#06b6d4');
      ctx.textAlign = 'left';
      var ty = py(st.w * 10 + st.b);
      ctx.fillText('当前模型：y = ' + fixed(st.w) + ' x + ' + fixed(st.b),
        L + 8, Math.max(T + 14, Math.min(Bm - 6, ty - 10)));
    }

    function drawLoss() {
      var cv = document.getElementById('aim1-curve');
      if (!cv || !cv.getContext) return;
      var ctx = cv.getContext('2d');
      var W = cv.width, H = cv.height;
      var L = 56, R = W - 22, T = 16, Bm = H - 26;
      ctx.clearRect(0, 0, W, H);
      var hi = 7, lo = -1;
      var n = Math.max(st.ep, 40);
      function px(i) { return L + (i / n) * (R - L); }
      function py(v) {
        var g = Math.log10(Math.max(v, 1e-2));
        g = Math.max(lo, Math.min(hi, g));
        return Bm - ((g - lo) / (hi - lo)) * (Bm - T);
      }
      ctx.font = font('600', 11);
      ctx.strokeStyle = themeColor('--line', '#e2e8f0');
      for (var g = lo; g <= hi; g += 2) {
        ctx.beginPath(); ctx.moveTo(L, py(Math.pow(10, g))); ctx.lineTo(R, py(Math.pow(10, g))); ctx.stroke();
        ctx.fillStyle = themeColor('--muted', '#64748b');
        ctx.textAlign = 'right';
        ctx.fillText(g === -1 ? '0.1' : (g === 0 ? '1' : '10^' + g), L - 8, py(Math.pow(10, g)) + 4);
      }
      ctx.save();
      ctx.beginPath(); ctx.rect(L - 1, T - 1, R - L + 2, Bm - T + 2); ctx.clip();
      ctx.strokeStyle = themeColor('--brand', '#3b82f6');
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      for (var i = 0; i < st.hist.length; i++) {
        var X = px(i), Y = py(st.hist[i]);
        if (i === 0) ctx.moveTo(X, Y); else ctx.lineTo(X, Y);
      }
      ctx.stroke();
      ctx.restore();
      ctx.font = font('600', 11);
      ctx.fillStyle = themeColor('--muted', '#64748b');
      ctx.textAlign = 'left';
      ctx.fillText('横轴：训练轮次　纵轴：损失（对数刻度）', L, H - 4);
    }

    function regimeOf() {
      var last = st.hist[st.hist.length - 1];
      var prev = st.hist.length > 1 ? st.hist[st.hist.length - 2] : last;
      if (st.flying) return 'flying';
      if (st.ep >= 2 && last > prev * 1.02) return 'unstable';
      if (last <= LOSS_FLOOR * 1.12) return 'good';
      if (st.ep >= 40) return 'slow';
      return 'working';
    }

    function renderA() {
      var lr = Number(eLr.value);
      eLrV.textContent = lr.toFixed(3);
      var last = st.hist[st.hist.length - 1];
      eW.textContent = fixed(st.w);
      eB.textContent = fixed(st.b);
      eL.textContent = fixed(last, 3);
      eEp.textContent = st.ep + ' 轮';
      drawFit();
      drawLoss();

      var rg = regimeOf();
      var parts = [];
      parts.push('<strong>学习率 ' + lr.toFixed(3) + '：已完成 ' + st.ep + ' 轮训练，' +
        '当前参数 w = ' + fixed(st.w) + '、b = ' + fixed(st.b) + '，损失 ' + fixed(last, 3) + '。</strong>');
      parts.push('这批数据自身的抖动决定了一个下限：损失最低只能压到大约 ' + LOSS_FLOOR.toFixed(2) +
        '，任何模型都低不过它。训练就是在把损失往这个下限推。');

      if (rg === 'flying') {
        parts.push('<strong>判定：发散，参数跑飞了。</strong>损失不降反升而且越来越大，说明每一步都把参数推过了头，' +
          '下一步的梯度方向跟着翻过来，于是在好位置两侧越跳越远。处置很直接：把学习率往小调，重新开始。');
        eOutA.className = 'result error';
      } else if (rg === 'unstable') {
        parts.push('<strong>判定：不稳定，损失开始上下震荡。</strong>步子已经踩到了临界附近，参数在好位置两侧来回跳。' +
          '往小调一点，损失就会重新稳稳下降。');
        eOutA.className = 'result warn';
      } else if (rg === 'good') {
        parts.push('<strong>判定：已经收敛。</strong>损失压到了接近下限的位置，参数也稳定下来，' +
          '继续训练也只是在这个位置附近微小抖动。');
        eOutA.className = 'result';
      } else if (rg === 'slow') {
        parts.push('<strong>判定：步子偏小，走得慢。</strong>损失确实在下降，但 ' + st.ep +
          ' 轮之后还没到位。注意看 b：它从 0 出发，目标大约在 1.05 附近，现在还差得多——' +
          '偏置这个方向上的梯度本来就小，学习率偏小时它走得最慢，所以损失迟迟下不来。');
        eOutA.className = 'result warn';
      } else {
        parts.push('<strong>判定：正在下降。</strong>继续按训练按钮或打开连续训练，观察损失往下走的速度。');
        eOutA.className = 'result';
      }

      parts.push('<strong>易错点：</strong>常见错误是误认为「训练轮次越多，模型一定越好」。轮次只决定走多少步，' +
        '步子大小不对，多走只会更远。另一个容易搞混的是把学习率当成模型参数——' +
        '它不由训练过程自己调出来，而是训练开始前由人设定的，这类量叫做超参数。');
      eOutA.innerHTML = parts.join('<br>');
    }

    function stopAuto() {
      if (timer) { clearInterval(timer); timer = null; }
      var bt = document.getElementById('aim1-auto');
      if (bt) bt.classList.remove('selected');
    }

    document.getElementById('aim1-step1').addEventListener('click', function () {
      stopAuto(); doStep(Number(eLr.value)); renderA();
    });
    document.getElementById('aim1-step10').addEventListener('click', function () {
      stopAuto();
      for (var i = 0; i < 10; i++) doStep(Number(eLr.value));
      renderA();
    });
    document.getElementById('aim1-auto').addEventListener('click', function () {
      var bt = document.getElementById('aim1-auto');
      if (timer) { stopAuto(); return; }
      bt.classList.add('selected');
      timer = setInterval(function () {
        var lr = Number(eLr.value);
        for (var i = 0; i < 5; i++) doStep(lr);
        renderA();
        if (st.flying || st.ep > 500) stopAuto();
      }, 90);
    });
    document.getElementById('aim1-reset').addEventListener('click', function () {
      stopAuto(); reset(); renderA();
    });
    eLr.addEventListener('input', function () {
      if (st.ep > 0) { reset(); }
      renderA();
    });
    reset();
    renderA();
  }

  /* ---------- 3. 覆盖范围与外推检验台 ---------- */
  /* 真实规律（画出来只为对照，实际工作中你看不到它） */
  function truth(x) { return 1 + 0.8 * x + 0.12 * x * x; }
  var NOISE_C = [0.42, -0.31, 0.55, -0.48, 0.27, -0.36, 0.61, -0.22, 0.44, -0.57, 0.33];

  var stageB = document.getElementById('aim2-stage');
  if (stageB) {
    var eR = document.getElementById('aim2-r');
    var eRV = document.getElementById('aim2-r-val');
    var eS = document.getElementById('aim2-s');
    var eSV = document.getElementById('aim2-s-val');
    var eOutB = document.getElementById('aim2-out');

    function fitLine(pts) {
      var n = pts.length, sx = 0, sy = 0;
      pts.forEach(function (p) { sx += p[0]; sy += p[1]; });
      var mx = sx / n, my = sy / n, sxy = 0, sxx = 0;
      pts.forEach(function (p) { sxy += (p[0] - mx) * (p[1] - my); sxx += (p[0] - mx) * (p[0] - mx); });
      var w = sxx > 1e-9 ? sxy / sxx : 0;
      return [w, my - w * mx];
    }

    function drawB(R, pts, w, b) {
      var cv = document.getElementById('aim2-canvas');
      if (!cv || !cv.getContext) return;
      var ctx = cv.getContext('2d');
      var W = cv.width, H = cv.height;
      var L = 56, Rt = W - 22, T = 22, Bm = H - 34;
      ctx.clearRect(0, 0, W, H);
      var yMax = 23;
      function px(x) { return L + (x / 10) * (Rt - L); }
      function py(y) { return Bm - (y / yMax) * (Bm - T); }

      ctx.fillStyle = themeColor('--brand-soft', 'rgba(59,130,246,.10)');
      ctx.fillRect(L, T, px(R) - L, Bm - T);
      ctx.fillStyle = themeColor('--warm-soft', 'rgba(245,158,11,.14)');
      ctx.fillRect(px(R), T, Rt - px(R), Bm - T);

      ctx.strokeStyle = themeColor('--line', '#e2e8f0');
      ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(L, Bm); ctx.lineTo(Rt, Bm); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(L, T); ctx.lineTo(L, Bm); ctx.stroke();
      ctx.font = font('600', 11);
      ctx.fillStyle = themeColor('--muted', '#64748b');
      ctx.textAlign = 'center';
      for (var x = 0; x <= 10; x += 2) ctx.fillText(String(x), px(x), Bm + 17);

      /* 真实规律 */
      ctx.strokeStyle = themeColor('--muted', '#64748b');
      ctx.lineWidth = 1.6;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      for (var i = 0; i <= 50; i++) {
        var xv = 10 * i / 50, yv = truth(xv);
        if (i === 0) ctx.moveTo(px(xv), py(yv)); else ctx.lineTo(px(xv), py(yv));
      }
      ctx.stroke();
      ctx.setLineDash([]);

      /* 拟合直线 */
      ctx.save();
      ctx.beginPath(); ctx.rect(L - 1, T - 1, Rt - L + 2, Bm - T + 2); ctx.clip();
      ctx.strokeStyle = themeColor('--brand', '#3b82f6');
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(px(0), py(b));
      ctx.lineTo(px(10), py(w * 10 + b));
      ctx.stroke();
      ctx.restore();

      /* 训练样本 */
      pts.forEach(function (p) {
        ctx.beginPath();
        ctx.arc(px(p[0]), py(p[1]), 5.5, 0, Math.PI * 2);
        ctx.fillStyle = themeColor('--brand-2', '#06b6d4');
        ctx.fill();
      });

      /* 最右端预测与真实 */
      var pEnd = w * 10 + b, tEnd = truth(10);
      if (R < 10) {
        ctx.strokeStyle = themeColor('--warn', '#f59e0b');
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(px(10), py(pEnd)); ctx.lineTo(px(10), py(tEnd));
        ctx.stroke();
        ctx.beginPath(); ctx.arc(px(10), py(pEnd), 4, 0, Math.PI * 2);
        ctx.fillStyle = themeColor('--brand', '#3b82f6'); ctx.fill();
        ctx.beginPath(); ctx.arc(px(10), py(tEnd), 4, 0, Math.PI * 2);
        ctx.fillStyle = themeColor('--muted', '#64748b'); ctx.fill();
      }

      ctx.font = font('700', 12);
      ctx.textAlign = 'center';
      ctx.fillStyle = themeColor('--brand', '#3b82f6');
      ctx.fillText('模型直线', px(2.2), Math.max(T + 12, py(w * 2.2 + b) - 8));
      ctx.fillStyle = themeColor('--muted', '#64748b');
      ctx.fillText('真实规律', px(8.6), Math.max(T + 12, py(truth(8.6)) - 10));
      ctx.font = font('600', 11);
      ctx.fillStyle = themeColor('--brand', '#3b82f6');
      ctx.fillText('数据覆盖区', (L + px(R)) / 2, Bm - 8);
      if (R < 10) {
        ctx.fillStyle = themeColor('--warn-deep', '#b45309');
        ctx.fillText('未覆盖区', (px(R) + Rt) / 2, Bm - 8);
      }
    }

    function renderB() {
      var R = Number(eR.value);
      var sg = Number(eS.value);
      eRV.textContent = '0 — ' + R + ' 小时';
      eSV.textContent = sg.toFixed(1);
      var pts = [];
      for (var x = 0; x <= R; x++) pts.push([x, truth(x) + NOISE_C[x % NOISE_C.length] * sg]);
      var wb = fitLine(pts);
      var w = wb[0], b = wb[1];

      var inSum = 0, inN = 0, outSum = 0, outN = 0;
      for (var i = 0; i <= 10; i += 0.5) {
        var err = Math.abs(w * i + b - truth(i));
        if (i <= R + 1e-9) { inSum += err; inN++; }
        else { outSum += err; outN++; }
      }
      var inMae = inN ? inSum / inN : 0;
      var outMae = outN ? outSum / outN : 0;
      document.getElementById('aim2-in').textContent = inMae.toFixed(2);
      document.getElementById('aim2-out-err').textContent = outN ? outMae.toFixed(2) : '—（已铺满）';
      document.getElementById('aim2-pred').textContent = fixed(w * 10 + b);
      document.getElementById('aim2-real').textContent = truth(10).toFixed(1);
      var barIn = Math.max(2, Math.min(100, inMae / 6 * 100));
      var barOut = outN ? Math.max(2, Math.min(100, outMae / 6 * 100)) : 0;
      document.getElementById('aim2-fill-in').style.width = barIn + '%';
      document.getElementById('aim2-fill-out').style.width = barOut + '%';

      drawB(R, pts, w, b);

      var parts = [];
      parts.push('<strong>训练数据只覆盖了 0 到 ' + R + ' 小时这一段：覆盖区内平均误差 ' + inMae.toFixed(2) +
        '，区间最右端的预测是 ' + fixed(w * 10 + b) + '，而真实值是 ' + truth(10).toFixed(1) + '。</strong>');
      parts.push('注意模型的形式没有变——它始终是一条直线；变的只是它见过哪些输入。' +
        '覆盖区内它贴着数据走，覆盖区外它就沿着这条直线一直延伸下去。');

      if (R >= 10) {
        parts.push('<strong>现在的覆盖已经铺满整个使用区间：</strong>没有未覆盖区，外推的问题不再出现。' +
          '但覆盖区内仍然留有 ' + inMae.toFixed(2) + ' 的误差——真实规律是弯的，一条直线拟合不了它，' +
          '这已经不是数据的问题，而是模型太简单了（下一张综合任务页会专门看这件事）。');
        eOutB.className = 'result warn';
      } else if (outMae > 2 * Math.max(inMae, 0.05)) {
        parts.push('<strong>判定：覆盖不足，外推不可信。</strong>区外误差 ' + outMae.toFixed(2) +
          ' 已经是区内误差 ' + inMae.toFixed(2) + ' 的两倍以上。模型在没见过的输入上并没有「推理」，' +
          '它只是把自己在覆盖区里学的直线延长出去而已。');
        parts.push('要改的不是调参，而是补数据：把训练样本铺到真正要用的输入范围上。');
        eOutB.className = 'result error';
      } else {
        parts.push('<strong>判定：区外误差还不算离谱，但差距已经出现。</strong>区外误差 ' + outMae.toFixed(2) +
          ' 对区内误差 ' + inMae.toFixed(2) + '。继续把覆盖范围缩小，看这个差距怎么拉开。');
        eOutB.className = 'result warn';
      }

      parts.push('<strong>易错点：</strong>常见错误是误认为「模型能预测任何输入」。模型只对它见过的输入分布负责，' +
        '数据没覆盖的区间里，它的输出只是这条直线的延续，没有依据。另一个容易搞混的是把噪声当成规律：' +
        '把抖动调大，覆盖区内的误差会明显上升，参数也被带着跑——真实数据本来就带噪声，' +
        '所以任何模型都不可能把误差压到零。');
      eOutB.innerHTML = parts.join('<br>');
    }
    eR.addEventListener('input', renderB);
    eS.addEventListener('input', renderB);
    renderB();
  }

  /* ---------- 4. 模型体检台 ---------- */
  /* 模型是一段多项式：阶数决定它能弯到什么程度。训练用最小二乘解正规方程，
     评价分两处：训练数据上的误差，和一批没参与训练的新数据上的误差。 */
  function truthS(x) { return 1 + 0.8 * x + 0.12 * x * x; }
  var NOISE_T = [0.42, -0.31, 0.55, -0.48, 0.27, -0.36, 0.61, -0.22, 0.44, -0.57, 0.33, -0.41,
                 0.52, -0.29, 0.38, -0.46, 0.49, -0.35, 0.58, -0.26, 0.31, -0.51, 0.47, -0.33];
  var NOISE_E = [0.51, -0.44, 0.36, -0.58, 0.29, -0.39, 0.47, -0.52, 0.33, -0.42, 0.56, -0.28,
                 0.41, -0.49, 0.31, -0.37, 0.53, -0.45, 0.39, -0.55, 0.34, -0.5, 0.43, -0.38];
  var TEST_X = [];
  for (var ti = 0; ti < 24; ti++) TEST_X.push(10 * (ti + 0.5) / 24);

  var stageC = document.getElementById('aim3-stage');
  if (stageC) {
    var eD = document.getElementById('aim3-d');
    var eN = document.getElementById('aim3-n');
    var eDV = document.getElementById('aim3-d-val');
    var eNV = document.getElementById('aim3-n-val');
    var eOutC = document.getElementById('aim3-out');

    /* 切比雪夫基：各列的数值范围相当，正规方程不会因为高阶项太小而失真 */
    function basis(x, d) {
      var z = 2 * (x / 10 - 0.5);
      var r = [1];
      if (d >= 1) r.push(z);
      for (var p = 2; p <= d; p++) r.push(2 * z * r[p - 1] - r[p - 2]);
      return r;
    }
    function solve(P, A, bb) {
      var M = [], i, j, c, cc;
      for (i = 0; i < P; i++) M.push(A[i].slice().concat([bb[i]]));
      for (c = 0; c < P; c++) {
        var p = c;
        for (i = c + 1; i < P; i++) if (Math.abs(M[i][c]) > Math.abs(M[p][c])) p = i;
        var tmp = M[c]; M[c] = M[p]; M[p] = tmp;
        if (Math.abs(M[c][c]) < 1e-14) continue;
        for (i = 0; i < P; i++) {
          if (i === c) continue;
          var f = M[i][c] / M[c][c];
          if (f === 0) continue;
          for (cc = c; cc <= P; cc++) M[i][cc] -= f * M[c][cc];
        }
      }
      /* 行置换后每行只保留一个非零，按列把解还原到对应的未知量上 */
      var th = [], i2;
      for (i2 = 0; i2 < P; i2++) th.push(0);
      for (i2 = 0; i2 < P; i2++) {
        var best = 0;
        for (j = 1; j < P; j++) if (Math.abs(M[i2][j]) > Math.abs(M[i2][best])) best = j;
        th[best] = Math.abs(M[i2][best]) > 1e-14 ? M[i2][P] / M[i2][best] : 0;
      }
      return th;
    }

    function evalC() {
      var dWant = Number(eD.value);
      var n = Number(eN.value);
      var d = Math.min(dWant, n - 1);
      var P = d + 1, i, j;

      var xs = [], ys = [];
      for (i = 0; i < n; i++) {
        var xv = 10 * i / (n - 1);
        xs.push(xv); ys.push(truthS(xv) + NOISE_T[i % NOISE_T.length] * 0.6);
      }
      var A = [], bb = [];
      for (i = 0; i < P; i++) { A.push([]); for (j = 0; j < P; j++) A[i].push(0); bb.push(0); }
      for (i = 0; i < n; i++) {
        var r = basis(xs[i], d);
        for (var a = 0; a < P; a++) {
          bb[a] += r[a] * ys[i];
          for (var bq = 0; bq < P; bq++) A[a][bq] += r[a] * r[bq];
        }
      }
      for (i = 0; i < P; i++) A[i][i] += 1e-10;
      var th = solve(P, A, bb);

      function pred(x) {
        var row = basis(x, d), s = 0;
        for (var p = 0; p < P; p++) s += th[p] * row[p];
        return s;
      }
      var s = 0;
      for (i = 0; i < n; i++) { var dd = pred(xs[i]) - ys[i]; s += dd * dd; }
      var rmseTr = Math.sqrt(s / n);
      var s2 = 0;
      for (i = 0; i < TEST_X.length; i++) {
        var dy = truthS(TEST_X[i]) + NOISE_E[i % NOISE_E.length] * 0.6;
        var d2 = pred(TEST_X[i]) - dy; s2 += d2 * d2;
      }
      var rmseTe = Math.sqrt(s2 / TEST_X.length);

      eDV.textContent = 'd = ' + d;
      eNV.textContent = n + ' 条';
      document.getElementById('aim3-rmse-tr').textContent = rmseTr.toFixed(2);
      document.getElementById('aim3-rmse-te').textContent = rmseTe.toFixed(2);
      document.getElementById('aim3-params').textContent = P + ' 个';
      document.getElementById('aim3-gap').textContent =
        (rmseTr > 0.02 ? (rmseTe / rmseTr).toFixed(1) + ' 倍' : '极大');
      document.getElementById('aim3-fill-tr').style.width = Math.max(2, Math.min(100, rmseTr / 3 * 100)) + '%';
      document.getElementById('aim3-fill-te').style.width = Math.max(2, Math.min(100, rmseTe / 3 * 100)) + '%';

      var verdict, cls;
      if (rmseTr >= 0.75) { verdict = '欠拟合'; cls = 'error'; }
      else if (rmseTe >= 2.0 * rmseTr) { verdict = '过拟合'; cls = 'warn'; }
      else { verdict = '合适'; cls = ''; }

      drawC(d, pred, xs, ys);

      var parts = [];
      parts.push('<strong>当前设置：模型阶数 ' + d + '（参数 ' + P + ' 个），训练数据 ' + n +
        ' 条。训练误差 ' + rmseTr.toFixed(2) + '，测试误差 ' + rmseTe.toFixed(2) + '，判定为' + verdict + '。</strong>');
      parts.push('这里有两条误差要分清。训练误差是模型在自己见过的数据上的表现；' +
        '测试误差是同一组参数在一批没参与训练的新数据上的表现，这批新数据叫测试集。' +
        '只有测试误差才反映它对新情况的能力。');

      if (verdict === '欠拟合') {
        parts.push('<strong>病因：模型太简单，容量不够。</strong>训练误差本身就高，说明它连见过的数据都拟合不好，' +
          '根本没有能力表达这批数据的弯度。处置：把阶数调高，让它能表达更细的形状。');
      } else if (verdict === '过拟合') {
        parts.push('<strong>病因：模型太灵活、数据太少，把噪声当规律记住了。</strong>' +
          (rmseTr < 0.02
            ? '训练误差已经接近零——模型几乎穿过了每一个训练点，连它们身上的随机抖动都当成规律记住了。'
            : '训练误差很小，但它记住的是每条记录上那点随机抖动；') +
          '换到新数据上这些抖动一点都不管用，测试误差于是成倍放大。处置：降低阶数，或者增加训练数据。');
      } else {
        parts.push('<strong>当前是一组比较均衡的设置：</strong>训练误差和测试误差接近，' +
          '而且都不高，说明模型的容量和数据的量大致配得上，学到的是规律而不是抖动。');
      }

      if (dWant > n - 1) {
        parts.push('<strong>注意：</strong>你把阶数调到了 ' + dWant + '，但训练数据只有 ' + n +
          ' 条，最高的可用阶数只有 ' + (n - 1) + ' 阶。参数数量不能超过数据能支撑的量——' +
          '这是过拟合最极端的来源。');
      }
      parts.push('<strong>易错点：</strong>常见错误是误认为「训练误差小就说明模型好」。' +
        '只看训练误差，你会一路把阶数加大、误差一路变小，最后得到一个只对训练数据有效的模型。' +
        '另一个容易搞混的是把两条误差当成一回事：它们量的是两种能力，一个是记忆，一个是泛化。');
      eOutC.className = 'result ' + cls;
      eOutC.innerHTML = parts.join('<br>');
    }

    function drawC(d, pred, xs, ys) {
      var cv = document.getElementById('aim3-canvas');
      if (!cv || !cv.getContext) return;
      var ctx = cv.getContext('2d');
      var W = cv.width, H = cv.height;
      var L = 50, R = W - 20, T = 18, Bm = H - 30;
      ctx.clearRect(0, 0, W, H);
      var yMax = 23, yMin = -2;
      function px(x) { return L + (x / 10) * (R - L); }
      function py(y) { return Bm - ((y - yMin) / (yMax - yMin)) * (Bm - T); }
      ctx.strokeStyle = themeColor('--line', '#e2e8f0');
      ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(L, Bm); ctx.lineTo(R, Bm); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(L, py(0)); ctx.lineTo(R, py(0)); ctx.stroke();
      ctx.font = font('600', 11);
      ctx.fillStyle = themeColor('--muted', '#64748b');
      ctx.textAlign = 'center';
      for (var x = 0; x <= 10; x += 2) ctx.fillText(String(x), px(x), Bm + 16);

      /* 测试集（空心点） */
      TEST_X.forEach(function (x, i) {
        var y = truthS(x) + NOISE_E[i % NOISE_E.length] * 0.6;
        ctx.beginPath();
        ctx.arc(px(x), py(y), 3.6, 0, Math.PI * 2);
        ctx.strokeStyle = themeColor('--muted', '#64748b');
        ctx.lineWidth = 1.6;
        ctx.stroke();
      });

      /* 模型曲线（裁剪在坐标区内，避免高阶模型冲出画面） */
      ctx.save();
      ctx.beginPath(); ctx.rect(L - 1, T - 1, R - L + 2, Bm - T + 2); ctx.clip();
      ctx.strokeStyle = themeColor('--brand', '#3b82f6');
      ctx.lineWidth = 3;
      ctx.beginPath();
      for (var i = 0; i <= 240; i++) {
        var xv = 10 * i / 240, yv = pred(xv);
        if (i === 0) ctx.moveTo(px(xv), py(yv)); else ctx.lineTo(px(xv), py(yv));
      }
      ctx.stroke();
      ctx.restore();

      /* 训练点 */
      xs.forEach(function (x, i) {
        ctx.beginPath();
        ctx.arc(px(x), py(ys[i]), 4.2, 0, Math.PI * 2);
        ctx.fillStyle = themeColor('--brand-2', '#06b6d4');
        ctx.fill();
      });

      ctx.font = font('600', 11);
      ctx.textAlign = 'left';
      ctx.fillStyle = themeColor('--muted', '#64748b');
      ctx.fillText('实心＝训练数据　空心＝没参与训练的新数据　阶数 d = ' + d, L, H - 4);
    }

    eD.addEventListener('input', evalC);
    eN.addEventListener('input', evalC);
    evalC();
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：模型里的参数到底是谁在调？", TTS["pretest"], [
        {"q": "训练一个模型时，参数（权重和偏置）是怎么定下来的？",
         "options": [("由一套固定的流程反复迭代、用数据把它逐步调到合适的位置", True),
                     ("由人一个一个试出来，试到满意为止", False),
                     ("程序启动时就随机生成好了，之后不再改变", False)],
         "explain": "训练是一套固定流程：预测、算损失、算梯度、更新参数，重复进行。<strong>错因提醒：</strong>常见错误是误认为「人得靠感觉去调参数」——人设定的是学习率这类超参数，参数本身是流程自己调出来的。"},
        {"q": "学习率这个量在训练中的作用是：",
         "options": [("决定每一次更新把参数挪多大的一步", True),
                     ("决定一共训练多少轮", False),
                     ("决定模型用多少条训练数据", False)],
         "explain": "学习率乘在梯度上，控制步长；轮次控制走多少步，两者是两件事。<strong>错因提醒：</strong>容易搞混的是把学习率和训练轮次当成一个东西——步子大小和步数要分开调。"},
        {"q": "某模型在训练数据上损失已经降到很低，但换一批新数据误差很大。最合理的判断是：",
         "options": [("它可能把训练数据里的随机抖动也当成规律记住了，属于过拟合", True),
                     ("它一定是一个好模型，只是新数据有问题", False),
                     ("继续加大训练轮次就能解决", False)],
         "explain": "训练误差小、测试误差大，是过拟合的典型表现。<strong>错因提醒：</strong>许多同学误认为「训练损失越低越好」——继续训练只会把噪声记得更牢。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "模型是带参数的函数，训练就是把它调到合适的位置", TTS["module-1"], f'''
        <div class="inner-card">
          <p><strong>为什么要学这一课？</strong>你已经见过不少会「认图」「会预测」的应用，也知道了它们的规则是从数据里学出来的。但「从数据里学」这句话太笼统了，<strong>所以</strong>我们要把它拆到可以看见的量：参数、损失、梯度、学习率。</p>
        </div>
        <p style="font-size:17px;margin:12px 0">在这节课里，模型就是一个<strong>带参数的函数</strong>：<code>y = w × x + b</code>。w 叫<strong>权重</strong>，b 叫<strong>偏置</strong>，合起来叫<strong>参数</strong>。训练不是人去猜参数，而是用固定的四步循环，把参数逐步调到损失最小的位置。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>预测：</strong>用当前的 w 和 b 对每条样本算出一个输出。</div></div>
          <div class="step"><span class="n">2</span><div><strong>算损失：</strong>把预测和真实答案的差距汇总成一个数。这里用均方误差：各个样本误差的平方再取平均。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>算梯度：</strong>求出损失对 w 和对 b 的梯度，它告诉我们往哪个方向调能让损失下降。</div></div>
          <div class="step"><span class="n">4</span><div><strong>更新参数：</strong>沿着梯度的<strong>反方向</strong>挪一小步，步长由学习率（记作 η）决定。</div></div>
        </div>
        <div class="ta-code" style="margin:14px 0">w ← 0，b ← 0
重复 N 轮：
    预测 ŷ = w × x + b
    损失 L = 平均((ŷ − y)²)
    梯度 gw = 平均(2 × x × (ŷ − y))
    梯度 gb = 平均(2 × (ŷ − y))
    更新 w ← w − η × gw
    更新 b ← b − η × gb
返回 w，b</div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="训练循环四步示意图：预测、计算损失、计算梯度、更新参数，循环往复直到损失下降到位">
          <figcaption>训练循环的四步：预测 → 算损失 → 算梯度 → 更新参数，重复进行，直到损失不再下降</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🧭</span><div><strong>记忆锚点：</strong>把训练想成下山。损失是当前的海拔，梯度是指出「哪个方向最陡」的罗盘，学习率是你的步长。罗盘只指方向，走多远由步长决定——步子迈太大的后果，下一张实验页你会亲眼看到。</div></div>
{insight_box([
    {"lens": "看见它", "text": "四步循环里没有任何一步需要人来做判断，全部是可以写成公式、交给程序重复执行的机械动作。这正是它能自动化的原因。"},
    {"lens": "拆开它", "text": "训练结束后真正留下来的东西只有 w 和 b 这两个数。所谓「模型」，在部署时往往就是这几个参数加上固定的计算结构。"},
    {"lens": "迁移它", "text": "「先量出差距，再朝着差距变小的方向调整」这个思路，也是人练技能时的常见路径：反馈越准，调整越有效。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "梯度下降训练台：学习率调大调小，后果完全不同", TTS["lab-1"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">拖动学习率，按「训练 10 轮」或打开连续训练，盯住 w、b、损失这三个数怎么变。损失曲线用对数刻度，否则前几轮的大数值会把后面全压平。</p>
        <div class="lab-panel">
          <div class="ta-stage" id="aim1-stage">
            <div class="slider-row">
              <label for="aim1-lr">学习率 η</label>
              <input type="range" id="aim1-lr" min="0.005" max="0.08" step="0.005" value="0.02">
              <span class="readout-cell" style="flex:0 0 108px"><span class="k">步长</span><span class="v" id="aim1-lr-val">0.020</span></span>
            </div>
            <div class="ta-btns">
              <button class="choice" id="aim1-step1">训练 1 轮</button>
              <button class="choice" id="aim1-step10">训练 10 轮</button>
              <button class="choice" id="aim1-auto">连续训练</button>
              <button class="choice" id="aim1-reset">重置</button>
            </div>
          </div>
          <canvas id="aim1-fit" width="680" height="250" aria-label="样本点与当前拟合直线" style="display:block;width:100%;margin-top:12px;border-radius:12px;background:var(--card);"></canvas>
          <canvas id="aim1-curve" width="680" height="170" aria-label="损失随训练轮次变化曲线" style="display:block;width:100%;margin-top:10px;border-radius:12px;background:var(--card);"></canvas>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">权重 w</span><span class="v" id="aim1-w">—</span></div>
            <div class="readout-cell"><span class="k">偏置 b</span><span class="v" id="aim1-b">—</span></div>
            <div class="readout-cell"><span class="k">当前损失</span><span class="v green" id="aim1-loss">—</span></div>
            <div class="readout-cell"><span class="k">已训练</span><span class="v" id="aim1-ep">—</span></div>
          </div>
          <p class="result warn" id="aim1-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">⚙️</span><div><strong>动手找一找：</strong>先用 0.02 训练 10 轮，记下损失；重置后换成 0.05 再训练 10 轮，看损失是往下走还是往上窜。同一个程序、同一批数据，只改了学习率这一个数，结果完全不同。</div></div>
    ''', tag="动手实验室", bloom="apply"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "数据决定模型的上限：没见过的输入，它只是在猜", TTS["module-2"], f'''
        <div class="inner-card">
          <p><strong>参数调好了，是不是就万事大吉？</strong>不是。参数的每一个取值都是从训练数据里推出来的，<strong>所以</strong>数据本身有三个绕不开的限制。</p>
        </div>
        <div class="grid grid-3">
          <div class="inner-card">
            <p><strong>覆盖范围</strong></p>
            <p style="color:var(--muted)">只见过 0 到 4 小时的记录，对 10 小时的情形只能外推，没有依据。</p>
          </div>
          <div class="inner-card">
            <p><strong>数据量</strong></p>
            <p style="color:var(--muted)">样本太少，参数会被个别样本带着跑，换一批数据结果就变。</p>
          </div>
          <div class="inner-card">
            <p><strong>数据质量</strong></p>
            <p style="color:var(--muted)">一条录错的记录会把参数和损失一起带偏，而且不会报错。</p>
          </div>
        </div>
        <p style="font-size:17px;margin:12px 0">还有一条最容易忽略：<strong>训练损失小不等于模型好</strong>。模型可能只是把每条训练样本上那点随机抖动也记住了（这叫<strong>过拟合</strong>）。要判断它有没有真的学到规律，必须留出一批<strong>没参与训练</strong>的新数据来测——这种做法叫<strong>留出法</strong>，在留出数据上算出的误差叫<strong>测试误差</strong>。</p>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="数据覆盖范围与外推误差示意图：左侧为数据覆盖区，模型贴合良好；右侧为未覆盖区，模型直线偏离真实规律">
          <figcaption>覆盖区内模型贴着数据走；覆盖区外模型只是把这条直线延长出去，误差越拉越大</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">最容易踩的是<strong>把训练误差当成模型的能力</strong>：损失一路下降就以为模型在变好，其实它可能正在把噪声背下来。第二个常见错误是<strong>误认为模型能预测任何输入</strong>——输入落在训练数据没覆盖的区间里，它的输出只是一条外推的直线。第三个是<strong>把噪声当成规律</strong>：真实数据天生带抖动，因此任何模型都不可能把损失压到零，那个下限由数据自身的抖动决定。</p>
        </div>
{insight_box([
    {"lens": "比较它", "text": "「参数是调出来的」和「上限是数据给的」这两件事要分开看：调参决定你能不能走到上限，数据决定上限在哪里。"},
    {"lens": "迁移它", "text": "用没参与训练的数据检验结果，和「练习时见过的题不算检验，要看新题」是同一个道理。"},
])}
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "覆盖范围与外推检验台：数据铺到哪里，模型才管到哪里", TTS["lab-2"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">拖动覆盖范围与数据抖动，盯住三个数字：覆盖区内误差、覆盖区外误差、区间最右端的预测值与真实值。</p>
        <div class="lab-panel">
          <div class="ta-stage" id="aim2-stage">
            <div class="slider-row">
              <label for="aim2-r">训练数据覆盖到</label>
              <input type="range" id="aim2-r" min="2" max="10" step="1" value="4">
              <span class="readout-cell" style="flex:0 0 130px"><span class="k">覆盖区间</span><span class="v" id="aim2-r-val">0 — 4 小时</span></span>
            </div>
            <div class="slider-row">
              <label for="aim2-s">数据抖动大小</label>
              <input type="range" id="aim2-s" min="0" max="2.5" step="0.5" value="0.5">
              <span class="readout-cell" style="flex:0 0 130px"><span class="k">抖动</span><span class="v" id="aim2-s-val">0.5</span></span>
            </div>
          </div>
          <canvas id="aim2-canvas" width="680" height="260" aria-label="训练数据覆盖范围与外推误差示意图" style="display:block;width:100%;margin-top:12px;border-radius:12px;background:var(--card);"></canvas>
          <div class="ta-meter"><span class="lbl">覆盖区内误差</span><span class="bar"><span class="fill" id="aim2-fill-in"></span></span><span class="val" id="aim2-in">—</span></div>
          <div class="ta-meter"><span class="lbl">覆盖区外误差</span><span class="bar"><span class="fill" id="aim2-fill-out"></span></span><span class="val" id="aim2-out-err">—</span></div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">最右端：模型预测</span><span class="v" id="aim2-pred">—</span></div>
            <div class="readout-cell"><span class="k">最右端：真实值</span><span class="v green" id="aim2-real">—</span></div>
          </div>
          <div class="ta-legend">
            <span><span class="dot" style="background:var(--brand-2)"></span>训练样本（模型见过的输入）</span>
            <span><span class="dot" style="background:var(--brand)"></span>模型拟合出的直线</span>
            <span><span class="dot" style="background:var(--muted)"></span>真实规律（实际工作中你看不到它，这里画出来只为对照）</span>
          </div>
          <p class="result" id="aim2-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🗺️</span><div><strong>试出边界：</strong>先把覆盖范围停在 4，记下区外误差；再拖到 10，看区外误差变成「已铺满」。然后把抖动拉到 2.5，注意区内误差也跟着涨——噪声是模型压不掉的那部分。</div></div>
    ''', tag="动手实验室", bloom="analyze"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：学习率调大了，损失为什么反而越来越大？", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:var(--warm)">
          <p style="margin:0"><strong>题目：</strong>某同学把学习率从 0.02 调到 0.05，训练 10 轮后损失从 163 变成了一千多，而且每一轮都比上一轮大。请分析原因并给出处置办法。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看清更新公式：</strong>参数的新值等于旧值减去「学习率 × 梯度」。梯度只负责指方向，走多远完全由学习率决定。</div></div>
          <div class="step"><span class="n">2</span><div><strong>算一步走了多远：</strong>初始 w = 0、b = 0，这批数据的梯度大小约为 151。学习率 0.02 时一步把 w 推到 3.02，已经越过了最优点；学习率 0.05 时一步推到 7.56，越过头太多了。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>看误差为什么会放大：</strong>越过最优点之后，梯度的方向会翻过来。如果步子还是那么大，参数就会在最优位置两侧越跳越远，损失一轮比一轮大——这就是<strong>发散</strong>。</div></div>
          <div class="step"><span class="n">4</span><div><strong>给出处置：</strong>损失不降反升、而且持续变大，说明学习率过大，应该往小调，然后重新开始训练；反过来，训练很多轮损失还在缓慢下降，那是步子偏小，可以适当调大。顺序永远是：先让损失稳稳下降，再追求更快。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">很多同学误认为<strong>「损失变大了，说明数据有问题或者代码写错了」</strong>，于是回头改数据、改结构。可这个现象有明确的成因，就在学习率这一个数上。另一处容易搞混的是<strong>把震荡和发散当成一回事</strong>：震荡是损失上下跳但总体还在低位，发散是损失持续变大、参数被推得越来越远——前者调小一点就能稳，后者必须停下来重训。</p>
        </div>
    ''', tag="例题示范", bloom="evaluate"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "下面哪句话是正确的？",
         "options": [("学习率是训练开始前由人设定的超参数，不由训练过程自己调出来", True),
                     ("参数是训练开始前由人设定的，学习率是训练过程调出来的", False),
                     ("参数和学习率都由训练过程自动调出来", False)],
         "explain": "参数（w、b）由训练循环调出来，学习率、轮次这些训练前设定、训练中不变的量叫超参数。<strong>错因提醒：</strong>常见错误是误认为「参数就是要靠人试出来的」——那正是训练循环要替你做的事。"},
        {"q": "训练时损失在最近几轮一会儿降一会儿升，位置都在低位附近。最合理的处置是：",
         "options": [("把学习率往小调一点，让更新稳定下来", True),
                     ("把学习率再调大，加快下降速度", False),
                     ("增加训练轮次，多训练几百轮", False)],
         "explain": "低位附近的上下跳动说明步子踩到了临界，缩小步长就能稳。<strong>错因提醒：</strong>容易搞混的是把震荡当发散——震荡总体还在低位，调小学习率即可，不必推倒重来。"},
        {"q": "两个模型在同一批训练数据上训练，A 的训练误差 0.25，B 的训练误差 0.95。下面哪个判断最站得住脚？",
         "options": [("还不能判断谁好，要看它们在一批没参与训练的新数据上的测试误差", True),
                     ("A 一定比 B 好，训练误差小说明模型更准", False),
                     ("B 一定比 A 好，误差大说明它更接近真实规律", False)],
         "explain": "训练误差小可能只是记住了训练数据里的抖动，必须用留出的新数据来测。<strong>错因提醒：</strong>许多同学误认为「一个训练误差就能代表模型好坏」——记忆和泛化是两种能力，要分开量。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：当一次模型体检员，分清欠拟合和过拟合", TTS["synthesis"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">拖动模型阶数和训练数据量，每一组设置都会重新拟合一次参数，并在训练数据和一批没参与训练的新数据上分别测误差。</p>
        <div class="lab-panel">
          <div class="ta-stage" id="aim3-stage">
            <div class="slider-row">
              <label for="aim3-d">模型阶数（多项式次数）</label>
              <input type="range" id="aim3-d" min="1" max="12" step="1" value="1">
              <span class="readout-cell" style="flex:0 0 118px"><span class="k">阶数</span><span class="v" id="aim3-d-val">d = 1</span></span>
            </div>
            <div class="slider-row">
              <label for="aim3-n">训练数据量</label>
              <input type="range" id="aim3-n" min="8" max="120" step="4" value="24">
              <span class="readout-cell" style="flex:0 0 110px"><span class="k">样本</span><span class="v" id="aim3-n-val">24 条</span></span>
            </div>
          </div>
          <canvas id="aim3-canvas" width="680" height="250" aria-label="模型拟合曲线与训练点、测试点对比图" style="display:block;width:100%;margin-top:12px;border-radius:12px;background:var(--card);"></canvas>
          <div class="ta-meter"><span class="lbl">训练误差</span><span class="bar"><span class="fill" id="aim3-fill-tr"></span></span><span class="val" id="aim3-rmse-tr">—</span></div>
          <div class="ta-meter"><span class="lbl">测试误差</span><span class="bar"><span class="fill" id="aim3-fill-te"></span></span><span class="val" id="aim3-rmse-te">—</span></div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">实际参数个数</span><span class="v" id="aim3-params">—</span></div>
            <div class="readout-cell"><span class="k">测试误差 ÷ 训练误差</span><span class="v green" id="aim3-gap">—</span></div>
          </div>
          <div class="ta-legend">
            <span><span class="dot" style="background:var(--brand-2)"></span>实心点：参与训练的数据</span>
            <span><span class="dot" style="background:var(--muted)"></span>空心点：没参与训练的新数据</span>
          </div>
          <p class="result" id="aim3-out" style="margin-top:12px"></p>
        </div>
        <div class="inner-card">
          <p><strong>写下来，说给同桌听：</strong>为什么「训练误差很小」不能说明模型好？请用「记忆」和「泛化」这两个词把你的理由说完整。</p>
          <textarea id="syn-answer" rows="3" placeholder="因为训练误差量的是模型对它见过的数据的表现，它完全可以把每条记录上的随机抖动也记住，这时训练误差会很小，但换到没参与训练的新数据上……"></textarea>
        </div>
    ''', tag="综合任务", bloom="evaluate"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换一个情境，看看规律还在不在", TTS["posttest"], [
        {"q": "某小组的模型在训练数据上损失降到了 0.4，在一批新数据上却是 3.2。下一步最该做的是：",
         "options": [("减少模型复杂度或增加训练数据，让两条误差的差距收窄", True),
                     ("把学习率调大，让损失继续往下走", False),
                     ("继续增加训练轮次，把 0.4 压得更低", False)],
         "explain": "训练误差低而测试误差高出好几倍，是过拟合的信号，处置方向是降低复杂度或补数据。<strong>错因提醒：</strong>常见错误是误认为「再训练久一点就好」——继续训练只会把训练数据里的抖动记得更牢。"},
        {"q": "一个用「每周练习时长」预测得分的模型，训练数据全部来自每天练习超过 3 小时的同学。用它去预测每天只练习 20 分钟的同学，最可能出现的情况是：",
         "options": [("预测不可靠，因为这个输入区间在训练数据里几乎没有出现过", True),
                     ("预测会更准，因为练习少的同学情况更简单", False),
                     ("只要模型参数调得足够好，任何输入都能预测准确", False)],
         "explain": "模型只对它见过的输入分布负责，训练数据没有覆盖的区间只能外推。<strong>错因提醒：</strong>许多同学误认为「模型能预测任何输入」——外推的结论没有数据支撑，不能直接拿来用。"},
        {"q": "训练时你把学习率调得很大，损失从 160 涨到 900，又涨到 5000。最恰当的处置是：",
         "options": [("判定为发散，把学习率调小后重新训练", True),
                     ("把训练轮次减少一些，让它停在涨上去之前", False),
                     ("换一批训练数据，当前这批数据可能有错", False)],
         "explain": "损失持续变大、参数被越推越远就是发散，根因在步长。<strong>错因提醒：</strong>容易搞混的是把发散当成数据问题——先看学习率这个超参数，再谈数据。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把自己讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>模型是带参数的函数</strong>：w 是权重、b 是偏置；训练就是一套固定流程把参数调到损失最小的位置。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>四步循环</strong>：预测 → 算损失 → 算梯度 → 更新参数，重复进行；学习率决定每一步挪多大。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>学习率有三种后果</strong>：太小走得慢、太大震荡甚至发散跑飞，适中才又快又稳。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>数据决定上限</strong>：没覆盖的输入只能外推；判断好坏要用测试误差，两条误差一对比就分得清欠拟合和过拟合。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:var(--warm)">
          <p style="margin:0"><strong>回到开头那个小组：</strong>他们的模型并没有坏。真正的问题是训练数据只覆盖了自己班的情况，而他们又只看了训练损失这一个数字。把样本铺到真正要用的范围上、留出一批新数据来测测试误差，同一个模型就能派上用场。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「参数、损失、学习率、测试误差」这四个词，把一次完整的训练过程讲清楚，并说明哪一步最容易出问题。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "写出训练循环的四步伪代码，并说明损失、梯度、学习率各起什么作用。",
            "说明学习率过小、适中、过大三种情况下的损失变化特征。",
            "说明训练误差和测试误差分别量的是模型的什么能力。",
        ],
        [
            "设计一次训练实验：数据固定、只改变学习率，记录每一次最终的损失值，画成表格并给出三档结论。",
            "某模型训练误差 0.3、测试误差 2.1。写出你的判断、依据，以及两条可行的改进办法。",
        ],
        [
            "为一个真实需求设计训练方案：说明训练数据要覆盖哪些情形、用哪一批新数据做测试、两个误差差多少你会判定为过拟合。",
            "举一个「数据没覆盖到」的真实场景，说明外推的结论会带来什么样的后果，并提出一条避免它的做法。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-m-ai-modeling",
    "node_id": "it-m-ai-modeling",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "middle",
    "stage_cn": "初中",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 初中",
    "title": "简单 AI 模型体验",
    "name_en": "Hands-on with a Simple AI Model",
    "grade": 9,
    "grade_cn": "九年级",
    "domain": "ai-society",
    "domain_cn": "人工智能与智慧社会",
    "lesson_type": "concept-practice",
    "version": "1.0.0",
    "description": "从一个「在自己班很准、换一个班就失灵」的预测模型出发，把模型拆成参数、损失、梯度、学习率四个可观察的量；亲手完成梯度下降训练，看清学习率过小、适中、过大的三种后果；再用覆盖范围与外推检验台理解数据为什么决定模型的上限，最后用训练误差与测试误差判断欠拟合、合适与过拟合。",
    "tags": ["人工智能模型", "参数与超参数", "损失函数", "梯度下降", "学习率", "欠拟合", "过拟合", "训练集与测试集", "模型评价"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》初中「人工智能与智慧社会」——体验训练或调用简单 AI 模型，理解数据与模型的关系。",
    "hero_question": "同一个模型，在自己班很准，换一个班就失灵——是哪一环没到位？",
    "hero_alt": "简单 AI 模型体验知识结构图：模型是带参数的函数、训练循环的四步、数据决定模型上限三栏",
    "hero_caption": "模型＝带参数的函数 · 训练＝四步循环调参数 · 数据决定模型上限 · 好坏要看测试误差",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的实验都会围着它转。",
    "anchor_choices": [
        {"t": "模型里的参数是谁调出来的？", "d": "预测、算损失、算梯度、更新参数", "v": "模型里的参数是谁调出来的"},
        {"t": "学习率为什么调大调小都不行？", "d": "步子大小的三种后果", "v": "学习率为什么调大调小都不行"},
        {"t": "训练损失已经很小了，为什么还是不能用？", "d": "记忆和泛化是两种能力", "v": "训练损失已经很小了，为什么还是不能用"},
        {"t": "数据没覆盖到的地方，模型凭什么给答案？", "d": "外推没有依据", "v": "数据没覆盖到的地方，模型凭什么给答案"},
    ],
    "objectives": [
        "能说出模型是一个带参数的函数，训练就是用固定流程把参数自动调到合适的位置",
        "能写出训练循环四步的伪代码：预测、算损失、算梯度、更新参数",
        "能通过实验说明学习率过小、适中、过大的三种后果，并给出调参方向",
        "能用训练误差与测试误差判断欠拟合、合适与过拟合，并说清数据覆盖范围对模型的影响",
    ],
    "objectives_plain": [
        "能说出模型是一个带参数的函数，训练就是用固定流程把参数自动调到合适的位置",
        "能写出训练循环四步的伪代码：预测、算损失、算梯度、更新参数",
        "能通过实验说明学习率过小、适中、过大的三种后果，并给出调参方向",
        "能用训练误差与测试误差判断欠拟合、合适与过拟合，并说清数据覆盖范围对模型的影响",
    ],
    "standards": [
        {"content": "体验训练或调用简单 AI 模型，理解数据与模型的关系。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》人工智能与智慧社会 · 初中"},
        {"content": "在真实情境中认识数据与模型的关系，理解数据质量、数量与覆盖范围对结果的影响，负责任地使用智能技术。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》数据与编码 / 信息社会责任 · 初中"},
    ],
    "prereqs": ["it-m-ai-applications"],
    "prereqs_name": "人工智能典型应用",
    "prereqs_meta": "it-m-ai-applications",
    "leads_to": ["it-m-digital-citizenship"],
    "next_meta": "it-m-digital-citizenship",
    "section_images": ["assets/it-m-ai-modeling-fig1.webp", "assets/it-m-ai-modeling-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "一个「在自己班很准、换一个班就失灵」的模型，问题往往在数据和评价方式上。带着它开始。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能亲手把一个模型的参数调出来，也能看出它为什么不行。",
        "objectives": "看清四件事：模型是什么、训练的四步循环、学习率的三种后果、用测试误差判好坏。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "四步循环：预测 → 算损失 → 算梯度 → 更新参数。人只设学习率，参数由流程调。",
        "lab-1": "先用 0.02 训练 10 轮记下损失，重置后换 0.05 再试：损失开始往上窜了。",
        "module-2": "数据给了模型上限：覆盖范围决定它能不能外推，数据量决定参数稳不稳。",
        "lab-2": "把覆盖范围停在 4，看区外误差是区内误差的几倍；再拖到 10，区外就铺满了。",
        "worked-example": "四步走：看清更新公式、算一步走了多远、看误差为什么放大、给出处置。",
        "conceptest-1": "干扰项里藏着最常见的那几个错误想法，选完看清每一个解释。",
        "synthesis": "把阶数拉到 7、数据量压到 8：训练误差接近零而测试误差涨上去，两条误差分叉了。",
        "posttest": "换了覆盖不足和训练发散的新情境，看看你还能不能用上四步循环与两条误差。",
        "summary": "用「参数、损失、学习率、测试误差」四个词，把一次完整的训练过程讲清楚。",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课是「人工智能与智慧社会」领域的模型体验课，承接人工智能典型应用，为后续的信息社会责任与数字公民做铺垫。设计上不引入任何品牌、产品与在线服务，全部用可计算、可观察的模拟承载概念：梯度下降训练台让学生用一根学习率滑块，在同一个程序上看到收敛、震荡、发散三种截然不同的后果，并把参数、损失、梯度、学习率四个量同时摆在读数上；覆盖范围与外推检验台把「数据决定上限」变成可以拖出来的两条误差，学生亲眼看到覆盖区内误差很小而覆盖区外越拉越开；模型体检台用阶数与数据量两个滑块驱动一次真实的拟合与留出评估，让欠拟合与过拟合各自表现为「两条误差都高」和「两条误差分叉」。价值取向上强调数据质量、覆盖范围与评价方式的重要性，以及不夸大模型能力、负责任使用智能技术的态度。",
    "plan_table": """| 1 | cover | 简单 AI 模型体验 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：模型里的参数到底是谁在调？ | 起·前测（暴露直觉） |
| 5 | concept | 模型是带参数的函数，训练就是把它调到合适的位置 | 承·概念一 |
| 6 | interactive | 梯度下降训练台：学习率调大调小，后果完全不同 | 承·实验室一（参数与损失可观察） |
| 7 | concept | 数据决定模型的上限：没见过的输入，它只是在猜 | 承·概念二 |
| 8 | interactive | 覆盖范围与外推检验台：数据铺到哪里，模型才管到哪里 | 承·实验室二（区内与区外误差可比较） |
| 9 | concept | 例题示范：学习率调大了，损失为什么反而越来越大？ | 转·重难点突破（分步示范 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：当一次模型体检员，分清欠拟合和过拟合 | 合·迁移应用 |
| 12 | quiz | 后测：换一个情境，看看规律还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把自己讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：模型是带参数的函数 / 训练循环的四步 / 数据决定模型上限 三栏\n- P5 训练循环四步图（已生成）：预测 → 算损失 → 算梯度 → 更新参数，循环往复\n- P7 覆盖范围与外推误差图（已生成）：覆盖区内贴合、覆盖区外偏离真实规律\n- 若需补充：不含任何品牌与在线服务界面的通用示意图（不出现真实产品名称与商标文字）",
}
