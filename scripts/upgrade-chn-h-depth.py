#!/usr/bin/env python3
"""Add topic-specific depth modules to chn-h shell courses.

High-school Chinese courses often pass via template sections but lack
topic-specific core teaching. Each course gets 知识精讲 + 方法范例
(worked example + diagnostic + 常见误区). No mp4. Idempotent via id="lesson-focus".
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_VERSION = "1.1.0"
UPDATED_AT = "2026-08-11"


def C(ct, cb, mt, mb, ex, q, opts, correct, fb, pit):
    return dict(
        concept_title=ct, concept_body=cb, method_title=mt, method_body=mb,
        example=ex, question=q, options=opts, correct=correct, feedback=fb, pitfall=pit,
    )


COURSES = {
    "chn-h-classical-vocab-h": C(
        "文言实词",
        "文言实词复习要抓住一词多义、古今异义、通假字、词类活用。同一个字在不同语境意义可能差别很大，必须“因文定义”。积累时应放回例句，而不是只背义项清单。",
        "方法：语境定位 + 代入验证",
        "先看语法位置（作何成分），再在备选义项中试填，选使句意贯通者；注意与现代汉语差异大的古今异义词。",
        "“走”常作“跑”讲，如“双兔傍地走”，不可一律译成现代的“行走”。",
        "解释文言实词最可靠的依据是？",
        ["只看字典第一个义项", "上下文语境与语法位置", "现代汉语语感唯一", "字的笔画多少"],
        1,
        "语境与语法位置决定取义。",
        "常见误区是以今律古，把今义硬套文言。",
    ),
    "chn-h-classical-function-words": C(
        "文言虚词",
        "常见文言虚词如之、其、以、于、而、则、乃、若、为、者、所等，用法灵活，可作代词、助词、介词、连词等。复习要按“词—用法—例句”建立网络，并比较易混虚词。",
        "方法：定词性再定关系",
        "先判断虚词在句中词性，再说明它连接或指代的对象。翻译时补出关系，勿空翻。",
        "“以”可表凭借、原因、目的等；“以君之力”中的“以”表凭借。",
        "辨析虚词用法首先应？",
        ["看拼音", "结合句子判断词性与语法作用", "只背例句不管句意", "按字数决定"],
        1,
        "词性与语法作用是辨析关键。",
        "常见误区是同一虚词只会一种用法，或脱离句子死记。",
    ),
    "chn-h-classical-grammar-h": C(
        "文言句式与语法",
        "特殊句式包括判断句、被动句、倒装句（宾语前置、定语后置、状语后置、主谓倒装）和省略句。识别靠标志词与语序异常；翻译要调语序、补省略，做到“信、达”。",
        "方法：找标志→调语序→补成分",
        "见“者……也”“为……所”“何……之有”等先定性；倒装按现代汉语习惯还原。",
        "“何陋之有”为宾语前置，译为“有什么简陋的呢”。",
        "“为……所……”通常表示？",
        ["判断", "被动", "感叹", "比较"],
        1,
        "这是典型被动句式标志。",
        "常见误区是只认标志不还原语序，译文生硬难懂。",
    ),
    "chn-h-classical-translation-h": C(
        "文言文翻译",
        "翻译以直译为主、意译为辅，力求信达雅。落实关键词（实词虚词、活用、句式），不漏译、不随意添油加醋。得分点往往在关键词与句式处理。",
        "方法：留删补换调",
        "专名保留，语助可删，省略要补，单音换双音，倒装要调。译完默读是否通顺。",
        "“假舟楫者，非能水也”译时落实“假”“水（活用）”，并补出主语逻辑。",
        "高考文言翻译更强调？",
        ["华丽辞藻", "关键词与句式准确落实", "全部意译不顾原文", "只译大意忽略得分点"],
        1,
        "关键词与特殊句式是采分重点。",
        "常见误区是通顺却偏离原意，或保留文言词不翻译。",
    ),
    "chn-h-classical-prose-advanced": C(
        "古文经典精读",
        "精读古文要在疏通文意后，把握叙事线索、人物形象、说理层次与作者情志。关注叙议结合、对比衬托、卒章显志等手法，体会古代士人的处境与选择。",
        "方法：文脉—主旨—写法",
        "先一句话概括写什么，再找点睛议论句，最后分析手法如何服务主旨。",
        "《劝学》以大量比喻论证学习的意义与方法，层次清晰。",
        "精读古文最核心的目标是？",
        ["只核对注释", "理解文意并把握主旨与写法", "只统计字数", "只背作者生平"],
        1,
        "文意、主旨、写法三者贯通才是精读。",
        "常见误区是停留在翻译层，不上到主旨与艺术。",
    ),
    "chn-h-classical-comprehensive": C(
        "文言文综合鉴赏",
        "综合题常考内容概括、人物评价、主旨情感、手法作用与文化常识。答题要“观点+原文依据+分析”，避免空喊标签。把字词句理解服务于篇章理解。",
        "方法：审题定向→回文定位→规范作答",
        "看清问的是内容、情感还是手法；到原文找对应句；用术语+效果表述。",
        "问“某句作用”，可答结构（承上启下）与内容（突出人物品质）两层。",
        "文言主观题最忌？",
        ["结合原文分析", "只贴标签无依据", "分点作答", "先审清题干"],
        1,
        "必须有文本依据，不能空贴手法标签。",
        "常见误区是套用万能模板，与文本脱节。",
    ),
    "chn-h-poetry-imagery-h": C(
        "古诗词意象与意境",
        "意象是融入主观情意的物象，意境是意象组合形成的艺术境界。抓意象要明其常见文化内涵，又要据诗境灵活理解。由意象到意境，再到情感，是鉴赏基本路径。",
        "方法：列意象→拼画面→定情感",
        "把关键意象列出，描述画面色彩动静，再归纳诗人情感或理趣。",
        "“枯藤老树昏鸦”以衰败意象营造凄清意境，烘托游子愁绪。",
        "意象与意境的关系理解正确的是？",
        ["意象就是意境", "意象组合可形成意境", "意境与情感无关", "只有名词没有画面"],
        1,
        "意境往往由多个意象营造而成。",
        "常见误区是只背意象词典，不顾具体诗句语境。",
    ),
    "chn-h-poetry-expression-h": C(
        "古诗词表现手法",
        "常见手法：抒情方式（直抒、借景、托物、用典），表达技巧（对比、衬托、虚实、动静、抑扬），修辞（比喻、拟人、对偶、夸张等）。分析要说明“用了什么+怎样体现+效果/情感”。",
        "方法：指名→释例→达效",
        "先准确命名手法，再引诗句说明如何运用，最后落到情感或主旨。",
        "“蝉噪林逾静”以动衬静，突出山林幽静。",
        "分析表现手法时最完整的答法是？",
        ["只写手法名称", "名称+文本依据+效果情感", "只翻译诗句", "只写作者简介"],
        1,
        "三步答法才完整得分。",
        "常见误区是手法名称混淆（如对比与衬托），或有名无析。",
    ),
    "chn-h-poetry-emotion": C(
        "古诗词情感主旨",
        "诗词情感常见：思乡边塞、咏史怀古、惜春悲秋、送别友情、爱国壮志、恬淡归隐等。抓情感可看标题、意象、抒情句、注释背景。主旨是对情感与思想的凝练概括。",
        "方法：标题注释+关键句",
        "先读标题与注释定范围，再抓直接抒情句与反常之景，归纳情感要具体，避免只写“悲伤”。",
        "杜甫《春望》标题与“感时花溅泪”等句共同指向忧国思家之情。",
        "概括诗词情感应力求？",
        ["越笼统越好", "具体准确并有诗句依据", "只写一个字", "与文本无关的发挥"],
        1,
        "情感概括要具体且有据。",
        "常见误区是情感标签万能化，如一律“壮志难酬”。",
    ),
    "chn-h-poetry-comparison-h": C(
        "古诗词比较阅读",
        "比较阅读常比意象、情感、手法、风格、语言。先求同再求异，或按题干指定角度比。答案要“分短诗表述+比较点”，避免混写成一团。",
        "方法：定比较点→分别概括→对照异同",
        "题干问手法就只比手法；问情感则比异同及原因。各用一句评点，再总结。",
        "同写“月”，一表思乡，一表超脱，意象同而情志不同。",
        "比较阅读作答关键是？",
        ["只分析其中一首", "紧扣比较角度分述并对照", "抄两首原文了事", "只谈作者朝代"],
        1,
        "必须按角度对照分析。",
        "常见误区是两首分开鉴赏却不比较，或比较点游移。",
    ),
    "chn-h-literary-reading-h": C(
        "文学类文本阅读",
        "文学类文本（小说、散文等）阅读要整体把握情节/线索、人物、环境、主题与语言。选择题重细节与理解，主观题重分析概括。始终回到文本，拒绝体外发挥。",
        "方法：整体初读→题干定位→证据作答",
        "先明文体与主问题，再按题目回原文区间勾画，概括题分层，赏析题手法+效果。",
        "小说问人物形象：找出描写语句，归纳性格，点明其推动情节或主题的作用。",
        "文学类阅读主观题首要原则是？",
        ["脱离文本自由议论", "忠于文本有理有据", "只凭印象", "抄袭作文素材"],
        1,
        "一切分析以文本为依据。",
        "常见误区是主题拔高过度，或情节复述代替分析。",
    ),
    "chn-h-literary-deep-analysis": C(
        "文学类深度鉴赏",
        "深度鉴赏关注叙述视角、结构安排、细节象征、语言风格与主旨的多层含义。要能说明“这样写比那样写好在哪里”，体现文学性理解，而不仅是内容复述。",
        "方法：形式选择服务内容",
        "看到倒叙、留白、反复、反讽等，先说明形式特征，再解释对人物心理或主题的强化。",
        "限制视角可制造悬念，使读者与人物同步认知，增强真实感。",
        "深度鉴赏更应关注？",
        ["字数统计", "形式如何服务于内容与效果", "作者年龄", "出版价格"],
        1,
        "形式与内容、效果的关系是鉴赏核心。",
        "常见误区是堆砌术语，却说不清表达效果。",
    ),
    "chn-h-info-reading": C(
        "实用类/论述类文本",
        "论述类重论点、论据、论证；实用类重信息筛选、整合与理解。阅读要区分事实与观点，把握概念含义与论证逻辑，警惕绝对化表述与偷换概念。",
        "方法：标论点→理层次→核选项",
        "论述文首尾与段首句常含观点；选择题用“比对原文”排除无中生有、曲解、绝对化。",
        "选项把“可能”改成“一定”，属于典型错误。",
        "论述类文本选择题最有效策略是？",
        ["凭语感不看原文", "选项与原文细比对", "只看第一段", "选最长选项"],
        1,
        "细比对可识别偷换与无中生有。",
        "常见误区是凭常识做题，脱离材料。",
    ),
    "chn-h-practical-reading": C(
        "非连续性实用文本",
        "非连续性文本常含图表、材料组合。关键是提取关键信息、比较材料异同、完成推断或建议。注意图例单位、时间范围与材料出处，避免误读。",
        "方法：题干关键词→对应材料→综合结论",
        "一题可能跨材料，先定位再整合；提建议要针对材料问题，具体可行。",
        "图表上升趋势要读清纵轴含义，不能只看线条陡峭。",
        "非连续性文本作答首先要？",
        ["忽略图表", "准确提取并整合材料信息", "只写个人感想", "改写为诗歌"],
        1,
        "信息提取与整合是基础。",
        "常见误区是看错图例或把不同材料信息张冠李戴。",
    ),
    "chn-h-argumentative-essay": C(
        "议论文写作",
        "议论文要有鲜明论点、充分论据与合理论证。结构常用总分总、并列、递进、对照。语言严谨，避免口号化。高中阶段尤其要“分析”，不能只叙述事例。",
        "方法：论点—论据—分析锁死",
        "每段：分论点句首→叙例简洁→分析回扣论点→小结。分析可用因果、假设、对比。",
        "写“坚持”，例后应分析坚持如何克服困难并指向观点，而非把故事写完即止。",
        "议论文段落中最易失分的是？",
        ["有论点", "叙例后缺少分析回扣", "有结尾", "字数足够"],
        1,
        "缺分析会导致论据与论点脱节。",
        "常见误区是论据堆砌，以叙代议。",
    ),
    "chn-h-essay-structure-h": C(
        "作文审题立意与结构",
        "审题要抓住任务指令、材料关键词与关系类型（因果、辩证、比较等）。立意求准、求深、求新（在准的前提下）。结构服务立意，段落功能清晰，开头结尾有力。",
        "方法：圈关键词→确定关系→列提纲",
        "把材料句分层，明确写作对象与态度；列出 3 个分论点或情节节点再开写。",
        "材料强调“过程与结果”，立意不可只谈结果忽视过程。",
        "审题最重要的是？",
        ["忽视材料自由发挥", "准确把握材料任务与关系", "只追求新颖不管是否离题", "先写结尾"],
        1,
        "准是立意的第一要求。",
        "常见误区是抓住一点不顾整体，造成偏题。",
    ),
    "chn-h-task-driven-writing": C(
        "任务驱动型作文",
        "任务驱动型写作强调真实情境与具体任务：写给谁、做什么、达成何目的。内容要贴合身份与场合，权衡多方立场，给出合情合理的方案或看法，避免空发感慨。",
        "方法：受众—目的—路径",
        "先明确体裁与对象，再表明态度，接着分析矛盾，最后给建议。语言得体。",
        "校庆征文若要求“给学弟学妹的建议”，口吻应亲切具体，而非纯学术论文腔。",
        "任务驱动型作文优先考虑？",
        ["华丽辞藻不顾对象", "任务指令与读者意识", "只堆名言", "完全无视情境"],
        1,
        "完成任务并契合读者最重要。",
        "常见误区是写成普通话题作文，丢掉情境任务。",
    ),
    "chn-h-gaokao-essay": C(
        "高考作文综合训练",
        "高考作文综合考查审题立意、选材构思、论证/叙事能力与语言表达。临场要稳：先准后深，结构完整，卷面清晰。素材在于用活，不在于多。",
        "方法：5 分钟提纲 + 分段推进",
        "审题列纲→段首分论→例证分析→结尾升华但不空洞。留时间检查标题与错别字。",
        "辩证类材料可用“承认A，指出局限，提出B与A统一”的思路展开。",
        "高考作文临场第一要务是？",
        ["追求险怪立意", "审题准确、结构完整", "放弃提纲直接写", "只写一半精雕细琢"],
        1,
        "准确与完整是得分基础。",
        "常见误区是为求新而跑题，或虎头蛇尾。",
    ),
    "chn-h-advanced-composition": C(
        "高级写作技巧",
        "在立意正确基础上，追求思想层次、逻辑密度与语言表现力：如设置思辨转折、细节场景化、比喻说理、整散句结合。技巧为内容服务，避免炫技空洞。",
        "方法：升格一句话",
        "把空泛句改成带具体场景或逻辑关联的句子；每段至少一处有力分析或金句，但忌堆砌。",
        "将“我们要努力”升格为“把每天的微小练习，叠成可见的成长轨迹”。",
        "高级技巧使用原则是？",
        ["技巧越多越好不顾内容", "服务立意与读者感受", "全用生僻字", "取消逻辑只要排比"],
        1,
        "技巧必须服务内容。",
        "常见误区是辞藻华丽而思辨薄弱。",
    ),
    "chn-h-language-expression-h": C(
        "语言表达简明连贯得体",
        "简明：无冗余；连贯：话题与逻辑衔接；得体：语体与对象场合合适。常见题型有语句复位、衔接排序、语境补写、得体改写。",
        "方法：抓话题一致与逻辑词",
        "排序看指代、时间、因果；补写看前后句式与信息缺口；得体改口头/书面、谦敬词。",
        "把“敝校”用于自家学校谦称，称对方学校用“贵校”。",
        "“连贯”主要要求？",
        ["字数最少", "语句衔接顺畅、话题统一", "全部用感叹号", "堆砌成语"],
        1,
        "衔接与话题统一是连贯核心。",
        "常见误区是得体题谦敬词用反。",
    ),
    "chn-h-sentence-revision-h": C(
        "病句修改与句式变换",
        "病句类型：语序不当、搭配不当、成分残缺/赘余、结构混乱、不合逻辑、表意不明等。修改要保持原意。句式变换如主动被动、长句短句、整散转换，服务于表达需要。",
        "方法：压缩主干找病因",
        "先找主谓宾，看搭配与残缺；再查并列项与否定逻辑；修改最小幅度。",
        "“能否成功，关键在于努力”主客与“能否”两边要对上，或改为“成功关键在于努力”。",
        "修改病句的原则是？",
        ["大改原意", "消除语病并尽量保持原意", "越改越长", "只改标点"],
        1,
        "既要通顺，又要忠实原意。",
        "常见误区是改了语病却改变原意，或漏改结构性混乱。",
    ),
    "chn-h-idiom-usage-h": C(
        "成语辨析与运用",
        "成语考查望文生义、对象误用、褒贬色彩、谦敬错位、语义重复等。复习要掌握常用易错成语的准确含义与适用对象，放入句子检验。",
        "方法：释义→对象→色彩→语境",
        "先准确释义，再看用于人还是物、褒还是贬，最后看与上下文是否重复矛盾。",
        "“美轮美奂”多形容建筑高大华美，不宜形容歌曲。",
        "成语使用错误常见原因是？",
        ["书写美观", "望文生义或对象色彩不当", "笔画太多", "出自古代"],
        1,
        "误解词义与用错对象最常见。",
        "常见误区是只知大概意思，不管适用对象。",
    ),
    "chn-h-red-chamber": C(
        "《红楼梦》整本书阅读",
        "整本书阅读要把握主要人物关系、叙事结构、主题意蕴与艺术成就。从“感动细节”进入，再上升到人物命运、家族盛衰与叙事技法。避免只记情节八卦。",
        "方法：人物弧光 + 细节印证",
        "选一个人物，梳理其关键事件与性格发展，用细节描写证明观点；再联系主题。",
        "黛玉进府的细节写出寄人篱下的谨慎，也为后续性格与命运作铺垫。",
        "整本书阅读更应注重？",
        ["只背人物名单", "情节、人物、主题与艺术的贯通", "只看影视解说", "只记作者生平"],
        1,
        "要贯通故事、人物、主题与写法。",
        "常见误区是碎片化了解，形不成整体认识。",
    ),
    "chn-h-countryside-china": C(
        "《乡土中国》学术论著阅读",
        "学术论著阅读要抓住核心概念（如差序格局、礼治秩序、血缘与地缘等），理清作者问题意识与论证逻辑，并能用概念解释社会生活现象。读“乡下人”相关章节要避免刻板偏见，理解其分析框架。",
        "方法：概念卡片 + 例子验证",
        "每章提炼 1–2 个概念定义，自己举生活例子验证；比较概念之间关系。",
        "用“差序格局”理解传统社会关系的伸缩与亲疏，不同于团体格局。",
        "阅读学术论著的关键是？",
        ["跳过概念只看故事", "把握核心概念与论证逻辑", "只记出版年份", "当成小说欣赏情节"],
        1,
        "概念与逻辑是论著阅读核心。",
        "常见误区是概念识记却不会迁移解释现实。",
    ),
    "chn-h-foreign-classics": C(
        "外国文学经典",
        "阅读外国文学经典要结合文化背景，把握人物、主题、叙事与象征。尊重译名与重要情节，关注人类共通情感与不同文化视角。比较阅读可加深理解。",
        "方法：背景—人物—主题",
        "先了解作者时代与创作意图简介，再抓人物冲突，最后概括主题，避免只讲故事。",
        "读《老人与海》既看情节坚持，也思“压力下的风度”等主题。",
        "阅读外国经典应特别注意？",
        ["用中国古代官职硬套一切", "文化背景与主题人物结合理解", "只记页码", "拒绝任何象征解读"],
        1,
        "要把文化背景与文本分析结合起来。",
        "常见误区是以本土经验简单比附，或停留在情节复述。",
    ),
}


STYLE = """
<style id="chnh-depth-css">
.chnh-depth .worked-example{margin:16px 0;padding:16px;border-left:4px solid var(--brand,#38bdf8);background:rgba(56,189,248,.08);border-radius:0 12px 12px 0}
.chnh-depth .module-check{margin-top:18px;padding:16px;border-radius:14px;background:rgba(251,146,60,.08);border:1px solid rgba(251,146,60,.28)}
.chnh-depth .module-check button{display:block;width:100%;margin:8px 0;text-align:left;border:1px solid var(--line,#233);border-radius:10px;background:#0b1628;color:var(--text,#e5e7eb);padding:11px 13px;cursor:pointer}
.chnh-depth .module-check button.correct{border-color:var(--ok,#22c55e);background:rgba(34,197,94,.14)}
.chnh-depth .module-check button.wrong{border-color:#f87171;background:rgba(248,113,113,.12)}
.chnh-depth .chnh-feedback{display:none;margin-top:10px;padding:12px;border-radius:10px;background:rgba(56,189,248,.1)}
.chnh-depth .chnh-pitfall{margin:14px 0 0;padding:12px;border-radius:10px;background:rgba(248,180,0,.08);border:1px solid rgba(248,180,0,.24)}
</style>
"""

CHECK_SCRIPT = """
<script id="chnh-depth-js">
function chnhDepthCheck(button, isCorrect, feedbackId, explanation) {
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
    feedback_id = "chnh-depth-feedback"
    options = []
    for idx, opt in enumerate(cfg["options"]):
        correct = idx == cfg["correct"]
        handler = "chnhDepthCheck(this,{c},'{f}',{e})".format(
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
  <section class="section chnh-depth core-knowledge-module text-module" id="lesson-focus"
    data-bloom-level="understand" data-scaffold="full" data-tts="lesson-focus">
    <div class="card">
      <span class="phase-tag">知识精讲</span>
      <h2>{html.escape(cfg['concept_title'])}</h2>
      <p>{html.escape(cfg['concept_body'])}</p>
    </div>
  </section>
</section>
<section class="slide-page" data-page-type="content" data-tsh="方法范例">
  <section class="section chnh-depth core-knowledge-module text-module" id="lesson-method"
    data-bloom-level="apply" data-scaffold="partial" data-tts="lesson-method">
    <div class="card">
      <span class="phase-tag">方法与范例</span>
      <h2>{html.escape(cfg['method_title'])}</h2>
      <p>{html.escape(cfg['method_body'])}</p>
      <div class="worked-example"><strong>范例：</strong>{html.escape(cfg['example'])}</div>
      <p id="lesson-pitfall" class="chnh-pitfall"><strong>常见误区：</strong>{html.escape(cfg['pitfall'])}</p>
      <div class="module-check" data-conceptest="true">
        <h3>马上练：辨析要点</h3>
        <p>{html.escape(cfg['question'])}</p>
        {''.join(options)}
        <div class="chnh-feedback" id="{feedback_id}" role="status"></div>
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
    if 'id="chnh-depth-css"' not in source:
        source = source.replace("</head>", STYLE + "\n</head>", 1)
    if 'id="chnh-depth-js"' not in source:
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
