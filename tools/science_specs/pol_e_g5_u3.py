# -*- coding: utf-8 -*-
"""小学道德与法治 · 我们的国土 我们的家园（五年级上·第3单元）—— 补齐知识树「国情与公民意识」空缺

学科语气（道德与法治）：从学生每天路过的街道、吃到的米饭、看到的天气预报讲起，情感共鸣 + 价值判断；
结论落在「应该怎么说、为什么这样说」，不做口号式抒情、不背条文。

★ 领土与疆域表述（最高优先级，全课统一口径，任何地方不得含糊）：
  · 台湾是中国不可分割的一部分；台湾省是我国的一个省级行政区。
  · 香港、澳门是中国的特别行政区，一律写作「中国香港」「中国澳门」，绝不表述为独立国家。
  · 钓鱼岛及其附属岛屿是中国固有领土；南海诸岛是中国固有领土。
  · 讲国土只用规范表述：「我国陆地面积约 960 万平方千米」「有 34 个省级行政区」。
  · 全课不出现任何地图图形；地势用抽象分层示意（西高东低三级阶梯），
    凡出现示意处均明确标注「示意图，不按比例，非标准地图」。

内容落点（对应统编五上第 3 单元「我们的国土 我们的家园」）：
  ① 我们神圣的国土：我国位于亚洲东部、太平洋西岸，陆地面积约 960 万平方千米；
     大陆濒临的海域从北到南依次是渤海、黄海、东海、南海；地势西高东低，大致呈三级阶梯分布，
     第一级阶梯是青藏高原，第二级阶梯是内蒙古高原、黄土高原、云贵高原和三大盆地，
     第三级阶梯是三大平原和东南丘陵；因此许多大河自西向东流，海洋暖湿气流也能深入内陆。
     全国分为省、自治区、直辖市和特别行政区，共 34 个省级行政区。
  ② 中华民族一家亲：我国是统一的多民族国家，由 56 个民族组成；各民族大杂居、小聚居、交错居住；
     民族平等、民族团结、各民族共同繁荣；在少数民族聚居的地方实行民族区域自治，
     设有内蒙古、广西、西藏、宁夏、新疆五个自治区——自治区是国家统一领导下的地方行政区域。
  ③ 落到自己身上：把国土知识说准确，就是爱国最实在的一种方式；尊重各民族风俗习惯，
     爱护一草一木，也是守护家园。

三个互动台子都能真操作（反馈一律写成「这样可能会……，还可以试试……」）：
  动手一 = 地域与特征配对台（5 个地域 × 5 张自然风貌/物产卡，配对成功生成「家园拼图」）；
  动手二 = 我国之最知识台（6 条「我国之最」先猜后揭示，逐条给出规范表述）；
  综合任务 = 「我眼中的祖国」名片生成台（选方面 → 选规范表述 → 选说明方式，合成一张名片）。
插图一律中性简洁扁平插画，不使用真人照片风格，不生成任何地图图形。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g5-u3"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "请你闭上眼睛想一秒：你每天走过的那条街，吃的那碗米饭，窗外那片天，都在同一片土地上。这片土地有多大？它东边和西边一样高吗？住在这里的人又有多少种不同的故乡？这节课我们弄清楚三件事。第一，我们的国土有多大、地势是什么样，省级行政区又是怎么划分的。第二，为什么说我们是统一的多民族国家、中华民族一家亲。第三，关于国土和家园，哪些话必须说准确。带着这三个问题，我们开始。",
    "problem-anchor": "开始之前，先选一个你真正想知道的问题。是想知道我国到底有多大，还是想知道地势为什么西高东低；是想知道 34 个省级行政区怎么分，还是想知道 56 个民族怎样共同生活在这片土地上。选好以后，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出我国陆地面积约 960 万平方千米，全国有 34 个省级行政区。第二，能说出我国地势西高东低、大致呈三级阶梯分布，并能举例说明它对河流的影响。第三，能把关于国土的话说准确：台湾是中国不可分割的一部分；香港、澳门是中国的特别行政区，写作中国香港、中国澳门；钓鱼岛及其附属岛屿是中国固有领土，南海诸岛是中国固有领土。第四，能说出我国是统一的多民族国家，56 个民族共同组成中华民族大家庭。",
    "pretest": "先做三道小题，用你现在的想法选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "先说国土有多大。我国位于亚洲东部、太平洋西岸，陆地面积约 960 万平方千米。我国大陆濒临的海洋，从北到南依次是渤海、黄海、东海、南海，这些海域和岛屿同样是我们家园的一部分。再说地势。我国地势西高东低，大致呈三级阶梯分布。第一级阶梯是青藏高原，平均海拔在 4000 米以上，被称为世界屋脊；第二级阶梯是内蒙古高原、黄土高原、云贵高原，以及塔里木盆地、准噶尔盆地、四川盆地，海拔多在 1000 到 2000 米；第三级阶梯是东北平原、华北平原、长江中下游平原和东南丘陵，海拔多在 500 米以下，再向东延伸到大陆架。西高东低的地势带来两个结果：一是许多大河自西向东流，长江、黄河都是这样，把东部的平原和西部的内陆连在一起；二是海洋的暖湿气流可以顺着地势深入内陆，给更远的地方带去雨水。最后说行政区划。全国分为省、自治区、直辖市和特别行政区，目前共 34 个省级行政区，其中包括 23 个省、5 个自治区、4 个直辖市和 2 个特别行政区。这里有两句话必须说准确：台湾是中国不可分割的一部分，台湾省是我国的一个省级行政区；香港、澳门是中国的特别行政区，写作中国香港、中国澳门。另外，钓鱼岛及其附属岛屿是中国固有领土，南海诸岛是中国固有领土。这里有两个最容易想歪的地方。第一个，有的同学误认为我国只有陆地，把海洋丢在一边，可渤海、黄海、东海、南海同样是我们家园的一部分。第二个，有的同学误认为省级行政区只有省，其实自治区、直辖市和特别行政区都是省级行政区。",
    "lab-1": "现在请你玩一次配对。左边是五个地域，右边是五张自然风貌和物产的卡片，顺序被打乱了。先点一个地域，再点你认为对应的那张卡片。配对了，两边会连起来；配错了，我会告诉你这样可能会错在哪里，还可以怎么想。五组都配对成功，你的家园拼图就完整了。",
    "module-2": "再说这片土地上的人。我国是统一的多民族国家，由 56 个民族组成。其中汉族人口最多，其他 55 个民族人口相对较少，习惯上称为少数民族。各民族的分布特点是：大杂居、小聚居、交错居住——不是各住一块、互不来往，而是你中有我、我中有你，很多地方几个民族是同村、同街、同校。我国坚持民族平等、民族团结、各民族共同繁荣。在少数民族聚居的地方实行民族区域自治，全国有五个自治区：内蒙古自治区、广西壮族自治区、西藏自治区、宁夏回族自治区、新疆维吾尔自治区。这里有一句必须说清楚：自治区是中华人民共和国的地方行政区域，是在国家统一领导下实行区域自治，绝不是独立的国家。各民族文化互相交流交融：蒙古族的那达慕、傣族的泼水节、壮族的三月三，各民族的语言、服饰、节庆、饮食，一起汇成了中华文化。尊重各民族的风俗习惯，就是尊重我们共同的家人。这里有两个最容易搞混的地方。第一个，把民族区域自治搞混成独立，这是绝对不行的，自治区和国家统一是一体的。第二个，误认为少数民族就是住在很远的山里、和自己没有关系，可我们班里、楼上楼下，就可能有不同民族的同学和邻居。最后再回到国土：我们的家园是一个不可分割的整体，台湾是中国不可分割的一部分，香港、澳门是中国的特别行政区，钓鱼岛及其附属岛屿、南海诸岛是我国固有领土。把这些话说准确，就是在守护家园。",
    "lab-2": "接下来我们打开我国之最知识台。这里放着六条我国之最，每一条都先请你猜一猜，再揭示答案和理由。猜错了也不扣分，正好知道要重点记哪一条。看的时候留意一句话：这里出现的地名，都要说规范。",
    "worked-example": "我们一起来看一次展板校对。班里要办一期祖国知多少展板，几位同学写了五条说法，请你判断哪一条表述规范、哪一条必须改。第一条，台湾是一个独立的国家。这一条错了，必须改成：台湾是中国不可分割的一部分，台湾省是我国的一个省级行政区。第二条，我国的陆地面积约 960 万平方千米。这一条正确。第三条，香港、澳门是中国的特别行政区，写作中国香港、中国澳门。这一条也正确，写这两个名字的时候，香港、澳门前面都要带上中国。第四条，钓鱼岛及其附属岛屿是中国固有领土，南海诸岛是中国固有领土。这一条正确。第五条，我国有 34 个省级行政区。这一条正确。这里有一个常见错误要提醒：有的同学误认为省级行政区就是省，把自治区、直辖市和特别行政区漏掉了；其实这四类都算省级行政区，加起来一共 34 个。把话说准确，展板才立得住。",
    "conceptest-1": "接下来用三个说法考考你，每个说法里都藏着一个容易想歪的地方。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件任务交给你：为我们的家园做一张名片。下面分三步：先选一个你想介绍的方面，再选一条说得准确的表述，最后选一种说明方式。三步选完，我会把它们拼成一张名片，你可以贴上展板，也可以念给家里人听。",
    "posttest": "最后一轮，换几个新情境来考考你。这次会遇到展板校对、天气预报和同学的作文，看看今天学的说法还用不用得上。",
    "summary": "这节课我们弄清楚三件事。第一，国土有多大：我国陆地面积约 960 万平方千米，大陆濒临的海域从北到南依次是渤海、黄海、东海、南海；地势西高东低，大致呈三级阶梯分布，许多大河自西向东流；全国有 34 个省级行政区。第二，家园里的人：我国是统一的多民族国家，56 个民族共同组成中华民族大家庭，各民族大杂居、小聚居、交错居住；自治区是国家统一领导下的地方行政区域。第三，这些话必须说准确：台湾是中国不可分割的一部分；香港、澳门是中国的特别行政区，写作中国香港、中国澳门；钓鱼岛及其附属岛屿是中国固有领土，南海诸岛是中国固有领土。把话说准确，就是爱国最实在的一种方式。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出我国陆地面积约多少平方千米、全国有多少个省级行政区；再写出我国地势的三个阶梯各自包括哪些主要地形区。第二层能力应用，动手做：找一张中国政区图或者地球仪，数一数你所在的省级行政区属于第几级阶梯，再找一条自西向东流的大河，用三句话说明地势和河流的关系。第三层迁移挑战，选做：为我们的家园做一张名片，写清楚你选的是哪个方面、用了哪条规范表述、用了什么方式说明，做完在班里讲一遍。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 疆域辽阔与西高东低三级阶梯", "lab-1": "动手一 地域与特征配对台",
    "module-2": "概念二 中华民族一家亲", "lab-2": "动手二 我国之最知识台",
    "worked-example": "例题示范 展板上的五条说法", "conceptest-1": "概念测试",
    "synthesis": "综合任务 我眼中的祖国名片生成台", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：地域与特征配对台（5 个地域 × 5 张自然风貌/物产卡） ──
REGIONS = [
    {"k": "r1", "n": "东北平原",
     "what": "我国面积最大的平原，位于地势第三级阶梯。",
     "f": "黑土肥沃，是我国重要的商品粮基地，盛产玉米、大豆和水稻。",
     "why": "黑土肥力高，地势又平坦，适合大面积种粮，所以这里成了我国重要的商品粮基地。",
     "tip": "还可以试试：把「地形平坦」和「土壤肥沃」分开想一想，它们各自带来什么。"},
    {"k": "r2", "n": "长江中下游平原",
     "what": "位于地势第三级阶梯，河湖密布。",
     "f": "水田连片，淡水鱼多，素称「鱼米之乡」。",
     "why": "这里降水多、河湖多，水田和养鱼都合适，所以被称作鱼米之乡。",
     "tip": "还可以试试：想一想「水多」对种田和养鱼分别意味着什么。"},
    {"k": "r3", "n": "内蒙古高原",
     "what": "位于地势第二级阶梯，草原辽阔。",
     "f": "草原一望无际，牛羊成群，是我国重要的牧区，那达慕大会在这里举行。",
     "why": "高原上降水较少，草场广布，适合放牧；那达慕是蒙古族的传统盛会。",
     "tip": "还可以试试：把降水多少和「种粮」还是「放牧」连起来想一想。"},
    {"k": "r4", "n": "青藏高原",
     "what": "位于地势第一级阶梯，是我国地势最高的地方。",
     "f": "平均海拔 4000 米以上，雪山连绵，被称为「世界屋脊」，牦牛和青稞是这里的特色。",
     "why": "海拔越高气温越低，所以这里雪山连绵；牦牛耐寒、青稞耐寒，都是适应高原环境的物产。",
     "tip": "还可以试试：把「海拔高」和「气温低」连起来，再推一推物产会有什么特点。"},
    {"k": "r5", "n": "海南岛",
     "what": "位于我国南部海域，是我国第二大岛。",
     "f": "终年温暖，椰林沙滩，是我国重要的热带作物产区。",
     "why": "海南岛纬度低，热量充足，所以能种椰子、橡胶等热带作物。",
     "tip": "还可以试试：把「纬度低」和「终年温暖」连起来想一想。"},
]

# ── 动手二：我国之最知识台（先猜后揭示） ──
MOST = [
    {"k": "q1", "q": "我国最长的河流是哪一条？",
     "opts": [{"t": "黄河", "ok": False}, {"t": "长江", "ok": True}, {"t": "珠江", "ok": False}],
     "a": "长江",
     "why": "长江长约 6300 千米，是我国最长的河流；黄河是我国第二长河。两条大河都自西向东流，这与我国地势西高东低有关。",
     "mis": "有的同学误认为黄河最长，其实黄河是第二长河；把长度和含沙量搞混，就容易记错。"},
    {"k": "q2", "q": "我国最大的岛屿是哪一座？",
     "opts": [{"t": "海南岛", "ok": False}, {"t": "崇明岛", "ok": False}, {"t": "台湾岛", "ok": True}],
     "a": "台湾岛",
     "why": "台湾岛是我国第一大岛，海南岛是第二大岛。台湾是中国不可分割的一部分，台湾省是我国的一个省级行政区。",
     "mis": "常见错误是把第一大岛和第二大岛搞混；记住台湾岛第一、海南岛第二，同时把台湾的归属说准确。"},
    {"k": "q3", "q": "我国地势最高的高原是哪一个？",
     "opts": [{"t": "青藏高原", "ok": True}, {"t": "黄土高原", "ok": False}, {"t": "云贵高原", "ok": False}],
     "a": "青藏高原",
     "why": "青藏高原是我国地势第一级阶梯，平均海拔在 4000 米以上，被称为「世界屋脊」。黄土高原和云贵高原属于第二级阶梯。",
     "mis": "容易把「最高」和「最大」搞混：青藏高原既高又大，但判断标准不同，题目问的是高。"},
    {"k": "q4", "q": "我国面积最大的盆地是哪一个？",
     "opts": [{"t": "四川盆地", "ok": False}, {"t": "塔里木盆地", "ok": True}, {"t": "准噶尔盆地", "ok": False}],
     "a": "塔里木盆地",
     "why": "塔里木盆地位于新疆，是我国面积最大的盆地；四川盆地素称「紫色盆地」，准噶尔盆地在新疆北部。三个大盆地都属于地势第二级阶梯。",
     "mis": "有的同学误认为四川盆地最大，其实它是最有名的一个，不是最大的一个。"},
    {"k": "q5", "q": "我国面积最大的平原是哪一个？",
     "opts": [{"t": "华北平原", "ok": False}, {"t": "长江中下游平原", "ok": False}, {"t": "东北平原", "ok": True}],
     "a": "东北平原",
     "why": "东北平原是我国面积最大的平原，其次是华北平原，第三是长江中下游平原。三个大平原都在地势第三级阶梯。",
     "mis": "容易把「人口多」误认为「面积大」：华北平原人口稠密，但面积不是最大的。"},
    {"k": "q6", "q": "我国最大的湖泊是哪一个？",
     "opts": [{"t": "青海湖", "ok": True}, {"t": "鄱阳湖", "ok": False}, {"t": "洞庭湖", "ok": False}],
     "a": "青海湖",
     "why": "青海湖是我国最大的湖泊，也是最大的咸水湖；鄱阳湖是我国最大的淡水湖。两个「最大」说的不是一回事。",
     "mis": "常见错误是把「最大的湖泊」和「最大的淡水湖」搞混：青海湖最大，鄱阳湖是最大的淡水湖。"},
]

# ── 综合任务：「我眼中的祖国」名片生成台 ──
NAMECARD = {
    "aspects": [
        {"k": "a1", "n": "疆域辽阔",
         "opts": [
             {"t": "我国陆地面积约 960 万平方千米，有 34 个省级行政区。", "ok": True,
              "why": "这是规范的表述：面积用约数，行政区数量说得清楚。"},
             {"t": "我国陆地面积世界第一，比任何国家都大。", "ok": False,
              "why": "这样说会错。我国陆地面积约 960 万平方千米，居世界前列，但不是第一。这样可能会：把不准确的说法传出去，听起来响亮，一查就站不住。"},
             {"t": "我国只有陆地，海洋不用算进来。", "ok": False,
              "why": "这样说会错。渤海、黄海、东海、南海同样是我们家园的一部分。还可以试试：把海域和岛屿也写进名片。"},
         ]},
        {"k": "a2", "n": "山河壮美",
         "opts": [
             {"t": "我国地势东高西低，河流大多自东向西流。", "ok": False,
              "why": "这是把方向搞反了。我国地势西高东低，许多大河自西向东流。这样可能会：以后读地图、看天气预报都跟着错。"},
             {"t": "我国地势西高东低，大致呈三级阶梯分布，许多大河自西向东流。", "ok": True,
              "why": "这是规范的表述，和地势示意图的意思完全一致。"},
             {"t": "我国的地形只有平原，没有高原和盆地。", "ok": False,
              "why": "这样说会错。我国地形多样：有高原、盆地、平原和丘陵。还可以试试：举出每一种地形各一个例子。"},
         ]},
        {"k": "a3", "n": "物产丰富",
         "opts": [
             {"t": "我国各地的物产都一样，南方北方没什么差别。", "ok": False,
              "why": "这样说会错。各地气候、地形不同，物产各有特色。这样可能会：把丰富多彩的家园写得很单调。"},
             {"t": "海南岛终年寒冷，盛产苹果。", "ok": False,
              "why": "这是把南北搞混了。海南岛终年温暖，是热带作物产区；苹果多产在北方。还可以试试：先想纬度，再想物产。"},
             {"t": "东北平原黑土肥沃，长江中下游平原素称「鱼米之乡」，各地物产各有特色。", "ok": True,
              "why": "这句话既说准了地方，也说准了特点，是很好的名片用语。"},
         ]},
        {"k": "a4", "n": "民族一家亲",
         "opts": [
             {"t": "我国只有一个民族，大家都是同一个民族。", "ok": False,
              "why": "这样说会错。我国是统一的多民族国家，由 56 个民族组成。这样可能会：把身边的同学和邻居都写没了。"},
             {"t": "民族自治区是独立的国家。", "ok": False,
              "why": "这句话绝对不可以说。自治区是中华人民共和国的地方行政区域，是在国家统一领导下实行区域自治。这样可能会：把国家统一这件大事说错了。"},
             {"t": "我国是统一的多民族国家，56 个民族共同组成中华民族大家庭。", "ok": True,
              "why": "这是规范的表述：既说清了数量，也说清了一个大家庭。"},
         ]},
    ],
    "ways": [
        {"t": "列数据：用 960 万平方千米、34 个省级行政区、56 个民族这样的数字说话。", "ok": True,
         "why": "用数字说明，别人一听就知道你说的准不准。"},
        {"t": "只说「很厉害」，不说理由也不举例子。", "ok": False,
         "why": "这样可能会：听的人记不住，也问不出问题。还可以试试：补一个具体例子或者一个数字。"},
        {"t": "把听来的说法直接抄上去，不去核对。", "ok": False,
         "why": "这样可能会：把不准确的说法传出去。还可以试试：先问一句「这句话规范吗」，再落笔。"},
    ],
}

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g5-u3 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 地域与特征配对台：5 个地域 × 5 张风貌物产卡 → 配对成功生成家园拼图
   3) 我国之最知识台：6 条之最先猜后揭示 → 规范表述 + 易错提醒
   4) 「我眼中的祖国」名片生成台：选方面 → 选规范表述 → 选说明方式 → 合成名片
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

  /* ---------- 2. 地域与特征配对台 ---------- */
  var REGIONS = __REGIONS_JSON__;
  var FEATURES = __FEATURES_JSON__;
  var stage1 = document.getElementById('mt-stage');
  if (stage1) {
    var selR = null;
    var matched = {};
    var out1 = document.getElementById('mt-out');
    var left = document.getElementById('mt-left');
    var right = document.getElementById('mt-right');
    var board = document.getElementById('mt-board');
    function regionByKey(k) {
      for (var i = 0; i < REGIONS.length; i++) { if (REGIONS[i].k === k) return REGIONS[i]; }
      return null;
    }
    function render1() {
      left.innerHTML = '';
      REGIONS.forEach(function (R) {
        var b = document.createElement('button');
        b.className = 'choice' + (matched[R.k] ? ' correct' : (selR === R.k ? ' selected' : ''));
        b.style.textAlign = 'left';
        b.innerHTML = '<strong>' + R.n + '</strong><br><span style="color:var(--muted);font-size:14px">' + R.what + '</span>' +
          (matched[R.k] ? '<br><span style="color:var(--accent-deep);font-size:14px">已配对 ✓</span>' : '');
        b.addEventListener('click', function () {
          if (matched[R.k]) return;
          selR = R.k;
          out1.className = 'result warn';
          out1.innerHTML = '<strong>你选了「' + R.n + '」。</strong>现在到右边点一张你认为对应的卡片。';
          render1();
        });
        left.appendChild(b);
      });
      right.innerHTML = '';
      FEATURES.forEach(function (F) {
        var R = regionByKey(F.k);
        var b = document.createElement('button');
        b.className = 'choice' + (matched[F.k] ? ' correct' : '');
        b.style.textAlign = 'left';
        b.innerHTML = F.t + (matched[F.k] ? '<br><span style="color:var(--accent-deep);font-size:14px">配对成功 ✓</span>' : '');
        b.addEventListener('click', function () {
          if (matched[F.k]) return;
          if (!selR) {
            out1.className = 'result warn';
            out1.innerHTML = '先到左边点一个地域，再回到右边点卡片。' +
              '<br><span style="color:var(--muted)">还可以试试：先看地域的「海拔和位置」，再看卡片里的地形和物产。</span>';
            return;
          }
          if (selR === F.k) {
            matched[F.k] = true;
            selR = null;
            out1.className = 'result';
            out1.innerHTML = '<strong>配对成功：' + R.n + ' —— ' + F.t + '</strong>' + R.why;
            var n = Object.keys(matched).length;
            if (n === REGIONS.length) {
              out1.innerHTML += '<br><br><strong>五组都配对了，你的家园拼图完整了。</strong>' +
                '你会发现，每个地域的地形、气候不同，物产和生活方式也就各有特色——这正是我们家园丰富多彩的地方。';
            }
          } else {
            var SR = regionByKey(selR);
            out1.className = 'result warn';
            out1.innerHTML = '<strong>这张卡片对不上「' + SR.n + '」。</strong>' +
              '这样可能会：把一个地方的地形、气候和物产记串了。' + SR.tip;
          }
          render1();
        });
        right.appendChild(b);
      });
      board.textContent = '已经配对 ' + Object.keys(matched).length + ' / ' + REGIONS.length + ' 组';
    }
    render1();
  }

  /* ---------- 3. 我国之最知识台 ---------- */
  var MOST = __MOST_JSON__;
  var stage2 = document.getElementById('mw-stage');
  if (stage2) {
    var curQ = null;
    var done = {};
    var out2 = document.getElementById('mw-out');
    var panel2 = document.getElementById('mw-panel');
    function mostByKey(k) {
      for (var i = 0; i < MOST.length; i++) { if (MOST[i].k === k) return MOST[i]; }
      return null;
    }
    function render2() {
      document.querySelectorAll('[data-mw-item]').forEach(function (b) {
        var k = b.dataset.mwItem;
        b.classList.toggle('selected', k === curQ);
        b.classList.toggle('correct', !!done[k]);
      });
      document.getElementById('mw-score').textContent =
        '已经揭开 ' + Object.keys(done).length + ' / ' + MOST.length + ' 条';
      if (!curQ) { panel2.innerHTML = ''; return; }
      var Q = mostByKey(curQ);
      var html = '<div style="font-weight:700;font-size:14px;margin:14px 0 0">' + Q.q + '</div>';
      html += '<div class="grid" style="margin-top:10px">';
      Q.opts.forEach(function (o, i) {
        var cls = 'choice';
        if (done[Q.k]) { cls += o.ok ? ' correct' : ''; }
        html += '<button class="' + cls + '" data-mw-opt="' + i + '" style="text-align:left">' + o.t + '</button>';
      });
      html += '</div>';
      panel2.innerHTML = html;
      panel2.querySelectorAll('[data-mw-opt]').forEach(function (b) {
        b.addEventListener('click', function () { choose(parseInt(b.dataset.mwOpt, 10)); });
      });
    }
    function choose(i) {
      var Q = mostByKey(curQ);
      var o = Q.opts[i];
      if (!done[Q.k]) { done[Q.k] = true; }
      if (o.ok) {
        out2.className = 'result';
        out2.innerHTML = '<strong>答对了：' + Q.a + '。</strong>' + Q.why;
      } else {
        out2.className = 'result warn';
        out2.innerHTML = '<strong>你选的是「' + o.t + '」，正确答案是「' + Q.a + '」。</strong>' + Q.why +
          '<br><span style="color:var(--muted)"><strong>错因提醒：</strong>' + Q.mis + '</span>';
      }
      render2();
      if (Object.keys(done).length === MOST.length) {
        out2.innerHTML += '<br><br><strong>六条我国之最都揭开了。</strong>' +
          '记住一件事：这些地名和数字，都要说得规范——特别是台湾岛、钓鱼岛及其附属岛屿、南海诸岛，都要按规范表述来说。';
      }
    }
    document.querySelectorAll('[data-mw-item]').forEach(function (b) {
      b.addEventListener('click', function () {
        curQ = b.dataset.mwItem;
        out2.className = 'result warn';
        out2.textContent = '先猜一猜，再点下面三个选项里的一个。';
        render2();
      });
    });
    render2();
  }

  /* ---------- 4. 「我眼中的祖国」名片生成台 ---------- */
  var NAMECARD = __NAMECARD_JSON__;
  var stage3 = document.getElementById('nc-stage');
  if (stage3) {
    var pick = { aspect: null, text: null, way: null };
    var out3 = document.getElementById('nc-out');
    var panel3 = document.getElementById('nc-panel');
    function aspectByKey(k) {
      for (var i = 0; i < NAMECARD.aspects.length; i++) {
        if (NAMECARD.aspects[i].k === k) return NAMECARD.aspects[i];
      }
      return null;
    }
    function render3() {
      var html = '<div style="font-weight:700;font-size:14px;margin-bottom:6px">第一步 · 我想介绍的方面是</div><div class="grid grid-2">';
      NAMECARD.aspects.forEach(function (A) {
        html += '<button class="choice' + (pick.aspect === A.k ? ' selected' : '') +
          '" data-nc-aspect="' + A.k + '" style="text-align:left">' + A.n + '</button>';
      });
      html += '</div>';
      if (pick.aspect) {
        var A = aspectByKey(pick.aspect);
        html += '<div style="font-weight:700;font-size:14px;margin:16px 0 6px">第二步 · 我想用这条表述</div><div class="grid">';
        A.opts.forEach(function (o, i) {
          var cls = 'choice';
          if (pick.text === i) cls += o.ok ? ' correct' : ' wrong';
          html += '<button class="' + cls + '" data-nc-text="' + i + '" style="text-align:left">' + o.t + '</button>';
        });
        html += '</div>';
      }
      html += '<div style="font-weight:700;font-size:14px;margin:16px 0 6px">第三步 · 我想这样说明</div><div class="grid">';
      NAMECARD.ways.forEach(function (w, i) {
        var cls = 'choice';
        if (pick.way === i) cls += w.ok ? ' correct' : ' wrong';
        html += '<button class="' + cls + '" data-nc-way="' + i + '" style="text-align:left">' + w.t + '</button>';
      });
      html += '</div>';
      panel3.innerHTML = html;
      panel3.querySelectorAll('[data-nc-aspect]').forEach(function (b) {
        b.addEventListener('click', function () {
          pick.aspect = b.dataset.ncAspect; pick.text = null; render3();
          out3.className = 'result warn';
          out3.textContent = '方面选好了，再选一条你认为说得准确的表述。';
        });
      });
      panel3.querySelectorAll('[data-nc-text]').forEach(function (b) {
        b.addEventListener('click', function () {
          pick.text = parseInt(b.dataset.ncText, 10);
          var A = aspectByKey(pick.aspect);
          var o = A.opts[pick.text];
          out3.className = 'result' + (o.ok ? '' : ' warn');
          out3.innerHTML = (o.ok ? '<strong>这条表述说得准确。</strong>' : '<strong>这条还需要改动。</strong>') + o.why;
          render3();
        });
      });
      panel3.querySelectorAll('[data-nc-way]').forEach(function (b) {
        b.addEventListener('click', function () {
          pick.way = parseInt(b.dataset.ncWay, 10);
          render3();
          if (pick.aspect === null || pick.text === null) {
            out3.className = 'result warn';
            out3.textContent = '三步还没选完，先把前面的补齐。';
            return;
          }
          var A = aspectByKey(pick.aspect);
          var o = A.opts[pick.text];
          var w = NAMECARD.ways[pick.way];
          var okN = (o.ok ? 1 : 0) + (w.ok ? 1 : 0);
          out3.className = 'result' + (okN === 2 ? '' : ' warn');
          out3.innerHTML = '<strong>你的名片：</strong>我眼中的祖国 · ' + A.n + '<br>' +
            '「' + o.t + '」<br>' + w.t +
            '<br><span style="color:var(--muted)">' + (okN === 2
              ? '表述准确，说明方式也清楚，这张名片可以贴上展板了。念一遍给同桌听，看他还想知道什么。'
              : '还可以再想一想：表述要说得准确，说明要给一个数字或者一个例子。换一个再试一次。') + '</span>';
        });
      });
    }
    render3();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__REGIONS_JSON__', json.dumps(REGIONS, ensure_ascii=False))
             .replace('__FEATURES_JSON__', json.dumps(
                 [{"k": "r5", "t": REGIONS[4]["f"]},
                  {"k": "r2", "t": REGIONS[1]["f"]},
                  {"k": "r4", "t": REGIONS[3]["f"]},
                  {"k": "r1", "t": REGIONS[0]["f"]},
                  {"k": "r3", "t": REGIONS[2]["f"]}], ensure_ascii=False))
             .replace('__MOST_JSON__', json.dumps(MOST, ensure_ascii=False))
             .replace('__NAMECARD_JSON__', json.dumps(NAMECARD, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：我们的家园，你了解多少？", TTS["pretest"], [
        {"q": "我国陆地面积大约是多少？",
         "options": [("约 960 万平方千米", True),
                     ("约 96 万平方千米", False),
                     ("约 9600 万平方千米", False)],
         "explain": "我国陆地面积约 960 万平方千米，是规范表述。"
                    "<strong>错因提醒：</strong>常见错误是数量级记错——数字后面带「万」时，要读一遍再确认。"},
        {"q": "我国地势的整体特点是什么？",
         "options": [("西高东低，大致呈三级阶梯分布", True),
                     ("东高西低，大致呈三级阶梯分布", False),
                     ("东西一样高，没有明显差别", False)],
         "explain": "我国地势西高东低，大致呈三级阶梯分布，所以许多大河自西向东流。"
                    "<strong>错因提醒：</strong>有的同学把方向搞反了——想一想，长江、黄河的水是往哪边流的。"},
        {"q": "关于我们家园的说法，下面哪一句是规范的？",
         "options": [("台湾是中国不可分割的一部分；香港、澳门是中国的特别行政区，写作中国香港、中国澳门", True),
                     ("香港、澳门是两个国家", False),
                     ("台湾是一个独立的国家", False)],
         "explain": "台湾是中国不可分割的一部分，台湾省是我国的一个省级行政区；香港、澳门是中国的特别行政区，"
                    "一律写作中国香港、中国澳门。"
                    "<strong>错因提醒：</strong>这类说法必须说得准确，出现含糊或错误的表述时，要立刻改过来。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "疆域辽阔：约 960 万平方千米，34 个省级行政区", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们每天走过的街、吃到的米饭、看到的天气，都在祖国这片土地上（And）；可要问「我国有多大、家园有哪些不一样」，很多同学只能说出零碎印象，甚至说不准确（But）；所以这节课先把疆域、地势和行政区划弄清楚，把话说规范（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">我国位于亚洲东部、太平洋西岸，<strong>陆地面积约 960 万平方千米</strong>。我国大陆濒临的海洋，从北到南依次是<strong>渤海、黄海、东海、南海</strong>——海域和岛屿，同样是我们家园的一部分。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>第一级阶梯：</strong>青藏高原，平均海拔 4000 米以上，被称为「世界屋脊」。</div></div>
          <div class="step"><span class="n">2</span><div><strong>第二级阶梯：</strong>内蒙古高原、黄土高原、云贵高原，以及塔里木盆地、准噶尔盆地、四川盆地，海拔多在 1000—2000 米。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>第三级阶梯：</strong>东北平原、华北平原、长江中下游平原和东南丘陵，海拔多在 500 米以下，再向东延伸到大陆架。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="我国地势西高东低三级阶梯抽象分层示意图，用三层色块分别标注青藏高原、高原与盆地、平原与丘陵，并标注示意图不按比例非标准地图">
          <figcaption>示意：我国地势西高东低，大致呈三级阶梯分布（示意图，不按比例，非标准地图）· 许多大河因此自西向东流</figcaption>
        </figure>
        <div class="inner-card">
          <p><strong>行政区划：全国分为省、自治区、直辖市和特别行政区，共 34 个省级行政区</strong></p>
          <p style="color:var(--muted)">目前有 23 个省、5 个自治区、4 个直辖市和 2 个特别行政区。这里两句话必须说准确：<strong>台湾是中国不可分割的一部分</strong>，台湾省是我国的一个省级行政区；<strong>香港、澳门是中国的特别行政区</strong>，写作「中国香港」「中国澳门」。此外，钓鱼岛及其附属岛屿是中国固有领土，南海诸岛是中国固有领土。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>我国只有陆地、海洋不算家园，也有的同学<strong>误认为</strong>省级行政区就是「省」一个类型，把自治区、直辖市和特别行政区漏掉了。<strong>这四类都属省级行政区，加起来一共 34 个。</strong></p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "同样一条河，从青藏高原一路向东流到海里——它流向哪里，其实是地势在替它选路。"},
    {"lens": "解释它", "text": "为什么大河大多自西向东流？因为西边高、东边低；水总是从高处往低处走，方向由地势决定。"},
    {"lens": "迁移它", "text": "地势还影响了别的事：东边的城市港口多，西边的太阳能和地热丰富，同一片土地上做的事不一样，原因常常藏在地形里。"},
])}
    ''', tag="概念一"))

    region_btns = "\n".join(
        f'            <button class="choice" data-mt-region="{r["k"]}" style="text-align:left">'
        f'<strong>{r["n"]}</strong><br><span style="color:var(--muted);font-size:14px">{r["what"]}</span></button>'
        for r in REGIONS
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：地域与特征配对台，把家园拼起来", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点左边一个<strong>地域</strong>，再点右边一张 <strong>自然风貌与物产卡</strong>。配对了会连起来，配错了会告诉你错在哪里。</p>
        <div class="lab-panel">
          <div id="mt-stage">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">点击左侧地域，再点右侧卡片进行配对</div>
            <div class="grid grid-2">
              <div id="mt-left"></div>
              <div id="mt-right"></div>
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">家园拼图</span><span class="v" id="mt-board">已经配对 0 / 5 组</span></div>
          </div>
          <p class="result warn" id="mt-out" style="margin-top:12px">先点左边一个地域。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧩</span><div><strong>配完回头看：</strong>东北平原和长江中下游平原都在第三级阶梯，为什么物产不一样？海拔相近，但纬度、降水不同——地形只是其中一个原因。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "中华民族一家亲：56 个民族共同的家园", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">我国是<strong>统一的多民族国家</strong>，由 56 个民族组成。汉族人口最多，其他 55 个民族人口相对较少，习惯上称为少数民族。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>各民族怎样居住</strong></p>
            <p style="color:var(--muted)">大杂居、小聚居、交错居住——你中有我、我中有你，很多地方几个民族同村、同街、同校。</p>
          </div>
          <div class="inner-card">
            <p><strong>我国坚持什么</strong></p>
            <p style="color:var(--muted)">民族平等、民族团结、各民族共同繁荣；在少数民族聚居的地方实行民族区域自治。</p>
          </div>
        </div>
        <div class="inner-card">
          <p><strong>五个自治区</strong></p>
          <p style="color:var(--muted)">内蒙古自治区、广西壮族自治区、西藏自治区、宁夏回族自治区、新疆维吾尔自治区。<strong>自治区是中华人民共和国的地方行政区域，是在国家统一领导下实行区域自治</strong>，绝不是独立的国家。</p>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="中华民族一家亲扁平插画：不同民族服饰的抽象人物剪影手拉手围成一圈，周围是文字、科技、艺术、建筑等文化元素图标，附中文标注">
          <figcaption>概念图：各民族文化互相交流交融，共同汇成中华文化 · 中华民族一家亲</figcaption>
        </figure>
        <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(78,205,196,.45)">
          <p><strong>一句可以随身带的话</strong></p>
          <p style="color:var(--muted)">我们的家园是<strong>一个不可分割的整体</strong>：台湾是中国不可分割的一部分；香港、澳门是中国的特别行政区；钓鱼岛及其附属岛屿、南海诸岛是我国固有领土。把这些话说准确，就是在守护家园。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学把民族区域自治<strong>搞混</strong>成「独立」，这是绝对不行的；也有的同学<strong>误认为</strong>少数民族离自己很远，可我们班里、楼上楼下，就可能有不同民族的同学和邻居。尊重各民族的风俗习惯，就是尊重我们共同的家人。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "同一个教室里，可能有吃不同风味午餐、过不同节日的同学——但大家写的是同一种文字，唱的是同一首国歌。"},
    {"lens": "解释它", "text": "为什么各民族能一起生活得很好？因为坚持民族平等和民族团结，谁也不比谁高、谁也不被落下；自治区在国家统一领导下实行区域自治，是「一起过日子」而不是「各过各的」。"},
    {"lens": "迁移它", "text": "这套想法在班里也一样用得上：差异不是分开的理由，互相尊重、彼此了解，才是一个大家庭的样子。"},
])}
    ''', tag="概念二"))

    most_btns = "\n".join(
        f'            <button class="choice" data-mw-item="{m["k"]}" style="text-align:left">'
        f'<strong>第 {i} 条</strong>：{m["q"]}</button>'
        for i, m in enumerate(MOST, 1)
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：我国之最知识台，先猜一猜", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">点开一条「我国之最」，先在三个选项里猜一个，再看答案和理由。猜错了会告诉你错在哪里。</p>
        <div class="lab-panel">
          <div id="mw-stage">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 挑一条你想先知道的</div>
            <div class="grid">
{most_btns}
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">揭开进度</span><span class="v" id="mw-score">已经揭开 0 / 6 条</span></div>
          </div>
          <p class="result warn" id="mw-out" style="margin-top:12px">先点一条我国之最。</p>
          <div id="mw-panel"></div>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">📌</span><div><strong>记住一句话：</strong>地名和数字都要说得规范。台湾岛是我国第一大岛，台湾是中国不可分割的一部分；钓鱼岛及其附属岛屿、南海诸岛是我国固有领土。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：「祖国知多少」展板上的五条说法", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>班里要办一期「祖国知多少」展板，几位同学写了五条说法。请你当一次校对员，判断哪条规范、哪条必须改。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>说法一（必须改）：</strong>「台湾是一个独立的国家」。<strong>正确表述：台湾是中国不可分割的一部分</strong>，台湾省是我国的一个省级行政区。</div></div>
          <div class="step"><span class="n">2</span><div><strong>说法二（规范）：</strong>我国的陆地面积约 960 万平方千米。</div></div>
          <div class="step"><span class="n">3</span><div><strong>说法三（规范）：</strong>香港、澳门是中国的特别行政区，写作「中国香港」「中国澳门」。<strong>香港、澳门前面都要带上中国。</strong></div></div>
          <div class="step"><span class="n">4</span><div><strong>说法四（规范）：</strong>钓鱼岛及其附属岛屿是中国固有领土，南海诸岛是中国固有领土。</div></div>
          <div class="step"><span class="n green">5</span><div><strong>说法五（规范）：</strong>我国有 34 个省级行政区——包括 23 个省、5 个自治区、4 个直辖市和 2 个特别行政区。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>省级行政区就是「省」，把自治区、直辖市和特别行政区漏掉了；也有同学把香港、澳门当成国家来写。<strong>把话说准确，展板才立得住。</strong></p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "关于我们家园的疆域，下面哪句话说得准确？",
         "options": [("我国陆地面积约 960 万平方千米，全国有 34 个省级行政区", True),
                     ("我国陆地面积不到 100 万平方千米", False),
                     ("我国只有陆地，没有海洋", False)],
         "explain": "我国陆地面积约 960 万平方千米，共有 34 个省级行政区；渤海、黄海、东海、南海同样是我们家园的一部分。"
                    "<strong>错因提醒：</strong>常见错误是把数量级记错，或者<strong>误认为</strong>海洋不算家园——海域和岛屿也是家园的一部分。"},
        {"q": "关于我国地势和河流，下面哪句话说得准确？",
         "options": [("我国地势西高东低，大致呈三级阶梯分布，许多大河自西向东流", True),
                     ("我国地势东高西低，河流大多自东向西流", False),
                     ("地势对河流没有影响", False)],
         "explain": "地势决定水流方向：西高东低，所以长江、黄河都自西向东流。"
                    "<strong>错因提醒：</strong>有的同学把方向<strong>搞混</strong>了，把「西高东低」说成「东高西低」；"
                    "只要想一想水往低处流，就不会搞反。"},
        {"q": "关于我国是统一的多民族国家，下面哪句话说得准确？",
         "options": [("我国由 56 个民族组成，各民族大杂居、小聚居、交错居住；自治区在国家统一领导下实行区域自治", True),
                     ("民族自治区是独立的国家", False),
                     ("我国只有一个民族", False)],
         "explain": "我国是统一的多民族国家，56 个民族共同组成中华民族大家庭；自治区是中华人民共和国的地方行政区域。"
                    "<strong>错因提醒：</strong>把民族区域自治<strong>误认为</strong>「独立」是绝不能出现的错误说法。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：「我眼中的祖国」名片生成台", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">三步各选一个：<strong>我想介绍的方面 → 我想用这条表述 → 我想这样说明</strong>。选完，你就设计出了一张可以贴上展板的名片。</p>
        <div class="lab-panel">
          <div id="nc-stage"></div>
          <div id="nc-panel"></div>
          <p class="result warn" id="nc-out" style="margin-top:12px">从第一步开始选。</p>
        </div>
        <div class="inner-card" style="margin-top:14px">
          <p><strong>把它写下来：</strong></p>
          <p style="color:var(--muted)">如果让你给外地的朋友介绍自己的家乡，你最想先说哪一件事？试着写三句话，其中至少有一句要用上数字或地名，并且说得规范。</p>
          <textarea id="syn-answer" rows="3" placeholder="我的家乡在……，这里有……，我想说的是……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，说法还准不准", TTS["posttest"], [
        {"q": "同学写作文时写了「我国有 34 个省级行政区，其中包括台湾省」，这句话：",
         "options": [("说法规范，可以保留", True),
                     ("应该把台湾省改成「台湾国」", False),
                     ("台湾省不属于省级行政区", False)],
         "explain": "台湾是中国不可分割的一部分，台湾省是我国的一个省级行政区，这句话是规范的。"
                    "<strong>错因提醒：</strong>见到任何含糊或错误的说法，都要立刻改过来，不能含糊过去。"},
        {"q": "天气预报说「一股冷空气从北方南下，影响长江中下游平原」。结合地势想一想，下面哪种说法更合理？",
         "options": [("我国地势西高东低，冷空气可以顺着地势南下、深入内陆", True),
                     ("地势和冷空气没关系，纯属巧合", False),
                     ("我国地势东高西低，所以冷空气进不来", False)],
         "explain": "地势会影响气流和水流：西高东低，海洋暖湿气流可以深入内陆，北方冷空气也容易南下。"
                    "<strong>错因提醒：</strong>容易把地理现象当成互不相关的巧合；其实地形常常是背后那个原因。"},
        {"q": "班里转来一位少数民族的同学，他的家乡过节时会办那达慕。作为同班同学，下面哪种做法更好？",
         "options": [("请他讲讲那达慕是怎么回事，也在班里一起了解各民族的节日", True),
                     ("告诉他到了这里就别提自己家乡的节日了", False),
                     ("觉得他的节日很奇怪，不和他一起玩", False)],
         "explain": "各民族文化交流交融，才汇成中华文化；互相尊重、彼此了解，是一个大家庭该有的样子。"
                    "<strong>错因提醒：</strong>有的同学<strong>误认为</strong>「不一样就不好」——不一样恰恰是我们家园丰富的地方。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：疆域多大、家园是谁的、话怎么说", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>疆域多大：</strong>我国陆地面积约 960 万平方千米；大陆濒临的海域从北到南依次是渤海、黄海、东海、南海。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>地势怎样：</strong>西高东低，大致呈三级阶梯分布；第一级阶梯是青藏高原，第二级是高原和三大盆地，第三级是三大平原和东南丘陵。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>家园是谁的：</strong>我国是统一的多民族国家，56 个民族共同组成中华民族大家庭；自治区在国家统一领导下实行区域自治。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>话怎么说：</strong>台湾是中国不可分割的一部分；香港、澳门是中国的特别行政区，写作「中国香港」「中国澳门」；钓鱼岛及其附属岛屿、南海诸岛是我国固有领土。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>一句口诀：</strong>约九百六十万，三十四个省级区；西高东低三级梯，大河滚滚向东去；五十六族一家亲，领土完整记心里。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「地势」「省级行政区」这两个词，给家里人讲一件我国国土的事，并说说为什么要把话说准确。</p>
          <p style="color:var(--muted)">再动一动手：<strong>写一写</strong>你家乡所在省级行政区的名字和它最大的特点，写清楚名称、位置和一样物产。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写出我国陆地面积约多少平方千米，以及全国有多少个省级行政区。",
            "写出我国地势的三个阶梯，并各举一个主要地形区。",
            "写出大陆濒临的四个海域名称，按从北到南的顺序排列。",
        ],
        [
            "找一张中国政区图或地球仪，看看你所在的省级行政区属于第几级阶梯，再找一条自西向东流的大河，用三句话说明地势与河流的关系。",
            "把本课出现的规范表述抄写一遍：台湾是中国不可分割的一部分；香港、澳门是中国的特别行政区，写作「中国香港」「中国澳门」；钓鱼岛及其附属岛屿、南海诸岛是我国固有领土。",
        ],
        [
            "为我们的家园做一张名片：选一个方面，写清一条规范表述，再用一个数字或一个例子说明，做完在班里讲一遍。",
            "查一查我国某一个自治区的一项特色文化或物产，写三句话介绍它，并说说它为什么让人自豪。",
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
    "title": "我们的国土 我们的家园",
    "name_en": "Our Land, Our Home",
    "grade": 5,
    "grade_cn": "五年级",
    "domain": "national-situation",
    "domain_cn": "国情与公民意识",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学五年级的道德与法治课，正对统编五上第 3 单元「我们的国土 我们的家园」，落到「我们神圣的国土」与「中华民族一家亲」两件事上，并把关于国土的表述说规范、说准确。第一件事是国土与家园：我国位于亚洲东部、太平洋西岸，陆地面积约 960 万平方千米；大陆濒临的海域从北到南依次是渤海、黄海、东海、南海；地势西高东低，大致呈三级阶梯分布——第一级阶梯是青藏高原，第二级阶梯是内蒙古高原、黄土高原、云贵高原和塔里木盆地、准噶尔盆地、四川盆地，第三级阶梯是东北平原、华北平原、长江中下游平原和东南丘陵，因此许多大河自西向东流，海洋暖湿气流也能深入内陆；全国分为省、自治区、直辖市和特别行政区，共 34 个省级行政区（23 个省、5 个自治区、4 个直辖市和 2 个特别行政区）。第二件事是家园里的人：我国是统一的多民族国家，由 56 个民族组成，各民族大杂居、小聚居、交错居住，坚持民族平等、民族团结、各民族共同繁荣，在少数民族聚居的地方实行民族区域自治，设有内蒙古、广西、西藏、宁夏、新疆五个自治区——自治区是中华人民共和国的地方行政区域，绝不是独立的国家。全课把领土与疆域的规范表述作为最高优先级反复落实：台湾是中国不可分割的一部分，台湾省是我国的一个省级行政区；香港、澳门是中国的特别行政区，一律写作「中国香港」「中国澳门」，绝不表述为独立国家；钓鱼岛及其附属岛屿是中国固有领土，南海诸岛是中国固有领土。三个互动台子都能真操作，反馈一律写成「这样可能会……，还可以试试……」：动手一是地域与特征配对台（五个地域与五张自然风貌、物产卡配对，配成一张「家园拼图」）、动手二是我国之最知识台（六条我国之最先猜后揭示，逐条给出规范表述与易错提醒）、综合任务是我眼中的祖国名片生成台（选方面 → 选规范表述 → 选说明方式，合成一张可贴上展板的名片）。全课不出现任何地图图形，地势改用抽象分层示意，并明确标注「示意图，不按比例，非标准地图」；插图一律为中性简洁扁平插画，不使用真人照片风格。",
    "tags": ["我们的国土 我们的家园", "我们神圣的国土", "中华民族一家亲", "960 万平方千米", "34 个省级行政区", "民族团结", "五年级", "国情与公民意识"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学「国情与公民意识」——了解宪法是国家的根本法，知道公民的基本权利和义务，树立法治观念；对应统编《道德与法治》五年级上册 第3单元「我们的国土 我们的家园」：我们神圣的国土、中华民族一家亲。",
    "hero_question": "我们脚下的这片土地有多大，它又把什么样的人聚在一起？",
    "hero_alt": "我们的国土我们的家园知识结构图：疆域辽阔、山河壮美、民族一家亲 三栏，附中文标注，不含地图轮廓",
    "hero_caption": "我们的国土 我们的家园：约 960 万平方千米 · 34 个省级行政区 · 西高东低三级阶梯 · 56 个民族一家亲",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "我们的祖国到底有多大？", "d": "面积、海域和东西南北的差别", "v": "我们的祖国到底有多大"},
        {"t": "地势为什么西高东低？", "d": "三级阶梯是怎么来的、又带来什么", "v": "地势为什么西高东低"},
        {"t": "34 个省级行政区怎么分？", "d": "省、自治区、直辖市和特别行政区各是什么", "v": "34 个省级行政区怎么分"},
        {"t": "为什么说中华民族一家亲？", "d": "56 个民族怎样共同生活在这片土地上", "v": "为什么说中华民族一家亲"},
    ],
    "objectives": [
        "能说出我国陆地面积约 960 万平方千米，全国有 34 个省级行政区；知道大陆濒临的海域从北到南依次是渤海、黄海、东海、南海",
        "能说出我国地势西高东低、大致呈三级阶梯分布，并能举例说明它对河流的影响",
        "能把关于国土的话说准确：台湾是中国不可分割的一部分；香港、澳门是中国的特别行政区，写作「中国香港」「中国澳门」；钓鱼岛及其附属岛屿是中国固有领土，南海诸岛是中国固有领土",
        "能说出我国是统一的多民族国家，56 个民族共同组成中华民族大家庭，各民族大杂居、小聚居、交错居住",
    ],
    "objectives_plain": [
        "能说出我国陆地面积约多少平方千米、全国有多少个省级行政区",
        "能说出我国地势西高东低、大致呈三级阶梯分布，并举例说明它对河流的影响",
        "能把关于国土的表述说准确、说规范",
        "能说出我国是统一的多民族国家，56 个民族共同组成中华民族大家庭",
    ],
    "standards": [
        {"content": "了解宪法是国家的根本法，知道公民的基本权利和义务，树立法治观念。",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学 国情与公民意识"},
        {"content": "我们神圣的国土；中华民族一家亲",
         "source": "统编《道德与法治》五年级上册 第3单元「我们的国土 我们的家园」"},
    ],
    "prereqs": ["pol-e-g5-u2"],
    "prereqs_name": "我们是班级的主人",
    "prereqs_meta": "pol-e-g5-u2",
    "leads_to": ["pol-e-g5-u4"],
    "next_meta": "pol-e-g5-u4",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "这片土地有多大，它又把什么样的人聚在一起？带着这个问题开始。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能把一件国土的事说得又准又清楚。",
        "objectives": "看清四件事：我国有多大、地势什么样、34 个省级行政区怎么分、56 个民族怎样一家亲。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "约 960 万平方千米；西高东低三级阶梯；34 个省级行政区。地形决定水流方向。",
        "lab-1": "先点地域，再点卡片。配错了会告诉你错在哪里——注意地形、气候和物产是连在一起的。",
        "module-2": "56 个民族一家亲：大杂居、小聚居、交错居住；自治区在国家统一领导下实行区域自治。",
        "lab-2": "六条我国之最先猜后揭示。特别留意台湾岛、钓鱼岛及其附属岛屿、南海诸岛的规范表述。",
        "worked-example": "展板校对的五条说法：一条必须改（台湾的表述），四条规范。",
        "conceptest-1": "三个说法里各藏着一个容易想歪的地方，选完把解释读一遍。",
        "synthesis": "三步合成名片：我想介绍的方面 → 我想用这条表述 → 我想这样说明。",
        "posttest": "出现了作文、天气预报和新同学，看看今天的说法还用不用得上。",
        "summary": "四句话：疆域多大、地势怎样、家园是谁的、话怎么说。",
        "homework": "三层小任务，先做前两层；第二层要动手去查、去看图。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学道德与法治「国情与公民意识」板块在五年级的空缺，正对统编五上第 3 单元「我们的国土 我们的家园」（我们神圣的国土、中华民族一家亲），并把「关于国土与疆域的表述必须规范准确」作为全课的最高优先级。五年级学生对「祖国」有情感，但对「有多大、地势什么样、有多少个省级行政区」往往只有零碎印象；同时，涉及台湾、香港、澳门、钓鱼岛及其附属岛屿、南海诸岛等表述，很容易出现含糊甚至错误，必须在课堂上一次说准、反复落实。所以全课不讲口号，而把内容换成能核对、能复述的规范表述与可操作的活动。第一层是「我们神圣的国土」：先给规范表述——我国位于亚洲东部、太平洋西岸，陆地面积约 960 万平方千米；大陆濒临的海域从北到南依次是渤海、黄海、东海、南海；再把地势拆成三级阶梯（第一级青藏高原、第二级高原与三大盆地、第三级三大平原与东南丘陵），并说明它对河流与气候的影响；最后落到行政区划：全国分为省、自治区、直辖市和特别行政区，共 34 个省级行政区。第二层是「中华民族一家亲」：我国是统一的多民族国家，由 56 个民族组成，各民族大杂居、小聚居、交错居住，坚持民族平等、民族团结、各民族共同繁荣，在少数民族聚居的地方实行民族区域自治；并明确纠正「自治区是独立国家」这类错误说法。第三层是「把话说准确」：台湾是中国不可分割的一部分，台湾省是我国的一个省级行政区；香港、澳门是中国的特别行政区，一律写作「中国香港」「中国澳门」；钓鱼岛及其附属岛屿是中国固有领土，南海诸岛是中国固有领土——这四条在概念页、例题示范、概念测试与后测中反复出现，例题示范直接做成一次「展板校对」。三个互动台子都能真操作，反馈一律写成「这样可能会……，还可以试试……」：动手一是地域与特征配对台，五个地域配五张自然风貌、物产卡，配对成功拼出「家园拼图」，配错则给出错因与下一步提示；动手二是我国之最知识台，六条「我国之最」先猜后揭示，逐条给出规范表述与易错提醒；综合任务是我眼中的祖国名片生成台，学生按「我想介绍的方面 → 我想用这条表述 → 我想这样说明」各选一步，由系统合成一张可贴上展板的名片。全课不出现任何地图图形，地势改用抽象分层示意，凡出现示意处均明确标注「示意图，不按比例，非标准地图」；插图一律为中性简洁扁平插画，不使用真人照片风格。",
    "plan_table": """| 1 | cover | 我们的国土 我们的家园 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：我们的家园，你了解多少？ | 起·前测（暴露已有印象与表述误区） |
