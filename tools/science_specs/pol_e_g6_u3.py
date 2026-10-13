# -*- coding: utf-8 -*-
"""小学道德与法治 · 我们的国家机构（六年级上 · 第3单元）—— 补齐知识树「国情与公民意识」空缺

学科语气（道德与法治）：从学生每天看得到的政府办事大厅、法院门口的牌子、社区里的公告栏讲起，
情境驱动 + 价值判断；结论落在「这件事该找谁、为什么找他」，不做机构名称的机械背诵。

★ 表述红线（最高优先级，全课统一口径，任何地方不得含糊）：
  · 机构名称一律用规范全称：全国人民代表大会、全国人民代表大会常务委员会、国务院（中央人民政府）、
    地方各级人民代表大会、地方各级人民政府、人民法院、人民检察院、监察委员会、人民代表大会代表。
    绝不使用「人大」「政府」「法院」「检察院」这类简称当作正式名称出现在结论句里。
  · 一律不出现任何法律条文编号（不写「第几条」，只说「宪法规定」「法律规定」）。
  · 职权表述只写得起检验的常识性表述：全国人民代表大会是最高国家权力机关；全国人民代表大会和
    全国人民代表大会常务委员会行使国家立法权；国务院即中央人民政府，是最高国家权力机关的执行机关、
    是最高国家行政机关；地方各级人民政府是地方各级国家行政机关；人民法院是国家的审判机关；
    人民检察院是国家的法律监督机关；监察委员会是行使国家监察职能的专责机关。
  · 不臆造案例细节、不编造具体案件与办理流程；情境一律写成校园、家庭、社区的公共事务层面，
    只到「该找哪一类机构」为止，不写结果、不写人名地名。
  · 不绘制国徽、法院徽章、国旗等图形；机构一律用抽象剪影（柱廊建筑、圆环、天平、齿轮、卷宗等）
    与地标性建筑的抽象轮廓表示，不使用真人照片风格。

内容落点（对应统编六上第 3 单元「我们的国家机构」）：
  ① 国家机构有哪些：国家机构是国家机关的统称；人民代表大会制度是我国的根本政治制度；
     全国人民代表大会是最高国家权力机关，全国人民代表大会和地方各级人民代表大会都由民主选举产生，
     对人民负责，受人民监督；国家行政机关、监察机关、审判机关、检察机关都由人民代表大会产生，
     对它负责，受它监督——这就是常说的「一府一委两院」与人民代表大会的关系。
  ② 职权分工：立法（全国人民代表大会和全国人民代表大会常务委员会行使国家立法权）、
     行政（国务院即中央人民政府是最高国家行政机关，地方各级人民政府是地方各级国家行政机关）、
     审判（人民法院是国家的审判机关）、检察（人民检察院是国家的法律监督机关）、
     监察（监察委员会是行使国家监察职能的专责机关）。
  ③ 人大代表为人民：人民代表大会代表代表人民的利益和意志，依法参加行使国家权力，
     密切联系群众，听取和反映群众的意见和要求。
  ④ 权力受到制约和监督：一切国家机关和国家工作人员必须依靠人民的支持，经常保持同人民的密切联系，
     倾听人民的意见和建议，接受人民的监督，努力为人民服务。

三个互动台子都能真操作（反馈一律写成「这样可能会……，还可以试试……」）：
  动手一 = ★核心模拟「事情该找哪个机构」对照台（6 个情境 × 选对应机构 + 说理由）；
  动手二 = 「机构名片与职权配对台」（5 张机构名片 × 5 张职权卡配对）；
  综合任务 = 「我的建议送出去」行动台（问题 → 主管机构 → 表达方式 → 合成办事路线卡）。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g6-u3"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "上一节课我们弄清楚了自己的公民身份。这节课把目光从「我」转到「国家」：我们每天都能见到一些挂着国徽的机关大门，社区里的公告栏、马路上的路灯、新闻里说的法律，都是这些机关在做事。它们合起来有一个名字，叫国家机构。今天我们把三件事弄清楚：国家机构有哪些，不同的机构分别管什么事，还有——它们手里的权力这么大，谁来监督。学完这节课，你会有一个很实用的本领：遇到一件事，能说出它大概该找哪一类国家机构。",
    "problem-anchor": "开始之前，先选一个你真正想知道的问题：国家机构到底有哪些？人民代表是怎么产生的、他们为谁说话？不同的机构分别管什么事？还是，权力这么大，谁来监督？选好以后，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出国家机构是国家机关的统称，能说出人民代表大会制度是我国的根本政治制度，知道全国人民代表大会是最高国家权力机关。第二，能说出全国人民代表大会、国务院、地方各级人民政府、人民法院、人民检察院各自的职权，能说出立法、行政、审判、检察这几种分工。第三，能说出国家行政机关、监察机关、审判机关、检察机关都由人民代表大会产生，对它负责，受它监督，能说出人民代表大会代表代表人民的利益和意志，为人民说话。第四，能对一个身边的事情做出判断，说出它大概该找哪一类国家机构，并说出理由。",
    "pretest": "先做三道小题，用你现在的想法选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "第一件事，国家机构有哪些。先说名字：国家机构，是国家机关的统称。我国的国家机构，包括中央国家机构和地方国家机构。它们不是各管各的，而是按同一个制度组织起来的，这个制度叫人民代表大会制度，它是我国的根本政治制度。这里有三句最要紧的话。第一句：全国人民代表大会是最高国家权力机关。第二句：全国人民代表大会和地方各级人民代表大会，都由民主选举产生，对人民负责，受人民监督。第三句：国家行政机关、监察机关、审判机关、检察机关，都由人民代表大会产生，对它负责，受它监督。把第三句话换成常听到的说法，就是「一府一委两院」——一府是人民政府，一委是监察委员会，两院是人民法院和人民检察院。它们都由本级人民代表大会产生，对它负责，也受它监督。这里有两个容易想歪的地方：有的同学误认为国家机构离自己很远，其实我们每天路过的社区办事窗口、同学家附近的法庭、新闻里报道的法律，都是国家机构在工作；也有的同学误认为人民代表大会和人民政府是一回事，其实一个是权力机关，一个是行政机关，分工不一样。",
    "lab-1": "现在请你当一次办事员。这里有六个情境，每一个后面有几个机构让你选。先读情境，想一想这件事到底是「定规矩」还是「办事」、是「审」还是「诉」，再选出你认为该找的那一类机构，然后看解释。选错了也没关系，正好知道要重点想哪一步。",
    "module-2": "第二件事，不同的机构分别管什么事。先看立法：全国人民代表大会和全国人民代表大会常务委员会行使国家立法权，法律由它们审议通过；地方各级人民代表大会在本行政区域内，保证宪法、法律、行政法规的遵守和执行。再看行政：国务院，即中央人民政府，是最高国家权力机关的执行机关，是最高国家行政机关；地方各级人民政府，是地方各级国家行政机关，管的是本地区的事。再看审判：人民法院是国家的审判机关，依法行使审判权。再看检察：人民检察院是国家的法律监督机关，依法行使检察权。还有监察：监察委员会是行使国家监察职能的专责机关。把这几句连起来，你会看到一条清楚的链条：立法机关定规矩，行政机关去办事，审判机关依法审理，检察机关依法监督，监察机关对公职人员依法监督。这里有两个最容易搞混的地方：有的同学误认为人民法院和人民检察院差不多，其实一个「审」、一个「察」，分工不同；也有的同学把全国人民代表大会和国务院搞混，其实一个是最高国家权力机关，一个是最高国家行政机关。记住一句口诀：人大定、国务院办、法院审、检察院察、监委督。",
    "lab-2": "接下来请你玩一次配对。左边是五张机构名片，右边是五张职权卡，顺序被打乱了。先点一张机构名片，再点一张你认为与它相配的职权卡。配对了，两边会连起来，我会告诉你为什么这样配得起来；配错了，我会告诉你这样可能会错在哪里，还可以怎么想。",
    "worked-example": "我们一起来看一次机构名牌的校对。学校要做一面「身边的国家机构」展示墙，几位同学写了五条说明，请你当一次校对员，判断哪一条准确、哪一条必须改。说明一：全国人民代表大会是最高国家权力机关。这条正确。说明二：国务院就是人民法院，都是管审判的。这条要改。国务院即中央人民政府，是最高国家行政机关，管国家的行政工作；人民法院是国家的审判机关，依法行使审判权。两个机关性质完全不同，「一府」和「两院」不能混在一起。说明三：人民政府、监察委员会、人民法院、人民检察院，都由本级人民代表大会产生，对它负责，受它监督。这条正确，这就是「一府一委两院」与人民代表大会的关系。说明四：地方上，学校门口路灯坏了这种事，只能报到国务院去解决。这条要改。地方各级人民政府是地方各级国家行政机关，本地区这样的事务由它们负责；遇到事情要按「事情有多大范围」来判断。说明五：一切国家机关和国家工作人员，都要倾听人民的意见和建议，接受人民的监督。这条正确，国家机构的权力是人民给的，也必须接受人民的监督。这里有一个常见错误要提醒：有的同学把「人民法院审、人民检察院察」记岔了，看到「诉」就选法院。可以这样记：先由人民检察院依法提起公诉，再由人民法院依法审理，一步接一步。",
    "conceptest-1": "接下来用三道题考考你，每道题里都藏着一个容易想歪的地方。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件任务交给你：把自己的一条建议真正送出去。下面分三步：先选一个你身边真想推动的问题，再找出主管这件事的国家机构，最后选一种合适的表达方式。三步选完，我会把它们拼成一张办事路线卡，你可以照着一步步去做。",
    "posttest": "最后一轮，换几个新情境来考考你。这次会遇到社区公告栏、跨省的工程和班里的建议箱，看看今天学的判断还用不用得上。",
    "summary": "这节课我们弄清楚四件事。第一，国家机构是国家机关的统称，人民代表大会制度是我国的根本政治制度，全国人民代表大会是最高国家权力机关。第二，职权分工：全国人民代表大会和全国人民代表大会常务委员会行使国家立法权；国务院即中央人民政府，是最高国家行政机关；地方各级人民政府是地方各级国家行政机关；人民法院是国家的审判机关；人民检察院是国家的法律监督机关；监察委员会是行使国家监察职能的专责机关。第三，「一府一委两院」——人民政府、监察委员会、人民法院、人民检察院，都由本级人民代表大会产生，对它负责，受它监督；人民代表大会代表代表人民的利益和意志，为人民说话。第四，一切国家机关和国家工作人员都要接受人民的监督，努力为人民服务。最后送一句口诀给你：人大定、国务院办、法院审、检察院察、监委督；要办事，先看这事有多大范围。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出国家机构是什么的统称，再写出全国人民代表大会、国务院、地方各级人民政府、人民法院、人民检察院各自的职权，各写一句话。第二层能力应用，动手做：观察自己家附近或学校附近挂着机构牌子的地方，记下两个机构的全称，判断它们属于哪一类，说一说你是怎么判断的。第三层迁移挑战，选做：从社区和校园里找一个你真正关心的问题，写一份建议，说清楚这件事该找哪一类国家机构、为什么找它，以及你打算用什么方式把建议送出去，做完在班里交流一遍。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域里的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 国家机构有哪些", "lab-1": "动手一 事情该找哪个机构",
    "module-2": "概念二 各自的职权分工", "lab-2": "动手二 机构名片与职权配对",
    "worked-example": "例题示范 机构名牌校对", "conceptest-1": "概念测试",
    "synthesis": "综合任务 我的建议送出去", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一（★核心模拟）：「事情该找哪个机构」对照台（6 情境 × 选机构 + 说理由） ──
FIND = [
    {"k": "f1", "n": "国家要制定一部保护未成年人的新法律",
     "case": "新闻里说，国家正在制定一部保护未成年人的新法律，要把草案提请审议。这件事该由哪一类机构来审议通过？",
     "opts": [
         {"t": "全国人民代表大会及其常务委员会", "ok": True},
         {"t": "国务院", "ok": False},
         {"t": "人民法院", "ok": False},
         {"t": "人民检察院", "ok": False}],
     "why": "全国人民代表大会和全国人民代表大会常务委员会行使国家立法权，法律由它们审议通过。制定法律属于立法，是权力机关的职权。",
     "mis": "常见错误是把「制定法律」和「执行法律」<strong>搞混</strong>了。国务院是最高国家行政机关，负责执行法律、管理国家的行政工作；定规矩这件事要由行使国家立法权的机关来做。还可以试试：先问一句——这是「定规矩」还是「办事」。"},
    {"k": "f2", "n": "一条跨省的高速铁路要开工建设",
     "case": "国家要建设一条跨省的高速铁路，需要由国家最高行政机关统一部署推进。这件事该找哪一类机构？",
     "opts": [
         {"t": "国务院", "ok": True},
         {"t": "全国人民代表大会", "ok": False},
         {"t": "人民法院", "ok": False},
         {"t": "地方各级人民政府", "ok": False}],
     "why": "国务院，即中央人民政府，是最高国家权力机关的执行机关，是最高国家行政机关。全国性的行政工作由它统一部署。",
     "mis": "容易把「最高国家权力机关」和「最高国家行政机关」<strong>误认为</strong>是一回事。可以这样记：全国人民代表大会是最高国家权力机关，国务院是最高国家行政机关，一个定、一个办。还可以试试：看到「全国范围」这个词，先想想这件事是决策还是执行。"},
    {"k": "f3", "n": "学校门口这条路一直没有路灯",
     "case": "同学们放学经过的一段路一直没有路灯，晚上走路不方便，居民想请人尽快把路灯装上。这件事该找哪一类机构？",
     "opts": [
         {"t": "地方各级人民政府", "ok": True},
         {"t": "国务院", "ok": False},
         {"t": "人民法院", "ok": False},
         {"t": "人民检察院", "ok": False}],
     "why": "地方各级人民政府是地方各级国家行政机关，本地区的这类公共事务由它们负责。路和路灯这些公共设施的事情，属于行政事务。",
     "mis": "有的同学一遇到事情就说「报到国务院去」。这样可能会：把身边的小事报到了不该报的地方，反而耽误时间。还可以试试：按「事情有多大范围」来判断——自己家门口这一段路的事，先找当地的政府；真是跨省、全国性的大工程，才是国务院的事。"},
    {"k": "f4", "n": "有人涉嫌犯罪，要依法审理",
     "case": "有人涉嫌犯罪，要由哪个机关依法审理，判明他应当承担什么责任？",
     "opts": [
         {"t": "人民法院", "ok": True},
         {"t": "人民检察院", "ok": False},
         {"t": "国务院", "ok": False},
         {"t": "全国人民代表大会", "ok": False}],
     "why": "人民法院是国家的审判机关，依法行使审判权。判明一个人该承担什么责任，是审判机关的职权。",
     "mis": "常见错误是把人民法院和人民检察院<strong>搞混</strong>。可以这样记：人民法院「审」，人民检察院「察」，一个负责审理，一个负责法律监督。还可以试试：把「审理、判决」这两个词和人民法院连在一起记。"},
    {"k": "f5", "n": "有人涉嫌犯罪，要依法提起公诉",
     "case": "有人涉嫌犯罪，要由哪个机关依法提起公诉，把案件送交法院审理？",
     "opts": [
         {"t": "人民检察院", "ok": True},
         {"t": "人民法院", "ok": False},
         {"t": "地方各级人民政府", "ok": False},
         {"t": "全国人民代表大会", "ok": False}],
     "why": "人民检察院是国家的法律监督机关，依法行使检察权，对涉嫌犯罪的依法提起公诉。",
     "mis": "把「诉」和「审」<strong>搞混</strong>，这一步就会选错。这样可能会：把两个环节的顺序记反。还可以试试：按顺序念一遍——先由人民检察院依法提起公诉，再由人民法院依法审理，一步接一步。"},
    {"k": "f6", "n": "想把一条建议反映上去",
     "case": "几位同学对一部正在征求意见的法律有一些自己的想法，想把意见反映上去。下面哪种方式更合适？",
     "opts": [
         {"t": "整理成清楚的意见，交给身边的人民代表大会代表", "ok": True},
         {"t": "直接去人民法院，请人民法院改这部法律", "ok": False},
         {"t": "直接去人民检察院，请人民检察院改这部法律", "ok": False},
         {"t": "等长大以后再说，现在这件事和自己没关系", "ok": False}],
     "why": "全国人民代表大会和地方各级人民代表大会的代表，代表人民的利益和意志，依法参加行使国家权力；他们密切联系群众，听取和反映群众的意见和要求。把意见交给身边的人民代表大会代表，是一条正当、畅通的路。",
     "mis": "有的同学<strong>误认为</strong>提意见和自己没关系，也有人把人民法院、人民检察院当成了改法律的地方。这样可能会：找错了门，意见反而送不到。还可以试试：先把想法写清楚——想让法律解决什么问题、希望怎么调整，再请老师或者家长帮忙一起交上去。"},
]

# ── 动手二：「机构名片与职权配对台」（5 张机构名片 × 5 张职权卡） ──
ORGS = [
    {"k": "o1", "n": "全国人民代表大会",
     "what": "我国的最高国家权力机关。它的常设机关是全国人民代表大会常务委员会。",
     "pair": "c1",
     "why": "全国人民代表大会是最高国家权力机关；全国人民代表大会和全国人民代表大会常务委员会行使国家立法权。",
     "tip": "还可以试试：把「最高国家权力机关」这七个字和全国人民代表大会连在一起念三遍。"},
    {"k": "o2", "n": "国务院（中央人民政府）",
     "what": "中央国家行政机关，管理国家的行政工作。",
     "pair": "c2",
     "why": "国务院，即中央人民政府，是最高国家权力机关的执行机关，是最高国家行政机关。",
     "tip": "还可以试试：想一想「执行机关」这四个字——法律定下来以后，由谁去落实。"},
    {"k": "o3", "n": "地方各级人民政府",
     "what": "本行政区域里的国家行政机关。",
     "pair": "c3",
     "why": "地方各级人民政府是地方各级国家行政机关，管的是本地区的行政事务，比如身边的道路、绿化、公共服务。",
     "tip": "还可以试试：找一找自己身边属于这一类机构的办事场所，看看门牌上的全称。"},
    {"k": "o4", "n": "人民法院",
     "what": "我国的审判机关。",
     "pair": "c4",
     "why": "人民法院是国家的审判机关，依法行使审判权。",
     "tip": "还可以试试：把「审理、判决」和人民法院连在一起记，别和人民检察院记岔。"},
    {"k": "o5", "n": "人民检察院",
     "what": "我国的法律监督机关。",
     "pair": "c5",
     "why": "人民检察院是国家的法律监督机关，依法行使检察权。",
     "tip": "还可以试试：把「法律监督」和人民检察院连在一起记。"},
]

POWERS = [
    {"k": "c1", "n": "最高国家权力机关；行使国家立法权", "pair": "o1"},
    {"k": "c2", "n": "最高国家权力机关的执行机关；最高国家行政机关", "pair": "o2"},
    {"k": "c3", "n": "地方各级国家行政机关", "pair": "o3"},
    {"k": "c4", "n": "国家的审判机关", "pair": "o4"},
    {"k": "c5", "n": "国家的法律监督机关", "pair": "o5"},
]

# ── 综合任务：「我的建议送出去」行动台 ──
ADVICE = {
    "issues": [
        {"k": "i1", "n": "上学路上有一段路没有路灯"},
        {"k": "i2", "n": "社区里的健身器材坏了很久没人修"},
        {"k": "i3", "n": "学校门口上下学时车辆太多、秩序乱"},
    ],
    "orgs": [
        {"t": "地方各级人民政府——这是本地区里的行政事务", "ok": True,
         "why": "想得准确。地方各级人民政府是地方各级国家行政机关，与生活相关的这类公共事务由它们负责。"},
        {"t": "人民法院——请人民法院来处理", "ok": False,
         "why": "这样可能会：把行政上的事送到了审判机关。还可以试试：先分清这件事是「需要有人去修、去管」，还是「需要依法审理」。"},
        {"t": "全国人民代表大会——请最高国家权力机关来处理", "ok": False,
         "why": "这样可能会：把家门口的小事报到了全国层面。还可以试试：按「事情有多大范围」来判断，自己身边的公共设施，先找当地的政府。"},
    ],
    "ways": [
        {"t": "把问题写清楚：在哪、什么事、希望怎么解决，请老师或家长陪着交给身边的人大代表", "ok": True,
         "why": "这是既守规矩、又走得通的一步。人民代表大会代表密切联系群众，听取和反映群众的意见和要求。"},
        {"t": "在网上把这件事说得很夸张、很难听，引起大家注意", "ok": False,
         "why": "这样可能会：话说过了头，反而伤了别人，问题也没解决。还可以试试：改成把事实写清楚——时间、地点、具体是什么问题。"},
        {"t": "先跟几个同学商量清楚，再一起向学校或者社区说明情况", "ok": True,
         "why": "这也是合适的一步。先把事实和想法商量清楚，再一起反映，意见更容易被听明白，也更容易推动起来。"},
    ],
}

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g6-u3 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) ★「事情该找哪个机构」对照台：6 个情境，每个四选一
   3) 「机构名片与职权配对台」：5 张机构名片 × 5 张职权卡
   4) 「我的建议送出去」行动台：问题 → 主管机构 → 表达方式 → 合成路线卡
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

  /* ---------- 2. ★「事情该找哪个机构」对照台 ---------- */
  var FIND = __FIND_JSON__;
  var stage1 = document.getElementById('fd-stage');
  if (stage1) {
    var cur = null;
    var done1 = {};
    var out1 = document.getElementById('fd-out');
    var panel1 = document.getElementById('fd-panel');
    function findItem(k) {
      for (var i = 0; i < FIND.length; i++) { if (FIND[i].k === k) return FIND[i]; }
      return null;
    }
    function render1() {
      document.querySelectorAll('[data-fd-item]').forEach(function (b) {
        var k = b.dataset.fdItem;
        b.classList.toggle('selected', k === cur);
        b.classList.toggle('correct', !!done1[k]);
      });
      document.getElementById('fd-score').textContent =
        '已经判断 ' + Object.keys(done1).length + ' / ' + FIND.length + ' 个情境';
      if (!cur) { panel1.innerHTML = ''; return; }
      var F = findItem(cur);
      var html = '<div style="font-weight:700;font-size:14px;margin:14px 0 0">' + F.case + '</div>';
      html += '<div class="grid" style="margin-top:10px">';
      F.opts.forEach(function (o, i) {
        var cls = 'choice';
        if (done1[F.k] && o.ok) cls += ' correct';
        html += '<button class="' + cls + '" data-fd-opt="' + i + '" style="text-align:left">' + o.t + '</button>';
      });
      html += '</div>';
      panel1.innerHTML = html;
      panel1.querySelectorAll('[data-fd-opt]').forEach(function (b) {
        b.addEventListener('click', function () { choose(parseInt(b.dataset.fdOpt, 10)); });
      });
    }
    function rightText(F) {
      for (var i = 0; i < F.opts.length; i++) { if (F.opts[i].ok) return F.opts[i].t; }
      return '';
    }
    function choose(i) {
      var F = findItem(cur);
      var o = F.opts[i];
      var first = !done1[F.k];
      done1[F.k] = true;
      if (o.ok) {
        out1.className = 'result';
        out1.innerHTML = '<strong>找对了。</strong>' + F.why;
      } else if (first) {
        out1.className = 'result warn';
        out1.innerHTML = '<strong>这样可能会找错门：' + o.t + '</strong>' + F.why +
          '<br><span style="color:var(--muted)"><strong>错因提醒：</strong>' + F.mis + '</span>';
      } else {
        out1.className = 'result';
        out1.innerHTML = '<strong>该找的是：' + rightText(F) + '。</strong>' + F.why;
      }
      render1();
      if (Object.keys(done1).length === FIND.length) {
        out1.innerHTML += '<br><br><strong>六个情境都判断过了。</strong>' +
          '记住这句口诀：人大定、国务院办、法院审、检察院察、监委督；要办事，先看这事有多大范围。';
      }
    }
    document.querySelectorAll('[data-fd-item]').forEach(function (b) {
      b.addEventListener('click', function () {
        cur = b.dataset.fdItem;
        out1.className = 'result warn';
        out1.textContent = '先读一读情境，想一想这件事是「定规矩」还是「办事」，再在下面选一个。';
        render1();
      });
    });
    render1();
  }

  /* ---------- 3. 「机构名片与职权配对台」 ---------- */
  var ORGS = __ORGS_JSON__;
  var POWERS = __POWERS_JSON__;
  var stage2 = document.getElementById('mt-stage');
  if (stage2) {
    var selO = null;
    var matched = {};
    var out2 = document.getElementById('mt-out');
    var leftEl = document.getElementById('mt-left');
    var rightEl = document.getElementById('mt-right');
    var board = document.getElementById('mt-board');
    function orgByKey(k) {
      for (var i = 0; i < ORGS.length; i++) { if (ORGS[i].k === k) return ORGS[i]; }
      return null;
    }
    function render2() {
      leftEl.innerHTML = '';
      ORGS.forEach(function (O) {
        var b = document.createElement('button');
        b.className = 'choice' + (matched[O.k] ? ' correct' : (selO === O.k ? ' selected' : ''));
        b.style.textAlign = 'left';
        b.innerHTML = '<strong>' + O.n + '</strong><br><span style="color:var(--muted);font-size:14px">' + O.what + '</span>' +
          (matched[O.k] ? '<br><span style="color:var(--accent-deep);font-size:14px">已配对 ✓</span>' : '');
        b.addEventListener('click', function () {
          if (matched[O.k]) return;
          selO = O.k;
          out2.className = 'result warn';
          out2.innerHTML = '<strong>你选了「' + O.n + '」。</strong>现在到右边点一张你认为属于它的职权卡。';
          render2();
        });
        leftEl.appendChild(b);
      });
      rightEl.innerHTML = '';
      POWERS.forEach(function (P) {
        var b = document.createElement('button');
        b.className = 'choice' + (matched[P.k] ? ' correct' : '');
        b.style.textAlign = 'left';
        b.innerHTML = '<strong>' + P.n + '</strong>' +
          (matched[P.k] ? '<br><span style="color:var(--accent-deep);font-size:14px">配对成功 ✓</span>' : '');
        b.addEventListener('click', function () {
          if (matched[P.k]) return;
          if (!selO) {
            out2.className = 'result warn';
            out2.innerHTML = '先到左边点一张机构名片，再回到右边点职权卡。' +
              '<br><span style="color:var(--muted)">还可以试试：先读职权卡上的关键词——「权力机关」「行政机关」「审判」「法律监督」。</span>';
            return;
          }
          if (selO === P.pair) {
            var OO = orgByKey(selO);
            matched[P.pair] = true;
            selO = null;
            out2.className = 'result';
            out2.innerHTML = '<strong>配上了：' + OO.n + ' —— ' + P.n + '</strong>' + OO.why;
            if (Object.keys(matched).length === ORGS.length) {
              out2.innerHTML += '<br><br><strong>五组都配上了。</strong>把这张表连起来看，就是一条清楚的链条：' +
                '立法机关定规矩，行政机关去办事，审判机关依法审理，检察机关依法监督，监察机关依法开展监察。';
            }
          } else {
            var SO = orgByKey(selO);
            out2.className = 'result warn';
            out2.innerHTML = '<strong>这张职权卡和「' + SO.n + '」配不上。</strong>' +
              '这样可能会：把不同性质的机关搞混，办事时找错门。' + SO.tip;
          }
          render2();
        });
        rightEl.appendChild(b);
      });
      board.textContent = '已经配对 ' + Object.keys(matched).length + ' / ' + ORGS.length + ' 组';
    }
    render2();
  }

  /* ---------- 4. 「我的建议送出去」行动台 ---------- */
  var ADVICE = __ADVICE_JSON__;
  var stage3 = document.getElementById('ad-stage');
  if (stage3) {
    var pick = { i: null, o: null, w: null };
    var out3 = document.getElementById('ad-out');
    var panel3 = document.getElementById('ad-panel');
    function issueByKey(k) {
      for (var i = 0; i < ADVICE.issues.length; i++) { if (ADVICE.issues[i].k === k) return ADVICE.issues[i]; }
      return null;
    }
    function render3() {
      var html = '<div style="font-weight:700;font-size:14px;margin-bottom:6px">第一步 · 我想推动的一个问题</div><div class="grid grid-2">';
      ADVICE.issues.forEach(function (C) {
        html += '<button class="choice' + (pick.i === C.k ? ' selected' : '') +
          '" data-ad-issue="' + C.k + '" style="text-align:left">' + C.n + '</button>';
      });
      html += '</div>';
      html += '<div style="font-weight:700;font-size:14px;margin:16px 0 6px">第二步 · 主管这件事的国家机构</div><div class="grid">';
      ADVICE.orgs.forEach(function (o, i) {
        var cls = 'choice';
        if (pick.o === i) cls += o.ok ? ' correct' : ' wrong';
        html += '<button class="' + cls + '" data-ad-org="' + i + '" style="text-align:left">' + o.t + '</button>';
      });
      html += '</div>';
      html += '<div style="font-weight:700;font-size:14px;margin:16px 0 6px">第三步 · 我打算用哪种方式把建议送出去</div><div class="grid">';
      ADVICE.ways.forEach(function (o, i) {
        var cls = 'choice';
        if (pick.w === i) cls += o.ok ? ' correct' : ' wrong';
        html += '<button class="' + cls + '" data-ad-way="' + i + '" style="text-align:left">' + o.t + '</button>';
      });
      html += '</div>';
      panel3.innerHTML = html;
      panel3.querySelectorAll('[data-ad-issue]').forEach(function (b) {
        b.addEventListener('click', function () {
          pick.i = b.dataset.adIssue; render3();
          out3.className = 'result warn';
          out3.textContent = '问题选好了，接着选第二步：这件事该找哪一类国家机构。';
        });
      });
      panel3.querySelectorAll('[data-ad-org]').forEach(function (b) {
        b.addEventListener('click', function () {
          pick.o = parseInt(b.dataset.adOrg, 10);
          var o = ADVICE.orgs[pick.o];
          out3.className = 'result' + (o.ok ? '' : ' warn');
          out3.innerHTML = (o.ok ? '<strong>这一步找得准。</strong>' : '<strong>这一步还可以再想想。</strong>') + o.why;
          render3();
        });
      });
      panel3.querySelectorAll('[data-ad-way]').forEach(function (b) {
        b.addEventListener('click', function () {
          pick.w = parseInt(b.dataset.adWay, 10);
          render3();
          if (pick.i === null || pick.o === null) {
            out3.className = 'result warn';
            out3.textContent = '三步还没选完，先把前面的补齐。';
            return;
          }
          var C = issueByKey(pick.i);
          var O = ADVICE.orgs[pick.o];
          var W = ADVICE.ways[pick.w];
          var okN = (O.ok ? 1 : 0) + (W.ok ? 1 : 0);
          out3.className = 'result' + (okN >= 1 ? '' : ' warn');
          out3.innerHTML = '<strong>我的办事路线卡 · ' + C.n + '</strong><br>' +
            '第一步：' + C.n + '<br>第二步：' + O.t + '<br>第三步：' + W.t +
            '<br><span style="color:var(--muted)">' + (okN === 2
              ? '机构找对了，方式也想清楚了。把这张路线卡留好，照着一步步去做。'
              : '还可以再想一想：先分清这件事是行政上的事还是需要依法审理的事，再把话说小一点、说具体一点。换一个再试一次。') + '</span>';
        });
      });
    }
    render3();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__FIND_JSON__', json.dumps(FIND, ensure_ascii=False))
             .replace('__ORGS_JSON__', json.dumps(ORGS, ensure_ascii=False))
             .replace('__POWERS_JSON__', json.dumps(
                 [POWERS[3], POWERS[0], POWERS[4], POWERS[2], POWERS[1]], ensure_ascii=False))
             .replace('__ADVICE_JSON__', json.dumps(ADVICE, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：国家机构，你听说过哪几个？", TTS["pretest"], [
        {"q": "下面哪一句话说得准确？",
         "options": [("全国人民代表大会是最高国家权力机关", True),
                     ("国务院是最高国家权力机关", False),
                     ("人民法院是最高国家行政机关", False)],
         "explain": "全国人民代表大会是最高国家权力机关；国务院是最高国家行政机关；人民法院是国家的审判机关。"
                    "<strong>错因提醒：</strong>常见错误是把「最高国家权力机关」和「最高国家行政机关」<strong>搞混</strong>了，"
                    "也有的同学误认为人民法院管行政。这三个名称一个都不能张冠李戴。"},
        {"q": "「一府一委两院」指的是下面哪一组？",
         "options": [("人民政府、监察委员会、人民法院、人民检察院", True),
                     ("人民政府、人民法院、人民检察院、学校", False),
                     ("人民代表大会、人民政府、人民法院、人民检察院", False)],
         "explain": "「一府一委两院」指人民政府、监察委员会、人民法院、人民检察院；它们都由本级人民代表大会产生，对它负责，受它监督。"
                    "<strong>错因提醒：</strong>有的同学把人民代表大会也算了进去，这样就<strong>搞混</strong>了——"
                    "人民代表大会是产生它们的机关，不在「一府一委两院」里面。"},
        {"q": "学校门口的一段路一直没有路灯，居民想请人尽快装上。这件事最该找哪一类机构？",
         "options": [("地方各级人民政府", True),
                     ("人民法院", False),
                     ("人民检察院", False)],
         "explain": "地方各级人民政府是地方各级国家行政机关，本地区的这类公共事务由它们负责。"
                    "<strong>错因提醒：</strong>有的同学<strong>误认为</strong>身边的事要和人民法院打交道。"
                    "这样可能会：找错了门。还可以试试：先分清这件事是「需要有人去修、去管」，还是「需要依法审理」。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "国家机构有哪些：一套制度，一串机构", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们每天路过挂着牌子的机关大门，却常常说不出它们分别管什么（And）；可遇到事情总要找对人，找错了门，事情就办不成（But）；所以这节课先把国家机构的名称和分工弄清楚（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px"><strong>国家机构，是国家机关的统称。</strong>我国的国家机构，包括中央国家机构和地方国家机构；把它们组织起来的制度，叫<strong>人民代表大会制度</strong>，它是我国的<strong>根本政治制度</strong>。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>全国人民代表大会</strong>是最高国家权力机关。它的常设机关是全国人民代表大会常务委员会。</div></div>
          <div class="step"><span class="n">2</span><div><strong>由民主选举产生：</strong>全国人民代表大会和地方各级人民代表大会都由民主选举产生，对人民负责，受人民监督。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>「一府一委两院」：</strong>国家行政机关、监察机关、审判机关、检察机关都由人民代表大会产生，对它负责，受它监督。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="国家机构职权分工抽象示意图：四栏分别标注立法、行政、审判、检察，用抽象建筑剪影与抽象符号表示，附中文标注，不含国徽国旗与徽章">
          <figcaption>职权分工示意：立法机关定规矩 · 行政机关去办事 · 审判机关依法审理 · 检察机关依法监督（抽象示意图，不按比例）</figcaption>
        </figure>
        <div class="inner-card">
          <p><strong>三句话，把名称记准</strong></p>
          <p style="color:var(--muted)">全国人民代表大会是<strong>最高国家权力机关</strong>；国务院即中央人民政府，是<strong>最高国家行政机关</strong>；人民法院是<strong>国家的审判机关</strong>，人民检察院是<strong>国家的法律监督机关</strong>。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>国家机构离自己很远；也有的同学<strong>误认为</strong>人民代表大会和人民政府是一回事。其实前者是权力机关，后者是行政机关，分工不一样。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "社区办事的窗口、新闻里的法律、路边新装的路灯，背后都是国家机构在工作。它们不是远在天边，而是天天在你身边。"},
    {"lens": "解释它", "text": "为什么这些机关都要「对它负责，受它监督」？因为国家机构的权力来自人民。人民代表大会由民主选举产生、对人民负责，再由它产生其他机关，权力的来路就是清楚的。"},
    {"lens": "迁移它", "text": "这就像班里的结构：全班同学选出班委会，班委会再去安排各个小组做事，班委会要向全班同学负责，也要接受大家的监督。"},
])}
    ''', tag="概念一"))

    find_btns = "\n".join(
        f'            <button class="choice" data-fd-item="{f["k"]}" style="text-align:left">'
        f'<strong>{f["n"]}</strong></button>'
        for f in FIND
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "★动手一：事情该找哪个机构？", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">挑一个情境，读清楚，再从下面几个机构里选出你认为该找的那一类。选完马上看到理由；选错了，会告诉你错在哪里。</p>
        <div class="lab-panel">
          <div id="fd-stage">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 挑一个情境</div>
            <div class="grid grid-2">
{find_btns}
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">判断进度</span><span class="v" id="fd-score">已经判断 0 / 6 个情境</span></div>
          </div>
          <p class="result warn" id="fd-out" style="margin-top:12px">先点一个情境。</p>
          <div id="fd-panel"></div>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🏛️</span><div><strong>判断的小窍门：</strong>先问两句话——这是「定规矩」还是「办事」？这件事有多大范围？问完这两句，大半情境都能选对。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "各自的职权分工：定、办、审、察、督", TTS["module-2"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们已经知道国家机构有哪些（And）；可它们各自管什么，名字常常被混着用（But）；所以这节课把立法、行政、审判、检察、监察的分工一条条说清楚（Therefore）。</p>
        </div>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>立法 · 行政</strong></p>
            <p style="color:var(--muted)">全国人民代表大会和全国人民代表大会常务委员会行使国家立法权；国务院即中央人民政府，是最高国家权力机关的执行机关，是最高国家行政机关；地方各级人民政府是地方各级国家行政机关。</p>
          </div>
          <div class="inner-card">
            <p><strong>审判 · 检察 · 监察</strong></p>
            <p style="color:var(--muted)">人民法院是国家的审判机关，依法行使审判权；人民检察院是国家的法律监督机关，依法行使检察权；监察委员会是行使国家监察职能的专责机关。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="人民代表大会与一府一委两院关系抽象示意图：下方用抽象柱廊建筑剪影表示人民代表大会，上方用四个抽象剪影表示人民政府、监察委员会、人民法院、人民检察院，中间用箭头标注由它产生、对它负责、受它监督，附中文标注，不含国徽">
          <figcaption>关系图：人民政府、监察委员会、人民法院、人民检察院由本级人民代表大会产生，对它负责，受它监督（抽象示意图，不按比例）</figcaption>
        </figure>
        <div class="inner-card">
          <p><strong>代表为人民</strong></p>
          <p style="color:var(--muted)">全国人民代表大会和地方各级人民代表大会的代表，代表人民的利益和意志，依法参加行使国家权力；他们密切联系群众，听取和反映群众的意见和要求。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>人民法院和人民检察院差不多。其实一个「审」、一个「察」：先由人民检察院依法提起公诉，再由人民法院依法审理。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "同一件事，在不同环节会经不同的机关：有人涉嫌犯罪，先由人民检察院依法提起公诉，再由人民法院依法审理。"},
    {"lens": "解释它", "text": "为什么要分成几家、而不是一家说了算？因为分工之后，权力之间才能相互制约、相互监督，事情才更不容易办偏。"},
    {"lens": "迁移它", "text": "这就像班里的分工：有人负责出题，有人负责判卷，还有人负责核对。同一个人的活儿由不同的人把关，结果才更让人放心。"},
])}
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "★动手二：机构名片与职权配对台", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点左边一张<strong>机构名片</strong>，再点右边一张你认为属于它的<strong>职权卡</strong>。配对了会连起来，配错了会告诉你错在哪里。</p>
        <div class="lab-panel">
          <div id="mt-stage">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">点击左侧机构名片，再点右侧职权卡进行配对</div>
            <div class="grid grid-2">
              <div id="mt-left"></div>
              <div id="mt-right"></div>
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">配对进度</span><span class="v" id="mt-board">已经配对 0 / 5 组</span></div>
          </div>
          <p class="result warn" id="mt-out" style="margin-top:12px">先点左边一张机构名片。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">⚖️</span><div><strong>配完回头看：</strong>把五组连起来读一遍，就是一句口诀——人大定、国务院办、法院审、检察院察、监委督。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：机构名牌校对，五条说明哪条要改", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>学校要做一面「身边的国家机构」展示墙，几位同学写了五条说明。请你当一次校对员，判断哪一条正确、哪一条必须改。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>说明一（正确）：</strong>「全国人民代表大会是最高国家权力机关。」</div></div>
          <div class="step"><span class="n">2</span><div><strong>说明二（必须改）：</strong>「国务院就是人民法院，都是管审判的。」国务院即中央人民政府，是最高国家行政机关；人民法院是国家的审判机关。</div></div>
          <div class="step"><span class="n">3</span><div><strong>说明三（正确）：</strong>「人民政府、监察委员会、人民法院、人民检察院，都由本级人民代表大会产生，对它负责，受它监督。」</div></div>
          <div class="step"><span class="n">4</span><div><strong>说明四（必须改）：</strong>「学校门口路灯坏了，只能报到国务院去解决。」地方各级人民政府是地方各级国家行政机关，本地区这样的事务由它们负责。</div></div>
          <div class="step"><span class="n green">5</span><div><strong>说明五（正确）：</strong>「一切国家机关和国家工作人员，都要倾听人民的意见和建议，接受人民的监督。」</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学把「人民法院审、人民检察院察」记岔了，看到「诉」就选人民法院；也有的同学把地方上的小事一直往上报。这样可能会：找错了门，事情反而办不成。可以这样记：人民检察院依法提起公诉，人民法院依法审理，一步接一步。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三句话，藏着三个容易想歪的地方", TTS["conceptest-1"], [
        {"q": "关于国家机构，下面哪句话说得准确？",
         "options": [("人民政府、监察委员会、人民法院、人民检察院都由本级人民代表大会产生，对它负责，受它监督", True),
                     ("人民政府和人民代表大会是同一个机关，只是叫法不同", False),
                     ("人民法院和人民检察院的职权完全一样", False)],
         "explain": "人民代表大会是权力机关，人民政府是行政机关；人民法院是国家的审判机关，人民检察院是国家的法律监督机关，职权并不相同。"
                    "<strong>错因提醒：</strong>常见错误是把这些机关的名称<strong>搞混</strong>，或者<strong>误认为</strong>「一府一委两院」里还包括人民代表大会。"},
        {"q": "有人涉嫌犯罪，先由哪个机关依法提起公诉，再由哪个机关依法审理？",
         "options": [("先由人民检察院依法提起公诉，再由人民法院依法审理", True),
                     ("先由人民法院提起公诉，再由人民检察院审理", False),
                     ("由地方各级人民政府提起公诉并审理", False)],
         "explain": "人民检察院是国家的法律监督机关，依法行使检察权；人民法院是国家的审判机关，依法行使审判权，两个环节前后相接。"
                    "<strong>错因提醒：</strong>把「诉」和「审」<strong>搞混</strong>，顺序就会记反。还可以试试：念一遍「检察院诉、法院审」，把它们连起来记。"},
        {"q": "社区里的一段路没有路灯，居民想请人尽快装上。下面哪种做法更合适？",
         "options": [("把情况写清楚，向地方各级人民政府反映", True),
                     ("直接请人民法院来处理路灯的事", False),
                     ("把这件事一直报到国务院去", False)],
         "explain": "地方各级人民政府是地方各级国家行政机关，本地区的这类公共事务由它们负责。"
                    "<strong>错因提醒：</strong>有的同学<strong>误认为</strong>级别越高越管用。这样可能会：把身边的小事报到了不该报的地方。还可以试试：按「事情有多大范围」来判断。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：我的建议送出去", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">三步各选一个：<strong>我想推动的问题 → 主管这件事的国家机构 → 我打算用的表达方式</strong>。选完，你就有了自己的办事路线卡。</p>
        <div class="lab-panel">
          <div id="ad-stage"></div>
          <div id="ad-panel"></div>
          <p class="result warn" id="ad-out" style="margin-top:12px">从第一步开始选。</p>
        </div>
        <div class="inner-card" style="margin-top:14px">
          <p><strong>把它写下来：</strong></p>
          <p style="color:var(--muted)">用三句话写清楚：我想推动的问题是……；这件事该找的国家机构是……；我打算这样把建议送出去……。</p>
          <textarea id="syn-answer" rows="3" placeholder="我想推动的问题是……；这件事该找的国家机构是……；我打算这样把建议送出去……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，判断还准不准", TTS["posttest"], [
        {"q": "社区公告栏上贴出一份正在征求意见的草案，居民可以把自己的想法反映上去。下面哪种说法更合适？",
         "options": [("这是公民参与国家和社会事务的一种方式，意见可以通过人民代表大会代表等途径反映上去", True),
                     ("征求意见只是走个形式，反映了也没用", False),
                     ("只有大人才能反映意见，小学生说了不算", False)],
         "explain": "人民代表大会代表密切联系群众，听取和反映群众的意见和要求；公民可以依法参与国家和社会事务。"
                    "<strong>错因提醒：</strong>有的同学<strong>误认为</strong>「提意见和自己没关系」。还可以试试：先把想法写清楚——想让法律或者政府解决什么问题、希望怎么调整。"},
        {"q": "国家要建设一条跨省的高速铁路，需要统一部署推进。这件事该找哪一类机构？",
         "options": [("国务院，它是最高国家行政机关", True),
                     ("人民法院，它负责审理工程中的纠纷", False),
                     ("人民检察院，它负责法律监督", False)],
         "explain": "国务院即中央人民政府，是最高国家权力机关的执行机关，是最高国家行政机关，全国性的行政工作由它统一部署。"
                    "<strong>错因提醒：</strong>容易把「最高国家权力机关」和「最高国家行政机关」<strong>搞混</strong>。还可以试试：看到「全国范围」，先想想这是决策还是执行。"},
        {"q": "班里的建议箱收到一条建议：「希望学校门口上下学时有人疏导交通。」如果要把这条建议反映给国家机构，最合适的是哪一类？",
         "options": [("地方各级人民政府，这是本地区的公共事务", True),
                     ("全国人民代表大会，请它直接派人来疏导", False),
                     ("人民法院，请它派人来疏导", False)],
         "explain": "地方各级人民政府是地方各级国家行政机关，本地区的公共事务由它们负责；涉及法规层面需要调整的，还可以通过人民代表大会代表反映。"
                    "<strong>错因提醒：</strong>有的同学把身边的事一路报到了全国层面。这样可能会：事情绕了一大圈还没办成。还可以试试：先判断这件事有多大范围。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：有哪些、管什么、谁监督", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>有哪些：</strong>国家机构是国家机关的统称；人民代表大会制度是我国的根本政治制度；全国人民代表大会是最高国家权力机关。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>管什么：</strong>全国人民代表大会和全国人民代表大会常务委员会行使国家立法权；国务院即中央人民政府，是最高国家行政机关；地方各级人民政府是地方各级国家行政机关；人民法院是国家的审判机关；人民检察院是国家的法律监督机关；监察委员会是行使国家监察职能的专责机关。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>什么关系：</strong>「一府一委两院」——人民政府、监察委员会、人民法院、人民检察院，都由本级人民代表大会产生，对它负责，受它监督。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>谁监督：</strong>一切国家机关和国家工作人员都必须依靠人民的支持，倾听人民的意见和建议，接受人民的监督，努力为人民服务。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>一句口诀：</strong>人大定、国务院办、法院审、检察院察、监委督；要办事，先看这事有多大范围。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「全国人民代表大会」和「地方各级人民政府」这两个规范名称，给家里人讲清楚：为什么有的事要找当地的政府，有的事要找全国人民代表大会。</p>
          <p style="color:var(--muted)">再动一动手：<strong>写一写</strong>五个机构的全称和它们各自的职权，每一个都用一句话说明它在生活里是什么样子。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写出国家机构是什么的统称，再写出人民代表大会制度在我国的地位。",
            "写出全国人民代表大会、国务院、地方各级人民政府、人民法院、人民检察院各自的职权，各写一句话。",
            "写出「一府一委两院」指的是哪几个机关，以及它们和本级人民代表大会是什么关系。",
        ],
        [
            "观察自己家附近或学校附近挂着机构牌子的地方，记下两个机构的全称，判断它们属于哪一类，并说一说你是怎么判断的。",
            "把「人民检察院依法提起公诉、人民法院依法审理」这个顺序，用一句话讲给同桌听，再各举一个该找它们的例子。",
        ],
        [
            "从社区和校园里找一个你真正关心的问题，写一份建议：说清楚这件事该找哪一类国家机构、为什么找它、你打算用什么方式把建议送出去，做完在班里交流一遍。",
            "回家采访一位家里人：问问他遇到过需要找国家机构办的事是什么、当时是怎么找到对应机构的，把他的话记下来，再说说你的想法。",
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
    "title": "我们的国家机构",
    "name_en": "Our State Institutions",
    "grade": 6,
    "grade_cn": "六年级",
    "domain": "national-situation",
    "domain_cn": "国情与公民意识",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学六年级的道德与法治课，正对统编六上第 3 单元「我们的国家机构」（国家机构有哪些、人大代表为人民、权力受到制约和监督），落到三件事上。第一件是国家机构有哪些：国家机构是国家机关的统称，我国的国家机构包括中央国家机构和地方国家机构；人民代表大会制度是我国的根本政治制度；全国人民代表大会是最高国家权力机关，全国人民代表大会和地方各级人民代表大会都由民主选举产生，对人民负责，受人民监督；国家行政机关、监察机关、审判机关、检察机关都由人民代表大会产生，对它负责，受它监督——这就是常说的「一府一委两院」与人民代表大会的关系。第二件是各自的职权分工：全国人民代表大会和全国人民代表大会常务委员会行使国家立法权；国务院即中央人民政府，是最高国家权力机关的执行机关，是最高国家行政机关；地方各级人民政府是地方各级国家行政机关；人民法院是国家的审判机关，依法行使审判权；人民检察院是国家的法律监督机关，依法行使检察权；监察委员会是行使国家监察职能的专责机关。第三件是人大代表为人民与权力受到制约和监督：全国人民代表大会和地方各级人民代表大会的代表，代表人民的利益和意志，依法参加行使国家权力，密切联系群众，听取和反映群众的意见和要求；一切国家机关和国家工作人员都必须依靠人民的支持，经常保持同人民的密切联系，倾听人民的意见和建议，接受人民的监督，努力为人民服务。三个互动台子都能真操作，反馈一律写成「这样可能会……，还可以试试……」：动手一是本课核心模拟「事情该找哪个机构」对照台（六个情境 × 选出对应机构 + 说出理由）、动手二是「机构名片与职权配对台」（五张机构名片与五张职权卡配对），综合任务是「我的建议送出去」行动台（问题 → 主管机构 → 表达方式，合成一张办事路线卡）。全课表述从严：机构名称一律用规范全称，绝不使用简称充当正式名称；不出现任何法律条文编号，不臆造案例细节与办理流程；情境只写到校园、家庭、社区的公共事务层面，不写结果、不写人名地名；插图一律为中性简洁扁平教学插画，不绘制国徽、法院徽章、国旗等图形，机构一律用抽象剪影与地标性建筑抽象轮廓表示，不使用真人照片风格。",
    "tags": ["我们的国家机构", "国家机构有哪些", "全国人民代表大会", "国务院", "人民法院", "人民检察院", "一府一委两院", "职权分工", "六年级", "政治认同"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学「国情与公民意识」——了解宪法是国家的根本法，知道公民的基本权利和义务，树立法治观念；对应统编《道德与法治》六年级上册 第3单元「我们的国家机构」：国家机构有哪些、人大代表为人民、权力受到制约和监督。",
    "hero_question": "遇到一件事，该找哪一类国家机构？",
    "hero_alt": "我们的国家机构知识结构图：三栏分别为国家机构有哪些、各自的职权分工、权力受到人民监督，用抽象柱廊建筑剪影、天平、齿轮、卷宗等符号表示，附中文标注，不含国徽国旗与徽章",
    "hero_caption": "我们的国家机构：国家机构是国家机关的统称 · 人民代表大会制度是我国的根本政治制度 · 一府一委两院由人民代表大会产生，对它负责，受它监督",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "国家机构到底有哪些？", "d": "全国人民代表大会、国务院、人民法院……它们是什么关系", "v": "国家机构到底有哪些"},
        {"t": "人民代表是怎么产生的、他们为谁说话？", "d": "为什么说人大代表为人民", "v": "人民代表是怎么产生的他们为谁说话"},
        {"t": "不同的机构分别管什么事？", "d": "立法、行政、审判、检察是怎么分工的", "v": "不同的机构分别管什么事"},
        {"t": "权力这么大，谁来监督？", "d": "为什么说国家机构要接受人民的监督", "v": "权力这么大谁来监督"},
    ],
    "objectives": [
        "能说出国家机构是国家机关的统称，能说出人民代表大会制度是我国的根本政治制度，知道全国人民代表大会是最高国家权力机关",
        "能说出全国人民代表大会、国务院、地方各级人民政府、人民法院、人民检察院各自的职权，能说出立法、行政、审判、检察这几种分工",
        "能说出「一府一委两院」由本级人民代表大会产生，对它负责，受它监督，能说出人民代表大会代表代表人民的利益和意志",
        "能对一个身边的事情做出判断，说出它大概该找哪一类国家机构，并说出理由",
    ],
    "objectives_plain": [
        "能说出国家机构是什么的统称，知道人民代表大会制度是我国的根本政治制度",
        "能说出几个主要国家机构的规范名称和各自的职权",
        "能说出「一府一委两院」与本级人民代表大会的关系",
        "能判断一件身边的事该找哪一类国家机构，并说出理由",
    ],
    "standards": [
        {"content": "了解宪法是国家的根本法，知道公民的基本权利和义务，树立法治观念。",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学 国情与公民意识"},
        {"content": "国家机构有哪些；人大代表为人民；权力受到制约和监督",
         "source": "统编《道德与法治》六年级上册 第3单元「我们的国家机构」"},
    ],
    "prereqs": ["pol-e-g6-u2"],
    "prereqs_name": "我们是公民",
    "prereqs_meta": "pol-e-g6-u2",
    "leads_to": ["pol-e-g6-u4"],
    "next_meta": "pol-e-g6-u4",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "三件事：国家机构有哪些、各自管什么、权力受谁监督。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能对一件身边的事说出该找哪一类机构。",
        "objectives": "看清四件事：国家机构是什么、主要机构各管什么、一府一委两院的关系、怎么判断该找谁。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "记住三句：全国人民代表大会是最高国家权力机关；人民代表大会由民主选举产生，对人民负责，受人民监督；一府一委两院由人民代表大会产生，对它负责，受它监督。",
        "lab-1": "先问两句：这是「定规矩」还是「办事」？这件事有多大范围？",
        "module-2": "口诀：人大定、国务院办、法院审、检察院察、监委督。注意「一府」和「两院」性质不同。",
        "lab-2": "先读职权卡上的关键词：权力机关、行政机关、审判、法律监督。",
        "worked-example": "五条说明：三条正确、两条必须改。留意「国务院就是人民法院」和「小事报到国务院」。",
        "conceptest-1": "三句话里各藏着一个容易想歪的地方，选完把解释读一遍。",
        "synthesis": "三步做路线卡：问题 → 主管机构 → 表达方式。",
        "posttest": "出现了征求意见的公告、跨省高铁和班里的建议箱，看看今天的判断还用不用得上。",
        "summary": "四句话：有哪些、管什么、什么关系、谁监督。",
        "homework": "三层小任务，先做前两层；第二层要走到家门口去看机构的全称。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学道德与法治「国情与公民意识」板块在六年级的一课，正对统编六上第 3 单元「我们的国家机构」（国家机构有哪些、人大代表为人民、权力受到制约和监督）。六年级学生天天路过挂国徽的机关大门、天天听说法律，但对「国家机构」这一整套制度几乎只有零散印象，容易出现三类典型偏差：误认为这些机关离自己很远、和自己没关系；把全国人民代表大会与国务院、人民法院与人民检察院混着说；遇到事情不知道该找哪一类机关，凭感觉乱猜。所以全课不做机构名称的机械背诵，而把内容落到「名称—职权—关系—怎么用」这条链上。第一层是「有哪些」：说明国家机构是国家机关的统称，我国的国家机构包括中央国家机构和地方国家机构；人民代表大会制度是我国的根本政治制度；全国人民代表大会是最高国家权力机关，全国人民代表大会和地方各级人民代表大会都由民主选举产生，对人民负责，受人民监督；国家行政机关、监察机关、审判机关、检察机关都由人民代表大会产生，对它负责，受它监督，并用「一府一委两院」这个常听到的说法把这层关系固定下来。第二层是「管什么」：把立法、行政、审判、检察、监察五种职权与对应机关一一对上，并特别强调「一府」与「两院」性质不同、人民法院「审」与人民检察院「察」分工不同。第三层是「谁监督」：人民代表大会代表代表人民的利益和意志，依法参加行使国家权力，密切联系群众，听取和反映群众的意见和要求；一切国家机关和国家工作人员都必须依靠人民的支持，倾听人民的意见和建议，接受人民的监督，努力为人民服务。三个互动台子都能真操作，反馈一律写成「这样可能会……，还可以试试……」：动手一是本课核心模拟「事情该找哪个机构」对照台——六个情境（立法、跨省工程、身边路灯、依法审理、依法提起公诉、反映建议），每个情境给出四个机构选项，选对给理由、选错给错因与下一步提示；动手二是「机构名片与职权配对台」——五张机构名片与五张职权卡配对，配错时提示该机构职权表述的关键词；综合任务是「我的建议送出去」行动台——学生按「问题 → 主管机构 → 表达方式」各选一步，由系统合成一张可以照着去做的办事路线卡。全课在表述上从严把关：机构名称一律用规范全称，绝不使用简称充当正式名称；不出现任何法律条文编号，不臆造案例细节与办理流程；情境只写到校园、家庭、社区的公共事务层面，不写结果、不写人名地名；插图一律为中性简洁扁平教学插画，不绘制国徽、法院徽章、国旗等图形，机构一律用抽象剪影与地标性建筑抽象轮廓表示，不使用真人照片风格。",
    "plan_table": """| 1 | cover | 我们的国家机构 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：国家机构，你听说过哪几个？ | 起·前测（暴露名称混淆） |
