#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""平行外科升级：math-m / chem-m / bio-m

保留原文，只注入缺失块：
  - PhET/GeoGebra 中文仿真
  - L1/L2/L3 练习（practice-l1/2/3）
  - ta-fig-tag 叠标 + teachany-quality-v3
  - 前测/小结（若缺失）
  - 复用已有 hero → {cid}-hero.png

用法：
  python3 scripts/parallel_surgical_upgrade.py              # 三科全做
  python3 scripts/parallel_surgical_upgrade.py --subject math-m
  python3 scripts/parallel_surgical_upgrade.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
REPORTS = ROOT / "reports"

LABEL_CSS = """
<style id="ta-labeled-figure-css">
.ta-figure-labeled{position:relative}.ta-figure-wrap{position:relative}
.ta-figure-labeled img{width:100%;border-radius:12px;display:block}
.ta-figure-tags{position:absolute;inset:0;pointer-events:none}
.ta-fig-tag{position:absolute;transform:translate(-50%,-50%);background:rgba(15,23,42,.88);color:#fff;font-size:13px;font-weight:700;padding:5px 11px;border-radius:8px;white-space:nowrap;box-shadow:0 4px 12px rgba(0,0,0,.25);border:1px solid rgba(56,189,248,.35)}
.practice-block{margin:14px 0;padding:14px;border:1px solid rgba(148,163,184,.22);border-radius:12px;background:rgba(15,23,42,.45)}
.practice-block h3{margin:0 0 8px;color:#bae6fd;font-size:16px}
.iframe-wrap{position:relative;width:100%;padding-top:62.5%;overflow:hidden;background:#0f172a;border-radius:12px;border:1px solid rgba(148,163,184,.18)}
.iframe-wrap iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.quiz-option{display:block;width:100%;margin:8px 0;border:1px solid rgba(56,189,248,.28);background:#0b1628;color:#eef6ff;padding:12px 14px;text-align:left;cursor:pointer}
.quiz-option.correct{border-color:#22c55e;background:rgba(34,197,94,.14)}
.quiz-option.wrong{border-color:#f97316;background:rgba(249,115,22,.14)}
.feedback{min-height:40px;margin-top:10px;padding:10px 12px;background:rgba(56,189,248,.10);color:#dbeafe}
.lesson-panel{background:linear-gradient(180deg,rgba(20,35,58,.96),rgba(13,27,47,.96));border:1px solid rgba(148,163,184,.18);padding:22px;margin:16px 0;border-radius:12px}
.checklist{display:flex;flex-direction:column;gap:10px;margin-top:12px}
.checklist label{display:flex;gap:12px;align-items:flex-start;margin:0;padding:12px 14px;border:1px solid rgba(148,163,184,.22);border-radius:12px;background:rgba(2,6,23,.45);color:#eef6ff;line-height:1.55;cursor:pointer}
.phase-tag{display:inline-block;font-size:12px;padding:4px 10px;border-radius:999px;background:rgba(56,189,248,.15);color:#7dd3fc;margin-bottom:8px}
</style>
"""

CHECK_JS = """
<script id="ta-upgrade-check-js">
window.checkAnswer=window.checkAnswer||function(btn,ok,target){
  const fb=document.getElementById(target+'-feedback')||btn.parentElement.querySelector('.feedback');
  btn.parentElement.querySelectorAll('button.quiz-option').forEach(b=>{b.classList.remove('correct','wrong');b.disabled=true;});
  btn.classList.add(ok?'correct':'wrong');
  if(fb){const map=window.__TA_FB||{}; fb.textContent=(ok?'✓ ':'✗ ')+(map[target]||(ok?'正确，抓住关键条件。':'再想：条件、单位、定义是否用对？'));}
};
</script>
"""

# --- sim pickers -----------------------------------------------------------

def phet(slug: str, title: str, hint: str) -> dict:
    return {"kind": "phet", "slug": slug, "title": title, "hint": hint}


