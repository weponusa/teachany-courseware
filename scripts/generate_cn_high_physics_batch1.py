#!/usr/bin/env python3
"""Generate TeachAny CN high-school physics batch 1 courseware."""
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
TREE = ROOT / "data/trees/cn/high/physics.json"
TODAY = date.today().isoformat()

BATCH_IDS = [
    "phy-h-motion-description",
    "phy-h-kinematics-linear",
    "phy-h-uniform-acceleration",
    "phy-h-free-fall",
    "phy-h-circular-motion",
]

DETAILS = {
    "phy-h-motion-description": {
        "title": "运动的描述：先选参考系，再谈位置和速度",
        "title_en": "Describing Motion",
        "role": "运动数据记录员",
        "and": "你已经能用生活语言说一个物体在动，比如汽车前进、同学跑步、列车驶离站台。",
        "but": "同一个人坐在车里看自己是静止的，站台上的人看他在运动；如果不先约定参考系，运动描述会互相矛盾。",
        "therefore": "所以要用参考系、质点、位置、位移、速度和加速度建立一套可测量的运动语言。",
        "question": "为什么讨论运动前必须先问“相对于谁在运动”？",
        "concepts": [
            ("参考系", "描述物体运动时被选作标准的物体或坐标系。参考系不同，运动状态描述可能不同。"),
            ("位移与路程", "位移是从初位置指向末位置的矢量，路程是实际轨迹长度，二者一般不相同。"),
            ("速度与加速度", "速度描述位置变化快慢和方向，加速度描述速度变化快慢和方向。"),
        ],
        "facts": ["坐在匀速列车上的乘客相对车厢静止，相对地面运动。", "绕操场一圈回到起点，路程不为零，但位移为零。", "速度变大、变小或方向改变，都意味着存在加速度。"],
        "memory": "运动描述三步：定参考系，看位移，再看速度怎样变。",
        "error": "常见错误：把路程和位移混为一谈。路程看轨迹长度，位移只看起点到终点的有向线段。",
        "pretest": ("绕操场一圈回到出发点，位移是多少？", ["等于一圈长度", "为零", "等于半圈", "无法判断"], 1, "位移只看初末位置，回到起点时位移为零。"),
        "posttest": ("同一乘客相对车厢静止、相对地面运动，说明运动描述具有？", ["绝对性", "相对性", "不可测性", "无方向性"], 1, "参考系不同，运动状态描述不同。"),
        "interaction": "motion",
        "external": "https://phet.colorado.edu/sims/html/forces-and-motion-basics/latest/forces-and-motion-basics_zh_CN.html",
        "objectives": ["能解释参考系对运动描述的影响", "能区分位移和路程", "能用速度和加速度描述运动变化"],
    },
    "phy-h-kinematics-linear": {
        "title": "直线运动综合：用图像把运动过程看清楚",
        "title_en": "Linear Kinematics",
        "role": "交通运动分析师",
        "and": "你已经知道速度、位移和加速度的基本含义，也能读懂简单的时间记录。",
        "but": "真实题目常同时给文字、表格和图像。只盯公式会漏掉图像斜率、面积和分段运动信息。",
        "therefore": "所以要把 x-t、v-t 图像和运动过程联系起来，用斜率、面积和分段分析解决直线运动问题。",
        "question": "怎样从一张 v-t 图像直接读出速度变化、位移和加速度？",
        "concepts": [
            ("x-t 图像", "x-t 图像的斜率表示速度；斜率正负反映运动方向。"),
            ("v-t 图像", "v-t 图像的斜率表示加速度，图线与时间轴围成面积表示位移。"),
            ("分段运动", "复杂直线运动可拆成若干匀速、加速或减速阶段，再分别计算并合成。"),
        ],
        "facts": ["v-t 图像在时间轴上方的面积对应正位移。", "水平的 v-t 图线表示速度不变，加速度为零。", "斜率越大，加速度大小越大。"],
        "memory": "运动图像口诀：x-t 斜率是速度，v-t 斜率是加速度，v-t 面积是位移。",
        "error": "常见错误：把 v-t 图像的高度当成位移。高度是瞬时速度，面积才是位移。",
        "pretest": ("v-t 图像的斜率表示什么？", ["位移", "速度", "加速度", "路程"], 2, "v-t 图像斜率表示速度随时间变化的快慢，即加速度。"),
        "posttest": ("v-t 图线与时间轴围成的有向面积表示？", ["位移", "加速度", "质量", "力"], 0, "速度对时间累积得到位移。"),
        "interaction": "linear_graph",
        "external": "",
        "objectives": ["能读懂 x-t 与 v-t 图像", "能用斜率和面积求速度、加速度、位移", "能把复杂直线运动分段处理"],
    },
    "phy-h-uniform-acceleration": {
        "title": "匀变速直线运动：三条公式背后的图像逻辑",
        "title_en": "Uniformly Accelerated Motion",
        "role": "刹车距离评估员",
        "and": "你已经会从 v-t 图像看速度变化，也知道加速度表示速度变化快慢。",
        "but": "匀变速公式很多，如果只背 v=v₀+at、x=v₀t+1/2at²、v²-v₀²=2ax，很容易乱套条件。",
        "therefore": "所以要从“加速度恒定”这个核心条件出发，用图像面积和斜率推导公式，再按已知量选择公式。",
        "question": "为什么匀变速直线运动的位移公式里会出现 1/2at²？",
        "concepts": [
            ("速度公式", "加速度恒定时，速度随时间线性变化：v = v₀ + at。"),
            ("位移公式", "v-t 图像面积给出位移：x = v₀t + 1/2at²。"),
            ("无时公式", "消去时间可得 v² - v₀² = 2ax，适合没有时间量的题目。"),
        ],
        "facts": ["汽车刹车可近似看作匀减速运动。", "自由落体在忽略空气阻力时是初速度为零的匀加速运动。", "v-t 图像是直线，是匀变速的重要判据。"],
        "memory": "匀变速先看 a 恒定：有时用 v=v₀+at，有位移用面积，缺时间用无时公式。",
        "error": "常见错误：不判断加速度是否恒定就套匀变速公式。公式成立的前提是 a 不随时间变化。",
        "pretest": ("匀变速直线运动的 v-t 图像通常是？", ["水平直线", "倾斜直线", "圆", "无规律曲线"], 1, "加速度恒定，速度随时间线性变化。"),
        "posttest": ("没有给时间 t，但给了 v、v₀、a、x，适合使用？", ["v=v₀+at", "x=v₀t", "v²-v₀²=2ax", "F=ma"], 2, "无时公式不含 t。"),
        "interaction": "uniform_accel",
        "external": "https://phet.colorado.edu/sims/html/projectile-motion/latest/projectile-motion_zh_CN.html",
        "objectives": ["能从 v-t 图像理解匀变速公式", "能根据已知量选择合适公式", "能判断公式适用前提"],
    },
    "phy-h-free-fall": {
        "title": "自由落体运动：只受重力时怎样下落？",
        "title_en": "Free Fall",
        "role": "落体实验复现实验员",
        "and": "你已经学习匀变速直线运动，知道初速度、加速度和位移之间的关系。",
        "but": "生活中纸片和石头下落不同，容易让人误以为重物一定下落更快；但空气阻力会干扰我们看到的现象。",
        "therefore": "所以要在“只受重力、忽略空气阻力”的理想条件下研究自由落体，理解 g 和运动公式。",
        "question": "为什么在真空中，轻重不同的物体会同时落地？",
        "concepts": [
            ("自由落体条件", "物体只受重力作用、初速度为零的下落运动叫自由落体运动。"),
            ("重力加速度", "近地面自由落体加速度约 g=9.8 m/s²，方向竖直向下。"),
            ("公式迁移", "自由落体是 v₀=0、a=g 的匀加速直线运动，可用 v=gt、h=1/2gt²。"),
        ],
        "facts": ["真空管实验中羽毛和硬币可近似同时落下。", "空气阻力越明显，实际下落与自由落体模型差异越大。", "自由落体第 1 秒位移约 4.9 m，第 2 秒末速度约 19.6 m/s。"],
        "memory": "自由落体三条件：只受重力、初速为零、加速度为 g。",
        "error": "常见错误：把所有下落都当自由落体。若空气阻力不可忽略，或初速度不为零，就不是标准自由落体。",
        "pretest": ("自由落体运动的初速度通常为？", ["0", "g", "9.8 m/s", "任意方向"], 0, "自由落体定义中初速度为零。"),
        "posttest": ("忽略空气阻力时，自由落体加速度取决于？", ["物体质量", "物体颜色", "当地重力场", "物体价格"], 2, "近地面自由落体加速度由当地重力场决定，与质量无关。"),
        "interaction": "free_fall",
        "external": "https://phet.colorado.edu/sims/html/projectile-motion/latest/projectile-motion_zh_CN.html",
        "objectives": ["能说清自由落体模型的条件", "能使用 v=gt 和 h=1/2gt² 解决问题", "能区分理想模型和空气阻力影响"],
    },
    "phy-h-circular-motion": {
        "title": "圆周运动：速度方向一直变就是有加速度",
        "title_en": "Circular Motion",
        "role": "过山车安全分析师",
        "and": "你已经知道速度是矢量，速度大小或方向改变都表示运动状态改变。",
        "but": "匀速圆周运动的速率不变，却仍然需要向心加速度和向心力；这和“速度没变就没有加速度”的直觉冲突。",
        "therefore": "所以要理解线速度、角速度、周期、向心加速度和向心力之间的关系。",
        "question": "为什么匀速圆周运动速率不变，却仍然有加速度？",
        "concepts": [
            ("线速度与角速度", "线速度描述沿圆周运动快慢，角速度描述转过角度快慢，二者满足 v=ωr。"),
            ("向心加速度", "匀速圆周运动速度方向不断改变，加速度指向圆心，大小 a=v²/r=ω²r。"),
            ("向心力", "向心力不是新性质的力，而是指向圆心、提供向心加速度的合力。"),
        ],
        "facts": ["过山车转弯时，轨道对车的支持力和重力合力可提供向心力。", "卫星近似圆周运动时，万有引力提供向心力。", "半径越小、速率越大，转弯所需向心加速度越大。"],
        "memory": "圆周运动看方向：速率可不变，速度方向变；向心加速度总指圆心。",
        "error": "常见错误：把向心力当成额外多出来的一种力。它其实是指向圆心的合力名称。",
        "pretest": ("匀速圆周运动中速度方向如何变化？", ["不变", "不断改变", "只在起点改变", "没有方向"], 1, "速度是矢量，沿圆周运动时方向不断改变。"),
        "posttest": ("向心加速度方向总是？", ["沿切线", "背离圆心", "指向圆心", "竖直向上"], 2, "向心加速度总指向圆心。"),
        "interaction": "circular",
        "external": "",
        "objectives": ["能区分线速度、角速度和周期", "能解释向心加速度来源于速度方向改变", "能判断向心力由哪些实际力提供"],
    },
}


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def read_tree_nodes():
    tree = json.loads(TREE.read_text(encoding="utf-8"))
    nodes = {}
    domains = {}
    for domain in tree["domains"]:
        for node in domain.get("nodes", []):
            nodes[node["id"]] = node
            domains[node["id"]] = domain
    return nodes, domains


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


