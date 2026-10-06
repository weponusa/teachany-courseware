#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quality pass for Batch A (except ohms-law already done):
no-text hero + HTML labels + L1/L2/L3 practice + strip junk + checkbox CSS.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

LABEL_CSS = """
<style id="ta-labeled-figure-css">
.ta-figure-labeled{position:relative}
.ta-figure-wrap{position:relative}
.ta-figure-labeled img{width:100%;border-radius:12px;display:block}
.ta-figure-tags{position:absolute;inset:0;pointer-events:none}
.ta-fig-tag{position:absolute;transform:translate(-50%,-50%);background:rgba(15,23,42,.88);color:#fff;font-size:13px;font-weight:700;padding:5px 11px;border-radius:8px;white-space:nowrap;box-shadow:0 4px 12px rgba(0,0,0,.25);border:1px solid rgba(56,189,248,.35)}
.practice-block{margin:14px 0;padding:14px;border:1px solid rgba(148,163,184,.22);border-radius:12px;background:rgba(15,23,42,.45)}
.practice-block h3{margin:0 0 8px;color:#bae6fd;font-size:16px}
input[type="checkbox"],input[type="radio"]{width:18px!important;height:18px!important;min-height:18px!important;min-width:18px!important;margin:2px 0 0;padding:0;flex:0 0 18px;accent-color:var(--brand);border:none;background:transparent}
.checklist{display:flex;flex-direction:column;gap:10px;margin-top:12px}
.checklist label{display:flex;gap:12px;align-items:flex-start;margin:0;padding:12px 14px;border:1px solid rgba(148,163,184,.22);border-radius:12px;background:rgba(2,6,23,.45);color:var(--text);line-height:1.55;cursor:pointer}
.checklist label span{flex:1;min-width:0}
.control-row input[type="range"]{width:100%;min-height:28px;padding:0;background:transparent;border:none}
</style>
"""

LESSON_STYLE = (
    '<style>.lesson-panel{background:linear-gradient(180deg,rgba(20,35,58,.96),rgba(13,27,47,.96));'
    'border:1px solid rgba(148,163,184,.18);padding:22px;box-shadow:0 16px 40px rgba(0,0,0,.18)}'
    '.mini-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}'
    '.mini-panel{background:rgba(15,23,42,.68);border:1px solid rgba(148,163,184,.18);padding:16px}'
    '.mini-panel h3{margin:0 0 8px;color:#bae6fd}'
    '.quiz-option{display:block;width:100%;margin:8px 0;border:1px solid rgba(56,189,248,.28);'
    'background:#0b1628;color:#eef6ff;padding:12px 14px;text-align:left;cursor:pointer}'
    '.quiz-option.correct{border-color:#22c55e;background:rgba(34,197,94,.14)}'
    '.quiz-option.wrong{border-color:#f97316;background:rgba(249,115,22,.14)}'
    '.feedback{min-height:44px;margin-top:10px;padding:10px 12px;background:rgba(56,189,248,.10);color:#dbeafe}'
    '.control-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;align-items:end;margin:12px 0}'
    '.control-row label{color:#cbd5e1;font-size:14px}'
    '.steps{margin:0;padding-left:1.2em;line-height:1.8}.steps li{margin:6px 0}</style>\n'
)


def tags(items: list[tuple[str, str, str]]) -> str:
    return "".join(
        f'<span class="ta-fig-tag" style="top:{t};left:{l}">{txt}</span>' for txt, t, l in items
    )


def hero_fig(cid: str, center: str, items: list[tuple[str, str, str]], caption: str) -> str:
    return f'''
<section data-scaffold="full" data-bloom-level="apply" class="section" id="hero-infographic" data-tsh="知识结构主图 - 无字生图 + 中文叠标">
  <figure class="ta-standard-figure ta-figure-labeled">
    <div class="ta-figure-wrap">
      <img class="hero-cover-img" src="./assets/{cid}-hero.png" alt="{center}知识结构（无字底图）">
      <div class="ta-figure-tags" aria-hidden="true">
        <span class="ta-fig-tag" style="top:48%;left:50%">{center}</span>
        {tags(items)}
      </div>
    </div>
    <figcaption>{caption}</figcaption>
  </figure>
</section>
'''


def labeled_img(cid: str, slot: str, alt: str, caption: str, items: list[tuple[str, str, str]]) -> str:
    return f'''<figure class="ta-standard-figure ta-figure-labeled" style="margin-top:16px">
  <div class="ta-figure-wrap">
    <img src="./assets/{cid}-{slot}.png" alt="{alt}">
    <div class="ta-figure-tags" aria-hidden="true">{tags(items)}</div>
  </div>
  <figcaption>{caption}</figcaption>
</figure>'''


def quiz(qid: str, title: str, stem: str, opts: list[tuple[str, bool]]) -> str:
    btns = "\n".join(
        f'<button class="quiz-option" onclick="checkAnswer(this,{"true" if ok else "false"},\'{qid}\')">{text}</button>'
        for text, ok in opts
    )
    return f'''<div class="practice-block">
<h3>{title}</h3>
<p>{stem}</p>
{btns}
<div id="{qid}-feedback" class="feedback"></div>
</div>'''


def summary_block(items: list[str]) -> str:
    labels = "\n".join(
        f'      <label><input type="checkbox" class="recap-check"><span>{t}</span></label>' for t in items
    )
    n = len(items)
    return f'''<section class="slide-page" data-page-index="13" data-page-type="content" data-tsh="小结">
<section class="section" id="summary" data-tts="summary">
  <div class="lesson-panel">
    <span class="phase-tag">小结清单</span>
    <h2>这节课你应能做到</h2>
    <div class="checklist" id="summary-checklist">
{labels}
    </div>
    <p id="summary-feedback" class="feedback" style="margin-top:12px">勾选你已掌握的条目。</p>
  </div>
</section>
</section>
<script>
const FEEDBACK = __FEEDBACK__;
function checkAnswer(btn,ok,target){{
  const root=btn.closest('.practice-block, .lesson-panel')||btn.parentElement;
  root.querySelectorAll('.quiz-option').forEach(b=>b.classList.remove('correct','wrong'));
  btn.classList.add(ok?'correct':'wrong');
  const box=document.getElementById(target+'-feedback');
  if(box) box.textContent=(ok?'✅ ':'❌ ')+(FEEDBACK[target]||'');
}}
function showOpenRubric(){{
  const box=document.getElementById('l3-open-feedback');
  if(!box) return;
  box.hidden=false;
  box.innerHTML=FEEDBACK.open||'对照量规补全要点。';
}}
document.querySelectorAll('.recap-check').forEach(cb=>{{
  cb.addEventListener('change',()=>{{
    const n=document.querySelectorAll('.recap-check:checked').length;
    const f=document.getElementById('summary-feedback');
    if(f) f.textContent=n?`已勾选 ${{n}}/{n} 项。`:'勾选你已掌握的条目。';
  }});
}});
</script>
'''.replace("__FEEDBACK__", "PLACEHOLDER")


