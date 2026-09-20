# -*- coding: utf-8 -*-
"""小学心理健康 · 面对挫折与情绪调节（G5）—— 补齐知识树「情绪调适」空缺

学科语气（心理健康）：温和、不评判、不贴标签；严禁临床诊断词汇；不涉及自伤自杀；插图一律中性简洁插画。
五年级落点：一件没做好的事（比赛输了 / 考砸了 / 被选掉了）——
  ① 先分清「哪些是我能改变的、哪些不是」；
  ② 再给每个「能改变的」配一个今天就能做的具体做法；
  ③ 同时辨析「都怪自己」与「都怪别人」两种极端归因，练习站得住的说法。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/psych-e-g5-negative-emotion-fig1.webp'
F2 = './assets/psych-e-g5-negative-emotion-fig2.webp'

TTS = {
    "hero": "五年级的同学，先想一想：一次比赛输了，或者一次考试没考好，心里那句话是不是马上就来了——我太差劲了，或者都怪别人。这节课我们练两件很有用的事。第一件，把一件没做好的事分成两堆：哪些是我能改变的，哪些是我改变不了的。第二件，给每一个能改变的，配一个今天就能做的具体做法。你会发现，名次不一定马上变，可你手里多了一份能动手的清单。",
    "problem-anchor": "开始之前，先选一个你最想知道的事。是想知道没做好的时候，怎么分清哪些是我能改变的，还是想知道为什么不能都怪自己、也不能都怪别人，或者你最想问的是，每件事都怪我是不是不太公平，再或者你想弄清楚，给能改变的事配一个具体做法到底长什么样。选好了，就带着它往下看。",
    "objectives": "这节课有四个小目标。第一，能说出一件事没做好之后，最先要分清的是能改变的和不能改变的。第二，能把一件具体的事分成我能改变的和我改变不了的两堆。第三，能给每一个能改变的事配上一个今天就能做的具体做法。第四，能分辨都怪自己和都怪别人这两种极端说法，说出更站得住的说法。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先说第一件事。一件事没做好，心里马上会冒出两样东西：一样是这件事里发生了什么，另一样是我心里对它的一句话。这句话常常不是事实，而是一个结论，比如我完了、我永远不行。所以第一步，先把事情说清楚，别急着给自己下结论。第二步，把这件事里的一条条小卡片拿出来，分成两堆：一堆是我能改变的，一堆是我改变不了的。这两堆分清楚了，心里的路就出来了。",
    "lab-1": "现在请你当一次分类员。下面有八张小卡片，都是比赛输了这件事里的东西。点一张卡片，再点上面两栏中的一个。分得不太合适也不会说你错，我会告诉你为什么，还可以换一栏再试试。分完之后你会发现，左边那一栏里，全都是可以动手的地方。",
    "module-2": "第二件事：别让归因走两个极端。一种是都怪自己，一件没做好的事被说成我这个人的问题，心里越来越沉。另一种是都怪别人，事情全推出去，自己一点办法也没有，下一次还是老样子。站得住的说法在中间：这件事我没做好，其中这几样有我的原因，我可以改；另外几样不是我能决定的，我先放一放。归因不等于认罪，也不等于甩手，它只是把责任放回合适的位置。",
    "lab-2": "现在请你当一次说法调整员。下面有四种说法，两种是都怪自己，两种是都怪别人。点开一句，你会看到三种改写，选一个更站得住的。选得不太合适也不会批评你，我会告诉你这样可能会发生什么，还可以试试什么。",
    "worked-example": "我们一起帮小舟想一想。班里的接力赛，小舟那一棒掉了棒，班里的名次一下就下来了。回教室的路上，他心里那句话特别重——都怪我，我怎么这么笨。我们陪他走四步。第一步，把事实说清楚：交接的时候，两个人的手没有对好，棒掉了。第二步，分成两堆：能改变的，是交接的动作和练习的次数；不能改变的，是当时的风、别的班跑得多快。第三步，把归因放回中间：这件事有我的原因，也有我们配合的原因，不等于我这个人笨。第四步，给能改变的配做法：今天中午和搭档练十次交接，每次只练出手的时机。走完四步，他手里有了一份清单。",
    "conceptest-1": "接下来用三个说法考考你，每一个里面都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件大事交给你。先选一件你最近没做好的事，把里面的小卡片分到两栏；再给每一个能改变的卡片，挑一个具体做法。分完、配完，你会得到一份自己的下一步清单。",
    "posttest": "最后一轮，换三个新的小情境来考考你。这次会出现考砸了、被选掉了，还有排练时被换下来，看看你能不能分清能改变的和不能改变的，并且给能改变的那一堆配一个做法。",
    "summary": "这节课我们记住三句话。第一句，一件事没做好，先把事情说清楚，别急着给自己下结论。第二句，把事情里的小卡片分成两堆：我能改变的，和我改变不了的。第三句，给每一个能改变的配一个今天就能做的具体做法，不要只说下次努力。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出三件你没做好的事，每件事分出两条能改变的、两条不能改变的。第二层能力应用，动手做：挑其中一件事，给每一个能改变的事配一个今天就能做的具体做法，写得越具体越好。第三层迁移挑战，选做：这一周里用一次四步法，记下当时的两种极端说法和你改过来以后的说法，写三个句子。",
    "knowledge-graph": "这张图展示了这节课在心理健康知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 先分清能改变的和不能改变的", "lab-1": "动手一 分一分：能改变 / 不能改变",
    "module-2": "概念二 别让归因走两个极端", "lab-2": "动手二 归因改写台",
    "worked-example": "例题讲解 小舟的接力棒", "conceptest-1": "概念测试",
    "synthesis": "综合任务 从一件事到我的下一步清单", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：分一分「能改变 / 不能改变」（八张卡片，比赛输了这件事） ──
CASE_BINS = [
    {"id": "ctl", "name": "① 我能改变的"},
    {"id": "uctl", "name": "② 我改变不了的"},
]

CASES = [
    {"id": "c1", "bin": "ctl", "t": "赛前我练了多少次",
     "fb": "这一条在我手里。练的次数，是今天就能加上去的。"},
    {"id": "c2", "bin": "uctl", "t": "抽签抽到哪一组",
     "fb": "抽签是当场决定的，我改变不了。能改变的是抽到谁之后我怎么打。"},
    {"id": "c3", "bin": "ctl", "t": "上场前我有没有把动作在脑子里走一遍",
     "fb": "这一条在我手里。走一遍只要一分钟，却是今天就能做的事。"},
    {"id": "c4", "bin": "uctl", "t": "那天场地的风和天气",
     "fb": "天气不归我管。能改变的是我上场前多做几次热身，让身体先热起来。"},
    {"id": "c5", "bin": "ctl", "t": "我不会的时候有没有去问人",
     "fb": "开口问是我能决定的，这一条今天就能用上。"},
    {"id": "c6", "bin": "uctl", "t": "对手那天发挥得特别好",
     "fb": "别人发挥成什么样，我改变不了。我能决定的是自己那一份练到什么程度。"},
    {"id": "c7", "bin": "ctl", "t": "我把最容易出错的那一段单独练了几遍",
     "fb": "把最容易错的地方挑出来单练，这是最能改变结果的一步。"},
    {"id": "c8", "bin": "uctl", "t": "班里最后排第几名",
     "fb": "名次是所有因素合起来的结果，不归任何一个人管。它后面自然跟着我能改变的那几条。"},
]

# ── 动手二：归因改写台（两种极端各两句） ──
ATTRIBS = [
    {"id": "a1", "kind": "都怪自己", "t": "都怪我，我怎么这么笨。",
     "opts": [
         {"t": "那一棒交接我没做好，交接的动作我还没练熟。今天中午我和搭档练十次。", "ok": True,
          "fb": "这句话把「一件事」和「我这个人」分开了，后面还跟着一个今天就能做的动作。"},
         {"t": "我天生就不适合跑接力，以后别让我上场了。", "ok": False,
          "fb": "这样可能会让你少掉很多练习的机会。还可以试试：把「天生」换成「还没」——「交接的动作我还没练熟」，再说出第一步。"},
         {"t": "都怪搭档的手伸得太低，跟我没关系。", "ok": False,
          "fb": "这是往另一个极端走了。还可以试试：说出自己在里面的那一部分——「交接时我出手早了一点，下次等半秒」。"},
     ]},
    {"id": "a2", "kind": "都怪自己", "t": "都是我不好，全班的名次都被我拖下去了。",
     "opts": [
         {"t": "我的那一棒掉了，这件事有我的原因。我把交接练好，下一场我还能帮上忙。", "ok": True,
          "fb": "先承认自己有原因，再立刻回到能做的事上——这就是站得住的说法。"},
         {"t": "我就是全班的累赘，说什么都没用。", "ok": False,
          "fb": "这样可能会把一次没做好，变成一句关于自己的结论，心里会越来越沉。还可以试试：只说自己那一棒，别给自己下结论。"},
         {"t": "要不是跑道太滑，怎么会掉棒，跟我一点关系都没有。", "ok": False,
          "fb": "跑道是因素之一，但不是全部。还可以试试：把两样都放进来——「交接没对好有我的原因，跑道也有点影响」。"},
     ]},
    {"id": "a3", "kind": "都怪别人", "t": "都怪老师，这道题他根本没讲过。",
     "opts": [
         {"t": "这道题的方法我还没弄懂。今天下课我去问老师，把第一步问清楚。", "ok": True,
          "fb": "把「怪谁」换成「我卡在哪一步、我下一步问什么」，手里就有事可做了。"},
         {"t": "老师讲得那么差，我学不好很正常。", "ok": False,
          "fb": "这样可能会让你一直等别人改变，自己却停在原地。还可以试试：今天先只做一件事——把不懂的第一步圈出来，明天去问。"},
         {"t": "都怪我太笨，老师讲了我也不懂。", "ok": False,
          "fb": "这是从怪别人滑到了怪自己，两个极端都不站得住。还可以试试：只说这道题的哪一步没懂，再定一个问的方法。"},
     ]},
    {"id": "a4", "kind": "都怪别人", "t": "都怪妈妈，她昨天没帮我检查作业。",
     "opts": [
         {"t": "作业是我自己的事。今天写完我先自己检查一遍，把不确定的题圈出来再问。", "ok": True,
          "fb": "把责任放回自己能管的那一格，也没有责怪谁——这句话说完整个人是往前走的。"},
         {"t": "妈妈都不管我，我考不好是应该的。", "ok": False,
          "fb": "这样可能会让下一次还是同一个结果，而且心里会多一层委屈。还可以试试：说出你今晚能做的一件事——自己先检查一遍。"},
         {"t": "我这个人做什么都不行，连作业都出错。", "ok": False,
          "fb": "这是从怪别人滑到了怪自己。还可以试试：只讲这道题——「这道题的方法我还没弄懂，我明天问一下。」"},
     ]},
]

# ── 综合任务：一件没做好的事 → 两栏 → 给能改变的配做法 ──
SCENARIOS = [
    {"id": "match", "name": "比赛输了",
     "cards": [
         {"id": "m1", "bin": "ctl", "t": "赛前我练了多少次",
          "fb": "练的次数在我手里，今天就能加上去。",
          "acts": ["把每天练的时间写进计划表，照着练二十分钟",
                   "把最容易出错的动作单独练十次",
                   "请老师看我练一遍，指出一处要改的地方"]},
         {"id": "m2", "bin": "uctl", "t": "抽签抽到哪一组",
          "fb": "抽签当场决定，不归我管。", "acts": []},
         {"id": "m3", "bin": "ctl", "t": "上场前有没有把动作走一遍",
          "fb": "这一条由我决定，一分钟就能做。",
          "acts": ["上场前找一块安静的地方，把动作在脑子里走一遍",
                   "把三个关键动作写在手心里，上场前看一眼",
                   "和搭档对一句口令，一起上场"]},
         {"id": "m4", "bin": "uctl", "t": "当天的天气和场地",
          "fb": "天气和场地我改变不了，能改变的是我提前热身。", "acts": []},
         {"id": "m5", "bin": "ctl", "t": "紧张的时候有没有做几次呼吸",
          "fb": "呼吸是我能控制的开关，随时可以用。",
          "acts": ["上场前做三次慢慢的长呼吸",
                   "轮到我之前，把手放在肚子上数四下",
                   "心里说一句：先做好第一个动作就行"]},
         {"id": "m6", "bin": "uctl", "t": "对手那天发挥得怎么样",
          "fb": "别人的发挥不归我管，我只需管好自己那一份。", "acts": []},
     ]},
    {"id": "exam", "name": "考砸了",
     "cards": [
         {"id": "e1", "bin": "ctl", "t": "考前我复习了哪几个单元",
          "fb": "复习的范围由我决定。",
          "acts": ["把这次考的单元列出来，一个一个打勾",
                   "每天复习一个单元，只做五道题",
                   "把最容易混的两个概念写在一张卡片上，每天看一遍"]},
         {"id": "e2", "bin": "uctl", "t": "这次卷子的难度",
          "fb": "卷子难不难，出题的人决定，我改变不了。", "acts": []},
         {"id": "e3", "bin": "ctl", "t": "不懂的时候有没有去问",
          "fb": "开口问是我能决定的。",
          "acts": ["把不懂的那一步圈出来，明天课间问老师",
                   "先问同桌一遍，再自己讲给他听",
                   "把问题写在小纸条上，攒够三个一起去问"]},
         {"id": "e4", "bin": "uctl", "t": "别人考了多少分",
          "fb": "别人的分数不归我管，也不说明我的下一步。", "acts": []},
         {"id": "e5", "bin": "ctl", "t": "错题有没有再想一遍",
          "fb": "错题是我能处理的地方，这是提分最快的一步。",
          "acts": ["把三道错题抄进错题本，每道写一句错在哪",
                   "过两天遮住答案，把这三道题再做一遍",
                   "给每道错题配一个提醒词，写在题旁边"]},
         {"id": "e6", "bin": "uctl", "t": "考试那天身体舒不舒服",
          "fb": "身体状态不总能由我决定，能改变的是考前早点睡。", "acts": []},
     ]},
    {"id": "pick", "name": "被选掉了",
     "cards": [
         {"id": "p1", "bin": "ctl", "t": "报名前我准备了哪些材料",
          "fb": "准备到什么程度，是我能决定的。",
          "acts": ["把要交的材料列成一张清单，交之前逐个打勾",
                   "提前两天把要说的话写下来，念一遍",
                   "请一个人帮我听一遍，记下他听不懂的地方"]},
         {"id": "p2", "bin": "uctl", "t": "一共有多少人报名",
          "fb": "报名人数不归我管，我改变不了。", "acts": []},
         {"id": "p3", "bin": "ctl", "t": "我有没有提前练过要说的话",
          "fb": "练几遍由我决定，练一遍就有一遍的效果。",
          "acts": ["对着镜子说一遍，只看自己的手势",
                   "说给同桌一个人听，请他指出一处要改的",
                   "掐着时间练一遍，看看会不会超时"]},
         {"id": "p4", "bin": "uctl", "t": "评委老师喜欢哪一种风格",
          "fb": "评委的偏好我猜不准，也不归我管。", "acts": []},
         {"id": "p5", "bin": "ctl", "t": "落选之后有没有去问问可以改哪里",
          "fb": "去问一句是我能决定的，而且下一次用得上。",
          "acts": ["找老师问一句：我哪一部分可以再改改",
                   "请老师指出一个最值得先改的地方",
                   "把问到的意见写在纸上，下一次照着改"]},
         {"id": "p6", "bin": "uctl", "t": "这次名额有几个",
          "fb": "名额多少不归我管，我改变不了。", "acts": []},
     ]},
]

CUSTOM_JS = r"""
/* ============================================================
   psych-e-g5-negative-emotion 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 分一分：能改变 / 不能改变（八张卡片两栏分类）
   3) 归因改写台：都怪自己 / 都怪别人 → 站得住的说法
   4) 综合任务：一件没做好的事 → 两栏 → 给能改变的配做法 → 生成下一步清单
   ============================================================ */
