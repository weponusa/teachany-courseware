# -*- coding: utf-8 -*-
"""小学道德与法治 · 在集体中长大（G3）—— 补齐知识树「生命安全与健康」空缺

学科语气（道德与法治）：情境案例驱动，情感共鸣 + 价值判断；结论落在「应该怎么做、为什么」，
不做道德说教，也不做法条背诵。三年级要落成能看见、能做到的具体行为。

内容落点（对应统编三上「在集体中长大」三课）：
  ① 走近我们的引路人：老师、父母和身边带我们的人，教给我们的不只是书本上的事
     （守时、诚实、把话说清楚、不放弃、有礼貌），这些做人做事的道理是祖辈传下来的，
     我们今天在班级里继续把它做出来 —— 呼应课标「感受中华优秀传统文化魅力」。
  ② 同学相伴：一起学、一起玩、有商有量；有矛盾先把话说完；看到同学有困难先问一句
     「要不要帮忙」；在集体里互相照应也是安全与健康的一部分。
  ③ 让我们的学校更美好：集体的事人人有份，三年级能做的小事一大把。

三个互动台子都能真操作：
  动手一 = 情境卡选做法 → 展开后果（六件事 × 三个做法，反馈「这样可能会……，还可以试试……」）；
  动手二 = 小组任务分工模拟（选任务 → 选分工方案 → 展开后果）；
  综合任务 = 把八条行为分进「在集体里该做的 / 要调整的」两个筐。
插图一律中性简洁扁平插画，不使用真人照片风格。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g3-u3"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "在班级里待了一天，你可能会想：谁在带我们长大？是每天站在讲台上的老师，是家里的爸爸妈妈，也是操场上、走廊里那些提醒过我们一句话的人。可是他们教的，真的只是书本上的知识吗？这节课我们做三件事：先走近我们的引路人，看看他们到底带给我们什么；再聊一聊同学相伴，看看怎样和身边的同学相处得更好；最后想一想，我能为班级和学校做一件什么小事。带着这三个问题，我们开始。",
    "problem-anchor": "开始之前，先选一个你最想弄清楚的问题。是想知道身边的引路人是谁，还是想知道同学之间怎样才能相伴得更好；是想知道自己能为集体做点什么，还是想知道在集体里有了矛盾该怎么办。选好以后，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出身边的引路人是谁，他们教给我们的做人做事的道理是什么。第二，能说出和同学相伴的两三条具体做法，比如一起商量、把话说完、看到同学有困难先问一句。第三，能说出自己能为班级和学校做的一件具体小事，并且愿意去做。第四，知道在集体里也要注意安全：上下楼梯不推挤，看到危险先告诉老师，自己不舒服或者遇到麻烦要说出来。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先来认识身边的引路人。引路人，就是那些带我们往前走的人。老师上课时讲的是一道题怎么算，可他也在教我们怎么把话说清楚；爸爸妈妈提醒我们按时起床，其实是在教我们守时；体育老师让我们把器材放回原处，是在教我们做事有头有尾。这些做人的道理，其实是很久以前就传下来的。古人说尊师重道，是说对教我们的人要有敬意；说与人为善，是说对人要和气、肯帮一把。我们今天在班级里继续把这两件事做出来，就是把这些道理接着往下传。三年级能做的很具体：上课认真听，没听懂的举手问；见到老师问好；答应过的事做到；别人帮了你，说一句谢谢。",
    "lab-1": "现在请你当一次班级里的小观察员。这里有六件在集体里常常遇到的事，每一件事都有三个做法。你选一个你觉得合适的，选完立刻会有一段话告诉你为什么；要是选得不太合适，也会告诉你还可以试试什么。",
    "module-2": "再来说同学相伴。同学是我们每天相处时间最长的人，相伴得好，一天都会很轻松。怎么做呢？第一，有商有量：两个人一起做事，先把想法说一遍，再一起定下来。第二，把话说完：有不同意见，先听完对方那一句，再讲自己的那一句。第三，看到同学有困难，先问一句要不要帮忙，别急着替他做。第四，不拿别人的短处开玩笑。班级和学校也是这样，集体的事人人有份：值日、图书角、教室的花草、走廊里的脚印，都和每个人有关。让我们的学校更美好，不是要做什么大事，而是把身边这点小事做好。还有一件事要记住：在集体里也要注意安全。上下楼梯不推挤、不追跑；实验课和体育活动听老师指挥；看到危险先离开，再告诉老师；自己不舒服或者被欺负了，一定要说出来，说出来才是保护自己。",
    "lab-2": "接下来请你当一次小组长。先挑一个小组要做的任务，再从三种分工办法里选一种，看看接下来会发生什么。选完以后，你会看到这件事往下走的样子，也会看到还可以怎么调整。",
    "worked-example": "我们一起来看小宇和小禾做手抄报。第一步，接到任务：两个人一起出一张关于节约用水的手抄报，周五交。第二步，先商量：他们先花了五分钟说清楚要什么，商定一半画画、一半写字，还留出一块写标题。第三步，分工：小宇说自己画得快，负责画；小禾说自己字工整，负责写。第四步，做到一半发现时间不够：他们没有各自硬撑，而是说出来一起想办法，把标题的字放大一点、画少两幅。第五步，互相说一句谢谢：交上去之前，两个人各说了一句对方做得好的地方，然后一起交给老师。这张手抄报不算最漂亮，但它是两个人一起做出来的。",
    "conceptest-1": "接下来用三个说法考考你，每个说法里都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件任务交给你。下面有八条在集体里的做法，请你判断一下：哪些是在集体里该做的，放进该做的这一边；哪些是需要调整的，放进要调整的这一边。放好以后，再读一读为什么。",
    "posttest": "最后一轮，换几个新的小情境来考考你。这次会遇到同学吵架、小组分工、还有集体里的安全，看看你能不能用上今天的办法。",
    "summary": "这节课我们记住四句话。第一句，引路人就在我们身边，他们教我们的不只是书本上的事，还有守时、诚实、把话说清楚、对人有礼貌。第二句，和同学相伴要做到有商有量、把话说完、看到困难先问一句、不拿别人的短处开玩笑。第三句，集体的事人人有份，我能为班级和学校做一件具体的小事。第四句，在集体里也要注意安全：不推挤、听指挥、看到危险先告诉老师，遇到麻烦一定要说出来。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出三位你身边的引路人，各写一句他们教过你的事；再写出和同学相伴的两条具体做法。第二层能力应用，动手做：在本周里为班级做一件具体的小事，写清楚你做了什么、别人有什么反应。第三层迁移挑战，选做：如果你和同学有过一次小矛盾，把当时的情况写下来，再说一说现在你会怎么做，然后找机会和他说一句话。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 走近我们的引路人", "lab-1": "动手一 班级小观察员",
    "module-2": "概念二 同学相伴 · 让我们的学校更美好", "lab-2": "动手二 小组任务分工模拟",
    "worked-example": "例题示范 小宇和小禾的手抄报", "conceptest-1": "概念测试",
    "synthesis": "综合任务 在集体里该做的 / 要调整的", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：班级里常常遇到的六件事 × 三个做法 ──
SCENES = [
    {"id": "s1", "t": "上课有一道题我没听懂，下课铃响了", "opts": [
        {"k": "a", "t": "拿起本子去问老师：这一步为什么要这样算", "ok": True,
         "fb": "问得越具体，老师越容易帮你。把没听懂的那一步指出来，比说一句「我都不会」管用得多。"},
        {"k": "b", "t": "不懂就算了，反正下课了，先出去玩", "ok": False,
         "fb": "这样可能会让这个小问题一直留到以后，下次遇到同类的题还是不会。还可以试试：先把卡住的那一步圈出来，下课后花一分钟问老师。"},
        {"k": "c", "t": "跟同桌说：老师讲得一点都不清楚", "ok": False,
         "fb": "这样可能会让同桌也跟着糊涂，老师还不知道你卡在哪里。还可以试试：把不懂的那一步说清楚，老师才知道该给你讲哪一块。"},
    ]},
    {"id": "s2", "t": "同桌写字比较慢，作业常常拖到最后一个交", "opts": [
        {"k": "a", "t": "等他一会儿，或者先帮他把要交的本子理好", "ok": True,
         "fb": "你没有替他写，只是帮他省了一点时间。这样的帮忙刚刚好。"},
        {"k": "b", "t": "先走，谁慢谁自己交", "ok": False,
         "fb": "这样可能会让他更着急，写字也会更慢。还可以试试：先问一句「要不要我帮你把本子理好」，再一起走。"},
        {"k": "c", "t": "当着大家的面说：他总是写得最慢", "ok": False,
         "fb": "这样可能会让他很难受，也容易被别人拿来开玩笑。还可以试试：私下问问他哪儿慢，需要什么帮忙。"},
    ]},
    {"id": "s3", "t": "走廊上有个低年级的小朋友摔倒了", "opts": [
        {"k": "a", "t": "扶他到旁边坐下，问一句疼不疼，再去叫老师", "ok": True,
         "fb": "先照看他，再找大人，这两步都做到了。遇到受伤的情况，找老师比自己处理更稳妥。"},
        {"k": "b", "t": "觉得好玩，先笑一下", "ok": False,
         "fb": "这样可能会让摔倒的小朋友更委屈，也可能让他不敢再求助。还可以试试：先把他扶起来，问一句有没有事。"},
        {"k": "c", "t": "不是我们班的，快走开", "ok": False,
         "fb": "这样可能会让他一个人躺在地上，错过帮助。还可以试试：帮着喊一声老师，或者找就近的同学一起来。"},
    ]},
    {"id": "s4", "t": "两个同学为一块橡皮吵起来，拉着你评理", "opts": [
        {"k": "a", "t": "让他们一人说一句，先把事情说清楚", "ok": True,
         "fb": "先听完两边的话，事情才看得明白。你做的其实是一件很了不起的事。"},
        {"k": "b", "t": "马上站到一边，帮着一起吵", "ok": False,
         "fb": "这样可能会让吵架变成两个人对三个人。还可以试试：先各听一句，再一起想想有没有别的办法。"},
        {"k": "c", "t": "谁也不管，快点走开", "ok": False,
         "fb": "这样可能会让他们的矛盾越闹越大，事后大家心里都不舒服。还可以试试：说一句「你们先说说怎么回事」再走。"},
    ]},
    {"id": "s5", "t": "班会上你想提一个建议：图书角多放几本科普书", "opts": [
        {"k": "a", "t": "举手，先说建议，再说一句为什么", "ok": True,
         "fb": "先说清楚再讲理由，大家更容易听明白，也更容易一起商量。"},
        {"k": "b", "t": "算了不说，反正说了也没人听", "ok": False,
         "fb": "这样可能会让一个好主意一直放在你心里。还可以试试：先把建议写在一句话里，等班会上举手说出来。"},
        {"k": "c", "t": "写在小纸条上传给同学，让他们替你说", "ok": False,
         "fb": "这样可能会让话传到最后变了样，大家还不知道是谁提的。还可以试试：自己站起来说一句，请同学帮你补充。"},
    ]},
    {"id": "s6", "t": "老师安排你和一位不太熟的同学一起做手抄报", "opts": [
        {"k": "a", "t": "先商量谁画、谁写字，再一起做", "ok": True,
         "fb": "先商量一件小事，两个人就有了共同的做法，后面的活就顺了。"},
        {"k": "b", "t": "自己一个人全做完，不告诉他", "ok": False,
         "fb": "这样可能会让你很累，他也没参与进来，交上去的作品里少了他那一份。还可以试试：先问他最想画哪一部分。"},
        {"k": "c", "t": "什么也不做，等他自己做完", "ok": False,
         "fb": "这样可能会让两个人的事变成一个人的事，时间也会很紧。还可以试试：先挑一件自己能做的，比如写字或者涂色。"},
    ]},
]

# ── 动手二：小组任务分工模拟（6 个任务 × 3 种分工办法） ──
SCHEMES = [
    {"k": "a", "n": "先一起商量，按各自擅长的分好", "ok": True},
    {"k": "b", "n": "一个人全做完，别人在旁边看", "ok": False},
    {"k": "c", "n": "谁抢到谁做，剩下的没人管", "ok": False},
]
TASKS = [
    {"id": "t1", "n": "出一期黑板报", "out": {
        "a": "会画画的画画，字工整的写字，个子高的写标题。黑板报出来得又快又好看，每个人都有自己的那一块，站远了看也很整齐。",
        "b": "一个人从头画到尾，可能会来不及，手也会很酸；旁边的同学想帮忙却插不上手。还可以试试：先把要做的事列出来，再问一句「你想做哪一件」。",
        "c": "抢到活的人做得很开心，没抢到的人站在一边看着。到了要交的时候才发现，右下角还空着一大块。还可以试试：先把事情分清楚，再一起动手。"}},
    {"id": "t2", "n": "整理班级图书角", "out": {
        "a": "有人按高矮摆好，有人贴分类标签，有人清点少了哪几本。午休还没结束，图书角就能用了，找书也不用翻半天。",
        "b": "一个人整理一整个图书角，可能会又累又慢，其他同学不知道自己该做什么。还可以试试：先问问谁愿意管标签、谁愿意管登记。",
        "c": "大家都在书角里翻来翻去，摆好的书又被翻乱，最后书架还是乱糟糟的。还可以试试：先分好谁做哪一步，再一起开始。"}},
    {"id": "t3", "n": "准备一次班级朗诵", "out": {
        "a": "有人领读，有人排队形，有人准备音乐。练上两遍就顺了，站上台也不慌。",
        "b": "一个人什么都自己上，可能会记不住那么多事，越到后面越着急。还可以试试：把领读、排队、音乐这三件事先分出去。",
        "c": "没人说清谁站在哪儿，每次练都要重来一遍，时间都花在整队上。还可以试试：先一起把每个人站的位置定下来，再开始练。"}},
    {"id": "t4", "n": "给教室做一次大扫除", "out": {
        "a": "分好擦窗、扫地、倒垃圾、整理讲台，各人做各人那一块，做完一起检查一遍。教室很快干净了。",
        "b": "一个人擦完所有的窗，可能会累到来不及扫地。还可以试试：先看看一共有几件事，再一件一件分出去。",
        "c": "大家都挤在同一扇窗前，别的地方一直没人管，最后还要重新来一次。还可以试试：先把要做的地方数一数，再分开做。"}},
    {"id": "t5", "n": "给一年级同学做一张安全提示卡", "out": {
        "a": "有人想内容，有人画画，有人把字写大。一年级的小朋友一看就懂，还会照着做。",
        "b": "一个人自己画完，可能想不到一年级同学哪里看不懂。还可以试试：先请一位同学念一遍，看看好不好懂。",
        "c": "你画一半我画一半，画到一半才发现写不下了，只好重画。还可以试试：先商量好大小和位置，再一起动笔。"}},
    {"id": "t6", "n": "班级运动会入场式", "out": {
        "a": "有人喊口号，有人拿班牌，有人带队伍。走起来整整齐齐，口号也响亮。",
        "b": "一个人安排所有人的位置，可能会记不过来，队伍一走就乱。还可以试试：先定几个小队长，各自记住自己那一段。",
        "c": "谁站哪儿都靠喊，一乱就得重来，练到最后大家都有点烦。还可以试试：先在地上做好记号，再对着记号站好。"}},
]

# ── 综合任务：在集体里该做的 / 要调整的（八条行为分进两个筐） ──
SORT_ITEMS = [
    {"id": "k1", "t": "两个人一起做事，先花几分钟把想法说清楚", "bin": "good",
     "why": "有商有量，是把两个人的事做成一件好事的开头。"},
    {"id": "k2", "t": "同学有不同意见，先听他把那一句说完", "bin": "good",
     "why": "把话听完，才谈得上一起商量。对方也会更愿意听你的。"},
    {"id": "k3", "t": "看到同学搬着一摞本子，先问一句要不要帮忙", "bin": "good",
     "why": "先问一句，比直接替他做更尊重他，也更帮得上忙。"},
    {"id": "k4", "t": "值日时把自己负责的那一块做完，再一起检查", "bin": "good",
     "why": "集体的事人人有份，把自己那一块守住，就是为集体做事。"},
    {"id": "k5", "t": "小组任务里，把最难的那部分直接塞给别人", "bin": "tune",
     "why": "这样可能会让同学心里不舒服，下次他也不愿意和你一组。还可以试试：先问问谁更擅长哪一块，难的活一起做。"},
    {"id": "k6", "t": "同学回答错了，跟着大家一起笑起来", "bin": "tune",
     "why": "这样可能会让他以后不敢再举手。还可以试试：安静地听他说完，等老师来讲。"},
    {"id": "k7", "t": "在走廊里追着同学跑，看谁先到教室", "bin": "tune",
     "why": "这样很容易撞到别人，也可能自己摔倒。还可以试试：把比赛放到操场上，跑之前先看看身边有没有人。"},
    {"id": "k8", "t": "被同学起了难听的外号，忍着自己不说话", "bin": "tune",
     "why": "这样可能会让这件事一直跟着你，心里越来越难受。还可以试试：先告诉他「我不喜欢这样」，再说给老师或爸爸妈妈听，说出来才是保护自己。"},
]
SORT_BIN = {"good": "在集体里该做的", "tune": "要调整的"}

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g3-u3 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 班级小观察员：六件事 × 三个做法 → 温和反馈（不判错、不贴标签）
   3) 小组任务分工模拟：选任务 → 选分工办法 → 展开后果
   4) 在集体里该做的 / 要调整的：八条行为分进两个筐
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

  /* ---------- 2. 班级小观察员 ---------- */
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

  /* ---------- 3. 小组任务分工模拟 ---------- */
  var TASKS = __TASKS_JSON__;
  var SCHEMES = __SCHEMES_JSON__;
  var stage2 = document.getElementById('task-stage');
  if (stage2) {
    var curTask = null, doneTask = {};
    var out2 = document.getElementById('task-out');

    function taskById(id) {
      for (var i = 0; i < TASKS.length; i++) { if (TASKS[i].id === id) return TASKS[i]; }
      return null;
    }
    function render2() {
      document.querySelectorAll('[data-task]').forEach(function (b) {
        var k = b.dataset.task;
        b.classList.toggle('selected', k === curTask);
        b.classList.toggle('correct', !!doneTask[k]);
      });
      document.getElementById('task-score').textContent =
        '已经试过 ' + Object.keys(doneTask).length + ' / ' + TASKS.length + ' 个任务';
    }
    document.querySelectorAll('[data-task]').forEach(function (b) {
      b.addEventListener('click', function () {
        curTask = b.dataset.task;
        var T = taskById(curTask);
        if (doneTask[curTask]) {
          out2.className = 'result';
          out2.innerHTML = '<strong>这个任务已经试过了：' + T.n + '</strong>你上次选的分工办法挺合适，换成别的任务再试试。';
        } else {
          out2.className = 'result warn';
          out2.innerHTML = '<strong>小组要做的任务是：' + T.n + '</strong><br>下面有三种分工办法，你选一种，看看接下来会发生什么。';
        }
        render2();
      });
    });
    document.querySelectorAll('[data-scheme]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!curTask) {
          out2.className = 'result warn';
          out2.textContent = '先在上面点一个任务，再来选分工办法。';
          return;
        }
        var T = taskById(curTask);
        var k = b.dataset.scheme;
        var isOk = false;
        for (var i = 0; i < SCHEMES.length; i++) { if (SCHEMES[i].k === k) isOk = !!SCHEMES[i].ok; }
        if (isOk) {
          doneTask[T.id] = true;
          out2.className = 'result';
          out2.innerHTML = '<strong>' + T.n + '：这样分工很顺。</strong>' + T.out[k];
        } else {
          out2.className = 'result warn';
          out2.innerHTML = '<strong>' + T.n + '：这样可能会不太顺。</strong>' + T.out[k];
        }
        render2();
      });
    });
    render2();
  }

  /* ---------- 4. 在集体里该做的 / 要调整的 ---------- */
  var ITEMS = __SORT_JSON__;
  var BINN = __SORTBIN_JSON__;
  var stage3 = document.getElementById('class-stage');
  if (stage3) {
    var pickItem = null, placed = {};
    var out3 = document.getElementById('class-out');
    function render3() {
      document.querySelectorAll('[data-item]').forEach(function (b) {
        var k = b.dataset.item;
        b.classList.toggle('selected', k === pickItem);
        b.classList.toggle('done', !!placed[k]);
        b.disabled = !!placed[k];
      });
      document.getElementById('class-score').textContent =
        '已经放好 ' + Object.keys(placed).length + ' / ' + ITEMS.length + ' 条';
      var a = document.getElementById('class-bin-a');
      var b2 = document.getElementById('class-bin-b');
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
        out3.className = 'result warn';
        out3.innerHTML = '<strong>你选的是：' + b.textContent + '</strong><br>想一想，它是「在集体里该做的」，还是「要调整的」？';
        render3();
      });
    });
    document.querySelectorAll('[data-class-bin]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pickItem) {
          out3.className = 'result warn';
          out3.textContent = '先在上面点一条做法，再选筐。';
          return;
        }
        var it = null;
        for (var i = 0; i < ITEMS.length; i++) { if (ITEMS[i].id === pickItem) it = ITEMS[i]; }
        if (b.dataset.classBin === it.bin) {
          placed[it.id] = true;
          out3.className = 'result';
          out3.innerHTML = '<strong>放对了，它属于「' + BINN[it.bin] + '」。</strong>' + it.why;
          pickItem = null;
          if (Object.keys(placed).length === ITEMS.length) {
            out3.className = 'result';
            out3.innerHTML = '<strong>八条全放对了！</strong>记住这句口诀：<strong>先商量、把话听完，' +
              '看到困难问一句，集体的事人人有份。</strong>';
          }
        } else {
          out3.className = 'result warn';
          out3.innerHTML = '<strong>再想一想这条做法。</strong>' + it.why +
            '<br><span style="color:var(--muted)">常见错误：容易把「看起来也很热心」误认为「在集体里该做的」——' +
            '先看这件事有没有让别人为难，答案就清楚了。</span>';
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
             .replace('__TASKS_JSON__', json.dumps(TASKS, ensure_ascii=False))
             .replace('__SCHEMES_JSON__', json.dumps(SCHEMES, ensure_ascii=False))
             .replace('__SORT_JSON__', json.dumps(SORT_ITEMS, ensure_ascii=False))
             .replace('__SORTBIN_JSON__', json.dumps(SORT_BIN, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "下面哪些人算是我们身边的引路人？",
         "options": [("教我们功课的老师、提醒我们按时起床的爸爸妈妈，还有操场上提醒过我们一句话的人", True),
                     ("只有站在讲台上的老师才算", False),
                     ("只有家里的大人算，同学不算", False)],
         "explain": "引路人就是那些带我们往前走的人，他们教我们的时候，不只是在讲知识，也在教我们做事和做人。"
                    "<strong>错因提醒：</strong>常见错误是误认为「引路人只有老师」——"
                    "其实家里的大人、教练、邻居，甚至同学的一句提醒，都可能教给我们一点东西。"},
        {"q": "两个人一起做一张手抄报，下面哪种开头比较好？",
         "options": [("先花几分钟说清楚各自想怎么做，再一起定下来", True),
                     ("一个人先做完，另一个人看着就好", False),
                     ("谁先拿到纸谁说了算", False)],
         "explain": "先把想法说清楚，两个人就有了共同的做法，后面的活才顺。"
                    "<strong>错因提醒：</strong>有的同学误认为「一起做事就是各做各的、最后拼起来」——"
                    "中间不说、不问，拼起来很容易对不上。"},
        {"q": "在走廊里，几个同学追着跑着玩，你会怎么做？",
         "options": [("不跟着追，提醒他们到操场上玩，跑之前先看看身边有没有人", True),
                     ("一起追，人多更好玩", False),
                     ("站在旁边给他们加油", False)],
         "explain": "走廊里人很多，追跑很容易撞到低年级的同学，也可能自己摔倒。"
                    "<strong>错因提醒：</strong>容易把「大家玩得开心」误认为「这样做没关系」——"
                    "集体里的安全，是每个人都要守的那一条线。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "走近我们的引路人：他们教我们的，不只是书本上的事", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们已经认识了很多老师和大人在帮我们，也习惯了他们每天提醒我们（And）；可是有时候我们只看见他们在「管」我们，没看见他们其实在教我们怎么做人做事（But）；所以这节课先走近引路人，看看他们到底把什么交给了我们（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">引路人，就是<strong>那些带我们往前走的人</strong>。他们教我们的时候，常常不是在上课。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>在学校里</strong></p>
            <p style="color:var(--muted)">老师讲一道题怎么算，也在教我们怎么把话说清楚；体育老师让我们把器材放回原处，是在教我们做事有头有尾。</p>
          </div>
          <div class="inner-card">
            <p><strong>在家里和身边</strong></p>
            <p style="color:var(--muted)">爸爸妈妈提醒我们按时起床，是在教我们守时；邻居阿姨帮着扶一下门，是在教我们待人客气。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="身边的引路人概念图：老师、家人、身边的人分别教给我们什么做人做事的道理，附中文标注">
          <figcaption>概念图：身边的引路人——守时 · 诚实 · 把话说清楚 · 有礼貌 · 不放弃（教学示意图，中性简洁扁平插画）</figcaption>
        </figure>
        <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(78,205,196,.45)">
          <p><strong>这些道理，我们祖辈就在讲</strong></p>
          <p style="color:var(--muted)">古人说<strong>尊师重道</strong>，是说对教我们的人要有敬意；说<strong>与人为善</strong>，是说对人要和气、肯帮一把。这不是什么大道理，我们今天在班级里就能接着做：上课认真听，没听懂就举手问；见到老师问好；答应过的事做到；别人帮了你，说一句谢谢。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「引路人的话必须句句照做，不能有自己的想法」。其实他们是在把做事做人的道理教给我们，遇到不懂的地方，你完全可以把自己的想法说出来问一问——会问，也是他们最希望看到的。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "同一件事可以有两种看法：「老师又在管我」和「老师在教我怎么把事做好」。换一种看法，心里的感觉会完全不同。"},
    {"lens": "解释它", "text": "为什么说这些道理是「传下来的」？因为尊师重道、与人为善不是哪个人发明的规矩，是一代一代人试出来、觉得好的做法，我们今天接着用。"},
    {"lens": "迁移它", "text": "这套眼光在家里也用得上：妈妈让你把碗收进厨房，其实在教你做事有头有尾；爸爸让你自己定闹钟，是在教你守时。"},
])}
    ''', tag="概念一"))

    case_btns = "\n".join(
        f'            <button class="choice" data-case="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in SCENES
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：班级小观察员，你会怎么做？", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一件在集体里常常遇到的事，再从三个做法里选一个。<strong>选得好会告诉你为什么，选得不太合适也会告诉你还可以试试什么。</strong></p>
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
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💛</span><div><strong>说给你听：</strong>这里的做法没有分数。有些做法只是会让同学不太舒服，换一个试试就好。拿不准的时候，去问老师，是很好的办法。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "同学相伴 · 让我们的学校更美好", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">同学是我们每天相处时间最长的人。相伴得好，一天都会很轻松。<strong>怎么做？有四个很具体的做法。</strong></p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>有商有量：</strong>两个人一起做事，先把想法说一遍，再一起定下来做什么、谁做哪一块。</div></div>
          <div class="step"><span class="n">2</span><div><strong>把话说完：</strong>有不同意见，先听完对方那一句，再讲自己那一句。</div></div>
          <div class="step"><span class="n">3</span><div><strong>先问一句：</strong>看到同学有困难，问一句「要不要帮忙」，别急着替他做。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>不开玩笑：</strong>不拿别人的短处、口音、家里的情况开玩笑。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="同学相伴与为学校做事的情境图：商量、分工、互相帮忙、把小事做好，附中文标注">
          <figcaption>情境图：同学相伴的四个做法 · 集体的事人人有份（教学示意图，中性简洁扁平插画）</figcaption>
        </figure>
        <div class="inner-card">
          <p><strong>让我们的学校更美好：三年级能做的小事</strong></p>
          <p style="color:var(--muted)">把自己负责的值日做完再一起检查 · 把图书角的书按类摆好 · 给教室的花浇一次水 · 看到走廊里的纸屑弯腰捡起来 · 上下楼梯靠右走、不推不挤 · 有新同学来，带他认一认教室和厕所的位置。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「集体的事是大人的事，和我没关系」。可是班级是我们每天待的地方：书本我们自己摆、地面我们自己走、同学就在身边——这件事里，本来就有你的一份。</p>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>还有一件要紧的事：在集体里也要注意安全</strong></p>
          <p style="color:var(--muted)">上下楼梯不推挤、不追跑；体育课和实验课听老师指挥；看到危险先离开，再告诉老师；自己不舒服、被欺负了、心里难受，一定要说出来——<strong>说出来才是保护自己，也是保护身边的同学。</strong></p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "「有商有量」看起来只是多说了几句话，其实它决定了这件事是一个人扛，还是两个人一起扛。"},
    {"lens": "比较它", "text": "同样是同学写字慢：一种是等一等、帮着理本子，一种是当众说他慢。两句话之后，两个人的一天会很不一样。"},
    {"lens": "迁移它", "text": "这套做法在家里也管用：和弟弟妹妹争一件东西时，先把两个人的想法说一遍，往往就不用吵了。"},
])}
    ''', tag="概念二"))

    task_btns = "\n".join(
        f'            <button class="choice" data-task="{t["id"]}" style="text-align:left">小组任务：{t["n"]}</button>'
        for t in TASKS
    )
    scheme_btns = "\n".join(
        f'            <button class="choice" data-scheme="{s["k"]}" style="text-align:left">{s["n"]}</button>'
        for s in SCHEMES
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：小组任务分工模拟", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">你现在是小组长。先挑一个小组要做的任务，再从三种分工办法里选一种，看看接下来会发生什么。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 我们小组要完成的任务</div>
          <div class="grid" id="task-stage">
{task_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 我们怎么分工</div>
          <div class="grid">
{scheme_btns}
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">试过几个任务</span><span class="v" id="task-score">已经试过 0 / 6 个任务</span></div>
          </div>
          <p class="result warn" id="task-out" style="margin-top:12px">先在上面点一个任务。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧩</span><div><strong>想一想：</strong>三种分工办法里，为什么「先商量、按擅长分」总是走得最顺？因为它让每个人的力气都用在了能做好的那一块上。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小宇和小禾的手抄报", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>老师让小宇和小禾一起出一张关于节约用水的手抄报，周五交。两个人平时不太熟，请你看看他们是怎么把这件事做下来的。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先商量：</strong>花了五分钟说清楚要什么——一半画画、一半写字，留出一块写标题。</div></div>
          <div class="step"><span class="n">2</span><div><strong>按擅长分工：</strong>小宇说自己画得快，负责画；小禾说自己字工整，负责写。谁都没有被剩下。</div></div>
          <div class="step"><span class="n">3</span><div><strong>遇到问题说出来：</strong>做到一半发现时间不够，他们没有各自硬撑，而是说出来一起想办法，把标题字放大、画少两幅。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>收尾说一句好：</strong>交上去之前，两个人各说了一句对方做得好的地方，然后一起交给老师。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「分工就是各做各的，最后拼在一起就行」。可是小宇和小禾中途发现时间不够，是<strong>说出来一起改</strong>才赶上的——不问不说，拼起来常常对不上。</p>
        </div>
        <div class="inner-card">
          <p><strong>说给同桌听：</strong>这四步里，哪一步最容易被忘掉？如果周五只能留一步，你会留哪一步？为什么？</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "下面哪句话说得对？",
         "options": [("引路人教我们的不只是书本上的事，还有守时、诚实、把话说清楚、对人有礼貌", True),
                     ("引路人说的话都要照做，不能有自己的想法", False),
                     ("只有成绩好的人才能当我们的引路人", False)],
         "explain": "引路人交给我们的，一半是知识，一半是做事的道理。"
                    "<strong>错因提醒：</strong>常见错误是误认为「引路人的话必须句句照做」——"
                    "遇到不懂的地方，把自己的想法说出来问一问，也是他们最希望看到的。"},
        {"q": "小组一起做一件事，下面哪个做法更好？",
         "options": [("先一起商量做什么、谁做哪一块，中途有问题就说出来", True),
                     ("一个人全做完，别人在旁边看着", False),
                     ("谁抢到活谁做，剩下的没人管", False)],
         "explain": "先商量、按擅长分，中途有问题就一起改，事情才做得完也做得好。"
                    "<strong>错因提醒：</strong>有的同学误认为「一个人做还快一些」——"
                    "一个人做确实没人妨碍，但会来不及，别人也少了参与的机会。"},
        {"q": "在班里被同学起了难听的外号，下面哪个做法更好？",
         "options": [("先告诉他我不喜欢这样，再说给老师或爸爸妈妈听", True),
                     ("忍着自己不说话，过几天就好了", False),
                     ("也给他起一个更难听的外号", False)],
         "explain": "说出来，是保护自己也保护同学的第一步；大人知道了才能帮上忙。"
                    "<strong>错因提醒：</strong>容易把「忍一忍就过去了」当成懂事——"
                    "忍着不说，事情常常不会自己变好。"}
    ], tag="概念测试"))

    item_btns = "\n".join(
        f'            <button class="sort-item" data-item="{it["id"]}">{it["t"]}</button>' for it in SORT_ITEMS
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：在集体里该做的 / 要调整的，把做法分进两个筐", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一条做法，再点它应该进的筐：<strong>在集体里该做的</strong>放一边，<strong>要调整的</strong>放另一边。</p>
        <div class="lab-panel">
          <div class="sort-bank" id="class-stage">
{item_btns}
          </div>
          <div class="grid grid-2" style="margin-top:14px">
            <button class="choice" data-class-bin="good" style="text-align:center">在集体里该做的</button>
            <button class="choice" data-class-bin="tune" style="text-align:center">要调整的</button>
          </div>
          <div class="sort-bins">
            <div class="sort-bin" id="class-bin-a"><h4>在集体里该做的</h4></div>
            <div class="sort-bin" id="class-bin-b"><h4>要调整的</h4></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">分类进度</span><span class="v" id="class-score">已经放好 0 / 8 条</span></div>
          </div>
          <p class="result warn" id="class-out" style="margin-top:12px">先在上面点一条做法。</p>
        </div>
        <div class="inner-card">
          <p><strong>分完之后，想一想：</strong></p>
          <p style="color:var(--muted)">「在集体里该做的」这一边里，你最想先做哪一条？写在下面，再说一说为什么选它。</p>
          <textarea id="syn-answer" rows="3" placeholder="我最想先做……，因为……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，办法还在不在", TTS["posttest"], [
        {"q": "两个同学吵起来，都来拉你评理，下面哪个做法更好？",
         "options": [("让他们一人说一句，先把事情说清楚", True),
                     ("马上站到一边，帮着一起吵", False),
                     ("谁也不管，快点走开", False)],
         "explain": "先听完两边的话，才看得明白事情是怎么回事。"
                    "<strong>错因提醒：</strong>常见错误是误认为「不管就是不吃亏」——"
                    "这样可能让矛盾越闹越大，事后大家心里都不舒服。"},
        {"q": "班会上你想提一个建议，下面哪个做法更好？",
         "options": [("举手，先说建议，再说一句为什么", True),
                     ("算了不说，反正说了也没人听", False),
                     ("写纸条到处传，让别人替你说", False)],
         "explain": "先说清楚再讲理由，大家更容易听明白，也更容易一起商量。"
                    "<strong>错因提醒：</strong>有人把「说出来没人听」当成不说的理由——"
                    "把建议说得具体一点，被听见的机会大得多。"},
        {"q": "上下楼梯时，后面的同学挤着往前推，下面哪个做法最合适？",
         "options": [("停下来靠右走，告诉他楼梯上不能推挤，人也多", True),
                     ("也挤回去，看谁厉害", False),
                     ("加快脚步往上跑，离他远一点", False)],
         "explain": "楼梯上推挤很危险，靠右慢走、提醒一句，是对大家最安全的做法。"
                    "<strong>错因提醒：</strong>容易把「大家都这样走」误认为「这样做没关系」——"
                    "集体里的安全，是每个人都要守住的那一条线。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：四句话，讲清怎样在集体中长大", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>走近引路人：</strong>他们教我们的不只是书本上的事，还有守时、诚实、把话说清楚、对人有礼貌。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>同学相伴：</strong>有商有量、把话说完、看到困难先问一句、不拿别人的短处开玩笑。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>让学校更美好：</strong>集体的事人人有份，我能为班级做一件具体的小事。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>安全记心上：</strong>不推挤、听指挥、看到危险先告诉老师；遇到麻烦一定要说出来。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>一句口诀：</strong>先商量、把话听完，看到困难问一句，集体的事人人有份。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「引路人、一起商量、我来做一件小事」这三个说法，说清楚你在集体里的一件事。</p>
          <p style="color:var(--muted)">再动一动手：<strong>写一写</strong>你这周想为班级做的那一件小事，写清做什么、什么时候做。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写出三位你身边的引路人，各写一句他们教过你的事。",
            "写出和同学相伴的两条具体做法，每条写一句话。",
            "写出在集体里要注意的一条安全做法。",
        ],
        [
            "本周为班级做一件具体的小事（比如整理一次图书角、帮值日生检查一遍），写清楚你做了什么、别人有什么反应。",
            "和一位同学一起完成一件小事，先商量分工，做完写一句你想对他说的话。",
        ],
        [
            "如果你和同学有过一次小矛盾，把当时的情况写下来，再说一说现在你会怎么做，然后找机会和他说一句话。",
            "问一问家里的大人：他小时候在集体里，有没有一位让他一直记得的引路人？把他的话记下来，和今天学的一起说一说。",
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
    "title": "在集体中长大",
    "name_en": "Growing Up in the Group",
    "grade": 3,
    "grade_cn": "三年级",
    "domain": "health-safety",
    "domain_cn": "生命安全与健康",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学三年级的道德与法治课：先走近身边的引路人——老师、家人和身边带我们的人，看见他们教给我们的不只是书本上的事，还有守时、诚实、把话说清楚、有礼貌，这些做人做事的道理正是尊师重道、与人为善这些传统美德在今天的样子；再聊同学相伴的四个具体做法：有商有量、把话说完、看到困难先问一句、不拿别人的短处开玩笑；最后落到「让我们的学校更美好」——集体的事人人有份，我能为班级做一件具体的小事，并把集体里的安全要求（不推挤、听指挥、遇到麻烦要说出来）讲清楚。全课以真实情境与可操作的选择为主，三个互动台子分别是情境卡选做法展开后果、小组任务分工模拟、以及把八条行为分进「在集体里该做的／要调整的」两个筐。",
    "tags": ["在集体中长大", "引路人", "同学相伴", "让我们的学校更美好", "集体意识", "同学相处", "三年级", "生命安全与健康"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学「生命安全与健康」——感受中华优秀传统文化魅力，增强文化自信，并在集体生活中学会与同学友好相处、注意安全；对应统编《道德与法治》三年级上册「在集体中长大」：走近我们的引路人、同学相伴、让我们的学校更美好。",
    "hero_question": "在班级这个集体里，是谁带你长大？你又为这个集体做过什么？",
    "hero_alt": "在集体中长大知识结构图：走近我们的引路人、同学相伴、让我们的学校更美好 三栏",
    "hero_caption": "在集体中长大：走近我们的引路人 · 同学相伴 · 让我们的学校更美好（先商量、把话听完、集体的事人人有份）",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "谁是我们身边的引路人？", "d": "他们教我们的到底是什么", "v": "谁是我们身边的引路人"},
        {"t": "同学之间怎样才能相伴得更好？", "d": "一起做一件事，怎样才顺", "v": "同学之间怎样才能相伴得更好"},
        {"t": "我能为班级和学校做点什么？", "d": "三年级能做的一件小事", "v": "我能为班级和学校做点什么"},
        {"t": "在集体里有了矛盾怎么办？", "d": "吵架、起外号、被推挤", "v": "在集体里有了矛盾怎么办"},
    ],
    "objectives": [
        "能说出身边的引路人是谁，他们教给我们的做人做事的道理是什么",
        "能说出和同学相伴的两三条具体做法：有商有量、把话说完、看到困难先问一句、不拿别人的短处开玩笑",
        "能说出自己能为班级和学校做的一件具体小事，并愿意动手去做",
        "知道在集体里也要注意安全：不推挤、听指挥、看到危险先告诉老师，遇到麻烦一定要说出来",
    ],
    "objectives_plain": [
        "能说出身边的引路人是谁，他们教给我们的做人做事的道理是什么",
        "能说出和同学相伴的两三条具体做法，并愿意在小组里试一试",
        "能说出自己能为班级和学校做的一件具体小事",
        "知道在集体里也要注意安全：不推挤、听指挥、遇到麻烦要说出来",
    ],
    "standards": [
        {"content": "感受中华优秀传统文化魅力，增强文化自信。",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学 生命安全与健康"},
        {"content": "走近我们的引路人；同学相伴；让我们的学校更美好",
         "source": "统编《道德与法治》三年级上册「在集体中长大」"},
    ],
    "prereqs": ["pol-e-g3-u2"],
    "prereqs_name": "学科学 爱科学",
    "prereqs_meta": "pol-e-g3-u2",
    "leads_to": ["pol-e-g3-u4"],
    "next_meta": "pol-e-g3-u4",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "每天带我们长大的人，不只站在讲台上。这节课我们走近引路人、聊同学相伴、为学校做一件小事。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能说出一件自己想为班级做的事。",
        "objectives": "看清四件事：引路人是谁、同学怎样相伴、我能做什么、集体里要注意什么安全。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "引路人教我们的不只是知识，还有守时、诚实、把话说清楚、有礼貌；这些道理祖辈就在讲。",
        "lab-1": "六件常常遇到的事，每件三个做法。选得不太合适也不会说你错，只会告诉你还可以试试什么。",
        "module-2": "同学相伴四个做法：有商有量、把话说完、先问一句、不开玩笑；集体的事人人有份。",
        "lab-2": "你是小组长：先挑任务，再挑分工办法，看看接下来会发生什么。",
        "worked-example": "小宇和小禾做手抄报四步：先商量、按擅长分工、有问题说出来、收尾说一句好。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "把八条做法分进「在集体里该做的」和「要调整的」两个筐，分完读一读为什么。",
        "posttest": "出现了同学吵架、班会提建议、楼梯上被推挤，看看你能不能把今天的办法用上去。",
        "summary": "四句话：走近引路人、同学相伴、为学校做事、安全记心上。",
        "homework": "三层小任务，先做前两层，第三层可以请家里人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学道德与法治「生命安全与健康」板块在三年级的空缺，正对统编教材三年级上册「在集体中长大」（走近我们的引路人、同学相伴、让我们的学校更美好）。三年级学生每天在班级里生活，但容易只看见「大人在管我」，看不见这些提醒背后的做人道理；也容易把「一群人在一块」当成「已经是集体」。所以全课先把集体拆成三个看得见的层面：一是引路人——老师、家人和身边带我们的人，他们教的不只是书本上的事，还有守时、诚实、把话说清楚、有礼貌，而这些正是尊师重道、与人为善等传统美德在今天的样子（呼应课标「感受中华优秀传统文化魅力」）；二是同学相伴的四个具体做法：有商有量、把话说完、看到困难先问一句、不拿别人的短处开玩笑；三是让我们的学校更美好——集体的事人人有份，落到三年级能做的六件小事上。同时把本学段「安全与健康」的要求落进集体场景：不推挤、听指挥、看到危险先告诉老师，遇到麻烦一定要说出来。三个互动台子都能真操作：动手一是六件集体里常见的事，每件三个做法，选完立刻展开后果，反馈一律写成「这样可能会……，还可以试试……」；动手二是小组任务分工模拟，先挑任务再挑分工办法，看这件事往下走的样子；综合任务是分类判断，把八条行为分进「在集体里该做的／要调整的」两个筐。插图一律为中性简洁扁平插画，不使用真人照片风格，也不做人物崇拜式的表达。",
    "plan_table": """| 1 | cover | 在集体中长大 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 走近我们的引路人：他们教我们的，不只是书本上的事 | 承·概念一（引路人与传统美德） |