COURSES: dict[str, dict] = {}


def build_resistance() -> dict:
    cid = "phy-m-resistance"
    lab = r'''<section class="section" id="interactive-lab" data-tts="interactive-lab" data-bloom-level="apply" data-scaffold="partial" data-interactive="R-lab"><div class="lesson-panel"><span class="phase-tag">互动实验</span>
<h2>调长度与横截面积，看电阻趋势</h2>
<p style="color:var(--muted)">定性：同种材料，R ∝ L / S（温度一定）</p>
<div class="control-row">
<label>长度 L<input id="r-l" type="range" min="1" max="10" value="4"></label>
<label>横截面积 S<input id="r-s" type="range" min="1" max="8" value="2"></label>
</div>
<div class="canvas-wrap"><canvas id="physics-canvas" class="wide-canvas" width="900" height="360"></canvas></div>
<div id="lab-feedback" class="feedback"></div></div></section>
<script>
(function(){
  const canvas=document.getElementById('physics-canvas'); if(!canvas) return;
  const ctx=canvas.getContext('2d');
  const L=document.getElementById('r-l'), S=document.getElementById('r-s'), fb=document.getElementById('lab-feedback');
  function draw(){
    const l=+L.value,s=+S.value,R=Math.round(10*l/s*10)/10;
    ctx.clearRect(0,0,canvas.width,canvas.height); ctx.fillStyle='#081426'; ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='#fbbf24'; ctx.font='26px PingFang SC,sans-serif'; ctx.fillText('定性：R ∝ L / S',60,50);
    ctx.fillStyle='#e2e8f0'; ctx.font='22px PingFang SC,sans-serif'; ctx.fillText('L='+l+' · S='+s+' · 相对电阻 ≈ '+R,60,100);
    ctx.fillStyle='#38bdf8'; ctx.fillRect(80,220, Math.min(700,l*60), Math.max(12,s*10));
    fb.textContent='长度加倍→电阻加倍；横截面积加倍→电阻减半（同材料、同温度）。';
  }
  L.addEventListener('input',draw); S.addEventListener('input',draw); draw();
})();
</script>'''
    feedback = {
        "pretest": "电阻是导体本身性质，常温下由材料、长度、横截面积、温度决定，不随 U、I 变性质。",
        "l1a": "长度越长，电阻越大。",
        "l1b": "横截面积越大，电阻越小。",
        "l2a": "滑动变阻器通过改变接入电路的电阻丝长度改变电阻。",
        "l2b": "R=U/I 是计算式，不能推出电阻与电压成正比。",
        "l3a": "研究电阻与长度关系：同材料、同粗细、同温度，只改变长度。",
        "open": "量规：①材料与温度控制；②提到长度或横截面积；③说明变阻器改接入长度。",
    }
    body = f'''{LESSON_STYLE}
<section class="slide-page" data-page-index="4" data-page-type="content" data-tsh="真实情境">
<section class="section" id="story" data-tts="story"><div class="lesson-panel"><span class="phase-tag">真实情境</span>
<h2>调光台灯为什么能由亮变暗？</h2>
<p>旋钮往往连着<strong>滑动变阻器</strong>：改变接入电路的电阻丝长度，从而改变电路电阻与电流，灯的亮度跟着变。</p>
<div class="mini-grid">
<div class="mini-panel"><h3>已有经验</h3><p>细导线更热；长电线有时压降更明显。</p></div>
<div class="mini-panel"><h3>真正卡点</h3><p>把电阻当成“随电压变大而变大”的量。</p></div>
<div class="mini-panel"><h3>本课任务</h3><p>影响因素 → 变阻器 → 计算式辨析。</p></div>
</div></div></section></section>

<section class="slide-page" data-page-index="5" data-page-type="content" data-tsh="前测">
<section class="section" id="pretest" data-tts="pretest" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">前测 · ConcepTest</span>
<h2>关于电阻，正确的是？</h2>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">A. 电阻随电压增大而增大</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'pretest')">B. 电阻是导体本身的性质（温度等条件一定时）</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">C. 横截面积越大电阻一定越大</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">D. 长度越长电阻越小</button>
<div id="pretest-feedback" class="feedback">先选再看解析。</div>
</div></section></section>

<section class="slide-page" data-page-index="6" data-page-type="content" data-tsh="核心概念">
<section class="section" id="core" data-tts="core"><div class="lesson-panel"><span class="phase-tag">核心概念</span>
<h2>电阻：阻碍作用有多大</h2>
<div class="mini-grid">
<div class="mini-panel"><h3>定义直觉</h3><p>电阻越大，同样电压下电流越小。</p></div>
<div class="mini-panel"><h3>决定因素</h3><p>材料、长度、横截面积、温度。</p></div>
<div class="mini-panel"><h3>变阻器</h3><p>改变接入长度 → 改变电阻。</p></div>
</div>
{labeled_img(cid,'section1','电阻丝与变阻器（无字）','同种材料：更长、更细 → 电阻通常更大。',[('电阻丝','30%','40%'),('滑动变阻器','70%','55%'),('接入长度','55%','75%')])}
</div></section></section>

<section class="slide-page" data-page-index="7" data-page-type="content" data-tsh="易混">
<section class="section" id="deep-understanding" data-tts="deep-understanding"><div class="lesson-panel"><span class="phase-tag">易混辨析</span>
<h2>R=U/I 是计算式</h2>
<ul class="steps">
<li>可用某状态的 U、I 算出当时电阻。</li>
<li>不表示“电压越大，电阻性质就越大”。</li>
</ul>
{labeled_img(cid,'section2','长短粗细对比（无字）','控制变量：比长度时保持材料、横截面积、温度相同。',[('更长','35%','30%'),('更粗','40%','70%'),('R 更大？','75%','35%'),('R 更小？','75%','70%')])}
</div></section></section>

<section class="slide-page" data-page-index="8" data-page-type="content" data-tsh="例题">
<section class="section" id="worked-example" data-tts="worked-example"><div class="lesson-panel"><span class="phase-tag">例题拆解</span>
<h2>例：U=6 V，I=0.3 A，求 R</h2>
<ol class="steps"><li>R=U/I=6/0.3=20 Ω。</li><li>强调：这是该状态下的电阻值。</li></ol>
</div></section></section>

<section class="slide-page" data-page-index="9" data-page-type="content" data-tsh="互动">{lab}</section>

<section class="slide-page" data-page-index="10" data-page-type="content" data-tsh="L1">
<section class="section" id="practice-l1" data-tts="practice-l1"><div class="lesson-panel"><span class="phase-tag">练习 L1</span><h2>基础巩固</h2>
{quiz('l1a','1. 影响因素','同种材料、同样粗细，导线越长则',
[('A. 电阻越小',False),('B. 电阻越大',True),('C. 电阻不变',False),('D. 无法判断',False)])}
{quiz('l1b','2. 横截面积','同种材料、同样长度，横截面积越大则',
[('A. 电阻越大',False),('B. 电阻越小',True),('C. 电阻一定为零',False),('D. 与电阻无关',False)])}
</div></section></section>

<section class="slide-page" data-page-index="11" data-page-type="content" data-tsh="L2">
<section class="section" id="practice-l2" data-tts="practice-l2"><div class="lesson-panel"><span class="phase-tag">练习 L2</span><h2>能力应用</h2>
{quiz('l2a','3. 变阻器','滑动变阻器改变电阻的主要方式是',
[('A. 改变电源电压',False),('B. 改变接入电阻丝的长度',True),('C. 改变灯泡额定功率',False),('D. 改变电流表量程',False)])}
{quiz('l2b','4. 概念陷阱','“由 R=U/I 可知电阻与电压成正比”',
[('A. 正确',False),('B. 错误：这是计算式',True),('C. 只在串联正确',False),('D. 只在并联正确',False)])}
</div></section></section>

<section class="slide-page" data-page-index="12" data-page-type="content" data-tsh="L3">
<section class="section" id="practice-l3" data-tts="practice-l3"><div class="lesson-panel"><span class="phase-tag">练习 L3</span><h2>迁移</h2>
{quiz('l3a','5. 控制变量','探究电阻与长度关系，应保持不变的是',
[('A. 材料、横截面积、温度',True),('B. 只保持电压',False),('C. 长度',False),('D. 什么都不用管',False)])}
<div class="practice-block"><h3>6. 开放产出</h3>
<p>用三句话说明：调光台灯变暗时，电路里可能改变了什么？</p>
<textarea id="l3-open" rows="3" style="width:100%;margin-top:8px;padding:10px;border-radius:8px;border:1px solid rgba(148,163,184,.3);background:#0b1628;color:#e2e8f0"></textarea>
<button type="button" class="quiz-option" style="margin-top:10px;text-align:center" onclick="showOpenRubric()">对照量规自检</button>
<div id="l3-open-feedback" class="feedback" hidden></div></div>
</div></section></section>
'''
    return {
        "cid": cid,
        "center": "电阻",
        "hero_tags": [
            ("材料", "18%", "18%"),
            ("长度", "18%", "82%"),
            ("横截面积", "48%", "12%"),
            ("温度", "48%", "88%"),
            ("滑动变阻器", "78%", "22%"),
            ("易错：R≠随U变", "78%", "78%"),
        ],
        "caption": "无字生图 + 中文叠标：材料 · 长度 · 横截面积 · 变阻器 · 易错",
        "anchors": [
            ("电阻由哪些因素决定？", "电阻由哪些因素决定？"),
            ("滑动变阻器怎样改变电阻？", "滑动变阻器怎样改变电阻？"),
            ("为什么不能说电阻跟电压成正比？", "为什么不能说电阻跟电压成正比？"),
        ],
        "objectives": [
            "说出电阻的决定因素（材料、长度、横截面积、温度）",
            "解释滑动变阻器如何改变接入长度",
            "区分 R=U/I 计算式与电阻决定因素",
        ],
        "body": body,
        "feedback": feedback,
        "summary": [
            "能说出电阻的四个主要影响因素",
            "会解释变阻器“改长度→改电阻”",
            "不把 R=U/I 误读成电阻决定律",
            "会设计控制变量实验（比长度时）",
        ],
    }


