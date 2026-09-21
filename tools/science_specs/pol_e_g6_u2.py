# -*- coding: utf-8 -*-
"""小学道德与法治 · 我们是公民（六年级上·第2单元）—— 补齐知识树「中华优秀传统文化」空缺

学科语气（道德与法治）：从学生手里的学生证、家里的户口本、班级群里的消息讲起，
情感共鸣 + 价值判断；结论落在「我是谁、我能做什么、我也要做什么」，不做口号式抒情、不背条文。

★ 表述红线（最高优先级，全课统一口径，任何地方不得含糊）：
  · 法律名称一律写全称、写准确：《中华人民共和国宪法》《中华人民共和国国籍法》。
  · 一律不出现任何法律条文编号（不写「第几条」，只说「宪法规定」「法律规定」）。
  · 不臆造案例细节、不编造人物与机关办理流程；权利与义务的举例只用常识层面、
    社会公认的、不会有争议的内容，宁少举一条也不含糊一条。
  · 公民身份的取得只讲常识层面：我国公民是指具有中华人民共和国国籍的人；
    国籍的取得主要有因出生取得和因申请加入取得两种方式；我国不承认中国公民具有双重国籍。

内容落点（对应统编六上第 2 单元「我们是公民」）：
  ① 公民意味着什么：我国公民是指具有中华人民共和国国籍的人；国籍的取得主要有两种方式，
     其中最常见的是因出生取得——父母双方或一方为中国公民，本人出生在中国，具有中国国籍；
     符合法律规定条件的，也可以申请加入中国国籍；我国不承认中国公民具有双重国籍。
     公民身份意味着：法律面前一律平等，同时受到国家的保护，也要承担相应的义务。
  ② 公民的基本权利与基本义务：把小学阶段应当知道的几项权利与几项义务讲清楚，
     并把两者的一致关系说明白——权利和义务相互依存、相互促进；
     公民既是权利的享有者，也是义务的承担者；不能只享受权利而不履行义务；
     劳动和受教育既是权利，也是义务；行使自由和权利不得损害国家的、社会的、集体的利益
     和其他公民的合法的自由和权利。

三个互动台子都能真操作（反馈一律写成「这样可能会……，还可以试试……」）：
  动手一 = ★核心模拟「权利与义务配对台」（6 张权利卡 × 6 张义务卡）；
  动手二 = ★核心模拟「我是小公民」情境判断台（6 个校园与家庭情境，判断属于哪一类）；
  综合任务 = 「我是小公民」行动卡生成台（选问题 → 选对应权利 → 选对应义务与行动 → 合成行动卡）。
插图一律中性简洁扁平插画，不使用真人照片风格，不绘制国旗、国徽、宪法文本封面等图形，
涉及公民身份与权利义务改用徽章圆环、人物剪影、天平、握手、齿轮等抽象符号与地标性建筑抽象剪影。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g6-u2"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "上一节课我们知道了法律和宪法在守护我们。这节课换一个角度：把目光转向我们自己。你有没有想过，从你出生的那天起，你就已经拥有一个身份了——中华人民共和国公民。这个身份意味着什么？它给你哪些权利？又要求你承担哪些义务？这节课我们弄清楚三件事：我是怎样成为一个中国公民的，我有什么样的基本权利，我又要履行哪些基本义务。",
    "problem-anchor": "开始之前，先选一个你真正想知道的问题：我是怎样成为一个中国公民的？公民和外国人有什么不一样？我的基本权利有哪些？还是权利和义务之间到底有什么关系？选好以后，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出我国公民是指具有中华人民共和国国籍的人，能说出国籍的取得主要有因出生取得和因申请加入取得两种方式。第二，能说出几项公民的基本权利，比如平等权、受教育权、人格尊严不受侵犯。第三，能说出几项公民的基本义务，比如遵守宪法和法律、依法纳税、受教育。第四，能说出权利和义务相互依存、相互促进，既不能只享受权利不履行义务，也不能在行使权利时损害他人的合法权益。",
    "pretest": "先做三道小题，用你现在的想法选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "第一件事，公民意味着什么。先记住一句话：我国公民，是指具有中华人民共和国国籍的人。国籍就像一张法律上的身份证明，它把一个人和一个国家连在一起。那么，一个人是怎样取得中国国籍的呢？主要有两种方式。第一种是因出生取得，这也是最常见的一种：父母双方或一方为中国公民，本人出生在中国，具有中国国籍。第二种是因申请加入取得：符合法律规定条件的，可以申请加入中国国籍。这里有一个很特别的例子要记住：父母双方或一方为中国公民，本人出生在外国，也具有中国国籍；但如果父母双方或一方为中国公民并定居在外国、本人出生时就已经具有外国国籍的，就不具有中国国籍。这就是为什么我国不承认中国公民具有双重国籍。公民这个身份，一来意味着保护：国家依法保护公民的合法权益；二来意味着平等：中华人民共和国公民在法律面前一律平等。这里有两个容易想歪的地方：有的同学误认为在中国居住的外国朋友就是中国公民；也有的同学误认为公民身份是长大后才有、小孩子还不算。其实只要具有中华人民共和国国籍，就是中国公民，我们已经是小公民了。",
    "lab-1": "现在请你玩一次配对。左边是六张权利卡，右边是六张义务卡，顺序被打乱了。先点一张权利卡，再点一张你认为与它相配的义务卡。配对了，两边会连起来，我会告诉你它们为什么配得起来；配错了，我会告诉你这样可能会错在哪里，还可以怎么想。",
    "module-2": "第二件事，我们的基本权利和基本义务。先说基本权利。我国公民在法律面前一律平等；年满十八周岁、依法享有政治权利的公民有选举权和被选举权；公民有言论、出版、集会、结社、游行、示威的自由，也有宗教信仰自由；公民的人身自由、人格尊严、住宅不受侵犯，通信自由和通信秘密受法律保护；公民对国家机关和国家工作人员有提出批评和建议的权利；公民有劳动的权利、休息的权利，有受教育的权利，有进行科学研究、文学艺术创作和其他文化活动的自由。再说基本义务。公民有维护国家统一和全国各民族团结的义务；有遵守宪法和法律、保守国家秘密、爱护公共财产、遵守劳动纪律、遵守公共秩序、尊重社会公德的义务；有维护祖国的安全、荣誉和利益的义务；有保卫祖国、依法服兵役的义务；有依法纳税的义务；劳动和受教育也同时是我们的义务。最后说两者的关系：在我国，公民的权利和义务相互依存、相互促进；公民既是合法权利的享有者，又是法定义务的承担者；不能只享受权利而不履行义务，也不能只要求履行义务而忽视权利的保障。还有一条边界要记住：公民在行使自由和权利的时候，不得损害国家的、社会的、集体的利益和其他公民的合法的自由和权利。这里有两个最容易搞混的地方：有的同学误认为权利和义务是两回事，可以分开来算；其实它们常常是一件事的两面，劳动和受教育就是最好的例子。也有的同学误认为权利就是想做什么就做什么，忘了行使权利也有边界。",
    "lab-2": "接下来请你自己判断几个情境。这里有六个发生在校园和家庭里的情境，每一个后面有三个选项：这是在行使权利、这是在履行义务，还是这样做其实不妥。先读情境，再选一个，然后看解释。判断错了也没关系，正好知道要重点想哪一步。",
    "worked-example": "我们一起来看一次权义账单的校对。班里要做一期我是小公民的展板，几位同学写了五条说法，请你当一次校对员。说法一，权利是我想行使就行使，义务可以等到长大以后再履行。这条要改。权利和义务相互依存、相互促进，公民既是权利的享有者，也是义务的承担者，不能只享受权利而不履行义务。说法二，受教育既是我们的权利，也是我们的义务。这条正确，很多权利和义务本来就是一件事的两面。说法三，班里有人在群里转发了某某同学偷东西这条没有核实的消息，他说这是在行使言论自由，别人管不着。这条要改。公民在行使自由和权利的时候，不得损害国家的、社会的、集体的利益和其他公民的合法的自由和权利，随便转发没有核实的消息，会伤害同学的人格尊严。说法四，依法纳税是公民的义务，国家依法征收的税款用在学校的建设、医院的建设、道路的修建这些公共事业上，所以依法纳税也是每个公民对国家应尽的责任。这条正确。说法五，中华人民共和国公民在法律面前一律平等。这条也正确，平等权是我们一项很重要的基本权利。这里有一个常见错误要提醒：有的同学把权利和义务搞混成两件互不相干的事，觉得可以只挑权利那一半；还有的同学把行使权利误认为想做什么就做什么。记住两句话就够了：权利与义务相互依存；行使权利有边界。",
    "conceptest-1": "接下来用三道题考考你，每道题里都藏着一个容易想歪的地方。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件任务交给你：为自己做一张小公民行动卡。下面分三步：先选一个你想去推动的校园或者社区问题，再选这件事和你的一项基本权利有什么关系，最后选你打算承担的一项义务或者一个具体行动。三步选完，我会把它们拼成一张行动卡，你可以贴上班级展板。",
    "posttest": "最后一轮，换几个新情境来考考你。这次会遇到户口本上的名字、班级群里的消息和小区里的事，看看今天学的说法还用不用得上。",
    "summary": "这节课我们弄清楚三件事。第一，公民意味着什么：我国公民是指具有中华人民共和国国籍的人；国籍的取得主要有因出生取得和因申请加入取得两种方式；父母双方或一方为中国公民、本人出生在中国，具有中国国籍；我国不承认中国公民具有双重国籍。第二，我们的基本权利：法律面前一律平等，享有政治权利和自由、人身自由和人格尊严不受侵犯、受教育权、劳动权等。第三，我们的基本义务：遵守宪法和法律、维护国家统一和民族团结、依法服兵役、依法纳税，劳动和受教育也同时是义务。最后记住两句话：权利和义务相互依存、相互促进，不能只享受权利不履行义务；行使自由和权利不得损害他人的合法权益。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出我国公民是指什么样的人，再写出国籍取得的两种主要方式。第二层能力应用，动手做：列出四项公民的基本权利和四项基本义务，每一项都用一句话说明它在生活里是什么样子。第三层迁移挑战，选做：做一张小公民行动卡，写清楚你想推动的一个问题、它与你哪一项权利有关、你打算承担哪一项义务或者做哪一件具体的事，做完在班里交流一遍。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域里的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 公民意味着什么", "lab-1": "动手一 权利与义务配对台",
    "module-2": "概念二 公民的基本权利与基本义务", "lab-2": "动手二 我是小公民情境判断台",
    "worked-example": "例题示范 权义账单校对", "conceptest-1": "概念测试",
    "synthesis": "综合任务 小公民行动卡生成台", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一（★核心模拟）：权利与义务配对台（6 权利卡 × 6 义务卡） ──
RIGHTS = [
    {"k": "r1", "n": "受教育的权利",
     "what": "我们有上学读书、接受教育的权利。",
     "pair": "d1",
     "why": "受教育既是我们的权利，也是我们的义务——这是同一件事的两面。国家保障我们上学，我们也要认真完成学业。",
     "tip": "还可以试试：想一想「我想上学」和「我必须上学」这两句话，分别说的是哪一面。"},
    {"k": "r2", "n": "劳动的权利",
     "what": "有劳动能力的公民有参加劳动、取得报酬的权利。",
     "pair": "d2",
     "why": "劳动同样是权利和义务的统一：既能通过劳动获得收入，也是每个有劳动能力的人对社会应尽的责任。",
     "tip": "还可以试试：把「我将来想做什么工作」和「我能为别人做什么」放在一起想一想。"},
    {"k": "r3", "n": "言论自由的权利",
     "what": "公民有言论的自由，可以表达自己的看法。",
     "pair": "d3",
     "why": "说话的权利有边界：行使自由和权利的时候，不得损害国家的、社会的、集体的利益和其他公民的合法的自由和权利，要尊重他人的人格尊严。",
     "tip": "还可以试试：说出口之前先问一句——这句话是真的吗，会不会伤到别人。"},
    {"k": "r4", "n": "享有国家提供的公共服务的权利",
     "what": "我们可以上学、可以走公共交通、可以得到公共卫生服务。",
     "pair": "d4",
     "why": "这些公共服务离不开国家的投入，而国家的收入主要来自税收，所以依法纳税的义务和每个人享有的公共服务是连在一起的。",
     "tip": "还可以试试：想一想自己每天用到的公共设施里，有哪些是大家一起支撑起来的。"},
    {"k": "r5", "n": "各民族一律平等的权利",
     "what": "各民族不论人口多少，都享有平等的权利。",
     "pair": "d5",
     "why": "我们享有民族平等的权利，也要履行维护国家统一和全国各民族团结的义务——权利要靠每个人一起来守护。",
     "tip": "还可以试试：想一想班里同学来自不同地方，怎样才能让大家都很自在。"},
    {"k": "r6", "n": "受国家保护、和平生活的权利",
     "what": "国家保护公民的安全，我们才能在和平的环境里生活。",
     "pair": "d6",
     "why": "和平安定的生活，来自有人依法守护国家安全，所以保卫祖国、依法服兵役也是公民的光荣义务。",
     "tip": "还可以试试：想一想安宁的日子背后，有哪些人在默默承担。"},
]

DUTIES = [
    {"k": "d1", "n": "受教育的义务",
     "what": "适龄儿童、少年要依法接受并完成义务教育。", "pair": "r1"},
    {"k": "d2", "n": "劳动的义务",
     "what": "有劳动能力的公民都要以劳动为社会尽一份力。", "pair": "r2"},
    {"k": "d3", "n": "尊重他人人格尊严的义务",
     "what": "表达看法时不能侵害他人的合法权益。", "pair": "r3"},
    {"k": "d4", "n": "依法纳税的义务",
     "what": "公民要依照法律规定缴纳税款。", "pair": "r4"},
    {"k": "d5", "n": "维护国家统一和全国各民族团结的义务",
     "what": "维护国家统一，维护民族团结，是每个公民的责任。", "pair": "r5"},
    {"k": "d6", "n": "保卫祖国、依法服兵役的义务",
     "what": "依法服兵役是公民的光荣义务。", "pair": "r6"},
]

# ── 动手二（★核心模拟）：「我是小公民」情境判断台（6 情境 × 3 选项） ──
JUDGE = [
    {"k": "j1", "n": "按时到校上课，认真完成作业",
     "case": "六年级的小美每天按时到校上课，回家认真完成作业。",
     "opts": [{"t": "这是在行使受教育的权利，不是义务", "ok": False},
              {"t": "这是在履行受教育的义务，和权利没关系", "ok": False},
              {"t": "既是行使受教育的权利，也是履行受教育的义务", "ok": True}],
     "why": "受教育是权利和义务的统一。国家保障我们上学读书；我们也应当按时入学、认真学习。",
     "mis": "有的同学误认为受教育只是自己的权利，想上就上、不想上就不上；也有的同学觉得它只是一项义务，忘了国家也在保障我们上学。这样可能会：把一件本来连着两面的事切成了一半。"},
    {"k": "j2", "n": "在换届选举中投下自己的选票",
     "case": "小美的妈妈在人大代表换届选举中投下了自己的选票。",
     "opts": [{"t": "这是在行使选举权和被选举权等政治权利", "ok": True},
              {"t": "这是在履行依法服兵役的义务", "ok": False},
              {"t": "这是在履行依法纳税的义务", "ok": False}],
     "why": "年满十八周岁、依法享有政治权利的公民，有选举权和被选举权。这是在行使公民的基本政治权利。",
     "mis": "有的同学把选举权和服兵役、纳税搞混了。可以这样记：选举是参与国家政治生活的权利；服兵役和纳税是义务。"},
    {"k": "j3", "n": "按规定申报并缴纳个人所得税",
     "case": "小美的爸爸按规定申报并缴纳了个人所得税。",
     "opts": [{"t": "这是在行使财产权，可以自己决定缴多少", "ok": False},
              {"t": "这是在履行依法纳税的义务", "ok": True},
              {"t": "这是在行使监督权", "ok": False}],
     "why": "依法纳税是公民的一项基本义务。国家依法征收的税款，用于学校、医院、道路这些公共事业。",
     "mis": "常见错误是把纳税<strong>误认为</strong>可以自己决定。税款怎么缴、缴多少，是依照法律规定来办的。"},
    {"k": "j4", "n": "转发了没有核实的消息",
     "case": "小刚在班级群里转发了「某某同学偷了东西」这条没有核实的消息。",
     "opts": [{"t": "这是在正确行使言论自由，别人管不着", "ok": False},
              {"t": "这样不妥，行使权利不能损害他人的合法权益", "ok": True},
              {"t": "这是在履行维护社会公德的义务", "ok": False}],
     "why": "公民在行使自由和权利的时候，不得损害国家的、社会的、集体的利益和其他公民的合法的自由和权利。转发没有核实的消息，会伤害同学的人格尊严。",
     "mis": "有的同学把言论自由<strong>误认为</strong>想说什么就说什么。这样可能会：一句没核实的话，让同学受到很大伤害。还可以试试：先核实，再决定要不要转发。"},
    {"k": "j5", "n": "把作文和画作拿出来展示",
     "case": "阳阳把自己写的作文投了稿，还画了一幅画贴在班级展板上。",
     "opts": [{"t": "这是在行使进行文学艺术创作和其他文化活动的自由", "ok": True},
              {"t": "这是在履行依法服兵役的义务", "ok": False},
              {"t": "这是在履行维护国家统一和民族团结的义务", "ok": False}],
     "why": "公民有进行科学研究、文学艺术创作和其他文化活动的自由，写作文、画画、做手工都是这项自由在生活中的样子。",
     "mis": "容易把这项文化活动的自由和其他义务搞混。可以这样记：写、画、创作属于文化活动的自由。"},
    {"k": "j6", "n": "在小区里爱护公共设施",
     "case": "小刚的小区里，大家都不在楼道里大声喧哗，也一起爱护公共设施。",
     "opts": [{"t": "这是在履行遵守公共秩序、尊重社会公德、爱护公共财产的义务", "ok": True},
              {"t": "这是在行使选举权和被选举权", "ok": False},
              {"t": "这是在行使宗教信仰自由", "ok": False}],
     "why": "遵守公共秩序、尊重社会公德、爱护公共财产，都是公民应当履行的义务；大家一起做，小区才会更舒服。",
     "mis": "有的同学觉得这些只是「讲文明」，跟公民的义务没关系。其实它们写在公民应当履行的义务里面。"},
]

# ── 综合任务：小公民行动卡生成台 ──
ACTION = {
    "issues": [
        {"k": "i1", "n": "班级群里总有人转发没核实的消息"},
        {"k": "i2", "n": "小区里的公共设施常被损坏"},
        {"k": "i3", "n": "有同学因为家里的事，很少能安心上学"},
    ],
    "rights": [
        {"t": "这和我的人格尊严不受侵犯有关，不能被没有核实的话伤害", "ok": True,
         "why": "想得准确。人格尊严不受侵犯是一项基本权利，没有核实的消息伤害的正是它。"},
        {"t": "这和我没有关系，我不转发就行了", "ok": False,
         "why": "这样可能会：把一件大家的权利当成别人的事。还可以试试：想一想自己或者同桌遇到这件事会有什么感受。"},
        {"t": "这属于别人的私事，不算权利问题", "ok": False,
         "why": "这样可能会：看不到问题背后的权利。还可以试试：先把「谁被伤害了、被伤害的是什么」写下来。"},
    ],
    "actions": [
        {"t": "先核实再转发，不确定就说「我不确定，先别传了」", "ok": True,
         "why": "这是既行使表达自由、又守住边界的具体行动，做得到、也说得出口。"},
        {"t": "等长大以后再说，现在先不管", "ok": False,
         "why": "这样可能会：眼看着事情一直发生。还可以试试：把行动改小一点——从自己这一句开始。"},
        {"t": "在群里把转发的人骂一顿，让他知道厉害", "ok": False,
         "why": "这样可能会：自己也伤害了别人，问题反而更乱。还可以试试：私下提醒他，或者请老师帮忙说明。"},
    ],
}

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g6-u2 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) ★权利与义务配对台：6 张权利卡 × 6 张义务卡
   3) ★「我是小公民」情境判断台：6 个情境，每个三选一
   4) 「小公民行动卡」生成台：问题 → 对应权利 → 对应行动 → 合成行动卡
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

  /* ---------- 2. ★权利与义务配对台 ---------- */
  var RIGHTS = __RIGHTS_JSON__;
  var DUTIES = __DUTIES_JSON__;
  var stage1 = document.getElementById('rw-stage');
  if (stage1) {
    var selR = null;
    var matched = {};
    var out1 = document.getElementById('rw-out');
    var left = document.getElementById('rw-left');
    var right = document.getElementById('rw-right');
    var board = document.getElementById('rw-board');
    function riteByKey(k) {
      for (var i = 0; i < RIGHTS.length; i++) { if (RIGHTS[i].k === k) return RIGHTS[i]; }
      return null;
    }
    function dutyByKey(k) {
      for (var i = 0; i < DUTIES.length; i++) { if (DUTIES[i].k === k) return DUTIES[i]; }
      return null;
    }
    function render1() {
      left.innerHTML = '';
      RIGHTS.forEach(function (R) {
        var b = document.createElement('button');
        b.className = 'choice' + (matched[R.k] ? ' correct' : (selR === R.k ? ' selected' : ''));
        b.style.textAlign = 'left';
        b.innerHTML = '<strong>' + R.n + '</strong><br><span style="color:var(--muted);font-size:14px">' + R.what + '</span>' +
          (matched[R.k] ? '<br><span style="color:var(--accent-deep);font-size:14px">已配对 ✓</span>' : '');
        b.addEventListener('click', function () {
          if (matched[R.k]) return;
          selR = R.k;
          out1.className = 'result warn';
          out1.innerHTML = '<strong>你选了「' + R.n + '」。</strong>现在到右边点一张你认为与它相配的义务卡。';
          render1();
        });
        left.appendChild(b);
      });
      right.innerHTML = '';
      DUTIES.forEach(function (D) {
        var b = document.createElement('button');
        b.className = 'choice' + (matched[D.k] ? ' correct' : '');
        b.style.textAlign = 'left';
        b.innerHTML = '<strong>履行 ' + D.n + '</strong><br><span style="color:var(--muted);font-size:14px">' + D.what + '</span>' +
          (matched[D.k] ? '<br><span style="color:var(--accent-deep);font-size:14px">配对成功 ✓</span>' : '');
        b.addEventListener('click', function () {
          if (matched[D.k]) return;
          if (!selR) {
            out1.className = 'result warn';
            out1.innerHTML = '先到左边点一张权利卡，再回到右边点义务卡。' +
              '<br><span style="color:var(--muted)">还可以试试：先想这项权利要成立，需要每个人做到什么。</span>';
            return;
          }
          if (selR === D.pair) {
            var RG = riteByKey(selR);
            matched[D.pair] = true;
            selR = null;
            out1.className = 'result';
            out1.innerHTML = '<strong>配上了：' + RG.n + ' —— ' + D.n + '</strong>' + RG.why;
            if (Object.keys(matched).length === RIGHTS.length) {
              out1.innerHTML += '<br><br><strong>六组都配上了。</strong>你会发现，权利和义务不是两件分开的事：' +
                '它们相互依存、相互促进，公民既是权利的享有者，也是义务的承担者。';
            }
          } else {
            var SR = riteByKey(selR);
            out1.className = 'result warn';
            out1.innerHTML = '<strong>这张义务卡和「' + SR.n + '」配不上。</strong>' +
              '这样可能会：把权利和义务当成两件互不相干的事。' + SR.tip;
          }
          render1();
        });
        right.appendChild(b);
      });
      board.textContent = '已经配对 ' + Object.keys(matched).length + ' / ' + RIGHTS.length + ' 组';
    }
    render1();
  }

  /* ---------- 3. ★「我是小公民」情境判断台 ---------- */
  var JUDGE = __JUDGE_JSON__;
  var stage2 = document.getElementById('jd-stage');
  if (stage2) {
    var curJ = null;
    var done2 = {};
    var out2 = document.getElementById('jd-out');
    var panel2 = document.getElementById('jd-panel');
    function judgeByKey(k) {
      for (var i = 0; i < JUDGE.length; i++) { if (JUDGE[i].k === k) return JUDGE[i]; }
      return null;
    }
    function render2() {
      document.querySelectorAll('[data-jd-item]').forEach(function (b) {
        var k = b.dataset.jdItem;
        b.classList.toggle('selected', k === curJ);
        b.classList.toggle('correct', !!done2[k]);
      });
      document.getElementById('jd-score').textContent =
        '已经判断 ' + Object.keys(done2).length + ' / ' + JUDGE.length + ' 个情境';
      if (!curJ) { panel2.innerHTML = ''; return; }
      var J = judgeByKey(curJ);
      var html = '<div style="font-weight:700;font-size:14px;margin:14px 0 0">' + J.case + '</div>';
      html += '<div class="grid" style="margin-top:10px">';
      J.opts.forEach(function (o, i) {
        var cls = 'choice';
        if (done2[J.k]) { cls += o.ok ? ' correct' : ''; }
        html += '<button class="' + cls + '" data-jd-opt="' + i + '" style="text-align:left">' + o.t + '</button>';
      });
      html += '</div>';
      panel2.innerHTML = html;
      panel2.querySelectorAll('[data-jd-opt]').forEach(function (b) {
        b.addEventListener('click', function () { choose(parseInt(b.dataset.jdOpt, 10)); });
      });
    }
    function choose(i) {
      var J = judgeByKey(curJ);
      var o = J.opts[i];
      var first = !done2[J.k];
      done2[J.k] = true;
      if (o.ok) {
        out2.className = 'result';
        out2.innerHTML = '<strong>判断得对。</strong>' + J.why;
      } else if (first) {
        out2.className = 'result warn';
        out2.innerHTML = '<strong>再想一想：' + J.case + '</strong>' + J.why +
          '<br><span style="color:var(--muted)"><strong>错因提醒：</strong>' + J.mis + '</span>';
      } else {
        out2.className = 'result';
        out2.innerHTML = '<strong>正确的判断是：' + J.opts[2].t + '。</strong>' + J.why;
      }
      render2();
      if (Object.keys(done2).length === JUDGE.length) {
        out2.innerHTML += '<br><br><strong>六个情境都判断过了。</strong>' +
          '记住两句话：权利和义务相互依存、相互促进；行使自由和权利不得损害他人的合法权益。';
      }
    }
    document.querySelectorAll('[data-jd-item]').forEach(function (b) {
      b.addEventListener('click', function () {
        curJ = b.dataset.jdItem;
        out2.className = 'result warn';
        out2.textContent = '先读一读情境，再在下面三个选项里选一个。';
        render2();
      });
    });
    render2();
  }

  /* ---------- 4. 「小公民行动卡」生成台 ---------- */
  var ACTION = __ACTION_JSON__;
  var stage3 = document.getElementById('ac-stage');
  if (stage3) {
    var pick = { i: null, r: null, a: null };
    var out3 = document.getElementById('ac-out');
    var panel3 = document.getElementById('ac-panel');
    function issueByKey(k) {
      for (var i = 0; i < ACTION.issues.length; i++) { if (ACTION.issues[i].k === k) return ACTION.issues[i]; }
      return null;
    }
    function render3() {
      var html = '<div style="font-weight:700;font-size:14px;margin-bottom:6px">第一步 · 我想推动的一个问题</div><div class="grid grid-2">';
      ACTION.issues.forEach(function (C) {
        html += '<button class="choice' + (pick.i === C.k ? ' selected' : '') +
          '" data-ac-issue="' + C.k + '" style="text-align:left">' + C.n + '</button>';
      });
      html += '</div>';
      html += '<div style="font-weight:700;font-size:14px;margin:16px 0 6px">第二步 · 这件事和我的哪一项权利有关</div><div class="grid">';
      ACTION.rights.forEach(function (o, i) {
        var cls = 'choice';
        if (pick.r === i) cls += o.ok ? ' correct' : ' wrong';
        html += '<button class="' + cls + '" data-ac-right="' + i + '" style="text-align:left">' + o.t + '</button>';
      });
      html += '</div>';
      html += '<div style="font-weight:700;font-size:14px;margin:16px 0 6px">第三步 · 我打算承担的义务与行动</div><div class="grid">';
      ACTION.actions.forEach(function (o, i) {
        var cls = 'choice';
        if (pick.a === i) cls += o.ok ? ' correct' : ' wrong';
        html += '<button class="' + cls + '" data-ac-act="' + i + '" style="text-align:left">' + o.t + '</button>';
      });
      html += '</div>';
      panel3.innerHTML = html;
      panel3.querySelectorAll('[data-ac-issue]').forEach(function (b) {
        b.addEventListener('click', function () {
          pick.i = b.dataset.acIssue; render3();
          out3.className = 'result warn';
          out3.textContent = '问题选好了，接着选第二步：这件事和哪一项权利有关。';
        });
      });
      panel3.querySelectorAll('[data-ac-right]').forEach(function (b) {
        b.addEventListener('click', function () {
          pick.r = parseInt(b.dataset.acRight, 10);
          var o = ACTION.rights[pick.r];
          out3.className = 'result' + (o.ok ? '' : ' warn');
          out3.innerHTML = (o.ok ? '<strong>这一步想得对。</strong>' : '<strong>这一步还可以再想想。</strong>') + o.why;
          render3();
        });
      });
      panel3.querySelectorAll('[data-ac-act]').forEach(function (b) {
        b.addEventListener('click', function () {
          pick.a = parseInt(b.dataset.acAct, 10);
          render3();
          if (pick.i === null || pick.r === null) {
            out3.className = 'result warn';
            out3.textContent = '三步还没选完，先把前面的补齐。';
            return;
          }
          var C = issueByKey(pick.i);
          var R = ACTION.rights[pick.r];
          var A = ACTION.actions[pick.a];
          var okN = (R.ok ? 1 : 0) + (A.ok ? 1 : 0);
          out3.className = 'result' + (okN === 2 ? '' : ' warn');
          out3.innerHTML = '<strong>我的行动卡 · ' + C.n + '</strong><br>' +
            '第一步：' + C.n + '<br>第二步：' + R.t + '<br>第三步：' + A.t +
            '<br><span style="color:var(--muted)">' + (okN === 2
              ? '权利看得清，行动也做得到。把这张行动卡贴上班级展板，再讲给同桌听一遍。'
              : '还可以再想一想：先弄清这件事和哪一项权利有关，再把行动改小一点、改具体一点。换一个再试一次。') + '</span>';
        });
      });
    }
    render3();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__RIGHTS_JSON__', json.dumps(RIGHTS, ensure_ascii=False))
             .replace('__DUTIES_JSON__', json.dumps(
                 [DUTIES[3], DUTIES[0], DUTIES[5], DUTIES[2], DUTIES[1], DUTIES[4]], ensure_ascii=False))
             .replace('__JUDGE_JSON__', json.dumps(JUDGE, ensure_ascii=False))
             .replace('__ACTION_JSON__', json.dumps(ACTION, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：我是一名小公民吗？", TTS["pretest"], [
        {"q": "下面哪一句话说准了「我国公民」的意思？",
         "options": [("我国公民是指具有中华人民共和国国籍的人", True),
                     ("在我国居住的人都是我国公民", False),
                     ("公民身份要长大以后才能取得", False)],
         "explain": "我国公民，是指具有中华人民共和国国籍的人。国籍把一个人和一个国家连在一起。"
                    "<strong>错因提醒：</strong>常见错误是把「在我国居住」和「具有我国国籍」<strong>搞混</strong>了；公民身份也不是长大以后才有的，我们已经是小公民了。",},
        {"q": "我国国籍的取得主要有哪两种方式？",
         "options": [("因出生取得和因申请加入取得", True),
                     ("因居住取得和因上学取得", False),
                     ("因工作取得和因买房取得", False)],
         "explain": "国籍的取得主要有因出生取得和因申请加入取得两种方式。最常见的是因出生取得：父母双方或一方为中国公民，本人出生在中国，具有中国国籍。"
                    "<strong>错因提醒：</strong>有的同学<strong>误认为</strong>住在中国、在中国上学就是中国公民；国籍的取得是有法律规定的，不然就说不准了。",},
        {"q": "关于权利和义务，下面哪句话说得准确？",
         "options": [("权利和义务相互依存、相互促进，不能只享受权利不履行义务", True),
                     ("权利是权利，义务是义务，可以只挑权利那一半", False),
                     ("行使权利想怎么做就怎么做，不用考虑别人", False)],
         "explain": "在我国，公民的权利和义务相互依存、相互促进；公民既是权利的享有者，也是义务的承担者。行使自由和权利时，不得损害他人的合法权益。"
                    "<strong>错因提醒：</strong>常见错误是把权利和义务当成两件互不相干的事，忘了它们常常是一件事的两面。",}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "公民意味着什么：我是怎样成为一个中国公民的", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们每天上学、写作业、和同学相处，从没想过自己还有一个身份（And）；可要问「我是怎样成为中国公民的、这个身份意味着什么」，很多同学答不上来（But）；所以这节课先把公民身份说清楚（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px"><strong>我国公民，是指具有中华人民共和国国籍的人。</strong>国籍把一个人和一个国家连在一起。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>因出生取得（最常见）：</strong>父母双方或一方为中国公民，本人出生在中国，具有中国国籍。</div></div>
          <div class="step"><span class="n">2</span><div><strong>因申请加入取得：</strong>符合法律规定条件的，可以申请加入中国国籍。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>出生在外国的情况：</strong>父母双方或一方为中国公民，本人出生在外国，也具有中国国籍。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="中国公民身份取得抽象示意：左侧是父母与孩子的人物剪影，中间用加号连接，右侧是圆环徽章标注中华人民共和国国籍，下方标注出生在中国与因申请加入两种方式，附中文标注">
          <figcaption>示意：国籍把一个人和一个国家连在一起 · 因出生取得是最常见的方式 · 抽象示意图，不按比例</figcaption>
        </figure>
        <div class="inner-card">
          <p><strong>一个要点与两重含义</strong></p>
          <p style="color:var(--muted)">我国<strong>不承认中国公民具有双重国籍</strong>。公民这个身份有两重含义：一是受国家保护，二是<strong>法律面前一律平等</strong>。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>在中国居住的外国朋友就是中国公民；也有的同学<strong>误认为</strong>公民身份是长大后才有。其实只要具有中华人民共和国国籍，就是中国公民。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "同一间教室里，大家的家庭、方言、爱好都不一样，但在法律上有一个共同的身份——中华人民共和国公民。"},
    {"lens": "解释它", "text": "为什么国籍这么重要？因为它决定了你受哪个国家的保护、按哪个国家的规则享有权利和承担义务。它不是一个称呼，而是一层法律关系。"},
    {"lens": "迁移它", "text": "这就像转学：进了新的班级，你就享有这个班集体的资源，也要遵守班里的约定。身份带来的是保护，同时带来责任。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "★动手一：权利与义务配对台，把两半配成一件", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点左边一张<strong>权利卡</strong>，再点右边一张你认为与它相配的<strong>义务卡</strong>。配对了会连起来，配错了会告诉你错在哪里。</p>
        <div class="lab-panel">
          <div id="rw-stage">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">点击左侧权利卡，再点右侧义务卡进行配对</div>
            <div class="grid grid-2">
              <div id="rw-left"></div>
              <div id="rw-right"></div>
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">配对进度</span><span class="v" id="rw-board">已经配对 0 / 6 组</span></div>
          </div>
          <p class="result warn" id="rw-out" style="margin-top:12px">先点左边一张权利卡。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">⚖️</span><div><strong>配完回头看：</strong>有些权利和义务本来就是同一件事的两面，比如受教育、劳动；也有些义务，是别人那项权利能成立的条件。权利要靠每个人一起守。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "公民的基本权利与基本义务，还有它们的关系", TTS["module-2"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们已经知道了自己的公民身份（And）；可这个身份到底给我们哪些权利、又要求我们做哪些事，很多同学说不清（But）；所以这节课把基本权利、基本义务和两者的关系讲明白（Therefore）。</p>
        </div>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>我们的基本权利</strong></p>
            <p style="color:var(--muted)">法律面前一律平等；选举权和被选举权；言论等自由与宗教信仰自由；人身自由、人格尊严、住宅不受侵犯；对国家机关和国家工作人员提出批评和建议；劳动、休息、受教育；进行文学艺术创作和其他文化活动。</p>
          </div>
          <div class="inner-card">
            <p><strong>我们的基本义务</strong></p>
            <p style="color:var(--muted)">维护国家统一和全国各民族团结；遵守宪法和法律、保守国家秘密、爱护公共财产、遵守劳动纪律、遵守公共秩序、尊重社会公德；维护祖国的安全、荣誉和利益；保卫祖国、依法服兵役；依法纳税；劳动和受教育同时也是义务。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="权利与义务关系抽象示意：一架天平，左边托盘标注权利，右边托盘标注义务，中央标注相互依存相互促进，两侧用握手与齿轮的抽象符号连接，附中文标注">
          <figcaption>概念图：权利和义务相互依存、相互促进 · 公民既是权利的享有者，也是义务的承担者</figcaption>
        </figure>
        <div class="inner-card">
          <p><strong>一条不能忘的边界</strong></p>
          <p style="color:var(--muted)">公民在行使自由和权利的时候，不得损害国家的、社会的、集体的利益和其他公民的合法的自由和权利。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>权利和义务是两回事，可以只挑权利那一半；也有的同学<strong>误认为</strong>权利就是想做什么就做什么。其实劳动和受教育本身就是权利与义务的统一，行使权利也有边界。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "你能上学，是因为国家保障了你的受教育权；可你要按时到校、认真完成学业——同一件事，一面是权利，一面是义务。"},
    {"lens": "解释它", "text": "为什么权利和义务分不开？因为每一项权利的实现，都要靠别人承担相应的义务；反过来，你履行义务，也在守护别人的权利。"},
    {"lens": "迁移它", "text": "这套想法在班里天天都用得上：你有在课上发言的权利，也有认真听别人发言的义务。只想自己说、不肯听别人说，课就上不下去了。"},
])}
    ''', tag="概念二"))

    judge_btns = "\n".join(
        f'            <button class="choice" data-jd-item="{j["k"]}" style="text-align:left">'
        f'<strong>{j["n"]}</strong><br><span style="color:var(--muted);font-size:14px">{j["case"]}</span></button>'
        for j in JUDGE
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "★动手二：「我是小公民」情境判断台", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">读一个情境，再从三个选项里选一个：这是在行使权利、在履行义务，还是这样做不妥。选完马上看到解释。</p>
        <div class="lab-panel">
          <div id="jd-stage">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 挑一个情境</div>
            <div class="grid">
{judge_btns}
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">判断进度</span><span class="v" id="jd-score">已经判断 0 / 6 个情境</span></div>
          </div>
          <p class="result warn" id="jd-out" style="margin-top:12px">先点一个情境。</p>
          <div id="jd-panel"></div>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🙋</span><div><strong>记住两句话：</strong>权利和义务相互依存、相互促进；行使自由和权利不得损害他人的合法权益。想清楚这两句，六个情境都能判断。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：权义账单校对，五条说法哪条要改", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>班里要做一期「我是小公民」的展板，几位同学写了五条说法。请你当一次校对员，判断哪一条正确、哪一条必须改。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>说法一（必须改）：</strong>「权利是我想行使就行使，义务可以等到长大以后再履行。」权利和义务相互依存、相互促进，不能只享受权利而不履行义务。</div></div>
          <div class="step"><span class="n">2</span><div><strong>说法二（正确）：</strong>「受教育既是我们的权利，也是我们的义务。」很多权利和义务本来就是一件事的两面。</div></div>
          <div class="step"><span class="n">3</span><div><strong>说法三（必须改）：</strong>「转发没核实的消息也是在行使言论自由，别人管不着。」行使权利不能损害他人的人格尊严。</div></div>
          <div class="step"><span class="n">4</span><div><strong>说法四（正确）：</strong>「依法纳税是公民的义务，国家依法征收的税款用在公共事业上。」</div></div>
          <div class="step"><span class="n green">5</span><div><strong>说法五（正确）：</strong>「中华人民共和国公民在法律面前一律平等。」平等权是一项很重要的基本权利。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学把权利和义务<strong>搞混</strong>成两件互不相干的事，觉得可以只挑权利那一半；也有的同学把行使权利<strong>误认为</strong>想做什么就做什么。记住两句话就够了：权利与义务相互依存；行使权利有边界。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三句话，藏着三个容易想歪的地方", TTS["conceptest-1"], [
        {"q": "关于公民身份的取得，下面哪句话说得准确？",
         "options": [("父母双方或一方为中国公民，本人出生在中国，具有中国国籍", True),
                     ("只要在中国居住满一段时间，就自动成为中国公民", False),
                     ("国籍可以自己选择，一个人可以同时拥有两国国籍并都被承认", False)],
         "explain": "国籍的取得主要有因出生取得和因申请加入取得两种方式；我国不承认中国公民具有双重国籍。"
                    "<strong>错因提醒：</strong>常见错误是把「居住」和「具有国籍」<strong>搞混</strong>了，或者<strong>误认为</strong>双重国籍也被承认。",},
        {"q": "小美按时到校上课、认真完成作业，这件事说明：",
         "options": [("受教育既是她的权利，也是她的义务", True),
                     ("受教育只是她的权利，跟义务无关", False),
                     ("受教育只是她的义务，跟权利无关", False)],
         "explain": "受教育是国家保障的权利，也是公民应当履行的义务，两者是同一件事的两面。"
                    "<strong>错因提醒：</strong>有的同学把权利和义务<strong>搞混</strong>成两件分开的事，只看到其中一面——这就说不完整了。",},
        {"q": "小刚在班级群里转发了「某某同学偷了东西」这条没有核实的消息。下面哪种说法更合适？",
         "options": [("这样不妥，行使自由和权利不得损害他人的合法权益", True),
                     ("这是在正确行使言论自由，别人管不着", False),
                     ("这只是同学之间的玩笑，和公民的权利义务没关系", False)],
         "explain": "公民在行使自由和权利的时候，不得损害国家的、社会的、集体的利益和其他公民的合法的自由和权利，人格尊严受法律保护。"
                    "<strong>错因提醒：</strong>有的同学<strong>误认为</strong>言论自由就是想说什么就说什么。还可以试试：先核实，再决定要不要转发。",}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：小公民行动卡生成台", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">三步各选一个：<strong>我想推动的问题 → 这件事和哪一项权利有关 → 我打算承担的义务与行动</strong>。选完，你就有了自己的行动卡。</p>
        <div class="lab-panel">
          <div id="ac-stage"></div>
          <div id="ac-panel"></div>
          <p class="result warn" id="ac-out" style="margin-top:12px">从第一步开始选。</p>
        </div>
        <div class="inner-card" style="margin-top:14px">
          <p><strong>把它写下来：</strong></p>
          <p style="color:var(--muted)">在小公民的身份里，你最想为身边的人做哪一件小事？把它写成一句话，并写清这件事和哪一项权利有关。</p>
          <textarea id="syn-answer" rows="3" placeholder="我想为……做一件小事：……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，说法还准不准", TTS["posttest"], [
        {"q": "小宇翻开家里的户口本，看到自己登记在上面。关于他的公民身份，下面哪种说法准确？",
         "options": [("他具有中华人民共和国国籍，是中华人民共和国公民，在法律面前一律平等", True),
                     ("他还是小学生，要等长大以后才是公民", False),
                     ("户口本只是家庭记录，和公民身份没有关系", False)],
         "explain": "我国公民是指具有中华人民共和国国籍的人；公民在法律面前一律平等，与年龄无关。"
                    "<strong>错因提醒：</strong>常见错误是<strong>误认为</strong>「小孩子还不算公民」。其实我们已经是小公民了。",},
        {"q": "社区要建一个小花园，大家商量着一起动手。从公民权利和义务的角度看，下面哪种说法更合适？",
         "options": [("我们可以表达意见、参与商量，也要爱护公共财产、遵守公共秩序", True),
                     ("我们只要享受花园带来的好处，不用出任何力", False),
                     ("花园是公共的，谁都可以随意破坏，反正不是自己的", False)],
         "explain": "公民有表达意见、参与公共事务的权利，也有爱护公共财产、遵守公共秩序、尊重社会公德的义务，两者是一致的。"
                    "<strong>错因提醒：</strong>有的同学把权利和义务<strong>搞混</strong>成「只要好处不尽责任」，这样公共的事就做不成了。",},
        {"q": "同学说：「劳动和受教育，我现在都做到了，那它们到底算权利还是算义务？」下面哪种回答最好？",
         "options": [("两者都是：它们既是我们的权利，也是我们的义务", True),
                     ("只算权利，因为上学是我自己的事", False),
                     ("只算义务，因为都是别人要求我做的", False)],
         "explain": "劳动和受教育既是公民的权利，也是公民的义务，这是权利与义务一致性的典型例子。"
                    "<strong>错因提醒：</strong>容易把「既是权利又是义务」<strong>误认为</strong>只能选一边。还可以试试：把「国家保障我」和「我应该做到」两句话都读一遍。",}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：我是谁、我有什么权利、我要做什么", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>我是谁：</strong>我国公民是指具有中华人民共和国国籍的人；国籍的取得主要有因出生取得和因申请加入取得两种方式。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>我有什么权利：</strong>法律面前一律平等；政治权利和自由、人身自由与人格尊严不受侵犯、受教育权、劳动权等。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>我要做什么：</strong>遵守宪法和法律，维护国家统一和民族团结，依法服兵役，依法纳税；劳动和受教育同时也是义务。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>一句最要紧的话：</strong>权利和义务相互依存、相互促进，行使自由和权利不得损害他人的合法权益。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>一句口诀：</strong>国籍连国家，公民就是我；权利有保障，义务也担着；两面一件事，行使有边界。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「国籍」和「基本义务」这两个词，给家里人讲一件今天学到的事，并说说权利和义务为什么分不开。</p>
          <p style="color:var(--muted)">再动一动手：<strong>写一写</strong>四项基本权利和四项基本义务，每一项都用一句话说明它在生活里是什么样子。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写出我国公民是指什么样的人，再写出国籍取得的两种主要方式。",
            "写出四项公民的基本权利，每项一句话。",
            "写出四项公民的基本义务，每项一句话。",
        ],
        [
            "把「受教育」和「劳动」这两件事各写两句话：一句说明它作为权利是什么样子，一句说明它作为义务是什么样子。",
            "写一句话说明行使自由和权利的边界在哪里，并举一个生活里的例子。",
        ],
        [
            "做一张小公民行动卡：写清楚你想推动的一个问题、它与你哪一项权利有关、你打算承担哪一项义务或者做哪一件具体的事，做完在班里交流。",
            "回家采访一位家里人：问问他觉得哪一项公民义务最重要、为什么，把他的话记下来，再说说你的想法。",
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
    "title": "我们是公民",
    "name_en": "We Are Citizens",
    "grade": 6,
    "grade_cn": "六年级",
    "domain": "tradition-culture",
    "domain_cn": "中华优秀传统文化",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学六年级的道德与法治课，正对统编六上第 2 单元「我们是公民」（公民意味着什么、公民的基本权利和义务），落到三件事上。第一件是公民意味着什么：我国公民是指具有中华人民共和国国籍的人；国籍的取得主要有因出生取得和因申请加入取得两种方式，其中因出生取得最常见——父母双方或一方为中国公民，本人出生在中国，具有中国国籍，父母双方或一方为中国公民、本人出生在外国的也具有中国国籍，但有法定例外情形，我国不承认中国公民具有双重国籍；公民身份意味着受国家保护，也意味着在法律面前一律平等。第二件是公民的基本权利：法律面前一律平等，选举权和被选举权，言论、出版、集会、结社、游行、示威的自由与宗教信仰自由，人身自由、人格尊严、住宅不受侵犯，通信自由和通信秘密受法律保护，对国家机关和国家工作人员提出批评和建议的权利，劳动、休息、受教育的权利，进行科学研究、文学艺术创作和其他文化活动的自由。第三件是公民的基本义务与两者的关系：维护国家统一和全国各民族团结，遵守宪法和法律、保守国家秘密、爱护公共财产、遵守劳动纪律、遵守公共秩序、尊重社会公德，维护祖国的安全、荣誉和利益，保卫祖国、依法服兵役，依法纳税，劳动和受教育同时也是义务；在我国，公民的权利和义务相互依存、相互促进，公民既是合法权利的享有者，又是法定义务的承担者，不能只享受权利而不履行义务，也不能只要求履行义务而忽视权利的保障；同时明确一条边界——公民在行使自由和权利的时候，不得损害国家的、社会的、集体的利益和其他公民的合法的自由和权利。三个互动台子都能真操作，反馈一律写成「这样可能会……，还可以试试……」：动手一是本课核心模拟「权利与义务配对台」（六张权利卡与六张义务卡配对，配出受教育权与受教育义务、劳动权与劳动义务等对应关系）、动手二是本课核心模拟「我是小公民」情境判断台（六个校园与家庭情境，判断属于行使权利、履行义务还是这样做不妥），综合任务是「小公民行动卡」生成台（问题 → 对应权利 → 对应义务与行动，合成一张可贴上展板的行动卡）。全课表述从严：法律名称一律写全称，《中华人民共和国宪法》与《中华人民共和国国籍法》严格区分；不出现任何法律条文编号，不臆造案例细节与办理流程；权利与义务的举例只用常识层面、不会有争议的内容；插图一律为中性简洁扁平教学插画，不使用真人照片风格，不绘制国旗、国徽、宪法文本封面等易失真、不庄重的图形，涉及公民身份与权利义务改用徽章圆环、人物剪影、天平、握手、齿轮等抽象符号与地标性建筑抽象剪影。",
    "tags": ["我们是公民", "公民意味着什么", "公民的基本权利和义务", "国籍", "受教育权与受教育义务", "权利与义务的一致性", "六年级", "道德修养"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学「法治启蒙与公民意识」——了解宪法是国家的根本法，知道公民的基本权利和义务，树立法治观念；对应统编《道德与法治》六年级上册 第2单元「我们是公民」：公民意味着什么、公民的基本权利和义务。",
    "hero_question": "「我是中国公民」这句话，到底意味着什么？",
    "hero_alt": "我们是公民知识结构图：我是中国公民、我的基本权利、我的基本义务 三栏，用徽章圆环、人物剪影、天平与握手等抽象符号表示，附中文标注，不含国旗国徽与宪法文本图形",
    "hero_caption": "我们是公民：国籍把我和国家连在一起 · 享有基本权利 · 承担基本义务 · 权利与义务相互依存",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "我是怎样成为一个中国公民的？", "d": "国籍是怎么取得的，公民身份意味着什么", "v": "我是怎样成为一个中国公民的"},
        {"t": "我有哪些基本权利？", "d": "平等、受教育、人格尊严……这些权利从哪里来", "v": "我有哪些基本权利"},
        {"t": "我要履行哪些基本义务？", "d": "遵守宪法和法律、依法纳税、依法服兵役……", "v": "我要履行哪些基本义务"},
        {"t": "权利和义务到底是什么关系？", "d": "为什么说它们常常是一件事的两面", "v": "权利和义务到底是什么关系"},
    ],
    "objectives": [
        "能说出我国公民是指具有中华人民共和国国籍的人，能说出国籍的取得主要有因出生取得和因申请加入取得两种方式，知道我国不承认中国公民具有双重国籍",
        "能说出几项公民的基本权利：法律面前一律平等、受教育权、人格尊严不受侵犯、选举权和被选举权等",
        "能说出几项公民的基本义务：遵守宪法和法律、维护国家统一和全国各民族团结、依法服兵役、依法纳税，知道劳动和受教育同时也是义务",
        "能说出权利和义务相互依存、相互促进，不能只享受权利而不履行义务，也能说出行使自由和权利不得损害他人的合法权益",
    ],
    "objectives_plain": [
        "能说出我国公民是指什么样的人，以及国籍取得的两种主要方式",
        "能说出几项公民的基本权利",
        "能说出几项公民的基本义务",
        "能说出权利和义务相互依存、相互促进，并知道行使权利有边界",
    ],
    "standards": [
        {"content": "了解宪法是国家的根本法，知道公民的基本权利和义务，树立法治观念。",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学 法治启蒙与公民意识"},
        {"content": "公民意味着什么；公民的基本权利和义务",
         "source": "统编《道德与法治》六年级上册 第2单元「我们是公民」"},
    ],
    "prereqs": ["pol-e-g6-u1"],
    "prereqs_name": "我们的守护者",
    "prereqs_meta": "pol-e-g6-u1",
    "leads_to": ["pol-e-g6-u3"],
    "next_meta": "pol-e-g6-u3",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "三件事：我是怎样成为中国公民的、我有什么权利、我要做什么。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能把一件和公民身份有关的事说清楚。",
        "objectives": "看清四件事：公民是什么、国籍怎么取得、基本权利有哪些、基本义务有哪些。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "记住一句话：我国公民是指具有中华人民共和国国籍的人；国籍的取得有因出生取得和因申请加入取得。",
        "lab-1": "先点权利卡，再点义务卡。想一想：这项权利要成立，需要每个人做到什么。",
        "module-2": "权利与义务相互依存、相互促进；劳动和受教育既是权利也是义务；行使权利有边界。",
        "lab-2": "先读情境，再判断属于行使权利、履行义务还是这样做不妥。注意受教育是两面。",
        "worked-example": "五条说法：三条正确、两条必须改。留意「等长大再履行义务」和「转发没核实的消息」。",
        "conceptest-1": "三句话里各藏着一个容易想歪的地方，选完把解释读一遍。",
        "synthesis": "三步做行动卡：问题 → 对应的权利 → 对应的义务与行动。",
        "posttest": "出现了户口本、社区花园和同学的提问，看看今天的说法还用不用得上。",
        "summary": "四句话：我是谁、我有什么权利、我要做什么、权利与义务分不开。",
        "homework": "三层小任务，先做前两层；第二层要把「两者都是」说清楚。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学道德与法治「法治启蒙与公民意识」板块在六年级的空缺，正对统编六上第 2 单元「我们是公民」（公民意味着什么、公民的基本权利和义务）。六年级学生已经知道自己是中国人，也常用「权利」「义务」这两个词，但对「我怎样成为一个中国公民」「我到底有哪些基本权利」「权利和义务为什么分不开」往往只有模糊印象，容易出现三类典型偏差：误认为居住在中国就是中国公民或者误认为小孩子还不算公民；误认为受教育只是权利、纳税只是义务，看不到两面；误认为行使权利可以不顾他人。所以全课不讲口号、不背条文，而把内容换成能核对、能复述的常识与可操作的活动。第一层是「公民意味着什么」：给出我国公民的界定——具有中华人民共和国国籍的人；说明国籍取得的两种主要方式，其中因出生取得最常见：父母双方或一方为中国公民，本人出生在中国，具有中国国籍；父母双方或一方为中国公民、本人出生在外国的也具有中国国籍，但有法定例外情形；并明确我国不承认中国公民具有双重国籍；最后落到公民身份的两重含义：受国家保护，在法律面前一律平等。第二层是「公民的基本权利与基本义务」：把小学阶段应当知道的几项权利与几项义务分栏讲清，权利一侧包括平等权、政治权利和自由、人身自由与人格尊严不受侵犯、批评建议权、劳动与休息权、受教育权、文化活动自由；义务一侧包括维护国家统一和全国各民族团结，遵守宪法和法律、保守国家秘密、爱护公共财产、遵守劳动纪律、遵守公共秩序、尊重社会公德，维护祖国的安全、荣誉和利益，保卫祖国、依法服兵役，依法纳税，劳动和受教育同时也是义务。第三层是「两者的关系」：权利和义务相互依存、相互促进，公民既是合法权利的享有者，又是法定义务的承担者，不能只享受权利而不履行义务，也不能只要求履行义务而忽视权利的保障；特别强调劳动和受教育既是权利也是义务；并明确一条边界——公民在行使自由和权利的时候，不得损害国家的、社会的、集体的利益和其他公民的合法的自由和权利。三个互动台子都能真操作，反馈一律写成「这样可能会……，还可以试试……」：动手一是本课核心模拟「权利与义务配对台」，六张权利卡与六张义务卡配对，配出受教育权与受教育义务、劳动权与劳动义务、言论自由与尊重他人人格尊严等对应关系，配错给出错因与下一步提示；动手二是本课核心模拟「我是小公民」情境判断台，六个校园与家庭情境，判断属于行使权利、履行义务还是这样做不妥，每个情境都配错因提醒；综合任务是「小公民行动卡」生成台，学生按「问题 → 对应权利 → 对应义务与行动」各选一步，由系统合成一张可以贴上展板的行动卡。全课在表述上从严把关：法律名称一律写全称并严格区分；不出现任何法律条文编号，不臆造案例细节与办理流程；权利与义务的举例只用常识层面、不会有争议的内容；插图一律为中性简洁扁平教学插画，不使用真人照片风格，不绘制国旗、国徽、宪法文本封面等易失真、不庄重的图形，涉及公民身份与权利义务改用徽章圆环、人物剪影、天平、握手、齿轮等抽象符号与地标性建筑抽象剪影。",
    "plan_table": """| 1 | cover | 我们是公民 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：我是一名小公民吗？ | 起·前测（暴露已有印象与混淆点） |
