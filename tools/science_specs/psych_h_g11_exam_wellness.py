# -*- coding: utf-8 -*-
"""高中 · 心理健康 · 考试心理与身心健康（高二）—— 补齐知识树「抗挫与适应」空缺

铁规：语气温和、不评判、不贴标签；不出现任何临床诊断词汇，不涉及自伤自杀与暴力情节。
不做紧张放大，不承诺「照做就一定能考好」；落点是「状态可调、节奏可控」。
核心模拟：考前一周安排台（七天 × 四种排法 → 看这个安排撑不撑得住）。
另含：临场应对选择台（心慌 / 卡题 / 想放弃 → 三种做法 → 可能的走向）
      + 考后复盘台（八句话 → 复盘题目与时间 / 复盘情绪）。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/psych-h-g11-exam-wellness-fig1.webp'
F2 = './assets/psych-h-g11-exam-wellness-fig2.webp'

TTS = {
    "hero": "先不急着讲方法。请你回想上一次考试前的那个星期：你在做什么？大概是——把复习表排得很满，把睡觉的时间往后挪一点、再挪一点；然后在考场上发现，明明看过的题，读两遍也进不去。这节课我们只做三件事：把考前一周排成一个撑得住的节奏，把大目标拆成今天做得完的小步，再练两个在考场上当场就能做的动作。最后还有一件事——考完之后，复盘题目，不复盘情绪。先说清楚：这些做法不保证你考得更好，它们能做的是让状态可调、节奏可控。",
    "problem-anchor": "在开始之前，先选出最贴近你最近状态的一项。是想知道考前这一周该怎么安排，还是想知道考场上慌了、卡住了怎么办，又或者是想知道考完之后该怎么看这次结果。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出考前一周里，睡眠和复习各自该留出多少空间，并给自己排一份七天都撑得住的安排。第二，会把一个大目标拆成当天做得完的小步，并说清判断这一步够不够小的标准。第三，会用在考场上当场能做的两个动作：把呼吸放慢，把注意力交回题目第一句。第四，能把考后复盘对准题目和时间安排，而不是对着自己的情绪反复回放。",
    "pretest": "先做三道小题，凭你平时的习惯选就行，没有对错，也不打分。选完会立刻出现解释，正好帮你看清自己现在习惯怎么安排考前的节奏。",
    "module-1": "考前一周最容易出问题的地方，是把所有力气都用在复习量上，而睡眠被当成了可以随时挪用的部分。先说睡觉这件事。你要做的不是提前很多天去补觉，而是把睡觉和起床的时间稳住，前后波动尽量不要超过半小时；考前两晚尤其不要用熬夜去换复习时间。再说复习量。当你写下一句话是复习数学的时候，它太大了，大到今天做不完；把它改成今晚把哪三道错题重做一遍，才是一个能开始的动作。这里有一个常见的误认为：拆小就是降低要求。不是，总量不变，只是换成了看得见起点的写法。",
    "lab-1": "现在打开考前一周安排台。七天，每天请你点一种排法。稳，复习、留白、按时睡三样都留住；赶，把复习量加上去，休息先挤掉；松，几乎不复习，早点睡；熬，复习到很晚，睡眠欠着。一天一天点下去，下面的可持续度会跟着变。它算的不是你能考多少分，而是这个安排一周下来撑不撑得住。请留意，这里的说法都是可能，不是保证。",
    "module-2": "考场上出现心口发紧、脑子发空、一道题怎么读都读不进去，这些都是很常见的反应，不代表你准备得不好。这个时候能做的动作有两个。第一个是把呼吸放慢：先把笔放下，吸气数到四，呼气数到六，做三次。它的作用不是让你马上不紧张，而是先给身体一个着落点。第二个是把注意力交回题目第一句：用手指着题干，只读这一句，读完再读下一句。如果一道题卡住太久，先在题号上做个记号跳过去，回头再来，通常比在原地耗着更划算。",
    "lab-2": "再看临场那几分钟。下面有三种情况：手有点抖、心口跳得快；一道题卡了五分钟；脑子里冒出算了这两个字。每一种我给了三种做法，你轮流点开，看看它们可能把后面带到哪里。请留意，三种做法都能让你继续坐在考场上，差别在于哪一种更省力。",
    "worked-example": "我们完整走一遍。情境是：还有七天的期中考试，你越想越觉得什么都没准备好。第一步，先把睡觉和起床的时间定下来，这七天前后不超过半小时，这一条先不谈复习。第二步，把目标拆小：不写复习物理，写今晚把受力分析的两道错题重做一遍。第三步，排出七天，中间至少留两个晚上不放新内容，只做整理和休息。第四步，考场上如果心口发紧，先放下笔做三次慢呼吸，再把手指放到题干第一句上。第五步，考完之后对着卷子复盘三件事：哪一类题没认出来、时间花在哪一段、下一步补哪一块；不反复回放我当时怎么那么差。",
    "conceptest-1": "现在用三个容易弄混的说法考考你。请仔细读每一个选项，选出你认为更合适的那个，然后看解释。",
    "synthesis": "最后做一次考后复盘。下面有八句话，都是考完之后可能冒出来的想法。请你判断：它是在复盘题目和时间，还是在复盘情绪。判断完会给出解释，也请你留意自己在哪一类上花的时间更多。",
    "posttest": "最后换几个新情境检验一下。这次的问题出现在考前两晚、考场上的一道大题，还有考完回家的路上，看看你能不能用上前面说过的方法。",
    "summary": "这节课我们弄明白了三件事。第一，考前一周先稳住两样：睡觉和起床的时间，以及被拆小到当天做得完的复习目标。第二，临场当场能做的两个动作，是把呼吸放慢、把注意力交回题目第一句。第三，考后复盘对着题目和时间安排，不跟着情绪反复回放。最后把期待放在合适的位置：这些做法不保证你考得更好，它们能做的是让状态可调、节奏可控。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写下你考前最典型的一天，从起床到睡觉逐段标出来，看看睡眠和留白各占了多少。第二层能力应用，动手做：用安排台排出你自己的七天，让可持续度尽量高，并写一句为什么这样排。第三层迁移挑战，选做：连续记录一次考试的全过程——考前两晚、考场上的一个动作、考后的一次复盘，三项各写一句，一周后回看哪一项最管用。",
    "knowledge-graph": "这张图展示了这节课在知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 考前一周先稳住两件事", "lab-1": "核心模拟 考前一周安排台",
    "module-2": "概念二 临场那几分钟", "lab-2": "选择台 临场三种情况",
    "worked-example": "例题讲解", "conceptest-1": "概念测试",
    "synthesis": "综合任务 考后复盘台", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

CUSTOM_JS = r"""
/* ============================================================
   psych-h-g11-exam-wellness 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 核心模拟：考前一周安排台（七天 × 四种排法 → 可持续度）
   3) 临场应对选择台（心慌 / 卡题 / 想放弃 → 三种做法 → 可能的走向）
   4) 考后复盘台（八句话 → 复盘题目与时间 / 复盘情绪）
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

  /* ---------- 2. 考前一周安排台 ---------- */
  var DAYS = ['周一', '周二', '周三', '周四', '周五', '周六', '考前晚'];
  var WAYS = {
    steady: { n: '稳', s: 4,
      d: '复习按计划走，中间留出走动和休息，按时睡。这一天结束时你大概还能读得进东西。',
      k: '复习够 · 留白有 · 睡眠有' },
    push:  { n: '赶', s: 2,
      d: '复习量加上去，休息和走动先挤掉。短期也许还能撑，连着几天之后，坐下来也容易读不进去。',
      k: '复习多 · 留白少 · 睡眠偏少' },
    rest:  { n: '松', s: 3,
      d: '几乎不放新内容，早点睡。恢复是够的，心里可能会有点没底，可以配一件十分钟的小整理。',
      k: '复习少 · 留白多 · 睡眠足' },
    late:  { n: '熬', s: 1,
      d: '复习到很晚，睡眠欠着。第二天上午的注意力通常会打折扣，补回来的效率不一定有你付出的多。',
      k: '复习多 · 留白无 · 睡眠欠着' }
  };
  var plan = new Array(7).fill('');
  var planStage = document.getElementById('plan-stage');
  if (planStage) {
    function renderPlan() {
      document.getElementById('plan-days').innerHTML = DAYS.map(function (d, i) {
        var cur = plan[i];
        var btns = Object.keys(WAYS).map(function (k) {
          var cls = 'choice' + (cur === k ? ' selected' : '');
          return '<button class="' + cls + '" data-plan-day="' + i + '" data-plan-way="' + k +
            '" style="text-align:center;font-size:13px;padding:10px 12px">' + WAYS[k].n + '</button>';
        }).join('');
        var note = cur
          ? '<p class="result" style="margin:8px 0 0">' + WAYS[cur].k + '。这样可能会：' + WAYS[cur].d + '</p>'
          : '<p style="margin:8px 0 0;color:var(--muted);font-size:13px">还没有选。点一个你最可能真的这样过的排法。</p>';
        return '<div class="plain-row" style="padding:12px 14px;border-radius:12px;background:var(--bg-subtle);' +
          'border:1px solid var(--line-subtle);margin:8px 0">' +
          '<p style="margin:0 0 8px"><strong>' + d + '</strong></p>' +
          '<div class="flex-row" style="margin-top:0;gap:6px">' + btns + '</div>' + note + '</div>';
      }).join('');

      var picked = plan.filter(function (x) { return x; }).length;
      var total = plan.reduce(function (a, x) { return a + (x ? WAYS[x].s : 0); }, 0);
      var pct = Math.round(total / 28 * 100);
      var bar = document.getElementById('plan-bar');
      var out = document.getElementById('plan-out');
      document.getElementById('plan-score').textContent = picked ? pct + ' / 100' : '—';
      bar.style.width = (picked ? pct : 0) + '%';

      if (!picked) {
        out.className = 'result warn';
        out.innerHTML = '先点一周里最像你的那种过法。这个数字算的不是分数，是这个安排一周下来撑不撑得住。';
      } else if (picked < 7) {
        out.className = 'result warn';
        out.innerHTML = '<strong>已排 ' + picked + '/7 天。</strong>接着排完，再看整周的可持续度。';
      } else if (pct >= 80) {
        out.className = 'result';
        out.innerHTML = '<strong>这个安排看起来撑得住：</strong>睡眠有保障，复习之间也留了缝。' +
          '它不一定让你考得更好，但一周下来状态更容易稳住。';
      } else if (pct >= 55) {
        out.className = 'result warn';
        out.innerHTML = '<strong>有几处偏紧。</strong>这样可能会：撑得住几天，到后面读题越来越费力。' +
          '还可以试试把最后两天改成稳，或者至少在考前两晚按时睡。';
      } else {
        out.className = 'result warn';
        out.innerHTML = '<strong>这个安排里睡眠被挤掉得比较多。</strong>这样可能会：短期内还能撑，' +
          '一周下来更容易出现坐着也读不进去的情况。还可以试试先固定睡觉时间，再把复习量填进空出来的时段。';
      }
      document.querySelectorAll('[data-plan-day]').forEach(function (b) {
        b.addEventListener('click', function () {
          plan[parseInt(b.dataset.planDay, 10)] = b.dataset.planWay;
          renderPlan();
        });
      });
    }
    renderPlan();
  }

  /* ---------- 3. 临场应对选择台 ---------- */
  var CUE = {
    flutter: {
      n: '手有点抖，心口跳得很快',
      breathe: '把笔先放下，吸气数到四，呼气数到六，做三次，再把手指放到题干第一句上。这样可能会：身体先有了一处着落点，注意力不见得马上回来，但你能从第一句重新读起。',
      force: '在心里催自己别慌，硬撑着往下写。这样可能会：题也能写下去，只是多花一份力气在压住身体上；还可以试试先把呼吸放慢三次。',
      watch: '一直留意自己的手，担心旁边的同学看出来。这样可能会：注意力全留在身体上，题目更读不进去。还可以试试把眼睛移回题干第一句。'
    },
    stuck: {
      n: '一道题卡了五分钟，越想越乱',
      breathe: '先在题号上做个记号跳过去，把后面会做的先拿下，回头再来。这样可能会：这一题没动，但整张卷子的时间还在你手上。',
      force: '不管花多久都一定要先把这题做出来。这样可能会：做出来了，也可能把后面本可以拿到的时间搭进去。还可以试试先做个记号往后走。',
      watch: '干脆把后面都放下，趴一会儿再说。这样可能会：当下松了一点，但交卷前那段时间会更紧；还可以试试只往后做一道最简单的。'
    },
    quit: {
      n: '脑子里冒出两个字：算了',
      breathe: '允许自己停三十秒，喝口水，然后只做下一小步——读下一题的第一句。这样可能会：念头还在，但你已经又往前挪了一点。',
      force: '在心里批评自己一顿，逼自己必须立刻精神起来。这样可能会：话说完更累了，题目还是没读进去；还可以试试把要求缩到只读一句。',
      watch: '合上卷子，就这样吧。这样可能会：当下确实轻松了，只是这张卷子上你原本会做的那部分也没写上去。还可以试试只挑一道最有把握的先写上。'
    }
  };
  var cueStage = document.getElementById('cue-stage');
  if (cueStage) {
    var KICKS = [['breathe', '先让身体和注意力各归各位'], ['force', '硬撑着压过去'], ['watch', '盯着自己的反应看']];
    document.querySelectorAll('[data-cue-scene]').forEach(function (host) {
      var sc = host.dataset.cueScene;
      host.innerHTML = KICKS.map(function (k) {
        return '<button class="choice" data-cue-pick="' + k[0] + '" style="font-size:13px;padding:12px 14px">' +
          k[1] + '</button>';
      }).join('');
      host.querySelectorAll('[data-cue-pick]').forEach(function (b) {
        b.addEventListener('click', function () {
          var key = b.dataset.cuePick;
          host.querySelectorAll('[data-cue-pick]').forEach(function (x) { x.classList.remove('selected'); });
          b.classList.add('selected');
          var out = document.querySelector('[data-cue-out="' + sc + '"]');
          out.style.display = 'block';
          out.className = 'result' + (key === 'breathe' ? '' : ' warn');
          out.innerHTML = '<strong>' + CUE[sc].n + '　→　' + CUE[sc][key] + '</strong>';
        });
      });
    });
  }

  /* ---------- 4. 考后复盘台 ---------- */
  var REVIEW = [
    { t: '第三题我把条件看错了，其实问的是另一件事', a: 'work',
      r: '对着题目的复盘，会直接接到一个动作：下次读题时先把问的那件事圈出来。' },
    { t: '我这个人就是不行，这种题永远做不出来', a: 'mood',
      r: '这句话里没有能改的地方，它对着的是对自己的评价。这样想很自然，但它带不来下一步。' },
    { t: '这次前四十分钟全用在选择上，后面大题没时间', a: 'work',
      r: '时间分配属于可以安排的部分：下次哪一段该留多少分钟，是可以提前定下来的。' },
    { t: '考场上我一直在想这次肯定完了，越想越慌', a: 'mood',
      r: '这一句记录的是当时的状态。先认出它，再换成能做的事会更有用，比如把呼吸放慢三次。' },
    { t: '那道大题的第二步公式我记混了', a: 'work',
      r: '记混了一个公式，是能补的：把它写进错题本，明早默一遍就算处理过了。' },
    { t: '考完我就一直难受，什么都不想做', a: 'mood',
      r: '这种感受值得被看见，但它不需要在今天被分析清楚。先去走一走，等身体缓一点再回到卷子上。' },
    { t: '老师讲过的那一类题型，这次我没认出来', a: 'work',
      r: '没认出来属于题目层面的问题：这类题的标志长什么样，是可以专门认一遍的。' },
    { t: '反正我每次都这样，改也没什么用', a: 'mood',
      r: '这是一句关于自己的判断，不是关于卷子的发现。还可以试试只挑出这次最具体的一个小问题。' }
  ];
  var reviewStage = document.getElementById('review-stage');
  if (reviewStage) {
    reviewStage.innerHTML = REVIEW.map(function (c, i) {
      var btns = [['work', '复盘题目与时间'], ['mood', '复盘情绪']].map(function (k) {
        var cls = 'choice';
        if (c.picked === k[0]) cls += (k[0] === c.a ? ' correct' : ' wrong');
        return '<button class="' + cls + '" data-review="' + i + '" data-review-pick="' + k[0] +
          '" style="text-align:center;font-size:13px">' + k[1] + '</button>';
      }).join('');
      return '<div class="plain-row" style="padding:12px 14px;border-radius:12px;background:var(--bg-subtle);' +
        'border:1px solid var(--line-subtle);margin:8px 0">' +
        '<p style="margin:0 0 8px"><strong>' + (i + 1) + '. ' + c.t + '</strong></p>' +
        '<div class="grid" style="grid-template-columns:repeat(2,1fr);gap:6px">' + btns + '</div>' +
        (c.picked ? '<p class="result ' + (c.picked === c.a ? '' : 'warn') + '" style="margin:8px 0 0">' +
          (c.picked === c.a ? '<strong>这一句挺适合放进这一栏。</strong>' : '<strong>还可以再想想：</strong>') +
          c.r + '</p>' : '') +
        '</div>';
    }).join('');
    function renderReview() {
      reviewStage.innerHTML = REVIEW.map(function (c, i) {
        var btns = [['work', '复盘题目与时间'], ['mood', '复盘情绪']].map(function (k) {
          var cls = 'choice';
          if (c.picked === k[0]) cls += (k[0] === c.a ? ' correct' : ' wrong');
          return '<button class="' + cls + '" data-review="' + i + '" data-review-pick="' + k[0] +
            '" style="text-align:center;font-size:13px">' + k[1] + '</button>';
        }).join('');
        return '<div class="plain-row" style="padding:12px 14px;border-radius:12px;background:var(--bg-subtle);' +
          'border:1px solid var(--line-subtle);margin:8px 0">' +
          '<p style="margin:0 0 8px"><strong>' + (i + 1) + '. ' + c.t + '</strong></p>' +
          '<div class="grid" style="grid-template-columns:repeat(2,1fr);gap:6px">' + btns + '</div>' +
          (c.picked ? '<p class="result ' + (c.picked === c.a ? '' : 'warn') + '" style="margin:8px 0 0">' +
            (c.picked === c.a ? '<strong>这一句挺适合放进这一栏。</strong>' : '<strong>还可以再想想：</strong>') +
            c.r + '</p>' : '') +
          '</div>';
      }).join('');
      reviewStage.querySelectorAll('[data-review]').forEach(function (b) {
        b.addEventListener('click', function () {
          var i = parseInt(b.dataset.review, 10);
          if (REVIEW[i].picked) return;
          REVIEW[i].picked = b.dataset.reviewPick;
          var done = REVIEW.filter(function (x) { return x.picked; }).length;
          var out = document.getElementById('review-out');
          if (done >= 8) {
            out.style.display = 'block';
            out.className = 'result';
            out.innerHTML = '<strong>八句都分完了。</strong>复盘的目的不是把自己说得更好或更差，' +
              '而是让卷子上那几处具体的地方被看见。所以每次复盘完，请只留下<em>一件</em>明天能补的小事。';
          } else {
            out.style.display = 'block';
            out.className = 'result warn';
            out.innerHTML = '<strong>已分 ' + done + '/8 句。</strong>继续把剩下的分完，最后会看到一段小结。';
          }
          renderReview();
        });
      });
    }
    renderReview();
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：考前的你，习惯怎么安排？", TTS["pretest"], [
        {"q": "离考试还有一周，你打算怎么安排这几个晚上？",
         "options": [("把复习量排到最满，其余都往后放", False),
                     ("定好睡觉时间，再把复习量填进空出来的时段", True),
                     ("先不安排，看当天状态再说", False)],
         "explain": "先把睡觉和起床的时间立住，再往里填复习量，这一周才更可能走得下去。<strong>错因提醒：</strong>常见错误是误认为只要复习量够大就一定有收获，而睡眠被挤掉之后，同样的时间往往读不进去。"},
        {"q": "「今晚复习物理」和「今晚把受力分析的两道错题重做一遍」，哪个更像一个能开始的目标？",
         "options": [("第一个更全面，一眼就知道要复习什么", False),
                     ("第二个更容易开始，因为它有看得见的起点", True),
                     ("两个差不多，都是复习", False)],
         "explain": "目标是给自己一个起点，不是给自己一个范围。<strong>错因提醒：</strong>容易把拆小搞混成降低要求——总量不变，只是换成了今天做得完的写法。"},
        {"q": "考场上心口跳得快、读不进题的时候，下面哪一种说法更贴近事实？",
         "options": [("这说明我准备得不够，状态不好", False),
                     ("这是很常见的反应，可以先做三次慢呼吸再回到题干第一句", True),
                     ("必须先把紧张彻底压下去，才能开始做题", False)],
         "explain": "身体有反应不等于准备得不好，也不一定要先把它压下去才开始。<strong>错因提醒：</strong>误认为必须等到完全不紧张才能动笔，结果常常在等待里把时间耗掉。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "考前一周：先稳住两件事", TTS["module-1"], f'''
        <p style="font-size:17px;margin:0 0 12px">这一周真正要管的，不是你还能多塞多少复习量，而是这两样有没有被挤掉。</p>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgb(var(--warm-rgb) / .45)">
          <p style="margin:0"><strong>为什么要先学这个？</strong>你已经知道考前要多复习；但<strong>但</strong>把所有力气都堆在复习量上，睡眠和休息就会被当成随时能挪用的部分；<strong>所以</strong>先学会稳住这两样，复习才落得下来。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>把睡觉和起床的时间立住：</strong>前后波动尽量不超过半小时。不是提前很多天补觉，而是让它稳定。</div></div>
          <div class="step"><span class="n">2</span><div><strong>考前两晚不用熬夜换时间：</strong>熬夜多出来的那一两小时，常常从第二天上午的读题能力里扣回去。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>把目标拆到当天做得完：</strong>不写复习物理，写今晚把哪三道错题重做一遍。</div></div>
        </div>
        <div class="kid-note"><span class="emoji">💡</span><div><strong>一个判断标准：</strong>如果这句话你今晚就能坐下开始，并且大概知道什么时候算做完，它就够小了。</div></div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">误认为拆小目标就是降低要求。其实总量没变，只是从「复习完一章」换成了「今晚先做这两道题」——后者才有起点。</p>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="考前一周两张表：左边是睡眠节律，右边是把大目标拆成小步">
          <figcaption>左边守时间，右边拆步长：睡觉时间先立住不动，复习目标一层层拆到今天做得完</figcaption>
        </figure>
{insight_box([
    {"lens": "解释它", "text": "为什么睡眠要排在复习前面？因为读题、算题靠的都是第二天的注意力，而它主要来自前一天的睡眠。"},
    {"lens": "比较它", "text": "「复习三小时」和「重做三道错题」用的时间可能差不多，区别在于后者知道什么时候算完成。"},
    {"lens": "迁移它", "text": "这套拆法不只用在考试：一场演出、一次比赛、一个要交的作品，都可以先定住休息时间，再把目标拆到今天做得完。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "plan", 5, "lab-1", "核心模拟：考前一周安排台", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">七天，每天点一种排法。下面的可持续度算的不是分数，而是这个安排一周下来撑不撑得住。</p>
        <div class="lab-panel" id="plan-stage">
          <div id="plan-days"></div>
          <div class="readout-cell" style="margin-top:12px">
            <span class="k">安排可持续度（按你的排法估算）</span>
            <span class="v" id="plan-score">—</span>
          </div>
          <div style="height:10px;border-radius:5px;background:var(--bg-subtle);overflow:hidden;margin-top:8px;border:1px solid var(--line-subtle)">
            <div id="plan-bar" style="height:100%;width:0%;background:linear-gradient(90deg,var(--brand),var(--brand-2));transition:width .3s ease"></div>
          </div>
          <p class="result warn" id="plan-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">📅</span><div><strong>排完请想一想：</strong>哪一个晚上是你最容易真的熬下去的？把它改一改，可持续度通常比再多加一小时复习涨得快。</div></div>
    ''', tag="核心模拟", bloom="apply"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "临场那几分钟：两个当场能做的动作", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">考场上身体有反应，不等于你准备得不好。这时候能做的不是说服自己别紧张，而是两个具体动作。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>动作一：把呼吸放慢</strong></p>
            <p style="color:var(--muted)">笔先放下，吸气数到四，呼气数到六，做三次。它的作用不是让你马上不紧张，而是先给身体一个着落点。</p>
          </div>
          <div class="inner-card">
            <p><strong>动作二：注意力回到题目第一句</strong></p>
            <p style="color:var(--muted)">用手指着题干，只读这一句，读完再读下一句。不求一次读懂整道题，只求有个起点。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="临场两个动作示意图：一条放慢的呼吸曲线和一个回到题目第一句的聚焦圈">
          <figcaption>先把呼吸的节奏拉长，再把注意力交回题干第一句——两个动作，当场就能做</figcaption>
        </figure>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>卡太久先跳：</strong>在题号上做个记号往后走，比在原地耗着更划算。</div></div>
          <div class="step"><span class="n">2</span><div><strong>做完一段歇十秒：</strong>抬起头、看一眼远处，让眼睛和注意力各换一次气。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>把注意力收在手上：</strong>只关心现在这道题，不去算总分，也不去想别人做到哪了。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">误认为必须先把紧张彻底压下去才能动笔，于是把时间花在等自己不紧张上。其实可以先动笔，让呼吸慢一点，注意力会跟着回来一些。</p>
        </div>
        <div class="kid-note"><span class="emoji">⏱️</span><div><strong>记忆锚点：</strong>两个字就够——<strong>放慢</strong>（呼吸）和<strong>回到</strong>（题干第一句）。考场上想得起这两个字，就有地方落脚。</div></div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "cue", 7, "lab-2", "选择台：临场那几分钟，你会怎么做？", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">三种情况，每种各点一个做法，看看它可能把后面带到哪里。三种都能让你继续坐着，差别在省不省力。</p>
        <div class="lab-panel" id="cue-stage">
          <div class="inner-card" style="margin:10px 0">
            <p><strong>情况一　手有点抖，心口跳得很快</strong></p>
            <div class="grid" style="gap:8px" data-cue-scene="flutter"></div>
            <p class="result warn" data-cue-out="flutter" style="display:none;margin-top:10px"></p>
          </div>
          <div class="inner-card" style="margin:10px 0">
            <p><strong>情况二　一道题卡了五分钟，越想越乱</strong></p>
            <div class="grid" style="gap:8px" data-cue-scene="stuck"></div>
            <p class="result warn" data-cue-out="stuck" style="display:none;margin-top:10px"></p>
          </div>
          <div class="inner-card" style="margin:10px 0">
            <p><strong>情况三　脑子里冒出两个字：算了</strong></p>
            <div class="grid" style="gap:8px" data-cue-scene="quit"></div>
            <p class="result warn" data-cue-out="quit" style="display:none;margin-top:10px"></p>
          </div>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧭</span><div><strong>三种情况都点完之后：</strong>选出你最容易出现的那一种，只记住对应的那一个做法。考场上不需要想起三种。</div></div>
    ''', tag="动手实验室", bloom="apply"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：考前七天，五步走一遍", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgb(var(--warm-rgb) / .45)">
          <p style="margin:0"><strong>情境：</strong>还有七天的期中考试，你越想越觉得什么都没准备好，晚上越睡越晚。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先定时间：</strong>把睡觉和起床的时间写下来，这七天前后不超过半小时，先不谈复习量。</div></div>
          <div class="step"><span class="n">2</span><div><strong>再拆目标：</strong>不写复习物理，写今晚把受力分析的两道错题重做一遍。</div></div>
          <div class="step"><span class="n">3</span><div><strong>排进七天：</strong>中间至少留两个晚上不放新内容，只做整理和休息。</div></div>
          <div class="step"><span class="n">4</span><div><strong>临场两个动作：</strong>心口发紧就先做三次慢呼吸，再把手指放到题干第一句上。</div></div>
          <div class="step"><span class="n green">5</span><div><strong>考后复盘三件事：</strong>哪一类题没认出来、时间花在哪一段、下一步补哪一块。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">两个方向都容易走偏：一种是<strong>把睡眠当成复习的备用时间</strong>，越到考前越晚睡；另一种是<strong>把复盘变成反复回放当时的感受</strong>，卷子上的问题反而没被看见。第七天的晚上尤其容易两样一起发生。</p>
        </div>
        <div class="inner-card">
          <p><strong>把期待放在合适的位置：</strong>这五步不保证你考得更好，也不会让你从此不再紧张。它们能做的是让这一周有一个走得下去的节奏。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "「这次我要把落下的全部补回来，一天也不能再拖」——这句话最需要改的地方是：",
         "options": [("范围太大、没有起点，往往一天都动不了", True),
                     ("语气太消极，应该更有信心", False),
                     ("不该补，过去的就算了", False)],
         "explain": "决心大不等于做得到。缩到今晚做得完的一件小事，才有真正的开始。<strong>错因提醒：</strong>常见错误是误认为计划越严越有用，结果常常第二天就散了。"},
        {"q": "关于「考前两晚熬夜多复习一点」，下面哪种说法更合适？",
         "options": [("多出来的时间常常要从第二天上午的读题能力里扣回去", True),
                     ("只要熬得住就一定有收获", False),
                     ("完全不能晚睡，必须提前两个小时上床", False)],
         "explain": "不是要求你提前很多天补觉，而是别用熬夜去换复习时间。<strong>错因提醒：</strong>容易把「稳住作息」搞混成「必须很早睡」，反而因为躺不着而更着急。"},
        {"q": "考后复盘时，下面哪一句更容易带来下一步？",
         "options": [("第三题我把条件看错了，问的其实是另一件事", True),
                     ("反正我每次都这样，改也没什么用", False),
                     ("我当时怎么那么差，越想越难受", False)],
         "explain": "对着题目和时间的复盘，会直接接到一个动作。对着自己的评价，通常只会停在原地。<strong>错因提醒：</strong>误认为把感受说清楚就算复盘完了，其实卷子上那几处具体的地方还没被看见。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "rev", 10, "synthesis", "综合任务：考后复盘台", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">八句话，都是考完之后可能冒出来的想法。每一句选一栏，留意自己在哪一栏停留得更久。</p>
        <div class="lab-panel" id="review-stage"></div>
        <p class="result warn" id="review-out" style="display:none;margin-top:12px"></p>
        <div class="inner-card">
          <p><strong>写下来，留给自己：</strong></p>
          <p style="color:var(--muted)">从「复盘题目与时间」那一栏里，挑一件明天就能补的小事，写清它做完的样子。</p>
          <textarea id="syn-answer" rows="3" placeholder="明天我要补的这件小事是……做完的样子是……" style="margin-top:8px"></textarea>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🤝</span><div><strong>还有一件事想告诉你：</strong>如果这段时间的睡眠、吃饭或者心情已经持续受到明显影响，别一个人扛着——找家长、班主任或者心理健康老师说一说，是照顾自己的方式，和「自己想办法」并不冲突。</div></div>
    ''', tag="综合任务", bloom="evaluate"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，看看方法还在不在", TTS["posttest"], [
        {"q": "考前两晚，你躺下很久也睡不着，脑子一直在转。比较合适的做法是：",
         "options": [("起来喝点水、把明天的安排写下来，再回到床上，不强迫自己马上睡着", True),
                     ("要求自己必须立刻入睡，睡不着就更着急", False),
                     ("索性不睡了，起来把这一章再看一遍", False)],
         "explain": "把注意力从「必须睡着」移开，通常会更容易睡。硬躺着催自己，反而让身体更紧。<strong>错因提醒：</strong>常见错误是误认为考前必须睡够几个小时才行，于是把睡不着当成了第二个问题。"},
        {"q": "考试中间，一道大题的第二步你怎么也想不起来。这时更合适的做法是：",
         "options": [("先在题号上做个记号，往后做会做的，回头再来", True),
                     ("不管花多久都要当场把它想出来", False),
                     ("认为自己这一科完了，后面也没心思做", False)],
         "explain": "先跳过去，是把整张卷子的时间留在自己手上。<strong>错因提醒：</strong>容易把「先跳过」搞混成「放弃这题」——它只是换了个顺序，题还在那儿。"},
        {"q": "考完回家的路上，你一直在回放当时那几分钟。下面哪一种做法更有用？",
         "options": [("等身体缓一点，再对着卷子挑出三件具体的事：哪类题没认出、时间花在哪段、下一步补哪块", True),
                     ("反复回想当时的心情，直到把自己说服", False),
                     ("告诉自己别想了，然后什么都不看", False)],
         "explain": "把复盘对准题目和时间，才接得上一个动作。当时的心情值得被看见，但不必在回家的路上分析清楚。<strong>错因提醒：</strong>误认为想通情绪之后问题就解决了，其实卷子上那几处地方还在原处。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把这一周讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>先稳住两样</strong>：睡觉和起床的时间，以及拆到当天做得完的复习目标。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>临场两个动作</strong>：把呼吸放慢，把注意力交回题干第一句。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>考后复盘两栏</strong>：对着题目和时间安排，不跟着情绪反复回放。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgb(var(--warm-rgb) / .45)">
          <p style="margin:0"><strong>回到开头那种星期：</strong>复习表排满、睡觉往后挪的时候，你不必先把状态调到最好。先定住睡觉时间，再把目标拆小，考场上记得放慢和回到，考完只复盘题目。做完这几件，这一周就算走得稳。</p>
        </div>
        <div class="inner-card">
          <p><strong>四步口诀，帮你记住：</strong>定住时间，拆小目标，放慢呼吸，回到题干。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「时间、小步、放慢、回到」这四个词，说说你上一次考试本来可以怎么安排。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "写下你考前最典型的一天，从起床到睡觉逐段标出来，看看睡眠和留白各占了多少。",
            "写出「拆小目标」和「降低要求」的区别，各用一句话说明。",
            "说出考场上当场能做的两个动作，并写清每一个具体怎么做。",
        ],
        [
            "用安排台排出你自己的七天，让可持续度尽量高，再写一句话说明为什么这样排。",
            "找出最近一次考完之后的三个想法，判断它们分别属于「复盘题目与时间」还是「复盘情绪」。",
        ],
        [
            "连续记录一次考试的全过程：考前两晚的安排、考场上的一个动作、考后的一次复盘，各写一句，一周后回看哪一项最管用。",
            "把四步口诀讲给一位同学听，再用他的一次真实经历一起走一遍，注意只从「复盘题目与时间」那一栏挑一件小事。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "psych-h-g11-exam-wellness",
    "node_id": "psych-h-g11-exam-wellness",
    "subject": "psychology",
    "subject_cn": "心理健康",
    "stage": "high",
    "stage_cn": "高中",
    "curriculum": "中小学心理健康教育指导纲要（2012年修订）/ 教育部相关要求 · 高中",
    "title": "考试心理与身心健康：把状态调稳，而不是把弦绷紧",
    "name_en": "Exam Wellbeing and Self-Regulation",
    "grade": 11,
    "grade_cn": "高二",
    "domain": "resilience",
    "domain_cn": "抗挫与适应",
    "lesson_type": "workshop",
    "version": "1.0.0",
    "description": "面向高二学生的考试心理与身心健康课：先讲考前一周要稳住的两件事——睡觉与起床的时间不要前后飘、把复习目标拆到当天做得完；再用核心模拟「考前一周安排台」排出七天（稳 / 赶 / 松 / 熬四种排法），看这个安排一周下来撑不撑得住；再练临场当场能做的两个动作——把呼吸放慢、把注意力交回题干第一句，并用「临场应对选择台」比较心慌、卡题、想放弃三种情况下不同做法可能的走向；最后用「考后复盘台」把复盘对准题目与时间安排，而不是对着情绪反复回放。全课明确写出这些做法不保证考得更好、只让状态可调、节奏可控，语气温和、不评判、不贴标签，不做紧张放大，不出现任何诊断性表述。",
    "tags": ["考试压力", "作息与睡眠节律", "拆小目标", "临场调节", "考后复盘", "高二"],
    "standard_ref": "《中小学心理健康教育指导纲要（2012年修订）· 高中》抗挫与适应——积极应对考试压力，保持身心健康；掌握科学的减压与身心调节方法。",
    "hero_question": "考前这一周，除了更用力，还能做点什么？",
    "hero_alt": "考试心理与身心健康知识结构图三栏：考前一周的节奏、临场两个动作、考后复盘",
    "hero_caption": "考前一周：守住时间、拆小目标 · 临场：放慢呼吸、回到题干 · 考后：复盘题目，不复盘情绪",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个最贴近你最近状态的困惑，后面的内容都会围着它展开。",
    "anchor_choices": [
        {"t": "考前这一周该怎么安排？", "d": "想多复习一点，又怕把自己耗空", "v": "考前这一周该怎么安排"},
        {"t": "考场上突然慌了、卡住了怎么办？", "d": "一紧张就读不进题，越急越乱", "v": "考场上突然慌了卡住了怎么办"},
        {"t": "考完之后该怎么看这次结果？", "d": "一直回放当时的画面，越想越沉", "v": "考完之后该怎么看这次结果"},
        {"t": "睡不好、作息乱了要不要紧？", "d": "越想早点睡，越躺不着", "v": "睡不好作息乱了要不要紧"},
    ],
    "objectives": [
        "能说出考前一周里睡眠和复习各自该留出多少空间，并给自己排一份七天都撑得住的安排",
        "会把一个大目标拆成当天做得完的小步，并说清判断这一步够不够小的标准",
        "会用在考场上当场能做的两个动作：把呼吸放慢，把注意力交回题干第一句",
        "能把考后复盘对准题目和时间安排，而不是对着自己的情绪反复回放",
    ],
    "objectives_plain": [
        "能说出考前一周里睡眠和复习各自该留出多少空间，并给自己排一份七天都撑得住的安排",
        "会把一个大目标拆成当天做得完的小步，并说清判断这一步够不够小的标准",
        "会用在考场上当场能做的两个动作：把呼吸放慢，把注意力交回题干第一句",
        "能把考后复盘对准题目和时间安排，而不是对着自己的情绪反复回放",
    ],
    "standards": [
        {"content": "积极应对考试压力，保持身心健康",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》高中 · 抗挫与适应"},
        {"content": "掌握科学的减压与身心调节方法",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》高中 · 抗挫与适应"},
    ],
    "prereqs": ["psych-h-g11-emotion-resilience"],
    "prereqs_name": "情绪管理与抗挫力",
    "prereqs_meta": "psych-h-g11-emotion-resilience",
    "leads_to": ["psych-h-g11-peer-support"],
    "next_meta": "psych-h-g11-peer-support",
    "section_images": ["assets/psych-h-g11-exam-wellness-fig1.webp", "assets/psych-h-g11-exam-wellness-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "除了更用力，考前这一周还能做点什么——这个问题先放在心里往下看。",
        "problem-anchor": "先定一个小目标：这节课结束时，你手上有自己的七天安排和两个临场动作。",
        "objectives": "看清四件事：守住时间、拆小目标、临场两个动作、考后复盘两栏。",
        "pretest": "凭平时的习惯选就好，不打分。前测只是帮你看清自己现在怎么安排考前的节奏。",
        "module-1": "睡觉和起床的时间先立住，再把复习目标拆到今天做得完。",
        "lab-1": "七天各点一种排法，看可持续度怎么变——它算的是撑不撑得住。",
        "module-2": "两个动作：把呼吸放慢，把注意力交回题干第一句。",
        "lab-2": "三种情况各点一个做法，比较它们可能把后面带到哪里。",
        "worked-example": "五步：定时间、拆目标、排七天、临场两动作、考后复盘三件事。",
        "conceptest-1": "三个选项里藏着最常见的几个误解，选完请把每条解释读一遍。",
        "synthesis": "八句话各选一栏，全部点完会看到一段小结。",
        "posttest": "考前两晚、考场中间、回家路上，三个新情境看看方法还在不在。",
        "summary": "记住四步口诀：定住时间，拆小目标，放慢呼吸，回到题干。",
        "homework": "三层练习，前两层做完就算通关，第三层留给愿意更进一步的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先帮你找到卡点，再给一个最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是高中「抗挫与适应」板块里长期空缺的一课。设计上不讲大道理，只把考前这一段拆成三个可以动手的地方。核心模拟是「考前一周安排台」——七天，每天在稳、赶、松、熬四种排法里点一种，右边实时给出可持续度，算的不是分数而是这个安排一周下来撑不撑得住；第二个台子是「临场应对选择台」，把心慌、卡题、想放弃三种情况和三种做法摆开，比较它们可能把后面带到哪里；综合任务用「考后复盘台」把八句话分成复盘题目与时间、复盘情绪两栏。全课明确写出这些做法不保证考得更好、只让状态可调、节奏可控，不放大紧张，语气温和、不评判、不贴标签。",
    "plan_table": """| 1 | cover | 考试心理与身心健康：把状态调稳，而不是把弦绷紧 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：考前的你，习惯怎么安排？ | 起·前测（暴露现有习惯） |
| 5 | concept | 考前一周：先稳住两件事 | 承·概念一（作息节律 + 拆小目标） |
| 6 | interactive | 核心模拟：考前一周安排台 | 承·核心模拟（七天 × 四种排法 → 可持续度） |
| 7 | concept | 临场那几分钟：两个当场能做的动作 | 承·概念二（放慢呼吸 + 回到题干） |
| 8 | interactive | 选择台：临场那几分钟，你会怎么做？ | 承·练习台（三种情况 × 三种做法） |
| 9 | concept | 例题示范：考前七天，五步走一遍 | 转·重难点突破（五步示范 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：考后复盘台 | 合·复盘分栏（迁移应用） |
| 12 | quiz | 后测：换几个新情境，看看方法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把这一周讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：考前一周的节奏、临场两个动作、考后复盘 三栏\n- P5 睡眠节律与拆步示意图（已生成）：左边日历与睡眠时段、右边逐级变小的方块\n- P7 临场两个动作示意图（已生成）：一条放慢的呼吸曲线与一个聚焦圈\n- 若需补充：一张可打印的七天安排空白表、一张考后复盘三栏表",
}
