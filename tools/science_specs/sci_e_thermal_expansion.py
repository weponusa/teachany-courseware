# -*- coding: utf-8 -*-
"""小学科学 · 温度与热胀冷缩（G4）—— 补齐课标「能的转化与能量守恒·4.1 能的形式、转移与转化」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/sci-e-thermal-expansion-fig1.webp'
F2 = './assets/sci-e-thermal-expansion-fig2.webp'

TTS = {
    "hero": "先看一件怪事。厨房里有一罐果酱，盖子拧得紧紧的，怎么拧都拧不开。妈妈拿热水把盖子浇了一圈，再一拧，盖子就松了。盖子和瓶子都没换过，为什么浇了热水就能拧开？还有一件事也很奇怪：温度计里的红色液柱，手一握就往上跑，一松开又往下退。这节课我们就弄明白，这两件事背后藏着同一个道理。",
    "problem-anchor": "开始之前，先选一个你最想弄明白的问题。是想知道温度计该怎么看，还是想知道东西为什么一热就变大，又或者你想弄懂怎么用热水帮忙拧开瓶盖。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出温度表示物体的冷热程度，知道它的单位是摄氏度。第二，能正确读出温度计上的度数，知道读数时视线要和液柱的上表面相平。第三，能说出一般物体受热时体积会膨胀、遇冷时体积会收缩。第四，能用热胀冷缩解释生活里的现象，比如瓶盖拧不开、铁轨要留缝隙。",
    "pretest": "先做三道小题，凭你现在的想法选就行，选错了也没关系，正好知道要重点听哪里。选完立刻会出现解释。",
    "module-1": "我们先认识温度。温度是什么？简单说，就是物体的冷热程度。一杯热水和一杯冰水，谁热谁冷，这就是温度在说话。要准确知道温度，光靠手感是不行的，得用温度计。温度的单位叫摄氏度，写作一个圆圈加一个大写字母C。看温度计的时候有个关键动作：视线要和液柱的上表面保持水平。低着头看或者仰着头看，读出来的数都会不准。",
    "lab-1": "现在请你自己练一练读数。下面有一支温度计，上面有刻度。你可以拖动红色液柱，让它升上去或者降下来，看看液柱对准刻度的时候温度是多少。然后点开始出题，它会给你一个温度，请你从三个答案里选出正确的读数。选错了会告诉你错在哪里。",
    "module-2": "再来看热胀冷缩。把铜球放在火上烤一会儿，它就会变大一点点，本来刚好能穿过的铁环，它就过不去了。把铜球放进冷水里凉一凉，它又缩回原来的大小，又能穿过铁环了。科学家发现，一般的物体都有这个脾气：受热的时候体积会膨胀，遇冷的时候体积会收缩。这就叫热胀冷缩。铜球是这样，铁轨是这样，温度计里的液体也是这样。",
    "lab-2": "现在你来当实验员。点按钮给铜球加热，看看它还能不能穿过铁环；再把它放进冷水里冷却，看看它能不能又钻过去。做的时候注意看铜球的颜色和大小有什么变化。然后切换到液体温度计的视角，看看液体受热以后液柱是怎么动的。",
    "worked-example": "我们一起分析一道题。夏天很热的时候，工人师傅为什么要在两段铁轨之间留一道小缝隙？第一步，先想铁轨受热会怎样，铁轨是金属，受热会膨胀变长。第二步，再想不留缝隙会怎样，两段铁轨都变长，就会互相顶住，把铁轨顶弯，火车开过去很危险。第三步，得出结论，留缝隙是为了给铁轨膨胀留出空间。第四步，补充检查，冬天铁轨遇冷收缩，缝隙会变得更大一些，这也是正常的。",
    "conceptest-1": "接下来用三个容易搞混的说法考考你。请仔细读每一个选项，选完再看解释。",
    "synthesis": "学到这里，请你当一次生活小侦探。请你找出家里三个热胀冷缩的例子，每一个都要说清楚：是哪个物体，受热还是遇冷，发生了什么变化。然后解决一个真实的小麻烦——玻璃瓶的金属盖子拧不开，请你写出办法，并说明为什么这个办法管用。",
    "posttest": "最后一轮，用新的情境检验一下。这次会出现温度计的读数、夏天的电线和瘪掉的乒乓球，看看你能不能把学到的规律用上去。",
    "summary": "这节课我们抓住两件事。第一，温度表示物体的冷热程度，用温度计测量，单位是摄氏度。读数的时候视线要和液柱的上表面保持水平，这样读出来才准。第二，一般的物体受热体积膨胀、遇冷体积收缩，这就是热胀冷缩。回到开头那两个问题：瓶盖能拧开，是因为金属盖子受热膨胀得比玻璃多，变得松了；温度计的液柱会上升，是因为里面的液体受热膨胀了。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出温度的单位，并说出温度计读数时视线应该怎么放。第二层能力应用，动手做：用温度计测量一杯温水、一杯常温和一杯冰水的温度，把三次读数记在表格里。第三层迁移挑战，选做：观察家里三个热胀冷缩的现象，写成三行小记录，并试一试能不能用它解决一个小问题。",
    "knowledge-graph": "这张图展示了这节课在科学知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 温度与摄氏度", "lab-1": "实验室一 温度计读数", "module-2": "概念二 热胀冷缩",
    "lab-2": "实验室二 铜球过环", "worked-example": "例题讲解 铁轨的缝隙", "conceptest-1": "概念测试",
    "synthesis": "综合任务 生活小侦探", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

CUSTOM_JS = r"""
/* ============================================================
   sci-e-thermal-expansion 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 温度计读数练习：拖动液柱 + 出题判读（含视线不平的错因提示）
   3) 铜球过环实验：加热膨胀过不去 / 冷却收缩又能通过 + 液体温度计液柱切换
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

  /* ---------- 2. 温度计读数练习 ---------- */
  var stem = document.getElementById('th-liquid');
  if (stem) {
    var range = document.getElementById('th-range');
    var valEl = document.getElementById('th-value');
    var qOut = document.getElementById('th-question');
    var out = document.getElementById('th-out');
    var opts = document.getElementById('th-options');
    var answer = null, locked = false;

    function valueOf() { return Number(range.value); }

    function paint() {
      var v = valueOf();
      // 量程 -20 ~ 110 ℃，映射到液柱高度 0% ~ 100%
      var pct = (v + 20) / 130 * 100;
      stem.style.height = Math.max(2, pct) + '%';
      valEl.textContent = v + ' ℃';
      // 温度越高颜色越暖
      stem.style.background = v < 0 ? '#5aa9e6' : (v < 40 ? '#ff8a5b' : '#e63946');
    }

    function newQuestion() {
      locked = false;
      var v = (Math.floor(Math.random() * 22) - 2) * 5;  // -10 ~ 100，步长 5
      answer = v;
      range.value = String(v);
      paint();
      var wrongs = [v - 5, v + 5];
      if (Math.random() < 0.5) wrongs = [v - 10, v + 10];
      var all = [v, wrongs[0], wrongs[1]].sort(function () { return Math.random() - 0.5; });
      opts.innerHTML = '';
      all.forEach(function (n) {
        var b = document.createElement('button');
        b.className = 'choice';
        b.style.textAlign = 'center';
        b.textContent = n + ' ℃';
        b.addEventListener('click', function () {
          if (locked) return;
          locked = true;
          if (n === answer) {
            b.classList.add('correct');
            out.className = 'result';
            out.innerHTML = '<strong>读对了！</strong>液柱的上表面对准的刻度是 ' + answer +
              ' ℃。记住：读数时视线要和液柱上表面<strong>保持水平</strong>，这样才不会看偏。';
          } else {
            b.classList.add('wrong');
            out.className = 'result error';
            out.innerHTML = '<strong>再仔细看一次刻度。</strong>正确答案是 ' + answer + ' ℃，你选了 ' + n + ' ℃。' +
              '<br><strong>错因提醒：</strong>常见错误是<strong>视线没有和液柱上表面相平</strong>——' +
              '低头俯视读出来会偏大，仰头仰视读出来会偏小。另外，别忘了先看清一小格代表多少摄氏度，再数格数。';
          }
          Array.prototype.forEach.call(opts.children, function (x) { x.disabled = true; });
        });
        opts.appendChild(b);
      });
      qOut.textContent = '请读出这支温度计示数，从下面三个答案里选一个。';
    }

    range.addEventListener('input', paint);
    document.getElementById('th-new').addEventListener('click', newQuestion);
    paint();
    newQuestion();
  }

  /* ---------- 3. 铜球过环实验 ---------- */
  var ring = document.getElementById('ring-stage');
  if (ring) {
    var ball = document.getElementById('ring-ball');
    var out2 = document.getElementById('ring-out');
    var state = 'normal';   // normal | hot | cold
    var mode = 'ball';      // ball | liquid

    function renderRing() {
      if (mode === 'liquid') {
        ball.textContent = '液体';
        ball.style.borderRadius = '10px';
        ball.style.width = '26px';
        ball.style.height = state === 'hot' ? '150px' : (state === 'cold' ? '54px' : '96px');
        ball.style.background = state === 'hot'
          ? 'linear-gradient(180deg,#ff8a5b,#e63946)'
          : 'linear-gradient(180deg,#ff8a5b,#f4a261)';
        ball.style.top = '54%';
      } else {
        ball.textContent = state === 'hot' ? '热铜球' : (state === 'cold' ? '冷铜球' : '铜球');
        ball.style.borderRadius = '50%';
        var size = state === 'hot' ? 96 : (state === 'cold' ? 68 : 78);
        ball.style.width = size + 'px';
        ball.style.height = size + 'px';
        ball.style.background = state === 'hot'
          ? 'radial-gradient(circle at 34% 30%,#ffd166,#e63946)'
          : 'radial-gradient(circle at 34% 30%,#f0c090,#b87333)';
        ball.style.top = state === 'hot' ? '50%' : (state === 'cold' ? '60%' : '57%');
      }

      var text;
      if (mode === 'liquid') {
        if (state === 'hot') {
          text = '<strong>液体受热 → 液柱上升。</strong>温度计里的液体受热膨胀，体积变大，只能沿着细细的玻璃管往上爬。这就是温度计能工作的秘密。';
        } else if (state === 'cold') {
          text = '<strong>液体遇冷 → 液柱下降。</strong>液体遇冷收缩，体积变小，液柱就退回去了。所以温度计的液柱会随着温度变化而升降。';
        } else {
          text = '现在液体处于常温，液柱停在中间的位置。点按钮给它加热或者降温，看看液柱怎么变。';
        }
        out2.className = 'result' + (state === 'normal' ? ' warn' : '');
      } else {
        if (state === 'hot') {
          text = '<strong>铜球受热膨胀，过不去了！</strong>铜球被烤热以后体积变大，比铁环的孔还大，卡在环的上面。这说明物体受热时体积会膨胀。';
          out2.className = 'result error';
        } else if (state === 'cold') {
          text = '<strong>铜球遇冷收缩，又能穿过去了！</strong>放进冷水以后，铜球的体积缩小回原来的大小，顺利通过铁环。说明物体遇冷时体积会收缩。';
          out2.className = 'result';
        } else {
          text = '现在铜球是常温的，刚好能穿过铁环。先点加热，再点冷却，对比两次的结果。';
          out2.className = 'result warn';
        }
      }
      out2.innerHTML = text;
    }

    document.getElementById('ring-heat').addEventListener('click', function () { state = 'hot'; renderRing(); });
    document.getElementById('ring-cool').addEventListener('click', function () { state = 'cold'; renderRing(); });
    document.getElementById('ring-reset').addEventListener('click', function () { state = 'normal'; renderRing(); });
    document.getElementById('ring-mode').addEventListener('click', function () {
      mode = mode === 'ball' ? 'liquid' : 'ball';
      state = 'normal';
      document.getElementById('ring-mode').textContent = mode === 'ball'
        ? '切换：看液体温度计的液柱' : '切换：看铜球过环实验';
      document.getElementById('ring-loop').style.display = mode === 'ball' ? 'block' : 'none';
      renderRing();
    });
    renderRing();
  }
})();
"""

# 温度计刻度（每 10 ℃ 一条长刻度，0 与 100 加粗）
TICKS = []
for _t in range(-20, 111, 10):
    _pct = (_t + 20) / 130 * 100
    _strong = _t in (0, 100)
    TICKS.append(
        f'<div style="position:absolute;left:0;right:0;bottom:{_pct:.2f}%;height:0;'
        f'border-top:{"3px solid #8d9bb5" if _strong else "1px solid #cfd8e3"}">'
        f'<span style="position:absolute;left:2px;top:-11px;font-size:11px;'
        f'color:{"#3a3126" if _strong else "#94866c"};font-weight:{"800" if _strong else "400"}">{_t}</span></div>'
    )
TICKS_HTML = "\n            ".join(TICKS)


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：温度该怎么量？", TTS["pretest"], [
        {"q": "要知道一杯水有多热，下面哪种做法最可靠？",
         "options": [("用温度计测量，读出它的摄氏度", True),
                     ("用手摸一摸，凭感觉判断", False),
                     ("看一看水面上有没有冒气", False)],
         "explain": "温度计能给出准确的度数，手感会被很多东西干扰。<strong>错因提醒：</strong>很多同学误认为手的感觉很准，其实同一杯温水，左手刚从冰水里拿出来会觉得它烫，右手刚从热水里拿出来又觉得它凉——所以不能只靠感觉。"},
        {"q": "读温度计时，视线应该怎么放？",
         "options": [("和液柱的上表面保持水平", True),
                     ("从上往下俯视读数", False),
                     ("从下往上仰视读数", False)],
         "explain": "视线与液柱上表面相平时读数才准确。<strong>错因提醒：</strong>俯视会让读数偏大，仰视会让读数偏小，这是读数时最常见的错误，注意不要跟看量筒的方法搞混。"},
        {"q": "把一壶水烧开，水的温度升高，水的体积会：",
         "options": [("变大一点点，所以水会有点溢出来", True),
                     ("变小一点点", False),
                     ("完全不变化", False)],
         "explain": "一般物体受热体积会膨胀，水也是一样。<strong>错因提醒：</strong>这个现象很容易被忽略。注意水和大多数物体一样是热胀冷缩，但水结成冰时体积反而会变大，这是一个特别的例外。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "温度表示物体的冷热程度，用摄氏度作单位", TTS["module-1"], f'''
        <p style="font-size:17px;margin:0 0 12px"><strong>温度</strong>就是物体的冷热程度。要把它量出来，需要用<strong>温度计</strong>，单位是<strong>摄氏度</strong>，写作 ℃。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>怎么看刻度</strong></p>
            <p style="color:var(--muted)">先看清一小格代表多少摄氏度，再从液柱上表面所在的位置数出格数。</p>
          </div>
          <div class="inner-card">
            <p><strong>视线怎么放</strong></p>
            <p style="color:var(--muted)">视线要和液柱的上表面<strong>保持水平</strong>，俯视偏大、仰视偏小。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="温度计刻度读数示意图：摄氏度刻度、液柱与平视读数方法">
          <figcaption>温度计上的数字就是摄氏度；读数时视线与液柱上表面相平，才能读出准确的度数</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🌡️</span><div><strong>一句口诀记住它：</strong>温度看冷热，单位摄氏度；读数要平视，数清一小格。另外要记住 0 ℃ 是水结冰的温度，100 ℃ 是水沸腾的温度。</div></div>
{insight_box([
    {"lens": "看见它", "text": "体温计、气温计、厨房用的探针温度计，刻度范围各不相同，但读数的方法完全一样：平视液柱上表面。"},
    {"lens": "比较它", "text": "温度计和尺子有点像：尺子量长度，温度计量冷热。它们都要先看清一小格代表多少，再数格数。"},
    {"lens": "迁移它", "text": "气象站每天记录的空气温度、冰箱冷藏室的 4 ℃、发烧时的 38 ℃，都是同一个单位在说话。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "温度计读数台：拖一拖、读一读", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先拖动滑块，让红色液柱升上去、降下来，看看刻度怎么对准。然后点出题，检验一下你能不能读准。</p>
        <div class="lab-panel">
          <div class="lab-stage" id="th-stage" style="height:290px;background:linear-gradient(180deg,#f7fbff 0%,#eaf6ff 100%)">
            <div style="position:absolute;left:50%;transform:translateX(-50%);top:12px;bottom:12px;width:64px;border-radius:10px;background:#fff;border:2px solid #cfd8e3"></div>
            <div id="th-scale" style="position:absolute;left:50%;transform:translateX(-50%);bottom:12px;top:12px;width:64px;margin-left:6px">
            {TICKS_HTML}
            </div>
            <div style="position:absolute;left:50%;transform:translateX(-50%);top:12px;bottom:12px;width:18px;border-radius:9px;background:#eef4fb;border:1px solid #d8e3ee"></div>
            <div id="th-liquid" style="position:absolute;left:50%;transform:translateX(-50%);bottom:12px;width:18px;border-radius:9px;background:#ff8a5b;height:50%;transition:height .12s linear,background .3s"></div>
            <div style="position:absolute;left:calc(50% + 96px);top:14px;font-size:14px;color:#94866c">温度计示数</div>
            <div style="position:absolute;left:calc(50% + 96px);top:38px;font-size:26px;font-weight:800;color:#e05555" id="th-value">45 ℃</div>
          </div>
          <div class="slider-row">
            <label for="th-range">拖动液柱</label>
            <input type="range" id="th-range" min="-20" max="110" step="5" value="45" style="flex:1;min-width:160px">
          </div>
          <div class="flex-row">
            <button class="choice" id="th-new" style="text-align:center">开始出题，我来读</button>
          </div>
          <p class="result warn" id="th-question" style="margin-top:12px">请读出这支温度计示数，从下面三个答案里选一个。</p>
          <div class="grid grid-3" id="th-options" style="margin-top:10px"></div>
          <p class="result warn" id="th-out" style="margin-top:12px">选完答案会立刻告诉你对不对，还会指出错在哪里。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">⚠️</span><div><strong>安全提示：</strong>真实实验里，测量热水温度要由老师操作，小心烫伤。温度计是玻璃做的，容易碎，千万不要拿它当搅拌棒用。实验室里的实验一律使用电池或专用电源，<strong>不要用家用插座做实验</strong>。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "一般物体受热体积膨胀，遇冷体积收缩", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">把铜球烤一烤，它就从铁环里过不去了；把它放进冷水凉一凉，又能钻过去。这个变化有个名字，叫<strong>热胀冷缩</strong>：受热膨胀，遇冷收缩。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div>铜球在常温下刚好能穿过铁环。</div></div>
          <div class="step"><span class="n">2</span><div>用火加热铜球，铜球温度升高，<strong>体积膨胀</strong>，比铁环的孔还大，卡住了。</div></div>
          <div class="step"><span class="n green">3</span><div>把铜球放进冷水，温度降低，<strong>体积收缩</strong>回到原样，又能穿过铁环。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="铜球过环实验：加热后的铜球体积膨胀，卡在铁环上过不去">
          <figcaption>同一个铜球，同一个铁环：受热的铜球膨大了过不去，冷却后又恢复原样，顺利通过</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">特别注意</span>
          <p style="margin:6px 0 0">水结冰是个例外：水结成冰以后体积反而<strong>变大</strong>。所以装满水的玻璃瓶放进冰箱冷冻会撑裂。不要误认为所有情况都严格是热胀冷缩，遇到水要多想一步。</p>
        </div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "铜球过环：加热过不去，冷却又能过", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点加热，看看铜球还能不能穿过铁环；再点冷却，看看它能不能又钻过去。最后切换到液体温度计，看看液柱是怎么动的。</p>
        <div class="lab-panel">
          <div class="lab-stage" id="ring-stage" style="height:270px;background:linear-gradient(180deg,#fdfaf3 0%,#f6efe0 100%)">
            <div id="ring-loop" style="position:absolute;left:50%;top:62%;transform:translate(-50%,-50%);width:150px;height:150px;border-radius:50%;border:16px solid #b8c4d4;box-shadow:inset 0 4px 10px rgba(0,0,0,.08)"></div>
            <div style="position:absolute;left:50%;top:calc(62% + 84px);transform:translateX(-50%);font-size:13px;color:#94866c">铁环</div>
            <div id="ring-ball" style="position:absolute;left:50%;transform:translate(-50%,-50%);width:78px;height:78px;border-radius:50%;background:radial-gradient(circle at 34% 30%,#f0c090,#b87333);display:grid;place-items:center;color:#fff;font-weight:800;font-size:13px;transition:all .6s cubic-bezier(.34,1.2,.5,1)">铜球</div>
          </div>
          <div class="flex-row">
            <button class="choice" id="ring-heat" style="text-align:center">🔥 用酒精灯加热铜球</button>
            <button class="choice" id="ring-cool" style="text-align:center">💧 放进冷水冷却</button>
            <button class="choice" id="ring-reset" style="text-align:center">重置</button>
          </div>
          <div class="flex-row">
            <button class="choice" id="ring-mode" style="text-align:center;flex:1">切换：看液体温度计的液柱</button>
          </div>
          <p class="result warn" id="ring-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔥</span><div><strong>安全提示：</strong>做这个实验要戴护目镜，加热后的铜球非常烫，<strong>绝对不能用手摸</strong>，要用夹子夹。酒精灯要用灯帽盖灭，不能用嘴吹。家里不要自己点火做实验，请由老师操作。用电器一律使用电池，<strong>不要用家用插座做实验</strong>。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：铁轨之间为什么要留一道缝？", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>工人铺铁轨的时候，会在两段铁轨之间留一道小小的缝隙。这是为什么？请说明理由。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看材料：</strong>铁轨是金属做的，金属有明显的受热膨胀、遇冷收缩的性质。</div></div>
          <div class="step"><span class="n">2</span><div><strong>想后果：</strong>夏天太阳晒得很热，铁轨会膨胀变长；如果不留缝隙，两段铁轨就会互相顶住。</div></div>
          <div class="step"><span class="n">3</span><div><strong>下结论：</strong>留缝隙是为了给铁轨的膨胀留出空间，防止铁轨被顶弯。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>再检查：</strong>冬天铁轨遇冷收缩，缝隙会比夏天大一些，这说明规律在两头都成立。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错法</span>
          <p style="margin:6px 0 0">有同学写成是为了让火车开过去时有声音，或者误认为是铁轨没铺好、留错了。这都是没有抓住<strong>热胀冷缩</strong>这个原因。以后遇到铺铁轨、架电线、装玻璃窗这类题目，第一反应就该想到热胀冷缩。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "下面哪句话是正确的？",
         "options": [("一般物体受热体积膨胀，遇冷体积收缩", True),
                     ("物体受热以后重量变大了", False),
                     ("物体受热以后质量变大了", False)],
         "explain": "热胀冷缩改变的是<strong>体积</strong>，不是轻重。<strong>错因提醒：</strong>很多同学把体积和重量搞混了——铜球烤过以后还是同一个铜球，它没有变重，只是胀大了一点点。"},
        {"q": "关于温度计，下面说法正确的是：",
         "options": [("温度计里的液体受热膨胀，液柱就升高", True),
                     ("温度计里的液体受热以后会变成气体跑出来", False),
                     ("液柱升高是因为玻璃管被撑长了", False)],
         "explain": "液柱升高是液体受热膨胀的结果，玻璃管本身几乎不变。<strong>错因提醒：</strong>常见错误是误认为玻璃管变长了。真正发生变化的是里面的液体，玻璃管只是一个细细的容器。"},
        {"q": "夏天架设电线时，工人会把电线放得松一些。这是因为：",
         "options": [("冬天电线遇冷收缩会绷紧，留出余量才安全", True),
                     ("松一点的电线看起来更好看", False),
                     ("电线变长了就不导电了", False)],
         "explain": "冬天电线收缩变短，如果夏天绷得太紧，冬天就可能被拉断。<strong>错因提醒：</strong>容易搞混的是方向——这里要预防的是<strong>冬天收缩</strong>，所以要在夏天留出余量。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：当一次生活小侦探", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">请你找出家里三个热胀冷缩的例子，再解决一个真实的小麻烦：玻璃瓶的金属盖拧不开。</p>
        <div class="inner-card">
          <p><strong>第一步：找出三个例子</strong></p>
          <textarea id="syn-cases" rows="3" placeholder="例 1：＿＿＿＿受热／遇冷，体积＿＿＿＿&#10;例 2：＿＿＿＿&#10;例 3：＿＿＿＿"></textarea>
        </div>
        <div class="inner-card">
          <p><strong>第二步：解决瓶盖拧不开的麻烦</strong></p>
          <p style="color:var(--muted)">写出你的办法，并说清楚道理：是谁膨胀了？为什么膨胀以后盖子就松了？</p>
          <textarea id="syn-solve" rows="3" placeholder="我的办法是……道理是：金属盖子受热膨胀比玻璃＿＿＿＿，所以……"></textarea>
        </div>
        <div class="inner-card">
          <p><strong>第三步：说给同桌听</strong></p>
          <p style="color:var(--muted)">用「温度、膨胀、收缩」这三个词，把上面两个任务连起来讲一遍。</p>
        </div>
        <div class="kid-note"><span class="emoji">⚠️</span><div><strong>安全提示：</strong>想用热水浇瓶盖，请让家长帮忙，水温不要太高，避免烫伤。任何加热的实验都不要自己在家用明火做。</div></div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换个情境，规律还在不在", TTS["posttest"], [
        {"q": "体温计上的示数是 36.8 ℃，它表示：",
         "options": [("人的体温是 36.8 摄氏度", True), ("人的体温是 36.8 千克", False), ("人的体温是 36.8 米", False)],
         "explain": "摄氏度的符号是 ℃，读作摄氏度，它是温度的单位。<strong>错因提醒：</strong>常见错误是把单位搞混，℃ 既不是质量单位也不是长度单位。"},
        {"q": "一个乒乓球被压瘪了，把它放进热水里，它又鼓了起来。原因是：",
         "options": [("球里的空气受热膨胀，把球顶回了原样", True),
                     ("乒乓球的外壳受热变软了，自己弹回来", False),
                     ("热水把球里的空气吸走了", False)],
         "explain": "球内空气受热膨胀，把瘪下去的地方顶了起来。<strong>错因提醒：</strong>很多同学误认为只是外壳变软，其实起主要作用的是<strong>球里的空气膨胀</strong>。如果球破了一个小洞，这个方法就不管用了。"},
        {"q": "把装满水的塑料瓶放进冷冻室，瓶子可能会被撑变形。这是因为：",
         "options": [("水结成冰以后体积会变大", True),
                     ("水结成冰以后变重了", False),
                     ("冷冻室里的空气挤破了瓶子", False)],
         "explain": "水结冰时体积会膨胀，所以装满水的瓶子容易被撑坏。<strong>错因提醒：</strong>这是热胀冷缩最容易被搞混的例外——水在结冰时是<strong>逆着</strong>来的，体积反而变大。所以瓶里装水不要装太满再冷冻。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：两句话，把温度和热胀冷缩讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>温度</strong>：表示物体的冷热程度，用温度计测量，单位是<strong>摄氏度</strong>（℃）。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>读数</strong>：视线和液柱上表面<strong>保持水平</strong>；俯视偏大，仰视偏小。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>热胀冷缩</strong>：一般物体受热体积<strong>膨胀</strong>，遇冷体积<strong>收缩</strong>。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>例外</strong>：水结成冰时体积反而变大，装满水的瓶子冷冻会撑裂。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那两个问题：</strong>瓶盖能拧开，是因为金属盖子受热膨胀，比玻璃瓶胀得多一点，于是松了；温度计的液柱会升降，是因为里面的液体受热膨胀、遇冷收缩。两件事用的是同一条规律。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「温度、膨胀、收缩」这三个词，说清楚铁轨为什么要留缝隙。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "写出温度的单位，并说出温度计读数时视线应该怎么放。",
            "用一句话写出什么是热胀冷缩，并举出一个例子。",
        ],
        [
            "用温度计测量一杯温水、一杯常温水、一杯冰水的温度，把三次读数记在表格里。",
            "把瘪掉的乒乓球放进热水，记录它的变化，并说明原因。",
        ],
        [
            "观察家里三个热胀冷缩的现象，各写一行记录，说明是哪个物体、受热还是遇冷、发生了什么变化。",
            "设计一个办法，把拧不开的玻璃瓶金属盖子打开，写出做法和道理，并在家长陪同下试一试。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "sci-e-thermal-expansion",
    "node_id": "sci-e-thermal-expansion",
    "title": "温度与热胀冷缩：物体为什么会变胖",
    "name_en": "Temperature and Thermal Expansion",
    "grade": 4,
    "grade_cn": "四年级",
    "domain": "matter-science",
    "domain_cn": "物质科学 · 热与能量",
    "lesson_type": "experiment-inquiry",
    "version": "1.0.0",
    "description": "认识温度与摄氏度，学会用平视液柱上表面的方法读温度计；通过铜球过环实验发现一般物体受热体积膨胀、遇冷体积收缩，并用水结冰这个例外解释生活中的热胀冷缩现象。",
    "tags": ["温度", "摄氏度", "温度计读数", "热胀冷缩", "铜球过环", "铁轨的缝隙"],
    "standard_ref": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念4「能的转化与能量守恒」学习内容4.1 能的形式、转移与转化——3～4年级描述测量物体温度的方法，知道摄氏度；知道热胀冷缩的性质及其应用。",
    "hero_question": "浇了热水，拧不开的瓶盖为什么就松了？温度计里的液柱为什么会自己升降？",
    "hero_alt": "温度与热胀冷缩知识结构图：温度与摄氏度、受热膨胀、遇冷收缩",
    "hero_caption": "温度：表示冷热程度 · 单位摄氏度 · 读数要平视 ｜ 热胀冷缩：一般物体受热膨胀、遇冷收缩",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的实验都会围着它转。",
    "anchor_choices": [
        {"t": "温度计该怎么看？", "d": "想知道怎样读出准确的度数", "v": "温度计该怎么看"},
        {"t": "物体为什么一热就变大？", "d": "想知道热胀冷缩是怎么回事", "v": "物体为什么一热就变大"},
        {"t": "瓶盖浇了热水怎么就不紧了？", "d": "想弄懂一个厨房里的窍门", "v": "瓶盖浇了热水怎么就不紧了"},
        {"t": "铁轨为什么不能接得严丝合缝？", "d": "想知道工程师为什么要留缝隙", "v": "铁轨为什么不能接得严丝合缝"},
    ],
    "objectives": [
        "能说出温度表示物体的冷热程度，知道温度的单位是摄氏度",
        "能正确读出温度计的示数，知道读数时视线要与液柱上表面相平",
        "能说出一般物体受热体积膨胀、遇冷体积收缩，并用它解释身边的现象",
        "知道水结成冰体积反而变大，能举例说明热胀冷缩的应用",
    ],
    "objectives_plain": [
        "能说出温度表示物体的冷热程度，知道温度的单位是摄氏度",
        "能正确读出温度计的示数，知道读数时视线要与液柱上表面相平",
        "能说出一般物体受热体积膨胀、遇冷体积收缩，并用它解释身边的现象",
        "知道水结成冰体积反而变大，能举例说明热胀冷缩的应用",
    ],
    "standards": [
        {"content": "描述测量物体温度的方法，知道温度的单位是摄氏度，能正确使用温度计读数",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念4 能的转化与能量守恒·4.1 能的形式、转移与转化（3～4年级）"},
        {"content": "知道物体具有热胀冷缩的性质，能举例说明它在生活中的应用",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念4 能的转化与能量守恒·4.1 能的形式、转移与转化（3～4年级）"},
    ],
    "prereqs": ["sci-e-solid-liquid-gas"],
    "prereqs_name": "物质的三态与变化",
    "prereqs_meta": "sci-e-solid-liquid-gas",
    "leads_to": ["sci-e-heat-transfer"],
    "next_meta": "sci-e-heat-transfer",
    "section_images": ["assets/sci-e-thermal-expansion-fig1.webp", "assets/sci-e-thermal-expansion-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "瓶盖浇热水就松了，温度计液柱自己会动——两件怪事，同一条规律。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能读准温度计，还能用热胀冷缩解释生活现象。",
        "objectives": "看清四件事：温度与摄氏度、平视读数、热胀冷缩、水结冰这个例外。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "温度量的是冷热，单位是摄氏度；读数时视线一定和液柱上表面相平。",
        "lab-1": "先拖液柱找感觉，再点出题。读出格数前，先看清一小格代表多少摄氏度。",
        "module-2": "受热膨胀、遇冷收缩，铜球就是最好的证据——它连铁环都过不去了。",
        "lab-2": "加热看它卡住，冷却看它通过，最后切到液体温度计看液柱怎么动。",
        "worked-example": "四步走：看材料、想后果、下结论、再检查。关键是抓住热胀冷缩。",
        "conceptest-1": "干扰项里藏着最常见的那几个错误想法，选完看清每一个解释。",
        "synthesis": "先找三个例子，再想清楚：到底是哪个部分膨胀了，盖子才松的？",
        "posttest": "换了体温计、乒乓球和冷冻瓶子的新情境，看看你还能不能用上同一条规律。",
        "summary": "回到开头那两个问题：它们背后是同一条规律，你能说清是哪一条吗？",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是「能的形式、转移与转化」在小学中段的空缺：知识树原有物质的三态与变化、热的传递，缺课标明确要求的温度测量与热胀冷缩。设计上把温度落到一个可以反复练的动作——平视液柱上表面读数，并给出俯视偏大、仰视偏小的具体错因；再把热胀冷缩收敛为铜球过环这一个可观察的证据，最后用铁轨、电线、瓶盖、乒乓球四个真实情境收束。",
    "plan_table": """| 1 | cover | 温度与热胀冷缩：物体为什么会变胖 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：温度该怎么量？ | 起·前测（暴露直觉） |
| 5 | concept | 温度表示物体的冷热程度，用摄氏度作单位 | 承·概念一（含读数方法） |
| 6 | interactive | 温度计读数台：拖一拖、读一读 | 承·实验室一（拖液柱 + 判读反馈） |
| 7 | concept | 一般物体受热体积膨胀，遇冷体积收缩 | 承·概念二（含水的例外） |
| 8 | interactive | 铜球过环：加热过不去，冷却又能过 | 承·实验室二（加热/冷却对比） |
| 9 | concept | 例题示范：铁轨之间为什么要留一道缝？ | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：当一次生活小侦探 | 合·迁移应用 |
| 12 | quiz | 后测：换个情境，规律还在不在 | 合·后测 |
| 13 | summary | 小结：两句话，把温度和热胀冷缩讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：温度与摄氏度、受热膨胀、遇冷收缩三栏标注\n- P5 温度计读数图（已生成）：摄氏度刻度、液柱与平视读数方法中文标注\n- P7 铜球过环实验图（已生成）：加热后的铜球膨胀卡在铁环上\n- 若需补充：真实温度计读数特写、铁轨缝隙与电线弧垂的实景照片",
}