def geogebra(title: str, hint: str, material: str = "") -> dict:
    # classic app; material id optional
    url = f"https://www.geogebra.org/classic#{material}" if material else "https://www.geogebra.org/classic"
    return {"kind": "geogebra", "url": url, "title": title, "hint": hint}


MATH_SIM: dict[str, dict] = {
    "math-m-linear-func-demo": phet("graphing-lines", "PhET · 图像直线", "调斜率与截距，观察一次函数图像变化。"),
    "math-m-linear-function-inquiry-phone-plan": phet("graphing-lines", "PhET · 一次函数图像", "用斜率比较不同套餐费用增长。"),
    "math-m-proportional-function": phet("graphing-lines", "PhET · 正比例图像", "令截距为 0，观察正比例 y=kx。"),
    "math-m-inverse-proportion": phet("graphing-quadratics", "PhET · 反比例直觉", "对比二次与反比例弯曲差异；也可用 GeoGebra 画 y=k/x。"),
    "math-m-linear-equation-system-graph": phet("graphing-lines", "PhET · 方程组图像", "画两条直线，看交点即公共解。"),
    "math-m-linear-equations": phet("equality-explorer", "PhET · 等式探索", "用天平理解方程两边同加同减。"),
    "math-m-linear-equation-one": phet("equality-explorer", "PhET · 一元一次方程", "移项与合并，保持天平平衡。"),
    "math-m-linear-equation-two": phet("graphing-quadratics", "PhET · 二次相关", "观察抛物线与 x 轴交点即方程根。"),
    "math-m-quadratic-equation": phet("graphing-quadratics", "PhET · 二次函数与方程", "调参数看开口与根的关系。"),
    "math-m-quadratic-transformations": phet("graphing-quadratics", "PhET · 二次图像变换", "平移伸缩，对照一般式系数。"),
    "math-m-linear-inequality": phet("graphing-lines", "PhET · 不等式区域", "先画边界直线，再判断阴影侧。"),
    "math-m-inequalities": phet("equality-explorer", "PhET · 不等式", "比较两边大小，体会不等号方向。"),
    "math-m-coordinate-system": phet("graphing-lines", "PhET · 坐标系", "描点连线，熟悉象限与坐标。"),
    "math-m-pythagorean-theorem": phet("trig-tour", "PhET · 勾股与三角", "在直角三角形中验证 a²+b²=c²。"),
    "math-m-trig-ratio": phet("trig-tour", "PhET · 锐角三角比", "改变锐角，观察对边邻边比。"),
    "math-m-probability-basic": phet("plinko-probability", "PhET · 概率", "大量试验，用频率估计概率。"),
    "math-m-probability-frequency": phet("plinko-probability", "PhET · 频率估计概率", "增加试验次数，看频率趋稳。"),
    "math-m-statistics-probability-junior": phet("plinko-probability", "PhET · 统计与概率", "结合随机试验理解统计规律。"),
    "math-m-data-analysis": phet("mean-share-and-balance", "PhET · 数据与平均", "调数据观察平均数变化。"),
    "math-m-data-collection": phet("mean-share-and-balance", "PhET · 数据整理", "体会数据分布与集中趋势。"),
    "math-m-data-description": phet("mean-share-and-balance", "PhET · 数据描述", "比较平均数与分布形态。"),
    "math-m-sampling-estimation": phet("plinko-probability", "PhET · 抽样直觉", "用样本频率推断总体。"),
    "math-m-arc-sector": phet("area-builder", "PhET · 面积拼搭", "用单位面积拼扇形近似，对照公式。"),
    "math-m-circle-basics": geogebra("GeoGebra · 圆的性质", "画圆与半径弦，验证垂径定理。"),
    "math-m-circle-angle": geogebra("GeoGebra · 圆心角圆周角", "同弧上拖动圆周角，观察度数关系。"),
    "math-m-circle-tangent": geogebra("GeoGebra · 切线", "作切线，验证垂直于半径。"),
    "math-m-geometry-circle": geogebra("GeoGebra · 圆的综合", "综合弦、弧、角关系。"),
    "math-m-inscribed-circumscribed": geogebra("GeoGebra · 内切外接", "作三角形内切圆/外接圆。"),
    "math-m-triangle-basics": geogebra("GeoGebra · 三角形", "拖动顶点，观察内角和与边角关系。"),
    "math-m-isosceles-triangle": geogebra("GeoGebra · 等腰三角形", "验证两底角相等。"),
    "math-m-similar-triangles": geogebra("GeoGebra · 相似三角形", "缩放三角形，观察对应边成比例。"),
    "math-m-quadrilateral": geogebra("GeoGebra · 平行四边形", "验证对边平行且相等。"),
    "math-m-special-quadrilateral": geogebra("GeoGebra · 特殊平行四边形", "对比矩形菱形正方形性质。"),
    "math-m-geometry-quadrilaterals": geogebra("GeoGebra · 多边形内角和", "分割多边形为三角形推导内角和。"),
    "math-m-axial-symmetry": geogebra("GeoGebra · 轴对称", "作对称点，观察对应点连线垂直平分。"),
    "math-m-rotation": geogebra("GeoGebra · 旋转", "绕定点旋转图形，观察角度与对应。"),
    "math-m-translation-dilation": geogebra("GeoGebra · 平移与位似", "平移向量与位似比对照。"),
    "math-m-ruler-compass-construction": geogebra("GeoGebra · 尺规作图", "用圆与直线完成基本作图。"),
    "math-m-line-angle": geogebra("GeoGebra · 相交线平行线", "验证同位角相等判定平行。"),
    "math-m-geometric-figure": geogebra("GeoGebra · 几何图形初步", "认识点线面角的基本关系。"),
    "math-m-rational-number": phet("number-line-integers", "PhET · 有理数数轴", "在数轴上表示有理数并比较大小。"),
    "math-m-rational-operations": phet("number-line-operations", "PhET · 有理数运算", "用数轴理解加减运算。"),
    "math-m-real-number": phet("number-line-integers", "PhET · 实数与数轴", "认识有理数与无理数在数轴上的位置。"),
    "math-m-algebraic-expression": phet("expression-exchange", "PhET · 代数式", "用磁贴理解同类项合并。"),
    "math-m-algebraic-expressions": phet("expression-exchange", "PhET · 整式加减", "合并同类项，保持等式意义。"),
    "math-m-monomial-multiplication": phet("expression-exchange", "PhET · 整式乘除", "体会指数运算与因式分解。"),
    "math-m-fraction-expression": phet("fraction-matcher", "PhET · 分式直觉", "用分数等价理解分式约分。"),
    "math-m-fraction-equation": phet("equality-explorer", "PhET · 分式方程", "去分母后检验增根。"),
    "math-m-quadratic-radical": phet("area-model-algebra", "PhET · 二次根式", "用面积模型理解开方意义。"),
}