| 6 | interactive | 动手一：班级小观察员，你会怎么做？ | 承·情境判断（六件事 × 三做法） |
| 7 | concept | 同学相伴 · 让我们的学校更美好 | 承·概念二（四个做法 + 集体安全） |
| 8 | interactive | 动手二：小组任务分工模拟 | 承·操作模拟（选任务 → 选分工 → 展开后果） |
| 9 | concept | 例题示范：小宇和小禾的手抄报 | 转·重难点突破（四步示范 + 易错点） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：在集体里该做的 / 要调整的，把做法分进两个筐 | 合·迁移应用（分类判断） |
| 12 | quiz | 后测：换几个新情境，办法还在不在 | 合·后测 |
| 13 | summary | 小结：四句话，讲清怎样在集体中长大 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：走近我们的引路人 / 同学相伴 / 让我们的学校更美好 三栏\n- P5 身边的引路人概念图（已生成）：老师、家人与身边的人分别教给我们什么，附中文标注\n- P7 同学相伴与为学校做事情境图（已生成）：商量、分工、互相帮忙、把小事做好，附中文标注\n- 三张图均为中性简洁扁平教学插画，不使用真人照片风格，不含可识别的真实人物\n- 涉及矛盾与安全的内容以文字表达，不出现冲突、受伤等画面\n- 若需补充：学校平面图与值日分工表（需学校提供并授权后使用）",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
