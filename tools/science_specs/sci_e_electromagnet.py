# -*- coding: utf-8 -*-
"""小学科学 · 电磁铁（G6）—— 补齐课标「物质的运动与相互作用·3.2 电磁相互作用」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/sci-e-electromagnet-fig1.webp'
F2 = './assets/sci-e-electromagnet-fig2.webp'

TTS = {
    "hero": "看一个神奇的装置。一根普通的铁钉，上面绕了几圈导线，接上电池，它就变成了一块磁铁，能把大头针一根一根地吸起来。可你一把开关断开，大头针就哗啦一下全掉了，铁钉又变成了一根最普通的铁钉。这节课我们就来弄明白，这根铁钉为什么一通电就有磁力，断电又为什么马上消失，还有，怎样才能让它吸得更多。",
    "problem-anchor": "开始之前，先选一个你最想弄明白的问题。是想知道电磁铁是怎么做出来的，还是想知道怎么让它吸起更多的大头针，又或者你想弄懂它和普通磁铁到底有什么不一样。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出电磁铁是把导线绕在铁芯上做成的，通电才有磁性。第二，能说出电磁铁的磁力大小与电流大小、线圈匝数、有没有铁芯有关。第三，知道断电以后电磁铁的磁性会消失，这是它和永久磁铁最大的不同。第四，能举例说明电磁铁在生活里的用处，比如电磁起重机。",
    "pretest": "先做三道小题，凭你现在的想法选就行，选错了也没关系，正好知道要重点听哪里。选完立刻会出现解释。",
    "module-1": "我们先认识电磁铁是怎么来的。把一根导线沿着同一个方向绕在一根铁棒上，绕得紧紧的，再把导线的两头接到电池上，一个电磁铁就做好了。它有三个零件：线圈就是绕起来的那圈导线，铁芯就是那根铁棒，再加上提供电的电池。接通电，它就有磁力；断开电，磁力马上消失。请特别注意，绕导线的时候方向要一致，一会儿往左绕一会儿往右绕，磁力就会互相抵消。",
    "lab-1": "现在你来当实验员，亲手试试怎么让电磁铁更有劲。下面有两条滑块和一个开关：一条调线圈的匝数，一条调电池的节数，还有一个按钮决定要不要插铁芯。每调一次，都会告诉你它能吸起多少枚大头针。请你做三组对比：只改匝数，看看有什么变化；只改电池节数，看看有什么变化；最后把铁芯抽出来，看看会怎样。",
    "module-2": "从刚才的实验里，我们得到三条经验。第一，线圈匝数越多，磁力越大。第二，电池节数越多，电流越大，磁力也越大。第三，插上铁芯以后磁力会强很多，因为铁芯本身容易被磁化，它能把磁性放大。还有一件最重要的事：只要一断电，磁性就全部消失了。这正是电磁铁和永久磁铁最大的不同——永久磁铁的磁性一直都在，而电磁铁听开关的话。",
    "lab-2": "现在请你做一个对比实验。左边是我们刚做的电磁铁，右边是一块永久磁铁。先给电磁铁通上电，两边都能吸大头针；然后把开关断开，看看会发生什么。你会发现左边的大头针全掉下来了，右边的纹丝不动。这个对比，就是电磁铁最了不起的地方。",
    "worked-example": "我们一起分析一道题。同一个电磁铁，接一节电池时能吸起六枚大头针，换成两节电池就能吸起十几枚。为什么？第一步，看清条件，线圈匝数没变，铁芯没变，只改了电池节数。第二步，想清楚电池节数变了会带来什么变化，两节电池让电流变大。第三步，得出结论，电流越大，电磁铁的磁力越大，所以吸起来的大头针变多了。第四步，回头检查，如果题目问的是换成更粗的铁芯，那结论就不一样了，所以一定要看清楚到底改的是哪一个条件。",
    "conceptest-1": "接下来用三个容易搞混的说法考考你。请仔细读每一个选项，选完再看解释。",
    "synthesis": "学到这里，请你当一次小工程师。任务是这样的：请你在不换电池节数的前提下，设计一个能吸起八枚大头针的电磁铁。你要写清楚三个可以调整的地方，并说明每一个调整为什么管用。写完以后，把方案说给同桌听，请他指出哪一条理由还不够清楚。",
    "posttest": "最后一轮，用新的情境检验一下。这次会出现电磁起重机、电铃和门禁卡，看看你能不能把学到的规律用上去。",
    "summary": "这节课我们抓住三件事。第一，把导线绕在铁芯上，再接到电池上，就做成了一个电磁铁，通电有磁性，断电没磁性。第二，电磁铁的磁力大小跟三个东西有关：线圈的匝数、电流的大小、有没有铁芯。匝数越多、电流越大、有铁芯，磁力就越强。第三，断电以后磁性立刻消失，这是电磁铁与永久磁铁最大的不同。回到开头那根铁钉：通电时它是一块磁铁，断开开关，它又变回一根普通铁钉。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出电磁铁是由哪几个部分组成的，并说出它的磁力大小跟哪三个因素有关。第二层能力应用，动手做：用一根铁钉、一段导线和一节电池做一个电磁铁，试一试它能吸起几枚大头针，把结果记下来。第三层迁移挑战，选做：查一查电磁铁在生活里的三种用途，选其中一种，说清楚人们是用什么办法来控制它的磁力大小的。",
    "knowledge-graph": "这张图展示了这节课在科学知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 电磁铁的组成", "lab-1": "实验室一 电磁铁实验台", "module-2": "概念二 磁力跟什么有关",
    "lab-2": "实验室二 电磁铁对永久磁铁", "worked-example": "例题讲解 两节电池为什么更强", "conceptest-1": "概念测试",
    "synthesis": "综合任务 小工程师的挑战", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

CUSTOM_JS = r"""
/* ============================================================
   sci-e-electromagnet 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 电磁铁实验台：线圈匝数 × 电池节数 × 有无铁芯 → 吸起的大头针数量
   3) 电磁铁 vs 永久磁铁：断电磁性归零对比
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

  /* ---------- 2. 电磁铁实验台 ---------- */
  var stage1 = document.getElementById('em-stage');
  if (stage1) {
    var turnsR = document.getElementById('em-turns');
    var power = 1, hasCore = true, powered = true;
    var turnsOut = document.getElementById('em-turns-out');
    var pinOut = document.getElementById('em-pins');
    var barOut = document.getElementById('em-bar');
    var out = document.getElementById('em-out');
    var coil = document.getElementById('em-coil');
    var coreEl = document.getElementById('em-core');

    function pinCount() {
      var t = Number(turnsR.value);
      var raw = t * power * (hasCore ? 0.35 : 0.05);
      return Math.max(0, Math.round(raw));
    }

    function renderCoil(turns) {
      var n = Math.max(3, Math.round(turns / 2));
      var parts = [];
      for (var i = 0; i < n; i++) {
        parts.push('<span style="position:absolute;left:0;right:0;height:7px;border-radius:4px;background:#c1662f;border:1px solid #a1511f;top:' +
          (i * (100 / n)) + '%"></span>');
      }
      coil.innerHTML = parts.join('');
    }

    function render() {
      var t = Number(turnsR.value);
      turnsOut.textContent = t + ' 匝';
      renderCoil(t);
      coreEl.style.background = hasCore ? '#9aa7b8' : 'transparent';
      coreEl.style.borderColor = hasCore ? '#7d8a9c' : '#cfd8e3';
      coreEl.textContent = hasCore ? '' : '空';

      var pins = powered ? pinCount() : 0;
      pinOut.textContent = pins + ' 枚';
      var pct = Math.min(100, pins / 32 * 100);
      barOut.style.width = pct + '%';
      barOut.style.background = pins === 0 ? '#cfd8e3' : (pins < 8 ? '#f4a261' : (pins < 20 ? '#ff8a5b' : '#e63946'));

      document.querySelectorAll('[data-em-power]').forEach(function (b) {
        b.classList.toggle('selected', Number(b.dataset.emPower) === power);
      });
      document.getElementById('em-core-btn').textContent = hasCore ? '抽走铁芯' : '插上铁芯';
      document.getElementById('em-power-btn').textContent = powered ? '断开开关' : '接通电源';
      document.getElementById('em-power-btn').classList.toggle('wrong', !powered);

      if (!powered) {
        out.className = 'result warn';
        out.innerHTML = '<strong>开关断开了：吸起 0 枚大头针。</strong>' +
          '断电以后，铁芯的磁性立刻消失，吸住的大头针会全部掉下来。这就是电磁铁与永久磁铁最大的不同——它听开关的话。';
        return;
      }
      var msg;
      if (pins === 0) {
        msg = '<strong>一枚也吸不起来。</strong>线圈太少、电流太小，磁力还不够。试试增加匝数或者多接一节电池。';
        out.className = 'result error';
      } else if (!hasCore) {
        msg = '<strong>抽走铁芯以后，只能吸起 ' + pins + ' 枚。</strong>' +
          '线圈和电池都没变，磁力却弱了很多——这说明铁芯能把磁性放大好几倍，它是电磁铁不可缺少的一部分。';
        out.className = 'result warn';
      } else if (power >= 2 && Number(turnsR.value) >= 25) {
        msg = '<strong>现在是 ' + Number(turnsR.value) + ' 匝、' + power + ' 节电池、有铁芯，能吸起 ' + pins + ' 枚大头针。</strong>' +
          '匝数多、电流大、有铁芯，三个条件都占了，磁力最强。<br><strong>安全提醒：</strong>通电时间不能太长，导线和电池会发热，做完实验要及时断开。';
        out.className = 'result';
      } else {
        msg = '<strong>现在是 ' + Number(turnsR.value) + ' 匝、' + power + ' 节电池、' + (hasCore ? '有铁芯' : '无铁芯') +
          '，能吸起 ' + pins + ' 枚大头针。</strong>换一个条件再试试，看看哪一个条件对磁力的影响最大。';
        out.className = 'result';
      }
      out.innerHTML = msg;
    }

    turnsR.addEventListener('input', render);
    document.querySelectorAll('[data-em-power]').forEach(function (b) {
      b.addEventListener('click', function () { power = Number(b.dataset.emPower); render(); });
    });
    document.getElementById('em-core-btn').addEventListener('click', function () { hasCore = !hasCore; render(); });
    document.getElementById('em-power-btn').addEventListener('click', function () { powered = !powered; render(); });
    render();
  }

  /* ---------- 3. 电磁铁 vs 永久磁铁 ---------- */
  var cmp = document.getElementById('cmp-stage');
  if (cmp) {
    var out2 = document.getElementById('cmp-out');
    var emPins = document.getElementById('cmp-em-pins');
    var pmPins = document.getElementById('cmp-pm-pins');
    var emBox = document.getElementById('cmp-em-box');
    var on = true;

    function render2() {
      var n = on ? 9 : 0;
      emPins.textContent = n + ' 枚';
      pmPins.textContent = '9 枚';
      emBox.style.borderColor = on ? 'rgba(255,107,107,.75)' : 'rgba(191,155,96,.35)';
      emBox.style.background = on ? 'rgba(255,107,107,.08)' : '#fdf7ea';
      document.getElementById('cmp-switch').textContent = on ? '断开开关' : '接通电源';
      document.getElementById('cmp-switch').classList.toggle('wrong', !on);
      if (on) {
        out2.className = 'result';
        out2.innerHTML = '<strong>通电：两边都能吸起大头针。</strong>' +
          '电磁铁吸住 9 枚，永久磁铁也吸住 9 枚，这时候它们看起来没什么两样。';
      } else {
        out2.className = 'result error';
        out2.innerHTML = '<strong>断电：大头针全掉下来了！</strong>' +
          '电磁铁吸起的数量从 9 枚变成 0 枚，而右边的永久磁铁纹丝不动。' +
          '<br><strong>错因提醒：</strong>常见错误是误认为电磁铁断电后还留着一部分磁性。' +
          '电磁铁的磁是电流带来的，电流一停，磁性立刻消失，这是它与永久磁铁最本质的区别。';
      }
    }

    document.getElementById('cmp-switch').addEventListener('click', function () { on = !on; render2(); });
    document.getElementById('cmp-reset').addEventListener('click', function () { on = true; render2(); });
    render2();
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：铁钉怎么会变成磁铁？", TTS["pretest"], [
        {"q": "把导线绕在铁钉上接到电池，铁钉就能吸起大头针。一断开开关，大头针：",
         "options": [("全部掉下来，磁力消失了", True),
                     ("还牢牢吸着，因为铁钉已经有磁性了", False),
                     ("掉下来一半，还剩一半", False)],
         "explain": "电磁铁的磁来自电流，断电就消失。<strong>错因提醒：</strong>很多同学把电磁铁和永久磁铁搞混了，误认为通电以后铁钉就永远带上磁性。其实断开的瞬间，它又变回一根普通铁钉。"},
        {"q": "想让同一个电磁铁吸起更多的大头针，下面哪个做法可行？",
         "options": [("把线圈多绕几圈，或者多接一节电池", True),
                     ("把铁钉换成木棒", False),
                     ("把导线的方向改成反过来绕", False)],
         "explain": "匝数越多、电流越大，磁力越强。<strong>错因提醒：</strong>换木棒是常见错误——木棒不能被磁化，没有铁芯的电磁铁磁力会弱很多，甚至吸不起东西。"},
        {"q": "做电磁铁实验时，下面哪种做法是安全的？",
         "options": [("只用干电池供电，做完就断开开关", True),
                     ("把导线直接插到家里的插座上", False),
                     ("让电磁铁一直通电一整天", False)],
         "explain": "电磁铁实验只能用干电池这类低压电源。<strong>错因提醒：</strong>千万不要用家用插座做实验，也绝不要用导线直接连接电池的两极——那样会造成短路，电池和导线会迅速发烫，有危险。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "通电导线绕在铁芯上，就构成了电磁铁", TTS["module-1"], f'''
        <div class="kid-note" style="margin-bottom:12px"><span class="emoji">🧲</span><div><strong>你已经知道：</strong>磁铁能吸起铁钉。<strong>但问题是：</strong>一根普通的铁棒，自己并不会吸铁。<strong>所以我们要学的是：</strong>怎样用电流把一根普通铁棒变成磁铁，以及它的磁力大小到底由什么决定。</div></div>
        <p style="font-size:17px;margin:0 0 12px">把导线沿着同一个方向绕在铁芯上，两端接到电池，就做成了一个<strong>电磁铁</strong>。它有磁性，能把大头针吸起来。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>三个组成部分</strong></p>
            <p style="color:var(--muted)"><strong>线圈</strong>（绕起来的导线）、<strong>铁芯</strong>（中间的铁棒）、<strong>电源</strong>（电池）。</p>
          </div>
          <div class="inner-card">
            <p><strong>一个关键要求</strong></p>
            <p style="color:var(--muted)">绕导线时方向要<strong>一致</strong>。一会儿左绕一会儿右绕，磁力会互相抵消。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="电磁铁结构示意图：铁芯、线圈、导线、电池与开关的中文标注">
          <figcaption>电磁铁的结构：中间是铁芯，外面一圈一圈绕的是线圈，导线两端接到电池，中间用一个开关控制通断</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🔌</span><div><strong>一句口诀记住它：</strong>导线绕铁芯，接上电池就有磁性。它把<strong>电能</strong>变成了<strong>磁能</strong>——通电才有磁，断电磁就没。</div></div>
{insight_box([
    {"lens": "看见它", "text": "电磁起重机、电铃、电动玩具里的马达，里面都藏着电磁铁。它们工作的时候，都在重复通电与断电这两个动作。"},
    {"lens": "拆开它", "text": "为什么中间要放铁芯？因为铁很听话，容易被磁化。放了铁芯，同样的电流能做出更强的磁力，相当于给磁力加了个放大器。"},
    {"lens": "迁移它", "text": "磁悬浮列车能在轨道上飘起来，靠的也是电磁铁：电一控制，磁力就跟着变，列车就能被精确地托起和推动。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "电磁铁实验台：三个条件，你来调", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">调一调线圈匝数和电池节数，再试试抽走铁芯，看看能吸起多少枚大头针。每次只改一个条件，才能看出是谁在起作用。</p>
        <div class="lab-panel">
          <div class="lab-stage" id="em-stage" style="height:250px;background:linear-gradient(180deg,#f7fbff 0%,#eef4fb 100%)">
            <div style="position:absolute;left:50%;top:16%;bottom:16%;transform:translateX(-50%);width:54px;border-radius:8px;border:2px dashed #cfd8e3" id="em-core"></div>
            <div id="em-coil" style="position:absolute;left:50%;top:16%;bottom:16%;transform:translateX(-50%);width:54px"></div>
            <div style="position:absolute;left:calc(50% + 52px);top:16%;font-size:13px;color:#94866c">线圈 + 铁芯</div>
            <div style="position:absolute;left:10%;bottom:14%;width:76px;height:44px;border-radius:8px;background:#3a3126;display:grid;place-items:center;color:#ffd166;font-size:12px;font-weight:800">电池</div>
            <div style="position:absolute;left:calc(50% - 26px);bottom:30%;width:5px;height:26px;background:#c1662f"></div>
            <div style="position:absolute;left:14%;bottom:calc(14% + 52px);font-size:13px;color:#94866c">大头针</div>
            <div style="position:absolute;left:16%;bottom:calc(14% + 14px);display:flex;gap:3px" id="em-pins-box">
              <span style="width:3px;height:22px;background:#9aa7b8;border-radius:2px"></span>
              <span style="width:3px;height:22px;background:#9aa7b8;border-radius:2px"></span>
              <span style="width:3px;height:22px;background:#9aa7b8;border-radius:2px"></span>
            </div>
          </div>
          <div class="slider-row">
            <label for="em-turns">线圈匝数</label>
            <input type="range" id="em-turns" min="5" max="30" step="5" value="15" style="flex:1;min-width:150px">
            <span id="em-turns-out" style="font-weight:800;color:#e05555">15 匝</span>
          </div>
          <div class="slider-row" style="display:block">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">电池节数</div>
            <div class="flex-row" style="margin-top:0">
              <button class="choice selected" data-em-power="1" style="text-align:center">1 节电池</button>
              <button class="choice" data-em-power="2" style="text-align:center">2 节电池</button>
              <button class="choice" data-em-power="3" style="text-align:center">3 节电池</button>
            </div>
          </div>
          <div class="flex-row">
            <button class="choice" id="em-core-btn" style="text-align:center">抽走铁芯</button>
            <button class="choice" id="em-power-btn" style="text-align:center">断开开关</button>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">吸起的大头针</span><span class="v" id="em-pins">8 枚</span></div>
            <div class="readout-cell" style="flex:2"><span class="k">磁力大小</span>
              <div style="margin-top:10px;height:14px;border-radius:7px;background:#eef4fb;overflow:hidden">
                <div id="em-bar" style="height:100%;width:25%;background:#f4a261;transition:width .3s,background .3s"></div>
              </div>
            </div>
          </div>
          <p class="result warn" id="em-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">⚠️</span><div><strong>安全提示：</strong>电磁铁实验只能用 1.5 伏的干电池，<strong>绝对不要用家用插座做实验</strong>。导线不要直接连接电池的两极，那样会短路发热。通电时间不要太长，做完实验及时断开开关。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "匝数越多、电流越大、有铁芯，磁力就越强", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">同一个电磁铁，为什么有的能吸一大把大头针，有的连一枚都吸不动？因为<strong>磁力的大小</strong>跟三个条件有关。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>线圈匝数：</strong>绕得越多，磁力越大。</div></div>
          <div class="step"><span class="n">2</span><div><strong>电流大小：</strong>电池节数越多，电流越大，磁力越大。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>有无铁芯：</strong>插上铁芯，磁力会强好几倍；抽走铁芯，磁力立刻变弱。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="电磁铁与永久磁铁对比图：通电吸起大头针，断电大头针全部掉落">
          <figcaption>左边是电磁铁：通电吸住大头针，一断电全部掉落；右边是永久磁铁：不管有没有电，它一直都有磁性</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">特别注意</span>
          <p style="margin:6px 0 0">有的同学认为只要通电，铁芯就会<strong>永远</strong>带上磁性，这是不对的。实验做完要断开开关，否则电池很快就耗光了，导线还会发热。要记住：电磁铁的磁性<strong>随电流来、随电流走</strong>。</p>
        </div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "电磁铁对永久磁铁：断电以后谁还在吸？", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">左边是电磁铁，右边是永久磁铁。先通电，再断开，比较两边吸住的大头针数量。这个对比，就是电磁铁最大的特点。</p>
        <div class="lab-panel">
          <div class="lab-stage" id="cmp-stage" style="height:250px;background:linear-gradient(180deg,#fbf8f1 0%,#f4eede 100%);display:flex;gap:16px;padding:14px">
            <div id="cmp-em-box" style="flex:1;border-radius:14px;border:2px solid rgba(255,107,107,.75);background:rgba(255,107,107,.08);position:relative">
              <div style="position:absolute;top:8px;left:12px;font-size:13px;font-weight:800;color:#c2410c">电磁铁</div>
              <div style="position:absolute;left:50%;top:34px;bottom:56px;transform:translateX(-50%);width:20px;border-radius:6px;background:#9aa7b8"></div>
              <div style="position:absolute;left:50%;top:34px;transform:translateX(-50%);width:20px;height:60px;background:repeating-linear-gradient(180deg,#c1662f 0 7px,transparent 7px 10px)"></div>
              <div style="position:absolute;left:50%;bottom:16px;transform:translateX(-50%);text-align:center">
                <div style="font-size:12px;color:#94866c">吸起大头针</div>
                <div style="font-size:22px;font-weight:800;color:#e05555" id="cmp-em-pins">9 枚</div>
              </div>
            </div>
            <div style="flex:1;border-radius:14px;border:2px solid rgba(78,205,196,.6);background:rgba(78,205,196,.08);position:relative">
              <div style="position:absolute;top:8px;left:12px;font-size:13px;font-weight:800;color:#0f6f68">永久磁铁</div>
              <div style="position:absolute;left:50%;top:56px;bottom:56px;transform:translateX(-50%);width:44px;border-radius:6px;background:linear-gradient(180deg,#ef4444 0 50%,#3b82f6 50% 100%)"></div>
              <div style="position:absolute;left:50%;bottom:16px;transform:translateX(-50%);text-align:center">
                <div style="font-size:12px;color:#94866c">吸起大头针</div>
                <div style="font-size:22px;font-weight:800;color:#14897f" id="cmp-pm-pins">9 枚</div>
              </div>
            </div>
          </div>
          <div class="flex-row">
            <button class="choice" id="cmp-switch" style="text-align:center">断开开关</button>
            <button class="choice" id="cmp-reset" style="text-align:center">重新通电</button>
          </div>
          <p class="result" id="cmp-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧠</span><div><strong>想一想：</strong>为什么电磁起重机用电磁铁，而不用永久磁铁？因为电磁铁能<strong>听开关的话</strong>——吸起废铁时通电，运到地方断电磁就没了，废铁自己掉下去，非常方便。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：两节电池为什么吸得更多？", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>同一个电磁铁，接一节电池时吸起 6 枚大头针，换成两节电池后吸起 14 枚。请解释原因。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看清条件：</strong>线圈匝数没变、铁芯没变，只把电池从 1 节换成了 2 节。</div></div>
          <div class="step"><span class="n">2</span><div><strong>想变化：</strong>电池节数增加，电路里的电流变大。</div></div>
          <div class="step"><span class="n">3</span><div><strong>得出结论：</strong>电流越大，电磁铁的磁力越大，所以能吸起更多大头针。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>回头检查：</strong>题目只改了电池这一个条件，所以结论只能落在电流上；如果同时换了铁芯，就必须重新分析。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错法</span>
          <p style="margin:6px 0 0">有的同学写成「因为两节电池的磁性更强」——这就把电池和磁铁搞混了。电池本身没有磁性，它提供的是<strong>电流</strong>，是电流让线圈产生磁性。还有同学误认为吸得更多是因为铁芯变粗了，但题目里铁芯根本没有换过。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "下面哪句话是正确的？",
         "options": [("电磁铁的磁力大小与线圈匝数、电流大小、有无铁芯有关", True),
                     ("电磁铁通电以后就变成永久磁铁了", False),
                     ("电磁铁的磁力大小只跟铁芯的粗细有关", False)],
         "explain": "磁力由匝数、电流、铁芯三个条件共同决定。<strong>错因提醒：</strong>最常见的错误是把电磁铁和永久磁铁搞混。电磁铁断电就没有磁性，永远变不成永久磁铁。"},
        {"q": "把电磁铁里的铁芯抽走，其他条件都不变，它的磁力会：",
         "options": [("明显变弱，可能连一枚大头针都吸不起来", True),
                     ("变得更强", False),
                     ("完全不变", False)],
         "explain": "铁芯被磁化后能大幅增强磁性，抽走它就失去了这个放大器。<strong>错因提醒：</strong>有同学误认为线圈自己就够用了，其实没有铁芯的线圈磁力很弱。"},
        {"q": "关于电磁铁通电时的做法，正确的是：",
         "options": [("通电时间不要太长，做完实验及时断开开关", True),
                     ("为了磁力最大，一直通电不要关", False),
                     ("把导线直接接在插座上，磁力会更强", False)],
         "explain": "长时间通电会让电池耗光、导线发热，用完要及时断开。<strong>错因提醒：</strong>用家用插座做实验是极其危险的常见错误——实验一律使用干电池这类低压电源。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：当一次小工程师", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">挑战来了：不增加电池节数，请你设计一个能吸起 8 枚大头针的电磁铁。写出三个可以调整的地方，并说明每个调整为什么管用。</p>
        <div class="inner-card">
          <p><strong>第一步：写下你的三个调整</strong></p>
          <textarea id="syn-plan" rows="3" placeholder="调整 1：＿＿＿＿，因为＿＿＿＿&#10;调整 2：＿＿＿＿，因为＿＿＿＿&#10;调整 3：＿＿＿＿，因为＿＿＿＿"></textarea>
        </div>
        <div class="inner-card">
          <p><strong>第二步：说明为什么管用</strong></p>
          <p style="color:var(--muted)">每一条理由里都要出现「磁力」这个词。比一比，哪一个调整对磁力的影响最大？</p>
          <textarea id="syn-why" rows="2" placeholder="我认为影响最大的是＿＿＿＿，因为＿＿＿＿"></textarea>
        </div>
        <div class="inner-card">
          <p><strong>第三步：说给同桌听</strong></p>
          <p style="color:var(--muted)">用「线圈匝数、电流、铁芯」这三个词，把你的方案完整讲一遍。</p>
        </div>
        <div class="kid-note"><span class="emoji">⚠️</span><div><strong>安全提示：</strong>动手做的时候，只能用 1.5 伏干电池，<strong>不要用家用插座做实验</strong>；导线不要直接连接电池两极，避免短路发热；做完实验马上断开开关。</div></div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换个情境，规律还在不在", TTS["posttest"], [
        {"q": "电磁起重机能把废铁吸起来，又能在运到地方后把废铁放下。它靠的是：",
         "options": [("用通断电流来控制电磁铁的磁性，需要时通电、放下时断电", True),
                     ("用工人用手把废铁掰下来", False),
                     ("用一块特别大的永久磁铁，靠人推下来", False)],
         "explain": "电磁起重机用通断电控制磁性，所以能吸起也能放下。<strong>错因提醒：</strong>永久磁铁的磁性关不掉，用它就没法把废铁自动放下来——这个对比正好说明了电磁铁的长处。"},
        {"q": "电铃能不停地响，是因为铃里有一个电磁铁在反复地：",
         "options": [("通电吸引小锤，断电小锤弹回，来回敲打", True),
                     ("给铃铛加热让它发声", False),
                     ("一直通电不动，靠振动发声", False)],
         "explain": "电铃靠电磁铁的反复通断电带动小锤敲击。<strong>错因提醒：</strong>很多同学误认为电铃里的磁铁是永久磁铁，其实正因为它能一通电一断电，小锤才会不停地敲。"},
        {"q": "同一个电磁铁，把线圈从 10 匝增加到 20 匝，磁力会：",
         "options": [("变大", True), ("变小", False), ("不变", False)],
         "explain": "匝数增加，磁力变大。<strong>错因提醒：</strong>注意不要跟「绕线方向」搞混——匝数多少影响磁力的<strong>大小</strong>，而绕线方向一致与否影响的是磁力能不能叠加起来。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把电磁铁讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>怎么做</strong>：把导线沿同一方向绕在<strong>铁芯</strong>上，两端接到电池，就做成了电磁铁。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>磁力跟什么有关</strong>：线圈<strong>匝数</strong>越多、<strong>电流</strong>越大、有<strong>铁芯</strong>，磁力就越强。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>最大的不同</strong>：一断电，磁性立刻<strong>消失</strong>；永久磁铁的磁性却一直都在。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那根铁钉：</strong>通电的时候，线圈里的电流让铁芯带上了磁性，它就成了磁铁；开关一断，电流没了，磁性也立刻消失，大头针只能全部掉下来。它把电能变成了磁能。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「线圈、铁芯、电流」这三个词，说清楚怎样才能让电磁铁吸起更多的大头针。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "写出电磁铁由哪几个部分组成，并说出它的磁力大小跟哪三个因素有关。",
            "用一句话说明电磁铁与永久磁铁最大的不同是什么。",
        ],
        [
            "用一根铁钉、一段导线和一节干电池做一个电磁铁，试试能吸起几枚大头针，把结果记下来。",
            "把线圈匝数增加一倍，再试一次，把两次的数据填进表格，比较有什么变化。",
        ],
        [
            "查找电磁铁在生活里的三种用途（例如电磁起重机、电铃、门禁卡），选其中一种，说清楚人们是用什么办法控制它磁力大小的。",
            "设计一个能自动把废铁吸起又放下的装置示意图，并写明通电和断电分别在什么时候发生。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "sci-e-electromagnet",
    "node_id": "sci-e-electromagnet",
    "title": "电磁铁：通电就有磁力的铁棒",
    "name_en": "Electromagnet: A powered magnet",
    "grade": 6,
    "grade_cn": "六年级",
    "domain": "matter-science",
    "domain_cn": "物质科学 · 电与磁",
    "lesson_type": "experiment-inquiry",
    "version": "1.0.0",
    "description": "用电池、导线和铁芯制作电磁铁，通过调匝数、调电池节数、抽插铁芯三个对比实验，发现电磁铁的磁力大小与线圈匝数、电流大小、有无铁芯有关；通过与永久磁铁的对比，认识断电后磁性消失这一本质区别。",
    "tags": ["电磁铁", "铁芯", "线圈", "电流", "磁力", "永久磁铁", "电磁起重机"],
    "standard_ref": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念3「物质的运动与相互作用」学习内容3.2 电磁相互作用——5～6年级用电池、铁棒、导线等制作一个电磁铁，观察电磁铁产生磁力的现象，体会电能转化成磁能。",
    "hero_question": "一根普通铁钉，接上电池就能吸大头针，一断电又马上松开——这是怎么回事？",
    "hero_alt": "电磁铁知识结构图：电磁铁的组成、磁力大小的影响因素、与永久磁铁的区别",
    "hero_caption": "电磁铁：导线绕铁芯 + 电池 ｜ 匝数越多、电流越大、有铁芯，磁力越强 ｜ 断电即失磁，这是它最大的特点",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的实验都会围着它转。",
    "anchor_choices": [
        {"t": "电磁铁是怎么做出来的？", "d": "想知道铁钉为什么能变成磁铁", "v": "电磁铁是怎么做出来的"},
        {"t": "怎样才能吸起更多大头针？", "d": "想找到让磁力变强的办法", "v": "怎样才能吸起更多大头针"},
        {"t": "它和普通磁铁有什么不一样？", "d": "想知道断电以后磁力去哪儿了", "v": "它和普通磁铁有什么不一样"},
        {"t": "生活里哪里用到了电磁铁？", "d": "想弄懂电磁起重机怎么干活", "v": "生活里哪里用到了电磁铁"},
    ],
    "objectives": [
        "能说出电磁铁是用导线绕在铁芯上做成的，通电时有磁性",
        "能说出电磁铁的磁力大小与线圈匝数、电流大小、有无铁芯有关",
        "知道电磁铁断电后磁性会消失，并能说出它与永久磁铁最大的不同",
        "能举例说明电磁铁在生活中的应用，体会电能可以转化成磁能",
    ],
    "objectives_plain": [
        "能说出电磁铁是用导线绕在铁芯上做成的，通电时有磁性",
        "能说出电磁铁的磁力大小与线圈匝数、电流大小、有无铁芯有关",
        "知道电磁铁断电后磁性会消失，并能说出它与永久磁铁最大的不同",
        "能举例说明电磁铁在生活中的应用，体会电能可以转化成磁能",
    ],
    "standards": [
        {"content": "用电池、铁棒、导线等制作一个电磁铁，观察电磁铁产生磁力的现象，体会电能转化成磁能",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念3 物质的运动与相互作用·3.2 电磁相互作用（5～6年级）"},
        {"content": "能通过控制变量的对比实验，找出影响电磁铁磁力大小的因素，并用证据说明结论",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》科学思维·推理论证（5～6年级）"},
    ],
    "prereqs": ["sci-e-electricity-basic"],
    "prereqs_name": "简单电路",
    "prereqs_meta": "sci-e-electricity-basic",
    "leads_to": ["sci-e-simple-robot"],
    "next_meta": "sci-e-simple-robot",
    "section_images": ["assets/sci-e-electromagnet-fig1.webp", "assets/sci-e-electromagnet-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "通电就吸针，断电就掉针——一根铁钉怎么做到的？",
        "problem-anchor": "先定一个小目标：这节课结束时，你能自己做电磁铁，还能说清怎么让它更有劲。",
        "objectives": "看清四件事：怎么制作、磁力跟什么有关、与永久磁铁的区别、生活里的应用。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "线圈、铁芯、电源，三样凑齐就是电磁铁。绕线方向要一致。",
        "lab-1": "每次只改一个条件：先只改匝数，再只改电池数，最后抽走铁芯。",
        "module-2": "匝数、电流、铁芯，三样都能让磁力变强；断电以后磁性立刻为零。",
        "lab-2": "通电两边一样，断电差距就出来了——这正是电磁铁的价值所在。",
        "worked-example": "四步走：看清条件、想变化、下结论、回头检查。注意别把电池和磁铁搞混。",
        "conceptest-1": "干扰项里藏着最常见的那几个错误想法，选完看清每一个解释。",
        "synthesis": "不能加电池，那就只能在匝数和铁芯上想办法了。",
        "posttest": "换了起重机、电铃和增加匝数的新情境，看看你还能不能用上同一条规律。",
        "summary": "回到开头那根铁钉：通电和断电，它到底发生了什么变化？",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是「电磁相互作用」在小学高段的空缺：知识树原有简单电路、磁铁与磁现象，但没有任何一课处理课标明确要求的电磁铁制作与探究。设计上把电磁铁收敛为一个可反复操作的三变量实验——匝数、电池节数、有无铁芯，用吸起的大头针数量作为可比较的证据；再用电磁铁对永久磁铁的断电对比，把「磁性随电流来、随电流走」这个本质区别钉牢，最后落到电磁起重机等真实应用。",
    "plan_table": """| 1 | cover | 电磁铁：通电就有磁力的铁棒 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：铁钉怎么会变成磁铁？ | 起·前测（暴露直觉） |
| 5 | concept | 通电导线绕在铁芯上，就构成了电磁铁 | 承·概念一（结构与能量转化） |
| 6 | interactive | 电磁铁实验台：三个条件，你来调 | 承·实验室一（三变量对比） |
| 7 | concept | 匝数越多、电流越大、有铁芯，磁力就越强 | 承·概念二（规律与安全） |
| 8 | interactive | 电磁铁对永久磁铁：断电以后谁还在吸？ | 承·实验室二（断电对比） |
| 9 | concept | 例题示范：两节电池为什么吸得更多？ | 转·重难点突破（控制变量 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：当一次小工程师 | 合·迁移应用 |
| 12 | quiz | 后测：换个情境，规律还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把电磁铁讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：电磁铁组成、磁力影响因素、与永久磁铁的区别三栏标注\n- P5 电磁铁结构图（已生成）：铁芯、线圈、导线、电池、开关中文标注\n- P7 电磁铁与永久磁铁对比图（已生成）：通电吸针 / 断电针掉 / 永久磁铁始终有磁性\n- 若需补充：电磁起重机实景照片、真实电磁铁实验装置照片",
}