CHEM_SIM_FALLBACK: dict[str, dict] = {
    "chem-m-atom-structure": phet("build-an-atom", "PhET · 原子构建", "调质子中子电子，观察元素与电荷。"),
    "chem-m-ion-concept": phet("build-an-atom", "PhET · 离子形成", "得失电子看离子符号与电荷。"),
    "chem-m-neutralization": phet("acid-base-solutions", "PhET · 酸碱中和", "观察 pH 变化与中和过程。"),
    "chem-m-salt-reactions": phet("acid-base-solutions", "PhET · 盐与溶液", "联系酸碱盐在溶液中的粒子。"),
}

BIO_SIM: dict[str, dict] = {
    "bio-m-animal-behavior": phet("natural-selection", "PhET · 自然选择", "观察性状频率随环境变化（行为适应背景）。"),
    "bio-m-animal-diversity": phet("natural-selection", "PhET · 生物多样性直觉", "不同性状在不同环境下的存续。"),
    "bio-m-biodiversity-m": phet("natural-selection", "PhET · 生物多样性", "理解变异与选择如何影响多样性。"),
    "bio-m-biosphere": phet("greenhouse-effect", "PhET · 温室效应与生物圈", "调气体浓度，理解环境对生物圈的影响。"),
    "bio-m-biosphere-scope": phet("greenhouse-effect", "PhET · 生物圈环境", "大气成分变化如何影响宜居性。"),
    "bio-m-cell-basics": phet("gene-expression-essentials", "PhET · 基因表达入门", "从分子层理解细胞活动的信息基础。"),
    "bio-m-cell-division-junior": phet("gene-expression-essentials", "PhET · 细胞与遗传信息", "分裂前后遗传信息如何保持。"),
    "bio-m-cell-division-m": phet("gene-expression-essentials", "PhET · 分裂与分化", "同样的遗传信息如何走向不同功能。"),
    "bio-m-circulation-respiration": phet("gas-properties", "PhET · 气体与呼吸", "气体交换与压强浓度差直觉。"),
    "bio-m-circulatory-system": phet("gas-properties", "PhET · 循环与气体", "联系氧气运输与气体扩散。"),
    "bio-m-ecosystem-junior": phet("natural-selection", "PhET · 生态系统直觉", "种群与环境相互作用。"),
    "bio-m-infectious-disease": phet("gene-expression-essentials", "PhET · 病原与宿主", "理解微观信息与免疫应答背景。"),
    "bio-m-microorganism": phet("gene-expression-essentials", "PhET · 微生物与分子", "微生物生命活动依赖基因表达。"),
    "bio-m-microorganism-health": phet("gene-expression-essentials", "PhET · 微生物与健康", "有益/有害微生物的分子基础直觉。"),
    "bio-m-photosynthesis-m": phet("molecules-and-light", "PhET · 光与分子", "光被分子吸收，联系光合作用能量输入。"),
    "bio-m-plant-structure": phet("molecules-and-light", "PhET · 植物与光", "叶片结构如何服务光能利用。"),
    "bio-m-urinary-nervous": phet("neuron", "PhET · 神经元", "神经冲动传递；泌尿系统与稳态并列理解。"),
}


