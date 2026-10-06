# -*- coding: utf-8 -*-
"""高中 · 心理健康 · 人际关系与沟通（高一）—— 补齐知识树「人际交往」空缺

铁规：语气温和、不评判、不贴标签；不出现任何临床诊断词汇，不涉及自伤自杀与暴力情节。
核心模拟：这样说／那样说对比台（同一句话两种表达 → 对方的感受与后续走向）。
另含：什么时候该向可信的大人求助。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/psych-h-g10-relationship-fig1.webp'
F2 = './assets/psych-h-g10-relationship-fig2.webp'

TTS = {
    "hero": "先说一件你大概经历过的小事。室友半夜还在开着灯，你想让他早点休息。一句是你能不能别这么自私，另一句是我明早有考试，灯亮着睡不着，能不能十一点后关掉台灯。同样一件事，说出来之后的结果往往完全不同。这节课我们就来看看，一句话里到底装了什么。",
    "problem-anchor": "在开始之前，先选出最贴近你的一次经历。是想知道为什么同一句话会有两种结果，还是想知道矛盾来了怎么开口，又或者想知道什么时候该找可信的大人帮忙。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出同一句话里同时传着事和关系两层意思。第二，会用我信息把一句指责改写成别人接得住的话。第三，能说出一句道歉里不能少的三样东西。第四，能判断哪些事自己先试试，哪些事该找可信的大人商量。",
    "pretest": "先做三道小题，凭你现在的习惯选就行，没有对错，也不打分。选完会立刻出现解释，正好帮你看清自己平时习惯哪一种说话方式。",
    "module-1": "我们先把一件事看清楚。一句话里通常装着两层东西：一层是内容，说的是这件事本身；另一层是关系，说的是我怎么看你。说你怎么又忘了带，内容是在讲一件事，关系那层却在说你不靠谱。对方最先接收到的往往是第二层，所以他会先保护自己，再听内容。常见的错误是以为只要道理对，语气不重要，结果道理全对，事情照样谈不成。",
    "lab-1": "现在做一次对比。同一个情境，左边是常见的说法，右边是换过一种的说法，你可以轮流点开，看看对方可能是什么感受、事情接下来会往哪里走。四个情境都在宿舍和教室里，是你真的会遇到的那种。",
    "module-2": "把指责换成我信息，是沟通里最实用的一招。它分四步。第一步说事实，只讲看得见的行为，不加评价。第二步说感受，用我感到开头，而不是你让我。第三步说需要，讲清这件事对你意味着什么。第四步说请求，给一个具体、做得到的做法。比如，十一点后台灯还亮着，我明早要考试睡不着，我需要睡够六个小时，能不能十一点后换成小台灯。四步说起来长，用熟了其实就一句话。",
    "lab-2": "现在你来拼一句道歉。左边选开头怎么说，中间选有没有说清影响，右边选结尾给出什么。拼完会显示这句道歉可能带来什么反应，你再换一种拼法比一比。道歉不是认输，它更像一次关系的修补。",
    "worked-example": "我们看一个完整的示范。小周和室友因为作息闹了两周别扭，两个人都没睡好。第一步，先选时机：等两个人都不赶时间的时候说，不在熄灯前那五分钟。第二步，说事实：这两周我十二点后还在洗漱，影响你休息了。第三步，说影响和感受：你这两天早上都没怎么说话，我有点不安，也不想一直这样。第四步，给请求：以后我十一点半前把洗漱做完，你能不能十二点后把外放的声音关小。第五步，留一个口子：如果你觉得时间不好办，我们可以再商量一下别的办法。整套话里没有一句是评判对方，所以对方接得住。",
    "conceptest-1": "现在用三个容易弄混的说法考考你。请仔细读每一个选项，选出你认为更合适的那个，然后看解释。",
    "synthesis": "最后做一次求助判断，也是这节课最重要的部分。下面有八张小卡片，每张请你想想：这件事我可以自己先试试，还是应该找可信的大人商量，还是需要马上求助。选完会给出解释。判断完，再为自己写一小段沟通剧本。",
    "posttest": "最后换几个新情境检验一下。这次的问题出现在家里、小组作业和一段让你犹豫的关系里，看看你能不能用上前面说过的方法。",
    "summary": "这节课我们弄明白了三件事。第一，一句话里同时装着事和关系，对方最先感受到的是关系那一层。第二，把指责换成我信息，说事实、说感受、说需要、说请求，对方就能接得住。第三，道歉的三样东西是具体的事、真实的影响和下一步的做法。还有一件事请一定记住：自己先试是本事，知道什么时候找可信的大人商量，也是本事。下面卡片上的求助渠道，希望你记住一个。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：把一句你最近说过的指责改写成一整句我信息。第二层能力应用，动手做：挑一次真实的别扭，按四步写一段开场白，找到合适的时机说出去，并记下对方的反应。第三层迁移挑战，选做：写下三个你可以求助的可信大人，包括他们的名字和你能找到他们的方式。",
    "knowledge-graph": "这张图展示了这节课在知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 一句话里的两层意思", "lab-1": "对比台 这样说与那样说", "module-2": "概念二 从指责到我信息",
    "lab-2": "练习台 拼一句道歉", "worked-example": "例题讲解", "conceptest-1": "概念测试",
    "synthesis": "综合任务 求助判断台", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

CUSTOM_JS = r"""
/* ============================================================
   psych-h-g10-relationship 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 这样说／那样说对比台：4 个情境 × 2 种表达 → 感受与走向
   3) 拼一句道歉：开头 × 影响 × 结尾 → 合成句子与反应
   4) 求助判断台：8 张小事卡 × 3 个选项 → 温和反馈
   ============================================================ */
