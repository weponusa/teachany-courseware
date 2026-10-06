# -*- coding: utf-8 -*-
"""高中 · 心理健康 · 学习策略与考试适应（高一）—— 补齐知识树「学习辅导」空缺

铁规：语气温和、不评判、不贴标签；不出现任何临床诊断词汇，不涉及自伤自杀话题。
落点：方法可改、节奏可控。
核心模拟：复习方式对比台（同一份内容用两种方式复习 → 看一周后还记得多少）。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/psych-h-g10-learning-strategy-fig1.webp'
F2 = './assets/psych-h-g10-learning-strategy-fig2.webp'

TTS = {
    "hero": "先说说你可能遇到过的一件事。同一份笔记，你从头到尾看了三遍，考试时却怎么也想不起来；同桌只复习了两遍，反而答得很顺。这时候很多人会下结论说自己记性不好。这节课我们换一个角度看这件事：也许问题不在记性，而在复习的方式。",
    "problem-anchor": "在开始之前，先选出最贴近你的一次经历。是想知道自己为什么看过就忘，还是想知道复习时间怎么分配，又或者想要一张能照着做的考前安排表。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出为什么反复阅读容易产生看过的熟悉感，却不一定记得住。第二，能说清楚集中复习和分散复习的区别。第三，会安排一个带间隔的复习节奏。第四，能给自己的考试前后做一份可执行的节奏安排。",
    "pretest": "先做三道小题，凭你现在的习惯选就行，没有对错，也不打分。选完会立刻出现解释，正好帮你看清自己现在的做法落在哪里。",
    "module-1": "我们先把一件常被搞混的事说清楚。看着眼熟和真的记得住，其实是两件事。反复阅读会让内容变得顺眼、好读，这种熟悉感很容易被当成已经掌握了。而真正让记忆变牢的，是在需要的时候把它从脑子里取出来。每次合上书回想一遍，再翻开对答案，这个费点力气的过程，恰恰在加固记忆。心理学上把这种做法叫做提取练习。",
    "lab-1": "光听道理不够，我们做一次对比。同一份内容，用三种不同的方式复习：考前一口气连看四遍、分成四天各看一遍、分成四天并且每次先合上书回想再对答案。选一种内容，看看一周之后大概还能记得多少。数值是示意量级，重要的是三种方式之间的差距。",
    "module-2": "第二个关键是把复习摊开到时间里。一天连看四小时，和分四天各看一小时，总时长一样，效果通常差很多。原因不神秘：遗忘本来就会在两次复习之间发生，而每一次有点费劲的回想，都在把这条记忆重新加固一遍。所以复习的安排不是越集中越好，而是间隔着来更稳。常见错误是误认为一口气学完最扎实，其实那只是当下最顺。",
    "lab-2": "现在你自己来排一下节奏。左边选复习次数，右边选相邻两次复习间隔几天，下面会画出这七天里记忆保持的曲线，还会标出每次复习的位置。试一试把间隔从一天拉长到四天，看看考试当天那条线落在哪里。",
    "worked-example": "我们看一个具体的安排。小林有两周时间准备一次单元测，内容是四个小节。第一步，把内容拆开：每小节整理成一张只写问题不写答案的回忆清单。第二步，把复习摊开：第一天学第一节，第二天先花三分钟回忆第一节再学第二节，第四天回忆前两节再学第三节，第八天回忆前三节再学第四节。第三步，每次回忆时把想不起来的点记下来，形成一份自己的薄弱清单。第四步，考前两天不再从头读，只做回忆清单和薄弱清单。这样安排，两周里每一节都被回想了三到四次，而且都隔开了时间。",
    "conceptest-1": "现在用三个容易弄混的说法考考你。请仔细读每一个选项，选出你认为更合适的那个，然后看解释。",
    "synthesis": "学到这里，请你给自己排一张表。先填上你这两周要复习的内容有几块、一周里能拿出几天、距离考试还有多少天，下面会生成一份可以照着做的排程建议。看完之后再想一想：哪几天你最容易被打断，需要提前留出余地。",
    "posttest": "最后换几个新情境检验一下。这次的问题出现在早读、错题本和考场上，看看你能不能用上前面说过的思路。",
    "summary": "这节课我们弄明白了三件事。第一，看着眼熟不等于记得住，合上书回想再对答案，才真正在加固记忆。第二，复习要摊开到时间里，间隔着来比一次学完更稳。第三，考前不必从头再读一遍，拿出回忆清单和自己的薄弱清单就够。回到开头的问题：你和同桌的差别，多半不在记性，而在复习的方式。方法是可以改的，节奏是可以自己安排的。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写下你这周复习某一份内容的具体做法，并把它改成先回想再对答案。第二层能力应用，动手做：为下周的一门小测排一份带间隔的复习表，写出每次复习的具体时间。第三层迁移挑战，选做：连续七天记录自己每次复习后的真实感受，找出最适合你的复习时段和地点。",
    "knowledge-graph": "这张图展示了这节课在知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 眼熟不等于记得住", "lab-1": "对比台 复习方式对比", "module-2": "概念二 把复习摊开",
    "lab-2": "实验台 间隔复习排程", "worked-example": "例题讲解", "conceptest-1": "概念测试",
    "synthesis": "综合任务 我的两周排程", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

CUSTOM_JS = r"""
/* ============================================================
   psych-h-g10-learning-strategy 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 复习方式对比台：内容类型 × 复习方式 → 一周后保持率
   3) 间隔复习排程台：复习次数 × 间隔天数 → 保持曲线
   4) 两周排程生成器：内容块数 × 每周天数 × 距考天数
    ============================================================ */