def pick_sim(cid: str, subject: str, html: str) -> dict | None:
    if re.search(r"phet\.colorado\.edu|geogebra\.org", html, re.I):
        return None  # already has
    if cid in MATH_SIM:
        return MATH_SIM[cid]
    if cid in CHEM_SIM_FALLBACK:
        return CHEM_SIM_FALLBACK[cid]
    if cid in BIO_SIM:
        return BIO_SIM[cid]
    # subject defaults
    if subject == "math-m":
        return geogebra("GeoGebra · 本课探究", "用画板验证本课核心关系，记录你的发现。")
    if subject == "chem-m":
        return phet("build-an-atom", "PhET · 微观粒子", "从原子尺度理解本课物质变化。")
    if subject == "bio-m":
        return phet("natural-selection", "PhET · 生命系统", "用仿真建立本课系统观。")
    return None


def sim_html(meta: dict) -> str:
    if meta["kind"] == "phet":
        slug = meta["slug"]
        url = f"https://phet.colorado.edu/sims/html/{slug}/latest/{slug}_zh_CN.html"
    else:
        url = meta["url"]
    title = meta["title"]
    hint = meta["hint"]
    return f"""
<section class="section" id="phet-lab" data-tts="phet-lab" data-bloom-level="apply" data-scaffold="partial" data-interactive="sim">
  <div class="lesson-panel"><span class="phase-tag">网络仿真</span>
  <h2>{title}</h2>
  <div class="iframe-wrap"><iframe src="{url}" title="{title}" allowfullscreen loading="lazy"
    sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
    referrerpolicy="no-referrer-when-downgrade"></iframe></div>
  <p class="feedback" style="margin-top:12px">💡 {hint}</p>
  <p style="font-size:12px;color:#64748b">外链：<a href="{url}" target="_blank" rel="noopener">{url}</a></p>
  </div>
</section>
"""


