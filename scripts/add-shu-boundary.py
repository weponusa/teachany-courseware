#!/usr/bin/env python3
"""add-shu-boundary.py — 构造蜀汉疆域近似边界并入三国地图数据
依据：《中国历史地图集》蜀汉益州图幅的山川锚点（秦岭祁山线、大巴山、巫山、
横断山、金沙江——这些地物的经纬度是确定的地理事实），连线构造教学示意的
蜀汉政权边界。示意性近似，非精确政区复原。
并入 assets/maps/details/tk-shu.geojson 并加进第一幕 overlays。
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "community/hist-h-wei-jin-tang/assets/maps/details"

# 蜀汉疆域外轮廓（[lng, lat]，顺时针；拐点全部落在真实地理锚点上）
SHU_RING = [
    # 北界：祁山—武都—阳平关—汉中北缘（秦岭一线，对魏前线）
    [104.2, 34.4], [105.5, 33.6], [106.6, 33.1], [107.3, 33.0], [108.4, 33.4],
    [108.9, 33.7],   # 汉中盆地北缘
    # 东北界：上庸以南（228年后东三郡属魏），房陵—巫溪山地
    [110.2, 32.6], [110.8, 31.8],
    # 东界：巫山—建平—天门—武陵南缘（对吴前线）
    [110.6, 30.4], [111.2, 29.0], [111.0, 27.8], [110.5, 26.5],
    # 南界：郁林西—兴古—贲古—哀牢（庲降都督辖区南缘，接交趾/永昌外域）
    [110.2, 24.8], [107.8, 23.6], [105.6, 23.2], [103.8, 23.3], [102.0, 22.6],
    [100.5, 21.9],
    # 西界：永昌西—越嶲—汶山（横断山脉，接外域羌胡）
    [99.0, 23.8], [98.3, 25.2], [99.0, 27.2], [100.3, 29.2], [101.6, 30.8],
    [102.4, 32.3], [103.2, 33.5],
]

FEATURE = {
    "type": "Feature",
    "properties": {
        "NAME_CH": "蜀汉", "NAME_EN": "Shu Han",
        "POWER": "蜀",
        "LEVEL": "country",
        "NOTE_ID": "teachany-approx",
        "OBJ_TYPE": "POLYGON",
    },
    "geometry": {"type": "Polygon", "coordinates": [SHU_RING]},
}


def main():
    out = BASE / "tk-shu.geojson"
    fc = {"type": "FeatureCollection", "name": "蜀汉（教学示意边界）", "features": [FEATURE]}
    out.write_text(json.dumps(fc, ensure_ascii=False), encoding="utf-8")
    print(f"{out.name} 写入完成（{len(SHU_RING)} 锚点，示意边界）")

    # 加进第一幕 overlays（visible: true 默认显示）
    ipage = ROOT / "community/hist-h-wei-jin-tang/index.html"
    html = ipage.read_text(encoding="utf-8")
    m = re.search(r'"overlays": \[\s*\{', html)
    if not m:
        print("未找到 overlays")
        return
    new_overlay = '''{
      "id": "shu",
      "label": "蜀汉示意界",
      "file": "details/tk-shu.geojson",
      "style": {
        "color": "#34d399",
        "weight": 1.2,
        "dashArray": null
      },
      "visible": true
    }, {
      "id": "capitals",
      "label": "古都",
      "file": "details/capitals-extended.geojson",
      "style": {
        "color": "#a855f7",
        "radius": 4
      },
      "visible": false'''
    html = html[:m.start()] + '"overlays": [\n    ' + new_overlay + html[m.end():]
    ipage.write_text(html, encoding="utf-8")
    print("overlays 已加蜀汉示意界")


if __name__ == "__main__":
    main()
