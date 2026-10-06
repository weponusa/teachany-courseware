# -*- coding: utf-8 -*-
"""小学科学 · 物理变化与化学变化（G6）—— 补齐课标「物质的变化与化学反应·2.3 物质变化的特征」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/sci-e-chemical-change-fig1.webp'
F2 = './assets/sci-e-chemical-change-fig2.webp'

TTS = {
    "hero": "看两支蜡烛。第一支被点燃，烧着烧着变短、消失了；第二支只是放在暖气旁边，慢慢软化、弯下来。两支蜡烛都变了样子，可它们变的是同一回事吗？这节课我们要学会一件很重要的本事：判断一个变化里，到底有没有产生新物质。",
    "problem-anchor": "先选一个你最想弄明白的问题。是想知道冰化成水到底算不算变了，还是想知道蜡烛燃烧以后东西去哪儿了，又或者你想学会一眼分辨厨房里哪一种变化，选好之后带着问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出物理变化和化学变化的根本区别，是有没有产生新物质。第二，能举例分辨生活中的物理变化和化学变化。第三，知道化学变化常常伴随发光、发热、变色、产生气体或沉淀。第四，能解释铁钉生锈、蜡烛燃烧为什么属于化学变化。",
    "pretest": "先做三道小题，用你现在的想法选就好。选完立刻能看到解释，选错了正好知道要重点听哪里。",
    "module-1": "先看物理变化。冰化成水，状态从固体变成了液体，可它还是水；纸被撕成碎片，形状变了，可每一片还是纸；玻璃杯打碎、糖块磨成粉，都是同一类情况。它们的共同点是：形状、大小或者状态变了，但构成物质的材料没有改变，没有新物质产生。",
    "lab-1": "现在请你自己当一次判断员。下面有八种生活中常见的变化，请你把它们分别放进物理变化或者化学变化两个筐里。放之前先问自己一句话：这里面有没有产生新的物质？放错了会有提示，看看你能不能全部放对。",
    "module-2": "再看化学变化。铁钉生了锈，锈是一种新物质，它和铁不一样，所以铁钉生锈是化学变化。蜡烛燃烧后产生了二氧化碳和水蒸气，跑掉了，蜡烛才越来越短，这也是化学变化。化学变化常常带上一些可以观察到的现象：发光、发热、变色、冒出气体、生成沉淀。不过要记住，有现象不等于一定是化学变化，最终还是要看有没有新物质产生。",
    "lab-2": "我们做一组对比实验。左边一杯是小苏打加白醋，右边一杯是糖溶解在水里。两边都动手混合一下，然后仔细观察：有没有气泡，温度有没有变化，物质还在不在。看完你就抓住判断的关键了。",
    "worked-example": "我们一起分析一道题：铁钉生锈到底是不是化学变化？第一步，先找出变化前后的物质，变化前是铁钉，变化后是铁钉和铁锈。第二步，比较它们是不是同一种物质，铁锈的颜色、硬度都和铁不一样，也不能被磁铁吸起来。第三步，得出判断，有新物质产生，所以是化学变化。第四步，补充证据，铁钉生锈还伴随着颜色从银白变成红棕，这是变色的现象，和我们的判断是一致的。",
    "conceptest-1": "接下来用三个容易混的说法考考你。请仔细读每一个选项，选完再看解释。",
    "synthesis": "最后一件事交给你。请你在厨房或者教室里找出三种物理变化和三种化学变化，每一种都要说清楚理由，理由里必须回答一句话：有没有产生新物质。写下来以后讲给同桌听。",
    "posttest": "最后一轮，用新的情境检验一下。这里面有食物、有火柴、有气球，看看你能不能把学到的判断标准用上去。",
    "summary": "这节课我们抓住了一条判断标准。物理变化，是形状、状态变了，物质本身没变；化学变化，是产生了新物质，常常伴随发光、发热、变色、产生气体或者沉淀。要特别提醒的是：出现气泡或者发光，只是线索，最后一定要回到那句话上，有没有新物质产生。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出一句判断两种变化的标准，并各举一个例子。第二层能力应用，动手做：回家找出三种物理变化和三种化学变化，逐一写明理由。第三层迁移挑战，选做：观察一枚铁钉在潮湿和干燥两种环境里的变化，记录下来，并提出两种防锈办法，说清每种办法挡住了什么。",
    "knowledge-graph": "这张图展示了这节课在科学知识网络里的位置。左边是先要学会的知识，右边是可以继续探索的内容，下面是同一领域的伙伴知识。点一点，看看还有哪些值得研究的现象。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先找到你卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 物理变化", "lab-1": "实验室一 变化分类器", "module-2": "概念二 化学变化",
    "lab-2": "实验室二 对比实验", "worked-example": "例题讲解 铁钉生锈", "conceptest-1": "概念测试",
    "synthesis": "综合任务 变化侦探", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

SORT_ITEMS = [
    {"id": "ice", "t": "冰化成水", "kind": "phys", "why": "状态从固体变成液体，但仍然是水，没有新物质产生。"},
    {"id": "tear", "t": "纸被撕成碎片", "kind": "phys", "why": "形状变了，每一片都还是纸，没有新物质产生。"},
    {"id": "glass", "t": "玻璃杯被打碎", "kind": "phys", "why": "只是形状改变，碎片的材料还是玻璃。"},
    {"id": "sugar", "t": "糖溶解在水里", "kind": "phys", "why": "糖只是分散到水里看不到了，蒸发水分还能把糖取回来，没有新物质产生。"},
    {"id": "rust", "t": "铁钉生锈", "kind": "chem", "why": "铁锈是铁和空气中的氧气、水反应生成的新物质，颜色和性质都变了。"},
    {"id": "candle", "t": "蜡烛燃烧", "kind": "chem", "why": "产生了二氧化碳和水蒸气等新物质，所以蜡烛才越来越短。"},
    {"id": "soda", "t": "小苏打和白醋混合", "kind": "chem", "why": "产生了二氧化碳气泡等新物质，是典型的化学变化。"},
    {"id": "rice", "t": "米饭放久了变馊", "kind": "chem", "why": "微生物让米饭产生了新的物质，闻起来变酸，是化学变化。"},
]

CUSTOM_JS = r"""
/* ============================================================
   sci-e-chemical-change 互动逻辑
   1) 选择题接线
   2) 变化分类器：八种变化 → 物理变化 / 化学变化 两个筐
   3) 对比实验：小苏打+白醋 vs 糖溶解
   ============================================================ */
