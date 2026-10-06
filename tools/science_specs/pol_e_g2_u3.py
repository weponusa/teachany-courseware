# -*- coding: utf-8 -*-
"""小学道德与法治 · 我的家乡美（G2）—— 补齐知识树课标空缺节点

学科语气（道德与法治）：情境案例驱动，情感共鸣 + 价值判断；结论落在「应该怎么做、为什么」，
不做道德说教，也不做法条背诵。
二年级落点：从能看见、能摸到的东西入手——家乡的山和水、家乡的物产、家乡话、过节的
老规矩、老桥老屋、从小吃到大的那碗小吃、还有可亲可敬的家乡人。核心动手是「家乡名片」
制作（选元素 → 拼成一张名片）；同时把「家乡的山水好玩，也要注意安全」讲清楚。
插图一律为中性简洁教学示意图，不使用真实人物照片。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g2-u3"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "小朋友，你的家乡在哪里？有的家乡有山有水，清早能看见雾从河面上慢慢飘过去；有的家乡是一大片一大片的稻田，秋天一片金黄；有的家乡就在城里，楼下就是热热闹闹的菜市场。你的家乡是什么样子？今天我们就一起找一找：家乡的山水和物产，家乡的方言、风俗和老建筑，还有家乡的小吃和可亲可敬的家乡人。找齐了，我们一起动手做一张「家乡名片」。",
    "problem-anchor": "开始之前，先选一个你最想弄清楚的问题。是想知道家乡到底美在哪里，还是想知道家乡有哪些好吃的好玩的；是想认识家乡那些了不起的人，还是想看看家乡这些年变了哪些地方。选好了，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出家乡的地形和物产，知道「一方水土养一方人」。第二，能说出家乡的方言、风俗、老建筑和小吃，感受到这就是家乡特有的味道。第三，能说出家乡有哪些可亲可敬的人，从心里敬佩他们。第四，能说出家乡这些年的新变化，并且愿意做一件爱护家乡的小事。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先从家乡的样子说起。家乡的地形，就是家乡「长什么样」：有的地方山多，一层一层叠着；有的地方一马平川，那是平原；有的地方靠着河、靠着湖、靠着海；还有的地方一起一伏，那是丘陵。不同的地形，会长出不同的东西。山里有竹子和茶叶，水边有鱼有虾，平原上是一望无际的稻田和麦田，这些都是家乡的物产。老人常说「一方水土养一方人」，说的就是：家乡的山、家乡的水，养大了家乡的人。",
    "lab-1": "现在请你当一次名片设计师。上面写一写你的家乡叫什么，下面四类元素里，每一类挑一个你最有感觉的，点一点。四类都选好，一张「家乡名片」就做出来了，看看它像不像你心里的家乡。",
    "module-2": "家乡除了山水物产，还有很多只有家乡才有的东西。第一样是方言：家乡话是我们最先学会的话，用家乡话喊一声爷爷奶奶，听起来格外亲。第二样是风俗：过年怎么过、过节吃什么、有什么老规矩，每个地方都不一样。第三样是老建筑：村口的老石桥、巷子里的老屋老墙、镇上的老戏台，它们比我们大得多，站在那里看着一代一代人长大。第四样是家乡的小吃：早上那碗热腾腾的面或者粉，逢年过节才做的糕点，街角那家从小吃到大的小摊，一闻到味道就想起了家。家乡还有可亲可敬的人：天不亮就起来扫街的环卫工人，把老手艺一代一代传下来的爷爷，还有把家乡越建越好的每一个人。这些年家乡也在变化：村里新修了水泥路，镇上有了图书馆，家家户户的日子越过越好。最后要记住一句：家乡的山水好玩，也要注意安全——去水边、去山上玩，一定要跟着大人一起去，不一个人往水里跑。",
    "lab-2": "接下来我们玩一个配对的游戏。上面是八件家乡里的事物，下面是四句话。先点一件，再点它属于哪一句话。配对了会告诉你为什么，配错了也会提醒你再想一想。",
    "worked-example": "我们一起来看看，怎么把家乡介绍给远方的朋友。第一步，想清楚说什么：先说家乡在哪里、家乡长什么样，再说家乡有什么好吃的、有什么老地方。第二步，挑最有特点的说：不用说得太多，挑一两件别的地方没有的，比如一座老桥、一种小吃。第三步，说清楚为什么：老桥为什么值得说？因为它在那儿站了一百多年，爷爷小时候也在桥上玩过。第四步，请对方也来说一说：介绍完，问问朋友的家乡是什么样，两个家乡比一比。这样介绍完，朋友就真的能「看见」你的家乡了。",
    "conceptest-1": "接下来用三个说法考考你，每个说法里都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "下面有八条在家乡可能会有的做法，请你判断一下：哪些是爱护家乡的好做法，放进这一边；哪些需要调整，放进那一边。放好以后，再读一读为什么。",
    "posttest": "最后一轮，换几个新的小情境来考考你。这次会出现用家乡话和奶奶说话、在老家墙上刻字、还有一个人跑去水塘边玩，看看你能不能用上今天学到的办法。",
    "summary": "这节课我们记住四句话。第一句，家乡的地形物产：山、水、平原、丘陵，不同的地方长出不同的物产，一方水土养一方人。第二句，家乡的方言风俗：家乡话、过节的老规矩、老桥老屋，还有那碗从小吃到大的小吃，这就是家乡的味道。第三句，可亲可敬的家乡人：天不亮就扫街的环卫工人、把老手艺传下来的爷爷，都是家乡的宝贝。第四句，家乡新变化：路修好了，图书馆有了，日子越过越好；家乡的山水好玩，也一定要跟着大人一起去，注意安全。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出家乡的地形和物产，再说出家乡的三种小吃或者风俗。第二层能力应用，动手做：回家问一问长辈，家乡以前是什么样子，把听来的故事说给同学听；再动手做一张自己的家乡名片。第三层迁移挑战，选做：找一找家乡的老照片，和现在比一比，写出三条家乡的新变化；再为家乡做一件小事，比如捡一捡垃圾、把家乡的故事讲给外地人听。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 家乡的地形和物产", "lab-1": "动手一 做一张家乡名片", "module-2": "概念二 方言 · 风俗 · 老建筑 · 小吃",
    "lab-2": "动手二 家乡事物配对", "worked-example": "例题讲解 把家乡介绍给远方的朋友", "conceptest-1": "概念测试",
    "synthesis": "综合任务 爱护家乡的好做法 / 要调整的做法", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：家乡名片设计台 —— 四类元素各选一个，拼成一张名片 ──
CARD_CATS = [
    {"id": "land", "n": "① 家乡的地形物产", "opts": [
        "我家门前有一条清清的河",
        "远处是一层一层叠着的山",
        "田里的稻子熟了，金黄金黄",
    ]},
    {"id": "dialect", "n": "② 家乡的方言风俗", "opts": [
        "用家乡话喊一声爷爷奶奶",
        "奶奶教我的家乡童谣",
        "过节时家乡特有的老规矩",
    ]},
    {"id": "old", "n": "③ 家乡的老建筑", "opts": [
        "村口那座走了很多年的老石桥",
        "巷子里的老屋和老墙",
        "镇上的老戏台",
    ]},
    {"id": "food", "n": "④ 家乡的特色小吃", "opts": [
        "早上那碗热腾腾的面或者粉",
        "逢年过节才做的糕点",
        "街角那家从小吃到大的小摊",
    ]},
]

# ── 动手二：八件家乡事物 → 四句话（山和水 / 物产 / 家乡人 / 新变化） ──
MATCH_CATS = [
    {"id": "shanshui", "n": "我爱家乡山和水", "use": "家乡的地形和风景"},
    {"id": "chanwu", "n": "家乡物产养育我", "use": "家乡地里、水里长出来的东西"},
    {"id": "ren", "n": "可亲可敬的家乡人", "use": "为家乡做事的人"},
    {"id": "bianhua", "n": "家乡新变化", "use": "这些年变新了的地方"},
]
MATCH_ITEMS = [
    {"id": "m1", "t": "家门口那条清清的河，夏天能看见小鱼游过", "hid": "shanshui",
     "why": "这是家乡的山和水。河、湖、山、海都是家乡的地形，它们的样子就是家乡的样子。"},
    {"id": "m2", "t": "后山的竹林，风一吹沙沙地响", "hid": "shanshui",
     "why": "这也是家乡的山和水。有山的地方常常有竹林、有茶叶，山养着人也养着草木。"},
    {"id": "m3", "t": "田里的稻子熟了，一片一片地收回来", "hid": "chanwu",
     "why": "这是家乡的物产。稻米是家乡地里长出来的东西，养育着家乡的人。"},
    {"id": "m4", "t": "山上的茶园，采茶的季节满山都是人", "hid": "chanwu",
     "why": "这也是家乡的物产。茶、果子、鱼虾、竹子，都是家乡的水土长出来的。"},
    {"id": "m5", "t": "天还没亮就来扫街的环卫工人", "hid": "ren",
     "why": "这是可亲可敬的家乡人。我们走过的干净街道，是他一大早扫出来的。"},
    {"id": "m6", "t": "把老手艺一代一代传下来的爷爷", "hid": "ren",
     "why": "这也是可亲可敬的家乡人。老手艺能留下来，是因为有人一直在做、一直在教。"},
    {"id": "m7", "t": "村里新修的水泥路，车子能开到家门口", "hid": "bianhua",
     "why": "这是家乡的新变化。路修好了，出门、运东西都方便了。"},
    {"id": "m8", "t": "镇上新建的图书馆，周末可以去看书", "hid": "bianhua",
     "why": "这也是家乡的新变化。家乡不光在长大，还在变得越来越好。"},
]

# ── 综合任务：八条做法，分进两个筐 ──
SORT_ITEMS = [
    {"id": "k1", "t": "把家乡的老照片拍下来，讲给同学听", "bin": "good",
     "why": "家乡的故事要有人讲，才会一直传下去。你很会做这件事。"},
    {"id": "k2", "t": "去家乡的河边、山上玩，跟着大人一起去", "bin": "good",
     "why": "山水好玩，安全第一。跟着大人去，看得开心，家里人也都放心。"},
    {"id": "k3", "t": "参加村里或社区组织的植树、捡垃圾活动", "bin": "good",
     "why": "家乡变干净一点、变绿一点，就是靠这样一件一件小事做出来的。"},
    {"id": "k4", "t": "学着用家乡话，和爷爷奶奶说几句话", "bin": "good",
     "why": "家乡话是我们最先学会的话。用它和长辈说话，老人听着格外亲。"},
    {"id": "k5", "t": "在老家的墙上、桥栏杆上刻下「到此一游」", "bin": "fix",
     "why": "这样可能会把老墙老桥弄坏，别人看了也不舒服。还可以试试：拍照、画下来、写进日记，一样能留下纪念。"},
    {"id": "k6", "t": "把零食袋、饮料瓶丢进家乡的小河里", "bin": "fix",
     "why": "这样可能会让河水变脏，小鱼小虾也活不了。还可以试试：走几步路丢进垃圾桶，或者先装进袋子里带回家。"},
    {"id": "k7", "t": "一个人偷偷跑去村边的水塘里玩水", "bin": "fix",
     "why": "这样可能会非常危险，水塘底下看不清楚，一滑就上不来。还可以试试：想去玩水就告诉大人，跟着大人一起去正规的泳池或者浅水边。"},
    {"id": "k8", "t": "觉得家乡又旧又土，不愿意跟别人提起", "bin": "fix",
     "why": "这样可能会错过家乡很多好东西——老桥、老手艺、老味道都很珍贵。还可以试试：先去问一问长辈，说不定你会发现家乡了不起的地方。"},
]
SORT_BIN = {"good": "爱护家乡的好做法", "fix": "要调整的做法"}

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g2-u3 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 家乡名片设计台：四类元素各选一个 + 写家乡名字 → 实时拼出名片
   3) 家乡事物配对：八件事物 → 四句话
   4) 分进两个筐：爱护家乡的好做法 / 要调整的做法
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

  /* ---------- 2. 家乡名片设计台 ---------- */
  var CATS = __CARDS_JSON__;
  var cardStage = document.getElementById('card-stage');
  if (cardStage) {
    var picked = {};
    var nameEl = document.getElementById('card-name');
    var out1 = document.getElementById('card-out');

    function render1() {
      var done = 0;
      CATS.forEach(function (c) {
        if (picked[c.id] !== undefined) done++;
      });
      document.querySelectorAll('[data-card-cat]').forEach(function (b) {
        var k = b.dataset.cardCat;
        var i = parseInt(b.dataset.cardOpt, 10);
        b.classList.toggle('selected', picked[k] === i);
      });
      document.getElementById('card-score').textContent = '已经选好 ' + done + ' / ' + CATS.length + ' 类';
      var nm = (nameEl && nameEl.value.trim()) || '我的家乡';
      var rows = '';
      CATS.forEach(function (c) {
        var v = picked[c.id] !== undefined ? c.opts[picked[c.id]] : '<span style="color:var(--muted)">还没有选</span>';
        rows += '<div style="margin:6px 0"><strong>' + c.n.replace(/^[①②③④]\s*/, '') + '：</strong>' + v + '</div>';
      });
      var box = document.getElementById('card-preview');
      box.innerHTML =
        '<div style="font-size:20px;font-weight:800;color:var(--link);margin-bottom:4px">我的家乡名片</div>' +
        '<div style="color:var(--muted);font-size:14px;margin-bottom:8px">' + nm + '</div>' +
        rows;
      if (done === CATS.length) {
        out1.className = 'result';
        out1.innerHTML = '<strong>四类都选好了，一张家乡名片就做出来了！</strong>把它读一遍，再问问自己：这张名片上，<strong>哪一样最有家乡的味道</strong>？把这一样圈出来，下面介绍家乡的时候就先讲它。';
      } else {
        out1.className = 'result warn';
        out1.innerHTML = '<strong>先把四类都选一选。</strong>选的时候想一想：家乡还有什么别的地方没有的东西？挑那样的说出来，名片才像你的家乡。';
      }
    }
    document.querySelectorAll('[data-card-cat]').forEach(function (b) {
      b.addEventListener('click', function () {
        picked[b.dataset.cardCat] = parseInt(b.dataset.cardOpt, 10);
        render1();
      });
    });
    if (nameEl) nameEl.addEventListener('input', render1);
    render1();
  }

  /* ---------- 3. 家乡事物配对 ---------- */
  var ITEMS = __MATCH_JSON__;
  var MCATS = __MCATS_JSON__;
  var stage2 = document.getElementById('match-stage');
  if (stage2) {
    var pickedItem = null, solved2 = {};
    var out2 = document.getElementById('match-out');

    function catName(hid) {
      for (var i = 0; i < MCATS.length; i++) { if (MCATS[i].id === hid) return MCATS[i].n; }
      return '';
    }
    function render2() {
      document.querySelectorAll('[data-mi]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.mi === pickedItem);
        b.classList.toggle('done', !!solved2[b.dataset.mi]);
        b.disabled = !!solved2[b.dataset.mi];
      });
      var n = Object.keys(solved2).length;
      document.getElementById('match-score').textContent = '已经配对 ' + n + ' / ' + ITEMS.length + ' 件事物';
      var bank = document.getElementById('match-done');
      bank.innerHTML = '';
      ITEMS.forEach(function (t) {
        if (!solved2[t.id]) return;
        var s = document.createElement('span');
        s.className = 'tag';
        s.textContent = t.t.slice(0, 9) + '… → ' + catName(t.hid);
        bank.appendChild(s);
      });
      if (!bank.innerHTML) {
        bank.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有配对成功的事物。</span>';
      }
    }
    document.querySelectorAll('[data-mi]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (solved2[b.dataset.mi]) return;
        pickedItem = b.dataset.mi;
        var T = null;
        for (var i = 0; i < ITEMS.length; i++) { if (ITEMS[i].id === pickedItem) T = ITEMS[i]; }
        out2.className = 'result warn';
        out2.innerHTML = '<strong>这件家乡事物是：' + T.t + '</strong><br>想一想，它属于下面哪一句话？';
        render2();
      });
    });
    document.querySelectorAll('[data-mc]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pickedItem) {
          out2.className = 'result warn';
          out2.textContent = '先在上面点一件家乡事物，再来选它属于哪一句话。';
          return;
        }
        var T = null;
        for (var i = 0; i < ITEMS.length; i++) { if (ITEMS[i].id === pickedItem) T = ITEMS[i]; }
        if (b.dataset.mc === T.hid) {
          solved2[T.id] = true;
          out2.className = 'result';
          out2.innerHTML = '<strong>配对成功，它属于「' + catName(T.hid) + '」。</strong>' + T.why;
          pickedItem = null;
          if (Object.keys(solved2).length === ITEMS.length) {
            out2.className = 'result';
            out2.innerHTML = '<strong>八件事物全配对成功了！</strong>记一句小口诀：<strong>山和水是家乡的样子，物产养大了家乡的人，家乡人守着家乡，家乡一天天变新。</strong>';
          }
        } else {
          out2.className = 'result warn';
          out2.innerHTML = '<strong>好像不是这一句。</strong>你点的是「' + b.textContent + '」。' +
            '<br><span style="color:var(--muted)">常见错误：容易把「家乡的物产」和「家乡的山水」搞混——先想一想，这件东西是地里、水里长出来的，还是本来就是山、是河？</span>';
        }
        render2();
      });
    });
    render2();
  }

  /* ---------- 4. 分进两个筐 ---------- */
  var SORT = __SORT_JSON__;
  var BINN = __SORTBIN_JSON__;
  var stage3 = document.getElementById('sort-stage');
  if (stage3) {
    var pick3 = null, placed = {};
    var out3 = document.getElementById('sort-out');

    function render3() {
      document.querySelectorAll('[data-item]').forEach(function (b) {
        var k = b.dataset.item;
        b.classList.toggle('selected', k === pick3);
        b.classList.toggle('done', !!placed[k]);
        b.disabled = !!placed[k];
      });
      var n = Object.keys(placed).length;
      document.getElementById('sort-score').textContent = '已经放好 ' + n + ' / ' + SORT.length + ' 条';
      var goodBox = document.getElementById('sort-bin-good');
      var fixBox = document.getElementById('sort-bin-fix');
      goodBox.innerHTML = ''; fixBox.innerHTML = '';
      SORT.forEach(function (it) {
        if (!placed[it.id]) return;
        var s = document.createElement('div');
        s.className = 'tag';
        s.textContent = it.t;
        (it.bin === 'good' ? goodBox : fixBox).appendChild(s);
      });
      if (!goodBox.innerHTML) goodBox.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
      if (!fixBox.innerHTML) fixBox.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
    }
    document.querySelectorAll('[data-item]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (placed[b.dataset.item]) return;
        pick3 = b.dataset.item;
        out3.className = 'result warn';
        out3.innerHTML = '<strong>你选的是：' + b.textContent + '</strong><br>想一想，它是爱护家乡的好做法，还是需要调整的做法？';
        render3();
      });
    });
    document.querySelectorAll('[data-sort-bin]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pick3) {
          out3.className = 'result warn';
          out3.textContent = '先在上面点一条做法，再选筐。';
          return;
        }
        var it = null;
        for (var i = 0; i < SORT.length; i++) { if (SORT[i].id === pick3) it = SORT[i]; }
        if (b.dataset.sortBin === it.bin) {
          placed[it.id] = true;
          out3.className = 'result';
          out3.innerHTML = '<strong>放对了，它属于「' + BINN[it.bin] + '」。</strong>' + it.why;
          pick3 = null;
          if (Object.keys(placed).length === SORT.length) {
            out3.className = 'result';
            out3.innerHTML = '<strong>八条全放对了！</strong>爱护家乡其实很简单：<strong>把家乡的故事讲出来，把家乡的干净留下来，去水边、上山跟着大人走。</strong>';
          }
        } else {
          out3.className = 'result warn';
          out3.innerHTML = '<strong>再想一想这条做法。</strong>' + it.why +
            '<br><span style="color:var(--muted)">常见错误：容易把「反正没人看见」误认为「这样做就没关系」。家乡是大家住的地方，做得好不好，家乡自己知道。</span>';
        }
        render3();
      });
    });
    render3();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__CARDS_JSON__', json.dumps(CARD_CATS, ensure_ascii=False))
             .replace('__MATCH_JSON__', json.dumps(MATCH_ITEMS, ensure_ascii=False))
             .replace('__MCATS_JSON__', json.dumps(MATCH_CATS, ensure_ascii=False))
             .replace('__SORT_JSON__', json.dumps(SORT_ITEMS, ensure_ascii=False))
             .replace('__SORTBIN_JSON__', json.dumps(SORT_BIN, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "「一方水土养一方人」这句话的意思是：",
         "options": [("家乡的山和水，养育了家乡的人", True),
                     ("每个地方的人长得都一样", False),
                     ("水土好不好的事，和人没关系", False)],
         "explain": "山里有竹子、水边有鱼虾、平原上有稻米，不同的水土长出不同的东西，也养大了不同地方的人。"
                    "<strong>错因提醒：</strong>常见错误是误认为「水土」只是风景——它其实是我们吃的、用的、过日子的来源。"},
        {"q": "下面哪一样最能让人一听就知道「这是你的家乡」？",
         "options": [("家乡话、家乡的老桥老屋、只有家乡才有的小吃", True),
                     ("和别人家一样的沙发和电视", False),
                     ("随便哪条马路都能看到的东西", False)],
         "explain": "别的地方也有马路和房子，但家乡话的口音、老桥老屋的样子、小吃的味道，往往是别的地方没有的。"
                    "<strong>错因提醒：</strong>容易误认为「到处都有的东西才是好的」——家乡的特别，恰恰在那些别处没有的东西上。"},
        {"q": "周末你和小伙伴想去家乡的河边玩，应该怎么做？",
         "options": [("先告诉爸爸妈妈，跟着大人一起去", True),
                     ("趁大人不注意，两个人偷偷去", False),
                     ("自己去，反正水看起来很浅", False)],
         "explain": "水边、山上都要有大人陪着才能去。看着浅的水，底下常常有坑、有石头、有水草，很危险。"
                    "<strong>错因提醒：</strong>常见错误是误认为「水浅就没事」——出去玩要跟大人一起，这是一条不能省的规矩。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "家乡的地形和物产：一方水土养一方人", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们每天都住在自己的家乡里（And）；可是问起来「你家乡有什么」，很多同学一时说不出（But）；因为家乡的东西太熟悉，熟了反而不留意。这节课我们就一样一样把它找出来（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">家乡的地形，就是家乡<strong>长什么样</strong>：山、河、湖、海、平原、丘陵。地形不一样，长出来的东西就不一样。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>家乡的地形</strong></p>
            <p style="color:var(--muted)">有的地方山多，一层一层叠着；有的是平原，一马平川；有的靠着河、湖、海；有的是丘陵，一起一伏。</p>
          </div>
          <div class="inner-card">
            <p><strong>家乡的物产</strong></p>
            <p style="color:var(--muted)">山里有竹子和茶叶，水边有鱼有虾，平原上是一望无际的稻田和麦田，果园里还有梨、橘子和苹果。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="家乡的地形与物产示意图：山、河、稻田、果园，附中文标注">
          <figcaption>示意图：家乡的样子——山 · 河 · 稻田 · 果园，不同的地形长出不同的物产（教学示意图）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「一方水土养一方人」说的是风景好看。其实这句话说的是过日子：家乡的水浇出家乡的稻米，家乡的山长出家乡的茶，我们吃的穿的，很多都来自脚下这片土地。</p>
        </div>
        <div class="kid-note"><span class="emoji">⛰️</span><div><strong>记一句小口诀：</strong>山是家乡的骨，水是家乡的血，地里的东西养大了家乡的人。</div></div>
{insight_box([
    {"lens": "看见它", "text": "把家乡的地形和物产画成一张小图：一条河、一座山、一片田、一个果园，这就是家乡的「样子」。"},
    {"lens": "解释它", "text": "为什么不同的地方长出不同的东西？因为有的地方水多、有的地方日照长、有的地方天冷。地不一样，长出来的东西当然不一样。"},
    {"lens": "迁移它", "text": "这套看法到哪里都管用：以后去到别的地方，先看看那里的水土，就能大致猜到那里的人吃什么、做什么。"},
])}
    ''', tag="概念一"))

    card_blocks = []
    for c in CARD_CATS:
        btns = "\n".join(
            f'              <button class="choice" data-card-cat="{c["id"]}" data-card-opt="{i}" style="text-align:center">{o}</button>'
            for i, o in enumerate(c["opts"])
        )
        card_blocks.append(f'''          <div style="margin-top:12px">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">{c["n"]}</div>
            <div class="grid grid-3">
{btns}
            </div>
          </div>''')
    card_html = "\n".join(card_blocks)
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：做一张「我的家乡名片」", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先写下家乡的名字，再从下面四类里<strong>每一类挑一个</strong>，点一点，右边的家乡名片就会一样一样长出来。</p>
        <div class="lab-panel" id="card-stage">
          <label style="display:block;font-weight:700;font-size:14px;margin-bottom:6px">我的家乡（可以写省市县，也可以写村名）
            <input id="card-name" placeholder="例如：湖南 · 湘西 · 小溪村" style="margin-top:8px">
          </label>
{card_html}
          <div class="inner-card" style="margin-top:16px;border:2px solid var(--brand);background:var(--card)">
            <div id="card-preview"><span style="color:var(--muted);font-size:14px">名片还没有做出来，先在上面选一选。</span></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">名片进度</span><span class="v" id="card-score">已经选好 0 / 4 类</span></div>
          </div>
          <p class="result warn" id="card-out" style="margin-top:12px">先把四类都选一选。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🪪</span><div><strong>说给你听：</strong>名片上写的东西不一定是「最有名」的，但要是<strong>你最熟悉的</strong>。你每天路过的那座老桥、奶奶常做的那道小吃，写上去才最像你的家乡。</div></div>
    ''', tag="动手一", bloom="apply"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "方言风俗 · 老建筑 · 小吃 · 家乡的人和变化", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">家乡除了山水物产，还有很多<strong>只有家乡才有</strong>的东西。它们凑在一起，就是家乡的味道。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>方言：</strong>家乡话是我们最先学会的话。用家乡话喊一声爷爷奶奶，老人听着格外亲。</div></div>
          <div class="step"><span class="n">2</span><div><strong>风俗：</strong>过年怎么过、过节吃什么、有哪些老规矩，每个地方都不一样，这就是家乡的过节方式。</div></div>
          <div class="step"><span class="n">3</span><div><strong>老建筑：</strong>村口的老石桥、巷子里的老屋老墙、镇上的老戏台，它们比我们大得多，站在那里看了一代又一代人。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>小吃与家乡人：</strong>早上那碗热腾腾的面或者粉，是从小吃到大的味道；天不亮就扫街的环卫工人、把老手艺传下来的爷爷，都是可亲可敬的家乡人。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="家乡名片元素示意图：方言风俗、老建筑、特色小吃，附中文标注">
          <figcaption>示意图：家乡的名片元素——方言风俗 · 老建筑 · 特色小吃（教学示意图）</figcaption>
        </figure>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>家乡新变化</strong></p>
            <p style="color:var(--muted)">村里新修了水泥路，镇上有了图书馆，家家户户的日子越过越好。家乡在长大，也在变好。</p>
          </div>
          <div class="inner-card">
            <p><strong>玩得开心，也要安全</strong></p>
            <p style="color:var(--muted)">去水边、去山上玩，一定要跟着大人一起去，不一个人往水里跑。看着浅的水，底下常常有坑。</p>
          </div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「老桥老屋又旧又破，没什么用」。其实它们站在那里很多年了，爷爷小时候也在桥上玩过。老东西不是没用，是它们身上有家乡的故事。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "家乡的味道藏在细节里：一句家乡话的口音、过节时桌上那道固定的菜、老墙上被雨水磨出的那道印子。"},
    {"lens": "比较它", "text": "把「到处都有的东西」和「只有家乡才有的东西」放在一起比一比，你就知道该向外地朋友介绍什么了。"},
    {"lens": "迁移它", "text": "以后去到别的地方，可以先用这套眼光看一看：那里的话怎么讲、节怎么过、房子什么样子、小吃什么味道。"},
])}
    ''', tag="概念二"))

    match_btns = "\n".join(
        f'            <button class="choice" data-mi="{t["id"]}" style="text-align:left">{t["t"]}</button>'
        for t in MATCH_ITEMS
    )
    mcat_btns = "\n".join(
        f'            <button class="choice" data-mc="{c["id"]}" style="text-align:center"><strong>{c["n"]}</strong><br><span style="color:var(--muted);font-size:13px">{c["use"]}</span></button>'
        for c in MATCH_CATS
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：家乡事物配对——放回自己的位置", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">上面是八件家乡里的事物，下面是四句话。先点一件事物，再点它属于哪一句话。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 家乡里的这一件事物</div>
          <div class="grid" id="match-stage">
{match_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 它属于哪一句话</div>
          <div class="grid grid-2">
{mcat_btns}
          </div>
          <div class="inner-card" style="margin-top:14px">
            <p><strong>我们配好的家乡</strong></p>
            <div id="match-done" style="display:flex;flex-wrap:wrap;gap:6px"><span style="color:var(--muted);font-size:14px">还没有配对成功的事物。</span></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">配对进度</span><span class="v" id="match-score">已经配对 0 / 8 件事物</span></div>
          </div>
          <p class="result warn" id="match-out" style="margin-top:12px">先在上面点一件家乡事物。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧭</span><div><strong>拿不准就问自己一句：</strong>这件东西是<strong>地里、水里长出来的</strong>，还是<strong>本来就在那儿的山和河</strong>，或者是<strong>人做出来的</strong>？问完这一句，答案就清楚了。</div></div>
    ''', tag="动手二", bloom="analyze"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：把家乡介绍给远方的朋友", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>班上来了一位新同学，他说他从来没见过你家乡的样子，很想知道。你会怎么向他介绍？请你一步一步想清楚。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>想清楚说什么：</strong>先说家乡在哪里、长什么样，再说家乡有什么好吃的、有什么老地方。</div></div>
          <div class="step"><span class="n">2</span><div><strong>挑最有特点的说：</strong>不用说得太多，挑一两件别的地方没有的——一座老桥、一种小吃、一句家乡话。</div></div>
          <div class="step"><span class="n">3</span><div><strong>说清楚为什么：</strong>老桥为什么值得说？因为它在那儿站了一百多年，爷爷小时候也在桥上玩过。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>请对方也来说：</strong>介绍完，问问他的家乡是什么样，两个家乡比一比——你会发现，每个家乡都有自己的好。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「介绍家乡要说得多、说得大」。其实说得再多，不如说清楚一件别人没听过的小事：比如你家门口那棵老树，或者过节时一定要吃的那道菜。</p>
        </div>
        <div class="inner-card">
          <p><strong>说给同桌听：</strong>如果要你用一句话向外地朋友介绍家乡，你会说哪一句？先在心里说一遍，再说给同桌听。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "关于家乡的物产，下面哪个说法是对的？",
         "options": [("物产是家乡的水土长出来的，山里有茶，水边有鱼虾", True),
                     ("物产就是从超市买回来的东西", False),
                     ("只有大城市才有物产", False)],
         "explain": "物产指的是家乡地里、水里长出来的东西：稻米、茶、果子、鱼虾。"
                    "<strong>错因提醒：</strong>常见错误是把「买来的东西」和「长出来的物产」搞混——超市里的东西，很多也是从某个家乡的田里来的。"},
        {"q": "有同学说：「老桥老屋又旧又破，早该拆掉。」你觉得：",
         "options": [("老桥老屋上有家乡的故事，应该保护，也可以修一修", True),
                     ("旧东西一律没有用，全拆了最好", False),
                     ("拆不拆和我没关系", False)],
         "explain": "老桥老屋站在那里很多年，爷爷小时候也在上面玩过，它们是家乡的记忆，可以修、可以用，不一定要拆。"
                    "<strong>错因提醒：</strong>容易误认为「旧的就是没用的」——用处不只看新旧，还要看它身上有没有故事。"},
        {"q": "家乡的河水很清，小鱼游来游去。你是村里的孩子，可以怎么做？",
         "options": [("不往河里丢垃圾，想去玩水就跟着大人一起去", True),
                     ("把喝完的饮料瓶顺手丢进去，反正会漂走", False),
                     ("一个人下水去抓鱼，不用告诉大人", False)],
         "explain": "河是家乡大家共有的。不丢垃圾，水才一直清；想去玩水，跟着大人一起才安全。"
                    "<strong>错因提醒：</strong>有人误认为「水会自己变干净」「水看起来浅就没事」——这两句话都很危险，记住：垃圾带回去，玩水跟大人。"}
    ], tag="概念测试"))

    item_btns = "\n".join(
        f'            <button class="sort-item" data-item="{it["id"]}">{it["t"]}</button>' for it in SORT_ITEMS
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：八条做法，分进两个筐", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一条做法，再点它应该进的筐：<strong>爱护家乡的好做法</strong>放一边，<strong>要调整的做法</strong>放另一边。</p>
        <div class="lab-panel">
          <div class="sort-bank" id="sort-stage">
{item_btns}
          </div>
          <div class="grid grid-2" style="margin-top:14px">
            <button class="choice" data-sort-bin="good" style="text-align:center">爱护家乡的好做法</button>
            <button class="choice" data-sort-bin="fix" style="text-align:center">要调整的做法</button>
          </div>
          <div class="sort-bins">
            <div class="sort-bin" id="sort-bin-good"><h4>爱护家乡的好做法</h4></div>
            <div class="sort-bin" id="sort-bin-fix"><h4>要调整的做法</h4></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">分类进度</span><span class="v" id="sort-score">已经放好 0 / 8 条</span></div>
          </div>
          <p class="result warn" id="sort-out" style="margin-top:12px">先在上面点一条做法。</p>
        </div>
        <div class="inner-card">
          <p><strong>分完之后，想一想：</strong></p>
          <p style="color:var(--muted)">这两边里，有没有哪一条是你以前做过的？把它记下来，再说一说：从明天开始，你打算为家乡做哪一件小事？</p>
          <textarea id="syn-answer" rows="3" placeholder="我以前做过……，从明天开始我想为家乡做……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，做法还在不在", TTS["posttest"], [
        {"q": "奶奶用家乡话喊你吃饭，你听不懂，你会：",
         "options": [("请奶奶再说一遍，跟着学一学这句话怎么说", True),
                     ("说奶奶说的话好难听，不愿意学", False),
                     ("装作没听见，自己吃自己的", False)],
         "explain": "家乡话是我们这里的人最先学会的话。学着说几句，长辈听着最开心，你也多了一样家乡的东西。"
                    "<strong>错因提醒：</strong>常见错误是误认为「家乡话不体面」——每一种话都值得被尊重，家乡话是最亲的那一种。"},
        {"q": "几位同学约着去家乡的老戏台那边玩，那里紧挨着一个水塘。你会：",
         "options": [("大家先回家告诉大人，大人同意了再去，到了水塘边走慢一点", True),
                     ("到了水塘边比谁走得离水更近", False),
                     ("大人不在，正好可以自己下水玩个够", False)],
         "explain": "水边是最容易出事的地方。先告诉大人、走慢一点，玩起来才安心。"
                    "<strong>错因提醒：</strong>有人误认为「人多就安全」——水边不分人多人少，靠得越近越危险。"},
        {"q": "外地朋友问你家乡有什么好，你说不出来。最该做的是：",
         "options": [("回家问问长辈，再自己走一走、看一看，把家乡的好找出来", True),
                     ("直接说「我们家乡没什么好的」", False),
                     ("照着别人的家乡随口编一个", False)],
         "explain": "家乡的好需要自己去找。问长辈、走一走、看一看，你会发现很多以前没留意的东西。"
                    "<strong>错因提醒：</strong>容易误认为「说不出来就是没有」——说不出来，往往只是还没认真看过。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：四句话，讲清我的家乡", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>家乡的地形物产：</strong>山、水、平原、丘陵，不同的水土长出不同的物产——一方水土养一方人。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>家乡的方言风俗：</strong>家乡话、过节的老规矩、老桥老屋，还有那碗从小吃到大的小吃，这就是家乡的味道。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>可亲可敬的家乡人：</strong>天不亮就扫街的环卫工人、把老手艺传下来的爷爷，都是家乡的宝贝。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>家乡新变化：</strong>路修好了，图书馆有了，日子越过越好；山水好玩，也一定要跟着大人一起去，注意安全。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那个问题：</strong>家乡美在哪里？美在山和水，美在方言和小吃，美在老桥老屋，更美在那些一直为家乡做事的人身上。这些加起来，就是「我的家乡美」。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「山水、物产、家乡人」这三个词，说清楚你的家乡好在哪，说给同桌听。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "说出家乡的地形是什么样子，再说出家乡的两三种物产。",
            "说出家乡的一样小吃、一个老地方，并说说它们为什么让你想起家乡。",
        ],
        [
            "回家问一问爷爷奶奶或爸爸妈妈：家乡以前是什么样子？把听来的一个故事说给同学听。",
            "动手做一张自己的家乡名片（可以画，也可以剪贴），把四类元素都放上去。",
        ],
        [
            "找一找家乡的老照片，和现在的样子比一比，写出三条家乡的新变化。",
            "为家乡做一件小事（捡垃圾、参加植树、把家乡的故事讲给外地人听），做完以后说说你的感受。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": ID,
    "node_id": ID,
    "subject": "politics",
    "subject_cn": "道德与法治",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "义务教育道德与法治课程标准（2022年版2025年修订）· 小学",
    "title": "我的家乡美",
    "name_en": "The Beauty of My Hometown",
    "grade": 2,
    "grade_cn": "二年级",
    "domain": "health-safety",
    "domain_cn": "生命安全与健康",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学二年级的道德与法治课：从家乡的地形物产、方言风俗、老建筑、特色小吃入手，一样一样找出「家乡好在哪」；再认识可亲可敬的家乡人和家乡这些年的新变化；最后动手做一张「我的家乡名片」。全课只讲能看见、能说出的具体事物，把价值判断落在「应该怎么做、为什么」上，不做道德说教，也不做法条背诵；同时把「家乡的山水好玩，也要跟着大人一起去」的安全提醒讲清楚。",
    "tags": ["我的家乡美", "家乡地形物产", "方言风俗", "老建筑", "特色小吃", "家乡名片", "二年级"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学——掌握基本安全知识和技能，珍爱生命；感受家乡文化、增强家乡认同。对应统编《道德与法治》二年级上册「我的家乡美」单元：我爱家乡山和水、家乡物产养育我、可亲可敬的家乡人、家乡新变化。",
    "hero_question": "天天住在家乡里，可你知道家乡好在哪吗？",
    "hero_alt": "我的家乡美知识结构图：家乡的山水物产、方言风俗与老建筑、小吃与家乡人 三栏",
    "hero_caption": "我的家乡美：山和水 · 物产 · 方言风俗 · 老建筑 · 特色小吃 · 家乡的人和变化",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "家乡美在哪里？", "d": "山、水、物产，家乡长什么样", "v": "家乡美在哪里"},
        {"t": "家乡有什么好吃、好玩的？", "d": "方言、风俗、老建筑和小吃", "v": "家乡有什么好吃好玩的"},
        {"t": "家乡有哪些了不起的人？", "d": "为家乡做事的人", "v": "家乡有哪些了不起的人"},
        {"t": "家乡这些年变了哪些地方？", "d": "老家和新家的样子比一比", "v": "家乡这些年变了哪些地方"},
    ],
    "objectives": [
        "能说出家乡的地形和物产，知道「一方水土养一方人」",
        "能说出家乡的方言、风俗、老建筑和小吃，感受到这就是家乡特有的味道",
        "能说出家乡有哪些可亲可敬的人，从心里敬佩他们",
        "能说出家乡这些年的新变化，并愿意做一件爱护家乡的小事",
    ],
    "objectives_plain": [
        "能说出家乡的地形和物产，知道「一方水土养一方人」",
        "能说出家乡的方言、风俗、老建筑和小吃，感受到这就是家乡特有的味道",
        "能说出家乡有哪些可亲可敬的人，从心里敬佩他们",
        "能说出家乡这些年的新变化，并愿意做一件爱护家乡的小事",
    ],
    "standards": [
        {"content": "掌握基本安全知识和技能，珍爱生命",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学 生命安全与健康"},
        {"content": "我爱家乡山和水；家乡物产养育我；可亲可敬的家乡人；家乡新变化",
         "source": "统编《道德与法治》二年级上册「我的家乡美」单元"},
    ],
    "prereqs": ["pol-e-g2-u2"],
    "prereqs_name": "我爱我们班",
    "prereqs_meta": "pol-e-g2-u2",
    "leads_to": ["pol-e-g2-u4"],
    "next_meta": "pol-e-g2-u4",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "家乡天天在眼前，可它好在哪？今天把它一样一样找出来。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能用一句话向外地朋友介绍你的家乡。",
        "objectives": "看清四件事：认识家乡的山水物产、找到家乡的味道、认识家乡的人、发现家乡的变化。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "地形是家乡长什么样，物产是水土长出来的东西——一方水土养一方人。",
        "lab-1": "四类元素各挑一个，选完就能看到自己的家乡名片。挑最熟悉的，不必挑最有名的。",
        "module-2": "方言、风俗、老建筑、小吃，还有家乡的人和变化；去水边、上山玩要跟着大人一起。",
        "lab-2": "先点一件家乡事物，再点它属于哪一句。容易把山水和物产搞混，看清楚再点。",
        "worked-example": "四步：说清在哪、挑最有特点的说、说清为什么、请对方也来说。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "八条做法分进「爱护家乡的好做法」和「要调整的做法」，分完读一读为什么。",
        "posttest": "出现了家乡话、老戏台边的水塘、还有说不出家乡好，看看你能不能把办法用上去。",
        "summary": "四句话：家乡的山水物产、家乡的味道、家乡的人、家乡的新变化。",
        "homework": "三层小任务，先做前两层，第三层可以和家人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课正对统编教材二年级上册「我的家乡美」单元，补知识树中「家乡认同」这一空缺。二年级学生的困难不是听不懂「家乡好」，而是说不出「家乡好在哪」——所以全课不喊口号，只做三件能落地的事：一是把家乡的样子说清楚（地形：山、水、平原、丘陵；物产：稻米、茶叶、鱼虾、果子，落点在「一方水土养一方人」）；二是把家乡特有的味道找出来（方言、风俗、老建筑、特色小吃，加上可亲可敬的家乡人与家乡的新变化）；三是动手做出一张「我的家乡名片」。三个互动台子都能真的操作：一个是「家乡名片设计台」，写下家乡名字、从四类元素各挑一个，名片会实时拼出来；一个是「家乡事物配对」，把八件家乡事物配到「我爱家乡山和水 / 家乡物产养育我 / 可亲可敬的家乡人 / 家乡新变化」四句话上；一个是「八条做法分进两个筐」，把做法分进「爱护家乡的好做法 / 要调整的做法」，其中特别放进防溺水的情境，落实课标「掌握基本安全知识和技能，珍爱生命」。全课反馈一律写成「这样可能会……还可以试试……」，不判错、不贴标签；插图均为中性简洁教学示意图，不使用任何真实人物照片。",
    "plan_table": """| 1 | cover | 我的家乡美 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 家乡的地形和物产：一方水土养一方人 | 承·概念一（家乡的样子） |