def build_voltage() -> dict:
    cid = "phy-m-voltage"
    lab = r'''<section class="section" id="interactive-lab" data-tts="interactive-lab" data-interactive="U-lab"><div class="lesson-panel"><span class="phase-tag">互动实验</span>
<h2>串联电池个数与灯两端电压趋势</h2>
<div class="control-row"><label>串联节数 n<input id="u-n" type="range" min="1" max="4" value="2"></label></div>
<div class="canvas-wrap"><canvas id="physics-canvas" class="wide-canvas" width="900" height="320"></canvas></div>
<div id="lab-feedback" class="feedback"></div></div></section>
<script>
(function(){
  const canvas=document.getElementById('physics-canvas'); if(!canvas) return;
  const ctx=canvas.getContext('2d'); const nEl=document.getElementById('u-n'); const fb=document.getElementById('lab-feedback');
  function draw(){
    const n=+nEl.value, U=1.5*n;
    ctx.clearRect(0,0,canvas.width,canvas.height); ctx.fillStyle='#081426'; ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='#fbbf24'; ctx.font='26px PingFang SC,sans-serif'; ctx.fillText('理想：串联电源电压相加',60,50);
    ctx.fillStyle='#e2e8f0'; ctx.font='22px PingFang SC,sans-serif'; ctx.fillText('约 '+n+'×1.5 V ≈ '+U.toFixed(1)+' V',60,100);
    for(let i=0;i<n;i++){ ctx.fillStyle='#38bdf8'; ctx.fillRect(80+i*90,180,70,60); ctx.fillStyle='#0b1628'; ctx.fillText((i+1)+'',105+i*90,218); }
    fb.textContent='电压表必须并联；注意正负与量程。串联分压、并联电压相等（后面课会用）。';
  }
  nEl.addEventListener('input',draw); draw();
})();
</script>'''
    feedback = {
        "pretest": "电压表要并联在被测部分两端，注意正负与量程。",
        "l1a": "电压单位是伏特（V）。",
        "l1b": "电压表并联。",
        "l2a": "串联电路总电压等于各部分电压之和（理想）。",
        "l2b": "并联各支路电压相等（等于电源电压，理想）。",
        "l3a": "测灯泡电压：电压表与灯泡并联。",
        "open": "量规：①电压是两点间；②推动电荷；③电压表并联。",
    }
    body = f'''{LESSON_STYLE}
<section class="slide-page" data-page-index="4" data-page-type="content" data-tsh="真实情境">
<section class="section" id="story" data-tts="story"><div class="lesson-panel"><span class="phase-tag">真实情境</span>
<h2>为什么电池没电，灯就不亮？</h2>
<p>电池提供<strong>电压</strong>：推动电荷形成电流。电压不足，电流变小，灯就暗甚至不亮。</p>
<div class="mini-grid">
<div class="mini-panel"><h3>已有经验</h3><p>1.5 V 干电池、手机电池、家庭 220 V。</p></div>
<div class="mini-panel"><h3>真正卡点</h3><p>电压表串联；说“某一点的电压”。</p></div>
<div class="mini-panel"><h3>本课任务</h3><p>电压含义 → 测量 → 串并联电压关系铺垫。</p></div>
</div></div></section></section>

<section class="slide-page" data-page-index="5" data-page-type="content" data-tsh="前测">
<section class="section" id="pretest" data-tts="pretest" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">前测</span>
<h2>测小灯泡两端电压，电压表应</h2>
<button class="quiz-option" onclick="checkAnswer(this,true,'pretest')">A. 与灯泡并联</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">B. 与灯泡串联</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">C. 直接接电源两极且无量程限制</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">D. 正负接反也完全无影响</button>
<div id="pretest-feedback" class="feedback">先选再看解析。</div>
</div></section></section>

<section class="slide-page" data-page-index="6" data-page-type="content" data-tsh="核心">
<section class="section" id="core" data-tts="core"><div class="lesson-panel"><span class="phase-tag">核心概念</span>
<h2>电压：推动电荷的“压力差”</h2>
<div class="mini-grid">
<div class="mini-panel"><h3>含义</h3><p>电压是<strong>两点之间</strong>的物理量，不是单点属性。</p></div>
<div class="mini-panel"><h3>测量</h3><p>电压表并联；红正黑负；先大量程。</p></div>
<div class="mini-panel"><h3>电源</h3><p>电源作用是维持电路两端电压。</p></div>
</div>
{labeled_img(cid,'section1','电压表并联示意（无字）','电压表与被测用电器并联。',[('电源','25%','25%'),('灯泡','45%','55%'),('电压表并联','70%','70%')])}
</div></section></section>

<section class="slide-page" data-page-index="7" data-page-type="content" data-tsh="易混">
<section class="section" id="deep-understanding" data-tts="deep-understanding"><div class="lesson-panel"><span class="phase-tag">易混辨析</span>
<h2>串联分压 · 并联电压相等</h2>
<ul class="steps">
<li>串联：总电压≈各部分电压之和。</li>
<li>并联：各支路电压相等（理想）。</li>
</ul>
{labeled_img(cid,'section2','电压高低直觉（无字）','可用水位差类比“推动”，但最终要落到电路测量。',[('高水位','30%','35%'),('低水位','70%','65%'),('“推动”直觉','50%','50%')])}
</div></section></section>

<section class="slide-page" data-page-index="8" data-page-type="content" data-tsh="例题">
<section class="section" id="worked-example" data-tts="worked-example"><div class="lesson-panel"><span class="phase-tag">例题</span>
<h2>两节 1.5 V 电池串联，总电压约？</h2>
<ol class="steps"><li>理想串联相加：1.5+1.5=3.0 V。</li><li>并联同规格电池：电压仍约 1.5 V，可提供更大电流能力（定性）。</li></ol>
</div></section></section>

<section class="slide-page" data-page-index="9" data-page-type="content" data-tsh="互动">{lab}</section>

<section class="slide-page" data-page-index="10" data-page-type="content" data-tsh="L1">
<section class="section" id="practice-l1" data-tts="practice-l1"><div class="lesson-panel"><span class="phase-tag">练习 L1</span><h2>基础巩固</h2>
{quiz('l1a','1. 单位','电压的单位是',
[('A. 安培 A',False),('B. 伏特 V',True),('C. 欧姆 Ω',False),('D. 瓦特 W',False)])}
{quiz('l1b','2. 接法','电压表在电路中应',
[('A. 串联',False),('B. 并联',True),('C. 随便接',False),('D. 与电流表串联即可',False)])}
</div></section></section>

<section class="slide-page" data-page-index="11" data-page-type="content" data-tsh="L2">
<section class="section" id="practice-l2" data-tts="practice-l2"><div class="lesson-panel"><span class="phase-tag">练习 L2</span><h2>能力应用</h2>
{quiz('l2a','3. 串联','两电阻串联，电源电压 6 V，若一个两端 2 V，另一个约为',
[('A. 2 V',False),('B. 4 V',True),('C. 6 V',False),('D. 8 V',False)])}
{quiz('l2b','4. 并联','两灯并联在 3 V 电源上，每灯两端电压约为',
[('A. 1.5 V',False),('B. 3 V',True),('C. 6 V',False),('D. 0 V',False)])}
</div></section></section>

<section class="slide-page" data-page-index="12" data-page-type="content" data-tsh="L3">
<section class="section" id="practice-l3" data-tts="practice-l3"><div class="lesson-panel"><span class="phase-tag">练习 L3</span><h2>迁移</h2>
{quiz('l3a','5. 操作','要测灯泡两端电压，正确操作是',
[('A. 电压表与灯并联，注意量程与正负',True),('B. 电压表与灯串联',False),('C. 只接电流表',False),('D. 电压表跨接电源再串联灯',False)])}
<div class="practice-block"><h3>6. 开放产出</h3>
<p>为什么不能说“这个点的电压是 3 V”，而要说“这两点之间电压是 3 V”？</p>
<textarea id="l3-open" rows="3" style="width:100%;margin-top:8px;padding:10px;border-radius:8px;border:1px solid rgba(148,163,184,.3);background:#0b1628;color:#e2e8f0"></textarea>
<button type="button" class="quiz-option" style="margin-top:10px;text-align:center" onclick="showOpenRubric()">对照量规自检</button>
<div id="l3-open-feedback" class="feedback" hidden></div></div>
</div></section></section>
'''
    return {
        "cid": cid,
        "center": "电压",
        "hero_tags": [
            ("电源作用", "18%", "18%"),
            ("电压表并联", "18%", "82%"),
            ("两点之间", "48%", "12%"),
            ("串联相加", "48%", "88%"),
            ("并联相等", "78%", "22%"),
            ("量程与正负", "78%", "78%"),
        ],
        "caption": "无字生图 + 中文叠标：含义 · 测量 · 串并联关系",
        "anchors": [
            ("电压是什么？怎样测量？", "电压是什么？怎样测量？"),
            ("串联、并联时电压怎么分配？", "串联、并联时电压怎么分配？"),
            ("电池没电灯为什么不亮？", "电池没电灯为什么不亮？"),
        ],
        "objectives": [
            "理解电压是两点之间的物理量",
            "会正确使用电压表（并联、正负、量程）",
            "会用串联分压、并联电压相等做简单判断",
        ],
        "body": body,
        "feedback": feedback,
        "summary": [
            "能说明电压是“两点之间”的量",
            "会正确连接电压表",
            "会判断串联分压、并联电压相等",
            "能解释电池没电灯不亮的电路原因",
        ],
    }


