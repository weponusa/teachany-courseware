#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hand-crafted de-template rewrites for TeachAny physics courses.

Usage:
  python3 scripts/rewrite_physics_authentic.py phy-m-thermometer
  python3 scripts/rewrite_physics_authentic.py phy-m-thermometer phy-m-heat-calculation
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

UPGRADE_CSS_JS = r'''<style id="teachany-upgrade-v2-css">.teachany-upgrade-block{margin:28px 0;padding:22px;border-radius:16px;border:1px solid rgba(148,163,184,.25);background:rgba(15,23,42,.35)}.tu-q,.tu-fill{margin:16px 0;padding:14px;border-radius:12px;background:rgba(30,41,59,.45)}.tu-opts{display:grid;gap:10px;margin-top:10px}.tu-opt{text-align:left;padding:12px 14px;border-radius:10px;border:1px solid rgba(148,163,184,.35);background:rgba(51,65,85,.55);color:inherit;cursor:pointer;font-size:15px;line-height:1.5}.tu-opt:hover{border-color:#60a5fa}.tu-opt.is-right{border-color:#34d399;background:rgba(16,185,129,.18)}.tu-opt.is-wrong{border-color:#f87171;background:rgba(239,68,68,.15)}.tu-fb{margin-top:12px;padding:12px;border-radius:10px;background:rgba(245,158,11,.12);border:1px solid rgba(245,158,11,.35);line-height:1.7}.tu-inquiry{display:grid;gap:12px;margin:14px 0}.tu-inquiry textarea{width:100%;min-height:72px;margin-top:6px;border-radius:8px;padding:10px;border:1px solid rgba(148,163,184,.3);background:rgba(15,23,42,.5);color:inherit}.tu-save{margin-top:8px;padding:10px 16px;border-radius:10px;border:0;background:#3b82f6;color:#fff;cursor:pointer;font-weight:600}details{margin-top:8px}summary{cursor:pointer;color:#93c5fd}</style>
<script id="teachany-upgrade-v2-js">(function(){function bind(root){root.querySelectorAll('.tu-q,.teachany-upgrade-block[data-interactive="conceptest"]').forEach(function(box){var ans=box.getAttribute('data-answer');var fb=box.querySelector('.tu-fb');box.querySelectorAll('.tu-opt').forEach(function(btn){btn.addEventListener('click',function(){var ch=btn.getAttribute('data-choice');var correct=btn.getAttribute('data-correct');var ok=(correct==='true')||(ans&&ch===ans);box.querySelectorAll('.tu-opt').forEach(function(b){b.classList.remove('is-right','is-wrong');});btn.classList.add(ok?'is-right':'is-wrong');if(fb){fb.hidden=false;fb.textContent=(ok?'✅ ':'❌ ')+(btn.getAttribute('data-diagnosis')||'');}});});});root.querySelectorAll('.tu-save').forEach(function(btn){btn.addEventListener('click',function(){var sec=btn.closest('section');var payload={};sec.querySelectorAll('[data-inq]').forEach(function(t){payload[t.getAttribute('data-inq')]=t.value;});try{localStorage.setItem('teachany_inq_'+location.pathname,JSON.stringify(payload));}catch(e){}var fb=sec.querySelector('[data-inq-fb]');if(fb){fb.hidden=false;fb.textContent='已保存到本机。';}});});}if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){bind(document);});else bind(document);})();</script>
'''

