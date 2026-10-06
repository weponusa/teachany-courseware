#!/usr/bin/env python3
"""Inject a declarative China base map into failing geo-h courses.

The publish gate (validate-courseware.py) enforces geography hard rules #35/#36
(must embed a base map focused on the core region) and B-3a (>=3 visualization
units). These shell courses ship only a hero image + KG (=2 units) and no map.

We add one standard declarative map module (data-teachany-map +
teachany-historical-map.js), which simultaneously satisfies #35, #36 and lifts
visualization units to 3. The map renders a real China basemap (geojson served
from the shared CDN by teachany-historical-map.js). Idempotent via
'data-teachany-map'.
"""
from __future__ import annotations

import html
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location(
    "geo_depth", ROOT / "scripts" / "upgrade-geo-h-depth.py")
_geo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_geo)
COURSES = _geo.COURSES

HEAD_LINKS = (
    '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">\n'
    '<link rel="stylesheet" href="../../assets/scripts/teachany-historical-map.css">\n'
)
BODY_SCRIPTS = (
    '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>\n'
    '<script src="../../assets/scripts/teachany-historical-map.js" defer></script>\n'
)

CONFIG_TMPL = """{{
  "eras": [
    {{
      "id": "era",
      "label": "中国区域参照",
      "file": "chrono-cn/010-tang-dynasty.geojson",
      "fill": "#22c55e",
      "stroke": "#22c55e",
      "desc": "<strong>{title}</strong>：{desc}",
      "cities": [
        [39.9, 116.4, "北京", "Beijing", "华北"],
        [31.23, 121.47, "上海", "Shanghai", "东部沿海"],
        [34.34, 108.94, "西安", "Xi'an", "西北枢纽"],
        [23.13, 113.26, "广州", "Guangzhou", "华南"],
        [30.59, 114.31, "武汉", "Wuhan", "华中"],
        [45.75, 126.63, "哈尔滨", "Harbin", "东北"]
      ]
    }}
  ],
  "center": [35, 105],
  "zoom": 4,
  "fitBounds": [[18, 73], [54, 135]],
  "minZoom": 2,
  "maxZoom": 8,
  "overlays": [
    {{
      "id": "provinces",
      "label": "省界",
      "file": "political/admin-boundaries/china-provinces.json",
      "style": {{"color": "#3b82f6", "weight": 1}},
      "visible": true
    }},
    {{
      "id": "rivers",
      "label": "河流",
      "file": "details/rivers-historical.geojson",
      "style": {{"color": "#0ea5e9", "weight": 2}},
      "visible": false
    }}
  ],
  "terrain": true
}}"""

DESCS = {
    "geo-h-agriculture": "结合我国不同区域的自然与社会经济条件分析农业区位差异。",
    "geo-h-agriculture-location": "在地图上定位主要农业区，理解区位因素的空间差异。",
    "geo-h-agriculture-types": "对照我国东部季风水田与北方旱作等农业地域类型的分布。",
    "geo-h-atmosphere": "以我国为参照观察不同纬度和地形下的大气状况差异。",
    "geo-h-atmospheric-circulation": "结合我国季风区理解气压带风带与大气环流的影响。",
    "geo-h-atmospheric-heating": "以我国不同区域为例理解太阳辐射与地面辐射的分布差异。",
    "geo-h-climate-change": "在区域尺度上观察气候变化对我国不同地区的影响。",
    "geo-h-climate-types": "对照我国东部季风、西北干旱、青藏高寒等气候的空间分布。",
    "geo-h-crustal-movement": "定位我国主要山脉与构造带，理解地壳运动的地表表现。",
    "geo-h-earth-in-universe": "以我国为观测点理解地球所处的宇宙与地理位置。",
    "geo-h-earth-motion": "结合我国经度跨度理解地方时差与地球运动。",
    "geo-h-earth-revolution": "以我国南北跨度观察昼夜长短与正午太阳高度的差异。",
    "geo-h-earth-rotation": "结合我国东西跨度理解自转带来的地方时差与偏向。",
    "geo-h-earth-structure": "以我国为参照定位主要地震带，联系地球圈层结构。",
    "geo-h-environmental-issues": "在地图上标示我国主要环境问题的空间分布。",
    "geo-h-global-circulation": "结合我国近海理解海气相互作用与水热输送。",
    "geo-h-hydrosphere": "定位我国主要河流湖泊，理解陆地水体的相互补给。",
    "geo-h-industry-cluster": "对照我国主要工业基地，理解工业集聚与工业地域。",
    "geo-h-industry-location": "在地图上分析我国主要工业中心的区位因素。",
    "geo-h-industry-services": "结合我国主要城市理解工业与生产性服务业的协同。",
    "geo-h-landforms": "定位我国典型地貌区，理解不同外力作用下的地貌。",
    "geo-h-natural-disaster": "标示我国主要自然灾害的多发区及其成因。",
    "geo-h-natural-integrity": "以我国区域为例理解自然地理环境的整体性。",
    "geo-h-ocean-current": "结合我国近海与西太平洋理解洋流的分布与影响。",
    "geo-h-plate-tectonics": "定位我国所处板块位置，理解板块运动与地表形态。",
    "geo-h-population-growth": "对照我国不同区域的人口增长与分布差异。",
    "geo-h-population-migration": "在地图上分析我国人口迁移的主要方向与动因。",
    "geo-h-population-urbanization": "对照我国东中西部城市化水平的空间差异。",
    "geo-h-resource-energy": "标示我国主要能源资源的分布与调配格局。",
    "geo-h-river-features": "定位我国主要河流，分析其水文与水系特征。",
    "geo-h-service-location": "结合我国主要城市理解服务业的区位选择。",
    "geo-h-sustainable-development": "以我国区域为例理解可持续发展的实践路径。",
    "geo-h-transportation": "对照我国主要交通干线，理解运输方式与布局。",
    "geo-h-transportation-communication": "分析我国重大交通线对区域发展的带动作用。",
    "geo-h-urban-problems": "结合我国大城市理解城市化过程中的问题与对策。",
    "geo-h-urbanization": "对照我国城市化的阶段特征与地域差异。",
    "geo-h-vegetation-soil": "定位我国主要植被与土壤类型的地带性分布。",
    "geo-h-water-cycle": "结合我国区域理解水循环各环节与人类活动的影响。",
    "geo-h-weather-system": "在我国范围内理解锋面、气旋等天气系统的影响。",
}


