# -*- coding: utf-8 -*-
"""小学道德与法治 · 为父母分担（四年级）—— 补齐知识树「中华优秀传统文化」空缺

学科语气（道德与法治）：情境案例驱动，情感共鸣 + 价值判断，用真实的家庭场景；
结论落在「应该怎么做、为什么」，不做道德说教，不用「要孝顺」这类空话收尾。
四年级要具体：家务怎么做才真的帮上忙、想做的事和家里的安排冲突了怎么办、
一个人在家遇到陌生人敲门怎么办。

内容落点（对应统编四上「为父母分担」三课）：
  ① 少让父母为我操心：父母操的心很具体——担心你路上不安全、担心你一个人在家、
     担心你睡不够。我做不到的大事很多，可我能做到的小事也很多：出门说一声去哪儿几点回、
     自己定闹钟起床、身体不舒服早说、一个人在家不给陌生人开门。呼应课标
     「掌握基本安全知识和技能，学会应对常见安全问题」。
  ② 这些事我来做：做家务要真的帮上忙，得走三步——先问一句「我能帮你做什么」、
     做到底、做完说一声；还要分清哪些事四年级能做，哪些事现在做了反而让大人更担心。
  ③ 我的家庭贡献与责任：家庭里每个人都有责任，我的贡献不只是干活，还包括好好说话、
     把话说清楚、家里的事也说说自己的想法。

三个互动台子都能真操作：
  动手一 = 家庭情境卡：六件家里常遇到的事 × 三个做法 → 展开后果与家人的感受；
  动手二 = 家务模拟台：选一件家务 → 选一种做法 → 看是真帮上忙还是要调整；
  综合任务 = 把八条做法分进「真帮上忙的／要调整的」两个筐。
插图一律中性简洁扁平插画，不使用真人照片风格。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g4-u2"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "爸爸妈妈每天操心的事，其实都很具体：你出门有没有说一声，一个人在家会不会害怕，晚上睡得够不够，书包里东西带齐了没有。这些心，你其实可以替他们分掉一部分。这节课我们做三件事。第一件，少让父母为我操心，看看我能做到的小事有哪些，还有一个人在家的时候要注意什么。第二件，这些事我来做，看看家务怎样做才真的帮上忙。第三件，我的家庭贡献与责任，想一想我在家里算不算一个有用的人。带着这三个问题，我们开始。",
    "problem-anchor": "开始之前，先选一个你最想弄清楚的问题。是想知道怎样让父母少操一份心，还是想知道家务怎么做才真的帮上忙；是想知道自己想做的事和家里的安排冲突了怎么办，还是想知道一个人在家该注意什么。选好以后，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出三到五件自己能做的、让父母少操心的小事，比如出门说一声去哪儿几点回、自己定闹钟起床、身体不舒服早说。第二，能说出做家务的三步：先问一句要做什么、做到底、做完说一声，并且知道哪些事四年级能做、哪些事现在做了反而让大人更担心。第三，掌握几条基本的安全做法：一个人在家不给不认识的人开门，湿手不碰插座，闻到煤气味先开窗离开再告诉大人。第四，知道自己在家里的贡献不只是干活，还包括好好说话、把话说清楚、家里的事也说说自己的想法。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先来算一笔账：爸爸妈妈每天到底在担心什么？他们担心你上学路上不安全，担心你一个人在家的时候有人敲门，担心你睡不够上课没精神，担心你忘了带作业本。这些担心，很多都和你有关，也很多都是你能替他们分掉的。哪些事你做不到？上班、做饭、挣钱，你确实做不到。哪些事你做得到？出门前说一声我去哪儿、和谁一起、几点回来，这一句话就能让妈妈少想好半天；自己定好闹钟按时起床，妈妈就不用一遍一遍来叫你；身体不舒服早点说，就不用等难受得厉害了才去医院；写作业自己安排好，就不用大人一遍一遍催。还有几件更要紧的事，属于安全的知识和技能，一定要记住。一个人在家的时候，门铃响了先问是谁，不认识的人不开门；有人说他是修水管的、抄表的、送快递的，也不要开，先给爸爸妈妈打个电话。家里的插座，湿手不要去碰；闻到厨房有煤气味，先开窗，再离开厨房，然后告诉大人，千万不要在里面开灯或者打火。走在路上，走人行道，过马路看清楚再走，不跟着不认识的人走。记住一句话：遇到危险，第一件事是先保护好自己，再去找大人。",
    "lab-1": "现在请你当一次家里的小观察员。这里有六件在家里常常遇到的事，每一件事都有三个做法。你选一个你觉得合适的，选完立刻会有一段话告诉你为什么；要是选得不太合适，也会告诉你还可以试试什么，还会告诉你家里人当时可能会怎么想。这里的做法没有分数，你可以放心试。",
    "module-2": "再来说做家务。很多同学以为，家务做得越多，就越算帮忙。其实更重要的是：怎么做才真的帮上忙。真的帮上忙，要走三步。第一步，先问一句：我可以帮你做什么？问到具体的那一件事，比如是洗碗还是收碗，是擦桌子还是倒垃圾，要做到什么程度。第二步，做到底：开始做就做完，中间不要想起别的就走开了。第三步，做完说一声：告诉大人我做完了，他们就不用再去看一遍。还有一件事要分清楚：有一些事，四年级做了反而更让人担心。比如自己去开煤气灶、自己用高压锅、爬到窗台上擦外面的玻璃、一个人搬很重的柜子——这些事不是不让你帮忙，是现在还不能做，做了会让大人心里更慌。还有，我的家庭贡献不只是干活。爸爸妈妈下班回来，你先说一句我作业写完了，他们的脚步就会轻一点；家里要决定周末去哪儿，你说说自己的想法，也是你在这个家里的一份。有的同学误认为「帮上忙的意思是我替大人做完了所有事」——其实让大人少操一份心，也是分担，而且常常是你现在就能做到的那一种。",
    "lab-2": "接下来请你当一次家里的帮忙小队长。先挑一件你想帮忙做的家务，再从三种做法里选一种，看看做完以后，是真的帮上忙了，还是需要调整。选完以后，你会看到这件事往下走的样子，也会看到还可以怎么调整。",
    "worked-example": "我们一起来看小禾经历的那一天。第一步，先看出来：妈妈早上起来脸色不好，量了体温，发烧了。第二步，问一句：小禾问妈妈，你现在最难受的是哪一件事？妈妈说，碗还在水池里，下午还得去接弟弟。第三步，做自己能做到的：小禾倒了一杯温水放在妈妈手边，把水池里的碗收进水槽泡好，又把自己剩下的作业先写完，不让妈妈再操心。第四步，把话说到位：她给正在上班的爸爸打了个电话，只说两件事——妈妈发烧了，碗我已经收好了。第五步，做不了的别硬做：小禾想给妈妈熬一锅粥，走到厨房门口停住了——开煤气这件事她还没做过。她先问了一句，妈妈说不行，她就改成把米淘好放进电饭煲，请爸爸回来按键。这一天，小禾没有做出什么大事，可妈妈下午睡了一个安稳的觉。这里有一个常见错误要提醒：有的同学误认为「为父母分担，就是把家务全包下来」。可小禾如果硬去开煤气，妈妈躺着也睡不踏实——分清哪些事能做、哪些事现在还不能做，本身就是分担的一部分。",
    "conceptest-1": "接下来用三个说法考考你，每个说法里都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件任务交给你。下面有八条在家里常做的做法，请你判断一下：哪些是真的帮上忙的，放进这一边；哪些是需要调整的，放进那一边。放好以后，再读一读为什么。",
    "posttest": "最后一轮，换几个新的家庭情境来考考你。这次会遇到一个人在家有人敲门、想说的事和家里的安排冲突、还有大人下班回来的时候，看看你能不能用上今天的办法。",
    "summary": "这节课我们记住四句话。第一句，我能做到的小事，就是替父母分掉的那一份心：出门说一声去哪儿几点回，自己定闹钟起床，身体不舒服早说。第二句，一个人在家要注意安全：不认识的人不开门，湿手不碰插座，闻到煤气味先开窗离开再告诉大人，遇到危险先保护好自己。第三句，做家务要走三步：先问一句、做到底、做完说一声；现在还不能做的事，先问一问，别硬做。第四句，我的家庭贡献不只是干活：好好说话、把话说清楚、家里的事也说说自己的想法。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出三件你能做的、让父母少操心的小事，各写一句话；再写出做家务的三步。第二层能力应用，动手做：本周在家里认真做一件家务，先问一句要做什么，做到底，做完告诉大人一声，再写一句话说说大人当时的反应。第三层迁移挑战，选做：找一件你想做、但家里的安排不一样的事，把当时的想法和最后商量的结果写下来，再说一说如果重来一次你会从哪一句开始说。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 少让父母为我操心", "lab-1": "动手一 家庭情境卡",
    "module-2": "概念二 这些事我来做", "lab-2": "动手二 家务模拟台",
    "worked-example": "例题示范 妈妈发烧那天", "conceptest-1": "概念测试",
    "synthesis": "综合任务 真帮上忙的 / 要调整的", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：家庭情境卡（六件家里常遇到的事 × 三个做法，含家人的感受） ──
SCENES = [
    {"id": "s1", "t": "周末我想和同学去打球，可妈妈说那天要去外婆家", "opts": [
        {"k": "a", "t": "先跟妈妈说清我想去打球这件事，再一起商量能不能改个时间或者打完球再去", "ok": True,
         "fb": "你把自己的想法说清楚了，也留了商量的余地。妈妈知道你并不是不想去外婆家，只是那天有约。"},
        {"k": "b", "t": "什么也不说，到了那天就跟着去，一路上都不高兴", "ok": False,
         "fb": "这样可能会让妈妈以为你不想去外婆家，却又不知道为什么，她自己心里也别扭。还可以试试：提前一天把你的事说一句，商量改时间比憋着容易多了。"},
        {"k": "c", "t": "直接说：我不去，你们自己去吧", "ok": False,
         "fb": "这样可能会让妈妈很为难，也可能让外婆白等一场。还可以试试：先说「我想去打球」，再说「我也想去外婆家」，两件事摆在一起商量。"},
    ]},
    {"id": "s2", "t": "放学后同学约你去他家写作业，可你平时是按时回家的", "opts": [
        {"k": "a", "t": "先给妈妈打个电话，说清去哪儿、和谁一起、大概几点回来，她同意再去", "ok": True,
         "fb": "三件事说清楚，妈妈就不用在家门口一遍遍看表了。这一句话，就是你在替她分掉一份担心。"},
        {"k": "b", "t": "先去了再说，回家再解释", "ok": False,
         "fb": "这样可能会让妈妈在家等得心里发慌，甚至跑出来找你。还可以试试：出门前打个电话，只要一分钟。"},
        {"k": "c", "t": "不去了，也不告诉任何人，自己绕着路走回家", "ok": False,
         "fb": "这样可能会让家里以为你早就到家了，你晚了也没人知道。还可以试试：把想去的想法说出来，商量一个家里都放心的办法。"},
    ]},
    {"id": "s3", "t": "你想看的节目和爸爸要看的节目不一样，遥控器就一个", "opts": [
        {"k": "a", "t": "先问问爸爸想看多久，再说我想看的那一段是几点，商量着来", "ok": True,
         "fb": "问一句、说清时间，两件事往往都能安排开。爸爸也会发现你是在好好商量，不是非要抢。"},
        {"k": "b", "t": "抢过来先换成自己想看的", "ok": False,
         "fb": "这样可能会让爸爸觉得累了一天还得让着你，两个人都不痛快。还可以试试：先说「我想看的那段是八点」，再说「八点前你看」。"},
        {"k": "c", "t": "什么也不说，回房间生气", "ok": False,
         "fb": "这样可能会让爸爸根本不知道你想要什么，你自己也越想越委屈。还可以试试：把想要的那一句说出来，哪怕只是「今天这一集是大结局」。"},
    ]},
    {"id": "s4", "t": "妈妈让你先写完作业再下楼玩，可你已经和同学约好了时间", "opts": [
        {"k": "a", "t": "跟妈妈说清约的是几点，再一起看看作业能不能先做完要交的那一部分", "ok": True,
         "fb": "把时间说出来，事情就有得商量。妈妈常常不是不让你玩，是怕你作业拖到很晚。"},
        {"k": "b", "t": "趁妈妈不注意就溜下楼", "ok": False,
         "fb": "这样可能会让妈妈发现你不见了，急得到处找，回来以后两个人都不好受。还可以试试：先说清几点回来，再请她看你怎么安排作业。"},
        {"k": "c", "t": "留在家里写，但一直磨磨蹭蹭，写到很晚", "ok": False,
         "fb": "这样可能会让你既没玩成，作业也没写好，睡觉还晚了。还可以试试：先把要交的那一部分做完，剩下的回来再补。"},
    ]},
    {"id": "s5", "t": "你一个人在家，门铃响了，外面的人说是修水管的", "opts": [
        {"k": "a", "t": "不出声，先给爸爸妈妈打电话说这件事，等他们回来再开门", "ok": True,
         "fb": "不开门、先告诉大人，这是最稳妥的做法。真的有人来修，爸爸妈妈会比你更清楚该怎么安排。"},
        {"k": "b", "t": "打开门让他进来看看，反正他说是修水管的", "ok": False,
         "fb": "这样可能会让你遇到意想不到的危险，爸爸妈妈知道了会很后怕。还可以试试：不管他怎么说，都先不开门，先打个电话。"},
        {"k": "c", "t": "在门里大声喊：家里没人，你走吧", "ok": False,
         "fb": "这样可能会让外面的人知道你确实一个人在家，反而更不安全。还可以试试：不出声，或者只说一句「我爸爸在忙，你晚点来」。"},
    ]},
    {"id": "s6", "t": "你在客厅闻到一股煤气味，家里只有你一个人", "opts": [
        {"k": "a", "t": "先开窗通风，再离开屋子，到外面给大人打电话", "ok": True,
         "fb": "开窗、离开、打电话，这三步都做对了。这种时候，保护好自己是最要紧的事。"},
        {"k": "b", "t": "先在屋里到处找是从哪里漏出来的", "ok": False,
         "fb": "这样可能会让你在危险的地方待得太久。还可以试试：先开窗、先出去，再告诉大人，找漏气的位置交给他们做。"},
        {"k": "c", "t": "先打开灯看看厨房怎么了", "ok": False,
         "fb": "这样可能会引燃屋里的气体，非常危险。还可以试试：不开灯、不打火，先开窗，再离开屋子打电话。"},
    ]},
]

# ── 动手二：家务模拟台（六件家务 × 三种做法） ──
SCHEMES = [
    {"k": "a", "n": "先问一句「我能帮你做什么」，问到具体那一件，做到底，做完说一声", "ok": True},
    {"k": "b", "n": "不问，按自己想的做，做到一半想起别的事就放下了", "ok": False},
    {"k": "c", "n": "一直等大人叫，叫一次动一下，不叫就一直不动", "ok": False},
]
TASKS = [
    {"id": "t1", "n": "收拾自己的书桌和书包", "out": {
        "a": "第二天早上，书包里东西齐了，作业本、水杯、跳绳都在。妈妈不用再翻一遍你的书包，出门前那几分钟轻松了不少。",
        "b": "书桌收了一半，抽屉里的本子摊在外面，第二天要交的作业本怎么也找不到。妈妈只好又陪你翻了十分钟。还可以试试：先把要交的作业本一本一本放进书包，再整理桌子。",
        "c": "妈妈叫了三次，你才把桌子上的几本书摞起来，剩下的还摊着。她看着那半张桌子，自己又收拾了一遍。还可以试试：每天放学前花三分钟，把明天要用的先装进书包。"}},
    {"id": "t2", "n": "洗自己的袜子", "out": {
        "a": "你问了妈妈用哪块肥皂、要搓几遍，洗完拧干晾在阳台上，还跟她说了一声洗好了。第二天鞋子里有一双干爽的袜子，妈妈没再提过这件事。",
        "b": "肥皂抹了两下就冲掉了，水开得很大，地上全是水，你想起作业还没写就走开了。妈妈回来拖了地，又把袜子重洗了一遍。还可以试试：一次只做这一件事，洗完再走。",
        "c": "妈妈叫了你两回，你才把袜子扔进盆里泡着，泡到晚上已经没味儿了。最后还是妈妈洗的。还可以试试：给自己定一个固定的时间，比如每天洗澡前五分钟。"}},
    {"id": "t3", "n": "晚饭前摆碗筷、擦桌子", "out": {
        "a": "你先问了要摆几双筷子、汤碗放哪儿，摆好后又擦了一遍桌子，跟妈妈说可以吃饭了。一家人坐下就能吃，妈妈少跑了两趟。",
        "b": "筷子摆了一半，你想起要回个消息，就坐在沙发上了。开饭时大家还得自己找筷子。还可以试试：摆完最后一双再去做别的事，就一小会儿。",
        "c": "妈妈喊「吃饭了」，你才慢吞吞起来拿了两双筷子，剩下的她一边端菜一边摆。还可以试试：看到妈妈开始炒菜，就先去把碗筷数出来。"}},
    {"id": "t4", "n": "把家里的垃圾拿下去倒", "out": {
        "a": "你问清是哪一袋、扔到楼下哪个桶，拎着袋子下去，回来跟妈妈说倒好了。厨房一下清爽了，妈妈洗碗的时候也顺手。",
        "b": "你拎着袋子走到楼下，看到同学在玩，就把袋子放在楼梯口忘了。第二天邻居帮忙扔掉，妈妈还道了歉。还可以试试：先扔进桶，再去找同学玩。",
        "c": "厨房那袋垃圾放了两天，直到妈妈叫你去倒。她每天做饭都得绕着它走。还可以试试：把它和一件固定的事绑在一起，比如晚饭后出门散步时顺手带下去。"}},
    {"id": "t5", "n": "叠衣服", "out": {
        "a": "你先问清楚哪些叠成方块、哪些挂起来，一件一件叠好放进柜子，还跟妈妈说放好了。第二天早上找衣服不用翻箱。",
        "b": "叠了五六件就丢在沙发上，你自己去看书了。妈妈回来重新叠了一遍，还要把你的书合上。还可以试试：叠完再去做别的，或者先说好「我把这一摞叠完」。",
        "c": "妈妈叫了几次，你才把自己的两件衣服叠好，剩下的还堆在沙发上。还可以试试：先挑自己最会叠的那一类，比如袜子，做完了再说。"}},
    {"id": "t6", "n": "浇花，再给弟弟妹妹读一个故事", "out": {
        "a": "你问了妈妈哪些花要浇、浇多少，浇完把水壶放回原处，又给弟弟读完了一本书，跟妈妈说都做完了。弟弟安安静静，妈妈能歇一会儿。",
        "b": "水浇得太满，阳台地上湿了一片，故事读到一半手机响了。弟弟自己跑去找妈妈。还可以试试：一次只做一件事，读完故事再去拿手机。",
        "c": "弟弟来找你读故事，你说等一会儿，一直等到妈妈把碗洗完自己来读。还可以试试：挑一个确定的时间，比如每天晚饭后十分钟，专门读给他听。"}},
]

# ── 综合任务：真帮上忙的 / 要调整的（八条做法分进两个筐） ──
SORT_ITEMS = [
    {"id": "k1", "t": "出门前说一句我去哪儿、和谁一起、几点回来", "bin": "good",
     "why": "一句话，就能让爸爸妈妈少担心好半天。这是你替他们分掉的第一份心。"},
    {"id": "k2", "t": "自己定好闹钟，早上按时起床", "bin": "good",
     "why": "不用人一遍一遍来叫，这一份力就省下来了。"},
    {"id": "k3", "t": "身体不舒服早一点说出来，不硬撑着", "bin": "good",
     "why": "早点说，大人心里有数，也能早点想办法；硬撑着反而让人更担心。"},
    {"id": "k4", "t": "做家务先问一句「我能帮你做什么」，做到底，做完说一声", "bin": "good",
     "why": "问清楚、做完整、说一声，这三步下来才真叫帮上忙。"},
    {"id": "k5", "t": "一个人在家时，不认识的人按门铃就不开门，先给爸爸妈妈打电话", "bin": "good",
     "why": "先保护好自己，再找大人，这是最稳妥的做法。"},
    {"id": "k6", "t": "想做的事和家里的安排不一样，就先说清自己的想法，再一起商量", "bin": "good",
     "why": "说清楚再商量，事情往往两边都能安排开，也不会让谁白等一场。"},
    {"id": "k7", "t": "自己动手去开煤气灶、用高压锅，想给大人一个惊喜", "bin": "tune",
     "why": "这样可能会让你遇到危险，大人知道了会非常后怕。还可以试试：先问一句能不能做；如果是想熬粥，可以先把米淘好，请大人来按键。"},
    {"id": "k8", "t": "大人问「今天在学校怎么样」，只回一句「还行」，就回房间了", "bin": "tune",
     "why": "这样可能会让爸爸妈妈想知道你的情况，又怕问多了你嫌烦，只好不问。还可以试试：挑一件事说给他们听，哪怕只是「今天体育课跑了八百米」。"},
]
SORT_BIN = {"good": "真帮上忙的", "tune": "要调整的"}

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g4-u2 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 家庭情境卡：六件事 × 三个做法 → 展开后果与家人的感受（不判错、不贴标签）
   3) 家务模拟台：选家务 → 选做法 → 看是真帮上忙还是要调整
   4) 真帮上忙的 / 要调整的：八条做法分进两个筐
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

  /* ---------- 2. 家庭情境卡 ---------- */
  var SCENES = __SCENES_JSON__;
  var stage1 = document.getElementById('home-stage');
  if (stage1) {
    var curScene = null, doneScene = {};
    var out1 = document.getElementById('home-out');
    function sceneById(id) {
      for (var i = 0; i < SCENES.length; i++) { if (SCENES[i].id === id) return SCENES[i]; }
      return null;
    }
    function render1() {
      document.querySelectorAll('[data-home-case]').forEach(function (b) {
        var k = b.dataset.homeCase;
        b.classList.toggle('selected', k === curScene);
        b.classList.toggle('correct', !!doneScene[k]);
      });
      document.getElementById('home-score').textContent =
        '已经想过 ' + Object.keys(doneScene).length + ' / ' + SCENES.length + ' 件事';
    }
    function paintOptions() {
      var box = document.getElementById('home-opts');
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
    document.querySelectorAll('[data-home-case]').forEach(function (b) {
      b.addEventListener('click', function () {
        curScene = b.dataset.homeCase;
        var S = sceneById(curScene);
        if (doneScene[curScene]) {
          out1.className = 'result';
          out1.innerHTML = '<strong>这件事已经想过啦。</strong>你上次选的做法挺合适，记住它就好。';
        } else {
          out1.className = 'result warn';
          out1.innerHTML = '<strong>你遇到的是：' + S.t + '</strong><br>下面有三个做法，你选一个试试看，再想想家里人当时可能会怎么想。';
        }
        render1();
        paintOptions();
      });
    });
    render1();
  }

  /* ---------- 3. 家务模拟台 ---------- */
  var TASKS = __TASKS_JSON__;
  var SCHEMES = __SCHEMES_JSON__;
  var stage2 = document.getElementById('chore-stage');
  if (stage2) {
    var curTask = null, doneTask = {};
    var out2 = document.getElementById('chore-out');
    function taskById(id) {
      for (var i = 0; i < TASKS.length; i++) { if (TASKS[i].id === id) return TASKS[i]; }
      return null;
    }
    function render2() {
      document.querySelectorAll('[data-chore]').forEach(function (b) {
        var k = b.dataset.chore;
        b.classList.toggle('selected', k === curTask);
        b.classList.toggle('correct', !!doneTask[k]);
      });
      document.getElementById('chore-score').textContent =
        '已经试过 ' + Object.keys(doneTask).length + ' / ' + TASKS.length + ' 件家务';
    }
    document.querySelectorAll('[data-chore]').forEach(function (b) {
      b.addEventListener('click', function () {
        curTask = b.dataset.chore;
        var T = taskById(curTask);
        if (doneTask[curTask]) {
          out2.className = 'result';
          out2.innerHTML = '<strong>这件家务已经试过了：' + T.n + '</strong>你上次选的做法挺好，换一件再试试。';
        } else {
          out2.className = 'result warn';
          out2.innerHTML = '<strong>我想帮忙做的是：' + T.n + '</strong><br>下面有三种做法，你选一种，看看做完以后家里是什么样子。';
        }
        render2();
      });
    });
    document.querySelectorAll('[data-chore-way]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!curTask) {
          out2.className = 'result warn';
          out2.textContent = '先在上面点一件家务，再来选做法。';
          return;
        }
        var T = taskById(curTask);
        var k = b.dataset.choreWay;
        var isOk = false;
        for (var i = 0; i < SCHEMES.length; i++) { if (SCHEMES[i].k === k) isOk = !!SCHEMES[i].ok; }
        if (isOk) {
          doneTask[T.id] = true;
          out2.className = 'result';
          out2.innerHTML = '<strong>' + T.n + '：这样是真的帮上忙了。</strong>' + T.out[k];
        } else {
          out2.className = 'result warn';
          out2.innerHTML = '<strong>' + T.n + '：这样可能还需要调整。</strong>' + T.out[k];
        }
        render2();
      });
    });
    render2();
  }

  /* ---------- 4. 真帮上忙的 / 要调整的 ---------- */
  var ITEMS = __SORT_JSON__;
  var BINN = __SORTBIN_JSON__;
  var stage3 = document.getElementById('share-stage');
  if (stage3) {
    var pickItem = null, placed = {};
    var out3 = document.getElementById('share-out');
    function render3() {
      document.querySelectorAll('[data-share-item]').forEach(function (b) {
        var k = b.dataset.shareItem;
        b.classList.toggle('selected', k === pickItem);
        b.classList.toggle('done', !!placed[k]);
        b.disabled = !!placed[k];
      });
      document.getElementById('share-score').textContent =
        '已经放好 ' + Object.keys(placed).length + ' / ' + ITEMS.length + ' 条';
      var a = document.getElementById('share-bin-a');
      var b2 = document.getElementById('share-bin-b');
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
    document.querySelectorAll('[data-share-item]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (placed[b.dataset.shareItem]) return;
        pickItem = b.dataset.shareItem;
        out3.className = 'result warn';
        out3.innerHTML = '<strong>你选的是：' + b.textContent + '</strong><br>想一想，它是真帮上忙的，还是要调整的？';
        render3();
      });
    });
    document.querySelectorAll('[data-share-bin]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pickItem) {
          out3.className = 'result warn';
          out3.textContent = '先在上面点一条做法，再选筐。';
          return;
        }
        var it = null;
        for (var i = 0; i < ITEMS.length; i++) { if (ITEMS[i].id === pickItem) it = ITEMS[i]; }
        if (b.dataset.shareBin === it.bin) {
          placed[it.id] = true;
          out3.className = 'result';
          out3.innerHTML = '<strong>放对了，它属于「' + BINN[it.bin] + '」。</strong>' + it.why;
          pickItem = null;
          if (Object.keys(placed).length === ITEMS.length) {
            out3.className = 'result';
            out3.innerHTML = '<strong>八条全放对了！</strong>记住这句口诀：<strong>说一声、做到底、先保护好自己，' +
              '能做的小事先做起来。</strong>';
          }
        } else {
          out3.className = 'result warn';
          out3.innerHTML = '<strong>再想一想这条做法。</strong>' + it.why +
            '<br><span style="color:var(--muted)">常见错误：容易把「我确实是想帮忙」误认为「这样做就叫帮上忙」——' +
            '先看这件事有没有真的减轻大人的负担、有没有反而让人更担心，答案就清楚了。</span>';
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
        {"q": "下面哪一件事，能让爸爸妈妈少操一份心？",
         "options": [("出门前说一句我去哪儿、和谁一起、大概几点回来", True),
                     ("出门前一声不响，回来再解释", False),
                     ("出门前把手机静音，免得他们一直问", False)],
         "explain": "一句话说清去哪儿、和谁、几点回，爸爸妈妈就不用在家门口一遍一遍看表。"
                    "<strong>错因提醒：</strong>常见错误是误认为「不说他们就不会担心」——"
                    "不知道你在哪儿，才是他们最担心的时候。"},
        {"q": "你想帮妈妈洗碗，下面哪种开始的方式更好？",
         "options": [("先问一句「要洗的是哪几个碗、洗完放哪儿」，再动手", True),
                     ("直接开始洗，洗完就算帮了忙", False),
                     ("先答应下来，等会儿再说", False)],
         "explain": "问清楚再做，才不会洗完还得有人重洗一遍。"
                    "<strong>错因提醒：</strong>有的同学误认为「做家务做得越多越好」——"
                    "做得不合适，大人反而要多花时间收拾，那就不是帮忙了。"},
        {"q": "你一个人在家，门铃响了，外面的人说是来修水管的，下面哪种做法更合适？",
         "options": [("不出声，先给爸爸妈妈打个电话说这件事，等他们回来再说", True),
                     ("开门让他进来看看", False),
                     ("在门里大声说：家里没人", False)],
         "explain": "不开门、先告诉大人，是最稳妥的做法；真有人来修，爸爸妈妈比你会安排。"
                    "<strong>错因提醒：</strong>容易把「礼貌」和「开门」搞混——"
                    "隔着门不出声也算不得没礼貌，说「家里没人」反而让人知道你确实一个人在家。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "少让父母为我操心：我能做到的小事，就是替他们分掉的一份心", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们每天觉得爸爸妈妈管得很多（And）；可是很少想过，他们那些提醒背后是一份担心，而这份担心有一部分是可以替他们分掉的（But）；所以这节课先算一算：哪些事我确实做不到，哪些事我今天就能做到（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">爸爸妈妈担心的都是很具体的事：路上安不安全、一个人在家怕不怕、睡够没睡够、书包带齐了没有。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>我做不到的</strong></p>
            <p style="color:var(--muted)">上班、做饭、挣钱、照顾生病的家人。这些现在确实还做不到，不必勉强自己。</p>
          </div>
          <div class="inner-card">
            <p><strong>我今天就能做到的</strong></p>
            <p style="color:var(--muted)">出门说一声去哪儿、和谁、几点回；自己定闹钟起床；身体不舒服早说；作业自己安排好。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="我做到的小事与爸爸妈妈少操的那份心对照图：出门说一声、自己定闹钟、不舒服早说、自己安排作业，附中文标注">
          <figcaption>概念图：我做到的小事 · 爸爸妈妈少操的那份心（教学示意图，中性简洁扁平插画）</figcaption>
        </figure>
        <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(78,205,196,.45)">
          <p><strong>还要记住几条安全做法</strong></p>
          <p style="color:var(--muted)">一个人在家，不认识的人按门铃就不开门，先给爸爸妈妈打电话 · 湿手不碰插座 · 闻到煤气味先开窗、再离开厨房，不开灯不打火，然后告诉大人 · 走人行道，过马路看清楚再走。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「让父母放心，就要什么都自己扛着」。可身体不舒服还硬撑、遇到害怕的事一声不吭，只会让大人事后更担心。<strong>遇到危险，第一件事是先保护好自己，再去找大人。</strong></p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "同一句「早点回来」，可以听成「又在管我」，也可以听成「她在家里等着我」。听成哪一种，你接下来做的事会很不一样。"},
    {"lens": "解释它", "text": "为什么说一句「我去哪儿、几点回」这么有用？因为担心大多来自不知道；知道了，那份担心自然就小了一半。"},
    {"lens": "迁移它", "text": "这套办法在家里和在学校都管用：和同学约着出去，也说清去哪儿、和谁、几点回，家里和老师都会放心。"},
])}
    ''', tag="概念一"))

    case_btns = "\n".join(
        f'            <button class="choice" data-home-case="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in SCENES
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：家庭情境卡，你会怎么做？", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一件在家里常常遇到的事，再从三个做法里选一个。<strong>选得好会告诉你为什么，选得不太合适也会告诉你还可以试试什么，还会告诉你家里人当时可能会怎么想。</strong></p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 家里遇到的这件事</div>
          <div class="grid" id="home-stage">
{case_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 我可以怎么做</div>
          <div class="grid" id="home-opts">
            <span style="color:var(--muted);font-size:14px">先在上面点一件事，这里就会出现三个做法。</span>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">想过几件事</span><span class="v" id="home-score">已经想过 0 / 6 件事</span></div>
          </div>
          <p class="result warn" id="home-out" style="margin-top:12px">先点一件家里可能遇到的事。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💛</span><div><strong>说给你听：</strong>这里的做法没有分数。有些做法只是会让家里人不太放心，换一个试试就好。家里的情况各家不一样，拿不准的时候，问一问爸爸妈妈最合适。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "这些事我来做：做家务要走三步，还要分清能做和不能做", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">做家务，不是做得越多越算帮忙，而是<strong>怎么做才真的帮上忙</strong>。真的帮上忙，要走三步。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先问一句：</strong>问清是洗碗还是收碗、擦桌子还是倒垃圾，要做到什么程度。</div></div>
          <div class="step"><span class="n">2</span><div><strong>做到底：</strong>开始做就做完，中间不要想起别的就走开了。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>做完说一声：</strong>告诉大人我做好了，他们就不用再去看一遍。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="做家务三步概念图：先问一句、做到底、做完说一声；旁边分成四年级能做的和现在还不能做的，附中文标注">
          <figcaption>概念图：做家务的三步 · 四年级能做的和现在还不能做的（教学示意图，中性简洁扁平插画）</figcaption>
        </figure>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>有些事，现在做了反而更让人担心</strong></p>
          <p style="color:var(--muted)">自己开煤气灶 · 自己用高压锅 · 爬到窗台上擦外面的玻璃 · 一个人搬很重的柜子。这些不是不让你帮忙，是现在还不能做——想做的时候，先问一句。</p>
        </div>
        <div class="inner-card">
          <p><strong>我的家庭贡献，不只是干活</strong></p>
          <p style="color:var(--muted)">爸爸妈妈下班回来，你先说一句「我作业写完了」，他们的脚步就会轻一点；家里商量周末去哪儿，你说说自己的想法，也是你在这个家里的一份。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「帮上忙，就是我替大人把所有事都做完」。其实让大人少操一份心，也是一种分担——而且常常是你现在就能做到的那一种。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "「我问了要不要帮忙」和「我做完告诉他一声」，中间差着一步「做到底」。差这一步，大人还是得自己去看一遍。"},
    {"lens": "比较它", "text": "同样是想熬粥：一种是直接去开煤气，一种是把米淘好请爸爸按键。两种都是心意，可只有后面这一种，妈妈躺着才睡得踏实。"},
    {"lens": "迁移它", "text": "这套办法在学校也管用：老师让小组做一件事，先问清要做什么、做到底、做完说一声，比闷头做完再说更让人放心。"},
])}
    ''', tag="概念二"))

    task_btns = "\n".join(
        f'            <button class="choice" data-chore="{t["id"]}" style="text-align:left">我想帮忙：{t["n"]}</button>'
        for t in TASKS
    )
    scheme_btns = "\n".join(
        f'            <button class="choice" data-chore-way="{s["k"]}" style="text-align:left">{s["n"]}</button>'
        for s in SCHEMES
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：家务模拟台，这样做是真的帮上忙了吗？", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">你现在是家里的帮忙小队长。先挑一件你想帮忙做的家务，再从三种做法里选一种，看看做完以后家里是什么样子。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 我想帮忙做的家务</div>
          <div class="grid" id="chore-stage">
{task_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 我怎么做</div>
          <div class="grid">
{scheme_btns}
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">试过几件家务</span><span class="v" id="chore-score">已经试过 0 / 6 件家务</span></div>
          </div>
          <p class="result warn" id="chore-out" style="margin-top:12px">先在上面点一件家务。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧩</span><div><strong>想一想：</strong>三种做法里，为什么「先问一句、做到底、做完说一声」总是最受欢迎？因为它让大人省下的不只是力气，还有那一份「还得再去看看」的心。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：妈妈发烧那天", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>那天早上，妈妈起来脸色不好，量了体温，发烧了。爸爸已经上班走了，弟弟下午才放学。请你看看小禾这一天是怎么做的。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先看出来：</strong>妈妈脸色不好、量了体温才知道是发烧，不是「妈妈今天有点懒」。</div></div>
          <div class="step"><span class="n">2</span><div><strong>先问一句：</strong>小禾问妈妈，你现在最难受的是哪一件事？妈妈说，碗还在水池里，下午还得去接弟弟。</div></div>
          <div class="step"><span class="n">3</span><div><strong>做自己能做到的：</strong>倒一杯温水放在妈妈手边；把水池里的碗收进水槽泡好；自己剩下的作业先写完，不让妈妈再操心。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>把话说到位：</strong>给上班的爸爸打了个电话，只说两件事——妈妈发烧了，碗我已经收好了。</div></div>
        </div>
        <div class="inner-card">
          <p><strong>第五步：做不了的别硬做</strong></p>
          <p style="color:var(--muted)">小禾想给妈妈熬一锅粥，走到厨房门口停住了——开煤气这件事她还没做过。她先问了一句，妈妈说不行，她就改成把米淘好放进电饭煲，请爸爸回来按键。这一天她没做出什么大事，可妈妈下午睡了一个安稳的觉。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「为父母分担，就是把家务全包下来」。可小禾如果硬去开煤气，妈妈躺着也睡不踏实——<strong>分清哪些能做、哪些现在还不能做，本身就是分担的一部分。</strong></p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "关于帮爸爸妈妈做家务，下面哪句话说得对？",
         "options": [("先问一句要做什么，做到底，做完说一声，才算真的帮上忙", True),
                     ("做得越多就越算帮忙，做成什么样没关系", False),
                     ("现在还不能做的事，偷偷学着做，给大人一个惊喜", False)],
         "explain": "问清楚、做完整、说一声，大人省下的不只是力气，还有那一份「还得再去看看」的心。"
                    "<strong>错因提醒：</strong>常见错误是误认为「心意到了就算帮上忙」——"
                    "做到一半走开，大人反而要多花时间收拾，那就不是帮忙了。"},
        {"q": "你想周末和同学去打球，可家里那天安排了去外婆家，下面哪种做法更好？",
         "options": [("先把自己的想法说清楚，再一起商量能不能改时间，或者打完球再去", True),
                     ("什么也不说，跟着去，一路上沉着脸", False),
                     ("直接说：我不去，你们自己去吧", False)],
         "explain": "说清楚再商量，两件事往往都能安排开，也不会让外婆白等一场。"
                    "<strong>错因提醒：</strong>有的同学误认为「不说就是不添麻烦」——"
                    "憋着不说，家里还是会觉得你不对劲，只是不知道问题在哪儿。"},
        {"q": "你一个人在家闻到一股煤气味，下面哪种做法更合适？",
         "options": [("先开窗通风，再离开屋子，到外面给大人打电话", True),
                     ("先打开灯，看看厨房里是怎么了", False),
                     ("先在屋里找一找是哪里漏出来的", False)],
         "explain": "开窗、离开、打电话，这三步都做对了；这种时候，先保护好自己最要紧。"
                    "<strong>错因提醒：</strong>容易把「找原因」摆在「保护自己」前面——"
                    "在漏气的屋子里开灯，可能会引燃气体，非常危险。"}
    ], tag="概念测试"))

    item_btns = "\n".join(
        f'            <button class="sort-item" data-share-item="{it["id"]}">{it["t"]}</button>' for it in SORT_ITEMS
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：真帮上忙的 / 要调整的，把做法分进两个筐", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一条做法，再点它应该进的筐：<strong>真帮上忙的</strong>放一边，<strong>要调整的</strong>放另一边。</p>
        <div class="lab-panel">
          <div class="sort-bank" id="share-stage">
{item_btns}
          </div>
          <div class="grid grid-2" style="margin-top:14px">
            <button class="choice" data-share-bin="good" style="text-align:center">真帮上忙的</button>
            <button class="choice" data-share-bin="tune" style="text-align:center">要调整的</button>
          </div>
          <div class="sort-bins">
            <div class="sort-bin" id="share-bin-a"><h4>真帮上忙的</h4></div>
            <div class="sort-bin" id="share-bin-b"><h4>要调整的</h4></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">分类进度</span><span class="v" id="share-score">已经放好 0 / 8 条</span></div>
          </div>
          <p class="result warn" id="share-out" style="margin-top:12px">先在上面点一条做法。</p>
        </div>
        <div class="inner-card">
          <p><strong>分完之后，想一想：</strong></p>
          <p style="color:var(--muted)">「真帮上忙的」这一边里，你最想先做哪一条？写在下面，再说一说为什么选它。</p>
          <textarea id="syn-answer" rows="3" placeholder="我最想先做……，因为……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，办法还在不在", TTS["posttest"], [
        {"q": "你一个人在家写作业，门外有人敲门说是抄表的，下面哪种做法更好？",
         "options": [("不开门，先给爸爸妈妈打电话说这件事", True),
                     ("隔着门大声说：家里没人", False),
                     ("开门让他进来看一眼就走", False)],
         "explain": "不开门、先告诉大人，是最稳妥的做法；真有人来抄表，爸爸妈妈比你会安排。"
                    "<strong>错因提醒：</strong>常见错误是误认为「隔着门不出声很没礼貌」——"
                    "说「家里没人」反而让人知道你确实一个人在家，不出声或者只说一句「你晚点来」更安全。"},
        {"q": "妈妈让你先把作业写完再下楼玩，可你已经和同学约好了时间，下面哪种做法更好？",
         "options": [("跟妈妈约的是几点说清楚，再一起看看能不能先做完要交的那一部分", True),
                     ("趁妈妈不注意就溜下楼", False),
                     ("留在家里，但一直磨磨蹭蹭写到很晚", False)],
         "explain": "把时间说出来，事情就有得商量；妈妈常常不是不让你玩，是怕你作业拖到很晚。"
                    "<strong>错因提醒：</strong>容易把「留在家里」当成「听话」——"
                    "磨到很晚才写完，作业没写好、觉也睡晚了，两边都亏。"},
        {"q": "爸爸下班回来，看起来有点累，下面哪种做法更好？",
         "options": [("先说一句我作业写完了、碗我收好了，再问他要不要喝点水", True),
                     ("装作没看见，继续看自己的书", False),
                     ("马上说：今天学校要交钱", False)],
         "explain": "把已经做好的事说一声，是让大人安心，也是最省力的分担。"
                    "<strong>错因提醒：</strong>有的同学误认为「不说就等于不添麻烦」——"
                    "一句「我做完了」其实很轻，却能让爸爸的脚步轻一点。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：四句话，讲清怎样为父母分担", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>少让父母操心：</strong>出门说一声去哪儿几点回，自己定闹钟起床，身体不舒服早说。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>安全记心上：</strong>不认识的人不开门，湿手不碰插座，闻到煤气味先开窗离开再告诉大人。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>这些事我来做：</strong>先问一句、做到底、做完说一声；现在还不能做的事，先问一问，别硬做。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>我的家庭贡献：</strong>不只是干活，还有好好说话、把话说清楚、家里的事也说说自己的想法。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>一句口诀：</strong>说一声、做到底、先保护好自己，能做的小事先做起来。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「说一声、我来做、我们一起想办法」这三个说法，说清楚你家里的一件事。</p>
          <p style="color:var(--muted)">再动一动手：<strong>写一写</strong>你今天回家想先做的那一件小事，写清做什么、什么时候做、做完告诉谁。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写出三件你能做的、让父母少操心的小事，各写一句话。",
            "写出做家务的三步：先问一句、做到底、做完说一声。",
            "写出三条一个人在家要注意的安全做法。",
        ],
        [
            "本周在家里认真做一件家务：先问一句要做什么，做到底，做完告诉大人一声；再写一句话说说大人当时的反应。",
            "和家里人一起定一条「我们家的约定」（比如出门说一声、几点前回家），写清楚约定内容和做不到时怎么办。",
        ],
        [
            "找一件你想做、但家里的安排不一样的事，把当时的想法和最后商量的结果写下来，再说一说如果重来一次，你会从哪一句话开始说。",
            "问一问爸爸妈妈：他小时候在家里做过哪一件家务？把他的话记下来，和今天学的三步比一比。",
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
    "title": "为父母分担",
    "name_en": "Sharing the Load with My Parents",
    "grade": 4,
    "grade_cn": "四年级",
    "domain": "tradition-culture",
    "domain_cn": "中华优秀传统文化",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学四年级的道德与法治课：先算一笔「父母在担心什么」的账——路上安不安全、一个人在家怕不怕、睡够没睡够、书包带齐没有，落到「少让父母为我操心」上，把出门说一声去哪儿几点回、自己定闹钟起床、身体不舒服早说、作业自己安排好这些能做到的小事讲具体，并把课标要求的安全知识与技能讲清楚（一个人在家不给陌生人开门、湿手不碰插座、闻到煤气味先开窗离开再告诉大人，遇到危险先保护好自己再找大人）；再说「这些事我来做」——做家务要走三步：先问一句、做到底、做完说一声，并分清四年级能做的和现在做了反而更让人担心的事；最后落到「我的家庭贡献与责任」——贡献不只是干活，还包括好好说话、把话说清楚、家里的事也说说自己的想法。全课以真实家庭情境与可操作的选择为主，三个互动台子分别是家庭情境卡（六件事 × 三做法，展开后果与家人的感受）、家务模拟台（选家务 → 选做法 → 看是真帮上忙还是要调整）、以及把八条做法分进「真帮上忙的／要调整的」两个筐。",
    "tags": ["为父母分担", "少让父母为我操心", "这些事我来做", "我的家庭贡献与责任", "家庭责任", "安全知识与技能", "四年级", "中华优秀传统文化"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学「中华优秀传统文化」——掌握基本安全知识和技能，学会应对常见安全问题，并在家庭生活中承担自己的一份责任；对应统编《道德与法治》四年级上册「为父母分担」：少让父母为我操心、这些事我来做、我的家庭贡献与责任。",
    "hero_question": "爸爸妈妈每天在担心什么？其中哪一份心，是我能替他们分掉的？",
    "hero_alt": "为父母分担知识结构图：少让父母为我操心、这些事我来做、我的家庭贡献与责任 三栏",
    "hero_caption": "为父母分担：少让父母为我操心 · 这些事我来做 · 我的家庭贡献与责任（说一声、做到底、先保护好自己）",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "怎样让爸爸妈妈少操一份心？", "d": "我今天就能做到的小事", "v": "怎样让爸爸妈妈少操一份心"},
        {"t": "家务怎么做，才真的帮上忙？", "d": "先问一句、做到底、做完说一声", "v": "家务怎么做才真的帮上忙"},
        {"t": "我想做的事和家里的安排不一样，怎么办？", "d": "打球、去同学家、看节目", "v": "我想做的事和家里的安排不一样怎么办"},
        {"t": "一个人在家的时候要注意什么？", "d": "有人敲门、电器、煤气", "v": "一个人在家的时候要注意什么"},
    ],
    "objectives": [
        "能说出三到五件自己能做的、让父母少操心的小事，比如出门说一声去哪儿几点回、自己定闹钟起床、身体不舒服早说",
        "能说出做家务的三步（先问一句、做到底、做完说一声），并分清四年级能做的和现在做了反而更让人担心的事",
        "掌握几条基本安全做法：一个人在家不给不认识的人开门，湿手不碰插座，闻到煤气味先开窗、离开再告诉大人",
        "知道自己在家里的贡献不只是干活，还包括好好说话、把话说清楚、家里的事也说说自己的想法",
    ],
    "objectives_plain": [
        "能说出三到五件让父母少操心的小事，并愿意先做起来",
        "能说出做家务的三步，知道哪些事现在还不能做，先问再动手",
        "记住几条安全做法：不给陌生人开门、湿手不碰插座、闻到煤气味先离开再告诉大人",
        "知道自己的家庭贡献不只是干活，还有好好说话、把话说清楚",
    ],
    "standards": [
        {"content": "掌握基本安全知识和技能，学会应对常见安全问题。",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学 中华优秀传统文化"},
        {"content": "少让父母为我操心；这些事我来做；我的家庭贡献与责任",
         "source": "统编《道德与法治》四年级上册「为父母分担」"},
    ],
    "prereqs": ["pol-e-g4-u1"],
    "prereqs_name": "与班级共成长",
    "prereqs_meta": "pol-e-g4-u1",
    "leads_to": ["pol-e-g4-u3"],
    "next_meta": "pol-e-g4-u3",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "爸爸妈妈担心的事都很具体。这节课我们算一算：哪一份心是我能替他们分掉的。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能说出自己回家想先做的那一件小事。",
        "objectives": "看清四件事：让父母少操心的小事、家务的三步、一个人在家怎么注意安全、我的家庭贡献是什么。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "父母的担心大多来自不知道；说一声、自己定闹钟、不舒服早说，就是把那份心分掉一部分。",
        "lab-1": "六件家里常遇到的事，每件三个做法。选得不太合适也不会说你错，会告诉你家里人当时可能会怎么想。",
        "module-2": "做家务三步：先问一句、做到底、做完说一声；现在还不能做的事，先问一问，别硬做。",
        "lab-2": "你是帮忙小队长：先挑家务，再挑做法，看看做完家里是什么样子。",
        "worked-example": "妈妈发烧那天五步：先看出来、先问一句、做自己能做的、把话说到位、做不了的别硬做。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "把八条做法分进「真帮上忙的」和「要调整的」两个筐，分完读一读为什么。",
        "posttest": "出现了陌生人敲门、约好玩的时间、爸爸下班回来，看看你能不能把今天的办法用上去。",
        "summary": "四句话：少让父母操心、安全记心上、这些事我来做、我的家庭贡献。",
        "homework": "三层小任务，先做前两层；第二层要请家里人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学道德与法治「中华优秀传统文化」板块在四年级的空缺，正对统编教材四年级上册「为父母分担」（少让父母为我操心、这些事我来做、我的家庭贡献与责任）。四年级学生开始有能力在家里做点事，但很容易走进两个误区：一是把「分担」理解成「多干活」，做得不合适反而让大人多花时间收拾；二是把「不让父母操心」理解成「什么都自己扛」，不舒服硬撑、遇到害怕的事不说，结果让人更担心。所以全课从一笔具体的账开始：爸爸妈妈到底在担心什么——路上安不安全、一个人在家怕不怕、睡够没睡够、书包带齐没有；再落到「少让父母为我操心」，把出门说一声去哪儿几点回、自己定闹钟起床、身体不舒服早说、作业自己安排好这些能做到的小事讲具体，同时把课标要求的基本安全知识与技能落在这个场景里：一个人在家不给不认识的人开门、湿手不碰插座、闻到煤气味先开窗离开再告诉大人、遇到危险先保护好自己再找大人。第二层是「这些事我来做」——把「帮上忙」拆成可操作的三步（先问一句、做到底、做完说一声），并明确分清四年级能做的和现在做了反而更让人担心的事（开煤气、用高压锅、爬窗台、搬重物），破除「做得越多越好」这个常见误解。第三层是「我的家庭贡献与责任」——贡献不只是干活，还包括好好说话、把话说清楚、家里的事也说说自己的想法，让「分担」从家务扩展到家庭里的一份位置。三个互动台子都能真操作：动手一是六件家庭里常遇到的事，每件三个做法，选完立刻展开后果与家人当时的感受，反馈一律写成「这样可能会……，还可以试试……」；动手二是家务模拟台，先挑一件家务，再挑一种做法，看做完以后是真帮上忙还是需要调整；综合任务是分类判断，把八条做法分进「真帮上忙的／要调整的」两个筐。插图一律为中性简洁扁平插画，不使用真人照片风格。",
    "plan_table": """| 1 | cover | 为父母分担 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 少让父母为我操心：我能做到的小事，就是替他们分掉的一份心 | 承·概念一（家庭责任 + 安全知识与技能） |