| 5 | concept | 公民意味着什么：我是怎样成为一个中国公民的 | 承·概念一（国籍的取得与公民身份） |
| 6 | interactive | ★动手一：权利与义务配对台，把两半配成一件 | 承·核心模拟（6 权利卡 × 6 义务卡） |
| 7 | concept | 公民的基本权利与基本义务，还有它们的关系 | 承·概念二（权利、义务与一致性） |
| 8 | interactive | ★动手二：「我是小公民」情境判断台 | 承·核心模拟（6 情境 × 三选一判断） |
| 9 | concept | 例题示范：权义账单校对，五条说法哪条要改 | 转·重难点突破（权利与义务的一致性 + 行使权利的边界） |
| 10 | quiz | 概念测试：三句话，藏着三个容易想歪的地方 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：小公民行动卡生成台 | 合·迁移应用（三步合成行动卡） |
| 12 | quiz | 后测：换几个新情境，说法还准不准 | 合·后测 |
| 13 | summary | 小结：我是谁、我有什么权利、我要做什么 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：我是中国公民 / 我的基本权利 / 我的基本义务 三栏，用徽章圆环、人物剪影、天平与握手等抽象符号表示，附中文标注\n- P5 公民身份取得抽象示意图（已生成）：父母与孩子的人物剪影 + 圆环徽章标注中华人民共和国国籍，下方标注因出生取得与因申请加入两种方式，并标注「抽象示意图，不按比例」\n- P7 权利与义务关系概念图（已生成）：一架天平，左托盘标注权利、右托盘标注义务，中央标注相互依存、相互促进，两侧用握手与齿轮的抽象符号连接\n- ★ 全课不绘制国旗、国徽、宪法文本封面等易失真、不庄重的图形；涉及公民身份与权利义务仅用徽章圆环、人物剪影、天平、握手、齿轮等抽象符号与地标性建筑抽象剪影\n- ★ 表述口径统一：法律名称一律写全称；不出现任何法律条文编号；不臆造案例细节与办理流程；权利与义务的举例只用常识层面、不会有争议的内容\n- 三张图均为中性简洁扁平教学插画，不使用真人照片风格，不含可识别的真实人物",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
