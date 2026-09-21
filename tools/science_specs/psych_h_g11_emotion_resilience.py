# -*- coding: utf-8 -*-
"""高中 · 心理健康 · 情绪管理与抗挫力（高二）—— 补齐知识树「情绪调适」空缺

铁规：语气温和、不评判、不贴标签；不出现任何临床诊断词汇，不涉及自伤自杀与暴力情节。
不做情绪放大，不承诺「一定变好」。
核心模拟：情绪调节工具箱（点选当下情境 → 选方法 → 看可能的走向）。
另含：失败后的归因区分（我能影响的 / 我影响不了的）。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/psych-h-g11-emotion-resilience-fig1.webp'
F2 = './assets/psych-h-g11-emotion-resilience-fig2.webp'

TTS = {
    "hero": "先想一个最近的时刻。也许是一场没考好的试，也许是一句没接住的话，也许只是某天晚上，事情堆在一起，你什么都不想开始。这种时候，我们常常先怪自己状态不好，却很少停下来看看身上发生了什么。这节课我们不谈大道理，只准备一个工具箱，里面放四件做得到的小事，再加上一个很关键的动作——把一件事分成我能影响的和影响不了的。",
    "problem-anchor": "在开始之前，先选出最贴近你最近状态的一项。是想知道情绪来的时候身上会发生什么，还是想知道那一刻可以做什么，又或者是想弄明白失败之后该怎么看这件事。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出情绪来的时候，身体、念头和行为三条线上分别有什么信号。第二，会用情绪调节工具箱，给自己当下的情境挑一件做得到的事。第三，能把一件不如意的事分成我能影响的和影响不了的两部分。第四，能说清这些方法能做什么、不能做什么，不会把它们当成必须立刻见效的承诺。",
    "pretest": "先做三道小题，凭你平时的习惯选就行，没有对错，也不打分。选完会立刻出现解释，正好帮你看清自己现在习惯用哪种方式应对。",
    "module-1": "我们先看清一件事。情绪来的时候，最早出现的变化常常不在想法里，而在身体上：肩膀紧起来、呼吸变浅、胃里发沉。接着是念头，比如完了、来不及了、我肯定不行。最后是行为，比如一遍遍刷手机、把书合上、谁都不想理。这三条线上的变化合起来，称为情绪信号。常见的错误是把它们当成想太多，于是只劝自己别想了，却不管身体和手上正在发生的事。",
    "lab-1": "现在打开工具箱。先选一个你最近真的遇到过的情境，再从四件小事里挑一件。你可以在同一个情境里把四件都试一遍，看看它们各自可能把事情带到哪里。请留意，这里的说法都是可能，不是保证。",
    "module-2": "四件小事里，最要紧的是换个角度，也就是把一件事分成两栏。左边写我能影响的，比如今晚先做哪两道题、明天怎么跟老师说；右边写我影响不了的，比如这次卷子的难度、别人当时的想法、已经过去的那些日子。分完你会发现，右边那一栏不需要你去扛，左边那一栏通常只剩一两件具体的事。请注意，这些方法不能让事情立刻变好，它们的用处是先让事情变得能处理。",
    "lab-2": "再看同一件事的两种看法。左边一种把注意力放在影响不了的部分，右边一种放在能影响的部分。你轮流点开，比较一下它们分别带来什么感受、下一步有没有变化。",
    "worked-example": "我们完整走一遍。情境是：一场准备了很久的考试，结果比预期低了不少，你连着两三天都不太想说话。第一步，先认信号：睡得比平时晚、白天没什么力气、不想提这件事。第二步，停一下，先让身体缓下来，去操场走十分钟，不做决定。第三步，分成两栏：我能影响的是下次复习的安排、错题的处理、跟老师问清漏在哪；我影响不了的是这次卷子的难度、已经过去的分数。第四步，从能影响的栏里挑一件小到三分钟能做完的事。第五步，找一个愿意听的人说三句，不必把整件事讲完。",
    "conceptest-1": "现在用三个容易弄混的说法考考你。请仔细读每一个选项，选出你认为更合适的那个，然后看解释。",
    "synthesis": "最后做一次分栏练习。下面有八张说法卡，每一张请你判断：它属于我能影响的，还是我影响不了的。判断完会给出解释，也请你留意自己在哪一类上花的时间更多。",
    "posttest": "最后换几个新情境检验一下。这次的问题出现在一场比赛、一段关系和一次小组合作里，看看你能不能用上前面说过的方法。",
    "summary": "这节课我们弄明白了三件事。第一，情绪会先在身体、念头和行为三条线上留下信号，认出信号是第一步。第二，工具箱里有四件做得到的小事，其中最关键的是把一件事分成我能影响的和影响不了的。第三，这些方法不能让事情立刻变好，它们的作用是先让事情变得能处理。所以请把要求放低一点：今天只做一件小事，也算数。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写下你紧张时的三个身体信号，越具体越好。第二层能力应用，动手做：找一件最近让你不太舒服的事，分成两栏写下来，再从能影响的那栏里挑一件明天能做完的小事。第三层迁移挑战，选做：连续七天记录一次情绪信号和当时的应对方式，一周后回看，找出对你最管用的那一件。",
    "knowledge-graph": "这张图展示了这节课在知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 情绪的三条信号线", "lab-1": "核心模拟 情绪调节工具箱", "module-2": "概念二 分成两栏看",
    "lab-2": "对比台 两种看法", "worked-example": "例题讲解", "conceptest-1": "概念测试",
    "synthesis": "综合任务 归因分栏台", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

CUSTOM_JS = r"""
/* ============================================================
   psych-h-g11-emotion-resilience 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 核心模拟：情绪调节工具箱（情境 × 四件小事 → 可能的走向）
   3) 两种看法对比台（同一件事 × 两种注意力 → 感受与下一步）
   4) 归因分栏台（8 张说法卡 → 我能影响的 / 我影响不了的）
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

  /* ---------- 2. 情绪调节工具箱 ---------- */
  var TOOLS = {
    breathe: { n: '先让身体缓下来', d: '去走动、喝口水、洗把脸、把呼吸放慢一点' },
    reframe: { n: '换个角度看', d: '把这件事分成我能影响的和影响不了的' },
    tiny: { n: '先做一件小事', d: '小到三分钟能做完、一定做得到的那种' },
    talk: { n: '找人说说', d: '找一个愿意听的人，说三句就够，不必讲完' }
  };
  var BOX = {
    homework: {
      n: '明天要交的作业，今晚还差一大半',
      breathe: '先离开桌子两分钟，接杯水、站到窗边把呼吸放慢。回来以后，桌上的东西看起来还是那么多，但你握笔的手会稳一些。它没有让作业变少。',
      reframe: '分成两栏：我能影响的是这两个小时先做哪一块、要不要跟老师说一声；我影响不了的是现在还剩多少时间。分完，右边那栏就不用再算了。',
      tiny: '挑最小的一块开始：先把第一道大题读完、写下已知条件。三分钟能做完的事，往往比「把作业写完」更容易真的动起来。',
      talk: '给朋友发一句：今晚有点赶，我先把数学做完再说。说出来的好处是你不用一个人硬撑，也不用解释太多。'
    },
    friend: {
      n: '和好朋友闹了别扭，两天没说话',
      breathe: '这两天你是不是一想到就胸口发紧？先让身体松一点，去走一圈再想这件事。身体先松下来，话才想得清楚。',
      reframe: '分成两栏：我能影响的是我要不要先开口、怎么说；我影响不了的是对方现在怎么想、当时那句话为什么脱口而出。分完，你会发现能影响的那栏只有一句话。',
      tiny: '先做一件很小的事：把想说的第一句写下来，不必发出去。写下来这件事，本身就是往前动了一小步。',
      talk: '找一个不在你们两个人之间的朋友，把过程说三句。有时候说完你自己就明白该不该先开口了。'
    },
    result: {
      n: '准备了很久的事，结果不如意',
      breathe: '这种时候身体常常比脑子还累。先去操场走十分钟或者早点躺下，今晚不做任何重要决定。',
      reframe: '分成两栏：我能影响的是下一次怎么准备、哪里可以补、要不要找人问清楚；我影响不了的是这一次的结果、别人的评价。分完，右手那栏可以先放下。',
      tiny: '从能影响的那栏里挑一件三分钟能做完的事：把这次没弄懂的那一页折个角。今天到此为止，也算数。',
      talk: '找一个愿意听的人，说三句就够：这次结果不好、我现在有点难受、我打算先做那一件小事。不用把整件事讲完。'
    },
    pile: {
      n: '事情堆在一起，哪件都不想开始',
      breathe: '先别列清单。站起来走一圈、把水杯洗掉，让眼睛离开屏幕一会儿。这一步没有产出的样子，但它会让你重新坐得住。',
      reframe: '分成两栏：我能影响的是今天只处理哪一件；我影响不了的是所有事今天都做完这个要求。分完，清单会短很多。',
      tiny: '挑那种三分钟能做完的：把要用的书翻到该翻的那页、把明天的闹钟设好。开始动了，后面往往就跟着动了。',
      talk: '跟身边人说一句：我今晚事情有点多，先做一件。说出来以后，你就不必再花力气假装自己没事。'
    }
  };
  var boxStage = document.getElementById('box-stage');
  if (boxStage) {
    var sc = 'homework', tl = 'tiny';
    function renderBox() {
      var S = BOX[sc], T = TOOLS[tl];
      document.getElementById('box-scene').textContent = '情境：' + S.n;
      document.querySelectorAll('[data-box-scene]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.boxScene === sc);
      });
      document.querySelectorAll('[data-box-tool]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.boxTool === tl);
      });
      var out = document.getElementById('box-out');
      out.className = 'result';
      out.innerHTML = '<strong>' + T.n + '，可能会：</strong>' + S[tl] +
        '<br><span style="color:var(--muted)">说明一下：它不一定让事情马上变好，通常只是先让你能继续处理它。</span>';
    }
    document.querySelectorAll('[data-box-scene]').forEach(function (b) {
      b.addEventListener('click', function () { sc = b.dataset.boxScene; renderBox(); });
    });
    document.querySelectorAll('[data-box-tool]').forEach(function (b) {
      b.addEventListener('click', function () { tl = b.dataset.boxTool; renderBox(); });
    });
    renderBox();
  }

  /* ---------- 3. 两种看法对比台 ---------- */
  var VIEWS = {
    exam: {
      n: '一次没考好的试',
      f: '我准备了这么久还是这样，大概我就到这了。',
      t: '这次有几块确实没弄懂，先把最不明白的那一章翻一遍。',
      fr: '注意力全放在结果上，人会先没力气，接着连翻书这一步也做不了。',
      tr: '注意力放在能动的部分，下一步变得具体，做得到的话就容易真的开始。'
    },
    match: {
      n: '一场比赛输了',
      f: '对手太强了，我们根本没机会。',
      t: '我们的配合问题出在哪一段，下次练球先练这一段。',
      fr: '这个说法听上去很省力，但它把整件事都交出去了，队伍里也就没人再提可改的地方。',
      tr: '把注意力放回可改的配合上，输球这件事就变成了一条具体的练习线索。'
    },
    team: {
      n: '小组作业里有人一直没做他那部分',
      f: '他就是这样的人，说也没用。',
      t: '离交作业还有三天，我可以说清时间和他那部分，也可以和老师说明情况。',
      fr: '一旦认定对方不会变，你连开口这一步都省了，最后常常是自己全干完，然后再难受一次。',
      tr: '能影响的一栏里其实有两三个选项，说出来之后，事情至少有了往前走的可能。'
    }
  };
  var viewStage = document.getElementById('view-stage');
  if (viewStage) {
    var vs = 'exam', vw = 'fix';
    function renderView() {
      var V = VIEWS[vs];
      document.getElementById('view-scene').textContent = '情境：' + V.n;
      document.getElementById('view-fixed-txt').textContent = V.f;
      document.getElementById('view-fix-txt').textContent = V.t;
      document.querySelectorAll('[data-view-scene]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.viewScene === vs);
      });
      document.querySelectorAll('[data-view-way]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.viewWay === vw);
      });
      var out = document.getElementById('view-out');
      out.className = 'result ' + (vw === 'fixed' ? 'warn' : '');
      out.innerHTML = vw === 'fixed'
        ? '<strong>把注意力放在结果上，可能会：</strong>' + V.fr + '<br>还可以试试另一种看法。'
        : '<strong>把注意力放在能影响的部分，可能会：</strong>' + V.tr + '<br>它没有改变已经发生的事，但让下一步变得看得见。';
    }
    document.querySelectorAll('[data-view-scene]').forEach(function (b) {
      b.addEventListener('click', function () { vs = b.dataset.viewScene; renderView(); });
    });
    document.querySelectorAll('[data-view-way]').forEach(function (b) {
      b.addEventListener('click', function () { vw = b.dataset.viewWay; renderView(); });
    });
    renderView();
  }

  /* ---------- 4. 归因分栏台 ---------- */
  var PILE = [
    { t: '这次卷子最后两道题的题型我没练过', a: 'can',
      r: '题型的准备是可以安排的：下次提前把这几类各练两道。它属于我能影响的那一栏。' },
    { t: '考试那两天我睡得不太好', a: 'can',
      r: '睡眠这件事有一部分可以调整，比如提前两天把作息往前挪半小时。不用一次改到位。' },
    { t: '这次的题目本来就偏难', a: 'cannot',
      r: '难度不由你决定，这一栏不必再花力气。知道它偏难，反而能帮你把标准定得合理一些。' },
    { t: '老师改卷的标准我不太清楚', a: 'can',
      r: '不清楚的部分是可以问的：找老师确认一遍给分点，下次就少一层不确定。' },
    { t: '我同桌一直比我考得好', a: 'cannot',
      r: '别人的分数你影响不了，比较也带不来下一步。把这一栏放下，能省下不少力气。' },
    { t: '我爸妈看到成绩时的表情', a: 'cannot',
      r: '别人的情绪和反应不归你控制。你可以在之后跟他们说说你的打算，但那不是你必须承担的部分。' },
    { t: '我这周复习时一直开着手机', a: 'can',
      r: '这是一个具体、可改的动作，比如把手机放到另一个房间。它属于能影响的那一栏，而且改起来不算难。' },
    { t: '我上次没弄懂的那一章还在那儿', a: 'can',
      r: '已经发生的事改不了，但把它补上是可以安排的。这一条恰好是能影响的那一栏里最有用的一个。' }
  ];
  var pileStage = document.getElementById('pile-stage');
  if (pileStage) {
    function renderPile() {
      var out = document.getElementById('pile-out');
      document.getElementById('pile-cards').innerHTML = PILE.map(function (c, i) {
        var btns = ['can', 'cannot'].map(function (k) {
          var cls = 'choice';
          if (c.picked === k) cls += (k === c.a ? ' correct' : ' wrong');
          return '<button class="' + cls + '" data-pile="' + i + '" data-pile-pick="' + k +
            '" style="text-align:center;font-size:13px">' + (k === 'can' ? '我能影响的' : '我影响不了的') + '</button>';
        }).join('');
        return '<div class="inner-card" style="margin:8px 0">' +
          '<p style="margin:0 0 8px"><strong>' + (i + 1) + '. ' + c.t + '</strong></p>' +
          '<div class="grid" style="grid-template-columns:repeat(2,1fr);gap:6px">' + btns + '</div>' +
          (c.picked ? '<p class="result ' + (c.picked === c.a ? '' : 'warn') + '" style="margin:8px 0 0">' +
            (c.picked === c.a ? '<strong>这样分挺合适。</strong>' : '<strong>还可以再想想：</strong>') + c.r + '</p>' : '') +
          '</div>';
      }).join('');
      document.querySelectorAll('[data-pile]').forEach(function (b) {
        b.addEventListener('click', function () {
          var i = parseInt(b.dataset.pile, 10);
          if (PILE[i].picked) return;
          PILE[i].picked = b.dataset.pilePick;
          renderPile();
          var done = PILE.filter(function (x) { return x.picked; }).length;
          out.style.display = 'block';
          out.className = 'result' + (done >= 8 ? '' : ' warn');
          out.innerHTML = '<strong>已完成 ' + done + '/8 张卡片。</strong>' +
            '提醒一句：分栏的目的不是把责任都推给外面，也不是把什么都扛在自己身上，' +
            '而是让你看清哪一栏真的可以动手。所以每次分完，请只从「我能影响的」那一栏里挑<em>一件</em>小事。' +
            (done >= 8 ? '<br>八张都分完了。你可以回头看看，自己在哪一栏停留的时间更长。' : '');
        });
      });
    }
    renderPile();
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：状态不好的时候，你习惯怎么办？", TTS["pretest"], [
        {"q": "明天要交作业，今晚还差一大半，你心里很紧。下面哪种做法更用得上？",
         "options": [("先在心里反复催自己，直到坐回桌前", False),
                     ("先离开桌子两分钟，回来挑最小的一块开始", True),
                     ("干脆不做了，先刷一会儿手机", False)],
         "explain": "先让身体缓一点，再挑一件三分钟能做完的事，通常比反复催自己更容易真的动起来。<strong>错因提醒：</strong>常见错误是误认为必须先有状态才能开始，其实很多时候是先开始一点，状态才跟上。"},
        {"q": "一件事结果不好，下面哪种想法更接近「分成两栏」的做法？",
         "options": [("全都是我的问题，是我做得不好", False),
                     ("这次难度高不由我决定，下一次怎么准备我能安排", True),
                     ("运气太差了，跟我没什么关系", False)],
         "explain": "把影响不了的部分放下，把能影响的部分留下，才不会把力气用光在没法动的地方。<strong>错因提醒：</strong>容易把「分栏」搞混成「推卸责任」——它其实是让你找到真正能动手的那一小块。"},
        {"q": "关于这几件调节方法，下面哪种说法更贴近事实？",
         "options": [("用了就一定会马上变好", False),
                     ("它们不一定让事情马上变好，但常常先让事情变得能处理", True),
                     ("方法没用，只能等时间过去", False)],
         "explain": "把这句期待放低一点，反而更容易坚持。<strong>错因提醒：</strong>误认为方法必须立刻见效，一旦没有马上好转就放弃，是很常见的误解。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "情绪会先给信号：身体、念头、行为", TTS["module-1"], f'''
        <p style="font-size:17px;margin:0 0 12px">在能说清「我现在很难受」之前，身上其实已经有了变化。先认出它们，比先讲道理有用。</p>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(251,191,36,.45)">
          <p style="margin:0"><strong>为什么要先学这个？</strong>你已经知道难受的时候要做点什么；但说不清难受在哪，就不知道从哪下手；所以先学会认信号。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>身体：</strong>肩膀紧、呼吸变浅、胃里发沉、手心出汗、睡不踏实。这些最早出现。</div></div>
          <div class="step"><span class="n">2</span><div><strong>念头：</strong>完了、来不及了、肯定不行、别人都在看我。念头跑得比事实快。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>行为：</strong>一遍遍刷手机、把书合上、谁都不想理、明明很累也不想睡。这一条最容易被自己看见。</div></div>
        </div>
        <div class="kid-note"><span class="emoji">💡</span><div><strong>三条线的说法：</strong>身体、念头、行为上的这些变化合起来，<strong>称为</strong>情绪信号。它们不是毛病，是身体在提醒你「现在有点吃力」。</div></div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">误认为这只是「想太多」，于是只劝自己别想了。可身体和行为那两条线还在，劝完往往还是动不了。先认信号，再动手。</p>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="情绪信号三条线的示意图：身体、念头、行为">
          <figcaption>同一个时刻的三条线：身体最先有反应，念头跟着变快，行为最后才看得见——认出任意一条，都是入口</figcaption>
        </figure>
{insight_box([
    {"lens": "看见它", "text": "你也许说不出自己是什么情绪，但你通常能说出「肩膀很紧」「不想回消息」——从这些具体的信号进去就好。"},
    {"lens": "解释它", "text": "为什么身体先有反应？因为它是自动的，不用你想。所以它常常比语言更早、也更诚实。"},
    {"lens": "迁移它", "text": "这条规律对身边的人也成立：同学突然话变少、一直趴着，可能不是不想理你，而是他正卡在某条线上。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "box", 5, "lab-1", "核心模拟：情绪调节工具箱", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先选一个你最近真的遇到过的情境，再从四件小事里挑一件。同一个情境可以把四件都试一遍，比一比。</p>
        <div class="lab-panel" id="box-stage">
          <div class="flex-row" style="flex-wrap:wrap">
            <button class="choice" data-box-scene="homework" style="text-align:center">作业今晚还差一大半</button>
            <button class="choice" data-box-scene="friend" style="text-align:center">和好朋友闹了别扭</button>
            <button class="choice" data-box-scene="result" style="text-align:center">准备了很久却没做好</button>
            <button class="choice" data-box-scene="pile" style="text-align:center">事情堆在一起</button>
          </div>
          <p class="result" id="box-scene" style="margin-top:12px"></p>
          <div class="slider-row" style="display:block">
            <div style="font-weight:700;font-size:14px">① 先让身体缓下来</div>
            <div class="flex-row" style="flex-wrap:wrap">
              <button class="choice" data-box-tool="breathe" style="text-align:center;font-size:13px">去走动、喝口水、把呼吸放慢</button>
            </div>
          </div>
          <div class="slider-row" style="display:block;margin-top:8px">
            <div style="font-weight:700;font-size:14px">② 换个角度看</div>
            <div class="flex-row" style="flex-wrap:wrap">
              <button class="choice" data-box-tool="reframe" style="text-align:center;font-size:13px">分成我能影响的和影响不了的</button>
            </div>
          </div>
          <div class="slider-row" style="display:block;margin-top:8px">
            <div style="font-weight:700;font-size:14px">③ 先做一件小事</div>
            <div class="flex-row" style="flex-wrap:wrap">
              <button class="choice" data-box-tool="tiny" style="text-align:center;font-size:13px">小到三分钟能做完</button>
            </div>
          </div>
          <div class="slider-row" style="display:block;margin-top:8px">
            <div style="font-weight:700;font-size:14px">④ 找人说说</div>
            <div class="flex-row" style="flex-wrap:wrap">
              <button class="choice" data-box-tool="talk" style="text-align:center;font-size:13px">找一个愿意听的人说三句</button>
            </div>
          </div>
          <p class="result warn" id="box-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧰</span><div><strong>四件都试完之后想一想：</strong>哪一件对你最省力？把它记住，比记住四件更有用。</div></div>
    ''', tag="核心模拟", bloom="apply"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "换个角度：把一件事分成两栏", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">四件小事里，这一件最值得练：分栏。它不改变已经发生的事，但能让你看清哪里还能动。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>我能影响的</strong></p>
            <p style="color:var(--muted)">下一次怎么准备、现在先做哪一块、要不要去问清楚、手机放哪儿。这一栏通常只剩一两件很具体的事。</p>
          </div>
          <div class="inner-card">
            <p><strong>我影响不了的</strong></p>
            <p style="color:var(--muted)">已经过去的分数、题目难不难、别人当时怎么想、别人的表情。这一栏不需要你去扛。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="两栏分栏示意图：左边是能影响的，右边是影响不了的">
          <figcaption>左边这一栏越具体越好，右边这一栏则可以直接放下——分清两栏，力气才不会用空</figcaption>
        </figure>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先认信号：</strong>身体、念头、行为，认出任意一条就可以开始。</div></div>
          <div class="step"><span class="n">2</span><div><strong>缓一缓：</strong>走动、喝水、把呼吸放慢，今晚不做重要决定。</div></div>
          <div class="step"><span class="n">3</span><div><strong>分两栏：</strong>能影响的留下，影响不了的放下。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>只做一件小事：</strong>小到三分钟能做完，做完了这一天就算数。</div></div>
        </div>
        <div class="kid-note"><span class="emoji">⚖️</span><div><strong>把期待放在合适的位置：</strong>这些方法不能让事情立刻变好，也不会让你从此不再难受。它们的用处是<strong>先让事情变得能处理</strong>。这句话请记住，它比方法本身更重要。</div></div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "view", 7, "lab-2", "对比台：同一件事，两种看法", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先选一个情境，再轮流点开两种看法，看看它们分别带来什么感受、下一步有没有变化。</p>
        <div class="lab-panel" id="view-stage">
          <div class="flex-row" style="flex-wrap:wrap">
            <button class="choice" data-view-scene="exam" style="text-align:center">一次没考好的试</button>
            <button class="choice" data-view-scene="match" style="text-align:center">一场比赛输了</button>
            <button class="choice" data-view-scene="team" style="text-align:center">小组里有人一直没做</button>
          </div>
          <p class="result" id="view-scene" style="margin-top:12px"></p>
          <div class="flex-row" style="flex-wrap:wrap">
            <button class="choice" data-view-way="fixed" style="text-align:center">盯着结果那一种</button>
            <button class="choice" data-view-way="fix" style="text-align:center">盯着能改的那一种</button>
          </div>
          <div class="grid grid-2" style="margin-top:12px">
            <div class="inner-card"><p><strong>盯着结果</strong></p><p id="view-fixed-txt" style="color:var(--muted)"></p></div>
            <div class="inner-card"><p><strong>盯着能改的</strong></p><p id="view-fix-txt" style="color:var(--muted)"></p></div>
          </div>
          <p class="result warn" id="view-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>三个情境都点一遍，你发现了什么？</strong>两种看法里的事实是同一件，差别只在注意力放在哪一栏。第二种也不是盲目乐观，它只是把下一步变得看得见。</div></div>
    ''', tag="动手实验室", bloom="analyze"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：一场没考好的试，五步走一遍", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(251,191,36,.45)">
          <p style="margin:0"><strong>情境：</strong>一场准备了很久的考试，结果比预期低了不少，你连着两三天都不太想说话。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先认信号：</strong>睡得比平时晚、白天没什么力气、别人一提这件事就想换话题。</div></div>
          <div class="step"><span class="n">2</span><div><strong>缓一缓：</strong>去操场走十分钟，今晚不做重要决定，先让身体松一点。</div></div>
          <div class="step"><span class="n">3</span><div><strong>分成两栏：</strong>能影响的是下次复习安排、错题处理、跟老师问清漏在哪；影响不了的是这次卷子的难度和已经出来的分数。</div></div>
          <div class="step"><span class="n">4</span><div><strong>只留一件小事：</strong>今晚把最想不通的那两道题折个角，明天先看它们。三分钟能做完的事，才叫下一步。</div></div>
          <div class="step"><span class="n green">5</span><div><strong>找人说说：</strong>说三句就够——结果不太好、我现在有点难受、我打算先做那一件小事。不必把整件事讲完。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">两个方向都容易走偏：一种是<strong>把影响不了的也扛在自己身上</strong>，比如反复想别人会怎么看，于是把力气用光；另一种是<strong>把什么都推给外部</strong>，于是能影响的那一栏空了，变成什么也做不了。分栏的目的，是让每一边都各归各位。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "关于「把一件事分成两栏」，下面哪种理解更合适？",
         "options": [("分栏就是把责任推给外部，让自己好受一点", False),
                     ("分清哪些能动手、哪些不用扛，再从能影响的那栏挑一件小事", True),
                     ("只要分好栏，事情就会好起来", False)],
         "explain": "分栏是让力气落在真的能动的地方，它不承诺结果。<strong>错因提醒：</strong>容易把「分栏」误认为「推卸责任」，也容易误认为只要分好栏就一定会好转，这两种理解都会让它失去作用。"},
        {"q": "情绪来的时候，下面哪一条信号通常出现得最早？",
         "options": [("身体上的变化，比如肩膀紧、呼吸变浅", True),
                     ("能准确说出自己是什么情绪", False),
                     ("想清楚该怎么处理这件事", False)],
         "explain": "身体反应是自动的，往往比说得出情绪更早。先抓住它，就有入口。<strong>错因提醒：</strong>常见错误是把这些变化当成想太多，于是忽略了最早就出现的线索。"},
        {"q": "「我要把这次落下的全部补回来，一天也不能再拖」——这句话的问题主要在哪？",
         "options": [("范围太大、没有起点，往往一天都动不了", True),
                     ("态度不够积极", False),
                     ("不应该补，过去就算了", False)],
         "explain": "决心大不等于做得到。把范围缩到三分钟能完成的一件小事，才有真正的开始。<strong>错因提醒：</strong>误认为计划越严越有用，结果常常是第二天就散了。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "pile", 10, "synthesis", "综合任务：这张说法，放进哪一栏？", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">八张说法卡，每一张选一栏。选完会给出解释，也留意一下自己在哪一栏停留得更久。</p>
        <div class="lab-panel" id="pile-stage">
          <div id="pile-cards"></div>
          <p class="result warn" id="pile-out" style="margin-top:12px;display:none"></p>
        </div>
        <div class="inner-card">
          <p><strong>写下来，留给自己：</strong></p>
          <p style="color:var(--muted)">在你刚刚分好的「我能影响的」那一栏里，挑一件明天就能做完的小事，写清它做完的样子。</p>
          <textarea id="syn-answer" rows="3" placeholder="我明天要做的这件小事是……做完的样子是……" style="margin-top:8px"></textarea>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🤝</span><div><strong>还有一件事想告诉你：</strong>如果一种状态持续了很久，已经影响到吃饭、睡觉或者上课，别一个人扛着——找家长、班主任或者心理健康老师说一说，是照顾自己的方式，和「自己想办法」并不冲突。</div></div>
    ''', tag="综合任务", bloom="evaluate"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，看看方法还在不在", TTS["posttest"], [
        {"q": "比赛前一天，你突然很紧，反复想着万一发挥不好。这时比较合适的第一步是：",
         "options": [("先把身体缓下来，早点休息，今晚不再加练", True),
                     ("反复在脑子里演练失误的画面，提醒自己别出错", False),
                     ("告诉自己别紧张，然后继续硬撑", False)],
         "explain": "先让身体松一点，比反复提醒自己更有用；反复演练失误画面会让信号更强。"},
        {"q": "和同学的关系出了点问题，你已经两天没睡好。比较好的做法是：",
         "options": [("把能影响的部分看清楚，比如要不要先开口、怎么说", True),
                     ("一直想对方到底怎么看你，想明白再说", False),
                     ("当作没事发生，谁也不提", False)],
         "explain": "对方的想法属于影响不了的那一栏，反复想它带不来下一步。<strong>错因提醒：</strong>容易把「想清楚对方怎么想」误认为解决问题的前提，其实它常常只是消耗。"},
        {"q": "小组合作里有个同学一直没完成他那部分，你打算怎么做？",
         "options": [("说清时间和他的那部分，同时留一个可以商量的空间", True),
                     ("在心里认定他就是不靠谱，以后不跟他一组", False),
                     ("自己全部做完，再也不提这件事", False)],
         "explain": "能影响的那一栏里有说清事实、给出时间、提出请求，甚至有向老师说明情况。先开口不等于一定成，但不开口就一定没有变化。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把自己讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>先认信号</strong>：身体、念头、行为三条线上，认出任意一条都是入口。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>分成两栏</strong>：能影响的留下，影响不了的放下，再从左边挑一件小事。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>把期待放准</strong>：这些方法不保证立刻变好，它们先让事情变得能处理。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(251,191,36,.45)">
          <p style="margin:0"><strong>回到开头那种时刻：</strong>事情堆在一起、什么都不想开始的时候，你不必先把状态调整到最好。先认一个信号，缓一缓，分两栏，然后做一件三分钟的小事。做完，今天就算数。</p>
        </div>
        <div class="inner-card">
          <p><strong>四步口诀，帮你记住：</strong>先缓一缓，分成两栏，做件小事，找人说说。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「信号、两栏、一件小事」这三个词，说说你上周某一次难受的时候，本来可以怎么走。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "写下你紧张时的三个身体信号，越具体越好，比如肩膀、呼吸、睡眠。",
            "写出「我能影响的」和「我影响不了的」两栏各自的含义，各用一句话说明。",
        ],
        [
            "找一件最近让你不太舒服的事，分成两栏写下来，再从能影响的那栏里挑一件明天能做完的小事。",
            "在情绪调节工具箱里选一个情境，把四件小事各试一遍，写出对你最省力的那一件和原因。",
        ],
        [
            "连续七天记录一次情绪信号和当时的应对方式，一周后回看，找出最管用的那一件并写下来。",
            "把四步口诀讲给一位同学听，再用他的一件真事一起分一次栏，注意只从左边那栏挑一件小事。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "psych-h-g11-emotion-resilience",
    "node_id": "psych-h-g11-emotion-resilience",
    "subject": "psychology",
    "subject_cn": "心理健康",
    "stage": "high",
    "stage_cn": "高中",
    "curriculum": "中小学心理健康教育指导纲要（2012年修订）/ 教育部相关要求 · 高中",
    "title": "情绪管理与抗挫力：给自己一个能用的工具箱",
    "name_en": "Emotion Regulation and Resilience",
    "grade": 11,
    "grade_cn": "高二",
    "domain": "emotion-regulation",
    "domain_cn": "情绪调适",
    "lesson_type": "workshop",
    "version": "1.0.0",
    "description": "面向高二学生的情绪调适与抗挫课：先从身体、念头、行为三条线认出情绪信号，再用核心模拟「情绪调节工具箱」——选一个真实情境，再从四件做得到的小事里挑一件，看它可能把事情带到哪里；重点练习「分成两栏」，把一件不如意的事分成我能影响的和影响不了的，只从能影响的那一栏挑一件小事；最后用八张说法卡做归因分栏练习。全课明确写出这些方法不保证立刻变好、只先让事情变得能处理，语气温和、不评判、不贴标签，不做情绪放大，不出现任何诊断性表述。",
    "tags": ["情绪信号", "情绪调节工具箱", "分成两栏", "抗挫力", "高二"],
    "standard_ref": "《中小学心理健康教育指导纲要（2012年修订）· 高中》情绪调适——进一步提高承受失败和应对挫折的能力，形成良好的意志品质；学会恰当地、正确地体验情绪和表达情绪。",
    "hero_question": "状态不好的时候，除了硬撑，还能做点什么？",
    "hero_alt": "情绪管理与抗挫力知识结构图三栏：情绪的三条信号线、情绪调节工具箱、分成两栏看",
    "hero_caption": "情绪管理与抗挫力：先认信号 · 工具箱四件小事 · 分成两栏，只做一件小事",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个最贴近你最近状态的困惑，后面的内容都会围着它展开。",
    "anchor_choices": [
        {"t": "难受的时候身上到底发生了什么？", "d": "说不清是什么情绪，只知道整个人不对劲", "v": "难受的时候身上到底发生了什么"},
        {"t": "那一刻我具体能做什么？", "d": "知道要调整，但不知道从哪下手", "v": "那一刻我具体能做什么"},
        {"t": "事情没做好之后，我该怎么看它？", "d": "一失败就想否定自己，越想越动不了", "v": "事情没做好之后我该怎么看它"},
        {"t": "为什么定了计划总是坚持不下去？", "d": "每次开头都很用力，几天就散了", "v": "为什么定了计划总是坚持不下去"},
    ],
    "objectives": [
        "能说出情绪来的时候，身体、念头、行为三条线上分别有什么信号，并写下自己的具体表现",
        "会用情绪调节工具箱，为当下的情境挑出一件做得到的小事，并说明为什么挑它",
        "能把一件不如意的事分成「我能影响的」和「我影响不了的」两栏，只从能影响的一栏挑一件小事",
        "能说清这些方法能做什么、不能做什么，不把它们当成必须立刻见效的承诺",
    ],
    "objectives_plain": [
        "能说出情绪来的时候，身体、念头、行为三条线上分别有什么信号，并写下自己的具体表现",
        "会用情绪调节工具箱，为当下的情境挑出一件做得到的小事，并说明为什么挑它",
        "能把一件不如意的事分成「我能影响的」和「我影响不了的」两栏，只从能影响的一栏挑一件小事",
        "能说清这些方法能做什么、不能做什么，不把它们当成必须立刻见效的承诺",
    ],
    "standards": [
        {"content": "进一步提高承受失败和应对挫折的能力，形成良好的意志品质",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》高中 · 情绪调适"},
        {"content": "学会恰当地、正确地体验情绪和表达情绪",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》高中 · 情绪调适"},
    ],
    "prereqs": ["psych-h-g10-relationship"],
    "prereqs_name": "人际关系与沟通",
    "prereqs_meta": "psych-h-g10-relationship",
    "leads_to": ["psych-h-g11-exam-wellness"],
    "next_meta": "psych-h-g11-exam-wellness",
    "section_images": ["assets/psych-h-g11-emotion-resilience-fig1.webp", "assets/psych-h-g11-emotion-resilience-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "除了硬撑，还能做点什么——这个问题先放在心里往下看。",
        "problem-anchor": "先定一个小目标：这节课结束时，你手上有四件做得到的小事。",
        "objectives": "看清四件事：认信号、用工具箱、分成两栏、把期待放准。",
        "pretest": "凭平时的习惯选就好，不打分。前测只是帮你看清自己现在的应对方式。",
        "module-1": "身体、念头、行为三条线，认出任意一条都是入口。",
        "lab-1": "一个情境可以把四件小事都试一遍，找对你最省力的那一件。",
        "module-2": "能影响的留下，影响不了的放下；只从左边挑一件小事。",
        "lab-2": "同一件事两种看法，比较感受和下一步的变化。",
        "worked-example": "五步：认信号、缓一缓、分两栏、留一件小事、找人说说。",
        "conceptest-1": "三个选项里藏着最常见的几个误解，选完请把每条解释读一遍。",
        "synthesis": "八张说法卡各选一栏，全部点完会看到一段小结。",
        "posttest": "比赛前、关系里、小组合作，三个新情境看看方法还在不在。",
        "summary": "记住四步口诀：先缓一缓，分成两栏，做件小事，找人说说。",
        "homework": "三层练习，前两层做完就算通关，第三层留给愿意更进一步的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先帮你找到卡点，再给一个最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是高中「情绪调适」板块里长期空缺的一课。设计上不讲大道理，只准备一个能当场打开的工具箱。核心模拟是「情绪调节工具箱」——四个真实情境（作业赶不完、和朋友闹别扭、准备了很久却没做好、事情堆在一起）各配四件做得到的小事（先让身体缓下来、换个角度看、先做一件小事、找人说说），学生自己轮换比较，看每种组合可能把事情带到哪里；第二个台子把同一件事的两种看法并排摆开，比较感受与下一步的变化。最要紧的动作是「分成两栏」，把不如意的事分成我能影响的和影响不了的，只在能影响的那一栏里挑一件三分钟能做完的小事；综合任务用八张说法卡做归因分栏练习。全课明确写出这些方法不保证立刻变好、只先让事情变得能处理，不放大情绪，语气温和、不评判、不贴标签。",
    "plan_table": """| 1 | cover | 情绪管理与抗挫力：给自己一个能用的工具箱 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：状态不好的时候，你习惯怎么办？ | 起·前测（暴露现有习惯） |
| 5 | concept | 情绪会先给信号：身体、念头、行为 | 承·概念一（三条信号线） |
| 6 | interactive | 核心模拟：情绪调节工具箱 | 承·核心模拟（情境 × 四件小事 → 可能的走向） |
| 7 | concept | 换个角度：把一件事分成两栏 | 承·概念二（能影响 / 影响不了 + 四步） |
| 8 | interactive | 对比台：同一件事，两种看法 | 承·练习台（结果视角 / 能改视角） |
| 9 | concept | 例题示范：一场没考好的试，五步走一遍 | 转·重难点突破（五步示范 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：这张说法，放进哪一栏？ | 合·归因分栏（迁移应用） |
| 12 | quiz | 后测：换几个新情境，看看方法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把自己讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：情绪的三条信号线、情绪调节工具箱、分成两栏 三栏\n- P5 三条信号线示意图（已生成）：身体、念头、行为三个抽象方块与箭头\n- P7 两栏分栏示意图（已生成）：左边我能影响的、右边我影响不了的\n- 若需补充：一张可打印的情绪信号记录卡、一张两栏分栏空白工作表",
}
