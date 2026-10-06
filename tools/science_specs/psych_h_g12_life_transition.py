# -*- coding: utf-8 -*-
"""高中 · 心理健康 · 人生过渡与社会适应（高三）—— 补齐知识树「生活适应」空缺

铁规：语气温和、不评判、不贴标签；通篇使用日常语言，只讲可操作的做法。
本课只讲过缓渡中的适应过程与可操作的做法，落脚点是「变化是正常的、想家是正常的、
不必马上适应」。反馈一律温和：这样可能会……，还可以试试……
核心模拟：变化盘点与应对台——把八条变化分进「我能掌控的／需要时间的／要找人帮忙的」三栏，
          每一条再配一个具体做法，三栏实时汇总。
另含：适应时间线对照台（六件事 → 头三天 / 第二到四周 / 两个月后）
      + 过渡准备卡生成台（挑变化 → 选可以联系的人 → 定检查时间）。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/psych-h-g12-life-transition-fig1.webp'
F2 = './assets/psych-h-g12-life-transition-fig2.webp'

TTS = {
    "hero": "这一年会过去，然后有一段时间，你会发现自己站在一个不太一样的地方。可能是去一个新的城市读书，可能是住进学校的宿舍，也可能是身边的人换了一批。这节课不打算告诉你别难过、要坚强，那种话没什么用。我们只做三件事。第一件，把正在发生的变化一条条摊开，看清楚变的到底是什么——是环境变了，是关系要重新建立，还是每天的节奏要重排。第二件，把每一条变化放进三个位置里：哪些是我能自己掌控的，哪些需要一点时间，哪些要找人帮忙。然后给每一条配一个具体做法。第三件，说清楚一件事：想家、觉得不习惯，这些都不是适应不良，它们本来就属于过渡的一部分。",
    "problem-anchor": "在开始之前，先选出最贴近你最近状态的一项。是担心离开熟悉的地方会不适应，是已经换了环境还在慢慢找感觉，还是想到要重新认识一批人心里没底，又或者只是偶尔会想家。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出过渡期里常见的变化可以分成三类：环境变了、关系要重建、节奏要重排。第二，会用变化盘点与应对台，把八条变化分进我能掌控的、需要时间的、要找人帮忙的三个位置，并为每一条配一个具体做法。第三，能说出想家和不习惯在过渡期里是正常的，并知道哪些事该给自己时间、哪些事可以找人帮忙。第四，能为自己的过渡期写出一张准备卡，上面有一条变化、一个做法、一个可以联系的人。",
    "pretest": "先做三道小题，凭你现在的想法选就行，没有对错，也不打分。选完会立刻出现解释，正好帮你看清自己现在怎么看这段过渡。",
    "module-1": "我们先把过渡期里到底变了什么分清楚。变的不只是地方，它大致有三类。第一类，环境变了：住的地方、上课的地方、吃饭的地方都不一样了，很多原来不用想的事情现在要想。第二类，关系要重建：原来那些熟的人不在身边了，新的关系要从头开始，这需要时间。第三类，节奏要重排：起床、睡觉、吃饭、做题、休息，这些原来被安排好的事情，现在要自己安排。这三类混在一起的时候，人会觉得哪里都不顺，其实只是它们同时发生了。请留意一点：同样的变化，对不同的人难易不一样，这跟谁更能吃苦没关系。",
    "lab-1": "现在打开变化盘点与应对台。左边有八条变化，每一条先选一个位置：我能掌控的、需要时间的、要找人帮忙的。选好之后，再为它挑一个具体做法。右边三个栏会实时汇总你放进去的内容。请留意，同一条变化放在不同位置都有道理，重要的是它后面有没有跟一个具体的做法。",
    "module-2": "接下来要说清楚三句话。第一句，想家是正常的。它不是不够独立，也不是适应能力差，它说明你原来有一些很重要的连接。第二句，不必马上适应。适应有一个大致的时间过程，头几天觉得什么都乱，第二到第四周开始找到一点节奏，两个月以后回头看会发现自己已经走了很远。第三句，关系要重建，这件事急不来。新的朋友通常不是第一周就出现的，它往往从一起做一件小事开始。所以这一段时间里，可以做的事不是逼自己赶紧合群，而是先把自己每天的基本节奏立住。",
    "lab-2": "下面有六件事，每件选一个时间点：到新环境的头三天、第二到第四周、或者两个月以后。选完会给出解释。请留意，这个排序只是给一个大致节奏，早一点也可以，晚一点也没关系。",
    "worked-example": "我们完整走一遍。假设有一位同学，两周前离开家去外地读书。第一步，先不评价自己的感受，只盘点变化：住的地方变了、身边没有原来那几个人了、三餐和睡觉的时间都要自己定。第二步，分类：三餐和睡觉的时间放进我能掌控的；身边没有原来那几个人放进需要时间的；心里发紧想家这件事放进要找人帮忙的。第三步，每条配一个做法：作息先列一张只照一周的表；新朋友给自己一个月，先做到每天跟一两个人打个招呼；想家的时候，定一个固定的时间和家里打个电话。第四步，把打电话的时间提前告诉家里，这样不用每次都解释。第五步，定一个检查点，比如一个月后回看一次，看看哪一条已经不用再想了。",
    "conceptest-1": "现在用三个容易弄混的说法考考你。请仔细读每一个选项，选出你认为更合适的那个，然后看解释。",
    "synthesis": "最后一步，给自己的过渡期写一张准备卡。先从八条变化里挑一到两条你觉得最可能遇到的，再选一个你愿意联系的人，最后定一个检查时间。选完会生成一句话，你可以抄下来。",
    "posttest": "最后换几个新情境检验一下。这次的问题出现在一个刚到新环境的晚上、一次家里的电话里，还有一次你回看自己的时候。",
    "summary": "这节课我们弄明白了三件事。第一，过渡期里变的是三类东西：环境变了、关系要重建、节奏要重排。第二，把变化分进三个位置——我能掌控的、需要时间的、要找人帮忙的，每条再配一个具体做法。第三，想家是正常的，不必马上适应，适应本来就需要一段时间。最后把要求放低一点：不必逼自己马上像个老手，先立住每天的作息，再慢慢把关系建起来，这就已经是在适应了。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出台过渡期里变化的三类，并为每一类举一个例子。第二层能力应用，动手做：完成一次变化盘点与应对台，把八条变化分进三栏，并为每条写一个具体做法。第三层迁移挑战，选做：给自己的过渡期写一张准备卡，找一个合适的时间跟家里人聊一次，一个月后再回看一次，看看哪一条已经不用再想了。",
    "knowledge-graph": "这张图展示了这节课在知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续想的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 变的是三类东西", "lab-1": "核心模拟 变化盘点与应对台",
    "module-2": "概念二 想家是正常的，不必马上适应", "lab-2": "对照台 适应的节奏",
    "worked-example": "例题示范", "conceptest-1": "概念测试",
    "synthesis": "综合任务 过渡准备卡", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

CUSTOM_JS = r"""
/* ============================================================
   psych-h-g12-life-transition 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 核心模拟：变化盘点与应对台（八条变化 × 三栏 → 三条汇总栏）
   3) 适应时间线对照台（六件事 → 头三天 / 第二到四周 / 两个月后）
   4) 过渡准备卡生成台（挑变化 → 选可以联系的人 → 定检查时间）
   本文件不写死颜色，需要强调时用 var(--brand) / var(--brand-2)。
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

  /* ---------- 2. 核心模拟：变化盘点与应对台 ---------- */
  var BINS = [
    { k: 'hold', n: '我能掌控的', tip: '这件事你自己就能动起来——先定一个很小的做法，比等它自己变顺要快。' },
    { k: 'time', n: '需要时间的', tip: '这件事需要一点时间——给它几周，不用今天就解决。' },
    { k: 'help', n: '要找人帮忙的', tip: '这件事不必一个人扛——找一个人说一声，会轻松很多。' }
  ];
  var CHANGES = [
    { t: '每天几点起、几点睡，要自己安排了', best: 'hold' },
    { t: '原来最熟的那几个同学不在身边了', best: 'time' },
    { t: '上课、吃饭、打水的地方都换了', best: 'hold' },
    { t: '想家的时候心里发紧，晚上更明显', best: 'help' },
    { t: '新的朋友要从头开始认识', best: 'time' },
    { t: '遇到麻烦要自己去找人问', best: 'help' },
    { t: '生活里的钱要自己算着花', best: 'hold' },
    { t: '一些熟悉的小习惯不在了', best: 'time' }
  ];
  var ACTIONS = [
    { k: 'hold', t: '列一张只照一周的作息表' },
    { k: 'hold', t: '把每周开销记在本子上' },
    { k: 'hold', t: '主动先跟同宿舍的人打招呼' },
    { k: 'time', t: '允许自己想家，不催自己' },
    { k: 'time', t: '给自己一个月再看好朋友的事' },
    { k: 'time', t: '每天走同一条路，让路先变熟' },
    { k: 'help', t: '找一位老师说一句现在的情况' },
    { k: 'help', t: '跟家里说明白你需要什么' },
    { k: 'help', t: '找学校的心理老师聊一次' }
  ];
  var BINNAME = {};
  BINS.forEach(function (b) { BINNAME[b.k] = b.n; });
  var chg = CHANGES.map(function () { return { bin: '', act: -1 }; });
  var sortStage = document.getElementById('sort-stage');
  if (sortStage) {
    function renderSort() {
      var cards = CHANGES.map(function (c, i) {
        var s = chg[i];
        var binBtns = BINS.map(function (b) {
          var cls = 'choice';
          if (s.bin === b.k) cls += (b.k === c.best ? ' correct' : ' wrong');
          return '<button class="' + cls + '" data-sort-i="' + i + '" data-sort-bin="' + b.k +
            '" style="text-align:center;font-size:12px;padding:9px 4px">' + b.n + '</button>';
        }).join('');
        var actHtml = '';
        if (s.bin) {
          var chips = ACTIONS.map(function (a, j) {
            var cls = 'choice';
            if (s.act === j) cls += (a.k === c.best ? ' correct' : ' wrong');
            return '<button class="' + cls + '" data-sort-i="' + i + '" data-sort-act="' + j +
              '" style="text-align:left;font-size:12px;padding:8px 10px">' + a.t + '</button>';
          }).join('');
          actHtml = '<p style="margin:10px 0 6px;font-size:13px"><strong>再给它配一个具体做法：</strong></p>' +
            '<div class="grid grid-3" style="gap:6px">' + chips + '</div>';
        }
        var fb = '';
        if (s.bin && s.act >= 0) {
          var okAct = ACTIONS[s.act].k === c.best;
          fb = '<p class="result ' + (okAct ? '' : 'warn') + '" style="margin:10px 0 0">' +
            (okAct ? '<strong>这一条里，栏和做法配得上。</strong>'
                   : '<strong>这样可能会不太对得上，还可以试试换一个。</strong>') +
            BINS.filter(function (b) { return b.k === c.best; })[0].tip + '</p>';
        } else if (s.bin) {
          fb = '<p class="result warn" style="margin:10px 0 0">这一条放在了「' + BINNAME[s.bin] +
            '」。' + (s.bin === c.best ? '' : '这样可能会慢一点，还可以试试「' + BINNAME[c.best] + '」这个位置。') +
            '接着给它挑一个做法吧。</p>';
        }
        return '<div class="inner-card" style="padding:12px 14px;margin:8px 0">' +
          '<p style="margin:0 0 8px;font-size:15px"><strong>' + (i + 1) + '. ' + c.t + '</strong></p>' +
          '<div class="grid grid-3" style="gap:6px">' + binBtns + '</div>' + actHtml + fb + '</div>';
      }).join('');

      var binsHtml = BINS.map(function (b) {
        var inside = CHANGES.map(function (c, i) { return { c: c, i: i, s: chg[i] }; })
          .filter(function (x) { return x.s.bin === b.k; });
        var tags = inside.length ? inside.map(function (x) {
          var act = x.s.act >= 0 ? '<br><span style="font-size:12px;color:var(--muted)">做法：' +
            ACTIONS[x.s.act].t + '</span>' : '<br><span style="font-size:12px;color:var(--muted)">还没有配做法</span>';
          return '<div class="tag" style="display:block;margin:4px 0">' + x.c.t + act + '</div>';
        }).join('') : '<span style="color:var(--muted);font-size:13px">还没有放进来</span>';
        return '<div class="sort-bin' + (inside.length ? ' ok' : '') + '"><h4>' + b.n + '（' +
          inside.length + '）</h4>' + tags + '</div>';
      }).join('');

      sortStage.innerHTML = '<div class="grid">' + cards + '</div>' +
        '<p style="margin:16px 0 8px;font-weight:700">三个栏现在是这样</p>' +
        '<div class="sort-bins" style="grid-template-columns:repeat(3,1fr)">' + binsHtml + '</div>';

      sortStage.querySelectorAll('[data-sort-bin]').forEach(function (b) {
        b.addEventListener('click', function () {
          var i = parseInt(b.dataset.sortI, 10);
          chg[i].bin = b.dataset.sortBin;
          chg[i].act = -1;
          renderSort();
          updateSortOut();
        });
      });
      sortStage.querySelectorAll('[data-sort-act]').forEach(function (b) {
        b.addEventListener('click', function () {
          var i = parseInt(b.dataset.sortI, 10);
          chg[i].act = parseInt(b.dataset.sortAct, 10);
          renderSort();
          updateSortOut();
        });
      });
    }
    function updateSortOut() {
      var done = chg.filter(function (s) { return s.bin && s.act >= 0; }).length;
      var out = document.getElementById('sort-out');
      out.style.display = 'block';
      out.className = 'result' + (done >= 8 ? '' : ' warn');
      var counts = BINS.map(function (b) {
        return b.n + ' ' + chg.filter(function (s) { return s.bin === b.k; }).length + ' 条';
      }).join('；');
      out.innerHTML = '<strong>已配好 ' + done + '/8 条。当前分布：' + counts + '。</strong>' +
        '三个位置没有好坏之分——需要时间的就给它时间，要找人帮忙的就去找人，' +
        '能自己动的就先动一小步。如果有一栏是空的，也许可以想一想是不是把某件事扛得太久了。' +
        (done >= 8 ? '<br>八条都配好了。你可以看看哪几条的做法是这周就能开始的。' : '');
    }
    renderSort();
    updateSortOut();
  }

  /* ---------- 3. 适应时间线对照台 ---------- */
  var STEPS = [
    { k: 'd3', n: '头三天' },
    { k: 'w24', n: '第二到四周' },
    { k: 'm2', n: '两个月以后' }
  ];
  var TL = [
    { t: '先弄清楚吃饭、打水、上课的地方分别在哪里。', a: 'd3',
      d3: '先把最要紧的几件生存小事解决掉，后面心里会稳一些。',
      w24: '这件事往后放一点也可以，只是前几周会多绕几次路。',
      m2: '放到两个月以后就有点晚了，这几件事越早知道越省力气。' },
    { t: '允许自己还有点想家，不急着说我适应了。', a: 'd3',
      d3: '刚到的这段时间，想家本来就会来，允许它在，比压着它省力。',
      w24: '想家这件事会持续一段时间，早点允许它，反而轻松些。',
      m2: '这件事不用等到两个月以后才允许，现在就可以给自己一点余地。' },
    { t: '试着和一两位新同学一起做一件小事，比如一起吃饭、一起走一段路。', a: 'w24',
      d3: '头三天就要求自己交到朋友，压力可能有点大。先安顿好自己也不算慢。',
      w24: '关系通常是从一起做一件小事开始的，这几周正好合适。',
      m2: '也可以，只是前两个月会相对孤单一些，看你自己觉得能不能接受。' },
    { t: '把每天的作息大致稳定下来，找到自己能用的学习时段。', a: 'w24',
      d3: '太早定死作息容易定得不合适，可以先照着看一周再调。',
      w24: '这几周摸清自己的节奏最合适，定下来之后效率会明显好一些。',
      m2: '晚一点也能定，只是前面这段时间会有点乱。' },
    { t: '回头看看这几个月自己的变化，把有效的做法记下来。', a: 'm2',
      d3: '这时候还没有多少变化可以回头看，先过着就好。',
      w24: '这时候可以先粗略看一眼，不过两个月的对比会更清楚。',
      m2: '这时候回头看最合适，你会发现自己已经走了挺远。' },
    { t: '想一想哪些原来的习惯值得带过来，哪些可以换掉。', a: 'm2',
      d3: '先别急着换掉旧习惯，它们一开始还能帮你稳住自己。',
      w24: '可以开始想了，等过一阵子再看会更清楚哪些真的不合适。',
      m2: '到这时候看会比较准，因为你已经知道哪些习惯在这里用不上。' }
  ];
  var tlStage = document.getElementById('tl-stage');
  if (tlStage) {
    function renderTl() {
      tlStage.innerHTML = TL.map(function (c, i) {
        var btns = STEPS.map(function (s) {
          var cls = 'choice';
          if (c.picked === s.k) cls += (s.k === c.a ? ' correct' : ' wrong');
          return '<button class="' + cls + '" data-tl="' + i + '" data-tl-pick="' + s.k +
            '" style="text-align:center;font-size:12px;padding:10px 6px">' + s.n + '</button>';
        }).join('');
        return '<div class="inner-card" style="padding:12px 14px;margin:8px 0">' +
          '<p style="margin:0 0 8px;font-size:15px"><strong>' + (i + 1) + '. ' + c.t + '</strong></p>' +
          '<div class="grid grid-3" style="gap:6px">' + btns + '</div>' +
          (c.picked ? '<p class="result ' + (c.picked === c.a ? '' : 'warn') + '" style="margin:8px 0 0">' +
            (c.picked === c.a ? '<strong>这个时间点挺合适。</strong>' : '<strong>还可以再想想：</strong>') +
            c[c.picked] + '</p>' : '') +
          '</div>';
      }).join('');
      tlStage.querySelectorAll('[data-tl]').forEach(function (b) {
        b.addEventListener('click', function () {
          var i = parseInt(b.dataset.tl, 10);
          if (TL[i].picked) return;
          TL[i].picked = b.dataset.tlPick;
          renderTl();
          var done = TL.filter(function (x) { return x.picked; }).length;
          var out = document.getElementById('tl-out');
          out.style.display = 'block';
          out.className = 'result' + (done >= 6 ? '' : ' warn');
          out.innerHTML = '<strong>已排好 ' + done + '/6 件。</strong>' +
            '适应有一个大致的时间过程：头几天先把基本的安顿好，第二到四周开始找到节奏，' +
            '两个月以后再回头整理。早一点晚一点都可以——这个排序只是想让你知道，慢不是问题。' +
            (done >= 6 ? '<br>六件都排好了。你可以看看自己现在大概在哪个位置。' : '');
        });
      });
    }
    renderTl();
  }

  /* ---------- 4. 过渡准备卡生成台 ---------- */
  var PEOPLE = ['家里的人', '班主任或辅导员', '学校的心理老师',
    '同宿舍的一位同学', '社团里认识的一位学长', '原来学校的一位老朋友'];
  var CHECKS = ['到新地方的第一周结束时', '第一个月结束时', '期中考试之后'];
  var prep = { items: {}, person: '', when: '' };
  var prepStage = document.getElementById('prep-stage');
  if (prepStage) {
    function renderPrep() {
      var itemBtns = CHANGES.map(function (c, i) {
        return '<button class="choice' + (prep.items[i] ? ' selected' : '') +
          '" data-prep-item="' + i + '" style="font-size:13px;padding:10px 14px;text-align:left">' +
          c.t + '</button>';
      }).join('');
      var personBtns = PEOPLE.map(function (p) {
        return '<button class="choice' + (prep.person === p ? ' selected' : '') +
          '" data-prep-person="' + p + '" style="font-size:13px;padding:10px 14px">' + p + '</button>';
      }).join('');
      var whenBtns = CHECKS.map(function (w) {
        return '<button class="choice' + (prep.when === w ? ' selected' : '') +
          '" data-prep-when="' + w + '" style="font-size:13px;padding:10px 14px;text-align:center">' + w + '</button>';
      }).join('');
      prepStage.innerHTML =
        '<div class="inner-card"><p style="margin:0 0 8px"><strong>第一步 · 挑一到两条你预计会遇到的</strong></p>' +
        '<div class="grid" style="gap:6px">' + itemBtns + '</div></div>' +
        '<div class="inner-card"><p style="margin:0 0 8px"><strong>第二步 · 选一个你愿意联系的人</strong></p>' +
        '<div class="grid grid-2" style="gap:6px">' + personBtns + '</div></div>' +
        '<div class="inner-card"><p style="margin:0 0 8px"><strong>第三步 · 定一个回看的时间</strong></p>' +
        '<div class="grid grid-3" style="gap:6px">' + whenBtns + '</div></div>';
      prepStage.querySelectorAll('[data-prep-item]').forEach(function (b) {
        b.addEventListener('click', function () {
          var k = b.dataset.prepItem;
          prep.items[k] = !prep.items[k];
          renderPrep();
        });
      });
      prepStage.querySelectorAll('[data-prep-person]').forEach(function (b) {
        b.addEventListener('click', function () { prep.person = b.dataset.prepPerson; renderPrep(); });
      });
      prepStage.querySelectorAll('[data-prep-when]').forEach(function (b) {
        b.addEventListener('click', function () { prep.when = b.dataset.prepWhen; renderPrep(); });
      });
      var picked = Object.keys(prep.items).filter(function (k) { return prep.items[k]; });
      var out = document.getElementById('prep-out');
      out.style.display = 'block';
      if (picked.length === 0 || !prep.person || !prep.when) {
        out.className = 'result warn';
        out.innerHTML = '<strong>三步都选好，这里会生成一句话。</strong>' +
          '它不保证什么，只是把你需要的两样东西提前写下来：一个做法，和一个可以联系的人。';
      } else {
        var names = picked.map(function (k) { return CHANGES[parseInt(k, 10)].t; });
        out.className = 'result';
        out.innerHTML = '<strong>你的过渡准备卡：</strong>如果遇到' +
          names.map(function (t) { return '「' + t + '」'; }).join('和') +
          '，我按「' + BINS.filter(function (b) {
            return b.k === CHANGES[parseInt(picked[0], 10)].best;
          })[0].n + '」这一栏来做，先做一件小的事。需要的时候，我会去找' +
          '「' + prep.person + '」说一声。' + prep.when + '，我会回来看一次，' +
          '看看哪一条已经不用再想了。' +
          '<br><span style="color:var(--muted);font-size:14px">最后一句写在这里：如果到了那个时候还有一条没解决，' +
          '那也说明不了什么——过渡本来就需要时间。</span>';
      }
    }
    renderPrep();
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：你怎么看这段时间的变化？", TTS["pretest"], [
        {"q": "过渡期里，下面哪种说法更贴近「变的到底是什么」？",
         "options": [("变的不只是地方，还有关系要重建、每天的节奏要重排", True),
                     ("变的只有住的地方和上课的地方", False),
                     ("只是自己心情变了，环境其实没变", False)],
         "explain": "环境、关系、节奏三类常常同时变，所以才觉得哪里都不顺。<strong>错因提醒：</strong>常见错误是误认为只有环境变了，于是忽略了自己每天都在重新安排生活这件事。"},
        {"q": "刚到新地方，晚上特别想家。下面哪种理解更合适？",
         "options": [("想家是正常的，它说明我原来有一些很重要的连接", True),
                     ("想家说明我不够独立，得赶紧克服", False),
                     ("既然想家，就应该马上多参加活动让自己忙起来", False)],
         "explain": "想家属于过渡的一部分，允许它在，比压着它省力。<strong>错因提醒：</strong>容易把「想家」搞混成「适应能力差」——它反映的是关系的重要，不是能力的高低。"},
        {"q": "关于「适应」，下面哪种说法更符合实际？",
         "options": [("适应有一个大致的时间过程，头几天乱是常见的", True),
                     ("应该在第一周就完全适应，否则就是没做好", False),
                     ("只要熬着，什么都不用做就会好", False)],
         "explain": "适应需要时间，但也不是纯等——先把基本的节奏立住会帮上忙。<strong>错因提醒：</strong>误认为适应是一个开关，一按就好，或者反过来认为完全不用做任何事。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "过渡期里变的，其实是三类东西", TTS["module-1"], f'''
        <p style="font-size:17px;margin:0 0 12px">把变化拆开来看，就不容易觉得是自己不行。变的通常是环境、关系、节奏这三类，而且常常一起来。</p>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgb(var(--warm-rgb) / .45)">
          <p style="margin:0"><strong>为什么要先学这个？</strong>你已经知道换个环境要适应；<strong>但</strong>把所有不顺手混成一件事之后，很容易得出自己适应能力差的结论；<strong>所以</strong>先把变化拆成三类，一类一类看。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>环境变了：</strong>住的地方、上课的地方、吃饭的地方都不一样了，很多原来不用想的事情现在要想。</div></div>
          <div class="step"><span class="n">2</span><div><strong>关系要重建：</strong>原来熟的人不在身边了，新的关系要从头开始。这件事需要时间，急不来。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>节奏要重排：</strong>起床、睡觉、吃饭、做题、休息，原来被安排好的事现在要自己安排。</div></div>
        </div>
        <div class="kid-note"><span class="emoji">🧳</span><div><strong>留意一件事：</strong>同样的变化，对不同的人难易不一样，这跟谁更能吃苦没关系。它和你在原来的地方待了多久、带走了多少习惯有关。</div></div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">误认为过渡期要做的第一件事是赶紧认识新朋友。其实先把每天的基本节奏立住，人稳下来了，关系反而更容易建起来。</p>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="过渡期变化的三类示意图：环境变了、关系要重建、节奏要重排">
          <figcaption>变的三类东西：环境变了、关系要重建、节奏要重排</figcaption>
        </figure>
{insight_box([
    {"lens": "解释它", "text": "为什么过渡期特别累？因为三类变化同时发生，而每一类都要占用注意力。累不是因为你不坚强，是因为同时要处理的确实多。"},
    {"lens": "比较它", "text": "「我需要时间」和「我做不好」，说的是完全不同的事。前者是对过程的描述，后者是对自己的判断——过渡期里要把这两句分开。"},
    {"lens": "迁移它", "text": "这一套不只用在升学上。换宿舍、换班级、以后换工作、换城市，都可以用这三类先拆一遍。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "sort", 5, "lab-1", "核心模拟：变化盘点与应对台", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">八条变化，每条先选一个位置，再配一个具体做法。右边三个栏会实时汇总你放进去的内容。</p>
        <div class="lab-panel" id="sort-stage"></div>
        <p class="result warn" id="sort-out" style="margin-top:12px"></p>
        <div class="inner-card">
          <p><strong>写下来，留给自己：</strong>从三个栏里各挑一条，把它们的做法抄在一张纸上，贴在你每天都能看到的地方。</p>
          <textarea id="sort-answer" rows="3" placeholder="我能掌控的一条……；需要时间的一条……；要找人帮忙的一条……" style="margin-top:8px"></textarea>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧭</span><div><strong>三个位置没有好坏之分。</strong>同一条变化放在不同位置都有道理，重要的是它后面有没有跟一个具体的做法——有做法，事情就开始动了。</div></div>
    ''', tag="核心模拟", bloom="apply"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "想家是正常的，不必马上适应", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">这一段有三句话要说清楚，都是为了把要求放到一个合适的位置上。</p>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="适应时间过程的示意图：一条带刻度的路径，标注头三天、第二到四周、两个月以后">
          <figcaption>适应有一个大致的过程：先安顿、再找节奏、再回头整理</figcaption>
        </figure>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>想家是正常的。</strong>它不是不够独立，也不是适应能力差；它说明你原来有一些很重要的连接。</div></div>
          <div class="step"><span class="n">2</span><div><strong>不必马上适应。</strong>头几天觉得什么都乱是常见的；第二到第四周开始找到一点节奏；两个月以后回头看，常常会发现自己已经走了挺远。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>关系要重建，急不来。</strong>新的朋友通常不是第一周就出现的，它往往从一起做一件小事开始。</div></div>
        </div>
        <div class="kid-note"><span class="emoji">🌤️</span><div><strong>所以这段时间可以做什么：</strong>不是逼自己赶紧合群，而是先把每天的基本节奏立住——几点起、几点睡、什么时候学、什么时候歇。节奏稳了，人就不那么慌。</div></div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">误认为想家或者不习惯是一件需要藏起来的事。其实说出来、写下来，或者找一个人聊一聊，往往比硬撑着省力得多。</p>
        </div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "tl", 7, "lab-2", "对照台：适应的节奏可以怎么排？", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">六件事，每件选一个时间点。选完会给出解释——早一点也可以，晚一点也没关系。</p>
        <div class="lab-panel" id="tl-stage"></div>
        <p class="result warn" id="tl-out" style="display:none;margin-top:12px"></p>
        <div class="inner-card">
          <p><strong>写下来，留给自己：</strong>你觉得这几件事里，哪一件是你现在最想先做好的？写下它，再写一句你打算这周怎么开始。</p>
          <textarea id="tl-answer" rows="3" placeholder="我现在最想先做好的是……；这周我打算……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="动手实验室", bloom="evaluate"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：离家两周，从什么都乱到找回节奏", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgb(var(--warm-rgb) / .45)">
          <p style="margin:0"><strong>情境：</strong>一位同学两周前离开家去外地读书。他说不上哪里不对，就是觉得每天都在忙，又说不出忙了什么。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先不评价感受，只盘点变化：</strong>住的地方变了；身边没有原来那几个人了；三餐和睡觉的时间都要自己定。</div></div>
          <div class="step"><span class="n">2</span><div><strong>把变化分类：</strong>三餐和睡觉的时间放进我能掌控的；身边没有原来那几个人放进需要时间的；心里发紧想家放进要找人帮忙的。</div></div>
          <div class="step"><span class="n">3</span><div><strong>每条配一个做法：</strong>作息先列一张只照一周的表；新朋友给自己一个月，先做到每天跟一两个人打个招呼；想家的时候，定一个固定的时间和家里打电话。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>把做法告诉相关的人：</strong>先把打电话的时间告诉家里，这样不用每次重新解释一遍。</div></div>
          <div class="step"><span class="n">5</span><div><strong>定一个检查点：</strong>比如一个月后回看一次，看看哪一条已经不用再想了。不用一次解决全部，一次动一条就好。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">两个方向都容易走偏：一种是<strong>把全部希望压在一句赶紧适应上</strong>，结果每天都在评价自己不够好；另一种是<strong>什么都不做，只等时间过去</strong>，于是头几周一直在原地打转。中间那条路是：先做一小件能做的事，剩下的交给时间。</p>
        </div>
        <div class="inner-card">
          <p><strong>把期待放在合适的位置：</strong>这套做法不保证一个月就完全适应，也不保证不再想家。它能做到的是：让每一天有一点可以自己安排的东西。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "「都一个月了还是不太习惯，看来我真的不行」——这句话最需要改的地方是：",
         "options": [("它把适应的时间过程当成了对自己的评价", True),
                     ("它太消极了，应该改成要积极一点", False),
                     ("它没有说清楚到底哪里不习惯", False)],
         "explain": "一个月只是过程中的一段时间，不是成绩单。<strong>错因提醒：</strong>常见错误是误认为习惯得慢等于能力差——换一种问法是：这一个月里哪一件小事比刚来时顺了。"},
        {"q": "关于「三栏」（我能掌控的 / 需要时间的 / 要找人帮忙的），下面哪种理解更合适？",
         "options": [("同一条变化放在哪个位置都有道理，重点是它后面有没有跟一个做法", True),
                     ("要找人帮忙的，说明这件事自己解决不了，所以最不好", False),
                     ("三栏里最理想的是一条都不放进要找人帮忙的", False)],
         "explain": "三栏是给事情分门别类，不是给自己打分。<strong>错因提醒：</strong>容易把「需要找人帮忙」搞混成「自己不行」——过渡期里找人帮忙，本来就是有效做法之一。"},
        {"q": "刚到一个新地方，头几天最该先做的是哪一件？",
         "options": [("先弄清楚吃饭、打水、上课的地方在哪里", True),
                     ("先想办法尽快融入一个新的朋友圈", False),
                     ("先给自己定一个严格的作息，一天都不许乱", False)],
         "explain": "先把最要紧的几件小事解决掉，心里会稳一些。<strong>错因提醒：</strong>误认为头几天就该迅速合群或立刻进入高效状态，往往会让头几周过得更紧。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "prep", 10, "synthesis", "综合任务：过渡准备卡生成台", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">三步都选好，下面会生成一句话。它不是承诺，只是把你需要的两样东西提前写下来。</p>
        <div class="lab-panel" id="prep-stage"></div>
        <p class="result warn" id="prep-out" style="display:none;margin-top:12px"></p>
        <div class="inner-card">
          <p><strong>抄下来，留给自己：</strong>把生成的这句话抄在一张纸上，和那张三栏的做法清单放在一起。</p>
          <textarea id="syn-answer" rows="3" placeholder="如果遇到……，我按「……」这一栏来做；需要的时候，我会去找……" style="margin-top:8px"></textarea>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🌤️</span><div><strong>还有一件事想告诉你：</strong>这张卡上写了两个东西——一个做法，一个可以联系的人。如果以后你觉得一件事在卡上都找不到位置，也可以直接找学校的心理老师或者正规医疗机构聊一次，那是一件很寻常的事。</div></div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，看看方法还在不在", TTS["posttest"], [
        {"q": "到新环境的第一个晚上，你躺在不太熟悉的床上，觉得哪儿都不对。这时更合适的第一步是：",
         "options": [("先承认现在有点难受，然后把明天要办的几件小事写下来", True),
                     ("立刻给自己下结论：我可能适应不了这里", False),
                     ("把自己塞进一堆新活动里，不给自己留一点空", False)],
         "explain": "先允许感受在，再把注意力放到明天能做的小事上。<strong>错因提醒：</strong>常见错误是误认为必须马上压住难受，或者必须马上把自己填满，两种都会更累。"},
        {"q": "家里打电话问你习不习惯，你其实还不太习惯。更合适的回答是：",
         "options": [("说清现在还不太顺的地方，也告诉他们你需要什么", True),
                     ("说挺好的，什么都好，省得他们担心", False),
                     ("说这边什么都不行，让他们也跟着着急", False)],
         "explain": "说清具体需要什么，是让关心落到实处的方式。<strong>错因提醒：</strong>容易把「报喜不报忧」搞混成懂事——把话说清楚，家里才帮得上。"},
        {"q": "两个月后你回看这段过渡，发现自己还有一条没解决。下面哪种想法更合适？",
         "options": [("还有一条没解决很正常，看看它现在是不是该换个位置放", True),
                     ("两个月还没全部搞定，说明我的适应能力不行", False),
                     ("既然没解决，那张卡就没用了", False)],
         "explain": "没解决的那一条，可以在三栏里换一个位置再试。<strong>错因提醒：</strong>误认为过渡有终点线，过了就必须全部搞定——其实它就是一段有起有落的过程。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把这段过渡讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>变的就三类</strong>：环境变了、关系要重建、节奏要重排；它们常常一起来，所以特别累。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>把变化放三栏</strong>：我能掌控的、需要时间的、要找人帮忙的；每一条后面跟一个具体做法。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>想家是正常的</strong>：不必马上适应；先立住每天的节奏，关系慢慢建。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgb(var(--warm-rgb) / .45)">
          <p style="margin:0"><strong>回到开头那个不太对劲的时刻：</strong>当你在一个还不熟悉的地方醒来，觉得哪儿都不对，不必急着给自己下结论。先写下明天要办的两三件小事，再定一个给家里打电话的时间——今天就算过好了。</p>
        </div>
        <div class="inner-card">
          <p><strong>记忆锚点：</strong>三个词帮你记住这节课——<strong>拆开看、分三栏、慢慢来</strong>。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「拆开看、分三栏、慢慢来」这三个词，跟一位也在过渡期的同学说说你自己的一件变化，以及你打算怎么做。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "写出过渡期里变化的三类，并为每一类举一个具体的例子。",
            "写出三栏的名字，并各用一句话说明这一栏里的做法通常是什么样子。",
            "用自己的话说明为什么想家是正常的，写两到三句。",
        ],
        [
            "完成一次变化盘点与应对台，把八条变化分进三栏，并为每一条写一个具体做法。",
            "为自己这段时间排一个大致节奏：头三天做什么、第二到四周做什么、两个月以后回头看什么。",
        ],
        [
            "给自己的过渡期写一张准备卡，抄下来带在身边，并在合适的时间跟家里人聊一次。",
            "一个月后回看一次那张卡，写下哪一条已经不用再想了；如果还有一条没解决，写下你打算把它换到哪一栏。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "psych-h-g12-life-transition",
    "node_id": "psych-h-g12-life-transition",
    "subject": "psychology",
    "subject_cn": "心理健康",
    "stage": "high",
    "stage_cn": "高中",
    "curriculum": "中小学心理健康教育指导纲要（2012年修订）/ 教育部相关要求 · 高中",
    "title": "人生过渡与社会适应：变化来了，一条一条安顿",
    "name_en": "Life Transitions and Social Adaptation",
    "grade": 12,
    "grade_cn": "高三",
    "domain": "life-adaptation",
    "domain_cn": "生活适应",
    "lesson_type": "workshop",
    "version": "1.0.0",
    "description": "面向高三学生的人生过渡与社会适应课：先把过渡期的变化拆成三类——环境变了、关系要重建、节奏要重排；再用核心模拟「变化盘点与应对台」把八条常见变化分别放进我能掌控的、需要时间的、要找人帮忙的三个位置，并为每一条配一个具体做法，三个栏实时汇总；接着讲清三句话——想家是正常的、不必马上适应、关系要重建急不来，并用「适应时间线对照台」把六件事排到合适的阶段；最后用「过渡准备卡生成台」写下一个做法和一个可以联系的人。全课语气温和、不评判、不贴标签，明确写出不适应不等于适应能力差；语气温和、不评判、不贴标签，只讲能自己动手做的事。",
    "tags": ["人生过渡", "生活适应", "社会适应", "想家", "变化盘点", "求助", "高三"],
    "standard_ref": "《中小学心理健康教育指导纲要（2012年修订）· 高中》生活适应——逐步适应生活和社会的各种变化，为走向社会做好心理准备；树立远大理想，培养社会责任意识。",
    "hero_question": "换了一个地方之后，那种说不上来的不对劲，到底是什么？",
    "hero_alt": "人生过渡知识结构图三栏：变的是三类、分进三栏、慢慢来",
    "hero_caption": "变的是三类 · 分进三栏 · 慢慢来——过渡本来就需要一段时间",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个最贴近你最近状态的困惑，后面的内容都会围着它展开。",
    "anchor_choices": [
        {"t": "离开熟悉的地方，我会不会不适应？", "d": "想到要一个人生活，心里没底", "v": "离开熟悉的地方我会不会不适应"},
        {"t": "已经换了环境，还是找不到感觉", "d": "每天都在忙，却说不清在忙什么", "v": "已经换了环境还是找不到感觉"},
        {"t": "朋友要重新认识，不知道从哪开始", "d": "看着别人很快熟起来，自己插不进去", "v": "朋友要重新认识不知道从哪开始"},
        {"t": "总是想家，这正常吗？", "d": "怕自己这样是不是太不独立了", "v": "总是想家这正常吗"},
    ],
    "objectives": [
        "能说出过渡期里常见的变化可以分成三类：环境变了、关系要重建、节奏要重排",
        "会用变化盘点与应对台，把八条变化分进三个位置，并为每一条配一个具体做法",
        "能说出想家和不习惯在过渡期里是正常的，并知道哪些事该给时间、哪些事可以找人帮忙",
        "能为自己的过渡期写出一张准备卡，上面有一条变化、一个做法、一个可以联系的人",
    ],
    "objectives_plain": [
        "能说出过渡期的变化可以分成三类",
        "会用变化盘点与应对台，把八条变化分进三栏并各配一个做法",
        "能说出想家与不习惯是正常的，知道哪些给时间、哪些找人帮忙",
        "能为过渡期写出一张准备卡：一条变化、一个做法、一个可以联系的人",
    ],
    "standards": [
        {"content": "逐步适应生活和社会的各种变化，为走向社会做好心理准备",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》高中 · 生活适应"},
        {"content": "树立远大理想，培养社会责任意识",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》高中 · 生活适应"},
    ],
    "prereqs": ["psych-h-g12-career-choice"],
    "prereqs_name": "生涯规划与升学择业",
    "prereqs_meta": "psych-h-g12-career-choice",
    "leads_to": ["psych-h-g12-mental-literacy"],
    "next_meta": "psych-h-g12-mental-literacy",
    "section_images": ["assets/psych-h-g12-life-transition-fig1.webp", "assets/psych-h-g12-life-transition-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "那种说不上来的不对劲，其实有名字——先把变化拆开看。",
        "problem-anchor": "先定一个小目标：这节课结束时，你有一张三栏清单和一张过渡准备卡。",
        "objectives": "看清四件事：变化的三类、三栏怎么分、适应的节奏、准备卡怎么写。",
        "pretest": "凭现在的想法选就好，不打分。前测只是帮你看清自己怎么看这段过渡。",
        "module-1": "变的三类：环境变了、关系要重建、节奏要重排。",
        "lab-1": "每条变化先选一个位置，再配一个具体做法；右边三栏会实时汇总。",
        "module-2": "想家是正常的，不必马上适应，关系重建急不来。",
        "lab-2": "六件事各选一个时间点，全部排完会看到一段小结。",
        "worked-example": "五步：盘点、分类、配做法、告诉相关的人、定检查点。",
        "conceptest-1": "三个选项里藏着最常见的几个误解，选完请把每条解释读一遍。",
        "synthesis": "三步都选好，这里会生成一句属于你的过渡准备卡。",
        "posttest": "第一个晚上、一次家里的电话、一次回看，三个新情境看看方法还在不在。",
        "summary": "记住三个词：拆开看、分三栏、慢慢来。",
        "homework": "三层练习，前两层做完就算通关，第三层留给愿意更进一步的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先帮你找到卡点，再给一个最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是高中「生活适应」板块里长期空缺的一课。高三学生即将进入毕业升学、离家住校这类真实转折，最需要的是把「不适应」这件事正常化，并拿到可操作的做法。全课先把变化拆成三类——环境变了、关系要重建、节奏要重排；核心模拟是「变化盘点与应对台」，八条关于变化的具体描述（作息要自己安排、老同学不在身边、三餐时间要自己定、想家、重新交朋友、遇到麻烦要自己找人问、钱要自己算、旧习惯不在了）每条先分进「我能掌控的 / 需要时间的 / 要找人帮忙的」三栏，再从九个做法里挑一个配上，三个栏位实时汇总，反馈一律用温和的「这样可能会……，还可以试试……」。第二个台子「适应时间线对照台」把六件事排到头三天、第二到四周、两个月以后，帮学生建立合理的时间预期。综合任务用「过渡准备卡生成台」落成一句话：一条变化、一个做法、一个可以联系的人、一个回看时间。全课明确写出想家是正常的、不必马上适应、不适应不等于适应能力差，语气温和、不评判、不贴标签，只讲能自己动手做的事。",
    "plan_table": """| 1 | cover | 人生过渡与社会适应：变化来了，一条一条安顿 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：你怎么看这段时间的变化？ | 起·前测（暴露现有想法） |
| 5 | concept | 过渡期里变的，其实是三类东西 | 承·概念一（环境 / 关系 / 节奏） |
| 6 | interactive | 核心模拟：变化盘点与应对台 | 承·核心模拟（八条变化 × 三栏 → 三栏汇总） |
| 7 | concept | 想家是正常的，不必马上适应 | 承·概念二（三句话 + 适应的时间过程） |
| 8 | interactive | 对照台：适应的节奏可以怎么排？ | 承·练习台（六件事 → 头三天 / 第二到四周 / 两个月后） |
| 9 | concept | 例题示范：离家两周，找回节奏 | 转·重难点突破（五步走一遍） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：过渡准备卡生成台 | 合·落成一句话 |
| 12 | quiz | 后测：换几个新情境，看看方法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把这段过渡讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：变的是三类、分进三栏、慢慢来 三栏\n- P5 变化三类示意图（已生成）：三个圆角卡片配抽象几何符号（房子轮廓、连接的圆点、日历）\n- P7 适应时间过程示意图（已生成）：带刻度的路径与三个时间标记，中性扁平插画\n- 若需补充：一张可打印的三栏空白清单、一张过渡准备卡空白模板",
}
