# -*- coding: utf-8 -*-
"""小学道德与法治 · 过好校园生活（G1）—— 补齐知识树「中华优秀传统文化」空缺

学科语气（道德与法治）：情境案例驱动，情感共鸣 + 价值判断；结论落在「应该怎么做、为什么」，
不做道德说教。
一年级落点：全部换成能看见的具体动作和具体的话（进教室问一声老师您好、借东西先说请问、
碰倒了水杯说对不起）。互动反馈一律展开「对方的感受与后果」，写成「这样可能会……，
还可以试试……」。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g1-u2"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "小朋友，上一节课我们认了校园里的地方，也学会了上学路上要怎么做。这节课我们来说一件更近的事：和老师、和同学在一起的时候，话该怎么说、事该怎么做。见到老师问一声老师您好，想借东西先说一句请问，碰倒了水杯就说对不起。上课的时候好好学，课余的时候开开心心玩。学完你会发现，礼貌的一句话，会让别人心里暖暖的，也会让校园生活过得更好。",
    "problem-anchor": "开始之前，先选一个你最想弄清楚的问题。是想知道见到老师该怎么说，还是想知道怎么和新同学交朋友；是想知道上课的时候要做好哪几件事，还是想知道课余时间可以怎么安排。选好了，就带着它往下看。",
    "objectives": "这节课有四个小目标。第一，见到老师会主动问好，别人帮了我会说谢谢，有事会找老师说。第二，会用请问、谢谢、对不起、没关系这几句话，知道说哪一句要看当时发生的事。第三，能说出上课的时候要做到的几件事，做到好好学。第四，能说出课余时间可以做的活动，把课余生活安排得又开心又有意思。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先说说和老师在一起的时候。早上走进教室，看见老师，走上前问一声老师您好。上课以前，全班一起起立，向老师问好。老师帮你解决了问题，说一句谢谢老师。有不懂的地方，或者身体不舒服，就走到老师身边，把话慢慢说清楚。一句问好、一句谢谢，说出来一点也不难，却能让老师知道，你把他放在心上。",
    "lab-1": "现在请你当一次校园小主人。这里有一天里可能遇到的六件事，每一件事都有三个做法。你选一个你觉得合适的，选完立刻会有一段话，告诉你这样做了以后，老师或者同学心里会是什么感觉；要是选得不太合适，也会告诉你还可以试试什么。",
    "module-2": "接下来说说和同学在一起的时候。想和别人做朋友，先走过去打个招呼，再说一句你好，问问他叫什么名字，然后邀请他一起玩。想用同学的东西，先问一句请问可以借我用一下吗，用完了说谢谢，还要还回去。不小心碰倒了同学的水杯，说一句对不起，再帮他把水擦干净。答应了同学的事情，就要做到。这几句话谁都会说，难的是在该说的时候说出来。",
    "lab-2": "现在我们来做一次这样说、那样的对比。下面有六件事，每一件都有两种说法。请你先选一种，看看同学心里会是什么感觉，再看看换一种说法会怎么样。同一件事，话说得不一样，结果常常很不一样。",
    "worked-example": "我们一起来帮小语想一想。第一步，小语想借同桌的橡皮，他先轻轻问了一句请问能借我用一下你的橡皮吗，同桌点点头，他拿到以后说了谢谢。第二步，下课时小语不小心碰倒了同桌的水杯，他马上说对不起，是我碰到的，然后和同桌一起把桌子擦干净。第三步，上课的时候老师提了一个问题，小语知道答案，他先举手，等老师请他，再站起来说。第四步，课间他没说完的话还想说，就跟同桌约好下课再聊，上课的时候先把话放在心里。",
    "conceptest-1": "接下来用三个说法考考你，每个说法里都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件事交给你。下面有八件事，请你判断一下：哪些是上课的时候要做的，放进上课了好好学这一边；哪些是课余时间可以做的，放进课余生活真丰富那一边。放好以后，再读一读为什么。",
    "posttest": "最后一轮，换几个新的小情境来考考你。这次会出现新来的同学、说错的一句话、还有一件答应过的事，看看你能不能用上今天学到的办法。",
    "summary": "这节课我们记住三句话。第一句，敬爱老师，从一句老师您好开始：见到老师问声好，别人帮了我说谢谢，有不懂的事就走到老师身边问清楚。第二句，友善待人，从一句请问开始：借东西先问，碰倒了说对不起，答应了的事要做到，同学有困难就帮一把。第三句，上课的时候好好学，眼睛看老师、想说话先举手；课余的时候好好玩，可以看书、做游戏、参加班里的活动。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出对老师要做的三件事，再说出请问、谢谢、对不起这三句话分别用在什么时候。第二层能力应用，动手做：和爸爸妈妈一起想一想，在家里说话也可以更礼貌，找出三句可以换一换的话，说给他们听。第三层迁移挑战，选做：给班里设计一张礼貌用语小海报，写四句话，画上插图，贴在教室的墙上。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 老师，您好！", "lab-1": "动手一 校园小主人", "module-2": "概念二 拉拉手，交朋友",
    "lab-2": "动手二 这样说，那样说", "worked-example": "例题讲解 小语的课间", "conceptest-1": "概念测试",
    "synthesis": "综合任务 上课好好学 · 课余真丰富", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：校园一天，六个情境 × 三个做法（反馈展开对方的感受与后果） ──
SCENES = [
    {
        "id": "s1",
        "t": "早上走进教室，我看见了老师",
        "opts": [
            {"k": "a", "t": "走上前，问一声「老师，您好！」", "ok": True,
             "fb": "老师心里暖暖的，一天的开头都亮了起来。一句问好只要一两秒，却能让老师知道你已经把他放在心上。"},
            {"k": "b", "t": "低头走到自己的座位上，不吭声", "ok": False,
             "fb": "老师可能会以为你有心事，想关心你又怕打扰你。还可以试试：抬起头，走到老师身边，轻轻说一声老师您好。"},
            {"k": "c", "t": "隔着好几排大声喊「老师——」", "ok": False,
             "fb": "老师会被突然提高的声音吓一跳，旁边的同学也会停下来看你。还可以试试：走到老师身边，用好听的声音问好。"},
        ],
    },
    {
        "id": "s2",
        "t": "上课铃响了，老师说上课",
        "opts": [
            {"k": "a", "t": "和全班一起起立，向老师问好", "ok": True,
             "fb": "全班一起问好，老师会觉得很受尊重，也很愿意带着大家好好上课。"},
            {"k": "b", "t": "坐着不动，等着老师开始讲", "ok": False,
             "fb": "老师看到只有你没站起来，心里会有点失落。还可以试试：听到起立，就和大家一起站起来，问一声老师您好。"},
            {"k": "c", "t": "一边起立一边和同桌打闹", "ok": False,
             "fb": "这样会让教室里变得乱糟糟的，老师要花时间让大家安静下来，上课的时间就变少了。还可以试试：站直、站稳，等老师说完再坐下。"},
        ],
    },
    {
        "id": "s3",
        "t": "老师帮我解决了问题",
        "opts": [
            {"k": "a", "t": "说一句「谢谢老师」", "ok": True,
             "fb": "老师会觉得自己的帮忙被看见了，心里很舒服。会说谢谢，是很懂事的做法。"},
            {"k": "b", "t": "转身就走，反正问题解决了", "ok": False,
             "fb": "老师帮了忙却没听到一句话，心里会有点凉。还可以试试：转过身来，看着老师，说一声谢谢老师。"},
            {"k": "c", "t": "大声说「这么简单，我也会」", "ok": False,
             "fb": "老师帮了你，却听到这样一句话，会有点难过。还可以试试：先说谢谢老师，再把你自己的想法说给老师听。"},
        ],
    },
    {
        "id": "s4",
        "t": "同桌的橡皮掉在我脚边",
        "opts": [
            {"k": "a", "t": "捡起来，还给他，说一句「给你」", "ok": True,
             "fb": "同桌会觉得很贴心，下次他也会愿意帮你。帮一个小忙，两个人心里都舒服。"},
            {"k": "b", "t": "看见了，当成没看见", "ok": False,
             "fb": "同桌要弯着腰找好一会儿，心里会有点着急。还可以试试：弯腰捡起来，送到他手上。"},
            {"k": "c", "t": "踢到同桌的桌子底下，逗他一下", "ok": False,
             "fb": "同桌会以为你在捉弄他，心里会不高兴。还可以试试：捡起来还给他，想逗他开心可以用别的方式。"},
        ],
    },
    {
        "id": "s5",
        "t": "我不小心碰倒了同学的水杯",
        "opts": [
            {"k": "a", "t": "说一句「对不起」，和大家一起把桌子擦干净", "ok": True,
             "fb": "同学会觉得你是个诚实、肯负责的人，心里那点不痛快很快就过去了。"},
            {"k": "b", "t": "赶紧走开，假装不是我碰的", "ok": False,
             "fb": "同学要自己收拾桌子，心里会有点难过。还可以试试：留下来，说一句对不起，帮他把桌子擦一擦。"},
            {"k": "c", "t": "说「是桌子太窄了，不怪我」", "ok": False,
             "fb": "同学听到这句话，可能会更不舒服。还可以试试：先承认是自己不小心，再说一句对不起。"},
        ],
    },
    {
        "id": "s6",
        "t": "我答应了同学，明天带贴纸给他",
        "opts": [
            {"k": "a", "t": "第二天把贴纸带来，交到他手上", "ok": True,
             "fb": "同学会觉得你说话算数，以后更愿意相信你。答应过的事做到了，就是讲诚信。"},
            {"k": "b", "t": "忘记了，第二天什么也没说", "ok": False,
             "fb": "同学等了一天，会有点失落。还可以试试：想起来以后马上说一句对不起，然后约好明天一定带来。"},
            {"k": "c", "t": "第二天说「我昨天没答应过呀」", "ok": False,
             "fb": "同学会觉得你不认账，心里很不好受。还可以试试：说实话，说一句对不起，是我忘了。"},
        ],
    },
]

# ── 动手二：这样说，那样说（同一件事，两种说法 → 对方的感受） ──
SITUATIONS = [
    {
        "id": "p1",
        "t": "想借同桌的橡皮用一下",
        "good": {"t": "「请问，能借我用一下你的橡皮吗？」",
                 "feel": "同桌心里很舒服：他先问过我，说明他尊重我。我很愿意借给他。"},
        "bad": {"t": "「哎，橡皮给我！」",
                "feel": "同桌心里有点不舒服：他连问都没问。这样可能会让同桌不太想借；还可以试试先说一句「请问，能借我用一下吗」。"},
    },
    {
        "id": "p2",
        "t": "不小心碰倒了同学的水杯",
        "good": {"t": "「对不起，是我碰倒的，我帮你一起擦干净。」",
                 "feel": "同学心里一松：他承认了，还愿意帮忙。那点不痛快很快就过去了。"},
        "bad": {"t": "「不是我，是它自己倒的。」",
                "feel": "同学心里很不是滋味：明明看见了，他却不肯认。这样可能会让同学以后不敢把东西放在你旁边；还可以试试说实话，说一句对不起。"},
    },
    {
        "id": "p3",
        "t": "我举了手，老师没请到我",
        "good": {"t": "「那我先听听别人怎么说，下次再举手。」",
                 "feel": "老师会觉得你很有耐心，也愿意回答别的同学。等一等，下次机会就是你的。"},
        "bad": {"t": "「老师总是不叫我，我不举手了！」",
                "feel": "老师会觉得有点为难：班里同学多，一次只能请一位。这样可能会让你错过下次的机会；还可以试试把手继续举好。"},
    },
    {
        "id": "p4",
        "t": "跑步比赛，我输给了同学",
        "good": {"t": "「你跑得真快！下次我们再来一次。」",
                 "feel": "同学心里很高兴：赢了还被人真心夸奖。你们俩下次还愿意一起玩。"},
        "bad": {"t": "「你肯定是作弊了，不算！」",
                "feel": "同学会很委屈：明明是他自己跑赢的。这样可能会让他下次不想和你比赛；还可以试试先夸他一句，再约下一次。"},
    },
    {
        "id": "p5",
        "t": "我想玩同学带来的新玩具",
        "good": {"t": "「你的玩具真好看，我可以玩一会儿吗？」",
                 "feel": "同学心里很乐意：他先问了我，我可以决定借不借。多半他会说可以。"},
        "bad": {"t": "「我先玩，玩够了再还你。」",
                "feel": "同学心里会有点着急：那是我带来的东西，还没轮到我玩。这样可能会让他以后不想带来学校；还可以试试先问一句可以不可以。"},
    },
    {
        "id": "p6",
        "t": "新同学一个人坐在座位上",
        "good": {"t": "「你好，我叫小语，要不要一起去玩？」",
                 "feel": "新同学心里一下子暖了：原来有人愿意和我做朋友。一句你好，就能让人不再孤单。"},
        "bad": {"t": "「他一个人坐着，肯定是不想和别人玩。」",
                "feel": "新同学会一直孤单下去，其实他只是还没找到说话的人。这样可能会让你错过一个好朋友；还可以试试先走过去打个招呼。"},
    },
]

# ── 综合任务：上课了，好好学 · 课余生活真丰富（分进两个筐） ──
SORT_ITEMS = [
    {"id": "c1", "t": "坐好，眼睛看着老师，耳朵认真听", "bin": "class",
     "why": "上课的时候看老师、认真听，学得最清楚。这是上课要做的第一件事。"},
    {"id": "c2", "t": "想说话先举手，老师请我再讲", "bin": "class",
     "why": "举手是一种不打扰别人的说话方式。老师请到你，全班都会安静听你说。"},
    {"id": "c3", "t": "同学发言的时候认真听，不插嘴", "bin": "class",
     "why": "认真听同学发言，他会觉得自己被尊重，你也多学了一遍。"},
    {"id": "c4", "t": "一笔一笔把字写清楚，写完检查一遍", "bin": "class",
     "why": "认真写好每一个字，是上课好好学最实在的样子，作业也更好看。"},
    {"id": "c5", "t": "课间先喝好水、上好厕所", "bin": "break",
     "why": "课余先把身体的事情做好，下一节课才能安心。"},
    {"id": "c6", "t": "课间和同学一起跳皮筋、做游戏", "bin": "break",
     "why": "课余和同学一起活动，身体动起来，心里也开心，还能交到好朋友。"},
    {"id": "c7", "t": "去图书角看一本图画书", "bin": "break",
     "why": "课余时间也可以安安静静地看书，这是很好的一种休息。"},
    {"id": "c8", "t": "参加班里组织的活动，比如合唱排练", "bin": "break",
     "why": "班里一起做事，自己出一份力，这就是爱护集体。"},
]
SORT_BIN = {"class": "上课了，好好学", "break": "课余生活真丰富"}

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g1-u2 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 校园小主人：六个情境 × 三个做法 → 展开对方的感受与后果
   3) 这样说，那样说：同一件事两种说法 → 同学的感受
   4) 上课了好好学 · 课余真丰富：八条做法分进两个筐
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

  /* ---------- 2. 校园小主人 ---------- */
  var SCENES = __SCENES_JSON__;
  var stage1 = document.getElementById('host-stage');
  if (stage1) {
    var curScene = null, doneScene = {};
    var out1 = document.getElementById('host-out');

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
      document.getElementById('host-score').textContent = '已经聊过 ' + n + ' / ' + SCENES.length + ' 件事';
    }
    function paintOptions() {
      var box = document.getElementById('host-opts');
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
            out1.innerHTML = '<strong>这样做了以后——</strong>' + o.fb;
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
          out1.innerHTML = '<strong>这件事已经聊过啦。</strong>你上次选的做法很合适，记住它就好。';
        } else {
          out1.className = 'result warn';
          out1.innerHTML = '<strong>你遇到的是：' + S.t + '</strong><br>下面有三个做法，你选一个试试看，再看看对方心里会怎么想。';
        }
        render1();
        paintOptions();
      });
    });
    render1();
  }

  /* ---------- 3. 这样说，那样说 ---------- */
  var SITS = __SITS_JSON__;
  var stage2 = document.getElementById('say-stage');
  if (stage2) {
    var curSit = null, talked = {};
    var out2 = document.getElementById('say-out');

    function sitById(id) {
      for (var i = 0; i < SITS.length; i++) { if (SITS[i].id === id) return SITS[i]; }
      return null;
    }
    function render2() {
      document.querySelectorAll('[data-sit]').forEach(function (b) {
        var k = b.dataset.sit;
        b.classList.toggle('selected', k === curSit);
        b.classList.toggle('correct', !!talked[k]);
      });
      var n = Object.keys(talked).length;
      document.getElementById('say-score').textContent = '已经聊过 ' + n + ' / ' + SITS.length + ' 件事';
    }
    function paintWays() {
      var box = document.getElementById('say-ways');
      box.innerHTML = '';
      if (!curSit) return;
      var S = sitById(curSit);
      if (!S) return;
      [['good', S.good, '这样说'], ['bad', S.bad, '那样说']].forEach(function (pair) {
        var kind = pair[0], W = pair[1], label = pair[2];
        var b = document.createElement('button');
        b.className = 'choice';
        b.style.textAlign = 'left';
        b.textContent = label + '：' + W.t;
        b.addEventListener('click', function () {
          if (kind === 'good') {
            talked[curSit] = true;
            out2.className = 'result';
            out2.innerHTML = '<strong>这样说，同学心里是这样的：</strong>' + W.feel;
          } else {
            out2.className = 'result warn';
            out2.innerHTML = '<strong>那样说，同学心里是这样的：</strong>' + W.feel;
          }
          render2();
          paintWays();
        });
        box.appendChild(b);
      });
    }
    document.querySelectorAll('[data-sit]').forEach(function (b) {
      b.addEventListener('click', function () {
        curSit = b.dataset.sit;
        var S = sitById(curSit);
        out2.className = 'result warn';
        out2.innerHTML = '<strong>现在遇到的是：' + S.t + '</strong><br>下面有两种说法，先选一种，看看同学心里会是什么感觉。';
        render2();
        paintWays();
      });
    });
    render2();
  }

  /* ---------- 4. 上课了好好学 · 课余真丰富 ---------- */
  var ITEMS = __SORT_JSON__;
  var BINN = __SORTBIN_JSON__;
  var stage3 = document.getElementById('time-stage');
  if (stage3) {
    var pickItem = null, placed = {};
    var out3 = document.getElementById('time-out');

    function render3() {
      document.querySelectorAll('[data-item]').forEach(function (b) {
        var k = b.dataset.item;
        b.classList.toggle('selected', k === pickItem);
        b.classList.toggle('done', !!placed[k]);
        b.disabled = !!placed[k];
      });
      var n = Object.keys(placed).length;
      document.getElementById('time-score').textContent = '已经放好 ' + n + ' / ' + ITEMS.length + ' 条';
      var cBox = document.getElementById('time-bin-c');
      var bBox = document.getElementById('time-bin-b');
      cBox.innerHTML = ''; bBox.innerHTML = '';
      ITEMS.forEach(function (it) {
        if (!placed[it.id]) return;
        var s = document.createElement('div');
        s.className = 'tag';
        s.textContent = it.t;
        (it.bin === 'class' ? cBox : bBox).appendChild(s);
      });
      if (!cBox.innerHTML) cBox.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
      if (!bBox.innerHTML) bBox.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
    }
    document.querySelectorAll('[data-item]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (placed[b.dataset.item]) return;
        pickItem = b.dataset.item;
        out3.className = 'result warn';
        out3.innerHTML = '<strong>你选的是：' + b.textContent + '</strong><br>想一想，它是上课的时候要做的，还是课余时间可以做的？';
        render3();
      });
    });
    document.querySelectorAll('[data-time-bin]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pickItem) {
          out3.className = 'result warn';
          out3.textContent = '先在上面点一条做法，再选筐。';
          return;
        }
        var it = null;
        for (var i = 0; i < ITEMS.length; i++) { if (ITEMS[i].id === pickItem) it = ITEMS[i]; }
        if (b.dataset.timeBin === it.bin) {
          placed[it.id] = true;
          out3.className = 'result';
          out3.innerHTML = '<strong>放对了，它属于「' + BINN[it.bin] + '」。</strong>' + it.why;
          pickItem = null;
          if (Object.keys(placed).length === ITEMS.length) {
            out3.className = 'result';
            out3.innerHTML = '<strong>八条全放对了！</strong>记一句口诀：<strong>上课看老师，举手再发言；课间喝好水，活动真开心——该学的时候好好学，该玩的时候好好玩。</strong>';
          }
        } else {
          out3.className = 'result warn';
          out3.innerHTML = '<strong>再想一想这一条。</strong>' + it.why +
            '<br><span style="color:var(--muted)">常见错误：容易把「课间要做的事」和「上课要做的事」搞混——上课是学的时候，课余是活动和休息的时候。再试一次。</span>';
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
             .replace('__SITS_JSON__', json.dumps(SITUATIONS, ensure_ascii=False))
             .replace('__SORT_JSON__', json.dumps(SORT_ITEMS, ensure_ascii=False))
             .replace('__SORTBIN_JSON__', json.dumps(SORT_BIN, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "早上走进教室，看见老师，怎么做比较合适？",
         "options": [("走上前，问一声「老师，您好！」", True),
                     ("低头走到自己的座位上，不吭声", False),
                     ("隔着好几排大声喊老师", False)],
         "explain": "走上前问一声好，老师心里暖暖的，一天的开头都亮了起来。"
                    "<strong>错因提醒：</strong>有人误认为「问好是小事，做不做都行」——正是这句小事，让老师和同学知道你心里有别人。"},
        {"q": "我想借同桌的橡皮用一下，怎么说更好？",
         "options": [("「请问，能借我用一下你的橡皮吗？」", True),
                     ("「哎，橡皮给我！」", False),
                     ("直接拿走，用完再还回去", False)],
         "explain": "先问一句「请问」，同桌会觉得自己被尊重，很愿意借给你。"
                    "<strong>错因提醒：</strong>常见错误是把「想要」和「直接拿」搞混了——先说一句请问，事情就顺了。"},
        {"q": "我不小心碰倒了同学的水杯，下面哪个做法更好？",
         "options": [("说一句「对不起」，和大家一起把桌子擦干净", True),
                     ("赶紧走开，假装不是我碰的", False),
                     ("说「是桌子太窄了，不怪我」", False)],
         "explain": "承认是自己不小心，再说一句对不起，同学心里那点不痛快很快就过去了。"
                    "<strong>错因提醒：</strong>容易误认为「只要不是故意的就不用说对不起」——别人在意的不是故不故意，而是你有没有把这件事放在心上。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "老师，您好！敬爱老师，从一声问好开始", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们已经知道，遇到不认识的事情可以问老师，老师也会帮我们（And）；可是有的同学看见老师不敢说话，老师帮了忙也不知道该说什么，明明心里挺感谢，话却没说出来（But）；所以这节课就来学一学，和老师说话的时候，那几句最简单的话该怎么讲（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">敬爱老师，不需要做很大的事。它就藏在<strong>三句很短的话</strong>里，每一句都只要一两秒钟。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>见到老师问声好：</strong>早上走进教室，或者上课铃响全班起立，主动说一句「老师，您好！」——不用别人提醒就开口，这个做法<strong>叫做主动问好</strong>。</div></div>
          <div class="step"><span class="n">2</span><div><strong>别人帮了我说谢谢：</strong>老师帮你捡起铅笔、帮你解决了难题，说一句「谢谢老师」。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>有不懂的就去问：</strong>听不懂，或者身体不舒服，走到老师身边，把话慢慢说清楚。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="校园里向老师问好的示意图：进教室问好、上课起立问好、说谢谢，附中文标注">
          <figcaption>示意图：敬爱老师的三句话——早上问一声老师您好 · 上课起立问好 · 别人帮忙说谢谢（教学示意图，人物为极简线条）</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🌻</span><div><strong>记一句小口诀：</strong>见面问声好，帮忙说谢谢，不懂就去问——<strong>话说出来，老师才知道。</strong></div></div>
{insight_box([
    {"lens": "看见它", "text": "敬爱老师不是一句口号，它就是三个能看见的动作：走过去、抬起头、把话说出来。"},
    {"lens": "解释它", "text": "为什么一句问好能让老师高兴？因为老师一天要面对很多同学，一句问好是他收到的回应——他知道自己被看见了。"},
    {"lens": "迁移它", "text": "回到家里也一样：出门说一声我去上学啦，回家说一声我回来了，家里人帮了忙说一声谢谢。地方换了，话没变。"},
])}
    ''', tag="概念一"))

    scene_btns = "\n".join(
        f'            <button class="choice" data-scene="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in SCENES
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：校园小主人，你会怎么做？", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一件你今天可能遇到的事，再从三个做法里选一个。<strong>选完会告诉你，这样做了以后老师和同学心里是什么感觉。</strong></p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 今天我遇到的一件事</div>
          <div class="grid" id="host-stage">
{scene_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 我可以怎么做</div>
          <div class="grid" id="host-opts">
            <span style="color:var(--muted);font-size:14px">先在上面点一件事，这里就会出现三个做法。</span>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">聊过几件事</span><span class="v" id="host-score">已经聊过 0 / 6 件事</span></div>
          </div>
          <p class="result warn" id="host-out" style="margin-top:12px">先点一件今天可能遇到的事。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💛</span><div><strong>说给你听：</strong>这里的做法没有分数。有些做法只是会让别人心里不太舒服，换一个试试就好。想一想对方的心情，比记住「应该怎么做」更要紧。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "拉拉手，交朋友：友善待人，从一句「请问」开始", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">交朋友不靠什么特别的法子，就靠<strong>几句话</strong>。这几句话谁都会说，难的是在该说的时候说出来。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>想和别人做朋友</strong></p>
            <p style="color:var(--muted)">走过去，打个招呼，说一句「你好，我叫……」；问问他叫什么名字；再邀请他一起玩。</p>
          </div>
          <div class="inner-card">
            <p><strong>想用别人的东西</strong></p>
            <p style="color:var(--muted)">先说「请问，能借我用一下吗」；用完了说谢谢，还要记得还回去。</p>
          </div>
          <div class="inner-card">
            <p><strong>做错了事</strong></p>
            <p style="color:var(--muted)">说一句「对不起」，再动手把事情补回来。帮别人一起收拾，比只说一句话更有用。</p>
          </div>
          <div class="inner-card">
            <p><strong>答应过的事</strong></p>
            <p style="color:var(--muted)">说到就要做到。真的忘了，就老实说一句对不起，再约好什么时候补上——这就是讲诚信。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="交朋友的四句礼貌用语示意图：你好、谢谢、对不起、没关系，附中文标注">
          <figcaption>示意图：交朋友的四句话——「你好」是开始 ·「谢谢」是回应 ·「对不起」是担当 ·「没关系」是宽容（教学示意图，人物为极简线条）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「说对不起很丢人」。其实肯说对不起的人，才是敢担当的人；而且说完对不起，还要动手把事情补回来，这才算说完整。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🤝</span><div><strong>记一句口诀：</strong>你好、谢谢、对不起、没关系——<strong>四句话记住了，朋友就多了。</strong></div></div>
{insight_box([
    {"lens": "比较它", "text": "同一件事，两种说法：一句「请问，能借我用一下吗」，和一句「哎，给我」。差别不在声音大小，而在有没有把对方放在心上。"},
    {"lens": "解释它", "text": "为什么礼貌的话有用？因为它把选择权交给了对方——先问一句，别人就有机会说愿意，也有机会说不愿意。"},
    {"lens": "迁移它", "text": "在家里、在公交车上、在小区里，这几句话一样管用。你希望别人怎么对你说话，就先那样对别人说话。"},
])}
    ''', tag="概念二"))

    sit_btns = "\n".join(
        f'            <button class="choice" data-sit="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in SITUATIONS
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：这样说，那样说，看看对方心里怎么想", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一件发生在校园里的事，再看看两种说法。选一种，读一读同学心里是什么感觉。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 发生了什么事</div>
          <div class="grid" id="say-stage">
{sit_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 这样说，还是那样说</div>
          <div class="grid" id="say-ways">
            <span style="color:var(--muted);font-size:14px">先在上面点一件事，这里就会出现两种说法。</span>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">聊过几件事</span><span class="v" id="say-score">已经聊过 0 / 6 件事</span></div>
          </div>
          <p class="result warn" id="say-out" style="margin-top:12px">先在上面点一件事。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">👂</span><div><strong>换位想一想：</strong>如果那句话是说给你听的，你心里会是什么感觉？能想到这一点，你就已经会替别人着想了。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小语的课间", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>小语今天在班里遇到了四件事。请你帮他一件一件想清楚，该怎么说、怎么做。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>想借橡皮：</strong>先轻轻问一句「请问能借我用一下你的橡皮吗」，同桌点点头，拿到以后说一句谢谢。</div></div>
          <div class="step"><span class="n">2</span><div><strong>碰倒水杯：</strong>马上说「对不起，是我碰到的」，然后和同桌一起把桌子擦干净。</div></div>
          <div class="step"><span class="n">3</span><div><strong>上课发言：</strong>知道答案也先举手，等老师请到自己，再站起来说。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>话还没说完：</strong>和同桌约好下课再聊，上课的时候先把想说的话放在心里。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「不说话、不惹事就是个好孩子」。其实同学摔倒了不扶、同桌找东西不帮、有话想说不说，别人也会觉得有点孤单。真正友善的人，是<strong>该开口的时候开口</strong>。</p>
        </div>
        <div class="inner-card">
          <p><strong>说给同桌听：</strong>小语这四步里，哪一步你自己已经做到了？哪一步还想再练一练？</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "下面哪句话说得对？",
         "options": [("借别人的东西，要先问一句「请问可以吗」", True),
                     ("同学的东西放在桌上，拿着用一下没关系", False),
                     ("只要东西还回去了，问不问都一样", False)],
         "explain": "先问一句，是把选择的机会交给对方，这是对别人的尊重。"
                    "<strong>错因提醒：</strong>常见错误是误认为「只要还回去就不算错」——别人在意的，是有没有先问过他。"},
        {"q": "我不小心把同学的作业本弄湿了，下面哪个做法更好？",
         "options": [("说一句「对不起」，再和他一起想办法把本子晾干", True),
                     ("偷偷把本子放回去，不说话", False),
                     ("说「反正只是一点水，没什么关系」", False)],
         "explain": "说对不起，再动手把事情补回来，这才是说完整的一句话。"
                    "<strong>错因提醒：</strong>容易搞混「不是故意的」和「不用负责」——不是故意的，也要说对不起、也要帮忙补回来。"},
        {"q": "我答应了同学，明天带一本图画书给他看，可是第二天忘了。下面哪个做法更好？",
         "options": [("老实说「对不起，我忘了」，再约好明天一定带来", True),
                     ("假装没有说过这件事", False),
                     ("说「那本书被我弄丢了」", False)],
         "explain": "答应过的事要做到；真的忘了，就老实承认，再补上。说实话的人，别人才会一直相信他。"
                    "<strong>错因提醒：</strong>有人误认为「撒个小谎就过去了」——一个谎要接上另一个谎，心里会很累，诚实反而最轻松。"}
    ], tag="概念测试"))

    item_btns = "\n".join(
        f'            <button class="sort-item" data-item="{it["id"]}">{it["t"]}</button>' for it in SORT_ITEMS
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：上课好好学，课余真丰富，把做法分进两个筐", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一条做法，再点它应该进的筐：<strong>上课的时候要做的</strong>放一边，<strong>课余时间可以做的</strong>放另一边。</p>
        <div class="lab-panel">
          <div class="sort-bank" id="time-stage">
{item_btns}
          </div>
          <div class="grid grid-2" style="margin-top:14px">
            <button class="choice" data-time-bin="class" style="text-align:center">上课了，好好学</button>
            <button class="choice" data-time-bin="break" style="text-align:center">课余生活真丰富</button>
          </div>
          <div class="sort-bins">
            <div class="sort-bin" id="time-bin-c"><h4>上课了，好好学</h4></div>
            <div class="sort-bin" id="time-bin-b"><h4>课余生活真丰富</h4></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">分类进度</span><span class="v" id="time-score">已经放好 0 / 8 条</span></div>
          </div>
          <p class="result warn" id="time-out" style="margin-top:12px">先在上面点一条做法。</p>
        </div>
        <div class="inner-card">
          <p><strong>分完之后，想一想：</strong></p>
          <p style="color:var(--muted)">课余时间你最喜欢做哪一件事？和谁一起做？把它写下来，明天讲给同桌听。</p>
          <textarea id="syn-answer" rows="3" placeholder="课余我最喜欢……，我想和……一起……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，做法还在不在", TTS["posttest"], [
        {"q": "班里来了一位新同学，一个人坐在座位上，你会：",
         "options": [("走过去打个招呼，问他要不要一起玩", True),
                     ("远远看着他，等他自己过来", False),
                     ("跟别人说他不爱说话", False)],
         "explain": "一句你好，就能让新同学知道自己是被欢迎的。"
                    "<strong>错因提醒：</strong>别把「他没说话」当成「他不想交朋友」——先打个招呼，再看他怎么回应，这样更公平。"},
        {"q": "课间我不小心说了一句让同桌不高兴的话，说完就发现了，你会：",
         "options": [("马上说一句「对不起，我刚才说错了」", True),
                     ("反正他还没生气，就不提了", False),
                     ("等他也说我一句，就扯平了", False)],
         "explain": "发现自己说错了，越早说对不起越好，事情不会拖大。"
                    "<strong>错因提醒：</strong>常见错误是误认为「他不说就说明没事」——有些难过藏在心里，说出来别人才能放下。"},
        {"q": "班里要出黑板报，老师问谁愿意帮忙，你会：",
         "options": [("举手报名，按老师安排做好自己那一份", True),
                     ("想去，但怕做不好就不举手", False),
                     ("让别人做，自己在旁边看着", False)],
         "explain": "班里的事大家一起做，自己出一份力，这就是爱护集体。做得不完美也没关系，老师和同学会帮你。"
                    "<strong>错因提醒：</strong>有人误认为「做不好就别参加」——集体的事情，重要的是愿意一起做，不是一开始就做得好。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，讲清怎么过好校园生活", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>敬爱老师：</strong>见面问声好，帮忙说谢谢，有不懂的事就走到老师身边问清楚。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>友善待人：</strong>借东西先说请问，做错了说对不起并补回来，答应了的事要做到，同学有困难帮一把。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>过好一天：</strong>上课好好学——看老师、先举手；课余好好玩——喝水、活动、看书、参加班里的活动。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>还要记牢一件事：</strong>这几句话谁都会说，难的是在该说的时候说出来。今天先挑一句试试——比如明天早上走进教室，主动跟老师说一声「老师，您好」。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「问好、请问、对不起」这三个词，说清楚你今天在班里做对的一件事。</p>
          <p style="color:var(--muted)">再动一动手：<strong>写一写</strong>你打算明天先做到的那一句话，写在纸上，放学带回家给家里人看看。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "说出对老师要做的三件事，每件用一句话说清楚。",
            "说出「请问、谢谢、对不起」这三句话，分别用在什么时候。",
        ],
        [
            "和家里人一起想一想：在家里说话也可以更礼貌，找出三句可以换一换的话，说给他们听。",
            "把「这样说，那样说」里的两件事讲给家里人听，请他们说说听到哪句话心里更舒服。",
        ],
        [
            "给班里设计一张礼貌用语小海报，写四句话，画上插图，贴在教室的墙上。",
            "找一找班里最近有没有需要帮忙的地方（比如同桌在找东西、同学搬不动椅子），主动帮一次，第二天说给同桌听。",
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
    "title": "过好校园生活",
    "name_en": "Living Well at School Day by Day",
    "grade": 1,
    "grade_cn": "一年级",
    "domain": "tradition-culture",
    "domain_cn": "中华优秀传统文化",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学一年级学生的道德与法治课：从「老师，您好！」开始学敬爱老师，从「拉拉手，交朋友」开始学友善待人与诚实守信，再学会上课时好好学、课余时好好玩。全课用真实校园场景与具体的一句话来展开，让学生在「这样说／那样说」的对比里看见对方的感受与后果，懂得礼貌、诚信、感恩与爱护集体。",
    "tags": ["过好校园生活", "礼貌用语", "尊敬师长", "友善交往", "诚实守信", "一年级"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学「中华优秀传统文化」与「道德修养」——懂礼貌、讲诚信，知道感恩，尊重父母师长，爱护集体；对应统编《道德与法治》一年级上册第二单元「过好校园生活」：老师，您好！；拉拉手，交朋友；上课了，好好学；课余生活真丰富。",
    "hero_question": "和老师、和同学在一起的时候，话该怎么说、事该怎么做？",
    "hero_alt": "过好校园生活知识结构图：老师您好、拉拉手交朋友、上课好好学课余真丰富 三栏",
    "hero_caption": "过好校园生活：老师，您好！ · 拉拉手，交朋友 · 上课了，好好学 · 课余生活真丰富",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "见到老师该怎么说？", "d": "什么时候问好、什么时候说谢谢", "v": "见到老师该怎么说"},
        {"t": "怎么和新同学交朋友？", "d": "第一句话说什么、怎么一起玩", "v": "怎么和新同学交朋友"},
        {"t": "上课的时候要做好哪几件事？", "d": "怎样才算好好学", "v": "上课的时候要做好哪几件事"},
        {"t": "课余时间可以做什么？", "d": "课间、活动时间怎么安排", "v": "课余时间可以做什么"},
    ],
    "objectives": [
        "见到老师会主动问好，别人帮了我会说谢谢，有事会走到老师身边说清楚",
        "会用「请问、谢谢、对不起、没关系」这几句话，知道说哪一句要看当时发生的事",
        "能说出上课时要做到的几件事：看老师、先举手、听同学发言、认真写字",
        "能说出课余时间可以做的活动，知道怎样把课余生活安排得又开心又有意思",
    ],
    "objectives_plain": [
        "见到老师会主动问好，别人帮了我会说谢谢，有事会走到老师身边说清楚",
        "会用「请问、谢谢、对不起、没关系」这几句话，知道说哪一句要看当时发生的事",
        "能说出上课时要做到的几件事：看老师、先举手、听同学发言、认真写字",
        "能说出课余时间可以做的活动，知道怎样把课余生活安排得又开心又有意思",
    ],
    "standards": [
        {"content": "懂礼貌、讲诚信，知道感恩，尊重父母师长，爱护集体",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学 中华优秀传统文化 / 道德修养"},
        {"content": "老师，您好！；拉拉手，交朋友；上课了，好好学；课余生活真丰富",
         "source": "统编《道德与法治》一年级上册 第二单元「过好校园生活」"},
    ],
    "prereqs": ["pol-e-g1-u1"],
    "prereqs_name": "我是小学生啦",
    "prereqs_meta": "pol-e-g1-u1",
    "leads_to": ["pol-e-g1-u3"],
    "next_meta": "pol-e-g1-u3",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "上学路上学会了，接下来学更近的一件事：和老师、和同学怎么相处。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能说出该在什么时候说哪一句话。",
        "objectives": "看清四件事：敬爱老师、友善待人说对话、上课好好学、课余真丰富。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "敬爱老师就三句话：见面问声好，帮忙说谢谢，不懂就去问。",
        "lab-1": "六件事，每件三个做法。选完会告诉你，对方心里是什么感觉。",
        "module-2": "你好、谢谢、对不起、没关系——四句话记住了，朋友就多了。",
        "lab-2": "同一件事两种说法，先选一种，读读同学心里怎么想，再换一种看看。",
        "worked-example": "小语的四步：先请问再谢谢、碰倒了说对不起并一起擦、发言先举手、话留到下课说。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "八条做法分进「上课了好好学」和「课余生活真丰富」两个筐。",
        "posttest": "出现了新同学、说错的一句话和班里的活动，看看你能不能用上今天的办法。",
        "summary": "三句话：敬爱老师、友善待人、过好一天。",
        "homework": "三层小任务，先做前两层，第三层可以请同桌一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学道德与法治一年级「过好校园生活」单元，承接上一课「我是小学生啦」，把落点从「认得地方、走对路」推进到「和老师、和同学怎么相处」。一年级学生的难点不在懂道理，而在「在该说的时候说出那句话」——所以全课只做三件能落地的事：敬爱老师（见面问好、帮忙说谢谢、不懂就去问）、友善与诚信（借东西先说请问、做错说对不起并补回来、答应的事要做到）、过好一天（上课好好学、课余好好玩）。三个互动台子都能真的操作：一是六张「校园小主人」情境卡，选做法后展开对方心里的感受与后果，反馈一律写成「这样可能会……，还可以试试……」；二是「这样说，那样说」对比台，同一件事给两种说法，学生选一种就能读到同学心里是什么感觉，再换一种对照；三是「上课了好好学 · 课余生活真丰富」分类台，把八条做法分进两个筐。插图一律为中性简洁的教学示意图（极简线条人物，不使用真实儿童照片）。",
    "plan_table": """| 1 | cover | 过好校园生活 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 老师，您好！敬爱老师，从一声问好开始 | 承·概念一（尊敬师长、知道感恩） |
| 6 | interactive | 动手一：校园小主人，你会怎么做？ | 承·情境判断（展开对方的感受与后果） |
| 7 | concept | 拉拉手，交朋友：友善待人，从一句「请问」开始 | 承·概念二（友善交往 + 诚实守信） |
| 8 | interactive | 动手二：这样说，那样说，看看对方心里怎么想 | 承·对比操作（两种说法 → 对方感受） |
| 9 | concept | 例题示范：小语的课间 | 转·重难点突破（分步示范 + 易错点） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：上课好好学，课余真丰富，把做法分进两个筐 | 合·迁移应用（上课 / 课余 分类） |
| 12 | quiz | 后测：换几个新情境，做法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，讲清怎么过好校园生活 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：老师您好 / 拉拉手交朋友 / 上课好好学·课余真丰富 三栏\n- P5 向老师问好示意图（已生成）：进教室问好、上课起立问好、说谢谢，附中文标注\n- P7 交朋友四句话示意图（已生成）：你好、谢谢、对不起、没关系，附中文标注\n- 三张图均为教学示意图，人物仅用极简线条，不使用任何真实儿童照片或可识别肖像\n- 若需补充：本班礼貌用语海报模板（可由学生手绘）",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