def build_series_parallel() -> dict:
    cid = "phy-m-series-parallel"
    lab = r'''<section class="section" id="interactive-lab" data-tts="interactive-lab" data-interactive="sp-lab"><div class="lesson-panel"><span class="phase-tag">互动实验</span>
<h2>串联断一盏 vs 并联断一盏</h2>
<div class="control-row">
<label>连接方式
<select id="sp-mode" style="width:100%;min-height:44px;background:#0b1628;color:#eef6ff;border:1px solid rgba(148,163,184,.3);border-radius:8px">
<option value="series">串联</option><option value="parallel">并联</option></select></label>
<label>灯2状态
<select id="sp-b2" style="width:100%;min-height:44px;background:#0b1628;color:#eef6ff;border:1px solid rgba(148,163,184,.3);border-radius:8px">
<option value="ok">完好</option><option value="break">断路</option></select></label>
</div>
<div class="canvas-wrap"><canvas id="physics-canvas" class="wide-canvas" width="900" height="320"></canvas></div>
<div id="lab-feedback" class="feedback"></div></div></section>
<script>
(function(){
  const canvas=document.getElementById('physics-canvas'); if(!canvas) return;
  const ctx=canvas.getContext('2d');
  const mode=document.getElementById('sp-mode'), b2=document.getElementById('sp-b2'), fb=document.getElementById('lab-feedback');
  function bulb(x,y,on){ ctx.beginPath(); ctx.arc(x,y,28,0,Math.PI*2); ctx.fillStyle=on?'#fbbf24':'#334155'; ctx.fill(); }
  function draw(){
    const series=mode.value==='series'; const ok2=b2.value==='ok';
    ctx.clearRect(0,0,canvas.width,canvas.height); ctx.fillStyle='#081426'; ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.strokeStyle='#94a3b8'; ctx.lineWidth=4; ctx.beginPath();
    if(series){
      ctx.moveTo(120,160); ctx.lineTo(780,160); ctx.stroke();
      const on1=ok2, on2=ok2; bulb(300,160,on1); bulb(560,160,on2);
      fb.textContent=ok2?'串联：同一路径，两灯都亮。':'串联：一处断路，两灯都不亮。';
    } else {
      ctx.moveTo(150,80); ctx.lineTo(150,240); ctx.lineTo(750,240); ctx.lineTo(750,80); ctx.lineTo(150,80); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(150,160); ctx.lineTo(750,160); ctx.stroke();
      bulb(300,80,true); bulb(560,80,ok2);
      fb.textContent=ok2?'并联：两支路都亮。':'并联：灯2断路，灯1仍可亮。';
    }
    ctx.fillStyle='#e2e8f0'; ctx.font='22px PingFang SC,sans-serif'; ctx.fillText(series?'串联一条路径':'并联多条支路',60,50);
  }
  mode.addEventListener('change',draw); b2.addEventListener('change',draw); draw();
})();
</script>'''
    feedback = {
        "pretest": "串联一条路径，一处断路全灭；并联各支路相对独立。",
        "l1a": "串联电流处处相等（理想）。",
        "l1b": "并联各支路电压相等（理想）。",
        "l2a": "串联总电阻大于任一分电阻。",
        "l2b": "并联总电阻小于任一支路电阻。",
        "l3a": "家用电器通常并联，互不影响。",
        "open": "量规：①路径条数；②一盏坏了是否全灭；③电流/电压谁相等。",
    }
    body = f'''{LESSON_STYLE}
<section class="slide-page" data-page-index="4" data-page-type="content" data-tsh="真实情境">
<section class="section" id="story" data-tts="story"><div class="lesson-panel"><span class="phase-tag">真实情境</span>
<h2>一串旧彩灯：一盏坏了全都不亮？</h2>
<p>旧式彩灯常<strong>串联</strong>：一条路径，一处断路全灭。家里灯大多<strong>并联</strong>：一盏坏了，其他还能亮。</p>
<div class="mini-grid">
<div class="mini-panel"><h3>已有经验</h3><p>开关控制、插座互不影响。</p></div>
<div class="mini-panel"><h3>真正卡点</h3><p>串并联电流电压规律记混。</p></div>
<div class="mini-panel"><h3>本课任务</h3><p>识别连接 → 规律表 → 生活迁移。</p></div>
</div></div></section></section>

<section class="slide-page" data-page-index="5" data-page-type="content" data-tsh="前测">
<section class="section" id="pretest" data-tts="pretest" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">前测</span>
<h2>两灯串联，一盏灯丝烧断，另一盏</h2>
<button class="quiz-option" onclick="checkAnswer(this,true,'pretest')">A. 也不亮</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">B. 一定更亮</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">C. 不受影响照常亮</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">D. 电源电压变为两倍</button>
<div id="pretest-feedback" class="feedback">先选再看解析。</div>
</div></section></section>

<section class="slide-page" data-page-index="6" data-page-type="content" data-tsh="核心">
<section class="section" id="core" data-tts="core"><div class="lesson-panel"><span class="phase-tag">核心概念</span>
<h2>串联一条路 · 并联多条路</h2>
<div class="mini-grid">
<div class="mini-panel"><h3>串联</h3><p>电流相等；电压相加；总电阻变大。</p></div>
<div class="mini-panel"><h3>并联</h3><p>电压相等；电流相加；总电阻变小。</p></div>
<div class="mini-panel"><h3>识别</h3><p>看电流路径：是否“只有一条必经之路”。</p></div>
</div>
{labeled_img(cid,'section1','串并联对照（无字）','左串右并：先数路径，再套规律。',[('串联','35%','28%'),('并联','35%','72%'),('一条路径','70%','28%'),('多条支路','70%','72%')])}
</div></section></section>

<section class="slide-page" data-page-index="7" data-page-type="content" data-tsh="易混">
<section class="section" id="deep-understanding" data-tts="deep-understanding"><div class="lesson-panel"><span class="phase-tag">易混辨析</span>
<h2>不要只背口诀，先画路径</h2>
<ul class="steps">
<li>断路：串联全灭；并联通常只灭该支路。</li>
<li>短路危险：并联支路被导线直接接通时电流过大。</li>
</ul>
{labeled_img(cid,'section2','生活对照（无字）','彩灯串 vs 房间灯：连接方式不同，故障表现不同。',[('串联彩灯','40%','30%'),('并联用电器','40%','70%')])}
</div></section></section>

<section class="slide-page" data-page-index="8" data-page-type="content" data-tsh="例题">
<section class="section" id="worked-example" data-tts="worked-example"><div class="lesson-panel"><span class="phase-tag">例题</span>
<h2>两灯分别 3 V、电流路径分析</h2>
<ol class="steps"><li>若串联接 6 V：电流相同，电压可相加分配。</li><li>若并联接 3 V：每灯约 3 V，干路电流为支路之和。</li></ol>
</div></section></section>

<section class="slide-page" data-page-index="9" data-page-type="content" data-tsh="互动">{lab}</section>

<section class="slide-page" data-page-index="10" data-page-type="content" data-tsh="L1">
<section class="section" id="practice-l1" data-tts="practice-l1"><div class="lesson-panel"><span class="phase-tag">练习 L1</span><h2>基础巩固</h2>
{quiz('l1a','1. 串联电流','串联电路中，电流',
[('A. 处处相等（理想）',True),('B. 到处不同',False),('C. 只在电源最大',False),('D. 无法比较',False)])}
{quiz('l1b','2. 并联电压','并联电路中，各支路电压',
[('A. 一定不同',False),('B. 相等（理想）',True),('C. 之和等于电源电压',False),('D. 为零',False)])}
</div></section></section>

<section class="slide-page" data-page-index="11" data-page-type="content" data-tsh="L2">
<section class="section" id="practice-l2" data-tts="practice-l2"><div class="lesson-panel"><span class="phase-tag">练习 L2</span><h2>能力应用</h2>
{quiz('l2a','3. 总电阻','两电阻串联后总电阻',
[('A. 比任何一个都小',False),('B. 比任何一个都大',True),('C. 一定等于较小者',False),('D. 一定为零',False)])}
{quiz('l2b','4. 并联总阻','两电阻并联后总电阻',
[('A. 比任何一个都大',False),('B. 比任何一个都小',True),('C. 等于两电阻之和',False),('D. 一定更大',False)])}
</div></section></section>

<section class="slide-page" data-page-index="12" data-page-type="content" data-tsh="L3">
<section class="section" id="practice-l3" data-tts="practice-l3"><div class="lesson-panel"><span class="phase-tag">练习 L3</span><h2>迁移</h2>
{quiz('l3a','5. 生活','家用台灯、电视通常怎样连接？',
[('A. 串联，一坏全灭',False),('B. 并联，互不影响',True),('C. 无法判断',False),('D. 必须混联才行',False)])}
<div class="practice-block"><h3>6. 开放产出</h3>
<p>用“路径条数 + 故障现象”说明如何判断是串联还是并联。</p>
<textarea id="l3-open" rows="3" style="width:100%;margin-top:8px;padding:10px;border-radius:8px;border:1px solid rgba(148,163,184,.3);background:#0b1628;color:#e2e8f0"></textarea>
<button type="button" class="quiz-option" style="margin-top:10px;text-align:center" onclick="showOpenRubric()">对照量规自检</button>
<div id="l3-open-feedback" class="feedback" hidden></div></div>
</div></section></section>
'''
    return {
        "cid": cid,
        "center": "串并联",
        "hero_tags": [
            ("串联路径", "18%", "18%"),
            ("并联支路", "18%", "82%"),
            ("电流规律", "48%", "12%"),
            ("电压规律", "48%", "88%"),
            ("断路现象", "78%", "22%"),
            ("生活应用", "78%", "78%"),
        ],
        "caption": "无字生图 + 中文叠标：识别连接 · 规律 · 故障 · 生活",
        "anchors": [
            ("怎样判断串联还是并联？", "怎样判断串联还是并联？"),
            ("串并联的电流电压规律是什么？", "串并联的电流电压规律是什么？"),
            ("为什么家里灯一盏坏了其他还亮？", "为什么家里灯一盏坏了其他还亮？"),
        ],
        "objectives": [
            "能根据路径识别串并联",
            "掌握串并联电流、电压、电阻基本规律",
            "能解释彩灯与家用电路的故障差异",
        ],
        "body": body,
        "feedback": feedback,
        "summary": [
            "会用“路径条数”识别串并联",
            "记住串并联电流/电压基本规律",
            "能解释串联断路全灭、并联相对独立",
            "能说明家用电器为何常用并联",
        ],
    }


