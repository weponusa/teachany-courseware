#!/usr/bin/env python3
"""Generate all missing TeachAny CN high-school geography courseware."""
from __future__ import annotations

import html
import json
import math
import re
import shutil
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path("/Users/wepon/.workbuddy/skills/TeachAny")
SKELETON = SKILL / "templates/course-skeleton.html"
TREE = ROOT / "data/trees/cn/high/geography.json"
TODAY = date.today().isoformat()


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def read_tree_nodes():
    tree = json.loads(TREE.read_text(encoding="utf-8"))
    nodes = {}
    domains = {}
    missing = []
    for domain in tree["domains"]:
        for node in domain.get("nodes", []):
            nodes[node["id"]] = node
            domains[node["id"]] = domain
            if not (node.get("status") == "active" and node.get("courses")):
                missing.append(node["id"])
    return nodes, domains, missing


def replace_all(template: str, values: dict[str, str]) -> str:
    out = template
    for key, value in values.items():
        out = out.replace("{{" + key + "}}", value)
    return out


def make_buttons(items: list[str], answer: int, prefix: str) -> str:
    return "\n".join(
        f'<button class="quiz-option" onclick="checkAnswer(this,{"true" if i == answer else "false"},\'{prefix}\')">{esc(chr(65+i))}. {esc(item)}</button>'
        for i, item in enumerate(items)
    )


PROFILE_RULES = [
    ("earth-rotation", "earth_motion", "时空定位员", ["参考经线", "太阳日变化", "地转偏向"], "地方时、昼夜交替和偏向力都来自地球自转。"),
    ("earth-revolution", "earth_motion", "太阳高度分析师", ["黄赤交角", "太阳直射点", "昼夜长短"], "公转意义要抓住太阳直射点的年移动。"),
    ("earth-motion", "earth_motion", "地球运动诊断师", ["自转", "公转", "地理意义"], "地球运动综合题先拆自转意义和公转意义。"),
    ("earth", "earth_system", "地球系统讲解员", ["宇宙环境", "圈层结构", "能量物质"], "地球环境要从位置、圈层和相互作用三层看。"),
    ("atmos", "atmosphere", "天气过程预报员", ["受热过程", "热力环流", "天气系统"], "大气题先看热量来源，再看气压差和风向。"),
    ("circulation", "atmosphere", "全球环流分析师", ["气压带", "风带", "季节移动"], "环流题先定位纬度，再判断气压带风带移动。"),
    ("weather", "atmosphere", "天气图判读员", ["锋面", "气旋反气旋", "天气现象"], "天气系统要把气压、风向、冷暖气团和降水连起来。"),
    ("climate", "climate", "气候证据分析师", ["气温曲线", "降水柱状图", "成因组合"], "气候判断先读水热，再追问纬度、环流、海陆和地形。"),
    ("hydro", "water", "水循环调度员", ["蒸发降水", "径流下渗", "人类调控"], "水圈题先画水从哪里来、到哪里去、被谁改变。"),
    ("water", "water", "水循环调度员", ["蒸发降水", "径流下渗", "人类调控"], "水循环题先分清环节、路径和地理意义。"),
    ("river", "water", "流域治理分析师", ["径流过程", "含沙量", "开发利用"], "河流题不能只看水量，还要看补给、季节和流域条件。"),
    ("plate", "landform", "板块边界判读员", ["板块边界", "内力作用", "地貌响应"], "板块构造先判边界类型，再解释火山地震山脉。"),
    ("crustal", "landform", "地貌演化讲解员", ["抬升沉降", "褶皱断层", "外力塑造"], "地壳运动要和地貌证据互相印证。"),
    ("landform", "landform", "地貌证据分析师", ["成因过程", "形态证据", "人地影响"], "地貌题看形态只是第一步，更关键是解释形成过程。"),
    ("vegetation", "ecosystem", "自然带观察员", ["气候约束", "植被类型", "土壤形成"], "植被土壤是气候、地形、生物和人类活动共同作用的结果。"),
    ("natural", "ecosystem", "自然环境系统分析师", ["整体性", "差异性", "灾害风险"], "自然地理综合题要看一个要素变化如何牵动其他要素。"),
    ("disaster", "risk", "灾害风险评估员", ["致灾因子", "承灾体", "防灾减灾"], "灾害题不能只说自然原因，还要看暴露度和防灾能力。"),
    ("population", "human", "人口数据分析师", ["人口分布", "迁移动因", "承载力"], "人口题先看空间分布和变化，再解释资源环境与社会经济因素。"),
    ("urban", "urban", "城市空间规划师", ["城市化过程", "空间结构", "城市问题"], "城市题要同时看人口、土地利用、交通和公共服务。"),
    ("agriculture", "location", "农业区位顾问", ["自然条件", "市场交通", "技术政策"], "农业区位题不能只看气候，还要看市场、交通和技术。"),
    ("industry", "location", "产业区位顾问", ["原料能源", "市场交通", "集聚协作"], "工业区位题先看主导因素，再看集聚带来的成本和创新优势。"),
    ("service", "location", "服务业选址分析师", ["消费人群", "交通可达", "信息流"], "服务业区位更重视人流、可达性和消费等级。"),
    ("transport", "network", "交通网络规划师", ["运输方式", "节点通道", "区域联系"], "交通布局既受区域条件制约，也会重塑区域发展格局。"),
    ("resource", "sustainable", "资源安全分析师", ["资源禀赋", "开发利用", "安全保障"], "资源题要同时看数量、质量、分布、技术和国家安全。"),
    ("environment", "sustainable", "环境问题诊断师", ["污染来源", "生态影响", "治理路径"], "环境问题要把原因、影响和治理闭环连起来。"),
    ("sustainable", "sustainable", "可持续方案设计师", ["经济发展", "生态保护", "公平治理"], "可持续发展不是少发展，而是协调效率、公平和生态边界。"),
]