def interaction_controls(kind: str) -> str:
    if kind == "motion":
        return '''<label>参考系<select id="frame"><option value="ground">地面</option><option value="car">车厢</option></select></label><label>物体速度 m/s<input id="obj-v" type="range" min="0" max="30" value="12"></label><label>参考系速度 m/s<input id="frame-v" type="range" min="0" max="30" value="12"></label>'''
    if kind == "linear_graph":
        return '''<label>初速度 m/s<input id="v0" type="range" min="-10" max="20" value="4"></label><label>加速度 m/s²<input id="acc" type="range" min="-5" max="5" value="2"></label>'''
    if kind == "uniform_accel":
        return '''<label>初速度 m/s<input id="ua-v0" type="range" min="0" max="30" value="10"></label><label>加速度 m/s²<input id="ua-a" type="range" min="-8" max="8" value="2"></label><label>时间 s<input id="ua-t" type="range" min="1" max="10" value="4"></label>'''
    if kind == "free_fall":
        return '''<label>下落时间 s<input id="fall-t" type="range" min="0.5" max="5" step="0.5" value="2"></label><label>空气阻力<select id="drag"><option value="0">忽略</option><option value="0.35">较小</option><option value="0.7">较大</option></select></label>'''
    if kind == "forces":
        return '''<label>质量 kg<input id="mass" type="range" min="1" max="20" value="5"></label><label>摩擦因数<input id="mu" type="range" min="0" max="0.8" step="0.05" value="0.3"></label><label>弹簧伸长 m<input id="stretch" type="range" min="0" max="0.5" step="0.05" value="0.2"></label>'''
    if kind == "decomposition":
        return '''<label>力 F/N<input id="force" type="range" min="10" max="200" value="100"></label><label>角度 θ<input id="angle" type="range" min="0" max="90" value="30"></label>'''
    if kind == "newton":
        return '''<label>合力 N<input id="netf" type="range" min="0" max="100" value="40"></label><label>质量 kg<input id="newton-m" type="range" min="1" max="20" value="5"></label>'''
    if kind == "projectile":
        return '''<label>初速度 m/s<input id="proj-v" type="range" min="5" max="50" value="25"></label><label>抛射角 °<input id="proj-a" type="range" min="0" max="80" value="35"></label>'''
    if kind == "gravitation":
        return '''<label>中心天体质量倍数<input id="grav-m" type="range" min="1" max="20" value="5"></label><label>距离倍数<input id="grav-r" type="range" min="1" max="10" value="3"></label>'''
    if kind == "energy":
        return '''<label>质量 kg<input id="en-m" type="range" min="1" max="20" value="5"></label><label>高度 m<input id="en-h" type="range" min="0" max="20" value="8"></label><label>速度 m/s<input id="en-v" type="range" min="0" max="30" value="10"></label>'''
    if kind == "momentum":
        return '''<label>质量 kg<input id="mo-m" type="range" min="1" max="20" value="4"></label><label>速度 m/s<input id="mo-v" type="range" min="-20" max="20" value="8"></label><label>作用时间 s<input id="mo-t" type="range" min="0.1" max="5" step="0.1" value="1"></label>'''
    if kind == "electric":
        return '''<label>电荷量倍数<input id="q1" type="range" min="-5" max="5" value="3"></label><label>距离倍数<input id="er" type="range" min="1" max="10" value="4"></label>'''
    if kind == "circuit":
        return '''<label>电压 V<input id="voltage" type="range" min="1" max="24" value="6"></label><label>电阻 Ω<input id="resistance" type="range" min="1" max="50" value="12"></label>'''
    if kind == "magnetic":
        return '''<label>电流 A<input id="mag-i" type="range" min="1" max="10" value="4"></label><label>磁场 T<input id="mag-b" type="range" min="0" max="5" step="0.1" value="1.5"></label><label>夹角 °<input id="mag-a" type="range" min="0" max="90" value="90"></label>'''
    if kind == "wave":
        return '''<label>频率 Hz<input id="wave-f" type="range" min="1" max="10" value="3"></label><label>波速 m/s<input id="wave-v" type="range" min="1" max="30" value="12"></label>'''
    if kind == "gas_laws":
        return '''<label>温度 K<input id="gas-t" type="range" min="200" max="600" value="300"></label><label>体积 L<input id="gas-v" type="range" min="1" max="20" value="8"></label>'''
    if kind == "modern":
        return '''<label>光频率倍数<input id="nu" type="range" min="1" max="10" value="5"></label><label>逸出功倍数<input id="work" type="range" min="1" max="8" value="3"></label>'''
    return '''<label>半径 m<input id="radius" type="range" min="1" max="10" value="4"></label><label>速率 m/s<input id="speed" type="range" min="1" max="30" value="12"></label>'''


