# -*- coding: utf-8 -*-
"""小学科学 · 浮力与物体的沉浮（G5）—— 补齐课标「物质的运动与相互作用·3.1 力」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/sci-e-buoyancy-fig1.webp'
F2 = './assets/sci-e-buoyancy-fig2.webp'

TTS = {
    "hero": "先问你一个问题。一艘十几万吨的大轮船，是钢铁造的，却能稳稳浮在海面上；一颗小小的石子，一松手就沉到水底。同样是水，为什么有的东西浮起来，有的东西沉下去？这节课我们就用实验把这件事弄明白。",
    "problem-anchor": "在开始之前，先选出你最想弄明白的那个问题。是想知道浮力到底从哪里来，还是想知道什么决定了一个物体是沉是浮，又或者你想亲手设计一艘能装很多货物的船。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出浮力是什么，知道它的方向是向上的。第二，能用弹簧测力计测出浮力的大小。第三，能说出浮力的大小和物体排开多少水有关。第四，能解释为什么钢铁轮船能浮在水面上。",
    "pretest": "先做三道小题，凭你现在的想法选就行，选错了也没关系，正好能看出哪里需要重点听。选完会立刻出现解释。",
    "module-1": "把一块木块按进水里，松开手，它会自己弹上来。是谁在往上托它？是水。物体浸在水里的时候，水会从下往上托住它，这个向上的托力就叫浮力。要注意两件事：第一，浮力的方向永远竖直向上；第二，不只是水，油、盐水，甚至空气，都会给浸在里面的物体一个向上的浮力。",
    "lab-1": "光说有浮力还不够，我们把它量出来。把物体挂在弹簧测力计下面，先在空气中读一次数，再让它浸进水里读一次数。你会发现水里的读数变小了，变小的那部分，就是水向上托的浮力。现在自己动手试三种物体，看看它们的浮力各是多少。",
    "module-2": "浮力的大小和什么有关？把同一个物体浸进水里，浸进去越多，读数变得越小，说明浮力越大。再换一个更小的物体，即使全部浸没，读数变化也比大物体小。科学家阿基米德发现：物体受到浮力的大小，等于它排开的那部分水受到的重力。物体排开的水越多，浮力就越大。",
    "lab-2": "现在你可以自己控制变量了。左边选液体，右边选物体的材料，看看谁浮谁沉。玩之前先想一个问题：决定沉浮的，到底是物体有多重，还是物体和液体谁更密实？试几组，你会发现规律的。",
    "worked-example": "我们一起来分析一道题。同样是体积为一百立方厘米的铝块和木块，放进水里，谁会沉，谁会浮？第一步，看清条件：体积相同，材料不同。第二步，比较密度：铝的密度大约是水的二点七倍，木头的密度大约只有水的一半。第三步，判断：密度比水大的铝块下沉，密度比水小的木块漂浮。第四步，想为什么：铝块把它那一百立方厘米的水排开，排开的水比它自己轻，托不住它；木块只排开一部分水，排开的水的重力正好等于木块的重力，就浮住了。",
    "conceptest-1": "现在用三个容易弄错的说法考考你。请仔细读每一个选项，选出你认为正确的那个，然后看解释。",
    "synthesis": "学到这里，请你当一次工程师。给你一张同样大小的铝箔，把它团成一个球，放进水里会立刻沉下去；把它折成一只小船，就能浮起来，还能放上好多枚硬币。请你动手试一试，再想一想：为什么同样重的铝箔，做成小船就能装货物？",
    "posttest": "最后用新情境检验一下。这次的问题里出现了盐水和潜水艇，看看你能不能把学到的规律用上去。",
    "summary": "这节课我们弄明白了三件事。第一，浸在水里的物体会受到竖直向上的浮力。第二，浮力的大小等于物体排开的水受到的重力，排开的水越多，浮力越大。第三，物体和液体比密实程度：物体比液体密实就下沉，比液体松散就漂浮，一样就悬浮。回到开头的问题，钢铁轮船能浮起来，是因为它做成了空心的形状，排开了非常多水，得到的浮力足够托住整艘船。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出浮力的方向，并解释为什么沉在水底的石子也受到浮力。第二层能力应用，动手做：用弹簧测力计测一个物体在水中的浮力，把两次读数记下来。第三层迁移挑战，选做：用一张铝箔设计一艘能装十枚硬币的船，画出你的设计图并说明道理。",
    "knowledge-graph": "这张图展示了这节课在科学知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 浮力从哪里来", "lab-1": "实验室一 量浮力", "module-2": "概念二 浮力有多大",
    "lab-2": "实验室二 沉浮实验室", "worked-example": "例题讲解", "conceptest-1": "概念测试",
    "synthesis": "综合任务 铝箔船", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

CUSTOM_JS = r"""
/* ============================================================
   sci-e-buoyancy 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 弹簧测力计实验室：空气中读数 vs 水中读数 → 浮力
   3) 沉浮实验室：液体密度 × 物体密度 → 浮 / 悬浮 / 沉
   4) 铝箔船载货模型
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

  /* ---------- 2. 弹簧测力计实验室 ---------- */
  var OBJ = {
    hook:  { name: '钩码',   air: 2.0, water: 1.2, color: '#8d9bb5', w: 46, h: 46, txt: '200g' },
    wood:  { name: '木块',   air: 1.0, water: 0.5, color: '#c99a5b', w: 56, h: 40, txt: '木' },
    foam:  { name: '泡沫块', air: 0.4, water: 0.0, color: '#ffd166', w: 60, h: 44, txt: '泡' }
  };
  var stage1 = document.getElementById('lab1-stage');
  if (stage1) {
    var objEl = document.getElementById('lab1-obj');
    var cur = 'hook', inWater = false;
    var vAir = document.getElementById('r-air');
    var vWater = document.getElementById('r-water');
    var vBuoy = document.getElementById('r-buoy');
    var verdict = document.getElementById('lab1-verdict');

    function render1() {
      var o = OBJ[cur];
      objEl.style.width = o.w + 'px';
      objEl.style.height = o.h + 'px';
      objEl.style.background = o.color;
      objEl.textContent = o.txt;
      objEl.style.top = inWater ? '72%' : '16%';
      vAir.textContent = o.air.toFixed(1) + ' N';
      if (inWater) {
        var rd = o.water;
        vWater.textContent = rd.toFixed(1) + ' N';
        var buoy = o.air - rd;
        vBuoy.textContent = buoy.toFixed(1) + ' N';
        verdict.style.display = 'block';
        verdict.className = 'result' + (buoy < 0.35 ? ' warn' : '');
        verdict.innerHTML = buoy < 0.35
          ? '<strong>注意：</strong>' + o.name + '在水里受到的浮力刚好等于它的重量，所以它不上不下地停在水里，其实是<strong>漂浮/悬浮</strong>——弹簧测力计几乎读不到数了。'
          : '<strong>读数变小的 0.1 牛的差值，就是水向上托的浮力。</strong>' + o.name + '受到的浮力是 ' + buoy.toFixed(1) + ' 牛。';
      } else {
        vWater.textContent = '— —';
        vBuoy.textContent = '— —';
        verdict.style.display = 'block';
        verdict.className = 'result warn';
        verdict.textContent = '现在物体还挂在空气里，点下面的按钮把它放进水里，看看读数会怎么变。';
      }
      document.querySelectorAll('[data-lab1-obj]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.lab1Obj === cur);
      });
      var tb = document.getElementById('lab1-toggle');
      tb.textContent = inWater ? '把物体提离水面' : '把物体放进水里';
    }
    document.querySelectorAll('[data-lab1-obj]').forEach(function (b) {
      b.addEventListener('click', function () { cur = b.dataset.lab1Obj; render1(); });
    });
    document.getElementById('lab1-toggle').addEventListener('click', function () {
      inWater = !inWater; render1();
    });
    render1();
  }

  /* ---------- 3. 沉浮实验室 ---------- */
  var LIQ = { oil: { n: '食用油', d: 0.92 }, water: { n: '清水', d: 1.00 }, brine: { n: '浓盐水', d: 1.15 } };
  var MAT = { wood: { n: '木块', d: 0.6, c: '#c99a5b' }, plastic: { n: '塑料块', d: 0.95, c: '#7fc8f8' }, alu: { n: '铝块', d: 2.7, c: '#8d9bb5' } };
  var stage2 = document.getElementById('lab2-stage');
  if (stage2) {
    var boxEl = document.getElementById('lab2-obj');
    var liq = 'water', mat = 'wood';
    var vOut = document.getElementById('lab2-verdict');

    function render2() {
      var L = LIQ[liq], M = MAT[mat];
      boxEl.style.background = M.c;
      boxEl.textContent = M.n;
      boxEl.style.width = '74px';
      boxEl.style.height = '54px';
      var state, top, msg;
      if (M.d < L.d - 0.02) {
        state = '漂浮'; top = '26%';
        msg = M.n + '的密度约 ' + M.d + '，比' + L.n + '的 ' + L.d + ' 小，所以它<strong>浮在液面上</strong>，只排开一部分液体。';
      } else if (Math.abs(M.d - L.d) <= 0.06) {
        state = '悬浮'; top = '62%';
        msg = M.n + '的密度约 ' + M.d + '，和' + L.n + '的 ' + L.d + ' 差不多，所以它<strong>悬浮</strong>在液体中间。';
      } else {
        state = '下沉'; top = '80%';
        msg = M.n + '的密度约 ' + M.d + '，比' + L.n + '的 ' + L.d + ' 大，排开的水托不住它，所以它<strong>沉到底部</strong>。';
      }
      boxEl.style.top = top;
      var color = state === '下沉' ? 'error' : (state === '悬浮' ? 'warn' : '');
      vOut.className = 'result ' + color;
      vOut.innerHTML = '<strong>' + M.n + ' 放进 ' + L.n + ' → ' + state + '</strong><br>' + msg;
      document.querySelectorAll('[data-lab2-liq]').forEach(function (b) { b.classList.toggle('selected', b.dataset.lab2Liq === liq); });
      document.querySelectorAll('[data-lab2-mat]').forEach(function (b) { b.classList.toggle('selected', b.dataset.lab2Mat === mat); });
    }
    document.querySelectorAll('[data-lab2-liq]').forEach(function (b) {
      b.addEventListener('click', function () { liq = b.dataset.lab2Liq; render2(); });
    });
    document.querySelectorAll('[data-lab2-mat]').forEach(function (b) {
      b.addEventListener('click', function () { mat = b.dataset.lab2Mat; render2(); });
    });
    render2();
  }

  /* ---------- 4. 铝箔船载货 ---------- */
  var shipStage = document.getElementById('ship-stage');
  if (shipStage) {
    var shapes = {
      ball: { n: '团成球', max: 0, msg: '铝箔团成球，几乎不排开水，浮力小得托不住自己——立刻沉底，一枚硬币也放不了。' },
      boat: { n: '折成小船', max: 15, msg: '铝箔折成小船，中间是空的，能排开很多水，浮力大大增加——这种形状最多能放 15 枚硬币。' }
    };
    var shape = 'ball', coins = 0;
    var shipEl = document.getElementById('ship-obj');
    var out = document.getElementById('ship-out');
    function renderShip() {
      var s = shapes[shape];
      shipEl.textContent = s.n;
      shipEl.style.borderRadius = shape === 'ball' ? '50%' : '6px 6px 22px 22px';
      shipEl.style.width = shape === 'ball' ? '48px' : '140px';
      shipEl.style.height = shape === 'ball' ? '48px' : '40px';
      var sink = coins > s.max;
      shipEl.style.top = sink ? '82%' : (shape === 'ball' ? '74%' : '52%');
      document.getElementById('ship-coins').textContent = coins + ' 枚';
      out.className = 'result ' + (sink ? 'error' : '');
      out.innerHTML = '<strong>' + s.n + '：' + s.msg + '</strong>' + (sink ? '<br>现在放了 ' + coins + ' 枚，超过上限，船沉了。' : '');
      document.querySelectorAll('[data-ship-shape]').forEach(function (b) { b.classList.toggle('selected', b.dataset.shipShape === shape); });
    }
    document.querySelectorAll('[data-ship-shape]').forEach(function (b) {
      b.addEventListener('click', function () { shape = b.dataset.shipShape; renderShip(); });
    });
    document.getElementById('ship-add').addEventListener('click', function () { coins = Math.min(coins + 5, 25); renderShip(); });
    document.getElementById('ship-reset').addEventListener('click', function () { coins = 0; renderShip(); });
    renderShip();
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：你猜谁会浮起来？", TTS["pretest"], [
        {"q": "把一颗石子和一块同样大小的木头放进水里，谁会浮起来？",
         "options": [("木头浮起来，石子沉下去", True), ("两个都沉下去", False), ("两个都浮起来", False)],
         "explain": "木头比水松散，石子比水密实，所以木头浮、石子沉。这说明沉浮和材料本身有关。"},
        {"q": "一个物体完全浸没在水里，它受到的浮力方向是：",
         "options": [("竖直向上", True), ("竖直向下", False), ("水平向前", False)],
         "explain": "浮力是液体从下往上托物体的力，方向永远竖直向上。"},
        {"q": "船是钢铁造的，按理说钢铁会沉，可大轮船为什么能浮着？",
         "options": [("船做成了空心的，排开了很多水", True), ("海水比铁还重", False), ("船开得快就不会沉", False)],
         "explain": "这个问题先记在心里，等下我们做实验来验证：排开的水越多，得到的浮力越大。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "浸在水里的物体，都受到水向上托的力", TTS["module-1"], f'''
        <p style="font-size:17px;margin:0 0 12px">把木块按进水里，一松手它就弹上来——因为水在<strong>向上托</strong>它。这个向上的托力，就叫<strong>浮力</strong>。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>浮力的方向</strong></p>
            <p style="color:var(--muted)">永远竖直向上，与重力方向相反。物体往哪边沉，浮力都朝上。</p>
          </div>
          <div class="inner-card">
            <p><strong>谁会产生浮力</strong></p>
            <p style="color:var(--muted)">水会、盐水会、油会，连空气也会。浸在什么流体里，就受到那个流体给的浮力。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="物体浸在水中受到竖直向上的浮力示意图">
          <figcaption>浮力来自液体对物体下表面向上的压力大于上表面向下的压力，所以合力竖直向上</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">💧</span><div><strong>小提示：</strong>浮力不是只有"浮起来的东西"才有。沉在水底的石子，同样受到水给它的浮力，只是浮力比它的重力小，托不住而已。</div></div>
{insight_box([
    {"lens": "看见它", "text": "水里的每一块石头、每一根木条，身上都贴着一个向上的箭头，大小不同，方向永远朝上。"},
    {"lens": "解释它", "text": "为什么是向上而不是向下？因为物体下表面浸得更深，水对它的向上压力大于上表面对它的向下压力，两个压力一抵，就剩下一股向上的力。"},
    {"lens": "迁移它", "text": "空气也是流体，所以热气球、降落伞同样受到空气给的浮力——这就是热气球能带着人升空的原因。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手测一测：浮力到底有多大？", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">选一个物体，先看清它在空气中的读数，再把它放进水里，看看读数变小了多少。</p>
        <div class="lab-panel">
          <div class="lab-stage" id="lab1-stage">
            <div class="airline"></div>
            <div class="lab-obj" id="lab1-obj" style="top:16%;background:#8d9bb5;width:46px;height:46px;">200g</div>
          </div>
          <div class="flex-row" style="margin-top:12px">
            <button class="choice" data-lab1-obj="hook" style="text-align:center">钩码</button>
            <button class="choice" data-lab1-obj="wood" style="text-align:center">木块</button>
            <button class="choice" data-lab1-obj="foam" style="text-align:center">泡沫块</button>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">空气中读数</span><span class="v" id="r-air">2.0 N</span></div>
            <div class="readout-cell"><span class="k">水中读数</span><span class="v green" id="r-water">— —</span></div>
            <div class="readout-cell"><span class="k">浮力 = 差值</span><span class="v" id="r-buoy">— —</span></div>
          </div>
          <div class="flex-row">
            <button class="choice" id="lab1-toggle" style="text-align:center;flex:1">把物体放进水里</button>
          </div>
          <p class="result warn" id="lab1-verdict" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>看完三组数据，你发现了什么？</strong>泡沫块放进水里，读数直接变成 0——因为它浮起来了，绳子不再被拉紧。这时浮力刚好等于它的重量。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "排开的水越多，浮力就越大", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">同一个物体，浸进水里的部分越多，弹簧测力计的读数就变得越小——说明<strong>浮力变大了</strong>。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div>物体浸进去一半时，它只"推开"了一半体积的水。</div></div>
          <div class="step"><span class="n">2</span><div>完全浸没时，它推开了和自身体积相同的水。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>阿基米德的发现：</strong>物体受到的浮力，等于它排开的那部分液体受到的重力。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="两个体积不同的物体排开不同水量的对比示意图">
          <figcaption>左边的物体小，排开的水少，受到的浮力小；右边的物体大，排开的水多，受到的浮力也大</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">⚖️</span><div><strong>换个说法：</strong>浮力的大小，跟你这个物体<em>有多重</em>没有直接关系，只跟它<strong>排开多少液体</strong>有关。这句话等一下做实验时会很有用。</div></div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "沉浮实验室：谁浮谁沉，你说了算", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先选液体，再选物体的材料，看看它浮、悬浮还是沉到底，然后读一读下面的解释。</p>
        <div class="lab-panel">
          <div class="lab-stage" id="lab2-stage">
            <div class="airline"></div>
            <div class="lab-obj" id="lab2-obj" style="top:26%;background:#c99a5b;width:74px;height:54px;">木块</div>
          </div>
          <div class="slider-row" style="margin-top:12px;display:block">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 选择液体</div>
            <div class="flex-row" style="margin-top:0">
              <button class="choice" data-lab2-liq="oil" style="text-align:center">食用油（0.92）</button>
              <button class="choice" data-lab2-liq="water" style="text-align:center">清水（1.00）</button>
              <button class="choice" data-lab2-liq="brine" style="text-align:center">浓盐水（1.15）</button>
            </div>
          </div>
          <div class="slider-row" style="margin-top:12px;display:block">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">② 选择物体</div>
            <div class="flex-row" style="margin-top:0">
              <button class="choice" data-lab2-mat="wood" style="text-align:center">木块（0.6）</button>
              <button class="choice" data-lab2-mat="plastic" style="text-align:center">塑料块（0.95）</button>
              <button class="choice" data-lab2-mat="alu" style="text-align:center">铝块（2.7）</button>
            </div>
          </div>
          <p class="result" id="lab2-verdict" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧪</span><div><strong>挑战：</strong>能不能找到一组，让塑料块在油里沉、在盐水里浮？找到之后，你就明白沉浮不是物体自己的"脾气"，而是<strong>物体和液体比较的结果</strong>。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：同体积的铝块和木块，谁沉谁浮", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>体积都是 100 立方厘米的铝块和木块，一起放进水里，会发生什么？请说明理由。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看清条件：</strong>体积相同（100 cm³），材料不同（铝 / 木）。</div></div>
          <div class="step"><span class="n">2</span><div><strong>比较密度：</strong>铝约为水的 2.7 倍（2.7 g/cm³）；木头约为水的一半（0.5 g/cm³）。</div></div>
          <div class="step"><span class="n">3</span><div><strong>做出判断：</strong>密度比水大的铝块下沉；密度比水小的木块漂浮。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>说清道理：</strong>铝块全部浸没时排开 100 cm³ 的水，这些水的重力小于铝块的重力，托不住它，所以下沉；木块只要排开一部分水，排开水的重力就等于木块的重力，于是浮住不动。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错法</span>
          <p style="margin:6px 0 0">说"因为铝块重所以下沉"是不准确的。体积相同的木块和铝块，铝块确实更重；但真正决定沉浮的是<strong>密度</strong>——换成一大块泡沫，即使比小铝块重得多，它依然能浮起来。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "下面哪句话是正确的？",
         "options": [("物体受到的浮力大小，等于它排开的液体受到的重力", True),
                     ("物体越重，受到的浮力一定越大", False),
                     ("只有浮起来的东西才受到浮力", False)],
         "explain": "浮力只看排开了多少液体，与物体自身轻重没有直接关系；沉在水底的石头同样受到浮力。<strong>错因提醒：</strong>把浮力和重力搞混，是这一课最高频的常见错误。"},
        {"q": "把一块木块从水中往上提，让它排开的水变少，它受到的浮力会：",
         "options": [("变小", True), ("变大", False), ("不变", False)],
         "explain": "排开的液体变少，浮力随之变小。这正是弹簧测力计读数会变化的原理。<strong>错因提醒：</strong>选不变的同学，多半是误认为浮力由物体的重量决定。请回到那句话：浮力等于排开液体受到的重力。"},
        {"q": "把同一个鸡蛋放进清水里它沉底，放进浓盐水里它浮起来。原因是：",
         "options": [("盐水的密度变大，鸡蛋排开同样体积的盐水重力更大，浮力变大", True),
                     ("盐水把鸡蛋往上吸", False),
                     ("鸡蛋在盐水里变轻了", False)],
         "explain": "鸡蛋没有变，变的是液体。液体密度越大，同样体积排开的液体越重，浮力越大。<strong>错因提醒：</strong>容易误认为物体在盐水里变轻了——物体的重并没有改变，改变的是它获得的浮力。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：用一张铝箔做一艘能装货的船", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">同一张铝箔，形状不同，能装的东西完全不同。先试一试，再总结原因。</p>
        <div class="lab-panel">
          <div class="lab-stage" id="ship-stage" style="height:180px">
            <div class="airline"></div>
            <div class="lab-obj" id="ship-obj" style="top:74%;background:#8d9bb5;width:48px;height:48px;">团成球</div>
          </div>
          <div class="flex-row" style="margin-top:12px">
            <button class="choice" data-ship-shape="ball" style="text-align:center">团成球</button>
            <button class="choice" data-ship-shape="boat" style="text-align:center">折成小船</button>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">已放硬币</span><span class="v" id="ship-coins">0 枚</span></div>
          </div>
          <div class="flex-row">
            <button class="choice" id="ship-add" style="text-align:center">放 5 枚硬币</button>
            <button class="choice" id="ship-reset" style="text-align:center">重新开始</button>
          </div>
          <p class="result warn" id="ship-out" style="margin-top:12px"></p>
        </div>
        <div class="inner-card">
          <p><strong>把它们写下来，说给同桌听：</strong></p>
          <p style="color:var(--muted)">铝箔的重量改变了没有？排开的水量改变了没有？浮力改变了没有？为什么折成船就能装货？</p>
          <textarea id="syn-answer" rows="3" placeholder="铝箔的重量……排开的水量……所以浮力……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换一个情境，看看规律还在不在", TTS["posttest"], [
        {"q": "潜水艇要下潜时，会往水舱里灌海水。灌水之后它下沉，是因为：",
         "options": [("自身变重了，重力大于浮力", True), ("海水的浮力突然消失了", False), ("潜水艇的密度变小了", False)],
         "explain": "潜水艇体积不变，所以浮力基本不变；灌水让它变重，重力大于浮力就下沉。它靠改变自身重力实现上浮下潜。"},
        {"q": "一株新鲜的黄瓜放在水里会浮着，切成小块后更容易沉。最合理的解释是：",
         "options": [("切开后内部的空隙减少，整体变得更密实", True), ("切小了就一定会沉", False), ("水变重了", False)],
         "explain": "沉的依据是密度。改变的是物体的密实程度，不是水的性质。"},
        {"q": "用弹簧测力计测出某物体在空气中重 4.0 牛，浸没在水中时读数为 3.0 牛，它受到的浮力是：",
         "options": [("1.0 牛", True), ("7.0 牛", False), ("4.0 牛", False)],
         "explain": "浮力等于两次读数的差：4.0 − 3.0 = 1.0 牛。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把自己讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>方向</strong>：浸在液体里的物体受到竖直向上的浮力。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>大小</strong>：浮力等于物体排开的液体受到的重力——排开越多，浮力越大。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>沉浮</strong>：物体比液体密实就下沉，比液体松散就漂浮，差不多就悬浮。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头的大轮船：</strong>钢铁确实比水密实，但船体是空心的，整艘船的平均密度比水小，还排开了巨量的水，得到的浮力足以托起全部重量——所以它浮着。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用"浮力、排开的水、密度"这三个词，说清楚木块为什么能浮，石子为什么会沉。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "说出浮力的方向，并解释为什么一块沉在水底的石子也受到浮力。",
            "写出判断物体沉浮的方法：比较物体和液体的什么？",
        ],
        [
            "用弹簧测力计测量一个物体在水中的浮力，把空气中读数、水中读数、算出浮力三栏记在实验记录本上。",
            "把一个鸡蛋分别放进清水和浓盐水，记录现象并解释原因。",
        ],
        [
            "用一张铝箔设计一艘能装下十枚硬币的小船，画出设计图，并写清楚你为什么把铝箔做成这个形状。",
            "找一个身边的例子（比如游泳、热气球、潜水艇），说明人们是怎样利用浮力来解决问题。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "sci-e-buoyancy",
    "node_id": "sci-e-buoyancy",
    "title": "浮力：为什么有的东西浮在水上？",
    "name_en": "Buoyancy: Why do some things float?",
    "grade": 5,
    "grade_cn": "五年级",
    "domain": "matter-science",
    "domain_cn": "物质科学 · 力",
    "lesson_type": "experiment-inquiry",
    "version": "1.0.0",
    "description": "通过称重法测浮力与沉浮对比实验，理解浮力的方向竖直向上、大小等于排开液体受到的重力，并用密度比较解释物体沉浮与钢铁轮船能浮起的原因。",
    "tags": ["浮力", "沉浮", "排开的水", "密度", "阿基米德原理"],
    "standard_ref": "《义务教育科学课程标准（2022年版2025年修订）》3～4年级/5～6年级 学科核心概念3「物质的运动与相互作用」——认识常见物体的基本特征与常见的力，知道力可以改变物体的运动状态；5～6年级能初步解释物体在水中的沉浮现象。",
    "hero_question": "钢铁造的大轮船为什么能浮着，轻轻一颗石子却立刻沉底？",
    "hero_alt": "浮力知识结构图：浮力的方向、大小与沉浮条件",
    "hero_caption": "浮力：方向竖直向上 · 大小等于排开液体受到的重力 · 沉浮取决于物体与液体的密度比较",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的实验都会围着它转。",
    "anchor_choices": [
        {"t": "浮力是从哪里来的？", "d": "水为什么能把东西往上托", "v": "浮力是从哪里来的"},
        {"t": "浮力到底有多大？", "d": "能不能像测重量一样把浮力测出来", "v": "浮力到底有多大"},
        {"t": "什么东西会浮，什么东西会沉？", "d": "有没有一条判断标准", "v": "什么东西会浮什么东西会沉"},
        {"t": "怎样做一艘能装很多货的船？", "d": "想让铝箔船装下更多硬币", "v": "怎样做一艘能装很多货的船"},
    ],
    "objectives": [
        "能说出浮力是什么，知道浮力的方向竖直向上",
        "能用弹簧测力计，通过两次读数之差测出物体受到的浮力",
        "能说出浮力大小与物体排开液体的多少有关，并举例说明",
        "能比较物体与液体的密度，解释物体沉浮，并说明钢铁轮船为什么能浮",
    ],
    "objectives_plain": [
        "能说出浮力是什么，知道浮力的方向竖直向上",
        "能用弹簧测力计，通过两次读数之差测出物体受到的浮力",
        "能说出浮力大小与物体排开液体的多少有关，并举例说明",
        "能比较物体与液体的密度，解释物体沉浮，并说明钢铁轮船为什么能浮",
    ],
    "standards": [
        {"content": "认识常见物体的基本特征，认识生活中常见的力，知道力可以改变物体的运动状态",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念3 物质的运动与相互作用（3～4年级）"},
        {"content": "能基于证据解释简单现象，知道物体在水中的沉浮与排开液体的多少有关",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念3 物质的运动与相互作用（5～6年级）"},
    ],
    "prereqs": ["sci-e-push-pull-force"],
    "prereqs_name": "推和拉的力",
    "prereqs_meta": "sci-e-push-pull-force",
    "leads_to": ["sci-e-simple-machines"],
    "next_meta": "sci-e-simple-machines",
    "section_images": ["assets/sci-e-buoyancy-fig1.webp", "assets/sci-e-buoyancy-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "钢铁造的大船为什么浮着？石子为什么沉底？带着这个矛盾开始。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能自己判断谁会浮、谁会沉。",
        "objectives": "看清四件事：说出浮力方向、量出浮力大小、说出浮力与排开的水有关、解释轮船为什么能浮。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "水会从下往上托物体，这个向上的托力就叫浮力，方向永远竖直向上。",
        "lab-1": "两次读数一相减，就是浮力。先看空气中的读数，再看水中的读数。",
        "module-2": "排开的水越多，浮力越大——这是阿基米德的发现，不用背公式。",
        "lab-2": "液体和物体都能换，试试能不能让同一块塑料在油里沉、在盐水里浮。",
        "worked-example": "四步走：看清条件、比较密度、做出判断、说清道理。",
        "conceptest-1": "干扰项里藏着最常见的那几个错误想法，选完看清每一个解释。",
        "synthesis": "同一张铝箔，团成球就沉，折成船能装货——想想排开的水变了没有。",
        "posttest": "换了潜水艇和黄瓜的新情境，看看你还能不能用上同一条规律。",
        "summary": "回到开头那条大船：它凭什么浮起来？用三句话讲清楚。",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是「物质的运动与相互作用」里力的板块长期空缺的一课：知识树原有推和拉的力、摩擦力，缺浮力与沉浮。设计上不引入公式，只做两件可测量的事——用弹簧测力计把浮力量出来，用密度比较把沉浮判断出来；再用钢铁轮船与铝箔船两个真实情境收束，让「排开的水越多、浮力越大」成为学生能自己复述的结论。",
    "plan_table": """| 1 | cover | 浮力：为什么有的东西浮在水上？ | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：你猜谁会浮起来？ | 起·前测（暴露直觉） |
| 5 | concept | 浸在水里的物体，都受到水向上托的力 | 承·概念一 |
| 6 | interactive | 动手测一测：浮力到底有多大？ | 承·实验室一（称重法） |
| 7 | concept | 排开的水越多，浮力就越大 | 承·概念二（阿基米德定性版） |
| 8 | interactive | 沉浮实验室：谁浮谁沉，你说了算 | 承·实验室二（密度比较） |
| 9 | concept | 例题示范：同体积的铝块和木块，谁沉谁浮 | 转·重难点突破（分步示范 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：用一张铝箔做一艘能装货的船 | 合·迁移应用 |
| 12 | quiz | 后测：换一个情境，看看规律还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把自己讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：浮力的方向、大小、沉浮条件三栏标注\n- P5 浮力来源示意图（已生成）：物体在液体中上下表面压力差\n- P7 排开水量对比图（已生成）：大物体排开更多水 → 浮力更大\n- 若需补充：弹簧测力计实物照片、轮船与石子的实景图",
}
