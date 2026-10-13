# -*- coding: utf-8 -*-
"""小学信息科技 · 在线体验与信息获取（G1）—— 补齐知识树「在线社会与信息表达」空缺

学科语气：信息科技 = 概念 + 动手并重。本课为小学一年级起始课，
一句话讲一件事，全部落在"先想清楚问什么 → 挑一个合适的办法 → 看看答案是谁说的"这条链上。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-e-online-experience-fig1.webp'
F2 = './assets/it-e-online-experience-fig2.webp'

TTS = {
    "hero": "小朋友，我问你一件事。明天上学要不要带伞呢？你会去问谁？有的小朋友去问大人，有的小朋友翻一翻天气预报，还有的小朋友在平板上一搜就知道了。你看，想知道一件事，办法不止一个。今天这节课，我们就来学着挑一个合适的办法，再学着看一看，找到的答案是谁说的。",
    "problem-anchor": "开始之前，先选一个你最想知道的事。是想弄清什么叫做在线，还是想知道找答案到底有哪几个办法，或者你想学会挑一挑网上找到的答案，再或者你想知道哪些事情不能拿到网上问。选好了，就带着它往下看。",
    "objectives": "这节课有四个小目标。第一，能说出在线就是用网络把身边和远处连起来，能举出两个在线做的事情。第二，遇到一个小问题，能挑出一个合适的找答案办法。第三，在网上找到答案以后，能说出这句话是谁说的，再决定信不信。第四，知道有些事不该拿到网上问，别人的私事不能说出去。",
    "pretest": "先做三道小题，用你现在的想法选就行。选完马上能看到解释，选错了也没关系，正好知道要重点听哪里。",
    "module-1": "先说什么叫做在线。你家里的平板、手机、电脑，通过网络，可以和学校连起来，和图书馆连起来，和很远的气象台也连起来。东西连起来了，你坐在家里就能看到外面的信息，这就叫在线。要记住一件事：在线只是办法中的一个，不是唯一的办法。问一问身边的人，翻一翻书，一样能知道很多事。",
    "lab-1": "现在请你当一次找答案的小帮手。左边有五件事，右边有六个办法。先点一件事，再点一个你觉得合适的办法。挑对了会告诉你为什么，挑得不太合适也会给你一个小提示，你可以再试一次。",
    "module-2": "在网上找答案，一般要走三步。第一步，把你想问的写成一两个词，也就是关键词。第二步，你会看到很多很多条结果。第三步，也是最重要的一步：挑一挑。怎么挑呢？先看这句话是谁说的。动物园写的科普、气象台发布的预报，比一条没有署名的留言可靠得多。",
    "lab-2": "这里有三条关于大熊猫吃什么的结果，它们说的都不一样。请你看一看每一条是谁说的，再判断能不能相信它。每一条都有两个按钮，你自己选一个，选完就有解释。",
    "worked-example": "我们一起来帮小明解决一个问题。小明想知道，明天上学要不要带伞。第一步，他先把问题想清楚，他要问的不是天气好不好，而是明天上午我们这儿下不下雨。第二步，挑一个合适的办法，他去查了天气预报。第三步，他看了看这个答案是谁说的，是气象台发布的，专门做这件事。第四步，他把答案记在便利贴上，第二天带上了伞。",
    "conceptest-1": "接下来用三个说法考考你，每一个说法里都藏着一个小陷阱。请你读一读，选一个你认为对的，再看解释。",
    "synthesis": "最后一件事交给你。找答案有四步，不过我把它们的顺序打乱了。请你按照正确的顺序，一步一步点出来：先做什么，再做什么，最后做什么。四步都排对了，你就会看到一句话总结。",
    "posttest": "最后一轮，换几个新的小情境来考考你。这次会出现陌生消息和别人的照片，看看你能不能把学到的两条规则用上去：挑办法，看是谁说的。",
    "summary": "这节课我们记住了三句话。第一句，在线就是用网络把身边和远处连起来，它只是办法中的一个。第二句，想找答案，先想清楚要问什么，再挑一个合适的办法。第三句，找到答案以后，先看看是谁说的，再决定信不信。最后还有一句要记牢：别人的私事，不要打听，也不要写到网上。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出两个你在家里做过的在线的事情，再各说一个不用在线也能办到的办法。第二层能力应用，动手做：挑一个你真正想知道的小问题，先写出你要问的关键词，再去找答案，把答案和它的来源一起记下来。第三层迁移挑战，选做：和家人一起定一条上网小约定，写清楚哪三件事你得先问过大人。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是学它之前要先会的，右边是学会之后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续学的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 什么叫做在线", "lab-1": "动手一 找答案工具台", "module-2": "概念二 看看是谁说的",
    "lab-2": "动手二 三条结果挑一挑", "worked-example": "例题讲解 小明与雨伞", "conceptest-1": "概念测试",
    "synthesis": "综合任务 四步排一排", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# 实验室一：五件事 × 六个办法
TASKS = {
    "rain": {
        "t": "明天上学要不要带伞？", "best": ["forecast", "ask"],
        "why": "天气预报就是专门回答这件事的，在线查最快；问一问刚看过预报的家人，也说得准。",
        "hint": "想一想，谁最清楚明天的天气？是有专门预报的人，还是随便猜一猜的人？",
    },
    "dino": {
        "t": "恐龙爱吃什么？", "best": ["bookdict", "search"],
        "why": "关于恐龙的知识，书里有，科普网页里也有，这两个办法都能找到答案。",
        "hint": "恐龙的知识藏在书里，也藏在科普网页里。再挑一个办法试试看。",
    },
    "zi": {
        "t": "「藏」这个字怎么写？", "best": ["bookdict", "search"],
        "why": "不认识的字，查字典最稳；在线搜索也能查到，但要看清是哪个字典、哪个网站给的。",
        "hint": "遇到一个不认识的字，最直接的办法就是把它查出来。",
    },
    "road": {
        "t": "外婆家怎么走？", "best": ["map"],
        "why": "地图就是为「怎么走」准备的，在线地图还能看到路上堵不堵。",
        "hint": "走哪条路、坐哪趟车，看一样东西就全清楚了。",
    },
    "privacy": {
        "t": "同桌家的门牌号是多少？", "best": ["none"],
        "why": "这是别人家的私事，不该打听，更不该上网去搜。保护别人的信息，也是在保护自己。",
        "hint": "再想一想：这件事，是不是你本来就不该知道的？",
    },
}

WAYS = [
    ("search", "在线搜索"),
    ("ask", "问身边人"),
    ("bookdict", "查书或查字典"),
    ("map", "看地图"),
    ("forecast", "查天气预报"),
    ("none", "这个不该到处找"),
]

# 实验室二：三条搜索结果
RESULTS = [
    {
        "source": "市动物园的科普网页",
        "text": "大熊猫最爱吃竹子，也吃竹笋和苹果。",
        "verdict": "ok",
        "why": "这是动物园写的科普，专门讲动物知识，说法也和别的地方一致。可以先相信它。",
    },
    {
        "source": "一条没有署名的留言",
        "text": "大熊猫其实最爱吃汉堡，我亲眼见过。",
        "verdict": "no",
        "why": "先看是谁说的——这条没人署名，也找不到别人这样说。这种话先别信，可以再找可靠的地方核对一下。",
    },
    {
        "source": "一家玩具店的广告",
        "text": "快买这只熊猫玩偶，买了你就知道它吃什么啦！",
        "verdict": "no",
        "why": "它是在推销东西，不是在讲知识。看到这样的内容要小心，它真正想的是让你花钱。",
    },
]

# 综合任务：四步排序
STEPS = [
    {"id": "q", "t": "① 先想清楚我要问什么"},
    {"id": "pick", "t": "② 挑一个合适的办法去找"},
    {"id": "check", "t": "③ 看看这个答案是谁说的"},
    {"id": "use", "t": "④ 把答案记下来，用起来"},
]

CUSTOM_JS = r"""
/* ============================================================
   it-e-online-experience 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 找答案工具台：五件事 × 六个办法 → 匹配反馈
   3) 三条结果挑一挑：看来源决定信不信
   4) 四步排一排：找答案的正确顺序
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

  /* ---------- 2. 找答案工具台 ---------- */
  var TASKS = {
    rain:    { t: '明天上学要不要带伞？', best: ['forecast', 'ask'],
               why: '天气预报就是专门回答这件事的，在线查最快；问一问刚看过预报的家人，也说得准。',
               hint: '想一想，谁最清楚明天的天气？是有专门预报的人，还是随便猜一猜的人？' },
    dino:    { t: '恐龙爱吃什么？', best: ['bookdict', 'search'],
               why: '关于恐龙的知识，书里有，科普网页里也有，这两个办法都能找到答案。',
               hint: '恐龙的知识藏在书里，也藏在科普网页里。再挑一个办法试试看。' },
    zi:      { t: '「藏」这个字怎么写？', best: ['bookdict', 'search'],
               why: '不认识的字，查字典最稳；在线搜索也能查到，但要看清是哪个字典、哪个网站给的。',
               hint: '遇到一个不认识的字，最直接的办法就是把它查出来。' },
    road:    { t: '外婆家怎么走？', best: ['map'],
               why: '地图就是为「怎么走」准备的，在线地图还能看到路上堵不堵。',
               hint: '走哪条路、坐哪趟车，看一样东西就全清楚了。' },
    privacy: { t: '同桌家的门牌号是多少？', best: ['none'],
               why: '这是别人家的私事，不该打听，更不该上网去搜。保护别人的信息，也是在保护自己。',
               hint: '再想一想：这件事，是不是你本来就不该知道的？' }
  };
  var WAY_NAME = {
    search: '在线搜索', ask: '问身边人', bookdict: '查书或查字典',
    map: '看地图', forecast: '查天气预报', none: '这个不该到处找'
  };

  var toolStage = document.getElementById('tool-stage');
  if (toolStage) {
    var curTask = null, solved = {}, wrongCount = 0;
    var out1 = document.getElementById('tool-out');
    var score1 = document.getElementById('tool-score');

    function render1() {
      document.querySelectorAll('[data-task]').forEach(function (b) {
        var k = b.dataset.task;
        b.classList.toggle('selected', k === curTask && !solved[k]);
        b.classList.toggle('correct', !!solved[k]);
        b.textContent = TASKS[k].t + (solved[k] ? ' ✓' : '');
      });
      var n = Object.keys(solved).length;
      score1.textContent = '已经解决 ' + n + ' / 5 件事，重试 ' + wrongCount + ' 次';
    }

    document.querySelectorAll('[data-task]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (solved[b.dataset.task]) {
          out1.className = 'result';
          out1.innerHTML = '<strong>这件事已经解决啦。</strong>' + TASKS[b.dataset.task].why;
          return;
        }
        curTask = b.dataset.task;
        render1();
        out1.className = 'result warn';
        out1.innerHTML = '<strong>你选的是：' + TASKS[curTask].t + '</strong><br>现在想一想，右边哪个办法最合适？';
      });
    });

    document.querySelectorAll('[data-way]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!curTask) {
          out1.className = 'result warn';
          out1.textContent = '先点左边的一件事，再挑办法。';
          return;
        }
        var T = TASKS[curTask];
        var w = b.dataset.way;
        if (T.best.indexOf(w) !== -1) {
          solved[curTask] = true;
          out1.className = 'result';
          out1.innerHTML = '<strong>挑对了：' + WAY_NAME[w] + '。</strong>' + T.why;
          curTask = null;
        } else {
          wrongCount++;
          out1.className = 'result error';
          out1.innerHTML = '<strong>' + WAY_NAME[w] + '，这次不太合适。</strong>' + T.hint +
            '<br><span style="color:var(--muted)">常见错误：一遇到问题就只想到上网搜。其实先看这件事适合谁来回答，才是第一步。</span>';
        }
        render1();
      });
    });
    render1();
  }

  /* ---------- 3. 三条结果挑一挑 ---------- */
  document.querySelectorAll('[data-verdict]').forEach(function (card) {
    card.querySelectorAll('[data-vote]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (card.dataset.done === '1') return;
        card.dataset.done = '1';
        var hit = btn.dataset.vote === card.dataset.verdict;
        var out = card.querySelector('[data-vote-out]');
        card.querySelectorAll('[data-vote]').forEach(function (b) {
          b.disabled = true;
          if (b.dataset.vote === card.dataset.verdict) b.classList.add('correct');
        });
        if (!hit) btn.classList.add('wrong');
        out.style.display = 'block';
        out.className = 'result ' + (hit ? '' : 'warn');
        out.innerHTML = '<strong>' + (hit ? '判断对了！' : '再想一想：') + '</strong>' + card.dataset.why;
      });
    });
  });

  /* ---------- 4. 四步排一排 ---------- */
  var orderStage = document.getElementById('order-stage');
  if (orderStage) {
    var RIGHT = ['q', 'pick', 'check', 'use'];
    var placed = [];
    var out4 = document.getElementById('order-out');
    var tip = {
      q: '不管找什么答案，第一步都是先想清楚：我到底想问什么。',
      pick: '想清楚了，再挑一个合适的办法，问人、翻书、上网都可以。',
      check: '找到答案了，先别急着信，看看这句话是谁说的。',
      use: '确认过来源，就把答案记下来用起来——这才算真的找到了。'
    };
    function render4() {
      var bar = document.getElementById('order-done');
      bar.innerHTML = placed.length
        ? placed.map(function (k, i) { return '<span class="tag">第' + (i + 1) + '步 · ' + tip[k].slice(0, 6) + '…</span>'; }).join(' ')
        : '<span style="color:var(--muted)">还没有排出第一步。</span>';
      document.querySelectorAll('[data-step]').forEach(function (b) {
        b.disabled = placed.indexOf(b.dataset.step) !== -1;
        b.classList.toggle('done', placed.indexOf(b.dataset.step) !== -1);
      });
    }
    document.querySelectorAll('[data-step]').forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.dataset.step;
        if (placed.indexOf(k) !== -1) return;
        if (RIGHT[placed.length] === k) {
          placed.push(k);
          out4.className = 'result';
          out4.innerHTML = '<strong>第 ' + placed.length + ' 步排好了。</strong>' + tip[k];
          if (placed.length === 4) {
            out4.className = 'result';
            out4.innerHTML = '<strong>四步全排对了！</strong>找答案的口诀就是：<strong>先想问什么，再挑办法；看到答案，先问是谁说的。</strong>';
          }
        } else {
          out4.className = 'result error';
          out4.innerHTML = '<strong>这一步还早了一点。</strong>先想一想，找答案的第一步应该是什么？<br>' +
            '<span style="color:var(--muted)">常见错误：一上来就急着去搜，结果搜出来的东西自己都用不上。</span>';
        }
        render4();
      });
    });
    render4();
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：想找答案，你会怎么办？", TTS["pretest"], [
        {"q": "想知道明天会不会下雨，下面哪个办法最合适？",
         "options": [("查一查天气预报", True), ("在网上随便搜一句话", False), ("问同学猜一猜", False)],
         "explain": "天气预报是专门回答这件事的，气象台每天发布。"
                    "<strong>错因提醒：</strong>常见错误是把「能上网搜」当成万能办法，其实先想清楚这件事该由谁来回答，才是第一步。"},
        {"q": "网上搜到「鸵鸟会把头埋进沙子」，你接下来应该做什么？",
         "options": [("先看看这句话是谁说的", True), ("马上记到本子上", False), ("马上讲给同学听", False)],
         "explain": "看到答案先看来源。这句话其实是流传很广的错误说法，鸵鸟并不会把头埋进沙子。"
                    "<strong>错因提醒：</strong>很多同学误认为排在搜索结果前面的就一定对，其实顺序不等于可靠。"},
        {"q": "同桌家的门牌号，可以拿到网上去搜吗？",
         "options": [("不可以，那是别人家的私事", True), ("可以，网上的东西都能查", False), ("可以先搜到再告诉别人", False)],
         "explain": "别人家的住址、电话都属于个人信息，不该打听、不该传播。"
                    "<strong>错因提醒：</strong>不要误认为「网上能找到」就等于「可以去找、可以说出去」，这两件事完全不一样。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "在线，就是把身边和远处连起来", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们已经知道，想知道一件事，可以问身边的人，也可以翻书（And）；但有些问题身边没人知道，书上也一时找不到（But）；所以我们要学会在线去获取信息，还要学会挑一挑再相信（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">一句话：<strong>在线</strong>，就是用网络，把你在的地方和远处连起来，让你不出门也能看到外面的信息。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>在线能做的事</strong></p>
            <p style="color:var(--muted)">查天气、看地图、和外婆视频、在图书馆网站上找书。</p>
          </div>
          <div class="inner-card">
            <p><strong>不在线也能做的事</strong></p>
            <p style="color:var(--muted)">问身边的人、翻一翻书、动笔写下来、面对面说说话。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="在线就是把家、学校、图书馆、气象台用网络连起来的示意图">
          <figcaption>示意图：在线就是用网络把家、学校、图书馆、气象台连在一起，信息可以在它们之间跑</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🌐</span><div><strong>要记住：</strong>在线只是办法里的一个，不是唯一的一个。有些事问一问身边的人，比上网找还快。</div></div>
{insight_box([
    {"lens": "看见它", "text": "家里、学校、图书馆、气象台，本来是分得远远的，接上网络以后，它们就像被一根根线牵在了一起。"},
    {"lens": "解释它", "text": "为什么在线能拿到远处的信息？因为信息可以被送出去、又被接回来——你发出一个请求，远处的电脑把答案送回来给你。"},
    {"lens": "迁移它", "text": "同一个问题，往往有好几条路：问人、翻书、上网。会挑路的人，才最省时间。"},
])}
    ''', tag="概念一"))

    task_btns = "\n".join(
        f'            <button class="choice" data-task="{k}" style="text-align:left">{v["t"]}</button>'
        for k, v in TASKS.items()
    )
    way_btns = "\n".join(
        f'            <button class="choice" data-way="{k}" style="text-align:center">{n}</button>'
        for k, n in WAYS
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：五件事，各挑一个合适的办法", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点左边的一件事，再点右边你觉得最合适的办法。挑完立刻能看到理由。</p>
        <div class="lab-panel">
          <div class="grid grid-2">
            <div>
              <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 我想知道的一件事</div>
              <div class="grid" id="tool-stage">
{task_btns}
              </div>
            </div>
            <div>
              <div style="font-weight:700;font-size:14px;margin-bottom:6px">② 我打算用的办法</div>
              <div class="grid">
{way_btns}
              </div>
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">完成情况</span><span class="v" id="tool-score">已经解决 0 / 5 件事，重试 0 次</span></div>
          </div>
          <p class="result warn" id="tool-out" style="margin-top:12px">先点一件事，再挑一个办法。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🛡️</span><div><strong>特别提醒：</strong>有五件事里，有一件是<strong>不该去找答案</strong>的——别人家的私事。你要是挑中了那个按钮，说明你已经懂得保护别人了。</div></div>
    '''))

    result_cards = "\n".join(f'''
          <div class="inner-card" data-verdict="{r["verdict"]}" data-why="{r["why"]}">
            <p><strong>来源：{r["source"]}</strong></p>
            <p style="color:var(--muted)">{r["text"]}</p>
            <div class="flex-row">
              <button class="choice" data-vote="ok" style="text-align:center">可以相信</button>
              <button class="choice" data-vote="no" style="text-align:center">要小心</button>
            </div>
            <p class="result" data-vote-out style="display:none;margin-top:10px"></p>
          </div>''' for r in RESULTS)
    pages.append(p_concept(SPEC, "m2", 6, "module-2", "找到答案，先看是谁说的", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">在网上找答案，其实只有三步。第三步最重要：<strong>挑一挑</strong>。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>写关键词：</strong>把想问的写成一两个词，比如「大熊猫 吃什么」。</div></div>
          <div class="step"><span class="n">2</span><div><strong>看结果：</strong>你会看到很多条，它们说的可能不一样。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>先看是谁说的：</strong>动物园的科普、气象台的预报，比没有署名的留言可靠得多。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="三条搜索结果对照示意图，标注来源不同可靠程度不同">
          <figcaption>示意图：同一个问题会出现很多条结果，先看它来自哪里，再决定信不信（非真实软件截图，与任何软件商标无关）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">很多同学<strong>误认为</strong>搜索结果排在最前面的就是最对的。其实排在哪里，和说得对不对是两件事——先看来源，才不会被带偏。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>先想问什么，再挑办法；看到答案，先问是谁说的。</div></div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：三条结果摆在你面前，你信哪一条？", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">三条结果都在说「大熊猫吃什么」。先读每一条的<strong>来源</strong>，再选一个按钮。</p>
        <div class="lab-panel">
{result_cards}
          <p class="result warn" style="margin-top:12px">三条都判断完以后，你会发现：<strong>决定信不信的，是来源，不是字数，也不是语气有多肯定。</strong></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>再想一想：</strong>如果三条里有一条是气象台发布的？如果有一条是你不认识的人发的？换成别的问题，你也能用同一个办法判断。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小明想知道明天要不要带伞", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>小明明天要去学校，他想知道要不要带伞。请你帮他一步一步想清楚。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先想清楚问什么：</strong>他要问的不是「天气好不好」，而是「明天上午我们这儿下不下雨」。</div></div>
          <div class="step"><span class="n">2</span><div><strong>挑一个办法：</strong>查天气预报。这件事有专门的人在回答，最合适。</div></div>
          <div class="step"><span class="n">3</span><div><strong>看答案是谁说的：</strong>这条预报是气象台发布的，专门做这件事，可以相信。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>记下来用起来：</strong>把答案写在便利贴上，第二天带上伞——这才算真的找到了答案。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学一打开搜索框，随手打两个字，看到第一条就照着做。这条路的错在<strong>跳过了第一步和第三步</strong>：既没想清楚要问什么，也没看答案是谁说的。用八个字记牢：<strong>先想清楚，再看来源</strong>。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "下面哪句话说得对？",
         "options": [("想找答案，办法不止一个，可以先挑一个最合适的", True),
                     ("在线是唯一的办法，什么事都得上网查", False),
                     ("只要上了网，就一定能找到正确答案", False)],
         "explain": "在线只是办法中的一个，问人、翻书也是好办法。"
                    "<strong>错因提醒：</strong>把「能上网」当成「只有上网」，是这一课最常见的错误想法。"},
        {"q": "同一件事，搜出来的两条结果说法不一样，你应该：",
         "options": [("看看它们分别是谁说的，再判断", True),
                     ("选字数多的那一条", False),
                     ("两条各信一半", False)],
         "explain": "判断可靠不可靠，看的是来源，不是长短。"
                    "<strong>错因提醒：</strong>有人误认为写得长、写得热闹就更可信，其实没有署名的长句，反而更要当心。"},
        {"q": "下面哪一件事，不应该拿到网上去问？",
         "options": [("同学家的门牌号和电话", True),
                     ("明天会不会下雨", False),
                     ("大熊猫爱吃什么", False)],
         "explain": "别人家的住址、电话属于个人信息，不该打听、不该传播。"
                    "<strong>错因提醒：</strong>不要把「好奇」和「可以问」搞混——有些不该知道的事，就不去知道。"}
    ], tag="概念测试"))

    step_btns = "\n".join(
        f'            <button class="sort-item" data-step="{s["id"]}">{s["t"]}</button>' for s in STEPS
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：把找答案的四步排一排", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">下面的四步被打乱了。请你按正确的顺序，一步一步点出来——排错了会给你一个提示。</p>
        <div class="lab-panel">
          <div class="sort-bank" id="order-stage">
{step_btns}
          </div>
          <div class="inner-card" style="margin-top:14px">
            <p><strong>我排出来的顺序</strong></p>
            <p id="order-done" style="color:var(--muted)">还没有排出第一步。</p>
          </div>
          <p class="result warn" id="order-out" style="margin-top:12px">请点出你认为的第一步。</p>
        </div>
        <div class="inner-card">
          <p><strong>排完之后，说给同桌听：</strong></p>
          <p style="color:var(--muted)">这四步里，哪一步最容易被跳过？跳过以后会出什么问题？</p>
          <p style="color:var(--muted)">再把它<strong>画出来</strong>：四个方框，用箭头连起来，就是一个流程图。</p>
          <textarea id="syn-answer" rows="3" placeholder="最容易跳过的是第……步，因为……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，规律还在不在", TTS["posttest"], [
        {"q": "你想知道学校图书馆周末开不开门，最合适的两个办法是：",
         "options": [("在学校网站上查，或者打电话问图书馆老师", True),
                     ("在网上随便发一条问大家的帖子", False),
                     ("等周末去了再说", False)],
         "explain": "学校网站和图书馆老师都是直接知道这件事的人。"
                    "<strong>错因提醒：</strong>把问题丢给不认识的人，等回来的往往是猜的答案——常见错误是把「有人回我」当成「答案可信」。"},
        {"q": "平板弹出一条消息：「点这里领游戏皮肤」。你应该：",
         "options": [("不点，先告诉爸爸妈妈", True), ("点进去看看是什么", False), ("转发给同学一起看看", False)],
         "explain": "陌生链接不要点，更不要转发。先告诉大人，是最稳的做法。"
                    "<strong>错因提醒：</strong>很多人误认为「只是点一下看看」没关系，其实点开的动作本身就可能带来麻烦。"},
        {"q": "同学让你把他家的照片发到班级群里，你应该：",
         "options": [("先问过他，他同意了再说", True),
                     ("照片好看就发，不用问", False),
                     ("发到小群里，人少没关系", False)],
         "explain": "别人的照片属于他的个人信息，发不发由他自己决定。"
                    "<strong>错因提醒：</strong>不要把「群里人少」和「没有关系」搞混——只要没经过同意，发出去就是不合适的。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，讲清在线这件事", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>在线是什么：</strong>用网络把身边和远处连起来，让你不出门也能看到外面的信息。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>怎么找答案：</strong>先想清楚要问什么，再挑一个合适的办法——问人、翻书、上网都行。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>找到之后：</strong>先看这句答案是谁说的，再决定信不信。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>还要记牢一件事：</strong>别人家的住址、电话、照片，都是他的个人信息。不打听、不传播，这也是在保护我们自己。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「在线、办法、来源」这三个词，说清楚你上周末是怎么查到一件事的答案的。</p>
          <p style="color:var(--muted)">再动一动手：<strong>画出</strong>一条属于你自己的找答案小路线，四个方框连起来，每个方框里写一步。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "说出两个你在家里做过的在线的事情。",
            "再说出一个不用在线也能办到的办法。",
        ],
        [
            "挑一个你真正想知道的小问题，先写出你要用的关键词，再去找答案。",
            "把答案和它的来源一起记在本子上：这句话是谁说的？",
        ],
        [
            "和家人一起设计一条上网小约定，写清楚哪三件事你得先问过大人。",
            "找一条你在网上看到过的说法，请大人帮你一起看看它的来源可靠不可靠，把结论写下来。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-e-online-experience",
    "node_id": "it-e-online-experience",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 小学",
    "title": "在线体验与信息获取",
    "name_en": "Going Online: Experiencing and Finding Information",
    "grade": 1,
    "grade_cn": "一年级",
    "domain": "online-society",
    "domain_cn": "在线社会与信息表达",
    "lesson_type": "concept-practice",
    "version": "1.0.0",
    "description": "面向小学一年级：用生活中的小问题认识「在线」，学会为不同的问题挑选合适的找答案办法，并在找到答案后先看来源再决定信不信，同时建立「别人的私事不打听、不传播」的信息社会责任意识。",
    "tags": ["在线", "信息获取", "找答案的办法", "信息来源", "个人信息保护"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》小学「在线社会与信息表达」——感知在线社会，体验在线信息获取与表达。",
    "hero_question": "想知道明天要不要带伞，你会去问谁？",
    "hero_alt": "在线体验与信息获取知识结构图：什么叫做在线、怎么挑找答案的办法、看到答案先看是谁说的",
    "hero_caption": "在线：用网络把身边和远处连起来 · 找答案：先想清楚问什么，再挑合适的办法 · 找到后：先看是谁说的",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的动手活动都会围着它转。",
    "anchor_choices": [
        {"t": "「在线」到底是什么意思？", "d": "为什么在家里也能看到外面的事", "v": "在线到底是什么意思"},
        {"t": "找答案有哪几个办法？", "d": "问人、翻书、上网，各在什么时候用", "v": "找答案有哪几个办法"},
        {"t": "网上的答案能直接相信吗？", "d": "怎么挑一挑再决定信不信", "v": "网上的答案能直接相信吗"},
        {"t": "哪些事不该拿到网上问？", "d": "别人的私事为什么不能打听", "v": "哪些事不该拿到网上问"},
    ],
    "objectives": [
        "能说出在线就是用网络把身边和远处连起来，并举出两个在线做的事情",
        "面对一个真实的小问题，能挑出一个合适的找答案办法并说出理由",
        "找到答案后，能说出这句答案是谁说的，再决定信不信",
        "知道别人的私事不该打听、不该传播，愿意先问过大人再行动",
    ],
    "objectives_plain": [
        "能说出在线就是用网络把身边和远处连起来，并举出两个在线做的事情",
        "面对一个真实的小问题，能挑出一个合适的找答案办法并说出理由",
        "找到答案后，能说出这句答案是谁说的，再决定信不信",
        "知道别人的私事不该打听、不该传播，愿意先问过大人再行动",
    ],
    "standards": [
        {"content": "感知在线社会，体验在线信息获取与表达",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 在线社会与信息表达"},
        {"content": "在真实情境中体验信息的获取过程，初步形成安全、负责任地使用信息的意识",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 信息意识与信息社会责任"},
    ],
    "prereqs": [],
    "prereqs_name": "本课是信息科技小学段「在线社会与信息表达」的起始课，不需要先修节点",
    "prereqs_meta": "",
    "leads_to": ["it-e-digital-tools-basic"],
    "next_meta": "it-e-digital-tools-basic",
    "section_images": ["assets/it-e-online-experience-fig1.webp", "assets/it-e-online-experience-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "明天要不要带伞？问人有用，查天气预报也有用——办法不止一个。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能自己挑一个合适的办法找一个答案。",
        "objectives": "看清四件事：在线是什么、怎么挑办法、怎么看来源、哪些事不该问。",
        "pretest": "凭直觉选就好，前测是帮你看清自己现在站在哪里。",
        "module-1": "在线就是用网络把身边和远处连起来；它只是办法里的一个。",
        "lab-1": "先点一件事，再挑办法。有一件事的正确答案是「不该到处找」，看看你能不能发现。",
        "module-2": "写关键词 → 看结果 → 先看是谁说的，这三步一个都不能少。",
        "lab-2": "三条结果站在你面前，先读「来源」那一行，再判断能不能信。",
        "worked-example": "四步走：先想清楚问什么、挑办法、看来源、记下来用起来。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "四步的顺序被打乱了，按正确的先后点出来，排错了会有提示。",
        "posttest": "出现了陌生消息和别人的照片，看看你能不能把两条规则都用上。",
        "summary": "三句话加一件事：在线是什么、怎么找、看来源，还有别人的私事不打听。",
        "homework": "三层小任务，先做前两层，第三层请和家人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学信息科技「在线社会与信息表达」的起始课。一年级学生的难点不在于记概念，而在于把「上网」当成万能办法——所以全课不铺概念，只串一条链：先想清楚问什么 → 挑一个合适的办法 → 看看答案是谁说的 → 记下来用起来。两个动手台子都做成真能操作的模拟：一个把五件真实小事和六个办法做匹配（其中一件事的正确选择是「不该到处找」，用来承载个人信息保护的价值引导），另一个让学生逐条判断三条搜索结果的来源；综合任务把四步顺序打乱，让学生自己排出来。全课只用「在线 / 办法 / 来源」三个词收口。",
    "plan_table": """| 1 | cover | 在线体验与信息获取 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：想找答案，你会怎么办？ | 起·前测（暴露直觉） |
| 5 | concept | 在线，就是把身边和远处连起来 | 承·概念一 |
| 6 | interactive | 动手一：五件事，各挑一个合适的办法 | 承·匹配互动（含「不该到处找」的价值引导） |
| 7 | concept | 找到答案，先看是谁说的 | 承·概念二（三步法与来源判断） |
| 8 | interactive | 三条结果挑一挑 | 承·动手二（来源判断题） |
| 9 | concept | 例题示范：小明想知道明天要不要带伞 | 转·重难点突破（分步示范 + 纠错） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：把找答案的四步排一排 | 合·迁移应用（排序模拟） |
| 12 | quiz | 后测：换几个新情境，规律还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，讲清在线这件事 | 合·小结与复述 |
| 14 | homework | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：在线是什么 / 怎么挑办法 / 看是谁说的 三栏\n- P5 在线连接示意图（已生成）：家、学校、图书馆、气象台用网络连起来\n- P7 搜索结果对照图（已生成）：三条来源不同的结果并排比较\n- 三张图均为教学示意图，不涉及任何真实软件界面、截图或商标\n- 若需补充：学校图书馆网站首页截图（需获得授权后使用）",
}
