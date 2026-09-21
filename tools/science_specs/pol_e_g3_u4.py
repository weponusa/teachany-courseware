# -*- coding: utf-8 -*-
"""小学道德与法治 · 公共生活靠大家（G3）—— 补齐知识树「法治启蒙」空缺

学科语气（道德与法治）：情境案例驱动，情感共鸣 + 价值判断；结论落在「应该怎么做、为什么」，
不做道德说教，也不做法条背诵。三年级要落成能看见、能做到的具体行为。

内容落点（对应统编三上「公共生活靠大家」四课）：
  ① 公共场所，文明言行：小声、排队、让一让，做好自己那一份
  ② 生活离不开规则：规则不是来管我们的，是让每个人都能安心
  ③ 我们都是热心人：爱护公物，参与力所能及的公益活动（捡垃圾、扶门、交还失物、捐书）
  ④ 安全记心上：不跟陌生人走、走散了找工作人员、不碰电气设备、发现危险先离开再告诉大人

三个互动台子都能真操作：
  动手一 = 情境卡选做法 → 展开后果（六件公共场所里的事 × 三个做法，反馈「这样可能会……，还可以试试……」）；
  动手二 = 把八条行为分进「公共生活里该做的 / 要调整的」两个筐；
  综合任务 = 公益小事规划（从九件力所能及的小事里选三件，组成「我们班的公益小计划」）。
插图一律中性简洁扁平插画，不使用真人照片风格。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g3-u4"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "你有没有遇到过这样的时候：在图书馆里，有人大声讲电话，你一个字都看不进去；在公交站，有人从旁边挤上来，排在前面的人反而上不去；在公园的长椅上，有人吃完东西把袋子留在那里，下一个人没法坐。这些地方都不是谁一个人的家，是我们大家一起去的地方。这节课我们做三件事：先看看在公共场所该怎么做、规则为什么不是来管我们的；再说一说，热心人能做的那些小事；最后把安全记在心上。开始吧。",
    "problem-anchor": "开始之前，先选一个你最想弄清楚的问题。是想知道公共场所为什么要有规则，还是想知道排队、让座、小点儿声这些事为什么重要；是想知道自己能为别人做点什么，还是想知道在公共场所要注意哪些安全。选好以后，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出公共场所里三件具体能做到的文明言行：小声、排队、让一让。第二，能说出规则不是来限制我们的，而是让每个人都能安心、都方便。第三，能说出自己能为别人做的两三件力所能及的小事，比如捡起垃圾、扶一下门、把捡到的东西交还。第四，知道公共场所里的安全要求：不跟陌生人走，走散了站在原处或找穿制服的工作人员，不碰公共场所的电气设备，发现危险先离开再告诉大人。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先来看公共场所。公共场所，就是大家一起去的地方：学校的走廊、公交车和地铁、图书馆、公园、超市、医院、车站。在家里，你想怎么说话都可以；可到了这些地方，身边有很多不认识的人，做法就要换一换。换哪三件事最有用呢？第一件，小声。图书馆、车厢、医院里，把手机音量调小，想聊天就走到一边去。第二件，排队。上公交、买水、进校门，先来后到，对每个人都公平，也不会挤到别人。第三件，让一让。看到抱小孩的、提着重东西的、站不太稳的人，愿意的话就让一让。这里要说清楚一件事：让座不是必须做的事，是你愿意做的好事；如果你自己也不舒服、也拿了很多东西，那就说明一下，或者帮着问一问身边的人。规则不是来管我们的，它的用处是让每个人都方便、都安心。",
    "lab-1": "现在请你当一次公共场所的小管家。这里有六件在公共场所常常遇到的事，每一件事都有三个做法。你选一个你觉得合适的，选完立刻会有一段话告诉你为什么；要是选得不太合适，也会告诉你还可以试试什么。",
    "module-2": "再来说热心人。热心人做的事，其实都很小：进商场时帮后面的人扶一下门；看到楼道里的纸屑，弯一下腰；捡到校园卡或者钥匙，交给门卫或者值班的老师；社区做旧书捐赠，从自己的书架上挑一本还很好的书送去。这些都属于力所能及的公益活动——能做的就做一点，做不了的不勉强。还有一件事和热心连在一起：爱护公物。公物是大家共用的东西，长椅、健身器材、图书、路灯、饮水机，用的时候像用自己家里的一样；坏了就告诉大人，不去动手乱拆。最后是安全记心上。第一，不跟陌生人走：有人说是你爸爸妈妈让他来接你，先站在原地，找老师或者穿制服的工作人员打电话确认。第二，和家人走散了，站在原处不乱跑，或者找商场服务台、保安、穿制服的工作人员。第三，不碰公共场所的电气设备和护栏，不把手指伸进插座和门缝。第四，发现危险先离开，再告诉大人。",
    "lab-2": "接下来请你做一次分类。下面有八条在公共场所里的做法，请你判断一下：哪些是公共生活里该做的，放进该做的那一边；哪些是需要调整的，放进要调整的那一边。放好以后，再读一读为什么。",
    "worked-example": "我们一起来看小雨和同学的一次公园小行动。第一步，先看一看：周末他们到公园，发现长椅旁边有不少纸屑，一个提示牌被碰倒在地上。第二步，选一件能做的事：他们商量了一下，决定先收纸屑，再把提示牌扶起来立好。第三步，遇到有人往地上扔瓶子：小雨没有直接说别人不对，而是走过去说了一句「我来帮你拿吧」，然后把瓶子接过去扔进垃圾箱。第四步，看到健身器材的螺丝松了：他们没有自己动手去拧，而是记下位置，去告诉了公园的管理员。第五步，收尾：走的时候把自己带来的东西都带走，座位擦一擦再离开。这一次小行动里，做的事都很小，但公园确实变好了一点。",
    "conceptest-1": "接下来用三个说法考考你，每个说法里都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件任务交给你。下面有九件三年级就能做的公益小事，请你从中选出三件，组成我们班的公益小计划。选好以后，写一句你为什么选这三件。",
    "posttest": "最后一轮，换几个新的小情境来考考你。这次会遇到排队、公物损坏、还有陌生人搭话，看看你能不能用上今天的办法。",
    "summary": "这节课我们记住四句话。第一句，公共场所是大家一起去的地方，文明言行落到三件具体事上：小声、排队、让一让。第二句，规则不是来管我们的，是让每个人都能安心、都方便。第三句，热心人做的事都很小，力所能及就做一点，公物要像用自己家的一样爱惜。第四句，安全记心上：不跟陌生人走，走散了找穿制服的工作人员，不碰电气设备，发现危险先离开再告诉大人。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出公共场所里三件你能做到的文明言行；再写出两条公共场所的安全要求。第二层能力应用，动手做：这个星期，在公共场所做一件力所能及的公益小事，写清楚你做了什么、当时的情况怎么样。第三层迁移挑战，选做：观察一下你家附近的一个公共场所，找出一个让别人不太方便的地方，写一条改进建议，说给家里人或者社区的工作人员听。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 公共场所，文明言行 · 生活离不开规则", "lab-1": "动手一 公共场所小管家",
    "module-2": "概念二 我们都是热心人 · 安全记心上", "lab-2": "动手二 公共生活里该做的 / 要调整的",
    "worked-example": "例题示范 一次公园小行动", "conceptest-1": "概念测试",
    "synthesis": "综合任务 我们班的公益小计划", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：公共场所里常常遇到的六件事 × 三个做法 ──
SCENES = [
    {"id": "s1", "t": "图书馆里，同学想和我讨论一道作业题", "opts": [
        {"k": "a", "t": "先不说话，用笔写给他看，或者走到门外再说", "ok": True,
         "fb": "这样既解决了题目，也没有打扰旁边看书的人。图书馆里「小声」其实是替别人着想。"},
        {"k": "b", "t": "直接在座位上小声讨论，反正声音不大", "ok": False,
         "fb": "这样可能会让身边的人一直听你们说话，书也看不进去。还可以试试：把要说的写在草稿纸上，或者到门外的走廊说。"},
        {"k": "c", "t": "一边讨论一边打开视频给他看", "ok": False,
         "fb": "这样可能会让整个区域都听见声音，别人会来提醒你们。还可以试试：先把视频存好，回家再看。"},
    ]},
    {"id": "s2", "t": "公交站等车的人很多，车来了", "opts": [
        {"k": "a", "t": "排队，等前面的人上完再上", "ok": True,
         "fb": "先来后到，对每个人都公平。排队不是慢，是让大家都能上去。"},
        {"k": "b", "t": "从旁边挤上去，先占个座位", "ok": False,
         "fb": "这样可能会把排队的人挤开，也容易碰到老人和小孩。还可以试试：跟着队伍走，上车后再看看有没有需要让座的人。"},
        {"k": "c", "t": "站在车门口不动，等别人让开", "ok": False,
         "fb": "这样可能会挡住后面的人上车。还可以试试：往车厢里走一走，门口留给要下车和要上车的人。"},
    ]},
    {"id": "s3", "t": "车厢里，一位老奶奶扶着扶手站着", "opts": [
        {"k": "a", "t": "如果自己方便，就安静地站起来，说一句「您坐这儿」", "ok": True,
         "fb": "安静地让一让，对方最自在。这一句轻轻的话，比什么都有用。"},
        {"k": "b", "t": "装作没看见，低头看窗外", "ok": False,
         "fb": "这样可能会让奶奶一路都站得很吃力。还可以试试：不方便让座时，帮奶奶问问旁边的人能不能让一让。"},
        {"k": "c", "t": "大声喊一句「我让座啦」，让大家都看过来", "ok": False,
         "fb": "这样可能会让奶奶站在那儿不好意思。还可以试试：轻轻站起来，把座位腾出来就好，不必让所有人都知道。"},
    ]},
    {"id": "s4", "t": "在公园吃完零食，手里剩一个空袋子", "opts": [
        {"k": "a", "t": "把袋子收好，找到垃圾箱再扔", "ok": True,
         "fb": "多走几步路，公园就少一处垃圾。这就是最实在的爱护公共环境。"},
        {"k": "b", "t": "塞进草丛里，反正看不见", "ok": False,
         "fb": "这样可能会让公园越来越脏，也容易被小动物误食。还可以试试：先把袋子放在自己包里，遇到垃圾箱再扔。"},
        {"k": "c", "t": "放在长椅上，等打扫的阿姨来收", "ok": False,
         "fb": "这样可能会让下一位想坐的人没法坐。还可以试试：自己带走，或者多找两步路找个垃圾箱。"},
    ]},
    {"id": "s5", "t": "公园的长椅上有一片脚印，旁边还有一个歪倒的提示牌", "opts": [
        {"k": "a", "t": "把提示牌扶正立好，长椅用纸巾擦一下", "ok": True,
         "fb": "顺手做的小事，下一个人就能安心坐下。爱护公物就是这样一件一件做出来的。"},
        {"k": "b", "t": "不管，反正不是我弄的", "ok": False,
         "fb": "这样可能会让长椅一直没人敢坐，提示牌也一直倒着。还可以试试：扶起来、擦一下，都是几秒钟的事。"},
        {"k": "c", "t": "拍下来发到网上，说这里又脏又乱", "ok": False,
         "fb": "这样可能会让大家都绕开这个地方，却没人去收拾。还可以试试：先做一件小事，再告诉管理员需要修的地方。"},
    ]},
    {"id": "s6", "t": "在商场里，我和家人走散了", "opts": [
        {"k": "a", "t": "站在原处不走动，或者找服务台、保安、穿制服的工作人员帮忙", "ok": True,
         "fb": "站在原地，家人回头才找得到你；穿制服的工作人员是最可靠的求助对象。"},
        {"k": "b", "t": "自己到处找，跑到商场外面看看", "ok": False,
         "fb": "这样可能会越走越远，家里人也更难找到你。还可以试试：回到走散的地方等，或者请工作人员广播。"},
        {"k": "c", "t": "跟着一位说「我带你去找妈妈」的陌生人走", "ok": False,
         "fb": "这样很危险。有人这样说的话，先站在原地，请工作人员帮着打电话确认。还可以试试：走到柜台或者保安旁边，那里有监控，也有大人。"},
    ]},
]

# ── 动手二：公共生活里该做的 / 要调整的（八条行为分进两个筐） ──
SORT_ITEMS = [
    {"id": "k1", "t": "在车厢里把手机音量调小，想打电话就走到一边", "bin": "good",
     "why": "小声一点，是公共场所里最容易被做到、也最让人舒服的一件事。"},
    {"id": "k2", "t": "上公交、买水、进校门都顺着队伍排", "bin": "good",
     "why": "先来后到，对每个人都公平，也不会挤到别人。"},
    {"id": "k3", "t": "看到抱小孩的人，方便就让一让，不方便就说一声", "bin": "good",
     "why": "让座是愿意做的事。愿意就让，不方便就说清楚，两种都可以。"},
    {"id": "k4", "t": "捡到别人的校园卡，交给门卫或者值班老师", "bin": "good",
     "why": "失物交还，是帮了别人一个大忙，也是公共生活里的信任。"},
    {"id": "k5", "t": "把零食袋塞进花丛里，反正没人看见", "bin": "tune",
     "why": "这样可能会让公园越来越脏，也容易伤到小动物。还可以试试：先放进自己的包里，遇到垃圾箱再扔。"},
    {"id": "k6", "t": "坐公交时把两条腿搭在旁边的座位上", "bin": "tune",
     "why": "这样可能会让想坐的人没法坐。还可以试试：把腿收回来，包也抱在身前。"},
    {"id": "k7", "t": "看见提示牌倒了，路过就当没看见", "bin": "tune",
     "why": "这样可能会让下一个人被绊一下。还可以试试：扶起来立好，几秒钟的事；自己扶不动就告诉管理员。"},
    {"id": "k8", "t": "在公共场所的插座和电器旁边玩，试着按按钮", "bin": "tune",
     "why": "这样很危险。公共场所的电气设备不要碰。还可以试试：把这件事告诉大人，或者去别的地方玩。"},
]
SORT_BIN = {"good": "公共生活里该做的", "tune": "要调整的"}

# ── 综合任务：公益小事规划（九件力所能及的小事里选三件） ──
GOOD_DEEDS = [
    {"id": "g1", "n": "帮后面进门的人扶一下门", "why": "几秒钟的事，对方会轻松很多。"},
    {"id": "g2", "n": "看到楼道里的纸屑，弯一下腰捡起来", "why": "一个人捡一点，整条楼道就不一样了。"},
    {"id": "g3", "n": "把捡到的校园卡、钥匙交给门卫", "why": "丢东西的人正在着急，你这一趟帮了大忙。"},
    {"id": "g4", "n": "从自己的书架上挑一本好书的旧书，参加社区旧书捐赠", "why": "对你来说是旧书，对别人来说可能是新的故事。"},
    {"id": "g5", "n": "在公交车上，方便时给需要的人让一让", "why": "愿意就让，这一份心意很实在。"},
    {"id": "g6", "n": "提醒同学把音量调小，自己也把手机声音关掉", "why": "小声是公共场所里最容易做到的好事。"},
    {"id": "g7", "n": "看到健身器材的螺丝松了，去告诉管理员", "why": "自己不动手修，把该让大人做的事交给大人。"},
    {"id": "g8", "n": "帮邻居家的老爷爷把门口的快递搬到门里", "why": "先问一句「要不要帮忙」，再动手。"},
    {"id": "g9", "n": "在小区里做一张「垃圾分类」的小提示卡，贴在垃圾箱旁边", "why": "把自己会的事写下来告诉大家，也是一种公益。"},
]

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g3-u4 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 公共场所小管家：六件事 × 三个做法 → 温和反馈（不判错、不贴标签）
   3) 公共生活里该做的 / 要调整的：八条行为分进两个筐
   4) 我们班的公益小计划：从九件小事里选三件（可点可撤），写一句理由
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

  /* ---------- 2. 公共场所小管家 ---------- */
  var SCENES = __SCENES_JSON__;
  var stage1 = document.getElementById('case-stage');
  if (stage1) {
    var curScene = null, doneScene = {};
    var out1 = document.getElementById('case-out');
    function sceneById(id) {
      for (var i = 0; i < SCENES.length; i++) { if (SCENES[i].id === id) return SCENES[i]; }
      return null;
    }
    function render1() {
      document.querySelectorAll('[data-case]').forEach(function (b) {
        var k = b.dataset.case;
        b.classList.toggle('selected', k === curScene);
        b.classList.toggle('correct', !!doneScene[k]);
      });
      document.getElementById('case-score').textContent =
        '已经想过 ' + Object.keys(doneScene).length + ' / ' + SCENES.length + ' 件事';
    }
    function paintOptions() {
      var box = document.getElementById('case-opts');
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
            out1.innerHTML = '<strong>这个做法挺好。</strong>' + o.fb;
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
    document.querySelectorAll('[data-case]').forEach(function (b) {
      b.addEventListener('click', function () {
        curScene = b.dataset.case;
        var S = sceneById(curScene);
        if (doneScene[curScene]) {
          out1.className = 'result';
          out1.innerHTML = '<strong>这件事已经想过啦。</strong>你上次选的做法挺合适，记住它就好。';
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

  /* ---------- 3. 公共生活里该做的 / 要调整的 ---------- */
  var ITEMS = __SORT_JSON__;
  var BINN = __SORTBIN_JSON__;
  var stage2 = document.getElementById('pub-stage');
  if (stage2) {
    var pickItem = null, placed = {};
    var out2 = document.getElementById('pub-out');
    function render2() {
      document.querySelectorAll('[data-item]').forEach(function (b) {
        var k = b.dataset.item;
        b.classList.toggle('selected', k === pickItem);
        b.classList.toggle('done', !!placed[k]);
        b.disabled = !!placed[k];
      });
      document.getElementById('pub-score').textContent =
        '已经放好 ' + Object.keys(placed).length + ' / ' + ITEMS.length + ' 条';
      var a = document.getElementById('pub-bin-a');
      var b2 = document.getElementById('pub-bin-b');
      a.innerHTML = ''; b2.innerHTML = '';
      ITEMS.forEach(function (it) {
        if (!placed[it.id]) return;
        var s = document.createElement('div');
        s.className = 'tag';
        s.textContent = it.t;
        (it.bin === 'good' ? a : b2).appendChild(s);
      });
      if (!a.innerHTML) a.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
      if (!b2.innerHTML) b2.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
    }
    document.querySelectorAll('[data-item]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (placed[b.dataset.item]) return;
        pickItem = b.dataset.item;
        out2.className = 'result warn';
        out2.innerHTML = '<strong>你选的是：' + b.textContent + '</strong><br>想一想，它是「公共生活里该做的」，还是「要调整的」？';
        render2();
      });
    });
    document.querySelectorAll('[data-pub-bin]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pickItem) {
          out2.className = 'result warn';
          out2.textContent = '先在上面点一条做法，再选筐。';
          return;
        }
        var it = null;
        for (var i = 0; i < ITEMS.length; i++) { if (ITEMS[i].id === pickItem) it = ITEMS[i]; }
        if (b.dataset.pubBin === it.bin) {
          placed[it.id] = true;
          out2.className = 'result';
          out2.innerHTML = '<strong>放对了，它属于「' + BINN[it.bin] + '」。</strong>' + it.why;
          pickItem = null;
          if (Object.keys(placed).length === ITEMS.length) {
            out2.className = 'result';
            out2.innerHTML = '<strong>八条全放对了！</strong>记住这句口诀：<strong>小声一点、顺着队排，' +
              '公物爱惜、危险不碰。</strong>';
          }
        } else {
          out2.className = 'result warn';
          out2.innerHTML = '<strong>再想一想这条做法。</strong>' + it.why +
            '<br><span style="color:var(--muted)">常见错误：容易把「大家都这么做」误认为「这样做没关系」——' +
            '先看这件事有没有让别人不方便、有没有危险，答案就清楚了。</span>';
        }
        render2();
      });
    });
    render2();
  }

  /* ---------- 4. 我们班的公益小计划 ---------- */
  var DEEDS = __DEEDS_JSON__;
  var stage3 = document.getElementById('plan-stage');
  if (stage3) {
    var chosen = {}, limit = 3;
    var out3 = document.getElementById('plan-out');

    function render3() {
      var keys = Object.keys(chosen);
      document.querySelectorAll('#plan-stage [data-deed]').forEach(function (b) {
        b.classList.toggle('selected', !!chosen[b.dataset.deed]);
      });
      document.getElementById('plan-score').textContent =
        '已经选了 ' + keys.length + ' / ' + limit + ' 件';
      var box = document.getElementById('plan-chosen');
      box.innerHTML = '';
      if (keys.length === 0) {
        box.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有选。先在上面挑三件你想做的事。</span>';
      }
      DEEDS.forEach(function (d) {
        if (!chosen[d.id]) return;
        var s = document.createElement('div');
        s.className = 'tag';
        s.textContent = d.n;
        box.appendChild(s);
      });
    }
    document.querySelectorAll('#plan-stage [data-deed]').forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.dataset.deed;
        if (chosen[k]) {
          delete chosen[k];
          out3.className = 'result warn';
          out3.innerHTML = '<strong>已取消这一件。</strong>再点一次就能重新选上。';
          render3();
          return;
        }
        if (Object.keys(chosen).length >= limit) {
          out3.className = 'result warn';
          out3.innerHTML = '<strong>已经选满三件了。</strong>想让计划更做得成，先把这三件做好；' +
            '要换一件，就先点掉一件，再选新的。';
          render3();
          return;
        }
        chosen[k] = true;
        var d = null;
        for (var i = 0; i < DEEDS.length; i++) { if (DEEDS[i].id === k) d = DEEDS[i]; }
        out3.className = 'result';
        out3.innerHTML = '<strong>选上了：' + d.n + '</strong>' + d.why;
        render3();
        if (Object.keys(chosen).length === limit) {
          out3.className = 'result';
          out3.innerHTML = '<strong>三件都选好了！</strong>这就是我们班的公益小计划。' +
            '做计划有个小窍门：<strong>选做得成的、选自己方便的时候能做的。</strong>';
        }
      });
    });
    render3();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__SCENES_JSON__', json.dumps(SCENES, ensure_ascii=False))
             .replace('__SORT_JSON__', json.dumps(SORT_ITEMS, ensure_ascii=False))
             .replace('__SORTBIN_JSON__', json.dumps(SORT_BIN, ensure_ascii=False))
             .replace('__DEEDS_JSON__', json.dumps(GOOD_DEEDS, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "在图书馆看书时，想和同学说一道题，下面哪个做法更好？",
         "options": [("用笔写在草稿纸上，或者走到门外再说", True),
                     ("在座位上小声讨论，声音不大就没关系", False),
                     ("打开视频给同学看，这样讲得更清楚", False)],
         "explain": "在图书馆里，小声一点就是替别人着想。写在纸上、走到门外，题目照样能说清楚。"
                    "<strong>错因提醒：</strong>常见错误是误认为「我声音不大就不算吵」——"
                    "在很安静的地方，一点点声音别人也能听见。"},
        {"q": "下面哪句话说得对？",
         "options": [("规则不是来管我们的，是让每个人都能安心、都方便", True),
                     ("规则越少越好，没人管最自在", False),
                     ("只有大人才需要守规则，小学生可以随便一点", False)],
         "explain": "排队、小声、让一让，这些做法让每个人都能用上这个地方。"
                    "<strong>错因提醒：</strong>有的同学误认为「规则就是限制」——"
                    "想一想要是没有排队，谁都上不了车。"},
        {"q": "在商场里和家人走散了，下面哪个做法最合适？",
         "options": [("站在原处不走动，或者找服务台、保安、穿制服的工作人员帮忙", True),
                     ("自己到处找，跑到商场外面看看", False),
                     ("跟着一位说带你去找家人的陌生人走", False)],
         "explain": "站在原处，家人才找得到你；穿制服的工作人员是最可靠的求助对象。"
                    "<strong>错因提醒：</strong>容易把「有人愿意帮忙」误认为「可以跟着他走」——"
                    "先请工作人员打电话确认，这一步不能省。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "公共场所，文明言行 · 生活离不开规则", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们每天都去这些地方：学校门口、公交车上、图书馆、公园、超市（And）；可是在这些地方，常常有人大声讲电话、从旁边挤上车、把脚搭在旁边的座位上，别人就不方便了（But）；所以我们要弄清楚一件事：规则不是来管我们的，是让每个人都能安心（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">公共场所，就是<strong>大家一起去的地方</strong>。在家里你想怎么说话都行；到了这些地方，身边有很多不认识的人，做法就要换一换。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>小声：</strong>图书馆、车厢、医院里把音量调小；想聊天就走到一边去。</div></div>
          <div class="step"><span class="n">2</span><div><strong>排队：</strong>上公交、买水、进校门，先来后到，对每个人都公平。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>让一让：</strong>看到抱小孩的、提重物的、站不稳的人，愿意的话就让一让。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="公共场所文明言行示意图：图书馆小声、公交站排队、车厢里让座，附中文标注">
          <figcaption>概念图：公共场所里的三件具体事——小声 · 排队 · 让一让（教学示意图，中性简洁扁平插画）</figcaption>
        </figure>
        <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(78,205,196,.45)">
          <p><strong>让座这件事，要说清楚</strong></p>
          <p style="color:var(--muted)">让座不是必须做的事，是你<strong>愿意</strong>做的好事。如果你自己也不舒服、也拿了很多东西，那就说明一下，或者帮着问一问身边的人能不能让一让——两种做法都很好，不用不好意思。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「规则就是来限制我的，越少越自在」。可是一旦没有排队、没有小声，最先不方便的其实是排在后面的自己。规则真正管住的，是那些会让别人不方便的做法。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "小声、排队、让一让，看着是三件事，其实是同一件事：先想一想身边还有别人。"},
    {"lens": "解释它", "text": "为什么说规则不是限制？因为公共场所是大家共用的地方，一个人的方便常常就是另一个人的不方便——规则把这个分寸定清楚了。"},
    {"lens": "迁移它", "text": "这个思路在家里也用得上：晚上家里人已经睡了，你会自动把声音放轻——这也是「先想一想身边还有别人」。"},
])}
    ''', tag="概念一"))

    case_btns = "\n".join(
        f'            <button class="choice" data-case="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in SCENES
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：公共场所小管家，你会怎么做？", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一件在公共场所里常常遇到的事，再从三个做法里选一个。<strong>选得好会告诉你为什么，选得不太合适也会告诉你还可以试试什么。</strong></p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 我遇到的一件事</div>
          <div class="grid" id="case-stage">
{case_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 我可以怎么做</div>
          <div class="grid" id="case-opts">
            <span style="color:var(--muted);font-size:14px">先在上面点一件事，这里就会出现三个做法。</span>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">想过几件事</span><span class="v" id="case-score">已经想过 0 / 6 件事</span></div>
          </div>
          <p class="result warn" id="case-out" style="margin-top:12px">先点一件可能遇到的事。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💛</span><div><strong>说给你听：</strong>这里的做法没有分数。有些做法只是会让别人不太方便，换一个试试就好。拿不准的时候，先问一句身边的大人，是很好的办法。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "我们都是热心人 · 安全记心上", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">热心人做的事，其实<strong>都很小</strong>。能做的就做一点，做不了的不勉强——这就是力所能及的公益活动。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>顺手就能做的</strong></p>
            <p style="color:var(--muted)">帮后面进门的人扶一下门 · 看到纸屑弯一下腰 · 把捡到的校园卡、钥匙交给门卫 · 从自己的书架上挑一本还很好的书送去旧书捐赠。</p>
          </div>
          <div class="inner-card">
            <p><strong>爱护公物</strong></p>
            <p style="color:var(--muted)">公物是大家共用的：长椅、健身器材、图书、路灯、饮水机。用的时候像用自己家里的一样；坏了就告诉大人，不自己动手乱拆。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="热心人与公共安全示意图：扶门、捡垃圾、交还失物、走散时找工作人员，附中文标注">
          <figcaption>情境图：我们都是热心人 · 安全记心上（教学示意图，中性简洁扁平插画）</figcaption>
        </figure>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>安全记心上：四条要记住的</strong></p>
          <p style="color:var(--muted)">第一，<strong>不跟陌生人走</strong>：有人说「你爸爸妈妈让我来接你」，先站在原地，找老师或穿制服的工作人员打电话确认。<br>
          第二，<strong>走散了不乱跑</strong>：站在原处，或者找服务台、保安、穿制服的工作人员。<br>
          第三，<strong>不碰公共场所的电气设备和护栏</strong>，不把手指伸进插座和门缝。<br>
          第四，<strong>发现危险先离开，再告诉大人</strong>。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「做好事一定要做大事才算」。可是三年级能做的小事一大把：扶一下门、弯一下腰、把失物交回去——这些小事加在一起，公共场所就变得舒服多了。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "「热心」不是喊出来的，是做出来的：一句话、一个弯腰、一趟交还失物，都很具体。"},
    {"lens": "比较它", "text": "同样是看到别人乱扔垃圾：一种是当面说「你怎么这么不讲卫生」，一种是走过去说「我来帮你拿吧」——后者更容易让人愿意改。"},
    {"lens": "迁移它", "text": "这套做法在小区里也用得上：楼道里有人乱放东西，先想一想是不是他实在没地方放，再决定怎么和大人说这件事。"},
])}
    ''', tag="概念二"))

    item_btns = "\n".join(
        f'            <button class="sort-item" data-item="{it["id"]}">{it["t"]}</button>' for it in SORT_ITEMS
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：公共生活里该做的 / 要调整的，把做法分进两个筐", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一条做法，再点它应该进的筐：<strong>公共生活里该做的</strong>放一边，<strong>要调整的</strong>放另一边。</p>
        <div class="lab-panel">
          <div class="sort-bank" id="pub-stage">
{item_btns}
          </div>
          <div class="grid grid-2" style="margin-top:14px">
            <button class="choice" data-pub-bin="good" style="text-align:center">公共生活里该做的</button>
            <button class="choice" data-pub-bin="tune" style="text-align:center">要调整的</button>
          </div>
          <div class="sort-bins">
            <div class="sort-bin" id="pub-bin-a"><h4>公共生活里该做的</h4></div>
            <div class="sort-bin" id="pub-bin-b"><h4>要调整的</h4></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">分类进度</span><span class="v" id="pub-score">已经放好 0 / 8 条</span></div>
          </div>
          <p class="result warn" id="pub-out" style="margin-top:12px">先在上面点一条做法。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧺</span><div><strong>想一想：</strong>「要调整的」那一边里，有些做法并不是坏心，只是没想到别人——换一个做法就好。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小雨和同学的一次公园小行动", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>周末，小雨和同学去附近的公园。长椅旁边有不少纸屑，一个提示牌被碰倒在地上。他们决定做点什么。请你看看他们是怎么做的。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先看一看：</strong>走一圈，看看哪里让别人不方便——纸屑、倒下的提示牌、还有一处螺丝松了的健身器材。</div></div>
          <div class="step"><span class="n">2</span><div><strong>选一件能做的事：</strong>商量一下，决定先收纸屑，再把提示牌扶起来立好。</div></div>
          <div class="step"><span class="n">3</span><div><strong>遇到有人乱扔：</strong>小雨没有当面说别人不对，而是走过去说了一句「我来帮你拿吧」，把瓶子接过来扔进垃圾箱。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>该大人做的交给大人：</strong>看到螺丝松了，他们没有自己动手拧，而是记下位置，去告诉了公园管理员。</div></div>
        </div>
        <div class="inner-card">
          <p><strong>收尾也有讲究</strong></p>
          <p style="color:var(--muted)">走的时候把自己带来的东西都带走，座位擦一擦再离开。做公益不是做给别人看的，走的时候不留下新的麻烦，这件事才算做完。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「热心就是当面指出别人不对」。可小雨换了一种做法：先说一句「我来帮你拿吧」——对方更容易接受，地上的瓶子也真的进了垃圾箱。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "下面哪句话说得对？",
         "options": [("公共场所里的规则，是让每个人都能安心、都方便", True),
                     ("规则就是来限制我们的，越少越自在", False),
                     ("只要没人看见，怎么做都可以", False)],
         "explain": "排队、小声、让一让，这些做法保护的是每一个用这个地方的人。"
                    "<strong>错因提醒：</strong>常见错误是误认为「规则是对着我的」——"
                    "想一想没有排队的时候，最先上不去车的是谁。"},
        {"q": "在车厢里看到一位站不太稳的老人，下面哪个做法更好？",
         "options": [("自己方便就安静地站起来让一让，不方便就帮着问一问身边的人", True),
                     ("装作没看见，低头看窗外", False),
                     ("大声说「我让座了」，让大家都看过来", False)],
         "explain": "让座是愿意做的事，安静地让最能照顾对方的心情。"
                    "<strong>错因提醒：</strong>有的同学误认为「不让座就是不好的孩子」——"
                    "如果自己也不舒服，说明一下、帮着问一问，同样是在帮忙。"},
        {"q": "看到公园里的健身器材有一颗螺丝松了，下面哪个做法更好？",
         "options": [("记下位置，去告诉公园的管理员", True),
                     ("自己找工具把它拧紧", False),
                     ("不管，反正不是自己弄坏的", False)],
         "explain": "自己动手修公共设施很危险，也可能修得更坏；告诉管理员才是对的做法。"
                    "<strong>错因提醒：</strong>容易把「自己修一下更快」误认为「热心」——"
                    "该大人做的事，就交给大人。"}
    ], tag="概念测试"))

    deed_btns = "\n".join(
        f'            <button class="sort-item" data-deed="{g["id"]}">{g["n"]}</button>' for g in GOOD_DEEDS
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：我们班的公益小计划，从九件小事里选出三件", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">下面是九件三年级就能做的公益小事。<strong>点一点，选出三件</strong>，组成我们班的公益小计划；点错了再点一次就能取消。</p>
        <div class="lab-panel">
          <div class="sort-bank" id="plan-stage">
{deed_btns}
          </div>
          <div class="inner-card" style="margin-top:14px">
            <p><strong>我们班的公益小计划</strong></p>
            <div id="plan-chosen" style="display:flex;flex-wrap:wrap;gap:6px"><span style="color:var(--muted);font-size:14px">还没有选。先在上面挑三件你想做的事。</span></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">已选件数</span><span class="v" id="plan-score">已经选了 0 / 3 件</span></div>
          </div>
          <p class="result warn" id="plan-out" style="margin-top:12px">先在上面点一件你想做的事。</p>
        </div>
        <div class="inner-card">
          <p><strong>选好之后，写一句话：</strong></p>
          <p style="color:var(--muted)">你为什么选这三件？打算什么时候做？写在下面。</p>
          <textarea id="syn-answer" rows="3" placeholder="我选这三件，因为……，我打算……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，办法还在不在", TTS["posttest"], [
        {"q": "公交站上，排队的人已经站了一长串，车来了，下面哪个做法更好？",
         "options": [("跟着队伍上，上车后看看有没有需要让座的人", True),
                     ("从旁边挤上去，先占一个座位", False),
                     ("站在车门口不动，等别人让开", False)],
         "explain": "先来后到，对每个人都公平；上车后再看看有没有需要让一让的人。"
                    "<strong>错因提醒：</strong>常见错误是误认为「抢一步不算什么」——"
                    "一个人挤，整条队都会乱。"},
        {"q": "在小区里看到长椅的一条腿有点松，坐上去会晃，下面哪个做法更好？",
         "options": [("不做上去，把位置和情况告诉小区的工作人员或者大人", True),
                     ("试着自己找工具把它钉牢", False),
                     ("不管它，反正自己不坐就行", False)],
         "explain": "公共设施坏了，报告给管理的人最稳妥，也最安全。"
                    "<strong>错因提醒：</strong>容易把「自己修一下更快」误认为「热心」——"
                    "自己动手可能受伤，也可能让别人更危险。"},
        {"q": "放学路上，一位不认识的叔叔说：「你妈妈让我来接你，跟我走吧。」下面哪个做法最合适？",
         "options": [("站在原地不走，回到学校门口找老师，或者请穿制服的人帮忙打电话确认", True),
                     ("跟他走，反正他知道我妈妈的名字", False),
                     ("自己一个人绕小路回家", False)],
         "explain": "知道名字不等于真的是家里人安排的，站在原地、找老师或工作人员确认最安全。"
                    "<strong>错因提醒：</strong>有的同学误认为「人家说得这么清楚，应该没问题」——"
                    "遇到这种情况，一定要先跟大人核实。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：四句话，讲清公共生活靠大家", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>文明言行三件事：</strong>小声、排队、让一让——先想一想身边还有别人。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>生活离不开规则：</strong>规则不是来管我们的，是让每个人都能安心、都方便。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>我们都是热心人：</strong>力所能及就做一点；公物像用自己家的一样爱惜，坏了报告大人。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>安全记心上：</strong>不跟陌生人走，走散了找穿制服的工作人员，不碰电气设备，发现危险先离开再告诉大人。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>一句口诀：</strong>小声一点、顺着队排，公物爱惜、危险不碰。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「小声、排队、让一让」这三个说法，说清楚你在公共场所会怎么做。</p>
          <p style="color:var(--muted)">再动一动手：<strong>写一写</strong>你打算做的三件小事，写清做什么、什么时候做。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写出公共场所里三件你能做到的文明言行，每件写一句话。",
            "写出两条公共场所的安全要求，比如走散了怎么办。",
            "说出让座这件事里，什么叫「愿意就让」，什么叫「不方便就说一声」。",
        ],
        [
            "这个星期，在公共场所做一件力所能及的公益小事（比如捡起垃圾、扶一下门、把捡到的东西交还），写清楚你做了什么、当时的情况怎么样。",
            "和家里人一起去一次公园或者小区，找出一个让别人不太方便的地方，写下来。",
        ],
        [
            "观察你家附近的一个公共场所，找出一个可以改进的地方，写一条具体建议，说给家里人或者社区的工作人员听。",
            "问一问家里的大人：他小时候在公共场所，有没有一件别人帮过他的小事，到现在还记得？把他的话记下来，和今天学的连起来说一说。",
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
    "title": "公共生活靠大家",
    "name_en": "Public Life Depends on Everyone",
    "grade": 3,
    "grade_cn": "三年级",
    "domain": "rule-of-law",
    "domain_cn": "法治启蒙",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学三年级的道德与法治课：先把公共场所里的文明言行落成三件具体的事——小声、排队、让一让，并说清规则不是来限制我们的，而是让每个人都能安心、都方便；再说热心人做的那些小事：扶一下门、弯一下腰、把失物交还、爱护公物、参与力所能及的公益活动；最后把公共场所的安全要求讲透：不跟陌生人走、走散了找穿制服的工作人员、不碰电气设备、发现危险先离开再告诉大人。全课以真实情境与可操作的选择为主，三个互动台子分别是情境卡选做法展开后果、把八条行为分进「公共生活里该做的／要调整的」两个筐、以及从九件力所能及的小事里选出三件组成「我们班的公益小计划」。",
    "tags": ["公共生活靠大家", "公共场所文明言行", "生活离不开规则", "我们都是热心人", "安全记心上", "爱护公物", "公益活动", "三年级", "法治启蒙"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学「法治启蒙」——遵守公共秩序，爱护公共设施，参与力所能及的公益活动；对应统编《道德与法治》三年级上册「公共生活靠大家」：公共场所，文明言行；我们都是热心人；生活离不开规则；安全记心上。",
    "hero_question": "在公共场所，怎样做才能让大家都方便、都安心？",
    "hero_alt": "公共生活靠大家知识结构图：公共场所文明言行、生活离不开规则、我们都是热心人·安全记心上 三栏",
    "hero_caption": "公共生活靠大家：公共场所文明言行 · 生活离不开规则 · 我们都是热心人（小声 · 排队 · 让一让 · 安全记心上）",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "公共场所为什么要有规则？", "d": "规则到底是在管谁", "v": "公共场所为什么要有规则"},
        {"t": "排队、让座、小点儿声，为什么重要？", "d": "这三件事具体怎么做", "v": "排队、让座、小点儿声为什么重要"},
        {"t": "热心人可以做哪些事？", "d": "三年级力所能及的小事", "v": "热心人可以做哪些事"},
        {"t": "在公共场所要注意哪些安全？", "d": "走散了、陌生人搭话怎么办", "v": "在公共场所要注意哪些安全"},
    ],
    "objectives": [
        "能说出公共场所里三件具体能做到的文明言行：小声、排队、让一让",
        "能说出规则不是来限制我们的，而是让每个人都能安心、都方便",
        "能说出自己能为别人做的两三件力所能及的小事，并愿意做一件",
        "知道公共场所里的安全要求：不跟陌生人走、走散了找穿制服的工作人员、不碰电气设备、发现危险先离开再告诉大人",
    ],
    "objectives_plain": [
        "能说出公共场所里三件具体能做到的文明言行：小声、排队、让一让",
        "能说出规则不是来限制我们的，而是让每个人都能安心、都方便",
        "能说出自己能为别人做的两三件力所能及的小事，并愿意在公共场所做一件",
        "知道公共场所里的安全要求，特别是走散和遇到陌生人搭话时该怎么做",
    ],
    "standards": [
        {"content": "遵守公共秩序，爱护公共设施，参与力所能及的公益活动。",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学 法治启蒙"},
        {"content": "公共场所，文明言行；我们都是热心人；生活离不开规则；安全记心上",
         "source": "统编《道德与法治》三年级上册「公共生活靠大家」"},
    ],
    "prereqs": ["pol-e-g3-u3"],
    "prereqs_name": "在集体中长大",
    "prereqs_meta": "pol-e-g3-u3",
    "leads_to": ["pol-e-g4-u1"],
    "next_meta": "pol-e-g4-u1",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "图书馆里的一声电话、公交站上的一次挤，都会让身边的人不方便。这节课我们看看该怎么做。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能说出三件自己在公共场所会做的小事。",
        "objectives": "看清四件事：文明言行有哪些、规则是为了什么、我能做什么、要注意哪些安全。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "公共场所三件事：小声、排队、让一让；规则不是来管我们的，是让大家都方便。",
        "lab-1": "六件公共场所里的事，每件三个做法。选得不太合适也不会说你错，只会告诉你还可以试试什么。",
        "module-2": "热心人做的小事、公物要爱惜，还有四条安全要求：不跟陌生人走、走散了找工作人员。",
        "lab-2": "把八条做法分进「公共生活里该做的」和「要调整的」两个筐，分完读一读为什么。",
        "worked-example": "公园小行动五步：先看一看、选一件能做的、遇到乱扔先帮一句、该大人做的交给大人、收尾不留麻烦。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "从九件小事里选出三件，组成我们班的公益小计划，再写一句为什么。",
        "posttest": "出现了排队、公物坏了、陌生人搭话，看看你能不能把今天的办法用上去。",
        "summary": "四句话：文明言行三件事、规则为了什么、热心人做什么、安全记心上。",
        "homework": "三层小任务，先做前两层，第三层可以请家里人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学道德与法治「法治启蒙」板块在三年级的空缺，正对统编教材三年级上册「公共生活靠大家」（公共场所，文明言行；我们都是热心人；生活离不开规则；安全记心上）。三年级学生每天都在公共场所里活动，但容易把「规则」理解成大人对自己的限制，也容易把「做好事」想成一件很大的事。所以全课先把文明言行落成三件看得见、做得到的具体行为——小声、排队、让一让，并把规则的意义讲清楚：规则不是来管我们的，是让每个人都能安心、都方便；其中「让座」特别说明它是愿意做的事，自己不方便时可以说明并帮着问一问，不做道德绑架。再把热心人做的事拉回到力所能及的范围：扶一下门、弯一下腰、交还失物、爱护公物、参与一次旧书捐赠，并强调公物坏了要报告大人而不是自己动手修。最后把安全要求讲透：不跟陌生人走、走散了站在原处或找穿制服的工作人员、不碰公共场所的电气设备、发现危险先离开再告诉大人。三个互动台子都能真操作：动手一是六件公共场所里的事，每件三个做法，选完立刻展开后果，反馈一律写成「这样可能会……，还可以试试……」；动手二是分类判断，把八条行为分进「公共生活里该做的／要调整的」两个筐；综合任务是从九件力所能及的小事里选出三件，点选与取消都即时生效，组成「我们班的公益小计划」。插图一律为中性简洁扁平插画，不使用真人照片风格，也不出现受伤、冲突画面。",
    "plan_table": """| 1 | cover | 公共生活靠大家 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 公共场所，文明言行 · 生活离不开规则 | 承·概念一（小声/排队/让一让 + 规则的意义） |