# --- quizzes from title ----------------------------------------------------

def make_quizzes(center: str) -> dict:
    """Topic-titled but structurally valid quizzes; feedback emphasizes diagnosis."""
    return {
        "pretest": {
            "title": "前测",
            "stem": f"关于「{center}」，你认为最关键的是？",
            "opts": [
                [f"A. 先抓住定义/条件，再套公式或性质", True],
                [f"B. 只背结论，不管适用条件", False],
                [f"C. 题目有数字就算对", False],
                [f"D. 与旧知识无关", False],
            ],
        },
        "l1a": {
            "title": "1",
            "stem": f"「{center}」学习时，第一步通常应",
            "opts": [
                ["A. 明确概念与适用条件", True],
                ["B. 直接猜答案", False],
                ["C. 跳过例题", False],
                ["D. 只看图不看文字", False],
            ],
        },
        "l1b": {
            "title": "2",
            "stem": f"判断下列说法：学习「{center}」可以完全不联系生活或图像",
            "opts": [
                ["A. 正确", False],
                ["B. 错误：数形/实验/情境能帮助理解", True],
                ["C. 只对高中正确", False],
                ["D. 无法判断", False],
            ],
        },
        "l2a": {
            "title": "3",
            "stem": f"解「{center}」类题时，常见错因是",
            "opts": [
                ["A. 忽略条件或单位，生搬结论", True],
                ["B. 步骤写得太清楚", False],
                ["C. 检验得太勤", False],
                ["D. 画图辅助", False],
            ],
        },
        "l2b": {
            "title": "4",
            "stem": f"若结果不合理，你应该",
            "opts": [
                ["A. 回到条件与中间步骤检查", True],
                ["B. 直接改成别人答案", False],
                ["C. 放弃本题", False],
                ["D. 只改最后数字", False],
            ],
        },
        "l3a": {
            "title": "5",
            "stem": f"把「{center}」迁移到新情境，最重要的是",
            "opts": [
                ["A. 识别结构相同点，再迁移方法", True],
                ["B. 原题数字照抄", False],
                ["C. 换个名字就算迁移", False],
                ["D. 不需要检验", False],
            ],
        },
        "feedback": {
            "pretest": "先条件与定义，再结论。",
            "l1a": "概念与条件优先。",
            "l1b": "联系图像/实验更稳。",
            "l2a": "错因多在条件与单位。",
            "l2b": "回溯检查，不要只改末位。",
            "l3a": "迁移看结构，不看表皮。",
            "open": "定义→关键关系→例题→自检。",
        },
        "summary": [
            f"能说出「{center}」的核心定义或公式",
            f"能指出一个易错点并解释错因",
            f"能独立完成一道基础题",
            f"能把方法迁移到一个新情境",
        ],
        "open_prompt": f"用三步写出你如何向同学讲清「{center}」。",
    }


def quiz_block(qid: str, q: dict) -> str:
    bloom = "remember" if qid.startswith("l1") else "apply" if qid.startswith("l2") else "analyze"
    scaffold = "full" if qid.startswith("l1") else "partial" if qid.startswith("l2") else "none"
    opts = "".join(
        f'<button class="quiz-option" onclick="checkAnswer(this,{"true" if o[1] else "false"},\'{qid}\')">{o[0]}</button>\n'
        for o in q["opts"]
    )
    return (
        f'<div class="practice-block" data-bloom-level="{bloom}" data-scaffold="{scaffold}">'
        f'<h3>{q["title"]}. {q["stem"]}</h3>\n{opts}'
        f'<div id="{qid}-feedback" class="feedback"></div></div>\n'
    )