def build_simple_machines() -> dict:
    cid = "phy-m-simple-machines"
    lab = r'''<section class="section" id="interactive-lab" data-tts="interactive-lab" data-interactive="lever-lab"><div class="lesson-panel"><span class="phase-tag">互动实验</span>
<h2>调动力臂与阻力，看所需动力</h2>
<p style="color:var(--muted)">理想杠杆：F₁ = F₂·L₂ / L₁</p>
<div class="control-row">
<label>阻力 F₂（N）<input id="lev-f2" type="range" min="50" max="800" step="10" value="400"></label>
<label>阻力臂 L₂（cm）<input id="lev-l2" type="range" min="10" max="80" value="20"></label>
<label>动力臂 L₁（cm）<input id="lev-l1" type="range" min="20" max="150" value="100"></label>
</div>
<div class="canvas-wrap"><canvas id="physics-canvas" class="wide-canvas" width="900" height="360"></canvas></div>
<div id="lab-feedback" class="feedback"></div></div></section>
<script>
(function(){
  const canvas=document.getElementById('physics-canvas'); if(!canvas) return;
  const ctx=canvas.getContext('2d');
  const f2=document.getElementById('lev-f2'), l2=document.getElementById('lev-l2'), l1=document.getElementById('lev-l1');
  const fb=document.getElementById('lab-feedback');
  function draw(){
    const F2=+f2.value, L2=+l2.value/100, L1=+l1.value/100, F1=F2*L2/L1;
    ctx.clearRect(0,0,canvas.width,canvas.height); ctx.fillStyle='#081426'; ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.strokeStyle='#94a3b8'; ctx.lineWidth=8; ctx.beginPath(); ctx.moveTo(120,220); ctx.lineTo(780,220); ctx.stroke();
    ctx.fillStyle='#f97316'; ctx.beginPath(); ctx.moveTo(450,220); ctx.lineTo(430,260); ctx.lineTo(470,260); ctx.fill();
    ctx.fillStyle='#fbbf24'; ctx.font='26px PingFang SC,sans-serif'; ctx.fillText('F₁≈'+F1.toFixed(1)+' N',60,50);
    ctx.fillStyle='#e2e8f0'; ctx.font='20px PingFang SC,sans-serif';
    ctx.fillText('F₂='+F2+' N · L₂='+(L2*100|0)+' cm · L₁='+(L1*100|0)+' cm',60,90);
    fb.textContent=(L1>L2?'省力杠杆：动力更小，但手移动距离更大。':'费力杠杆：动力更大，但可省距离/更灵活。')+' 省力不省功。';
  }
  [f2,l2,l1].forEach(el=>el.addEventListener('input',draw)); draw();
})();
</script>'''
    feedback = {
        "pretest": "省力往往费距离；机械不能使有用功大于总功；定滑轮不省力。",
        "l1a": "动力臂大于阻力臂 → 省力。",
        "l1b": "定滑轮不省力，只改变力的方向。",
        "l2a": "F₁L₁=F₂L₂。",
        "l2b": "机械效率 η=W有用/W总 < 1（通常）。",
        "l3a": "瓶起子：动力臂更长，省力杠杆。",
        "open": "量规：①支点；②动力臂/阻力臂谁长；③是否省力及代价。",
    }
    body = f'''{LESSON_STYLE}
<section class="slide-page" data-page-index="4" data-page-type="content" data-tsh="真实情境">
<section class="section" id="story" data-tts="story"><div class="lesson-panel"><span class="phase-tag">真实情境</span>
<h2>为什么一根撬棍能撬起大石头？</h2>
<p>撬棍是杠杆：动力臂更长时，可用更小的力——但手要移动更远。<strong>省力不省功</strong>。</p>
<div class="mini-grid">
<div class="mini-panel"><h3>已有经验</h3><p>剪刀、瓶起子、旗杆定滑轮、斜坡。</p></div>
<div class="mini-panel"><h3>真正卡点</h3><p>以为机械可以“凭空省功”；力臂当成杆长。</p></div>
<div class="mini-panel"><h3>本课任务</h3><p>杠杆条件 → 滑轮 → 效率。</p></div>
</div></div></section></section>

<section class="slide-page" data-page-index="5" data-page-type="content" data-tsh="前测">
<section class="section" id="pretest" data-tts="pretest" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">前测</span>
<h2>正确的是？</h2>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">A. 省力杠杆一定省距离</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'pretest')">B. 省力往往费距离；费力往往省距离</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">C. 简单机械可以让有用功大于总功</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">D. 定滑轮一定省力一半</button>
<div id="pretest-feedback" class="feedback">先选再看解析。</div>
</div></section></section>

<section class="slide-page" data-page-index="6" data-page-type="content" data-tsh="核心">
<section class="section" id="core" data-tts="core"><div class="lesson-panel"><span class="phase-tag">核心概念</span>
<h2>杠杆 · 滑轮 · 效率</h2>
<div class="mini-grid">
<div class="mini-panel"><h3>杠杆</h3><p>F₁L₁=F₂L₂。动力臂&gt;阻力臂→省力。</p></div>
<div class="mini-panel"><h3>滑轮</h3><p>定滑轮：不省力，改方向。动滑轮：理想省一半力，费距离。</p></div>
<div class="mini-panel"><h3>效率</h3><p>η=W有用/W总。额外功来自摩擦、自重，η&lt;1。</p></div>
</div>
{labeled_img(cid,'section1','撬棍杠杆（无字）','先找支点，再比较动力臂与阻力臂。',[('动力','30%','20%'),('支点','55%','48%'),('阻力','35%','78%')])}
</div></section></section>

<section class="slide-page" data-page-index="7" data-page-type="content" data-tsh="易混">
<section class="section" id="deep-understanding" data-tts="deep-understanding"><div class="lesson-panel"><span class="phase-tag">易混辨析</span>
<h2>省力 ≠ 省功</h2>
<ul class="steps">
<li>力臂是支点到力的作用线的<strong>垂直距离</strong>。</li>
<li>任何机械都不能使有用功大于总功。</li>
</ul>
{labeled_img(cid,'section2','定滑轮与动滑轮（无字）','定滑轮不省力；动滑轮省力但费距离。',[('定滑轮改方向','35%','28%'),('动滑轮省力','40%','72%'),('费距离','75%','70%')])}
</div></section></section>

<section class="slide-page" data-page-index="8" data-page-type="content" data-tsh="例题">
<section class="section" id="worked-example" data-tts="worked-example"><div class="lesson-panel"><span class="phase-tag">例题</span>
<h2>阻力 600 N，阻力臂 0.2 m，动力臂 1.2 m</h2>
<ol class="steps"><li>F₁=F₂L₂/L₁=600×0.2/1.2=100 N。</li><li>代价：动力端移动距离更大。</li></ol>
</div></section></section>

<section class="slide-page" data-page-index="9" data-page-type="content" data-tsh="互动">{lab}</section>

<section class="slide-page" data-page-index="10" data-page-type="content" data-tsh="L1">
<section class="section" id="practice-l1" data-tts="practice-l1"><div class="lesson-panel"><span class="phase-tag">练习 L1</span><h2>基础巩固</h2>
{quiz('l1a','1. 省力条件','杠杆省力的条件是',
[('A. 动力臂大于阻力臂',True),('B. 动力臂小于阻力臂',False),('C. 两臂相等必省力',False),('D. 与力臂无关',False)])}
{quiz('l1b','2. 定滑轮','定滑轮的主要作用是',
[('A. 一定省一半力',False),('B. 改变力的方向',True),('C. 增大有用功',False),('D. 消除摩擦',False)])}
</div></section></section>

<section class="slide-page" data-page-index="11" data-page-type="content" data-tsh="L2">
<section class="section" id="practice-l2" data-tts="practice-l2"><div class="lesson-panel"><span class="phase-tag">练习 L2</span><h2>能力应用</h2>
{quiz('l2a','3. 平衡','理想杠杆平衡条件是',
[('A. F₁=F₂',False),('B. F₁L₁=F₂L₂',True),('C. L₁=L₂',False),('D. F₁/L₁=F₂/L₂',False)])}
{quiz('l2b','4. 效率','机械效率通常',
[('A. 大于 1',False),('B. 小于 1',True),('C. 一定等于 1',False),('D. 可为负数',False)])}
</div></section></section>

<section class="slide-page" data-page-index="12" data-page-type="content" data-tsh="L3">
<section class="section" id="practice-l3" data-tts="practice-l3"><div class="lesson-panel"><span class="phase-tag">练习 L3</span><h2>迁移</h2>
{quiz('l3a','5. 工具','瓶起子开瓶盖，一般是',
[('A. 省力杠杆',True),('B. 费力杠杆',False),('C. 定滑轮',False),('D. 不能省力',False)])}
<div class="practice-block"><h3>6. 开放产出</h3>
<p>任选家中一件工具，指出支点、动力臂、阻力臂，并判断省力还是费力。</p>
<textarea id="l3-open" rows="3" style="width:100%;margin-top:8px;padding:10px;border-radius:8px;border:1px solid rgba(148,163,184,.3);background:#0b1628;color:#e2e8f0"></textarea>
<button type="button" class="quiz-option" style="margin-top:10px;text-align:center" onclick="showOpenRubric()">对照量规自检</button>
<div id="l3-open-feedback" class="feedback" hidden></div></div>
</div></section></section>
'''
    return {
        "cid": cid,
        "center": "简单机械",
        "hero_tags": [
            ("杠杆平衡", "18%", "18%"),
            ("动力臂/阻力臂", "18%", "82%"),
            ("定滑轮", "48%", "12%"),
            ("动滑轮", "48%", "88%"),
            ("省力不省功", "78%", "22%"),
            ("机械效率", "78%", "78%"),
        ],
        "caption": "无字生图 + 中文叠标：杠杆 · 滑轮 · 效率",
        "anchors": [
            ("杠杆怎样省力？", "杠杆怎样省力？"),
            ("定滑轮和动滑轮有何不同？", "定滑轮和动滑轮有何不同？"),
            ("机械效率为什么小于 1？", "机械效率为什么小于 1？"),
        ],
        "objectives": [
            "能用杠杆平衡条件解释省力/费力",
            "区分定滑轮与动滑轮",
            "理解有用功、额外功与机械效率",
        ],
        "body": body,
        "feedback": feedback,
        "summary": [
            "会用 F₁L₁=F₂L₂ 判断省力/费力",
            "能区分定滑轮与动滑轮",
            "理解省力不省功",
            "能解释机械效率为何通常小于 1",
        ],
    }


