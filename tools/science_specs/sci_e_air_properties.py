# -*- coding: utf-8 -*-
"""小学科学 · 空气：看不见，但它占地方（G3）—— 补齐课标「物质的结构与性质·1.2 空气与水是重要的物质」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/sci-e-air-properties-fig1.webp'
F2 = './assets/sci-e-air-properties-fig2.webp'

TTS = {
    "hero": "我们来猜一个谜语。有一个东西，你看不见，也摸不着。可是你吹气球的时候，是它把气球撑得鼓鼓的。风吹过来的时候，是它把树叶吹得哗哗响。你一分钟也离不开它。它是谁呢？对啦，它就是空气。今天我们就当一次小研究员，一起去找一找，空气到底藏在哪儿，它又会做哪些事。",
    "problem-anchor": "开始之前，先选一个你最想知道的问题。是空气到底在哪里，还是空气有没有重量，又或者你只想知道，杯子里那张纸为什么不会湿。选好以后，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出空气就在我们身边，它看不见，但真的存在。第二，能说出空气会占地方。第三，能说出空气有质量，还会流动。第四，能说出空气是我们呼吸必需的东西。",
    "pretest": "先做三道小题。你不用怕选错，凭自己现在的想法选就行。选完马上会告诉你为什么。",
    "module-1": "我们先做一个小实验。把一团纸塞在杯子底部，杯口朝下，竖直按进水里。猜一猜，纸团会湿吗？答案是不会。为什么呢？因为杯子里装满了空气，空气先占了里面的地方，水就挤不进去。我们看不见空气，可是一旦它占了位置，别的东西就进不来。这就叫空气占据空间。你要记住，空气不是空的，它实实在在待在那里。",
    "lab-1": "现在请你自己动手。左边这个杯子，你可以把它竖直倒扣着压进水里，也可以把它歪一歪。每做一步，都看看杯里的纸团变没变湿。右边还有一个针筒，推一推活塞，看看里面的空气会怎么样。",
    "module-2": "空气还会做两件事。第一件，空气有质量。给两个一样的气球挂在简易天平两边，天平是平的。只给右边那个打足气，右边就沉下去了。气球没多重，可空气也有分量，加在一起就把天平压低了。第二件，空气会流动。空气跑来跑去，就形成了风。你能感觉到风，其实就是在感觉流动的空气。",
    "lab-2": "我们来给右边的气球打气。每点一次，就多打十下气。一边打，一边看天平往哪边倒。打完之后，想一想：气球变大了一点点，为什么天平就歪了呢？",
    "worked-example": "我们来一起分析一道题。把一团纸塞在杯子底部，杯口朝下竖直按进水底，再竖直拿出来，纸团会湿吗？第一步，先看清条件，杯子是竖直按下去的，杯口一直没有歪。第二步，找原因，杯子里装满了空气，空气占了地方，水进不去。第三步，得结论，纸团不会湿。第四步，想一想，如果把杯子歪一歪呢？空气从旁边跑出去，空出来的地方马上被水填满，纸团就湿了。",
    "conceptest-1": "接下来用三个很容易弄错的说法考考你。请一个一个字读清楚，选完再看解释。",
    "synthesis": "学到这里，请你当一次空气侦探。下面有三件生活中的小事，点一点，看看你能不能用今天学的道理说清楚。看完以后，再想一想，你身边还有哪些地方用到空气。",
    "posttest": "最后再用三道题检验一下。这一次有足球、有风车、还有塑料袋，看看你还能不能说出道理。",
    "summary": "这节课我们弄明白了四件事。第一，空气看不见摸不着，但它真的在我们身边。第二，空气会占地方，杯子里的空气把水挡住了。第三，空气有质量，还会流动，风就是流动的空气。第四，空气是我们呼吸必需的东西。回到开头那个谜语，答案就是空气。",
    "homework": "最后留三项作业，分三个层次。第一层是基础巩固，人人都要做：说出空气的三个特点。第二层是能力应用，动手做：在家里找一个用得到空气的地方，说清楚空气在那里帮了什么忙。第三层是迁移挑战，选做：设计一个小实验，证明空气真的占了地方，画下来讲给同学听。",
    "knowledge-graph": "这张图会告诉你，这节课在科学知识网里的位置。左边是要先学会的内容，右边是可以接着探索的内容，下面是同一个领域的伙伴知识。点一点，看看还有哪些有意思的问题。",
    "ai-tutor": "如果还有没想明白的地方，就把你的问题写下来，问问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 空气占地方", "lab-1": "实验室一 纸团会不会湿", "module-2": "概念二 空气有质量也会流动",
    "lab-2": "实验室二 气球天平", "worked-example": "例题讲解", "conceptest-1": "概念测试",
    "synthesis": "综合任务 空气侦探", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

CUSTOM_JS = r"""
/* ============================================================
   sci-e-air-properties 互动逻辑
   1) 选择题接线
   2) 实验室一：杯子倒扣入水（竖直 / 倾斜）+ 针筒压缩空气
   3) 实验室二：给气球打气，气球天平倾斜
   4) 综合任务：三件生活小事 → 用空气占据空间解释
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

  /* ---------- 实验室一：杯子 + 针筒 ---------- */
  var stage1 = document.getElementById('air1-stage');
  if (stage1) {
    var cupWrap = document.getElementById('cup-wrap');
    var cupAir = document.getElementById('cup-air');
    var cupPaper = document.getElementById('cup-paper');
    var out1 = document.getElementById('air1-out');
    var cupState = 'deck';

    function renderCup() {
      document.querySelectorAll('[data-cup-state]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.cupState === cupState);
      });
      if (cupState === 'deck') {
        cupWrap.style.top = '6%';
        cupAir.style.opacity = '1';
        cupPaper.textContent = '干纸团';
        cupPaper.style.background = '#fffdf8';
        out1.className = 'result warn';
        out1.innerHTML = '杯子还在水面上方。杯子里装着<strong>空气</strong>，现在把它竖直倒扣着压进水里试试。';
      } else if (cupState === 'down') {
        cupWrap.style.top = '58%';
        cupAir.style.opacity = '1';
        cupPaper.textContent = '干纸团';
        cupPaper.style.background = '#fffdf8';
        out1.className = 'result';
        out1.innerHTML = '<strong>纸团没有湿！</strong>杯子里装满了空气，空气先占了地方，水就挤不进去。这就是<strong>空气占据空间</strong>。';
      } else {
        cupWrap.style.top = '58%';
        cupAir.style.opacity = '.2';
        cupPaper.textContent = '湿纸团';
        cupPaper.style.background = '#cfe6ff';
        out1.className = 'result error';
        out1.innerHTML = '<strong>纸团湿了！</strong>杯子一歪，空气从旁边跑出去了。空气一让位，水马上就填了进来。';
      }
    }
    document.querySelectorAll('[data-cup-state]').forEach(function (b) {
      b.addEventListener('click', function () { cupState = b.dataset.cupState; renderCup(); });
    });
    renderCup();

    var syrV = document.getElementById('air1-syr-v');
    var syrBar = document.getElementById('air1-syr-bar');
    var outSyr = document.getElementById('air1-syr-out');
    function setSyringe(v, msg) {
      syrV.textContent = v + ' mL';
      syrBar.style.width = (v / 30 * 100) + '%';
      outSyr.className = 'result warn';
      outSyr.innerHTML = msg;
    }
    document.getElementById('air1-syr-push').addEventListener('click', function () {
      setSyringe(12, '<strong>空气被压小了。</strong>针筒口堵住，空气跑不出去，只能挤在一起。原来占 20 毫升的空气，现在只占 12 毫升。空气没有固定的形状，可以被压缩。');
    });
    document.getElementById('air1-syr-pull').addEventListener('click', function () {
      setSyringe(27, '<strong>空气散开了。</strong>往外一拉活塞，空气跟着摊开，占的地方变大。空气总是把能占的地方都填满。');
    });
    document.getElementById('air1-syr-reset').addEventListener('click', function () {
      setSyringe(20, '活塞回到中间。针筒口是堵住的，空气一直在里面，不多也不少。再推推看，它还能变得更小。');
    });
  }

  /* ---------- 实验室二：气球天平 ---------- */
  var stage2 = document.getElementById('air2-stage');
  if (stage2) {
    var beam = document.getElementById('balance-beam');
    var balRight = document.getElementById('bal-right');
    var balLeft = document.getElementById('bal-left');
    var vPump = document.getElementById('air2-pump');
    var vTilt = document.getElementById('air2-tilt');
    var out2 = document.getElementById('air2-out');
    var pumps = 0;

    function renderBeam() {
      var deg = pumps * 3;
      beam.style.transform = 'translateX(-50%) rotate(' + deg + 'deg)';
      var size = 46 + pumps * 4;
      balRight.style.width = size + 'px';
      balRight.style.height = (size + 8) + 'px';
      balLeft.style.width = '46px';
      balLeft.style.height = '54px';
      balRight.style.background = pumps > 0 ? 'rgba(255,107,107,.22)' : 'rgba(255,255,255,.5)';
      vPump.textContent = pumps * 10 + ' 下';
      vTilt.textContent = deg + '°';
      if (pumps === 0) {
        out2.className = 'result warn';
        out2.innerHTML = '两个气球一样大，天平是平的。现在点一下按钮，只给<strong>右边</strong>那个气球打气。';
      } else if (pumps === 1) {
        out2.className = 'result';
        out2.innerHTML = '<strong>天平有一点点歪了，右边低了下去。</strong>右边只多了十几下空气，天平就有反应了。';
      } else {
        out2.className = 'result';
        out2.innerHTML = '<strong>右边越来越低。</strong>气球本身没有变重，多出来的是打进气球里的<strong>空气</strong>。空气看不见，可它确实有质量。';
      }
      out2.className = (pumps === 0) ? 'result warn' : 'result';
    }
    document.getElementById('air2-pump-once').addEventListener('click', function () {
      pumps = Math.min(pumps + 1, 3); renderBeam();
    });
    document.getElementById('air2-reset').addEventListener('click', function () {
      pumps = 0; renderBeam();
    });
    renderBeam();
  }

  /* ---------- 综合任务：空气侦探 ---------- */
  var detStage = document.getElementById('det-stage');
  if (detStage) {
    var CASES = {
      ball: '篮球打足了气就变得硬硬的。打气筒把空气挤进篮球里，空气占了篮球里面的地方，把它撑得紧紧的，拍起来才弹手。',
      pillow: '坐上去软软的空气枕，里面装满了空气。你一坐，空气被挤到别的地方；你一起来，它又占回原来的位置，所以又软又有弹性。',
      glass: '把空杯子竖直倒扣着压进水里，水进不去。因为杯子里装满了空气，空气占了地方，水只能待在外面。'
    };
    var outDet = document.getElementById('det-out');
    document.querySelectorAll('[data-det]').forEach(function (b) {
      b.addEventListener('click', function () {
        document.querySelectorAll('[data-det]').forEach(function (x) { x.classList.toggle('selected', x === b); });
        outDet.className = 'result';
        outDet.innerHTML = '<strong>' + b.textContent.trim() + '：</strong>' + CASES[b.dataset.det];
      });
    });
    outDet.className = 'result warn';
    outDet.textContent = '点上面任意一张卡片，看看空气在这里帮了什么忙。';
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：空气藏在哪里？", TTS["pretest"], [
        {"q": "一个空杯子扣在桌子上，杯子里有什么？",
         "options": [("装满了空气", True), ("什么都没有，是空的", False), ("装了半杯水", False)],
         "explain": "我们看不见空气，所以常常误认为杯子是空的。其实杯子里装满了空气。<strong>错因提醒：</strong>这是这一课最常见的错误——看不见不等于不存在。空气也是物质，它占了杯子里全部的地方。"},
        {"q": "把一团纸塞在杯子底部，杯口朝下竖直按进水里，纸团会怎样？",
         "options": [("纸团还是干的", True), ("纸团马上就湿了", False), ("纸团会掉出来", False)],
         "explain": "杯子里的空气挡住了水，水进不去，纸团就还是干的。<strong>错因提醒：</strong>有同学误认为杯子一进水纸必然湿，忽略了杯子里那份占了地方的空气。"},
        {"q": "风是什么？",
         "options": [("流动的空气", True), ("空气变重了", False), ("树叶自己在动", False)],
         "explain": "空气跑动起来就是风，我们看不到空气，只能感觉到它在流动。<strong>错因提醒：</strong>不要把风和树叶搞混——树叶是被流动的空气推着动的，风本身是空气在跑。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "空气会占地方，杯子里的空气把水挡住了", TTS["module-1"], f'''
        <p style="font-size:17px;margin:0 0 12px">我们的身边到处都是空气。你已经知道杯子看起来是空的，但有一个问题一直没弄明白：为什么倒扣进水里的杯子，纸团不会湿？答案就在杯子里那份<strong>看不见的空气</strong>上。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>空气在哪里</strong></p>
            <p style="color:var(--muted)">教室里、书包里、气球里、甚至一杯水里，都有空气。它看不见、摸不着，但到处都在。</p>
          </div>
          <div class="inner-card">
            <p><strong>空气占据空间</strong></p>
            <p style="color:var(--muted)">空气不是空的，它实实在在占着位置。一个地方被空气占了，别的东西就挤不进去。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="杯子倒扣入水的实验图：竖直按入纸团不湿，倾斜杯口纸团变湿">
          <figcaption>左边竖直倒扣，空气被关在杯里，水进不去，纸团是干的；右边把杯口一歪，空气跑掉，水立刻填进去，纸团就湿了</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🔍</span><div><strong>当一次小研究员：</strong>你可以在家试一试。拿一个透明杯子，塞一团纸巾，竖直按进水盆里，再竖直拿出来，看看纸巾到底湿了没有。记住，手不要歪。</div></div>
{insight_box([
    {"lens": "看见它", "text": "空气看不见，我们只能看它做出来的事：气球鼓起来、杯子挡住水、树叶被吹动。"},
    {"lens": "解释它", "text": "为什么水进不去杯子？因为一个地方只能待一样东西。空气已经占了杯子里全部的地方，水就没有位置了。"},
    {"lens": "迁移它", "text": "把空的矿泉水瓶按进水里，你会看到咕噜咕噜冒泡——那是空气在往外跑，它在给水让位置。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手做：纸团为什么没有湿？", TTS["lab-1"], '''
        <p style="color:var(--muted);margin:0 0 12px">先做杯子实验，再玩针筒。每做一步，读一读下面的解释。</p>
        <div class="lab-panel">
          <div class="lab-stage" id="air1-stage" style="height:260px;background:linear-gradient(180deg,#f7fbff 0%,#eaf6ff 46%,#d8ecff 46.5%,#cbe6ff 100%)">
            <div class="airline" style="top:46%"></div>
            <div id="cup-wrap" style="position:absolute;left:50%;transform:translateX(-50%);top:6%;transition:top .8s cubic-bezier(.34,1.2,.5,1)">
              <div style="width:92px;height:104px;border:4px solid #8d9bb5;border-bottom:none;border-radius:10px 10px 4px 4px;background:rgba(255,255,255,.45);position:relative">
                <div id="cup-paper" style="position:absolute;left:50%;transform:translateX(-50%);top:5px;width:58px;height:32px;background:#fffdf8;border:2px solid #e2cfa8;border-radius:4px;display:grid;place-items:center;font-size:12px;color:#5c5142">干纸团</div>
                <div id="cup-air" style="position:absolute;left:8px;right:8px;top:44px;bottom:6px;border:2px dashed rgba(78,205,196,.9);border-radius:8px;display:grid;place-items:center;font-size:12px;color:#14897f;font-weight:700;transition:opacity .4s">杯里的空气</div>
              </div>
            </div>
          </div>
          <div class="flex-row" style="margin-top:12px">
            <button class="choice" data-cup-state="deck" style="text-align:center;flex:1">① 还在水面上</button>
            <button class="choice" data-cup-state="down" style="text-align:center;flex:1">② 竖直倒扣压入水中</button>
            <button class="choice" data-cup-state="tilt" style="text-align:center;flex:1">③ 把杯口歪一歪</button>
          </div>
          <p class="result warn" id="air1-out" style="margin-top:12px"></p>
          <div style="border-top:1px dashed var(--line-subtle);margin-top:16px;padding-top:14px">
            <div style="font-weight:700;font-size:14px;margin-bottom:8px">再玩一个：堵住口的针筒，里面装着 20 mL 空气</div>
            <div style="height:14px;border-radius:999px;background:var(--bg-subtle);border:1px solid var(--line-subtle);overflow:hidden">
              <div id="air1-syr-bar" style="height:100%;width:66.7%;background:linear-gradient(90deg,#4ecdc4,#7fd8d2);transition:width .5s"></div>
            </div>
            <div class="lab-readout">
              <div class="readout-cell"><span class="k">空气占的地方</span><span class="v green" id="air1-syr-v">20 mL</span></div>
            </div>
            <div class="flex-row">
              <button class="choice" id="air1-syr-push" style="text-align:center">推活塞</button>
              <button class="choice" id="air1-syr-pull" style="text-align:center">拉活塞</button>
              <button class="choice" id="air1-syr-reset" style="text-align:center">松手复位</button>
            </div>
            <p class="result warn" id="air1-syr-out" style="margin-top:12px">活塞回到中间。针筒口是堵住的，空气一直在里面，不多也不少。再推推看，它还能变得更小。</p>
          </div>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💡</span><div><strong>做完比一比：</strong>杯口一直竖直，纸团就是干的；杯口一歪，纸团马上就湿。这两个结果不一样，就是因为空气有没有地方可待。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "空气有质量，也会流动", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">空气除了会占地方，还有两个很有用的本领：它<strong>有质量</strong>，也<strong>会流动</strong>。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>空气有质量：</strong>两个一样的气球挂在简易天平两边，天平是平的。只给一个打足气，那一边就沉下去了。</div></div>
          <div class="step"><span class="n">2</span><div><strong>空气会流动：</strong>空气跑起来，就成了风。扇扇子、吹泡泡、放风筝，都是空气在流动。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>空气是混合物，也是生命必需的物质：</strong>空气里不止一种东西，我们每时每刻都要呼吸它。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="气球天平对比图：只给一边打气，天平向充气的一边倾斜">
          <figcaption>左边两个气球一样大，天平平平的；右边只给一个气球打足了气，多的那部分空气也有质量，天平就朝它那边低下去</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">很多同学误认为空气没有质量，因为气球很轻、看不见。其实气球本来就轻，多打进去的空气更轻，但天平还是能感觉出来。所以空气不是没有质量，只是质量很小。</p>
        </div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手做：给气球打气，天平会怎样？", TTS["lab-2"], '''
        <p style="color:var(--muted);margin:0 0 12px">只给右边的气球打气，一边打一边看天平。想一想，气球重了吗？</p>
        <div class="lab-panel">
          <div class="lab-stage" id="air2-stage" style="height:250px;background:linear-gradient(180deg,#fffdf8 0%,#f7f2e6 100%)">
            <div style="position:absolute;left:50%;bottom:12%;width:14px;height:92px;background:#cbb894;border-radius:6px;transform:translateX(-50%)"></div>
            <div id="balance-beam" style="position:absolute;left:50%;bottom:calc(12% + 92px);width:280px;height:8px;background:#b9a27c;border-radius:999px;transform:translateX(-50%) rotate(0deg);transform-origin:50% 50%;transition:transform .7s cubic-bezier(.34,1.2,.5,1)">
              <div id="bal-left" style="position:absolute;left:10px;top:-54px;width:46px;height:54px;border-radius:50%;background:rgba(255,255,255,.6);border:2px solid #b9a27c;display:grid;place-items:center;font-size:11px;color:#5c5142">气球</div>
              <div id="bal-right" style="position:absolute;right:10px;top:-54px;width:46px;height:54px;border-radius:50%;background:rgba(255,255,255,.6);border:2px solid #b9a27c;display:grid;place-items:center;font-size:11px;color:#5c5142">气球</div>
            </div>
          </div>
          <div class="flex-row" style="margin-top:12px">
            <button class="choice" id="air2-pump-once" style="text-align:center;flex:1">给右边气球打 10 下气</button>
            <button class="choice" id="air2-reset" style="text-align:center;flex:1">重新开始</button>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">一共打了</span><span class="v green" id="air2-pump">0 下</span></div>
            <div class="readout-cell"><span class="k">天平倾斜</span><span class="v" id="air2-tilt">0°</span></div>
          </div>
          <p class="result warn" id="air2-out" style="margin-top:12px">两个气球一样大，天平是平的。现在点一下按钮，只给右边那个气球打气。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">⚖️</span><div><strong>想清楚一句话：</strong>气球皮没有变，多出来的重量只可能是空气。空气也有质量，只是它太轻了，平时我们感觉不到。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：竖直倒扣的杯子，纸团会湿吗", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>把一团纸塞在杯子底部，杯口朝下，竖直按进水底，再竖直拿出来。纸团会湿吗？请说出理由。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看清条件：</strong>杯子是竖直按下去，又竖直拿出来的，杯口一直没有歪。</div></div>
          <div class="step"><span class="n">2</span><div><strong>找原因：</strong>杯子里装满了空气，空气占了杯子里全部的地方，水没有位置可进。</div></div>
          <div class="step"><span class="n">3</span><div><strong>得出结论：</strong>纸团<strong>不会湿</strong>，因为水根本没有进到杯子里。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>再想一步：</strong>如果中途把杯子歪一歪，空气会从杯口跑出去，空出来的地方立刻被水填满，这时纸团就湿了。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错法</span>
          <p style="margin:6px 0 0">直接说杯子进水了、纸一定湿，是最典型的错误。这里要区分两件事：<strong>杯子到了水里</strong>，不等于<strong>水进了杯子里</strong>。只要空气还在，水就进不去。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：这三个说法错在哪里", TTS["conceptest-1"], [
        {"q": "下面哪句话是对的？",
         "options": [("空气会占地方", True), ("看不见的东西就没有质量", False), ("空气只在天上，教室里没有", False)],
         "explain": "空气占地方，也有质量，教室里到处都是空气。<strong>错因提醒：</strong>把看不见和不存在搞混，是这一课最典型的常见错误。"},
        {"q": "打完气的气球比没打气的时候重一点，这说明：",
         "options": [("空气有质量", True), ("气球皮变重了", False), ("空气变成水了", False)],
         "explain": "气球皮没有变，多出来的是打进去的空气。<strong>错因提醒：</strong>很多同学误认为空气轻得没有质量，所以天平不会动。实际上天平能感觉出这一点点差别。"},
        {"q": "把杯口歪着按进水里，纸团湿了。最合理的解释是：",
         "options": [("空气从杯口跑出去，水填了进来", True), ("歪着按水就一定会进去", False), ("纸团自己吸水变湿了", False)],
         "explain": "杯子一歪，空气有了出口就跑了，空出来的地方被水填满。<strong>错因提醒：</strong>不要误认为纸湿是纸自己的问题，真正变的是杯子里还有没有空气。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：当一次空气侦探", TTS["synthesis"], '''
        <p style="color:var(--muted);margin:0 0 12px">点开三张卡片，用「空气占据空间」把每一件事说清楚。然后写一写你自己想到的例子。</p>
        <div class="lab-panel">
          <div class="sort-bank" id="det-stage">
            <button class="choice" data-det="ball">🏀 打足了气的篮球</button>
            <button class="choice" data-det="pillow">🛏️ 软软的空气枕</button>
            <button class="choice" data-det="glass">🥛 倒扣进水里的空杯子</button>
          </div>
          <p class="result warn" id="det-out" style="margin-top:12px">点上面任意一张卡片，看看空气在这里帮了什么忙。</p>
        </div>
        <div class="inner-card">
          <p><strong>轮到你了：</strong>在你家里或者教室里，找一个用得到空气的地方，写下来。</p>
          <textarea id="syn-answer" rows="3" placeholder="我发现……，因为空气……" style="margin-top:8px"></textarea>
        </div>
        <div class="kid-note"><span class="emoji">🗣️</span><div>写完之后讲给同桌听，请他帮你看一看：你有没有说清楚「空气占了哪里的地方」。</div></div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换个情境，规律还在不在", TTS["posttest"], [
        {"q": "足球打足了气就变得很硬，踢起来弹得远。这是因为：",
         "options": [("空气占满了球里的地方，把球撑得紧紧的", True), ("球皮变厚了", False), ("球里装的是水", False)],
         "explain": "打气把空气挤进足球里，空气占了里面的空间，球就撑紧了。看不见的力，来自看不见的空气。"},
        {"q": "风车的叶片转起来了，是谁在推它？",
         "options": [("流动的空气", True), ("太阳光", False), ("叶片自己在转", False)],
         "explain": "风就是流动的空气。空气跑动的时候会推着东西走，风车叶片就是这样被推着转起来的。"},
        {"q": "把塑料袋的口张开，在空中兜一圈再扎紧，塑料袋就鼓起来了。里面装的是：",
         "options": [("空气", True), ("水蒸气变成的水", False), ("什么都没有", False)],
         "explain": "兜一圈的时候，空气跑进了袋子，再把口扎紧，空气就跑不掉了。这说明空气看得见「形状」，也占地方。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：四句话记住空气", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>看得见吗</strong>：空气看不见、摸不着，但它就在我们身边。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>占地方吗</strong>：占。杯子里的空气把水挡住了，纸团才不会湿。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>有质量吗</strong>：有。给气球打气，天平会朝那一边低下去。它还会流动，风就是流动的空气。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>有什么用</strong>：空气是混合物，更是我们呼吸必需的东西。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那个谜语：</strong>看不见、摸不着，吹气球靠它，风吹树叶也靠它，一分钟都离不开——答案就是<strong>空气</strong>。今天我们还发现，它不只是「在」，它还会占地方、有质量、会流动。</p>
        </div>
        <div class="inner-card">
          <p><strong>打个比方记住它：</strong>空气就像一群挤在教室里的小朋友。人进了教室，别的班就进不来；人往外走，位置就空出来。空气也是这样，谁占了地方，别人就进不去。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "说出空气的三个特点，说给爸爸妈妈听。",
            "用一句话解释：为什么倒扣进水里的杯子，纸团不会湿？",
        ],
        [
            "在家做一次纸团实验：把纸团塞进杯子底部，竖直按进水盆里，再竖直拿出来，看看纸团有没有湿，把结果记下来。",
            "找一个家里的东西（比如篮球、气垫、气球），说清楚空气在里面帮了什么忙。",
        ],
        [
            "自己设计一个小实验，证明空气真的占了地方。把步骤画下来，讲给同学听。",
            "观察家里一个用得到空气的地方，想一想：如果那里没有空气，会发生什么事？",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "sci-e-air-properties",
    "node_id": "sci-e-air-properties",
    "title": "空气：看不见，但它占地方",
    "name_en": "Air: Invisible but It Takes Up Space",
    "grade": 3,
    "grade_cn": "三年级",
    "domain": "matter-science",
    "domain_cn": "物质科学 · 物质的结构与性质",
    "lesson_type": "experiment-inquiry",
    "version": "1.0.0",
    "description": "用杯子倒扣入水、针筒压缩空气、气球天平三个可操作实验，让三年级学生亲眼看到看不见的空气会占据空间、有质量、会流动，并知道空气是混合物、是生命必需的物质。",
    "tags": ["空气", "占据空间", "空气有质量", "空气流动", "纸团实验"],
    "standard_ref": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念1「物质的结构与性质」学习内容1.2 空气与水是重要的物质——3～4年级能说出空气的特征，知道空气占据空间、有质量、会流动，知道空气是生命必需的物质。",
    "hero_question": "一个空杯子、一个气球、一阵风——看不见的空气到底在哪里？",
    "hero_alt": "空气知识结构图：空气占据空间、有质量、会流动三栏",
    "hero_caption": "空气的三个本领：占据空间 · 有质量 · 会流动；空气是混合物，也是生命必需的物质",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的实验都会围着它转。",
    "anchor_choices": [
        {"t": "空气到底在哪里？", "d": "看不见，怎么知道它真的在", "v": "空气到底在哪里"},
        {"t": "杯子里那张纸为什么不会湿？", "d": "想让纸团实验一次成功", "v": "杯子里那张纸为什么不会湿"},
        {"t": "空气有重量吗？", "d": "想知道气球里装了什么", "v": "空气有重量吗"},
        {"t": "风是怎么来的？", "d": "想知道风到底是什么", "v": "风是怎么来的"},
    ],
    "objectives": [
        "能说出空气看不见、摸不着，但确实在我们身边",
        "能说出空气会占据空间，并解释杯子倒扣入水纸团不湿的原因",
        "能说出空气有质量、会流动，并各举一个生活中的例子",
        "能说出空气是混合物，是我们呼吸必需的物质",
    ],
    "objectives_plain": [
        "能说出空气看不见、摸不着，但确实在我们身边",
        "能说出空气会占据空间，并解释杯子倒扣入水纸团不湿的原因",
        "能说出空气有质量、会流动，并各举一个生活中的例子",
        "能说出空气是混合物，是我们呼吸必需的物质",
    ],
    "standards": [
        {"content": "能说出空气的特征，知道空气占据空间、有质量、会流动",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念1 物质的结构与性质 学习内容1.2 空气与水是重要的物质（3～4年级）"},
        {"content": "知道空气是混合物，空气中的氧气是生命必需的物质",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念1 物质的结构与性质 学习内容1.2 空气与水是重要的物质（3～4年级）"},
    ],
    "prereqs": ["sci-e-object-properties"],
    "prereqs_name": "物体的特征",
    "prereqs_meta": "sci-e-object-properties",
    "leads_to": ["sci-e-materials-in-life"],
    "next_meta": "sci-e-materials-in-life",
    "section_images": ["assets/sci-e-air-properties-fig1.webp", "assets/sci-e-air-properties-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "看不见、摸不着，可它就在我们身边——这节课去找空气。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能自己说出空气在哪里、它会做什么。",
        "objectives": "看清四件事：空气在身边、会占地方、有质量会流动、是呼吸必需的物质。",
        "pretest": "凭感觉选就行，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "空气不是空的，它实实在在占着位置。谁占了地方，别人就进不去。",
        "lab-1": "先做杯子，杯口要一直竖直；再做针筒，推一推看看空气会不会被压小。",
        "module-2": "气球皮没有变，多出来的重量就是空气。风就是流动的空气。",
        "lab-2": "只给右边打气，一边打一边看天平往哪边倒。",
        "worked-example": "四步走：看清条件、找原因、得结论、再想一步。",
        "conceptest-1": "这三句话都是最容易弄错的说法，看清每一个错在哪里。",
        "synthesis": "点开三张卡片，用「空气占了哪里的地方」把每件事说清楚。",
        "posttest": "换了足球、风车和塑料袋，看看你还能不能说出道理。",
        "summary": "回到开头那个谜语：为什么说答案一定是空气？用四句话说清楚。",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是「物质的结构与性质」在小学低段长期空缺的一课：知识树原有物体特征的观察，但没有任何一课处理课标明确要求的空气特征。三年级学生抽象思维弱，所以全课不出现任何术语与公式，只做三件看得见的实验——纸团杯子、针筒压缩、气球天平，让「看不见的空气」变成「看得见的结果」。每个实验都配一句孩子能带走的话：空气占地方、空气有质量、空气会流动。",
    "plan_table": """| 1 | cover | 空气：看不见，但它占地方 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：空气藏在哪里？ | 起·前测（暴露直觉） |
| 5 | concept | 空气会占地方，杯子里的空气把水挡住了 | 承·概念一 |
| 6 | interactive | 动手做：纸团为什么没有湿？ | 承·实验室一（杯子 + 针筒） |
| 7 | concept | 空气有质量，也会流动 | 承·概念二（含常见错误） |
| 8 | interactive | 动手做：给气球打气，天平会怎样？ | 承·实验室二（气球天平） |
| 9 | concept | 例题示范：竖直倒扣的杯子，纸团会湿吗 | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：这三个说法错在哪里 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：当一次空气侦探 | 合·迁移应用 |
| 12 | quiz | 后测：换个情境，规律还在不在 | 合·后测 |
| 13 | summary | 小结：四句话记住空气 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：空气占据空间 / 有质量 / 会流动 三栏标注\n- P5 纸团杯子实验图（已生成）：竖直倒扣纸团不湿 vs 倾斜杯口纸团变湿\n- P7 气球天平对比图（已生成）：只给一边打气，天平向该侧倾斜\n- 若需补充：针筒压缩空气的实拍照片、风车与树叶的实景图",
}