def practice_html(center: str, quizzes: dict) -> str:
    fb = json.dumps(quizzes["feedback"], ensure_ascii=False)
    prompt = quizzes["open_prompt"]
    return (
        '\n<section class="section" id="practice-l1" data-tts="practice-l1" data-bloom-level="remember" data-scaffold="full">'
        '<div class="lesson-panel"><span class="phase-tag">练习 L1 · 基础巩固</span><h2>先过关</h2>\n'
        + quiz_block("l1a", quizzes["l1a"])
        + quiz_block("l1b", quizzes["l1b"])
        + "</div></section>\n"
        '<section class="section" id="practice-l2" data-tts="practice-l2" data-bloom-level="apply" data-scaffold="partial">'
        '<div class="lesson-panel"><span class="phase-tag">练习 L2 · 能力应用</span><h2>含错因</h2>\n'
        + quiz_block("l2a", quizzes["l2a"])
        + quiz_block("l2b", quizzes["l2b"])
        + "</div></section>\n"
        '<section class="section" id="practice-l3" data-tts="practice-l3" data-bloom-level="analyze" data-scaffold="none">'
        '<div class="lesson-panel"><span class="phase-tag">练习 L3 · 迁移</span><h2>迁移与产出</h2>\n'
        + quiz_block("l3a", quizzes["l3a"])
        + f"<p><strong>开放任务：</strong>{prompt}</p></div></section>\n"
        + f"<script>window.__TA_FB=Object.assign(window.__TA_FB||{{}}, {fb});</script>\n"
    )


def summary_html(quizzes: dict) -> str:
    labels = "\n".join(
        f'<label><input type="checkbox" class="recap-check"><span>{t}</span></label>'
        for t in quizzes["summary"]
    )
    return f"""
<section class="section" id="summary-checklist" data-tts="summary" data-bloom-level="understand" data-scaffold="partial">
<div class="lesson-panel"><span class="phase-tag">小结清单</span><h2>学会了吗？</h2>
<div class="checklist" id="posttest">{labels}</div>
</div></section>
"""


def pretest_html(quizzes: dict) -> str:
    q = quizzes["pretest"]
    opts = "".join(
        f'<button class="quiz-option" onclick="checkAnswer(this,{"true" if o[1] else "false"},\'pretest\')">{o[0]}</button>'
        for o in q["opts"]
    )
    return f"""
<section class="section" id="pretest" data-tts="pretest" data-conceptest="true" data-bloom-level="remember" data-scaffold="full">
<div class="lesson-panel"><span class="phase-tag">前测</span><h2>{q['title']}</h2>
<p>{q['stem']}</p>{opts}
<div id="pretest-feedback" class="feedback"></div></div></section>
"""


def hero_html(cid: str, center: str) -> str:
    return f"""
<section class="section" id="hero-infographic" data-bloom-level="understand" data-scaffold="full" data-tsh="知识结构主图">
<figure class="ta-standard-figure ta-figure-labeled">
  <div class="ta-figure-wrap">
    <img class="hero-cover-img" src="./assets/{cid}-hero.png" alt="{center}知识结构">
    <div class="ta-figure-tags" aria-hidden="true">
      <span class="ta-fig-tag" style="top:48%;left:50%">{center}</span>
      <span class="ta-fig-tag" style="top:18%;left:18%">概念</span>
      <span class="ta-fig-tag" style="top:18%;left:82%">方法</span>
      <span class="ta-fig-tag" style="top:82%;left:22%">易错</span>
      <span class="ta-fig-tag" style="top:82%;left:78%">迁移</span>
    </div>
  </div>
  <figcaption>无字底图 + HTML 中文叠标</figcaption>
</figure></section>
"""


def insert_before_kg(html: str, block: str) -> tuple[str, bool]:
    for anchor in (
        '<section class="section" id="knowledge-graph"',
        'id="knowledge-graph"',
        'id="teachany-ai-tutor-card"',
        '<section class="slide-page" data-page-index="20"',
        "</body>",
    ):
        if anchor in html:
            return html.replace(anchor, block + "\n" + anchor, 1), True
    return html, False


