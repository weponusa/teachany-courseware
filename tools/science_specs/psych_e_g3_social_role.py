# -*- coding: utf-8 -*-
"""小学心理健康 · 角色意识与时间管理（G3）—— 补齐知识树「生活适应」空缺

学科语气（心理健康）：温和、不评判、不贴标签；不出现任何临床诊断词汇，不涉及自伤自杀。
三年级落点：先在「教室里 / 在家里 / 在运动队里」把行为与角色对上（角色是位置，不是等级），
再把一天的事情按「必须做 / 想先做 / 可以等」排进时间格，排不下的时候实时看到撞车提示，
学会自己比较、自己挪一挪。

插图一律为中性简洁教学插画，不使用任何真实儿童照片风格人像。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/psych-e-g3-social-role-fig1.webp'
F2 = './assets/psych-e-g3-social-role-fig2.webp'

TTS = {
    "hero": "小朋友，想一想今天的你：早上在家里，你是家里的孩子；到了学校，你是班里的同学；放学去运动队，你又成了队里的一名队员。一个人，一天里会有好几个不同的身份，这些身份就叫角色。这节课我们做两件事：第一件，看看在不一样的地方，我这个角色该做什么；第二件，把一天要做的事情排进时间格，看看排不下、两件事撞在一起的时候，可以怎么办。",
    "problem-anchor": "开始之前，先选一个你最想弄清楚的问题。是想知道在不一样的场合我该做什么，还是想知道事情怎么分轻重，或者你想弄清楚两件事撞在一起该怎么办，再或者，你只想让自己的晚上不那么赶。选好了，就带着它往下看。",
    "objectives": "这节课有四个小目标。第一，能说出我在教室里、在家里、在运动队里分别是怎样的角色，以及这个角色该做的事。第二，知道角色是位置不同，不是等级高低，换一个地方就换一种做法。第三，能把一天的事情分成必须做、想先做、可以等三类。第四，两件事撞在一起的时候，能自己比较一下，把可以等的那件挪到别的时间。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先说角色。角色不是什么了不起的词，它说的就是：在一个地方，我站在哪个位置上，这个位置该做什么。在教室里，我是学生，该做的事是听讲、举手说想法、把自己的值日做完。在家里，我是家里的孩子，该做的事是把自己的事做好，也帮家里一点。在运动队里，我是队员，该做的事是听教练的安排、和队友配合。同一个人，三个地方，做的事情不一样，这很正常。还有一句要紧的话：角色是位置不同，不是等级高低。打扫卫生的、上课发言的、当队长的，都是在做这个位置上的事，没有谁比谁高一等。",
    "lab-1": "现在请你当一次角色配对员。下面有九件事，分别属于教室里、在家里、在运动队里。先点一件事，再点它应该在的地方。放好了，我会告诉你这个角色在这个位置上，到底该做什么。",
    "module-2": "再说时间。一天里要做的事情不少，它们不是一样重要的，可以分成三类。第一类叫必须做：今天不做，明天就会出问题，比如作业、明天的书包、睡觉前的刷牙。第二类叫想先做：不做难受，很想马上做，可是往后挪一点也不会出事，比如看动画片、练一会儿琴。第三类叫可以等：放到明天或者周末也完全可以，比如和爸爸下一盘棋。分好类以后，再把它们排进时间格：先给必须做的划格子，剩下的格子才给想先做的和可以等的。",
    "lab-2": "现在请你当一次自己一天的小排程员。下面有八件事，每一件你先判断它是哪一类：必须做、想先做，还是可以等。判断对了，才能把它放进时间格。每个时间格最多放两件事——放不下的时候我会马上提醒你，那时候就请你比一比，把可以等的那一件挪到别的时间去。",
    "worked-example": "我们一起来帮小舟想一想。周三放学回家，小舟把书包一放就想看动画片。可作业还没写，琴也没练，晚上还要刷牙、装第二天的书包。到了晚上九点，他还在赶作业，心里又急又累。第一步，他先把今天要做的事摊开写在纸上，一共六件。第二步，他分三类：必须做的是作业、装书包、刷牙洗脸；想先做的是练琴、看动画片；可以等的是和爸爸下棋。第三步，他先给必须做的划格子：作业放放学后，装书包和刷牙放晚饭后。第四步，他发现放学后想放的东西放不下了——作业已经占了一个格子，练琴和动画片都想要第二个。比一比，动画片可以放到周末，练琴先做。就这样，晚上九点他已经在收书包了。",
    "conceptest-1": "接下来用三个说法考考你，每一个里面都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件事交给你。请你选三样：我必须先做完的一件事、我很想先做但要等一等的一件事、我可以放到明天或周末的一件事。三样选好，我就送给你一张「我的一天小计划卡」。",
    "posttest": "最后一轮，换三个新的小情境来考考你。这次会出现：周末想踢球但作业没写、正看得入迷被叫去帮忙、训练和同学约好的手工撞在一起，看看你能不能用上今天的办法。",
    "summary": "这节课我们记住三句话。第一句，一个人会有好几个角色，角色是位置不同，不是等级高低。第二句，事情分三类：必须做、想先做、可以等，先给必须做的划格子。第三句，两件事撞在一起的时候，别慌，比一比——把可以等的那件挪到别的时间去。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写下我在教室里、在家里、在运动队或兴趣班里分别该做的一件事。第二层能力应用，动手做：把明天要做的事分成必须做、想先做、可以等三类，写下来。第三层迁移挑战，选做：画一张自己的时间格，把明天的事情排进去，晚上和家里人一起看看排得顺不顺，哪里可以改。",
    "knowledge-graph": "这张图展示了这节课在心理健康知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 在不同的地方，我是不同的角色", "lab-1": "动手一 角色配对台",
    "module-2": "概念二 一天的事情，可以分成三类", "lab-2": "动手二 我的时间格",
    "worked-example": "例题讲解 小舟的周三", "conceptest-1": "概念测试",
    "synthesis": "综合任务 做出我的一天小计划卡", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：角色配对（九件事 → 三个地方） ──
ROLE_PLACES = {
    "classroom": "在教室里",
    "home": "在家里",
    "team": "在运动队里",
}
ROLE_NAME = {
    "classroom": "我是班里的同学",
    "home": "我是家里的孩子",
    "team": "我是队里的队员",
}
ROLE_MEANING = {
    "classroom": "在教室里，我这个位置要做的是：听讲、有想法举手说、把自己的值日和小组里那一份做完。",
    "home": "在家里，我这个位置要做的是：自己的事情自己做，也帮家里一点，出门前跟家里人说一声。",
    "team": "在运动队里，我这个位置要做的是：听教练的安排、轮到自己就上、和队友一起把球打好。",
}
ROLE_ITEMS = [
    {"id": "r1", "t": "上课时认真听，有想法就举手说", "place": "classroom",
     "why": "这是学生这个位置最基本的一件：听，和说。"},
    {"id": "r2", "t": "小组讨论时，先听完别人说，再开口", "place": "classroom",
     "why": "在小组里，我是其中一员。先听完再说，讨论才做得下去。"},
    {"id": "r3", "t": "值日的时候，把自己那一块做完", "place": "classroom",
     "why": "值日分好工，每个人做完自己那一块，教室就是干净的。"},
    {"id": "r4", "t": "吃完饭把自己的碗端到厨房", "place": "home",
     "why": "在家里的位置，就是自己能做的事自己做。"},
    {"id": "r5", "t": "出门前跟家里人说一声去哪里", "place": "home",
     "why": "在家里，我做的事家里人会牵挂。说一声，是让家里人放心。"},
    {"id": "r6", "t": "周末帮家里做一件家务，比如擦桌子", "place": "home",
     "why": "这个家不是只有大人要做事。我做一点，家里就轻一点。"},
    {"id": "r7", "t": "训练时按教练说的做，轮到自己就上", "place": "team",
     "why": "队员这个位置，首先要跟大家一起往前走，而不是自己一个人走。"},
    {"id": "r8", "t": "队友失误了，过去拍拍他的肩膀", "place": "team",
     "why": "队里的位置不是一个人的位置。队友低落的时候，一句话就很有用。"},
    {"id": "r9", "t": "比赛输了，和队友一起看哪里可以改", "place": "team",
     "why": "输了一场，队还在。一起看问题，就是队员做的事。"},
]

# ── 动手二：时间格排程（八件事 → 三类 → 四个时间格） ──
KINDS = {
    "must": "必须做",
    "should": "想先做",
    "can": "可以等",
}
KIND_RULE = {
    "must": "今天不做，明天就会出问题——这一类就是必须做。",
    "should": "不做心里难受，很想马上做，可往后挪一点也不出事——这一类是想先做。",
    "can": "放到明天、放到周末也完全可以——这一类是可以等。",
}
SLOTS = {
    "morning": "早上出门前",
    "school": "白天在学校",
    "after": "放学后到晚饭前",
    "night": "晚饭后到睡觉前",
}
SLOT_CAP = 2
TASKS = [
    {"id": "t1", "t": "把今天的作业写完", "kind": "must", "slot": "after"},
    {"id": "t2", "t": "练20分钟琴", "kind": "should", "slot": "after"},
    {"id": "t3", "t": "看一集动画片", "kind": "should", "slot": "after"},
    {"id": "t4", "t": "上课认真听，把重点圈出来", "kind": "must", "slot": "school"},
    {"id": "t5", "t": "课间和同学玩一会儿", "kind": "can", "slot": "school"},
    {"id": "t6", "t": "把明天要带的书和文具装进书包", "kind": "must", "slot": "night"},
    {"id": "t7", "t": "刷牙洗脸再睡觉", "kind": "must", "slot": "night"},
    {"id": "t8", "t": "和爸爸下一盘棋", "kind": "can", "slot": "night"},
]

# ── 综合任务：我的一天小计划卡（三栏各选一样） ──
DAY_CARD = {
    "must": {
        "name": "① 我必须先做完的一件事",
        "items": [
            {"id": "m1", "t": "把今天的作业写完"},
            {"id": "m2", "t": "把明天要带的书装进书包"},
            {"id": "m3", "t": "洗脸刷牙，按时睡觉"},
            {"id": "m4", "t": "把明天课上要用的东西准备好"},
        ],
    },
    "should": {
        "name": "② 我很想先做、但要等一等的一件事",
        "items": [
            {"id": "s1", "t": "看一集动画片"},
            {"id": "s2", "t": "练一会儿琴"},
            {"id": "s3", "t": "和同学在楼下玩一会儿"},
            {"id": "s4", "t": "把没看完的那本故事书看完"},
        ],
    },
    "can": {
        "name": "③ 我可以放到明天或周末的一件事",
        "items": [
            {"id": "c1", "t": "和爸爸下一盘棋"},
            {"id": "c2", "t": "做一个新的小手工"},
            {"id": "c3", "t": "整理书桌的抽屉"},
            {"id": "c4", "t": "给远方的朋友写一张小卡片"},
        ],
    },
}

CUSTOM_JS = r"""
/* ============================================================
   psych-e-g3-social-role 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 角色配对台：九件事 → 教室里 / 在家里 / 在运动队里
   3) 时间格排程器：先分三类，再排进四个时间格；放不下时实时撞车提示
   4) 我的一天小计划卡：三栏各选一样，拼成一张卡
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

  /* ---------- 2. 角色配对台 ---------- */
  var RITEMS = __RITEMS_JSON__;
  var RNAME = __RNAME_JSON__;
  var RMEAN = __RMEAN_JSON__;
  var roleStage = document.getElementById('role-stage');
  if (roleStage) {
    var pickedR = null, placedR = {};
    var outR = document.getElementById('role-out');

    function roleById(id) {
      for (var i = 0; i < RITEMS.length; i++) { if (RITEMS[i].id === id) return RITEMS[i]; }
      return null;
    }
    function renderR() {
      document.querySelectorAll('[data-roleitem]').forEach(function (b) {
        var k = b.dataset.roleitem;
        b.classList.toggle('selected', k === pickedR);
        b.classList.toggle('done', !!placedR[k]);
        b.disabled = !!placedR[k];
      });
      ['classroom', 'home', 'team'].forEach(function (pl) {
        var box = document.getElementById('role-box-' + pl);
        if (!box) return;
        box.innerHTML = '';
      });
      RITEMS.forEach(function (r) {
        if (!placedR[r.id]) return;
        var box = document.getElementById('role-box-' + r.place);
        var d = document.createElement('div');
        d.className = 'tag';
        d.style.display = 'block';
        d.style.margin = '4px 0';
        d.textContent = r.t;
        box.appendChild(d);
      });
      ['classroom', 'home', 'team'].forEach(function (pl) {
        var box = document.getElementById('role-box-' + pl);
        if (box && !box.innerHTML) {
          box.innerHTML = '<span style="color:var(--muted);font-size:13px">还空着。</span>';
        }
      });
      document.getElementById('role-score').textContent = '已经放好 ' + Object.keys(placedR).length + ' / ' + RITEMS.length + ' 件事';
    }
    document.querySelectorAll('[data-roleitem]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (placedR[b.dataset.roleitem]) return;
        pickedR = b.dataset.roleitem;
        outR.className = 'result warn';
        outR.innerHTML = '<strong>「' + b.textContent + '」</strong><br>想一想，这件事我是在哪里、以什么身份做的？';
        renderR();
      });
    });
    document.querySelectorAll('[data-roleplace]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pickedR) {
          outR.className = 'result warn';
          outR.textContent = '先在上面点一件事，再点它所在的地方。';
          return;
        }
        var r = roleById(pickedR);
        var pl = b.dataset.roleplace;
        if (pl !== r.place) {
          outR.className = 'result warn';
          outR.innerHTML = '<strong>再想一想「' + r.t + '」。</strong>' + r.why +
            '<br><span style="color:var(--muted)">常见错误：容易把「在教室里的做法」和「在运动队里的做法」搞混。问自己一句：这件事发生的时候，我旁边站着的是同学、家里人，还是队友？</span>';
          return;
        }
        placedR[r.id] = pl;
        outR.className = 'result';
        outR.innerHTML = '<strong>放对了。</strong>' + r.why + '<br>' + RMEAN[pl];
        pickedR = null;
        renderR();
        if (Object.keys(placedR).length === RITEMS.length) {
          outR.className = 'result';
          outR.innerHTML = '<strong>九件都放好了。</strong>同一个人，在教室里、在家里、在运动队里做的事不一样，' +
            '因为我的<strong>角色</strong>不一样。<br>再说一句要紧的话：角色是位置不同，不是等级高低——每个位置上的事都值得做好。';
        }
      });
    });
    renderR();
  }

  /* ---------- 3. 时间格排程器 ---------- */
  var TASKS = __TASKS_JSON__;
  var KINDS = __KINDS_JSON__;
  var SLOTS = __SLOTS_JSON__;
  var CAP = __CAP__;
  var schedStage = document.getElementById('sched-stage');
  if (schedStage) {
    var pickedT = null, kindOf = {}, slotOf = {}, clashes = 0;
    var outT = document.getElementById('sched-out');

    function taskById(id) {
      for (var i = 0; i < TASKS.length; i++) { if (TASKS[i].id === id) return TASKS[i]; }
      return null;
    }
    function slotIds(sl) {
      var arr = [];
      TASKS.forEach(function (t) { if (slotOf[t.id] === sl) arr.push(t.id); });
      return arr;
    }
    function renderT() {
      document.querySelectorAll('[data-task]').forEach(function (b) {
        var k = b.dataset.task;
        b.classList.toggle('selected', k === pickedT);
        b.classList.toggle('done', !!slotOf[k]);
        b.textContent = (kindOf[k] ? '[' + KINDS[kindOf[k]] + '] ' : '[还没分类] ') +
          taskById(k).t + (slotOf[k] ? ' → ' + SLOTS[slotOf[k]] : '');
      });
      document.querySelectorAll('[data-kind]').forEach(function (b) {
        var k = b.dataset.kind;
        var n = 0;
        TASKS.forEach(function (t) { if (kindOf[t.id] === k) n++; });
        var lab = document.getElementById('kind-lab-' + k);
        if (lab) lab.textContent = '（' + n + ' 件）';
        b.classList.toggle('selected', pickedT && kindOf[pickedT] === k);
      });
      Object.keys(SLOTS).forEach(function (sl) {
        var box = document.getElementById('slot-' + sl);
        if (!box) return;
        box.innerHTML = '';
        slotIds(sl).forEach(function (id) {
          var sp = document.createElement('span');
          sp.className = 'tag';
          sp.style.display = 'block';
          sp.style.margin = '4px 0';
          sp.style.cursor = 'pointer';
          sp.textContent = taskById(id).t + '　（点一下取回）';
          sp.addEventListener('click', function () {
            delete slotOf[id];
            outT.className = 'result warn';
            outT.innerHTML = '<strong>已经取回「' + taskById(id).t + '」。</strong>再比一比：它和这一格里别的哪一件撞了？把可以等的那件挪到别的时间去。';
            renderT();
          });
          box.appendChild(sp);
        });
        if (!box.innerHTML) {
          box.innerHTML = '<span style="color:var(--muted);font-size:13px">空着，最多能放 ' + CAP + ' 件。</span>';
        }
      });
      var nPlaced = Object.keys(slotOf).length;
      document.getElementById('sched-score').textContent = '已经排进时间格 ' + nPlaced + ' / ' + TASKS.length + ' 件';
      document.getElementById('sched-clash').textContent = '撞车 ' + clashes + ' 次';
      if (nPlaced === TASKS.length) {
        outT.className = 'result';
        outT.innerHTML = '<strong>八件事都排进去了。</strong>回头看看你的时间格：<strong>必须做的事，先把格子占住了；' +
          '剩下的格子，才轮得到想先做的和可以等的。</strong>这就是时间管理最要紧的一步。';
      }
    }
    document.querySelectorAll('[data-task]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (slotOf[b.dataset.task]) return;
        pickedT = b.dataset.task;
        var t = taskById(pickedT);
        if (kindOf[pickedT]) {
          outT.className = 'result warn';
          outT.innerHTML = '<strong>「' + t.t + '」已经分好类：' + KINDS[kindOf[pickedT]] + '。</strong>现在点一个时间格，把它排进去（每格最多 ' + CAP + ' 件）。';
        } else {
          outT.className = 'result warn';
          outT.innerHTML = '<strong>「' + t.t + '」</strong><br>它属于哪一类？先点一个标签：必须做、想先做，还是可以等。';
        }
        renderT();
      });
    });
    document.querySelectorAll('[data-kind]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pickedT) {
          outT.className = 'result warn';
          outT.textContent = '先在上面点一件事，再给它选一个标签。';
          return;
        }
        var t = taskById(pickedT);
        var k = b.dataset.kind;
        if (kindOf[t.id] && kindOf[t.id] !== k) {
          outT.className = 'result warn';
          outT.innerHTML = '<strong>「' + t.t + '」刚才已经分在「' + KINDS[kindOf[t.id]] + '」了。</strong>再想一想：今天不做，明天会不会出问题？';
          return;
        }
        if (k !== t.kind) {
          outT.className = 'result warn';
          outT.innerHTML = '<strong>再想一想「' + t.t + '」。</strong>' + KIND_RULE[t.kind] +
            '<br><span style="color:var(--muted)">常见错误：容易把「很想做的事」当成「必须做的事」——问自己三句：今天不做明天会不会出问题？不做会不会一直想着？晚一点做影响大不大？</span>';
          return;
        }
        kindOf[t.id] = k;
        outT.className = 'result';
        outT.innerHTML = '<strong>分类对了：' + KINDS[k] + '。</strong>' + KIND_RULE[k] + '<br>接着点一个时间格，把它排进去。';
        renderT();
      });
    });
    document.querySelectorAll('[data-slot]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pickedT) {
          outT.className = 'result warn';
          outT.textContent = '先在上面点一件事，再点时间格。';
          return;
        }
        var t = taskById(pickedT);
        if (!kindOf[t.id]) {
          outT.className = 'result warn';
          outT.textContent = '先给「' + t.t + '」选一个标签，再排时间。';
          return;
        }
        var sl = b.dataset.slot;
        var ids = slotIds(sl);
        if (ids.length >= CAP) {
          clashes++;
          outT.className = 'result error';
          outT.innerHTML = '<strong>⚠️ 撞车了：「' + SLOTS[sl] + '」这一格已经有两件事了。</strong><br>' +
            '现在这一格里是：' + ids.map(function (x) { return '「' + taskById(x).t + '」'; }).join('') +
            '，再加上你手上的「' + t.t + '」，三件事挤在同一段时间，做不完，也做不好。<br>' +
            '<span style="color:var(--muted)">怎么办：比一比这三件——哪一件是<strong>可以等</strong>的？先把它取回来（点一下那一格里的卡片），放到别的时间格去，再排这一件。</span>';
          renderT();
          return;
        }
        slotOf[t.id] = sl;
        var after = slotIds(sl).length;
        outT.className = 'result';
        outT.innerHTML = '<strong>排好了：「' + t.t + '」放进「' + SLOTS[sl] + '」（' + after + '/' + CAP + ' 件）。</strong>' +
          (after === CAP ? '<br><span style="color:var(--muted)">这一格满了，再想往这里放就会撞车——记住这句话：必须做的先占格子。</span>' : '');
        pickedT = null;
        renderT();
      });
    });
    renderT();
  }

  /* ---------- 4. 我的一天小计划卡 ---------- */
  var DAYC = __DAYC_JSON__;
  var planStage = document.getElementById('plan-stage');
  if (planStage) {
    var chosenP = {}, colsP = ['must', 'should', 'can'];
    var outP = document.getElementById('plan-out');

    function txtP(col, id) {
      var arr = DAYC[col].items;
      for (var i = 0; i < arr.length; i++) { if (arr[i].id === id) return arr[i].t; }
      return '';
    }
    function renderP() {
      colsP.forEach(function (col) {
        document.querySelectorAll('[data-plan="' + col + '"]').forEach(function (b) {
          b.classList.toggle('selected', chosenP[col] === b.dataset.planId);
        });
        var slot = document.getElementById('plan-pick-' + col);
        if (slot) {
          slot.textContent = chosenP[col] ? txtP(col, chosenP[col]) : '还没有选';
          slot.style.color = chosenP[col] ? 'var(--text)' : 'var(--muted)';
        }
      });
      var n = colsP.filter(function (c) { return chosenP[c]; }).length;
      document.getElementById('plan-score').textContent = '计划卡完成 ' + n + ' / 3 项';
      if (n === 3) {
        outP.className = 'result';
        outP.innerHTML = '<strong>我的一天小计划卡：</strong>我必须先做完「' + txtP('must', chosenP.must) +
          '」；我很想先做「' + txtP('should', chosenP.should) + '」，不过要等一等；「' + txtP('can', chosenP.can) +
          '」可以放到明天或者周末。<br><span style="color:var(--muted)">把这张卡念给同桌听，请他帮你看一眼：三件事排的顺序对不对。</span>';
      } else {
        outP.className = 'result warn';
        outP.textContent = '三栏各选一样，计划卡就做好了。';
      }
    }
    colsP.forEach(function (col) {
      document.querySelectorAll('[data-plan="' + col + '"]').forEach(function (b) {
        b.addEventListener('click', function () {
          chosenP[col] = b.dataset.planId;
          renderP();
        });
      });
    });
    renderP();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__RITEMS_JSON__', json.dumps(ROLE_ITEMS, ensure_ascii=False))
             .replace('__RNAME_JSON__', json.dumps(ROLE_NAME, ensure_ascii=False))
             .replace('__RMEAN_JSON__', json.dumps(ROLE_MEANING, ensure_ascii=False))
             .replace('__TASKS_JSON__', json.dumps(TASKS, ensure_ascii=False))
             .replace('__KINDS_JSON__', json.dumps(KINDS, ensure_ascii=False))
             .replace('__SLOTS_JSON__', json.dumps(SLOTS, ensure_ascii=False))
             .replace('__CAP__', str(SLOT_CAP))
             .replace('__DAYC_JSON__', json.dumps(DAY_CARD, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "下面哪一件事，是「在运动队里」该做的？",
         "options": [("训练时按教练说的做，和队友一起把球打好", True),
                     ("上课时认真听，有想法举手说", False),
                     ("吃完饭把自己的碗端到厨房", False)],
         "explain": "同一件事，换个地方就不一样。在运动队里，我是队员，位置上的事就是配合和服从安排。"
                    "<strong>错因提醒：</strong>常见错误是把「在教室里的做法」和「在运动队里的做法」搞混——先想清楚我旁边站着的是同学、家里人，还是队友。"},
        {"q": "下面哪一件属于「必须做」？",
         "options": [("把今天的作业写完——今天不交，明天就会出问题", True),
                     ("看一集动画片——很想马上看", False),
                     ("和爸爸下一盘棋——他很想和我下", False)],
         "explain": "判断「必须做」，看的是：今天不做，明天会不会出问题。会的，就是必须做。"
                    "<strong>错因提醒：</strong>容易把「很想做的事」当成「必须做的事」——想做是心里的急，必须做是事情本身的期限。"},
        {"q": "放学后想看书、想练琴、还想看动画片，可时间只够两件。下面哪个做法更合适？",
         "options": [("把最必须的一件先定下来，再比一比剩下的哪件可以等", True),
                     ("哪件最想看就先做哪件", False),
                     ("三件都做，晚一点睡也没关系", False)],
         "explain": "时间格就那么大，先放必须做的，剩下的再比较——这就是排时间最核心的一步。"
                    "<strong>错因提醒：</strong>有人误认为「时间管理就是抓紧每一分钟」——其实它是先定住必须做的，再安心地玩。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "在不同的地方，我是不同的角色", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">上一节课我们认识了自己：喜欢什么、擅长什么（And）；可是同一个我，早上在家里、白天在教室里、下午在运动队里，要做的事却不一样，有的同学会因此觉得「我到底该听谁的」（But）；所以这节课先把「角色」这件事说清楚——角色就是我在一个地方站的位置，位置不同，该做的事就不同（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px"><strong>角色</strong>说的就是：在某个地方，我站在哪个位置上，这个位置该做什么。一个人一天里会有好几个角色。</p>
        <div class="grid grid-3">
          <div class="inner-card">
            <p><strong>在教室里</strong></p>
            <p style="color:var(--muted)">我是班里的同学：听讲、有想法举手说、和小组一起把事做完。</p>
          </div>
          <div class="inner-card">
            <p><strong>在家里</strong></p>
            <p style="color:var(--muted)">我是家里的孩子：自己的事自己做，也帮家里一点，出门前说一声。</p>
          </div>
          <div class="inner-card">
            <p><strong>在运动队里</strong></p>
            <p style="color:var(--muted)">我是队里的队员：听教练安排、轮到自己就上、和队友配合。</p>
          </div>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先问「我在哪」：</strong>这一个地方是什么地方？我身边站着谁？</div></div>
          <div class="step"><span class="n">2</span><div><strong>再问「我在这里是谁」：</strong>是同学、是家里的孩子，还是队里的队员？</div></div>
          <div class="step"><span class="n green">3</span><div><strong>最后问「这个位置该做什么」：</strong>想清楚这一句，就不用再纠结该听谁的。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="三个场景的角色示意图：教室里是同学、在家里是孩子、在运动队里是队员，各自标注该做的事">
          <figcaption>示意图：同一个人，三个地方，三个角色——位置不同，该做的事就不同（教学示意图，中性简洁插画）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「角色是分高低的：队长比队员高，说话的比听讲的高」。其实角色是<strong>位置不同</strong>，不是等级高低。同一个队里，前锋和守门员做的事不一样，缺了谁都打不成一场球；教室里，打扫的、发言的、收作业的，都是在做自己位置上的一件事。<strong>做事可以不一样，人是一样的。</strong></p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "有的同学在家里很放松，一到教室就不敢说话。这不是他变了，是他换了一个位置，还在找这个位置上的做法，慢慢来就好。"},
    {"lens": "比较它", "text": "同样一句「大声说话」：在运动队里，喊出来是应该的；在教室里，就需要放轻一点。同一件事，位置不同，做法就不同。"},
    {"lens": "迁移它", "text": "这个想法以后还能用：坐公交车是乘客，去商店是顾客，进了图书馆是读者。先问「我在哪」，就知道该怎么做。"},
])}
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>换个地方换个位置——<strong>角色是位置不同，不是等级高低。</strong></div></div>
    ''', tag="概念一"))

    role_btns = "\n".join(
        f'            <button class="choice" data-roleitem="{r["id"]}" style="text-align:left">{r["t"]}</button>'
        for r in ROLE_ITEMS
    )
    place_btns = "\n".join(
        f'            <button class="choice" data-roleplace="{pl}" style="text-align:center">{ROLE_PLACES[pl]}</button>'
        for pl in ("classroom", "home", "team")
    )
    role_boxes = "\n".join(
        f'''            <div class="sort-bin">
              <h4>{ROLE_PLACES[pl]}　<span style="color:var(--muted);font-weight:400">{ROLE_NAME[pl]}</span></h4>
              <div id="role-box-{pl}"><span style="color:var(--muted);font-size:13px">还空着。</span></div>
            </div>'''
        for pl in ("classroom", "home", "team")
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：角色配对台，九件事找地方", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">点一件事，再点它所在的地方。<strong>放好了我会告诉你：在这个位置上，我到底该做什么。</strong></p>
        <div class="lab-panel" id="role-stage">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 九件事（点一件）</div>
          <div class="grid" id="role-bank">
{role_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 它发生在哪里（点一个地方）</div>
          <div class="grid grid-3">
{place_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">③ 我在这里是谁</div>
          <div class="sort-bins" style="grid-template-columns:1fr">
{role_boxes}
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">配对进度</span><span class="v" id="role-score">已经放好 0 / 9 件事</span></div>
          </div>
          <p class="result warn" id="role-out" style="margin-top:12px">先在上面点一件事。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧭</span><div><strong>拿不准的时候问自己一句：</strong>这件事发生的时候，我旁边站着的是<strong>同学、家里人，还是队友</strong>？想清楚这一句，位置就出来了。</div></div>
    ''', tag="动手一", bloom="apply"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "一天的事情，可以分成三类", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">一天里要做的事不少，它们<strong>不是一样重要的</strong>。先把它们分成三类，再排时间，就顺多了。</p>
        <div class="grid grid-3">
          <div class="inner-card" style="border-top:4px solid var(--brand)">
            <p><strong>必须做</strong></p>
            <p style="color:var(--muted)">今天不做，明天就会出问题。比如作业、明天的书包、睡觉前的刷牙。</p>
          </div>
          <div class="inner-card" style="border-top:4px solid var(--brand-2)">
            <p><strong>想先做</strong></p>
            <p style="color:var(--muted)">不做心里难受，很想马上做，但往后挪一点也不出事。比如看动画片、练一会儿琴。</p>
          </div>
          <div class="inner-card" style="border-top:4px solid var(--warm)">
            <p><strong>可以等</strong></p>
            <p style="color:var(--muted)">放到明天、放到周末也完全可以。比如下一盘棋、整理抽屉。</p>
          </div>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>三句判据：</strong>今天不做，明天会不会出问题？不做，心里会不会一直想着？晚一点做，影响大不大？</div></div>
          <div class="step"><span class="n">2</span><div><strong>必须做的先占格子：</strong>把一天分成几个时间段，先把必须做的划进去，别的事不许挤进来。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>撞车了就比一比：</strong>两件事撞在同一段时间，问问「哪一件是可以等的」，把它挪到别的时间。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="时间格示意图：一天分成四个时间段，必须做的事情先占格子，其余按想先做和可以等排入">
          <figcaption>示意图：一天分成几个时间格，必须做的事先占住格子，剩下的格子才给想先做的和可以等的（教学示意图，中性简洁插画）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「时间管理就是把想玩的事全都砍掉，只留学习」。其实不是——它是<strong>把必须做的先安排好，剩下的时间就可以安心地玩</strong>。真正让人累的，不是玩了一会儿，而是玩的时候心里一直悬着没写完的作业。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "晚上赶作业的时候，人又急又累，写出来的字也不好看——这不是你不够努力，是把必须做的放在了最后。"},
    {"lens": "拆开它", "text": "把「我今天好忙」拆成一张清单：一共几件？哪几件必须做？常常会发现，真正必须做的只有两三件。"},
    {"lens": "迁移它", "text": "这个办法也能用在周末和假期：先把必须做的划出来，剩下的时间自己安排，玩起来也踏实。"},
])}
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>必须做的先占格子，剩下的才轮到想做的——<strong>撞车了就比一比，哪件可以等。</strong></div></div>
    ''', tag="概念二"))

    task_btns = "\n".join(
        f'            <button class="choice" data-task="{t["id"]}" style="text-align:left">[还没分类] {t["t"]}</button>'
        for t in TASKS
    )
    kind_btns = "\n".join(
        f'''            <button class="choice" data-kind="{k}" style="text-align:center">{KINDS[k]}<span id="kind-lab-{k}" style="color:var(--muted);font-weight:400"></span></button>'''
        for k in ("must", "should", "can")
    )
    slot_boxes = "\n".join(
        f'''          <div class="inner-card" style="margin:0">
            <p><strong>{SLOTS[sl]}</strong></p>
            <button class="choice" data-slot="{sl}" style="text-align:center;margin:6px 0">把手上这件事放进这一格</button>
            <div id="slot-{sl}"><span style="color:var(--muted);font-size:13px">空着，最多能放 2 件。</span></div>
          </div>'''
        for sl in ("morning", "school", "after", "night")
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：我的时间格，放不下会提醒你", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一件事，给它选一个标签（必须做 / 想先做 / 可以等）；分好类以后，再点一个时间格把它排进去。<strong>每格最多放 2 件</strong>，放不下的时候我会马上提醒你。</p>
        <div class="lab-panel" id="sched-stage">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 今天要做的八件事（点一件）</div>
          <div class="grid" id="task-bank">
{task_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 它是哪一类（点一个标签）</div>
          <div class="grid grid-3">
{kind_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">③ 排进时间格（点一格放进）</div>
          <div class="grid grid-2">
{slot_boxes}
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">排程进度</span><span class="v" id="sched-score">已经排进时间格 0 / 8 件</span></div>
            <div class="readout-cell"><span class="k">撞车次数</span><span class="v" id="sched-clash">撞车 0 次</span></div>
          </div>
          <p class="result warn" id="sched-out" style="margin-top:12px">先在上面点一件事。</p>
        </div>
        <div class="lab-panel" style="margin-top:14px">
          <p style="margin:0"><strong>如果撞车了，这样做：</strong></p>
          <div class="step-grid">
            <div class="step"><span class="n">1</span><div>看清楚撞在一起的是哪几件。</div></div>
            <div class="step"><span class="n">2</span><div>在它们中间找<strong>可以等</strong>的那一件。</div></div>
            <div class="step"><span class="n green">3</span><div>点一下那一格里的事，把它取回来，放到空着的时间格去。</div></div>
          </div>
        </div>
    ''', tag="动手二", bloom="apply"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小舟的周三", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>周三放学回家，小舟把书包一放就想看动画片。可作业还没写，琴也没练，晚上还要刷牙、装第二天的书包。到了晚上九点，他还在赶作业，心里又急又累。请你陪他走四步。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>把今天的事摊开：</strong>写在纸上数一数，一共六件。写出来，心就不那么乱了。</div></div>
          <div class="step"><span class="n">2</span><div><strong>分三类：</strong>必须做——作业、装书包、刷牙洗脸；想先做——练琴、看动画片；可以等——和爸爸下棋。</div></div>
          <div class="step"><span class="n">3</span><div><strong>先给必须做的划格子：</strong>作业放「放学后」，装书包和刷牙放「晚饭后」。这两格先占住，别的事不许挤。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>撞车了，比一比：</strong>放学后只剩一个格子，练琴和动画片都想要。动画片可以放到周末，练琴先做——问题就解决了。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「排时间就是把想玩的事全都划掉」。小舟这四步里，动画片并没有被划掉，它只是被挪到了周末——<strong>排时间不是不让你玩，是让你玩的时候心里不悬着。</strong></p>
        </div>
        <div class="inner-card">
          <p><strong>说给同桌听：</strong>想想你昨天放学后到睡觉前这一段。把它按这四步排一遍，说给同桌听，请他帮你看一眼：哪一件事其实可以等，两件都想做的时候哪个更合适。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "下面哪一句说得对？",
         "options": [("角色是位置不同，不是等级高低", True),
                     ("当队长的人比队员高一等", False),
                     ("打扫卫生的角色不如上课发言的角色", False)],
         "explain": "每个位置上都有自己的事，缺了谁都做不成一件事。位置不一样，人是一样的。"
                    "<strong>错因提醒：</strong>常见错误是把「分工不同」和「高低不同」搞混——分工说的是事情，不是人的价值。"},
        {"q": "明天要交的作业还没写完，我很想先看动画片。下面哪个做法更合适？",
         "options": [("先写作业，写完再看一会儿，心里踏实", True),
                     ("先看动画片，作业晚一点再说", False),
                     ("一边看动画片一边写作业", False)],
         "explain": "必须做的事先占住时间，之后玩起来才安心。两件事同时做，常常两件都做不好。"
                    "<strong>错因提醒：</strong>容易把「很想做的事」当成「必须先做的事」——想做是心里的急，必须做是事情的期限。"},
        {"q": "我给自己排了时间表：放学后写作业、练琴、看书，一样都没排玩的时间。结果两天都没做到。问题在哪里？",
         "options": [("排得太满了，没有留出可以等的时间，也没有留出休息", True),
                     ("我太懒了，说话不算数", False),
                     ("时间表根本没用，不用排", False)],
         "explain": "排时间要留出空档，不然第一件拖了，后面全崩。留一点玩的时间，计划才走得下去。"
                    "<strong>错因提醒：</strong>有人误认为「做到不计划就是自己不够自觉」——大多数时候不是不够自觉，是计划本身排得太满。"}
    ], tag="概念测试"))

    plan_blocks = []
    for col in ("must", "should", "can"):
        btns = "\n".join(
            f'              <button class="choice" data-plan="{col}" data-plan-id="{it["id"]}" style="text-align:left">{it["t"]}</button>'
            for it in DAY_CARD[col]["items"]
        )
        plan_blocks.append(f'''          <div class="inner-card">
            <p><strong>{DAY_CARD[col]["name"]}</strong>　<span style="color:var(--muted);font-size:13px">已选：</span><span id="plan-pick-{col}" style="color:var(--muted)">还没有选</span></p>
            <div class="grid" style="margin-top:8px">
{btns}
            </div>
          </div>''')
    plan_html = "\n".join(plan_blocks)
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：做出我的一天小计划卡", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">三栏各选一样，就做好了你的<strong>一天小计划卡</strong>。这一张卡只写明天真正做得到的事，不用排得太满。</p>
        <div class="lab-panel" id="plan-stage">
{plan_html}
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">计划卡进度</span><span class="v" id="plan-score">计划卡完成 0 / 3 项</span></div>
          </div>
          <p class="result warn" id="plan-out" style="margin-top:12px">三栏各选一样，计划卡就做好了。</p>
        </div>
        <div class="inner-card">
          <p><strong>再写一句给明天的话：</strong></p>
          <p style="color:var(--muted)">这句话的开头是「如果两件事撞在一起，我会……」，把它写完。</p>
          <textarea id="syn-answer" rows="3" placeholder="如果两件事撞在一起，我会先看看哪一件可以等，然后……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换三个新情境，办法还在不在", TTS["posttest"], [
        {"q": "周末上午，我很想和小伙伴去踢球，可作业还没写。下面哪个做法更合适？",
         "options": [("先把作业写完再出去，或者约定下午再踢", True),
                     ("先去踢球，作业晚上再说", False),
                     ("一边踢球一边想着作业，两边都不痛快", False)],
         "explain": "必须做的事先定下来，玩的时候才能真正放松。定一个时间点，比一直悬着舒服得多。"
                    "<strong>错因提醒：</strong>常见错误是把「玩」和「必须做」当成对立的——先做必须做的，玩反而是你的奖品。"},
        {"q": "我正在看一本很好看的书，妈妈喊我去帮忙摆碗筷。下面哪个做法更合适？",
         "options": [("先记下看到哪里，去帮忙，回来接着看", True),
                     ("假装没听见，继续看", False),
                     ("大声说：你别烦我", False)],
         "explain": "在家里，我是这个家的孩子。帮忙只要两分钟，回来书还是那本书，心情却不一样了。"
                    "<strong>错因提醒：</strong>容易误认为「书看到一半不能停」——真正停下来的是书页，不是你和家里人的关系。"},
        {"q": "队里周四要训练，可我早就和同学约好周四一起做手工。两件撞在一起了，怎么办？",
         "options": [("先看看哪一件能改时间，改不了就提前跟一边说清楚", True),
                     ("两边都不去，谁也不得罪", False),
                     ("先去训练，手工那件事不管了，也不用说", False)],
         "explain": "撞车的时候，能做的是「比较 + 说明」。改不了的那一件，提前告诉对方一声，事情就不会烂在手里。"
                    "<strong>错因提醒：</strong>有人误认为「撞车了只能放弃一件、不用解释」——一句话的说明，常常比硬扛更管用。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，讲清角色和时间这件事", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>一个人有好几个角色：</strong>在教室里是同学，在家里是孩子，在运动队里是队员；角色是位置不同，不是等级高低。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>事情分三类：</strong>必须做、想先做、可以等；必须做的先占格子。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>撞车了就比一比：</strong>找出可以等的那一件，把它挪到别的时间去。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>还要记牢一件事：</strong>计划排了没做到，不代表你说话不算数。改一改再排，比骂自己有用得多——排时间这件事，本来就是越排越准的。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「角色、必须做、撞车」这三个词，说一说你昨天放学后的那段时间。</p>
          <p style="color:var(--muted)">再动一动手：<strong>画出</strong>你的四个时间格，把明天的事写成小纸条贴进去，晚上自己检查一遍。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写下我在教室里、在家里、在运动队或兴趣班里分别该做的一件事。",
            "把下面三件事分一分：今天要交的作业、想看的动画片、想和爸爸下的棋。",
        ],
        [
            "把明天要做的事分成必须做、想先做、可以等三类，写在一张纸上。",
            "把「撞车了就比一比」用在一件真实的事上：记下一次撞车，写出你最后挪走了哪一件，为什么挪它。",
        ],
        [
            "画一张自己的时间格，把明天的事情排进去，晚上和家里人一起看看排得顺不顺，哪里可以改。",
            "采访家里的一位大人：他一天里要做哪几件必须做的事？他是怎么排的？写下你发现的一招。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "psych-e-g3-social-role",
    "node_id": "psych-e-g3-social-role",
    "subject": "psychology",
    "subject_cn": "心理健康",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "中小学心理健康教育指导纲要（2012年修订）/ 教育部相关要求 · 小学",
    "title": "角色意识与时间管理",
    "name_en": "Roles in Different Places and Managing My Day",
    "grade": 3,
    "grade_cn": "三年级",
    "domain": "life-adaptation",
    "domain_cn": "生活适应",
    "lesson_type": "workshop",
    "version": "1.0.0",
    "description": "面向小学三年级的生活适应课：先在「教室里 / 在家里 / 在运动队里」把九件事与三个角色配对，弄清角色是位置不同、不是等级高低；再把一天要做的事情按「必须做 / 想先做 / 可以等」分成三类，排进四个时间格，每格只容两件，放不下会实时提示撞车，学生自己比较、自己把可以等的那件挪走；最后拼出一张「我的一天小计划卡」。全课不评判、不贴标签，落点是「必须做的先占格子，剩余的时间安心去玩」。",
    "tags": ["角色意识", "时间管理", "生活适应", "冲突处理", "三年级"],
    "standard_ref": "《中小学心理健康教育指导纲要（2012年修订）· 小学中年级》生活适应——帮助学生建立正确的角色意识，培养学生对不同社会角色的适应；增强时间管理意识，帮助学生正确处理学习与兴趣、娱乐之间的矛盾。",
    "hero_question": "同一个人，为什么在教室里、在家里、在运动队里要做的事不一样？",
    "hero_alt": "角色意识与时间管理知识结构图：换个地方换个角色、事情分三类、撞车了就比一比 三栏",
    "hero_caption": "角色意识与时间管理：角色是位置不同不是等级高低 · 必须做、想先做、可以等 · 撞车了就比一比",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "在不同的场合，我该做什么？", "d": "教室里、家里、运动队里不一样", "v": "在不同的场合我该做什么"},
        {"t": "事情怎么分轻重？", "d": "哪件必须做，哪件可以等", "v": "事情怎么分轻重"},
        {"t": "两件事撞在一起怎么办？", "d": "时间只够做一件的时候", "v": "两件事撞在一起怎么办"},
        {"t": "怎么让我的晚上不那么赶？", "d": "不想再九点还在赶作业", "v": "怎么让我的晚上不那么赶"},
    ],
    "objectives": [
        "能说出我在教室里、在家里、在运动队里分别是怎样的角色，以及这个角色该做的事",
        "知道角色是位置不同，不是等级高低，换一个地方就换一种做法",
        "能把一天的事情分成必须做、想先做、可以等三类",
        "两件事撞在一起的时候，能自己比较一下，把可以等的那件挪到别的时间",
    ],
    "objectives_plain": [
        "能说出我在教室里、在家里、在运动队里分别是怎样的角色，以及这个角色该做的事",
        "知道角色是位置不同，不是等级高低，换一个地方就换一种做法",
        "能把一天的事情分成必须做、想先做、可以等三类",
        "两件事撞在一起的时候，能自己比较一下，把可以等的那件挪到别的时间",
    ],
    "standards": [
        {"content": "帮助学生建立正确的角色意识，培养学生对不同社会角色的适应",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学中年级 · 生活适应"},
        {"content": "增强时间管理意识，帮助学生正确处理学习与兴趣、娱乐之间的矛盾",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学中年级 · 生活适应"},
    ],
    "prereqs": ["psych-e-g3-self-know"],
    "prereqs_name": "认识自我与学习兴趣",
    "prereqs_meta": "psych-e-g3-self-know",
    "leads_to": ["psych-e-g4-peer-relation"],
    "next_meta": "psych-e-g4-peer-relation",
    "section_images": ["assets/psych-e-g3-social-role-fig1.webp", "assets/psych-e-g3-social-role-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "一个人一天有好几个角色——角色是位置不同，不是等级高低。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能把明天的事排出个先后。",
        "objectives": "四件事：说清三个角色、知道角色不是等级、把事分三类、撞车会自己挪。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "先问我在哪，再问我在这里是谁，最后问这个位置该做什么。",
        "lab-1": "拿不准就问：我旁边站着的是同学、家里人，还是队友？",
        "module-2": "三类：必须做、想先做、可以等。必须做的先占格子。",
        "lab-2": "每格最多两件，放不下会提醒你；撞车了就点卡片取回来，挪到别的时间。",
        "worked-example": "小舟四步：摊开事、分三类、必须做先划格子、撞车就比一比。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "三栏各选一样，做好你的一天小计划卡，再念给同桌听一遍。",
        "posttest": "出现了周末踢球、看书被叫去帮忙、训练和手工撞时间，看看你能不能用上今天的办法。",
        "summary": "三句话：角色是位置不同、事情分三类、撞车了就比一比。",
        "homework": "三层小任务，先做前两层，第三层可以请家里人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先帮你找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学心理健康「生活适应」在三年级的空缺，正对课标「帮助学生建立正确的角色意识，培养学生对不同社会角色的适应」与「增强时间管理意识，帮助学生正确处理学习与兴趣、娱乐之间的矛盾」。三年级学生的角色困惑，很少是「不知道该怎么做」，多半是「换了个地方还用上一个地方的做法」，或者把角色听成了等级；时间上的困难，也很少是「不想安排」，多半是「什么都想做、排不下就全乱了」。所以全课只做两件能落地的事——先把九件行为与「教室里 / 在家里 / 在运动队里」三个角色配对，弄清角色是位置不同、不是等级高低；再把八件事按「必须做 / 想先做 / 可以等」分类，排进四个时间格，每格只容两件，放不下时实时提示撞车，学生自己比较、自己把可以等的那件挪走（可操作的时间管理）。两个互动台子都能真的操作：一个是角色配对台，九件事归入三个地方，配对时给出角色含义；一个是时间格排程器，先分三类再排格子，撞车时给出「哪件可以等」的处置提示，并统计撞车次数。综合任务把「必须做 + 想先做但要等 + 可以等」拼成一张一天小计划卡。插图一律为中性简洁的教学插画，不使用真实儿童照片风格人像；全课不出现任何临床诊断词汇，不比较、不贴标签、不评判。",
    "plan_table": """| 1 | cover | 角色意识与时间管理 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 在不同的地方，我是不同的角色 | 承·概念一（角色是位置不是等级） |
| 6 | interactive | 动手一：角色配对台，九件事找地方 | 承·角色适应操作（九件事 → 三个地方） |
| 7 | concept | 一天的事情，可以分成三类 | 承·概念二（必须做 / 想先做 / 可以等） |
| 8 | interactive | 动手二：我的时间格，放不下会提醒你 | 承·可操作的时间管理（分类 + 排格 + 撞车提示） |
| 9 | concept | 例题示范：小舟的周三 | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：做出我的一天小计划卡 | 合·迁移应用（计划卡拼装） |
| 12 | quiz | 后测：换三个新情境，办法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，讲清角色和时间这件事 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：换个地方换个角色 / 事情分三类 / 撞车了就比一比 三栏\n- P5 三场景角色示意图（已生成）：教室里是同学、在家里是孩子、在运动队里是队员，各自标注该做的事，附中文标注\n- P7 时间格示意图（已生成）：一天分成四个时间段，必须做的事先占格子，其余按想先做和可以等排入，附中文标注\n- 三张图均为中性简洁教学插画，人物只用简单几何图形，不使用任何真实儿童照片或可识别肖像\n- 若需补充：学生自己画的时间格实物照片（需本人同意后才可使用）",
}
