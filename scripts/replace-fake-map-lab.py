#!/usr/bin/env python3
"""把 45 个课件里的假地图实验（mGeoFiles 调试画布）替换为真实地图实验组件
（teachany-geo-lab：真实国界底图 + 天文公式太阳辐射 + 纬带气候平均值）。

手术内容（每课件）：
1. 替换 <section id="interactive-lab"> 内部为真实组件容器 + 配置
2. 切除脚本块中的假代码尾段（map-canvas 起的 canvas/drawWorld/drawGeo 等），
   保留 FEEDBACK/checkAnswer 等真实代码
3. head 注入 teachany-geo-lab.css，尾部注入 teachany-geo-lab.js
4. 删除伪造的 assets/maps/world-outline.geojson（10 个手编坐标的假多边形）

用法：--only geo-h-atmospheric-heating --dry
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMMUNITY = ROOT / "community"

SPECIAL = {"imperial-unification", "geo-m-contour-topographic"}  # 单独处理

SECTION_RE = re.compile(r'<section\b[^>]*id="interactive-lab"[^>]*>', re.I)
SCRIPT_RE = re.compile(r"<script\b[^>]*>[\s\S]*?</script>", re.I)
FAKE_MARKER = "const canvas = document.getElementById('map-canvas');"

CSS_LINK = '<link rel="stylesheet" href="../../assets/scripts/teachany-geo-lab.css">'
JS_TAG = '<script src="../../assets/scripts/teachany-geo-lab.js" defer></script>'


def find_section_span(html: str):
    """定位 interactive-lab 顶层 section 的起止（处理嵌套 section）。"""
    m = SECTION_RE.search(html)
    if not m:
        return None
    depth = 1
    for t in re.finditer(r"<section\b[^>]*>|</section>", html[m.end():], re.I):
        if t.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                return m.start(), m.end() + t.end()
        else:
            depth += 1
    return None


def extract_topic(html: str, cid: str) -> str:
    # 优先从实验任务文本提取：解释“X”；限长并排除标签字符
    m = re.search(r"本课任务[^“”\"]*[“\"]([^”\"<>\n]{2,30})[”\"]", html)
    if m:
        return m.group(1)
    m = re.search(r"解释[“\"]([^”\"<>\n]{2,30})[”\"]", html)
    if m:
        return m.group(1)
    mf = COMMUNITY / cid / "manifest.json"
    if mf.is_file():
        try:
            return json.loads(mf.read_text(encoding="utf-8")).get("name") or cid
        except Exception:
            pass
    return cid


def fix_file(f: Path, dry: bool):
    cid = f.parent.name
    html = f.read_text(encoding="utf-8", errors="replace")
    if "mGeoFiles" not in html:
        return None

    span = find_section_span(html)
    if not span:
        return f"⚠️ 未找到 interactive-lab section"
    topic = extract_topic(html, cid)

    old_open = SECTION_RE.search(html).group(0)
    new_inner = (
        '<div class="lesson-panel"><span class="phase-tag">Real Map Lab</span>'
        f'<h2>真实地图实验：纬度 × 月份，看「{topic}」的真实空间格局</h2>'
        '<p style="color:var(--muted)">底图为 Natural Earth 真实国界；太阳辐射为天文公式精确值，'
        '气温/降水为 10° 纬带气候平均值。拖动纬度与月份，用一句话解释机制。</p>'
        '<div id="teachany-geo-lab"></div></div>'
    )
    new_section = old_open + new_inner + "</section>"
    html = html[: span[0]] + new_section + html[span[1]:]

    # 切除假 JS 尾段
    cut = False
    def excise(m):
        nonlocal cut
        seg = m.group(0)
        if "mGeoFiles" not in seg:
            return seg
        i = seg.find(FAKE_MARKER)
        if i < 0:
            return seg
        cut = True
        return seg[:i].rstrip() + "\n</script>"
    html = SCRIPT_RE.sub(excise, html)
    if not cut:
        return "⚠️ 假代码标记未找到"

    # 注入配置 + 组件
    cfg = json.dumps({"topic": topic, "task": f"拖动纬度与月份，读真实数据，用「纬度位置 + 图层机制」解释{topic}。"},
                     ensure_ascii=False)
    inject = f"<script>window.__TEACHANY_GEO_LAB__={cfg};</script>\n{JS_TAG}\n</body>"
    html = html.replace("</body>", inject, 1)
    if "teachany-geo-lab.css" not in html:
        html = html.replace("</head>", CSS_LINK + "\n</head>", 1)

    # 删除伪造 geojson
    fake_geo = f.parent / "assets" / "maps" / "world-outline.geojson"
    removed_geo = False
    if fake_geo.is_file() and not dry:
        fake_geo.unlink()
        removed_geo = True

    if not dry:
        f.write_text(html, encoding="utf-8")
    return f"✏️ 替换完成（topic={topic}，删假geojson={removed_geo}）"


def main():
    only = None
    dry = "--dry" in sys.argv
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]
    n = 0
    for f in sorted(COMMUNITY.glob("*/index.html")):
        cid = f.parent.name
        if cid in SPECIAL:
            continue
        if only and only not in cid:
            continue
        r = fix_file(f, dry)
        if r:
            print(f"{'[DRY] ' if dry else ''}{cid}: {r}")
            n += 1
    print(f"\n处理 {n} 个{'（dry-run）' if dry else ''}")


if __name__ == "__main__":
    main()