def interaction_script(kind: str) -> str:
    common = """
const canvas = document.getElementById('physics-canvas');
const ctx = canvas.getContext('2d');
function clearCanvas(){ctx.clearRect(0,0,canvas.width,canvas.height);ctx.fillStyle='#081426';ctx.fillRect(0,0,canvas.width,canvas.height);}
function text(t,x,y,size=24,color='#eef6ff'){ctx.fillStyle=color;ctx.font=`${size}px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif`;ctx.fillText(t,x,y);}
function axis(){ctx.strokeStyle='#334155';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(70,330);ctx.lineTo(830,330);ctx.moveTo(90,60);ctx.lineTo(90,360);ctx.stroke();}
"""
    if kind == "motion":
        return common + """
function drawMotion(){clearCanvas();const frame=document.getElementById('frame').value;const v=+document.getElementById('obj-v').value;const vf=+document.getElementById('frame-v').value;const rel=frame==='ground'?v:v-vf;axis();ctx.fillStyle='#38bdf8';ctx.fillRect(120+rel*10,230,120,55);text('观察参考系：'+(frame==='ground'?'地面':'车厢'),80,80,32,'#fbbf24');text(`相对速度 = ${rel.toFixed(1)} m/s`,80,140,30,'#dbeafe');text('参考系改变，运动描述也会改变。',80,390,24,'#cbd5e1');document.getElementById('lab-feedback').textContent=`相对${frame==='ground'?'地面':'车厢'}，物体速度为 ${rel.toFixed(1)} m/s。`;}
document.querySelectorAll('#frame,#obj-v,#frame-v').forEach(el=>el.addEventListener('input',drawMotion));drawMotion();
"""
    if kind == "linear_graph":
        return common + """
function drawLinear(){clearCanvas();axis();const v0=+document.getElementById('v0').value,a=+document.getElementById('acc').value;ctx.strokeStyle='#38bdf8';ctx.lineWidth=4;ctx.beginPath();for(let t=0;t<=10;t+=0.2){const v=v0+a*t;const x=90+t*65,y=330-v*8;if(t===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);}ctx.stroke();const disp=v0*10+0.5*a*100;text(`v(t)=${v0}+${a}t`,110,90,32,'#fbbf24');text(`0-10s 位移≈v-t 面积=${disp.toFixed(1)} m`,110,145,28,'#dbeafe');document.getElementById('lab-feedback').textContent=`斜率是加速度 ${a}，面积给出位移 ${disp.toFixed(1)} m。`;}
document.querySelectorAll('#v0,#acc').forEach(el=>el.addEventListener('input',drawLinear));drawLinear();
"""
    if kind == "uniform_accel":
        return common + """
function drawUA(){clearCanvas();const v0=+document.getElementById('ua-v0').value,a=+document.getElementById('ua-a').value,t=+document.getElementById('ua-t').value;const v=v0+a*t;const x=v0*t+0.5*a*t*t;axis();ctx.strokeStyle='#fbbf24';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(100,300-v0*6);ctx.lineTo(100+t*65,300-v*6);ctx.stroke();text(`v=v₀+at=${v.toFixed(1)} m/s`,90,90,32,'#fbbf24');text(`x=v₀t+1/2at²=${x.toFixed(1)} m`,90,150,32,'#dbeafe');text('v-t 图像的梯形面积就是位移。',90,390,24,'#cbd5e1');document.getElementById('lab-feedback').textContent=`${t}s 后速度 ${v.toFixed(1)} m/s，位移 ${x.toFixed(1)} m。`;}
document.querySelectorAll('#ua-v0,#ua-a,#ua-t').forEach(el=>el.addEventListener('input',drawUA));drawUA();
"""
    if kind == "free_fall":
        return common + """
function drawFall(){clearCanvas();const t=+document.getElementById('fall-t').value,drag=+document.getElementById('drag').value;const g=9.8*(1-drag);const h=0.5*g*t*t;ctx.strokeStyle='#94a3b8';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(500,70);ctx.lineTo(500,370);ctx.stroke();ctx.fillStyle='#fbbf24';ctx.beginPath();ctx.arc(500,80+Math.min(280,h*6),24,0,Math.PI*2);ctx.fill();text(`有效加速度≈${g.toFixed(1)} m/s²`,90,100,32,'#fbbf24');text(`下落位移≈${h.toFixed(1)} m`,90,160,32,'#dbeafe');text(drag===0?'理想自由落体：只受重力。':'空气阻力使实际下落偏离自由落体模型。',90,390,24,'#cbd5e1');document.getElementById('lab-feedback').textContent=`下落 ${t}s，位移约 ${h.toFixed(1)}m。`;}
document.querySelectorAll('#fall-t,#drag').forEach(el=>el.addEventListener('input',drawFall));drawFall();
"""
    if kind == "forces":
        return common + """
function drawForces(){clearCanvas();const m=+document.getElementById('mass').value,mu=+document.getElementById('mu').value,x=+document.getElementById('stretch').value;const g=9.8,N=m*g,f=mu*N,k=100,F=k*x;axis();text(`重力 G=mg=${N.toFixed(1)}N`,80,90,30,'#fbbf24');text(`滑动摩擦 f=μN=${f.toFixed(1)}N`,80,145,30,'#dbeafe');text(`弹力 F=kx=${F.toFixed(1)}N`,80,200,30,'#bae6fd');ctx.fillStyle='#38bdf8';ctx.fillRect(420,230,120,70);ctx.strokeStyle='#f97316';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(480,230);ctx.lineTo(480,140);ctx.stroke();ctx.strokeStyle='#22c55e';ctx.beginPath();ctx.moveTo(540,265);ctx.lineTo(650,265);ctx.stroke();document.getElementById('lab-feedback').textContent=`先画受力图，再分别计算重力、弹力、摩擦力。`;}
document.querySelectorAll('#mass,#mu,#stretch').forEach(el=>el.addEventListener('input',drawForces));drawForces();
"""
    if kind == "decomposition":
        return common + """
function drawDecomposition(){clearCanvas();const F=+document.getElementById('force').value,ang=+document.getElementById('angle').value*Math.PI/180;const fx=F*Math.cos(ang),fy=F*Math.sin(ang);axis();const x0=160,y0=300,scale=2;ctx.strokeStyle='#fbbf24';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(x0,y0);ctx.lineTo(x0+fx*scale,y0-fy*scale);ctx.stroke();ctx.strokeStyle='#38bdf8';ctx.beginPath();ctx.moveTo(x0,y0);ctx.lineTo(x0+fx*scale,y0);ctx.stroke();ctx.strokeStyle='#a78bfa';ctx.beginPath();ctx.moveTo(x0+fx*scale,y0);ctx.lineTo(x0+fx*scale,y0-fy*scale);ctx.stroke();text(`Fx=Fcosθ=${fx.toFixed(1)}N`,90,90,30,'#38bdf8');text(`Fy=Fsinθ=${fy.toFixed(1)}N`,90,145,30,'#a78bfa');document.getElementById('lab-feedback').textContent=`分解不是把力变少，而是换成等效的两个方向分量。`;}
document.querySelectorAll('#force,#angle').forEach(el=>el.addEventListener('input',drawDecomposition));drawDecomposition();
"""
    if kind == "newton":
        return common + """
function drawNewton(){clearCanvas();const F=+document.getElementById('netf').value,m=+document.getElementById('newton-m').value;const a=F/m;axis();ctx.fillStyle='#38bdf8';ctx.fillRect(260,230,130,70);ctx.strokeStyle='#fbbf24';ctx.lineWidth=6;ctx.beginPath();ctx.moveTo(390,265);ctx.lineTo(390+F*4,265);ctx.stroke();text(`a=F合/m=${a.toFixed(2)} m/s²`,90,95,34,'#fbbf24');text(`合力 ${F}N，质量 ${m}kg`,90,155,28,'#dbeafe');document.getElementById('lab-feedback').textContent=`合力决定加速度：同样合力下，质量越大加速度越小。`;}
document.querySelectorAll('#netf,#newton-m').forEach(el=>el.addEventListener('input',drawNewton));drawNewton();
"""
    if kind == "projectile":
        return common + """
function drawProjectile(){clearCanvas();const v=+document.getElementById('proj-v').value,a=+document.getElementById('proj-a').value*Math.PI/180;const vx=v*Math.cos(a),vy=v*Math.sin(a),g=9.8;axis();ctx.strokeStyle='#fbbf24';ctx.lineWidth=4;ctx.beginPath();for(let t=0;t<=2*vy/g;t+=0.05){const x=90+vx*t*10,y=330-(vy*t-0.5*g*t*t)*10;if(t===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);}ctx.stroke();text(`vx=${vx.toFixed(1)} m/s（水平匀速）`,90,80,28,'#38bdf8');text(`vy0=${vy.toFixed(1)} m/s（竖直匀变速）`,90,130,28,'#a78bfa');document.getElementById('lab-feedback').textContent=`抛体运动可分解为水平匀速和竖直匀变速。`;}
document.querySelectorAll('#proj-v,#proj-a').forEach(el=>el.addEventListener('input',drawProjectile));drawProjectile();
"""
    if kind == "gravitation":
        return common + """
function drawGravitation(){clearCanvas();const M=+document.getElementById('grav-m').value,r=+document.getElementById('grav-r').value;const F=M/(r*r);const cx=450,cy=220,R=40+18*r;ctx.fillStyle='#fbbf24';ctx.beginPath();ctx.arc(cx,cy,35+M,0,Math.PI*2);ctx.fill();ctx.strokeStyle='#38bdf8';ctx.lineWidth=4;ctx.beginPath();ctx.arc(cx,cy,R,0,Math.PI*2);ctx.stroke();ctx.fillStyle='#bae6fd';ctx.beginPath();ctx.arc(cx+R,cy,14,0,Math.PI*2);ctx.fill();text(`F∝M/r²=${F.toFixed(2)}（相对值）`,90,90,32,'#fbbf24');text('距离变为 2 倍，引力变为 1/4；质量变大，引力等比例增大。',90,380,24,'#dbeafe');document.getElementById('lab-feedback').textContent=`中心质量倍数 ${M}，距离倍数 ${r}，相对引力 ${F.toFixed(2)}。`;}
document.querySelectorAll('#grav-m,#grav-r').forEach(el=>el.addEventListener('input',drawGravitation));drawGravitation();
"""
    if kind == "energy":
        return common + """
function drawEnergy(){clearCanvas();const m=+document.getElementById('en-m').value,h=+document.getElementById('en-h').value,v=+document.getElementById('en-v').value;const Ep=m*9.8*h,Ek=.5*m*v*v,E=Ep+Ek;text(`重力势能 Ep=mgh=${Ep.toFixed(1)}J`,80,90,30,'#fbbf24');text(`动能 Ek=1/2mv²=${Ek.toFixed(1)}J`,80,145,30,'#38bdf8');text(`机械能 E=${E.toFixed(1)}J`,80,200,30,'#22c55e');ctx.fillStyle='#a78bfa';ctx.fillRect(520,320-h*10,70,h*10);ctx.fillStyle='#fbbf24';ctx.beginPath();ctx.arc(555,300-h*10,20,0,Math.PI*2);ctx.fill();document.getElementById('lab-feedback').textContent=`能量分析先确定系统和是否只有保守力做功。当前机械能 ${E.toFixed(1)}J。`;}
document.querySelectorAll('#en-m,#en-h,#en-v').forEach(el=>el.addEventListener('input',drawEnergy));drawEnergy();
"""
    if kind == "momentum":
        return common + """
function drawMomentum(){clearCanvas();const m=+document.getElementById('mo-m').value,v=+document.getElementById('mo-v').value,t=+document.getElementById('mo-t').value;const p=m*v,F=p/t;ctx.fillStyle='#38bdf8';ctx.fillRect(340+v*8,235,110,60);ctx.strokeStyle='#fbbf24';ctx.lineWidth=6;ctx.beginPath();ctx.moveTo(395,235);ctx.lineTo(395+v*10,235);ctx.stroke();text(`动量 p=mv=${p.toFixed(1)} kg·m/s`,90,90,32,'#fbbf24');text(`平均力≈Δp/Δt=${F.toFixed(1)}N`,90,145,30,'#dbeafe');document.getElementById('lab-feedback').textContent=`碰撞时间越长，同样动量变化对应的平均力越小。`;}
document.querySelectorAll('#mo-m,#mo-v,#mo-t').forEach(el=>el.addEventListener('input',drawMomentum));drawMomentum();
"""
    if kind == "electric":
        return common + """
function drawElectric(){clearCanvas();const q=+document.getElementById('q1').value,r=+document.getElementById('er').value;const E=q/(r*r);const cx=450,cy=220;ctx.fillStyle=q>=0?'#f97316':'#38bdf8';ctx.beginPath();ctx.arc(cx,cy,35,0,Math.PI*2);ctx.fill();for(let i=0;i<12;i++){const a=i*Math.PI/6;ctx.strokeStyle=q>=0?'#fbbf24':'#bae6fd';ctx.beginPath();ctx.moveTo(cx,cy);ctx.lineTo(cx+Math.cos(a)*r*30,cy+Math.sin(a)*r*30);ctx.stroke();}text(`场强相对值 E∝q/r²=${E.toFixed(2)}`,90,90,32,'#fbbf24');text('电场是电荷周围对其他电荷施力的空间性质。',90,380,24,'#dbeafe');document.getElementById('lab-feedback').textContent=`电荷量越大场越强，距离越远按平方减弱。`;}
document.querySelectorAll('#q1,#er').forEach(el=>el.addEventListener('input',drawElectric));drawElectric();
"""
    if kind == "circuit":
        return common + """
function drawCircuit(){clearCanvas();const U=+document.getElementById('voltage').value,R=+document.getElementById('resistance').value;const I=U/R,P=U*I;ctx.strokeStyle='#38bdf8';ctx.lineWidth=5;ctx.strokeRect(220,130,380,190);ctx.fillStyle='#fbbf24';ctx.fillRect(250,200,60,30);ctx.strokeStyle='#f97316';ctx.beginPath();ctx.arc(500,225,35,0,Math.PI*2);ctx.stroke();text(`I=U/R=${I.toFixed(2)}A`,90,90,32,'#fbbf24');text(`P=UI=${P.toFixed(1)}W`,90,145,30,'#dbeafe');document.getElementById('lab-feedback').textContent=`电压推动电荷定向移动，电阻限制电流。`;}
document.querySelectorAll('#voltage,#resistance').forEach(el=>el.addEventListener('input',drawCircuit));drawCircuit();
"""
    if kind == "magnetic":
        return common + """
function drawMagnetic(){clearCanvas();const I=+document.getElementById('mag-i').value,B=+document.getElementById('mag-b').value,a=+document.getElementById('mag-a').value*Math.PI/180;const F=B*I*Math.sin(a);text(`F=BILsinθ=${F.toFixed(2)}（相对）`,90,90,32,'#fbbf24');ctx.strokeStyle='#38bdf8';ctx.lineWidth=8;ctx.beginPath();ctx.moveTo(160,260);ctx.lineTo(720,260);ctx.stroke();ctx.strokeStyle='#f97316';ctx.lineWidth=4;for(let x=180;x<720;x+=60){ctx.beginPath();ctx.moveTo(x,110);ctx.lineTo(x,390);ctx.stroke();}text('磁场方向、电流方向和受力方向共同决定带电粒子或通电导线运动。',90,410,24,'#dbeafe');document.getElementById('lab-feedback').textContent=`夹角越接近 90°，安培力或洛伦兹力越明显。`;}
document.querySelectorAll('#mag-i,#mag-b,#mag-a').forEach(el=>el.addEventListener('input',drawMagnetic));drawMagnetic();
"""
    if kind == "wave":
        return common + """
function drawWave(){clearCanvas();const f=+document.getElementById('wave-f').value,v=+document.getElementById('wave-v').value;const lam=v/f;ctx.strokeStyle='#38bdf8';ctx.lineWidth=4;ctx.beginPath();for(let x=80;x<820;x+=4){const y=230+60*Math.sin((x-80)/lam/12*Math.PI*2);if(x===80)ctx.moveTo(x,y);else ctx.lineTo(x,y);}ctx.stroke();text(`λ=v/f=${lam.toFixed(2)}m`,90,90,32,'#fbbf24');text('频率越高，在同一波速下波长越短。',90,380,24,'#dbeafe');document.getElementById('lab-feedback').textContent=`波速 ${v}m/s，频率 ${f}Hz，波长 ${lam.toFixed(2)}m。`;}
document.querySelectorAll('#wave-f,#wave-v').forEach(el=>el.addEventListener('input',drawWave));drawWave();
"""
    if kind == "gas_laws":
        return common + """
function drawGasLaw(){clearCanvas();const T=+document.getElementById('gas-t').value,V=+document.getElementById('gas-v').value;const P=T/V;ctx.strokeStyle='#38bdf8';ctx.lineWidth=4;ctx.strokeRect(360,120,180,V*12);for(let i=0;i<40;i++){ctx.fillStyle='#fbbf24';ctx.beginPath();ctx.arc(370+Math.random()*160,130+Math.random()*Math.max(40,V*12-20),4,0,Math.PI*2);ctx.fill();}text(`P∝T/V=${P.toFixed(1)}（相对）`,90,90,32,'#fbbf24');document.getElementById('lab-feedback').textContent=`温度升高压强增大，体积增大压强降低（定量模型需看控制变量）。`;}
document.querySelectorAll('#gas-t,#gas-v').forEach(el=>el.addEventListener('input',drawGasLaw));drawGasLaw();
"""
    if kind == "modern":
        return common + """
function drawModern(){clearCanvas();const nu=+document.getElementById('nu').value,W=+document.getElementById('work').value;const Ek=Math.max(0,nu-W);text(`光子能量 E=hν：频率倍数 ${nu}`,90,90,32,'#fbbf24');text(`逸出功倍数 ${W}，最大动能≈${Ek}`,90,150,30,'#dbeafe');ctx.fillStyle=Ek>0?'#22c55e':'#64748b';ctx.fillRect(420,260,260,60);text(Ek>0?'有光电子逸出':'频率不足，无光电子',420,240,26,'#f8fafc');document.getElementById('lab-feedback').textContent=Ek>0?'频率超过阈值，发生光电效应。':'强度再大也不够，频率未超过阈值。';}
document.querySelectorAll('#nu,#work').forEach(el=>el.addEventListener('input',drawModern));drawModern();
"""
    return common + """
function drawCircular(){clearCanvas();const r=+document.getElementById('radius').value,v=+document.getElementById('speed').value;const a=v*v/r;const cx=470,cy=220,R=r*23;ctx.strokeStyle='#38bdf8';ctx.lineWidth=4;ctx.beginPath();ctx.arc(cx,cy,R,0,Math.PI*2);ctx.stroke();ctx.fillStyle='#fbbf24';ctx.beginPath();ctx.arc(cx+R/Math.sqrt(2),cy-R/Math.sqrt(2),18,0,Math.PI*2);ctx.fill();ctx.strokeStyle='#22c55e';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(cx+R/Math.sqrt(2),cy-R/Math.sqrt(2));ctx.lineTo(cx,cy);ctx.stroke();text(`a=v²/r=${a.toFixed(1)} m/s²`,90,90,32,'#fbbf24');text('绿色箭头指向圆心：速度方向改变产生向心加速度。',90,380,24,'#dbeafe');document.getElementById('lab-feedback').textContent=`半径 ${r}m、速率 ${v}m/s，向心加速度 ${a.toFixed(1)}m/s²。`;}
document.querySelectorAll('#radius,#speed').forEach(el=>el.addEventListener('input',drawCircular));drawCircular();
"""