(function () {
  'use strict';

  function cssVar(n, f) {
    var v = getComputedStyle(document.body).getPropertyValue(n).trim();
    return v || f;
  }
  var BRAND = cssVar('--brand', '#60a5fa');
  var BRAND2 = cssVar('--brand-2', '#a78bfa');
  var MUTED = cssVar('--muted', '#93a4bf');

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

  /* ---------- 2. 这样说／那样说对比台 ---------- */
  var SCENES = {
    light: {
      n: '室友半夜还开着大灯',
      fact: '已经十二点，宿舍的大灯还亮着，你明早要考试。',
      hard: '你能不能别这么自私，别人不用睡觉吗。',
      soft: '我明早要考试，灯亮着睡不着，十一点后能不能换成小台灯。',
      hardR: '对方多半会先觉得被指责，第一反应是解释或顶回来，事情容易从关灯变成谁更有理。',
      softR: '对方听到的是一件具体的事加一个具体请求，比较容易直接回应，后面还能继续商量。'
    },
    borrow: {
      n: '同学借了你的笔记没还',
      fact: '上周借出的笔记，说好周一还，现在已经周四了。',
      hard: '你怎么每次都这样，借东西从来不还。',
      soft: '还在你那儿的那本笔记我这两天要用，明天能带来吗。',
      hardR: '每次都这样的说法容易被听成人身评价，对方可能先反驳，笔记反而更难拿回来。',
      softR: '说的是这一本笔记和这个时间，对方不需要先保护自己，直接处理事情就好。'
    },
    nick: {
      n: '有人给你起了你不喜欢的称呼',
      fact: '有同学在班上用你不喜欢的称呼叫你，大家跟着笑。',
      hard: '你这么叫我就是没素质，你等着。',
      soft: '这个称呼让我不太舒服，能不能直接叫我名字。',
      hardR: '带火气的还击常常把场面推向对抗，现场气氛会更尴尬，旁观的同学也不好插话。',
      softR: '只说自己不舒服和希望怎么叫，立场清楚又不伤人，多数同学这时候会顺势改口。'
    },
    parent: {
      n: '和父母说话总被打断',
      fact: '你想说学校的事，说了两句就被父母接过去讲道理。',
      hard: '你们根本不懂，跟你们说不通。',
      soft: '我还没说完就被打断了，我想先把这件事讲完，五分钟就好。',
      hardR: '说不通很容易被听成关门的话，双方都会觉得谈不下去，于是更少说话。',
      softR: '把请求限定成五分钟讲完，父母更容易答应，你也确实把想说的说完了。'
    }
  };
  var sayStage = document.getElementById('say-stage');
  if (sayStage) {
    var scene = 'light';
    var style = 'hard';

    function renderSay() {
      var S = SCENES[scene];
      document.getElementById('say-fact').textContent = '情境：' + S.n + '　' + S.fact;
      document.getElementById('say-hard-txt').textContent = S.hard;
      document.getElementById('say-soft-txt').textContent = S.soft;
      document.querySelectorAll('[data-say-scene]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.sayScene === scene);
      });
      document.querySelectorAll('[data-say-style]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.sayStyle === style);
      });
      var out = document.getElementById('say-out');
      out.className = 'result ' + (style === 'hard' ? 'warn' : '');
      out.innerHTML = style === 'hard'
        ? '<strong>这样说，可能会：</strong>' + S.hardR + '<br>还可以试试右边那种说法。'
        : '<strong>这样说，可能会：</strong>' + S.softR + '<br>它没有评判对方，只说了感受和请求。';
    }

    document.querySelectorAll('[data-say-scene]').forEach(function (b) {
      b.addEventListener('click', function () { scene = b.dataset.sayScene; renderSay(); });
    });
    document.querySelectorAll('[data-say-style]').forEach(function (b) {
      b.addEventListener('click', function () { style = b.dataset.sayStyle; renderSay(); });
    });
    renderSay();
  }

  /* ---------- 3. 拼一句道歉 ---------- */
  var HEAD = {
    avoid: { t: '那天的事就算了吧，别放心上。', s: -2, r: '回避了具体的事，对方很可能觉得你没当回事。' },
    vague: { t: '如果我哪里让你不舒服，我道歉。', s: 0, r: '如果我哪里听起来留了退路，对方容易觉得不够诚恳。' },
    fact: { t: '昨天小组讨论的时候，我把你的方案打断了两次。', s: 2, r: '说清了具体的事和时间，对方知道你在讲哪一桩，也知道你记得。' }
  };
  var MID = {
    none: { t: '', s: 0, r: '没有说到影响，对方可能不知道这件事对你、对他意味着什么。' },
    self: { t: '我当时只顾着讲自己的，散会后我挺过意不去。', s: 2, r: '说自己的感受而不是评价对方，对方更容易听下去。' },
    blame: { t: '不过你当时也没给我机会说。', s: -2, r: '不过两个字一出来，道歉就变成了翻旧账。' }
  };
  var TAIL = {
    threat: { t: '下次你再这样，我也不会客气。', s: -2, r: '以威胁结尾，前面的道歉基本会被抵消。' },
    none: { t: '', s: 0, r: '没有给出下一步，对方不知道以后会有什么不同。' },
    ask: { t: '下次讨论，我想先把你那部分听完再讲自己的。', s: 2, r: '给了一个具体又做得到的做法，对方能看到变化。' }
  };
  var apolStage = document.getElementById('apol-stage');
  if (apolStage) {
    var head = 'fact', mid = 'self', tail = 'ask';

    function renderApol() {
      var H = HEAD[head], M = MID[mid], T = TAIL[tail];
      var score = H.s + M.s + T.s;
      var sentence = [H.t, M.t, T.t].filter(function (x) { return x; }).join('　');
      document.getElementById('apol-sentence').textContent = '「' + sentence + '」';
      var lvl = score >= 5 ? { tag: '比较完整', note: '三样东西都在：具体的事、真实的影响、下一步的做法。' }
        : (score >= 2 ? { tag: '还差一点', note: '已经有了道歉的样子，再看看缺的是哪一样。' }
          : { tag: '容易被听成敷衍', note: '回避、绕弯或反过来指责，都会让修补变得困难。' });
      var tips = [];
      if (H.s < 2) tips.push(H.r);
      if (M.s < 2) tips.push(M.r);
      if (T.s < 2) tips.push(T.r);
      var out = document.getElementById('apol-out');
      out.className = 'result ' + (score >= 5 ? '' : 'warn');
      out.innerHTML = '<strong>' + lvl.tag + '：</strong>' + lvl.note +
        (tips.length ? '<br>' + tips.join('<br>') : '<br>这样说出来，对方接得住，你也不丢面子。');
      document.querySelectorAll('[data-apol-head]').forEach(function (b) { b.classList.toggle('selected', b.dataset.apolHead === head); });
      document.querySelectorAll('[data-apol-mid]').forEach(function (b) { b.classList.toggle('selected', b.dataset.apolMid === mid); });
      document.querySelectorAll('[data-apol-tail]').forEach(function (b) { b.classList.toggle('selected', b.dataset.apolTail === tail); });
    }

    document.querySelectorAll('[data-apol-head]').forEach(function (b) {
      b.addEventListener('click', function () { head = b.dataset.apolHead; renderApol(); });
    });
    document.querySelectorAll('[data-apol-mid]').forEach(function (b) {
      b.addEventListener('click', function () { mid = b.dataset.apolMid; renderApol(); });
    });
    document.querySelectorAll('[data-apol-tail]').forEach(function (b) {
      b.addEventListener('click', function () { tail = b.dataset.apolTail; renderApol(); });
    });
    renderApol();
  }

  /* ---------- 4. 求助判断台 ---------- */
  var CARDS = [
    { t: '自习课上有一道题怎么都想不出来', a: 'self', ok: 'self',
      r: '这类事自己先试试最合适：可以翻书、换个思路，也可以下课后问同学或老师。' },
    { t: '小组里没人愿意跟你一组，已经连着几次了', a: 'adult', ok: 'adult',
      r: '持续被排除在外，自己扛会很累。可以找班主任或心理健康老师说说情况，这不是打小报告。' },
    { t: '和室友为作息吵了两次，你试着说过但没变化', a: 'adult', ok: 'adult',
      r: '你已经自己试过了，效果有限。这时候请宿管或班主任帮忙搭个话，是把事情往前推。' },
    { t: '这次测验没考好，心里挺不好受', a: 'self', ok: 'self',
      r: '先给自己一点时间，也可以找朋友说说。如果这种低落一直持续，同样可以找可信的大人聊。' },
    { t: '有人反复给你发让你难受的消息，你让他停也没停', a: 'now', ok: 'now',
      r: '这种情况需要马上求助：保存消息，告诉信任的大人，让学校帮你处理，不用自己一个人面对。' },
    { t: '妈妈让你少玩手机，你觉得她说得不对', a: 'self', ok: 'self',
      r: '这是可以自己先沟通的事。用我信息说清你的想法和希望，不急着一次谈成。' },
    { t: '你发现自己已经好几周睡不好、干什么都提不起劲', a: 'adult', ok: 'adult',
      r: '持续几周的状态变化值得让大人知道。找家长、班主任或心理健康老师说一说，是照顾自己的方式。' },
    { t: '有人说要让你在班里待不下去', a: 'now', ok: 'now',
      r: '这类让你感到不安的话，请马上告诉班主任或家长，保留证据，让大人介入处理。' }
  ];
  var HELP = { self: '自己先试试', adult: '找可信的大人商量', now: '尽快求助' };
  var askStage = document.getElementById('ask-stage');
  if (askStage) {
    var out = document.getElementById('ask-out');
    var answered = 0;
    var right = 0;
    function renderAsk() {
      document.getElementById('ask-cards').innerHTML = CARDS.map(function (c, i) {
        var btns = ['self', 'adult', 'now'].map(function (k) {
          var cls = 'choice';
          if (c.picked === k) cls += (k === c.ok ? ' correct' : ' wrong');
          return '<button class="' + cls + '" data-ask="' + i + '" data-ask-pick="' + k + '" style="text-align:center;font-size:13px">' + HELP[k] + '</button>';
        }).join('');
        return '<div class="inner-card" style="margin:8px 0">' +
          '<p style="margin:0 0 8px"><strong>' + (i + 1) + '. ' + c.t + '</strong></p>' +
          '<div class="grid" style="grid-template-columns:repeat(3,1fr);gap:6px">' + btns + '</div>' +
          (c.picked ? '<p class="result ' + (c.picked === c.ok ? '' : 'warn') + '" style="margin:8px 0 0">'
            + (c.picked === c.ok ? '<strong>这样判断挺合适。</strong>' : '<strong>还可以再想想：</strong>')
            + c.r + '</p>' : '') +
          '</div>';
      }).join('');
      document.querySelectorAll('[data-ask]').forEach(function (b) {
        b.addEventListener('click', function () {
          var i = parseInt(b.dataset.ask, 10);
          if (CARDS[i].picked) return;
          CARDS[i].picked = b.dataset.askPick;
          if (CARDS[i].picked === CARDS[i].ok) right++;
          answered++;
          renderAsk();
          out.style.display = 'block';
          out.className = 'result' + (right >= 6 ? '' : ' warn');
          out.innerHTML = '<strong>已完成 ' + answered + '/8 张卡片。</strong>' +
            '提醒一句：<em>自己先试试</em>和<em>找人帮忙</em>都不是丢脸的事。' +
            '如果一件事让你持续不安、已经影响到吃饭睡觉，或者你已经试过几次都没有变化，就值得让可信的大人知道。' +
            '请在这节课后，记住至少一个你能找到的求助对象和方式。';
        });
      });
    }
    renderAsk();
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：你平时更习惯哪一种说法？", TTS["pretest"], [
        {"q": "室友半夜还开着大灯，你会怎么说？",
         "options": [("你怎么这么自私，别人不用睡觉吗", False), ("我明早要考试，灯亮着睡不着，十一点后能换小台灯吗", True), ("算了，忍着不说", False)],
         "explain": "第二种只说了自己的处境和一个具体请求，对方比较容易直接回应。<strong>错因提醒：</strong>常见错误是误认为只要道理在自己这边，语气就不重要——对方往往先听到的是评价。"},
        {"q": "同学借了你的笔记一直没还，你更愿意：",
         "options": [("直接说你怎么每次都这样", False), ("说清是哪一本、什么时候要用、希望什么时候还", True), ("从此以后不再借东西给他", False)],
         "explain": "说清具体的事和具体的时间，对方不需要先保护自己，事情才好办。<strong>错因提醒：</strong>用「每次都」开头，容易把一件小事升级成对人的评价。"},
        {"q": "如果一件事你已经自己试过几次，还是没变化，比较合适的是：",
         "options": [("继续自己扛，不想麻烦别人", False), ("找可信的大人商量一下下一步", True), ("干脆放弃，谁都不说了", False)],
         "explain": "自己先试是本事，试过之后找人商量，也是本事。<strong>错因提醒：</strong>容易把求助误认为示弱或者打小报告，其实它只是换一个更有力的办法。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "一句话里，同时装着事和关系", TTS["module-1"], f'''
        <p style="font-size:17px;margin:0 0 12px">同一件事，说法不同，结果常常完全不同。原因就藏在一句话的两层里。</p>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(251,191,36,.45)">
          <p style="margin:0"><strong>为什么要先学这个？</strong>你已经知道，说话是为了把事情讲清楚；但同一句话换个说法，结果常常完全相反；所以我们得先看清一句话里到底装着什么，再学怎么把它说出来。</p>
        </div>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>内容那一层</strong></p>
            <p style="color:var(--muted)">说的是事情本身：灯还亮着、笔记没还、你打断了我的话。在沟通里，这一层<strong>称为</strong>内容层。</p>
          </div>
          <div class="inner-card">
            <p><strong>关系那一层</strong></p>
            <p style="color:var(--muted)">说的是我怎么看你：自私、不可靠、说了也没用。这一层会先被听到，也最容易让人竖起身上的刺。</p>
          </div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">误认为「我讲的道理是对的，对方就该听」。道理对不等于对方接得住——他先要应付关系那一层，才轮得到内容。</p>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="同一情境下两种表达方式的走向对比示意图">
          <figcaption>左边是带评价的说法，箭头很快拐向对抗；右边是只讲事实和请求的说法，箭头继续往前，事情还能谈</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">💬</span><div><strong>小提示：</strong>沟通里的第一句话，往往决定后面五分钟是在解决问题，还是在互相保护。先让对方不必自我保护，事情才谈得下去。</div></div>
{insight_box([
    {"lens": "看见它", "text": "「你怎么又忘了」和「这件事还没做完」讲的是同一件事，可被听到的东西完全不同。"},
    {"lens": "解释它", "text": "人被评价时，第一反应通常是解释或还击，这时候他顾不上处理事情本身——这不是他脾气差，是很自然的反应。"},
    {"lens": "迁移它", "text": "这条规律在家里、在小组作业里、在网上的对话里都一样成立：先去掉评价，事情才有得谈。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "say", 5, "lab-1", "这样说／那样说对比台：同一件事，两种说法", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先选一个情境，再轮流点开两种说法，看看对方的感受和后面会怎么走。</p>
        <div class="lab-panel" id="say-stage">
          <div class="flex-row" style="flex-wrap:wrap">
            <button class="choice" data-say-scene="light" style="text-align:center">室友半夜开大灯</button>
            <button class="choice" data-say-scene="borrow" style="text-align:center">笔记借了没还</button>
            <button class="choice" data-say-scene="nick" style="text-align:center">被起了外号</button>
            <button class="choice" data-say-scene="parent" style="text-align:center">和父母说话被打断</button>
          </div>
          <p class="result" id="say-fact" style="margin-top:12px"></p>
          <div class="flex-row" style="flex-wrap:wrap">
            <button class="choice" data-say-style="hard" style="text-align:center">这样说</button>
            <button class="choice" data-say-style="soft" style="text-align:center">那样说</button>
          </div>
          <div class="grid grid-2" style="margin-top:12px">
            <div class="inner-card"><p><strong>这样说</strong></p><p id="say-hard-txt" style="color:var(--muted)"></p></div>
            <div class="inner-card"><p><strong>那样说</strong></p><p id="say-soft-txt" style="color:var(--muted)"></p></div>
          </div>
          <p class="result" id="say-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>四个情境都点一遍，你发现了什么？</strong>差别不在谁说得多有理，而在<strong>有没有把评价摘出去</strong>。</div></div>
    ''', tag="动手实验室", bloom="analyze"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "把指责换成我信息：四步就够", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">我信息不是要你软下来，而是把话说得对方接得住，事情才推得动。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>说事实：</strong>只讲看得见的行为——十一点半后洗漱、笔记还没还，不加「总是」。</div></div>
          <div class="step"><span class="n">2</span><div><strong>说感受：</strong>用「我感到」开头，说自己，不说「你让我」。</div></div>
          <div class="step"><span class="n">3</span><div><strong>说需要：</strong>讲清这件事对你意味着什么，比如我想睡够六个小时。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>说请求：</strong>给一个具体、做得到的做法，并且留一句「也可以商量」。</div></div>
        </div>
        <div class="inner-card">
          <p><strong>关于边界，也说三句：</strong>同学之间出现好感是正常的事；友谊和恋爱是两种不同的关系，都需要尊重对方的意愿和节奏；别人的好意不等于必须回应，你的拒绝也不需要道歉到失去自己。</p>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="我信息四步流程示意图：事实、感受、需要、请求">
          <figcaption>四步像一条流水线：事实是入口，请求是出口，中间的称呼和解说越少，对方越容易跟上</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🧩</span><div><strong>换个说法：</strong>把「你」开头的句子翻译成「我」开头，就像把一记直球换成一次递手——同样是表达，对方不用先躲。</div></div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "apol", 7, "lab-2", "练一练：拼出一句对方接得住的道歉", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">三段各选一句，看看拼出来的道歉会带来什么反应，再换一种拼法比一比。</p>
        <div class="lab-panel" id="apol-stage">
          <div class="slider-row" style="display:block">
            <div style="font-weight:700;font-size:14px">① 开头怎么说这件事</div>
            <div class="flex-row" style="flex-wrap:wrap">
              <button class="choice" data-apol-head="avoid" style="text-align:center;font-size:13px">那天的事就算了吧</button>
              <button class="choice" data-apol-head="vague" style="text-align:center;font-size:13px">如果我哪里让你不舒服</button>
              <button class="choice" data-apol-head="fact" style="text-align:center;font-size:13px">昨天讨论我打断了你两次</button>
            </div>
          </div>
          <div class="slider-row" style="display:block;margin-top:12px">
            <div style="font-weight:700;font-size:14px">② 有没有说清影响</div>
            <div class="flex-row" style="flex-wrap:wrap">
              <button class="choice" data-apol-mid="none" style="text-align:center;font-size:13px">（不加这一句）</button>
              <button class="choice" data-apol-mid="self" style="text-align:center;font-size:13px">我当时只顾讲自己的，散会后挺过意不去</button>
              <button class="choice" data-apol-mid="blame" style="text-align:center;font-size:13px">不过你当时也没给我机会</button>
            </div>
          </div>
          <div class="slider-row" style="display:block;margin-top:12px">
            <div style="font-weight:700;font-size:14px">③ 结尾怎么说下一步</div>
            <div class="flex-row" style="flex-wrap:wrap">
              <button class="choice" data-apol-tail="threat" style="text-align:center;font-size:13px">下次你再这样我也不客气</button>
              <button class="choice" data-apol-tail="none" style="text-align:center;font-size:13px">（不加这一句）</button>
              <button class="choice" data-apol-tail="ask" style="text-align:center;font-size:13px">下次我想先听完你那部分</button>
            </div>
          </div>
          <p class="result" id="apol-sentence" style="margin-top:14px"></p>
          <p class="result warn" id="apol-out" style="margin-top:8px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧪</span><div><strong>挑战：</strong>把三段都换一遍，找出<strong>唯一</strong>一组能让反馈变成「比较完整」的组合。记住这三样东西：具体的事、真实的影响、下一步的做法。</div></div>
    ''', tag="动手实验室", bloom="apply"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：和室友闹了两周别扭，怎么开口", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(251,191,36,.45)">
          <p style="margin:0"><strong>情境：</strong>小周和室友因为作息别扭了两周，两个人都没睡好，这几天见面基本不说话。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>选时机：</strong>等两个人都赶时间的那五分钟过去再说，不在熄灯前开口。</div></div>
          <div class="step"><span class="n">2</span><div><strong>说事实：</strong>这两周我十二点后还在洗漱，影响你休息了。</div></div>
          <div class="step"><span class="n">3</span><div><strong>说感受：</strong>你这两天早上都没怎么说话，我有点不安，也不想一直这样。</div></div>
          <div class="step"><span class="n">4</span><div><strong>说请求：</strong>以后我十一点半前把洗漱做完，你十二点后能把外放的声音关小吗。</div></div>
          <div class="step"><span class="n green">5</span><div><strong>留口子：</strong>如果你觉得时间不好办，我们可以再商量别的办法。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">不少同学会等对方先开口，误认为先说话就是先认输。其实先开口的人只是先动手把事情往前推；真正的关键在这句话里<strong>有没有评价对方</strong>。整套示范里没有一句是评判，所以对方接得住。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "下面哪一句最接近我信息的说法？",
         "options": [("你每次都把东西乱放，太不自觉了", False),
                     ("桌上堆着我的书，我找不到要用的那本，能帮我一起收拾一下吗", True),
                     ("算了，我自己收就是了", False)],
         "explain": "第二种只讲事实、影响和请求，没有给对方下判断。<strong>错因提醒：</strong>用「每次都」开头，很容易把一件小事升级成对人的评价——这是沟通里最常见的搞混：把事和人混在一起说。"},
        {"q": "一句道歉里，下面哪三样东西不能少？",
         "options": [("具体的事、真实的影响、下一步的做法", True),
                     ("好听的话、礼物、保证", False),
                     ("解释原因、说明对方也有错、再道一次歉", False)],
         "explain": "道歉的重点是让对方知道你看清了哪件事、它带来了什么、以后会有什么不同。<strong>错因提醒：</strong>误认为道歉就是态度软，于是拼命加好话，反而绕开了最该说清的那一件事。"},
        {"q": "关于求助，下面哪种想法更合适？",
         "options": [("自己先试是本事，试过之后找人商量也是本事", True),
                     ("找人帮忙就说明我不行", False),
                     ("只要告诉老师，就是在打小报告", False)],
         "explain": "求助只是换一个更有力的办法推进事情，尤其是持续被排除、反复被为难这类自己扛不动的情况。<strong>错因提醒：</strong>把求助和打小报告搞混，是最容易让人独自硬撑的常见错误。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "ask", 10, "synthesis", "综合任务：这件事，我该自己试还是找大人帮忙？", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">八张小卡片，各选一个判断。选完会给出解释，全部点完后下面会有一段小结。</p>
        <div class="lab-panel" id="ask-stage">
          <div id="ask-cards"></div>
          <p class="result warn" id="ask-out" style="margin-top:12px;display:none"></p>
        </div>
        <div class="inner-card">
          <p><strong>写下来，留给自己：</strong></p>
          <p style="color:var(--muted)">如果现在有一件事让你为难，你第一个愿意开口的人是谁？你打算怎么跟他说第一句？</p>
          <textarea id="syn-answer" rows="3" placeholder="我第一个想到的人是……我打算先说……" style="margin-top:8px"></textarea>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🤝</span><div><strong>请记住一个渠道：</strong>班主任、家长、心理健康老师、你信任的任何一位长辈——记住其中一个，以及你能找到他的方式。</div></div>
    ''', tag="综合任务", bloom="evaluate"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，看看方法还在不在", TTS["posttest"], [
        {"q": "小组作业里，有同学总是不做自己那部分，你打算怎么开口？",
         "options": [("说你到底要不要做，大家都等着你", False),
                     ("这周三要交，你那部分还没动，我有点着急，今晚能先给我一版初稿吗", True),
                     ("在群里不说话，自己把活全干了", False)],
         "explain": "说清时间、影响和一个具体的请求，比质问更容易得到回应。自己全干完虽然省了口舌，但下次还是会碰上同样的情况。"},
        {"q": "有同学对你有好感，但你只想做朋友。比较合适的是：",
         "options": [("明确说清自己的想法，同时尊重对方，不嘲笑也不传播", True),
                     ("不回复、慢慢躲开，让对方自己猜", False),
                     ("把这件事讲给全班听", False)],
         "explain": "友谊和恋爱是两种不同的关系，都需要尊重对方的意愿和节奏。说清楚、不伤人，也是对自己负责。<strong>错因提醒：</strong>误认为拖着不回应比较不伤人，其实猜测往往比一句清楚的话更让人难受。"},
        {"q": "你已经在班群里被人反复说不友善的话，让他们停也没停。接下来更合适的是：",
         "options": [("保存消息，马上告诉班主任或家长", True),
                     ("在群里用同样的话回敬过去", False),
                     ("退出群，谁也不说", False)],
         "explain": "持续被为难而自己止不住时，让大人介入是最快的办法，保留记录能帮你说清事情经过。<strong>错因提醒：</strong>常见错误是觉得说了也没用，于是独自忍着——事情往往因此拖得更久。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把自己讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>一句话两层</strong>：内容之外还有关系那一层，对方先听到的往往是关系。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>我信息四步</strong>：说事实、说感受、说需要、说请求，把评价摘出去，事情才谈得下去。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>道歉三样</strong>：具体的事、真实的影响、下一步的做法——少一样都会打折。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(251,191,36,.45)">
          <p style="margin:0"><strong>还有一件同样重要的事：</strong>自己先试是本事，知道什么时候找可信的大人商量，也是本事。请在这节课后记住至少一个你能找到的求助对象。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「事实、感受、请求」这三个词，把一次真实的别扭说成对方接得住的话。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "把一句你最近说过的指责，改写成一句完整的我信息：事实、感受、需要、请求四样齐全。",
            "写出道歉不能少的三样东西，各用一句话说明为什么。",
        ],
        [
            "挑一次真实的别扭，按四步写一段开场白，找到合适的时机说出去，记下对方的第一反应。",
            "用对比台里的四个情境，各写一句你觉得更合适的说法，念一遍给自己听。",
        ],
        [
            "写下三个你可以求助的可信大人，包括他们的名字和你能找到他们的方式，放在你看得到的地方。",
            "连续三天观察身边一次对话，用「内容和关系」两层来分析它为什么谈得下去或者谈不下去。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "psych-h-g10-relationship",
    "node_id": "psych-h-g10-relationship",
    "subject": "psychology",
    "subject_cn": "心理健康",
    "stage": "high",
    "stage_cn": "高中",
    "curriculum": "中小学心理健康教育指导纲要（2012年修订）/ 教育部相关要求 · 高中",
    "title": "人际关系与沟通：把话说清楚",
    "name_en": "Interpersonal Relationships and Communication",
    "grade": 10,
    "grade_cn": "高一",
    "domain": "interpersonal",
    "domain_cn": "人际交往",
    "lesson_type": "workshop",
    "version": "1.0.0",
    "description": "面向高一学生的人际沟通课：从「同一句话换一种说法结果完全不同」这个现象出发，讲清一句话里同时装着内容与关系两层，练习把指责改写为我信息的四步（事实、感受、需要、请求），并掌握道歉不能少的三样东西。核心模拟是「这样说／那样说」对比台——同一情境下两种表达轮流点开，可以看到对方可能的感受和事情接下来的走向；第二个台子让学生自己拼出一句道歉，实时看到评价，并挑战找出唯一完整的组合。综合任务是一张求助判断台：八张真实校园小事卡，各自判断「自己先试试、找可信的大人商量、尽快求助」，把「什么时候该向可信的大人求助」讲清楚。全课语气温和、不评判、不贴标签，涉及同伴关系时同时说明尊重意愿与界限，不涉及任何伤害性情节。",
    "tags": ["人际沟通", "我信息", "道歉与修复", "求助边界", "尊重与界限", "高一"],
    "standard_ref": "《中小学心理健康教育指导纲要（2012年修订）· 高中》人际交往——正确认识人际关系状况，培养人际沟通能力，促进积极的情感反应和体验；正确对待同伴交往，知道友谊与好感的界限。",
    "hero_question": "同一句话，为什么换一种说法，结果就完全不同？",
    "hero_alt": "人际关系与沟通知识结构图三栏：一句话里的两层、我信息四步、什么时候该求助",
    "hero_caption": "人际关系与沟通：内容之外还有关系那一层 · 事实感受需要请求四步 · 自己先试和找人帮忙都是本事",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个最贴近你经历的困惑，后面的内容都会围着它展开。",
    "anchor_choices": [
        {"t": "为什么同一句话有两种结果？", "d": "我讲的道理明明是对的，对方却听不进去", "v": "为什么同一句话有两种结果"},
        {"t": "和室友、同学的别扭怎么开口？", "d": "憋着不说难受，一开口又容易吵起来", "v": "和室友同学的别扭怎么开口"},
        {"t": "道歉的话该怎么说才不敷衍？", "d": "说了对不起，对方还是觉得我没当回事", "v": "道歉的话该怎么说才不敷衍"},
        {"t": "什么时候该找可信的大人帮忙？", "d": "想找人帮，又怕被说打小报告", "v": "什么时候该找可信的大人帮忙"},
    ],
    "objectives": [
        "能说出同一句话里同时传着内容与关系两层，并解释为什么关系那一层先被听到",
        "会用我信息的四步——事实、感受、需要、请求，把一句指责改写成对方接得住的话",
        "能说出一句道歉不能少的三样东西，并拼出一句完整的道歉",
        "能判断哪些事自己先试试、哪些事该找可信的大人商量，并说出至少一个求助渠道",
    ],
    "objectives_plain": [
        "能说出同一句话里同时传着内容与关系两层，并解释为什么关系那一层先被听到",
        "会用我信息的四步——事实、感受、需要、请求，把一句指责改写成对方接得住的话",
        "能说出一句道歉不能少的三样东西，并拼出一句完整的道歉",
        "能判断哪些事自己先试试、哪些事该找可信的大人商量，并说出至少一个求助渠道",
    ],
    "standards": [
        {"content": "正确认识人际关系状况，培养人际沟通能力，促进积极的情感反应和体验",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》高中 · 人际交往"},
        {"content": "正确对待同伴交往，知道友谊与好感的界限，学会尊重对方的意愿和节奏",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》高中 · 人际交往"},
    ],
    "prereqs": ["psych-h-g10-learning-strategy"],
    "prereqs_name": "学习策略与考试适应",
    "prereqs_meta": "psych-h-g10-learning-strategy",
    "leads_to": ["psych-h-g11-emotion-resilience"],
    "next_meta": "psych-h-g11-emotion-resilience",
    "section_images": ["assets/psych-h-g10-relationship-fig1.webp", "assets/psych-h-g10-relationship-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "同一件事，两种说法，两种结果——差别就藏在一句话的两层里。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能把一次别扭说成一句对方接得住的话。",
        "objectives": "看清四件事：一句话的两层、我信息四步、道歉三样、什么时候该找大人帮忙。",
        "pretest": "凭现在的习惯选就好，不打分。前测只是帮你看清自己平时习惯哪种说法。",
        "module-1": "内容之外还有关系那一层，对方往往先听到后者——所以道理对不等于谈得成。",
        "lab-1": "四个情境，每个都点开两种说法，比较对方可能的感受和事情的走向。",
        "module-2": "四步：说事实、说感受、说需要、说请求，把评价摘出去。",
        "lab-2": "三段各选一句，拼出道歉，再找出唯一那组完整组合。",
        "worked-example": "五步示范：选时机、说事实、说感受、说请求、留口子。",
        "conceptest-1": "三个选项里藏着最常见的几个误解，选完请把每条解释读一遍。",
        "synthesis": "八张小卡片各选一个判断，全部点完会看到一段小结。",
        "posttest": "小组作业、同伴好感和群里的为难，三个新情境看看方法还在不在。",
        "summary": "用「事实、感受、请求」三个词，把一次别扭说清楚；再记住一个求助渠道。",
        "homework": "三层练习，前两层做完就算通关，第三层留给愿意更进一步的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先帮你找到卡点，再给一个最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是高中「人际交往」板块里长期空缺的一课。设计上不讲大道理，只做两件可练的事：把一句话里的评价摘出去，把求助的边界想清楚。核心模拟是一张「这样说／那样说」对比台，四个真实校园情境各配两种表达，学生轮流点开就能看到对方可能的感受与事情的走向；第二个台子让学生自己拼一句道歉，三段选择实时合成一句话，并挑战找出唯一完整的组合。综合任务是一张求助判断台，八张小事卡分别判断「自己先试试、找可信的大人商量、尽快求助」，把「什么时候该向可信的大人求助」讲清楚，并请学生记住至少一个求助渠道。全课语气温和、不评判、不贴标签，涉及同伴关系时说明尊重意愿与界限。",
    "plan_table": """| 1 | cover | 人际关系与沟通：把话说清楚 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：你平时更习惯哪一种说法？ | 起·前测（暴露现有习惯） |
| 5 | concept | 一句话里，同时装着事和关系 | 承·概念一（内容层与关系层） |
| 6 | interactive | 这样说／那样说对比台：同一件事，两种说法 | 承·核心模拟（感受与走向对比） |
| 7 | concept | 把指责换成我信息：四步就够 | 承·概念二（事实感受需要请求 + 尊重与界限） |
| 8 | interactive | 练一练：拼出一句对方接得住的道歉 | 承·练习台（三段合成 + 评价） |
| 9 | concept | 例题示范：和室友闹了两周别扭，怎么开口 | 转·重难点突破（五步示范 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：这件事，我该自己试还是找大人帮忙？ | 合·求助判断台（迁移应用） |
| 12 | quiz | 后测：换几个新情境，看看方法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把自己讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：一句话里的两层、我信息四步、什么时候该求助 三栏\n- P5 两种表达走向对比图（已生成）：带评价的说法拐向对抗，只讲事实的说法继续往前\n- P7 我信息四步流程示意图（已生成）：事实、感受、需要、请求\n- 若需补充：一张可打印的求助渠道卡（空白填写版）、一张道歉三样清单",
}
