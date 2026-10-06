#!/usr/bin/env python3
"""Add two core-knowledge modules to the remaining assorted failing courses.

Covers 5 singletons failing with module_like < 3 and 3 sci-e courses failing
with substantial sections < 5. Two modules (精讲 + 方法范例含诊断与常见误区)
per course satisfy both. No mp4. Idempotent via id="lesson-focus".
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COURSE_VERSION = "1.1.0"
UPDATED_AT = "2026-08-09"


def C(ct, cb, mt, mb, ex, q, opts, correct, fb, pit):
    return dict(concept_title=ct, concept_body=cb, method_title=mt, method_body=mb,
                example=ex, question=q, options=opts, correct=correct, feedback=fb, pitfall=pit)


COURSES = {
    "ext-3966191-urban-drainage": C(
        "城市排水与内涝：从管网到海绵城市", "城市排水系统负责及时排走雨水和污水，防止内涝和污染。传统做法主要依靠管网、泵站快速把雨水排走，但硬化地面过多会使雨水下渗减少、径流增大，暴雨时容易发生城市内涝。海绵城市理念主张让城市像海绵一样，能吸水、蓄水、渗水、净水，需要时再把蓄存的水释放利用。",
        "方法：源头减排、过程蓄滞、末端排放", "缓解城市内涝要多措并举：源头上建设透水铺装、下沉式绿地、雨水花园增加下渗；过程中用调蓄池、植草沟滞留雨水、削减洪峰；末端完善管网和排涝设施。分析某地内涝问题时，先找出硬化过度、管网不足等原因，再对症提出综合治理措施。",
        "某老城区暴雨后积水严重，改造时增加透水砖和下沉绿地、清疏管网并新建调蓄池，内涝明显减轻。",
        "海绵城市理念的核心是？", ["尽快把雨水排走", "让城市能吸、蓄、渗、净、用水", "多建高楼", "填埋所有河道"], 1,
        "海绵城市强调吸、蓄、渗、净、用水，而非一排了之。",
        "常见误区是认为治理内涝只要加粗管网、加快排水即可。应认识到过度硬化是内涝的重要原因，需坚持源头减排、过程蓄滞、末端排放相结合，用海绵城市理念综合治理。"),
    "geography-earth-shape-size": C(
        "地球的形状与大小", "地球是一个两极稍扁、赤道略鼓的不规则球体。人类对地球形状的认识经历了“天圆地方”到“球体”的漫长过程，麦哲伦船队环球航行、卫星照片等提供了地球是球体的确凿证据。地球的平均半径约6371千米，赤道周长约4万千米，表面积约5.1亿平方千米。",
        "方法：用证据说明地球形状", "说明地球是球体，可举出多种证据：远处驶来的帆船先见桅杆后见船身、月食时地球投在月面的影子是圆弧、登高望远看得更远、环球航行、卫星照片等。记忆地球大小的数据时，可抓住“半径六千多千米、周长约四万千米”等关键数字。",
        "站在海边看远方来船，总是先看到桅杆再看到船身，这说明海面是弯曲的，是地球为球体的证据之一。",
        "下列能说明地球是球体的证据是？", ["天空是蓝色的", "远方帆船先见桅杆后见船身", "白天黑夜交替", "四季变化"], 1,
        "帆船先见桅杆后见船身，说明地表是弯曲的球面。",
        "常见误区是把地球当成正球体，或只凭直觉认为大地是平的。应认识到地球是两极稍扁的不规则球体，并能用帆船、月食、环球航行、卫星照片等证据加以说明。"),
    "hist-m-russian-revolution": C(
        "俄国十月革命：世界上第一个社会主义国家", "1917年，俄国爆发十月革命，在列宁领导下，布尔什维克党推翻资产阶级临时政府，建立了世界上第一个无产阶级专政的国家——苏维埃俄国。十月革命是人类历史上第一次胜利的社会主义革命，它把社会主义从理论变为现实，对世界历史进程产生了深远影响。",
        "方法：从背景、过程、意义把握革命", "分析十月革命可从背景（一战加剧社会矛盾、二月革命后两个政权并存）、过程（列宁提出《四月提纲》、彼得格勒武装起义）和意义（建立第一个社会主义国家、鼓舞世界被压迫民族）三方面梳理，理解其历史必然性和世界意义。",
        "1917年11月7日（俄历十月），彼得格勒武装起义攻占冬宫，推翻临时政府，宣告苏维埃政权建立。",
        "十月革命最重要的历史意义是？", ["结束了第一次世界大战", "建立了世界上第一个社会主义国家", "统一了欧洲", "废除了农奴制"], 1,
        "十月革命建立了世界上第一个社会主义国家，意义深远。",
        "常见误区是把二月革命和十月革命混为一谈，或忽视其世界意义。应分清二月革命推翻沙皇专制、十月革命推翻资产阶级临时政府建立社会主义国家，并认识其对世界历史的深远影响。"),
    "math-quadratic-function": C(
        "二次函数的图象与性质", "形如 y=ax²+bx+c（a≠0）的函数是二次函数，其图象是抛物线。a 决定开口方向和大小：a>0 开口向上、有最小值，a<0 开口向下、有最大值。抛物线的对称轴是直线 x=-b/(2a)，顶点坐标为 (-b/2a, (4ac-b²)/4a)。",
        "方法：配方法求顶点与最值", "研究二次函数常用配方法把一般式化为顶点式 y=a(x-h)²+k，直接读出顶点(h,k)、对称轴 x=h 和最值 k。结合 a 的符号判断开口方向和增减性；求与坐标轴交点时，令 x=0 求与 y 轴交点、令 y=0 解方程求与 x 轴交点。",
        "把 y=x²-4x+3 配方得 y=(x-2)²-1，顶点为(2,-1)，对称轴 x=2，开口向上，最小值为-1。",
        "二次函数 y=ax²+bx+c 的对称轴是？", ["x=-b/(2a)", "x=b/(2a)", "x=-c/a", "x=a"], 0,
        "抛物线的对称轴是直线 x=-b/(2a)。",
        "常见误区是把二次函数当一次函数处理，或求最值时忘记 a 的符号决定是最大值还是最小值。应用配方法求顶点，先由 a 的符号判断开口方向，再确定最值和增减性。"),
    "teachany-phy-mid-pressure": C(
        "压强：压力的作用效果", "压强是表示压力作用效果的物理量，等于物体所受压力与受力面积之比：p=F/S，单位是帕斯卡（Pa）。在压力一定时，受力面积越小，压强越大；在受力面积一定时，压力越大，压强越大。液体内部也存在压强，且随深度增加而增大。",
        "方法：用 p=F/S 分析增减压强", "分析压强问题先分清压力 F 和受力面积 S，代入 p=F/S 计算。要增大压强可增大压力或减小受力面积（如刀刃磨薄）；要减小压强可减小压力或增大受力面积（如宽履带、书包宽背带）。注意压力方向垂直于受力面。",
        "菜刀磨得锋利，是在压力一定时减小受力面积来增大压强，使切割更省力；铁轨铺在枕木上则是增大受力面积减小压强。",
        "在压力一定时，要增大压强应该？", ["增大受力面积", "减小受力面积", "改变力的方向", "保持面积不变"], 1,
        "压力一定时，减小受力面积可增大压强。",
        "常见误区是把压力和压强混为一谈，或忽视受力面积的影响。应用 p=F/S 分析：压强既取决于压力，也取决于受力面积，要通过改变压力或面积来调节压强。"),
    "sci-e-disease-prevention": C(
        "疾病预防与卫生习惯", "传染病是由病原体（细菌、病毒等）引起、能在人与人之间传播的疾病。传染病流行需要三个环节：传染源、传播途径和易感人群。预防传染病要针对这三个环节：控制传染源、切断传播途径、保护易感人群。养成良好卫生习惯是预防疾病的重要方式。",
        "方法：从三个环节预防疾病", "预防传染病可从三方面着手：及时隔离和治疗病人（控制传染源）；勤洗手、戴口罩、通风消毒、不随地吐痰（切断传播途径）；加强锻炼、合理营养、按时接种疫苗（保护易感人群）。分析某种传染病的预防措施时，先判断它属于哪个环节。",
        "流感季节勤洗手、戴口罩、开窗通风属于切断传播途径，接种流感疫苗则是保护易感人群。",
        "接种疫苗预防传染病，属于哪个环节？", ["控制传染源", "切断传播途径", "保护易感人群", "消灭病原体"], 2,
        "接种疫苗使人获得免疫力，属于保护易感人群。",
        "常见误区是把所有预防措施都当成“消毒杀菌”，分不清预防环节。应从控制传染源、切断传播途径、保护易感人群三个环节分析预防措施，做到有针对性。"),
    "sci-e-solar-system": C(
        "太阳系与行星运动", "太阳系以太阳为中心，包括八大行星及其卫星、矮行星、小行星、彗星等天体。八大行星按离太阳由近到远依次是水星、金星、地球、火星、木星、土星、天王星、海王星，它们都绕太阳沿椭圆轨道自西向东公转，同时自转。太阳是太阳系中唯一的恒星，自身能发光发热。",
        "方法：按顺序和特征认识行星", "认识太阳系要记住八大行星的顺序，并把握其特征：靠近太阳的水金地火是类地行星，体积小、密度大；木星、土星是巨行星，体积大、主要由气体组成。区分恒星、行星和卫星：恒星自身发光，行星绕恒星转，卫星绕行星转。",
        "月球本身不发光，我们看到的月光是它反射的太阳光；月球绕地球转，地球绕太阳转。",
        "下列关于太阳系的说法正确的是？", ["月球是行星", "八大行星都绕太阳公转", "太阳绕地球转", "行星自身发光"], 1,
        "八大行星都绕太阳沿椭圆轨道公转。",
        "常见误区是把月球当行星、把行星当作自身发光的天体。应分清恒星（自身发光，如太阳）、行星（绕恒星转，如地球）和卫星（绕行星转，如月球）的区别。"),
    "sci-e-tools-use": C(
        "常见工具的使用与简单机械", "生活中的许多工具应用了简单机械的原理，能帮助我们省力或方便工作。杠杆、滑轮、斜面、轮轴是常见的简单机械：撬棍、剪刀是杠杆，旗杆顶上的定滑轮能改变力的方向，斜坡（斜面）能省力。正确、安全地使用工具，能提高效率、保护自己。",
        "方法：分析工具的省力原理", "使用工具前先弄清它属于哪种简单机械、如何省力或方便：省力杠杆动力臂长于阻力臂，斜面越长越省力，定滑轮不省力但能改变力的方向。使用时注意安全规范，如用剪刀、锤子要按正确方法操作，用完归位。",
        "用羊角锤起钉子时，锤柄越长越省力，这是因为增大了动力臂，是省力杠杆的应用。",
        "定滑轮的主要作用是？", ["省力", "改变力的方向", "省距离", "既省力又改变方向"], 1,
        "定滑轮不省力，但能改变用力的方向。",
        "常见误区是认为所有工具、所有滑轮都省力。应分清：省力杠杆和动滑轮能省力，定滑轮只改变力的方向不省力，斜面越长越省力，要根据原理正确选用和使用工具。"),
}


STYLE = """
<style id="misc-depth-css">
.misc-depth .worked-example{margin:16px 0;padding:16px;border-left:4px solid var(--brand,#38bdf8);background:rgba(56,189,248,.08);border-radius:0 12px 12px 0}
.misc-depth .module-check{margin-top:18px;padding:16px;border-radius:14px;background:rgba(96,165,250,.08);border:1px solid rgba(96,165,250,.24)}
.misc-depth .module-check button{display:block;width:100%;margin:8px 0;text-align:left;border:1px solid var(--line,#233);border-radius:10px;background:#0b1628;color:var(--text,#e5e7eb);padding:11px 13px;cursor:pointer}
.misc-depth .module-check button.correct{border-color:var(--ok,#22c55e);background:rgba(34,197,94,.14)}
.misc-depth .module-check button.wrong{border-color:#f87171;background:rgba(248,113,113,.12)}
.misc-depth .misc-feedback{display:none;margin-top:10px;padding:12px;border-radius:10px;background:rgba(56,189,248,.1)}
.misc-depth .misc-pitfall{margin:14px 0 0;padding:12px;border-radius:10px;background:rgba(248,180,0,.08);border:1px solid rgba(248,180,0,.24)}
</style>
"""

CHECK_SCRIPT = """
<script id="misc-depth-js">
function miscDepthCheck(button, isCorrect, feedbackId, explanation) {
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
    feedback_id = "misc-depth-feedback"
    options = []
    for idx, opt in enumerate(cfg["options"]):
        correct = idx == cfg["correct"]
        handler = "miscDepthCheck(this,{c},'{f}',{e})".format(
            c="true" if correct else "false", f=feedback_id,
            e=json.dumps(cfg["feedback"], ensure_ascii=False))
        options.append(
            '<button type="button" data-correct="{flag}" onclick="{h}">{letter}. {opt}</button>'.format(
                flag="1" if correct else "0", h=html.escape(handler, quote=True),
                letter=chr(65 + idx), opt=html.escape(opt)))
    return f"""
<section class="slide-page" data-page-type="content" data-tsh="精讲">
  <section class="section misc-depth core-knowledge-module" id="lesson-focus"
    data-bloom-level="understand" data-scaffold="full" data-tts="lesson-focus">
    <div class="card">
      <span class="phase-tag">知识精讲</span>
      <h2>{html.escape(cfg['concept_title'])}</h2>
      <p>{html.escape(cfg['concept_body'])}</p>
    </div>
  </section>
</section>
<section class="slide-page" data-page-type="content" data-tsh="方法范例">
  <section class="section misc-depth core-knowledge-module" id="lesson-method"
    data-bloom-level="apply" data-scaffold="partial" data-tts="lesson-method">
    <div class="card">
      <span class="phase-tag">方法与范例</span>
      <h2>{html.escape(cfg['method_title'])}</h2>
      <p>{html.escape(cfg['method_body'])}</p>
      <div class="worked-example"><strong>范例：</strong>{html.escape(cfg['example'])}</div>
      <p id="lesson-pitfall" class="misc-pitfall"><strong>常见误区：</strong>{html.escape(cfg['pitfall'])}</p>
      <div class="module-check" data-conceptest="true">
        <h3>马上练：辨析要点</h3>
        <p>{html.escape(cfg['question'])}</p>
        {''.join(options)}
        <div class="misc-feedback" id="{feedback_id}" role="status"></div>
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
    block = build_block(cfg)
    source = source[:insert_at] + block + "\n" + source[insert_at:]
    if 'id="misc-depth-css"' not in source:
        source = source.replace("</head>", STYLE + "\n</head>", 1)
    if 'id="misc-depth-js"' not in source:
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
    return True, "2 core modules + metadata"


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