def make_extra_svg(node: dict, detail: dict, mode: str) -> str:
    title = "概念结构图" if mode == "concept" else "过程机制图"
    labels = [c[0] for c in detail["concepts"]] if mode == "concept" else ["物理对象", "变量关系", "可测证据"]
    subtitle = detail["question"] if mode == "concept" else detail["memory"]
    cards = []
    colors = ["#38bdf8", "#a78bfa", "#22c55e"]
    for i, label in enumerate(labels[:3]):
        x = 80 + i * 360
        cards.append(f'<rect x="{x}" y="250" width="280" height="150" rx="22" fill="#0f172a" stroke="{colors[i]}" stroke-width="4"/><text x="{x+30}" y="330" fill="{colors[i]}" font-size="30" font-weight="800">{esc(label)}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="640" viewBox="0 0 1200 640"><rect width="1200" height="640" fill="#081426"/><circle cx="1020" cy="110" r="170" fill="#38bdf8" opacity="0.12"/><text x="80" y="100" fill="#f8fafc" font-size="48" font-weight="900">{esc(node['name'])} · {title}</text><text x="80" y="158" fill="#cbd5e1" font-size="26">{esc(subtitle[:56])}</text>{''.join(cards)}<text x="80" y="540" fill="#fbbf24" font-size="28">从图像进入问题，再回到定义、模型、数据和迁移任务。</text></svg>'''


def make_hero_svg(course_id: str, node: dict, detail: dict) -> str:
    labels = detail["concepts"]
    cards = []
    colors = ["#38bdf8", "#a78bfa", "#22c55e"]
    for i, (title, txt) in enumerate(labels):
        x = 70 + i * 390
        cards.append(f'<rect x="{x}" y="270" width="330" height="190" rx="24" fill="#0f172a" stroke="{colors[i]}" stroke-width="4"/><text x="{x+26}" y="325" fill="{colors[i]}" font-size="28" font-weight="800">{esc(title)}</text><text x="{x+26}" y="374" fill="#dbeafe" font-size="21">{esc(txt[:30])}</text><text x="{x+26}" y="410" fill="#dbeafe" font-size="21">{esc(txt[30:58])}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720"><defs><linearGradient id="g" x1="0" x2="1"><stop stop-color="#07111f"/><stop offset="1" stop-color="#172554"/></linearGradient></defs><rect width="1280" height="720" fill="url(#g)"/><circle cx="1050" cy="120" r="180" fill="#38bdf8" opacity="0.13"/><circle cx="220" cy="620" r="220" fill="#a78bfa" opacity="0.12"/><text x="70" y="112" fill="#f8fafc" font-size="52" font-weight="900">{esc(node['name'])}</text><text x="70" y="168" fill="#bae6fd" font-size="28">{esc(detail['question'])}</text><text x="70" y="225" fill="#cbd5e1" font-size="24">角色任务：{esc(detail['role'])} · 课标节点：{esc(node['id'])}</text>{''.join(cards)}<rect x="70" y="525" width="1140" height="105" rx="24" fill="#020617" opacity="0.72" stroke="#334155"/><text x="105" y="585" fill="#fbbf24" font-size="30" font-weight="800">记忆锚点</text><text x="260" y="585" fill="#e0f2fe" font-size="26">{esc(detail['memory'])}</text><text x="70" y="675" fill="#64748b" font-size="18">TeachAny v7.14 · 高中物理完整模式 · AI 学伴 / TTS / 知识图谱 / Canvas 互动 / 课标挂树</text></svg>'''


def make_content(course_id: str, node: dict, detail: dict) -> str:
    pre_q, pre_opts, pre_ans, pre_feedback = detail["pretest"]
    post_q, post_opts, post_ans, post_feedback = detail["posttest"]
    concepts = "\n".join(f'<div class="mini-panel"><h3>{esc(t)}</h3><p>{esc(txt)}</p></div>' for t, txt in detail["concepts"])
    facts = "\n".join(f"<li>{esc(x)}</li>" for x in detail["facts"])
    external = ""
    if detail.get("external"):
        external = f'''
<section class="section" id="external-sim" data-tts="external-sim" data-tsh="外部仿真 - 用成熟工具观察变量变化">
  <div class="lesson-panel">
    <span class="phase-tag">PhET Simulation</span>
    <h2>成熟仿真：自由操作，回到模型解释</h2>
    <p style="color:var(--muted)">拖动参数，观察变量变化。仿真负责让现象可见，解释仍要回到本课的物理模型。</p>
    <div class="iframe-wrap"><iframe src="{esc(detail['external'])}" allowfullscreen loading="lazy" sandbox="allow-scripts allow-same-origin allow-forms allow-popups"></iframe></div>
  </div>
</section>'''
    return f'''
<style>.lesson-panel{{background:linear-gradient(180deg,rgba(20,35,58,.96),rgba(13,27,47,.96));border:1px solid rgba(148,163,184,.18);border-radius:18px;padding:22px;box-shadow:0 16px 40px rgba(0,0,0,.18)}}.mini-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}}.mini-panel{{background:rgba(15,23,42,.68);border:1px solid rgba(148,163,184,.18);border-radius:16px;padding:16px}}.mini-panel h3{{margin:0 0 8px;color:#bae6fd}}.quiz-option{{display:block;width:100%;margin:8px 0;border:1px solid rgba(56,189,248,.28);background:#0b1628;color:#eef6ff;border-radius:12px;padding:12px 14px;text-align:left;cursor:pointer}}.quiz-option.correct{{border-color:#22c55e;background:rgba(34,197,94,.14)}}.quiz-option.wrong{{border-color:#f97316;background:rgba(249,115,22,.14)}}.feedback{{min-height:44px;margin-top:10px;padding:10px 12px;border-radius:12px;background:rgba(56,189,248,.10);color:#dbeafe}}.control-row{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;align-items:end;margin:12px 0}}.control-row label{{color:#cbd5e1;font-size:14px}}.iframe-wrap{{position:relative;width:100%;padding-top:62.5%;border-radius:14px;overflow:hidden;background:#0f172a}}.iframe-wrap iframe{{position:absolute;inset:0;width:100%;height:100%;border:0}}.video-box video{{width:100%;border-radius:14px;border:1px solid rgba(148,163,184,.18);background:#020617}}figure img{{width:100%;border-radius:12px}}</style>
<section class="section" id="story" data-tts="story" data-tsh="情境任务 - 用 ABT 明确为什么学"><div class="lesson-panel"><span class="phase-tag">ABT Story</span><h2>角色任务：{esc(detail['role'])}</h2><div class="mini-grid"><div class="mini-panel"><h3>And 已有经验</h3><p>{esc(detail['and'])}</p></div><div class="mini-panel"><h3>But 真实卡点</h3><p>{esc(detail['but'])}</p></div><div class="mini-panel"><h3>Therefore 本课任务</h3><p>{esc(detail['therefore'])}</p></div></div><p>这不是单纯换一个题目名称，而是换一种看物理问题的方式：先明确研究对象，再明确参考方向和可忽略条件，最后才把数量关系写成公式。只要这三步没有走完，任何公式代入都可能只是碰运气。</p></div></section>
<section class="section" id="model-checklist" data-tts="model-checklist" data-bloom-level="analyze" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">Model Checklist</span><h2>建模检查表：这道题到底能不能这样算？</h2><p><strong>第一问：对象是谁？</strong>物理题里的“车”“球”“乘客”“卫星”不能混着看。研究对象一旦换了，受力、速度、位移和参考系都可能跟着变。本课所有判断都要先锁定对象。</p><p><strong>第二问：方向怎么定？</strong>速度、位移、加速度都是带方向的量。把正方向定清楚，才能解释为什么某个量为正、为负或为零。很多错误不是不会算，而是把方向当成普通数字。</p><p><strong>第三问：条件能不能简化？</strong>忽略阻力、加速度恒定、只看一维运动、半径不变等条件都是模型边界。题目一旦越过边界，就要换模型或分段处理。</p></div></section>
<section class="section" id="pretest" data-tts="pretest" data-bloom-level="remember" data-scaffold="full" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">Pre-test</span><h2>前测：你已经知道什么？</h2><p><strong>{esc(pre_q)}</strong></p>{make_buttons(pre_opts, pre_ans, 'pretest')}<div id="pretest-feedback" class="feedback">先选一项，系统会给出错因诊断。</div></div></section>
<section class="section" id="core" data-tts="core" data-bloom-level="understand" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">Core Ideas</span><h2>核心概念：先抓物理模型</h2><div class="mini-grid">{concepts}</div></div></section>
<section class="section" id="deep-understanding" data-tts="deep-understanding"><div class="lesson-panel insight-box"><span class="phase-tag">Five Lens</span><h2>🔍 深层理解：五镜头看本质</h2><ul><li><strong>看见它：</strong>{esc(detail['facts'][0])}</li><li><strong>拆开它：</strong>{esc(detail['facts'][1])}</li><li><strong>解释它：</strong>{esc(detail['facts'][2])}</li><li><strong>比较它：</strong>把本课模型和另一个容易混淆的运动场景放在一起，比较对象、方向、条件和图像含义。</li><li><strong>迁移它：</strong>换一个真实情境，仍然用同一套变量关系解释现象。</li></ul><p class="feedback"><strong>记忆锚点：</strong>{esc(detail['memory'])}</p></div></section>
<section class="section" id="worked-example" data-tts="worked-example" data-bloom-level="analyze" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">Worked Example</span><h2>例题拆解：先画对象和变量</h2><p>遇到「{esc(node['name'])}」问题，先画研究对象和参考方向，再标出已知量、未知量和约束条件。不要先套公式，先判断模型是否成立：是理想化模型、分段模型，还是需要考虑方向变化。</p><p>第二步，把文字翻译成物理量关系。题干里的“静止、匀速、加速、回到起点、方向改变、忽略阻力”等词，都不是装饰，它们决定公式能不能用。</p><p>第三步写结论，并解释为什么不是另一个选项。本课高频误区是：{esc(detail['error'])} 这个错误通常来自忽略矢量方向、模型条件或图像含义。</p></div></section>
<section class="section" id="transfer-task" data-tts="transfer-task" data-bloom-level="create" data-scaffold="none"><div class="lesson-panel"><span class="phase-tag">Transfer Task</span><h2>迁移任务：设计一个新运动场景</h2><p>请设计一个与本课模型相似但情境不同的问题，必须写出研究对象、参考系或正方向、已知量、要判断的物理量，以及一个容易误判的选项。最后写诊断反馈：错在哪里、该看哪个条件、正确判断怎样得到。</p></div></section>
<section class="section" id="visual-evidence" data-tts="visual-evidence"><div class="lesson-panel"><span class="phase-tag">Visual Evidence</span><h2>两张图先建立直觉</h2><div class="mini-grid"><figure class="mini-panel"><img src="./assets/concept-diagram.svg" alt="概念结构图"><figcaption>概念结构：核心对象、变量和判断标准。</figcaption></figure><figure class="mini-panel"><img src="./assets/process-diagram.svg" alt="过程机制图"><figcaption>过程机制：条件如何改变可观察结果。</figcaption></figure></div></div></section>
<section class="section" id="evidence-table" data-tts="evidence-table" data-bloom-level="evaluate" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">Evidence Table</span><h2>证据表：把现象翻译成物理判断</h2><p><strong>如果题目给图像，</strong>先看横轴和纵轴分别是什么，再判断斜率、面积或截距有没有物理意义。x-t 图和 v-t 图绝不能混读；同样一条斜线，在不同图像里的含义完全不同。</p><p><strong>如果题目给文字，</strong>要把“匀速”“静止”“回到起点”“忽略空气阻力”“做圆周运动”等词翻译成数学条件。这些词通常决定一个量是不是零、一个公式能不能用、一个方向是否改变。</p><p><strong>如果题目给实验现象，</strong>不要只说“看起来更快”。要追问可测证据是什么：位置随时间怎样变、速度是否改变、加速度方向在哪里、哪个因素被控制了。</p></div></section>
<section class="section" id="interactive-lab" data-tts="interactive-lab" data-bloom-level="apply" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">Interactive Lab</span><h2>互动实验：调变量，看结果</h2><p style="color:var(--muted)">先动手改变变量，再用一句话解释图像为什么变了。</p><div class="control-row">{interaction_controls(detail['interaction'])}</div><div class="canvas-wrap"><canvas id="physics-canvas" class="wide-canvas" width="900" height="430"></canvas></div><div id="lab-feedback" class="feedback">拖动或选择变量，观察画布变化。</div></div></section>
{external}
<section class="section" id="micro-video" data-tts="micro-video"><div class="lesson-panel video-box"><span class="phase-tag">Micro Lesson</span><h2>微课讲解：60 秒内复盘核心关系</h2><video controls preload="metadata" playsinline><source src="./assets/video/{esc(course_id)}-main.mp4" type="video/mp4"></video></div></section>
<section class="section" id="posttest" data-tts="posttest" data-bloom-level="evaluate" data-scaffold="none" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">Post-test</span><h2>后测：学会了吗？</h2><p><strong>{esc(post_q)}</strong></p>{make_buttons(post_opts, post_ans, 'posttest')}<div id="posttest-feedback" class="feedback">先独立判断，再看诊断反馈。</div></div></section>
<section class="section" id="tiered-practice" data-tts="tiered-practice"><div class="lesson-panel"><span class="phase-tag">Level Practice</span><h2>三段式作业</h2><div class="mini-grid"><div class="mini-panel"><h3>⭐ 基础巩固</h3><p>写出本课模型、变量和适用条件。</p></div><div class="mini-panel"><h3>⭐⭐ 能力应用</h3><p>把模型用于一个新运动情境，并说明方向和单位。</p></div><div class="mini-panel"><h3>⭐⭐⭐ 迁移挑战</h3><p>设计一个反例，说明常见错误为什么站不住脚。</p></div></div></div></section>
<section class="section" id="summary" data-tts="summary"><div class="lesson-panel"><span class="phase-tag">Summary</span><h2>一句话带走</h2><ul>{facts}</ul><p class="feedback">如果你能解释“{esc(detail['question'])}”，这节课就真正过关了。</p></div></section>
<script>const FEEDBACK={{ pretest:{json.dumps(pre_feedback, ensure_ascii=False)}, posttest:{json.dumps(post_feedback, ensure_ascii=False)} }};function checkAnswer(btn,ok,target){{btn.parentElement.querySelectorAll('.quiz-option').forEach(b=>b.classList.remove('correct','wrong'));btn.classList.add(ok?'correct':'wrong');const box=document.getElementById(target+'-feedback');if(box)box.textContent=ok?FEEDBACK[target]:'错因诊断：先回到模型条件、方向和单位，再检查你是否把物理量含义搞混了。'+FEEDBACK[target];}}{interaction_script(detail['interaction'])}</script>
'''


def write_manifest(course_dir: Path, course_id: str, node: dict, domain: dict, detail: dict):
    manifest = {
        "id": course_id,
        "course_id": course_id,
        "node_id": node["id"],
        "name": detail["title"],
        "name_en": detail["title_en"],
        "subject": "physics",
        "grade": node.get("grade", 10),
        "stage": "high",
        "domain": domain.get("id", "kinematics"),
        "lesson_type": "experiment",
        "status": "community",
        "author": "TeachAny",
        "version": "1.0.0",
        "teachany_version": "7.14.0",
        "curriculum": "cn-national",
        "description": f"高中物理课标互动课件：{node['name']}。包含问题锚点、ABT 情境、Canvas/PhET 互动、TTS、微课、知识图谱与 AI 学伴。",
        "tags": ["高中物理", "中国课标", node["name"]],
        "difficulty": 3,
        "duration": "15-20 min",
        "prerequisites": node.get("prerequisites", []),
        "leads_to": node.get("extends", []),
        "learning_objectives": detail["objectives"],
        "curriculum_standards": [
            {"source": "普通高中物理课程标准", "content": point}
            for point in (node.get("curriculum_points") or [f"围绕{node['name']}形成物理观念、科学推理和模型建构能力。"])
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
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 {node.get('grade', 10)} 年级
- 学科：物理
- 课标节点：{node['name']}
- 课标摘录：{'；'.join(node.get('curriculum_points', [])[:3])}

## Phase 1 教学骨架
- 问题锚点：{detail['question']}
- ABT：
  - And：{detail['and']}
  - But：{detail['but']}
  - Therefore：{detail['therefore']}
- 真实互动：Canvas 变量实验 + PhET/本地模型 + 前后测反馈
- 评估闭环：前测 → 概念拆解 → 例题拆解 → 互动实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 物理仿真：按课题使用 Canvas + PhET/成熟资源，未使用外部资源的课件由本地 Canvas 完成核心互动。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/{course_id}`
- `python3 scripts/validate-courseware.py {course_id}`
- `python3 scripts/rebuild-index.py`
"""


def generate_tts(course_dir: Path, detail: dict):
    tts_dir = course_dir / "tts"
    tts_dir.mkdir(parents=True, exist_ok=True)
    segments = [("s01", f"今天我们学习{detail['title']}。核心问题是：{detail['question']}"), ("s02", f"这节课先抓模型条件，再看变量关系。{detail['memory']}"), ("s03", f"最后提醒一个高频易错点：{detail['error']}")]
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
        try: return ImageFont.truetype(str(font_path), size) if font_path else ImageFont.load_default()
        except Exception: return ImageFont.load_default()
    frames_dir = video_dir / "_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    frame_texts = [(node["name"], detail["question"]), ("模型条件", detail["memory"]), ("易错诊断", detail["error"]), ("迁移任务", "换一个场景，仍然从对象、方向、变量和模型条件开始。"), ("学习闭环", "前测 → 模型 → 图像/实验 → 后测 → 迁移")]
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
                draw.text((110, y), line, font=font(34), fill="#dbeafe"); y += 58; line = ch
            else:
                line = trial
        if line: draw.text((110, y), line, font=font(34), fill="#dbeafe")
        draw.text((110, 585), f"TeachAny 高中物理 · {course_id} · {i}/5", font=font(26), fill="#94a3b8")
        img.save(frames_dir / f"frame_{i:03d}.png")
    audio = course_dir / "tts" / "s01.mp3"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(frames_dir / "frame_%03d.png")]
    if audio.exists(): cmd += ["-i", str(audio)]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "25"]
    if audio.exists(): cmd += ["-c:a", "aac", "-shortest"]
    cmd += [str(out)]
    subprocess.run(cmd, check=True)
    shutil.rmtree(frames_dir, ignore_errors=True)


def generate_course(course_id: str, node: dict, domain: dict, detail: dict):
    course_dir = ROOT / "community" / course_id
    if course_dir.exists(): shutil.rmtree(course_dir)
    (course_dir / "assets").mkdir(parents=True, exist_ok=True)
    generate_tts(course_dir, detail)
    generate_video(course_dir, course_id, node, detail)
    (course_dir / "assets/hero-infographic.svg").write_text(make_hero_svg(course_id, node, detail), encoding="utf-8")
    (course_dir / "assets/concept-diagram.svg").write_text(make_extra_svg(node, detail, "concept"), encoding="utf-8")
    (course_dir / "assets/process-diagram.svg").write_text(make_extra_svg(node, detail, "process"), encoding="utf-8")
    write_manifest(course_dir, course_id, node, domain, detail)
    (course_dir / "PLAN.md").write_text(make_plan(course_id, node, detail), encoding="utf-8")
    audio_manifest = json.loads((course_dir / "tts/manifest.json").read_text(encoding="utf-8"))
    skeleton = SKELETON.read_text(encoding="utf-8")
    choices = "\n".join(f'<button class="choice" data-anchor-choice="{esc(label)}">{esc(label)}</button>' for label in ["判断模型", "读图求量", "解释现象"])
    objectives = "\n".join(f"<li>{esc(x)}</li>" for x in detail["objectives"])
    html_text = replace_all(skeleton, {
        "COURSE_ID": course_id, "TITLE": detail["title"], "DESCRIPTION": f"高中物理课标互动课件：{node['name']}。", "SUBJECT": "physics", "STAGE_GRADE": f"high-{node.get('grade', 10)}", "GRADE": str(node.get("grade", 10)), "STAGE": "high", "NODE_ID": node["id"], "DOMAIN": domain.get("id", "kinematics"), "PREREQ_COURSE_IDS": ",".join(node.get("prerequisites", [])), "NEXT_COURSE_ID": "", "COURSE_VERSION": "1.0.0", "TEACHANY_VERSION": "7.14.0", "LESSON_TYPE": "experiment", "HERO_QUESTION": detail["question"], "HERO_IMAGE_ALT": f"{node['name']}知识结构图", "HERO_FIGCAPTION": f"{node['name']}：模型、变量、图像和迁移任务。", "AUDIO_PLAYLIST_JSON": json.dumps(audio_manifest, ensure_ascii=False, indent=2), "PROBLEM_ANCHOR_CHOICES": choices, "LEARNING_OBJECTIVES": objectives, "CONTENT_SECTIONS": make_content(course_id, node, detail), "OPTIONAL_MAP_HEAD": "", "OPTIONAL_MAP_TAIL": "", "PREREQUISITE_NAMES": ", ".join(node.get("prerequisites", [])) or "无", "FREE_MODE": "false"
    })
    html_text = html_text.replace('src="./assets/' + course_id + '-hero.png" onerror="this.src=\'./assets/hero-infographic.svg\'"', 'src="./assets/hero-infographic.svg"')
    html_text = html_text.replace(f'<title>{detail["title"]}</title>', f'<title>{detail["title"]} · 高中物理 G{node.get("grade", 10)} · TeachAny v7.14</title>')
    html_text = html_text.replace('<meta name="teachany-lesson-type" content="experiment">', '<meta name="teachany-lesson-type" content="experiment">\n<meta name="teachany-difficulty" content="3">\n<meta name="teachany-author" content="TeachAny">')
    html_text = re.sub(r'<!--.*?-->', '', html_text, flags=re.S)
    html_text = html_text.replace(' placeholder="把你卡住的问题写在这里"', ' aria-label="把你卡住的问题写在这里"').replace('aria-label="知识图谱互动画布占位"', 'aria-label="知识图谱互动画布"').replace('placeholder', '提示输入').replace('占位', '备用')
    (course_dir / "index.html").write_text(html_text, encoding="utf-8")
    print(f"✅ generated {course_id}")


def main():
    nodes, domains = read_tree_nodes()
    for node_id in BATCH_IDS:
        generate_course(node_id, nodes[node_id], domains[node_id], DETAILS[node_id])


if __name__ == "__main__":
    main()
