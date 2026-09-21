# -*- coding: utf-8 -*-
"""小学道德与法治 · 面对成长中的新问题（五年级上·第1单元）—— 补齐知识树「道德修养」空缺

学科语气（道德与法治）：情境案例驱动，情感共鸣 + 价值判断，从五年级孩子成长中真实会遇到的小事讲起；
结论落在「应该怎么做、为什么」，不做道德说教、不背法条、不喊口号。

内容落点（对应统编五上第 1 单元「面对成长中的新问题」三课）：
  ① 自主选择课余生活：课余生活要自己选，也要有取舍。选择前先问三件事——我自己想不想、今天有没有
     必须先做完的事、家里人和同伴怎么看。别人的选择可以参考，但不能替自己做决定。
  ② 学会沟通交流：有分歧、被误解的时候，把话说清楚有顺序——先说看到的事实，再说自己的感受，
     最后说出希望怎么办；不指责、不憋着。说清楚了，事情才可能往前走。
  ③ 主动拒绝烟酒与毒品：拒绝要练过才做得到。三步是——说清楚「我不」、走开、把这件事告诉
     可信任的大人。不是硬扛，也不是逞强；先保护好自己，再想别的办法。

三个互动台子都能真操作（反馈一律写成「这样可能会……，还可以试试……」）：
  动手一 = 课余生活选择台（4 张真实情境卡 × 每卡 3 个做法 → 展开对方感受与后果）；
  动手二 = 好好说话台（3 个真实分歧情境 × 3 种说话方式 = 9 组后果与对方感受）；
  综合任务 = 成长新问题三步决策台（先想清楚 → 怎么说话 → 怎么拒绝，三步选定后合成一条完整应对）。
插图一律中性简洁扁平插画，不使用真人照片风格。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g5-u1"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "升上五年级，你会发现身边的事情变得复杂了一点。同学约你去做一件事，你心里拿不准要不要去；想参加一个活动，又怕耽误作业；明明自己没做错，却被人误会了；还有人会递过来一支烟，说抽一口没事。这些事没有标准答案，可每一件都要你自己做决定。这节课我们练三件事。第一件，学会自己选择课余生活。第二件，学会把话说清楚。第三件，学会说「不」。带着这三件事，我们开始。",
    "problem-anchor": "开始之前，先选一个你真正想知道的问题。是想知道课余时间该怎么安排，还是想知道被同学误会了话该怎么说；是想知道怎么跟家里人商量，还是想知道有人递烟的时候怎么办。选好以后，就带着这个问题往下看，后面的练习都会围着它转。",
    "objectives": "这节课有四个小目标。第一，能说出课余生活要自己选择，也知道选择的时候要看三件事：我自己想不想、今天有没有必须先做完的事、家里人和同伴怎么看，并且能说清自己选的理由。第二，遇到分歧或者被误解的时候，能先说清楚看到的事实，再说自己的感受，最后说出希望怎么办，而不是指责别人或者憋着不说。第三，能说出拒绝烟酒等不良诱惑的三个办法：说清楚「我不」、走开、把这件事告诉可信任的大人。第四，遇到拿不准的事，能先把处境想清楚，再决定怎么做，并说出这样选的理由。",
    "pretest": "先做三道小题，用你现在的想法选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "先说一件每天都会发生的事：放学以后到睡觉以前，这段时间怎么过。课余生活是指上课以外可以自己安排的时间。低年级的时候，这段时间多半是家里人在安排；到了五年级，越来越多的安排要你自己拿主意。自己拿主意，不等于想干什么就干什么，而是要先把三件事看清楚：第一，我自己想不想做这件事，为什么想做；第二，今天有没有必须先做完的事，比如答应过的作业；第三，家里人和同学怎么看，他们的话可以参考，但不能替你做决定。这里有两个最容易想歪的地方。第一个，很多同学误认为「别人都去，我不去就不合群」，其实合不合群，不取决于这一件事跟不跟，而取决于你是不是把话说清楚、有没有把答应的事做到。第二个，有人误认为「我自己决定，就不用跟家里说」，可你要是事先说一声，家里人不但不会拦你，还会帮你把时间安排好。一句话记住：先看清三件事，再自己做选择；能说出理由的选择，才算真的自己选的。",
    "lab-1": "现在请你到选择台前，当一次自己的主。这里有四张情境卡，都是五年级同学真实会遇到的事。点开一张卡，会看到三个做法。你选一个，我就把接下来可能发生的事，还有对方心里会怎么想，一并告诉你。选错了也没关系，看完还可以换一个做法再试一遍。",
    "module-2": "再说第二件更常见的事：和同学、家里人有了分歧，或者被人误会了。沟通交流是指把自己的想法和感受清楚地告诉对方，同时也听一听对方的想法。很多同学以为沟通就是「把我想说的说完」，其实顺序很重要。有一个可以随身带的三步说法：第一步，先说看到的事实，不加评价，比如「我的本子被碰到了地上，还被踩了一下」；第二步，再说自己的感受，比如「我有点难过」；第三步，最后说出希望怎么办，比如「能不能帮我看看还能不能用，下次注意一下好吗」。这三步连起来，对方就知道发生了什么、你是什么心情、他可以做什么。这里有两个最容易搞混的地方。第一个，把「说事实」说成了「下判断」——说「你就是故意的」，对方第一反应是辩解，不是帮你；说「本子被踩脏了」，对方才有机会做点什么。第二个，把「不吵架」当成了「什么都不说」，可你不说，对方根本不知道你生气了，事情只会一直搁着。记住一句话：先说事实，再说感受，最后说希望；说清楚了，事情才可能往前走。",
    "lab-2": "接下来我们练说话。下面有三个真实的分歧情境，每个情境都有三种说法：一种是指责，一种是憋着不说，一种是把话说清楚。你可以随便组合着点，看看每一种说法会让对方怎么想、又会让事情往哪儿走。九种组合都试一遍之后，你就知道为什么说清楚最管用了。",
    "worked-example": "我们一起来看小北的一件事。星期五放学，同学拉他去打球，还递过来一支烟，说就抽一口没事。第一步，先想清楚自己的处境：我今天已经答应妈妈回家先写作业，而且不管谁给的烟，我都不能抽。第二步，把话说清楚：他先对约他打球的同学说，今天我答应在先，得先回家，明天放学我们一起去，行吗？同学听了，就没再拉他。第三步，拒绝那支烟：他没有接，也没有解释很多，只说了一句，我不抽烟，谢谢，我先走了，说完就走开了。第四步，把这件事告诉可信任的大人：回到家，他把有人递烟的事告诉了妈妈。这里有一个常见错误要提醒：有的同学误认为「拒绝就是跟对方吵一架」，觉得当场翻脸才算出气。可拒绝的目的是保护好自己，不是赢一场架；说清楚、走开、告诉大人，比自己站在那儿硬扛更管用，也更安全。还有一个误认为：怕被说胆小，就把烟接过来。可真正需要勇气的是说「不」，而不是跟着做。",
    "conceptest-1": "接下来用三个说法考考你，每个说法里都藏着一个容易想歪的地方。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件任务交给你，请你当一次自己的决策师。下面有一个连着发生的情境，分三步：先想清楚自己现在处在什么情况，再想怎么把话说清楚，最后想怎么拒绝那支烟。每一步都有三个做法，你各选一个，我会把你的选择拼成一条完整的应对，再告诉你这样可能会有什么结果。",
    "posttest": "最后一轮，换几个新的情境来考考你。这次会遇到被同学起外号、想跟家里人商量周末安排，还有人在楼梯间递烟，看看今天练的三件事还用不用得上。",
    "summary": "这节课我们练成三件事。第一件，自己选择课余生活：先看清三件事——我自己想不想、今天有没有必须先做完的事、家里人和同伴怎么看，然后再自己定，并且说得出理由。第二件，学会沟通交流：先说看到的事实，再说自己的感受，最后说希望怎么办；不指责，也不憋着。第三件，学会说不：说清楚「我不」，走开，把这件事告诉可信任的大人；拒绝的目的是保护好自己，不是赢一场架。三句话连起来就是：自己选、好好说、敢说不。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出选择课余生活时要看的三件事，再写出一句「先说事实、再说感受、再说希望」的完整说法。第二层能力应用，动手做：这一周记录一次你和同学或家里人意见不一样的事，写下你当时是怎么说的、对方的反应是什么，再写一句下次可以怎么说得更好。第三层迁移挑战，选做：给自己设计一张「拒绝三步卡」，把说清楚、走开、告诉大人三步写在上面，先和同桌练两遍，再说说练的时候最难的是哪一步、你是怎么过的。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 自主选择课余生活", "lab-1": "动手一 课余生活选择台",
    "module-2": "概念二 学会沟通交流", "lab-2": "动手二 好好说话台",
    "worked-example": "例题示范 小北的一次拒绝", "conceptest-1": "概念测试",
    "synthesis": "综合任务 成长新问题三步决策台", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：课余生活选择台（4 张情境卡 × 每卡 3 个做法） ──
CARDS = [
    {"id": "c1",
     "scene": "放学了，同学拉着你说：别写作业了，一起去玩一会儿。",
     "extra": "你今天还答应过妈妈，回家先把作业写完。",
     "opts": [
         {"t": "答应他去玩，作业晚上熬夜再补。", "ok": False,
          "feel": "同学当时很高兴，觉得你够朋友。",
          "out": "玩是玩痛快了，可作业写到很晚，第二天上课一直打瞌睡，还被要求重写。",
          "tip": "还可以试试：先问问自己今天有没有必须做完的事，再决定去不去。"},
         {"t": "今天我要先回家把作业做完；明天放学我们一起去，行吗？", "ok": True,
          "feel": "同学明白你不是不愿意，只是今天有安排，心里不会别扭。",
          "out": "他拿到了一个具体的时间，你也把自己答应的事做完了，两样都没耽误。",
          "tip": "还可以试试：把约好的时间记下来，说到就做到。"},
         {"t": "很不耐烦地说：不行，你别烦我。", "ok": False,
          "feel": "同学会觉得被嫌弃，心里不太舒服。",
          "out": "玩的事是躲过去了，可他下次有事可能就不找你了，两个人也慢慢远了。",
          "tip": "还可以试试：把原因说清楚，再给一个别的时间。"},
     ]},
    {"id": "c2",
     "scene": "你想参加学校的篮球队，可是每天放学都要训练到比较晚。",
     "extra": "你还没跟家里人提过这件事。",
     "opts": [
         {"t": "怕耽误学习，干脆不报名了。", "ok": False,
          "feel": "没有人反对，可你自己心里一直惦记着这件事。",
          "out": "喜欢的事没做成，学习也不一定就更专心；过一阵子你可能会后悔。",
          "tip": "还可以试试：算一算每天要花多少时间，看看作业能不能换个时间做。"},
         {"t": "不跟家里说，自己先去训练。", "ok": False,
          "feel": "家里人是从别人那里听说的，会更担心。",
          "out": "家里人不知道你去了哪里，容易着急，也可能不同意你继续去。",
          "tip": "还可以试试：先把自己的安排说给家里人听，请他们一起想办法。"},
         {"t": "把训练时间写下来，和家里人一起商量作业怎么安排。", "ok": True,
          "feel": "家里人看到你想清楚了，会更愿意支持你。",
          "out": "训练和学习都排得开，你自己也清楚每天该先做什么。",
          "tip": "还可以试试：先试两周，再把结果告诉家里人。"},
     ]},
    {"id": "c3",
     "scene": "周末的时间被各种班排得满满的，你很希望留半天自己安排。",
     "extra": "这件事你一直没跟家里人说过。",
     "opts": [
         {"t": "我想留半天做点自己喜欢的事，我打算这样安排……可以吗？", "ok": True,
          "feel": "家里人听清了你要什么，也知道你不是想偷懒。",
          "out": "半天的安排有了商量的余地，答应的那部分你也愿意做好。",
          "tip": "还可以试试：把「这半天做什么」说得再具体一点。"},
         {"t": "什么都不说，心里憋着。", "ok": False,
          "feel": "家里人以为你愿意，就按原来的安排继续。",
          "out": "你还是每天不高兴，可家里人一直不知道你为什么。",
          "tip": "还可以试试：选一个大家都不忙的时候，把想法说出来。"},
         {"t": "冲家里人大发脾气，说你们根本不管我。", "ok": False,
          "feel": "家里人会觉得突然被指责，很容易跟你吵起来。",
          "out": "本来想说「我想留半天」，结果变成了互相生气，事情还是没解决。",
          "tip": "还可以试试：先说自己的希望，再说自己打算怎么做。"},
     ]},
    {"id": "c4",
     "scene": "班上最近流行一个游戏，很多同学都在聊，你不太会玩。",
     "extra": "为了能插上话，你心里有点想跟着玩。",
     "opts": [
         {"t": "觉得大家都在做的事就一定没错，跟着做就是了。", "ok": False,
          "feel": "没有人会反对，你也不显眼了。",
          "out": "跟着做很容易，可万一这件事不合适，最后承担结果的是你自己。",
          "tip": "还可以试试：先想一想这件事合不合适，再决定跟不跟。"},
         {"t": "先问问自己想不想玩，再看看有没有别的事也能和大家一起做。", "ok": True,
          "feel": "同学会发现你也有自己擅长、喜欢的事。",
          "out": "不一定玩同一个游戏，也能玩到一起；你也没耽误自己的安排。",
          "tip": "还可以试试：把你喜欢的那件事讲给同学听。"},
         {"t": "为了能一起聊，每天偷偷玩到很晚。", "ok": False,
          "feel": "同学觉得你也在玩，话题一下多了。",
          "out": "可你第二天总是很困，也可能被家里人发现偷偷玩手机。",
          "tip": "还可以试试：先问问自己是真想玩，还是只是怕插不上话。"},
     ]},
]

# ── 动手二：好好说话台（3 个情境 × 3 种说话方式 = 9 组反馈） ──
TALK_SCENES = [
    {"id": "s1", "n": "情境一 · 本子被碰掉了",
     "d": "同桌站起来的时候碰掉了你的作业本，本子还被踩脏了。"},
    {"id": "s2", "n": "情境二 · 被误会了",
     "d": "有同学听别人说你去老师那里告了状，当着大家的面问你。"},
    {"id": "s3", "n": "情境三 · 主意没被采用",
     "d": "小组一起做手抄报，你提的主意没有被大家采用。"},
]
TALK_WAYS = [
    {"k": "blame", "n": "说法一 · 直接指责",
     "say": {"s1": "你怎么这么不小心！你就是故意的！",
             "s2": "我根本没告状！你凭什么说我！",
             "s3": "你们这样排版根本不行，还是用我的吧。"}},
    {"k": "mute", "n": "说法二 · 憋着不说",
     "say": {"s1": "什么都不说，自己把本子捡起来，一节课都不理他。",
             "s2": "不解释了，随他们怎么说。",
             "s3": "不说话了，他们爱怎么做就怎么做。"}},
    {"k": "clear", "n": "说法三 · 把话说清楚",
     "say": {"s1": "我的本子被碰掉、还被踩脏了，我有点难过。能不能帮我看看还能不能用？下次注意一下好吗？",
             "s2": "这件事不是我说的。你这么生气，是不是还有别的事？要不我们一起去问清楚。",
             "s3": "我这个想法是这样的……你们那个是怎么想的？要不两样各用一半，先试一次。"}},
]
TALK_FB = {
    "s1": {
        "blame": {"feel": "他会先想着辩解，甚至觉得你也在发火，顾不上你的本子。",
                  "out": "两个人都很生气，本子还是脏的，事情一点没解决。",
                  "tip": "还可以试试：先说发生了什么，再说自己的感受。"},
        "mute": {"feel": "他可能完全没发现已经惹到了你。",
                 "out": "你越来越生气，他还不知道为什么，两个人的关系悄悄变远了。",
                 "tip": "还可以试试：把「我不高兴」说出来，别让对方猜。"},
        "clear": {"feel": "他知道发生了什么，也知道自己可以做什么。",
                  "out": "本子的事有了说法，两个人都不别扭，下次他也会更注意。",
                  "tip": "还可以试试：说完以后，听一听他怎么说。"},
    },
    "s2": {
        "blame": {"feel": "他会觉得你在跟他吵，反而更相信听来的那些话。",
                  "out": "越吵越像真有事，误会不但没澄清，还变大了。",
                  "tip": "还可以试试：先稳住，把事实按顺序说清楚。"},
        "mute": {"feel": "他不确定到底是不是你，就继续照着听来的说法想。",
                 "out": "传言没人澄清，可能越传越远，你心里也一直堵着。",
                 "tip": "还可以试试：找他说一句，甚至请老师一起把事说清楚。"},
        "clear": {"feel": "他发现你愿意好好说，也愿意把话听完。",
                  "out": "事实清楚了，你也能知道他为什么这么激动。",
                  "tip": "还可以试试：把当时的经过按顺序讲一遍。"},
    },
    "s3": {
        "blame": {"feel": "大家会觉得被否定了，即使你的主意不错，也不太想听。",
                  "out": "组里的气氛变差，手抄报反而做得更慢。",
                  "tip": "还可以试试：先听听他们的想法，再说你的。"},
        "mute": {"feel": "大家不知道你有意见，就按原来的做法继续。",
                 "out": "手抄报最后是做完了，可你一直觉得「我说了也没用」。",
                 "tip": "还可以试试：把想法说一次，至少让大家听见。"},
        "clear": {"feel": "大家会觉得你的主意是来帮忙的，不是来抢的。",
                  "out": "两样合起来，手抄报反而比原来更好看。",
                  "tip": "还可以试试：定一个「先试一次，不行再改」的办法。"},
    },
}

# ── 综合任务：成长新问题三步决策台 ──
DECISION = {
    "scene": "星期五放学，同学拉着你去打球，可你已经答应妈妈回家先把作业写完。"
             "这时一个高年级的同学递过来一支烟，说：就抽一口，没事的。",
    "steps": [
        {"k": "s1", "n": "第一步 · 先想清楚自己的处境",
         "opts": [
             {"t": "大家都去了，我不去不好意思，先跟着去再说。", "ok": False,
              "out": "不好意思的代价是把自己的安排放到了最后，后面容易越拖越乱。",
              "tip": "还可以试试：先分清哪些是「不好意思」，哪些是「我已经答应过的事」。"},
             {"t": "我今天有答应在先；而且递烟这件事，不管谁说，我都不能答应。", "ok": True,
              "out": "你把两件事分开了：打球可以商量，烟的事没有商量的余地。",
              "tip": "还可以试试：把这句话在心里先说一遍，开口的时候就不慌了。"},
             {"t": "先去打球，作业和烟的事都等一下再说。", "ok": False,
              "out": "「等一下再说」常常就变成了「来不及再说」，事情会堆在一起。",
              "tip": "还可以试试：先把最不能拖的那一件想出来。"},
         ]},
        {"k": "s2", "n": "第二步 · 怎么把话说清楚",
         "opts": [
             {"t": "什么都不说，转身就走。", "ok": False,
              "out": "同学不知道你为什么走，可能觉得你不合群，下次还会来拉你。",
              "tip": "还可以试试：只说一句也行——把原因讲出来再走。"},
             {"t": "今天我有答应在先，得先回家；明天放学我们一起去打球，行吗？", "ok": True,
              "out": "你把原因说清楚了，还给了对方一个具体的时间，谁都不用不高兴。",
              "tip": "还可以试试：说到就做到，下一次拒绝才更有分量。"},
             {"t": "你们真无聊，就知道玩。", "ok": False,
              "out": "本来是拒绝这一次，说成这样就成了否定别人，容易吵起来。",
              "tip": "还可以试试：把「这件事我不去」和「你们不好」分开说。"},
         ]},
        {"k": "s3", "n": "第三步 · 怎么拒绝那支烟",
         "opts": [
             {"t": "接过来抽一口，免得被人说胆小。", "ok": False,
              "out": "这一步一旦做了，后面就很难再往回退；身体受的伤害也是真的。",
              "tip": "还可以试试：先在心里定好一句固定的话，比如「我不抽，谢谢」。"},
             {"t": "我不抽烟。谢谢。我先走了。说完就走开，回家把这件事告诉家里人。", "ok": True,
              "out": "说清楚、走开、告诉可信任的大人，这三步做到了，你就把自己保护好了。",
              "tip": "还可以试试：把这件事告诉老师或者家里人，让他们也知道。"},
             {"t": "大声骂他一顿，然后站在那儿看着他们。", "ok": False,
              "out": "骂完还站在原地，等于把自己留在了那个场合里，并不更安全。",
              "tip": "还可以试试：说一句就走开，先离开那个地方，再说别的。"},
         ]},
    ],
}

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g5-u1 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 课余生活选择台：4 张情境卡 × 每卡 3 个做法 → 对方感受 + 后果 + 还可以试试
   3) 好好说话台：3 个情境 × 3 种说话方式 = 9 组后果
   4) 成长新问题三步决策台：三步各选一个 → 合成一条完整应对
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

  /* ---------- 2. 课余生活选择台 ---------- */
  var CARDS = __CARDS_JSON__;
  var stage1 = document.getElementById('pick-stage');
  if (stage1) {
    var curCard = null, picked = {};
    var out1 = document.getElementById('pick-out');
    var panel = document.getElementById('pick-panel');
    function cardById(id) {
      for (var i = 0; i < CARDS.length; i++) { if (CARDS[i].id === id) return CARDS[i]; }
      return null;
    }
    function render1() {
      document.querySelectorAll('[data-pick-card]').forEach(function (b) {
        var k = b.dataset.pickCard;
        b.classList.toggle('selected', k === curCard);
        b.classList.toggle('done', !!picked[k]);
      });
      var doneN = Object.keys(picked).length;
      document.getElementById('pick-score').textContent = '已经选过 ' + doneN + ' / ' + CARDS.length + ' 张卡';
      if (!curCard) { panel.innerHTML = ''; return; }
      var C = cardById(curCard);
      var html = '<div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">' +
        '<p style="margin:0"><strong>情境卡：</strong>' + C.scene + '</p>' +
        '<p style="margin:6px 0 0;color:var(--muted)">' + C.extra + '</p></div>';
      html += '<div style="font-weight:700;font-size:14px;margin:14px 0 0">你会怎么做？选一个试试</div>';
      html += '<div class="grid" style="margin-top:10px">';
      C.opts.forEach(function (o, i) {
        var cls = 'choice';
        if (picked[C.id] === i) cls += o.ok ? ' correct' : ' wrong';
        html += '<button class="' + cls + '" data-pick-opt="' + i + '" style="text-align:left">' + o.t + '</button>';
      });
      html += '</div>';
      panel.innerHTML = html;
      panel.querySelectorAll('[data-pick-opt]').forEach(function (b) {
        b.addEventListener('click', function () { chooseOpt(parseInt(b.dataset.pickOpt, 10)); });
      });
    }
    function chooseOpt(i) {
      var C = cardById(curCard);
      var o = C.opts[i];
      picked[C.id] = i;
      out1.className = 'result' + (o.ok ? '' : ' warn');
      out1.innerHTML = '<strong>你选的是：' + o.t + '</strong><br>' +
        '<strong>' + (o.ok ? '这样可能会更好：' : '这样可能会：') + '</strong>' + o.out +
        '<br><span style="color:var(--muted)"><strong>对方的感受：</strong>' + o.feel + '</span>' +
        '<br><span style="color:var(--muted)">' + o.tip + '</span>';
      render1();
      if (Object.keys(picked).length === CARDS.length) {
        out1.className = 'result';
        out1.innerHTML += '<br><br><strong>四张卡都选过了！</strong>你会发现，好的选择大多有一个共同点：' +
          '先把话说清楚，再自己拿主意。';
      }
    }
    document.querySelectorAll('[data-pick-card]').forEach(function (b) {
      b.addEventListener('click', function () {
        curCard = b.dataset.pickCard;
        out1.className = 'result warn';
        out1.innerHTML = '<strong>' + cardById(curCard).scene + '</strong><br>想一想你会怎么做，再点下面三个做法里的一个。';
        render1();
      });
    });
    render1();
  }

  /* ---------- 3. 好好说话台（3 情境 × 3 说法） ---------- */
  var TALK_SCENES = __TALK_SCENES_JSON__;
  var TALK_WAYS = __TALK_WAYS_JSON__;
  var TALK_FB = __TALK_FB_JSON__;
  var stage2 = document.getElementById('talk-stage');
  if (stage2) {
    var curScene = 's1';
    var out2 = document.getElementById('talk-out');
    var sayBox = document.getElementById('talk-say');
    function sceneById(id) {
      for (var i = 0; i < TALK_SCENES.length; i++) { if (TALK_SCENES[i].id === id) return TALK_SCENES[i]; }
      return null;
    }
    function render2() {
      document.querySelectorAll('[data-talk-scene]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.talkScene === curScene);
      });
      var S = sceneById(curScene);
      document.getElementById('talk-scene-text').innerHTML =
        '<strong>' + S.n + '</strong>：' + S.d;
      sayBox.innerHTML = '';
      TALK_WAYS.forEach(function (W) {
        var b = document.createElement('button');
        b.className = 'choice';
        b.style.textAlign = 'left';
        b.textContent = W.n + '：' + W.say[curScene];
        b.addEventListener('click', function () { say(W.k); });
        sayBox.appendChild(b);
      });
    }
    function say(k) {
      var F = TALK_FB[curScene][k];
      var S = sceneById(curScene);
      var W = null;
      TALK_WAYS.forEach(function (x) { if (x.k === k) W = x; });
      var head = k === 'clear' ? '这样可能会更好：' : '这样可能会：';
      out2.className = 'result' + (k === 'clear' ? '' : ' warn');
      out2.innerHTML = '<strong>' + S.n + ' × ' + W.n + '</strong><br>' +
        '<strong>' + head + '</strong>' + F.out +
        '<br><span style="color:var(--muted)"><strong>对方的感受：</strong>' + F.feel + '</span>' +
        '<br><span style="color:var(--muted)">' + F.tip + '</span>';
    }
    document.querySelectorAll('[data-talk-scene]').forEach(function (b) {
      b.addEventListener('click', function () {
        curScene = b.dataset.talkScene;
        out2.className = 'result warn';
        out2.textContent = '先读一读上面的情境，再点一种说法，看看会怎么样。';
        render2();
      });
    });
    render2();
  }

  /* ---------- 4. 成长新问题三步决策台 ---------- */
  var DECISION = __DECISION_JSON__;
  var stage3 = document.getElementById('dec-stage');
  if (stage3) {
    var chosen = {};
    var out3 = document.getElementById('dec-out');
    var panel3 = document.getElementById('dec-panel');
    function render3() {
      var html = '';
      DECISION.steps.forEach(function (S, si) {
        html += '<div class="inner-card" style="margin-top:' + (si ? '10px' : '0') + '">';
        html += '<p><strong>' + S.n + '</strong></p>';
        html += '<div class="grid" style="margin-top:8px">';
        S.opts.forEach(function (o, oi) {
          var cls = 'choice';
          if (chosen[S.k] === oi) cls += o.ok ? ' correct' : ' wrong';
          html += '<button class="' + cls + '" data-dec-step="' + S.k + '" data-dec-opt="' + oi +
            '" style="text-align:left">' + o.t + '</button>';
        });
        html += '</div></div>';
      });
      panel3.innerHTML = html;
      panel3.querySelectorAll('[data-dec-opt]').forEach(function (b) {
        b.addEventListener('click', function () {
          var sk = b.dataset.decStep;
          var oi = parseInt(b.dataset.decOpt, 10);
          var S = null;
          DECISION.steps.forEach(function (x) { if (x.k === sk) S = x; });
          var o = S.opts[oi];
          chosen[sk] = oi;
          var n = Object.keys(chosen).length;
          if (n < DECISION.steps.length) {
            out3.className = 'result' + (o.ok ? '' : ' warn');
            out3.innerHTML = '<strong>' + S.n + '：</strong>' + o.out +
              '<br><span style="color:var(--muted)">' + o.tip + '</span>' +
              '<br><span style="color:var(--muted)">还有 ' + (DECISION.steps.length - n) + ' 步没选。</span>';
          } else {
            var okN = 0, badStep = '';
            DECISION.steps.forEach(function (x) {
              var idx = chosen[x.k];
              if (x.opts[idx].ok) { okN++; } else if (!badStep) { badStep = x.n; }
            });
            if (okN === DECISION.steps.length) {
              out3.className = 'result';
              out3.innerHTML = '<strong>三步都选好了：这是一条完整又稳妥的应对。</strong>' +
                '先想清楚自己的处境，再把原因说清楚，最后说一句「我不抽，谢谢」，说完就走开，' +
                '回家把这件事告诉可信任的大人。三句话就是：自己选、好好说、敢说不。';
            } else {
              out3.className = 'result warn';
              out3.innerHTML = '<strong>三步都选好了，其中 ' + okN + ' 步选得稳，还有一步可以再想想。</strong>' +
                '可以回头看看「' + badStep + '」，再看一遍它的后果，然后换一个做法试试。';
            }
          }
          render3();
        });
      });
    }
    render3();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__CARDS_JSON__', json.dumps(CARDS, ensure_ascii=False))
             .replace('__TALK_SCENES_JSON__', json.dumps(TALK_SCENES, ensure_ascii=False))
             .replace('__TALK_WAYS_JSON__', json.dumps(TALK_WAYS, ensure_ascii=False))
             .replace('__TALK_FB_JSON__', json.dumps(TALK_FB, ensure_ascii=False))
             .replace('__DECISION_JSON__', json.dumps(DECISION, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：这三件事你会怎么处理？", TTS["pretest"], [
        {"q": "同学约你放学后去玩，可你答应过妈妈今天先把作业写完。下面哪种做法更合适？",
         "options": [("说清楚原因，再跟他约一个具体的时间", True),
                     ("怕他不高兴，直接答应去玩", False),
                     ("很不耐烦地回一句「别烦我」", False)],
         "explain": "拒绝这一件事，不等于拒绝这个人；把原因说清楚、给一个具体时间，"
                    "既把自己答应的事做到，也不让对方难受。"
                    "<strong>错因提醒：</strong>常见错误是误认为「不去就是不合群」——"
                    "合不合群，不取决于这一件事跟不跟。"},
        {"q": "同桌碰掉了你的本子，还踩脏了。下面哪种说法最能让事情往前走？",
         "options": [("我的本子被碰掉还踩脏了，我有点难过，能不能帮我看看还能不能用", True),
                     ("你就是故意的", False),
                     ("什么都不说，自己捡起来生闷气", False)],
         "explain": "先说看到的事实，再说自己的感受，最后说希望怎么办，对方才知道发生了什么、"
                    "可以做什么。<strong>错因提醒：</strong>容易把「说事实」搞混成「下判断」——"
                    "一句「你就是故意的」，对方第一反应是辩解，而不是帮你。"},
        {"q": "有人递给你一支烟，说就抽一口没事。下面哪种做法最稳妥？",
         "options": [("说一句「我不抽，谢谢」，走开，再把这件事告诉可信任的大人", True),
                     ("接过来抽一口，免得被人说胆小", False),
                     ("大声骂他一顿，然后站在原地跟他理论", False)],
         "explain": "说清楚、走开、告诉大人，这三步能让你先离开那个场合，把自己保护好。"
                    "<strong>错因提醒：</strong>有的同学误认为「拒绝就是跟他吵一架」——"
                    "可拒绝的目的是保护好自己，不是赢一场架。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "自主选择课余生活：先看清三件事，再自己拿主意", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们已经知道，自己喜欢什么、不喜欢什么（And）；可到了五年级，选择变多了，同学约你、家里有安排、时间又只有那么多，常常拿不准该听谁的（But）；所以这节课先学会把三件事看清楚，再自己做选择，并且说得出理由（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px"><strong>课余生活</strong>是指上课以外可以自己安排的时间。「自己安排」不是想干什么就干什么，而是先看清三件事，再下决定。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>我自己想不想做，为什么想。</strong>先把「喜欢」和「别人都在做」分开。</div></div>
          <div class="step"><span class="n">2</span><div><strong>今天有没有必须先做完的事。</strong>比如答应过别人的作业、值日、和家里说好的安排。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>家里人和同伴怎么看。</strong>他们的话可以参考，但不能代替你做决定。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="自主选择课余生活示意图：同学邀约、社团活动、家里安排三种声音，学生按「想不想、有没有必须先做的事、别人怎么看」三件事做选择，附中文标注">
          <figcaption>概念图：选择课余生活时先看清的三件事 · 别人的选择可以参考，但决定要自己做</figcaption>
        </figure>
        <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(78,205,196,.45)">
          <p><strong>一句可以随身带的话</strong></p>
          <p style="color:var(--muted)">先看清三件事，再自己做选择；<strong>能说出理由的选择，才算真的自己选的。</strong></p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「我自己决定，就不用跟家里说」。可你事先说一声，家里人不但不会拦你，还会帮你把时间安排好——自己决定和让家里人知道，从来不冲突。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "同样是「不去」，一句「别烦我」和一句「明天我们一起去」，结果完全不一样。差别不在去不去，在有没有把话说清楚。"},
    {"lens": "比较它", "text": "「跟着大家做」很省事，「想清楚再做」要多花一点力气，可后面要承担结果的是你自己。"},
    {"lens": "迁移它", "text": "这套方法在哪里都用得上：选社团、安排周末、决定要不要买一样东西——先看清三件事，再说出自己的理由。"},
])}
    ''', tag="概念一"))

    card_btns = "\n".join(
        f'            <button class="choice" data-pick-card="{c["id"]}" style="text-align:left">'
        f'<strong>情境卡 {i}</strong><br><span style="color:var(--muted);font-size:14px">{c["scene"]}</span></button>'
        for i, c in enumerate(CARDS, 1)
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：课余生活选择台，你会怎么做？", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">点开一张情境卡，从三个做法里选一个。选完会告诉你<strong>这样可能会发生什么、对方心里会怎么想</strong>，还有一个别的办法。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 挑一张情境卡</div>
          <div id="pick-stage">
            <div class="grid">
{card_btns}
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">选择进度</span><span class="v" id="pick-score">已经选过 0 / 4 张卡</span></div>
          </div>
          <p class="result warn" id="pick-out" style="margin-top:12px">先点一张情境卡。</p>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 这张卡上，你会怎么做</div>
          <div id="pick-panel"></div>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧭</span><div><strong>选完回头看：</strong>四张卡里，哪个做法让你觉得最难说出口？那多半就是你需要练的那一步。可以先在心里把台词说一遍，再试第二次。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "学会沟通交流：先说事实，再说感受，最后说希望", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px"><strong>沟通交流</strong>是指把自己的想法和感受清楚地告诉对方，同时也听一听对方的想法。很多同学以为沟通就是把想说的说完，其实<strong>顺序</strong>很重要。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先说看到的事实：</strong>「我的本子被碰到了地上，还被踩了一下。」不加评价，对方才听得进去。</div></div>
          <div class="step"><span class="n">2</span><div><strong>再说自己的感受：</strong>「我有点难过。」把自己的心情讲出来，对方才知道这件事对你有影响。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>最后说希望怎么办：</strong>「能不能帮我看看还能不能用，下次注意一下好吗？」</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="好好说话三步示意图：指责的说法与说清楚的说法对比，旁边标注对方的感受，附中文标注">
          <figcaption>概念图：同样一件事，三种说法的不同结果 · 先说事实、再说感受、最后说希望</figcaption>
        </figure>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>口诀：说事实、说感受、说希望</strong></p>
          <p style="color:var(--muted)">三步连起来，对方就知道三件事：发生了什么、你是什么心情、他可以做什么。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学把「不吵架」当成「什么都不说」。可你不说，对方根本不知道你生气了，事情只会一直搁着；<strong>憋着不说，和自己生闷气没有区别</strong>。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "「你就是故意的」和「本子被踩脏了」，说的是同一件事，可一句是在猜对方的心思，一句只是在讲发生了什么。"},
    {"lens": "解释它", "text": "为什么先说事实最管用？因为事实是两个人能一起看见的东西，判断却只属于你一个人；从共同的地方说起，事情才谈得下去。"},
    {"lens": "迁移它", "text": "和同学、和家里人、和老师，这套说法都一样：被误会的时候先讲经过，有分歧的时候先讲自己的希望。"},
])}
    ''', tag="概念二"))

    scene_btns = "\n".join(
        f'            <button class="choice" data-talk-scene="{s["id"]}" style="text-align:left">{s["n"]}</button>'
        for s in TALK_SCENES
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：好好说话台，同一件事的三种说法", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先选一个情境，再点一种说法，看看<strong>对方心里会怎么想、事情会往哪儿走</strong>。三个情境、三种说法，一共九种结果，都可以试。</p>
        <div class="lab-panel">
          <div id="talk-stage">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 选一个情境</div>
            <div class="grid grid-3">
{scene_btns}
            </div>
            <p class="result warn" id="talk-scene-text" style="margin-top:12px">点一个情境，看看这里发生了什么。</p>
            <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 选一种说法</div>
            <div class="grid" id="talk-say"></div>
          </div>
          <p class="result warn" id="talk-out" style="margin-top:12px">先点一种说法。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💬</span><div><strong>九种都试过之后，想一想：</strong>为什么「说清楚」这一种，在三个情境里都好用？因为它把「发生了什么」和「希望怎么办」都交给了对方，而不是替对方下结论。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小北的一次拒绝", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>星期五放学，同学拉小北去打球，还递过来一支烟，说就抽一口没事。小北答应过妈妈，今天回家先写作业。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先想清楚自己的处境：</strong>今天已经答应妈妈先写作业；而且不管谁给的烟，我都不能抽。打球可以商量，烟的事没有商量的余地。</div></div>
          <div class="step"><span class="n">2</span><div><strong>把话说清楚：</strong>对约他打球的同学说——今天我答应在先，得先回家；明天放学我们一起去，行吗？同学听了，就没再拉他。</div></div>
          <div class="step"><span class="n">3</span><div><strong>拒绝那支烟：</strong>他没有接，也没有解释很多，只说了一句——我不抽烟，谢谢，我先走了，说完就走开。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>告诉可信任的大人：</strong>回到家，他把有人递烟的事告诉了妈妈。有人管这件事，他就不用一个人扛。</div></div>
        </div>
        <div class="inner-card">
          <p><strong>为什么这三步要按这个顺序</strong></p>
          <p style="color:var(--muted)">先想清楚，才知道自己要守住什么；先把原因说清楚，才不会被人当成不合群；说一句就走开，才能先离开那个地方。三步都做完，你既保护了自己，也没有把关系弄僵。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「拒绝就是跟对方吵一架」，觉得当场翻脸才算出气。可拒绝的目的是保护好自己，不是赢一场架；说清楚、走开、告诉大人，比自己站在那儿硬扛更管用。<strong>还有一个误认为：怕被说胆小，就把烟接过来——真正需要勇气的其实是说「不」。</strong></p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "关于课余生活的安排，下面哪句话说得对？",
         "options": [("先看清自己想不想、有没有必须先做完的事、别人怎么看，再自己定，并且说得出理由", True),
                     ("别人都去我就去，不然就不合群", False),
                     ("既然是自己决定，就不用跟家里人说", False)],
         "explain": "自己选择不等于随便选，也不等于瞒着家里；能把理由说出来，才算真的自己选。"
                    "<strong>错因提醒：</strong>常见错误是误认为「不去就不合群」——"
                    "合不合群看的是有没有把话说清楚、答应的事有没有做到。"},
        {"q": "被同学误会了，下面哪种说法最能让事情往前走？",
         "options": [("这件事不是我说的，你这么生气是不是还有别的事，要不我们一起去问清楚", True),
                     ("我根本没告状，你凭什么说我", False),
                     ("不解释了，随他们怎么说", False)],
         "explain": "先把事实说清楚，再问一问对方的想法，误会才有机会澄清。"
                    "<strong>错因提醒：</strong>有的同学把「不吵架」搞混成「什么都不说」——"
                    "可传言没人澄清，只会越传越远，你心里也一直堵着。"},
        {"q": "有人递烟给你，下面哪句话说得对？",
         "options": [("说清楚我不抽，走开，再把这件事告诉可信任的大人", True),
                     ("抽一口试试，反正就一次", False),
                     ("真正的朋友不会递烟，所以只要骂他一顿就行", False)],
         "explain": "拒绝的落点在「保护自己」：说清楚、走开、告诉大人，这三步都能做到。"
                    "<strong>错因提醒：</strong>容易把「出一口气」误认为「解决了事情」——"
                    "骂完还站在原地，等于把自己留在了那个场合里。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：成长新问题三步决策台", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">下面这件事连着发生，分三步。每一步选一个做法，我会把你的选择拼成一条完整的应对。</p>
        <div class="lab-panel">
          <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
            <p style="margin:0"><strong>情境：</strong>星期五放学，同学拉着你去打球，可你已经答应妈妈回家先把作业写完。这时一个高年级的同学递过来一支烟，说：就抽一口，没事的。</p>
          </div>
          <div id="dec-stage" style="margin-top:12px"></div>
          <div id="dec-panel"></div>
          <p class="result warn" id="dec-out" style="margin-top:12px">从第一步开始选。</p>
        </div>
        <div class="inner-card" style="margin-top:14px">
          <p><strong>把它写下来，说给同桌听：</strong></p>
          <p style="color:var(--muted)">今天这节课里，哪一句话是你最想记住、也最想说出口的？写下来，再对着同桌说一遍。</p>
          <textarea id="syn-answer" rows="3" placeholder="我最想记住的一句话是……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，办法还在不在", TTS["posttest"], [
        {"q": "有同学给你起了个外号，你很不喜欢。下面哪种做法更好？",
         "options": [("找个机会跟他说：你叫我这个我心里不舒服，能不能别再叫了", True),
                     ("当场给他也起一个更难听的", False),
                     ("忍着不说，以后也不理他了", False)],
         "explain": "先说自己的感受，再说希望对方怎么办——这一步说清楚了，他才有机会改。"
                    "<strong>错因提醒：</strong>常见错误是误认为「回敬一句才不算吃亏」——"
                    "互相起外号只会越闹越大，你想要的是他别再叫，不是比谁更伤人。"},
        {"q": "你想跟家里人商量，周末留半天自己安排。下面哪种说法更好？",
         "options": [("我想留半天做点自己喜欢的事，我打算这样安排，可以吗", True),
                     ("你们根本不管我想干什么", False),
                     ("什么都不说，到时候自己溜出去", False)],
         "explain": "先说自己的希望，再说自己打算怎么做，家里人更容易同意，也更放心。"
                    "<strong>错因提醒：</strong>有的同学把「说出来」搞混成「吵出来」——"
                    "一开口就指责，本来能商量的事也容易变成互相生气。"},
        {"q": "同学说楼梯间有人递烟，还叫你一起去看看。下面哪种做法更好？",
         "options": [("不去那个地方，并且把这件事告诉老师或者家里人", True),
                     ("跟着去，只看不抽就没事", False),
                     ("自己一个人去劝他们别抽", False)],
         "explain": "先离开那个场合、再把这件事交给大人，比自己冲上去更安全，也更管用。"
                    "<strong>错因提醒：</strong>容易把「有勇气」误认为「一个人去挡」——"
                    "保护好自己、把事告诉大人，同样需要勇气。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：自己选、好好说、敢说不", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>自己选：</strong>看三件事——我自己想不想、今天有没有必须先做完的事、家里人和同伴怎么看，再自己定，并说得出理由。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>好好说：</strong>先说看到的事实，再说自己的感受，最后说希望怎么办；不指责，也不憋着。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>敢说不：</strong>说清楚「我不」，走开，把这件事告诉可信任的大人。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>一句口诀：</strong>自己选、好好说、敢说不。拒绝是为了保护好自己，不是为了赢一场架。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请从这节课的三件事里挑一件，讲给家里人听，并说清楚你打算从哪一次开始试一试。</p>
          <p style="color:var(--muted)">再动一动手：<strong>写一写</strong>你最近遇到的一件拿不准的事，把「我先想清楚了什么、我打算怎么说」写下来。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写出选择课余生活时要看清的三件事。",
            "写出一句完整的「先说事实、再说感受、再说希望」的说法，用在最近发生的一件事上。",
            "写出拒绝烟酒等不良诱惑的三个办法。",
        ],
        [
            "这一周记录一次你和同学或家里人意见不一样的事：你当时是怎么说的、对方的反应是什么，再写一句下次可以怎么说得更好。",
            "和家里人一起商量一次你的课余时间安排，把你的想法和打算写下来，一周以后看看做到了几件。",
        ],
        [
            "给自己做一张「拒绝三步卡」，写上说清楚、走开、告诉大人三步，先和同桌练两遍，再说说练的时候最难的是哪一步、你是怎么过的。",
            "把今天课上的三个情境换一个说法，自己设计一张情境卡，写清楚三个做法和各自的后果，带到班会上和同学一起用。",
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
    "title": "面对成长中的新问题",
    "name_en": "Facing New Problems as We Grow Up",
    "grade": 5,
    "grade_cn": "五年级",
    "domain": "moral-cultivation",
    "domain_cn": "道德修养",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学五年级的道德与法治课，正对统编五上第 1 单元「面对成长中的新问题」，落在三件学生每天都在碰的事上。一是「自主选择课余生活」：课余生活是指上课以外可以自己安排的时间，自己安排不是想干什么就干什么，而是先看清三件事——我自己想不想做、今天有没有必须先做完的事、家里人和同伴怎么看，再自己下决定，并且说得出理由；同时澄清两个常见误解：不去不等于不合群，自己决定也不等于瞒着家里。二是「学会沟通交流」：给出一个可以随身带的三步说法——先说看到的事实、再说自己的感受、最后说出希望怎么办，并点明两个最容易搞混的地方：把「说事实」说成了「下判断」，以及把「不吵架」当成了「什么都不说」。三是「主动拒绝烟酒与毒品」：不背法条，只练能做的三步——说清楚「我不」、走开、把这件事告诉可信任的大人，并纠正「拒绝就是吵一架」「怕被说胆小就接过来」两种误认为。三个互动台子都能真操作，反馈一律写成「这样可能会……，还可以试试……」：动手一是课余生活选择台（四张真实情境卡，每卡三个做法，选完展开对方的感受与后果）、动手二是好好说话台（三个真实分歧情境 × 三种说话方式，九组后果与对方感受）、综合任务是成长新问题三步决策台（先想清楚处境、怎么把话说清楚、怎么拒绝那支烟，三步选定后合成一条完整应对）。插图一律为中性简洁扁平插画，不使用真人照片风格。",
    "tags": ["面对成长中的新问题", "自主选择课余生活", "学会沟通交流", "主动拒绝烟酒与毒品", "沟通三步", "拒绝三步", "五年级", "道德修养"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学「道德修养」——自律自强，孝敬长辈，友善待人，有正确的价值取向；对应统编《道德与法治》五年级上册 第1单元「面对成长中的新问题」：自主选择课余生活、学会沟通交流、主动拒绝烟酒与毒品。",
    "hero_question": "长大的路上遇到拿不准的事，我该怎么选、怎么说、怎么说不？",
    "hero_alt": "面对成长中的新问题知识结构图：自主选择课余生活、学会沟通交流、主动拒绝不良诱惑 三栏，附中文标注",
    "hero_caption": "面对成长中的新问题：自己选 · 好好说 · 敢说不（先看清三件事，再说事实、说感受、说希望）",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的练习都会围着它转。",
    "anchor_choices": [
        {"t": "课余时间怎么安排，我该听谁的？", "d": "想自己决定，又怕家里人和同学不高兴", "v": "课余时间怎么安排我该听谁的"},
        {"t": "想参加的活动和作业撞在一起，怎么办？", "d": "喜欢的事放不下，该做的事也不能拖", "v": "想参加的活动和作业撞在一起怎么办"},
        {"t": "被误会、和同学闹别扭了，话该怎么说？", "d": "一开口就容易吵起来，不说又憋得难受", "v": "被误会和同学闹别扭了话该怎么说"},
        {"t": "有人递来烟或者酒，怎么拒绝才不别扭？", "d": "想拒绝，又怕被说不合群、胆小", "v": "有人递来烟或者酒怎么拒绝才不别扭"},
    ],
    "objectives": [
        "能说出课余生活要自己选择，也知道选择时要看清三件事：我自己想不想、今天有没有必须先做完的事、家里人和同伴怎么看，并能说清自己选的理由",
        "遇到分歧或被误解时，能先说看到的事实、再说自己的感受、最后说出希望怎么办，而不是指责别人或者憋着不说",
        "能说出拒绝烟酒等不良诱惑的三个办法：说清楚「我不」、走开、把这件事告诉可信任的大人",
        "遇到拿不准的事，能先把处境想清楚再决定怎么做，并说出自己这样选的理由",
    ],
    "objectives_plain": [
        "能说出选择课余生活时要看清的三件事，并说清自己选的理由",
        "能在有分歧或被误解时，说事实、说感受、说希望",
        "能说出拒绝烟酒等不良诱惑的三个办法",
        "遇到拿不准的事，能先把处境想清楚，再说出这样选的理由",
    ],
    "standards": [
        {"content": "自律自强，孝敬长辈，友善待人，有正确的价值取向。",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学 道德修养"},
        {"content": "自主选择课余生活；学会沟通交流；主动拒绝烟酒与毒品",
         "source": "统编《道德与法治》五年级上册 第1单元「面对成长中的新问题」"},
    ],
    "prereqs": ["pol-e-g4-u4"],
    "prereqs_name": "让生活多一些绿色",
    "prereqs_meta": "pol-e-g4-u4",
    "leads_to": ["pol-e-g5-u2"],
    "next_meta": "pol-e-g5-u2",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "升上五年级，拿不准的事变多了：选不选、去不去、说不说。这节课练三件事：自己选、好好说、敢说不。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能把最难说出口的那一句话说出来。",
        "objectives": "看清四件事：选择要看哪三样、话怎么说、烟酒怎么拒绝、拿不准时先做什么。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "先看清三件事——我自己想不想、今天有没有必须先做完的事、别人怎么看，再自己定。",
        "lab-1": "四张情境卡，每张三个做法。选一个，看对方的感受和接下来会发生什么。",
        "module-2": "说事实、说感受、说希望——三步连起来，对方才知道发生了什么、可以做什么。",
        "lab-2": "三个情境 × 三种说法 = 九种结果。都试一遍，你就知道为什么说清楚最管用。",
        "worked-example": "小北的四步：先想清楚、把话说清楚、说一句就走开、告诉可信任的大人。",
        "conceptest-1": "三个说法里各藏着一个容易想歪的地方，选完把解释读一遍。",
        "synthesis": "三步选定，合成一条完整的应对：先想清楚 → 怎么说话 → 怎么拒绝。",
        "posttest": "出现了起外号、商量周末安排、楼梯间递烟，看看今天的办法还用不用得上。",
        "summary": "三句话：自己选、好好说、敢说不。拒绝是为了保护好自己，不是为了赢一场架。",
        "homework": "三层小任务，先做前两层；第二层要请家里人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学道德与法治「道德修养」板块在五年级的空缺，正对统编五上第 1 单元「面对成长中的新问题」（自主选择课余生活、学会沟通交流、主动拒绝烟酒与毒品）。五年级学生正处在「选择变多、主意也变多」的阶段：同学约你、家里有安排、时间只有那么多，很多事第一次要自己拿主意；同时被误会、闹别扭、被人递烟这些真实困扰也开始出现，可他们往往要么一开口就吵起来，要么憋着不说，碰到烟酒更不知道该怎么拒绝才不别扭。所以全课不做道德说教，也不背法条，把每一件都换成能练出来的动作。第一层是「自主选择课余生活」：把「自己安排」落成先看清三件事——我自己想不想做、今天有没有必须先做完的事、家里人和同伴怎么看，再自己下决定并说得出理由；同时澄清两个常见误解：不去不等于不合群，自己决定也不等于瞒着家里。第二层是「学会沟通交流」：给出一个可随身带的三步说法——先说看到的事实、再说自己的感受、最后说出希望怎么办，并点明两个最容易搞混的地方，把「说事实」说成了「下判断」，以及把「不吵架」当成了「什么都不说」。第三层是「主动拒绝烟酒与毒品」：不背条文，只练三步——说清楚「我不」、走开、把这件事告诉可信任的大人，并纠正「拒绝就是吵一架」「怕被说胆小就接过来」两种误认为。三个互动台子都能真操作，反馈一律写成「这样可能会……，还可以试试……」：动手一是课余生活选择台，四张真实情境卡各配三个做法，选完展开对方的感受与后果；动手二是好好说话台，三个真实分歧情境 × 三种说话方式，形成九组后果对照；综合任务是成长新问题三步决策台，学生按「先想清楚处境 → 怎么把话说清楚 → 怎么拒绝那支烟」各选一步，系统合成一条完整应对。插图一律为中性简洁扁平插画，不使用真人照片风格。",
    "plan_table": """| 1 | cover | 面对成长中的新问题 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：这三件事你会怎么处理？ | 起·前测（暴露已有想法） |