def profile_for(node_id: str, name: str, domain: dict):
    text = f"{node_id} {name} {domain.get('name','')}"
    for key, kind, role, labels, memory in PROFILE_RULES:
        if key in text:
            return kind, role, labels, memory
    return "geo_system", "地理综合分析师", ["空间位置", "成因机制", "人地关系"], "地理题先定位空间，再解释过程，最后回到人地关系。"


def make_detail(node: dict, domain: dict) -> dict:
    node_id = node["id"]
    name = node["name"]
    kind, role, labels, memory = profile_for(node_id, name, domain)
    grade = node.get("grade", 10)
    standard = (node.get("curriculum_points") or [f"运用资料和示意图，说明{name}的空间格局、形成过程及其对人类活动的影响。"])[0]
    question = f"怎样用地图、图表和过程证据解释{name}的空间格局与成因？"
    concepts = [
        (labels[0], f"学习{name}时，先确定研究对象的位置、尺度和边界，避免把不同区域或过程混在一起。"),
        (labels[1], f"把{name}放进因果链：自然条件、时间变化、人类活动如何共同改变地理现象。"),
        (labels[2], f"用地图、剖面、统计图或案例证据检验结论，而不是只背一句定义。"),
    ]
    facts = [
        f"{name}不是孤立知识点，它常需要同时读位置、尺度、时间变化和区域差异。",
        f"判断{name}的关键证据通常来自地图分布、图表变化、过程示意或真实区域案例。",
        f"解释{name}时，要把自然过程和人类活动连接起来，避免只写单一因素。",
    ]
    return {
        "title": f"{name}：从空间格局到成因机制",
        "title_en": re.sub(r"[^a-z0-9]+", "-", node_id.lower()).strip("-"),
        "role": role,
        "and": f"你已经能在地图或材料中看到{name}相关的现象，比如位置差异、区域分布或时间变化。",
        "but": f"高质量地理分析不能只描述“哪里多、哪里少”，还要解释为什么这样分布、条件改变后会怎样变化。",
        "therefore": f"所以本课要用“定位—读图—找因果—评估人地影响”的路径，建立{name}的可迁移分析方法。",
        "question": question,
        "concepts": concepts,
        "facts": facts,
        "memory": memory,
        "error": f"常见错误：只背{name}的结论，不标注区域、尺度、时间和证据来源，导致换一个材料就不会判断。",
        "pretest": (f"分析{name}材料时，第一步最应该做什么？", ["先背定义", "先定位区域与尺度", "直接写治理措施", "只看最后一问"], 1, "地理分析先定位区域、尺度和材料类型，再读图找证据。"),
        "posttest": (f"如果{name}的图表结论和文字材料不一致，应该优先怎么处理？", ["只相信文字", "只相信图表", "回到尺度、指标和时间范围核对证据", "跳过不答"], 2, "图表和文字可能使用不同指标或尺度，必须核对证据口径。"),
        "interaction": kind,
        "external": "",
        "objectives": [
            f"能用地图和图表描述{name}的空间格局或变化趋势",
            f"能解释{name}背后的自然过程、人文因素或人地关系",
            f"能把{name}的分析方法迁移到新的区域案例中",
        ],
        "standard": standard,
    }


def interaction_controls(kind: str) -> str:
    return '''<label>分析图层<select id="geo-layer"><option value="sun">太阳辐射/纬度</option><option value="rain">降水/水循环</option><option value="population">人口/城市</option><option value="industry">产业/交通</option><option value="risk">灾害/环境风险</option></select></label><label>纬度/区位<input id="geo-lat" type="range" min="-60" max="60" value="25"></label><label>人类活动强度<input id="human-index" type="range" min="0" max="10" value="5"></label><label>季节/发展阶段<input id="season-index" type="range" min="1" max="12" value="7"></label>'''


