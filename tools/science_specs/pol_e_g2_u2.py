# -*- coding: utf-8 -*-
"""小学道德与法治 · 我爱我们班（G2）—— 补齐知识树课标空缺节点

学科语气（道德与法治）：情境案例驱动，情感共鸣 + 价值判断；结论落在「应该怎么做、为什么」，
不做道德说教，也不做法条背诵。
二年级落点：全部换成能看见、能做到的具体动作——借东西先说一声、同学摔倒了扶一下、
值日一样一样做完再走、顺手捡起地上的纸。不讲抽象概念。
插图一律为中性简洁教学示意图，不使用真实人物照片。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g2-u2"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "小朋友，你每天在学校里待得最久的地方是哪里？是教室，是我们的班。班里有你的同桌、你的好朋友，也有和你不太熟的同学；有一起上过的课，也有一起参加过的活动。这节课我们就一起说一说：我们的班是什么样的；班里为什么要讲规则；轮到我做值日生，应该做些什么；我还能为我们的班做一件什么小事。想清楚这四件事，你会更明白——这个班，是我们大家的。",
    "problem-anchor": "开始之前，先选一个你最想弄清楚的问题。是想知道我们班有哪些让人喜欢的地方，还是想知道班里的规则到底是为了谁；是想知道值日生要做哪些事，还是想为班级做一件小事。选好了，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出我们班里几个让自己喜欢的地方，知道班级是大家一起生活的地方。第二，能说出班级生活里的几条规则，并说出遵守规则给全班带来的方便。第三，知道值日生要做哪些事，做值日时会一样一样认真做完，走之前再看一眼。第四，愿意为班级做一件力所能及的小事，知道我和我们班是连在一起的。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先一起看看我们的班。教室里有什么？有我们的座位、黑板、书柜，还有墙上的奖状。班里有什么人？有每天一起上课的同学，有教我们读书的老师。班里还有一起做过的事：一起上过的一节课，一起参加过的一次活动，一起打扫过的一次值日。这些东西凑在一起，就是我们的班。同学之间怎么相处呢？借东西先说一声，用完还回去；同学摔倒了，扶他一下；别人说话的时候，先听他说完；不给人起外号。这些事都很小，但正是它们，让教室待起来舒服。",
    "lab-1": "现在请你当一次班里的小主人。下面有六件在班里可能会遇到的事，每件事都有三个做法。你选一个你觉得合适的，选完立刻会有一段话告诉你为什么；要是选得不太合适，也会告诉你还可以试试什么。",
    "module-2": "接下来我们看三件事。第一件，班级生活有规则。上课要专心听讲，想说话先举手；课间在走廊里轻声慢步；借了东西要说一声再还回去；排队不插队。规则不是为了限制谁，是为了让全班都方便。第二件，我是班级值日生。值日要做这些事：扫地、擦黑板、摆好桌椅、倒垃圾、关灯关窗。一样一样做完，走之前再回头看一眼，有没有漏掉的地方。第三件，我为班级作贡献。贡献不一定很大：把自己的座位和抽屉收拾干净，顺手把地上的纸捡起来，同学有困难帮一把，参加班级活动，或者给班里提一个有用的建议。班级是我们每个人的，做一件小事，它就会好一点。",
    "lab-2": "接下来我们玩一个找家的小游戏。上面是六件在班里做的事，下面是三句话：班级规则、值日生的事、我为班级做的事。先点一件事，再点它属于哪一类。找对了会告诉你为什么，找错了也会提醒你再想一想。",
    "worked-example": "我们一起来看看小刚的值日生一天。第一步，看清任务：今天轮到小刚做值日，要做的是擦黑板、扫地、摆桌椅、倒垃圾、关灯关窗。第二步，想一想为什么：值日不是做给老师看的，是为了让全班同学第二天进来，有一个干干净净的教室。第三步，一样一样做完：先擦黑板，再扫地，桌椅摆整齐，最后倒垃圾，走的时候关灯关窗。第四步，做完再看一眼：走到门口回头看一看，地上还有没有纸屑，桌椅有没有歪。就是这样回头的一眼，让值日从做完变成了做好。",
    "conceptest-1": "接下来用三个说法考考你，每个说法里都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "下面有八条在班里可能会有的做法，请你判断一下：哪些是对班级好的做法，放进这一边；哪些需要调整，放进那一边。放好以后，再读一读为什么。",
    "posttest": "最后一轮，换几个新的小情境来考考你。这次会出现报名收作业、和同桌抢一本书、还有同学被起外号，看看你能不能用上今天学到的办法。",
    "summary": "这节课我们记住四句话。第一句，这是我们班：同学、老师，加上一起做过的事，凑在一起就是我们的班。第二句，班级生活有规则：规则不是限制谁，是为了让全班都方便。第三句，我是班级值日生：一样一样做完，走之前再看一眼，做完才算做好。第四句，我为班级作贡献：收拾好自己的座位、顺手捡起地上的纸、帮同学一把——班级是大家的，做一件小事，它就好一点。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出我们班里三个让你喜欢的地方，再说出值日生要做的三件事。第二层能力应用，动手做：轮到你的那一天，把值日认真做完，回家说说做完以后教室是什么样子；再找一件能为班级做的小事，做完以后告诉同桌。第三层迁移挑战，选做：和同学一起商量一条对班级有用的新建议，写下来交给老师；再观察一个星期，看看哪一条规则最有用，为什么。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 这是我们班", "lab-1": "动手一 班里遇到这样的事", "module-2": "概念二 规则 · 值日 · 贡献",
    "lab-2": "动手二 这三件事属于哪一类", "worked-example": "例题讲解 小刚的值日生一天", "conceptest-1": "概念测试",
    "synthesis": "综合任务 对班级好的做法 / 要调整的做法", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：班里遇到这样的事，六个情境 × 三个做法（反馈一律「这样可能会……还可以试试……」） ──
SCENES = [
    {
        "id": "s1",
        "t": "上课的时候，我很想和同桌说说昨天看的动画片",
        "opts": [
            {"k": "a", "t": "先记在心里，下课以后再和他说", "ok": True,
             "fb": "这个办法真好。上课专心听，下课再聊，两件事都不耽误。"},
            {"k": "b", "t": "小声和同桌说起来", "ok": False,
             "fb": "这样可能会让同桌也漏掉老师讲的内容，老师还要停下来提醒。还可以试试：把想说的话记在心里，下课再说。"},
            {"k": "c", "t": "写张纸条传过去", "ok": False,
             "fb": "这样可能会让周围的同学也跟着分心。还可以试试：先认真听课，下课把动画片的事一口气讲个够。"},
        ],
    },
    {
        "id": "s2",
        "t": "同学的新橡皮掉在地上，我捡到了",
        "opts": [
            {"k": "a", "t": "还给他，说一声「这是你的橡皮」", "ok": True,
             "fb": "做得真好。捡到东西还给同学，他心里会踏实，你心里也舒服。"},
            {"k": "b", "t": "先放进自己的笔盒里", "ok": False,
             "fb": "这样可能会让同学找不到自己的东西，还以为是丢了。还可以试试：马上还给他，说一声这是你的橡皮。"},
            {"k": "c", "t": "藏起来逗他玩一会儿", "ok": False,
             "fb": "这样可能会让同学着急，玩笑开过头就不太好了。还可以试试：直接还给他，想一起玩可以下课请他一起做游戏。"},
        ],
    },
    {
        "id": "s3",
        "t": "小组讨论的时候，我的想法和同学不一样",
        "opts": [
            {"k": "a", "t": "先听他说完，再说说我的想法", "ok": True,
             "fb": "这样商量真好。两个想法放在一起，常常能想出一个更好的办法。"},
            {"k": "b", "t": "马上打断他，说我的才对", "ok": False,
             "fb": "这样可能会让同学不想说了，讨论也停下来。还可以试试：等他说完，我再说——不一样的想法都值得听一听。"},
            {"k": "c", "t": "不说了，随便他吧", "ok": False,
             "fb": "这样可能会让小组少了一个好主意，你也会觉得没意思。还可以试试：把想法说出来，大家一起比一比。"},
        ],
    },
    {
        "id": "s4",
        "t": "同学生病请假，回来问我这两天讲了什么",
        "opts": [
            {"k": "a", "t": "把老师讲的重点讲给他听，不会的再一起问老师", "ok": True,
             "fb": "真热心。你帮他补上了课，自己讲一遍也更清楚了。"},
            {"k": "b", "t": "告诉他「你自己看书吧」", "ok": False,
             "fb": "这样可能会让他更着急，也不知道从哪里看起。还可以试试：先讲一两件最重要的，其他的陪他一起找。"},
            {"k": "c", "t": "装作没听见，先做自己的事", "ok": False,
             "fb": "这样可能会让同学觉得没人愿意帮他。还可以试试：先花几分钟讲一讲，课后再做自己的事也来得及。"},
        ],
    },
    {
        "id": "s5",
        "t": "我叫同学的时候，用了别人给他起的外号",
        "opts": [
            {"k": "a", "t": "叫他的姓名，好好和他说话", "ok": True,
             "fb": "这个做法很体贴。用姓名叫人，是最基本的尊重，同学听了会舒服。"},
            {"k": "b", "t": "觉得好玩，一直这么叫", "ok": False,
             "fb": "这样可能会让同学心里难过，只是他不好意思说。还可以试试：换成他的姓名，如果已经叫过了，可以跟他说一声对不起。"},
            {"k": "c", "t": "他不高兴了，就说他小气", "ok": False,
             "fb": "这样可能会让他更难受，两个人也容易闹起来。还可以试试：想一想如果别人这样叫我，我会是什么感觉。"},
        ],
    },
    {
        "id": "s6",
        "t": "做值日的时候，我发现角落里还有一点纸屑，可是已经下课了",
        "opts": [
            {"k": "a", "t": "把纸屑捡起来，把垃圾倒了再走", "ok": True,
             "fb": "做得真好。走之前多看一眼、多捡一下，第二天的教室就是干净的。"},
            {"k": "b", "t": "直接走人，反正已经扫过了", "ok": False,
             "fb": "这样可能会让那点纸屑留到明天，别人看到了还得再收拾。还可以试试：走之前回头看一眼，顺手就捡起来了。"},
            {"k": "c", "t": "把纸屑踢到桌子底下", "ok": False,
             "fb": "这样可能会让下一个值日的同学更麻烦。还可以试试：弯腰捡起来，这件事其实只要几秒钟。"},
        ],
    },
]

# ── 动手二：六件事 → 三句话（班级规则 / 值日生的事 / 我为班级做的事） ──
CATS = [
    {"id": "rule", "n": "班级规则", "use": "让全班都方便的事"},
    {"id": "duty", "n": "值日生的事", "use": "轮到值日时要做的"},
    {"id": "give", "n": "我为班级做的事", "use": "每个人都能做的小事"},
]
FEST_TASKS = [
    {"id": "t1", "t": "上课专心听讲，想说话先举手", "hid": "rule",
     "why": "这是班级的规则。大家都专心听，老师讲的内容才听得清，全班都受益。"},
    {"id": "t2", "t": "课间在走廊里轻声慢步，不追跑打闹", "hid": "rule",
     "why": "这也是班级的规则。走廊里人很多，慢一点走，就不会撞到别人。"},
    {"id": "t3", "t": "扫地、擦黑板、把桌椅摆整齐", "hid": "duty",
     "why": "这是值日生要做的事。一样一样做完，教室就干净整齐了。"},
    {"id": "t4", "t": "倒垃圾，走的时候关灯、关窗", "hid": "duty",
     "why": "这也是值日的一部分。最后这两下做完，值日才算真做完。"},
    {"id": "t5", "t": "把自己的座位和抽屉收拾干净", "hid": "give",
     "why": "这是每个人都能为班级做的事。自己的地方整齐了，整个教室就好看了。"},
    {"id": "t6", "t": "参加班级活动，给班里提一个有用的建议", "hid": "give",
     "why": "这也是为班级做的事。班级是我们每个人的，大家都出一份力，它就会更好。"},
]

# ── 综合任务：八条做法，分进两个筐 ──
SORT_ITEMS = [
    {"id": "k1", "t": "借同学的橡皮，先说一声，用完就还回去", "bin": "good",
     "why": "借东西说明白、还回去，同学下次还愿意借给你，这就是友善待人。"},
    {"id": "k2", "t": "同学摔倒了，扶他起来，问一问疼不疼", "bin": "good",
     "why": "扶一下、问一句，是班级里最暖的事，也是每个人都能做到的。"},
    {"id": "k3", "t": "做值日的时候，把黑板擦干净、桌椅摆整齐", "bin": "good",
     "why": "一样一样做完，全班第二天就有一个干净的教室。"},
    {"id": "k4", "t": "参加班级活动时认真准备，为班级出一份力", "bin": "good",
     "why": "班级是大家的。每个人都出一份力，班级的事才做得好。"},
    {"id": "k5", "t": "上课的时候和同桌小声聊天，反正老师没看见", "bin": "fix",
     "why": "老师没看见，可是你漏掉了老师讲的内容，同桌也没听好。上课的时间，专心听最划算。"},
    {"id": "k6", "t": "给同学起外号，觉得这样很好玩", "bin": "fix",
     "why": "好玩是别人的难受换来的。用姓名叫人，是最基本的尊重；如果已经叫过，可以对他说一声对不起。"},
    {"id": "k7", "t": "值日的时候随便扫两下，趁老师不在就先走了", "bin": "fix",
     "why": "值日不是做给老师看的，是做给全班用的。走之前回头看一眼，这一眼很值。"},
    {"id": "k8", "t": "看到地上有纸，绕过去，反正今天不是我值日", "bin": "fix",
     "why": "班级不是某个人的。顺手捡起来只要几秒钟，教室就一直是干净的。"},
]
SORT_BIN = {"good": "对班级好的做法", "fix": "要调整的做法"}

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g2-u2 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 班里遇到这样的事：六个情境 × 三个做法 → 温和反馈（不判错、不贴标签）
   3) 这三件事属于哪一类：六件事 → 三类
   4) 分进两个筐：八条做法 → 对班级好的做法 / 要调整的做法
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

  /* ---------- 2. 班里遇到这样的事 ---------- */
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
            out1.innerHTML = '<strong>这个做法挺好。</strong>' + o.fb;
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

  /* ---------- 3. 这三件事属于哪一类 ---------- */
  var TASKS = __FEST_JSON__;
  var CATS = __CATS_JSON__;
  var stage2 = document.getElementById('fest-stage');
  if (stage2) {
    var pickedTask = null, solved = {};
    var out2 = document.getElementById('fest-out');

    function catName(hid) {
      for (var i = 0; i < CATS.length; i++) { if (CATS[i].id === hid) return CATS[i].n; }
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
      document.getElementById('fest-score').textContent = '已经找对 ' + n + ' / ' + TASKS.length + ' 件事';
      var bank = document.getElementById('fest-done');
      bank.innerHTML = '';
      TASKS.forEach(function (t) {
        if (!solved[t.id]) return;
        var s = document.createElement('span');
        s.className = 'tag';
        s.textContent = t.t.slice(0, 10) + '… → ' + catName(t.hid);
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
        out2.innerHTML = '<strong>你遇到的这件事是：' + T.t + '</strong><br>想一想，它属于下面哪一类？点一点。';
        render2();
      });
    });
    document.querySelectorAll('[data-cat]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pickedTask) {
          out2.className = 'result warn';
          out2.textContent = '先在上面点一件事，再来选它属于哪一类。';
          return;
        }
        var T = null;
        for (var i = 0; i < TASKS.length; i++) { if (TASKS[i].id === pickedTask) T = TASKS[i]; }
        if (b.dataset.cat === T.hid) {
          solved[T.id] = true;
          out2.className = 'result';
          out2.innerHTML = '<strong>找对了，它属于「' + catName(T.hid) + '」。</strong>' + T.why;
          pickedTask = null;
          if (Object.keys(solved).length === TASKS.length) {
            out2.className = 'result';
            out2.innerHTML = '<strong>六件事全找对了！</strong>班级规则是为了让全班都方便，值日生的事要一样一样做完，为班级做的事每个人都能做——<strong>班级是大家的。</strong>';
          }
        } else {
          out2.className = 'result warn';
          out2.innerHTML = '<strong>好像不是这一类。</strong>你点的是「' + b.textContent + '」。' +
            '<br><span style="color:var(--muted)">常见错误：容易把「值日生的事」和「每个人都能做的小事」搞混——先想一想，这件事是轮到我值日才做的，还是谁都可以做的。</span>';
        }
        render2();
      });
    });
    render2();
  }

  /* ---------- 4. 分进两个筐 ---------- */
  var ITEMS = __SORT_JSON__;
  var BINN = __SORTBIN_JSON__;
  var stage3 = document.getElementById('sort-stage');
  if (stage3) {
    var pickItem = null, placed = {};
    var out3 = document.getElementById('sort-out');

    function render3() {
      document.querySelectorAll('[data-item]').forEach(function (b) {
        var k = b.dataset.item;
        b.classList.toggle('selected', k === pickItem);
        b.classList.toggle('done', !!placed[k]);
        b.disabled = !!placed[k];
      });
      var n = Object.keys(placed).length;
      document.getElementById('sort-score').textContent = '已经放好 ' + n + ' / ' + ITEMS.length + ' 条';
      var okBox = document.getElementById('sort-bin-good');
      var fixBox = document.getElementById('sort-bin-fix');
      okBox.innerHTML = ''; fixBox.innerHTML = '';
      ITEMS.forEach(function (it) {
        if (!placed[it.id]) return;
        var s = document.createElement('div');
        s.className = 'tag';
        s.textContent = it.t;
        (it.bin === 'good' ? okBox : fixBox).appendChild(s);
      });
      if (!okBox.innerHTML) okBox.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
      if (!fixBox.innerHTML) fixBox.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
    }
    document.querySelectorAll('[data-item]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (placed[b.dataset.item]) return;
        pickItem = b.dataset.item;
        out3.className = 'result warn';
        out3.innerHTML = '<strong>你选的是：' + b.textContent + '</strong><br>想一想，它是对班级好的做法，还是需要调整的做法？';
        render3();
      });
    });
    document.querySelectorAll('[data-sort-bin]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pickItem) {
          out3.className = 'result warn';
          out3.textContent = '先在上面点一条做法，再选筐。';
          return;
        }
        var it = null;
        for (var i = 0; i < ITEMS.length; i++) { if (ITEMS[i].id === pickItem) it = ITEMS[i]; }
        if (b.dataset.sortBin === it.bin) {
          placed[it.id] = true;
          out3.className = 'result';
          out3.innerHTML = '<strong>放对了，它属于「' + BINN[it.bin] + '」。</strong>' + it.why;
          pickItem = null;
          if (Object.keys(placed).length === ITEMS.length) {
            out3.className = 'result';
            out3.innerHTML = '<strong>八条全放对了！</strong>记一句小口诀：<strong>我的座位我收拾，班里的纸我捡起，同学的事我帮一把——班级是大家的。</strong>';
          }
        } else {
          out3.className = 'result warn';
          out3.innerHTML = '<strong>再想一想这条做法。</strong>' + it.why +
            '<br><span style="color:var(--muted)">常见错误：容易把「老师没看见」误认为「这样做就没关系」。班级里的事，看的是对全班好不好，不是有没有人看见。</span>';
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
             .replace('__FEST_JSON__', json.dumps(FEST_TASKS, ensure_ascii=False))
             .replace('__CATS_JSON__', json.dumps(CATS, ensure_ascii=False))
             .replace('__SORT_JSON__', json.dumps(SORT_ITEMS, ensure_ascii=False))
             .replace('__SORTBIN_JSON__', json.dumps(SORT_BIN, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "班里有一条规则：借同学的东西要先说一声。这条规则是为了：",
         "options": [("让大家的东西都有个数，借和还都清楚，全班都方便", True),
                     ("让老师管起来更省事", False),
                     ("规定谁可以借、谁不可以借", False)],
         "explain": "规则不是用来分出谁高谁低的，是让全班一起生活时都方便。"
                    "<strong>错因提醒：</strong>常见错误是误认为「规则就是老师管着我们」——想一想，如果大家都不说一声就拿走东西，你会是什么感觉。"},
        {"q": "教室里地上有几张纸，今天不是你做值日，你会：",
         "options": [("顺手捡起来，放进垃圾桶", True),
                     ("绕过去，反正不是我值日", False),
                     ("等做值日的同学来收拾", False)],
         "explain": "班级是大家的，每个人都能做一点。顺手捡一张纸只要几秒钟。"
                    "<strong>错因提醒：</strong>容易把「不是我值日」搞混成「和我没关系」——值日只是分工，班级是共有的。"},
        {"q": "有同学读课文时读错了一个字，旁边有人笑他，你会：",
         "options": [("不跟着笑，先听他读完，后面再一起帮他", True),
                     ("跟着笑一下，反正大家都在笑", False),
                     ("大声说他读错了，让全班都知道", False)],
         "explain": "同学读错了很正常，谁都会读错。不笑他、帮他一把，才是友善待人。"
                    "<strong>错因提醒：</strong>有人误认为「大家都在笑，我不笑显得不合群」——真正让人愿意待在一起的班级，是不拿别人开玩笑的班级。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "这是我们班：同学、老师，和一起做过的事", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">在家里，一起生活的是爸爸妈妈和我（And）；在学校里，每天和我待在一起的是一整个班的同学和老师（But）；这个班是怎么来的、我在这里能做点什么，值得好好想一想（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">每天走进教室，你会看到<strong>同样的座位、同样的同学</strong>。这些东西凑在一起，就是「我们的班」。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>我们班里有什么</strong></p>
            <p style="color:var(--muted)">我的座位、同桌、黑板和书柜、墙上的奖状；每天一起上课的同学，教我们读书的老师；还有一起上过的课、一起参加过的活动、一起打扫过的一次值日。</p>
          </div>
          <div class="inner-card">
            <p><strong>同学之间怎么相处</strong></p>
            <p style="color:var(--muted)">借东西先说一声，用完还回去；同学摔倒了，扶他一下；别人说话的时候，先听他说完；用姓名叫人，不给同学起外号。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="我们班示意图：我们的班、同学之间、一起做过的事 三栏，附中文标注">
          <figcaption>示意图：我们的班——教室里的人和物 · 同学之间的相处 · 一起做过的事（教学示意图，整体为中性简洁插画）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「班级是老师管的，跟我关系不大」。其实教室是全班一起用的：讲台上的粉笔灰、地上的一张纸、同桌看不清的黑板，都和我们每个人有关。班级不是某个人的，是我们大家的。</p>
        </div>
        <div class="kid-note"><span class="emoji">🏫</span><div><strong>记一句小口诀：</strong>这是我的同桌，这是我的老师，这是我们的班——<strong>班级是大家的。</strong></div></div>
{insight_box([
    {"lens": "看见它", "text": "一个班不是墙上的那张合影，而是每天发生的那些小事：谁帮谁捡了东西，谁和谁一起值日，谁被谁的笑话弄红了眼睛。"},
    {"lens": "解释它", "text": "为什么说班级是大家的？因为教室里的一切——黑板、地面、空气里的安静——都由全班每个人一起决定，一个人做得好一点，全班都好一点。"},
    {"lens": "迁移它", "text": "这样的相处方式不只用在班里：以后参加小组活动、和邻居相处、和家里人一起做事，用的都是同一套做法——有商量、有分寸、有帮忙。"},
])}
    ''', tag="概念一"))

    scene_btns = "\n".join(
        f'            <button class="choice" data-scene="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in SCENES
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：班里遇到这样的事，你会怎么做？", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一件在班里可能遇到的事，再从三个做法里选一个。<strong>选得好会告诉你为什么，选得不太合适也会告诉你还可以试试什么。</strong></p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 在班里，我遇到了这样一件事</div>
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
          <p class="result warn" id="day-out" style="margin-top:12px">先点一件在班里可能遇到的事。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💛</span><div><strong>说给你听：</strong>这里的做法没有「对」和「错」的分数。有些做法只是会让同学不太舒服，换一个试试就好。拿不准的时候，想一想：如果换成我，我希望别人怎么做？</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "班级生活有规则 · 我是班级值日生 · 我为班级作贡献", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">在班里生活，有三件事值得弄明白。它们看起来很小，天天做，一个班的样子就出来了。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>班级生活有规则：</strong>上课专心听讲、想说话先举手；课间在走廊里轻声慢步；借了东西先说一声再还回去；排队不插队。<strong>规则不是为了限制谁，是为了让全班都方便。</strong></div></div>
          <div class="step"><span class="n">2</span><div><strong>我是班级值日生：</strong>扫地、擦黑板、摆好桌椅、倒垃圾、关灯关窗。一样一样做完，<strong>走之前再回头看一眼</strong>，有没有漏掉的地方——做完，才算做好。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>我为班级作贡献：</strong>把自己的座位和抽屉收拾干净；顺手把地上的纸捡起来；同学有困难帮一把；参加班级活动；给班里提一个有用的建议。<strong>班级是我们每个人的。</strong></div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="值日生的一天与为班级做的小事示意图：擦黑板、扫地、摆桌椅、倒垃圾、关灯关窗，附中文标注">
          <figcaption>示意图：值日生的一天——擦黑板 · 扫地 · 摆好桌椅 · 倒垃圾 · 关灯关窗，走之前回头看一眼（教学示意图）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「值日是老师安排的任务，随便扫两下就算做了」。其实值日不是做给老师看的，是做给全班用的：第二天同学们进来，看到的是干净整齐的教室。所以走之前回头那一看，很值得。</p>
        </div>
        <div class="kid-note"><span class="emoji">🧹</span><div><strong>一句话记住它：</strong>规则让大家方便，值日让教室干净，贡献让班级更好——这三件事，每一件我都能做。</div></div>
{insight_box([
    {"lens": "看见它", "text": "规则、值日、贡献，都能化成具体的动作：举手、轻声走、先还回去、擦黑板、捡起一张纸。看不见的心意，要靠看得见的动作做出来。"},
    {"lens": "比较它", "text": "班级规则是全班一起守的，值日是有分工轮着做的，为班级作贡献是谁都可以做的。三件事不一样，但都在让班级变好。"},
    {"lens": "迁移它", "text": "换一个场合也一样：在图书馆、在公交车上、在小区里，都会有「大家都要守的」和「我可以多做一点的」。"},
])}
    ''', tag="概念二"))

    fest_task_btns = "\n".join(
        f'            <button class="choice" data-task="{t["id"]}" style="text-align:left">{t["t"]}</button>'
        for t in FEST_TASKS
    )
    fest_btns = "\n".join(
        f'            <button class="choice" data-cat="{c["id"]}" style="text-align:center">{c["n"]}</button>'
        for c in CATS
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：这三件事，属于哪一类？", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">上面是六件在班里做的事，下面是三句话。先点一件事，再点它属于哪一类。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 班里有人做了这样一件事</div>
          <div class="grid" id="fest-stage">
{fest_task_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 它属于哪一类</div>
          <div class="grid grid-3">
{fest_btns}
          </div>
          <div class="inner-card" style="margin-top:14px">
            <p><strong>我们找到的家</strong></p>
            <div id="fest-done" style="display:flex;flex-wrap:wrap;gap:6px"><span style="color:var(--muted);font-size:14px">还没有找对一件事。</span></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">闯关进度</span><span class="v" id="fest-score">已经找对 0 / 6 件事</span></div>
          </div>
          <p class="result warn" id="fest-out" style="margin-top:12px">先在上面点一件事。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔎</span><div><strong>拿不准就问自己一句：</strong>这件事是<strong>大家都得守</strong>的，还是<strong>轮到我值日才做</strong>的，或者<strong>谁都可以顺手做</strong>的？问完这一句，答案就清楚了。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小刚的值日生一天", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>今天轮到小刚做值日。下课铃响了，同学们都走光了，教室里只剩他一个。他应该怎么做？请你陪他一步一步想清楚。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看清任务：</strong>值日要做的是擦黑板、扫地、摆桌椅、倒垃圾、关灯关窗——不是只做其中一样。</div></div>
          <div class="step"><span class="n">2</span><div><strong>想一想为什么：</strong>值日不是做给老师看的，是为了让全班同学第二天进来，有一个干干净净的教室。</div></div>
          <div class="step"><span class="n">3</span><div><strong>一样一样做完：</strong>先擦黑板，再扫地，把桌椅摆整齐，然后倒垃圾，走的时候关灯关窗。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>做完再看一眼：</strong>走到门口回头看一看，地上还有没有纸屑、桌椅有没有歪——就是这一眼，让值日从「做完」变成了「做好」。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「值日就是扫两下地，老师不在就可以快点了事」。可是值日真正服务的是全班同学，不是老师。同样一件事，认真做和应付做，第二天教室的样子完全不同。</p>
        </div>
        <div class="inner-card">
          <p><strong>说给同桌听：</strong>小刚这四步里，哪一步你以前漏掉过？下次轮到你值日，你打算从哪一步开始做起来？</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "关于班级里的规则，下面哪个说法是对的？",
         "options": [("规则是为了让全班都方便，不是为了限制谁", True),
                     ("规则是老师用来管同学的", False),
                     ("规则只是写在墙上的，做不到也没关系", False)],
         "explain": "想一想借东西先说一声、走廊里轻声慢步，这些规则保护的是全班的方便。"
                    "<strong>错因提醒：</strong>常见错误是误认为「遵守规则是因为怕老师说」——规则真正管的是让大家都方便。"},
        {"q": "轮到同学做值日，可他今天生病请假了，你会：",
         "options": [("和另外几个同学一起帮他做完，回头看一眼再走", True),
                     ("他的值日跟我没关系，我自己走", False),
                     ("随便扫两下，能交差就行", False)],
         "explain": "同学有困难的时候帮一把，这就是班级在一起的意思。"
                    "<strong>错因提醒：</strong>容易误认为「分工就是各管各的」——分工是为了做事清楚，不是为了让谁落单。"},
        {"q": "关于「我为班级作贡献」，下面哪个做法最贴近？",
         "options": [("把自己的座位和抽屉收拾干净，顺手捡起地上的纸", True),
                     ("等哪天有大事，再为班级做一次大的", False),
                     ("在班里大声说出来，让老师知道我做了", False)],
         "explain": "贡献不一定很大，就是每天顺手能做的那几件小事。"
                    "<strong>错因提醒：</strong>有人误认为「做贡献要做得大、要让人看见」——真正的贡献，常常是没人看见也没关系的那种。"}
    ], tag="概念测试"))

    item_btns = "\n".join(
        f'            <button class="sort-item" data-item="{it["id"]}">{it["t"]}</button>' for it in SORT_ITEMS
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：八条做法，分进两个筐", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一条做法，再点它应该进的筐：<strong>对班级好的做法</strong>放一边，<strong>要调整的做法</strong>放另一边。</p>
        <div class="lab-panel">
          <div class="sort-bank" id="sort-stage">
{item_btns}
          </div>
          <div class="grid grid-2" style="margin-top:14px">
            <button class="choice" data-sort-bin="good" style="text-align:center">对班级好的做法</button>
            <button class="choice" data-sort-bin="fix" style="text-align:center">要调整的做法</button>
          </div>
          <div class="sort-bins">
            <div class="sort-bin" id="sort-bin-good"><h4>对班级好的做法</h4></div>
            <div class="sort-bin" id="sort-bin-fix"><h4>要调整的做法</h4></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">分类进度</span><span class="v" id="sort-score">已经放好 0 / 8 条</span></div>
          </div>
          <p class="result warn" id="sort-out" style="margin-top:12px">先在上面点一条做法。</p>
        </div>
        <div class="inner-card">
          <p><strong>分完之后，想一想：</strong></p>
          <p style="color:var(--muted)">要调整的做法里，有没有哪一条是「我以前做过」的？把它记下来，再说一说换成对班级好的做法，应该怎么做。</p>
          <textarea id="syn-answer" rows="3" placeholder="我以前做过……，换成对班级好的做法，我会……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，做法还在不在", TTS["posttest"], [
        {"q": "班里要选一位同学负责每天收作业。你想试试，可是有点怕做不好，你会：",
         "options": [("举手报名，做不好就问老师和同学", True),
                     ("不报，等以后有把握了再说", False),
                     ("报是报了，做的时候随手收一收", False)],
         "explain": "愿意为班级做一件事，本身就很好；不会的地方可以问、可以学。"
                    "<strong>错因提醒：</strong>常见错误是误认为「做不好就别做」——先把事情接过来，边做边学，比一直等着更有收获。"},
        {"q": "你和同桌都想看同一本课外书，你会：",
         "options": [("和他商量一下谁先看，看完就给对方", True),
                     ("我先拿到的，我先看完再说", False),
                     ("两个人一起看，谁也不让谁", False)],
         "explain": "商量一下，两个人都能看到，比抢来抢去好得多。"
                    "<strong>错因提醒：</strong>容易误认为「我先拿到就归我」——东西是大家的，商量才是班级里的做法。"},
        {"q": "有同学在班里被起了外号，他很难受，你会：",
         "options": [("不跟着叫，劝一劝；如果他还很难受，告诉老师", True),
                     ("不关我的事，装作没听见", False),
                     ("跟着叫两声，反正大家都在叫", False)],
         "explain": "不跟着叫，是友善待人的底线；再劝一劝、请老师帮一帮，就是替同学做了一件大事。"
                    "<strong>错因提醒：</strong>有人误认为「我又没先叫，跟我没关系」——旁边的人跟着叫，就是让这件事继续下去。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：四句话，讲清我们的班", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>这是我们班：</strong>同学的座位、老师、一起上过的课、一起做过的事，凑在一起就是我们的班。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>班级生活有规则：</strong>专心听讲、轻声慢步、借东西先说一声——规则不是限制谁，是为了让全班都方便。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>我是班级值日生：</strong>擦黑板、扫地、摆桌椅、倒垃圾、关灯关窗；一样一样做完，走之前再看一眼。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>我为班级作贡献：</strong>收拾好自己的座位、顺手捡起一张纸、帮同学一把——班级是大家的，做一件小事，它就好一点。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那个问题：</strong>为什么说「这是我们班」？因为班里的黑板、地面、安静和笑声，都由我们每个人一起决定。我做好一点，我们班就好一点。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「我们班、规则、值日」这三个词，说清楚一件你明天就能为班级做的小事。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "说出我们班里三个让你喜欢的地方，再说说为什么喜欢。",
            "说出值日生要做的三件事，并说说走之前为什么要回头看一眼。",
        ],
        [
            "轮到你值日的那一天，把值日认真做完，回家说说做完以后教室是什么样子。",
            "找一件能为班级做的小事做一做（收拾抽屉、捡起地上的纸、帮同学一把），做完以后告诉同桌。",
        ],
        [
            "和同学一起商量一条对班级有用的新建议，写下来交给老师，说说为什么这条建议有用。",
            "观察一个星期：班里哪一条规则最有用？它是为谁带来方便的？说给家人听。",
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
    "title": "我爱我们班",
    "name_en": "I Love Our Class",
    "grade": 2,
    "grade_cn": "二年级",
    "domain": "tradition-culture",
    "domain_cn": "中华优秀传统文化",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学二年级的道德与法治课：从「这是我们班」开始，看见班里的人和一起做过的事；再认识班级规则、值日生的工作、以及每个人都能为班级做的小事；最后学会用合适的做法和同学相处。全课只讲能看见、能做到的具体动作，把价值判断落在「应该怎么做、为什么」上，不做道德说教，也不做法条背诵。",
    "tags": ["我爱我们班", "班级规则", "值日生", "为班级作贡献", "集体意识", "二年级"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学——诚实守信，友善待人，有集体意识和责任感；对应统编《道德与法治》二年级上册「我爱我们班」单元：这是我们班、班级生活有规则、我是班级值日生、我为班级作贡献。",
    "hero_question": "我们班有那么多同学，为什么说「这是我们班」？",
    "hero_alt": "我爱我们班知识结构图：这是我们班、班级规则、值日与贡献 三栏",
    "hero_caption": "我爱我们班：这是我们班 · 班级生活有规则 · 我是班级值日生 · 我为班级作贡献",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "我们班有哪些让我喜欢的地方？", "d": "同学、老师，还有一起做过的事", "v": "我们班有哪些让我喜欢的地方"},
        {"t": "班级生活里有哪些规则？为什么要遵守？", "d": "规则到底是为了谁", "v": "班级生活里有哪些规则为什么要遵守"},
        {"t": "值日生要做哪些事？", "d": "一样一样都做些什么", "v": "值日生要做哪些事"},
        {"t": "我能为班级做一件什么小事？", "d": "从最小的一件开始", "v": "我能为班级做一件什么小事"},
    ],
    "objectives": [
        "能说出我们班里几个让自己喜欢的地方，知道班级是大家一起生活的地方",
        "能说出班级生活里的几条规则，并说出遵守规则给全班带来的方便",
        "知道值日生要做哪些事，做值日时会一样一样认真做完，走之前再看一眼",
        "愿意为班级做一件力所能及的小事，知道「我」和「我们班」是连在一起的",
    ],
    "objectives_plain": [
        "能说出我们班里几个让自己喜欢的地方，知道班级是大家一起生活的地方",
        "能说出班级生活里的几条规则，并说出遵守规则给全班带来的方便",
        "知道值日生要做哪些事，做值日时会一样一样认真做完，走之前再看一眼",
        "愿意为班级做一件力所能及的小事，知道「我」和「我们班」是连在一起的",
    ],
    "standards": [
        {"content": "诚实守信，友善待人，有集体意识和责任感",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学 道德修养"},
        {"content": "这是我们班；班级生活有规则；我是班级值日生；我为班级作贡献",
         "source": "统编《道德与法治》二年级上册「我爱我们班」单元"},
    ],
    "prereqs": ["pol-e-g2-u1"],
    "prereqs_name": "过好节假日",
    "prereqs_meta": "pol-e-g2-u1",
    "leads_to": ["pol-e-g2-u3"],
    "next_meta": "pol-e-g2-u3",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "每天在学校待得最久的地方就是我们的班——今天先弄清楚「这个班和我有什么关系」。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能说出自己明天就能为班级做的一件小事。",
        "objectives": "看清四件事：认识我们班、懂班级规则、会做值日、愿意为班级做一点。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "同学、老师、一起上过的课和一起做过的事，凑在一起就是我们的班。",
        "lab-1": "六件事，每件三个做法。选得不太合适也不会说你错，只会告诉你还可以试试什么。",
        "module-2": "规则是让全班方便，值日要一样一样做完再回头看一眼，贡献就是每天顺手能做的小事。",
        "lab-2": "先点一件事，再点它属于哪一类。容易把值日和贡献搞混，看清楚再点。",
        "worked-example": "小刚四步：看清任务、想想为什么、一样一样做完、做完再看一眼。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "八条做法分进「对班级好的做法」和「要调整的做法」两个筐，分完读一读为什么。",
        "posttest": "出现了报名收作业、和同桌抢一本书、还有同学被起外号，看看你能不能把办法用上去。",
        "summary": "四句话：这是我们班、班级有规则、我是值日生、我为班级作贡献。",
        "homework": "三层小任务，先做前两层，第三层可以和同学一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课正对统编教材二年级上册「我爱我们班」单元，补知识树中「集体意识与责任感」这一空缺。二年级学生的难点不是听不懂道理，而是不知道「具体该怎么做」——所以全课不讲抽象概念，只做四件能落地的事：这是我们班（同学、老师、一起上过的课、一起做过的事）、班级生活有规则（专心听讲、轻声慢步、借东西先说一声，规则是为了让全班都方便）、我是班级值日生（擦黑板、扫地、摆桌椅、倒垃圾、关灯关窗，走之前再看一眼）、我为班级作贡献（收拾好自己的座位、顺手捡起一张纸、帮同学一把）。三个互动台子都能真的操作：一个是六张「班里遇到这样的事」情境卡，选做法后立刻展开后果（「这样可能会……，还可以试试……」），不判错、不贴标签；一个是「这三件事，属于哪一类」，把六件事配到班级规则／值日生的事／我为班级做的事；一个是「八条做法，分进两个筐」，把做法分进「对班级好的做法／要调整的做法」。全课以具体动作收口，插图一律为中性简洁教学示意图，不使用真实人物照片。",
    "plan_table": """| 1 | cover | 我爱我们班 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 这是我们班：同学、老师，和一起做过的事 | 承·概念一（班级认同） |
