# -*- coding: utf-8 -*-
"""小学心理健康 · 青春期教育与异性交往（G6）—— 补齐知识树「青春期与成长」空缺

铁规（这两门尤其敏感）：
  · 语气温和、不评判、不贴标签；严禁任何临床诊断词汇；绝不涉及自伤、自杀、性行为细节。
  · 本课只讲三件事：① 身体变化的科学常识（身高体重变化、第二性征的出现是正常的）；
    ② 个人边界与身体自主权（我的身体我做主，别人的身体要先问一句）；
    ③ 同伴与异性交往的尊重与分寸感（自然大方、公开场合、尊重对方答复、不拿身体变化开玩笑）。
  · 插图一律使用中性抽象符号/成长箭头/简笔小人轮廓（无细节），绝不生成写实人体或真人照片风格人像。
六年级落点：这一年身体开始变、同学之间开始不一样、心里多了说不清的感觉——
  先弄明白「什么是正常的」，再守住「我的边界」和「别人的边界」，最后练「怎么开口」。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/psych-e-g6-puberty-fig1.webp'
F2 = './assets/psych-e-g6-puberty-fig2.webp'

TTS = {
    "hero": "六年级的同学，先请你做一件很小的事：想一想这一年里，自己的身体发生了什么变化。可能是长得快了一点，可能是嗓音有点不一样，也可能是脸上多了几颗小痘痘。这些变化不用紧张，它们是身体在长大的记号。这节课我们说三件事：这些变化为什么会出现，为什么每个人的节奏都不一样，还有——当别人靠得太近、或者开你身体的玩笑时，你可以怎么说。",
    "problem-anchor": "开始之前，先选一个你最想弄清楚的问题。是想知道身体上的哪些变化是正常的，还是想知道为什么同学之间开始不一样了，又或者你想弄清楚，和异性同学相处怎么把握分寸，再或者你更想问：别人让我不舒服的时候，我该怎么开口。选好了，就带着它往下看。",
    "objectives": "这节课有四个小目标。第一，能说出青春期身体上常见的变化，知道这些变化每个人都会经历，是正常的。第二，能说出每个人的节奏不一样，早一点晚一点都在正常范围里，不给自己和同学贴标签。第三，能理解身体是属于自己的，遇到让自己不舒服的接触或者玩笑时，可以清楚地说出我不愿意，并且告诉信任的大人。第四，能说出和异性同伴交往的几条分寸：自然大方、在公开场合、尊重对方的答复、不拿别人的身体变化开玩笑。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "先说身体上的变化。到了这个年纪，身体里面有一些物质开始慢慢工作，它们会让你的身高长得比前几年快，体重也跟着增加；嗓音可能变得和以前不一样；额头和鼻子周围会冒出几颗小痘痘；出汗以后身上的气味比以前重一点。这些变化是从身体里面开始的，不是你做错了什么，也不是你哪里不好。它们有一个共同的名字，叫长大的记号。",
    "lab-1": "现在我们做一个小练习。下面有六张卡片，都是同学们身上真实发生过的事。先点一张卡片，再点上面两栏里的一个：它属于每个人长大时几乎都会有的变化，还是属于每个人节奏不一样的地方。分得不太合适也不会说你错，我会告诉你为什么，你还可以换一栏再试一次。",
    "module-2": "再说第二件事：身体是属于你自己的。哪些地方可以被碰到、和别人靠多近、愿不愿意被人搂着走，这些由你自己决定。别人也有同样的权利，所以想靠近之前先问一句。如果对方说不要，就停下来；如果自己觉得不舒服，也可以直接说出不愿意。这不是不礼貌，这是在守住自己，也是在尊重别人。",
    "lab-2": "现在请你当一次边界判断员。下面有四个小情境，每个情境里有三种做法。先点开一个情境，再从三种做法里选一个，看看它会带来什么。选得不太合适也不会批评你，我会告诉你这样可能会发生什么，还可以试试什么。",
    "worked-example": "我们一起帮小然想一想。老师让每四个人一组做一块板报，小然想邀请隔壁组的小雨一起做，又怕别人起哄。我们陪他走四步。第一步，把事情说清楚：我想和小雨一起做板报这一块。第二步，分成两堆：我能决定的，是我怎么开口、在哪里开口、说完怎么接话；我不能决定的，是别人怎么想、会不会起哄。第三步，套上分寸三条：自然大方，不遮不掩；在教室里说，不去没人的角落；尊重对方的答复，对方说不太方便也可以。第四步，给今天配一个做法：课间在教室里问一句，我们一起做这一块板报好吗。",
    "conceptest-1": "接下来用三个说法考考你，每一个里面都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件大事交给你。先选一个你可能会遇到的情境，再想一想那三句话：这样安全吗，我舒服吗，对方愿意吗。然后从三个第一步里选一个，看看每一个选择的后果。选完以后，你会得到一张属于自己的分寸提示卡。",
    "posttest": "最后一轮，换三个新的小情境来考考你。这次会出现长得特别快、同学开始变声，还有大人想抱你，看看你能不能守住自己的边界，也尊重别人的边界。",
    "summary": "这节课我们记住三句话。第一句，青春期身体上的变化是长大的记号，每个人都会经历，只是节奏不一样。第二句，身体是属于你自己的，别人靠近之前要先问一句，你不愿意就可以说不愿意。第三句，和异性同伴相处，自然大方、在公开场合、尊重对方的答复，就不容易出问题。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出三条青春期常见的身体变化，再说一说每个人的节奏不一样是什么意思。第二层能力应用，动手做：和家人说一件你最近注意到的身体变化，再练习一句拒绝的话。第三层迁移挑战，选做：找出班里两三句拿别人身体变化开玩笑的话，把它们改成尊重人的说法。",
    "knowledge-graph": "这张图展示了这节课在心理健康知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 身体在长大，这些变化是正常的", "lab-1": "动手一 分一分：常见的成长变化 / 不一样的节奏",
    "module-2": "概念二 身体是自己的：边界与尊重", "lab-2": "动手二 边界判断台",
    "worked-example": "例题讲解 小然的板报小组", "conceptest-1": "概念测试",
    "synthesis": "综合任务 分寸三问练习台", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：成长变化分类台（六张卡片，两栏） ──
GROW_BINS = [
    {"id": "common", "name": "① 长大时几乎都会有的"},
    {"id": "pace", "name": "② 每个人节奏不一样的地方"},
]

GROW_CARDS = [
    {"id": "g1", "bin": "common", "t": "一年里个头蹿高了好几厘米",
     "fb": "这是最常见的变化。身体长得快的时候，一年高几厘米很平常。"},
    {"id": "g2", "bin": "common", "t": "嗓音和以前不太一样了",
     "fb": "嗓音的变化也是长大的记号之一。它自己会慢慢稳定下来。"},
    {"id": "g3", "bin": "common", "t": "额头上开始冒出几颗小痘痘",
     "fb": "长痘痘在这个年纪很常见。保持清洁、早点睡觉，会舒服一些。"},
    {"id": "g4", "bin": "pace", "t": "同桌已经长得很高，我还没有动静",
     "fb": "这一条讲的是节奏。开始的时间前后差一两年都算正常，不用拿别人当尺子。"},
    {"id": "g5", "bin": "pace", "t": "有的同学先变声，有的同学后变声",
     "fb": "同样是节奏问题。谁早谁晚，都不说明谁更好或者更差。"},
    {"id": "g6", "bin": "pace", "t": "有人半年就换了两双鞋，我一年也没换",
     "fb": "长个子有快慢，鞋子换得勤不勤也是节奏的一部分。别急着和别人比。"},
]

# ── 动手二：边界判断台（四个情境 × 三种做法） ──
BOUNDS = [
    {"id": "b1", "t": "同桌想借我的外套披一下",
     "opts": [
         {"t": "先问自己愿不愿意：愿意就借，不愿意就说「今天我也要用，下次吧」", "ok": True,
          "fb": "这样可能会让你心里很踏实——你既没有为难自己，也没有为难对方。"},
         {"t": "觉得不好意思拒绝，就勉强借出去，心里有点不自在", "ok": False,
          "fb": "这样可能会让你心里堵一小会儿，还容易越想越委屈。还可以试试：先停两秒，问自己一句「我愿不愿意」，再把答案说出来。"},
         {"t": "皱着眉说「你好烦」，把外套塞过去", "ok": False,
          "fb": "这样可能会让两个人都尴尬。还可以试试：拒绝也可以好好说——「对不起，今天我自己也要穿」。"},
     ]},
    {"id": "b2", "t": "有同学在班里喊我关于身体变化的绰号",
     "opts": [
         {"t": "平静地说「我不喜欢这个称呼，请不要这样叫我」，还继续就告诉老师", "ok": True,
          "fb": "这样可能会让玩笑停下来——你说清楚了边界，也给了对方改的机会。"},
         {"t": "跟着一起笑，装作不在意", "ok": False,
          "fb": "这样可能会让对方以为你不介意，玩笑就停不下来。还可以试试：说一句「我不喜欢这个称呼」，声音不用大，说清楚就够了。"},
         {"t": "也给他起一个更难听的绰号", "ok": False,
          "fb": "这样可能会把玩笑变成互相伤害。还可以试试：把你的不舒服说给老师听，让老师帮着把话说清楚。"},
     ]},
    {"id": "b3", "t": "我想邀请一位异性同学和我一组做板报",
     "opts": [
         {"t": "在教室里大方地说一句「我们一起做这一块板报，好吗」", "ok": True,
          "fb": "这样可能会很顺利——事情说得清清楚楚，对方答不答应都轻松。"},
         {"t": "写一张纸条，让他放学后到没人的地方再说", "ok": False,
          "fb": "这样可能会让对方为难，也容易被别人误会。还可以试试：在大家都看得见的地方，把事情直接说出来。"},
         {"t": "让别的同学替我传话，自己不开口", "ok": False,
          "fb": "话传一遍容易变样。还可以试试：自己说一句，简单直接，其实最轻松。"},
     ]},
    {"id": "b4", "t": "好朋友走路时一直挽着我的胳膊，我有点不舒服",
     "opts": [
         {"t": "说一句「我不太习惯这样」，换一个都舒服的方式，比如并排走", "ok": True,
          "fb": "这样可能会让两个人都自在——你把习惯说出来，也留住了这段友谊。"},
         {"t": "忍着不说，走完这一路", "ok": False,
          "fb": "这样可能会让你下次还想躲开。还可以试试：把自己的习惯说一句给对方听，真正的朋友会尊重它。"},
         {"t": "甩开手，什么也不说就走掉", "ok": False,
          "fb": "这样可能会让对方觉得莫名其妙。还可以试试：先说出来再走——「这样我有点不自在，我们并排走吧」。"},
     ]},
]

# ── 综合任务：分寸三问练习台（情境 × 三个「我能做的第一步」） ──
PACE = [
    {"id": "p1", "t": "有人想和我玩推来推去的游戏",
     "steps": [
         {"t": "先问自己「这样玩我安全吗、我舒服吗」，不舒服就说「换一个玩」",
          "fb": "这样可能会让你既玩得开心，也守住了自己的边界。"},
         {"t": "先答应下来，觉得不舒服再中途退出",
          "fb": "这样可能会在你还来不及开口的时候就被撞到了。还可以试试：玩之前先说好规则，不做容易摔倒的动作。"},
         {"t": "大声说「别碰我」，然后转身走开",
          "fb": "这样可能会让气氛一下子紧张起来。还可以试试：把话说清楚就够了——「我不想玩这个，我们玩别的。」"},
     ]},
    {"id": "p2", "t": "同学在议论另一位同学的身高和嗓音",
     "steps": [
         {"t": "不跟着说，把话头换一个方向：「要不我们说运动会的事吧」",
          "fb": "这样可能会让被议论的同学少受一次委屈，也让聊天轻松下来。"},
         {"t": "跟着说两句，反正大家都在说",
          "fb": "这样可能会让被议论的同学很难受，下一次也可能轮到你。还可以试试：把话头接过来换个方向，一句话就能停下来。"},
         {"t": "指着说话的同学说「就你话多」",
          "fb": "这样可能会吵起来。还可以试试：提醒那个具体的点——「他本人听到会不舒服的。」"},
     ]},
    {"id": "p3", "t": "我想约一位异性同学一起准备小组展示，别人开始起哄",
     "steps": [
         {"t": "继续把正事说完：「我们只是一起做这一组，走吧」",
          "fb": "这样可能会让起哄的人没什么可说的——你把事情本身讲清楚了。"},
         {"t": "马上说不做了，红着脸走开",
          "fb": "这样可能会让你少掉一次合作的机会。还可以试试：把正事说完再走，起哄的话就落不到你身上。"},
         {"t": "和起哄的人当场吵起来",
          "fb": "这样可能会把注意力全引到起哄上。还可以试试：先做正事，事后把这件事告诉老师。"},
     ]},
    {"id": "p4", "t": "有人靠我特别近说话，我有点不舒服",
     "steps": [
         {"t": "退一小步，再把话说出来：「我们站开一点说话吧」",
          "fb": "这样可能会让你舒服很多——只说距离，不说人，对方也听得进去。"},
         {"t": "一直往后躲，什么也不说",
          "fb": "这样可能会让对方一直没发现自己越过了线。还可以试试：说出来，哪怕只有一句。"},
         {"t": "伸手把对方推开",
          "fb": "这样可能会把小事变成冲突。还可以试试：先退一步，再用一句话说出来。"},
     ]},
]

CUSTOM_JS = r"""
/* ============================================================
   psych-e-g6-puberty 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 成长变化分类台：六张卡片 → 「几乎都会有 / 节奏不一样」两栏
   3) 边界判断台：情境 × 三种做法 → 温和反馈（这样可能会……，还可以试试……）
   4) 分寸三问练习台：选情境 → 选第一步 → 展开后果 → 生成分寸提示卡
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

  /* ---------- 2. 成长变化分类台 ---------- */
  var CARDS = __CARDS_JSON__;
  var BINS = __BINS_JSON__;
  var bank = document.getElementById('gr-bank');
  if (bank && CARDS.length) {
    var placed = {}, picked = null;
    var out = document.getElementById('gr-out');
    var score = document.getElementById('gr-score');

    function cardById(id) {
      for (var i = 0; i < CARDS.length; i++) { if (CARDS[i].id === id) return CARDS[i]; }
      return null;
    }
    function binName(id) {
      for (var i = 0; i < BINS.length; i++) {
        if (BINS[i].id === id) return BINS[i].name.replace(/^[①②]\s*/, '');
      }
      return '';
    }
    CARDS.forEach(function (it) {
      var b = document.createElement('button');
      b.className = 'sort-item';
      b.dataset.gcard = it.id;
      b.textContent = it.t;
      b.addEventListener('click', function () {
        if (placed[it.id]) return;
        picked = it.id;
        document.querySelectorAll('[data-gcard]').forEach(function (x) {
          x.classList.toggle('selected', x.dataset.gcard === picked);
        });
        out.className = 'result warn';
        out.innerHTML = '<strong>你选中了：</strong>' + it.t + '<br>它属于哪一栏？点一下上面两栏中的一个。';
      });
      bank.appendChild(b);
    });
    BINS.forEach(function (bn) {
      var box = document.getElementById('gr-bin-' + bn.id);
      if (!box) return;
      box.addEventListener('click', function () {
        if (!picked) {
          out.className = 'result warn';
          out.textContent = '先在左边点一张卡片，再点这一栏。';
          return;
        }
        var it = cardById(picked);
        if (!it || placed[it.id]) return;
        if (it.bin !== bn.id) {
          out.className = 'result warn';
          out.innerHTML = '<strong>这一条再想一想。</strong>' + it.fb +
            '<br>它更合适放在「' + binName(it.bin) + '」那一栏，换一栏再点一次试试。';
          return;
        }
        placed[it.id] = true;
        var card = document.querySelector('[data-gcard="' + it.id + '"]');
        if (card) { card.classList.add('done'); card.classList.remove('selected'); }
        var tag = document.createElement('span');
        tag.className = 'tag';
        tag.textContent = it.t;
        box.querySelector('.bin-list').appendChild(tag);
        box.classList.add('ok');
        picked = null;
        var n = Object.keys(placed).length;
        score.textContent = '已经分好 ' + n + ' / ' + CARDS.length + ' 张';
        out.className = 'result';
        out.innerHTML = '<strong>分对了。</strong>' + it.fb;
        if (n === CARDS.length) {
          out.className = 'result';
          out.innerHTML = '<strong>六张卡片都分好了。</strong>左边那一栏，是几乎所有人在这个年纪都会遇到的变化；' +
            '右边那一栏，说的是节奏——谁早谁晚都正常。<br>记住这个顺序：<strong>先知道什么是正常的，再决定要不要为自己担心。</strong>';
        }
      });
    });
    score.textContent = '已经分好 0 / ' + CARDS.length + ' 张';
  }

  /* ---------- 3. 边界判断台 ---------- */
  var BND = __BOUNDS_JSON__;
  var bStage = document.getElementById('bd-stage');
  if (bStage && BND.length) {
    var curB = null, doneB = {};
    var bOut = document.getElementById('bd-out');
    var bScore = document.getElementById('bd-score');

    function bById(id) {
      for (var i = 0; i < BND.length; i++) { if (BND[i].id === id) return BND[i]; }
      return null;
    }
    function renderB() {
      document.querySelectorAll('[data-bd]').forEach(function (b) {
        var k = b.dataset.bd;
        b.classList.toggle('selected', k === curB);
        b.classList.toggle('done', !!doneB[k]);
      });
      bScore.textContent = '已经找到合适做法 ' + Object.keys(doneB).length + ' / ' + BND.length + ' 个情境';
    }
    function paintB() {
      var box = document.getElementById('bd-opts');
      box.innerHTML = '';
      if (!curB) return;
      var S = bById(curB);
      if (!S) return;
      S.opts.forEach(function (o) {
        var b = document.createElement('button');
        b.className = 'choice' + (doneB[curB] && o.ok ? ' correct' : '');
        b.style.textAlign = 'left';
        b.textContent = o.t;
        b.addEventListener('click', function () {
          if (doneB[curB]) return;
          if (o.ok) {
            doneB[curB] = true;
            bOut.className = 'result';
            bOut.innerHTML = '<strong>这一条站得住。</strong>' + o.fb;
          } else {
            bOut.className = 'result warn';
            bOut.innerHTML = '<strong>这个选择不少同学都做过，我们看看它会带来什么。</strong>' + o.fb;
          }
          renderB();
          paintB();
        });
        box.appendChild(b);
      });
    }
    document.querySelectorAll('[data-bd]').forEach(function (b) {
      b.addEventListener('click', function () {
        curB = b.dataset.bd;
        var S = bById(curB);
        if (doneB[curB]) {
          bOut.className = 'result';
          bOut.innerHTML = '<strong>这个情境已经看过了。</strong>记住那句话：<strong>先说出自己的感觉，再给出一个办法</strong>——两句话就够了。';
        } else {
          bOut.className = 'result warn';
          bOut.innerHTML = '<strong>情境：' + S.t + '</strong><br>下面有三种做法，选一个你觉得合适的试试。';
        }
        renderB();
        paintB();
      });
    });
    renderB();
  }

  /* ---------- 4. 分寸三问练习台 ---------- */
  var PACE = __PACE_JSON__;
  var pBank = document.getElementById('pc-stage');
  if (pBank && PACE.length) {
    var curP = null, pPicked = {}, pChosen = {};
    var pOut = document.getElementById('pc-out');
    var pScore = document.getElementById('pc-score');
    var pCard = document.getElementById('pc-card-out');

    function pById(id) {
      for (var i = 0; i < PACE.length; i++) { if (PACE[i].id === id) return PACE[i]; }
      return null;
    }
    function pName(id) { var s = pById(id); return s ? s.t : ''; }
    function renderP() {
      document.querySelectorAll('[data-pc]').forEach(function (b) {
        var k = b.dataset.pc;
        b.classList.toggle('selected', k === curP);
        b.classList.toggle('done', pChosen[k] !== undefined);
      });
      pScore.textContent = '已经练习 ' + Object.keys(pChosen).length + ' / ' + PACE.length + ' 个情境';
    }
    function paintP() {
      var box = document.getElementById('pc-steps');
      box.innerHTML = '';
      if (!curP) return;
      var S = pById(curP);
      if (!S) return;
      var head = document.createElement('p');
      head.style.cssText = 'margin:0 0 8px;color:var(--muted);font-size:14px';
      head.textContent = '先问三句：这样安全吗？我舒服吗？对方愿意吗？再从三个第一步里挑一个。';
      box.appendChild(head);
      (S.steps || []).forEach(function (st, i) {
        var b = document.createElement('button');
        b.className = 'choice' + (pChosen[curP] === i ? ' correct' : '');
        b.style.cssText = 'text-align:left;margin:4px 0';
        b.textContent = '第一步 ' + (i + 1) + '：' + st.t;
        b.addEventListener('click', function () {
          if (pPicked[curP]) return;
          pPicked[curP] = true;
          pChosen[curP] = i;
          pOut.className = (i === 0) ? 'result' : 'result warn';
          pOut.innerHTML = '<strong>你选了第一步 ' + (i + 1) + '。</strong>' + st.fb;
          renderP();
          paintP();
        });
        box.appendChild(b);
      });
    }
    document.querySelectorAll('[data-pc]').forEach(function (b) {
      b.addEventListener('click', function () {
        curP = b.dataset.pc;
        var S = pById(curP);
        if (pChosen[curP] !== undefined || pPicked[curP]) {
          pOut.className = 'result';
          pOut.innerHTML = '<strong>这个情境已经练习过了。</strong>换一个情境，或者到右边生成你的分寸提示卡。';
        } else {
          pOut.className = 'result warn';
          pOut.innerHTML = '<strong>情境：' + S.t + '</strong><br>下面有三个「我能做的第一步」，选一个试试，看看它的后果。';
        }
        renderP();
        paintP();
      });
    });
    var pGen = document.getElementById('pc-gen');
    if (pGen) {
      pGen.addEventListener('click', function () {
        var lines = [];
        PACE.forEach(function (s) {
          var idx = pChosen[s.id];
          if (idx === undefined) {
            lines.push('· ' + s.t + ' → 还没选，想一想三句话：安全吗、舒服吗、对方愿意吗。');
          } else {
            lines.push('· ' + s.t + ' → ' + s.steps[idx].t);
          }
        });
        var miss = 0;
        PACE.forEach(function (s) { if (pChosen[s.id] === undefined) miss++; });
        pOut.className = 'result';
        pOut.innerHTML = '<strong>我的分寸提示卡：</strong><br>' + lines.join('<br>') +
          (miss ? '<br>还有 ' + miss + ' 个情境没练，练完这张卡就完整了。'
                : '<br>四个情境都练完了。三句话随身带着：安全吗、舒服吗、对方愿意吗。');
        if (pCard) {
          pCard.className = 'result';
          pCard.innerHTML = '<strong>提示卡写好了。</strong>把它抄在便签上，贴在书桌前：' +
            '身体是我的，别人的身体要先问一句；不愿意就说出来，说出来的时候语气可以很平静。';
        }
      });
    }
    renderP();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__CARDS_JSON__', json.dumps(GROW_CARDS, ensure_ascii=False))
             .replace('__BINS_JSON__', json.dumps(GROW_BINS, ensure_ascii=False))
             .replace('__BOUNDS_JSON__', json.dumps(BOUNDS, ensure_ascii=False))
             .replace('__PACE_JSON__', json.dumps(PACE, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "这一年里，你的同桌长得比你快，你还没有什么变化。下面哪种想法更合适？",
         "options": [("每个人的节奏不一样，早一点晚一点都在正常范围里", True),
                     ("我没变化，说明我身体有问题", False),
                     ("我得想办法快点长，不然就落后了", False)],
         "explain": "长个子有快有慢，开始的时间前后差一两年是很常见的事。"
                    "<strong>错因提醒：</strong>常见错误是拿同学的时间表当尺子，把自己和别人比出一个结论——比出来的只是节奏不同，不是谁好谁不好。"},
        {"q": "有同学当众拿你的身体变化开玩笑，你心里不太舒服。下面哪个做法更合适？",
         "options": [("平静地说「我不喜欢这个玩笑，请不要这样说」，还继续就告诉老师", True),
                     ("忍着不说，等他/她自己发现", False),
                     ("也去说他一句更狠的", False)],
         "explain": "把自己的感觉说出来，是在守边界，不是在闹脾气。"
                    "<strong>错因提醒：</strong>最容易搞混的是「忍一下」和「守住边界」——忍着不说，玩笑往往不会自己停下来。"},
        {"q": "下面哪一句是在尊重别人的边界？",
         "options": [("想挽着同学一起走之前，先问一句「可以吗」", True),
                     ("关系好就可以不打招呼，直接翻看对方的笔记本", False),
                     ("对方说了不要，还是继续试一下", False)],
         "explain": "别人的身体和东西由别人决定，问一句是最省事的办法。"
                    "<strong>错因提醒：</strong>有人误认为「关系好就不用问」——边界和关系好坏是两件事，越亲近越要问一句。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "身体在长大，这些变化是正常的", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们已经知道了怎么给自己的情绪起名字，也练过遇到挫折先分清能改变的和不能改变的（And）；可是最近身体开始变了，同学之间也开始不一样了，心里会冒出一些没人可问的问题（But）；所以这节课先把身体上的变化讲清楚——哪些是正常的、为什么每个人节奏不同（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">到了这个年纪，身体会开始出现一些<strong>看得见的变化</strong>。它们不是毛病，是身体在长大的记号。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>① 常见的变化有哪些</strong></p>
            <p style="color:var(--muted)">身高长得比前几年快、体重跟着增加、嗓音变得不一样、脸上冒出几颗小痘痘、出汗后气味重一点。</p>
          </div>
          <div class="inner-card">
            <p><strong>② 它们从哪里来</strong></p>
            <p style="color:var(--muted)">身体里面有几种物质开始慢慢工作，把长大的开关一个接一个打开。它自己会发生，不需要你做什么。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="青春期身体常见变化的成长示意图，用成长箭头与中性简笔轮廓表示身高、体重与嗓音的变化，附中文标注">
          <figcaption>示意图：身高、体重、嗓音、皮肤上的小变化，都是身体在长大的记号（教学示意图，人物为中性简笔轮廓，不含身体细节）</figcaption>
        </figure>
        <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(78,205,196,.45)">
          <p><strong>可以照着问自己的两句话：</strong></p>
          <p style="color:var(--muted)">第一句：<strong>这是不是很多人都遇到过的变化？</strong>　第二句：<strong>我有没有把它变成一句关于自己的结论？</strong>如果有，就把结论放下来，只留下那件能看见的变化。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「只有我自己是这样，别人都很正常」。这里最容易<strong>搞混</strong>的是「我不知道」和「只有我这样」——不知道是因为大家都不好意思说，不是因为只有你一个人。把它说给信任的大人听，你会发现自己并不特别。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "把这一年照的几张照片放在一起看，你会看到一条慢慢向上的线。变化一直在发生，只是每天看不太出来。"},
    {"lens": "拆开它", "text": "身体的变化分两种：一种几乎所有人在这个年纪都会遇到，比如长个子；另一种只和时间有关，比如谁先谁后。两种都不是评价，只是过程。"},
    {"lens": "迁移它", "text": "这种「先知道什么是正常的，再决定要不要担心」的办法，之后在许多事情上都能用：第一次住校、第一次上台、第一次和同学闹别扭。"},
])}
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>长高长重、嗓音痘痘——<strong>都是长大的记号，不是毛病；有人早有人晚，都不是好坏。</strong></div></div>
    ''', tag="概念一"))

    grow_bins = "\n".join(
        f'''            <div class="sort-bin" id="gr-bin-{b["id"]}" role="button" tabindex="0">
              <h4>{b["name"]}</h4>
              <div class="bin-list"></div>
            </div>'''
        for b in GROW_BINS
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：分一分，哪些是常见的、哪些是节奏不同", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">六张卡片都来自同学们身上真实发生过的事。先在左边点一张，再点上面两栏中的一个。<strong>分得不太合适也不会说你错</strong>，我会告诉你为什么，还可以换一栏再试一次。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 六张小卡片（点一张选中）</div>
          <div class="sort-bank" id="gr-bank"></div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 它属于哪一栏</div>
          <div class="sort-bins">
{grow_bins}
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">分类进度</span><span class="v" id="gr-score">已经分好 0 / 6 张</span></div>
          </div>
          <p class="result warn" id="gr-out" style="margin-top:12px">先在左边点一张卡片。</p>
        </div>
        <div class="inner-card" style="margin-top:14px">
          <p><strong>写一条你自己的：</strong></p>
          <p style="color:var(--muted)">写下这一年里你注意到的<strong>一条变化</strong>，再写一句：它属于常见的变化，还是属于节奏不同？</p>
          <textarea id="gr-answer" rows="2" placeholder="我注意到的变化是……它属于……" style="margin-top:8px"></textarea>
        </div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "身体是自己的：我的边界和别人的边界", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">第二件事，是这一课最重要的：<strong>身体是属于你自己的</strong>。哪些地方可以被碰到、和别人靠多近，由你自己决定。</p>
        <div class="grid grid-3">
          <div class="inner-card">
            <p><strong>我的边界</strong></p>
            <p style="color:var(--muted)">我觉得不舒服，就可以说出来。不愿意的时候说不愿意，不需要先找一个理由。</p>
          </div>
          <div class="inner-card">
            <p><strong>别人的边界</strong></p>
            <p style="color:var(--muted)">别人也有同样的权利。想靠近、想借用、想牵手之前，先问一句；对方说不要，就停下来。</p>
          </div>
          <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(78,205,196,.45)">
            <p><strong>同伴交往的分寸</strong></p>
            <p style="color:var(--muted)">和异性同学相处也可以很自然：在大家都看得见的地方，大方地把事情说出来，尊重对方的答复。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="个人边界与尊重示意图，用两个圆圈、一条边界虚线与中性简笔轮廓表示身体自主权，附中文标注">
          <figcaption>示意图：每个人身边都有一个自己的圈；别人的圈要靠问一句才进得去（教学示意图，图形为抽象符号，不含身体细节）</figcaption>
        </figure>
        <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(78,205,196,.45)">
          <p><strong>说不愿意，可以这样说：</strong></p>
          <p style="color:var(--muted)">「我不太喜欢这样」　「我们站开一点说话吧」　「这件事我不想说」　「请你不要这样叫我」。<strong>语气平静就够了，越简短越有力。</strong></p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「拒绝了别人，就是不给面子、会伤感情」。这里最容易<strong>搞混</strong>的是「拒绝这件事」和「否定这个人」——你拒绝的是一件事，不是那个人。真正的同伴关系，经得起一句「我不太喜欢这样」。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "想象每个人身边都有一个自己的圈。圈的大小由自己定，圈里的东西由自己做主——这不是小气，是每个人都有的权利。"},
    {"lens": "比较它", "text": "「我不想」和「我不该」是两句不同的话。前者说的是我的感觉，可以直接说出口；后者是一句评价，说出来自己也会难受。"},
    {"lens": "迁移它", "text": "同一句话，也可以用在自己的东西上：不想借的文具、不想被翻看的笔记本、不想被传出去的聊天记录。"},
])}
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>我的身体我做主，别人的身体问一句——<strong>不愿意就停下，不拿身体开玩笑。</strong></div></div>
    ''', tag="概念二"))

    bd_btns = "\n".join(
        f'            <button class="choice" data-bd="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in BOUNDS
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：边界判断台，四种做法你选哪个", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">四个小情境，每个情境里有三种做法。点开一个情境，再从三种做法里选一个。<strong>选得不太合适也不会批评你</strong>，我会告诉你这样可能会发生什么，还可以试试什么。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 选一个情境</div>
          <div class="grid" id="bd-stage">
{bd_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 三种做法，选一个试试</div>
          <div class="grid" id="bd-opts">
            <span style="color:var(--muted);font-size:14px">先在上面点一个情境，这里就会出现三种做法。</span>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">练习进度</span><span class="v" id="bd-score">已经找到合适做法 0 / 4 个情境</span></div>
          </div>
          <p class="result warn" id="bd-out" style="margin-top:12px">先点一个你自己也遇到过的情况。</p>
        </div>
        <div class="inner-card" style="margin-top:14px">
          <p><strong>轮到你自己写一句：</strong></p>
          <p style="color:var(--muted)">如果有人做了一件让你不太舒服的事，你会怎么说？把你的那一句话写下来。</p>
          <textarea id="bd-answer" rows="2" placeholder="我不太喜欢这样，可以请你……" style="margin-top:8px"></textarea>
        </div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小然的板报小组", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>老师让每四个人一组做一块板报。小然想邀请隔壁组的小雨一起做，那是他挺投缘的一位同学。可他又怕别人起哄，站在教室门口犹豫了很久。请你陪他走四步。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>把事情说清楚：</strong>我想和小雨一起做板报这一块。只说想做什么，不给这件事下别的结论。</div></div>
          <div class="step"><span class="n">2</span><div><strong>分成两堆：</strong>我能决定的——怎么开口、在哪里开口、说完以后怎么接话；我不能决定的——别人怎么想、会不会起哄。</div></div>
          <div class="step"><span class="n">3</span><div><strong>套上分寸三条：</strong>自然大方，不遮不掩；在教室里说，不去没人的角落；尊重对方的答复，对方说不太方便也可以。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>给今天配一个做法：</strong>课间在教室里问一句「我们一起做这一块板报，好吗」。如果对方说不太方便，就说「好，需要的时候叫我」。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「和异性同学一起做事，就一定要被人起哄，所以还是躲开最好」。这里最容易<strong>搞混</strong>的是「一起完成任务」和「别的什么」——一起做板报就是把板报做好，事情本身就是最好的说明。起哄的人需要的只是一个话题，你把正事说完，这个话题就落空了。</p>
        </div>
        <div class="inner-card">
          <p><strong>说给同桌听：</strong>这四步里，哪一步你自己已经做到了？哪一步还想再练一练？如果换成是你，你会把这句话放在哪里说？</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "关于身体上的变化，下面哪种说法更合适？",
         "options": [("每个人的节奏不一样，早一点晚一点都在正常范围里", True),
                     ("我还没开始长，说明我身体出了问题", False),
                     ("长得快的那位同学，应该被大家多注意一下", False)],
         "explain": "节奏不同是常态，不是评价；把同学的变化拿来当话题，也会让对方不舒服。"
                    "<strong>错因提醒：</strong>常见错误是把「和别人不一样」直接读成「我有问题」——中间的这一步其实不成立，不一样本来就是常态。"},
        {"q": "下面哪一种做法，最接近「守住自己的边界」？",
         "options": [("平静地说一句「我不太喜欢这样」，把话说清楚", True),
                     ("一直忍着，心里希望对方自己发现", False),
                     ("当场发很大的脾气，让别人知道厉害", False)],
         "explain": "说出感觉是最省事、也最有效的一步，语气平静就够了。"
                    "<strong>错因提醒：</strong>最容易搞混的是「忍着」和「大发脾气」——两个极端都没把话说到点子上，而一句平静的话往往就够用了。"},
        {"q": "想和一位异性同学一起做小组作业，下面哪种做法更合适？",
         "options": [("在教室或图书角大方地说一句「我们一起做这一组吧」", True),
                     ("写纸条，约对方放学后到没人的地方说", False),
                     ("让别人替自己传话，自己不开口", False)],
         "explain": "在大家都看得见的地方把事情说出来，对方轻松，你也不容易被误会。"
                    "<strong>错因提醒：</strong>有人误认为「越秘密越认真」——其实越公开越简单，事情说完就过去了。"}
    ], tag="概念测试"))

    pc_btns = "\n".join(
        f'            <button class="choice" data-pc="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in PACE
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：分寸三问练习台，找到我的第一步", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先选一个你可能会遇到的情境，再问那三句话：<strong>这样安全吗？我舒服吗？对方愿意吗？</strong>然后从三个第一步里挑一个，看看每个选择的后果。<strong>选得不太合适也不用担心</strong>，我会告诉你还可以试试什么。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 选一个你可能遇到的情境</div>
          <div class="grid" id="pc-stage">
{pc_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 三个「我能做的第一步」</div>
          <div class="grid" id="pc-steps">
            <span style="color:var(--muted);font-size:14px">先在上面点一个情境，这里就会出现三个第一步。</span>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">练习进度</span><span class="v" id="pc-score">已经练习 0 / 4 个情境</span></div>
          </div>
          <div class="flex-row">
            <button class="choice" id="pc-gen" style="text-align:center">③ 生成我的分寸提示卡</button>
          </div>
          <p class="result warn" id="pc-out" style="margin-top:12px">先在第一步选一个情境。</p>
          <p id="pc-card-out" style="margin-top:10px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💛</span><div><strong>记在心里的三句话：</strong>身体是我的，别人的身体要先问一句；不愿意就说出来，说出来的时候可以很平静；一起做事，就在大家都看得见的地方说。</div></div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换三个新情境，办法还在不在", TTS["posttest"], [
        {"q": "这一年你长得特别快，鞋子半年换了两双，心里有点慌。下面哪个想法更合适？",
         "options": [("这是长得快的常见样子，先把鞋换好，别急着给自己下结论", True),
                     ("我一定是不正常，得赶紧想办法停下来", False),
                     ("以后尽量少动，免得再长高", False)],
         "explain": "长得快的那几年换鞋勤，是很常见的现象，不需要用什么办法去打断它。"
                    "<strong>错因提醒：</strong>常见错误是把「变化快」误认为「出问题了」——变化的快慢都在正常范围里，先观察，再决定要不要问大人。"},
        {"q": "班里几位同学开始变声，有同学觉得好玩，一直在学。你更赞同下面哪一种做法？",
         "options": [("提醒一句：这个学起来他本人会不舒服，咱们说点别的", True),
                     ("跟着一起笑，反正大家都很开心", False),
                     ("当场和他吵，让大家评理", False)],
         "explain": "把话头换一个方向，是成本最低、也最有效的一种帮忙。"
                    "<strong>错因提醒：</strong>最容易搞混的是「好玩的玩笑」和「让别人难受的玩笑」——被笑的那个人是不是舒服，才是分界线。"},
        {"q": "一位很久不见的亲戚见到你就想抱一下，你不太想被抱。下面哪个做法更合适？",
         "options": [("说一句「我不太喜欢被抱，握个手吧」，回家也可以告诉爸爸妈妈", True),
                     ("忍着让他抱完，什么也不说", False),
                     ("什么都不说，一直往后退", False)],
         "explain": "身体是自己的，长辈也一样要先问。说一句客气话，既守住了边界，也照顾了场面。"
                    "<strong>错因提醒：</strong>有人误认为「大人要抱就是喜欢我，拒绝会不礼貌」——礼貌可以用别的方式表达，比如握手、打招呼。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，讲清长大的这件事", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>变化是正常的：</strong>长个子、体重增加、嗓音变化、小痘痘，都是身体在长大的记号，每个人都会遇到。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>节奏是各不相同的：</strong>谁早谁晚都在正常范围里，不拿别人的时间表当尺子，也不拿别人的变化当话题。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>边界要守，也要尊重：</strong>身体是我的，别人靠近前先问一句；不愿意就说出来，语气可以很平静。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>还想多说一句：</strong>如果有些变化让你一直放不下，或者心里有点沉，把它说给信任的大人听——爸爸妈妈、老师都可以。说出来不是说你有问题，而是让懂的人帮你把不清楚的地方说清楚。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「正常、节奏、边界」这三个词，说清楚你这一年身体上的一件事。</p>
          <p style="color:var(--muted)">再动一动手：<strong>画出</strong>两个圆圈，左边写三条「我能自己做主的」，右边写两条「我要先问一句的」。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写出三条青春期常见的身体变化，每条写一句「它为什么是正常的」。",
            "用自己的话说一说：为什么每个人的节奏不一样，却都算正常？",
            "写出两句可以在不舒服时说出口的话，越短越好。",
        ],
        [
            "和家里的大人说一说：这一年你注意到的身体变化里，哪一件你一开始有点担心，现在明白了什么。",
            "练习一次拒绝：对着镜子把「我不太喜欢这样，可以请你……」说三遍，注意语气要平静。",
        ],
        [
            "找一找班里聊天里两三句拿别人身体变化开玩笑的话，把它们改成尊重人的说法，写下来。",
            "和同学讨论一次：在教室里一起做小组作业时，怎样的距离和说话方式让大家都觉得舒服？写出三条约定。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "psych-e-g6-puberty",
    "node_id": "psych-e-g6-puberty",
    "subject": "psychology",
    "subject_cn": "心理健康",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "中小学心理健康教育指导纲要（2012年修订）/ 教育部相关要求 · 小学",
    "title": "青春期的变化与同伴交往",
    "name_en": "Puberty, Personal Boundaries and Respectful Friendships",
    "grade": 6,
    "grade_cn": "六年级",
    "domain": "puberty-growth",
    "domain_cn": "青春期与成长",
    "lesson_type": "workshop",
    "version": "1.0.0",
    "description": "面向小学六年级的青春期教育课，只围绕三件适合这个年龄的事：① 身体变化的科学常识——身高体重的变化、嗓音与皮肤上的一些变化，都是身体在长大的记号，每个人都会经历；② 个人边界与身体自主权——我的身体我做主，别人的身体要先问一句，不愿意可以直接说；③ 同伴与异性交往的尊重与分寸感——自然大方、在公开场合、尊重对方的答复、不拿别人的身体变化开玩笑。三个互动台子都能真的操作：成长变化分类台（六张卡片分两栏，分错会说明它更合适放在哪里）、边界判断台（四个情境各三种做法，反馈一律写成「这样可能会……，还可以试试……」），以及综合任务里的分寸三问练习台（选情境 → 问三句「安全吗、舒服吗、对方愿意吗」 → 选第一步 → 展开后果 → 生成分寸提示卡）。全课不涉及任何性行为内容与身体接触细节，不使用任何临床诊断词汇，不贴标签；插图一律为中性抽象的成长箭头、简笔轮廓与几何符号，不含身体细节。",
    "tags": ["青春期", "身体变化", "边界与尊重", "同伴交往", "六年级", "青春期与成长"],
    "standard_ref": "《中小学心理健康教育指导纲要（2012年修订）· 小学中高年级》——开展初步的青春期教育，引导学生进行恰当的异性交往，建立和维持良好的异性同伴关系，扩大人际交往的范围；帮助学生正确认识自己的优缺点和兴趣爱好，在各种活动中悦纳自己。",
    "hero_question": "这一年身体开始变了，同学之间也开始不一样了——哪些变化是正常的？和同伴相处，怎样的距离刚刚好？",
    "hero_alt": "青春期变化与同伴交往知识结构图：身体在长大、每个人的节奏不一样、边界与尊重 三栏",
    "hero_caption": "青春期与成长：变化是正常的 · 每个人的节奏不一样 · 身体是我的，别人的要先问一句",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "身体上的变化，哪些是正常的？", "d": "长个子、嗓音、痘痘……有点担心，又不太好意思问", "v": "身体上的变化哪些是正常的"},
        {"t": "为什么同学之间开始不一样了？", "d": "有人长得快，有人还没动静，会不会是我有问题", "v": "为什么同学之间开始不一样了"},
        {"t": "和异性同学相处，怎么把握分寸？", "d": "想一起做事，又怕别人起哄", "v": "和异性同学相处怎么把握分寸"},
        {"t": "别人让我不舒服的时候，我该怎么开口？", "d": "想说「不愿意」，可又怕伤感情", "v": "别人让我不舒服的时候我该怎么开口"},
    ],
    "objectives": [
        "能说出青春期身体上常见的变化，知道这些变化每个人都会经历，是正常的",
        "能说出每个人的节奏不一样，早一点晚一点都在正常范围里，不给自己和同学贴标签",
        "能理解身体是属于自己的，遇到让自己不舒服的接触或玩笑时，可以清楚地说出「我不愿意」，并告诉信任的大人",
        "能说出和异性同伴交往的四条分寸：自然大方、在公开场合、尊重对方答复、不拿别人的身体变化开玩笑",
    ],
    "objectives_plain": [
        "能说出青春期身体上常见的变化，知道这些变化每个人都会经历，是正常的",
        "能说出每个人的节奏不一样，早一点晚一点都在正常范围里，不给自己和同学贴标签",
        "能理解身体是属于自己的，遇到让自己不舒服的接触或玩笑时，可以清楚地说出「我不愿意」，并告诉信任的大人",
        "能说出和异性同伴交往的四条分寸：自然大方、在公开场合、尊重对方答复、不拿别人的身体变化开玩笑",
    ],
    "standards": [
        {"content": "开展初步的青春期教育，引导学生进行恰当的异性交往，建立和维持良好的异性同伴关系，扩大人际交往的范围",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学中高年级"},
        {"content": "帮助学生正确认识自己的优缺点和兴趣爱好，在各种活动中悦纳自己",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学中高年级"},
    ],
    "prereqs": ["psych-e-g5-negative-emotion"],
    "prereqs_name": "面对挫折与情绪调节",
    "prereqs_meta": "psych-e-g5-negative-emotion",
    "leads_to": ["psych-e-g6-social-citizen"],
    "next_meta": "psych-e-g6-social-citizen",
    "section_images": ["assets/psych-e-g6-puberty-fig1.webp",
                       "assets/psych-e-g6-puberty-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "身体开始变了，心里也有了一些说不清的问题——这节课先把「什么是正常的」说清楚。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能说出三条常见变化，也能说出一句守住边界的话。",
        "objectives": "看清四件事：哪些变化正常、节奏为什么不一样、边界是什么、交往的分寸在哪里。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "长个子、体重、嗓音、小痘痘，都是身体在长大的记号；它们自己会发生，不需要你做什么。",
        "lab-1": "重点不是分得快，而是看看每一张为什么归那一栏——常见的变化和不一样的节奏，是两回事。",
        "module-2": "身体是我的，别人的身体要先问一句；不愿意就说出来，语气可以很平静。",
        "lab-2": "四个情境各三种做法，选完把反馈读一遍；它写的是「这样可能会……，还可以试试……」。",
        "worked-example": "小然四步：说清事情、分成两堆、套上分寸三条、给今天配一个做法。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "选情境 → 问三句 → 选第一步 → 看后果 → 生成分寸提示卡，走完一遍就有自己的办法了。",
        "posttest": "出现了长得快、同学变声、大人想抱你，看看你能不能守住自己的边界。",
        "summary": "三句话：变化是正常的、节奏各不相同、边界要守也要尊重。",
        "homework": "三层小任务，先做前两层；第二层可以请家里人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先帮你找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学心理健康「青春期与成长」在六年级的空缺，正对课标「开展初步的青春期教育，引导学生进行恰当的异性交往，建立和维持良好的异性同伴关系」与「在各种活动中悦纳自己」。六年级学生的真实难点有三个：① 身体开始变化，但没有人把话说明白，于是心里容易冒出「是不是只有我不正常」这样的结论；② 同伴之间开始不一样，容易拿别人的时间表当尺子，给自己或别人贴标签；③ 交往的分寸没有人示范过，既可能不敢开口，也可能把玩笑开过界。所以全课只讲三件适合这个年龄的事：概念一给出身体变化的科学常识（长个子、体重、嗓音、皮肤上的小变化），并明确「节奏不同不等于好坏」；概念二讲个人边界与身体自主权（我的身体我做主、别人的身体先问一句、说不愿意可以很平静）；例题与综合任务练与异性同伴交往的分寸四条（自然大方、在公开场合、尊重对方答复、不拿身体变化开玩笑）。三个台子都能真的操作：成长变化分类台（六张卡片分两栏，分错不放行并说明它更合适放在哪里）、边界判断台（四个情境各三种做法，反馈一律写成「这样可能会……，还可以试试……」），以及综合任务里的分寸三问练习台（选情境 → 问三句「安全吗、舒服吗、对方愿意吗」 → 选一个第一步 → 展开后果 → 生成分寸提示卡）。全课不涉及任何性行为内容与身体接触细节，不使用任何临床诊断词汇，不给学生贴标签；插图一律为中性抽象的成长箭头、简笔轮廓与几何符号，不含身体细节，也不使用真实照片风格人像。",
    "plan_table": """| 1 | cover | 青春期的变化与同伴交往 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 身体在长大，这些变化是正常的 | 承·概念一（身体变化的科学常识） |
| 6 | interactive | 动手一：分一分，哪些是常见的、哪些是节奏不同 | 承·分类台（六张卡片两栏） |
| 7 | concept | 身体是自己的：我的边界和别人的边界 | 承·概念二（边界与身体自主权） |
| 8 | interactive | 动手二：边界判断台，四种做法你选哪个 | 承·判断台（四情境 × 三做法） |
| 9 | concept | 例题示范：小然的板报小组 | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：分寸三问练习台，找到我的第一步 | 合·迁移应用（选情境 + 选第一步 + 生成提示卡） |
| 12 | quiz | 后测：换三个新情境，办法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，讲清长大的这件事 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：身体在长大 / 每个人的节奏不一样 / 边界与尊重 三栏\n- P5 成长变化示意图（已生成）：成长箭头与中性简笔轮廓表示身高、体重与嗓音的变化，附中文标注\n- P7 边界与尊重示意图（已生成）：两个圆圈、边界虚线与抽象符号，附中文标注\n- 三张图均为中性抽象教学插画（成长箭头、简笔轮廓、几何符号），不含身体细节，不使用真实照片风格人像\n- 若需补充：学校卫生室提供的青春期保健宣传页（需学校审核后使用）",
}
