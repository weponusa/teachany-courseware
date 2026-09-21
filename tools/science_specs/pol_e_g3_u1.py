# -*- coding: utf-8 -*-
"""小学道德与法治 · 做学习的主人（G3）—— 补齐知识树「道德修养」空缺

学科语气（道德与法治）：情境案例驱动，情感共鸣 + 价值判断；结论落在「应该怎么做、为什么」，
不做道德说教，也不做法条背诵。
三年级落点（全部换成能看见、能做到的具体动作与选择）：
  ① 自己安排作业时间（先做要紧的、做完检查一遍）
  ② 遇到不会的题怎么办（先想 → 再看 → 再问 → 再记）
  ③ 「为什么」比「是什么」更重要（多问一句为什么，知识才变成自己的）
三个互动台子都能真操作：情境卡选做法（反馈一律「这样可能会……，还可以试试……」）、
「遇到不会的题」四步排序、「会学习的 / 要调整的」两筐分类。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g3-u1"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "学习这件事，我们每天都在做。可是有同学会发现，同样一份作业，有人半小时就做完了，有人一直拖到睡觉前才写完；同样是遇到一道不会的题，有人越做越有兴趣，有人一看见就想放弃。这是为什么呢？这节课我们一起来弄清楚三件事：学习会陪着我们一路长大；学习其实可以是一件让人高兴的事；学习是有方法的。学完以后，你会更清楚怎么安排自己的时间，也知道遇到不会的题该怎么办。",
    "problem-anchor": "开始之前，先选一个你最想弄清楚的问题。是想知道作业该什么时候做、时间怎么安排，还是想知道遇到不会的题怎么办；是想知道学不会、觉得累的时候该怎么办，还是想知道有没有让学习更省力的方法。选好以后，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出学习不只发生在课堂上，生活里到处都有学习。第二，能自己安排一份放学后的学习小计划，知道先做什么、后做什么。第三，遇到不会的题，知道可以按先自己想、再看书、再问同学、最后问老师的顺序去试。第四，能说出一两个适合自己的学习方法，愿意在学习里多问一句为什么。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先来说说，学习这件事到底发生在哪里。很多同学以为，学习就是坐在教室里上课、回家写作业，其实不止。你在家里学做一道菜，是学习；你跟着家里人认路，记住哪个路口该转弯，是学习；你养的一盆花开了，你发现它朝着窗户长，也是学习。学习就是一个人从不会变成会的过程。而且你会发现，比起只记住这是什么，多问一句为什么会这样，往往能让你懂得更牢、记得更久。",
    "lab-1": "现在请你当一次学习小主人。这里有六件放学以后可能会遇到的事，每一件事都有三个做法。你选一个你觉得合适的，选完立刻会有一段话告诉你为什么；要是选得不太合适，也会告诉你还可以试试什么。",
    "module-2": "学习这件事，有时候会觉得累，有时候会觉得有意思。那份有意思从哪里来呢？多半来自你自己想明白了一件事：当你花了很久，终于把一道题弄懂，那种高兴是别人拿不走的。学得比较顺的同学，常常有几条共同的做法。第一，把时间安排清楚，先做要紧的事，做完检查一遍。第二，遇到不会的题，按先自己想、再看书、再问同学、最后问老师的顺序去试；问的时候说清楚自己卡在哪一步。第三，不明白的地方多问一句为什么，而不是只把答案记下来。第四，学完了回头看一看，自己是怎么一步一步想出来的。方法不一定是别人的，适合你的才是最好的。",
    "lab-2": "遇到不会的题，先做什么、后做什么，顺序很重要。这里有四张步骤卡，它们现在排得有点乱，请你按你觉得对的顺序一张一张点下去。点对了，它们会排成一队；点错了，也会告诉你为什么，以及还可以怎么试。",
    "worked-example": "我们一起来帮小雨安排一个傍晚。第一步，看清条件：小雨五点半到家，六点半吃晚饭，九点睡觉；今天有数学、语文、英语三样作业，数学最难。第二步，排好顺序：回家先歇十分钟，然后从当天最要紧、最难的那一样开始，先做数学；做完数学休息十分钟，再做语文和英语。第三步，遇到不会的题：先在题目上圈出已经知道的条件，自己想一想；想不出来就翻课本和例题，找一个相似的做法；还是不会，就做个小记号先跳过去，把会的做完。第四步，回头处理：把做过记号的题拿去问同学、问老师，问的时候说清楚自己卡在哪一步；问懂了，在旁边自己再写一遍。",
    "conceptest-1": "接下来用三个说法考考你，每个说法里都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件事交给你。下面有八条放学以后的做法，请你判断一下：哪些做法是学习小主人的做法，放进会学习的这一边；哪些做法需要调整，放进要调整的这一边。放好以后，再读一读为什么。",
    "posttest": "最后一轮，换几个新的小情境来考考你。这次会遇到时间不够用、预习时看到不认识的词、还有学完了要不要回头想一想，看看你能不能用上今天的办法。",
    "summary": "这节课我们记住四句话。第一句，学习不只在课堂上，生活里到处都有学习，从不会到会的过程就是学习。第二句，做学习的主人，就是自己安排时间：先做要紧的事，做完检查一遍。第三句，遇到不会的题，按先自己想、再看书、再问同学、最后问老师的顺序去试；实在想不出来，先做个记号，把会的做完再回头。第四句，多问一句为什么，比只记住答案更有用。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出学习会发生在家里的哪两件事上，再说出遇到不会的题时的先后顺序。第二层能力应用，动手做：给自己安排一张放学后到睡觉前的小计划表，写清楚先做什么、后做什么，第二天照着做一遍。第三层迁移挑战，选做：学完一课以后，写一写自己是怎么想明白的，再提一个还想继续问下去的为什么。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 学习伴我成长", "lab-1": "动手一 放学以后怎么办",
    "module-2": "概念二 我学习我快乐 · 学习有方法", "lab-2": "动手二 不会的题，四步来",
    "worked-example": "例题讲解 小雨的一个傍晚", "conceptest-1": "概念测试",
    "synthesis": "综合任务 会学习的 / 要调整的", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：放学以后，六个情境 × 三个做法（反馈一律「这样可能会……，还可以试试……」） ──
SCENES = [
    {
        "id": "s1",
        "t": "放学回家，作业还没写，我想先玩一会儿",
        "opts": [
            {"k": "a", "t": "先歇十分钟、喝点水，然后开始写当天的作业", "ok": True,
             "fb": "这个安排挺好。歇一小会儿再动笔，人更精神，作业也不容易拖到很晚。"},
            {"k": "b", "t": "先玩到吃完饭，作业留到睡觉前赶", "ok": False,
             "fb": "这样可能会写得很急、错得也多，还会睡得很晚。还可以试试：回家先做一部分，剩下的放在晚饭后。"},
            {"k": "c", "t": "先去同学家玩，等妈妈打电话再回来", "ok": False,
             "fb": "这样可能会让家里人等得着急，回来以后时间也紧了。还可以试试：先和家人说好什么时候出去、什么时候回来。"},
        ],
    },
    {
        "id": "s2",
        "t": "今天的作业有数学、语文、英语，数学最难",
        "opts": [
            {"k": "a", "t": "先把今天最要紧、最难的数学做完，再写另外两样", "ok": True,
             "fb": "这个顺序很聪明。趁着精神最好的时候做最难的那一样，后面就轻松了。"},
            {"k": "b", "t": "先挑最简单、写得最快的，难的留到最后", "ok": False,
             "fb": "这样可能会等到很累了才开始做难题，越做越着急。还可以试试：精神好的时候先啃难点。"},
            {"k": "c", "t": "三样混在一起，想起哪样写哪样", "ok": False,
             "fb": "这样可能会让你一会儿翻这本、一会儿翻那本，时间都花在找东西上了。还可以试试：一样一样来，写完一样再做下一样。"},
        ],
    },
    {
        "id": "s3",
        "t": "写作业时遇到一道怎么也想不出来的题",
        "opts": [
            {"k": "a", "t": "先在题目上圈出已经知道的条件，自己想一想", "ok": True,
             "fb": "这一步很关键。把条件一条条看清楚，常常就能找到下手的地方。"},
            {"k": "b", "t": "一直盯着这道题，想不出来就不往下写", "ok": False,
             "fb": "这样可能会在这道题上耗掉很多时间，后面的作业没写完更着急。还可以试试：做个记号先跳过去，把会的做完再回头。"},
            {"k": "c", "t": "直接看答案，照着抄下来", "ok": False,
             "fb": "这样可能会让这道题看起来会了，换一道同类的还是不会。还可以试试：先自己想，再看例题里的做法，最后才看答案。"},
        ],
    },
    {
        "id": "s4",
        "t": "想了很久还是不会，我想去问别人",
        "opts": [
            {"k": "a", "t": "先问同学，两个人都说不明白，再举手问老师", "ok": True,
             "fb": "这个顺序很好。和同学说一说，常常能互相提醒；实在不行再问老师，问题就问得更清楚了。"},
            {"k": "b", "t": "一遇到不懂的就马上问老师，自己还没想过", "ok": False,
             "fb": "这样可能会让你一直不太会自己想。还可以试试：先自己想三分钟，再去问，问的时候也更知道卡在哪里。"},
            {"k": "c", "t": "干脆不问了，反正明天老师会讲", "ok": False,
             "fb": "这样可能会让这个不懂的地方越攒越多。还可以试试：今天先做个记号，明天上课前问一问。"},
        ],
    },
    {
        "id": "s5",
        "t": "作业全都写完了，离睡觉还有一点时间",
        "opts": [
            {"k": "a", "t": "把写完的作业检查一遍，再收拾好明天要带的东西", "ok": True,
             "fb": "这两件事做得好。检查一遍能少犯不少小错，书包收好，明天早上就不慌了。"},
            {"k": "b", "t": "收进书包就行，检查太麻烦了", "ok": False,
             "fb": "这样可能会把本来能做对的小题做错，交上去才知道。还可以试试：只挑最容易错的几道看一眼。"},
            {"k": "c", "t": "一直看电视看到很晚", "ok": False,
             "fb": "这样可能会让你第二天上课没精神。还可以试试：留一小段时间做自己喜欢的事，到点就去休息。"},
        ],
    },
    {
        "id": "s6",
        "t": "今天学的一课，我有一个地方没听懂",
        "opts": [
            {"k": "a", "t": "先在书上做个小记号，再问问自己「为什么会这样」", "ok": True,
             "fb": "这个习惯真好。多问一句为什么，下次遇到新的问题也知道从哪里想。"},
            {"k": "b", "t": "没关系，反正把老师说的记住就行了", "ok": False,
             "fb": "这样可能会一换问法就答不上来。还可以试试：把没懂的地方圈出来，试着说说自己的猜想。"},
            {"k": "c", "t": "等考试前再一起想办法", "ok": False,
             "fb": "这样可能会攒下越来越多的不懂。还可以试试：今天就问一句，不懂的地方当天弄清楚。"},
        ],
    },
]

# ── 动手二：遇到不会的题，四步排序 ──
STEPS = [
    {"id": "p1", "rank": 1, "t": "先自己想一想，把题里已经知道的条件圈出来",
     "why": "第一步是「先想」。把条件一条条看清，常常就能找到下手的地方。"},
    {"id": "p2", "rank": 2, "t": "翻一翻课本和例题，找一个相似的做法",
     "why": "第二步是「再看」。例题里往往有可以照着走的思路，比一比就有线索了。"},
    {"id": "p3", "rank": 3, "t": "问问同学，把两个人的想法都说一说",
     "why": "第三步是「再问」。和同学互相说一说，常常能互相提醒。"},
    {"id": "p4", "rank": 4, "t": "还是不明白，举手问老师，说清楚自己卡在哪一步",
     "why": "最后问老师，并且说清楚自己卡在哪一步——问得越具体，越容易听懂。"},
]
STEP_DISPLAY = ["p2", "p4", "p1", "p3"]  # 展示顺序打乱，学生自己排出正确顺序
STEP_WRONG = {
    "p1": "这样可能会跳过最关键的一步：还没看清题目就去翻书，往往翻了半天也对不上。还可以试试：先把它放一放，从「先想」开始。",
    "p2": "这样可能会让思路来得有点慢，也容易照着例题硬套。还可以试试：先自己想一小会儿，再看例题。",
    "p3": "这样可能会让你和同学都说不清楚。还可以试试：自己想过、也看过例题之后再问，问题会更清楚。",
    "p4": "这样可能会让老师不太好回答——因为还没人知道你卡在哪里。还可以试试：先自己想一想，再看例题，最后带着具体的问题去问老师。",
}

# ── 综合任务：会学习的 / 要调整的（分进两个筐） ──
SORT_ITEMS = [
    {"id": "k1", "t": "放学回家先歇十分钟，然后把当天最要紧的作业先做完", "bin": "own",
     "why": "先做最要紧的事，剩下的时间就宽裕了。"},
    {"id": "k2", "t": "不会的题先圈出条件，自己想一想再看例题", "bin": "own",
     "why": "自己先想，是让脑子动起来的开始。"},
    {"id": "k3", "t": "问老师的时候，说清楚自己卡在哪一步", "bin": "own",
     "why": "把问题说具体，别人才好帮你，你也更容易听懂。"},
    {"id": "k4", "t": "写完作业检查一遍，再把明天要带的东西收拾好", "bin": "own",
     "why": "检查能少犯小错，收好书包明天早上就不慌。"},
    {"id": "k5", "t": "作业留到睡觉前再赶，写得越快越好", "bin": "tune",
     "why": "这样可能会写得很急、错得也多，还会睡得很晚。还可以试试：回家先做一部分，剩下的放在晚饭后。"},
    {"id": "k6", "t": "一道题想不出来，就一直盯着，不做后面的了", "bin": "tune",
     "why": "这样可能会在难题上耗掉太多时间。还可以试试：做个记号先跳过去，把会的做完再回头。"},
    {"id": "k7", "t": "写完直接收进书包，不想再检查", "bin": "tune",
     "why": "这样可能会把本来能做对的小题做错。还可以试试：只挑最容易错的几道看一眼。"},
    {"id": "k8", "t": "一遇到不懂的就马上问别人，自己还没想过", "bin": "tune",
     "why": "这样可能会让「自己想」的本领长得慢。还可以试试：先自己想三分钟，再去问。"},
]
SORT_BIN = {"own": "会学习的", "tune": "要调整的"}

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g3-u1 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 放学以后怎么办：六个情境 × 三个做法 → 温和反馈（不判错、不贴标签）
   3) 不会的题四步排序：按顺序点步骤卡
   4) 会学习的 / 要调整的：八条做法分进两个筐
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

  /* ---------- 2. 放学以后怎么办 ---------- */
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
      document.getElementById('day-score').textContent =
        '已经聊过 ' + Object.keys(doneScene).length + ' / ' + SCENES.length + ' 件事';
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
            out1.innerHTML = '<strong>这个安排挺好。</strong>' + o.fb;
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
          out1.innerHTML = '<strong>这件事已经聊过啦。</strong>你上次选的做法挺合适，记住它就好。';
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

  /* ---------- 3. 不会的题，四步排序 ---------- */
  var STEPS = __STEPS_JSON__;
  var stage2 = document.getElementById('step-stage');
  if (stage2) {
    var seq = [];
    var out2 = document.getElementById('step-out');

    function stepById(id) {
      for (var i = 0; i < STEPS.length; i++) { if (STEPS[i].id === id) return STEPS[i]; }
      return null;
    }
    function render2() {
      document.querySelectorAll('[data-step]').forEach(function (b) {
        var inSeq = seq.indexOf(b.dataset.step) >= 0;
        b.classList.toggle('done', inSeq);
        b.disabled = inSeq;
      });
      var box = document.getElementById('step-track');
      box.innerHTML = '';
      if (!seq.length) {
        box.innerHTML = '<span style="color:var(--muted);font-size:14px">点上面的步骤卡，正确的顺序会排在这里。</span>';
      }
      seq.forEach(function (id, i) {
        var s = document.createElement('div');
        s.className = 'tag';
        s.textContent = '第 ' + (i + 1) + ' 步：' + stepById(id).t;
        box.appendChild(s);
      });
      document.getElementById('step-score').textContent =
        '已经排好 ' + seq.length + ' / ' + STEPS.length + ' 步';
    }
    document.querySelectorAll('[data-step]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (seq.indexOf(b.dataset.step) >= 0) return;
        var S = stepById(b.dataset.step);
        if (S.rank === seq.length + 1) {
          seq.push(S.id);
          out2.className = 'result';
          out2.innerHTML = '<strong>排对了。</strong>' + S.why;
          if (seq.length === STEPS.length) {
            out2.className = 'result';
            out2.innerHTML = '<strong>四步全排好了！</strong>记住这句口诀：<strong>先想、再看、再问、再记</strong>。' +
              '想不出来的时候，就顺着这四步往前走。';
          }
        } else {
          out2.className = 'result warn';
          out2.innerHTML = '<strong>这一步可能放早了一点。</strong>' + STEP_WRONG[S.id];
        }
        render2();
      });
    });
    render2();
  }

  /* ---------- 4. 会学习的 / 要调整的 ---------- */
  var ITEMS = __SORT_JSON__;
  var BINN = __SORTBIN_JSON__;
  var stage3 = document.getElementById('own-stage');
  if (stage3) {
    var pickItem = null, placed = {};
    var out3 = document.getElementById('own-out');

    function render3() {
      document.querySelectorAll('[data-item]').forEach(function (b) {
        var k = b.dataset.item;
        b.classList.toggle('selected', k === pickItem);
        b.classList.toggle('done', !!placed[k]);
        b.disabled = !!placed[k];
      });
      document.getElementById('own-score').textContent =
        '已经放好 ' + Object.keys(placed).length + ' / ' + ITEMS.length + ' 条';
      var a = document.getElementById('own-bin-a');
      var b2 = document.getElementById('own-bin-b');
      a.innerHTML = ''; b2.innerHTML = '';
      ITEMS.forEach(function (it) {
        if (!placed[it.id]) return;
        var s = document.createElement('div');
        s.className = 'tag';
        s.textContent = it.t;
        (it.bin === 'own' ? a : b2).appendChild(s);
      });
      if (!a.innerHTML) a.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
      if (!b2.innerHTML) b2.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
    }
    document.querySelectorAll('[data-item]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (placed[b.dataset.item]) return;
        pickItem = b.dataset.item;
        out3.className = 'result warn';
        out3.innerHTML = '<strong>你选的是：' + b.textContent + '</strong><br>想一想，它是「会学习的」，还是「要调整的」？';
        render3();
      });
    });
    document.querySelectorAll('[data-own-bin]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pickItem) {
          out3.className = 'result warn';
          out3.textContent = '先在上面点一条做法，再选筐。';
          return;
        }
        var it = null;
        for (var i = 0; i < ITEMS.length; i++) { if (ITEMS[i].id === pickItem) it = ITEMS[i]; }
        if (b.dataset.ownBin === it.bin) {
          placed[it.id] = true;
          out3.className = 'result';
          out3.innerHTML = '<strong>放对了，它属于「' + BINN[it.bin] + '」。</strong>' + it.why;
          pickItem = null;
          if (Object.keys(placed).length === ITEMS.length) {
            out3.className = 'result';
            out3.innerHTML = '<strong>八条全放对了！</strong>记一句口诀：<strong>自己的事自己排，不会的题分步来；' +
              '做完检查再收拾，多问一句为什么。</strong>';
          }
        } else {
          out3.className = 'result warn';
          out3.innerHTML = '<strong>再想一想这条做法。</strong>' + it.why +
            '<br><span style="color:var(--muted)">常见错误：容易把「看起来很努力」误认为「会学习」——' +
            '一直盯着一道难题不动，看着很用力，其实换个顺序会更省时间。</span>';
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
             .replace('__STEPS_JSON__', json.dumps(STEPS, ensure_ascii=False))
             .replace('__SORT_JSON__', json.dumps(SORT_ITEMS, ensure_ascii=False))
             .replace('__SORTBIN_JSON__', json.dumps(SORT_BIN, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "下面哪个说法最接近「做学习的主人」？",
         "options": [("自己安排什么时候写作业，写完检查一遍", True),
                     ("等家里人催了再开始写", False),
                     ("先玩够了，睡觉前随便赶一赶", False)],
         "explain": "做学习的主人，就是自己安排、自己检查，心里有一份自己的小计划。"
                    "<strong>错因提醒：</strong>常见错误是误认为「别人催着我、我照着做也算自己做主」——"
                    "被推着走和自己安排，是两回事。"},
        {"q": "遇到一道怎么也做不出来的题，下面哪个做法更合适？",
         "options": [("先圈出条件自己想一想，再翻例题，最后问同学、问老师", True),
                     ("一直盯着这道题，做不出来就不往下写", False),
                     ("直接看答案抄下来", False)],
         "explain": "自己先想、再看、再问，这条路走得通，也能让你越来越会想。"
                    "<strong>错因提醒：</strong>容易把「坚持」和「硬扛」搞混——一直卡在一道题上会浪费时间，"
                    "先做个记号跳过去，把会的做完再回头，反而更快。"},
        {"q": "小美背课文时，不光背下来，还问了问「作者为什么要这样写」。她这样做：",
         "options": [("懂得更牢，也更容易记住", True),
                     ("浪费了时间，不如多背几遍", False),
                     ("没什么用，背课文不用想为什么", False)],
         "explain": "多问一句为什么，是把知识变成自己的办法，换个问法也答得上来。"
                    "<strong>错因提醒：</strong>有的同学误认为「背下来就等于学会了」——"
                    "只记结论、不问原因，换一道题就容易卡住。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "学习伴我成长：学习不只在课堂上", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">在低年级，很多事情是家里人帮我们安排好的，什么时候写作业、先做什么，都有人提醒（And）；可是到了三年级，作业变多了、时间变紧了，光等着别人来安排，很容易拖到很晚、也容易着急（But）；所以这节课我们先弄清楚：学习到底发生在哪里，又该怎么自己安排它（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">学习就是一个人<strong>从「不会」变成「会」</strong>的过程。它不只在教室里发生，生活里到处都有它。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>学习发生的三个地方</strong></p>
            <p style="color:var(--muted)">课堂上跟着老师学；家里在做家务、做饭、养花的时候学；路上认路、记事、看别人怎么做的时候也在学。</p>
          </div>
          <div class="inner-card">
            <p><strong>比「是什么」更重要的是「为什么」</strong></p>
            <p style="color:var(--muted)">记住答案，换一道同类题可能就不会了；问一句为什么，你就有了自己想出来的办法。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="学习发生的地方示意图：课堂上、家里、路上都在学习，从不会到会的过程，附中文标注">
          <figcaption>概念图：学习不只在课堂——课堂上、家里、路上都在发生；每一件事都是从「不会」走到「会」（教学示意图，人物为中性简洁扁平插画）</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🌱</span><div><strong>记一句小口诀：</strong>不会不要紧，多问一句为什么——<strong>从不会到会，就是学习。</strong></div></div>
{insight_box([
    {"lens": "看见它", "text": "学习到处都是：你在厨房里学会煮一碗面，在放学路上记住了哪个路口要转弯，在花盆边发现花朝着窗户长——这些都在长本领。"},
    {"lens": "解释它", "text": "为什么多问一句为什么能让知识更牢？因为「是什么」只是一条结论，而「为什么」是你自己走通的一条路，走过一次，下次还认得。"},
    {"lens": "迁移它", "text": "这个习惯到哪里都用得上：学骑车的时候想为什么歪了就倒，做家务的时候想为什么要先做什么，都是同一件事。"},
])}
    ''', tag="概念一"))

    scene_btns = "\n".join(
        f'            <button class="choice" data-scene="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in SCENES
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：放学以后，你会怎么做？", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一件放学以后可能遇到的事，再从三个做法里选一个。<strong>选得好会告诉你为什么，选得不太合适也会告诉你还可以试试什么。</strong></p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 今天放学以后，我遇到了</div>
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
          <p class="result warn" id="day-out" style="margin-top:12px">先点一件放学以后可能遇到的事。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💛</span><div><strong>说给你听：</strong>这里的做法没有分数。有些做法只是会让你麻烦一点，换一个试试就好。拿不准的时候，问问家里人、问问老师，都是很好的办法。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "我学习我快乐 · 学习有方法", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">学习里的高兴，多半来自<strong>自己想明白了一件事</strong>。而学得比较顺，往往是因为有方法。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>自己排时间：</strong>把时间安排清楚，先做要紧的事，做完检查一遍。</div></div>
          <div class="step"><span class="n">2</span><div><strong>不会的题分步来：</strong>先自己想 → 再看课本和例题 → 再问同学 → 最后问老师，说清楚卡在哪一步。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>多问一句为什么：</strong>不只把答案记下来，还弄明白它为什么是这样。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>学完回头看：</strong>想一想自己是怎么一步一步做出来的，下次就有办法了。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="遇到不会的题的四步示意图：先想、再看、再问、再记，附中文标注">
          <figcaption>概念图：遇到不会的题，按「先想 → 再看 → 再问 → 再记」四步走；实在想不出来先做个记号，把会的做完再回头（教学示意图）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「学得慢是因为我不够聪明」。其实很多差别不在聪明，而在有没有方法：先做什么、不会的时候怎么办、做完要不要检查。方法是可以慢慢学、慢慢练的。</p>
        </div>
        <div class="kid-note"><span class="emoji">🔑</span><div><strong>一句口诀：</strong>先想、再看、再问、再记——<strong>方法不用背下来，用几次就成自己的了。</strong></div></div>
{insight_box([
    {"lens": "看见它", "text": "会学习的同学，做法往往很像：先做要紧的事，遇到难题先自己想一想，问人的时候说得很具体，做完还会检查。"},
    {"lens": "比较它", "text": "同样一道不会的题：一直盯着不动，看着很用力；先跳过去把会的做完再回头，反而更快写完、也更少着急——差别就在顺序。"},
    {"lens": "迁移它", "text": "这套顺序不只用在作业上：学一件新家务、学一种乐器，也都是先自己想、再看别人怎么做、再问、再记住。"},
])}
    ''', tag="概念二"))

    step_btns = "\n".join(
        f'            <button class="choice" data-step="{sid}" style="text-align:left">'
        f'{next(s["t"] for s in STEPS if s["id"] == sid)}</button>'
        for sid in STEP_DISPLAY
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：遇到不会的题，四步来", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">下面是四张步骤卡，顺序被打乱了。请你按你觉得对的顺序，一张一张点下去。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 点出你的顺序</div>
          <div class="grid" id="step-stage">
{step_btns}
          </div>
          <div class="inner-card" style="margin-top:14px">
            <p><strong>四步走出来的顺序</strong></p>
            <div id="step-track" style="display:flex;flex-wrap:wrap;gap:6px"><span style="color:var(--muted);font-size:14px">点上面的步骤卡，正确的顺序会排在这里。</span></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">排队进度</span><span class="v" id="step-score">已经排好 0 / 4 步</span></div>
          </div>
          <p class="result warn" id="step-out" style="margin-top:12px">先点一张你觉得应该排在最前面的步骤卡。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧭</span><div><strong>想一想：</strong>为什么「先自己想」要排在「问别人」前面？因为自己想过了，你就知道自己卡在哪一步，问的时候也说得清楚。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小雨的一个傍晚", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>小雨五点半到家，六点半吃晚饭，九点睡觉。今天有数学、语文、英语三样作业，数学最难。请你帮她安排这个傍晚，再说说遇到不会的题该怎么办。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看清条件：</strong>五点半到家，六点半吃晚饭，九点睡觉；三样作业，数学最难。</div></div>
          <div class="step"><span class="n">2</span><div><strong>排好顺序：</strong>回家先歇十分钟，精神最好的时候先做最要紧、最难的数学；中间休息十分钟，再做语文和英语。</div></div>
          <div class="step"><span class="n">3</span><div><strong>遇到不会的题：</strong>先圈出已经知道的条件，自己想一想；再翻课本和例题；还是不会，就做个小记号先跳过去，把会的做完。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>回头处理：</strong>把做过记号的题拿去问同学、问老师，说清楚自己卡在哪一步；问懂了，在旁边自己再写一遍。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「不会的题要一直想，想不出来就不能往下做」。其实先做个记号跳过去、把会的做完，再回头解决，反而更省时间，也更不容易着急。</p>
        </div>
        <div class="inner-card">
          <p><strong>说给同桌听：</strong>小雨这个傍晚，哪一步你自己已经做到了？哪一步还想再练一练？</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "下面哪句话说得对？",
         "options": [("做学习的主人，就是自己安排时间，先做要紧的事，做完检查一遍", True),
                     ("学习就是上课听讲、回家写作业，别的地方不算学习", False),
                     ("学得慢说明我不够聪明", False)],
         "explain": "自己安排、自己检查，是「做学习的主人」最实在的样子；学习也发生在家里、路上和做事的过程中。"
                    "<strong>错因提醒：</strong>常见错误是误认为「我学得慢就是笨」——"
                    "很多差别不在聪明，而在有没有方法。"},
        {"q": "做作业时遇到一道不会的题，下面哪个做法更好？",
         "options": [("先圈出条件自己想一想，再翻例题，最后问同学和老师", True),
                     ("一直盯着这道题，做不出来就不往下写", False),
                     ("翻开答案抄下来，交上去就行", False)],
         "explain": "先想、再看、再问，这条路能让这道题真正变成你会做的题。"
                    "<strong>错因提醒：</strong>有人误认为「一直想才叫认真」——"
                    "卡住太久会耽误后面的作业，先做记号跳过去更聪明。"},
        {"q": "学完一课以后，「回头想一想自己是怎么做出来的」这件事的好处是：",
         "options": [("下次遇到同类的题，知道自己该从哪里下手", True),
                     ("只是多花时间，没什么用", False),
                     ("能多写一遍字，写得更工整", False)],
         "explain": "回头看一看，是把一次经验变成自己的方法。"
                    "<strong>错因提醒：</strong>容易把「多做几道题」和「弄懂一道题」搞混——"
                    "只做不想，做十道还是十道；想清楚了，一道就能顶好几道。"}
    ], tag="概念测试"))

    item_btns = "\n".join(
        f'            <button class="sort-item" data-item="{it["id"]}">{it["t"]}</button>' for it in SORT_ITEMS
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：会学习的 / 要调整的，把做法分进两个筐", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一条做法，再点它应该进的筐：<strong>学习小主人的做法</strong>放一边，<strong>需要调整的做法</strong>放另一边。</p>
        <div class="lab-panel">
          <div class="sort-bank" id="own-stage">
{item_btns}
          </div>
          <div class="grid grid-2" style="margin-top:14px">
            <button class="choice" data-own-bin="own" style="text-align:center">会学习的</button>
            <button class="choice" data-own-bin="tune" style="text-align:center">要调整的</button>
          </div>
          <div class="sort-bins">
            <div class="sort-bin" id="own-bin-a"><h4>会学习的</h4></div>
            <div class="sort-bin" id="own-bin-b"><h4>要调整的</h4></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">分类进度</span><span class="v" id="own-score">已经放好 0 / 8 条</span></div>
          </div>
          <p class="result warn" id="own-out" style="margin-top:12px">先在上面点一条做法。</p>
        </div>
        <div class="inner-card">
          <p><strong>分完之后，想一想：</strong></p>
          <p style="color:var(--muted)">「要调整的」这一边里，有没有哪一条很像你昨天的做法？把它记下来，再说一说换成会学习的做法应该怎么做。</p>
          <textarea id="syn-answer" rows="3" placeholder="昨天我……，现在我会……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，办法还在不在", TTS["posttest"], [
        {"q": "小刚放学回家先和弟弟玩，吃完晚饭才写作业，每天都写到很晚。如果他想改一改，最合适的做法是：",
         "options": [("回家先完成当天最要紧的作业，再出去玩", True),
                     ("以后写快一点就可以了", False),
                     ("每天让家里人陪着他写", False)],
         "explain": "把要紧的事排在前面，玩起来也更安心。"
                    "<strong>错因提醒：</strong>常见错误是误认为「写得快就来得及」——"
                    "时间紧的时候越写越快，反而容易出错、也容易着急。"},
        {"q": "预习时看到一个不认识的词，下面哪个做法更好？",
         "options": [("先根据前后文猜一猜，再查一查确认", True),
                     ("跳过不管，等老师讲", False),
                     ("直接问别人它是什么意思，自己不想", False)],
         "explain": "先猜再查，是自己想过的过程，印象会比直接被告知深得多。"
                    "<strong>错因提醒：</strong>容易把「记住了」当成「懂了」——"
                    "猜一猜、再确认，才是把新词真正弄明白。"},
        {"q": "同学说：「不会的题直接问老师最快，自己多想是浪费时间。」你怎么看？",
         "options": [("自己先想过再问，问得更清楚，也更会自己想", True),
                     ("他说得对，问老师最快，不用自己想", False),
                     ("不会的题干脆别做，等老师讲", False)],
         "explain": "自己先想过，才知道自己卡在哪一步，问的时候说得具体，也更容易听懂。"
                    "<strong>错因提醒：</strong>有人误认为「问得快就是学得快」——"
                    "问之前没有想过，下次遇到同类的题还是不会。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：四句话，讲清怎么当学习的主人", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>学习在哪里：</strong>不只在课堂上，家里、路上、做事的时候都在学习——从不会到会，就是学习。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>自己排时间：</strong>先做要紧的事，做完检查一遍，再收拾好明天要带的东西。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>不会的题分步来：</strong>先想 → 再看 → 再问 → 再记；实在想不出来先做记号，把会的做完再回头。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>多问为什么：</strong>不只记住答案，还弄明白它为什么是这样，知识才真正变成自己的。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>还要记牢一句话：</strong>做学习的主人，不是一下子就能做好，而是今天比昨天多安排好一点点。慢一点也没关系，走在自己的路上就好。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「自己排、分步来、多问为什么」这三个说法，说清楚你今天学到的一个办法。</p>
          <p style="color:var(--muted)">再动一动手：<strong>写一写</strong>你的放学后小计划——先做什么、后做什么、什么时候休息，明天照着做一遍。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "说出学习会发生在家里的两件事，再说说为什么它们也是学习。",
            "写出遇到不会的题时的先后顺序：先做什么、再做什么。",
        ],
        [
            "给自己安排一张放学后到睡觉前的小计划表，写清楚先做什么、后做什么、什么时候休息，第二天照着做一遍，再和同桌说一说哪一步做起来最难。",
            "挑一道今天不会的题，把「先想、再看、再问、再记」四步走一遍，把你卡在哪一步说给老师听。",
        ],
        [
            "学完一课以后，写三句话：这一课我最想弄明白的是什么？我是怎么想通的？我还想问一个什么「为什么」？",
            "问一问家里的大人：他小时候遇到过不会做的题是怎么解决的？把他的办法记下来，和今天学的四条比一比。",
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
    "title": "做学习的主人",
    "name_en": "Be the Master of Your Own Learning",
    "grade": 3,
    "grade_cn": "三年级",
    "domain": "moral-cultivation",
    "domain_cn": "道德修养",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学三年级的道德与法治课：从「学习不只在课堂上」开始，弄明白学习是从不会到会的过程，多问一句为什么比只记住答案更重要；再学着像学习的主人那样安排时间（先做要紧的事、做完检查一遍），遇到不会的题按「先想、再看、再问、再记」四步去试；最后把做法分进「会学习的／要调整的」两个筐，落在能看见、能做到的具体动作上，帮助三年级学生养成良好学习习惯、体会学习本身的快乐。",
    "tags": ["做学习的主人", "学习伴我成长", "我学习我快乐", "学习有方法", "良好学习习惯", "三年级", "道德修养"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学「道德修养」——诚实守信，友善待人，尊重他人，有集体意识和责任感；对应统编《道德与法治》三年级上册「做学习的主人」：学习伴我成长、我学习我快乐、学习有方法。",
    "hero_question": "学习这件事，是等着别人来安排，还是可以自己做主？",
    "hero_alt": "做学习的主人知识结构图：学习伴我成长、我学习我快乐、学习有方法 三栏",
    "hero_caption": "做学习的主人：学习伴我成长 · 我学习我快乐 · 学习有方法（自己排时间 · 不会的题分步来 · 多问一句为什么）",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "作业该什么时候做？", "d": "放学回家先做什么、怎么排时间", "v": "作业该什么时候做"},
        {"t": "遇到不会的题怎么办？", "d": "先自己想，还是先去问别人", "v": "遇到不会的题怎么办"},
        {"t": "学不会、觉得累的时候怎么办？", "d": "怎么让自己接着往前走", "v": "学不会觉得累的时候怎么办"},
        {"t": "有没有让学习更省力的方法？", "d": "学得顺的同学都有什么做法", "v": "有没有让学习更省力的方法"},
    ],
    "objectives": [
        "能说出学习不只发生在课堂上，生活里到处都有学习，从「不会」到「会」的过程就是学习",
        "能自己安排一份放学后的学习小计划，知道先做要紧的事、做完检查一遍",
        "遇到不会的题，知道按「先想 → 再看 → 再问 → 再记」的顺序去试，实在想不出来先做记号、把会的做完再回头",
        "能说出一两个适合自己的学习方法，愿意在学习里多问一句为什么",
    ],
    "objectives_plain": [
        "能说出学习不只发生在课堂上，生活里到处都有学习，从「不会」到「会」的过程就是学习",
        "能自己安排一份放学后的学习小计划，知道先做要紧的事、做完检查一遍",
        "遇到不会的题，知道按「先想 → 再看 → 再问 → 再记」的顺序去试",
        "能说出一两个适合自己的学习方法，愿意在学习里多问一句为什么",
    ],
    "standards": [
        {"content": "诚实守信，友善待人，尊重他人，有集体意识和责任感。",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学 道德修养"},
        {"content": "学习伴我成长；我学习我快乐；学习有方法",
         "source": "统编《道德与法治》三年级上册「做学习的主人」"},
    ],
    "prereqs": ["pol-e-g2-u4"],
    "prereqs_name": "我爱我们的祖国",
    "prereqs_meta": "pol-e-g2-u4",
    "leads_to": ["pol-e-g3-u2"],
    "next_meta": "pol-e-g3-u2",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "同样一份作业，有人半小时写完，有人拖到睡前——差别常常不在聪明，而在有没有方法。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能给自己排一份放学后的小计划。",
        "objectives": "看清四件事：学习在哪里发生、时间怎么排、不会的题怎么办、为什么比是什么更要紧。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "学习是从不会到会的过程，不只在课堂；多问一句为什么，比只记住答案更牢。",
        "lab-1": "六件事，每件三个做法。选得不太合适也不会说你错，只会告诉你还可以试试什么。",
        "module-2": "自己排时间、不会的题分步来、多问为什么、学完回头看——方法用几次就成自己的。",
        "lab-2": "把四张步骤卡按你觉得对的顺序点下去：先想、再看、再问、再记。点错了会告诉你为什么。",
        "worked-example": "小雨的傍晚四步：看清条件、排好顺序、遇到难题先记号、回头问清楚再写一遍。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "把八条放学后的做法分进「会学习的」和「要调整的」两个筐，分完读一读为什么。",
        "posttest": "出现了时间不够用、不认识的词、同学的看法，看看你还能不能用上今天的办法。",
        "summary": "四句话：学习在哪里、自己排时间、不会的题分步来、多问一句为什么。",
        "homework": "三层小任务，先做前两层，第三层可以请家里人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学道德与法治「道德修养」板块在三年级的空缺，正对统编教材三年级上册「做学习的主人」（学习伴我成长、我学习我快乐、学习有方法）。三年级学生的难处不在不懂道理，而在「知道具体该怎么做」——所以全课不讲抽象口号，只做三件能落地的事：一是弄明白学习是从「不会」到「会」的过程，多问一句为什么比只记住答案更牢；二是自己安排时间，先做要紧的事、做完检查一遍；三是遇到不会的题按「先想、再看、再问、再记」四步走，实在想不出来先做记号、把会的做完再回头。三个互动台子都能真操作：一个是六张「放学以后」情境卡，选做法后给即时反馈，反馈一律写成「这样可能会……，还可以试试……」，不判错、不贴标签；一个是「遇到不会的题」四步排序，把打乱的步骤卡按正确顺序排成一队，点错时说明为什么这一步放早了；一个是综合任务，把八条做法分进「会学习的／要调整的」两个筐。全课以具体动作收口，插图一律为中性简洁扁平插画，不使用真实儿童照片。",
    "plan_table": """| 1 | cover | 做学习的主人 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 学习伴我成长：学习不只在课堂上 | 承·概念一（学习在哪里发生 + 为什么比是什么重要） |
| 6 | interactive | 动手一：放学以后，你会怎么做？ | 承·情境判断（温和反馈，不判错） |
| 7 | concept | 我学习我快乐 · 学习有方法 | 承·概念二（时间安排 + 难题四步 + 学完回头看） |
| 8 | interactive | 动手二：遇到不会的题，四步来 | 承·步骤排序（先想 / 再看 / 再问 / 再记） |
| 9 | concept | 例题示范：小雨的一个傍晚 | 转·重难点突破（分步示范 + 易错点） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：会学习的 / 要调整的，把做法分进两个筐 | 合·迁移应用（分类判断） |
| 12 | quiz | 后测：换几个新情境，办法还在不在 | 合·后测 |
| 13 | summary | 小结：四句话，讲清怎么当学习的主人 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：学习伴我成长 / 我学习我快乐 / 学习有方法 三栏\n- P5 学习发生的地方概念图（已生成）：课堂上、家里、路上都在学习，从不会到会，附中文标注\n- P7 难题四步图（已生成）：先想 → 再看 → 再问 → 再记，附中文标注\n- 三张图均为中性简洁扁平教学插画，不使用真人照片风格，不含可识别的真实人物\n- 若需补充：本校作息时间表（需学校提供并授权后使用）",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
