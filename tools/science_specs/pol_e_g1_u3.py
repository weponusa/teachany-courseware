# -*- coding: utf-8 -*-
"""小学道德与法治 · 养成良好习惯（G1）—— 补齐知识树「生命安全与健康」空缺

学科语气（道德与法治）：情境案例驱动，情感共鸣 + 价值判断；真实校园/家庭场景，
结论落在「应该怎么做、为什么」，不做道德说教，不背法条。
一年级落点：全部换成能看见、能照做的具体动作（晚上八点半上床、饭前用肥皂洗手、
青菜先尝一小口、过马路先看左右再走），不说「要养成良好习惯」这种抽象话。
三个互动台子都能真的操作：①「这样做会怎样」六张情境卡，选做法后展开后果与对方感受，
反馈写成「这样可能会……，还可以试试……」；②「要坚持的／要改一改的」两筐分类；
③「安全过马路小演练」——自己选灯、选怎么做，看这一次能不能安全通过。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g1-u3"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "小朋友，你有没有发现，有的同学每天早上精神特别好，上课听得最清楚；有的同学却总是打瞌睡、肚子疼。差别常常不在聪不聪明，而在一些很小的事情上：晚上几点睡，吃饭前有没有洗手，出门会不会看红绿灯。今天这节课，我们就一起来学一学这些小事该怎么做，为什么这样做身体更舒服、也更安全。",
    "problem-anchor": "开始之前，先选一个你最想弄清楚的问题。是想知道晚上该几点睡、早上怎么才能起得来，还是想知道吃饭前要做哪几件事；是想知道哪些零食和饮料要少碰，还是想知道怎么玩才安全、过马路要注意什么。选好了，就带着它往下看。",
    "objectives": "这节课有四个小目标。第一，能说出按时睡觉、按时起床的时间，知道睡够了第二天才有精神。第二，能说出吃饭前要做的几件事，做到饭前洗手、不挑食、慢慢吃。第三，能说出哪些东西要少吃或不吃，渴了先喝白开水。第四，能说出玩耍和过马路时要注意什么，知道红灯停、绿灯行，过马路先看左右。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先说第一件小事：作息有规律。作息，就是你每天几点睡、几点起，天天差不多。一年级的小朋友，晚上八点半到九点上床最合适，睡够十个小时左右，第二天早上自己就能醒。睡前别再看小视频、别再玩平板，把手机放到客厅，让眼睛和脑子都歇一歇。你试试看，按时睡上一个星期，早上起床是不是容易多了。",
    "lab-1": "现在我们来看六件真实的小事。每一件都有三个做法，你选一个你觉得合适的，选完立刻会有一段话，告诉你这样做以后身体会怎么样、身边的人会怎么样；要是选得不太合适，也会告诉你还可以试试什么。",
    "module-2": "第二件小事是吃饭有讲究。吃饭前先做三件事：把玩具放下、用肥皂把手心和手背都搓一搓、把水甩干净再擦干。坐下以后慢慢吃，一口饭嚼十来下，不边吃边玩。青菜、鸡蛋、米饭都要吃一点，不爱吃的菜先尝一小口，一次不行就下次再试。渴了喝白开水，冰饮料、甜饮料少喝，辣条、油炸的小零食少吃。",
    "lab-2": "接下来我们来做一次分类。下面有八条做法，有的对身体好，要一直坚持下去；有的会让自己不舒服、也有点危险，要改一改。请你先点一条，再点它应该进的筐，看看放对没有。",
    "worked-example": "我们一起来看看小安的一天。第一步，晚上八点半，小安自己关掉动画片，去刷牙洗脸，九点前躺下睡着了。第二步，早上六点半闹钟响，他坐起来穿好衣服，吃了热乎乎的早饭才出门。第三步，午饭前他到水池边，用肥皂把手心、手背、指缝都搓干净，再坐到饭桌前。第四步，下午放学他和同学在小区里玩，先跟家长说了去哪里，太阳落山前就回家了；过马路的时候，他站在斑马线边上，看到绿灯亮了，先看左边、再看右边，才走过去。",
    "conceptest-1": "接下来用三个说法考考你，每个说法里都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件事交给你。现在我们站到马路边上，来一次过马路的小演练。你先选现在是什么灯，再选你打算怎么做，然后点过马路，看看这一次能不能安全通过。试几种不同的选法，你会发现，能不能安全过去，就取决于这两件事选得对不对。",
    "posttest": "最后一轮，换几个新的小情境来考考你。这次会出现睡前想玩平板、早上起不来、路上想买饮料，还有一次下雨天过马路，看看你能不能用上今天学到的方法。",
    "summary": "这节课我们记住三句话。第一句，作息有规律：晚上八点半到九点上床，睡够十个小时，睡前把手机放到客厅，早上按时起。第二句，吃饭有讲究：饭前用肥皂洗手，慢慢吃、不挑食，青菜先尝一小口，渴了喝白开水。第三句，安全记心上：玩耍先告诉家里人一声、按时回家，红灯停、绿灯行，过马路站在斑马线上先看左右再走。这三句话都不难，做一天容易，做一个月就变成你自己的好习惯了。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出你今天几点睡、几点起，再说出吃饭前要做到的三件事。第二层能力应用，动手做：和家里人一起做一张我的一天小表格，把起床、上学、吃饭、睡觉的时间填进去，坚持记三天。第三层迁移挑战，选做：把安全过马路的做法讲给家里人或者邻居家的小朋友听，再和他一起到路边看一次红绿灯，说说什么时候才能走。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 作息有规律", "lab-1": "动手一 这样做会怎样", "module-2": "概念二 吃饭有讲究",
    "lab-2": "动手二 要坚持的·要改一改的", "worked-example": "例题讲解 小安的一天", "conceptest-1": "概念测试",
    "synthesis": "综合任务 安全过马路小演练", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：六件小事 × 三个做法（反馈展开身体的感受与后果） ──
SCENES = [
    {
        "id": "s1",
        "t": "晚上八点半，动画片还有一点没看完，明天要早起上学",
        "opts": [
            {"k": "a", "t": "把电视关掉，去刷牙洗脸，准备上床", "ok": True,
             "fb": "这样做，你能在九点前躺下，睡够十个小时。第二天早上眼睛一亮就能起来，上课也听得清楚。"},
            {"k": "b", "t": "一直看到十一点，困得眼睛都睁不开才去睡", "ok": False,
             "fb": "这样可能会让你只睡七八个小时，第二天上课打瞌睡，老师讲什么也听不进去。还可以试试：先把这一集看完，就自己把电视关掉，明天再看下一集。"},
            {"k": "c", "t": "假装去睡觉，偷偷把平板藏进被窝里继续看", "ok": False,
             "fb": "这样可能会让眼睛又酸又干，还睡不踏实；被发现以后，家里人也就不放心把平板给你了。还可以试试：把平板放到客厅充电，睡前听一段喜欢的故事。"},
        ],
    },
    {
        "id": "s2",
        "t": "早上闹钟响了，我还想再睡一会儿",
        "opts": [
            {"k": "a", "t": "揉揉眼睛坐起来，自己穿好衣服", "ok": True,
             "fb": "这样做，你能慢慢悠悠吃完早饭，出门也不慌。自己起床，是长大一点的标志。"},
            {"k": "b", "t": "把闹钟按掉，一直睡到家里人喊第三遍", "ok": False,
             "fb": "这样可能会让早饭来不及吃，匆匆忙忙出门，上午饿得肚子咕咕叫。还可以试试：把闹钟放到要下床才够得着的地方，响了自己去关。"},
            {"k": "c", "t": "起来了，但是磨磨蹭蹭，穿一只袜子玩一会儿", "ok": False,
             "fb": "这样可能会让家里人一直催你，大家的心情都不太好，还容易迟到。还可以试试：把衣服按穿的顺序摆好，一件一件穿上。"},
        ],
    },
    {
        "id": "s3",
        "t": "家里人喊我吃饭了，我刚从外面玩回来",
        "opts": [
            {"k": "a", "t": "先去水池边用肥皂洗手，再到饭桌前坐下", "ok": True,
             "fb": "这样做，手上的灰尘和细菌就被洗掉了，吃下去的东西更干净，肚子不容易疼。洗手只要半分钟。"},
            {"k": "b", "t": "拿起筷子就吃，手还脏着", "ok": False,
             "fb": "这样可能会把手上看不见的细菌一起吃进肚子里，容易肚子疼、拉肚子。还可以试试：进屋先放下手里的东西，到水池边洗一洗再坐下。"},
            {"k": "c", "t": "先玩一会儿玩具，饭一直放着不吃", "ok": False,
             "fb": "这样可能会让饭菜变凉，吃了肚子不舒服，家里人也要一直等着你。还可以试试：把玩具放回原处，先吃完饭再接着玩。"},
        ],
    },
    {
        "id": "s4",
        "t": "桌上有一盘青菜，我不太爱吃",
        "opts": [
            {"k": "a", "t": "先尝一小口，能接受就再吃一点", "ok": True,
             "fb": "这样做，你会慢慢习惯这种味道。青菜里的营养能帮身体长得结实，拉臭臭也更顺畅。"},
            {"k": "b", "t": "把青菜全部挑出来放在桌子上", "ok": False,
             "fb": "这样可能会让你只吃到米饭和肉，时间长了容易缺营养、长不高。还可以试试：这一顿只挑一半出来，下次再少挑一点。"},
            {"k": "c", "t": "把青菜推到旁边，一口也不动", "ok": False,
             "fb": "这样可能会让你越来越不爱吃青菜，身体也跟着少了必要的营养。还可以试试：让家里把青菜切得小一点、和喜欢的菜一起炒。"},
        ],
    },
    {
        "id": "s5",
        "t": "放学回家，我把书包一扔就想跑到楼下玩",
        "opts": [
            {"k": "a", "t": "先跟家里人说一声去哪里、和谁玩，约定回来的时间", "ok": True,
             "fb": "这样做，家里人知道你在哪里，心里踏实；你玩起来也不用总担心被找。玩完按时回家，下次家里人会放心让你出去玩。"},
            {"k": "b", "t": "一声不响就跑了，家里人到处找你", "ok": False,
             "fb": "这样可能会让家里人急得团团转，找不到你的时候还会担心出危险。还可以试试：出门前大声说一句我去楼下玩，六点就回来。"},
            {"k": "c", "t": "跑到马路旁边追来追去，觉得很好玩", "ok": False,
             "fb": "这样可能会让路上的车来不及躲，非常危险。还可以试试：到小区的空地或者操场上去玩，那里没有车。"},
        ],
    },
    {
        "id": "s6",
        "t": "我想喝水，桌上放着刚烧开的热水壶",
        "opts": [
            {"k": "a", "t": "请家里人帮忙倒进杯子里，放凉一点再喝", "ok": True,
             "fb": "这样做最安全，也不会烫到手。等水凉一点再喝，对身体也更好。"},
            {"k": "b", "t": "自己踮着脚去端滚烫的水壶", "ok": False,
             "fb": "这样可能会让水洒出来，烫到手臂和肚子，痛好几天。还可以试试：喊一声请帮我倒杯水，等大人来了再喝。"},
            {"k": "c", "t": "嘴巴直接对着热水壶喝一口", "ok": False,
             "fb": "这样可能会烫到嘴巴和喉咙，非常难受。还可以试试：拿自己的杯子，请大人帮忙倒。"},
        ],
    },
]

# ── 动手二：八条做法分进「要坚持的」／「要改一改的」两个筐 ──
SORT_ITEMS = [
    {"id": "h1", "t": "晚上八点半上床，早上六点半自己起床", "bin": "keep",
     "why": "按时睡、按时起，一天到晚都有精神，长身体也长得好。这条要坚持。"},
    {"id": "h2", "t": "睡前把手机和平板放到客厅充电", "bin": "keep",
     "why": "眼睛和脑子都要歇一歇，睡着得才快。这条要坚持。"},
    {"id": "h3", "t": "饭前用肥皂把手心、手背都搓一搓", "bin": "keep",
     "why": "洗手能把看不见的细菌冲走，肚子不容易疼。这条要坚持。"},
    {"id": "h4", "t": "吃饭慢慢嚼，一口饭嚼十来下", "bin": "keep",
     "why": "慢慢吃，肚子里更好受，也不容易噎着。这条要坚持。"},
    {"id": "h5", "t": "晚上不睡，早上起不来，上学总迟到", "bin": "change",
     "why": "睡不够，白天上课容易打瞌睡，早饭也来不及吃。这一条要改一改。"},
    {"id": "h6", "t": "只吃零食和肉，青菜一口都不动", "bin": "change",
     "why": "身体少了必要的营养，容易长不高、拉臭臭也费劲。这一条要改一改。"},
    {"id": "h7", "t": "一整天不喝白开水，渴了就喝冰饮料", "bin": "change",
     "why": "甜饮料喝多了牙齿不好，冰的喝多了肚子也不舒服。这一条要改一改。"},
    {"id": "h8", "t": "放学后在马路边上追来追去", "bin": "change",
     "why": "路上的车来不及躲，非常危险。这一条要改一改。"},
]
SORT_BIN = {"keep": "要坚持的好习惯", "change": "要改一改的地方"}

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g1-u3 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 这样做会怎样：六件小事 × 三个做法 → 展开后果
   3) 要坚持的 · 要改一改的：八条做法分进两个筐
   4) 安全过马路小演练：选灯 × 选怎么做 → 能不能安全通过
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

  /* ---------- 2. 这样做会怎样 ---------- */
  var SCENES = __SCENES_JSON__;
  var stage1 = document.getElementById('habit-stage');
  if (stage1) {
    var curScene = null, doneScene = {};
    var out1 = document.getElementById('habit-out');

    function sceneById(id) {
      for (var i = 0; i < SCENES.length; i++) { if (SCENES[i].id === id) return SCENES[i]; }
      return null;
    }
    function render1() {
      document.querySelectorAll('[data-scene]').forEach(function (b) {
        var k = b.dataset.scene;
        b.classList.toggle('selected', k === curScene);
        b.classList.toggle('correct', !!doneScene[k]);
      });
      var n = Object.keys(doneScene).length;
      document.getElementById('habit-score').textContent = '已经聊过 ' + n + ' / ' + SCENES.length + ' 件小事';
    }
    function paintOptions() {
      var box = document.getElementById('habit-opts');
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
            out1.innerHTML = '<strong>这样做会怎样——</strong>' + o.fb;
          } else {
            out1.className = 'result warn';
            out1.innerHTML = '<strong>这样可能会……</strong>' + o.fb;
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
          out1.innerHTML = '<strong>这件小事已经聊过啦。</strong>你上次选的做法对身体很好，记住它就好。';
        } else {
          out1.className = 'result warn';
          out1.innerHTML = '<strong>你现在遇到的是：' + S.t + '</strong><br>下面有三个做法，你选一个试试看，再看看这样做以后会怎样。';
        }
        render1();
        paintOptions();
      });
    });
    render1();
  }

  /* ---------- 3. 要坚持的 · 要改一改的 ---------- */
  var ITEMS = __SORT_JSON__;
  var BINN = __SORTBIN_JSON__;
  var stage2 = document.getElementById('bin-stage');
  if (stage2) {
    var pickItem = null, placed = {};
    var out2 = document.getElementById('bin-out');

    function render2() {
      document.querySelectorAll('[data-item]').forEach(function (b) {
        var k = b.dataset.item;
        b.classList.toggle('selected', k === pickItem);
        b.classList.toggle('done', !!placed[k]);
        b.disabled = !!placed[k];
      });
      var n = Object.keys(placed).length;
      document.getElementById('bin-score').textContent = '已经放好 ' + n + ' / ' + ITEMS.length + ' 条';
      var kBox = document.getElementById('bin-keep');
      var cBox = document.getElementById('bin-change');
      kBox.innerHTML = ''; cBox.innerHTML = '';
      ITEMS.forEach(function (it) {
        if (!placed[it.id]) return;
        var s = document.createElement('div');
        s.className = 'tag';
        s.textContent = it.t;
        (it.bin === 'keep' ? kBox : cBox).appendChild(s);
      });
      if (!kBox.innerHTML) kBox.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
      if (!cBox.innerHTML) cBox.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
    }
    document.querySelectorAll('[data-item]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (placed[b.dataset.item]) return;
        pickItem = b.dataset.item;
        out2.className = 'result warn';
        out2.innerHTML = '<strong>你选的是：' + b.textContent + '</strong><br>想一想，这一条对身体好、要一直做下去，还是会让自己不舒服、要改一改？';
        render2();
      });
    });
    document.querySelectorAll('[data-bin]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pickItem) {
          out2.className = 'result warn';
          out2.textContent = '先在上面点一条做法，再选筐。';
          return;
        }
        var it = null;
        for (var i = 0; i < ITEMS.length; i++) { if (ITEMS[i].id === pickItem) it = ITEMS[i]; }
        if (b.dataset.bin === it.bin) {
          placed[it.id] = true;
          out2.className = 'result';
          out2.innerHTML = '<strong>放对了，它属于「' + BINN[it.bin] + '」。</strong>' + it.why;
          pickItem = null;
          if (Object.keys(placed).length === ITEMS.length) {
            out2.className = 'result';
            out2.innerHTML = '<strong>八条全放对了！</strong>记一句口诀：<strong>按时睡、饭前洗手、慢慢吃、先喝白开水；不熬夜、不挑食、少喝冰饮、不在马路边玩——好习惯是练出来的。</strong>';
          }
        } else {
          out2.className = 'result warn';
          out2.innerHTML = '<strong>再想一想这一条。</strong>' + it.why +
            '<br><span style="color:var(--muted)">常见错误：容易把「对身体好的做法」和「让自己不舒服的做法」搞混——好做法要坚持，不好的做法要改一改。再试一次。</span>';
        }
        render2();
      });
    });
    render2();
  }

  /* ---------- 4. 安全过马路小演练 ---------- */
  var stage3 = document.getElementById('road-stage');
  if (stage3) {
    var light = 'green', act = 'check', safeCount = 0, tryCount = 0;
    var out3 = document.getElementById('road-out');
    var ACTS = {
      check:  { t: '站在斑马线边上，先看左边、再看右边，慢慢走过去', good: true },
      phone:  { t: '一边低头看手机一边往前走', good: false },
      run:    { t: '看都不看，从两辆车中间跑过去', good: false },
      wait:   { t: '红灯的时候站在路边等，绿灯亮了才走', good: true, needRed: true }
    };

    function render3() {
      document.querySelectorAll('[data-light]').forEach(function (b) { b.classList.toggle('selected', b.dataset.light === light); });
      document.querySelectorAll('[data-act]').forEach(function (b) { b.classList.toggle('selected', b.dataset.act === act); });
      document.getElementById('road-try').textContent = '一共试了 ' + tryCount + ' 次';
      document.getElementById('road-ok').textContent = '安全通过 ' + safeCount + ' 次';
    }
    document.querySelectorAll('[data-light]').forEach(function (b) {
      b.addEventListener('click', function () { light = b.dataset.light; render3(); });
    });
    document.querySelectorAll('[data-act]').forEach(function (b) {
      b.addEventListener('click', function () { act = b.dataset.act; render3(); });
    });
    document.getElementById('road-go').addEventListener('click', function () {
      tryCount += 1;
      var A = ACTS[act];
      var lightCn = light === 'green' ? '绿灯亮着' : '红灯亮着';
      var safe, msg;
      if (light === 'green' && A.good && !A.needRed) {
        safe = true;
        msg = '绿灯亮着，你站在斑马线上先看左右再慢慢走——这一次安全通过！走的时候还要一直留意转弯的车，不跑不追。';
      } else if (light === 'red' && A.needRed) {
        safe = true;
        msg = '红灯亮着，你站在路边等，这是最安全的做法。等绿灯亮了，看清左右再走，就更好啦。';
      } else if (A === ACTS.phone) {
        safe = false;
        msg = '低头看手机的时候看不到来车，司机也不一定看得见你。这样可能会非常危险，还可以试试：把手机放进口袋，站在斑马线上先看左右再走。';
      } else if (A === ACTS.run) {
        safe = false;
        msg = '从两辆车中间跑过去，司机来不及刹车。这样可能会受很重的伤，还可以试试：走到斑马线前停下来，等绿灯亮、看清左右再过去。';
      } else if (light === 'red') {
        safe = false;
        msg = '现在是红灯，路上的车正在走。这样可能会被车碰到，还可以试试：站在人行道上等一等，绿灯亮了再走。';
      } else {
        safe = false;
        msg = '绿灯亮着，但你没有站在斑马线上、也没有先看左右。这样可能会让转弯的车来不及躲，还可以试试：走到斑马线上，先看左边、再看右边，再慢慢过去。';
      }
      if (safe) safeCount += 1;
      out3.className = 'result' + (safe ? '' : ' warn');
      out3.innerHTML = '<strong>' + lightCn + '，你选择的做法是：' + A.t + '</strong><br>' +
        '<strong>' + (safe ? '这一次安全通过。' : '这一次不安全。') + '</strong>' + msg;
      render3();
    });
    render3();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__SCENES_JSON__', json.dumps(SCENES, ensure_ascii=False))
             .replace('__SORT_JSON__', json.dumps(SORT_ITEMS, ensure_ascii=False))
             .replace('__SORTBIN_JSON__', json.dumps(SORT_BIN, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "明天要早起上学，晚上八点半动画片还没看完，下面哪个做法更合适？",
         "options": [("把电视关掉，去刷牙洗脸准备睡觉", True),
                     ("一直看到十一点，困得睁不开眼才去睡", False),
                     ("假装去睡觉，偷偷把平板藏进被窝里继续看", False)],
         "explain": "九点前上床，能睡够十个小时，第二天早上眼睛一亮就能起来。"
                    "<strong>错因提醒：</strong>有人误认为「少睡一会儿没关系」——一晚上少睡两三个小时，第二天上课就容易打瞌睡，这是最常见的一个搞混。"},
        {"q": "家里人喊我吃饭了，我刚从外面玩回来，应该先做什么？",
         "options": [("先去水池边用肥皂洗手，再到饭桌前坐下", True),
                     ("拿起筷子就吃，手还脏着", False),
                     ("先玩一会儿玩具，饭放着不吃", False)],
         "explain": "用肥皂把手心和手背都搓一搓，看不见的细菌就被冲走了，吃下去的东西更干净。"
                    "<strong>错因提醒：</strong>常见错误是误认为「手看上去不脏就不用洗」——细菌用眼睛看不见，洗手只要半分钟。"},
        {"q": "放学后想和同学在小区里玩一会儿，出门前应该怎么做？",
         "options": [("跟家里人说一声去哪里、和谁玩、几点回来", True),
                     ("一声不响跑出去，玩够了再回来", False),
                     ("跑到马路边上追来追去", False)],
         "explain": "说一声去哪里，家里人心里踏实，你玩起来也安心，玩完按时回家，下次还放心让你出去玩。"
                    "<strong>错因提醒：</strong>容易搞混「玩得开心」和「玩得安全」——到没有车的地方去玩，才能又开心又安全。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "作息有规律：按时睡，按时起", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们已经知道，每天要到学校上课、要早起出门（And）；可是一到晚上，动画片和小视频总让人舍不得放下，早上就起不来，匆匆忙忙出门，上午饿着肚子打瞌睡（But）；所以这节课就来学一学，几点睡、几点起，睡觉前先把什么放下来（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">让身体舒服的第一件小事，就是<strong>作息有规律</strong>——每天差不多同一个时间睡，同一个时间起。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>晚上八点半到九点上床：</strong>一年级的小朋友每天要睡够<strong>十个小时</strong>左右，第二天早上才能自己醒过来。</div></div>
          <div class="step"><span class="n">2</span><div><strong>睡前把手机、平板放到客厅：</strong>屏幕的光会让眼睛和脑子一直处在兴奋里，<strong>越看越睡不着</strong>。放下来，去刷牙、洗脸、听一段故事。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>早上按时起：</strong>闹钟响了就坐起来，把衣服按顺序穿好，慢慢悠悠吃完早饭再出门。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="一天作息时间表示意图：起床、上学、吃饭、睡觉的时间，附中文标注">
          <figcaption>示意图：有规律的一天——早上六点半起床 · 中午小睡一会儿 · 晚上八点半上床 · 睡前把屏幕放到客厅（教学示意图，人物为极简线条）</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🌙</span><div><strong>记一句小口诀：</strong>八点半，洗漱完；九点前，闭上眼；屏幕放在客厅里，早上六点半自己起。</div></div>
{insight_box([
    {"lens": "看见它", "text": "作息有规律不是一句空话，它就是三个能看见的动作：看钟表、关屏幕、上床躺下。"},
    {"lens": "解释它", "text": "为什么屏幕会让睡不着？因为屏幕的光让脑子以为还是白天，身体就不肯进入休息的状态；早一点放下，才容易睡着。"},
    {"lens": "迁移它", "text": "周末和放假的日子也一样。不用完全一样的时间，但也别睡到中午——作息一乱，回到学校就要难受好几天。"},
])}
    ''', tag="概念一"))

    scene_btns = "\n".join(
        f'            <button class="choice" data-scene="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in SCENES
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：这样做会怎样？", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一件你每天可能遇到的小事，再从三个做法里选一个。<strong>选完会告诉你，这样做以后身体会怎么样。</strong></p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 今天我遇到的一件小事</div>
          <div class="grid" id="habit-stage">
{scene_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 我可以怎么做</div>
          <div class="grid" id="habit-opts">
            <span style="color:var(--muted);font-size:14px">先在上面点一件小事，这里就会出现三个做法。</span>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">聊过几件小事</span><span class="v" id="habit-score">已经聊过 0 / 6 件小事</span></div>
          </div>
          <p class="result warn" id="habit-out" style="margin-top:12px">先点一件今天可能遇到的小事。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💛</span><div><strong>说给你听：</strong>这里的做法没有分数。有些做法只是会让身体不太舒服，换一个试试就好。想一想这样做以后自己会怎么样，比记住「应该怎么做」更要紧。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "吃饭有讲究：饭前洗手，慢慢吃，不挑食", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">让身体舒服的第二件小事，是<strong>吃饭有讲究</strong>。它分成三步，一步一步来就好。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>吃饭前：先洗手</strong></p>
            <p style="color:var(--muted)">把玩具放下，用水打湿双手，抹上肥皂，手心、手背、指缝都搓一搓，冲干净再擦干。</p>
          </div>
          <div class="inner-card">
            <p><strong>吃饭时：慢慢吃</strong></p>
            <p style="color:var(--muted)">坐下来一口一口吃，一口饭嚼十来下。不边吃边玩，不追着跑着吃，也不含着饭说话。</p>
          </div>
          <div class="inner-card">
            <p><strong>吃什么：样样都吃一点</strong></p>
            <p style="color:var(--muted)">米饭、青菜、鸡蛋、豆腐都要吃。不爱吃的菜先尝一小口，这一顿不行，下一顿再试。</p>
          </div>
          <div class="inner-card">
            <p><strong>喝什么：先喝白开水</strong></p>
            <p style="color:var(--muted)">渴了喝白开水。冰饮料、甜饮料少喝，辣条和油炸的小零食少吃。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="正确的洗手步骤示意图：打湿、抹肥皂、搓手心手背、冲干净、擦干，附中文标注">
          <figcaption>示意图：洗手五步——打湿双手 · 抹上肥皂 · 搓手心手背和指缝 · 冲干净 · 擦干（教学示意图，人物为极简线条）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「手看上去不脏就不用洗」。手上的细菌用眼睛看不见，摸过门把手、玩过玩具以后，一定要洗。还有的同学以为「不爱吃的菜一口不吃也没关系」，其实身体需要的营养，正好藏在那些不太爱吃的菜里。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🥬</span><div><strong>记一句口诀：</strong>饭前洗洗手，坐下慢慢嚼；青菜尝一口，渴了喝白开。</div></div>
{insight_box([
    {"lens": "比较它", "text": "同一顿饭，两种吃法：一种洗手坐下慢慢吃，一种手脏着边跑边吃。吃进去的东西一样，身体受不受累却完全不一样。"},
    {"lens": "解释它", "text": "为什么洗手这么要紧？因为手每天摸很多东西，细菌就藏在手上；把它冲掉，肚子才不会闹意见。"},
    {"lens": "迁移它", "text": "在学校也一样：吃午饭前、上完厕所后、摸过公共的东西以后，都要洗一洗。地方换了，做法不变。"},
])}
    ''', tag="概念二"))

    item_btns = "\n".join(
        f'            <button class="sort-item" data-item="{it["id"]}">{it["t"]}</button>' for it in SORT_ITEMS
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：要坚持的，要改一改的，把做法分进两个筐", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一条做法，再点它应该进的筐：<strong>对身体好、要一直做下去的</strong>放一边，<strong>会让自己不舒服、要改一改的</strong>放另一边。</p>
        <div class="lab-panel">
          <div class="sort-bank" id="bin-stage">
{item_btns}
          </div>
          <div class="grid grid-2" style="margin-top:14px">
            <button class="choice" data-bin="keep" style="text-align:center">要坚持的好习惯</button>
            <button class="choice" data-bin="change" style="text-align:center">要改一改的地方</button>
          </div>
          <div class="sort-bins">
            <div class="sort-bin" id="bin-keep"><h4>要坚持的好习惯</h4></div>
            <div class="sort-bin" id="bin-change"><h4>要改一改的地方</h4></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">分类进度</span><span class="v" id="bin-score">已经放好 0 / 8 条</span></div>
          </div>
          <p class="result warn" id="bin-out" style="margin-top:12px">先在上面点一条做法。</p>
        </div>
        <div class="inner-card">
          <p><strong>分完之后，想一想：</strong></p>
          <p style="color:var(--muted)">「要改一改的地方」里，哪一条最像你自己？你打算从明天开始改哪一条？把它写下来。</p>
          <textarea id="syn-answer" rows="3" placeholder="我要改的那一条是……，我打算这样做……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="动手二", bloom="apply"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小安的一天", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>小安上一年级。我们从早到晚跟着他看一天，请你一步一步想一想，他哪几步做得对，为什么。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>晚上八点半：</strong>小安自己关掉动画片，说了一句明天再看下一集，然后去刷牙洗脸，九点前躺下睡着了。</div></div>
          <div class="step"><span class="n">2</span><div><strong>早上六点半：</strong>闹钟一响，他坐起来自己穿好衣服，坐下把热乎乎的早饭吃完才出门。</div></div>
          <div class="step"><span class="n">3</span><div><strong>午饭前：</strong>他到水池边，用肥皂把手心、手背、指缝都搓干净，再坐到饭桌前慢慢吃。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>放学后：</strong>他先跟家里人说了一声去哪里玩，太阳落山前就回家；过马路时站在斑马线边上，绿灯亮了，先看左边、再看右边，才走过去。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「习惯是长大以后自然会有的」。其实好习惯是一天一天练出来的，今天做到一次，明天再做到一次，才慢慢变成你自己的。也有的同学不注意区分「不迟到」和「睡够觉」——早点睡才不会迟到，靠少睡多赶路，反而一天都没精神。</p>
        </div>
        <div class="inner-card">
          <p><strong>说给同桌听：</strong>小安这四步里，你已经做到哪几步？哪一步最想学着做？</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "下面哪句话说得对？",
         "options": [("一年级的小朋友每天要睡够十个小时左右", True),
                     ("只要早上能起来，晚上几点睡都行", False),
                     ("周末可以睡到中午，把平时的觉补回来", False)],
         "explain": "睡够十个小时，长身体和上课听讲都更有精神。周末起床时间也别差太多，作息一乱，回到学校要难受好几天。"
                    "<strong>错因提醒：</strong>常见错误是误认为「睡得晚、起得晚也一样是睡够了」——身体喜欢的是差不多的时间，睡得太晚，睡再久也不舒服。"},
        {"q": "吃饭前，下面哪个做法更好？",
         "options": [("先把玩具放下，用肥皂洗手，再到饭桌前坐下", True),
                     ("手看上去不脏，直接拿起筷子就吃", False),
                     ("边吃边玩玩具，一口饭含很久", False)],
         "explain": "手心、手背、指缝都用肥皂搓一搓，看不见的细菌就被冲走了，肚子不容易疼。"
                    "<strong>错因提醒：</strong>容易搞混「看上去干净」和「真的干净」——细菌用眼睛看不见，洗手只要半分钟。"},
        {"q": "我不太爱吃青菜，下面哪个做法更好？",
         "options": [("先尝一小口，能接受就再吃一点", True),
                     ("把青菜全部挑出来放在桌子上", False),
                     ("只吃米饭和肉，青菜一口都不动", False)],
         "explain": "先尝一小口，慢慢地就会习惯这种味道。青菜里的营养能帮身体长得结实，拉臭臭也更顺畅。"
                    "<strong>错因提醒：</strong>有的同学误认为「不喜欢就一口别吃」——口味是可以慢慢练出来的，今天尝一口，下次再多一口。"}
    ], tag="概念测试"))

    light_btns = '''
            <button class="choice" data-light="green" style="text-align:center">绿灯亮着</button>
            <button class="choice" data-light="red" style="text-align:center">红灯亮着</button>'''
    act_btns = "\n".join([
        '            <button class="choice" data-act="check" style="text-align:left">站在斑马线边上，先看左边、再看右边，慢慢走过去</button>',
        '            <button class="choice" data-act="wait" style="text-align:left">红灯的时候站在路边等，绿灯亮了才走</button>',
        '            <button class="choice" data-act="phone" style="text-align:left">一边低头看手机一边往前走</button>',
        '            <button class="choice" data-act="run" style="text-align:left">看都不看，从两辆车中间跑过去</button>',
    ])
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：安全过马路小演练", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先选现在是什么灯，再选你打算怎么做，然后点「过马路」，看看这一次能不能安全通过。</p>
        <div class="lab-panel">
          <div class="lab-stage" id="road-stage" style="height:120px">
            <div class="airline"></div>
            <div class="lab-obj" style="top:62%;width:150px;height:34px;background:#4ecdc4;border-radius:6px;color:#fff;font-size:13px">斑马线</div>
          </div>
          <div style="font-weight:700;font-size:14px;margin:14px 0 6px">① 现在是什么灯</div>
          <div class="grid grid-2">
{light_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 你打算怎么做</div>
          <div class="grid" id="road-acts">
{act_btns}
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">一共试了几次</span><span class="v" id="road-try">一共试了 0 次</span></div>
            <div class="readout-cell"><span class="k">安全通过</span><span class="v green" id="road-ok">安全通过 0 次</span></div>
          </div>
          <div class="flex-row">
            <button class="choice" id="road-go" style="text-align:center;flex:1">过马路</button>
          </div>
          <p class="result warn" id="road-out" style="margin-top:12px">先选灯，再选做法，然后点「过马路」。</p>
        </div>
        <div class="inner-card">
          <p><strong>试完几种，说一说：</strong></p>
          <p style="color:var(--muted)">哪一次最安全？为什么？请把最安全的做法用一句话写下来，明天上学路上照着做。</p>
          <textarea id="syn-road" rows="3" placeholder="最安全的做法是……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，做法还在不在", TTS["posttest"], [
        {"q": "晚上我特别想再玩一会儿平板，可是已经八点四十了，你会：",
         "options": [("把平板放到客厅充电，去洗漱准备上床", True),
                     ("再玩半个小时，反正明天能起来", False),
                     ("躲在被子里玩，不让家里人看见", False)],
         "explain": "把屏幕放下，眼睛和脑子都能歇一歇，睡着得快，第二天早上也起得来。"
                    "<strong>错因提醒：</strong>别把「今天多玩一会儿」当成小事——一晚少睡三个小时，第二天上课就打瞌睡，这样可能会越拖越晚。"},
        {"q": "放学路上我渴了，身上有一块钱，你会：",
         "options": [("回家喝白开水，路上先不买冷饮", True),
                     ("买一瓶冰饮料，一口气喝半瓶", False),
                     ("买一包辣条，边走边吃", False)],
         "explain": "白开水最解渴，也不会让肚子难受。冰饮料喝多了肚子容易疼，甜饮料喝多了牙齿也不好。"
                    "<strong>错因提醒：</strong>常见错误是误认为「渴了随便什么都能喝」——先想到白开水，身体最舒服。"},
        {"q": "下雨天我要过马路去对面，你会：",
         "options": [("站在斑马线上等绿灯，撑好伞再慢慢走", True),
                     ("趁着没车，从两辆车中间跑过去", False),
                     ("低着头快步走，边走边看脚下的水坑", False)],
         "explain": "下雨天路上更滑，车也看得更不清楚，所以要站在斑马线上等绿灯，撑稳伞再走。"
                    "<strong>错因提醒：</strong>容易搞混「没看到车」和「没有车」——转弯的车常常一下子才出现，先看左右再走才安全。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，记住怎么养成好习惯", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>作息有规律：</strong>晚上八点半到九点上床，睡够十个小时；睡前把屏幕放到客厅；早上按时起，慢慢吃完早饭。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>吃饭有讲究：</strong>饭前用肥皂洗手，坐下慢慢嚼；样样都吃一点，青菜先尝一小口；渴了先喝白开水。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>安全记心上：</strong>出去玩先告诉家里人一声、按时回家；红灯停、绿灯行，站在斑马线上先看左右再走。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>还要记牢一件事：</strong>这三句话都不难，难的是天天做。今天就先挑一句试试——比如今晚八点半，自己把平板放到客厅。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「按时睡、饭前洗手、先看左右」这三个词，说清楚你今天打算做到的一件事。</p>
          <p style="color:var(--muted)">再动一动手：<strong>写一写</strong>你今天几点睡、几点起，把这两个时间写在纸上，明天再写一次，看看能不能差不多。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "说出你今天几点睡、几点起，再算出自己大概睡了几个小时。",
            "说出吃饭前要做到的三件事，每件用一句话说清楚。",
        ],
        [
            "和家里人一起画出「我的一天」小表格，把起床、上学、吃饭、睡觉的时间填进去，坚持记三天。",
            "把「要坚持的好习惯」那一边的四条读给家里人听，请他们说说你哪一条已经做到了。",
        ],
        [
            "设计一张安全过马路的小提示卡，画上红绿灯和斑马线，贴到教室或楼道里，提醒大家先看左右再走。",
            "把安全过马路的做法讲给邻居家的小朋友听，再和他一起到路边看一次红绿灯，说说什么时候才能走。",
            "找一找自己身上最想改掉的一条，想出一个小办法（比如把闹钟放远一点、把饮料换成白开水），试三天再告诉同桌。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": ID,
    "node_id": ID,
    "subject": "politics",
    "subject_cn": "道德与法治",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "义务教育道德与法治课程标准（2022年版2025年修订）· 小学",
    "title": "养成良好习惯",
    "name_en": "Growing Good Daily Habits",
    "grade": 1,
    "grade_cn": "一年级",
    "domain": "health-safety",
    "domain_cn": "生命安全与健康",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学一年级学生的道德与法治课：从「作息有规律」学按时睡、按时起，从「吃饭有讲究」学饭前洗手、慢慢吃、不挑食，再学玩耍与过马路时的安全做法。全课用真实家庭与校园场景中的具体动作展开，让学生在「这样做会怎样」的后果里自己得出结论，懂得良好的卫生习惯、饮食习惯与安全意识为什么让身体更舒服、更安全。",
    "tags": ["养成良好习惯", "作息规律", "饭前洗手", "饮食卫生", "安全意识", "交通规则", "一年级"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学「生命安全与健康」——养成良好的卫生、饮食习惯，有安全意识和自我保护意识，遵守交通规则；对应统编《道德与法治》一年级上册第三单元「养成良好习惯」：作息有规律；吃饭有讲究；对人有礼貌；玩也有学问。",
    "hero_question": "晚上几点睡、饭前要不要洗手、过马路先看哪边——这些小事为什么这么重要？",
    "hero_alt": "养成良好习惯知识结构图：作息有规律、吃饭有讲究、安全记心上 三栏",
    "hero_caption": "养成良好习惯：作息有规律 · 吃饭有讲究 · 安全记心上（玩也有学问）",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "晚上该几点睡？早上怎么才起得来？", "d": "睡够了第二天会有什么不一样", "v": "晚上该几点睡早上怎么才起得来"},
        {"t": "吃饭前要做哪几件事？", "d": "为什么要饭前洗手、为什么要慢慢吃", "v": "吃饭前要做哪几件事"},
        {"t": "哪些零食和饮料要少碰？", "d": "渴了喝什么、饿了吃什么才对", "v": "哪些零食和饮料要少碰"},
        {"t": "怎么玩才安全？过马路要注意什么？", "d": "红灯绿灯、斑马线是怎么回事", "v": "怎么玩才安全过马路要注意什么"},
    ],
    "objectives": [
        "能说出按时睡觉、按时起床的大致时间，知道每天要睡够十个小时左右",
        "能说出吃饭前要做到的三件事，做到饭前洗手、慢慢吃、样样都吃一点",
        "能说出哪些东西要少吃或不吃，知道渴了先喝白开水",
        "能说出玩耍和过马路时的安全做法，知道红灯停、绿灯行，过马路先看左右",
    ],
    "objectives_plain": [
        "能说出按时睡觉、按时起床的大致时间，知道每天要睡够十个小时左右",
        "能说出吃饭前要做到的三件事，做到饭前洗手、慢慢吃、样样都吃一点",
        "能说出哪些东西要少吃或不吃，知道渴了先喝白开水",
        "能说出玩耍和过马路时的安全做法，知道红灯停、绿灯行，过马路先看左右",
    ],
    "standards": [
        {"content": "养成良好的卫生、饮食习惯，有安全意识和自我保护意识，遵守交通规则",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学 生命安全与健康"},
        {"content": "作息有规律；吃饭有讲究；对人有礼貌；玩也有学问",
         "source": "统编《道德与法治》一年级上册 第三单元「养成良好习惯」"},
    ],
    "prereqs": ["pol-e-g1-u2"],
    "prereqs_name": "过好校园生活",
    "prereqs_meta": "pol-e-g1-u2",
    "leads_to": ["pol-e-g1-u4"],
    "next_meta": "pol-e-g1-u4",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "先从一件小事开始：今天晚上你打算几点睡？",
        "problem-anchor": "先定一个小目标：这节课结束时，你能说出自己明天要先做到的那一件事。",
        "objectives": "看清四件事：按时睡按时起、饭前洗手慢慢吃、少喝冰饮多喝白开水、过马路先看左右。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "作息有规律就三件事：八点半到九点上床、睡前把屏幕放到客厅、早上按时起。",
        "lab-1": "六件小事，每件三个做法。选完会告诉你，这样做以后身体会怎么样。",
        "module-2": "吃饭有讲究：饭前洗手、坐下慢慢嚼、样样吃一点、渴了喝白开水。",
        "lab-2": "八条做法分进「要坚持的好习惯」和「要改一改的地方」两个筐。",
        "worked-example": "小安的一天：按时睡、按时起、饭前洗手、出门先告诉家里人、过马路先看左右。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "先选灯，再选做法，然后点过马路——试几种，找出最安全的那一种。",
        "posttest": "出现了想玩平板、想买饮料、下雨天过马路，看看你能不能用上今天的办法。",
        "summary": "三句话：作息有规律、吃饭有讲究、安全记心上。",
        "homework": "三层小任务，先做前两层，第三层可以请家里人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学道德与法治一年级「养成良好习惯」单元，承接上一课「过好校园生活」，把落点从「怎么和老师同学相处」推进到「怎么照顾好自己的身体」。一年级学生懂道理不难，难的是把道理变成每天的动作——所以全课只做三件具体的事：作息有规律（八点半到九点上床、睡前把屏幕放到客厅、早上按时起）、吃饭有讲究（饭前用肥皂洗手、坐下慢慢嚼、样样吃一点、渴了喝白开水）、安全记心上（玩耍先告诉家里人、红灯停绿灯行、过马路先看左右）。三个互动台子都能真的操作：一是六张「这样做会怎样」情境卡，选做法后展开对身体和身边人的后果，反馈一律写成「这样可能会……，还可以试试……」；二是「要坚持的／要改一改的」分类台，把八条做法分进两个筐；三是「安全过马路小演练」，学生自己选灯、选做法，点一下就看到这一次能不能安全通过，并统计安全通过的次数。插图一律为中性简洁的教学示意图（极简线条人物，不使用真实儿童照片）。",
    "plan_table": """| 1 | cover | 养成良好习惯 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 作息有规律：按时睡，按时起 | 承·概念一（卫生与作息） |
| 6 | interactive | 动手一：这样做会怎样？ | 承·情境判断（展开后果） |
| 7 | concept | 吃饭有讲究：饭前洗手，慢慢吃，不挑食 | 承·概念二（饮食习惯） |
| 8 | interactive | 动手二：要坚持的，要改一改的，把做法分进两个筐 | 承·分类操作 |
| 9 | concept | 例题示范：小安的一天 | 转·重难点突破（分步示范 + 易错点） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：安全过马路小演练 | 合·迁移应用（交通规则） |
| 12 | quiz | 后测：换几个新情境，做法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，记住怎么养成好习惯 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：作息有规律 / 吃饭有讲究 / 安全记心上 三栏\n- P5 一天作息时间表示意图（已生成）：起床、上学、吃饭、睡觉的时间，附中文标注\n- P7 洗手五步示意图（已生成）：打湿、抹肥皂、搓手心手背、冲干净、擦干，附中文标注\n- 三张图均为教学示意图，人物仅用极简线条，不使用任何真实儿童照片或可识别肖像\n- 若需补充：一年级「我的一天」表格模板（可由学生手写填写）",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
