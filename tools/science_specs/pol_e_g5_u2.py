# -*- coding: utf-8 -*-
"""小学道德与法治 · 我们是班级的主人（五年级上·第2单元）—— 补齐知识树「中华优秀传统文化」空缺

学科语气（道德与法治）：情境案例驱动，情感共鸣 + 价值判断，从班级里天天发生的小事讲起；
结论落在「应该怎么做、为什么」，不做道德说教、不背条文、不喊口号。

内容落点（对应统编五上第 2 单元「我们是班级的主人」）：
  ① 选举产生班委会：班委会是指班级里由同学们推选出来、为大家服务的一小组人，成员由全班同学
     选举产生。选举要看清三件事——先看岗位要做什么、再听他打算怎么做、最后看平时做得怎么样；
     一人一票，按大家一起商定的办法投。选上的人认真做，没选上的人也能继续出力。
  ② 协商决定班级事务：协商是指把问题摆到桌面上，每个人把想法和理由说清楚，一起找一个大家都
     愿意试一试的办法。议事五步：把问题说清楚 → 每人说想法和理由 → 找共同点 → 定一个能试的
     办法（说清试多久、谁来做）→ 过一段时间回来看效果再调整。
     评判一个办法好不好，看三条：能不能解决大家的问题、能不能做到、有没有照顾到少数同学。
  ③ 落到自己身上：班规是大家一起定的，也要大家一起守；班级公约里也能一起商量「哪些事我们不做」，
     比如不玩有危险的游戏、遇到有人在校外递烟要及时告诉老师和家里人——保护好自己，也是主人
     该做的一件事。

三个互动台子都能真操作（反馈一律写成「这样可能会……，还可以试试……」）：
  动手一 = 班务议事台（4 个真实班务问题 × 每个 3 个处理办法 → 选 → 看执行后果）；
  动手二 = 议事五步搭建台（打乱的步骤卡按顺序点，排对生成「我们班的议事五步」）；
  综合任务 = 我的班级提案生成台（选问题 → 选办法 → 选怎么试，合成一份可提交给班委的提案）。
插图一律中性简洁扁平插画，不使用真人照片风格。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g5-u2"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "班里有四十来个同学，每天在一起上课、活动、值日。有人的桌子脏了，有人要借一本书，有人今天请假没值日，这些事总得有人管一管、有人张罗一下，班委会就是这么来的。可你想过没有：班委是谁定下来的？班里的事，又该谁说了算？这节课我们弄清楚两件事。第一件，班委会是怎么选出来的。第二件，班级的事怎么一起商量着定。带着这两个问题，我们开始。",
    "problem-anchor": "开始之前，先选一个你真正想知道的问题。是想知道班委到底该怎么选，还是想知道班里的事该怎么商量；是想知道被选上的人要做什么，还是想知道自己不做班委又能为班级做点什么。选好以后，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出班委会是什么，它的成员是由全班同学选举产生的。第二，能说出选举时要看清的三件事：先看这个岗位要做什么、再听他打算怎么做、最后看他平时做得怎么样。第三，能说出协商决定班级事务的五个步骤：把问题说清楚、每人说想法和理由、找共同点、定一个能试的办法、过一段时间回来看效果再调整。第四，能说出判断一个办法好不好要看的三条：能不能解决大家的问题、能不能做到、有没有照顾到少数同学。",
    "pretest": "先做三道小题，用你现在的想法选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "先说第一件事：班委是谁定下来的。班委会是指班级里由同学们推选出来、为大家服务的一小组人，比如班长、学习委员、体育委员、劳动委员。它的成员不是老师指定的，也不是谁自己说了算，而是由全班同学选举产生的。选举是指按照大家一起商定的办法，由全班同学投票或者举手表决，选出愿意为班级做事、大家信得过的人。要选得明白，得先看清三件事。第一，这个岗位要做什么。体育委员要组织大家做操、管器材借还；劳动委员要排值日、看卫生。岗位干什么都不清楚，投票就是凭印象。第二，他打算怎么做。愿意做的同学把自己的打算讲一讲，大家提问，他当场回答。第三，他平时做得怎么样。说过的话有没有做到，是最实在的一票。这三件事看完，再一人一票，投给自己认为合适的那个人。这里有两个最容易想歪的地方。第一个，很多同学误认为「选班委就是看平时关系好不好」，可班级的事是大家一起过的日子，要选的是能把事做好的人。第二个，有人误认为「反正我不当，选谁都一样」，可班委是替全班做事的，选谁都在决定这个班以后怎么样，你的一票也算数。一句话记住：先看岗位、再听打算、后投一票；选上的人认真做，没选上的人也能继续出力。",
    "lab-1": "现在请你坐到议事台前，当一次班里的小主人。这里有四个班务问题，都是班里真实会碰到的。每个问题下面有三个处理办法，你选一个，我就把执行下去会发生什么、谁会受影响，一并告诉你。选得不太合适也没关系，看完还可以换一个办法再试。",
    "module-2": "再说第二件事：班级的事谁说了算。答案是大家一起商量着定。协商是指把问题摆到桌面上，每个人把自己的想法和理由说清楚，一起找一个大家都愿意试一试的办法。商量不是随便聊聊，它有五个步骤。第一步，把问题说清楚：到底是什么事、影响到了谁。第二步，每人说想法和理由，别人说的时候不打断。第三步，找共同点：说来说去，大家最在意的常常是同一件事，比如「想做操的时候别乱」「想借书的时候书在」。第四步，定一个能试的办法，并且说清楚先试多久、谁来做。第五步，过一段时间回来看效果，不行就再商量一次。第五步最容易被忘掉，可它最要紧——办法是试出来的，不是一次就定死的。判断一个办法好不好，看三条：能不能解决大家的问题、能不能做到、有没有照顾到少数同学。这里有两个最容易搞混的地方。第一个，把「商量」搞混成「听谁的嗓门大」，或者「谁先说就听谁的」，可商量要的是把理由讲出来。第二个，误认为「少数服从多数就够了」，可班上总有值日赶不上、眼睛不舒服、家里有事的同学，办法里给他们留一条路，才算真的解决大家的问题。还有一件事要记住：班规是大家一起定的，也要大家一起守；自己定的规矩自己先做到，才叫班级的主人。班会上也可以一起商量「哪些事我们不做」——比如不玩有危险的游戏，遇到有人在校外递烟，及时告诉老师和家里人。保护好自己，也是主人该做的一件事。",
    "lab-2": "接下来我们搭一次议事流程。下面有五张步骤卡，顺序被打乱了。请你按正确的先后顺序一张一张点下去：点对了，它就会排进「我们班的议事五步」；点错了，我会告诉你这一步该放在哪儿想。五张都排好，流程图就出来了。",
    "worked-example": "我们一起来看五(2)班的一次改选。新学期要改选班委，小雨想当体育委员，小航也想当。有同学说，两个都是我好朋友，投谁好呢；还有同学说，反正我不当，选谁都一样。第一步，先看清楚这个岗位要做什么：体育委员要组织大家做操、管体育器材借还、帮体育老师收表。第二步，听两个人说打算：小雨说，我想每周三放学后带大家练一次跳绳；小航说，我想做一本器材借还本，谁借谁还都记上。第三步，大家提问，他们当场回答：有人问小雨，星期三有同学要值日怎么办；有人问小航，本子谁来记。两个人都把自己的办法说清楚了。第四步，一人一票，投给自己认为合适的人。不看谁关系好，看谁的打算更靠谱、谁平时更愿意做事。第五步，结果公布：小雨当选。可小航并没有没事做——他把那本器材借还本做了起来，交给体育委员一起用。班级的事，谁都能出力。这里有一个常见错误要提醒：有的同学误认为「选班委就是看平时关系好不好」，可真正该看的是「他打算怎么做、平时做得怎么样」。想清楚这一点，你手里那一票就不再是随手一投了。",
    "conceptest-1": "接下来用三个说法考考你，每个说法里都藏着一个容易想歪的地方。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件任务交给你，请你当一次提提案的人。下面分三步：先选一个你想提的问题，再选一个你打算怎么试的办法，最后选一个怎么知道有没有用的办法。三步选完，我会把它们拼成一份提案，你可以直接念给班委听。",
    "posttest": "最后一轮，换几个新情境来考考你。这次会遇到改选时拉票、值日表和校外的烟，看看今天学的办法还用不用得上。",
    "summary": "这节课我们弄清楚两件事。第一件，班委会的成员由全班同学选举产生，选举时要先看岗位要做什么、再听他打算怎么做、最后看他平时做得怎么样；一人一票，选上的人认真做，没选上的人也能继续出力。第二件，班级的事协商着定，五个步骤是：把问题说清楚、每人说想法和理由、找共同点、定一个能试的办法、过一段时间回来看效果再调整；判断办法好不好，看能不能解决问题、能不能做到、有没有照顾到少数同学。最后记住一句话：班规是大家一起定的，也要大家一起守；自己定的规矩自己先做到，才叫班级的主人。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出班委会是什么、它的成员是怎么产生的；再写出选举时要看清的三件事。第二层能力应用，动手做：观察这一周班里的一个班务问题，按议事五步写一份简短的议事记录，写清楚问题是什么、大家提了哪些办法、最后定了什么。第三层迁移挑战，选做：为班级写一份提案，说清楚你想解决什么问题、打算怎么试、试多久、请谁记录，写完念给班委或者班会课上讲一遍，再说说听完以后大家提了什么意见。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 班委会由全班选举产生", "lab-1": "动手一 班务议事台",
    "module-2": "概念二 班级事务协商着定", "lab-2": "动手二 议事五步搭建台",
    "worked-example": "例题示范 五(2)班的一次改选", "conceptest-1": "概念测试",
    "synthesis": "综合任务 我的班级提案生成台", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：班务议事台（4 个真实班务问题 × 每个 3 个处理办法） ──
ISSUES = [
    {"id": "i1",
     "title": "问题一 · 课间太吵",
     "scene": "课间教室里特别吵，隔壁班来提了意见；午休的时候也静不下来，好几个同学睡不了。",
     "opts": [
         {"t": "班委会直接定一条：以后课间谁都不许说话。", "ok": False,
          "out": "第一天还算安静，第二天就有人偷偷说，第三天没人当回事——这条规定做不到，也没人愿意守。",
          "who": "想聊天、想活动一下的同学最难受，守在教室里反而更憋。",
          "tip": "还可以试试：先问问大家课间最想做什么，是想聊天、没地方玩，还是下课时间太短。"},
         {"t": "把问题摆到班会课上，大家说说课间最想做什么，再一起定一两条做得到的办法，比如走廊说话小点声、教室留一个安静角落。", "ok": True,
          "out": "办法是大家一起定的，守起来才顺；而且能顺着大家的需要想，比一味禁止管用。",
          "who": "想安静的同学有了角落，想说话的同学也不必憋着。",
          "tip": "还可以试试：先试两周，看看午休是不是真的静下来了。"},
         {"t": "先不管它，反正隔壁班说说而已。", "ok": False,
          "out": "声音越来越大，午休睡不着的同学越来越多，下一次提意见的可能就是自己班的同学。",
          "who": "被吵到的同学最受影响，可他们往往不吭声。",
          "tip": "还可以试试：先看看这件事影响到了谁，再决定要不要提。"},
     ]},
    {"id": "i2",
     "title": "问题二 · 图书角乱了",
     "scene": "图书角的书乱堆着，有的书找不到，这个月还弄丢了两本。",
     "opts": [
         {"t": "一起商量：做一本借还本，每排一位同学轮值，先试两周。", "ok": True,
          "out": "借还有了记录，轮值的人也知道自己要做什么；两周以后看效果，不行再改。",
          "who": "爱看书的同学知道该找谁借，轮值的同学也不至于一个人忙。",
          "tip": "还可以试试：把「怎么借、怎么还、弄丢了怎么办」先一起说清楚。"},
         {"t": "把图书角锁起来，以后谁都不许借。", "ok": False,
          "out": "书是不丢了，可图书角也没人用了——本来是为大家办的事，变成了摆设。",
          "who": "想借书的同学最失望，做这个角的同学也觉得白费了力气。",
          "tip": "还可以试试：先想一想书为什么会丢——是没人记，还是借了忘了还。"},
         {"t": "让弄丢书的同学赔两本，这件事就算过去了。", "ok": False,
          "out": "这一件是解决了，可下次还会丢，因为没人知道该找谁借、找谁还。",
          "who": "赔了书的同学心里可能不服气，别的同学也没学到怎么管书。",
          "tip": "还可以试试：把「怎么借、怎么还」先说清楚，再谈丢了怎么办。"},
     ]},
    {"id": "i3",
     "title": "问题三 · 值日分工不均",
     "scene": "值日总是那几个人做得最多，有同学常常铃一响就先走了。",
     "opts": [
         {"t": "谁也不提，多做的人继续多做。", "ok": False,
          "out": "做得多的同学越来越委屈，到最后连他们也不想做了，值日只会越来越差。",
          "who": "一直是那几个人在受影响，可他们不好意思开口。",
          "tip": "还可以试试：把「我觉得不太公平」说出来，这不是打小报告。"},
         {"t": "把先走的同学的名字写在黑板上，让大家看看。", "ok": False,
          "out": "被点名的同学很委屈，其他人也不敢再说话，下一次还是老样子。",
          "who": "被点名的同学最难受，而且他们可能真有赶不及的原因。",
          "tip": "还可以试试：先问一问他们为什么总赶不上，再想怎么排班。"},
         {"t": "一起商量重新排班：把任务写成一张表，按周轮换，请假的人自己找一位同学换，换完在表上写一句。", "ok": True,
          "out": "谁做什么一目了然，有困难的也能换，不用互相埋怨；两周后回来看表就知道有没有变好。",
          "who": "一直多做的同学轻松了，有事的同学也有了出路。",
          "tip": "还可以试试：把「换班要提前说一声」也写进表里。"},
     ]},
    {"id": "i4",
     "title": "问题四 · 校外有人递烟",
     "scene": "有同学在校外被高年级的人递了烟，还被叫上另外两个同学一起去那个地方。",
     "opts": [
         {"t": "让被递烟的那位同学自己去解决，别把别人牵连进来。", "ok": False,
          "out": "他一个人扛着，很可能下一次又被叫去，也不敢跟任何人说。",
          "who": "最需要帮助的那位同学，反而成了最没有人帮的那个。",
          "tip": "还可以试试：把这件事告诉老师和家里人，有人一起管才更安全。"},
         {"t": "把这件事告诉老师和家里人，同时在班会上商量：遇到这种事我们怎么办，班上定一句一致的说法。", "ok": True,
          "out": "先离开那个地方、再让大人知道，事情就不只是他一个人的事了；班上有了统一说法，谁碰到都知道怎么应对。",
          "who": "被叫去的同学不再孤立，其他人也知道该怎么保护自己。",
          "tip": "还可以试试：在班会上把「不去那个地方、说一句就走开、回来告诉老师」写成一致的说法。"},
         {"t": "让班上同学以后都不许去那一带，谁去就告诉家长。", "ok": False,
          "out": "一刀切的禁令做不到，也没解决问题；真正要练的是「碰到了怎么办」。",
          "who": "住在那附近的同学最不方便，还容易被误会。",
          "tip": "还可以试试：把问题说清楚——我们要解决的不是「去哪儿」，而是「遇到递烟怎么办」。"},
     ]},
]

# ── 动手二：议事五步搭建台（步骤打乱，按顺序点） ──
STEPS5 = [
    {"k": "st1", "n": "把问题说清楚", "d": "到底是什么事、影响到了谁，先说明白。"},
    {"k": "st2", "n": "每人说想法和理由", "d": "别人说的时候不打断，一个人一个人来。"},
    {"k": "st3", "n": "找共同点", "d": "说来说去，大家最在意的常常是同一件事。"},
    {"k": "st4", "n": "定一个能试的办法", "d": "说清楚先试多久、谁来做这件事。"},
    {"k": "st5", "n": "过一段时间回来看效果", "d": "不行就再商量一次——办法是试出来的。"},
]
STEPS_SHUFFLED = ["st3", "st5", "st1", "st4", "st2"]

# ── 综合任务：我的班级提案生成台 ──
PROPOSAL = {
    "problems": [
        {"k": "q1", "n": "课间教室里太吵，午休也静不下来",
         "opts": [
             {"t": "定一条「课间不许说话」，谁说话就记名字。", "ok": False},
             {"t": "先问问大家课间最想做什么，再一起定一两条做得到的办法，比如走廊说话小点声、教室留一个安静角落。", "ok": True},
             {"t": "上课时批评全班一顿，让大家知道这件事很严重。", "ok": False},
         ]},
        {"k": "q2", "n": "图书角的书乱放，还弄丢了两本",
         "opts": [
             {"t": "把图书角锁起来，以后谁都不许借。", "ok": False},
             {"t": "一起做一本借还本，每排一位同学轮值，借还都记上一句。", "ok": True},
             {"t": "让弄丢书的同学赔两本，这件事就算过去了。", "ok": False},
         ]},
        {"k": "q3", "n": "值日分工不均，总是几个人做得最多",
         "opts": [
             {"t": "把先走的同学的名字写在黑板上。", "ok": False},
             {"t": "把任务写成一张表，按周轮换，请假的人自己找同学换并在表上写一句。", "ok": True},
             {"t": "谁也不提，多做的人继续多做。", "ok": False},
         ]},
        {"k": "q4", "n": "有同学在校外被递烟，还被叫上别人一起去",
         "opts": [
             {"t": "让被递烟的同学自己解决，别牵连别人。", "ok": False},
             {"t": "把这件事告诉老师和家里人，再在班会上定一句一致的说法：不去那个地方、说一句就走开、回来告诉老师。", "ok": True},
             {"t": "全班以后都不许去那一带，谁去就告诉家长。", "ok": False},
         ]},
    ],
    "checks": [
        {"t": "试完就算了，不用回头看。", "ok": False},
        {"t": "先试两周，由值日班长把情况记在一张纸上，班会课上念一遍，看有没有变好；不行就再商量。", "ok": True},
        {"t": "谁没做到就把名字记下来，交给老师。", "ok": False},
    ],
}

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g5-u2 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 班务议事台：4 个班务问题 × 每个 3 个处理办法 → 执行后果 + 谁受影响 + 还可以试试
   3) 议事五步搭建台：打乱的步骤卡按顺序点 → 生成「我们班的议事五步」
   4) 我的班级提案生成台：选问题 → 选办法 → 选怎么试 → 合成一份提案
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

  /* ---------- 2. 班务议事台 ---------- */
  var ISSUES = __ISSUES_JSON__;
  var stage1 = document.getElementById('bw-stage');
  if (stage1) {
    var curIssue = null, picked = {};
    var out1 = document.getElementById('bw-out');
    var panel = document.getElementById('bw-panel');
    function issueById(id) {
      for (var i = 0; i < ISSUES.length; i++) { if (ISSUES[i].id === id) return ISSUES[i]; }
      return null;
    }
    function render1() {
      document.querySelectorAll('[data-bw-issue]').forEach(function (b) {
        var k = b.dataset.bwIssue;
        b.classList.toggle('selected', k === curIssue);
        b.classList.toggle('done', !!picked[k]);
      });
      document.getElementById('bw-score').textContent =
        '已经议过 ' + Object.keys(picked).length + ' / ' + ISSUES.length + ' 个问题';
      if (!curIssue) { panel.innerHTML = ''; return; }
      var I = issueById(curIssue);
      var html = '<div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">' +
        '<p style="margin:0"><strong>' + I.title + '</strong>：' + I.scene + '</p></div>';
      html += '<div style="font-weight:700;font-size:14px;margin:14px 0 0">班委会打算这么办，你选一个</div>';
      html += '<div class="grid" style="margin-top:10px">';
      I.opts.forEach(function (o, i) {
        var cls = 'choice';
        if (picked[I.id] === i) cls += o.ok ? ' correct' : ' wrong';
        html += '<button class="' + cls + '" data-bw-opt="' + i + '" style="text-align:left">' + o.t + '</button>';
      });
      html += '</div>';
      panel.innerHTML = html;
      panel.querySelectorAll('[data-bw-opt]').forEach(function (b) {
        b.addEventListener('click', function () { chooseOpt(parseInt(b.dataset.bwOpt, 10)); });
      });
    }
    function chooseOpt(i) {
      var I = issueById(curIssue);
      var o = I.opts[i];
      picked[I.id] = i;
      out1.className = 'result' + (o.ok ? '' : ' warn');
      out1.innerHTML = '<strong>你们打算这么办：' + o.t + '</strong><br>' +
        '<strong>' + (o.ok ? '这样可能会更好：' : '这样可能会：') + '</strong>' + o.out +
        '<br><span style="color:var(--muted)"><strong>谁会受影响：</strong>' + o.who + '</span>' +
        '<br><span style="color:var(--muted)">' + o.tip + '</span>';
      render1();
      if (Object.keys(picked).length === ISSUES.length) {
        out1.className = 'result';
        out1.innerHTML += '<br><br><strong>四个问题都议过了！</strong>你会发现，走得通的办法大多做了同一件事：' +
          '先把问题说清楚，再想一个大家做得到的办法，最后留一步回头看。';
      }
    }
    document.querySelectorAll('[data-bw-issue]').forEach(function (b) {
      b.addEventListener('click', function () {
        curIssue = b.dataset.bwIssue;
        out1.className = 'result warn';
        out1.innerHTML = '<strong>' + issueById(curIssue).scene + '</strong><br>想一想班里该怎么办，再点下面三个办法里的一个。';
        render1();
      });
    });
    render1();
  }

  /* ---------- 3. 议事五步搭建台 ---------- */
  var STEPS5 = __STEPS5_JSON__;
  var stage2 = document.getElementById('fl-stage');
  if (stage2) {
    var placed = [];
    var out2 = document.getElementById('fl-out');
    var flow = document.getElementById('fl-flow');
    function stepByKey(k) {
      for (var i = 0; i < STEPS5.length; i++) { if (STEPS5[i].k === k) return STEPS5[i]; }
      return null;
    }
    function render2() {
      document.querySelectorAll('[data-fl-step]').forEach(function (b) {
        b.classList.toggle('done', placed.indexOf(b.dataset.flStep) >= 0);
        b.disabled = placed.indexOf(b.dataset.flStep) >= 0;
      });
      document.getElementById('fl-score').textContent = '已经排好 ' + placed.length + ' / ' + STEPS5.length + ' 步';
      flow.innerHTML = '';
      if (!placed.length) {
        flow.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有排好的步骤。</span>';
        return;
      }
      placed.forEach(function (k, i) {
        var S = stepByKey(k);
        var d = document.createElement('div');
        d.className = 'tag';
        d.textContent = '第' + (i + 1) + '步 · ' + S.n;
        flow.appendChild(d);
      });
    }
    document.querySelectorAll('[data-fl-step]').forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.dataset.flStep;
        var want = STEPS5[placed.length].k;
        if (k === want) {
          placed.push(k);
          var S = stepByKey(k);
          out2.className = 'result';
          out2.innerHTML = '<strong>排对了：第' + placed.length + '步是「' + S.n + '」。</strong>' + S.d;
          render2();
          if (placed.length === STEPS5.length) {
            out2.className = 'result';
            out2.innerHTML = '<strong>五步都排好了，这就是「我们班的议事五步」：</strong>' +
              '把问题说清楚 → 每人说想法和理由 → 找共同点 → 定一个能试的办法 → 过一段时间回来看效果再调整。' +
              '<br><span style="color:var(--muted)">记住：第五步最容易被忘掉，可办法是试出来的，不是一次就定死的。</span>';
          }
        } else {
          var S2 = stepByKey(k);
          out2.className = 'result warn';
          out2.innerHTML = '<strong>这一步现在还不到时候。</strong>「' + S2.n + '」要解决的是：' + S2.d +
            '<br><span style="color:var(--muted)">这样可能会：顺序一乱，前一步还没说清楚，后面就定不下来。' +
            '还可以试试：先想一想，现在最需要先弄明白的是什么。</span>';
        }
      });
    });
    render2();
  }

  /* ---------- 4. 我的班级提案生成台 ---------- */
  var PROPOSAL = __PROPOSAL_JSON__;
  var stage3 = document.getElementById('pp-stage');
  if (stage3) {
    var pick = { problem: null, plan: null, check: null };
    var out3 = document.getElementById('pp-out');
    var panel3 = document.getElementById('pp-panel');
    var card3 = document.getElementById('pp-card');
    function problemByKey(k) {
      for (var i = 0; i < PROPOSAL.problems.length; i++) {
        if (PROPOSAL.problems[i].k === k) return PROPOSAL.problems[i];
      }
      return null;
    }
    function render3() {
      var html = '<div style="font-weight:700;font-size:14px;margin-bottom:6px">第一步 · 我想提的问题是</div><div class="grid grid-2">';
      PROPOSAL.problems.forEach(function (P) {
        html += '<button class="choice' + (pick.problem === P.k ? ' selected' : '') +
          '" data-pp-problem="' + P.k + '" style="text-align:left">' + P.n + '</button>';
      });
      html += '</div>';
      if (pick.problem) {
        var P = problemByKey(pick.problem);
        html += '<div style="font-weight:700;font-size:14px;margin:16px 0 6px">第二步 · 我打算这样试</div><div class="grid">';
        P.opts.forEach(function (o, i) {
          var cls = 'choice';
          if (pick.plan === i) cls += o.ok ? ' correct' : ' wrong';
          html += '<button class="' + cls + '" data-pp-plan="' + i + '" style="text-align:left">' + o.t + '</button>';
        });
        html += '</div>';
      }
      html += '<div style="font-weight:700;font-size:14px;margin:16px 0 6px">第三步 · 怎么知道有没有用</div><div class="grid">';
      PROPOSAL.checks.forEach(function (c, i) {
        var cls = 'choice';
        if (pick.check === i) cls += c.ok ? ' correct' : ' wrong';
        html += '<button class="' + cls + '" data-pp-check="' + i + '" style="text-align:left">' + c.t + '</button>';
      });
      html += '</div>';
      panel3.innerHTML = html;
      panel3.querySelectorAll('[data-pp-problem]').forEach(function (b) {
        b.addEventListener('click', function () {
          pick.problem = b.dataset.ppProblem; pick.plan = null; render3();
          out3.className = 'result warn';
          out3.textContent = '问题选好了，再想一个你打算怎么试的办法。';
        });
      });
      panel3.querySelectorAll('[data-pp-plan]').forEach(function (b) {
        b.addEventListener('click', function () {
          pick.plan = parseInt(b.dataset.ppPlan, 10);
          out3.className = 'result warn';
          out3.textContent = '办法选好了，最后想想怎么知道有没有用。';
          render3();
        });
      });
      panel3.querySelectorAll('[data-pp-check]').forEach(function (b) {
        b.addEventListener('click', function () {
          pick.check = parseInt(b.dataset.ppCheck, 10);
          render3();
          if (pick.problem === null || pick.plan === null) {
            out3.className = 'result warn';
            out3.textContent = '三步还没选完，先把前面的补齐。';
            return;
          }
          var P = problemByKey(pick.problem);
          var plan = P.opts[pick.plan];
          var chk = PROPOSAL.checks[pick.check];
          card3.style.display = 'block';
          var okN = (plan.ok ? 1 : 0) + (chk.ok ? 1 : 0);
          out3.className = 'result' + (okN === 2 ? '' : ' warn');
          out3.innerHTML = '<strong>你的提案：</strong>关于「' + P.n + '」，我们打算' + plan.t +
            '先试两周，' + chk.t +
            '<br><span style="color:var(--muted)">' +
            (okN === 2
              ? '这两步都选得稳：办法做得到，也留了回头看的余地。可以把它念给班委听，或者放在班会课上一起议。'
              : '还可以再想一想：办法要能解决大家的问题、也能做得到；而且要留一步回头看。换一个再试一次。') +
            '</span>';
        });
      });
    }
    render3();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__ISSUES_JSON__', json.dumps(ISSUES, ensure_ascii=False))
             .replace('__STEPS5_JSON__', json.dumps(STEPS5, ensure_ascii=False))
             .replace('__PROPOSAL_JSON__', json.dumps(PROPOSAL, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：班级的事，谁说了算？", TTS["pretest"], [
        {"q": "班委会的成员是怎么产生的？",
         "options": [("由全班同学选举产生", True),
                     ("由老师直接指定", False),
                     ("谁想当谁就能当", False)],
         "explain": "班委会是班级里由同学们推选出来、为大家服务的一小组人，成员由全班同学选举产生。"
                    "<strong>错因提醒：</strong>常见错误是误认为「班委是老师安排好的」——"
                    "选举的意思，就是这件事由全班同学一起定。"},
        {"q": "改选班委的时候，下面哪种做法更合适？",
         "options": [("先看他打算怎么做、平时做得怎么样，再投出自己的一票", True),
                     ("谁跟我关系好就投谁", False),
                     ("反正我不当，投不投都一样", False)],
         "explain": "班委是替全班做事的，要选的是能把事做好的人；你的一票也在决定这个班以后怎么样。"
                    "<strong>错因提醒：</strong>容易把「关系好」误认为「合适」——"
                    "关系好不好是一回事，能不能把事做好是另一回事。"},
        {"q": "班里想解决「课间太吵」，下面哪种做法最可能真的管用？",
         "options": [("把问题摆到班会课上，大家说说原因，再一起定一两条做得到的办法，先试两周", True),
                     ("直接定一条「以后课间谁都不许说话」", False),
                     ("先不管，等别的班再提意见再说", False)],
         "explain": "一起商量出来的办法，大家才愿意守；先试一段时间，才知道管不管用。"
                    "<strong>错因提醒：</strong>有的同学误认为「规定越严越管用」——"
                    "做不到的规定，第一天之后就成了纸上的字。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "班委会由全班选举产生：先看岗位，再听打算，后投一票", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们每天都在班里上课、值日、借书，班里的日子好不好过，其实和每个人都有关系（And）；可一到改选班委，不少同学要么只看关系好不好，要么觉得「反正我不当，选谁都一样」（But）；所以这节课先弄清楚班委是怎么选出来的，再学会把班里的事一起商量着定（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px"><strong>班委会</strong>是指班级里由同学们推选出来、为大家服务的一小组人，比如班长、学习委员、体育委员、劳动委员。它的成员由<strong>全班同学选举产生</strong>。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先看岗位要做什么。</strong>体育委员要组织做操、管器材借还；劳动委员要排值日、看卫生。岗位干什么都不清楚，投票就是凭印象。</div></div>
          <div class="step"><span class="n">2</span><div><strong>再听他打算怎么做。</strong>愿意做的同学讲一讲打算，大家提问，他当场回答。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>最后看他平时做得怎么样。</strong>说过的话有没有做到，是最实在的一票。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="班委会选举流程示意图：先看岗位要做什么、再听竞选打算、一人一票投出结果、选上认真做没选上也能出力，附中文标注">
          <figcaption>概念图：选举产生班委会的过程 · 一人一票，选上的人认真做，没选上的人也能继续出力</figcaption>
        </figure>
        <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(78,205,196,.45)">
          <p><strong>一句可以随身带的话</strong></p>
          <p style="color:var(--muted)">先看岗位、再听打算、后投一票；<strong>选上的人认真做，没选上的人也能继续出力。</strong></p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「选班委就是看平时关系好不好」。可班委是替全班做事的，要看的是他打算怎么做、平时做得怎么样；<strong>关系好不好是一回事，能不能把事做好是另一回事。</strong></p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "同样是一票，一票是「他跟我玩得好」，一票是「他的办法我听得明白」，两票投出去，班里的日子会很不一样。"},
    {"lens": "解释它", "text": "为什么要先看岗位再投票？因为班委不是一个荣誉称号，而是一件具体的事；知道了要做什么，才知道谁合适。"},
    {"lens": "迁移它", "text": "这套看法在家里、在小组里也一样：要交给别人一件事，先看这件事要做什么，再看他愿不愿意做、做起来靠不靠得住。"},
])}
    ''', tag="概念一"))

    issue_btns = "\n".join(
        f'            <button class="choice" data-bw-issue="{it["id"]}" style="text-align:left">'
        f'<strong>{it["title"]}</strong><br><span style="color:var(--muted);font-size:14px">{it["scene"]}</span></button>'
        for it in ISSUES
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：班务议事台，这件事班里该怎么办？", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">点开一个班务问题，从三个办法里选一个。选完会告诉你<strong>执行下去会发生什么、谁会受影响</strong>，还有一个别的思路。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 挑一个班务问题</div>
          <div id="bw-stage">
            <div class="grid">
{issue_btns}
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">议事进度</span><span class="v" id="bw-score">已经议过 0 / 4 个问题</span></div>
          </div>
          <p class="result warn" id="bw-out" style="margin-top:12px">先点一个班务问题。</p>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 班委会打算这么办</div>
          <div id="bw-panel"></div>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🪑</span><div><strong>议完回头看：</strong>四个问题里，哪几个办法有一个共同点？它们都先把问题说清楚了，也都留了一步「回头看看」。这两点，就是班级议事最重要的地方。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "班级事务协商着定：摆问题、说想法、找共同点、定试行、回头看", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px"><strong>协商</strong>是指把问题摆到桌面上，每个人把自己想到的办法<strong>提出</strong>来、把理由说清楚，一起找一个大家都愿意试一试的方案。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>把问题说清楚：</strong>到底是什么事、影响到了谁。</div></div>
          <div class="step"><span class="n">2</span><div><strong>每人说想法和理由：</strong>别人说的时候不打断，一个人一个人来。</div></div>
          <div class="step"><span class="n">3</span><div><strong>找共同点：</strong>说来说去，大家最在意的常常是同一件事。</div></div>
          <div class="step"><span class="n">4</span><div><strong>定一个能试的办法：</strong>说清楚先试多久、谁来做这件事。</div></div>
          <div class="step"><span class="n green">5</span><div><strong>过一段时间回来看效果：</strong>不行就再商量一次。办法是试出来的，不是一次就定死的。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="协商决定班级事务的五步示意图：把问题说清楚、每人说想法、找共同点、定一个能试的办法、过一段时间回来看效果，附中文标注">
          <figcaption>概念图：协商决定班级事务的五步 · 判断办法好不好，看能不能解决、能不能做到、有没有照顾到少数同学</figcaption>
        </figure>
        <div class="inner-card">
          <p><strong>判断一个办法好不好，看三条</strong></p>
          <p style="color:var(--muted)">能不能解决大家的问题；能不能做到，人手和时间够不够；有没有照顾到少数同学——总有值日赶不上、家里有事的同学，办法里给他们留一条路，才算真的解决大家的问题。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学把「商量」<strong>搞混</strong>成「听谁的嗓门大」，或者误认为「少数服从多数就够了」。商量要的是把理由讲出来；<strong>只靠「罚站」「不许上体育课」这类办法，大家守规矩是因为怕，不是因为明白了为什么。</strong></p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "同样是「安静一点」，一条是「谁说话就记名字」，一条是「走廊说话小点声，教室留个安静角落」——后一条大家愿意守，因为它照顾到了想说话的人。"},
    {"lens": "解释它", "text": "为什么一定要留第五步「回头看」？因为定办法的时候，谁也不知道它到底管不管用；试过再看，办法才越改越对。"},
    {"lens": "迁移它", "text": "班级公约里也可以一起商量「哪些事我们不做」：不玩有危险的游戏，遇到有人在校外递烟，及时告诉老师和家里人——保护好自己，也是主人该做的一件事。"},
])}
    ''', tag="概念二"))

    _step_name = {s["k"]: s["n"] for s in STEPS5}
    shuffled_btns = "\n".join(
        f'            <button class="choice" data-fl-step="{k}" style="text-align:left">'
        f'{i}. {_step_name[k]}</button>'
        for i, k in enumerate(STEPS_SHUFFLED, 1)
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：议事五步搭建台，把顺序排出来", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">下面五张步骤卡是打乱的。按正确的先后顺序一张一张点下去：点对了就排进流程图，点错了会告诉你这一步该在哪儿想。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 打乱的步骤卡（点你认为该在最前面的那一张）</div>
          <div id="fl-stage">
            <div class="grid">
{shuffled_btns}
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">搭建进度</span><span class="v" id="fl-score">已经排好 0 / 5 步</span></div>
          </div>
          <p class="result warn" id="fl-out" style="margin-top:12px">先点一张步骤卡。</p>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 我们班的议事五步</div>
          <div class="sort-bank" id="fl-flow"><span style="color:var(--muted);font-size:14px">还没有排好的步骤。</span></div>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧩</span><div><strong>排完想一想：</strong>哪一步最容易被跳过？多半是最后一步「回来看效果」。可要是省了它，我们永远不知道办法到底管不管用。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：五(2)班的一次改选", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>新学期要改选班委，小雨想当体育委员，小航也想当。有同学说，两个都是我好朋友，投谁好呢；还有同学说，反正我不当，选谁都一样。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先看清楚岗位要做什么：</strong>体育委员要组织大家做操、管体育器材借还、帮体育老师收表。</div></div>
          <div class="step"><span class="n">2</span><div><strong>听两个人说打算：</strong>小雨说，我想每周三放学后带大家练一次跳绳；小航说，我想做一本器材借还本，谁借谁还都记上。</div></div>
          <div class="step"><span class="n">3</span><div><strong>大家提问，他们当场回答：</strong>有人问小雨，星期三有同学要值日怎么办；有人问小航，本子谁来记。两个人都把自己的办法说清楚了。</div></div>
          <div class="step"><span class="n">4</span><div><strong>一人一票，投给自己认为合适的人：</strong>不看谁关系好，看谁的打算更靠谱、谁平时更愿意做事。</div></div>
          <div class="step"><span class="n green">5</span><div><strong>结果公布之后：</strong>小雨当选。可小航并没有没事做——他把那本器材借还本做了起来，交给体育委员一起用。班级的事，谁都能出力。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「选班委就是看平时关系好不好」，可真正该看的是「他打算怎么做、平时做得怎么样」。想清楚这一点，你手里那一票就不再是随手一投了。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "关于班委会的选举，下面哪句话说得对？",
         "options": [("先看这个岗位要做什么，再听他打算怎么做，最后看他平时做得怎么样", True),
                     ("谁平时跟我关系好，我就投谁", False),
                     ("班委是老师定的，投票只是走个过场", False)],
         "explain": "班委是替全班做事的，选举就是把这件事交给全班一起定；要看的是他打算怎么做、做起来靠不靠得住。"
                    "<strong>错因提醒：</strong>常见错误是误认为「关系好就合适」——"
                    "关系好不好是一回事，能不能把事做好是另一回事。"},
        {"q": "班里想解决「图书角乱了、还丢书」，下面哪种做法更好？",
         "options": [("一起商量出一本借还本和轮值办法，先试两周再看效果", True),
                     ("把图书角锁起来，谁都不许借", False),
                     ("让弄丢书的同学赔两本就算了", False)],
         "explain": "商量出来的办法既解决借还，又留了一步回头看；锁起来是把问题藏起来，赔书只解决了这一件。"
                    "<strong>错因提醒：</strong>容易把「不出事」误认为「解决了问题」——"
                    "书不丢，可图书角也没人用了。"},
        {"q": "关于班级议事，下面哪句话说得对？",
         "options": [("把问题说清楚，每人说想法和理由，定了办法先试一段时间，再回来看效果", True),
                     ("商量就是听谁的嗓门大，谁先说听谁的", False),
                     ("少数服从多数就够了，不用管少数同学", False)],
         "explain": "商量要的是把理由讲出来；办法定完还要试、还要看，才能越改越对。"
                    "<strong>错因提醒：</strong>有的同学把「商量」搞混成「谁声音大谁说了算」——"
                    "总有值日赶不上、家里有事的同学，办法里给他们留一条路，才算真的解决大家的问题。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：我的班级提案生成台", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">三步各选一个：<strong>我想提的问题是 → 我打算这样试 → 怎么知道有没有用</strong>。选完，我会把它拼成一份可以念给班委听的提案。</p>
        <div class="lab-panel">
          <div id="pp-stage"></div>
          <div id="pp-panel"></div>
          <p class="result warn" id="pp-out" style="margin-top:12px">从第一步开始选。</p>
          <div class="inner-card" id="pp-card" style="display:none;background:var(--accent-soft);border-color:rgba(78,205,196,.45)">
            <p style="margin:0"><strong>提案写好了，请念一遍给班委或者同桌听。</strong>听完以后问一句：这个办法做得到吗？还有谁没被照顾到？</p>
          </div>
        </div>
        <div class="inner-card" style="margin-top:14px">
          <p><strong>把它写下来：</strong></p>
          <p style="color:var(--muted)">如果给你一次在班会课上发言的机会，你最想为班里提哪一件事？试着自己设计一条班级小约定，写清楚问题和你的办法。</p>
          <textarea id="syn-answer" rows="3" placeholder="我想提的是……，我打算……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，办法还在不在", TTS["posttest"], [
        {"q": "改选的时候，有同学在班里挨个说：你投我，下次我也帮你。下面哪种看法更合适？",
         "options": [("投票要看谁适合这个岗位，不能拿票换来换去", True),
                     ("他既然答应了帮我，那投他一票也没什么", False),
                     ("反正我不当，怎么投都行", False)],
         "explain": "选班委是把班级的事交给人做，判断的标准是「他适不适合、做不做得来」。"
                    "<strong>错因提醒：</strong>常见错误是误认为「投票是私人的事，人情往来很正常」——"
                    "可这一票关系到全班以后的日子。"},
        {"q": "值日表排出来以后，有同学说自己放学要去接弟弟，总赶不上。下面哪种做法更好？",
         "options": [("在排班表上给他换一个时间段，或者让他和别人换，换完在表上写一句", True),
                     ("规定就是规定，赶不上也要值完", False),
                     ("把他的名字写在黑板上，让大家看看", False)],
         "explain": "办法要照顾到少数同学，换一换并不影响值日这件事本身；写清楚换班记录，也不用互相埋怨。"
                    "<strong>错因提醒：</strong>有的同学误认为「讲情面就是不公平」——"
                    "能让每个人做得到的安排，才是真的公平。"},
        {"q": "班上有人在校外被递烟，还被叫上别人一起去。作为班级的一员，下面哪种做法更好？",
         "options": [("不去那个地方，及时把这件事告诉老师和家里人，并和同学一起商量碰到时怎么办", True),
                     ("能躲就躲，别把这件事说出去", False),
                     ("自己一个人去找那个人讲道理", False)],
         "explain": "先离开、再让大人知道，同时让班上有一句一致的说法，谁碰到都知道怎么应对。"
                    "<strong>错因提醒：</strong>容易把「不说就是帮朋友」误认为「保护朋友」——"
                    "瞒着不说，下一次受影响的可能还是他。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：班委怎么选，班里的事怎么定", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>班委怎么选：</strong>班委会的成员由全班同学选举产生；先看岗位要做什么，再听他打算怎么做，最后看他平时做得怎么样。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>班里的事怎么定：</strong>协商的五个步骤——把问题说清楚、每人说想法和理由、找共同点、定一个能试的办法、过一段时间回来看效果再调整。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>办法好不好看三条：</strong>能不能解决大家的问题、能不能做到、有没有照顾到少数同学。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>每个人都能出力：</strong>选上的人认真做，没选上的人也能继续出力；班级公约里也可以一起商量「哪些事我们不做」。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>一句口诀：</strong>先看岗位、再听打算、后投一票；摆问题、说想法、找共同点、定试行、回头看。班规是大家一起定的，也要大家一起守。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「选举」「协商」这两个词，给家里人讲一件最近班里定下来的事，并说说这件事是怎么定下来的。</p>
          <p style="color:var(--muted)">再动一动手：<strong>写一写</strong>你打算为班级做的一件小事，写清楚做什么、什么时候做、怎么知道做好了。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写出班委会是什么，它的成员是怎么产生的。",
            "写出选举班委时要看清的三件事。",
            "写出协商决定班级事务的五个步骤。",
        ],
        [
            "观察这一周班里的一个班务问题，按议事五步写一份简短的议事记录：问题是什么、大家提了哪些办法、最后定了什么。",
            "和小组同学一起，为小组定一条大家都能做到的小约定，写清楚试多久、谁来做、怎么知道有没有用。",
        ],
        [
            "为班级写一份提案，说清楚你想解决什么问题、打算怎么试、试多久、请谁记录；写完念给班委或者班会课上讲一遍，再说说听完以后大家提了什么意见。",
            "采访一位班委，问问他这学期最想做的一件事是什么、做起来最难的地方在哪里，把回答整理成三句话。",
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
    "title": "我们是班级的主人",
    "name_en": "We Are the Masters of Our Class",
    "grade": 5,
    "grade_cn": "五年级",
    "domain": "tradition-culture",
    "domain_cn": "中华优秀传统文化",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学五年级的道德与法治课，正对统编五上第 2 单元「我们是班级的主人」，落到两件学生最常碰到的事上。一是「选举产生班委会」：班委会是指班级里由同学们推选出来、为大家服务的一小组人，成员由全班同学选举产生；选举要看清三件事——先看这个岗位要做什么、再听他打算怎么做、最后看他平时做得怎么样；一人一票，选上的人认真做，没选上的人也能继续出力；同时纠正两个常见误认为：选班委不是看平时关系好不好，也不因为「我不当」就与己无关。二是「协商决定班级事务」：协商是指把问题摆到桌面上，每个人把想法和理由说清楚，一起找一个大家都愿意试一试的办法；议事五步是把问题说清楚、每人说想法和理由、找共同点、定一个能试的办法、过一段时间回来看效果再调整；判断一个办法好不好看三条——能不能解决大家的问题、能不能做到、有没有照顾到少数同学。落点还包括：班规是大家一起定的也要大家一起守，班级公约里也可以一起商量「哪些事我们不做」（不玩有危险的游戏、遇到有人在校外递烟及时告诉老师和家里人），保护好自己也是主人该做的一件事。三个互动台子都能真操作，反馈一律写成「这样可能会……，还可以试试……」：动手一是班务议事台（四个真实班务问题，每个三种处理办法，选完展开执行后果与谁会受影响）、动手二是议事五步搭建台（打乱的步骤卡按顺序点，排对生成「我们班的议事五步」）、综合任务是我的班级提案生成台（选问题 → 选办法 → 选怎么知道有没有用，合成一份可提交给班委的提案）。插图一律为中性简洁扁平插画，不使用真人照片风格。",
    "tags": ["我们是班级的主人", "选举产生班委会", "协商决定班级事务", "班级议事五步", "班级公约", "五年级", "中华优秀传统文化"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学「中华优秀传统文化」——增强自我保护意识，拒绝不良诱惑，珍爱生命；对应统编《道德与法治》五年级上册 第2单元「我们是班级的主人」：选举产生班委会、协商决定班级事务。",
    "hero_question": "班里的日子，凭什么要我来操心？",
    "hero_alt": "我们是班级的主人知识结构图：班委会由全班选举产生、班级事务协商着定、每个人都是班级的主人 三栏，附中文标注",
    "hero_caption": "我们是班级的主人：班委怎么选 · 事情怎么定 · 每个人都能出力（先看岗位、再听打算、后投一票）",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "班委到底该怎么选？", "d": "是看关系好，还是看谁能把事做好", "v": "班委到底该怎么选"},
        {"t": "班里的事，谁说了算？", "d": "有的事吵来吵去也定不下来", "v": "班里的事谁说了算"},
        {"t": "被选上的人要做哪些事？", "d": "班委不是一个称号，是一件件具体的事", "v": "被选上的人要做哪些事"},
        {"t": "我不当班委，能为班级做什么？", "d": "班级的主人，不只是班委", "v": "我不当班委能为班级做什么"},
    ],
    "objectives": [
        "能说出班委会是什么，知道它的成员是由全班同学选举产生的",
        "能说出选举班委时要看清的三件事：先看岗位要做什么、再听他打算怎么做、最后看他平时做得怎么样",
        "能说出协商决定班级事务的五个步骤：把问题说清楚、每人说想法和理由、找共同点、定一个能试的办法、过一段时间回来看效果再调整",
        "能说出判断一个办法好不好要看的三条：能不能解决大家的问题、能不能做到、有没有照顾到少数同学",
    ],
    "objectives_plain": [
        "能说出班委会是什么，它的成员是怎么产生的",
        "能说出选举班委时要看清的三件事",
        "能说出协商决定班级事务的五个步骤",
        "能说出判断一个办法好不好的三条标准",
    ],
    "standards": [
        {"content": "增强自我保护意识，拒绝不良诱惑，珍爱生命。",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学 中华优秀传统文化"},
        {"content": "选举产生班委会；协商决定班级事务",
         "source": "统编《道德与法治》五年级上册 第2单元「我们是班级的主人」"},
    ],
    "prereqs": ["pol-e-g5-u1"],
    "prereqs_name": "面对成长中的新问题",
    "prereqs_meta": "pol-e-g5-u1",
    "leads_to": [],
    "next_meta": "",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "班里的事总得有人张罗。这节课弄清楚：班委是怎么选出来的，事情又是怎么一起定下来的。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能为班里的一件事说清楚「为什么该这么办」。",
        "objectives": "看清四件事：班委怎么产生、选举看哪三样、议事分几步、办法好不好看哪三条。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "先看岗位、再听打算、后投一票；选上认真做，没选上也能继续出力。",
        "lab-1": "四个班务问题，每个三个办法。选一个，看执行下去会发生什么、谁会受影响。",
        "module-2": "议事五步：摆问题、说想法、找共同点、定试行、回头看。第五步最容易被忘掉。",
        "lab-2": "五张步骤卡是打乱的，按正确顺序点下去，就搭出「我们班的议事五步」。",
        "worked-example": "五(2)班改选五步：看清岗位、听打算、当场提问、一人一票、选完都能出力。",
        "conceptest-1": "三个说法里各藏着一个容易想歪的地方，选完把解释读一遍。",
        "synthesis": "三步选完，合成一份提案：我想提的问题是 → 我打算这样试 → 怎么知道有没有用。",
        "posttest": "出现了拉票、值日表、校外的烟，看看今天的办法还用不用得上。",
        "summary": "四句话：班委怎么选、事情怎么定、办法好不好看三条、每个人都能出力。",
        "homework": "三层小任务，先做前两层；第二层要请小组同学一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学道德与法治「中华优秀传统文化」板块在五年级的空缺，正对统编五上第 2 单元「我们是班级的主人」（选举产生班委会、协商决定班级事务）。五年级学生天天在班里过日子，可对「班里的日子是怎么定下来的」往往没有概念：改选班委时，有的只看平时关系好不好，有的觉得「反正我不当，选谁都一样」；碰到课间太吵、图书角乱、值日不均这类班务，也常常是抱怨几句就过去，很少真的坐下来商量出一个能试的办法。所以全课不讲大道理，把两件事都换成能练出来的动作。第一层是「选举产生班委会」：先给规范表述——班委会是指班级里由同学们推选出来、为大家服务的一小组人，成员由全班同学选举产生；再把选举落成先看岗位要做什么、再听他打算怎么做、最后看他平时做得怎么样，一人一票；并纠正两个误认为：选班委不是看关系好不好，「我不当」也不等于与我无关。第二层是「协商决定班级事务」：先给规范表述——协商是指把问题摆到桌面上，每个人把想法和理由说清楚，一起找一个大家都愿意试一试的办法；再把议事拆成五步：把问题说清楚、每人说想法和理由、找共同点、定一个能试的办法、过一段时间回来看效果再调整；并给出判断办法好不好的三条：能不能解决大家的问题、能不能做到、有没有照顾到少数同学。第三层是「自己也是主人」：班规是大家一起定的，也要大家一起守；班级公约里也可以一起商量「哪些事我们不做」，比如不玩有危险的游戏、遇到有人在校外递烟及时告诉老师和家里人——保护好自己，也是主人该做的一件事。三个互动台子都能真操作，反馈一律写成「这样可能会……，还可以试试……」：动手一是班务议事台，四个真实班务问题各配三个处理办法，选完展开执行后果与谁会受影响；动手二是议事五步搭建台，把打乱的步骤卡按正确顺序点出来，搭成一张议事流程；综合任务是我的班级提案生成台，学生按「我想提的问题是 → 我打算这样试 → 怎么知道有没有用」各选一步，由系统合成一份可以直接念给班委听的提案。插图一律为中性简洁扁平插画，不使用真人照片风格。",
    "plan_table": """| 1 | cover | 我们是班级的主人 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：班级的事，谁说了算？ | 起·前测（暴露已有想法） |
