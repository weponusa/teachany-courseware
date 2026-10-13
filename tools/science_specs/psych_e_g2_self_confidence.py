# -*- coding: utf-8 -*-
"""小学心理健康 · 自信与集体归属感（G2）—— 补齐知识树「人际交往」空缺

学科语气（心理健康）：温和、不评判、不贴标签；不出现任何临床诊断词汇，不涉及自伤自杀。
二年级落点：把"我有点不敢"的事拆成三小步一步一步做完（长信心），再找到"我能为班级做的事"（归属感）。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/psych-e-g2-self-confidence-fig1.webp'
F2 = './assets/psych-e-g2-self-confidence-fig2.webp'

TTS = {
    "hero": "小朋友，你有没有过这样的时候：有一件事你其实很想做，可心里一直有个小小的声音在说，我不敢。可能是举手发言，可能是上台读课文，也可能是走过去跟同学说一句我们一起玩吧。这节课我们不劝你勇敢，只教你一个很实在的办法：把这件事拆成三小步，一步一步走过去。走完三步你会发现，胆子是这样一点一点长出来的。",
    "problem-anchor": "开始之前，先选一个你最想知道的事。是想知道心里说不敢的时候可以怎么想，还是想知道怎么把一件大事拆成小步，或者你想知道自己能为班里做点什么，再或者你想知道没被选上、没被叫到的时候该怎么办。选好了，就带着它往下看。",
    "objectives": "这节课有四个小目标。第一，能说出一件我有点不敢做的事，并知道不敢不等于做不到。第二，能把一件有点难的事拆成三小步，一步一步做完。第三，能说出两三件我自己就能为班级做的事，知道我也是班里的一分子。第四，没被选上、没被叫到的时候，能继续试，或者找一个人帮帮忙。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先说一件很要紧的事：有点不敢，不代表做不到。心里说不敢的时候，常常是因为这件事看起来太大了，一次做不完。这时候可以把它拆成三小步，先做最小的那一步。信心不是天生就有的，它像小芽一样，是做完一步、再做完一步，慢慢长出来的。每做完一步，就给自己打一个勾。",
    "lab-1": "现在请你当一次自己的小教练。下面有三件小事，都是很多同学会说不敢的事。点一件，我会帮你把它拆成三小步；你做完一步就点一下，右边的信心条就会长一点。三步都点完，看看信心条长什么样。",
    "module-2": "再来说说我们的班。班级像一棵树，树干是我们一起的地方，叶子就是每个人做的一点点事。一个人的力量看起来很小，可是很多人的一点点合起来，就是很茂盛的一棵树。你能为班里做的事，不一定要很大：把自己的桌椅摆整齐、看到地上有纸顺手捡起来、把图书角的书放回原处，这些都算。",
    "lab-2": "现在请你当一次班级小管家。下面有六件事，请你判断一下：哪些是我自己就能做的小力量，哪些是要和同学一起做的大力量。点一件事，再点它应该进的那个筐，放好以后可以看看为什么。",
    "worked-example": "我们一起来帮小禾想一想。班里要办朗读展示，小禾很想参加，可是一想到要站在前面，他心里就发紧，说了句我不敢。第一步，他先把这件事看清楚：我有点不敢，是因为要站在全班同学前面。第二步，他把这件事拆成三小步：先在家读给妈妈听，再在课间小声读给自己听，最后上台只读第一句。第三步，他从最小的一步做起，当天晚上就读给妈妈听了，读完妈妈给他鼓掌。第四步，他在纸上给第一步画了一个勾，发现原来我真的可以。四步走完，离上台已经很近了。",
    "conceptest-1": "接下来用三个说法考考你，每一个里面都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件事交给你。请你认领一个班级小岗位，再选好你的第一步，还有遇到困难时可以找的人。三样选好，我就送给你一张班级小岗位卡。",
    "posttest": "最后一轮，换三个新的小情境来考考你。这次会出现选小组长没选上、举手没被叫到、班里有同学总是不说话，看看你能不能用上今天的办法。",
    "summary": "这节课我们记住三句话。第一句，有点不敢，不代表做不到——心里说不敢的时候，先把这件事拆小。第二句，大事拆成三小步，做完一步打一个勾，信心是这样一点一点长出来的。第三句，我是班里的一分子：我能为班里做的小事有很多，一个人的一点点，合起来就是我们班的茂盛。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出一件我有点不敢做的事，再把它拆成三小步。第二层能力应用，动手做：去认领一件我能为班里做的小事，做满三天，每天打一个勾。第三层迁移挑战，选做：给自己画一张信心阶梯图，把走过的一步一步画上去，贴在书桌前。",
    "knowledge-graph": "这张图展示了这节课在心理健康知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 有点不敢，不代表做不到", "lab-1": "动手一 我的信心阶梯", "module-2": "概念二 我是班里的一分子",
    "lab-2": "动手二 我能为班级做的事", "worked-example": "例题讲解 小禾的朗读展示", "conceptest-1": "概念测试",
    "synthesis": "综合任务 认领一个班级小岗位", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：信心阶梯（一件"我有点不敢"的事 → 三小步 → 打勾长信心条） ──
LADDER = [
    {
        "id": "l1",
        "t": "上课举手发言，我有点不敢",
        "steps": [
            {"n": 1, "t": "先把想说的答案在心里小声说一遍",
             "fb": "第一步做到了。在心里先说一遍，站起来的时候就不容易忘。"},
            {"n": 2, "t": "把手举起来，举到老师看得见",
             "fb": "第二步做到了。举手这个动作，本身就是在告诉别人：我想说。"},
            {"n": 3, "t": "站起来，大声说出第一句",
             "fb": "第三步做到了。只要第一句说出口，后面就顺了。今天的勾，画得很有分量。"},
        ],
    },
    {
        "id": "l2",
        "t": "在班里读一段课文，我有点不敢",
        "steps": [
            {"n": 1, "t": "先在家里读给一个人听（妈妈、爸爸或者家里人）",
             "fb": "第一步做到了。先读给一个人听，声音就练出来了。"},
            {"n": 2, "t": "上课前小声读给自己听一遍",
             "fb": "第二步做到了。读过的句子，会变得更熟，心里也更稳。"},
            {"n": 3, "t": "上台后看着前两排同学，把第一句读完",
             "fb": "第三步做到了。只看前两排，眼睛就不用到处飘。你今天已经站在台上了。"},
        ],
    },
    {
        "id": "l3",
        "t": "走过去请同学一起玩，我有点不敢",
        "steps": [
            {"n": 1, "t": "先对他笑一笑，打个招呼",
             "fb": "第一步做到了。一个笑、一句招呼，就是开口的前一步。"},
            {"n": 2, "t": "问他一句：要不要一起玩？",
             "fb": "第二步做到了。这一句问出来，你就已经把自己介绍给他了。"},
            {"n": 3, "t": "听他说说他想玩什么，一起定一个玩法",
             "fb": "第三步做到了。愿意听别人说，朋友就会越来越多。"},
        ],
    },
]

# ── 动手二：我能为班级做的事（两个筐） ──
CLASS_JOBS = [
    {"id": "c1", "t": "把自己的桌椅摆整齐", "bin": "me",
     "why": "这一件我伸手就能做到，不用等谁，也不用叫谁。"},
    {"id": "c2", "t": "看到地上有纸，顺手捡起来", "bin": "me",
     "why": "弯一下腰就做完了，教室就干净一点。"},
    {"id": "c3", "t": "上课前把要用的书和笔准备好", "bin": "me",
     "why": "这是我自己的一份准备，做好了也帮了同桌的忙。"},
    {"id": "c4", "t": "和同学一起把黑板擦干净", "bin": "us",
     "why": "黑板高，一个人擦得慢，两个人一起就快多了。"},
    {"id": "c5", "t": "和大家一起排队，提醒同学靠右走", "bin": "us",
     "why": "排队是大家的事，一句提醒，队伍就顺了。"},
    {"id": "c6", "t": "值日的时候和同伴分好工", "bin": "us",
     "why": "先说好谁做什么，两个人都不累，活也做得更好。"},
]
BIN_NAME = {"me": "我一个人的小力量", "us": "大家一起的大力量"}

# ── 综合任务：班级小岗位认领（三栏各选一样） ──
POST_CARD = {
    "job": {
        "name": "① 我想认领的岗位",
        "items": [
            {"id": "j1", "t": "图书角小管家"},
            {"id": "j2", "t": "植物角浇水员"},
            {"id": "j3", "t": "课前带读小老师"},
            {"id": "j4", "t": "排队小提醒员"},
        ],
    },
    "first": {
        "name": "② 我的第一步（越小越好）",
        "items": [
            {"id": "f1", "t": "说出我最想为班里做的一件小事"},
            {"id": "f2", "t": "今天就做完最小的那一件"},
            {"id": "f3", "t": "请同桌给我提一个小建议"},
        ],
    },
    "help": {
        "name": "③ 遇到困难时，我会找谁",
        "items": [
            {"id": "h1", "t": "找同桌帮个忙"},
            {"id": "h2", "t": "找班长说一声"},
            {"id": "h3", "t": "请老师教教我怎么做"},
        ],
    },
}

CUSTOM_JS = r"""
/* ============================================================
   psych-e-g2-self-confidence 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 信心阶梯：选一件"我有点不敢"的事 → 三小步依次打勾 → 信心条逐格生长
   3) 我能为班级做的事：六件事分进「我一个人的小力量 / 大家一起的大力量」两个筐
   4) 班级小岗位卡：三栏各选一样，拼成一句承诺
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

  /* ---------- 2. 信心阶梯 ---------- */
  var LADDER = __LADDER_JSON__;
  var ladStage = document.getElementById('ladder-stage');
  if (ladStage) {
    var curL = null, doneL = {};
    var outL = document.getElementById('ladder-out');
    var scoreL = document.getElementById('ladder-score');

    function ladById(id) {
      for (var i = 0; i < LADDER.length; i++) { if (LADDER[i].id === id) return LADDER[i]; }
      return null;
    }
    function paintBar() {
      var done = curL && doneL[curL] ? doneL[curL] : 0;
      var pct = Math.round(done / 3 * 100);
      var bar = document.getElementById('ladder-bar');
      var num = document.getElementById('ladder-pct');
      if (bar) bar.style.width = pct + '%';
      if (num) num.textContent = '信心 ' + pct + ' %';
    }
    function renderL() {
      document.querySelectorAll('[data-ladder]').forEach(function (b) {
        var k = b.dataset.ladder;
        b.classList.toggle('selected', k === curL);
        b.classList.toggle('done', (doneL[k] || 0) >= 3);
      });
      var total = 0;
      Object.keys(doneL).forEach(function (k) { total += doneL[k]; });
      scoreL.textContent = '一共打勾 ' + total + ' / 9 步';
      paintBar();
    }
    function paintSteps() {
      var box = document.getElementById('ladder-steps');
      box.innerHTML = '';
      if (!curL) return;
      var S = ladById(curL);
      var done = doneL[curL] || 0;
      S.steps.forEach(function (st, idx) {
        var b = document.createElement('button');
        var reached = idx < done;
        b.className = 'choice' + (reached ? ' correct' : '');
        b.style.textAlign = 'left';
        b.textContent = (reached ? '✅ ' : '☐ ') + '第 ' + st.n + ' 步　' + st.t;
        b.addEventListener('click', function () {
          if (reached) return;
          var cur = doneL[curL] || 0;
          if (idx === cur) {
            doneL[curL] = cur + 1;
            outL.className = 'result';
            outL.innerHTML = '<strong>' + st.fb + '</strong>';
            if (doneL[curL] === 3) {
              outL.className = 'result';
              outL.innerHTML = '<strong>三小步都走完了，信心条长满了。</strong>回头看看：这三步还是刚才那件"不敢"的事吗？它已经变成一件做过的事了。';
            }
          } else {
            outL.className = 'result warn';
            outL.innerHTML = '<strong>先别急着跳步。</strong>大事要一步一步走：现在该做的是第 ' + (cur + 1) +
              ' 步——' + S.steps[cur].t + '。把这一步做完，再往下走，心里会稳得多。';
          }
          renderL();
          paintSteps();
        });
        box.appendChild(b);
      });
    }
    document.querySelectorAll('[data-ladder]').forEach(function (b) {
      b.addEventListener('click', function () {
        curL = b.dataset.ladder;
        var S = ladById(curL);
        if ((doneL[curL] || 0) >= 3) {
          outL.className = 'result';
          outL.innerHTML = '<strong>这件事的三小步你已经走完了。</strong>可以换一件"我有点不敢"的事，再练一次这个拆小步的办法。';
        } else {
          outL.className = 'result warn';
          outL.innerHTML = '<strong>你选的是：' + S.t + '</strong><br>我把这件事拆成了三小步，请你从第一步开始，做完一步点一下。';
        }
        renderL();
        paintSteps();
      });
    });
    renderL();
  }

  /* ---------- 3. 我能为班级做的事 ---------- */
  var JOBS = __JOBS_JSON__;
  var jobStage = document.getElementById('job-stage');
  if (jobStage) {
    var picked = null, placed = {};
    var outJ = document.getElementById('job-out');

    function renderJ() {
      document.querySelectorAll('[data-job]').forEach(function (b) {
        var k = b.dataset.job;
        b.classList.toggle('selected', k === picked);
        b.classList.toggle('done', !!placed[k]);
        b.disabled = !!placed[k];
      });
      document.getElementById('job-score').textContent = '已经放好 ' + Object.keys(placed).length + ' / ' + JOBS.length + ' 件事';
      var meBox = document.getElementById('job-me');
      var usBox = document.getElementById('job-us');
      meBox.innerHTML = ''; usBox.innerHTML = '';
      JOBS.forEach(function (j) {
        if (!placed[j.id]) return;
        var s = document.createElement('div');
        s.className = 'tag';
        s.textContent = j.t;
        (j.bin === 'me' ? meBox : usBox).appendChild(s);
      });
      if (!meBox.innerHTML) meBox.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
      if (!usBox.innerHTML) usBox.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
    }
    document.querySelectorAll('[data-job]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (placed[b.dataset.job]) return;
        picked = b.dataset.job;
        outJ.className = 'result warn';
        outJ.innerHTML = '<strong>你选的是：' + b.textContent + '</strong><br>想一想，它应该放进哪一个筐？';
        renderJ();
      });
    });
    document.querySelectorAll('[data-bin2]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!picked) {
          outJ.className = 'result warn';
          outJ.textContent = '先在上面点一件事，再选筐。';
          return;
        }
        var j = null;
        for (var i = 0; i < JOBS.length; i++) { if (JOBS[i].id === picked) j = JOBS[i]; }
        if (b.dataset.bin2 === j.bin) {
          placed[j.id] = true;
          outJ.className = 'result';
          outJ.innerHTML = '<strong>放对了，它属于「' + (j.bin === 'me' ? __BIN_ME__ : __BIN_US__) + '」。</strong>' + j.why;
          picked = null;
        } else {
          outJ.className = 'result warn';
          outJ.innerHTML = '<strong>再想一想「' + j.t + '」。</strong>' + j.why +
            '<br><span style="color:var(--muted)">常见错误：容易把「自己顺手能做好的事」和「要几个人一起做的事」搞混。想一想，这件事一个人做，够不够？</span>';
        }
        renderJ();
      });
    });
    renderJ();
  }

  /* ---------- 4. 班级小岗位卡 ---------- */
  var CARD = __CARD_JSON__;
  var cardStage = document.getElementById('card-stage');
  if (cardStage) {
    var chosen = {}, cols = ['job', 'first', 'help'];
    var outC = document.getElementById('card-out');

    function txt(col, id) {
      var arr = CARD[col].items;
      for (var i = 0; i < arr.length; i++) { if (arr[i].id === id) return arr[i].t; }
      return '';
    }
    function renderC() {
      cols.forEach(function (col) {
        document.querySelectorAll('[data-card="' + col + '"]').forEach(function (b) {
          b.classList.toggle('selected', chosen[col] === b.dataset.cardId);
        });
        var slot = document.getElementById('card-pick-' + col);
        if (slot) {
          slot.textContent = chosen[col] ? txt(col, chosen[col]) : '还没有选';
          slot.style.color = chosen[col] ? 'var(--text)' : 'var(--muted)';
        }
      });
      var n = cols.filter(function (c) { return chosen[c]; }).length;
      document.getElementById('card-score').textContent = '岗位卡完成 ' + n + ' / 3 项';
      if (n === 3) {
        outC.className = 'result';
        outC.innerHTML = '<strong>班级小岗位卡：</strong>我是班里的' + txt('job', chosen.job) +
          '，我会先' + txt('first', chosen.first) + '；遇到困难的时候，我会' + txt('help', chosen.help) + '。<br>' +
          '<span style="color:var(--muted)">把这句话念给同桌听，再说一句：请你看看我做到了没有。</span>';
      } else {
        outC.className = 'result warn';
        outC.textContent = '三栏各选一样，岗位卡就做好了。';
      }
    }
    cols.forEach(function (col) {
      document.querySelectorAll('[data-card="' + col + '"]').forEach(function (b) {
        b.addEventListener('click', function () {
          chosen[col] = b.dataset.cardId;
          renderC();
        });
      });
    });
    renderC();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__LADDER_JSON__', json.dumps(LADDER, ensure_ascii=False))
             .replace('__JOBS_JSON__', json.dumps(CLASS_JOBS, ensure_ascii=False))
             .replace('__CARD_JSON__', json.dumps(POST_CARD, ensure_ascii=False))
             .replace('__BIN_ME__', json.dumps(BIN_NAME["me"], ensure_ascii=False))
             .replace('__BIN_US__', json.dumps(BIN_NAME["us"], ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "明天要在班里读一小段课文，我有点不敢。下面哪个做法更有帮助？",
         "options": [("先在家里读给一个人听，再一步一步来", True),
                     ("直接放弃，请老师换成别的同学", False),
                     ("什么也不准备，硬着头皮上去", False)],
         "explain": "把一件大事拆成几小步，先做最小的那一步，心里就有底了。"
                    "<strong>错因提醒：</strong>常见错误是把「不敢」当成了「做不到」——不敢只是说明这件事有点大，拆小了就好办。"},
        {"q": "班里的图书角有点乱，我可以做什么？",
         "options": [("把书按大小摆回原来的位置", True),
                     ("不是我弄乱的，不用管", False),
                     ("等老师发现了让老师来收拾", False)],
         "explain": "为班级做事不一定要很大，顺手做好一件小事就算。"
                    "<strong>错因提醒：</strong>有人误认为「为班级做事是班干部的事」，其实班里的每个人都是班里的一分子。"},
        {"q": "新同学一个人坐在位子上，我会：",
         "options": [("走过去打个招呼，问他要不要一起玩", True),
                     ("远远看着，先不说话", False),
                     ("跟旁边的人说：他好像不爱说话", False)],
         "explain": "一句招呼，就是把自己的一点善意递过去。"
                    "<strong>错因提醒：</strong>不要把「他还没说话」当成「他不想交朋友」——先打个招呼，再看看他怎么办。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "有点不敢，不代表做不到", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">一年级的时候，我们已经学过友好地打招呼、和同学一起玩（And）；可是有时候，一件事明明很想做，心里却一直说「我不敢」，就这样错过了（But）；所以这节课学一件很实在的事——把「我有点不敢」的事拆成三小步，一步一步走过去（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">心里说「不敢」的时候，常常是因为<strong>这件事看起来太大、一次做不完</strong>。那就把它拆小一点。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看清楚：</strong>我有点不敢的到底是哪一件事？说清楚它，它就没那么模糊了。</div></div>
          <div class="step"><span class="n">2</span><div><strong>拆三小步：</strong>最小的一步要小到「今天就能做完」，比如先读给一个人听。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>做完打勾：</strong>做完一步画一个勾。勾越来越多，胆子就越来越大。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="信心阶梯示意图：一件不敢做的事拆成三小步，信心条逐步长满">
          <figcaption>示意图：一件「有点不敢」的事 → 拆成三小步 → 做完一步打一个勾，信心条一格一格长满（教学示意图，人物为中性简洁插画）</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🌱</span><div><strong>一句要紧的话：</strong>信心不是天生就有的，也不是别人夸出来的。<strong>信心是做完一步、再做完一步，长出来的。</strong></div></div>
{insight_box([
    {"lens": "看见它", "text": "「不敢」的时候，身体会给你信号：心跳快一点、手心有点潮、腿想往后缩。它在提醒你：这件事对你有一点难度。"},
    {"lens": "拆开它", "text": "把一件大事拆开看，会发现难的地方其实只是一两处。像上台读课文，难的不是读，是站在前面——那就先解决这一处。"},
    {"lens": "迁移它", "text": "这个办法到哪里都能用：学跳绳、学游泳、认识新朋友，都是先做最小的那一步，再做下一步。"},
])}
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>大事拆小步，一步一个勾——<strong>走过三步，胆子就长出来了。</strong></div></div>
    ''', tag="概念一"))

    lad_btns = "\n".join(
        f'            <button class="choice" data-ladder="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in LADDER
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：我的信心阶梯，一步一步打勾", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一件「我有点不敢」的事，我会把它拆成三小步。<strong>从第一步开始</strong>，做完一步点一下，右边的信心条就会长一点。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 我有点不敢的一件事</div>
          <div class="grid" id="ladder-stage">
{lad_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 把它拆成三小步（做完一步点一下）</div>
          <div class="sort-bank" id="ladder-steps">
            <span style="color:var(--muted);font-size:14px">先在上面点一件事，这里就会出现三小步。</span>
          </div>
          <div class="slider-row" style="display:block">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">③ 我的信心条</div>
            <div style="height:18px;border-radius:999px;background:var(--bg-subtle);border:1px solid var(--line-subtle);overflow:hidden">
              <div id="ladder-bar" style="height:100%;width:0;border-radius:999px;background:linear-gradient(90deg,var(--brand),var(--brand-2));transition:width .5s ease"></div>
            </div>
            <p id="ladder-pct" style="margin:6px 0 0;font-weight:700;color:var(--link)">信心 0 %</p>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">打勾进度</span><span class="v" id="ladder-score">一共打勾 0 / 9 步</span></div>
          </div>
          <p class="result warn" id="ladder-out" style="margin-top:12px">先点一件你有点不敢的事。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🌱</span><div><strong>看看信心条：</strong>它一开始是空的，做完一步就长一截。这就是信心本来的样子——不是等来的，是做出来的。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "我是班里的一分子", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">班级像<strong>一棵树</strong>：树干是我们一起待的地方，叶子就是每个人做的一点点事。一个人的一点点看着小，很多人的一点点合起来，就是很茂盛的一棵树。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>我一个人的小力量</strong></p>
            <p style="color:var(--muted)">把自己的桌椅摆整齐、看到地上有纸顺手捡起来、上课前把书和笔准备好——伸手就能做，不用等谁。</p>
          </div>
          <div class="inner-card">
            <p><strong>大家一起的大力量</strong></p>
            <p style="color:var(--muted)">和同学一起擦黑板、排队时提醒同学靠右走、值日时先分好工——几个人一起做，才做得成、做得好。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="班级树示意图：树干写着我们的班，叶子标注每个人的小力量与大家一起的大力量">
          <figcaption>示意图：班级像一棵树——每个人的一点点，合起来就是我们班的茂盛（教学示意图，中性简洁插画）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「为班级做事，得是班干部，或者得做一件大事才算」。其实顺手捡一张纸、把书放回原处、提醒同学靠右走，这些都算。<strong>做事的大小，不看事情有多大，看是不是真的做了。</strong></p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>我在班里，班里也有我——<strong>一个人的一点点，合起来就是我们班。</strong></div></div>
{insight_box([
    {"lens": "看见它", "text": "班里每天都在发生很多小事：有人把窗台的花浇了，有人把地上的纸捡了。这些事没有人指派，可它们让班级一直好好的。"},
    {"lens": "比较它", "text": "一个人擦黑板，要擦很久；两个人分开擦，很快就干净了。这就是「一起」和「一个人」不一样的地方。"},
    {"lens": "迁移它", "text": "把家也看成一棵小树：收拾自己的书包、把碗端到厨房、帮家里人拿一下东西，都是你在这个家里的一点点。"},
])}
    ''', tag="概念二"))

    job_btns = "\n".join(
        f'            <button class="choice" data-job="{j["id"]}" style="text-align:left">{j["t"]}</button>'
        for j in CLASS_JOBS
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：我能为班级做的事，分进两个筐", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一件事，再点它应该进的筐：<strong>我自己就能做的</strong>放进上筐，<strong>要和同学一起做的</strong>放进下筐。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 挑一件我能为班里做的事</div>
          <div class="grid" id="job-stage">
{job_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 它属于哪一类</div>
          <div class="grid grid-2">
            <button class="choice" data-bin2="me" style="text-align:center">我一个人的小力量</button>
            <button class="choice" data-bin2="us" style="text-align:center">大家一起的大力量</button>
          </div>
          <div class="inner-card" style="margin-top:14px">
            <p><strong>我能为班级做的事</strong></p>
            <p style="margin:6px 0 4px"><strong>我一个人的小力量</strong></p>
            <div id="job-me" style="display:flex;flex-wrap:wrap;gap:6px"><span style="color:var(--muted);font-size:14px">还没有放进来。</span></div>
            <p style="margin:10px 0 4px"><strong>大家一起的大力量</strong></p>
            <div id="job-us" style="display:flex;flex-wrap:wrap;gap:6px"><span style="color:var(--muted);font-size:14px">还没有放进来。</span></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">分筐进度</span><span class="v" id="job-score">已经放好 0 / 6 件事</span></div>
          </div>
          <p class="result warn" id="job-out" style="margin-top:12px">先在上面点一件事。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🌳</span><div><strong>拿不准的时候问自己一句：</strong>这件事，我一个人做，够不够？够，就是我一个人的小力量；不够，就是大家一起的大力量。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小禾的朗读展示", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>班里要办朗读展示，小禾很想参加，可一想到要站在全班同学前面，他心里就发紧，说了句「我不敢」。请你陪他走四步。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看清楚那件事：</strong>他不敢的不是「读课文」，是「站在全班前面」。把不敢的地方找准，就好办了。</div></div>
          <div class="step"><span class="n">2</span><div><strong>拆成三小步：</strong>先在家读给妈妈听；课间小声读给自己听一遍；上台后只读第一句。</div></div>
          <div class="step"><span class="n">3</span><div><strong>从最小的一步做起：</strong>当天晚上就读给妈妈听，读完妈妈给他鼓掌。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>画一个勾：</strong>他在纸上给第一步画了勾，发现「原来我真的可以」。离上台，已经很近了。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「等我哪天不害怕了再去做」。小禾这四步里，他上台前也还是有点紧张的——<strong>不是不紧张才去做，而是先做一小步，紧张就慢慢变小了。</strong></p>
        </div>
        <div class="inner-card">
          <p><strong>说给同桌听：</strong>你有什么「有点不敢」的事？把它拆成三小步，说给同桌听一听，请他帮你看看第一步够不够小。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "心里说「我不敢」的时候，下面哪个想法更有帮助？",
         "options": [("把它拆成三小步，先做最小的那一步", True),
                     ("我不敢，说明我做不到", False),
                     ("等别人都做完了我再试试", False)],
         "explain": "不敢只是说明这件事对你有点大，拆小了就好办。"
                    "<strong>错因提醒：</strong>常见错误是把「不敢」和「做不到」搞混——这两件事中间，还隔着「拆成三小步」这一步。"},
        {"q": "下面哪一个，是「大家一起的大力量」？",
         "options": [("值日的时候和同伴先分好工，再一起做", True),
                     ("把自己的桌椅摆整齐", False),
                     ("上课前把要用的书和笔准备好", False)],
         "explain": "需要几个人一起才做得成的事，就是大家一起的大力量。"
                    "<strong>错因提醒：</strong>容易把「自己顺手能做好的事」和「要一起做的事」混淆——问一句「我一个人做，够不够」就分清了。"},
        {"q": "我举手了，老师没有叫我，心里有点不舒服。下面哪个做法更合适？",
         "options": [("下次继续举手，也可以课后告诉老师我很想回答", True),
                     ("以后再也不举手了", False),
                     ("觉得老师不喜欢我", False)],
         "explain": "一节课要叫的人很多，没叫到不等于你不行；继续说，老师就会记得。"
                    "<strong>错因提醒：</strong>有人误认为「没被叫到就是我不够好」——把一次结果当成对自己的评价，最容易让人不敢再试。"}
    ], tag="概念测试"))

    card_blocks = []
    for col in ("job", "first", "help"):
        btns = "\n".join(
            f'              <button class="choice" data-card="{col}" data-card-id="{it["id"]}" style="text-align:left">{it["t"]}</button>'
            for it in POST_CARD[col]["items"]
        )
        card_blocks.append(f'''          <div class="inner-card">
            <p><strong>{POST_CARD[col]["name"]}</strong>　<span style="color:var(--muted);font-size:13px">已选：</span><span id="card-pick-{col}" style="color:var(--muted)">还没有选</span></p>
            <div class="grid" style="margin-top:8px">
{btns}
            </div>
          </div>''')
    card_html = "\n".join(card_blocks)
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：认领一个班级小岗位", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">三栏各选一样，就做好了你的<strong>班级小岗位卡</strong>。岗位不在大小，先挑一个你真的做得来的。</p>
        <div class="lab-panel" id="card-stage">
{card_html}
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">岗位卡进度</span><span class="v" id="card-score">岗位卡完成 0 / 3 项</span></div>
          </div>
          <p class="result warn" id="card-out" style="margin-top:12px">三栏各选一样，岗位卡就做好了。</p>
        </div>
        <div class="inner-card">
          <p><strong>再写一句给班里的话：</strong></p>
          <p style="color:var(--muted)">想一想，你做了这件事之后，班里会有什么不一样？把它写成一句话。</p>
          <textarea id="syn-answer" rows="3" placeholder="我是班里的……，我做了……之后，班里会……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换三个新情境，办法还在不在", TTS["posttest"], [
        {"q": "班里选小组长，我没有被选上，心里有点失落。下面哪个做法更合适？",
         "options": [("先做好自己手上的事，下次再参加，也可以去帮帮选上的同学", True),
                     ("以后班里的活动我再也不参加了", False),
                     ("觉得同学们都不喜欢我", False)],
         "explain": "一次没选上，只是这一次的结果；你还能为班里做很多事，大家也会看见。"
                    "<strong>错因提醒：</strong>常见错误是把「这一次没选上」当成「我这个人不行」——把一件事的结果，和对自己整个人的评价分开，就不容易泄气。"},
        {"q": "我在小组里提出了一个想法，没有人回应，我有点想放弃。下面哪个做法更合适？",
         "options": [("把想法再说一遍，说慢一点、举一个例子", True),
                     ("算了，以后我什么也不说了", False),
                     ("心里记住这件事，下次也不支持别人", False)],
         "explain": "有时候不是别人不同意，是还没听清楚。再说一遍、举个例子，想法就容易被人接住。"
                    "<strong>错因提醒：</strong>容易误认为「没人回应就是我说得不好」——先把话说清楚，再看大家的反应。"},
        {"q": "班里有一位同学总是一个人待着，很少说话。下面哪个做法更合适？",
         "options": [("走过去问他一个简单的问题，比如「你在看什么书」", True),
                     ("他不说话，那就不去管他", False),
                     ("告诉别人他就爱一个人待着", False)],
         "explain": "一个简单的问题，别人就接得住，也不会让人觉得为难。"
                    "<strong>错因提醒：</strong>不要把「他很少说话」当成「他喜欢一个人待着」——先递一句话过去，再看他怎么回应。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，讲清自信和班级这件事", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>不敢不等于做不到：</strong>心里说不敢的时候，先看清楚不敢的是哪一点。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>大事拆三小步：</strong>做完一步打一个勾，信心条一格一格长满。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>我是班里的一分子：</strong>我一个人的小力量，加上大家一起的大力量，就是我们班。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>还要记牢一件事：</strong>每个人能做到的事不一样，快一点慢一点也很正常。今天做成一小步，就已经比昨天多走了一步。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「不敢、三小步、班里」这三个词，说清楚你最近做成的一件事。</p>
          <p style="color:var(--muted)">再动一动手：<strong>画一画</strong>你的信心阶梯，在每一级台阶上写一个你已经做到的小动作。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "说出一件我有点不敢做的事，再把它拆成三小步写下来。",
            "说出两件我自己就能为班里做的小事。",
        ],
        [
            "认领一件我能为班里做的小事（比如把图书角的书摆好），做满三天，每天打一个勾。",
            "把「大事拆小步」的办法用在一件事上：学跳绳、学游泳、或者认识一位新同学。",
        ],
        [
            "画一张自己的信心阶梯图，把走过的一步一步画上去，贴在书桌前。",
            "和同桌一起，为我们班想两条让教室更舒服的小办法，写清楚为什么。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "psych-e-g2-self-confidence",
    "node_id": "psych-e-g2-self-confidence",
    "subject": "psychology",
    "subject_cn": "心理健康",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "中小学心理健康教育指导纲要（2012年修订）/ 教育部相关要求 · 小学",
    "title": "自信与集体归属感",
    "name_en": "Confidence and Belonging: Growing Step by Step",
    "grade": 2,
    "grade_cn": "二年级",
    "domain": "interpersonal",
    "domain_cn": "人际交往",
    "lesson_type": "workshop",
    "version": "1.0.0",
    "description": "面向小学二年级的自信与集体归属课：先把一件「我有点不敢」的事拆成三小步，做完一步打一个勾，让信心条一格一格长满；再找一找「我能为班级做的事」，分清我一个人的小力量和大家一起的大力量，最后认领一个班级小岗位。全课不评价、不贴标签，把「不敢」和「做不到」分开，让孩子在能做到的小事里累积自信与归属感。",
    "tags": ["自信", "集体归属感", "拆解小步", "交往品质", "二年级"],
    "standard_ref": "《中小学心理健康教育指导纲要（2012年修订）· 小学低年级》人际交往与集体意识——培养学生礼貌友好的交往品质，乐于与老师、同学交往；使学生有安全感和归属感，初步学会自我控制；树立集体意识，培养自主参与各种活动的能力。",
    "hero_question": "有一件事你很想做，可心里一直说「我不敢」，这时候可以怎么办？",
    "hero_alt": "自信与集体归属感知识结构图：有点不敢也没关系、大事拆成三小步、我是班里的一分子 三栏",
    "hero_caption": "自信与集体归属感：不敢不等于做不到 · 大事拆成三小步 · 一个人的一点点，合起来就是我们班",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "心里说「我不敢」的时候，可以怎么想？", "d": "不敢和做不到，是不是一回事", "v": "心里说我不敢的时候可以怎么想"},
        {"t": "怎么把一件大事拆成小步？", "d": "想学会自己给自己拆步骤", "v": "怎么把一件大事拆成小步"},
        {"t": "我能为班里做点什么？", "d": "我一个人的小力量有多大", "v": "我能为班里做点什么"},
        {"t": "没被选上、没被叫到，心里不舒服怎么办？", "d": "一次结果是不是就等于我不行", "v": "没被选上没被叫到心里不舒服怎么办"},
    ],
    "objectives": [
        "能说出一件「我有点不敢」的事，并知道不敢不等于做不到",
        "能把一件有点难的事拆成三小步，按顺序一步一步做完",
        "能说出两三件自己就能为班级做的事，知道我也是班里的一分子",
        "没被选上、没被叫到的时候，能继续试，或者找一个人帮帮忙",
    ],
    "objectives_plain": [
        "能说出一件「我有点不敢」的事，并知道不敢不等于做不到",
        "能把一件有点难的事拆成三小步，按顺序一步一步做完",
        "能说出两三件自己就能为班级做的事，知道我也是班里的一分子",
        "没被选上、没被叫到的时候，能继续试，或者找一个人帮帮忙",
    ],
    "standards": [
        {"content": "培养学生礼貌友好的交往品质，乐于与老师、同学交往，在谦让、友善的交往中感受友情",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学低年级 · 人际交往"},
        {"content": "使学生有安全感和归属感，初步学会自我控制；树立集体意识，培养自主参与各种活动的能力",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学低年级 · 集体意识与自我控制"},
    ],
    "prereqs": ["psych-e-g1-learning-habit"],
    "prereqs_name": "学习习惯与友好交往",
    "prereqs_meta": "psych-e-g1-learning-habit",
    "leads_to": ["psych-e-g2-emotion-basics"],
    "next_meta": "psych-e-g2-emotion-basics",
    "section_images": ["assets/psych-e-g2-self-confidence-fig1.webp", "assets/psych-e-g2-self-confidence-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "有件事很想做，心里却说不敢——这节课教你把它拆成三小步。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能自己把一件不敢的事拆成三小步。",
        "objectives": "看清四件事：不敢不等于做不到、拆成三小步、为班里做点事、没被选上也能继续试。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "不敢只是说明这件事有点大。拆成三小步，先做最小的那一步就够。",
        "lab-1": "选一件不敢的事，从第一步开始打勾，看看右边的信心条怎么长。",
        "module-2": "班级像一棵树：一个人的一点点，合起来就是我们班的茂盛。",
        "lab-2": "分不清就问自己：这件事我一个人做，够不够？够就是我一个人的小力量。",
        "worked-example": "小禾四步：看清不敢的是哪一点、拆成三小步、从最小的一步做起、画一个勾。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "三栏各选一样，做好你的班级小岗位卡，再念给同桌听一遍。",
        "posttest": "出现了没选上小组长、没人回应你的想法、同学总是一个人，看看你能不能用上今天的办法。",
        "summary": "三句话：不敢不等于做不到、大事拆三小步、我是班里的一分子。",
        "homework": "三层小任务，先做前两层，第三层可以请家里人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先帮你找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学心理健康「人际交往」在二年级的空缺，正对课标「培养学生礼貌友好的交往品质」「使学生有安全感和归属感」「树立集体意识，培养自主参与各种活动的能力」。二年级学生的自信问题很少是「我不行」，多半是「这事太大，我不敢开始」；归属感问题也很少是「我不想参与」，多半是「我不知道自己能做什么」。所以全课只做两件能落地的事——先把一件「我有点不敢」的事拆成三小步，一步一步做完（可操作的自信）；再找出「我能为班级做的事」，分清一个人的小力量和一起做的大力量（可参与的归属）。两个互动台子都能真的操作：一个是「信心阶梯」，选一件不敢的事，系统给出三小步，必须按顺序打勾，右边的信心条随之逐格长满；一个是「我能为班级做的事」，六件事分进「我一个人的小力量 / 大家一起的大力量」两个筐。综合任务把「岗位 + 第一步 + 遇到困难找谁」拼成一张班级小岗位卡，落到自主参与上。插图一律为中性简洁的教学插画，不使用真实儿童照片风格人像；全课不出现任何临床诊断词汇，不贴标签、不评判。",
    "plan_table": """| 1 | cover | 自信与集体归属感 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 有点不敢，不代表做不到 | 承·概念一（把不敢与做不到分开） |
| 6 | interactive | 动手一：我的信心阶梯，一步一步打勾 | 承·可操作的自信心（三小步 + 信心条） |
| 7 | concept | 我是班里的一分子 | 承·概念二（集体意识与参与） |
| 8 | interactive | 动手二：我能为班级做的事，分进两个筐 | 承·分类操作（一个人的 / 一起做的） |
| 9 | concept | 例题示范：小禾的朗读展示 | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：认领一个班级小岗位 | 合·迁移应用（岗位卡拼装） |
| 12 | quiz | 后测：换三个新情境，办法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，讲清自信和班级这件事 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：有点不敢也没关系 / 大事拆成三小步 / 我是班里的一分子 三栏\n- P5 信心阶梯示意图（已生成）：一件不敢做的事拆成三小步，信心条逐格长满，附中文标注\n- P7 班级树示意图（已生成）：树干是我们的班，叶子标注每个人的一点点，附中文标注\n- 三张图均为中性简洁教学插画，人物只用简单几何图形，不使用任何真实儿童照片或可识别肖像\n- 若需补充：本班合影（需学校与家长授权后才可使用）",
}
