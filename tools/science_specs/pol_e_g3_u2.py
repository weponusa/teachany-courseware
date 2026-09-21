# -*- coding: utf-8 -*-
"""小学道德与法治 · 学科学 爱科学（G3）—— 补齐知识树「中华优秀传统文化」空缺

学科语气（道德与法治）：情境案例驱动，情感共鸣 + 价值判断；结论落在「应该怎么做、为什么」，
不做道德说教，也不做法条背诵。
三年级落点（全部换成能看见、能做到的具体做法）：
  ① 科技力量大：身边的科技解决了哪些真实问题
  ② 走近科学家：科学家共同的做法（爱问为什么、认真观察、动手试、如实记录、不怕失败）
  ③ 争做未来科学家：三年级能做的科学小事 + 做实验时的安全（呼应课标「基本安全知识」）
三个互动台子都能真操作：问题 ↔ 科技配对、情境卡选做法（反馈「这样可能会……，还可以试试……」）、
「像科学家那样做的 / 要调整的」两筐分类。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g3-u2"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "你有没有想过这样的问题：出门不认识路，为什么手机能告诉我们往哪边转弯？田里的稻子被虫子咬了，为什么有的品种还是长得好好的？生病了，医生为什么能查清楚是哪里不舒服？这些问题的背后，都站着同一件事——科学和技术。这节课我们做三件事：看一看科技给我们的生活带来了哪些变化；走近科学家，看看他们做事有什么共同的地方；再想一想，我们自己现在能做一点什么。",
    "problem-anchor": "开始之前，先选一个你最想弄清楚的问题。是想知道科技帮我们解决了什么问题，还是想知道科学家到底是什么样的人；是想知道自己现在能不能做科学，还是想知道做实验的时候要注意哪些安全。选好以后，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能举出两三个身边的例子，说出科技帮我们解决了什么真实问题。第二，能说出科学家共同的做法：爱问为什么、认真观察、动手去试、如实记录、不怕失败。第三，能说出自己现在可以做的一两件科学小事，比如提一个问题、认真记一次观察。第四，知道做观察和小实验时的安全要求，听老师的指导，不随意尝、不随意混、不用湿手碰电器。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先来看看身边的科技。出门不认识路，手机里的导航会告诉我们往哪边转弯；田里的稻子被虫子咬了，科学家培育出更抗虫的品种，让收成保住了；生病了要查清楚原因，医生借助各种检查设备，能看得更清楚；冬天屋子里冷，新的保温材料让房间更暖和；想念远方的亲人，打开手机就能看见对方的脸。这些看起来不一样的事，背后做着同一件事：人们遇到了难题，然后一步一步想办法，把它变成了有办法。这就是科技的力量。",
    "lab-1": "现在请你当一次连线的工程师。上面是六个生活里真实遇到的难题，下面是六种解决问题的办法。先点一个难题，再点你觉得能解决它的那种办法。连对了会告诉你为什么，连错了也会提醒你再想一想。",
    "module-2": "科学家是什么样的人呢？他们做的事不一样，做法却很像。第一，他们爱问为什么，看到平常的事情也会多想一句。第二，他们认真观察，看一看、量一量，把看到的东西记下来。第三，他们动手去试，用实验来检验自己的想法。第四，他们如实记录，哪怕记录的结果和自己猜的不一样，也照实写下来——这一点特别重要。第五，他们不怕失败，一次不行就改一改再试一次。研究杂交水稻的科学家，就是在很多次失败里一次一次试出来的。其实这些做法，我们三年级也能做。还有一件最要紧的事：做观察和小实验的时候要注意安全。听清老师的要求，按步骤做；实验用的东西不管看起来多像吃的，都不能尝；不要自己把几种东西混在一起；不要用湿手碰插座和电器。",
    "lab-2": "现在请你当一次科学小侦探。这里有六件做观察或小实验时会遇到的事，每一件事都有三个做法。你选一个你觉得合适的，选完立刻会有一段话告诉你为什么；要是选得不太合适，也会告诉你还可以试试什么。",
    "worked-example": "我们一起来看小雨的绿豆发芽观察。第一步，提出问题：绿豆发芽需要水吗？没有水它会不会发芽？第二步，猜一猜：小雨猜没有水就不会发芽。第三步，做计划：她拿两个小杯子，各放三粒绿豆，一个每天浇一点水，另一个不浇水，都放在窗台上。第四步，每天记录：她在本子上写清日期，画下绿豆的样子，量一量高度。第五步，如实记下来：到了第三天，她发现自己猜的和记录的不完全一样——不浇水的那个杯子里，有一粒绿豆居然也裂开了皮。她没有改数据，而是照实写下来。第六步，再试一次：她想了想，可能是杯子里剩下的那点水汽帮了忙，于是又做了一次，这次把杯子擦干再试。",
    "conceptest-1": "接下来用三个说法考考你，每个说法里都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件事交给你。下面有八条做法，请你判断一下：哪些做法像科学家那样做，放进像科学家那样做这一边；哪些做法需要调整，放进要调整的这一边。放好以后，再读一读为什么。",
    "posttest": "最后一轮，换几个新的小情境来考考你。这次会遇到观察记录、别人转发的说法、还有实验安全，看看你能不能用上今天的办法。",
    "summary": "这节课我们记住四句话。第一句，科技就在我们身边，它做的事就是帮人们把难题变成有办法。第二句，科学家共同的做法是：爱问为什么、认真观察、动手去试、如实记录、不怕失败。第三句，我们现在就能做科学小事，比如提一个问题、认真记一次观察、把结果照实写下来。第四句，做观察和小实验要记住安全：听老师的指导，不尝、不混、不用湿手碰电器。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出两件身边的科技，分别说说它们解决了什么问题；再说出做实验时要记住的两条安全要求。第二层能力应用，动手做：选一颗种子或一盆植物，连续观察五天，每天记下日期和你看到的变化。第三层迁移挑战，选做：提一个自己真正好奇的问题，说一说你打算怎么去找到答案，再把自己的观察结果讲给同学听。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 科技力量大", "lab-1": "动手一 难题和办法连连看",
    "module-2": "概念二 走近科学家 · 争做未来科学家", "lab-2": "动手二 科学小侦探",
    "worked-example": "例题讲解 小雨的绿豆发芽观察", "conceptest-1": "概念测试",
    "synthesis": "综合任务 像科学家那样做的 / 要调整的", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：难题 ↔ 办法（配对） ──
PROBLEMS = [
    {"id": "q1", "t": "出门去一个不熟悉的地方，不知道该往哪边走", "aid": "nav",
     "why": "导航借助卫星定位，能告诉我们大概往哪边走、还有多远。它解决的是「不认路」这个难题。"},
    {"id": "q2", "t": "田里的稻子被虫子咬了，收成要保不住", "aid": "seed",
     "why": "农业科学家培育出更抗虫的品种，还研究出更省力的防治办法，帮人们把收成保住。"},
    {"id": "q3", "t": "身体不舒服，想知道到底是哪里出了问题", "aid": "exam",
     "why": "各种检查设备能帮医生看得更清楚，查明白原因才好对症下药。"},
    {"id": "q4", "t": "很想念在外地工作的亲人，想看看他的样子", "aid": "video",
     "why": "网络视频通话让人隔着很远也能看见对方的脸、听见对方的声音。"},
    {"id": "q5", "t": "冬天家里的屋子很冷，想让它暖和一点", "aid": "warm",
     "why": "保温材料和取暖设备能把热量留在屋里，让屋子更暖和、也更省电。"},
    {"id": "q6", "t": "明天要出门活动，想知道会不会下雨", "aid": "weather",
     "why": "气象观测和预报把各地收集到的数据算一算，帮我们提前安排明天的活动。"},
]
AIDS = [
    {"id": "nav", "n": "卫星导航"},
    {"id": "seed", "n": "良种与农业科技"},
    {"id": "exam", "n": "医学检查设备"},
    {"id": "video", "n": "网络视频通话"},
    {"id": "warm", "n": "保温材料与取暖设备"},
    {"id": "weather", "n": "气象观测与预报"},
]

# ── 动手二：做观察或小实验时，六个情境 × 三个做法 ──
SCENES = [
    {
        "id": "s1",
        "t": "做实验时，看到了一个我没见过的现象",
        "opts": [
            {"k": "a", "t": "先仔细看一看，再问一句「为什么会这样」", "ok": True,
             "fb": "这就是科学家的第一反应。多问一句为什么，后面的观察才有方向。"},
            {"k": "b", "t": "先不管它，照着书上写的做下去", "ok": False,
             "fb": "这样可能会错过一个有意思的发现。还可以试试：先把这个现象记下来，做完实验再去问。"},
            {"k": "c", "t": "马上大声说出来，打断老师和其他同学", "ok": False,
             "fb": "这样可能会让实验停下来，别人也听不清要求。还可以试试：先记在本子上，等老师讲完再说。"},
        ],
    },
    {
        "id": "s2",
        "t": "同伴说：「这个实验用的液体闻着像糖水，尝一口试试？」",
        "opts": [
            {"k": "a", "t": "告诉他不能尝，实验用的东西一律不入口", "ok": True,
             "fb": "这个提醒很关键。实验用的东西不管看起来多像吃的，都不能尝，安全永远排在第一位。"},
            {"k": "b", "t": "自己先尝一点点，看看是什么味道", "ok": False,
             "fb": "这样很危险。有些东西看起来像糖水，其实不能入口。还可以试试：马上告诉老师，请老师来处理。"},
            {"k": "c", "t": "让他一个人尝，自己在旁边看着", "ok": False,
             "fb": "这样也很危险。看见同学这样做，要及时提醒他，并且告诉老师。还可以试试：一起把这件事报告给老师。"},
        ],
    },
    {
        "id": "s3",
        "t": "记录下来的数据和我的猜想不一样",
        "opts": [
            {"k": "a", "t": "照实记下来，再想一想是哪里和自己想的不同", "ok": True,
             "fb": "这一点特别重要。科学家的记录里，常常正是这些「不一样」带来了新的发现。"},
            {"k": "b", "t": "把数据改成和自己猜想一样的", "ok": False,
             "fb": "这样就不是真的观察了，别人照你的记录也做不出来。还可以试试：照实写下来，再写一句你的想法。"},
            {"k": "c", "t": "不记这一条，反正和想的不一样", "ok": False,
             "fb": "这样可能会丢掉最有价值的那一条。还可以试试：把不一样的地方圈出来，做个小记号。"},
        ],
    },
    {
        "id": "s4",
        "t": "同学说：「网上都这么讲，那肯定是真的。」",
        "opts": [
            {"k": "a", "t": "先问一问：他是从哪里看到的？有没有别的说法？", "ok": True,
             "fb": "这个问题问得好。先弄清楚话是从哪来的，再看看有没有别的说法，才不容易被带偏。"},
            {"k": "b", "t": "马上相信，并且转给更多同学", "ok": False,
             "fb": "这样可能会把没弄清楚的说法传得更远。还可以试试：先查一查、问一问，确认了再决定要不要说。"},
            {"k": "c", "t": "不管真假，反正和自己没关系", "ok": False,
             "fb": "这样可能会让不准确的说法一直传下去。还可以试试：花一分钟查一查，或者问问老师。"},
        ],
    },
    {
        "id": "s5",
        "t": "绿豆发芽要观察七天，第三天我忘记记了",
        "opts": [
            {"k": "a", "t": "照实写「今天忘记记录了」，接着把后面几天记好", "ok": True,
             "fb": "照实写下来，就是诚实。少了一天不丢人，把后面的记好更重要。"},
            {"k": "b", "t": "凭印象补上一条，反正看起来差不多", "ok": False,
             "fb": "这样记下来的就不是真的观察了。还可以试试：写上「今天忘记记」，从明天继续。"},
            {"k": "c", "t": "干脆不记了，反正已经断了一天", "ok": False,
             "fb": "这样可能会让前面的记录也白做了。还可以试试：接着往下记，五天里记满四天也很有价值。"},
        ],
    },
    {
        "id": "s6",
        "t": "做了好几次，实验都没有成功",
        "opts": [
            {"k": "a", "t": "看看哪一步可能有问题，改一改再试一次", "ok": True,
             "fb": "这正是科学家常做的事。一次不行就找找原因，改一改再来。"},
            {"k": "b", "t": "把结果写成成功，反正差不多", "ok": False,
             "fb": "这样就不是真的结果了。还可以试试：如实写下「这次没有成功」，再写写你发现的问题。"},
            {"k": "c", "t": "算了，不做了，这个实验太难", "ok": False,
             "fb": "这样可能会有点可惜，你已经做的观察其实很有用。还可以试试：把难的地方说给老师听，一起想一想。"},
        ],
    },
]

# ── 综合任务：像科学家那样做的 / 要调整的（分进两个筐） ──
SORT_ITEMS = [
    {"id": "k1", "t": "看到不明白的现象，先问一句「为什么会这样」", "bin": "sci",
     "why": "爱问为什么，是科学家的第一个做法。"},
    {"id": "k2", "t": "每天认真看一看、量一量，写清日期记下来", "bin": "sci",
     "why": "认真观察、如实记录，后面才有话可说、有据可查。"},
    {"id": "k3", "t": "记录的结果和自己的猜想不一样，也照实写下来", "bin": "sci",
     "why": "照实记录，是科学里最重要的诚实——不一样的地方往往最有价值。"},
    {"id": "k4", "t": "做实验前先听清老师说的安全要求，按步骤来", "bin": "sci",
     "why": "安全永远排在第一位，听清要求再动手。"},
    {"id": "k5", "t": "猜不出来就直接查答案抄下来，不用自己想", "bin": "tune",
     "why": "这样可能会让你少了一次自己想的机会。还可以试试：先猜一猜，再去查一查对不对。"},
    {"id": "k6", "t": "看到一个新奇的说法，马上转给同学", "bin": "tune",
     "why": "这样可能会把没弄清楚的说法传得更远。还可以试试：先查一查、问一问，确认了再说。"},
    {"id": "k7", "t": "试了两次没成功，就放在一边不管了", "bin": "tune",
     "why": "这样可能会丢掉快要成功的发现。还可以试试：想想是哪一步不对，改一改再试一次。"},
    {"id": "k8", "t": "实验里的东西看起来像糖，尝一尝是什么味道", "bin": "tune",
     "why": "这样很危险。实验用的东西不管看起来多像吃的，都不能尝。还可以试试：马上告诉老师。"},
]
SORT_BIN = {"sci": "像科学家那样做的", "tune": "要调整的"}

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g3-u2 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 难题 ↔ 办法 连连看（六组配对）
   3) 科学小侦探：六个情境 × 三个做法 → 温和反馈（不判错、不贴标签）
   4) 像科学家那样做的 / 要调整的：八条做法分进两个筐
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

  /* ---------- 2. 难题 ↔ 办法 连连看 ---------- */
  var PROBLEMS = __PROBLEMS_JSON__;
  var AIDS = __AIDS_JSON__;
  var stage1 = document.getElementById('link-stage');
  if (stage1) {
    var picked = null, solved = {};
    var out1 = document.getElementById('link-out');

    function aidName(id) {
      for (var i = 0; i < AIDS.length; i++) { if (AIDS[i].id === id) return AIDS[i].n; }
      return '';
    }
    function render1() {
      document.querySelectorAll('[data-problem]').forEach(function (b) {
        var k = b.dataset.problem;
        b.classList.toggle('selected', k === picked);
        b.classList.toggle('done', !!solved[k]);
        b.disabled = !!solved[k];
      });
      document.querySelectorAll('[data-aid]').forEach(function (b) {
        b.classList.toggle('done', !!solved[b.dataset.aid]);
      });
      document.getElementById('link-score').textContent =
        '已经连对 ' + Object.keys(solved).length + ' / ' + PROBLEMS.length + ' 组';
      var bank = document.getElementById('link-done');
      bank.innerHTML = '';
      PROBLEMS.forEach(function (p) {
        if (!solved[p.id]) return;
        var s = document.createElement('span');
        s.className = 'tag';
        s.textContent = p.t.slice(0, 8) + '… → ' + aidName(p.aid);
        bank.appendChild(s);
      });
      if (!bank.innerHTML) {
        bank.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有连对一组。</span>';
      }
    }
    document.querySelectorAll('[data-problem]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (solved[b.dataset.problem]) return;
        picked = b.dataset.problem;
        out1.className = 'result warn';
        out1.innerHTML = '<strong>你遇到的难题是：' + b.textContent + '</strong><br>想一想，下面哪种办法能解决它？点一点试试。';
        render1();
      });
    });
    document.querySelectorAll('[data-aid]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!picked) {
          out1.className = 'result warn';
          out1.textContent = '先在上面点一个难题，再来选办法。';
          return;
        }
        var P = null;
        for (var i = 0; i < PROBLEMS.length; i++) { if (PROBLEMS[i].id === picked) P = PROBLEMS[i]; }
        if (b.dataset.aid === P.aid) {
          solved[P.id] = true;
          out1.className = 'result';
          out1.innerHTML = '<strong>连对了，是「' + aidName(P.aid) + '」。</strong>' + P.why;
          picked = null;
          if (Object.keys(solved).length === PROBLEMS.length) {
            out1.className = 'result';
            out1.innerHTML = '<strong>六组全连对了！</strong>你会发现，这些看起来不一样的事，背后做的是同一件事：' +
              '<strong>人们遇到了难题，就一步一步想办法。</strong>';
          }
        } else {
          out1.className = 'result warn';
          out1.innerHTML = '<strong>这两个可能对不上。</strong>你点的是「' + b.textContent + '」。' +
            '<br><span style="color:var(--muted)">常见错误：容易把「看着有点关系」当成「能解决这个难题」——' +
            '先想清楚这个难题最缺的是什么，再选办法。</span>';
        }
        render1();
      });
    });
    render1();
  }

  /* ---------- 3. 科学小侦探 ---------- */
  var SCENES = __SCENES_JSON__;
  var stage2 = document.getElementById('case-stage');
  if (stage2) {
    var curScene = null, doneScene = {};
    var out2 = document.getElementById('case-out');

    function sceneById(id) {
      for (var i = 0; i < SCENES.length; i++) { if (SCENES[i].id === id) return SCENES[i]; }
      return null;
    }
    function render2() {
      document.querySelectorAll('[data-case]').forEach(function (b) {
        var k = b.dataset.case;
        b.classList.toggle('selected', k === curScene);
        b.classList.toggle('correct', !!doneScene[k]);
      });
      document.getElementById('case-score').textContent =
        '已经聊过 ' + Object.keys(doneScene).length + ' / ' + SCENES.length + ' 件事';
    }
    function paintOptions() {
      var box = document.getElementById('case-opts');
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
            out2.className = 'result';
            out2.innerHTML = '<strong>这个做法挺好。</strong>' + o.fb;
          } else {
            out2.className = 'result warn';
            out2.innerHTML = '<strong>还可以再想一想。</strong>' + o.fb;
          }
          render2();
          paintOptions();
        });
        box.appendChild(b);
      });
    }
    document.querySelectorAll('[data-case]').forEach(function (b) {
      b.addEventListener('click', function () {
        curScene = b.dataset.case;
        var S = sceneById(curScene);
        if (doneScene[curScene]) {
          out2.className = 'result';
          out2.innerHTML = '<strong>这件事已经聊过啦。</strong>你上次选的做法挺合适，记住它就好。';
        } else {
          out2.className = 'result warn';
          out2.innerHTML = '<strong>你遇到的是：' + S.t + '</strong><br>下面有三个做法，你选一个试试看。';
        }
        render2();
        paintOptions();
      });
    });
    render2();
  }

  /* ---------- 4. 像科学家那样做的 / 要调整的 ---------- */
  var ITEMS = __SORT_JSON__;
  var BINN = __SORTBIN_JSON__;
  var stage3 = document.getElementById('sci-stage');
  if (stage3) {
    var pickItem = null, placed = {};
    var out3 = document.getElementById('sci-out');

    function render3() {
      document.querySelectorAll('[data-item]').forEach(function (b) {
        var k = b.dataset.item;
        b.classList.toggle('selected', k === pickItem);
        b.classList.toggle('done', !!placed[k]);
        b.disabled = !!placed[k];
      });
      document.getElementById('sci-score').textContent =
        '已经放好 ' + Object.keys(placed).length + ' / ' + ITEMS.length + ' 条';
      var a = document.getElementById('sci-bin-a');
      var b2 = document.getElementById('sci-bin-b');
      a.innerHTML = ''; b2.innerHTML = '';
      ITEMS.forEach(function (it) {
        if (!placed[it.id]) return;
        var s = document.createElement('div');
        s.className = 'tag';
        s.textContent = it.t;
        (it.bin === 'sci' ? a : b2).appendChild(s);
      });
      if (!a.innerHTML) a.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
      if (!b2.innerHTML) b2.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
    }
    document.querySelectorAll('[data-item]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (placed[b.dataset.item]) return;
        pickItem = b.dataset.item;
        out3.className = 'result warn';
        out3.innerHTML = '<strong>你选的是：' + b.textContent + '</strong><br>想一想，它是「像科学家那样做的」，还是「要调整的」？';
        render3();
      });
    });
    document.querySelectorAll('[data-sci-bin]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pickItem) {
          out3.className = 'result warn';
          out3.textContent = '先在上面点一条做法，再选筐。';
          return;
        }
        var it = null;
        for (var i = 0; i < ITEMS.length; i++) { if (ITEMS[i].id === pickItem) it = ITEMS[i]; }
        if (b.dataset.sciBin === it.bin) {
          placed[it.id] = true;
          out3.className = 'result';
          out3.innerHTML = '<strong>放对了，它属于「' + BINN[it.bin] + '」。</strong>' + it.why;
          pickItem = null;
          if (Object.keys(placed).length === ITEMS.length) {
            out3.className = 'result';
            out3.innerHTML = '<strong>八条全放对了！</strong>记住这句口诀：<strong>多问一句为什么，认真看、动手试，' +
              '照实记下来，安全记心上。</strong>';
          }
        } else {
          out3.className = 'result warn';
          out3.innerHTML = '<strong>再想一想这条做法。</strong>' + it.why +
            '<br><span style="color:var(--muted)">常见错误：容易把「看起来很热闹」误认为「像科学家那样做」——' +
            '科学最看重的是认真观察和如实记录，不是谁的声音大。</span>';
        }
        render3();
      });
    });
    render3();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__PROBLEMS_JSON__', json.dumps(PROBLEMS, ensure_ascii=False))
             .replace('__AIDS_JSON__', json.dumps(AIDS, ensure_ascii=False))
             .replace('__SCENES_JSON__', json.dumps(SCENES, ensure_ascii=False))
             .replace('__SORT_JSON__', json.dumps(SORT_ITEMS, ensure_ascii=False))
             .replace('__SORTBIN_JSON__', json.dumps(SORT_BIN, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "出门去一个不熟悉的地方，下面哪种办法能帮我们找到路？",
         "options": [("用手机里的卫星导航看往哪边走", True),
                     ("走到哪里算哪里，反正总会到", False),
                     ("一直站在路口等人来带路", False)],
         "explain": "导航借助卫星定位，能告诉我们大概往哪边走、还有多远。"
                    "<strong>错因提醒：</strong>常见错误是误认为「科技离我们很远」——"
                    "其实它就在每天的生活里，帮我们解决很具体的小麻烦。"},
        {"q": "科学家做事时，下面哪个做法是他们共同的做法？",
         "options": [("认真做好观察和记录，结果和自己想的不一样也照实写下来", True),
                     ("记住书上的结论就可以了，不用自己动手", False),
                     ("一次做不成功就换一件别的事做", False)],
         "explain": "认真观察、如实记录、不怕失败，是科学家共同的做法。"
                    "<strong>错因提醒：</strong>有的同学误认为「科学家靠的是特别聪明」——"
                    "比起聪明，他们更靠一次次认真的观察和尝试。"},
        {"q": "做实验的时候，同伴说「这个东西闻着像糖水，想尝一口」，你会：",
         "options": [("告诉他不能尝，实验用的东西一律不入口，并马上告诉老师", True),
                     ("让他尝一点点，应该没关系", False),
                     ("自己也尝一点，先试试看", False)],
         "explain": "实验用的东西不管看起来多像吃的，都不能尝，这是最基本的安全要求。"
                    "<strong>错因提醒：</strong>容易把「看起来像吃的」误认为「真的可以吃」——"
                    "做实验时，安全永远排在第一位。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "科技力量大：身边的科技，帮我们解决真实的问题", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们都用过手机、坐过高铁、见过田里的农机，觉得这些很平常（And）；可是这些平常的事，背后是很多人遇到难题、一次次想办法才做成的（But）；所以要真正走近科学，先得看见这件事：科技就是把难题一步一步变成办法（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">科技不只在实验室里，它就在我们每天的生活里。它们做的是同一件事：<strong>把难题变成有办法</strong>。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>回家路上</strong></p>
            <p style="color:var(--muted)">不认路，有卫星导航；下雨前，有天气预报提醒我们带好雨具；出门远一点，有又快又稳的列车。</p>
          </div>
          <div class="inner-card">
            <p><strong>家里和医院</strong></p>
            <p style="color:var(--muted)">屋冷有保温材料和取暖设备；身体不舒服，检查设备能帮医生看得更清楚；想远方亲人，打开手机就能看见。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="身边的科技解决真实问题示意图：不认路、稻子被虫咬、身体不舒服分别对应什么办法，附中文标注">
          <figcaption>概念图：生活里遇到的难题，人们一步一步想办法解决——科技就是把「难题」变成「有办法」（教学示意图，中性简洁扁平插画）</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">💡</span><div><strong>记一句话：</strong>科技做的事不神秘——<strong>遇到了难题，就一步一步想办法。</strong></div></div>
{insight_box([
    {"lens": "看见它", "text": "导航、良种、检查设备、保温材料、视频通话……它们看着互不相干，其实做的都是同一件事：替人解决一个具体的难题。"},
    {"lens": "解释它", "text": "为什么说科技是「一步一步」想办法？因为没有人一开始就知道答案。先弄清难题在哪里，再试着做，不行就改一改再试。"},
    {"lens": "迁移它", "text": "这个思路在家里也用得上：衣服总找不到，就想个固定的地方放；书包总是忘带东西，就写一张清单——这也是在解决自己的难题。"},
])}
    ''', tag="概念一"))

    prob_btns = "\n".join(
        f'            <button class="choice" data-problem="{p["id"]}" style="text-align:left">{p["t"]}</button>'
        for p in PROBLEMS
    )
    aid_btns = "\n".join(
        f'            <button class="choice" data-aid="{a["id"]}" style="text-align:center">{a["n"]}</button>'
        for a in AIDS
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：难题和办法，连连看", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">上面是六个生活里真实遇到的难题，下面是六种解决问题的办法。先点一个难题，再点你觉得能解决它的那种办法。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 遇到了一个难题</div>
          <div class="grid" id="link-stage">
{prob_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 哪种办法能解决它</div>
          <div class="grid grid-3">
{aid_btns}
          </div>
          <div class="inner-card" style="margin-top:14px">
            <p><strong>连好的难题与办法</strong></p>
            <div id="link-done" style="display:flex;flex-wrap:wrap;gap:6px"><span style="color:var(--muted);font-size:14px">还没有连对一组。</span></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">连线进度</span><span class="v" id="link-score">已经连对 0 / 6 组</span></div>
          </div>
          <p class="result warn" id="link-out" style="margin-top:12px">先在上面点一个难题。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔧</span><div><strong>想一想：</strong>这六种办法有没有共同的地方？它们都是有人先弄清了难题在哪里，再一点点想办法做出来的。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "走近科学家 · 争做未来科学家", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">科学家做的事各不相同，<strong>做法却很相像</strong>。这些做法，我们三年级也能学。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>爱问为什么：</strong>看到平常的事，也多想一句「它为什么会这样」。</div></div>
          <div class="step"><span class="n">2</span><div><strong>认真观察：</strong>看一看、量一量，把看到的东西记下来。</div></div>
          <div class="step"><span class="n">3</span><div><strong>动手去试：</strong>用一个小小的实验，检验自己的想法对不对。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>如实记录：</strong>结果和自己想的不一样，也照实写下来——这一点最要紧。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="科学家的共同做法五步示意图与做实验的安全提醒，附中文标注">
          <figcaption>概念图：像科学家那样做——提问 · 猜想 · 动手试 · 如实记录 · 再试一次；做实验安全记心上（教学示意图）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「科学家一定特别聪明，一猜就中」。其实他们更靠的是一次次认真的观察和尝试：猜错了就照实记下来，改一改再试一次。研究杂交水稻的科学家，就是在上千次失败里一点点试出来的。</p>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>最要紧的一件事：安全记心上</strong></p>
          <p style="color:var(--muted)">做观察和小实验要听老师的指导，按步骤来；实验用的东西不管看起来多像吃的，都不能尝；不自己把几种东西混在一起；不用湿手碰插座和电器。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "「如实记录」听起来很平常，却是科学里最要紧的一条：结果和自己想的不一样，也照实写下来，别人才敢照着你的记录再做一次。"},
    {"lens": "比较它", "text": "同样是没成功：一种是照实写下「这次没有成功」再找原因，一种是悄悄改成成功——两种做法，长出来的本领完全不同。"},
    {"lens": "迁移它", "text": "这套做法不止在实验里：学一样新本领、想弄清一件好奇的事，都是先问、再看、再试、再如实记下来。"},
])}
    ''', tag="概念二"))

    case_btns = "\n".join(
        f'            <button class="choice" data-case="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in SCENES
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：科学小侦探，你会怎么做？", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一件做观察或小实验时可能遇到的事，再从三个做法里选一个。<strong>选得好会告诉你为什么，选得不太合适也会告诉你还可以试试什么。</strong></p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 我遇到的一件事</div>
          <div class="grid" id="case-stage">
{case_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 我可以怎么做</div>
          <div class="grid" id="case-opts">
            <span style="color:var(--muted);font-size:14px">先在上面点一件事，这里就会出现三个做法。</span>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">聊过几件事</span><span class="v" id="case-score">已经聊过 0 / 6 件事</span></div>
          </div>
          <p class="result warn" id="case-out" style="margin-top:12px">先点一件可能遇到的事。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💛</span><div><strong>说给你听：</strong>这里的做法没有分数。有些做法只是会让你错过一次发现，换一个试试就好。拿不准的时候，问老师，是很好的办法。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小雨的绿豆发芽观察", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>小雨想弄清一件事：绿豆发芽需要水吗？没有水它会不会发芽？请你帮她把这个观察一步一步做下来。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>提出问题：</strong>绿豆发芽需要水吗？没有水它会不会发芽？</div></div>
          <div class="step"><span class="n">2</span><div><strong>猜一猜：</strong>小雨猜没有水就不会发芽，并想一想怎么才能看得出来。</div></div>
          <div class="step"><span class="n">3</span><div><strong>做计划、动手试：</strong>两个小杯子各放三粒绿豆，一个每天浇一点水，另一个不浇水，都放在窗台上。</div></div>
          <div class="step"><span class="n">4</span><div><strong>每天如实记录：</strong>写清日期，画下样子，量一量高度。第三天她发现，不浇水的杯子里竟有一粒绿豆也裂开了皮——她没有改数据，照实写下来。</div></div>
          <div class="step"><span class="n green">5</span><div><strong>再试一次：</strong>她想可能是杯子里剩下的水汽帮了忙，于是把杯子擦干，又做了一次。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「记录要和自己猜的一样才算做对了」。其实记录只要和看到的一样就是对的；正是那些「不一样」的地方，往往藏着一个新的发现。</p>
        </div>
        <div class="inner-card">
          <p><strong>说给同桌听：</strong>小雨这五步里，哪一步最不容易做到？如果是你，那一条「不一样」的记录，你会怎么写？</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "下面哪句话说得对？",
         "options": [("科技离我们不远，它做的是把生活里的难题一步一步变成办法", True),
                     ("科技是科学家的事，和我们小学生没什么关系", False),
                     ("科技就是让东西看起来更先进", False)],
         "explain": "导航、良种、检查设备、保温材料，解决的都是一件件很具体的难题。"
                    "<strong>错因提醒：</strong>常见错误是误认为「科技只是大人和机器的世界」——"
                    "其实它每天都在帮我们解决小麻烦。"},
        {"q": "做观察记录时，你看到的结果和自己的猜想不一样，下面哪个做法更好？",
         "options": [("照实写下来，再想一想是哪里和自己想的不同", True),
                     ("改成和自己猜想一样的，这样比较整齐", False),
                     ("这一条干脆不记，反正和想的不一样", False)],
         "explain": "照实记录才是真的观察，别人照着你的记录也能再做一次。"
                    "<strong>错因提醒：</strong>有人误认为「记录要好看、要符合猜想」——"
                    "其实记录只要和看到的一样，就是对的。"},
        {"q": "同伴做实验时说：「这个东西闻着像糖水，我尝一口行吗？」下面哪个做法最合适？",
         "options": [("告诉他不能尝，并马上把这件事告诉老师", True),
                     ("让他只尝一小口，应该没事", False),
                     ("先不管，等他尝完再说", False)],
         "explain": "实验用的东西不管看起来多像吃的，都不能尝，这是最基本的安全要求。"
                    "<strong>错因提醒：</strong>容易把「看起来像吃的」和「真的能吃」搞混——"
                    "做实验时，安全永远排在第一位。"}
    ], tag="概念测试"))

    item_btns = "\n".join(
        f'            <button class="sort-item" data-item="{it["id"]}">{it["t"]}</button>' for it in SORT_ITEMS
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：像科学家那样做的 / 要调整的，把做法分进两个筐", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一条做法，再点它应该进的筐：<strong>像科学家那样做的</strong>放一边，<strong>要调整的</strong>放另一边。</p>
        <div class="lab-panel">
          <div class="sort-bank" id="sci-stage">
{item_btns}
          </div>
          <div class="grid grid-2" style="margin-top:14px">
            <button class="choice" data-sci-bin="sci" style="text-align:center">像科学家那样做的</button>
            <button class="choice" data-sci-bin="tune" style="text-align:center">要调整的</button>
          </div>
          <div class="sort-bins">
            <div class="sort-bin" id="sci-bin-a"><h4>像科学家那样做的</h4></div>
            <div class="sort-bin" id="sci-bin-b"><h4>要调整的</h4></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">分类进度</span><span class="v" id="sci-score">已经放好 0 / 8 条</span></div>
          </div>
          <p class="result warn" id="sci-out" style="margin-top:12px">先在上面点一条做法。</p>
        </div>
        <div class="inner-card">
          <p><strong>分完之后，想一想：</strong></p>
          <p style="color:var(--muted)">「像科学家那样做的」这一边里，你最想先练哪一条？写在下面，再说一说为什么选它。</p>
          <textarea id="syn-answer" rows="3" placeholder="我最想先练……，因为……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，办法还在不在", TTS["posttest"], [
        {"q": "观察记录做了五天，第三天忘记记了，下面哪个做法更好？",
         "options": [("照实写上「今天忘记记录」，接着把后面几天记好", True),
                     ("凭印象补一条，看起来差不多就行", False),
                     ("干脆不记了，反正已经断了一天", False)],
         "explain": "照实写下来就是诚实，少了一天不丢人，把后面的记好更重要。"
                    "<strong>错因提醒：</strong>常见错误是误认为「补一条差不多就行」——"
                    "凭印象补的不是真观察，别人照着也做不出来。"},
        {"q": "同学说：「网上都这么讲，那肯定是真的。」下面哪个做法更好？",
         "options": [("先问一问他是从哪里看到的，再看看有没有别的说法", True),
                     ("马上相信，并且转给更多同学", False),
                     ("不管真假，反正和自己没关系", False)],
         "explain": "先弄清楚说法从哪里来，再看有没有别的说法，才不容易被带偏。"
                    "<strong>错因提醒：</strong>容易把「很多人都说」当成「一定是真的」——"
                    "人多，不等于有依据。"},
        {"q": "做小实验时，老师提醒要用到小刀，下面哪个做法最合适？",
         "options": [("听清老师的要求，按步骤做，用的时候刀刃朝外、手指避开", True),
                     ("为了快一点，自己拿起来就切", False),
                     ("先玩一玩小刀，等老师讲完再开始", False)],
         "explain": "听清要求、按步骤做、刀刃朝外，都是最基本的安全做法。"
                    "<strong>错因提醒：</strong>有人误认为「我会用就不用听」——"
                    "实验里的安全做法，是为了保护你和身边的同学。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：四句话，讲清怎么学科学、爱科学", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>科技力量大：</strong>科技就在身边，它做的是把生活里的难题一步一步变成有办法。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>科学家的做法：</strong>爱问为什么、认真观察、动手去试、如实记录、不怕失败。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>我们现在能做的：</strong>提一个问题、认真记一次观察、把结果照实写下来，再试一次。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>安全记心上：</strong>听老师的指导、按步骤来；不尝、不混、不用湿手碰电器。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>一句口诀：</strong>多问一句为什么，认真看、动手试，照实记下来，安全记心上。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「提问、记录、再试一次」这三个说法，说清楚你打算做的一次小观察。</p>
          <p style="color:var(--muted)">再动一动手：<strong>写一写</strong>你最想问的一个「为什么」，再说说你打算怎么去找答案。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "说出两件身边的科技，分别说说它们解决了什么问题。",
            "写出做观察和小实验时要记住的两条安全要求。",
        ],
        [
            "选一颗种子或一盆植物，连续观察五天，每天记下日期和你看到的变化；有一天忘记记，就照实写上「今天忘记记录了」。",
            "提一个自己好奇的问题，猜一猜答案，再想一个能看出对错的简单办法，把它说给同桌听。",
        ],
        [
            "学完一课以后，写三句话：我提出了什么问题？我是怎么去找答案的？结果和我猜的一样吗？",
            "问一问家里的大人：他小时候有没有一件「特别想知道为什么」的事？后来弄明白了吗？把他的话记下来，和今天学的做法比一比。",
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
    "title": "学科学 爱科学",
    "name_en": "Love Science, Learn Science",
    "grade": 3,
    "grade_cn": "三年级",
    "domain": "tradition-culture",
    "domain_cn": "中华优秀传统文化",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学三年级的道德与法治课：先看见身边的科技——导航、良种、检查设备、保温材料、视频通话，它们做的事都是把生活里的难题一步一步变成办法；再走近科学家，看看他们共同的做法：爱问为什么、认真观察、动手去试、如实记录、不怕失败；最后落到三年级能做的科学小事上，并且牢牢记住做观察和小实验的安全要求（听老师指导、不尝、不混、不用湿手碰电器）。全课以真实情境和可操作的选择为主，帮助学生在动手与判断中体会科学精神、增强规则与安全意识。",
    "tags": ["学科学爱科学", "科技力量大", "走近科学家", "争做未来科学家", "如实记录", "实验安全", "三年级", "中华优秀传统文化"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学「中华优秀传统文化」——掌握基本安全知识和技能，学会应对常见安全问题；对应统编《道德与法治》三年级上册「学科学 爱科学」：科技力量大、走近科学家、争做未来科学家。",
    "hero_question": "身边的科技帮我们解决了哪些难题？科学家做事，又和我们有什么不一样？",
    "hero_alt": "学科学 爱科学知识结构图：科技力量大、走近科学家、争做未来科学家 三栏",
    "hero_caption": "学科学 爱科学：科技力量大 · 走近科学家 · 争做未来科学家（多问一句为什么 · 如实记录 · 安全记心上）",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "科技帮我们解决了什么问题？", "d": "身边的科技和我有什么关系", "v": "科技帮我们解决了什么问题"},
        {"t": "科学家到底是什么样的人？", "d": "他们做事有什么共同的地方", "v": "科学家到底是什么样的人"},
        {"t": "我现在能不能也做科学？", "d": "三年级能做的一件小事", "v": "我现在能不能也做科学"},
        {"t": "做实验要注意哪些安全？", "d": "哪些事一定不能做", "v": "做实验要注意哪些安全"},
    ],
    "objectives": [
        "能举出两三个身边的例子，说出科技帮我们解决了什么真实问题",
        "能说出科学家共同的做法：爱问为什么、认真观察、动手去试、如实记录、不怕失败",
        "能说出自己现在可以做的一两件科学小事，比如提一个问题、认真记一次观察、把结果照实写下来",
        "知道做观察和小实验时的安全要求：听老师指导、按步骤来，不尝、不混、不用湿手碰电器",
    ],
    "objectives_plain": [
        "能举出两三个身边的例子，说出科技帮我们解决了什么真实问题",
        "能说出科学家共同的做法：爱问为什么、认真观察、动手去试、如实记录、不怕失败",
        "能说出自己现在可以做的一两件科学小事，并愿意动手记一次观察",
        "知道做观察和小实验时的安全要求：听老师指导、按步骤来，不尝、不混、不用湿手碰电器",
    ],
    "standards": [
        {"content": "掌握基本安全知识和技能，学会应对常见安全问题。",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学 中华优秀传统文化"},
        {"content": "科技力量大；走近科学家；争做未来科学家",
         "source": "统编《道德与法治》三年级上册「学科学 爱科学」"},
    ],
    "prereqs": ["pol-e-g3-u1"],
    "prereqs_name": "做学习的主人",
    "prereqs_meta": "pol-e-g3-u1",
    "leads_to": ["pol-e-g3-u3"],
    "next_meta": "pol-e-g3-u3",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "不认路有导航，稻子被虫咬有良种，身体不舒服能查得更清楚——这些背后站着同一件事。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能说出一件自己想动手去弄清楚的事。",
        "objectives": "看清四件事：科技解决了什么、科学家怎么做、我们能做什么、实验要注意什么。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "科技不神秘：遇到了难题，一步一步想办法，把难题变成有办法。",
        "lab-1": "六个难题，六种办法。先点难题再点办法，连错了会提醒你再想一想。",
        "module-2": "科学家的共同做法：爱问为什么、认真观察、动手去试、如实记录、不怕失败；安全记心上。",
        "lab-2": "六件事，每件三个做法。选得不太合适也不会说你错，只会告诉你还可以试试什么。",
        "worked-example": "小雨的绿豆观察六步：提问、猜想、做计划动手试、每天如实记录、发现不一样、再试一次。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "把八条做法分进「像科学家那样做的」和「要调整的」两个筐，分完读一读为什么。",
        "posttest": "出现了忘记录、网上的说法、还要用小刀，看看你能不能把今天的办法用上去。",
        "summary": "四句话：科技力量大、科学家的做法、我们能做的、安全记心上。",
        "homework": "三层小任务，先做前两层，第三层可以请家里人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学道德与法治「中华优秀传统文化」板块在三年级的空缺，正对统编教材三年级上册「学科学 爱科学」（科技力量大、走近科学家、争做未来科学家）。三年级学生容易把科学想成「很遥远、很聪明的人才做的事」，所以全课先把科学拉回到身边：导航、良种、检查设备、保温材料、视频通话，这些看着互不相干的东西做的是同一件事——把生活里的难题一步一步变成办法；再讲科学家共同的做法（爱问为什么、认真观察、动手去试、如实记录、不怕失败），重点放在「如实记录」这一条上：结果和猜想不一样，也照实写下来。最后落到三年级能做的科学小事，并把课标要求的「基本安全知识和技能」具体化为可执行的三句：听老师指导按步骤来、不尝不混、不用湿手碰电器。三个互动台子都能真操作：一个是「难题和办法连连看」，把六个生活难题和六种办法连起来；一个是「科学小侦探」，六张情境卡选做法，反馈一律写成「这样可能会……，还可以试试……」；一个是综合任务，把八条做法分进「像科学家那样做的／要调整的」两个筐。插图一律为中性简洁扁平插画，不使用真人照片，也不做人物崇拜式的表达。",
    "plan_table": """| 1 | cover | 学科学 爱科学 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 科技力量大：身边的科技，帮我们解决真实的问题 | 承·概念一（科技即把难题变办法） |
