# -*- coding: utf-8 -*-
"""小学道德与法治 · 我是小学生啦（G1）—— 补齐知识树「道德修养」空缺

学科语气（道德与法治）：情境案例驱动，情感共鸣 + 价值判断；结论落在「应该怎么做、为什么」，
不做道德说教，也不做法条背诵。
一年级落点：全部换成能看见的具体动作（进校门先问好、上课想说话先举手、放学在老师身边等），
不讲抽象概念。
国旗相关表述一律庄重得体：国旗是国家的象征，升国旗、奏国歌时停下手中的事、立正站好、
面向国旗、不说话不打闹，认真唱国歌。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g1-u1"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "小朋友，从今天起，你就是一名小学生啦。背上书包，走过一条马路，走进一扇新的大门，学校里的一切都有点陌生。别着急，这节课我们一起来做四件事：上学路上怎么走才安全；国歌响起的时候应该怎么做；学校里有哪些地方、分别是做什么用的；放学了家长还没来，在哪里等最安全。学完这几件小事，你就能开开心心上学去，平平安安回家来。",
    "problem-anchor": "开始之前，先选一个你最想弄清楚的问题。是想知道上学路上怎么走才安全，还是想知道国歌响起来的时候应该怎么做；是想认一认学校里的地方，还是想知道放学家长还没来该怎么办。选好了，就带着它往下看。",
    "objectives": "这节课有四个小目标。第一，能说出上学路上和放学路上要注意的几件事，知道怎么走才安全。第二，知道国旗是我们国家的象征，升国旗、奏国歌的时候要立正站好、不说话，庄重地行礼。第三，能说出校园里几个常用的地方和它们的用处。第四，遇到不懂的、不确定的事情，知道可以问老师、问家长。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先来说说上学路上。出门以前，先检查一下书包和水杯，跟家里人说一声我去上学啦。走在路上，要走在人行道上，牵着大人的手；过马路的时候，看清红绿灯，走斑马线，不追跑不打闹。到了校门口，看见老师，走上前问一声老师您好。这几件小事都做到了，上学这一天开头就是顺顺当当的。",
    "lab-1": "现在请你当一次上学小向导。这里有一天里可能遇到的六件事，每一件事都有三个做法。你选一个你觉得合适的，选完立刻会有一段话告诉你为什么；要是选得不太合适，也会告诉你还可以试试什么。",
    "module-2": "每个星期一的早上，学校都要举行升旗仪式。国旗是我们国家的象征，升国旗、奏国歌是一件很庄重的事。国歌一响起来，就要停下手里的事情，面向国旗立正站好，不说话、不打闹，少先队员行队礼，其他同学行注目礼，唱国歌的时候跟着认真地唱。除了升旗的地方，学校里还有几个每天都会去的地方：教室是上课的地方，饮水处接水，卫生间课间去，操场活动，保健室是身体不舒服的时候去的，图书角可以借书看。把它们认清楚，你在学校里就不会迷路。",
    "lab-2": "现在请你当一次校园小向导。上面是六件在学校里可能会发生的事，下面是校园里的六个地方。先点一件事，再点你觉得该去的地方。找对了会告诉你为什么，找错了也会提醒你再想一想。",
    "worked-example": "我们一起来帮平平想一想。平平第一天上小学。第一步，出门前，他检查了书包和水杯，然后牵着妈妈的手，走人行道去学校。第二步，在校门口看见老师，他走上前问了一声老师您好，然后找到自己的座位，把语文书和铅笔盒摆在桌角。第三步，升旗仪式上，国歌一响起来，他马上停下动作，面向国旗立正站好，跟着认真唱国歌。第四步，下午放学，家长还没来，他回到老师身边，在老师能看到的地方等着。",
    "conceptest-1": "接下来用三个说法考考你，每个说法里都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件事交给你。下面有六条放学路上的做法，请你判断一下：哪些做法是安全的，放进这样做安全这一边；哪些做法有危险，放进这样做有危险那一边。放好以后，再读一读为什么。",
    "posttest": "最后一轮，换几个新的小情境来考考你。这次会出现下雨天、不认识的人、还有和同学一起走路，看看你能不能用上今天学到的办法。",
    "summary": "这节课我们记住四句话。第一句，上学路上走人行道、牵大人的手，过马路看红绿灯、走斑马线。第二句，国歌响起的时候停下手里的事，面向国旗立正站好，认真唱国歌，这是我们对国旗、对祖国的尊敬。第三句，教室上课、饮水处接水、卫生间课间去、操场活动、保健室不舒服就去，认得路，心不慌。第四句，放学家长还没来，就回到老师身边等，这是最安全的做法。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出上学路上要注意的两件事，再说出校园里三个地方和它们的用处。第二层能力应用，动手做：和家里人一起走一遍从家到学校上学的路，把过马路的地方指出来，说说应该看什么。第三层迁移挑战，选做：画一张我们的校园图，把教室、饮水处、卫生间、操场、保健室、升旗广场都标出来，讲给同桌听。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 开开心心上学去", "lab-1": "动手一 校园一天", "module-2": "概念二 向国旗敬礼 · 认认校园",
    "lab-2": "动手二 我们的校园", "worked-example": "例题讲解 平平的第一天", "conceptest-1": "概念测试",
    "synthesis": "综合任务 平平安安回家来", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：校园一天，六个情境 × 三个做法（反馈一律「这样可能会……还可以试试……」） ──
SCENES = [
    {
        "id": "s1",
        "t": "早上出门，我要去上学了",
        "opts": [
            {"k": "a", "t": "背好书包，和家里人牵着手走人行道", "ok": True,
             "fb": "这样安排真好。走在人行道上，大人在你身边，一路上又安全又开心。"},
            {"k": "b", "t": "先在家里玩一会儿，快迟到了再跑着去", "ok": False,
             "fb": "这样可能会让你一路都很着急，跑起来还容易摔跤。还可以试试：早一点出门，慢慢走过去。"},
            {"k": "c", "t": "自己先跑出家门", "ok": False,
             "fb": "这样可能会让家里人找不到你，路上有车也很危险。还可以试试：和家人一起出门，牵着大人的手。"},
        ],
    },
    {
        "id": "s2",
        "t": "走进校门，我看见了老师",
        "opts": [
            {"k": "a", "t": "走上前，问一声「老师，您好！」", "ok": True,
             "fb": "真有礼貌。一句问好，老师心里暖暖的，你自己也会觉得学校很亲切。"},
            {"k": "b", "t": "低着头，从老师身边快快走过去", "ok": False,
             "fb": "这样可能会让老师以为你有心事，你自己也少了一次被关心的机会。还可以试试：抬起头，笑着说一声老师您好。"},
            {"k": "c", "t": "一边跑一边大声喊老师的外号", "ok": False,
             "fb": "这样可能会让老师有点难过，旁边的同学也会觉得吵。还可以试试：站稳了，轻轻地说一声老师您好。"},
        ],
    },
    {
        "id": "s3",
        "t": "上课了，我很想说话",
        "opts": [
            {"k": "a", "t": "先举手，老师请我再说", "ok": True,
             "fb": "这个办法真好。举了手，老师就知道你有话要说，其他同学也还能听清老师讲话。"},
            {"k": "b", "t": "直接大声说出来", "ok": False,
             "fb": "这样可能会打断老师，也会让旁边的同学听不清。还可以试试：先举手，等老师看到你。"},
            {"k": "c", "t": "不管老师，和同桌小声聊", "ok": False,
             "fb": "这样可能会让同桌也漏掉老师说的话。还可以试试：把想说的话在心里放一放，举手以后再说。"},
        ],
    },
    {
        "id": "s4",
        "t": "课间十分钟，我想去操场玩",
        "opts": [
            {"k": "a", "t": "先去喝水、上厕所，再和同学慢慢走去操场", "ok": True,
             "fb": "安排得真好。先把身体的事情做好，玩起来也更放心。"},
            {"k": "b", "t": "在走廊里追着同学跑", "ok": False,
             "fb": "这样可能会撞到别人，自己也很容易摔跤。还可以试试：在走廊里慢慢走，到操场上再放开玩。"},
            {"k": "c", "t": "一直玩到上课铃响才往回跑", "ok": False,
             "fb": "这样可能会迟到，还会一上课就气喘吁吁。还可以试试：听到铃声以前就收拾好，慢慢走回教室。"},
        ],
    },
    {
        "id": "s5",
        "t": "星期一早上，国歌响起来了",
        "opts": [
            {"k": "a", "t": "马上停下手里的动作，面向国旗立正站好", "ok": True,
             "fb": "这个做法很庄重。国歌响起的时候停下动作、站好、不说话，是我们对国旗、对祖国的尊敬。"},
            {"k": "b", "t": "先把手里的事情做完，再站好", "ok": False,
             "fb": "这样可能会错过升旗最庄重的时刻。还可以试试：一听到国歌就停下来，面向国旗站好。"},
            {"k": "c", "t": "和旁边的同学小声说这首歌我会唱", "ok": False,
             "fb": "这样可能会让队伍不整齐，也不太庄重。还可以试试：把话留到仪式结束以后，先跟着认真唱。"},
        ],
    },
    {
        "id": "s6",
        "t": "放学了，家长还没来接我",
        "opts": [
            {"k": "a", "t": "回到老师身边，在老师能看到的地方等", "ok": True,
             "fb": "这个做法最安全。老师会陪着你等，也会帮你联系家里人。"},
            {"k": "b", "t": "自己走出校门去找家人", "ok": False,
             "fb": "这样可能会让老师和家人都非常着急，校门外车多人多也很危险。还可以试试：先回到老师身边。"},
            {"k": "c", "t": "跟着一位不认识的大人走", "ok": False,
             "fb": "这样非常危险。不认识的人要带你走，一定不可以答应。还可以试试：马上回到老师身边，把这件事告诉老师。"},
        ],
    },
]

# ── 动手二：我们的校园，六件事 → 六个地方 ──
PLACES = [
    {"id": "water", "n": "饮水处", "use": "接水喝的地方"},
    {"id": "wc", "n": "卫生间", "use": "上厕所的地方"},
    {"id": "clinic", "n": "保健室", "use": "身体不舒服时去的地方"},
    {"id": "corner", "n": "图书角", "use": "看书、借书的地方"},
    {"id": "playground", "n": "操场", "use": "体育课和课间活动的地方"},
    {"id": "flag", "n": "升旗广场", "use": "每周一举行升旗仪式的地方"},
]
TASKS = [
    {"id": "t1", "t": "上完体育课，口渴了，想喝水", "pid": "water",
     "why": "喝水要去饮水处，接好水慢慢喝，喝完把水杯放好。"},
    {"id": "t2", "t": "上课前想去上厕所", "pid": "wc",
     "why": "课间先上厕所，上课的时候就不会着急了。"},
    {"id": "t3", "t": "头有点晕，身体不舒服", "pid": "clinic",
     "why": "身体不舒服要告诉老师，去保健室让老师看一看。"},
    {"id": "t4", "t": "想借一本图画书看", "pid": "corner",
     "why": "去图书角借书，看完记得还回去，这样别人也能看。"},
    {"id": "t5", "t": "体育课要跑步、做游戏", "pid": "playground",
     "why": "跑步和做游戏都在操场上进行，那里地方大，跑起来更安全。"},
    {"id": "t6", "t": "星期一早上，要参加升旗仪式", "pid": "flag",
     "why": "升旗仪式在升旗广场举行。国歌响起时，要面向国旗立正站好。"},
]

# ── 综合任务：平平安安回家来（分进两个筐） ──
SORT_ITEMS = [
    {"id": "k1", "t": "过马路时牵着大人的手，看清红绿灯，走斑马线", "bin": "safe",
     "why": "看信号灯、走斑马线，是过马路最稳当的办法。"},
    {"id": "k2", "t": "走在人行道上，不追跑、不打闹", "bin": "safe",
     "why": "人行道是给人走路的地方，慢慢走就不会撞到别人。"},
    {"id": "k3", "t": "下雨打伞的时候，把伞沿抬起来看清前面", "bin": "safe",
     "why": "伞挡着眼睛就看不见路，把伞抬一抬，前面就看得清了。"},
    {"id": "k4", "t": "看到没有车，就自己跑过马路", "bin": "danger",
     "why": "车来得很快，看见没车不等于安全。过马路一定要看信号灯、走斑马线，还要有大人在身边。"},
    {"id": "k5", "t": "跟着一位不认识的大人走", "bin": "danger",
     "why": "不认识的人要带你走，一定不可以答应，要马上回到老师身边。"},
    {"id": "k6", "t": "在马路边等家长，顺便和同学追着玩", "bin": "danger",
     "why": "马路边车来车往，追着玩很容易冲到路上，等家长要站在安全的地方。"},
]
SORT_BIN = {"safe": "这样做安全", "danger": "这样做有危险"}

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g1-u1 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 校园一天：六个情境 × 三个做法 → 温和反馈（不判错、不贴标签）
   3) 我们的校园：六件事 → 六个地方（配对）
   4) 平平安安回家来：七条做法分进「安全 / 有危险」两个筐
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

  /* ---------- 2. 校园一天 ---------- */
  var SCENES = __SCENES_JSON__;
  var stage1 = document.getElementById('day-stage');
  if (stage1) {
    var curScene = null, doneScene = {};
    var out1 = document.getElementById('day-out');

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
      document.getElementById('day-score').textContent = '已经聊过 ' + n + ' / ' + SCENES.length + ' 件事';
    }
    function paintOptions() {
      var box = document.getElementById('day-opts');
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
            out1.innerHTML = '<strong>这个办法挺好。</strong>' + o.fb;
          } else {
            out1.className = 'result warn';
            out1.innerHTML = '<strong>还可以再想一想。</strong>' + o.fb;
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
          out1.innerHTML = '<strong>这件事已经聊过啦。</strong>你上次选的做法很合适，记住它就好。';
        } else {
          out1.className = 'result warn';
          out1.innerHTML = '<strong>你遇到的是：' + S.t + '</strong><br>下面有三个做法，你选一个试试看。';
        }
        render1();
        paintOptions();
      });
    });
    render1();
  }

  /* ---------- 3. 我们的校园：六件事 → 六个地方 ---------- */
  var TASKS = __TASKS_JSON__;
  var PLACES = __PLACES_JSON__;
  var stage2 = document.getElementById('campus-stage');
  if (stage2) {
    var pickedTask = null, solved = {};
    var out2 = document.getElementById('campus-out');

    function placeName(pid) {
      for (var i = 0; i < PLACES.length; i++) { if (PLACES[i].id === pid) return PLACES[i].n; }
      return '';
    }
    function render2() {
      document.querySelectorAll('[data-task]').forEach(function (b) {
        var k = b.dataset.task;
        b.classList.toggle('selected', k === pickedTask);
        b.classList.toggle('done', !!solved[k]);
        b.disabled = !!solved[k];
      });
      var n = Object.keys(solved).length;
      document.getElementById('campus-score').textContent = '已经找对 ' + n + ' / ' + TASKS.length + ' 件事';
      var bank = document.getElementById('campus-done');
      bank.innerHTML = '';
      TASKS.forEach(function (t) {
        if (!solved[t.id]) return;
        var s = document.createElement('span');
        s.className = 'tag';
        s.textContent = t.t.slice(0, 8) + '… → ' + placeName(t.pid);
        bank.appendChild(s);
      });
      if (!bank.innerHTML) {
        bank.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有找对一件事。</span>';
      }
    }
    document.querySelectorAll('[data-task]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (solved[b.dataset.task]) return;
        pickedTask = b.dataset.task;
        var T = null;
        for (var i = 0; i < TASKS.length; i++) { if (TASKS[i].id === pickedTask) T = TASKS[i]; }
        out2.className = 'result warn';
        out2.innerHTML = '<strong>你遇到的事是：' + T.t + '</strong><br>想一想，学校里哪个地方能做这件事？点一点下面。';
        render2();
      });
    });
    document.querySelectorAll('[data-place]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pickedTask) {
          out2.className = 'result warn';
          out2.textContent = '先在上面点一件事，再来选地方。';
          return;
        }
        var T = null;
        for (var i = 0; i < TASKS.length; i++) { if (TASKS[i].id === pickedTask) T = TASKS[i]; }
        if (b.dataset.place === T.pid) {
          solved[T.id] = true;
          out2.className = 'result';
          out2.innerHTML = '<strong>找对了，是' + placeName(T.pid) + '。</strong>' + T.why;
          pickedTask = null;
          if (Object.keys(solved).length === TASKS.length) {
            out2.className = 'result';
            out2.innerHTML = '<strong>六件事全找对了！</strong>教室上课、饮水处接水、卫生间课间去、操场活动、保健室不舒服就去、升旗广场参加升旗仪式——<strong>认得路，心不慌。</strong>';
          }
        } else {
          out2.className = 'result warn';
          out2.innerHTML = '<strong>这里不是做这件事的地方。</strong>你点的是「' + b.textContent + '」。' +
            '<br><span style="color:var(--muted)">常见错误：容易把「饮水处」和「保健室」搞混——喝水去饮水处，身体不舒服才去保健室。再想一想。</span>';
        }
        render2();
      });
    });
    render2();
  }

  /* ---------- 4. 平平安安回家来：分进两个筐 ---------- */
  var ITEMS = __SORT_JSON__;
  var BINN = __SORTBIN_JSON__;
  var stage3 = document.getElementById('safe-stage');
  if (stage3) {
    var pickItem = null, placed = {};
    var out3 = document.getElementById('safe-out');

    function render3() {
      document.querySelectorAll('[data-item]').forEach(function (b) {
        var k = b.dataset.item;
        b.classList.toggle('selected', k === pickItem);
        b.classList.toggle('done', !!placed[k]);
        b.disabled = !!placed[k];
      });
      var n = Object.keys(placed).length;
      document.getElementById('safe-score').textContent = '已经放好 ' + n + ' / ' + ITEMS.length + ' 条';
      var safeBox = document.getElementById('safe-bin-s');
      var riskBox = document.getElementById('safe-bin-d');
      safeBox.innerHTML = ''; riskBox.innerHTML = '';
      ITEMS.forEach(function (it) {
        if (!placed[it.id]) return;
        var s = document.createElement('div');
        s.className = 'tag';
        s.textContent = it.t;
        (it.bin === 'safe' ? safeBox : riskBox).appendChild(s);
      });
      if (!safeBox.innerHTML) safeBox.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
      if (!riskBox.innerHTML) riskBox.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
    }
    document.querySelectorAll('[data-item]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (placed[b.dataset.item]) return;
        pickItem = b.dataset.item;
        out3.className = 'result warn';
        out3.innerHTML = '<strong>你选的是：' + b.textContent + '</strong><br>想一想，它是安全的做法，还是有危险的做法？';
        render3();
      });
    });
    document.querySelectorAll('[data-safe-bin]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pickItem) {
          out3.className = 'result warn';
          out3.textContent = '先在上面点一条做法，再选筐。';
          return;
        }
        var it = null;
        for (var i = 0; i < ITEMS.length; i++) { if (ITEMS[i].id === pickItem) it = ITEMS[i]; }
        if (b.dataset.safeBin === it.bin) {
          placed[it.id] = true;
          out3.className = 'result';
          out3.innerHTML = '<strong>放对了，它属于「' + BINN[it.bin] + '」。</strong>' + it.why;
          pickItem = null;
          if (Object.keys(placed).length === ITEMS.length) {
            out3.className = 'result';
            out3.innerHTML = '<strong>六条全放对了！</strong>记一句口诀：<strong>人行道，慢慢走；红绿灯，看清楚；斑马线，才过路；家长没来，老师身边站。</strong>';
          }
        } else {
          out3.className = 'result warn';
          out3.innerHTML = '<strong>再想一想这条做法。</strong>' + it.why +
            '<br><span style="color:var(--muted)">常见错误：容易把「现在没出问题」误认为「这样做就是安全的」。安全靠的是看信号灯、走斑马线、有大人在身边这些做法。</span>';
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
             .replace('__TASKS_JSON__', json.dumps(TASKS, ensure_ascii=False))
             .replace('__PLACES_JSON__', json.dumps(PLACES, ensure_ascii=False))
             .replace('__SORT_JSON__', json.dumps(SORT_ITEMS, ensure_ascii=False))
             .replace('__SORTBIN_JSON__', json.dumps(SORT_BIN, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "过马路的时候，怎么做最安全？",
         "options": [("牵着大人的手，看清红绿灯，走斑马线", True),
                     ("看到没有车，就自己快点跑过去", False),
                     ("一边走一边和同学追着玩", False)],
         "explain": "看信号灯、走斑马线、有大人在身边，这三件事一起做到才最稳当。"
                    "<strong>错因提醒：</strong>常见错误是误认为「没看到车就可以过」——车来得比我们想得快，一定要看信号灯。"},
        {"q": "星期一早上，国歌响起来了，下面哪个做法最合适？",
         "options": [("马上停下手里的事，面向国旗立正站好", True),
                     ("先把手里的事情做完，再站好", False),
                     ("和旁边的同学小声说话", False)],
         "explain": "国旗是我们国家的象征，国歌响起时要停下动作、站好、不说话，认真地唱国歌。"
                    "<strong>错因提醒：</strong>有人误认为「只要不出声就够了」——还要停下手里的事、站好、面向国旗，这样才庄重。"},
        {"q": "在学校里口渴了，应该去哪里？",
         "options": [("饮水处", True), ("保健室", False), ("老师办公室", False)],
         "explain": "饮水处是接水喝的地方，课间去接好水，慢慢喝。"
                    "<strong>错因提醒：</strong>容易把饮水处和保健室搞混——保健室是身体不舒服的时候才去的。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "开开心心上学去：路上的小事做好了，一天就顺了", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">在幼儿园的时候，我们每天也有家里人接送，走一小段路就到（And）；可是上了小学，路要自己走，校门更大、人更多，路上有红绿灯也有车，走错了会不安全（But）；所以先来学一学，从家门口到教室，一路上该怎么做（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">从家里出门，到走进教室坐下来，中间有几件<strong>很小、但很重要</strong>的事。做好它们，上学这一天开头就顺了。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>出门以前</strong></p>
            <p style="color:var(--muted)">检查书包和水杯带好了没有；跟家里人说一声「我去上学啦」；和家人一起出门。</p>
          </div>
          <div class="inner-card">
            <p><strong>走在路上</strong></p>
            <p style="color:var(--muted)">走在人行道上，牵着大人的手；过马路看清红绿灯，走斑马线；不追跑、不打闹。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="上学路上示意图：走人行道、过马路看红绿灯走斑马线、到校门口向老师问好，附中文标注">
          <figcaption>示意图：上学路上的三件事——走人行道 · 过马路看红绿灯走斑马线 · 到校门口向老师问一声好（教学示意图，人物为极简线条）</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🚸</span><div><strong>记一句小口诀：</strong>人行道，慢慢走；红绿灯，看清楚；斑马线，才过路——<strong>路走对了，上学就开心。</strong></div></div>
{insight_box([
    {"lens": "看见它", "text": "安全的做法都是能看见的小动作：牵着手、看灯、走斑马线、慢慢走。它们不在纸上，就在每一步里。"},
    {"lens": "解释它", "text": "为什么这几件事能保护我们？因为司机能看见走斑马线的人，大人能拉住突然想跑的你——把「别人看得见我」变成一件确定的事。"},
    {"lens": "迁移它", "text": "去公园、去超市、去外婆家，路上也是这几件事。地方换了，做法不变：走人行道、看信号灯、有大人陪着。"},
])}
    ''', tag="概念一"))

    scene_btns = "\n".join(
        f'            <button class="choice" data-scene="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in SCENES
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：校园一天，你会怎么做？", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一件你今天可能遇到的事，再从三个做法里选一个。<strong>选得好会告诉你为什么，选得不太合适也会告诉你还可以试试什么。</strong></p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 今天我遇到的一件事</div>
          <div class="grid" id="day-stage">
{scene_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 我可以怎么做</div>
          <div class="grid" id="day-opts">
            <span style="color:var(--muted);font-size:14px">先在上面点一件事，这里就会出现三个做法。</span>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">聊过几件事</span><span class="v" id="day-score">已经聊过 0 / 6 件事</span></div>
          </div>
          <p class="result warn" id="day-out" style="margin-top:12px">先点一件今天可能遇到的事。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💛</span><div><strong>说给你听：</strong>这里的做法没有「对」和「错」的分数。有些做法只是会让你麻烦一点，换一个试试就好。拿不准的时候，问老师、问家长，都是很好的办法。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "我向国旗敬个礼 · 认认我们的校园", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">每个星期一早上，学校都要举行升旗仪式。<strong>国旗是我们国家的象征</strong>，升国旗、奏国歌是一件很庄重的事。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>国歌一响：</strong>马上停下手里的事情，不再走动，不再说笑。</div></div>
          <div class="step"><span class="n">2</span><div><strong>站好行礼：</strong>面向国旗立正站好，不说话、不打闹。少先队员行队礼，其他同学行注目礼——这个站好、看着国旗的动作，<strong>叫做行注目礼</strong>。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>认真唱国歌：</strong>跟着队伍一起唱，声音不用很大，但要用心。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「升旗的时候只要不说话就算做到了」。其实还要停下手里的事、面向国旗站好。这些动作，是我们对国旗、对祖国表达尊敬的方式。</p>
        </div>
        <p style="font-size:17px;margin:16px 0 12px">除了升旗的地方，学校里还有几个<strong>每天都会去的地方</strong>，认清楚它们，走到哪里都不慌。</p>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="校园常用地点示意图：教室、饮水处、卫生间、图书馆、操场、升旗广场，附中文标注">
          <figcaption>示意图：校园里每天都会用到的几个地方——教室上课 · 饮水处接水 · 卫生间课间去 · 图书角借书 · 操场活动 · 保健室不舒服就去（教学示意图）</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🏫</span><div><strong>一句小口诀：</strong>教室上课、水房接水、厕所课间去、操场活动、保健室不舒服就去、升旗广场要站好——<strong>认得路，心不慌。</strong></div></div>
{insight_box([
    {"lens": "看见它", "text": "国旗是国家的象征。升国旗的时候，全校同学停下动作、站好、面向国旗，这一个整齐的动作，就是大家在说同一句话。"},
    {"lens": "比较它", "text": "平时在教室里可以说话、可以走动；升旗仪式上要停下、站好、不说话。同一群人，换了一个时刻，做法就不一样。"},
    {"lens": "迁移它", "text": "认地方这个办法到哪里都有用：先去认一认门在哪里、水在哪里、不舒服的时候去哪里、找不到路可以问谁。"},
])}
    ''', tag="概念二"))

    task_btns = "\n".join(
        f'            <button class="choice" data-task="{t["id"]}" style="text-align:left">{t["t"]}</button>'
        for t in TASKS
    )
    place_btns = "\n".join(
        f'            <button class="choice" data-place="{p["id"]}" style="text-align:center">{p["n"]}</button>'
        for p in PLACES
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：我们的校园，这是哪儿？", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">上面是六件在学校里可能会发生的事，下面是校园里的六个地方。先点一件事，再点你觉得该去的地方。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 发生了一件事</div>
          <div class="grid" id="campus-stage">
{task_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 该去哪个地方</div>
          <div class="grid grid-3">
{place_btns}
          </div>
          <div class="inner-card" style="margin-top:14px">
            <p><strong>我们的校园地图</strong></p>
            <div id="campus-done" style="display:flex;flex-wrap:wrap;gap:6px"><span style="color:var(--muted);font-size:14px">还没有找对一件事。</span></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">闯关进度</span><span class="v" id="campus-score">已经找对 0 / 6 件事</span></div>
          </div>
          <p class="result warn" id="campus-out" style="margin-top:12px">先在上面点一件事。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🗺️</span><div><strong>找不到路怎么办？</strong>那就问。找一位老师，说清楚你要做什么，老师会告诉你去哪里。问路一点也不丢人，是很聪明的做法。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：平平的第一天", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>平平第一天上小学。从出门到放学，他遇到了四件事。请你帮他一件一件想清楚。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>出门上学：</strong>检查书包和水杯，牵着妈妈的手走人行道，过马路看清红绿灯，走斑马线。</div></div>
          <div class="step"><span class="n">2</span><div><strong>走进校门：</strong>看见老师，走上前问一声「老师，您好！」；找到自己的座位，把语文书和铅笔盒摆在桌角。</div></div>
          <div class="step"><span class="n">3</span><div><strong>升旗仪式：</strong>国歌一响，马上停下动作，面向国旗立正站好，跟着认真唱国歌。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>放学以后：</strong>家长还没来，就回到老师身边，在老师能看到的地方等着。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「第一天上小学，要赶紧做点什么才不显得笨」。其实第一天完全可以慢一点、看一看。平平这四步里，最要紧的是<strong>该停的时候停下来，该等的时候等一等</strong>。</p>
        </div>
        <div class="inner-card">
          <p><strong>说给同桌听：</strong>平平这四步里，哪一步你自己已经做到了？哪一步还想再练一练？</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "下面哪句话说得对？",
         "options": [("国旗是我们国家的象征，升国旗、奏国歌时要庄重地站好行注目礼", True),
                     ("升旗的时候只要不出声，做什么都可以", False),
                     ("升旗仪式是老师的事，和同学关系不大", False)],
         "explain": "国旗是国家的象征，参加升旗仪式是每个同学都要认真做好的事。"
                    "<strong>错因提醒：</strong>常见错误是误认为「不出声就够了」——还要停下动作、面向国旗站好、认真唱国歌。"},
        {"q": "放学了，家长还没来接你，下面哪个做法最安全？",
         "options": [("回到老师身边，在老师能看到的地方等", True),
                     ("自己走出校门去找家长", False),
                     ("校门外有人招手，就走过去看看是不是家长", False)],
         "explain": "在老师身边等，老师会陪着你，也能帮你联系家里人。"
                    "<strong>错因提醒：</strong>有人误认为「自己去找更快」，其实校外车多人多，一个人走反而最危险。"},
        {"q": "在学校里，下面哪个地方是「课间先把身体的事情做好」要去的地方？",
         "options": [("卫生间", True), ("图书角", False), ("升旗广场", False)],
         "explain": "课间先上厕所、喝好水，上课的时候才不会着急。"
                    "<strong>错因提醒：</strong>容易把几个地方搞混——图书角是看书借书的地方，升旗广场是举行升旗仪式的地方。"}
    ], tag="概念测试"))

    item_btns = "\n".join(
        f'            <button class="sort-item" data-item="{it["id"]}">{it["t"]}</button>' for it in SORT_ITEMS
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：平平安安回家来，把做法分进两个筐", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一条做法，再点它应该进的筐：<strong>安全的做法</strong>放一边，<strong>有危险的做法</strong>放另一边。</p>
        <div class="lab-panel">
          <div class="sort-bank" id="safe-stage">
{item_btns}
          </div>
          <div class="grid grid-2" style="margin-top:14px">
            <button class="choice" data-safe-bin="safe" style="text-align:center">这样做安全</button>
            <button class="choice" data-safe-bin="danger" style="text-align:center">这样做有危险</button>
          </div>
          <div class="sort-bins">
            <div class="sort-bin" id="safe-bin-s"><h4>这样做安全</h4></div>
            <div class="sort-bin" id="safe-bin-d"><h4>这样做有危险</h4></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">分类进度</span><span class="v" id="safe-score">已经放好 0 / 6 条</span></div>
          </div>
          <p class="result warn" id="safe-out" style="margin-top:12px">先在上面点一条做法。</p>
        </div>
        <div class="inner-card">
          <p><strong>分完之后，想一想：</strong></p>
          <p style="color:var(--muted)">有危险的做法里，有没有哪一条很像「我上次差点做过的事」？把它记下来，再说一说换成安全的做法应该怎么做。</p>
          <textarea id="syn-answer" rows="3" placeholder="我差点做过……，现在我会……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，做法还在不在", TTS["posttest"], [
        {"q": "下雨天，你打着伞走到路口，发现伞沿挡住了眼睛，你会：",
         "options": [("把伞往上抬一抬，看清红绿灯再走", True),
                     ("低着头快步走过去", False),
                     ("把伞收起来跑过马路", False)],
         "explain": "伞挡住眼睛就看不见灯和车，先看清再走。"
                    "<strong>错因提醒：</strong>常见错误是误认为「打伞看不见也没关系，反正走得快」——看不见的时候，走得快最危险。"},
        {"q": "校门口有一位不认识的大人对你说「我带你去找妈妈」，你会：",
         "options": [("不跟他走，马上回到老师身边", True),
                     ("跟他走，他看起来不凶", False),
                     ("先跟他说说我家住在哪里", False)],
         "explain": "不认识的人要带你走，一定不可以答应，要马上回到老师身边，把这件事告诉老师。"
                    "<strong>错因提醒：</strong>容易误认为「看起来和善就可以相信」——认不认识，比凶不凶更重要。"},
        {"q": "和同学一起走在回家的路上，同学说「我们跑着比赛吧」，你会：",
         "options": [("告诉他这样不安全，一起慢慢走", True),
                     ("跟着一起跑，跑在人行道上就行", False),
                     ("跑一小段，等没车再继续跑", False)],
         "explain": "路上不是玩的地方，跑起来容易冲到马路上。"
                    "<strong>错因提醒：</strong>有人误认为「有人一起就没事」——人多更容易互相追着冲到路上，安全靠的是做法，不是人数。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：四句话，讲清小学生的一天", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>上学路上：</strong>走人行道、牵大人的手；过马路看红绿灯、走斑马线；不追跑不打闹。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>国旗面前：</strong>国歌一响就停下手里的事，面向国旗立正站好，认真唱国歌。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>认认校园：</strong>教室上课、饮水处接水、卫生间课间去、操场活动、保健室不舒服就去、图书角借书。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>平安回家：</strong>家长还没来，就回到老师身边等，这是最安全的做法。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>还要记牢一件事：</strong>刚上小学，有一点紧张、有一点想念家里人，很多小朋友都会这样，你一点也不奇怪。慢慢地，学校会变成你熟悉的地方。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「安全、国旗、认得路」这三个词，说清楚你今天在学校做对的一件事。</p>
          <p style="color:var(--muted)">再动一动手：<strong>画一画</strong>从校门到你的教室，路上会经过哪些地方，把它们标在纸上。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "说出上学路上要注意的两件事，再说说为什么要注意它们。",
            "说出校园里三个常用的地方，分别说说它们是做什么用的。",
        ],
        [
            "和家里人一起走一遍从家到学校的路，把要过马路的地方指出来，说说应该看什么。",
            "把「升国旗时要怎么做」说给家里人听，请他们帮你检查有没有漏掉的。",
        ],
        [
            "画一张「我们的校园」图，把教室、饮水处、卫生间、操场、保健室、升旗广场都标出来，讲给同桌听。",
            "想一想：家里也有要注意安全的时候吗？挑一条写在纸上，说说为什么要这样做。",
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
    "title": "我是小学生啦",
    "name_en": "I Am a Primary School Student Now",
    "grade": 1,
    "grade_cn": "一年级",
    "domain": "moral-cultivation",
    "domain_cn": "道德修养",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学一年级新生的道德与法治起始课：从上学路上的安全做法开始，再到升国旗、奏国歌时庄重地站好行礼，接着认一认校园里每天都会去的地方，最后学会放学家长还没来时在老师身边等。全课只讲能看见、能做到的具体动作，帮助一年级学生适应小学生活、养成良好习惯，乐于与老师、同学交往。",
    "tags": ["我是小学生啦", "入学适应", "国旗礼仪", "校园安全", "一年级", "道德修养"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学「道德修养」——帮助学生适应小学生活，养成良好学习习惯和生活习惯，乐于与老师、同学交往；对应统编《道德与法治》一年级上册第一单元「我是小学生啦」：开开心心上学去、我向国旗敬个礼、这是我们的校园、平平安安回家来。",
    "hero_question": "第一天背起书包走进校门，该怎么做，才能开开心心上学去、平平安安回家来？",
    "hero_alt": "我是小学生啦知识结构图：开开心心上学去、我向国旗敬个礼、我们的校园与平安回家 三栏",
    "hero_caption": "我是小学生啦：开开心心上学去 · 我向国旗敬个礼 · 认认我们的校园 · 平平安安回家来",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "上学路上怎么走才安全？", "d": "过马路要看什么、和谁一起走", "v": "上学路上怎么走才安全"},
        {"t": "看到国旗升起来，我应该怎么做？", "d": "要站在哪里、眼睛看哪里", "v": "看到国旗升起来我应该怎么做"},
        {"t": "学校里都有哪些地方？", "d": "口渴了、不舒服了该去哪里", "v": "学校里都有哪些地方"},
        {"t": "放学了家长还没来，我该怎么办？", "d": "在哪里等最安全", "v": "放学了家长还没来我该怎么办"},
    ],
    "objectives": [
        "能说出上学路上和放学路上要注意的几件事，知道怎么做才安全",
        "知道国旗是我们国家的象征，升国旗、奏国歌时会停下手里的事，面向国旗立正站好、认真唱国歌",
        "能说出校园里几个常用的地方和它们的用处",
        "遇到不懂的、不确定的事情，知道可以问老师、问家长，心里有安全感",
    ],
    "objectives_plain": [
        "能说出上学路上和放学路上要注意的几件事，知道怎么做才安全",
        "知道国旗是我们国家的象征，升国旗、奏国歌时会停下手里的事，面向国旗立正站好、认真唱国歌",
        "能说出校园里几个常用的地方和它们的用处",
        "遇到不懂的、不确定的事情，知道可以问老师、问家长，心里有安全感",
    ],
    "standards": [
        {"content": "帮助学生适应小学生活，养成良好学习习惯和生活习惯，乐于与老师、同学交往",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学 道德修养"},
        {"content": "开开心心上学去；我向国旗敬个礼；这是我们的校园；平平安安回家来",
         "source": "统编《道德与法治》一年级上册 第一单元「我是小学生啦」"},
    ],
    "prereqs": [],
    "prereqs_name": "本课是小学道德与法治的起始课，不需要先修节点",
    "prereqs_meta": "",
    "leads_to": ["pol-e-g1-u2"],
    "next_meta": "pol-e-g1-u2",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "第一天背起书包走进校门，既高兴又有点紧张——今天先学四件能做到的小事。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能说出上学路上和校园里该怎么做。",
        "objectives": "看清四件事：路上安全、向国旗敬礼、认得校园、有事会问。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "出门检查书包、路上牵大人的手、过马路看灯走斑马线——小事做好了，一天就顺了。",
        "lab-1": "六件事，每件三个做法。选得不太合适也不会说你错，只会告诉你还可以试试什么。",
        "module-2": "国旗是国家的象征：国歌一响就停下、站好、面向国旗，认真唱国歌。认得路，心不慌。",
        "lab-2": "先点一件事，再点该去的地方。容易把饮水处和保健室搞混，看清楚再点。",
        "worked-example": "平平的四步：出门牵手走人行道、到校问好摆好书、升旗停下站好、放学在老师身边等。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "把七条放学路上的做法分进「安全」和「有危险」两个筐，分完读一读为什么。",
        "posttest": "出现了下雨天、陌生人和同学的邀请，看看你能不能把今天的办法用上去。",
        "summary": "四句话：上学路上、国旗面前、认认校园、平安回家。",
        "homework": "三层小任务，先做前两层，第三层可以请同桌一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学道德与法治「道德修养」的起始课，正对统编教材一年级上册第一单元「我是小学生啦」。一年级学生的难点不在理解道理，而在「知道该怎么做具体的一件事」——所以全课不讲抽象概念，只做四件能落地的事：路上安全（走人行道、牵大人的手、看红绿灯走斑马线）、国旗礼仪（国歌一响停下手里的事、面向国旗立正站好、认真唱国歌）、认得校园（教室、饮水处、卫生间、图书角、操场、保健室、升旗广场）、平安回家（家长还没来就回到老师身边等）。三个互动台子都能真的操作：一个是六张「校园一天」情境卡，选做法后给出即时反馈，反馈一律写成「这样可能会……，还可以试试……」，不判错、不贴标签；一个是「我们的校园」，把六件事和六个地方配对；一个是「平平安安回家来」，把六条做法分进「这样做安全／这样做有危险」两个筐。全课以具体动作收口，插图一律为中性简洁的教学示意图（极简线条人物，不使用真实儿童照片），涉及国旗、国歌的表述一律庄重得体。",
    "plan_table": """| 1 | cover | 我是小学生啦 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 开开心心上学去：路上的小事做好了，一天就顺了 | 承·概念一（上学路上与到校问好） |
