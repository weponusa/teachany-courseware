# -*- coding: utf-8 -*-
"""小学信息科技 · 反馈控制原理（G6）—— 补齐知识树「过程与控制」空缺

学科语气：信息科技 = 概念 + 动手并重。本课不背术语，只做三件真能上手的事：
  ① 恒温控制器：亲手设好目标温度、把房间换个环境，再点「跑一步」，
     看着 读数 → 比较 → 执行 → 再读 这一圈一步步转起来
  ② 震荡实验室：三个预设方案（稳妥 / 苛刻 / 保守）各跑一趟，用温度曲线看出
     「要求定得太苛刻 + 每次动手太猛 → 温度一直来回震荡」
  ③ 自动浇花器设计：自己定目标湿度、浇水量和天气，跑 20 天看它稳不稳
最后收口到一句可带走的口诀与一条判断经验：
  目标值定好，读回来，比一比，再动手——动手之后还要再读一次；
  要求越苛刻、动作越猛，就越容易在目标两边来回跳。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)
import json

F1 = './assets/it-e-feedback-control-fig1.webp'
F2 = './assets/it-e-feedback-control-fig2.webp'

TTS = {
    "hero": "先看一件很常见的事。给房间设好二十五摄氏度，它就一直默默地做事：过一会儿量一量现在多少度，比一比离二十五度还差多少，差得多就多加热一会儿，差得少就停下来。它从来没有一次就把温度调到刚刚好，只是不停地量、不停地比、不停地一点点调整。这种转着圈自己修正的能力，就是反馈。今天这节课，我们要亲手给一台恒温控制器设好目标值，看它怎样一圈一圈把温度稳下来，还要故意把要求定得太苛刻，让它一直来回震荡。",
    "problem-anchor": "开始之前，先选一个你最想弄明白的问题。是想知道机器凭什么能一直把温度稳在一个数上，还是想知道它每一圈到底做了哪几件事，又或者你想弄明白为什么有的装置会一直在目标两边来回跳，再或者你想亲手给一台自动浇花器定一套规矩。选好了，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出反馈控制里的四件事：定下目标值、读回当前值、比一比差多少、照着差值动手。第二，能按顺序说出感知、比较、执行、再感知这一圈，并说清为什么动手之后还要再读一次。第三，能解释为什么要求定得太苛刻、每次动手太猛，就会一直在目标两边来回震荡。第四，能给一个生活中的自动控制装置写出它的目标值、读什么、比什么、动什么手。",
    "pretest": "先做三道小题，用你现在的想法选就行。选完马上能看到解释，选错了也没关系，正好知道该重点听哪里。",
    "module-1": "先说反馈是什么。普通的做法是做完一次就结束，可自动控制不是。它的做法是转着圈来：先定下一个目标值，这是希望达到的数；再让传感器读回当前值，这是现在的实际样子；然后把两个数比一比，看看差多少；再照着这个差值动手调整；调整完以后，还要再读一次，看看现在离目标还有多远。这一圈转下去，就叫反馈。要记住的是：最后一件事永远是再读一次，因为它决定了下一圈该往哪个方向调。",
    "lab-1": "我们现在亲手跑一台恒温控制器。先在左边设好目标温度，再点一个环境，把房间放到不同的地方。然后点跑一步，你会看到四件事一个一个亮起来：先读回现在的温度，再和目标比一比差多少，然后决定加热器开还是不开，最后再读一次新温度。连着跑几步，看它是不是一点一点靠近目标。也试试把要求调到最苛刻、加热力度调到最大，看会出现什么。",
    "module-2": "第二件事，说说比较这一格里到底在算什么。它其实只做一次减法：目标值减去当前值，得到差值。差值正数，说明还没到，要动手往上补；差值接近零，说明已经到位，可以停手；差值变成负数，说明超过了，就该往下收。所以动作的大小，是由差值决定的。这里还有一个很关键的细节：几乎所有的执行元件都只有开和关两档，不能一点点地微调。于是要求越苛刻、每次动手越猛，就越容易一冲冲过头，然后关掉，掉下来，再冲过头——温度就在目标两边来回跳，这叫震荡。",
    "lab-2": "现在来做对比实验。这里准备了三套方案：稳妥型要求合理、每次适度加热；苛刻型要求非常准、每次加热很猛；保守型放在一个有点冷的房间里，每次只加热一丁点。三套各跑一趟，盯着那条温度曲线看：哪一套能稳稳贴在目标线上，哪一套在目标两边大幅来回跳，哪一套怎么跑都够不着目标。你也可以自己拖动滑块，把这三种情况都调出来。",
    "worked-example": "我们一起把恒温热水器完整拆一遍。第一步定目标值：设成五十摄氏度。第二步感知：温度传感器读回现在多少度，比如四十三度。第三步比较：五十减四十三，差七度，还差得远。第四步执行：加热器全功率加热。第五步再感知：读完这一圈之后再读一次，现在是四十八度。于是下一圈的比较结果变成差两度，加热就减弱。就这样一圈一圈，差值越来越小，水温慢慢稳定在五十度附近。第五步是最容易被漏掉的一步。",
    "conceptest-1": "接下来用三个容易弄错的说法考考你。请仔细读每一个选项，选完再看解释。",
    "synthesis": "最后一件事交给你。花房要装一台自动浇花器，参数由你来定：目标湿度是多少、每次浇多少水、天气有多干。定好以后让它自动浇二十天，看看土壤湿度曲线是稳稳贴在目标上，还是一会儿干一会儿淹，或者一直浇不够。跑完再回来想一想：如果每次浇水量调到最大会发生什么，为什么。",
    "posttest": "最后一轮，换几个新的小情境来考考你。这次会出现空调、一个一直在目标两边来回跳的装置，还有一道关于安全用电的题目，看看你能不能把反馈这一圈用上去。",
    "summary": "这节课我们记住三句话。第一句，反馈控制的四件事是：定下目标值、读回当前值、比一比差多少、照着差值动手，动手之后还要再读一次。第二句，比较就是一减法：差值正数就往上补，接近零就停手，负数就往下收，动作的大小由差值决定。第三句，要求定得越苛刻、每次动手越猛，就越容易一冲冲过头，然后关掉、掉下来、再冲过头，温度就在目标两边来回跳——这叫震荡，不是机器坏了，是要求提得太狠了。回到开头那台空调，它靠的就是这一圈一圈的反馈。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出反馈控制的四件事，并说说为什么动手之后还要再读一次。第二层能力应用，动手做：观察家里的空调或者电热水器，写出它的目标值是什么、读回的是什么、比对的标准是什么、动的是什么手。第三层迁移挑战，选做：给家里的自动浇花器写一份控制方案，写出目标湿度、每次浇多少、以及怎样避免它一会儿干一会儿淹。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是学它之前要先会的，右边是学会之后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续学的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 反馈：转着圈自己修正", "lab-1": "动手一 恒温控制器", "module-2": "概念二 比较就是一减法",
    "lab-2": "动手二 震荡实验室", "worked-example": "例题讲解 拆开恒温热水器", "conceptest-1": "概念测试",
    "synthesis": "综合任务 设计自动浇花器", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# 动手一：三个环境
FC_ENVS = [
    ("cool", "凉爽的窗边（18 ℃）", 18),
    ("room", "普通房间（22 ℃）", 22),
    ("sun", "太阳晒着的教室（30 ℃）", 30),
]

# 动手二：三套预设方案（目标温度 / 允许误差 / 加热力度 / 房间环境温度）
FC_PRESETS = [
    ("safe", "稳妥型：要求合理（误差 0.5 ℃），每次适度加热（力度 0.35 ℃）", 25, 0.5, 0.35, 22),
    ("harsh", "苛刻型：要求非常准（误差 0.1 ℃），每次加热很猛（力度 1.5 ℃）", 25, 0.1, 1.5, 22),
    ("lazy", "保守型：房间有点冷（18 ℃），每次只加热一丁点（力度 0.12 ℃）", 25, 0.5, 0.12, 18),
]

CUSTOM_JS = r"""
/* ============================================================
   it-e-feedback-control 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 动手一：恒温控制器（设目标值 + 换环境 + 一步一步跑闭环）
   3) 动手二：震荡实验室（三套预设 + 三个滑块 + 自动跑出温度曲线）
   4) 综合任务：自动浇花器设计（目标湿度 / 浇水量 / 天气 → 跑 20 天）
   ============================================================ */
