#!/usr/bin/env python3
"""Fix failing chn-e (小学语文) courses.

Heterogeneous failures: text < 1800, substantial sections < 5, one course lacks
a pretest, one lacks a 3rd visualization unit (B-3a). Each course gets three
substantial modules (精讲 / 方法范例含诊断与常见误区 / 拓展应用); optionally an
interactive <canvas> (B-3a) and a pretest section (learning loop). No mp4.
Idempotent via id="lesson-focus".
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COURSE_VERSION = "1.1.0"
UPDATED_AT = "2026-08-09"


def C(ct, cb, mt, mb, ex, q, opts, correct, fb, pit, et, eb, canvas=False, pretest=None):
    return dict(concept_title=ct, concept_body=cb, method_title=mt, method_body=mb,
                example=ex, question=q, options=opts, correct=correct, feedback=fb,
                pitfall=pit, ext_title=et, ext_body=eb, canvas=canvas, pretest=pretest)


COURSES = {
    "chn-e-poetry-appreciation": C(
        "古诗鉴赏：读懂诗意、体会诗情", "鉴赏古诗要先读懂诗句的意思，再体会诗人表达的思想感情。可以按“知诗人、解诗题、明诗意、悟诗情”的步骤：了解作者和写作背景，理解题目和字词，说出诗句大意，最后体会诗中蕴含的情感和道理。",
        "方法：抓关键词、想象画面", "鉴赏时抓住诗中的关键字词和描写的景物，边读边在头脑中想象画面；联系诗人的处境和写作背景，体会借景抒情、情景交融的表达。说感受时先概括情感，再结合诗句说明，做到有理有据。",
        "读《静夜思》，抓住“明月”“霜”“故乡”，想象诗人月夜独立、思念家乡的画面，体会浓浓的思乡之情。",
        "鉴赏古诗，体会诗情前首先要做到？", ["背下全诗", "读懂诗句意思", "数有几句", "看字数多少"], 1,
        "先读懂诗意，才能进一步体会诗人的情感。",
        "常见误区是把古诗鉴赏当成逐字翻译或死记硬背，只说“写得美”却讲不出美在哪里。应按知人、解题、明意、悟情的步骤，抓关键词、想象画面，结合诗句体会情感。",
        "拓展应用：古诗与生活", "古诗离我们并不遥远，很多诗句已成为常用的表达。遇到月圆之夜会想到“但愿人长久，千里共婵娟”，看到春雨会想起“随风潜入夜，润物细无声”。学习古诗时，可以把诗句和自己的生活体验联系起来，在合适的情境中吟诵、运用，既能加深理解，又能感受中华古诗词的魅力，让古诗成为我们表达情感、积累语言的宝库。",
        canvas=True),
    "chn-e-poetry-imagery": C(
        "古诗意象：景物寄托情感", "意象是古诗中带有作者情感的景物。很多景物有相对固定的含义，如“月”常寄托思念、“柳”表示惜别、“梅”象征高洁。读懂意象的含义，就找到了体会古诗情感的钥匙。",
        "方法：由景物想情感", "读古诗先找出诗中写到的景物（意象），回忆它们常见的含义，再结合诗句体会诗人借这些景物表达的情感。不要脱离诗境生搬硬套，要联系整首诗和作者心情来理解。",
        "“遥知兄弟登高处，遍插茱萸少一人”借“茱萸”这一意象，表达了诗人重阳佳节思念亲人的感情。",
        "古诗中的“意象”指的是？", ["单纯的景物", "寄托了作者情感的景物", "诗的题目", "诗的字数"], 1,
        "意象是融入了作者情感的景物。",
        "常见误区是把意象当成普通景物，或生硬套用固定含义而不看诗境。应结合整首诗和诗人心情来理解意象，做到由景物想到情感。",
        "拓展应用：积累常见意象", "学习古诗可以分类积累常见意象及其含义，如“明月”多表思乡怀人、“流水”常喻时光流逝、“梅兰竹菊”象征高洁品格、“杨柳”寄托离别之情。读到新的古诗时，先圈出其中的意象，想一想它带来怎样的感受，再联系全诗体会情感。日积月累，我们对古诗意象就会越来越熟悉，读懂古诗、感受诗情也会越来越容易。"),
    "chn-e-poetry-rhythm": C(
        "古诗的节奏与韵律", "古诗读起来朗朗上口，是因为它有整齐的节奏和押韵。朗读古诗要读准节奏，五言诗常按“二三”或“二二一”停顿，七言诗常按“二二三”停顿；押韵是诗句末尾用韵母相同或相近的字，读起来和谐动听。",
        "方法：划节奏、读韵脚", "朗读前先给诗句划分节奏、找出韵脚。按意义和音节停顿，不读破词语；朗读时读出韵脚的呼应，注意语调的抑扬和感情的表达，做到有节奏、有感情，在诵读中体会古诗的音韵之美。",
        "“床前/明月/光，疑是/地上/霜”按二二一停顿，“光”“霜”“乡”押 ang 韵，读来和谐上口。",
        "朗读七言诗，常见的节奏划分是？", ["二二三", "一二一", "三三一", "随意停顿"], 0,
        "七言诗常按“二二三”的节奏停顿朗读。",
        "常见误区是朗读古诗时把词语读破、忽视节奏和押韵，读成一字一顿或平淡无味。应先划分节奏、找出韵脚，按意义停顿，读出韵律和感情。",
        "拓展应用：在诵读中积累", "古诗的节奏和韵律最适合通过反复诵读来体会。我们可以先听老师或录音范读，再模仿着读，读准字音和停顿；熟读之后尝试背诵，感受诗句的整齐和押韵之美。还可以给古诗配上简单的拍手节奏，或和同学分组对读、接龙，让诵读变得有趣。坚持诵读积累，不仅能记住许多古诗，还能培养良好的语感，为今后的语文学习打下基础。",
        pretest={
            "question": "下面哪一项是朗读古诗时需要注意的？",
            "options": ["读得越快越好", "读准节奏、读出韵律", "不用管停顿", "声音越大越好"],
            "correct": 1,
            "feedback": "朗读古诗要读准节奏、读出韵律和感情。",
        }),
    "chn-e-rhetoric-in-writing": C(
        "写作中的修辞：让语言更生动", "在写作中恰当运用修辞，能使语言更加生动形象、富有感染力。常用的修辞有比喻、拟人、排比、夸张等：比喻能把事物写得具体可感，拟人能让事物有人的情态，排比能增强语势，夸张能突出特点。",
        "方法：按需选用、贴切自然", "写作时根据表达的需要选用修辞：要写得形象就用比喻、拟人，要增强气势就用排比。用修辞要贴切自然、不生搬硬套，比喻要找准相似点，拟人要符合情境，让修辞真正为表达内容和情感服务。",
        "“小草偷偷地从土里钻出来”用拟人，把小草写得活泼可爱；“弯弯的月亮像小船”用比喻，写出月亮的形状。",
        "“太阳公公露出了笑脸”运用了哪种修辞？", ["比喻", "拟人", "排比", "夸张"], 1,
        "把太阳当作人来写，是拟人修辞。",
        "常见误区是为用修辞而堆砌修辞，比喻找不准相似点、拟人不合情境，反而显得生硬。应根据表达需要恰当选用，做到贴切自然，让修辞为内容和情感服务。",
        "拓展应用：在片段中练修辞", "学会修辞后，可以在写景、状物、写人的片段中有意识地练习。写一处景物时，试着用一个比喻和一个拟人，让画面更生动；写一段感受时，用排比增强气势。写完后读一读，检查修辞是否贴切、是否帮助表达了自己的意思。平时多留心课文中优美的修辞句，摘抄下来仿写，日积月累，我们的语言就会越来越生动、越来越有表现力。"),
    "chn-e-sentence-expansion": C(
        "句子扩写：把句子写具体", "扩写句子就是在保持原意的基础上，添加恰当的修饰成分，把句子写得更具体、更生动。可以在“谁、做什么、什么样”上加修饰，回答“怎样地、什么样的、在哪里、什么时候”等问题，使句子内容更丰富。",
        "方法：抓主干、添修饰", "扩写先找出句子的主干（谁+做什么），再想一想可以补充哪些内容：给人物或事物加上修饰语（什么样的），给动作加上状语（怎样地、在哪里、什么时候）。添加的内容要合理、通顺，不改变句子的原意。",
        "把“花开了”扩写成“春天来了，公园里五颜六色的花儿争先恐后地开放了”，句子就变得具体生动。",
        "扩写句子时必须做到？", ["改变原来的意思", "保持原意，添加修饰使句子具体", "越短越好", "去掉主语"], 1,
        "扩写要在不改变原意的前提下，添加修饰使句子更具体。",
        "常见误区是扩写时改变了句子原意，或随意堆砌华丽词语导致句子啰嗦不通。应先抓住主干，再合理添加修饰成分，做到内容具体、语句通顺、原意不变。",
        "拓展应用：多角度扩写", "同一个简单句子，可以从不同角度扩写。以“鸟儿飞”为例：加上样子可写“美丽的小鸟”，加上方式可写“自由自在地飞”，加上地点时间可写“清晨在蓝天上飞”，合起来就是“清晨，美丽的小鸟在蓝天上自由自在地飞翔”。练习时可以先一次只添加一个方面，再把它们组合起来，逐步把句子写具体。多做这样的练习，写作时就能把话说得更清楚、更生动。"),
    "chn-e-summarization": C(
        "归纳概括：抓住主要内容", "归纳概括就是用简练的语言说出一段话或一篇文章的主要内容。它要求我们读懂内容、分清主次，抓住主要人物和事件，去掉次要的细节，把长的内容变短，把复杂的内容说清楚。",
        "方法：找要素、连成句", "概括记叙性内容可抓住“谁、在什么情况下、做了什么、结果怎样”这些要素，再把它们连成通顺的一句话或一段话。概括说明性内容则抓住说明的对象和主要特点。概括要完整、准确、简练，不遗漏要点也不啰嗦。",
        "一段讲“小明帮助迷路的老人找到回家的路”的文字，可概括为：小明帮助迷路的老人回了家。",
        "归纳文章的主要内容，正确的做法是？", ["原文照抄", "抓住主要人物和事件，简练表达", "只写一个词", "加入自己的想象"], 1,
        "概括要抓住主要人物和事件，用简练的语言表达。",
        "常见误区是概括时照抄原文、面面俱到，或丢掉主要事件只写细节。应分清主次，抓住主要人物和事件，用自己的话简练、准确地表达，不遗漏要点也不啰嗦。",
        "拓展应用：分层概括法", "遇到较长的文章，可以用“分层概括”的方法：先把文章分成几个部分，用一句话概括每一部分的意思，再把各部分的意思合起来，就得到全文的主要内容。概括时注意保留主要人物、事件和结果，去掉举例、描写等次要内容。概括完读一读，看是否通顺、是否说清了主要内容。经常练习分层概括，不仅能提高阅读理解能力，也能帮助我们把话说得有条理、有重点。"),
}


STYLE = """
<style id="chne-depth-css">
.chne-depth .worked-example{margin:16px 0;padding:16px;border-left:4px solid var(--brand,#38bdf8);background:rgba(56,189,248,.08);border-radius:0 12px 12px 0}
.chne-depth .module-check{margin-top:18px;padding:16px;border-radius:14px;background:rgba(251,146,60,.08);border:1px solid rgba(251,146,60,.24)}
.chne-depth .module-check button{display:block;width:100%;margin:8px 0;text-align:left;border:1px solid var(--line,#233);border-radius:10px;background:#0b1628;color:var(--text,#e5e7eb);padding:11px 13px;cursor:pointer}
.chne-depth .module-check button.correct{border-color:var(--ok,#22c55e);background:rgba(34,197,94,.14)}
.chne-depth .module-check button.wrong{border-color:#f87171;background:rgba(248,113,113,.12)}
.chne-depth .chne-feedback{display:none;margin-top:10px;padding:12px;border-radius:10px;background:rgba(56,189,248,.1)}
.chne-depth .chne-pitfall{margin:14px 0 0;padding:12px;border-radius:10px;background:rgba(248,180,0,.08);border:1px solid rgba(248,180,0,.24)}
.chne-depth .chne-canvas{width:100%;max-width:560px;height:auto;background:#0b1628;border:1px solid rgba(148,163,184,.28);border-radius:12px;display:block;margin:8px auto 0}
</style>
"""

CHECK_SCRIPT = """
<script id="chne-depth-js">
function chneDepthCheck(button, isCorrect, feedbackId, explanation) {
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
(function () {
  function draw(cv) {
    var ctx = cv.getContext('2d'); var W = cv.width, H = cv.height;
    ctx.clearRect(0, 0, W, H);
    ctx.font = '15px sans-serif'; ctx.textAlign = 'center';
    // 节奏/停顿示意：把诗句音节画成带停顿的方块
    var tokens = ['床前', '·', '明月', '·', '光'];
    var x = 30, y = H / 2;
    ctx.fillStyle = '#e5e7eb';
    ctx.fillText('朗读节奏示意：床前 / 明月 / 光', W / 2, 30);
    tokens.forEach(function (t) {
      if (t === '·') { ctx.fillStyle = '#f472b6'; ctx.fillText('/', x + 12, y + 6); x += 26; return; }
      ctx.fillStyle = 'rgba(56,189,248,.22)'; ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 2;
      var w = 64; ctx.fillRect(x, y - 22, w, 44); ctx.strokeRect(x, y - 22, w, 44);
      ctx.fillStyle = '#e5e7eb'; ctx.fillText(t, x + w / 2, y + 6); x += w + 8;
    });
    ctx.fillStyle = '#94a3b8'; ctx.fillText('“光/霜/乡”押 ang 韵，读来和谐上口', W / 2, H - 20);
  }
  function init() { document.querySelectorAll('canvas.chne-canvas').forEach(draw); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
</script>
"""


def build_block(cfg: dict, course_id: str) -> str:
    feedback_id = "chne-depth-feedback"
    options = []
    for idx, opt in enumerate(cfg["options"]):
        correct = idx == cfg["correct"]
        handler = "chneDepthCheck(this,{c},'{f}',{e})".format(
            c="true" if correct else "false", f=feedback_id,
            e=json.dumps(cfg["feedback"], ensure_ascii=False))
        options.append(
            '<button type="button" data-correct="{flag}" onclick="{h}">{letter}. {opt}</button>'.format(
                flag="1" if correct else "0", h=html.escape(handler, quote=True),
                letter=chr(65 + idx), opt=html.escape(opt)))

    pretest_html = ""
    if cfg.get("pretest"):
        pt = cfg["pretest"]
        pt_opts = []
        for idx, opt in enumerate(pt["options"]):
            correct = idx == pt["correct"]
            handler = "chneDepthCheck(this,{c},'chne-pretest-feedback',{e})".format(
                c="true" if correct else "false",
                e=json.dumps(pt["feedback"], ensure_ascii=False))
            pt_opts.append(
                '<button type="button" data-correct="{flag}" onclick="{h}">{letter}. {opt}</button>'.format(
                    flag="1" if correct else "0", h=html.escape(handler, quote=True),
                    letter=chr(65 + idx), opt=html.escape(opt)))
        pretest_html = f"""
<section class="slide-page" data-page-type="content" data-tsh="前测">
  <section class="section chne-depth" id="pretest" data-tts="pretest">
    <div class="card">
      <span class="phase-tag">课前前测</span>
      <h2>学前小测：你已经知道多少？</h2>
      <div class="module-check" data-conceptest="true">
        <p>{html.escape(pt['question'])}</p>
        {''.join(pt_opts)}
        <div class="chne-feedback" id="chne-pretest-feedback" role="status"></div>
      </div>
    </div>
  </section>
</section>
"""

    canvas_html = ""
    if cfg.get("canvas"):
        canvas_html = f"""
      <canvas class="chne-canvas" id="chne-canvas-{course_id}" width="560" height="220"
        role="img" aria-label="朗读节奏示意"></canvas>"""

    return f"""{pretest_html}
<section class="slide-page" data-page-type="content" data-tsh="精讲">
  <section class="section chne-depth core-knowledge-module" id="lesson-focus"
    data-bloom-level="understand" data-scaffold="full" data-tts="lesson-focus">
    <div class="card">
      <span class="phase-tag">知识精讲</span>
      <h2>{html.escape(cfg['concept_title'])}</h2>
      <p>{html.escape(cfg['concept_body'])}</p>
    </div>
  </section>
</section>
<section class="slide-page" data-page-type="content" data-tsh="方法范例">
  <section class="section chne-depth core-knowledge-module" id="lesson-method"
    data-bloom-level="apply" data-scaffold="partial" data-tts="lesson-method">
    <div class="card">
      <span class="phase-tag">方法与范例</span>
      <h2>{html.escape(cfg['method_title'])}</h2>
      <p>{html.escape(cfg['method_body'])}</p>
      <div class="worked-example"><strong>范例：</strong>{html.escape(cfg['example'])}</div>
      <p id="lesson-pitfall" class="chne-pitfall"><strong>常见误区：</strong>{html.escape(cfg['pitfall'])}</p>
      <div class="module-check" data-conceptest="true">
        <h3>马上练：辨析要点</h3>
        <p>{html.escape(cfg['question'])}</p>
        {''.join(options)}
        <div class="chne-feedback" id="{feedback_id}" role="status"></div>
      </div>
    </div>
  </section>
</section>
<section class="slide-page" data-page-type="content" data-tsh="拓展应用">
  <section class="section chne-depth core-knowledge-module" id="lesson-extend"
    data-bloom-level="apply" data-scaffold="partial" data-tts="lesson-extend">
    <div class="card">
      <span class="phase-tag" data-variant="success">拓展应用</span>
      <h2>{html.escape(cfg['ext_title'])}</h2>
      <p>{html.escape(cfg['ext_body'])}</p>{canvas_html}
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
    block = build_block(cfg, course_id)
    source = source[:insert_at] + block + "\n" + source[insert_at:]
    if 'id="chne-depth-css"' not in source:
        source = source.replace("</head>", STYLE + "\n</head>", 1)
    if 'id="chne-depth-js"' not in source:
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
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True, "3 modules + extras"


def main() -> int:
    changed = failed = 0
    for course_id, cfg in COURSES.items():
        ok, msg = upgrade(course_id, cfg)
        if ok:
            changed += 1
        elif msg == "already upgraded":
            print(f"SKIP {course_id}: {msg}")
        else:
            failed += 1
            print(f"FAIL {course_id}: {msg}")
    print(f"done: changed={changed} failed={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
