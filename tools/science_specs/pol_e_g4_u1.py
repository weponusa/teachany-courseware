# -*- coding: utf-8 -*-
"""小学道德与法治 · 与班级共成长（四年级）—— 补齐知识树「道德修养」空缺

学科语气（道德与法治）：情境案例驱动，情感共鸣 + 价值判断，多用真实班级场景；
结论落在「应该怎么做、为什么」，不做道德说教，也不做法条背诵。
四年级要具体：班规怎么定才公平、班里的矛盾怎么处理、和别的班怎么相处。

内容落点（对应统编四上「与班级共成长」三课）：
  ① 我们班四岁了：共同的名字、共同的记号、一起经历过的事，让四十个同学变成「我们班」；
     班级也像人一样会「长大」，它的样子是全班一起做出来的。呼应的课标要求是
     「有集体意识和责任感」「友善待人」。
  ② 我们的班规我们订：班规不是老师定的规矩，是全班一起商量出来的约定。一条公平的班规
     要过五关——大家一起商量、说得具体能做、对所有人一样、定完能执行、不合适可以改。
  ③ 我们班 他们班：班级之间有比赛也有合作；看到别的班做得好，先看看人家怎么做的，
     挑一条自己班也能做的，不贬低、不攀比、也不照抄。

三个互动台子都能真操作：
  动手一 = 班级小议事员：六件班里常遇到的事 × 三个做法 → 展开后果（含同学的感受），
           反馈一律写成「这样可能会……，还可以试试……」；
  动手二 = 班规模拟台：选一个班里真实存在的问题 → 选一种班规写法 → 展开执行后果；
  综合任务 = 把八条做法分进「在为班级做事／要调整的」两个筐。
插图一律中性简洁扁平插画，不使用真人照片风格。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g4-u1"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "你在这个班里待了四年。四年里，你换过座位，熟过很多张脸，也一起经历过不少事。可是你有没有想过一件事：一个四十几个人坐在一起的屋子，是怎么变成「我们班」的？这节课我们做三件事。第一件，我们班四岁了，一起看看这四年给班里留下了什么。第二件，我们的班规我们订，看看一条班规怎样定才算公平。第三件，我们班他们班，想一想和别的班该怎样相处。带着这三个问题，我们开始。",
    "problem-anchor": "开始之前，先选一个你最想弄清楚的问题。是想知道班里那些共同的东西是怎么来的，还是想知道班规怎样定才公平；是想知道班里有了矛盾怎么办，还是想知道和别的班怎样才能相处得好。选好以后，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出我们班有哪些共同的东西，比如班级的名字、标志、一起经历过的事，并且知道这些东西是全班一起做出来的。第二，能说出公平的班规要满足哪几条：大家一起商量、说得具体能做、对所有人一样、定完能执行、不合适可以改。第三，遇到班里的小矛盾，会先听清楚事情、再看看有没有别的办法，而不是先怪人或者躲开。第四，知道和别的班既能比赛也能合作，看到别的班做得好，可以学过来，不去贬低别人，也不照抄。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先来看一件有意思的事：一个班是怎么「长大」的。四年级的你，已经在这个班里待了四年。四年前，大家谁也不认识谁，坐在一起还有点拘谨；现在，一个眼神就知道同桌在想什么。中间发生了什么？发生了很多一起的事。一起参加过的运动会，一起练过的合唱，一起排过的队伍，一起为一道难题着急过，也一起为一次成功高兴过。这些事一件一件攒起来，就攒出了一个东西，叫做「我们班」。所以班级的样子不是天生的，是一起做出来的。班级的名字、班徽、班歌、班级的大事记，都不是装饰，它们是这个班的记号：看到它就知道，我是这个班里的人。四年级能做的事很具体：为班里设计一个标志；把班里的好人好事记下来，做成一本班级大事记；有同学请假好几天，帮他抄一份课上的要点；班里来了新同学，带他认一认教室、厕所、饮水机在哪儿。这些事情看着小，但它们正是「我们班」继续长大的方式。",
    "lab-1": "现在请你当一次班级小议事员。这里有六件在班里常常遇到的事，每一件事都有三个做法。你选一个你觉得合适的，选完立刻会有一段话告诉你为什么；要是选得不太合适，也会告诉你还可以试试什么。这里的做法没有分数，你可以放心试。",
    "module-2": "再来说班规。班规不是老师拿来管我们的规矩，它是全班一起商量出来的约定。一条公平的班规，要过五关。第一关，大家一起商量：不是班长和几个班干部定完贴出来，而是每个同学都有机会说一句。第二关，说得具体能做：写「要守纪律」谁也不知道该怎么做；写「课间不追跑打闹，要跑就到操场上」就清楚多了。第三关，对所有人一样：这条规矩管同学，也管班干部，还包括在教室里的每一个人。第四关，定完能执行：说清楚谁提醒、做不到怎么办，而且这个后果要合理，不能太重也不能没有。第五关，不合适可以改：执行了一段时间发现不好用，就在班会上说清楚为什么要改，再一起改。举个例子，一条真正能用的班规长这样：课间在教室里不追跑，由当天的值日班长提醒；提醒两次不听，当天的课间休息先在座位上坐五分钟。你看，谁、什么时候、做什么、做不到怎么办，四件事都说得清。有的同学误认为「班规越严越好」——其实太重的一条规矩执行不下去，最后成了谁都不当真的一句话。",
    "lab-2": "接下来请你当一次班会的主持人。先挑一个班里真实存在的问题，再从三种班规写法里选一种，看看这条班规执行下去会发生什么。选完以后，你会看到这件事往下走的样子，也会看到还可以怎么调整。",
    "worked-example": "我们一起来看四班的那次班会。第一步，先把问题说清楚：最近课间总有人在教室里追跑，撞翻过两次水杯，还差点撞到人。第二步，一起想原因：教室地方小、下课只有几分钟、想跑又没处跑。第三步，一起定规矩，一条一条说清楚：课间在教室里不追跑；要跑就到操场上；由当天的值日班长提醒；提醒两次以后，当天的课间在座位上坐五分钟。第四步，定完试一个星期，再回来看好不好用：一个星期以后，班里发现「坐五分钟」这件事执行起来有点麻烦，就把后果改成「帮当天的值日生擦一次黑板」。第五步，和别的班比一比：有同学说五班的课间很安静，老师让大家去看了看——原来五班在下课的时候会把桌椅轻轻推回原位，走路的脚步也放轻。四班没有照抄，只挑了一条自己也能做的：下课时先把桌椅推好，再出门。同一个星期，四班的合唱没拿到名次，班会上有人说「都是跑调的同学害的」。大家没有接着怪人，而是一起把跑得最不齐的那两句挑出来，约好下周一起练。",
    "conceptest-1": "接下来用三个说法考考你，每个说法里都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件任务交给你。下面有八条班里的做法，请你判断一下：哪些是在为班级做事，放进这一边；哪些是需要调整的，放进那一边。放好以后，再读一读为什么。",
    "posttest": "最后一轮，换几个新的小情境来考考你。这次会遇到定班规、班里闹矛盾、还有和别的班比赛，看看你能不能用上今天的办法。",
    "summary": "这节课我们记住四句话。第一句，班级的样子是一起做出来的：共同的名字、共同的记号、一起经历过的事，把四十个同学变成我们班。第二句，公平的班规要过五关：大家一起商量、说得具体能做、对所有人一样、定完能执行、不合适可以改。第三句，班里有了问题，先把事情说清楚，再一起想别的办法，不先怪人也不躲开。第四句，和别的班既能比赛也能合作：看到别的班做得好，挑一条自己也能做的学过来，不贬低、不攀比、也不照抄。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出我们班的三样共同的东西，各写一句话说明它是怎么来的；再写出公平班规要过的五关。第二层能力应用，动手做：为班里做一件具体的事，比如整理一次图书角、帮一位请假的同学抄一份要点，写清楚你做了什么、别人有什么反应。第三层迁移挑战，选做：留意一个班里大家都有点意见的小问题，用今天学的五关，写一条具体可执行的班规提案，下节班会上提出来。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 我们班四岁了", "lab-1": "动手一 班级小议事员",
    "module-2": "概念二 我们的班规我们订", "lab-2": "动手二 班规模拟台",
    "worked-example": "例题示范 四班的那次班会", "conceptest-1": "概念测试",
    "synthesis": "综合任务 在为班级做事的 / 要调整的", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：班级小议事员（六件班里常遇到的事 × 三个做法） ──
SCENES = [
    {"id": "s1", "t": "班里要选一个班徽，同学问你想画什么", "opts": [
        {"k": "a", "t": "把我想的画法说出来，再听听别人想画什么", "ok": True,
         "fb": "先说自己的想法，再听别人的，最后一起挑——这样出来的班徽，全班都认。"},
        {"k": "b", "t": "我画得不好，随便你们吧", "ok": False,
         "fb": "这样可能会让你那一份想法一直没有被听见，班徽里也少了你的一笔。还可以试试：哪怕只说一句「我想要蓝色」，也是你出的主意。"},
        {"k": "c", "t": "我不管，反正要用我画的", "ok": False,
         "fb": "这样可能会让别的同学不敢再说想法，最后大家心里都不太舒服。还可以试试：先把自己的想法说完，再问一句「你们想画什么」。"},
    ]},
    {"id": "s2", "t": "班会讨论新班规，有人提了一条：迟到的人罚站一节课", "opts": [
        {"k": "a", "t": "说出我的想法：这条太重了，我们再想想别的办法，并说说为什么", "ok": True,
         "fb": "把话讲清楚、连理由一起讲出来，别人才听得进去。这正是在为班里定一条用得住的好规矩。"},
        {"k": "b", "t": "通过就通过，反正我又不迟到", "ok": False,
         "fb": "这样可能会让被罚的同学很难受，也可能有一天轮到你自己。还可以试试：定规矩的时候就说一句「这条会不会太重」。"},
        {"k": "c", "t": "当场说：这个想法太蠢了", "ok": False,
         "fb": "这样可能会让提建议的同学下不来台，下次他不敢再开口。还可以试试：说「我担心这条太重」，说的是这件事，不是这个人。"},
    ]},
    {"id": "s3", "t": "值日那天，同组的一位同学有事先走了，他那块没做完", "opts": [
        {"k": "a", "t": "先把他那一块做完，第二天跟他提一句：昨天我帮你扫了", "ok": True,
         "fb": "你把事做完了，也把话说清楚了。他知道了下一次就会记得，也不会以为没人发现。"},
        {"k": "b", "t": "凭什么就我一个人做，我也不做了", "ok": False,
         "fb": "这样可能会让全组都挨批评，教室也没人打扫。还可以试试：先把自己那一块做完，再和组里商量下次怎么分。"},
        {"k": "c", "t": "赶紧去告诉老师：他逃值日", "ok": False,
         "fb": "这样可能会让同学觉得你在告状，事情也未必真的是他故意跑掉。还可以试试：先问问同学那天为什么走了，再说给老师听。"},
    ]},
    {"id": "s4", "t": "班里的合唱比赛没拿到名次，班会上有人开始抱怨", "opts": [
        {"k": "a", "t": "一起说说这次哪里可以做得更好，约好下次一起练", "ok": True,
         "fb": "把力气用在下次怎么做好上，班里才不会因为一次比赛就散了气。"},
        {"k": "b", "t": "就是那个跑调的同学害的", "ok": False,
         "fb": "这样可能会让那位同学以后不敢再张嘴，也让大家只顾着找人负责。还可以试试：一起把没唱齐的那两句挑出来，约个时间一起练。"},
        {"k": "c", "t": "以后这种比赛我再也不参加了", "ok": False,
         "fb": "这样可能会让班里少一个人手，你自己也少了一次和大家一起做事的机会。还可以试试：说一句「下次我想负责排队形」。"},
    ]},
    {"id": "s5", "t": "老师让大家去隔壁班看看，说人家教室布置得很漂亮", "opts": [
        {"k": "a", "t": "认真看看人家怎么做的，回来挑一条我们班也能做的", "ok": True,
         "fb": "学过来能用的那一条，比一比快，也比照抄有用。"},
        {"k": "b", "t": "有什么好看的，还不如我们班", "ok": False,
         "fb": "这样可能会让全班少一次变好的机会。还可以试试：找一个他们做得确实好的地方，哪怕只是一处小角落。"},
        {"k": "c", "t": "把他们班的布置全部照搬过来，一点都不改", "ok": False,
         "fb": "这样可能会做出一个不像我们班的教室，也未必适合我们班的墙。还可以试试：学他们的做法，用我们班自己的想法来做。"},
    ]},
    {"id": "s6", "t": "班会上问大家对班里的事有什么想法，你其实有话想说", "opts": [
        {"k": "a", "t": "举手说出来，先说是什么事，再说我希望怎样", "ok": True,
         "fb": "说出自己的那一条，是你在为班级做事。说清楚了，大家才好一起商量。"},
        {"k": "b", "t": "不说了，反正我们的意见也不重要", "ok": False,
         "fb": "这样可能会让你和同学的很多想法一直没有被听见。还可以试试：只挑最在意的那一件事说出来，哪怕只有一句话。"},
        {"k": "c", "t": "写在纸条上传来传去，看谁同意", "ok": False,
         "fb": "这样可能会让话传到最后变了样，大家还不知道是谁提的。还可以试试：在班会上举一次手，把那条建议直接说出来。"},
    ]},
]

# ── 动手二：班规模拟台（六个班里真实存在的问题 × 三种班规写法） ──
SCHEMES = [
    {"k": "a", "n": "大家一起商量，把「什么时候、谁来做、做不到怎么办」都写清楚，对所有人一样", "ok": True},
    {"k": "b", "n": "只写一句「要守纪律」，谁做不到就批评谁", "ok": False},
    {"k": "c", "n": "让班长一个人定，定完贴在墙上就行", "ok": False},
]
TASKS = [
    {"id": "t1", "n": "课间有人在教室里追跑，撞翻过水杯，还差点撞到人", "out": {
        "a": "班规这样写：课间在教室不追跑，要跑就到操场上；当天的值日班长提醒；提醒两次以后，当天的课间在座位上坐五分钟。定完试一个星期再看。撞翻水杯的事少了很多，想跑的同学也有了去处。",
        "b": "「要守纪律」这句话谁都挑不出错，可是课间该怎么做，还是没人知道。真有人跑起来，也只能等老师来批评一顿。还可以试试：把规矩写到能照着做的程度，比如「要跑就到操场上」。",
        "c": "班长一个人定完贴出来，第二天就有同学说「这条我不知道」。执行的时候他自己也心虚，因为定的时候没人跟他说过。还可以试试：在班会上留几分钟，让每个同学都说一句。"}},
    {"id": "t2", "n": "值日经常有人忘记，最后留下的人一个人做完整个教室", "out": {
        "a": "班规这样写：值日按组轮，每人负责一块地方；当天有事要先跟组长换一次；做完由组长一起检查一遍再走。留下来的那个人不再是一个人扛，谁忘了也有换的办法。",
        "b": "「要守纪律」管不了值日：忘的人还是忘，做完的人还是委屈。批评完第二天照样有人忘记。还可以试试：把谁负责哪一块写清楚，再留一个换人的办法。",
        "c": "班长自己定了值日表贴出来，可他不知道有两位同学每周三下午要上兴趣班。这两次的值日还是空着。还可以试试：定之前先问一句大家哪几天不方便。"}},
    {"id": "t3", "n": "图书角的书被翻得很乱，第二天找不到想看的书", "out": {
        "a": "班规这样写：借书在登记本上写名字和日期；一次最多借两本，看完放回原来的格子；每周五下午由图书管理员清点一次。找书不用翻半天，少的书也查得出来。",
        "b": "「要守纪律」在图书角没什么用，因为没有说清楚借书要登记、看完要放回哪儿。书还是照样乱。还可以试试：把「放回原来的格子」这一句加上。",
        "c": "班长一个人定的规矩是「谁也不许把书带出教室」。这样书是不乱了，可午休想看书的同学也看不成，大家觉得这条规矩定得有点亏。还可以试试：定之前先问问大家想怎么借。"}},
    {"id": "t4", "n": "有人在课桌和墙上乱画，擦不掉，看着很脏", "out": {
        "a": "班规这样写：想画可以画在教室后墙的展示板上；课桌上不乱画；发现有画过的地方，当天值日组一起擦干净。有了能画的地方，课桌上反而干净了。",
        "b": "「要守纪律」这句话贴在墙上，可是想画的人还是想画，也不知道能画在哪儿。还可以试试：先给想画的人一个地方，比如教室后墙的展示板。",
        "c": "班长一个人定的是「谁画谁罚抄课文十遍」。这条规矩重得让人不敢说真话，画了的人也不敢认。还可以试试：把后果定得轻一点、做得到一点，比如一起把画过的地方擦干净。"}},
    {"id": "t5", "n": "上课有同学一直小声讲话，影响到别人听课", "out": {
        "a": "班规这样写：上课想说话先举手；同桌之间听到小声讲话，轻碰一下提醒；提醒两次以后的人，下课后来和老师说一句为什么。上课安静了，也没有人当着全班被点名。",
        "b": "「要守纪律」说了等于没说，谁都不知道提醒的时候该怎么提醒。小声讲话的人还是照样讲。还可以试试：把提醒的办法定下来，比如同桌轻碰一下。",
        "c": "班长一个人定的是「讲话的人站到教室后面去」。真执行起来，站过去的人一节课什么都没听进去，班长自己也不好意思叫。还可以试试：定一条轻一点、又真能做到底的办法。"}},
    {"id": "t6", "n": "饮水机旁常常有积水，有同学差点滑倒", "out": {
        "a": "班规这样写：接水时把杯子放稳，水不要接太满；看到地上有水，顺手用旁边的拖把擦一下；每周五由值日组检查一次地面。滑倒的事没再发生，因为每个人顺手就能做一点。",
        "b": "「要守纪律」管不到地上的一滩水。地还是湿的，走过的人还是要小心。还可以试试：把规矩写到具体动作上，比如「看到地上有水，顺手擦一下」。",
        "c": "班长一个人定的是「谁也不许再去饮水机接水」。这条规矩把大家都难住了，喝水也成了问题。还可以试试：定的规矩要让人能过日子，再在班会上改一改。"}},
]

# ── 综合任务：在为班级做事的 / 要调整的（八条做法分进两个筐） ──
SORT_ITEMS = [
    {"id": "k1", "t": "定班规之前，先在班会上让每个同学都说一句自己的想法", "bin": "good",
     "why": "大家一起商量出来的规矩，才有人愿意一起守。"},
    {"id": "k2", "t": "把班规写到能照着做的程度：什么时候、谁来做、做不到怎么办", "bin": "good",
     "why": "说得具体，规矩才用得住，不会变成墙上的一句空话。"},
    {"id": "k3", "t": "班规对同学一样，对班干部也一样", "bin": "good",
     "why": "对所有人一样，才叫公平；不一样，规矩就会慢慢没人当真。"},
    {"id": "k4", "t": "看到别的班做得好，挑一条自己班也能做的学过来", "bin": "good",
     "why": "学过来能用的那一条，是让班级变好的最快的办法。"},
    {"id": "k5", "t": "定完一条班规以后，发现不好用，就在班会上说清楚为什么要改，再一起改", "bin": "good",
     "why": "规矩不是刻在石头上的，能改的规矩才活得久。"},
    {"id": "k6", "t": "比赛没拿到名次，先找出那个拖后腿的同学", "bin": "tune",
     "why": "这样可能会让那位同学以后不敢再参加，也让大家只顾着找人负责。还可以试试：一起把没做好的那两处挑出来，约好下次一起练。"},
    {"id": "k7", "t": "班规是几个人定完贴出来的，别人照着做就行", "bin": "tune",
     "why": "这样可能会让很多同学觉得「这条跟我没关系」，执行起来也没人当真。还可以试试：定之前在班会上留几分钟，让每个同学说一句。"},
    {"id": "k8", "t": "班里出了点问题，先躲开，反正不久就轮到别人了", "bin": "tune",
     "why": "这样可能会让小问题一直留着，班里的事也总落在几个人身上。还可以试试：先说一句「这件事我能做哪一点」，再说给班会上听。"},
]
SORT_BIN = {"good": "在为班级做事的", "tune": "要调整的"}

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g4-u1 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 班级小议事员：六件事 × 三个做法 → 温和反馈（不判错、不贴标签）
   3) 班规模拟台：选问题 → 选班规写法 → 展开执行后果
   4) 在为班级做事的 / 要调整的：八条做法分进两个筐
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

  /* ---------- 2. 班级小议事员 ---------- */
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

  /* ---------- 3. 班规模拟台 ---------- */
  var TASKS = __TASKS_JSON__;
  var SCHEMES = __SCHEMES_JSON__;
  var stage2 = document.getElementById('rule-stage');
  if (stage2) {
    var curTask = null, doneTask = {};
    var out2 = document.getElementById('rule-out');
    function taskById(id) {
      for (var i = 0; i < TASKS.length; i++) { if (TASKS[i].id === id) return TASKS[i]; }
      return null;
    }
    function render2() {
      document.querySelectorAll('[data-rule-task]').forEach(function (b) {
        var k = b.dataset.ruleTask;
        b.classList.toggle('selected', k === curTask);
        b.classList.toggle('correct', !!doneTask[k]);
      });
      document.getElementById('rule-score').textContent =
        '已经试过 ' + Object.keys(doneTask).length + ' / ' + TASKS.length + ' 个问题';
    }
    document.querySelectorAll('[data-rule-task]').forEach(function (b) {
      b.addEventListener('click', function () {
        curTask = b.dataset.ruleTask;
        var T = taskById(curTask);
        if (doneTask[curTask]) {
          out2.className = 'result';
          out2.innerHTML = '<strong>这个班里的问题已经试过了：' + T.n + '</strong>你上次选的班规写法挺好，换个问题再试试。';
        } else {
          out2.className = 'result warn';
          out2.innerHTML = '<strong>班里出现的问题是：' + T.n + '</strong><br>下面有三种班规写法，你选一种，看看执行下去会发生什么。';
        }
        render2();
      });
    });
    document.querySelectorAll('[data-rule-scheme]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!curTask) {
          out2.className = 'result warn';
          out2.textContent = '先在上面点一个班里存在的问题，再来选班规写法。';
          return;
        }
        var T = taskById(curTask);
        var k = b.dataset.ruleScheme;
        var isOk = false;
        for (var i = 0; i < SCHEMES.length; i++) { if (SCHEMES[i].k === k) isOk = !!SCHEMES[i].ok; }
        if (isOk) {
          doneTask[T.id] = true;
          out2.className = 'result';
          out2.innerHTML = '<strong>' + T.n + '：这样定班规，能用得住。</strong>' + T.out[k];
        } else {
          out2.className = 'result warn';
          out2.innerHTML = '<strong>' + T.n + '：这样定，可能会不太顺。</strong>' + T.out[k];
        }
        render2();
      });
    });
    render2();
  }

  /* ---------- 4. 在为班级做事的 / 要调整的 ---------- */
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
        out3.innerHTML = '<strong>你选的是：' + b.textContent + '</strong><br>想一想，它是在为班级做事的，还是要调整的？';
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
            out3.innerHTML = '<strong>八条全放对了！</strong>记住这句口诀：<strong>一起商量、说得具体、对所有人一样，' +
              '定完能做、不好就改，班里的事人人有份。</strong>';
          }
        } else {
          out3.className = 'result warn';
          out3.innerHTML = '<strong>再想一想这条做法。</strong>' + it.why +
            '<br><span style="color:var(--muted)">常见错误：容易把「看起来也是想让班里好」误认为「在班里能用的做法」——' +
            '先看这件事有没有让某位同学为难、有没有人一直被落下，答案就清楚了。</span>';
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
        {"q": "「我们班」这三个字，是怎么来的？",
         "options": [("是全班一起经历过的事一件一件攒起来的，比如一起参加过的比赛、一起做的事",
                      True),
                     ("是开学那天老师给这个班起的名字", False),
                     ("是教室门口挂的那块牌子写出来的", False)],
         "explain": "牌子上的名字谁都能挂，可「我们班」的感觉是要一起做事才有的。"
                    "<strong>错因提醒：</strong>常见错误是误认为「班级就是一群人在同一个教室里」——"
                    "同一间教室里的四十几个人，要一起经历过一些事，才会变成「我们班」。"},
        {"q": "一条公平的班规，下面哪一种定法比较合适？",
         "options": [("在班会上让每个同学都说一句，把「什么时候、谁来做、做不到怎么办」写清楚", True),
                     ("班长和几位班干部商量好，贴出来让全班照着做", False),
                     ("写一句「要守纪律」，谁做不到就批评谁", False)],
         "explain": "大家一起商量，规矩才有人一起守；写得具体，规矩才用得住。"
                    "<strong>错因提醒：</strong>有的同学误认为「班干部定得更快，也更公平」——"
                    "快是真的，可大家没有参与过，执行的时候就没人当真。"},
        {"q": "班里的合唱比赛没拿到名次，下面哪种做法更合适？",
         "options": [("一起说说哪里可以做得更好，约好下次一起练", True),
                     ("想一想是谁拖了后腿", False),
                     ("以后这类比赛全班都不参加了", False)],
         "explain": "把力气用在下次怎么做好上，班里才不会因为一次比赛散了气。"
                    "<strong>错因提醒：</strong>容易把「找到原因」和「找到人负责」搞混——"
                    "找原因要的是下次做得更好，找人负责只会让那位同学以后不敢再张嘴。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "我们班四岁了：班级的样子，是全班一起做出来的", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们每天都在这个班里上课、值日、聊天（And）；可是有时候只觉得「一群人在一个教室里」，没觉得这是「我们班」（But）；所以这节课先看看这四年给班里留下了什么，看看班级是怎么长大的（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">「我们班」这三个字，不是开学那天就有的，是<strong>一起经历过的事一件一件攒出来的</strong>。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>共同的记号</strong></p>
            <p style="color:var(--muted)">班名、班徽、班歌、教室里那面贴满照片的墙。看到这些记号，就知道我是这个班里的人。</p>
          </div>
          <div class="inner-card">
            <p><strong>共同经历的事</strong></p>
            <p style="color:var(--muted)">一起参加过的运动会、一起练过的合唱、一起为一道难题着急过，也一起为一次成功高兴过。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="「我们班」是怎么长大的概念图：共同的记号、共同经历的事、一起做的事，最后攒成我们班，附中文标注">
          <figcaption>概念图：「我们班」是怎么长出来的——共同的记号 · 共同经历的事 · 一起做的事（教学示意图，中性简洁扁平插画）</figcaption>
        </figure>
        <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(78,205,196,.45)">
          <p><strong>四年级能做的事，很具体</strong></p>
          <p style="color:var(--muted)">为班里设计一个标志 · 把班里的好人好事记下来，做成一本班级大事记 · 有同学请假好几天，帮他抄一份课上的要点 · 班里来了新同学，带他认一认教室、厕所、饮水机在哪儿。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「为班级做事就是参加比赛拿名次」。可班徽是有人画的、大事记是有人写的、请假的同学是有人帮他抄要点的——这些事小得多，也真得多。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "同一个教室，可以只是「上课的地方」，也可以是「我们班」。差别就在你和这里的人有没有一起做过事、一起记着一些事。"},
    {"lens": "解释它", "text": "为什么共同经历这么重要？因为一起做过事的人，心里有一份「我们一起过」的记忆，遇事才会愿意先替对方想一步。"},
    {"lens": "迁移它", "text": "这套眼光在家里也管用：一家人一起做过饭、一起出过一趟远门，家里的感觉就会不一样。"},
])}
    ''', tag="概念一"))

    case_btns = "\n".join(
        f'            <button class="choice" data-case="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in SCENES
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：班级小议事员，你会怎么做？", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一件班里常常遇到的事，再从三个做法里选一个。<strong>选得好会告诉你为什么，选得不太合适也会告诉你还可以试试什么。</strong></p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 班里遇到的这件事</div>
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
          <p class="result warn" id="case-out" style="margin-top:12px">先点一件班里可能遇到的事。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💛</span><div><strong>说给你听：</strong>这里的做法没有分数。有些做法只是会让同学不太舒服，换一个试试就好。拿不准的时候，去问问老师的看法，是很好的办法。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "我们的班规我们订：一条公平的班规要过五关", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">班规不是老师拿来管我们的规矩，它是<strong>全班一起商量出来的约定</strong>。要公平，得过五关。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>大家一起商量：</strong>不是班长和几个班干部定完贴出来，而是每个同学都有机会说一句。</div></div>
          <div class="step"><span class="n">2</span><div><strong>说得具体能做：</strong>写「要守纪律」谁也不知道怎么做；写「要跑就到操场上」就清楚了。</div></div>
          <div class="step"><span class="n">3</span><div><strong>对所有人一样：</strong>这条规矩管同学，也管班干部，还包括在教室里的每一个人。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>定完能执行：</strong>说清楚谁提醒、做不到怎么办，而且后果不能太重，也不能没有。</div></div>
          <div class="step"><span class="n">5</span><div><strong>不合适可以改：</strong>用了发现不好用，就在班会上说清楚为什么要改，再一起改。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="公平班规怎么定：五关和一条班规的四个要素（谁、什么时候、做什么、做不到怎么办），附中文标注">
          <figcaption>概念图：公平班规的五关 · 一条班规要写清的四件事（教学示意图，中性简洁扁平插画）</figcaption>
        </figure>
        <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(78,205,196,.45)">
          <p><strong>一条用得住的班规，长这样</strong></p>
          <p style="color:var(--muted)">课间在教室里不追跑，要跑就到操场上；由当天的值日班长提醒；提醒两次以后，当天的课间在座位上坐五分钟。<strong>谁、什么时候、做什么、做不到怎么办</strong>，四件事都说得清。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「班规定得越严越好」。可太重的一条规矩执行不下去，最后就成了谁都不当真的一句话；真正管用的规矩，是大家做得到、也愿意做的那一条。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "同一条班规，写「要守纪律」和写「要跑就到操场上」，留给同学的其实是两种不同的东西：一种是不知道怎么办，一种是知道怎么办。"},
    {"lens": "比较它", "text": "「班长一个人定」和「大家在班会上一起定」，差的不只是过程；执行的时候，一个是班长在管人，一个是全班在守约定。"},
    {"lens": "迁移它", "text": "这套办法在家里也用得上：和家里人商量晚上几点睡，先把「几点、谁提醒、做不到怎么办」说清楚，比争一句「你就是不听话」有用得多。"},
])}
    ''', tag="概念二"))

    task_btns = "\n".join(
        f'            <button class="choice" data-rule-task="{t["id"]}" style="text-align:left">班里的问题：{t["n"]}</button>'
        for t in TASKS
    )
    scheme_btns = "\n".join(
        f'            <button class="choice" data-rule-scheme="{s["k"]}" style="text-align:left">{s["n"]}</button>'
        for s in SCHEMES
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：班规模拟台，这条班规该怎么写？", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">你现在是班会的主持人。先挑一个班里真实存在的问题，再从三种班规写法里选一种，看看这条班规执行下去会发生什么。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 班里出现的问题</div>
          <div class="grid" id="rule-stage">
{task_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 这条班规怎么写</div>
          <div class="grid">
{scheme_btns}
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">试过几个问题</span><span class="v" id="rule-score">已经试过 0 / 6 个问题</span></div>
          </div>
          <p class="result warn" id="rule-out" style="margin-top:12px">先在上面点一个班里存在的问题。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧩</span><div><strong>想一想：</strong>三种写法里，为什么「大家一起商量、写得具体」总是走得最顺？因为规矩要有人愿意守，也要有人做得到。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：四班的那次班会", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>四班最近课间总有人在教室里追跑，撞翻过两次水杯，还差点撞到人。请你看看四班是怎么把这条班规定下来的，又是怎么面对和别的班的比较的。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先把问题说清楚：</strong>课间在教室里追跑，撞翻过水杯，还差点撞到人。说的是这件事，不是某个人。</div></div>
          <div class="step"><span class="n">2</span><div><strong>一起想原因：</strong>教室地方小、下课只有几分钟、想跑又没处跑。找到了原因，办法才好想。</div></div>
          <div class="step"><span class="n">3</span><div><strong>一起定规矩：</strong>课间在教室不追跑；要跑就到操场上；当天值日班长提醒；提醒两次以后，当天课间在座位上坐五分钟。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>试一段时间再回来看：</strong>一个星期后，班里发现「坐五分钟」不太好执行，就在班会上说明原因，把后果改成帮当天的值日生擦一次黑板。</div></div>
        </div>
        <div class="inner-card">
          <p><strong>和别的班比的时候</strong></p>
          <p style="color:var(--muted)">有同学说五班的课间很安静，老师带大家去看了看——五班下课时会把桌椅轻轻推回原位，走路也放轻脚步。四班没有照抄，只挑了一条自己也能做的：下课时先把桌椅推好，再出门。同一个星期，四班的合唱没拿到名次，班会上有人说「都是跑调的同学害的」。大家没有接着怪人，而是一起把最不齐的那两句挑出来，约好下周一起练。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「班规定下来就不能改了，改了就是没威信」。可四班正是把「坐五分钟」改成「擦一次黑板」，规矩才真正执行下去了——能改的班规，才活得久。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "关于班规，下面哪句话说得对？",
         "options": [("班规是全班一起商量出来的约定，它管同学，也管班干部", True),
                     ("班规定得越严，大家就越守规矩", False),
                     ("班规是老师定给我们执行的，我们照着做就行", False)],
         "explain": "大家一起商量、对所有人一样，规矩才有人愿意守。"
                    "<strong>错因提醒：</strong>常见错误是误认为「班规越严越好」——"
                    "太重的规矩执行不下去，最后成了谁都不当真的一句话。"},
        {"q": "班里要解决「图书角很乱」这个问题，下面哪种班规写法更好？",
         "options": [("借书在登记本上写名字和日期，一次最多两本，看完放回原来的格子，每周五清点一次", True),
                     ("谁也不许再把书带出教室", False),
                     ("大家要爱护图书，要守纪律", False)],
         "explain": "借书、归还、清点三件事都写清楚了，规矩才用得住。"
                    "<strong>错因提醒：</strong>有的同学误认为「规矩写严一点就不会乱」——"
                    "把书全都锁起来确实不乱，可午休想看书的同学也看不成，大家会觉得这条规矩定得亏。"},
        {"q": "隔壁班把教室布置得很好看，下面哪种做法更合适？",
         "options": [("认真看看人家怎么做的，回来挑一条我们班也能做的", True),
                     ("有什么好看的，还不如我们班", False),
                     ("把他们班的布置全部照搬过来", False)],
         "explain": "学过来能用的那一条，比一比快，也比照抄有用。"
                    "<strong>错因提醒：</strong>容易把「照抄」当成「学得好」——"
                    "全部照搬常常做出一个不像我们班的教室，也未必适合我们班的墙。"}
    ], tag="概念测试"))

    item_btns = "\n".join(
        f'            <button class="sort-item" data-item="{it["id"]}">{it["t"]}</button>' for it in SORT_ITEMS
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：在为班级做事的 / 要调整的，把做法分进两个筐", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一条做法，再点它应该进的筐：<strong>在为班级做事的</strong>放一边，<strong>要调整的</strong>放另一边。</p>
        <div class="lab-panel">
          <div class="sort-bank" id="class-stage">
{item_btns}
          </div>
          <div class="grid grid-2" style="margin-top:14px">
            <button class="choice" data-class-bin="good" style="text-align:center">在为班级做事的</button>
            <button class="choice" data-class-bin="tune" style="text-align:center">要调整的</button>
          </div>
          <div class="sort-bins">
            <div class="sort-bin" id="class-bin-a"><h4>在为班级做事的</h4></div>
            <div class="sort-bin" id="class-bin-b"><h4>要调整的</h4></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">分类进度</span><span class="v" id="class-score">已经放好 0 / 8 条</span></div>
          </div>
          <p class="result warn" id="class-out" style="margin-top:12px">先在上面点一条做法。</p>
        </div>
        <div class="inner-card">
          <p><strong>分完之后，想一想：</strong></p>
          <p style="color:var(--muted)">「在为班级做事的」这一边里，你最想先做哪一条？写在下面，再说一说为什么选它。</p>
          <textarea id="syn-answer" rows="3" placeholder="我最想先做……，因为……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，办法还在不在", TTS["posttest"], [
        {"q": "班会上要定一条新班规，一位同学提的建议你觉得不太合适，下面哪种做法更好？",
         "options": [("说出我的担心，并说清楚是哪一点让我觉得不合适", True),
                     ("既然大家都同意，那我也不说话了", False),
                     ("当场说：这个想法太蠢了", False)],
         "explain": "说清楚担心的是哪一点，别人才听得进去，规矩也能定得更稳。"
                    "<strong>错因提醒：</strong>常见错误是误认为「不反对就是配合」——"
                    "定规矩的时候不说的那一条，往往就是以后最难执行的那一条。"},
        {"q": "值日那天同组同学有事先走了，他负责的那一块没做，下面哪种做法更好？",
         "options": [("先把他那一块做完，第二天跟他提一句：昨天我帮你扫了", True),
                     ("我也不做了，凭什么就我一个人做", False),
                     ("立刻去告诉老师：他逃值日", False)],
         "explain": "把事情做完，也把话说清楚，他下一次就会记得。"
                    "<strong>错因提醒：</strong>容易把「忍住不讲」和「大度」搞混——"
                    "做了好事不说，同学会以为反正有人替他做，下次还是忘。"},
        {"q": "两个同学为了一件事吵起来，都说自己有道理，下面哪种做法更好？",
         "options": [("让他们一人说一句，先把事情说清楚", True),
                     ("马上站到一边，帮着一起吵", False),
                     ("谁也不管，快点走开", False)],
         "explain": "先听完两边的话，事情才看得明白。"
                    "<strong>错因提醒：</strong>常见错误是误认为「不管就是不吃亏」——"
                    "这样可能让矛盾越闹越大，事后班里每个人心里都不太舒服。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：四句话，讲清怎样与班级共成长", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>我们班四岁了：</strong>班级的样子是全班一起做出来的，共同的记号、共同经历的事，把同学变成「我们班」。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>班规我们订：</strong>一起商量、说得具体、对所有人一样、定完能执行、不合适可以改。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>班里的事先做再想：</strong>先把事做完、把话说清楚，不先怪人，也不躲开。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>我们班 他们班：</strong>能比赛也能合作；学别人做得好的那一条，不贬低、不攀比、不照抄。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>一句口诀：</strong>一起商量、说得具体、对所有人一样，定完能做、不好就改，班里的事人人有份。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「我们班、一起商量、我来做一件小事」这三个说法，说清楚你和班级之间的一件事。</p>
          <p style="color:var(--muted)">再动一动手：<strong>写一写</strong>你这周想为班里做的那一件事，写清做什么、什么时候做、做完告诉谁。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写出我们班的三样共同的东西，每样写一句话说明它是怎么来的。",
            "写出公平的班规要过的五关，每关写一句话。",
            "写出班里两位你愿意帮他做一件小事的同学，各写一句你想做什么。",
        ],
        [
            "为班里做一件具体的事（比如整理一次图书角、帮一位请假的同学抄一份要点），写清楚你做了什么、别人有什么反应。",
            "找一位同学一起做一件小事，先商量谁做哪一块，做完写一句你想对他说的话。",
        ],
        [
            "留意一个班里大家都有点意见的小问题，用今天学的五关，写一条具体可执行的班规提案，下节班会上提出来。",
            "去隔壁班看一看，找一条他们做得确实好的做法，写清楚它好在哪里，以及我们班能不能用、要怎么改。",
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
    "title": "与班级共成长",
    "name_en": "Growing Together with Our Class",
    "grade": 4,
    "grade_cn": "四年级",
    "domain": "moral-cultivation",
    "domain_cn": "道德修养",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学四年级的道德与法治课：先看「我们班四岁了」——班级的样子不是天生的，是共同的名字、共同的记号、一起经历过的事一件一件攒出来的，四十几个人才变成「我们班」；再说「我们的班规我们订」——一条公平的班规要过五关：大家一起商量、说得具体能做、对所有人一样、定完能执行、不合适可以改，并落到一条班规要写清的四件事（谁、什么时候、做什么、做不到怎么办）；最后讲「我们班 他们班」——班级之间既能比赛也能合作，看到别的班做得好，挑一条自己班也能做的学过来，不贬低、不攀比、也不照抄。全课以真实班级情境与可操作的选择为主，三个互动台子分别是班级小议事员（六件事 × 三做法，展开后果与同学感受）、班规模拟台（选问题 → 选班规写法 → 展开执行后果）、以及把八条做法分进「在为班级做事的／要调整的」两个筐。",
    "tags": ["与班级共成长", "我们班四岁了", "我们的班规我们订", "我们班 他们班", "集体意识", "班规公平", "四年级", "道德修养"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学「道德修养」——诚实守信、友善待人、尊重他人，有集体意识和责任感；对应统编《道德与法治》四年级上册「与班级共成长」：我们班四岁了、我们的班规我们订、我们班 他们班。",
    "hero_question": "四十几个人坐在同一间教室里，是怎么变成「我们班」的？",
    "hero_alt": "与班级共成长知识结构图：我们班四岁了、我们的班规我们订、我们班 他们班 三栏",
    "hero_caption": "与班级共成长：我们班四岁了 · 我们的班规我们订 · 我们班 他们班（一起商量、说得具体、对所有人一样）",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "「我们班」这三个字是怎么来的？", "d": "班里那些共同的东西", "v": "「我们班」这三个字是怎么来的"},
        {"t": "班规怎么定才算公平？", "d": "谁来定、定得多具体", "v": "班规怎么定才算公平"},
        {"t": "班里有了矛盾或者大家都懒得管的事，怎么办？", "d": "值日、追跑、图书角", "v": "班里有了矛盾或者大家都懒得管的事怎么办"},
        {"t": "和别的班该怎样相处？", "d": "比赛输了、别人班做得好", "v": "和别的班该怎样相处"},
    ],
    "objectives": [
        "能说出我们班有哪些共同的东西（班名、班徽、一起经历过的事），并知道它们是全班一起做出来的",
        "能说出公平的班规要过的五关：一起商量、说得具体、对所有人一样、定完能执行、不合适可以改",
        "遇到班里的小问题，会先把事情说清楚、再一起想别的办法，不先怪人也不躲开",
        "知道和别的班既能比赛也能合作：看到别的班做得好，挑一条自己也能做的学过来，不贬低、不攀比、不照抄",
    ],
    "objectives_plain": [
        "能说出我们班有哪些共同的东西，并知道它们是全班一起做出来的",
        "能说出公平的班规要过的五关，并试着用它写一条班里能用的规矩",
        "遇到班里的小问题，会先把事情说清楚，再一起想别的办法",
        "知道和别的班既能比赛也能合作，学别人做得好的那一条，不贬低也不照抄",
    ],
    "standards": [
        {"content": "诚实守信，友善待人，尊重他人，有集体意识和责任感。",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学 道德修养"},
        {"content": "我们班四岁了；我们的班规我们订；我们班 他们班",
         "source": "统编《道德与法治》四年级上册「与班级共成长」"},
    ],
    "prereqs": ["pol-e-g3-u4"],
    "prereqs_name": "公共生活靠大家",
    "prereqs_meta": "pol-e-g3-u4",
    "leads_to": ["pol-e-g4-u2"],
    "next_meta": "pol-e-g4-u2",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "在这个班里待了四年，你有没有想过：「我们班」这三个字是怎么来的？这节课我们看班级怎么长大、班规怎么定才公平、和别的班怎么相处。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能写出一条自己班用得上的班规。",
        "objectives": "看清四件事：班里共同的东西、班规的五关、班里出了问题怎么办、和别的班怎么相处。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "班级的样子是一起做出来的：共同的记号 + 共同经历的事，攒成「我们班」。",
        "lab-1": "六件班里常遇到的事，每件三个做法。选得不太合适也不会说你错，只会告诉你还可以试试什么。",
        "module-2": "公平班规五关：一起商量、说得具体、对所有人一样、定完能执行、不合适可以改。",
        "lab-2": "你是班会主持人：先挑班里存在的问题，再挑班规写法，看看执行下去会发生什么。",
        "worked-example": "四班定班规四步：说清问题、想原因、一起定规矩、试一周再改；还看了和别的班怎么比。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "把八条做法分进「在为班级做事的」和「要调整的」两个筐，分完读一读为什么。",
        "posttest": "出现了定班规、值日同学先走、两个同学吵架，看看你能不能把今天的办法用上去。",
        "summary": "四句话：我们班四岁了、班规我们订、班里的事先做再想、我们班他们班。",
        "homework": "三层小任务，先做前两层，第三层可以留到下次班会上用。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学道德与法治「道德修养」板块在四年级的空缺，正对统编教材四年级上册「与班级共成长」（我们班四岁了、我们的班规我们订、我们班 他们班）。四年级学生已经在同一个班里待了四年，对班级有感情，但容易把「一群人在同一间教室」当成「我们班」，也容易把班规理解成「老师和大人的规矩」，只在被提醒时才想起它。所以全课先把班级拆成三个看得见的层面：一是「我们班四岁了」——共同的名字、共同的记号、一起经历过的事，让四十几个人攒出「我们班」这三个字，落点在课标「有集体意识和责任感」「友善待人」；二是「我们的班规我们订」——把「公平」这份价值判断拆成能操作的五个关卡（大家一起商量、说得具体能做、对所有人一样、定完能执行、不合适可以改），再用一条真实的班规示范「谁、什么时候、做什么、做不到怎么办」四件事怎么写清楚，重点破除「班规越严越好」这个常见误解；三是「我们班 他们班」——班级之间有比赛也有合作，看到别的班做得好可以学，但不贬低、不攀比、也不照抄。三个互动台子都能真操作：动手一是六件班里常遇到的事，每件三个做法，选完立刻展开后果（含同学的感受），反馈一律写成「这样可能会……，还可以试试……」；动手二是班规模拟台，先挑一个班里真实存在的问题，再挑一种班规写法，看这条规矩执行下去的样子；综合任务是分类判断，把八条做法分进「在为班级做事的／要调整的」两个筐。插图一律为中性简洁扁平插画，不使用真人照片风格。",
    "plan_table": """| 1 | cover | 与班级共成长 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 我们班四岁了：班级的样子，是全班一起做出来的 | 承·概念一（共同记忆与集体意识） |