var FC_PRESETS = __FC_PRESETS_JSON__;
(function () {
  'use strict';

  var st = document.createElement('style');
  st.textContent =
    '.fc-row{display:flex;align-items:stretch;gap:8px;flex-wrap:wrap;margin-top:14px;}' +
    '.fc-row .inner-card{flex:1;min-width:160px;margin:0;transition:box-shadow .3s ease;}' +
    '.fc-arrow{display:grid;place-items:center;color:var(--muted);font-size:18px;font-weight:800;min-width:16px;}' +
    '.fc-v{color:var(--text-secondary);font-size:14px;line-height:1.6;margin:0;min-height:46px;}' +
    '.fc-lit{box-shadow:0 0 0 2px var(--brand) inset;}' +
    '.fc-gauge{position:relative;height:26px;border-radius:13px;background:var(--bg-subtle);border:1px solid var(--line);overflow:hidden;margin-top:12px;}' +
    '.fc-gauge-fill{position:absolute;left:0;top:0;bottom:0;width:0%;border-radius:13px;background:linear-gradient(90deg,var(--brand-2),var(--brand));transition:width .5s ease;}' +
    '.fc-gauge-goal{position:absolute;top:-3px;bottom:-3px;width:3px;background:var(--warm-deep);transition:left .3s ease;}' +
    '.fc-chart{position:relative;display:flex;align-items:flex-end;gap:2px;height:150px;padding:6px;border:1px solid var(--line);border-radius:12px;background:var(--bg-subtle);margin-top:12px;}' +
    '.fc-bar{flex:1;min-width:4px;height:100%;display:flex;align-items:flex-end;}' +
    '.fc-bar-fill{width:100%;border-radius:4px 4px 0 0;background:var(--brand-2);transition:height .3s ease;}' +
    '.fc-goalline{position:absolute;left:6px;right:6px;border-top:2px dashed var(--warm-deep);opacity:.85;}' +
    '.fc-legend{font-size:12px;color:var(--muted);margin-top:6px;}' +
    '.fc-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:12px;}' +
    '.fc-tick{border:1px dashed var(--line);border-radius:12px;padding:8px 6px;text-align:center;font-size:13px;color:var(--muted);background:var(--bg-subtle);transition:all .3s ease;}' +
    '.fc-tick.on{border-style:solid;border-color:var(--brand);color:var(--link);background:var(--brand-soft);font-weight:700;}' +
    '@media (max-width:768px){.fc-grid{grid-template-columns:repeat(2,1fr);}}';
  document.head.appendChild(st);

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

  function setV(el, text) {
    if (!el) return;
    el.classList.add('selected');
    el.querySelector('.fc-v').textContent = text;
  }
  function clearV(ids, placeholders) {
    ids.forEach(function (id, i) {
      var el = document.getElementById(id);
      if (!el) return;
      el.classList.remove('selected');
      el.querySelector('.fc-v').textContent = placeholders ? (placeholders[i] || '—') : '—';
    });
  }
  function ticks(ids, upto) {
    ids.forEach(function (id, i) {
      var el = document.getElementById(id);
      if (el) el.classList.toggle('on', i < upto);
    });
  }
  function gauge(fillId, goalId, t, target) {
    var lo = 14, hi = 36;
    var f = document.getElementById(fillId);
    var g = document.getElementById(goalId);
    if (f) f.style.width = Math.max(0, Math.min(100, (t - lo) / (hi - lo) * 100)) + '%';
    if (g) g.style.left = Math.max(0, Math.min(99, (target - lo) / (hi - lo) * 100)) + '%';
  }
  function drawChart(boxId, series, target, lo, hi) {
    var box = document.getElementById(boxId);
    if (!box) return;
    var html = '';
    series.forEach(function (v) {
      var h = Math.max(2, Math.min(100, (v - lo) / (hi - lo) * 100));
      html += '<div class="fc-bar"><div class="fc-bar-fill" style="height:' + h.toFixed(1) + '%"></div></div>';
    });
    var gp = Math.max(2, Math.min(99, (target - lo) / (hi - lo) * 100));
    html += '<div class="fc-goalline" style="bottom:' + gp.toFixed(1) + '%" title="目标线"></div>';
    box.innerHTML = html;
  }
  function oscillates(tail, span) {
    var th = span / 4, prevSign = 0, rev = 0;
    for (var i = 1; i < tail.length; i++) {
      var d = tail[i] - tail[i - 1];
      if (Math.abs(d) < th) continue;
      var s = d > 0 ? 1 : -1;
      if (prevSign !== 0 && s !== prevSign) rev++;
      prevSign = s;
    }
    return rev > 0;
  }
  function judge(series, target, span) {
    var tail = series.slice(-8);
    var mx = Math.max.apply(null, tail), mn = Math.min.apply(null, tail);
    var rng = mx - mn;
    var sum = 0;
    tail.forEach(function (v) { sum += v; });
    var avg = sum / tail.length;
    if (rng > span && oscillates(tail, span)) return { kind: 'shake', rng: rng, avg: avg };
    if (Math.abs(avg - target) > span) return { kind: 'miss', rng: rng, avg: avg };
    return { kind: 'ok', rng: rng, avg: avg };
  }

  /* ---------- 2. 动手一：恒温控制器 ---------- */
  var p1 = document.getElementById('fc-panel');
  if (p1) {
    var T = 22, TENV = 22, target = 25, band = 0.5, power = 0.35, heater = false, nstep = 0, busy1 = false;
    var hist1 = [];
    var TICK = ['fc-t1', 'fc-t2', 'fc-t3', 'fc-t4'];
    var CELL = ['fc-c1', 'fc-c2', 'fc-c3', 'fc-c4'];
    var PLACE = ['等着读温度', '等着比一比', '等着动手', '等着再读一次'];
    var v1 = document.getElementById('fc-verdict');

    function r2(x) { return Math.round(x * 100) / 100; }
    function showState() {
      var d = r2(target - T);
      document.getElementById('fc-now').textContent = T.toFixed(1) + ' ℃';
      document.getElementById('fc-diff').textContent = (d > 0 ? '+' : '') + d.toFixed(1) + ' ℃';
      document.getElementById('fc-heater').textContent = heater ? '正在加热' : '停止加热';
      document.getElementById('fc-steps').textContent = String(nstep);
      gauge('fc-gauge-fill', 'fc-gauge-goal', T, target);
    }
    function reset1(envT) {
      TENV = envT; T = envT; heater = false; nstep = 0; hist1 = [T];
      clearV(CELL, PLACE); ticks(TICK, 0); showState();
    }

    p1.querySelectorAll('[data-fc-env]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (busy1) return;
        p1.querySelectorAll('[data-fc-env]').forEach(function (x) { x.classList.remove('selected'); });
        b.classList.add('selected');
        reset1(parseFloat(b.dataset.fcEnv));
        v1.className = 'result warn';
        v1.innerHTML = '房间换到了<strong>' + b.textContent.trim() + '</strong>，里面的温度一下变成了 ' +
          T.toFixed(1) + ' ℃。目标还是 ' + target.toFixed(1) +
          ' ℃ —— 你看，环境一变，装置马上就有活干了。点「跑一步」看它怎么反应。';
      });
    });

    function bindSlider(id, outId, apply, unit, dec) {
      var s = document.getElementById(id);
      if (!s) return;
      s.addEventListener('input', function () {
        var v = parseFloat(s.value);
        apply(v);
        var o = document.getElementById(outId);
        if (o) o.textContent = v.toFixed(dec === undefined ? 1 : dec) + unit;
        showState();
      });
    }
    bindSlider('fc-target-slider', 'fc-target-out', function (v) { target = v; }, ' ℃');
    bindSlider('fc-band-slider', 'fc-band-out', function (v) { band = v; }, ' ℃');
    bindSlider('fc-power-slider', 'fc-power-out', function (v) { power = v; }, ' ℃', 2);

    function runStep(done, speed) {
      speed = speed || 320;
      var read = r2(T);
      var d = r2(target - read);
      ticks(TICK, 1);
      setV(document.getElementById(CELL[0]), '传感器读数 = ' + read.toFixed(1) + ' ℃');
      setTimeout(function () {
        ticks(TICK, 2);
        setV(document.getElementById(CELL[1]), '目标 ' + target.toFixed(1) + ' − 现在 ' + read.toFixed(1) +
          ' = ' + (d > 0 ? '还差 ' + d.toFixed(1) : '已经超过 ' + Math.abs(d).toFixed(1)) + ' ℃');
      }, speed);
      setTimeout(function () {
        heater = d > band;
        ticks(TICK, 3);
        setV(document.getElementById(CELL[2]), heater
          ? '差值比允许的 ' + band.toFixed(1) + ' ℃ 大 —— 加热器打开'
          : '差值在允许的 ' + band.toFixed(1) + ' ℃ 以内 —— 加热器停下');
      }, speed * 2);
      setTimeout(function () {
        T = T + 0.08 * (TENV - T) + (Math.random() * 0.2 - 0.1) + (heater ? power : 0);
        T = r2(T);
        nstep++;
        ticks(TICK, 4);
        setV(document.getElementById(CELL[3]), '再读一次 = ' + T.toFixed(1) + ' ℃');
        hist1.push(T);
        showState();
        if (done) done();
      }, speed * 3);
    }

    var ids1 = ['fc-c1', 'fc-c2', 'fc-c3', 'fc-c4'];
    document.getElementById('fc-step').addEventListener('click', function () {
      if (busy1) return;
      busy1 = true;
      clearV(ids1, PLACE);
      runStep(function () {
        busy1 = false;
        var d = r2(target - T);
        v1.className = 'result warn';
        v1.innerHTML = '跑完一圈。现在是 ' + T.toFixed(1) + ' ℃，' +
          (Math.abs(d) <= band ? '已经在允许的范围里，加热器会停下来。'
            : (d > 0 ? '还差 ' + d.toFixed(1) + ' ℃，下一圈继续加热。' : '超过了 ' + Math.abs(d).toFixed(1) + ' ℃，下一圈会停手。')) +
          '　<strong>注意最后一步：动手之后一定要再读一次</strong>，它决定了下一圈往哪个方向调。';
      }, 320);
    });

    document.getElementById('fc-auto').addEventListener('click', function () {
      if (busy1) return;
      busy1 = true;
      clearV(ids1, PLACE);
      var left = 16;
      function loop() {
        if (left <= 0) {
          busy1 = false;
          var j = judge(hist1, target, 1.0);
          if (TENV > target + 0.5 && Math.abs(j.avg - target) > 1.5) {
            v1.className = 'result error';
            v1.innerHTML = '<strong>连跑 16 圈：它一直降不下来。</strong>房间本身就有 ' + TENV.toFixed(0) +
              ' ℃，比目标 ' + target.toFixed(0) + ' ℃ 还热。这台装置的执行元件只会加热、不会降温，' +
              '温度只能往上走，最后停在 ' + j.avg.toFixed(1) + ' ℃。' +
              '<span style="color:var(--muted)">这不是反馈失灵，是装置的能力不够——这种情况得换一个会制冷的执行元件，' +
              '或者先把房间弄凉一点。改变环境之后，同一台装置表现会完全不同。</span>';
          } else if (j.kind === 'shake') {
            v1.className = 'result error';
            v1.innerHTML = '<strong>连跑 16 圈：温度一直在目标两边来回跳。</strong>' +
              '最后几圈在 ' + (j.avg - j.rng / 2).toFixed(1) + ' ℃ 和 ' + (j.avg + j.rng / 2).toFixed(1) +
              ' ℃ 之间反复（相差 ' + j.rng.toFixed(1) + ' ℃）。' +
              '<strong>这就是「目标值设得太苛刻」的样子</strong>：允许误差只有 ' + band.toFixed(1) +
              ' ℃，每次却加热 ' + power.toFixed(2) + ' ℃，一冲就冲过头，关掉、掉下来，再冲过头。' +
              '把允许误差放宽一点，或者把力度调小一点，它就稳了。';
          } else if (j.kind === 'miss') {
            v1.className = 'result error';
            v1.innerHTML = '<strong>连跑 16 圈：怎么跑都够不着目标。</strong>温度平均停在 ' + j.avg.toFixed(1) +
              ' ℃，离目标 ' + target.toFixed(1) + ' ℃ 还差得远。每次只加热 ' + power.toFixed(2) +
              ' ℃，补进来的还不够房间散掉的。把力度调大一点试试。';
          } else {
            v1.className = 'result';
            v1.innerHTML = '<strong>连跑 16 圈：稳住了。</strong>温度最后停在 ' + j.avg.toFixed(1) + ' ℃ 附近' +
              '（目标 ' + target.toFixed(1) + ' ℃，允许误差 ' + band.toFixed(1) + ' ℃）。' +
              '它不会一动不动——加热器只有开和关两档，本来就会在目标附近小幅上下。' +
              '这一圈一圈靠近、然后稳下来的过程，就是反馈。';
          }
          return;
        }
        left--;
        runStep(loop, 110);
      }
      v1.className = 'result warn';
      v1.textContent = '开始自动跑 16 圈……盯着温度条上那根橙色的目标线。';
      loop();
    });

    document.getElementById('fc-reset').addEventListener('click', function () {
      if (busy1) return;
      reset1(TENV);
      v1.className = 'result warn';
      v1.textContent = '重来了。温度回到 ' + TENV.toFixed(1) + ' ℃，再把刚才那几步跑一遍。';
    });

    reset1(22);
    var roomBtn = p1.querySelector('[data-fc-env="22"]');
    if (roomBtn) roomBtn.classList.add('selected');
    showState();
  }

  /* ---------- 3. 动手二：震荡实验室 ---------- */
  var p2 = document.getElementById('fs-panel');
  if (p2) {
    var T2 = 25, TENV2 = 22, tar2 = 25, band2 = 1.0, pow2 = 0.3, hist2 = [], bk2 = false;
    var v2 = document.getElementById('fs-out');
    var CELL2 = ['fs-c1', 'fs-c2', 'fs-c3', 'fs-c4'];
    var PLACE2 = ['等着读温度', '等着比一比', '等着动手', '等着再读一次'];

    function sync2() {
      document.getElementById('fs-target').textContent = tar2.toFixed(1) + ' ℃';
      document.getElementById('fs-band').textContent = band2.toFixed(1) + ' ℃';
      document.getElementById('fs-power').textContent = pow2.toFixed(2) + ' ℃';
      document.getElementById('fs-now').textContent = T2.toFixed(1) + ' ℃';
      var pf = document.getElementById('fs-profile');
      if (pf) pf.textContent = '目标 ' + tar2.toFixed(1) + ' ℃ · 允许 ' + band2.toFixed(1) +
        ' ℃ · 力度 ' + pow2.toFixed(2) + ' ℃ · 房间 ' + TENV2.toFixed(0) + ' ℃';
    }
    function s2(id, outId, apply, unit, dec) {
      var s = document.getElementById(id);
      if (!s) return;
      s.addEventListener('input', function () {
        var v = parseFloat(s.value);
        apply(v);
        var o = document.getElementById(outId);
        if (o) o.textContent = v.toFixed(dec === undefined ? 1 : dec) + unit;
        sync2();
      });
    }
    s2('fs-target-slider', 'fs-target-out', function (v) { tar2 = v; }, ' ℃');
    s2('fs-band-slider', 'fs-band-out', function (v) { band2 = v; }, ' ℃');
    s2('fs-power-slider', 'fs-power-out', function (v) { pow2 = v; }, ' ℃', 2);

    function load2(preset) {
      tar2 = preset[2]; band2 = preset[3]; pow2 = preset[4]; TENV2 = preset[5];
      document.getElementById('fs-target-slider').value = tar2;
      document.getElementById('fs-band-slider').value = band2;
      document.getElementById('fs-power-slider').value = pow2;
      document.getElementById('fs-target-out').textContent = tar2.toFixed(1) + ' ℃';
      document.getElementById('fs-band-out').textContent = band2.toFixed(1) + ' ℃';
      document.getElementById('fs-power-out').textContent = pow2.toFixed(2) + ' ℃';
      T2 = TENV2; hist2 = [];
      drawChart('fs-chart', [T2], tar2, 14, 36);
      clearV(CELL2, PLACE2); ticks(['fs-t1', 'fs-t2', 'fs-t3', 'fs-t4'], 0);
      sync2();
    }

    p2.querySelectorAll('[data-fs-preset]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (bk2) return;
        p2.querySelectorAll('[data-fs-preset]').forEach(function (x) { x.classList.remove('selected'); });
        b.classList.add('selected');
        var i = parseInt(b.dataset.fsPreset, 10);
        load2(FC_PRESETS[i]);
        v2.className = 'result warn';
        v2.textContent = '方案已装好：' + b.textContent.trim() + '。点「自动跑 16 圈」，看温度曲线长什么样。';
      });
    });

    document.getElementById('fs-run').addEventListener('click', function () {
      if (bk2) return;
      bk2 = true;
      clearV(CELL2, PLACE2);
      T2 = TENV2; hist2 = [T2];
      var left = 16;
      v2.className = 'result warn';
      v2.textContent = '开始跑 16 圈……';
      function loop() {
        if (left <= 0) {
          bk2 = false;
          drawChart('fs-chart', hist2, tar2, 14, 36);
          var j = judge(hist2, tar2, 1.0);
          sync2();
          if (j.kind === 'shake') {
            v2.className = 'result error';
            v2.innerHTML = '<strong>结论：一直在目标两边来回震荡。</strong>' +
              '最后八圈的读数在 ' + (j.avg + j.rng / 2).toFixed(1) + ' ℃ 和 ' + (j.avg - j.rng / 2).toFixed(1) +
              ' ℃ 之间反复跳（相差 ' + j.rng.toFixed(1) + ' ℃，平均 ' + j.avg.toFixed(1) + ' ℃）。' +
              '常见错误：以为「要求越准越好、动作越大越快」。<strong>要求定得太苛刻，加上每次加热太猛，' +
              '就会一冲冲过头，关掉、掉下来，再冲过头</strong>——这不是机器坏了，是要求提得太狠了。' +
              '把允许误差放宽一点，或者把每次加热的力度调小一点，曲线就会平下来。';
          } else if (j.kind === 'miss') {
            v2.className = 'result error';
            v2.innerHTML = '<strong>结论：怎么跑都够不着目标。</strong>' +
              '十六圈下来，平均只有 ' + j.avg.toFixed(1) + ' ℃，离目标 ' + tar2.toFixed(1) +
              ' ℃ 差了一大截。不是它不努力——每次只加热一丁点，而房间一直在散热，补进来的还不够散掉的。' +
              '常见错误：以为「动作越小越保险」。动作太小，它就永远追不上目标。';
          } else {
            v2.className = 'result';
            v2.innerHTML = '<strong>结论：稳稳贴在目标附近。</strong>' +
              '最后八圈的读数在 ' + (j.avg + j.rng / 2).toFixed(1) + ' ℃ 和 ' + (j.avg - j.rng / 2).toFixed(1) +
              ' ℃ 之间小幅波动（平均 ' + j.avg.toFixed(1) + ' ℃）。它不会一动不动——' +
              '加热器只有开和关两档，本来就会小幅上上下下。这种小幅波动是正常的，' +
              '只要始终在目标附近，就算稳住了。';
          }
          return;
        }
        left--;
        var read = T2;
        var d = tar2 - read;
        ticks(['fs-t1', 'fs-t2', 'fs-t3', 'fs-t4'], 1);
        setV(document.getElementById(CELL2[0]), '读数 = ' + read.toFixed(1) + ' ℃');
        var heater2 = d > band2;
        ticks(['fs-t1', 'fs-t2', 'fs-t3', 'fs-t4'], 3);
        setV(document.getElementById(CELL2[1]), '目标 ' + tar2.toFixed(1) + ' − 现在 ' + read.toFixed(1) + ' = ' +
          (d > 0 ? '还差 ' + d.toFixed(1) : '超过 ' + Math.abs(d).toFixed(1)) + ' ℃');
        setV(document.getElementById(CELL2[2]), heater2 ? '加热器：开（+ ' + pow2.toFixed(2) + ' ℃）' : '加热器：关（自然散热）');
        T2 = T2 + 0.08 * (TENV2 - T2) + (Math.random() * 0.2 - 0.1) + (heater2 ? pow2 : 0);
        T2 = Math.round(T2 * 100) / 100;
        hist2.push(T2);
        setV(document.getElementById(CELL2[3]), '再读一次 = ' + T2.toFixed(1) + ' ℃');
        ticks(['fs-t1', 'fs-t2', 'fs-t3', 'fs-t4'], 4);
        sync2();
        drawChart('fs-chart', hist2, tar2, 14, 36);
        setTimeout(loop, 90);
      }
      loop();
    });

    load2(FC_PRESETS[0]);
  }

  /* ---------- 4. 综合任务：自动浇花器设计 ---------- */
  var p3 = document.getElementById('wf-panel');
  if (p3) {
    var tarH = 50, amount = 6, evap = 2, bk3 = false;
    var v3 = document.getElementById('wf-out');

    function s3(id, outId, apply, unit) {
      var s = document.getElementById(id);
      if (!s) return;
      s.addEventListener('input', function () {
        var v = parseFloat(s.value);
        apply(v);
        var o = document.getElementById(outId);
        if (o) o.textContent = v.toFixed(1) + unit;
      });
    }
    s3('wf-target-slider', 'wf-target-out', function (v) { tarH = v; }, ' %');
    s3('wf-amount-slider', 'wf-amount-out', function (v) { amount = v; }, ' %');
    s3('wf-evap-slider', 'wf-evap-out', function (v) { evap = v; }, ' %');

    document.getElementById('wf-run').addEventListener('click', function () {
      if (bk3) return;
      bk3 = true;
      var H = tarH - 5, hist = [H], i;
      for (i = 0; i < 20; i++) {
        H = H - evap;
        if (tarH - H > 0) H = H + amount;
        if (H > 100) H = 100;
        if (H < 0) H = 0;
        hist.push(Math.round(H * 10) / 10);
      }
      drawChart('wf-chart', hist, tarH, 0, 100);
      var j = judge(hist, tarH, 8);
      var mx = Math.max.apply(null, hist);
      var note = '';
      if (mx > 85) note = ' 另外，湿度最高冲到 ' + mx.toFixed(0) + '%，根一直泡在水里会烂——这是容易忽略的另一半风险。';
      var txt;
      if (j.kind === 'shake') {
        txt = '<strong>结论：一会儿干、一会儿淹。</strong>土壤湿度在 ' + (j.avg - j.rng / 2).toFixed(0) +
          '% 到 ' + (j.avg + j.rng / 2).toFixed(0) + '% 之间大幅来回跳。每次浇水太多，浇一次就浇过头，' +
          '接下来好几天只能干等着它慢慢干掉，然后再狠狠浇一次。' +
          '<span style="color:var(--muted)">改进办法：把每次浇水量调小，改成少量多次。</span>';
      } else if (j.kind === 'miss') {
        txt = '<strong>结论：一直浇不够。</strong>二十天下来平均只有 ' + j.avg.toFixed(0) +
          '%，离目标 ' + tarH.toFixed(0) + '% 差得远。每次浇的水还不够蒸发的，土壤越来越干。' +
          '<span style="color:var(--muted)">改进办法：把每次浇水量调大，或者让它更频繁地来看一眼。</span>';
      } else {
        txt = '<strong>结论：稳在目标附近。</strong>湿度大体保持在 ' + tarH.toFixed(0) +
          '% 上下，浇水之后高一点、蒸发之后低一点，是正常的来回调整。' +
          '<span style="color:var(--muted)">它的做法就是反馈：读一次湿度、和目标比一比、差得多就浇、浇完再看一眼。</span>';
      }
      v3.className = j.kind === 'ok' ? 'result' : 'result warn';
      v3.innerHTML = txt + note;
      bk3 = false;
    });

    drawChart('wf-chart', [tarH], tarH, 0, 100);
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：它是怎么把温度稳住的？", TTS["pretest"], [
        {"q": "给房间设好 25 ℃ 以后，空调是怎么做的？",
         "options": [("过一会儿量一下温度，比一比差多少，再决定吹大还是吹小，然后接着量", True),
                     ("一口气把房间吹到 25 ℃，然后就再也不管了", False),
                     ("先把温度记在心里，最后再一起调", False)],
         "explain": "它不会一次到位，而是量一次、比一次、动一次，再量一次，一圈一圈地靠近目标。"
                    "<strong>错因提醒：</strong>常见错误是把自动控制想成「一次设定就完成」。"
                    "真实的做法是一直转着圈调整。"},
        {"q": "反馈控制里，「比较」这一步在算什么？",
         "options": [("拿目标值减去当前读数，看看差多少", True),
                     ("看看用了多少电", False),
                     ("随便挑一个数来用", False)],
         "explain": "比较就是一减法：目标值 − 当前值 = 差值。差值正数就往上补，接近零就停手，负数就往下收。"
                    "<strong>错因提醒：</strong>容易误认为比较是「做不做」的二选一——"
                    "其实它先算出一个数，动作的大小由这个数决定。"},
        {"q": "一台装置把温度调到目标以后，为什么还要再读一次？",
         "options": [("为了知道现在离目标还有多远，决定下一圈往哪个方向调", True),
                     ("为了把数字记下来交作业", False),
                     ("读不读都一样，它是多此一举", False)],
         "explain": "再读一次是闭环的最后一步，也是下一圈的开始。没有它，装置就不知道自己有没有把事办好。"
                    "<strong>错因提醒：</strong>这是最容易漏掉的一步——不少人以为「动手做完就结束了」。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "反馈：做完一步，还要回头再看一眼", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们已经会拆「感知 → 判断 → 动作」这三步了（And）；可只会这三步的装置并不聪明：天亮了它可能还傻乎乎地开着灯，温度到了它可能还在加热（But）；于是要在这三步后面再补上一个「再感知」，让它照着结果回头修正自己——这一圈转起来，才叫反馈（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">自动控制和我们平时做事最大的不同是：它<strong>做完不算完</strong>，还要回头看一眼结果，再照着结果调整。</p>
        <div class="grid grid-2">
          <div class="inner-card"><p><strong>① 定目标值</strong></p><p style="color:var(--muted)">希望达到的那个数，比如 25 ℃。</p></div>
          <div class="inner-card"><p><strong>② 读当前值</strong></p><p style="color:var(--muted)">传感器读回来的真实情况，比如 22.6 ℃。</p></div>
          <div class="inner-card"><p><strong>③ 比一比</strong></p><p style="color:var(--muted)">两个数相减，看看差多少、往哪边差。</p></div>
          <div class="inner-card"><p><strong>④ 动手 + 再读</strong></p><p style="color:var(--muted)">照着差值调整，然后<strong>再读一次</strong>，看现在离目标还有多远。</p></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="反馈闭环示意图：定下目标值，传感器读回当前值，两个数比一比，照着差值动手调整，然后再读一次回到起点">
          <figcaption>反馈就是转着圈自己修正：读回当前值 → 和目标比一比 → 照着差值动手 → 再读一次，回到起点开始下一圈</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">💡</span><div><strong>记一句口诀：</strong>定目标、读回来、比一比、再动手——动手之后还要再读一次。少了最后那一次，它就只能瞎调整。</div></div>
{insight_box([
    {"lens": "解释它", "text": "为什么不能一次就把温度调到刚刚好？因为加热需要时间，房间还在不断散热，一次动作之后结果难料——所以只能边做边看、边看边改。"},
    {"lens": "比较它", "text": "「感知 → 判断 → 动作」是一条直线，做完就结束了；加上「再感知」以后首尾接上，变成一圈。直线只做一次，圈能一直修正自己。"},
    {"lens": "迁移它", "text": "你自己练字、跑步也是反馈：写完看一眼歪不歪（再感知），下一笔再调。会回头看的人，进步比只顾埋头做的人快。"},
])}
    ''', tag="概念一"))

    env_btns = "\n".join(
        f'              <button class="choice" data-fc-env="{t}" style="text-align:center">{label}</button>'
        for _k, label, t in FC_ENVS
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：恒温控制器——点着一步步跑起来", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先设好目标温度，再点一个环境把房间换掉（环境一换，装置马上就有活干）。然后点「跑一步」，看感知、比较、执行、再感知一格一格亮起来。</p>
        <div class="lab-panel" id="fc-panel">
          <div class="slider-row">
            <label for="fc-target-slider">目标温度</label>
            <input type="range" id="fc-target-slider" min="18" max="30" step="0.5" value="25">
            <span class="readout-cell" style="flex:0 0 96px"><span class="v" id="fc-target-out">25.0 ℃</span></span>
          </div>
          <div class="slider-row">
            <label for="fc-band-slider">要求多准（允许差多少）</label>
            <input type="range" id="fc-band-slider" min="0.1" max="2" step="0.1" value="0.5">
            <span class="readout-cell" style="flex:0 0 96px"><span class="v" id="fc-band-out">0.5 ℃</span></span>
          </div>
          <div class="slider-row">
            <label for="fc-power-slider">每次加热的力度</label>
            <input type="range" id="fc-power-slider" min="0.1" max="1.5" step="0.05" value="0.35">
            <span class="readout-cell" style="flex:0 0 96px"><span class="v" id="fc-power-out">0.35 ℃</span></span>
          </div>
          <div style="font-weight:700;font-size:14px;margin:14px 0 6px">把房间换到哪个环境？</div>
          <div class="sort-bank">
{env_btns}
          </div>
          <div class="fc-gauge">
            <div class="fc-gauge-fill" id="fc-gauge-fill"></div>
            <div class="fc-gauge-goal" id="fc-gauge-goal"></div>
          </div>
          <p class="fc-legend">温度条：蓝色越满表示现在越热，橙色竖线是目标值所在的位置。</p>
          <div class="fc-row">
            <div class="inner-card" id="fc-c1"><p><strong>① 感知</strong></p><p class="fc-v">等着读温度</p></div>
            <div class="fc-arrow">→</div>
            <div class="inner-card" id="fc-c2"><p><strong>② 比较</strong></p><p class="fc-v">等着比一比</p></div>
            <div class="fc-arrow">→</div>
            <div class="inner-card" id="fc-c3"><p><strong>③ 执行</strong></p><p class="fc-v">等着动手</p></div>
            <div class="fc-arrow">→</div>
            <div class="inner-card" id="fc-c4"><p><strong>④ 再感知</strong></p><p class="fc-v">等着再读一次</p></div>
          </div>
          <div class="fc-grid">
            <div class="fc-tick" id="fc-t1">① 感知</div>
            <div class="fc-tick" id="fc-t2">② 比较</div>
            <div class="fc-tick" id="fc-t3">③ 执行</div>
            <div class="fc-tick" id="fc-t4">④ 再感知</div>
          </div>
          <div class="readout-cell" style="margin-top:12px"><span class="k">现在读数</span><span class="v" id="fc-now">22.0 ℃</span></div>
          <div class="readout-cell" style="margin-top:8px"><span class="k">和目标差多少</span><span class="v" id="fc-diff">+3.0 ℃</span></div>
          <div class="readout-cell" style="margin-top:8px"><span class="k">加热器</span><span class="v green" id="fc-heater">停止加热</span></div>
          <div class="readout-cell" style="margin-top:8px"><span class="k">已跑圈数</span><span class="v" id="fc-steps">0</span></div>
          <div class="flex-row">
            <button class="choice" id="fc-step" style="text-align:center">▶ 跑一步</button>
            <button class="choice" id="fc-auto" style="text-align:center">自动跑 16 圈</button>
            <button class="choice" id="fc-reset" style="text-align:center">重来</button>
          </div>
          <p class="result warn" id="fc-verdict" style="margin-top:12px">先设好目标温度、点一个环境，然后点「跑一步」。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>试一件事：</strong>把「要求多准」拉到最左边 0.1 ℃，把「加热力度」拉到最右边 1.5 ℃，再自动跑一趟。看看温度是稳稳停住，还是在目标线两边来回跳。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "比较就是一减法：差值决定动作的大小", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">「比较」这一格里，机器只算一次减法：<strong>目标值 − 当前值 = 差值</strong>。这个差值有正有负，动作的方向和大小全看它。</p>
        <div class="grid grid-3">
          <div class="inner-card"><p><strong>差值是正数</strong></p><p style="color:var(--muted)">还没到，要往上补。差得越多，动作越大。</p></div>
          <div class="inner-card"><p><strong>差值接近零</strong></p><p style="color:var(--muted)">已经到位，可以停手。</p></div>
          <div class="inner-card"><p><strong>差值是负数</strong></p><p style="color:var(--muted)">超过了，该往下收。</p></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="两条温度曲线对比：要求宽松、力度合适时曲线稳稳贴在橙色目标线上；要求苛刻、力度太猛时曲线在目标线上下大幅来回跳动">
          <figcaption>同一台装置，两套要求：左边要求合理、动作适度，温度稳稳停在目标附近；右边要求太苛刻、动作太猛，温度在目标两边来回震荡</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">以为「要求定得越准越好、每次动手越猛越快」。可现实中的执行元件大多只有<strong>开和关两档</strong>，不能一点点微调。要求太苛刻、动作太猛，就会一冲冲过头，关掉、掉下来，再冲过头——温度在目标两边来回跳，这就是<strong>震荡</strong>。它不是机器坏了，是要求提得太狠了。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🧭</span><div><strong>一句话记住：</strong>允许差一点点，动作小一点，它反而更容易稳住。做人也一样——要求一步到位，常常来回摇摆。</div></div>
    ''', tag="概念二"))

    preset_btns = "\n".join(
        f'              <button class="choice" data-fs-preset="{i}" style="text-align:center">{label}</button>'
        for i, (_k, label, _t, _b, _p, _e) in enumerate(FC_PRESETS)
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：震荡实验室——三套方案各跑一趟", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">点一套预设方案，再点「自动跑 16 圈」，看下面那条温度曲线长什么样。也可以自己拖动滑块，把三种情况都调出来。</p>
        <div class="lab-panel" id="fs-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 先选一套方案（也可以自己调滑块）</div>
          <div class="sort-bank">
{preset_btns}
          </div>
          <div class="slider-row">
            <label for="fs-target-slider">目标温度</label>
            <input type="range" id="fs-target-slider" min="18" max="30" step="0.5" value="25">
            <span class="readout-cell" style="flex:0 0 96px"><span class="v" id="fs-target-out">25.0 ℃</span></span>
          </div>
          <div class="slider-row">
            <label for="fs-band-slider">要求多准（允许差多少）</label>
            <input type="range" id="fs-band-slider" min="0.1" max="2" step="0.1" value="0.5">
            <span class="readout-cell" style="flex:0 0 96px"><span class="v" id="fs-band-out">0.5 ℃</span></span>
          </div>
          <div class="slider-row">
            <label for="fs-power-slider">每次加热的力度</label>
            <input type="range" id="fs-power-slider" min="0.1" max="1.5" step="0.05" value="0.35">
            <span class="readout-cell" style="flex:0 0 96px"><span class="v" id="fs-power-out">0.35 ℃</span></span>
          </div>
          <div class="fc-chart" id="fs-chart"></div>
          <p class="fc-legend">横着每一根柱子是一圈的结果，柱子的高低表示温度；橙色虚线是目标值。柱子忽高忽低地跨过虚线，就是震荡。</p>
          <div class="fc-row">
            <div class="inner-card" id="fs-c1"><p><strong>① 感知</strong></p><p class="fc-v">等着读温度</p></div>
            <div class="fc-arrow">→</div>
            <div class="inner-card" id="fs-c2"><p><strong>② 比较</strong></p><p class="fc-v">等着比一比</p></div>
            <div class="fc-arrow">→</div>
            <div class="inner-card" id="fs-c3"><p><strong>③ 执行</strong></p><p class="fc-v">等着动手</p></div>
            <div class="fc-arrow">→</div>
            <div class="inner-card" id="fs-c4"><p><strong>④ 再感知</strong></p><p class="fc-v">等着再读一次</p></div>
          </div>
          <div class="readout-cell" style="margin-top:12px"><span class="k">目标 / 允许误差 / 力度</span><span class="v" id="fs-profile" style="font-size:15px">25.0 ℃</span></div>
          <div class="readout-cell" style="margin-top:8px"><span class="k">目标值</span><span class="v" id="fs-target">25.0 ℃</span></div>
          <div class="readout-cell" style="margin-top:8px"><span class="k">允许误差</span><span class="v" id="fs-band">1.0 ℃</span></div>
          <div class="readout-cell" style="margin-top:8px"><span class="k">每次力度</span><span class="v" id="fs-power">0.3 ℃</span></div>
          <div class="readout-cell" style="margin-top:8px"><span class="k">现在读数</span><span class="v green" id="fs-now">25.0 ℃</span></div>
          <div class="flex-row">
            <button class="choice" id="fs-run" style="text-align:center">▶ 自动跑 16 圈</button>
          </div>
          <p class="result warn" id="fs-out" style="margin-top:12px">先选一套方案，再点「自动跑 16 圈」。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">📉</span><div><strong>看曲线的时候问三句话：</strong>它是稳稳贴在虚线上方一点点吗？它在虚线两边大幅来回跨吗？它一直在虚线下面够不着吗？三种曲线对应三种不同的原因。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：把恒温热水器拆成五步", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>家里的恒温热水器，水温总能稳定在设定的温度附近。请说出它每一圈各做了什么，以及为什么它不会一次就调到位。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>定目标值：</strong>人把水温设成 50 ℃。这是希望达到的那个数。</div></div>
          <div class="step"><span class="n">2</span><div><strong>感知：</strong>温度传感器读回现在的水温，比如 43 ℃。</div></div>
          <div class="step"><span class="n">3</span><div><strong>比较：</strong>50 减 43，差 7 ℃。差值很大，说明还差得远。</div></div>
          <div class="step"><span class="n">4</span><div><strong>执行：</strong>差值大，加热器就以较大功率加热。</div></div>
          <div class="step"><span class="n green">5</span><div><strong>再感知：</strong>过一会儿再读一次，现在是 48 ℃。下一圈差值变成 2 ℃，加热就减弱。差得越来越少，最后稳稳停在 50 ℃ 附近。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">漏掉第五步「再感知」，把它当成重复劳动。少了它，加热器就不知道该在什么时候减弱、什么时候停，水温只会一路冲上去，不可能稳定在设定值附近。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">✏️</span><div><strong>动手画一画：</strong>在本子上画一个圈，四个箭头分别写上「读回水温」「和 50 ℃ 比一比」「差了就加热」「再读一次」，把箭头连成一个闭环。圈画好了，这台热水器才算讲清楚。</div></div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，错在哪里", TTS["conceptest-1"], [
        {"q": "「只要把目标值设好，机器就能一次把温度调到刚刚好。」这句话对吗？",
         "options": [("不对，它是量一次、比一次、调一次，一圈一圈靠近目标", True),
                     ("对，机器算得比人准", False),
                     ("对，只要加热器功率足够大就行", False)],
         "explain": "加热需要时间，房间还在散热，一次动作之后结果难料，所以只能边做边看、边看边改。"
                    "<strong>错因提醒：</strong>常见错误是把自动控制当成「一次设定就完成」——"
                    "真实的过程是一圈一圈修正。"},
        {"q": "某一圈里，目标 25 ℃，读回来 24.6 ℃，允许误差是 0.5 ℃。这一圈它会怎么做？",
         "options": [("差值只有 0.4 ℃，在允许范围内，就先不动手", True),
                     ("差值不是零，必须马上满功率加热", False),
                     ("把目标值改成 24.6 ℃，这样就没有误差了", False)],
         "explain": "差值 0.4 ℃ 小于允许的 0.5 ℃，已经在范围里，不需要调整。"
                    "<strong>错因提醒：</strong>容易误认为「差值不是零就得动手」——"
                    "留着一个小小的允许误差，反而更稳。"},
        {"q": "一台装置的温度一直在目标值上下大幅来回跳。最可能的原因是？",
         "options": [("要求定得太苛刻，加上每次动手太猛，一冲就冲过头", True),
                     ("这台机器已经坏掉了，只能换新的", False),
                     ("目标值设得太低了", False)],
         "explain": "执行元件大多只有开和关两档，要求太准、动作太猛就会反复冲过头——这叫震荡，是要求提得太狠。"
                    "<strong>错因提醒：</strong>常见错误是「一跳就以为机器坏了」。"
                    "先把允许误差放宽一点、力度调小一点试试。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：给花房设计一台自动浇花器", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">这回参数由你来定。先设好目标湿度、每次浇多少水、天气有多干，再点「自动浇 20 天」，看土壤湿度曲线是稳稳贴在目标上，还是一会儿干一会儿淹。</p>
        <div class="lab-panel" id="wf-panel">
          <div class="slider-row">
            <label for="wf-target-slider">目标湿度</label>
            <input type="range" id="wf-target-slider" min="30" max="70" step="1" value="50">
            <span class="readout-cell" style="flex:0 0 96px"><span class="v" id="wf-target-out">50.0 %</span></span>
          </div>
          <div class="slider-row">
            <label for="wf-amount-slider">每次浇多少</label>
            <input type="range" id="wf-amount-slider" min="1" max="20" step="1" value="6">
            <span class="readout-cell" style="flex:0 0 96px"><span class="v" id="wf-amount-out">6.0 %</span></span>
          </div>
          <div class="slider-row">
            <label for="wf-evap-slider">天气有多干（每天蒸发多少）</label>
            <input type="range" id="wf-evap-slider" min="0.5" max="4" step="0.5" value="2">
            <span class="readout-cell" style="flex:0 0 96px"><span class="v" id="wf-evap-out">2.0 %</span></span>
          </div>
          <div class="fc-chart" id="wf-chart"></div>
          <p class="fc-legend">每根柱子是一天的土壤湿度，橙色虚线是目标湿度。柱子忽上忽下地跨过虚线，就是一会儿干一会儿淹。</p>
          <div class="flex-row">
            <button class="choice" id="wf-run" style="text-align:center">▶ 自动浇 20 天</button>
          </div>
          <p class="result warn" id="wf-out" style="margin-top:12px">先设好三个参数，再点「自动浇 20 天」。</p>
        </div>
        <div class="inner-card">
          <p><strong>跑完以后想一想，说给同桌听：</strong></p>
          <p style="color:var(--muted)">把这台浇花器的反馈四步写出来：它读的是什么？和什么比？比完动什么手？「再感知」安排在什么时候？如果每次浇水量调到最大，曲线会变成什么样，为什么？</p>
          <textarea id="syn-answer" rows="3" placeholder="它读的是……，和目标湿度比一比；差了就……；浇完之后……。如果每次浇得太多，就会……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个情境，这一圈还在不在", TTS["posttest"], [
        {"q": "自动调温的空调把目标设成 26 ℃。下面哪一句正确地说出了它的「比较」这一步？",
         "options": [("拿 26 ℃ 减去当前室温，看看差多少、往哪边差", True),
                     ("看看今天用了多少度电", False),
                     ("把 26 ℃ 直接送给压缩机", False)],
         "explain": "比较就是一减法，算出差值和方向，动作才有依据。"
                    "<strong>错因提醒：</strong>常见错误是把「执行」和「比较」合成一步——"
                    "先算出差值，才谈得上决定怎么动手。"},
        {"q": "一台恒温装置的温度在目标值上下大幅来回跳。下面哪种改法最可能有效？",
         "options": [("把允许误差放宽一点，同时把每次调整的力度调小一些", True),
                     ("把目标值改成一个更大的数", False),
                     ("把允许误差改成 0，要求它一步到位", False)],
         "explain": "要求越苛刻、动作越猛越容易震荡；放宽允许误差、减小力度，曲线就会平下来。"
                    "<strong>错因提醒：</strong>容易误认为「要求提得越严就越准」——"
                    "在只有开和关两档的装置上，过严的要求只会换来更大的摇摆。"},
        {"q": "给花房做自动浇水，哪种做法最稳妥？",
         "options": [("少量多次地浇，浇完再读一次湿度，确认够了就停", True),
                     ("把水泵一直开着，省得来回判断", False),
                     ("把湿度传感器蒙起来，免得它读到数就乱浇水", False)],
         "explain": "少量多次加上「再感知」，湿度就能稳在目标附近；一直开着既费水又会淹根，蒙住传感器等于把眼睛遮上，那样就成了盲动。"
                    "<strong>错因提醒：</strong>常见的错误想法是「动作大才保险」——"
                    "在反馈控制里，动作太大恰恰是震荡的主要原因。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把反馈讲清楚", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>四件事：</strong>定下目标值、读回当前值、比一比差多少、照着差值动手——动手之后还要再读一次。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>比较是一减法：</strong>目标 − 当前 = 差值。正数往上补，接近零就停手，负数往下收；动作的大小由差值决定。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>震荡不是坏了：</strong>要求太苛刻＋动作太猛，就会一冲过头、关掉、掉下来、再冲过头，温度在目标两边来回跳。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>还有一条不该忘的提醒：</strong>做恒温、浇花这类项目时，加热元件会烫、水泵会碰水，一定要在老师指导下接线，湿手不碰电源。机器能替我们一直盯着，但安全这一步，永远得由人把关。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「目标值、读回来、比一比、再动手、再读一次」这五个说法，讲清楚一台空调是怎样把房间稳在 26 ℃ 的。</p>
          <p style="color:var(--muted)">再动一动手：画一个圈，把五步写在圈上，指着圈讲给同桌听。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写出反馈控制的四件事，并说说为什么动手之后还要再读一次。",
            "用自己的话说说：什么情况下装置会在目标两边来回震荡。",
        ],
        [
            "观察家里的空调或者恒温水壶，写出它的目标值是什么、读回来的是什么、拿什么和什么比、动的是什么手。",
            "把它的一圈工作过程画成一个闭环，每步都标上做的什么事。",
        ],
        [
            "给家里的自动浇花器写一份控制方案：目标湿度是多少、每次浇多少、多久看一次，以及怎样避免一会儿干一会儿淹。",
            "再补充一条：如果传感器坏了、读回来的数一直是同一个，装置会怎么表现？你会怎样提醒人及时发现？",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-e-feedback-control",
    "node_id": "it-e-feedback-control",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 小学",
    "title": "反馈控制原理",
    "name_en": "Feedback Control: How Machines Keep Themselves on Target",
    "grade": 6,
    "grade_cn": "六年级",
    "domain": "process-control",
    "domain_cn": "过程与控制",
    "lesson_type": "concept-practice",
    "version": "1.0.0",
    "description": "面向小学六年级：理解反馈在自动控制中的作用，能说出定目标值、读回当前值、比一比、照着差值动手、再读一次这一圈闭环，能解释要求太苛刻加动作太猛会引起震荡，并能给空调、恒温热水器、自动浇花器这类装置写出简单的控制方案。",
    "tags": ["反馈", "闭环", "目标值", "过程与控制", "震荡", "控制方案"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》小学「过程与控制」——理解反馈在自动控制中的作用，设计简单控制方案。",
    "hero_question": "它从来没有一次调到刚刚好——那它凭什么能把温度稳稳守住？",
    "hero_alt": "反馈控制知识结构图：目标值、读回当前值、比一比比出差值、照着差值动手，以及再读一次形成的闭环",
    "hero_caption": "定目标值 · 读回来 · 比一比 · 再动手 · 动手之后还要再读一次——这一圈就是反馈",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的动手活动都会围着它转。",
    "anchor_choices": [
        {"t": "它凭什么能把温度一直稳在一个数上？", "d": "它又没有一次调到刚刚好", "v": "它凭什么能把温度一直稳在一个数上"},
        {"t": "它每一圈到底做了哪几件事？", "d": "想知道那四步分别是什么", "v": "它每一圈到底做了哪几件事"},
        {"t": "为什么会一直在目标两边来回跳？", "d": "是不是机器坏了", "v": "为什么会一直在目标两边来回跳"},
        {"t": "怎样给一台自动浇花器定规矩？", "d": "想自己设计一套控制方案", "v": "怎样给一台自动浇花器定规矩"},
    ],
    "objectives": [
        "能说出反馈控制的四件事：定下目标值、读回当前值、比一比差多少、照着差值动手",
        "能按顺序说出感知、比较、执行、再感知这一圈，并说清为什么动手之后还要再读一次",
        "能解释为什么要求定得太苛刻、每次动手太猛，装置就会在目标两边来回震荡",
        "能给一个生活中的自动控制装置写出它的目标值、读什么、比什么、动什么手",
    ],
    "objectives_plain": [
        "能说出反馈控制的四件事：定下目标值、读回当前值、比一比差多少、照着差值动手",
        "能按顺序说出感知、比较、执行、再感知这一圈，并说清为什么动手之后还要再读一次",
        "能解释为什么要求定得太苛刻、每次动手太猛，装置就会在目标两边来回震荡",
        "能给一个生活中的自动控制装置写出它的目标值、读什么、比什么、动什么手",
    ],
    "standards": [
        {"content": "理解反馈在自动控制中的作用，设计简单控制方案",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 过程与控制"},
        {"content": "在恒温与浇花等真实场景中体验「感知—比较—执行—再感知」的闭环，能根据结果调整参数的严苛程度，并形成安全用电的责任意识",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 过程与控制 / 信息社会责任"},
    ],
    "prereqs": ["it-e-sensors-actuators"],
    "prereqs_name": "传感与执行（初识）",
    "prereqs_meta": "it-e-sensors-actuators",
    "leads_to": ["it-m-iot-concept"],
    "next_meta": "it-m-iot-concept",
    "section_images": ["assets/it-e-feedback-control-fig1.webp", "assets/it-e-feedback-control-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "它从来没有一次调到刚刚好，却能把温度守住——秘密就在那一圈一圈的反馈里。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能给一台装置写出它的一圈反馈是怎么转的。",
        "objectives": "看清四件事：四步分别是什么、为什么还要再读一次、什么时候会震荡、怎么给装置写方案。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "定目标值、读回来、比一比、再动手，最后再读一次——首尾接上才是闭环。",
        "lab-1": "先设目标再换环境，然后点「跑一步」，看着四件事一格一格亮起来。",
        "module-2": "比较就是一减法：目标 − 当前 = 差值。差值决定动作的方向和大小。",
        "lab-2": "三套方案各跑一趟：哪套稳稳贴住目标，哪套来回震荡，哪套怎么跑都够不着。",
        "worked-example": "五步走：定目标、感知、比较、执行，最后别忘了再感知一次。",
        "conceptest-1": "三个说法里都藏着高频错误，选完把解释读一遍。",
        "synthesis": "参数由你定：目标湿度、每次浇多少、天气多干。跑完看曲线，再写一句话解释。",
        "posttest": "空调、来回跳的装置、还有一道安全题，看看这一圈反馈管不管用。",
        "summary": "三句话：四件事、比较是一减法、震荡不是坏了。再记住一条安全提醒。",
        "homework": "三层小任务，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS.replace("__FC_PRESETS_JSON__", json.dumps(FC_PRESETS, ensure_ascii=False)),
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学信息科技「过程与控制」里反馈控制的一课，前置是传感与执行。六年级学生有两处硬骨头：一是把自动控制想成「一次设定就完成」，看不见中间一圈一圈的修正；二是以为「要求定得越准、动作越猛就越好」，不知道这恰恰会造成震荡。所以全课只做三件真能上手的事——先用一台恒温控制器，学生亲手设目标温度、换环境（凉爽窗边 / 普通房间 / 太阳晒着的教室），再点「跑一步」，看读数 → 比较 → 执行 → 再读 四件事一格一格亮起来，温度条上那根橙色目标线让「靠近目标」变成看得见的过程；再用震荡实验室，把「允许误差」和「加热力度」做成滑块，配上稳妥型、苛刻型、保守型三套预设，各跑 16 圈画出温度曲线，让学生亲眼看出三种结局——稳稳贴住、来回跨线震荡、怎么跑都够不着；最后把参数交给学生，自己设计一台自动浇花器的目标湿度和每次浇水量，跑 20 天看曲线。概念页把这一圈收成一句口诀（定目标、读回来、比一比、再动手——动手之后还要再读一次），震荡的原理放在概念二的常见错误里，明确说「不是机器坏了，是要求提得太狠」，安全用电的提醒放在小结页，不写成口号。",
    "plan_table": """| 1 | cover | 反馈控制原理 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：它是怎么把温度稳住的？ | 起·前测（暴露直觉） |
| 5 | concept | 反馈：做完一步，还要回头再看一眼 | 承·概念一（四件事 + 闭环图 + 口诀） |
| 6 | interactive | 动手一：恒温控制器 | 承·动手模拟（设目标值 + 换环境 + 一步一步跑闭环） |
| 7 | concept | 比较就是一减法：差值决定动作的大小 | 承·概念二（差值 + 开/关两档 + 震荡成因） |
| 8 | interactive | 动手二：震荡实验室 | 承·参数实验（三套预设 + 三滑块 + 温度曲线） |
| 9 | concept | 例题示范：把恒温热水器拆成五步 | 转·重难点突破（五步示范 + 纠错） |
| 10 | quiz | 概念测试：三个说法，错在哪里 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：给花房设计自动浇花器 | 合·迁移应用（自定参数跑 20 天 + 方案表述） |
| 12 | quiz | 后测：换几个情境，这一圈还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把反馈讲清楚 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：目标值 / 一圈闭环 / 再读一次 三栏与首尾相接的闭环关系\n- P5 反馈闭环示意图（已生成）：读回当前值 → 和目标比一比 → 照着差值动手 → 再读一次，回到起点\n- P7 两条温度曲线对比图（已生成）：要求合理时稳稳贴住目标线，要求太苛刻、动作太猛时在目标线上下大幅震荡\n- 三张图均为教学示意图，不涉及任何真实设备界面、截图、品牌或商标\n- 若需补充：温度传感器、加热片等实物照片（需获得授权后使用）",
}
