# -*- coding: utf-8 -*-
"""小学科学 · 人的生命从哪里来（G6）—— 补齐课标「生命的延续与进化·8.3 人的生命从受精卵开始」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/sci-e-human-life-origin-fig1.webp'
F2 = './assets/sci-e-human-life-origin-fig2.webp'

TTS = {
    "hero": "每个同学都曾经问过一个问题：我是从哪里来的？答案就藏在你自己身上。你的生命，最初只是一个细胞，小到看不见。它一点点分裂、长大，在妈妈的身体里住了九个多月，才有了今天的你。这节课我们就沿着这条路，看看一个小生命是怎样一步步长出来的。",
    "problem-anchor": "开始之前，先选一个你最想弄明白的问题。是想知道生命的起点是什么样子，还是想知道我在妈妈身体里住了多久、怎么长大的，又或者你想弄清楚为什么我既像爸爸又像妈妈。选好之后，带着问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出人的生命是从受精卵开始的。第二，能说出受精卵经过细胞分裂，逐步发育成胎儿，大约三十八周后出生。第三，能说出新生命同时带着父母双方的遗传信息，所以和家人既像又不像。第四，能体会每一个生命都来之不易，懂得珍爱自己和他人的生命。",
    "pretest": "先做三道小题，用你现在的想法选就好。选完马上能看到解释，选错了也没关系，正好知道要重点听哪里。",
    "module-1": "我们的生命，都是从一个细胞开始的。这个细胞叫受精卵，它是爸爸提供的一份遗传信息和妈妈提供的一份遗传信息结合在一起形成的。受精卵会不断分裂，一个变成两个，两个变成四个，越分越多，慢慢长出各种器官，变成一个小宝宝。他在妈妈身体里一个温暖的地方住下来，从这里获得营养，大约住三十八周，也就是九个多月，然后才出生。妈妈孕育我们的这段时间很辛苦，所以每一个生命都来得不容易。",
    "lab-1": "现在请你拖动时间滑块，沿着小生命长大的这条路走一遍。从受精卵开始，经过细胞分裂、在妈妈身体里安家、器官形成，一直到长成胎儿。每到一站，右边都会出现这一站的说明。",
    "module-2": "你一定听大人说过：眼睛像妈妈，鼻子像爸爸。这是为什么？因为新生命身上，同时带着爸爸和妈妈双方的遗传信息。你的每一个特征，都是由两份遗传信息一起决定的。有的特征，爸爸给的那份影响更明显；有的特征，妈妈给的那份影响更明显；还有一些，会像家里的其他长辈。所以你和家人既像又不像，这就是你独一无二的原因。",
    "lab-2": "下面我们来玩一个配对游戏。这里有六个特征，请你判断它来自爸爸、来自妈妈，还是爸爸妈妈都有份。放完六个，你会有新的发现。",
    "worked-example": "我们一起分析一道题：为什么弟弟的眼睛像妈妈，鼻子却像爸爸？第一步，先看清楚问题问的是什么，问的是长相特征的来源。第二步，回想遗传信息从哪里来，新生命的遗传信息来自爸爸和妈妈双方。第三步，比较结果，每个特征都由两份信息一起决定，哪一份影响更明显，表现出来的样子就更像谁。第四步，得出结论，弟弟身上同时带着爸爸妈妈的遗传信息，所以有的地方像妈妈，有的地方像爸爸。",
    "conceptest-1": "下面有三道容易弄错的说法，请你仔细读每一个选项，选完再看解释，看看自己有没有掉进那几个常见的坑里。",
    "synthesis": "最后一件事交给你。请你用三句话，给一年级的小朋友讲清楚我从哪里来。讲完之后，用下面的清单检查一下：三句话里有没有说清楚起点、说清楚怎么长大、说清楚遗传信息从哪里来。",
    "posttest": "最后一轮，用新的情境检验一下。这里面有细胞分裂、像爷爷的特征，还有如何对待生命，看看你能不能把学到的知识用上去。",
    "summary": "这节课我们沿着来时的路走了一遍。人的生命，从受精卵开始；受精卵经过细胞不断分裂，一步步长出各种器官，发育成胎儿，在妈妈身体里大约住三十八周后出生。新生命身上同时带着爸爸妈妈双方的遗传信息，所以和家人既像又不像。回到你最开始时问的那个问题，答案就是：你是爸爸妈妈的遗传信息结合在一起，一点一点长出来的，每一个生命都来之不易。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出人的生命从什么开始，以及在妈妈身体里大约住多少周才出生。第二层能力应用，动手做：做一张我和家人的特征小调查，把三个特征记下来，写清楚它更像爸爸还是更像妈妈。第三层迁移挑战，选做：写一小段话，讲给爸爸妈妈听，说说你知道自己生命来历之后的感受，也可以采访妈妈怀你时的经历，记录下来。",
    "knowledge-graph": "这张图展示了这节课在科学知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 从受精卵开始", "lab-1": "实验室一 发育时间轴", "module-2": "概念二 遗传信息来自父母",
    "lab-2": "实验室二 我像谁", "worked-example": "例题讲解 弟弟像谁", "conceptest-1": "概念测试",
    "synthesis": "综合任务 讲给小朋友听", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

TRAITS = [
    {"id": "eye", "t": "双眼皮", "kind": "both",
     "why": "眼皮是单是双，由爸爸妈妈各给的一份遗传信息一起决定，所以可能像爸爸，也可能像妈妈。"},
    {"id": "dimple", "t": "酒窝", "kind": "both",
     "why": "笑起来有没有小酒窝，同样是父母双方的信息共同决定的结果。"},
    {"id": "blood", "t": "血型", "kind": "both",
     "why": "你的血型由爸爸妈妈各提供的一份信息一起决定，所以常常和家里人有相同的血型。"},
    {"id": "curl", "t": "头发直还是卷", "kind": "both",
     "why": "头发是直是卷，来自父母双方的遗传信息，不是只听一个人的。"},
    {"id": "ear", "t": "耳垂的形状", "kind": "both",
     "why": "耳垂是分开的还是连着长的，也由父母双方的遗传信息共同决定。"},
    {"id": "height", "t": "个子高矮的倾向", "kind": "both",
     "why": "身高的倾向受父母双方的遗传信息影响，当然，后天的营养和运动也很重要。"},
]

CHECKLIST = [
    "我说清楚了生命的起点是受精卵，而不是出生那一刻。",
    "我说清楚了细胞会不断分裂，慢慢长出各种器官。",
    "我说清楚了小宝宝大约在妈妈身体里住三十八周。",
    "我说清楚了身上同时带着爸爸妈妈双方的遗传信息。",
]

CUSTOM_JS = r"""
/* ============================================================
   sci-e-human-life-origin 互动逻辑
   1) 选择题接线
   2) 发育时间轴：滑块 / 站点按钮 → 五站发育图与说明
   3) 我像谁：六个特征 → 来自爸爸 / 来自妈妈 / 爸爸妈妈都有份
   4) 讲解自评清单
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

  /* ---------- 2. 发育时间轴 ---------- */
  var tw = document.getElementById('tl-canvas');
  if (tw) {
    var tctx = tw.getContext('2d');
    var tlRange = document.getElementById('tl-range');
    var STATIONS = [
      { title: '受精卵', when: '生命的起点', size: '约 0.1 毫米',
        msg: '爸爸和妈妈各提供一份遗传信息，结合在一起形成一个新的细胞，叫做受精卵。每个同学的生命，都是从这一个细胞开始的。' },
      { title: '细胞分裂', when: '第 1 周', size: '约 0.2 毫米',
        msg: '受精卵一个变成两个，两个变成四个，越分越多，慢慢形成一个小小的细胞团。' },
      { title: '在妈妈身体里安家', when: '第 2 周左右', size: '约 0.3 毫米',
        msg: '细胞团住进妈妈身体里一个温暖的地方，从这里获得氧气和营养，开始安稳地生长。' },
      { title: '器官开始形成', when: '第 4 ～ 8 周', size: '约 2.5 厘米',
        msg: '心脏开始跳动，手和脚的轮廓慢慢出现，身体的各个器官开始一样一样地形成。' },
      { title: '长成胎儿', when: '第 9 周以后', size: '出生时约 50 厘米',
        msg: '他会伸伸胳膊、蹬蹬腿，还能听见妈妈的心跳和说话声。大约 38 周，也就是九个多月以后，他才出生。' }
    ];
    var sid = 0;
    var titleEl = document.getElementById('tl-title');
    var whenEl = document.getElementById('tl-when');
    var sizeEl = document.getElementById('tl-size');
    var outEl = document.getElementById('tl-out');

    function circle(x, y, r) { tctx.beginPath(); tctx.arc(x, y, r, 0, Math.PI * 2); }
    function note(str, x, y, size, color, align) {
      tctx.fillStyle = color || '#3a3126';
      tctx.font = '700 ' + (size || 16) + 'px "PingFang SC", "Microsoft YaHei", sans-serif';
      tctx.textAlign = align || 'center';
      tctx.fillText(str, x, y);
      tctx.textAlign = 'left';
    }
    function backdrop() {
      var W = tw.width, H = tw.height;
      tctx.setTransform(1, 0, 0, 1, 0, 0);
      tctx.clearRect(0, 0, W, H);
      var g = tctx.createRadialGradient(360, 150, 20, 360, 150, 420);
      g.addColorStop(0, '#fff8f2');
      g.addColorStop(1, '#ffeede');
      tctx.fillStyle = g;
      tctx.fillRect(0, 0, W, H);
      tctx.strokeStyle = 'rgba(255,107,107,.18)';
      tctx.lineWidth = 3;
      for (var i = 1; i < 5; i++) {
        tctx.beginPath();
        tctx.moveTo(120 + i * 120, 40);
        tctx.lineTo(120 + i * 120, 280);
        tctx.stroke();
      }
    }
    // 中性、简洁的早期发育示意
    function drawEmbryo(cx, cy, scale, phase) {
      tctx.save();
      tctx.translate(cx, cy);
      tctx.scale(scale, scale);
      tctx.strokeStyle = '#c98b8b';
      tctx.lineWidth = 3.4;
      tctx.fillStyle = '#ffe3e3';
      // 头
      circle(-6, -18, 22); tctx.fill(); tctx.stroke();
      // 蜷曲的身体
      tctx.beginPath();
      tctx.moveTo(-6, 4);
      tctx.quadraticCurveTo(26, 8, 14, 34);
      tctx.quadraticCurveTo(2, 54, -22, 40);
      tctx.quadraticCurveTo(-34, 20, -6, 4);
      tctx.stroke();
      if (phase >= 3) {
        // 小手小脚
        tctx.beginPath(); tctx.moveTo(6, 12); tctx.lineTo(34, 4); tctx.stroke();
        tctx.beginPath(); tctx.moveTo(-10, 40); tctx.lineTo(-24, 60); tctx.stroke();
        tctx.fillStyle = '#ff8f8f';
        note('♥', -2, -14, 18, '#ff6b6b', 'center');
      }
      tctx.restore();
    }

    function drawStage(i) {
      backdrop();
      if (i === 0) {
        tctx.fillStyle = '#ffe3e3';
        tctx.strokeStyle = '#c98b8b';
        tctx.lineWidth = 3.4;
        circle(360, 160, 52); tctx.fill(); tctx.stroke();
        tctx.fillStyle = 'rgba(160,205,240,.75)';
        circle(388, 138, 16); tctx.fill();
        note('1 个细胞', 360, 258, 18, '#b03a3a');
        note('爸爸一份 + 妈妈一份遗传信息结合', 360, 288, 16, '#5c5142');
      } else if (i === 1) {
        var pts = [[360, 150], [306, 128], [414, 128], [286, 176], [434, 176], [316, 200], [404, 200], [360, 178]];
        pts.forEach(function (p, k) {
          tctx.fillStyle = k % 2 ? '#ffe3e3' : '#e6f2ff';
          tctx.strokeStyle = '#c98b8b';
          tctx.lineWidth = 2.4;
          circle(p[0], p[1], 24); tctx.fill(); tctx.stroke();
        });
        note('1 → 2 → 4 → 8 ……', 360, 258, 18, '#b03a3a');
        note('细胞不断分裂，数目越来越多', 360, 288, 16, '#5c5142');
      } else if (i === 2) {
        tctx.strokeStyle = '#e0a5a5';
        tctx.lineWidth = 14;
        tctx.beginPath();
        tctx.moveTo(120, 300);
        tctx.quadraticCurveTo(140, 130, 360, 110);
        tctx.quadraticCurveTo(580, 130, 604, 300);
        tctx.stroke();
        var cp = [[330, 200], [360, 182], [392, 200], [346, 220], [378, 220], [362, 236]];
        cp.forEach(function (p, k) {
          tctx.fillStyle = k % 2 ? '#ffe3e3' : '#e6f2ff';
          tctx.strokeStyle = '#c98b8b';
          tctx.lineWidth = 2.4;
          circle(p[0], p[1], 18); tctx.fill(); tctx.stroke();
        });
        note('一个温暖的地方', 360, 60, 18, '#b03a3a');
        note('细胞团在这里住下来，获得氧气和营养', 360, 292, 16, '#5c5142');
      } else if (i === 3) {
        drawEmbryo(360, 160, 1.15, 3);
        note('心脏开始跳动，手脚的轮廓出现', 360, 276, 17, '#5c5142');
        note('第 4 ～ 8 周', 360, 60, 18, '#b03a3a');
      } else {
        drawEmbryo(360, 158, 1.45, 4);
        tctx.strokeStyle = 'rgba(120,170,200,.8)';
        tctx.lineWidth = 2.6;
        for (var r = 1; r <= 3; r++) {
          tctx.beginPath();
          tctx.arc(452, 120, 12 * r, -0.6, 0.9);
          tctx.stroke();
        }
        note('听见妈妈的心跳和说话声', 560, 108, 16, '#2b6f9e');
        note('大约 38 周以后出生', 360, 288, 18, '#b03a3a');
      }
      document.querySelectorAll('[data-tl-jump]').forEach(function (b) {
        b.classList.toggle('selected', parseInt(b.dataset.tlJump, 10) === i);
      });
    }

    function renderTl(i) {
      sid = Math.max(0, Math.min(4, i));
      var s = STATIONS[sid];
      drawStage(sid);
      titleEl.textContent = s.title;
      whenEl.textContent = s.when;
      sizeEl.textContent = s.size;
      outEl.className = 'result';
      outEl.innerHTML = '<strong>第 ' + (sid + 1) + ' 站 · ' + s.title + '</strong>（' + s.when + '）：' + s.msg;
    }
    tlRange.addEventListener('input', function () {
      renderTl(Math.min(4, Math.floor(parseInt(tlRange.value, 10) / 20)));
    });
    document.querySelectorAll('[data-tl-jump]').forEach(function (b) {
      b.addEventListener('click', function () {
        var i = parseInt(b.dataset.tlJump, 10);
        tlRange.value = String(i * 20 + 10);
        renderTl(i);
      });
    });
    renderTl(0);
  }

  /* ---------- 3. 我像谁 ---------- */
  var tbank = document.getElementById('trait-bank');
  if (tbank) {
    var pickedT = null;
    var doneT = 0, wrongT = 0;
    var tmsg = document.getElementById('trait-msg');
    var totalT = tbank.querySelectorAll('.sort-item').length;

    tbank.querySelectorAll('.sort-item').forEach(function (card) {
      card.addEventListener('click', function () {
        if (card.classList.contains('done')) return;
        tbank.querySelectorAll('.sort-item').forEach(function (c) { c.style.outline = 'none'; });
        card.style.outline = '3px solid var(--brand)';
        pickedT = card;
        tmsg.className = 'result warn';
        tmsg.textContent = '已选中「' + card.textContent.trim() + '」，现在点下面三个筐里的一个。';
      });
    });

    document.querySelectorAll('[data-trait-bin]').forEach(function (bin) {
      bin.addEventListener('click', function () {
        if (!pickedT) { tmsg.className = 'result warn'; tmsg.textContent = '先点一张特征卡片，再点筐。'; return; }
        var want = pickedT.dataset.kind, got = bin.dataset.traitBin;
        var name = pickedT.textContent.trim();
        pickedT.style.outline = 'none';
        if (want === got) {
          var tag = document.createElement('span');
          tag.className = 'tag';
          tag.textContent = name + ' ✓';
          tag.style.borderColor = 'rgba(78,205,196,.8)';
          tag.style.background = 'rgba(78,205,196,.14)';
          bin.querySelector('.bin-body').appendChild(tag);
          pickedT.classList.add('done');
          doneT++;
          tmsg.className = 'result';
          tmsg.innerHTML = '<strong>放对了！</strong>' + pickedT.dataset.why;
          pickedT = null;
          if (doneT === totalT) {
            tmsg.className = 'result';
            tmsg.innerHTML = '<strong>六张全部完成，错误 ' + wrongT + ' 次。</strong>你有没有发现：这些特征都被归到了同一个筐里——爸爸妈妈都有份。每个人身上都同时带着父母双方的遗传信息，所以和家人既像又不像。';
          }
        } else {
          wrongT++;
          tmsg.className = 'result error';
          tmsg.innerHTML = '<strong>再想一下：</strong>' + name + ' 真的只来自一个人吗？每一个特征，都是由爸爸妈妈各给的一份遗传信息一起决定的。你把它只算给了一方，就是把父母共同决定这件事搞混了。';
          pickedT.style.outline = '3px dashed rgba(239,68,68,.7)';
        }
      });
    });
  }

  /* ---------- 4. 讲解自评清单 ---------- */
  var cl = document.getElementById('check-list');
  if (cl) {
    var clOut = document.getElementById('check-out');
    var items = cl.querySelectorAll('[data-check]');
    cl.addEventListener('click', function (e) {
      var btn = e.target.closest ? e.target.closest('[data-check]') : null;
      if (!btn) return;
      btn.classList.toggle('selected');
      var n = 0;
      items.forEach(function (b) { if (b.classList.contains('selected')) n++; });
      clOut.className = 'result ' + (n === items.length ? '' : 'warn');
      clOut.innerHTML = n === items.length
        ? '<strong>四项全部达标！</strong>你的讲解已经包含起点、成长、时间、遗传信息四件要紧的事，可以讲给一年级的小朋友听了。'
        : '你已经做到 <strong>' + n + ' / ' + items.length + '</strong> 项。再检查一下还没点亮的那几条，把它补进你的三句话里。';
    });
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：你从哪里来？", TTS["pretest"], [
        {"q": "人的生命是从哪里开始的？",
         "options": [("从一个细胞开始，这个细胞叫受精卵", True), ("从出生那一刻开始", False), ("从会走路开始", False)],
         "explain": "生命从一个受精卵开始，出生之前已经在妈妈身体里生长了九个多月。<strong>错因提醒：</strong>常见错误是误认为生命从出生才开始的，把出生当成了起点。"},
        {"q": "一个小宝宝在妈妈身体里大约住多久才出生？",
         "options": [("大约 38 周，也就是九个多月", True), ("大约 3 周", False), ("大约 5 年", False)],
         "explain": "从受精卵到出生，大约要经过 38 周。<strong>错因提醒：</strong>把 38 周和 38 天搞混是这一课最容易出现的错误，九个多月可不短。"},
        {"q": "为什么我们和家人既像又不像？",
         "options": [("因为身上同时带着爸爸妈妈双方的遗传信息", True),
                     ("因为长相会自己变化", False),
                     ("因为和谁生活得久就像谁", False)],
         "explain": "每个特征都由父母双方的遗传信息一起决定，哪一份影响更明显，就更像谁。这一题先记在心里。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "人的生命从受精卵开始，大约 38 周后出生", TTS["module-1"], f'''
        <p style="font-size:17px;margin:0 0 12px">你已经知道，除病毒外的生物体都是由细胞构成的。<strong>那么</strong>我们每一个人的生命，最开始是什么样子？答案是：<strong>一个细胞</strong>。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>起点：受精卵</strong></p>
            <p style="color:var(--muted)">爸爸和妈妈各提供一份遗传信息，结合在一起，形成一个新的细胞，叫做受精卵。</p>
          </div>
          <div class="inner-card">
            <p><strong>发育：分裂与生长</strong></p>
            <p style="color:var(--muted)">细胞不断分裂、逐渐分化，慢慢长出各种器官，最后发育成胎儿。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="人的生命早期发育时间轴示意图，从受精卵到胎儿">
          <figcaption>从小到大的五个阶段：受精卵 → 细胞分裂 → 在妈妈身体里安家 → 器官形成 → 长成胎儿</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">⏳</span><div><strong>记住这个数字：</strong>大约 <strong>38 周</strong>，也就是九个多月。这九个多月里，妈妈一直小心地照顾着我们，所以每一个生命都来之不易。</div></div>
{insight_box([
    {"lens": "解释它", "text": "为什么说一个细胞就能长成一个人？因为细胞会不断分裂，让数目变多，还会逐渐分化，长成心脏、大脑这些不同的器官。"},
    {"lens": "比较它", "text": "比起上一课认识的草履虫，我们的起点也是一个细胞；不同的是我们的细胞会分工，最后组成完整的身体。"},
    {"lens": "迁移它", "text": "其他动物也大多从受精卵开始发育，只不过时间长短不同——小鸡大约 21 天，小狗大约 60 天。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "发育时间轴：从受精卵到胎儿，走一遍", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">拖动滑块，或者直接点下面的站点按钮，看看小生命在每一站是什么样子。</p>
        <div class="lab-panel">
          <div class="canvas-wrap" style="padding:10px">
            <canvas id="tl-canvas" width="720" height="320" style="width:100%;display:block;border-radius:14px"></canvas>
          </div>
          <div class="slider-row">
            <label for="tl-range">时间轴</label>
            <input type="range" id="tl-range" min="0" max="100" value="0" step="1">
          </div>
          <div class="flex-row" style="margin-top:6px">
            <button class="choice" data-tl-jump="0" style="text-align:center;font-size:13px">受精卵</button>
            <button class="choice" data-tl-jump="1" style="text-align:center;font-size:13px">细胞分裂</button>
            <button class="choice" data-tl-jump="2" style="text-align:center;font-size:13px">安家</button>
            <button class="choice" data-tl-jump="3" style="text-align:center;font-size:13px">器官形成</button>
            <button class="choice" data-tl-jump="4" style="text-align:center;font-size:13px">胎儿</button>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">现在到哪一步</span><span class="v" id="tl-title">受精卵</span></div>
            <div class="readout-cell"><span class="k">大约时间</span><span class="v" id="tl-when">生命的起点</span></div>
            <div class="readout-cell"><span class="k">大约大小</span><span class="v green" id="tl-size">约 0.1 毫米</span></div>
          </div>
          <p class="result" id="tl-out" style="margin-top:12px"></p>
        </div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "你身上带着爸爸妈妈双方的遗传信息", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">你一定听大人说过：眼睛像妈妈，鼻子像爸爸。<strong>为什么</strong>会这样？因为新生命身上，同时带着<strong>爸爸妈妈双方的遗传信息</strong>。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>每个特征都由两份信息一起决定</strong></p>
            <p style="color:var(--muted)">双眼皮、酒窝、血型、耳垂的形状，都不是只听一个人的。</p>
          </div>
          <div class="inner-card">
            <p><strong>哪份更明显，就像谁</strong></p>
            <p style="color:var(--muted)">有的特征爸爸那份影响更明显，有的特征妈妈那份更明显，还有的可能像爷爷奶奶。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="孩子的特征由父母双方遗传信息共同决定的示意图">
          <figcaption>爸爸妈妈各给一份遗传信息，两份一起决定孩子的每个特征，所以和家人既像又不像</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">不要<strong>误认为</strong>长得像爸爸的特征就只来自爸爸。每个遗传特征都由父母双方的信息一起决定；也不要<strong>误认为</strong>孩子是把爸爸妈妈的各部分各拼一半。要<strong>区分</strong>更像谁和只来自谁这两件事——两份信息组合起来，才形成了独一无二的你。</p>
        </div>
    ''', tag="概念二"))

    items_html = "\n".join(
        f'          <button class="sort-item" data-kind="{t["kind"]}" data-why="{t["why"]}">{t["t"]}</button>'
        for t in TRAITS
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "我像谁：六个特征，放进三个筐", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一张特征卡片，再点你认为正确的筐。放完六张，看看你会有什么发现。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">待归类的特征</div>
          <div class="sort-bank" id="trait-bank">
{items_html}
          </div>
          <div class="grid grid-3" style="margin-top:14px">
            <div class="sort-bin" data-trait-bin="dad" style="min-height:110px">
              <h4>👨 来自爸爸</h4>
              <div class="bin-body"></div>
            </div>
            <div class="sort-bin" data-trait-bin="mom" style="min-height:110px">
              <h4>👩 来自妈妈</h4>
              <div class="bin-body"></div>
            </div>
            <div class="sort-bin" data-trait-bin="both" style="min-height:110px">
              <h4>🧬 爸爸妈妈都有份</h4>
              <div class="bin-body"></div>
            </div>
          </div>
          <p class="result warn" id="trait-msg" style="margin-top:12px">点一张卡片开始归类。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🗣️</span><div><strong>顺便想一想：</strong>会说哪种方言、会背几首古诗，这些也和遗传有关吗？它们其实是后天学会的，和遗传信息没有关系。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：为什么弟弟的眼睛像妈妈，鼻子却像爸爸", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>小丽的弟弟眼睛像妈妈，鼻子却像爸爸。有人说，弟弟一半像妈妈、一半像爸爸，是这样吗？请说明理由。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看清问题：</strong>问的是长相特征的来源，不是把身体分成两半。</div></div>
          <div class="step"><span class="n">2</span><div><strong>回想来源：</strong>新生命的遗传信息来自爸爸和妈妈双方，每个特征都由两份信息一起决定。</div></div>
          <div class="step"><span class="n">3</span><div><strong>比较结果：</strong>哪一份信息影响更明显，表现出来的样子就更像谁，所以有的地方像妈妈，有的地方像爸爸。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>得出结论：</strong>弟弟身上同时带着爸爸妈妈的遗传信息，他和家人既像又不像，而不是各拼一半。</div></div>
        </div>
        <div class="kid-note"><span class="emoji">🧬</span><div><strong>换个说法：</strong>遗传信息像两封信合在一起读。两封信一起起作用，读出来的你，就是独一无二的。</div></div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：这三个说法错在哪里", TTS["conceptest-1"], [
        {"q": "下面关于人的生命开始的描述，哪一句是正确的？",
         "options": [("人的生命从一个受精卵开始", True),
                     ("人的生命从出生的那一刻开始", False),
                     ("人的生命从会说话的时候开始", False)],
         "explain": "在出生之前，人已经在妈妈身体里生长发育了大约 38 周。<strong>错因提醒：</strong>最常见错误是误认为出生才是生命的起点，把出生和起点搞混了。"},
        {"q": "受精卵能长成一个完整的人，最主要的原因是：",
         "options": [("细胞不断分裂，并且慢慢分化成不同的器官", True),
                     ("细胞不停地吸水变大", False),
                     ("妈妈把身体的一部分变成了他", False)],
         "explain": "数目靠分裂变多，器官靠分化形成，两者一起完成了发育。<strong>错因提醒：</strong>误认为只要细胞变大就行的同学，忽略了细胞分裂和分化这两个关键过程。"},
        {"q": "小华的耳朵形状很像爷爷，这可能吗？",
         "options": [("可能，遗传信息来自父母双方，也可能带着更早一辈的信息", True),
                     ("不可能，只能像爸爸或者妈妈", False),
                     ("可能，因为和爷爷住在一起就会像他", False)],
         "explain": "遗传信息来自父母，其中也带着更早一辈的信息，所以像爷爷奶奶是很常见的。<strong>错因提醒：</strong>把长相随谁误认为由住在一起决定，是常见的错误想法。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：给一年级小朋友讲清楚我从哪里来", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">请用三句话，讲给一年级的小朋友听。写完以后，用下面的清单检查一下自己讲清楚了没有。</p>
        <div class="inner-card">
          <p><strong>我的三句话</strong></p>
          <textarea id="syn-answer" rows="4" placeholder="我从一个……开始。我在妈妈身体里……。我身上带着……，所以我既像爸爸又像妈妈。" style="margin-top:8px"></textarea>
        </div>
        <div class="inner-card" style="margin-top:12px">
          <p><strong>自评清单（点一点，看看自己做到几条）</strong></p>
          <div id="check-list" class="grid" style="margin-top:8px">
''' + "\n".join(f'            <button class="choice" data-check="{i}" style="text-align:left">{c}</button>' for i, c in enumerate(CHECKLIST, 1)) + f'''
          </div>
          <p class="result warn" id="check-out" style="margin-top:12px">还没点任何一条，先看看自己的三句话里有没有说清楚。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💗</span><div><strong>讲完之后想一想：</strong>妈妈孕育你的九个多月里，一直小心地照顾着你。知道了这些，你想对爸爸妈妈说一句什么？也可以<strong>设计</strong>一张小小的讲解卡，把三句话写上去，贴在教室里。</div></div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换个情境，你还能判断吗", TTS["posttest"], [
        {"q": "从受精卵到胎儿，身体里细胞的变化是：",
         "options": [("细胞数目不断增多，并分化出不同的器官", True),
                     ("细胞数目一直不变，只是变大", False),
                     ("细胞会越来越小，最后消失", False)],
         "explain": "发育的过程就是细胞分裂让数目变多，细胞分化让不同器官形成。"},
        {"q": "关于每一个生命的来历，下面哪句话最合适？",
         "options": [("每个人的生命都来之不易，应当珍爱自己和他人的生命", True),
                     ("反正都会长大，不用特别在意", False),
                     ("只有自己的生命最要紧", False)],
         "explain": "从受精卵到出生要经过九个多月，妈妈付出了很多辛苦。懂得生命的来历，就应该尊重和珍惜每一个生命。"},
        {"q": "姐姐和妹妹是双胞胎，可她们的长相还是有细微差别。最合理的原因是：",
         "options": [("她们各自获得的遗传信息组合不完全相同", True),
                     ("她们不是同一个妈妈生的", False),
                     ("长大以后才变得不一样的，出生时完全一样", False)],
         "explain": "即使是双胞胎，各自得到的遗传信息组合也不完全一样，再加上后天环境的影响，长相就会有差别。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话讲清生命的来历", TTS["summary"], f'''
        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>起点</strong>：人的生命从受精卵开始，它是爸爸妈妈的遗传信息结合在一起形成的一个细胞。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>发育</strong>：细胞不断分裂、逐渐分化，长出各种器官，发育成胎儿，大约 38 周后出生。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>遗传</strong>：每个特征都由父母双方的遗传信息一起决定，所以和家人既像又不像。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到你最想问的那个问题：</strong>我是从哪里来的？你是爸爸妈妈的遗传信息结合在一起，从一个细胞开始，一点一点长出来的。这九个多月里，妈妈一直陪着你、照顾你——每一个生命，都来得不容易。</p>
        </div>
        <div class="inner-card">
          <p><strong>讲给同桌听：</strong>请用"受精卵、细胞分裂、38 周、遗传信息"这四个词，说说你从哪里来。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "写出人的生命从什么开始，以及在妈妈身体里大约住多少周才出生。",
            "说出两个由父母双方遗传信息共同决定的特征。",
        ],
        [
            "做一张我和家人的特征小调查：选三个特征（例如眼皮、酒窝、耳垂），写清楚自己更像爸爸还是更像妈妈，再问问家人有什么看法。",
            "用三句话写一段讲解稿，讲给一年级的小朋友听：我是从哪里来的。",
        ],
        [
            "采访妈妈或者家人，记录你出生前后的一件事（例如怀孕时的感受、出生时的体重），写一小段记录，并写下你的感受。",
            "查一查别的动物从受精卵到出生大约需要多少天（例如小鸡、小狗），和我们人类比一比；再画出小生命发育的路线图，把五站标出来。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "sci-e-human-life-origin",
    "node_id": "sci-e-human-life-origin",
    "title": "人的生命从哪里来",
    "name_en": "Where does human life come from?",
    "grade": 6,
    "grade_cn": "六年级",
    "domain": "life-science",
    "domain_cn": "生命科学 · 生命的延续",
    "lesson_type": "concept-inquiry",
    "version": "1.0.0",
    "description": "沿着受精卵到胎儿的发育时间轴，认识人的生命从受精卵开始、经过细胞分裂与分化逐步发育、约 38 周后出生；并通过特征配对理解新生命同时带着父母双方的遗传信息。",
    "tags": ["受精卵", "发育", "细胞分裂", "遗传信息", "珍爱生命"],
    "standard_ref": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念8「生命的延续与进化」学习内容8.3 人的生命是从受精卵开始的——知道人的生命从受精卵开始，经过发育逐渐形成胎儿并出生。",
    "hero_question": "我从哪里来？一个小生命是怎样一点点长成的？",
    "hero_alt": "人的生命早期发育知识结构图：起点、发育过程、遗传信息来自父母双方",
    "hero_caption": "生命的来历 · 从受精卵开始 · 细胞分裂分化，约 38 周后出生 · 遗传信息来自父母双方",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的时间轴和配对游戏都会围着它转。",
    "anchor_choices": [
        {"t": "生命最开始是什么样子？", "d": "想知道受精卵到底是什么", "v": "生命最开始是什么样子"},
        {"t": "我在妈妈身体里住了多久？", "d": "想知道这九个多月怎么长大", "v": "我在妈妈身体里住了多久"},
        {"t": "为什么我既像爸爸又像妈妈？", "d": "想弄清楚长相随谁的道理", "v": "为什么我既像爸爸又像妈妈"},
        {"t": "为什么说生命来之不易？", "d": "想了解妈妈孕育我的过程", "v": "为什么说生命来之不易"},
    ],
    "objectives": [
        "能说出人的生命是从受精卵开始的",
        "能说出受精卵经过细胞分裂和分化逐步发育成胎儿，大约 38 周后出生",
        "能说出新生命同时带着父母双方的遗传信息，所以和家人既像又不像",
        "能体会生命来之不易，懂得珍爱自己和他人的生命",
    ],
    "objectives_plain": [
        "能说出人的生命是从受精卵开始的",
        "能说出受精卵经过细胞分裂和分化逐步发育成胎儿，大约 38 周后出生",
        "能说出新生命同时带着父母双方的遗传信息，所以和家人既像又不像",
        "能体会生命来之不易，懂得珍爱自己和他人的生命",
    ],
    "standards": [
        {"content": "知道人的生命是从受精卵开始的，经过发育逐渐形成胎儿并出生",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念8 生命的延续与进化·学习内容8.3"},
        {"content": "认识到生命的可贵，形成珍爱生命、尊重生命的意识",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》生命教育·态度责任（5～6年级）"},
    ],
    "prereqs": ["sci-e-animal-life-cycle"],
    "prereqs_name": "动物的一生",
    "prereqs_meta": "sci-e-animal-life-cycle",
    "leads_to": ["sci-e-heredity-intro"],
    "next_meta": "sci-e-heredity-intro",
    "section_images": ["assets/sci-e-human-life-origin-fig1.webp", "assets/sci-e-human-life-origin-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "我是从哪里来的？这是每个同学都想过的问题，今天我们一起找答案。",
        "problem-anchor": "先定一个小目标：这节课结束时，你要能说清生命的起点和发育过程。",
        "objectives": "看清四件事：起点是受精卵、怎样发育、多久出生、为什么像家人。",
        "pretest": "凭直觉选就好，错了不扣分——前测帮你先看清自己现在站在哪里。",
        "module-1": "一个细胞能长成一个人，靠的是不断分裂和逐渐分化，大约 38 周后出生。",
        "lab-1": "一站一站地看：受精卵、细胞分裂、安家、器官形成、胎儿。",
        "module-2": "每个特征都由父母双方的信息一起决定，哪份更明显就更像谁。",
        "lab-2": "放完六张你会发现，它们最后都进了同一个筐。",
        "worked-example": "四步走：看清问题、回想来源、比较结果、得出结论。",
        "conceptest-1": "这三道题都埋了高频错误，选完看清每一个解释。",
        "synthesis": "讲给一年级的小朋友听，再用清单检查自己讲清楚了没有。",
        "posttest": "换了细胞分裂、像爷爷和双胞胎的新情境，看看你还能不能判断准确。",
        "summary": "回到最初的问题：你从哪里来？用四句话讲清楚。",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是「生命的延续与进化」在小学段最要紧的一课。学生在生活里早已产生过我从哪里来的疑问，知识树却缺这一层，于是问题被留给了课外。设计上把发育过程做成一条可以亲手拖动的五站时间轴，用中性、简洁的示意图呈现，内容只聚焦三件事：生命的起点是受精卵、经过细胞分裂与分化逐步发育、约 38 周后出生；再用我像谁的配对游戏把遗传信息来自父母双方讲透，最后落到珍爱生命的价值引导。",
    "plan_table": """| 1 | cover | 人的生命从哪里来 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：你从哪里来？ | 起·前测（暴露直觉） |
| 5 | concept | 人的生命从受精卵开始，大约 38 周后出生 | 承·概念一（起点与发育） |
| 6 | interactive | 发育时间轴：从受精卵到胎儿，走一遍 | 承·实验室一（五站拖动） |
| 7 | concept | 你身上带着爸爸妈妈双方的遗传信息 | 承·概念二（遗传信息来源） |
| 8 | interactive | 我像谁：六个特征，放进三个筐 | 承·实验室二（配对与发现） |
| 9 | concept | 例题示范：为什么弟弟的眼睛像妈妈，鼻子却像爸爸 | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：这三个说法错在哪里 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：给一年级小朋友讲清楚我从哪里来 | 合·迁移应用与自评 |
| 12 | quiz | 后测：换个情境，你还能判断吗 | 合·后测 |
| 13 | summary | 小结：三句话讲清生命的来历 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：起点 / 发育过程 / 遗传信息来自父母双方 三栏标注\n- P5 发育时间轴图（已生成）：受精卵→细胞分裂→安家→器官形成→胎儿\n- P7 遗传信息来源图（已生成）：爸爸妈妈各一份信息共同决定孩子的特征\n- 强调：全部人物与胎儿图示均为中性、简洁的插画，不出现任何年龄不当内容\n- 若需补充：不同动物从受精卵到出生的时间对比表",
}