| 5 | concept | 疆域辽阔：约 960 万平方千米，34 个省级行政区 | 承·概念一（疆域、三级阶梯、行政区划） |
| 6 | interactive | 动手一：地域与特征配对台，把家园拼起来 | 承·核心模拟（地域 → 自然风貌与物产配对） |
| 7 | concept | 中华民族一家亲：56 个民族共同的家园 | 承·概念二（民族分布与民族区域自治） |
| 8 | interactive | 动手二：我国之最知识台，先猜一猜 | 承·知识台（六条我国之最先猜后揭示） |
| 9 | concept | 例题示范：「祖国知多少」展板上的五条说法 | 转·重难点突破（五条说法校对 + 规范表述） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：「我眼中的祖国」名片生成台 | 合·迁移应用（三步合成名片） |
| 12 | quiz | 后测：换几个新情境，说法还准不准 | 合·后测 |
| 13 | summary | 小结：疆域多大、家园是谁的、话怎么说 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：疆域辽阔 / 山河壮美 / 民族一家亲 三栏，附中文标注，画面不含地图轮廓\n- P5 地势三级阶梯抽象分层示意图（已生成）：三层色块分别标注第一、二、三级阶梯与主要地形区，并标注「示意图，不按比例，非标准地图」\n- P7 中华民族一家亲扁平插画（已生成）：不同民族服饰的抽象人物剪影手拉手，周围是文字、科技、艺术、建筑元素图标\n- ★ 全课不生成任何地图图形；凡涉及疆域均改用文字与抽象示意表达，并明确标注非标准地图\n- 领土表述统一口径：台湾是中国不可分割的一部分；香港、澳门是中国的特别行政区，写作「中国香港」「中国澳门」；钓鱼岛及其附属岛屿、南海诸岛是我国固有领土\n- 三张图均为中性简洁扁平教学插画，不使用真人照片风格，不含可识别的真实人物",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
