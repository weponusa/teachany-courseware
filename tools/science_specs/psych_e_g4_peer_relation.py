# -*- coding: utf-8 -*-
"""小学心理健康 · 同伴交往与解决困难（G4）—— 补齐知识树「人际交往」空缺

学科语气（心理健康）：温和、不评判、不贴标签；只讲可操作的相处办法，不涉及伤害性情节。
四年级落点：想加入别人的游戏被拒绝、和好朋友闹别扭、被起外号这三种真实的
交友困境，练「情境 → 选做法 → 展开对方可能的反应与后果」，并把「正当求助不是打小报告」说清。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/psych-e-g4-peer-relation-fig1.webp'
F2 = './assets/psych-e-g4-peer-relation-fig2.webp'

TTS = {
    "hero": "小朋友，先想一想：课间你在操场边上，看见几个同学踢球踢得很开心，你很想走过去说我也想玩，可是脚像被粘在地上一样，怎么也开不了口。或者，你和最好的朋友闹了两天别扭，谁都不肯先说话。这节课我们就聊这些事。学完你会发现，想加入别人不是硬闯进去，闹别扭也不一定要等谁先低头；而且当你真的解决不了的时候，开口请人帮忙，是很聪明的做法，不是丢脸的事。",
    "problem-anchor": "开始之前，先选一个你最想知道的事。是想知道想加入别人的游戏被拒绝了该怎么办，还是想知道和好朋友闹别扭以后怎么和好，或者你最想问的是，有人给我起外号，我可以怎么回应，再或者你想弄明白，什么时候该找老师帮忙，什么时候该自己先试一试。选好了，就带着它往下看。",
    "objectives": "这节课有四个小目标。第一，能说出三种常见的交友困境：想加入被拒绝、和好朋友闹别扭、被起了不喜欢的称呼。第二，想加入同伴活动的时候，会用看一看、问一句、试一试这三步。第三，能和同伴闹别扭以后说出自己的感受，并提出一个具体的和好办法。第四，能分辨正当求助和打小报告，知道求助是保护自己，也是解决问题的一种办法。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先说第一件事：想加入别人的游戏。站在旁边不敢开口，或者一开口就被拒绝，心里都不好受。其实加入同伴活动有三步小准备。第一步看一看，先看看他们在玩什么、还缺不缺人、有没有轮到休息。第二步问一句，把想法说出来：我可以跟你们一起玩吗，我来当守门的可以吗。第三步试一试，先跟着大家一起玩一会儿，等熟悉了再提出自己的想法。请你记住一句话：被拒绝，不等于你不好。他们可能只是人够了，也可能这个游戏只能两个人玩。",
    "lab-1": "现在请你当一次交友小教练。下面有五个真实的课间情境，点开一个，再从三个做法里选一个。选完我会告诉你：对方可能会有怎样的反应，事情接下来会变成什么样。选得不太合适也不会说你错，只会告诉你这样可能会发生什么，还可以试试什么。",
    "module-2": "第二件事：闹别扭以后怎么办。和好朋友闹别扭，最难受的不是那天，而是接下来两天谁都不说话。我们可以走四步：停一停，说感受，听对方说，一起想一个下次的办法。说感受的时候只说自己的感觉，不给对方下结论，比如那天你那样说我，我心里挺难过的，比你怎么能这样说我，更容易让人听得进去。还有一件很要紧的事：需要帮忙的时候，求助不是打小报告。正当求助是为了让谁更安全、把问题解决掉，说的时候讲清事实，也说说自己试过什么；打小报告是为了让别人挨批评，把别人的小事专门讲一遍。判断的时候可以问自己三句话：这件事有没有人受伤，我自己试过了吗，我说的是事实吗。",
    "lab-2": "现在请你当一次小法官。下面有八张小事卡，请你把它们放进三个框里：哪些可以自己先试一试，哪些是正当求助，哪些属于打小报告。放错了也没关系，我会告诉你为什么，再给你换一个判断的角度。",
    "worked-example": "我们一起帮小禾想一想。课间跳绳，小禾很想加入，走过去说我想玩，同学说人够了。小禾心里一下凉了。第一步，先看一看：他站在旁边看了一会儿，发现摇绳的同学手酸了，一直在换手。第二步，问一句：他问，我来帮你们摇绳好不好。第三步，试一试：他认认真真摇了两分钟，大家跳得很顺。后来他们还主动叫小禾一起跳。你看，小禾一句都没有争，他只是换了一个能进去的位置。万一还是不行呢，那就问一问什么时候人多，或者去找另一个也在等人的同学，一起玩别的。",
    "conceptest-1": "接下来用三个说法考考你，每一个里面都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件事交给你。请从三栏里各选一条，拼成你自己的交友小名片：遇到什么情况，我先做什么，如果还不行可以请谁帮忙。拼好以后，把它说给同桌听一遍。",
    "posttest": "最后一轮，换三个新的小情境来考考你。这次会出现小组分工争起来、新同学一个人坐着、还有同学让你别跟某个人玩，看看你能不能用上今天的办法。",
    "summary": "这节课我们记住三句话。第一句，想加入别人的游戏，走三步：看一看、问一句、试一试；被拒绝不等于你不好。第二句，闹别扭以后走四步：停一停、说感受、听对方说、一起想一个下次的办法。第三句，正当求助不是打小报告——有人受伤、自己试过还是不行，就去找可以帮忙的大人，说事实，说你试过什么。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出三种交友困境，再写出想加入同伴活动时的三步。第二层能力应用，动手做：做一张交友小名片，写上我先做什么、如果不行可以请谁帮忙。第三层迁移挑战，选做：这一周里，主动和一个平时不太说话的同学聊一件事，回来把经过写两句话。",
    "knowledge-graph": "这张图展示了这节课在心理健康知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 想加入，先做三步小准备", "lab-1": "动手一 交友小教练",
    "module-2": "概念二 闹别扭以后，说开与求助", "lab-2": "动手二 求助还是打小报告",
    "worked-example": "例题讲解 小禾的跳绳", "conceptest-1": "概念测试",
    "synthesis": "综合任务 我的交友小名片", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：交友困境小教练（情境 → 选做法 → 展开对方的反应与后果） ──
SCENES = [
    {
        "id": "s1",
        "t": "课间踢球，我跑过去说想加入，他们喊：人够了！",
        "opts": [
            {"k": "a", "t": "先站旁边看一会儿，等有人下来休息时问一句：我来替一会儿好不好，我会守门", "ok": True,
             "fb": "对方多半会说：那你来守门吧。等他们看见你认真，下一次常常会主动叫你。你只是换了一个能进去的位置，一点也没输。"},
            {"k": "b", "t": "一句话不说，转身走开，心里想：他们肯定不喜欢我", "ok": False,
             "fb": "他们可能根本不知道你想一起玩，下一次还是不会叫你；而你会把这件小事记很久。这样可能会让你更难受，还可以试试：先看一会儿，再挑一个合适的时机问一句。"},
            {"k": "c", "t": "冲他们大声说：你们凭什么不让我玩！", "ok": False,
             "fb": "对方可能会被吓一跳，也可能跟你吵起来，球也踢不成了。这样可能会让大家都下不来台，还可以试试：把话说清楚就够——「我可以跟你们一起玩吗？我当守门的。」"},
        ],
    },
    {
        "id": "s2",
        "t": "和最好的朋友闹别扭，他已经两天没跟我说话了",
        "opts": [
            {"k": "a", "t": "先想一想是不是自己那句话让他难受，再找个只有我们俩的时候说开", "ok": True,
             "fb": "对方可能会先愣了一下，然后也说出一句心里话。两天的不说话，常常就这样过去了。说感受的时候只说自己的感觉，比怪对方更容易被听进去。"},
            {"k": "b", "t": "等他先来找我，谁先开口谁就输了", "ok": False,
             "fb": "他可能也在等你先开口，两个人就这样一直僵着，越等越难开口。这样可能会让这段友谊白白多难过几天，还可以试试：找一个只有你们俩的时候，先说一句「那天的事，我想跟你说说」。"},
            {"k": "c", "t": "把这件事讲给别的同学听，让大家来评评理", "ok": False,
             "fb": "话传到对方耳朵里，他可能会更难受，本来两个人的事变成了全班的话题。这样可能会让事情变大，还可以试试：先和当事人说，说不通再请老师帮忙。"},
        ],
    },
    {
        "id": "s3",
        "t": "有同学给我起了一个我不喜欢的称呼，一叫大家就笑",
        "opts": [
            {"k": "a", "t": "先深吸一口气，看着他说：我不喜欢这个称呼，请叫我的名字", "ok": True,
             "fb": "对方可能会愣一下，然后换个叫法；就算他没马上改，你身边的人也听明白了你的态度。说「我不喜欢」本身就是一种很有力量的表达。"},
            {"k": "b", "t": "也给他起一个更难听的称呼，让他也尝尝这个滋味", "ok": False,
             "fb": "对方可能会立刻还回来，两个人越叫越难听，旁边的人还在笑。这样可能会让两个人都下不来台，还可以试试：只说自己的感受——「我不喜欢这个称呼。」"},
            {"k": "c", "t": "装作没听见，回家一个人难受很久", "ok": False,
             "fb": "对方可能会以为你不在意，下次还这样叫；而这份难受全落在你一个人身上。这样可能会让你憋得更久，还可以试试：当场说一句「请叫我的名字」，或者回家说给爸爸妈妈听。"},
        ],
    },
    {
        "id": "s4",
        "t": "小组做手工，我和同桌都想照自己的办法做，谁都不肯让",
        "opts": [
            {"k": "a", "t": "停一停，说：我们各说一遍理由，再各试一分钟，哪个好就用哪个", "ok": True,
             "fb": "同桌可能会点头试一下。一个小小的试验，常常比争十分钟都快。争的是办法，不是谁高谁低——把这句话记住。"},
            {"k": "b", "t": "不说了，直接把材料拿过来先做起来", "ok": False,
             "fb": "同桌可能会很生气，也可能干脆不做了，剩下的活都归你。这样可能会让小组散了架，还可以试试：先停一停，各说一遍理由，再各试一分钟。"},
            {"k": "c", "t": "我不做了，让他们自己弄吧", "ok": False,
             "fb": "作品做不成，你的想法也没人知道。这样可能会让你既生气又吃亏，还可以试试：说一句「我有个想法，先听我说十秒钟」。"},
        ],
    },
    {
        "id": "s5",
        "t": "新同学转来第三天了，他一个人坐在座位上，没有人跟他说话",
        "opts": [
            {"k": "a", "t": "走过去问一句：你叫什么名字？课间要不要一起去看看我们班的植物角", "ok": True,
             "fb": "他可能会有点害羞，但眼睛会亮一下。你这一句话，可能就是他这一周最想听到的。你自己刚转学的时候，大概也等过这样一句话。"},
            {"k": "b", "t": "等他先来跟我说话吧", "ok": False,
             "fb": "他可能也在等别人先开口，两个人就一直坐着。这样可能会让新同学更孤单，还可以试试：你先问一句他的名字，或者问问他原来在哪个学校。"},
            {"k": "c", "t": "想跟他玩，又怕别人笑我，就假装没看见", "ok": False,
             "fb": "你可能一整天都有点别扭。这样可能会让你自己也不舒服，还可以试试：找一个你信任的同学一起去，两个人一起开口，就不那么难了。"},
        ],
    },
]

# ── 动手二：求助还是打小报告（八张小事卡 → 三个框） ──
BINS = [
    {"id": "self", "name": "① 自己先试一试"},
    {"id": "help", "name": "② 正当求助（找大人或同伴帮忙）"},
    {"id": "tell", "name": "③ 打小报告（不合适）"},
]

ITEMS = [
    {"id": "c1", "bin": "self", "t": "想加入别人的游戏，先看一会儿他们在玩什么，再开口问一句",
     "fb": "对，这是自己先试一试。看一看、问一句，是进入同伴活动最常见的第一步。"},
    {"id": "c2", "bin": "self", "t": "好朋友两天不理我，我先想一想自己是不是说错了话，再找机会说开",
     "fb": "对，这是自己先试一试。先想一想，不是认输，是给自己多一个办法。"},
    {"id": "c3", "bin": "self", "t": "被起了不喜欢的称呼，先深吸一口气，告诉对方我不喜欢这个称呼，然后走开",
     "fb": "对，这是自己先试一试。一句话说清楚自己的边界，手不动、嘴不骂，已经很了不起。"},
    {"id": "c4", "bin": "help", "t": "被同学撞倒，膝盖破皮出血了，去告诉老师请老师帮忙处理",
     "fb": "对，这是正当求助。有人受伤的时候，找大人帮忙是最快的办法，也是保护自己。"},
    {"id": "c5", "bin": "help", "t": "被起了不喜欢的称呼，心里很久放不下，回家说给爸爸妈妈听",
     "fb": "对，这是正当求助。心里的事说出来，就不用一个人扛着；愿意听你说话的人，也可以是家里人。"},
    {"id": "c6", "bin": "help", "t": "看见同学被大孩子拦住要东西，赶紧去找老师过来看看",
     "fb": "对，这是正当求助。这不是管别人的闲事，是有人需要帮忙，而你一个人解决不了。"},
    {"id": "c7", "bin": "tell", "t": "想让老师批评上课说话的同学，专门跑去讲一遍",
     "fb": "这更接近打小报告。目的不是把人扶起来，而是让人挨批评。还可以试试：如果这件事影响了大家上课，可以让老师知道情况，但说的时候只说事实，不评价别人。"},
    {"id": "c8", "bin": "tell", "t": "把同桌没交作业的事专门告诉老师，希望老师批评他",
     "fb": "这更接近打小报告。别人的小事不归你管，专门去讲一遍，对方可能会很难受。还可以试试：先问一问同桌是不是遇到什么困难，需要时陪他一起去找老师。"},
]

# ── 综合任务：我的交友小名片（三栏各选一条） ──
CARD = {
    "case": {
        "name": "① 我遇到的情况",
        "items": [
            {"id": "k1", "t": "想加入别人的游戏，被说人够了"},
            {"id": "k2", "t": "和好朋友闹别扭，两天不说话"},
            {"id": "k3", "t": "被起了我不喜欢的称呼"},
            {"id": "k4", "t": "小组里为了用谁的办法争起来"},
        ],
    },
    "step": {
        "name": "② 我先做的一件事",
        "items": [
            {"id": "d1", "t": "看一看，再挑一个合适的时机问一句"},
            {"id": "d2", "t": "停一停，先说自己的感受：我心里挺难过的"},
            {"id": "d3", "t": "说出来：我不喜欢这个称呼，请叫我的名字"},
            {"id": "d4", "t": "各说一遍理由，再各试一分钟"},
        ],
    },
    "help": {
        "name": "③ 如果还不行，我可以请谁帮忙",
        "items": [
            {"id": "h1", "t": "我信任的一个同学，两个人一起开口"},
            {"id": "h2", "t": "老师，请老师帮我们商量一下"},
            {"id": "h3", "t": "爸爸妈妈，回家把这件事说给他们听"},
        ],
    },
}

CUSTOM_JS = r"""
/* ============================================================
   psych-e-g4-peer-relation 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 交友小教练：五个困境 × 三个做法 → 展开对方可能的反应与后果
   3) 求助还是打小报告：八张小事卡 → 三个框
   4) 我的交友小名片：三栏各选一条，拼成一句话
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

  /* ---------- 2. 交友小教练 ---------- */
  var SCENES = __SCENES_JSON__;
  var stage = document.getElementById('peer-stage');
  if (stage) {
    var cur = null, done = {};
    var out = document.getElementById('peer-out');
    var score = document.getElementById('peer-score');

    function sceneById(id) {
      for (var i = 0; i < SCENES.length; i++) { if (SCENES[i].id === id) return SCENES[i]; }
      return null;
    }
    function render() {
      document.querySelectorAll('[data-peer]').forEach(function (b) {
        var k = b.dataset.peer;
        b.classList.toggle('selected', k === cur);
        b.classList.toggle('done', !!done[k]);
      });
      score.textContent = '已经聊过 ' + Object.keys(done).length + ' / ' + SCENES.length + ' 个情境';
    }
    function paint() {
      var box = document.getElementById('peer-opts');
      box.innerHTML = '';
      if (!cur) return;
      var S = sceneById(cur);
      if (!S) return;
      S.opts.forEach(function (o) {
        var b = document.createElement('button');
        b.className = 'choice' + (done[cur] && o.ok ? ' correct' : '');
        b.style.textAlign = 'left';
        b.textContent = o.t;
        b.addEventListener('click', function () {
          if (done[cur]) return;
          if (o.ok) {
            done[cur] = true;
            out.className = 'result';
            out.innerHTML = '<strong>这个做法挺稳当。</strong>我们看看接下来会怎样：' + o.fb;
          } else {
            out.className = 'result warn';
            out.innerHTML = '<strong>这样做也很好理解，我们一起看看会发生什么。</strong>' + o.fb;
          }
          render();
          paint();
        });
        box.appendChild(b);
      });
    }
    document.querySelectorAll('[data-peer]').forEach(function (b) {
      b.addEventListener('click', function () {
        cur = b.dataset.peer;
        var S = sceneById(cur);
        if (done[cur]) {
          out.className = 'result';
          out.innerHTML = '<strong>这个情境已经聊过啦。</strong>记住那个稳当的做法，下次真的遇上，就可以照着做。';
        } else {
          out.className = 'result warn';
          out.innerHTML = '<strong>你遇到的是：' + S.t + '</strong><br>下面有三个做法，选一个，我们看看对方可能会有什么反应。';
        }
        render();
        paint();
      });
    });
    render();
  }

  /* ---------- 3. 求助还是打小报告 ---------- */
  var ITEMS = __ITEMS_JSON__;
  var BINS = __BINS_JSON__;
  var bank = document.getElementById('sort-bank');
  if (bank && ITEMS.length) {
    var placed = {}, picked = null;
    var out2 = document.getElementById('sort-out');
    var score2 = document.getElementById('sort-score');

    function itemById(id) {
      for (var i = 0; i < ITEMS.length; i++) { if (ITEMS[i].id === id) return ITEMS[i]; }
      return null;
    }
    function binOf(id) {
      for (var i = 0; i < BINS.length; i++) { if (BINS[i].id === id) return BINS[i]; }
      return null;
    }
    ITEMS.forEach(function (it) {
      var b = document.createElement('button');
      b.className = 'sort-item';
      b.dataset.pick = it.id;
      b.textContent = it.t;
      b.addEventListener('click', function () {
        if (placed[it.id]) return;
        picked = it.id;
        document.querySelectorAll('[data-pick]').forEach(function (x) {
          x.classList.toggle('selected', x.dataset.pick === picked);
        });
        out2.className = 'result warn';
        out2.innerHTML = '<strong>你选中了这一张：</strong>' + it.t + '<br>它应该放进哪个框里？点一下上面的框试试。';
      });
      bank.appendChild(b);
    });
    BINS.forEach(function (bn) {
      var box = document.getElementById('sort-bin-' + bn.id);
      if (!box) return;
      box.addEventListener('click', function () {
        if (!picked) {
          out2.className = 'result warn';
          out2.textContent = '先在左边点一张小事卡，再点这个框。';
          return;
        }
        var it = itemById(picked);
        if (!it || placed[it.id]) return;
        placed[it.id] = true;
        var right = (it.bin === bn.id);
        var card = document.querySelector('[data-pick="' + it.id + '"]');
        if (card) { card.classList.add('done'); card.classList.remove('selected'); }
        var tag = document.createElement('span');
        tag.className = 'tag';
        tag.style.borderColor = right ? 'rgba(78,205,196,.9)' : 'rgba(239,68,68,.7)';
        tag.textContent = it.t;
        box.querySelector('.bin-list').appendChild(tag);
        box.classList.toggle('ok', right);
        box.classList.toggle('no', !right);
        picked = null;
        var n = Object.keys(placed).length;
        score2.textContent = '已经放好 ' + n + ' / ' + ITEMS.length + ' 张';
        if (right) {
          out2.className = 'result';
          out2.innerHTML = '<strong>放对了。</strong>' + it.fb;
        } else {
          out2.className = 'result warn';
          out2.innerHTML = '<strong>它更合适的框是「' + binOf(it.bin).name.replace(/^[①②③]\s*/, '') + '」。</strong>' + it.fb;
        }
        if (n === ITEMS.length) {
          out2.className = 'result';
          out2.innerHTML = '<strong>八张小事卡全放好了。</strong>以后再遇到拿不准的事，就问自己三句话：这件事有没有人受伤？我自己试过了吗？我说的是事实吗？三句里只要有一句指向帮忙，去找大人说，就是正当求助。';
        }
      });
    });
    score2.textContent = '已经放好 0 / ' + ITEMS.length + ' 张';
  }

  /* ---------- 4. 我的交友小名片 ---------- */
  var CARD = __CARD_JSON__;
  var cardStage = document.getElementById('card-stage');
  if (cardStage) {
    var chosen = {}, order = ['case', 'step', 'help'];
    var out3 = document.getElementById('card-out');

    function textOf(col, id) {
      var arr = CARD[col].items;
      for (var i = 0; i < arr.length; i++) { if (arr[i].id === id) return arr[i].t; }
      return '';
    }
    function render3() {
      Object.keys(CARD).forEach(function (col) {
        document.querySelectorAll('[data-card="' + col + '"]').forEach(function (b) {
          b.classList.toggle('selected', chosen[col] === b.dataset.cardId);
        });
        var slot = document.getElementById('card-pick-' + col);
        if (slot) {
          slot.textContent = chosen[col] ? textOf(col, chosen[col]) : '还没有选';
          slot.style.color = chosen[col] ? 'var(--text)' : 'var(--muted)';
        }
      });
      var n = order.filter(function (c) { return chosen[c]; }).length;
      document.getElementById('card-score').textContent = '名片已经写上 ' + n + ' / 3 条';
      if (n === 3) {
        out3.className = 'result';
        out3.innerHTML = '<strong>你的交友小名片写好了：</strong>遇到' + textOf('case', chosen.case) +
          '的时候，我先' + textOf('step', chosen.step) + '；如果还不行，我就请' + textOf('help', chosen.help) + '。' +
          '<br><span style="color:var(--muted)">把这句话念给同桌听一遍，念出来，它就真的属于你了。</span>';
      } else {
        out3.className = 'result warn';
        out3.textContent = '三栏各选一条，名片就写好了。';
      }
    }
    Object.keys(CARD).forEach(function (col) {
      document.querySelectorAll('[data-card="' + col + '"]').forEach(function (b) {
        b.addEventListener('click', function () {
          chosen[col] = b.dataset.cardId;
          render3();
        });
      });
    });
    render3();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__SCENES_JSON__', json.dumps(SCENES, ensure_ascii=False))
             .replace('__ITEMS_JSON__', json.dumps(ITEMS, ensure_ascii=False))
             .replace('__BINS_JSON__', json.dumps(BINS, ensure_ascii=False))
             .replace('__CARD_JSON__', json.dumps(CARD, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "我走过去说想加入踢球，他们回答人够了。下面哪个想法更合适？",
         "options": [("人够了不等于他们不喜欢我，我可以换个方式再问一次", True),
                     ("他们肯定讨厌我，以后再也不找他们了", False),
                     ("他们不让我玩，我也不让他们玩", False)],
         "explain": "被拒绝的原因常常很简单：人够了、这个游戏只能两个人玩、这会儿不方便。"
                    "<strong>错因提醒：</strong>常见错误是把「这件事没成」误认为「我这个人不行」——把一件事的答案，当成了对自己的评价。"},
        {"q": "和好朋友闹别扭，两天没说话了。下面哪个做法更合适？",
         "options": [("找一个只有我们俩的时候，先说一句：那天的事我想跟你说说", True),
                     ("等他先来找我，谁先开口谁就输", False),
                     ("讲给全班同学听，让大家来评评理", False)],
         "explain": "先说一句自己的感受，比等谁先低头更容易把话说开；两个人的事，放在两个人之间解决。"
                    "<strong>错因提醒：</strong>有人误认为先开口就是认输——其实先开口的人，是把这段友谊看得更重要的人。"},
        {"q": "下面哪一件事属于正当求助，不属于打小报告？",
         "options": [("被同学撞倒膝盖出血了，去找老师帮忙处理", True),
                     ("想告诉老师谁上课说话，让他被批评", False),
                     ("把同桌没交作业的事专门讲一遍", False)],
         "explain": "有人受伤、自己试过还是不行，就去找能帮忙的大人——这是正当求助。"
                    "<strong>错因提醒：</strong>最容易搞混的是把「想让别人挨批评」也当成求助；判断的时候问一句：这件事有没有人受伤？我说的是事实吗？"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "想加入，先做三步小准备", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">三年级的时候，我们已经知道自己在班里有哪些角色，也知道见人要问好（And）；可是轮到自己想加入别人的游戏，脚就像被粘在地上，或者一开口就被一句「人够了」挡回来，心里一下子凉了（But）；所以这节课先学最要紧的一件事——怎么走进同伴的活动里（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">想加入一群正在玩的同学，不需要硬闯进去，也不必一直站在旁边。可以用<strong>三步小准备</strong>。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看一看：</strong>先看他们在玩什么、还缺不缺人、有没有人正想下来休息。看一会儿，你就知道从哪儿进去。</div></div>
          <div class="step"><span class="n">2</span><div><strong>问一句：</strong>把想法说出来——「我可以跟你们一起玩吗？」「我来当守门的可以吗？」</div></div>
          <div class="step"><span class="n green">3</span><div><strong>试一试：</strong>先跟着大家一起玩一会儿，等熟悉了，再提出自己的想法。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="加入同伴活动的三步示意图：看一看、问一句、试一试，附中文标注">
          <figcaption>示意图：想加入同伴的活动，走三步——看一看、问一句、试一试（教学示意图，人物为中性简洁插画）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「被拒绝就是他们不喜欢我」。其实被拒绝的原因常常和「你这个人怎么样」没关系——人够了、游戏只能两个人玩、这会儿不方便，都是很常见的原因。要紧的不是这一次成没成，而是你有没有给自己留一句可以再问的话。</p>
        </div>
        <div class="kid-note"><span class="emoji">💛</span><div><strong>一句要紧的话：</strong>想和别人一起玩，是一件很自然的事。你在门口站了一会儿，只是因为还没找到进去的方式，不是因为你不好。</div></div>
{insight_box([
    {"lens": "看见它", "text": "「被拒绝」这三个字看着很大，其实常常只是一句很具体的话：人够了。把这句话听成一件小事，心里就松一点。"},
    {"lens": "解释它", "text": "为什么要先看一看？因为直接冲进去，别人正在玩到一半，多半会先拒绝；先看清场面，你就能挑到一个真的能进去的位置。"},
    {"lens": "迁移它", "text": "这三步到哪里都好用：新的兴趣班、小区里的球场、转学后的第一天——先看一看，再问一句，然后试一试。"},
])}
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>看一看，问一句，试一试——<strong>被拒绝，不等于我不好。</strong></div></div>
    ''', tag="概念一"))

    peer_btns = "\n".join(
        f'            <button class="choice" data-peer="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in SCENES
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：交友小教练，看一看会发生什么", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一个课间情境，再从三个做法里选一个。<strong>选得不太合适也不会说你错</strong>，只会告诉你：对方可能会有什么反应，事情接下来会变成什么样，还可以试试什么。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 我遇到的一件事</div>
          <div class="grid" id="peer-stage">
{peer_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 我可以做的一件事</div>
          <div class="grid" id="peer-opts">
            <span style="color:var(--muted);font-size:14px">先在上面点一件事，这里就会出现三个做法。</span>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">聊过几个情境</span><span class="v" id="peer-score">已经聊过 0 / 5 个情境</span></div>
          </div>
          <p class="result warn" id="peer-out" style="margin-top:12px">先点一个你今天可能遇到的情境。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>小教练的秘密：</strong>这里的重点不是「选对」，而是看看<strong>同一个情境、不同做法，对方会怎么反应</strong>。看完再想一想，哪一个更像你平时的做法。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "闹别扭以后怎么说开；求助不是打小报告", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">和好朋友闹别扭，最难受的不是那天，而是接下来两天谁都不说话。想和好，可以走<strong>四步</strong>。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>停一停：</strong>先别急着还回去，做几次慢慢的呼吸，让身体慢下来。</div></div>
          <div class="step"><span class="n">2</span><div><strong>说感受：</strong>只说自己的感觉——「那天你那样说，我心里挺难过的。」不给对方下结论。</div></div>
          <div class="step"><span class="n">3</span><div><strong>听对方说：</strong>他的话里可能也有你不知道的原因，先听完。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>一起想一个下次的办法：</strong>「下次我们谁先不高兴了，就先说一句好不好？」</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="求助不是打小报告的判断三问示意图，附中文标注">
          <figcaption>示意图：拿不准的时候问自己三句话——有没有人受伤？我自己试过了吗？我说的是事实吗？（教学示意图，人物为中性简洁插画）</figcaption>
        </figure>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>正当求助是</strong></p>
            <p style="color:var(--muted)">为了让大家安全、把问题解决掉，去找能帮忙的大人：说事情经过，说说自己试过什么，也说出你需要什么帮助。</p>
          </div>
          <div class="inner-card">
            <p><strong>打小报告是</strong></p>
            <p style="color:var(--muted)">为了让别人挨批评，把别人的小事专门讲一遍，甚至添上自己的猜测。管的是别人，不是问题。</p>
          </div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「找老师就是打小报告，会被同学说闲话」，于是一个人硬扛。这里最容易<strong>搞混</strong>的是两者想要的结果：一个想把事解决掉，一个想让人挨批评。只要你是为了让谁更安全、把事情说清楚，那就是正当求助。</p>
        </div>
{insight_box([
    {"lens": "拆开它", "text": "「闹别扭」拆开看是两件事：一件是我心里不舒服（感觉），一件是接下来我做什么（做法）。感觉不用道歉，做法可以挑。"},
    {"lens": "比较它", "text": "「你怎么能这样说」和「你那样说的时候我有点难过」——说的是同一件事，听的人反应常常很不一样。第二句只讲自己，不审判别人。"},
    {"lens": "迁移它", "text": "这四步在家里和兄弟姐妹闹别扭时也管用；求助的三问，在小区里、在兴趣班也能用。"},
])}
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>停一停，说感受，听对方说，想个下次的办法——<strong>求助不是打小报告。</strong></div></div>
    ''', tag="概念二"))

    sort_bins = "\n".join(
        f'''            <div class="sort-bin" id="sort-bin-{b["id"]}" role="button" tabindex="0">
              <h4>{b["name"]}</h4>
              <div class="bin-list"></div>
            </div>'''
        for b in BINS
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：求助，还是打小报告？", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先在左边点一张小事卡，再点下面三个框中的一个，把它放进去。<strong>放错了也不扣分</strong>，我会告诉你它更合适放在哪儿，以及为什么。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 八张小事卡（点一张选中）</div>
          <div class="sort-bank" id="sort-bank"></div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 它属于哪一类</div>
          <div class="sort-bins" style="grid-template-columns:1fr">
{sort_bins}
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">放进去了几张</span><span class="v" id="sort-score">已经放好 0 / 8 张</span></div>
          </div>
          <p class="result warn" id="sort-out" style="margin-top:12px">先在左边点一张小事卡。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💛</span><div><strong>放不下的时候问三句：</strong>这件事有没有人受伤？我自己试过了吗？我说的是事实吗？——三句里只要有一句指向「需要帮忙」，去找大人说，就是正当求助。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小禾想加入跳绳，被说人够了", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>课间跳绳，小禾很想加入，走过去说「我想玩」，同学回答「人够了」。他的脸一下子热了。请你陪他走三步。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看一看：</strong>小禾没有走开，先站在旁边看了一会儿。他发现摇绳的同学手酸了，一直在换手。</div></div>
          <div class="step"><span class="n">2</span><div><strong>问一句：</strong>他问：「我来帮你们摇绳好不好？我会数拍子。」——他换了一个能进去的位置。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>试一试：</strong>他认认真真摇了两分钟，大家跳得很顺。后来，他们主动叫小禾一起跳。</div></div>
        </div>
        <div class="inner-card">
          <p><strong>如果还是不行呢？</strong></p>
          <p style="color:var(--muted)">还可以问一句「那你们什么时候人少一点」；或者去找另一个也在等人的同学，一起玩别的。一次没成，只说明这一种方式这次不合适。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「被拒绝了还要再问，很没面子」。小禾这三次开口，一次也没有低三下四——他一直在做同一件事：找到自己能出力的地方。真正让人看得起的，不是从不被拒绝，而是被拒绝以后还能好好说话。</p>
        </div>
        <div class="inner-card">
          <p><strong>说给同桌听：</strong>小禾这三步里，哪一步你自己已经做到了？哪一步还想再练一练？</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "下面哪句话说得对？",
         "options": [("想加入同伴的活动，可以先看一看，再问一句，然后试一试", True),
                     ("被别人拒绝一次，就说明我不适合和他们玩", False),
                     ("想和别人一起玩，最好等别人主动来叫我", False)],
         "explain": "看一看、问一句、试一试，是自己能掌控的三步；它把「能不能进去」变成了一件可以练习的事。"
                    "<strong>错因提醒：</strong>常见错误是把一次被拒绝误认为对自己的评价；也有的同学误认为主动开口很丢脸——其实主动的人，只是更想要这段相处而已。"},
        {"q": "和好朋友闹别扭了，下面哪个说法更合适？",
         "options": [("那天你那样说，我心里挺难过的", True),
                     ("你怎么能这样对我，你也太过分了", False),
                     ("算了，以后我再也不理他了", False)],
         "explain": "说自己感受的时候，只讲自己的感觉，对方更容易听得进去，也更容易接话。"
                    "<strong>错因提醒：</strong>容易搞混的是「说感受」和「给对方下结论」——「你太过分了」是在审判人，「我有点难过」是在说自己的心情。"},
        {"q": "下面哪件事是正当求助，不是打小报告？",
         "options": [("同学被大孩子拦住要东西，我去请老师过来看看", True),
                     ("想让老师批评上课说话的同学，专门去讲一遍", False),
                     ("把同桌没交作业的事专门告诉老师", False)],
         "explain": "有人可能受伤害、你自己也解决不了的时候，找大人帮忙是最合适的办法。"
                    "<strong>错因提醒：</strong>最常搞混的是目的——为了让谁更安全、把事情说清楚，是求助；为了让谁挨批评，就变成了打小报告。"}
    ], tag="概念测试"))

    card_blocks = []
    for col in ("case", "step", "help"):
        btns = "\n".join(
            f'              <button class="choice" data-card="{col}" data-card-id="{it["id"]}" style="text-align:left">{it["t"]}</button>'
            for it in CARD[col]["items"]
        )
        card_blocks.append(f'''          <div class="inner-card">
            <p><strong>{CARD[col]["name"]}</strong>　<span style="color:var(--muted);font-size:13px">已选：</span><span id="card-pick-{col}" style="color:var(--muted)">还没有选</span></p>
            <div class="grid" style="margin-top:8px">
{btns}
            </div>
          </div>''')
    card_html = "\n".join(card_blocks)
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：写一张属于你的交友小名片", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">三栏里各选一条，拼成一句话。这句话就是你的<strong>交友小名片</strong>，下次真的遇上，照着它走一步就行。</p>
        <div class="lab-panel" id="card-stage">
{card_html}
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">名片进度</span><span class="v" id="card-score">名片已经写上 0 / 3 条</span></div>
          </div>
          <p class="result warn" id="card-out" style="margin-top:12px">三栏各选一条，名片就写好了。</p>
        </div>
        <div class="inner-card">
          <p><strong>把它变成你自己的话：</strong></p>
          <p style="color:var(--muted)">想一想，这一周你最可能遇上哪一件事？把上面选好的三条，写成你自己的句子。</p>
          <textarea id="syn-answer" rows="3" placeholder="遇到……的时候，我先……；如果还不行，我就请……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换三个新情境，办法还在不在", TTS["posttest"], [
        {"q": "小组做展板，我和同桌都想照自己的办法排，谁也不肯让。下面哪个做法更合适？",
         "options": [("停一停，各说一遍理由，再各试一分钟，哪个好看就用哪个", True),
                     ("直接把材料拿过来先做起来", False),
                     ("不做了，让他们自己弄", False)],
         "explain": "争的是办法，不是谁高谁低。一个小试验，常常比争十分钟都快。"
                    "<strong>错因提醒：</strong>有人误认为「让一步就是输」，于是干脆撒手不管——结果作品没做成，自己的想法也没人听见。"},
        {"q": "新同学转来第三天，一直一个人坐着。下面哪个做法更合适？",
         "options": [("走过去问一句他的名字，再邀他一起去看看植物角", True),
                     ("等他先来跟我说话", False),
                     ("想跟他说话，又怕别人笑我，就假装没看见", False)],
         "explain": "你先开口的这一句，可能就是他这一周最想听到的一句话。"
                    "<strong>错因提醒：</strong>常见错误是误认为「他那么安静，应该是不想被打扰」——安静和孤单，看起来很像，问一句才知道。"},
        {"q": "有同学跟你说：你以后别跟小宇玩，跟我们玩就行。下面哪个做法更合适？",
         "options": [("说清楚：我和他玩，也可以和你们玩", True),
                     ("当场答应，回头偷偷再去找小宇", False),
                     ("两边都不理了，一个人待着", False)],
         "explain": "把话说清楚，别人就知道你的界线在哪里；偷偷来偷偷去，最后两边都不好受。"
                    "<strong>错因提醒：</strong>不要误认为「必须选一边才安全」——真实的情况常常是，你可以同时和不同的人做朋友。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，讲清同伴交往这件事", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>想加入，走三步：</strong>看一看、问一句、试一试。被拒绝，不等于我不好。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>闹别扭，走四步：</strong>停一停、说感受、听对方说、一起想一个下次的办法。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>需要帮忙就开口：</strong>正当求助不是打小报告，说事实，说你试过什么。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>还要记牢一件事：</strong>和同伴相处，有开心也一定有闹别扭的时候，两样都很正常。如果有些事你自己试过还是解决不了，心里也一直放不下，说给老师或者爸爸妈妈听，是很聪明的做法。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「看一看、问一句、试一试」这三个词，说清楚你上一次想加入同伴活动的经过。</p>
          <p style="color:var(--muted)">再动一动手：<strong>画一画</strong>你的三步小台阶，在每一级台阶上写一个你自己做得到的小动作。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "说出三种常见的交友困境：想加入被拒绝、和好朋友闹别扭、被起了不喜欢的称呼。",
            "写出想加入同伴活动时的三步：看一看、问一句、试一试。",
            "写出判断正当求助的三个问题。",
        ],
        [
            "做一张「交友小名片」：写上我先做什么、如果不行可以请谁帮忙，贴在书桌前。",
            "把「停一停、说感受、听对方说、想个下次的办法」四步写下来，说给家里人听一遍。",
        ],
        [
            "这一周里，主动和一个平时不太说话的同学聊一件事，回来写两句话说说经过。",
            "和同桌一起想一想：我们班的同学闹别扭时，可以做一件什么小事让气氛松一点？写两条建议。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "psych-e-g4-peer-relation",
    "node_id": "psych-e-g4-peer-relation",
    "subject": "psychology",
    "subject_cn": "心理健康",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "中小学心理健康教育指导纲要（2012年修订）/ 教育部相关要求 · 小学",
    "title": "同伴交往与解决困难",
    "name_en": "Getting Along with Peers: Joining In, Making Up, Asking for Help",
    "grade": 4,
    "grade_cn": "四年级",
    "domain": "interpersonal",
    "domain_cn": "人际交往",
    "lesson_type": "workshop",
    "version": "1.0.0",
    "description": "面向小学四年级的同伴交往课：围绕三种真实的交友困境——想加入别人的游戏被拒绝、和好朋友闹别扭、被起了不喜欢的称呼，练「看一看、问一句、试一试」和「停一停、说感受、听对方说、想个下次的办法」，并把「正当求助不是打小报告」说清楚。两个互动台子都能真的操作：一个是交友小教练，五个课间情境各配三个做法，选完会展开对方可能的反应与后果，错误反馈一律写成「这样可能会……，还可以试试……」；一个是八张小事卡的分类台，把「自己先试试」「正当求助」「打小报告」分清楚。综合任务把三条做法拼成个人化的「交友小名片」。全课语气温和、不评判、不贴标签，只讲可操作的相处办法，不涉及伤害性情节；插图一律为中性简洁的教学插画。",
    "tags": ["同伴交往", "解决困难", "求助边界", "四年级", "人际交往"],
    "standard_ref": "《中小学心理健康教育指导纲要（2012年修订）· 小学中高年级》人际交往——树立集体意识，善于与同学、老师交往，培养开朗、合群、自立的健康人格；引导学生在学习生活中感受解决困难的快乐，学会体验情绪并表达自己的情绪。",
    "hero_question": "想加入别人的游戏，却被一句「人够了」挡回来，这时候可以怎么办？",
    "hero_alt": "同伴交往与解决困难知识结构图：想加入怎么办、闹别扭怎么办、解决不了怎么求助 三栏",
    "hero_caption": "同伴交往与解决困难：看一看问一句试一试 · 闹别扭四步 · 求助不是打小报告",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "想加入别人的游戏，被拒绝了怎么办？", "d": "站在旁边不敢开口，或者被一句人够了挡回来", "v": "想加入别人的游戏被拒绝了怎么办"},
        {"t": "和好朋友闹别扭了，怎么和好？", "d": "两天不说话，谁都不肯先开口", "v": "和好朋友闹别扭了怎么和好"},
        {"t": "有人给我起外号，我可以怎么回应？", "d": "一叫大家就笑，心里挺难受", "v": "有人给我起外号我可以怎么回应"},
        {"t": "什么时候该找老师帮忙，什么时候自己先试试？", "d": "想请人帮忙，又怕被说打小报告", "v": "什么时候该找老师帮忙什么时候自己先试试"},
    ],
    "objectives": [
        "能说出三种常见的交友困境：想加入被拒绝、和好朋友闹别扭、被起了不喜欢的称呼",
        "想加入同伴活动时，会用「看一看、问一句、试一试」三步，并知道被拒绝不等于自己不好",
        "和同伴闹别扭后，能说出自己的感受，并提出一个具体可行的和好办法",
        "能分辨正当求助和打小报告，知道有人受伤或自己试过还是不行时，可以找可信任的大人帮忙",
    ],
    "objectives_plain": [
        "能说出三种常见的交友困境：想加入被拒绝、和好朋友闹别扭、被起了不喜欢的称呼",
        "想加入同伴活动时，会用「看一看、问一句、试一试」三步，并知道被拒绝不等于自己不好",
        "和同伴闹别扭后，能说出自己的感受，并提出一个具体可行的和好办法",
        "能分辨正当求助和打小报告，知道有人受伤或自己试过还是不行时，可以找可信任的大人帮忙",
    ],
    "standards": [
        {"content": "树立集体意识，善于与同学、老师交往，培养开朗、合群、自立的健康人格",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学中高年级 · 人际交往"},
        {"content": "引导学生在学习生活中感受解决困难的快乐，学会体验情绪并表达自己的情绪",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学中高年级 · 人际交往"},
    ],
    "prereqs": ["psych-e-g3-social-role"],
    "prereqs_name": "角色意识与时间管理",
    "prereqs_meta": "psych-e-g3-social-role",
    "leads_to": ["psych-e-g4-study-motivation"],
    "next_meta": "psych-e-g4-study-motivation",
    "section_images": ["assets/psych-e-g4-peer-relation-fig1.webp", "assets/psych-e-g4-peer-relation-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "站在旁边不敢开口、闹别扭两天不说话——这节课聊的就是这些事，并且教你怎么求助不丢脸。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能说出自己遇上的是哪一种困境，还知道下一步做什么。",
        "objectives": "看清四件事：说出三种困境、学会加入的三步、闹别扭后怎么说开、分辨求助和打小报告。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "想加入不是硬闯：看一看、问一句、试一试。被拒绝，不等于我不好。",
        "lab-1": "重点看「对方会有什么反应」：同一个情境，做法不同，接下来发生的事会很不一样。",
        "module-2": "闹别扭四步：停一停、说感受、听对方说、想个下次的办法。求助不是打小报告。",
        "lab-2": "放不下的时候问三句：有没有人受伤？我自己试过了吗？我说的是事实吗？",
        "worked-example": "小禾三步：先看一看发现有人手酸、再问一句我来摇绳、然后试一试——他换了一个能进去的位置。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "三栏各选一条，拼成你自己的交友小名片，再念给同桌听一遍。",
        "posttest": "出现了小组分工、新同学、有人让你别跟谁玩，看看你能不能用上今天的办法。",
        "summary": "三句话：加入走三步、闹别扭走四步、需要帮忙就开口。",
        "homework": "三层小任务，先做前两层，第三层可以请家里人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先帮你找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学心理健康「人际交往」在四年级的空缺，正对课标「树立集体意识，善于与同学、老师交往」「引导学生在学习生活中感受解决困难的快乐，学会体验情绪并表达自己的情绪」。四年级学生的难点不在「要不要和同伴好」，而在三个具体卡点上：①想加入却不知道从哪儿进去，被拒绝一次就归因到自己身上；②闹别扭后只有「等对方先开口」和「干脆不理」两种做法；③想请人帮忙又怕被说打小报告，于是硬扛。所以全课围绕三种真实交友困境展开：概念一把「加入」拆成可练习的看一看、问一句、试一试；概念二把「说开」拆成四步，并用「有没有人受伤、我自己试过了吗、我说的是事实吗」三问把正当求助和打小报告区分开。两个互动台子都能真的操作：交友小教练（五个情境 × 三个做法，选完展开对方可能的反应与后果，错误反馈一律写成「这样可能会……，还可以试试……」）、求助分类台（八张小事卡放进三个框）。综合任务把三条做法拼成个人化的「交友小名片」。全课语气温和、不评判、不贴标签，只讲可操作的相处办法，不涉及伤害性情节；插图一律为中性简洁的教学插画，不使用真实儿童照片风格人像。",
    "plan_table": """| 1 | cover | 同伴交往与解决困难 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 想加入，先做三步小准备 | 承·概念一（加入同伴活动） |
| 6 | interactive | 动手一：交友小教练，看一看会发生什么 | 承·情境模拟（做法 → 对方的反应与后果） |
| 7 | concept | 闹别扭以后怎么说开；求助不是打小报告 | 承·概念二（说开四步 + 求助边界） |
| 8 | interactive | 动手二：求助，还是打小报告？ | 承·边界辨析（八张小事卡分三类） |
| 9 | concept | 例题示范：小禾想加入跳绳，被说人够了 | 转·重难点突破（三步示范 + 纠错） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：写一张属于你的交友小名片 | 合·迁移应用（三栏拼句） |
| 12 | quiz | 后测：换三个新情境，办法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，讲清同伴交往这件事 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化辅导 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：想加入怎么办 / 闹别扭怎么办 / 解决不了怎么求助 三栏\n- P5 加入同伴活动三步示意图（已生成）：看一看、问一句、试一试，附中文标注\n- P7 求助判断三问示意图（已生成）：有没有人受伤、我自己试过了吗、我说的是事实吗，附中文标注\n- 三张图均为中性简洁教学插画，人物只用简单图形，不使用任何真实儿童照片或可识别肖像\n- 若需补充：班级「和解角」实景照片（需学校提供并授权后使用）",
}