| 6 | interactive | 动手一：公共场所小管家，你会怎么做？ | 承·情境判断（六件事 × 三做法 → 展开后果） |
| 7 | concept | 我们都是热心人 · 安全记心上 | 承·概念二（公益小事 + 四条安全要求） |
| 8 | interactive | 动手二：公共生活里该做的 / 要调整的 | 承·分类判断（八条行为分两筐） |
| 9 | concept | 例题示范：小雨和同学的一次公园小行动 | 转·重难点突破（五步示范 + 易错点） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：我们班的公益小计划 | 合·迁移应用（九选三，可点可撤） |
| 12 | quiz | 后测：换几个新情境，办法还在不在 | 合·后测 |
| 13 | summary | 小结：四句话，讲清公共生活靠大家 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：公共场所文明言行 / 生活离不开规则 / 我们都是热心人 三栏\n- P5 公共场所文明言行概念图（已生成）：图书馆小声、公交站排队、车厢里让座，附中文标注\n- P7 热心人与公共安全情境图（已生成）：扶门、捡垃圾、交还失物、走散时找工作人员，附中文标注\n- 三张图均为中性简洁扁平教学插画，不使用真人照片风格，不含可识别的真实人物\n- 涉及安全与失物的内容以文字与图示表达，不出现冲突、受伤画面\n- 若需补充：社区或学校周边公共场所实景照片（需自行拍摄或授权后使用）",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
