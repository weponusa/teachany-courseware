# -*- coding: utf-8 -*-
"""小学科学 · 地球的内部：往地心挖下去会看到什么（G5）—— 补齐课标「地球系统·10.4 地球内部圈层和地壳运动」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/sci-e-earth-interior-fig1.webp'
F2 = './assets/sci-e-earth-interior-fig2.webp'

TTS = {
    "hero": "先一起做个思想实验。如果给你一台超级钻机，一直往下挖，穿过泥土、穿过岩石，一直挖到地球的中心，你会看到什么？会不会挖到一个藏在地下的巨大空洞？地球里面到底是空的、是水、还是别的什么东西？这节课我们就当一次地心探险家，从地面一直走到六千多千米深的地方，看看一路上会经过哪些圈层。",
    "problem-anchor": "在开始之前，先选出你最想弄明白的那个问题。是想知道地球里面分成了哪几层，还是想知道越往下走会越热还是越冷，又或者你想弄清楚火山和地震到底是从哪里来的。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出地球内部由地壳、地幔、地核三个圈层组成，并说出它们大致的顺序。第二，能说出越往地球深处温度越高、压力越大。第三，能说出地壳不是一整块，而是分成若干板块。第四，能举例说明板块的挤压、张裂和错动会造成山脉、火山和地震。",
    "pretest": "先做三道小题，凭你现在的想法选就行，选错了也没关系，正好能看出哪里需要重点听。选完会立刻出现解释。",
    "module-1": "我们先把地球切开看一看。从外往里数，地球内部分成三个大圈层。最外面薄薄的一层叫做地壳，就是我们脚下的岩石层。地壳往下到大约两千九百千米深处，是地幔，这是最厚的一层，上部的岩石又热又软，可以非常缓慢地流动。再往下一直到底，是地核，它是地球的最中心。科学家又按状态把地核分成两部分：外面那一圈是液态的外核，最里面是固态的内核。往深处走，温度越来越高，从地表的大约二十摄氏度，一路升到地心附近的五千多摄氏度，比炼钢炉还要热得多；压力也越来越大，越深的地方，上面的岩石压得越紧，到了地心，压力大到我们很难想象。",
    "lab-1": "光听数字不够直观，我们来当一次地心探险家。下面这个滑块可以让你从地面一直往下走到六千三百七十一千米深的地心。拖动滑块，右边会实时告诉你现在到了哪个圈层，那里的温度有多高，压力有多大。你可以慢慢拖，也可以直接拖到最底下，看看地心到底是什么样的地方。",
    "module-2": "知道了地球内部的样子，我们再来解决另一个问题：火山和地震是从哪里来的？原来，地壳并不是完整的一整块，它像一件摔碎又拼起来的巨大拼图，分成好多块，这些大块叫做板块。板块不是固定不动的，它们趴在又热又软的软流层上，非常缓慢地移动，一年只移动几厘米，和我们手指甲生长的速度差不多。板块挨在一起的地方最不安分：两块互相挤压，岩层被挤得弯起来、拱起来，就形成了高大的山脉；两块互相张裂，地壳被拉开一道口子，下面的岩浆顺着裂缝涌上来，就形成了火山；两块水平错动，岩层被卡住又突然滑开，就会发生地震。所以我们看到的火山、地震和山脉，大多集中在板块交界的地方。",
    "lab-2": "现在请你亲手演示一次板块运动。下面有两个板块，你可以让它们挤压、张裂或者错动，看看地面上会跟着发生什么变化。每点一种运动，都读一读下面的解释，想一想这种运动形成了什么地形、又带来了什么自然现象。",
    "worked-example": "我们一起来分析一道题。有一座小岛，岛上经常发生地震，山上还不断有岩浆冒出来。请判断这里的地壳可能在发生什么运动，并说明理由。第一步，看清条件：有两个关键线索，一是经常地震，二是有岩浆喷出。第二步，找出线索背后的意思：地震说明这里的板块在活动；岩浆来自地幔上部，能冒到地面，说明地壳下面有一条通道。第三步，做出判断：地壳被拉开了一道口子、岩浆才能顺着裂缝涌上来，所以这里最可能是板块张裂。第四步，把道理说完整：张裂时地壳变薄、破裂，形成火山，同时伴随地震；如果是挤压，岩层会拱起来形成山脉；如果是错动，最突出的表现是地震，不一定有火山。",
    "conceptest-1": "现在用三个容易弄错的说法考考你。请仔细读每一个选项，选出你认为正确的那个，然后看解释。",
    "synthesis": "学到这里，请你当一次科学讲解员。学校科技节要做一张地球内部圈层海报，需要你写一份讲解稿：从地表出发，一路讲到地心，每到一个圈层就说出它的名字、大约到多深、温度大概多少，以及那里是什么状态。请写三到五句话，让别人看完海报就能记住这条路线。",
    "posttest": "最后用新的情境检验一下。这次的问题里出现了温泉、深井和海底山脉，看看你能不能把圈层和板块运动用上去。",
    "summary": "这节课我们弄明白了三件事。第一，地球内部从外到里分成地壳、地幔、地核三个圈层，越往深处温度越高、压力越大。第二，地壳不是一整块，而是分成若干板块，它们趴在又热又软的软流层上缓慢移动。第三，板块挤压会形成山脉，张裂会形成火山，错动会引发地震，这些现象大多出现在板块交界的地方。回到开头的问题，往地心挖下去，你不会挖到一个空洞，而是会穿过一层层越来越热、越来越密的岩石和金属。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：按从外到里的顺序写出地球的三个圈层，并各写一句它的特点。第二层能力应用，动手做：用橡皮泥、彩泥或者切开的熟鸡蛋做一个地球内部圈层模型，标出三个圈层的名字。第三层迁移挑战，选做：查一查我国哪一带有火山、哪一带地震比较多，把它们画在一张简图上，并说说和板块交界有什么关系。",
    "knowledge-graph": "这张图展示了这节课在科学知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 地球的三个圈层", "lab-1": "实验室一 地球剖面探针", "module-2": "概念二 板块在慢慢移动",
    "lab-2": "实验室二 板块运动演示", "worked-example": "例题讲解 判断板块运动方向", "conceptest-1": "概念测试",
    "synthesis": "综合任务 圈层讲解稿", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

CUSTOM_JS = r"""
/* ============================================================
   sci-e-earth-interior 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 地球剖面探针：深度滑块 0→6371 km → 圈层 / 温度 / 压力
   3) 板块运动演示：挤压 / 张裂 / 错动
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

  /* ---------- 2. 地球剖面探针 ---------- */
  var DEPTHS = [0, 35, 100, 400, 670, 2900, 5100, 6371];
  var TEMPS  = [20, 600, 1300, 1600, 1900, 3000, 5000, 5500];
  var PRESS  = [0, 1, 3, 13, 23, 136, 329, 364];

  function interp(xs, ys, v) {
    if (v <= xs[0]) return ys[0];
    for (var i = 1; i < xs.length; i++) {
      if (v <= xs[i]) {
        var t = (v - xs[i - 1]) / (xs[i] - xs[i - 1]);
        return ys[i - 1] + t * (ys[i] - ys[i - 1]);
      }
    }
    return ys[ys.length - 1];
  }

  function layerOf(d) {
    if (d < 35) return { n: '地壳', sub: '我们脚下的岩石层', c: '#c9a46a' };
    if (d < 2900) return { n: '地幔', sub: '最厚的一层，上部又热又软，能缓慢流动', c: '#e07a3f' };
    if (d < 5100) return { n: '地核 · 外核', sub: '温度很高，这里的金属是液态的', c: '#e84c3d' };
    return { n: '地核 · 内核', sub: '压力最大，温度最高，金属被压成固态', c: '#b02a24' };
  }

  var probeStage = document.getElementById('probe-stage');
  if (probeStage) {
    var slider = document.getElementById('probe-range');
    var probe = document.getElementById('probe-dot');
    var outLayer = document.getElementById('probe-layer');
    var outDepth = document.getElementById('probe-depth');
    var outTemp = document.getElementById('probe-temp');
    var outPress = document.getElementById('probe-press');
    var outDesc = document.getElementById('probe-desc');
    var SHELL_PX = 14, REST_PX = 306;

    function renderProbe() {
      var d = parseFloat(slider.value);
      var y = (d <= 35) ? (d / 35) * SHELL_PX : SHELL_PX + ((d - 35) / 6336) * REST_PX;
      probe.style.top = Math.max(0, Math.min(318, y)) + 'px';
      var L = layerOf(d);
      probe.style.background = L.c;
      outLayer.textContent = L.n;
      outDepth.textContent = (d >= 6371 ? 6371 : Math.round(d)) + ' 千米';
      outTemp.textContent = '约 ' + Math.round(interp(DEPTHS, TEMPS, d) / 10) * 10 + ' ℃';
      var p = interp(DEPTHS, PRESS, d);
      outPress.textContent = p < 0.5 ? '接近 0' : '约 ' + Math.round(p) + ' 万个大气压';
      outDesc.innerHTML = '<strong>' + L.n + '</strong>：' + L.sub + '。';
      document.querySelectorAll('[data-jump]').forEach(function (b) {
        b.classList.toggle('selected', Math.abs(parseFloat(b.dataset.jump) - d) < 1);
      });
    }
    slider.addEventListener('input', renderProbe);
    document.querySelectorAll('[data-jump]').forEach(function (b) {
      b.addEventListener('click', function () { slider.value = b.dataset.jump; renderProbe(); });
    });
    renderProbe();
  }

  /* ---------- 3. 板块运动演示 ---------- */
  var plateStage = document.getElementById('plate-stage');
  if (plateStage) {
    var pl = document.getElementById('plate-left');
    var pr = document.getElementById('plate-right');
    var mid = document.getElementById('plate-mid');
    var mt = document.getElementById('plate-mountain');
    var vc = document.getElementById('plate-volcano');
    var out = document.getElementById('plate-out');

    var MODES = {
      push: {
        name: '挤压',
        left: 'translateX(26px)', right: 'translateX(-26px)',
        midW: '0%', midTop: '0px',
        mountain: 'translateY(-30px)', volc: 'translateY(0) scale(.5)',
        cls: 'result',
        msg: '<strong>两块板块互相挤压 → 岩层拱起来，形成高大山脉，同时也会有地震。</strong><br>' +
             '岩层被挤得弯起来、一层层叠上去，越挤越高。我国的喜马拉雅山脉就是这样隆起来的，它至今还在长高。'
      },
      split: {
        name: '张裂',
        left: 'translateX(-26px)', right: 'translateX(26px)',
        midW: '26%', midTop: '0px',
        mountain: 'translateY(0) scale(.5)', volc: 'translateY(-26px) scale(1)',
        cls: 'result',
        msg: '<strong>两块板块互相分开 → 地壳被拉开一道口子，岩浆上涌，形成火山。</strong><br>' +
             '裂缝处地壳变薄、破裂，地幔上部的岩浆顺着裂缝冒出来。东非大裂谷正在这样被拉开，海底也常常这样长出新的地壳。'
      },
      slip: {
        name: '错动',
        left: 'translateX(20px) translateY(-16px)', right: 'translateX(-20px) translateY(16px)',
        midW: '4%', midTop: '0px',
        mountain: 'translateY(0) scale(.5)', volc: 'translateY(0) scale(.5)',
        cls: 'result error',
        msg: '<strong>两块板块水平错动 → 岩层被卡住，然后突然滑开，发生地震。</strong><br>' +
             '错动时岩层先被卡住、越卡越紧，能量一点点攒起来；一旦撑不住突然滑动，能量一下子放出来，地面就剧烈震动。'
      }
    };

    function renderPlate(key) {
      var m = MODES[key];
      pl.style.transform = m.left;
      pr.style.transform = m.right;
      mid.style.width = m.midW;
      mt.style.transform = m.mountain;
      vc.style.transform = m.volc;
      out.className = m.cls;
      out.innerHTML = m.msg;
      document.querySelectorAll('[data-plate]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.plate === key);
      });
    }
    document.querySelectorAll('[data-plate]').forEach(function (b) {
      b.addEventListener('click', function () { renderPlate(b.dataset.plate); });
    });
    renderPlate('push');
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：地球里面是什么样子？", TTS["pretest"], [
        {"q": "如果一直往地下挖，穿过泥土和岩石，最后会挖到什么？",
         "options": [("会一路遇到越来越热、越来越密的岩石和金属，直到地心", True),
                     ("会挖到一个巨大的空洞", False),
                     ("会挖到一片地下海", False)],
         "explain": "地球内部是实心的，分成三个圈层，越往深处温度越高、压力越大。<strong>错因提醒：</strong>科幻片里的地下空洞是想象，真实的地球内部被岩石和金属填得满满的。"},
        {"q": "从地面往下走，温度会怎么变化？",
         "options": [("越来越高，地心附近有五千多摄氏度", True),
                     ("先升高，到了地幔又开始变冷", False),
                     ("一直保持不变", False)],
         "explain": "越往深处越热，地心附近的温度比炼钢炉还高得多。<strong>错因提醒：</strong>不要误认为地下深处是阴冷的，正好相反，那里又热又挤。"},
        {"q": "火山喷发和地震为什么常常出现在同一片地方？",
         "options": [("因为那里往往是板块交界处，地壳活动最剧烈", True),
                     ("因为它们约好了一起发生", False),
                     ("因为那里的天气不好", False)],
         "explain": "火山和地震大多集中在板块交界处。这个问题先记在心里，等下我们要亲手演示板块运动。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "地球里面分三层：地壳、地幔、地核", TTS["module-1"], f'''
        <p style="font-size:17px;margin:0 0 12px">把地球切开，从外往里数，一共三个大圈层：<strong>地壳、地幔、地核</strong>。越往深处走，温度越高，压力越大。</p>
        <div class="grid grid-3">
          <div class="inner-card">
            <p><strong>地壳</strong></p>
            <p style="color:var(--muted)">最外面薄薄的一层岩石，我们就站在它上面。</p>
          </div>
          <div class="inner-card">
            <p><strong>地幔</strong></p>
            <p style="color:var(--muted)">最厚的一层，上部又热又软，能非常缓慢地流动。</p>
          </div>
          <div class="inner-card">
            <p><strong>地核</strong></p>
            <p style="color:var(--muted)">最中心，温度最高、压力最大，外面是液态，里面是固态。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="地球内部圈层剖面示意图，标注地壳、地幔、外核、内核与深度">
          <figcaption>地球内部从外到里：地壳（约 0～35 千米）、地幔（约 35～2900 千米）、地核（约 2900～6371 千米）</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🥚</span><div><strong>打个比方：</strong>把一个熟鸡蛋切开，蛋壳很像地壳，蛋白很像地幔，蛋黄很像地核。当然，真实的地球比鸡蛋热得多、也挤得多。</div></div>
        <div class="kid-note"><span class="emoji">🤔</span><div><strong>为什么要学地球的内部？</strong>因为火山喷发、地震和温泉，都来自地下这几个圈层之间的相互作用。看不清里面，就说不清外面的现象。</div></div>
{insight_box([
    {"lens": "看见它", "text": "地壳很薄，最厚的地方也只有几十千米；地幔厚达两千多千米，占了地球体积的绝大部分。"},
    {"lens": "解释它", "text": "为什么越深越热？因为地球内部藏着大量热量，外面的岩石又像一层厚棉被，把热量捂在里面散不出去。"},
    {"lens": "迁移它", "text": "我们虽然挖不到地心，却能靠地震波给地球做「透视」——地震波穿过不同圈层时速度会变化，科学家就是这样知道地球分层的。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "地球剖面探针：一口气走到六千三百七十一千米", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">拖动滑块，让探针从地面一直往下走。右边会实时显示你所在的圈层、温度有多高、压力有多大。</p>
        <div class="lab-panel">
          <div style="display:flex;gap:14px;align-items:flex-start;flex-wrap:wrap">
            <div id="probe-stage" style="position:relative;width:150px;height:320px;flex-shrink:0;border-radius:14px;overflow:hidden;border:1px solid var(--line-subtle);background:linear-gradient(180deg,#f2ead9 0%,#f6d9b8 20%,#f0a874 55%,#e2643f 78%,#a8241c 100%)">
              <div style="position:absolute;left:0;right:0;top:0;height:14px;background:#c9a46a;border-bottom:1px solid rgba(0,0,0,.2)"></div>
              <div style="position:absolute;left:0;right:0;top:14px;height:138px;background:rgba(224,122,63,.55)"></div>
              <div style="position:absolute;left:0;right:0;top:152px;height:106px;background:rgba(232,76,61,.55)"></div>
              <div style="position:absolute;left:0;right:0;top:258px;bottom:0;background:rgba(176,42,36,.65)"></div>
              <span style="position:absolute;left:6px;top:0px;font-size:11px;color:#5c5142;font-weight:700">地壳</span>
              <span style="position:absolute;left:6px;top:20px;font-size:11px;color:#4a2a10;font-weight:700">地幔</span>
              <span style="position:absolute;left:6px;top:158px;font-size:11px;color:#fff;font-weight:700">外核</span>
              <span style="position:absolute;left:6px;top:264px;font-size:11px;color:#fff;font-weight:700">内核</span>
              <div id="probe-dot" style="position:absolute;left:50%;margin-left:-7px;width:14px;height:14px;border-radius:50%;background:#c9a46a;border:2px solid #fff;box-shadow:0 0 8px rgba(0,0,0,.35);transition:top .15s linear"></div>
              <span style="position:absolute;right:5px;bottom:4px;font-size:10px;color:rgba(255,255,255,.85)">示意剖面 · 地壳已放大</span>
            </div>
            <div style="flex:1;min-width:220px">
              <div class="lab-readout" style="margin-top:0">
                <div class="readout-cell"><span class="k">深度</span><span class="v" id="probe-depth">0 千米</span></div>
                <div class="readout-cell"><span class="k">所在圈层</span><span class="v green" id="probe-layer">地壳</span></div>
              </div>
              <div class="lab-readout">
                <div class="readout-cell"><span class="k">温度</span><span class="v" id="probe-temp">约 20 ℃</span></div>
                <div class="readout-cell"><span class="k">压力</span><span class="v" id="probe-press">接近 0</span></div>
              </div>
              <div class="slider-row" style="display:block">
                <label for="probe-range" style="display:block;margin-bottom:4px">往下挖的深度：0 → 6371 千米</label>
                <input type="range" id="probe-range" min="0" max="6371" step="1" value="0" style="width:100%">
              </div>
              <div class="flex-row" style="margin-top:8px">
                <button class="choice selected" data-jump="0" style="text-align:center;font-size:13px">地面 0</button>
                <button class="choice" data-jump="35" style="text-align:center;font-size:13px">地壳底 35</button>
                <button class="choice" data-jump="2900" style="text-align:center;font-size:13px">地幔底 2900</button>
                <button class="choice" data-jump="6371" style="text-align:center;font-size:13px">地心 6371</button>
              </div>
              <p class="result warn" id="probe-desc" style="margin-top:10px"></p>
            </div>
          </div>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🌡️</span><div><strong>发现了吗：</strong>深度从 0 变到 6371 千米，温度从二十摄氏度涨到五千多摄氏度，压力从接近 0 涨到三十多万个大气压。可是地壳只占了最上面极薄的一点——所以图中把地壳放大了，不然根本看不见。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "地壳是拼起来的，板块一动就有了山、火山和地震", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">地壳不是完整的一整块，而是分成好多大块，叫做<strong>板块</strong>。它们趴在又热又软的软流层上，每年只移动几厘米。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>挤压：</strong>两块板块互相撞过来，岩层被拱起，形成高大山脉，同时伴随地震。</div></div>
          <div class="step"><span class="n">2</span><div><strong>张裂：</strong>两块板块互相分开，地壳裂开口子，岩浆上涌，形成火山。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>错动：</strong>两块板块水平错开，岩层卡住后突然滑动，能量一下子放出来，发生地震。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="板块运动的三种方式示意图，标注挤压、张裂、错动及其形成的地形">
          <figcaption>挤压隆起山脉，张裂生成火山，错动引发地震——三种运动都发生在板块交界的地方</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">误认为一地震就是板块在挤压。其实三种运动都可能引发地震，判断方向还要看有没有山脉隆起、有没有火山喷发。记住这句口诀：<strong>挤压成山，张裂生火，错动地震</strong>。</p>
        </div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "板块运动演示：看看地面会跟着发生什么", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">点下面的三个按钮，让两块板块做出不同的运动，观察地面上出现了什么。</p>
        <div class="lab-panel">
          <div class="lab-stage" id="plate-stage" style="height:200px;background:linear-gradient(180deg,#eef6ff 0%,#dceaf7 55%,#c9a46a 56%,#b3904f 100%)">
            <div id="plate-left" style="position:absolute;bottom:0;left:6%;width:36%;height:56px;background:#8d6a3f;border-radius:6px 6px 0 0;transition:transform .8s cubic-bezier(.34,1.2,.5,1)"></div>
            <div id="plate-right" style="position:absolute;bottom:0;right:6%;width:36%;height:56px;background:#8d6a3f;border-radius:6px 6px 0 0;transition:transform .8s cubic-bezier(.34,1.2,.5,1)"></div>
            <div id="plate-mid" style="position:absolute;left:44%;bottom:56px;width:0%;height:60px;background:#e84c3d;opacity:.75;border-radius:6px 6px 0 0;transition:all .8s ease"></div>
            <div id="plate-mountain" style="position:absolute;left:50%;margin-left:-40px;bottom:56px;width:80px;height:56px;background:#7a5c33;clip-path:polygon(50% 0,100% 100%,0 100%);transform:translateY(-30px);transition:transform .8s ease"></div>
            <div id="plate-volcano" style="position:absolute;left:50%;margin-left:-30px;bottom:56px;width:60px;height:52px;background:#a03a2a;clip-path:polygon(50% 12%,100% 100%,0 100%);transform:translateY(0) scale(.5);transition:transform .8s ease"></div>
          </div>
          <div class="flex-row" style="margin-top:12px">
            <button class="choice selected" data-plate="push" style="text-align:center">➡️⬅️ 挤压</button>
            <button class="choice" data-plate="split" style="text-align:center">⬅️➡️ 张裂</button>
            <button class="choice" data-plate="slip" style="text-align:center">↕️ 错动</button>
          </div>
          <p class="result" id="plate-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🗺️</span><div><strong>连起来想：</strong>为什么火山和地震常常出现在同一片区域？因为它们都和板块交界有关。打开地图软件搜一搜，你会发现火山和地震带大多连成一条条线。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：这座小岛上的地壳在怎么运动", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>有一座小岛，岛上经常发生地震，山上还不断有岩浆冒出来。请判断这里的地壳可能在发生什么运动，并说明理由。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看清条件：</strong>题目给了两个线索——经常地震，有岩浆喷出。</div></div>
          <div class="step"><span class="n">2</span><div><strong>读出线索的意思：</strong>地震说明板块在活动；岩浆来自地幔上部，能冒到地面，说明地壳下面有一条通道。</div></div>
          <div class="step"><span class="n">3</span><div><strong>做出判断：</strong>地壳被拉开一道口子，岩浆才能顺着裂缝上来，所以这里最可能是<strong>板块张裂</strong>。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>把道理说完整：</strong>张裂时地壳变薄、破裂，形成火山并伴随地震；挤压会拱起山脉；错动最突出的表现是地震，不一定有火山。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错法</span>
          <p style="margin:6px 0 0">只看到「地震」就答成挤压，是这道题最常见的错误。地震在三种运动里都可能发生，所以必须再看<strong>有没有火山、有没有山脉</strong>，才能判断方向。这正是把现象和原因搞混的典型表现。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "下面哪句话是正确的？",
         "options": [("地球内部从外到里分成地壳、地幔、地核三个圈层", True),
                     ("地球内部是空的，所以才有火山", False),
                     ("地幔在最外面，地壳在最里面", False)],
         "explain": "从外到里的顺序是地壳、地幔、地核。<strong>错因提醒：</strong>把地壳和地幔的里外顺序搞混，是这一课最常见的错误。"},
        {"q": "越往地球深处走，温度和压力会怎样变化？",
         "options": [("温度越来越高，压力也越来越大", True),
                     ("温度越来越高，压力越来越小", False),
                     ("温度和压力都不变", False)],
         "explain": "深处被上面的岩石压着，越深越挤，同时热量也越攒越多。<strong>错因提醒：</strong>容易误认为压力会随深度减小，其实正好相反。"},
        {"q": "喜马拉雅山脉是怎么形成的？",
         "options": [("两块板块互相挤压，岩层被拱起来", True),
                     ("两块板块张裂，岩浆堆起来", False),
                     ("河流把泥沙堆起来", False)],
         "explain": "高大的山脉主要由板块挤压形成，而且它现在还在缓慢长高。<strong>错因提醒：</strong>不要把它和火山堆出来的山搞混——火山是岩浆喷出后堆成的，形状和成因都不一样。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：写一份地球圈层讲解稿", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">科技节的海报上要配一段讲解稿，请带着读者从地面一路走到地心。</p>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>每一站都要写清四件事：</strong>圈层名字 · 大约有多深 · 温度大概多少 · 那里是什么状态。</p>
        </div>
        <div class="inner-card">
          <p><strong>第一步：排出路线顺序</strong></p>
          <p style="color:var(--muted)">先经过哪一层，再经过哪一层，最后到哪一层？把它们写下来。</p>
          <textarea id="syn-route" rows="2" placeholder="地面 → …… → …… → 地心"></textarea>
        </div>
        <div class="inner-card">
          <p><strong>第二步：写成三到五句话的讲解稿</strong></p>
          <textarea id="syn-answer" rows="5" placeholder="从地面出发，我们首先进入……"></textarea>
        </div>
        <div class="kid-note"><span class="emoji">🗣️</span><div>写完后读给同桌听，请他只看你的文字，能不能说出每一层的名字和温度。</div></div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换个情境，规律还在不在", TTS["posttest"], [
        {"q": "有的地方能打出上千米深的深井，井水抽上来就是热的。这个现象说明：",
         "options": [("越往地下深处温度越高", True),
                     ("地下水自己会发热", False),
                     ("深井里的水被泵加热了", False)],
         "explain": "井越深，水接触到的岩层越热，所以抽上来的水温度更高。"},
        {"q": "海底有一条长长的山脉，中间有一道裂口，不断有岩浆涌出来形成新的海底。这里最可能在发生：",
         "options": [("板块张裂", True), ("板块挤压", False), ("板块错动", False)],
         "explain": "有岩浆上涌、有裂口，是张裂的典型表现。<strong>错因提醒：</strong>不要一看到「山」就判断成挤压——海底山脉很多是岩浆堆出来的。"},
        {"q": "两个板块交界处，岩层先被卡住很多年，某一天突然滑动了一下，地面剧烈震动。这是：",
         "options": [("板块错动引发的地震", True), ("板块张裂引发的火山", False), ("板块挤压形成的山脉", False)],
         "explain": "水平错动时岩层先卡住、蓄积能量，突然滑动就释放出能量，形成地震。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把自己讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>三个圈层</strong>：从外到里是地壳、地幔、地核，越深温度越高、压力越大。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>板块在动</strong>：地壳分成若干板块，趴在软流层上，每年只移动几厘米。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>三种结果</strong>：挤压成山，张裂生火，错动地震，大多发生在板块交界处。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头的问题：</strong>往地心挖下去，你不会挖到一个空洞，而是会穿过越来越热、越来越密的岩石和金属——先是薄薄的地壳，再是厚厚的地幔，最后是又烫又挤的地核。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用"地壳、地幔、地核、板块"这四个词，说清火山和地震是从哪里来的。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "按从外到里的顺序写出地球的三个圈层，并给每一层写一句特点。",
            "写出板块挤压、张裂、错动分别会带来什么结果。",
            "判断对错并说明理由：越往地下深处走，温度越低、压力越小。",
        ],
        [
            "用橡皮泥、彩泥或者切开的熟鸡蛋做一个地球内部圈层模型，标出三个圈层的名字，并写一句说明。",
            "打开地图软件，找一找我国的火山和地震多发区，把它们的位置抄下来，说说它们和板块交界有什么关系。",
        ],
        [
            "假设你能坐进一艘地心探险舱，请设计一条从地面到地心的路线：每一站写明深度、温度、能看到的景象，并说明为什么越往后越难前进。",
            "查一查科学家是怎么在不挖开地球的情况下知道地球内部分层的，用三句话讲清他们的办法。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "sci-e-earth-interior",
    "node_id": "sci-e-earth-interior",
    "title": "地球的内部：往地心挖下去会看到什么",
    "name_en": "Inside the Earth: What would we see digging to the core?",
    "grade": 5,
    "grade_cn": "五年级",
    "domain": "earth-space-science",
    "domain_cn": "地球与宇宙科学 · 地球系统",
    "lesson_type": "concept-inquiry",
    "version": "1.0.0",
    "description": "用深度滑块把地球内部三个圈层变成一段可以自己走一遍的旅程，再用板块运动演示说明山脉、火山与地震的成因，理解地球圈层之间的相互作用。",
    "tags": ["地球内部", "地壳", "地幔", "地核", "板块运动", "火山与地震"],
    "standard_ref": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念10「地球系统」学习内容10.4 地球内部圈层和地壳运动——5～6年级知道地球系统不同圈层的相互作用产生了各种自然现象。",
    "hero_question": "如果一直往地下挖，穿过泥土和岩石，最后会挖到什么？",
    "hero_alt": "地球内部圈层知识结构图：地壳、地幔、地核与板块运动",
    "hero_caption": "地壳、地幔、地核三个圈层 · 越深越热越挤 · 地壳分成板块 · 挤压成山、张裂生火、错动地震",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的探究都会围着它转。",
    "anchor_choices": [
        {"t": "地球里面分成哪几层？", "d": "想知道脚下的地球到底是什么结构", "v": "地球里面分成哪几层"},
        {"t": "越往地下走，是更热还是更冷？", "d": "想知道深处的温度和压力", "v": "越往地下走是更热还是更冷"},
        {"t": "火山和地震到底是怎么来的？", "d": "想知道它们为什么总在同一片地方出现", "v": "火山和地震到底是怎么来的"},
        {"t": "我想亲手走一遍去地心的路", "d": "拖动探针，一直走到六千多千米深", "v": "我想亲手走一遍去地心的路"},
    ],
    "objectives": [
        "能说出地球内部由地壳、地幔、地核三个圈层组成，并说出它们从外到里的顺序",
        "能说出越往地球深处走，温度越高、压力越大",
        "能说出地壳不是一整块，而是分成若干板块，它们在缓慢移动",
        "能举例说明板块挤压、张裂、错动分别会造成山脉、火山和地震",
    ],
    "objectives_plain": [
        "能说出地球内部由地壳、地幔、地核三个圈层组成，并说出它们从外到里的顺序",
        "能说出越往地球深处走，温度越高、压力越大",
        "能说出地壳不是一整块，而是分成若干板块，它们在缓慢移动",
        "能举例说明板块挤压、张裂、错动分别会造成山脉、火山和地震",
    ],
    "standards": [
        {"content": "知道地球内部由地壳、地幔、地核等圈层组成，越往深处温度越高、压力越大",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念10 地球系统（5～6年级）"},
        {"content": "知道地球系统不同圈层的相互作用产生了各种自然现象，能举例说明地壳运动与火山、地震的关系",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》学习内容10.4 地球内部圈层和地壳运动（5～6年级）"},
    ],
    "prereqs": ["sci-e-rocks-soil"],
    "prereqs_name": "岩石与土壤",
    "prereqs_meta": "sci-e-rocks-soil",
    "leads_to": ["sci-e-natural-disasters"],
    "next_meta": "sci-e-natural-disasters",
    "section_images": ["assets/sci-e-earth-interior-fig1.webp", "assets/sci-e-earth-interior-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "一直往下挖会挖到什么？带着这个思想实验开始。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能说清火山和地震是从哪里来的。",
        "objectives": "看清四件事：说出三个圈层、说出越深越热越挤、说出板块在动、说出三种运动的结果。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "地壳薄、地幔厚、地核烫，越深越热也越挤。",
        "lab-1": "从 0 拖到 6371，看看温度和压力怎么一路涨上去。",
        "module-2": "地壳是拼起来的，板块每年只移动几厘米，但几千万年就能改变大地。",
        "lab-2": "分别点挤压、张裂、错动，看地面跟着出现山、火山还是地震。",
        "worked-example": "四步走：看清条件、读出线索、做出判断、说清道理。",
        "conceptest-1": "干扰项里藏着最常见的那几个错误想法，选完看清每一个解释。",
        "synthesis": "讲解稿按路线写：每一站写清名字、深度、温度和状态。",
        "posttest": "换了深井、海底山脉和断层的新情境，看看你还能不能判断准确。",
        "summary": "用三个圈层和三种运动，把火山地震的来历讲清楚。",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是「地球系统」在学习内容10.4 上的空缺：知识树原有岩石与土壤、地表变化，但没有一课讲清地球内部结构与板块运动这条因果链。设计上把看不见的地下变成可以走一遍的路线——用深度滑块把三个圈层、温度与压力变成实时读数；再用板块运动演示把「挤压成山、张裂生火、错动地震」变成可以反复点击的对比，最后用熟鸡蛋模型、深井水温和海底山脉等真实情境收束。",
    "plan_table": """| 1 | cover | 地球的内部：往地心挖下去会看到什么 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：地球里面是什么样子？ | 起·前测（暴露直觉） |
| 5 | concept | 地球里面分三层：地壳、地幔、地核 | 承·概念一（圈层结构） |
| 6 | interactive | 地球剖面探针：一口气走到六千三百七十一千米 | 承·实验室一（深度滑块探针） |
| 7 | concept | 地壳是拼起来的，板块一动就有了山、火山和地震 | 承·概念二（板块运动） |
| 8 | interactive | 板块运动演示：看看地面会跟着发生什么 | 承·实验室二（三种运动对比） |
| 9 | concept | 例题示范：这座小岛上的地壳在怎么运动 | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：写一份地球圈层讲解稿 | 合·迁移应用 |
| 12 | quiz | 后测：换个情境，规律还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把自己讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：地壳 / 地幔 / 地核 + 板块运动三栏标注\n- P5 地球内部圈层剖面图（已生成）：中文标注地壳、地幔、外核、内核与深度\n- P7 板块运动示意图（已生成）：挤压成山、张裂生火、错动地震三种对比\n- 若需补充：熟鸡蛋剖面实拍对照照片、全球火山地震带分布图",
}
