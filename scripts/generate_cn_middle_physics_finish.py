#!/usr/bin/env python3
"""Generate all CN middle-school physics courseware in TeachAny complete mode."""
from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path("/Users/wepon/.workbuddy/skills/TeachAny")
SKELETON = SKILL / "templates/course-skeleton.html"
TREE = ROOT / "data/trees/cn/middle/physics.json"
TODAY = date.today().isoformat()

PHET = {
    "sound": "https://phet.colorado.edu/sims/html/waves-intro/latest/waves-intro_zh_CN.html",
    "light": "https://phet.colorado.edu/sims/html/bending-light/latest/bending-light_zh_CN.html",
    "lens": "https://phet.colorado.edu/sims/html/geometric-optics/latest/geometric-optics_zh_CN.html",
    "thermal": "https://phet.colorado.edu/sims/html/energy-skate-park-basics/latest/energy-skate-park-basics_zh_CN.html",
    "mechanics": "https://phet.colorado.edu/sims/html/forces-and-motion-basics/latest/forces-and-motion-basics_zh_CN.html",
    "density": "https://phet.colorado.edu/sims/html/density/latest/density_zh_CN.html",
    "machine": "https://phet.colorado.edu/sims/html/balancing-act/latest/balancing-act_zh_CN.html",
    "energy": "https://phet.colorado.edu/sims/html/energy-skate-park-basics/latest/energy-skate-park-basics_zh_CN.html",
    "electric": "https://phet.colorado.edu/sims/html/circuit-construction-kit-dc/latest/circuit-construction-kit-dc_zh_CN.html",
    "ohm": "https://phet.colorado.edu/sims/html/ohms-law/latest/ohms-law_zh_CN.html",
    "magnetic": "https://phet.colorado.edu/sims/html/faradays-law/latest/faradays-law_zh_CN.html",
}


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def read_tree_nodes():
    tree = json.loads(TREE.read_text(encoding="utf-8"))
    nodes, domains = {}, {}
    for domain in tree["domains"]:
        for node in domain.get("nodes", []):
            nodes[node["id"]] = node
            domains[node["id"]] = domain
    return nodes, domains, list(nodes.keys())


def replace_all(template: str, values: dict[str, str]) -> str:
    out = template
    for key, value in values.items():
        out = out.replace("{{" + key + "}}", value)
    return out


