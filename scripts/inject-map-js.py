#!/usr/bin/env python3
"""inject-map-js.py — 给有地图容器但缺渲染 JS 的课件注入 Leaflet + teachany-historical-map.js
同时补齐 leaflet.css（若缺）。幂等。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
LEAFLET_CSS = '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">'
MAP_SCRIPTS = ('<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>\n'
               '<script src="../../assets/scripts/teachany-historical-map.js" defer></script>')


def main():
    fixed, skipped = 0, []
    for f in sorted(COMMUNITY.glob("*/index.html")):
        html = f.read_text(encoding="utf-8", errors="replace")
        if "data-teachany-map" not in html:
            continue
        if 'http-equiv="refresh"' in html[:3000]:
            continue
        if "teachany-historical-map.js" in html:
            continue
        # 补 CSS
        if "leaflet.css" not in html:
            if "</head>" in html:
                html = html.replace("</head>", LEAFLET_CSS + "\n</head>", 1)
        # 补 historical-map.css（少数缺）
        if "teachany-historical-map.css" not in html:
            html = html.replace("</head>",
                                '<link rel="stylesheet" href="../../assets/scripts/teachany-historical-map.css">\n</head>', 1)
        # 注入 JS（</body> 前）
        if "</body>" in html:
            html = html.replace("</body>", MAP_SCRIPTS + "\n</body>", 1)
        else:
            html += "\n" + MAP_SCRIPTS + "\n"
        f.write_text(html, encoding="utf-8")
        fixed += 1
    print(f"注入地图JS: {fixed} 个课件")


if __name__ == "__main__":
    main()
