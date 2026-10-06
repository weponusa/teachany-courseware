# -*- coding: utf-8 -*-
"""小学心理健康 · 学习自信与情绪表达（G4）—— 补齐知识树「学习辅导」空缺

学科语气（心理健康）：温和、不评判、不贴标签；只讲可操作的表达办法，不涉及伤害性情节。
四年级落点：把「我不会」改写成「我还没学会……，我下一步可以……」的表达练习（学习自信），
再用情绪温度计先量一量、再说出来（情绪表达），最后分清考砸之后哪些表达方式对自己更有帮助。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/psych-e-g4-study-motivation-fig1.webp'
F2 = './assets/psych-e-g4-study-motivation-fig2.webp'

TTS = {
    "hero": "小朋友，先想一想：作业本上有一道题，你看了两遍还是不会，心里那句话是不是立刻就冒出来了——我不会。这句话说出来以后，笔就放在那里不想动了。这节课我们做两件事。第一件，把「我不会」换一个说法，变成「我还没学会」，并且在后面加一个下一步。第二件，学会用一根情绪温度计，量一量自己这会儿有多难受，再把它说出来。你会发现，话换一种说法，路就多出一条。",
    "problem-anchor": "开始之前，先选一个你最想知道的事。是想知道一句「我不会」和一句「我还没学会」到底差在哪里，还是心里难受的时候怎么知道自己到了几分，或者你最想问的是，考砸了可以说哪些话、哪一种对自己更有帮助，再或者你想弄清楚，怎么做才能真的学会，而不是一直觉得自己不行。选好了，就带着它往下看。",
    "objectives": "这节课有四个小目标。第一，能说出「我不会」和「我还没学会」在说法上的不同，知道差别就在后面有没有一个下一步。第二，能把三句「我不会」改写成「我还没学会」，并补上自己的下一步。第三，能用情绪温度计找到自己现在的温度，再用一句话把感受说出来。第四，能分辨考砸以后不同的表达方式，说出哪一种对自己更有帮助。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先说第一件事。「我不会」这三个字，说的是现在，也是一句结论，像一扇门被关上了，说完就不想再动笔。「我还没学会」不一样，它也说的是现在，但它后面留着一扇门，所以它一定还会跟着一个下一步。我们可以用这样一个句子：我还没学会哪一件事，因为我还没弄懂或者还没练够，我下一步可以做什么。请你留意，这里要挑的是说法，不是人。说自己还没学会，一点也不丢脸，那只是一句实话。",
    "lab-1": "现在请你当一次说法小改手。下面有五个句子，都是我们心里常冒出来的「我不会」。点开一句，你会看到三种改写，选一个更像成长说法的。选得不太合适也不会说你错，我会告诉你这样可能会发生什么，还可以试试什么。最后还有一个空格，请你写下自己的那一句。",
    "module-2": "第二件事：心里难受的时候怎么办。我们可以给自己画一根情绪温度计，从零到十。零是很平稳，十是快满出来了。温度不是好坏，它只是一个信号，告诉你现在需要什么。温度低的时候，你可以安安静静地做完手头的事；温度升到五六分，先做三次慢慢的呼吸，喝几口水；到了七八分，就找一个人说几句话，或者把心里的事写下来。量完温度，再说一句话，别人就知道怎么帮你了。",
    "lab-2": "现在请你用一次情绪温度计。拖动下面的滑块，或者点一个温度按钮，找到最像你现在的那个数。我会告诉你这个温度常常是什么样子，还有一句你可以说出来的话，和一个马上能做的小办法。",
    "worked-example": "我们一起帮小满想一想。数学卷子发下来，比上次退步了不少，小满心里一下凉了。第一步，量一量温度：差不多八分，挺难受的。第二步，把感受说出来：我现在很失望，因为我很想考好。第三步，把那句「我不会」改一改：我不是不会，我是这几道应用题还没弄懂。第四步，定一个下一步：今天把三道错题抄到错题本上，明天课间去问老师。四步走完，卷子还是那张卷子，可小满知道下一步做什么了。",
    "conceptest-1": "接下来用三个说法考考你，每一个里面都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件事交给你。下面有六张卡片，都是考砸以后可能出现的心思和做法，请你把它们分成两栏：哪些对自己更有帮助，哪些帮助不大。分完以后，再写出你自己最想说的那一句。",
    "posttest": "最后一轮，换三个新的小情境来考考你。这次会出现上课答错了被同学笑、背课文背了五遍还背不下来、还有好朋友考得比我好，看看你能不能用上今天的办法。",
    "summary": "这节课我们记住三句话。第一句，「我不会」是一句结论，「我还没学会」后面还留着一个下一步。第二句，难受的时候先用情绪温度计量一量，再用一句话把感受说出来。第三句，考砸了以后，说出感受加上说出下一步，是对自己最有帮助的一种说法。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：把三句「我不会」改写成「我还没学会」，每一句后面补上自己的下一步。第二层能力应用，动手做：做一张情绪温度计贴在书桌前，标出三个温度，各写一个你能做到的小办法。第三层迁移挑战，选做：这一周里，挑一次你觉得有点难的学习任务，记下当时的温度，和用完之后的效果，写三句话。",
    "knowledge-graph": "这张图展示了这节课在心理健康知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 我不会，还是我还没学会", "lab-1": "动手一 说法小改手",
    "module-2": "概念二 情绪温度计：先量一量，再说出来", "lab-2": "动手二 量一量我的情绪温度",
    "worked-example": "例题讲解 小满的卷子", "conceptest-1": "概念测试",
    "synthesis": "综合任务 考砸了，哪种说法更有帮助", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：「我不会」→「我还没学会……」改写练习 ──
REWRITES = [
    {
        "id": "r1",
        "t": "我不会写看图作文。",
        "opts": [
            {"k": "a", "t": "我还没学会把图上的事连成一段话。我下一步先照着课文的一句话，把图里的人、地方、做什么各写一个词，再连起来。", "ok": True,
             "fb": "这句里既有「还没」，也有一个今天就能动手的小步骤。说完这句话，笔就动起来了。"},
            {"k": "b", "t": "我永远都学不会写作文，怎么写都比别人差。", "ok": False,
             "fb": "这样可能会让笔一直放在那里，明天还是同一句「我不会」。还可以试试：把「永远」换成「还没」，再说出第一步——先照着课文写三个词。"},
            {"k": "c", "t": "我大概没有写作文的天分吧。", "ok": False,
             "fb": "这样可能会让你跳过练习，直接给自己一个结论。还可以试试：把话说回具体的事上——「我还没学会把事情连成一段话」，然后写下第一步。"},
        ],
    },
    {
        "id": "r2",
        "t": "我不会做这种应用题。",
        "opts": [
            {"k": "a", "t": "我还没学会这类题。我下一步先把题目里的条件画出来，再问问老师我卡在哪一步。", "ok": True,
             "fb": "「还没学会」后面跟着一个具体动作，这就是它和「我不会」最大的不同。"},
            {"k": "b", "t": "我就是数学不行，做多少题都没用。", "ok": False,
             "fb": "这样可能会让你连题目都不想读第二遍。还可以试试：先只做一件事——把条件画出来，看看卡在哪一步。"},
            {"k": "c", "t": "我不会，那就空着，等老师讲。", "ok": False,
             "fb": "等老师讲也是一种办法，可是你错过了自己找出卡点的机会。还可以试试：先画一画条件，把不懂的那一步圈出来，明天带着圈去问。"},
        ],
    },
    {
        "id": "r3",
        "t": "我不会在大家面前发言。",
        "opts": [
            {"k": "a", "t": "我还没学会在大家面前发言。我下一步先在家里对着镜子说一遍，再说给同桌一个人听。", "ok": True,
             "fb": "把一件大事拆成两级小台阶——先对着镜子，再说给一个人听。台阶小一点，才迈得上去。"},
            {"k": "b", "t": "我天生就胆小，改不了了。", "ok": False,
             "fb": "这样可能会把一次没做到，变成一辈子做不到。还可以试试：把「天生」换成「还没」——「我还没练过，我先说给同桌一个人听」。"},
            {"k": "c", "t": "我以后都不要举手了，就不会出错。", "ok": False,
             "fb": "这样可能会让你少了很多练习的机会。还可以试试：先挑一个你最有把握的问题举手，只举这一次。"},
        ],
    },
    {
        "id": "r4",
        "t": "我不会背这篇课文。",
        "opts": [
            {"k": "a", "t": "我还没背下来。我下一步先分成三段，每段读五遍再合起来背。", "ok": True,
             "fb": "把「不会背」变成「分成三段」——这就是把大困难改成能动手的小步骤。"},
            {"k": "b", "t": "我记性太差了，背什么都没用。", "ok": False,
             "fb": "这样可能会让你还没开始就放弃。还可以试试：不整篇背，先只背第一段，看看到底需要几遍。"},
            {"k": "c", "t": "我不会背，明天再说吧。", "ok": False,
             "fb": "这样可能会让这件事一直往后拖，心里也一直挂着一件事。还可以试试：今天就只读第一段三遍，算作开始。"},
        ],
    },
    {
        "id": "r5",
        "t": "我不会画立方体。",
        "opts": [
            {"k": "a", "t": "我还没学会画立方体。我下一步先照着课本描两个，再自己画一个。", "ok": True,
             "fb": "从描两个开始，是最好的第一步。学会一件事，常常就是从模仿开始的。"},
            {"k": "b", "t": "别人随手一画就很像，我肯定学不会。", "ok": False,
             "fb": "别人画得像，多半是因为他画过很多次，不是因为他天生会。这样可能会让你直接放弃，还可以试试：先描两个，再自己画一个。"},
            {"k": "c", "t": "我画不好，那就干脆不画了。", "ok": False,
             "fb": "这样可能会让你错过一个本来能学会的技能。还可以试试：把目标改小——只画一个，画得歪也没关系。"},
        ],
    },
]

# ── 动手二：情绪温度计（0—10，四个温度带 + 一句话 + 一个小办法） ──
TEMP_BANDS = [
    {"max": 2, "name": "很平稳", "desc": "心里很安静，能专心做完手头的事。",
     "say": "「我现在挺平静的，想把这一页先做完。」",
     "tip": "这个温度很适合做需要动脑的事；趁现在把最难的题先做掉。"},
    {"max": 4, "name": "有一点起伏", "desc": "有点紧张，也有点想做好，肚子里像有只小蝴蝶。",
     "say": "「我有点紧张，我想先做三次慢慢的呼吸。」",
     "tip": "紧张说明你在意这件事。做三次慢慢的呼吸，就能把这点劲儿用在题目上。"},
    {"max": 6, "name": "心里不太舒服", "desc": "有点闷，有点烦，看书上的字有点看不进去。",
     "say": "「我心里有点闷，我想先坐一会儿，再回来写。」",
     "tip": "先喝几口水，站起来走一走，让身体先松下来；一分钟后回来，只做一道题。"},
    {"max": 8, "name": "挺难受的", "desc": "胸口沉沉地，很想找个地方待着，什么都不想做。",
     "say": "「我现在很难过，也有点失望，我想找人说三分钟。」",
     "tip": "找一个人说三分钟，或者拿一张纸把心里的事写下来。写的时候不用讲道理，写清楚就行。"},
    {"max": 10, "name": "难受得快满出来了", "desc": "鼻子发酸，心里像被塞满了，一个人待着会更难受。",
     "say": "「我现在很难受，我需要有人陪我待一会儿。」",
     "tip": "先离开那个让你难受的地方，去找一个大人待在一起。开口说这句话本身，就会让你松一点。"},
]

TEMP_FEELINGS = ["失望", "着急", "生气", "担心", "委屈", "有点累", "平静"]

# ── 综合任务：考砸了，哪些说法对自己更有帮助（两栏分类） ──
EXPR_ITEMS = [
    {"id": "e1", "bin": "good", "t": "「我现在很失望，因为我很想考好。」",
     "fb": "这句话既说出了感受，也没有给自己下结论。说出来之后，别人知道该怎么陪你了。"},
    {"id": "e2", "bin": "good", "t": "「我想看看错在哪里，下次先检查计算。」",
     "fb": "这句把注意力放在了下一步。分数是结果，错题才是可以动手的地方。"},
    {"id": "e3", "bin": "good", "t": "「我有点难过，想一个人坐五分钟，再来找你商量。」",
     "fb": "先说出感受，再说出你需要什么，还给了自己一个时间。这是很有力量的一种表达。"},
    {"id": "e4", "bin": "less", "t": "「我完了，我永远都考不好。」",
     "fb": "这是一句结论，说完整个人就动不了了。还可以试试：把「永远」换成「这次」——「我这次没考好」。"},
    {"id": "e5", "bin": "less", "t": "把卷子揉成一团塞进抽屉，不想看。",
     "fb": "这样可能会让卷子里的错题一直没被弄懂，下次还是同样的地方丢分。还可以试试：先放十分钟，再把它摊开，只挑一道错题看看。"},
    {"id": "e6", "bin": "less", "t": "冲妈妈大声说：「都怪你昨天没帮我检查！」",
     "fb": "这样可能会让家里人也很难受，事情还是没解决。还可以试试：说出自己的感受——「我现在很失望，我想和你一起看看错在哪里。」"},
]

EXPR_BINS = [
    {"id": "good", "name": "① 对自己更有帮助"},
    {"id": "less", "name": "② 帮助不大"},
]

CUSTOM_JS = r"""
/* ============================================================
   psych-e-g4-study-motivation 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 说法小改手：「我不会」→「我还没学会……，我下一步可以……」
   3) 情绪温度计：滑块 / 温度按钮 → 四档描述 + 一句可以说的话 + 一个小办法
   4) 考砸了的表达方式：六张卡片 → 两栏分类
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

  /* ---------- 2. 说法小改手 ---------- */
  var RW = __RW_JSON__;
  var rwStage = document.getElementById('rw-stage');
  if (rwStage) {
    var curR = null, doneR = {};
    var outR = document.getElementById('rw-out');
    var scoreR = document.getElementById('rw-score');

    function rwById(id) {
      for (var i = 0; i < RW.length; i++) { if (RW[i].id === id) return RW[i]; }
      return null;
    }
    function renderR() {
      document.querySelectorAll('[data-rw]').forEach(function (b) {
        var k = b.dataset.rw;
        b.classList.toggle('selected', k === curR);
        b.classList.toggle('done', !!doneR[k]);
      });
      scoreR.textContent = '已经改写 ' + Object.keys(doneR).length + ' / ' + RW.length + ' 句';
    }
    function paintR() {
      var box = document.getElementById('rw-opts');
      box.innerHTML = '';
      if (!curR) return;
      var S = rwById(curR);
      if (!S) return;
      S.opts.forEach(function (o) {
        var b = document.createElement('button');
        b.className = 'choice' + (doneR[curR] && o.ok ? ' correct' : '');
        b.style.textAlign = 'left';
        b.textContent = o.t;
        b.addEventListener('click', function () {
          if (doneR[curR]) return;
          if (o.ok) {
            doneR[curR] = true;
            outR.className = 'result';
            outR.innerHTML = '<strong>这一句改写得好。</strong>' + o.fb;
          } else {
            outR.className = 'result warn';
            outR.innerHTML = '<strong>这句话很多人心里都冒出来过，我们看看它会带来什么。</strong>' + o.fb;
          }
          renderR();
          paintR();
        });
        box.appendChild(b);
      });
    }
    document.querySelectorAll('[data-rw]').forEach(function (b) {
      b.addEventListener('click', function () {
        curR = b.dataset.rw;
        var S = rwById(curR);
        if (doneR[curR]) {
          outR.className = 'result';
          outR.innerHTML = '<strong>这一句已经改写过了。</strong>记住那个句式：我还没学会（什么），我下一步可以（做什么）。';
        } else {
          outR.className = 'result warn';
          outR.innerHTML = '<strong>心里冒出来的是：「' + S.t + '」</strong><br>下面有三种改写，选一个更像成长说法的试试。';
        }
        renderR();
        paintR();
      });
    });
    renderR();
  }

  /* ---------- 3. 情绪温度计 ---------- */
  var BANDS = __BANDS_JSON__;
  var slider = document.getElementById('thermo');
  if (slider && BANDS.length) {
    var labelEl = document.getElementById('thermo-band');
    var numEl = document.getElementById('thermo-num');
    var fillEl = document.getElementById('thermo-fill');
    var outT = document.getElementById('thermo-out');
    var chosenFeeling = '';

    function bandOf(v) {
      for (var i = 0; i < BANDS.length; i++) { if (v <= BANDS[i].max) return BANDS[i]; }
      return BANDS[BANDS.length - 1];
    }
    function renderT() {
      var v = parseInt(slider.value, 10);
      var B = bandOf(v);
      numEl.textContent = v + ' 度';
      labelEl.textContent = B.name;
      fillEl.style.width = (v * 10) + '%';
      var feelLine = chosenFeeling ? '心里的名字：' + chosenFeeling + '。' : '';
      outT.className = (v >= 7 ? 'result warn' : 'result');
      outT.innerHTML = '<strong>' + v + ' 度 · ' + B.name + '：</strong>' + B.desc + '<br>' +
        feelLine + '<strong>可以说出来的一句话：</strong>' + B.say + '<br>' +
        '<strong>马上能做的一个小办法：</strong>' + B.tip;
    }
    slider.addEventListener('input', renderT);
    slider.addEventListener('change', renderT);
    document.querySelectorAll('[data-temp]').forEach(function (b) {
      b.addEventListener('click', function () {
        slider.value = b.dataset.temp;
        renderT();
      });
    });
    document.querySelectorAll('[data-feel]').forEach(function (b) {
      b.addEventListener('click', function () {
        chosenFeeling = b.dataset.feel;
        document.querySelectorAll('[data-feel]').forEach(function (x) {
          x.classList.toggle('selected', x === b);
        });
        renderT();
      });
    });
    renderT();
  }

  /* ---------- 4. 考砸了的表达方式（两栏分类） ---------- */
  var ITEMS = __EXPR_JSON__;
  var BINS = __EXPRBINS_JSON__;
  var bank2 = document.getElementById('expr-bank');
  if (bank2 && ITEMS.length) {
    var placed2 = {}, picked2 = null;
    var out4 = document.getElementById('expr-out');
    var score4 = document.getElementById('expr-score');

    function itemById(id) {
      for (var i = 0; i < ITEMS.length; i++) { if (ITEMS[i].id === id) return ITEMS[i]; }
      return null;
    }
    function binName(id) {
      for (var i = 0; i < BINS.length; i++) { if (BINS[i].id === id) return BINS[i].name.replace(/^[①②]\s*/, ''); }
      return '';
    }
    ITEMS.forEach(function (it) {
      var b = document.createElement('button');
      b.className = 'sort-item';
      b.dataset.pick2 = it.id;
      b.textContent = it.t;
      b.addEventListener('click', function () {
        if (placed2[it.id]) return;
        picked2 = it.id;
        document.querySelectorAll('[data-pick2]').forEach(function (x) {
          x.classList.toggle('selected', x.dataset.pick2 === picked2);
        });
        out4.className = 'result warn';
        out4.innerHTML = '<strong>你选中了这一张：</strong>' + it.t + '<br>它应该放进哪一栏？点一下上面的栏试试。';
      });
      bank2.appendChild(b);
    });
    BINS.forEach(function (bn) {
      var box = document.getElementById('expr-bin-' + bn.id);
      if (!box) return;
      box.addEventListener('click', function () {
        if (!picked2) {
          out4.className = 'result warn';
          out4.textContent = '先在左边点一张卡片，再点这一栏。';
          return;
        }
        var it = itemById(picked2);
        if (!it || placed2[it.id]) return;
        placed2[it.id] = true;
        var right = (it.bin === bn.id);
        var card = document.querySelector('[data-pick2="' + it.id + '"]');
        if (card) { card.classList.add('done'); card.classList.remove('selected'); }
        var tag = document.createElement('span');
        tag.className = 'tag';
        tag.style.borderColor = right ? 'rgba(78,205,196,.9)' : 'rgba(239,68,68,.7)';
        tag.textContent = it.t;
        box.querySelector('.bin-list').appendChild(tag);
        box.classList.toggle('ok', right);
        box.classList.toggle('no', !right);
        picked2 = null;
        var n = Object.keys(placed2).length;
        score4.textContent = '已经分好 ' + n + ' / ' + ITEMS.length + ' 张';
        if (right) {
          out4.className = 'result';
          out4.innerHTML = '<strong>分对了。</strong>' + it.fb;
        } else {
          out4.className = 'result warn';
          out4.innerHTML = '<strong>它更合适放在「' + binName(it.bin) + '」那一栏。</strong>' + it.fb;
        }
        if (n === ITEMS.length) {
          out4.className = 'result';
          out4.innerHTML = '<strong>六张卡片都分好了。</strong>对自己更有帮助的说法有一个共同点：<strong>先说感受，再说下一步</strong>。记住这个共同点，下次不用背句子，自己就能说出来。';
        }
      });
    });
    score4.textContent = '已经分好 0 / ' + ITEMS.length + ' 张';
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__RW_JSON__', json.dumps(REWRITES, ensure_ascii=False))
             .replace('__BANDS_JSON__', json.dumps(TEMP_BANDS, ensure_ascii=False))
             .replace('__EXPR_JSON__', json.dumps(EXPR_ITEMS, ensure_ascii=False))
             .replace('__EXPRBINS_JSON__', json.dumps(EXPR_BINS, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "下面哪句话更像「成长的」说法？",
         "options": [("这道题我还没学会，我下一步先把条件画出来", True),
                     ("我就是数学不行，做多少都没用", False),
                     ("我不会，那就空着等老师讲", False)],
         "explain": "「还没学会」说的是现在，「我下一步可以……」跟着一个能动手的小步骤，路就留着了。"
                    "<strong>错因提醒：</strong>常见错误是把「这一次没做到」误认为「我这个人不行」——要挑的是说法，不是人。"},
        {"q": "考试退步了，心里很难受。下面哪个做法更合适？",
         "options": [("先量一量自己的温度，再用一句话把感受说出来", True),
                     ("把卷子揉成一团，再也不看", False),
                     ("大声说都怪别人，然后一整天不说话", False)],
         "explain": "先量温度，是让自己先看清楚现在有多难受；说出来，别人才知道怎么帮你。"
                    "<strong>错因提醒：</strong>有人误认为「不看卷子就不难受了」——难受会过去，可错题还在那里，下次还会在同一个地方丢分。"},
        {"q": "「我还没学会在大家面前发言」这句话后面，最适合补上哪一句？",
         "options": [("我下一步先在家里对着镜子说一遍，再说给同桌一个人听", True),
                     ("所以我以后都不举手了", False),
                     ("反正别人天生就比我胆大", False)],
         "explain": "「还没学会」后面一定跟着一个下一步，而且这一步要小到你今天就能做。"
                    "<strong>错因提醒：</strong>最容易搞混的是把「还没」当成抱怨的借口——成长的说法后面一定有一个动作，没有动作的句子，还停在原地。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "「我不会」还是「我还没学会」，差的是下一步", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们已经学过怎么给心里的感觉起名字，也知道了难受的时候可以说出来（And）；可是学习上一遇到难题，心里那句「我不会」来得特别快，话说出来之后，笔就放下了，人也跟着停住（But）；所以这节课先学一件很小、很有用的事——把这句话换一个说法（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">「我不会」和「我还没学会」，说的都是现在，差别在<strong>后面有没有一个下一步</strong>。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>「我不会」像一扇关上的门</strong></p>
            <p style="color:var(--muted)">它是一句结论，说完就停住了。门关上以后，连试一次的念头都没有了。</p>
          </div>
          <div class="inner-card">
            <p><strong>「我还没学会」留着一扇门</strong></p>
            <p style="color:var(--muted)">它说的是现在，却没有把以后说死，所以它后面一定还会跟着一个动作。</p>
          </div>
        </div>
        <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(78,205,196,.45)">
          <p><strong>可以照着说的句式：</strong></p>
          <p style="color:var(--muted)">我还没学会（<strong>哪一件事</strong>），因为我（还没弄懂 / 还没练够），我下一步可以（<strong>一个今天就能做的小动作</strong>）。</p>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="我不会改写成我还没学会的句式示意图，附中文标注">
          <figcaption>示意图：把「我不会」改写成「我还没学会……，我下一步可以……」（教学示意图，人物为中性简洁插画）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「说自己还没学会，是在给自己找借口」。这里最容易<strong>搞混</strong>的是两种句子的落脚点：找借口的句子停在原地，说完还是不动；成长的说法后面一定跟着一个具体的下一步。判断的办法很简单——<strong>这句话后面有没有一个动作？</strong>有动作，就不是借口。</p>
        </div>
{insight_box([
    {"lens": "拆开它", "text": "一句话拆开看是两段：前一段说我现在在哪里，后一段说我要往哪里走。缺了后一段，它就从一句话变成了一堵墙。"},
    {"lens": "比较它", "text": "「我永远都学不会」和「我这次还没学会」——两句话里，只有一个留着明天。换个词，明天就回来了。"},
    {"lens": "迁移它", "text": "不止学习。跳绳、画画、和同学相处，凡是心里冒出「我不会」的时候，都可以补上一个下一步。"},
])}
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>「还」字一加上，门就留一条缝——<strong>我还没学会，我下一步可以……</strong></div></div>
    ''', tag="概念一"))

    rw_btns = "\n".join(
        f'            <button class="choice" data-rw="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in REWRITES
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：说法小改手，把「我不会」改一改", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一句心里常冒出来的「我不会」，再从三种改写里选一个。<strong>选得不太合适也不会说你错</strong>，我会告诉你这样可能会发生什么，还可以试试什么。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 心里冒出来的那一句</div>
          <div class="grid" id="rw-stage">
{rw_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 换一种说法试试</div>
          <div class="grid" id="rw-opts">
            <span style="color:var(--muted);font-size:14px">先在上面点一句，这里就会出现三种改写。</span>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">改写进度</span><span class="v" id="rw-score">已经改写 0 / 5 句</span></div>
          </div>
          <p class="result warn" id="rw-out" style="margin-top:12px">先点一句你自己也说过的话。</p>
        </div>
        <div class="inner-card" style="margin-top:14px">
          <p><strong>轮到你自己写一句：</strong></p>
          <p style="color:var(--muted)">想一想，最近哪一件事让你说过「我不会」？把它改写成你的句子。</p>
          <textarea id="rw-answer" rows="2" placeholder="我还没学会……，我下一步可以……" style="margin-top:8px"></textarea>
        </div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "情绪温度计：先量一量，再把它说出来", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">心里难受的时候，光说「我不高兴」别人也不知道怎么帮你。可以给自己画一根<strong>情绪温度计</strong>，从 0 度到 10 度。</p>
        <div class="grid grid-3">
          <div class="inner-card">
            <p><strong>0—3 度</strong></p>
            <p style="color:var(--muted)">很平稳。适合做需要动脑的事。</p>
          </div>
          <div class="inner-card">
            <p><strong>4—6 度</strong></p>
            <p style="color:var(--muted)">有点起伏。做三次慢慢的呼吸，喝几口水。</p>
          </div>
          <div class="inner-card">
            <p><strong>7—10 度</strong></p>
            <p style="color:var(--muted)">挺难受。找一个人说几句话，或者写下来。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="情绪温度计示意图，0到10度分四档，附中文标注">
          <figcaption>示意图：从 0 度到 10 度的情绪温度计，每一档配一句可以说出来的话（教学示意图，人物为中性简洁插画）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「温度高就是不好，得赶紧压下去」。温度只是一个信号，像手碰到热水会缩回来那样，它在提醒你<strong>现在需要什么</strong>。真正要练的不是把温度压下去，而是量准它，然后说出那句让别人听得懂的话。</p>
        </div>
        <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(78,205,196,.45)">
          <p><strong>说完感受，再补一句下一步：</strong></p>
          <p style="color:var(--muted)">「我现在很失望，因为我很想考好。<strong>我想和你一起看看错在哪里。</strong>」——后面这半句，才是让事情往前走的那半句。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "温度看不见，可身体会替它说话：脸红、手心出汗、胸口发闷、鼻子发酸。先看见身体，就看见了温度。"},
    {"lens": "解释它", "text": "为什么量出来好受一些？因为说不清的时候最闷，像一团打了结的线；给出一个数，心里就知道自己站在哪儿了。"},
    {"lens": "迁移它", "text": "和同伴闹别扭、被误会、家里有事的时候，都可以先量一量，再决定现在做什么、找谁说话。"},
])}
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>先量温度，再说感受，最后加一句下一步——<strong>温度不是好坏，它告诉我需要什么。</strong></div></div>
    ''', tag="概念二"))

    temp_btns = "\n".join(
        f'            <button class="choice" data-temp="{v}" style="text-align:center">{v} 度</button>'
        for v in (2, 5, 8, 10)
    )
    feel_btns = "\n".join(
        f'            <button class="choice" data-feel="{f}" style="text-align:center">{f}</button>'
        for f in TEMP_FEELINGS
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：量一量我的情绪温度", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">拖动滑块，或者直接点一个温度按钮，找到最像你现在的那个数。再给你的感觉起一个名字，看看这个温度下可以说哪一句话。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 我现在的温度是</div>
          <div class="slider-row">
            <label for="thermo">0 — 10 度</label>
            <input type="range" id="thermo" min="0" max="10" step="1" value="5">
            <span id="thermo-num" style="font-weight:800;color:var(--link);min-width:56px;text-align:right">5 度</span>
          </div>
          <div class="grid grid-2" style="margin-top:10px">
{temp_btns}
          </div>
          <div style="margin-top:14px;background:var(--bg-subtle);border:1px solid var(--line-subtle);border-radius:12px;padding:12px">
            <div style="font-size:13px;color:var(--muted);margin-bottom:6px">温度计</div>
            <div style="height:18px;border-radius:9px;background:rgb(var(--paper-rgb) / .18);overflow:hidden">
              <div id="thermo-fill" style="height:100%;width:50%;border-radius:9px;background:linear-gradient(90deg,var(--brand-2),var(--brand));transition:width .25s ease"></div>
            </div>
            <div style="margin-top:8px;font-weight:700">现在这一档：<span id="thermo-band">心里不太舒服</span></div>
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 给这种感觉起个名字</div>
          <div class="grid grid-3">
{feel_btns}
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">量出来的温度</span><span class="v" id="thermo-readout">5 度</span></div>
          </div>
          <p class="result warn" id="thermo-out" style="margin-top:12px">拖动滑块，看看你这个温度可以说哪一句话。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💛</span><div><strong>不用挑一个「对」的温度：</strong>温度是你自己的，几度都可以。量准了，才知道现在最需要的是什么。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小满的数学卷子", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>数学卷子发下来，比上次退步了不少。小满一眼看到那几个红圈，脸一下热了，心里那句话又冒出来了——我不会。请你陪他走四步。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>量一量温度：</strong>胸口沉沉的，什么都不想做——大概八度，挺难受的。先承认它，不用假装没事。</div></div>
          <div class="step"><span class="n">2</span><div><strong>把感受说出来：</strong>「我现在很失望，因为我很想考好。」说出感受，别人就知道怎么陪你了。</div></div>
          <div class="step"><span class="n">3</span><div><strong>把那句话改一改：</strong>「我不是不会，我是这几道应用题还没弄懂。」——加一个「还」字，门就留了一条缝。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>定一个下一步：</strong>「今天把三道错题抄到错题本上，明天课间去问老师。」卷子还是那张卷子，可他知道明天先做什么了。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「心情好了再学，成绩才会好」，于是先等心情过去。小满这四步里，心情没有立刻变好——他量出来是八度，也确实难受。可是他把难受说出来了，并且给自己定了一个能做到的小步骤。<strong>不是等难受走了才学，而是带着难受先做一小步。</strong></p>
        </div>
        <div class="inner-card">
          <p><strong>说给同桌听：</strong>小满这四步里，哪一步你自己已经做到了？哪一步还想再练一练？</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "下面哪句话更像成长的说法？",
         "options": [("这篇课文我还没背下来，我下一步先分三段，每段读五遍", True),
                     ("我记性太差了，背什么都没用", False),
                     ("我不会背，明天再说吧", False)],
         "explain": "给自己一个具体的小步骤，比给自己一个结论有用得多。"
                    "<strong>错因提醒：</strong>常见错误是把「还没练够」误认为「天生不行」——把练习次数的问题，当成了自己的能力问题。"},
        {"q": "关于情绪温度计，下面哪种理解更合适？",
         "options": [("温度只是一个信号，它在提醒我现在需要什么", True),
                     ("温度高就说明我心里有问题", False),
                     ("温度要一直保持在 0 度才好", False)],
         "explain": "温度像身体的疼感一样，是提示，不是评价。量准它，才知道现在该做什么。"
                    "<strong>错因提醒：</strong>有人误认为「难受就得马上压下去」——压下去容易，可问题还在；先量一量、说出来，反而更快走过去。"},
        {"q": "考试没考好，下面哪种说法对自己更有帮助？",
         "options": [("我现在挺失望的，我想和你一起看看错在哪里", True),
                     ("我完了，我永远都考不好", False),
                     ("都怪别人，跟我没关系", False)],
         "explain": "先说感受，再补一句下一步，是对自己最有帮助的一种说法，别人也知道该怎么帮你。"
                    "<strong>错因提醒：</strong>最容易搞混的是「说出感受」和「给自己下结论」——「我很失望」说的是心情，「我永远都考不好」说的是命运。"}
    ], tag="概念测试"))

    expr_bins = "\n".join(
        f'''            <div class="sort-bin" id="expr-bin-{b["id"]}" role="button" tabindex="0">
              <h4>{b["name"]}</h4>
              <div class="bin-list"></div>
            </div>'''
        for b in EXPR_BINS
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：考砸了，哪种说法对自己更有帮助", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">六张卡片都是考试没考好以后可能出现的心思和做法。先在左边点一张，再点上面两栏中的一个。<strong>分错了也不扣分</strong>，我会告诉你它更合适放在哪里，以及为什么。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 六张卡片（点一张选中）</div>
          <div class="sort-bank" id="expr-bank"></div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 它属于哪一栏</div>
          <div class="sort-bins">
{expr_bins}
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">分好了几张</span><span class="v" id="expr-score">已经分好 0 / 6 张</span></div>
          </div>
          <p class="result warn" id="expr-out" style="margin-top:12px">先在左边点一张卡片。</p>
        </div>
        <div class="inner-card" style="margin-top:14px">
          <p><strong>写出你自己最想说的那一句：</strong></p>
          <p style="color:var(--muted)">格式是：先说感受，再说下一步。写下来，下次遇到就照着说。</p>
          <textarea id="syn-answer" rows="2" placeholder="我现在……，我想……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换三个新情境，办法还在不在", TTS["posttest"], [
        {"q": "上课回答问题答错了，有同学笑了一下，你心里很不舒服。下面哪个做法更合适？",
         "options": [("先量一量温度，再说一句：我刚才有点紧张，我想再试一次", True),
                     ("以后再也不举手了，免得又出错", False),
                     ("下课去说那个笑的同学一顿", False)],
         "explain": "把紧张说出来，再给自己一次机会，比从此不举手有用得多；下课去找人理论，只会让事情更大。"
                    "<strong>错因提醒：</strong>有人误认为「不举手就不会出错」——不出错的办法确实有，可同时也把学会的机会一起关掉了。"},
        {"q": "课文背了五遍还是背不下来，心里有点烦。下面哪个做法更合适？",
         "options": [("停下来量一量温度，把课文分成三段，今天先背第一段", True),
                     ("把书一合，说反正我记性差", False),
                     ("一直坐着硬背，背到很晚", False)],
         "explain": "烦的时候，先把任务变小一点再开始，往往比硬撑更容易走下去。"
                    "<strong>错因提醒：</strong>常见错误是误认为「背不下来就是不够努力」——有时候是方法要换，不是力气要加。"},
        {"q": "好朋友这次考得比我好很多，你心里有点不是滋味。下面哪个做法更合适？",
         "options": [("先承认自己有点羡慕，再问一句：你这部分是怎么复习的", True),
                     ("不理他了，等他来哄我", False),
                     ("对自己说：我怎么努力都比不上他", False)],
         "explain": "羡慕是很自然的心情，承认它，它就不会一直在心里打转；问一句方法，你还多学到一样东西。"
                    "<strong>错因提醒：</strong>容易搞混的是「羡慕这件事」和「否定自己这个人」——别人考得好，说明这条路走得通，不等于你走不通。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，讲清学习自信这件事", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>换一个说法：</strong>「我不会」是一句结论，「我还没学会……，我下一步可以……」留着一个下一步。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>先量再说：</strong>用情绪温度计找到几度，再用一句话把感受说出来，温度只是信号。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>感受加下一步：</strong>考砸了以后，说感受、看错题、定一个小步骤，是对自己最有帮助的说法。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>还要记牢一件事：</strong>学一样新东西，一开始觉得难、觉得不会，几乎每个人都会遇到，这很正常。如果有一段时间你一直很难受，上课也听不进去，说给老师、爸爸妈妈听一听，是很聪明的做法。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「还没、温度、下一步」这三个词，说清楚你上一次没考好的经过。</p>
          <p style="color:var(--muted)">再动一动手：<strong>画一画</strong>你的情绪温度计，在三个温度旁边，各写一个你自己做得到的小办法。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "把三句「我不会」改写成「我还没学会……」，每一句后面补上自己的下一步。",
            "写出情绪温度计里，你能做到的两个小办法。",
            "说出「我还没学会」和「我永远都学不会」这两句话的不同。",
        ],
        [
            "做一张「情绪温度计」贴在书桌前，标出 3 度、6 度、8 度，各写一句可以说出来的话。",
            "记录一次：遇到一道不会的题，你心里的温度是几度，后来做了什么。",
        ],
        [
            "这一周里，挑一件你觉得有点难的学习任务，做完以后写三句话：当时的温度、你说的一句话、你的下一步。",
            "和同桌一起想一想：我们班上还有哪些说法，能把「我不会」说得更有希望？写两条。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "psych-e-g4-study-motivation",
    "node_id": "psych-e-g4-study-motivation",
    "subject": "psychology",
    "subject_cn": "心理健康",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "中小学心理健康教育指导纲要（2012年修订）/ 教育部相关要求 · 小学",
    "title": "学习自信与情绪表达",
    "name_en": "Learning Confidence and Naming Feelings",
    "grade": 4,
    "grade_cn": "四年级",
    "domain": "learning-support",
    "domain_cn": "学习辅导",
    "lesson_type": "workshop",
    "version": "1.0.0",
    "description": "面向小学四年级的学习辅导课：把「我不会」改写成「我还没学会……，我下一步可以……」的表达练习，用情绪温度计先量一量难受的程度再说出来，最后分清考砸以后哪些表达方式对自己更有帮助。两个互动台子都能真的操作：一个是说法小改手，五句「我不会」各配三种改写，错误反馈一律写成「这样可能会……，还可以试试……」；一个是情绪温度计，滑块加温度按钮真的能拖、能点，实时给出这一档的描述、一句可以说出来的话和一个马上能做的小办法。综合任务把六张「考砸以后的心思和做法」分成两栏。全课语气温和、不评判、不贴标签，只讲可操作的表达办法，不涉及伤害性情节，插图一律为中性简洁的教学插画。",
    "tags": ["学习自信", "情绪表达", "成长型说法", "四年级", "学习辅导"],
    "standard_ref": "《中小学心理健康教育指导纲要（2012年修订）· 小学中高年级》学习辅导——初步培养学生的学习能力，激发学习兴趣和探究精神，树立自信，乐于学习；学会体验情绪并表达自己的情绪。",
    "hero_question": "作业本上那句「我不会」说出来以后，笔就不想动了——这句话能换一种说法吗？",
    "hero_alt": "学习自信与情绪表达知识结构图：换一种说法、量一量温度、说出感受加下一步 三栏",
    "hero_caption": "学习自信与情绪表达：我还没学会…… · 情绪温度计 · 说出感受再加一句下一步",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "「我不会」和「我还没学会」到底差在哪里？", "d": "两句话我好像都说过，效果很不一样", "v": "我不会和我还没学会到底差在哪里"},
        {"t": "心里难受的时候，怎么知道自己到了几分？", "d": "有时候闷得说不清，也不知道算不算严重", "v": "心里难受的时候怎么知道自己到了几分"},
        {"t": "考砸了可以说哪些话，哪一种对自己更有帮助？", "d": "想说点什么，又怕越说越难受", "v": "考砸了可以说哪些话哪一种对自己更有帮助"},
        {"t": "怎么才能真的学会，而不是一直觉得自己不行？", "d": "想找到那种「能往前走一步」的办法", "v": "怎么才能真的学会而不是一直觉得自己不行"},
    ],
    "objectives": [
        "能说出「我不会」和「我还没学会」在说法上的不同，知道差别就在后面有没有一个下一步",
        "能把三句「我不会」改写成「我还没学会……，我下一步可以……」，并补上自己的下一步",
        "能用情绪温度计找到自己现在的温度，再用一句话把感受说出来",
        "能分辨考砸以后不同的表达方式，说出哪一种对自己更有帮助",
    ],
    "objectives_plain": [
        "能说出「我不会」和「我还没学会」在说法上的不同，知道差别就在后面有没有一个下一步",
        "能把三句「我不会」改写成「我还没学会……，我下一步可以……」，并补上自己的下一步",
        "能用情绪温度计找到自己现在的温度，再用一句话把感受说出来",
        "能分辨考砸以后不同的表达方式，说出哪一种对自己更有帮助",
    ],
    "standards": [
        {"content": "初步培养学生的学习能力，激发学习兴趣和探究精神，树立自信，乐于学习",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学中高年级 · 学习辅导"},
        {"content": "学会体验情绪并表达自己的情绪",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学中高年级 · 学习辅导"},
    ],
    "prereqs": ["psych-e-g4-peer-relation"],
    "prereqs_name": "同伴交往与解决困难",
    "prereqs_meta": "psych-e-g4-peer-relation",
    "leads_to": ["psych-e-g5-self-accept"],
    "next_meta": "psych-e-g5-self-accept",
    "section_images": ["assets/psych-e-g4-study-motivation-fig1.webp", "assets/psych-e-g4-study-motivation-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "那句「我不会」说出来以后，笔就放下了——这节课教你把它换一个说法，并且量一量自己有多难受。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能改写自己的一句话，也能说出自己现在的温度。",
        "objectives": "看清四件事：两句话差在哪里、怎么改写、怎么量温度、考砸了怎么说更有帮助。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "「我不会」像关上的门，「我还没学会」留一条缝——后面一定跟着一个下一步。",
        "lab-1": "重点不是选对，而是看看同一个说法换一换，接下来会发生什么。",
        "module-2": "温度只是信号，不是好坏。先量一量，再说一句别人听得懂的话。",
        "lab-2": "拖一拖滑块，找到最像你现在的那个数；几度都可以，没有「对」的温度。",
        "worked-example": "小满四步：量温度（八度）、说感受、把「我不会」改成「还没弄懂」、定一个下一步。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "把六张卡片分两栏，找出对自己更有帮助的那一类说法有什么共同点。",
        "posttest": "出现了答错被笑、背不下来、朋友考得比我好，看看你能不能用上今天的办法。",
        "summary": "三句话：换一个说法、先量再说、感受加下一步。",
        "homework": "三层小任务，先做前两层，第三层可以请家里人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先帮你找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学心理健康「学习辅导」在四年级的空缺，正对课标「初步培养学生的学习能力，激发学习兴趣和探究精神，树立自信，乐于学习」「学会体验情绪并表达自己的情绪」。四年级学生的难点有两个：①「我不会」是一句来得极快的结论，一出口人就停住，缺的不是能力，而是一个把话接下去的句式；②难受的时候分不清自己有多难受，也说不清需要什么，于是只有硬撑和撒手两种做法。所以全课围绕两件能立刻上手的小工具：概念一把「我不会」改写成「我还没学会……，我下一步可以……」，并且明确「后面有没有一个动作」是区分成长说法和找借口的判据；概念二给出一根 0—10 度的情绪温度计，把温度和「现在需要什么」连起来，并强调说完感受要再补一句下一步。两个互动台子都能真的操作：说法小改手（五句「我不会」各配三种改写，错误反馈一律写成「这样可能会……，还可以试试……」，另留一个自由文本框）、情绪温度计（range 滑块 + 温度按钮真的能拖能点，实时给出描述、一句可以说出来的话和一个马上能做的小办法）。综合任务把六张「考砸以后的心思和做法」分成「对自己更有帮助」和「帮助不大」两栏，收尾让学生自己说出共同点——先说感受，再说下一步。全课语气温和、不评判、不贴标签，只讲可操作的表达办法，不涉及伤害性情节；插图一律为中性简洁的教学插画，不使用真实儿童照片风格人像。",
    "plan_table": """| 1 | cover | 学习自信与情绪表达 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 「我不会」还是「我还没学会」，差的是下一步 | 承·概念一（成长型说法） |
| 6 | interactive | 动手一：说法小改手，把「我不会」改一改 | 承·表达练习（五句改写 + 自由书写） |
| 7 | concept | 情绪温度计：先量一量，再把它说出来 | 承·概念二（情绪表达） |
| 8 | interactive | 动手二：量一量我的情绪温度 | 承·情绪温度计（滑块 + 温度档 + 一句话 + 小办法） |
| 9 | concept | 例题示范：小满的数学卷子 | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：考砸了，哪种说法对自己更有帮助 | 合·迁移应用（六张卡片分两栏） |
| 12 | quiz | 后测：换三个新情境，办法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，讲清学习自信这件事 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：换一种说法 / 量一量温度 / 感受加下一步 三栏\n- P5 「我不会」改写成「我还没学会」句式示意图（已生成），附中文标注\n- P7 情绪温度计示意图（已生成）：0—10 度分档，每档一句可以说出来的话，附中文标注\n- 三张图均为中性简洁教学插画，人物只用简单图形，不使用任何真实儿童照片或可识别肖像\n- 若需补充：班级「错题本」样例照片（需学校提供并授权后使用）",
}