| 6 | interactive | 动手一：做一张「我的家乡名片」 | 承·名片制作（选元素 → 拼成名片） |
| 7 | concept | 方言风俗 · 老建筑 · 小吃 · 家乡的人和变化 | 承·概念二（家乡的味道 + 安全提醒） |
| 8 | interactive | 动手二：家乡事物配对——放回自己的位置 | 承·配对操作（八件事物 → 四句话） |
| 9 | concept | 例题示范：把家乡介绍给远方的朋友 | 转·重难点突破（分步示范 + 易错点） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：八条做法，分进两个筐 | 合·迁移应用（爱护家乡 / 要调整） |
| 12 | quiz | 后测：换几个新情境，做法还在不在 | 合·后测 |
| 13 | summary | 小结：四句话，讲清我的家乡 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：家乡的山水物产 / 方言风俗与老建筑 / 小吃与家乡人 三栏，附中文标注\n- P5 家乡的样子示意图（已生成）：山、河、稻田、果园，附中文标注\n- P7 家乡名片元素示意图（已生成）：方言风俗、老建筑、特色小吃，附中文标注\n- 三张图均为中性简洁教学示意图，不使用任何真实人物照片或可识别肖像\n- 若需补充：本班学生家乡的照片（需家长授权后使用）、家乡老照片与现状对比图",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
