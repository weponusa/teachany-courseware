# -*- coding: utf-8 -*-
"""小学道德与法治 · 骄人祖先 灿烂文化（五年级上·第4单元）—— 补齐知识树「中华优秀传统文化」空缺

学科语气（道德与法治）：从学生每天写的字、背的诗、逛的博物馆讲起，情感共鸣 + 价值判断，
讲灿烂文明与民族团结，积极正面；结论落在「为什么值得自豪、今天怎么接着做」，
不做口号式抒情，不堆砌名词，不把文化自信讲成排外。

内容落点（对应统编五上第 4 单元「骄人祖先 灿烂文化」）：
  ① 美丽文字 民族瑰宝：汉字是世界上最古老的文字之一，也是目前世界上仍在使用的最古老的文字；
     甲骨文（商代，刻在龟甲兽骨上）→ 金文（商周，铸在青铜器上）→ 小篆（秦统一文字）→
     隶书（汉代）→ 楷书（魏晋以后通行）；汉字构造以形声字最多；秦统一文字，促进了各地交流；
     书法成为一门艺术，王羲之《兰亭集序》被誉为「天下第一行书」；汉字传到周边国家，
     对那里的文字和文化产生了影响。
  ② 古代科技 耀我中华：四大发明——造纸术（东汉蔡伦改进）、印刷术（北宋毕昇发明活字印刷）、
     指南针（战国已有司南，宋代用于航海）、火药（唐代已有配方，宋代广泛用于军事）；
     都江堰（战国，李冰主持修建，至今仍发挥灌溉作用）、赵州桥（隋代李春设计建造）、
     张衡发明地动仪、祖冲之把圆周率算到小数点后第七位；《九章算术》《本草纲目》《天工开物》；
     文学典籍《诗经》《史记》、唐诗宋词、四大名著；艺术有书法、国画、京剧、曾侯乙编钟、
     敦煌莫高窟彩塑壁画；建筑有万里长城、北京故宫、赵州桥、布达拉宫。
  ③ 传统美德 源远流长：孝敬长辈、诚实守信、勤劳节俭、尊师重道、扶危济困、家国情怀；
     这些美德是中华民族的精神财富，今天依然是我们做人的根本，
     并与社会主义核心价值观相衔接。

三个互动台子都能真操作（反馈一律写成「这样可能会……，还可以试试……」）：
  动手一 = 文化瑰宝分类台（12 张成就卡分入科技发明 / 文学典籍 / 艺术 / 建筑 四栏，含四大发明）；
  动手二 = 文化瑰宝时间轴（5 张成就卡按时间先后排，排对生成一条中华文明时间轴）；
  综合任务 = 「我的文化自豪卡」生成台（选门类 → 选一项成就 → 选一句说明，合成一张自豪卡）。
插图一律中性简洁扁平插画，不使用真人照片风格。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g5-u4"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "你每天写的字，是几千年前就长成这样的；你背的那句「春眠不觉晓」，一千多年前就已经有人这样说了。我们脚下这片土地上，祖先留下的东西比想象中多得多：一套用了几千年的文字，一批改变了世界的技术，还有一句句传下来的做人的道理。这节课我们弄清楚三件事。第一，汉字是怎么走到今天的，为什么说它是民族的瑰宝。第二，我国古代的科技、文学、艺术和建筑成就有哪些，它们凭什么让世界记住。第三，那些传了几千年的传统美德，今天还在不在我们身边。带着这三个问题，我们开始。",
    "problem-anchor": "开始之前，先选一个你真正想知道的问题。是想知道汉字是怎么一路演变过来的，还是想知道四大发明为什么了不起；是想知道我们的诗歌、书画、建筑有多美，还是想知道那些传统美德今天还有什么用。选好以后，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出汉字是世界上最古老的文字之一，也是目前世界上仍在使用的最古老的文字，并能说出甲骨文、金文、小篆、隶书、楷书的大致演变顺序。第二，能说出造纸术、印刷术、指南针和火药是我国古代的四大发明，并各说一句它们的作用。第三，能举例说出我国古代的科技、文学、艺术和建筑成就，学会把它们分门别类。第四，能说出孝敬长辈、诚实守信、勤劳节俭这些传统美德源远流长，今天依然是我们做人的根本。",
    "pretest": "先做三道小题，用你现在的想法选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "先说文字。汉字是世界上最古老的文字之一，也是目前世界上仍在使用的最古老的文字。也就是说，别的古文字大多已经不再使用了，而汉字从几千年前一路写到了今天。它的样子是慢慢变过来的。商代的甲骨文刻在龟甲和兽骨上，笔画细细的、弯弯的，很多字还能看出它所画的东西；商周的金文铸在青铜器上，笔画圆厚；秦始皇统一中国后，把小篆作为通行文字，各地写法归到一处，交流方便了很多；到了汉代，隶书把弯弯的笔画拉直，写起来更快；魏晋以后，楷书通行开来，一笔一画端端正正，一直用到今天。我们平时写的字，大多数是形声字——一部分表示意思，一部分表示读音，这样的字占汉字的绝大多数，所以看到不认识的字，有时候能猜出个大概。字写得好，还成了一门艺术——书法。东晋王羲之的《兰亭集序》被誉为「天下第一行书」；唐代的欧阳询、颜真卿、柳公权，楷书写得各有风骨。写字用的笔、墨、纸、砚，被称为「文房四宝」。汉字还传到了周边国家，对那里的文字和文化产生了影响。这里有两个最容易想歪的地方。第一个，有的同学误认为汉字是别人发明的、后来才传给我们，其实汉字是中华民族在长期的生产生活中一点一点创造出来的。第二个，有的同学误认为汉字从古到今一个样子、从来没变过，可光看甲骨文和楷书的差别就知道，它一直在变，只是变得有迹可循。一句话记住：一种文字能被几千年的人一直接着用，这本身就是一件了不起的事。",
    "lab-1": "现在请你当一次文化馆的分类员。这里放着十二张成就卡，顺序被打乱了。上面有四个分类栏，分别是科技发明、文学典籍、艺术和建筑。请你把每张卡放进它该去的那一栏：放对了卡片会落进框里，放错了我会告诉你这样可能会错在哪里，还可以怎么想。",
    "module-2": "再说说祖先留下的本事和作品。我国古代的科技成就在世界上长期居于前列，最出名的就是四大发明。造纸术，东汉的蔡伦改进了造纸的方法，用树皮、麻头、破布、旧渔网这些便宜材料造纸，纸变得又好用又便宜；印刷术，北宋的毕昇发明了活字印刷，一个字一个印，排版灵活，印书快了很多；指南针，战国时期就已经有了指向的司南，到了宋代，人们把它用在航海上，远洋航行不再只能靠看星星；火药，唐代就已经有了火药的配方，宋代广泛用于军事。这四项技术后来传播到世界各地，推动了世界文明的发展。除了四大发明，还有很多：战国时期李冰主持修建的都江堰，把岷江的水引到成都平原，两千多年过去了，今天仍在发挥灌溉作用；隋代李春设计建造的赵州桥，是世界上现存年代最久远的单孔敞肩石拱桥；东汉张衡发明地动仪，用来观测地震；南北朝时期的祖冲之，把圆周率精确到小数点后第七位，这一成果领先世界近千年。典籍方面，汉代有数学名著《九章算术》，明代有李时珍的《本草纲目》和宋应星的《天工开物》。文学艺术同样灿烂：《诗经》是我国最早的一部诗歌总集；西汉司马迁写的《史记》，是我国第一部纪传体通史；唐诗、宋词、元曲各领风骚，李白、杜甫、苏轼、李清照的名字至今被人念起；《三国演义》《水浒传》《西游记》《红楼梦》被称为四大名著。艺术上，书法、国画、京剧、昆曲各具特色，京剧被称为我国的国粹；战国时期的曾侯乙编钟，至今还能奏出乐音；甘肃的敦煌莫高窟里，保存着大量精美的彩塑和壁画。建筑方面，万里长城是我国古代伟大的军事防御工程；北京故宫是明清两代的皇宫，是世界上现存规模最大、保存最完整的木质结构古建筑群；位于西藏拉萨的布达拉宫，融合了藏汉建筑艺术——这些成就，是各民族共同创造出来的。这里有两个最容易搞混的地方。第一个，有的同学误认为四大发明是近代才出现的，其实它们都产生在古代，而且很早就传到了世界其他地方。第二个，有的同学误认为我国古代只有诗歌、没有科技，一提起古代就是背书，其实我们的祖先在天文、数学、农学、医药、水利上都留下过实打实的成果。",
    "lab-2": "接下来我们排一条时间轴。下面五张卡片是打乱的，请你按事情发生的先后顺序，一张一张点下去：点对了，它就会排进这条中华文明时间轴；点错了，我会告诉你这一步该放在哪里想。五张都排好，你就能一眼看到，我们的文明是一步一步走过来的。",
    "worked-example": "我们一起来看一次文化展的讲解准备。小语要为展板写五条讲解词，请你判断每一条说法是否正确。第一条，传统美德已经过时了，现在用不上。这一条错：孝敬长辈、诚实守信、勤劳节俭、扶危济困，这些美德源远流长，今天依然是我们做人的根本，和社会主义核心价值观也是一致的。第二条，四大发明指的是造纸术、印刷术、指南针和火药。这一条正确。第三条，文化自信就是不听、不看外国的文化。这一条错：文化自信是尊重和传承自己的文化，同时也学习借鉴外来文化的有益成果，这样自己的文化才会越来越有活力。第四条，汉字是世界上最古老的文字之一，也是目前世界上仍在使用的最古老的文字。这一条正确。第五条，这些成就是汉族一个民族创造的。这一条错：中华文化是各民族共同创造的，布达拉宫融合了藏汉建筑艺术，敦煌莫高窟的彩塑壁画里也有各民族交流的痕迹。这里有一个常见错误要提醒：有的同学误认为讲文化就要说「我们最强」，可真正的自豪不用靠贬低别人来衬托——把成就说准、说出它解决了什么问题、说清它今天还在不在用，才最有说服力。",
    "conceptest-1": "接下来用三个说法考考你，每个说法里都藏着一个容易想歪的地方。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件任务交给你：为自己的文化自豪卡做一个设计。下面分三步：先选一个门类，再选一项你最喜欢的成就，最后选一句说明——为什么它值得自豪。三步选完，我会把它们拼成一张自豪卡，你可以贴在自己的书桌上，也可以讲给同学听。",
    "posttest": "最后一轮，换几个新情境来考考你。这次会遇到博物馆参观、外国朋友提问和班级展板，看看今天学的说法还用不用得上。",
    "summary": "这节课我们弄清楚三件事。第一，美丽文字：汉字是世界上最古老的文字之一，也是目前世界上仍在使用的最古老的文字；从甲骨文、金文、小篆、隶书到楷书，一路演变到今天，还长出了书法这门艺术。第二，古代科技：造纸术、印刷术、指南针和火药是我国古代的四大发明，它们传播到世界各地，推动了世界文明的发展；此外还有都江堰、赵州桥、地动仪、圆周率，以及《诗经》《史记》《本草纲目》和唐诗宋词、四大名著、京剧、长城、故宫、布达拉宫——这些成就是各民族共同创造的。第三，传统美德：孝敬长辈、诚实守信、勤劳节俭、扶危济困，源远流长，今天依然是我们做人的根本。祖先留下的东西，不是摆着看的古董，而是还在用的本领和还在守的道理。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出汉字演变的大致顺序；写出四大发明的名称，并各写一句它们的作用。第二层能力应用，动手做：选一项你最喜欢的文化成就，查一查它产生在什么时候、解决了什么问题，把答案整理成三句话，再运用本课学到的分类方法，说说它属于科技发明、文学典籍、艺术还是建筑。第三层迁移挑战，选做：设计一张文化自豪卡，写清楚你选的门类、成就和说明，配一幅自己的小画，在班里讲一遍，再请同学说说听完以后还想知道什么。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 美丽文字 民族瑰宝", "lab-1": "动手一 文化瑰宝分类台",
    "module-2": "概念二 古代科技 耀我中华", "lab-2": "动手二 文化瑰宝时间轴",
    "worked-example": "例题示范 文化展的讲解词", "conceptest-1": "概念测试",
    "synthesis": "综合任务 我的文化自豪卡", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：文化瑰宝分类台（12 张成就卡 → 4 栏） ──
BINS = [
    {"k": "b1", "n": "科技发明",
     "done": "四大发明都在这一栏：造纸术、印刷术、指南针和火药。它们都产生在古代，后来传播到世界各地，推动了世界文明的发展。"},
    {"k": "b2", "n": "文学典籍",
     "done": "这些是先人留下的书与诗。《诗经》是我国最早的一部诗歌总集，《史记》是我国第一部纪传体通史，《本草纲目》是一部药物学巨著。"},
    {"k": "b3", "n": "艺术",
     "done": "这些都是看得见、听得到的艺术。书法、京剧、编钟、石窟彩塑，各有各的美。"},
    {"k": "b4", "n": "建筑",
     "done": "这些都是留在大地上的作品。长城是古代伟大的军事防御工程，故宫是世界上现存规模最大、保存最完整的木质结构古建筑群。"},
]
CARDS = [
    {"k": "c1", "t": "造纸术：东汉蔡伦改进造纸方法，用树皮、麻头、破布等便宜材料造出好用的纸", "b": "b1",
     "why": "造纸术是四大发明之一，属于科技发明。它解决的是「字写在什么上面」这个难题。"},
    {"k": "c2", "t": "印刷术：北宋毕昇发明活字印刷，一个字一个印，印书快了很多", "b": "b1",
     "why": "活字印刷是四大发明之一，属于科技发明。它解决的是「书怎么印得多、印得快」。"},
    {"k": "c3", "t": "指南针：战国时期已有司南，宋代把它用在航海上", "b": "b1",
     "why": "指南针是四大发明之一，属于科技发明。它解决的是「在海上怎么认方向」。"},
    {"k": "c4", "t": "火药：唐代已有火药配方，宋代广泛用于军事", "b": "b1",
     "why": "火药是四大发明之一，属于科技发明。它来自古人的炼丹与配药实践。"},
    {"k": "c5", "t": "《诗经》：我国最早的一部诗歌总集", "b": "b2",
     "why": "《诗经》是一部书，属于文学典籍。它收的是西周到春秋时期的诗歌。"},
    {"k": "c6", "t": "《史记》：西汉司马迁所写，我国第一部纪传体通史", "b": "b2",
     "why": "《史记》是一部史书，属于文学典籍。它记的是从上古到汉武帝时期的历史。"},
    {"k": "c7", "t": "《本草纲目》：明代李时珍编写的药物学巨著", "b": "b2",
     "why": "《本草纲目》是一部书，属于文学典籍。它记录了大量的药物和药方。"},
    {"k": "c8", "t": "唐诗宋词：李白、杜甫、苏轼、李清照留下的名篇", "b": "b2",
     "why": "诗词作品属于文学典籍。同一个门类里，诗和词只是体裁不同。"},
    {"k": "c9", "t": "书法：东晋王羲之《兰亭集序》被誉为「天下第一行书」", "b": "b3",
     "why": "书法是看得见的艺术，属于艺术。它把写字变成了一种美的表达。"},
    {"k": "c10", "t": "京剧：被称为我国的国粹，唱念做打都有讲究", "b": "b3",
     "why": "京剧是表演艺术，属于艺术。它由多种地方戏曲融合发展而来。"},
    {"k": "c11", "t": "曾侯乙编钟：战国时期的乐器，今天仍能奏出乐音", "b": "b3",
     "why": "编钟是乐器，属于艺术。它让我们听见了两千多年前的声音。"},
    {"k": "c12", "t": "敦煌莫高窟：保存着大量精美的彩塑和壁画", "b": "b3",
     "why": "彩塑和壁画是造型艺术，属于艺术。莫高窟里的内容也留下了各民族交流的痕迹。"},
    {"k": "c13", "t": "万里长城：我国古代伟大的军事防御工程", "b": "b4",
     "why": "长城是留在大地上的工程，属于建筑。"},
    {"k": "c14", "t": "北京故宫：明清两代的皇宫，世界上现存规模最大、保存最完整的木质结构古建筑群", "b": "b4",
     "why": "故宫是建筑群，属于建筑。"},
    {"k": "c15", "t": "赵州桥：隋代李春设计建造，世界上现存年代最久远的单孔敞肩石拱桥", "b": "b4",
     "why": "赵州桥是桥梁，属于建筑。"},
    {"k": "c16", "t": "布达拉宫：位于西藏拉萨，融合了藏汉建筑艺术", "b": "b4",
     "why": "布达拉宫是建筑，属于建筑；它也说明中华文化是各民族共同创造的。"},
]
CARDS_ORDER = ["c5", "c1", "c14", "c9", "c3", "c11", "c7", "c15", "c2", "c16", "c8", "c4"]

# ── 动手二：文化瑰宝时间轴（按时间先后排） ──
TIMELINE = [
    {"k": "t1", "n": "甲骨文", "d": "商代，人们把字刻在龟甲和兽骨上，这是我国已知最早的成熟文字。"},
    {"k": "t2", "n": "都江堰", "d": "战国时期，李冰主持修建，把岷江的水引到成都平原，今天仍在发挥灌溉作用。"},
    {"k": "t3", "n": "蔡伦改进造纸术", "d": "东汉时期，蔡伦用树皮、麻头、破布等便宜材料造纸，纸变得好用又便宜。"},
    {"k": "t4", "n": "毕昇发明活字印刷", "d": "北宋时期，毕昇用泥活字排版印书，印书快了很多。"},
    {"k": "t5", "n": "李时珍编写《本草纲目》", "d": "明代，李时珍把药物知识整理成一部巨著，记录了大量的药物和药方。"},
]
TIMELINE_SHUFFLED = ["t4", "t1", "t5", "t2", "t3"]

# ── 综合任务：我的文化自豪卡 ──
PRIDECARD = {
    "cats": [
        {"k": "c1", "n": "美丽文字",
         "opts": [
             {"t": "汉字是世界上最古老的文字之一，也是目前世界上仍在使用的最古老的文字；从甲骨文、小篆、隶书到楷书，一路演变到今天。", "ok": True,
              "why": "这条说法准确，也说清了「活到今天」这件最了不起的事。"},
             {"t": "汉字是外国人发明的，后来才传到我国。", "ok": False,
              "why": "这样说会错。汉字是中华民族在长期的生产生活中一点一点创造出来的。这样可能会：把自己民族的东西说成别人的。"},
             {"t": "汉字从古到今一个样子，从来没变过。", "ok": False,
              "why": "这样说会错。光是甲骨文和楷书的差别就能看出来，汉字一直在变。还可以试试：把演变顺序排一遍再说。"},
         ]},
        {"k": "c2", "n": "古代科技",
         "opts": [
             {"t": "造纸术、印刷术、指南针和火药是我国古代的四大发明，它们传播到世界各地，推动了世界文明的发展。", "ok": True,
              "why": "四大发明说得完整，也说清了它们在世界上的影响。"},
             {"t": "四大发明是近代才出现的。", "ok": False,
              "why": "这样说会错。四大发明都产生在古代，而且很早就传到了世界其他地方。这样可能会：把时间前后说反。"},
             {"t": "我国古代只有诗歌，没有什么科技成就。", "ok": False,
              "why": "这样说会错。除了四大发明，还有都江堰、地动仪、圆周率的成果等。还可以试试：一个门类举一个例子。"},
         ]},
        {"k": "c3", "n": "艺术殿堂",
         "opts": [
             {"t": "东晋王羲之的《兰亭集序》被誉为「天下第一行书」，京剧被称为我国的国粹。", "ok": True,
              "why": "书法和京剧都是我国传统的艺术瑰宝，这条说法准确。"},
             {"t": "京剧是从外国传进来的。", "ok": False,
              "why": "这样说会错。京剧是我国传统戏曲，由多种地方戏曲融合发展而来。这样可能会：把自家的东西认成别人的。"},
             {"t": "书法就是把字写得快一点，不算艺术。", "ok": False,
              "why": "这样说会错。书法讲究笔画的轻重、结构和气韵，是一门艺术。还可以试试：仔细看一幅字帖，说说哪里好看。"},
         ]},
        {"k": "c4", "n": "建筑与工程",
         "opts": [
             {"t": "赵州桥是隋代李春设计建造的，是世界上现存年代最久远的单孔敞肩石拱桥；都江堰修建于战国时期，今天仍在发挥灌溉作用。", "ok": True,
              "why": "两条都说得准确，而且都指出了「今天还在用」这一点。"},
             {"t": "万里长城是最近才修建的。", "ok": False,
              "why": "这样说会错。长城是我国古代伟大的军事防御工程。这样可能会：把古代和现代搅在一起。"},
             {"t": "这些成就是汉族一个民族创造的。", "ok": False,
              "why": "这样说会错。中华文化是各民族共同创造的，布达拉宫就融合了藏汉建筑艺术。还可以试试：举一个各民族文化交融的例子。"},
         ]},
        {"k": "c5", "n": "传统美德",
         "opts": [
             {"t": "孝敬长辈、诚实守信、勤劳节俭、扶危济困，这些传统美德源远流长，今天依然是我们做人的根本。", "ok": True,
              "why": "传统美德是传下来的精神财富，今天仍然管用——这条说法准确。"},
             {"t": "传统美德已经过时了，现在用不上。", "ok": False,
              "why": "这样说会错。这些美德和今天提倡的价值观是一致的。这样可能会：把老道理当成老古董。"},
             {"t": "文化自信就是不听、不看外国的文化。", "ok": False,
              "why": "这样说会错。文化自信是尊重和传承自己的文化，同时也学习借鉴外来文化的有益成果。还可以试试：说一说自己的文化里哪些地方可以吸收别人的长处。"},
         ]},
    ],
    "reasons": [
        {"t": "因为它一直用到了今天：都江堰还在灌溉，汉字还在写，诗句还在念。", "ok": True,
         "why": "「今天还在用」是最有说服力的理由，说明它不是摆着看的古董。"},
        {"t": "因为它解决了实实在在的问题，还传到了世界各地，推动了世界文明的发展。", "ok": True,
         "why": "说出它解决了什么问题、影响了谁，自豪就站得住。"},
        {"t": "因为外国人做不到。", "ok": False,
         "why": "这样可能会：把自豪说成比谁强谁弱。还可以试试：把话改成「它解决了什么问题、今天还在不在用」。"},
        {"t": "因为它是古董，越老越值钱。", "ok": False,
         "why": "这样可能会：把文化说成了价钱。还可以试试：从它今天还在用这一点说起。"},
    ],
}

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g5-u4 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 文化瑰宝分类台：12 张成就卡 → 科技发明 / 文学典籍 / 艺术 / 建筑 四栏
   3) 文化瑰宝时间轴：5 张成就卡按时间先后点出 → 生成中华文明时间轴
   4) 我的文化自豪卡：选门类 → 选成就 → 选说明 → 合成一张自豪卡
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

  /* ---------- 2. 文化瑰宝分类台 ---------- */
  var BINS = __BINS_JSON__;
  var CARDS = __CARDS_JSON__;
  var shop = __ORDER_JSON__;
  var stage1 = document.getElementById('ct-stage');
  if (stage1) {
    var placed = {};
    var out1 = document.getElementById('ct-out');
    var bank = document.getElementById('ct-bank');
    var binsEl = document.getElementById('ct-bins');
    function cardByKey(k) {
      for (var i = 0; i < CARDS.length; i++) { if (CARDS[i].k === k) return CARDS[i]; }
      return null;
    }
    function binByKey(k) {
      for (var i = 0; i < BINS.length; i++) { if (BINS[i].k === k) return BINS[i]; }
      return null;
    }
    function render1() {
      bank.innerHTML = '';
      shop.forEach(function (k) {
        if (placed[k]) return;
        var C = cardByKey(k);
        var b = document.createElement('button');
        b.className = 'choice';
        b.style.textAlign = 'left';
        b.textContent = C.t;
        b.addEventListener('click', function () {
          window.__ctPick = k;
          render1();
          out1.className = 'result warn';
          out1.innerHTML = '<strong>你拿起了这张卡：' + C.t + '</strong><br>现在点它该去的分类栏。';
        });
        if (window.__ctPick === k) b.classList.add('selected');
        bank.appendChild(b);
      });
      if (!bank.children.length) {
        bank.innerHTML = '<span style="color:var(--muted);font-size:14px">卡片都分类完了。</span>';
      }
      binsEl.innerHTML = '';
      BINS.forEach(function (B) {
        var d = document.createElement('div');
        d.className = 'sort-bin';
        var inner = '<h4>' + B.n + '</h4>';
        CARDS.forEach(function (C) {
          if (placed[C.k] === B.k) {
            inner += '<span class="tag">' + C.t.split('：')[0] + '</span>';
          }
        });
        d.innerHTML = inner;
        d.addEventListener('click', function () {
          if (!window.__ctPick) {
            out1.className = 'result warn';
            out1.innerHTML = '先在左边点一张成就卡，再点分类栏。' +
              '<br><span style="color:var(--muted)">还可以试试：先看这张卡是「一样技术」「一本书」「一件艺术品」，还是「一座建筑」。</span>';
            return;
          }
          var C = cardByKey(window.__ctPick);
          if (C.b === B.k) {
            placed[C.k] = B.k;
            window.__ctPick = null;
            out1.className = 'result';
            out1.innerHTML = '<strong>放对了：' + C.t + ' → ' + B.n + '</strong>' + C.why;
            var n = Object.keys(placed).length;
            if (n === CARDS.length) {
              var all = BINS.map(function (X) { return X.n + '：' + X.done; }).join('<br>');
              out1.innerHTML += '<br><br><strong>十二张卡片都归位了，这就是中华文化的一角。</strong><br>' + all;
            }
          } else {
            out1.className = 'result warn';
            out1.innerHTML = '<strong>放错了：「' + C.t.split('：')[0] + '」不属于「' + B.n + '」。</strong>' +
              '这样可能会：把「技术」「典籍」「艺术」「建筑」搞混。' +
              '<br><span style="color:var(--muted)">还可以试试：问自己一句——它是一样能用的技术，一本读的书，一件欣赏的作品，还是一座立在地上的建筑？</span>';
          }
          render1();
        });
        binsEl.appendChild(d);
      });
      var n2 = Object.keys(placed).length;
      document.getElementById('ct-score').textContent = '已经归位 ' + n2 + ' / ' + CARDS.length + ' 张';
    }
    render1();
  }

  /* ---------- 3. 文化瑰宝时间轴 ---------- */
  var TIMELINE = __TIMELINE_JSON__;
  var stage2 = document.getElementById('tl-stage');
  if (stage2) {
    var done = [];
    var out2 = document.getElementById('tl-out');
    var axis = document.getElementById('tl-axis');
    function stepByKey(k) {
      for (var i = 0; i < TIMELINE.length; i++) { if (TIMELINE[i].k === k) return TIMELINE[i]; }
      return null;
    }
    function render2() {
      document.querySelectorAll('[data-tl-step]').forEach(function (b) {
        var k = b.dataset.tlStep;
        b.classList.toggle('done', done.indexOf(k) >= 0);
        b.disabled = done.indexOf(k) >= 0;
      });
      document.getElementById('tl-score').textContent = '已经排好 ' + done.length + ' / ' + TIMELINE.length + ' 步';
      axis.innerHTML = '';
      if (!done.length) {
        axis.innerHTML = '<span style="color:var(--muted);font-size:14px">时间轴还是空的。</span>';
        return;
      }
      done.forEach(function (k, i) {
        var T = stepByKey(k);
        var d = document.createElement('div');
        d.className = 'tag';
        d.textContent = (i + 1) + '. ' + T.n;
        axis.appendChild(d);
      });
    }
    document.querySelectorAll('[data-tl-step]').forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.dataset.tlStep;
        var want = TIMELINE[done.length].k;
        if (k === want) {
          done.push(k);
          var T = stepByKey(k);
          out2.className = 'result';
          out2.innerHTML = '<strong>排对了：第' + done.length + '步是「' + T.n + '」。</strong>' + T.d;
          render2();
          if (done.length === TIMELINE.length) {
            out2.className = 'result';
            out2.innerHTML = '<strong>时间轴排好了。</strong>' +
              '从商代的甲骨文，到战国的都江堰、东汉的造纸术、北宋的活字印刷，再到明代的《本草纲目》——' +
              '你会看到，我们的文明不是一天建成的，而是一代一代人接着往前走的。' +
              '<br><span style="color:var(--muted)">想一想：这条时间轴还没有结束，今天的人也在往上写字。</span>';
          }
        } else {
          var T2 = stepByKey(k);
          out2.className = 'result warn';
          out2.innerHTML = '<strong>这一步现在还不到时候。</strong>「' + T2.n + '」说的是：' + T2.d +
            '<br><span style="color:var(--muted)">这样可能会：把先后顺序排反，看起来就像技艺「倒着长」。' +
            '还可以试试：先找那张时间最早的卡片——它是最容易被认出来的一张。</span>';
        }
      });
    });
    render2();
  }

  /* ---------- 4. 我的文化自豪卡 ---------- */
  var PRIDECARD = __PRIDECARD_JSON__;
  var stage3 = document.getElementById('pc-stage');
  if (stage3) {
    var pick = { cat: null, item: null, reason: null };
    var out3 = document.getElementById('pc-out');
    var panel3 = document.getElementById('pc-panel');
    function catByKey(k) {
      for (var i = 0; i < PRIDECARD.cats.length; i++) {
        if (PRIDECARD.cats[i].k === k) return PRIDECARD.cats[i];
      }
      return null;
    }
    function render3() {
      var html = '<div style="font-weight:700;font-size:14px;margin-bottom:6px">第一步 · 我想介绍的门类</div><div class="grid grid-2">';
      PRIDECARD.cats.forEach(function (C) {
        html += '<button class="choice' + (pick.cat === C.k ? ' selected' : '') +
          '" data-pc-cat="' + C.k + '" style="text-align:left">' + C.n + '</button>';
      });
      html += '</div>';
      if (pick.cat) {
        var C = catByKey(pick.cat);
        html += '<div style="font-weight:700;font-size:14px;margin:16px 0 6px">第二步 · 我想介绍的成就是</div><div class="grid">';
        C.opts.forEach(function (o, i) {
          var cls = 'choice';
          if (pick.item === i) cls += o.ok ? ' correct' : ' wrong';
          html += '<button class="' + cls + '" data-pc-item="' + i + '" style="text-align:left">' + o.t + '</button>';
        });
        html += '</div>';
      }
      html += '<div style="font-weight:700;font-size:14px;margin:16px 0 6px">第三步 · 我为什么为它自豪</div><div class="grid">';
      PRIDECARD.reasons.forEach(function (w, i) {
        var cls = 'choice';
        if (pick.reason === i) cls += w.ok ? ' correct' : ' wrong';
        html += '<button class="' + cls + '" data-pc-reason="' + i + '" style="text-align:left">' + w.t + '</button>';
      });
      html += '</div>';
      panel3.innerHTML = html;
      panel3.querySelectorAll('[data-pc-cat]').forEach(function (b) {
        b.addEventListener('click', function () {
          pick.cat = b.dataset.pcCat; pick.item = null; render3();
          out3.className = 'result warn';
          out3.textContent = '门类选好了，再选一项你觉得说得准确的成就介绍。';
        });
      });
      panel3.querySelectorAll('[data-pc-item]').forEach(function (b) {
        b.addEventListener('click', function () {
          pick.item = parseInt(b.dataset.pcItem, 10);
          var C = catByKey(pick.cat);
          var o = C.opts[pick.item];
          out3.className = 'result' + (o.ok ? '' : ' warn');
          out3.innerHTML = (o.ok ? '<strong>这条介绍说得准确。</strong>' : '<strong>这条介绍还需要改动。</strong>') + o.why;
          render3();
        });
      });
      panel3.querySelectorAll('[data-pc-reason]').forEach(function (b) {
        b.addEventListener('click', function () {
          pick.reason = parseInt(b.dataset.pcReason, 10);
          render3();
          if (pick.cat === null || pick.item === null) {
            out3.className = 'result warn';
            out3.textContent = '三步还没选完，先把前面的补齐。';
            return;
          }
          var C = catByKey(pick.cat);
          var o = C.opts[pick.item];
          var w = PRIDECARD.reasons[pick.reason];
          var okN = (o.ok ? 1 : 0) + (w.ok ? 1 : 0);
          out3.className = 'result' + (okN === 2 ? '' : ' warn');
          out3.innerHTML = '<strong>你的文化自豪卡 · ' + C.n + '</strong><br>' +
            '「' + o.t + '」<br>我为它自豪，' + w.t +
            '<br><span style="color:var(--muted)">' + (okN === 2
              ? '介绍准确，理由也站得住。把这张卡念给同学听，看看他还想追问什么，那往往就是可以继续探索的地方。'
              : '还可以再想一想：介绍要说得准确，理由要给一个事实——它解决了什么问题，或者今天还在不在用。换一个再试一次。') + '</span>';
        });
      });
    }
    render3();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__BINS_JSON__', json.dumps(BINS, ensure_ascii=False))
             .replace('__CARDS_JSON__', json.dumps(CARDS, ensure_ascii=False))
             .replace('__ORDER_JSON__', json.dumps(CARDS_ORDER, ensure_ascii=False))
             .replace('__TIMELINE_JSON__', json.dumps(TIMELINE, ensure_ascii=False))
             .replace('__PRIDECARD_JSON__', json.dumps(PRIDECARD, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：祖先留下的东西，你记得多少？", TTS["pretest"], [
        {"q": "关于汉字，下面哪句话说得准确？",
         "options": [("汉字是世界上最古老的文字之一，也是目前世界上仍在使用的最古老的文字", True),
                     ("汉字是外国人发明的，后来才传到我国", False),
                     ("汉字从古到今一个样子，从来没变过", False)],
         "explain": "汉字是世界上最古老的文字之一，也是目前世界上仍在使用的最古老的文字，从甲骨文一路演变到今天。"
                    "<strong>错因提醒：</strong>常见错误是<strong>误认为</strong>汉字从没变过——"
                    "把甲骨文和楷书放在一起看看，就知道它一直在变。"},
        {"q": "我国古代的四大发明指的是：",
         "options": [("造纸术、印刷术、指南针和火药", True),
                     ("造纸术、印刷术、指南针和瓷器", False),
                     ("丝绸、瓷器、茶叶和火药", False)],
         "explain": "四大发明是造纸术、印刷术、指南针和火药。"
                    "<strong>错因提醒：</strong>容易把我国其他同样有名的物产（丝绸、瓷器、茶叶）<strong>和四大发明搞混</strong>；"
                    "四大发明说的是四项技术。"},
        {"q": "关于中华优秀传统文化，下面哪句话说得准确？",
         "options": [("中华文化是各民族共同创造的，各民族文化互相交流交融", True),
                     ("这些成就是汉族一个民族创造的", False),
                     ("传统美德已经过时了，今天用不上", False)],
         "explain": "中华文化是各民族共同创造的：布达拉宫融合了藏汉建筑艺术，敦煌莫高窟的彩塑壁画里也有各民族交流的痕迹。"
                    "<strong>错因提醒：</strong>有的同学<strong>误认为</strong>传统文化就是「老古董」——"
                    "传统美德今天依然是我们做人的根本。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "美丽文字 民族瑰宝：一种一直在用的古老文字", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们每天都在写字、读诗、过节，用的是祖先传下来的语言和文字（And）；可要问「汉字是怎么走到今天的、祖先留下了哪些了不起的东西」，很多同学只能说出零碎的名字（But）；所以这节课把文字的来路、古代成就和传下来的道理理清楚，让自豪有依据（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px"><strong>汉字是世界上古老的文字之一，也是目前世界上仍在使用的最古老的文字。</strong>别的古文字大多已不再使用，汉字却从几千年前一路写到了今天。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>甲骨文：</strong>商代，刻在龟甲和兽骨上，很多字还能看出它所画的东西。</div></div>
          <div class="step"><span class="n">2</span><div><strong>金文与小篆：</strong>商周把字铸在青铜器上；秦统一中国后以小篆通行，各地写法归到一处。</div></div>
          <div class="step"><span class="n">3</span><div><strong>隶书与楷书：</strong>汉代隶书把弯笔拉直、写得更快；魏晋以后楷书通行，一笔一画端端正正，一直用到今天。</div></div>
        </div>
        <div class="inner-card">
          <p><strong>三件值得记一记的事</strong></p>
          <p style="color:var(--muted)">① 我们写的字大多是<strong>形声字</strong>——一部分表意、一部分表音，这类字占汉字的大多数。② 书法成为一门艺术，东晋王羲之的《兰亭集序》被誉为「天下第一行书」，写字用的笔、墨、纸、砚被称为「文房四宝」。③ 汉字传到周边国家，对那里的文字和文化产生了影响。</p>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="中国古代四大发明扁平插画：造纸、印刷、指南针、火药四格图标，每格配中文标签说明">
          <figcaption>概念图：造纸术、印刷术、指南针和火药——我国古代的四大发明，后来传播到世界各地</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>汉字是别人发明的、后来才传给我们，也有的同学<strong>误认为</strong>汉字从古到今一个样子。<strong>汉字是中华民族在生产生活中一点一点创造出来的，而且一直在变——只是变得有迹可循。</strong></p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "同一个「水」字，刻在甲骨上像一条弯曲的河，写在小篆里像一束流动的线，落在楷书里成了方方正正的四笔——三千年，同一条河。"},
    {"lens": "解释它", "text": "为什么汉字能一直用下来？因为它一直在跟着生活变：字变简单了、写起来快了，但表意的根没断。一种文字能被几千人接着用，靠的就是「好用」。"},
    {"lens": "迁移它", "text": "这套眼光也可以用在别处：一样东西能不能传下去，不看它多古老，看它今天还有没有人需要、还有没有人在改进。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：文化瑰宝分类台，十二张卡片各归其位", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先在左边点一张成就卡，再点右侧它该去的分类栏。放对了卡片会落进框里，放错了会告诉你错在哪里。</p>
        <div class="lab-panel">
          <div id="ct-stage">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 打乱的成就卡</div>
            <div class="sort-bank" id="ct-bank"></div>
            <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 四个分类栏（点一下把卡片放进去）</div>
            <div class="sort-bins" id="ct-bins"></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">分类进度</span><span class="v" id="ct-score">已经归位 0 / 12 张</span></div>
          </div>
          <p class="result warn" id="ct-out" style="margin-top:12px">先点左边一张成就卡。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🏛️</span><div><strong>分完想一想：</strong>「科技发明」那一栏里的四张卡，正好就是四大发明。它们和「建筑」「艺术」不一样的地方在哪里？前四项解决的是「怎么造」，后面是把东西「造成什么样」。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "古代科技 耀我中华：从四大发明到诗书建筑", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">我国古代的科技成就在世界上长期居于前列。<strong>造纸术、印刷术、指南针和火药</strong>是我国古代的四大发明，它们后来传播到世界各地，<strong>推动了世界文明的发展</strong>。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>四大发明各解决了什么</strong></p>
            <p style="color:var(--muted)">造纸术（东汉蔡伦改进）解决「字写在哪儿」；印刷术（北宋毕昇发明活字印刷）解决「书怎么印得快」；指南针（战国已有司南，宋代用于航海）解决「海上怎么认方向」；火药（唐代已有配方，宋代广泛用于军事）来自古人的配药实践。</p>
          </div>
          <div class="inner-card">
            <p><strong>不止四大发明</strong></p>
            <p style="color:var(--muted)">战国李冰主持修建的都江堰，今天仍在灌溉；隋代李春设计建造的赵州桥，是世界上现存年代最久远的单孔敞肩石拱桥；东汉张衡发明地动仪；南北朝祖冲之把圆周率精确到小数点后第七位。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="中华优秀传统文化成就四栏分类示意图：科技发明、文学典籍、艺术、建筑，每栏配扁平图标与中文标签">
          <figcaption>概念图：中华优秀传统文化的一角 · 科技发明 / 文学典籍 / 艺术 / 建筑，这些成就是各民族共同创造的</figcaption>
        </figure>
        <div class="inner-card">
          <p><strong>文学、艺术与建筑，同样灿烂</strong></p>
          <p style="color:var(--muted)">《诗经》是我国最早的一部诗歌总集；西汉司马迁的《史记》是我国第一部纪传体通史；唐诗宋词、《三国演义》《水浒传》《西游记》《红楼梦》流传至今。艺术上有书法、国画、京剧（被称为我国的国粹）、曾侯乙编钟，甘肃敦煌莫高窟保存着大量精美彩塑和壁画。建筑上有万里长城、北京故宫（世界上现存规模最大、保存最完整的木质结构古建筑群），以及融合藏汉建筑艺术的布达拉宫。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>四大发明是近代才出现的，也有的同学<strong>误认为</strong>我国古代只有诗歌、没有科技。其实这些成果都产生在古代，而且很早就传到了世界其他地方。<strong>中华文化是各民族共同创造的。</strong></p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "一张纸、一本书、一个指方向的针、一撮黑色的药粉——四样不起眼的东西，改写了世界许多地方的生活。"},
    {"lens": "解释它", "text": "为什么四项技术能有那么大的影响？因为它们解决的都是人人都遇到的问题：怎么记、怎么传、怎么走、怎么防。越普通的问题，解决了就越了不起。"},
    {"lens": "迁移它", "text": "这套眼光放到今天一样有用：判断一项技术值不值得记下来，就问它替多少人解决了多日常的麻烦。"},
])}
    ''', tag="概念二"))

    _tl_name = {t["k"]: t["n"] for t in TIMELINE}
    shuffled_btns = "\n".join(
        f'            <button class="choice" data-tl-step="{k}" style="text-align:left">'
        f'{i}. {_tl_name[k]}</button>'
        for i, k in enumerate(TIMELINE_SHUFFLED, 1)
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：文化瑰宝时间轴，按先后排一排", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">下面五张卡片是打乱的。请你按事情发生的先后顺序，一张一张点下去：点对了就排进时间轴，点错了会告诉你这一步该放在哪里想。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 打乱的成就卡（点你认为最早的那一张）</div>
          <div id="tl-stage">
            <div class="grid">
{shuffled_btns}
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">时间轴进度</span><span class="v" id="tl-score">已经排好 0 / 5 步</span></div>
          </div>
          <p class="result warn" id="tl-out" style="margin-top:12px">先点一张成就卡。</p>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 中华文明时间轴</div>
          <div class="sort-bank" id="tl-axis"><span style="color:var(--muted);font-size:14px">时间轴还是空的。</span></div>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">⏳</span><div><strong>排完想一想：</strong>从商代的甲骨文到明代的《本草纲目》，中间隔了两千多年。这条时间轴上没有终点——今天的人也在往上写字。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：文化展的五条讲解词", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>小语要为文化展写五条讲解词。请你逐条判断这些说法是否正确：哪条能直接用，哪条必须改。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>「传统美德已经过时了」（必须改）：</strong>孝敬长辈、诚实守信、勤劳节俭、扶危济困，这些美德源远流长，今天依然是我们做人的根本。</div></div>
          <div class="step"><span class="n">2</span><div><strong>「四大发明指的是造纸术、印刷术、指南针和火药」（正确）：</strong>四项技术都产生在古代，后来传播到世界各地。</div></div>
          <div class="step"><span class="n">3</span><div><strong>「文化自信就是不听、不看外国文化」（必须改）：</strong>文化自信是尊重和传承自己的文化，同时也学习借鉴外来文化的有益成果。</div></div>
          <div class="step"><span class="n">4</span><div><strong>「汉字是世界上仍在使用的最古老的文字」（正确）：</strong>从甲骨文、金文、小篆、隶书到楷书，一路演变到今天。</div></div>
          <div class="step"><span class="n green">5</span><div><strong>「这些成就是汉族一个民族创造的」（必须改）：</strong>中华文化是各民族共同创造的——布达拉宫融合藏汉建筑艺术，敦煌莫高窟的彩塑壁画里也有各民族交流的痕迹。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>讲文化就要说「我们最强」。可真正的自豪不用靠贬低别人来衬托：<strong>把成就说准、说出它解决了什么问题、说清它今天还在不在用</strong>，才最有说服力。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "关于汉字，下面哪句话说得准确？",
         "options": [("汉字从甲骨文、金文、小篆、隶书到楷书，一路演变到今天，是世界上仍在使用的最古老的文字", True),
                     ("汉字是外国人发明后传到我国的", False),
                     ("汉字的写法从古到今完全一样", False)],
         "explain": "汉字是中华民族创造出来的，形体一直跟着生活变，但表意的根没有断。"
                    "<strong>错因提醒：</strong>常见错误是<strong>误认为</strong>汉字一成不变，或者把自家人创造的东西说成别人的。"},
        {"q": "关于我国古代的科技成就，下面哪句话说得准确？",
         "options": [("四大发明是造纸术、印刷术、指南针和火药，它们传播到世界各地，推动了世界文明的发展", True),
                     ("四大发明里包括瓷器", False),
                     ("我国古代只有诗歌，没有科技成就", False)],
         "explain": "四大发明指的是四项技术；除它们之外，都江堰、赵州桥、地动仪、圆周率的成果也都产生在古代。"
                    "<strong>错因提醒：</strong>容易把丝绸、瓷器、茶叶这些同样有名的物产<strong>和四大发明搞混</strong>。"},
        {"q": "关于中华优秀传统文化，下面哪句话说得准确？",
         "options": [("中华文化是各民族共同创造的，传统美德源远流长，今天依然是我们做人的根本", True),
                     ("这些成就是汉族一个民族创造的，与其他民族无关", False),
                     ("讲文化自信就要抵制一切外来文化", False)],
         "explain": "中华文化是各民族共同创造的；传统美德今天仍然管用；文化自信是传承自己的文化，同时也学习借鉴外来文化的有益成果。"
                    "<strong>错因提醒：</strong>有的同学<strong>误认为</strong>「自信就是排外」——真正的自信不怕交流。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：我的文化自豪卡", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">三步各选一个：<strong>我想介绍的门类 → 我想介绍的成就 → 我为什么为它自豪</strong>。选完，你就设计出了一张属于自己的文化自豪卡。</p>
        <div class="lab-panel">
          <div id="pc-stage"></div>
          <div id="pc-panel"></div>
          <p class="result warn" id="pc-out" style="margin-top:12px">从第一步开始选。</p>
        </div>
        <div class="inner-card" style="margin-top:14px">
          <p><strong>把它写下来：</strong></p>
          <p style="color:var(--muted)">如果让你向外国的小朋友介绍一种中华文化，你最想介绍哪一样？试着写三句话：它是什么、它解决了什么问题或美在哪里、今天还有没有在用。</p>
          <textarea id="syn-answer" rows="3" placeholder="我想介绍的是……，它……，今天……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，说法还站得住吗", TTS["posttest"], [
        {"q": "在博物馆里，你看到一件东汉时期的器物，说明牌上写着它与「造纸术的改进」有关。这位改进造纸术的人是：",
         "options": [("蔡伦", True), ("毕昇", False), ("李时珍", False)],
         "explain": "东汉的蔡伦改进了造纸术，用树皮、麻头、破布等便宜材料造纸；毕昇是北宋发明活字印刷的人，李时珍是明代编写《本草纲目》的人。"
                    "<strong>错因提醒：</strong>容易把人物和成就<strong>搞混</strong>——记住朝代，人就不容易认错。"},
        {"q": "一位外国小朋友问你：「你们的古人最了不起的是什么？」下面哪种回答更好？",
         "options": [("先举一个具体的例子，说清它解决了什么问题、今天还在不在用，再请他一起看", True),
                     ("说「我们什么都比你们强」，别的不用讲", False),
                     ("说「都是很久以前的事，说不清楚」", False)],
         "explain": "把成就说准、说出它解决了什么问题，是最有说服力的介绍，也最能让别人记住。"
                    "<strong>错因提醒：</strong>有的同学<strong>误认为</strong>自豪就要说「最强」——真正的自豪不怕说出细节，也不怕听别人讲他们自己的文化。"},
        {"q": "班级要做一期「传统美德在身边」的展板，下面哪种做法更合适？",
         "options": [("先和同学一起找出身边孝敬长辈、诚实守信、勤劳节俭的具体事例，再写成小故事", True),
                     ("把「孝敬长辈」「诚信」几个词抄一遍贴在展板上就够了", False),
                     ("写「这些美德已经过时了，不用做了」", False)],
         "explain": "传统美德源远流长，今天依然是我们做人的根本；用身边的具体事例来说明，别人才看得见它还在。"
                    "<strong>错因提醒：</strong>容易把「记词」<strong>误认为</strong>「懂得」——能把道理讲成一件身边的小事，才算真的明白了。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：美丽文字、耀我中华、源远流长的美德", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>美丽文字：</strong>汉字是世界上最古老的文字之一，也是目前世界上仍在使用的最古老的文字；甲骨文、金文、小篆、隶书、楷书一路演变到今天，还长出了书法这门艺术。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>古代科技：</strong>造纸术、印刷术、指南针和火药是我国古代的四大发明；此外还有都江堰、赵州桥、地动仪和圆周率的成果，都产生在古代。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>灿烂文化：</strong>《诗经》《史记》和唐诗宋词、四大名著；书法、国画、京剧、编钟、敦煌莫高窟；万里长城、北京故宫、布达拉宫——这些成就是各民族共同创造的。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>源远流长的美德：</strong>孝敬长辈、诚实守信、勤劳节俭、扶危济困，今天依然是我们做人的根本。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>一句口诀：</strong>甲骨一路写到楷，四大发明传到外；诗书戏画皆瑰宝，传统美德传下来。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「演变」「四大发明」这两个词，给家里人讲一件祖先留下的东西，并说说它今天还有没有在用。</p>
          <p style="color:var(--muted)">再动一动手：<strong>写一写</strong>你最想学会的一样传统本领（比如写毛笔字、包粽子、剪纸），写清楚它属于哪个门类、你打算怎么开始学。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写出汉字演变的大致顺序（至少写四个阶段）。",
            "写出四大发明的名称，并各写一句它们各自的作用。",
            "写出两条你记住的传统美德，并各举一个身边的小例子。",
        ],
        [
            "选一项你最喜欢的文化成就，查一查它产生在什么时候、解决了什么问题，把答案整理成三句话。",
            "运用本课学到的分类方法，判断下面四项分别属于科技发明、文学典籍、艺术还是建筑：《史记》、京剧、赵州桥、指南针；判断完说说你的理由。",
        ],
        [
            "设计一张文化自豪卡，写清楚你选的门类、成就和说明，配一幅自己的小画，在班里讲一遍，再请同学说说听完以后还想知道什么。",
            "和家人一起做一件与传统技艺有关的小事（写一页毛笔字、剪一张窗花、学做一种传统小吃），记录过程，并说说它让你对传统美德有了什么新的感受。",
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
    "title": "骄人祖先 灿烂文化",
    "name_en": "Our Glorious Ancestors and Splendid Culture",
    "grade": 5,
    "grade_cn": "五年级",
    "domain": "tradition-culture",
    "domain_cn": "中华优秀传统文化",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学五年级的道德与法治课，正对统编五上第 4 单元「骄人祖先 灿烂文化」，落到「美丽文字 民族瑰宝」「古代科技 耀我中华」「传统美德 源远流长」三件事上，讲灿烂文明与民族团结，积极正面。第一件事是文字：汉字是世界上最古老的文字之一，也是目前世界上仍在使用的最古老的文字；从商代刻在龟甲兽骨上的甲骨文，到商周铸在青铜器上的金文，到秦统一后通行的小篆，到汉代把弯笔拉直的隶书，再到魏晋以后通行至今的楷书，一路演变；我们写的字大多是形声字；书法成为一门艺术，东晋王羲之的《兰亭集序》被誉为「天下第一行书」，笔、墨、纸、砚被称为「文房四宝」；汉字传到周边国家，对那里的文字和文化产生了影响。第二件事是古代成就：造纸术（东汉蔡伦改进）、印刷术（北宋毕昇发明活字印刷）、指南针（战国已有司南，宋代用于航海）、火药（唐代已有配方，宋代广泛用于军事）是我国古代的四大发明，后来传播到世界各地，推动了世界文明的发展；此外还有战国李冰主持修建、至今仍在灌溉的都江堰，隋代李春设计建造的赵州桥，东汉张衡发明的地动仪，南北朝祖冲之把圆周率精确到小数点后第七位；典籍有《九章算术》《本草纲目》《天工开物》《诗经》《史记》，文学有唐诗宋词与四大名著，艺术有书法、国画、京剧、曾侯乙编钟与敦煌莫高窟，建筑有万里长城、北京故宫与布达拉宫——这些成就是各民族共同创造的。第三件事是传统美德：孝敬长辈、诚实守信、勤劳节俭、尊师重道、扶危济困与家国情怀，源远流长，今天依然是我们做人的根本，并与社会主义核心价值观相衔接。三个互动台子都能真操作，反馈一律写成「这样可能会……，还可以试试……」：动手一是文化瑰宝分类台（十二张成就卡分入科技发明、文学典籍、艺术、建筑四栏，四大发明尽在其中）、动手二是文化瑰宝时间轴（五张成就卡按时间先后排成一条中华文明时间轴）、综合任务是我的文化自豪卡（选门类 → 选成就 → 选一句说明，合成一张自豪卡）。全课同时纠正三类常见偏差：误认为汉字一成不变或由他人发明，误认为四大发明是近代产物或把瓷器混入其中，误认为传统美德过时、文化自信就是排外。插图一律为中性简洁扁平插画，不使用真人照片风格。",
    "tags": ["骄人祖先 灿烂文化", "美丽文字 民族瑰宝", "古代科技 耀我中华", "传统美德 源远流长", "四大发明", "汉字演变", "五年级", "中华优秀传统文化"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学「中华优秀传统文化」——了解基本国情，热爱祖国，增强民族自豪感，树立国家认同；对应统编《道德与法治》五年级上册 第4单元「骄人祖先 灿烂文化」：美丽文字 民族瑰宝；古代科技 耀我中华；传统美德 源远流长。",
    "hero_question": "祖先留下的东西，凭什么让我们今天还在用、还在讲？",
    "hero_alt": "骄人祖先灿烂文化知识结构图：美丽文字民族瑰宝、古代科技耀我中华、传统美德源远流长 三栏，附中文标注",
    "hero_caption": "骄人祖先 灿烂文化：甲骨一路写到楷 · 四大发明传到外 · 诗书戏画皆瑰宝 · 传统美德传下来",
    "anchor_title": "今天最想知道哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "汉字是怎么变成今天这样的？", "d": "从甲骨文到楷书，中间发生了什么", "v": "汉字是怎么变成今天这样的"},
        {"t": "四大发明为什么了不起？", "d": "造纸、印刷、指南针、火药各解决了什么", "v": "四大发明为什么了不起"},
        {"t": "祖先还留下了哪些宝贝？", "d": "诗歌、书画、建筑、器物里藏着什么", "v": "祖先还留下了哪些宝贝"},
        {"t": "那些传统美德今天还有用吗？", "d": "孝、信、勤、俭，今天怎么接着做", "v": "那些传统美德今天还有用吗"},
    ],
    "objectives": [
        "能说出汉字是世界上最古老的文字之一，也是目前世界上仍在使用的最古老的文字，并能说出甲骨文、金文、小篆、隶书、楷书的大致演变顺序",
        "能说出造纸术、印刷术、指南针和火药是我国古代的四大发明，并各说一句它们的作用",
        "能举例说出我国古代的科技、文学、艺术和建筑成就，并把它们分门别类",
        "能说出孝敬长辈、诚实守信、勤劳节俭等传统美德源远流长，今天依然是我们做人的根本",
    ],
    "objectives_plain": [
        "能说出汉字的大致演变顺序，知道汉字是目前世界上仍在使用的最古老的文字",
        "能说出四大发明的名称和各自的作用",
        "能举例说出我国古代的科技、文学、艺术和建筑成就，并分门别类",
        "能说出传统美德源远流长，今天依然是我们做人的根本",
    ],
    "standards": [
        {"content": "了解基本国情，热爱祖国，增强民族自豪感，树立国家认同。",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学 中华优秀传统文化"},
        {"content": "美丽文字 民族瑰宝；古代科技 耀我中华；传统美德 源远流长",
         "source": "统编《道德与法治》五年级上册 第4单元「骄人祖先 灿烂文化」"},
    ],
    "prereqs": ["pol-e-g5-u3"],
    "prereqs_name": "我们的国土 我们的家园",
    "prereqs_meta": "pol-e-g5-u3",
    "leads_to": ["pol-e-g6-u1"],
    "next_meta": "pol-e-g6-u1",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "你写的字、背的诗，都是祖先留下的东西——它们凭什么能一直用到今天？",
        "problem-anchor": "先定一个小目标：这节课结束时，你能为一件事说出「为什么值得自豪」，而且说得准。",
        "objectives": "看清四件事：汉字怎么演变、四大发明是什么、古代成就有哪些门类、传统美德今天还管不管用。",
        "pretest": "凭现在的印象选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "一种文字能被几千年的人一直接着用，本身就是了不起的事。注意它的分期：甲骨文、金文、小篆、隶书、楷书。",
        "lab-1": "先点卡片、再点分类栏。分不清时问自己：它是能用的技术、读的书、欣赏的作品，还是地上的建筑？",
        "module-2": "四大发明各解决了一个日常难题：写在哪儿、怎么印、怎么认路、怎么配药。加上诗书戏画建筑，成就数不完。",
        "lab-2": "五张卡按时间先后排。先找最早的甲骨文，再一路往后排——你会看到文明是一步一步长出来的。",
        "worked-example": "五条讲解词里三条要改：把传统美德说成过时、把文化自信说成排外、把成就归给一个民族。",
        "conceptest-1": "三个说法里各藏着一个容易想歪的地方，选完把解释读一遍。",
        "synthesis": "三步合成自豪卡：我想介绍的门类 → 我想介绍的成就 → 我为什么为它自豪。",
        "posttest": "出现了博物馆、外国朋友和班级展板，看看今天的说法还用不用得上。",
        "summary": "四句话：美丽文字、古代科技、灿烂文化、源远流长的美德。",
        "homework": "三层小任务，先做前两层；第三层要动手做一件与传统技艺有关的小事。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学道德与法治「中华优秀传统文化」板块在五年级的空缺，正对统编五上第 4 单元「骄人祖先 灿烂文化」（美丽文字 民族瑰宝；古代科技 耀我中华；传统美德 源远流长），基调是灿烂文明与民族团结、积极正面。五年级学生对手抄报上的名词并不陌生，但对「汉字为什么值得自豪」「四大发明到底解决了什么问题」「传统美德今天还有没有用」往往说不清楚；另外还容易产生三类偏差：把汉字说成一成不变或由他人发明，把四大发明说成近代产物或把瓷器混进去，把传统美德说成过时的老古董、把文化自信说成排外。所以全课不讲空泛的赞美，而是把每一样成就还原成「它解决了什么问题、今天还在不在用」。第一层是「美丽文字」：从甲骨文、金文、小篆、隶书到楷书，把汉字演变的线索理顺，说明它一直在变、也变得好用，所以能被几千年的人接着用；再从形声字讲到书法与文房四宝。第二层是「古代科技」：把四大发明各自解决的难题说清（写在哪儿、怎么印得快、海上怎么认方向、配药里长出的火药），再扩展到都江堰、赵州桥、地动仪、圆周率，以及典籍、诗词、戏曲、书画、石窟与长城、故宫、布达拉宫——并明确这些成就是各民族共同创造的。第三层是「传统美德」：孝敬长辈、诚实守信、勤劳节俭、扶危济困，源远流长，今天依然是我们做人的根本；例题示范做成一次「文化展讲解词校对」，直接纠正「美德过时」「自信就是排外」「成就归一个民族」这三种说法。三个互动台子都能真操作，反馈一律写成「这样可能会……，还可以试试……」：动手一是文化瑰宝分类台，十二张成就卡分入科技发明、文学典籍、艺术、建筑四栏，四大发明尽在其中，放错即给错因与下一步提示；动手二是文化瑰宝时间轴，五张成就卡按时间先后排成一条从商代甲骨文到明代《本草纲目》的时间轴；综合任务是我的文化自豪卡，学生按「我想介绍的门类 → 我想介绍的成就 → 我为什么为它自豪」各选一步，由系统合成一张自己的自豪卡。插图一律为中性简洁扁平插画，不使用真人照片风格。",
    "plan_table": """| 1 | cover | 骄人祖先 灿烂文化 | 定向 |