| 6 | interactive | 动手一：校园一天，你会怎么做？ | 承·情境判断（温和反馈，不判错） |
| 7 | concept | 我向国旗敬个礼 · 认认我们的校园 | 承·概念二（国旗礼仪 + 认识校园） |
| 8 | interactive | 动手二：我们的校园，这是哪儿？ | 承·配对操作（六件事 → 六个地方） |
| 9 | concept | 例题示范：平平的第一天 | 转·重难点突破（分步示范 + 易错点） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：平平安安回家来，把做法分进两个筐 | 合·迁移应用（安全 / 有危险 分类） |
| 12 | quiz | 后测：换几个新情境，做法还在不在 | 合·后测 |
| 13 | summary | 小结：四句话，讲清小学生的一天 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：开开心心上学去 / 我向国旗敬个礼 / 我们的校园与平安回家 三栏\n- P5 上学路上示意图（已生成）：走人行道、过马路看红绿灯走斑马线、到校门口向老师问好，附中文标注\n- P7 校园常用地点示意图（已生成）：教室、饮水处、卫生间、图书角、操场、升旗广场，附中文标注\n- 三张图均为教学示意图，人物仅用极简线条，不使用任何真实儿童照片或可识别肖像\n- 涉及国旗、国歌的内容一律以文字庄重表述，不生成国旗图形，避免图形失真\n- 若需补充：本校校园平面图（需学校提供并授权后使用）",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
