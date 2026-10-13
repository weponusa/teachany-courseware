# -*- coding: utf-8 -*-
"""小学道德与法治 · 过好节假日（G2）—— 补齐知识树「道德修养」空缺

学科语气（道德与法治）：情境案例驱动，情感共鸣 + 价值判断；结论落在「应该怎么做、为什么」，
不做道德说教，也不做法条背诵。
二年级落点：全部换成能看见、能做到的具体做法——假期怎么排、教师节说什么做什么、
中秋节的晚上一家人怎么过、国庆节怎么表达祝福。不讲抽象概念，不要求背诵。
涉及国旗、国歌的表述一律庄重得体：看到升国旗，停下手里的事、立正站好、认真唱国歌。
插图一律为中性简洁教学示意图，不使用真实人物照片。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g2-u1"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "小朋友，一说到放假，你是不是特别高兴？可是有的同学放假回来会说：假期好像什么也没做，就过去了。这节课我们就一起来想一想，怎样把节假日过好。我们自己要聊四件事：假期里怎么安排，才能又开心又有收获；教师节快到了，怎样向老师表达感谢；中秋节一家人在一起，可以做些什么；国庆节放假，我们怎样表达对祖国的祝福。想清楚这四件事，你的假期就不会白过。",
    "problem-anchor": "开始之前，先选一个你最想弄清楚的问题。是想知道假期怎么安排才不浪费，还是想给老师表达一次感谢；是想知道中秋节的晚上一家人可以做什么，还是想知道国庆节我们能做点什么。选好了，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出假期里可以做的几件有意义的事，会给自己排一份假期一天的小计划。第二，知道教师节是感谢老师的日子，会用一句真心的话或者一个小行动表达感谢。第三，能说出中秋节团圆的习俗，愿意和家人一起过节。第四，知道国庆节是庆祝祖国生日的日子，会用庄重又具体的方式表达祝福。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先来说假期。放假不等于什么都不做，也不等于整天赶作业，而是把要做的和想做的都安排好。有个很好用的办法：早上起来想一想，今天最想做的一件事是什么，先把它写下来。然后先把要做的做完，比如写作业、整理书桌；再去做想做的，比如看一本喜欢的书、和同学一起玩、学一样小本领。玩的时候放心玩，累的时候就歇一歇，也别忘了让眼睛休息一会儿。这样一天过完，你会觉得这一天很满。",
    "lab-1": "现在请你当一次小小的生活策划师。下面有六件在节假日里可能会遇到的事，每件事都有三个做法。你选一个你觉得合适的，选完立刻会有一段话告诉你为什么；要是选得不太合适，也会告诉你还可以试试什么。",
    "module-2": "接下来我们认识三个节日。第一个是教师节。教师节是感谢老师的日子，感谢不一定要送贵重的东西：一句真心的话、一张自己画的小卡片、上课认真听讲、把作业认真写好，都是很好的感谢。第二个是中秋节。中秋节的晚上，一家人一起吃月饼、一起看看月亮，听爷爷奶奶讲讲他们小时候是怎么过中秋的，也可以给不在身边的亲人打个电话，问一声好。团圆不是人坐在一起就算，而是人在一起，心也在一起。第三个是国庆节。国庆节是庆祝祖国生日的日子。我们可以和家人一起看庆祝活动的节目，说一说身边这几年的新变化，看到升国旗就停下手里的事、立正站好、认真唱国歌。表达祝福要用庄重的方式，不喧闹、不打闹。",
    "lab-2": "接下来我们玩一个找家的小游戏。上面是六件在节假日里做的事，下面是三个节日：教师节、中秋节、国庆节。先点一件事，再点它属于哪个节日。找对了会告诉你为什么，找错了也会提醒你再想一想。",
    "worked-example": "我们一起来帮小美想一想。中秋节那天晚上，爷爷奶奶来了，妈妈在准备月饼和水果，小美正在看动画片，正好看到最精彩的地方。第一步，看清情境：一家人在等她，动画片明天还能看。第二步，想一想为什么：中秋是团圆的节日，一家人凑在一起的时间并不多，错过去就要等下一年。第三步，选一个合适的做法：先把动画片暂停，出来和大家一起吃月饼，请爷爷讲讲他小时候过中秋的事。第四步，还可以怎样：吃完月饼给外婆打个电话，说一声节日快乐，祝她身体健康。",
    "conceptest-1": "接下来用三个说法考考你，每个说法里都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "下面有八条关于节假日的做法，请你判断一下：哪些做法是合适的，放进合适的做法这一边；哪些做法需要调整，放进要调整的做法那一边。放好以后，再读一读为什么。",
    "posttest": "最后一轮，换几个新的小情境来考考你。这次会出现寒假、重阳节看望外婆、还有假期最后一天的作业，看看你能不能用上今天学到的办法。",
    "summary": "这节课我们记住四句话。第一句，假期有收获：先做要做的，再做想做的，玩和休息搭着来。第二句，教师节快乐：一句真心的话、一个小行动，感谢在心里，不在礼物有多贵。第三句，团团圆圆过中秋：一家人一起吃月饼、赏月、听长辈讲过去的事，人在一起，心也在一起。第四句，欢欢喜喜庆国庆：和家人一起看庆祝活动，看到升国旗就停下站好、认真唱国歌，用庄重的方式祝祖国生日快乐。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出假期里可以做的三件事，再说说中秋节的晚上一家人可以一起做什么。第二层能力应用，动手做：和家人一起排一份假期一天的小计划，第二天照着做，晚上说一说哪一件做到了；再给老师写一句感谢的话，或者画一张小卡片。第三层迁移挑战，选做：采访一位长辈，问问他小时候是怎么过中秋或者过年的，把听到的记下来讲给同学听。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 假期有收获", "lab-1": "动手一 节假日里的一天", "module-2": "概念二 教师节 · 中秋 · 国庆",
    "lab-2": "动手二 三个节日，各自的心意", "worked-example": "例题讲解 小美家的中秋节", "conceptest-1": "概念测试",
    "synthesis": "综合任务 合适的做法 / 要调整的做法", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：节假日里的一天，六个情境 × 三个做法（反馈一律「这样可能会……还可以试试……」） ──
SCENES = [
    {
        "id": "s1",
        "t": "放长假的第一天早上，我醒得比平时晚了一点",
        "opts": [
            {"k": "a", "t": "和家人一起商量，把作业和玩的时间都安排好", "ok": True,
             "fb": "这样安排真好。先把要做的和想做的都说清楚，这个假期你心里就有底了。"},
            {"k": "b", "t": "先不管它，作业留到假期最后一天再说", "ok": False,
             "fb": "这样可能会让最后一天特别着急，写也写不安心。还可以试试：每天留一点时间写一点，写完再去玩。"},
            {"k": "c", "t": "一睁眼就打开电视，看到中午", "ok": False,
             "fb": "这样可能会让一整天很快就过去了，眼睛也会累。还可以试试：先做一件要做的，再看一会儿电视。"},
        ],
    },
    {
        "id": "s2",
        "t": "假期里，作业还剩一点没写完，同学来叫我出去玩",
        "opts": [
            {"k": "a", "t": "先把剩下的写完，再去找同学玩", "ok": True,
             "fb": "这个办法真好。写的时候专心写，玩的时候就能痛痛快快地玩，两件事都不耽误。"},
            {"k": "b", "t": "先出去玩，作业回来再说", "ok": False,
             "fb": "这样可能会让你玩的时候还惦记着作业，回家又得赶。还可以试试：把剩下的先写完，再出去玩，玩得更轻松。"},
            {"k": "c", "t": "让同学帮我写一点", "ok": False,
             "fb": "这样可能会让同学为难，你自己的功课也补不上。还可以试试：告诉同学等我一会儿，我写完就出来。"},
        ],
    },
    {
        "id": "s3",
        "t": "教师节快到了，我想向老师表达感谢",
        "opts": [
            {"k": "a", "t": "画一张小卡片，写上一句真心的话，上课认真听讲", "ok": True,
             "fb": "真有心意。一句真心的话、一张自己画的卡片，老师收到会很高兴；认真做好每一件事，是最好的感谢。"},
            {"k": "b", "t": "请家里人买一份很贵的礼物送给老师", "ok": False,
             "fb": "这样可能会给家里添负担，也和感谢的本意不太一样。还可以试试：用自己的手做一张卡片，说一句真心的话。"},
            {"k": "c", "t": "上课的时候大声喊「老师节日快乐」，别的同学还在听讲", "ok": False,
             "fb": "这样可能会打断老师上课，旁边的同学也听不清。还可以试试：下课以后，走到老师身边轻轻地说一声。"},
        ],
    },
    {
        "id": "s4",
        "t": "中秋节晚上，一家人坐在一起",
        "opts": [
            {"k": "a", "t": "和爷爷奶奶一起吃月饼，听他们讲小时候过中秋的事", "ok": True,
             "fb": "这个晚上真有味道。月饼是甜的，长辈的故事更珍贵——这就是团圆的样子。"},
            {"k": "b", "t": "一个人回房间里玩手机", "ok": False,
             "fb": "这样可能会让你错过一家人难得坐在一起的这个晚上。还可以试试：先出来和大家一起吃月饼，晚一点再玩。"},
            {"k": "c", "t": "只顾着抢最大的那一块月饼", "ok": False,
             "fb": "这样可能会让旁边的人心里不太舒服，节日的味道也淡了。还可以试试：把月饼分成小块，一人一块，先递给长辈。"},
        ],
    },
    {
        "id": "s5",
        "t": "国庆节放假，家里商量这几天怎么过",
        "opts": [
            {"k": "a", "t": "和家人一起看庆祝活动的节目，说说身边这几年的新变化", "ok": True,
             "fb": "这个安排很有意义。看一看、说一说，你会更明白国庆节是给谁过生日。"},
            {"k": "b", "t": "什么也不用做，反正只是多放了几天假", "ok": False,
             "fb": "这样可能会让国庆节和平常的休息日没什么两样。还可以试试：和家人一起看一看庆祝活动，说说祖国的变化。"},
            {"k": "c", "t": "在小区里一边跑一边大声喊，闹个不停", "ok": False,
             "fb": "这样可能会吵到别人，也不够庄重。还可以试试：把高兴放在心里，和家人一起用安静又认真的方式庆祝。"},
        ],
    },
    {
        "id": "s6",
        "t": "假期里，同学说他去了很远的地方玩，我心里有点羡慕",
        "opts": [
            {"k": "a", "t": "和爸爸妈妈说说自己的想法，一起商量一次全家的出行", "ok": True,
             "fb": "这个办法很成熟。把心里的话说出来，一家人一起商量，比憋在心里好得多。"},
            {"k": "b", "t": "一定要家里也带我去一样远的地方", "ok": False,
             "fb": "这样可能会让家里人很为难。还可以试试：说出你的想法，再一起商量一个家里能安排的出行。"},
            {"k": "c", "t": "生闷气，不理家里人", "ok": False,
             "fb": "这样可能会让家里人不知道你在想什么，你也一直不高兴。还可以试试：先说出来，再说说你想怎么做。"},
        ],
    },
]

# ── 综合任务：八条节假日做法，分进两个筐 ──
SORT_ITEMS = [
    {"id": "k1", "t": "放长假先和家人一起商量，把作业和玩的时间都安排好", "bin": "ok",
     "why": "先说清楚、再安排，做起来就不慌，假期也不容易白白过去。"},
    {"id": "k2", "t": "每天留一点时间写作业，写完再出门玩", "bin": "ok",
     "why": "每天做一点，最后一天就不用赶；玩的时候心里也踏实。"},
    {"id": "k3", "t": "教师节给老师画一张小卡片，写上一句真心的话", "bin": "ok",
     "why": "用自己的手做出来的东西最真诚，感谢在心里，不在礼物有多贵。"},
    {"id": "k4", "t": "中秋节晚上和爷爷奶奶一起吃月饼，听他们讲讲小时候的事", "bin": "ok",
     "why": "一家人围在一起，说说话、听听故事，这就是中秋节说的团圆。"},
    {"id": "k5", "t": "国庆节和家人一起看庆祝活动，说说身边这几年的新变化", "bin": "ok",
     "why": "国庆节是给祖国过生日。看一看、说一说，是我们表达祝福的方式。"},
    {"id": "k6", "t": "假期里每天玩手机玩到很晚，作业堆到最后一晚上赶", "bin": "fix",
     "why": "这样会把身体累坏，作业也写不好。把时间分一分：玩一会儿，歇一会儿，留一点给要完成的事。"},
    {"id": "k7", "t": "过节的时候嫌爷爷奶奶说话慢，自己回房间玩去了", "bin": "fix",
     "why": "长辈想和我们说说话。慢一点没关系，听他们说完，这个节日才更有温度。"},
    {"id": "k8", "t": "听同学说家里买了很贵的礼物，就吵着一定要家里也买", "bin": "fix",
     "why": "心意不是用价钱来比的。一句真心的话、一件自己动手做的小东西，一样能表达感谢。"},
]
SORT_BIN = {"ok": "合适的做法", "fix": "要调整的做法"}

# ── 动手二：三个节日，各自的心意（六件事 → 三个节日） ──
HOLIDAYS = [
    {"id": "teacher", "n": "教师节", "use": "感谢老师的日子"},
    {"id": "moon", "n": "中秋节", "use": "一家人团圆的日子"},
    {"id": "national", "n": "国庆节", "use": "庆祝祖国生日的日子"},
]
FEST_TASKS = [
    {"id": "t1", "t": "我画了一张小卡片，写上一句真心的话，送给老师", "hid": "teacher",
     "why": "感谢老师，重在心里：一句真心的话、一张自己动手做的卡片，老师收到会很高兴。"},
    {"id": "t2", "t": "上课认真听讲，把作业认真写好，让老师放心", "hid": "teacher",
     "why": "认真上好每一节课，是对老师最好的感谢，也是送给老师最好的礼物。"},
    {"id": "t3", "t": "一家人一起吃月饼、看月亮，听爷爷讲他小时候过中秋的事", "hid": "moon",
     "why": "中秋节最珍贵的就是一家人聚在一起，说说过去的事——这就是团圆。"},
    {"id": "t4", "t": "给不在身边的亲人打个电话，问一声好，祝他身体健康", "hid": "moon",
     "why": "团圆也可以隔着电话。一句问候，把不在身边的人也拉进了这个节日里。"},
    {"id": "t5", "t": "和家人一起看庆祝活动的节目，说说身边这几年的新变化", "hid": "national",
     "why": "国庆节是庆祝祖国生日的日子。看一看、说一说，就是我们表达祝福的方式。"},
    {"id": "t6", "t": "看到升国旗，停下手里的事，立正站好，认真唱国歌", "hid": "national",
     "why": "国旗是我们国家的象征。看到升国旗停下来站好、认真唱国歌，是一件很庄重的事。"},
]

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g2-u1 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 节假日里的一天：六个情境 × 三个做法 → 温和反馈（不判错、不贴标签）
   3) 分进两个筐：八条做法 → 合适的做法 / 要调整的做法
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

  /* ---------- 2. 节假日里的一天 ---------- */
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

  /* ---------- 3. 三个节日：六件事 → 三个节日 ---------- */
  var TASKS = __FEST_JSON__;
  var HOLIDAYS = __HOLIDAYS_JSON__;
  var stage2 = document.getElementById('fest-stage');
  if (stage2) {
    var pickedTask = null, solved = {};
    var out2 = document.getElementById('fest-out');

    function holidayName(hid) {
      for (var i = 0; i < HOLIDAYS.length; i++) { if (HOLIDAYS[i].id === hid) return HOLIDAYS[i].n; }
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
        s.textContent = t.t.slice(0, 10) + '… → ' + holidayName(t.hid);
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
        out2.innerHTML = '<strong>你遇到的这件事是：' + T.t + '</strong><br>想一想，它是哪个节日的做法？点一点下面。';
        render2();
      });
    });
    document.querySelectorAll('[data-holiday]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pickedTask) {
          out2.className = 'result warn';
          out2.textContent = '先在上面点一件事，再来选节日。';
          return;
        }
        var T = null;
        for (var i = 0; i < TASKS.length; i++) { if (TASKS[i].id === pickedTask) T = TASKS[i]; }
        if (b.dataset.holiday === T.hid) {
          solved[T.id] = true;
          out2.className = 'result';
          out2.innerHTML = '<strong>找对了，这是' + holidayName(T.hid) + '的做法。</strong>' + T.why;
          pickedTask = null;
          if (Object.keys(solved).length === TASKS.length) {
            out2.className = 'result';
            out2.innerHTML = '<strong>六件事全找对了！</strong>教师节说感谢，中秋说团圆，国庆说祝福——<strong>日子不一样，心意也不一样。</strong>';
          }
        } else {
          out2.className = 'result warn';
          out2.innerHTML = '<strong>好像不是这个节日。</strong>你点的是「' + b.textContent + '」。' +
            '<br><span style="color:var(--muted)">常见错误：容易把「感谢老师」和「庆祝祖国生日」搞混——先想一想，这件事是在对谁表达心意。</span>';
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
      var okBox = document.getElementById('sort-bin-ok');
      var fixBox = document.getElementById('sort-bin-fix');
      okBox.innerHTML = ''; fixBox.innerHTML = '';
      ITEMS.forEach(function (it) {
        if (!placed[it.id]) return;
        var s = document.createElement('div');
        s.className = 'tag';
        s.textContent = it.t;
        (it.bin === 'ok' ? okBox : fixBox).appendChild(s);
      });
      if (!okBox.innerHTML) okBox.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
      if (!fixBox.innerHTML) fixBox.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
    }
    document.querySelectorAll('[data-item]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (placed[b.dataset.item]) return;
        pickItem = b.dataset.item;
        out3.className = 'result warn';
        out3.innerHTML = '<strong>你选的是：' + b.textContent + '</strong><br>想一想，它是合适的做法，还是需要调整的做法？';
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
            out3.innerHTML = '<strong>八条全放对了！</strong>记一句小口诀：<strong>先做要做的，再做想做的；过节一家人，人在心也在。</strong>';
          }
        } else {
          out3.className = 'result warn';
          out3.innerHTML = '<strong>再想一想这条做法。</strong>' + it.why +
            '<br><span style="color:var(--muted)">常见错误：容易把「省事、痛快」误认为「合适的做法」。合适的做法要看做完以后，自己、家人和周围的人是不是都还好。</span>';
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
             .replace('__HOLIDAYS_JSON__', json.dumps(HOLIDAYS, ensure_ascii=False))
             .replace('__SORT_JSON__', json.dumps(SORT_ITEMS, ensure_ascii=False))
             .replace('__SORTBIN_JSON__', json.dumps(SORT_BIN, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "放长假了，下面哪种安排更合适？",
         "options": [("先做要做的，再做想做的，玩和休息搭着来", True),
                     ("先把作业放到一边，玩到最后一天再说", False),
                     ("每天睡到中午，剩下的时间都看电视", False)],
         "explain": "把要做的先做完，玩的时候才能安心玩，假期也过得满。"
                    "<strong>错因提醒：</strong>常见错误是误认为「放假就是什么都不用安排」——假期不安排，很容易一转眼就过完了。"},
        {"q": "教师节到了，下面哪种表达感谢的方式最合适？",
         "options": [("自己画一张小卡片，写上一句真心的话，上课认真听讲", True),
                     ("请家里人买一份很贵的礼物送给老师", False),
                     ("上课时突然大声喊「老师节日快乐」", False)],
         "explain": "感谢老师，靠的是真心和行动：一句真心的话、一件自己动手做的小东西、认真上好每一节课。"
                    "<strong>错因提醒：</strong>有人误认为「礼物越贵越有诚意」——其实心意不是用价钱来比的。"},
        {"q": "中秋节说的「团圆」，是什么意思？",
         "options": [("一家人在一起，人在一起，心也在一起", True),
                     ("一定要吃到最大的那块月饼", False),
                     ("只要放假不用上学就算团圆", False)],
         "explain": "中秋节是一家人聚在一起的日子：一起吃月饼、一起看看月亮、听长辈说说过去的事。"
                    "<strong>错因提醒：</strong>容易把「团圆」和「放假玩个痛快」搞混——团圆说的是人聚在一起、心里想着彼此。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "假期有收获：先做要做的，再做想做的", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">平时的日子，什么时候上课、什么时候写作业，都是学校排好的（And）；可是到了假期，时间全都交给你自己，想怎么过就怎么过（But）；所以要先学会给假期做个小安排，不然一天天过去，回头想不起来做过什么（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">放假<strong>不等于什么都不做</strong>，也不等于整天赶作业。真正过得好的假期，是<strong>要做的</strong>和<strong>想做的</strong>都安排上了。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>假期里可以做的事</strong></p>
            <p style="color:var(--muted)">写作业、读一本喜欢的书、和家人一起出门走走、学一样小本领（跳绳、做一道菜）、和同学一起玩、好好休息。</p>
          </div>
          <div class="inner-card">
            <p><strong>安排的小办法</strong></p>
            <p style="color:var(--muted)">早上想一想今天最想做的一件事，把它写下来；先做完要做的，再去做想做的；玩一会儿，歇一会儿，也让眼睛休息一会儿。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="假期一天的小计划示意图：上午、下午、晚上三栏分别安排要做的和想做的事，附中文标注">
          <figcaption>示意图：假期一天的小计划——上午做要做的 · 下午做想做的 · 晚上歇一歇（教学示意图，整体为中性简洁插画）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「放假了，睡到几点、玩到几点都没关系」。其实作息一乱，白天没精神，作业也写不进去，最后一天还得赶。假期也要有一点自己的节奏，早上起来、晚上按时睡，一天才过得舒服。</p>
        </div>
        <div class="kid-note"><span class="emoji">📅</span><div><strong>记一句小口诀：</strong>先做要做的，再做想做的；玩一会儿，歇一会儿——<strong>假期不白过。</strong></div></div>
{insight_box([
    {"lens": "看见它", "text": "会过假期的人，做的事都很小：写下来、先做一件、玩一会儿、按时睡觉。它们不在纸上，就在每一天里。"},
    {"lens": "解释它", "text": "为什么先做要做的更舒服？因为放着没做的事会一直惦记着，玩也玩不安心；先做完，玩的时候就真的是在玩。"},
    {"lens": "迁移它", "text": "这个办法不只用在假期：周末、寒暑假、放学以后，甚至一个下午，都可以这样排——先做要做的，再做想做的。"},
])}
    ''', tag="概念一"))

    scene_btns = "\n".join(
        f'            <button class="choice" data-scene="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in SCENES
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：节假日里的一天，你会怎么做？", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一件你在节假日里可能会遇到的事，再从三个做法里选一个。<strong>选得好会告诉你为什么，选得不太合适也会告诉你还可以试试什么。</strong></p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 节假日里，我遇到了这样一件事</div>
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
          <p class="result warn" id="day-out" style="margin-top:12px">先点一件节假日里可能遇到的事。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💛</span><div><strong>说给你听：</strong>这里的做法没有「对」和「错」的分数。有些做法只是会让你麻烦一点，换一个试试就好。拿不准的时候，和家里人商量一下，是很好的办法。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "教师节快乐 · 团团圆圆过中秋 · 欢欢喜喜庆国庆", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">节假日里，有三个日子特别值得记住。它们不只是「放假」，还各有一份<strong>心里的意思</strong>。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>教师节：</strong>谢谢老师教我们读书、陪我们长大。一句真心的话、一张自己画的小卡片、上课认真听讲、把作业认真写好，都是很好的感谢。</div></div>
          <div class="step"><span class="n">2</span><div><strong>中秋节：</strong>一家人一起吃月饼、一起看看月亮，听爷爷奶奶讲讲他们小时候是怎么过中秋的；也可以给不在身边的亲人打个电话，问一声好。<strong>团圆，是人在一起，心也在一起。</strong></div></div>
          <div class="step"><span class="n green">3</span><div><strong>国庆节：</strong>国庆节是庆祝祖国生日的日子。和家人一起看庆祝活动的节目，说一说身边这几年的新变化；<strong>看到升国旗，就停下手里的事、立正站好、认真唱国歌</strong>。表达祝福要庄重，不喧闹、不打闹。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="三个节日的做法示意图：教师节表达感谢、中秋节一家人团圆、国庆节庄重庆祝，附中文标注">
          <figcaption>示意图：三个节日的做法——教师节说一句真心的感谢 · 中秋节一家人一起吃月饼赏月 · 国庆节庄重地庆祝并为祖国祝福（教学示意图）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「过节就是放假、收礼物、玩个痛快」。其实这些日子还有它自己的意思：教师节要感谢老师，中秋节要一家团圆，国庆节要为祖国庆祝。把这份意思过出来，节日才不一样。</p>
        </div>
        <div class="kid-note"><span class="emoji">🌕</span><div><strong>一句话记住它们：</strong>中秋的月亮圆，一家人围坐在一起；国庆的旗子红，我们一起祝祖国生日快乐。</div></div>
{insight_box([
    {"lens": "看见它", "text": "三个节日里，真正让人记住的都不是礼物，而是那几件小事：给老师递上一张卡片、给爷爷倒一杯水、和家人一起看一次庆祝活动。"},
    {"lens": "比较它", "text": "教师节是对身边人的感谢，中秋节是一家人的团圆，国庆节是对祖国的祝福。日子不一样，要表达的心意也不一样。"},
    {"lens": "迁移它", "text": "这样的心意不只在节日里。平时对老师认真一点、对长辈耐心一点、看到升国旗停下来站好，都是在做同一件事。"},
])}
    ''', tag="概念二"))

    fest_task_btns = "\n".join(
        f'            <button class="choice" data-task="{t["id"]}" style="text-align:left">{t["t"]}</button>'
        for t in FEST_TASKS
    )
    fest_btns = "\n".join(
        f'            <button class="choice" data-holiday="{h["id"]}" style="text-align:center">{h["n"]}</button>'
        for h in HOLIDAYS
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：三个节日，各自的心意", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">上面是六件在节假日里做的事，下面是三个节日。先点一件事，再点它属于哪个节日。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 节假日里，有人做了这样一件事</div>
          <div class="grid" id="fest-stage">
{fest_task_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 它是哪个节日的做法</div>
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
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🎈</span><div><strong>想一想再点：</strong>拿不准的时候，先问自己一句——这件事是在对<strong>谁</strong>表达心意？是想谢谢老师，想和家人团圆，还是想为祖国祝福？想清楚这一点，答案就出来了。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小美家的中秋节", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>中秋节那天晚上，爷爷奶奶来了，妈妈在准备月饼和水果，小美正在看动画片，正好看到最精彩的地方。她应该怎么做比较好？请你帮她一步一步想清楚。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看清情境：</strong>一家人在等她，月饼还没切；动画片明天还能看，而且随时能重看。</div></div>
          <div class="step"><span class="n">2</span><div><strong>想一想为什么：</strong>中秋是团圆的节日，一家人凑在一起的时间并不多，错过去就要等下一年。</div></div>
          <div class="step"><span class="n">3</span><div><strong>选一个合适的做法：</strong>先把动画片暂停，出来和大家一起吃月饼，请爷爷讲讲他小时候过中秋的事。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>还可以怎样：</strong>吃完月饼给外婆打个电话，说一声节日快乐，祝她身体健康——团圆也可以隔着电话。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「过节最重要的是自己玩得开心，家里人的事等一等没关系」。可是团圆的日子，一家人坐在一起才是最重要的。动画片随时能看，一家人的这个晚上，过去了就过去了。</p>
        </div>
        <div class="inner-card">
          <p><strong>说给同桌听：</strong>小美这四步里，哪一步你自己已经做到了？如果换成你，你还会加上哪一件小事？</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "关于假期安排，下面哪个说法更合适？",
         "options": [("先做要做的，再做想做的，玩和休息搭着来", True),
                     ("放假就是什么都不用安排，想做什么做什么", False),
                     ("把作业全部留到最后一天一起写完", False)],
         "explain": "有安排不等于不自由，而是让这一天过得更舒服、更满。"
                    "<strong>错因提醒：</strong>常见错误是误认为「有安排就不好玩」——真正不好玩的是最后一天手忙脚乱地赶作业。"},
        {"q": "中秋节一家人围着桌子坐下来了，下面哪个做法更合适？",
         "options": [("一起吃月饼，听爷爷奶奶讲讲他们小时候过中秋的事", True),
                     ("一个人回房间继续看手机", False),
                     ("先挑最大的那一块月饼拿在自己手里", False)],
         "explain": "中秋节最珍贵的就是一家人在一起说说话。"
                    "<strong>错因提醒：</strong>容易把「团圆」搞混成「只要大家在同一间屋子里就行」——要坐在一起、有说有笑，才是团圆。"},
        {"q": "国庆节，下面哪个做法既合适又庄重？",
         "options": [("和家人一起看庆祝活动，看到升国旗就停下站好、认真唱国歌", True),
                     ("在小区里一边跑一边大声喊", False),
                     ("国庆节和平常的休息日一样，什么也不用做", False)],
         "explain": "国庆节是庆祝祖国生日的日子，我们用庄重的方式表达祝福。"
                    "<strong>错因提醒：</strong>有人误认为「国庆就是多放几天假」——它还是一个为祖国庆祝的日子。"}
    ], tag="概念测试"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，做法还在不在", TTS["posttest"], [
        {"q": "寒假第一天，你打算怎么安排？",
         "options": [("和家人一起把假期想做的事写下来，排个大概的顺序", True),
                     ("每天睡到中午，起来再说", False),
                     ("先玩个够，作业开学前一晚再写", False)],
         "explain": "先把想做的事写下来，假期就有了一个大致的样子。"
                    "<strong>错因提醒：</strong>常见错误是误认为「寒假很长，慢慢来也来得及」——一天一天过去，很快就到开学了。"},
        {"q": "重阳节，家里要去看望外婆，你会：",
         "options": [("跟着一起去，见到外婆问一声好，陪她说说话", True),
                     ("说自己要和同学玩，让父母自己去", False),
                     ("路上一直嫌无聊，闹着要回家", False)],
         "explain": "看望长辈是心里有他们。问一声好、陪她说说话，这几件小事长辈会记很久。"
                    "<strong>错因提醒：</strong>容易误认为「去了就行，站着不说话也算陪」——陪是要说说话的。"},
        {"q": "假期最后一天，作业还剩一点没写完，你会：",
         "options": [("静下心来一鼓作气写完，再安心玩一会儿", True),
                     ("熬到很晚硬赶，第二天没精神", False),
                     ("借同学的抄一下应付过去", False)],
         "explain": "写完再去玩，玩的时候心里是轻松的。"
                    "<strong>错因提醒：</strong>有人误认为「抄一遍也算完成」——抄来的东西自己没学会，下次遇到还是不会。"}
    ], tag="后测"))

    item_btns = "\n".join(
        f'            <button class="sort-item" data-item="{it["id"]}">{it["t"]}</button>' for it in SORT_ITEMS
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：八条做法，分进两个筐", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一条做法，再点它应该进的筐：<strong>合适的做法</strong>放一边，<strong>要调整的做法</strong>放另一边。</p>
        <div class="lab-panel">
          <div class="sort-bank" id="sort-stage">
{item_btns}
          </div>
          <div class="grid grid-2" style="margin-top:14px">
            <button class="choice" data-sort-bin="ok" style="text-align:center">合适的做法</button>
            <button class="choice" data-sort-bin="fix" style="text-align:center">要调整的做法</button>
          </div>
          <div class="sort-bins">
            <div class="sort-bin" id="sort-bin-ok"><h4>合适的做法</h4></div>
            <div class="sort-bin" id="sort-bin-fix"><h4>要调整的做法</h4></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">分类进度</span><span class="v" id="sort-score">已经放好 0 / 8 条</span></div>
          </div>
          <p class="result warn" id="sort-out" style="margin-top:12px">先在上面点一条做法。</p>
        </div>
        <div class="inner-card">
          <p><strong>分完之后，想一想：</strong></p>
          <p style="color:var(--muted)">要调整的做法里，有没有哪一条是「我下次很像会做的事」？把它记下来，再说一说换成合适的做法应该怎么做。</p>
          <textarea id="syn-answer" rows="3" placeholder="我下次很像会……，换成合适的做法，我会……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：四句话，讲清怎样过好节假日", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>假期有收获：</strong>先做要做的，再做想做的；玩和休息搭着来，作息不乱。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>教师节快乐：</strong>一句真心的话、一张自己画的卡片、上课认真听讲——感谢在心里，不在礼物有多贵。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>团团圆圆过中秋：</strong>一家人一起吃月饼、赏月，听长辈讲过去的事，也给不在身边的亲人问一声好。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>欢欢喜喜庆国庆：</strong>和家人一起看庆祝活动；看到升国旗，停下手里的事、立正站好、认真唱国歌。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那个问题：</strong>为什么有的同学放假回来会说「假期什么也没做」？因为假期需要一点点安排。只要把要做的先做完，再做想做的，节日里的心意也说出口、做出来，你的假期就不会白过。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「安排、感谢、团圆」这三个词，说清楚你打算怎样过好下一个节假日。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "说出假期里可以做的三件事，再说说为什么要先做要做的。",
            "说出中秋节的晚上，一家人可以一起做的两件事。",
        ],
        [
            "和家人一起排一份「假期一天的小计划」，第二天照着做，晚上说说哪一件做到了。",
            "给老师写一句感谢的话，或者自己动手画一张小卡片，教师节前后送给老师。",
        ],
        [
            "采访一位长辈，问问他小时候是怎么过中秋或者过年的，把听到的记下来，讲给同学听。",
            "在家里找一找：哪些时候能看到国旗？看到升国旗应该怎么做？说给家里人听。",
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
    "title": "过好节假日",
    "name_en": "Making the Most of Holidays and Festivals",
    "grade": 2,
    "grade_cn": "二年级",
    "domain": "moral-cultivation",
    "domain_cn": "道德修养",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学二年级的道德与法治课：从「假期有收获」开始，学会把要做的和想做的安排好；再认识教师节、中秋节、国庆节三个日子，知道每个节日心里装着的是什么；最后学会用合适的做法和最亲近的人相处。全课只讲能看见、能做到的具体做法，把价值判断落在「应该怎么做、为什么」上，不做道德说教，也不做法条背诵。",
    "tags": ["过好节假日", "假期有收获", "教师节", "中秋节", "国庆节", "二年级", "道德修养"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学「道德修养 / 中华优秀传统文化」——礼貌与诚信，克己守礼，自尊自爱，自强自律；感受传统节日与家乡文化；对应统编《道德与法治》二年级上册「过好节假日」单元：假期有收获、教师节快乐、团团圆圆过中秋、欢欢喜喜庆国庆。",
    "hero_question": "同样是放假，为什么有的同学回来会说「假期什么也没做」？",
    "hero_alt": "过好节假日知识结构图：假期有收获、三个节日的心意、和家人一起过 三栏",
    "hero_caption": "过好节假日：假期有收获 · 教师节快乐 · 团团圆圆过中秋 · 欢欢喜喜庆国庆",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "假期怎么安排，才不白白过去？", "d": "玩和写作业，怎么放在一起", "v": "假期怎么安排才不白白过去"},
        {"t": "教师节，我想向老师表达感谢，可以怎么做？", "d": "说一句什么、做一件什么", "v": "教师节我想向老师表达感谢可以怎么做"},
        {"t": "中秋节的晚上，一家人可以做什么？", "d": "团圆到底是什么样子", "v": "中秋节的晚上一家人可以做什么"},
        {"t": "国庆节，我怎样表达对祖国的祝福？", "d": "做什么才庄重又合适", "v": "国庆节我怎样表达对祖国的祝福"},
    ],
    "objectives": [
        "能说出假期里可以做的几件有意义的事，会给自己排一份「假期一天的小计划」",
        "知道教师节是感谢老师的日子，会用一句真心的话或一个小行动表达感谢",
        "能说出中秋节团圆的习俗，愿意和家人一起过节、听长辈讲过去的事",
        "知道国庆节是庆祝祖国生日的日子，会用庄重又具体的方式表达祝福",
    ],
    "objectives_plain": [
        "能说出假期里可以做的几件有意义的事，会给自己排一份「假期一天的小计划」",
        "知道教师节是感谢老师的日子，会用一句真心的话或一个小行动表达感谢",
        "能说出中秋节团圆的习俗，愿意和家人一起过节、听长辈讲过去的事",
        "知道国庆节是庆祝祖国生日的日子，会用庄重又具体的方式表达祝福",
    ],
    "standards": [
        {"content": "礼貌与诚信，克己守礼，自尊自爱，自强自律；感受传统节日与家乡文化",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学 道德修养 / 中华优秀传统文化"},
        {"content": "假期有收获；教师节快乐；团团圆圆过中秋；欢欢喜喜庆国庆",
         "source": "统编《道德与法治》二年级上册「过好节假日」单元"},
    ],
    "prereqs": ["pol-e-g1-u4"],
    "prereqs_name": "我们讲文明",
    "prereqs_meta": "pol-e-g1-u4",
    "leads_to": ["pol-e-g2-u2"],
    "next_meta": "pol-e-g2-u2",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "同样是放假，有的同学回来会说「假期什么也没做」——今天先弄清楚怎么过才不白过。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能说出节假日里该怎么做。",
        "objectives": "看清四件事：假期会安排、教师节会感谢、中秋会团圆、国庆会祝福。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "先做要做的，再做想做的；玩和休息搭着来，作息不要乱。",
        "lab-1": "六件事，每件三个做法。选得不太合适也不会说你错，只会告诉你还可以试试什么。",
        "module-2": "教师节说感谢，中秋说团圆，国庆说祝福——三个日子，三份心意。",
        "synthesis": "八条做法分进「合适的做法」和「要调整的做法」两个筐，分完读一读为什么。",
        "worked-example": "小美四步：看清情境、想想为什么、选合适的做法、再说还可以怎样。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "posttest": "出现了寒假、重阳节和假期最后一天的作业，看看你能不能把办法用上去。",
        "summary": "四句话：假期有收获、教师节快乐、团团圆圆过中秋、欢欢喜喜庆国庆。",
        "homework": "三层小任务，先做前两层，第三层可以请家里人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学道德与法治「道德修养」，正对统编教材二年级上册「过好节假日」单元。二年级学生的难点不是听不懂道理，而是不知道「具体该怎么做」——所以全课不讲抽象概念，只做四件能落地的事：假期有收获（先做要做的、再做想做的、玩和休息搭着来、作息不乱）、教师节快乐（一句真心的话、一张自己画的卡片、上课认真听讲）、团团圆圆过中秋（一起吃月饼、赏月、听长辈讲过去的事、给不在身边的亲人问好）、欢欢喜喜庆国庆（和家人一起看庆祝活动、看到升国旗就停下站好认真唱国歌、用庄重的方式表达祝福）。三个互动台子都能真的操作：一个是六张「节假日里的一天」情境卡，选做法后立刻展开后果（「这样可能会……，还可以试试……」），不判错、不贴标签；一个是「三个节日，各自的心意」，把六件事配到教师节、中秋节、国庆节三个节日上；一个是「八条做法，分进两个筐」，把做法分进「合适的做法／要调整的做法」。全课以具体做法收口，插图一律为中性简洁的教学示意图，不使用真实人物照片；涉及国旗、国歌的表述一律庄重得体。",
    "plan_table": """| 1 | cover | 过好节假日 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 假期有收获：先做要做的，再做想做的 | 承·概念一（假期安排） |
