# -*- coding: utf-8 -*-
"""小学信息科技 · 人工智能伦理与责任（G6）—— 补齐知识树「互联网与人工智能」空缺

学科语气：信息科技的价值判断部分——用生活情境做价值判断，不写技术原理，也不喊口号。
全课只做一件事：遇到一个具体情境，先说出你会怎么做，再跟着看它的后果。
两个互动都真的能操作：
  ① 情境 → 选做法 → 看后果：
     三个生活情境（换脸、用机器写作业、只推你爱看的），每个三种做法，
     选完立刻展开一条三步的后果链，再用三把尺子量一次。
  ② 只推你爱看的「信息小屋」：
     点几次「多看看这类」，看着内容池一类一类被挡住，直到只剩自己那一类；
     再点「我想看看别的」，看视野怎么宽回来。
最后收口到一句能带走的方法：
  问伤不伤人，问骗没骗人，问该不该我来做。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-e-ai-ethics-fig1.webp'
F2 = './assets/it-e-ai-ethics-fig2.webp'

TTS = {
    "hero": "先想三个画面。第一个，有人把同学照片里的脸换成别人的，做成搞笑视频发到群里。第二个，一篇作文是让机器写完的，交上去的时候，署名写的是自己。第三个，你刷到的内容越来越像，昨天喜欢什么，今天满屏都是什么，别的东西好像都不见了。这三件事里，机器其实都只是在干活，它没有做错什么。真正要做判断的，是使用它的人。这节课我们不下结论、不背口号，只做一件事：看到一个情境，先选出你会怎么做，再跟着看它的后果。",
    "problem-anchor": "开始之前，先选一个你最想弄明白的问题。是想知道用别人的照片做视频到底行不行，还是想知道让机器帮着写作业算不算作弊，又或者你想知道自己为什么总刷到同一类内容，再或者你更想弄清楚，判断这些事情该看哪几条标准。选好了，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能用自己的话说出，技术能做一件事，和人应该做一件事，是两个不同的问题。第二，面对一个具体情境时，能用三把尺子判断这件事该不该做。第三，能说清楚只推你爱看的内容，会带来什么后果。第四，能和同学一起，为班级写出一份能够照着做的机器使用约定。",
    "pretest": "先做三道小题，用你现在的想法选就行。这几道题不一定非黑即白，但每一种选择都会带来不一样的后果。选完马上能看到解释。",
    "module-1": "先把最重要的一句话放在前面：机器能不能做出这件事，和人该不该做这件事，是两个完全不同的问题。机器不会替你想第二个问题，它只会老老实实按你说的做。所以我们先看三个常见情境。第一个是换脸，把一个人的脸换到另一个人身上，技术上能做得出来，可如果没经过本人同意，被换脸的人会怎么样？第二个是让机器替你把作业写完，它确实能写出一篇看起来通顺的文章，可你交上去的时候，署的是自己的名字。第三个是只推你爱看的内容，你看着很舒服，可渐渐地，别的声音你就听不到了。这三件事，机器都在正常干活，做判断的是用它的人。",
    "lab-1": "现在请你当一次当事人。上面会出现一个生活里的情境，下面有三种做法，请你先点出你觉得自己会怎么做。点完之后会展开一条后果链，一步一步看下去，再用三把尺子量一次。三个情境都做完，你会发现：有些做法没有人受伤，有些做法一开始挺好，走到第三步就出了问题。",
    "module-2": "那到底怎么判断呢？给你三把尺子，遇到拿不准的事，用它们各量一次。第一把尺子问伤害：这件事会不会让某个人难受、被取笑、被误会？只要会伤到人，再好玩也要停。第二把尺子问真假：这件事会不会让别人以为一件不真实的事？换脸视频、编出来的消息，都在这把尺子下面。第三把尺子问本分：这件事本来该我自己完成的，是不是整个交给了机器？让机器帮忙查资料、改错字没有问题，让机器替你交作业，就过了线。",
    "lab-2": "接下来做一个小实验。下面是一个内容池，里面装着不同类别的十二条内容。你可以点某一类旁边的「多看看这类」，看看会发生什么。每点一次，别的内容就会被挡住一些。点到后面，你会发现池子里只剩你原来喜欢的那一类了。然后请点一下「我想看看别的」，看看视野能不能宽回来。",
    "worked-example": "我们一起把一道题想完整。老师布置了一次读书笔记，用机器帮忙算不算作弊？我们一步一步来。第一步，先问伤害：如果这份笔记是你自己读出来的，交上去对谁都没有伤害；可如果你根本没读，只是把机器写的交上去，被伤到的是你自己——你失去了练一次的机会。第二步，再问真假：署名是你，内容却不是你写的，这就让老师以为你读过了，属于让别人以为一件不真实的事。第三步，问本分：查一查作者是谁、这本书讲什么，让机器帮忙找，没问题；整篇笔记让机器替你写，就过了线。第四步，得出结论：让机器当助手，不让它当代笔。而且用完之后，最好跟老师说清楚你用了什么帮助。",
    "conceptest-1": "接下来用三个容易弄混的说法考考你。请仔细读每一个选项，选完再看解释。",
    "synthesis": "最后一件事交给你，也是这节课最重要的产出。下面有六条候选条款，请每条先表个态：赞成、反对，还是赞成但要加一条限制。六条都表完态之后，点一下生成我们的约定，看看这六条能拼成一份什么样的班级约定。",
    "posttest": "最后一轮，换几个新的情境来考考你。这次会出现一个替同学写作文的机器、一条只有你自己看得见的小圈子，还有一段看起来很真的换脸视频。看看你能不能把三把尺子用上去。",
    "summary": "这节课我们记住三句话。第一句，技术能做和人应该做，是两个问题；机器不会替你想第二个。第二句，判断拿不准的事，用三把尺子：问伤不伤人，问骗没骗人，问该不该我来做。第三句，只推你爱看的内容，一开始很舒服，但你的世界会越来越小——记得主动去看看别的。回到开头那三个画面：机器一直在正常干活，做判断的一直是用它的那个人。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：把三把尺子写下来，并用它们各判断一件你身边的小事。第二层能力应用，动手做：回想一次你差点用机器替自己完成任务的经历，写出当时三把尺子各量出了什么。第三层迁移挑战，选做：和小组同学一起，把我们课上生成的那份班级约定做成一张海报，贴在教室里，并写清楚每一条为什么要这么定。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是学它之前要先会的，右边是学会之后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续学的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 能做不等于应该做", "lab-1": "动手一 情境、做法与后果", "module-2": "概念二 判断的三把尺子",
    "lab-2": "动手二 只推你爱看的", "worked-example": "例题讲解 机器帮忙算不算作弊", "conceptest-1": "概念测试",
    "synthesis": "综合任务 班级机器使用约定", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# 动手一：三个情境（选项见 CUSTOM_JS 的 SCENES，本处仅作文案参考）
# 综合任务：六条候选条款（kind 仅用于生成约定时的分类）
CLAUSES = [
    ("c1", "不拿同学的照片做换脸或者有损形象的图，要用先问本人同不同意", 'yes',
     "同意还要说清楚：用在哪、给谁看。发出去之前再问一次。"),
    ("c2", "交上去的作业，如果是机器帮忙写的，就在末尾写清楚用了什么帮助", 'yes',
     "老师可以事先说清楚：哪一类作业允许用，哪一类必须自己写。"),
    ("c3", "看到明显是编出来的消息，不转发", 'yes',
     "拿不准的时候怎么办？再加上一句：先在小组里问一问，不自己在群里下结论。"),
    ("c4", "发现自己在某一类内容里出不来的时候，主动去看看别的", 'yes',
     "给自己定一个时间边界：连着看多久，就去做一件别的事。"),
    ("c5", "用机器帮忙之前，先自己想一遍", 'yes',
     "先自己写出三句话，再去问；问完之后，把答案用自己的话重新写一遍。"),
    ("c6", "如果自己成了被换脸、被取笑的那个人，可以直接说出来", 'yes',
     "说出来之后谁来回？班级里约定一个负责的人，或者约定一句可以说的话。"),
]

# 动手二：内容池（6 类 × 2 条）
FEED = [
    ("足球", "足球比赛的精彩进球"), ("足球", "班级足球赛的排兵布阵"),
    ("画画", "水彩画的调色小技巧"), ("画画", "同学的手绘作品分享"),
    ("恐龙", "恐龙是怎么被发现的"), ("恐龙", "最大的恐龙有多大"),
    ("天文", "今晚可以看到哪些星座"), ("天文", "望远镜怎么挑"),
    ("古诗", "一首送别诗里的画面"), ("古诗", "古人怎么写春天"),
    ("昆虫", "校园里常见的昆虫"), ("昆虫", "蝴蝶的一生"),
]

CUSTOM_JS = r"""
/* ============================================================
   it-e-ai-ethics 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 动手一：情境 → 选做法 → 看后果（三个情境 × 三种做法）
   3) 动手二：只推你爱看的「信息小屋」
   4) 综合任务：班级机器使用约定（六条 × 三种表态 → 生成约定）
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

  /* ---------- 2. 动手一：情境 → 选做法 → 看后果 ---------- */
  var scPanel = document.getElementById('scene-panel');
  if (scPanel) {
    var SCENES = [
      {
        t: '同学让你把一张合影里另一位同学的脸，换成搞笑的表情，发到班级群里',
        opts: [
          { k: '照做，反正好玩，大家都在笑',
            chain: ['视频做好了，群里一下子热闹起来。', '第二天，被换脸的同学在隔壁班也被人认出来取笑。', '他找你说自己很难受，你才发觉：你觉得是玩笑，他觉得是被取笑。'],
            lens: '伤到人了吗？伤了。这一把尺子没过，后面就不用再问了。',
            bad: true },
          { k: '先问问被换脸的那个同学同不同意',
            chain: ['你问了他，他想了想说：不想被换。', '你们换了个不涉及别人脸的好玩做法。', '群里一样热闹，谁也没有难受。'],
            lens: '问过本人再动手，是最省事的办法。这也是三把尺子里最要紧的一把。',
            bad: false },
          { k: '换个办法，把大家都熟悉的卡通表情贴上去，不用真人脸',
            chain: ['用卡通表情做出来的图一样好笑。', '没有一个人的脸被别人拿去用。', '大家笑完，谁也不用担心自己的照片被传出去。'],
            lens: '同样能玩得开心，又没有人被冒犯。很多时候，第三个办法比前两个都好。',
            bad: false }
        ]
      },
      {
        t: '周末的作文还没写完，你想到可以让机器帮你写一篇，再改几个词交上去',
        opts: [
          { k: '让机器写一篇，改几个词就交上去',
            chain: ['作业交上去了，这次没有被发现。', '老师在课上读了几篇范文，没有你的，因为读出来不像你平时写的。', '再遇到要当场写的场合，你发现自己还是不会写——这一次练习的机会，你弄丢了。'],
            lens: '署名是你，内容却不是你写的，这让老师以为你练过了。第二把和第三把尺子都没过。',
            bad: true },
          { k: '让机器帮忙列一个提纲，正文自己写',
            chain: ['你先想清楚这篇作文分几段。', '每一句话还是你自己想出来的。', '交上去的是你自己的话，老师说这次结构比上次清楚。'],
            lens: '机器当助手，不当代笔。第二把尺子过了——交上去的东西是你自己的。',
            bad: false },
          { k: '跟老师说清楚：这次卡住了，我用了机器帮忙列提纲',
            chain: ['老师知道了你卡在哪一步。', '他教了你一个更省事的写法。', '下一次同类作文，你自己就能起头了。'],
            lens: '把用了什么帮助说出来，别人就不会误会。这是让第二把尺子一直过关的办法。',
            bad: false }
        ]
      },
      {
        t: '你发现自己刷到的内容全是同一类，别的东西好像都看不见了',
        opts: [
          { k: '继续刷，反正推过来的都很喜欢',
            chain: ['刷得越久，推的东西越像你昨天看过的。', '你的喜欢被反复放大，慢慢地，你只对那一类有感觉了。', '一个月后同学在聊别的事，你完全接不上话。'],
            lens: '舒服是舒服，可你的世界变窄了。这件事没有人受伤，但你被悄悄关进了一间小屋。',
            bad: true },
          { k: '主动去搜一搜不一样的内容',
            chain: ['你搜了几次别的话题。', '推荐里重新出现了一些新东西。', '能看到的内容变多了，你也多了几件想聊的事。'],
            lens: '主动去搜，就是自己把小屋的门推开。推一次，屋子就大一点。',
            bad: false },
          { k: '把这个现象告诉同学，一起想想为什么',
            chain: ['同学们一说才发现，原来大家看到的都不一样。', '你们明白了一件事：自己看到的，不等于全部。', '以后看内容的时候，都会多留一个心眼。'],
            lens: '看清这件事本身，就是一种能力。看清楚了，就不容易被它牵着走。',
            bad: false }
        ]
      }
    ];
    var cur = 0, picked = null, out = document.getElementById('scene-verdict');
    var headEl = document.getElementById('scene-text');
    var optBox = document.getElementById('scene-opts');
    var chainEl = document.getElementById('scene-chain');

    function paint1() {
      var s = SCENES[cur];
      headEl.textContent = '情境 ' + (cur + 1) + '：' + s.t;
      optBox.innerHTML = '';
      s.opts.forEach(function (o, i) {
        var b = document.createElement('button');
        b.className = 'choice';
        b.textContent = o.k;
        if (picked === i) b.classList.add(o.bad ? 'wrong' : 'correct');
        b.addEventListener('click', function () {
          picked = i;
          paint1();
          var ch = s.opts[i].chain;
          chainEl.innerHTML = ch.map(function (x, j) {
            return '<div class="step"><span class="n' + (j === 2 ? ' green' : '') + '">' + (j + 1) + '</span><div>' + x + '</div></div>';
          }).join('');
          out.className = 'result ' + (s.opts[i].bad ? 'error' : '');
          out.innerHTML = '<strong>用三把尺子量一量：</strong>' + s.opts[i].lens;
          document.getElementById('scene-next').disabled = cur >= SCENES.length - 1;
        });
        optBox.appendChild(b);
      });
      document.getElementById('scene-progress').textContent = '第 ' + (cur + 1) + ' / ' + SCENES.length + ' 个情境';
      if (picked === null) {
        chainEl.innerHTML = '';
        out.className = 'result warn';
        out.textContent = '先点一个你会这么做，后果会一步一步展开。';
      }
    }
    document.getElementById('scene-next').addEventListener('click', function () {
      if (cur < SCENES.length - 1) {
        cur++; picked = null; paint1();
        document.getElementById('scene-next').disabled = cur >= SCENES.length - 1;
      }
    });
    document.getElementById('scene-reset').addEventListener('click', function () {
      cur = 0; picked = null; paint1();
      document.getElementById('scene-next').disabled = false;
    });
    paint1();
  }

  /* ---------- 3. 动手二：只推你爱看的 ---------- */
  var feedBox = document.getElementById('feed-box');
  if (feedBox) {
    var FEED = [
      ['足球', '足球比赛的精彩进球'], ['足球', '班级足球赛的排兵布阵'],
      ['画画', '水彩画的调色小技巧'], ['画画', '同学的手绘作品分享'],
      ['恐龙', '恐龙是怎么被发现的'], ['恐龙', '最大的恐龙有多大'],
      ['天文', '今晚可以看到哪些星座'], ['天文', '望远镜怎么挑'],
      ['古诗', '一首送别诗里的画面'], ['古诗', '古人怎么写春天'],
      ['昆虫', '校园里常见的昆虫'], ['昆虫', '蝴蝶的一生']
    ];
    var likes = {}, hidden = {};
    var out2 = document.getElementById('feed-verdict');

    function topicsLeft() {
      var t = {};
      FEED.forEach(function (f, i) { if (!hidden[i]) t[f[0]] = 1; });
      return Object.keys(t);
    }

    function paint2() {
      feedBox.innerHTML = '';
      FEED.forEach(function (f, i) {
        if (hidden[i]) return;
        var d = document.createElement('div');
        d.className = 'inner-card';
        d.style.margin = '0';
        d.innerHTML = '<p style="margin:0"><strong>' + f[0] + '</strong>　' + f[1] + '</p>';
        var b = document.createElement('button');
        b.className = 'sort-item';
        b.style.marginTop = '8px';
        b.textContent = '多看看这类';
        b.addEventListener('click', function () { like(f[0]); });
        d.appendChild(b);
        feedBox.appendChild(d);
      });
      var left = topicsLeft();
      document.getElementById('feed-left').textContent = left.length + ' 类';
      document.getElementById('feed-liked').textContent =
        Object.keys(likes).length ? Object.keys(likes).join('、') : '还没有';
      if (left.length <= 1) {
        out2.className = 'result error';
        out2.innerHTML = '<strong>你的内容池只剩 ' + left.length + ' 类了。</strong>' +
          '不是内容变少了，是别的内容被挡在了外面。你并没有不喜欢它们，你只是<strong>再也没机会看到它们</strong>。' +
          '<br><span style="color:var(--muted)">这就是「只推你爱看的」带来的后果：一开始很舒服，慢慢地，你的世界只剩下你喜欢过的那一点。</span>';
      } else {
        out2.className = 'result warn';
        out2.textContent = '现在还能看到 ' + left.length + ' 类内容。再点几次「多看看这类」，看看会发生什么。';
      }
    }

    function like(topic) {
      likes[topic] = (likes[topic] || 0) + 1;
      var pool = [];
      FEED.forEach(function (f, i) {
        if (!hidden[i] && f[0] !== topic) pool.push(i);
      });
      pool.sort(function (a, b) { return (likes[FEED[a][0]] || 0) - (likes[FEED[b][0]] || 0); });
      pool.slice(0, 2).forEach(function (i) { hidden[i] = 1; });
      paint2();
    }

    document.getElementById('feed-restore').addEventListener('click', function () {
      hidden = {}; likes = {};
      paint2();
      out2.className = 'result';
      out2.innerHTML = '<strong>视野又宽回来了。</strong>' +
        '主动去看别的内容，就是自己在推那扇门。门推开一次，屋子就大一点。' +
        '<br><span style="color:var(--muted)">记住这件事：你看到的不等于全部，推荐只推它以为你喜欢的。</span>';
    });
    paint2();
  }

  /* ---------- 4. 综合任务：班级机器使用约定 ---------- */
  var clPanel = document.getElementById('clause-panel');
  if (clPanel) {
    var CLAUSES = [
      ['c1', '不拿同学的照片做换脸或者有损形象的图，要用先问本人同不同意',
        '「同意」还要说清楚：用在哪、给谁看。发出去之前再问一次。'],
      ['c2', '交上去的作业，如果是机器帮忙写的，就在末尾写清楚用了什么帮助',
        '老师可以事先说清楚：哪一类作业允许用，哪一类必须自己写。'],
      ['c3', '看到明显是编出来的消息，不转发',
        '拿不准的时候怎么办？再加一句：先在小组里问一问，不自己在群里下结论。'],
      ['c4', '发现自己在某一类内容里出不来的时候，主动去看看别的',
        '给自己定一个时间边界：连着看多久，就去做一件别的事。'],
      ['c5', '用机器帮忙之前，先自己想一遍',
        '先自己写出三句话，再去问；问完把答案用自己的话重新写一遍。'],
      ['c6', '如果自己成了被换脸、被取笑的那个人，可以直接说出来',
        '说出来之后谁来回？班级里约定一个负责的人，或者约定一句可以说的话。']
    ];
    var state = {};
    var out4 = document.getElementById('clause-verdict');
    var listBox = document.getElementById('clause-list');
    var summary = document.getElementById('clause-summary');

    CLAUSES.forEach(function (c) {
      var card = document.createElement('div');
      card.className = 'inner-card';
      card.innerHTML = '<p style="margin:0 0 8px"><strong>' + c[1] + '</strong></p>';
      var row = document.createElement('div');
      row.className = 'flex-row';
      row.style.marginTop = '0';
      [['yes', '赞成'], ['no', '反对'], ['limit', '赞成，但要加限制']].forEach(function (opt) {
        var b = document.createElement('button');
        b.className = 'choice';
        b.style.textAlign = 'center';
        b.textContent = opt[1];
        b.addEventListener('click', function () {
          state[c[0]] = opt[0];
          paint4();
        });
        row.appendChild(b);
      });
      card.appendChild(row);
      listBox.appendChild(card);
      c.el = row;
    });

    function paint4() {
      CLAUSES.forEach(function (c) {
        var btn = c.el.querySelectorAll('.choice');
        btn[0].classList.toggle('selected', state[c[0]] === 'yes');
        btn[1].classList.toggle('selected', state[c[0]] === 'no');
        btn[2].classList.toggle('selected', state[c[0]] === 'limit');
      });
      var done = Object.keys(state).length;
      document.getElementById('clause-count').textContent = done + ' / ' + CLAUSES.length + ' 条已表态';
      out4.className = 'result warn';
      out4.innerHTML = done < CLAUSES.length
        ? '还有 ' + (CLAUSES.length - done) + ' 条没有表态。六条都表完，再点「生成我们的约定」。'
        : '六条都表完态了。点一下「生成我们的约定」，看看能拼成一份什么样的班级约定。';
    }

    document.getElementById('clause-make').addEventListener('click', function () {
      if (Object.keys(state).length < CLAUSES.length) {
        out4.className = 'result error';
        out4.textContent = '还有条款没有表态。先把六条都选一遍，生成的约定才是完整的。';
        return;
      }
      var keep = CLAUSES.filter(function (c) { return state[c[0]] === 'yes' || state[c[0]] === 'limit'; });
      var drop = CLAUSES.filter(function (c) { return state[c[0]] === 'no'; });
      var html = '';
      if (keep.length) {
        html += '<div class="grid" style="margin-top:8px">';
        keep.forEach(function (c, i) {
          html += '<div class="summary-item"><span class="num">' + (i + 1) + '</span><div>' + c[1] +
            (state[c[0]] === 'limit'
              ? '<br><span style="color:var(--muted)">需要补上：' + c[2] + '</span>'
              : '') + '</div></div>';
        });
        html += '</div>';
      }
      if (drop.length) {
        html += '<p style="color:var(--muted);margin-top:12px">你没有选进约定的：' +
          drop.map(function (c) { return '「' + c[1] + '」'; }).join('、') + '</p>';
      }
      summary.innerHTML = html;
      out4.className = 'result';
      out4.innerHTML = '<strong>约定生成好了，一共 ' + keep.length + ' 条。</strong>' +
        '把它抄在纸上，贴在教室里。要注意的是：一份约定光有条款不够，' +
        (keep.some(function (c) { return state[c[0]] === 'limit'; })
          ? '你已经给其中几条加了限制——加限制，条款才真的做得到。'
          : '最好给每一条都加一句具体怎么做，条款才真的做得到。') +
        '<br><span style="color:var(--muted)">常见错误：把约定写成口号。「要尊重别人」喊一百遍也拦不住一次换脸；' +
        '写成「要用照片里的同学的照片，先问本人」，才拦得住。</span>';
    });

    document.getElementById('clause-reset').addEventListener('click', function () {
      state = {}; summary.innerHTML = ''; paint4();
    });
    paint4();
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：这三种做法，你会怎么选？", TTS["pretest"], [
        {"q": "同学想拿班里另一位同学的照片做个搞笑表情，发到群里。下面哪种做法最妥当？",
         "options": [("先用卡通形象代替，不用真人照片", True),
                     ("先做出来，被换的人反对了再删", False),
                     ("大家都觉得好玩，直接发出去", False)],
         "explain": "用卡通形象一样能玩得开心，而且没有人的脸被拿去用。乐趣和尊重并不冲突。"
                    "<strong>错因提醒：</strong>最常见的错误是误认为「反正是开玩笑，被换的人不会介意」。"
                    "你觉得是玩笑，对方可能觉得是被取笑——这件事只有他本人说了算。"},
        {"q": "用机器帮忙查资料、改错字，和让机器整篇替你写作文，最大的区别在哪里？",
         "options": [("前者是帮你做得更好，后者是让别人以为这是你自己完成的", True),
                     ("没有区别，都是用了机器", False),
                     ("区别在于用机器的时间长短", False)],
         "explain": "前者你仍然是作者，机器是助手；后者署的是你的名字，内容却不是你的，这会让别人产生误会。"
                    "<strong>错因提醒：</strong>容易把「用了机器」和「交给机器」搞混。"
                    "关键在于最后交出去的东西，到底是谁完成的。"},
        {"q": "你发现自己刷到的内容越来越像，别的内容几乎看不到。这件事的后果是什么？",
         "options": [("你看到的世界会越来越窄，慢慢只剩下你原来喜欢的那一点", True),
                     ("没有任何后果，看自己喜欢的最省时间", False),
                     ("网上的内容会因此变少", False)],
         "explain": "推荐只会推它以为你喜欢的。久了以后，你不是不喜欢别的，而是根本没机会看到。"
                    "<strong>错因提醒：</strong>常见错误是误认为「自己选的，怎么会变窄」。"
                    "你选的是喜欢的，被挡掉的是你还没机会喜欢的。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "机器能做，不等于我们应该做", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们已经会用机器做很多事情了，它也确实做得又快又好（And）；可它从来不会想「这件事该不该做」，你让它做什么它就做什么，闯了祸它也担不了责任（But）；所以做判断这件事，只能由用它的那个人来做（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">先看三个常见情境。它们有一个共同点：<strong>机器都在正常干活，没有出错</strong>。</p>
        <div class="grid grid-3">
          <div class="inner-card"><p><strong>🎭 换脸</strong></p><p style="color:var(--muted)">把一个人的脸换到另一个人身上。技术上做得到，可被换脸的人会怎么样？</p></div>
          <div class="inner-card"><p><strong>📝 机器代笔</strong></p><p style="color:var(--muted)">它确实能写出一篇通顺的文章，可你交上去时，署的是自己的名字。</p></div>
          <div class="inner-card"><p><strong>🫧 只推你爱看的</strong></p><p style="color:var(--muted)">你看着很舒服。可渐渐地，别的声音你就听不到了。</p></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="机器能做不等于应该做示意图：换脸、机器代笔、只推你爱看的三个情境，下面标注判断要由用机器的人来做">
          <figcaption>三件事里，机器都没有出错。要不要做、做到哪一步——做这个判断的，一直是<strong>用它的人</strong></figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">⚖️</span><div><strong>关键的一句：</strong>「能不能做」是一道技术题，「该不该做」是一道人的题。机器只会答第一道。它答不出第二道，也不会替我们承担后果。</div></div>
{insight_box([
    {"lens": "看见它", "text": "回想一次你用机器做事的过程：它有没有在任何一步停下来问你「这样做合适吗」？一般不会。"},
    {"lens": "解释它", "text": "它不问，不是因为冷漠，而是因为它本来就没有「该不该」这个概念。它只有「能不能算出来」。"},
    {"lens": "迁移它", "text": "以后每用一次机器，先自己补上它跳过的那一步：这件事做完之后，谁会受到影响？"}])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：选一个做法，看它的后果", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">读一读上面的情境，先点出你觉得你会怎么做。点完之后，后果会一步一步展开，再用三把尺子量一次。</p>
        <div class="lab-panel" id="scene-panel">
          <div class="inner-card" style="background:var(--card);border:2px solid var(--brand)">
            <p style="margin:0" id="scene-text">情境 1</p>
          </div>
          <div style="font-weight:700;font-size:14px;margin:14px 0 6px">你会怎么做？</div>
          <div class="grid" id="scene-opts"></div>
          <div style="font-weight:700;font-size:14px;margin:14px 0 6px">后果一步一步展开</div>
          <div class="step-grid" id="scene-chain"></div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">进度</span><span class="v" id="scene-progress">第 1 / 3 个情境</span></div>
          </div>
          <div class="flex-row">
            <button class="choice" id="scene-next" style="text-align:center">下一个情境 →</button>
            <button class="choice" id="scene-reset" style="text-align:center">从头再来</button>
          </div>
          <p class="result warn" id="scene-verdict" style="margin-top:12px">先点一个你会这么做，后果会一步一步展开。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>三个情境做完，回头看：</strong>有些做法一开始挺好，走到第三步就出了问题。判断一件事，不能只看第一步。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "拿不准的时候，用三把尺子各量一次", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">遇到拿不准的事，用下面<strong>三把尺子</strong>各量一次，过不去就停下来。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>第一把尺子 · 伤不伤人：</strong>这件事会不会让某个人难受、被取笑、被误会？只要会伤到人，再好玩也要停。</div></div>
          <div class="step"><span class="n">2</span><div><strong>第二把尺子 · 骗没骗人：</strong>这件事会不会让别人以为一件不真实的事？换脸视频、编出来的消息，都在这把尺子下面。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>第三把尺子 · 该不该我来做：</strong>这件事本来该我自己完成，是不是整个交给了机器？查资料、改错字没问题；整篇代写，就过了线。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="判断的三把尺子示意图：伤不伤人、骗没骗人、该不该我来做，三把尺子依次量过才做决定">
          <figcaption>三把尺子：问伤不伤人，问骗没骗人，问该不该我来做——三把都过了，再动手</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有同学会想：「不是我动手做的坏事，就不算我的责任。」可是换脸、代写、只推你爱看的，<strong>机器都只是在执行你的要求</strong>。让它做什么，是你决定的；做完之后影响了谁，也是从你这儿开始的。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">📏</span><div><strong>记一句口诀：</strong>问伤不伤人，问骗没骗人，问该不该我来做。</div></div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：只推你爱看的，会发生什么？", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">下面是你的内容池，一共有六类内容。点某一类的「多看看这类」，看看别的内容会怎么样。</p>
        <div class="lab-panel">
          <div class="grid grid-2" id="feed-box"></div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">还能看到</span><span class="v" id="feed-left">6 类</span></div>
            <div class="readout-cell"><span class="k">你点过「多看看」的</span><span class="v green" id="feed-liked">还没有</span></div>
          </div>
          <div class="flex-row">
            <button class="choice" id="feed-restore" style="text-align:center">我想看看别的</button>
          </div>
          <p class="result warn" id="feed-verdict" style="margin-top:12px">现在还能看到 6 类内容。再点几次「多看看这类」，看看会发生什么。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🫧</span><div><strong>想清楚一件事：</strong>被挡住的内容，并不是你讨厌它们。你只是<strong>再也没机会看到</strong>它们了。让视野宽回来的办法，是自己主动去搜一搜、看一看——那个「我想看看别的」，其实就是你自己。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：机器帮忙写的读书笔记，算不算作弊？", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>老师布置了一次读书笔记。用机器帮忙查作者资料、改错字，可以吗？整篇让机器写，可以吗？请用三把尺子说清楚。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>第一把尺子·伤不伤人：</strong>查资料、改错字，对谁都没有伤害。可如果整篇是机器写的，被伤到的是你自己——你失去了练一次的机会。</div></div>
          <div class="step"><span class="n">2</span><div><strong>第二把尺子·骗没骗人：</strong>署名是你，内容却不是你写的，这让老师以为你读过了这本书。这属于让别人以为一件不真实的事。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>第三把尺子·该不该我来做：</strong>读书笔记本来就是练「你怎么想」。查资料可以让机器帮忙，想法必须是你自己的。</div></div>
          <div class="step"><span class="n">4</span><div><strong>得出结论：</strong>让机器当<strong>助手</strong>，不让它当<strong>代笔</strong>。用完之后，最好主动跟老师说清楚你用了什么帮助——说清楚了，第二把尺子就一直是过的。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有同学会想：「我改了几个词，就算我自己写的了。」可改词<strong>不改变作者是谁</strong>。真正要问的是：这篇东西里的想法，有多少是你自己想出来的？如果一句都没有，那署名就不该是你。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，问题出在哪里", TTS["conceptest-1"], [
        {"q": "有同学说：「机器什么都能做，所以做什么都行。」这句话的问题在哪里？",
         "options": [("机器能做，只说明技术上做得到；该不该做，要由人来判断", True),
                     ("机器其实不能做什么，所以这句话错了", False),
                     ("只要是机器做的，就不需要有人负责", False)],
         "explain": "「能不能做」和「该不该做」是两道完全不同的题。机器只会答第一道，第二道永远由人来做。"
                    "<strong>错因提醒：</strong>最常见的是把「技术可行」直接当成「可以去做」。"
                    "技术可行只是起点，不是理由。"},
        {"q": "用机器把一段视频里的人换成另一个人的脸，最该先想清楚的是：",
         "options": [("被换脸的那个人同意吗，看到的人会不会被误导", True),
                     ("换得够不够像，别人看不看得出来", False),
                     ("这一段视频会不会太占地方", False)],
         "explain": "第一把尺子问伤不伤人，第二把尺子问骗没骗人。这两条都是关于人的，和换得多像没有关系。"
                    "<strong>错因提醒：</strong>容易把注意力全放在「做得像不像」上。"
                    "做得越像，越要先问清楚这两件事。"},
        {"q": "关于「只推你爱看的」这类推荐，下面哪句话更准确？",
         "options": [("它让舒服的东西变多，也让你看到的世界越来越小", True),
                     ("它只会把好的内容推给你", False),
                     ("被挡住的内容是因为质量不好", False)],
         "explain": "推荐只会推它以为你喜欢的。久了以后，你不是不喜欢别的，而是没机会看到。"
                    "<strong>错因提醒：</strong>这里最容易误认为「没推给我，说明那些内容不行」。"
                    "被挡住的原因只有一个：你没点过它。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：一起定一份班级机器使用约定", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">下面有六条候选条款。每条先表个态：赞成、反对，还是赞成但要加一条限制。六条都表完，再生成你们的约定。</p>
        <div class="lab-panel" id="clause-panel">
          <div id="clause-list"></div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">表态进度</span><span class="v" id="clause-count">0 / 6 条已表态</span></div>
          </div>
          <div class="flex-row">
            <button class="choice" id="clause-make" style="text-align:center">生成我们的约定</button>
            <button class="choice" id="clause-reset" style="text-align:center">重新来</button>
          </div>
          <p class="result warn" id="clause-verdict" style="margin-top:12px">先把六条都表一遍态。</p>
        </div>
        <div class="inner-card">
          <p><strong>你们生成的约定：</strong></p>
          <div id="clause-summary"><p style="color:var(--muted);margin:0">还没有生成。先把六条都表完态，再点上面的按钮。</p></div>
        </div>
        <div class="inner-card">
          <p><strong>最后想一想，说给同桌听：</strong></p>
          <p style="color:var(--muted)">如果把「要尊重别人」直接写进约定，它拦得住一次换脸吗？为什么加上「要用别人的照片，先问本人」就管用了？</p>
          <textarea id="syn-answer" rows="3" placeholder="只写号召的问题是……写成具体动作的好处是……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个情境，三把尺子还在不在", TTS["posttest"], [
        {"q": "同学请你用机器帮他把一整篇作文写完，他想直接交上去。你会怎么回应？",
         "options": [("可以帮他一起想思路，但不整篇替他写——那会让他以为是他自己完成的", True),
                     ("帮他写，反正他也不是坏人", False),
                     ("帮他写，但让他自己改几个词", False)],
         "explain": "第三把尺子问的是「该不该我来做」。作业本来该他自己完成，整篇代写就越过了这条线，交上去还会让老师误会。"
                    "<strong>错因提醒：</strong>常见错误是误认为「我只是帮个忙，责任不在我」。"
                    "帮忙的人也是这件事的一部分，交上去之后署的只有他一个名字。"},
        {"q": "你在一个小圈子里看到的全是同一类说法，别人都说你说得对。最该想到的是：",
         "options": [("这在个小圈子可能正好把我爱听的都聚在一起了，我得去看看圈外的说法", True),
                     ("大家都同意，说明我想的一定对", False),
                     ("圈子太小了，应该换个更大的圈子继续看同类内容", False)],
         "explain": "所有人都同意的圈子，可能只是把不同的声音挡在了外面。看到的一样多，不等于真相就是这样。"
                    "<strong>错因提醒：</strong>这里最容易犯的是误认为「多数人同意就是对的」。"
                    "要问的是：那些不同意的人，我有没有机会听到？"},
        {"q": "手机上收到一段看起来很真的视频，里面是一位同学说了很难听的话。在转发之前，你最该做的是：",
         "options": [("先想一想它会不会是假的，会不会伤到那位同学，核实之前不转发", True),
                     ("先转发，如果后来发现是假的再删", False),
                     ("视频看起来很真，直接转发让大家都知道", False)],
         "explain": "第一把尺子问伤不伤人，第二把尺子问骗没骗人。转发出去，两把尺子可能一起被撞倒。"
                    "<strong>错因提醒：</strong>最常见的想法是「我是在提醒大家」。"
                    "可是看到的人可能已经存下来了，删掉也追不回来。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把判断这件事握在自己手里", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>两个问题：</strong>机器能做，和人应该做，是完全不同的两道题。机器只答第一道。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>三把尺子：</strong>问伤不伤人，问骗没骗人，问该不该我来做。过不去就停下来。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>一间小屋：</strong>只推你爱看的，一开始很舒服，久了你的世界会越来越小。记得主动去看看别的。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那三个画面：</strong>换脸的人、让机器代写的人、只刷同一类内容的人，机器都没有替他们做决定。做决定的一直是他们自己——所以这件事，也只能由我们每个人自己来把关。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「问伤人、问骗人、问本分」这三句话，说清楚为什么不该把同学的真人照片拿去做换脸视频。</p>
          <p style="color:var(--muted)">再动一动手：<strong>写下来</strong>——把你们课上生成的那份班级约定抄一遍，给每一条后面补一句「具体怎么做」。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "把三把尺子写下来：问伤不伤人，问骗没骗人，问该不该我来做。",
            "用三把尺子各判断一件你身边的小事，写出你判断的结果。",
        ],
        [
            "回想一次你差点用机器替自己完成任务的经历，写出当时三把尺子各量出了什么。",
            "观察自己一周内刷到的内容，记录其中有几类是重复的，再写出你打算怎么让视野变宽。",
        ],
        [
            "和小组同学一起，把课上生成的班级约定做成一张海报，贴在教室里。",
            "给海报上的每一条补一句「具体怎么做」，并写清楚这一条为什么必须写下来。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-e-ai-ethics",
    "node_id": "it-e-ai-ethics",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 小学",
    "title": "人工智能伦理与责任",
    "name_en": "AI Ethics and Responsibility in Everyday Life",
    "grade": 6,
    "grade_cn": "六年级",
    "domain": "internet-ai",
    "domain_cn": "互联网与人工智能",
    "lesson_type": "value-judgement",
    "version": "1.0.0",
    "description": "面向小学六年级：用换脸、机器代写作业、只推你爱看的三个生活情境做价值判断，理解技术能做什么与人应该做什么是两回事，学会用伤不伤人、骗没骗人、该不该我来做三把尺子判断具体情境，并共同产出一份能够照着做的班级机器使用约定。",
    "tags": ["人工智能伦理", "信息社会责任", "换脸", "学术诚信", "推荐算法"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》小学「互联网与人工智能」——讨论人工智能应用中的伦理问题，增强信息社会责任。",
    "hero_question": "这三件事里机器都没有出错，可为什么每一件都需要我们停下来想一想？",
    "hero_alt": "人工智能伦理与责任知识结构图：换脸、机器代笔、只推你爱看的三个情境，以及判断的三把尺子",
    "hero_caption": "三个情境：换脸 · 机器代笔 · 只推你爱看的　|　三把尺子：伤不伤人 · 骗没骗人 · 该不该我来做",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的情境讨论都会围着它转。",
    "anchor_choices": [
        {"t": "用别人的照片做视频，到底行不行？", "d": "想知道这条线画在哪里", "v": "用别人的照片做视频到底行不行"},
        {"t": "让机器帮着写作业，算不算作弊？", "d": "想弄清楚帮忙和代做的区别", "v": "让机器帮着写作业算不算作弊"},
        {"t": "我为什么总刷到同一类内容？", "d": "想知道自己的视野是怎么变窄的", "v": "我为什么总刷到同一类内容"},
        {"t": "判断这些事情，该看哪几条标准？", "d": "想要一把遇到新情况也能用的尺子", "v": "判断这些事情该看哪几条标准"},
    ],
    "objectives": [
        "能用自己的话说出，技术能做一件事和人应该做一件事是两个不同的问题",
        "面对具体情境时，能用伤不伤人、骗没骗人、该不该我来做这三把尺子做出判断",
        "能说清楚只推你爱看的内容会带来什么后果，并说出让视野变宽的办法",
        "能和同学一起，为班级写出一份带具体做法、能够照着执行的机器使用约定",
    ],
    "objectives_plain": [
        "能用自己的话说出，技术能做一件事和人应该做一件事是两个不同的问题",
        "面对具体情境时，能用伤不伤人、骗没骗人、该不该我来做这三把尺子做出判断",
        "能说清楚只推你爱看的内容会带来什么后果，并说出让视野变宽的办法",
        "能和同学一起，为班级写出一份带具体做法、能够照着执行的机器使用约定",
    ],
    "standards": [
        {"content": "讨论人工智能应用中的伦理问题，增强信息社会责任",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 互联网与人工智能"},
        {"content": "在换脸、机器代写、个性化推荐等真实情境中做出负责任的价值判断，并形成可执行的行为约定",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 互联网与人工智能 / 信息社会责任"},
    ],
    "prereqs": ["it-e-ai-awareness"],
    "prereqs_name": "人工智能初识",
    "prereqs_meta": "it-e-ai-awareness",
    "leads_to": ["it-m-digital-citizenship"],
    "next_meta": "it-m-digital-citizenship",
    "section_images": ["assets/it-e-ai-ethics-fig1.webp", "assets/it-e-ai-ethics-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "三件事里机器都没出错，那问题出在谁身上？带着这个疑问开始。",
        "problem-anchor": "先定一个小目标：这节课结束时，你手里会多一把判断新情况的尺子。",
        "objectives": "看清四件事：能做和该做的区别、三把尺子、只推你爱看的后果、写一份能照着做的约定。",
        "pretest": "这几道题不一定非黑即白，凭现在的想法选，选完读一读解释。",
        "module-1": "换脸、代写、只推你爱看的：机器都在正常干活，做判断的是用它的人。",
        "lab-1": "先点做法，再看后果一步一步展开。有些做法第一步挺好，第三步就出问题了。",
        "module-2": "三把尺子：问伤不伤人，问骗没骗人，问该不该我来做。过不去就停下来。",
        "lab-2": "多点几次「多看看这类」，你会看到内容池一类一类被挡住。再点「我想看看别的」。",
        "worked-example": "四步走：问伤害、问真假、问本分、然后才下结论。",
        "conceptest-1": "三个说法里都藏着最容易犯的想法，选完把解释读一遍。",
        "synthesis": "光写「要尊重别人」拦不住任何事。给每条约定补一句「具体怎么做」。",
        "posttest": "替同学代写、小圈子里全是同一种声音、一段看不出的假视频——三把尺子还管用吗？",
        "summary": "三句话：两个问题、三把尺子、一间小屋。",
        "homework": "三层小任务，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学信息科技「互联网与人工智能」里价值判断的那一课。六年级学生最容易走两个极端：要么认为「机器什么都能做，所以做什么都行」，要么把伦理课上成一串口号——「要尊重别人」「要有责任心」，喊完就忘。所以全课刻意不写技术原理，也不停在态度表态上，只做一件事：遇到一个具体情境，先说出你会怎么做，再跟着看它的后果。动手一给出三个生活情境（换脸、用机器代写作业、只推你爱看的），每个三种做法，选完立刻展开一条三步的后果链，再用三把尺子量一次——学生自己会看到，有些做法第一步挺好，走到第三步就出了问题。动手二把「只推你爱看的」变成一个可以点的实验：内容池里六类十二条内容，每点一次「多看看这类」，别的内容就被挡掉一些，直到只剩自己那一类，再点「我想看看别的」让视野宽回来——「信息茧房」这个概念因此被看见，而不是被讲解。综合任务让全班给六条候选条款逐条表态（赞成／反对／赞成但要加限制），并生成一份班级机器使用约定；每条条款都配了「具体怎么做」的限制建议，因为只写号召的约定拦不住任何事，写成具体动作的约定才真的做得到。全课不出现任何真实产品或品牌。",
    "plan_table": """| 1 | cover | 人工智能伦理与责任 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：这三种做法，你会怎么选？ | 起·前测（暴露既有判断） |
| 5 | concept | 机器能做，不等于我们应该做 | 承·概念一（三个情境 + 能做与该做之分） |
| 6 | interactive | 动手一：选一个做法，看它的后果 | 承·价值判断模拟（3 情境 × 3 做法 → 三步后果链） |
| 7 | concept | 拿不准的时候，用三把尺子各量一次 | 承·概念二（三把尺子 + 口诀 + 常见错误） |
| 8 | interactive | 动手二：只推你爱看的，会发生什么？ | 承·信息小屋模拟（内容池逐类被挡 / 视野宽回来） |
| 9 | concept | 例题示范：机器帮忙写的读书笔记，算不算作弊？ | 转·重难点突破（三把尺子分步示范 + 纠错） |
| 10 | quiz | 概念测试：三个说法，问题出在哪里 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：一起定一份班级机器使用约定 | 合·迁移应用（6 条逐条表态 → 生成能照着做的约定） |
| 12 | quiz | 后测：换几个情境，三把尺子还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把判断这件事握在自己手里 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：换脸 / 机器代笔 / 只推你爱看的 三栏情境，配「能做不等于应该做」\n- P5 能做不等于应该做示意图（已生成）：三个情境 + 判断由使用者来做\n- P7 三把尺子示意图（已生成）：伤不伤人 → 骗没骗人 → 该不该我来做\n- 三张图均为教学示意图，画面中不出现任何真实产品、平台或品牌\n- 若需补充：班级讨论现场照片（需获得授权后使用）",
}