| 6 | interactive | 动手一：班里遇到这样的事，你会怎么做？ | 承·情境判断（选做法 → 展开后果，不判错） |
| 7 | concept | 班级生活有规则 · 我是班级值日生 · 我为班级作贡献 | 承·概念二（规则 / 值日 / 贡献） |
| 8 | interactive | 动手二：这三件事，属于哪一类？ | 承·配对操作（六件事 → 三类） |
| 9 | concept | 例题示范：小刚的值日生一天 | 转·重难点突破（分步示范 + 易错点） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：八条做法，分进两个筐 | 合·迁移应用（对班级好 / 要调整 分类） |
| 12 | quiz | 后测：换几个新情境，做法还在不在 | 合·后测 |
| 13 | summary | 小结：四句话，讲清我们的班 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：这是我们班 / 班级生活有规则 / 值日与贡献 三栏，附中文标注\n- P5 我们班示意图（已生成）：教室里的人和物 · 同学之间的相处 · 一起做过的事，附中文标注\n- P7 值日生的一天示意图（已生成）：擦黑板、扫地、摆好桌椅、倒垃圾、关灯关窗，附中文标注\n- 三张图均为中性简洁教学示意图，不使用任何真实人物照片或可识别肖像\n- 若需补充：本班教室平面图、班级活动照片（需家长与学校授权后使用）",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