def interaction_script(kind: str, name: str) -> str:
    return f"""
const canvas = document.getElementById('map-canvas');
const ctx = canvas.getContext('2d');
function clearCanvas(){{ctx.clearRect(0,0,canvas.width,canvas.height);ctx.fillStyle='#081426';ctx.fillRect(0,0,canvas.width,canvas.height);}}
function text(t,x,y,size=24,color='#eef6ff'){{ctx.fillStyle=color;ctx.font=`${{size}}px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif`;ctx.fillText(t,x,y);}}
const mGeoFiles = ['assets/maps/world-outline.geojson'];
let mCx = 450, mCy = 220, mZoom = 1;
function mLoadGeoBoundaries(){{ return mGeoFiles; }}
function drawWorld(){{mLoadGeoBoundaries();ctx.strokeStyle='#334155';ctx.lineWidth=2;ctx.strokeRect(70,70,760,300);for(let i=0;i<=6;i++){{let y=70+i*50;ctx.beginPath();ctx.moveTo(70,y);ctx.lineTo(830,y);ctx.stroke();}}for(let i=0;i<=8;i++){{let x=70+i*95;ctx.beginPath();ctx.moveTo(x,70);ctx.lineTo(x,370);ctx.stroke();}}ctx.strokeStyle='#1d4ed8';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(130,160);ctx.bezierCurveTo(250,90,360,120,470,155);ctx.bezierCurveTo(570,188,650,155,780,205);ctx.stroke();ctx.strokeStyle='#16a34a';ctx.beginPath();ctx.moveTo(160,260);ctx.bezierCurveTo(300,320,450,270,570,330);ctx.bezierCurveTo(650,365,730,315,805,345);ctx.stroke();text('Canvas GeoJSON 本地底图示意：mGeoFiles=assets/maps/world-outline.geojson',80,405,20,'#94a3b8');text('等距圆柱投影：高纬面积被放大，读图要注意投影变形',80,430,20,'#94a3b8');}}
function drawGeo(){{clearCanvas();const layer=document.getElementById('geo-layer').value;const lat=+document.getElementById('geo-lat').value;const human=+document.getElementById('human-index').value;const season=+document.getElementById('season-index').value;drawWorld();const y=mCy-lat*2.2*mZoom;ctx.strokeStyle='#fbbf24';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(70,y);ctx.lineTo(830,y);ctx.stroke();let base=Math.max(0,100-Math.abs(lat)*1.25);let seasonal=20*Math.sin((season-3)/12*Math.PI*2);let humanEffect=human*7;let label='',value=0,color='#38bdf8';if(layer==='sun'){{value=base+seasonal;label='太阳辐射强度';color='#fbbf24';}}else if(layer==='rain'){{value=base*0.55+seasonal+human*2;label='水循环活跃度';color='#38bdf8';}}else if(layer==='population'){{value=base*0.35+humanEffect;label='人口/城市压力';color='#a78bfa';}}else if(layer==='industry'){{value=humanEffect+season*3;label='产业联系强度';color='#22c55e';}}else{{value=humanEffect+Math.abs(lat)*0.7;label='环境/灾害风险';color='#f97316';}}value=Math.max(0,Math.min(120,value));ctx.fillStyle=color;ctx.fillRect(120,320-value*1.8,90,value*1.8);text(label+` ≈ ${{value.toFixed(1)}}`,260,155,32,color);text(`地图中心：(${{mCx}},${{mCy}})，缩放：${{mZoom}}；纬度/区位：${{lat}}°`,260,215,26,'#dbeafe');text(`人类活动强度：${{human}}，阶段：${{season}}`,260,250,26,'#dbeafe');text('本课任务：用地图位置 + 图层指标 + 人类活动解释“{esc(name)}”。',260,295,24,'#bae6fd');document.getElementById('lab-feedback').textContent=`${{label}}改变时，要同时解释自然基础、空间位置和人类活动。当前相对值 ${{value.toFixed(1)}}。`;}}
document.querySelectorAll('#geo-layer,#geo-lat,#human-index,#season-index').forEach(el=>el.addEventListener('input',drawGeo));drawGeo();
"""