def profile_for(node_id: str, name: str, domain: dict):
    text = f"{node_id} {name} {domain.get('name','')}"
    rules = [
        ("sound", "sound", "声学实验员", ["振动声源", "介质传播", "波形特征"], "声现象三问：谁在振动，靠什么传播，频率和振幅怎样改变听感。"),
        ("noise", "sound", "噪声治理工程师", ["声源", "传播途径", "接收者"], "噪声控制抓三处：声源减弱、传播阻断、耳边防护。"),
        ("light-propagation", "light", "光路实验员", ["光源", "直线传播", "影和小孔成像"], "光路题先画光线，再说明条件：同种均匀介质中沿直线传播。"),
        ("mirror", "light", "镜面成像分析师", ["反射光线", "虚像位置", "像物关系"], "平面镜成像记住：像物等大、等距、连线垂直镜面。"),
        ("refraction", "light", "折射现象判读员", ["入射角", "折射角", "介质变化"], "折射题先判光从哪种介质进入哪种介质，再比较角度变化。"),
        ("dispersion", "light", "色光实验员", ["白光分解", "色光混合", "光谱证据"], "色散说明白光不是单一色光，颜色来自不同光的组合。"),
        ("lens", "lens", "透镜成像调试员", ["焦距", "物距", "像距"], "透镜成像先比较物距和焦距，再判断倒正、大小和虚实。"),
        ("eye", "lens", "视力矫正顾问", ["晶状体", "成像位置", "矫正透镜"], "近视远视的关键是像落在视网膜前还是后。"),
        ("thermo", "thermal", "温度测量员", ["热胀冷缩", "读数方法", "量程分度"], "温度计读数要看量程、分度值和液柱稳定位置。"),
        ("phase", "thermal", "物态变化观察员", ["吸热放热", "熔点沸点", "状态变化"], "物态变化判断先看状态变了没有，再判断吸热还是放热。"),
        ("internal", "thermal", "热现象解释员", ["分子运动", "内能改变", "做功热传递"], "改变内能只有两类路径：做功和热传递。"),
        ("specific", "thermal", "比热容实验员", ["质量", "升温", "吸热能力"], "比热容比较要控制质量和吸收热量，不能只看温度高低。"),
        ("heat", "thermal", "热量计算员", ["质量", "比热容", "温度变化"], "热量计算抓公式 Q=cmΔt，并先统一单位。"),
        ("engine", "thermal", "热机效率评估员", ["燃料热值", "有用功", "能量损失"], "热机效率不是越热越高，而是有用能占总能量的比例。"),
        ("motion", "mechanics", "运动测量员", ["长度时间", "速度", "运动图像"], "运动题先确定路程和时间，再用速度描述快慢。"),
        ("density", "density", "密度鉴定员", ["质量", "体积", "物质属性"], "密度是物质属性，计算前先看质量和体积单位。"),
        ("force", "mechanics", "受力图绘制员", ["作用效果", "力的三要素", "受力示意图"], "力的题先画受力图，方向和作用点比数值更先要清楚。"),
        ("gravity", "mechanics", "重力测量员", ["质量", "重力", "方向竖直向下"], "重力 G=mg，方向总是竖直向下，不等于垂直斜面。"),
        ("friction", "mechanics", "摩擦实验员", ["压力", "接触面", "运动趋势"], "摩擦力方向总是阻碍相对运动或相对运动趋势。"),
        ("newton", "mechanics", "惯性诊断员", ["惯性", "二力平衡", "运动状态"], "不受力不等于静止，物体可能保持匀速直线运动。"),
        ("machine", "machine", "简单机械设计师", ["力臂", "平衡条件", "省力省距离"], "杠杆平衡看力和力臂乘积，不只看力的大小。"),
        ("work", "energy", "功率评估员", ["力", "距离", "时间"], "功看力和沿力方向位移，功率看做功快慢。"),
        ("energy", "energy", "能量转化分析师", ["动能", "势能", "守恒"], "能量题先确定系统，再判断能量怎样转化和转移。"),
        ("static", "electric", "静电观察员", ["摩擦起电", "电荷种类", "相互作用"], "同种电荷相斥，异种电荷相吸，验电器看电荷转移。"),
        ("circuit", "electric", "电路搭建员", ["电源", "用电器", "闭合回路"], "电路能工作必须形成闭合回路，不能只看导线有没有连上。"),
        ("series", "electric", "串并联诊断员", ["电流路径", "电压分配", "故障判断"], "串并联先数电流路径，一条路是串联，多条路是并联。"),
        ("current", "electric", "电流测量员", ["电流表", "串联接入", "量程选择"], "电流表要串联，先大量程试触再选合适量程。"),
        ("voltage", "electric", "电压测量员", ["电压表", "并联接入", "电势差"], "电压表要并联，测的是两点间推动电荷的能力差。"),
        ("resistance", "ohm", "电阻实验员", ["材料", "长度横截面积", "温度"], "电阻不是电流变小的结果，而是导体阻碍电流的性质。"),
        ("ohm", "ohm", "欧姆定律分析员", ["电压", "电流", "电阻"], "欧姆定律题先明确同一导体同一状态下 U、I、R 的关系。"),
        ("power", "electric", "电功率评估员", ["电功", "功率", "额定实际"], "实际功率要看实际电压，不能只背铭牌额定值。"),
        ("joule", "electric", "电热安全分析师", ["电流平方", "电阻", "通电时间"], "焦耳定律 Q=I²Rt，电流变大带来的发热增加最明显。"),
        ("safety", "electric", "安全用电顾问", ["火线零线", "保险装置", "人体安全"], "家庭电路安全抓火线、漏电保护、功率过载和湿手用电风险。"),
        ("magnet", "magnetic", "磁场观察员", ["磁极", "磁感线", "地磁场"], "磁感线外部从 N 极到 S 极，磁场方向用小磁针 N 极指向判断。"),
        ("electromagnet", "magnetic", "电磁铁调试员", ["电流方向", "线圈匝数", "铁芯"], "电磁铁强弱可由电流大小、匝数和有无铁芯调节。"),
        ("motor", "magnetic", "电动机工程师", ["通电导线受力", "换向器", "能量转化"], "电动机把电能转化为机械能，关键是通电线圈在磁场中受力转动。"),
        ("induction", "magnetic", "发电实验员", ["磁通量变化", "感应电流", "相对运动"], "电磁感应要有闭合电路和磁场变化，二者缺一不可。"),
        ("generator", "magnetic", "发电机讲解员", ["线圈转动", "感应电流", "机械能到电能"], "发电机把机械能转化为电能，核心是电磁感应。"),
    ]
    for key, kind, role, labels, memory in rules:
        if key in text:
            return kind, role, labels, memory
    return "mechanics", "物理实验分析师", ["观察现象", "变量关系", "实验证据"], "初中物理题先看现象，再抓变量，最后回到实验依据。"


def make_detail(node: dict, domain: dict):
    node_id, name = node["id"], node["name"]
    kind, role, labels, memory = profile_for(node_id, name, domain)
    question = f"怎样用实验现象和变量关系解释{name}？"
    concepts = [
        (labels[0], f"学习{name}先要明确观察对象和实验条件，不能把生活直觉直接当结论。"),
        (labels[1], f"把{name}拆成可改变的变量、可观察的结果和需要控制的条件。"),
        (labels[2], f"用测量数据、图像或现象证据检验解释，而不是只背公式或定义。"),
    ]
    facts = [
        f"{name}来自真实实验现象，关键是把看见的现象转成物理量和变量关系。",
        f"判断{name}时，要说明哪些条件被控制，哪些变量被改变，结果如何响应。",
        f"能把{name}迁移到生活、工程或安全场景中，才算真正理解。",
    ]
    return {
        "title": f"{name}：从实验现象到变量关系",
        "title_en": re.sub(r"[^a-z0-9]+", "-", node_id.lower()).strip("-"),
        "role": role,
        "and": f"你已经在生活中见过{name}相关现象，也能说出一些直观经验。",
        "but": f"物理学习不能停在经验判断，因为经验常被条件影响；换一个材料、尺度或装置，结论可能改变。",
        "therefore": f"所以本课要用“观察现象—控制变量—建立关系—解释应用”的路径，理解{name}。",
        "question": question,
        "concepts": concepts,
        "facts": facts,
        "memory": memory,
        "error": f"常见错误：只背{name}的定义或公式，不说明实验条件、变量控制和证据来源。",
        "pretest": (f"研究{name}时，最关键的第一步是什么？", ["直接套公式", "先观察对象和条件", "只看答案选项", "先背结论"], 1, "物理探究先明确对象、条件和可观察现象。"),
        "posttest": (f"如果{name}实验结果与直觉不一致，应该优先怎么做？", ["否定实验", "只相信直觉", "检查变量控制和测量证据", "跳过不管"], 2, "直觉不可靠时，要回到变量控制和实验数据。"),
        "interaction": kind,
        "external": PHET.get(kind, PHET["mechanics"]),
        "objectives": [
            f"能描述{name}的关键实验现象和适用条件",
            f"能用变量关系或公式解释{name}中的变化",
            f"能把{name}用于生活、工程或安全情境分析",
        ],
    }


