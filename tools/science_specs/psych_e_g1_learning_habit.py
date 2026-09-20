# -*- coding: utf-8 -*-
"""小学心理健康 · 学习习惯与友好交往（G1）—— 补齐知识树「学习辅导」空缺

学科语气（心理健康）：温和、不评判、不贴标签；不出现任何临床诊断词汇。
一年级落点：全部换成具体动作（"上课前把书摆好""想说话先举手""借东西先说请"），不讲抽象心理概念。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/psych-e-g1-learning-habit-fig1.webp'
F2 = './assets/psych-e-g1-learning-habit-fig2.webp'

TTS = {
    "hero": "小朋友，我猜你有一件事很好奇：为什么有的同学上课很轻松，老师说的话都能记住？其实不是他比你聪明，而是他做了几件很小的事——上课前把书摆好，上课时眼睛看着老师，想说话先举手。这节课我们还要学另一件本事：怎么和老师、和同学好好说话。这两件事学会了，你在学校里会过得舒服很多。",
    "problem-anchor": "开始之前，先选一个你最想知道的事。是想知道上课前要准备什么，还是想知道怎样听课才能记住，或者你想知道怎么和同学借东西、怎么说谢谢，再或者你想知道和同学闹了别扭该怎么办。选好了，就带着它往下看。",
    "objectives": "这节课有四个小目标。第一，能说出上课前要准备好的两三样东西，并自己动手摆好。第二，能说出听课要做到的三件事：眼睛看老师、耳朵认真听、想说话先举手。第三，想借东西、想道谢、想道歉的时候，能说出合适的那个句子。第四，和同学闹了别扭，能说出先停下来、再说清楚、一起想办法这种处理顺序。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "好的学习习惯，其实只有几件很小的事。上课前，把这节课要用的课本和铅笔盒摆在桌角；上课的时候，眼睛看着老师，耳朵认真听；想说话的时候先举手。这三件事看起来简单，做到以后你会发现，老师讲的话更容易听进去，作业也不容易做错。",
    "lab-1": "现在请你当一次课堂小主人。下面有三个小动作，你点一个，教室里就会亮起一盏灯，还会告诉你这件事做了有什么好处。三盏灯全亮了，就说明你今天准备好了。",
    "module-2": "和同学好好相处，也有几句很好用的话。想借东西的时候，先说一句请；别人帮了你，说一句谢谢；不小心碰到了别人，说一句对不起。这些话很短，可是一说出来，别人心里就舒服多了，也更愿意和你做朋友。",
    "lab-2": "这里有几个课间会遇到的情境。你读一读，从三个做法里选一个，选完立刻会有一段话告诉你为什么；要是选得不太合适，也会告诉你还可以试试什么。",
    "worked-example": "我们一起来看小雨的一节课。第一步，上课前，小雨把语文书和铅笔盒摆到桌角，水杯放到桌洞里。第二步，上课时她眼睛看着老师，听到老师说打开第十二页，马上就找到了。第三步，她有一个问题想问，先举手，老师请她说，她才说。第四步，下课后她把借同桌的橡皮还回去，还说了一声谢谢。",
    "conceptest-1": "接下来用三个说法考考你，每一个说法里都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件事交给你。有一次，你和同学为了一件事都不高兴了，接下来该怎么做呢？这里有四步，被我打乱了。请你按照合适的顺序，一步一步点出来。",
    "posttest": "最后一轮，换几个新的小情境来考考你。这次会出现举手提问、摔倒的同学和借来的橡皮，看看你能不能用上今天学到的办法。",
    "summary": "这节课我们记住三句话。第一句，好习惯就是几件小事：上课前把书摆好，上课时眼睛看老师、耳朵认真听，想说话先举手。第二句，想借东西说请，别人帮了你说谢谢，不小心碰到了说对不起。第三句，和同学闹了别扭，先停下来，再说清楚自己的想法，然后一起想个办法。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出上课前要准备好的三样东西，再说出听课要做到的三件事。第二层能力应用，动手做：请家里人当同学，练一练借东西、道谢和道歉这三句话，把练习的感受说给家人听。第三层迁移挑战，选做：和同桌一起，把我们班同学最喜欢用的三句友好用语写在卡片上，贴到教室的友爱角。",
    "knowledge-graph": "这张图展示了这节课在心理健康知识网络里的位置。左边是学它之前要先会的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 好习惯就是几件小事", "lab-1": "动手一 课堂三步做一做",
    "module-2": "概念二 一句话的魔法", "lab-2": "动手二 课间小情境",
    "worked-example": "例题讲解 小雨的一节课", "conceptest-1": "概念测试",
    "synthesis": "综合任务 和好四步排一排", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：课堂三步（可点亮的互动模拟） ──
ACTIONS = [
    {"id": "a1", "t": "眼睛看老师",
     "fb": "眼睛看着说话的人，耳朵就更容易抓住他讲的话。老师讲到哪一页，你马上就能找到。"},
    {"id": "a2", "t": "耳朵认真听",
     "fb": "认真听，就是把老师说的那句话在心里过一遍。你会发现作业也变简单了。"},
    {"id": "a3", "t": "想说话先举手",
     "fb": "举起手，老师就知道你有话要说。等老师请你说，你的话全班都能听见。"},
]

# ── 动手二：课间小情境（错误做法也给温和的「还可以试试」） ──
SCENES = [
    {
        "id": "s1",
        "t": "我想借同桌的橡皮用一下",
        "opts": [
            {"k": "a", "t": "先问一句：能借我用一下吗？", "ok": True,
             "fb": "这样问真好。同桌一听就知道你需要帮忙，多半会笑着递给你。"},
            {"k": "b", "t": "不说话，直接从他笔袋里拿", "ok": False,
             "fb": "你只是想快一点。只是没问过就拿，同桌可能会吓一跳。还可以试试：先说一句能借我用一下吗。"},
            {"k": "c", "t": "不好意思开口，就不借了", "ok": False,
             "fb": "有点不好意思是很正常的。还可以试试：把那句话说小声一点也没关系——说出来，多半就成了。"},
        ],
    },
    {
        "id": "s2",
        "t": "课间，同桌在走廊上摔倒了",
        "opts": [
            {"k": "a", "t": "走过去问一句：你还好吗？要不要我扶你？", "ok": True,
             "fb": "这一句很暖。被问到的同学，心里会舒服很多。"},
            {"k": "b", "t": "站着看一看，不知道说什么", "ok": False,
             "fb": "一下子想不出说什么，很多小朋友都这样。还可以试试：只要问一句你还好吗，就已经很好了。"},
            {"k": "c", "t": "觉得好玩，笑一下", "ok": False,
             "fb": "你可能是被吓了一跳。只是被笑的同学会更难受。还可以试试：先问一问他疼不疼，需要什么帮助。"},
        ],
    },
    {
        "id": "s3",
        "t": "我想和同学一起玩跳房子",
        "opts": [
            {"k": "a", "t": "走过去问：我可以一起玩吗？", "ok": True,
             "fb": "问一句最省事。大多数同学都会给你让出位置。"},
            {"k": "b", "t": "直接站进去跟着跳", "ok": False,
             "fb": "你很想马上加入。只是队伍被打乱了，大家会有点乱。还可以试试：先问一句我可以一起玩吗。"},
            {"k": "c", "t": "站在旁边看着，一直不开口", "ok": False,
             "fb": "看着看着，时间就过去了。还可以试试：走上前一步，说一句我来当第二个好吗。"},
        ],
    },
    {
        "id": "s4",
        "t": "我和同桌都想先看同一本绘本",
        "opts": [
            {"k": "a", "t": "商量一下：你先看，看完给我，好吗？", "ok": True,
             "fb": "商量出来的办法，两个人心里都舒服，书也还在，谁都能看。"},
            {"k": "b", "t": "快点把书抢过来先看", "ok": False,
             "fb": "你太想看了，手比嘴快了一步。只是抢到以后，一起玩就没那么有意思了。还可以试试：说一句你先看还是我先看。"},
            {"k": "c", "t": "生气地把书合上，谁也别看", "ok": False,
             "fb": "你心里不太舒服，这很正常。只是书合上了，你自己也没看成。还可以试试：把心里的话说出来——我很想看这本书。"},
        ],
    },
]

# ── 综合任务：和好四步（打乱顺序） ──
HELLO_STEPS = [
    {"id": "h1", "t": "先停一停，不动手，也不说难听的话"},
    {"id": "h2", "t": "说说自己心里是怎么想的"},
    {"id": "h3", "t": "听听他心里是怎么想的"},
    {"id": "h4", "t": "一起想一个两个人都能接受的办法"},
]
HELLO_RIGHT = ["h1", "h2", "h3", "h4"]

CUSTOM_JS = r"""
/* ============================================================
   psych-e-g1-learning-habit 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 课堂三步：点一个动作亮一盏灯，三盏灯全亮算准备好
   3) 课间小情境：四个情境 × 三个做法 → 温和反馈（不判错、不贴标签）
   4) 和好四步：按合适的顺序排出来
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

  /* ---------- 2. 课堂三步 ---------- */
  var ACTIONS = __ACTIONS_JSON__;
  var stage1 = document.getElementById('class-stage');
  if (stage1) {
    var on = {};
    var out1 = document.getElementById('class-out');
    var score1 = document.getElementById('class-score');
    var READY = '三盏灯都亮了！你今天在课堂上准备好啦：书摆好、眼睛看老师、想说话先举手。';

    function render1() {
      var n = 0;
      ACTIONS.forEach(function (a) {
        var lit = !!on[a.id];
        if (lit) n++;
        var lamp = document.getElementById('lamp-' + a.id);
        if (lamp) {
          lamp.classList.toggle('correct', lit);
          lamp.textContent = (lit ? '● ' : '○ ') + a.t;
        }
      });
      score1.textContent = '已经做到 ' + n + ' / 3 件事';
      if (n === ACTIONS.length) {
        out1.className = 'result';
        out1.innerHTML = '<strong>' + READY + '</strong>';
      }
    }

    ACTIONS.forEach(function (a) {
      var lamp = document.getElementById('lamp-' + a.id);
      if (!lamp) return;
      lamp.addEventListener('click', function () {
        if (on[a.id]) {
          out1.className = 'result';
          out1.innerHTML = '<strong>' + a.t + '，你已经做到啦。</strong>' + a.fb;
          return;
        }
        on[a.id] = true;
        out1.className = 'result';
        out1.innerHTML = '<strong>灯亮了：' + a.t + '。</strong>' + a.fb;
        render1();
      });
    });
    var rs = document.getElementById('class-reset');
    if (rs) {
      rs.addEventListener('click', function () {
        on = {};
        out1.className = 'result warn';
        out1.textContent = '灯都关上啦，你可以再点一次试试。';
        render1();
      });
    }
    render1();
  }

  /* ---------- 3. 课间小情境 ---------- */
  var SCENES = __SCENES_JSON__;
  var stage2 = document.getElementById('scene-stage');
  if (stage2) {
    var curScene = null, doneScene = {};
    var out2 = document.getElementById('scene-out');
    var score2 = document.getElementById('scene-score');

    function sceneById(id) {
      for (var i = 0; i < SCENES.length; i++) { if (SCENES[i].id === id) return SCENES[i]; }
      return null;
    }

    function render2() {
      document.querySelectorAll('[data-scene2]').forEach(function (b) {
        var k = b.dataset.scene2;
        b.classList.toggle('selected', k === curScene);
        b.classList.toggle('done', !!doneScene[k]);
      });
      var n = Object.keys(doneScene).length;
      score2.textContent = '已经聊过 ' + n + ' / ' + SCENES.length + ' 个情境';
    }

    function paintOptions() {
      var box = document.getElementById('scene-opts');
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
            out2.className = 'result';
            out2.innerHTML = '<strong>这句话很好用。</strong>' + o.fb;
          } else {
            out2.className = 'result warn';
            out2.innerHTML = '<strong>还可以再想一想。</strong>' + o.fb;
          }
          render2();
          paintOptions();
        });
        box.appendChild(b);
      });
    }

    document.querySelectorAll('[data-scene2]').forEach(function (b) {
      b.addEventListener('click', function () {
        curScene = b.dataset.scene2;
        var S = sceneById(curScene);
        if (doneScene[curScene]) {
          out2.className = 'result';
          out2.innerHTML = '<strong>这件事已经聊过啦。</strong>你上次选的那句话很合适，记住它就好。';
        } else {
          out2.className = 'result warn';
          out2.innerHTML = '<strong>你遇到的是：' + S.t + '</strong><br>下面有三个做法，你选一个试试看。';
        }
        render2();
        paintOptions();
      });
    });
    render2();
  }

  /* ---------- 4. 和好四步 ---------- */
  var STEPS = __HELLO_JSON__;
  var RIGHT = __HELLO_RIGHT_JSON__;
  var stage3 = document.getElementById('hello-stage');
  if (stage3) {
    var placed = [];
    var out3 = document.getElementById('hello-out');
    var TIP = {
      h1: '第一步最要紧：先停下来。不动手，也不说难听的话，事情就不会变糟。',
      h2: '第二步，把自己心里的话说出来：我有点生气，因为……说出来，对方才知道。',
      h3: '第三步，也听一听他是怎么想的。很多时候，他的想法和我们不一样。',
      h4: '第四步，一起想一个两个人都能接受的办法。这才是真的把别扭解开了。'
    };
    function render3() {
      var bar = document.getElementById('hello-done');
      bar.innerHTML = placed.length
        ? placed.map(function (k, i) {
            var t = ''; for (var j = 0; j < STEPS.length; j++) { if (STEPS[j].id === k) t = STEPS[j].t; }
            return '<span class="tag">第' + (i + 1) + '步 · ' + t + '</span>';
          }).join(' ')
        : '<span style="color:var(--muted)">还没有排出第一步。</span>';
      document.querySelectorAll('[data-hello]').forEach(function (b) {
        var k = b.dataset.hello;
        b.disabled = placed.indexOf(k) !== -1;
        b.classList.toggle('done', placed.indexOf(k) !== -1);
      });
    }
    document.querySelectorAll('[data-hello]').forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.dataset.hello;
        if (placed.indexOf(k) !== -1) return;
        if (RIGHT[placed.length] === k) {
          placed.push(k);
          out3.className = 'result';
          out3.innerHTML = '<strong>第 ' + placed.length + ' 步排好了。</strong>' + TIP[k];
          if (placed.length === STEPS.length) {
            out3.className = 'result';
            out3.innerHTML = '<strong>四步全排对了！</strong>和好的顺序就是：<strong>先停下来 → 说出自己的想法 → 听听他的想法 → 一起想个办法。</strong>';
          }
        } else {
          out3.className = 'result warn';
          out3.innerHTML = '<strong>这一步放得早了一点。</strong>想一想，两个人正不高兴的时候，最应该先做什么？' +
            '<br><span style="color:var(--muted)">常见错误：一着急就想先争个明白。其实先把事情停下来，后面才谈得下去。</span>';
        }
        render3();
      });
    });
    render3();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__ACTIONS_JSON__', json.dumps(ACTIONS, ensure_ascii=False))
             .replace('__SCENES_JSON__', json.dumps(SCENES, ensure_ascii=False))
             .replace('__HELLO_JSON__', json.dumps(HELLO_STEPS, ensure_ascii=False))
             .replace('__HELLO_RIGHT_JSON__', json.dumps(HELLO_RIGHT, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "上课前，桌角上摆什么最合适？",
         "options": [("这节课要用的课本和铅笔盒", True),
                     ("自己最喜欢的小玩具", False),
                     ("一包好吃的零食", False)],
         "explain": "桌角放着上课要用的东西，一伸手就能拿到，心里也踏实。"
                    "<strong>错因提醒：</strong>常见错误是把「我喜欢的」和「上课要用的」搞混了——喜欢的东西，回家再玩就好。"},
        {"q": "我想借同桌的橡皮，怎么做比较好？",
         "options": [("先问一句：能借我用一下吗？", True),
                     ("不说话，直接拿过来用", False),
                     ("自己翻他的笔袋找一找", False)],
         "explain": "先说一句「能借我用一下吗」，又礼貌又省事。"
                    "<strong>错因提醒：</strong>不要把「反正他也会同意」和「可以先拿」搞混——问一问，是尊重他的东西。"},
        {"q": "和同学一起玩的时候，两个人都想玩同一个球，你会：",
         "options": [("商量一下：我们一个一个来，好吗？", True),
                     ("用力把球抢过来", False),
                     ("不玩了，自己回教室", False)],
         "explain": "商量一句，两个人都能玩到，还能玩得更久。"
                    "<strong>错因提醒：</strong>容易误认为「先拿到就是我的」——抢过来的东西，玩起来也没那么有意思。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "好习惯，其实就是几件小事", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们已经知道上课要坐好、听老师说话（And）；可是有时候书没带齐、笔找不到，一节课就在翻书包里过去了，老师讲的那句话也没听清（But）；所以我们要先学几件特别小的准备动作，把它们变成习惯，上课就轻松多了（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">好习惯不是大道理，它是<strong>三件很小的事</strong>。做到一件，就是做好一次。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>上课前</strong></p>
            <p style="color:var(--muted)">把课本和铅笔盒摆到桌角，水杯放进桌洞，人坐正。</p>
          </div>
          <div class="inner-card">
            <p><strong>上课时</strong></p>
            <p style="color:var(--muted)">眼睛看着老师，耳朵认真听，想说话先举手。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="课前四步小准备示意图：摆好书、削好笔、坐端正、看着老师，附中文标注">
          <figcaption>示意图：课前四步小准备——摆好书、削好笔、坐端正、看着老师（教学示意图，非实景照片）</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">✏️</span><div><strong>一句小口诀：</strong>书摆好，笔削好，人坐正，看老师——<strong>四步做完，上课不慌。</strong></div></div>
{insight_box([
    {"lens": "看见它", "text": "学习习惯不在天上，它就在桌角上：一本摆好的书、一支削好的笔、一个坐正的小身影。"},
    {"lens": "解释它", "text": "为什么眼睛看着老师，就听得更清楚？因为看和听是配合的——看着说话的人，注意力就跟着他的话走。"},
    {"lens": "迁移它", "text": "这几件小事到哪里都好用：在家写作业、在兴趣班上课，先准备好、再专心听，一样省力气。"},
])}
    ''', tag="概念一"))

    lamp_btns = "\n".join(
        f'            <button class="choice" id="lamp-{a["id"]}" data-action="{a["id"]}" style="text-align:center">○ {a["t"]}</button>'
        for a in ACTIONS
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：课堂三步，做一做就亮灯", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">点一个你打算做到的动作，教室里就会亮起一盏灯，还会告诉你这件事有什么好处。<strong>三盏灯全亮，就说明你今天准备好了。</strong></p>
        <div class="lab-panel">
          <div class="lab-stage" id="class-stage" style="height:150px;background:var(--bg-subtle)">
            <div class="lab-obj" style="top:38%;left:50%;transform:translateX(-50%);background:var(--card);border:2px solid var(--brand-2);width:150px;height:64px;border-radius:12px;color:var(--text-strong);font-weight:700;display:grid;place-items:center">我的小课桌</div>
          </div>
          <div class="grid grid-3" style="margin-top:12px">
{lamp_btns}
          </div>
          <div class="flex-row">
            <button class="choice" id="class-reset" style="text-align:center;flex:1">重新来一次</button>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">准备好了吗</span><span class="v" id="class-score">已经做到 0 / 3 件事</span></div>
          </div>
          <p class="result warn" id="class-out" style="margin-top:12px">点一点上面的动作，看看灯会不会亮。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💡</span><div><strong>想一想：</strong>这三件事里，哪一件你已经做得很好了？哪一件还想再练一练？把它记在心里，明天试一次。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "一句话的魔法：请、谢谢、对不起", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">和同学、和老师好好相处，只要几句话就够了。它们很短，可是说出来，别人心里就舒服多了。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>想借东西：</strong>先说「请」——「能借我用一下吗？」</div></div>
          <div class="step"><span class="n">2</span><div><strong>别人帮了你：</strong>说一句「谢谢」——哪怕只是帮你捡起一支笔。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>不小心碰到了别人：</strong>说「对不起」，再帮他把东西捡起来。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="三句友好用语示意图：请、谢谢、对不起，各配一个对话气泡，附中文标注">
          <figcaption>示意图：三句很好用的话——请、谢谢、对不起，各配一个对话气泡（教学示意图，人物为极简线条）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「很小的事不用说谢谢」，「不认识的人也不用打招呼」。其实越是这些小事，说出来越让人愿意和你在一起。还有同学把「借」和「给」<strong>搞混</strong>——借来的东西，用完要记得还。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>借东西说请，受了帮忙说谢谢，碰到别人说对不起——<strong>三句话，交朋友。</strong></div></div>
{insight_box([
    {"lens": "看见它", "text": "友好交往的本事，藏在几句话里：请、谢谢、对不起、我来帮你。"},
    {"lens": "比较它", "text": "同样是想看同一本绘本：抢过来，只有一个人看一会儿；商量一下，两个人都能看到最后。"},
    {"lens": "迁移它", "text": "在家里、在楼道里、在公交车上，这几句话也一样好用。别人会觉得，和你在一起很舒服。"},
])}
    ''', tag="概念二"))

    scene_btns = "\n".join(
        f'            <button class="choice" data-scene2="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in SCENES
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：课间小情境，你选哪一句？", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一个课间会遇到的情境，再从三个做法里选一个。<strong>选得好会告诉你为什么，选得不太合适也会告诉你还可以试试什么</strong>。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 课间我会遇到的事</div>
          <div class="grid" id="scene-stage">
{scene_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 我可以怎么做</div>
          <div class="grid" id="scene-opts">
            <span style="color:var(--muted);font-size:14px">先在上面点一件事，这里就会出现三个做法。</span>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">聊过几个情境</span><span class="v" id="scene-score">已经聊过 0 / 4 个情境</span></div>
          </div>
          <p class="result warn" id="scene-out" style="margin-top:12px">先点一件课间会遇到的事。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🫶</span><div><strong>说给你听：</strong>这里没有「对」和「错」的分数。有的做法只是会让事情麻烦一点，换一个试试就好。不好意思开口，是很正常的，慢慢来。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小雨的一节课", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>小雨上一年级，她想知道「怎么上课才听得清楚」。请你陪她走一遍这一节课。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>上课前：</strong>把语文书和铅笔盒摆到桌角，水杯放进桌洞。</div></div>
          <div class="step"><span class="n">2</span><div><strong>上课时：</strong>眼睛看着老师，听到「打开第十二页」，马上就能翻到。</div></div>
          <div class="step"><span class="n">3</span><div><strong>有问题想问：</strong>先举手，等老师请她说，她才说。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>下课后：</strong>把借同桌的橡皮还回去，还说了一声谢谢。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「举手太慢，直接说更快」。可你直接说的时候，老师正在讲的那句话就被打断了，全班都要重听一遍。小雨的办法是：<strong>先举手，等老师看到你，再说</strong>——这样既说了自己的话，也没耽误别人。</p>
        </div>
        <div class="inner-card">
          <p><strong>说给同桌听：</strong>小雨这四步里，你哪一步已经很熟练了？哪一步还想明天再试一次？</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "下面哪句话说得对？",
         "options": [("上课眼睛看着老师，听到的就更多", True),
                     ("偷偷玩橡皮，不出声就没关系", False),
                     ("想说话不用举手，直接说更快", False)],
         "explain": "眼睛看着老师，注意力就跟着老师的话走。"
                    "<strong>错因提醒：</strong>常见错误是误认为「不出声就没影响」——低头玩东西的那一会儿，老师讲的那句话就漏过去了。"},
        {"q": "同学帮你把掉在地上的铅笔捡了起来，你可以说：",
         "options": [("谢谢你", True),
                     ("什么也不用说", False),
                     ("下次你也帮我捡", False)],
         "explain": "一句谢谢，让人愿意和你继续做朋友。"
                    "<strong>错因提醒：</strong>不要误认为「小事不用说谢谢」——说出来，对方才知道你收到了这份好意。"},
        {"q": "你不小心碰掉了同桌的铅笔盒，下面哪个做法更合适？",
         "options": [("马上说对不起，再帮他把笔捡起来", True),
                     ("装作没看见，赶快走开", False),
                     ("先看看老师有没有发现", False)],
         "explain": "说声对不起，再一起捡起来，事情很快就过去了。"
                    "<strong>错因提醒：</strong>容易把「没被看见」当成「没发生」——主动说对不起，是很有担当的做法，同桌也会更信任你。"}
    ], tag="概念测试"))

    step_btns = "\n".join(
        f'            <button class="sort-item" data-hello="{h["id"]}">{h["t"]}</button>' for h in HELLO_STEPS
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：和好四步，排一排", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">两个人都不高兴的时候，接下来怎么做才对呢？下面四步被打乱了，请你<strong>按合适的顺序</strong>一步一步点出来。</p>
        <div class="lab-panel">
          <div class="sort-bank" id="hello-stage">
{step_btns}
          </div>
          <div class="inner-card" style="margin-top:14px">
            <p><strong>我排出来的顺序</strong></p>
            <p id="hello-done" style="color:var(--muted)">还没有排出第一步。</p>
          </div>
          <p class="result warn" id="hello-out" style="margin-top:12px">请点出你认为的第一步。</p>
        </div>
        <div class="inner-card">
          <p><strong>排完之后，想一想：</strong></p>
          <p style="color:var(--muted)">这四步里，哪一步最难做到？如果第一次没做好，还可以怎么办？</p>
          <p style="color:var(--muted)">再把它<strong>画出来</strong>：四个小方框，用箭头连起来，就是你的「和好小图」。</p>
          <textarea id="syn-answer" rows="3" placeholder="最难做到的是第……步，因为……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，办法还在不在", TTS["posttest"], [
        {"q": "上课的时候，你有一个问题很想问，你会：",
         "options": [("先举手，等老师请我再说", True),
                     ("直接大声问出来", False),
                     ("先憋着，下课后就忘了", False)],
         "explain": "举手问，老师听得见，别的同学也还在听课。"
                    "<strong>错因提醒：</strong>不要让「怕打扰老师」变成「什么都不问」——举手，就是把打扰换成了合适的方式。"},
        {"q": "课间，同桌不小心摔倒了，你会：",
         "options": [("走过去问一句：你还好吗？要不要我扶你？", True),
                     ("站着看一看，不知道说什么", False),
                     ("觉得好玩，笑一下", False)],
         "explain": "一句问候，就能让同学心里暖一下。"
                    "<strong>错因提醒：</strong>不要把「不知道该说什么」当成「什么都不做」——只要问一句你还好吗，就已经很好了。"},
        {"q": "同学把橡皮借给了你，你用完了，你会：",
         "options": [("还给他，并说一声谢谢", True),
                     ("放到自己笔袋里，下次再说", False),
                     ("放在桌上，不管了", False)],
         "explain": "用完就还，再说声谢谢，下次他还愿意借给你。"
                    "<strong>错因提醒：</strong>常见错误是把「借」和「给」搞混——借来的东西，用完要想着还，这是最简单的守信。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，学会学习和相处", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>上课前：</strong>书摆好、笔削好、人坐正、看老师——几件小事，就是好习惯。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>和同学：</strong>借东西说请，受了帮忙说谢谢，碰到别人说对不起。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>闹别扭了：</strong>先停下来，说出自己的想法，听听他的想法，再一起想个办法。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>还要记牢一件事：</strong>刚开始做不到、不好意思开口，都是很正常的。今天做到一件，明天再做到一件，慢慢地它们就变成你的习惯了。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「摆好、举手、谢谢」这三个词，说清楚你今天在学校做得好的一件事。</p>
          <p style="color:var(--muted)">再动一动手：<strong>画一画</strong>你的桌角——哪边放课本，哪边放铅笔盒，用三个小方框标出来。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "说出上课前要准备好的三样东西。",
            "说出听课要做到的三件事，再说出一句借东西时会用的礼貌用语。",
        ],
        [
            "请家里人当同学，练一练借东西、道谢和道歉这三句话，把练习的感受说给家人听。",
            "今天放学后，自己动手把桌角整理一次，把课本、铅笔盒和橡皮放到固定的位置。",
        ],
        [
            "和同桌一起，把我们班同学最喜欢用的三句友好用语写在卡片上，贴到教室的友爱角。",
            "想一想：家里有没有需要商量的事？用「先停下来、说出想法、听听对方、一起想办法」试一试，把结果写在纸上。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "psych-e-g1-learning-habit",
    "node_id": "psych-e-g1-learning-habit",
    "subject": "psychology",
    "subject_cn": "心理健康",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "中小学心理健康教育指导纲要（2012年修订）/ 教育部相关要求 · 小学",
    "title": "学习习惯与友好交往",
    "name_en": "Learning Habits and Getting Along Well with Others",
    "grade": 1,
    "grade_cn": "一年级",
    "domain": "learning-support",
    "domain_cn": "学习辅导",
    "lesson_type": "workshop",
    "version": "1.0.0",
    "description": "面向小学一年级的学习习惯与交往启蒙课：先练「上课前把书摆好、笔削好，上课时眼睛看老师、想说话先举手」这几件具体小事，再学「借东西说请、受了帮忙说谢谢、碰到别人说对不起」这三句友好用语，最后用「先停下来、说出想法、听听对方、一起想办法」四步处理同伴间的小别扭。",
    "tags": ["学习习惯", "友好交往", "礼貌用语", "同伴相处", "一年级"],
    "standard_ref": "《中小学心理健康教育指导纲要（2012年修订）· 小学低年级》学习辅导与人际交往——初步感受学习知识的乐趣，重点是学习习惯的培养与训练；培养学生礼貌友好的交往品质，乐于与老师、同学交往，在谦让、友善的交往中感受友情。",
    "hero_question": "为什么有的同学上课很轻松，老师讲的话都能记住？",
    "hero_alt": "学习习惯与友好交往知识结构图：上课前摆好书、上课时看老师举手、和同学好好说话 三栏",
    "hero_caption": "学习习惯与友好交往：书摆好、看老师、先举手 · 借东西说请、受帮忙说谢谢 · 先停下来再一起想办法",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "上课前要准备什么？", "d": "桌角上应该摆哪几样东西", "v": "上课前要准备什么"},
        {"t": "怎样听课才能记得住？", "d": "眼睛、耳朵和手各要做一件什么事", "v": "怎样听课才能记得住"},
        {"t": "想借东西、想道谢，该说什么？", "d": "有没有几句很好用的话", "v": "想借东西想道谢该说什么"},
        {"t": "和同学闹别扭了怎么办？", "d": "不高兴的时候先说哪一句", "v": "和同学闹别扭了怎么办"},
    ],
    "objectives": [
        "能说出上课前要准备好的两三样东西，并自己动手把桌角摆好",
        "能说出听课要做到的三件事：眼睛看老师、耳朵认真听、想说话先举手",
        "想借东西、想道谢、想道歉的时候，能说出合适的那一句话",
        "和同学闹别扭时，能说出先停下来、说出想法、听听对方、一起想办法的处理顺序",
    ],
    "objectives_plain": [
        "能说出上课前要准备好的两三样东西，并自己动手把桌角摆好",
        "能说出听课要做到的三件事：眼睛看老师、耳朵认真听、想说话先举手",
        "想借东西、想道谢、想道歉的时候，能说出合适的那一句话",
        "和同学闹别扭时，能说出先停下来、说出想法、听听对方、一起想办法的处理顺序",
    ],
    "standards": [
        {"content": "初步感受学习知识的乐趣，重点是学习习惯的培养与训练",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学低年级 · 学习辅导"},
        {"content": "培养学生礼貌友好的交往品质，乐于与老师、同学交往，在谦让、友善的交往中感受友情",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学低年级 · 人际交往"},
    ],
    "prereqs": ["psych-e-g1-school-adapt"],
    "prereqs_name": "入学适应与规则意识",
    "prereqs_meta": "psych-e-g1-school-adapt",
    "leads_to": ["psych-e-g2-self-confidence"],
    "next_meta": "psych-e-g2-self-confidence",
    "section_images": ["assets/psych-e-g1-learning-habit-fig1.webp", "assets/psych-e-g1-learning-habit-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "上课轻松的同学，不是更聪明，而是做了几件很小的事。带着这个好奇开始。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能说出三件上课要做的小事和三句友好用语。",
        "objectives": "看清四件事：课前准备、听课三件事、三句友好用语、和好四步。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "书摆好、笔削好、人坐正、看老师——四步做完，上课不慌。",
        "lab-1": "点一个动作亮一盏灯，三盏灯全亮就说明你今天准备好了。",
        "module-2": "借东西说请，受了帮忙说谢谢，碰到别人说对不起。三句话，交朋友。",
        "lab-2": "四个课间情境，每个有三个做法。选得不太合适也不会说你错，只会告诉你还可以试试什么。",
        "worked-example": "小雨的四步：课前摆好书、上课看老师、想问先举手、下课还橡皮说谢谢。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "两个人都不高兴的时候，第一步最要紧：先停下来。按合适的顺序点出来。",
        "posttest": "出现了举手提问、摔倒的同学和借来的橡皮，看看你能不能用上今天的办法。",
        "summary": "三句话：课前准备、三句友好用语、和好四步。",
        "homework": "三层小任务，先做前两层，第三层可以请同桌或家人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学心理健康「学习辅导」（兼及人际交往）的一课，正对一年级学习习惯的培养与友好交往品质的养成。一年级学生的困难不是听不懂道理，而是知道该做的具体动作是什么——所以全课只练两类可操作的事：学习侧的「书摆好、笔削好、人坐正、看老师、想说话先举手」，交往侧的「借东西说请、受帮忙说谢谢、碰到别人说对不起」。三个互动台子都能真的动手：①「课堂三步」模拟器，点一个动作亮一盏灯，三盏灯全亮算准备好；②四个课间情境卡片，选做法后给即时反馈，反馈一律写成「还可以试试……」而不判错、不贴标签、不讲抽象心理概念；③综合任务把「和好四步」打乱，让学生自己排出先停下来 → 说出想法 → 听听对方 → 一起想办法。全课只用「摆好、举手、谢谢」三个词收口，插图一律为中性简洁的教学示意图（极简线条人物，不使用真实儿童照片）。",
    "plan_table": """| 1 | cover | 学习习惯与友好交往 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 好习惯，其实就是几件小事 | 承·概念一（学习习惯） |
| 6 | interactive | 动手一：课堂三步，做一做就亮灯 | 承·动作模拟（点亮三盏灯） |
| 7 | concept | 一句话的魔法：请、谢谢、对不起 | 承·概念二（友好交往用语） |
| 8 | interactive | 动手二：课间小情境，你选哪一句？ | 承·情境判断（温和反馈，不判错） |
| 9 | concept | 例题示范：小雨的一节课 | 转·重难点突破（分步示范 + 易错点） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：和好四步，排一排 | 合·迁移应用（排序模拟） |
| 12 | quiz | 后测：换几个新情境，办法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，学会学习和相处 | 合·小结与复述 |
| 14 | homework | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：课前摆好书 / 上课看老师举手 / 和同学好好说话 三栏\n- P5 课前四步小准备示意图（已生成）：摆好书、削好笔、坐端正、看着老师，附中文标注\n- P7 三句友好用语示意图（已生成）：请、谢谢、对不起各配一个对话气泡，附中文标注\n- 三张图均为教学示意图，人物仅用极简线条，不使用任何真实儿童照片或可识别肖像\n- 若需补充：本班课桌摆放的实拍示位图（需学校授权后使用）",
}
