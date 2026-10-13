#!/usr/bin/env python3
"""Add depth modules to remaining geo-h courses missing lesson-focus.

Batch 2 after upgrade-geo-h-depth.py. Same remediation pattern and geoh-depth-*
ids for CSS/JS/feedback consistency. Idempotent via id="lesson-focus". No mp4.
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
    "geo-h-monsoon-system": C(
        "季风系统：海陆热力差异与气压场季节转换",
        "季风是大范围盛行风向随季节显著改变的大气环流现象。东亚季风主要因海陆热力性质差异：冬季大陆冷高压、风由陆吹向海；夏季大陆热低压、风由海吹向陆，带来丰沛降水。南亚季风还与气压带风带季节移动、青藏高原热力作用等有关。季风影响气候类型、农业熟制、旱涝灾害与航运。理解季风要抓住“季节—气压中心—风向—干湿”这条因果链。",
        "方法：冬夏气压场对照推风向降水",
        "分析季风先画（或心中默画）冬、夏海陆气压形势，再据气压梯度与地转偏向力推近地面风向，最后联系干湿：冬季风来自内陆偏干，夏季风来自海洋偏湿。答题把成因机制与东亚/南亚差异、对农业与灾害的影响对应说明。",
        "我国东部夏季盛行东南季风，从太平洋带来水汽，形成雨热同期，利于水稻种植；冬季偏北风寒冷干燥。",
        "东亚冬季风的主要成因基础是？",
        ["赤道暖流", "海陆热力差异导致的气压场季节转换", "火山喷发", "月球引力"],
        1,
        "海陆热力差异使冬季大陆形成冷高压，风由陆吹向海。",
        "常见误区是只记“夏季风带来降水”而不讲气压场转换，或把东亚与南亚季风成因完全等同。应抓住海陆热力差异主线，并补充气压带风带移动等区域差异因素。",
    ),
    "geo-h-natural-zones": C(
        "自然带与地域分异规律",
        "自然带是气候、植被、土壤等要素在地表呈带状组合的地域单元，如热带雨林带、温带落叶阔叶林带、苔原带等。地域分异主要有：纬度地带性（热量主导，大致南北更替）、干湿度地带性（水分主导，大致东西更替）、垂直地带性（海拔引起水热变化）。非地带性因素（海陆分布、地形、洋流等）会使地带性规律发生偏离。认识自然带要“以水热定植被，以植被定带名”。",
        "方法：先判地带性类型，再找干扰因素",
        "读图或分析某地自然带：先看沿纬度、经度还是海拔方向更替，判断属哪类地带性；再检查山地、沿岸洋流、深居内陆等是否造成局部异常。答题把“理想地带性模式 + 实际偏离原因”写全。",
        "从赤道向两极，自然带大致按雨林—草原—荒漠—温带森林—苔原—冰原更替，体现纬度地带性（以热量变化为基础）。",
        "由沿海向内陆，自然带因水分递减而更替，主要属于？",
        ["纬度地带性", "干湿度地带性（经度地带性）", "垂直地带性", "只有非地带性"],
        1,
        "沿海向内陆水分条件变化主导的更替属干湿度地带性。",
        "常见误区是把所有自然带分布都只归因于纬度，忽视水分与垂直变化；或把山地垂直带与纬度带简单一一等同而不看基带与水热组合。",
    ),
    "geo-h-natural-zones-demo": C(
        "自然带判读演示：从景观到成因",
        "自然带教学常用景观、气候资料与分布模式图对照：见常绿阔叶林联想到亚热带湿润气候，见温带草原联想到半干旱内陆等。演示路径是“观察景观特征→推断水热状况→匹配气候类型→落到自然带名称与分布规律”。通过典型样带（如非洲沿20°E、亚欧大陆中纬从西向东）可分别演示纬度地带性与干湿度地带性。",
        "方法：景观—气候—自然带三步对齐",
        "拿到景观或资料先描述植被外貌（叶型、疏密），再推降水与气温特征，最后给出自然带与可能分布位置。比较两地时突出主导差异是热量还是水分。演示中明确指出哪条样带说明哪条规律。",
        "在亚欧大陆中纬度，自西向东由温带落叶阔叶林过渡到温带草原、温带荒漠，演示的是沿海向内陆的干湿度地带性。",
        "判读自然带最稳妥的思路是？",
        ["只看颜色好看与否", "由景观推水热，再匹配气候与自然带", "只记带名不问成因", "只看海拔数字"],
        1,
        "应从景观到水热再到气候与自然带对应，才能既知其然又知其所以然。",
        "常见误区是死记自然带名称与地图着色，不会用样带解释规律；演示课要把“看见什么—说明什么规律”说清楚，避免只看图不讲因果。",
    ),
    "geo-h-urban-structure": C(
        "城市空间结构：功能分区与成因",
        "城市内部空间结构指住宅区、商业区、工业区等功能区的分布格局及其组合。常见模式有同心圆、扇形、多核心等，用于概括而非刻板套用。地租水平、交通便捷度、历史继承与规划政策共同影响布局：中心商务区（CBD）多位于交通最便捷、地租最高处；工业区常趋向交通干线与城区外缘；住宅区有高级与普通之分并可能随交通改善外迁。理解结构要抓住“付租能力—交通—环境”综合权衡。",
        "方法：付租能力曲线 + 交通轴线",
        "分析功能区先比较不同活动的付租能力随距市中心距离的变化，再叠加放射状/环状交通线、河流风向等环境因素。答题说明为何该区在此、是否合理、如何优化（如卫星城、工业外迁、职住平衡）。",
        "许多大城市工业向郊区与交通走廊迁移，既降低市中心地租与污染压力，又依托高速路/铁路保持货运便利。",
        "中心商务区（CBD）通常布局在？",
        ["城市最边缘、地租最低处", "交通便捷、人流物流集中、地租较高的核心区位", "只在山区", "只能邻近农田"],
        1,
        "CBD 需要极高的交通可达性与集聚效应，多位于核心高地租区位。",
        "常见误区是把某一种城市模式当成所有城市的唯一真相，或只谈自然条件忽视地租、交通与规划；应用多因素综合解释功能分区。",
    ),
}


STYLE = """
<style id="geoh-depth-css">
.geoh-depth .worked-example{margin:16px 0;padding:16px;border-left:4px solid var(--brand,#38bdf8);background:rgba(56,189,248,.08);border-radius:0 12px 12px 0}
.geoh-depth .module-check{margin-top:18px;padding:16px;border-radius:14px;background:rgba(52,211,153,.08);border:1px solid rgba(52,211,153,.24)}
.geoh-depth .module-check button{display:block;width:100%;margin:8px 0;text-align:left;border:1px solid var(--line,#233);border-radius:10px;background:#0b1628;color:var(--text,#e5e7eb);padding:11px 13px;cursor:pointer}
.geoh-depth .module-check button.correct{border-color:var(--ok,#22c55e);background:rgba(34,197,94,.14)}
.geoh-depth .module-check button.wrong{border-color:#f87171;background:rgba(248,113,113,.12)}
.geoh-depth .geoh-feedback{display:none;margin-top:10px;padding:12px;border-radius:10px;background:rgba(56,189,248,.1)}
.geoh-depth .geoh-pitfall{margin:14px 0 0;padding:12px;border-radius:10px;background:rgba(248,180,0,.08);border:1px solid rgba(248,180,0,.24)}
</style>
"""

CHECK_SCRIPT = """
<script id="geoh-depth-js">
function geohDepthCheck(button, isCorrect, feedbackId, explanation) {
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
    feedback_id = "geoh-depth-feedback"
    options = []
    for idx, opt in enumerate(cfg["options"]):
        correct = idx == cfg["correct"]
        handler = "geohDepthCheck(this,{c},'{f}',{e})".format(
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
  <section class="section geoh-depth core-knowledge-module" id="lesson-focus"
    data-bloom-level="understand" data-scaffold="full" data-tts="lesson-focus">
    <div class="card">
      <span class="phase-tag">知识精讲</span>
      <h2>{html.escape(cfg['concept_title'])}</h2>
      <p>{html.escape(cfg['concept_body'])}</p>
    </div>
  </section>
</section>
<section class="slide-page" data-page-type="content" data-tsh="方法范例">
  <section class="section geoh-depth core-knowledge-module" id="lesson-method"
    data-bloom-level="apply" data-scaffold="partial" data-tts="lesson-method">
    <div class="card">
      <span class="phase-tag">方法与范例</span>
      <h2>{html.escape(cfg['method_title'])}</h2>
      <p>{html.escape(cfg['method_body'])}</p>
      <div class="worked-example"><strong>范例：</strong>{html.escape(cfg['example'])}</div>
      <p id="lesson-pitfall" class="geoh-pitfall"><strong>常见误区：</strong>{html.escape(cfg['pitfall'])}</p>
      <div class="module-check" data-conceptest="true">
        <h3>马上练：辨析要点</h3>
        <p>{html.escape(cfg['question'])}</p>
        {''.join(options)}
        <div class="geoh-feedback" id="{feedback_id}" role="status"></div>
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
    if 'id="geoh-depth-css"' not in source:
        source = source.replace("</head>", STYLE + "\n</head>", 1)
    if 'id="geoh-depth-js"' not in source:
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
    return True, "2 depth sections + metadata"


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
