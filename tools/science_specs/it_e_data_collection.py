# -*- coding: utf-8 -*-
"""小学信息科技 · 数据收集与记录（G3）—— 补齐知识树「数据与编码」空缺

学科语气：信息科技 = 概念 + 动手并重。
本课只做一个真能上手的模拟：把 12 条调查记录一条一条归进类别筐，
统计表实时长出计数、条形长度和"最多的一项"。
其中埋着一个陷阱记录——"跑步和跳绳都喜欢"，硬塞进哪一类都会让统计失真，
学生必须先发现这个麻烦，才会长出"先放一边、问清楚再归"的办法。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-e-data-collection-fig1.webp'
F2 = './assets/it-e-data-collection-fig2.webp'

TTS = {
    "hero": "同学们，我们来想一件事。要是有人问你：咱们班同学最喜欢哪一项运动？你大概会说，好像喜欢跑步的人挺多。可是「好像」「挺多」到底是多少人呢？换一个同学来回答，说的可能跟你不一样。光凭感觉说不准，也说不清。那怎么办？我们可以去问一问，再把每个人的答案一条一条记下来，然后数一数。今天这节课，我们就要学会问得清楚、记得明白，还要从这一堆记录里，读出一句真正靠得住的话。",
    "problem-anchor": "开始之前，先选一个你最想弄明白的问题。是想知道问问题的时候该注意什么，还是想知道一大堆答案怎么才数得清，又或者你遇到过有人说「都喜欢」，根本不知道该算哪一边，再或者你想知道这一堆记录到底能告诉我们什么。选好了，就带着它往下看。",
    "objectives": "这节课有四个小目标。第一，能说出数据就是一条一条记录下来的答案，会按一个统一的问法去收集。第二，记录的时候能做到分类标准唯一：同一条答案只能进一个类，说法不同但意思一样的要归到同一类。第三，遇到说不清属于哪一类的记录，能先把它放到一边，问清楚了再归进去，不硬塞。第四，能把一堆记录数一数、比一比，读出一句数据真正支持的话，也知道哪些话数据并没有告诉我们。",
    "pretest": "先做三道小题，用你现在的想法选就行。选完马上能看到解释，选错了也没关系，正好知道该重点听哪里。",
    "module-1": "先说什么叫数据。你拿一张纸，问班里的同学最喜欢哪一项运动，每问到一个就写一条：跑步、跳绳、羽毛球。这些一条一条记下来的答案，就是数据。要收得清楚，得先做好三件事。第一，想清楚要问什么，问题要具体，说好每人只答一个。第二，定好记录的办法，选项要说得统一，也要尽量把可能的情况都想到。第三，一条一条如实记下来，听到什么就记什么，不能按自己心里想的去挑。还要记住一件事：只收集和这个问题有关的信息，同学的姓名、住址这些跟问题无关的私人信息，不要记。",
    "lab-1": "现在我们真的来统计一次。调查的问题是「你最喜欢哪一项运动，每人只说一个」，下面有十二张记录卡片和几个类别筐，请你一条一条把它们归类。每归一条，右边的统计表就会自己更新，你随时能看到每一类有几个人、哪一类最多。注意，里面有一条记录会给你出个难题，看看你能不能自己发现它。",
    "module-2": "记录的时候还有一条规矩最要紧：分类标准要唯一。同一条答案，只能落进一个类别，不能两边都算；说法不一样但说的是同一件事的，要归到同一类，比如「羽毛球」和「打羽毛球」是一回事；实在说不清属于哪一类的，先把它单独放在一边，回去问清楚再归，千万不要硬塞进去。为什么要这么严格？因为只要有一条被算了两次，或者有一些被漏掉了，数出来的总人数就对不上，后面的结论也就靠不住了。",
    "lab-2": "现在请你当一次记录表体检员。下面有三张调查记录表，都是同学自己设计的。请你看一看每一张，判断它是可以直接用，还是必须改一改。判断完会告诉你哪里有问题。",
    "worked-example": "我们一起分析一道题。小组想调查「全班同学每天读多长时间课外书」，于是设计了一张记录表，选项写的是：不到二十分钟、二十分钟到四十分钟、四十分钟以上、其他。这张表能不能用？第一步，先看问题问得清不清楚：问的是每天读书的时长，说好了每人只答一个，清楚。第二步，看选项会不会重叠：三段时间首尾相接又互不重叠，一个人只会落进一格。第三步，看有没有漏掉的情况：选项里有「其他」，说不准的人也有地方去。第四步，得出结论：这张表可以用。反过来，如果选项写的是「二十分钟以内、二十分钟到四十分钟、半小时以上」，「二十分钟到四十分钟」和「半小时以上」就打架了，同一个人可能落进两格，这种表就必须改。",
    "conceptest-1": "接下来用三个容易弄错的说法考考你。请仔细读每一个选项，选完再看解释。",
    "synthesis": "最后一步，也是最有意思的一步：把数据变成信息。下面是刚才统计出来的结果，一共二十位同学参加了调查。表格里只是一堆数字，可只要把它数一数、比一比，就能读出一句有用的话。请你判断下面四条说法，哪些是这张表真正支持的，哪些是表里根本没有告诉我们的。",
    "posttest": "最后一轮，换几个新的小情境来考考你。这次会出现隐私、编数据和说不清的答案，看看你能不能把学到的规矩用上去。",
    "summary": "这节课我们记住了三句话。第一句，数据就是一条一条记录下来的答案；收集的时候要先想清楚问什么，再如实记下来，只记和问题有关的信息。第二句，分类标准要唯一：一条记录只算一次，说法不同意思一样的归到同一类，说不清的先放一边问清楚。第三句，把记录数一数、比一比，就变成了信息——它能帮我们回答问题，也能告诉我们哪些话其实没有依据。还要记牢一句口诀：先问清楚，再记下来；一条只算一次；数一数，就变信息。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出收集数据的三步，并说出「分类标准要唯一」是什么意思。第二层能力应用，动手做：选一个你真正想知道的小问题，先写出问题和你定好的选项，再去问至少八位同学，把答案一条一条记下来。第三层迁移挑战，选做：把记下来的答案整理成一张统计表，数出每一类各有多少人，写出两条这张表真正支持的结论，再写一条表里没有告诉我们的话，并说明为什么。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是学它之前要先会的，右边是学会之后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续学的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 数据是记下来的答案", "lab-1": "动手一 分类统计台", "module-2": "概念二 分类标准要唯一",
    "lab-2": "动手二 记录表体检", "worked-example": "例题讲解 这张表能用吗", "conceptest-1": "概念测试",
    "synthesis": "综合任务 数据变信息", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# 动手一：12 条调查记录（"跑步和跳绳都喜欢"是埋进去的陷阱项）
RECORDS = [
    ("跑步", "run"),
    ("跳绳", "rope"),
    ("羽毛球", "bad"),
    ("跑步", "run"),
    ("打羽毛球", "bad"),
    ("篮球", "ball"),
    ("跑步", "run"),
    ("跳绳", "rope"),
    ("跑步和跳绳都喜欢", "unsure"),
    ("篮球", "ball"),
    ("跑步", "run"),
    ("羽毛球", "bad"),
]

CATS = [
    ("run", "🏃 跑步"),
    ("rope", "🪢 跳绳"),
    ("bad", "🏸 羽毛球"),
    ("ball", "🏀 篮球"),
]

TOTAL_RECORDS = len(RECORDS)

# 动手二：三张记录表样本
SHEETS = [
    {
        "title": "记录表 A",
        "q": "你最喜欢什么水果？",
        "opts": "苹果 ｜ 香蕉 ｜ 苹果和香蕉 ｜ 西瓜 ｜ 其他",
        "verdict": "no",
        "why": "问题本身很好，可选项里有「苹果和香蕉」这么一项。它和「苹果」「香蕉」重复了，同一位同学的答案可能被数两次，同一条记录落进了两个类。"
               "分类标准要唯一，必须把这一项去掉，或者把它换成一个不重叠的新类，比如「都喜欢」。",
    },
    {
        "title": "记录表 B",
        "q": "你每天大约睡几个小时？",
        "opts": "不到 9 小时 ｜ 9 到 10 小时 ｜ 超过 10 小时",
        "verdict": "ok",
        "why": "三档首尾相接、互不重叠，一个人只会落进一格；三档合起来也把各种情况都盖住了。每人只说一个，数得清、不重不漏，这张表可以直接用。",
    },
    {
        "title": "记录表 C",
        "q": "你喜欢哪些运动？",
        "opts": "跑步 ｜ 跳绳 ｜ 篮球",
        "verdict": "no",
        "why": "两个地方要改。第一，问的是「你喜欢哪些运动」，一个人可以答好几个，统计时一个人会被数好几遍；要改成「你最喜欢哪一项运动」，说好每人只答一个。"
               "第二，选项没有把可能的情况都想到，也没有留「其他」，说不准的同学无处可去。",
    },
]

# 综合任务：统计结果与四条结论
STAT_RESULT = [("跑步", 8), ("跳绳", 5), ("羽毛球", 4), ("篮球", 3)]
CONCLUSIONS = [
    {"t": "在我们班这个班里，喜欢跑步的同学最多。", "ok": "yes",
     "why": "这条表里直接写着：跑步 8 人，比其他三项都多。数据支持它。"},
    {"t": "这次一共有 20 位同学回答了调查。", "ok": "yes",
     "why": "把四类人数加起来，8 加 5 加 4 加 3 正好是 20。这是一条从数据里数出来的信息。"},
    {"t": "全校的同学都喜欢跑步。", "ok": "no",
     "why": "这次只调查了我们班，表里没有任何一位别的班同学的回答。数据没有告诉我们全校的情况——把一小群的结论套到一大群身上，是这一类问题里最常见的错误。"},
    {"t": "喜欢跳绳的同学，跑步也一定很厉害。", "ok": "no",
     "why": "记录表里只问了「最喜欢哪一项运动」，没有问谁跑得快不快。这个问题数据根本没有回答，所以这句话只是猜的。"},
]

CUSTOM_JS = r"""
/* ============================================================
   it-e-data-collection 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 动手一：12 条记录 → 类别筐，统计表实时更新（含"分类标准唯一"陷阱）
   3) 动手二：三张记录表体检
   4) 综合任务：数据变信息（四条结论判断）
   ============================================================ */