| 6 | interactive | 动手一：班级小议事员，你会怎么做？ | 承·情境判断（六件事 × 三做法） |
| 7 | concept | 我们的班规我们订：一条公平的班规要过五关 | 承·概念二（公平与可执行） |
| 8 | interactive | 动手二：班规模拟台，这条班规该怎么写？ | 承·操作模拟（选问题 → 选写法 → 展开后果） |
| 9 | concept | 例题示范：四班的那次班会 | 转·重难点突破（五步示范 + 易错点） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：在为班级做事的 / 要调整的，把做法分进两个筐 | 合·迁移应用（分类判断） |
| 12 | quiz | 后测：换几个新情境，办法还在不在 | 合·后测 |
| 13 | summary | 小结：四句话，讲清怎样与班级共成长 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：我们班四岁了 / 我们的班规我们订 / 我们班 他们班 三栏\n- P5 「我们班」是怎么长出来的概念图（已生成）：共同的记号、共同经历的事、一起做的事，附中文标注\n- P7 公平班规五关与一条班规的四件事概念图（已生成）：谁、什么时候、做什么、做不到怎么办，附中文标注\n- 三张图均为中性简洁扁平教学插画，不使用真人照片风格，不含可识别的真实人物\n- 涉及矛盾与班级比较的内容以文字表达，不出现冲突、指责等画面\n- 若需补充：本班班徽、班歌与班级大事记（需班主任提供并授权后使用）",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