COURSES = {
    "phy-m-thermometer": {
        "subtitle": "发烧时听大人说“37.5℃”，这个数是怎么从温度计上读出来的？",
        "figcaption": "温度与温度计：热胀冷缩、摄氏温标、读数与使用注意",
        "anchors": [
            ("体温计为什么能测体温？", "体温计为什么能测体温？"),
            ("0℃ 和 100℃ 是怎么定的？", "0℃ 和 100℃ 是怎么定的？"),
            ("读温度计要注意什么？", "读温度计要注意什么？"),
        ],
        "objectives": [
            "能说明温度计利用液体热胀冷缩显示温度",
            "知道摄氏温标：冰水混合物 0℃、1 标准大气压沸水 100℃",
            "能正确读数，并说出使用温度计的关键注意点",
        ],
        "story": """<section class="section" id="story" data-tts="story" data-tsh="真实情境"><div class="lesson-panel"><span class="phase-tag">真实情境</span><h2>发烧了，温度计上的数字从哪来？</h2>
<p>妈妈把体温计夹在腋下几分钟，读出 37.8℃。玻璃管很细，里面那截银白色液体似乎“自己会涨”。温度计并不是魔法，它靠的是<strong>测温液体受热膨胀、遇冷收缩</strong>，再对照温标读出温度。</p>
<div class="mini-grid">
<div class="mini-panel"><h3>已有经验</h3><p>夏天柏油路发软、冬天水结冰；热水倒进玻璃杯有时会烫手——冷热变化无处不在。</p></div>
<div class="mini-panel"><h3>真正卡点</h3><p>容易把“感觉热”当成温度本身；也常搞不清 0℃/100℃ 怎么规定，以及读数时眼睛要平视刻度。</p></div>
<div class="mini-panel"><h3>本课任务</h3><p>弄清温度计原理 → 摄氏温标 → 会读数、会规范使用。</p></div>
</div>
<p><strong>一句话：</strong>温度描述冷热程度；温度计把冷热变成可见的液柱高度。</p>
</div></section>""",
        "checklist": """<section class="section" id="experiment-checklist" data-tts="experiment-checklist" data-bloom-level="analyze" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">实验检查表</span><h2>观察温度计：到底在测什么？</h2>
<p><strong>第一问：观察对象是谁？</strong>玻璃泡内液体的体积变化，表现为细管内液柱高度变化。</p>
<p><strong>第二问：条件是什么？</strong>玻璃泡要与被测物体充分接触，等待液柱稳定后再读数。</p>
<p><strong>第三问：证据是什么？</strong>液柱升高表示温度升高（在测温范围内）；读数必须平视刻度，避免视差。</p>
</div></section>""",
        "pretest": """<section class="section" id="pretest" data-tts="pretest" data-bloom-level="remember" data-scaffold="full" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">前测</span><h2>前测：温度计靠什么工作？</h2>
<p><strong>常用液体温度计能够显示温度，主要是因为</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,true,'pretest')">A. 测温液体热胀冷缩，液柱高度随温度变化</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">B. 玻璃管本身会发光显示数字</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">C. 温度计内部有电池供电</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">D. 只有水银温度计能测温度，酒精不行</button>
<div id="pretest-feedback" class="feedback">先选一项。关键：热胀冷缩 + 温标。</div></div></section>""",
        "core": """<section class="section" id="core" data-tts="core" data-bloom-level="understand" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">核心概念</span><h2>温度 · 温标 · 温度计</h2>
<div class="mini-grid">
<div class="mini-panel"><h3>温度</h3><p>表示物体冷热程度。感觉不可靠：同一盆水，一只手刚从冷水来、一只手刚从热水来，感觉会不同。</p></div>
<div class="mini-panel"><h3>摄氏温标</h3><p>规定：1 标准大气压下，冰水混合物为 0℃，沸水为 100℃，中间分成 100 等份。</p></div>
<div class="mini-panel"><h3>温度计</h3><p>常用液体温度计利用液体热胀冷缩。使用：不能超量程；玻璃泡充分接触；稳定后平视读数。</p></div>
</div></div></section>""",
        "deep": """<section class="section" id="deep-understanding" data-tts="deep-understanding"><div class="lesson-panel insight-box"><span class="phase-tag">易混辨析</span><h2>感觉热 ≠ 温度高</h2>
<ul>
<li><strong>感觉：</strong>受皮肤、环境、干湿影响，只能粗略判断。</li>
<li><strong>温度：</strong>用温度计测量，有明确温标和单位（℃）。</li>
<li><strong>体温计特殊结构：</strong>有缩口，离开人体后液柱不易自动退回，便于读数。</li>
<li><strong>记忆锚点：</strong>先接触、再等待、后平视。</li>
</ul>
</div></section>""",
        "worked": """<section class="section" id="worked-example" data-tts="worked-example" data-bloom-level="analyze" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">例题拆解</span><h2>例题：怎样正确读温度计？</h2>
<p>实验室温度计插入温水中，液柱稳定后，刻度显示液柱上表面对准 42 与 43 之间第 2 小格（每大格 1℃，分 10 小格）。</p>
<p><strong>读数：</strong>42.2℃（估读到分度值下一位的习惯按老师要求；此处强调平视与稳定）。</p>
<p class="feedback"><strong>高频错因：</strong>①未等稳定就读；②仰视/俯视造成偏大偏小；③玻璃泡碰到容器底/壁。</p>
</div></section>""",
        "transfer": """<section class="section" id="transfer-task" data-tts="transfer-task" data-bloom-level="create" data-scaffold="none"><div class="lesson-panel"><span class="phase-tag">迁移任务</span><h2>设计：给家里厨房选一支温度计</h2>
<p>写出：①要测什么（水温/油温/室温）；②量程大概需要多少；③为什么不能用量程不够的温度计；④读数时要注意哪两步。</p>
</div></section>""",
        "lab_html": """<section class="section" id="interactive-lab" data-tts="interactive-lab" data-bloom-level="apply" data-scaffold="partial" data-interactive="thermo-lab"><div class="lesson-panel"><span class="phase-tag">互动实验</span><h2>调温度，看液柱高度</h2>
<p style="color:var(--muted)">拖动温度。画布示意：温度升高 → 液柱升高（热胀冷缩示意，非某品牌真实刻度）。</p>
<div class="control-row"><label>温度 t（℃）<input id="th-temp" type="range" min="-10" max="100" step="1" value="37"></label></div>
<div class="canvas-wrap"><canvas id="physics-canvas" class="wide-canvas" width="900" height="430" aria-label="温度计液柱示意"></canvas></div>
<div id="lab-feedback" class="feedback">先调到 0℃ 与 100℃，想象冰水与沸水两个定点。</div></div></section>
<script>
(function(){
  const canvas=document.getElementById('physics-canvas'); if(!canvas) return;
  const ctx=canvas.getContext('2d');
  const el=document.getElementById('th-temp');
  const fb=document.getElementById('lab-feedback');
  function draw(){
    const t=+el.value;
    const h=Math.max(20, ((t+10)/110)*260);
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='#081426'; ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.strokeStyle='#94a3b8'; ctx.lineWidth=5; ctx.strokeRect(520,80,50,300);
    ctx.beginPath(); ctx.arc(545,390,28,0,Math.PI*2); ctx.fillStyle='#38bdf8'; ctx.fill();
    ctx.fillStyle='#38bdf8'; ctx.fillRect(530,380-h,30,h);
    ctx.fillStyle='#fbbf24'; ctx.font='28px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('液体温度计示意',80,70);
    ctx.fillStyle='#e2e8f0'; ctx.font='24px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('当前温度 t = '+t+' ℃',80,120);
    ctx.fillText('液柱随温度升高而升高（热胀）',80,160);
    ctx.fillStyle='#94a3b8'; ctx.font='20px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('0℃：冰水混合物　100℃：1atm 沸水',80,400);
    fb.textContent='t='+t+'℃。想想：读数时为什么要平视？离开被测液体前要不要先读实验室温度计？';
  }
  el.addEventListener('input',draw); draw();
})();
</script>
<script>const FEEDBACK={pretest:"液体温度计利用热胀冷缩，把温度变成液柱高度。",posttest:"摄氏温标：冰水混合物 0℃，1 标准大气压沸水 100℃。"};
function checkAnswer(btn,ok,target){btn.parentElement.querySelectorAll('.quiz-option').forEach(b=>b.classList.remove('correct','wrong'));btn.classList.add(ok?'correct':'wrong');const box=document.getElementById(target+'-feedback');if(box)box.textContent=ok?('✅ '+FEEDBACK[target]):('❌ 再想想：'+FEEDBACK[target]);}</script>
""",
        "external": """<section class="section" id="external-sim" data-tts="external-sim"><div class="lesson-panel"><span class="phase-tag">实验回放</span><h2>温度计课三句话</h2>
<ol><li>温度描述冷热程度，感觉不可靠。</li><li>液体温度计靠热胀冷缩工作。</li><li>摄氏温标有两个定点：0℃ 与 100℃；读数要稳定、平视。</li></ol>
</div></section>""",
        "posttest": """<section class="section" id="posttest" data-tts="posttest" data-bloom-level="evaluate" data-scaffold="none" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">后测</span><h2>后测：温标与使用</h2>
<p><strong>关于摄氏温标，正确的是？</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">A. 0℃ 是水开始结冰的任意温度，与气压无关</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'posttest')">B. 1 标准大气压下，冰水混合物为 0℃，沸水为 100℃</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">C. 100℃ 是人体正常体温</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">D. 温度计液柱越高，温度一定越低</button>
<div id="posttest-feedback" class="feedback">先独立判断两个定点。</div></div></section>""",
        "summary": """<section class="section" id="summary" data-tts="summary"><div class="lesson-panel"><span class="phase-tag">一句话带走</span><h2>温度计课过关标准</h2>
<ul><li>能说出温度计原理是热胀冷缩。</li><li>能写出摄氏温标两个定点。</li><li>能描述正确读数与使用注意。</li></ul>
<p class="feedback">如果你能解释“体温计为什么离开人体还能读数”，这节课就过关了。</p>
</div></section>""",
        "upgrade": """<!-- teachany-upgrade-v2 -->
<!-- upgrade topic: 温度与温度计（去套路） -->
<section class="section teachany-upgrade-block" data-bloom-level="evaluate" data-scaffold="partial"><h2>📝 中考风格真题</h2>
<div class="tu-q" data-answer="B"><h3>选择题 1</h3><p>使用实验室温度计测量液体温度时，正确的是</p><div class="tu-opts">
<button type="button" class="tu-opt" data-choice="A" data-diagnosis="玻璃泡碰到容器底/壁会导致读数不准">A. 玻璃泡紧贴容器底部</button>
<button type="button" class="tu-opt" data-choice="B" data-diagnosis="要充分接触并等待稳定后平视读数">B. 玻璃泡浸没在液体中，稳定后平视读数</button>
<button type="button" class="tu-opt" data-choice="C" data-diagnosis="读数前不应随意离开液体（实验室温度计）">C. 先取出再读数，与体温计一样</button>
<button type="button" class="tu-opt" data-choice="D" data-diagnosis="不能超出量程">D. 可以测量任意高温，没有量程限制</button>
</div><div class="tu-fb" hidden></div></div>
<div class="tu-q" data-answer="A"><h3>选择题 2</h3><p>摄氏温度 0℃ 指的是</p><div class="tu-opts">
<button type="button" class="tu-opt" data-choice="A" data-diagnosis="冰水混合物的温度（在规定条件下）">A. 冰水混合物的温度</button>
<button type="button" class="tu-opt" data-choice="B" data-diagnosis="那是 100℃ 定点相关">B. 沸水的温度</button>
<button type="button" class="tu-opt" data-choice="C" data-diagnosis="人体约 37℃">C. 人体正常体温</button>
<button type="button" class="tu-opt" data-choice="D" data-diagnosis="0℃ 不是绝对零度">D. 宇宙最低温度</button>
</div><div class="tu-fb" hidden></div></div>
<div class="tu-q" data-answer="C"><h3>选择题 3</h3><p>体温计有缩口，主要是为了</p><div class="tu-opts">
<button type="button" class="tu-opt" data-choice="A" data-diagnosis="不是为了好看">A. 装饰</button>
<button type="button" class="tu-opt" data-choice="B" data-diagnosis="缩口不是加热用">B. 加快升温</button>
<button type="button" class="tu-opt" data-choice="C" data-diagnosis="离开人体后液柱不易退回，方便读数">C. 离开人体后液柱不易自动退回，便于读数</button>
<button type="button" class="tu-opt" data-choice="D" data-diagnosis="量程由刻度决定">D. 扩大测量范围到 200℃</button>
</div><div class="tu-fb" hidden></div></div>
<div class="tu-fill"><h3>填空题 1</h3><p>1 标准大气压下，沸水的温度被规定为 ____ ℃。</p>
<details><summary>查看答案与解析</summary><p><strong>答案：</strong>100</p></details></div>
<div class="tu-fill"><h3>填空题 2</h3><p>常用液体温度计的工作原理是液体的 ____。</p>
<details><summary>查看答案与解析</summary><p><strong>答案：</strong>热胀冷缩</p></details></div>
</section>
<section class="section teachany-upgrade-block" data-interactive="conceptest" data-conceptest="true"><h2>💡 概念检测</h2>
<p>“用手摸摸就知道水温”这种做法</p><div class="tu-opts tu-concept">
<button type="button" class="tu-opt" data-choice="A" data-correct="false" data-diagnosis="感觉不可靠">A. 完全可靠</button>
<button type="button" class="tu-opt" data-choice="B" data-correct="true" data-diagnosis="感觉受环境影响，应用温度计测量">B. 不可靠，要用温度计测量</button>
<button type="button" class="tu-opt" data-choice="C" data-correct="false" data-diagnosis="感觉不能代替温标">C. 比温度计更准确</button>
<button type="button" class="tu-opt" data-choice="D" data-correct="false" data-diagnosis="仍不准确">D. 只要两只手一起摸就准</button>
</div><div class="tu-fb" hidden></div></section>
<section class="section teachany-upgrade-block" data-interactive="inquiry"><h2>🔬 探究记录：温度计读数</h2>
<div class="tu-inquiry">
<label>💡 我的假设<textarea data-inq="h" placeholder="例如：俯视读数会偏大还是偏小？"></textarea></label>
<label>📊 我的证据<textarea data-inq="e" placeholder="记录平视/俯视/仰视的读数差异"></textarea></label>
<label>✅ 我的结论<textarea data-inq="c" placeholder="读数必须平视"></textarea></label>
</div>
<button type="button" class="tu-save">保存探究记录（本机）</button>
<div class="tu-fb" data-inq-fb hidden></div></section>
""",
        "fingerprint": "发烧了，温度计",
    },
    "phy-m-heat-calculation": {
        "subtitle": "同样晒太阳，为什么沙比水烫得快？热量到底怎么算？",
        "figcaption": "热量计算：Q=cmΔt，比热容，升降温与生活应用",
        "anchors": [
            ("Q=cmΔt 里每个字母什么意思？", "Q=cmΔt 里每个字母什么意思？"),
            ("比热容大说明什么？", "比热容大说明什么？"),
            ("水和沙谁更容易升温？", "水和沙谁更容易升温？"),
        ],
        "objectives": [
            "能用 Q=cmΔt 计算物体吸收或放出的热量",
            "理解比热容的意义：单位质量升高 1℃ 吸收的热量",
            "能解释水和沙升温快慢不同等生活现象",
        ],
        "story": """<section class="section" id="story" data-tts="story" data-tsh="真实情境"><div class="lesson-panel"><span class="phase-tag">真实情境</span><h2>夏天沙滩烫脚，海水却没那么烫</h2>
<p>同样暴晒，沙烫得快，水升温慢。不是太阳“偏心”，而是不同物质<strong>比热容</strong>不同：升高相同温度，水往往要吸收更多热量。</p>
<div class="mini-grid">
<div class="mini-panel"><h3>已有经验</h3><p>烧开一壶水要很久；铁锅却很快烫手。</p></div>
<div class="mini-panel"><h3>真正卡点</h3><p>把“温度高”和“热量多”混为一谈；算题时忘了 Δt 是变化量，或单位不统一。</p></div>
<div class="mini-panel"><h3>本课任务</h3><p>抓住 Q=cmΔt → 理解 c → 会算、会解释。</p></div>
</div>
<p><strong>一句话：</strong>热量是过程量；比较升温快慢，先看比热容与质量。</p>
</div></section>""",
        "checklist": """<section class="section" id="experiment-checklist" data-tts="experiment-checklist" data-bloom-level="analyze" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">实验检查表</span><h2>热量计算题：先抓什么？</h2>
<p><strong>第一问：谁在吸热/放热？</strong>明确研究对象与质量 m。</p>
<p><strong>第二问：温度怎么变？</strong>写出初温、末温，算出 Δt=|t-t₀|。</p>
<p><strong>第三问：用哪条公式？</strong>Q=cmΔt（未涉及物态变化时）。单位：c 常取 J/(kg·℃)，m 用 kg，Δt 用 ℃。</p>
</div></section>""",
        "pretest": """<section class="section" id="pretest" data-tts="pretest" data-bloom-level="remember" data-scaffold="full" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">前测</span><h2>前测：热量与温度</h2>
<p><strong>下列说法正确的是？</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">A. 温度高的物体一定比温度低的物体含热量更多</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'pretest')">B. 热量是过程量，用 Q=cmΔt 描述升温/降温过程吸收或放出的热量</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">C. 比热容越大，升高相同温度一定吸收热量越少</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">D. Δt 就是末温度，不用相减</button>
<div id="pretest-feedback" class="feedback">关键：热量是过程量；温度是状态量。</div></div></section>""",
        "core": """<section class="section" id="core" data-tts="core" data-bloom-level="understand" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">核心概念</span><h2>Q = c m Δt</h2>
<div class="mini-grid">
<div class="mini-panel"><h3>公式</h3><p>Q=cmΔt。Q 热量，c 比热容，m 质量，Δt 温度变化量。</p></div>
<div class="mini-panel"><h3>比热容 c</h3><p>单位质量的某种物质温度升高 1℃ 吸收的热量。水的比热容较大。</p></div>
<div class="mini-panel"><h3>生活</h3><p>水升温慢、降温也慢，可调节气温；沙漠昼夜温差大，与沙比热容较小有关。</p></div>
</div></div></section>""",
        "deep": """<section class="section" id="deep-understanding" data-tts="deep-understanding"><div class="lesson-panel insight-box"><span class="phase-tag">易混辨析</span><h2>温度高 ≠ 热量多</h2>
<ul>
<li><strong>温度：</strong>状态量，描述冷热程度。</li>
<li><strong>热量：</strong>过程量，描述传热过程中转移的能量。</li>
<li><strong>Δt：</strong>必须是变化量，不是末温本身。</li>
<li><strong>记忆锚点：</strong>先找 m、c、Δt，再代入。</li>
</ul>
</div></section>""",
        "worked": """<section class="section" id="worked-example" data-tts="worked-example" data-bloom-level="analyze" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">例题拆解</span><h2>例题：把水从 20℃ 加热到 100℃</h2>
<p>m=2 kg 的水，c=4.2×10³ J/(kg·℃)，从 20℃ 升到 100℃，吸收多少热量？</p>
<p>Δt=80℃，Q=cmΔt=4.2×10³×2×80=6.72×10⁵ J。</p>
<p class="feedback"><strong>高频错因：</strong>①Δt 写成 100；②c 的数量级写错；③质量和单位不一致。</p>
</div></section>""",
        "transfer": """<section class="section" id="transfer-task" data-tts="transfer-task" data-bloom-level="create" data-scaffold="none"><div class="lesson-panel"><span class="phase-tag">迁移任务</span><h2>解释：海边昼夜温差为什么往往比沙漠小？</h2>
<p>用比热容与 Q=cmΔt 写 3–4 句话：白天吸热、夜晚放热时，水和沙谁温度变化更剧烈。</p>
</div></section>""",
        "lab_html": """<section class="section" id="interactive-lab" data-tts="interactive-lab" data-bloom-level="apply" data-scaffold="partial" data-interactive="heat-lab"><div class="lesson-panel"><span class="phase-tag">互动实验</span><h2>调质量与温升，看吸收热量</h2>
<p style="color:var(--muted)">默认物质为水 c=4.2×10³ J/(kg·℃)。观察 Q 如何随 m、Δt 变化。</p>
<div class="control-row">
<label>质量 m（kg）<input id="q-m" type="range" min="0.5" max="5" step="0.1" value="1"></label>
<label>升温 Δt（℃）<input id="q-dt" type="range" min="1" max="80" step="1" value="20"></label>
</div>
<div class="canvas-wrap"><canvas id="physics-canvas" class="wide-canvas" width="900" height="430"></canvas></div>
<div id="lab-feedback" class="feedback">试着：m 加倍或 Δt 加倍，Q 是否大约加倍。</div></div></section>
<script>
(function(){
  const canvas=document.getElementById('physics-canvas'); if(!canvas) return;
  const ctx=canvas.getContext('2d');
  const mEl=document.getElementById('q-m'), dtEl=document.getElementById('q-dt');
  const fb=document.getElementById('lab-feedback');
  const c=4.2e3;
  function draw(){
    const m=+mEl.value, dt=+dtEl.value, Q=c*m*dt;
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='#081426'; ctx.fillRect(0,0,canvas.width,canvas.height);
    const bar=Math.min(520, Q/2000);
    ctx.fillStyle='#f59e0b'; ctx.fillRect(120,320-bar/5,80,bar/5+20);
    ctx.fillStyle='#fbbf24'; ctx.font='28px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('Q = c m Δt（水）',80,70);
    ctx.fillStyle='#e2e8f0'; ctx.font='24px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('c = 4.2×10³ J/(kg·℃)',80,120);
    ctx.fillText('m = '+m+' kg，Δt = '+dt+' ℃',80,160);
    ctx.fillText('Q ≈ '+Q.toExponential(2)+' J',80,200);
    fb.textContent='吸收热量约 '+Math.round(Q)+' J。想想：若换成比热容更小的沙，同样 m、Δt，Q 会怎样？';
  }
  mEl.addEventListener('input',draw); dtEl.addEventListener('input',draw); draw();
})();
</script>
<script>const FEEDBACK={pretest:"热量是过程量；Q=cmΔt。",posttest:"Δt 是温度变化量；水比热容较大，升温较慢。"};
function checkAnswer(btn,ok,target){btn.parentElement.querySelectorAll('.quiz-option').forEach(b=>b.classList.remove('correct','wrong'));btn.classList.add(ok?'correct':'wrong');const box=document.getElementById(target+'-feedback');if(box)box.textContent=ok?('✅ '+FEEDBACK[target]):('❌ 再想想：'+FEEDBACK[target]);}</script>
""",
        "external": """<section class="section" id="external-sim" data-tts="external-sim"><div class="lesson-panel"><span class="phase-tag">实验回放</span><h2>热量计算三句话</h2>
<ol><li>Q=cmΔt，先确认质量和温度变化。</li><li>比热容大，升温慢、降温也慢。</li><li>温度高不等于热量多。</li></ol>
</div></section>""",
        "posttest": """<section class="section" id="posttest" data-tts="posttest" data-bloom-level="evaluate" data-scaffold="none" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">后测</span><h2>后测：会算也会解释</h2>
<p><strong>质量相同的水和沙吸收相同热量，谁的温度升高更多？（沙的比热容小于水）</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">A. 水升高更多</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'posttest')">B. 沙升高更多</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">C. 一样多</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">D. 无法判断</button>
<div id="posttest-feedback" class="feedback">由 Q=cmΔt，Q、m 相同，c 小则 Δt 大。</div></div></section>""",
        "summary": """<section class="section" id="summary" data-tts="summary"><div class="lesson-panel"><span class="phase-tag">一句话带走</span><h2>热量计算过关标准</h2>
<ul><li>会用 Q=cmΔt 计算。</li><li>能解释比热容意义。</li><li>能区分温度与热量。</li></ul>
</div></section>""",
        "upgrade": """<!-- teachany-upgrade-v2 -->
<!-- upgrade topic: 热量计算（去套路） -->
<section class="section teachany-upgrade-block"><h2>📝 中考风格真题</h2>
<div class="tu-q" data-answer="C"><h3>选择题 1</h3><p>公式 Q=cmΔt 中，Δt 表示</p><div class="tu-opts">
<button type="button" class="tu-opt" data-choice="A" data-diagnosis="不是初温">A. 初温</button>
<button type="button" class="tu-opt" data-choice="B" data-diagnosis="不是末温">B. 末温</button>
<button type="button" class="tu-opt" data-choice="C" data-diagnosis="温度变化量">C. 温度变化量</button>
<button type="button" class="tu-opt" data-choice="D" data-diagnosis="不是比热容">D. 比热容</button>
</div><div class="tu-fb" hidden></div></div>
<div class="tu-q" data-answer="A"><h3>选择题 2</h3><p>水的比热容较大，这意味着</p><div class="tu-opts">
<button type="button" class="tu-opt" data-choice="A" data-diagnosis="同样质量升高相同温度，水吸热更多">A. 同样质量升高相同温度，水吸收热量较多</button>
<button type="button" class="tu-opt" data-choice="B" data-diagnosis="相反">B. 水最容易升温</button>
<button type="button" class="tu-opt" data-choice="C" data-diagnosis="比热容不是密度">C. 水的密度最大</button>
<button type="button" class="tu-opt" data-choice="D" data-diagnosis="比热容不是温度">D. 水的温度总是最高</button>
</div><div class="tu-fb" hidden></div></div>
<div class="tu-fill"><h3>填空题 1</h3><p>2 kg 水从 20℃ 升到 70℃，c=4.2×10³ J/(kg·℃)，吸收热量 ____ J。</p>
<details><summary>查看答案</summary><p><strong>答案：</strong>4.2×10⁵</p><p>Δt=50，Q=4.2e3×2×50=4.2e5 J</p></details></div>
<div class="tu-fill"><h3>填空题 2</h3><p>热量的国际单位是 ____。</p>
<details><summary>查看答案</summary><p><strong>答案：</strong>焦耳（J）</p></details></div>
</section>
<section class="section teachany-upgrade-block" data-interactive="conceptest"><h2>💡 概念检测</h2>
<p>“今天好热，热量真大”这种说法</p><div class="tu-opts tu-concept">
<button type="button" class="tu-opt" data-choice="A" data-correct="false" data-diagnosis="日常口语常把温度和热量混用">A. 物理上完全正确</button>
<button type="button" class="tu-opt" data-choice="B" data-correct="true" data-diagnosis="更准确应说气温高；热量是过程量">B. 不严谨：更准确是温度高</button>
<button type="button" class="tu-opt" data-choice="C" data-correct="false" data-diagnosis="热量有明确物理含义">C. 热量不能谈</button>
<button type="button" class="tu-opt" data-choice="D" data-correct="false" data-diagnosis="仍混淆">D. 热量和温度是一回事</button>
</div><div class="tu-fb" hidden></div></section>
<section class="section teachany-upgrade-block" data-interactive="inquiry"><h2>🔬 探究记录</h2>
<div class="tu-inquiry">
<label>💡 假设<textarea data-inq="h" placeholder="同等加热，水和沙谁升温快？"></textarea></label>
<label>📊 证据<textarea data-inq="e" placeholder="记录质量、时间、温度变化"></textarea></label>
<label>✅ 结论<textarea data-inq="c" placeholder="联系比热容"></textarea></label>
</div>
<button type="button" class="tu-save">保存探究记录（本机）</button>
<div class="tu-fb" data-inq-fb hidden></div></section>
""",
        "fingerprint": "沙滩烫脚",
    },
    "phy-m-friction": {
        "subtitle": "鞋子抓地、轮胎防滑，摩擦力到底帮我们还是拖后腿？",
        "figcaption": "摩擦力：产生条件、静摩擦与滑动摩擦、增大减小方法",
        "anchors": [
            ("摩擦力什么时候出现？", "摩擦力什么时候出现？"),
            ("怎么增大有益摩擦？", "怎么增大有益摩擦？"),
            ("怎么减小有害摩擦？", "怎么减小有害摩擦？"),
        ],
        "objectives": [
            "能说出摩擦力产生的条件与方向判断思路",
            "能区分生活中有益摩擦与有害摩擦",
            "能举出增大/减小摩擦的具体方法",
        ],
        "story": """<section class="section" id="story" data-tts="story" data-tsh="真实情境"><div class="lesson-panel"><span class="phase-tag">真实情境</span><h2>雨天路滑，为什么更容易摔？</h2>
<p>地面有水时更滑，是因为接触面情况变了，<strong>摩擦力变小</strong>。走路、刹车都靠摩擦；机器发热磨损又常恨摩擦。同一类力，有时要它大，有时要它小。</p>
<div class="mini-grid">
<div class="mini-panel"><h3>已有经验</h3><p>鞋底花纹、汽车轮胎沟槽、门轴上油。</p></div>
<div class="mini-panel"><h3>真正卡点</h3><p>以为“越重摩擦力一定越大”却说不清接触面；分不清静摩擦与滑动摩擦。</p></div>
<div class="mini-panel"><h3>本课任务</h3><p>条件 → 方向 → 增大/减小方法 → 生活判断。</p></div>
</div>
</div></section>""",
        "checklist": """<section class="section" id="experiment-checklist" data-tts="experiment-checklist" data-bloom-level="analyze" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">实验检查表</span><h2>摩擦力题三问</h2>
<p><strong>接触？</strong>是否相互接触并挤压。</p>
<p><strong>相对运动/趋势？</strong>有相对运动或相对运动趋势才谈摩擦。</p>
<p><strong>有益还是有害？</strong>再决定增大还是减小。</p>
</div></section>""",
        "pretest": """<section class="section" id="pretest" data-tts="pretest" data-bloom-level="remember" data-scaffold="full" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">前测</span><h2>前测：摩擦一定有害吗？</h2>
<p><strong>下列说法正确的是？</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">A. 摩擦力总是有害的，应该全部消除</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'pretest')">B. 摩擦有时有益（走路、刹车），有时有害（磨损、发热）</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">C. 只有滑动才有摩擦，静止物体间一定没有</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">D. 摩擦力方向总是与运动方向相同</button>
<div id="pretest-feedback" class="feedback">摩擦可有益也可有害；方向与相对运动（趋势）相反。</div></div></section>""",
        "core": """<section class="section" id="core" data-tts="core" data-bloom-level="understand" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">核心概念</span><h2>摩擦力：条件与调控</h2>
<div class="mini-grid">
<div class="mini-panel"><h3>产生条件</h3><p>接触、挤压，并有相对运动或相对运动趋势。</p></div>
<div class="mini-panel"><h3>增大摩擦</h3><p>增大压力；增大接触面粗糙程度（鞋底花纹、轮胎）。</p></div>
<div class="mini-panel"><h3>减小摩擦</h3><p>减小压力；使接触面更光滑；用滚动代替滑动；加润滑油等。</p></div>
</div></div></section>""",
        "deep": """<section class="section" id="deep-understanding" data-tts="deep-understanding"><div class="lesson-panel insight-box"><span class="phase-tag">易混辨析</span><h2>方向怎么想？</h2>
<ul>
<li>摩擦力阻碍的是<strong>相对运动或相对运动趋势</strong>，不是“总跟运动反向”一句背死。</li>
<li>静摩擦：物体相对静止但有滑动趋势时存在。</li>
<li>滑动摩擦：接触面发生相对滑动时存在。</li>
</ul>
</div></section>""",
        "worked": """<section class="section" id="worked-example" data-tts="worked-example" data-bloom-level="analyze" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">例题拆解</span><h2>例题：行李箱轮子的作用</h2>
<p>行李箱装轮子，主要是用<strong>滚动代替滑动</strong>，减小摩擦，更省力。</p>
<p class="feedback">别只答“更方便”——要落到减小摩擦的方法分类。</p>
</div></section>""",
        "transfer": """<section class="section" id="transfer-task" data-tts="transfer-task" data-bloom-level="create" data-scaffold="none"><div class="lesson-panel"><span class="phase-tag">迁移任务</span><h2>给校服鞋底提一条防滑改进</h2>
<p>说明你改的是压力还是粗糙程度，为什么能增大有益摩擦。</p>
</div></section>""",
        "lab_html": """<section class="section" id="interactive-lab" data-tts="interactive-lab" data-bloom-level="apply" data-scaffold="partial" data-interactive="friction-lab"><div class="lesson-panel"><span class="phase-tag">互动实验</span><h2>调压力与粗糙程度，看滑动摩擦力示意</h2>
<p style="color:var(--muted)">示意模型：f ≈ μN（教学示意）。增大压力或粗糙程度，摩擦力示意值变大。</p>
<div class="control-row">
<label>压力 N（N）<input id="f-n" type="range" min="1" max="20" value="8"></label>
<label>粗糙系数 μ<input id="f-mu" type="range" min="1" max="10" value="4"></label>
</div>
<div class="canvas-wrap"><canvas id="physics-canvas" class="wide-canvas" width="900" height="430"></canvas></div>
<div id="lab-feedback" class="feedback">观察箭头长度随 N、μ 变化。</div></div></section>
<script>
(function(){
  const canvas=document.getElementById('physics-canvas'); if(!canvas) return;
  const ctx=canvas.getContext('2d');
  const nEl=document.getElementById('f-n'), muEl=document.getElementById('f-mu');
  const fb=document.getElementById('lab-feedback');
  function draw(){
    const N=+nEl.value, mu=+muEl.value/10, f=mu*N;
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='#081426'; ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='#475569'; ctx.fillRect(200,280,500,40);
    ctx.fillStyle='#38bdf8'; ctx.fillRect(360,200,120,80);
    ctx.strokeStyle='#f97316'; ctx.lineWidth=6;
    ctx.beginPath(); ctx.moveTo(420,240); ctx.lineTo(420-f*18,240); ctx.stroke();
    ctx.fillStyle='#fbbf24'; ctx.font='28px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('滑动摩擦示意 f≈μN',80,70);
    ctx.fillStyle='#e2e8f0'; ctx.font='24px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('N='+N+' N，μ='+mu.toFixed(1)+'，f≈'+f.toFixed(1)+' N',80,120);
    fb.textContent='示意摩擦力约 '+f.toFixed(1)+' N。想想：鞋底花纹增大的是 μ 还是 N？';
  }
  nEl.addEventListener('input',draw); muEl.addEventListener('input',draw); draw();
})();
</script>
<script>const FEEDBACK={pretest:"摩擦可有益可有害；方向与相对运动或趋势相反。",posttest:"增大粗糙程度或压力可增大摩擦；滚动代滑动可减小摩擦。"};
function checkAnswer(btn,ok,target){btn.parentElement.querySelectorAll('.quiz-option').forEach(b=>b.classList.remove('correct','wrong'));btn.classList.add(ok?'correct':'wrong');const box=document.getElementById(target+'-feedback');if(box)box.textContent=ok?('✅ '+FEEDBACK[target]):('❌ 再想想：'+FEEDBACK[target]);}</script>
""",
        "external": """<section class="section" id="external-sim" data-tts="external-sim"><div class="lesson-panel"><span class="phase-tag">实验回放</span><h2>摩擦课三句话</h2>
<ol><li>接触并有相对运动/趋势才产生摩擦。</li><li>有益要增大，有害要减小。</li><li>方法对应：压力、粗糙程度、滚动、润滑。</li></ol>
</div></section>""",
        "posttest": """<section class="section" id="posttest" data-tts="posttest" data-bloom-level="evaluate" data-scaffold="none" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">后测</span><h2>后测：增大还是减小？</h2>
<p><strong>下列属于减小有害摩擦的是？</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">A. 鞋底做防滑纹</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'posttest')">B. 给自行车轴加润滑油</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">C. 轮胎表面做花纹</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">D. 举重运动员手上擦镁粉增大摩擦</button>
<div id="posttest-feedback" class="feedback">润滑油减小有害摩擦。</div></div></section>""",
        "summary": """<section class="section" id="summary" data-tts="summary"><div class="lesson-panel"><span class="phase-tag">一句话带走</span><h2>摩擦课过关标准</h2>
<ul><li>能判断摩擦是否产生。</li><li>能举出增大/减小摩擦的方法。</li><li>能区分有益与有害。</li></ul>
</div></section>""",
        "upgrade": """<!-- teachany-upgrade-v2 -->
<!-- upgrade topic: 摩擦力（去套路） -->
<section class="section teachany-upgrade-block"><h2>📝 中考风格真题</h2>
<div class="tu-q" data-answer="B"><h3>选择题 1</h3><p>下列属于增大有益摩擦的是</p><div class="tu-opts">
<button type="button" class="tu-opt" data-choice="A" data-diagnosis="润滑是减小摩擦">A. 机器轴承加润滑油</button>
<button type="button" class="tu-opt" data-choice="B" data-diagnosis="花纹增大粗糙程度">B. 运动鞋底做花纹</button>
<button type="button" class="tu-opt" data-choice="C" data-diagnosis="气垫是减小摩擦">C. 气垫船靠气垫行驶</button>
<button type="button" class="tu-opt" data-choice="D" data-diagnosis="滚动代滑动是减小">D. 行李箱装轮子</button>
</div><div class="tu-fb" hidden></div></div>
<div class="tu-q" data-answer="A"><h3>选择题 2</h3><p>滑动摩擦力的方向</p><div class="tu-opts">
<button type="button" class="tu-opt" data-choice="A" data-diagnosis="与相对运动方向相反">A. 与物体相对运动方向相反</button>
<button type="button" class="tu-opt" data-choice="B" data-diagnosis="不是总与运动同向">B. 总与运动方向相同</button>
<button type="button" class="tu-opt" data-choice="C" data-diagnosis="不一定竖直">C. 总竖直向下</button>
<button type="button" class="tu-opt" data-choice="D" data-diagnosis="有明确方向">D. 没有方向</button>
</div><div class="tu-fb" hidden></div></div>
<div class="tu-fill"><h3>填空题 1</h3><p>用滚动代替滑动，目的是 ____ 摩擦。</p>
<details><summary>查看答案</summary><p><strong>答案：</strong>减小</p></details></div>
<div class="tu-fill"><h3>填空题 2</h3><p>在接触面材料一定时，滑动摩擦力大小与 ____ 有关。</p>
<details><summary>查看答案</summary><p><strong>答案：</strong>压力大小（及接触面粗糙程度）</p></details></div>
</section>
<section class="section teachany-upgrade-block" data-interactive="conceptest"><h2>💡 概念检测</h2>
<p>“只要两个物体接触就一定有摩擦力”</p><div class="tu-opts tu-concept">
<button type="button" class="tu-opt" data-choice="A" data-correct="false" data-diagnosis="还需要挤压和相对运动/趋势">A. 正确</button>
<button type="button" class="tu-opt" data-choice="B" data-correct="true" data-diagnosis="还要有挤压和相对运动或趋势">B. 错误，还要看挤压与相对运动趋势</button>
<button type="button" class="tu-opt" data-choice="C" data-correct="false" data-diagnosis="不充分">C. 正确，接触就够了</button>
<button type="button" class="tu-opt" data-choice="D" data-correct="false" data-diagnosis="仍缺条件">D. 正确，因为重力存在</button>
</div><div class="tu-fb" hidden></div></section>
<section class="section teachany-upgrade-block" data-interactive="inquiry"><h2>🔬 探究记录</h2>
<div class="tu-inquiry">
<label>💡 假设<textarea data-inq="h" placeholder="压力越大，拉动木块越费力？"></textarea></label>
<label>📊 证据<textarea data-inq="e" placeholder="记录砝码与拉力示数"></textarea></label>
<label>✅ 结论<textarea data-inq="c" placeholder="联系压力与摩擦"></textarea></label>
</div>
<button type="button" class="tu-save">保存探究记录（本机）</button>
<div class="tu-fb" data-inq-fb hidden></div></section>
""",
        "fingerprint": "雨天路滑",
    },
    "phy-m-gravity": {
        "subtitle": "抛出去的球总会掉下来——重力方向到底朝哪？",
        "figcaption": "重力：方向竖直向下、G=mg、重心与生活应用",
        "anchors": [
            ("重力方向是什么？", "重力方向是什么？"),
            ("G=mg 怎么用？", "G=mg 怎么用？"),
            ("重心在哪里？", "重心在哪里？"),
        ],
        "objectives": [
            "知道重力是由于地球吸引产生的力，方向竖直向下",
            "会用 G=mg 计算重力（g 通常取 9.8 N/kg 或 10 N/kg）",
            "能说明重心概念，并联系稳定与倾倒等生活现象",
        ],
        "story": """<section class="section" id="story" data-tts="story" data-tsh="真实情境"><div class="lesson-panel"><span class="phase-tag">真实情境</span><h2>上抛的球为什么总会落回地面？</h2>
<p>不管你把篮球抛多高，它最终都会落下来。这个把物体拉向地面的力叫<strong>重力</strong>。方向不是“指向地心”一句话就能在初中题里乱用——作图时通常画<strong>竖直向下</strong>。</p>
<div class="mini-grid">
<div class="mini-panel"><h3>已有经验</h3><p>苹果落地、河水往低处流、人跳起还会落下。</p></div>
<div class="mini-panel"><h3>真正卡点</h3><p>把重力方向画成斜的；把质量与重力混为一谈；g 的单位写成 m/s² 却当 N/kg 用时不统一。</p></div>
<div class="mini-panel"><h3>本课任务</h3><p>方向 → G=mg → 重心 → 应用。</p></div>
</div>
</div></section>""",
        "checklist": """<section class="section" id="experiment-checklist" data-tts="experiment-checklist" data-bloom-level="analyze" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">实验检查表</span><h2>重力题三问</h2>
<p><strong>对象质量？</strong>先确认 m。</p>
<p><strong>g 取多少？</strong>题目给 9.8 还是 10。</p>
<p><strong>方向怎么画？</strong>作用点可画在重心，方向竖直向下。</p>
</div></section>""",
        "pretest": """<section class="section" id="pretest" data-tts="pretest" data-bloom-level="remember" data-scaffold="full" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">前测</span><h2>前测：重力方向</h2>
<p><strong>关于重力，正确的是？</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">A. 重力方向总指向运动方向</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'pretest')">B. 重力方向竖直向下</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">C. 失重时物体质量变为 0</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">D. 重力与质量无关</button>
<div id="pretest-feedback" class="feedback">重力方向竖直向下；G=mg。</div></div></section>""",
        "core": """<section class="section" id="core" data-tts="core" data-bloom-level="understand" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">核心概念</span><h2>重力 G = mg</h2>
<div class="mini-grid">
<div class="mini-panel"><h3>定义</h3><p>由于地球吸引而使物体受到的力叫重力。</p></div>
<div class="mini-panel"><h3>公式</h3><p>G=mg。g≈9.8 N/kg（常取 10）。质量单位 kg，重力单位 N。</p></div>
<div class="mini-panel"><h3>重心</h3><p>重力作用点叫重心。形状规则、质量分布均匀的物体，重心在几何中心。</p></div>
</div></div></section>""",
        "deep": """<section class="section" id="deep-understanding" data-tts="deep-understanding"><div class="lesson-panel insight-box"><span class="phase-tag">易混辨析</span><h2>质量 ≠ 重力</h2>
<ul>
<li><strong>质量 m：</strong>物质多少，单位 kg，不随位置改变（初中范围）。</li>
<li><strong>重力 G：</strong>力，单位 N，G=mg。</li>
<li><strong>称重：</strong>台秤读数与压力有关，不完全等于“质量本身”。</li>
</ul>
</div></section>""",
        "worked": """<section class="section" id="worked-example" data-tts="worked-example" data-bloom-level="analyze" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">例题拆解</span><h2>例题：m=50 kg 的人重力多大？</h2>
<p>取 g=10 N/kg，G=mg=50×10=500 N。方向竖直向下。</p>
</div></section>""",
        "transfer": """<section class="section" id="transfer-task" data-tts="transfer-task" data-bloom-level="create" data-scaffold="none"><div class="lesson-panel"><span class="phase-tag">迁移任务</span><h2>解释：卡车装货时为什么要把重物放低一点更稳？</h2>
<p>用重心高低与稳定程度写 3 句话。</p>
</div></section>""",
        "lab_html": """<section class="section" id="interactive-lab" data-tts="interactive-lab" data-bloom-level="apply" data-scaffold="partial" data-interactive="gravity-lab"><div class="lesson-panel"><span class="phase-tag">互动实验</span><h2>调质量，看重力大小</h2>
<div class="control-row"><label>质量 m（kg）<input id="g-m" type="range" min="1" max="100" value="50"></label>
<label>g（N/kg）<input id="g-g" type="range" min="9" max="10" step="0.1" value="10"></label></div>
<div class="canvas-wrap"><canvas id="physics-canvas" class="wide-canvas" width="900" height="430"></canvas></div>
<div id="lab-feedback" class="feedback">观察箭头长度随 G 变化。</div></div></section>
<script>
(function(){
  const canvas=document.getElementById('physics-canvas'); if(!canvas) return;
  const ctx=canvas.getContext('2d');
  const mEl=document.getElementById('g-m'), gEl=document.getElementById('g-g');
  const fb=document.getElementById('lab-feedback');
  function draw(){
    const m=+mEl.value, g=+gEl.value, G=m*g;
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='#081426'; ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='#38bdf8'; ctx.beginPath(); ctx.arc(450,160,40,0,Math.PI*2); ctx.fill();
    ctx.strokeStyle='#f97316'; ctx.lineWidth=6;
    const len=Math.min(200, G/4);
    ctx.beginPath(); ctx.moveTo(450,200); ctx.lineTo(450,200+len); ctx.stroke();
    ctx.fillStyle='#fbbf24'; ctx.font='28px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('G = mg',80,70);
    ctx.fillStyle='#e2e8f0'; ctx.font='24px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('m='+m+' kg，g='+g+' N/kg，G='+G.toFixed(0)+' N',80,120);
    ctx.fillText('方向：竖直向下',80,160);
    fb.textContent='重力 '+G.toFixed(0)+' N。质量变，重力跟着变；方向不变。';
  }
  mEl.addEventListener('input',draw); gEl.addEventListener('input',draw); draw();
})();
</script>
<script>const FEEDBACK={pretest:"重力方向竖直向下；G=mg。",posttest:"质量单位 kg，重力单位 N。"};
function checkAnswer(btn,ok,target){btn.parentElement.querySelectorAll('.quiz-option').forEach(b=>b.classList.remove('correct','wrong'));btn.classList.add(ok?'correct':'wrong');const box=document.getElementById(target+'-feedback');if(box)box.textContent=ok?('✅ '+FEEDBACK[target]):('❌ 再想想：'+FEEDBACK[target]);}</script>
""",
        "external": """<section class="section" id="external-sim" data-tts="external-sim"><div class="lesson-panel"><span class="phase-tag">实验回放</span><h2>重力课三句话</h2>
<ol><li>重力因地球吸引产生，方向竖直向下。</li><li>G=mg。</li><li>质量不是重力。</li></ol>
</div></section>""",
        "posttest": """<section class="section" id="posttest" data-tts="posttest" data-bloom-level="evaluate" data-scaffold="none" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">后测</span><h2>后测</h2>
<p><strong>物体质量 2 kg，g=10 N/kg，重力是</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">A. 2 N</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'posttest')">B. 20 N</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">C. 2 kg</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">D. 20 kg</button>
<div id="posttest-feedback" class="feedback">G=mg=20 N。</div></div></section>""",
        "summary": """<section class="section" id="summary" data-tts="summary"><div class="lesson-panel"><span class="phase-tag">一句话带走</span><h2>重力课过关</h2>
<ul><li>方向竖直向下。</li><li>会算 G=mg。</li><li>区分质量与重力。</li></ul>
</div></section>""",
        "upgrade": """<!-- teachany-upgrade-v2 -->
<!-- upgrade topic: 重力（去套路） -->
<section class="section teachany-upgrade-block"><h2>📝 中考风格真题</h2>
<div class="tu-q" data-answer="B"><h3>选择题 1</h3><p>关于重力，正确的是</p><div class="tu-opts">
<button type="button" class="tu-opt" data-choice="A" data-diagnosis="方向是竖直向下">A. 重力方向总水平</button>
<button type="button" class="tu-opt" data-choice="B" data-diagnosis="竖直向下">B. 重力方向竖直向下</button>
<button type="button" class="tu-opt" data-choice="C" data-diagnosis="质量不变（初中）">C. 到月球质量变为 0</button>
<button type="button" class="tu-opt" data-choice="D" data-diagnosis="有重力公式">D. 重力与质量无关</button>
</div><div class="tu-fb" hidden></div></div>
<div class="tu-fill"><h3>填空题 1</h3><p>g 常取 9.8，单位是 ____。</p>
<details><summary>查看答案</summary><p><strong>答案：</strong>N/kg</p></details></div>
<div class="tu-fill"><h3>填空题 2</h3><p>质量 5 kg 的物体，g=10 N/kg，重力为 ____ N。</p>
<details><summary>查看答案</summary><p><strong>答案：</strong>50</p></details></div>
</section>
<section class="section teachany-upgrade-block" data-interactive="conceptest"><h2>💡 概念检测</h2>
<p>“质量就是重力”</p><div class="tu-opts tu-concept">
<button type="button" class="tu-opt" data-choice="A" data-correct="false" data-diagnosis="单位和含义都不同">A. 正确</button>
<button type="button" class="tu-opt" data-choice="B" data-correct="true" data-diagnosis="质量 kg，重力 N，G=mg">B. 错误，二者不同</button>
<button type="button" class="tu-opt" data-choice="C" data-correct="false" data-diagnosis="仍错">C. 在地球上正确</button>
<button type="button" class="tu-opt" data-choice="D" data-correct="false" data-diagnosis="仍错">D. 数值总相等所以是一回事</button>
</div><div class="tu-fb" hidden></div></section>
<section class="section teachany-upgrade-block" data-interactive="inquiry"><h2>🔬 探究记录</h2>
<div class="tu-inquiry">
<label>💡 假设<textarea data-inq="h" placeholder="质量越大，弹簧测力计示数？"></textarea></label>
<label>📊 证据<textarea data-inq="e" placeholder="记录 m 与示数"></textarea></label>
<label>✅ 结论<textarea data-inq="c" placeholder="G 与 m 成正比"></textarea></label>
</div>
<button type="button" class="tu-save">保存探究记录（本机）</button>
<div class="tu-fb" data-inq-fb hidden></div></section>
""",
        "fingerprint": "上抛的球为什么总会落回",
    },
    "phy-m-force-basics": {
        "subtitle": "推箱子、提书包——怎样判断有没有力？力的作用效果看什么？",
        "figcaption": "力：三要素、作用效果、示意图与相互作用",
        "anchors": [
            ("力的三要素是什么？", "力的三要素是什么？"),
            ("力可以改变什么？", "力可以改变什么？"),
            ("怎样画力的示意图？", "怎样画力的示意图？"),
        ],
        "objectives": [
            "知道力是物体对物体的作用，能说出施力物体与受力物体",
            "掌握力的三要素：大小、方向、作用点",
            "能说明力可改变物体的运动状态或形状，并会画简单力的示意图",
        ],
        "story": """<section class="section" id="story" data-tts="story" data-tsh="真实情境"><div class="lesson-panel"><span class="phase-tag">真实情境</span><h2>同样推箱子，为什么有人推得动、有人推不动？</h2>
<p>推箱子时，力的<strong>大小、方向、作用点</strong>都会影响结果。力不是“感觉一下”就够了，要用三要素把它说清楚，还要会画示意图。</p>
<div class="mini-grid">
<div class="mini-panel"><h3>已有经验</h3><p>踢球改变球的运动；捏橡皮泥改变形状；弹簧被拉长。</p></div>
<div class="mini-panel"><h3>真正卡点</h3><p>忘记力不能离开物体；画力时箭头方向乱标；把“速度”和“运动状态”混为一谈。</p></div>
<div class="mini-panel"><h3>本课任务</h3><p>力的含义 → 三要素 → 作用效果 → 示意图。</p></div>
</div>
</div></section>""",
        "checklist": """<section class="section" id="experiment-checklist" data-tts="experiment-checklist" data-bloom-level="analyze" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">实验检查表</span><h2>受力分析三问</h2>
<p><strong>谁对谁？</strong>找出施力物体与受力物体。</p>
<p><strong>三要素？</strong>大小、方向、作用点是否齐全。</p>
<p><strong>效果？</strong>改变运动状态，还是改变形状？</p>
</div></section>""",
        "pretest": """<section class="section" id="pretest" data-tts="pretest" data-bloom-level="remember" data-scaffold="full" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">前测</span><h2>前测：力离开物体存在吗？</h2>
<p><strong>正确的是？</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">A. 力可以离开物体单独存在</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'pretest')">B. 力是物体对物体的作用，不能离开物体</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">C. 只有接触才有力，磁场力不存在</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">D. 力只有大小，没有方向</button>
<div id="pretest-feedback" class="feedback">力不能离开物体；有大小、方向、作用点。</div></div></section>""",
        "core": """<section class="section" id="core" data-tts="core" data-bloom-level="understand" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">核心概念</span><h2>力的三要素与作用效果</h2>
<div class="mini-grid">
<div class="mini-panel"><h3>含义</h3><p>力是物体对物体的作用。单位：牛顿（N）。</p></div>
<div class="mini-panel"><h3>三要素</h3><p>大小、方向、作用点。缺一不可。</p></div>
<div class="mini-panel"><h3>效果</h3><p>①改变运动状态（速度大小/方向）；②改变形状。</p></div>
</div></div></section>""",
        "deep": """<section class="section" id="deep-understanding" data-tts="deep-understanding"><div class="lesson-panel insight-box"><span class="phase-tag">易混辨析</span><h2>运动状态改变 ≠ 一定受力？</h2>
<ul>
<li>初中：力是改变运动状态的原因；物体受力情况要结合具体分析。</li>
<li>物体间力的作用是相互的：你推墙，墙也推你。</li>
<li>示意图：从作用点沿力的方向画带箭头的线段，箭头表示方向。</li>
</ul>
</div></section>""",
        "worked": """<section class="section" id="worked-example" data-tts="worked-example" data-bloom-level="analyze" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">例题拆解</span><h2>例题：画出人对箱子的推力</h2>
<p>作用点画在箱子受力处，箭头指向推力方向，可在箭头旁标 F。注意：箭头方向就是力的方向。</p>
</div></section>""",
        "transfer": """<section class="section" id="transfer-task" data-tts="transfer-task" data-bloom-level="create" data-scaffold="none"><div class="lesson-panel"><span class="phase-tag">迁移任务</span><h2>举两个例子</h2>
<p>一个说明力改变运动状态，一个说明力改变形状，并指出施力/受力物体。</p>
</div></section>""",
        "lab_html": """<section class="section" id="interactive-lab" data-tts="interactive-lab" data-bloom-level="apply" data-scaffold="partial" data-interactive="force-lab"><div class="lesson-panel"><span class="phase-tag">互动实验</span><h2>调力的大小与方向，看示意图</h2>
<div class="control-row">
<label>力的大小 F<input id="force-f" type="range" min="1" max="20" value="8"></label>
<label>方向角（°）<input id="force-ang" type="range" min="0" max="360" value="0"></label>
</div>
<div class="canvas-wrap"><canvas id="physics-canvas" class="wide-canvas" width="900" height="430"></canvas></div>
<div id="lab-feedback" class="feedback">箭头长度表示大小，箭头指向表示方向。</div></div></section>
<script>
(function(){
  const canvas=document.getElementById('physics-canvas'); if(!canvas) return;
  const ctx=canvas.getContext('2d');
  const fEl=document.getElementById('force-f'), aEl=document.getElementById('force-ang');
  const fb=document.getElementById('lab-feedback');
  function draw(){
    const F=+fEl.value, ang=+aEl.value*Math.PI/180;
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='#081426'; ctx.fillRect(0,0,canvas.width,canvas.height);
    const x0=450,y0=220, L=F*12;
    const x1=x0+L*Math.cos(ang), y1=y0-L*Math.sin(ang);
    ctx.fillStyle='#38bdf8'; ctx.fillRect(x0-40,y0-30,80,60);
    ctx.strokeStyle='#f97316'; ctx.lineWidth=5;
    ctx.beginPath(); ctx.moveTo(x0,y0); ctx.lineTo(x1,y1); ctx.stroke();
    ctx.fillStyle='#fbbf24'; ctx.font='28px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('力的示意图：三要素',80,70);
    ctx.fillStyle='#e2e8f0'; ctx.font='24px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('大小 F='+F+'（示意） 方向='+aEl.value+'°',80,120);
    fb.textContent='作用点在方块中心；改变滑块，看箭头长短与指向如何变。';
  }
  fEl.addEventListener('input',draw); aEl.addEventListener('input',draw); draw();
})();
</script>
<script>const FEEDBACK={pretest:"力是物体对物体的作用，有三要素。",posttest:"力可改变运动状态或形状。"};
function checkAnswer(btn,ok,target){btn.parentElement.querySelectorAll('.quiz-option').forEach(b=>b.classList.remove('correct','wrong'));btn.classList.add(ok?'correct':'wrong');const box=document.getElementById(target+'-feedback');if(box)box.textContent=ok?('✅ '+FEEDBACK[target]):('❌ 再想想：'+FEEDBACK[target]);}</script>
""",
        "external": """<section class="section" id="external-sim" data-tts="external-sim"><div class="lesson-panel"><span class="phase-tag">实验回放</span><h2>力的初步三句话</h2>
<ol><li>力不能离开物体。</li><li>三要素：大小、方向、作用点。</li><li>效果：改运动状态或改形状。</li></ol>
</div></section>""",
        "posttest": """<section class="section" id="posttest" data-tts="posttest" data-bloom-level="evaluate" data-scaffold="none" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">后测</span><h2>后测</h2>
<p><strong>下列属于力改变物体形状的是？</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">A. 守门员扑出足球</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'posttest')">B. 用力捏橡皮泥变扁</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">C. 踢出的足球在空中飞行（忽略形变讨论）</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">D. 汽车匀速直线行驶（理想）</button>
<div id="posttest-feedback" class="feedback">捏橡皮泥是典型的改变形状。</div></div></section>""",
        "summary": """<section class="section" id="summary" data-tts="summary"><div class="lesson-panel"><span class="phase-tag">一句话带走</span><h2>力的初步过关</h2>
<ul><li>会说施力/受力物体。</li><li>会背三要素。</li><li>会举两类作用效果并画示意图。</li></ul>
</div></section>""",
        "upgrade": """<!-- teachany-upgrade-v2 -->
<!-- upgrade topic: 力的初步（去套路） -->
<section class="section teachany-upgrade-block"><h2>📝 中考风格真题</h2>
<div class="tu-q" data-answer="C"><h3>选择题 1</h3><p>力的三要素是</p><div class="tu-opts">
<button type="button" class="tu-opt" data-choice="A" data-diagnosis="缺作用点">A. 大小、方向</button>
<button type="button" class="tu-opt" data-choice="B" data-diagnosis="缺方向">B. 大小、作用点</button>
<button type="button" class="tu-opt" data-choice="C" data-diagnosis="大小、方向、作用点">C. 大小、方向、作用点</button>
<button type="button" class="tu-opt" data-choice="D" data-diagnosis="不是速度">D. 速度、质量、时间</button>
</div><div class="tu-fb" hidden></div></div>
<div class="tu-q" data-answer="A"><h3>选择题 2</h3><p>下列说法正确的是</p><div class="tu-opts">
<button type="button" class="tu-opt" data-choice="A" data-diagnosis="力是物体对物体的作用">A. 力不能离开物体而存在</button>
<button type="button" class="tu-opt" data-choice="B" data-diagnosis="可以不接触，如磁力">B. 只有接触才有力</button>
<button type="button" class="tu-opt" data-choice="C" data-diagnosis="力有方向">C. 力没有方向</button>
<button type="button" class="tu-opt" data-choice="D" data-diagnosis="相互作用">D. 一个物体也可以产生力</button>
</div><div class="tu-fb" hidden></div></div>
<div class="tu-fill"><h3>填空题 1</h3><p>力的作用效果可以改变物体的 ____ 或 ____。</p>
<details><summary>查看答案</summary><p><strong>答案：</strong>运动状态；形状</p></details></div>
</section>
<section class="section teachany-upgrade-block" data-interactive="conceptest"><h2>💡 概念检测</h2>
<p>“力可以离开物体单独存在”</p><div class="tu-opts tu-concept">
<button type="button" class="tu-opt" data-choice="A" data-correct="false" data-diagnosis="错误">A. 正确</button>
<button type="button" class="tu-opt" data-choice="B" data-correct="true" data-diagnosis="力是物体对物体的作用">B. 错误</button>
<button type="button" class="tu-opt" data-choice="C" data-correct="false" data-diagnosis="仍错">C. 只在真空中正确</button>
<button type="button" class="tu-opt" data-choice="D" data-correct="false" data-diagnosis="仍错">D. 只对重力正确</button>
</div><div class="tu-fb" hidden></div></section>
<section class="section teachany-upgrade-block" data-interactive="inquiry"><h2>🔬 探究记录</h2>
<div class="tu-inquiry">
<label>💡 假设<textarea data-inq="h" placeholder="作用点不同，推门效果是否不同？"></textarea></label>
<label>📊 证据<textarea data-inq="e" placeholder="记录推门把手与推门轴附近的难易"></textarea></label>
<label>✅ 结论<textarea data-inq="c" placeholder="作用点影响效果"></textarea></label>
</div>
<button type="button" class="tu-save">保存探究记录（本机）</button>
<div class="tu-fb" data-inq-fb hidden></div></section>
""",
        "fingerprint": "同样推箱子，为什么有人推得动",
    },
    "phy-m-circuit-basics": {
        "subtitle": "灯泡为什么有时亮、有时不亮？电路怎样才算通路？",
        "figcaption": "电路：通路/断路/短路、电路元件、电路图",
        "anchors": [
            ("什么是通路？", "什么是通路？"),
            ("短路为什么危险？", "短路为什么危险？"),
            ("怎样画简单电路图？", "怎样画简单电路图？"),
        ],
        "objectives": [
            "能区分通路、断路与短路",
            "认识电源、开关、用电器、导线的作用",
            "能识别并画出简单电路图",
        ],
        "story": """<section class="section" id="story" data-tts="story" data-tsh="真实情境"><div class="lesson-panel"><span class="phase-tag">真实情境</span><h2>开关一扳，灯为什么会亮？</h2>
<p>灯亮说明电流形成了完整路径：从电源出发，经过导线、开关、灯泡再回到电源。这条路径叫<strong>通路</strong>。若某处断开就是断路；若电流不经用电器直接被导线“抄近路”，可能是<strong>短路</strong>——很危险。</p>
<div class="mini-grid">
<div class="mini-panel"><h3>已有经验</h3><p>手电筒、台灯、教室灯的开关控制。</p></div>
<div class="mini-panel"><h3>真正卡点</h3><p>把断路和短路混为一谈；电路图符号记不清；以为有电源就一定有电流。</p></div>
<div class="mini-panel"><h3>本课任务</h3><p>元件作用 → 三种状态 → 电路图。</p></div>
</div>
</div></section>""",
        "checklist": """<section class="section" id="experiment-checklist" data-tts="experiment-checklist" data-bloom-level="analyze" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">实验检查表</span><h2>看电路三问</h2>
<p><strong>有电源吗？</strong>没有电源通常没有持续电流。</p>
<p><strong>路径通吗？</strong>开关是否闭合，导线是否接好。</p>
<p><strong>有没有短路？</strong>电流是否绕开用电器直接连通电源两极。</p>
</div></section>""",
        "pretest": """<section class="section" id="pretest" data-tts="pretest" data-bloom-level="remember" data-scaffold="full" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">前测</span><h2>前测：断路还是短路？</h2>
<p><strong>灯泡不亮，开关已闭合，更可能是？</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">A. 一定是短路</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'pretest')">B. 可能是断路（接触不良、灯丝断等）</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">C. 一定没有电源</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">D. 短路时用电器一定更亮</button>
<div id="pretest-feedback" class="feedback">断路：电流无法形成通路；短路危险且用电器往往不工作。</div></div></section>""",
        "core": """<section class="section" id="core" data-tts="core" data-bloom-level="understand" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">核心概念</span><h2>电路的组成与状态</h2>
<div class="mini-grid">
<div class="mini-panel"><h3>基本组成</h3><p>电源、用电器、开关、导线。</p></div>
<div class="mini-panel"><h3>三种状态</h3><p>通路：用电器工作；断路：某处断开；短路：电流抄近路，危险。</p></div>
<div class="mini-panel"><h3>电路图</h3><p>用统一符号表示元件，便于设计与交流。</p></div>
</div></div></section>""",
        "deep": """<section class="section" id="deep-understanding" data-tts="deep-understanding"><div class="lesson-panel insight-box"><span class="phase-tag">易混辨析</span><h2>断路 ≠ 短路</h2>
<ul>
<li><strong>断路：</strong>电路某处断开，一般没有电流，用电器不工作。</li>
<li><strong>短路：</strong>电源两极被导线直接连通（或用电器被短路），电流很大，易损坏电源/引发危险。</li>
<li><strong>安全：</strong>连接电路时开关应断开；禁止把导线直接接在电源两极上玩。</li>
</ul>
</div></section>""",
        "worked": """<section class="section" id="worked-example" data-tts="worked-example" data-bloom-level="analyze" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">例题拆解</span><h2>例题：开关应接在哪里？</h2>
<p>开关要能控制电路通断，通常与用电器串联在电路中。画图时注意符号规范，导线连接在符号端点上。</p>
</div></section>""",
        "transfer": """<section class="section" id="transfer-task" data-tts="transfer-task" data-bloom-level="create" data-scaffold="none"><div class="lesson-panel"><span class="phase-tag">迁移任务</span><h2>画一个控制一盏灯的电路图</h2>
<p>包含电源、开关、灯泡、导线；并说明怎样操作使灯亮/灭。</p>
</div></section>""",
        "lab_html": """<section class="section" id="interactive-lab" data-tts="interactive-lab" data-bloom-level="apply" data-scaffold="partial" data-interactive="circuit-lab"><div class="lesson-panel"><span class="phase-tag">互动实验</span><h2>拨开关，看灯亮与电路状态</h2>
<div class="control-row">
<label>开关<input id="ckt-sw" type="range" min="0" max="1" step="1" value="0"></label>
<label>人为短路演示（危险示意）<input id="ckt-short" type="range" min="0" max="1" step="1" value="0"></label>
</div>
<div class="canvas-wrap"><canvas id="physics-canvas" class="wide-canvas" width="900" height="430"></canvas></div>
<div id="lab-feedback" class="feedback">0=断开/正常，1=闭合/短路示意。</div></div></section>
<script>
(function(){
  const canvas=document.getElementById('physics-canvas'); if(!canvas) return;
  const ctx=canvas.getContext('2d');
  const sw=document.getElementById('ckt-sw'), sh=document.getElementById('ckt-short');
  const fb=document.getElementById('lab-feedback');
  function draw(){
    const on=+sw.value===1, short=+sh.value===1;
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='#081426'; ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.strokeStyle='#94a3b8'; ctx.lineWidth=4;
    ctx.strokeRect(200,140,500,160);
    ctx.fillStyle= short ? '#f97316' : (on ? '#fbbf24' : '#334155');
    ctx.beginPath(); ctx.arc(450,220,36,0,Math.PI*2); ctx.fill();
    let state='断路：灯不亮';
    if(short) state='短路示意：电流抄近路，危险！灯通常不正常工作';
    else if(on) state='通路：灯亮';
    ctx.fillStyle='#fbbf24'; ctx.font='28px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('简单电路状态示意',80,70);
    ctx.fillStyle='#e2e8f0'; ctx.font='24px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText(state,80,120);
    fb.textContent=state+'。请用自己的话区分断路与短路。';
  }
  sw.addEventListener('input',draw); sh.addEventListener('input',draw); draw();
})();
</script>
<script>const FEEDBACK={pretest:"灯不亮常见是断路；短路很危险。",posttest:"通路灯亮；断路断开；短路抄近路危险。"};
function checkAnswer(btn,ok,target){btn.parentElement.querySelectorAll('.quiz-option').forEach(b=>b.classList.remove('correct','wrong'));btn.classList.add(ok?'correct':'wrong');const box=document.getElementById(target+'-feedback')||document.getElementById('pretest-feedback');if(box)box.textContent=ok?('✅ '+FEEDBACK[target]):('❌ 再想想：'+FEEDBACK[target]);}</script>
""",
        "external": """<section class="section" id="external-sim" data-tts="external-sim"><div class="lesson-panel"><span class="phase-tag">实验回放</span><h2>电路基础三句话</h2>
<ol><li>基本组成：电源、用电器、开关、导线。</li><li>通路/断路/短路要分清。</li><li>会画简单电路图。</li></ol>
</div></section>""",
        "posttest": """<section class="section" id="posttest" data-tts="posttest" data-bloom-level="evaluate" data-scaffold="none" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">后测</span><h2>后测</h2>
<p><strong>把导线直接接在电源两极上，属于</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">A. 通路的正确接法</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'posttest')">B. 短路，十分危险</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">C. 断路</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">D. 开路且安全</button>
<div id="posttest-feedback" class="feedback">电源两极被导线直接连通是短路。</div></div></section>""",
        "summary": """<section class="section" id="summary" data-tts="summary"><div class="lesson-panel"><span class="phase-tag">一句话带走</span><h2>电路基础过关</h2>
<ul><li>能说出电路基本组成。</li><li>能区分通路、断路、短路。</li><li>能画控制一盏灯的电路图。</li></ul>
</div></section>""",
        "upgrade": """<!-- teachany-upgrade-v2 -->
<!-- upgrade topic: 电路基础（去套路） -->
<section class="section teachany-upgrade-block"><h2>📝 中考风格真题</h2>
<div class="tu-q" data-answer="B"><h3>选择题 1</h3><p>关于短路，正确的是</p><div class="tu-opts">
<button type="button" class="tu-opt" data-choice="A" data-diagnosis="短路危险">A. 短路时用电器一定更亮且安全</button>
<button type="button" class="tu-opt" data-choice="B" data-diagnosis="电流不经用电器直接连通电源两极">B. 电流抄近路，可能损坏电源，很危险</button>
<button type="button" class="tu-opt" data-choice="C" data-diagnosis="那是断路">C. 就是开关断开</button>
<button type="button" class="tu-opt" data-choice="D" data-diagnosis="短路有电流且很大">D. 短路时一定没有电流</button>
</div><div class="tu-fb" hidden></div></div>
<div class="tu-fill"><h3>填空题 1</h3><p>电路的三种状态：通路、____、短路。</p>
<details><summary>查看答案</summary><p><strong>答案：</strong>断路</p></details></div>
<div class="tu-fill"><h3>填空题 2</h3><p>提供电能的装置叫 ____。</p>
<details><summary>查看答案</summary><p><strong>答案：</strong>电源</p></details></div>
</section>
<section class="section teachany-upgrade-block" data-interactive="conceptest"><h2>💡 概念检测</h2>
<p>“有电源，电路就一定有电流”</p><div class="tu-opts tu-concept">
<button type="button" class="tu-opt" data-choice="A" data-correct="false" data-diagnosis="还需要形成通路">A. 正确</button>
<button type="button" class="tu-opt" data-choice="B" data-correct="true" data-diagnosis="还必须是通路，不能断路">B. 错误，还要形成通路</button>
<button type="button" class="tu-opt" data-choice="C" data-correct="false" data-diagnosis="仍错">C. 正确，开关无关</button>
<button type="button" class="tu-opt" data-choice="D" data-correct="false" data-diagnosis="仍错">D. 正确，灯泡无关</button>
</div><div class="tu-fb" hidden></div></section>
<section class="section teachany-upgrade-block" data-interactive="inquiry"><h2>🔬 探究记录</h2>
<div class="tu-inquiry">
<label>💡 假设<textarea data-inq="h" placeholder="开关断开时灯为何不亮？"></textarea></label>
<label>📊 证据<textarea data-inq="e" placeholder="记录开关状态与灯的亮灭"></textarea></label>
<label>✅ 结论<textarea data-inq="c" placeholder="断路无持续工作电流"></textarea></label>
</div>
<button type="button" class="tu-save">保存探究记录（本机）</button>
<div class="tu-fb" data-inq-fb hidden></div></section>
""",
        "fingerprint": "开关一扳，灯为什么会亮",
    },
    "phy-m-current-circuit": {
        "subtitle": "电流从哪流向哪？怎样用电流表安全测量？",
        "figcaption": "电流：方向规定、串联并联电流特点、电流表使用",
        "anchors": [
            ("电流方向怎么规定？", "电流方向怎么规定？"),
            ("串联电路电流有何特点？", "串联电路电流有何特点？"),
            ("电流表怎样接入电路？", "电流表怎样接入电路？"),
        ],
        "objectives": [
            "知道电流的形成与方向的规定",
            "掌握串联电路各处电流相等、并联干路等于支路之和",
            "会正确使用电流表（串联、正负接线柱、量程）",
        ],
        "story": """<section class="section" id="story" data-tts="story" data-tsh="真实情境"><div class="lesson-panel"><span class="phase-tag">真实情境</span><h2>为什么保险丝会“跳”？</h2>
<p>电流过大时，电路保护装置可能断开。要理解这一点，先要会描述<strong>电流强弱</strong>，并用电流表测量。测错接法（并联进电流表、超量程）会损坏仪表。</p>
<div class="mini-grid">
<div class="mini-panel"><h3>已有经验</h3><p>电池标的电流、家用电器功率大时电线更粗。</p></div>
<div class="mini-panel"><h3>真正卡点</h3><p>电流方向与自由电子定向移动方向搞混；电流表当成电压表用。</p></div>
<div class="mini-panel"><h3>本课任务</h3><p>电流概念 → 串并联规律 → 电流表规范使用。</p></div>
</div>
</div></section>""",
        "checklist": """<section class="section" id="experiment-checklist" data-tts="experiment-checklist" data-bloom-level="analyze" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">实验检查表</span><h2>用电流表三问</h2>
<p><strong>串联了吗？</strong>电流表必须串联在被测电路中。</p>
<p><strong>正负对吗？</strong>电流从正接线柱流入、负接线柱流出。</p>
<p><strong>量程够吗？</strong>先估算或大量程试触，避免超量程。</p>
</div></section>""",
        "pretest": """<section class="section" id="pretest" data-tts="pretest" data-bloom-level="remember" data-scaffold="full" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">前测</span><h2>前测：电流表怎么接？</h2>
<p><strong>测量电路中的电流，电流表应</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">A. 与用电器并联</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'pretest')">B. 与用电器串联</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">C. 直接接在电源两极上</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">D. 可以随便接，无正负要求</button>
<div id="pretest-feedback" class="feedback">电流表串联；注意正负与量程。</div></div></section>""",
        "core": """<section class="section" id="core" data-tts="core" data-bloom-level="understand" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">核心概念</span><h2>电流与测量</h2>
<div class="mini-grid">
<div class="mini-panel"><h3>电流</h3><p>电荷的定向移动形成电流。规定：正电荷定向移动方向为电流方向。</p></div>
<div class="mini-panel"><h3>串并联</h3><p>串联：电流处处相等。并联：干路电流等于各支路电流之和。</p></div>
<div class="mini-panel"><h3>电流表</h3><p>测电流，串联接入；正进负出；不能直接接电源两极。</p></div>
</div></div></section>""",
        "deep": """<section class="section" id="deep-understanding" data-tts="deep-understanding"><div class="lesson-panel insight-box"><span class="phase-tag">易混辨析</span><h2>电流方向规定</h2>
<ul>
<li>金属导体中实际是自由电子定向移动，方向与规定电流方向相反。</li>
<li>初中解题以“规定方向”为准。</li>
<li>电流单位：安培（A）。</li>
</ul>
</div></section>""",
        "worked": """<section class="section" id="worked-example" data-tts="worked-example" data-bloom-level="analyze" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">例题拆解</span><h2>例题：串联两灯，电流表示数</h2>
<p>串联电路电流处处相等。若电流表测干路（也是各处）电流为 0.2 A，则通过每盏灯的电流都是 0.2 A。</p>
</div></section>""",
        "transfer": """<section class="section" id="transfer-task" data-tts="transfer-task" data-bloom-level="create" data-scaffold="none"><div class="lesson-panel"><span class="phase-tag">迁移任务</span><h2>设计测量小灯泡电流的步骤</h2>
<p>写出：选量程、串联位置、正负接线、闭合开关前的检查。</p>
</div></section>""",
        "lab_html": """<section class="section" id="interactive-lab" data-tts="interactive-lab" data-bloom-level="apply" data-scaffold="partial" data-interactive="current-lab"><div class="lesson-panel"><span class="phase-tag">互动实验</span><h2>调支路电流，看并联干路电流</h2>
<p style="color:var(--muted)">并联示意：I = I₁ + I₂</p>
<div class="control-row">
<label>I₁（A）<input id="i1" type="range" min="0" max="20" value="5"></label>
<label>I₂（A）<input id="i2" type="range" min="0" max="20" value="3"></label>
</div>
<div class="canvas-wrap"><canvas id="physics-canvas" class="wide-canvas" width="900" height="430"></canvas></div>
<div id="lab-feedback" class="feedback">观察干路电流随支路变化。</div></div></section>
<script>
(function(){
  const canvas=document.getElementById('physics-canvas'); if(!canvas) return;
  const ctx=canvas.getContext('2d');
  const a=document.getElementById('i1'), b=document.getElementById('i2');
  const fb=document.getElementById('lab-feedback');
  function draw(){
    const i1=+a.value/10, i2=+b.value/10, I=i1+i2;
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='#081426'; ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='#fbbf24'; ctx.font='28px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('并联：I = I₁ + I₂',80,70);
    ctx.fillStyle='#e2e8f0'; ctx.font='24px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('I₁='+i1.toFixed(1)+' A，I₂='+i2.toFixed(1)+' A',80,130);
    ctx.fillText('干路 I='+I.toFixed(1)+' A',80,180);
    ctx.fillStyle='#38bdf8'; ctx.fillRect(200,260,I*80,40);
    fb.textContent='干路电流 '+I.toFixed(1)+' A。串联时各处相等，对比记忆。';
  }
  a.addEventListener('input',draw); b.addEventListener('input',draw); draw();
})();
</script>
<script>const FEEDBACK={pretest:"电流表要串联，注意正负与量程。",posttest:"并联干路等于支路之和；串联处处相等。"};
function checkAnswer(btn,ok,target){btn.parentElement.querySelectorAll('.quiz-option').forEach(b=>b.classList.remove('correct','wrong'));btn.classList.add(ok?'correct':'wrong');const box=document.getElementById(target+'-feedback');if(box)box.textContent=ok?('✅ '+FEEDBACK[target]):('❌ 再想想：'+FEEDBACK[target]);}</script>
""",
        "external": """<section class="section" id="external-sim" data-tts="external-sim"><div class="lesson-panel"><span class="phase-tag">实验回放</span><h2>电流课三句话</h2>
<ol><li>电流有方向规定与强弱。</li><li>串联处处相等；并联干路等于支路和。</li><li>电流表串联、正进负出、不直接接电源两极。</li></ol>
</div></section>""",
        "posttest": """<section class="section" id="posttest" data-tts="posttest" data-bloom-level="evaluate" data-scaffold="none" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">后测</span><h2>后测</h2>
<p><strong>两灯并联，支路电流 0.2 A 与 0.3 A，干路电流约为</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">A. 0.2 A</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">B. 0.3 A</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'posttest')">C. 0.5 A</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">D. 0.1 A</button>
<div id="posttest-feedback" class="feedback">并联：I=I₁+I₂=0.5 A。</div></div></section>""",
        "summary": """<section class="section" id="summary" data-tts="summary"><div class="lesson-panel"><span class="phase-tag">一句话带走</span><h2>电流课过关</h2>
<ul><li>会说串并联电流规律。</li><li>会正确使用电流表。</li></ul>
</div></section>""",
        "upgrade": """<!-- teachany-upgrade-v2 -->
<!-- upgrade topic: 电流与电路（去套路） -->
<section class="section teachany-upgrade-block"><h2>📝 中考风格真题</h2>
<div class="tu-q" data-answer="A"><h3>选择题 1</h3><p>关于电流表使用，错误的是</p><div class="tu-opts">
<button type="button" class="tu-opt" data-choice="A" data-diagnosis="这正是错误做法">A. 可以直接接在电源两极上测电源</button>
<button type="button" class="tu-opt" data-choice="B" data-diagnosis="正确要求">B. 应串联在电路中</button>
<button type="button" class="tu-opt" data-choice="C" data-diagnosis="正确要求">C. 电流从正接线柱流入</button>
<button type="button" class="tu-opt" data-choice="D" data-diagnosis="正确要求">D. 选择合适量程</button>
</div><div class="tu-fb" hidden></div></div>
<div class="tu-fill"><h3>填空题 1</h3><p>串联电路中电流 ____（填“相等”或“不相等”）。</p>
<details><summary>查看答案</summary><p><strong>答案：</strong>相等</p></details></div>
</section>
<section class="section teachany-upgrade-block" data-interactive="conceptest"><h2>💡 概念检测</h2>
<p>“电流表可以并联在用电器两端测电流”</p><div class="tu-opts tu-concept">
<button type="button" class="tu-opt" data-choice="A" data-correct="false" data-diagnosis="电流表必须串联">A. 正确</button>
<button type="button" class="tu-opt" data-choice="B" data-correct="true" data-diagnosis="测电流要串联；并联的是电压表">B. 错误</button>
<button type="button" class="tu-opt" data-choice="C" data-correct="false" data-diagnosis="仍错">C. 只在直流时正确</button>
<button type="button" class="tu-opt" data-choice="D" data-correct="false" data-diagnosis="仍错">D. 只在交流时正确</button>
</div><div class="tu-fb" hidden></div></section>
<section class="section teachany-upgrade-block" data-interactive="inquiry"><h2>🔬 探究记录</h2>
<div class="tu-inquiry">
<label>💡 假设<textarea data-inq="h" placeholder="串联两处电流是否相等？"></textarea></label>
<label>📊 证据<textarea data-inq="e" placeholder="两处电流表示数"></textarea></label>
<label>✅ 结论<textarea data-inq="c" placeholder="串联电流相等"></textarea></label>
</div>
<button type="button" class="tu-save">保存探究记录（本机）</button>
<div class="tu-fb" data-inq-fb hidden></div></section>
""",
        "fingerprint": "为什么保险丝会",
    },
    "phy-m-electrical-safety": {
        "subtitle": "触电、漏电、保险丝——家庭用电怎样才安全？",
        "figcaption": "安全用电：触电类型、保险丝/空气开关、接地与基本原则",
        "anchors": [
            ("触电常见原因是什么？", "触电常见原因是什么？"),
            ("保险丝的作用是什么？", "保险丝的作用是什么？"),
            ("安全用电原则有哪些？", "安全用电原则有哪些？"),
        ],
        "objectives": [
            "了解常见触电事故类型与危险",
            "理解保险丝（或空气开关）的保护作用",
            "能说出家庭安全用电的基本原则与做法",
        ],
        "story": """<section class="section" id="story" data-tts="story" data-tsh="真实情境"><div class="lesson-panel"><span class="phase-tag">真实情境</span><h2>湿手拔插头，为什么特别危险？</h2>
<p>水会降低人体电阻，电流更容易通过人体。安全用电不是口号，而是：不接触低压带电体、不靠近高压带电体，并用保险丝等装置在电流过大时切断电路。</p>
<div class="mini-grid">
<div class="mini-panel"><h3>已有经验</h3><p>家中漏电保护器跳闸、插座儿童保护门。</p></div>
<div class="mini-panel"><h3>真正卡点</h3><p>以为“电压不高就绝对没事”；分不清保险丝熔断是保护还是故障本身。</p></div>
<div class="mini-panel"><h3>本课任务</h3><p>危险来源 → 保护装置 → 安全原则。</p></div>
</div>
</div></section>""",
        "checklist": """<section class="section" id="experiment-checklist" data-tts="experiment-checklist" data-bloom-level="analyze" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">安全检查表</span><h2>家庭用电三问</h2>
<p><strong>会不会使人触电？</strong>是否接触带电体、环境是否潮湿。</p>
<p><strong>电流过大怎么办？</strong>保险丝/空气开关能否切断。</p>
<p><strong>电器是否超载？</strong>接线、插座、功率是否匹配。</p>
</div></section>""",
        "pretest": """<section class="section" id="pretest" data-tts="pretest" data-bloom-level="remember" data-scaffold="full" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">前测</span><h2>前测：保险丝熔断说明什么？</h2>
<p><strong>更合理的理解是？</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">A. 保险丝坏了所以电路更危险，应换成铜丝</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'pretest')">B. 电路电流过大时保险丝熔断，起到保护作用</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">C. 保险丝熔断后应继续加大用电器功率</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">D. 保险丝与安全无关</button>
<div id="pretest-feedback" class="feedback">保险丝是保护元件，不能用铜丝替代。</div></div></section>""",
        "core": """<section class="section" id="core" data-tts="core" data-bloom-level="understand" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">核心概念</span><h2>安全用电要点</h2>
<div class="mini-grid">
<div class="mini-panel"><h3>原则</h3><p>不接触低压带电体；不靠近高压带电体。</p></div>
<div class="mini-panel"><h3>保护</h3><p>保险丝/空气开关在电流过大时切断电路，保护用电器与线路。</p></div>
<div class="mini-panel"><h3>习惯</h3><p>湿手不碰电器；检修先断电；插座不乱插大功率电器。</p></div>
</div></div></section>""",
        "deep": """<section class="section" id="deep-understanding" data-tts="deep-understanding"><div class="lesson-panel insight-box"><span class="phase-tag">易混辨析</span><h2>保险丝不是“越粗越好”</h2>
<ul>
<li>额定电流要匹配电路设计；过粗等于失去保护。</li>
<li>用铜丝代替保险丝非常危险。</li>
<li>触电急救：先切断电源，再施救（按安全规范）。</li>
</ul>
</div></section>""",
        "worked": """<section class="section" id="worked-example" data-tts="worked-example" data-bloom-level="analyze" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">例题拆解</span><h2>例题：为什么不能用铜丝代替保险丝？</h2>
<p>铜丝熔点高、不易熔断，电流过大时不能及时切断电路，失去保护作用，可能导致导线过热起火。</p>
</div></section>""",
        "transfer": """<section class="section" id="transfer-task" data-tts="transfer-task" data-bloom-level="create" data-scaffold="none"><div class="lesson-panel"><span class="phase-tag">迁移任务</span><h2>给家里写 5 条用电安全提醒</h2>
<p>每条对应一个具体场景（浴室、厨房、插排、电器检修等）。</p>
</div></section>""",
        "lab_html": """<section class="section" id="interactive-lab" data-tts="interactive-lab" data-bloom-level="apply" data-scaffold="partial" data-interactive="safety-lab"><div class="lesson-panel"><span class="phase-tag">互动实验</span><h2>调电路电流，看保险丝是否熔断（示意）</h2>
<div class="control-row">
<label>电路电流（A）<input id="safe-i" type="range" min="1" max="20" value="5"></label>
<label>保险丝额定（A）<input id="safe-fuse" type="range" min="3" max="15" value="10"></label>
</div>
<div class="canvas-wrap"><canvas id="physics-canvas" class="wide-canvas" width="900" height="430"></canvas></div>
<div id="lab-feedback" class="feedback">当电流大于额定值，示意熔断。</div></div></section>
<script>
(function(){
  const canvas=document.getElementById('physics-canvas'); if(!canvas) return;
  const ctx=canvas.getContext('2d');
  const iEl=document.getElementById('safe-i'), fEl=document.getElementById('safe-fuse');
  const fb=document.getElementById('lab-feedback');
  function draw(){
    const I=+iEl.value, F=+fEl.value, blow=I>F;
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='#081426'; ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle=blow?'#f97316':'#22c55e';
    ctx.fillRect(300,200,300,40);
    ctx.fillStyle='#fbbf24'; ctx.font='28px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('保险丝保护示意',80,70);
    ctx.fillStyle='#e2e8f0'; ctx.font='24px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('I='+I+' A，额定='+F+' A → '+(blow?'熔断保护':'正常'),80,130);
    fb.textContent=blow?'电流过大，保险丝熔断，切断电路（保护）。':'电流未超过额定，电路保持接通。';
  }
  iEl.addEventListener('input',draw); fEl.addEventListener('input',draw); draw();
})();
</script>
<script>const FEEDBACK={pretest:"保险丝在电流过大时熔断，起保护作用，不能用铜丝代替。",posttest:"安全用电：不接触低压带电体，不靠近高压带电体。"};
function checkAnswer(btn,ok,target){btn.parentElement.querySelectorAll('.quiz-option').forEach(b=>b.classList.remove('correct','wrong'));btn.classList.add(ok?'correct':'wrong');const box=document.getElementById(target+'-feedback');if(box)box.textContent=ok?('✅ '+FEEDBACK[target]):('❌ 再想想：'+FEEDBACK[target]);}</script>
""",
        "external": """<section class="section" id="external-sim" data-tts="external-sim"><div class="lesson-panel"><span class="phase-tag">实验回放</span><h2>安全用电三句话</h2>
<ol><li>触电危险来自电流通过人体。</li><li>保险丝/空气开关保护电路。</li><li>遵守安全原则与良好习惯。</li></ol>
</div></section>""",
        "posttest": """<section class="section" id="posttest" data-tts="posttest" data-bloom-level="evaluate" data-scaffold="none" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">后测</span><h2>后测</h2>
<p><strong>安全用电的基本原则包括</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">A. 可以随便接触低压带电体</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'posttest')">B. 不接触低压带电体，不靠近高压带电体</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">C. 用铜丝代替保险丝更安全</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">D. 湿手拔插头更导电所以更安全</button>
<div id="posttest-feedback" class="feedback">记住两条基本原则。</div></div></section>""",
        "summary": """<section class="section" id="summary" data-tts="summary"><div class="lesson-panel"><span class="phase-tag">一句话带走</span><h2>安全用电过关</h2>
<ul><li>知道触电危险。</li><li>理解保险丝作用。</li><li>能说出安全原则与习惯。</li></ul>
</div></section>""",
        "upgrade": """<!-- teachany-upgrade-v2 -->
<!-- upgrade topic: 安全用电（去套路） -->
<section class="section teachany-upgrade-block"><h2>📝 中考风格真题</h2>
<div class="tu-q" data-answer="C"><h3>选择题 1</h3><p>下列做法正确的是</p><div class="tu-opts">
<button type="button" class="tu-opt" data-choice="A" data-diagnosis="危险">A. 湿手拔插头</button>
<button type="button" class="tu-opt" data-choice="B" data-diagnosis="危险">B. 用铜丝代替保险丝</button>
<button type="button" class="tu-opt" data-choice="C" data-diagnosis="检修先断电">C. 检修电路前切断电源</button>
<button type="button" class="tu-opt" data-choice="D" data-diagnosis="危险">D. 在电线上晾湿衣服</button>
</div><div class="tu-fb" hidden></div></div>
<div class="tu-fill"><h3>填空题 1</h3><p>保险丝的作用是在电流过大时 ____ 电路。</p>
<details><summary>查看答案</summary><p><strong>答案：</strong>切断（熔断保护）</p></details></div>
</section>
<section class="section teachany-upgrade-block" data-interactive="conceptest"><h2>💡 概念检测</h2>
<p>“保险丝越粗越安全”</p><div class="tu-opts tu-concept">
<button type="button" class="tu-opt" data-choice="A" data-correct="false" data-diagnosis="过粗会失去保护">A. 正确</button>
<button type="button" class="tu-opt" data-choice="B" data-correct="true" data-diagnosis="额定要匹配，过粗危险">B. 错误，可能失去保护</button>
<button type="button" class="tu-opt" data-choice="C" data-correct="false" data-diagnosis="仍错">C. 正确，越粗越不容易坏</button>
<button type="button" class="tu-opt" data-choice="D" data-correct="false" data-diagnosis="仍错">D. 正确，铜丝最好</button>
</div><div class="tu-fb" hidden></div></section>
<section class="section teachany-upgrade-block" data-interactive="inquiry"><h2>🔬 探究记录</h2>
<div class="tu-inquiry">
<label>💡 假设<textarea data-inq="h" placeholder="为什么不能用铜丝替代保险丝？"></textarea></label>
<label>📊 证据<textarea data-inq="e" placeholder="熔点/能否及时熔断"></textarea></label>
<label>✅ 结论<textarea data-inq="c" placeholder="失去保护会更危险"></textarea></label>
</div>
<button type="button" class="tu-save">保存探究记录（本机）</button>
<div class="tu-fb" data-inq-fb hidden></div></section>
""",
        "fingerprint": "湿手拔插头，为什么特别危险",
    },
}