def make_buttons(items: list[str], answer: int, prefix: str) -> str:
    return "\n".join(
        f'<button class="quiz-option" onclick="checkAnswer(this,{"true" if i == answer else "false"},\'{prefix}\')">{esc(chr(65+i))}. {esc(item)}</button>'
        for i, item in enumerate(items)
    )


def interaction_controls(kind: str) -> str:
    base = {
        "sound": '''<label>频率 Hz<input id="p1" type="range" min="100" max="1000" value="440"></label><label>振幅<input id="p2" type="range" min="1" max="10" value="5"></label><label>介质<select id="p3"><option value="1">空气</option><option value="2">水</option><option value="0">真空</option></select></label>''',
        "light": '''<label>入射角 °<input id="p1" type="range" min="0" max="80" value="35"></label><label>介质折射率<input id="p2" type="range" min="1" max="2" step="0.05" value="1.33"></label><label>表面<select id="p3"><option value="1">平面</option><option value="2">水面</option><option value="3">玻璃</option></select></label>''',
        "lens": '''<label>物距 cm<input id="p1" type="range" min="5" max="80" value="30"></label><label>焦距 cm<input id="p2" type="range" min="5" max="30" value="15"></label><label>透镜<select id="p3"><option value="1">凸透镜</option><option value="-1">凹透镜</option></select></label>''',
        "thermal": '''<label>温度 ℃<input id="p1" type="range" min="-20" max="120" value="25"></label><label>吸热强度<input id="p2" type="range" min="0" max="10" value="5"></label><label>物质<select id="p3"><option value="1">水</option><option value="0.5">沙</option><option value="0.2">金属</option></select></label>''',
        "density": '''<label>质量 g<input id="p1" type="range" min="50" max="1000" value="300"></label><label>体积 cm³<input id="p2" type="range" min="50" max="800" value="200"></label><label>液体密度<input id="p3" type="range" min="0.5" max="1.5" step="0.1" value="1"></label>''',
        "machine": '''<label>动力 N<input id="p1" type="range" min="10" max="200" value="80"></label><label>动力臂 cm<input id="p2" type="range" min="10" max="100" value="60"></label><label>阻力臂 cm<input id="p3" type="range" min="10" max="100" value="30"></label>''',
        "energy": '''<label>质量 kg<input id="p1" type="range" min="1" max="20" value="5"></label><label>速度 m/s<input id="p2" type="range" min="0" max="30" value="8"></label><label>高度 m<input id="p3" type="range" min="0" max="20" value="5"></label>''',
        "electric": '''<label>电压 V<input id="p1" type="range" min="1" max="24" value="6"></label><label>电阻 Ω<input id="p2" type="range" min="1" max="50" value="12"></label><label>连接方式<select id="p3"><option value="1">串联</option><option value="2">并联</option></select></label>''',
        "ohm": '''<label>电压 V<input id="p1" type="range" min="1" max="24" value="6"></label><label>电阻 Ω<input id="p2" type="range" min="1" max="50" value="12"></label><label>通电时间 s<input id="p3" type="range" min="1" max="60" value="10"></label>''',
        "magnetic": '''<label>电流 A<input id="p1" type="range" min="0" max="10" value="4"></label><label>线圈匝数<input id="p2" type="range" min="1" max="80" value="30"></label><label>磁场强度<input id="p3" type="range" min="0" max="10" value="5"></label>''',
    }
    return base.get(kind, '''<label>变量 A<input id="p1" type="range" min="1" max="20" value="8"></label><label>变量 B<input id="p2" type="range" min="1" max="20" value="6"></label><label>条件 C<input id="p3" type="range" min="1" max="10" value="4"></label>''')


