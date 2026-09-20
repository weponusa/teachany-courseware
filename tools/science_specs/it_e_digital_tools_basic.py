# -*- coding: utf-8 -*-
"""小学信息科技 · 常用数字工具与安全使用（G2）—— 补齐知识树「在线社会与信息表达」空缺

学科语气：概念 + 动手并重。本课把"工具"讲成"跟着任务走"，把"安全使用"讲成一张
学生能逐条打勾、每打一次都能得到即时反馈的清单。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-e-digital-tools-basic-fig1.webp'
F2 = './assets/it-e-digital-tools-basic-fig2.webp'

TTS = {
    "hero": "看一看你身边。手机、平板、电脑，还有教室里的投影和电子黑板，它们都是数字工具。有的帮我们查资料，有的帮我们记事情，有的帮我们和远方的人说话。工具很多，可它们并不是随便用的。用哪个、用多久、什么不能点，都有讲究。今天这节课，我们做两件事：学会给事情挑工具，学会安全地用工具。",
    "problem-anchor": "开始之前，先选一个你最想弄清楚的问题。是想知道身边到底有哪些数字工具，还是想知道怎么给一件事挑对的工具，或者你想知道用的时候要守住哪几条安全规则，再或者你想和我一起做一张家里的使用小约定。选好之后，就带着它往下看。",
    "objectives": "这节课有四个目标。第一，能说出至少五种常用数字工具，并说出它们分别帮我们做什么。第二，给你一件小任务，能挑出一个合适的工具，并说清楚为什么挑它。第三，能说出安全使用数字工具的三条规则：时间有度、信息不露、内容先问过大人。第四，遇到陌生链接和陌生消息，能做出不点、不说、告诉大人的选择。",
    "pretest": "先做三道小题，用你现在的想法选就好。选完立刻能看到解释，选错了也没关系，正好知道要重点听哪里。",
    "module-1": "先认识工具。数字工具按它帮我们做的事来分，常见的就这么几类：查，用来找答案，比如搜索；记，用来把事情记下来，比如备忘录；算，用来算数，比如计算器；画，用来画图和做卡；聊，用来和远方的人说话，比如视频通话；拍，用来拍照和录像。要记住一句最要紧的话：不是哪个工具最好，而是哪件事该用哪个工具。",
    "lab-1": "现在请你当一次挑工具的小管家。上面有六件事，下面有七个工具。先点一件事，再点一个你觉得最合适的工具。挑对了会告诉你理由，挑得不太合适也会给你提示。六件事里有一件，正确答案是哪个工具都不用——看看你能不能发现它。",
    "module-2": "工具会帮我们做事，也会带来麻烦，所以要守住三条安全规则。第一条，时间有度：用屏幕要有约定好的时间，中间要休息，眼睛要离远一点。第二条，信息不露：自己的姓名、学校、住址、电话，还有家人的照片，都不随便发到网上。第三条，内容先问：陌生的链接和二维码不点，看到让自己不舒服的内容，马上关掉并告诉大人。",
    "lab-2": "我们把三条规则做成了十个可以打勾的小条目。请你一条一条看，做到的就在后面点一下，没做到就再努力。你每点一条，都会看到这一条为什么重要。十条都看完了，看看你的安全分是多少。",
    "worked-example": "我们一起来分析一件事。小美用平板的时候，跳出一条消息说，点这个链接就能领到免费的皮肤。她该怎么办？第一步，先看清楚这条消息是谁发来的，是熟悉的人，还是完全不认识的人。第二步，想一想它要什么，它要的是她点开那个链接。第三步，想清楚点开会有什么后果，链接背后可能是骗人的网站，也可能是要花钱的东西。第四步，做出决定，不点、不填、马上告诉大人。",
    "conceptest-1": "接下来用三个说法考考你。每一个说法里都有一处不对的地方，请你读一读，选一个你认为对的，再看解释。",
    "synthesis": "最后请你做一张自己家的使用小约定。下面有六条候选，最多最多只能挑三条，挑多了约定就没人记得住了。想一想，哪三条对你家最重要，把它挑出来，下面就会生成你的约定。",
    "posttest": "最后一轮，换几个新的情境来考考你。这次会出现陌生的二维码、太长时间的屏幕和一条要照片的消息，看看你能不能把三条规则都用上去。",
    "summary": "这节课记住两句话。第一句，工具跟着任务走：查、记、算、画、聊、拍，什么事用什么工具。第二句，安全使用守三条：时间有度、信息不露、内容先问。遇到不认识的东西，最稳的做法永远是三步：不点、不说、告诉大人。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出五种数字工具，并各写一句它帮你做的事。第二层能力应用，动手做：和爸爸妈妈一起，把家里最常用的那个工具找出来，说说它该用在什么事上、不该用在什么事上。第三层迁移挑战，选做：和大人一起，为家里做一张使用小约定，贴在你平时用平板的地方，一周以后看看自己做到了几条。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是学它之前要先会的，右边是学会之后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续学的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 工具跟着任务走", "lab-1": "动手一 挑工具小管家", "module-2": "概念二 安全使用三条",
    "lab-2": "动手二 安全自查清单", "worked-example": "例题讲解 陌生链接", "conceptest-1": "概念测试",
    "synthesis": "综合任务 我家的小约定", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# 实验室一：六件事 × 七个工具
TOOL_TASKS = {
    "sum": {
        "t": "算一算 23 加 48 等于多少", "best": ["calc"],
        "why": "算数就是计算器的本职，按一下就能得到答案，不用自己数半天。",
        "hint": "想一想，这件事的关键是算得快、算得准，哪个工具专门干这个？",
    },
    "pack": {
        "t": "记住明天要带的三样东西", "best": ["note"],
        "why": "备忘录就是把要记的事写下来，明天打开一看就不会忘。",
        "hint": "这件事要的是「记下来、别忘了」，哪个工具专门替我们记事？",
    },
    "hall": {
        "t": "找到少年宫在哪、怎么坐车", "best": ["map"],
        "why": "地图就是为「在哪儿、怎么走」准备的，还能看到坐哪趟车。",
        "hint": "要走的路这样的事，看一样东西就全清楚了。",
    },
    "grandma": {
        "t": "和外婆说说话，还想看看她", "best": ["chat"],
        "why": "视频通话能听见声音，还能看见人，在外婆这件事上最合适。",
        "hint": "既要听见、又要看见，哪个工具能做到这两件事？",
    },
    "card": {
        "t": "给同学画一张生日卡", "best": ["draw"],
        "why": "画图工具能画能涂色，做一张卡片正合适——当然，用纸和笔画也可以。",
        "hint": "这件事要的是画出来、涂上颜色。",
    },
    "phone": {
        "t": "把爸爸的手机号码发到班级群里", "best": ["none"],
        "why": "手机号码是家人的个人信息，不该发到群里让所有人看到。这件事哪个工具都不该做。",
        "hint": "再想一想：这件事就算能做到，是不是本来就不该做？",
    },
}

TOOLS = [
    ("calc", "计算器"),
    ("note", "记事本（备忘录）"),
    ("map", "地图"),
    ("chat", "视频通话"),
    ("draw", "画图工具"),
    ("search", "在线搜索"),
    ("none", "这件事不该做"),
]

# 实验室二：安全自查清单
CHECKS = [
    {"id": "c1", "t": "用平板之前先和家人说一声，用完也说一声。",
     "why": "让家人知道你在做什么，遇到麻烦时他们才能帮上你。"},
    {"id": "c2", "t": "每次用屏幕不超过我们约定好的时间。",
     "why": "时间有度，眼睛和身体才不会累，也才有时间做别的事。"},
    {"id": "c3", "t": "眼睛离屏幕一尺远，坐正了再看。",
     "why": "距离太近、躺着看，眼睛最容易累。"},
    {"id": "c4", "t": "陌生的链接、陌生的二维码，我不点。",
     "why": "点开之前你不知道它通向哪里，不点是最稳的一步。"},
    {"id": "c5", "t": "我不把自己的姓名、学校、住址、电话发到网上。",
     "why": "信息不露：这些信息一旦发出去，就收不回来了。"},
    {"id": "c6", "t": "家人的照片、同学的照片，我不随便发出去。",
     "why": "照片是别人的信息，发不发要由他自己决定。"},
    {"id": "c7", "t": "网上有人要我的照片，或者约我见面，我马上告诉大人。",
     "why": "遇到这样的事，不是你的错，一定要说出来让大人帮你。"},
    {"id": "c8", "t": "看到让我不舒服的内容，我马上关掉并告诉大人。",
     "why": "看到不舒服的内容，关掉它、说出来，这件事就结束了。"},
    {"id": "c9", "t": "我不随便下载不认识的软件，也不在软件里花钱。",
     "why": "下载和花钱都要先问过大人，这是家里的约定。"},
    {"id": "c10", "t": "睡觉前把平板放到客厅，不带进被窝。",
     "why": "睡前不玩屏幕，才睡得踏实。"},
]

# 综合任务：家庭使用小约定候选
PACTS = [
    ("p1", "每天用屏幕不超过 20 分钟，中间要休息。"),
    ("p2", "吃饭的时候，手机和平板都放到一边。"),
    ("p3", "睡觉前一小时不用屏幕。"),
    ("p4", "要用的时候先跟家人说一声，用完也说一声。"),
    ("p5", "只有大人陪着才用，自己不乱点。"),
    ("p6", "遇到不认识的内容，先关掉，再告诉大人。"),
]

CUSTOM_JS = r"""
/* ============================================================
   it-e-digital-tools-basic 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 挑工具小管家：六件事 × 七个工具 → 匹配反馈（含「不该做」）
   3) 安全自查清单：十条逐项打勾 + 即时反馈 + 安全分
   4) 我家的小约定：从六条候选里挑三条，生成约定
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

  /* ---------- 2. 挑工具小管家 ---------- */
  var TASKS = {
    sum:     { t: '算一算 23 加 48 等于多少', best: ['calc'],
               why: '算数就是计算器的本职，按一下就能得到答案，不用自己数半天。',
               hint: '想一想，这件事的关键是算得快、算得准，哪个工具专门干这个？' },
    pack:    { t: '记住明天要带的三样东西', best: ['note'],
               why: '备忘录就是把要记的事写下来，明天打开一看就不会忘。',
               hint: '这件事要的是「记下来、别忘了」，哪个工具专门替我们记事？' },
    hall:    { t: '找到少年宫在哪、怎么坐车', best: ['map'],
               why: '地图就是为「在哪儿、怎么走」准备的，还能看到坐哪趟车。',
               hint: '要走的路这样的事，看一样东西就全清楚了。' },
    grandma: { t: '和外婆说说话，还想看看她', best: ['chat'],
               why: '视频通话能听见声音，还能看见人，在外婆这件事上最合适。',
               hint: '既要听见、又要看见，哪个工具能做到这两件事？' },
    card:    { t: '给同学画一张生日卡', best: ['draw'],
               why: '画图工具能画能涂色，做一张卡片正合适——当然，用纸和笔画也可以。',
               hint: '这件事要的是画出来、涂上颜色。' },
    phone:   { t: '把爸爸的手机号码发到班级群里', best: ['none'],
               why: '手机号码是家人的个人信息，不该发到群里让所有人看到。这件事哪个工具都不该做。',
               hint: '再想一想：这件事就算能做到，是不是本来就不该做？' }
  };
  var TOOL_NAME = {
    calc: '计算器', note: '记事本', map: '地图', chat: '视频通话',
    draw: '画图工具', search: '在线搜索', none: '这件事不该做'
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
      score1.textContent = '已经解决 ' + Object.keys(solved).length + ' / 6 件事，重试 ' + wrongCount + ' 次';
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
        out1.innerHTML = '<strong>你选的是：' + TASKS[curTask].t + '</strong><br>现在想一想，下面哪个工具最合适？';
      });
    });

    document.querySelectorAll('[data-tool]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!curTask) {
          out1.className = 'result warn';
          out1.textContent = '先点上面的一件事，再挑工具。';
          return;
        }
        var T = TASKS[curTask], w = b.dataset.tool;
        if (T.best.indexOf(w) !== -1) {
          solved[curTask] = true;
          out1.className = 'result';
          out1.innerHTML = '<strong>挑对了：' + TOOL_NAME[w] + '。</strong>' + T.why;
          curTask = null;
        } else {
          wrongCount++;
          out1.className = 'result error';
          out1.innerHTML = '<strong>' + TOOL_NAME[w] + '，这次不太合适。</strong>' + T.hint +
            '<br><span style="color:var(--muted)">常见错误：手里有什么工具就用什么工具。其实要先看清事情要的是什么——是算、是记、是画，还是找路。</span>';
        }
        render1();
      });
    });
    render1();
  }

  /* ---------- 3. 安全自查清单 ---------- */
  var checkList = document.getElementById('check-list');
  if (checkList) {
    var score3 = document.getElementById('check-score');
    var bar = document.getElementById('check-bar');
    function render3() {
      var on = checkList.querySelectorAll('[data-check].on').length;
      score3.textContent = on + ' / 10';
      bar.style.width = (on * 10) + '%';
      var verdict;
      if (on >= 9) verdict = '安全小卫士！十条里你已经做到 ' + on + ' 条，还可以把没做到的写在小纸条上提醒自己。';
      else if (on >= 6) verdict = '做得不错，已经做到 ' + on + ' 条。挑一条最难的，明天争取多做到一条。';
      else verdict = '还有不少条没做到。别着急，请家人陪你一条一条再过一遍，先做到三条也行。';
      document.getElementById('check-verdict').textContent = verdict;
    }
    document.querySelectorAll('[data-check]').forEach(function (row) {
      var btn = row.querySelector('[data-check-btn]');
      var out = row.querySelector('[data-check-out]');
      btn.addEventListener('click', function () {
        var on = row.classList.toggle('on');
        btn.textContent = on ? '我做到了 ✓' : '还没做到';
        btn.className = 'choice' + (on ? ' correct' : '');
        out.style.display = 'block';
        out.className = 'result ' + (on ? '' : 'warn');
        out.innerHTML = '<strong>' + (on ? '很好的习惯！' : '先别急，这条还可以再努力：') + '</strong>' + row.dataset.why;
        render3();
      });
    });
    render3();
  }

  /* ---------- 4. 我家的小约定 ---------- */
  var pactStage = document.getElementById('pact-stage');
  if (pactStage) {
    var picked = [];
    var out4 = document.getElementById('pact-out');
    var card4 = document.getElementById('pact-card');
    function render4() {
      document.querySelectorAll('[data-pact]').forEach(function (b) {
        var k = b.dataset.pact;
        var i = picked.indexOf(k);
        b.classList.toggle('selected', i !== -1);
        b.textContent = b.dataset.text + (i !== -1 ? '（第 ' + (i + 1) + ' 条）' : '');
      });
      if (picked.length === 0) {
        card4.innerHTML = '<span style="color:var(--muted)">还没有挑，约定还是空的。</span>';
        return;
      }
      card4.innerHTML = '<strong>我们家的数字工具使用约定</strong><br>' +
        picked.map(function (k, i) {
          var b = document.querySelector('[data-pact="' + k + '"]');
          return '第 ' + (i + 1) + ' 条：' + b.dataset.text;
        }).join('<br>') +
        (picked.length === 3 ? '<br><span style="color:var(--muted)">三条正好——挑得再多，就没人记得住了。</span>' : '');
    }
    document.querySelectorAll('[data-pact]').forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.dataset.pact;
        var i = picked.indexOf(k);
        if (i !== -1) {
          picked.splice(i, 1);
          out4.className = 'result warn';
          out4.textContent = '已经去掉一条，现在是 ' + picked.length + ' 条。';
        } else if (picked.length >= 3) {
          out4.className = 'result error';
          out4.innerHTML = '<strong>已经三条啦。</strong>约定太长就记不住了——先去掉一条，再挑这一条。' +
            '<br><span style="color:var(--muted)">常见错误：什么都想写进去，结果一条也做不到。</span>';
        } else {
          picked.push(k);
          out4.className = 'result';
          out4.innerHTML = '<strong>已挑 ' + picked.length + ' 条。</strong>' +
            (picked.length === 3 ? '三条齐了！把它念给家人听，约定就算定下来了。' : '再挑 ' + (3 - picked.length) + ' 条对你家最重要的。');
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

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：这些工具，你用得对吗？", TTS["pretest"], [
        {"q": "想要知道明天的天气，下面哪个工具最合适？",
         "options": [("在线的天气应用或气象网站", True), ("计算器", False), ("画图工具", False)],
         "explain": "天气应用拿到的就是气象台发布的信息，专门回答天气这件事。"
                    "<strong>错因提醒：</strong>常见错误是手里有什么工具就用什么工具，没先看清事情要的是什么。"},
        {"q": "在不认识的网站上，跳出一个框让你填妈妈的手机号，你应该：",
         "options": [("不填，马上告诉妈妈", True), ("填上，反正只是个号码", False), ("先随便填一个假的试试", False)],
         "explain": "家人的手机号属于个人信息，不管对方说什么都不要填。"
                    "<strong>错因提醒：</strong>很多同学误认为「只是填个号码没关系」，其实信息一旦发出去就收不回来了。"},
        {"q": "用平板看动画片，下面哪种做法是安全的？",
         "options": [("看之前和家人约定好时间，到点就停", True), ("一口气看到眼睛酸为止", False), ("躲进被窝里悄悄看", False)],
         "explain": "时间有度是第一条安全规则。约定好时间、到点就停，眼睛和身体才不会被累坏。"
                    "<strong>错因提醒：</strong>不要把「停下来」当成「不好玩了」——会停的人，才能一直玩得开心。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "工具跟着任务走：什么事，用什么工具", TTS["module-1"], f'''
        <p style="font-size:17px;margin:0 0 12px">手机、平板、电脑都是<strong>数字工具</strong>。它们按「帮我们做什么」分成几类：<strong>查、记、算、画、聊、拍</strong>。</p>
        <div class="grid grid-3">
          <div class="inner-card"><p><strong>查</strong></p><p style="color:var(--muted)">在线搜索：找答案。</p></div>
          <div class="inner-card"><p><strong>记</strong></p><p style="color:var(--muted)">备忘录：把事记下来。</p></div>
          <div class="inner-card"><p><strong>算</strong></p><p style="color:var(--muted)">计算器：算数。</p></div>
          <div class="inner-card"><p><strong>画</strong></p><p style="color:var(--muted)">画图工具：画图做卡。</p></div>
          <div class="inner-card"><p><strong>聊</strong></p><p style="color:var(--muted)">视频通话：和远方的人说话。</p></div>
          <div class="inner-card"><p><strong>拍</strong></p><p style="color:var(--muted)">相机：拍照、录像。</p></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="常用数字工具与用途对应关系示意图">
          <figcaption>示意图：把常见数字工具按用途归成六类（示意图，非真实软件界面、截图或商标）</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🧰</span><div><strong>最要紧的一句：</strong>不是哪个工具最好，而是<strong>哪件事该用哪个工具</strong>。同一件事，有时用纸和笔比用平板还快。</div></div>
{insight_box([
    {"lens": "看见它", "text": "身边每一个工具都在替你干一件具体的事：计算器替你算，备忘录替你记，地图替你认路。"},
    {"lens": "比较它", "text": "同一件事常有好几个工具都能做：算 23 加 48，计算器最快，自己列竖式也行——挑的是最合适，不是唯一。"},
    {"lens": "迁移它", "text": "换一件事，工具就换。写作业要的是想清楚，这时候最该用的工具其实是自己的脑子。"},
])}
    ''', tag="概念一"))

    task_btns = "\n".join(
        f'            <button class="choice" data-task="{k}" style="text-align:left">{v["t"]}</button>'
        for k, v in TOOL_TASKS.items()
    )
    tool_btns = "\n".join(
        f'            <button class="choice" data-tool="{k}" style="text-align:center">{n}</button>'
        for k, n in TOOLS
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：挑工具小管家，六件事你说了算", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点上面的一件事，再点下面你觉得最合适的工具。挑完立刻能看到理由。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 我要做的这件事</div>
          <div class="grid" id="tool-stage">
{task_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:14px 0 6px">② 我打算用的工具</div>
          <div class="grid grid-3">
{tool_btns}
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">完成情况</span><span class="v" id="tool-score">已经解决 0 / 6 件事，重试 0 次</span></div>
          </div>
          <p class="result warn" id="tool-out" style="margin-top:12px">先点一件事，再挑一个工具。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🛡️</span><div><strong>特别提醒：</strong>六件事里有一件，什么工具都不该用——因为它本来就不该做。看看你能不能发现它。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "安全使用守三条：时间有度、信息不露、内容先问", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">工具帮我们做事，也会带来麻烦。所以要守住三条规则——记成六个字：<strong>有度、不露、先问</strong>。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>时间有度：</strong>用屏幕有约定好的时间，中间要休息，眼睛离屏幕一尺远，坐正了再看。</div></div>
          <div class="step"><span class="n">2</span><div><strong>信息不露：</strong>姓名、学校、住址、电话，还有家人和同学的照片，都不随便发到网上。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>内容先问：</strong>陌生链接和二维码不点；看到不舒服的内容，关掉并告诉大人；下载和花钱，先问过大人。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="安全使用数字工具的三条规则示意图">
          <figcaption>三条规则：时间有度、信息不露、内容先问（示意图，非真实软件界面、截图或商标）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「只是点开看一眼」「只是发到小群里」没关系。其实点开的那一下可能已经带来了麻烦，发出去的号码也收不回来了。记住六个字：<strong>不点、不说、告诉大人</strong>。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>口诀：</strong>工具用对，时间有度，信息不露，内容先问。</div></div>
    ''', tag="概念二"))

    check_rows = "\n".join(f'''
          <div class="inner-card" data-check="{c["id"]}" data-why="{c["why"]}">
            <div class="flex-row" style="margin-top:0">
              <span style="flex:1;min-width:200px"><strong>{i}. {c["t"]}</strong></span>
              <button class="choice" data-check-btn style="text-align:center;min-width:120px">还没做到</button>
            </div>
            <p class="result" data-check-out style="display:none;margin-top:10px"></p>
          </div>''' for i, c in enumerate(CHECKS, 1))
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：安全自查清单，一条一条点一点", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">十条规则，做到的就点一下按钮。每点一条，都会告诉你这一条为什么重要。</p>
        <div class="lab-panel">
          <div class="lab-readout" style="margin-top:0">
            <div class="readout-cell"><span class="k">我的安全分</span><span class="v green" id="check-score">0 / 10</span></div>
          </div>
          <div style="height:8px;border-radius:4px;background:rgba(0,0,0,.07);overflow:hidden;margin-top:10px">
            <div id="check-bar" style="height:100%;width:0%;background:linear-gradient(90deg,var(--brand),var(--brand-2));transition:width .3s ease"></div>
          </div>
          <div id="check-list" style="margin-top:12px">
{check_rows}
          </div>
          <p class="result" id="check-verdict" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">✅</span><div><strong>怎么用这张清单：</strong>今天先看一遍，把做到的勾上；一周以后再来看一次，看看有没有多勾上几条。<strong>没做到不等于做错</strong>，它只是下一条要努力的地方。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小美收到一条「免费领皮肤」的消息", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>小美用平板时跳出一条消息：「点这个链接，免费领游戏皮肤。」她该怎么办？请一步一步说清楚。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看清来源：</strong>这条消息是谁发来的？是认识的人，还是完全不认识的人。</div></div>
          <div class="step"><span class="n">2</span><div><strong>看它要什么：</strong>它要的不是别的，就是要她<strong>点开那个链接</strong>。</div></div>
          <div class="step"><span class="n">3</span><div><strong>想清后果：</strong>链接背后可能是骗人的网站，也可能要她填信息、花钱买东西。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>做出决定：</strong>不点、不填、不转发，<strong>马上告诉大人</strong>，然后继续做自己原来在做的事。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有同学会说：「我就点开看一眼，不填东西。」这条路错在<strong>把「看一眼」当成「没有关系」</strong>——点开的那一下，麻烦可能已经进来了。把四步收成六个字：<strong>不点、不说、告诉大人</strong>。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：每个说法里都藏着一处不对", TTS["conceptest-1"], [
        {"q": "下面哪句话说得对？",
         "options": [("不是哪个工具最好，而是哪件事该用哪个工具", True),
                     ("越贵的工具，做事情就越快", False),
                     ("有了平板，就不用纸和笔了", False)],
         "explain": "工具是为任务服务的，先看清事情要什么，再挑工具。"
                    "<strong>错因提醒：</strong>把「工具厉害」和「工具合适」搞混，是这一课最常见的错误。"},
        {"q": "下面哪一种做法是安全的？",
         "options": [("陌生二维码不扫，先拿给大人看", True),
                     ("扫一扫看看里面是什么", False),
                     ("先扫了，再决定要不要填信息", False)],
         "explain": "不认识的东西先给大人看，这是最稳的一步。"
                    "<strong>错因提醒：</strong>有人误认为「先扫了再说」没关系，其实扫开之后你再想回头就晚了。"},
        {"q": "网上有人发消息说：「把你家的照片发给我看看。」你应该：",
         "options": [("不发，马上告诉爸爸妈妈", True), ("发一张没关系的", False), ("先问他是谁，再发给他", False)],
         "explain": "不管对方是谁，家里的照片都不该随便发出去。"
                    "<strong>错因提醒：</strong>不要把「他先问我」当成「他就有权知道」——该不该发，由你和家人决定。"}
    ], tag="概念测试"))

    pact_btns = "\n".join(
        f'            <button class="sort-item" data-pact="{k}" data-text="{t}">{t}</button>' for k, t in PACTS
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：给我家做一张使用小约定", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">下面有六条候选，最多只能挑三条。想一想哪三条对你家最重要，点一下就能选上，再点一下可以去掉。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">候选条款（最多选 3 条）</div>
          <div class="sort-bank" id="pact-stage">
{pact_btns}
          </div>
          <div class="inner-card" style="margin-top:14px">
            <p id="pact-card" style="color:var(--muted)">还没有挑，约定还是空的。</p>
          </div>
          <p class="result warn" id="pact-out" style="margin-top:12px">先点一条你认为最重要的。</p>
        </div>
        <div class="inner-card">
          <p><strong>写下来，念给家人听：</strong></p>
          <p style="color:var(--muted)">这三条里面，哪一条你最容易忘？打算怎么提醒自己？</p>
          <textarea id="syn-answer" rows="3" placeholder="最容易忘的是第……条，我打算……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换个新情境，三条规则还在不在", TTS["posttest"], [
        {"q": "放学路上，有人递给你一张卡片，上面印着一个二维码，说扫一下能领礼物。你应该：",
         "options": [("不扫，回家把这件事告诉爸爸妈妈", True), ("扫一下看看是什么礼物", False), ("拿回家扫，反正不在外面扫", False)],
         "explain": "陌生的二维码和陌生的链接一样，都不要扫。告诉大人是最稳的一步。"
                    "<strong>错因提醒：</strong>常见错误是相信「换个地方扫就安全了」——不安全的是那张码，不是扫的地点。"},
        {"q": "你正看得起劲，约定的 20 分钟到了，你应该：",
         "options": [("停下来，休息一下眼睛", True), ("把这一集看完再停", False), ("先调成小声音，接着看", False)],
         "explain": "时间有度，到点就停，这是自己在管自己。"
                    "<strong>错因提醒：</strong>很多同学误认为「看完这一集」不算超时，可一集接着一集，时间就悄悄跑掉了。"},
        {"q": "下面哪一件事，用了数字工具反而是不合适的？",
         "options": [("把爸爸的手机号码发到班级群里", True), ("用备忘录记下明天要带的东西", False), ("用地图找少年宫怎么走", False)],
         "explain": "家人手机号是个人信息，再方便的工具也不该用来做这件事。"
                    "<strong>错因提醒：</strong>不要把「能做」和「该做」搞混——工具能做到，不代表这件事合适做。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：两句话，把工具和安全都记住", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>工具跟着任务走：</strong>查、记、算、画、聊、拍——先看清事情要什么，再挑工具。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>安全使用守三条：</strong>时间有度、信息不露、内容先问。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>遇到不认识的东西：</strong>不点、不说、告诉大人。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>再说一句：</strong>工具的本事，比不上用工具的人会安排。会挑、会停、会问，才是真的会用它。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「工具、任务、三条规则」这三组词，说清楚你今天在自查清单上勾掉了几条、还剩几条。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写出五种常用数字工具，并各写一句它帮你做的事。",
            "把三条安全规则写下来，每条后面各举一个小例子。",
        ],
        [
            "和爸爸妈妈一起，找出家里最常用的那个数字工具，说说它该用在什么事上、不该用在什么事上。",
            "再做一遍安全自查清单，把没做到的那几条抄在小纸条上，贴在平时用平板的地方。",
        ],
        [
            "和家人一起为家里做一张使用小约定，贴在平时用平板的地方，一周以后看看自己做到了几条。",
            "找一条你遇到的、说不清该不该信的网络消息，请大人帮你一起判断，把判断的过程写下来。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-e-digital-tools-basic",
    "node_id": "it-e-digital-tools-basic",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 小学",
    "title": "常用数字工具与安全使用",
    "name_en": "Everyday Digital Tools and Using Them Safely",
    "grade": 2,
    "grade_cn": "二年级",
    "domain": "online-society",
    "domain_cn": "在线社会与信息表达",
    "lesson_type": "concept-practice",
    "version": "1.0.0",
    "description": "面向小学二年级：认识常见数字工具并按用途归类，学会为一件具体任务挑出合适的工具；通过十条可逐项打勾的安全自查清单和家庭使用小约定，落实时间有度、信息不露、内容先问三条安全规则。",
    "tags": ["数字工具", "工具的用途", "安全使用", "个人信息保护", "不点陌生链接"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》小学「在线社会与信息表达」——体验常用数字工具，知道安全、规范使用。",
    "hero_question": "身边的手机、平板、电脑，各能帮我们做什么？用的时候要注意什么？",
    "hero_alt": "常用数字工具与安全使用知识结构图：工具做什么用、怎么挑工具、安全三条规则",
    "hero_caption": "工具跟着任务走：查、记、算、画、聊、拍 · 怎么挑：先看清事情要什么 · 安全三条：时间有度、信息不露、内容先问",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的动手活动都会围着它转。",
    "anchor_choices": [
        {"t": "身边到底有哪些数字工具？", "d": "它们分别能帮我们做什么", "v": "身边到底有哪些数字工具"},
        {"t": "一件事该挑哪个工具？", "d": "怎么才能挑得又快又对", "v": "一件事该挑哪个工具"},
        {"t": "用的时候要守哪几条规矩？", "d": "安全使用到底要守什么", "v": "用的时候要守哪几条规矩"},
        {"t": "怎么做一张我家的使用约定？", "d": "让全家都记得住的约定长什么样", "v": "怎么做一张我家的使用约定"},
    ],
    "objectives": [
        "能说出至少五种常用数字工具，并说出它们分别帮我们做什么",
        "面对一件具体任务，能挑出一个合适的工具并说清楚理由",
        "能说出安全使用数字工具的三条规则：时间有度、信息不露、内容先问",
        "遇到陌生链接、陌生二维码或索要照片的消息，能做出不点、不说、告诉大人的选择",
    ],
    "objectives_plain": [
        "能说出至少五种常用数字工具，并说出它们分别帮我们做什么",
        "面对一件具体任务，能挑出一个合适的工具并说清楚理由",
        "能说出安全使用数字工具的三条规则：时间有度、信息不露、内容先问",
        "遇到陌生链接、陌生二维码或索要照片的消息，能做出不点、不说、告诉大人的选择",
    ],
    "standards": [
        {"content": "体验常用数字工具，知道安全、规范使用",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 在线社会与信息表达"},
        {"content": "使用数字工具时遵守时间约定，保护个人信息，遇到可疑内容主动求助",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 信息社会责任"},
    ],
    "prereqs": ["it-e-online-experience"],
    "prereqs_name": "在线体验与信息获取",
    "prereqs_meta": "it-e-online-experience",
    "leads_to": ["it-e-algorithm-steps"],
    "next_meta": "it-e-algorithm-steps",
    "section_images": ["assets/it-e-digital-tools-basic-fig1.webp", "assets/it-e-digital-tools-basic-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "工具很多，但用哪个、用多久、什么不能点，都有讲究。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能给一件事挑出对的工具，也能说出三条安全规则。",
        "objectives": "看清四件事：有哪些工具、怎么挑、守哪三条、遇到可疑怎么办。",
        "pretest": "凭直觉选就好，前测是帮你看清自己现在站在哪里。",
        "module-1": "工具按用途分成查、记、算、画、聊、拍六类，工具跟着任务走。",
        "lab-1": "先点一件事，再挑工具。有一件事的正确答案是「什么工具都不该用」，看看你能不能发现。",
        "module-2": "三条规则记成六个字：有度、不露、先问。",
        "lab-2": "十条清单，做到就点一下。没做到不等于做错，它只是下一条要努力的地方。",
        "worked-example": "四步走：看清来源、看它要什么、想清后果、做出决定。",
        "conceptest-1": "每个说法里都藏着一处不对，选完把解释读一遍。",
        "synthesis": "最多只能挑三条——约定太长，就没人记得住了。",
        "posttest": "出现了二维码、超时和要照片的消息，看看你还能不能用上三条规则。",
        "summary": "两句话加六个字：工具跟着任务走，安全守三条；不点、不说、告诉大人。",
        "homework": "三层小任务，先做前两层，第三层请和家人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学信息科技「在线社会与信息表达」里关于数字工具与安全使用的一课，前置节点是在线体验与信息获取。二年级学生认识不少工具，但习惯是「手里有什么工具就用什么工具」，安全教育的难点也不是不知道规则，而是不知道规则具体落在哪一下动作上。所以本课把概念压到两句：工具跟着任务走；安全守三条。两处动手都做成真能操作的模拟——第一处把六件真实小事和七个工具做匹配（其中一件的正确答案是「什么工具都不该用」，承载个人信息保护的价值引导）；第二处把三条安全规则拆成十条可以逐项打勾的清单，每勾一条都给出这条为什么重要的即时反馈，并实时给出安全分。综合任务让学生从六条候选里只挑三条，做成一张能被全家记住的使用小约定。",
    "plan_table": """| 1 | cover | 常用数字工具与安全使用 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：这些工具，你用得对吗？ | 起·前测（暴露直觉） |
| 5 | concept | 工具跟着任务走：什么事，用什么工具 | 承·概念一（六类用途） |
| 6 | interactive | 动手一：挑工具小管家，六件事你说了算 | 承·匹配互动（含「不该做」的价值引导） |
| 7 | concept | 安全使用守三条：时间有度、信息不露、内容先问 | 承·概念二 |
| 8 | interactive | 动手二：安全自查清单，一条一条点一点 | 承·动手二（逐项打勾 + 即时反馈 + 安全分） |
| 9 | concept | 例题示范：小美收到一条「免费领皮肤」的消息 | 转·重难点突破（分步示范 + 纠错） |
| 10 | quiz | 概念测试：每个说法里都藏着一处不对 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：给我家做一张使用小约定 | 合·迁移应用（限选三条的生成器） |
| 12 | quiz | 后测：换个新情境，三条规则还在不在 | 合·后测 |
| 13 | summary | 小结：两句话，把工具和安全都记住 | 合·小结与复述 |
| 14 | homework | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：工具做什么用 / 怎么挑工具 / 安全三条规则 三栏\n- P5 数字工具与用途对应图（已生成）：查、记、算、画、聊、拍六类\n- P7 安全使用三条规则图（已生成）：时间有度、信息不露、内容先问\n- 三张图均为教学示意图，不涉及任何真实软件界面、截图或商标\n- 若需补充：学生真实设备使用场景照片（需家长授权后使用）",
}