| 6 | interactive | 动手一：难题和办法，连连看 | 承·配对操作（六组连线） |
| 7 | concept | 走近科学家 · 争做未来科学家 | 承·概念二（科学家的共同做法 + 实验安全） |
| 8 | interactive | 动手二：科学小侦探，你会怎么做？ | 承·情境判断（温和反馈，不判错） |
| 9 | concept | 例题示范：小雨的绿豆发芽观察 | 转·重难点突破（六步示范 + 易错点） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：像科学家那样做的 / 要调整的，把做法分进两个筐 | 合·迁移应用（分类判断） |
| 12 | quiz | 后测：换几个新情境，办法还在不在 | 合·后测 |
| 13 | summary | 小结：四句话，讲清怎么学科学、爱科学 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：科技力量大 / 走近科学家 / 争做未来科学家 三栏\n- P5 身边的科技概念图（已生成）：不认路、稻子被虫咬、身体不舒服等难题与对应办法，附中文标注\n- P7 科学家的共同做法与实验安全图（已生成）：提问 · 猜想 · 动手试 · 如实记录 · 再试一次，附中文标注\n- 三张图均为中性简洁扁平教学插画，不使用真人照片风格，不含可识别的真实人物\n- 涉及实验安全的内容以文字与图示表达，不出现危险操作画面\n- 若需补充：学校实验室安全须知（需学校提供并授权后使用）",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