def apply_course(cfg: dict) -> str:
    cid = cfg["cid"]
    path = COMMUNITY / cid / "index.html"
    if not path.exists():
        return f"{cid}: missing"
    html = path.read_text(encoding="utf-8")

    if 'id="ta-labeled-figure-css"' not in html:
        html = html.replace("</head>", LABEL_CSS + "\n</head>", 1)
    else:
        html = re.sub(
            r'<style id="ta-labeled-figure-css">[\s\S]*?</style>',
            LABEL_CSS.strip(),
            html,
            count=1,
        )

    # Fix nav/body if broken
    html = re.sub(
        r"</head>\s*<nav[\s\S]*?</nav>\s*<body[^>]*>",
        f'</head>\n<body class="teachany-middle">\n<nav class="teachany-page-nav" style="margin:12px auto;max-width:1080px;padding:8px 14px;display:flex;gap:14px;flex-wrap:wrap;font-size:14px;background:rgba(245,247,250,.08);border:1px solid rgba(148,163,184,.18);border-radius:10px;"><a href="#knowledge-graph">📑 知识图谱</a><a href="#teachany-ai-tutor-card">🤝 AI 学伴</a><a href="#story">📚 课程内容</a></nav>\n',
        html,
        count=1,
    )

    hero = hero_fig(cid, cfg["center"], cfg["hero_tags"], cfg["caption"])
    html = re.sub(
        r'<section[^>]*id="hero-infographic"[\s\S]*?</section>\s*</section>',
        hero + "\n</section>",
        html,
        count=1,
    )

    # Anchors
    choices = "\n".join(
        f'<button class="choice" data-anchor-choice="{a}">{t}</button>' for a, t in cfg["anchors"]
    )
    html = re.sub(
        r'(<div class="grid" id="problem-anchor-choices">)[\s\S]*?(</div>)',
        rf"\1\n{choices}\n\2",
        html,
        count=1,
    )

    # Objectives
    objs = "\n".join(f"<li>{o}</li>" for o in cfg["objectives"])
    html = re.sub(
        r'(<ul class="objectives">)[\s\S]*?(</ul>)',
        rf"\1\n{objs}\n\2",
        html,
        count=1,
    )

    import json

    feedback_js = json.dumps(cfg["feedback"], ensure_ascii=False)
    summary = summary_block(cfg["summary"]).replace(
        "const FEEDBACK = PLACEHOLDER;", f"const FEEDBACK = {feedback_js};"
    )
    # summary_block had PLACEHOLDER via replace quirk — fix:
    summary = summary_block(cfg["summary"])
    summary = summary.replace("const FEEDBACK = PLACEHOLDER;", f"const FEEDBACK = {feedback_js};")
    if "PLACEHOLDER" in summary:
        summary = summary.replace("__FEEDBACK__", feedback_js).replace(
            "const FEEDBACK = PLACEHOLDER;", f"const FEEDBACK = {feedback_js};"
        )
    # Direct build summary script properly
    labels = "\n".join(
        f'      <label><input type="checkbox" class="recap-check"><span>{t}</span></label>'
        for t in cfg["summary"]
    )
    n = len(cfg["summary"])
    lesson = (
        cfg["body"]
        + f'''
<section class="slide-page" data-page-index="13" data-page-type="content" data-tsh="小结">
<section class="section" id="summary" data-tts="summary">
  <div class="lesson-panel">
    <span class="phase-tag">小结清单</span>
    <h2>这节课你应能做到</h2>
    <div class="checklist" id="summary-checklist">
{labels}
    </div>
    <p id="summary-feedback" class="feedback" style="margin-top:12px">勾选你已掌握的条目。</p>
  </div>
</section>
</section>
<script>
const FEEDBACK = {feedback_js};
function checkAnswer(btn,ok,target){{
  const root=btn.closest('.practice-block, .lesson-panel')||btn.parentElement;
  root.querySelectorAll('.quiz-option').forEach(b=>b.classList.remove('correct','wrong'));
  btn.classList.add(ok?'correct':'wrong');
  const box=document.getElementById(target+'-feedback');
  if(box) box.textContent=(ok?'✅ ':'❌ ')+(FEEDBACK[target]||'');
}}
function showOpenRubric(){{
  const box=document.getElementById('l3-open-feedback');
  if(!box) return;
  box.hidden=false;
  box.innerHTML=FEEDBACK.open||'对照量规补全要点。';
}}
document.querySelectorAll('.recap-check').forEach(cb=>{{
  cb.addEventListener('change',()=>{{
    const c=document.querySelectorAll('.recap-check:checked').length;
    const f=document.getElementById('summary-feedback');
    if(f) f.textContent=c?('已勾选 '+c+'/{n} 项。'):'勾选你已掌握的条目。';
  }});
}});
</script>
'''
    )

    pattern = re.compile(
        r'(?:<style>\.lesson-panel\{|<section class="slide-page" data-page-index="4")[\s\S]*?'
        r'<section class="slide-page" data-page-index="20"',
        re.M,
    )
    html2, nrep = pattern.subn(lesson + '\n<section class="slide-page" data-page-index="20"', html, count=1)
    if nrep != 1:
        return f"{cid}: lesson replace failed ({nrep})"
    html = html2

    html = re.sub(
        r"<!-- teachany-enhanced -->[\s\S]*?(?=<section class=\"section\" id=\"knowledge-graph\"|<section class=\"slide-page\" data-page-index=\"20\")",
        "",
        html,
        count=1,
    )
    # Also strip upgrade blocks after KG if present before knowledge-graph
    html = re.sub(
        r"<!-- teachany-enhanced -->[\s\S]*?(?=<section class=\"section\" id=\"knowledge-graph\")",
        "",
        html,
        count=1,
    )
    html = re.sub(
        r"<!-- teachany-upgrade-v2 -->[\s\S]*?(?=<section class=\"section\" id=\"knowledge-graph\")",
        "",
        html,
        count=1,
    )
    html = re.sub(
        r"<!-- upgrade topic:[\s\S]*?(?=<section class=\"section\" id=\"knowledge-graph\")",
        "",
        html,
        count=1,
    )

    path.write_text(html, encoding="utf-8")
    return f"{cid}: OK"


def main() -> None:
    courses = [build_resistance(), build_voltage(), build_series_parallel(), build_simple_machines()]
    for cfg in courses:
        # verify images exist
        assets = COMMUNITY / cfg["cid"] / "assets"
        for slot in ("hero", "section1", "section2"):
            p = assets / f"{cfg['cid']}-{slot}.png"
            if not p.exists() or p.stat().st_size < 20_000:
                print(f"{cfg['cid']}: WAIT image missing {p.name}")
        print(apply_course(cfg), flush=True)


if __name__ == "__main__":
    main()
