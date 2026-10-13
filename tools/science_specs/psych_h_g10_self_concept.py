# -*- coding: utf-8 -*-
"""高中 · 心理健康 · 自我认同与理想信念（高一）—— 补齐知识树「认识自我」空缺

铁规：语气温和、不评判、不贴标签；不出现任何临床诊断词汇，不涉及自伤自杀与暴力情节。
不灌输价值观、不替学生定理想；落点是「可以慢慢想清楚」。
核心模拟：自我三圈梳理台（我看重的 / 别人期待我的 / 我实际在做的 → 落差与重合）。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/psych-h-g10-self-concept-fig1.webp'
F2 = './assets/psych-h-g10-self-concept-fig2.webp'

TTS = {
    "hero": "先做一件很小的事。请你在心里回答一句话：我是谁。你会发现，答案可能是学生、是某个人的朋友、是喜欢某件事的人，也可能是别人嘴里那个不太爱说话的人。这些答案都对，可是哪一个才算数？这节课我们不急着定答案，只做一件事——把关于自己的那些说法分开放好，再慢慢看清它们。",
    "problem-anchor": "在开始之前，先选出最贴近你此刻的一个困惑。是想知道自己到底是个什么样的人，还是想弄清别人的评价该听几分，又或者只是想找一找将来可能的方向。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出自我认识有很多面，一个标签遮不住全部。第二，会用三圈梳理台，把我看重的、别人期待我的、我实际在做的分开放好。第三，能区分一句评价里关于一件事的部分和关于我这个人的部分。第四，能写出一段属于自己的方向草稿，并知道它可以慢慢改。",
    "pretest": "先做三道小题，凭你现在的想法选就行，没有对错，也不打分。选完会立刻出现解释，正好帮你看清自己现在怎么看自己。",
    "module-1": "我们先看清楚一件事。别人认识你，通常是从一个标签开始的：成绩好、话少、坐得住。标签有用，它能让别人很快认出你，但它只是其中一面。真实的你还有别的部分：你在意什么、你和谁在一起最放松、你做什么事会忘记时间。常见的错误是把别人给的一个标签当成对自己的结论，于是把别的部分都收了起来。分清标签和你自己，是这节课的第一步。",
    "lab-1": "现在来做这台梳理台。下面有一排卡条，每一条都是关于你的一句实在话。你可以先选一条，再把它放进三个圈里最合适的那一个：我看重的、别人期待我的、我实际在做的。全部放完之后，我们一起看三个圈叠起来是什么样子。",
    "module-2": "三个圈放在一起，会出现两种东西：重合和落差。重合的地方，是别人期待的和你在意的一致，这样的期待可以借力；落差的地方更值得看看。比如你很看重把事情做扎实，可实际时间大半花在刷手机上，这就是落差。请注意，看出落差不是要批评自己，它只是把情况说清楚——说清楚了，才知道下一步可以从哪里动。",
    "lab-2": "再看一件事。我们每天都会听到关于自己的评价，有的让人心里一沉。这里准备了四个情境，每个情境下有三种处理方式，你可以轮流点开，看看它们各自可能会把你带到哪里。",
    "worked-example": "我们完整走一遍。情境是：有人对你说，你这次考得这么差，就是因为你不够努力。第一步，先停一下，看清是谁、在什么情况下说的。第二步，把这句话拆成两部分：一部分关于这件事，比如这周确实有几个晚上没有复习；一部分关于我这个人，比如你不够努力。第三步，核对能核对的部分。第四步，划掉不能核对的部分。第五步，只在能核对的那部分里，写一件明天可以做的小事。整套走完你会发现，一句让人难受的话，里面常常只有一小块是真正属于你的。",
    "conceptest-1": "现在用三个容易弄混的说法考考你。请仔细读每一个选项，选出你认为更合适的那个，然后看解释。",
    "synthesis": "最后做一件轻松一点的事。下面有三组线索卡，每一组都可以多选。选好之后点一下生成，就会得到一段属于你的方向草稿。它只是一份草稿，随时可以改，也允许你现在还没有答案。",
    "posttest": "最后换几个新情境检验一下。这次的问题出现在成绩单、家里的饭桌和一条朋友圈评论里，看看你能不能用上前面说过的方法。",
    "summary": "这节课我们弄明白了三件事。第一，标签只是你的一面，别人给的说法是一条信息，不是关于你的结论。第二，三圈梳理台能帮你看清重合和落差，看出落差不是批评自己，只是把情况说清楚。第三，方向可以是一段草稿，慢慢改就好。所以回到开头那个问题——我是谁，这节课不给你答案，但你已经有了把它慢慢想清楚的方法。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出三个别人常用来形容你的说法，再各写一句你自己更认可的说法。第二层能力应用，动手做：把三圈梳理台在纸上完整做一遍，找出重合的一处和落差的一处。第三层迁移挑战，选做：写一段三百字以内的方向草稿，过一个月再拿出来读，看看有什么变化。",
    "knowledge-graph": "这张图展示了这节课在知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 标签只是其中一面", "lab-1": "核心模拟 自我三圈梳理台", "module-2": "概念二 重合与落差",
    "lab-2": "练习台 评价该怎么听", "worked-example": "例题讲解", "conceptest-1": "概念测试",
    "synthesis": "综合任务 我的方向草稿", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

CUSTOM_JS = r"""
/* ============================================================
   psych-h-g10-self-concept 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 核心模拟：自我三圈梳理台（卡条 → 我看重的 / 别人期待我的 / 我实际在做的）
   3) 评价该怎么听：4 个情境 × 3 种处理 → 可能把你带到哪里
   4) 我的方向草稿：三组线索多选 → 生成一段草稿
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

  /* ---------- 2. 自我三圈梳理台 ---------- */
  var RINGS = {
    value: { n: '我看重的', d: '我在意什么、愿意为什么花力气' },
    expect: { n: '别人期待我的', d: '家人、老师、同学希望我成为的样子' },
    doing: { n: '我实际在做的', d: '我的时间真正花在哪里' }
  };
  var CARDS = [
    { id: 'c1', t: '我希望自己说话算数', home: 'value' },
    { id: 'c2', t: '家里人希望我选理科', home: 'expect' },
    { id: 'c3', t: '我答应自己的事，常常拖到最后一刻', home: 'doing' },
    { id: 'c4', t: '我在意身边的人是不是过得还好', home: 'value' },
    { id: 'c5', t: '同学觉得我话少，应该再活泼一点', home: 'expect' },
    { id: 'c6', t: '我每天的时间，大半花在刷手机和补作业上', home: 'doing' },
    { id: 'c7', t: '我愿意为自己感兴趣的事熬到很晚', home: 'value' },
    { id: 'c8', t: '老师希望我成绩再往上冲一冲', home: 'expect' },
    { id: 'c9', t: '我每周真正坐下来练习的时间，比计划少很多', home: 'doing' }
  ];
  var placed = {};
  var selId = null;
  var ringStage = document.getElementById('ring-stage');
  if (ringStage) {
    function renderRing() {
      var bank = document.getElementById('ring-bank');
      if (selId && placed[selId]) selId = null;
      if (!selId) {
        var first = CARDS.filter(function (c) { return !placed[c.id]; });
        if (first.length) selId = first[0].id;
      }
      bank.innerHTML = CARDS.map(function (c) {
        if (placed[c.id]) return '';
        var on = c.id === selId
          ? ' style="border-color:var(--brand);background:var(--brand-soft)"' : '';
        return '<button class="sort-item" data-ring-card="' + c.id + '"' + on + '>' + c.t + '</button>';
      }).join('') || '<span style="color:var(--muted);font-size:14px">卡条都放好了，看看三个圈叠起来的样子。</span>';

      var bins = document.getElementById('ring-bins');
      bins.innerHTML = Object.keys(RINGS).map(function (k) {
        var R = RINGS[k];
        var inside = CARDS.filter(function (c) { return placed[c.id] === k; }).map(function (c) {
          var ok = c.home === k;
          return '<span class="tag" style="' + (ok ? '' : 'border-color:rgba(251,191,36,.65)') + '">' +
            c.t + (ok ? ' ✓' : ' ·?') + '</span>';
        }).join('') || '<span style="color:var(--muted);font-size:13px">还没放</span>';
        return '<div class="sort-bin" data-ring-bin="' + k + '"><h4>' + R.n + '<br>' +
          '<span style="font-weight:400;font-size:12px;color:var(--muted)">' + R.d + '</span></h4>' + inside + '</div>';
      }).join('');

      var total = Object.keys(placed).length;
      var out = document.getElementById('ring-out');
      if (total === 0) {
        out.className = 'result warn';
        out.innerHTML = '<strong>先选一条卡条，再点它最合适的那一个圈。</strong>放得不合适也没关系，这里没有标准答案，只有更像你或者不太像你。';
      } else if (total < CARDS.length) {
        out.className = 'result warn';
        out.innerHTML = '<strong>已经放好 ' + total + ' / ' + CARDS.length + ' 条。</strong>带着 ✓ 的表示这条和你放的位置比较贴；带 ·? 的说明它还能放进别的圈——不是错，只是值得再看一眼。';
      } else {
        out.className = 'result';
        out.innerHTML = '<strong>九个位置都放好了，来看三个圈叠起来的样子。</strong><br>' +
          '① <strong>重合处</strong>：别人期待的和你在意的正好对上的地方，这些期待可以借力。' +
          '② <strong>落差处</strong>：你很看重、但实际时间没花上去的地方——它只是把情况说清楚了，不是要批评你。' +
          '③ <strong>借来的目标</strong>：只落在别人期待里、你自己既不在意也没在做的那一条，可以先放在这儿，不用马上处理。';
      }

      document.querySelectorAll('[data-ring-card]').forEach(function (b) {
        b.addEventListener('click', function () {
          selId = b.dataset.ringCard;
          renderRing();
        });
      });
      document.querySelectorAll('[data-ring-bin]').forEach(function (b) {
        b.addEventListener('click', function () {
          if (!selId) return;
          placed[selId] = b.dataset.ringBin;
          selId = null;
          renderRing();
        });
      });
    }
    renderRing();
  }

  /* ---------- 3. 评价该怎么听 ---------- */
  var SCENES2 = {
    score: {
      n: '考完试后有人说',
      s: '你这次考得这么差，就是因为你不够努力。',
      accept: '把一句针对这一次考试的话，听成了关于整个人的结论，接下来容易越想越没力气，也懒得再翻书。',
      reject: '这样能护住自己不受影响，但也可能把里面真正有用的那一小块一起丢掉，比如这周确实有几个晚上没复习。',
      unpack: '拆开看：这一句里，关于这件事的部分是「这次没考好，复习时间不够」；关于我这个人「不够努力」是一个判断。留下能核对的那一块，就已经知道下一步做什么了。'
    },
    group: {
      n: '同学群里有人说',
      s: '你怎么这么不合群，别人叫你都不去。',
      accept: '一句关于去不去某一次活动的话，被听成关于性格的定论，于是你可能开始躲着集体活动，反而让情况更像那句话。',
      reject: '直接顶回去能让自己舒服一点，不过也可能错过一个信息：同学其实是想让你一起来。',
      unpack: '拆开看：关于这件事的部分是「这次没去，大家有点失望」；关于我这个人「不合群」是别人的一个印象。你可以决定去不去，也可以说明原因，两件事可以分开。',
    },
    parent: {
      n: '家里饭桌上有人说',
      s: '我们为你付出这么多，你要争气。',
      accept: '把这句话全接下来，容易变成一份越来越重的心债，做事的时候先想的是怕让人失望，而不是自己想做什么。',
      reject: '完全挡回去能保住自己，不过也可能把这句话里那份在意一起关在门外，家里的气氛会僵住。',
      unpack: '拆开看：这句话里有他们的担心和期待，也有一部分是他们自己的着急。你可以听见他们的在意，同时把目标和节奏放在自己手上——这两件事并不冲突。',
    },
    level: {
      n: '有同学对你说',
      s: '你也就这个水平了。',
      accept: '这类把人和水平钉死的话，一旦接下来，最容易让人提前给自己划一个上限，连试都懒得试。',
      reject: '不理会是合适的，同时也可以留意一下：他说的是哪一次、哪一方面，有没有一条具体的信息值得留下来。',
      unpack: '拆开看：这句话里几乎没有关于具体事情的部分，它主要是对方的一个判断。所以你可以把它放在一边，不必用它来定义自己的范围。',
    }
  };
  var HANDLE = { accept: '全盘接受', reject: '全盘弹开', unpack: '拆开看看' };
  var say2Stage = document.getElementById('say2-stage');
  if (say2Stage) {
    var scene2 = 'score', how = 'unpack';
    function renderSay2() {
      var S = SCENES2[scene2];
      document.getElementById('say2-line').textContent = S.n + '：' + S.s;
      document.querySelectorAll('[data-say2-scene]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.say2Scene === scene2);
      });
      document.querySelectorAll('[data-say2-how]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.say2How === how);
      });
      var out = document.getElementById('say2-out');
      out.className = 'result ' + (how === 'unpack' ? '' : 'warn');
      out.innerHTML = '<strong>' + HANDLE[how] + '，这样可能会：</strong>' + S[how] +
        (how === 'unpack' ? '<br>把评价分成「关于这件事」和「关于我这个人」，你只需要处理前者。'
          : '<br>还可以试试第三种：先拆开看看，再决定留哪一部分。');
    }
    document.querySelectorAll('[data-say2-scene]').forEach(function (b) {
      b.addEventListener('click', function () { scene2 = b.dataset.say2Scene; renderSay2(); });
    });
    document.querySelectorAll('[data-say2-how]').forEach(function (b) {
      b.addEventListener('click', function () { how = b.dataset.say2How; renderSay2(); });
    });
    renderSay2();
  }

  /* ---------- 4. 我的方向草稿 ---------- */
  var CLUES = {
    time: {
      t: '什么事会让我忘记时间',
      items: ['动手做东西', '写点自己的东西', '跟人聊很久', '解出一道难题', '运动', '整理和归类', '照顾小孩或小动物', '看纪录片']
    },
    help: {
      t: '别人常来找我帮什么',
      items: ['讲题', '听他说心事', '修东西', '整理资料', '组织活动', '帮着拿主意']
    },
    pay: {
      t: '没人要求我也愿意多花力气的事',
      items: ['把事情做得漂亮一点', '让别人少为难一点', '把一个原理弄清楚', '把安排理清楚']
    }
  };
  var picked = {};
  var draftStage = document.getElementById('draft-stage');
  if (draftStage) {
    function renderDraft() {
      document.getElementById('draft-groups').innerHTML = Object.keys(CLUES).map(function (g) {
        var G = CLUES[g];
        var btns = G.items.map(function (it) {
          var on = picked[g + '|' + it];
          return '<button class="choice' + (on ? ' selected' : '') + '" data-draft="' + g + '|' + it +
            '" style="text-align:center;font-size:13px">' + it + '</button>';
        }).join('');
        return '<div class="slider-row" style="display:block">' +
          '<div style="font-weight:700;font-size:14px">' + G.t + '</div>' +
          '<div class="flex-row" style="flex-wrap:wrap">' + btns + '</div></div>';
      }).join('');
      document.querySelectorAll('[data-draft]').forEach(function (b) {
        b.addEventListener('click', function () {
          var k = b.dataset.draft;
          picked[k] = !picked[k];
          renderDraft();
        });
      });
    }
    function listOf(g) {
      return Object.keys(picked).filter(function (k) {
        return k.indexOf(g + '|') === 0 && picked[k];
      }).map(function (k) { return k.split('|')[1]; });
    }
    renderDraft();
    document.getElementById('draft-build').addEventListener('click', function () {
      var a = listOf('time'), b = listOf('help'), c = listOf('pay');
      var out = document.getElementById('draft-out');
      if (!a.length && !b.length && !c.length) {
        out.className = 'result warn';
        out.textContent = '先在上面勾几条线索吧，一条也行。';
        return;
      }
      var s = [];
      if (a.length) s.push('我可能会在「' + a.join('、') + '」这些事情里比较有劲。');
      if (b.length) s.push('身边的人常来找我「' + b.join('、') + '」，这大概是我用得上的地方。');
      if (c.length) s.push('就算没人要求，我也愿意「' + c.join('、') + '」。');
      s.push('这三条线指向的方向，现在还不必说清楚。它只是一份草稿——可以慢慢改，也允许暂时空着。');
      out.className = 'result';
      out.innerHTML = '<strong>我的一号方向草稿：</strong><br>' + s.join('<br>');
    });
    document.getElementById('draft-clear').addEventListener('click', function () {
      picked = {};
      renderDraft();
      var out = document.getElementById('draft-out');
      out.className = 'result warn';
      out.textContent = '已经清空，可以重新勾一遍。';
    });
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：你怎么看自己？", TTS["pretest"], [
        {"q": "有人说你「就是不太爱说话」。下面哪种想法对你更有帮助？",
         "options": [("这就是我这个人，改不了", False),
                     ("这只是别人看到的一面，我还有别的部分", True),
                     ("那我以后干脆一句话都不说", False)],
         "explain": "标签只是其中一面，它描述的是别人观察到的部分，不是关于你的结论。<strong>错因提醒：</strong>常见错误是把别人给的一个标签当成对自己的定论，于是把别的部分都收了起来。"},
        {"q": "你发现自己很看重把事做扎实，但实际时间大半花在刷手机上。比较合适的是：",
         "options": [("承认自己就是懒，不用再看", False),
                     ("把这个落差看清楚，它就是下一步的线索", True),
                     ("马上给自己定一个特别严的计划", False)],
         "explain": "看出落差不是批评自己，只是把情况说清楚，说清楚了才知道从哪里动。<strong>错因提醒：</strong>容易把「看出落差」误认为「给自己定罪」，这两种心态带来的结果差得很远。"},
        {"q": "关于「我想成为什么样的人」，下面哪种说法更贴近这节课的想法？",
         "options": [("必须现在就想清楚，想不清就是没出息", False),
                     ("可以先是一份草稿，慢慢改", True),
                     ("照别人给你安排的路走最省事", False)],
         "explain": "方向可以边经历边清晰，一份能改的草稿比一个硬想出来的答案更耐用。<strong>错因提醒：</strong>误认为理想必须一次定好，是很多同学迟迟不敢动笔的原因。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "标签只是其中一面，不是关于你的结论", TTS["module-1"], f'''
        <p style="font-size:17px;margin:0 0 12px">别人认识你，常常是从一个词开始的。这个词有用，但它遮不住全部的你。</p>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(251,191,36,.45)">
          <p style="margin:0"><strong>为什么要先学这个？</strong>你已经知道自己有多面；但别人给你的说法只有一个词，听多了容易当成全部；所以得先把「标签」和「我」分开。</p>
        </div>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>标签是什么</strong></p>
            <p style="color:var(--muted)">标签是别人从某几次观察里抽出来的一个词：成绩好、话少、坐得住。它<strong>称为</strong>别人对你的一个印象，不是对你的判决。</p>
          </div>
          <div class="inner-card">
            <p><strong>你还有什么</strong></p>
            <p style="color:var(--muted)">你在意什么、和谁在一起最放松、做什么事会忘记时间、别人常来找你帮什么忙——这些同样属于你。</p>
          </div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">误认为「别人都这么说，那我就是这样」。一个词越被重复，越像真的，可它仍然只是一个词。</p>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="三个相交的圆圈示意图：我看重的、别人期待我的、我实际在做的">
          <figcaption>三个圈各有各的内容，叠在一起的部分是重合，没叠上的部分是落差——先把它们分开放，才看得清</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🧩</span><div><strong>小提示：</strong>分清标签和你自己，就像把别人贴在你身上的便利贴拿下来看一眼，而不是把它当成脸。</div></div>
{insight_box([
    {"lens": "看见它", "text": "同一个人可以在老师眼里安静、在球场上喊得最大声、在好朋友面前话最多——三个都是真的，只是场景不同。"},
    {"lens": "解释它", "text": "为什么一个标签这么容易变重？因为人习惯用最少的信息做判断，标签省事，于是就留下来了。"},
    {"lens": "迁移它", "text": "这条规律对别人也一样成立：你给同学贴的那个词，多半也只是他的其中一面。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "ring", 5, "lab-1", "核心模拟：自我三圈梳理台", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一条卡条，再点它更贴的那个圈。九个都放好之后，看看三个圈叠起来是什么样子。</p>
        <div class="lab-panel" id="ring-stage">
          <div class="sort-bank" id="ring-bank"></div>
          <div class="sort-bins" id="ring-bins"></div>
          <p class="result warn" id="ring-out" style="margin-top:14px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>放完之后再看一眼：</strong>哪一条让你最想把它挪到别的圈里？那个犹豫的地方，往往就是你现在最在意的事。</div></div>
    ''', tag="核心模拟", bloom="analyze"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "三个圈叠起来：重合值得借力，落差值得看看", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">三圈放好之后，会自然出现两种结果：对得上和对不上。它们都不评价你，只提供线索。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>重合：</strong>别人期待的和你在意的正好对上。这样的期待可以借力，不用一个人硬撑。</div></div>
          <div class="step"><span class="n">2</span><div><strong>落差：</strong>你很看重，但时间没花上去。它不是结论，是你下一步可以选的地方。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>借来的目标：</strong>只在别人期待里、你自己既不在意也没在做的那一条，可以先放着，不必马上处理。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="一句话被拆成两部分的示意图：关于这件事的部分与关于我这个人的部分">
          <figcaption>三个圈之外还有一个动作：把听到的说法拆成两部分——关于这件事的留下核对，关于我这个人的先放一边</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">⚖️</span><div><strong>换个说法：</strong>落差就像体重秤上的数字，它告诉你现在的状态，不负责给你打分。看不看是你的事，看清了更容易选下一步。</div></div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "say2", 7, "lab-2", "练一练：一句评价，你可以怎么听", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先选一个情境，再轮流点开三种处理方式，看看它们可能把你带到哪里。</p>
        <div class="lab-panel" id="say2-stage">
          <div class="flex-row" style="flex-wrap:wrap">
            <button class="choice" data-say2-scene="score" style="text-align:center">考完试后有人说</button>
            <button class="choice" data-say2-scene="group" style="text-align:center">同学群里有人说</button>
            <button class="choice" data-say2-scene="parent" style="text-align:center">家里饭桌上有人说</button>
            <button class="choice" data-say2-scene="level" style="text-align:center">有人说你也就这个水平</button>
          </div>
          <p class="result" id="say2-line" style="margin-top:12px"></p>
          <div class="flex-row" style="flex-wrap:wrap">
            <button class="choice" data-say2-how="accept" style="text-align:center">全盘接受</button>
            <button class="choice" data-say2-how="reject" style="text-align:center">全盘弹开</button>
            <button class="choice" data-say2-how="unpack" style="text-align:center">拆开看看</button>
          </div>
          <p class="result warn" id="say2-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💬</span><div><strong>四个情境都点一遍，你发现了什么？</strong>三种方式都不是错，只是它们各自会把你带到不同的地方。<strong>拆开看看</strong>通常最省力，因为你不必接受全部，也不必拒绝全部。</div></div>
    ''', tag="动手实验室", bloom="analyze"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：一句让人心里一沉的话，怎么拆开看", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(251,191,36,.45)">
          <p style="margin:0"><strong>情境：</strong>有人对你说，你这次考得这么差，就是因为你不够努力。这句话让你心里一沉，接下来一整晚都不太想说话。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先停一下：</strong>看清是谁、在什么情况下说的。他可能只是随口一句，也可能是真的着急——先不急着回应。</div></div>
          <div class="step"><span class="n">2</span><div><strong>拆成两部分：</strong>关于这件事的是「这次没考好、复习时间不够」；关于我这个人的是「不够努力」这个判断。</div></div>
          <div class="step"><span class="n">3</span><div><strong>核对能核对的：</strong>这周确实有几个晚上没复习——这一部分是真实的，可以留下。</div></div>
          <div class="step"><span class="n">4</span><div><strong>划掉不能核对的：</strong>「不够努力」是关于人的判断，不适合用来定义你整个人，先放在一边。</div></div>
          <div class="step"><span class="n green">5</span><div><strong>只留一件小事：</strong>明天晚自习先把错题里最想不通的那两道翻一遍。范围小到一定做得到，才叫下一步。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">常见错误是把一句评价直接当成关于自己的结论，于是要么整晚难受，要么干脆一句话都听不进去。其实一句话里通常只有一小块属于你：<strong>关于这件事</strong>的部分留下，<strong>关于我这个人</strong>的部分放一边。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "关于「别人怎么看我」，下面哪种想法更合适？",
         "options": [("别人怎么看我，就是关于我的结论", False),
                     ("别人的说法是一条信息，我可以核对后再决定留不留", True),
                     ("别人的看法完全不重要，一律不听", False)],
         "explain": "把评价当成信息来处理，比当成结论来接受或拒绝都好用。<strong>错因提醒：</strong>常见错误是走两个极端——要么全收，要么全挡，这两种都会让你少掉一条可能有用的信息。"},
        {"q": "「我很看重把身体练好，但实际每周一次都没动」——这段话最像三圈里的哪一种情况？",
         "options": [("重合", False), ("落差", True), ("借来的目标", False)],
         "explain": "看重和实际做法对不上，就是落差。它只描述现状，不等于你不自律。<strong>错因提醒：</strong>容易把落差误认为对自己的批评，于是要么放着不看，要么立刻定一个过严的计划，三天就散了。"},
        {"q": "关于「我想成为什么样的人」，下面哪种做法更接近这节课的建议？",
         "options": [("先写一份草稿，过一段时间再看一眼", True),
                     ("等一个完美的答案出现再动笔", False),
                     ("把家里人的期待直接抄下来当答案", False)],
         "explain": "方向是边走边清晰的，草稿可以改。<strong>错因提醒：</strong>把「还没想清楚」和「我不行」搞混，是很常见的误解——没想清楚只是还没到时候。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "draft", 10, "synthesis", "综合任务：写一段属于我的方向草稿", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">三组线索都可以多选，选好点一下生成，看看它们拼起来指向哪里。它只是草稿，随时可以清空重来。</p>
        <div class="lab-panel" id="draft-stage">
          <div id="draft-groups"></div>
          <div class="flex-row">
            <button class="choice" id="draft-build" style="text-align:center">生成我的方向草稿</button>
            <button class="choice" id="draft-clear" style="text-align:center">清空重来</button>
          </div>
          <p class="result warn" id="draft-out" style="margin-top:12px">还没有勾选。先随便点两条也可以——草稿本来就是用来改的。</p>
        </div>
        <div class="inner-card">
          <p><strong>写下来，留给自己：</strong></p>
          <p style="color:var(--muted)">这段草稿里，哪一句你自己看了最想点头？把它抄在手机备忘录里，过一个月再读一遍。</p>
          <textarea id="syn-answer" rows="3" placeholder="我自己最想点头的一句是……" style="margin-top:8px"></textarea>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🌱</span><div><strong>请记住一句话：</strong>这节课不替你定理想，也不会催你现在就有答案。方向可以在往后的经历里慢慢清晰，<strong>可以慢慢想清楚</strong>。</div></div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，看看方法还在不在", TTS["posttest"], [
        {"q": "成绩单发下来，比预期低了一些。下面哪种做法更用得上这节课的方法？",
         "options": [("先把「这次哪几块没拿到分」看清楚，再挑一块最想弄明白的", True),
                     ("告诉自己我大概就是这个水平了", False),
                     ("把成绩单收起来不看，也先不处理", False)],
         "explain": "把「这一次的结果」和「我这个人」分开看，是这节课最核心的动作。"},
        {"q": "饭桌上，家里人说「隔壁孩子都考那么高，你怎么回事」。整理一下，这句话里可以留下的是：",
         "options": [("他们很在意你的成绩，也担心你的将来", True),
                     ("我不如隔壁那个同学", False),
                     ("家里人根本不了解我，没什么好说的", False)],
         "explain": "留下能核对的担心，放下拿你和别人比较的那部分。<strong>错因提醒：</strong>常见的是全盘接下或者全盘顶回，两边都很消耗。"},
        {"q": "有同学在朋友圈评论说「你这照片拍得真难看」。你可以：",
         "options": [("把「难看」当成一句关于人的判断，先放在一边", True),
                     ("立刻回一句更难听的", False),
                     ("删掉所有照片，以后再也不发", False)],
         "explain": "一句关于照片好不好看的话，并不负责定义你这个人。<strong>错因提醒：</strong>把针对某件事的评价，误认为关于自己的结论，是这一课最容易搞混的地方。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把自己讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>标签只是一面</strong>：别人给的说法是一条信息，不是关于你的结论。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>三圈梳理台</strong>：我看重的、别人期待我的、我实际在做的——重合可借力，落差是线索。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>方向是草稿</strong>：可以改，也允许暂时空着，它会在往后的经历里慢慢清晰。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(251,191,36,.45)">
          <p style="margin:0"><strong>回到开头那个问题——我是谁：</strong>这节课不给你答案。但你已经有了工具：把说法分开放好，把评价拆成两半，把方向写成草稿。有这三样，这个问题就可以慢慢想清楚。</p>
        </div>
        <div class="inner-card">
          <p><strong>小口诀，帮你记住这三步：</strong>标签拿下来看一眼，评价拆成两半走，方向写成草稿慢慢修。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「看重、期待、实际」这三个词，说说你身上一处重合和一处落差。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "写出三个别人常用来形容你的说法，再各写一句你自己更认可的说法，列成两栏对照。",
            "写出三圈梳理台里三个圈各自的含义，各用一句话说明。",
        ],
        [
            "在纸上把三圈梳理台完整做一遍，至少各放三条卡条，标出你找到的一处重合和一处落差。",
            "找一句最近听到的、让你有点在意的评价，按例题的五步把它拆开，写下你留下的那一小部分。",
        ],
        [
            "写一段三百字以内的方向草稿，放进手机备忘录；一个月后拿出来读一遍，把有变化的地方标出来。",
            "观察身边一位同学，试着说出他身上的三个不同侧面，用来提醒自己：标签从来只是其中一面。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "psych-h-g10-self-concept",
    "node_id": "psych-h-g10-self-concept",
    "subject": "psychology",
    "subject_cn": "心理健康",
    "stage": "high",
    "stage_cn": "高中",
    "curriculum": "中小学心理健康教育指导纲要（2012年修订）/ 教育部相关要求 · 高中",
    "title": "自我认同与理想信念：把自己慢慢看清楚",
    "name_en": "Self-Identity and Personal Direction",
    "grade": 10,
    "grade_cn": "高一",
    "domain": "self-awareness",
    "domain_cn": "认识自我",
    "lesson_type": "workshop",
    "version": "1.0.0",
    "description": "面向高一学生的自我认识课：从「我是谁，哪一个答案才算数」这个现象出发，说明标签只是其中一面；核心模拟是「自我三圈梳理台」——把我看重的、别人期待我的、我实际在做的分开放好，从三个圈的重合与落差里看见线索；再用「评价拆开看」的五步示范，学会把一句评价分成关于这件事与关于我这个人两部分；最后用三组线索卡生成一段属于自己的方向草稿。全课不灌输价值观、不替学生定理想，落点是方向可以慢慢想清楚；语气温和、不评判、不贴标签，不出现任何诊断性表述。",
    "tags": ["自我认同", "标签与评价", "三圈梳理", "方向草稿", "高一"],
    "standard_ref": "《中小学心理健康教育指导纲要（2012年修订）· 高中》认识自我——帮助学生确立正确的自我意识，树立人生理想和信念；学会恰当地体验和表达自己，方向可以随经历逐步清晰。",
    "hero_question": "我是谁？别人说的和我想的，哪一个才算数？",
    "hero_alt": "自我认同知识结构图三栏：标签只是其中一面、三圈梳理台、方向可以慢慢清晰",
    "hero_caption": "自我认同：标签只是一面 · 三圈梳理看清重合与落差 · 方向写成草稿慢慢改",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个最贴近你此刻的困惑，后面的内容都会围着它展开。",
    "anchor_choices": [
        {"t": "我到底是个什么样的人？", "d": "别人说我是一回事，我自己感觉又是另一回事", "v": "我到底是个什么样的人"},
        {"t": "别人的评价该听几分？", "d": "有些话听完心里会沉很久", "v": "别人的评价该听几分"},
        {"t": "我好像找不到自己的方向", "d": "说不清自己在意什么、想往哪走", "v": "我好像找不到自己的方向"},
        {"t": "家里人的期待和我自己的不一样", "d": "两边都放不下，也不知道该听谁的", "v": "家里人的期待和我自己的不一样"},
    ],
    "objectives": [
        "能说出自我认识有很多面，一个标签遮不住全部，并举例说明",
        "会用三圈梳理台把我看重的、别人期待我的、我实际在做的分开放好，并指出重合与落差",
        "能把一句关于自己的评价拆成「关于这件事」和「关于我这个人」两部分，只留下可核对的部分",
        "能写出一段属于自己的方向草稿，并说明它可以随经历逐步调整",
    ],
    "objectives_plain": [
        "能说出自我认识有很多面，一个标签遮不住全部，并举例说明",
        "会用三圈梳理台把我看重的、别人期待我的、我实际在做的分开放好，并指出重合与落差",
        "能把一句关于自己的评价拆成「关于这件事」和「关于我这个人」两部分，只留下可核对的部分",
        "能写出一段属于自己的方向草稿，并说明它可以随经历逐步调整",
    ],
    "standards": [
        {"content": "帮助学生确立正确的自我意识，树立人生理想和信念",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》高中 · 认识自我"},
        {"content": "学会恰当地、正确地体验情绪和表达情绪，逐步形成对自我的稳定认识",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》高中 · 认识自我"},
    ],
    "prereqs": [],
    "prereqs_name": "本课为高中「认识自我」板块的起点",
    "prereqs_meta": "",
    "leads_to": ["psych-h-g10-learning-strategy"],
    "next_meta": "psych-h-g10-learning-strategy",
    "section_images": ["assets/psych-h-g10-self-concept-fig1.webp", "assets/psych-h-g10-self-concept-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "我是谁？别人说的和我想的，哪一个才算数——先带着这个问题往下看。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能把自己身上的三圈分开放好。",
        "objectives": "看清四件事：标签只是一面、三圈怎么放、评价怎么拆、方向怎么写草稿。",
        "pretest": "凭现在的想法选就好，不打分。前测只是帮你看清自己现在怎么看自己。",
        "module-1": "标签是别人从几次观察里抽出来的一个词，不是对你的判决。",
        "lab-1": "先点卡条，再点圈。带 ·? 的位置不是错，只是值得再看一眼。",
        "module-2": "重合可以借力，落差只是线索。看出落差不是批评自己。",
        "lab-2": "四个情境各点三种处理方式，看看它们分别把你带到哪里。",
        "worked-example": "五步：停下看清、拆成两半、核对能核对的、划掉不能核对的、只留一件小事。",
        "conceptest-1": "三个选项里藏着最常见的误解，选完请把每条解释读一遍。",
        "synthesis": "三组线索都能多选，生成后可以清空重来——草稿本来就是用来改的。",
        "posttest": "成绩单、饭桌、朋友圈，三个新情境看看方法还在不在。",
        "summary": "记住那个小口诀：标签拿下来看一眼，评价拆成两半走，方向写成草稿慢慢修。",
        "homework": "三层练习，前两层做完就算通关，第三层留给愿意更进一步的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先帮你找到卡点，再给一个最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是高中「认识自我」板块里长期空缺的一课。设计上不做价值灌输，也不替学生定理想，只做三件能自己动手的事：把关于自己的说法分开放好，把听到的评价拆成两半，把方向写成一份可以改的草稿。核心模拟是「自我三圈梳理台」——九条卡条分别归入我看重的、别人期待我的、我实际在做的三个圈，全部放完后自动给出重合、落差与借来的目标三种读法。第二个台子是「一句评价，你可以怎么听」，四个真实校园情境各配三种处理方式，学生自己比较它们分别把人带到哪里。综合任务用三组线索卡生成一段方向草稿，明确写出「它只是一份草稿，可以慢慢改」。全课语气温和、不评判、不贴标签，不出现任何诊断性表述。",
    "plan_table": """| 1 | cover | 自我认同与理想信念：把自己慢慢看清楚 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：你怎么看自己？ | 起·前测（暴露现有想法） |
| 5 | concept | 标签只是其中一面，不是关于你的结论 | 承·概念一（标签与自我） |
| 6 | interactive | 核心模拟：自我三圈梳理台 | 承·核心模拟（归位 + 重合与落差） |
| 7 | concept | 三个圈叠起来：重合值得借力，落差值得看看 | 承·概念二（三圈读法 + 评价拆分） |
| 8 | interactive | 练一练：一句评价，你可以怎么听 | 承·练习台（接受 / 弹开 / 拆开） |
| 9 | concept | 例题示范：一句让人心里一沉的话，怎么拆开看 | 转·重难点突破（五步示范 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：写一段属于我的方向草稿 | 合·迁移应用（线索卡 + 草稿生成） |
| 12 | quiz | 后测：换几个新情境，看看方法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把自己讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：标签只是一面、三圈梳理台、方向慢慢清晰 三栏\n- P5 三圈相交示意图（已生成）：三个抽象圆框，标出我看重的、别人期待我的、我实际在做的\n- P7 评价拆成两部分示意图（已生成）：一句话分成两块，一块留下核对，一块放在一边\n- 若需补充：一张可打印的三圈梳理台空白工作表、一张方向草稿卡片",
}