| 5 | concept | 自主选择课余生活：先看清三件事，再自己拿主意 | 承·概念一（选择的依据） |
| 6 | interactive | 动手一：课余生活选择台，你会怎么做？ | 承·核心模拟（情境卡 → 对方感受与后果） |
| 7 | concept | 学会沟通交流：先说事实，再说感受，最后说希望 | 承·概念二（沟通三步） |
| 8 | interactive | 动手二：好好说话台，同一件事的三种说法 | 承·对照模拟（3 情境 × 3 说法） |
| 9 | concept | 例题示范：小北的一次拒绝 | 转·重难点突破（四步示范 + 易错点） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：成长新问题三步决策台 | 合·迁移应用（三步合成应对） |
| 12 | quiz | 后测：换几个新情境，办法还在不在 | 合·后测 |
| 13 | summary | 小结：自己选、好好说、敢说不 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：自主选择课余生活 / 学会沟通交流 / 主动拒绝不良诱惑 三栏\n- P5 自主选择课余生活示意图（已生成）：三种声音与三件事的判断依据，附中文标注\n- P7 好好说话三步示意图（已生成）：指责的说法与说清楚的说法对比，附中文标注\n- 三张图均为中性简洁扁平教学插画，不使用真人照片风格，不含可识别的真实人物\n- 课件不出现真实烟酒商品包装与品牌，不呈现任何吸烟或饮酒的示范画面\n- 若需补充：本班学生自己写的情境卡（由学生匿名提供），不在课件中呈现任何个人真实信息",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