(function () {
  'use strict';

  /* 统计条形样式（注入，颜色一律走主题变量，不写死） */
  var st = document.createElement('style');
  st.textContent =
    '.stat-row{display:flex;align-items:center;gap:8px;margin:6px 0;font-size:14px;}' +
    '.stat-row .nm{min-width:96px;flex:0 0 auto;}' +
    '.stat-row .bar{height:14px;border-radius:7px;background:var(--brand-2);min-width:2px;' +
    'transition:width .35s ease;flex:0 0 auto;}' +
    '.stat-row .num{font-weight:800;color:var(--link);font-variant-numeric:tabular-nums;}' +
    '.stat-row .scale{flex:1;min-width:20px;height:0;border-top:1px dashed var(--line);}' +
    '.stat-foot{color:var(--muted);font-size:14px;margin:10px 0 0;}';
  document.head.appendChild(st);

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

  /* ---------- 2. 动手一：分类统计台 ---------- */
  var bank = document.getElementById('rec-bank');
  if (bank) {
    var CATS = [
      { k: 'run', n: '跑步' },
      { k: 'rope', n: '跳绳' },
      { k: 'bad', n: '羽毛球' },
      { k: 'ball', n: '篮球' }
    ];
    var counts = { run: 0, rope: 0, bad: 0, ball: 0, unsure: 0 };
    var picked = null, done = 0, unsureFound = false;
    var out = document.getElementById('stat-out');

    function nameOf(k) {
      for (var i = 0; i < CATS.length; i++) { if (CATS[i].k === k) return CATS[i].n; }
      return '一时说不准的';
    }

    function renderStat() {
      var total = 0;
      CATS.forEach(function (c) { total += counts[c.k]; });
      var maxK = null;
      CATS.forEach(function (c) {
        if (counts[c.k] > 0 && (maxK === null || counts[c.k] > counts[maxK])) maxK = c.k;
      });
      var html = CATS.map(function (c) {
        var pct = Math.round(counts[c.k] / 12 * 100);
        return '<div class="stat-row"><span class="nm">' + c.n + '</span>' +
          '<span class="bar" style="width:' + pct + '%"></span>' +
          '<span class="scale"></span>' +
          '<span class="num">' + counts[c.k] + ' 人</span></div>';
      }).join('');
      if (unsureFound) {
        html += '<div class="stat-row"><span class="nm">一时说不准的</span>' +
          '<span class="bar" style="width:' + Math.round(counts.unsure / 12 * 100) + '%;background:var(--warm)"></span>' +
          '<span class="scale"></span>' +
          '<span class="num">' + counts.unsure + ' 人</span></div>';
      }
      html += '<p class="stat-foot">已归类 ' + total + ' / 12 条' +
        (maxK ? '　目前最多的一项：<strong>' + nameOf(maxK) + '</strong>（' + counts[maxK] + ' 人）' : '') +
        '</p>';
      document.getElementById('stat-table').innerHTML = html;
      CATS.forEach(function (c) {
        var el = document.querySelector('[data-count="' + c.k + '"]');
        if (el) el.textContent = counts[c.k];
      });
      var ue = document.querySelector('[data-count="unsure"]');
      if (ue) ue.textContent = counts.unsure;
    }

    bank.querySelectorAll('.sort-item').forEach(function (card) {
      card.addEventListener('click', function () {
        if (card.classList.contains('done')) return;
        bank.querySelectorAll('.sort-item').forEach(function (c) { c.style.outline = 'none'; });
        card.style.outline = '3px solid var(--brand)';
        picked = card;
        out.className = 'result warn';
        out.textContent = '已选中「' + card.textContent.trim() + '」，现在点下面你认为对的那个筐。';
      });
    });

    document.querySelectorAll('[data-rec-bin]').forEach(function (bin) {
      bin.addEventListener('click', function () {
        if (!picked) {
          out.className = 'result warn';
          out.textContent = '先点上面的一条记录，再点筐。';
          return;
        }
        var kind = picked.dataset.kind, got = bin.dataset.recBin;
        picked.style.outline = 'none';

        if (kind === got) {
          var tag = document.createElement('span');
          tag.className = 'tag';
          tag.textContent = picked.textContent.trim() + ' ✓';
          bin.querySelector('.bin-body').appendChild(tag);
          picked.classList.add('done');
          picked.disabled = true;
          counts[kind]++;
          done++;
          out.className = 'result';
          if (kind === 'unsure') {
            out.innerHTML = '<strong>处理得对！</strong>这条记录同时说到两件事，硬放进任何一类都会让统计不准。' +
              '先把它放在「一时说不准的」这一边，回头问清楚：你到底最喜欢哪一项？问清楚了再归进去。';
          } else if (picked.textContent.trim() === '打羽毛球') {
            out.innerHTML = '<strong>归对了。</strong>注意这一条写的是「打羽毛球」，和上面那条「羽毛球」说法不一样，' +
              '可它们说的是同一件事，所以要归到同一个类。分类标准要统一。';
          } else {
            out.innerHTML = '<strong>归对了，「' + picked.textContent.trim() + '」放进「' + nameOf(kind) + '」。</strong>' +
              '同一类每多一条，统计表里的数字就加一。';
          }
          picked = null;
          if (done === 12) {
            out.className = 'result';
            out.innerHTML = '<strong>十二条记录全部归位。</strong>现在数一数：<strong>' + nameOf(maxKeyOf()) +
              '</strong>这一项最多。这一句「最多」，就是你的数据告诉你的信息——它不是你猜的，是你数出来的。';
          }
        } else if (kind === 'unsure') {
          if (!unsureFound) {
            unsureFound = true;
            var extra = document.getElementById('unsure-bin');
            if (extra) extra.style.display = '';
          }
          out.className = 'result error';
          out.innerHTML = '<strong>发现一个难题。</strong>这条记录同时说了两件事：跑步和跳绳。' +
            '把它塞进任何一类，那一类的人数就会多算一次，总数也会超过十二。' +
            '看看下面多出来的那个筐——先把它放到一边，<strong>问清楚了他最喜欢哪一项，再归进去</strong>。' +
            '<br><span style="color:var(--muted)">常见错误：硬塞进一个类，让统计悄悄出错。分类标准要唯一，一条记录只能算一次。</span>';
          picked.style.outline = '3px dashed rgba(239,68,68,.7)';
        } else {
          out.className = 'result error';
          out.innerHTML = '<strong>再想一下。</strong>一条记录同时说了两件事，放进「' + nameOf(got) + '」会怎么样？' +
            '<br><span style="color:var(--muted)">常见错误：看到里面有「跑步」两个字就归到跑步。' +
            '这样一来，同一个人被数了两次，后面的结论也就不准了。</span>';
          picked.style.outline = '3px dashed rgba(239,68,68,.7)';
        }
        renderStat();
      });
    });

    function maxKeyOf() {
      var maxK = CATS[0].k;
      CATS.forEach(function (c) { if (counts[c.k] > counts[maxK]) maxK = c.k; });
      return maxK;
    }

    renderStat();
  }

  /* ---------- 3. 动手二：记录表体检 ---------- */
  document.querySelectorAll('[data-sheet]').forEach(function (card) {
    card.querySelectorAll('[data-verdict]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (card.dataset.done === '1') return;
        card.dataset.done = '1';
        var hit = btn.dataset.verdict === card.dataset.sheet;
        var outEl = card.querySelector('[data-verdict-out]');
        card.querySelectorAll('[data-verdict]').forEach(function (b) {
          b.disabled = true;
          if (b.dataset.verdict === card.dataset.sheet) b.classList.add('correct');
        });
        if (!hit) btn.classList.add('wrong');
        outEl.style.display = 'block';
        outEl.className = 'result ' + (hit ? '' : 'warn');
        outEl.innerHTML = '<strong>' + (hit ? '看准了！' : '再想一想：') + '</strong>' + card.dataset.why;
      });
    });
  });

  /* ---------- 4. 综合任务：数据变信息 ---------- */
  document.querySelectorAll('[data-concl]').forEach(function (card) {
    card.querySelectorAll('[data-cv]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (card.dataset.done === '1') return;
        card.dataset.done = '1';
        var hit = btn.dataset.cv === card.dataset.concl;
        var outEl = card.querySelector('[data-cv-out]');
        card.querySelectorAll('[data-cv]').forEach(function (b) {
          b.disabled = true;
          if (b.dataset.cv === card.dataset.concl) b.classList.add('correct');
        });
        if (!hit) btn.classList.add('wrong');
        outEl.style.display = 'block';
        outEl.className = 'result ' + (hit ? '' : 'warn');
        outEl.innerHTML = '<strong>' + (hit ? '判断对了！' : '再想一想：') + '</strong>' + card.dataset.why;
      });
    });
  });
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：一堆答案，怎么才数得清？", TTS["pretest"], [
        {"q": "想知道咱们班同学最喜欢哪一项运动，下面哪个做法最好？",
         "options": [("定好一个问法，让每人只说一个，一条一条记下来", True),
                     ("问几个平时爱运动的同学，听听他们怎么说", False),
                     ("先想好答案就是跑步，再去问别人对不对", False)],
         "explain": "先定问法、每人只答一个、逐条记录，这样收来的数据才数得清、比得出。"
                    "<strong>错因提醒：</strong>问了几个同学就下结论，或者心里先有了答案再去挑人问，"
                    "收来的不是数据，是偏见——这是收集数据时最常见的错误。"},
        {"q": "记录的时候，一条写的是「打羽毛球」，另一条写的是「羽毛球」，它们应该算：",
         "options": [("同一类，它们是同一件事", True),
                     ("两类，因为字不一样", False),
                     ("随便算哪一类都行", False)],
         "explain": "说法不同，说的还是同一件事，就要归到同一个类，否则统计会漏掉一批人。"
                    "<strong>错因提醒：</strong>不要看到字不一样就当成两类——分类标准要统一。"},
        {"q": "已经记下来的十二条记录，能直接告诉我们什么？",
         "options": [("要数一数、比一比，才能看出哪一项最多", True),
                     ("什么也说明不了，记录没有用", False),
                     ("按第一条记录就能知道答案", False)],
         "explain": "一堆记录还是数据，数一数、比一比，它才变成能回答问题的信息。"
                    "<strong>错因提醒：</strong>很多同学误认为「记完就完事了」，其实统计和比较才是关键的一步。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "数据，就是一条一条记下来的答案", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们平时会说「好多同学喜欢跑步」（And）；可「好多」到底是多少人，两个人说的可能不一样，凭感觉说不清（But）；所以我们先去问、再把答案一条一条如实记下来，这些记录就是数据（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">你问同学最喜欢哪一项运动，每听到一个就写一条：跑步、跳绳、羽毛球……这些<strong>一条一条记录下来的答案</strong>，就是<strong>数据</strong>。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>想清楚问什么</strong>：问题要具体，说好<strong>每人只答一个</strong>。</div></div>
          <div class="step"><span class="n">2</span><div><strong>定好记录的办法</strong>：候选项要说得统一，尽量把可能的情况都想到。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>一条一条如实记</strong>：听到什么就记什么，不能按心里想的去挑。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="数据收集与记录示意图：同学举手回答，把答案一条一条写进记录表">
          <figcaption>示意图：先问清楚，再一条一条记下来——这张写满答案的纸，就是最早的数据</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">特别注意</span>
          <p style="margin:6px 0 0">只收集和这个问题有关的信息就够。同学的姓名、住址、电话号码，跟「喜欢哪项运动」没有关系，<strong>不要记</strong>——少收集一点无关的信息，就是多一分安全。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🔎</span><div><strong>再提醒一句：</strong>记录必须<strong>如实</strong>。听到「跳绳」就写跳绳，不能因为自己希望跑步最多，就把别人的答案改成跑步。</div></div>
{insight_box([
    {"lens": "看见它", "text": "一张写满答案的记录纸，看着乱，其实每一条都是一个同学真实回答过的话。"},
    {"lens": "比较它", "text": "「好像喜欢跑步的人挺多」和「喜欢跑步的有 4 人」——前一句是感觉，后一句才是数据。"},
    {"lens": "迁移它", "text": "要调查的事都能这样办：先定问法，再如实记，最后数一数。运动会报名、班级读书角选书，用的都是同一套办法。"},
])}
    ''', tag="概念一"))

    rec_btns = "\n".join(
        f'            <button class="sort-item" data-kind="{k}">{t}</button>'
        for t, k in RECORDS
    )
    cat_bins = "\n".join(f'''            <div class="sort-bin" data-rec-bin="{k}">
              <h4>{label} <span data-count="{k}">0</span> 人</h4>
              <div class="bin-body"></div>
            </div>''' for k, label in CATS)
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：把十二张记录卡片归进类别，统计表自己会长", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">调查的问题：<strong>你最喜欢哪一项运动？（每人只说一个）</strong>先点一张记录卡片，再点你认为对的筐。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 待归类的记录</div>
          <div class="sort-bank" id="rec-bank">
{rec_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:14px 0 6px">② 类别筐（点它，把选中的记录放进去）</div>
          <div class="sort-bins" style="grid-template-columns:repeat(auto-fit,minmax(140px,1fr))">
{cat_bins}
            <div class="sort-bin" data-rec-bin="unsure" id="unsure-bin" style="display:none">
              <h4>❓ 一时说不准的 <span data-count="unsure">0</span> 人</h4>
              <div class="bin-body"></div>
            </div>
          </div>
          <div style="font-weight:700;font-size:14px;margin:14px 0 6px">③ 自动生成的统计表</div>
          <div class="canvas-wrap" style="padding:14px"><div id="stat-table"></div></div>
          <p class="result warn" id="stat-out" style="margin-top:12px">点一条记录，开始归类。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧩</span><div><strong>遇到麻烦别硬塞：</strong>如果有一条记录怎么说都归不进一个类，那说明它本身就没问清楚。课程的最后，你要学会给这种记录找一个专门的去处。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "分类标准要唯一：一条记录只算一次", TTS["module-2"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么这一条这么要紧？</strong></p>
          <p style="color:var(--muted)">记下来的答案看着乱，但只要分类分得准，数一数就清楚了（And）；可一旦有一条记录同时落进两个类，或者说法不同被拆成两类，数出来的总人数就会对不上（But）；所以分类标准必须唯一、统一，实在说不清的先单独放一边（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">把记录归类的时候，有<strong>三条规矩</strong>，一条都不能少。</p>
        <div class="grid grid-3">
          <div class="inner-card"><p><strong>① 唯一</strong></p><p style="color:var(--muted)">同一条记录只能进一个类，不能两边都算。</p></div>
          <div class="inner-card"><p><strong>② 统一</strong></p><p style="color:var(--muted)">说法不同、意思一样的，归到同一类。</p></div>
          <div class="inner-card"><p><strong>③ 有去处</strong></p><p style="color:var(--muted)">说不清的先放「一时说不准的」，问清楚再归。</p></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">看到「跑步和跳绳都喜欢」里有「跑步」两个字，就把它归到跑步这一类。这样一来，同一个人被数了两次，总数超过了实际人数，后面的结论也就<strong>靠不住</strong>了。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>先问清楚，再记下来；一条只算一次；数一数，就变信息。</div></div>
    ''', tag="概念二"))

    sheet_cards = "\n".join(f'''
          <div class="inner-card" data-sheet="{s["verdict"]}" data-why="{s["why"]}">
            <p><strong>{s["title"]}</strong>　问题：{s["q"]}</p>
            <p style="color:var(--muted)">选项：{s["opts"]}</p>
            <div class="flex-row">
              <button class="choice" data-verdict="ok" style="text-align:center">可以直接用</button>
              <button class="choice" data-verdict="no" style="text-align:center">必须改一改</button>
            </div>
            <p class="result" data-verdict-out style="display:none;margin-top:10px"></p>
          </div>''' for s in SHEETS)
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：三张记录表，哪张能直接用？", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">一张合格的记录表要满足三件事：问得清楚、每人只答一个、选项不重不漏。请逐张体检。</p>
        <div class="lab-panel">
{sheet_cards}
          <p class="result warn" style="margin-top:12px">三张都体检完以后，你会发现：<strong>问题问得好不好，早在收集数据之前就决定了后面能不能数清楚。</strong></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🛠️</span><div><strong>动手改一改：</strong>把记录表 A 和记录表 C 里你觉得有问题的那一项圈出来，在下面写下你的修改办法，再和同桌交换看看。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：这张记录表能用吗？", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>小组要调查「全班同学每天读多长时间课外书」，设计的选项是：不到二十分钟 ｜ 二十分钟到四十分钟 ｜ 四十分钟以上 ｜ 其他。这张记录表能用吗？请说明理由。</p>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="从数据到信息示意图：左边是统计表与条形长度，右边是由此读出的一句结论">
          <figcaption>示意图：把记录数一数、比一比，条形长度就出来了，一句靠得住的话也跟着出来了</figcaption>
        </figure>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先看问得清不清楚：</strong>问的是「每天读多长时间」，说好每人只答一个，清楚。</div></div>
          <div class="step"><span class="n">2</span><div><strong>再看选项会不会重叠：</strong>三段时间首尾相接、互不重叠，一个人只会落进一格。</div></div>
          <div class="step"><span class="n">3</span><div><strong>最后看有没有漏掉的情况：</strong>末尾留了「其他」，说不准的同学也有地方去。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>得出结论：</strong>三关都过，这张表可以直接用。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">把选项改成「二十分钟以内 ｜ 二十分钟到四十分钟 ｜ 半小时以上」。看起来更细了，其实「二十分钟到四十分钟」和「半小时以上」打架——一个人可能同时落进两格。分类标准不唯一，这张表就必须改。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，错在哪里", TTS["conceptest-1"], [
        {"q": "记录里出现了「打羽毛球」和「羽毛球」两种写法，应该怎么处理？",
         "options": [("归到同一类，它们说的是同一件事", True),
                     ("分成两类，字写得不一样", False),
                     ("把「打羽毛球」这一条删掉", False)],
         "explain": "说法不同、意思一样，就要合并成同一类，不然统计会漏掉一批人。"
                    "<strong>错因提醒：</strong>常见错误是看到字不一样就当成两类。分类标准要统一，"
                    "统一的是「意思」，不是「字面」。"},
        {"q": "有一条记录写的是「跑步和跳绳都喜欢」，最好的处理办法是：",
         "options": [("先放到「一时说不准的」那边，问清楚他最喜欢哪一项再归", True),
                     ("随便归到跑步这一类", False),
                     ("两条记录里各算一次", False)],
         "explain": "说不清属于哪一类的，先单独放一边，问清楚再归，这样统计才不会失真。"
                    "<strong>错因提醒：</strong>最容易犯的错就是硬塞——随便归一类、或者两边各算一次，"
                    "都会让人数超过实际人数。"},
        {"q": "记录全部记完以后，接下来最该做的是：",
         "options": [("把记录数一数、比一比，读出结论", True),
                     ("把记录纸收好，这件事就算完成了", False),
                     ("挑几条自己爱看的记录留下来", False)],
         "explain": "数一数、比一比，数据才变成能回答问题的信息。"
                    "<strong>错因提醒：</strong>不要把「收集完」当成「做完了」。挑着看自己爱看的记录，"
                    "那又回到凭感觉说话了。"}
    ], tag="概念测试"))

    stat_rows = "\n".join(
        f'            <div class="stat-row"><span class="nm">{n}</span>'
        f'<span class="bar" style="width:{int(c / 20 * 100)}%"></span><span class="scale"></span>'
        f'<span class="num">{c} 人</span></div>' for n, c in STAT_RESULT
    )
    concl_cards = "\n".join(f'''
          <div class="inner-card" data-concl="{c["ok"]}" data-why="{c["why"]}">
            <p style="margin:0 0 8px">{c["t"]}</p>
            <div class="flex-row" style="margin-top:0">
              <button class="choice" data-cv="yes" style="text-align:center">这张表支持它</button>
              <button class="choice" data-cv="no" style="text-align:center">表里没告诉我们</button>
            </div>
            <p class="result" data-cv-out style="display:none;margin-top:10px"></p>
          </div>''' for c in CONCLUSIONS)
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：把数据变成一句靠得住的话", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">下面是统计好的结果（共 20 位同学回答）。请判断每一条说法，是这张表支持的，还是表里根本没有告诉我们。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 统计结果</div>
          <div class="canvas-wrap" style="padding:14px">
{stat_rows}
            <p class="stat-foot">合计：20 人</p>
          </div>
          <div style="font-weight:700;font-size:14px;margin:14px 0 6px">② 四条说法，逐条判断</div>
{concl_cards}
        </div>
        <div class="inner-card">
          <p><strong>再想一想，写下来：</strong></p>
          <p style="color:var(--muted)">你自己还能从这张表里读出一条什么信息？反过来，如果要办一场班级运动会，这张表能帮你做什么决定？</p>
          <textarea id="syn-answer" rows="3" placeholder="从表里我还看得出来……所以运动会可以……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="evaluate"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个情境，规矩还在不在", TTS["posttest"], [
        {"q": "小组调查「全班同学每天读多长时间课外书」，记录表上还要不要记下每位同学的姓名和家庭住址？",
         "options": [("不用记，只记和问题有关的答案就够了", True),
                     ("要记，记全一点更保险", False),
                     ("姓名要记，住址可以不记", False)],
         "explain": "收集数据只收和问题有关的信息。姓名、住址和「读多久书」没有关系，多收就是用不上的风险。"
                    "<strong>错因提醒：</strong>常见错误是觉得「多记一点总没坏处」——"
                    "和问题无关的个人信息，一条也不该多问。"},
        {"q": "「喜欢跳绳的同学比喜欢跑步的少」，这句话属于：",
         "options": [("信息——它是把数据数一数、比一比之后读出来的", True),
                     ("数据——它就是记录纸上的一个字", False),
                     ("感觉——没有依据的说法", False)],
         "explain": "记录纸上一条一条答案是数据；数过、比过之后读出来的那句话，才是信息。"
                    "<strong>错因提醒：</strong>不要把数据和信息搞混，它们中间隔着「统计」这一步。"},
        {"q": "有位同学的答案你没听清楚，不能确定属于哪一类，最好的做法是：",
         "options": [("先放到「一时说不准的」那边，找机会问清楚再归进去", True),
                     ("按自己觉得最可能的类别归进去", False),
                     ("把他的答案划掉不算", False)],
         "explain": "先放一边、问清楚再归，统计才不会失真，这位同学的答案也不会被丢掉。"
                    "<strong>错因提醒：</strong>「猜一个」和「划掉」都是常见做法，但一个让数据不准，一个让人被漏掉。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，讲清数据这件事", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>数据是什么：</strong>一条一条记录下来的答案。先想清楚问什么，再如实记，只记和问题有关的信息。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>怎么记得准：</strong>分类标准要唯一——一条只算一次，说法不同意思一样的归一类，说不清的先放一边问清楚。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>怎么变成信息：</strong>把记录数一数、比一比，就能读出一句靠得住的话；表里没有的，别当成结论。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那个问题：</strong>「好像喜欢跑步的人挺多」只是感觉；把二十位同学的答案一条条记下来、归好类、数一数，你才敢说：<strong>喜欢跑步的最多，有 4 位同学。这句是数出来的，不是猜的。</strong></p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「数据、分类、信息」这三个词，说清楚你打算怎么调查一件小事。</p>
          <p style="color:var(--muted)">再动一动手：<strong>做一张表</strong>——三行五列，写出你要问的问题、候选的选项，留好「其他」那一栏。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写出收集数据的三步：先做什么、再做什么、最后做什么。",
            "用一句话说说「分类标准要唯一」是什么意思，并举一个例子。",
        ],
        [
            "选一个你真正想知道的小问题，先写出问题和你定好的选项（要留「其他」），再去问至少八位同学，把答案一条一条记下来。",
            "从记下来的记录里找出说法不一样但意思相同的两条，说明它们为什么要归到同一类。",
        ],
        [
            "把记下来的答案整理成一张统计表，数出每一类各有多少人，写出两条这张表真正支持的结论，再写一条表里没有告诉我们的话，并说明为什么。",
            "和同桌互相检查对方设计的记录表：有没有重复的选项？有没有漏掉的情况？有没有多问了和问题无关的私人信息？",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-e-data-collection",
    "node_id": "it-e-data-collection",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 小学",
    "title": "数据收集与记录",
    "name_en": "Collecting and Recording Data",
    "grade": 3,
    "grade_cn": "三年级",
    "domain": "data-encoding",
    "domain_cn": "数据与编码",
    "lesson_type": "concept-practice",
    "version": "1.0.0",
    "description": "面向小学三年级：知道数据是一条一条记录下来的答案，会先定问法再如实记录，只收集与问题有关的信息；能按「唯一、统一、有去处」三条规矩把记录归类，并用统计表把数据数一数、比一比，读出一句数据真正支持的话。",
    "tags": ["数据", "数据收集", "记录", "分类标准", "统计表", "数据与信息"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》小学「数据与编码」——体验数据收集与记录，感知数据与信息的关系。",
    "hero_question": "「好像喜欢跑步的人挺多」——到底是多少人？我们怎么才能问明白、数清楚？",
    "hero_alt": "数据收集与记录知识结构图：怎么收集数据、怎么记录得准、怎么从数据读出信息",
    "hero_caption": "收集：先想清楚问什么，再如实记 · 记录：一条只算一次，说法不同意思一样归一类 · 统计：数一数、比一比，数据就变成了信息",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的动手活动都会围着它转。",
    "anchor_choices": [
        {"t": "想问一件事，问题该怎么问才算清楚？", "d": "为什么问法不对，后面的数据就没用", "v": "想问一件事问题该怎么问才算清楚"},
        {"t": "一大堆答案，怎么才能数得清？", "d": "记录和分类有什么讲究", "v": "一大堆答案怎么才能数得清"},
        {"t": "有人的答案说不清属于哪一类，怎么办？", "d": "硬塞进去真的会出错吗", "v": "有人的答案说不清属于哪一类怎么办"},
        {"t": "这些记录到底能告诉我们什么？", "d": "哪些话是数据说的，哪些是猜的", "v": "这些记录到底能告诉我们什么"},
    ],
    "objectives": [
        "能说出数据就是一条一条记录下来的答案，知道收集前要先定好问法",
        "知道分类标准要唯一：一条记录只算一次，说法不同意思一样的归到同一类",
        "遇到说不清类别的记录，能先单独放一边、问清楚再归，不硬塞也不丢掉",
        "能把记录统计成表格并读出一句数据支持的结论，分清哪些话数据并没有告诉我们",
    ],
    "objectives_plain": [
        "能说出数据就是一条一条记录下来的答案，知道收集前要先定好问法",
        "知道分类标准要唯一：一条记录只算一次，说法不同意思一样的归到同一类",
        "遇到说不清类别的记录，能先单独放一边、问清楚再归，不硬塞也不丢掉",
        "能把记录统计成表格并读出一句数据支持的结论，分清哪些话数据并没有告诉我们",
    ],
    "standards": [
        {"content": "体验数据收集与记录，感知数据与信息的关系",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 数据与编码"},
        {"content": "在真实调查任务中只收集与问题有关的信息，如实记录，初步形成数据安全意识",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 信息社会责任"},
    ],
    "prereqs": [],
    "prereqs_name": "本课是信息科技小学段「数据与编码」的起始课，不需要先修节点",
    "prereqs_meta": "",
    "leads_to": ["it-e-data-visualization"],
    "next_meta": "it-e-data-visualization",
    "section_images": ["assets/it-e-data-collection-fig1.webp", "assets/it-e-data-collection-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "「好像挺多」到底是多少人？凭感觉说不清，得去问、去记、去数。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能自己收集一次数据，并说出它告诉了你什么。",
        "objectives": "看清四件事：数据是什么、怎么记得准、说不清的怎么办、数据怎么变成信息。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "数据就是一条一条记下来的答案；只记和问题有关的信息，如实记，不挑不编。",
        "lab-1": "每归一条，下面的统计表就长一格。有一条记录会难住你，看你能不能发现。",
        "module-2": "三条规矩：唯一、统一、有去处。硬塞会让总数超过实际人数，结论就不可靠了。",
        "lab-2": "体检三张记录表：问得清楚吗？每人只答一个吗？选项有没有重复和遗漏？",
        "worked-example": "四步走：看问得清不清楚、看选项会不会重叠、看有没有漏掉的情况、得出结论。",
        "conceptest-1": "三个说法都是高频错误，选完把解释读一遍。",
        "synthesis": "表里写着的才算支持；表里没问过的，说得再顺也只是猜的。",
        "posttest": "隐私、编数据和说不清的答案，看看你能不能把三条规矩都用上。",
        "summary": "三句话：数据是什么、怎么记得准、怎么变成信息。",
        "homework": "三层小任务，先做前两层，第三层要真的去问一问、数一数。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学信息科技「数据与编码」的起始一课。三年级学生的两个真实难点是：一是把「感觉」当成「数据」，二是遇到说不清类别的记录就硬塞。所以全课只围绕一次真实的班级调查展开，并把动手台子做成真能算的统计表：十二条记录逐条归入类别筐，每归一条，统计表的计数与条形长度就更新一次，最多的一项自动标出。陷阱记录「跑步和跳绳都喜欢」被埋进卡片里——硬塞进任何一类都会让总数超过十二，学生失败一次之后才会长出一个专门的去处「一时说不准的」，从而真正理解「分类标准要唯一」。概念页把规矩收成三条（唯一、统一、有去处）和一句口诀，例题页用「这张记录表能用吗」示范体检四步，综合任务则把统计好的表格摆出来，让学生分辨哪句话是数据支持的、哪句话数据根本没告诉他们——这正是「感知数据与信息的关系」的落点。数据安全与信息社会责任落在两处：只收集与问题有关的信息、如实记录不编造。",
    "plan_table": """| 1 | cover | 数据收集与记录 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：一堆答案，怎么才数得清？ | 起·前测（暴露直觉） |
| 5 | concept | 数据，就是一条一条记下来的答案 | 承·概念一（收集三步 + 只收有关信息） |
| 6 | interactive | 动手一：把十二张记录卡片归进类别，统计表自己会长 | 承·分类统计模拟（实时计数 + 唯一性陷阱） |
| 7 | concept | 分类标准要唯一：一条记录只算一次 | 承·概念二（唯一/统一/有去处 + 口诀） |
| 8 | interactive | 动手二：三张记录表，哪张能直接用？ | 承·记录表体检（判断 + 诊断） |
| 9 | concept | 例题示范：这张记录表能用吗？ | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：三个说法，错在哪里 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：把数据变成一句靠得住的话 | 合·迁移应用（数据与信息之辨） |
| 12 | quiz | 后测：换几个情境，规矩还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，讲清数据这件事 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：怎么收集 / 怎么记录得准 / 怎么变成信息 三栏\n- P5 数据收集与记录示意图（已生成）：举手回答 → 逐条写进记录表\n- P9 从数据到信息示意图（已生成）：统计表与条形长度 → 一句结论\n- 三张图均为教学示意图，不涉及任何真实软件界面、截图或商标\n- 若需补充：学生真实记录纸的实拍照片（需获得授权、并隐去姓名后使用）",
}
