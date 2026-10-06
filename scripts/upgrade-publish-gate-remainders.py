#!/usr/bin/env python3
"""Fix remaining publish-gate failures after teaching-quality gate cleared.

Targets (错误 > 0):
  - geo-h-monsoon-system / natural-zones / urban-structure: #35/#36 + B-3a
  - math-elem-area-units / average-median / complex-word-problems / decimal-operations: B-3a
  - lithium-ion-battery-tech: B-3a

Injects declarative China map (geo-h) or a topic canvas (others). No mp4.
Idempotent via data-teachany-map / id="b3a-visual".
"""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HEAD_LINKS = (
    '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">\n'
    '<link rel="stylesheet" href="../../assets/scripts/teachany-historical-map.css">\n'
)
BODY_SCRIPTS = (
    '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>\n'
    '<script src="../../assets/scripts/teachany-historical-map.js" defer></script>\n'
)

GEO = {
    "geo-h-monsoon-system": (
        "季风系统",
        "结合我国季风气候区理解冬夏季风的源地、风向与降水格局。",
    ),
    "geo-h-natural-zones": (
        "自然带",
        "对照我国从沿海到内陆、从赤道到两极的自然带更替格局。",
    ),
    "geo-h-urban-structure": (
        "城市空间结构",
        "结合我国主要城市理解中心商务区、居住区、工业区的空间布局。",
    ),
}

CANVAS = {
    "math-elem-area-units": {
        "title": "面积单位换算示意",
        "desc": "1 平方分米 = 100 平方厘米。左边大正方形表示 1 dm²，里面正好能放下 10×10=100 个小方格（每格 1 cm²）。换算时记住相邻面积单位之间通常是 100 倍。",
        "kind": "area_units",
    },
    "math-elem-average-median": {
        "title": "平均数与中位数对比",
        "desc": "一组数据先按大小排好序，正中间的数是中位数；把所有数加起来再除以个数得到平均数。看图区分：中位数看位置，平均数看总和。",
        "kind": "avg_median",
    },
    "math-elem-complex-word-problems": {
        "title": "复合应用题：分步图示",
        "desc": "复合应用题常有两步或更多：先求出中间量，再求最终问题。用箭头把已知→中间量→所求连起来，每一步写清用什么运算，就不容易漏步或乱算。",
        "kind": "word_problem",
    },
    "math-elem-decimal-operations": {
        "title": "小数加减：数位对齐",
        "desc": "小数加减时要把小数点对齐（也就是相同数位对齐），再逐位相加减。竖式里小数点上下对齐后，计算过程和整数加减一样。",
        "kind": "decimal_ops",
    },
    "lithium-ion-battery-tech": {
        "title": "锂离子电池充放电示意",
        "desc": "充电时锂离子从正极经电解液迁移到负极；放电时反向迁移并对外供电。理解“锂离子在正负极之间往返”，就能抓住锂电工作原理的核心。",
        "kind": "battery",
    },
}

MAP_CONFIG = """{{
  "eras": [{{
    "id": "era",
    "label": "中国区域参照",
    "file": "chrono-cn/010-tang-dynasty.geojson",
    "fill": "#22c55e",
    "stroke": "#22c55e",
    "desc": "<strong>{title}</strong>：{desc}",
    "cities": [
      [39.9, 116.4, "北京", "Beijing", "华北"],
      [31.23, 121.47, "上海", "Shanghai", "东部沿海"],
      [34.34, 108.94, "西安", "Xi'an", "西北"],
      [23.13, 113.26, "广州", "Guangzhou", "华南"]
    ]
  }}],
  "center": [35, 105],
  "zoom": 4,
  "fitBounds": [[18, 73], [54, 135]],
  "minZoom": 2,
  "maxZoom": 8,
  "overlays": [{{
    "id": "provinces",
    "label": "省界",
    "file": "political/admin-boundaries/china-provinces.json",
    "style": {{"color": "#3b82f6", "weight": 1}},
    "visible": true
  }}],
  "terrain": true
}}"""


def find_insert(source: str) -> int | None:
    dpos = -1
    for anchor in (
        'id="deep-understanding"',
        'id="transfer-task"',
        'id="posttest"',
        'id="summary"',
    ):
        dpos = source.find(anchor)
        if dpos >= 0:
            break
    if dpos < 0:
        return None
    marker = source.rfind('<section class="slide-page"', 0, dpos)
    insert_at = marker if marker >= 0 else source.rfind("<section", 0, dpos)
    return insert_at if insert_at >= 0 else None


