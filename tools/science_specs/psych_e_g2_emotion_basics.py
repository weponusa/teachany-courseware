# -*- coding: utf-8 -*-
"""小学心理健康 · 情绪体验与自我控制（G2）—— 补齐知识树「情绪调适」空缺

学科语气（心理健康）：温和、不评判、不贴标签；不出现任何临床诊断词汇，不涉及自伤自杀。
二年级落点：先给感觉起名字（体验与表达），再选一个不动手、不伤人的做法（自我控制）。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/psych-e-g2-emotion-basics-fig1.webp'
F2 = './assets/psych-e-g2-emotion-basics-fig2.webp'

TTS = {
    "hero": "小朋友，先想一想：上一次你心里忽然冒出一股气，或者鼻子一下子酸酸的，是什么时候？那时候你的身体有什么感觉？这节课我们不批评任何感觉，只做三件事：给心里的感觉起一个名字，学会用一句话把它说出来，再一起找一找，生气的时候可以做哪些不动手、不伤人的小事。学完你会发现，心里那团乱乱的东西，说出来就轻了一半。",
    "problem-anchor": "开始之前，先选一个你最想知道的事。是想知道心里不舒服的时候身体会有什么信号，还是想知道怎么把感觉说清楚，或者你最想问的是——生气的时候到底能不能动手，再或者你想学几个让自己慢慢平静下来的小办法。选好了，就带着它往下看。",
    "objectives": "这节课有四个小目标。第一，能说出开心、生气、难过、害怕、紧张这些感觉的名字，知道感觉没有对错。第二，能从身体的小信号里发现自己现在是什么感觉，比如心跳变快、手心发热、鼻子发酸。第三，能用一句简单的话把感觉说出来，比如我现在有点生气。第四，生气或者难过的时候，能选一个不动手、不伤人的做法。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先来认识心里的这些感觉。开心、生气、难过、害怕、紧张、委屈、后悔，它们有一个共同的名字，叫情绪。每一种感觉都有自己的名字，把它们叫出名字，心里那团乱乱的东西就会小一点。请你记住一句话：感觉没有对错。每个人遇到同一件事，感觉都可能不一样，这很正常。",
    "lab-1": "现在请你当一次情绪小侦探。下面有五个小情境，点开一个，再从三个感觉里选一个。这里的三个选项都可以选，没有对错。选完我会告诉你，这种感觉常常带着什么样的身体信号，还会教你一句可以说出来的话。",
    "module-2": "感觉是真的，可是做法可以自己选。生气的时候，心里那团火是真的，但火不一定非要烧到别人身上。我们可以走三步小台阶：第一步停一停，第二步说一说，第三步做一件小事。停一停，是让身体先慢下来；说一说，是让别人知道你怎么了；做一件小事，是给自己找一个出口。这三步，就是自我控制本来的样子。",
    "lab-2": "现在请你当一次小主考官。下面有五个情境，每个情境里有三个做法。你选一个，选完会看到一段话：这样做可能会发生什么，还可以试试什么。特别提醒你注意第一个情境：生气的时候，可以直接动手吗？",
    "worked-example": "我们一起来帮小满想一想。课间，小满在桌上搭了很久的积木，被跑过的同学一下子撞倒了，他胸口一下子发烫，很想推那个同学一把。第一步，他先发现自己怎么了：心跳得快，拳头握紧了，这是生气。第二步，他在心里说出这句话：我现在很生气。第三步，他停一停，做了三次慢慢的呼吸，让身体先慢下来。第四步，他说清楚自己要什么：请你看一看路，帮我一起捡起来。四步走完，火小了很多，积木也捡回来了。",
    "conceptest-1": "接下来用三个说法考考你，每一个里面都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件事交给你。请从三栏里各选一条，拼成你自己的情绪小锦囊：停一停、说一说、做一件小事。拼好以后，把它说给同桌听一遍。",
    "posttest": "最后一轮，换三个新的小情境来考考你。这次会出现下雨、妹妹涂花你的画、好朋友没来上学，看看你能不能用上今天的办法。",
    "summary": "这节课我们记住三句话。第一句，心里的感觉都有名字：开心、生气、难过、害怕、紧张，感觉没有对错。第二句，从身体的小信号里能找到感觉：心跳变快、手心发热、鼻子发酸、想哭。第三句，感觉来了就走三步小台阶：停一停、说一说、做一件小事。生气的时候不动手，既是保护别人，也是保护自己。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出五种感觉的名字，再说说生气的时候身体会有什么信号。第二层能力应用，动手做：做一张我的感觉卡，画四种表情，每种表情旁边写一句可以说出来的话。第三层迁移挑战，选做：当一周的感觉小侦探，每天记一次今天的感觉和做过的一件小事。",
    "knowledge-graph": "这张图展示了这节课在心理健康知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 给感觉起个名字", "lab-1": "动手一 情绪小侦探", "module-2": "概念二 感觉没有对错，做法可以选",
    "lab-2": "动手二 我可以做的一件事", "worked-example": "例题讲解 小满的积木", "conceptest-1": "概念测试",
    "synthesis": "综合任务 我的情绪小锦囊", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：情绪小侦探（情境 → 选一个"我现在的感觉"，三个选项都可以选） ──
FEEL_SCENES = [
    {
        "id": "f1",
        "t": "我搭了很久的积木，被跑过的同学碰倒了",
        "opts": [
            {"k": "a", "t": "有点生气",
             "fb": "生气的时候，身体常常会发热，拳头会想握紧，心里像有一小团火。这种感觉在告诉你：我很在意这件事。可以说一句：「我现在有点生气。」"},
            {"k": "b", "t": "有点难过",
             "fb": "难过的时候，鼻子会酸酸的，胸口有点闷。这种感觉在告诉你：这件事让我心里疼了一下。可以说一句：「我有点难过。」"},
            {"k": "c", "t": "又生气又难过",
             "fb": "心里同时有两种感觉，很常见。感觉可以一起待着，不用挑一个去掉另一个。可以说一句：「我又生气又难过。」"},
        ],
    },
    {
        "id": "f2",
        "t": "明天要上台读课文，我排在第一个",
        "opts": [
            {"k": "a", "t": "有点紧张",
             "fb": "紧张的时候，心跳会变快，手心有点潮，肚子里像有小蝴蝶在飞。这是身体在帮你做准备。可以说一句：「我有点紧张。」"},
            {"k": "b", "t": "有点期待，想试一试",
             "fb": "心里痒痒的，像按着一根小弹簧——这是期待。可以说一句：「我有点期待，也有点紧张。」"},
            {"k": "c", "t": "有点想躲开",
             "fb": "想躲一躲，很多人都这样，它不等于胆小。这种感觉在提醒你：这件事对我来说有点难。可以说一句：「这件事我有点怕，能先陪我说说话吗？」"},
        ],
    },
    {
        "id": "f3",
        "t": "好朋友今天和别人一起玩，没有叫我",
        "opts": [
            {"k": "a", "t": "有点委屈",
             "fb": "委屈的时候，喉咙会有点堵，心里像被轻轻压了一下。可以说一句：「今天我有点委屈。」"},
            {"k": "b", "t": "有点生气",
             "fb": "生气的时候会想跺脚、想大声一点。可以说一句：「我今天有点生气，因为没有人叫我一起玩。」"},
            {"k": "c", "t": "有点孤单",
             "fb": "孤单的时候，会觉得周围很热闹，自己却隔了一点距离。可以说一句：「我有点孤单，我想和你一起玩。」"},
        ],
    },
    {
        "id": "f4",
        "t": "我的小豆芽被我不小心碰断了",
        "opts": [
            {"k": "a", "t": "有点难过",
             "fb": "难过的时候，肩膀会往下沉，做什么都提不起劲。可以说一句：「我很舍不得它。」"},
            {"k": "b", "t": "有点后悔，怪自己",
             "fb": "会想「要是我小心一点就好了」——这种感觉叫后悔。可以说一句：「我有点后悔，下次我会小心一点。」"},
            {"k": "c", "t": "有点想哭",
             "fb": "想哭就哭一小会儿也可以，眼泪也是身体在帮你。可以说一句：「我想哭一小会儿。」"},
        ],
    },
    {
        "id": "f5",
        "t": "外面在打雷，我一个人在房间里",
        "opts": [
            {"k": "a", "t": "有点害怕",
             "fb": "害怕的时候，身体会绷紧，会想找个人在身边。这是身体在保护你。可以说一句：「我有点害怕。」"},
            {"k": "b", "t": "心里怦怦跳",
             "fb": "怦怦跳是身体最常见的信号之一。可以说一句：「我心里怦怦跳，想坐一会儿。」"},
            {"k": "c", "t": "不太害怕，只是觉得吵",
             "fb": "也有人对打雷没什么感觉，只是被声音吵到。感觉是很个人的事，没有标准答案，不用和别人一样。"},
        ],
    },
]

# ── 动手二：感觉来了，我可以做的一件事（每个情境一个"更合适"+两个"还可以试试"） ──
ACT_SCENES = [
    {
        "id": "a1",
        "t": "同桌把我的橡皮拿走了，怎么要都不还，我很生气",
        "opts": [
            {"k": "a", "t": "先停一停，做一次慢慢的呼吸，然后大声说：请还给我，不还我就告诉老师", "ok": True,
             "fb": "这样说，既说清了自己的需要，也没有伤到别人。生气的时候，说话的声音可以大一点，但手不动。"},
            {"k": "b", "t": "直接动手推他一下，把橡皮抢回来", "ok": False,
             "fb": "这样可能会让他摔倒，也可能让你自己被批评，事情会变得更大。还可以试试：先停一停，再说清「请还给我」，或者请老师帮忙。"},
            {"k": "c", "t": "什么都不说，自己憋着，回家再说", "ok": False,
             "fb": "憋着可能一下午都不舒服，他也一直不知道你不开心。还可以试试：把感觉说出来——「你这样我很生气」，或者请老师帮个忙。"},
        ],
    },
    {
        "id": "a2",
        "t": "排队的时候，后面的同学一直挤我",
        "opts": [
            {"k": "a", "t": "回头小声说：请别挤我，我站不稳", "ok": True,
             "fb": "一句话就说清了。声音不用大，说清楚就够。"},
            {"k": "b", "t": "转过身也用力挤回去", "ok": False,
             "fb": "这样可能会让队伍乱掉，有人会摔倒。还可以试试：往前站一点，再小声告诉他别挤。"},
            {"k": "c", "t": "不出声，走回教室生一整节课的气", "ok": False,
             "fb": "一个人生气很久，最累的是自己。还可以试试：当下说一句，或者请排队的老师帮忙看一看。"},
        ],
    },
    {
        "id": "a3",
        "t": "我举了好几次手，老师都没有叫我",
        "opts": [
            {"k": "a", "t": "把手举好等一等，下课后跟老师说：我很想回答，下次能叫我吗", "ok": True,
             "fb": "这样既没有打断上课，也让老师知道了你的想法。这是一种很聪明的表达。"},
            {"k": "b", "t": "不等了，站起来大声把答案喊出来", "ok": False,
             "fb": "你想说答案的心情很重要，只是这样可能会打断老师和其他同学。还可以试试：先举手，等老师看到你。"},
            {"k": "c", "t": "生气了，把书合上，不再听了", "ok": False,
             "fb": "这样做，错过的还是自己那一节课。还可以试试：先做一次深呼吸，课后再把想法告诉老师。"},
        ],
    },
    {
        "id": "a4",
        "t": "同学看了我写的字，说：好难看",
        "opts": [
            {"k": "a", "t": "先停一停，说：我不喜欢这句话。然后继续写自己的", "ok": True,
             "fb": "别人说的话可以不同意。说出「我不喜欢」，本身就是一种很有力量的表达。"},
            {"k": "b", "t": "把笔一扔，不写了", "ok": False,
             "fb": "你可能是心里很不舒服。只是不写之后，字还是不会变好看。还可以试试：说一句「我不喜欢这句话」，再挑一个字重写一遍。"},
            {"k": "c", "t": "趁他不注意，也在他的本子上划一笔", "ok": False,
             "fb": "这样可能会让他也很难过，两个人都开心不起来。还可以试试：把这句话说给他听，或者请老师帮忙说说看。"},
        ],
    },
    {
        "id": "a5",
        "t": "听写还没写完，下课铃就响了，我心里很急",
        "opts": [
            {"k": "a", "t": "先放下笔，做三次慢慢的呼吸，再想：下次我写快一点", "ok": True,
             "fb": "急的时候，呼吸是最容易做到的一件事。让身体慢下来，脑子才转得动。"},
            {"k": "b", "t": "把本子揉成一团，塞进书包", "ok": False,
             "fb": "这样做，本子坏了，没写完的题目也还在。还可以试试：先呼吸三次，再问问老师没写完怎么办。"},
            {"k": "c", "t": "一直想着这件事，下一节课也听不进去", "ok": False,
             "fb": "一件事占住了整颗心，后面的事就都挤不进来了。还可以试试：给自己一句话——「这件事下课再想」，然后先听眼前这一节。"},
        ],
    },
]

# ── 综合任务：情绪小锦囊（三栏各选一条，拼成一句话） ──
KIT = {
    "stop": {
        "name": "① 停一停",
        "items": [
            {"id": "s1", "t": "停下手里的动作，做三次慢慢的呼吸"},
            {"id": "s2", "t": "走到教室后面，站一小会儿"},
            {"id": "s3", "t": "在心里数五下：一、二、三、四、五"},
        ],
    },
    "say": {
        "name": "② 说一说",
        "items": [
            {"id": "y1", "t": "「我现在有点生气。」"},
            {"id": "y2", "t": "「我不喜欢你这样说。」"},
            {"id": "y3", "t": "「我想请你帮个忙。」"},
        ],
    },
    "do": {
        "name": "③ 做一件小事",
        "items": [
            {"id": "d1", "t": "喝几口水，去洗一把脸"},
            {"id": "d2", "t": "找一个愿意听我说话的人，说一会儿话"},
            {"id": "d3", "t": "拿一张纸，把心里的事画下来"},
        ],
    },
}

CUSTOM_JS = r"""
/* ============================================================
   psych-e-g2-emotion-basics 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 情绪小侦探：五个情境 × 三个感觉 → 全部接受，只讲身体信号 + 可以说的一句话
   3) 我可以做的一件事：五个情境 × 三个做法 → 温和反馈（这样做可能会……还可以试试……）
   4) 我的情绪小锦囊：三栏各选一条，拼成一句话
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

  /* ---------- 2. 情绪小侦探 ---------- */
  var FEEL = __FEEL_JSON__;
  var feelStage = document.getElementById('feel-stage');
  if (feelStage) {
    var curF = null, doneF = {};
    var outF = document.getElementById('feel-out');
    var scoreF = document.getElementById('feel-score');

    function feelById(id) {
      for (var i = 0; i < FEEL.length; i++) { if (FEEL[i].id === id) return FEEL[i]; }
      return null;
    }
    function renderF() {
      document.querySelectorAll('[data-feel]').forEach(function (b) {
        var k = b.dataset.feel;
        b.classList.toggle('selected', k === curF);
        b.classList.toggle('done', !!doneF[k]);
      });
      scoreF.textContent = '已经聊过 ' + Object.keys(doneF).length + ' / ' + FEEL.length + ' 个情境';
    }
    function paintFeelOpts() {
      var box = document.getElementById('feel-opts');
      box.innerHTML = '';
      if (!curF) return;
      var S = feelById(curF);
      if (!S) return;
      S.opts.forEach(function (o) {
        var b = document.createElement('button');
        b.className = 'choice';
        b.style.textAlign = 'left';
        b.textContent = '我感觉：' + o.t;
        b.addEventListener('click', function () {
          doneF[curF] = true;
          outF.className = 'result';
          outF.innerHTML = '<strong>「' + o.t + '」也是一种很好的回答。</strong>' + o.fb;
          renderF();
          paintFeelOpts();
        });
        box.appendChild(b);
      });
    }
    document.querySelectorAll('[data-feel]').forEach(function (b) {
      b.addEventListener('click', function () {
        curF = b.dataset.feel;
        var S = feelById(curF);
        if (doneF[curF]) {
          outF.className = 'result';
          outF.innerHTML = '<strong>这个情境已经聊过啦。</strong>你上次选的感觉也很好，换个感觉再选一次也可以，感觉本来就可以有很多种。';
        } else {
          outF.className = 'result warn';
          outF.innerHTML = '<strong>你遇到的是：' + S.t + '</strong><br>下面三个感觉都可以选，先看一看，哪个最像你现在的心情？';
        }
        renderF();
        paintFeelOpts();
      });
    });
    renderF();
  }

  /* ---------- 3. 我可以做的一件事 ---------- */
  var ACT = __ACT_JSON__;
  var actStage = document.getElementById('act-stage');
  if (actStage) {
    var curA = null, doneA = {};
    var outA = document.getElementById('act-out');
    var scoreA = document.getElementById('act-score');

    function actById(id) {
      for (var i = 0; i < ACT.length; i++) { if (ACT[i].id === id) return ACT[i]; }
      return null;
    }
    function renderA() {
      document.querySelectorAll('[data-act]').forEach(function (b) {
        var k = b.dataset.act;
        b.classList.toggle('selected', k === curA);
        b.classList.toggle('correct', !!doneA[k]);
        b.classList.toggle('done', !!doneA[k]);
      });
      scoreA.textContent = '已经想过 ' + Object.keys(doneA).length + ' / ' + ACT.length + ' 个情境';
    }
    function paintActOpts() {
      var box = document.getElementById('act-opts');
      box.innerHTML = '';
      if (!curA) return;
      var S = actById(curA);
      if (!S) return;
      S.opts.forEach(function (o) {
        var b = document.createElement('button');
        b.className = 'choice' + (doneA[curA] && o.ok ? ' correct' : '');
        b.style.textAlign = 'left';
        b.textContent = o.t;
        b.addEventListener('click', function () {
          if (doneA[curA]) return;
          if (o.ok) {
            doneA[curA] = true;
            outA.className = 'result';
            outA.innerHTML = '<strong>这个做法挺稳当。</strong>' + o.fb;
          } else {
            outA.className = 'result warn';
            outA.innerHTML = '<strong>这样做也可以理解，我们看看会发生什么。</strong>' + o.fb;
          }
          renderA();
          paintActOpts();
        });
        box.appendChild(b);
      });
    }
    document.querySelectorAll('[data-act]').forEach(function (b) {
      b.addEventListener('click', function () {
        curA = b.dataset.act;
        var S = actById(curA);
        if (doneA[curA]) {
          outA.className = 'result';
          outA.innerHTML = '<strong>这件事已经想过啦。</strong>你上次选的做法很稳当，记住它就好。';
        } else {
          outA.className = 'result warn';
          outA.innerHTML = '<strong>你遇到的是：' + S.t + '</strong><br>下面有三个做法，你选一个试试看。';
        }
        renderA();
        paintActOpts();
      });
    });
    renderA();
  }

  /* ---------- 4. 我的情绪小锦囊 ---------- */
  var KIT = __KIT_JSON__;
  var kitStage = document.getElementById('kit-stage');
  if (kitStage) {
    var chosen = {}, order = ['stop', 'say', 'do'];
    var outK = document.getElementById('kit-out');

    function textOf(col, id) {
      var arr = KIT[col].items;
      for (var i = 0; i < arr.length; i++) { if (arr[i].id === id) return arr[i].t; }
      return '';
    }
    function renderK() {
      Object.keys(KIT).forEach(function (col) {
        document.querySelectorAll('[data-kit="' + col + '"]').forEach(function (b) {
          b.classList.toggle('selected', chosen[col] === b.dataset.kitId);
        });
        var slot = document.getElementById('kit-pick-' + col);
        if (slot) {
          slot.textContent = chosen[col] ? textOf(col, chosen[col]) : '还没有选';
          slot.style.color = chosen[col] ? 'var(--text)' : 'var(--muted)';
        }
      });
      var n = order.filter(function (c) { return chosen[c]; }).length;
      document.getElementById('kit-score').textContent = '锦囊已经放进 ' + n + ' / 3 条';
      if (n === 3) {
        outK.className = 'result';
        outK.innerHTML = '<strong>你的情绪小锦囊拼好了：</strong>感觉来了的时候，我先' + textOf('stop', chosen.stop) +
          '，再说' + textOf('say', chosen.say) + '，然后' + textOf('do', chosen.do) + '。<br>' +
          '<span style="color:var(--muted)">把这句话念给同桌听一遍，念出来，它就真的属于你了。</span>';
      } else {
        outK.className = 'result warn';
        outK.textContent = '三栏各选一条，锦囊就拼好了。';
      }
    }
    Object.keys(KIT).forEach(function (col) {
      document.querySelectorAll('[data-kit="' + col + '"]').forEach(function (b) {
        b.addEventListener('click', function () {
          chosen[col] = b.dataset.kitId;
          renderK();
        });
      });
    });
    renderK();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__FEEL_JSON__', json.dumps(FEEL_SCENES, ensure_ascii=False))
             .replace('__ACT_JSON__', json.dumps(ACT_SCENES, ensure_ascii=False))
             .replace('__KIT_JSON__', json.dumps(KIT, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "下面哪一句话说得对？",
         "options": [("每种感觉都有名字，感觉没有对错", True),
                     ("生气是不好的，小朋友不应该生气", False),
                     ("难过的时候，最好别让别人看出来", False)],
         "explain": "开心、生气、难过、害怕、紧张，都只是感觉的名字，感觉本身没有对错。"
                    "<strong>错因提醒：</strong>常见错误是把「感觉」和「做法」搞混了——需要挑一挑的是做法，不是感觉。"},
        {"q": "小明很生气，下面哪个做法更合适？",
         "options": [("先停一停做三次呼吸，再说出「我很生气」", True),
                     ("直接动手推他一下", False),
                     ("什么也不说，自己憋一整天", False)],
         "explain": "停一停让身体慢下来，说一说让别人知道你怎么了。"
                    "<strong>错因提醒：</strong>有人误认为动手最快解决问题，其实事情常常会变得更大；也有人误认为憋着就是控制得好，可是憋太久，身体会更难受。"},
        {"q": "心里的感觉一下子说不出来，可以先做什么？",
         "options": [("先看看身体有什么信号：心跳快不快、手心热不热", True),
                     ("假装什么也没有发生", False),
                     ("把这件事放到一边，过几天就忘了", False)],
         "explain": "身体常常比嘴巴先知道：心跳变快、手心发热、鼻子发酸，都是线索。"
                    "<strong>错因提醒：</strong>容易误认为「说不出来就是没事」——先看身体，再给感觉起名字，慢慢就说得出来了。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "给感觉起个名字，心就不那么乱", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">一年级的时候，我们已经知道心里不舒服可以说给老师听（And）；可是有时候，我们只感觉到「心里乱乱的」，说不清到底是哪一种（But）；所以这节课先学最要紧的一件事——给感觉起名字（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">心里的感觉有一个共同的名字，叫<strong>情绪</strong>。开心、生气、难过、害怕、紧张、委屈、后悔，每一种都有自己的名字。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>身体会先告诉你</strong></p>
            <p style="color:var(--muted)">心跳变快、手心发热、鼻子发酸、肩膀绷紧、喉咙发堵——这些都是感觉的线索。</p>
          </div>
          <div class="inner-card">
            <p><strong>叫出名字，就轻一点</strong></p>
            <p style="color:var(--muted)">把感觉叫出名字，心里那团乱乱的东西就小了一点。能说出来，就不用一个人扛着。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="四种常见感觉的简单表情插画与对应的身体信号标注">
          <figcaption>示意图：开心、生气、难过、紧张——每种感觉都有自己的名字，身体也会给出线索（教学示意图，人物为中性简洁插画）</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">💛</span><div><strong>一句要紧的话：</strong>感觉没有对错。同一件事，有人生气，有人难过，有人没什么感觉，这都很正常。</div></div>
{insight_box([
    {"lens": "看见它", "text": "心里的感觉看不见，可身体会替它说话：手心会热、心跳会快、鼻子会酸。先看见身体，就看见了感觉。"},
    {"lens": "解释它", "text": "为什么叫出名字就轻松一点？因为说不清的时候最难受，像一团打了结的线；起了名字，就知道自己遇到的是什么了。"},
    {"lens": "迁移它", "text": "这个办法到哪里都能用：在家里、在医院、在陌生的地方，先看看身体的感觉，再给感觉起个名字。"},
])}
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>先看身体信号，再给感觉起名字——<strong>我叫得出它，它就小一半。</strong></div></div>
    ''', tag="概念一"))

    feel_btns = "\n".join(
        f'            <button class="choice" data-feel="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in FEEL_SCENES
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：情绪小侦探，给这件事配一个感觉", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一件小事，再从三个感觉里选一个。<strong>三个都可以选，没有对错</strong>；选完会告诉你这种感觉常常带着什么身体信号。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 我遇到的一件小事</div>
          <div class="grid" id="feel-stage">
{feel_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 我现在的感觉是</div>
          <div class="grid" id="feel-opts">
            <span style="color:var(--muted);font-size:14px">先在上面点一件小事，这里就会出现三个感觉。</span>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">聊过几个情境</span><span class="v" id="feel-score">已经聊过 0 / 5 个情境</span></div>
          </div>
          <p class="result warn" id="feel-out" style="margin-top:12px">先点一件你今天可能遇到的小事。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>小侦探的秘密：</strong>这里不会有「选错」的提醒。感觉是你自己的，你说是哪一种，就是哪一种。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "感觉没有对错，做法可以自己选", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">生气的时候，心里那团火是真的。可火不一定非要烧到别人身上——<strong>感觉要留下，做法可以换</strong>。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>停一停：</strong>把手上的动作停下来，做三次慢慢的呼吸。让身体先慢下来，脑子才转得动。</div></div>
          <div class="step"><span class="n">2</span><div><strong>说一说：</strong>用一句话告诉别人你怎么了——「我现在有点生气」「我不喜欢你这样说」。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>做一件小事：</strong>喝几口水、洗一把脸、画一张画、找人待一会儿，给自己找一个出口。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="情绪三步小台阶示意图：停一停、说一说、做一件小事，附中文标注">
          <figcaption>示意图：感觉来了就走三步小台阶——停一停、说一说、做一件小事（教学示意图，人物为中性简洁插画）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「生气的时候动手，最快把事解决掉」。其实手一动，事情常常一下子变大，两个人都会受伤、都会被批评。<strong>生气的时候，手可以不动</strong>——声音可以说大一点，话可以说清楚，但手放下来。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>手放下来，话说出来——<strong>停一停，说一说，做一件小事。</strong></div></div>
{insight_box([
    {"lens": "拆开它", "text": "「生气」拆开看是两件事：一件是心里那团火（感觉），一件是接下来要做什么（做法）。火不用道歉，做法可以挑。"},
    {"lens": "比较它", "text": "同样很生气，一个同学推了人，一个同学先呼吸再说出来——感觉一样大，结果很不一样。不一样的地方就在做法上。"},
    {"lens": "迁移它", "text": "在家里和弟弟妹妹抢玩具、在操场上被人撞到，都能走这三步。三步在哪里都好用。"},
])}
    ''', tag="概念二"))

    act_btns = "\n".join(
        f'            <button class="choice" data-act="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in ACT_SCENES
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：感觉来了，我可以做的一件事", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一个情境，再从三个做法里选一个。<strong>选得不太合适也不会说你错</strong>，只会告诉你：这样做可能会发生什么，还可以试试什么。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 我遇到的一件事</div>
          <div class="grid" id="act-stage">
{act_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 我可以做的一件事</div>
          <div class="grid" id="act-opts">
            <span style="color:var(--muted);font-size:14px">先在上面点一件事，这里就会出现三个做法。</span>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">想过几个情境</span><span class="v" id="act-score">已经想过 0 / 5 个情境</span></div>
          </div>
          <p class="result warn" id="act-out" style="margin-top:12px">先点一个你今天可能遇到的情境。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💛</span><div><strong>第一个情境请一定试一试：</strong>同桌拿走你的橡皮，怎么要都不还，你很生气——这时候，可以直接动手吗？</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小满的积木被撞倒了", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>课间，小满搭了很久的积木被跑过的同学撞倒了。他胸口发烫，很想推那个同学一把。请你陪他走四步。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>发现自己怎么了：</strong>心跳得快，拳头握紧了，肩膀也绷起来——这是生气。先承认它，不用假装没有。</div></div>
          <div class="step"><span class="n">2</span><div><strong>在心里说出这句话：</strong>「我现在很生气。」叫出名字，那团火就小一点。</div></div>
          <div class="step"><span class="n">3</span><div><strong>停一停：</strong>把手放下来，做三次慢慢的呼吸，让身体先慢下来。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>说清楚要什么：</strong>「请你看一看路，帮我一起捡起来。」说完，火小了很多，积木也捡回来了。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「生气就要马上还回去，不然显得好欺负」。小满这四步里，一步也没有忍气吞声——他停下来了，也说清楚了。真正的力量，不在推那一下，而在能把自己的话说出来。</p>
        </div>
        <div class="inner-card">
          <p><strong>说给同桌听：</strong>小满这四步里，哪一步你自己已经做到了？哪一步还想再练一练？</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "下面哪句话说得对？",
         "options": [("感觉没有对错，要看的是接下来怎么做", True),
                     ("会生气的小朋友，不是好孩子", False),
                     ("心里难过的时候，最好一个人躲起来", False)],
         "explain": "每一种感觉都有自己的名字和用处，感觉不是好坏的分数。"
                    "<strong>错因提醒：</strong>常见错误是给感觉贴标签，把「有感觉」当成「做得不好」——要挑一挑的是做法，不是感觉。"},
        {"q": "很生气的时候，下面哪个做法更合适？",
         "options": [("先停下来做几次慢慢呼吸，再大声说清楚「请还给我」", True),
                     ("不管那么多，先动手推他一下", False),
                     ("一句话也不说，自己憋着", False)],
         "explain": "停一停是给身体一点时间，说一说能让别人知道你怎么了；声音可以大，手不动。"
                    "<strong>错因提醒：</strong>前一个想法是误认为动手最省事，后一个想法是误认为憋住就是控制得好——憋太久，身体会更难受。"},
        {"q": "感觉自己慢慢平静下来之后，最好再做一件事，是：",
         "options": [("把刚才的事说给一个愿意听的人", True),
                     ("装作什么都没发生过，不再提起", False),
                     ("记着这件事，下次找机会还回去", False)],
         "explain": "说出来，事情才算真的过去，别人也知道下次该怎么做。"
                    "<strong>错因提醒：</strong>不要把「不说了」当成「事情过去了」——闷在心里的事，常常会再冒出来一次。"}
    ], tag="概念测试"))

    kit_blocks = []
    for col in ("stop", "say", "do"):
        btns = "\n".join(
            f'              <button class="choice" data-kit="{col}" data-kit-id="{it["id"]}" style="text-align:left">{it["t"]}</button>'
            for it in KIT[col]["items"]
        )
        kit_blocks.append(f'''          <div class="inner-card">
            <p><strong>{KIT[col]["name"]}</strong>　<span style="color:var(--muted);font-size:13px">已选：</span><span id="kit-pick-{col}" style="color:var(--muted)">还没有选</span></p>
            <div class="grid" style="margin-top:8px">
{btns}
            </div>
          </div>''')
    kit_html = "\n".join(kit_blocks)
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：拼一个属于你的情绪小锦囊", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">三栏里各选一条，拼成一句话。这句话就是你的<strong>情绪小锦囊</strong>，下次感觉来了，照着它走就行。</p>
        <div class="lab-panel" id="kit-stage">
{kit_html}
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">锦囊进度</span><span class="v" id="kit-score">锦囊已经放进 0 / 3 条</span></div>
          </div>
          <p class="result warn" id="kit-out" style="margin-top:12px">三栏各选一条，锦囊就拼好了。</p>
        </div>
        <div class="inner-card">
          <p><strong>把它变成你自己的话：</strong></p>
          <p style="color:var(--muted)">想一想，你最常遇到的是哪一件事？把上面选好的三条，写成你自己的句子。</p>
          <textarea id="syn-answer" rows="3" placeholder="我遇到……的时候，我先……，再说……，然后……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换三个新情境，办法还在不在", TTS["posttest"], [
        {"q": "妈妈答应带我去公园，出门前忽然下雨，去不成了，我心里有点难过。下面哪个做法更合适？",
         "options": [("说出「我有点失望」，再问问能不能改到明天", True),
                     ("把伞扔在地上", False),
                     ("一个人回房间，一整天都不理妈妈", False)],
         "explain": "把失望说出来，事情还有商量的余地；说清楚之后，心里也会松一点。"
                    "<strong>错因提醒：</strong>常见错误是把「心里不舒服」变成「让对方也不舒服」——扔东西和不说话，都只会让两个人都更难受。"},
        {"q": "妹妹把我的画涂花了，我很想发火。下面哪个做法更合适？",
         "options": [("先去洗把脸，回来告诉妹妹「我不喜欢你这样做」", True),
                     ("把她的画笔藏起来，让她也难过", False),
                     ("大声吼她一顿，吼到她不说话", False)],
         "explain": "先把身体安顿好，再说清楚自己的不喜欢，妹妹才知道以后不能这样做。"
                    "<strong>错因提醒：</strong>有人误认为「她也难受一次才算公平」，可是两个人都不高兴，事情还是没解决。"},
        {"q": "我最好的朋友今天没来上学，老师说她生病了，我心里有点担心。下面哪个做法更合适？",
         "options": [("请老师帮忙带句话，或者给她画一张小卡片", True),
                     ("一直想「是不是我做错了什么」", False),
                     ("什么也不做，装作不担心", False)],
         "explain": "担心别人的时候，做一件小事，比一直想更有用。"
                    "<strong>错因提醒：</strong>不要在别人不说话的时候，就以为是自己哪里做错了——想不通的时候，直接问一问，会更清楚。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，讲清情绪这件事", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>给感觉起名字：</strong>开心、生气、难过、害怕、紧张——感觉没有对错。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>从身体找线索：</strong>心跳变快、手心发热、鼻子发酸、想哭，都是感觉在说话。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>走三步小台阶：</strong>停一停、说一说、做一件小事。生气的时候手不动。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>还要记牢一件事：</strong>有感觉，是一件很自然的事，你一点也不奇怪。心里的事情如果一直很重、一直放不下，说给爸爸妈妈或者老师说一听，是很聪明的做法。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「感觉、名字、做法」这三个词，说清楚你上一次生气的经过。</p>
          <p style="color:var(--muted)">再动一动手：<strong>画一画</strong>你的三步小台阶，在每一级台阶上写一个你自己做得到的小动作。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "说出五种感觉的名字，再说说生气的时候身体会有什么信号。",
            "用一句话说出今天的一种感觉，说给家里人听。",
        ],
        [
            "做一张「我的感觉卡」：画四种表情，每种表情旁边写一句可以说出来的话。",
            "把「停一停、说一说、做一件小事」三步写在纸上，贴在书桌前。",
        ],
        [
            "当一周的「感觉小侦探」：每天记一次今天的感觉，和当时做过的一件小事。",
            "和同桌一起想一想：我们班的「平静角」可以放些什么？写两条建议。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "psych-e-g2-emotion-basics",
    "node_id": "psych-e-g2-emotion-basics",
    "subject": "psychology",
    "subject_cn": "心理健康",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "中小学心理健康教育指导纲要（2012年修订）/ 教育部相关要求 · 小学",
    "title": "情绪体验与自我控制",
    "name_en": "Feeling and Naming Emotions: A First Step to Self-Control",
    "grade": 2,
    "grade_cn": "二年级",
    "domain": "emotion-regulation",
    "domain_cn": "情绪调适",
    "lesson_type": "workshop",
    "version": "1.0.0",
    "description": "面向小学二年级的情绪调适课：先给心里的感觉起名字（开心、生气、难过、害怕、紧张），学会从身体信号里发现感觉、用一句话把感觉说出来；再走「停一停—说一说—做一件小事」三步小台阶，学会在生气时不动手、不伤人地表达自己。全课不评价、不贴标签，两个互动台子分别做「情境→我现在的感觉」和「情境→我可以做的一件事」。",
    "tags": ["情绪体验", "情绪表达", "自我控制", "二年级", "情绪调适"],
    "standard_ref": "《中小学心理健康教育指导纲要（2012年修订）· 小学低年级》情绪调适——初步学会体验情绪并表达自己的情绪；使学生有安全感和归属感，初步学会自我控制。",
    "hero_question": "心里忽然冒出一股气，或者鼻子一下子酸酸的，这时候可以怎么办？",
    "hero_alt": "情绪体验与自我控制知识结构图：认识感觉、说出感觉、选择做法 三栏",
    "hero_caption": "情绪体验与自我控制：给感觉起名字 · 用一句话说出来 · 生气时不动手，走三步小台阶",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "心里不舒服的时候，身体会有什么信号？", "d": "心跳、手心、鼻子，都在替我说话", "v": "心里不舒服的时候身体会有什么信号"},
        {"t": "怎么把感觉说出来，别人才听得懂？", "d": "想学一句可以说出来的话", "v": "怎么把感觉说出来别人才听得懂"},
        {"t": "生气的时候，可以直接动手吗？", "d": "这股火到底该怎么办", "v": "生气的时候可以直接动手吗"},
        {"t": "有没有让自己慢慢平静下来的小办法？", "d": "想学几个马上能做的小动作", "v": "有没有让自己慢慢平静下来的小办法"},
    ],
    "objectives": [
        "能说出开心、生气、难过、害怕、紧张等感觉的名字，知道感觉没有对错",
        "能从身体的信号里发现自己现在的感觉，例如心跳变快、手心发热、鼻子发酸",
        "能用一句简单的话把感觉说出来，例如「我现在有点生气」",
        "生气或难过的时候，能选一个不动手、不伤人的做法，让自己慢慢平静下来",
    ],
    "objectives_plain": [
        "能说出开心、生气、难过、害怕、紧张等感觉的名字，知道感觉没有对错",
        "能从身体的信号里发现自己现在的感觉，例如心跳变快、手心发热、鼻子发酸",
        "能用一句简单的话把感觉说出来，例如「我现在有点生气」",
        "生气或难过的时候，能选一个不动手、不伤人的做法，让自己慢慢平静下来",
    ],
    "standards": [
        {"content": "初步学会体验情绪并表达自己的情绪",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学低年级 · 情绪调适"},
        {"content": "使学生有安全感和归属感，初步学会自我控制",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学低年级 · 情绪调适"},
    ],
    "prereqs": ["psych-e-g2-self-confidence"],
    "prereqs_name": "自信与集体归属感",
    "prereqs_meta": "psych-e-g2-self-confidence",
    "leads_to": ["psych-e-g3-self-know"],
    "next_meta": "psych-e-g3-self-know",
    "section_images": ["assets/psych-e-g2-emotion-basics-fig1.webp", "assets/psych-e-g2-emotion-basics-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "心里冒出气、鼻子发酸的时候，先别急着怪自己——这节课教你把感觉说出来。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能说出自己的感觉，还能选一个不动手的做法。",
        "objectives": "看清四件事：说出感觉的名字、从身体找线索、用一句话表达、选一个不伤人的做法。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "感觉都有名字：开心、生气、难过、害怕、紧张。叫得出名字，它就小一半。",
        "lab-1": "三个感觉都可以选，没有对错。选完看看身体信号，再学一句可以说出来的话。",
        "module-2": "感觉是真的，做法可以选：停一停、说一说、做一件小事。手放下来，话说出来。",
        "lab-2": "特别注意第一个情境：同桌拿走你的橡皮，你很生气——这时候可以直接动手吗？",
        "worked-example": "小满四步：发现自己怎么了、说出「我很生气」、停一停呼吸、说清楚要什么。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "三栏各选一条，拼成你自己的情绪小锦囊，再念给同桌听一遍。",
        "posttest": "出现了下雨、妹妹涂花你的画、好朋友生病，看看你能不能用上今天的办法。",
        "summary": "三句话：给感觉起名字、从身体找线索、走三步小台阶。",
        "homework": "三层小任务，先做前两层，第三层可以请家里人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先帮你找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学心理健康「情绪调适」在二年级的空缺，正对课标「初步学会体验情绪并表达自己的情绪」「有安全感和归属感，初步学会自我控制」。二年级学生的难点不在理解情绪这个词，而在：①不知道心里那团东西叫什么；②知道生气却只有动手或憋着两种做法。所以全课只做两件能落地的事——先给感觉起名字（体验与表达），再走「停一停 / 说一说 / 做一件小事」三步小台阶（自我控制）。两个互动台子都能真的操作：一个是「情绪小侦探」，五个生活情境各配三个感觉选项，三个都可以选、不判对错，选完只讲身体信号和一句可以说出来的话；一个是「我可以做的一件事」，五个情境各配三个做法，错误反馈一律写成「这样可能会……，还可以试试……」，第一个情境专门处理边界问题——生气的时候可以直接动手吗。综合任务把三条做法拼成个人化的「情绪小锦囊」。插图一律为中性简洁的教学插画，不使用真实儿童照片风格人像；全课不出现任何临床诊断词汇，不贴标签、不评判。",
    "plan_table": """| 1 | cover | 情绪体验与自我控制 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 给感觉起个名字，心就不那么乱 | 承·概念一（体验与表达） |
| 6 | interactive | 动手一：情绪小侦探，给这件事配一个感觉 | 承·感受识别（三个选项都不判错） |
| 7 | concept | 感觉没有对错，做法可以自己选 | 承·概念二（三步小台阶与边界） |
| 8 | interactive | 动手二：感觉来了，我可以做的一件事 | 承·做法选择（温和反馈 + 生气不动手） |
| 9 | concept | 例题示范：小满的积木被撞倒了 | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：拼一个属于你的情绪小锦囊 | 合·迁移应用（三栏拼句） |
| 12 | quiz | 后测：换三个新情境，办法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，讲清情绪这件事 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：认识感觉 / 说出感觉 / 选择做法 三栏\n- P5 四种感觉与身体信号示意图（已生成）：开心、生气、难过、紧张，附中文标注\n- P7 情绪三步小台阶示意图（已生成）：停一停、说一说、做一件小事，附中文标注\n- 三张图均为中性简洁教学插画，人物只用简单图形，不使用任何真实儿童照片或可识别肖像\n- 若需补充：班级「平静角」实景照片（需学校提供并授权后使用）",
}