(function () {
  'use strict';

  function cssVar(name, fallback) {
    var v = getComputedStyle(document.body).getPropertyValue(name).trim();
    return v || fallback;
  }
  var BRAND = cssVar('--brand', '#60a5fa');
  var BRAND2 = cssVar('--brand-2', '#a78bfa');
  var WARM = cssVar('--warm', '#fbbf24');
  var MUTED = cssVar('--muted', '#93a4bf');
  var LINE = cssVar('--line', '#2a3d5c');

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

  /* ---------- 2. 复习方式对比台 ---------- */
  var METHODS = [
    { k: 'mass', n: '集中复习', d: '考前一次连看四遍',
      keep: { word: 26, history: 30, formula: 24 } },
    { k: 'spaced', n: '分散复习', d: '分成四天，每天看一遍',
      keep: { word: 45, history: 52, formula: 40 } },
    { k: 'recall', n: '分散 + 先回忆', d: '分成四天，每次合上书先回想再对答案',
      keep: { word: 72, history: 76, formula: 68 } }
  ];
  var CONTENTS = {
    word: { n: '英语单词表', note: '单词的遗忘在前两天最快，所以间隔着回想特别关键。' },
    history: { n: '历史年代与事件', note: '有线索的内容更容易被回想带出来，分散复习的收益往往更明显。' },
    formula: { n: '数学公式', note: '公式光看推导容易顺眼，动手默写一遍再对照，才算真的取出来过。' }
  };
  var lab1 = document.getElementById('cmp-stage');
  if (lab1) {
    var content = 'word';
    var cv = document.getElementById('cmp-canvas');
    var ctx = cv.getContext('2d');

    function drawCompare() {
      var w = cv.width, h = cv.height;
      ctx.clearRect(0, 0, w, h);
      var padL = 44, padR = 16, padT = 18, padB = 30;
      var iw = w - padL - padR, ih = h - padT - padB;
      var colors = [MUTED, BRAND2, BRAND];
      ctx.font = '12px -apple-system, "PingFang SC", sans-serif';
      for (var g = 0; g <= 4; g++) {
        var y = padT + ih * g / 4;
        ctx.strokeStyle = LINE; ctx.globalAlpha = .6;
        ctx.beginPath(); ctx.moveTo(padL, y); ctx.lineTo(w - padR, y); ctx.stroke();
        ctx.globalAlpha = 1;
        ctx.fillStyle = MUTED; ctx.textAlign = 'right';
        ctx.fillText((100 - g * 25) + '%', padL - 6, y + 4);
      }
      var days = ['当天', '1天', '2天', '3天', '4天', '5天', '6天', '7天'];
      ctx.textAlign = 'center'; ctx.fillStyle = MUTED;
      days.forEach(function (t, i) {
        ctx.fillText(t, padL + iw * i / 7, h - padB + 18);
      });
      METHODS.forEach(function (m, mi) {
        var target = m.keep[content];
        ctx.strokeStyle = colors[mi];
        ctx.lineWidth = mi === 2 ? 2.6 : 1.6;
        ctx.beginPath();
        for (var i = 0; i <= 7; i++) {
          var decay = Math.exp(-0.55 * i);
          var boost = 0;
          if (m.k === 'spaced' && i === 2) boost = 0.14;
          if (m.k === 'spaced' && i === 5) boost = 0.10;
          if (m.k === 'recall' && i === 1) boost = 0.24;
          if (m.k === 'recall' && i === 3) boost = 0.20;
          if (m.k === 'recall' && i === 5) boost = 0.17;
          var v = Math.min(1, 0.98 * decay + boost);
          var x = padL + iw * i / 7;
          var y = padT + ih * (1 - v);
          if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }
        ctx.stroke();
      });
    }

    function renderCompare() {
      var rows = document.getElementById('cmp-rows');
      rows.innerHTML = METHODS.map(function (m) {
        var v = m.keep[content];
        return '<div style="margin:8px 0">' +
          '<div style="display:flex;justify-content:space-between;font-size:14px">' +
          '<span><strong>' + m.n + '</strong>　<span style="color:var(--muted)">' + m.d + '</span></span>' +
          '<span style="font-weight:700">' + v + '%</span></div>' +
          '<div style="height:10px;border-radius:6px;background:var(--brand-soft);margin-top:4px;overflow:hidden">' +
          '<div style="height:100%;width:' + v + '%;border-radius:6px;background:linear-gradient(90deg,var(--brand),var(--brand-2))"></div>' +
          '</div></div>';
      }).join('');
      var C = CONTENTS[content];
      var out = document.getElementById('cmp-out');
      out.className = 'result';
      out.innerHTML = '<strong>' + C.n + '　一周后大约还记得：</strong>集中复习 ' +
        METHODS[0].keep[content] + '%，分散复习 ' + METHODS[1].keep[content] + '%，分散加先回忆 ' +
        METHODS[2].keep[content] + '%。<br>' + C.note +
        '<br><span style="color:var(--muted)">这是示意量级，用来比较三种方式的差距，不是对你个人的预测。</span>';
      document.querySelectorAll('[data-cmp-content]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.cmpContent === content);
      });
      drawCompare();
    }

    document.querySelectorAll('[data-cmp-content]').forEach(function (b) {
      b.addEventListener('click', function () { content = b.dataset.cmpContent; renderCompare(); });
    });
    renderCompare();
  }

  /* ---------- 3. 间隔复习排程台 ---------- */
  var SCHED = {
    once:    { n: '只在考前一次', gaps: [], desc: '全部内容挤在考前一次看完。当时感觉最熟，一周后掉得最快。' },
    each2:   { n: '每两天复习一次', gaps: [2, 2, 2], desc: '间隔均匀，比只看一次稳很多；如果每次都能先回想再对答案，效果会再上一个台阶。' },
    expand:  { n: '间隔逐渐拉长', gaps: [1, 2, 4, 8], desc: '第一次挨得近，之后慢慢拉开。这是常被推荐的一种安排，因为越熟的内容越经得起长间隔。' }
  };
  var lab2 = document.getElementById('sched-stage');
  if (lab2) {
    var mode = 'expand';
    var cv2 = document.getElementById('sched-canvas');
    var ctx2 = cv2.getContext('2d');

    function curveAt(day, gaps) {
      var v = 1.0;
      for (var i = 0; i <= day; i++) {
        if (gaps.indexOf(i) !== -1) { v = Math.min(1, v + 0.42); }
        v = v * Math.exp(-0.30);
      }
      return Math.max(0, Math.min(1, v));
    }

    function drawSched() {
      var S = SCHED[mode];
      var w = cv2.width, h = cv2.height;
      ctx2.clearRect(0, 0, w, h);
      var padL = 44, padR = 16, padT = 18, padB = 30;
      var iw = w - padL - padR, ih = h - padT - padB;
      var span = 14;
      ctx2.font = '12px -apple-system, "PingFang SC", sans-serif';
      for (var g = 0; g <= 4; g++) {
        var y = padT + ih * g / 4;
        ctx2.strokeStyle = LINE; ctx2.globalAlpha = .6;
        ctx2.beginPath(); ctx2.moveTo(padL, y); ctx2.lineTo(w - padR, y); ctx2.stroke();
        ctx2.globalAlpha = 1;
        ctx2.fillStyle = MUTED; ctx2.textAlign = 'right';
        ctx2.fillText((100 - g * 25) + '%', padL - 6, y + 4);
      }
      ctx2.textAlign = 'center'; ctx2.fillStyle = MUTED;
      for (var d = 0; d <= span; d += 2) {
        ctx2.fillText(d === 0 ? '今天' : ('第' + d + '天'), padL + iw * d / span, h - padB + 18);
      }
      // 考试日竖线
      var examX = padL + iw * span / span;
      ctx2.strokeStyle = WARM; ctx2.setLineDash([4, 4]);
      ctx2.beginPath(); ctx2.moveTo(examX, padT); ctx2.lineTo(examX, padT + ih); ctx2.stroke();
      ctx2.setLineDash([]);
      ctx2.fillStyle = WARM; ctx2.textAlign = 'right';
      ctx2.fillText('考试当天', examX - 6, padT + 12);
      // 曲线
      ctx2.strokeStyle = BRAND; ctx2.lineWidth = 2.4;
      ctx2.beginPath();
      for (var i = 0; i <= span; i++) {
        var x = padL + iw * i / span;
        var y2 = padT + ih * (1 - curveAt(i, S.gaps));
        if (i === 0) ctx2.moveTo(x, y2); else ctx2.lineTo(x, y2);
      }
      ctx2.stroke();
      // 复习标记
      S.gaps.forEach(function (day, idx) {
        if (day > span) return;
        var x = padL + iw * day / span;
        ctx2.fillStyle = BRAND2;
        ctx2.beginPath(); ctx2.arc(x, padT + ih * (1 - curveAt(day, S.gaps)), 5, 0, Math.PI * 2); ctx2.fill();
        ctx2.fillStyle = MUTED; ctx2.textAlign = 'center';
        ctx2.fillText('复习' + (idx + 1), x, padT + ih + 4);
      });
    }

    function renderSched() {
      var S = SCHED[mode];
      var final = Math.round(curveAt(14, S.gaps) * 100);
      document.getElementById('sched-count').textContent = S.gaps.length === 0 ? '0 次' : (S.gaps.length + 1) + ' 次';
      document.getElementById('sched-keep').textContent = '约 ' + final + '%';
      var out = document.getElementById('sched-out');
      out.className = 'result' + (final < 45 ? ' warn' : '');
      out.innerHTML = '<strong>' + S.n + '：</strong>' + S.desc +
        '<br>按这个安排，到考试当天大约还能取出 <strong>' + final + '%</strong>。' +
        '<br><span style="color:var(--muted)">把复习放在被遗忘追上之前，比考前一次看完更省力，也更稳。</span>';
      document.querySelectorAll('[data-sched-mode]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.schedMode === mode);
      });
      drawSched();
    }

    document.querySelectorAll('[data-sched-mode]').forEach(function (b) {
      b.addEventListener('click', function () { mode = b.dataset.schedMode; renderSched(); });
    });
    renderSched();
  }

  /* ---------- 4. 两周排程生成器 ---------- */
  var planStage = document.getElementById('plan-stage');
  if (planStage) {
    var blocks = 4, days = 4, until = 14;

    function buildPlan() {
      var list = [];
      var blockNames = ['第一块', '第二块', '第三块', '第四块', '第五块', '第六块'];
      var learnGap = Math.max(1, Math.floor((until - 2) / Math.max(1, blocks)));
      for (var b = 0; b < blocks; b++) {
        var learnDay = 1 + b * learnGap;
        if (learnDay > until - 2) learnDay = Math.max(1, until - 2 - (blocks - 1 - b));
        var recall = [];
        if (learnDay + 1 <= until) recall.push('第' + (learnDay + 1) + '天');
        if (learnDay + 3 <= until) recall.push('第' + (learnDay + 3) + '天');
        recall.push('考前两天');
        list.push({
          name: blockNames[b] || ('第' + (b + 1) + '块'),
          learn: '第' + learnDay + '天',
          recall: recall.join('、')
        });
      }
      var rows = list.map(function (it) {
        return '<tr><td>' + it.name + '</td><td>' + it.learn + '</td><td>' + it.recall + '</td></tr>';
      }).join('');
      document.getElementById('plan-table').innerHTML =
        '<table style="width:100%;border-collapse:collapse;font-size:14px">' +
        '<thead><tr style="color:var(--muted);text-align:left">' +
        '<th style="padding:6px 4px">内容</th><th style="padding:6px 4px">第一次学</th><th style="padding:6px 4px">回想复习</th></tr></thead>' +
        '<tbody>' + rows + '</tbody></table>';
      var perWeek = Math.round(blocks * 3 / Math.max(1, days) * 10) / 10;
      var out = document.getElementById('plan-out');
      out.className = 'result';
      out.innerHTML = '<strong>给你的排程建议：</strong>把 ' + blocks + ' 块内容分别安排第一次学习，' +
        '每块至少回想复习两次，最后一次放在考前两天。每周拿出 ' + days +
        ' 天复习，平均每天大约要处理 ' + perWeek + ' 个回想任务，每次十到十五分钟就够。' +
        '<br>考前一天只做回忆清单和薄弱清单，不再从头读一遍。' +
        '<br><span style="color:var(--muted)">其余 ' + Math.max(0, 7 - days) + ' 天留白，是给突发情况的余地，不是浪费。</span>';
      ['blocks', 'days', 'until'].forEach(function (k) {
        var v = document.getElementById('plan-' + k + '-val');
        if (v) v.textContent = (k === 'blocks' ? blocks + ' 块' : (k === 'days' ? days + ' 天' : until + ' 天'));
      });
    }

    function bindRange(id, setter) {
      var el = document.getElementById(id);
      if (!el) return;
      el.addEventListener('input', function () { setter(parseInt(el.value, 10)); buildPlan(); });
    }
    bindRange('plan-blocks', function (v) { blocks = v; });
    bindRange('plan-days', function (v) { days = v; });
    bindRange('plan-until', function (v) { until = v; });
    buildPlan();
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：你平时的复习习惯是哪一种？", TTS["pretest"], [
        {"q": "背一份单词表的时候，你的做法更接近哪一种？",
         "options": [("从头读很多遍，读到顺口为止", False), ("遮住中文，先自己回想再看答案", True), ("抄写几遍，抄完就放下", False)],
         "explain": "遮住答案先回想，是让记忆被真正取出来一次。读和抄都比较像在看和写。<strong>错因提醒：</strong>很多同学误认为抄得越多记得越牢，常见错误是把手上动作的熟练，当成了脑子里的记住。"},
        {"q": "如果两周后有一次单元测，你更愿意把复习放在什么时候？",
         "options": [("考前两天集中背完", False), ("分成几次，中间隔几天各复习一次", True), ("考前一晚通读一遍", False)],
         "explain": "隔开时间复习，每次回想都在重新加固记忆。全部挤在考前，记得快也掉得快。<strong>错因提醒：</strong>考前集中背当下感觉最熟，容易误认为这就是最扎实的安排。"},
        {"q": "考试时遇到一道暂时想不起来的题，比较稳的做法是：",
         "options": [("先跳过，把会做的做完，再回头处理", True), ("一定要先把它做出来才往下走", False), ("直接空着不写", False)],
         "explain": "先做会的，能让你稳住节奏，也让大脑在后台继续找那条线索。<strong>错因提醒：</strong>常见错误是把一道题卡住当成整场考试失控——其实节奏是可以自己安排的。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "看着眼熟，不等于真的记得住", TTS["module-1"], f'''
        <p style="font-size:17px;margin:0 0 12px">同一份笔记读三遍，会觉得越来越顺、越来越熟。但这份熟悉感，常常被我们当成了已经掌握。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>反复阅读做了什么</strong></p>
            <p style="color:var(--muted)">它让内容变得好读、好认。当下很顺，但内容一直在书上，不在你脑子里被取出来过。</p>
          </div>
          <div class="inner-card">
            <p><strong>合上书回想做了什么</strong></p>
            <p style="color:var(--muted)">它逼你把内容从记忆里取出来一次。过程有点费劲，但正是这份费劲在加固记忆。</p>
          </div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">把「看得很顺」误认为「已经记住」，是这一课最高频的易错点。判断标准很简单：<strong>合上书，能不能说出来。</strong></p>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="两种复习方式对比示意图：反复阅读与合书回想的记忆保持差距">
          <figcaption>同样花四十分钟：一直读，一周后剩得少；中间合上书回想两次，一周后剩下的明显更多</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🧠</span><div><strong>小提示：</strong>在心理学上，把「先自己回想、再对答案」这样的做法<strong>叫做</strong>提取练习。它不是额外任务，只是把「再读一遍」换成了「先想一遍」。</div></div>
{insight_box([
    {"lens": "看见它", "text": "翻书复习时，眼睛在动、手在划，看起来一直在学；合上书回想时，那份安静反而让人心虚。"},
    {"lens": "解释它", "text": "回想时需要费力搜索，这个搜索的过程正是记忆被重新加固的时刻；只读不取，记忆始终停在原地。"},
    {"lens": "迁移它", "text": "同样的道理也适用于体育动作和乐器练习——只看教学视频永远学不会，得自己上一次场。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "cmp", 5, "lab-1", "复习方式对比台：同一份内容，三种复习方式", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先选一种内容，再比较三种复习方式在一周之后各自留下多少。数值是示意量级，看的是差距。</p>
        <div class="lab-panel" id="cmp-stage">
          <div class="flex-row" style="flex-wrap:wrap">
            <button class="choice" data-cmp-content="word" style="text-align:center">英语单词表</button>
            <button class="choice" data-cmp-content="history" style="text-align:center">历史年代与事件</button>
            <button class="choice" data-cmp-content="formula" style="text-align:center">数学公式</button>
          </div>
          <div id="cmp-rows" style="margin-top:14px"></div>
          <canvas id="cmp-canvas" width="640" height="200" style="width:100%;margin-top:14px;border-radius:10px;background:var(--brand-soft)"></canvas>
          <p style="color:var(--muted);font-size:13px;margin:8px 0 0">横轴是考试后的天数，纵轴是还能回想出来的比例。折线往上抬的位置，就是做过回想复习的那几天。</p>
          <p class="result" id="cmp-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>看完三组差距，你发现了什么？</strong>三次复习的总时间差不多，差别在于：复习之间有没有隔开，以及每次有没有先自己回想一遍。</div></div>
    ''', tag="动手实验室", bloom="analyze"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "把复习摊开到时间里，比一次学完更稳", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">一天连看四小时，和分四天各看一小时，总时长完全一样，一周后的结果通常差很多。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div>记忆本来就会在两次复习之间变淡，这是正常的，不是你不努力。</div></div>
          <div class="step"><span class="n">2</span><div>在变淡之后再回想一次，比在最熟的时候再读一遍，加固得更牢。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>所以安排的重点不是总时长，而是间隔：</strong>把同样的时间分成几次，中间隔开几天。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="间隔复习时间轴示意图：复习点分散在两周内，最后一次落在考前">
          <figcaption>把复习点摊在时间轴上：每块内容至少回想两次，最后一次落在考前两三天</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">📅</span><div><strong>换个说法：</strong>复习像给墙刷漆，一次刷厚不如隔一段时间再刷一层。<em>每一次都要等前一层半干</em>，才粘得牢。</div></div>
{insight_box([
    {"lens": "拆开它", "text": "一次复习里其实有两件事：先费力把内容取出来，再对答案修正。两件都做，才是完整的一次。"},
    {"lens": "比较它", "text": "集中复习赢在当天的手感，分散复习赢在两周后的结果——看你更在意哪个时间点。"},
])}
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "sched", 7, "lab-2", "间隔复习排程台：把复习点放进这两周", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">选一种复习节奏，看看这十四天里记忆保持的曲线，以及考试当天它落在哪里。</p>
        <div class="lab-panel" id="sched-stage">
          <div class="flex-row" style="flex-wrap:wrap">
            <button class="choice" data-sched-mode="once" style="text-align:center">只在考前一次</button>
            <button class="choice" data-sched-mode="each2" style="text-align:center">每两天复习一次</button>
            <button class="choice" data-sched-mode="expand" style="text-align:center">间隔逐渐拉长</button>
          </div>
          <canvas id="sched-canvas" width="640" height="200" style="width:100%;margin-top:14px;border-radius:10px;background:var(--brand-soft)"></canvas>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">复习次数</span><span class="v" id="sched-count">5 次</span></div>
            <div class="readout-cell"><span class="k">考试当天大约可以取出</span><span class="v green" id="sched-keep">约 78%</span></div>
          </div>
          <p class="result" id="sched-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧪</span><div><strong>挑战：</strong>试着说出一组「复习次数更少、但考试当天保持得更好」的安排。想清楚之后你会发现，决定结果的往往是<strong>间隔的位置</strong>，不只是次数。</div></div>
    ''', tag="动手实验室", bloom="evaluate"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：把四小节内容排成两周的复习表", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(251,191,36,.45)">
          <p style="margin:0"><strong>情境：</strong>小林有两周准备单元测，内容四小节，每天能拿出四十分钟，希望别再出现「看过就忘」。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>拆内容：</strong>每小节整理成一张回忆清单——只写问题，不写答案。</div></div>
          <div class="step"><span class="n">2</span><div><strong>摊时间：</strong>第 1 天学第一节；第 2 天先回想第一节再学第二节；第 4 天回想前两节再学第三节；第 8 天回想前三节再学第四节。</div></div>
          <div class="step"><span class="n">3</span><div><strong>留痕迹：</strong>每次回想时把想不起来的点记下来，形成一份自己的薄弱清单。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>收尾：</strong>考前两天不再从头读，只做回忆清单和薄弱清单，每节回想三分钟。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">不少人把「第 2 天先回想第一节」当成浪费时间，误认为应该先把新课全部学完再统一复习。结果是四节内容全挤在最后两天，间隔没被利用上。真正省力的做法是<strong>边学边回想</strong>。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "下面哪种做法，更能让你在一周后还记得住这份内容？",
         "options": [("把课本从头再读一遍，读到顺口", False),
                     ("合上书先自己回忆一遍，再翻开对答案", True),
                     ("用荧光笔把重点全部划出来", False)],
         "explain": "回想再对答案，让内容被真正取出来一次。划线和重读都停留在「看」这一层。<strong>错因提醒：</strong>把看着眼熟当成已经记住，是这一课最常见的误认为。"},
        {"q": "同样是四小时复习时间，下面哪种安排通常记得更牢？",
         "options": [("分在四天里，每天一小时", True),
                     ("考前一次连续四小时", False),
                     ("安排在考前一天晚上一次做完", False)],
         "explain": "总时长一样时，间隔着复习效果更稳，因为每次回想都发生在记忆变淡之后。<strong>错因提醒：</strong>容易误认为一口气学完最扎实，其实是当下的手感最好而已。"},
        {"q": "错题本怎么用，对提高分数最有帮助？",
         "options": [("把答案工整地抄一遍收好", False),
                     ("隔几天自己重做一遍，找出卡在哪一步", True),
                     ("收藏起来，考前翻一翻就好", False)],
         "explain": "错题的价值在于重做时暴露卡点。抄答案和翻一翻，都是在看别人怎么解。<strong>错因提醒：</strong>常见错误是把错题本当收藏夹，记下来了却没有再取出来过。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "plan", 10, "synthesis", "综合任务：给自己排一张两周复习表", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">拖动三个滑块，生成一份你可以照着做的排程建议，然后想一想哪几天需要留余地。</p>
        <div class="lab-panel" id="plan-stage">
          <div class="slider-row" style="display:block">
            <div style="font-weight:700;font-size:14px">① 这次要复习的内容有几块？<span id="plan-blocks-val" style="color:var(--muted)">4 块</span></div>
            <input id="plan-blocks" type="range" min="3" max="6" step="1" value="4" style="width:100%">
          </div>
          <div class="slider-row" style="display:block;margin-top:12px">
            <div style="font-weight:700;font-size:14px">② 一周里能拿出几天复习？<span id="plan-days-val" style="color:var(--muted)">4 天</span></div>
            <input id="plan-days" type="range" min="3" max="6" step="1" value="4" style="width:100%">
          </div>
          <div class="slider-row" style="display:block;margin-top:12px">
            <div style="font-weight:700;font-size:14px">③ 距离考试还有多少天？<span id="plan-until-val" style="color:var(--muted)">14 天</span></div>
            <input id="plan-until" type="range" min="7" max="21" step="1" value="14" style="width:100%">
          </div>
          <div id="plan-table" style="margin-top:14px"></div>
          <p class="result" id="plan-out" style="margin-top:12px"></p>
        </div>
        <div class="inner-card">
          <p><strong>写下来，说给自己听：</strong></p>
          <p style="color:var(--muted)">这份表里哪一天最容易被打断？你打算怎么给它留出余地？</p>
          <textarea id="syn-answer" rows="3" placeholder="我最容易被打断的是……所以我打算……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，看看思路还在不在", TTS["posttest"], [
        {"q": "早读时有二十分钟背一篇文言文，下面哪种安排更划算？",
         "options": [("十分钟读、十分钟合上书默述，再对一次原文", True),
                     ("二十分钟一直朗读到流畅", False),
                     ("二十分钟全部用来抄写", False)],
         "explain": "读加回想各占一半，比全程朗读多了一次真正的取出。朗读流畅只说明读得顺。"},
        {"q": "距离期末还有三周，最合理的做法是：",
         "options": [("前两周按块推进并回想，最后几天只做回忆清单和薄弱清单", True),
                     ("前两周放松，最后几天集中突击", False),
                     ("三周里每天把所有内容通读一遍", False)],
         "explain": "前松后紧会让大量内容挤在没有间隔的几天里；每天通读则缺少回想，容易留下熟悉的错觉。<strong>错因提醒：</strong>通读三周看着很努力，但常见错误正是用阅读时间替代了回想时间。"},
        {"q": "考场上发现有一题完全没思路，比较合适的是：",
         "options": [("先做后面的题，回头用剩下时间再试一次", True),
                     ("停下来反复读题，直到想出来", False),
                     ("放弃整张卷子的后半部分", False)],
         "explain": "跳过再回来，能保住整体节奏，也让大脑在后台继续找线索。整场考试的节奏是可以自己安排的。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把自己讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>眼熟不等于记住</strong>：合上书先回想、再对答案，才真正把内容取出来过一次。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>把复习摊开</strong>：同样的时长分成几次、隔几天来一次，比一次学完更稳。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>考前做减法</strong>：只过回忆清单和自己的薄弱清单，不再从头读一遍。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(251,191,36,.45)">
          <p style="margin:0"><strong>回到开头那个对比：</strong>你和同桌的差别，多半不在记性，而在复习的方式。方式是可以换的，节奏也是可以自己排的。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「回想、间隔、薄弱清单」这三个词，说清楚你打算怎么准备下一次测验。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "写出你这周复习某一份内容的具体做法，再把它改成「先合上书回想，再对答案」。",
            "说出集中复习和分散复习的一个主要区别，并举一个你自己身上的例子。",
        ],
        [
            "为下周的一门小测排一份带间隔的复习表，写清每次复习在哪一天、做什么。",
            "准备一张只有问题没有答案的回忆清单，用它复习一次，记录哪几题卡住了。",
        ],
        [
            "连续七天记录自己每次复习后的真实感受、时长和地点，找出最适合你的复习时段。",
            "观察家人或同学的一种学习习惯，用这节课的思路分析它可能的效果，并写下一句温和的建议。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "psych-h-g10-learning-strategy",
    "node_id": "psych-h-g10-learning-strategy",
    "subject": "psychology",
    "subject_cn": "心理健康",
    "stage": "high",
    "stage_cn": "高中",
    "curriculum": "中小学心理健康教育指导纲要（2012年修订）/ 教育部相关要求 · 高中",
    "title": "学习策略与考试适应：把复习握住",
    "name_en": "Learning Strategies and Exam Readiness",
    "grade": 10,
    "grade_cn": "高一",
    "domain": "learning-support",
    "domain_cn": "学习辅导",
    "lesson_type": "workshop",
    "version": "1.0.0",
    "description": "面向高一学生的学习策略课：从「看了三遍还是想不起来」这个常见困惑出发，把反复阅读带来的熟悉感与真正的记住区分开，讲清提取练习、分散复习与间隔重复三个可操作的做法，再用两周排程把方法落到时间表上。两个互动台都能真的操作：一个是复习方式对比台，同一份内容用集中复习、分散复习、分散加先回忆三种方式处理，可以看到一周后保住的比例差距与保持曲线；一个是间隔复习排程台，调整复习次数与间隔天数，画出十四天的记忆保持曲线（示意量级，不是对个人的预测）。综合任务用三个滑块生成一份可照着做的两周复习表。全课不评判、不贴标签，落点是「方法可改、节奏可控」，不出现任何诊断性说法。",
    "tags": ["学习策略", "复习方法", "提取练习", "间隔重复", "考试适应", "高一"],
    "standard_ref": "《中小学心理健康教育指导纲要（2012年修订）· 高中》学习辅导——掌握学习策略，开发学习潜能，提高学习效率；积极应对考试压力，学会根据自己的节奏安排学习与应考。",
    "hero_question": "同一份笔记，我看了三遍还是想不起来，同桌看两遍就记住了——差别到底在哪里？",
    "hero_alt": "学习策略知识结构图三栏：为什么看过就忘、复习怎么隔开、考前怎么安排",
    "hero_caption": "学习策略与考试适应：合书回想才叫记住 · 复习要摊开在时间里 · 考前做减法只过清单",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个最贴近你经历的困惑，后面的内容都会围着它展开。",
    "anchor_choices": [
        {"t": "为什么我看了很多遍还是想不起来？", "d": "书上的字都认识，考试时就是取不出来", "v": "为什么我看了很多遍还是想不起来"},
        {"t": "复习时间到底该怎么分配？", "d": "总时长一样，为什么效果差那么多", "v": "复习时间到底该怎么分配"},
        {"t": "错题本记了却没什么用，怎么办？", "d": "抄得整整齐齐，考试还是错同一类题", "v": "错题本记了却没什么用怎么办"},
        {"t": "怎么给自己排一份能执行的考前安排？", "d": "想要一张照着做就行的表", "v": "怎么给自己排一份能执行的考前安排"},
    ],
    "objectives": [
        "能说出反复阅读带来的熟悉感与真正记住之间的区别，并解释提取练习为什么更有效",
        "能说清集中复习和分散复习的差别，并举出一个自己的例子",
        "会为自己的一门小测安排带间隔的复习节奏，写出每次复习的时间与内容",
        "能给考前两三天做出可执行的安排，把注意力放在回忆清单与薄弱清单上",
    ],
    "objectives_plain": [
        "能说出反复阅读带来的熟悉感与真正记住之间的区别，并解释提取练习为什么更有效",
        "能说清集中复习和分散复习的差别，并举出一个自己的例子",
        "会为自己的一门小测安排带间隔的复习节奏，写出每次复习的时间与内容",
        "能给考前两三天做出可执行的安排，把注意力放在回忆清单与薄弱清单上",
    ],
    "standards": [
        {"content": "掌握学习策略，开发学习潜能，提高学习效率",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》高中 · 学习辅导"},
        {"content": "积极应对考试压力，学会按自己的节奏安排复习与应考",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》高中 · 学习辅导"},
    ],
    "prereqs": ["psych-h-g10-self-concept"],
    "prereqs_name": "自我认同与理想信念",
    "prereqs_meta": "psych-h-g10-self-concept",
    "leads_to": ["psych-h-g10-relationship"],
    "next_meta": "psych-h-g10-relationship",
    "section_images": ["assets/psych-h-g10-learning-strategy-fig1.webp", "assets/psych-h-g10-learning-strategy-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "看过三遍还是想不起来，先别急着说记性不好——这节课换一个角度看这件事。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能给自己排出一份照着做就行的复习安排。",
        "objectives": "看清四件事：眼熟与记住的区别、两种复习方式的差别、带间隔的节奏、考前怎么安排。",
        "pretest": "凭现在的习惯选就好，不打分。前测只是帮你看清自己现在站在哪里。",
        "module-1": "反复阅读带来的是熟悉感；合上书回想一次，才是真正把内容取出来。",
        "lab-1": "选一种内容，比较三种复习方式一周后剩下的比例，再看下面的曲线。",
        "module-2": "总时长一样时，间隔着复习更稳——每一次回想都发生在记忆变淡之后。",
        "lab-2": "调一调复习次数和间隔天数，看考试当天那条线落在哪里。",
        "worked-example": "四步走：拆内容、摊时间、留痕迹、考前收尾，每一步都能照着做。",
        "conceptest-1": "三个选项里藏着最常见的几个误解，选完请把每条解释读一遍。",
        "synthesis": "拖动三个滑块，生成属于你的两周复习表，再想想哪几天要留余地。",
        "posttest": "早读、期末和考场的三个新情境，看看你的思路还在不在。",
        "summary": "用「回想、间隔、薄弱清单」三个词，把这份安排讲给自己听。",
        "homework": "三层练习，前两层做完就算通关，第三层留给愿意继续观察的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先帮你找到卡点，再给一个最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是高中「学习辅导」板块里长期空缺的一课。设计上不喊口号、不谈意志力，只讲三件可操作的事：把「再读一遍」换成「先回想再对答案」，把复习时间摊开成带间隔的几次，把考前两三天留给回忆清单和薄弱清单。核心模拟是一张复习方式对比台——同一份内容用集中复习、分散复习、分散加先回忆三种方式处理，学生能看到一周后保住的比例差距与保持曲线；第二个台子把间隔排程画成十四天的曲线，让「间隔位置比次数更关键」这件事变得可见。最后用三个滑块生成一份可执行的排程表，把方法落到学生自己的时间上。全课语气温和、不评判，落点是方法可改、节奏可控。",
    "plan_table": """| 1 | cover | 学习策略与考试适应：把复习握住 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：你平时的复习习惯是哪一种？ | 起·前测（暴露现有习惯） |
| 5 | concept | 看着眼熟，不等于真的记得住 | 承·概念一（提取练习） |
| 6 | interactive | 复习方式对比台：同一份内容，三种复习方式 | 承·核心模拟（一周后保持率对比） |
| 7 | concept | 把复习摊开到时间里，比一次学完更稳 | 承·概念二（分散复习与间隔重复） |
| 8 | interactive | 间隔复习排程台：把复习点放进这两周 | 承·实验台（间隔位置与保持曲线） |
| 9 | concept | 例题示范：把四小节内容排成两周的复习表 | 转·重难点突破（分步示范 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：给自己排一张两周复习表 | 合·迁移应用（滑块生成排程） |
| 12 | quiz | 后测：换几个新情境，看看思路还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把自己讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：为什么看过就忘、复习怎么隔开、考前怎么安排 三栏\n- P5 两种复习方式对比图（已生成）：反复阅读与合书回想的保持差距\n- P7 间隔复习时间轴（已生成）：复习点分散在两周内，最后一次落在考前\n- 若需补充：一张可打印的空白两周排程表、一张回忆清单模板",
}