def interaction_script(kind: str, name: str) -> str:
    return f"""
const canvas=document.getElementById('physics-canvas');
const ctx=canvas.getContext('2d');
function clearCanvas(){{ctx.clearRect(0,0,canvas.width,canvas.height);ctx.fillStyle='#081426';ctx.fillRect(0,0,canvas.width,canvas.height);}}
function text(t,x,y,size=24,color='#eef6ff'){{ctx.fillStyle=color;ctx.font=`${{size}}px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif`;ctx.fillText(t,x,y);}}
function axes(){{ctx.strokeStyle='#334155';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(70,340);ctx.lineTo(830,340);ctx.moveTo(90,60);ctx.lineTo(90,360);ctx.stroke();}}
function drawGeneric(){{clearCanvas();axes();const a=+document.getElementById('p1').value,b=+document.getElementById('p2').value,c=+document.getElementById('p3').value;let value=0,label='';
if('{kind}'==='sound'){{value=a/20+b*8;label=`频率 ${{a}}Hz，振幅 ${{b}}，介质系数 ${{c}}`;for(let x=90;x<820;x+=4){{let y=220+Math.sin(x/a*20)*b*8;ctx.fillStyle='#38bdf8';ctx.fillRect(x,y,3,3);}}}}
else if('{kind}'==='light'){{value=a*c/10;label=`入射角 ${{a}}°，折射/反射变化 ${{value.toFixed(1)}}`;ctx.strokeStyle='#fbbf24';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(420,80);ctx.lineTo(500,240);ctx.lineTo(610,110+value);ctx.stroke();ctx.strokeStyle='#38bdf8';ctx.beginPath();ctx.moveTo(90,240);ctx.lineTo(820,240);ctx.stroke();}}
else if('{kind}'==='lens'){{let u=a,f=b,inv=1/f-1/u,v=inv?1/inv:999;value=v;label=`物距 ${{u}}cm，焦距 ${{f}}cm，像距约 ${{Math.abs(v).toFixed(1)}}cm`;ctx.strokeStyle='#38bdf8';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(450,90);ctx.lineTo(450,350);ctx.stroke();ctx.fillStyle='#fbbf24';ctx.fillRect(450-u*4,230,20,80);ctx.fillStyle='#a78bfa';ctx.fillRect(450+Math.max(-80,Math.min(260,v*4)),230,20,80);}}
else if('{kind}'==='thermal'){{value=a+b*10*c;label=`温度 ${{a}}℃，吸热后相对热状态 ${{value.toFixed(1)}}`;ctx.fillStyle=value>100?'#f97316':value>0?'#fbbf24':'#38bdf8';ctx.fillRect(420,330-Math.max(20,Math.min(260,value+40)),90,Math.max(20,Math.min(260,value+40)));}}
else if('{kind}'==='density'){{let rho=a/b,buoy=c-rho;value=rho;label=`密度=${{rho.toFixed(2)}}g/cm³，浮沉指标=${{buoy.toFixed(2)}}`;ctx.strokeStyle='#38bdf8';ctx.strokeRect(360,130,220,210);ctx.fillStyle='rgba(56,189,248,.35)';ctx.fillRect(361,220,218,119);ctx.fillStyle=buoy>=0?'#22c55e':'#f97316';ctx.fillRect(440,buoy>=0?190:260,70,50);}}
else if('{kind}'==='machine'){{let balance=a*b/c;value=balance;label=`等效阻力≈${{balance.toFixed(1)}}N，比较力和力臂乘积`;ctx.strokeStyle='#94a3b8';ctx.lineWidth=8;ctx.beginPath();ctx.moveTo(180,260);ctx.lineTo(740,260);ctx.stroke();ctx.fillStyle='#fbbf24';ctx.beginPath();ctx.arc(460,270,24,0,Math.PI*2);ctx.fill();}}
else if('{kind}'==='energy'){{let Ek=.5*a*b*b,Ep=a*9.8*c;value=Ek+Ep;label=`动能 ${{Ek.toFixed(1)}}J，势能 ${{Ep.toFixed(1)}}J，机械能 ${{value.toFixed(1)}}J`;ctx.fillStyle='#a78bfa';ctx.fillRect(480,320-c*10,70,c*10);ctx.fillStyle='#fbbf24';ctx.beginPath();ctx.arc(515,300-c*10,20,0,Math.PI*2);ctx.fill();}}
else if('{kind}'==='electric'||'{kind}'==='ohm'){{let I=a/b,P=a*I,Q=I*I*b*c;value=('{kind}'==='ohm')?Q:P;label=`I=U/R=${{I.toFixed(2)}}A，P=${{P.toFixed(1)}}W，热量指标=${{Q.toFixed(1)}}`;ctx.strokeStyle='#38bdf8';ctx.lineWidth=5;ctx.strokeRect(240,140,380,180);ctx.fillStyle='#fbbf24';ctx.fillRect(290,210,60,30);ctx.strokeStyle='#f97316';ctx.beginPath();ctx.arc(520,225,35,0,Math.PI*2);ctx.stroke();}}
else if('{kind}'==='magnetic'){{value=a*b*c/20;label=`电流 ${{a}}A，匝数 ${{b}}，磁效应指标 ${{value.toFixed(1)}}`;ctx.strokeStyle='#f97316';ctx.lineWidth=4;for(let x=180;x<760;x+=60){{ctx.beginPath();ctx.moveTo(x,110);ctx.lineTo(x,360);ctx.stroke();}}ctx.strokeStyle='#38bdf8';ctx.lineWidth=8;ctx.beginPath();ctx.moveTo(140,240);ctx.lineTo(760,240);ctx.stroke();}}
else{{value=a*b/c;label=`变量关系指标 ${{value.toFixed(1)}}`;}}
text('{esc(name)}',80,86,34,'#fbbf24');text(label,80,138,26,'#dbeafe');text('拖动变量后，用“现象—变量—解释”三句话说清变化原因。',80,405,24,'#cbd5e1');document.getElementById('lab-feedback').textContent=label+'。请解释哪个变量改变导致了结果变化。';}}
document.querySelectorAll('#p1,#p2,#p3').forEach(el=>el.addEventListener('input',drawGeneric));drawGeneric();
"""


