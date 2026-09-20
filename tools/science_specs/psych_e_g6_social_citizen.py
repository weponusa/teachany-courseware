# -*- coding: utf-8 -*-
"""小学心理健康 · 亲社会行为与问题解决（G6）—— 补齐知识树「生活适应」空缺

学科语气（心理健康）：温和、不评判、不贴标签；严禁临床诊断词汇；不涉及自伤自杀；插图一律中性简洁插画。
六年级落点：班级与社区里的真实小问题——
  ① 愿意帮，也要会帮：帮忙前先三问「我安全吗 / 对方需要吗 / 我帮得上吗」，分辨会不会帮倒忙；
  ② 问题解决四步法：看清问题 → 想三个办法 → 选一个今天就能做的第一步 → 做完再看效果；
  ③ 核心模拟：真实小问题 → 先选「我能做的第一步」→ 展开三个选项的后果 → 生成我的行动小卡。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/psych-e-g6-social-citizen-fig1.webp'
F2 = './assets/psych-e-g6-social-citizen-fig2.webp'

TTS = {
    "hero": "六年级的同学，先想一想这几个画面：下课铃响了，走廊上有人摔了一跤；图书角的书堆得像小山，管书的同学不在；新来的同学一个人站在操场边。这些事你大概都见过。你心里可能也冒过两种念头：一种是想上去帮，又怕帮倒忙；另一种是怕做不好，干脆走开。这节课我们练两件事：帮忙之前先问三句话，看清自己安不安全、对方需不需要、自己帮不帮得上；再用四步法，把一件看得见的小麻烦变成一个今天就能做的第一步。",
    "problem-anchor": "开始之前，先选一个你最想知道的问题。是想知道看到有人需要帮助时，第一件事该做什么，还是想知道怎么判断自己会不会帮倒忙，又或者你想弄清楚，一件小麻烦缠成一团时从哪儿下手，再或者你更想问：想帮忙可是不好意思开口，怎么办。选好了，就带着它往下看。",
    "objectives": "这节课有四个小目标。第一，能说出什么是亲社会行为：在不伤害自己的前提下，做出对别人、对集体有帮助的事。第二，能在帮忙之前完成三句自检：我安全吗、对方需要吗、我帮得上吗，并分辨什么是帮倒忙。第三，能用四步法解决身边的小问题：看清问题、想三个办法、选一个今天就能做的第一步、做完再看效果。第四，能说出帮忙没帮好时可以怎么调整，并知道求助老师和家里人也是解决问题的一部分。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "先说第一件事。看到别人遇到麻烦，心里愿意动一下，这个念头就是亲社会行为的开始。可是光有心还不够，帮忙之前先问三句话。第一句，我安全吗——不站在车来车往的地方，不逞能去做危险的动作。第二句，对方需要吗——先问一句「需要我帮忙吗」，有时候对方只是想自己先缓一缓。第三句，我帮得上吗——帮不上就去找能帮上的人，叫老师、叫家里人，这也是一种帮忙。三句话问完再动手，你的热心就不会变成别人的麻烦。",
    "lab-1": "现在我们做一个小练习。下面有四个真实的小情境，每个情境里有三种做法。先点开一个情境，再从三种做法里选一个，看看它会带来什么结果。选得不太合适也不会说你错，我会告诉你这样可能会发生什么，还可以试试什么。",
    "module-2": "再说第二件事：怎么把一件麻烦变小。我们用四步法。第一步，看清问题，只说能看见的事，不急着评价谁对谁错。第二步，想三个办法，想到几个写几个，先不挑好坏。第三步，选一个今天就能做的第一步，说清楚谁来做、做什么、什么时候做、在哪里做。第四步，做完再看效果，有用就继续，不管用就换一个办法，或者请人一起帮忙。四步走下来，麻烦就从一团乱麻变成一件事。",
    "lab-2": "现在请你当一次第一步选择员。三个小麻烦里，每个麻烦都配了三个第一步。点开一个麻烦，再从三个第一步里挑一个，看看它接下来会发生什么。选得不太合适也不会批评你，我会告诉你还可以试试什么。",
    "worked-example": "我们一起帮小林想一想。放学后小林去图书角借书，发现书堆得像小山，管书的同学已经走了。我们陪他走四步。第一步，看清问题：书没有按标签放回原位，堆在两张桌子上。第二步，想三个办法：一是自己按标签放回去；二是先问老师可不可以整理；三是在班里说一句请大家一起收。第三步，选一个今天就能做的第一步：先走到办公室问老师一句，我可以帮着把书放回去吗。第四步，做完再看效果：老师同意了，他就按标签把书放回去；有几本不知道放哪一格，就放在最上面，等管理员来了问一句。走完四步，一个乱糟糟的图书角变成了他自己的一个小任务。",
    "conceptest-1": "接下来用三个说法考考你，每一个里面都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件大事交给你。先选一个真实的小麻烦，可以是班级里的，也可以是小区里的。然后先做三句自检：我安全吗、对方需要吗、我帮得上吗。再从三个第一步里挑一个，看看它的后果。最后生成一张属于你自己的行动小卡，写清楚谁来做、做什么、什么时候做、如果不管用怎么办。",
    "posttest": "最后一轮，换三个新的小情境来考考你。这次会出现操场上的球、社区里的快递架，还有同学之间的小别扭，看看你能不能先判断，再动手。",
    "summary": "这节课我们记住三句话。第一句，愿意帮忙是好的，先问三句再动手：我安全吗、对方需要吗、我帮得上吗。第二句，一件麻烦用四步变小：看清问题、想三个办法、选一个今天就能做的第一步、做完再看效果。第三句，帮不上不等于不热心——去叫老师、去请大人一起帮忙，也是解决问题的一部分。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出帮忙前的三句自检，再说一说什么是帮倒忙。第二层能力应用，动手做：找一件班里或者家里的小麻烦，用四步法写出三个办法和一个今天就能做的第一步。第三层迁移挑战，选做：这一周真正做一次第一步，做完写三句话：我做了什么、结果怎么样、下一次我会怎么改。",
    "knowledge-graph": "这张图展示了这节课在心理健康知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 愿意帮，也要会帮：帮忙前三问", "lab-1": "动手一 帮不帮，怎么帮",
    "module-2": "概念二 四步法：把一件麻烦变小", "lab-2": "动手二 第一步选择台",
    "worked-example": "例题讲解 小林和图书角", "conceptest-1": "概念测试",
    "synthesis": "综合任务 从一个小麻烦到我的行动小卡", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：帮不帮，怎么帮（四个情境 × 三种做法） ──
JUDGE = [
    {"id": "j1", "t": "走廊上有人摔了一跤，旁边围了几个人",
     "opts": [
         {"t": "先看清周围安不安全，蹲下来问一句「你还好吗？需要我扶你吗」，需要就去叫老师", "ok": True,
          "fb": "这样可能会让摔倒的同学舒服一些——先判断，再动手，帮得稳。"},
         {"t": "立刻冲过去把人拉起来", "ok": False,
          "fb": "这样可能会让受伤的地方更疼。还可以试试：先问一句「需要我扶你吗」，再决定扶不扶，站不起来就去叫老师。"},
         {"t": "绕开走，反正有人管", "ok": False,
          "fb": "这样可能会让你心里惦记一整天。还可以试试：做一件你真能做到的小事——去最近的办公室把老师叫来。"},
     ]},
    {"id": "j2", "t": "图书角的书堆得像小山，管书的同学不在",
     "opts": [
         {"t": "先问一句「我可以帮你整理吗」，再按书上的标签把它们放回去", "ok": True,
          "fb": "这样可能会让图书角很快恢复整齐，也不会打乱别人的分类。"},
         {"t": "不说话，直接把书全部搬到自己的座位上重新排", "ok": False,
          "fb": "这样可能会让管理员怎么都找不到书，反而帮了倒忙。还可以试试：先问一句，再按原来的标签归位。"},
         {"t": "拍一张照片发到班级群里，说一句「这里太乱了」", "ok": False,
          "fb": "这样可能会让负责的同学难堪，书还是乱的。还可以试试：把力气用在手上——顺手把最上面几本放回去。"},
     ]},
    {"id": "j3", "t": "新同学课间一个人站在墙边",
     "opts": [
         {"t": "走过去问一句「要不要一起去操场走走」，或者介绍一个人给他认识", "ok": True,
          "fb": "这样可能会让新同学这一天好过很多——他要的往往只是一个开头。"},
         {"t": "拉着他问一大串问题：你从哪儿转来的？为什么不跟别人玩？", "ok": False,
          "fb": "这样可能会让新同学更紧张。还可以试试：先做伴，再聊天——一起走一走，话自己就出来了。"},
         {"t": "不管他，等他自己来加入", "ok": False,
          "fb": "这样可能会让这一天对他来说特别长。还可以试试：一句「一起吗」就够了，不用先想好台词。"},
     ]},
    {"id": "j4", "t": "妈妈拎着很多袋子走进小区门口，你正要赶去上课",
     "opts": [
         {"t": "先判断我来得及吗、拿得动吗——能就拿一袋，来不及就说清楚晚上我来帮你", "ok": True,
          "fb": "这样可能会两边都顾得上——你先量了自己的力气和时间，再决定帮多少。"},
         {"t": "不管三七二十一全都接过来，结果两个人都慌了", "ok": False,
          "fb": "这样可能会让时间更紧，手里还容易掉东西。还可以试试：先分一件，说清楚剩下的一会儿再拿。"},
         {"t": "假装没看见，先跑过去", "ok": False,
          "fb": "这样可能会让你心里有点过不去。还可以试试：哪怕只说一句「我快迟到了，回来帮你拿」，也是一种帮忙。"},
     ]},
]

# ── 动手二：第一步选择台（三个麻烦 × 三个「我能做的第一步」） ──
STEPS = [
    {"id": "s1", "t": "走廊上有人摔了一跤",
     "steps": [
         {"t": "先看清周围，蹲下来问「需要我扶你吗」，站不起来就去叫老师",
          "fb": "这样可能会帮得刚刚好——先判断，再动手，不添乱。"},
         {"t": "马上扶他起来，让他自己走两步试试",
          "fb": "这样可能会让受伤的地方更疼。还可以试试：先问一句，再决定要不要叫老师。"},
         {"t": "站在旁边大声喊「有人摔倒啦」，等别人过来",
          "fb": "这样可能会让走廊更乱。还可以试试：声音小一点、事情多做一点——先把老师叫来。"},
     ]},
    {"id": "s2", "t": "图书角的书乱成一堆，管书的同学不在",
     "steps": [
         {"t": "先问老师或图书角管理员「我可以帮你整理吗」，再按标签归位",
          "fb": "这样可能会让图书角恢复整齐，也不会把别人的分类打乱。"},
         {"t": "不说话，把书全部搬到自己的座位上重新排",
          "fb": "这样可能会让管理员找不到书。还可以试试：按原来的标签放回原位，不确定的就先放在一边。"},
         {"t": "只在旁边提醒别人「别碰，等管理员来」",
          "fb": "这样可能会让书一直乱着。还可以试试：自己动手做最小的一步——把最上面几本放回去。"},
     ]},
    {"id": "s3", "t": "新同学课间一个人站在墙边",
     "steps": [
         {"t": "走过去问一句「要不要一起去操场走走」，或者介绍一个人给他认识",
          "fb": "这样可能会让新同学很快就有了伴——你只花了一句话。"},
         {"t": "拉着他说个不停，还追问他为什么一个人",
          "fb": "这样可能会让新同学更紧张。还可以试试：先做伴，少问几句，让他自己说。"},
         {"t": "只把这件事告诉老师，自己不去打招呼",
          "fb": "这样可能会让老师知道了，可新同学还是一个人。还可以试试：告诉老师之后，自己再走过去说一句「一起吗」。"},
     ]},
]

# ── 综合任务：真实小问题 → 三句自检 → 选第一步 → 生成行动小卡 ──
SIM = [
    {"id": "corridor", "t": "走廊上有人摔了一跤（班级里）",
     "checks": ["我站的位置会不会被后面的人撞到", "他/她自己想起来，还是需要人扶一把", "我是去扶，还是先去叫老师"],
     "steps": [
         {"t": "先看清周围，蹲下来问一句「你还好吗？需要我扶你吗」，需要就去叫老师",
          "fb": "这样可能会帮得稳——先判断，再动手，还顺手把老师叫来了。",
          "who": "我（和旁边的同学一起把路让开）", "when": "今天下课的时候", "where": "走廊那一侧，靠墙的位置"},
         {"t": "马上冲过去把人拉起来",
          "fb": "这样可能会让受伤的地方更疼。还可以试试：先问一句再动手，站不起来就去叫老师。",
          "who": "我", "when": "马上", "where": "摔倒的地方"},
         {"t": "先请旁边的同学去叫老师，自己留在原地陪他，等老师来",
          "fb": "这样可能会很稳妥——你分了一件自己真能做到的事，也有人在旁边陪着。",
          "who": "我留下陪他，旁边同学去叫老师", "when": "今天下课的时候", "where": "走廊靠墙的位置"},
     ]},
    {"id": "library", "t": "图书角的书乱成一堆（班级里）",
     "checks": ["我一个人整理会不会挡着别人借书", "管理员需不需要我按她的规矩来", "我一次能整理多少，要不要找人一起"],
     "steps": [
         {"t": "先问老师或管理员一句「我可以帮你整理吗」，再按标签把书放回去",
          "fb": "这样可能会让图书角很快整齐，也不会打乱别人的分类。",
          "who": "我和一两位同学", "when": "今天午休的时候", "where": "教室后面的图书角"},
         {"t": "把全部书搬到自己的座位上重新排一遍",
          "fb": "这样可能会让管理员怎么都找不到书。还可以试试：原地按标签归位，不确定的先放在一边。",
          "who": "我", "when": "今天午休的时候", "where": "自己的座位"},
         {"t": "先问一句，再把最乱的两格整理好，剩下的等管理员回来一起弄",
          "fb": "这样可能会让事情一步一步变小——先做你真能做完的那一部分。",
          "who": "我（管理员回来后再一起）", "when": "今天午休的时候", "where": "图书角最乱的两格"},
     ]},
    {"id": "newcomer", "t": "新同学课间一个人站在墙边（班级里）",
     "checks": ["我是不是真的能说上一句话", "他现在想不想有人过去", "我是自己过去，还是叫上一个同学一起"],
     "steps": [
         {"t": "先问一句「要不要一起去操场走走」，或者介绍一个人给他认识",
          "fb": "这样可能会让新同学马上就轻松一点——他要的只是一个开头。",
          "who": "我和我的同桌", "when": "今天课间的时候", "where": "教室门口的走廊"},
         {"t": "拉着他说个不停，还追问他为什么一个人",
          "fb": "这样可能会让新同学更紧张。还可以试试：先做伴，少问几句。",
          "who": "我", "when": "今天课间的时候", "where": "墙边"},
         {"t": "叫上一位同学一起过去，先陪他走一走，再问要不要一起玩",
          "fb": "这样可能会更自然——两个人一起去，新同学不用一个人面对一屋子人。",
          "who": "我和一位同学", "when": "今天课间的时候", "where": "操场的跑道边"},
     ]},
    {"id": "parcel", "t": "小区门口的快递架倒了，几件快递掉在地上（社区里）",
     "checks": ["我站的位置有没有车子经过", "这些是不是别人家的东西，我该不该动", "我一个人扶得动吗，要不要叫大人"],
     "steps": [
         {"t": "先看清有没有车子经过，把掉下的快递挪到架子旁边的干地方，再请门口的保安叔叔一起扶架子",
          "fb": "这样可能会让东西先安全下来——你做了能做的部分，也把扶架子这件事交给更稳的人。",
          "who": "我和门口的保安叔叔", "when": "今天放学回家的时候", "where": "小区门口的快递架旁"},
         {"t": "把掉在地上的快递一件件抱回自己家暂存，等失主来问",
          "fb": "这样可能会让人找不到自己的快递。还可以试试：原地码好、挪到干的地方，再告诉保安一声。",
          "who": "我", "when": "今天放学回家的时候", "where": "自己家门口"},
         {"t": "拍张照片发到小区群里，请大家自己来认领",
          "fb": "这样可能会让消息很快被刷过去，东西还在地上。还可以试试：先动手把东西挪到安全的地方，再在群里说一句。",
          "who": "我", "when": "今天放学回家的时候", "where": "小区的聊天群里"},
     ]},
]

CUSTOM_JS = r"""
/* ============================================================
   psych-e-g6-social-citizen 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 帮不帮，怎么帮：情境 × 三种做法 → 温和反馈
   3) 第一步选择台：麻烦 × 三个第一步 → 展开后果
   4) 综合任务：真实小问题 → 三句自检 → 选第一步 → 生成行动小卡
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

  /* ---------- 2. 帮不帮，怎么帮 ---------- */
  var JUDGE = __JUDGE_JSON__;
  var jStage = document.getElementById('jd-stage');
  if (jStage && JUDGE.length) {
    var curJ = null, doneJ = {};
    var jOut = document.getElementById('jd-out');
    var jScore = document.getElementById('jd-score');

    function jById(id) {
      for (var i = 0; i < JUDGE.length; i++) { if (JUDGE[i].id === id) return JUDGE[i]; }
      return null;
    }
    function renderJ() {
      document.querySelectorAll('[data-jd]').forEach(function (b) {
        var k = b.dataset.jd;
        b.classList.toggle('selected', k === curJ);
        b.classList.toggle('done', !!doneJ[k]);
      });
      jScore.textContent = '已经找到合适做法 ' + Object.keys(doneJ).length + ' / ' + JUDGE.length + ' 个情境';
    }
    function paintJ() {
      var box = document.getElementById('jd-opts');
      box.innerHTML = '';
      if (!curJ) return;
      var S = jById(curJ);
      if (!S) return;
      S.opts.forEach(function (o) {
        var b = document.createElement('button');
        b.className = 'choice' + (doneJ[curJ] && o.ok ? ' correct' : '');
        b.style.textAlign = 'left';
        b.textContent = o.t;
        b.addEventListener('click', function () {
          if (doneJ[curJ]) return;
          if (o.ok) {
            doneJ[curJ] = true;
            jOut.className = 'result';
            jOut.innerHTML = '<strong>这一条想得周到。</strong>' + o.fb;
          } else {
            jOut.className = 'result warn';
            jOut.innerHTML = '<strong>这个做法不少同学都想过，我们看看它会带来什么。</strong>' + o.fb;
          }
          renderJ();
          paintJ();
        });
        box.appendChild(b);
      });
    }
    document.querySelectorAll('[data-jd]').forEach(function (b) {
      b.addEventListener('click', function () {
        curJ = b.dataset.jd;
        var S = jById(curJ);
        if (doneJ[curJ]) {
          jOut.className = 'result';
          jOut.innerHTML = '<strong>这个情境已经找到了合适做法。</strong>记住那三句：我安全吗、对方需要吗、我帮得上吗。';
        } else {
          jOut.className = 'result warn';
          jOut.innerHTML = '<strong>情境：' + S.t + '</strong><br>下面有三种做法，选一个你觉得合适的试试。';
        }
        renderJ();
        paintJ();
      });
    });
    renderJ();
  }

  /* ---------- 3. 第一步选择台 ---------- */
  var STEPS = __STEPS_JSON__;
  var stStage = document.getElementById('st-stage');
  if (stStage && STEPS.length) {
    var curS = null, sPicked = {}, sChosen = {};
    var stOut = document.getElementById('st-out');
    var stScore = document.getElementById('st-score');

    function sById(id) {
      for (var i = 0; i < STEPS.length; i++) { if (STEPS[i].id === id) return STEPS[i]; }
      return null;
    }
    function renderS() {
      document.querySelectorAll('[data-st]').forEach(function (b) {
        var k = b.dataset.st;
        b.classList.toggle('selected', k === curS);
        b.classList.toggle('done', sChosen[k] !== undefined);
      });
      stScore.textContent = '已经练习 ' + Object.keys(sChosen).length + ' / ' + STEPS.length + ' 个麻烦';
    }
    function paintS() {
      var box = document.getElementById('st-steps');
      box.innerHTML = '';
      if (!curS) return;
      var S = sById(curS);
      if (!S) return;
      var head = document.createElement('p');
      head.style.cssText = 'margin:0 0 8px;color:var(--muted);font-size:14px';
      head.textContent = '下面是三个「我能做的第一步」，挑一个试试，看看它接下来会发生什么。';
      box.appendChild(head);
      (S.steps || []).forEach(function (st, i) {
        var b = document.createElement('button');
        b.className = 'choice' + (sChosen[curS] === i ? ' correct' : '');
        b.style.cssText = 'text-align:left;margin:4px 0';
        b.textContent = '第一步 ' + (i + 1) + '：' + st.t;
        b.addEventListener('click', function () {
          if (sPicked[curS]) return;
          sPicked[curS] = true;
          sChosen[curS] = i;
          stOut.className = (i === 0) ? 'result' : 'result warn';
          stOut.innerHTML = '<strong>你选了第一步 ' + (i + 1) + '。</strong>' + st.fb;
          renderS();
          paintS();
        });
        box.appendChild(b);
      });
    }
    document.querySelectorAll('[data-st]').forEach(function (b) {
      b.addEventListener('click', function () {
        curS = b.dataset.st;
        var S = sById(curS);
        if (sChosen[curS] !== undefined) {
          stOut.className = 'result';
          stOut.innerHTML = '<strong>这个麻烦已经练过了。</strong>换一个试试，看看第一步不同，结果有什么不一样。';
        } else {
          stOut.className = 'result warn';
          stOut.innerHTML = '<strong>麻烦：' + S.t + '</strong><br>下面有三个第一步，选一个试试它的后果。';
        }
        renderS();
        paintS();
      });
    });
    renderS();
  }

  /* ---------- 4. 综合任务：真实小问题 → 三句自检 → 选第一步 → 行动小卡 ---------- */
  var SIM = __SIM_JSON__;
  var simStage = document.getElementById('sq-stage');
  if (simStage && SIM.length) {
    var curQ = null, qChosen = {}, qChecked = {};
    var qOut = document.getElementById('sq-out');
    var qScore = document.getElementById('sq-score');
    var qCheckOut = document.getElementById('sq-check-out');
    var qCard = document.getElementById('sq-card-out');

    function qById(id) {
      for (var i = 0; i < SIM.length; i++) { if (SIM[i].id === id) return SIM[i]; }
      return null;
    }
    function qName(id) { var s = qById(id); return s ? s.t : ''; }
    function renderQ() {
      document.querySelectorAll('[data-sq]').forEach(function (b) {
        var k = b.dataset.sq;
        b.classList.toggle('selected', k === curQ);
        b.classList.toggle('done', qChosen[k] !== undefined);
      });
      var done = 0;
      SIM.forEach(function (s) { if (qChosen[s.id] !== undefined) done++; });
      qScore.textContent = '已经生成 ' + done + ' / ' + SIM.length + ' 张行动小卡';
    }
    function paintChecks() {
      var box = document.getElementById('sq-checks');
      box.innerHTML = '';
      if (!curQ) return;
      var S = qById(curQ);
      if (!S) return;
      var head = document.createElement('p');
      head.style.cssText = 'margin:0 0 8px;color:var(--muted);font-size:14px';
      head.textContent = '动手之前，先把这三句问一遍：我安全吗？对方需要吗？我帮得上吗？';
      box.appendChild(head);
      (S.checks || []).forEach(function (c, i) {
        var b = document.createElement('button');
        b.className = 'choice' + (qChecked[curQ] && qChecked[curQ][i] ? ' selected' : '');
        b.style.cssText = 'text-align:left;margin:4px 0';
        b.textContent = '想一想 ' + (i + 1) + '：' + c;
        b.addEventListener('click', function () {
          if (!qChecked[curQ]) qChecked[curQ] = {};
          qChecked[curQ][i] = true;
          paintChecks();
          var n = Object.keys(qChecked[curQ]).length;
          qCheckOut.className = (n === 3) ? 'result' : 'result warn';
          qCheckOut.innerHTML = (n === 3)
            ? '<strong>三句都问过了。</strong>判断清楚了，再动手就稳当得多——现在到右边挑一个第一步。'
            : '<strong>已经想过 ' + n + ' 句。</strong>把剩下的也问一遍，帮忙的时候心里就更有底了。';
        });
        box.appendChild(b);
      });
    }
    function paintQ() {
      var box = document.getElementById('sq-steps');
      box.innerHTML = '';
      if (!curQ) return;
      var S = qById(curQ);
      if (!S) return;
      var head = document.createElement('p');
      head.style.cssText = 'margin:0 0 8px;color:var(--muted);font-size:14px';
      head.textContent = '下面是三个「我能做的第一步」，选一个，看看它的后果。';
      box.appendChild(head);
      (S.steps || []).forEach(function (st, i) {
        var b = document.createElement('button');
        b.className = 'choice' + (qChosen[curQ] === i ? ' correct' : '');
        b.style.cssText = 'text-align:left;margin:4px 0';
        b.textContent = '第一步 ' + (i + 1) + '：' + st.t;
        b.addEventListener('click', function () {
          if (qChosen[curQ] !== undefined) return;
          qChosen[curQ] = i;
          qOut.className = (i === 0) ? 'result' : 'result warn';
          qOut.innerHTML = '<strong>你选了第一步 ' + (i + 1) + '。</strong>' + st.fb;
          renderQ();
          paintQ();
        });
        box.appendChild(b);
      });
    }
    document.querySelectorAll('[data-sq]').forEach(function (b) {
      b.addEventListener('click', function () {
        curQ = b.dataset.sq;
        var S = qById(curQ);
        if (qCard) qCard.innerHTML = '';
        if (qChosen[curQ] !== undefined) {
          qOut.className = 'result';
          qOut.innerHTML = '<strong>这个麻烦已经练过了。</strong>到下面生成行动小卡，或者换一个麻烦试试。';
        } else {
          qOut.className = 'result warn';
          qOut.innerHTML = '<strong>你选的麻烦：' + S.t + '</strong><br>先做三句自检，再挑一个第一步。';
        }
        qCheckOut.className = 'result warn';
        qCheckOut.textContent = '先在左边把三句自检点一遍，再挑第一步。';
        renderQ();
        paintChecks();
        paintQ();
      });
    });
    var qGen = document.getElementById('sq-gen');
    if (qGen) {
      qGen.addEventListener('click', function () {
        if (!curQ) {
          qOut.className = 'result warn';
          qOut.textContent = '先在第一步选一个麻烦。';
          return;
        }
        var S = qById(curQ);
        var idx = qChosen[curQ];
        if (idx === undefined) {
          qOut.className = 'result warn';
          qOut.textContent = '先挑一个「我能做的第一步」，再来生成行动小卡。';
          return;
        }
        var st = S.steps[idx];
        var nChk = qChecked[curQ] ? Object.keys(qChecked[curQ]).length : 0;
        var lines = [
          '谁来做：' + (st.who || '我'),
          '做什么：' + st.t,
          '什么时候：' + (st.when || '今天'),
          '在哪里：' + (st.where || '现场'),
          '如果不管用：换一个办法试试，也可以请老师、家里人或者身边的人一起帮忙。',
        ];
        qOut.className = 'result';
        qOut.innerHTML = '<strong>这就是你的第一步。</strong>' + st.fb +
          '<br>三句自检你已经问过 ' + nChk + ' 句。';
        if (qCard) {
          qCard.className = 'result';
          qCard.innerHTML = '<strong>我的行动小卡（' + S.t + '）：</strong><br>' + lines.join('<br>') +
            (nChk < 3 ? '<br><span style="color:var(--muted)">提醒：还有自检没问完，动手之前补上更稳当。</span>' : '');
        }
        renderQ();
      });
    }
    renderQ();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__JUDGE_JSON__', json.dumps(JUDGE, ensure_ascii=False))
             .replace('__STEPS_JSON__', json.dumps(STEPS, ensure_ascii=False))
             .replace('__SIM_JSON__', json.dumps(SIM, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "走廊上有人摔了一跤，你正好路过。下面哪个做法更合适？",
         "options": [("先看清周围安不安全，问一句「需要我扶你吗」，需要就去叫老师", True),
                     ("先冲过去把人拉起来，越快越好", False),
                     ("绕开走，反正会有别人来管", False)],
         "explain": "先判断，再动手，帮得稳；帮不上也不等于不热心，叫老师也是一种帮忙。"
                    "<strong>错因提醒：</strong>常见错误是把「快」当成「好」——帮忙之前多花五秒钟看一眼，往往能少一次帮倒忙。"},
        {"q": "下面哪一条属于「帮倒忙」？",
         "options": [("不说话就把图书角的书全部搬走重新排，别人再也找不到", True),
                     ("先问一句「我可以帮你整理吗」，再按标签放回去", False),
                     ("把掉在地上的东西挪到旁边安全的地方，再告诉大人", False)],
         "explain": "帮忙的前提是尊重原来的秩序，也要问一句对方需不需要。"
                    "<strong>错因提醒：</strong>最容易搞混的是「热心」和「替别人做主」——不问一句就动手，很多时候是给自己省事，不是给别人帮忙。"},
        {"q": "一件小麻烦缠成一团，你不知道从哪儿下手。下面哪个做法更合适？",
         "options": [("先看清问题，再想三个办法，挑一个今天就能做的第一步", True),
                     ("先等几天，说不定它自己就解决了", False),
                     ("一次把所有事全做完，做到很晚", False)],
         "explain": "把麻烦变小，靠的是四步：看清、想三个、选一个第一步、做完再看效果。"
                    "<strong>错因提醒：</strong>有人误认为「要一次全部解决才算解决」——一口气做完往往第二天就停下来了，一个小步骤反而能接着往前走。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "愿意帮，也要会帮：帮忙前的三句话", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们已经练过遇到挫折先分清能改变的和不能改变的，也知道了身体和边界都属于自己（And）；可是看到别人遇到麻烦时，心里常常卡在两种反应上——冲上去怕帮倒忙，走开又过意不去（But）；所以这节课先练三句话，让热心帮到点子上（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">看到别人有麻烦，愿意动一下，这个念头就是<strong>亲社会行为</strong>的开始。可是光有心还不够，动手之前先问三句。</p>
        <div class="grid grid-3">
          <div class="inner-card">
            <p><strong>① 我安全吗</strong></p>
            <p style="color:var(--muted)">不站在车来车往的地方，不逞能去做危险的动作。先把自己安顿好，才有余力帮别人。</p>
          </div>
          <div class="inner-card">
            <p><strong>② 对方需要吗</strong></p>
            <p style="color:var(--muted)">先问一句「需要我帮忙吗」。有时候对方只是想先缓一缓，问一句比直接上手更贴心。</p>
          </div>
          <div class="inner-card">
            <p><strong>③ 我帮得上吗</strong></p>
            <p style="color:var(--muted)">帮不上就去找能帮上的人：叫老师、请保安叔叔、喊家里人——这也是帮忙的一部分。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="帮忙前三问示意图，三个圆形图标分别表示我安全吗、对方需要吗、我帮得上吗，配中性简笔轮廓，附中文标注">
          <figcaption>示意图：帮忙之前先问三句——我安全吗、对方需要吗、我帮得上吗（教学示意图，人物为中性简洁插画）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「没帮上，就是不够热心」。这里最容易<strong>搞混</strong>的是「帮不上」和「不用帮」——真的帮不上，还可以去叫能帮上的人。把老师请来、把大人叫来，麻烦解决得可能比你自己上手更快。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "把一次帮忙拆成两段：动手之前先看五秒，动手之后再看一眼结果。两段加起来，才是完整的帮忙。"},
    {"lens": "比较它", "text": "「我帮你」和「我帮你，可以吗」只差三个字，一个替别人做主，另一个把选择留给对方。"},
    {"lens": "迁移它", "text": "同一套三句话，在小区里、在车上、在陌生的地方都用得上：先看自己安不安全，再问一句，再决定做什么。"},
])}
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>帮忙先三问——<strong>我安全、他需要、我帮得上；帮不上就去叫人。</strong></div></div>
    ''', tag="概念一"))

    jd_btns = "\n".join(
        f'            <button class="choice" data-jd="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in JUDGE
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：帮不帮，怎么帮", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">四个真实的小情境，每个情境里有三种做法。先点开一个情境，再从三种做法里选一个。<strong>选得不太合适也不会说你错</strong>，我会告诉你这样可能会发生什么，还可以试试什么。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 选一个情境</div>
          <div class="grid" id="jd-stage">
{jd_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 三种做法，选一个试试</div>
          <div class="grid" id="jd-opts">
            <span style="color:var(--muted);font-size:14px">先在上面点一个情境，这里就会出现三种做法。</span>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">练习进度</span><span class="v" id="jd-score">已经找到合适做法 0 / 4 个情境</span></div>
          </div>
          <p class="result warn" id="jd-out" style="margin-top:12px">先点一个你自己也遇到过的情境。</p>
        </div>
        <div class="inner-card" style="margin-top:14px">
          <p><strong>写一条你自己的：</strong></p>
          <p style="color:var(--muted)">最近你见过哪一件「有人需要帮忙」的事？写下你的三句自检：我安全吗、对方需要吗、我帮得上吗。</p>
          <textarea id="jd-answer" rows="2" placeholder="我安全吗……对方需要吗……我帮得上吗……" style="margin-top:8px"></textarea>
        </div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "四步法：把一件麻烦变小", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">第二件事，是怎么把一团乱麻变成一件事。方法只有四步，一步一步往前走就行。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看清问题：</strong>只说能看见的事——书堆在两张桌子上、快递掉在架子旁边。不急着评价谁对谁错。</div></div>
          <div class="step"><span class="n">2</span><div><strong>想三个办法：</strong>想到几个写几个，先不挑好坏。办法多一点，手就不会被一件事卡住。</div></div>
          <div class="step"><span class="n">3</span><div><strong>选一个第一步：</strong>说清楚谁来做、做什么、什么时候做、在哪里做。今天就能动起来的那种最好。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>做完再看效果：</strong>有用就接着做，不管用就换一个办法，或者请人一起帮忙。求助也是办法之一。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="问题解决四步法流程图，四个方框依次表示看清问题、想三个办法、选一个第一步、做完再看效果，附中文标注">
          <figcaption>示意图：四步法——看清问题 → 想三个办法 → 选一个今天就能做的第一步 → 做完再看效果（教学示意图）</figcaption>
        </figure>
        <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(78,205,196,.45)">
          <p><strong>一个「第一步」长什么样？</strong></p>
          <p style="color:var(--muted)">它要能回答三件事：<strong>做什么、什么时候做、和谁一起</strong>。比如「今天午休的时候，我和同桌把最乱的两格书按标签放回去」——这句话今天就能开始。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「第一步必须把整件事解决掉」。这里最容易<strong>搞混</strong>的是「最小的一步」和「不认真的一步」——先做一小步，是为了让事情真的动起来。不动的一整套计划，比不上已经做完的一小步。</p>
        </div>
{insight_box([
    {"lens": "拆开它", "text": "麻烦之所以让人发愁，是因为它被当成一整块。把它拆成看得见的小事，每一件都可能有一个今天能做的动作。"},
    {"lens": "解释它", "text": "为什么先想三个办法？只有一个办法的时候，只要它行不通，人就会停在原地；三个办法里总有一个今天能开始。"},
    {"lens": "迁移它", "text": "四步法不只用在班里：家里的一堆杂物、一次没准备好的小组展示、一次和同学的别扭，都可以先看清、再想三个、再选一步。"},
])}
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>看清、想三、选一步、再看效果——<strong>麻烦变小，靠的是动手的第一步。</strong></div></div>
    ''', tag="概念二"))

    st_btns = "\n".join(
        f'            <button class="choice" data-st="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in STEPS
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：第一步选择台", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">三个小麻烦，每个麻烦都配了三个第一步。点开一个麻烦，再从三个第一步里挑一个，看看它接下来会发生什么。<strong>选得不太合适也不会批评你</strong>，我会告诉你还可以试试什么。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 选一个麻烦</div>
          <div class="grid" id="st-stage">
{st_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 三个「我能做的第一步」</div>
          <div class="grid" id="st-steps">
            <span style="color:var(--muted);font-size:14px">先在上面点一个麻烦，这里就会出现三个第一步。</span>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">练习进度</span><span class="v" id="st-score">已经练习 0 / 3 个麻烦</span></div>
          </div>
          <p class="result warn" id="st-out" style="margin-top:12px">先点一个麻烦。</p>
        </div>
        <div class="inner-card" style="margin-top:14px">
          <p><strong>写一句你自己的第一步：</strong></p>
          <p style="color:var(--muted)">说清楚三件事——<strong>做什么、什么时候做、和谁一起</strong>。写得越具体，今天越容易开始。</p>
          <textarea id="st-answer" rows="2" placeholder="今天午休的时候，我和……把……" style="margin-top:8px"></textarea>
        </div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小林和图书角", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>放学后小林去图书角借书，发现书堆得像小山，管书的同学已经走了。他站在那儿想了两分钟：整理吧，怕弄乱别人的分类；不整理吧，明天大家又找不到书。请你陪他走四步。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看清问题：</strong>书没有按标签放回原位，堆在两张桌子上；旁边还有人等着借书。</div></div>
          <div class="step"><span class="n">2</span><div><strong>想三个办法：</strong>① 自己按标签放回去；② 先问老师可不可以整理；③ 在班里说一句，请大家一起收。</div></div>
          <div class="step"><span class="n">3</span><div><strong>选一个第一步：</strong>今天放学前，走到办公室问老师一句「我可以帮着把书放回去吗」。这件事他今天就做得到。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>做完再看效果：</strong>老师同意了，他就按标签放回去；有几本不知道放哪一格，就先放在最上面，等管理员来了问一句。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「帮忙就得一个人全包，问别人显得不够能干」。这里最容易<strong>搞混</strong>的是「自己扛」和「把事情做成」——小林先问一句，反而少了一次帮倒忙；问一句不丢人，事情做成才是目标。</p>
        </div>
        <div class="inner-card">
          <p><strong>说给同桌听：</strong>这四步里，哪一步你自己已经做到了？如果换成是你，你会把哪一件事定为今天的第一步？</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "关于「帮忙前三句自检」，下面哪种理解更合适？",
         "options": [("先问一句是为了帮到点子上，不是不想帮", True),
                     ("问来问去太麻烦，看到就去帮才对", False),
                     ("只要我力气大，就不用先看情况", False)],
         "explain": "三句自检花不了几秒钟，却能让帮忙刚刚好。"
                    "<strong>错因提醒：</strong>常见错误是把「先判断」误认为「不够热心」——判断和热心是两件事，判断让热心真正落地。"},
        {"q": "下面哪一句是一个合格的「第一步」？",
         "options": [("今天午休的时候，我和同桌把最乱的两格书按标签放回去", True),
                     ("以后我要多帮助同学", False),
                     ("这件事我一定要彻底解决", False)],
         "explain": "合格的第一步能回答三件事：做什么、什么时候做、和谁一起。"
                    "<strong>错因提醒：</strong>最容易搞混的是「决心」和「做法」——决心说的是心情，做法说的是动作。"},
        {"q": "你用了四步法，可是第一步做完发现没什么用。下面哪个做法更合适？",
         "options": [("说清楚哪里不管用，换一个办法，或者请人一起帮忙", True),
                     ("算了，我果然什么都做不好", False),
                     ("原来打算怎么做就怎么做，再多试几遍一样的", False)],
         "explain": "第四步本来就是「做完再看效果」，不管用是正常的，换一个办法接着走。"
                    "<strong>错因提醒：</strong>有人误认为「没做成就是白做了」——你已经看清了哪条路不通，这一步本身就是收获。"}
    ], tag="概念测试"))

    sq_btns = "\n".join(
        f'            <button class="choice" data-sq="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in SIM
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：从一个小麻烦到我的行动小卡", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先选一个真实的小麻烦（班级里的或小区里的），把三句自检问一遍，再挑一个「我能做的第一步」，最后生成你的行动小卡。<strong>选得不太合适也不扣分</strong>，我会告诉你还可以试试什么。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 选一个真实的小麻烦</div>
          <div class="grid" id="sq-stage">
{sq_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 三句自检（点一遍，想一想）</div>
          <div class="grid" id="sq-checks">
            <span style="color:var(--muted);font-size:14px">先在上面选一个麻烦，这里就会出现三句自检。</span>
          </div>
          <p class="result warn" id="sq-check-out" style="margin-top:10px">先在左边把三句自检点一遍。</p>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">③ 三个「我能做的第一步」</div>
          <div class="grid" id="sq-steps">
            <span style="color:var(--muted);font-size:14px">选好麻烦之后，这里会出现三个第一步。</span>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">生成进度</span><span class="v" id="sq-score">已经生成 0 / 4 张行动小卡</span></div>
          </div>
          <div class="flex-row">
            <button class="choice" id="sq-gen" style="text-align:center">④ 生成我的行动小卡</button>
          </div>
          <p class="result warn" id="sq-out" style="margin-top:12px">先在第一步选一个麻烦。</p>
          <p id="sq-card-out" style="margin-top:10px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💛</span><div><strong>记住这件事：</strong>第一步可以很小。小到只是问一句、只是把三本书放回去——但它今天就能做完，明天就能接着做。</div></div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换三个新情境，办法还在不在", TTS["posttest"], [
        {"q": "课间操场上，一个球滚到你脚边，一个低年级同学跑过来捡。下面哪个做法更合适？",
         "options": [("看一眼周围有没有人跑过来，再把球递给他，或者轻轻踢回去", True),
                     ("用力一脚把球踢回去", False),
                     ("装作没看见，走开", False)],
         "explain": "先看一眼周围，再决定怎么还，是既安全又省事的做法。"
                    "<strong>错因提醒：</strong>常见错误是把「马上动手」当成帮忙——用力踢回去，球可能砸到人，帮忙就成了添乱。"},
        {"q": "小区里一辆自行车被风吹倒了，压在花坛边。下面哪个做法更合适？",
         "options": [("先看有没有车经过、扶不扶得动，扶不动就去请大人一起帮忙", True),
                     ("立刻跑过去扛起来，不管自己站的位置", False),
                     ("拍张照片发到小区群里就不管了", False)],
         "explain": "扶得起就扶，扶不动就请人一起——三句自检在任何场合都适用。"
                    "<strong>错因提醒：</strong>有人误认为「发到群里就等于做了事」——事情还倒在那里，先动手把能做的做了，再说话。"},
        {"q": "两位同学因为值日的事闹别扭，谁也不说话。下面哪个做法更合适？",
         "options": [("先分别听两句，把两个人说的不同说法记下来，再提议一起找老师说说", True),
                     ("马上替他们决定谁对谁错，宣布结果", False),
                     ("当着全班的面把事情说一遍，让大家评判", False)],
         "explain": "小别扭的关键是让两边都说得上话，替别人下判断往往会火上浇油。"
                    "<strong>错因提醒：</strong>最容易搞混的是「调解」和「当裁判」——调解是让两个人自己说清楚，裁判是替他们下结论。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，讲清帮忙这件事", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>先问三句：</strong>我安全吗、对方需要吗、我帮得上吗——问完再动手，热心就能落到点子上。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>用四步变小：</strong>看清问题、想三个办法、选一个今天就能做的第一步、做完再看效果。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>求助也是办法：</strong>帮不上不等于不热心；叫上老师、家里人或者旁边的叔叔阿姨一起，事情往往解决得更快。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>还想多说一句：</strong>做得好或做得不太好，都可以让身边的人知道——和同桌聊聊、跟老师说说。有人一起商量，事情通常没那么难。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「三句自检、四步、第一步」这几个词，说清楚你最近见过的一件小事，以及你会怎么开始。</p>
          <p style="color:var(--muted)">再动一动手：<strong>画出</strong>一张四步法的格子图，把一件班里的小麻烦填进去，第三步只写一句话——你的第一步。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写出帮忙前的三句自检，每句配一个例子。",
            "用自己的话说一说，什么叫「帮倒忙」，举一个你见过的例子。",
            "把一个「第一步」补完整：今天放学前，我和____，把____。",
        ],
        [
            "在班里或家里找一件小麻烦，用四步法写出三个办法，再标出你选的第一步。",
            "记录一次真实的帮忙：你做了什么、结果怎么样，写三句话。",
        ],
        [
            "这一周真正做一次第一步，做完写三句话：我做了什么、结果怎么样、下一次我会怎么改。",
            "和小组同学一起，为班级想一件可以长期做的小事（比如整理图书角、照顾新同学），写出三个办法和一条分工约定。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "psych-e-g6-social-citizen",
    "node_id": "psych-e-g6-social-citizen",
    "subject": "psychology",
    "subject_cn": "心理健康",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "中小学心理健康教育指导纲要（2012年修订）/ 教育部相关要求 · 小学",
    "title": "亲社会行为与问题解决",
    "name_en": "Prosocial Behaviour and Solving Everyday Problems",
    "grade": 6,
    "grade_cn": "六年级",
    "domain": "life-adaptation",
    "domain_cn": "生活适应",
    "lesson_type": "workshop",
    "version": "1.0.0",
    "description": "面向小学六年级的生活适应课：看到别人遇到麻烦时，怎么帮得刚刚好。全课围绕两条可操作的线索：① 帮忙前三句自检——我安全吗、对方需要吗、我帮得上吗，用来分辨什么是帮忙、什么是帮倒忙；② 四步法——看清问题、想三个办法、选一个今天就能做的第一步、做完再看效果，并明确求助老师与家里人也是解决问题的一部分。核心模拟真的能操作：选一个真实的小问题（走廊上有人摔了 / 图书角的书乱放 / 新同学没人一起玩 / 小区门口的快递架倒了）→ 先做三句自检 → 再选「我能做的第一步」→ 展开三个选项各自会带来什么结果 → 生成一张写清谁来做、做什么、什么时候做、不管用怎么办的行动小卡。另有两个练习台：帮不帮怎么帮（四个情境各三种做法）、第一步选择台（三个麻烦各三个第一步）。所有反馈一律温和，写成「这样可能会……，还可以试试……」，不评判、不贴标签，不使用任何临床诊断词汇。",
    "tags": ["亲社会行为", "问题解决", "帮忙前先判断", "第一步", "六年级", "生活适应"],
    "standard_ref": "《中小学心理健康教育指导纲要（2012年修订）· 小学中高年级》——积极促进学生的亲社会行为，逐步认识自己与社会、国家和世界的关系；培养学生分析问题和解决问题的能力，为初中阶段学习生活做好准备。",
    "hero_question": "走廊上有人摔了、图书角的书乱成一堆、新同学一个人站在墙边——想帮忙，又怕帮倒忙，第一步到底该做什么？",
    "hero_alt": "亲社会行为与问题解决知识结构图：愿意帮忙、帮忙前三句自检、四步法变小麻烦 三栏",
    "hero_caption": "亲社会行为与问题解决：愿意帮 · 先问三句（我安全吗、对方需要吗、我帮得上吗）· 选一个今天就能做的第一步",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "看到有人需要帮助，我第一件事该做什么？", "d": "想上去帮，又怕做错", "v": "看到有人需要帮助我第一件事该做什么"},
        {"t": "怎么判断我会不会帮倒忙？", "d": "有时候越帮越乱，心里挺不好意思", "v": "怎么判断我会不会帮倒忙"},
        {"t": "一件小麻烦缠成一团，从哪儿下手？", "d": "想做的太多，最后一件也没做成", "v": "一件小麻烦缠成一团从哪儿下手"},
        {"t": "想帮忙，可是不好意思开口，怎么办？", "d": "怕被拒绝，也怕别人觉得我多事", "v": "想帮忙可是不好意思开口怎么办"},
    ],
    "objectives": [
        "能说出什么是亲社会行为：在不伤害自己的前提下，做出对别人、对集体有帮助的事",
        "能在帮忙之前完成三句自检——我安全吗、对方需要吗、我帮得上吗，并分辨什么是帮倒忙",
        "能用四步法解决身边的小问题：看清问题、想三个办法、选一个今天就能做的第一步、做完再看效果",
        "能说出帮忙没帮好时可以怎么调整，并知道求助老师和家里人也是解决问题的一部分",
    ],
    "objectives_plain": [
        "能说出什么是亲社会行为：在不伤害自己的前提下，做出对别人、对集体有帮助的事",
        "能在帮忙之前完成三句自检——我安全吗、对方需要吗、我帮得上吗，并分辨什么是帮倒忙",
        "能用四步法解决身边的小问题：看清问题、想三个办法、选一个今天就能做的第一步、做完再看效果",
        "能说出帮忙没帮好时可以怎么调整，并知道求助老师和家里人也是解决问题的一部分",
    ],
    "standards": [
        {"content": "积极促进学生的亲社会行为，逐步认识自己与社会、国家和世界的关系",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学中高年级"},
        {"content": "培养学生分析问题和解决问题的能力，为初中阶段学习生活做好准备",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学中高年级"},
    ],
    "prereqs": ["psych-e-g6-puberty"],
    "prereqs_name": "青春期的变化与同伴交往",
    "prereqs_meta": "psych-e-g6-puberty",
    "leads_to": ["psych-m-g7-interpersonal"],
    "next_meta": "psych-m-g7-interpersonal",
    "section_images": ["assets/psych-e-g6-social-citizen-fig1.webp",
                       "assets/psych-e-g6-social-citizen-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "三个熟悉的画面：有人摔了、书乱了、新同学一个人站着——这节课练怎么帮得刚刚好。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能写出一句今天就能做的第一步。",
        "objectives": "看清四件事：什么是亲社会行为、帮前三问、四步法、帮不上时怎么办。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "帮忙先三问：我安全吗、对方需要吗、我帮得上吗；帮不上就去叫能帮上的人。",
        "lab-1": "四个情境各三种做法，选完把反馈读一遍；不合适的那条会告诉你还可以试试什么。",
        "module-2": "四步法：看清问题、想三个办法、选一个今天就能做的第一步、做完再看效果。",
        "lab-2": "三个麻烦各三个第一步；点开两个不同的第一步，比一比结果有什么不一样。",
        "worked-example": "小林四步：看清问题、想三个办法、选一个第一步、做完再看效果。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "选麻烦 → 三句自检 → 选第一步 → 看后果 → 生成行动小卡，五样都齐了。",
        "posttest": "出现了操场上的球、小区里的自行车、同学之间的小别扭，看看你能不能用上今天的办法。",
        "summary": "三句话：先问三句、用四步变小、求助也是办法。",
        "homework": "三层小任务，先做前两层；第三层要真的动手做一次。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先帮你找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学心理健康「生活适应」在六年级的空缺，正对课标「积极促进学生的亲社会行为」与「培养学生分析问题和解决问题的能力，为初中阶段学习生活做好准备」。六年级学生的真实难点有两个：① 愿意帮，但不知道从哪里下手——要么冲上去越帮越乱，要么怕做不好干脆走开；② 手里的办法只有一个，一旦行不通就停在原地，于是「一件小麻烦」被当成一整块压在心里。所以全课围绕一条可操作的链路：概念一给出帮忙前三句自检（我安全吗、对方需要吗、我帮得上吗）并明确什么叫帮倒忙、什么叫求助也是帮忙；概念二给出四步法（看清问题、想三个办法、选一个今天就能做的第一步、做完再看效果），并要求「第一步」能回答做什么、什么时候做、和谁一起。三个台子都能真的操作：帮不帮怎么帮（四个情境各三种做法，不合适的那条一律写成「这样可能会……，还可以试试……」）、第一步选择台（三个麻烦各三个第一步，点开两个不同选择可以比较后果），以及核心模拟——综合任务里的完整链路：选一个真实的小问题（走廊上有人摔了 / 图书角的书乱放 / 新同学没人一起玩 / 小区门口的快递架倒了）→ 先做三句自检 → 再选「我能做的第一步」→ 展开三个选项各自会带来什么结果 → 生成一张写清谁来做、做什么、什么时候做、不管用怎么办的行动小卡。全课语气温和、不评判、不贴标签，不使用任何临床诊断词汇；插图一律为中性简洁的教学插画。",
    "plan_table": """| 1 | cover | 亲社会行为与问题解决 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 愿意帮，也要会帮：帮忙前的三句话 | 承·概念一（三句自检） |
| 6 | interactive | 动手一：帮不帮，怎么帮 | 承·判断台（四情境 × 三做法） |
| 7 | concept | 四步法：把一件麻烦变小 | 承·概念二（问题解决四步） |
| 8 | interactive | 动手二：第一步选择台 | 承·选择台（三麻烦 × 三第一步） |
| 9 | concept | 例题示范：小林和图书角 | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：从一个小麻烦到我的行动小卡 | 合·迁移应用（自检 + 选第一步 + 生成卡片） |
| 12 | quiz | 后测：换三个新情境，办法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，讲清帮忙这件事 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：愿意帮忙 / 帮忙前三句自检 / 四步法变小麻烦 三栏\n- P5 帮忙前三问示意图（已生成）：三个圆形图标配中性简笔轮廓，附中文标注\n- P7 问题解决四步流程图（已生成）：四个方框与箭头，附中文标注\n- 三张图均为中性简洁教学插画，人物只用简单图形，不使用真实儿童照片或可识别肖像\n- 若需补充：班级「行动小卡」空白模板（可印发作课堂用纸）",
}