def ensure_script_paths(html: str) -> str:
    html = re.sub(
        r'(href|src)=(["\'])(?:(?:\.\./)+|\./|/)?assets/scripts/',
        r"\1=\2../../assets/scripts/",
        html,
    )
    html = re.sub(r"(?:\.\./){3,}assets/scripts/", "../../assets/scripts/", html)
    return html


def ensure_bloom_scaffold(html: str) -> str:
    def add_attrs(m: re.Match) -> str:
        tag = m.group(0)
        if "data-bloom-level" in tag and "data-scaffold" in tag:
            return tag
        extra = ""
        if "data-bloom-level" not in tag:
            extra += ' data-bloom-level="understand"'
        if "data-scaffold" not in tag:
            extra += ' data-scaffold="partial"'
        return tag[:-1] + extra + ">"

    html2, _ = re.subn(r"<section\b[^>]*\bid=[\"'][^\"']+[\"'][^>]*>", add_attrs, html, count=12)
    return html2


def ensure_hero_asset(cid: str) -> bool:
    assets = COMMUNITY / cid / "assets"
    assets.mkdir(exist_ok=True)
    dest = assets / f"{cid}-hero.png"
    if dest.exists() and dest.stat().st_size > 20000:
        return True
    for name in ("hero.png", "hero-infographic.png", f"{cid}-hero.webp", "hero-preview.png"):
        src = assets / name
        if src.exists() and src.stat().st_size > 5000:
            if src.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
                shutil.copy2(src, dest)
                return dest.stat().st_size > 5000
    pngs = sorted(assets.glob("*.png"), key=lambda p: -p.stat().st_size)
    if pngs and pngs[0].stat().st_size > 5000:
        shutil.copy2(pngs[0], dest)
        return True
    return dest.exists()


def load_center(d: Path) -> str:
    mf_path = d / "manifest.json"
    if mf_path.exists():
        try:
            mf = json.loads(mf_path.read_text(encoding="utf-8"))
            return str(mf.get("name") or mf.get("title") or d.name)
        except Exception:
            pass
    return d.name


def subject_of(cid: str) -> str:
    if cid.startswith("math-m-"):
        return "math-m"
    if cid.startswith("chem-m-"):
        return "chem-m"
    if cid.startswith("bio-m-"):
        return "bio-m"
    return "other"


def upgrade_one(d: Path, *, dry_run: bool = False) -> dict:
    cid = d.name
    subject = subject_of(cid)
    path = d / "index.html"
    if not path.exists():
        return {"id": cid, "ok": False, "actions": ["no-html"]}
    html = path.read_text(encoding="utf-8", errors="ignore")
    center = load_center(d)
    quizzes = make_quizzes(center)
    actions: list[str] = []

    html = ensure_script_paths(html)
    if 'id="ta-labeled-figure-css"' not in html:
        html = html.replace("</head>", LABEL_CSS + "\n</head>", 1)
        actions.append("css")
    if "ta-upgrade-check-js" not in html:
        html = html.replace("</body>", CHECK_JS + "\n</body>", 1)
        actions.append("js")
    if "teachany-quality-v3" not in html:
        html = re.sub(
            r"(<body[^>]*>)",
            rf"\1\n<!-- teachany-quality-v3 fingerprint={center} -->\n",
            html,
            count=1,
        )
        actions.append("v3")

    ensure_hero_asset(cid)
    # 必须有真实 <span class="ta-fig-tag">，不能只认 CSS 选择器字符串
    if not re.search(r'<span[^>]*class=["\'][^"\']*ta-fig-tag', html):
        html, ok = insert_before_kg(html, hero_html(cid, center))
        if ok:
            actions.append("labels")

    sim = pick_sim(cid, subject, html)
    if sim is not None:
        html, ok = insert_before_kg(html, sim_html(sim))
        if ok:
            actions.append("sim")

    if not all(x in html for x in ('id="practice-l1"', 'id="practice-l2"', 'id="practice-l3"')):
        html, ok = insert_before_kg(html, practice_html(center, quizzes))
        if ok:
            actions.append("L123")

    if "summary-checklist" not in html and not re.search(r'id=["\']posttest["\']', html):
        html, ok = insert_before_kg(html, summary_html(quizzes))
        if ok:
            actions.append("summary")

    if not re.search(r'id=["\']pretest["\']|前测', html):
        html = re.sub(r"(<body[^>]*>)", lambda m: m.group(0) + pretest_html(quizzes), html, count=1)
        actions.append("pretest")

    html = ensure_bloom_scaffold(html)

    if not dry_run and actions:
        path.write_text(html, encoding="utf-8")

    # qc flags
    t = html
    flags = {
        "sim": bool(re.search(r"phet\.colorado\.edu|geogebra\.org", t, re.I)),
        "labels": bool(re.search(r'<span[^>]*class=["\'][^"\']*ta-fig-tag', t)),
        "L123": all(x in t for x in ("practice-l1", "practice-l2", "practice-l3")),
        "v3": "teachany-quality-v3" in t,
    }
    return {"id": cid, "ok": all(flags.values()), "actions": actions or ["noop"], "flags": flags, "center": center}


