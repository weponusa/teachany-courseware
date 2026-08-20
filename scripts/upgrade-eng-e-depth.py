#!/usr/bin/env python3
"""Add topic-specific depth modules to eng-e shell courses.

Elementary English courses often pass via template sections but lack
topic-specific core teaching. Each course gets 知识精讲 + 方法范例
(worked example + diagnostic + 常见误区). No mp4. Idempotent via id="lesson-focus".
Bilingual: Chinese explanation + English examples, appropriate for 小学英语.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_VERSION = "1.1.0"
UPDATED_AT = "2026-08-20"


def C(ct, cb, mt, mb, ex, q, opts, correct, fb, pit):
    return dict(
        concept_title=ct, concept_body=cb, method_title=mt, method_body=mb,
        example=ex, question=q, options=opts, correct=correct, feedback=fb, pitfall=pit,
    )


COURSES = {
    "eng-e-alphabet": C(
        "英语字母表 ABC",
        "英语有 26 个字母，分大写与小写。字母是拼读单词的基础：先认形、记名（letter name），再学发音。按顺序唱字母歌，能帮助记忆位置，也为查词典打基础。",
        "方法：认形→唱名→书写",
        "每天跟读字母歌；对比易混字母 b/d、p/q、m/n；写时注意起笔与占格。",
        "A a, B b, C c … Z z. 例：apple 以 A 开头。",
        "英语字母一共有多少个？",
        ["24", "26", "28", "30"],
        1,
        "英语有 26 个字母。",
        "常见误区是只背字母名，不练书写与易混字母区分。",
    ),
    "eng-e-asking-directions": C(
        "问路与指路",
        "问路常用 Excuse me. / Where is …? / How can I get to …? 指路用 go straight, turn left/right, across from, next to。礼貌用语与关键路标词是重点。",
        "方法：先礼貌→再问地点→听关键词",
        "抓住 left/right/straight/near；听完复述路线。回答可用：Go straight and turn left.",
        "A: Excuse me, where is the library? B: Go straight and turn right.",
        "“向左转”用英语怎么说？",
        ["go straight", "turn left", "sit down", "open the door"],
        1,
        "turn left 表示向左转。",
        "常见误区是 left/right 说反，或问路忘记 Excuse me。",
    ),
    "eng-e-consonant-sounds": C(
        "英语辅音发音",
        "辅音是气流受阻发出的音，如 /b/ /p/ /t/ /d/ /k/ /g/。学习时注意清浊对立（p/b、t/d）与口型位置，结合单词跟读比孤立记符号更有效。",
        "方法：最小对立词对比",
        "用 pat/bat、cap/gap 等成对词听辨；用手感受嗓子振动判断清浊。",
        "pen /p/ 与 ben /b/：一个不振动，一个振动。",
        "辅音学习中，清音与浊音的主要区别是？",
        ["字母个数", "声带是否振动", "必须大写", "只能在句末"],
        1,
        "清浊主要看声带是否振动。",
        "常见误区是用中文近似音硬套，导致 p/b、l/n 等长期混淆。",
    ),
    "eng-e-daily-topics-basic": C(
        "日常话题基础",
        "小学日常话题包括天气、爱好、食物、周末活动等。每个话题记住核心问句与 5–8 个高频词，并能用 I like … / I have … / It is … 简单回答。",
        "方法：话题三件套",
        "每话题记：1 个问句 + 一组词 + 2 句自己的答语。课上用角色扮演巩固。",
        "Q: What's the weather like? A: It's sunny. I like sunny days.",
        "谈论爱好时，常用哪一句？",
        ["How old are you?", "I like reading.", "Where is the park?", "Turn left."],
        1,
        "I like … 常用来谈爱好。",
        "常见误区是只会背单词表，不会用完整句回答话题问题。",
    ),
    "eng-e-future-simple": C(
        "一般将来时（小学）",
        "一般将来时表示将要发生的事，小学常用 will + 动词原形，或 be going to + 动词原形。时间词如 tomorrow, next week, soon 是重要线索。",
        "方法：找时间词→选 will / be going to",
        "明天计划：I will … / I'm going to …。否定：will not (won't)。疑问：Will you …?",
        "I will visit my grandma tomorrow. / She is going to play football next week.",
        "表示明天要发生的动作，常用？",
        ["am playing now", "will / be going to", "played yesterday", "have done"],
        1,
        "将来用 will 或 be going to。",
        "常见误区是 will 后加 -ing，或 be going to 漏掉 be。",
    ),
    "eng-e-greetings-classroom": C(
        "课堂用语",
        "课堂用语帮助听懂老师指令并礼貌回应，如 Stand up. / Sit down. / Open your books. / Listen carefully. / May I come in? 听清动词是关键。",
        "方法：听动词→做动作",
        "老师说指令时先抓动词；回答用 Yes. / OK. / Here you are. 等简短礼貌语。",
        "Teacher: Open your books, please. Student: OK.",
        "老师说 Sit down 时，你应该？",
        ["站起来", "坐下", "关门", "跑步"],
        1,
        "Sit down 表示坐下。",
        "常见误区是只背中文意思，听到英文指令反应慢或做错动作。",
    ),
    "eng-e-greetings-intro": C(
        "问候与自我介绍",
        "见面问候用 Hello / Hi / Good morning。自我介绍常用 I'm … / My name is … / I'm … years old. / Nice to meet you. 注意礼貌与完整句。",
        "方法：问候→姓名→年龄→再见",
        "先说 Hello，再说 I'm Tom. I'm 9. Nice to meet you. 分别用 Goodbye / See you.",
        "A: Hello! I'm Lily. B: Hi, Lily. Nice to meet you.",
        "自我介绍时说自己的名字，常用？",
        ["Where are you?", "My name is … / I'm …", "Turn right", "How much is it?"],
        1,
        "My name is … 或 I'm … 用来介绍自己。",
        "常见误区是只说单词不说完整句，或 Nice to meet you 用不完整。",
    ),
    "eng-e-listening-speaking": C(
        "小学听说入门",
        "听说课先听懂关键词（who/what/where），再用完整短句说出来。听前看图预测，听中抓核心词，说时注意语音语调，不怕说错。",
        "方法：听关键词→跟读→替换造句",
        "听两遍：第一遍大意，第二遍细节。跟读后把人名、地点换成自己的信息。",
        "听：Tom is in the park. → 说：Tom is in the park. / I am in the classroom.",
        "听力时最应优先抓住的是？",
        ["每个生词都查词典", "人物、地点、动作等关键词", "只看选项不听", "放弃不听"],
        1,
        "关键词帮助快速理解大意。",
        "常见误区是逐词翻译导致跟不上，或不敢开口只听不说。",
    ),
    "eng-e-nouns-articles": C(
        "名词与冠词（小学）",
        "名词表示人或物，可数名词有单复数（book/books）。冠词 a/an 用于可数单数“某一个”，the 表特指。元音音素开头用 an（an apple）。",
        "方法：先判单复数，再选 a/an/the",
        "一个：a/an + 单数；特指：the；复数常可不用 a。注意 an hour（h 不发音）。",
        "I see a cat. The cat is black. / an egg, a book.",
        "apple 前常用哪个冠词？",
        ["a", "an", "一律不用", "只能 the"],
        1,
        "apple 以元音音素开头，用 an。",
        "常见误区是按字母不是按发音选 a/an，或可数单数前漏冠词。",
    ),
    "eng-e-numbers-colors": C(
        "数字与颜色",
        "数字 one–ten（及更大数）用于数数、年龄与电话；颜色 red, blue, yellow, green 等描述事物。常结合 How many …? / What colour is …?",
        "方法：数一数 + 涂一涂",
        "用实物数数说英文；看物品说颜色：It's red. There are three pencils.",
        "I have two red apples. / What colour is it? It's blue.",
        "“三个”用英语说是？",
        ["two", "three", "tree", "free"],
        1,
        "three 表示三。",
        "常见误区是 thirteen/thirty 等易混，或颜色词当名词乱加复数。",
    ),
    "eng-e-passage-questions": C(
        "短文阅读答题",
        "小学短文题先读问题再读文章，带着问题找答案。常见题型：找细节、判断正误、选标题。答案一般能在文中直接找到或简单推断。",
        "方法：读题→圈关键词→回文定位",
        "把问题中的人名、时间、地点圈出来，到文中找相同或近义表达，再选答案。",
        "Q: Where is Amy? 文中：Amy is at school. → 答案 at school.",
        "做阅读理解时，较好的第一步是？",
        ["不看题直接乱选", "先读问题再读文章找关键信息", "只看最后一句", "翻译每一个词才开始"],
        1,
        "先读题能带着目标找信息。",
        "常见误区是凭感觉选，不回原文核对。",
    ),
    "eng-e-past-simple": C(
        "一般过去时（小学）",
        "一般过去时表示过去发生的事。规则动词加 -ed（played）；不规则要记（go→went, see→saw）。时间词：yesterday, last week, ago。",
        "方法：找过去时间→动词变过去式",
        "肯定：I played … / She went …。否定：didn't + 原形。疑问：Did you …?",
        "I visited my aunt yesterday. / He didn't go to school last Monday.",
        "yesterday 的句子，动词常用？",
        ["原形或 -ing 表示现在", "过去式", "will + 原形", "have + 过去分词必须"],
        1,
        "过去时间用过去式。",
        "常见误区是否定句写成 didn't went，或规则/不规则混淆。",
    ),
    "eng-e-phonics-blends": C(
        "辅音组合（blends）",
        "辅音组合是两个或多个辅音连在一起发，如 bl, cl, fl, br, tr, st。每个音仍能听出来，只是连得快。掌握 blends 有助于更快拼读生词。",
        "方法：分音→连读→整词",
        "先分别读 /b/+/l/，再连成 bl；再读 black, blue, block。",
        "bl → black；tr → tree；st → stop.",
        "black 开头的辅音组合是？",
        ["sh", "bl", "th", "ng"],
        1,
        "black 以 bl 开头。",
        "常见误区是把 blend 当成一个全新单音，或漏读其中一个辅音。",
    ),
    "eng-e-phonics-consonants": C(
        "自然拼读：辅音",
        "自然拼读中，辅音字母多数有较稳定发音，如 b→/b/, t→/t/, s→/s/。先认字母音（sound），再与元音拼成词，比只记中文意思更能独立认读。",
        "方法：见字→出声→拼词",
        "指着字母说音：c-/k/, a-/æ/, t-/t/ → cat。每天练 5 个辅音+熟词。",
        "m → /m/ → map, mom, milk.",
        "自然拼读中学习辅音，重点是？",
        ["只背字母中文名", "字母常见发音并能拼读", "只抄写不发音", "取消朗读"],
        1,
        "要掌握字母音并用于拼读。",
        "常见误区是用汉字注音，或混淆 letter name 与 letter sound。",
    ),
    "eng-e-phonics-rules": C(
        "常见拼读规则",
        "小学常见规则：闭音节短元音（cat）、开音节/魔 e 长元音（cake）、辅音字组合 sh/ch/th。规则帮助猜读，但仍有例外要积累。",
        "方法：看结构选规则",
        "一词一辅元辅→短元音；元音+辅音+e→前面元音常发字母名。sh 一起读 /ʃ/。",
        "hat（短 a）/ hate（长 a）；ship 中 sh=/ʃ/。",
        "cake 中的魔 e（silent e）常使前面元音？",
        ["变短", "发字母名（长音）", "不发音且无影响", "变成辅音"],
        1,
        "silent e 常使前面元音发长音。",
        "常见误区是把所有词硬套一条规则，忽略例外词要单独记。",
    ),
    "eng-e-phonics-vowels": C(
        "自然拼读：元音",
        "元音 a e i o u 有短音与长音。短音如 cat, pen, sit；长音常如 cake, me, like（接近字母名）。分清长短元音能减少认读错误。",
        "方法：短长对比听读",
        "成对练：cap/cape, bit/bite。先听再跟读，看唇形开口大小。",
        "a 短音：apple；a 长音：name, cake.",
        "cat 中的 a 通常是？",
        ["长元音（字母名）", "短元音", "不发音", "辅音"],
        1,
        "cat 是闭音节，a 发短音。",
        "常见误区是长短元音不分，导致 ship/sheep 类词读错。",
    ),
    "eng-e-prepositions": C(
        "方位介词",
        "小学常用方位介词：in（在……里）, on（在……上）, under（在……下）, near（在……附近）, between（在……之间）。结合图片与动作记忆最牢。",
        "方法：指物说介词",
        "把橡皮放在书上说 on；放进铅笔盒说 in；藏到桌下说 under。造句：The ball is under the desk.",
        "The cat is on the box. / The book is in the bag.",
        "“在盒子里面”用？",
        ["on the box", "in the box", "under the box only", "between 必须"],
        1,
        "里面用 in。",
        "常见误区是 in/on 不分，或只记中文不练空间位置。",
    ),
    "eng-e-present-continuous": C(
        "现在进行时（小学）",
        "现在进行时表示正在做的事，结构是 be (am/is/are) + 动词-ing。标志词：now, look, listen。注意 drop→dropping, run→running 等双写，以及 e 结尾去 e 加 -ing。",
        "方法：看 now→选 be + doing",
        "I am reading. He is playing. They are running. 否定在 be 后加 not。",
        "Look! The boys are playing football now.",
        "现在进行时的基本结构是？",
        ["will + 原形", "be + 动词-ing", "have + 过去分词", "动词原形 alone"],
        1,
        "am/is/are + doing。",
        "常见误区是漏掉 be，或 He play football now 忘记 -ing。",
    ),
    "eng-e-present-simple": C(
        "一般现在时（小学）",
        "一般现在时表示习惯、事实。主语是 I/you/we/they 用动词原形；he/she/it 用动词 +s/-es。标志词：every day, usually, often, always。",
        "方法：看主语是否第三人称单数",
        "I like apples. She likes apples. 否定：don't / doesn't + 原形。疑问：Do/Does …?",
        "He goes to school every day. / They play basketball on Sundays.",
        "She ______ milk every morning.（like）",
        ["like", "likes", "liking", "liked"],
        1,
        "第三人称单数用 likes。",
        "常见误区是 he/she 后忘记加 -s，或否定句写成 doesn't likes。",
    ),
    "eng-e-pronouns-be-verbs": C(
        "代词与 be 动词",
        "人称代词 I/you/he/she/it/we/they 要与 be 动词搭配：I am, you/we/they are, he/she/it is。物主代词 my/your/his/her 后接名词。这是造句的基础。",
        "方法：先选代词再配 be",
        "说自己用 I am；说他用 He is；说我们用 We are。My name is … / Her bag is red.",
        "I am a student. She is my friend. They are in Class 3.",
        "He 后面的 be 动词用？",
        ["am", "is", "are", "be 原形直接"],
        1,
        "he/she/it 配 is。",
        "常见误区是 I is / He are，或 my/I 混用（I name is 错误）。",
    ),
    "eng-e-reading-skills-primary": C(
        "小学阅读技巧",
        "小学阅读重在抓住大意与关键细节。先看标题与插图预测，再读文；遇到生词先跳过，靠上下文猜。读完能用一句话说“谁做了什么”。",
        "方法：看图预测→读文找谁/哪/做什么",
        "边读边在人物、地点下划线；读完合书复述一句。标题题选“最概括”的选项。",
        "标题 Cats Like Fish，文中讲猫爱吃鱼 → 大意与标题一致。",
        "阅读时遇到个别生词，较好做法是？",
        ["立刻放弃全文", "先跳过并结合上下文猜测", "每个词都查完才读下一句且永不猜", "只看生词不看句子"],
        1,
        "先跳过、靠上下文猜更利于理解大意。",
        "常见误区是逐词死抠，读完仍说不出文章大意。",
    ),
    "eng-e-short-passage": C(
        "短文阅读入门",
        "短文通常有主题句与几句细节。读短文要知道：谁（who）、在哪（where）、做什么（what）。能回答这三个问题，就基本读懂了。",
        "方法：三问阅读法",
        "读完自问 Who? Where? What? 用文中词回答。可画简图帮助记忆情节。",
        "Tom is in the zoo. He sees a panda. → Who: Tom; Where: zoo; What: sees a panda.",
        "读懂短文最基本的三要素通常是？",
        ["字体、页码、价格", "人物、地点、事件", "只记生词表", "作者年龄"],
        1,
        "who/where/what 帮助把握大意。",
        "常见误区是只盯生词，忽略人物与情节。",
    ),
    "eng-e-simple-sentences": C(
        "简单句型",
        "小学常用简单句：主系表（I am happy.）、主谓（Birds fly.）、主谓宾（I like apples.）。先保证有主语和动词，再添加时间地点。",
        "方法：主谓齐全再扩展",
        "先写 I like …，再加 very much / on Sundays。问句注意 Do/Does/Is/Are 开头。",
        "I am a pupil. / She has a bag. / We play in the park.",
        "一个简单句通常至少需要？",
        ["只有形容词", "主语和动词（谓语）", "三个从句", "必须有 will"],
        1,
        "主语+谓语是简单句基础。",
        "常见误区是中式堆词无动词，如 I happy（应 I am happy）。",
    ),
    "eng-e-simple-writing": C(
        "简单写作（小学）",
        "小学写作要求写出完整、正确的短句，围绕提示把要点写全。注意首字母大写、句末标点、人称与 be/时态一致。先说后写更顺利。",
        "方法：看提示→口头造句→写下检查",
        "每条提示写 1 句；用 and 连接两句；写完检查大写、句号与 is/are。",
        "My name is Amy. I am 10. I like music.",
        "写作时每句开头一般要？",
        ["小写任意", "大写", "必须用问号", "不加标点"],
        1,
        "英文句子开头要大写。",
        "常见误区是中式语序硬译，或漏写提示中的要点。",
    ),
    "eng-e-story-retelling": C(
        "故事复述",
        "故事复述按时间顺序讲：开头（谁/哪）→中间（发生什么）→结尾（结果）。用 First, Then, Finally 连接，尽量用学过的短句。",
        "方法：三步时间线",
        "画三格漫画：开始、经过、结果；每格说一句英文，再连起来复述。",
        "First, Tom saw a dog. Then, he gave it some food. Finally, the dog was happy.",
        "复述故事时，较清晰的顺序是？",
        ["随意跳着讲", "按开始→经过→结果", "只说生词", "从结尾倒着且无连接"],
        1,
        "时间顺序让听者更清楚。",
        "常见误区是细节过多抓不住主线，或不会用 First/Then 连接。",
    ),
    "eng-e-tenses-primary": C(
        "小学时态综合",
        "小学综合常见三种：一般现在（习惯）、现在进行（正在）、一般过去（昨天）。靠时间标志词快速判断，再选对动词形式。",
        "方法：时间词决定时态",
        "every day→一般现在；now→进行时；yesterday→过去时。做题先圈时间词。",
        "She reads every day. / She is reading now. / She read a book yesterday.",
        "句中有 now 且表示正在做，多用？",
        ["一般过去时", "现在进行时", "只有 will", "没有动词"],
        1,
        "now 常提示现在进行时。",
        "常见误区是看见动词就乱选形式，不先看时间标志。",
    ),
    "eng-e-topic-conversation": C(
        "话题对话",
        "话题对话是一问一答：听清对方问题，用完整句回答，并可补充一句细节。话题如学校、爱好、天气、家庭。礼貌用语请穿插使用。",
        "方法：听问题→答一句→加细节",
        "Q: What do you like? A: I like football. I play it on Sundays.",
        "A: How is the weather? B: It's rainy. I stay at home.",
        "对话回答较好的方式是？",
        ["只回一个词就结束且不相关", "完整回答并适当补充", "长时间不说话", "完全用中文"],
        1,
        "完整句+细节更自然得体。",
        "常见误区是答非所问，或只背范文不会根据问题调整。",
    ),
    "eng-e-vocab-600-words": C(
        "小学词汇总复习",
        "小学阶段词汇覆盖校园、家庭、食物、动物、天气、动作等主题。复习时按主题归类，结合拼读与例句，比孤立中译更牢固。",
        "方法：主题词卡 + 造句",
        "每主题抽 10 词：看英文说中文、看中文说英文，再各写一句。易混词对比记。",
        "school: classroom, teacher, homework — I do my homework in the classroom.",
        "词汇总复习更有效的做法是？",
        ["只看中文不看英文", "按主题归类并放进句子里用", "一天硬背永不复习", "只抄写不做听说"],
        1,
        "归类与语境使用记得更牢。",
        "常见误区是只记中文意思，不会读也不会用。",
    ),
    "eng-e-vocab-daily-life": C(
        "日常生活词汇",
        "日常生活词包括衣服、食物、交通、作息等，如 breakfast, bus, jacket, brush teeth。学习时把词放进一天的时间线里记更鲜活。",
        "方法：一日时间线记词",
        "早晨–中午–晚上各列 5 个词，造句：I eat breakfast at 7. I go to school by bus.",
        "I put on my jacket. I have lunch. I go home.",
        "breakfast 属于哪类话题词汇？",
        ["方位介词专用", "日常生活（餐食）", "只用于将来时语法名", "字母表"],
        1,
        "breakfast 是日常餐食词。",
        "常见误区是词与生活场景脱节，考试认得出却说不出。",
    ),
    "eng-e-vocab-family-school": C(
        "家庭与学校词汇",
        "家庭词：father, mother, brother, sister；学校词：teacher, classmate, classroom, playground。用 This is my … / I am in … 介绍最实用。",
        "方法：画家谱/校园图贴词",
        "在图上标注英文，指着说：This is my mother. This is my classroom.",
        "My father is a doctor. My classroom is big.",
        "classmate 的意思更接近？",
        ["教室桌椅", "同班同学", "家庭地址", "校服颜色 only"],
        1,
        "classmate 指同班同学。",
        "常见误区是 family/school 词混记，或只会中文不会指物说英语。",
    ),
    "eng-e-vocab-nature-society": C(
        "自然与社会词汇",
        "自然词：sun, rain, tree, animal；社会词：hospital, police, library, festival。结合天气、场所与简单公共标识学习。",
        "方法：场所+能做什么",
        "每记一个场所，配一个动作：library — read books；hospital — see a doctor。",
        "It's sunny. The birds are in the tree. We go to the library.",
        "在 library 人们常常？",
        ["swim only", "read books", "cook dinner always", "fly a plane"],
        1,
        "图书馆常与读书相关。",
        "常见误区是场所词记混（hospital/hotel），或不会搭配常用动词。",
    ),
    "eng-e-vowel-sounds": C(
        "英语元音发音",
        "元音气流不受阻，开口程度不同。小学先感知常见短元音与长元音差异，通过听辨最小对立词建立音感，再跟读纠正口型。",
        "方法：听辨→跟读→对照口型",
        "对比 bit/beat、full/fool；看老师口型，对着镜子练。",
        "ship /ɪ/ 与 sheep /i:/ 靠元音长短区分。",
        "区分 ship 与 sheep，关键主要在？",
        ["辅音完全不同", "元音长短/音质不同", "必须大写", "标点符号"],
        1,
        "元音不同造成词义不同。",
        "常见误区是用汉字注音，长短元音“听着差不多”就不区分。",
    ),
    "eng-e-word-reading": C(
        "单词拼读",
        "单词拼读把字母/字母组合的音连贯读出，再认词义。步骤：看→分音节或音素→连读→整词。熟练后能“见词能读”。",
        "方法：分音连读三步走",
        "如 rabbit：rab-bit，先分再连。不熟的词用自然拼读规则试读，再查听验证。",
        "c-a-t → cat；sh-i-p → ship.",
        "拼读生词时较好的顺序是？",
        ["先猜中文再不管发音", "看字母音并连起来读", "跳过不读", "只写不说"],
        1,
        "先出字母音再连成词。",
        "常见误区是看词直接猜中文，从不尝试拼读。",
    ),
    "eng-e-writing-skills-primary": C(
        "小学写作技巧",
        "小学写作技巧包括：审清题目、列要点、写完整句、适当连接、检查修改。内容真实简单即可，正确比“高级词”更重要。",
        "方法：要点清单→成句→连接→检查",
        "把提示写成 ①②③；每点一句；用 and/but/because；检查大写、时态、be 动词。",
        "I am Xiaoming. I like English because it is fun.",
        "写完短文后最值得检查的是？",
        ["是否全用超难单词", "要点是否写全、句子是否正确", "是否取消句号", "是否全用中文"],
        1,
        "要点齐全与句子正确是得分关键。",
        "常见误区是追求华丽词汇却时态、主谓错误连连。",
    ),
}


STYLE = """
<style id="enge-depth-css">
.enge-depth .worked-example{margin:16px 0;padding:16px;border-left:4px solid var(--brand,#38bdf8);background:rgba(56,189,248,.08);border-radius:0 12px 12px 0}
.enge-depth .module-check{margin-top:18px;padding:16px;border-radius:14px;background:rgba(251,146,60,.08);border:1px solid rgba(251,146,60,.28)}
.enge-depth .module-check button{display:block;width:100%;margin:8px 0;text-align:left;border:1px solid var(--line,#233);border-radius:10px;background:#0b1628;color:var(--text,#e5e7eb);padding:11px 13px;cursor:pointer}
.enge-depth .module-check button.correct{border-color:var(--ok,#22c55e);background:rgba(34,197,94,.14)}
.enge-depth .module-check button.wrong{border-color:#f87171;background:rgba(248,113,113,.12)}
.enge-depth .enge-feedback{display:none;margin-top:10px;padding:12px;border-radius:10px;background:rgba(56,189,248,.1)}
.enge-depth .enge-pitfall{margin:14px 0 0;padding:12px;border-radius:10px;background:rgba(248,180,0,.08);border:1px solid rgba(248,180,0,.24)}
</style>
"""

CHECK_SCRIPT = """
<script id="enge-depth-js">
function engeDepthCheck(button, isCorrect, feedbackId, explanation) {
  var box = button.closest('.module-check');
  if (!box || box.dataset.answered) return;
  box.dataset.answered = '1';
  box.querySelectorAll('button').forEach(function (item) {
    item.disabled = true;
    if (item.dataset.correct === '1') item.classList.add('correct');
  });
  if (!isCorrect) button.classList.add('wrong');
  var feedback = document.getElementById(feedbackId);
  if (feedback) {
    feedback.style.display = 'block';
    feedback.textContent = (isCorrect ? '正确。' : '再想想。') + explanation;
  }
}
</script>
"""


def build_block(cfg: dict) -> str:
    feedback_id = "enge-depth-feedback"
    options = []
    for idx, opt in enumerate(cfg["options"]):
        correct = idx == cfg["correct"]
        handler = "engeDepthCheck(this,{c},'{f}',{e})".format(
            c="true" if correct else "false",
            f=feedback_id,
            e=json.dumps(cfg["feedback"], ensure_ascii=False),
        )
        options.append(
            '<button type="button" data-correct="{flag}" onclick="{h}">{letter}. {opt}</button>'.format(
                flag="1" if correct else "0",
                h=html.escape(handler, quote=True),
                letter=chr(65 + idx),
                opt=html.escape(opt),
            )
        )
    return f"""
<section class="slide-page" data-page-type="content" data-tsh="精讲">
  <section class="section enge-depth core-knowledge-module text-module" id="lesson-focus"
    data-bloom-level="understand" data-scaffold="full" data-tts="lesson-focus">
    <div class="card">
      <span class="phase-tag">知识精讲</span>
      <h2>{html.escape(cfg['concept_title'])}</h2>
      <p>{html.escape(cfg['concept_body'])}</p>
    </div>
  </section>
</section>
<section class="slide-page" data-page-type="content" data-tsh="方法范例">
  <section class="section enge-depth core-knowledge-module text-module" id="lesson-method"
    data-bloom-level="apply" data-scaffold="partial" data-tts="lesson-method">
    <div class="card">
      <span class="phase-tag">方法与范例</span>
      <h2>{html.escape(cfg['method_title'])}</h2>
      <p>{html.escape(cfg['method_body'])}</p>
      <div class="worked-example"><strong>范例：</strong>{html.escape(cfg['example'])}</div>
      <p id="lesson-pitfall" class="enge-pitfall"><strong>常见误区：</strong>{html.escape(cfg['pitfall'])}</p>
      <div class="module-check" data-conceptest="true">
        <h3>马上练：辨析要点</h3>
        <p>{html.escape(cfg['question'])}</p>
        {''.join(options)}
        <div class="enge-feedback" id="{feedback_id}" role="status"></div>
      </div>
    </div>
  </section>
</section>
"""


def upgrade(course_id: str, cfg: dict) -> tuple[bool, str]:
    path = ROOT / "community" / course_id / "index.html"
    if not path.exists():
        return False, "missing index.html"
    source = path.read_text(encoding="utf-8")
    if 'id="lesson-focus"' in source:
        return False, "already upgraded"
    dpos = -1
    for anchor in ('id="deep-understanding"', 'id="transfer-task"', 'id="posttest"', 'id="summary"'):
        dpos = source.find(anchor)
        if dpos >= 0:
            break
    if dpos < 0:
        return False, "insert anchor not found"
    marker = source.rfind('<section class="slide-page"', 0, dpos)
    insert_at = marker if marker >= 0 else source.rfind("<section", 0, dpos)
    if insert_at < 0:
        return False, "insert marker not found"
    source = source[:insert_at] + build_block(cfg) + "\n" + source[insert_at:]
    if 'id="enge-depth-css"' not in source:
        source = source.replace("</head>", STYLE + "\n</head>", 1)
    if 'id="enge-depth-js"' not in source:
        source = source.replace("</body>", CHECK_SCRIPT + "\n</body>", 1)
    source = re.sub(r"[ \t]+\n", "\n", source)
    path.write_text(source, encoding="utf-8")
    manifest_path = path.parent / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        changed = False
        for key, value in {"version": COURSE_VERSION, "updated_at": UPDATED_AT}.items():
            if manifest.get(key) != value:
                manifest[key] = value
                changed = True
        if changed:
            manifest_path.write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
    return True, "2 depth modules + metadata"


def main() -> int:
    # Ensure every on-disk eng-e course missing lesson-focus is covered
    missing_on_disk = []
    for path in sorted((ROOT / "community").glob("eng-e-*/index.html")):
        course_id = path.parent.name
        text = path.read_text(encoding="utf-8")
        if 'id="lesson-focus"' not in text and course_id not in COURSES:
            missing_on_disk.append(course_id)
    if missing_on_disk:
        print("ERROR: COURSES missing entries for:", ", ".join(missing_on_disk))
        return 1

    changed = failed = 0
    for course_id, cfg in COURSES.items():
        ok, msg = upgrade(course_id, cfg)
        if ok:
            changed += 1
            print(f"OK {course_id}: {msg}")
        elif msg == "already upgraded":
            print(f"SKIP {course_id}: {msg}")
        else:
            failed += 1
            print(f"FAIL {course_id}: {msg}")
    print(f"done: changed={changed} failed={failed} of {len(COURSES)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
