# -*- coding: utf-8 -*-
"""小学科学 · 弹力：被压弯的东西想弹回来（G5）—— 补齐课标「物质的运动与相互作用·3.1 力」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/sci-e-elastic-force-fig1.webp'
F2 = './assets/sci-e-elastic-force-fig2.webp'

TTS = {
    "hero": "先看两样东西。一根橡皮筋，你把它拉长了，一松手，它啪地缩回去。一块橡皮泥，你把它拉长了，一松手，它就停在那个长长的形状上，再也回不去了。同样是被你拉，为什么一个回得来，一个回不来？还有，跳跳床为什么能把你弹到半空中？这节课我们就来弄清楚这件事。",
    "problem-anchor": "开始之前，先选一个你最想弄明白的问题。是想知道为什么有的东西能弹回来，还是想知道弹力到底有多大，又或者你想知道弹簧测力计为什么能量出力。选好以后，带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出物体受力会发生变化，撤去力以后能恢复原状的叫弹性形变。第二，能说出弹性形变恢复时产生的力叫弹力。第三，能说出弹力的大小跟形变的程度有关，形变越大，弹力越大。第四，知道弹性有一定的限度，超过限度就回不去了。",
    "pretest": "先做三道小题，用你现在的想法选就行。选完马上会给你解释，选错了正好知道要重点听哪里。",
    "module-1": "我们先看一个现象。用手压一压弹簧，弹簧变短了；一松手，它又变回原来的长度。用手拉一拉橡皮筋，它变长了；一松手，它又缩回去。这一类变化有一个共同点：受了力，形状变了；撤去力，形状又回来了。这就叫弹性形变。再看橡皮泥和面团，用力把它们捏成别的形状，松手以后，它们就停在那个新形状上，再也回不去了，这叫塑性形变。所以判断的标准只有一条：撤去力以后，它还能不能回到原来的样子。",
    "lab-1": "现在请你做一次弹簧实验。每点一次加钩码，就多挂一个；一边挂一边看弹簧伸长了多少。注意看下面三个数：挂了几个钩码、弹簧现在多长、一共伸长了多少。等你挂得太多的时候，会发生一件很特别的事，一定要看一看。",
    "module-2": "从刚才的实验里，你能发现两件事。第一件，钩码挂得越多，弹簧伸得越长，形变越大，弹簧想恢复的力也就越大。这个力就是弹力，弹力的大小跟形变的程度有关。第二件，弹簧不能无限地拉。拉得太多，超过了弹性限度，弹簧就回不到原来的长度了，这叫被拉坏了。所以弹簧测力计上都写着量程，用的时候不能超过它。",
    "lab-2": "接下来做一个对比实验。这里有四个东西：橡皮筋、弹簧、橡皮泥和面团。请你逐个拉一拉，再松手，看看谁回得来、谁回不来，然后把它放进对应的筐里。放之前先问自己一句话：撤去力以后，它还能回到原来的样子吗？",
    "worked-example": "我们一起来分析一道题。把 1 个钩码挂在弹簧下面，弹簧伸长 2 厘米；挂 3 个同样的钩码，弹簧伸长 6 厘米。为什么弹簧测力计可以量出力的大小？第一步，先看清现象，钩码越多，弹簧伸得越长。第二步，找一找关系，钩码数变成原来的 3 倍，伸长量也变成原来的 3 倍，伸长量和力是对应的。第三步，得出方法，只要在弹簧旁边标好刻度，就能用伸长量表示力的大小，这就是弹簧测力计。第四步，特别注意，这种对应关系只在弹性限度以内成立，超过了就会把弹簧拉坏，读数也不再准了，所以测力计都有量程。",
    "conceptest-1": "下面用三个容易弄混的说法考考你。请仔细读每一个选项，选完再看解释。",
    "synthesis": "最后一件事交给你，请你当一次弹力侦探。下面有六种常见的现象，请你判断每一种里面有没有弹力在起作用，然后把它们分别放进两个筐里。放之前，先在心里问一句：这里的物体，撤去力以后能不能恢复原状？",
    "posttest": "最后再用三道题检验一下。这一次有汽车减震、撑杆跳和弹簧测力计，看看你能不能把学到的关系用上去。",
    "summary": "这节课我们抓住了一条主线。物体受力会发生形变；撤去力以后能恢复原状的，叫弹性形变；不能恢复原状的，叫塑性形变。弹性形变在恢复的过程中产生的力，就是弹力。弹力的大小跟形变的程度有关，形变越大，弹力越大。还要记住一句话：弹性有一定的限度，超过限度就回不去了，所以弹簧测力计都有量程。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出一句话，说清楚什么是弹性形变、什么是塑性形变，并各举一个例子。第二层能力应用，动手做：用一根橡皮筋和一个纸杯，做一个能弹起小纸球的小装置，记录下你的做法。第三层迁移挑战，选做：设计一个用弹力的物品，画出草图，写出你打算用哪种材料、为什么它能提供弹力，以及需要注意什么限度。",
    "knowledge-graph": "这张图展示了这节课在科学知识网里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 弹性形变与塑性形变", "lab-1": "实验室一 弹簧挂钩码",
    "module-2": "概念二 弹力大小与弹性限度", "lab-2": "实验室二 弹性与塑性分类",
    "worked-example": "例题讲解 弹簧测力计", "conceptest-1": "概念测试",
    "synthesis": "综合任务 弹力侦探", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

SORT_ITEMS = [
    {"id": "trampoline", "t": "跳跳床把人弹起来", "kind": "yes", "why": "跳跳床的床面被压下以后，撤去力能弹回原状，是弹性形变，恢复时产生了弹力，把人弹了起来。"},
    {"id": "clay", "t": "把橡皮泥捏成新形状", "kind": "no", "why": "橡皮泥被捏过以后停在新的形状上，撤去力回不去，是塑性形变，没有产生弹力。"},
    {"id": "bow", "t": "拉开的弓把箭射出去", "kind": "yes", "why": "弓臂被拉开后发生了弹性形变，松手时恢复原状，产生的弹力把箭推了出去。"},
    {"id": "paper", "t": "把一张纸揉成一团", "kind": "no", "why": "纸被揉皱以后展不平，撤去力回不到原来平整的样子，是塑性形变。"},
    {"id": "sofa", "t": "坐沙发，起来后沙发又鼓回来", "kind": "yes", "why": "海绵被压下去以后能弹回原状，是弹性形变，所以坐上去会有回弹的感觉。"},
    {"id": "can", "t": "把一个空易拉罐捏扁", "kind": "no", "why": "易拉罐被捏扁以后就那样了，回不去原来的样子，是塑性形变，不会产生弹力。"},
]

CUSTOM_JS = r"""
/* ============================================================
   sci-e-elastic-force 互动逻辑
   1) 选择题接线
   2) 实验室一：弹簧挂钩码（伸长量随钩码变化，超限回不去）
   3) 实验室二：弹性 / 塑性分类（拉一拉 → 松手 → 放进两个筐）
   4) 综合任务：弹力侦探（六种现象分类）
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

  /* ---------- 实验室一：弹簧挂钩码 ---------- */
  var sprStage = document.getElementById('spr-stage');
  if (sprStage) {
    var NAT = 8;            /* 自然长度 cm */
    var LIMIT_W = 5;        /* 弹性限度：5 个钩码 */
    var wCount = 0, damaged = false, released = false;
    var sPath = document.getElementById('spr-path');
    var sWeight = document.getElementById('spr-weight');
    var sWeightT = document.getElementById('spr-weight-t');
    var vW = document.getElementById('spr-w');
    var vLen = document.getElementById('spr-len');
    var vExt = document.getElementById('spr-ext');
    var vF = document.getElementById('spr-f');
    var sOut = document.getElementById('spr-out');

    function drawSpring() {
      var lenCm = NAT + wCount * 2;
      if (released) lenCm = damaged ? NAT + 4 : NAT;
      var px = 40 + (lenCm - NAT) * 10;
      var y0 = 10, y1 = y0 + px;
      var coils = 8, seg = (y1 - y0) / (coils * 2);
      var pts = ['M60,' + y0];
      for (var i = 0; i < coils * 2; i++) {
        pts.push('L' + (i % 2 === 0 ? 26 : 94) + ',' + (y0 + seg * (i + 0.5)).toFixed(1));
      }
      pts.push('L60,' + y1.toFixed(1));
      sPath.setAttribute('d', pts.join(' '));

      var shown = released ? 0 : wCount;
      sWeight.setAttribute('y', (y1 + 6).toFixed(1));
      sWeightT.setAttribute('y', (y1 + 30).toFixed(1));
      sWeightT.textContent = shown + ' 个';
      sWeight.setAttribute('opacity', shown === 0 ? '.28' : '1');
      sWeightT.setAttribute('opacity', shown === 0 ? '.45' : '1');
      sWeight.setAttribute('fill', damaged ? '#ef4444' : '#8d9bb5');

      vW.textContent = shown + ' 个';
      vLen.textContent = lenCm + ' cm';
      vExt.textContent = (lenCm - NAT) + ' cm';
      vF.textContent = (shown * 0.5).toFixed(1) + ' N';

      if (released && damaged) {
        sOut.className = 'result error';
        sOut.innerHTML = '<strong>弹簧停在了 12 厘米，回不到 8 厘米了！</strong>刚才挂的钩码太多，超过了弹性限度，弹簧被拉坏了。所以弹簧测力计上都标着量程，用的时候绝对不能超过。';
      } else if (released) {
        sOut.className = 'result';
        sOut.innerHTML = '<strong>弹簧回到了 8 厘米，一点没变。</strong>受力时变形、撤去力能恢复，这就是<strong>弹性形变</strong>；它在恢复的过程中产生的力，就是<strong>弹力</strong>。';
      } else if (wCount === 0) {
        sOut.className = 'result warn';
        sOut.innerHTML = '弹簧现在的自然长度是 8 厘米，还没有受力。点下面的按钮，给它挂上钩码。';
      } else if (wCount <= LIMIT_W) {
        sOut.className = 'result';
        sOut.innerHTML = '<strong>挂了 ' + wCount + ' 个钩码，弹簧伸长 ' + (wCount * 2) + ' 厘米。</strong>每多挂一个钩码，就多伸长 2 厘米——形变越大，弹簧想恢复的力（弹力）也越大。';
      } else {
        sOut.className = 'result error';
        sOut.innerHTML = '<strong>注意！已经挂了 ' + wCount + ' 个钩码，超过弹性限度了。</strong>再拉下去，弹簧可能再也回不到原来的长度。点一下「松手」，看看会发生什么。';
      }
    }
    document.getElementById('spr-add').addEventListener('click', function () {
      released = false;
      wCount = Math.min(wCount + 1, 6);
      if (wCount > LIMIT_W) damaged = true;
      drawSpring();
    });
    document.getElementById('spr-sub').addEventListener('click', function () {
      released = false;
      wCount = Math.max(wCount - 1, 0);
      drawSpring();
    });
    document.getElementById('spr-release').addEventListener('click', function () {
      released = true;
      wCount = 0;
      drawSpring();
    });
    document.getElementById('spr-reset').addEventListener('click', function () {
      wCount = 0; damaged = false; released = false;
      drawSpring();
    });
    drawSpring();
  }

  /* ---------- 实验室二：弹性 / 塑性分类 ---------- */
  var elasStage = document.getElementById('elas-stage');
  if (elasStage) {
    var ELAS = {
      band:   { n: '橡皮筋', recover: true,  c: '#ff8fa3', why: '橡皮筋被拉长以后一松手，马上就缩回原来的长度。它是弹性形变，恢复时产生了弹力。' },
      spring: { n: '弹簧',   recover: true,  c: '#8d9bb5', why: '弹簧被拉长以后一松手，马上弹回原来的长度。它也是弹性形变。' },
      clay:   { n: '橡皮泥', recover: false, c: '#c98a5b', why: '橡皮泥被拉长以后松手，它就停在那个新形状上，回不去了。这是塑性形变，不会产生弹力。' },
      dough:  { n: '面团',   recover: false, c: '#e8d3a9', why: '面团被拉长以后松手，也不会缩回去。它同样是塑性形变。' }
    };
    var eCur = 'band', eStretch = false;
    var eObj = document.getElementById('elas-obj');
    var eOut = document.getElementById('elas-out');
    var bYes = document.querySelector('[data-bin="yes"] .bin-body');
    var bNo = document.querySelector('[data-bin="no"] .bin-body');
    var placed = {};

    function renderElas() {
      var d = ELAS[eCur];
      eObj.textContent = d.n;
      eObj.style.background = d.c;
      eObj.style.width = eStretch ? '170px' : '72px';
      eObj.style.color = (eCur === 'dough') ? '#5c5142' : '#fff';
      document.querySelectorAll('[data-elas]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.elas === eCur);
      });
      var cnt = 0;
      for (var k in placed) { if (placed[k]) cnt++; }
      if (cnt === 4) {
        eOut.className = 'result';
        eOut.innerHTML = '<strong>四个都分完啦。</strong>橡皮筋和弹簧回得来，是弹性形变；橡皮泥和面团回不去，是塑性形变。判断的依据只有一条：撤去力以后，还能不能回到原来的样子。';
      }
    }
    function place(item, ok) {
      if (placed[item]) return;
      placed[item] = true;
      var tag = document.createElement('span');
      tag.className = 'tag';
      tag.textContent = ELAS[item].n + ' ✓';
      tag.style.borderColor = ok ? 'rgba(78,205,196,.8)' : 'rgba(255,209,102,.9)';
      tag.style.background = ok ? 'rgba(78,205,196,.14)' : 'rgba(255,209,102,.18)';
      (ok ? bYes : bNo).appendChild(tag);
    }
    document.querySelectorAll('[data-elas]').forEach(function (b) {
      b.addEventListener('click', function () {
        eCur = b.dataset.elas;
        eStretch = false;
        eOut.className = 'result warn';
        eOut.innerHTML = '已经拿起 <strong>' + ELAS[eCur].n + '</strong>。先点「拉一拉」，再点「松手」，看看它回不回得来。';
        renderElas();
      });
    });
    document.getElementById('elas-pull').addEventListener('click', function () {
      eStretch = true;
      eOut.className = 'result warn';
      eOut.innerHTML = '<strong>' + ELAS[eCur].n + '被拉长了。</strong>现在松手，看它会不会缩回去。';
      renderElas();
    });
    document.getElementById('elas-release').addEventListener('click', function () {
      var d = ELAS[eCur];
      eStretch = !d.recover;
      eOut.className = 'result ' + (d.recover ? '' : 'warn');
      eOut.innerHTML = '<strong>' + d.n + '：' + (d.recover ? '恢复原状 → 弹性形变' : '保持新形状 → 塑性形变') + '</strong><br>' + d.why;
      place(eCur, d.recover);
      renderElas();
    });
    document.getElementById('elas-reset').addEventListener('click', function () {
      eCur = 'band'; eStretch = false; placed = {};
      bYes.innerHTML = ''; bNo.innerHTML = '';
      eOut.className = 'result warn';
      eOut.textContent = '先选一个物品，拉一拉，再松手。';
      renderElas();
    });
    eOut.className = 'result warn';
    eOut.textContent = '先选一个物品，拉一拉，再松手。';
    renderElas();
  }

  /* ---------- 综合任务：弹力侦探 ---------- */
  var detRoot = document.getElementById('ef-det');
  if (detRoot) {
    var picked = null;
    var doneN = 0, wrongN = 0;
    var detMsg = document.getElementById('ef-det-msg');
    detRoot.querySelectorAll('.sort-item').forEach(function (card) {
      card.addEventListener('click', function () {
        if (card.classList.contains('done')) return;
        detRoot.querySelectorAll('.sort-item').forEach(function (c) { c.style.outline = 'none'; });
        card.style.outline = '3px solid var(--brand)';
        picked = card;
        detMsg.className = 'result warn';
        detMsg.textContent = '已选中「' + card.textContent.trim() + '」，现在点下面左筐或右筐。';
      });
    });
    document.querySelectorAll('[data-ef-bin]').forEach(function (bin) {
      bin.addEventListener('click', function () {
        if (!picked) { detMsg.className = 'result warn'; detMsg.textContent = '先点一张现象卡片，再点筐。'; return; }
        var want = picked.dataset.kind, got = bin.dataset.efBin;
        picked.style.outline = 'none';
        if (want === got) {
          var tag = document.createElement('span');
          tag.className = 'tag';
          tag.textContent = picked.textContent.trim() + ' ✓';
          tag.style.borderColor = 'rgba(78,205,196,.8)';
          tag.style.background = 'rgba(78,205,196,.14)';
          bin.querySelector('.bin-body').appendChild(tag);
          picked.classList.add('done');
          doneN++;
          detMsg.className = 'result';
          detMsg.innerHTML = '<strong>放对了！</strong>' + picked.dataset.why;
          picked = null;
          if (doneN === 6) {
            detMsg.className = 'result';
            detMsg.innerHTML = '<strong>六张卡片全部分类完成，错误 ' + wrongN + ' 次。</strong>你已经在用一条很关键的标准判断：撤去力以后，这个物体还能不能恢复原状。';
          }
        } else {
          wrongN++;
          detMsg.className = 'result error';
          detMsg.innerHTML = '<strong>再想一下：</strong>' + picked.textContent.trim() + ' 里，那个东西受力变形以后，撤去力能恢复原状吗？';
          picked.style.outline = '3px dashed rgba(239,68,68,.7)';
        }
      });
    });
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：它回得来吗？", TTS["pretest"], [
        {"q": "把一根橡皮筋拉长，松手后它会怎样？",
         "options": [("缩回原来的长度", True), ("停在被拉长的样子", False), ("断掉", False)],
         "explain": "橡皮筋撤去力以后能恢复原状，属于弹性形变。<strong>错因提醒：</strong>常见错误是把橡皮筋和橡皮泥搞混——橡皮泥松手后回不去，橡皮筋能回去。"},
        {"q": "下面哪种变化是塑性形变？",
         "options": [("把橡皮泥捏成一个小动物", True), ("把弹簧拉长后松手", False), ("把弯曲的钢尺按直后松手", False)],
         "explain": "橡皮泥捏过之后停在新的形状上，撤去力回不去，是塑性形变。<strong>错因提醒：</strong>判断依据只有一条——撤去力以后能不能恢复原状，不要看它变形大不大。"},
        {"q": "用弹簧测力计测量时，为什么不能挂太重的物体？",
         "options": [("超过了弹性限度，弹簧会被拉坏，读数就不准了", True), ("弹簧会被压短", False), ("物体挂不住会掉下来", False)],
         "explain": "弹簧的伸长量只在弹性限度以内才和力的大小对应。<strong>错因提醒：</strong>很多同学误认为弹簧能无限拉长，其实超过限度它就回不去了。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "受力变形，撤去力能回来的才是弹性形变", TTS["module-1"], f'''
        <p style="font-size:17px;margin:0 0 12px">你已经知道力可以推东西、拉东西。但有一个问题还没弄明白：为什么有的东西被拉长以后，一松手就弹回来，有的却停在原地不动？答案在<strong>材料本身</strong>上。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>弹性形变</strong></p>
            <p style="color:var(--muted)">受力时形状改变，撤去力以后能恢复原状。例：弹簧、橡皮筋、跳跳床、弓。</p>
          </div>
          <div class="inner-card">
            <p><strong>塑性形变</strong></p>
            <p style="color:var(--muted)">受力时形状改变，撤去力以后回不到原来的样子。例：橡皮泥、面团、被揉皱的纸。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="橡皮筋回弹与橡皮泥不回弹的对比示意图">
          <figcaption>同样是被拉长：上面的橡皮筋松手后缩回原长（弹性形变），下面的橡皮泥松手后停在新形状上（塑性形变）</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🔍</span><div><strong>一条标准，两个名字：</strong>判断的时候只问一句话——撤去力以后，它还能不能回到原来的样子？能，就是弹性形变；不能，就是塑性形变。</div></div>
{insight_box([
    {"lens": "看见它", "text": "弹簧被压短、橡皮筋被拉长、弓臂被拉开——这些「变了形但还想回去」的状态，就是弹性形变的现场。"},
    {"lens": "解释它", "text": "为什么它能弹回来？因为材料内部的粒子被挤开或拉开以后，会像一群想回到原位的小朋友一样往回挤，这个往回挤的力就是弹力。"},
    {"lens": "比较它", "text": "弹性形变和塑性形变的差别不在「变形多大」，而在「撤去力以后回不回得去」。橡皮筋拉一点点也会回去，橡皮泥拉一点点也回不去。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "弹簧实验：钩码越多，弹簧伸得越长", TTS["lab-1"], '''
        <p style="color:var(--muted);margin:0 0 12px">每挂一个钩码，看一看弹簧伸长了多少。挂到第 6 个的时候，再点一下「松手」。</p>
        <div class="lab-panel">
          <div class="lab-stage" id="spr-stage" style="height:270px;background:linear-gradient(180deg,#f7fbff 0%,#eef6ff 100%)">
            <div style="position:absolute;left:0;right:0;top:5%;height:10px;background:#cbb894"></div>
            <div style="position:absolute;left:12px;top:5%;font-size:12px;color:#94866c;transform:translateY(-120%)">支架</div>
            <svg viewBox="0 0 120 220" width="120" height="220" style="position:absolute;left:50%;top:9%;transform:translateX(-50%)">
              <path id="spr-path" d="M60,10 L60,40" fill="none" stroke="#7f8fa6" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"></path>
              <rect id="spr-weight" x="36" y="46" width="48" height="34" rx="8" fill="#8d9bb5" opacity=".28"></rect>
              <text id="spr-weight-t" x="60" y="70" text-anchor="middle" font-size="14" font-weight="700" fill="#fff" opacity=".45">0 个</text>
            </svg>
            <div style="position:absolute;left:10px;bottom:10px;font-size:12px;color:#94866c">弹簧自然长度 8 cm</div>
          </div>
          <div class="flex-row" style="margin-top:12px">
            <button class="choice" id="spr-add" style="text-align:center">加一个钩码</button>
            <button class="choice" id="spr-sub" style="text-align:center">减一个钩码</button>
            <button class="choice" id="spr-release" style="text-align:center">松手（撤去力）</button>
            <button class="choice" id="spr-reset" style="text-align:center">重新开始</button>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">钩码</span><span class="v green" id="spr-w">0 个</span></div>
            <div class="readout-cell"><span class="k">弹簧长度</span><span class="v green" id="spr-len">8 cm</span></div>
            <div class="readout-cell"><span class="k">伸长量</span><span class="v" id="spr-ext">0 cm</span></div>
            <div class="readout-cell"><span class="k">弹力（平衡时）</span><span class="v" id="spr-f">0.0 N</span></div>
          </div>
          <p class="result warn" id="spr-out" style="margin-top:12px">弹簧现在的自然长度是 8 厘米，还没有受力。点下面的按钮，给它挂上钩码。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">⚖️</span><div><strong>想一想：</strong>钩码静止挂在弹簧下面，说明弹力正好把钩码托住了，所以弹力的大小就等于钩码受到的重力。这就是弹簧测力计的原理。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "形变越大弹力越大，但弹性有限度", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">刚才的实验告诉我们两句话。第一句：形变越大，弹力越大。第二句：弹簧不可能无限拉长，超过了限度就回不去了。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>弹力大小跟形变程度有关：</strong>挂 1 个钩码，弹簧伸长 2 厘米；挂 3 个，伸长 6 厘米。形变越大，弹力越大。</div></div>
          <div class="step"><span class="n">2</span><div><strong>拉伸的方向就是弹力的方向：</strong>你把橡皮筋往外拉，它往回收；你把弹簧往下压，它往上顶。弹力总想让它恢复原状。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>弹性有限度：</strong>拉得太多，弹簧再也回不到原来的长度，这叫超过了弹性限度。所以弹簧测力计都标着量程。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="弹簧伸长量随钩码数量变化的示意图，以及超过弹性限度后无法恢复">
          <figcaption>限度以内：钩码越多，弹簧伸得越长，伸长量和力一一对应；超过限度：弹簧被拉坏，再也回不到原来的长度</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">很多同学误认为「弹力是物体本来就有的」。其实弹力只有在物体发生弹性形变的时候才会出现，而且形变越大，弹力越大；没有形变，就没有弹力。</p>
        </div>
    ''', tag="概念二"))

    items_html = "\n".join(
        f'            <button class="sort-item" data-elas="{it["id"]}" style="border-color:rgba(78,205,196,.45)">{it["n"]}</button>'
        for it in [
            {"id": "band", "n": "橡皮筋"}, {"id": "spring", "n": "弹簧"},
            {"id": "clay", "n": "橡皮泥"}, {"id": "dough", "n": "面团"},
        ]
    )

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "对比实验：谁回得来，谁回不来", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">选一个物品，先拉一拉，再松手。看看它能不能回到原来的样子，然后放进对应的筐里。</p>
        <div class="lab-panel" id="elas-stage">
          <div class="lab-stage" style="height:170px;background:linear-gradient(180deg,#fffdf8 0%,#f7f2e6 100%)">
            <div id="elas-obj" class="lab-obj" style="top:38%;width:72px;height:44px;background:#ff8fa3;border-radius:14px;transition:width .6s cubic-bezier(.34,1.2,.5,1),background .3s">橡皮筋</div>
          </div>
          <div class="sort-bank" style="margin-top:12px">
{items_html}
          </div>
          <div class="flex-row">
            <button class="choice" id="elas-pull" style="text-align:center">拉一拉</button>
            <button class="choice" id="elas-release" style="text-align:center">松手</button>
            <button class="choice" id="elas-reset" style="text-align:center">重新开始</button>
          </div>
          <p class="result warn" id="elas-out" style="margin-top:12px">先选一个物品，拉一拉，再松手。</p>
          <div class="sort-bins">
            <div class="sort-bin" data-bin="yes">
              <h4>🪃 弹性形变（回得来）</h4>
              <div class="bin-body"></div>
            </div>
            <div class="sort-bin" data-bin="no">
              <h4>🧱 塑性形变（回不去）</h4>
              <div class="bin-body"></div>
            </div>
          </div>
        </div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：弹簧测力计为什么能量出力", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>把 1 个钩码挂在弹簧下面，弹簧伸长 2 厘米；挂 3 个同样的钩码，弹簧伸长 6 厘米。为什么弹簧测力计可以量出力的大小？</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看清现象：</strong>钩码挂得越多，弹簧伸得越长。力越大，形变越大。</div></div>
          <div class="step"><span class="n">2</span><div><strong>找出关系：</strong>钩码数变成原来的 3 倍，伸长量也从 2 厘米变成 6 厘米，也是 3 倍。伸长量和力一一对应。</div></div>
          <div class="step"><span class="n">3</span><div><strong>得出方法：</strong>在弹簧旁边标好刻度，用伸长量就能读出力的大小——这就是弹簧测力计。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>特别注意：</strong>这种对应关系只在<strong>弹性限度以内</strong>成立。超过了，弹簧被拉坏，读数就不再准，所以测力计上都写着量程。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错法</span>
          <p style="margin:6px 0 0">说「弹簧本来就有一股力」是不对的。弹力只在<strong>发生弹性形变的时候</strong>才出现。没有形变，就没有弹力；形变撤去，弹力也跟着消失。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：这三种说法错在哪里", TTS["conceptest-1"], [
        {"q": "关于弹力，下面哪句话是对的？",
         "options": [("弹力只有在物体发生弹性形变时才出现", True),
                     ("只要是固体就一定有弹力", False),
                     ("弹力的大小跟形变程度没有关系", False)],
         "explain": "弹力来自弹性形变的恢复过程，形变越大弹力越大。<strong>错因提醒：</strong>常见错误是误认为弹力是物体自带的，忽略了它必须由形变产生。"},
        {"q": "把一根弹簧拉到超过弹性限度，会怎样？",
         "options": [("弹簧不能完全恢复原来的长度，测力也会不准", True),
                     ("弹簧会变得更有弹性", False),
                     ("弹簧会变成橡皮泥", False)],
         "explain": "超过限度弹簧就被拉坏了，只能恢复一部分。<strong>错因提醒：</strong>不少同学认为弹簧可以无限拉长，所以用弹簧测力计时随手超量程，这是要避免的。"},
        {"q": "把橡皮泥捏成一只小动物，这个变化属于：",
         "options": [("塑性形变，撤去力以后不能恢复原状", True),
                     ("弹性形变，因为橡皮泥有弹性", False),
                     ("不是形变，只是形状变好看", False)],
         "explain": "橡皮泥捏过以后停在新形状上，回不去原来的样子，是塑性形变。<strong>错因提醒：</strong>不要把「形状变了」和「有弹力」搞混，关键要看撤去力以后回不回得来。"}
    ], tag="概念测试"))

    items6 = "\n".join(
        f'            <button class="sort-item" data-kind="{it["kind"]}" data-why="{it["why"]}">{it["t"]}</button>'
        for it in SORT_ITEMS
    )

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：当一次弹力侦探", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一张现象卡片，再点你认为正确的筐。每放一次都会立刻告诉你理由。</p>
        <div class="lab-panel" id="ef-det">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">待判断的现象</div>
          <div class="sort-bank">
{items6}
          </div>
          <div class="sort-bins">
            <div class="sort-bin" data-ef-bin="yes">
              <h4>🪃 有弹力在起作用</h4>
              <div class="bin-body"></div>
            </div>
            <div class="sort-bin" data-ef-bin="no">
              <h4>🧱 没有弹力（塑性形变）</h4>
              <div class="bin-body"></div>
            </div>
          </div>
          <p class="result warn" id="ef-det-msg" style="margin-top:12px">点一张卡片开始判断。</p>
        </div>
        <div class="inner-card">
          <p><strong>再想一想：</strong>你自己设计的弹力装置里，是哪个部分发生了弹性形变？把它的名字写下来。</p>
          <textarea rows="2" placeholder="会形变的部分是……因为撤去力以后它能……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换个情境，规律还在不在", TTS["posttest"], [
        {"q": "汽车的减震器里装着弹簧，它的主要作用是：",
         "options": [("让车身在颠簸时能缓一缓，靠弹力把震动吸收掉", True),
                     ("让汽车变重一些", False),
                     ("让汽车跑得更快", False)],
         "explain": "路面颠簸时弹簧被压缩，弹性形变恢复时把冲击化解掉，所以坐在车里会稳一些。"},
        {"q": "撑杆跳运动员把杆压弯后弹起来，这个过程中：",
         "options": [("杆发生了弹性形变，恢复时产生的弹力把人推上去", True),
                     ("杆被压坏了，所以人弹不高", False),
                     ("人自己跳得高，跟杆没关系", False)],
         "explain": "撑杆被压弯是弹性形变，恢复时产生的弹力把运动员推向上方。形变越大，弹力越大。"},
        {"q": "用弹簧测力计测量一个 8 牛的力，但它的量程只有 5 牛。正确的做法是：",
         "options": [("换一个量程更大的测力计", True),
                     ("照样挂上去，凑合读一下", False),
                     ("把弹簧拉长一点再用", False)],
         "explain": "超过弹性限度会把弹簧拉坏，读数也不准。所以必须换成量程合适的测力计。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：形变、弹力、限度", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>形变</strong>：物体受力，形状会改变。撤去力能恢复原状的叫弹性形变。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>弹力</strong>：弹性形变在恢复的过程中产生的力，就叫弹力。没有形变就没有弹力。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>大小</strong>：弹力的大小跟形变程度有关，形变越大，弹力越大，而且拉伸方向就是它想恢复的方向。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>限度</strong>：弹性有一定限度，超过了就回不去，所以弹簧测力计都有量程。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那两样东西：</strong>橡皮筋松手能缩回去，因为它发生的是弹性形变，恢复时产生了弹力；橡皮泥松手停在原地，因为它发生的是塑性形变，不产生弹力。跳跳床能把你弹起来，也是同一个道理——床面被压下，恢复时把弹力还给了你。</p>
        </div>
        <div class="inner-card">
          <p><strong>打个比方记住它：</strong>弹性形变就像被人挤开的小朋友，一放手就想挤回自己的位置，这个往回挤的劲就是弹力。塑性形变就像大家重新排了一次队，位置定下来就不动了。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "用一句话说清楚什么是弹性形变、什么是塑性形变，并各举一个例子。",
            "写出弹力的大小和什么有关，并说明弹簧测力计为什么有量程。",
        ],
        [
            "用一根橡皮筋、一个纸杯和一个小纸球，做一个能把纸球弹起来的小装置，记下你的做法和结果。",
            "在家找三样东西，判断它们受到挤压或拉伸时发生的是弹性形变还是塑性形变，各写一句理由。",
        ],
        [
            "设计一个用弹力的物品（比如自动关门的装置、弹跳玩具），画出草图，写出你选的材料、它为什么能提供弹力，以及使用时的限度。",
            "找一找生活中因为超过弹性限度而坏掉的例子（比如被拉变形的弹簧、被撑大的毛衣），说明它是怎么发生的。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "sci-e-elastic-force",
    "node_id": "sci-e-elastic-force",
    "title": "弹力：被压弯的东西想弹回来",
    "name_en": "Elastic Force: Why Bent Things Want to Spring Back",
    "grade": 5,
    "grade_cn": "五年级",
    "domain": "matter-science",
    "domain_cn": "物质科学 · 力",
    "lesson_type": "experiment-inquiry",
    "version": "1.0.0",
    "description": "通过弹簧挂钩码与弹性/塑性对比实验，让学生自己归纳出弹性形变与塑性形变的判据、弹力的来源与大小规律，并知道弹性有限度、弹簧测力计因此必有量程。",
    "tags": ["弹力", "弹性形变", "塑性形变", "弹性限度", "弹簧测力计"],
    "standard_ref": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念3「物质的运动与相互作用」学习内容3.1 力是改变物体运动状态的原因——5～6年级观察常见的摩擦力、弹力、浮力和地球引力，知道弹力是物体发生弹性形变时产生的力。",
    "hero_question": "橡皮筋一松手就弹回来，橡皮泥一松手就不动——差别在哪里？",
    "hero_alt": "弹力知识结构图：弹性形变、弹力大小与弹性限度三栏",
    "hero_caption": "受力变形 · 撤去力能恢复的叫弹性形变 · 恢复时产生的力叫弹力 · 形变越大弹力越大 · 弹性有限度",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的实验都会围着它转。",
    "anchor_choices": [
        {"t": "为什么有的东西能弹回来？", "d": "想弄清弹性形变和塑性形变的区别", "v": "为什么有的东西能弹回来"},
        {"t": "弹力到底有多大？", "d": "想知道弹力和形变是什么关系", "v": "弹力到底有多大"},
        {"t": "为什么弹簧拉过头就回不去了？", "d": "想弄明白弹性限度", "v": "为什么弹簧拉过头就回不去了"},
        {"t": "弹簧测力计是怎么量出力的？", "d": "想自己读出一个力的大小", "v": "弹簧测力计是怎么量出力的"},
    ],
    "objectives": [
        "能说出物体受力会发生形变，撤去力后能恢复原状的叫弹性形变",
        "能说出弹性形变恢复时产生的力叫弹力，没有形变就没有弹力",
        "能说出弹力的大小与形变的程度有关，形变越大弹力越大",
        "知道弹性有一定的限度，超过限度物体无法恢复原状，能解释弹簧测力计为什么有量程",
    ],
    "objectives_plain": [
        "能说出物体受力会发生形变，撤去力后能恢复原状的叫弹性形变",
        "能说出弹性形变恢复时产生的力叫弹力，没有形变就没有弹力",
        "能说出弹力的大小与形变的程度有关，形变越大弹力越大",
        "知道弹性有一定的限度，超过限度物体无法恢复原状，能解释弹簧测力计为什么有量程",
    ],
    "standards": [
        {"content": "观察常见的弹力，知道弹力是物体发生弹性形变时产生的力",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念3 物质的运动与相互作用 学习内容3.1 力是改变物体运动状态的原因（5～6年级）"},
        {"content": "能基于观察到的现象归纳出弹力大小与形变程度的关系，并说明弹性限度",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念3 物质的运动与相互作用 学习内容3.1（5～6年级）"},
    ],
    "prereqs": ["sci-e-push-pull-force"],
    "prereqs_name": "推和拉的力",
    "prereqs_meta": "sci-e-push-pull-force",
    "leads_to": ["sci-e-buoyancy"],
    "next_meta": "sci-e-buoyancy",
    "section_images": ["assets/sci-e-elastic-force-fig1.webp", "assets/sci-e-elastic-force-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "橡皮筋弹回来，橡皮泥不回弹——同样被拉，差别在哪里？带着这个疑问开始。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能自己判断一个形变是弹性的还是塑性的。",
        "objectives": "看清四件事：说出弹性形变、说出弹力、说出弹力与形变的关系、知道弹性有限度。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "判断只有一条标准：撤去力以后，它还能不能回到原来的样子。",
        "lab-1": "挂到第 6 个钩码，再点「松手」，看看弹簧能不能回到 8 厘米。",
        "module-2": "形变越大弹力越大，但只在弹性限度以内成立——所以测力计都有量程。",
        "lab-2": "每个物品都先拉一拉再松手，然后放进对应的筐里。",
        "worked-example": "四步走：看清现象、找出关系、得出方法、特别注意限度。",
        "conceptest-1": "弹力不是物体自带的，它只在发生弹性形变的时候才出现。",
        "synthesis": "六种现象逐一判断，只问一句：撤去力以后能不能恢复原状。",
        "posttest": "换了减震器、撑杆跳和量程，看看你还能不能用上同一条规律。",
        "summary": "回到开头那两样东西：橡皮筋和橡皮泥，差别到底在哪里？用四句话说清楚。",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是「物质的运动与相互作用」里力的板块空缺：知识树原有推和拉的力、摩擦力与浮力，缺课标明确要求的弹力。设计上不引入胡克定律的表达式，只把两件事做实——用弹簧挂钩码的真实数据让学生自己看出「形变越大弹力越大」，再让弹簧真的被拉坏一次，让「弹性限度」成为亲眼见过的后果而不是老师的一句叮嘱。判据收敛为一句可带走的话：撤去力以后，它还能不能回到原来的样子。",
    "plan_table": """| 1 | cover | 弹力：被压弯的东西想弹回来 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：它回得来吗？ | 起·前测（暴露直觉） |
| 5 | concept | 受力变形，撤去力能回来的才是弹性形变 | 承·概念一 |
| 6 | interactive | 弹簧实验：钩码越多，弹簧伸得越长 | 承·实验室一（含超限回不去） |
| 7 | concept | 形变越大弹力越大，但弹性有限度 | 承·概念二（含常见错误） |
| 8 | interactive | 对比实验：谁回得来，谁回不来 | 承·实验室二（弹性/塑性分类） |
| 9 | concept | 例题示范：弹簧测力计为什么能量出力 | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：这三种说法错在哪里 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：当一次弹力侦探 | 合·迁移应用 |
| 12 | quiz | 后测：换个情境，规律还在不在 | 合·后测 |
| 13 | summary | 小结：形变、弹力、限度 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：弹性形变、弹力大小、弹性限度三栏标注\n- P5 橡皮筋与橡皮泥对比图（已生成）：回得来 vs 回不去\n- P7 弹簧伸长量与弹性限度示意图（已生成）：限度以内一一对应，超过限度回不去\n- 若需补充：弹簧测力计的实拍照片、撑杆跳与跳跳床的实景图",
}