def replace_section(html: str, section_id: str, new_html: str) -> str:
    pat = rf'<section class="section" id="{section_id}"[^>]*>.*?</section>'
    html2, n = re.subn(pat, new_html, html, count=1, flags=re.S)
    if not n:
        raise RuntimeError(f"section id={section_id} not found")
    return html2


def apply_course(cid: str) -> str:
    if cid not in COURSES:
        return f"{cid}: 无手写配方"
    cfg = COURSES[cid]
    path = COMMUNITY / cid / "index.html"
    if not path.exists():
        return f"{cid}: 无 index.html"
    html = path.read_text(encoding="utf-8")
    if cfg["fingerprint"] in html and "And 已有经验" not in html:
        return f"{cid}: 已是去套路版，跳过"

    # subtitle: replace first hero subtitle loosely
    html = re.sub(
        r'(<header class="hero"[^>]*>.*?<p class="subtitle">).*?(</p>)',
        r"\1" + cfg["subtitle"] + r"\2",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r"<figcaption>.*?</figcaption>",
        f"<figcaption>{cfg['figcaption']}</figcaption>",
        html,
        count=1,
        flags=re.S,
    )
    anchors = "".join(
        f'<button class="choice" data-anchor-choice="{a[0]}">{a[1]}</button>\n'
        for a in cfg["anchors"]
    )
    html = re.sub(
        r'(<div class="grid" id="problem-anchor-choices">).*?(</div>\s*<label)',
        r"\1\n" + anchors + r"\2",
        html,
        count=1,
        flags=re.S,
    )
    objs = "".join(f"<li>{x}</li>\n" for x in cfg["objectives"])
    html = re.sub(
        r'(<ul class="objectives">).*?(</ul>)',
        r"\1\n" + objs + r"\2",
        html,
        count=1,
        flags=re.S,
    )

    for sid, key in [
        ("story", "story"),
        ("experiment-checklist", "checklist"),
        ("pretest", "pretest"),
        ("core", "core"),
        ("deep-understanding", "deep"),
        ("worked-example", "worked"),
        ("transfer-task", "transfer"),
        ("external-sim", "external"),
        ("posttest", "posttest"),
        ("summary", "summary"),
    ]:
        html = replace_section(html, sid, cfg[key])

    # interactive lab + old script
    html = re.sub(
        r'<section class="section" id="interactive-lab"[^>]*>.*?</section>\s*<script>const FEEDBACK=.*?</script>',
        cfg["lab_html"],
        html,
        count=1,
        flags=re.S,
    )
    if "data-interactive=" not in html or cid.split("-")[-1][:4] not in html:
        # fallback if script pattern differed
        html = re.sub(
            r'<section class="section" id="interactive-lab"[^>]*>.*?</section>',
            cfg["lab_html"].split("<script>")[0] + "</section>",
            html,
            count=1,
            flags=re.S,
        )
        html = re.sub(
            r"<script>const FEEDBACK=\{ pretest:.*?drawGeneric\(\);\s*</script>",
            "<script>" + "<script>".join(cfg["lab_html"].split("<script>")[1:]),
            html,
            count=1,
            flags=re.S,
        )

    # strip wrong phet leftovers
    html = html.replace(
        "https://phet.colorado.edu/sims/html/forces-and-motion-basics/latest/forces-and-motion-basics_zh_CN.html",
        "",
    )

    if "<!-- teachany-upgrade-v2 -->" in html:
        html = re.sub(
            r"<!-- teachany-upgrade-v2 -->.*?(?=<style id=\"teachany-upgrade-v2-css\">|<!--\s*v7\.7\.4|<section class=\"section\" id=\"knowledge-graph\")",
            cfg["upgrade"],
            html,
            count=1,
            flags=re.S,
        )
    else:
        html = re.sub(
            r'(<section class="section" id="knowledge-graph")',
            cfg["upgrade"] + r"\1",
            html,
            count=1,
        )

    if "teachany-upgrade-v2-css" not in html:
        html = html.replace(
            "<!-- teachany-upgrade-v2 -->",
            "<!-- teachany-upgrade-v2 -->\n" + UPGRADE_CSS_JS,
            1,
        )

    path.write_text(html, encoding="utf-8")
    t = path.read_text(encoding="utf-8")
    ok = cfg["fingerprint"] in t and "And 已有经验" not in t and "forces-and-motion-basics" not in t
    return f"{cid}: {'OK' if ok else 'CHECK'} fingerprint={cfg['fingerprint'][:12]}…"


def main():
    cids = sys.argv[1:] or list(COURSES.keys())
    for cid in cids:
        try:
            print(apply_course(cid), flush=True)
        except Exception as e:
            print(f"{cid}: FAIL {e}", flush=True)


if __name__ == "__main__":
    main()
