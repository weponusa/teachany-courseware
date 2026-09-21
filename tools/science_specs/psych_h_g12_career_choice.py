# -*- coding: utf-8 -*-
"""高中 · 心理健康 · 生涯规划与升学择业（高三）—— 补齐知识树「生涯规划」空缺

铁规：语气温和、不评判、不贴标签；通篇使用日常语言，只讲可操作的做法。
本课只讲探索方法和信息核实，不替学生定方向：
  · 不做任何学校排名、不做专业热度推销、不做薪资导向的择业引导
  · 落点是「可以先探索、允许改变」
核心模拟：三圈交集探索台——把若干条关于自己的描述分别放进兴趣 / 能力 / 价值三个圈
          （可同时属于多个圈），台面实时画出三圆交集，看出交集在哪里、哪些地方对不上。
另含：信息来源核实台（六条常见说法 → 主要依据 / 需要再核对 / 不能作为依据）
      + 下一步行动卡生成台（挑交集 → 选了解方式 → 定回看时间）。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/psych-h-g12-career-choice-fig1.webp'
F2 = './assets/psych-h-g12-career-choice-fig2.webp'

TTS = {
    "hero": "高三这一年，教室里最常出现的一句话大概是：你想好了吗。可是想好了什么，有时候自己也说不清。这节课不替你做决定，也不会告诉你哪条路更好走。我们只做三件事。第一件，把你自己摊开看一看：做什么事的时候你会忘了时间，做什么事你上手比较快，还有什么是你心里真正在意的。第二件，把这三个圈放进同一个台面上，看它们的交集在哪里，也看它们对不上的地方。第三件，学一套核实信息的办法，因为关于升学的说法实在太多，其中有一些是站不住的。最后会说到一件事：现在看到的这个交集不是结论，它只是你此刻的一个线索，以后可以改。",
    "problem-anchor": "在开始之前，先选出最贴近你最近状态的一项。是分不清自己到底喜欢什么，还是担心现在选的以后会用不上，又或者是听来的说法太多，不知道能信哪一个。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出兴趣、能力、价值三个圈各自问的是什么问题，并为自己的每个圈写下至少两条。第二，会用三圈交集探索台，把若干条关于自己的描述放进三个圈，看清交集在哪里、哪些地方对不上。第三，能说出专业和职业不是一一对应的关系，并用三个问题去核实一条关于升学的说法。第四，能为自己的交集写出一句可以先试的方向，并说明你打算什么时候回来看一看。",
    "pretest": "先做三道小题，凭你现在的想法选就行，没有对错，也不打分。选完会立刻出现解释，正好帮你看清自己现在习惯怎么判断。",
    "module-1": "我们先把三个圈各自问的问题分清楚。兴趣圈问的是：做什么的时候你会觉得时间过得快，做完了还愿意再来一次。能力圈问的是：做什么的时候你上手比较快，做完之后自己心里有底。价值圈问的是：什么事对你来说算重要——是做出来的东西真的帮到了别人，还是这件事足够扎实、靠得住，又或者是你有自己能安排的时间。这三个圈问的是不一样的问题，所以答案对不上，很正常。请留意一点：兴趣说的是此刻的倾向，不是天赋；能力说的是现在能做的事，不是天花板。它们都会变。",
    "lab-1": "现在打开三圈交集探索台。左边有九条关于自己的描述，每一条都可以放进你觉得合适的圈里，也可以同时放进两个圈甚至三个圈。放的时候凭第一感觉，不必反复权衡。右边会实时画出三个圈，出现交集的地方会亮起来。请留意，这个台面不判断对错，它只是把你现在的判断摆出来给你看。",
    "module-2": "第二件要说清楚的事是：专业和职业不是一一对应的关系。同一个专业出来的同学，后来做的事可能差别很大；反过来，同一类工作，进来的人也来自很多不同的专业。所以选专业更像是选一条你愿意先走几年的路，而不是给一辈子定型。既然不是一一对应，那些关于升学的说法就更要核实。核实只需要问三句话。第一句，这是谁说的，他有没有直接的依据。第二句，依据是什么，有没有公开的来源可以自己查。第三句，有没有第二个来源能对上——只有一个来源的说法，先放一放。",
    "lab-2": "下面有六条你大概听过的说法，每一条选一个判断：可以作为主要依据，需要再核对，或者不能作为依据。选完会给出解释。请留意，说某条说法不能作为依据，不是说讲这句话的人在骗你，而是说它给的信息还不够支撑你拿它做决定。",
    "worked-example": "我们完整走一遍。假设有一位同学，兴趣圈里写的是喜欢把复杂的东西讲清楚给别人听；能力圈里写的是整理资料和写东西比较顺；价值圈里写的是希望做出来的东西真的对别人有用。第一步，三个圈并排看：三个圈里同时出现的是「把事情讲清楚」和「对别人有用」。第二步，看对不上的地方：他喜欢讲清楚，但暂时不喜欢长时间独自做研究——这一条不用急着改，记下来就好。第三步，把交集写成一句可以先试的方向：去做一件需要把信息整理清楚再讲给别人听的事。第四步，去核实：这条方向对应哪些学习内容、哪些课程会练到，用三个问题去查。第五步，定一个回看的时间，比如一个月以后，问自己还愿不愿意做。",
    "conceptest-1": "现在用三个容易弄混的说法考考你。请仔细读每一个选项，选出你认为更合适的那个，然后看解释。",
    "synthesis": "最后一步，把探索变成一个具体动作。从你放出的交集里挑一到两条最想先了解的，再选一种了解的方式，最后定一个回看的时间。选完会生成一句话，你可以抄下来带在身边。",
    "posttest": "最后换几个新情境检验一下。这次的问题出现在一条短视频里、一次家里的饭桌对话里，还有一次你要给自己写一句话的时候。",
    "summary": "这节课我们弄明白了三件事。第一，兴趣、能力、价值三个圈问的是不一样的问题：做着有意思、做起来顺手、心里觉得重要。第二，专业和职业不是一一对应的，核实一条说法只要三句话：谁说的、依据是什么、有没有第二个来源。第三，交集只是此刻的一个线索，不是结论。最后把要求放低一点：不必现在就找到那个唯一正确的方向，你只要愿意继续探索、也允许自己改变，就已经走在路上了。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写下三个圈各自问的问题，并为自己的每个圈写两条。第二层能力应用，动手做：完成一次三圈交集探索台，把交集抄下来，再挑一条关于升学的说法用三个问题核实一遍。第三层迁移挑战，选做：把交集写成一句可以先试的方向，找一位你信得过的人聊二十分钟，一个月后回看一次自己还愿不愿意做。",
    "knowledge-graph": "这张图展示了这节课在知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续想的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 三个圈问的是不同的问题", "lab-1": "核心模拟 三圈交集探索台",
    "module-2": "概念二 专业与职业不是一一对应", "lab-2": "核实台 一条说法怎么查",
    "worked-example": "例题示范", "conceptest-1": "概念测试",
    "synthesis": "综合任务 下一步行动卡", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

CUSTOM_JS = r"""
/* ============================================================
   psych-h-g12-career-choice 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 核心模拟：三圈交集探索台（九条描述 × 三个圈 → canvas 三圆交集）
   3) 信息来源核实台（六条说法 → 主要依据 / 需要再核对 / 不能作为依据）
   4) 下一步行动卡生成台（挑交集 → 选了解方式 → 定回看时间）
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

  /* ---------- 2. 三圈交集探索台 ---------- */
  var TRENDS = [
    '一个人琢磨一个问题的答案，能坐得住',
    '把一件事讲清楚给别人听，觉得有意思',
    '动手装配或者做手工的时候，手比较稳',
    '看到数字和图表，不觉得费劲',
    '写东西的时候，能把话说顺',
    '组织一群人的时候，知道谁适合做什么',
    '做的事真的帮到了别人，这件事对我重要',
    '东西做出来要扎实、靠得住，这件事对我重要',
    '有自己能安排的时间，这件事对我重要'
  ];
  var CIRCLES = [
    { k: 'i', n: '兴趣圈', q: '做着有意思' },
    { k: 'a', n: '能力圈', q: '做起来顺手' },
    { k: 'v', n: '价值圈', q: '心里觉得重要' }
  ];
  /* 三圆几何：r=95，圆心 (215,130) / (305,130) / (260,215) */
  var GEO = {
    'iav': [260, 150], 'ia': [260, 95], 'iv': [185, 185],
    'av': [335, 185], 'i': [160, 100], 'a': [360, 100], 'v': [260, 295]
  };
  var vennState = TRENDS.map(function () { return { i: false, a: false, v: false }; });
  var vennCanvas = document.getElementById('venn-canvas');
  if (vennCanvas) {
    var vctx = vennCanvas.getContext('2d');

    function drawVenn() {
      var W = vennCanvas.width, H = vennCanvas.height;
      vctx.clearRect(0, 0, W, H);
      var cs = [[215, 130], [305, 130], [260, 215]];
      var cols = ['96,165,250', '167,139,250', '251,191,36'];
      for (var c = 0; c < 3; c++) {
        vctx.beginPath();
        vctx.arc(cs[c][0], cs[c][1], 95, 0, Math.PI * 2);
        vctx.fillStyle = 'rgba(' + cols[c] + ',0.13)';
        vctx.fill();
        vctx.lineWidth = 2;
        vctx.strokeStyle = 'rgba(' + cols[c] + ',0.75)';
        vctx.stroke();
      }
      vctx.font = '700 15px -apple-system, "PingFang SC", sans-serif';
      vctx.textAlign = 'center';
      vctx.fillStyle = 'rgba(96,165,250,1)';
      vctx.fillText('兴趣圈', 215, 26);
      vctx.fillStyle = 'rgba(167,139,250,1)';
      vctx.fillText('能力圈', 305, 26);
      vctx.fillStyle = 'rgba(251,191,36,1)';
      vctx.fillText('价值圈', 260, 336);
      /* 按归属组合分区 */
      var region = {};
      vennState.forEach(function (s, idx) {
        var key = (s.i ? 'i' : '') + (s.a ? 'a' : '') + (s.v ? 'v' : '');
        if (!key) return;
        region[key] = region[key] || [];
        region[key].push(idx);
      });
      /* 交集区块高亮 */
      Object.keys(region).forEach(function (key) {
        if (key.length < 2) return;
        var p = GEO[key];
        if (!p) return;
        vctx.beginPath();
        vctx.arc(p[0], p[1], 10 + Math.min(region[key].length, 4) * 4, 0, Math.PI * 2);
        vctx.fillStyle = 'rgba(34,197,94,0.16)';
        vctx.fill();
        vctx.strokeStyle = 'rgba(34,197,94,0.55)';
        vctx.lineWidth = 1.5;
        vctx.stroke();
      });
      /* 每一条描述画一个点 */
      Object.keys(region).forEach(function (key) {
        var p = GEO[key];
        if (!p) return;
        region[key].forEach(function (idx, n) {
          var dx = (n % 3) * 11 - 11, dy = Math.floor(n / 3) * 11 - 5;
          vctx.beginPath();
          vctx.arc(p[0] + dx, p[1] + dy, 5, 0, Math.PI * 2);
          vctx.fillStyle = key.length >= 2 ? 'rgba(34,197,94,0.95)' : 'rgba(148,163,184,0.85)';
          vctx.fill();
        });
      });
      /* 交集计数 */
      var inter = vennState.filter(function (s) {
        return (Number(s.i) + Number(s.a) + Number(s.v)) >= 2;
      }).length;
      vctx.textAlign = 'left';
      vctx.font = '700 13px -apple-system, "PingFang SC", sans-serif';
      vctx.fillStyle = 'rgba(34,197,94,0.95)';
      vctx.fillText('落在两个圈以上：' + inter + ' 条', 12, H - 10);
    }

    var renderVenn = function () {
      var bank = document.getElementById('venn-bank');
      bank.innerHTML = TRENDS.map(function (t, i) {
        var btns = CIRCLES.map(function (c) {
          return '<button class="choice' + (vennState[i][c.k] ? ' selected' : '') +
            '" data-venn-item="' + i + '" data-venn-circle="' + c.k +
            '" style="text-align:center;font-size:12px;padding:8px 4px">' + c.n + '</button>';
        }).join('');
        return '<div class="inner-card" style="padding:10px 12px;margin:8px 0">' +
          '<p style="margin:0 0 8px;font-size:14px">' + (i + 1) + '. ' + t + '</p>' +
          '<div class="grid grid-3" style="gap:6px">' + btns + '</div></div>';
      }).join('');
      bank.querySelectorAll('[data-venn-item]').forEach(function (b) {
        b.addEventListener('click', function () {
          var i = parseInt(b.dataset.vennItem, 10);
          var k = b.dataset.vennCircle;
          vennState[i][k] = !vennState[i][k];
          renderVenn();
        });
      });
      var placed = vennState.filter(function (s) { return s.i || s.a || s.v; }).length;
      var inter = vennState.filter(function (s) {
        return (Number(s.i) + Number(s.a) + Number(s.v)) >= 2;
      }).length;
      var out = document.getElementById('venn-out');
      out.style.display = 'block';
      out.className = 'result' + (inter >= 2 ? '' : ' warn');
      if (placed === 0) {
        out.innerHTML = '<strong>还没有放进任何一条。</strong>先挑两三条你最有感觉的，点一下它下面的圈名就行。' +
          '放错了也没关系，再点一下就能取出来。';
      } else if (inter < 2) {
        out.innerHTML = '<strong>已经放进 ' + placed + ' 条，暂时还没有两条落在同一个位置上。</strong>' +
          '可以想一想：有没有哪一条描述，其实既是你喜欢的，也是你做起来顺手的？';
      } else {
        out.innerHTML = '<strong>已经放进 ' + placed + ' 条，其中 ' + inter + ' 条落在两个圈以上（绿色亮点）。</strong>' +
          '绿色区域里的这几条，就是你此刻的交集。它不保证什么，只是一条可以继续看的线索。' +
          '那些只落在一个圈里的，也一样有用——它们告诉你哪里还对不上，这件事不用急着解决。';
      }
      drawVenn();
    };
    renderVenn();
  }

  /* ---------- 3. 信息来源核实台 ---------- */
  var SRC = [
    { t: '一条短视频说，某个方向以后一定好就业。',
      a: 'no',
      ok: '它只给了结论，没有说自己是从哪里知道的，也没有给出可以查的来源。',
      mid: '先记下它提到的信息，再去找公开来源对照。',
      no: '这句话可以作为线索，但不能作为依据——它没有说清依据是什么。先去查公开来源，再决定要不要信。' },
    { t: '省级考试院公布的选考科目要求文件。',
      a: 'yes',
      ok: '这是公开的官方文件，能直接查到原文，可以拿它当主要依据。',
      mid: '这类文件可以当主要依据，注意看清是哪一年的版本。',
      no: '这类公开的官方文件，正是最该拿来当依据的那一种。' },
    { t: '一位学长讲他自己读这个方向的真实经历。',
      a: 'mid',
      ok: '他的经历是真的，但只有一个人、一个角度，可以当参考。',
      mid: '这是很值得听的一手经验，但它是一个人的一次经历，可以当参考，不急着当结论。',
      no: '把一个人的真实经历直接丢掉，有点可惜。它不能替你做决定，但能让你看到一种可能。' },
    { t: '一个培训机构的老师说，报这个方向包你以后不愁。',
      a: 'no',
      ok: '这句话和他要不要你报名有关系，而且包你以后不愁这件事本身无法验证。',
      mid: '可以先问他依据是什么，看看他能不能给出可以自己查的来源。',
      no: '当一句话和说话人的收益有关，又无法验证时，它就不能作为你决定的依据。' },
    { t: '一张网上的热度排行榜，没有说明数据从哪里来。',
      a: 'no',
      ok: '没说数据来源的排行榜，看不出它是怎么算出来的，无法核对。',
      mid: '可以看看它有没有写清楚数据来源；写清楚了再看。',
      no: '没有数据来源的排行榜，只能说明有人在讨论这件事，不能说明它适合你。' },
    { t: '学校发的招生章程和专业介绍册。',
      a: 'yes',
      ok: '这是学校自己发布的公开材料，内容可以去原件上核对。',
      mid: '这类公开材料可以当主要依据，遇到关键信息再回原件核一遍更稳。',
      no: '学校自己的公开材料，是可以拿来当依据的。' }
  ];
  var LABELS = { yes: '可以作为主要依据', mid: '需要再核对', no: '不能作为依据' };
  var srcStage = document.getElementById('src-stage');
  if (srcStage) {
    function renderSrc() {
      srcStage.innerHTML = SRC.map(function (c, i) {
        var btns = ['yes', 'mid', 'no'].map(function (k) {
          var cls = 'choice';
          if (c.picked === k) cls += (k === c.a ? ' correct' : ' wrong');
          return '<button class="' + cls + '" data-src="' + i + '" data-src-pick="' + k +
            '" style="text-align:center;font-size:12px;padding:10px 6px">' + LABELS[k] + '</button>';
        }).join('');
        return '<div class="inner-card" style="padding:12px 14px;margin:8px 0">' +
          '<p style="margin:0 0 8px;font-size:15px"><strong>' + (i + 1) + '. ' + c.t + '</strong></p>' +
          '<div class="grid grid-3" style="gap:6px">' + btns + '</div>' +
          (c.picked ? '<p class="result ' + (c.picked === c.a ? '' : 'warn') + '" style="margin:8px 0 0">' +
            (c.picked === c.a ? '<strong>这个判断挺合适。</strong>' : '<strong>还可以再想想：</strong>') +
            c[c.picked] + '</p>' : '') +
          '</div>';
      }).join('');
      srcStage.querySelectorAll('[data-src]').forEach(function (b) {
        b.addEventListener('click', function () {
          var i = parseInt(b.dataset.src, 10);
          if (SRC[i].picked) return;
          SRC[i].picked = b.dataset.srcPick;
          renderSrc();
          var done = SRC.filter(function (x) { return x.picked; }).length;
          var out = document.getElementById('src-out');
          out.style.display = 'block';
          out.className = 'result' + (done >= 6 ? '' : ' warn');
          out.innerHTML = '<strong>已判断 ' + done + '/6 条。</strong>' +
            '三句话帮你筛：谁说的、依据是什么、有没有第二个来源能对上。' +
            (done >= 6 ? '<br>六条都判断完了。你可以回头看看，有没有哪一条是你以前会直接信的。' : '');
        });
      });
    }
    renderSrc();
  }

  /* ---------- 4. 下一步行动卡生成台 ---------- */
  var WAYS = ['读一份公开的招生章程或选考科目要求', '找一位学长聊二十分钟',
    '试听一节相关方向的课或讲座', '做一个小的动手项目试试',
    '问一位相关科目的老师', '去学校图书馆翻一本相关的入门书'];
  var WHEN = ['一个月后', '这学期结束前', '下一个长假结束前'];
  var genPick = { items: {}, way: '', when: '' };
  var genStage = document.getElementById('gen-stage');
  if (genStage) {
    function chosenTrends() {
      var out = [];
      TRENDS.forEach(function (t, i) {
        var s = vennState[i];
        if (!s) return;
        if ((Number(s.i) + Number(s.a) + Number(s.v)) >= 2) out.push([i, t]);
      });
      return out;
    }
    function renderGen() {
      var pool = chosenTrends();
      var head = pool.length ? '你在探索台里放出的交集有 ' + pool.length + ' 条，挑一到两条最想先了解的：'
        : '还没有交集也不要紧。下面是全部九条描述，挑一到两条你最想先弄清楚的：';
      var poolUse = pool.length ? pool : TRENDS.map(function (t, i) { return [i, t]; });
      var itemBtns = poolUse.map(function (p) {
        return '<button class="choice' + (genPick.items[p[0]] ? ' selected' : '') +
          '" data-gen-item="' + p[0] + '" style="font-size:13px;padding:10px 14px;text-align:left">' +
          p[1] + '</button>';
      }).join('');
      var wayBtns = WAYS.map(function (w) {
        return '<button class="choice' + (genPick.way === w ? ' selected' : '') +
          '" data-gen-way="' + w + '" style="font-size:13px;padding:10px 14px">' + w + '</button>';
      }).join('');
      var whenBtns = WHEN.map(function (w) {
        return '<button class="choice' + (genPick.when === w ? ' selected' : '') +
          '" data-gen-when="' + w + '" style="font-size:13px;padding:10px 14px;text-align:center">' + w + '</button>';
      }).join('');
      genStage.innerHTML =
        '<div class="inner-card"><p style="margin:0 0 8px"><strong>第一步 · 挑交集</strong></p>' +
        '<p style="margin:0 0 8px;color:var(--muted);font-size:14px">' + head + '</p>' +
        '<div class="grid" style="gap:6px">' + itemBtns + '</div></div>' +
        '<div class="inner-card"><p style="margin:0 0 8px"><strong>第二步 · 选一种了解的方式</strong></p>' +
        '<div class="grid grid-2" style="gap:6px">' + wayBtns + '</div></div>' +
        '<div class="inner-card"><p style="margin:0 0 8px"><strong>第三步 · 定一个回看的时间</strong></p>' +
        '<div class="grid grid-3" style="gap:6px">' + whenBtns + '</div></div>';
      genStage.querySelectorAll('[data-gen-item]').forEach(function (b) {
        b.addEventListener('click', function () {
          var k = b.dataset.genItem;
          genPick.items[k] = !genPick.items[k];
          renderGen();
        });
      });
      genStage.querySelectorAll('[data-gen-way]').forEach(function (b) {
        b.addEventListener('click', function () { genPick.way = b.dataset.genWay; renderGen(); });
      });
      genStage.querySelectorAll('[data-gen-when]').forEach(function (b) {
        b.addEventListener('click', function () { genPick.when = b.dataset.genWhen; renderGen(); });
      });
      var picked = Object.keys(genPick.items).filter(function (k) { return genPick.items[k]; });
      var out = document.getElementById('gen-out');
      out.style.display = 'block';
      if (picked.length === 0 || !genPick.way || !genPick.when) {
        out.className = 'result warn';
        out.innerHTML = '<strong>三步都选好，这里就会生成一句话。</strong>' +
          '这句话不是承诺，只是给你自己定一个可以动手的起点。';
      } else {
        var os = picked.map(function (k) { return byIndex(k); }).filter(Boolean);
        out.className = 'result';
        out.innerHTML = '<strong>你的一句话行动卡：</strong>接下来，我先去弄清楚' +
          os.map(function (t) { return '「' + t + '」'; }).join('和') + '这件事，方式是' +
          '「' + genPick.way + '」。' + genPick.when + '，我会回来问自己一次：还愿不愿意继续做这件事。' +
          '<br><span style="color:var(--muted);font-size:14px">愿意就往前走一步，不愿意就换一条试试——' +
          '这两种结果都算探索有收获。</span>';
      }
    }
    function byIndex(k) { return TRENDS[parseInt(k, 10)]; }
    renderGen();
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：你怎么判断一个方向适不适合自己？", TTS["pretest"], [
        {"q": "关于「兴趣圈」和「能力圈」，下面哪种说法更贴近它们本来的意思？",
         "options": [("兴趣说的是此刻做起来有意思，能力说的是现在做起来比较顺手，两个都可以变", True),
                     ("兴趣就是天赋，能力就是天花板，基本定了", False),
                     ("兴趣圈和能力圈问的是同一个问题，只是叫法不同", False)],
         "explain": "两个圈问的是不一样的问题，而且都在变。<strong>错因提醒：</strong>常见错误是误认为兴趣等于天赋、能力等于上限，于是一次对不上就认定自己不行。"},
        {"q": "一位学长跟你讲了他自己读书时的真实经历。下面哪种处理方式更合适？",
         "options": [("他的经历就是我的答案，照着走就行", False),
                     ("它是很值得听的一手经验，可以当参考，但只有一个人、一个角度", True),
                     ("一个人的经历没有价值，直接跳过", False)],
         "explain": "真实的一手经验很珍贵，但它是一个人的一次经历。<strong>错因提醒：</strong>容易把「一个人的真实经历」搞混成「普遍规律」——前者是参考，后者才需要多个来源。"},
        {"q": "关于「专业」和「以后做什么」，下面哪种说法更符合实际？",
         "options": [("同一个专业出来的同学，后来做的事差别可能很大；同一类工作，进来的人也来自很多专业", True),
                     ("选专业就是给一辈子定型，选错了很难改", False),
                     ("先看哪个方向现在最热，跟着选就稳", False)],
         "explain": "专业更像是你愿意先走几年的那条路，不是一张定终身的表格。<strong>错因提醒：</strong>误认为选专业等于定终身，会让一次本来就允许调整的选择变得过分沉重。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "三个圈，问的是三个不一样的问题", TTS["module-1"], f'''
        <p style="font-size:17px;margin:0 0 12px">兴趣、能力、价值——先把它们各自在问什么分清楚，答案对不上就不奇怪了。</p>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgb(var(--warm-rgb) / .45)">
          <p style="margin:0"><strong>为什么要先学这个？</strong>你已经听过很多次「要了解自己的兴趣和能力」；<strong>但</strong>把它们混成一个问题之后，就很容易觉得哪里都不对；<strong>所以</strong>先把三个圈分开问，再看它们能不能对上。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>兴趣圈问的是——做着有意思吗。</strong>做什么的时候你会觉得时间过得快，做完了还愿意再来一次。</div></div>
          <div class="step"><span class="n">2</span><div><strong>能力圈问的是——做起来顺手吗。</strong>做什么的时候你上手比较快，做完之后自己心里有底。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>价值圈问的是——这件事对我重要吗。</strong>是帮到了别人，是做得扎实靠得住，还是留出了自己能安排的时间。</div></div>
        </div>
        <div class="kid-note"><span class="emoji">🧭</span><div><strong>留意两个「不是」：</strong>兴趣说的是此刻的倾向，不是天赋；能力说的是现在能做的事，不是上限。所以三个圈里的内容会随着经历变化，这不是不靠谱，这是正常的。</div></div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">误认为三个圈必须完全重合才算找到了方向。其实对不上的地方同样有用——它告诉你哪里还需要时间去试，而不是告诉你哪里不行。</p>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="兴趣、能力、价值三个圈各自提问的示意图：做着有意思、做起来顺手、心里觉得重要">
          <figcaption>三个圈问的是三个不一样的问题：做着有意思、做起来顺手、心里觉得重要</figcaption>
        </figure>
{insight_box([
    {"lens": "解释它", "text": "为什么三个圈分开问更有用？因为它们混在一起的时候，一次对不上就会让人觉得自己什么都行不通；分开看，问题就变成了一件可以慢慢查的事。"},
    {"lens": "比较它", "text": "「我喜欢这个」和「我做这个比较顺手」，听起来接近，其实一个是感受、一个是证据，需要不一样的方式去确认。"},
    {"lens": "迁移它", "text": "这一套不只用在升学上。以后选修课、社团、实习、换工作，都可以拿这三个圈问一遍。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "venn", 5, "lab-1", "核心模拟：三圈交集探索台", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">左边九条描述，每条点一下它下面的圈名就能放进去，也可以同时放进两三个圈。右边会实时画出交集。</p>
        <div class="lab-panel" id="venn-stage">
          <div class="grid grid-2" style="align-items:start">
            <div>
              <p style="font-weight:700;margin:0 0 6px">把这些描述放进你觉得合适的圈里</p>
              <p style="color:var(--muted);font-size:13px;margin:0 0 8px">可以多选，放错了再点一下就取出来了</p>
              <div id="venn-bank"></div>
            </div>
            <div>
              <canvas id="venn-canvas" width="520" height="356" aria-label="三圈交集探索台画布" style="display:block;width:100%;border-radius:12px;background:var(--bg-subtle);border:1px solid var(--line-subtle)"></canvas>
              <p style="color:var(--muted);font-size:13px;margin:8px 0 0">绿色亮点＝同时属于两个圈以上的描述，也就是你此刻的交集。</p>
            </div>
          </div>
          <p class="result warn" id="venn-out" style="margin-top:12px"></p>
        </div>
        <div class="inner-card">
          <p><strong>写下来，留给自己：</strong>把绿色区域里的那几条抄在一张纸上，再抄一条只落在一个圈里的——写这条是想提醒自己，对不上的地方不用急着解决。</p>
          <textarea id="venn-answer" rows="3" placeholder="我的交集是……；有一条只落在一个圈里的是……" style="margin-top:8px"></textarea>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧭</span><div><strong>这个台面不判断对错。</strong>同一条描述放进哪个圈，没有人能替你决定；放的位置只是你此刻的判断，以后可以改。</div></div>
    ''', tag="核心模拟", bloom="apply"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "专业和职业不是一一对应，所以说法要核实", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">先把这件事松开：选专业不是给一辈子定型。然后学三句话，用来筛掉靠不住的说法。</p>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="专业与职业不是一一对应的示意图：一条分叉的路标与多来源对照">
          <figcaption>一条路可以通向很多地方，一个位置也有很多人从不同的路走过来——所以说法要核实</figcaption>
        </figure>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>不是一一对应：</strong>同一个专业出来的同学，后来做的事差别可能很大；同一类工作，进来的人也来自很多不同的专业。</div></div>
          <div class="step"><span class="n">2</span><div><strong>它更像一条路：</strong>你选的是愿意先走几年的方向，路上可以调整，也可以换。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>所以说法要核实：</strong>信息越多越要问一句——它是怎么知道的。</div></div>
        </div>
        <div class="kid-note"><span class="emoji">🔎</span><div><strong>核实三句话：</strong>第一句，这是谁说的，他有没有直接的依据；第二句，依据是什么，有没有公开来源可以自己查；第三句，有没有第二个来源能对上。只有一个来源的说法，先放一放。</div></div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">误认为只要说的人很有经验或很热情就可以信。经验值得听，判断依据还得自己查一遍——这两件事不冲突，可以同时做。</p>
        </div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "src", 7, "lab-2", "核实台：一条说法该怎么查？", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">六条你大概听过的说法，每条选一个判断。选完会给出解释——说它不能作为依据，不等于说讲这话的人在骗你。</p>
        <div class="lab-panel" id="src-stage"></div>
        <p class="result warn" id="src-out" style="display:none;margin-top:12px"></p>
        <div class="inner-card">
          <p><strong>写下来，留给自己：</strong>最近有哪一条关于升学的说法，是你听过之后有点在意的？用三句话去查一查，把查到的来源写在这里。</p>
          <textarea id="src-answer" rows="3" placeholder="我听到的说法是……；它是谁说的……；我能查到的公开来源是……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="动手实验室", bloom="evaluate"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：一次完整的探索，从摊开自己到定一个回看时间", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgb(var(--warm-rgb) / .45)">
          <p style="margin:0"><strong>情境：</strong>一位同学把三个圈都填了一遍，却发现里面有几条对不上，一时不知道该怎么办。我们陪他走一遍。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>三个圈并排看：</strong>兴趣圈写的是喜欢把复杂的东西讲清楚；能力圈写的是整理资料和写东西比较顺；价值圈写的是希望做出来的东西对别人有用。同时出现在两个圈以上的是「讲清楚」和「对别人有用」。</div></div>
          <div class="step"><span class="n">2</span><div><strong>也看对不上的地方：</strong>他喜欢讲清楚，但暂时不太喜欢长时间一个人做研究。这一条记下来就好，不用急着改。</div></div>
          <div class="step"><span class="n">3</span><div><strong>把交集写成一句可以先试的方向：</strong>去做一件需要把信息整理清楚、再讲给别人听的事。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>去核实：</strong>用三句话查——哪些学习内容会练到这件事、谁能给出一手信息、有没有第二个来源能对上。</div></div>
          <div class="step"><span class="n">5</span><div><strong>定一个回看的时间：</strong>一个月以后，回来问自己还愿不愿意做。愿意就往前一步，不愿意就换一条再试。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">两个方向都容易走偏：一种是<strong>把交集当成结论</strong>，马上认定以后只能走这一条；另一种是<strong>因为对不上就停下来</strong>，觉得还没想清楚就不能开始。前者太重，后者太慢——交集是线索，先试起来才有新的信息。</p>
        </div>
        <div class="inner-card">
          <p><strong>把期待放在合适的位置：</strong>这五步不保证一次就找到答案，也不保证试了就一定喜欢。它能做到的是：让下一步变成一件具体可做的事。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "「现在还没找到自己想做什么，所以先别动，等想清楚再说」——这句话最需要改的地方是：",
         "options": [("它把探索当成了动身之前的事，其实先试起来才会得到新的信息", True),
                     ("它太消极了，应该改成要积极一点", False),
                     ("它没有说明白到底要想清楚什么", False)],
         "explain": "探索本身就是一个边做边看的过程。<strong>错因提醒：</strong>常见错误是误认为必须先想清楚才能开始，结果把一件可以小步试的事一直往后拖。"},
        {"q": "关于「专业和职业不是一一对应」，下面哪种理解更合适？",
         "options": [("所以选专业不重要，随便选就行", False),
                     ("所以选专业更像是选一段愿意先走的路，路上可以调整", True),
                     ("所以应该先看哪个方向现在最热", False)],
         "explain": "不是一一对应，意味着这条路允许调整，也意味着不必把它想成定终身。<strong>错因提醒：</strong>容易把「不是一一对应」搞混成「怎么选都一样」——松一点不等于不用认真看。"},
        {"q": "一条说法只在一个地方看到过，别处都查不到。下面哪种处理更合适？",
         "options": [("先放一放，试着找第二个来源能不能对上", True),
                     ("说法很具体，应该就是真的", False),
                     ("既然只有一个来源，那一定是假的", False)],
         "explain": "只有一个来源，说明它还没被对上，先放一放是稳妥的做法。<strong>错因提醒：</strong>误认为只有一个来源就一定错——先放着，等对上或对不上，再决定。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "gen", 10, "synthesis", "综合任务：下一步行动卡生成台", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">三步都选好，下面会生成一句话。它不是承诺，只是给自己定一个可以动手的起点。</p>
        <div class="lab-panel" id="gen-stage"></div>
        <p class="result warn" id="gen-out" style="display:none;margin-top:12px"></p>
        <div class="inner-card">
          <p><strong>抄下来，带在身边：</strong>把生成的这句话抄在课本的第一页，或者存进手机备忘录；到了回看的时间再读一遍。</p>
          <textarea id="syn-answer" rows="3" placeholder="接下来，我先去弄清楚……，方式是……，我会在……回看一次。" style="margin-top:8px"></textarea>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🌱</span><div><strong>还有一件事想告诉你：</strong>如果试过之后发现自己不喜欢，这不是失败，这是这次探索给你的答案。可以先探索、允许改变——这两句话是这节课的全部落点。</div></div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，看看方法还在不在", TTS["posttest"], [
        {"q": "家里吃饭时，有人跟你说：这个方向以后没前途，换一个。这时更合适的回应是：",
         "options": [("先问一句他是从哪里知道的，再自己去找公开来源对一遍", True),
                     ("马上改主意，跟着换", False),
                     ("不理会，反正他们不懂", False)],
         "explain": "问一句依据是什么，是把关心变成可以查的信息。<strong>错因提醒：</strong>常见错误是误认为要么全听、要么全不听，其实可以听进去，同时自己去核对。"},
        {"q": "你做完三圈探索台，发现三个圈里有两条对不上。下面哪种做法更合适？",
         "options": [("把对不上的地方记下来，先从交集里的那几条动手试一试", True),
                     ("硬把对不上的地方改成一致，看起来舒服一点", False),
                     ("认为三个圈对不上，说明这个办法没用", False)],
         "explain": "对不上的地方是信息，不是错误。<strong>错因提醒：</strong>容易把「暂时对不上」搞混成「我有问题」——它往往只说明某一件事还没轮到你去试。"},
        {"q": "一个月后回看自己写的那句行动卡，你发现自己不太想继续了。下面哪种想法更合适？",
         "options": [("这次探索给了答案，可以换一条再来", True),
                     ("我做事没有长性，看来选什么都一样", False),
                     ("那就不再想了，等以后再急起来再说", False)],
         "explain": "试过之后知道不喜欢，本身就是收获。<strong>错因提醒：</strong>误认为放弃一次等于没有毅力——在探索阶段，换一条恰恰是往前走的方式。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把这件事讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>三个圈问三件事</strong>：做着有意思、做起来顺手、心里觉得重要；它们会变，对不上很正常。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>不是一一对应</strong>：选专业是选一条愿意先走几年的路，核实说法只要问三句话——谁说的、依据是什么、有没有第二个来源。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>交集是线索</strong>：先试起来才会拿到新信息，回看一次再决定要不要继续。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgb(var(--warm-rgb) / .45)">
          <p style="margin:0"><strong>回到开头那句「你想好了吗」：</strong>现在你可以换一个回答——我还没想完，但我有一个可以先去试的方向，也知道什么时候回来看看。这个回答就够用了。</p>
        </div>
        <div class="inner-card">
          <p><strong>记忆锚点：</strong>三个词帮你记住这节课——<strong>摊开看、对一遍、试一步</strong>。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「摊开看、对一遍、试一步」这三个词，跟一位同学说说你的交集在哪里，以及你打算先去弄清楚哪一件事。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "写出兴趣、能力、价值三个圈各自问的问题，并为自己的每个圈写下至少两条。",
            "写出核实一条说法的三句话，每句话用一句话说清在问什么。",
            "用自己的话说明为什么专业和职业不是一一对应的，举一个你听过的例子。",
        ],
        [
            "完成一次三圈交集探索台，把落在两个圈以上的描述抄下来，再抄一条只落在一个圈里的。",
            "挑一条你听过的关于升学的说法，用三句话核实一遍，写下你查到的公开来源。",
        ],
        [
            "把交集写成一句可以先试的方向，找一位你信得过的人聊二十分钟，只问信息、不请他替你决定。",
            "按行动卡里的方式去做一件具体的小事，一个月后回看一次，写下你还愿不愿意继续；换过方向的同学，写下这次换让你知道了什么。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "psych-h-g12-career-choice",
    "node_id": "psych-h-g12-career-choice",
    "subject": "psychology",
    "subject_cn": "心理健康",
    "stage": "high",
    "stage_cn": "高中",
    "curriculum": "中小学心理健康教育指导纲要（2012年修订）/ 教育部相关要求 · 高中",
    "title": "生涯规划与升学择业：先摊开看，再试一步",
    "name_en": "Career Planning and Further Study Choices",
    "grade": 12,
    "grade_cn": "高三",
    "domain": "career-planning",
    "domain_cn": "生涯规划",
    "lesson_type": "workshop",
    "version": "1.0.0",
    "description": "面向高三学生的生涯规划与升学择业课：先分清楚兴趣、能力、价值三个圈各自问的问题（做着有意思、做起来顺手、心里觉得重要），并用核心模拟「三圈交集探索台」把九条关于自己的描述分别放进三个圈，台面实时画出三圆交集，看清交集在哪里、哪些地方对不上；再讲专业与职业不是一一对应的关系，并用「核实台」练六条常见说法的来源核实，落点是三句话——谁说的、依据是什么、有没有第二个来源；最后用「下一步行动卡生成台」把交集变成一句可以动手的话，并定一个回看的时间。全课只讲探索方法与信息核实，不替学生定方向，也不做任何导向性的推荐，落点是「可以先探索、允许改变」；语气温和、不评判、不贴标签，只讲能自己动手做的事。",
    "tags": ["生涯规划", "自我探索", "三圈交集", "升学择业", "信息核实", "允许改变", "高三"],
    "standard_ref": "《中小学心理健康教育指导纲要（2012年修订）· 高中》生涯规划——充分了解兴趣、能力、性格、特长和社会需要，确立职业志向，培养职业道德意识；进行升学就业的选择和准备，培养担当意识和社会责任感。",
    "hero_question": "都说要想清楚方向，可这个「清楚」到底从哪里来？",
    "hero_alt": "生涯规划知识结构图三栏：三个圈、核实信息、先试一步",
    "hero_caption": "三个圈 · 核实信息 · 先试一步——方向是在探索里慢慢清楚的",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个最贴近你最近状态的困惑，后面的内容都会围着它展开。",
    "anchor_choices": [
        {"t": "我到底喜欢什么、擅长什么？", "d": "被问起来的时候，脑子里一片空", "v": "我到底喜欢什么、擅长什么"},
        {"t": "现在选的方向，以后会不会用不上？", "d": "怕一步走错，越想越不敢动", "v": "现在选的方向以后会不会用不上"},
        {"t": "听来的说法太多，该信哪一个？", "d": "每个人说的都不一样，越听越乱", "v": "听来的说法太多该信哪一个"},
        {"t": "想不清楚是不是就不能开始？", "d": "总觉得没想明白就动手，心里不踏实", "v": "想不清楚是不是就不能开始"},
    ],
    "objectives": [
        "能说出兴趣、能力、价值三个圈各自问的是什么问题，并为自己的每个圈写下至少两条",
        "会用三圈交集探索台，把若干条关于自己的描述放进三个圈，看清交集在哪里、哪些地方对不上",
        "能说出专业和职业不是一一对应的关系，并用三句话核实一条关于升学的说法",
        "能为自己的交集写出一句可以先试的方向，并说明打算什么时候回来看一看",
    ],
    "objectives_plain": [
        "能说出三个圈各自问的问题，并为每个圈写下至少两条",
        "会用三圈交集探索台，看清交集与对不上的地方",
        "能说出专业与职业不是一一对应，并用三句话核实说法",
        "能写出可以先试的方向，并定一个回看时间",
    ],
    "standards": [
        {"content": "充分了解兴趣、能力、性格、特长和社会需要，确立职业志向，培养职业道德意识",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》高中 · 生涯规划"},
        {"content": "进行升学就业的选择和准备，培养担当意识和社会责任感",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》高中 · 生涯规划"},
    ],
    "prereqs": ["psych-h-g11-peer-support"],
    "prereqs_name": "同伴支持与合作学习",
    "prereqs_meta": "psych-h-g11-peer-support",
    "leads_to": ["psych-h-g12-life-transition"],
    "next_meta": "psych-h-g12-life-transition",
    "section_images": ["assets/psych-h-g12-career-choice-fig1.webp", "assets/psych-h-g12-career-choice-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "方向不是一次想出来的，是边试边清楚的——先把这个念头放在心里往下看。",
        "problem-anchor": "先定一个小目标：这节课结束时，你有一句可以先试的方向和一个回看的时间。",
        "objectives": "看清四件事：三个圈各问什么、交集怎么看、说法怎么核实、下一步怎么定。",
        "pretest": "凭现在的想法选就好，不打分。前测只是帮你看清自己现在习惯怎么判断。",
        "module-1": "三个圈问三件事：做着有意思、做起来顺手、心里觉得重要。",
        "lab-1": "九条描述可以同时放进多个圈；绿色亮点就是你的交集。",
        "module-2": "专业与职业不是一一对应；核实三句话：谁说的、依据是什么、有没有第二个来源。",
        "lab-2": "六条说法各选一个判断，全部判断完会看到一段小结。",
        "worked-example": "五步：并排看、记下对不上的、写成一句方向、去核实、定回看时间。",
        "conceptest-1": "三个选项里藏着最常见的几个误解，选完请把每条解释读一遍。",
        "synthesis": "三步都选好，这里会生成一句属于你的行动卡。",
        "posttest": "饭桌对话、对不上的地方、一次回看，三个新情境看看方法还在不在。",
        "summary": "记住三个词：摊开看、对一遍、试一步。",
        "homework": "三层练习，前两层做完就算通关，第三层留给愿意更进一步的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先帮你找到卡点，再给一个最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是高中「生涯规划」板块里长期空缺的一课。高三最需要的不是被安排一个方向，而是拿到一套可以自己用的探索方法。全课只做三件事：把兴趣、能力、价值三个圈各自问的问题分清；用核心模拟「三圈交集探索台」把九条关于自己的描述分放进三个圈（支持一条同时属于多个圈），台面上的 canvas 实时画出三圆交集，落在两个圈以上的描述以绿色高亮，让学生在操作中看见交集在哪里、哪些地方对不上；再讲专业与职业不是一一对应，并用「核实台」练六条常见说法的来源判断。综合任务用「下一步行动卡生成台」把交集变成一句可以动手的话，并定一个回看时间。全课不替学生定方向，也不做任何导向性的推荐，落点明确写在「可以先探索、允许改变」；语气温和、不评判、不贴标签，只讲能自己动手做的事。",
    "plan_table": """| 1 | cover | 生涯规划与升学择业：先摊开看，再试一步 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：你怎么判断一个方向适不适合自己？ | 起·前测（暴露现有判断习惯） |
| 5 | concept | 三个圈，问的是三个不一样的问题 | 承·概念一（兴趣 / 能力 / 价值 + 两个「不是」） |
| 6 | interactive | 核心模拟：三圈交集探索台 | 承·核心模拟（九条描述 × 三个圈 → canvas 三圆交集） |
| 7 | concept | 专业和职业不是一一对应，所以说法要核实 | 承·概念二（不是一一对应 + 核实三句话） |
| 8 | interactive | 核实台：一条说法该怎么查？ | 承·练习台（六条说法 → 主要依据 / 再核对 / 不能作为依据） |
| 9 | concept | 例题示范：一次完整的探索 | 转·重难点突破（五步走一遍） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：下一步行动卡生成台 | 合·把交集变成可以动手的一句话 |
| 12 | quiz | 后测：换几个新情境，看看方法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把这件事讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：三个圈、核实信息、先试一步 三栏\n- P5 三个圈各自提问的示意图（已生成）：三个圆角卡片配抽象几何符号\n- P7 专业与职业不是一一对应的示意图（已生成）：分叉路标与多来源对照，中性扁平插画\n- 若需补充：一张可打印的三圈空白模板、一张核实三句话提示卡",
}