(function () {
  'use strict';

  /* ---------- 1. 选择题接线 ---------- */
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

  /* ---------- 2. 分一分：能改变 / 不能改变 ---------- */
  var CASES = __CASES_JSON__;
  var BINS = __BINS_JSON__;
  var bank = document.getElementById('ctl-bank');
  if (bank && CASES.length) {
    var placedC = {}, pickedC = null;
    var outC = document.getElementById('ctl-out');
    var scoreC = document.getElementById('ctl-score');

    function caseById(id) {
      for (var i = 0; i < CASES.length; i++) { if (CASES[i].id === id) return CASES[i]; }
      return null;
    }
    function binName(id) {
      for (var i = 0; i < BINS.length; i++) {
        if (BINS[i].id === id) return BINS[i].name.replace(/^[①②]\s*/, '');
      }
      return '';
    }
    CASES.forEach(function (it) {
      var b = document.createElement('button');
      b.className = 'sort-item';
      b.dataset.card = it.id;
      b.textContent = it.t;
      b.addEventListener('click', function () {
        if (placedC[it.id]) return;
        pickedC = it.id;
        document.querySelectorAll('[data-card]').forEach(function (x) {
          x.classList.toggle('selected', x.dataset.card === pickedC);
        });
        outC.className = 'result warn';
        outC.innerHTML = '<strong>你选中了：</strong>' + it.t + '<br>它属于哪一栏？点一下上面两栏中的一个。';
      });
      bank.appendChild(b);
    });
    BINS.forEach(function (bn) {
      var box = document.getElementById('ctl-bin-' + bn.id);
      if (!box) return;
      box.addEventListener('click', function () {
        if (!pickedC) {
          outC.className = 'result warn';
          outC.textContent = '先在左边点一张卡片，再点这一栏。';
          return;
        }
        var it = caseById(pickedC);
        if (!it || placedC[it.id]) return;
        if (it.bin !== bn.id) {
          outC.className = 'result warn';
          outC.innerHTML = '<strong>这一条再想一想。</strong>' + it.fb +
            '<br>它更合适放在「' + binName(it.bin) + '」那一栏，换一栏再点一次试试。';
          return;
        }
        placedC[it.id] = true;
        var card = document.querySelector('[data-card="' + it.id + '"]');
        if (card) { card.classList.add('done'); card.classList.remove('selected'); }
        var tag = document.createElement('span');
        tag.className = 'tag';
        tag.textContent = it.t;
        box.querySelector('.bin-list').appendChild(tag);
        box.classList.add('ok');
        pickedC = null;
        var n = Object.keys(placedC).length;
        scoreC.textContent = '已经分好 ' + n + ' / ' + CASES.length + ' 张';
        outC.className = 'result';
        outC.innerHTML = '<strong>分对了。</strong>' + it.fb;
        if (n === CASES.length) {
          outC.className = 'result';
          outC.innerHTML = '<strong>八张卡片都分好了。</strong>左边那一栏里，全都是能动手的地方；' +
            '右边那一栏，先放在一边，不用替它们使劲。<br>记住这个顺序：<strong>先分清，再决定做哪一件</strong>。';
        }
      });
    });
    scoreC.textContent = '已经分好 0 / ' + CASES.length + ' 张';
  }

  /* ---------- 3. 归因改写台 ---------- */
  var ATT = __ATT_JSON__;
  var stageA = document.getElementById('att-stage');
  if (stageA && ATT.length) {
    var curA = null, doneA = {};
    var outA = document.getElementById('att-out');
    var scoreA = document.getElementById('att-score');

    function attById(id) {
      for (var i = 0; i < ATT.length; i++) { if (ATT[i].id === id) return ATT[i]; }
      return null;
    }
    function renderA() {
      document.querySelectorAll('[data-att]').forEach(function (b) {
        var k = b.dataset.att;
        b.classList.toggle('selected', k === curA);
        b.classList.toggle('done', !!doneA[k]);
      });
      scoreA.textContent = '已经改写 ' + Object.keys(doneA).length + ' / ' + ATT.length + ' 句';
    }
    function paintA() {
      var box = document.getElementById('att-opts');
      box.innerHTML = '';
      if (!curA) return;
      var S = attById(curA);
      if (!S) return;
      var head = document.createElement('p');
      head.style.cssText = 'margin:0 0 8px;color:var(--muted);font-size:14px';
      head.textContent = '这一句是哪一种极端：' + S.kind;
      box.appendChild(head);
      S.opts.forEach(function (o) {
        var b = document.createElement('button');
        b.className = 'choice' + (doneA[curA] && o.ok ? ' correct' : '');
        b.style.textAlign = 'left';
        b.textContent = o.t;
        b.addEventListener('click', function () {
          if (doneA[curA]) return;
          if (o.ok) {
            doneA[curA] = true;
            outA.className = 'result';
            outA.innerHTML = '<strong>这一句站得住。</strong>' + o.fb;
          } else {
            outA.className = 'result warn';
            outA.innerHTML = '<strong>这句话很多人心里都冒出来过，我们看看它会带来什么。</strong>' + o.fb;
          }
          renderA();
          paintA();
        });
        box.appendChild(b);
      });
    }
    document.querySelectorAll('[data-att]').forEach(function (b) {
      b.addEventListener('click', function () {
        curA = b.dataset.att;
        var S = attById(curA);
        if (doneA[curA]) {
          outA.className = 'result';
          outA.innerHTML = '<strong>这一句已经改写过了。</strong>记住这个句式：这件事有我的原因，也有别的因素；能改的那几样，我下一步做什么。';
        } else {
          outA.className = 'result warn';
          outA.innerHTML = '<strong>心里冒出来的是：「' + S.t + '」</strong><br>下面有三种改写，选一个更站得住的试试。';
        }
        renderA();
        paintA();
      });
    });
    renderA();
  }

  /* ---------- 4. 综合任务：我的下一步清单 ---------- */
  var SCEN = __SCEN_JSON__;
  var sBank = document.getElementById('syn-bank');
  if (sBank && SCEN.length) {
    var curS = null, sPlaced = {}, sActs = {}, sPicked = null;
    var sOut = document.getElementById('syn-out');
    var sScore = document.getElementById('syn-score');
    var sGenerated = document.getElementById('syn-card-out');

    function scById(id) {
      for (var i = 0; i < SCEN.length; i++) { if (SCEN[i].id === id) return SCEN[i]; }
      return null;
    }
    function cardList() { var s = scById(curS); return s ? s.cards : []; }
    function cardById(id) {
      var cs = cardList();
      for (var i = 0; i < cs.length; i++) { if (cs[i].id === id) return cs[i]; }
      return null;
    }
    function scName(id) { var s = scById(id); return s ? s.name : ''; }

    function renderBank() {
      sBank.innerHTML = '';
      cardList().forEach(function (it) {
        var b = document.createElement('button');
        b.className = 'sort-item' + (sPlaced[it.id] ? ' done' : '') + (sPicked === it.id ? ' selected' : '');
        b.dataset.scard = it.id;
        b.textContent = it.t;
        b.addEventListener('click', function () {
          if (sPlaced[it.id]) return;
          sPicked = it.id;
          renderBank();
          sOut.className = 'result warn';
          sOut.innerHTML = '<strong>你选中了：</strong>' + it.t + '<br>它属于哪一栏？点一下下面两栏中的一个。';
        });
        sBank.appendChild(b);
      });
    }
    function renderBins() {
      var listCtl = document.getElementById('syn-list-ctl');
      var listUctl = document.getElementById('syn-list-uctl');
      if (!listCtl || !listUctl) return;
      listCtl.innerHTML = '';
      listUctl.innerHTML = '';
      cardList().forEach(function (it) {
        if (!sPlaced[it.id]) return;
        var list = (it.bin === 'ctl') ? listCtl : listUctl;
        var row = document.createElement('div');
        row.style.cssText = 'margin:8px 0';
        var t = document.createElement('div');
        t.style.cssText = 'font-size:14px';
        t.innerHTML = '✓ ' + it.t;
        row.appendChild(t);
        if (it.bin === 'ctl') {
          var lab = document.createElement('div');
          lab.style.cssText = 'font-size:13px;color:var(--muted);margin:6px 0 4px';
          lab.textContent = '给它配一个今天就能做的具体做法：';
          row.appendChild(lab);
          (it.acts || []).forEach(function (a) {
            var chip = document.createElement('button');
            chip.className = 'choice' + (sActs[it.id] === a ? ' selected' : '');
            chip.style.cssText = 'text-align:left;font-size:14px;padding:10px 12px;margin:4px 0';
            chip.textContent = a;
            chip.addEventListener('click', function (ev) {
              ev.stopPropagation();
              sActs[it.id] = a;
              renderBins();
              sOut.className = 'result';
              sOut.innerHTML = '<strong>配好了一条做法。</strong>「' + it.t + '」→ ' + a;
            });
            row.appendChild(chip);
          });
        }
        list.appendChild(row);
      });
    }
    function renderProgress() {
      var cs = cardList();
      var n = 0;
      cs.forEach(function (it) { if (sPlaced[it.id]) n++; });
      sScore.textContent = '已经分好 ' + n + ' / ' + cs.length + ' 张';
    }

    document.querySelectorAll('[data-scen]').forEach(function (b) {
      b.addEventListener('click', function () {
        curS = b.dataset.scen;
        sPlaced = {}; sActs = {}; sPicked = null;
        document.querySelectorAll('[data-scen]').forEach(function (x) {
          x.classList.toggle('selected', x === b);
        });
        renderBank();
        renderBins();
        renderProgress();
        if (sGenerated) sGenerated.innerHTML = '';
        sOut.className = 'result warn';
        sOut.innerHTML = '<strong>场景选好了：' + scName(curS) + '。</strong>先在左边点一张卡片，再点下面两栏中的一个。';
      });
    });

    [['ctl', 'syn-bin-ctl'], ['uctl', 'syn-bin-uctl']].forEach(function (pair) {
      var box = document.getElementById(pair[1]);
      if (!box) return;
      box.addEventListener('click', function () {
        if (!curS) {
          sOut.className = 'result warn';
          sOut.textContent = '先在第一步选一个场景。';
          return;
        }
        if (!sPicked) {
          sOut.className = 'result warn';
          sOut.textContent = '先在左边点一张卡片，再点这一栏。';
          return;
        }
        var it = cardById(sPicked);
        if (!it || sPlaced[it.id]) return;
        if (it.bin !== pair[0]) {
          sOut.className = 'result warn';
          sOut.innerHTML = '<strong>这一条再想一想。</strong>' + it.fb + ' 换一栏再点一次试试。';
          return;
        }
        sPlaced[it.id] = 'ok';
        sPicked = null;
        renderBank();
        renderBins();
        renderProgress();
        sOut.className = 'result';
        sOut.innerHTML = '<strong>分对了。</strong>' + it.fb;
        var cs = cardList(), n = 0;
        cs.forEach(function (x) { if (sPlaced[x.id]) n++; });
        if (n === cs.length) {
          sOut.className = 'result';
          sOut.innerHTML = '<strong>卡片都分好了。</strong>左边那一栏每一张，都可以配一个具体做法；' +
            '配完点下面的按钮，生成你自己的下一步清单。';
        }
      });
    });

    var genBtn = document.getElementById('syn-gen');
    if (genBtn) {
      genBtn.addEventListener('click', function () {
        if (!curS) {
          sOut.className = 'result warn';
          sOut.textContent = '先在第一步选一个场景。';
          return;
        }
        var cs = cardList(), lines = [], miss = 0;
        cs.forEach(function (it) {
          if (it.bin !== 'ctl') return;
          if (sActs[it.id]) {
            lines.push('· ' + it.t + ' → ' + sActs[it.id]);
          } else {
            miss++;
            lines.push('· ' + it.t + ' → 还没配做法，想一想今天能做的第一步。');
          }
        });
        sOut.className = 'result';
        sOut.innerHTML = '<strong>我的下一步清单（' + scName(curS) + '）：</strong><br>' + lines.join('<br>') +
          (miss ? '<br>还有 ' + miss + ' 条没配做法，配完整就是一份完整的清单。'
                : '<br>每一条都有具体做法了，今天就能从第一条开始。');
        if (sGenerated) {
          sGenerated.className = 'result';
          sGenerated.innerHTML = '<strong>清单已经写好了。</strong>把它抄在便签上，贴在书桌前；' +
            '右边那一栏不用管，它们本来就不归你管。';
        }
      });
    }
    renderProgress();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__CASES_JSON__', json.dumps(CASES, ensure_ascii=False))
             .replace('__BINS_JSON__', json.dumps(CASE_BINS, ensure_ascii=False))
             .replace('__ATT_JSON__', json.dumps(ATTRIBS, ensure_ascii=False))
             .replace('__SCEN_JSON__', json.dumps(SCENARIOS, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "比赛输了，回家路上你一直想「我怎么这么笨」。下面哪个做法更合适？",
         "options": [("先把事情说清楚：哪一棒没做好、当时发生了什么，再想我能改什么", True),
                     ("给自己下一个结论：我这个人就是不行", False),
                     ("大声说都怪别人，跟我没关系", False)],
         "explain": "先把「发生了什么」和「我心里那句话」分开，事情才有下手的地方。"
                    "<strong>错因提醒：</strong>常见错误是把「这一次没做好」误认为「我这个人不行」——前者是一件事，后者是一句结论。"},
        {"q": "下面哪一条属于「我能改变的」？",
         "options": [("把最容易错的那一段多练几遍", True),
                     ("抽签抽到哪一组对手", False),
                     ("那天场地的风和天气", False)],
         "explain": "能不能自己动手去做，是判断的分界线；练几遍由我决定，抽签和天气不由我决定。"
                    "<strong>错因提醒：</strong>最容易搞混的是把「别人发挥得好不好」也算进自己的清单——那一条不归你管，写进去只会白费力气。"},
        {"q": "考试没考好，心里很难受。下面哪句话更站得住？",
         "options": [("我这次有几道题没弄懂，我今天先把错题抄一遍", True),
                     ("都是我不好，我永远都考不好", False),
                     ("都怪老师没讲清楚，跟我没关系", False)],
         "explain": "站得住的说法在中间：承认有我的原因，同时回到今天能做的事上。"
                    "<strong>错因提醒：</strong>有人误认为「承认自己有原因就等于认罪」——归因只是把责任放到合适的位置，不是给自己判刑。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "「这件事没做好」之后，先分清能改变的和不能改变的", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们已经学过怎么给心里的感觉起名字，也知道难受的时候可以说出来（And）；可是一件事真的没做好，心里立刻冒出来的是「我太差了」，这句话一出口，人就沉下去了，什么也不想做（But）；所以这节课先练第一步——把事情说清楚，再把它分成「能改变的」和「不能改变的」两堆（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">一件事没做好，心里会同时冒出<strong>两样东西</strong>：这件事里发生了什么，和我心里对它的一句话。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>① 事情本身</strong></p>
            <p style="color:var(--muted)">可以核对的：第几棒掉了、哪道题空着、投票时差了几票。它像一张可以摊开来看的清单。</p>
          </div>
          <div class="inner-card">
            <p><strong>② 心里那句话</strong></p>
            <p style="color:var(--muted)">常常是一个结论：我完了、我永远不行、我就是笨。它不是事实，它是心里那一刻说出的一句话。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="一件事没做好之后的两步示意图：先说清事实，再分成能改变的和不能改变的两堆，附中文标注">
          <figcaption>示意图：第一步把事情说清楚，第二步把里面的小卡片分成「我能改变的」和「我改变不了的」（教学示意图，人物为中性简洁插画）</figcaption>
        </figure>
        <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(78,205,196,.45)">
          <p><strong>可以照着问自己的两句话：</strong></p>
          <p style="color:var(--muted)">第一句：<strong>这件事里，实际发生了什么？</strong>（只讲能看见的事）　第二句：<strong>哪几条我能动手改，哪几条我改不了？</strong>分完以后，只管左边那一堆。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「分清哪些不归我管，就是在给自己找借口」。这里最容易<strong>搞混</strong>的是两件事：找借口的句子说完就没有下文；分清责任的句子说完，后面一定跟着一件我能做的事。判断的办法还是那一句——<strong>这句话后面有没有一个能动手的做法？</strong>有，就不是借口。</p>
        </div>
{insight_box([
    {"lens": "拆开它", "text": "一件事可以拆成一条条小卡片。卡片越多越小，能动手的地方就越清楚；只留下一句「我就是不行」，那就只剩下沉。"},
    {"lens": "比较它", "text": "「我要把它做好」和「我只能做好」是两句不同的话。前者留着一个能改的空间，后者把结果提前写死了。"},
    {"lens": "迁移它", "text": "不只是比赛和考试。和同学闹别扭、排练被换下来、家里有事，都可以先分两堆，再去动左边那一堆。"},
])}
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>先说事实，再分两堆——<strong>能改的动手做，改不了的先放下。</strong></div></div>
    ''', tag="概念一"))

    case_bins = "\n".join(
        f'''            <div class="sort-bin" id="ctl-bin-{b["id"]}" role="button" tabindex="0">
              <h4>{b["name"]}</h4>
              <div class="bin-list"></div>
            </div>'''
        for b in CASE_BINS
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：分一分，哪些是我能改变的", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">八张卡片都来自「这次比赛输了」这件事。先在左边点一张，再点上面两栏中的一个。<strong>分得不太合适也不会说你错</strong>，我会告诉你为什么，还可以换一栏再试试。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 八张小卡片（点一张选中）</div>
          <div class="sort-bank" id="ctl-bank"></div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 它属于哪一栏</div>
          <div class="sort-bins">
{case_bins}
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">分类进度</span><span class="v" id="ctl-score">已经分好 0 / 8 张</span></div>
          </div>
          <p class="result warn" id="ctl-out" style="margin-top:12px">先在左边点一张卡片。</p>
        </div>
        <div class="inner-card" style="margin-top:14px">
          <p><strong>写一条你自己的：</strong></p>
          <p style="color:var(--muted)">想一想最近一件没做好的事，写下其中<strong>一条你能改变的</strong>。</p>
          <textarea id="ctl-answer" rows="2" placeholder="这件事里，我能改变的是……" style="margin-top:8px"></textarea>
        </div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "别让归因走两个极端：都怪自己，和都怪别人", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">事情没做好以后，我们心里会解释它为什么发生，这个解释<strong>叫做归因</strong>。归因很容易滑向两个极端。</p>
        <div class="grid grid-3">
          <div class="inner-card">
            <p><strong>极端一：都怪自己</strong></p>
            <p style="color:var(--muted)">一件没做好的事，被说成我这个人的问题。心里越来越沉，手也抬不起来。</p>
          </div>
          <div class="inner-card">
            <p><strong>极端二：都怪别人</strong></p>
            <p style="color:var(--muted)">事情全推出去，自己一点办法也没有。当下轻松一点，下次还是老样子。</p>
          </div>
          <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(78,205,196,.45)">
            <p><strong>站得住的说法</strong></p>
            <p style="color:var(--muted)">这件事没做好，其中这几样有我的原因，我可以改；另外几样不是我能决定的，我先放一放。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="都怪自己、都怪别人、站得住的说法三栏对照图，附中文标注">
          <figcaption>示意图：两种极端的归因，和中间那个站得住的说法（教学示意图，人物为中性简洁插画）</figcaption>
        </figure>
        <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(78,205,196,.45)">
          <p><strong>站得住的说法，长这个样子：</strong></p>
          <p style="color:var(--muted)">「这件事有我的原因」<strong>＋</strong>「也有别的因素」<strong>＋</strong>「能改的那几样，我下一步做（一件具体的小事）」。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「不怪自己就是不认真」。这里最容易<strong>搞混</strong>的是「有我的原因」和「全都是我的错」——前者是一句具体的话，后面跟着一个动作；后者是一句结论，说完整个人就动不了了。<strong>承认原因，不等于给自己判刑。</strong></p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "两个极端有一句共同的话：把「所有」都交给一个人。「全都怪我」和「全不怪我」，其实都只剩一个答案。"},
    {"lens": "解释它", "text": "为什么站得住的说法更有用？因为它把原因拆到能动手的位置上。原因一旦具体，下一步就跟着出现了。"},
    {"lens": "迁移它", "text": "和同伴闹别扭、被老师提醒、被家长说了一顿，都可以用一次三件套：有我的原因、也有别的因素、我下一步做什么。"},
])}
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>不都怪自己，也不都怪别人——<strong>有我的那份，我认；我认的那份，我做。</strong></div></div>
    ''', tag="概念二"))

    att_btns = "\n".join(
        f'            <button class="choice" data-att="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in ATTRIBS
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：归因改写台，把极端说法改一改", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">四种说法里，两种是「都怪自己」，两种是「都怪别人」。点开一句，再从三种改写里选一个更站得住的。<strong>选得不太合适也不会批评你</strong>。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 心里冒出来的那一句</div>
          <div class="grid" id="att-stage">
{att_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 换一种说法试试</div>
          <div class="grid" id="att-opts">
            <span style="color:var(--muted);font-size:14px">先在上面点一句，这里就会出现三种改写。</span>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">改写进度</span><span class="v" id="att-score">已经改写 0 / 4 句</span></div>
          </div>
          <p class="result warn" id="att-out" style="margin-top:12px">先点一句你自己也想过的话。</p>
        </div>
        <div class="inner-card" style="margin-top:14px">
          <p><strong>轮到你自己写一句：</strong></p>
          <p style="color:var(--muted)">最近有哪件事，你心里说过「都怪……」？把它改写成站得住的说法。</p>
          <textarea id="att-answer" rows="2" placeholder="这件事有我的原因……也有别的因素……我下一步可以……" style="margin-top:8px"></textarea>
        </div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小舟的接力棒", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>班里的接力赛，小舟跑最后一棒，交接的时候棒掉了。班里的名次一下退了好几名。回教室的路上，他心里那句话特别重——都怪我，我怎么这么笨。请你陪他走四步。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>把事实说清楚：</strong>交接的时候，我们两个人的手没有对好，棒掉在地上。只说能看见的事，不加结论。</div></div>
          <div class="step"><span class="n">2</span><div><strong>分成两堆：</strong>能改变的——交接的动作、我们俩练的次数、上场前有没有对好口令；不能改变的——当时的风、别的班跑得多快、裁判怎么判。</div></div>
          <div class="step"><span class="n">3</span><div><strong>把归因放回中间：</strong>这件事有我的原因，也有我们配合的原因。有我的原因，不等于我这个人笨。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>给能改变的配做法：</strong>今天中午和搭档练十次交接，每次只练一件事——出手的时机。走完四步，他手里有了一份清单。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「不难受了才算走出来了」，于是先等心情过去。小舟这四步里，心情并没有立刻变好，他确实还很难过。可是他把事实说清楚了，把能做的事挑了出来，还配了一个今天的动作。<strong>不是等难受走了才动手，而是带着难受先做一小步。</strong></p>
        </div>
        <div class="inner-card">
          <p><strong>说给同桌听：</strong>小舟这四步里，哪一步你自己已经做到了？哪一步还想再练一练？</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "关于「能改变的」和「不能改变的」，下面哪种理解更合适？",
         "options": [("分两栏是为了知道先动哪里，不是给自己找借口", True),
                     ("不能改变的那几条也要一直盯着，想办法补偿", False),
                     ("只要分清责任，名次就一定会变好", False)],
         "explain": "分两栏是为了把力气放在能动手的地方；右栏先放一放，不等于不管。"
                    "<strong>错因提醒：</strong>常见错误是误认为「分清了就一定会成功」——分清只是让下一步更清楚，结果还要看练习和时间。"},
        {"q": "下面哪句话属于「都怪别人」的极端说法？",
         "options": [("要不是跑道滑，我根本不会掉棒，跟我一点关系都没有", True),
                     ("交接没对好有我的原因，跑道也确实有点影响", False),
                     ("我那一棒没做好，我明天再练十次", False)],
         "explain": "「全都是别人的问题」和「全都是我的问题」是同一个毛病的两面：都只留一个答案。"
                    "<strong>错因提醒：</strong>有人误认为「不怪自己就是不认真」——承认有我的原因，和把一切都揽过来，是两件事。"},
        {"q": "「下次我一定努力」和「今天中午和搭档练十次交接」，哪一句更像一个具体的做法？",
         "options": [("第二句，因为它说清了做什么、什么时候做", True),
                     ("第一句，因为态度更坚决", False),
                     ("两句一样，都是表态", False)],
         "explain": "具体做法要能回答三个问题：做什么、什么时候做、做多少。答得上来，今天就能开始。"
                    "<strong>错因提醒：</strong>最容易搞混的是「决心」和「做法」——决心说的是心情，做法说的是动作。"}
    ], tag="概念测试"))

    scen_btns = "\n".join(
        f'            <button class="choice" data-scen="{s["id"]}" style="text-align:center">{s["name"]}</button>'
        for s in SCENARIOS
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：从一件没做好的事，到我的下一步清单", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先选一件你最近没做好的事，把里面的小卡片分到两栏；再给每一个能改变的卡片，挑一个具体做法；最后生成你的下一步清单。<strong>分得不太合适也不扣分</strong>，我会告诉你它更合适放在哪里。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 选一件没做好的事</div>
          <div class="grid grid-3">
{scen_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 把卡片分到两栏（点卡片，再点栏）</div>
          <div class="sort-bank" id="syn-bank"></div>
          <div class="sort-bins" style="margin-top:12px">
            <div class="sort-bin" id="syn-bin-ctl" role="button" tabindex="0">
              <h4>① 我能改变的</h4>
              <div class="bin-list" id="syn-list-ctl"></div>
            </div>
            <div class="sort-bin" id="syn-bin-uctl" role="button" tabindex="0">
              <h4>② 我改变不了的</h4>
              <div class="bin-list" id="syn-list-uctl"></div>
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">分类进度</span><span class="v" id="syn-score">已经分好 0 / 6 张</span></div>
          </div>
          <div class="flex-row">
            <button class="choice" id="syn-gen" style="text-align:center">③ 生成我的下一步清单</button>
          </div>
          <p class="result warn" id="syn-out" style="margin-top:12px">先在第一步选一个场景。</p>
          <p id="syn-card-out" style="margin-top:10px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💛</span><div><strong>别忘了右边那一栏：</strong>它不用配做法。把改不了的先放下，不是放弃，是把力气省下来用在左边。</div></div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换三个新情境，办法还在不在", TTS["posttest"], [
        {"q": "这次考试退步了十几名，你心里很不好受。下面哪个做法更合适？",
         "options": [("先把这次的事实写下来，再挑出三条能改变的，各配一个今天就能做的做法", True),
                     ("反复想「我怎么这么笨」，想到很晚", False),
                     ("对自己说：都怪题目太偏，反正跟我无关", False)],
         "explain": "把事实和自己那句话分开，再去动能改变的那一堆，这是最省力气的一条路。"
                    "<strong>错因提醒：</strong>有人误认为「想得越久越有收获」——只反复想那句结论，时间过去了，清单还是空的。"},
        {"q": "参加社团选拔，你被选掉了，心里有点失落。下面哪一条属于「我能改变的」？",
         "options": [("下一次报名前，把要说的话提前练三遍", True),
                     ("这次一共有多少人报名", False),
                     ("评委老师更喜欢哪一种风格", False)],
         "explain": "报名人数和评委偏好都不归你管；练三遍由你决定，而且是下次马上能用上的。"
                    "<strong>错因提醒：</strong>最容易搞混的是把「别人的选择」写进自己的清单——那一条写着，只会让你更无力。"},
        {"q": "排练时老师把你从原来的位置换了下来，你有点难过。下面哪句话更站得住？",
         "options": [("这次的位置换了，有我没练到位的原因。我去问问老师，我哪一部分可以先改", True),
                     ("老师就是看我不顺眼，怎么练都没用", False),
                     ("我什么角色都做不好，以后不参加了", False)],
         "explain": "一句话里既承认了自己的那一部分，也留了一个可以问、可以改的动作，这样的人不会停在原地。"
                    "<strong>错因提醒：</strong>常见错误是误认为「问一句就等于认输」——去问清楚哪里可以改，恰恰是手里最有用的那张牌。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，讲清面对挫折这件事", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>先说事实：</strong>一件事没做好，先讲清楚发生了什么，别急着给自己下一个「我不行」的结论。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>再分两堆：</strong>把事情里的小卡片分成「我能改变的」和「我改变不了的」，只管左边那一堆。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>配一个做法：</strong>给每一个能改变的配一个今天就能做的具体做法，说清做什么、什么时候做。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>还要记牢一件事：</strong>遇到没做好的事，心里难受、有点沉，是几乎每个人都会有的反应，这很正常。如果有一段时间你一直打不起精神、上课也听不进去，把这件事说给老师或者爸爸妈妈听，是很聪明的做法。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「事实、两堆、一个做法」这三个词，说清楚你上一次没做好的经过。</p>
          <p style="color:var(--muted)">再动一动手：<strong>画出</strong>你的两栏清单，左边写三条能改变的，各配一个做法；右边写两条改不了的，画一个框把它们先圈起来。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写出三件你没做好的事，每件事分出两条「能改变的」、两条「不能改变的」。",
            "说出「都怪自己」和「都怪别人」这两种说法，各自会带来什么。",
            "把「我下次一定努力」改写成一句具体做法：做什么、什么时候做、做多少。",
        ],
        [
            "挑其中一件事，给每一个能改变的事配一个今天就能做的具体做法，做成一张两栏清单。",
            "记录一次：心里那句话冒出来的时候，你做了什么，后来事情有没有往前走一点。",
        ],
        [
            "这一周里用一次四步法：事实、两堆、中间的说法、一个做法。做完写三句话：当时的想法、改过来的说法、你的下一步。",
            "和同桌一起想一想：我们班里还有哪些说法，能把「都怪别人」改得更站得住？写两条。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "psych-e-g5-negative-emotion",
    "node_id": "psych-e-g5-negative-emotion",
    "subject": "psychology",
    "subject_cn": "心理健康",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "中小学心理健康教育指导纲要（2012年修订）/ 教育部相关要求 · 小学",
    "title": "面对挫折与情绪调节",
    "name_en": "Facing Setbacks and Sorting What You Can Change",
    "grade": 5,
    "grade_cn": "五年级",
    "domain": "emotion-regulation",
    "domain_cn": "情绪调适",
    "lesson_type": "workshop",
    "version": "1.0.0",
    "description": "面向小学五年级的情绪调适课：遇到一件没做好的事（比赛输了 / 考砸了 / 被选掉了），先把「事情本身」和「心里那句话」分开，再把这件事里的小卡片分成「我能改变的」和「我改变不了的」两堆，最后给每一个能改变的配一个今天就能做的具体做法。同时辨析「都怪自己」与「都怪别人」两种极端归因，练习站得住的说法。三个互动台子都能真的操作：分类器（八张卡片分两栏，分错会说明它更合适放在哪里）、归因改写台（四种极端说法各配三种改写，反馈一律写成「这样可能会……，还可以试试……」），以及综合任务里从选场景、分两栏到配做法、生成下一步清单的完整模拟。全课语气温和、不评判、不贴标签，不使用任何临床诊断词汇，不涉及自伤自杀话题，插图一律为中性简洁的教学插画。",
    "tags": ["面对挫折", "情绪调节", "归因", "能改变的与不能改变的", "五年级", "情绪调适"],
    "standard_ref": "《中小学心理健康教育指导纲要（2012年修订）· 小学中高年级》情绪调适——帮助学生克服学习困难，正确面对厌学等负面情绪，学会恰当地、正确地体验情绪和表达情绪；配合开展初步的青春期教育，引导学生进行恰当的异性交往，建立和维持良好的异性同伴关系。",
    "hero_question": "一次比赛输了，心里那句「都怪我，我怎么这么笨」一冒出来，人就沉下去了——这句话能改吗？改完以后先做什么？",
    "hero_alt": "面对挫折与情绪调节知识结构图：分清能改变的与不能改变的、别让归因走两个极端、给能改变的配一个具体做法 三栏",
    "hero_caption": "面对挫折与情绪调节：先说事实 · 分成两堆 · 给能改变的配一个具体做法",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "没做好的时候，怎么分清哪些是我能改变的？", "d": "事情一多就乱，想动手又不知道从哪一条开始", "v": "没做好的时候怎么分清哪些是我能改变的"},
        {"t": "为什么不能都怪自己，也不能都怪别人？", "d": "两种说法我都说过，可好像哪一种都不太对", "v": "为什么不能都怪自己也不能都怪别人"},
        {"t": "每件事都怪我，是不是不太公平？", "d": "有时候明明有别的因素，我还是先怪自己", "v": "每件事都怪我是不是不太公平"},
        {"t": "给能改变的事配一个具体做法，到底长什么样？", "d": "我只写得出「下次一定努力」这种话", "v": "给能改变的事配一个具体做法到底长什么样"},
    ],
    "objectives": [
        "能说出一件事没做好之后，最先要分清的是「我能改变的」和「我改变不了的」",
        "能把一件具体的事情，分成我能改变的和我改变不了的两堆",
        "能给每一个能改变的事，配上一个今天就能做的具体做法",
        "能分辨「都怪自己」和「都怪别人」这两种极端说法，说出更站得住的说法",
    ],
    "objectives_plain": [
        "能说出一件事没做好之后，最先要分清的是「我能改变的」和「我改变不了的」",
        "能把一件具体的事情，分成我能改变的和我改变不了的两堆",
        "能给每一个能改变的事，配上一个今天就能做的具体做法",
        "能分辨「都怪自己」和「都怪别人」这两种极端说法，说出更站得住的说法",
    ],
    "standards": [
        {"content": "帮助学生克服学习困难，正确面对厌学等负面情绪，学会恰当地、正确地体验情绪和表达情绪",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学中高年级 · 情绪调适"},
        {"content": "开展初步的青春期教育，引导学生进行恰当的异性交往，建立和维持良好的异性同伴关系",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学中高年级 · 情绪调适"},
    ],
    "prereqs": ["psych-e-g5-self-accept"],
    "prereqs_name": "悦纳自我与学习动机",
    "prereqs_meta": "psych-e-g5-self-accept",
    "leads_to": ["psych-e-g6-puberty"],
    "next_meta": "psych-e-g6-puberty",
    "section_images": ["assets/psych-e-g5-negative-emotion-fig1.webp",
                       "assets/psych-e-g5-negative-emotion-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "那句「都怪我」一冒出来人就沉下去了——这节课教你把它拆开：先说事实，再分成能改变的和不能改变的。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能写出一份自己的下一步清单。",
        "objectives": "看清四件事：为什么要分两堆、怎么分、怎么配做法、两种极端归因差在哪里。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "先分清「事情本身」和「心里那句话」，再把事情分成能改变的和不能改变的两堆。",
        "lab-1": "重点不是分得快，而是看看每一张为什么归那一栏——能动手的才算左边。",
        "module-2": "「全都怪我」和「全不怪我」只剩一个答案；站得住的说法把原因放到能动手的位置上。",
        "lab-2": "四种极端说法，各配三种改写；选完把解释读一遍，看看它带来的是什么。",
        "worked-example": "小舟四步：说清事实、分成两堆、把归因放回中间、给能改变的配一个做法。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "选场景 → 分两栏 → 配做法 → 生成清单，走完一遍就有自己的下一步了。",
        "posttest": "出现了考砸了、被选掉了、排练被换下来，看看你能不能用上今天的办法。",
        "summary": "三句话：先说事实、再分两堆、配一个具体做法。",
        "homework": "三层小任务，先做前两层，第三层可以请家里人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先帮你找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学心理健康「情绪调适」在五年级的空缺，正对课标「帮助学生克服学习困难，正确面对厌学等负面情绪，学会恰当地、正确地体验情绪和表达情绪」。五年级学生的难点有两个：① 事情一没做好，心里立刻冒出的是一句关于「我这个人」的结论，这句话一出口，人就停住了，缺的不是意志，而是「先把事实和自己那句话分开」的动作；② 有了力气之后不知道往哪儿使劲，因为分不清哪些在自己手里、哪些不在，于是只有「全都怪我」和「全不怪我」两种极端。所以全课围绕一条可操作的链路：概念一给出两步（把事实说清楚 → 分成「我能改变的」和「我改变不了的」）并给出判断分界线的问法；概念二辨析两种极端归因，给出站得住说法的三件套（有我的原因 ＋ 也有别的因素 ＋ 我下一步做什么）。三个台子都能真的操作：分类器（八张卡片分两栏，选错不放行并说明它更合适放在哪里，另留一个自由文本框）、归因改写台（四种极端说法各配三种改写，错误反馈一律写成「这样可能会……，还可以试试……」），以及综合任务里的完整模拟——选一件没做好的事（比赛输了 / 考砸了 / 被选掉了）→ 把六张卡片分到两栏 → 给每一张「能改变的」从三个具体做法里挑一个 → 生成「我的下一步清单」。全课语气温和、不评判、不贴标签，不使用任何临床诊断词汇，不涉及自伤自杀话题；插图一律为中性简洁的教学插画，不使用真实儿童照片风格人像。",
    "plan_table": """| 1 | cover | 面对挫折与情绪调节 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 「这件事没做好」之后，先分清能改变的和不能改变的 | 承·概念一（事实与两堆） |
| 6 | interactive | 动手一：分一分，哪些是我能改变的 | 承·分类器（八张卡片两栏） |
| 7 | concept | 别让归因走两个极端：都怪自己，和都怪别人 | 承·概念二（归因辨析） |
| 8 | interactive | 动手二：归因改写台，把极端说法改一改 | 承·改写练习（四句极端各三种改写） |
| 9 | concept | 例题示范：小舟的接力棒 | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：从一件没做好的事，到我的下一步清单 | 合·迁移应用（分两栏 + 配做法 + 生成清单） |
| 12 | quiz | 后测：换三个新情境，办法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，讲清面对挫折这件事 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：分清能改变的与不能改变的 / 别让归因走两个极端 / 给能改变的配一个具体做法 三栏\n- P5 挫折后的两步示意图（已生成）：先说清事实，再分成两堆，附中文标注\n- P7 两种极端归因与站得住说法的三栏对照图（已生成），附中文标注\n- 三张图均为中性简洁教学插画，人物只用简单图形，不使用任何真实儿童照片或可识别肖像\n- 若需补充：班级「下一步清单」便签样例（需学校提供并授权后使用）",
}
