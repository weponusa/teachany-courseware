# -*- coding: utf-8 -*-
"""小学心理健康 · 入学适应与规则意识（G1）—— 补齐知识树「生活适应」空缺

学科语气（心理健康）：温和、不评判、不贴标签；不出现任何临床诊断词汇。
一年级落点：全部换成具体动作（"上课前把书摆好""想说话先举手"），不讲抽象心理概念。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/psych-e-g1-school-adapt-fig1.webp'
F2 = './assets/psych-e-g1-school-adapt-fig2.webp'

TTS = {
    "hero": "小朋友，今天是你上小学的日子。校门好大，人好多，你可能有点紧张，也可能有一点想妈妈。没关系的，很多小朋友第一天都是这样。这节课我们一起来做三件事：认一认学校里的地方，学几条特别具体的小规则，再知道遇到不认识的事情可以问谁。学完你会发现，学校是个很安全的地方。",
    "problem-anchor": "开始之前，先选一个你最想知道的事。是想认一认学校里都有哪些地方，还是想知道上课、课间、吃饭该怎么安排，或者你想学几条保护自己的小规则，再或者你想知道心里有点紧张的时候可以怎么办。选好了，就带着它往下看。",
    "objectives": "这节课有四个小目标。第一，能说出学校里几个常用的地方，知道每个地方是做什么用的。第二，能说出三条以上在学校要遵守的规则，比如上课前把书摆好、想说话先举手。第三，能自己安排好一天里的几件事，知道什么时候做什么。第四，遇到不认识、不确定的事情，知道可以去问谁。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先来认一认学校。学校里有教室，是上课的地方；有饮水处，口渴了可以去接水；有卫生间；有操场，课间和体育课在那里活动；还有保健室，身体不舒服可以去。把这些地方认清楚，你在学校里就不会迷路，心里也会踏实很多。",
    "lab-1": "现在请你当一次上学小向导。这里有六个情境，每个情境里都有三个做法。你选一个你觉得合适的，选完立刻会有一段话告诉你为什么；要是选得不太合适，也会告诉你还可以试试什么。",
    "module-2": "学校里为什么要有规则呢？你可以把规则想成小路两旁的栏杆。有了栏杆，大家走起来才不挤，也不容易摔跤。上课前把书和铅笔盒摆好，上课的时候眼睛看老师，想说话先举手，课间走路慢慢走，这些都是特别具体的小事，做到一件，就是做好一次。",
    "lab-2": "现在我们动手做一本我的规则小书。下面有六个做法，请你判断一下：哪些是本来就可以做的，放进要做的那一筐；哪些是要先问一问老师或者爸爸妈妈的，放进先问一问的那一筐。放好以后，可以再点一点，看看为什么。",
    "worked-example": "我们一起来帮小豆想一想。小豆第一天上小学，到了教室门口，不知道该做什么。第一步，他先在门口停一停，看看教室里的同学在做什么。第二步，他找到自己的座位，把书包放好，把语文书和铅笔盒摆在桌角。第三步，上课铃响了，他坐好，眼睛看老师。第四步，课间他想上厕所，先问了老师，老师点点头，他就放心地去了。",
    "conceptest-1": "接下来用三个说法考考你，每一个说法里都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件事交给你。一天里的事情被我打乱了，请你按照从早到晚的顺序，一步一步点出来。排错了会给你一个提示，你可以再试一次。",
    "posttest": "最后一轮，换几个新的小情境来考考你。这次会出现下雨天、不认识的人和座位旁边的新同学，看看你能不能用上今天学到的办法。",
    "summary": "这节课我们记住三句话。第一句，学校里有教室、饮水处、卫生间、操场和保健室，把它们认清楚，心里就不慌。第二句，规则就像小路两旁的栏杆，上课前把书摆好、想说话先举手、课间慢慢走，都是很简单的小事。第三句，遇到不认识、不确定的事情，可以先问老师，也可以回家问爸爸妈妈——问一问，是很聪明的做法。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出学校里三个地方，再说说它们是做什么用的。第二层能力应用，动手做：和爸爸妈妈一起画一张我的上学一天小地图，把每天要去的几个地方标出来。第三层迁移挑战，选做：和同桌一起，给我们班的规则小书补充两条，写清楚为什么要有这一条。",
    "knowledge-graph": "这张图展示了这节课在心理健康知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 认一认我们的学校", "lab-1": "动手一 上学一天", "module-2": "概念二 规则像小路两旁的栏杆",
    "lab-2": "动手二 我的规则小书", "worked-example": "例题讲解 小豆的第一天", "conceptest-1": "概念测试",
    "synthesis": "综合任务 一天排一排", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：上学一天的六个情境（真实反馈文案，错误选项也要温和） ──
SCENES = [
    {
        "id": "s1",
        "t": "早上走进教室，我想坐好准备上课",
        "opts": [
            {"k": "a", "t": "先把书包放好，把语文书和铅笔盒摆在桌角", "ok": True,
             "fb": "这样安排真好。上课要用的时候，一伸手就能拿到，心里也不会慌。"},
            {"k": "b", "t": "先把书包里的玩具拿出来玩一会儿", "ok": False,
             "fb": "这样也说得过去，只是上课铃响的时候可能还没准备好。还可以试试：先把上课要用的书和笔摆好，玩具留到家里玩。"},
            {"k": "c", "t": "趴在桌上等老师来", "ok": False,
             "fb": "可能是有点累了。还可以试试：坐起来一点，眼睛看看老师来了没有，这样不会错过老师说的第一句话。"},
        ],
    },
    {
        "id": "s2",
        "t": "上课的时候，我特别想说话",
        "opts": [
            {"k": "a", "t": "先把手举起来，等老师请我再说", "ok": True,
             "fb": "这是很好的办法。举了手，老师就知道你有话要说，其他同学也能听清老师讲话。"},
            {"k": "b", "t": "直接大声说出来", "ok": False,
             "fb": "你想说的这句话很重要，只是这样可能会打断老师和其他同学。还可以试试：先举手，等老师看到你。"},
            {"k": "c", "t": "小声和同桌说", "ok": False,
             "fb": "小声也会让旁边的人听不清老师说话。还可以试试：先把想说的话在心里放一放，举手以后再说出来。"},
        ],
    },
    {
        "id": "s3",
        "t": "课间，我想去上厕所",
        "opts": [
            {"k": "a", "t": "跟老师说一声，然后去", "ok": True,
             "fb": "这样最稳当。老师知道你去了哪里，也就不会到处找你。"},
            {"k": "b", "t": "不告诉任何人，自己跑出去", "ok": False,
             "fb": "你大概是想快去快回。只是老师找不到你，会有点担心。还可以试试：出门前跟老师说一句我马上回来。"},
            {"k": "c", "t": "先忍一忍，等上课了再说", "ok": False,
             "fb": "忍太久自己会难受，上课再去也会漏掉功课。还可以试试：课间就把这件事做好。"},
        ],
    },
    {
        "id": "s4",
        "t": "我找不到自己的教室了",
        "opts": [
            {"k": "a", "t": "找一位老师，告诉她我是几班的", "ok": True,
             "fb": "这样做很聪明。老师最熟悉学校，一听班号就能带你回去。"},
            {"k": "b", "t": "自己一个班一个班地找", "ok": False,
             "fb": "你很勇敢，想自己解决。只是走廊很长，可能会越走越远。还可以试试：先找一位老师帮个忙。"},
            {"k": "c", "t": "站在走廊上等别人来问我", "ok": False,
             "fb": "站在那里等着，心里会更着急。还可以试试：走到一位老师身边，说一句我找不到教室了。"},
        ],
    },
    {
        "id": "s5",
        "t": "中午吃饭前，我想洗手",
        "opts": [
            {"k": "a", "t": "排好队，一个一个来", "ok": True,
             "fb": "排队的人看起来慢，其实很快。大家都洗得干净，也没有人会被挤到。"},
            {"k": "b", "t": "挤到前面去先洗", "ok": False,
             "fb": "你可能是肚子饿了。只是往前挤，旁边的同学容易站不稳。还可以试试：站到队尾，一会儿就轮到了。"},
            {"k": "c", "t": "不洗了，直接去拿饭", "ok": False,
             "fb": "小手上有看不见的脏东西。还可以试试：先去洗一洗，再回来拿饭，吃起来更放心。"},
        ],
    },
    {
        "id": "s6",
        "t": "放学了，家长还没来接我",
        "opts": [
            {"k": "a", "t": "回到老师身边，在老师能看到的地方等", "ok": True,
             "fb": "这个做法最安全。老师会陪着你等，也会帮你联系家里人。"},
            {"k": "b", "t": "自己走出校门去找", "ok": False,
             "fb": "你想快点见到家人。只是校门外车多人多，一个人走会有危险。还可以试试：先回到老师身边，让老师帮忙联系。"},
            {"k": "c", "t": "和同学一起走回家", "ok": False,
             "fb": "有伙伴一起好像胆子大一些。只是没有大人同意就自己走，家长会非常担心。还可以试试：先告诉老师，等家长来接。"},
        ],
    },
]

# ── 动手二：我的规则小书（两个筐） ──
RULES = [
    {"id": "r1", "t": "上课前把书和铅笔盒摆好", "bin": "do",
     "why": "这是上课前就能做好的准备。做到它，上课会更顺手。"},
    {"id": "r2", "t": "想说话先举手", "bin": "do",
     "why": "举手是一种不打扰别人的说话方式，可以放心做。"},
    {"id": "r3", "t": "课间走路慢慢走", "bin": "do",
     "why": "走廊里人很多，慢慢走最稳当，别人也安全。"},
    {"id": "r4", "t": "想借同学的橡皮", "bin": "ask",
     "why": "那是同学的东西，先问一问他愿不愿意，他同意了再拿。"},
    {"id": "r5", "t": "上课时想离开教室去厕所", "bin": "ask",
     "why": "先告诉老师一声，老师才知道你在哪里。"},
    {"id": "r6", "t": "想把自己的玩具带到学校", "bin": "ask",
     "why": "学校有学校的安排，先问一问老师可不可以带。"},
]
BIN_NAME = {"do": "要做的", "ask": "先问一问的"}

# ── 综合任务：我的一天（打乱顺序，学生排出来） ──
DAY_STEPS = [
    {"id": "d1", "t": "出门前，检查书包和水杯"},
    {"id": "d2", "t": "到校进教室，把书和文具摆好"},
    {"id": "d3", "t": "上课铃响，坐好，眼睛看老师"},
    {"id": "d4", "t": "课间喝水、上厕所，走路慢慢走"},
    {"id": "d5", "t": "放学排队，在老师身边等家长"},
]
DAY_RIGHT = ["d1", "d2", "d3", "d4", "d5"]

CUSTOM_JS = r"""
/* ============================================================
   psych-e-g1-school-adapt 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 上学一天：六个情境 × 三个做法 → 温和反馈（不评判、不贴标签）
   3) 我的规则小书：六个做法分进「要做的 / 先问一问的」两个筐
   4) 我的一天：五步按从早到晚排出来
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

  /* ---------- 2. 上学一天 ---------- */
  var SCENES = __SCENES_JSON__;
  var stage1 = document.getElementById('day-stage');
  if (stage1) {
    var curScene = null, doneScene = {};
    var out1 = document.getElementById('day-out');
    var score1 = document.getElementById('day-score');

    function sceneById(id) {
      for (var i = 0; i < SCENES.length; i++) { if (SCENES[i].id === id) return SCENES[i]; }
      return null;
    }

    function render1() {
      document.querySelectorAll('[data-scene]').forEach(function (b) {
        var k = b.dataset.scene;
        b.classList.toggle('selected', k === curScene);
        b.classList.toggle('correct', !!doneScene[k]);
        b.classList.toggle('done', !!doneScene[k]);
      });
      var n = Object.keys(doneScene).length;
      score1.textContent = '已经聊过 ' + n + ' / ' + SCENES.length + ' 个情境';
    }

    function paintOptions() {
      var box = document.getElementById('day-opts');
      box.innerHTML = '';
      if (!curScene) return;
      var S = sceneById(curScene);
      if (!S) return;
      S.opts.forEach(function (o) {
        var b = document.createElement('button');
        b.className = 'choice' + (doneScene[curScene] && o.ok ? ' correct' : '');
        b.style.textAlign = 'left';
        b.textContent = o.t;
        b.addEventListener('click', function () {
          if (doneScene[curScene]) return;
          if (o.ok) {
            doneScene[curScene] = true;
            out1.className = 'result';
            out1.innerHTML = '<strong>这个办法挺好。</strong>' + o.fb;
          } else {
            out1.className = 'result warn';
            out1.innerHTML = '<strong>还可以再想一想。</strong>' + o.fb;
          }
          render1();
          paintOptions();
        });
        box.appendChild(b);
      });
    }

    document.querySelectorAll('[data-scene]').forEach(function (b) {
      b.addEventListener('click', function () {
        curScene = b.dataset.scene;
        var S = sceneById(curScene);
        if (doneScene[curScene]) {
          out1.className = 'result';
          out1.innerHTML = '<strong>这件事已经聊过啦。</strong>你上次选的做法很合适，记住它就好。';
        } else {
          out1.className = 'result warn';
          out1.innerHTML = '<strong>你遇到的是：' + S.t + '</strong><br>下面有三个做法，你选一个试试看。';
        }
        render1();
        paintOptions();
      });
    });
    render1();
  }

  /* ---------- 3. 我的规则小书 ---------- */
  var RULES = __RULES_JSON__;
  var stage2 = document.getElementById('book-stage');
  if (stage2) {
    var picked = null, placed = {};
    var out2 = document.getElementById('book-out');
    var WHYN = { do: '要做的', ask: '先问一问的' };

    function render2() {
      document.querySelectorAll('[data-rule]').forEach(function (b) {
        var k = b.dataset.rule;
        b.classList.toggle('selected', k === picked);
        b.classList.toggle('done', !!placed[k]);
        b.disabled = !!placed[k];
      });
      var n = Object.keys(placed).length;
      document.getElementById('book-score').textContent = '已经放进小书 ' + n + ' / ' + RULES.length + ' 条';
      var doBox = document.getElementById('book-do');
      var askBox = document.getElementById('book-ask');
      doBox.innerHTML = ''; askBox.innerHTML = '';
      RULES.forEach(function (r) {
        if (!placed[r.id]) return;
        var s = document.createElement('div');
        s.className = 'tag';
        s.textContent = r.t;
        (r.bin === 'do' ? doBox : askBox).appendChild(s);
      });
      if (!doBox.innerHTML) doBox.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
      if (!askBox.innerHTML) askBox.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
    }

    document.querySelectorAll('[data-rule]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (placed[b.dataset.rule]) return;
        picked = b.dataset.rule;
        out2.className = 'result warn';
        out2.innerHTML = '<strong>你选的是：' + b.textContent + '</strong><br>想一想，它应该放进哪一筐？';
        render2();
      });
    });

    document.querySelectorAll('[data-bin]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!picked) {
          out2.className = 'result warn';
          out2.textContent = '先在上面点一条做法，再选筐。';
          return;
        }
        var r = null;
        for (var i = 0; i < RULES.length; i++) { if (RULES[i].id === picked) r = RULES[i]; }
        if (b.dataset.bin === r.bin) {
          placed[r.id] = true;
          out2.className = 'result';
          out2.innerHTML = '<strong>放对了，它属于「' + WHYN[r.bin] + '」。</strong>' + r.why;
          picked = null;
        } else {
          out2.className = 'result warn';
          out2.innerHTML = '<strong>再想一想「' + r.t + '」。</strong>' + r.why +
            '<br><span style="color:var(--muted)">常见错误：容易把「我自己想做的事」和「可以自己做主的事」搞混。拿不准的时候，先问一问，是很好的办法。</span>';
        }
        render2();
      });
    });
    render2();
  }

  /* ---------- 4. 我的一天 ---------- */
  var DAY = __DAY_JSON__;
  var RIGHT = __DAY_RIGHT_JSON__;
  var stage3 = document.getElementById('order-day-stage');
  if (stage3) {
    var placed3 = [];
    var out3 = document.getElementById('order-day-out');
    var TIP = {
      d1: '出门前检查一遍，到了学校才不会发现少了东西。',
      d2: '到了教室先安顿好自己，上课就顺了。',
      d3: '上课的时候坐好、看老师，这是学得最清楚的时候。',
      d4: '课间先把身体的事情做好：喝水、上厕所，走路慢慢走。',
      d5: '放学了，在老师身边等家长，最安全。'
    };
    function render3() {
      var bar = document.getElementById('order-day-done');
      bar.innerHTML = placed3.length
        ? placed3.map(function (k, i) {
            var t = ''; for (var j = 0; j < DAY.length; j++) { if (DAY[j].id === k) t = DAY[j].t; }
            return '<span class="tag">第' + (i + 1) + '步 · ' + t + '</span>';
          }).join(' ')
        : '<span style="color:var(--muted)">还没有排出第一步。</span>';
      document.querySelectorAll('[data-day]').forEach(function (b) {
        var k = b.dataset.day;
        b.disabled = placed3.indexOf(k) !== -1;
        b.classList.toggle('done', placed3.indexOf(k) !== -1);
      });
    }
    document.querySelectorAll('[data-day]').forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.dataset.day;
        if (placed3.indexOf(k) !== -1) return;
        if (RIGHT[placed3.length] === k) {
          placed3.push(k);
          out3.className = 'result';
          out3.innerHTML = '<strong>第 ' + placed3.length + ' 步排好了。</strong>' + TIP[k];
          if (placed3.length === DAY.length) {
            out3.className = 'result';
            out3.innerHTML = '<strong>五步全排对了！</strong>我的一天就是：<strong>出门前检查 → 到校摆好书 → 上课坐好看老师 → 课间做好身体的事 → 放学在老师身边等家长。</strong>';
          }
        } else {
          out3.className = 'result warn';
          out3.innerHTML = '<strong>这一步放得早了一点。</strong>想一想，一天是从哪里开始的？' +
            '<br><span style="color:var(--muted)">常见错误：容易只按「我喜欢做的事」来排，忘了先做该做的事。再试一次。</span>';
        }
        render3();
      });
    });
    render3();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__SCENES_JSON__', json.dumps(SCENES, ensure_ascii=False))
             .replace('__RULES_JSON__', json.dumps(RULES, ensure_ascii=False))
             .replace('__DAY_JSON__', json.dumps(DAY_STEPS, ensure_ascii=False))
             .replace('__DAY_RIGHT_JSON__', json.dumps(DAY_RIGHT, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "上课的时候，我很想说话，怎么做比较合适？",
         "options": [("先举手，等老师请我再说", True),
                     ("直接大声说出来", False),
                     ("小声和同桌说", False)],
         "explain": "举了手，老师就知道你有话要说，别的同学也还能听清老师讲话。"
                    "<strong>错因提醒：</strong>常见错误是把「想说话」和「马上说出来」搞混了——先举手，是让大家都方便的做法。"},
        {"q": "在学校里，我忽然找不到自己的教室了，怎么做比较好？",
         "options": [("找一位老师，告诉她我是几班的", True),
                     ("自己一个班一个班地找", False),
                     ("站在走廊上等别人来问", False)],
         "explain": "老师最熟悉学校，一听班号就能带你回去。"
                    "<strong>错因提醒：</strong>有些小朋友误认为「自己找显得能干」，其实开口问一问，是又聪明又安全的做法。"},
        {"q": "课间十分钟，哪一件事最好先做好？",
         "options": [("先去喝水、上厕所", True),
                     ("一直玩到上课铃响", False),
                     ("坐在座位上一动不动", False)],
         "explain": "课间先把身体的事情做好，上课才能安心。"
                    "<strong>错因提醒：</strong>容易把课间当成「只有玩」的时间，结果一上课就着急——先把该做的做完，玩起来也更放心。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "认一认我们的学校，心里就不慌", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">在幼儿园里，我们已经知道口渴了要喝水、想上厕所要说一声（And）；可是小学比幼儿园大得多，教室、操场、保健室都在不同的地方，第一天走进来，很容易不知道往哪走（But）；所以我们先来认一认这些地方，知道每个地方做什么用，心里就有底了（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">学校就像一个大院子，里面有几个<strong>每天都会去的地方</strong>。认清楚它们，你在学校里就不会迷路。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>教室里要用的</strong></p>
            <p style="color:var(--muted)">自己的座位、放书包的地方、黑板和讲台。上课、写字、听老师说话，都在这里。</p>
          </div>
          <div class="inner-card">
            <p><strong>课间要去的</strong></p>
            <p style="color:var(--muted)">饮水处接水，卫生间上厕所，操场课间活动——这三件事都在课间做好。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="学校常用地点示意图：教室、饮水处、卫生间、操场、保健室，附中文标注">
          <figcaption>示意图：学校里每天都会用到的几个地方——把它们认清楚，走到哪里都不慌（教学示意图，非实景照片）</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🏫</span><div><strong>一句小口诀：</strong>教室上课、水房接水、厕所课间去、操场活动、保健室不舒服就去——<strong>认得路，心不慌。</strong></div></div>
{insight_box([
    {"lens": "看见它", "text": "学校里每一个地方都有自己的名字和用处，就像家里有厨房、有卧室一样，各有各的事要做。"},
    {"lens": "解释它", "text": "为什么认得路，心里就踏实？因为知道自己在哪里、接下来要去哪，不用一直猜来猜去，力气就省下来学东西了。"},
    {"lens": "迁移它", "text": "换一个新地方也一样：先去认一认门在哪里、卫生间在哪里、找不到路的时候可以问谁。这个办法到哪里都能用。"},
])}
    ''', tag="概念一"))

    scene_btns = "\n".join(
        f'            <button class="choice" data-scene="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in SCENES
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：上学一天，你会怎么做？", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一件你今天可能遇到的事，再从三个做法里选一个。<strong>选得好会告诉你为什么，选得不太合适也会告诉你还可以试试什么</strong>。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 今天我遇到的一件事</div>
          <div class="grid" id="day-stage">
{scene_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 我可以怎么做</div>
          <div class="grid" id="day-opts">
            <span style="color:var(--muted);font-size:14px">先在上面点一件事，这里就会出现三个做法。</span>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">聊过几个情境</span><span class="v" id="day-score">已经聊过 0 / 6 个情境</span></div>
          </div>
          <p class="result warn" id="day-out" style="margin-top:12px">先点一件今天可能遇到的事。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💛</span><div><strong>说给你听：</strong>这里的做法没有「对」和「错」的分数。有些做法只是会让你麻烦一点，换一个试试就好。拿不准的时候，问老师、问家长，都是很好的办法。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "规则就像小路两旁的栏杆", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">规则不是用来管住谁的，它更像<strong>小路两旁的栏杆</strong>：有了它，大家走起来不挤，也不容易摔跤。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>上课前：</strong>把书和铅笔盒摆在桌角，人坐好。</div></div>
          <div class="step"><span class="n">2</span><div><strong>上课时：</strong>眼睛看老师，想说话先举手。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>课间：</strong>走路慢慢走，喝水、上厕所先做好，离开教室先跟老师说一声。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="规则像小路两旁的栏杆示意图：有栏杆时大家依次通过，附中文标注">
          <figcaption>示意图：规则就像小路两旁的栏杆——不挡着你走，而是让大家都能稳稳地走过去（教学示意图，人物为极简线条）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「老师没看见，规则就可以不做」。其实这些小事的好处，先落在自己身上：书摆好了，自己一伸手就能拿到；走路慢慢走，摔跤的也不会是自己。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>书摆好，手举起，慢慢走——<strong>做到一件，就是做好一次。</strong></div></div>
{insight_box([
    {"lens": "看见它", "text": "规则不在墙上，它就在每个人的动作里：把书摆好、举手、慢慢走，这些都是规则本来的样子。"},
    {"lens": "比较它", "text": "一条没有栏杆的小路，看着自由，可人一多就挤；一条有栏杆的小路，走得稳，人人都能过去。"},
    {"lens": "迁移它", "text": "在家里、过马路、坐公交车，也都有这样的规则。做法不一样，道理是同一个：让大家都方便、都安全。"},
])}
    ''', tag="概念二"))

    rule_btns = "\n".join(
        f'            <button class="choice" data-rule="{r["id"]}" style="text-align:left">{r["t"]}</button>'
        for r in RULES
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：我的规则小书，把做法分进两个筐", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一条做法，再点它应该进的筐。<strong>要做的</strong>放进上筐，<strong>先问一问的</strong>放进下筐。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 挑一条做法</div>
          <div class="grid" id="book-stage">
{rule_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 它应该放进哪一筐</div>
          <div class="grid grid-2">
            <button class="choice" data-bin="do" style="text-align:center">要做的</button>
            <button class="choice" data-bin="ask" style="text-align:center">先问一问的</button>
          </div>
          <div class="inner-card" style="margin-top:14px">
            <p><strong>我的规则小书</strong></p>
            <p style="margin:6px 0 4px"><strong>要做的</strong></p>
            <div id="book-do" style="display:flex;flex-wrap:wrap;gap:6px"><span style="color:var(--muted);font-size:14px">还没有放进来。</span></div>
            <p style="margin:10px 0 4px"><strong>先问一问的</strong></p>
            <div id="book-ask" style="display:flex;flex-wrap:wrap;gap:6px"><span style="color:var(--muted);font-size:14px">还没有放进来。</span></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">小书进度</span><span class="v" id="book-score">已经放进小书 0 / 6 条</span></div>
          </div>
          <p class="result warn" id="book-out" style="margin-top:12px">先在上面点一条做法。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">📖</span><div><strong>拿不准怎么办？</strong>如果一件事是「我自己就能做好的准备」，放进要做的；如果它关系到别人的东西、或者要离开教室，就先问一问。问，一点也不丢人。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小豆的第一天", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>小豆第一天上小学，站在教室门口，不知道该做什么。请你帮他一步一步想清楚。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先停一停，看一看：</strong>在门口站一下，看看教室里的同学在做什么，不着急往里冲。</div></div>
          <div class="step"><span class="n">2</span><div><strong>找到自己的座位：</strong>把书包放好，把语文书和铅笔盒摆在桌角。</div></div>
          <div class="step"><span class="n">3</span><div><strong>上课铃响了：</strong>坐好，眼睛看老师，想说话先举手。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>课间想上厕所：</strong>先跟老师说一句「我去卫生间」，老师点点头，再放心地去。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「到了教室要马上做点什么，才不显得笨」。其实第一天完全可以先看一看、再慢慢来。小豆的四步里，最要紧的是第一步——<strong>不着急，先看清楚</strong>。</p>
        </div>
        <div class="inner-card">
          <p><strong>说给同桌听：</strong>小豆这四步里，哪一步你自己已经做到了？哪一步还想再练一练？</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "下面哪句话说得对？",
         "options": [("学校里的规则，是为了让大家更安全、更舒服", True),
                     ("规则就是专门用来管人的", False),
                     ("只要老师没看见，有些规则就不用做", False)],
         "explain": "规则像小路两旁的栏杆，保护的是走在路上的每一个人。"
                    "<strong>错因提醒：</strong>常见错误是误认为规则只是来限制自己的——它其实是让大家都方便的约定。"},
        {"q": "上课前把书和铅笔盒摆好，最大的好处是：",
         "options": [("上课要用的时候，一伸手就能拿到", True),
                     ("老师会表扬我", False),
                     ("同桌会羡慕我", False)],
         "explain": "做好准备，最先方便的是自己。"
                    "<strong>错因提醒：</strong>不要把「把事做好」和「为了被夸」搞混——就算没人看见，书摆好了，你自己也少着急一次。"},
        {"q": "心里有点紧张、有点想妈妈的时候，下面哪个做法更合适？",
         "options": [("跟老师说一说心里的感觉", True),
                     ("一直忍着，什么都不说", False),
                     ("马上跑出教室去找妈妈", False)],
         "explain": "把感觉说出来，老师才知道怎么帮你。"
                    "<strong>错因提醒：</strong>有人误认为「说出来是胆小」，其实能说出自己的感觉，是很勇敢、也很聪明的做法。"}
    ], tag="概念测试"))

    day_btns = "\n".join(
        f'            <button class="sort-item" data-day="{d["id"]}">{d["t"]}</button>' for d in DAY_STEPS
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：把「我的一天」排一排", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">下面五件事被打乱了。请你按<strong>从早到晚</strong>的顺序，一步一步点出来。</p>
        <div class="lab-panel">
          <div class="sort-bank" id="order-day-stage">
{day_btns}
          </div>
          <div class="inner-card" style="margin-top:14px">
            <p><strong>我排出来的一天</strong></p>
            <p id="order-day-done" style="color:var(--muted)">还没有排出第一步。</p>
          </div>
          <p class="result warn" id="order-day-out" style="margin-top:12px">请点出你认为的第一步。</p>
        </div>
        <div class="inner-card">
          <p><strong>排完之后，想一想：</strong></p>
          <p style="color:var(--muted)">这五步里，哪一步最容易被忘掉？忘掉以后会带来什么小麻烦？</p>
          <p style="color:var(--muted)">再把它<strong>画出来</strong>：五个小方框，用箭头连起来，就成了你自己的「上学一天图」。</p>
          <textarea id="syn-answer" rows="3" placeholder="最容易忘掉的是……，因为……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，做法还在不在", TTS["posttest"], [
        {"q": "下雨天，你的伞放在教室门口的桶里，放学时发现伞不见了，你会：",
         "options": [("告诉老师，请老师帮忙一起找", True),
                     ("自己去翻别人的书包", False),
                     ("拿一把别人的伞先回家", False)],
         "explain": "告诉老师最稳当，老师认识班里的每一位同学，找起来也快。"
                    "<strong>错因提醒：</strong>不要把「着急」和「随便拿」搞混——再着急，也不能动别人的东西。"},
        {"q": "校门口有个不认识的大人跟你说「我带你去找妈妈」，你会：",
         "options": [("不跟他走，回到老师身边", True),
                     ("跟他走，他看起来不凶", False),
                     ("先跟他说说我家的事", False)],
         "explain": "不认识的人要带你走，不可以答应，要马上回到老师身边。"
                    "<strong>错因提醒：</strong>常见错误是误认为「看起来和善」就等于「可以信任」。认不认识，比凶不凶更重要。"},
        {"q": "班上来了一位新同学，一个人坐在座位上，你会：",
         "options": [("走过去打个招呼，问他要不要一起玩", True),
                     ("远远看着他，不说话", False),
                     ("跟别人说他不爱说话", False)],
         "explain": "一句招呼，就能让人觉得自己是被欢迎的。"
                    "<strong>错因提醒：</strong>别把「他没说话」当成「他不想交朋友」——先打个招呼，再看他怎么回应，这样更公平。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，讲清入学这件事", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>认得地方：</strong>教室、饮水处、卫生间、操场、保健室——认清楚，走到哪里都不慌。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>记住小事：</strong>上课前把书摆好，想说话先举手，课间慢慢走。做到一件，就是做好一次。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>有事就问：</strong>找不到教室、不认识的人要带你走、心里紧张——先说给老师听。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>还要记牢一件事：</strong>刚上小学，有点紧张、有点想家，很多小朋友都会这样，你一点也不奇怪。慢慢地，学校会变成你熟悉的地方。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「地方、规则、问一问」这三个词，说清楚你今天在学校做对的一件事。</p>
          <p style="color:var(--muted)">再动一动手：<strong>画一画</strong>从校门到你的教室，路上会经过哪些地方，把它们标在纸上。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "说出学校里三个地方，再说说它们是做什么用的。",
            "说出三条在学校要做到的小事，每条用一句话说清楚。",
        ],
        [
            "和爸爸妈妈一起画一张「我的上学一天」小地图，把每天要去的几个地方标出来。",
            "把「我的规则小书」里的六条念给家里人听，请他们帮你检查有没有漏掉的。",
        ],
        [
            "和同桌一起，给我们班的规则小书补充两条，写清楚为什么要有这一条。",
            "想一想：家里也有类似的小规则吗？挑一条写在纸上，说说它保护了什么。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "psych-e-g1-school-adapt",
    "node_id": "psych-e-g1-school-adapt",
    "subject": "psychology",
    "subject_cn": "心理健康",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "中小学心理健康教育指导纲要（2012年修订）/ 教育部相关要求 · 小学",
    "title": "入学适应与规则意识",
    "name_en": "Starting Primary School: Getting Used to It and Learning the Rules",
    "grade": 1,
    "grade_cn": "一年级",
    "domain": "life-adaptation",
    "domain_cn": "生活适应",
    "lesson_type": "workshop",
    "version": "1.0.0",
    "description": "面向小学一年级新生的入学适应课：先认一认学校里的常用地方，再把「上课前把书摆好」「想说话先举手」「课间慢慢走」这些具体小事练成习惯，最后知道遇到不认识、不确定的事情可以问老师、问家长，从而对学校产生安全感和归属感。",
    "tags": ["入学适应", "规则意识", "校园安全", "一年级", "生活适应"],
    "standard_ref": "《中小学心理健康教育指导纲要（2012年修订）· 小学低年级》生活适应——认识班级、学校与日常学习生活环境及基本规则；适应新环境、新集体和新的学习生活，树立纪律意识、时间意识和规则意识；使学生有安全感和归属感，初步学会自我控制。",
    "hero_question": "第一天走进校门，心里有点紧张，该怎么办？",
    "hero_alt": "入学适应与规则意识知识结构图：认得地方、记住小事、有事就问 三栏",
    "hero_caption": "入学适应：认得地方心不慌 · 记住小事好上课 · 有事就问最妥当",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "学校里都有哪些地方？", "d": "教室、水房、卫生间、操场都在哪里", "v": "学校里都有哪些地方"},
        {"t": "上课、课间该做什么？", "d": "一天里的几件事该按什么顺序做", "v": "上课课间该做什么"},
        {"t": "学校里有哪些要做的小事？", "d": "哪些是我自己就能做好的", "v": "学校里有哪些要做的小事"},
        {"t": "紧张、想妈妈的时候怎么办？", "d": "心里不舒服可以说给谁听", "v": "紧张想妈妈的时候怎么办"},
    ],
    "objectives": [
        "能说出学校里几个常用地方，知道每个地方是做什么用的",
        "能说出三条以上在学校要做到的小事，例如上课前把书摆好、想说话先举手",
        "能按从早到晚的顺序安排一天里的几件事，知道什么时候做什么",
        "遇到不认识、不确定的事情，知道可以问老师、问家长，心里有安全感",
    ],
    "objectives_plain": [
        "能说出学校里几个常用地方，知道每个地方是做什么用的",
        "能说出三条以上在学校要做到的小事，例如上课前把书摆好、想说话先举手",
        "能按从早到晚的顺序安排一天里的几件事，知道什么时候做什么",
        "遇到不认识、不确定的事情，知道可以问老师、问家长，心里有安全感",
    ],
    "standards": [
        {"content": "帮助学生认识班级、学校、日常学习生活环境和基本规则",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学低年级 · 生活适应"},
        {"content": "帮助学生适应新环境、新集体和新的学习生活，树立纪律意识、时间意识和规则意识；使学生有安全感和归属感，初步学会自我控制",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学低年级 · 生活适应"},
    ],
    "prereqs": [],
    "prereqs_name": "本课是小学心理健康「生活适应」的起始课，不需要先修节点",
    "prereqs_meta": "",
    "leads_to": ["psych-e-g1-learning-habit"],
    "next_meta": "psych-e-g1-learning-habit",
    "section_images": ["assets/psych-e-g1-school-adapt-fig1.webp", "assets/psych-e-g1-school-adapt-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "第一天上学，有点紧张很正常——先认认路、学几件小事，心里就有底了。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能说出学校里的地方和三条要做的小事。",
        "objectives": "看清四件事：认得地方、记住小事、排好一天、有事会问。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "教室上课、水房接水、卫生间课间去、操场活动、保健室不舒服就去。认得路，心不慌。",
        "lab-1": "六个情境，每个都有三个做法。选得不太合适也不会说你错，只会告诉你还可以试试什么。",
        "module-2": "规则像小路两旁的栏杆：书摆好、手举起、慢慢走，做到一件就是做好一次。",
        "lab-2": "拿不准就先问一问：关系到别人的东西，或者要离开教室，都该先问。",
        "worked-example": "小豆的四步：先停一停、找到座位摆好书、上课坐好看老师、课间先跟老师说一声。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "一天是从出门前开始的，按从早到晚的顺序点出来，点错了会有提示。",
        "posttest": "出现了下雨天、陌生人和新同学，看看你能不能把今天的办法用上去。",
        "summary": "三句话：认得地方、记住小事、有事就问。",
        "homework": "三层小任务，先做前两层，第三层可以请同桌一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学心理健康「生活适应」的起始课，正对一年级新生入学适应与规则意识。一年级学生的难点不在理解概念，而在「知道该怎么做具体的一件事」——所以全课不讲抽象心理概念，只做三件能落地的事：认地方（教室、饮水处、卫生间、操场、保健室）、做小事（上课前把书摆好、想说话先举手、课间慢慢走）、会求助（找不到教室、陌生人要带走、心里紧张都说给老师听）。两个互动台子都能真的操作：一个是六个「上学一天」情境卡片，选做法后给出即时反馈，反馈一律写成「还可以试试……」而不判错、不贴标签；一个是「我的规则小书」，把六个做法分进「要做的／先问一问的」两个筐。综合任务把一天的五步打乱，让学生自己排出从早到晚的顺序。全课只用「地方、规则、问一问」三个词收口，插图一律为中性简洁的教学示意图（极简线条人物，不使用真实儿童照片）。",
    "plan_table": """| 1 | cover | 入学适应与规则意识 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 认一认我们的学校，心里就不慌 | 承·概念一（认识环境） |
| 6 | interactive | 动手一：上学一天，你会怎么做？ | 承·情境判断（温和反馈，不判错） |
| 7 | concept | 规则就像小路两旁的栏杆 | 承·概念二（规则与纪律、时间意识） |
| 8 | interactive | 动手二：我的规则小书，把做法分进两个筐 | 承·分类操作（要做的／先问一问的） |
| 9 | concept | 例题示范：小豆的第一天 | 转·重难点突破（分步示范 + 易错点） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：把「我的一天」排一排 | 合·迁移应用（排序模拟） |
| 12 | quiz | 后测：换几个新情境，做法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，讲清入学这件事 | 合·小结与复述 |
| 14 | homework | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：认得地方 / 记住小事 / 有事就问 三栏\n- P5 学校常用地点示意图（已生成）：教室、饮水处、卫生间、操场、保健室，附中文标注\n- P7 规则栏杆示意图（已生成）：有栏杆的小路走得稳，附中文标注\n- 三张图均为教学示意图，人物仅用极简线条，不使用任何真实儿童照片或可识别肖像\n- 若需补充：本校校园平面图（需学校提供并授权后使用）",
}