def inject_map(course_id: str, title: str, desc: str) -> tuple[bool, str]:
    path = ROOT / "community" / course_id / "index.html"
    source = path.read_text(encoding="utf-8")
    if "data-teachany-map" in source:
        return False, "already has map"
    insert_at = find_insert(source)
    if insert_at is None:
        return False, "no anchor"
    config = MAP_CONFIG.format(title=html.escape(title), desc=html.escape(desc))
    block = f"""
<section class="slide-page" data-page-type="content" data-tsh="区域地图">
  <section class="section" id="region-map" data-tts="region-map">
    <div class="card card-glow">
      <div class="section-header"><span class="phase-tag" data-variant="success">Map</span>
        <h2>{html.escape(title)} · 区域地图</h2></div>
      <p style="margin:0 0 12px;color:inherit;opacity:.85">点击图层切换叠加；悬停边界、点击城市标记，结合地图理解本课的空间格局。</p>
      <div class="map-host" data-teachany-map="thm-{course_id}" data-teachany-map-scope="china"
        data-teachany-map-title="{html.escape(title)} · 区域地图"><script type="application/json" data-teachany-map-config>
{config}
</script></div>
    </div>
  </section>
</section>
"""
    source = source[:insert_at] + block + "\n" + source[insert_at:]
    if "leaflet.css" not in source:
        source = source.replace("</head>", HEAD_LINKS + "</head>", 1)
    if "teachany-historical-map.js" not in source:
        source = source.replace("</body>", BODY_SCRIPTS + "</body>", 1)
    path.write_text(source, encoding="utf-8")
    return True, "map injected"


CANVAS_CSS = """
<style id="b3a-visual-css">
.b3a-visual .b3a-canvas{width:100%;max-width:560px;height:auto;background:#0b1628;border:1px solid rgba(148,163,184,.28);border-radius:12px;display:block;margin:8px auto 0}
</style>
"""

CANVAS_JS = """
<script id="b3a-visual-js">
(function(){
  function draw(cv){
    var kind=cv.getAttribute('data-kind'), ctx=cv.getContext('2d'), W=cv.width, H=cv.height;
    ctx.clearRect(0,0,W,H); ctx.font='13px sans-serif'; ctx.textAlign='center';
    ctx.fillStyle='#e5e7eb'; ctx.strokeStyle='#94a3b8'; ctx.lineWidth=2;
    if(kind==='area_units'){
      var s=140, x=40, y=40;
      ctx.strokeStyle='#38bdf8'; ctx.strokeRect(x,y,s,s);
      ctx.fillText('1 dm²', x+s/2, y-10);
      for(var i=0;i<10;i++) for(var j=0;j<10;j++){
        ctx.strokeStyle='rgba(56,189,248,.35)';
        ctx.strokeRect(x+i*s/10,y+j*s/10,s/10,s/10);
      }
      ctx.fillStyle='#e5e7eb'; ctx.fillText('= 100 个 1 cm² 小方格', x+s/2, y+s+24);
      ctx.fillStyle='#94a3b8'; ctx.fillText('相邻面积单位通常 ×100', W*0.72, H/2);
    } else if(kind==='avg_median'){
      var data=[2,3,5,8,12], xs=[];
      for(var k=0;k<data.length;k++){
        var px=80+k*90, py=H-40-data[k]*8;
        xs.push([px,py,data[k]]);
        ctx.fillStyle='#38bdf8'; ctx.fillRect(px-18,py,36,H-40-py);
        ctx.fillStyle='#e5e7eb'; ctx.fillText(String(data[k]), px, H-18);
      }
      ctx.fillStyle='#f472b6'; ctx.fillText('中位数=5（中间位置）', W/2, 28);
      ctx.fillStyle='#34d399'; ctx.fillText('平均数=6（总和/个数）', W/2, 50);
    } else if(kind==='word_problem'){
      var boxes=[['已知',80],['中间量',W/2],['所求',W-80]];
      ctx.strokeStyle='#38bdf8';
      for(var i=0;i<3;i++){
        var bx=boxes[i][1];
        ctx.strokeRect(bx-50,H/2-30,100,60);
        ctx.fillStyle='#e5e7eb'; ctx.fillText(boxes[i][0], bx, H/2+6);
      }
      ctx.strokeStyle='#f472b6';
      ctx.beginPath(); ctx.moveTo(130,H/2); ctx.lineTo(W/2-50,H/2); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(W/2+50,H/2); ctx.lineTo(W-130,H/2); ctx.stroke();
      ctx.fillStyle='#94a3b8'; ctx.fillText('分步：先求中间量，再求最终问题', W/2, H-24);
    } else if(kind==='decimal_ops'){
      ctx.fillStyle='#e5e7eb'; ctx.font='18px monospace'; ctx.textAlign='right';
      ctx.fillText('3.50', W/2+40, 70);
      ctx.fillText('+1.25', W/2+40, 100);
      ctx.beginPath(); ctx.moveTo(W/2-40,112); ctx.lineTo(W/2+50,112); ctx.strokeStyle='#38bdf8'; ctx.stroke();
      ctx.fillText('4.75', W/2+40, 140);
      ctx.font='13px sans-serif'; ctx.textAlign='center'; ctx.fillStyle='#94a3b8';
      ctx.fillText('小数点上下对齐（相同数位对齐）', W/2, H-28);
      // dots
      ctx.fillStyle='#f472b6';
      ctx.beginPath(); ctx.arc(W/2+8,64,3,0,Math.PI*2); ctx.fill();
      ctx.beginPath(); ctx.arc(W/2+8,94,3,0,Math.PI*2); ctx.fill();
      ctx.beginPath(); ctx.arc(W/2+8,134,3,0,Math.PI*2); ctx.fill();
    } else if(kind==='battery'){
      // battery outline
      ctx.strokeStyle='#38bdf8'; ctx.strokeRect(80,60,160,100);
      ctx.strokeRect(240,90,16,40);
      ctx.fillStyle='rgba(52,211,153,.25)'; ctx.fillRect(80,60,80,100);
      ctx.fillStyle='rgba(248,113,113,.25)'; ctx.fillRect(160,60,80,100);
      ctx.fillStyle='#e5e7eb'; ctx.fillText('负极', 120, 50); ctx.fillText('正极', 200, 50);
      ctx.strokeStyle='#fbbf24'; ctx.beginPath();
      ctx.moveTo(120,110); ctx.lineTo(200,110); ctx.stroke();
      ctx.fillStyle='#fbbf24'; ctx.fillText('Li⁺ 迁移', W/2-40, 150);
      ctx.fillStyle='#94a3b8'; ctx.fillText('充电：Li⁺ → 负极　放电：Li⁺ → 正极', W/2, H-24);
    }
  }
  function init(){ document.querySelectorAll('canvas.b3a-canvas').forEach(draw); }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
</script>
"""