(function () {
  'use strict';

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

  /* ---------- 变化分类器 ---------- */
  var bank = document.getElementById('sort-bank');
  if (bank) {
    var picked = null;
    var done = 0, wrongCount = 0;
    var msg = document.getElementById('sort-msg');

    bank.querySelectorAll('.sort-item').forEach(function (card) {
      card.addEventListener('click', function () {
        if (card.classList.contains('done')) return;
        bank.querySelectorAll('.sort-item').forEach(function (c) { c.style.outline = 'none'; });
        card.style.outline = '3px solid var(--brand)';
        picked = card;
        msg.className = 'result warn';
        msg.textContent = '已选中「' + card.textContent.trim() + '」，现在点左边或右边的筐把它分类。';
      });
    });

    document.querySelectorAll('[data-sort-bin]').forEach(function (bin) {
      bin.addEventListener('click', function () {
        if (!picked) { msg.className = 'result warn'; msg.textContent = '先点一张变化卡片，再点筐。'; return; }
        var want = picked.dataset.kind, got = bin.dataset.sortBin;
        picked.style.outline = 'none';
        if (want === got) {
          var tag = document.createElement('span');
          tag.className = 'tag';
          tag.textContent = picked.textContent.trim() + ' ✓';
          tag.style.borderColor = 'rgba(78,205,196,.8)';
          tag.style.background = 'rgba(78,205,196,.14)';
          bin.querySelector('.bin-body').appendChild(tag);
          picked.classList.add('done');
          picked.textContent = picked.textContent.trim();
          done++;
          msg.className = 'result';
          msg.innerHTML = '<strong>放对了！</strong>' + picked.dataset.why;
          picked = null;
          if (done === 8) {
            msg.className = 'result';
            msg.innerHTML = '<strong>八张卡片全部分类完成，错误 ' + wrongCount + ' 次。</strong>你已经在用一个很关键的问题判断：这个变化里，有没有产生新物质。';
          }
        } else {
          wrongCount++;
          msg.className = 'result error';
          msg.innerHTML = '<strong>再想一下：</strong>' + picked.textContent.trim() + ' 里，有没有产生和原来不一样的新物质？';
          picked.style.outline = '3px dashed rgba(239,68,68,.7)';
        }
      });
    });
  }

  /* ---------- 对比实验 ---------- */
  var expStage = document.getElementById('exp-stage');
  if (expStage) {
    var out = document.getElementById('exp-out');
    var bubbleLayer = document.getElementById('exp-bubbles');
    var tempA = document.getElementById('exp-temp-a');

    function clearBubbles() { bubbleLayer.innerHTML = ''; }

    function mixSoda() {
      clearBubbles();
      for (var i = 0; i < 14; i++) {
        var b = document.createElement('span');
        b.className = 'bubble';
        b.style.left = (8 + Math.random() * 84) + '%';
        b.style.animationDelay = (Math.random() * 1.6).toFixed(2) + 's';
        b.style.animationDuration = (1.8 + Math.random() * 1.4).toFixed(2) + 's';
        bubbleLayer.appendChild(b);
      }
      tempA.textContent = '18.5 ℃';
      out.className = 'result';
      out.innerHTML = '<strong>小苏打 + 白醋 → 化学变化</strong><br>杯里立刻冒出大量气泡，是二氧化碳；杯壁摸起来变凉，说明温度下降。最重要的是：<strong>产生了新物质</strong>，这两个现象都和它一致。';
    }
    function mixSugar() {
      clearBubbles();
      out.className = 'result warn';
      out.innerHTML = '<strong>糖 + 水 → 物理变化</strong><br>看不到气泡，温度没有变化，糖只是散到水里看不见了。把水蒸发掉，糖还能重新取回来——<strong>没有产生新物质</strong>。';
    }
    document.getElementById('exp-btn-a').addEventListener('click', mixSoda);
    document.getElementById('exp-btn-b').addEventListener('click', mixSugar);
    document.getElementById('exp-reset').addEventListener('click', function () {
      clearBubbles();
      tempA.textContent = '22.0 ℃';
      out.className = 'result warn';
      out.textContent = '先选左边或者右边动手混合，再对比两边的现象有什么不同。';
    });
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：它们算不算变了？", TTS["pretest"], [
        {"q": "冰化成水，这个变化里有没有产生新物质？",
         "options": [("没有，水还是水，只是状态变了", True), ("有，冰变成了水这个新物质", False), ("说不清，要看冰有多少", False)],
         "explain": "固体变液体只是状态改变，物质本身仍然是水，所以没有新物质产生。<strong>错因提醒：</strong>常见错误是看到样子变了就判成化学变化。请务必回到那一句：有没有产生新物质。"},
        {"q": "判断一个变化是不是化学变化，最关键的依据是：",
         "options": [("有没有产生新物质", True), ("有没有发出声音", False), ("变化大不大、快不快", False)],
         "explain": "现象只是线索，最终依据只有一个：有没有产生和原来不同的新物质。<strong>错因提醒：</strong>很多同学会把剧烈程度和变化类型搞混——爆炸般快的也可能只是物理变化，安静缓慢的也可能在生成新物质。"},
        {"q": "蜡烛燃烧后越来越短，烧掉的部分去哪儿了？",
         "options": [("变成了二氧化碳和水蒸气等新物质跑到空气里", True), ("变成水一直留在烛台上", False), ("凭空消失了", False)],
         "explain": "燃烧产生了二氧化碳和水蒸气等新物质，以气体形式散到空气中，所以蜡烛看着像消失了。<strong>错因提醒：</strong>不要误认为物质凭空消失。变化前后物质的总量是守恒的，只是它跑到了我们看不见的地方。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "形状变了、状态变了，但物质没有变", TTS["module-1"], f'''
        <p style="font-size:17px;margin:0 0 12px">冰化成水，纸被撕碎，玻璃杯打碎——这些都叫<strong>物理变化</strong>。判断的依据只有一句话：<strong>有没有新物质产生</strong>。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>变了什么</strong></p>
            <p style="color:var(--muted)">形状、大小、状态（固/液/气）发生变化。</p>
          </div>
          <div class="inner-card">
            <p><strong>没变什么</strong></p>
            <p style="color:var(--muted)">构成物体的材料还是原来那种，能想办法变回去。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="物理变化与化学变化对比示意图">
          <figcaption>同样的形状改变，左边是物理变化（还是原来的物质），右边是化学变化（长出了新物质）</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🔎</span><div><strong>一个反问帮你判断：</strong>能不能想办法把它变回去？冰化成水，冻一冻又变回冰；纸撕碎了，却再也拼不回那张纸，但每一片都还是纸——所以还是物理变化。</div></div>
    ''', tag="概念一"))

    import json as _json
    items_html = "\n".join(
        f'          <button class="sort-item" data-kind="{it["kind"]}" data-why="{it["why"]}">{it["t"]}</button>'
        for it in SORT_ITEMS
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "变化分类器：八种变化，放进两个筐", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一张卡片，再点你认为正确的筐。每放一次都会立刻告诉你理由。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">待分类的变化</div>
          <div class="sort-bank" id="sort-bank">
{items_html}
          </div>
          <div class="sort-bins">
            <div class="sort-bin" data-sort-bin="phys">
              <h4>🧊 物理变化</h4>
              <div class="bin-body"></div>
            </div>
            <div class="sort-bin" data-sort-bin="chem">
              <h4>🔥 化学变化</h4>
              <div class="bin-body"></div>
            </div>
          </div>
          <p class="result warn" id="sort-msg" style="margin-top:12px">点一张卡片开始分类。</p>
        </div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "产生了新物质，就是化学变化", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">铁钉生锈、蜡烛燃烧、小苏打和白醋混合——这些是<strong>化学变化</strong>。它们的共同点是：<strong>产生了和原来不同的新物质</strong>。</p>
        <div class="inner-card">
          <p><strong>化学变化常见的五个现象（只是线索，不是依据）</strong></p>
          <div class="sort-bank" style="margin-top:6px">
            <span class="sort-item done" style="cursor:default">💡 发光</span>
            <span class="sort-item done" style="cursor:default">🌡️ 发热</span>
            <span class="sort-item done" style="cursor:default">🎨 变色</span>
            <span class="sort-item done" style="cursor:default">🫧 产生气体</span>
            <span class="sort-item done" style="cursor:default">⬇️ 生成沉淀</span>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="铁钉生锈与蜡烛燃烧两种化学变化示意图">
          <figcaption>左边铁钉表面长出红棕色的铁锈，右边蜡烛燃烧生成二氧化碳和水蒸气——都产生了新物质</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">特别注意</span>
          <p style="margin:6px 0 0">水烧开也冒气泡、电灯也发光发热，但它们都是物理变化。所以不能只看现象，最后一定要回到那句话：<strong>有没有产生新物质</strong>。</p>
        </div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "对比实验：冒气泡的一定是化学变化吗？", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">两杯液体摆在这里，左边是小苏打，右边是糖水。分别混合一下，对比它们的现象。</p>
        <div class="lab-panel">
          <div class="lab-stage" id="exp-stage" style="height:230px;background:linear-gradient(180deg,#f7fbff 0%,#eaf6ff 100%)">
            <div id="exp-bubbles" style="position:absolute;inset:0;overflow:hidden"></div>
            <div style="position:absolute;left:12%;bottom:10%;width:96px;height:96px;border-radius:8px 8px 14px 14px;background:rgba(255,255,255,.85);border:2px solid rgba(78,205,196,.6);display:grid;place-items:center;font-size:13px;font-weight:700;color:#5c5142;text-align:center;line-height:1.3">小苏打<br>+白醋</div>
            <div style="position:absolute;right:12%;bottom:10%;width:96px;height:96px;border-radius:8px 8px 14px 14px;background:rgba(255,255,255,.85);border:2px solid rgba(255,209,102,.8);display:grid;place-items:center;font-size:13px;font-weight:700;color:#5c5142;text-align:center;line-height:1.3">糖<br>+水</div>
            <div style="position:absolute;left:12%;bottom:calc(10% + 104px);font-size:13px;color:#94866c">温度 <strong id="exp-temp-a">22.0 ℃</strong></div>
          </div>
          <div class="flex-row">
            <button class="choice" id="exp-btn-a" style="text-align:center">混合：小苏打 + 白醋</button>
            <button class="choice" id="exp-btn-b" style="text-align:center">混合：糖 + 水</button>
            <button class="choice" id="exp-reset" style="text-align:center">重置</button>
          </div>
          <p class="result warn" id="exp-out" style="margin-top:12px">先选左边或者右边动手混合，再对比两边的现象有什么不同。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧠</span><div><strong>想清楚一件事：</strong>两边都"看不见原来的东西了"，但左边产生了新物质，右边没有。这就是两种变化的根本分界。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：铁钉生锈算化学变化吗", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>把一枚光亮铁钉放在潮湿的空气中，几天后表面变成红棕色。这个变化是物理变化还是化学变化？请说明理由。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>找出变化前后的物质：</strong>变化前是银白色、能被磁铁吸住的铁；变化后表面多了一层红棕色物质。</div></div>
          <div class="step"><span class="n">2</span><div><strong>比较是不是同一种物质：</strong>铁锈颜色不同、又硬又脆、磁铁吸不起来，它不是铁。</div></div>
          <div class="step"><span class="n">3</span><div><strong>得出结论：</strong>产生了新物质，所以是<strong>化学变化</strong>。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>补充证据：</strong>颜色由银白变成红棕，这与化学变化中常见的变化现象一致，支持我们的结论。</div></div>
        </div>
        <div class="kid-note"><span class="emoji">🛠️</span><div><strong>连起来想一想：</strong>既然铁锈是新物质，那防锈的办法就有方向了——把铁和水、空气隔开。涂油、刷漆、镀上一层别的金属，都是用这个思路。</div></div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：这三种说法错在哪里", TTS["conceptest-1"], [
        {"q": "下面哪个变化属于化学变化？",
         "options": [("铁钉在潮湿空气里生锈", True), ("冰块放进饮料里融化", False), ("橡皮筋被拉长", False)],
         "explain": "只有铁钉生锈产生了新物质（铁锈），另外两个都只是形状或状态改变。"},
        {"q": "水烧开时冒出大量气泡，这个变化是：",
         "options": [("物理变化，气泡是水蒸气，还是水", True), ("化学变化，因为有气体产生", False), ("无法判断", False)],
         "explain": "冒气泡只是现象。水蒸气冷却后又变回水，没有新物质产生，所以是物理变化。"},
        {"q": "下列说法正确的是：",
         "options": [("化学变化一定产生新物质", True), ("有发光发热的变化一定是化学变化", False), ("物理变化一定比化学变化简单", False)],
         "explain": "发光发热只是线索；判断的唯一依据是有没有新物质产生。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：当一次变化侦探", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">请找出 3 种物理变化和 3 种化学变化，每一种都要说清理由。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>🧊 物理变化（写 3 种）</strong></p>
            <textarea rows="5" placeholder="例如：冰化成水——状态变了，但还是水，没有新物质"></textarea>
          </div>
          <div class="inner-card">
            <p><strong>🔥 化学变化（写 3 种）</strong></p>
            <textarea rows="5" placeholder="例如：铁钉生锈——长出了铁锈这个新物质"></textarea>
          </div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>必须回答的问题：</strong>你写的每一种变化里，有没有产生新物质？说出你的判断依据。</p>
        </div>
        <div class="kid-note"><span class="emoji">🗣️</span><div>写完之后讲给同桌听，请他指出哪一种理由不清楚，再补上。</div></div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换个情境，规律还在不在", TTS["posttest"], [
        {"q": "把一根火柴点燃，火焰熄灭后只剩一小截黑色残渣。这个变化是：",
         "options": [("化学变化，燃烧生成了新物质", True), ("物理变化，只是火柴变短了", False), ("先是物理变化，后来才变", False)],
         "explain": "燃烧生成了二氧化碳、水蒸气和黑色的炭等新物质，所以是化学变化。"},
        {"q": "气球吹大以后松开手，气球飞走变小，这是：",
         "options": [("物理变化，只是形状和大小的改变", True), ("化学变化，因为气球里的空气变了", False), ("化学变化，因为会发出声音", False)],
         "explain": "空气只是进出气球，没有产生新物质。"},
        {"q": "妈妈把土豆切成丝，过一会儿土豆丝表面变黑了，这个变化：",
         "options": [("是化学变化，土豆里的物质和空气发生了反应生成了新物质", True),
                     ("是物理变化，只是切的时候沾了脏东西", False),
                     ("是物理变化，因为看起来只是颜色深了", False)],
         "explain": "颜色变深是产生了新物质的信号。切开后土豆里的成分接触空气发生反应，属于化学变化。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：一句话记住两种变化", TTS["summary"], f'''
        <div class="grid">
          <div class="summary-item"><span class="num">🧊</span><div><strong>物理变化</strong>：形状、大小、状态变了，<strong>物质没有变</strong>。例：冰化成水、纸被撕碎、糖溶解。</div></div>
          <div class="summary-item"><span class="num">🔥</span><div><strong>化学变化</strong>：<strong>产生了新物质</strong>。例：铁钉生锈、蜡烛燃烧、小苏打和白醋混合。</div></div>
          <div class="summary-item"><span class="num">🔑</span><div><strong>判断依据只有一句</strong>：有没有产生新物质。发光、发热、变色、冒气泡、生成沉淀都只是线索。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那两支蜡烛：</strong>被点燃的那支，产生了二氧化碳和水蒸气等新物质，是化学变化；只是被暖气烤软的那支，形状变了但没有新物质，是物理变化。看起来都是变了样子，本质并不一样。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "用一句话写出判断物理变化和化学变化的标准，并各举一个例子。",
            "在下面的变化里选出化学变化并说明理由：冰化成水、铁钉生锈、纸被撕碎、小苏打和白醋混合。",
        ],
        [
            "在家里找出三种物理变化和三种化学变化，逐一写明理由，理由里必须回答有没有产生新物质。",
            "把小苏打和白醋混合后的现象记录下来，写成一份不超过五行的实验小报告。",
        ],
        [
            "观察一枚铁钉放在潮湿处和干燥处一周后的变化，记录下来，并据此提出两种防锈办法，说明每种办法挡住了什么。",
            "查找一种生活中常见的变化（例如食物变质、金属焊接、烟花燃放），判断它属于哪一类变化，并说清你的判断依据。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "sci-e-chemical-change",
    "node_id": "sci-e-chemical-change",
    "title": "物理变化与化学变化：物质到底变了没有？",
    "name_en": "Physical and Chemical Changes: Did the substance change?",
    "grade": 6,
    "grade_cn": "六年级",
    "domain": "matter-science",
    "domain_cn": "物质科学 · 物质的变化",
    "lesson_type": "concept-inquiry",
    "version": "1.0.0",
    "description": "以有没有产生新物质为唯一判据，区分物理变化与化学变化；通过分类互动与对比实验，识别化学变化的常见现象并避免只看现象下结论。",
    "tags": ["物理变化", "化学变化", "新物质", "铁钉生锈", "对比实验"],
    "standard_ref": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念2「物质的变化与化学反应」学习内容2.3 物质变化的特征——5～6年级知道物体变化时构成物体的物质可能改变也可能不改变。",
    "hero_question": "蜡烛烧短了，蜡烛软了，同样是变了样子——它们变的是同一回事吗？",
    "hero_alt": "物理变化与化学变化对比知识结构图",
    "hero_caption": "判断依据只有一句：有没有产生新物质 · 物理变化：物质没变 · 化学变化：长出了新物质",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的实验都会围着它转。",
    "anchor_choices": [
        {"t": "冰化成水，到底算不算变了？", "d": "状态变了，物质算不算变", "v": "冰化成水到底算不算变了"},
        {"t": "蜡烛燃烧后，东西去哪儿了？", "d": "烧掉的部分是不是消失了", "v": "蜡烛燃烧后东西去哪儿了"},
        {"t": "有没有一句话能判断所有变化？", "d": "想学一条万能的判断标准", "v": "有没有一句话能判断所有变化"},
        {"t": "为什么铁会生锈，怎么防锈？", "d": "想知道生活里的防锈办法", "v": "为什么铁会生锈怎么防锈"},
    ],
    "objectives": [
        "能说出物理变化与化学变化的根本区别是有没有产生新物质",
        "能举例分辨生活中常见的物理变化和化学变化，并说明理由",
        "知道化学变化常伴随发光、发热、变色、产生气体或生成沉淀",
        "能解释铁钉生锈、蜡烛燃烧为什么属于化学变化",
    ],
    "objectives_plain": [
        "能说出物理变化与化学变化的根本区别是有没有产生新物质",
        "能举例分辨生活中常见的物理变化和化学变化，并说明理由",
        "知道化学变化常伴随发光、发热、变色、产生气体或生成沉淀",
        "能解释铁钉生锈、蜡烛燃烧为什么属于化学变化",
    ],
    "standards": [
        {"content": "知道物体变化时构成物体的物质可能改变也可能不改变，能举例说明",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念2 物质的变化与化学反应（5～6年级）"},
        {"content": "能基于观察到的现象与证据作出判断，并说明判断依据",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》科学思维·推理论证（5～6年级）"},
    ],
    "prereqs": ["sci-e-dissolving", "sci-e-solid-liquid-gas"],
    "prereqs_name": "溶解现象；物质的三态与变化",
    "prereqs_meta": "sci-e-dissolving,sci-e-solid-liquid-gas",
    "leads_to": ["sci-e-energy-forms"],
    "next_meta": "sci-e-energy-forms",
    "section_images": ["assets/sci-e-chemical-change-fig1.webp", "assets/sci-e-chemical-change-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "两支蜡烛都变了样子，可它们变的是同一回事吗？带着这个疑问开始。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能一眼说清一个变化有没有产生新物质。",
        "objectives": "看清四件事：说出判据、分辨生活实例、认识化学变化的常见现象、解释生锈与燃烧。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "形状变、状态变，但材料没变——这就是物理变化。",
        "lab-1": "放之前先问自己一句话：这里面有没有产生新的物质？",
        "module-2": "冒出气泡、发出光、变了颜色，都只是线索，关键还是有没有新物质。",
        "lab-2": "两边都混合一下，比一比气泡和温度有什么不同。",
        "worked-example": "四步走：找变化前后的物质、比较是不是同一种、得出结论、补充证据。",
        "conceptest-1": "这三个说法都是高频错误，看清每一个错在哪里。",
        "synthesis": "到厨房和教室里去找，每一种都要说出判断依据。",
        "posttest": "换了火柴、气球和土豆丝的新情境，看看你还能不能判断准确。",
        "summary": "回到开头那两支蜡烛：一支是物理变化，一支是化学变化，差别在哪里？",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是「物质的变化与化学反应」在小学段的空缺：知识树原有水的三态变化、溶解现象，但没有任何一课处理课标明确要求的「物质变化的特征」。设计上把判据收敛为一句学生能带走的话——有没有产生新物质；再用八张分类卡和一组对比实验，专门破解「冒气泡就是化学变化」这个高频错误，最后落到防锈、厨余变色等真实情境。",
    "plan_table": """| 1 | cover | 物理变化与化学变化：物质到底变了没有？ | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：它们算不算变了？ | 起·前测 |
| 5 | concept | 形状变了、状态变了，但物质没有变 | 承·概念一（物理变化） |
| 6 | interactive | 变化分类器：八种变化，放进两个筐 | 承·分类实践（即时反馈） |
| 7 | concept | 产生了新物质，就是化学变化 | 承·概念二（含现象线索与反例） |
| 8 | interactive | 对比实验：冒气泡的一定是化学变化吗？ | 转·用反例破误解 |
| 9 | concept | 例题示范：铁钉生锈算化学变化吗 | 转·重难点突破（四步示范） |
| 10 | quiz | 概念测试：这三种说法错在哪里 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：当一次变化侦探 | 合·迁移应用 |
| 12 | quiz | 后测：换个情境，规律还在不在 | 合·后测 |
| 13 | summary | 小结：一句话记住两种变化 | 合·小结 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 对比知识结构图（已生成）：物理变化 / 化学变化 双栏标注\n- P5 变化类型示意图（已生成）：同样的形状改变，是否长出新物质\n- P7 铁钉生锈与蜡烛燃烧示意图（已生成）\n- 若需补充：小苏打与白醋实验的实拍照片、铁钉生锈前后对照照片",
}
