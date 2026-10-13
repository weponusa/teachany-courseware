#!/usr/bin/env python3
"""Add topic-specific depth modules to eng-m shell courses.

Middle-school English courses often pass via template sections but lack
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
UPDATED_AT = "2026-08-12"


def C(ct, cb, mt, mb, ex, q, opts, correct, fb, pit):
    return dict(
        concept_title=ct, concept_body=cb, method_title=mt, method_body=mb,
        example=ex, question=q, options=opts, correct=correct, feedback=fb, pitfall=pit,
    )


COURSES = {
    "eng-m-ipa-transcription": C(
        "国际音标入门",
        "国际音标（IPA）用符号表示英语发音，帮助认读生词与区分易混音。学习时先分清元音与辅音，注意长元音/短元音、清浊辅音对立，并结合单词拼读规则。",
        "方法：听辨→跟读→标注",
        "每个新符号配 2–3 个熟词；对比 /i:/ 与 /ɪ/、/θ/ 与 /s/ 等最小对立。查字典先看音标再读。",
        "ship /ʃɪp/ 与 sheep /ʃi:p/ 靠元音长短区分意义。",
        "学习音标的主要目的是？",
        ["代替所有语法", "准确认读与区分发音", "只练书写好看", "取消听力"],
        1,
        "音标服务发音与认读。",
        "常见误区是用汉字注音，导致发音偏差固化。",
    ),
    "eng-m-theme-vocabulary": C(
        "主题词汇",
        "按校园、家庭、社会、自然等主题归类记单词，比散乱背诵更高效。每个主题抓住高频名词、动词与形容词，并记住常用搭配与例句。",
        "方法：主题词网 + 一句活用",
        "画词网：中心主题向外连词；每词写一个自己的句子。复习时按主题默写。",
        "校园主题：homework, classmate, laboratory；搭配 do homework / in the lab。",
        "主题词汇学习更强调？",
        ["完全随机无联系", "归类记忆并在语境中使用", "只背中文意思", "一天背完永不复习"],
        1,
        "归类与语境使用记得更牢。",
        "常见误区是脱离主题与句子，只看词表中译。",
    ),
    "eng-m-word-formation-en": C(
        "构词法：前缀、后缀与合成",
        "初中常见前缀 un-/im-/re-/pre-，后缀 -er/-or/-ful/-less/-ly/-tion 等，以及合成词。会拆词就能猜测词义并扩大词汇量。",
        "方法：拆分定词性",
        "看后缀判词性：-ly 常副词，-ful 常形容词，-er 常“人/物”。前缀常改意义不改词性。",
        "care → careful → carefully；play + ground → playground。",
        "unhappy 中的 un- 表示？",
        ["比较级", "否定", "过去式", "复数"],
        1,
        "un- 常构成否定意义。",
        "常见误区是见到生词不会拆，只会放弃或乱猜。",
    ),
    "eng-m-phrasal-verbs": C(
        "动词短语",
        "动词短语由动词+介词/副词构成，意义常不能按字面相加，如 look after、give up、put on。要整块记忆，并分清及物/不及物与宾语位置（代词宾语常放中间）。",
        "方法：整块记 + 造句",
        "每个短语记中文与一个情景句；注意 turn on the light / turn it on。",
        "Please look after my dog.（照顾）不是“向上看后面”。",
        "动词短语最好怎样记忆？",
        ["把每个词分开孤立背", "作为固定搭配整块记忆并造句", "只记动词本身", "忽略宾语位置"],
        1,
        "整块记忆才能用对。",
        "常见误区是按字面直译，或代词宾语位置放错。",
    ),
    "eng-m-nouns-articles": C(
        "名词、代词与冠词",
        "名词分可数/不可数，注意复数规则；代词代替名词，注意主格宾格与形容词性/名词性物主代词；冠词 a/an/the 与零冠词有使用条件。三者常在同一句子里一起考查。",
        "方法：先判可数再选冠词",
        "可数单数一般要限定词；特指用 the；元音音素开头用 an。物主代词后不再加名词时用 mine/yours。",
        "I have an apple. The apple is sweet. It is mine.",
        "元音音素开头的可数名词单数前常用？",
        ["a", "an", "一律 the", "不能用冠词"],
        1,
        "an 用于元音音素前，如 an hour。",
        "常见误区是按字母不是按音素选 a/an，或 the 滥用。",
    ),
    "eng-m-tenses-present": C(
        "一般现在时与现在进行时",
        "一般现在时表习惯、事实与客观真理，动词用原形或第三人称单数；现在进行时表此刻或现阶段正在进行，结构 be + doing。时间状语是重要线索。",
        "方法：看时间标志选时态",
        "often/usually/every day→一般现在；now/look/listen→现在进行。注意 he/she/it 加 -s/-es。",
        "She usually walks to school, but she is riding a bike now.",
        "Look! The boys ______ football.",
        ["play", "are playing", "plays", "played"],
        1,
        "Look 提示此刻进行，用 are playing。",
        "常见误区是进行时漏 be，或一般现在第三人称单数忘记变形。",
    ),
    "eng-m-tenses-past": C(
        "一般过去时与过去进行时",
        "一般过去时表过去发生的动作或状态，动词用过去式；过去进行时表过去某时刻正在进行，结构 was/were + doing。常在叙事中对比“正在……这时……”。",
        "方法：定点时间用进行，整段经历用一般过去",
        "at 8 last night / when 引导的一点→过去进行；yesterday/last week→一般过去。",
        "I was reading when the phone rang.",
        "表示昨晚八点正在做某事，多用？",
        ["一般现在时", "过去进行时", "一般将来时", "现在完成时"],
        1,
        "过去某时刻正在发生用过去进行时。",
        "常见误区是不规则动词过去式记错，或 when/while 搭配混淆。",
    ),
    "eng-m-tenses-future": C(
        "一般将来时与过去将来时",
        "一般将来时可用 will/shall do 或 be going to do，表将要发生或打算；过去将来时用 would do 或 was/were going to do，常出现在宾语从句中与主句过去时呼应。",
        "方法：看打算还是临时决定，再看主句时态",
        "有计划迹象多用 be going to；转述过去的“将要”用 would。",
        "He said he would call me later.",
        "He said he ______ the next day.",
        ["comes", "would come", "come", "coming"],
        1,
        "主句过去时，从句用过去将来 would come。",
        "常见误区是 will 与 be going to 不分，或宾从时态不呼应。",
    ),
    "eng-m-tenses-perfect": C(
        "现在完成时与过去完成时",
        "现在完成时 have/has + 过去分词，表过去发生对现在仍有影响，或从过去持续到现在；过去完成时 had + 过去分词，表“过去的过去”。注意 for/since 与非延续动词的限制。",
        "方法：先定“现在相关”还是“过去的过去”",
        "already/yet/ever/never/since/for 常提示现在完成；by the time + 一般过去，主句常用过去完成。",
        "She has lived here since 2020. / He had left before I arrived.",
        "since 2020 的句子常用？",
        ["一般过去时 alone", "现在完成时", "过去将来时", "现在进行时 only"],
        1,
        "since 时间点常与现在完成时连用。",
        "常见误区是 have gone to / have been to 混淆，或非延续动词与 for 一段时间误用。",
    ),
    "eng-m-passive-voice": C(
        "被动语态",
        "被动语态强调动作承受者，结构为 be + 过去分词，时态体现在 be 上。主动句宾语变主语，原主语用 by 引出（可省略）。不及物动词一般无被动。",
        "方法：找承受者 + 改 be 的时态",
        "先确认有宾语；再按原时态选 is/was/will be/have been 等，加上过去分词。",
        "They clean the room every day. → The room is cleaned every day.",
        "被动语态的基本结构是？",
        ["do + be", "be + 过去分词", "have + 原形", "to + doing"],
        1,
        "be + 过去分词是被动核心。",
        "常见误区是漏掉 be，或把不及物动词强行变被动。",
    ),
    "eng-m-modal-verbs": C(
        "情态动词 can/may/must/should",
        "情态动词表能力、许可、推测、义务等，后接动词原形。can 能力/许可，may 许可/可能，must 必须/肯定推测，should 应该。注意否定意义差异：mustn't 禁止，needn't 不必。",
        "方法：先定语气功能再选词",
        "问能力用 can；请求许可 can/may；禁止 mustn't；建议 should。",
        "You mustn't smoke here.（禁止）You needn't come tomorrow.（不必）",
        "情态动词后一般接？",
        ["动词-ing 必须", "动词原形", "过去分词 alone", "to do 一律"],
        1,
        "情态动词 + 动词原形。",
        "常见误区是 must 与 have to、mustn't 与 needn't 混淆。",
    ),
    "eng-m-sentence-patterns": C(
        "基本句型与复合句",
        "英语五种基本句型（主谓、主谓宾、主系表等）是造句基础。复合句含两个及以上分句，用并列连词或从属连词连接。先写对简单句，再学习合并成复合句。",
        "方法：抓主干再加从句",
        "先写出主谓（宾），再用 and/but/because/when 等连接。避免逗号连接两句（中式逗号病）。",
        "I stayed at home because it rained.",
        "复合句与简单句的主要区别是？",
        ["单词更长", "含有两个或以上分句", "没有动词", "不能有宾语"],
        1,
        "复合句包含多个分句。",
        "常见误区是用逗号硬接两个完整句，缺少连词。",
    ),
    "eng-m-object-clause": C(
        "宾语从句",
        "宾语从句在句中作宾语，常用 that/if/whether/wh- 引导。注意语序用陈述语序，时态与主句呼应：主句现在时，从句按实际；主句过去时，从句常相应变过去。",
        "方法：连接词 + 陈述语序 + 时态",
        "疑问句变宾从要把助动词还原：What's wrong? → He asked what was wrong.（注意 what 作主语时语序）。",
        "I don't know if he will come. / She said she was tired.",
        "宾语从句的语序应是？",
        ["一律疑问语序", "陈述语序", "任意颠倒", "只有单词无动词"],
        1,
        "宾从用陈述语序。",
        "常见误区是保留疑问语序，或 if/whether 与 that 混用。",
    ),
    "eng-m-attributive-clause": C(
        "定语从句（初中）",
        "定语从句修饰名词，初中重点掌握 that/which/who/whom/whose 等关系词。先找先行词，再看关系词在从句中作主语还是宾语。",
        "方法：先行词是人还是物",
        "人用 who/that，物用 which/that；作宾语时常可省略。句子翻译成“……的”。",
        "The book that I bought is interesting. / The girl who sings well is my sister.",
        "修饰“物”且作从句宾语时，常用？",
        ["who", "which/that", "where 必须", "whose 必须"],
        1,
        "物用 which 或 that。",
        "常见误区是关系词与先行词不一致，或从句缺少成分却不用关系词。",
    ),
    "eng-m-adverbial-clause": C(
        "状语从句（初中）",
        "状语从句表时间、条件、原因、结果、比较、让步等。初中高频连词：when/while/as、if、because、so...that、than、though。注意“主将从现”：条件/时间状语从句用一般现在表将来。",
        "方法：判逻辑关系选连词",
        "条件 if，时间 when，原因 because（不与 so 同用），结果 so...that。",
        "If it rains tomorrow, we will stay home.（从句 rains，主句 will）",
        "If 条件句谈将来，从句时态常用？",
        ["一般将来时 will", "一般现在时", "现在完成时必须", "过去完成时"],
        1,
        "主将从现：从句用一般现在。",
        "常见误区是 because 与 so 连用，或条件从句误用 will。",
    ),
    "eng-m-reading-strategies": C(
        "阅读策略：略读、扫读与精读",
        "略读（skimming）抓大意，扫读（scanning）找特定信息，精读解决细节与难句。按题目选择策略，能提高速度与准确率。",
        "方法：题型决定策略",
        "主旨题先略读首尾；细节题扫读关键词定位；推理题精读相关句。生词先跳过再回看。",
        "问时间地点，用扫读找数字与大写；问文章大意，看标题与首段。",
        "寻找某个具体数字信息，优先用？",
        ["精读每个生词", "扫读", "放弃文章", "只看最后一句"],
        1,
        "扫读适合定位具体信息。",
        "常见误区是一律逐词翻译，既慢又易断章取义。",
    ),
    "eng-m-text-types": C(
        "语篇类型：记叙、说明与议论",
        "记叙文讲故事，有人物情节；说明文介绍事物特征或事理；议论文表达观点并说理。识别类型有助于预测内容与答题方向。",
        "方法：看结构信号",
        "记叙找时间线；说明找定义—特征—例子；议论找观点—理由。选项表述要符合文体。",
        "How does a volcano form? 多为说明；In my opinion... 偏议论。",
        "以讲故事、写经历为主的语篇通常是？",
        ["说明文", "记叙文", "议论文唯一", "词典条目"],
        1,
        "记叙文以叙事为主。",
        "常见误区是把说明文中的例子当成全文主旨。",
    ),
    "eng-m-cloze-test": C(
        "完形填空（初中）",
        "初中完形多记叙，考查词汇、搭配与上下文逻辑。先通读了解大意，再选词，最后复查情节是否通顺。",
        "方法：通读→逻辑→搭配",
        "利用前后句线索；同义复现常是提示；动词看时态，名词看可数与冠词。",
        "前文提到 birthday party，后空选 gift/cake 等更合语境。",
        "做完形填空第一步最好是？",
        ["逐空立刻选定", "通读全文了解大意", "只看选项不看文章", "从最后一空做起且不回头"],
        1,
        "先通读再填更准。",
        "常见误区是只看空格本句，不顾全文感情色彩与情节。",
    ),
    "eng-m-listening-basic": C(
        "基础听力：对话与短文",
        "基础听力抓 who/what/where/when/how。听前读选项预测，听中抓关键词，听后迅速选题。注意数字、时间与转折词 but。",
        "方法：预读选项定焦点",
        "选项都是地点就盯场景词；都是时间就盯钟点。第二遍核对。",
        "A: Where is Tom? B: He is in the library. → 抓 library。",
        "听力开始前最有用的准备是？",
        ["不看题", "快速预读选项预测问题", "背诵全文脚本", "关闭注意力"],
        1,
        "预读能带着目标听。",
        "常见误区是被干扰信息带走，忽略答语中的关键事实。",
    ),
    "eng-m-listening-long": C(
        "长对话与语段听力",
        "信息量更大时，要学会边听边记：人名、时间顺序、问题与建议。题目通常按听力顺序出现，错过一题立即跟上下一题。",
        "方法：题号推进 + 符号笔记",
        "用箭头表示先后，用 +/- 表示态度。独白注意开头主题句与结尾总结。",
        "长对话先谈计划再改时间，答案常在更正后的信息。",
        "长听力中某一题没听清时应该？",
        ["一直想这题错过后面", "先放下并跟上后面题目", "停止听力", "放弃整套"],
        1,
        "不要因一题丢掉后面连续信息。",
        "常见误区是纠缠上一空导致连锁失误。",
    ),
    "eng-m-basic-writing": C(
        "基础写作：短文、书信与邮件",
        "初中写作要求要点齐全、句子正确、格式得体。书信/邮件有称呼与结尾；短文按提示逐点写，注意时态与人称一致，适当使用连词使文章连贯。",
        "方法：审题列点→造句→连接",
        "把中文提示变成英文要点清单；每点 1–2 句；用 and/but/because/first 连接；写完检查三单与时态。",
        "邮件首句：I'm writing to tell you about my school life.",
        "写作最容易失分的原因之一是？",
        ["字迹清楚", "漏写内容要点或时态混乱", "有称呼", "适当连词"],
        1,
        "要点与时态是基础得分点。",
        "常见误区是逐字中式翻译，或书信格式缺失。",
    ),
    "eng-m-oral-topic": C(
        "话题口语表达",
        "话题口语要听清问题，用完整句回答，并补充 1–2 句细节。常用开场、举例与结尾套话，发音清楚、语速适中。主题涉及学校、爱好、家乡、计划等。",
        "方法：三句式回答",
        "第一句直接答；第二句给原因/例子；第三句小结或感受。不会的词换简单说法。",
        "Q: What's your hobby? A: I like reading. I read every evening. It makes me happy.",
        "口语答题较好的结构是？",
        ["只答一个单词结束", "直接回答并补充细节", "长时间沉默", "完全用中文"],
        1,
        "完整句+细节更清晰得体。",
        "常见误区是只回 yes/no，或背诵与问题无关的段落。",
    ),
}


STYLE = """
<style id="engm-depth-css">
.engm-depth .worked-example{margin:16px 0;padding:16px;border-left:4px solid var(--brand,#38bdf8);background:rgba(56,189,248,.08);border-radius:0 12px 12px 0}
.engm-depth .module-check{margin-top:18px;padding:16px;border-radius:14px;background:rgba(251,146,60,.08);border:1px solid rgba(251,146,60,.28)}
.engm-depth .module-check button{display:block;width:100%;margin:8px 0;text-align:left;border:1px solid var(--line,#233);border-radius:10px;background:#0b1628;color:var(--text,#e5e7eb);padding:11px 13px;cursor:pointer}
.engm-depth .module-check button.correct{border-color:var(--ok,#22c55e);background:rgba(34,197,94,.14)}
.engm-depth .module-check button.wrong{border-color:#f87171;background:rgba(248,113,113,.12)}
.engm-depth .engm-feedback{display:none;margin-top:10px;padding:12px;border-radius:10px;background:rgba(56,189,248,.1)}
.engm-depth .engm-pitfall{margin:14px 0 0;padding:12px;border-radius:10px;background:rgba(248,180,0,.08);border:1px solid rgba(248,180,0,.24)}
</style>
"""

CHECK_SCRIPT = """
<script id="engm-depth-js">
function engmDepthCheck(button, isCorrect, feedbackId, explanation) {
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
    feedback_id = "engm-depth-feedback"
    options = []
    for idx, opt in enumerate(cfg["options"]):
        correct = idx == cfg["correct"]
        handler = "engmDepthCheck(this,{c},'{f}',{e})".format(
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
  <section class="section engm-depth core-knowledge-module text-module" id="lesson-focus"
    data-bloom-level="understand" data-scaffold="full" data-tts="lesson-focus">
    <div class="card">
      <span class="phase-tag">知识精讲</span>
      <h2>{html.escape(cfg['concept_title'])}</h2>
      <p>{html.escape(cfg['concept_body'])}</p>
    </div>
  </section>
</section>
<section class="slide-page" data-page-type="content" data-tsh="方法范例">
  <section class="section engm-depth core-knowledge-module text-module" id="lesson-method"
    data-bloom-level="apply" data-scaffold="partial" data-tts="lesson-method">
    <div class="card">
      <span class="phase-tag">方法与范例</span>
      <h2>{html.escape(cfg['method_title'])}</h2>
      <p>{html.escape(cfg['method_body'])}</p>
      <div class="worked-example"><strong>范例：</strong>{html.escape(cfg['example'])}</div>
      <p id="lesson-pitfall" class="engm-pitfall"><strong>常见误区：</strong>{html.escape(cfg['pitfall'])}</p>
      <div class="module-check" data-conceptest="true">
        <h3>马上练：辨析要点</h3>
        <p>{html.escape(cfg['question'])}</p>
        {''.join(options)}
        <div class="engm-feedback" id="{feedback_id}" role="status"></div>
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
    if 'id="engm-depth-css"' not in source:
        source = source.replace("</head>", STYLE + "\n</head>", 1)
    if 'id="engm-depth-js"' not in source:
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