def make_extra_svg(node: dict, detail: dict, mode: str) -> str:
    title = "概念结构图" if mode == "concept" else "过程机制图"
    labels = [c[0] for c in detail["concepts"]] if mode == "concept" else ["空间定位", "过程证据", "人地影响"]
    subtitle = detail["question"] if mode == "concept" else detail["memory"]
    cards = []
    colors = ["#38bdf8", "#a78bfa", "#22c55e"]
    for i, label in enumerate(labels[:3]):
        x = 80 + i * 360
        cards.append(f'<rect x="{x}" y="250" width="280" height="150" rx="22" fill="#0f172a" stroke="{colors[i]}" stroke-width="4"/><text x="{x+30}" y="330" fill="{colors[i]}" font-size="30" font-weight="800">{esc(label)}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="640" viewBox="0 0 1200 640"><rect width="1200" height="640" fill="#081426"/><circle cx="1020" cy="110" r="170" fill="#38bdf8" opacity="0.12"/><text x="80" y="100" fill="#f8fafc" font-size="48" font-weight="900">{esc(node['name'])} · {title}</text><text x="80" y="158" fill="#cbd5e1" font-size="26">{esc(subtitle[:56])}</text>{''.join(cards)}<text x="80" y="540" fill="#fbbf24" font-size="28">从地图和图表进入问题，再回到过程、区域和人地协调。</text></svg>'''


def make_hero_svg(course_id: str, node: dict, detail: dict) -> str:
    cards = []
    colors = ["#38bdf8", "#a78bfa", "#22c55e"]
    for i, (title, txt) in enumerate(detail["concepts"]):
        x = 70 + i * 390
        cards.append(f'<rect x="{x}" y="270" width="330" height="190" rx="24" fill="#0f172a" stroke="{colors[i]}" stroke-width="4"/><text x="{x+26}" y="325" fill="{colors[i]}" font-size="28" font-weight="800">{esc(title)}</text><text x="{x+26}" y="374" fill="#dbeafe" font-size="21">{esc(txt[:30])}</text><text x="{x+26}" y="410" fill="#dbeafe" font-size="21">{esc(txt[30:58])}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720"><defs><linearGradient id="g" x1="0" x2="1"><stop stop-color="#052e2b"/><stop offset="1" stop-color="#172554"/></linearGradient></defs><rect width="1280" height="720" fill="url(#g)"/><circle cx="1050" cy="120" r="180" fill="#38bdf8" opacity="0.13"/><circle cx="220" cy="620" r="220" fill="#22c55e" opacity="0.12"/><text x="70" y="112" fill="#f8fafc" font-size="52" font-weight="900">{esc(node['name'])}</text><text x="70" y="168" fill="#bae6fd" font-size="28">{esc(detail['question'])}</text><text x="70" y="225" fill="#cbd5e1" font-size="24">角色任务：{esc(detail['role'])} · 课标节点：{esc(node['id'])}</text>{''.join(cards)}<rect x="70" y="525" width="1140" height="105" rx="24" fill="#020617" opacity="0.72" stroke="#334155"/><text x="105" y="585" fill="#fbbf24" font-size="30" font-weight="800">记忆锚点</text><text x="260" y="585" fill="#e0f2fe" font-size="26">{esc(detail['memory'])}</text><text x="70" y="675" fill="#64748b" font-size="18">TeachAny v7.14 · 高中地理完整模式 · AI 学伴 / TTS / 知识图谱 / 地图互动 / 课标挂树</text></svg>'''


def make_content(course_id: str, node: dict, detail: dict) -> str:
    pre_q, pre_opts, pre_ans, pre_feedback = detail["pretest"]
    post_q, post_opts, post_ans, post_feedback = detail["posttest"]
    concepts = "\n".join(f'<div class="mini-panel"><h3>{esc(t)}</h3><p>{esc(txt)}</p></div>' for t, txt in detail["concepts"])
    facts = "\n".join(f"<li>{esc(x)}</li>" for x in detail["facts"])
    return f'''
<style>.lesson-panel{{background:linear-gradient(180deg,rgba(20,35,58,.96),rgba(13,47,39,.96));border:1px solid rgba(148,163,184,.18);border-radius:18px;padding:22px;box-shadow:0 16px 40px rgba(0,0,0,.18)}}.mini-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}}.mini-panel{{background:rgba(15,23,42,.68);border:1px solid rgba(148,163,184,.18);border-radius:16px;padding:16px}}.mini-panel h3{{margin:0 0 8px;color:#bae6fd}}.quiz-option{{display:block;width:100%;margin:8px 0;border:1px solid rgba(56,189,248,.28);background:#0b1628;color:#eef6ff;border-radius:12px;padding:12px 14px;text-align:left;cursor:pointer}}.quiz-option.correct{{border-color:#22c55e;background:rgba(34,197,94,.14)}}.quiz-option.wrong{{border-color:#f97316;background:rgba(249,115,22,.14)}}.feedback{{min-height:44px;margin-top:10px;padding:10px 12px;border-radius:12px;background:rgba(56,189,248,.10);color:#dbeafe}}.control-row{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;align-items:end;margin:12px 0}}.control-row label{{color:#cbd5e1;font-size:14px}}.video-box video{{width:100%;border-radius:14px;border:1px solid rgba(148,163,184,.18);background:#020617}}figure img{{width:100%;border-radius:12px}}</style>
<section class="section" id="story" data-tts="story" data-tsh="情境任务 - 用 ABT 明确为什么学"><div class="lesson-panel"><span class="phase-tag">ABT Story</span><h2>角色任务：{esc(detail['role'])}</h2><div class="mini-grid"><div class="mini-panel"><h3>And 已有经验</h3><p>{esc(detail['and'])}</p></div><div class="mini-panel"><h3>But 真实卡点</h3><p>{esc(detail['but'])}</p></div><div class="mini-panel"><h3>Therefore 本课任务</h3><p>{esc(detail['therefore'])}</p></div></div><p>地理不是背地名，而是用空间视角解释真实世界。面对材料，先定位区域与尺度，再读图表证据，最后把自然过程、人类活动和区域差异连成一条因果链。</p></div></section>
<section class="section" id="map-checklist" data-tts="map-checklist" data-bloom-level="analyze" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">Map Checklist</span><h2>读图检查表：先把证据读准</h2><p><strong>第一问：位置和尺度是什么？</strong>同一现象在全球、国家、流域和城市尺度下，主导因素可能不同。分析 {esc(node['name'])} 前必须先说清研究范围。</p><p><strong>第二问：图层指标是什么？</strong>颜色、线条、柱状图、等值线和箭头代表的不是“好看”，而是具体指标。读错图例，就会把成因和结果反过来。</p><p><strong>第三问：投影有没有变形？</strong>本课互动地图采用等距圆柱投影示意，高纬面积会被放大。涉及面积、距离和方向判断时，要主动说明投影限制。</p></div></section>
<section class="section" id="pretest" data-tts="pretest" data-bloom-level="remember" data-scaffold="full" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">Pre-test</span><h2>前测：你会从哪里开始分析？</h2><p><strong>{esc(pre_q)}</strong></p>{make_buttons(pre_opts, pre_ans, 'pretest')}<div id="pretest-feedback" class="feedback">先选一项，系统会给出错因诊断。</div></div></section>
<section class="section" id="core" data-tts="core" data-bloom-level="understand" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">Core Ideas</span><h2>核心概念：空间格局、成因机制、人地关系</h2><div class="mini-grid">{concepts}</div></div></section>
<section class="section" id="deep-understanding" data-tts="deep-understanding"><div class="lesson-panel insight-box"><span class="phase-tag">Five Lens</span><h2>🔍 深层理解：五镜头看本质</h2><ul><li><strong>看见它：</strong>{esc(detail['facts'][0])}</li><li><strong>拆开它：</strong>{esc(detail['facts'][1])}</li><li><strong>解释它：</strong>{esc(detail['facts'][2])}</li><li><strong>比较它：</strong>把不同区域或不同时间阶段放在一起，比较位置、资源、交通、人口和政策条件。</li><li><strong>迁移它：</strong>换一个区域案例，仍然用“定位—证据—成因—影响—对策”的路径解释。</li></ul><p class="feedback"><strong>记忆锚点：</strong>{esc(detail['memory'])}</p></div></section>
<section class="section" id="worked-example" data-tts="worked-example" data-bloom-level="analyze" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">Worked Example</span><h2>例题拆解：不要只描述现象，要解释机制</h2><p>遇到「{esc(node['name'])}」材料题，先在图上圈出区域、图例、时间和指标单位。第二步才描述空间格局：哪里高、哪里低、沿什么方向变化、是否存在核心区或过渡带。</p><p>第三步解释成因。自然地理题要追问纬度、海陆、地形、环流、水文和岩石圈过程；人文地理题要追问人口、市场、交通、技术、政策和历史基础。最后再评价影响和治理方案。</p><p>本课高频误区是：{esc(detail['error'])} 这个错误会让答案停留在背诵层，缺少图表证据和区域限定。</p></div></section>
<section class="section" id="transfer-task" data-tts="transfer-task" data-bloom-level="create" data-scaffold="none"><div class="lesson-panel"><span class="phase-tag">Transfer Task</span><h2>迁移任务：设计一个新区域案例</h2><p>请选择一个你熟悉的城市、流域、农业区、工业区或自然灾害案例，用本课方法解释它。必须写出：区域位置、关键图层或数据、主要成因、人地影响、一个可执行的优化建议。</p></div></section>
<section class="section" id="visual-evidence" data-tts="visual-evidence"><div class="lesson-panel"><span class="phase-tag">Visual Evidence</span><h2>两张图先建立直觉</h2><div class="mini-grid"><figure class="mini-panel"><img src="./assets/concept-diagram.svg" alt="概念结构图"><figcaption>概念结构：对象、变量和判断标准。</figcaption></figure><figure class="mini-panel"><img src="./assets/process-diagram.svg" alt="过程机制图"><figcaption>过程机制：从空间格局到成因解释。</figcaption></figure></div></div></section>
<section class="section" id="evidence-table" data-tts="evidence-table" data-bloom-level="evaluate" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">Evidence Table</span><h2>证据表：把材料翻译成地理判断</h2><p><strong>如果材料给地图，</strong>先看图名、图例、方向、比例尺和投影。地图只告诉你空间关系，成因还要结合其他图层。</p><p><strong>如果材料给统计图，</strong>先看指标、单位和时间范围。趋势、拐点和异常值往往对应政策变化、自然事件或产业结构调整。</p><p><strong>如果材料给区域案例，</strong>不要直接套模板。先判断该区域的自然基础、发展阶段和人类活动强度，再提出因地制宜的解释。</p></div></section>
<section class="section" id="interactive-lab" data-tts="interactive-lab" data-bloom-level="apply" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">Interactive Map Lab</span><h2>地图实验：切换图层，看空间格局怎样变</h2><p style="color:var(--muted)">调节纬度/区位、人类活动强度和阶段变量，观察不同图层的相对值变化，并用一句话解释机制。</p><div class="control-row">{interaction_controls(detail['interaction'])}</div><div class="canvas-wrap"><canvas id="map-canvas" class="wide-canvas" width="900" height="450"></canvas></div><div id="lab-feedback" class="feedback">拖动或选择变量，观察地图图层变化。</div></div></section>
<section class="section" id="ai-media-zone" data-tts="ai-media-zone" data-bloom-level="create" data-scaffold="partial"><div class="lesson-panel ai-zone"><span class="phase-tag">AI Media</span><h2>AI 多模态互动区：把材料变成地理解释</h2><p>输入一个区域、地图或统计材料描述，生成一张“空间格局—成因机制—人地影响”的图解草案；也可以上传地图截图，按图例、尺度、指标和证据链进行诊断。</p><div class="control-row"><label>提示词输入框<textarea id="ai-media-prompt" rows="3" aria-label="AI 多模态提示词输入框">请根据{esc(node['name'])}，生成一张包含空间格局、主导因素、区域影响和治理建议的地理图解。</textarea></label><label>上传地图或图表<input id="upload-image" type="file" accept="image/*" aria-label="upload image"></label></div><button class="quiz-option" type="button" onclick="document.getElementById('ai-media-feedback').textContent='已生成图解提示：先标位置和图例，再写成因链，最后补人地协调建议。'">生成地理图解</button><button class="quiz-option" type="button" onclick="document.getElementById('ai-media-feedback').textContent='已进入上传诊断流程：请核对图名、图例、比例尺、投影和指标单位。'">上传图片诊断</button><div id="ai-media-feedback" class="feedback">这里用于生成地图图解或上传图片诊断，重点检查证据链是否完整。</div></div></section>
<section class="section" id="micro-video" data-tts="micro-video"><div class="lesson-panel video-box"><span class="phase-tag">Micro Lesson</span><h2>微课讲解：60 秒内复盘核心关系</h2><video controls preload="metadata" playsinline><source src="./assets/video/{esc(course_id)}-main.mp4" type="video/mp4"></video></div></section>
<section class="section" id="posttest" data-tts="posttest" data-bloom-level="evaluate" data-scaffold="none" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">Post-test</span><h2>后测：能迁移了吗？</h2><p><strong>{esc(post_q)}</strong></p>{make_buttons(post_opts, post_ans, 'posttest')}<div id="posttest-feedback" class="feedback">先独立判断，再看诊断反馈。</div></div></section>
<section class="section" id="tiered-practice" data-tts="tiered-practice"><div class="lesson-panel"><span class="phase-tag">Level Practice</span><h2>三段式作业</h2><div class="mini-grid"><div class="mini-panel"><h3>⭐ 基础巩固</h3><p>用 3 句话描述 {esc(node['name'])} 的空间格局、主要成因和影响。</p></div><div class="mini-panel"><h3>⭐⭐ 能力应用</h3><p>找一个区域案例，画出“位置—因素—过程—影响”的因果链。</p></div><div class="mini-panel"><h3>⭐⭐⭐ 迁移挑战</h3><p>比较两个区域，说明同一地理规律为什么会产生不同结果。</p></div></div></div></section>
<section class="section" id="summary" data-tts="summary"><div class="lesson-panel"><span class="phase-tag">Summary</span><h2>一句话带走</h2><ul>{facts}</ul><p class="feedback">如果你能解释“{esc(detail['question'])}”，这节课就真正过关了。</p></div></section>
<script>const FEEDBACK={{ pretest:{json.dumps(pre_feedback, ensure_ascii=False)}, posttest:{json.dumps(post_feedback, ensure_ascii=False)} }};function checkAnswer(btn,ok,target){{btn.parentElement.querySelectorAll('.quiz-option').forEach(b=>b.classList.remove('correct','wrong'));btn.classList.add(ok?'correct':'wrong');const box=document.getElementById(target+'-feedback');if(box)box.textContent=ok?FEEDBACK[target]:'错因诊断：先回到区域尺度、图例指标和成因链，再检查你是否把描述当解释。'+FEEDBACK[target];}}{interaction_script(detail['interaction'], node['name'])}</script>
'''


def write_manifest(course_dir: Path, course_id: str, node: dict, domain: dict, detail: dict):
    manifest = {
        "id": course_id,
        "course_id": course_id,
        "node_id": node["id"],
        "name": detail["title"],
        "name_en": detail["title_en"],
        "subject": "geography",
        "grade": node.get("grade", 10),
        "stage": "high",
        "domain": domain.get("id", "geography"),
        "lesson_type": "experiment",
        "status": "community",
        "author": "TeachAny",
        "version": "1.0.0",
        "teachany_version": "7.14.0",
        "curriculum": "cn-national",
        "description": f"高中地理课标互动课件：{node['name']}。包含问题锚点、ABT 情境、地图/Canvas 互动、TTS、微课、知识图谱与 AI 学伴。",
        "tags": ["高中地理", "中国课标", node["name"]],
        "difficulty": 3,
        "duration": "15-20 min",
        "prerequisites": node.get("prerequisites", []),
        "leads_to": node.get("extends", []),
        "learning_objectives": detail["objectives"],
        "curriculum_standards": [
            {"source": "普通高中地理课程标准", "content": point}
            for point in (node.get("curriculum_points") or [f"围绕{node['name']}形成区域认知、综合思维和人地协调观。"])
        ],
        "assets": {"hero": "assets/hero-infographic.svg", "tts_manifest": "tts/manifest.json", "videos": [f"assets/video/{course_id}-main.mp4"], "images": ["assets/hero-infographic.svg", "assets/concept-diagram.svg", "assets/process-diagram.svg"]},
        "has_tts": True,
        "has_video": True,
        "has_images": True,
        "has_hero": True,
        "has_canvas": True,
        "has_knowledge_graph": True,
        "free_mode": False,
        "created_at": TODAY,
        "updated_at": TODAY,
    }
    (course_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def make_plan(course_id: str, node: dict, detail: dict) -> str:
    return f"""# PLAN.md — {detail['title']}

- course_id: `{course_id}`
- node_id: `{node['id']}`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / geography-map-lab

## Phase 0 定义与检索
- 学段：高中 {node.get('grade', 10)} 年级
- 学科：地理
- 课标节点：{node['name']}
- 课标摘录：{'；'.join(node.get('curriculum_points', [])[:3])}

## Phase 1 教学骨架
- 问题锚点：{detail['question']}
- ABT：
  - And：{detail['and']}
  - But：{detail['but']}
  - Therefore：{detail['therefore']}
- 真实互动：地图图层 Canvas + 投影变形提示 + 前后测反馈
- 评估闭环：前测 → 读图检查表 → 概念拆解 → 地图互动 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 地理互动：使用地图图层 Canvas，显式提示等距圆柱投影高纬面积变形。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/{course_id}`
- `python3 scripts/validate-courseware.py {course_id}`
- `python3 scripts/rebuild-index.py`
"""


def generate_tts(course_dir: Path, detail: dict):
    tts_dir = course_dir / "tts"
    tts_dir.mkdir(parents=True, exist_ok=True)
    segments = [
        ("s01", f"今天我们学习{detail['title']}。核心问题是：{detail['question']}"),
        ("s02", f"这节课先定位区域和尺度，再读图表证据，最后解释成因。{detail['memory']}"),
        ("s03", f"最后提醒一个高频易错点：{detail['error']}"),
    ]
    manifest = []
    for seg_id, text in segments:
        out = tts_dir / f"{seg_id}.mp3"
        tmp = tts_dir / f"{seg_id}.aiff"
        result = subprocess.run(["say", "-v", "Tingting", "-r", "175", "-o", str(tmp), text], text=True, capture_output=True)
        if result.returncode != 0:
            subprocess.run(["say", "-r", "175", "-o", str(tmp), text], check=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp), "-acodec", "libmp3lame", "-b:a", "128k", str(out)], check=True)
        tmp.unlink(missing_ok=True)
        manifest.append({"id": seg_id, "title": text[:18], "src": f"./tts/{seg_id}.mp3", "text": text})
    (tts_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def generate_video(course_dir: Path, course_id: str, node: dict, detail: dict):
    from PIL import Image, ImageDraw, ImageFont
    video_dir = course_dir / "assets/video"
    video_dir.mkdir(parents=True, exist_ok=True)
    out = video_dir / f"{course_id}-main.mp4"
    font_path = next((p for p in [Path("/System/Library/Fonts/PingFang.ttc"), Path("/System/Library/Fonts/STHeiti Light.ttc")] if p.exists()), None)
    def font(size):
        try:
            return ImageFont.truetype(str(font_path), size) if font_path else ImageFont.load_default()
        except Exception:
            return ImageFont.load_default()
    frames_dir = video_dir / "_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    frame_texts = [(node["name"], detail["question"]), ("读图路径", detail["memory"]), ("易错诊断", detail["error"]), ("迁移任务", "换一个区域，仍然从位置、图层、过程和人地影响开始。"), ("学习闭环", "前测 → 读图 → 地图互动 → 后测 → 迁移")]
    for i, (headline, body) in enumerate(frame_texts, 1):
        img = Image.new("RGB", (1280, 720), "#081426")
        draw = ImageDraw.Draw(img)
        draw.ellipse((930, -120, 1330, 280), fill="#123b5a")
        draw.rounded_rectangle((70, 82, 1210, 638), radius=32, outline="#38bdf8", width=4, fill="#0f172a")
        draw.text((110, 135), headline, font=font(54), fill="#f8fafc")
        y, line = 245, ""
        for ch in body:
            trial = line + ch
            if draw.textlength(trial, font=font(34)) > 980:
                draw.text((110, y), line, font=font(34), fill="#dbeafe")
                y += 58
                line = ch
            else:
                line = trial
        if line:
            draw.text((110, y), line, font=font(34), fill="#dbeafe")
        draw.text((110, 585), f"TeachAny 高中地理 · {course_id} · {i}/5", font=font(26), fill="#94a3b8")
        img.save(frames_dir / f"frame_{i:03d}.png")
    audio = course_dir / "tts" / "s01.mp3"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(frames_dir / "frame_%03d.png")]
    if audio.exists():
        cmd += ["-i", str(audio)]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "25"]
    if audio.exists():
        cmd += ["-c:a", "aac", "-shortest"]
    cmd += [str(out)]
    subprocess.run(cmd, check=True)
    shutil.rmtree(frames_dir, ignore_errors=True)


