# -*- coding: utf-8 -*-
"""小学道德与法治 · 我们讲文明（G1）—— 补齐知识树「法治启蒙」空缺

学科语气（道德与法治）：情境案例驱动，情感共鸣 + 价值判断；真实校园/公共场所场景，
结论落在「应该怎么做、为什么」，不做道德说教，不背法条。
一年级落点：全部换成能看见的具体动作（说话轻轻的小声说、排队站在最后、垃圾走到垃圾桶前再扔、
升旗时立正站好不说话），不说「要有规则意识」这种抽象话。
三个互动台子都能真的操作：①「这样做会怎样」六张情境卡，选做法后展开后果与别人的感受，
反馈写成「这样可能会……，还可以试试……」；②「这样做，大家都舒服／会打扰到别人」两筐分类；
③「校园文明小管家」——给图书馆、食堂、操场、升旗台四个地方各配一条最合适的规则。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g1-u4"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "小朋友，你有没有想过：为什么在图书馆大家说话都很轻，为什么打饭的时候大家要排队，为什么升旗的时候全班都要立正站好不说话？这些看起来不一样的事情，背后其实是同一个道理——生活里处处都有规则，规则让大家待在一起的时候都舒服。今天这节课，我们就一起来看看这些规则是什么，为什么要有它们，还有升国旗、唱国歌的时候该怎么做。",
    "problem-anchor": "开始之前，先选一个你最想弄清楚的问题。是想知道为什么有的地方要小声说话，还是想知道为什么要排队、为什么不能插队；是想知道为什么不能乱画墙壁、乱扔垃圾，还是想知道升国旗、唱国歌的时候应该怎么做。选好了，就带着它往下看。",
    "objectives": "这节课有四个小目标。第一，能说出图书馆、教室、食堂这些地方要小声说话，知道声音太大会打扰到别人。第二，能说出排队时要一个跟着一个、站在队伍里不往前挤，知道先来后到。第三，能说出爱护公物的具体做法，做到不在墙壁和课桌上乱画、垃圾走到垃圾桶前再扔。第四，知道五星红旗是我们的国旗、《义勇军进行曲》是我们的国歌，升国旗、唱国歌的时候要立正站好、不说话不乱动。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先说两件最常遇到的事：小点儿声，排好队。在图书馆看书的时候，说话要轻轻的，连走路也轻轻的，因为旁边的人正在专心看书，声音一大，他就什么都看不进去了。在食堂打饭、上下楼梯、上公交车的时候，要一个跟着一个排好队，先到的先来。队伍里不往前挤，也不插到好朋友前面。你可能会觉得等一会儿很慢，可是大家都排队，每个人都能快一点拿到饭、快一点上车；只要有一个人往前挤，队伍就乱了。",
    "lab-1": "现在我们来看六件真实的小事。每一件都有三个做法，你选一个你觉得合适的，选完立刻会有一段话，告诉你这样做以后别人心里会怎么样；要是选得不太合适，也会告诉你还可以试试什么。",
    "module-2": "接下来说说公共的东西。公共的东西，就是大家一起用的东西：教室的墙壁和桌椅、学校的图书、公园的花草、马路边的垃圾桶，这些都不是哪一个人的。公共的东西要大家一起爱护。具体怎么做呢？不在墙壁和课桌上乱涂乱画、不用小刀刻字；看到水龙头没关紧就伸手关上；看到地上有纸屑就顺手捡起来；果皮和包装袋一定要走到垃圾桶前再扔，不能随手丢，更不能从窗户扔出去。摘一朵公园的花看着是小事，可是每个人摘一朵，花坛就秃了。",
    "lab-2": "接下来我们来做一次分类。下面有八条做法，有的做出来大家都很舒服，有的会打扰到别人、把公共的地方弄脏弄坏。请你先点一条，再点它应该进的筐，看看放对没有。",
    "worked-example": "我们一起来看看升旗仪式上的小美。第一步，集合音乐一响，小美马上放下手里的东西，走到操场上站到自己的位置上，不说话也不推前面的同学。第二步，主持人说升国旗、奏国歌，她立刻立正站好，两只手放在身体两边，眼睛看着国旗慢慢升上去，不说话也不乱动。第三步，国歌响起来的时候，她跟着音乐轻声唱，一句一句唱完。第四步，仪式结束以后，她跟着队伍一个跟着一个走回教室，不跑不挤。国旗和国歌是我们国家的象征，五星红旗是中华人民共和国的国旗，《义勇军进行曲》是国歌，升旗的时候立正站好，就是在向自己的国家表达尊重。",
    "conceptest-1": "接下来用三个说法考考你，每个说法里都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件事交给你。现在请你当一次校园文明小管家，管四个地方：图书馆、食堂、操场和升旗台。先点一个地方，再从下面的规则卡里挑一条最合适的放上去，看看配得对不对。八条规则卡里有四条是配上位置的，另外四条要小心，它们放到哪儿都不合适。",
    "posttest": "最后一轮，换几个新的小情境来考考你。这次会出现电影院里、公交车上、公园里还有一次升旗，看看你能不能用上今天学到的方法。",
    "summary": "这节课我们记住三句话。第一句，小点儿声：在图书馆、教室、电影院这些地方，说话轻轻的，走路也轻轻的，不打扰别人。第二句，排好队、爱护公物、不乱扔：一个跟着一个，先来后到；不在墙上和桌上乱画；垃圾走到垃圾桶前再扔，看到水龙头没关紧就伸手关上。第三句，尊重国家象征：五星红旗是我们的国旗，《义勇军进行曲》是我们的国歌，升国旗、唱国歌的时候立正站好，不说话不乱动，跟着音乐唱。这些规则看起来是管着我们的，其实是让每个人都能舒舒服服地待在一起。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出两个需要小声说话的地方，再说出排队时要做到的两件事。第二层能力应用，动手做：和家里人一起，找一找小区或者回家路上有没有公共的东西被弄坏了，把它记下来，想一想可以怎么爱护。第三层迁移挑战，选做：当一次文明小管家，画一张校园文明提示卡，写上一句话，贴到班里相应的位置；再和家里人一起，在下一次升国旗的时候立正站好、跟着唱国歌。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 我们小点儿声·大家排好队", "lab-1": "动手一 这样做会怎样", "module-2": "概念二 爱护公物·我们不乱扔",
    "lab-2": "动手二 大家都舒服·会打扰别人", "worked-example": "例题讲解 升旗仪式上的小美", "conceptest-1": "概念测试",
    "synthesis": "综合任务 校园文明小管家", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：六件小事 × 三个做法（反馈展开公共场合里别人的感受与后果） ──
SCENES = [
    {
        "id": "s1",
        "t": "在图书馆看书，我看到一幅很有意思的图画，想和旁边的同学说",
        "opts": [
            {"k": "a", "t": "凑到他耳边，轻轻地小声说", "ok": True,
             "fb": "旁边的同学听到了，其他看书的人也没有被打扰。轻轻地说话，是想到了别人也在做自己的事。"},
            {"k": "b", "t": "直接喊他的名字，把书举起来给他看", "ok": False,
             "fb": "这样可能会把整个阅览室的人都吓一跳，正在看书的人要重新看一遍。还可以试试：先记在心里，走出图书馆再和他说。"},
            {"k": "c", "t": "一边笑一边拍桌子，越说越起劲", "ok": False,
             "fb": "这样可能会让图书管理员走过来提醒你，旁边的人也会觉得这里太吵。还可以试试：把想说的话写在纸上递给他。"},
        ],
    },
    {
        "id": "s2",
        "t": "食堂打饭，前面排了很长的队，我肚子已经很饿了",
        "opts": [
            {"k": "a", "t": "走到队尾站好，一个跟着一个慢慢往前", "ok": True,
             "fb": "队伍走得很快，大家都拿到了热饭。先来后到，是让每个人都能快一点的办法。"},
            {"k": "b", "t": "挤到前面去，说我特别饿让我先打", "ok": False,
             "fb": "这样可能会让前面的同学很不高兴，大家都饿，谁都不愿意被挤到后面。还可以试试：站到队尾，一边等一边想好今天要吃什么。"},
            {"k": "c", "t": "插到好朋友前面，让他帮我一起打", "ok": False,
             "fb": "这样可能会让排在后面的同学觉得不公平，队伍也容易乱起来。还可以试试：先跟好朋友打个招呼，自己站到他后面一起排。"},
        ],
    },
    {
        "id": "s3",
        "t": "教室的墙又白又平，我很想在墙上画一只小猫",
        "opts": [
            {"k": "a", "t": "画在自己的图画本上，画好拿给同学看", "ok": True,
             "fb": "图画本是你自己的，想画多少画多少；教室的墙还是干净的，大家看着都舒服。"},
            {"k": "b", "t": "用彩笔在墙上直接画一只小猫", "ok": False,
             "fb": "这样可能会让墙上的印子怎么擦都擦不掉，全班同学要一起看着它，老师也很为难。还可以试试：把小猫画在纸上，贴到班级的展示板上。"},
            {"k": "c", "t": "用小刀在课桌上刻自己的名字", "ok": False,
             "fb": "这样可能会把课桌刻坏，下一个坐这张桌子的同学写作业都会硌手。还可以试试：想要自己的名字被大家看到，就把作业本上的名字写得端端正正。"},
        ],
    },
    {
        "id": "s4",
        "t": "我吃完了一个橘子，手里剩下橘皮和一小袋纸巾",
        "opts": [
            {"k": "a", "t": "走到垃圾桶前，把橘皮和纸袋扔进去", "ok": True,
             "fb": "教室和操场都干干净净，打扫卫生的同学也轻松一些。多走几步路，大家都舒服。"},
            {"k": "b", "t": "先塞进课桌抽屉里，等放学再说", "ok": False,
             "fb": "这样可能会让抽屉里又脏又乱，还会招来小虫子。还可以试试：现在就站起来，走到垃圾桶前扔进去。"},
            {"k": "c", "t": "从窗户直接扔到楼下", "ok": False,
             "fb": "这样可能会砸到楼下走过的同学，也把操场弄脏了。还可以试试：拿在手里，等下楼的时候顺手扔进垃圾桶。"},
        ],
    },
    {
        "id": "s5",
        "t": "公园里有一大片花，开得很好看，我想拍张照片",
        "opts": [
            {"k": "a", "t": "站在花坛外面，把整片花拍进去", "ok": True,
             "fb": "花留在原处，后面来的人也能看到这一片好看的花。站远一点拍，照片反而更好看。"},
            {"k": "b", "t": "摘一朵拿在手里，拍照更好看", "ok": False,
             "fb": "这样可能会让这一朵花很快蔫掉，别人再也看不到它；要是每个人都摘一朵，花坛就空了。还可以试试：让它长在土里，你站到旁边和它一起拍照。"},
            {"k": "c", "t": "踩进花坛里，蹲到花中间去拍", "ok": False,
             "fb": "这样可能会把脚下的花和草踩断，花坛也被踩得坑坑洼洼。还可以试试：沿着花坛边的小路走，找一个好角度。"},
        ],
    },
    {
        "id": "s6",
        "t": "上公交车，车门口人很多，车上也站满了人",
        "opts": [
            {"k": "a", "t": "排在前门后面，一个一个上车，上去抓好扶手", "ok": True,
             "fb": "大家上得又快又稳，没有人被挤倒。抓好扶手，车开起来的时候也不会摔倒。"},
            {"k": "b", "t": "车门一开就使劲往上挤，抢一个座位", "ok": False,
             "fb": "这样可能会把旁边的人挤得站不住，老人和小朋友最容易摔倒。还可以试试：等前面的人上完再上，站一会儿也没关系。"},
            {"k": "c", "t": "上车以后在车厢里跑来跑去，扶着栏杆荡来荡去", "ok": False,
             "fb": "这样可能会在刹车的时候摔出去，撞到别的乘客。还可以试试：坐好或者抓好扶手，站定了再和同学说话。"},
        ],
    },
]

# ── 动手二：八条做法分进「大家都舒服」／「会打扰到别人」两个筐 ──
SORT_ITEMS = [
    {"id": "c1", "t": "在图书馆和教室里，说话轻轻的小声说", "bin": "good",
     "why": "小声说话，旁边的人才能专心做自己的事。这一条做出来，大家都舒服。"},
    {"id": "c2", "t": "上下楼梯和坐公交车，一个跟着一个排好队", "bin": "good",
     "why": "排好队先来后到，每个人都能又快又稳地过去。这一条做出来，大家都舒服。"},
    {"id": "c3", "t": "看到水龙头没关紧，伸手把它关上", "bin": "good",
     "why": "水龙头是大家共用的，随手关上，水就不白白流走了。这一条做出来，大家都舒服。"},
    {"id": "c4", "t": "果皮纸屑走到垃圾桶前再扔进去", "bin": "good",
     "why": "垃圾进了垃圾桶，教室和操场就干干净净。这一条做出来，大家都舒服。"},
    {"id": "c5", "t": "上课的时候大声喊同学的名字，喊他快看这边", "bin": "bad",
     "why": "老师正讲着课，这一声喊把大家的注意力都打断了。这一条会打扰到别人。"},
    {"id": "c6", "t": "从队伍中间挤到前面去，说自己很饿", "bin": "bad",
     "why": "后面的同学只能继续等，心里也会不服气，队伍还容易乱。这一条会打扰到别人。"},
    {"id": "c7", "t": "在教室的墙上和课桌上乱画、用小刀刻字", "bin": "bad",
     "why": "墙壁和课桌是大家一起用的，画上去就擦不掉了。这一条会打扰到别人。"},
    {"id": "c8", "t": "把果皮从窗户直接扔到楼下", "bin": "bad",
     "why": "楼下走过的同学可能被砸到，操场也被弄脏了。这一条会打扰到别人。"},
]
SORT_BIN = {"good": "这样做，大家都舒服", "bad": "这样做，会打扰到别人"}

# ── 综合任务：为四个地方各配一条最合适的规则 ──
PLACES = [
    {"id": "lib", "t": "图书馆"},
    {"id": "canteen", "t": "食堂"},
    {"id": "playground", "t": "操场"},
    {"id": "flag", "t": "升旗台"},
]
RULES = [
    {"id": "r1", "t": "说话轻轻的、走路也轻轻的，看完的书放回原处", "place": "lib",
     "why": "图书馆是大家安静看书的地方，声音一小，每个人都能看进去。看完把书放回原处，下一个人也找得到。"},
    {"id": "r2", "t": "排好队打饭，吃多少打多少，吃完把桌面擦干净", "place": "canteen",
     "why": "排队打饭先来后到，吃多少打多少不浪费，桌面擦干净下一位同学才好坐下。"},
    {"id": "r3", "t": "玩完体育器材放回原处，看到地上有纸屑顺手捡起来", "place": "playground",
     "why": "操场是大家一起玩的地方。器材放回原处，下一个同学拿得到；垃圾捡起来，跑起来才不怕绊倒。"},
    {"id": "r4", "t": "立正站好，不说话不乱动，跟着音乐唱国歌", "place": "flag",
     "why": "五星红旗是我们的国旗，《义勇军进行曲》是我们的国歌。升旗的时候立正站好，就是向自己的国家表达尊重。"},
    {"id": "r5", "t": "一边看书一边和同学大声讨论刚看的内容", "place": "none",
     "why": "讨论是好事情，但在图书馆里大声说，会把旁边正在看书的人都打断。想讨论可以走到走廊上，或者出了图书馆再说。"},
    {"id": "r6", "t": "端着饭碗一边跑一边吃，追着同学喂他一口", "place": "none",
     "why": "端着热汤热饭跑，很容易滑倒、烫到自己和别人。吃饭要坐下来慢慢吃，跑和追留到操场上。"},
    {"id": "r7", "t": "把篮球使劲往教室的窗户上砸", "place": "none",
     "why": "玻璃碎了会伤到人，教室里的同学还在上课。打球要到操场上，往该投的方向投。"},
    {"id": "r8", "t": "升旗的时候和同学小声聊天，手里还玩着小东西", "place": "none",
     "why": "升国旗、唱国歌是很庄重的时刻，说话、玩东西都是对国旗和国歌的不尊重。"},
]

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g1-u4 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 这样做会怎样：六件小事 × 三个做法 → 展开别人心里的感受
   3) 大家都舒服 · 会打扰别人：八条做法分进两个筐
   4) 校园文明小管家：四个地方 × 八张规则卡 → 配得对不对
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

  /* ---------- 2. 这样做会怎样 ---------- */
  var SCENES = __SCENES_JSON__;
  var stage1 = document.getElementById('civic-stage');
  if (stage1) {
    var curScene = null, doneScene = {};
    var out1 = document.getElementById('civic-out');

    function sceneById(id) {
      for (var i = 0; i < SCENES.length; i++) { if (SCENES[i].id === id) return SCENES[i]; }
      return null;
    }
    function render1() {
      document.querySelectorAll('[data-scene]').forEach(function (b) {
        var k = b.dataset.scene;
        b.classList.toggle('selected', k === curScene);
        b.classList.toggle('correct', !!doneScene[k]);
      });
      var n = Object.keys(doneScene).length;
      document.getElementById('civic-score').textContent = '已经聊过 ' + n + ' / ' + SCENES.length + ' 件小事';
    }
    function paintOptions() {
      var box = document.getElementById('civic-opts');
      box.innerHTML = '';
      if (!curScene) return;
      var S = sceneById(curScene);
      if (!S) return;
      S.opts.forEach(function (o) {
        var b = document.createElement('button');
        b.className = 'choice' + (doneScene[curScene] && o.ok ? ' correct' : '');
        b.style.textAlign = 'left';
        b.textContent = o.t;
        b.addEventListener('click', function () {
          if (doneScene[curScene]) return;
          if (o.ok) {
            doneScene[curScene] = true;
            out1.className = 'result';
            out1.innerHTML = '<strong>这样做会怎样——</strong>' + o.fb;
          } else {
            out1.className = 'result warn';
            out1.innerHTML = '<strong>这样可能会……</strong>' + o.fb;
          }
          render1();
          paintOptions();
        });
        box.appendChild(b);
      });
    }
    document.querySelectorAll('[data-scene]').forEach(function (b) {
      b.addEventListener('click', function () {
        curScene = b.dataset.scene;
        var S = sceneById(curScene);
        if (doneScene[curScene]) {
          out1.className = 'result';
          out1.innerHTML = '<strong>这件小事已经聊过啦。</strong>你上次选的做法让别人很舒服，记住它就好。';
        } else {
          out1.className = 'result warn';
          out1.innerHTML = '<strong>你现在遇到的是：' + S.t + '</strong><br>下面有三个做法，你选一个试试看，再看看别人心里会怎么想。';
        }
        render1();
        paintOptions();
      });
    });
    render1();
  }

  /* ---------- 3. 大家都舒服 · 会打扰别人 ---------- */
  var ITEMS = __SORT_JSON__;
  var BINN = __SORTBIN_JSON__;
  var stage2 = document.getElementById('nudge-stage');
  if (stage2) {
    var pickItem = null, placed = {};
    var out2 = document.getElementById('nudge-out');

    function render2() {
      document.querySelectorAll('[data-item]').forEach(function (b) {
        var k = b.dataset.item;
        b.classList.toggle('selected', k === pickItem);
        b.classList.toggle('done', !!placed[k]);
        b.disabled = !!placed[k];
      });
      var n = Object.keys(placed).length;
      document.getElementById('nudge-score').textContent = '已经放好 ' + n + ' / ' + ITEMS.length + ' 条';
      var gBox = document.getElementById('nudge-good');
      var bBox = document.getElementById('nudge-bad');
      gBox.innerHTML = ''; bBox.innerHTML = '';
      ITEMS.forEach(function (it) {
        if (!placed[it.id]) return;
        var s = document.createElement('div');
        s.className = 'tag';
        s.textContent = it.t;
        (it.bin === 'good' ? gBox : bBox).appendChild(s);
      });
      if (!gBox.innerHTML) gBox.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
      if (!bBox.innerHTML) bBox.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
    }
    document.querySelectorAll('[data-item]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (placed[b.dataset.item]) return;
        pickItem = b.dataset.item;
        out2.className = 'result warn';
        out2.innerHTML = '<strong>你选的是：' + b.textContent + '</strong><br>想一想，这一条做出来，旁边的人是更舒服了，还是被打扰到了？';
        render2();
      });
    });
    document.querySelectorAll('[data-bin]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pickItem) {
          out2.className = 'result warn';
          out2.textContent = '先在上面点一条做法，再选筐。';
          return;
        }
        var it = null;
        for (var i = 0; i < ITEMS.length; i++) { if (ITEMS[i].id === pickItem) it = ITEMS[i]; }
        if (b.dataset.bin === it.bin) {
          placed[it.id] = true;
          out2.className = 'result';
          out2.innerHTML = '<strong>放对了，它属于「' + BINN[it.bin] + '」。</strong>' + it.why;
          pickItem = null;
          if (Object.keys(placed).length === ITEMS.length) {
            out2.className = 'result';
            out2.innerHTML = '<strong>八条全放对了！</strong>记一句口诀：<strong>小声说话、排好队、护公物、不乱扔——规则不是管着我们，是让大家都能舒服地待在一起。</strong>';
          }
        } else {
          out2.className = 'result warn';
          out2.innerHTML = '<strong>再想一想这一条。</strong>' + it.why +
            '<br><span style="color:var(--muted)">常见错误：容易把「我自己方便」和「大家都舒服」搞混——判断的标准不是我想不想做，而是做出来旁边的人会怎么样。再试一次。</span>';
        }
        render2();
      });
    });
    render2();
  }

  /* ---------- 4. 校园文明小管家 ---------- */
  var RULES = __RULES_JSON__;
  var stage3 = document.getElementById('keeper-stage');
  if (stage3) {
    var curPlace = null, curRule = null, matched = {};
    var out3 = document.getElementById('keeper-out');

    function ruleById(id) {
      for (var i = 0; i < RULES.length; i++) { if (RULES[i].id === id) return RULES[i]; }
      return null;
    }
    function render3() {
      document.querySelectorAll('[data-place]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.place === curPlace);
        b.classList.toggle('correct', !!matched[b.dataset.place]);
      });
      document.querySelectorAll('[data-rule]').forEach(function (b) {
        var k = b.dataset.rule;
        b.classList.toggle('selected', k === curRule);
        b.classList.toggle('done', !!matched[k] || matched['__used_' + k]);
        b.disabled = !!matched['__used_' + k];
      });
      var n = 0;
      ['lib', 'canteen', 'playground', 'flag'].forEach(function (p) { if (matched[p]) n += 1; });
      document.getElementById('keeper-score').textContent = '已经管好 ' + n + ' / 4 个地方';
    }
    document.querySelectorAll('[data-place]').forEach(function (b) {
      b.addEventListener('click', function () {
        curPlace = b.dataset.place;
        if (matched[curPlace]) {
          out3.className = 'result';
          out3.innerHTML = '<strong>这个地方已经配好啦。</strong>换一个地方试试。';
        } else {
          out3.className = 'result warn';
          out3.innerHTML = '<strong>你想管好的是：' + b.textContent + '</strong><br>再从下面的规则卡里挑一条最合适的，点一下试试。';
        }
        render3();
      });
    });
    document.querySelectorAll('[data-rule]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (matched['__used_' + b.dataset.rule]) return;
        if (!curPlace) {
          out3.className = 'result warn';
          out3.textContent = '先在上面点一个地方，再挑规则卡。';
          return;
        }
        if (matched[curPlace]) {
          out3.className = 'result warn';
          out3.textContent = '这个地方已经配好一条啦，换一个地方试试。';
          return;
        }
        curRule = b.dataset.rule;
        var R = ruleById(curRule);
        if (R.place === curPlace) {
          matched[curPlace] = true;
          matched['__used_' + curRule] = true;
          curPlace = null;
          curRule = null;
          out3.className = 'result';
          out3.innerHTML = '<strong>配对了！</strong>' + R.why;
          var n = 0;
          ['lib', 'canteen', 'playground', 'flag'].forEach(function (p) { if (matched[p]) n += 1; });
          if (n === 4) {
            out3.className = 'result';
            out3.innerHTML = '<strong>四个地方全管好了！</strong>你已经会当校园文明小管家了。记一句话：<strong>规则不是管着我们，是让大家都能舒服地待在一起。</strong>';
          }
        } else if (R.place === 'none') {
          out3.className = 'result warn';
          out3.innerHTML = '<strong>这一条放到哪儿都不合适。</strong>' + R.why +
            '<br><span style="color:var(--muted)">误认为「只要在公共的地方做就行」的同学，常常会漏掉一件事：还要看这样做会不会影响到旁边的人。换一条规则卡试试。</span>';
        } else {
          out3.className = 'result warn';
          out3.innerHTML = '<strong>这条规则讲的是另一个地方。</strong>' + R.why +
            '<br><span style="color:var(--muted)">再想一想：这个动作最常发生在哪里？找到那个地方，把它放上去。</span>';
        }
        render3();
      });
    });
    render3();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__SCENES_JSON__', json.dumps(SCENES, ensure_ascii=False))
             .replace('__SORT_JSON__', json.dumps(SORT_ITEMS, ensure_ascii=False))
             .replace('__SORTBIN_JSON__', json.dumps(SORT_BIN, ensure_ascii=False))
             .replace('__RULES_JSON__', json.dumps(RULES, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "在图书馆看书，我想和旁边的同学说一句话，下面哪个做法更合适？",
         "options": [("凑到他耳边，轻轻地小声说", True),
                     ("直接喊他的名字，把书举起来给他看", False),
                     ("一边笑一边拍桌子，越说越起劲", False)],
         "explain": "小声说，旁边的同学听到了，看书的人也没被打扰。图书馆是大家安静看书的地方。"
                    "<strong>错因提醒：</strong>有人误认为「只说一句没什么关系」——一个人一句，一间阅览室就会吵起来，这是最常见的一个搞混。"},
        {"q": "食堂打饭，前面排了很长的队，我肚子已经很饿了，应该怎么做？",
         "options": [("走到队尾站好，一个跟着一个慢慢往前", True),
                     ("挤到前面去，说我特别饿让我先打", False),
                     ("插到好朋友前面，让他帮我一起打", False)],
         "explain": "先来后到，队伍走得快，每个人都能早一点拿到热饭。"
                    "<strong>错因提醒：</strong>常见错误是误认为「插一次队没什么大事」——只要有一个人往前挤，后面的人就都想挤，队伍就乱了。"},
        {"q": "升国旗、奏国歌的时候，下面哪个做法是对的？",
         "options": [("立正站好，眼睛看着国旗，不说话不乱动", True),
                     ("和同学小声聊天，反正老师看不见", False),
                     ("手里玩着小东西，等国歌放完就好", False)],
         "explain": "五星红旗是我们的国旗，《义勇军进行曲》是我们的国歌。升旗的时候立正站好、跟着唱国歌，就是向自己的国家表达尊重。"
                    "<strong>错因提醒：</strong>容易搞混「不说话」和「不乱动」——立正站好，是手和脚都要站定，手里也不能玩东西。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "我们小点儿声，大家排好队", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们已经知道，在学校要听老师的话、和同学好好相处（And）；可是一高兴就容易忘，在图书馆大声喊、打饭时挤到前面去，旁边的人就皱起了眉头（But）；所以这节课就来学一学，生活里处处都有规则，这些规则到底是什么、为什么要守着它（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">规则不是拿来管我们的，它是<strong>让每个人都能舒舒服服待在一起</strong>的办法。先看两件最常遇到的事。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>我们小点儿声</strong></p>
            <p style="color:var(--muted)">在图书馆、教室、电影院这些地方，说话轻轻的，走路也轻轻的。声音一小，旁边的人才能专心做自己的事。</p>
          </div>
          <div class="inner-card">
            <p><strong>大家排好队</strong></p>
            <p style="color:var(--muted)">打饭、上下楼梯、上公交车，一个跟着一个，先来后到。不往前挤，也不插到好朋友前面。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="公共场所守规则示意图：图书馆小声说话、排队打饭、垃圾扔进垃圾桶，附中文标注">
          <figcaption>示意图：公共场所里的规则——图书馆说话轻轻的 · 打饭一个跟着一个排好队 · 果皮纸屑走到垃圾桶前再扔（教学示意图，人物为极简线条）</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🔔</span><div><strong>记一句小口诀：</strong>看书轻轻说，打饭排好队；一个跟着一个走，先来后到不着急。</div></div>
{insight_box([
    {"lens": "看见它", "text": "规则不是一句口号，它就是能看见的动作：把声音放小、站到队尾、一个跟着一个往前走。"},
    {"lens": "解释它", "text": "为什么要有这些规则？因为一个地方不只我一个人。声音一大，别人就看不进书；有人往前挤，队伍就走不动。规则让每个人都少吃一点亏。"},
    {"lens": "迁移它", "text": "医院、电影院、公交车上，规则也一样。地方换了，做法不变——先想一想，我这样做，旁边的人会怎么样。"},
])}
    ''', tag="概念一"))

    scene_btns = "\n".join(
        f'            <button class="choice" data-scene="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in SCENES
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：这样做会怎样？", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一件你在公共场所可能遇到的小事，再从三个做法里选一个。<strong>选完会告诉你，旁边的人心里会怎么样。</strong></p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 今天我遇到的一件小事</div>
          <div class="grid" id="civic-stage">
{scene_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 我可以怎么做</div>
          <div class="grid" id="civic-opts">
            <span style="color:var(--muted);font-size:14px">先在上面点一件小事，这里就会出现三个做法。</span>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">聊过几件小事</span><span class="v" id="civic-score">已经聊过 0 / 6 件小事</span></div>
          </div>
          <p class="result warn" id="civic-out" style="margin-top:12px">先点一件今天可能遇到的小事。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💛</span><div><strong>说给你听：</strong>这里的做法没有分数。有些做法只是会让旁边的人不太舒服，换一个试试就好。先想一想别人会怎么样，比记住「应该怎么做」更要紧。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "人人爱护公物，我们不乱扔", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px"><strong>公共的东西</strong>，就是大家一起用的东西：教室的墙壁和桌椅、学校的图书、公园的花草、路边的垃圾桶。它们不是哪一个人的，所以要大家一起爱护。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>不在墙上和桌上乱画：</strong>想画就画在自己的本子上。用小刀刻字，会把课桌刻坏，下一个同学写作业都会硌手。</div></div>
          <div class="step"><span class="n">2</span><div><strong>垃圾走到垃圾桶前再扔：</strong>果皮、包装袋拿在手里，走到垃圾桶前扔进去。不能随手丢，更不能从窗户往外扔。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>看见不好的地方，顺手做一点：</strong>看到水龙头没关紧就伸手关上，看到地上有纸屑就顺手捡起来。多花几秒钟，大家都舒服。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="爱护公物与不乱扔垃圾示意图：垃圾进桶、关紧水龙头、不摘花、不在墙上乱画，附中文标注">
          <figcaption>示意图：爱护公物四件事——垃圾走到垃圾桶前再扔 · 看见水龙头没关紧就关上 · 公园的花不摘 · 不在墙上和课桌上乱画（教学示意图，人物为极简线条）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「公共的东西坏了不关我的事」。可是墙壁花了、桌子刻坏了、花坛秃了，难受的是每天要用它们的每一个人，包括你自己。还有的同学以为「摘一朵花、扔一张纸都是小事」——每个人都来一次小事，公共的地方就待不住了。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🌷</span><div><strong>记一句口诀：</strong>墙不画，桌不刻；垃圾进桶，随手关水；公共的东西，大家一起护。</div></div>
{insight_box([
    {"lens": "比较它", "text": "自己的东西和公共的东西：自己的本子你会收好，公共的课桌也该一样对待。差别只在用它的人有几个。"},
    {"lens": "解释它", "text": "为什么不能乱扔？因为垃圾留在大家要走过的地方，会绊倒人、招虫子，还得别人来收。多走几步路，就把麻烦留给了垃圾桶。"},
    {"lens": "迁移它", "text": "在小区里、在公园里、在公交车上，这条做法也一样：看到公共的东西被弄坏，能顺手做的就顺手做一点。"},
])}
    ''', tag="概念二"))

    item_btns = "\n".join(
        f'            <button class="sort-item" data-item="{it["id"]}">{it["t"]}</button>' for it in SORT_ITEMS
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：这样做，大家都舒服，还是会打扰到别人？", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一条做法，再点它应该进的筐：<strong>做出来大家都舒服的</strong>放一边，<strong>会打扰到别人的</strong>放另一边。</p>
        <div class="lab-panel">
          <div class="sort-bank" id="nudge-stage">
{item_btns}
          </div>
          <div class="grid grid-2" style="margin-top:14px">
            <button class="choice" data-bin="good" style="text-align:center">这样做，大家都舒服</button>
            <button class="choice" data-bin="bad" style="text-align:center">这样做，会打扰到别人</button>
          </div>
          <div class="sort-bins">
            <div class="sort-bin" id="nudge-good"><h4>这样做，大家都舒服</h4></div>
            <div class="sort-bin" id="nudge-bad"><h4>这样做，会打扰到别人</h4></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">分类进度</span><span class="v" id="nudge-score">已经放好 0 / 8 条</span></div>
          </div>
          <p class="result warn" id="nudge-out" style="margin-top:12px">先在上面点一条做法。</p>
        </div>
        <div class="inner-card">
          <p><strong>分完之后，想一想：</strong></p>
          <p style="color:var(--muted)">「会打扰到别人」那一边里，哪一条最像你自己？你打算从明天开始改哪一条？把它写下来。</p>
          <textarea id="syn-answer" rows="3" placeholder="我要改的那一条是……，我打算这样做……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="动手二", bloom="apply"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：升旗仪式上的小美", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>星期一早上，学校要举行升旗仪式。我们跟着小美看一遍，请你一步一步想一想，她哪几步做得对，为什么。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>集合音乐响了：</strong>小美马上放下手里的东西，走到操场上站到自己的位置，不说话，也不推前面的同学。</div></div>
          <div class="step"><span class="n">2</span><div><strong>主持人说升国旗、奏国歌：</strong>她立刻立正站好，两只手放在身体两边，眼睛看着国旗慢慢升上去，不说不乱动。</div></div>
          <div class="step"><span class="n">3</span><div><strong>国歌响起来：</strong>她跟着音乐轻声唱，一句一句唱完，中间不笑也不东张西望。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>仪式结束：</strong>她跟着队伍一个跟着一个走回教室，不跑不挤，手里的东西也拿好。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>为什么要这样做？</strong>五星红旗是我们国家的国旗，《义勇军进行曲》是我们国家的国歌。国旗和国歌是一个国家的象征，升旗的时候立正站好、跟着唱，就是在向自己的国家表达尊重。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「升旗的时候小声说两句、手里玩个东西没什么」。可是升国旗、唱国歌是很庄重的时刻，说话、玩东西就是对国旗和国歌的不尊重。还有的同学要注意区分「站起来了」和「站好了」——立正站好，是两只手放在身体两边、不乱动，不是随便站一站。</p>
        </div>
        <div class="inner-card">
          <p><strong>说给同桌听：</strong>小美这四步里，你已经做到哪几步？哪一步最想学着做？</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "下面哪句话说得对？",
         "options": [("规则不是拿来管我们的，是让大家都能舒服地待在一起", True),
                     ("只要没人看见，插一次队也没什么", False),
                     ("在图书馆只说一句话，不会影响到别人", False)],
         "explain": "一间阅览室里只要有几个人各说一句，就再也安静不下来了。规则保护的是每一个在里面的人。"
                    "<strong>错因提醒：</strong>常见错误是误认为「一个人一次没关系」——每个人都这样想，规则就没了，这是最容易搞混的一点。"},
        {"q": "看见教室的地上有一张纸屑，可是不是我扔的，下面哪个做法更好？",
         "options": [("顺手捡起来，走到垃圾桶前扔进去", True),
                     ("不是我扔的，不管它", False),
                     ("踢到别人的桌子底下，让别人捡", False)],
         "explain": "教室是大家一起用的地方，顺手捡一张纸只要几秒钟，教室就干净了。"
                    "<strong>错因提醒：</strong>有人误认为「不是我弄的我就不用管」——公共的地方靠的是每个人都顺手做一点。"},
        {"q": "升国旗、奏国歌的时候，下面哪个做法是对的？",
         "options": [("立正站好，手放在身体两边，跟着音乐轻声唱国歌", True),
                     ("站着，但手里继续玩小东西", False),
                     ("和旁边的同学讨论今天的作业", False)],
         "explain": "立正站好、跟着唱国歌，是在向国旗和国歌表达尊重。五星红旗是我们的国旗，《义勇军进行曲》是我们的国歌。"
                    "<strong>错因提醒：</strong>容易搞混「人站起来了」和「站好了」——手和脚都要站定，手里也不能玩东西。"}
    ], tag="概念测试"))

    place_btns = "\n".join(
        f'            <button class="choice" data-place="{p["id"]}" style="text-align:center">{p["t"]}</button>'
        for p in PLACES
    )
    rule_btns = "\n".join(
        f'            <button class="sort-item" data-rule="{r["id"]}">{r["t"]}</button>' for r in RULES
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：校园文明小管家", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一个地方，再从下面的八张规则卡里挑一条最合适的放上去。<strong>八张卡里有四张要小心，它们放到哪儿都不合适。</strong></p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 我要管好哪个地方</div>
          <div class="grid grid-2" id="keeper-stage">
{place_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 挑一条最合适的规则卡</div>
          <div class="sort-bank" id="keeper-rules">
{rule_btns}
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">管理进度</span><span class="v" id="keeper-score">已经管好 0 / 4 个地方</span></div>
          </div>
          <p class="result warn" id="keeper-out" style="margin-top:12px">先在上面点一个地方，再挑一张规则卡。</p>
        </div>
        <div class="inner-card">
          <p><strong>四个地方都配好以后，想一想：</strong></p>
          <p style="color:var(--muted)">这四条规则里，哪一条我们班最需要？请你给班里设计一句文明提示语，明天贴到相应的地方去。</p>
          <textarea id="syn-keeper" rows="3" placeholder="我写的提示语是……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，做法还在不在", TTS["posttest"], [
        {"q": "在电影院里，电影还没开始，我想和同学说说昨天的事，你会：",
         "options": [("把声音放到最轻，或者等散场以后再说", True),
                     ("正常音量说话，反正电影还没开始", False),
                     ("一边吃零食一边大声笑", False)],
         "explain": "电影院里声音一小，别人才能看清字幕、听清声音；散场以后再聊，想聊多久都可以。"
                    "<strong>错因提醒：</strong>别把「电影还没开始」当成可以大声说的理由——旁边的人已经在看了。"},
        {"q": "在公交车上，一位老奶奶上车了，车上没有空座位，你会：",
         "options": [("站起来把座位让给她，自己抓好扶手", True),
                     ("装作没看见，继续坐着", False),
                     ("把书包放到旁边的座位上，多占一个位置", False)],
         "explain": "把座位让给更需要的人，也是公共场所里的一条规则。自己抓好扶手，下一次仍然可以坐。"
                    "<strong>错因提醒：</strong>容易搞混「我先来的」和「我该让给谁」——先来后到说的是排队，让座是照顾更需要的人，两件事不冲突。"},
        {"q": "公园的长椅上有别人丢下的空瓶子，你会：",
         "options": [("顺手捡起来，走到垃圾桶前扔掉", True),
                     ("踢到草丛里，反正看不见", False),
                     ("换一张长椅坐，不管它", False)],
         "explain": "公园是大家一起用的地方，顺手捡起来扔进垃圾桶，下一位来的人就能舒舒服服坐下。"
                    "<strong>错因提醒：</strong>有人误认为「不是我喝的就不用管」——公共的地方，靠的就是每个人都顺手做一点。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，记住怎么讲文明", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>我们小点儿声：</strong>在图书馆、教室、电影院这些地方，说话轻轻的，走路也轻轻的，不打扰别人。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>排队、护公物、不乱扔：</strong>一个跟着一个，先来后到；不在墙上和桌上乱画；垃圾走到垃圾桶前再扔，看见水龙头没关紧就顺手关上。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>尊重国家象征：</strong>五星红旗是我们的国旗，《义勇军进行曲》是我们的国歌；升国旗、唱国歌的时候立正站好，不说话不乱动，跟着音乐唱。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>还要记牢一句话：</strong>规则看起来是管着我们的，其实是让每个人都能舒舒服服地待在一起。今天就先挑一条试试——比如课间说话轻一点，或者看到地上有纸屑顺手捡起来。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「小声、排队、不乱扔」这三个词，说清楚你今天打算做到的一件事。</p>
          <p style="color:var(--muted)">再动一动手：<strong>写一写</strong>你下一次升国旗打算怎么做，把三件事写在纸上，贴在自己的书桌前。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "说出两个需要小声说话的地方，每处用一句话说清楚为什么。",
            "说出排队时要做到的两件事，再说出「不乱扔」是什么意思。",
        ],
        [
            "和家里人一起，找一找小区或者回家路上有没有公共的东西被弄坏了，把它记下来，想一想可以怎么爱护。",
            "把「这样做，大家都舒服」那一边的四条读给家里人听，请他们说说哪一条你也做到了。",
        ],
        [
            "当一次文明小管家，画出一张校园文明提示卡，写上一句话，贴到班里相应的位置。",
            "和家里人约好，下一次升国旗、唱国歌的时候一起立正站好、跟着唱，做完说说心里的感觉。",
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
    "title": "我们讲文明",
    "name_en": "Being Courteous in Public",
    "grade": 1,
    "grade_cn": "一年级",
    "domain": "rule-of-law",
    "domain_cn": "法治启蒙",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学一年级学生的道德与法治课：从「我们小点儿声」「大家排好队」学公共场所的规则，从「人人爱护公物」「我们不乱扔」学怎样爱护大家一起用的东西，再在升旗仪式的情境里认识国旗、国歌是国家象征，知道升旗时要立正站好。全课用真实校园与公共场所场景里能看见的具体动作展开，让学生在「这样做会怎样」的后果里自己发现：规则不是管着我们，而是让大家都能舒服地待在一起。",
    "tags": ["我们讲文明", "规则意识", "公共秩序", "爱护公物", "不乱扔", "国旗国歌", "一年级"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学「法治启蒙」——知道生活中处处有规则，初步树立规则意识，了解国旗、国歌等国家象征的意义；对应统编《道德与法治》一年级上册第四单元「我们讲文明」：我们小点儿声；人人爱护公物；我们不乱扔；大家排好队。",
    "hero_question": "为什么有的地方要小声说话，为什么大家要排队，升旗的时候又为什么要立正站好？",
    "hero_alt": "我们讲文明知识结构图：我们小点儿声、大家排好队、爱护公物不乱扔 三栏",
    "hero_caption": "我们讲文明：我们小点儿声 · 大家排好队 · 人人爱护公物 · 我们不乱扔",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "为什么有的地方要小声说话？", "d": "声音大了会发生什么", "v": "为什么有的地方要小声说话"},
        {"t": "为什么要排队？为什么不能插队？", "d": "先来后到是什么意思", "v": "为什么要排队为什么不能插队"},
        {"t": "为什么不能乱画墙壁、乱扔垃圾？", "d": "公共的东西为什么大家一起护", "v": "为什么不能乱画墙壁乱扔垃圾"},
        {"t": "升国旗、唱国歌的时候要怎么做？", "d": "国旗和国歌为什么这么重要", "v": "升国旗唱国歌的时候要怎么做"},
    ],
    "objectives": [
        "能说出图书馆、教室、食堂这些地方要小声说话，知道声音太大会打扰别人",
        "能说出排队时要一个跟着一个、站在队伍里不往前挤，知道先来后到",
        "能说出爱护公物、不乱扔的具体做法：不在墙上和桌上乱画、垃圾走到垃圾桶前再扔",
        "知道五星红旗是国旗、《义勇军进行曲》是国歌，知道升国旗、唱国歌时要立正站好、不说话不乱动",
    ],
    "objectives_plain": [
        "能说出图书馆、教室、食堂这些地方要小声说话，知道声音太大会打扰别人",
        "能说出排队时要一个跟着一个、站在队伍里不往前挤，知道先来后到",
        "能说出爱护公物、不乱扔的具体做法：不在墙上和桌上乱画、垃圾走到垃圾桶前再扔",
        "知道五星红旗是国旗、《义勇军进行曲》是国歌，知道升国旗、唱国歌时要立正站好、不说话不乱动",
    ],
    "standards": [
        {"content": "知道生活中处处有规则，初步树立规则意识，了解国旗、国歌等国家象征的意义",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学 法治启蒙"},
        {"content": "我们小点儿声；人人爱护公物；我们不乱扔；大家排好队",
         "source": "统编《道德与法治》一年级上册 第四单元「我们讲文明」"},
    ],
    "prereqs": ["pol-e-g1-u3"],
    "prereqs_name": "养成良好习惯",
    "prereqs_meta": "pol-e-g1-u3",
    "leads_to": ["pol-e-g2-u1"],
    "next_meta": "pol-e-g2-u1",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "先想一个问题：图书馆里为什么大家都说话很轻？",
        "problem-anchor": "先定一个小目标：这节课结束时，你能说出一个地方的一条规则，还有为什么要有它。",
        "objectives": "看清四件事：小声说话、排队不挤、爱护公物不乱扔、升旗时立正站好。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "规则不是管我们的：小声说话让旁边的人能专心，排队让每个人都能快一点。",
        "lab-1": "六件小事，每件三个做法。选完会告诉你，旁边的人心里会怎么样。",
        "module-2": "公共的东西是大家一起用的：不在墙上乱画、垃圾走到垃圾桶前再扔、看见水龙头没关紧顺手关上。",
        "lab-2": "八条做法分进「这样做，大家都舒服」和「这样做，会打扰到别人」两个筐。",
        "worked-example": "小美的四步：集合就站好、国歌响起立正、跟着唱、结束跟着队伍回教室。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "给图书馆、食堂、操场、升旗台各配一条最合适的规则；八张卡里有四张放到哪儿都不合适。",
        "posttest": "出现了电影院、公交车、公园，还有一次升旗，看看你能不能用上今天的办法。",
        "summary": "三句话：小点儿声、排队护公物不乱扔、尊重国家象征。",
        "homework": "三层小任务，先做前两层，第三层可以请家里人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学道德与法治一年级「我们讲文明」单元，承接上一课「养成良好习惯」，把落点从「照顾好自己的身体」推进到「在大家共用的地方怎么做」。一年级学生第一次正式接触「规则」和「国家象征」，所以全课不做抽象说理：一是把规则还原成能看见的动作（说话轻轻的小声说、走到队尾站好、垃圾走到垃圾桶前再扔、升旗时立正站好不说话），二是把每条规则都落到「这样做别人会怎么样」上，让学生自己发现规则不是管着我们，而是让大家都能舒服地待在一起。三个互动台子都能真的操作：一是六张「这样做会怎样」情境卡，选做法后展开旁边人的感受与后果，反馈一律写成「这样可能会……，还可以试试……」；二是「这样做，大家都舒服／会打扰到别人」分类台，把八条做法分进两个筐；三是「校园文明小管家」，给图书馆、食堂、操场、升旗台四个地方各配一条最合适的规则，八张规则卡里有四张是放到哪儿都不合适的干扰项。国家象征部分放在升旗仪式的情境里讲，只讲清楚国旗是五星红旗、国歌是《义勇军进行曲》，升旗时立正站好、跟着唱，不引法条。插图一律为中性简洁的教学示意图（极简线条人物，不使用真实儿童照片）。",
    "plan_table": """| 1 | cover | 我们讲文明 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 我们小点儿声，大家排好队 | 承·概念一（公共秩序） |
| 6 | interactive | 动手一：这样做会怎样？ | 承·情境判断（展开别人的感受） |
| 7 | concept | 人人爱护公物，我们不乱扔 | 承·概念二（爱护公物） |
| 8 | interactive | 动手二：这样做，大家都舒服，还是会打扰到别人？ | 承·分类操作 |
| 9 | concept | 例题示范：升旗仪式上的小美 | 转·重难点突破（国家象征 + 易错点） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：校园文明小管家 | 合·迁移应用（规则与场所配对） |
| 12 | quiz | 后测：换几个新情境，做法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，记住怎么讲文明 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：我们小点儿声 / 大家排好队 / 爱护公物·不乱扔 三栏\n- P5 公共场所守规则示意图（已生成）：图书馆小声、排队打饭、垃圾入桶，附中文标注\n- P7 爱护公物四件事示意图（已生成）：垃圾进桶、关紧水龙头、不摘花、不在墙上乱画，附中文标注\n- 三张图均为教学示意图，人物仅用极简线条，不使用任何真实儿童照片或可识别肖像\n- 若需补充：本班文明提示卡模板（可由学生手绘）",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