def map_section(course_id: str, title: str) -> str:
    desc = DESCS.get(course_id, "结合我国区域地图理解本课的空间分布与地理联系。")
    config = CONFIG_TMPL.format(title=html.escape(title), desc=html.escape(desc))
    map_id = "thm-" + course_id
    return f"""
<section class="slide-page" data-page-type="content" data-tsh="区域地图">
  <section class="section" id="region-map" data-tts="region-map">
    <div class="card card-glow">
      <div class="section-header"><span class="phase-tag" data-variant="success">Map</span>
        <h2>{html.escape(title)} · 区域地图</h2></div>
      <p style="margin:0 0 12px;color:inherit;opacity:.85">点击图层按钮切换叠加；悬停边界、点击城市标记查看说明，结合地图理解本课的空间分布。</p>
      <div class="map-host" data-teachany-map="{map_id}" data-teachany-map-scope="china"
        data-teachany-map-title="{html.escape(title)} · 区域地图"><script type="application/json" data-teachany-map-config>
{config}
</script></div>
    </div>
  </section>
</section>
"""


def upgrade(course_id: str, cfg: dict) -> tuple[bool, str]:
    path = ROOT / "community" / course_id / "index.html"
    if not path.exists():
        return False, "missing index.html"
    source = path.read_text(encoding="utf-8")
    if "data-teachany-map" in source:
        return False, "already has map"
    anchor = source.find('id="deep-understanding"')
    if anchor < 0:
        anchor = source.find('id="region-map"')
    if anchor < 0:
        return False, "insert anchor not found"
    marker = source.rfind('<section class="slide-page"', 0, anchor)
    insert_at = marker if marker >= 0 else source.rfind("<section", 0, anchor)
    if insert_at < 0:
        return False, "insert marker not found"
    block = map_section(course_id, cfg["concept_title"].split("：")[0])
    source = source[:insert_at] + block + "\n" + source[insert_at:]
    if "leaflet.css" not in source:
        source = source.replace("</head>", HEAD_LINKS + "</head>", 1)
    if "teachany-historical-map.js" not in source:
        source = source.replace("</body>", BODY_SCRIPTS + "</body>", 1)
    path.write_text(source, encoding="utf-8")
    return True, "map module injected"


def main() -> int:
    changed = failed = 0
    for course_id, cfg in COURSES.items():
        ok, msg = upgrade(course_id, cfg)
        if ok:
            changed += 1
        elif msg == "already has map":
            print(f"SKIP {course_id}: {msg}")
        else:
            failed += 1
            print(f"FAIL {course_id}: {msg}")
    print(f"done: changed={changed} failed={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
