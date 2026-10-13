#!/usr/bin/env python3
"""Add topic-specific depth modules to math-h shell courses (NOT math-high-*).

These high-school shell courses lack id="lesson-focus". Each course gets
知识精讲 + 方法范例 with a worked example, a 常见误区 note and TWO diagnostics.
No mp4. Idempotent via id="lesson-focus". Unique CSS/JS ids: mathh-depth-*.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_VERSION = "1.1.0"
UPDATED_AT = "2026-08-20"


def Q(question, options, correct, feedback):
    return dict(question=question, options=options, correct=correct, feedback=feedback)


def C(ct, cb, mt, mb, ex, pit, quizzes):
    return dict(
        concept_title=ct, concept_body=cb, method_title=mt, method_body=mb,
        example=ex, pitfall=pit, quizzes=quizzes,
    )


COURSES = {
    "math-h-analytic-geometry": C(
        "解析几何综合：用坐标刻画曲线",
        "解析几何用代数方法研究几何：在平面直角坐标系中，点对应坐标，曲线对应方程。直线、圆、椭圆、双曲线、抛物线是常见研究对象。基本问题包括：求轨迹方程、判断位置关系（相交、相切、相离）、求弦长与面积、利用几何性质简化计算。核心思想是“几何条件代数化，代数结果几何解释”。",
        "方法：设点列式 → 消参/联立 → 回译几何意义",
        "求轨迹：设动点 (x,y)，把几何条件写成方程并化简。研究直线与曲线：联立方程，用判别式判断交点个数；弦长可用韦达定理。能用定义（焦点、准线、圆心距）时优先用定义，少硬算。",
        "圆 x²+y²=25 与直线 x−y+1=0：联立得交点，或算圆心到直线距离 d=|0−0+1|/√2=1/√2＜5，故相交于两点。",
        "常见误区是只联立运算却不解释几何意义，或忽略定义域、渐近线、焦点等约束导致增根。",
        [
            Q("解析几何研究问题的基本途径是？",
              ["只用尺规作图", "用坐标把几何条件化为方程再求解", "只记忆图形名称", "不使用代数"],
              1, "坐标法把几何问题转化为代数方程来处理。"),
            Q("圆 x²+y²=r² 的圆心到直线 Ax+By+C=0 的距离小于 r，则直线与圆？",
              ["相离", "相切", "相交于两点", "重合"],
              2, "圆心距 d＜r 时直线与圆相交于两点。"),
        ],
    ),
    "math-h-functions-advanced": C(
        "函数综合性质：单调、奇偶与最值",
        "函数性质是高中函数综合的主干：定义域优先；单调性描述函数增减，常用导数或定义法；奇偶性由 f(−x) 与 ±f(x) 的关系判定，须先关于原点对称的定义域；最值可结合单调性、基本不等式、导数求极值。综合题常把性质与方程、不等式、图像变换串联。",
        "方法：先定义域，再奇偶/单调，最后求值或比大小",
        "判断奇偶：先看定义域是否关于原点对称，再算 f(−x)。判断单调：在区间内求导看符号，或用定义比较。求最值：能配方/基本不等式则用之，否则用导数找驻点并检验端点。",
        "f(x)=x+1/x（x>0）：由基本不等式 x+1/x≥2，当 x=1 时取等，最小值为 2；在 (0,1] 递减、[1,+∞) 递增。",
        "常见误区是未限制定义域就谈奇偶或单调，或求最值时不检验等号能否取到。",
        [
            Q("判断函数奇偶性时，首先必须检查？",
              ["值域是否为正", "定义域是否关于原点对称", "是否有最大值", "导数是否存在"],
              1, "定义域不关于原点对称则既不是奇函数也不是偶函数。"),
            Q("x>0 时，x+1/x 的最小值是？",
              ["0", "1", "2", "4"],
              2, "x+1/x≥2√(x·1/x)=2，x=1 时取等。"),
        ],
    ),
    "math-h-sets-logic": C(
        "集合的基本运算：交、并、补",
        "集合运算是高中数学的语言基础。并集 A∪B={x|x∈A 或 x∈B}；交集 A∩B={x|x∈A 且 x∈B}；补集 ∁ᵤA={x|x∈U 且 x∉A}。空集是任何集合的子集，与任何集合的交集为空、并集为该集合本身。Venn 图与数轴是理解运算关系的重要直观工具。",
        "方法：先定全集与元素归属，再用图或列举运算",
        "有限集合可列表或枚举；用不等式描述的集合先在数轴上标出，再读写区间。计数问题常用容斥：|A∪B|=|A|+|B|−|A∩B|。补集问题先明确全集 U。",
        "A={1,2,3}，B={2,3,4}，则 A∪B={1,2,3,4}，A∩B={2,3}。若 U={1,2,3,4,5}，则 ∁ᵤA={4,5}。",
        "常见误区是把“或”与“且”弄反，或求补集时忘记全集，把不属于 A 的所有对象都算进去。",
        [
            Q("A∩B 表示的是？",
              ["属于 A 或属于 B 的元素", "既属于 A 又属于 B 的元素", "不属于 A 的元素", "A 与 B 的元素个数之差"],
              1, "交集是同时属于两个集合的元素构成的集合。"),
            Q("某班 35 人，数学社 20 人，文学社 15 人，两社都参加 5 人，则至少参加一个社的人数是？",
              ["30", "35", "40", "25"],
              0, "由容斥：20+15−5=30。"),
        ],
    ),
    "math-h-trigonometric-functions": C(
        "三角函数综合：图像、性质与变换",
        "正弦、余弦、正切函数把角与比值联系起来，并能用单位圆与图像研究性质。y=Asin(ωx+φ)+B（及余弦型）通过 A、ω、φ、B 控制振幅、周期、相位与上下平移。周期 T=2π/|ω|；对称轴、对称中心、单调区间是综合题常考点。同角关系、诱导公式用于化简求值。",
        "方法：化标准型 → 读 A、ω、φ、B → 写性质",
        "先把解析式化为 Asin(ωx+φ)+B 或 Acos(ωx+φ)+B，再求周期、最值、单调区间。求值优先用诱导公式化到锐角，或用单位圆判断象限符号。图像变换按“左右相位 → 横向伸缩 → 纵向伸缩/平移”的顺序分析更稳。",
        "y=2sin(2x−π/3)：A=2，ω=2，φ=−π/3，T=π；最大值为 2，最小值为 −2。",
        "常见误区是周期写成 2π/ω 却漏了绝对值，或相位左右平移方向搞反。",
        [
            Q("函数 y=Asin(ωx+φ)（A≠0，ω≠0）的周期是？",
              ["2π/ω", "2π/|ω|", "π/|ω|", "|ω|/2π"],
              1, "周期 T=2π/|ω|。"),
            Q("y=2sin(2x−π/3) 的最大值为？",
              ["1", "2", "π", "2/3"],
              1, "振幅 |A|=2，故最大值为 2。"),
        ],
    ),
    "math-h-trigonometry-solution": C(
        "解三角形：正弦定理与余弦定理",
        "解三角形指由边角的已知条件求其余边角及面积等。正弦定理：a/sinA=b/sinB=c/sinC=2R。余弦定理：a²=b²+c²−2bc cosA（及其轮换）。面积公式有 (1/2)ab sinC 等。已知条件对应不同思路：两角一边优先正弦定理；两边及夹角或三边优先余弦定理。注意 SSA 可能出现两解、一解或无解。",
        "方法：先分类已知，再选定理，最后检验合理性",
        "ASA/AAS：先求第三角，再用正弦定理求边。SAS：余弦定理求第三边，再求角。SSS：余弦定理求角。SSA：用正弦定理求角时检查是否有两解（钝角/锐角），并验证三角形内角和。",
        "在 △ABC 中，a=2，b=2√3，A=30°：由正弦定理 sinB=b sinA/a=√3/2，得 B=60° 或 120°；若 B=120°，则 A+B=150°，可求 C=30°，两边情形都需结合题设取舍。",
        "常见误区是 SSA 情况直接取锐角忽略两解，或余弦定理符号记错（把 −2bc cosA 写成 +）。",
        [
            Q("已知三角形两边及其夹角，优先选用？",
              ["正弦定理", "余弦定理", "勾股定理（任意三角）", "诱导公式"],
              1, "两边夹角（SAS）用余弦定理求第三边最直接。"),
            Q("余弦定理 a²=b²+c²−2bc cosA 中，当 A=90° 时退化为？",
              ["正弦定理", "勾股定理 a²=b²+c²", "面积公式", "诱导公式"],
              1, "cos90°=0，故 a²=b²+c²。"),
        ],
    ),
}


STYLE = """
<style id="mathh-depth-css">
.mathh-depth .worked-example{margin:16px 0;padding:16px;border-left:4px solid var(--brand,#38bdf8);background:rgba(56,189,248,.08);border-radius:0 12px 12px 0}
.mathh-depth .module-check{margin-top:18px;padding:16px;border-radius:14px;background:rgba(251,146,60,.08);border:1px solid rgba(251,146,60,.28)}
.mathh-depth .module-check button{display:block;width:100%;margin:8px 0;text-align:left;border:1px solid var(--line,#233);border-radius:10px;background:#0b1628;color:var(--text,#e5e7eb);padding:11px 13px;cursor:pointer}
.mathh-depth .module-check button.correct{border-color:var(--ok,#22c55e);background:rgba(34,197,94,.14)}
.mathh-depth .module-check button.wrong{border-color:#f87171;background:rgba(248,113,113,.12)}
.mathh-depth .mathh-feedback{display:none;margin-top:10px;padding:12px;border-radius:10px;background:rgba(56,189,248,.1)}
.mathh-depth .mathh-pitfall{margin:14px 0 0;padding:12px;border-radius:10px;background:rgba(248,180,0,.08);border:1px solid rgba(248,180,0,.24)}
</style>
"""

CHECK_SCRIPT = """
<script id="mathh-depth-js">
function mathhDepthCheck(button, isCorrect, feedbackId, explanation) {
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


def build_check(quiz: dict, index: int, label: str) -> str:
    feedback_id = f"mathh-depth-feedback-{index}"
    options = []
    for idx, opt in enumerate(quiz["options"]):
        correct = idx == quiz["correct"]
        handler = "mathhDepthCheck(this,{c},'{f}',{e})".format(
            c="true" if correct else "false",
            f=feedback_id,
            e=json.dumps(quiz["feedback"], ensure_ascii=False),
        )
        options.append(
            '<button type="button" data-correct="{flag}" onclick="{h}">{letter}. {opt}</button>'.format(
                flag="1" if correct else "0",
                h=html.escape(handler, quote=True),
                letter=chr(65 + idx),
                opt=html.escape(opt),
            )
        )
    return f"""      <div class="module-check" data-conceptest="true">
        <h3>{html.escape(label)}</h3>
        <p>{html.escape(quiz['question'])}</p>
        {''.join(options)}
        <div class="mathh-feedback" id="{feedback_id}" role="status"></div>
      </div>
"""


def build_block(cfg: dict) -> str:
    labels = ["马上练 1：概念辨析", "马上练 2：计算应用"]
    checks = "".join(
        build_check(quiz, i + 1, labels[i] if i < len(labels) else f"马上练 {i + 1}")
        for i, quiz in enumerate(cfg["quizzes"])
    )
    return f"""
<section class="slide-page" data-page-type="content" data-tsh="精讲">
  <section class="section mathh-depth core-knowledge-module text-module" id="lesson-focus"
    data-bloom-level="understand" data-scaffold="full" data-tts="lesson-focus">
    <div class="card">
      <span class="phase-tag">知识精讲</span>
      <h2>{html.escape(cfg['concept_title'])}</h2>
      <p>{html.escape(cfg['concept_body'])}</p>
    </div>
  </section>
</section>
<section class="slide-page" data-page-type="content" data-tsh="方法范例">
  <section class="section mathh-depth core-knowledge-module text-module" id="lesson-method"
    data-bloom-level="apply" data-scaffold="partial" data-tts="lesson-method">
    <div class="card">
      <span class="phase-tag">方法与范例</span>
      <h2>{html.escape(cfg['method_title'])}</h2>
      <p>{html.escape(cfg['method_body'])}</p>
      <div class="worked-example"><strong>范例：</strong>{html.escape(cfg['example'])}</div>
      <p id="lesson-pitfall" class="mathh-pitfall"><strong>常见误区：</strong>{html.escape(cfg['pitfall'])}</p>
{checks}    </div>
  </section>
</section>
"""


def find_insert_at(source: str) -> int:
    dpos = -1
    for anchor in ('id="deep-understanding"', 'id="transfer-task"', 'id="posttest"', 'id="summary"'):
        dpos = source.find(anchor)
        if dpos >= 0:
            break
    if dpos < 0:
        return -1
    marker = source.rfind('<section class="slide-page"', 0, dpos)
    if marker >= 0:
        return marker
    tag_start = source.rfind("<", 0, dpos)
    if tag_start >= 0:
        return tag_start
    return source.rfind("<section", 0, dpos)


def upgrade(course_id: str, cfg: dict) -> tuple[bool, str]:
    path = ROOT / "community" / course_id / "index.html"
    if not path.exists():
        return False, "missing index.html"
    source = path.read_text(encoding="utf-8")
    if 'id="lesson-focus"' in source:
        return False, "already upgraded"
    insert_at = find_insert_at(source)
    if insert_at < 0:
        return False, "insert anchor not found"
    source = source[:insert_at] + build_block(cfg) + "\n" + source[insert_at:]
    if 'id="mathh-depth-css"' not in source:
        source = source.replace("</head>", STYLE + "\n</head>", 1)
    if 'id="mathh-depth-js"' not in source:
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
    return True, f"2 depth modules + {len(cfg['quizzes'])} checks"


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