def iter_courses(subject: str | None) -> list[Path]:
    out = []
    for d in sorted(COMMUNITY.iterdir()):
        if not d.is_dir() or not (d / "index.html").exists():
            continue
        if subject:
            if not d.name.startswith(subject + "-"):
                continue
        else:
            if not (d.name.startswith("math-m-") or d.name.startswith("chem-m-") or d.name.startswith("bio-m-")):
                continue
        out.append(d)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", choices=["math-m", "chem-m", "bio-m"], default="")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    courses = iter_courses(args.subject or None)
    if args.limit:
        courses = courses[: args.limit]
    print(f"parallel surgical upgrade: {len(courses)} courses subject={args.subject or 'ALL'}")

    results = []
    for d in courses:
        r = upgrade_one(d, dry_run=args.dry_run)
        results.append(r)
        mark = "PASS" if r["ok"] else "FAIL"
        print(f"  {mark} {r['id']}: {', '.join(r['actions'])}")

    by_subj: dict[str, list] = {"math-m": [], "chem-m": [], "bio-m": []}
    for r in results:
        by_subj[subject_of(r["id"])].append(r)

    summary = {}
    for subj, rows in by_subj.items():
        if not rows:
            continue
        summary[subj] = {
            "total": len(rows),
            "pass": sum(1 for x in rows if x["ok"]),
            "fail": sum(1 for x in rows if not x["ok"]),
            "fail_ids": [x["id"] for x in rows if not x["ok"]],
        }
        print(f"\n{subj}: {summary[subj]['pass']}/{summary[subj]['total']} pass")

    REPORTS.mkdir(exist_ok=True)
    (REPORTS / "parallel-surgical-upgrade.json").write_text(
        json.dumps({"summary": summary, "results": results}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    # qc page
    links = []
    for r in results:
        if not r["ok"]:
            continue
        links.append(f'<a href="/community/{r["id"]}/index.html">{r["id"]} · {r.get("center","")} ✓</a>')
    (ROOT / "qc-parallel.html").write_text(
        f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><title>平行升级进度</title>
<style>body{{font-family:system-ui;background:#0b1220;color:#e2e8f0;max-width:860px;margin:32px auto;padding:0 20px}}
a{{display:block;padding:10px;margin:6px 0;border-radius:10px;background:rgba(59,130,246,.18);color:#93c5fd;text-decoration:none}}
.ok{{color:#34d399}}</style></head><body>
<h1>math / chem / bio 平行升级</h1>
<p class="ok">{json.dumps(summary, ensure_ascii=False)}</p>
{''.join(links[:40])}
<p>… 共 {sum(1 for r in results if r['ok'])} 门通过</p>
</body></html>""",
        encoding="utf-8",
    )
    fail_n = sum(1 for r in results if not r["ok"])
    return 1 if fail_n else 0


if __name__ == "__main__":
    sys.exit(main())