| 6 | interactive | 动手一：家庭情境卡，你会怎么做？ | 承·情境判断（六件事 × 三做法，含家人感受） |
| 7 | concept | 这些事我来做：做家务要走三步，还要分清能做和不能做 | 承·概念二（可操作的三步 + 安全边界） |
| 8 | interactive | 动手二：家务模拟台，这样做是真的帮上忙了吗？ | 承·操作模拟（选家务 → 选做法 → 看后果） |
| 9 | concept | 例题示范：妈妈发烧那天 | 转·重难点突破（五步示范 + 易错点） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：真帮上忙的 / 要调整的，把做法分进两个筐 | 合·迁移应用（分类判断） |
| 12 | quiz | 后测：换几个新情境，办法还在不在 | 合·后测 |
| 13 | summary | 小结：四句话，讲清怎样为父母分担 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：少让父母为我操心 / 这些事我来做 / 我的家庭贡献与责任 三栏\n- P5 「我做到的小事 · 父母少操的那份心」对照图（已生成）：附中文标注\n- P7 做家务三步与「能做的／还不能做的」概念图（已生成）：附中文标注\n- 三张图均为中性简洁扁平教学插画，不使用真人照片风格，不含可识别的真实人物\n- 涉及家庭矛盾与安全问题（陌生人敲门、煤气泄漏）仅以文字表达，不出现危险或受伤画面\n- 若需补充：本班学生家务清单（需家长知情同意后收集），不在课件中呈现任何学生家庭信息",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