| 2 | interactive | 今天最想知道哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：祖先留下的东西，你记得多少？ | 起·前测（暴露已有印象与三类偏差） |
| 5 | concept | 美丽文字 民族瑰宝：一种一直在用的古老文字 | 承·概念一（汉字演变与书法） |
| 6 | interactive | 动手一：文化瑰宝分类台，十二张卡片各归其位 | 承·核心模拟（科技发明/文学典籍/艺术/建筑分类） |
| 7 | concept | 古代科技 耀我中华：从四大发明到诗书建筑 | 承·概念二（四大发明与各门类成就） |
| 8 | interactive | 动手二：文化瑰宝时间轴，按先后排一排 | 承·时间轴（商代甲骨文 → 明代《本草纲目》） |
| 9 | concept | 例题示范：文化展的五条讲解词 | 转·重难点突破（逐条判断 + 三类偏差纠正） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：我的文化自豪卡 | 合·迁移应用（三步合成自豪卡） |
| 12 | quiz | 后测：换几个新情境，说法还站得住吗 | 合·后测 |
| 13 | summary | 小结：美丽文字、耀我中华、源远流长的美德 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：美丽文字 民族瑰宝 / 古代科技 耀我中华 / 传统美德 源远流长 三栏，附中文标注\n- P5 四大发明扁平插画（已生成）：造纸、印刷、指南针、火药四格图标，每格配中文标签\n- P7 中华优秀传统文化成就四栏分类示意图（已生成）：科技发明 / 文学典籍 / 艺术 / 建筑，每栏配扁平图标与中文标签\n- 三张图均为中性简洁扁平教学插画，不使用真人照片风格，不含可识别的真实人物\n- 成就表述均核对朝代与人物：蔡伦（东汉）改进造纸术、毕昇（北宋）发明活字印刷、李冰（战国）主持修建都江堰、李春（隋代）设计建造赵州桥、李时珍（明代）编写《本草纲目》\n- 明确表述中华文化是各民族共同创造的（布达拉宫融合藏汉建筑艺术、敦煌莫高窟彩塑壁画含各民族交流痕迹）\n- 若需补充：学生自己书写的书法练习、剪纸作品照片（由学生提供，不在课件中呈现任何个人真实信息）",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
