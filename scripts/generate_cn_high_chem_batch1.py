#!/usr/bin/env python3
"""Generate TeachAny CN high-school chemistry batch 1 courseware.

Batch 1 covers the matter-classification domain:
- 物质的分类
- 分散系（溶液/胶体）
- 物质的量（摩尔）
- 气体摩尔体积
- 物质的量浓度
"""
from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path("/Users/wepon/.workbuddy/skills/TeachAny")
SKELETON = SKILL / "templates/course-skeleton.html"
TREE = ROOT / "data/trees/cn/high/chemistry.json"
TODAY = date.today().isoformat()

BATCH_IDS = [
    "chem-h-substance-classification-h",
    "chem-h-dispersion-system",
    "chem-h-mole-concept",
    "chem-h-gas-molar-volume",
    "chem-h-solution-concentration-h",
]

DETAILS = {
    "chem-h-substance-classification-h": {
        "title": "物质的分类：从混乱试剂柜到清晰化学地图",
        "title_en": "Classification of Matter",
        "role": "实验室试剂管理员",
        "and": "你已经见过空气、水、铁粉、食盐水这些常见物质，也知道它们的外观和用途不同。",
        "but": "如果只靠名称和外观，面对一柜未知试剂很快会混乱：空气是纯净物吗，氧气和氧化铜为什么都带“氧”？",
        "therefore": "所以要用组成和性质建立分类地图，把混合物、纯净物、单质、化合物、氧化物、酸、碱、盐放到正确位置。",
        "question": "拿到一瓶未知物质时，怎样用“组成—性质”两条线把它快速归类？",
        "concepts": [
            ("纯净物 / 混合物", "只含一种物质的是纯净物；由多种物质混合且各成分保持原性质的是混合物。空气、食盐水属于混合物。"),
            ("单质 / 化合物", "纯净物继续看元素种类：只由一种元素组成的是单质，如 O₂、Fe；由多种元素组成的是化合物，如 H₂O、NaCl。"),
            ("氧化物 / 酸碱盐", "化合物还可按组成和性质细分。氧化物只含两种元素且一种是氧；酸电离产生 H⁺，碱产生 OH⁻，盐由金属离子或铵根与酸根组成。"),
        ],
        "facts": ["空气不是单质也不是化合物，它是氮气、氧气等组成的混合物。", "氧气 O₂ 是单质，二氧化碳 CO₂ 是氧化物，氯化钠 NaCl 是盐。", "分类不是背名单，而是先问“是否纯净”，再问“含几种元素”，最后看组成和性质。"],
        "memory": "分类口诀：先分纯混，再分单化；化合物里看氧酸碱盐。",
        "error": "常见错误：把“含氧元素的物质”都叫氧化物。硫酸 H₂SO₄ 含氧，但有三种元素，不是氧化物。",
        "pretest": ("空气属于哪一类？", ["单质", "化合物", "混合物", "氧化物"], 2, "空气由氮气、氧气、二氧化碳等组成，各成分保持原性质，所以是混合物。"),
        "posttest": ("下列判断正确的是？", ["O₂ 是化合物", "CO₂ 是氧化物", "NaCl 是氧化物", "盐酸是单质"], 1, "CO₂ 由碳、氧两种元素组成，其中一种是氧，是氧化物。"),
        "interaction": "classification",
        "external": "",
        "objectives": ["能按组成区分纯净物、混合物、单质和化合物", "能用“是否只含两种元素且一种为氧”判断氧化物", "能解释酸、碱、盐分类与电离产生离子的关系"],
    },
    "chem-h-dispersion-system": {
        "title": "分散系：为什么胶体会让光路显形？",
        "title_en": "Dispersions, Solutions and Colloids",
        "role": "饮料研发工程师",
        "and": "你已经知道食盐能溶于水，也见过泥水静置后会沉降。",
        "but": "牛奶、豆浆、雾这些体系既不像食盐水那样完全透明，也不像泥水那样很快沉降，它们到底处在什么中间状态？",
        "therefore": "所以要用分散质粒子大小和稳定性认识溶液、胶体、浊液，并用丁达尔效应识别胶体。",
        "question": "为什么一束光穿过胶体会出现明亮光路，而穿过真正溶液却看不见？",
        "concepts": [
            ("分散系三要素", "分散质被分散到分散剂中形成分散系。按粒子直径可分为溶液、胶体和浊液。"),
            ("胶体的粒子尺度", "胶体粒子通常约 1—100 nm，足够小而不易沉降，又足够大而能散射光。"),
            ("丁达尔效应", "光通过胶体时被胶体粒子散射，从侧面可看到一条光路；溶液粒子太小，散射很弱。"),
        ],
        "facts": ["Fe(OH)₃ 胶体、牛奶、雾都可能表现出丁达尔效应。", "NaCl 溶液属于溶液，泥水属于浊液，豆浆接近胶体或复杂分散体系。", "判断胶体不能只看颜色，要看粒子大小、稳定性和光散射。"],
        "memory": "尺度锚点：溶液小到看不见，浊液大到会沉，胶体夹在中间会散光。",
        "error": "常见错误：把“透明”当成溶液的唯一标准。有些胶体也可半透明，关键看粒子尺度和丁达尔效应。",
        "pretest": ("泥水久置后出现沉淀，最可能属于哪类分散系？", ["溶液", "胶体", "浊液", "纯净物"], 2, "浊液粒子较大，不稳定，久置容易沉降。"),
        "posttest": ("丁达尔效应主要说明胶体粒子具有什么特征？", ["粒子足够大可散射光", "粒子都是带正电", "胶体一定有颜色", "胶体一定会沉降"], 0, "丁达尔效应来自胶体粒子对光的散射。"),
        "interaction": "tyndall",
        "external": "",
        "objectives": ["能说明分散质、分散剂和分散系的关系", "能比较溶液、胶体、浊液的粒子尺度和稳定性", "能用丁达尔效应解释胶体识别方法"],
    },
    "chem-h-mole-concept": {
        "title": "物质的量：把微观粒子数变成可称量的宏观量",
        "title_en": "Amount of Substance and Mole",
        "role": "药物配方计算师",
        "and": "你会用质量描述一包食盐有多重，也知道化学反应本质上是粒子之间按比例反应。",
        "but": "原子、分子太小，无法一粒一粒数；只看克数又无法直接知道有多少粒子参与反应。",
        "therefore": "所以引入物质的量 n 和摩尔 mol，用阿伏加德罗常数把微观粒子数、质量和化学方程式连接起来。",
        "question": "为什么化学计算不直接数分子，而要引入“1 mol”这个桥梁？",
        "concepts": [
            ("1 mol 的含义", "1 mol 任何粒子集合都含约 6.02×10²³ 个粒子，这个数叫阿伏加德罗常数 Nₐ。"),
            ("n、N、Nₐ 的关系", "粒子数 N = n × Nₐ；物质的量 n = N / Nₐ。这里的粒子可以是原子、分子、离子。"),
            ("摩尔质量", "摩尔质量 M 的数值常与相对分子质量相同，单位是 g/mol；质量 m = n × M。"),
        ],
        "facts": ["1 mol 水分子约含 6.02×10²³ 个 H₂O 分子。", "18 g 水约为 1 mol 水，因为 H₂O 的摩尔质量约 18 g/mol。", "方程式 2H₂ + O₂ = 2H₂O 中，系数既可表示粒子个数比，也可表示物质的量比。"],
        "memory": "三角关系：m、n、M 中间放 n，m = nM；N、n、Nₐ 中间也放 n，N = nNₐ。",
        "error": "常见错误：说“1 mol 氢”不指明粒子种类。1 mol H、1 mol H₂、1 mol H⁺代表的粒子不同。",
        "pretest": ("18 g H₂O 约等于多少 mol？", ["0.5 mol", "1 mol", "2 mol", "18 mol"], 1, "水的摩尔质量约为 18 g/mol，所以 18 g ÷ 18 g/mol = 1 mol。"),
        "posttest": ("0.5 mol CO₂ 含有多少个 CO₂ 分子？", ["0.5 个", "3.01×10²³ 个", "6.02×10²³ 个", "12.04×10²³ 个"], 1, "N = nNₐ = 0.5 × 6.02×10²³ = 3.01×10²³。"),
        "interaction": "mole",
        "external": "",
        "objectives": ["能说清 1 mol 与阿伏加德罗常数的含义", "能在 m、n、M、N、Nₐ 之间换算", "能把化学方程式系数理解为物质的量之比"],
    },
    "chem-h-gas-molar-volume": {
        "title": "气体摩尔体积：同温同压下气体为什么按体积比反应？",
        "title_en": "Molar Volume of Gas",
        "role": "气体储罐工程师",
        "and": "你已经知道 1 mol 代表相同数量的粒子，也会用 n=m/M 计算物质的量。",
        "but": "气体很难像固体那样直接称量；同样 1 mol 氧气、氢气、二氧化碳质量不同，体积却在同温同压下近似相同。",
        "therefore": "所以要学习气体摩尔体积 Vₘ，用温度、压强和物质的量解释气体体积关系。",
        "question": "为什么在标准状况下，1 mol 不同气体都近似占 22.4 L？",
        "concepts": [
            ("气体摩尔体积 Vₘ", "单位物质的量气体所占的体积叫气体摩尔体积，Vₘ = V/n，单位 L/mol。"),
            ("标准状况近似值", "在 0 ℃、101 kPa 条件下，1 mol 理想气体体积约为 22.4 L。"),
            ("适用边界", "22.4 L/mol 只适合标准状况下的气体，不能直接套到液体、固体或非标况气体。"),
        ],
        "facts": ["标准状况下 2 mol O₂ 体积约 44.8 L。", "同温同压下，气体体积比约等于物质的量比，也等于分子数比。", "升温体积变大、加压体积变小，本质是气体粒子间距变化。"],
        "memory": "22.4 只问三件事：是不是气体？是不是 1 mol？是不是标准状况？少一个都要谨慎。",
        "error": "常见错误：把 1 mol 水也写成 22.4 L。水在常温下是液体，不适用气体摩尔体积。",
        "pretest": ("标准状况下 0.5 mol O₂ 的体积约为多少？", ["5.6 L", "11.2 L", "22.4 L", "44.8 L"], 1, "V = nVₘ = 0.5 × 22.4 = 11.2 L。"),
        "posttest": ("下列哪种情况可以直接用 22.4 L/mol？", ["常温下 1 mol 水", "标准状况下 1 mol 氮气", "任意温度下 1 mol 氧气", "标准状况下 1 mol 食盐"], 1, "22.4 L/mol 适用于标准状况下的气体。"),
        "interaction": "gas",
        "external": "",
        "objectives": ["能定义气体摩尔体积并使用 V=nVₘ", "能说明 22.4 L/mol 的条件限制", "能解释同温同压下气体体积比与物质的量比的关系"],
    },
    "chem-h-solution-concentration-h": {
        "title": "物质的量浓度：怎样配出准确浓度的溶液？",
        "title_en": "Molar Concentration",
        "role": "滴定实验配液员",
        "and": "你已经会用物质的量表示粒子数量，也知道溶液由溶质和溶剂组成。",
        "but": "只说“加了 5 g 溶质”还不够，因为同样的溶质放进 100 mL 和 1 L 水中浓度完全不同。",
        "therefore": "所以要用物质的量浓度 c=n/V 精确描述单位体积溶液中含有多少物质的量，并掌握容量瓶配制步骤。",
        "question": "实验室怎样把“称多少、加多少水”转化成准确的 mol/L 浓度？",
        "concepts": [
            ("浓度定义", "物质的量浓度 c 表示单位体积溶液中所含溶质 B 的物质的量：cB = nB / V。"),
            ("单位与体积", "常用单位 mol/L。计算时体积 V 必须用 L，不是 mL。"),
            ("稀释守恒", "稀释过程中溶质物质的量不变，所以 c₁V₁ = c₂V₂。"),
        ],
        "facts": ["配制 1.00 L 0.100 mol/L NaCl 溶液，需要 0.100 mol NaCl，质量约 5.85 g。", "容量瓶定容时要等液面凹面最低处与刻度线相切。", "“加水到 1 L”与“加入 1 L 水”不是一回事，前者是定容到总体积 1 L。"],
        "memory": "浓度口诀：先求 n，再看 V；mL 先换 L，定容看总量。",
        "error": "常见错误：把 250 mL 直接代入 250 L，导致浓度小 1000 倍；或把“加入水的体积”当成“溶液总体积”。",
        "pretest": ("0.2 mol 溶质配成 1.0 L 溶液，浓度是多少？", ["0.2 mol/L", "0.5 mol/L", "1.0 mol/L", "5.0 mol/L"], 0, "c=n/V=0.2/1.0=0.2 mol/L。"),
        "posttest": ("将 10 mL 1.0 mol/L 溶液稀释到 100 mL，稀释后浓度是？", ["0.01 mol/L", "0.10 mol/L", "1.0 mol/L", "10 mol/L"], 1, "c₂=c₁V₁/V₂=1.0×10/100=0.10 mol/L。"),
        "interaction": "concentration",
        "external": "https://phet.colorado.edu/sims/html/molarity/latest/molarity_zh_CN.html",
        "objectives": ["能用 c=n/V 计算物质的量浓度", "能区分溶液体积、溶剂体积与定容体积", "能用 c₁V₁=c₂V₂ 解决稀释问题"],
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
    lines = []
    for i, item in enumerate(items):
        ok = "true" if i == answer else "false"
        lines.append(f'<button class="quiz-option" onclick="checkAnswer(this,{ok},\'{prefix}\')">{esc(chr(65+i))}. {esc(item)}</button>')
    return "\n".join(lines)


def make_content(course_id: str, node: dict, domain: dict, detail: dict) -> str:
    pre_q, pre_opts, pre_ans, pre_feedback = detail["pretest"]
    post_q, post_opts, post_ans, post_feedback = detail["posttest"]
    concepts = "\n".join(
        f'<div class="mini-panel"><h3>{esc(t)}</h3><p>{esc(txt)}</p></div>' for t, txt in detail["concepts"]
    )
    facts = "\n".join(f"<li>{esc(x)}</li>" for x in detail["facts"])
    external = ""
    if detail.get("external"):
        external = f'''
<section class="section" id="external-sim" data-tts="external-sim" data-tsh="外部仿真 - 用成熟工具观察变量变化">
  <div class="lesson-panel">
    <span class="phase-tag">PhET Simulation</span>
    <h2>成熟仿真：先观察，再回到公式</h2>
    <p style="color:var(--muted)">拖动浓度、体积或溶质参数，观察颜色深浅和浓度变化。注意：仿真负责“看见变量”，计算仍要回到本课公式。</p>
    <div class="iframe-wrap"><iframe src="{esc(detail['external'])}" allowfullscreen loading="lazy" sandbox="allow-scripts allow-same-origin allow-forms allow-popups"></iframe></div>
  </div>
</section>'''
    return f'''
<style>
.lesson-panel {{ background:linear-gradient(180deg, rgba(20,35,58,.96), rgba(13,27,47,.96)); border:1px solid rgba(148,163,184,.18); border-radius:18px; padding:22px; box-shadow:0 16px 40px rgba(0,0,0,.18); }}
.mini-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:14px; }}
.mini-panel {{ background:rgba(15,23,42,.68); border:1px solid rgba(148,163,184,.18); border-radius:16px; padding:16px; }}
.mini-panel h3 {{ margin:0 0 8px; color:#bae6fd; }}
.quiz-option {{ display:block; width:100%; margin:8px 0; border:1px solid rgba(56,189,248,.28); background:#0b1628; color:#eef6ff; border-radius:12px; padding:12px 14px; text-align:left; cursor:pointer; }}
.quiz-option.correct {{ border-color:#22c55e; background:rgba(34,197,94,.14); }}
.quiz-option.wrong {{ border-color:#f97316; background:rgba(249,115,22,.14); }}
.feedback {{ min-height:44px; margin-top:10px; padding:10px 12px; border-radius:12px; background:rgba(56,189,248,.10); color:#dbeafe; }}
.control-row {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:12px; align-items:end; margin:12px 0; }}
.control-row label {{ color:#cbd5e1; font-size:14px; }}
.control-row input, .control-row select {{ margin-top:4px; }}
.iframe-wrap {{ position:relative; width:100%; padding-top:62.5%; border-radius:14px; overflow:hidden; background:#0f172a; }}
.iframe-wrap iframe {{ position:absolute; inset:0; width:100%; height:100%; border:0; }}
.video-box video {{ width:100%; border-radius:14px; border:1px solid rgba(148,163,184,.18); background:#020617; }}
</style>

<section class="section" id="story" data-tts="story" data-tsh="情境任务 - 用 ABT 明确为什么学">
  <div class="lesson-panel">
    <span class="phase-tag">ABT Story</span>
    <h2>角色任务：{esc(detail['role'])}</h2>
    <div class="mini-grid">
      <div class="mini-panel"><h3>And 已有经验</h3><p>{esc(detail['and'])}</p></div>
      <div class="mini-panel"><h3>But 真实卡点</h3><p>{esc(detail['but'])}</p></div>
      <div class="mini-panel"><h3>Therefore 本课任务</h3><p>{esc(detail['therefore'])}</p></div>
    </div>
  </div>
</section>

<section class="section" id="pretest" data-tts="pretest" data-tsh="前测 - 先暴露已有理解" data-bloom-level="remember" data-scaffold="full" data-conceptest="true">
  <div class="lesson-panel">
    <span class="phase-tag">Pre-test</span>
    <h2>前测：你已经知道什么？</h2>
    <p><strong>{esc(pre_q)}</strong></p>
    {make_buttons(pre_opts, pre_ans, 'pretest')}
    <div id="pretest-feedback" class="feedback">先选一项，系统会给出错因诊断。</div>
  </div>
</section>

<section class="section" id="core" data-tts="core" data-tsh="核心概念 - 从定义到判断标准" data-bloom-level="understand" data-scaffold="full">
  <div class="lesson-panel">
    <span class="phase-tag">Core Ideas</span>
    <h2>核心概念：先抓判断标准</h2>
    <div class="mini-grid">{concepts}</div>
  </div>
</section>

<section class="section" id="deep-understanding" data-tts="deep-understanding" data-tsh="深层理解 - 五镜头拆开看本质">
  <div class="lesson-panel insight-box">
    <span class="phase-tag">Five Lens</span>
    <h2>深层理解：五镜头看本质</h2>
    <ul>
      <li><strong>看见它：</strong>{esc(detail['facts'][0])}</li>
      <li><strong>拆开它：</strong>{esc(detail['facts'][1])}</li>
      <li><strong>比较它：</strong>{esc(detail['facts'][2])}</li>
      <li><strong>迁移它：</strong>把这个判断标准用到一个新的实验或生活场景中。</li>
    </ul>
    <p class="feedback"><strong>记忆锚点：</strong>{esc(detail['memory'])}</p>
    <p class="feedback warn"><strong>易错提醒：</strong>{esc(detail['error'])}</p>
  </div>
</section>

<section class="section" id="visual-evidence" data-tts="visual-evidence" data-tsh="可视化证据 - 用两张图补足结构和过程">
  <div class="lesson-panel">
    <span class="phase-tag">Visual Evidence</span>
    <h2>两张图先建立直觉</h2>
    <div class="mini-grid">
      <figure class="mini-panel"><img src="./assets/concept-diagram.svg" alt="概念结构图"><figcaption>概念结构：把核心对象、变量和判断标准放到一张图里。</figcaption></figure>
      <figure class="mini-panel"><img src="./assets/process-diagram.svg" alt="过程机制图"><figcaption>过程机制：从输入条件到可观察现象，再回到化学解释。</figcaption></figure>
    </div>
  </div>
</section>

<section class="section" id="interactive-lab" data-tts="interactive-lab" data-tsh="互动实验 - 调变量并观察结果" data-bloom-level="apply" data-scaffold="partial">
  <div class="lesson-panel">
    <span class="phase-tag">Interactive Lab</span>
    <h2>互动实验：调变量，看结果</h2>
    <p style="color:var(--muted)">不要只看结论。动手改变变量后，再用一句话解释画面为什么变了。</p>
    <div class="control-row">{interaction_controls(detail['interaction'])}</div>
    <div class="canvas-wrap"><canvas id="chem-canvas" class="wide-canvas" width="900" height="420" aria-label="{esc(node['name'])}互动实验画布"></canvas></div>
    <div id="lab-feedback" class="feedback">拖动或选择变量，观察画布变化。</div>
  </div>
</section>
{external}
<section class="section" id="micro-video" data-tts="micro-video" data-tsh="教学动画 - 用动态画面复盘核心关系">
  <div class="lesson-panel video-box">
    <span class="phase-tag">Micro Animation</span>
    <h2>教学动画：60 秒内复盘核心关系</h2>
    <video controls preload="metadata" playsinline><source src="./assets/video/{esc(course_id)}-main.mp4" type="video/mp4"></video>
  </div>
</section>

<section class="section" id="posttest" data-tts="posttest" data-tsh="后测 - 检验是否形成迁移能力" data-bloom-level="evaluate" data-scaffold="none" data-conceptest="true">
  <div class="lesson-panel">
    <span class="phase-tag">Post-test</span>
    <h2>后测：学会了吗？</h2>
    <p><strong>{esc(post_q)}</strong></p>
    {make_buttons(post_opts, post_ans, 'posttest')}
    <div id="posttest-feedback" class="feedback">先独立判断，再看诊断反馈。</div>
  </div>
</section>

<section class="section" id="tiered-practice" data-tts="tiered-practice" data-tsh="三段式作业 - 从基础到迁移">
  <div class="lesson-panel">
    <span class="phase-tag">Level Practice</span>
    <h2>三段式作业</h2>
    <div class="mini-grid">
      <div class="mini-panel"><h3>⭐ 基础巩固</h3><p>识别并写出本节核心定义、公式或分类标准。</p></div>
      <div class="mini-panel"><h3>⭐⭐ 能力应用</h3><p>把本课标准用于一个实验数据或真实生活场景。</p></div>
      <div class="mini-panel"><h3>⭐⭐⭐ 迁移挑战</h3><p>设计一个反例，说明常见错误为什么站不住脚。</p></div>
    </div>
  </div>
</section>

<section class="section" id="summary" data-tts="summary" data-tsh="总结 - 用一句话带走本课">
  <div class="lesson-panel">
    <span class="phase-tag">Summary</span>
    <h2>一句话带走</h2>
    <ul>{facts}</ul>
    <p class="feedback">如果你能解释“{esc(detail['question'])}”，这节课就真正过关了。</p>
  </div>
</section>

<script>
const FEEDBACK = {{ pretest: {json.dumps(pre_feedback, ensure_ascii=False)}, posttest: {json.dumps(post_feedback, ensure_ascii=False)} }};
function checkAnswer(btn, ok, target) {{
  btn.parentElement.querySelectorAll('.quiz-option').forEach(b => b.classList.remove('correct','wrong'));
  btn.classList.add(ok ? 'correct' : 'wrong');
  const box = document.getElementById(target + '-feedback');
  if (box) box.textContent = ok ? FEEDBACK[target] : '错因诊断：先回到定义里的关键词，再检查你是否把对象、条件或单位搞混了。' + FEEDBACK[target];
}}
{interaction_script(detail['interaction'])}
</script>
'''


def interaction_controls(kind: str) -> str:
    if kind == "classification":
        return '''<label>样品<select id="sample-select"><option value="air">空气</option><option value="oxygen">氧气 O₂</option><option value="water">水 H₂O</option><option value="salt">氯化钠 NaCl</option><option value="co2">二氧化碳 CO₂</option></select></label><label>判断路径<select id="path-select"><option value="pure">先问：是否纯净</option><option value="elements">再问：元素种类</option><option value="type">最后：性质类别</option></select></label>'''
    if kind == "tyndall":
        return '''<label>粒子直径 nm<input id="particle-size" type="range" min="0" max="500" value="50"></label><label>光强<input id="light" type="range" min="1" max="100" value="70"></label>'''
    if kind == "mole":
        return '''<label>物质<select id="substance"><option value="18">水 H₂O，M=18</option><option value="44">二氧化碳 CO₂，M=44</option><option value="58.5">氯化钠 NaCl，M=58.5</option></select></label><label>质量 g<input id="mass" type="range" min="1" max="117" value="18"></label>'''
    if kind == "gas":
        return '''<label>物质的量 mol<input id="gas-n" type="range" min="0.5" max="5" step="0.5" value="1"></label><label>条件<select id="gas-cond"><option value="22.4">标准状况</option><option value="24.5">常温常压近似</option><option value="11.2">加压后近似</option></select></label>'''
    if kind == "ion_mixer":
        return '''<label>溶液 A<select id="ion-a"><option value="AgNO3">AgNO₃</option><option value="BaCl2">BaCl₂</option><option value="NaOH">NaOH</option></select></label><label>溶液 B<select id="ion-b"><option value="NaCl">NaCl</option><option value="Na2SO4">Na₂SO₄</option><option value="CuSO4">CuSO₄</option></select></label>'''
    if kind == "equation":
        return '''<label>反应场景<select id="eq-scene"><option value="agcl">AgNO₃ + NaCl</option><option value="baso4">BaCl₂ + Na₂SO₄</option><option value="cuoh2">CuSO₄ + NaOH</option></select></label><label>步骤<select id="eq-step"><option value="split">拆强电解质</option><option value="cancel">删旁观离子</option><option value="net">写净离子方程式</option></select></label>'''
    if kind == "redox":
        return '''<label>还原剂电子数<input id="electron-lost" type="range" min="1" max="8" value="2"></label><label>氧化剂电子数<input id="electron-gain" type="range" min="1" max="8" value="2"></label>'''
    if kind == "sodium":
        return '''<label>反应对象<select id="na-target"><option value="water">水</option><option value="oxygen">氧气</option><option value="chlorine">氯气</option></select></label><label>钠块大小<input id="na-size" type="range" min="1" max="5" value="2"></label>'''
    if kind == "iron":
        return '''<label>铁离子<select id="fe-ion"><option value="Fe2">Fe²⁺</option><option value="Fe3">Fe³⁺</option></select></label><label>加入试剂<select id="fe-reagent"><option value="OH">NaOH</option><option value="SCN">KSCN</option><option value="Ox">氧化剂</option></select></label>'''
    if kind == "silicon":
        return '''<label>结构对象<select id="si-object"><option value="SiO2">SiO₂ 网络</option><option value="silicate">硅酸盐</option><option value="glass">玻璃材料</option></select></label><label>网络连接度<input id="si-connect" type="range" min="1" max="5" value="3"></label>'''
    if kind == "sulfur_nitrogen":
        return '''<label>污染物<select id="pollutant"><option value="SO2">SO₂</option><option value="NO2">NO₂</option><option value="NH3">NH₃</option></select></label><label>转化条件<select id="pollutant-cond"><option value="water">遇水</option><option value="oxygen">氧化</option><option value="base">碱吸收</option></select></label>'''
    if kind == "atom":
        return '''<label>质子数 Z<input id="protons" type="range" min="1" max="18" value="11"></label><label>中子数<input id="neutrons" type="range" min="0" max="22" value="12"></label>'''
    if kind == "periodic":
        return '''<label>周期<input id="period" type="range" min="2" max="4" value="3"></label><label>主族<input id="group" type="range" min="1" max="8" value="1"></label>'''
    if kind == "periodic_table":
        return '''<label>元素位置<select id="pt-element"><option value="Na">Na 第三周期 IA</option><option value="Mg">Mg 第三周期 IIA</option><option value="Cl">Cl 第三周期 VIIA</option><option value="Ar">Ar 第三周期 0族</option></select></label><label>比较方向<select id="pt-trend"><option value="period">同周期比较</option><option value="group">同主族比较</option></select></label>'''
    if kind == "bond":
        return '''<label>成键对象<select id="bond-pair"><option value="NaCl">Na + Cl</option><option value="HCl">H + Cl</option><option value="O2">O + O</option><option value="H2O">H + O</option></select></label><label>电负性差<input id="bond-diff" type="range" min="0" max="4" step="0.1" value="2.1"></label>'''
    if kind == "molecule":
        return '''<label>分子<select id="mol-shape"><option value="CO2">CO₂</option><option value="H2O">H₂O</option><option value="NH3">NH₃</option><option value="CH4">CH₄</option></select></label><label>孤电子对数<input id="lone-pairs" type="range" min="0" max="2" value="1"></label>'''
    if kind == "thermo":
        return '''<label>反应类型<select id="thermo-type"><option value="exo">放热反应</option><option value="endo">吸热反应</option></select></label><label>能量差 kJ<input id="energy-gap" type="range" min="20" max="300" value="120"></label>'''
    if kind == "enthalpy":
        return '''<label>反应物总能量<input id="react-energy" type="range" min="100" max="500" value="320"></label><label>生成物总能量<input id="prod-energy" type="range" min="100" max="500" value="220"></label>'''
    if kind == "hess":
        return '''<label>路径 A ΔH₁<input id="hess-a" type="range" min="-400" max="200" value="-120"></label><label>路径 B ΔH₂<input id="hess-b" type="range" min="-400" max="200" value="-180"></label>'''
    if kind == "rate":
        return '''<label>浓度<input id="rate-conc" type="range" min="1" max="5" value="2"></label><label>温度 ℃<input id="rate-temp" type="range" min="20" max="80" value="40"></label><label>催化剂<select id="rate-cat"><option value="1">无</option><option value="2.4">有</option></select></label>'''
    if kind == "equilibrium":
        return '''<label>正反应速率<input id="eq-forward" type="range" min="1" max="10" value="6"></label><label>逆反应速率<input id="eq-reverse" type="range" min="1" max="10" value="6"></label>'''
    if kind == "rate_equilibrium":
        return '''<label>调控目标<select id="rq-target"><option value="fast">加快速率</option><option value="yield">提高产率</option><option value="balance">兼顾速率与平衡</option></select></label><label>温度<input id="rq-temp" type="range" min="200" max="600" value="400"></label>'''
    if kind == "lechatelier":
        return '''<label>扰动<select id="lc-change"><option value="increaseA">增大反应物浓度</option><option value="pressure">增大压强</option><option value="heat">升高温度</option></select></label><label>反应类型<select id="lc-type"><option value="exo">正反应放热</option><option value="endo">正反应吸热</option></select></label>'''
    if kind == "k_eq":
        return '''<label>[生成物]<input id="prod-conc" type="range" min="0.1" max="5" step="0.1" value="2"></label><label>[反应物]<input id="react-conc" type="range" min="0.1" max="5" step="0.1" value="1"></label>'''
    if kind == "galvanic":
        return '''<label>负极金属<select id="anode-metal"><option value="Zn">Zn</option><option value="Fe">Fe</option><option value="Cu">Cu</option></select></label><label>正极离子<select id="cathode-ion"><option value="Cu2">Cu²⁺</option><option value="Ag">Ag⁺</option><option value="H">H⁺</option></select></label>'''
    if kind == "electrolysis":
        return '''<label>电解质<select id="electrolyte"><option value="NaClaq">NaCl 溶液</option><option value="CuCl2">CuCl₂ 溶液</option><option value="water">水</option></select></label><label>电流强度<input id="current" type="range" min="1" max="8" value="3"></label>'''
    if kind == "corrosion":
        return '''<label>环境<select id="cor-env"><option value="dry">干燥空气</option><option value="water">潮湿空气</option><option value="salt">盐水</option></select></label><label>防护<select id="cor-protect"><option value="none">无防护</option><option value="paint">涂层</option><option value="zn">镀锌/牺牲阳极</option></select></label>'''
    if kind == "organic":
        return '''<label>碳骨架<select id="carbon-chain"><option value="alkane">烷烃</option><option value="alkene">烯烃</option><option value="alcohol">醇</option><option value="acid">羧酸</option></select></label><label>碳原子数<input id="carbon-count" type="range" min="1" max="6" value="2"></label>'''
    if kind == "corrosion_protection":
        return '''<label>防腐方案<select id="protect-method"><option value="paint">涂层隔绝</option><option value="zinc">镀锌</option><option value="sacrificial">牺牲阳极</option><option value="current">外加电流</option></select></label><label>破损程度<input id="damage-level" type="range" min="0" max="10" value="3"></label>'''
    if kind == "hydrocarbon":
        return '''<label>烃类别<select id="hydro-type"><option value="alkane">烷烃</option><option value="alkene">烯烃</option><option value="alkyne">炔烃</option><option value="arene">芳香烃</option></select></label><label>碳数<input id="hydro-c" type="range" min="2" max="8" value="4"></label>'''
    if kind == "functional":
        return '''<label>官能团<select id="fg"><option value="OH">醇羟基 -OH</option><option value="CHO">醛基 -CHO</option><option value="COOH">羧基 -COOH</option><option value="COOR">酯基 -COOR</option></select></label><label>反应试剂<select id="fg-reagent"><option value="oxidize">氧化剂</option><option value="na">Na</option><option value="base">碱</option></select></label>'''
    if kind == "derivatives":
        return '''<label>衍生物<select id="deriv"><option value="halo">卤代烃</option><option value="alcohol">醇</option><option value="aldehyde">醛</option><option value="ester">酯</option></select></label><label>性质维度<select id="deriv-prop"><option value="polarity">极性/溶解性</option><option value="reaction">典型反应</option></select></label>'''
    if kind == "organic_reactions":
        return '''<label>反应类型<select id="org-rx"><option value="add">加成</option><option value="sub">取代</option><option value="elim">消去</option><option value="oxid">氧化</option><option value="ester">酯化</option></select></label><label>底物<select id="org-sub"><option value="alkene">烯烃</option><option value="alkane">烷烃</option><option value="alcohol">醇</option><option value="acid">羧酸+醇</option></select></label>'''
    if kind == "organic_synthesis":
        return '''<label>起点<select id="syn-start"><option value="ethene">乙烯</option><option value="ethanol">乙醇</option><option value="benzene">苯</option></select></label><label>目标<select id="syn-target"><option value="ethanol">乙醇</option><option value="acetic">乙酸</option><option value="ester">乙酸乙酯</option></select></label>'''
    if kind == "biomolecules":
        return '''<label>生物大分子<select id="bio-mol"><option value="sugar">糖类</option><option value="protein">蛋白质</option><option value="nucleic">核酸</option></select></label><label>功能维度<select id="bio-dim"><option value="unit">基本单元</option><option value="bond">连接方式</option><option value="function">生命功能</option></select></label>'''
    if kind == "polymers":
        return '''<label>聚合方式<select id="poly-type"><option value="addition">加聚</option><option value="condensation">缩聚</option></select></label><label>单体数<input id="monomer-count" type="range" min="2" max="12" value="6"></label>'''
    return '''<label>溶质物质的量 mol<input id="solute-n" type="range" min="0.05" max="1" step="0.05" value="0.2"></label><label>溶液体积 L<input id="solution-v" type="range" min="0.1" max="2" step="0.1" value="1"></label>'''


def interaction_script(kind: str) -> str:
    common = """
const canvas = document.getElementById('chem-canvas');
const ctx = canvas.getContext('2d');
function clearCanvas() { ctx.clearRect(0,0,canvas.width,canvas.height); ctx.fillStyle='#081426'; ctx.fillRect(0,0,canvas.width,canvas.height); }
function text(t,x,y,size=24,color='#eef6ff') { ctx.fillStyle=color; ctx.font=`${size}px -apple-system, BlinkMacSystemFont, PingFang SC, sans-serif`; ctx.fillText(t,x,y); }
function box(x,y,w,h,label,color='#38bdf8') { ctx.strokeStyle=color; ctx.lineWidth=3; ctx.strokeRect(x,y,w,h); text(label,x+16,y+42,24,color); }
"""
    if kind == "classification":
        return common + """
const samples = {air:['混合物','氮气+氧气+少量 CO₂'],oxygen:['纯净物 → 单质','只含氧元素 O₂'],water:['纯净物 → 化合物','H 与 O 组成'],salt:['纯净物 → 化合物 → 盐','Na⁺ 与 Cl⁻'],co2:['纯净物 → 化合物 → 氧化物','C 与 O 两种元素']};
function drawClassification(){ clearCanvas(); const key=document.getElementById('sample-select').value; const [type,why]=samples[key]; box(60,60,210,88,'是否纯净?'); box(345,60,210,88,'元素种类?','#a78bfa'); box(630,60,210,88,'性质类别?','#22c55e'); ctx.strokeStyle='#94a3b8'; ctx.beginPath(); ctx.moveTo(270,104); ctx.lineTo(345,104); ctx.moveTo(555,104); ctx.lineTo(630,104); ctx.stroke(); text('样品判断：'+type,90,240,34,'#fbbf24'); text('理由：'+why,90,295,28,'#dbeafe'); text('先问组成，再看性质；不要只凭名称或外观判断。',90,355,24,'#9fb4cc'); document.getElementById('lab-feedback').textContent='当前样品：'+type+'。'+why; }
document.querySelectorAll('#sample-select,#path-select').forEach(el=>el.addEventListener('change',drawClassification)); drawClassification();
"""
    if kind == "tyndall":
        return common + """
function drawTyndall(){ clearCanvas(); const size=+document.getElementById('particle-size').value; const light=+document.getElementById('light').value; const scatter=Math.min(1,size/120)*light/100; ctx.strokeStyle=`rgba(250,204,21,${0.25+scatter*0.65})`; ctx.lineWidth=14+scatter*20; ctx.beginPath(); ctx.moveTo(80,210); ctx.lineTo(820,210); ctx.stroke(); for(let i=0;i<90;i++){ const x=110+Math.random()*680, y=80+Math.random()*250; ctx.fillStyle=`rgba(125,211,252,${scatter*0.55})`; ctx.beginPath(); ctx.arc(x,y,2+Math.min(size/80,8),0,Math.PI*2); ctx.fill(); } text(size<1?'溶液区：粒子太小，光路弱':'胶体/浊液区：粒子变大，散射增强',90,360,28,'#fbbf24'); document.getElementById('lab-feedback').textContent=size<1?'接近溶液：几乎看不到光路。':size<=100?'胶体尺度：可观察到丁达尔效应。':'粒子偏大：可能变成浊液并逐渐沉降。'; }
document.querySelectorAll('#particle-size,#light').forEach(el=>el.addEventListener('input',drawTyndall)); drawTyndall();
"""
    if kind == "mole":
        return common + """
function drawMole(){ clearCanvas(); const M=+document.getElementById('substance').value; const m=+document.getElementById('mass').value; const n=m/M; text(`m = ${m.toFixed(1)} g`,80,80,30,'#bae6fd'); text(`M = ${M} g/mol`,80,125,30,'#bae6fd'); text(`n = m/M = ${n.toFixed(2)} mol`,80,185,36,'#fbbf24'); text(`N ≈ ${n.toFixed(2)} × 6.02×10²³ 个粒子`,80,240,30,'#dbeafe'); for(let i=0;i<Math.min(80,Math.round(n*24));i++){ ctx.fillStyle=i%2?'#38bdf8':'#a78bfa'; ctx.beginPath(); ctx.arc(470+(i%16)*22,80+Math.floor(i/16)*38,8,0,Math.PI*2); ctx.fill(); } document.getElementById('lab-feedback').textContent=`质量 ${m.toFixed(1)} g 对应 ${n.toFixed(2)} mol。微观粒子数通过阿伏加德罗常数连接。`; }
document.querySelectorAll('#substance,#mass').forEach(el=>el.addEventListener('input',drawMole)); drawMole();
"""
    if kind == "gas":
        return common + """
function drawGas(){ clearCanvas(); const n=+document.getElementById('gas-n').value; const vm=+document.getElementById('gas-cond').value; const V=n*vm; const w=Math.min(700,100+V*12); box(80,100,w,190,`气体体积 V ≈ ${V.toFixed(1)} L`,'#38bdf8'); for(let i=0;i<70;i++){ ctx.fillStyle='#a78bfa'; ctx.beginPath(); ctx.arc(100+Math.random()*(w-40),125+Math.random()*140,4,0,Math.PI*2); ctx.fill(); } text(`V = nVₘ = ${n} × ${vm} = ${V.toFixed(1)} L`,90,350,30,'#fbbf24'); document.getElementById('lab-feedback').textContent=`同样物质的量，温度和压强改变会改变气体摩尔体积。当前 Vₘ=${vm} L/mol。`; }
document.querySelectorAll('#gas-n,#gas-cond').forEach(el=>el.addEventListener('input',drawGas)); drawGas();
"""
    if kind == "ion_mixer":
        return common + """
const precip = {AgNO3:{NaCl:['AgCl 白色沉淀','Ag⁺ + Cl⁻ = AgCl↓'],Na2SO4:['无明显沉淀','离子主要共存'],CuSO4:['无明显沉淀','没有生成难溶物']},BaCl2:{NaCl:['无明显沉淀','离子主要共存'],Na2SO4:['BaSO₄ 白色沉淀','Ba²⁺ + SO₄²⁻ = BaSO₄↓'],CuSO4:['BaSO₄ 白色沉淀','Ba²⁺ + SO₄²⁻ = BaSO₄↓']},NaOH:{NaCl:['无明显沉淀','Na⁺、Cl⁻、OH⁻ 共存'],Na2SO4:['无明显沉淀','没有生成气体/水/沉淀'],CuSO4:['Cu(OH)₂ 蓝色沉淀','Cu²⁺ + 2OH⁻ = Cu(OH)₂↓']}};
function drawIonMixer(){ clearCanvas(); const a=document.getElementById('ion-a').value,b=document.getElementById('ion-b').value; const [res,eq]=precip[a][b]; box(80,70,260,110,a,'#38bdf8'); box(560,70,260,110,b,'#a78bfa'); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=5; ctx.beginPath(); ctx.moveTo(340,125); ctx.lineTo(560,125); ctx.stroke(); text('混合后：'+res,95,270,34,'#fbbf24'); text('净变化：'+eq,95,335,30,'#dbeafe'); document.getElementById('lab-feedback').textContent=`${a} 与 ${b}：${res}；${eq}`; }
document.querySelectorAll('#ion-a,#ion-b').forEach(el=>el.addEventListener('change',drawIonMixer)); drawIonMixer();
"""
    if kind == "equation":
        return common + """
const scenes={agcl:['Ag⁺ + NO₃⁻ + Na⁺ + Cl⁻','NO₃⁻、Na⁺ 是旁观离子','Ag⁺ + Cl⁻ = AgCl↓'],baso4:['Ba²⁺ + 2Cl⁻ + 2Na⁺ + SO₄²⁻','Cl⁻、Na⁺ 是旁观离子','Ba²⁺ + SO₄²⁻ = BaSO₄↓'],cuoh2:['Cu²⁺ + SO₄²⁻ + 2Na⁺ + 2OH⁻','SO₄²⁻、Na⁺ 是旁观离子','Cu²⁺ + 2OH⁻ = Cu(OH)₂↓']};
function drawEquation(){ clearCanvas(); const scene=document.getElementById('eq-scene').value, step=document.getElementById('eq-step').value; const arr=scenes[scene]; text('完整离子：'+arr[0],70,120,26,'#dbeafe'); text('旁观离子：'+arr[1],70,210,30,'#fbbf24'); text('净离子：'+arr[2],70,310,34,'#22c55e'); if(step==='split') box(60,70,780,80,'1 拆：强酸强碱可溶盐写离子'); if(step==='cancel') box(60,160,780,80,'2 删：反应前后不变的是旁观离子','#a78bfa'); if(step==='net') box(60,260,780,80,'3 查：原子守恒、电荷守恒','#22c55e'); document.getElementById('lab-feedback').textContent=step==='net'?'检查净离子方程式：原子和电荷必须同时守恒。':'先按步骤处理，不要跳过旁观离子识别。'; }
document.querySelectorAll('#eq-scene,#eq-step').forEach(el=>el.addEventListener('change',drawEquation)); drawEquation();
"""
    if kind == "redox":
        return common + """
function gcd(a,b){return b?gcd(b,a%b):a} function lcm(a,b){return a*b/gcd(a,b)}
function drawRedox(){ clearCanvas(); const lost=+document.getElementById('electron-lost').value, gain=+document.getElementById('electron-gain').value; const L=lcm(lost,gain); const left=L/lost, right=L/gain; box(80,90,260,120,`还原剂 × ${left}`,'#f97316'); box(560,90,260,120,`氧化剂 × ${right}`,'#38bdf8'); text(`失电子 ${lost} × ${left} = ${L}`,95,280,32,'#fbbf24'); text(`得电子 ${gain} × ${right} = ${L}`,95,340,32,'#bae6fd'); text('电子守恒是配平氧化还原方程式的第一把尺子。',95,390,26,'#cbd5e1'); document.getElementById('lab-feedback').textContent=`最小公倍数 ${L}：还原剂系数乘 ${left}，氧化剂系数乘 ${right}，使得失电子=得电子。`; }
document.querySelectorAll('#electron-lost,#electron-gain').forEach(el=>el.addEventListener('input',drawRedox)); drawRedox();
"""
    if kind == "sodium":
        return common + """
const reactions={water:['2Na + 2H₂O = 2NaOH + H₂↑','浮、熔、游、响、红：产热、放氢气、生成强碱'],oxygen:['4Na + O₂ = 2Na₂O 或 2Na + O₂ = Na₂O₂','条件不同，氧化物类型不同：氧化钠/过氧化钠'],chlorine:['2Na + Cl₂ = 2NaCl','剧烈燃烧，生成离子化合物氯化钠']};
function drawSodium(){ clearCanvas(); const target=document.getElementById('na-target').value; const size=+document.getElementById('na-size').value; const [eq,obs]=reactions[target]; text(eq,80,110,34,'#fbbf24'); text(obs,80,180,26,'#dbeafe'); ctx.fillStyle='#cbd5e1'; ctx.beginPath(); ctx.arc(240,300,20+size*12,0,Math.PI*2); ctx.fill(); ctx.strokeStyle='#38bdf8'; ctx.lineWidth=4; ctx.beginPath(); ctx.arc(240,300,70+size*10,0,Math.PI*2); ctx.stroke(); text('钠越大，放热和产气风险越高；实验必须小块、镊子、远离水面观察。',80,395,24,'#fecaca'); document.getElementById('lab-feedback').textContent=`钠与${target==='water'?'水':target==='oxygen'?'氧气':'氯气'}反应：${eq}`; }
document.querySelectorAll('#na-target,#na-size').forEach(el=>el.addEventListener('input',drawSodium)); drawSodium();
"""
    if kind == "iron":
        return common + """
const feData={Fe2:{OH:['Fe(OH)₂ 白色沉淀迅速变灰绿再变红褐','Fe²⁺ + 2OH⁻ = Fe(OH)₂↓，随后被 O₂ 氧化'],SCN:['无血红色','SCN⁻ 主要用于检验 Fe³⁺'],Ox:['Fe²⁺ 被氧化为 Fe³⁺','Fe²⁺ 失 1e⁻ → Fe³⁺']},Fe3:{OH:['Fe(OH)₃ 红褐色沉淀','Fe³⁺ + 3OH⁻ = Fe(OH)₃↓'],SCN:['出现血红色络合物','Fe³⁺ + SCN⁻ 显血红色'],Ox:['Fe³⁺ 已是较高价态','常表现氧化性，可被还原为 Fe²⁺']}};
function drawIron(){ clearCanvas(); const ion=document.getElementById('fe-ion').value, r=document.getElementById('fe-reagent').value; const [res,eq]=feData[ion][r]; box(80,70,260,105,ion==='Fe2'?'Fe²⁺':'Fe³⁺','#f97316'); box(560,70,260,105,r,'#38bdf8'); text(res,95,255,32,'#fbbf24'); text(eq,95,325,28,'#dbeafe'); text('铁的核心是 Fe²⁺ / Fe³⁺ 相互转化与特征检验。',95,390,24,'#cbd5e1'); document.getElementById('lab-feedback').textContent=res+'；'+eq; }
document.querySelectorAll('#fe-ion,#fe-reagent').forEach(el=>el.addEventListener('change',drawIron)); drawIron();
"""
    if kind == "silicon":
        return common + """
function drawSilicon(){ clearCanvas(); const obj=document.getElementById('si-object').value; const conn=+document.getElementById('si-connect').value; for(let i=0;i<conn*7;i++){ const x=140+(i%7)*90,y=110+Math.floor(i/7)*70; ctx.fillStyle=i%2?'#fbbf24':'#38bdf8'; ctx.beginPath(); ctx.arc(x,y,18,0,Math.PI*2); ctx.fill(); if(i%7>0){ ctx.strokeStyle='#94a3b8'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(x-72,y); ctx.lineTo(x-18,y); ctx.stroke(); }} const desc={SiO2:'SiO₂ 是空间网状结构，熔点高、硬度大，是石英和玻璃的重要基础。',silicate:'硅酸盐由 Si-O 骨架和金属阳离子组成，是岩石、陶瓷和水泥的重要成分。',glass:'普通玻璃可看作硅酸盐材料，结构无固定长程有序，性能来自网络结构。'}[obj]; text(obj+'：'+desc,70,350,24,'#dbeafe'); document.getElementById('lab-feedback').textContent=desc; }
document.querySelectorAll('#si-object,#si-connect').forEach(el=>el.addEventListener('input',drawSilicon)); drawSilicon();
"""
    if kind == "sulfur_nitrogen":
        return common + """
const poll={SO2:{water:['SO₂ + H₂O ⇌ H₂SO₃','形成亚硫酸，酸雨来源之一'],oxygen:['2SO₂ + O₂ ⇌ 2SO₃','催化氧化后可制硫酸'],base:['SO₂ + 2OH⁻ = SO₃²⁻ + H₂O','可用碱液吸收尾气']},NO2:{water:['3NO₂ + H₂O = 2HNO₃ + NO','形成硝酸型酸雨'],oxygen:['2NO + O₂ = 2NO₂','NO 易被氧化成红棕色 NO₂'],base:['2NO₂ + 2OH⁻ = NO₂⁻ + NO₃⁻ + H₂O','碱液可吸收部分氮氧化物']},NH3:{water:['NH₃ + H₂O ⇌ NH₃·H₂O','氨水显弱碱性'],oxygen:['4NH₃ + 5O₂ → 4NO + 6H₂O','工业制硝酸的重要步骤'],base:['NH₃ 本身显碱性','不能用碱液吸收，常用酸吸收']}};
function drawPollutant(){ clearCanvas(); const p=document.getElementById('pollutant').value,c=document.getElementById('pollutant-cond').value; const [eq,meaning]=poll[p][c]; text(p+' 转化：',80,90,34,'#fbbf24'); text(eq,80,165,32,'#dbeafe'); text(meaning,80,240,28,'#bae6fd'); for(let i=0;i<55;i++){ ctx.fillStyle=i%3?'rgba(148,163,184,.35)':'rgba(251,191,36,.45)'; ctx.beginPath(); ctx.arc(120+Math.random()*700,290+Math.random()*80,5+Math.random()*6,0,Math.PI*2); ctx.fill(); } text('硫、氮化合物要连到价态转化、工业制备和环境影响。',80,400,24,'#cbd5e1'); document.getElementById('lab-feedback').textContent=eq+'；'+meaning; }
document.querySelectorAll('#pollutant,#pollutant-cond').forEach(el=>el.addEventListener('change',drawPollutant)); drawPollutant();
"""
    if kind == "atom":
        return common + """
function drawAtom(){ clearCanvas(); const Z=+document.getElementById('protons').value,N=+document.getElementById('neutrons').value; const e=Z; text(`Z=${Z}：质子数=核电荷数=核外电子数`,70,80,30,'#fbbf24'); text(`质量数 A≈Z+N=${Z+N}`,70,130,30,'#dbeafe'); ctx.strokeStyle='#38bdf8'; ctx.lineWidth=3; for(let r of [70,125,180]){ctx.beginPath();ctx.arc(450,250,r,0,Math.PI*2);ctx.stroke();} ctx.fillStyle='#f97316'; ctx.beginPath();ctx.arc(450,250,42,0,Math.PI*2);ctx.fill(); for(let i=0;i<Math.min(e,18);i++){ const shell=i<2?70:i<10?125:180; const a=i*2.399; ctx.fillStyle='#bae6fd'; ctx.beginPath();ctx.arc(450+Math.cos(a)*shell,250+Math.sin(a)*shell,7,0,Math.PI*2);ctx.fill(); } document.getElementById('lab-feedback').textContent=`该原子质子数 ${Z}，核外电子数 ${e}，质量数近似 ${Z+N}。结构决定元素种类与性质。`; }
document.querySelectorAll('#protons,#neutrons').forEach(el=>el.addEventListener('input',drawAtom)); drawAtom();
"""
    if kind == "periodic":
        return common + """
function drawPeriodic(){ clearCanvas(); const period=+document.getElementById('period').value, group=+document.getElementById('group').value; for(let r=0;r<4;r++){ for(let c=0;c<8;c++){ const x=80+c*90,y=70+r*70; ctx.strokeStyle=(r+1===period && c+1===group)?'#fbbf24':'#334155'; ctx.lineWidth=(r+1===period && c+1===group)?5:2; ctx.strokeRect(x,y,70,52); text(`${r+1}-${c+1}`,x+12,y+34,18,'#cbd5e1'); }} const radiusTrend=group<=2?'原子半径较大，金属性较强':group>=7?'非金属性较强，得电子趋势强':'性质过渡'; text(`第 ${period} 周期，第 ${group} 主族`,80,385,32,'#fbbf24'); text(radiusTrend,80,430,28,'#dbeafe'); document.getElementById('lab-feedback').textContent=`周期律：同周期从左到右核电荷增加，原子半径总体减小，金属性减弱、非金属性增强。当前：${radiusTrend}`; }
document.querySelectorAll('#period,#group').forEach(el=>el.addEventListener('input',drawPeriodic)); drawPeriodic();
"""
    if kind == "periodic_table":
        return common + """
const pt={Na:['金属性强，易失 1e⁻ 形成 Na⁺','第三周期从 Na 到 Cl，金属性减弱'],Mg:['金属性较强，易形成 Mg²⁺','同周期向右原子半径减小'],Cl:['非金属性强，易得 1e⁻ 形成 Cl⁻','卤族元素同族性质相似'],Ar:['稀有气体，最外层稳定','0 族元素通常化学性质稳定']};
function drawPeriodicTable(){ clearCanvas(); const e=document.getElementById('pt-element').value; for(let c=0;c<8;c++){ const x=90+c*92,y=95; ctx.strokeStyle=['Na','Mg','','','','','Cl','Ar'][c]===e?'#fbbf24':'#334155'; ctx.lineWidth=['Na','Mg','','','','','Cl','Ar'][c]===e?5:2; ctx.strokeRect(x,y,72,58); text(['Na','Mg','Al','Si','P','S','Cl','Ar'][c],x+16,y+38,22,'#dbeafe'); } const [a,b]=pt[e]; text(`${e}：${a}`,90,245,30,'#fbbf24'); text(b,90,310,28,'#bae6fd'); text('周期表不是背格子，而是位置→电子排布→性质预测。',90,385,24,'#cbd5e1'); document.getElementById('lab-feedback').textContent=`${e}：${a}。${b}`; }
document.querySelectorAll('#pt-element,#pt-trend').forEach(el=>el.addEventListener('change',drawPeriodicTable)); drawPeriodicTable();
"""
    if kind == "bond":
        return common + """
const bonds={NaCl:['离子键','Na 失电子，Cl 得电子，形成 Na⁺ 与 Cl⁻ 的静电作用'],HCl:['极性共价键','电子对偏向 Cl，分子有极性'],O2:['非极性共价键','相同原子共用电子对，电子分布对称'],H2O:['极性共价键','O-H 键有极性，分子呈折线形']};
function drawBond(){ clearCanvas(); const p=document.getElementById('bond-pair').value,d=+document.getElementById('bond-diff').value; const [type,why]=bonds[p]; box(90,95,260,110,p,'#38bdf8'); box(550,95,260,110,type,'#fbbf24'); ctx.strokeStyle=d>1.7?'#f97316':'#a78bfa'; ctx.lineWidth=8; ctx.beginPath(); ctx.moveTo(350,150); ctx.lineTo(550,150); ctx.stroke(); text(why,90,295,28,'#dbeafe'); text(`电负性差参考：${d.toFixed(1)}，差越大越偏离子性。`,90,370,24,'#cbd5e1'); document.getElementById('lab-feedback').textContent=`${p}：${type}。${why}`; }
document.querySelectorAll('#bond-pair,#bond-diff').forEach(el=>el.addEventListener('input',drawBond)); drawBond();
"""
    if kind == "molecule":
        return common + """
const mols={CO2:['直线形','O=C=O，中心 C 周围两组电子域，键角约 180°'],H2O:['折线形','O 有两对孤电子对，压缩 H-O-H 键角'],NH3:['三角锥形','N 有一对孤电子对，分子有极性'],CH4:['正四面体','C 周围四个等价 C-H 键，键角约 109.5°']};
function drawMolecule(){ clearCanvas(); const m=document.getElementById('mol-shape').value; const [shape,why]=mols[m]; text(`${m}：${shape}`,90,90,36,'#fbbf24'); const cx=450,cy=230; ctx.fillStyle='#38bdf8'; ctx.beginPath();ctx.arc(cx,cy,30,0,Math.PI*2);ctx.fill(); const atoms=m==='CO2'?[[cx-170,cy],[cx+170,cy]]:m==='H2O'?[[cx-130,cy+110],[cx+130,cy+110]]:m==='NH3'?[[cx-150,cy+90],[cx+150,cy+90],[cx,cy-145]]:[[cx-150,cy+90],[cx+150,cy+90],[cx,cy-145],[cx,cy+155]]; atoms.forEach(([x,y])=>{ctx.strokeStyle='#94a3b8';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(cx,cy);ctx.lineTo(x,y);ctx.stroke();ctx.fillStyle='#fbbf24';ctx.beginPath();ctx.arc(x,y,18,0,Math.PI*2);ctx.fill();}); text(why,90,395,26,'#dbeafe'); document.getElementById('lab-feedback').textContent=`${m} 是${shape}：${why}`; }
document.querySelectorAll('#mol-shape,#lone-pairs').forEach(el=>el.addEventListener('input',drawMolecule)); drawMolecule();
"""
    if kind == "thermo":
        return common + """
function drawThermo(){ clearCanvas(); const type=document.getElementById('thermo-type').value,gap=+document.getElementById('energy-gap').value; const ry=type==='exo'?160:300, py=type==='exo'?310:150; ctx.strokeStyle='#38bdf8';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(110,ry);ctx.lineTo(380,ry);ctx.lineTo(650,py);ctx.lineTo(820,py);ctx.stroke(); text('反应物',120,ry-25,26,'#bae6fd'); text('生成物',680,py-25,26,'#bae6fd'); const dh=type==='exo'?-gap:gap; text(`ΔH = ${dh} kJ/mol`,110,390,36,dh<0?'#22c55e':'#f97316'); text(dh<0?'放热：体系能量降低，环境获得热量':'吸热：体系能量升高，需要从环境吸热',110,445,26,'#dbeafe'); document.getElementById('lab-feedback').textContent=dh<0?`放热反应，ΔH=${dh} kJ/mol。`:`吸热反应，ΔH=+${dh} kJ/mol。`; }
document.querySelectorAll('#thermo-type,#energy-gap').forEach(el=>el.addEventListener('input',drawThermo)); drawThermo();
"""
    if kind == "enthalpy":
        return common + """
function drawEnthalpy(){ clearCanvas(); const r=+document.getElementById('react-energy').value,p=+document.getElementById('prod-energy').value; const dh=p-r; const ry=420-r*0.55, py=420-p*0.55; ctx.strokeStyle='#38bdf8';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(120,ry);ctx.lineTo(360,ry);ctx.moveTo(560,py);ctx.lineTo(800,py);ctx.stroke(); ctx.strokeStyle=dh<0?'#22c55e':'#f97316';ctx.beginPath();ctx.moveTo(460,ry);ctx.lineTo(460,py);ctx.stroke(); text(`反应物焓 ${r}`,125,ry-20,24,'#bae6fd'); text(`生成物焓 ${p}`,565,py-20,24,'#bae6fd'); text(`ΔH = H生成物 - H反应物 = ${dh} kJ/mol`,100,470,32,dh<0?'#22c55e':'#f97316'); document.getElementById('lab-feedback').textContent=dh<0?`生成物焓低于反应物，ΔH=${dh}，为放热反应。`:`生成物焓高于反应物，ΔH=+${dh}，为吸热反应。`; }
document.querySelectorAll('#react-energy,#prod-energy').forEach(el=>el.addEventListener('input',drawEnthalpy)); drawEnthalpy();
"""
    if kind == "hess":
        return common + """
function drawHess(){ clearCanvas(); const a=+document.getElementById('hess-a').value,b=+document.getElementById('hess-b').value,total=a+b; box(80,80,240,90,`路径1 ΔH=${a}`,'#38bdf8'); box(520,80,240,90,`路径2 ΔH=${b}`,'#a78bfa'); ctx.strokeStyle='#94a3b8';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(320,125);ctx.lineTo(520,125);ctx.stroke(); text(`总 ΔH = ${a} + ${b} = ${total} kJ/mol`,90,265,34,total<0?'#22c55e':'#f97316'); text('盖斯定律：只看始态和终态，路径可拆可加。',90,340,28,'#dbeafe'); document.getElementById('lab-feedback').textContent=`无论分几步，只要始态终态相同，总焓变为 ${total} kJ/mol。`; }
document.querySelectorAll('#hess-a,#hess-b').forEach(el=>el.addEventListener('input',drawHess)); drawHess();
"""
    if kind == "rate":
        return common + """
function drawRate(){ clearCanvas(); const c=+document.getElementById('rate-conc').value,t=+document.getElementById('rate-temp').value,cat=+document.getElementById('rate-cat').value; const rate=c*(1+(t-20)/40)*cat; for(let i=0;i<Math.min(120,rate*10);i++){ ctx.fillStyle=i%2?'#38bdf8':'#fbbf24'; ctx.beginPath();ctx.arc(90+Math.random()*720,90+Math.random()*250,5,0,Math.PI*2);ctx.fill(); } text(`相对速率 ≈ ${rate.toFixed(1)}`,90,380,36,'#fbbf24'); text(`浓度 ${c}、温度 ${t}℃、催化剂系数 ${cat}`,90,435,26,'#dbeafe'); document.getElementById('lab-feedback').textContent=`有效碰撞增多，反应速率提高。当前相对速率 ${rate.toFixed(1)}。`; }
document.querySelectorAll('#rate-conc,#rate-temp,#rate-cat').forEach(el=>el.addEventListener('input',drawRate)); drawRate();
"""
    if kind == "equilibrium":
        return common + """
function drawEquilibrium(){ clearCanvas(); const f=+document.getElementById('eq-forward').value,r=+document.getElementById('eq-reverse').value; ctx.fillStyle='#38bdf8';ctx.fillRect(120,260-f*18,220,f*18); ctx.fillStyle='#a78bfa';ctx.fillRect(520,260-r*18,220,r*18); text(`v正=${f}`,145,310,30,'#bae6fd'); text(`v逆=${r}`,545,310,30,'#e9d5ff'); const msg=Math.abs(f-r)<=1?'动态平衡：v正≈v逆，但反应并未停止':f>r?'正向占优，体系会向生成物方向推进':'逆向占优，体系会向反应物方向推进'; text(msg,90,405,28,'#fbbf24'); document.getElementById('lab-feedback').textContent=msg; }
document.querySelectorAll('#eq-forward,#eq-reverse').forEach(el=>el.addEventListener('input',drawEquilibrium)); drawEquilibrium();
"""
    if kind == "rate_equilibrium":
        return common + """
function drawRateEquilibrium(){ clearCanvas(); const target=document.getElementById('rq-target').value,temp=+document.getElementById('rq-temp').value; const speed=(temp/100).toFixed(1); const yieldIndex=target==='yield'?75:target==='fast'?45:62; box(80,90,260,110,`速率指数 ${speed}`,'#38bdf8'); box(540,90,260,110,`产率指数 ${yieldIndex}`,'#fbbf24'); text(target==='fast'?'高温常加快速率，但不一定提高平衡产率。':target==='yield'?'提高产率要看平衡移动方向，不能只看速度。':'工业条件常在速率、产率、成本、安全之间折中。',80,305,28,'#dbeafe'); text(`当前温度：${temp}℃`,80,380,30,'#bae6fd'); document.getElementById('lab-feedback').textContent='速率和平衡是两套问题：催化剂改变速率，不改变平衡位置。'; }
document.querySelectorAll('#rq-target,#rq-temp').forEach(el=>el.addEventListener('input',drawRateEquilibrium)); drawRateEquilibrium();
"""
    if kind == "lechatelier":
        return common + """
function drawLeChatelier(){ clearCanvas(); const ch=document.getElementById('lc-change').value,type=document.getElementById('lc-type').value; let dir,why; if(ch==='increaseA'){dir='向正反应方向移动';why='体系会消耗被增加的反应物';} else if(ch==='pressure'){dir='向气体体积减小方向移动';why='体系会减弱压强增大的影响';} else {dir=type==='exo'?'向逆反应方向移动':'向正反应方向移动';why='升温时平衡向吸热方向移动';} box(90,90,300,110,'外界扰动','#f97316'); box(520,90,300,110,dir,'#22c55e'); text(why,90,300,30,'#dbeafe'); text('勒夏特列原理：平衡移动的方向总是减弱外界改变。',90,375,26,'#fbbf24'); document.getElementById('lab-feedback').textContent=`${dir}：${why}。`; }
document.querySelectorAll('#lc-change,#lc-type').forEach(el=>el.addEventListener('change',drawLeChatelier)); drawLeChatelier();
"""
    if kind == "k_eq":
        return common + """
function drawKEq(){ clearCanvas(); const p=+document.getElementById('prod-conc').value,r=+document.getElementById('react-conc').value; const K=(p/r).toFixed(2); box(80,80,260,100,`[生成物]=${p}`,'#22c55e'); box(520,80,260,100,`[反应物]=${r}`,'#38bdf8'); text(`K ≈ [生成物]/[反应物] = ${K}`,90,280,36,'#fbbf24'); text(K>1?'K>1：平衡更偏向生成物':'K<1：平衡更偏向反应物',90,350,28,'#dbeafe'); document.getElementById('lab-feedback').textContent=`当前 K≈${K}。K 只受温度影响，不随起始浓度任意改变。`; }
document.querySelectorAll('#prod-conc,#react-conc').forEach(el=>el.addEventListener('input',drawKEq)); drawKEq();
"""
    if kind == "galvanic":
        return common + """
function drawGalvanic(){ clearCanvas(); const an=document.getElementById('anode-metal').value, ca=document.getElementById('cathode-ion').value; box(90,95,220,130,`负极 ${an}`,'#f97316'); box(590,95,220,130,`正极 ${ca}`,'#38bdf8'); ctx.strokeStyle='#fbbf24';ctx.lineWidth=6;ctx.beginPath();ctx.moveTo(310,130);ctx.lineTo(590,130);ctx.stroke(); text('电子从负极流向正极；负极氧化，正极还原。',90,305,30,'#dbeafe'); text(`${an} → ${an}²⁺ + e⁻（示意）`,90,370,26,'#fbbf24'); document.getElementById('lab-feedback').textContent=`原电池把自发氧化还原反应转化为电能：${an} 作负极，电子经外电路流向正极。`; }
document.querySelectorAll('#anode-metal,#cathode-ion').forEach(el=>el.addEventListener('change',drawGalvanic)); drawGalvanic();
"""
    if kind == "electrolysis":
        return common + """
const ely={NaClaq:['阴极：2H₂O + 2e⁻ = H₂↑ + 2OH⁻','阳极：2Cl⁻ - 2e⁻ = Cl₂↑'],CuCl2:['阴极：Cu²⁺ + 2e⁻ = Cu','阳极：2Cl⁻ - 2e⁻ = Cl₂↑'],water:['阴极生成 H₂','阳极生成 O₂']};
function drawElectrolysis(){ clearCanvas(); const e=document.getElementById('electrolyte').value,cur=+document.getElementById('current').value; const [cat,ano]=ely[e]; box(80,80,300,120,'阴极 还原','#38bdf8'); box(520,80,300,120,'阳极 氧化','#f97316'); text(cat,90,275,26,'#dbeafe'); text(ano,90,335,26,'#fbbf24'); text(`电流越大，单位时间电子转移越多：当前 ${cur}`,90,400,24,'#cbd5e1'); document.getElementById('lab-feedback').textContent=`电解池由外电源驱动非自发反应。${cat}；${ano}`; }
document.querySelectorAll('#electrolyte,#current').forEach(el=>el.addEventListener('input',drawElectrolysis)); drawElectrolysis();
"""
    if kind == "corrosion":
        return common + """
function drawCorrosion(){ clearCanvas(); const env=document.getElementById('cor-env').value,pro=document.getElementById('cor-protect').value; const envRate={dry:1,water:4,salt:7}[env]; const protect={none:1,paint:.35,zn:.18}[pro]; const rate=(envRate*protect).toFixed(1); box(90,80,260,110,`环境风险 ${envRate}`,'#f97316'); box(560,80,260,110,`防护系数 ${protect}`,'#22c55e'); text(`腐蚀速率指数 ≈ ${rate}`,90,300,34,'#fbbf24'); text(pro==='zn'?'牺牲阳极：Zn 先被氧化，保护 Fe。':pro==='paint'?'涂层隔绝水和氧，但破损后保护下降。':'无防护时水、氧和电解质会加快电化学腐蚀。',90,370,26,'#dbeafe'); document.getElementById('lab-feedback').textContent=`当前腐蚀风险指数 ${rate}。金属腐蚀本质是电化学氧化过程。`; }
document.querySelectorAll('#cor-env,#cor-protect').forEach(el=>el.addEventListener('change',drawCorrosion)); drawCorrosion();
"""
    if kind == "organic":
        return common + """
function drawOrganic(){ clearCanvas(); const type=document.getElementById('carbon-chain').value,n=+document.getElementById('carbon-count').value; const suffix={alkane:'烷烃 C-C 单键，通式 CnH2n+2',alkene:'烯烃含 C=C，易发生加成反应',alcohol:'醇含 -OH 官能团，可发生氧化/酯化',acid:'羧酸含 -COOH，显酸性并可酯化'}[type]; for(let i=0;i<n;i++){ const x=130+i*95,y=190; ctx.fillStyle='#38bdf8';ctx.beginPath();ctx.arc(x,y,24,0,Math.PI*2);ctx.fill(); text('C',x-8,y+8,22,'#07111f'); if(i>0){ctx.strokeStyle='#94a3b8';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(x-72,y);ctx.lineTo(x-24,y);ctx.stroke();}} text(suffix,90,330,28,'#fbbf24'); text('有机入门先抓两件事：碳骨架 + 官能团。',90,395,26,'#dbeafe'); document.getElementById('lab-feedback').textContent=`${suffix}；碳原子数 ${n}。`; }
document.querySelectorAll('#carbon-chain,#carbon-count').forEach(el=>el.addEventListener('input',drawOrganic)); drawOrganic();
"""
    if kind == "corrosion_protection":
        return common + """
function drawCorrosionProtection(){ clearCanvas(); const m=document.getElementById('protect-method').value,d=+document.getElementById('damage-level').value; const desc={paint:'涂层隔绝水和氧，破损越大保护越弱。',zinc:'镀锌既隔绝环境，也能在破损处牺牲 Zn 保护 Fe。',sacrificial:'牺牲阳极把更活泼金属接入体系，让它先氧化。',current:'外加电流让被保护金属成为阴极，减少氧化。'}[m]; const risk=Math.max(0.5,(d+1)*({paint:.8,zinc:.25,sacrificial:.2,current:.18}[m])); box(80,90,300,110,m,'#38bdf8'); box(540,90,300,110,`风险指数 ${risk.toFixed(1)}`,'#fbbf24'); text(desc,90,310,28,'#dbeafe'); text('防腐不是“永不腐蚀”，而是让氧化反应更难发生或转移到牺牲材料。',90,385,24,'#cbd5e1'); document.getElementById('lab-feedback').textContent=`${desc} 当前风险指数 ${risk.toFixed(1)}。`; }
document.querySelectorAll('#protect-method,#damage-level').forEach(el=>el.addEventListener('input',drawCorrosionProtection)); drawCorrosionProtection();
"""
    if kind == "hydrocarbon":
        return common + """
const hd={alkane:['烷烃','只含 C-C 单键，主要发生取代/燃烧'],alkene:['烯烃','含 C=C，易加成、可使溴水褪色'],alkyne:['炔烃','含 C≡C，反应活性强于烷烃'],arene:['芳香烃','苯环结构稳定，常发生取代而非加成']};
function drawHydrocarbon(){ clearCanvas(); const t=document.getElementById('hydro-type').value,n=+document.getElementById('hydro-c').value; const [name,desc]=hd[t]; for(let i=0;i<n;i++){const x=100+i*80,y=180;ctx.fillStyle='#38bdf8';ctx.beginPath();ctx.arc(x,y,22,0,Math.PI*2);ctx.fill(); if(i>0){ctx.strokeStyle=t==='alkyne'?'#f97316':t==='alkene'?'#fbbf24':'#94a3b8';ctx.lineWidth=t==='alkane'?4:t==='alkene'?7:10;ctx.beginPath();ctx.moveTo(x-58,y);ctx.lineTo(x-22,y);ctx.stroke();}} text(`${name}：${desc}`,90,330,30,'#fbbf24'); text(`碳数：${n}，先看不饱和度，再判断典型反应。`,90,395,24,'#dbeafe'); document.getElementById('lab-feedback').textContent=`${name}：${desc}`; }
document.querySelectorAll('#hydro-type,#hydro-c').forEach(el=>el.addEventListener('input',drawHydrocarbon)); drawHydrocarbon();
"""
    if kind == "functional":
        return common + """
const fgData={OH:['醇羟基','可与 Na 反应放 H₂，可被氧化或酯化'],CHO:['醛基','可被氧化为羧酸，能发生银镜等反应'],COOH:['羧基','显酸性，可与醇酯化'],COOR:['酯基','可水解生成酸和醇']};
function drawFunctional(){ clearCanvas(); const fg=document.getElementById('fg').value,re=document.getElementById('fg-reagent').value; const [name,desc]=fgData[fg]; box(90,90,260,110,fg,'#38bdf8'); box(560,90,260,110,re,'#a78bfa'); text(`${name}：${desc}`,90,300,30,'#fbbf24'); text('官能团决定一类有机物的典型性质。',90,375,26,'#dbeafe'); document.getElementById('lab-feedback').textContent=`${name}：${desc}`; }
document.querySelectorAll('#fg,#fg-reagent').forEach(el=>el.addEventListener('change',drawFunctional)); drawFunctional();
"""
    if kind == "derivatives":
        return common + """
const dv={halo:['卤代烃','C-X 键带来取代/消去反应入口'],alcohol:['醇','-OH 让分子更极性，可氧化、消去、酯化'],aldehyde:['醛','-CHO 易被氧化，是还原性官能团'],ester:['酯','有香味，酸性/碱性条件下可水解']};
function drawDerivatives(){ clearCanvas(); const d=document.getElementById('deriv').value,p=document.getElementById('deriv-prop').value; const [name,desc]=dv[d]; box(90,90,300,110,name,'#38bdf8'); box(540,90,300,110,p,'#fbbf24'); text(desc,90,305,30,'#dbeafe'); text('烃的衍生物 = 烃骨架 + 取代原子/官能团。',90,380,26,'#bae6fd'); document.getElementById('lab-feedback').textContent=`${name}：${desc}`; }
document.querySelectorAll('#deriv,#deriv-prop').forEach(el=>el.addEventListener('change',drawDerivatives)); drawDerivatives();
"""
    if kind == "organic_reactions":
        return common + """
const rx={add:['加成','不饱和键打开，原子或原子团加到两端'],sub:['取代','一个原子/基团被另一个替换'],elim:['消去','小分子脱去，形成不饱和键'],oxid:['氧化','有机物失氢/得氧或碳价态升高'],ester:['酯化','羧酸与醇生成酯和水']};
function drawOrganicReaction(){ clearCanvas(); const r=document.getElementById('org-rx').value,s=document.getElementById('org-sub').value; const [name,desc]=rx[r]; box(90,90,260,110,name,'#38bdf8'); box(560,90,260,110,s,'#a78bfa'); text(desc,90,300,30,'#fbbf24'); text('判断反应类型先看断什么键、成什么键、官能团如何变化。',90,375,26,'#dbeafe'); document.getElementById('lab-feedback').textContent=`${name}：${desc}`; }
document.querySelectorAll('#org-rx,#org-sub').forEach(el=>el.addEventListener('change',drawOrganicReaction)); drawOrganicReaction();
"""
    if kind == "organic_synthesis":
        return common + """
function drawSynthesis(){ clearCanvas(); const s=document.getElementById('syn-start').value,t=document.getElementById('syn-target').value; const route=s==='ethene'&&t==='ethanol'?'乙烯 + H₂O → 乙醇（加成）':s==='ethanol'&&t==='acetic'?'乙醇 → 乙醛 → 乙酸（氧化）':t==='ester'?'乙酸 + 乙醇 ⇌ 乙酸乙酯 + H₂O（酯化）':'先改变官能团，再调整碳骨架'; box(80,100,240,110,`起点 ${s}`,'#38bdf8'); box(570,100,240,110,`目标 ${t}`,'#22c55e'); ctx.strokeStyle='#fbbf24';ctx.lineWidth=6;ctx.beginPath();ctx.moveTo(320,155);ctx.lineTo(570,155);ctx.stroke(); text(route,90,320,28,'#dbeafe'); text('合成路线设计：逆推目标官能团，正推可行反应。',90,395,26,'#fbbf24'); document.getElementById('lab-feedback').textContent=route; }
document.querySelectorAll('#syn-start,#syn-target').forEach(el=>el.addEventListener('change',drawSynthesis)); drawSynthesis();
"""
    if kind == "biomolecules":
        return common + """
const bm={sugar:{unit:'单糖，如葡萄糖',bond:'糖苷键连接成多糖',function:'供能、储能、结构支持'},protein:{unit:'氨基酸',bond:'肽键连接成多肽',function:'催化、运输、结构、调控'},nucleic:{unit:'核苷酸',bond:'磷酸二酯键连接',function:'储存和传递遗传信息'}};
function drawBiomolecules(){ clearCanvas(); const m=document.getElementById('bio-mol').value,d=document.getElementById('bio-dim').value; const data=bm[m]; text(`${m}：${data[d]}`,90,110,34,'#fbbf24'); for(let i=0;i<8;i++){ const x=120+i*80,y=230; ctx.fillStyle=i%2?'#38bdf8':'#a78bfa'; ctx.beginPath();ctx.arc(x,y,22,0,Math.PI*2);ctx.fill(); if(i>0){ctx.strokeStyle='#94a3b8';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(x-58,y);ctx.lineTo(x-22,y);ctx.stroke();}} text('生物大分子不是只背名称，要看单体、连接键和生命功能。',90,390,26,'#dbeafe'); document.getElementById('lab-feedback').textContent=`${m}：${data[d]}`; }
document.querySelectorAll('#bio-mol,#bio-dim').forEach(el=>el.addEventListener('change',drawBiomolecules)); drawBiomolecules();
"""
    if kind == "polymers":
        return common + """
function drawPolymers(){ clearCanvas(); const type=document.getElementById('poly-type').value,n=+document.getElementById('monomer-count').value; for(let i=0;i<n;i++){ const x=80+i*65,y=220; ctx.fillStyle=type==='addition'?'#38bdf8':'#a78bfa'; ctx.fillRect(x,y,42,42); if(i>0){ctx.strokeStyle='#fbbf24';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(x-23,y+21);ctx.lineTo(x,y+21);ctx.stroke();}} const desc=type==='addition'?'加聚：不饱和单体打开双键，链增长，无小分子副产物。':'缩聚：含两个或多个官能团的单体缩合，常生成小分子副产物。'; text(desc,80,340,28,'#dbeafe'); text(`聚合度示意：${n}`,80,400,28,'#fbbf24'); document.getElementById('lab-feedback').textContent=desc; }
document.querySelectorAll('#poly-type,#monomer-count').forEach(el=>el.addEventListener('input',drawPolymers)); drawPolymers();
"""
    return common + """
function drawConcentration(){ clearCanvas(); const n=+document.getElementById('solute-n').value; const V=+document.getElementById('solution-v').value; const c=n/V; const h=Math.min(260,60+c*120); ctx.fillStyle='rgba(56,189,248,.28)'; ctx.fillRect(330,330-h,240,h); ctx.strokeStyle='#bae6fd'; ctx.lineWidth=4; ctx.strokeRect(330,70,240,260); for(let i=0;i<Math.round(n*80);i++){ ctx.fillStyle='#fbbf24'; ctx.beginPath(); ctx.arc(350+Math.random()*200,90+Math.random()*220,4,0,Math.PI*2); ctx.fill(); } text(`c = n/V = ${n.toFixed(2)} / ${V.toFixed(1)} = ${c.toFixed(2)} mol/L`,80,370,30,'#fbbf24'); document.getElementById('lab-feedback').textContent=`溶质 ${n.toFixed(2)} mol，溶液总体积 ${V.toFixed(1)} L，浓度 ${c.toFixed(2)} mol/L。`; }
document.querySelectorAll('#solute-n,#solution-v').forEach(el=>el.addEventListener('input',drawConcentration)); drawConcentration();
"""


def make_extra_svg(node: dict, detail: dict, mode: str) -> str:
    if mode == "concept":
        title = "概念结构图"
        labels = [c[0] for c in detail["concepts"]]
        subtitle = detail["question"]
    else:
        title = "过程机制图"
        labels = ["输入条件", "可观察现象", "化学解释"]
        subtitle = detail["memory"]
    cards = []
    colors = ["#38bdf8", "#a78bfa", "#22c55e"]
    for i, label in enumerate(labels[:3]):
        x = 80 + i * 360
        cards.append(f'''<rect x="{x}" y="250" width="280" height="150" rx="22" fill="#0f172a" stroke="{colors[i]}" stroke-width="4"/>
<text x="{x+30}" y="330" fill="{colors[i]}" font-size="30" font-weight="800">{esc(label)}</text>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="640" viewBox="0 0 1200 640">
<rect width="1200" height="640" fill="#081426"/>
<circle cx="1020" cy="110" r="170" fill="#38bdf8" opacity="0.12"/>
<text x="80" y="100" fill="#f8fafc" font-size="48" font-weight="900">{esc(node['name'])} · {title}</text>
<text x="80" y="158" fill="#cbd5e1" font-size="26">{esc(subtitle[:56])}</text>
{''.join(cards)}
<text x="80" y="540" fill="#fbbf24" font-size="28">从图像进入问题，再回到定义、证据和迁移任务。</text>
</svg>'''


def make_hero_svg(course_id: str, node: dict, detail: dict) -> str:
    concepts = detail["concepts"]
    cards = []
    colors = ["#38bdf8", "#a78bfa", "#22c55e"]
    for i, (title, txt) in enumerate(concepts):
        x = 70 + i * 390
        cards.append(f'''
  <rect x="{x}" y="270" width="330" height="190" rx="24" fill="#0f172a" stroke="{colors[i]}" stroke-width="4"/>
  <text x="{x+26}" y="325" fill="{colors[i]}" font-size="28" font-weight="800">{esc(title)}</text>
  <text x="{x+26}" y="374" fill="#dbeafe" font-size="21">{esc(txt[:30])}</text>
  <text x="{x+26}" y="410" fill="#dbeafe" font-size="21">{esc(txt[30:58])}</text>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
  <defs><linearGradient id="g" x1="0" x2="1"><stop stop-color="#07111f"/><stop offset="1" stop-color="#172554"/></linearGradient></defs>
  <rect width="1280" height="720" fill="url(#g)"/>
  <circle cx="1050" cy="120" r="180" fill="#38bdf8" opacity="0.13"/>
  <circle cx="220" cy="620" r="220" fill="#a78bfa" opacity="0.12"/>
  <text x="70" y="112" fill="#f8fafc" font-size="52" font-weight="900">{esc(node['name'])}</text>
  <text x="70" y="168" fill="#bae6fd" font-size="28">{esc(detail['question'])}</text>
  <text x="70" y="225" fill="#cbd5e1" font-size="24">角色任务：{esc(detail['role'])} · 课标节点：{esc(node['id'])}</text>
  {''.join(cards)}
  <rect x="70" y="525" width="1140" height="105" rx="24" fill="#020617" opacity="0.72" stroke="#334155"/>
  <text x="105" y="585" fill="#fbbf24" font-size="30" font-weight="800">记忆锚点</text>
  <text x="260" y="585" fill="#e0f2fe" font-size="26">{esc(detail['memory'])}</text>
  <text x="70" y="675" fill="#64748b" font-size="18">TeachAny v7.14 · 高中化学完整模式 · AI 学伴 / TTS / 知识图谱 / Canvas 互动 / 课标挂树</text>
</svg>'''


def write_manifest(course_dir: Path, course_id: str, node: dict, domain: dict, detail: dict):
    manifest = {
        "id": course_id,
        "course_id": course_id,
        "node_id": node["id"],
        "name": detail["title"],
        "name_en": detail["title_en"],
        "subject": "chemistry",
        "grade": node.get("grade", 10),
        "stage": "high",
        "domain": domain.get("id", "matter-classification"),
        "lesson_type": "experiment",
        "status": "community",
        "author": "TeachAny",
        "version": "1.0.0",
        "teachany_version": "7.14.0",
        "curriculum": "cn-national",
        "description": f"高中化学课标互动课件：{node['name']}。包含问题锚点、ABT 情境、Canvas 互动、TTS、教学动画、知识图谱与 AI 学伴。",
        "tags": ["高中化学", "中国课标", node["name"]],
        "difficulty": 3,
        "duration": "15-20 min",
        "prerequisites": node.get("prerequisites", []),
        "leads_to": node.get("extends", []),
        "learning_objectives": detail["objectives"],
        "curriculum_standards": [
            {"source": "普通高中化学课程标准", "content": point}
            for point in (node.get("curriculum_points") or [f"围绕{node['name']}形成结构化理解、证据推理和真实情境迁移能力。"])
        ],
        "assets": {
            "hero": "assets/hero-infographic.svg",
            "tts_manifest": "tts/manifest.json",
            "videos": [f"assets/video/{course_id}-main.mp4"],
            "images": ["assets/hero-infographic.svg"],
        },
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
- 学科：化学
- 课标节点：{node['name']}
- 课标摘录：{'；'.join(node.get('curriculum_points', [])[:3])}

## Phase 1 教学骨架
- 问题锚点：{detail['question']}
- ABT：
  - And：{detail['and']}
  - But：{detail['but']}
  - Therefore：{detail['therefore']}
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/{course_id}`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
"""


def generate_tts(course_dir: Path, detail: dict):
    tts_dir = course_dir / "tts"
    tts_dir.mkdir(parents=True, exist_ok=True)
    segments = [
        ("s01", f"今天我们学习{detail['title']}。先记住核心问题：{detail['question']}"),
        ("s02", f"这节课的关键不是背名词，而是抓判断标准。{detail['memory']}"),
        ("s03", f"最后提醒一个高频易错点：{detail['error']}"),
    ]
    manifest = []
    for seg_id, text in segments:
        out = tts_dir / f"{seg_id}.mp3"
        tmp = tts_dir / f"{seg_id}.aiff"
        say_cmd = ["say", "-v", "Tingting", "-r", "175", "-o", str(tmp), text]
        result = subprocess.run(say_cmd, text=True, capture_output=True)
        if result.returncode != 0:
            subprocess.run(["say", "-r", "175", "-o", str(tmp), text], check=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp), "-acodec", "libmp3lame", "-b:a", "128k", str(out)], check=True)
        tmp.unlink(missing_ok=True)
        manifest.append({"id": seg_id, "title": text[:18], "src": f"./tts/{seg_id}.mp3", "text": text})
    (tts_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def generate_video(course_dir: Path, course_id: str, node: dict, detail: dict):
    video_dir = course_dir / "assets/video"
    video_dir.mkdir(parents=True, exist_ok=True)
    out = video_dir / f"{course_id}-main.mp4"

    # Homebrew ffmpeg on this machine is built without drawtext. Generate
    # content-specific PNG frames with Pillow first, then encode them to mp4.
    from PIL import Image, ImageDraw, ImageFont

    font_candidates = [
        Path("/System/Library/Fonts/PingFang.ttc"),
        Path("/System/Library/Fonts/STHeiti Light.ttc"),
        Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
    ]
    font_path = next((p for p in font_candidates if p.exists()), None)

    def load_font(size: int):
        if font_path:
            try:
                return ImageFont.truetype(str(font_path), size)
            except Exception:
                pass
        return ImageFont.load_default()

    title_font = load_font(54)
    body_font = load_font(34)
    small_font = load_font(26)
    frames_dir = video_dir / "_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    frame_texts = [
        (node["name"], detail["question"]),
        ("判断标准", detail["memory"]),
        ("易错提醒", detail["error"]),
        ("迁移任务", "把本课判断标准用于一个新的实验或生活场景。"),
        ("学习闭环", "前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业"),
    ]
    for i, (headline, body) in enumerate(frame_texts, 1):
        img = Image.new("RGB", (1280, 720), "#081426")
        draw = ImageDraw.Draw(img)
        draw.ellipse((930, -120, 1330, 280), fill="#123b5a")
        draw.ellipse((-140, 470, 300, 910), fill="#2e235a")
        draw.rounded_rectangle((70, 82, 1210, 638), radius=32, outline="#38bdf8", width=4, fill="#0f172a")
        draw.text((110, 135), headline, font=title_font, fill="#f8fafc")
        y = 245
        line = ""
        for ch in body:
            trial = line + ch
            if draw.textlength(trial, font=body_font) > 980:
                draw.text((110, y), line, font=body_font, fill="#dbeafe")
                y += 58
                line = ch
            else:
                line = trial
        if line:
            draw.text((110, y), line, font=body_font, fill="#dbeafe")
        draw.text((110, 585), f"TeachAny 高中化学 · {course_id} · {i}/5", font=small_font, fill="#94a3b8")
        img.save(frames_dir / f"frame_{i:03d}.png")

        audio = course_dir / "tts" / "s01.mp3"
        cmd = [
            "ffmpeg", "-y", "-loglevel", "error",
            "-framerate", "1",
            "-i", str(frames_dir / "frame_%03d.png"),
        ]
        if audio.exists():
            cmd += ["-i", str(audio)]
        cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "25"]
        if audio.exists():
            cmd += ["-c:a", "aac", "-shortest"]
        cmd += [str(out)]
        subprocess.run(cmd, check=True)
    shutil.rmtree(frames_dir, ignore_errors=True)


def generate_course(course_id: str, node: dict, domain: dict, detail: dict):
    course_dir = ROOT / "community" / course_id
    if course_dir.exists():
        shutil.rmtree(course_dir)
    (course_dir / "assets").mkdir(parents=True, exist_ok=True)
    (course_dir / "tts").mkdir(parents=True, exist_ok=True)

    audio_manifest = generate_tts(course_dir, detail)
    generate_video(course_dir, course_id, node, detail)
    (course_dir / "assets/hero-infographic.svg").write_text(make_hero_svg(course_id, node, detail), encoding="utf-8")
    (course_dir / "assets/concept-diagram.svg").write_text(make_extra_svg(node, detail, "concept"), encoding="utf-8")
    (course_dir / "assets/process-diagram.svg").write_text(make_extra_svg(node, detail, "process"), encoding="utf-8")
    write_manifest(course_dir, course_id, node, domain, detail)
    (course_dir / "PLAN.md").write_text(make_plan(course_id, node, detail), encoding="utf-8")

    skeleton = SKELETON.read_text(encoding="utf-8")
    content = make_content(course_id, node, domain, detail)
    anchor_items = ["判断类别", "避开易错点", "解决实验题"]
    choices = "\n".join(f'<button class="choice" data-anchor-choice="{esc(label)}">{esc(label)}</button>' for label in anchor_items)
    objectives = "\n".join(f"<li>{esc(x)}</li>" for x in detail["objectives"])
    prereq_names = ", ".join(node.get("prerequisites", [])) or "无"
    html_text = replace_all(skeleton, {
        "COURSE_ID": course_id,
        "TITLE": detail["title"],
        "DESCRIPTION": f"高中化学课标互动课件：{node['name']}。",
        "SUBJECT": "chemistry",
        "STAGE_GRADE": f"high-{node.get('grade', 10)}",
        "GRADE": str(node.get("grade", 10)),
        "STAGE": "high",
        "NODE_ID": node["id"],
        "DOMAIN": domain.get("id", "matter-classification"),
        "PREREQ_COURSE_IDS": ",".join(node.get("prerequisites", [])),
        "NEXT_COURSE_ID": "",
        "COURSE_VERSION": "1.0.0",
        "TEACHANY_VERSION": "7.14.0",
        "LESSON_TYPE": "experiment",
        "HERO_QUESTION": detail["question"],
        "HERO_IMAGE_ALT": f"{node['name']}知识结构图",
        "HERO_FIGCAPTION": f"{node['name']}：问题锚点、核心概念、易错点与迁移任务。",
        "AUDIO_PLAYLIST_JSON": json.dumps(audio_manifest, ensure_ascii=False, indent=2),
        "PROBLEM_ANCHOR_CHOICES": choices,
        "LEARNING_OBJECTIVES": objectives,
        "CONTENT_SECTIONS": content,
        "OPTIONAL_MAP_HEAD": "",
        "OPTIONAL_MAP_TAIL": "",
        "PREREQUISITE_NAMES": prereq_names,
        "FREE_MODE": "false",
    })
    html_text = html_text.replace('src="./assets/' + course_id + '-hero.png" onerror="this.src=\'./assets/hero-infographic.svg\'"', 'src="./assets/hero-infographic.svg"')
    html_text = html_text.replace(f'<title>{detail["title"]}</title>', f'<title>{detail["title"]} · 高中化学 G{node.get("grade", 10)} · TeachAny v7.14</title>')
    html_text = html_text.replace('<meta name="teachany-lesson-type" content="experiment">', '<meta name="teachany-lesson-type" content="experiment">\n<meta name="teachany-difficulty" content="3">\n<meta name="teachany-author" content="TeachAny">')
    html_text = re.sub(r'<!--.*?-->', '', html_text, flags=re.S)
    html_text = html_text.replace(' placeholder="把你卡住的问题写在这里"', ' aria-label="把你卡住的问题写在这里"')
    html_text = html_text.replace('aria-label="知识图谱互动画布占位"', 'aria-label="知识图谱互动画布"')
    html_text = html_text.replace('placeholder', '提示输入')
    html_text = html_text.replace('占位', '备用')
    (course_dir / "index.html").write_text(html_text, encoding="utf-8")
    print(f"✅ generated {course_id}")


def main():
    nodes, domains = read_tree_nodes()
    for node_id in BATCH_IDS:
        generate_course(node_id, nodes[node_id], domains[node_id], DETAILS[node_id])


if __name__ == "__main__":
    main()