def inject_canvas(course_id: str, cfg: dict) -> tuple[bool, str]:
    path = ROOT / "community" / course_id / "index.html"
    source = path.read_text(encoding="utf-8")
    if 'id="b3a-visual"' in source:
        return False, "already has b3a visual"
    insert_at = find_insert(source)
    if insert_at is None:
        return False, "no anchor"
    block = f"""
<section class="slide-page" data-page-type="content" data-tsh="互动可视">
  <section class="section b3a-visual" id="b3a-visual" data-tts="b3a-visual">
    <div class="card">
      <span class="phase-tag" data-variant="success">互动可视</span>
      <h2>{html.escape(cfg['title'])}</h2>
      <p>{html.escape(cfg['desc'])}</p>
      <canvas class="b3a-canvas" width="560" height="220" data-kind="{cfg['kind']}"
        role="img" aria-label="{html.escape(cfg['title'])}"></canvas>
    </div>
  </section>
</section>
"""
    source = source[:insert_at] + block + "\n" + source[insert_at:]
    if 'id="b3a-visual-css"' not in source:
        source = source.replace("</head>", CANVAS_CSS + "\n</head>", 1)
    if 'id="b3a-visual-js"' not in source:
        source = source.replace("</body>", CANVAS_JS + "\n</body>", 1)
    path.write_text(source, encoding="utf-8")
    return True, "canvas injected"


def main() -> int:
    changed = failed = 0
    for cid, (title, desc) in GEO.items():
        ok, msg = inject_map(cid, title, desc)
        print(("OK" if ok else "SKIP/FAIL"), cid, msg)
        if ok:
            changed += 1
        elif msg not in ("already has map",):
            failed += 1
    for cid, cfg in CANVAS.items():
        ok, msg = inject_canvas(cid, cfg)
        print(("OK" if ok else "SKIP/FAIL"), cid, msg)
        if ok:
            changed += 1
        elif msg not in ("already has b3a visual",):
            failed += 1
    print(f"done: changed={changed} failed={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
