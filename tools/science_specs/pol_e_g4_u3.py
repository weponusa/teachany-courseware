# -*- coding: utf-8 -*-
"""小学道德与法治 · 信息万花筒（四年级）—— 补齐知识树「生命安全与健康」空缺

学科语气（道德与法治）：情境案例驱动，情感共鸣 + 价值判断，全部用真实校园/家庭/社区场景；
结论落在「应该怎么做、为什么」，不做道德说教，不背法条、不堆标语。

内容落点（对应统编四上「信息万花筒」三课）：
  ① 健康看电视：媒介时间自己管——看电视的时间、距离和内容，心里有个数。
  ② 网络新世界：消息先核实再转发。转发前做「三查」——谁说的、什么时候说的、有没有证据；
     查到之前先不转，拿不准就问一句老师或爸爸妈妈。自己的照片、姓名、学校、住址、电话不随便发；
     要填手机号、填住址的链接先停下问一声。
  ③ 正确认识广告：广告是把东西介绍给可能想买的人，它想让我买东西，所以有三种常见说法——
     把好处说得很大、只说好的不说别的、催我马上做决定；听到就回三句问话。
  核心易错点：把「好心提醒大家」当成「转一转没关系」——错的消息转得越快，错得越远。

三个互动台子都能真操作：
  动手一 = 转发前的检查台（六条消息 → 点开看谁说的/什么时候说的/有没有证据 → 再决定转发还是先核实）；
  动手二 = 广告小侦探（四则广告 × 三种看法 → 展开后果）；
  综合任务 = 把八条消息和说法分进「可以信／先核实」两个筐。
课件内不出现任何真实平台品牌与商标，插图一律中性简洁扁平插画，不使用真人照片风格。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g4-u3"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "每天打开电视、翻一翻手机，信息就像万花筒一样转过来：有广告，有别人转来的消息，也有自己拍的照片。信息多不是坏事，可有三件事要先弄明白——广告为什么这样说，网上的消息要不要转发，自己的照片可以发给谁。这节课我们做三件事。第一件，看看广告是怎么说话的，我该怎样听。第二件，给别人转消息之前，先查三样东西。第三件，把消息分一分：哪些可以信，哪些先核实。带着这三个问题，我们开始。",
    "problem-anchor": "开始之前，先选一个你最想弄清楚的问题。是想知道广告为什么那样说，还是想知道网上的消息能不能转发；是想知道自己的照片可以发给谁，还是想知道看电视怎样才不累眼睛。选好以后，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出广告常见的几种说话方式，比如把好处说得很大、只说好的不说别的、用限时和便宜催我赶快做决定，并且知道听到以后先问自己三句话。第二，能说出转发消息之前要查的三样东西：谁说的、什么时候说的、有没有证据，查清楚之前先不转发。第三，知道自己的信息要保护：自己和家人的照片、姓名、学校、住址、电话不随便发；别人发来要填手机号的链接，先问一声爸爸妈妈。第四，知道看电视的时间、距离和内容，自己心里要有个安排。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不太合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先来说广告。广告在做的事，是把一件东西介绍给可能想买的人，这件事本身不奇怪。可广告是想让我买东西的，所以它有几种常用的说话方式。第一种，把好处说得很大：一瓶饮料说成一瓶顶三瓶牛奶，听着让人心动，却说不出是什么营养、有多少。第二种，只说好的，不说别的：一支笔说写出了好成绩，中间那些练习、老师、时间都不提。第三种，催我马上决定：限时一小时、前一百名、手慢就没有了，让人来不及想一想家里到底需不需要。听到这些话，我不用生气，也不用什么都不信，只要问自己三句：它有没有把话说清楚？它有没有什么没说？它是不是想让我赶快做决定？还有一件和看电视有关的事。看电视的时间、距离和内容，最好自己心里有个数：看到精彩的地方，也不妨隔一段时间站起来走走；屏幕亮、屋里暗的时候，眼睛离屏幕太近容易累，坐远一点、把灯打开会舒服很多。",
    "lab-1": "现在请你当一次转发前的检查员。这里有六条别人发来的消息。点开一条，你会看到三样东西：谁是发布的人、什么时候发的、有没有能验证的证据。看完以后再决定：是直接转发，还是先核实。这里没有扣分，选得不对会告诉你这样可能会怎么样，也会告诉你还可以试试什么。",
    "module-2": "再来说网络上的消息。一条消息从一个人手里转到另一个人手里，可能转了几十次，每一次都可能被改掉一点。所以给别人转发之前，先查三样东西，我把它叫做三查。第一查，谁说的：是学校、社区、正规媒体这样的正式来源，还是一个不知道是谁的账号。第二查，什么时候说的：有些消息讲的是两年前的事，今天再转出去就会让人误会。第三查，有没有证据：有没有照片、有没有正式的通知，还是只有一句听说。三样都清楚，转发可以放心一些；三样里有一两样说不清，就先别转，或者先问问老师、爸爸妈妈。还有一件和自己的信息有关的事：自己和家人的照片、姓名、学校、住址、电话，都不要随便发到网上，也不要随手放到公开的群里。别人发来一个链接，说要填手机号、填家庭住址才能领东西，先停下来，问问爸爸妈妈。这里有一个常见错误要提醒：有的同学误认为只要是好心提醒大家，转一转没关系——可如果这条消息本身是错的，转得越快，错得越远，好心也会变成麻烦。所以顺序永远是：先核实，再转发。",
    "lab-2": "接下来请你当一次广告小侦探。这里有四则广告的说法，每一则都有三种看它的方式。你选一种，看看这样想之后会发生什么。选完还能换一种再试，你会发现同一句广告，看的角度不一样，心里的判断也不一样。",
    "worked-example": "我们一起来看那个周末的晚上。第一步，先看清楚来的是什么：家里长辈在家庭群里转了一条消息，说某地的一种水果不能吃了，让大家别买，还写着请马上转发给家里人。第二步，三查。谁说的？消息里没写清楚，只说是一个朋友讲的。什么时候说的？消息最后的日期是两年前。有没有证据？没有。三样都说不清。第三步，先不转发，先去问一问。第二步还没完，小禾把消息读给妈妈听，妈妈在网上找到了当地正规媒体两年前的报道。原来这件事早就处理好了，当地也一直在做检测。第四步，把话说清楚。小禾没有直接说这条消息是假的，而是把找到的报道拿给长辈看，说这条消息是两年前的，现在的情况已经不一样了。第五步，告诉长辈一个好办法：以后看到这类消息，先看看是谁说的、什么时候说的、有没有证据，拿不准就问一句。这天晚上家里没有因为一条消息闹别扭，长辈还学会了三查。这里有一个常见错误要提醒：有的同学误认为消息不对，就要马上大声指出来——可对方往往是好意，把找到的证据拿出来，再一起看一看，比一句这是假的更容易让人接受。",
    "conceptest-1": "接下来用三个说法考考你，每个说法里都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件任务交给你。下面有八条消息和说法，请你判断一下：哪些可以信，放进这一边；哪些要先核实，放进那一边。放好以后，再读一读为什么。",
    "posttest": "最后一轮，换几条新的消息来考考你。这次会遇到限时优惠的广告、要填手机号的免费领取，还有同学发来的合影，看看你能不能用上今天的三查和三句问话。",
    "summary": "这节课我们记住四句话。第一句，广告是想让我买东西的，听到把好处说得很大、只说好的不说别的、催我马上决定，就先问自己：说清楚了吗、有没有没说、是不是要我赶快决定。第二句，转发之前三查：谁说的、什么时候说的、有没有证据；查不清就先不转，先问一问。第三句，自己和家人的照片、姓名、学校、住址、电话不随便发；要填个人信息的链接，先问爸爸妈妈。第四句，看电视的时间、距离和内容，自己心里有个安排。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出转发消息前的三查，各写一句话；再写出广告常见的一种说话方式，并举一个例子。第二层能力应用，动手做：这一周帮家里人看一条转来的消息，把三查的结果写下来，再说一说最后有没有转发。第三层迁移挑战，选做：和家里一起定一条我们家的消息约定，写清楚看到拿不准的消息时先做什么；再设计一张看电视的时间安排表。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 广告为什么这样说", "lab-1": "动手一 转发前的检查台",
    "module-2": "概念二 先核实再转发", "lab-2": "动手二 广告小侦探",
    "worked-example": "例题示范 长辈转来的那条消息", "conceptest-1": "概念测试",
    "synthesis": "综合任务 可以信 / 先核实", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：转发前的检查台（六条消息 × 三查 → 再决定转发还是先核实） ──
MSGS = [
    {"id": "m1", "t": "小区门口那家店明天要关门啦，全场五折，大家快来",
     "src": "小区群里一个没写清是谁的账号发的，只说「听朋友讲的」",
     "time": "今天上午",
     "ev": "没有店里的公告，也没有店门口的照片",
     "ok": False,
     "why": "这条消息的来源说不清、证据也没有，直接转发可能会让邻居白跑一趟，也可能让店里的人被问得莫名其妙。"
            "还可以试试：先看看这家店自己贴出的公告，或者打个电话问一句，再决定要不要转。"},
    {"id": "m2", "t": "今天下午有大暴雨，请家长提前到校接孩子",
     "src": "班主任老师在班级群里发的正式通知",
     "time": "今天中午，就在刚才",
     "ev": "通知里写清了时间、地点和怎么接",
     "ok": True,
     "why": "来源是老师，时间是刚才，内容也说得很清楚。这样的通知转给家里人，大家都放心。"},
    {"id": "m3", "t": "每天吃两个这种果子，感冒再也不会找你",
     "src": "一段短视频，发视频的账号自己写着在卖这种果子",
     "time": "前几天发的",
     "ev": "没有医生或者研究的信息，只有几个人说自己吃了有用",
     "ok": False,
     "why": "这条消息既想看我的钱包，也关系到身体，来源和证据都说不上。直接转发可能会让家里人多花钱，"
            "还可能耽误正经看病。还可以试试：先看看有没有正规医院或者医生的说法；身体不舒服，先问医生。"},
    {"id": "m4", "t": "这个视频里有人在电梯里晕倒了，请大家帮忙找人，快点转",
     "src": "一个不认识的网友发过来的",
     "time": "视频里写的时间是三年前",
     "ev": "视频里的地方和我们这儿对不上",
     "ok": False,
     "why": "这条消息的时间是三年前、地点也对不上。直接转发可能会让早就结束的事又被传一遍，还容易让人担心。"
            "还可以试试：先看清楚视频里的时间和地点；真有需要帮忙的事，学校和社区会正式通知。"},
    {"id": "m5", "t": "明天学校开运动会，请穿运动服、带上水杯",
     "src": "班主任老师在班级群里发的",
     "time": "今天下午",
     "ev": "写清了集合时间和地点",
     "ok": True,
     "why": "来源、时间、内容都清清楚楚。这样的消息转给爸爸妈妈，他们就知道该准备什么了。"},
    {"id": "m6", "t": "扫码就能免费领一套画笔，填一下手机号和家庭住址就行",
     "src": "一个陌生链接，不知道是谁发的",
     "time": "没有写",
     "ev": "只说要填手机号和住址，没说为什么要填",
     "ok": False,
     "why": "这条消息要的是我的个人信息。直接转发或者直接填写，可能会让家里的电话和住址被别人收走，"
            "之后收到很多打扰。还可以试试：想要画笔，和爸爸妈妈一起去正规文具店；"
            "遇到要填个人信息的链接，先停下来问一声。"},
]

# ── 动手二：广告小侦探（四则广告 × 三种看法） ──
ADS = [
    {"id": "a1", "t": "这款果味饮料，小朋友都爱喝，一瓶顶三瓶牛奶的营养！", "opts": [
        {"k": "a", "t": "「顶三瓶牛奶」这句话，我先问一句：是什么营养？有多少？", "ok": True,
         "fb": "你抓住了最要紧的那一句。说得越大的话，越需要问清楚。"},
        {"k": "b", "t": "既然能顶三瓶牛奶，那就让孩子多喝点，牛奶不用喝了", "ok": False,
         "fb": "这样可能会让孩子少喝了真正需要的牛奶。还可以试试：先看看瓶子上的成分表，再问一问它凭什么这么说。"},
        {"k": "c", "t": "广告都是骗人的，以后什么都不能买", "ok": False,
         "fb": "这样可能会让你把有用的信息也一起挡在门外。还可以试试：分开看——说得清楚的地方可以参考，"
               "说不清楚的地方先放一放。"},
    ]},
    {"id": "a2", "t": "限时一小时，前一百名下单立减，手慢就没有了！", "opts": [
        {"k": "a", "t": "「限时」是让我来不及多想，我先看看家里到底需不需要", "ok": True,
         "fb": "想得很稳。让人赶快决定，常常就是这句话最想做到的事。"},
        {"k": "b", "t": "这么便宜，赶紧下单，晚了就亏了", "ok": False,
         "fb": "这样可能会买回一堆用不上的东西。还可以试试：先把它放一放，过一晚再看，还想买再说。"},
        {"k": "c", "t": "这么便宜，多买几份分给同学", "ok": False,
         "fb": "这样可能会替别人花了钱，也可能让同学为难。还可以试试：先想清楚这笔钱是谁的，要不要先和家里商量。"},
    ]},
    {"id": "a3", "t": "小星学习桌，孩子用了都考上了好学校！", "opts": [
        {"k": "a", "t": "「都考上了」把成绩全算在一张桌子上，中间还有很多别的原因，这句话要打个问号", "ok": True,
         "fb": "你看得很准。一件事做得好，原因常常有好多个，广告只挑了其中一个。"},
        {"k": "b", "t": "买了就能考好，让爸爸妈妈赶紧买", "ok": False,
         "fb": "这样可能会让你和爸爸妈妈都误会了成绩是怎么来的。还可以试试：把桌子该有的样子列出来——"
               "高低合适、放得下书，再照这个去找。"},
        {"k": "c", "t": "广告里的孩子都考上了，那一定真有这么回事", "ok": False,
         "fb": "这样可能会把广告里的话当成自己亲眼看到的事。还可以试试：问一句这些例子是从哪里来的、有没有说清。"},
    ]},
    {"id": "a4", "t": "扫码填手机号，就能免费领一套画笔", "opts": [
        {"k": "a", "t": "先想想为什么要填手机号；个人信息不随便给，要不要填问一问爸爸妈妈", "ok": True,
         "fb": "这一步想得很对。免费的东西，往往要用别的东西来换。"},
        {"k": "b", "t": "免费的东西不要白不要，先填了再说", "ok": False,
         "fb": "这样可能会让家里的电话被收走，之后收到很多打扰。还可以试试：想领东西，先和家长一起看看"
               "这个链接是谁发的。"},
        {"k": "c", "t": "随便填一个假号码应付一下就行", "ok": False,
         "fb": "这样可能会让你养成随手填信息的习惯，不知道哪一天就填了真的。还可以试试：不想填就关掉它，"
               "这件事本来就该由你决定。"},
    ]},
]

# ── 综合任务：可以信 / 先核实（八条消息和说法分进两个筐） ──
SORT_ITEMS = [
    {"id": "k1", "t": "班主任在班级群里发的明天集合通知，写清了时间和地点", "bin": "trust",
     "why": "谁说的、什么时候说的、内容是什么，三样都清楚，可以放心。"},
    {"id": "k2", "t": "一段短视频说吃某种偏方可以治好病，发视频的人正在卖这种偏方", "bin": "check",
     "why": "这条消息想让我买东西，又说不出证据。先别照做，先问医生。"},
    {"id": "k3", "t": "当地正规媒体今天发的报道，写清了时间、地点和公布的检测结果", "bin": "trust",
     "why": "正式来源、最新时间、还能查到证据，这样的消息比较靠得住。"},
    {"id": "k4", "t": "有人在群里说某超市所有食品都不能吃了，却没说消息从哪里来", "bin": "check",
     "why": "只有一句听说，来源查不到。先别转，先去问一问、看一看正式通知。"},
    {"id": "k5", "t": "学校官方发布的天气提醒，讲了要注意什么和怎么安排", "bin": "trust",
     "why": "学校正式发布、内容具体，转给家里人正好用得上。"},
    {"id": "k6", "t": "不认识的账号发来免费领取链接，要填手机号和家庭住址", "bin": "check",
     "why": "它要的是我的个人信息。先停下，先和家长一起看看这是谁发的。"},
    {"id": "k7", "t": "消息里满是「听说」「据说」，却找不到是谁说的", "bin": "check",
     "why": "三查里第一查就过不去。找不到说的人，就先不转。"},
    {"id": "k8", "t": "社区贴在公告栏里的办事通知，落款写着社区的名字和日期", "bin": "trust",
     "why": "贴在看得见的地方、有署名有日期，这样的通知可以照着办。"},
]
SORT_BIN = {"trust": "可以信", "check": "先核实"}

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g4-u3 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 转发前的检查台：点消息 → 看三查（谁说的/什么时候说的/有没有证据）→ 决定转发还是先核实
   3) 广告小侦探：选广告 → 选一种看法 → 展开后果
   4) 可以信 / 先核实：八条消息和说法分进两个筐
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

  /* ---------- 2. 转发前的检查台 ---------- */
  var MSGS = __MSGS_JSON__;
  var stage1 = document.getElementById('gate-stage');
  if (stage1) {
    var curMsg = null, doneMsg = {};
    var out1 = document.getElementById('gate-out');
    var checkBox = document.getElementById('gate-checks');
    function msgById(id) {
      for (var i = 0; i < MSGS.length; i++) { if (MSGS[i].id === id) return MSGS[i]; }
      return null;
    }
    function render1() {
      document.querySelectorAll('[data-gate-msg]').forEach(function (b) {
        var k = b.dataset.gateMsg;
        b.classList.toggle('selected', k === curMsg);
        b.classList.toggle('correct', !!doneMsg[k]);
      });
      document.getElementById('gate-score').textContent =
        '已经查过 ' + Object.keys(doneMsg).length + ' / ' + MSGS.length + ' 条消息';
    }
    function makeRow(key, val) {
      var d = document.createElement('div');
      d.className = 'inner-card';
      var p = document.createElement('p');
      p.style.margin = '0';
      var s = document.createElement('strong');
      s.textContent = key + '：';
      p.appendChild(s);
      p.appendChild(document.createTextNode(val));
      d.appendChild(p);
      return d;
    }
    function paintChecks() {
      checkBox.innerHTML = '';
      if (!curMsg) {
        var tip = document.createElement('span');
        tip.style.color = 'var(--muted)';
        tip.style.fontSize = '14px';
        tip.textContent = '先在上面点一条消息，这里就会出现要查的三样东西。';
        checkBox.appendChild(tip);
        return;
      }
      var M = msgById(curMsg);
      checkBox.appendChild(makeRow('谁说的', M.src));
      checkBox.appendChild(makeRow('什么时候说的', M.time));
      checkBox.appendChild(makeRow('有没有证据', M.ev));
    }
    document.querySelectorAll('[data-gate-msg]').forEach(function (b) {
      b.addEventListener('click', function () {
        curMsg = b.dataset.gateMsg;
        if (doneMsg[curMsg]) {
          out1.className = 'result';
          out1.innerHTML = '<strong>这条消息已经查过啦。</strong>你看看下面这三样，再换一条试试。';
        } else {
          out1.className = 'result warn';
          out1.innerHTML = '<strong>你要看的是这一条：</strong>' + b.textContent +
            '<br>先看下面查到的三样，再决定怎么办。';
        }
        render1();
        paintChecks();
      });
    });
    document.querySelectorAll('[data-gate-act]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!curMsg) {
          out1.className = 'result warn';
          out1.textContent = '先在上面点一条消息，再来决定。';
          return;
        }
        var M = msgById(curMsg);
        var act = b.dataset.gateAct;
        var want = M.ok ? 'forward' : 'verify';
        if (act === want) {
          doneMsg[M.id] = true;
          out1.className = 'result';
          out1.innerHTML = '<strong>这一步做得好。</strong>' + M.why;
        } else {
          out1.className = 'result warn';
          out1.innerHTML = '<strong>这样可能会有点着急了。</strong>' + M.why;
        }
        render1();
        paintChecks();
      });
    });
    render1();
    paintChecks();
  }

  /* ---------- 3. 广告小侦探 ---------- */
  var ADS = __ADS_JSON__;
  var stage2 = document.getElementById('ad-stage');
  if (stage2) {
    var curAd = null, doneAd = {};
    var out2 = document.getElementById('ad-out');
    function adById(id) {
      for (var i = 0; i < ADS.length; i++) { if (ADS[i].id === id) return ADS[i]; }
      return null;
    }
    function render2() {
      document.querySelectorAll('[data-ad]').forEach(function (b) {
        var k = b.dataset.ad;
        b.classList.toggle('selected', k === curAd);
        b.classList.toggle('correct', !!doneAd[k]);
      });
      document.getElementById('ad-score').textContent =
        '已经看明白 ' + Object.keys(doneAd).length + ' / ' + ADS.length + ' 则广告';
    }
    function paintOpts() {
      var box = document.getElementById('ad-opts');
      box.innerHTML = '';
      if (!curAd) return;
      var A = adById(curAd);
      if (!A) return;
      A.opts.forEach(function (o) {
        var b = document.createElement('button');
        b.className = 'choice' + (doneAd[curAd] && o.ok ? ' correct' : '');
        b.style.textAlign = 'left';
        b.textContent = o.t;
        b.addEventListener('click', function () {
          if (doneAd[curAd]) return;
          if (o.ok) {
            doneAd[curAd] = true;
            out2.className = 'result';
            out2.innerHTML = '<strong>这样看挺清楚。</strong>' + o.fb;
          } else {
            out2.className = 'result warn';
            out2.innerHTML = '<strong>这样想可能会出点偏差。</strong>' + o.fb;
          }
          render2();
          paintOpts();
        });
        box.appendChild(b);
      });
    }
    document.querySelectorAll('[data-ad]').forEach(function (b) {
      b.addEventListener('click', function () {
        curAd = b.dataset.ad;
        var A = adById(curAd);
        if (doneAd[curAd]) {
          out2.className = 'result';
          out2.innerHTML = '<strong>这则广告已经看明白了。</strong>你上次选的看法挺合适，换一则再试试。';
        } else {
          out2.className = 'result warn';
          out2.innerHTML = '<strong>广告是这么说的：' + A.t + '</strong><br>下面有三种看它的方式，你选一种，' +
            '再想想这样看会怎么样。';
        }
        render2();
        paintOpts();
      });
    });
    render2();
  }

  /* ---------- 4. 可以信 / 先核实 ---------- */
  var ITEMS = __SORT_JSON__;
  var BINN = __SORTBIN_JSON__;
  var stage3 = document.getElementById('bin-stage');
  if (stage3) {
    var pickItem = null, placed = {};
    var out3 = document.getElementById('bin-out');
    function render3() {
      document.querySelectorAll('[data-bin-item]').forEach(function (b) {
        var k = b.dataset.binItem;
        b.classList.toggle('selected', k === pickItem);
        b.classList.toggle('done', !!placed[k]);
        b.disabled = !!placed[k];
      });
      document.getElementById('bin-score').textContent =
        '已经放好 ' + Object.keys(placed).length + ' / ' + ITEMS.length + ' 条';
      var a = document.getElementById('bin-box-a');
      var b2 = document.getElementById('bin-box-b');
      a.innerHTML = ''; b2.innerHTML = '';
      ITEMS.forEach(function (it) {
        if (!placed[it.id]) return;
        var s = document.createElement('div');
        s.className = 'tag';
        s.textContent = it.t;
        (it.bin === 'trust' ? a : b2).appendChild(s);
      });
      if (!a.innerHTML) a.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
      if (!b2.innerHTML) b2.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有放进来。</span>';
    }
    document.querySelectorAll('[data-bin-item]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (placed[b.dataset.binItem]) return;
        pickItem = b.dataset.binItem;
        out3.className = 'result warn';
        out3.innerHTML = '<strong>你选的是：' + b.textContent + '</strong><br>三查过了吗？它应该进哪一个筐？';
        render3();
      });
    });
    document.querySelectorAll('[data-bin-box]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pickItem) {
          out3.className = 'result warn';
          out3.textContent = '先在上面点一条消息，再选筐。';
          return;
        }
        var it = null;
        for (var i = 0; i < ITEMS.length; i++) { if (ITEMS[i].id === pickItem) it = ITEMS[i]; }
        if (b.dataset.binBox === it.bin) {
          placed[it.id] = true;
          out3.className = 'result';
          out3.innerHTML = '<strong>放对了，它属于「' + BINN[it.bin] + '」。</strong>' + it.why;
          pickItem = null;
          if (Object.keys(placed).length === ITEMS.length) {
            out3.className = 'result';
            out3.innerHTML = '<strong>八条全放对了！</strong>记住这句口诀：<strong>谁说的、什么时候说的、' +
              '有没有证据——三样清楚再转发。</strong>';
          }
        } else {
          out3.className = 'result warn';
          out3.innerHTML = '<strong>再想一想这一条。</strong>' + it.why +
            '<br><span style="color:var(--muted)">常见错误：容易把「这条消息听起来很有道理」误认为' +
            '「这条消息可以信」——把三查摆出来对一对，答案就清楚了。</span>';
        }
        render3();
      });
    });
    render3();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__MSGS_JSON__', json.dumps(MSGS, ensure_ascii=False))
             .replace('__ADS_JSON__', json.dumps(ADS, ensure_ascii=False))
             .replace('__SORT_JSON__', json.dumps(SORT_ITEMS, ensure_ascii=False))
             .replace('__SORTBIN_JSON__', json.dumps(SORT_BIN, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "家里长辈在群里转来一条消息，说某地的一种水果不能吃了。要判断能不能信，下面哪种做法更好？",
         "options": [("先查：谁说的、什么时候说的、有没有证据，查不清就先不转", True),
                     ("看起来很有道理，先转给家里人再说", False),
                     ("反正不是我写的，随手一转没关系", False)],
         "explain": "三查是转发前最省事的一步：谁说的、什么时候说的、有没有证据。"
                    "<strong>错因提醒：</strong>常见错误是误认为「好心提醒大家，转一转没关系」——"
                    "如果这条消息本身是错的，转得越快，错得越远。"},
        {"q": "一则广告写着「限时一小时，前一百名下单立减，手慢就没有了」。看到这句话，下面哪种想法更合适？",
         "options": [("它是想让我赶快做决定，我先看看家里到底需不需要", True),
                     ("这么便宜，赶紧下单，晚了就亏了", False),
                     ("广告都是假的，以后什么都不能买", False)],
         "explain": "「限时」最想做到的事，就是让人来不及多想；先放一放，答案自己会清楚。"
                    "<strong>错因提醒：</strong>有的同学把「它一直催我」搞混成「它一定很划算」——"
                    "催得越急，越要先停一下。"},
        {"q": "下面哪一样东西，最好不要随便发到网上或者公开的群里？",
         "options": [("自己家的住址、学校全名和家人的手机号", True),
                     ("在公园里拍的一片树叶", False),
                     ("一张画好的手抄报", False)],
         "explain": "住址、学校全名和家人的电话连在一起，就能让人找到你家和你家人。"
                    "<strong>错因提醒：</strong>容易把「发出去别人不一定看」误认为「发出去没关系」——"
                    "信息发出去就收不回来了，先想一想再发。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "广告为什么这样说：它想让我买东西，我该怎样听", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们每天都在看信息：电视里、手机上、路边的广告牌上（And）；信息多不是坏事，可有些话是别人为了让我买东西、让我赶快转发才那么说的（But）；所以这节课先学会听懂广告的三种说话方式，再学会转发前的三查（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">广告在做的事，是把一件东西介绍给可能想买的人。可它是想让我买东西的，所以说话有讲究。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>把好处说得很大：</strong>一句「一瓶顶三瓶牛奶」，听着心动，却说不出是什么营养、有多少。</div></div>
          <div class="step"><span class="n">2</span><div><strong>只说好的，不说别的：</strong>说一支笔写出了好成绩，中间的练习、老师、时间都不提。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>催我马上决定：</strong>限时一小时、前一百名、手慢就没有了，让我来不及想一想。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="听广告的三句问话与看电视健康提示概念图：说清楚了吗、有没有没说、是不是要我赶快决定，附中文标注">
          <figcaption>概念图：听广告的三句问话 · 看电视的时间、距离和内容（教学示意图，中性简洁扁平插画）</figcaption>
        </figure>
        <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(78,205,196,.45)">
          <p><strong>听到这些话，我可以问自己三句</strong></p>
          <p style="color:var(--muted)">它有没有把话说清楚？它有没有什么没说？它是不是想让我赶快做决定？</p>
        </div>
        <div class="inner-card">
          <p><strong>看电视这件事，也归自己管</strong></p>
          <p style="color:var(--muted)">时间上心里有个数，隔一段站起来走走；坐远一点、把屋里灯打开，眼睛舒服很多；内容也挑一挑，看完能说出看了什么，就不算白白花掉这段时间。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「广告都在骗人，所以什么都不用听」。可广告里也有有用的信息，比如东西是做什么用的、多大、多少钱。<strong>学会分开看：说得清楚的地方可以参考，说不清楚的地方先放一放。</strong></p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "同一句「限时一小时」，可以听成「再不买就亏了」，也可以听成「它想让我赶快决定」。听成哪一种，你接下来做的事会很不一样。"},
    {"lens": "解释它", "text": "为什么问一句「有没有什么没说」就这么有用？因为广告只讲它想让我看见的那一面，另一面得我自己去找。"},
    {"lens": "迁移它", "text": "这套问话在看电视、看短视频、看街边广告牌时都用得上：不是不听，而是听完自己再想一想。"},
])}
    ''', tag="概念一"))

    msg_btns = "\n".join(
        f'            <button class="choice" data-gate-msg="{m["id"]}" style="text-align:left">{m["t"]}</button>'
        for m in MSGS
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：转发前的检查台，这条消息要转吗？", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">你现在是转发前的检查员。先点开一条消息，看清楚<strong>谁说的、什么时候说的、有没有证据</strong>，再决定怎么办。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 别人发来的这条消息</div>
          <div class="grid" id="gate-stage">
{msg_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 三查：点开看这三样</div>
          <div class="grid" id="gate-checks">
            <span style="color:var(--muted);font-size:14px">先在上面点一条消息。</span>
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">③ 我的决定</div>
          <div class="grid grid-2">
            <button class="choice" data-gate-act="forward" style="text-align:center">直接转发</button>
            <button class="choice" data-gate-act="verify" style="text-align:center">先核实，不转发</button>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">查过几条</span><span class="v" id="gate-score">已经查过 0 / 6 条消息</span></div>
          </div>
          <p class="result warn" id="gate-out" style="margin-top:12px">先点开一条消息看看。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💛</span><div><strong>说给你听：</strong>这里没有扣分。有的消息看起来很像真的，可是时间或来源对不上；有的消息看着平平常常，其实来源和证据都清楚。拿不准的时候，问一句老师或者爸爸妈妈最合适。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "先核实再转发：三查之后，再谈转发", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">一条消息从一个人手里转到另一个人手里，可能转了几十次，每一次都可能被改掉一点。所以转发之前，先做<strong>三查</strong>。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>谁说的：</strong>是学校、社区、正规媒体这样的正式来源，还是一个不知道是谁的账号。</div></div>
          <div class="step"><span class="n">2</span><div><strong>什么时候说的：</strong>有些消息讲的是两年前的事，今天再转出去就会让人误会。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>有没有证据：</strong>有没有照片、有没有正式的通知，还是只有一句听说。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="转发前三查与个人信息保护概念图：谁说的、什么时候说的、有没有证据，以及不随便发照片住址电话，附中文标注">
          <figcaption>概念图：转发前的三查 · 自己的信息不随便发（教学示意图，中性简洁扁平插画）</figcaption>
        </figure>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>三样都清楚，可以放心一些</strong></p>
          <p style="color:var(--muted)">三样里有一两样说不清，就先别转。不是不关心别人，而是先把事情弄清楚，转出去的话才真的帮得上忙。</p>
        </div>
        <div class="inner-card">
          <p><strong>自己的信息，也要看住</strong></p>
          <p style="color:var(--muted)">自己和家人的照片、姓名、学校、住址、电话，不随便发到网上，也不随手放进公开的群里。有人发来链接要填手机号、填住址才给东西，先停下来，问一声爸爸妈妈。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「只要是好心提醒大家，转一转没关系」。可如果这条消息本身是错的，转得越快，错得越远，好心也会变成麻烦。<strong>顺序永远是：先核实，再转发。</strong></p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "「我先转过去，反正不是我写的」和「我先查一查，再决定转不转」，中间差着一步。差这一步，别人收到的可能是帮忙，也可能是麻烦。"},
    {"lens": "比较它", "text": "同样是提醒大家注意，一种是学校正式发的通知，一种是听说来的消息。两种都出于好意，可只有前一种，大家照着做不会出错。"},
    {"lens": "迁移它", "text": "三查不只用在家里：同学之间传来传去的消息、作业要求、活动时间，也都可以这样对一对，少跑很多冤枉路。"},
])}
    ''', tag="概念二"))

    ad_btns = "\n".join(
        f'            <button class="choice" data-ad="{a["id"]}" style="text-align:left">广告：{a["t"]}</button>'
        for a in ADS
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：广告小侦探，同一句话可以有三种看法", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">你是广告小侦探。先选一则广告，再从三种看它的方式里选一种，看看这样想之后会怎么样。选完可以换一种再试。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 这则广告是这么说的</div>
          <div class="grid" id="ad-stage">
{ad_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 我可以怎么看它</div>
          <div class="grid" id="ad-opts">
            <span style="color:var(--muted);font-size:14px">先在上面选一则广告，这里就会出现三种看法。</span>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">看明白几则</span><span class="v" id="ad-score">已经看明白 0 / 4 则广告</span></div>
          </div>
          <p class="result warn" id="ad-out" style="margin-top:12px">先在上面选一则广告。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔎</span><div><strong>想一想：</strong>三种看法里，哪一种会让你和家人少花冤枉钱、也少错过真有用的东西？广告可以听，但最后做决定的是我自己。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：长辈转来的那条消息", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>周末晚上，家里长辈在群里转了一条消息，说某地的一种水果不能吃了，让大家别买，还写着请马上转发给家里人。这条消息，该怎么看？</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先看清楚来的是什么：</strong>一条转来的消息，末尾写着请马上转发。</div></div>
          <div class="step"><span class="n">2</span><div><strong>三查：</strong>谁说的——没写清楚，只说是一个朋友讲的；什么时候说的——日期是两年前；有没有证据——没有。三样都说不清。</div></div>
          <div class="step"><span class="n">3</span><div><strong>先不转发，先去问一问：</strong>把消息读给妈妈听，妈妈找到了当地正规媒体两年前的报道。原来这件事早就处理好了。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>把话说清楚：</strong>不说「这是假的」，而是把找到的报道拿给长辈看，说这条是两年前的，现在情况已经不一样了。</div></div>
        </div>
        <div class="inner-card">
          <p><strong>第五步：留下一个好办法</strong></p>
          <p style="color:var(--muted)">告诉长辈，以后看到这类消息，先看看是谁说的、什么时候说的、有没有证据，拿不准就问一句。这天晚上家里没有为一条消息闹别扭，长辈还学会了三查。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>消息不对，就要马上大声指出来。可对方往往是好意——<strong>把找到的证据拿出来，再一起看一看，比一句「这是假的」更容易让人接受。</strong></p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "关于转发别人发来的消息，下面哪句话说得对？",
         "options": [("先查谁说的、什么时候说的、有没有证据，查清楚了再决定转不转", True),
                     ("只要是好心提醒大家，转一转没关系", False),
                     ("消息看着很有道理，就可以放心转出去", False)],
         "explain": "三查过了再转发，转出去的才真的帮得上忙。"
                    "<strong>错因提醒：</strong>常见错误是误认为「读起来有道理就是真的」——"
                    "有些错消息写得很像回事，只有来源和时间能说明问题。"},
        {"q": "一则广告说「孩子用了都考上了好学校」。下面哪种看法更合适？",
         "options": [("成绩的原因有很多个，广告只挑了其中一个，这句话要打个问号", True),
                     ("广告里的孩子都考上了，说明桌子真有用", False),
                     ("广告都在骗人，以后什么都不用听", False)],
         "explain": "一件事做得好，原因常常有好多个；广告只讲它想让我看见的那一面。"
                    "<strong>错因提醒：</strong>有的同学把「说出了一半」搞混成「说出了全部」——"
                    "听到很大的结论，先问一句它凭什么这么说。"},
        {"q": "有一个链接写着「填手机号，免费领一套画笔」。下面哪种做法更好？",
         "options": [("先想想为什么要填手机号，要不要填问一问爸爸妈妈", True),
                     ("免费的东西不要白不要，先填了再说", False),
                     ("随便填一个假号码应付一下", False)],
         "explain": "手机号和住址连在一起，就能让人找到你家和你家人；填之前先问一声最稳妥。"
                    "<strong>错因提醒：</strong>容易把「填个号码没什么」误认为「填了也不会怎样」——"
                    "信息发出去就收不回来了。"}
    ], tag="概念测试"))

    item_btns = "\n".join(
        f'            <button class="sort-item" data-bin-item="{it["id"]}">{it["t"]}</button>' for it in SORT_ITEMS
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：可以信 / 先核实，把消息分进两个筐", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一条消息或说法，再点它应该进的筐：<strong>可以信</strong>放一边，<strong>先核实</strong>放另一边。</p>
        <div class="lab-panel">
          <div class="sort-bank" id="bin-stage">
{item_btns}
          </div>
          <div class="grid grid-2" style="margin-top:14px">
            <button class="choice" data-bin-box="trust" style="text-align:center">可以信</button>
            <button class="choice" data-bin-box="check" style="text-align:center">先核实</button>
          </div>
          <div class="sort-bins">
            <div class="sort-bin" id="bin-box-a"><h4>可以信</h4></div>
            <div class="sort-bin" id="bin-box-b"><h4>先核实</h4></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">分类进度</span><span class="v" id="bin-score">已经放好 0 / 8 条</span></div>
          </div>
          <p class="result warn" id="bin-out" style="margin-top:12px">先在上面点一条消息。</p>
        </div>
        <div class="inner-card">
          <p><strong>分完之后，想一想：</strong></p>
          <p style="color:var(--muted)">下次家里人转来一条拿不准的消息，你打算先说哪一句？写在下面。</p>
          <textarea id="syn-answer" rows="3" placeholder="我会先说……，因为……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几条新消息，办法还在不在", TTS["posttest"], [
        {"q": "同学在群里发了一张你们的合影，下面哪种做法更好？",
         "options": [("先问问照片里的同学愿不愿意，再决定要不要往外发", True),
                     ("照片挺好看的，先发出去再说", False),
                     ("只发到自己的家庭群里，肯定没关系", False)],
         "explain": "照片里有别人，先问一句最稳妥；同意之后再发，谁都不会为难。"
                    "<strong>错因提醒：</strong>常见错误是误认为「只发到小群里就不算公开」——"
                    "照片一旦发出，就可能被再转出去。"},
        {"q": "一条消息说某地明天要停水，落款写着当地供水部门的正式通知，时间是今天上午。下面哪种做法更好？",
         "options": [("来源是正式部门、时间是今天、内容也写清了，可以转给家里人", True),
                     ("不管什么消息，先别转最安全", False),
                     ("把通知改成自己说的话，再转出去", False)],
         "explain": "三查都过得去，这样的消息转给家里人正好用得上。"
                    "<strong>错因提醒：</strong>有的同学把「谨慎」搞混成「什么都不转」——"
                    "三查是为了转得准，不是为了什么都不做。"},
        {"q": "你正在看一个很精彩的节目，已经看了一个多小时。下面哪种做法更好？",
         "options": [("先站起来走一走、看看远处，再想想今天的作业和睡觉时间怎么安排", True),
                     ("一直看到结束，中间不休息", False),
                     ("把屏幕凑近一点，看得更清楚", False)],
         "explain": "时间、距离和内容都由自己心里有个数，才叫真的会看。"
                    "<strong>错因提醒：</strong>容易把「看得很入迷」误认为「这样看没问题」——"
                    "眼睛累了、时间没了，都是要自己留意的信号。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：四句话，讲清信息怎么看", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>广告怎么听：</strong>它想让我买东西，所以会说得很大、只说好的、催我赶快决定；先问三句。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>转发前三查：</strong>谁说的、什么时候说的、有没有证据；查不清就先不转，先问一问。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>信息看住：</strong>自己和家人的照片、姓名、学校、住址、电话不随便发；要填个人信息的链接先问一声。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>看电视自己管：</strong>时间、距离、内容心里有数，隔一段起身走一走。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>一句口诀：</strong>说清楚了吗、有没有没说、是不是催我赶快决定；谁说的、什么时候说的、有没有证据。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「三查」和「三句问话」这两个说法，给家里人讲一条你最近看到的消息。</p>
          <p style="color:var(--muted)">再动一动手：<strong>写一写</strong>你家里最常转发消息的人是谁，你打算怎样把三查讲给他听。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写出转发消息前的三查，各写一句话。",
            "写出广告常见的一种说话方式，并举一个例子。",
            "写出三样最好不要随便发到网上的信息。",
        ],
        [
            "这一周帮家里人看一条转来的消息：把三查的结果写下来，再说一说最后有没有转发。",
            "给自己定一张看电视的时间安排表，写清楚每天看多久、什么时候看、中间怎么休息，请家里人签个字。",
        ],
        [
            "和家里一起定一条我们家的消息约定：写清楚看到拿不准的消息时先做什么、谁来核实、核实之后再怎么办。",
            "挑一则你最近看到的广告，把它的三种说话方式里用到的那些找出来，写一句你自己的提醒送给自己。",
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
    "title": "信息万花筒",
    "name_en": "A Kaleidoscope of Information",
    "grade": 4,
    "grade_cn": "四年级",
    "domain": "health-safety",
    "domain_cn": "生命安全与健康",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学四年级的道德与法治课：从每天都会遇到的信息场景出发，讲清三件事。一是「广告为什么这样说」——广告是把东西介绍给可能想买的人，它想让我买东西，所以有把好处说得很大、只说好的不说别的、催我马上做决定这三种常见说法，听到就问自己三句话：说清楚了吗、有没有没说、是不是要我赶快决定；同时把媒介时间自己管起来，看电视的时间、距离和内容心里有个数。二是「先核实再转发」——转发前做三查：谁说的、什么时候说的、有没有证据；三样清楚再转，查不清就先别转、先问一句，并把好心转发反而传错消息这个常见误解讲透。三是「自己的信息看住」——自己和家人的照片、姓名、学校、住址、电话不随便发，要填手机号填住址的链接先问爸爸妈妈。三个互动台子都能真操作：动手一是转发前的检查台（六条消息点开看三查，再决定转发还是先核实）、动手二是广告小侦探（四则广告 × 三种看法，展开后果）、综合任务是把八条消息和说法分进「可以信／先核实」两个筐。全课不出现任何真实平台品牌与商标，以真实家庭与校园情境为主，反馈一律写成「这样可能会……，还可以试试……」。",
    "tags": ["信息万花筒", "健康看电视", "网络新世界", "正确认识广告", "媒介素养", "先核实再转发", "个人信息保护", "四年级", "生命安全与健康"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学「生命安全与健康」——感受媒介信息对生活的影响，学会分辨与选择，保护好自己的信息安全；对应统编《道德与法治》四年级上册「信息万花筒」：健康看电视、网络新世界、正确认识广告。",
    "hero_question": "每天涌到眼前的信息，哪一些可以信？哪一些要先核实？",
    "hero_alt": "信息万花筒知识结构图：广告怎么听、消息三查再转发、个人信息不随便发 三栏",
    "hero_caption": "信息万花筒：广告怎么听 · 消息三查再转发 · 自己的信息看住（谁说的、什么时候说的、有没有证据）",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "广告为什么那样说？", "d": "说得很大、只说好的、催我赶快决定", "v": "广告为什么那样说"},
        {"t": "别人发来的消息，要不要转发？", "d": "三查：谁说的、什么时候说的、有没有证据", "v": "别人发来的消息要不要转发"},
        {"t": "我的照片和信息，可以发给谁？", "d": "照片、姓名、学校、住址、电话", "v": "我的照片和信息可以发给谁"},
        {"t": "看电视怎样才不累眼睛？", "d": "时间、距离、内容自己管", "v": "看电视怎样才不累眼睛"},
    ],
    "objectives": [
        "能说出广告常见的三种说话方式（把好处说得很大、只说好的不说别的、催我马上做决定），并会用三句问话去听",
        "能说出转发消息前的三查（谁说的、什么时候说的、有没有证据），并知道查不清就先不转、先问一句",
        "知道自己和家人的照片、姓名、学校、住址、电话不随便发，遇到要填个人信息的链接先问一声",
        "知道看电视的时间、距离和内容要自己心里有个安排",
    ],
    "objectives_plain": [
        "能说出广告常见的说法，听到以后先问自己三句话",
        "能说出转发前的三查，查不清就先不转",
        "知道自己和家人的信息不随便发，要填个人信息的链接先问一声",
        "知道看电视的时间、距离、内容自己要有安排",
    ],
    "standards": [
        {"content": "感受媒介信息对生活的影响，学会分辨与选择，保护好自己的信息安全。",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学 生命安全与健康"},
        {"content": "健康看电视；网络新世界；正确认识广告",
         "source": "统编《道德与法治》四年级上册「信息万花筒」"},
    ],
    "prereqs": ["pol-e-g4-u2"],
    "prereqs_name": "为父母分担",
    "prereqs_meta": "pol-e-g4-u2",
    "leads_to": ["pol-e-g4-u4"],
    "next_meta": "pol-e-g4-u4",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "信息多不是坏事。这节课弄清楚三件事：广告怎么听、消息怎么转、自己的信息怎么守住。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能把一条拿不准的消息查清楚，再决定转不转。",
        "objectives": "看清四件事：广告的三种说话方式、转发前的三查、个人信息要保护、看电视自己管。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "广告是想让我买东西的：说得很大、只说好的、催我赶快决定，听到先问三句。",
        "lab-1": "六条消息，点开先看谁说的、什么时候说的、有没有证据，再决定转发还是先核实。",
        "module-2": "转发前先做三查；自己的照片、姓名、学校、住址、电话不随便发。",
        "lab-2": "你是广告小侦探：同一句广告，看的角度不一样，判断也不一样。",
        "worked-example": "长辈转来的那条消息，五步走完：看清楚、三查、先问一问、把话说清楚、留下好办法。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "把八条消息和说法分进「可以信」和「先核实」两个筐，分完读一读为什么。",
        "posttest": "出现了同学发来的合影、正式部门发的停水通知、看了一个多小时的节目，看看办法还在不在。",
        "summary": "四句话：广告怎么听、转发前三查、信息看住、看电视自己管。",
        "homework": "三层小任务，先做前两层；第二层要请家里人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学道德与法治「生命安全与健康」板块在四年级的空缺，正对统编教材四年级上册「信息万花筒」（健康看电视、网络新世界、正确认识广告）。四年级学生已经每天在接触电视、手机和家人转来的消息，但分辨能力还没跟上：很容易把「读起来有道理」当成「可以信」，把「好心提醒大家」当成「转一转没关系」，也很少意识到自己和家人的照片、住址、电话连在一起意味着什么。所以全课不背条文、不讲大道理，全部落在学生真实会遇到的场景上，把判断拆成能操作的步骤。第一层是「广告为什么这样说」：先说明白广告在做什么——把东西介绍给可能想买的人；再点出它是要让我买东西的，因此有把好处说得很大、只说好的不说别的、催我马上决定这三种常见说法；最后给出三句可以随身带走的问话：说清楚了吗、有没有没说、是不是要我赶快决定。同时把媒介时间自己管起来，讲清看电视的时间、距离和内容。第二层是「先核实再转发」：把判断拆成可执行的三查——谁说的、什么时候说的、有没有证据；三样清楚再转，查不清就先别转、先问一句老师或爸爸妈妈。第三层是「自己的信息看住」：照片、姓名、学校、住址、电话不随便发，要填手机号、填住址的链接先停下来问一声。课件专门处理两个常见误解：一是「读起来有道理就等于可信」，二是「好心转发就没关系」，并在例题里补上怎么把证据拿给长辈看、把话说清楚。三个互动台子都能真操作：动手一是转发前的检查台，六条消息点开后先看三查，再决定直接转发还是先核实，反馈一律写成「这样可能会……，还可以试试……」；动手二是广告小侦探，四则广告各配三种看法，选完立刻展开后果；综合任务是分类判断，把八条消息和说法分进「可以信／先核实」两个筐。全课不出现任何真实平台品牌与商标，插图一律为中性简洁扁平插画，不使用真人照片风格。",
    "plan_table": """| 1 | cover | 信息万花筒 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 广告为什么这样说：它想让我买东西，我该怎样听 | 承·概念一（正确认识广告 + 媒介时间） |