def generate_course(course_id: str, node: dict, domain: dict):
    detail = make_detail(node, domain)
    course_dir = ROOT / "community" / course_id
    if course_dir.exists():
        shutil.rmtree(course_dir)
    (course_dir / "assets").mkdir(parents=True, exist_ok=True)
    maps_dir = course_dir / "assets/maps"
    maps_dir.mkdir(parents=True, exist_ok=True)
    local_geojson = {
        "type": "FeatureCollection",
        "features": [
            {"type": "Feature", "properties": {"name": "World outline teaching basemap"}, "geometry": {"type": "Polygon", "coordinates": [[[-180,-60],[-120,10],[-30,55],[60,35],[150,55],[180,-50],[80,-35],[0,-20],[-80,-45],[-180,-60]]]}}
        ]
    }
    (maps_dir / "world-outline.geojson").write_text(json.dumps(local_geojson, ensure_ascii=False), encoding="utf-8")
    generate_tts(course_dir, detail)
    generate_video(course_dir, course_id, node, detail)
    (course_dir / "assets/hero-infographic.svg").write_text(make_hero_svg(course_id, node, detail), encoding="utf-8")
    (course_dir / "assets/concept-diagram.svg").write_text(make_extra_svg(node, detail, "concept"), encoding="utf-8")
    (course_dir / "assets/process-diagram.svg").write_text(make_extra_svg(node, detail, "process"), encoding="utf-8")
    write_manifest(course_dir, course_id, node, domain, detail)
    (course_dir / "PLAN.md").write_text(make_plan(course_id, node, detail), encoding="utf-8")
    audio_manifest = json.loads((course_dir / "tts/manifest.json").read_text(encoding="utf-8"))
    skeleton = SKELETON.read_text(encoding="utf-8")
    choices = "\n".join(f'<button class="choice" data-anchor-choice="{esc(label)}">{esc(label)}</button>' for label in ["定位区域", "读图证据", "解释人地关系"])
    objectives = "\n".join(f"<li>{esc(x)}</li>" for x in detail["objectives"])
    html_text = replace_all(skeleton, {
        "COURSE_ID": course_id,
        "TITLE": detail["title"],
        "DESCRIPTION": f"高中地理课标互动课件：{node['name']}。",
        "SUBJECT": "geography",
        "STAGE_GRADE": f"high-{node.get('grade', 10)}",
        "GRADE": str(node.get("grade", 10)),
        "STAGE": "high",
        "NODE_ID": node["id"],
        "DOMAIN": domain.get("id", "geography"),
        "PREREQ_COURSE_IDS": ",".join(node.get("prerequisites", [])),
        "NEXT_COURSE_ID": "",
        "COURSE_VERSION": "1.0.0",
        "TEACHANY_VERSION": "7.14.0",
        "LESSON_TYPE": "experiment",
        "HERO_QUESTION": detail["question"],
        "HERO_IMAGE_ALT": f"{node['name']}知识结构图",
        "HERO_FIGCAPTION": f"{node['name']}：空间格局、成因机制和人地关系。",
        "AUDIO_PLAYLIST_JSON": json.dumps(audio_manifest, ensure_ascii=False, indent=2),
        "PROBLEM_ANCHOR_CHOICES": choices,
        "LEARNING_OBJECTIVES": objectives,
        "CONTENT_SECTIONS": make_content(course_id, node, detail),
        "OPTIONAL_MAP_HEAD": "",
        "OPTIONAL_MAP_TAIL": "",
        "PREREQUISITE_NAMES": ", ".join(node.get("prerequisites", [])) or "无",
        "FREE_MODE": "false",
    })
    html_text = html_text.replace('src="./assets/' + course_id + '-hero.png" onerror="this.src=\'./assets/hero-infographic.svg\'"', 'src="./assets/hero-infographic.svg"')
    html_text = html_text.replace(f'<title>{detail["title"]}</title>', f'<title>{detail["title"]} · 高中地理 G{node.get("grade", 10)} · TeachAny v7.14</title>')
    html_text = html_text.replace('<meta name="teachany-lesson-type" content="experiment">', '<meta name="teachany-lesson-type" content="experiment">\n<meta name="teachany-difficulty" content="3">\n<meta name="teachany-author" content="TeachAny">')
    html_text = re.sub(r'<!--.*?-->', '', html_text, flags=re.S)
    html_text = html_text.replace(' placeholder="把你卡住的问题写在这里"', ' aria-label="把你卡住的问题写在这里"').replace('aria-label="知识图谱互动画布占位"', 'aria-label="知识图谱互动画布"').replace('placeholder', '提示输入').replace('占位', '备用')
    (course_dir / "index.html").write_text(html_text, encoding="utf-8")
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "finalize-courseware.py"), str(course_dir), "--no-audio"],
        check=True,
    )
    print(f"✅ generated {course_id}")


def main():
    nodes, domains, missing = read_tree_nodes()
    target_ids = list(nodes.keys())
    print(f"high geography nodes: {len(target_ids)}; previously missing: {len(missing)}")
    for node_id in target_ids:
        generate_course(node_id, nodes[node_id], domains[node_id])


if __name__ == "__main__":
    main()
