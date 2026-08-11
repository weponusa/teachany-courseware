#!/usr/bin/env python3
"""Add topic-specific depth modules to eng-h shell courses.

High-school English courses often pass via template sections but lack
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
    "eng-h-vocab-3500": C(
        "高中 3500 词汇",
        "高中英语词汇学习不能只背中文释义，要掌握词性、搭配、派生与语境义。3500 词是阅读与写作的底座：高频词优先，按主题与词族记忆，并在句子中复用。",
        "方法：词族 + 搭配 + 造句",
        "每个生词记 1 个搭配和 1 个短句；同根词一起记（act/action/active）。隔日复习对抗遗忘。",
        "meet the deadline / a sense of belonging 比孤立背 deadline、belonging 更管用。",
        "记单词最有效的做法是？",
        ["只看中文表", "结合搭配与语境句子记忆", "一次贪多不复习", "只记拼写不看词性"],
        1,
        "搭配与语境能提高保持与运用。",
        "常见误区是只会中译英单词表，阅读中仍猜不出语境义。",
    ),
    "eng-h-word-formation-h": C(
        "构词法：派生、合成与转化",
        "英语构词主要有派生（前后缀）、合成（两词合一）与转化（词性变化、形式不变）。掌握常见词缀可快速扩词并猜测词义，是阅读与完形的利器。",
        "方法：拆词缀定词性词义",
        "见 -tion/-ment 多名词，-ive/-ful 多形容词，un-/dis-/in- 常表否定。先判词性再代入句意。",
        "happy→happiness；possible→impossible；blackboard 为合成词。",
        "impossible 中的 im- 主要作用是？",
        ["表比较级", "表否定", "表过去", "表复数"],
        1,
        "im-/in-/un- 等常构成反义。",
        "常见误区是只记整词，不会用词缀推断生词。",
    ),
    "eng-h-context-vocab": C(
        "语境词义推断",
        "高考常考熟词生义与猜测词义。线索来自定义、同位、举例、对比、因果与前后逻辑。把目标词所在句及上下句一起看，避免只盯住该词。",
        "方法：画逻辑信号词",
        "however/but 表转折；that is/which means 表解释；for example 表例证。用选项回代验证。",
        "The soil was so barren that nothing could grow. barren≈贫瘠，由结果推断。",
        "猜测词义时最应依靠？",
        ["只看词根不管句子", "上下文逻辑与信号词", "随便选熟悉选项", "忽略标点与从句"],
        1,
        "语境线索是推断依据。",
        "常见误区是用自己最熟的义项硬套，不顾上下文。",
    ),
    "eng-h-tense-system": C(
        "时态与语态系统",
        "时态表示时间与体（进行、完成等），语态表示主被动。高中要形成“时间轴+体貌+主动/被动”的系统观，并注意时间状语与时态呼应，尤其在记叙与说明中。",
        "方法：定时间→选体→查语态",
        "先找时间状语与上下文时态，再决定一般/进行/完成；宾语与主语是动作承受关系时用被动。",
        "The bridge was built in 1998. 强调桥被建成的事实。",
        "选择时态的首要依据通常是？",
        ["句子长短", "时间关系与上下文", "生词多少", "是否定语从句"],
        1,
        "时间与上下文决定时态。",
        "常见误区是看见 have 就用完成时，或被动漏掉 be + 过去分词。",
    ),
    "eng-h-attributive-clauses-h": C(
        "定语从句",
        "定语从句修饰名词/代词，由关系代词或关系副词引导。关键：先行词、关系词在从句中充当的成分、限制性与非限制性差异，以及介词+which/whom 结构。",
        "方法：先行词 + 缺什么成分",
        "缺主语/宾语用 that/which/who/whom；缺地点/时间/原因状语用 where/when/why（或相应介词+which）。",
        "This is the school where I studied. where=in which。",
        "关系词的选择主要看？",
        ["从句长度", "先行词及关系词在从句中的成分", "作者国籍", "标点多少"],
        1,
        "成分与先行词决定关系词。",
        "常见误区是 where/which 混用，或非限制性从句误用 that。",
    ),
    "eng-h-adverbial-clauses-h": C(
        "状语从句",
        "状语从句表示时间、条件、原因、让步、目的、结果、方式、比较等。连词是识别标志。注意主句与从句时态呼应，以及 when/while/as、though/although 等易混点。",
        "方法：先判逻辑类型再选连词",
        "问“两分句什么关系”：条件用 if/unless，让步用 although/even if，目的用 so that 等。",
        "Although it rained, we went out. 让步，不可与 but 连用。",
        "although 引导的是？",
        ["名词性从句", "让步状语从句", "定语从句", "主语从句唯一"],
        1,
        "although 表让步。",
        "常见误区是 although 与 but 同现，或条件从句误用将来时（主将从现）。",
    ),
    "eng-h-noun-clauses": C(
        "名词性从句",
        "名词性从句包括主语从句、宾语从句、表语从句与同位语从句，在句中充当名词性成分。连接词 that/whether/if/wh- 的选用取决于是否缺成分、是否表疑问。",
        "方法：缺成分用 wh-，不缺用 that",
        "从句若成分齐全用 that（可省略于宾从）；缺名词性成分用 what；是否用 whether/if。同位语从句解释抽象名词。",
        "What he said is true.（主语从句，what 作 said 的宾语）",
        "同位语从句与定语从句的主要区别是？",
        ["都一定用 which", "同位语从句解释名词内容，定语从句修饰限定", "没有区别", "同位语从句不能用 that"],
        1,
        "同位语补充说明，定语修饰限定。",
        "常见误区是 what/that 混用，或 if 用于介宾与主从表“是否”。",
    ),
    "eng-h-non-finite-h": C(
        "非谓语动词",
        "非谓语包括不定式、动名词与分词（现在/过去），不作谓语，可作主宾定状补。解题抓“主动/被动”与“进行/完成”，以及固定搭配后接 to do 或 doing。",
        "方法：成分功能 + 主被动",
        "作目的状语多用 to do；作伴随/结果看分词；与逻辑主语是被动完成关系常用 done。",
        "Seeing the teacher, the students stood up.（主动、几乎同时）",
        "非谓语选择首先应分析？",
        ["字体颜色", "逻辑主语与主动被动、时间关系", "段落字数", "是否听力题"],
        1,
        "逻辑主语与语态时间是关键。",
        "常见误区是双谓语，或忽略固定搭配（如 enjoy doing）。",
    ),
    "eng-h-subjunctive-mood": C(
        "虚拟语气",
        "虚拟语气表示假设、愿望、建议等非真实情况。常见：if 虚拟（现在/过去/将来），wish/as if，以及 suggest/insist 等后 that 从句用 (should)+动词原形。先判“是否与事实相反”。",
        "方法：定时间轴再选形式",
        "与现在相反：did/were + would do；与过去相反：had done + would have done。建议类记“should do”。",
        "If I were you, I would try again.",
        "表示与过去事实相反的 if 从句常用？",
        ["did", "had done", "will do", "does"],
        1,
        "过去虚拟从句用 had done。",
        "常见误区是主从句时间错配，或建议类动词后仍用陈述语气。",
    ),
    "eng-h-special-sentences": C(
        "特殊句式：倒装、强调与省略",
        "倒装分完全与部分倒装（否定词开头、only+状语等）；强调句 It is/was...that/who...；省略常见于比较句与对话。识别标志并还原正常语序有助于理解与改错。",
        "方法：找标志→还原语序",
        "Never/Hardly/Only then 等开头想部分倒装；强调句去掉 It is...that 后仍完整。",
        "Only then did I realize the truth.",
        "“It was in the park that we met.” 属于？",
        ["定语从句", "强调句", "主语从句", "被动语态"],
        1,
        "强调地点状语的强调句。",
        "常见误区是把强调句误判为定语从句，或倒装漏助动词。",
    ),
    "eng-h-advanced-grammar": C(
        "语法综合进阶",
        "综合语法题把时态语态、从句、非谓语、一致与固定搭配揉在一起。解题要有全局观：先抓句子主干，再处理修饰成分，最后检查一致与逻辑。",
        "方法：主干优先，层层剥离",
        "划出主谓宾，把从句与非谓语当作“零件”判断其作用；长难句先译主干。",
        "The book that he recommended was worth reading. 主干：The book was worth reading.",
        "面对长难句，优先做什么？",
        ["从最后一个单词往前猜", "找出主干再分析修饰语", "放弃阅读", "只看生词表"],
        1,
        "主干清楚再看修饰，不易崩溃。",
        "常见误区是平行结构看走眼，或主谓一致被插入语干扰。",
    ),
    "eng-h-reading-detail-h": C(
        "阅读细节题",
        "细节题考查定位与准确理解，答案多是原文同义改写。要杜绝凭印象，必须回文核对人名、数字、因果与否定范围。",
        "方法：题干关键词定位→比对选项",
        "用专有名词、数字、生词回原文；选项常见陷阱：偷换、绝对化、答非所问、拼凑。",
        "题干问原因，原文 because/lead to 处才是答案区，不可抄结果句。",
        "细节题最可靠的做法是？",
        ["不读文章直接选", "定位原文并比对同义改写", "只选含文章原词的选项", "选最长选项"],
        1,
        "定位+同义改写验证最稳。",
        "常见误区是看见原词就选，掉入拼凑陷阱。",
    ),
    "eng-h-reading-inference-h": C(
        "阅读推理题",
        "推理题要求基于文意合理推断，不是主观脑补。推断要有原文依据，程度不可过度。注意作者态度与言外之意，但须可追溯到句子。",
        "方法：依据句→合理一步推断",
        "先找到相关句，再问“由此必然/很可能得出什么”；排除无依据与相反项。",
        "文中说某人多次推迟申请，可推其犹豫，不可推其一定失败。",
        "推理题不可？",
        ["依据原文", "脱离文本过度引申", "比较选项语气强弱", "排除相反信息"],
        1,
        "过度引申是推理题大忌。",
        "常见误区是把可能当一定，或掺入个人经验。",
    ),
    "eng-h-reading-purpose": C(
        "阅读主旨与目的题",
        "主旨题抓全文中心，目的题关注写作意图（告知、说服、娱乐等）。看首尾段与各段首句，区分“段落大意”与“全文主旨”，警惕细节冒充主旨。",
        "方法：各段大意叠加→升维概括",
        "把每段用四个词概括，再合并；选项过宽过窄都错。目的题关注读者收获。",
        "说明文主旨常是对象+特征/问题+对策，而非某一例子本身。",
        "主旨题最常见干扰是？",
        ["全面概括", "用细节或过宽表述冒充主旨", "与原文同义改写正确项", "忠于结构"],
        1,
        "细节项与扩得太大的项都是干扰。",
        "常见误区是被首段例子带走，忽略后文观点。",
    ),
    "eng-h-reading-7-choose-5": C(
        "七选五语篇填空",
        "七选五考查语篇连贯：词汇复现、代词指代、逻辑关系与结构线索。先通读留空处前后句，再把选项当“桥梁”检验。",
        "方法：空前空后+代词复现",
        "看空后 this/these/such 指什么；看 meanwhile/however；把候选项代入读是否顺。",
        "空后出现 These methods，则上句应出现复数方法概念。",
        "七选五优先关注？",
        ["字体", "衔接逻辑与指代复现", "选项字母顺序", "是否含生词"],
        1,
        "连贯手段是解题钥匙。",
        "常见误区是只看空前一句，不看空后限制条件。",
    ),
    "eng-h-reading-comprehension-advanced": C(
        "高阶阅读综合",
        "高阶阅读综合细节、推理、主旨、词义与结构题。先快速把握文体与篇章结构，再按题型策略逐题击破，时间分配上先易后难。",
        "方法：结构通读 + 题型切换",
        "记叙抓情节线，说明抓对象特征，议论抓观点态度。做题回扣原文，忌凭记忆。",
        "议论文先框出中心论点句，细节题都围绕是否支持该论点来核对。",
        "综合阅读开篇最应先？",
        ["逐词翻译全篇", "判断文体并把握结构大意", "先做最后一题", "抄写所有生词"],
        1,
        "文体与结构决定阅读路径。",
        "常见误区是平均用力抠每个生词，丢失语篇重心。",
    ),
    "eng-h-cloze-narrative": C(
        "完形填空（记叙型）",
        "记叙型完形重情节发展与情感变化。选项多在名词、动词、形容词间考查逻辑与搭配。通读掌握“谁、何处、何转折”，再逐空验证。",
        "方法：先通读情节再填空",
        "标出转折与结局；每空四步：词性→逻辑→搭配→回读。情感词服务人物弧光。",
        "前文写紧张焦虑，后文释然，空处态度词应前后一致或合理转变。",
        "记叙型完形首先要抓住？",
        ["印刷颜色", "故事线与情感变化", "只选熟悉单词", "忽略连词"],
        1,
        "情节与情感是叙事完形的魂。",
        "常见误区是逐空死磕，不通读导致前后矛盾。",
    ),
    "eng-h-cloze-comprehensive": C(
        "完形填空综合",
        "综合完形可能夹叙夹议或说明。除情节外，还考篇章词汇复现、常识与语法线索。保持“全局意义优先于局部漂亮词”。",
        "方法：复现与逻辑优先",
        "同义/反义复现常是答案提示；语法保证正确，但最终仍要意义成立。",
        "全文反复出现 teamwork，空处近义 collaboration 更贴。",
        "完形选词最终标准是？",
        ["字母排序", "语法正确且语篇意义连贯", "最长单词", "只看本句不管全文"],
        1,
        "意义连贯+语法正确。",
        "常见误区是只盯本句搭配，破坏全文逻辑。",
    ),
    "eng-h-listening-short-h": C(
        "短对话听力",
        "短对话常考数字、地点、关系、请求与弦外之音。听前预读选项预测问题，听时抓第二个说话人关键信息，注意转折与建议句。",
        "方法：预读选项→定位问题类型",
        "数字题记演算；场景题抓关键词（menu/board）；弦外之音听语气与否定。",
        "A: How about the museum? B: I have a paper due. → 委婉拒绝。",
        "短对话听力听前最有用的是？",
        ["闭目养神", "预读选项预测问点", "逐词书写全文", "放弃前两题"],
        1,
        "预读能带着目标听。",
        "常见误区是被第一个说话人信息误导，忽略答语重点。",
    ),
    "eng-h-listening-long-h": C(
        "长对话与独白听力",
        "长对话/独白信息量大，要边听边记关键词：人名、时间线、问题与解决、观点态度。题文同序常见，学会“听一段做一题”的节奏。",
        "方法：题号跟上+符号速记",
        "用箭头、加减号速记；错过一空不纠缠，紧跟下一题。独白注意首尾总结句。",
        "独白开头常给主题，结尾给建议或态度，主旨题多落此处。",
        "长听力过程中更合理的策略是？",
        ["一题卡住反复想", "题文推进，关键信息速记", "不看题只听欣赏", "全部听完再回忆"],
        1,
        "跟题推进并速记更高效。",
        "常见误区是纠结上一题导致连续丢失。",
    ),
    "eng-h-application-letter": C(
        "应用文写作：书信/邮件",
        "应用文要格式规范、目的明确、要点齐全、语气得体。书信/邮件通常：称呼→开门见山说明目的→分点展开→礼貌收尾署名。覆盖命题所有内容要点。",
        "方法：目的句+要点清单",
        "首段点明写信目的；正文用 firstly/also 覆盖要点；结尾期待回复并致谢。",
        "I'm writing to apply for... / I would appreciate it if...",
        "应用文首段最应做的是？",
        ["写无关天气长篇", "清楚说明写作目的", "抄题目所有英文", "只写祝福不表意"],
        1,
        "目的明确是应用文第一要求。",
        "常见误区是要点遗漏，或语气过于口语/不得体。",
    ),
    "eng-h-essay-writing": C(
        "议论文/记叙文写作",
        "议论文：观点清晰、理由分层、例证适度、结尾回扣；记叙文：时间线清楚、细节生动、有冲突与收束。两种文体都要控制审题，避免跑题与中式英语堆砌。",
        "方法：三段/四段提纲先行",
        "议论文：立场→理由1→理由2→总结；记叙文：背景→发展→高潮→感悟（点到为止）。",
        "议论文每段首句主题句，再用 for example 支撑，避免只有口号。",
        "写作前最关键的一步是？",
        ["不审题直接写", "审题并列提纲", "只查生词不构思", "先写结尾华丽句"],
        1,
        "审题与提纲保证不跑偏。",
        "常见误区是记叙变流水账，议论缺理由只有态度。",
    ),
    "eng-h-continuation-writing": C(
        "读后续写",
        "读后续写要求情节合理衔接、人物一致、语言生动，并尽量点题升华。先读原文抓冲突与伏笔，续写两段常有字数与段落提示，须与原文语气风格协调。",
        "方法：定结局方向→伏笔回收→感知描写",
        "列出可回收的物件/对话伏笔；每段有动作+心理+环境；结尾情感自然落点。",
        "前文多次写到一把钥匙，续写可让钥匙推动转折，而非完全另起炉灶。",
        "读后续写最重要的是？",
        ["完全无视原文", "情节衔接与人物一致", "只堆高级单词", "改变原文体裁为说明文"],
        1,
        "衔接与一致性是评分关键。",
        "常见误区是情节断层或人物性格突变。",
    ),
    "eng-h-summary-writing": C(
        "概要写作",
        "概要写作是用简洁语言忠实概括原文要点，不掺个人观点与细节堆砌。先分清原文结构（论点/原因/对策等），再用自己的话改写，注意词数限制与衔接。",
        "方法：骨架句 + 改写压缩",
        "每段一句要点；删除例子与重复；同义改写关键句，保留逻辑词。",
        "原文三段：问题—原因—建议，概要也按此三句连接。",
        "概要写作不应？",
        ["概括主要观点", "加入大量个人评价与细节例子", "控制词数", "使用衔接"],
        1,
        "概要要客观压缩，不添私货。",
        "常见误区是抄原句过多，或写成读后感。",
    ),
}


STYLE = """
<style id="engh-depth-css">
.engh-depth .worked-example{margin:16px 0;padding:16px;border-left:4px solid var(--brand,#38bdf8);background:rgba(56,189,248,.08);border-radius:0 12px 12px 0}
.engh-depth .module-check{margin-top:18px;padding:16px;border-radius:14px;background:rgba(251,146,60,.08);border:1px solid rgba(251,146,60,.28)}
.engh-depth .module-check button{display:block;width:100%;margin:8px 0;text-align:left;border:1px solid var(--line,#233);border-radius:10px;background:#0b1628;color:var(--text,#e5e7eb);padding:11px 13px;cursor:pointer}
.engh-depth .module-check button.correct{border-color:var(--ok,#22c55e);background:rgba(34,197,94,.14)}
.engh-depth .module-check button.wrong{border-color:#f87171;background:rgba(248,113,113,.12)}
.engh-depth .engh-feedback{display:none;margin-top:10px;padding:12px;border-radius:10px;background:rgba(56,189,248,.1)}
.engh-depth .engh-pitfall{margin:14px 0 0;padding:12px;border-radius:10px;background:rgba(248,180,0,.08);border:1px solid rgba(248,180,0,.24)}
</style>
"""

CHECK_SCRIPT = """
<script id="engh-depth-js">
function enghDepthCheck(button, isCorrect, feedbackId, explanation) {
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
    feedback_id = "engh-depth-feedback"
    options = []
    for idx, opt in enumerate(cfg["options"]):
        correct = idx == cfg["correct"]
        handler = "enghDepthCheck(this,{c},'{f}',{e})".format(
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
  <section class="section engh-depth core-knowledge-module text-module" id="lesson-focus"
    data-bloom-level="understand" data-scaffold="full" data-tts="lesson-focus">
    <div class="card">
      <span class="phase-tag">知识精讲</span>
      <h2>{html.escape(cfg['concept_title'])}</h2>
      <p>{html.escape(cfg['concept_body'])}</p>
    </div>
  </section>
</section>
<section class="slide-page" data-page-type="content" data-tsh="方法范例">
  <section class="section engh-depth core-knowledge-module text-module" id="lesson-method"
    data-bloom-level="apply" data-scaffold="partial" data-tts="lesson-method">
    <div class="card">
      <span class="phase-tag">方法与范例</span>
      <h2>{html.escape(cfg['method_title'])}</h2>
      <p>{html.escape(cfg['method_body'])}</p>
      <div class="worked-example"><strong>范例：</strong>{html.escape(cfg['example'])}</div>
      <p id="lesson-pitfall" class="engh-pitfall"><strong>常见误区：</strong>{html.escape(cfg['pitfall'])}</p>
      <div class="module-check" data-conceptest="true">
        <h3>马上练：辨析要点</h3>
        <p>{html.escape(cfg['question'])}</p>
        {''.join(options)}
        <div class="engh-feedback" id="{feedback_id}" role="status"></div>
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
    if 'id="engh-depth-css"' not in source:
        source = source.replace("</head>", STYLE + "\n</head>", 1)
    if 'id="engh-depth-js"' not in source:
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
