# -*- coding: utf-8 -*-
"""高中 · 心理健康 · 心理素养与终身发展（高三）—— 补齐知识树「抗挫与适应」空缺

铁规：语气温和、不评判、不贴标签；通篇使用日常语言，只讲可操作的做法。
本课只讲可以长期用的心理素养与可操作做法，不做自我评价或自我判断类工具。
需要帮助时明确指向「学校的心理老师或正规医疗机构」。
核心模拟：日常自我关照清单生成台——四个维度里各挑做法 → 选一个做的时机 → 生成一张清单。
另含：靠谱信息识别台（六条内容 → 专业渠道 / 需要再看看 / 流量内容）
      + 边界一句话练习（五句常见难开口的话 → 选出能说出口又不伤关系的那一句）。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/psych-h-g12-mental-literacy-fig1.webp'
F2 = './assets/psych-h-g12-mental-literacy-fig2.webp'

TTS = {
    "hero": "有一件事，越早学会越好，可是很少有人正式教过。那就是怎么照顾自己——不是那种励志口号，而是一些很小、很具体、可以一直用下去的做法。这节课讲四件事。第一件，认识自己的情绪和需要：难受的时候，先给这种感觉起个名字，再看看它背后想要的是什么。第二件，会求助：知道什么时候开口，也知道跟谁说。第三件，会休息：把休息当成一件正经事，而不是等撑不住了才允许自己停。第四件，会设定边界：知道哪些事可以说我需要想一想、这次不行。我们还会做一件事，就是学着分清楚，网上那些看起来很懂你的心理测试，哪些可以当娱乐，哪些根本不能当依据。",
    "problem-anchor": "在开始之前，先选出最贴近你最近状态的一项。是不会照顾自己的情绪，是很难开口找人帮忙，是休息的时候有负罪感，还是总被别人推着走、说不出口不行。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出可以长期用的四件心理素养分别是什么，并各举一个具体的做法。第二，会用日常自我关照清单生成台，从四个维度里各挑做法，生成一张自己能照着做的清单。第三，能用三个问题分辨一份网上的心理测试或科普内容：谁写的、有没有出处、是不是为了让你转发。第四，能说出需要帮助时可以找谁，并写出一句自己说得出口的求助话。",
    "pretest": "先做三道小题，凭你现在的习惯选就行，没有对错，也不打分。选完会立刻出现解释，正好帮你看清自己现在怎么照顾自己。",
    "module-1": "先把可以长期用的四件事说清楚。第一件，认识自己的情绪和需要。做法很朴素：难受的时候先别急着评价自己，先给这种感觉起个名字，是着急、是委屈、还是累；起完名字，再看看它背后想要什么——是被听见、是歇一会儿，还是想把话说清楚。第二件，会求助。求助不是把问题丢给别人，而是把「我遇到了什么」和「我需要什么」说明白。第三件，会休息。休息不是把时间花掉，它是让你还能继续做下去的东西，所以要提前安排，而不是等到撑不住了才允许自己停。第四件，会设定边界。边界不是把人推开，而是把你能给的部分说清楚：这件事我可以，那件事我需要想一想。这四件事都不复杂，难的是记住它们可以用一辈子。",
    "lab-1": "现在打开日常自我关照清单生成台。四个维度里，每个都挑一到两条你愿意试试的做法，再选一个做的时机。台面会把你挑的整理成一张清单。请留意，这张清单不是任务表，挑两条就够，做不到也没关系，它只是给你一个可以照着做的小起点。",
    "module-2": "接着要说一件很实际的事：网上的心理内容和心理测试太多，怎么分辨。你大概见过那种三题测出你的性格、点进去还要分享到几个群的测试。它们不算有害，当娱乐看一看没什么，但有一件事要清楚：它们给不了你关于自己的结论。分辨的方法只有三个问题。第一，这是谁写的，能不能找到作者和出处。第二，它有没有依据，是随口一说还是引了可以查的来源。第三，它是不是在推动你转发或者付费。三个问题里只要有一个答不上来，就先当成娱乐内容，别拿它当依据。真正需要帮助的时候，可以找学校的心理老师聊一次，也可以到正规医疗机构问一次——这两条路都是正规的，去找人本身就是一种能力。",
    "lab-2": "下面有六条你大概刷到过的内容，每条选一个判断：专业渠道、需要再看看、流量内容。选完会给出解释。请留意，说它是流量内容，不是说它在骗你，而是说它给的东西还不足以让你拿它来判断自己。",
    "worked-example": "我们完整走一遍。假设有一位同学，最近总觉得时间不够用，一停下来就有点慌。第一步，先给感觉起名字：不是笼统的累，而是心里悬着、放不下。第二步，找它背后的需要：他想要的是把该做的事收个尾，而不是一直开着。第三步，为自己选一个具体的做法：每天睡前一小时把第二天要做的三件事写下来，写完就合上本子。第四步，配上一个求助对象：如果连续两周还是悬着，就找班主任或学校心理老师聊一次，先说清自己的状态，再说需要什么。第五步，设一条自己的边界：晚上十一点以后，群里的事第二天再看。第六步，定一个回看时间：两周后看看哪一条真的做下来了。",
    "conceptest-1": "现在用三个容易弄混的说法考考你。请仔细读每一个选项，选出你认为更合适的那个，然后看解释。",
    "synthesis": "最后练一练怎么说出口。下面有五句话，是很多人想设边界时最难开口的那几句。每一句给你三个说法，选出最可能说出口、又不伤关系的那一个。选完会给出解释。",
    "posttest": "最后换几个新情境检验一下。这次的问题出现在一次深夜的消息里、一张网上的测试结果里，还有一次你想找人帮忙的时候。",
    "summary": "这节课我们弄明白了三件事。第一，可以长期用的四件事：认识自己的情绪与需要、会求助、会休息、会设定边界。它们不复杂，难的是记住它们能用一辈子。第二，分辨网上的心理内容只要三个问题：谁写的、有没有出处、是不是为了让你转发；答不上来就先当娱乐。第三，需要帮助的时候有正规的路：学校的心理老师，或者正规医疗机构。最后把要求放低一点：这些做法不是要把你变成另一个人，只是让你在不好过的时候，多几个可以用的办法。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出四件可以长期用的心理素养，并为每一件举一个具体做法。第二层能力应用，动手做：用清单生成台做一张自己的清单，再找一条网上的心理内容用三个问题分辨一次。第三层迁移挑战，选做：把清单真正执行两周，两周后回看一次哪一条做下来了，并给一位朋友写一句你愿意在他的边界上配合的话。",
    "knowledge-graph": "这张图展示了这节课在知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续想的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 可以长期用的四件事", "lab-1": "核心模拟 日常自我关照清单生成台",
    "module-2": "概念二 分辨网上的心理内容", "lab-2": "识别台 六条内容怎么分辨",
    "worked-example": "例题示范", "conceptest-1": "概念测试",
    "synthesis": "综合任务 边界一句话练习", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

CUSTOM_JS = r"""
/* ============================================================
   psych-h-g12-mental-literacy 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 核心模拟：日常自我关照清单生成台（四个维度各挑做法 → 选时机 → 生成清单）
   3) 靠谱信息识别台（六条内容 → 专业渠道 / 需要再看看 / 流量内容）
   4) 边界一句话练习（五句难开口的话 → 选出能说出口的一句）
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

  /* ---------- 2. 核心模拟：日常自我关照清单生成台 ---------- */
  var DIMS = [
    { k: 'emo', n: '一、认识自己的情绪与需要', tip: '难受的时候，先给它起个名字，再看它想要什么',
      items: ['先说一句现在心里是什么感觉', '写下它背后想要的是什么', '问自己这件事急不急', '把感觉说给一个人听'] },
    { k: 'ask', n: '二、会求助', tip: '把「我遇到了什么」和「我需要什么」说明白',
      items: ['想好先跟谁说这件事', '先说清自己现在的状态', '直接说出你需要什么帮助', '约一个具体的时间聊'] },
    { k: 'rest', n: '三、会休息', tip: '休息要提前安排，不是撑不住了才允许自己停',
      items: ['每天留一段不安排任何事的时间', '睡前半小时不看消息', '每周安排一件只为自己做的事', '累了就先停十分钟再继续'] },
    { k: 'edge', n: '四、会设定边界', tip: '边界是把你能给的说清楚，不是把人推开',
      items: ['先说我可以做的那一部分', '用我需要想一想往后挪一挪', '约定消息在什么时间之后不回', '拒绝的时候给一个替代时间'] }
  ];
  var WHEN = ['每天早上', '每天睡前', '每个周末'];
  var litPick = {};
  var litWhen = '';
  DIMS.forEach(function (d) { litPick[d.k] = {}; });
  var litStage = document.getElementById('lit-stage');
  if (litStage) {
    function renderLit() {
      litStage.innerHTML = DIMS.map(function (d) {
        var chips = d.items.map(function (t, j) {
          return '<button class="choice' + (litPick[d.k][j] ? ' selected' : '') +
            '" data-lit-dim="' + d.k + '" data-lit-item="' + j +
            '" style="text-align:left;font-size:13px;padding:10px 14px">' + t + '</button>';
        }).join('');
        return '<div class="inner-card"><p style="margin:0 0 4px"><strong>' + d.n + '</strong></p>' +
          '<p style="margin:0 0 8px;color:var(--muted);font-size:13px">' + d.tip + '</p>' +
          '<div class="grid grid-2" style="gap:6px">' + chips + '</div></div>';
      }).join('') +
        '<div class="inner-card"><p style="margin:0 0 8px"><strong>这张清单你打算什么时候看</strong></p>' +
        '<div class="grid grid-3" style="gap:6px">' + WHEN.map(function (w) {
          return '<button class="choice' + (litWhen === w ? ' selected' : '') +
            '" data-lit-when="' + w + '" style="text-align:center;font-size:13px;padding:10px 8px">' + w + '</button>';
        }).join('') + '</div></div>';

      litStage.querySelectorAll('[data-lit-item]').forEach(function (b) {
        b.addEventListener('click', function () {
          var k = b.dataset.litDim, j = b.dataset.litItem;
          litPick[k][j] = !litPick[k][j];
          renderLit();
        });
      });
      litStage.querySelectorAll('[data-lit-when]').forEach(function (b) {
        b.addEventListener('click', function () { litWhen = b.dataset.litWhen; renderLit(); });
      });

      var total = 0, dimsCovered = 0;
      DIMS.forEach(function (d) {
        var n = Object.keys(litPick[d.k]).filter(function (j) { return litPick[d.k][j]; }).length;
        total += n;
        if (n > 0) dimsCovered++;
      });
      var out = document.getElementById('lit-out');
      out.style.display = 'block';
      if (total === 0) {
        out.className = 'result warn';
        out.innerHTML = '<strong>先从四个维度各挑一条试试。</strong>' +
          '不必都挑满，一条就够开始——这张清单的重点不是数量，是它真的能照着做。';
      } else if (!litWhen) {
        out.className = 'result warn';
        out.innerHTML = '<strong>已经挑了 ' + total + ' 条，覆盖 ' + dimsCovered + '/4 个维度。</strong>' +
          '再选一个看的时机，清单就完整了。';
      } else {
        var groups = DIMS.filter(function (d) {
          return Object.keys(litPick[d.k]).some(function (j) { return litPick[d.k][j]; });
        }).map(function (d) {
          var items = Object.keys(litPick[d.k]).filter(function (j) { return litPick[d.k][j]; })
            .map(function (j) { return d.items[parseInt(j, 10)]; });
          return d.n.replace(/^[一二三四]、/, '') + '：' + items.join('；');
        });
        out.className = 'result';
        out.innerHTML = '<strong>你的日常自我关照清单（' + litWhen + '看一次）：</strong><br>' +
          groups.join('<br>') +
          '<br><span style="color:var(--muted);font-size:14px">做到两条就算这张清单有用。' +
          (dimsCovered < 4 ? '还没挑的维度不用急，过一阵子再加也可以。' : '') +
          '</span>';
      }
    }
    renderLit();
  }

  /* ---------- 3. 靠谱信息识别台 ---------- */
  var LBL = { pro: '专业渠道', wait: '需要再看看', flow: '流量内容' };
  var INFO = [
    { t: '一条短视频说，三道题就能测出你的心理年龄。', a: 'flow',
      pro: '三道题要给出关于你的结论，依据太少了。',
      wait: '可以先看看它有没有写出依据在哪里。',
      flow: '题目太少、结论又很绝对、也没有出处——当娱乐看看就好，不能拿来判断自己。' },
    { t: '学校心理老师发的一份情绪记录方法说明。', a: 'pro',
      pro: '这是学校心理老师给的公开方法说明，属于正规渠道，可以拿来用。',
      wait: '这类材料可以直接用，遇到不清楚的地方再问一句就好。',
      flow: '这是学校的正规材料，不是流量内容，丢掉有点可惜。' },
    { t: '一个没有署名、没有出处的测试网页，做完要求你分享到三个群。', a: 'flow',
      pro: '没有署名和出处的测试，谈不上专业渠道。',
      wait: '在找不到作者和出处之前，先别把它当依据。',
      flow: '没有出处，还要求你转发——这两条加起来，它更像是在做传播，不是在讲心理。' },
    { t: '正规医疗机构官网上的一篇科普文章。', a: 'pro',
      pro: '这是正规医疗机构发布的公开科普，属于可以查阅的渠道。',
      wait: '这类文章可以放心读，有不明白的地方还可以去问一次。',
      flow: '正规医疗机构的官网文章，是可以拿来当依据的。' },
    { t: '同学转来的一篇文章，讲得挺有道理，但没写作者是谁。', a: 'wait',
      pro: '内容有道理，但作者和出处都查不到，还不能直接当专业渠道。',
      wait: '可以先记下来，等找到作者和出处再决定要不要当真。',
      flow: '也不必急着当成流量内容——先把作者和出处找出来再看。' },
    { t: '学校组织的一次心理健康讲座的记录。', a: 'pro',
      pro: '学校组织的讲座属于正规渠道，记录里的做法可以直接试一试。',
      wait: '这类记录可以直接用，有疑问的地方可以去问讲过的老师。',
      flow: '这是学校正规组织的讲座，不是流量内容。' }
  ];
  var infoStage = document.getElementById('info-stage');
  if (infoStage) {
    function renderInfo() {
      infoStage.innerHTML = INFO.map(function (c, i) {
        var btns = ['pro', 'wait', 'flow'].map(function (k) {
          var cls = 'choice';
          if (c.picked === k) cls += (k === c.a ? ' correct' : ' wrong');
          return '<button class="' + cls + '" data-info="' + i + '" data-info-pick="' + k +
            '" style="text-align:center;font-size:12px;padding:10px 6px">' + LBL[k] + '</button>';
        }).join('');
        return '<div class="inner-card" style="padding:12px 14px;margin:8px 0">' +
          '<p style="margin:0 0 8px;font-size:15px"><strong>' + (i + 1) + '. ' + c.t + '</strong></p>' +
          '<div class="grid grid-3" style="gap:6px">' + btns + '</div>' +
          (c.picked ? '<p class="result ' + (c.picked === c.a ? '' : 'warn') + '" style="margin:8px 0 0">' +
            (c.picked === c.a ? '<strong>这个判断挺合适。</strong>' : '<strong>还可以再想想：</strong>') +
            c[c.picked] + '</p>' : '') +
          '</div>';
      }).join('');
      infoStage.querySelectorAll('[data-info]').forEach(function (b) {
        b.addEventListener('click', function () {
          var i = parseInt(b.dataset.info, 10);
          if (INFO[i].picked) return;
          INFO[i].picked = b.dataset.infoPick;
          renderInfo();
          var done = INFO.filter(function (x) { return x.picked; }).length;
          var out = document.getElementById('info-out');
          out.style.display = 'block';
          out.className = 'result' + (done >= 6 ? '' : ' warn');
          out.innerHTML = '<strong>已判断 ' + done + '/6 条。</strong>' +
            '三个问题：谁写的、有没有出处、是不是为了让你转发。三个里有一个答不上来，就先当娱乐内容。' +
            '真正需要帮助的时候，走正规的路——学校的心理老师，或者正规医疗机构。' +
            (done >= 6 ? '<br>六条都判断完了。你可以回头看看，有没有哪一条是你以前会直接当真的。' : '');
        });
      });
    }
    renderInfo();
  }

  /* ---------- 4. 边界一句话练习 ---------- */
  var EDGE = [
    { q: '同学让你帮他把整份作业做一遍。',
      o: [['你自己做吧，别老想着靠别人。', 0, '这句话把事和人都否了。边界说清了，但关系也跟着冷了。'],
          ['我可以给你讲讲卡住的那两道，整份我没法替你写。', 1, '说清了能给的部分和不能给的部分，两个都在，对方知道你愿意帮。'],
          ['行吧，我帮你写。', 0, '这一次过去了，但下次他还会来找你，你心里的那点堵也还在。']] },
    { q: '已经很晚了，群里还在@你。',
      o: [['这么晚还发，有没有点分寸。', 0, '说的是人，对方先要为自己辩解，事情往后拖。'],
          ['这条我明天早上回你，先说一声免得你等。', 1, '给了明确时间，还先安抚了对方，最容易被接受。'],
          ['装作没看见。', 0, '不说清楚，对方不知道你在不在，下次还会一直发。']] },
    { q: '一位朋友总在深夜找你聊很久，你第二天很累。',
      o: [['我陪你可以，但十一点以后我要睡了，白天找我吧。', 1, '说的是时间和条件，不是拒绝这个人。他仍然知道你愿意在。'],
          ['我最近很忙，你找别人吧。', 0, '边界说清了，但话说得像推人，对方容易以为你不想理他。'],
          ['硬撑着陪，第二天自己难受。', 0, '这一次撑过去了，但撑不了很久，最后往往是一次突然的爆发。']] },
    { q: '你不想参加一个周末的聚会长途活动。',
      o: [['我不去了，你们玩。', 0, '意思到了，但没给理由也没给替代方案，容易被追问。'],
          ['这次我不太想去，下次近一点的一起去。', 1, '说清这次不行，也给出了下一次，把门留着。'],
          ['答应了，然后当天临时说有事。', 0, '这样对方会觉得被放鸽子，比直接说更伤关系。']] },
    { q: '有人反复问你一件你不想说的事。',
      o: [['这不关你的事。', 0, '边界竖起来了，同时把关系推远了。'],
          ['这事我现在还不想说，等我想说的时候再告诉你。', 1, '说的是自己的状态，不是对方的错，也留了以后的余地。'],
          ['编一个理由糊过去。', 0, '理由要一直维持，下次还得再编一个。']] }
  ];
  var edgeStage = document.getElementById('edge-stage');
  if (edgeStage) {
    function renderEdge() {
      edgeStage.innerHTML = EDGE.map(function (c, i) {
        var opts = c.o.map(function (o, j) {
          var cls = 'choice';
          if (c.picked === j) cls += (o[1] ? ' correct' : ' wrong');
          return '<button class="' + cls + '" data-edge="' + i + '" data-edge-pick="' + j +
            '" style="font-size:13px;padding:10px 14px">' + o[0] + '</button>';
        }).join('');
        return '<div class="inner-card" style="padding:12px 14px;margin:8px 0">' +
          '<p style="margin:0 0 8px;font-size:15px"><strong>' + (i + 1) + '. ' + c.q + '</strong></p>' +
          '<div class="grid" style="gap:6px">' + opts + '</div>' +
          (c.picked !== undefined ? '<p class="result ' + (c.o[c.picked][1] ? '' : 'warn') +
            '" style="margin:8px 0 0">' + (c.o[c.picked][1] ? '<strong>这一句能说出口，也不太伤关系。</strong>' :
            '<strong>还可以再想想：</strong>') + c.o[c.picked][2] + '</p>' : '') +
          '</div>';
      }).join('');
      edgeStage.querySelectorAll('[data-edge]').forEach(function (b) {
        b.addEventListener('click', function () {
          var i = parseInt(b.dataset.edge, 10);
          if (EDGE[i].picked !== undefined) return;
          EDGE[i].picked = parseInt(b.dataset.edgePick, 10);
          renderEdge();
          var done = EDGE.filter(function (x) { return x.picked !== undefined; }).length;
          var out = document.getElementById('edge-out');
          out.style.display = 'block';
          out.className = 'result' + (done >= 5 ? '' : ' warn');
          out.innerHTML = '<strong>已选 ' + done + '/5 句。</strong>' +
            '好的边界说法通常有三样：说清这次能给的、给出一个替代的、把话说在事情上而不是人身上。' +
            (done >= 5 ? '<br>五句都选完了。你可以挑一句最贴近你最近情况的，改写成你自己的说法。' : '');
        });
      });
    }
    renderEdge();
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：你平时怎么照顾自己？", TTS["pretest"], [
        {"q": "心里有点堵，但说不上来怎么了。下面哪种做法更贴近「认识自己的情绪与需要」？",
         "options": [("先给这种感觉起个名字，再看它背后想要的是什么", True),
                     ("先别想它，等它自己过去", False),
                     ("告诉自己这不算什么事，别太矫情", False)],
         "explain": "起名字是让模糊的感觉变得可以处理的第一步，再看它想要什么，就知道能做什么。<strong>错因提醒：</strong>常见错误是误认为不去看就等于没事——感觉不会因为不被看就消失，它只会换一种方式出现。"},
        {"q": "关于「会求助」，下面哪种说法更合适？",
         "options": [("求助是把「我遇到了什么」和「我需要什么」说明白", True),
                     ("求助就是把问题交给别人，越省事越好", False),
                     ("能自己扛就不要求助，求助是能力不够的表现", False)],
         "explain": "把状态和需要说清楚，别人才能真正帮上忙。<strong>错因提醒：</strong>容易把「求助」搞混成「给别人添麻烦」——说清楚之后，大多数人其实很愿意帮。"},
        {"q": "网上那种三道题测出你性格的测试，下面哪种看法更合适？",
         "options": [("当娱乐看一看可以，但不能拿它的结果来判断自己", True),
                     ("测出来的结果挺准的，可以当参考依据", False),
                     ("这类测试都是骗人的，看都不该看", False)],
         "explain": "它给不了关于你的结论，但也不必因此紧张。<strong>错因提醒：</strong>误认为测试结果等于对自己的判断，容易用一个随机的标签把自己框住。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "可以长期用的，是这四件事", TTS["module-1"], f'''
        <p style="font-size:17px;margin:0 0 12px">这四件事不复杂，也不需要什么条件。难的是记住它们可以用一辈子。</p>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgb(var(--warm-rgb) / .45)">
          <p style="margin:0"><strong>为什么要先学这个？</strong>你已经知道要好好照顾自己；<strong>但</strong>这句话太大，落到具体的一天里常常不知道做什么；<strong>所以</strong>把它拆成四件具体的事，每件配一个能立刻做的做法。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>认识自己的情绪与需要：</strong>难受的时候先给它起个名字——是着急、是委屈、还是累；再看它背后想要什么。</div></div>
          <div class="step"><span class="n">2</span><div><strong>会求助：</strong>把「我遇到了什么」和「我需要什么」说明白，而不是把问题丢出去。</div></div>
          <div class="step"><span class="n">3</span><div><strong>会休息：</strong>休息要提前安排，而不是等到撑不住了才允许自己停。它是让你还能继续的东西。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>会设定边界：</strong>把你能给的部分说清楚——这件事我可以，那件事我需要想一想。边界不是把人推开。</div></div>
        </div>
        <div class="kid-note"><span class="emoji">🧰</span><div><strong>这四件事可以一起用：</strong>先认出感觉，再看需要什么；需要别人搭把手的部分就说出来；撑不住之前先安排休息；对超出你能给的部分，说清这次不行。</div></div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">误认为会休息就是不够努力，会设边界就是不合群。其实这两件事做得好的人，往往能更久地做下去，关系也不容易积怨。</p>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="可以长期用的四件事示意图：认识情绪与需要、会求助、会休息、会设定边界">
          <figcaption>四件可以长期用的事：认识情绪与需要、会求助、会休息、会设定边界</figcaption>
        </figure>
{insight_box([
    {"lens": "解释它", "text": "为什么给情绪起个名字有用？因为模糊的感觉最难处理。起了名字之后，它就从一团东西变成了一个可以回应的信号。"},
    {"lens": "比较它", "text": "「会休息」和「不上进」看起来像同一件事，差别在于前者是安排好的，后者是撑不住之后的塌下来。"},
    {"lens": "迁移它", "text": "这四件事不只在高中有用。以后上大学、工作、成家，遇到的还是这些题目，只是场景换了。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lit", 5, "lab-1", "核心模拟：日常自我关照清单生成台", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">四个维度里，每个挑一到两条你愿意试的做法，再选一个看的时机。挑两条就够，做不到也没关系。</p>
        <div class="lab-panel" id="lit-stage"></div>
        <p class="result warn" id="lit-out" style="margin-top:12px"></p>
        <div class="inner-card">
          <p><strong>把清单抄下来：</strong>抄在一张纸上，或者存进手机备忘录。两周以后回看一次，只问一句：哪一条我真的做下来了？</p>
          <textarea id="lit-answer" rows="3" placeholder="我打算每天睡前看一次，先做的两条是……" style="margin-top:8px"></textarea>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧰</span><div><strong>这张清单不是任务表。</strong>它只是给你一个可以照着做的小起点。如果有些时候你觉得撑得比较久，或者睡觉、吃饭、上课都明显受影响，可以找学校的心理老师聊一次，也可以到正规医疗机构问一次——去找人本身就是一种能力。</div></div>
    ''', tag="核心模拟", bloom="apply"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "网上的心理内容，用三个问题分辨", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">网上的心理内容太多，学会分辨比记住内容更重要。分辨只需要三个问题。</p>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="分辨网上心理内容的三个问题示意图：谁写的、有没有出处、是不是为了让你转发">
          <figcaption>三个问题：谁写的、有没有出处、是不是在推动你转发或付费</figcaption>
        </figure>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>这是谁写的？</strong>能不能找到作者和出处。找不到作者的测试和文章，先当娱乐内容看。</div></div>
          <div class="step"><span class="n">2</span><div><strong>有没有出处？</strong>它是随口给结论，还是引了可以自己查的来源。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>是不是在推动你转发或付费？</strong>如果内容的主要目的是传播或者推销，要格外留一分。</div></div>
        </div>
        <div class="kid-note"><span class="emoji">🔎</span><div><strong>三个问题里，有一个答不上来就先放一放。</strong>这不代表它在骗你，只说明它给的东西还不足以让你拿它来判断自己。</div></div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">误认为看到一条对得上的描述就说明自己就是这样的人。描述能对上，往往因为它写得足够宽——这也正是它不能当依据的原因。</p>
        </div>
        <div class="inner-card">
          <p><strong>需要帮助的时候，请走正规的路：</strong>学校的心理老师，或者正规医疗机构。这两条路都是正规且常见的，去找人本身就是一种照顾自己的能力。</p>
        </div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "info", 7, "lab-2", "识别台：六条内容，怎么分辨？", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">六条你大概刷到过的内容，每条选一个判断。选完会给出解释——说它是流量内容，不是说它在骗你。</p>
        <div class="lab-panel" id="info-stage"></div>
        <p class="result warn" id="info-out" style="display:none;margin-top:12px"></p>
        <div class="inner-card">
          <p><strong>写下来，留给自己：</strong>最近有一条让你对号入座的内容吗？写下它，再用三个问题给自己一个判断。</p>
          <textarea id="info-answer" rows="3" placeholder="我看到的内容是……；它是不是写了作者……；它有没有出处……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="动手实验室", bloom="evaluate"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：一停下来就有点慌，怎么办", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgb(var(--warm-rgb) / .45)">
          <p style="margin:0"><strong>情境：</strong>一位同学说，最近总觉得时间不够用，一停下来心里就有点慌，说不上到底在慌什么。我们陪他走一遍。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先给感觉起个名字：</strong>不是笼统的累，是心里悬着、放不下。名字起出来，就好办了。</div></div>
          <div class="step"><span class="n">2</span><div><strong>找它背后想要什么：</strong>他想要的是把该做的事收个尾，而不是一直开着。</div></div>
          <div class="step"><span class="n">3</span><div><strong>选一个具体的做法：</strong>每天睡前一小时，把第二天要做的三件事写下来，写完就合上本子。</div></div>
          <div class="step"><span class="n">4</span><div><strong>配上一个求助对象：</strong>如果连续两周还是悬着，就找班主任或学校心理老师聊一次，先说清状态，再说需要什么。</div></div>
          <div class="step"><span class="n green">5</span><div><strong>设一条自己的边界：</strong>晚上十一点以后，群里的事第二天再看。</div></div>
          <div class="step"><span class="n">6</span><div><strong>定一个回看时间：</strong>两周后看看哪一条真的做下来了。做下来一条就算有用。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">两个方向都容易走偏：一种是<strong>一次性给自己定七八条</strong>，两天后全部放弃；另一种是<strong>觉得必须先全部想通才能开始</strong>。中间那条路是：一次只加一条，做下来了再加下一条。</p>
        </div>
        <div class="inner-card">
          <p><strong>把期待放在合适的位置：</strong>这套做法不是要把你变成另一个人，也不保证每天都顺利。它能做到的是：在不好过的时候，多几个可以用的办法。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "「休息就是浪费时间，等忙完这一阵再好好歇」——这句话最需要改的地方是：",
         "options": [("它把休息放到忙完之后，可忙完往往一直没有来", True),
                     ("它说得太绝对了，应该加一个也许", False),
                     ("它没有说清楚休息具体要休息多久", False)],
         "explain": "休息需要提前安排，而不是等撑不住了才允许自己停。<strong>错因提醒：</strong>常见错误是误认为休息是可以往后挪的奖励——挪到最后，常常是身体先替你停下来。"},
        {"q": "关于「会求助」，下面哪种理解更合适？",
         "options": [("先说清自己的状态，再直接说出需要什么帮助", True),
                     ("先说自己多惨，让人不好意思不帮", False),
                     ("求助就是把问题交出去，之后不用管了", False)],
         "explain": "说清状态加需要，别人才能真正搭上手。<strong>错因提醒：</strong>容易把「求助」搞混成「抱怨」——前者有明确的需要，后者说完之后双方都还是原地不动。"},
        {"q": "你刷到一条内容，把某种性格描述得特别像你。下面哪种反应更合适？",
         "options": [("先看一下是谁写的、有没有出处，再决定要不要当依据", True),
                     ("描述得这么准，说明就是这样", False),
                     ("直接转发给同学，让大家都测一测", False)],
         "explain": "能对上，常常是因为描述写得足够宽。<strong>错因提醒：</strong>误认为对得上就等于准确——一个能套住大多数人的描述，恰恰说明它不能用来判断单独的某个人。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "edge", 10, "synthesis", "综合任务：边界一句话练习", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">五句最难开口的话，每句选一个说法。留意哪一种能说出口，又不至于把关系推远。</p>
        <div class="lab-panel" id="edge-stage"></div>
        <p class="result warn" id="edge-out" style="display:none;margin-top:12px"></p>
        <div class="inner-card">
          <p><strong>写下来，留给自己：</strong>挑一句最贴近你最近情况的，改成你自己的说法写在这里。一句就够。</p>
          <textarea id="syn-answer" rows="3" placeholder="我可以说：这次我可以……，但……；或者，我需要想一想，……" style="margin-top:8px"></textarea>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🛡️</span><div><strong>最后一句提醒：</strong>设边界不是变冷漠，是让关系可以长久地维持下去。如果有些时候你自己也觉得撑得比较久，记得还有学校的心理老师和正规医疗机构这两条正规的路可以走。</div></div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，看看方法还在不在", TTS["posttest"], [
        {"q": "深夜十一点半，同学发来一条很长的消息，想找你说说话。你明天一早有事。下面哪种做法更合适？",
         "options": [("先说一句看到了，说明天早上回，并问他是不是着急", True),
                     ("不理他，等明天再说", False),
                     ("硬撑着陪他聊到很晚，第二天自己很难受", False)],
         "explain": "给一个明确的时间，同时问一句急不急，两边都照顾到了。<strong>错因提醒：</strong>常见错误是误认为边界和关心只能二选一——说清时间恰恰让关心变得可持续。"},
        {"q": "你最近总是觉得有点悬着，睡觉和吃饭都受了影响。下面哪种做法更合适？",
         "options": [("找学校的心理老师聊一次，或者到正规医疗机构问一次", True),
                     ("上网搜几个测试，自己测一测看是什么情况", False),
                     ("再撑一撑，等过去这段时间就好了", False)],
         "explain": "去找正规渠道是一种能力，不需要先把事情说得多严重才配去。<strong>错因提醒：</strong>容易把「再撑一撑」搞混成「坚强」——撑久了再找人，往往要多花好几倍的力气。"},
        {"q": "朋友请你帮忙做一件事，你这次确实做不了。下面哪种说法更合适？",
         "options": [("这次我做不了，下周三之后可以，你看行不行", True),
                     ("我最近特别忙，你找别人吧", False),
                     ("答应下来，到时候再说做不了", False)],
         "explain": "说清这次不行，同时给一个可以的时间。<strong>错因提醒：</strong>误认为拒绝一定要彻底，或者答应了再推掉更省事——后者往往比直接说更伤关系。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把这份素养讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>四件事可以用一辈子</strong>：认识情绪与需要、会求助、会休息、会设定边界；每件都有能立刻做的做法。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>分辨内容问三句</strong>：谁写的、有没有出处、是不是为了让你转发；答不上来就先当娱乐。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>需要帮助有正规的路</strong>：学校的心理老师，或者正规医疗机构；去找人本身就是一种能力。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgb(var(--warm-rgb) / .45)">
          <p style="margin:0"><strong>回到开头那个说不上来的时刻：</strong>当你觉得有点堵、又说不清怎么了，不必先解决它。先给它起个名字，再看它想要什么——能做的第一件事，往往就从这里出现。</p>
        </div>
        <div class="inner-card">
          <p><strong>记忆锚点：</strong>三个词帮你记住这节课——<strong>先起名、会开口、留边界</strong>。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「先起名、会开口、留边界」这三个词，把自己清单里最先想做的那一条讲给一位同学听。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "写出可以长期用的四件心理素养，并为每一件举一个具体做法。",
            "写出分辨网上心理内容的三个问题，每句话用一句话说清在问什么。",
            "用自己的话说明休息为什么需要提前安排，写两到三句。",
        ],
        [
            "用日常自我关照清单生成台做一张自己的清单，抄下来，并写下你打算什么时候看它。",
            "找一条你最近刷到的心理内容，用三个问题分辨一次，写下你的判断和理由。",
        ],
        [
            "把清单真正执行两周，两周后回看一次，写下哪一条做下来了、哪一条想换掉。",
            "给一位朋友写一句话，说明你愿意在他的哪一条边界上配合；如果你需要帮助，写出你打算找谁、第一句话准备怎么说。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "psych-h-g12-mental-literacy",
    "node_id": "psych-h-g12-mental-literacy",
    "subject": "psychology",
    "subject_cn": "心理健康",
    "stage": "high",
    "stage_cn": "高中",
    "curriculum": "中小学心理健康教育指导纲要（2012年修订）/ 教育部相关要求 · 高中",
    "title": "心理素养与终身发展：四件事，可以用一辈子",
    "name_en": "Mental Health Literacy for Lifelong Development",
    "grade": 12,
    "grade_cn": "高三",
    "domain": "resilience",
    "domain_cn": "抗挫与适应",
    "lesson_type": "workshop",
    "version": "1.0.0",
    "description": "面向高三学生的心理素养与终身发展课：讲四件可以长期用的心理素养——认识自己的情绪与需要（先给感觉起个名字，再看它背后想要什么）、会求助（把遇到了什么和需要什么说明白）、会休息（提前安排，而不是撑不住了才允许自己停）、会设定边界（把能给的部分说清楚）。核心模拟是「日常自我关照清单生成台」，从四个维度各挑一到两条做法并选一个执行时机，台面整理成一张可以照着做的清单；第二个台子是「靠谱信息识别台」，用谁写的、有没有出处、是不是为了让你转发三个问题分辨六条常见的网上内容。综合任务用「边界一句话练习」把难开口的五句话改成能说出口又不伤关系的说法。全课不做自我评价或自我判断类工具，明确指向需要帮助时找学校心理老师或正规医疗机构；语气温和、不评判、不贴标签，只讲能自己动手做的事。",
    "tags": ["心理素养", "终身发展", "情绪与需要", "会求助", "会休息", "设定边界", "信息分辨", "高三"],
    "standard_ref": "《中小学心理健康教育指导纲要（2012年修订）· 高中》抗挫与适应——形成积极心理品质，掌握心理保健常识和技能；具备自主自助维护心理健康的能力，促进终身发展。",
    "hero_question": "有什么东西学会了，可以一直用下去？",
    "hero_alt": "心理素养知识结构图三栏：认识自己、会求助与会休息、分辨靠不靠谱的信息",
    "hero_caption": "认识自己 · 会求助会休息 · 分辨信息——四件事可以用一辈子",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个最贴近你最近状态的困惑，后面的内容都会围着它展开。",
    "anchor_choices": [
        {"t": "说不清自己到底怎么了", "d": "心里有点堵，但讲不明白是什么", "v": "说不清自己到底怎么了"},
        {"t": "想找人帮忙，但开不了口", "d": "怕麻烦别人，也怕说出来显得自己不行", "v": "想找人帮忙但开不了口"},
        {"t": "休息的时候总觉得有负罪感", "d": "一停下来就慌，好像应该一直忙着", "v": "休息的时候总觉得有负罪感"},
        {"t": "总被别人推着走，说不出不行", "d": "答应了又后悔，不答应又怕生分", "v": "总被别人推着走说不出不行"},
    ],
    "objectives": [
        "能说出可以长期用的四件心理素养分别是什么，并各举一个具体的做法",
        "会用日常自我关照清单生成台，从四个维度里各挑做法，生成一张自己能照着做的清单",
        "能用三个问题分辨一份网上的心理测试或科普内容：谁写的、有没有出处、是不是为了让你转发",
        "能说出需要帮助时可以找谁，并写出一句自己说得出口的求助话",
    ],
    "objectives_plain": [
        "能说出四件可以长期用的心理素养，并各举一个做法",
        "会用清单生成台做出一张能照着做的自我关照清单",
        "能用三个问题分辨网上的心理测试与科普内容",
        "能说出需要帮助时可以找谁，并写出一句说得出口的求助话",
    ],
    "standards": [
        {"content": "形成积极心理品质，掌握心理保健常识和技能",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》高中 · 抗挫与适应"},
        {"content": "具备自主自助维护心理健康的能力，促进终身发展",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》高中 · 抗挫与适应"},
    ],
    "prereqs": ["psych-h-g12-life-transition"],
    "prereqs_name": "人生过渡与社会适应",
    "prereqs_meta": "psych-h-g12-life-transition",
    "leads_to": [],
    "next_meta": "",
    "section_images": ["assets/psych-h-g12-mental-literacy-fig1.webp", "assets/psych-h-g12-mental-literacy-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "有一件事越早学会越好，却很少有人正式教过——怎么照顾自己。",
        "problem-anchor": "先定一个小目标：这节课结束时，你有一张自我关照清单和一句说得出口的求助话。",
        "objectives": "看清四件事：四件素养、清单怎么做、信息怎么分辨、需要帮助找谁。",
        "pretest": "凭平时的习惯选就好，不打分。前测只是帮你看清自己现在怎么照顾自己。",
        "module-1": "四件事：认识情绪与需要、会求助、会休息、会设定边界。",
        "lab-1": "四个维度各挑一到两条，再选一个看的时机，清单就生成了。",
        "module-2": "分辨三问：谁写的、有没有出处、是不是为了让你转发。",
        "lab-2": "六条内容各选一个判断，全部判断完会看到一段小结。",
        "worked-example": "六步：起名、找需要、配做法、配找人、设边界、定回看。",
        "conceptest-1": "三个选项里藏着最常见的几个误解，选完请把每条解释读一遍。",
        "synthesis": "五句话各选一个说法，全部选完会看到一段小结。",
        "posttest": "一次深夜消息、一次想找人帮忙、一次拒绝，三个新情境看看方法还在不在。",
        "summary": "记住三个词：先起名、会开口、留边界。",
        "homework": "三层练习，前两层做完就算通关，第三层留给愿意更进一步的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先帮你找到卡点，再给一个最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是高中「抗挫与适应」板块里长期空缺的一课，也是这一段的收尾课——把前面几课里零散出现的做法，收成四件可以长期用的心理素养。全课只讲可操作的做法，不讲大道理，也刻意不做自我评价或自我判断类工具。第一件是认识自己的情绪与需要：先给感觉起个名字，再看它背后想要什么。第二件是会求助：把遇到了什么和需要什么说明白。第三件是会休息：提前安排，而不是撑不住了才允许自己停。第四件是会设定边界：把能给的部分说清楚。核心模拟是「日常自我关照清单生成台」，四个维度各给四条具体做法候选，学生每个维度挑一到两条、再选一个执行时机，台面立刻整理成一张可以照着做的清单，并且只挑两条也算完成。第二个台子「靠谱信息识别台」用六条常见的网上内容，练三个问题：谁写的、有没有出处、是不是在推动你转发或付费。综合任务「边界一句话练习」把五句最难开口的话改成能说出口又不伤关系的说法。全课明确写出需要帮助时可以走的两条正规路径——学校心理老师与正规医疗机构，并在多处强调去找人本身就是一种能力；语气温和、不评判、不贴标签，不出现任何诊断性表述，不涉及自伤自杀与暴力情节。",
    "plan_table": """| 1 | cover | 心理素养与终身发展：四件事，可以用一辈子 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：你平时怎么照顾自己？ | 起·前测（暴露现有习惯） |
| 5 | concept | 可以长期用的，是这四件事 | 承·概念一（认识需要 / 求助 / 休息 / 边界） |
| 6 | interactive | 核心模拟：日常自我关照清单生成台 | 承·核心模拟（四维度挑做法 → 生成清单） |
| 7 | concept | 网上的心理内容，用三个问题分辨 | 承·概念二（谁写的 / 出处 / 是否推转发）+ 正规路径 |
| 8 | interactive | 识别台：六条内容，怎么分辨？ | 承·练习台（六条内容 → 专业渠道 / 再看看 / 流量内容） |
| 9 | concept | 例题示范：一停下来就有点慌，怎么办 | 转·重难点突破（六步走一遍） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：边界一句话练习 | 合·把话说成能说出口的那一种 |
| 12 | quiz | 后测：换几个新情境，看看方法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把这份素养讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：认识自己、会求助会休息、分辨信息 三栏\n- P5 四件素养示意图（已生成）：四个圆角卡片配抽象符号（对话气泡、相连的两点、暂停键、虚线边框）\n- P7 三个分辨问题示意图（已生成）：署名标签、放大镜、循环箭头划掉，中性扁平插画\n- 若需补充：一张可打印的自我关照清单空白模板、一张正规求助路径提示卡",
}