| 5 | concept | 班委会由全班选举产生：先看岗位，再听打算，后投一票 | 承·概念一（选举的依据与程序） |
| 6 | interactive | 动手一：班务议事台，这件事班里该怎么办？ | 承·核心模拟（班务问题 → 处理办法 → 执行后果） |
| 7 | concept | 班级事务协商着定：摆问题、说想法、找共同点、定试行、回头看 | 承·概念二（议事五步与三条评判） |
| 8 | interactive | 动手二：议事五步搭建台，把顺序排出来 | 承·流程搭建（打乱步骤按序点出） |
| 9 | concept | 例题示范：五(2)班的一次改选 | 转·重难点突破（五步示范 + 易错点） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：我的班级提案生成台 | 合·迁移应用（三步合成提案） |
| 12 | quiz | 后测：换几个新情境，办法还在不在 | 合·后测 |
| 13 | summary | 小结：班委怎么选，班里的事怎么定 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：班委会由全班选举产生 / 班级事务协商着定 / 每个人都是班级的主人 三栏\n- P5 班委会选举流程示意图（已生成）：先看岗位、再听打算、一人一票、选上认真做，附中文标注\n- P7 协商决定班级事务五步示意图（已生成）：摆问题、说想法、找共同点、定试行、回头看，附中文标注\n- 三张图均为中性简洁扁平教学插画，不使用真人照片风格，不含可识别的真实人物\n- 课件不出现真实的学校名称、班级合影或学生个人信息，示例均为虚构情境\n- 班会与议事场景不呈现任何惩罚性画面（罚站、批评名单等一律不出现在插图中）\n- 若需补充：本班学生自己记录的议事记录表（由学生手写），不在课件中呈现任何个人真实信息",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