| 6 | interactive | 动手一：转发前的检查台，这条消息要转吗？ | 承·核心模拟（点开三查 → 再决定） |
| 7 | concept | 先核实再转发：三查之后，再谈转发 | 承·概念二（三查 + 个人信息保护） |
| 8 | interactive | 动手二：广告小侦探，同一句话可以有三种看法 | 承·情境判断（四则广告 × 三种看法） |
| 9 | concept | 例题示范：长辈转来的那条消息 | 转·重难点突破（五步示范 + 易错点） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：可以信 / 先核实，把消息分进两个筐 | 合·迁移应用（分类判断） |
| 12 | quiz | 后测：换几条新消息，办法还在不在 | 合·后测 |
| 13 | summary | 小结：四句话，讲清信息怎么看 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：广告怎么听 / 消息三查再转发 / 自己的信息看住 三栏\n- P5 听广告的三句问话与看电视健康提示概念图（已生成）：附中文标注\n- P7 转发前三查与个人信息保护概念图（已生成）：附中文标注\n- 三张图均为中性简洁扁平教学插画，不使用真人照片风格，不含可识别的真实人物\n- 课件全文不出现任何真实平台品牌与商标，消息情境均为虚构的通用场景\n- 涉及网络风险（陌生链接、个人信息泄露）仅以文字与情境选择表达，不出现危险或受惊画面\n- 若需补充：本班学生常见的媒介使用时间统计（需家长知情同意后收集），不在课件中呈现任何学生个人信息",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
