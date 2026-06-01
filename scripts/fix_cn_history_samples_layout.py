#!/usr/bin/env python3
"""Fix CN high history sample courseware: slide layout, diagrams, map eras."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "assets" / "maps" / "chrono-world"

SLIDE_CSS = """
<style id="cn-history-slide-fix">
body.play-mode .slide-page .card .grid { display: block !important; }
body.play-mode .slide-page .card .grid figure { margin: 0 0 16px; width: 100%; }
body.play-mode .slide-page .card .grid figure img,
body.play-mode .ta-figure-full img {
  width: 100%; height: auto; max-height: 68vh; object-fit: contain; display: block;
  border-radius: 12px; border: 1px solid rgba(255,255,255,.12);
}
body.play-mode .slide-page--map .ta-standard-section > h2,
body.play-mode .slide-page--map .ta-standard-section > p:first-of-type { display: none; }
body.play-mode .slide-page--map .thm-map-container { height: min(58vh, 480px) !important; min-height: 320px !important; }
body.play-mode .slide-page .card p { color: #d6b894; }
.thm-host .thm-title { color: #fff7ed !important; }
</style>
""".strip()

COURSES = {
    "ancient-china-h": {
        "short": "中国古代史总览",
        "concept_title": "核心概念：史料—解释—迁移",
        "process_title": "分析流程：定位→证据→机制→评价",
    },
    "hist-h-ancient-civ": {
        "short": "文明起源",
        "concept_title": "文明起源：证据类型",
        "process_title": "分析流程：遗址→推论→结论",
    },
    "hist-h-early-state": {
        "short": "早期国家",
        "concept_title": "早期国家：权力与分层",
        "process_title": "分析流程：卜辞→制度→统一",
    },
}

ANCIENT_CIV_ERAS = [
    {
        "id": "bce-3000", "label": "BCE 3000 文明曙光",
        "file": "chrono-world/001-bce-3000.geojson", "fill": "#d97706", "stroke": "#b45309",
        "desc": "<span class=\"thm-year-tag\">前3000</span><strong>文明发轫</strong>：尼罗河流域、两河流域、印度河流域与黄河流域分别出现复杂聚落与礼制萌芽。",
        "cities": [[34.80, 111.20, "仰韶", "Yangshao", "粟作农业聚落"], [30.37, 119.88, "良渚", "Liangzhu", "玉器礼制"], [34.70, 112.20, "二里头", "Erlitou", "早期复杂社会"]],
    },
    {
        "id": "bce-1500", "label": "BCE 1500 青铜时代",
        "file": "chrono-world/002-bce-1500.geojson", "fill": "#2563eb", "stroke": "#1d4ed8",
        "desc": "<span class=\"thm-year-tag\">前1500</span><strong>青铜文明</strong>：商朝与赫梯、埃及新王国等并存，国家权力与青铜礼器结合。",
        "cities": [[34.77, 113.65, "殷墟", "Yin Xu", "商都"], [25.70, 32.65, "底比斯", "Thebes", "埃及"], [32.54, 44.42, "巴比伦", "Babylon", "两河"]],
    },
    {
        "id": "bce-1000", "label": "BCE 1000 铁器时代",
        "file": "chrono-world/003-bce-1000.geojson", "fill": "#7c3aed", "stroke": "#6d28d9",
        "desc": "<span class=\"thm-year-tag\">前1000</span><strong>铁器扩散</strong>：西周分封、亚述崛起，铁器推动战争与社会组织变化。",
        "cities": [[34.27, 108.95, "镐京", "Haojing", "西周"], [36.36, 43.12, "尼尼微", "Nineveh", "亚述"]],
    },
    {
        "id": "bce-500", "label": "BCE 500 轴心时代",
        "file": "chrono-world/004-bce-500.geojson", "fill": "#059669", "stroke": "#047857",
        "desc": "<span class=\"thm-year-tag\">前500</span><strong>轴心时代</strong>：波斯帝国、希腊城邦、东周诸子百家并存，思想与政治变革共振。",
        "cities": [[34.77, 113.65, "洛阳", "Luoyang", "东周"], [37.97, 23.73, "雅典", "Athens", "希腊"]],
    },
]


def svg_concept(short: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 420" width="900" height="420">
<rect width="900" height="420" fill="#101827"/>
<text x="450" y="48" fill="#e2e8f0" font-size="28" font-weight="700" text-anchor="middle">核心概念 · {short}</text>
<rect x="40" y="90" width="250" height="280" rx="16" fill="#13243a" stroke="#38bdf8"/>
<text x="165" y="135" fill="#7dd3fc" font-size="22" text-anchor="middle">史料证据</text>
<text x="65" y="185" fill="#e5e7eb" font-size="18">考古遗存</text>
<text x="65" y="220" fill="#e5e7eb" font-size="18">文献记载</text>
<text x="65" y="255" fill="#e5e7eb" font-size="18">图像器物</text>
<rect x="325" y="90" width="250" height="280" rx="16" fill="#1f2937" stroke="#a78bfa"/>
<text x="450" y="135" fill="#c4b5fd" font-size="22" text-anchor="middle">历史解释</text>
<text x="350" y="185" fill="#e5e7eb" font-size="18">因果机制</text>
<text x="350" y="220" fill="#e5e7eb" font-size="18">结构变迁</text>
<text x="350" y="255" fill="#e5e7eb" font-size="18">阶段比较</text>
<rect x="610" y="90" width="250" height="280" rx="16" fill="#052e2b" stroke="#22c55e"/>
<text x="735" y="135" fill="#86efac" font-size="22" text-anchor="middle">迁移应用</text>
<text x="635" y="185" fill="#e5e7eb" font-size="18">新材料题</text>
<text x="635" y="220" fill="#e5e7eb" font-size="18">证据链表达</text>
<text x="635" y="255" fill="#e5e7eb" font-size="18">历史评价</text>
</svg>'''


def svg_process(short: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 320" width="900" height="320">
<rect width="900" height="320" fill="#0f172a"/>
<text x="450" y="42" fill="#e2e8f0" font-size="26" font-weight="700" text-anchor="middle">分析流程 · {short}</text>
<g fill="#1e293b" stroke="#475569"><rect x="50" y="80" width="180" height="200" rx="14"/><rect x="270" y="80" width="180" height="200" rx="14"/><rect x="490" y="80" width="180" height="200" rx="14"/><rect x="710" y="80" width="140" height="200" rx="14"/></g>
<text x="140" y="130" fill="#7dd3fc" font-size="20" text-anchor="middle">定位</text><text x="140" y="200" fill="#cbd5e1" font-size="16" text-anchor="middle">时空框架</text>
<text x="360" y="130" fill="#c4b5fd" font-size="20" text-anchor="middle">证据</text><text x="360" y="200" fill="#cbd5e1" font-size="16" text-anchor="middle">史料分类</text>
<text x="580" y="130" fill="#fbbf24" font-size="20" text-anchor="middle">机制</text><text x="580" y="200" fill="#cbd5e1" font-size="16" text-anchor="middle">因果链条</text>
<text x="780" y="130" fill="#86efac" font-size="20" text-anchor="middle">评价</text><text x="780" y="200" fill="#cbd5e1" font-size="16" text-anchor="middle">意义</text>
</svg>'''


def split_core_slide(html: str, meta: dict) -> str:
    pat = (
        r'<section class="slide-page"[^>]*data-tsh="核心概念图"[^>]*>\s*'
        r'<section class="section" id="core"[^>]*>.*?</section>\s*</section>'
    )
    rep = f'''<section class="slide-page" data-page-type="concept" data-tsh="{meta["concept_title"]}">
<section class="section" id="core-concept" data-tts="core-concept" data-bloom-level="understand" data-scaffold="full"><div class="card">
<h2>核心概念结构</h2>
<p>把本课知识拆成三层：先找可核验史料，再写因果机制，最后完成迁移表达。避免只背结论、不引证据。</p>
<figure class="ta-figure-full"><img src="./assets/concept-diagram.svg" alt="核心概念结构图"></figure>
</div></section></section>
<section class="slide-page" data-page-type="concept" data-tsh="{meta["process_title"]}">
<section class="section" id="core-process" data-tts="core-process" data-bloom-level="understand" data-scaffold="full"><div class="card">
<h2>历史分析流程</h2>
<p>答题时按“定位→证据→机制→评价”四步组织语言；每步至少对应一条材料信息，防止空泛概括。</p>
<figure class="ta-figure-full"><img src="./assets/process-diagram.svg" alt="分析流程图"></figure>
</div></section></section>'''
    return re.sub(pat, rep, html, count=1, flags=re.S)


def fix_map_slide(html: str) -> str:
    html = re.sub(
        r'(<section class="slide-page"[^>]*data-tsh="🗺️[^"]*"[^>]*)>',
        r'\1 class="slide-page--map">',
        html,
        count=1,
    )
    return html


def patch_ancient_civ_map(html: str) -> str:
    cfg = {
        "eras": ANCIENT_CIV_ERAS,
        "center": [28, 55],
        "zoom": 3,
        "fitBounds": [[10, 20], [50, 120]],
        "minZoom": 2,
        "maxZoom": 8,
        "overlays": [{
            "id": "rivers", "label": "🌊 黄河故道",
            "file": "details/rivers-historical.geojson",
            "style": {"color": "#0ea5e9", "weight": 3},
            "visible": False,
        }],
        "hillshade": "physical/hillshade/global-color-hillshade-2k.jpg",
    }
    new_json = json.dumps(cfg, ensure_ascii=False, indent=2)
    return re.sub(
        r'(<script type="application/json" data-teachany-map-config>)([\s\S]*?)(</script>)',
        lambda m: m.group(1) + "\n" + new_json + "\n    " + m.group(3),
        html,
        count=1,
    )


def copy_extra_geojson(course_dir: Path) -> None:
    dest = course_dir / "assets" / "maps" / "chrono-world"
    dest.mkdir(parents=True, exist_ok=True)
    for name in ("003-bce-1000.geojson", "004-bce-500.geojson"):
        src = MAPS / name
        if src.exists():
            shutil.copy2(src, dest / name)


def fix_one(cid: str) -> None:
    meta = COURSES[cid]
    d = ROOT / "community" / cid
    html_path = d / "index.html"
    html = html_path.read_text(encoding="utf-8")
    if "cn-history-slide-fix" not in html:
        html = html.replace("</head>", SLIDE_CSS + "\n</head>", 1)
    (d / "assets" / "concept-diagram.svg").write_text(svg_concept(meta["short"]), encoding="utf-8")
    (d / "assets" / "process-diagram.svg").write_text(svg_process(meta["short"]), encoding="utf-8")
    html = split_core_slide(html, meta)
    html = fix_map_slide(html)
    if cid == "hist-h-ancient-civ":
        copy_extra_geojson(d)
        html = patch_ancient_civ_map(html)
    html_path.write_text(html, encoding="utf-8")
    print("fixed", cid)


def main() -> None:
    for cid in COURSES:
        fix_one(cid)


if __name__ == "__main__":
    main()