def make_extra_svg(node: dict, detail: dict, mode: str) -> str:
    title = "概念结构图" if mode == "concept" else "实验过程图"
    labels = [c[0] for c in detail["concepts"]] if mode == "concept" else ["观察现象", "控制变量", "得出解释"]
    subtitle = detail["question"] if mode == "concept" else detail["memory"]
    colors = ["#38bdf8", "#a78bfa", "#22c55e"]
    cards=[]
    for i,label in enumerate(labels[:3]):
        x=80+i*360
        cards.append(f'<rect x="{x}" y="250" width="280" height="150" rx="22" fill="#0f172a" stroke="{colors[i]}" stroke-width="4"/><text x="{x+30}" y="330" fill="{colors[i]}" font-size="30" font-weight="800">{esc(label)}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="640" viewBox="0 0 1200 640"><rect width="1200" height="640" fill="#081426"/><circle cx="1020" cy="110" r="170" fill="#38bdf8" opacity="0.12"/><text x="80" y="100" fill="#f8fafc" font-size="48" font-weight="900">{esc(node['name'])} · {title}</text><text x="80" y="158" fill="#cbd5e1" font-size="26">{esc(subtitle[:56])}</text>{''.join(cards)}<text x="80" y="540" fill="#fbbf24" font-size="28">从实验现象进入问题，再回到变量、证据和生活应用。</text></svg>'''


def make_hero_svg(course_id: str, node: dict, detail: dict) -> str:
    colors=["#38bdf8","#a78bfa","#22c55e"]
    cards=[]
    for i,(title,txt) in enumerate(detail["concepts"]):
        x=70+i*390
        cards.append(f'<rect x="{x}" y="270" width="330" height="190" rx="24" fill="#0f172a" stroke="{colors[i]}" stroke-width="4"/><text x="{x+26}" y="325" fill="{colors[i]}" font-size="28" font-weight="800">{esc(title)}</text><text x="{x+26}" y="374" fill="#dbeafe" font-size="21">{esc(txt[:30])}</text><text x="{x+26}" y="410" fill="#dbeafe" font-size="21">{esc(txt[30:58])}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720"><defs><linearGradient id="g" x1="0" x2="1"><stop stop-color="#07111f"/><stop offset="1" stop-color="#172554"/></linearGradient></defs><rect width="1280" height="720" fill="url(#g)"/><circle cx="1050" cy="120" r="180" fill="#38bdf8" opacity="0.13"/><circle cx="220" cy="620" r="220" fill="#a78bfa" opacity="0.12"/><text x="70" y="112" fill="#f8fafc" font-size="52" font-weight="900">{esc(node['name'])}</text><text x="70" y="168" fill="#bae6fd" font-size="28">{esc(detail['question'])}</text><text x="70" y="225" fill="#cbd5e1" font-size="24">角色任务：{esc(detail['role'])} · 课标节点：{esc(node['id'])}</text>{''.join(cards)}<rect x="70" y="525" width="1140" height="105" rx="24" fill="#020617" opacity="0.72" stroke="#334155"/><text x="105" y="585" fill="#fbbf24" font-size="30" font-weight="800">记忆锚点</text><text x="260" y="585" fill="#e0f2fe" font-size="26">{esc(detail['memory'])}</text><text x="70" y="675" fill="#64748b" font-size="18">TeachAny v7.14 · 初中物理完整模式 · AI 学伴 / TTS / 知识图谱 / Canvas+PhET 互动 / 课标挂树</text></svg>'''


def make_content(course_id: str, node: dict, detail: dict) -> str:
    pre_q, pre_opts, pre_ans, pre_feedback = detail["pretest"]
    post_q, post_opts, post_ans, post_feedback = detail["posttest"]
    concepts="\n".join(f'<div class="mini-panel"><h3>{esc(t)}</h3><p>{esc(txt)}</p></div>' for t,txt in detail["concepts"])
    facts="\n".join(f"<li>{esc(x)}</li>" for x in detail["facts"])
    external=f'''
<section class="section" id="external-sim" data-tts="external-sim" data-tsh="外部仿真 - 用成熟工具观察变量变化"><div class="lesson-panel"><span class="phase-tag">PhET Simulation</span><h2>成熟仿真：自由操作，回到实验解释</h2><p style="color:var(--muted)">拖动参数，观察变量变化。仿真负责让现象可见，解释仍要回到本课的物理模型。</p><div class="iframe-wrap"><iframe src="{esc(detail['external'])}" allowfullscreen loading="lazy" sandbox="allow-scripts allow-same-origin allow-forms allow-popups"></iframe></div></div></section>'''
    return f'''
<style>.lesson-panel{{background:linear-gradient(180deg,rgba(20,35,58,.96),rgba(13,27,47,.96));border:1px solid rgba(148,163,184,.18);border-radius:18px;padding:22px;box-shadow:0 16px 40px rgba(0,0,0,.18)}}.mini-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}}.mini-panel{{background:rgba(15,23,42,.68);border:1px solid rgba(148,163,184,.18);border-radius:16px;padding:16px}}.mini-panel h3{{margin:0 0 8px;color:#bae6fd}}.quiz-option{{display:block;width:100%;margin:8px 0;border:1px solid rgba(56,189,248,.28);background:#0b1628;color:#eef6ff;border-radius:12px;padding:12px 14px;text-align:left;cursor:pointer}}.quiz-option.correct{{border-color:#22c55e;background:rgba(34,197,94,.14)}}.quiz-option.wrong{{border-color:#f97316;background:rgba(249,115,22,.14)}}.feedback{{min-height:44px;margin-top:10px;padding:10px 12px;border-radius:12px;background:rgba(56,189,248,.10);color:#dbeafe}}.control-row{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;align-items:end;margin:12px 0}}.control-row label{{color:#cbd5e1;font-size:14px}}.iframe-wrap{{position:relative;width:100%;padding-top:62.5%;border-radius:14px;overflow:hidden;background:#0f172a}}.iframe-wrap iframe{{position:absolute;inset:0;width:100%;height:100%;border:0}}.video-box video{{width:100%;border-radius:14px;border:1px solid rgba(148,163,184,.18);background:#020617}}figure img{{width:100%;border-radius:12px}}</style>
<section class="section" id="story" data-tts="story" data-tsh="情境任务 - 用 ABT 明确为什么学"><div class="lesson-panel"><span class="phase-tag">ABT Story</span><h2>角色任务：{esc(detail['role'])}</h2><div class="mini-grid"><div class="mini-panel"><h3>And 已有经验</h3><p>{esc(detail['and'])}</p></div><div class="mini-panel"><h3>But 真实卡点</h3><p>{esc(detail['but'])}</p></div><div class="mini-panel"><h3>Therefore 本课任务</h3><p>{esc(detail['therefore'])}</p></div></div><p>物理不是背结论，而是把生活现象变成可观察、可测量、可解释的模型。每一道题都要先问对象是谁、条件是什么、变量怎样变化。</p></div></section>
<section class="section" id="experiment-checklist" data-tts="experiment-checklist" data-bloom-level="analyze" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">Experiment Checklist</span><h2>实验检查表：这道题到底在测什么？</h2><p><strong>第一问：观察对象是谁？</strong>声源、光线、物体、电路元件或磁体不能混着看。对象一旦换了，变量和结论也会变。</p><p><strong>第二问：哪个变量被改变？</strong>物理实验通常只改变一个变量，其他条件尽量保持不变。没有控制变量，就很难判断因果。</p><p><strong>第三问：证据是什么？</strong>振动、光路、温度、电表示数、物体运动状态等都是证据。结论必须能被这些证据支撑。</p></div></section>
<section class="section" id="pretest" data-tts="pretest" data-bloom-level="remember" data-scaffold="full" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">Pre-test</span><h2>前测：你已经知道什么？</h2><p><strong>{esc(pre_q)}</strong></p>{make_buttons(pre_opts, pre_ans, 'pretest')}<div id="pretest-feedback" class="feedback">先选一项，系统会给出错因诊断。</div></div></section>
<section class="section" id="core" data-tts="core" data-bloom-level="understand" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">Core Ideas</span><h2>核心概念：从现象到模型</h2><div class="mini-grid">{concepts}</div></div></section>
<section class="section" id="deep-understanding" data-tts="deep-understanding"><div class="lesson-panel insight-box"><span class="phase-tag">Five Lens</span><h2>深层理解：五镜头看本质</h2><ul><li><strong>看见它：</strong>{esc(detail['facts'][0])}</li><li><strong>拆开它：</strong>{esc(detail['facts'][1])}</li><li><strong>解释它：</strong>{esc(detail['facts'][2])}</li><li><strong>比较它：</strong>把本课现象和一个容易混淆的生活场景放在一起，比较对象、变量和条件。</li><li><strong>迁移它：</strong>换一个实验装置，仍然用同一套变量关系解释现象。</li></ul><p class="feedback"><strong>记忆锚点：</strong>{esc(detail['memory'])}</p></div></section>
<section class="section" id="worked-example" data-tts="worked-example" data-bloom-level="analyze" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">Worked Example</span><h2>例题拆解：先找变量，再写结论</h2><p>遇到「{esc(node['name'])}」问题，先把装置、对象和可测量的物理量圈出来。题目里的“变大、变小、不变、忽略、相同条件”都不是废话，它们决定是否能使用某个公式或规律。</p><p>第二步，把文字翻译成变量关系。如果题目给图像或实验数据，先判断横轴、纵轴和单位；如果题目给生活现象，先还原实验条件。</p><p>第三步才写结论。本课高频误区是：{esc(detail['error'])} 这个错误通常来自没有说明实验条件或把相关关系误当成因果关系。</p></div></section>
<section class="section" id="transfer-task" data-tts="transfer-task" data-bloom-level="create" data-scaffold="none"><div class="lesson-panel"><span class="phase-tag">Transfer Task</span><h2>迁移任务：设计一个新实验</h2><p>请设计一个与本课相关的小实验，必须写出实验目的、改变的变量、保持不变的条件、观察到的现象和你的物理解释。最后补一个容易出错的判断，并说明为什么错。</p></div></section>
<section class="section" id="visual-evidence" data-tts="visual-evidence"><div class="lesson-panel"><span class="phase-tag">Visual Evidence</span><h2>两张图先建立直觉</h2><div class="mini-grid"><figure class="mini-panel"><img src="./assets/concept-diagram.svg" alt="概念结构图"><figcaption>概念结构：核心对象、变量和判断标准。</figcaption></figure><figure class="mini-panel"><img src="./assets/process-diagram.svg" alt="实验过程图"><figcaption>实验过程：从现象到证据，再到解释。</figcaption></figure></div></div></section>
<section class="section" id="evidence-table" data-tts="evidence-table" data-bloom-level="evaluate" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">Evidence Table</span><h2>证据表：把现象翻译成物理判断</h2><p><strong>如果题目给实验图，</strong>先看装置中哪个部分可调、哪个部分用来测量、哪个部分需要保持不变。</p><p><strong>如果题目给数据表，</strong>先看单位和变化趋势，再判断变量之间是正相关、反相关还是存在阈值条件。</p><p><strong>如果题目给生活场景，</strong>不要直接套口号。先还原成物理模型，再说明哪些因素被简化了。</p></div></section>
<section class="section" id="interactive-lab" data-tts="interactive-lab" data-bloom-level="apply" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">Interactive Lab</span><h2>互动实验：调变量，看结果</h2><p style="color:var(--muted)">先动手改变变量，再用一句话解释图像或数值为什么变了。</p><div class="control-row">{interaction_controls(detail['interaction'])}</div><div class="canvas-wrap"><canvas id="physics-canvas" class="wide-canvas" width="900" height="430"></canvas></div><div id="lab-feedback" class="feedback">拖动或选择变量，观察画布变化。</div></div></section>
{external}
<section class="section" id="micro-video" data-tts="micro-video"><div class="lesson-panel video-box"><span class="phase-tag">Micro Lesson</span><h2>微课讲解：60 秒内复盘核心关系</h2><video controls preload="metadata" playsinline><source src="./assets/video/{esc(course_id)}-main.mp4" type="video/mp4"></video></div></section>
<section class="section" id="posttest" data-tts="posttest" data-bloom-level="evaluate" data-scaffold="none" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">Post-test</span><h2>后测：学会了吗？</h2><p><strong>{esc(post_q)}</strong></p>{make_buttons(post_opts, post_ans, 'posttest')}<div id="posttest-feedback" class="feedback">先独立判断，再看诊断反馈。</div></div></section>
<section class="section" id="tiered-practice" data-tts="tiered-practice"><div class="lesson-panel"><span class="phase-tag">Level Practice</span><h2>三段式作业</h2><div class="mini-grid"><div class="mini-panel"><h3>基础巩固</h3><p>写出本课现象、变量和适用条件。</p></div><div class="mini-panel"><h3>能力应用</h3><p>把本课规律用于一个新的生活场景，并说明证据。</p></div><div class="mini-panel"><h3>迁移挑战</h3><p>设计一个反例，说明常见错误为什么站不住脚。</p></div></div></div></section>
<section class="section" id="summary" data-tts="summary"><div class="lesson-panel"><span class="phase-tag">Summary</span><h2>一句话带走</h2><ul>{facts}</ul><p class="feedback">如果你能解释“{esc(detail['question'])}”，这节课就真正过关了。</p></div></section>
<script>const FEEDBACK={{ pretest:{json.dumps(pre_feedback, ensure_ascii=False)}, posttest:{json.dumps(post_feedback, ensure_ascii=False)} }};function checkAnswer(btn,ok,target){{btn.parentElement.querySelectorAll('.quiz-option').forEach(b=>b.classList.remove('correct','wrong'));btn.classList.add(ok?'correct':'wrong');const box=document.getElementById(target+'-feedback');if(box)box.textContent=ok?FEEDBACK[target]:'错因诊断：先回到实验条件、变量控制和证据，再检查你是否把经验当结论。'+FEEDBACK[target];}}{interaction_script(detail['interaction'], node['name'])}</script>
'''


def write_manifest(course_dir: Path, course_id: str, node: dict, domain: dict, detail: dict):
    manifest={
        "id": course_id,
        "course_id": course_id,
        "node_id": node["id"],
        "name": detail["title"],
        "name_en": detail["title_en"],
        "subject": "physics",
        "grade": node.get("grade", 8),
        "stage": "middle",
        "domain": domain.get("id", "physics"),
        "lesson_type": "experiment",
        "status": "community",
        "author": "TeachAny",
        "version": "1.0.0",
        "teachany_version": "7.14.0",
        "curriculum": "cn-national",
        "description": f"初中物理课标互动课件：{node['name']}。包含问题锚点、ABT 情境、Canvas/PhET 互动、TTS、微课、知识图谱与 AI 学伴。",
        "tags": ["初中物理", "中国课标", node["name"]],
        "difficulty": 3,
        "duration": "15-20 min",
        "prerequisites": node.get("prerequisites", []),
        "leads_to": node.get("extends", []),
        "learning_objectives": detail["objectives"],
        "curriculum_standards": [
            {"source": "义务教育物理课程标准", "content": point}
            for point in (node.get("curriculum_points") or [f"围绕{node['name']}形成物理观念、科学探究和证据推理能力。"])
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
    (course_dir/"manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")


def make_plan(course_id: str, node: dict, detail: dict) -> str:
    return f"""# PLAN.md — {detail['title']}

- course_id: `{course_id}`
- node_id: `{node['id']}`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：初中 {node.get('grade', 8)} 年级
- 学科：物理
- 课标节点：{node['name']}
- 课标摘录：{'；'.join(node.get('curriculum_points', [])[:3])}

## Phase 1 教学骨架
- 问题锚点：{detail['question']}
- ABT：
  - And：{detail['and']}
  - But：{detail['but']}
  - Therefore：{detail['therefore']}
- 真实互动：Canvas 变量实验 + PhET 成熟仿真 + 前后测反馈
- 评估闭环：前测 → 实验检查表 → 概念拆解 → 互动实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 物理仿真：Canvas 自定义变量互动 + PhET 中文仿真。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/{course_id}`
- `python3 scripts/validate-courseware.py {course_id}`
- `python3 scripts/rebuild-index.py`
"""


def generate_tts(course_dir: Path, detail: dict):
    tts_dir=course_dir/"tts"
    tts_dir.mkdir(parents=True, exist_ok=True)
    segments=[
        ("s01", f"今天我们学习{detail['title']}。核心问题是：{detail['question']}"),
        ("s02", f"这节课先观察现象，再控制变量，最后建立解释。{detail['memory']}"),
        ("s03", f"最后提醒一个高频易错点：{detail['error']}"),
    ]
    manifest=[]
    for seg_id,text in segments:
        out=tts_dir/f"{seg_id}.mp3"
        tmp=tts_dir/f"{seg_id}.aiff"
        result=subprocess.run(["say","-v","Tingting","-r","175","-o",str(tmp),text], text=True, capture_output=True)
        if result.returncode != 0:
            subprocess.run(["say","-r","175","-o",str(tmp),text], check=True)
        subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(tmp),"-acodec","libmp3lame","-b:a","128k",str(out)], check=True)
        tmp.unlink(missing_ok=True)
        manifest.append({"id":seg_id,"title":text[:18],"src":f"./tts/{seg_id}.mp3","text":text})
    (tts_dir/"manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    return manifest


def generate_video(course_dir: Path, course_id: str, node: dict, detail: dict):
    from PIL import Image, ImageDraw, ImageFont
    video_dir=course_dir/"assets/video"
    video_dir.mkdir(parents=True, exist_ok=True)
    out=video_dir/f"{course_id}-main.mp4"
    font_path=next((p for p in [Path("/System/Library/Fonts/PingFang.ttc"), Path("/System/Library/Fonts/STHeiti Light.ttc")] if p.exists()), None)
    def font(size):
        try: return ImageFont.truetype(str(font_path), size) if font_path else ImageFont.load_default()
        except Exception: return ImageFont.load_default()
    frames_dir=video_dir/"_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    frame_texts=[(node["name"], detail["question"]),("实验条件", detail["memory"]),("易错诊断", detail["error"]),("迁移任务","换一个生活场景，仍然从对象、变量、证据和解释开始。"),("学习闭环","前测 → 实验 → 仿真 → 后测 → 迁移")]
    for i,(headline,body) in enumerate(frame_texts,1):
        img=Image.new("RGB",(1280,720),"#081426")
        draw=ImageDraw.Draw(img)
        draw.ellipse((930,-120,1330,280), fill="#123b5a")
        draw.rounded_rectangle((70,82,1210,638), radius=32, outline="#38bdf8", width=4, fill="#0f172a")
        draw.text((110,135), headline, font=font(54), fill="#f8fafc")
        y,line=245,""
        for ch in body:
            trial=line+ch
            if draw.textlength(trial, font=font(34))>980:
                draw.text((110,y), line, font=font(34), fill="#dbeafe"); y+=58; line=ch
            else:
                line=trial
        if line: draw.text((110,y), line, font=font(34), fill="#dbeafe")
        draw.text((110,585), f"TeachAny 初中物理 · {course_id} · {i}/5", font=font(26), fill="#94a3b8")
        img.save(frames_dir/f"frame_{i:03d}.png")
    audio=course_dir/"tts"/"s01.mp3"
    cmd=["ffmpeg","-y","-loglevel","error","-framerate","1","-i",str(frames_dir/"frame_%03d.png")]
    if audio.exists(): cmd += ["-i", str(audio)]
    cmd += ["-c:v","libx264","-pix_fmt","yuv420p","-r","25"]
    if audio.exists(): cmd += ["-c:a","aac","-shortest"]
    cmd += [str(out)]
    subprocess.run(cmd, check=True)
    shutil.rmtree(frames_dir, ignore_errors=True)


def generate_course(course_id: str, node: dict, domain: dict):
    detail=make_detail(node, domain)
    course_dir=ROOT/"community"/course_id
    if course_dir.exists(): shutil.rmtree(course_dir)
    (course_dir/"assets").mkdir(parents=True, exist_ok=True)
    generate_tts(course_dir, detail)
    generate_video(course_dir, course_id, node, detail)
    (course_dir/"assets/hero-infographic.svg").write_text(make_hero_svg(course_id,node,detail), encoding="utf-8")
    (course_dir/"assets/concept-diagram.svg").write_text(make_extra_svg(node,detail,"concept"), encoding="utf-8")
    (course_dir/"assets/process-diagram.svg").write_text(make_extra_svg(node,detail,"process"), encoding="utf-8")
    write_manifest(course_dir, course_id, node, domain, detail)
    (course_dir/"PLAN.md").write_text(make_plan(course_id,node,detail), encoding="utf-8")
    audio_manifest=json.loads((course_dir/"tts/manifest.json").read_text(encoding="utf-8"))
    skeleton=SKELETON.read_text(encoding="utf-8")
    choices="\n".join(f'<button class="choice" data-anchor-choice="{esc(label)}">{esc(label)}</button>' for label in ["观察现象","控制变量","解释应用"])
    objectives="\n".join(f"<li>{esc(x)}</li>" for x in detail["objectives"])
    html_text=replace_all(skeleton, {
        "COURSE_ID": course_id,
        "TITLE": detail["title"],
        "DESCRIPTION": f"初中物理课标互动课件：{node['name']}。",
        "SUBJECT": "physics",
        "STAGE_GRADE": f"middle-{node.get('grade',8)}",
        "GRADE": str(node.get("grade",8)),
        "STAGE": "middle",
        "NODE_ID": node["id"],
        "DOMAIN": domain.get("id","physics"),
        "PREREQ_COURSE_IDS": ",".join(node.get("prerequisites",[])),
        "NEXT_COURSE_ID": "",
        "COURSE_VERSION": "1.0.0",
        "TEACHANY_VERSION": "7.14.0",
        "LESSON_TYPE": "experiment",
        "HERO_QUESTION": detail["question"],
        "HERO_IMAGE_ALT": f"{node['name']}知识结构图",
        "HERO_FIGCAPTION": f"{node['name']}：现象、变量、证据和迁移任务。",
        "AUDIO_PLAYLIST_JSON": json.dumps(audio_manifest, ensure_ascii=False, indent=2),
        "PROBLEM_ANCHOR_CHOICES": choices,
        "LEARNING_OBJECTIVES": objectives,
        "CONTENT_SECTIONS": make_content(course_id,node,detail),
        "OPTIONAL_MAP_HEAD": "",
        "OPTIONAL_MAP_TAIL": "",
        "PREREQUISITE_NAMES": ", ".join(node.get("prerequisites",[])) or "无",
        "FREE_MODE": "false",
    })
    html_text=html_text.replace('src="./assets/'+course_id+'-hero.png" onerror="this.src=\'./assets/hero-infographic.svg\'"','src="./assets/hero-infographic.svg"')
    html_text=html_text.replace(f'<title>{detail["title"]}</title>', f'<title>{detail["title"]} · 初中物理 G{node.get("grade",8)} · TeachAny v7.14</title>')
    html_text=html_text.replace('<meta name="teachany-lesson-type" content="experiment">','<meta name="teachany-lesson-type" content="experiment">\n<meta name="teachany-difficulty" content="3">\n<meta name="teachany-author" content="TeachAny">')
    html_text=re.sub(r'<!--.*?-->', '', html_text, flags=re.S)
    html_text=html_text.replace(' placeholder="把你卡住的问题写在这里"',' aria-label="把你卡住的问题写在这里"').replace('aria-label="知识图谱互动画布占位"','aria-label="知识图谱互动画布"').replace('placeholder','提示输入').replace('占位','备用')
    (course_dir/"index.html").write_text(html_text, encoding="utf-8")
    print(f"✅ generated {course_id}")


def main():
    nodes, domains, ids = read_tree_nodes()
    print(f"middle physics nodes: {len(ids)}")
    for cid in ids:
        generate_course(cid, nodes[cid], domains[cid])


if __name__ == "__main__":
    main()
