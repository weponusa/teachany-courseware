#!/usr/bin/env python3
"""Replace Tang-dynasty placeholder maps on geography courses with modern layers.

Root cause: cn-map-config.py used chrono-cn/010-tang-dynasty.geojson as the
default "中国疆域" era for every geography course. Climate / monsoon / terrain
lessons therefore showed Tang borders.

This rewriter:
  - China-topic geo → political/china-modern/provinces.geojson
  - World-topic geo → political/world/countries.geojson
  - Drops the duplicate historical-rivers overlay (or swaps to modern rivers)
  - Keeps existing city pins unless the course is climate-related
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

TANG = "chrono-cn/010-tang-dynasty.geojson"
CHINA_FILE = "political/china-modern/provinces.geojson"
WORLD_FILE = "political/world/countries.geojson"
RIVER_FILE = "physical/rivers/ne_10m_rivers_china.json"

WORLD_HINTS = (
    "world", "continent", "globe", "season", "earth", "ocean", "climate-m",
    "population-distribution", "terrain-types",
)

CLIMATE_HINTS = ("climate", "weather", "monsoon", "气候", "天气", "气温", "降水", "季风")

CLIMATE_CITIES = [
    [45.75, 126.65, "哈尔滨", "Harbin", "温带季风·冬季严寒"],
    [39.90, 116.40, "北京", "Beijing", "温带季风"],
    [30.59, 114.31, "武汉", "Wuhan", "亚热带·冬冷夏热"],
    [23.13, 113.26, "广州", "Guangzhou", "亚热带·降水丰沛"],
    [43.83, 87.62, "乌鲁木齐", "Urumqi", "温带大陆性·干旱"],
    [29.65, 91.13, "拉萨", "Lhasa", "高原山地气候"],
]

WORLD_CITIES = [
    [51.51, -0.13, "伦敦", "London", "温带海洋性气候"],
    [30.04, 31.24, "开罗", "Cairo", "热带沙漠气候"],
    [1.35, 103.82, "新加坡", "Singapore", "热带雨林气候"],
    [-33.87, 151.21, "悉尼", "Sydney", "亚热带湿润气候"],
]

CFG_RE = re.compile(
    r'(<script type="application/json" data-teachany-map-config>\s*)(\{.*?\})(\s*</script>)',
    re.S,
)
HINT_OLD = "点击时代/图层按钮切换地图；悬停边界，点击城市标记查看说明。"
HINT_NEW = "拖动缩放地图，点击城市标记查看气候或区域说明；可开河流图层对照。"


def is_world(cid: str, title: str) -> bool:
    blob = f"{cid} {title}".lower()
    return any(h in blob for h in WORLD_HINTS)


def is_climate(cid: str, title: str, desc: str) -> bool:
    blob = f"{cid} {title} {desc}"
    return any(h in blob for h in CLIMATE_HINTS)


def rewrite_cfg(cfg: dict, cid: str, title: str) -> dict:
    eras = cfg.get("eras") or []
    if not eras:
        return cfg
    era = eras[0]
    file = era.get("file") or ""
    if TANG not in file and "tang-dynasty" not in file:
        return cfg

    desc = era.get("desc") or title
    world = is_world(cid, title)
    climate = is_climate(cid, title, desc)

    if world:
        era["id"] = "modern-world"
        era["label"] = "当代世界"
        era["file"] = WORLD_FILE
        era["fill"] = "#38bdf8"
        era["stroke"] = "#38bdf8"
        era["desc"] = f"<strong>{title}</strong>：用当代国界阅读大洲、气候带与空间格局。"
        era["cities"] = WORLD_CITIES
        cfg["scope"] = "world"
        cfg["center"] = [20, 20]
        cfg["zoom"] = 2
        cfg["fitBounds"] = [[-50, -140], [70, 160]]
        cfg["overlays"] = []
    else:
        era["id"] = "modern-china"
        era["label"] = "当代中国"
        era["file"] = CHINA_FILE
        era["fill"] = "#22c55e"
        era["stroke"] = "#22c55e"
        era["desc"] = f"<strong>{title}</strong>：用当代省级政区阅读位置、范围与空间联系。"
        if climate:
            era["cities"] = CLIMATE_CITIES
        cfg["scope"] = "china"
        cfg["center"] = [35, 105]
        cfg["zoom"] = 4
        cfg["fitBounds"] = [[18, 73], [54, 135]]
        cfg["overlays"] = [
            {
                "id": "rivers",
                "label": "主要河流",
                "file": RIVER_FILE,
                "style": {"color": "#0ea5e9", "weight": 2},
                "visible": False,
            }
        ]
    cfg["eras"] = [era]
    cfg["terrain"] = True
    return cfg


def extract_title(html: str, cid: str) -> str:
    m = re.search(r'data-teachany-map-title="([^"]+)"', html)
    if m:
        return m.group(1).replace(" · 区域地图", "")
    m = re.search(r"<title>([^<]+)</title>", html)
    return (m.group(1).split("·")[0].strip() if m else cid)


def patch_html(html: str, cid: str) -> str | None:
    if TANG not in html and "tang-dynasty" not in html:
        return None
    title = extract_title(html, cid)
    changed = False

    def _sub(match: re.Match) -> str:
        nonlocal changed
        raw = match.group(2)
        try:
            cfg = json.loads(raw)
        except json.JSONDecodeError:
            return match.group(0)
        new_cfg = rewrite_cfg(cfg, cid, title)
        if new_cfg is cfg and (cfg.get("eras") or [{}])[0].get("file") in (TANG,):
            return match.group(0)
        if (cfg.get("eras") or [{}])[0].get("file") in (CHINA_FILE, WORLD_FILE):
            body = json.dumps(new_cfg, ensure_ascii=False, indent=2)
            changed = True
            return match.group(1) + body + match.group(3)
        body = json.dumps(new_cfg, ensure_ascii=False, indent=2)
        changed = True
        return match.group(1) + body + match.group(3)

    html2 = CFG_RE.sub(_sub, html, count=1)
    if HINT_OLD in html2:
        html2 = html2.replace(HINT_OLD, HINT_NEW, 1)
        changed = True
    html2 = html2.replace('data-teachany-map-scope="china"', 'data-teachany-map-scope="world"', 1) if is_world(cid, title) else html2
    if "tang-dynasty" in html2:
        # still leftover in this map block? keep going if we already replaced the file
        pass
    return html2 if changed else None


def main() -> int:
    updated = skipped = failed = 0
    for path in sorted(COMMUNITY.glob("geo-*/index.html")):
        cid = path.parent.name
        src = path.read_text(encoding="utf-8")
        if TANG not in src and "tang-dynasty" not in src:
            skipped += 1
            continue
        out = patch_html(src, cid)
        if out is None:
            failed += 1
            print(f"FAIL {cid}: no rewrite")
            continue
        path.write_text(out, encoding="utf-8")
        kind = "world" if is_world(cid, extract_title(out, cid)) else "china"
        updated += 1
        print(f"OK {cid} ({kind})")
    print(f"done: updated={updated} skipped={skipped} failed={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