| 5 | concept | 国家机构有哪些：一套制度，一串机构 | 承·概念一（统称、根本政治制度、一府一委两院） |
| 6 | interactive | ★动手一：事情该找哪个机构？ | 承·核心模拟（6 情境 × 选机构 + 说理由） |
| 7 | concept | 各自的职权分工：定、办、审、察、督 | 承·概念二（立法/行政/审判/检察/监察） |
| 8 | interactive | ★动手二：机构名片与职权配对台 | 承·核心模拟（5 机构名片 × 5 职权卡） |
| 9 | concept | 例题示范：机构名牌校对，五条说明哪条要改 | 转·重难点突破（一府与两院、层级范围判断） |
| 10 | quiz | 概念测试：三句话，藏着三个容易想歪的地方 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：我的建议送出去 | 合·迁移应用（三步合成办事路线卡） |
| 12 | quiz | 后测：换几个新情境，判断还准不准 | 合·后测 |
| 13 | summary | 小结：有哪些、管什么、谁监督 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：国家机构有哪些 / 各自的职权分工 / 权力受到人民监督 三栏，用抽象柱廊建筑剪影、天平、齿轮、卷宗等符号表示，附中文标注\n- P5 国家机构职权分工抽象示意图（已生成）：四栏标注立法、行政、审判、检察，用抽象建筑剪影与抽象符号表示，并标注「抽象示意图，不按比例」\n- P7 人民代表大会与一府一委两院关系图（已生成）：下方用抽象柱廊建筑剪影表示人民代表大会，上方用四个抽象剪影表示人民政府、监察委员会、人民法院、人民检察院，中间用箭头标注「由它产生、对它负责、受它监督」\n- ★ 全课不绘制国徽、法院徽章、国旗等图形；机构一律用抽象剪影与地标性建筑抽象轮廓表示，不使用真人照片风格\n- ★ 表述口径统一：机构名称一律用规范全称（不写简称当正式名称）；不出现任何法律条文编号；不臆造案例细节与办理流程；情境只写到校园、家庭、社区的公共事务层面\n- 三张图均为中性简洁扁平教学插画，不含可识别的真实人物与真实徽标",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