| 6 | interactive | 动手一：节假日里的一天，你会怎么做？ | 承·情境判断（选做法 → 展开后果，不判错） |
| 7 | concept | 教师节快乐 · 团团圆圆过中秋 · 欢欢喜喜庆国庆 | 承·概念二（三个节日的心意） |
| 8 | interactive | 动手二：三个节日，各自的心意 | 承·配对操作（六件事 → 三个节日） |
| 9 | concept | 例题示范：小美家的中秋节 | 转·重难点突破（分步示范 + 易错点） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：八条做法，分进两个筐 | 合·迁移应用（合适 / 要调整 分类） |
| 12 | quiz | 后测：换几个新情境，做法还在不在 | 合·后测 |
| 13 | summary | 小结：四句话，讲清怎样过好节假日 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：假期有收获 / 三个节日的心意 / 和家人一起过 三栏，附中文标注\n- P5 假期一天的小计划示意图（已生成）：上午要做的 · 下午想做的 · 晚上歇一歇，附中文标注\n- P7 三个节日的做法示意图（已生成）：教师节表达感谢、中秋节团圆、国庆节庄重庆祝，附中文标注\n- 三张图均为中性简洁教学示意图，不使用任何真实人物照片或可识别肖像\n- 涉及国旗、国歌的内容一律以文字庄重表述，不生成国旗图形，避免图形失真\n- 若需补充：本班节假日活动照片（需家长授权后使用）",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
