#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batch A recipes: simple-machines, resistance, voltage, ohms-law, series-parallel."""
from __future__ import annotations

BATCH_A = {
    "phy-m-simple-machines": {
        "subtitle": "撬棍、滑轮、斜面——怎样用更小的力办成同样的事？",
        "figcaption": "简单机械：杠杆平衡、滑轮、斜面与机械效率",
        "anchors": [
            ("杠杆怎样省力？", "杠杆怎样省力？"),
            ("定滑轮和动滑轮有何不同？", "定滑轮和动滑轮有何不同？"),
            ("机械效率为什么小于 1？", "机械效率为什么小于 1？"),
        ],
        "objectives": [
            "能用杠杆平衡条件解释省力/费力杠杆",
            "区分定滑轮与动滑轮的作用",
            "理解有用功、额外功与机械效率",
        ],
        "story": """<section class="section" id="story" data-tts="story" data-tsh="真实情境"><div class="lesson-panel"><span class="phase-tag">真实情境</span><h2>为什么一根撬棍能撬起大石头？</h2>
<p>撬棍是杠杆：在支点一侧用较小的力，另一侧可以产生较大效果——代价是力臂更长、手移动的距离更大。<strong>省力不省功</strong>是简单机械的核心。</p>
<div class="mini-grid">
<div class="mini-panel"><h3>已有经验</h3><p>剪刀、瓶起子、旗杆定滑轮、斜坡推车。</p></div>
<div class="mini-panel"><h3>真正卡点</h3><p>以为机械可以“凭空省功”；分不清动力臂与阻力臂。</p></div>
<div class="mini-panel"><h3>本课任务</h3><p>杠杆条件 → 滑轮 → 效率。</p></div>
</div></div></section>""",
        "checklist": """<section class="section" id="experiment-checklist" data-tts="experiment-checklist" data-bloom-level="analyze" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">实验检查表</span><h2>杠杆题三问</h2>
<p><strong>支点在哪？</strong>动力、阻力作用点在哪？</p>
<p><strong>力臂怎么量？</strong>从支点到力的作用线的垂直距离。</p>
<p><strong>平衡条件？</strong>动力×动力臂 = 阻力×阻力臂。</p>
</div></section>""",
        "pretest": """<section class="section" id="pretest" data-tts="pretest" data-bloom-level="remember" data-scaffold="full" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">前测</span><h2>前测：省力杠杆一定更好吗？</h2>
<p><strong>正确的是？</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">A. 省力杠杆一定省距离</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'pretest')">B. 省力往往费距离；费力往往省距离</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">C. 简单机械可以让有用功大于总功</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">D. 定滑轮一定省力一半</button>
<div id="pretest-feedback" class="feedback">省力不省功；定滑轮不省力，只改变方向。</div></div></section>""",
        "core": """<section class="section" id="core" data-tts="core" data-bloom-level="understand" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">核心概念</span><h2>简单机械要点</h2>
<div class="mini-grid">
<div class="mini-panel"><h3>杠杆</h3><p>平衡：F₁L₁=F₂L₂。动力臂大于阻力臂→省力。</p></div>
<div class="mini-panel"><h3>滑轮</h3><p>定滑轮：不省力，改变方向。动滑轮：省一半力（理想），费距离。</p></div>
<div class="mini-panel"><h3>效率</h3><p>η=W有用/W总×100%。额外功来自摩擦、自重等，η&lt;1。</p></div>
</div></div></section>""",
        "deep": """<section class="section" id="deep-understanding" data-tts="deep-understanding"><div class="lesson-panel insight-box"><span class="phase-tag">易混辨析</span><h2>省力 ≠ 省功</h2>
<ul>
<li>任何机械都不能使有用功大于总功。</li>
<li>力臂是“垂直距离”，不是杆长本身。</li>
<li>剪刀、筷子、镊子：有的省力，有的费力但更灵活。</li>
</ul>
</div></section>""",
        "worked": """<section class="section" id="worked-example" data-tts="worked-example" data-bloom-level="analyze" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">例题拆解</span><h2>例题：撬棍</h2>
<p>阻力 600 N，阻力臂 0.2 m，动力臂 1.2 m。理想情况下动力 F=600×0.2/1.2=100 N。</p>
</div></section>""",
        "transfer": """<section class="section" id="transfer-task" data-tts="transfer-task" data-bloom-level="create" data-scaffold="none"><div class="lesson-panel"><span class="phase-tag">迁移任务</span><h2>判断家里 3 件工具：省力还是费力杠杆？</h2>
</div></section>""",
        "lab_html": """<section class="section" id="interactive-lab" data-tts="interactive-lab" data-bloom-level="apply" data-scaffold="partial" data-interactive="lever-lab"><div class="lesson-panel"><span class="phase-tag">互动实验</span><h2>调动力臂与阻力，看所需动力</h2>
<p style="color:var(--muted)">理想杠杆：F₁ = F₂ L₂ / L₁</p>
<div class="control-row">
<label>阻力 F₂（N）<input id="lev-f2" type="range" min="50" max="800" step="10" value="400"></label>
<label>阻力臂 L₂（cm）<input id="lev-l2" type="range" min="10" max="80" value="20"></label>
<label>动力臂 L₁（cm）<input id="lev-l1" type="range" min="20" max="150" value="100"></label>
</div>
<div class="canvas-wrap"><canvas id="physics-canvas" class="wide-canvas" width="900" height="430"></canvas></div>
<div id="lab-feedback" class="feedback">观察 F₁ 随力臂变化。</div></div></section>
<script>
(function(){
  const canvas=document.getElementById('physics-canvas'); if(!canvas) return;
  const ctx=canvas.getContext('2d');
  const f2=document.getElementById('lev-f2'), l2=document.getElementById('lev-l2'), l1=document.getElementById('lev-l1');
  const fb=document.getElementById('lab-feedback');
  function draw(){
    const F2=+f2.value, L2=+l2.value/100, L1=+l1.value/100;
    const F1=F2*L2/L1;
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='#081426'; ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.strokeStyle='#94a3b8'; ctx.lineWidth=8;
    ctx.beginPath(); ctx.moveTo(150,250); ctx.lineTo(750,250); ctx.stroke();
    ctx.fillStyle='#f97316'; ctx.beginPath(); ctx.moveTo(450,250); ctx.lineTo(430,290); ctx.lineTo(470,290); ctx.fill();
    ctx.fillStyle='#fbbf24'; ctx.font='28px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('杠杆平衡：F₁L₁=F₂L₂',80,70);
    ctx.fillStyle='#e2e8f0'; ctx.font='24px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('F₂='+F2+' N，L₂='+L2.toFixed(2)+' m，L₁='+L1.toFixed(2)+' m',80,120);
    ctx.fillText('所需动力 F₁ ≈ '+F1.toFixed(1)+' N',80,170);
    fb.textContent='动力约 '+F1.toFixed(1)+' N。增大 L₁ 或减小 L₂，都会更省力。';
  }
  [f2,l2,l1].forEach(el=>el.addEventListener('input',draw)); draw();
})();
</script>
<script>const FEEDBACK={pretest:"省力往往费距离；机械不能省功。",posttest:"F₁L₁=F₂L₂；定滑轮不省力。"};
function checkAnswer(btn,ok,target){btn.parentElement.querySelectorAll('.quiz-option').forEach(b=>b.classList.remove('correct','wrong'));btn.classList.add(ok?'correct':'wrong');const box=document.getElementById(target+'-feedback');if(box)box.textContent=ok?('✅ '+FEEDBACK[target]):('❌ 再想想：'+FEEDBACK[target]);}</script>
""",
        "external": """<section class="section" id="external-sim" data-tts="external-sim"><div class="lesson-panel"><span class="phase-tag">实验回放</span><h2>简单机械三句话</h2>
<ol><li>杠杆平衡看力×力臂。</li><li>定滑轮改方向，动滑轮可省力。</li><li>效率总小于 100%。</li></ol>
</div></section>""",
        "posttest": """<section class="section" id="posttest" data-tts="posttest" data-bloom-level="evaluate" data-scaffold="none" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">后测</span><h2>后测</h2>
<p><strong>关于定滑轮，正确的是？</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,true,'posttest')">A. 不省力，但能改变力的方向</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">B. 一定省一半力</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">C. 能使有用功大于总功</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">D. 力臂概念不适用于杠杆</button>
<div id="posttest-feedback" class="feedback">定滑轮本质是等臂杠杆。</div></div></section>""",
        "summary": """<section class="section" id="summary" data-tts="summary"><div class="lesson-panel"><span class="phase-tag">一句话带走</span><h2>简单机械过关</h2>
<ul><li>会用杠杆平衡条件。</li><li>分清定/动滑轮。</li><li>理解效率与额外功。</li></ul>
</div></section>""",
        "upgrade": """<!-- teachany-upgrade-v2 -->
<!-- upgrade topic: 简单机械（去套路） -->
<section class="section teachany-upgrade-block"><h2>📝 中考风格真题</h2>
<div class="tu-q" data-answer="B"><h3>选择题 1</h3><p>杠杆平衡条件是</p><div class="tu-opts">
<button type="button" class="tu-opt" data-choice="A" data-diagnosis="不是力相等即可">A. 动力=阻力</button>
<button type="button" class="tu-opt" data-choice="B" data-diagnosis="F₁L₁=F₂L₂">B. 动力×动力臂=阻力×阻力臂</button>
<button type="button" class="tu-opt" data-choice="C" data-diagnosis="不是臂长相等即可">C. 动力臂=阻力臂</button>
<button type="button" class="tu-opt" data-choice="D" data-diagnosis="错误">D. 动力+阻力=0</button>
</div><div class="tu-fb" hidden></div></div>
<div class="tu-fill"><h3>填空题 1</h3><p>机械效率 η = W有用 / ____ 。</p>
<details><summary>查看答案</summary><p><strong>答案：</strong>W总</p></details></div>
</section>
<section class="section teachany-upgrade-block" data-interactive="conceptest"><h2>💡 概念检测</h2>
<p>“简单机械可以省功”</p><div class="tu-opts tu-concept">
<button type="button" class="tu-opt" data-choice="A" data-correct="false" data-diagnosis="只能省力或省距离，不能省功">A. 正确</button>
<button type="button" class="tu-opt" data-choice="B" data-correct="true" data-diagnosis="任何机械都不能使有用功大于总功">B. 错误</button>
<button type="button" class="tu-opt" data-choice="C" data-correct="false" data-diagnosis="仍错">C. 只对滑轮正确</button>
<button type="button" class="tu-opt" data-choice="D" data-correct="false" data-diagnosis="仍错">D. 只对杠杆正确</button>
</div><div class="tu-fb" hidden></div></section>
<section class="section teachany-upgrade-block" data-interactive="inquiry"><h2>🔬 探究记录</h2>
<div class="tu-inquiry">
<label>💡 假设<textarea data-inq="h" placeholder="增大动力臂是否更省力？"></textarea></label>
<label>📊 证据<textarea data-inq="e" placeholder="记录力与力臂"></textarea></label>
<label>✅ 结论<textarea data-inq="c" placeholder="联系平衡条件"></textarea></label>
</div>
<button type="button" class="tu-save">保存探究记录（本机）</button>
<div class="tu-fb" data-inq-fb hidden></div></section>
""",
        "fingerprint": "为什么一根撬棍能撬起大石头",
    },
    "phy-m-resistance": {
        "subtitle": "同样电压，为什么有的灯更亮？电阻到底在挡什么？",
        "figcaption": "电阻：定义、影响因素、滑动变阻器",
        "anchors": [
            ("电阻的定义是什么？", "电阻的定义是什么？"),
            ("哪些因素影响电阻？", "哪些因素影响电阻？"),
            ("滑动变阻器怎样改变电阻？", "滑动变阻器怎样改变电阻？"),
        ],
        "objectives": [
            "理解电阻是导体对电流的阻碍作用",
            "知道电阻与材料、长度、横截面积、温度有关",
            "会说明滑动变阻器改变接入电路长度从而改变电阻",
        ],
        "story": """<section class="section" id="story" data-tts="story" data-tsh="真实情境"><div class="lesson-panel"><span class="phase-tag">真实情境</span><h2>调光台灯为什么能由亮变暗？</h2>
<p>很多调光靠改变电路中的电阻：电阻变大，电流变小，灯变暗。电阻不是“电量”，而是导体对电流的<strong>阻碍程度</strong>。</p>
<div class="mini-grid">
<div class="mini-panel"><h3>已有经验</h3><p>电线有粗有细；电阻丝会发热。</p></div>
<div class="mini-panel"><h3>真正卡点</h3><p>以为电阻随电压变；把电阻率与电阻混为一谈。</p></div>
<div class="mini-panel"><h3>本课任务</h3><p>定义 → 影响因素 → 变阻器。</p></div>
</div></div></section>""",
        "checklist": """<section class="section" id="experiment-checklist" data-tts="experiment-checklist" data-bloom-level="analyze" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">实验检查表</span><h2>研究电阻影响因素</h2>
<p><strong>控制变量：</strong>比长度时材料、横截面积、温度相同。</p>
<p><strong>观察什么：</strong>电流表示数变化（电压一定时）。</p>
</div></section>""",
        "pretest": """<section class="section" id="pretest" data-tts="pretest" data-bloom-level="remember" data-scaffold="full" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">前测</span><h2>前测</h2>
<p><strong>关于电阻，正确的是？</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">A. 电阻随电压增大而增大</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'pretest')">B. 电阻是导体本身的性质，与电压电流无关（常温下金属丝等）</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">C. 横截面积越大电阻一定越大</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">D. 长度越长电阻越小</button>
<div id="pretest-feedback" class="feedback">电阻是导体性质；与材料、长度、横截面积、温度有关。</div></div></section>""",
        "core": """<section class="section" id="core" data-tts="core" data-bloom-level="understand" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">核心概念</span><h2>电阻 R</h2>
<div class="mini-grid">
<div class="mini-panel"><h3>定义</h3><p>导体对电流的阻碍作用叫电阻，单位欧姆（Ω）。</p></div>
<div class="mini-panel"><h3>影响因素</h3><p>材料、长度（越长越大）、横截面积（越粗越小）、温度。</p></div>
<div class="mini-panel"><h3>变阻器</h3><p>靠改变接入电路的电阻丝长度改变电阻。</p></div>
</div></div></section>""",
        "deep": """<section class="section" id="deep-understanding" data-tts="deep-understanding"><div class="lesson-panel insight-box"><span class="phase-tag">易混辨析</span><h2>R 不是由 U/I“决定性质”</h2>
<ul>
<li>可用 R=U/I 计算某一状态下的电阻值。</li>
<li>但不能说“电阻随电压变”；对欧姆定律适用的导体，R 由导体本身决定。</li>
</ul>
</div></section>""",
        "worked": """<section class="section" id="worked-example" data-tts="worked-example" data-bloom-level="analyze" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">例题拆解</span><h2>例题</h2>
<p>两根同种材料电阻丝，长度比为 2:1，横截面积比为 1:2，则电阻比为 4:1。</p>
</div></section>""",
        "transfer": """<section class="section" id="transfer-task" data-tts="transfer-task" data-bloom-level="create" data-scaffold="none"><div class="lesson-panel"><span class="phase-tag">迁移任务</span><h2>解释：为何远距离输电要用粗导线？</h2>
</div></section>""",
        "lab_html": """<section class="section" id="interactive-lab" data-tts="interactive-lab" data-bloom-level="apply" data-scaffold="partial" data-interactive="R-lab"><div class="lesson-panel"><span class="phase-tag">互动实验</span><h2>调长度与横截面积，看电阻示意</h2>
<p style="color:var(--muted)">示意：R ∝ L / S</p>
<div class="control-row">
<label>长度 L<input id="r-l" type="range" min="1" max="20" value="8"></label>
<label>横截面积 S<input id="r-s" type="range" min="1" max="20" value="4"></label>
</div>
<div class="canvas-wrap"><canvas id="physics-canvas" class="wide-canvas" width="900" height="430"></canvas></div>
<div id="lab-feedback" class="feedback">观察 R 示意值变化。</div></div></section>
<script>
(function(){
  const canvas=document.getElementById('physics-canvas'); if(!canvas) return;
  const ctx=canvas.getContext('2d');
  const lEl=document.getElementById('r-l'), sEl=document.getElementById('r-s');
  const fb=document.getElementById('lab-feedback');
  function draw(){
    const L=+lEl.value, S=+sEl.value, R=L/S;
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='#081426'; ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='#f59e0b'; ctx.fillRect(200,250, L*20, Math.max(8,S*3));
    ctx.fillStyle='#fbbf24'; ctx.font='28px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('R ∝ L / S（同种材料）',80,70);
    ctx.fillStyle='#e2e8f0'; ctx.font='24px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('L='+L+'，S='+S+'，R示意='+R.toFixed(2),80,120);
    fb.textContent='电阻示意 '+R.toFixed(2)+'。加长或变细，电阻变大。';
  }
  lEl.addEventListener('input',draw); sEl.addEventListener('input',draw); draw();
})();
</script>
<script>const FEEDBACK={pretest:"电阻是导体性质，与材料、长度、横截面积、温度有关。",posttest:"变阻器改变接入长度从而改变电阻。"};
function checkAnswer(btn,ok,target){btn.parentElement.querySelectorAll('.quiz-option').forEach(b=>b.classList.remove('correct','wrong'));btn.classList.add(ok?'correct':'wrong');const box=document.getElementById(target+'-feedback');if(box)box.textContent=ok?('✅ '+FEEDBACK[target]):('❌ 再想想：'+FEEDBACK[target]);}</script>
""",
        "external": """<section class="section" id="external-sim" data-tts="external-sim"><div class="lesson-panel"><span class="phase-tag">实验回放</span><h2>电阻三句话</h2>
<ol><li>电阻表示阻碍作用。</li><li>与材料、长度、横截面积、温度有关。</li><li>变阻器改接入长度。</li></ol>
</div></section>""",
        "posttest": """<section class="section" id="posttest" data-tts="posttest" data-bloom-level="evaluate" data-scaffold="none" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">后测</span><h2>后测</h2>
<p><strong>同种材料，长度加倍、横截面积减半，电阻变为原来的</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">A. 2 倍</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'posttest')">B. 4 倍</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">C. 1/2</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">D. 不变</button>
<div id="posttest-feedback" class="feedback">R∝L/S → 2/(1/2)=4。</div></div></section>""",
        "summary": """<section class="section" id="summary" data-tts="summary"><div class="lesson-panel"><span class="phase-tag">一句话带走</span><h2>电阻课过关</h2>
<ul><li>会说定义与单位。</li><li>会分析影响因素。</li><li>会解释变阻器。</li></ul>
</div></section>""",
        "upgrade": """<!-- teachany-upgrade-v2 -->
<!-- upgrade topic: 电阻（去套路） -->
<section class="section teachany-upgrade-block"><h2>📝 中考风格真题</h2>
<div class="tu-q" data-answer="A"><h3>选择题 1</h3><p>下列说法正确的是</p><div class="tu-opts">
<button type="button" class="tu-opt" data-choice="A" data-diagnosis="导体越长电阻越大（其它条件相同）">A. 同种材料，长度越长电阻越大</button>
<button type="button" class="tu-opt" data-choice="B" data-diagnosis="越粗电阻越小">B. 横截面积越大电阻越大</button>
<button type="button" class="tu-opt" data-choice="C" data-diagnosis="电阻是性质">C. 电阻随电压成正比增大</button>
<button type="button" class="tu-opt" data-choice="D" data-diagnosis="材料影响电阻">D. 材料不影响电阻</button>
</div><div class="tu-fb" hidden></div></div>
<div class="tu-fill"><h3>填空题 1</h3><p>电阻的单位是 ____。</p>
<details><summary>查看答案</summary><p><strong>答案：</strong>欧姆（Ω）</p></details></div>
</section>
<section class="section teachany-upgrade-block" data-interactive="conceptest"><h2>💡 概念检测</h2>
<p>“电压越大，导体电阻越大”</p><div class="tu-opts tu-concept">
<button type="button" class="tu-opt" data-choice="A" data-correct="false" data-diagnosis="混淆了计算式与决定因素">A. 正确</button>
<button type="button" class="tu-opt" data-choice="B" data-correct="true" data-diagnosis="电阻由导体本身决定（适用范围内）">B. 错误</button>
<button type="button" class="tu-opt" data-choice="C" data-correct="false" data-diagnosis="仍错">C. 只对液体正确</button>
<button type="button" class="tu-opt" data-choice="D" data-correct="false" data-diagnosis="仍错">D. 只对气体正确</button>
</div><div class="tu-fb" hidden></div></section>
<section class="section teachany-upgrade-block" data-interactive="inquiry"><h2>🔬 探究记录</h2>
<div class="tu-inquiry">
<label>💡 假设<textarea data-inq="h" placeholder="导线越长电流是否越小（U一定）？"></textarea></label>
<label>📊 证据<textarea data-inq="e" placeholder="记录长度与电流"></textarea></label>
<label>✅ 结论<textarea data-inq="c" placeholder="联系电阻"></textarea></label>
</div>
<button type="button" class="tu-save">保存探究记录（本机）</button>
<div class="tu-fb" data-inq-fb hidden></div></section>
""",
        "fingerprint": "调光台灯为什么能由亮变暗",
    },
    "phy-m-voltage": {
        "subtitle": "电压是什么？为什么没有电压就没有电流？",
        "figcaption": "电压：作用、电源、电压表使用与串并联电压特点",
        "anchors": [
            ("电压的作用是什么？", "电压的作用是什么？"),
            ("电压表怎样接入？", "电压表怎样接入？"),
            ("串联电路电压有何特点？", "串联电路电压有何特点？"),
        ],
        "objectives": [
            "理解电压是形成电流的原因（与电源有关）",
            "会正确使用电压表（并联、正负、量程）",
            "掌握串联分压、并联电压相等",
        ],
        "story": """<section class="section" id="story" data-tts="story" data-tsh="真实情境"><div class="lesson-panel"><span class="phase-tag">真实情境</span><h2>为什么电池没电灯就不亮？</h2>
<p>电池提供电压，推动电荷定向移动形成电流。电压不是电流，也不等于电阻。测电压要用<strong>电压表并联</strong>在用电器两端。</p>
<div class="mini-grid">
<div class="mini-panel"><h3>已有经验</h3><p>1.5 V 干电池、家庭电路约 220 V。</p></div>
<div class="mini-panel"><h3>真正卡点</h3><p>电压表串联进电路；串并联电压规律记反。</p></div>
<div class="mini-panel"><h3>本课任务</h3><p>电压含义 → 电压表 → 串并联规律。</p></div>
</div></div></section>""",
        "checklist": """<section class="section" id="experiment-checklist" data-tts="experiment-checklist" data-bloom-level="analyze" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">实验检查表</span><h2>用电压表三问</h2>
<p><strong>并联了吗？</strong>电压表必须并联在被测部分两端。</p>
<p><strong>正负对吗？</strong>电流从正接线柱流入。</p>
<p><strong>量程够吗？</strong>先估测或大量程试触。</p>
</div></section>""",
        "pretest": """<section class="section" id="pretest" data-tts="pretest" data-bloom-level="remember" data-scaffold="full" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">前测</span><h2>前测</h2>
<p><strong>测量小灯泡两端电压，电压表应</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,true,'pretest')">A. 与灯泡并联</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">B. 与灯泡串联</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">C. 直接接电源两极且无量程限制</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">D. 可以反接正负无影响</button>
<div id="pretest-feedback" class="feedback">电压表并联；注意正负与量程。</div></div></section>""",
        "core": """<section class="section" id="core" data-tts="core" data-bloom-level="understand" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">核心概念</span><h2>电压 U</h2>
<div class="mini-grid">
<div class="mini-panel"><h3>作用</h3><p>电压使电路中形成电流。单位伏特（V）。电源提供电压。</p></div>
<div class="mini-panel"><h3>电压表</h3><p>测电压，并联；正进负出；不能超过量程。</p></div>
<div class="mini-panel"><h3>串并联</h3><p>串联：总电压等于各部分电压之和。并联：各支路电压相等。</p></div>
</div></div></section>""",
        "deep": """<section class="section" id="deep-understanding" data-tts="deep-understanding"><div class="lesson-panel insight-box"><span class="phase-tag">易混辨析</span><h2>电压表 vs 电流表</h2>
<ul>
<li>电压表：并联，电阻很大。</li>
<li>电流表：串联，电阻很小。</li>
<li>接反或超量程都会损坏仪表。</li>
</ul>
</div></section>""",
        "worked": """<section class="section" id="worked-example" data-tts="worked-example" data-bloom-level="analyze" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">例题拆解</span><h2>例题</h2>
<p>两灯串联，电源电压 6 V，一灯两端 2.5 V，则另一灯两端约 3.5 V。</p>
</div></section>""",
        "transfer": """<section class="section" id="transfer-task" data-tts="transfer-task" data-bloom-level="create" data-scaffold="none"><div class="lesson-panel"><span class="phase-tag">迁移任务</span><h2>画出测小灯泡电压的电路图</h2>
</div></section>""",
        "lab_html": """<section class="section" id="interactive-lab" data-tts="interactive-lab" data-bloom-level="apply" data-scaffold="partial" data-interactive="U-lab"><div class="lesson-panel"><span class="phase-tag">互动实验</span><h2>串联分压示意：U = U₁ + U₂</h2>
<div class="control-row">
<label>U₁（V）<input id="u1" type="range" min="0" max="10" value="3"></label>
<label>U₂（V）<input id="u2" type="range" min="0" max="10" value="3"></label>
</div>
<div class="canvas-wrap"><canvas id="physics-canvas" class="wide-canvas" width="900" height="430"></canvas></div>
<div id="lab-feedback" class="feedback">总电压随两部分变化。</div></div></section>
<script>
(function(){
  const canvas=document.getElementById('physics-canvas'); if(!canvas) return;
  const ctx=canvas.getContext('2d');
  const a=document.getElementById('u1'), b=document.getElementById('u2');
  const fb=document.getElementById('lab-feedback');
  function draw(){
    const u1=+a.value, u2=+b.value, U=u1+u2;
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='#081426'; ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='#fbbf24'; ctx.font='28px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('串联：U = U₁ + U₂',80,70);
    ctx.fillStyle='#e2e8f0'; ctx.font='24px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('U₁='+u1+' V，U₂='+u2+' V，U='+U+' V',80,130);
    ctx.fillStyle='#38bdf8'; ctx.fillRect(200,260,u1*25,36);
    ctx.fillStyle='#a78bfa'; ctx.fillRect(200+u1*25,260,u2*25,36);
    fb.textContent='总电压 '+U+' V。并联时各支路电压相等，对比记忆。';
  }
  a.addEventListener('input',draw); b.addEventListener('input',draw); draw();
})();
</script>
<script>const FEEDBACK={pretest:"电压表要并联。",posttest:"串联分压；并联电压相等。"};
function checkAnswer(btn,ok,target){btn.parentElement.querySelectorAll('.quiz-option').forEach(b=>b.classList.remove('correct','wrong'));btn.classList.add(ok?'correct':'wrong');const box=document.getElementById(target+'-feedback');if(box)box.textContent=ok?('✅ '+FEEDBACK[target]):('❌ 再想想：'+FEEDBACK[target]);}</script>
""",
        "external": """<section class="section" id="external-sim" data-tts="external-sim"><div class="lesson-panel"><span class="phase-tag">实验回放</span><h2>电压三句话</h2>
<ol><li>电压推动形成电流。</li><li>电压表并联。</li><li>串联分压，并联电压相等。</li></ol>
</div></section>""",
        "posttest": """<section class="section" id="posttest" data-tts="posttest" data-bloom-level="evaluate" data-scaffold="none" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">后测</span><h2>后测</h2>
<p><strong>两灯并联在电源两端，则</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,true,'posttest')">A. 两灯两端电压相等</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">B. 两灯两端电压之和等于电源电压的两倍</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">C. 电压表应串联测量</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">D. 没有电压也能有持续电流</button>
<div id="posttest-feedback" class="feedback">并联各支路电压相等。</div></div></section>""",
        "summary": """<section class="section" id="summary" data-tts="summary"><div class="lesson-panel"><span class="phase-tag">一句话带走</span><h2>电压课过关</h2>
<ul><li>会说电压作用。</li><li>会用电压表。</li><li>会串并联电压规律。</li></ul>
</div></section>""",
        "upgrade": """<!-- teachany-upgrade-v2 -->
<!-- upgrade topic: 电压（去套路） -->
<section class="section teachany-upgrade-block"><h2>📝 中考风格真题</h2>
<div class="tu-q" data-answer="B"><h3>选择题 1</h3><p>电压表使用错误的是</p><div class="tu-opts">
<button type="button" class="tu-opt" data-choice="A" data-diagnosis="正确">A. 并联在被测电路两端</button>
<button type="button" class="tu-opt" data-choice="B" data-diagnosis="电压表不能串联当电流表用">B. 串联在电路中测电流</button>
<button type="button" class="tu-opt" data-choice="C" data-diagnosis="正确">C. 注意正负接线柱</button>
<button type="button" class="tu-opt" data-choice="D" data-diagnosis="正确">D. 选择合适量程</button>
</div><div class="tu-fb" hidden></div></div>
<div class="tu-fill"><h3>填空题 1</h3><p>电压的单位是 ____。</p>
<details><summary>查看答案</summary><p><strong>答案：</strong>伏特（V）</p></details></div>
</section>
<section class="section teachany-upgrade-block" data-interactive="conceptest"><h2>💡 概念检测</h2>
<p>“电压表要串联在电路中”</p><div class="tu-opts tu-concept">
<button type="button" class="tu-opt" data-choice="A" data-correct="false" data-diagnosis="应并联">A. 正确</button>
<button type="button" class="tu-opt" data-choice="B" data-correct="true" data-diagnosis="电压表并联">B. 错误</button>
<button type="button" class="tu-opt" data-choice="C" data-correct="false" data-diagnosis="仍错">C. 只在测电源时正确</button>
<button type="button" class="tu-opt" data-choice="D" data-correct="false" data-diagnosis="仍错">D. 只在交流时正确</button>
</div><div class="tu-fb" hidden></div></section>
<section class="section teachany-upgrade-block" data-interactive="inquiry"><h2>🔬 探究记录</h2>
<div class="tu-inquiry">
<label>💡 假设<textarea data-inq="h" placeholder="串联两灯电压之和是否等于电源电压？"></textarea></label>
<label>📊 证据<textarea data-inq="e" placeholder="电压表示数"></textarea></label>
<label>✅ 结论<textarea data-inq="c" placeholder="串联分压"></textarea></label>
</div>
<button type="button" class="tu-save">保存探究记录（本机）</button>
<div class="tu-fb" data-inq-fb hidden></div></section>
""",
        "fingerprint": "为什么电池没电灯就不亮",
    },
    "phy-m-ohms-law": {
        "subtitle": "电流、电压、电阻怎样定量联系？I=U/R 怎么用？",
        "figcaption": "欧姆定律：I=U/R、探究实验、图像与计算",
        "anchors": [
            ("欧姆定律内容是什么？", "欧姆定律内容是什么？"),
            ("怎样用图像表示？", "怎样用图像表示？"),
            ("计算时要注意什么？", "计算时要注意什么？"),
        ],
        "objectives": [
            "掌握欧姆定律：导体中的电流跟电压成正比、跟电阻成反比",
            "会用 I=U/R 及相关变形公式计算",
            "能看懂 I-U 图像（过原点的直线）",
        ],
        "story": """<section class="section" id="story" data-tts="story" data-tsh="真实情境"><div class="lesson-panel"><span class="phase-tag">真实情境</span><h2>电压升高，灯为什么更亮？</h2>
<p>在电阻一定时，电压越大，电流越大，灯通常更亮。欧姆定律把三者定量联系起来：<strong>I=U/R</strong>。</p>
<div class="mini-grid">
<div class="mini-panel"><h3>已有经验</h3><p>电池电压不足灯变暗；电阻丝发热。</p></div>
<div class="mini-panel"><h3>真正卡点</h3><p>公式变形出错；把 R=U/I 理解成“电阻随电压变”。</p></div>
<div class="mini-panel"><h3>本课任务</h3><p>定律表述 → 计算 → 图像。</p></div>
</div></div></section>""",
        "checklist": """<section class="section" id="experiment-checklist" data-tts="experiment-checklist" data-bloom-level="analyze" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">实验检查表</span><h2>探究欧姆定律</h2>
<p><strong>控制变量：</strong>研究 I 与 U：保持 R 不变；研究 I 与 R：保持 U 不变。</p>
<p><strong>测量：</strong>电压表并联，电流表串联。</p>
</div></section>""",
        "pretest": """<section class="section" id="pretest" data-tts="pretest" data-bloom-level="remember" data-scaffold="full" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">前测</span><h2>前测</h2>
<p><strong>欧姆定律的内容是？</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,true,'pretest')">A. 导体中的电流跟导体两端电压成正比，跟导体电阻成反比</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">B. 电流跟电阻成正比</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">C. 电压跟电流成反比</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">D. 电阻跟电压成正比</button>
<div id="pretest-feedback" class="feedback">I=U/R。</div></div></section>""",
        "core": """<section class="section" id="core" data-tts="core" data-bloom-level="understand" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">核心概念</span><h2>I = U / R</h2>
<div class="mini-grid">
<div class="mini-panel"><h3>定律</h3><p>导体中的电流，跟导体两端的电压成正比，跟导体的电阻成反比。</p></div>
<div class="mini-panel"><h3>公式</h3><p>I=U/R，U=IR，R=U/I（计算式）。</p></div>
<div class="mini-panel"><h3>图像</h3><p>R 一定时，I-U 图像是过原点的直线，斜率与 R 有关。</p></div>
</div></div></section>""",
        "deep": """<section class="section" id="deep-understanding" data-tts="deep-understanding"><div class="lesson-panel insight-box"><span class="phase-tag">易混辨析</span><h2>R=U/I 是计算式</h2>
<ul>
<li>可用来求某一状态下的 R。</li>
<li>对欧姆定律适用的导体，R 由本身决定，不随 U、I 正比“变性质”。</li>
</ul>
</div></section>""",
        "worked": """<section class="section" id="worked-example" data-tts="worked-example" data-bloom-level="analyze" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">例题拆解</span><h2>例题</h2>
<p>R=10 Ω，U=6 V，则 I=U/R=0.6 A。</p>
</div></section>""",
        "transfer": """<section class="section" id="transfer-task" data-tts="transfer-task" data-bloom-level="create" data-scaffold="none"><div class="lesson-panel"><span class="phase-tag">迁移任务</span><h2>若电阻变为原来 2 倍、电压不变，电流如何变？</h2>
</div></section>""",
        "lab_html": """<section class="section" id="interactive-lab" data-tts="interactive-lab" data-bloom-level="apply" data-scaffold="partial" data-interactive="ohm-lab"><div class="lesson-panel"><span class="phase-tag">互动实验</span><h2>调 U 与 R，看 I=U/R</h2>
<div class="control-row">
<label>电压 U（V）<input id="ohm-u" type="range" min="1" max="12" value="6"></label>
<label>电阻 R（Ω）<input id="ohm-r" type="range" min="1" max="20" value="10"></label>
</div>
<div class="canvas-wrap"><canvas id="physics-canvas" class="wide-canvas" width="900" height="430"></canvas></div>
<div id="lab-feedback" class="feedback">观察电流随 U、R 变化。</div></div></section>
<script>
(function(){
  const canvas=document.getElementById('physics-canvas'); if(!canvas) return;
  const ctx=canvas.getContext('2d');
  const uEl=document.getElementById('ohm-u'), rEl=document.getElementById('ohm-r');
  const fb=document.getElementById('lab-feedback');
  function draw(){
    const U=+uEl.value, R=+rEl.value, I=U/R;
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='#081426'; ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='#fbbf24'; ctx.font='28px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('I = U / R',80,70);
    ctx.fillStyle='#e2e8f0'; ctx.font='24px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
    ctx.fillText('U='+U+' V，R='+R+' Ω，I='+I.toFixed(2)+' A',80,130);
    ctx.fillStyle='#38bdf8'; ctx.fillRect(200,280, Math.min(500,I*200), 40);
    fb.textContent='电流 '+I.toFixed(2)+' A。U 加倍则 I 加倍；R 加倍则 I 减半。';
  }
  uEl.addEventListener('input',draw); rEl.addEventListener('input',draw); draw();
})();
</script>
<script>const FEEDBACK={pretest:"I=U/R，电流与电压成正比、与电阻成反比。",posttest:"公式变形注意单位统一。"};
function checkAnswer(btn,ok,target){btn.parentElement.querySelectorAll('.quiz-option').forEach(b=>b.classList.remove('correct','wrong'));btn.classList.add(ok?'correct':'wrong');const box=document.getElementById(target+'-feedback');if(box)box.textContent=ok?('✅ '+FEEDBACK[target]):('❌ 再想想：'+FEEDBACK[target]);}</script>
""",
        "external": """<section class="section" id="external-sim" data-tts="external-sim"><div class="lesson-panel"><span class="phase-tag">实验回放</span><h2>欧姆定律三句话</h2>
<ol><li>I=U/R。</li><li>控制变量做实验。</li><li>R=U/I 是计算式。</li></ol>
</div></section>""",
        "posttest": """<section class="section" id="posttest" data-tts="posttest" data-bloom-level="evaluate" data-scaffold="none" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">后测</span><h2>后测</h2>
<p><strong>U=12 V，R=6 Ω，电流为</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,true,'posttest')">A. 2 A</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">B. 72 A</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">C. 0.5 A</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">D. 18 A</button>
<div id="posttest-feedback" class="feedback">I=12/6=2 A。</div></div></section>""",
        "summary": """<section class="section" id="summary" data-tts="summary"><div class="lesson-panel"><span class="phase-tag">一句话带走</span><h2>欧姆定律过关</h2>
<ul><li>会表述定律。</li><li>会算 I、U、R。</li><li>会读 I-U 图像。</li></ul>
</div></section>""",
        "upgrade": """<!-- teachany-upgrade-v2 -->
<!-- upgrade topic: 欧姆定律（去套路） -->
<section class="section teachany-upgrade-block"><h2>📝 中考风格真题</h2>
<div class="tu-q" data-answer="C"><h3>选择题 1</h3><p>由 I=U/R 可知，当 R 一定时</p><div class="tu-opts">
<button type="button" class="tu-opt" data-choice="A" data-diagnosis="应成正比">A. I 与 U 成反比</button>
<button type="button" class="tu-opt" data-choice="B" data-diagnosis="R 一定不是这个">B. I 与 R 成正比</button>
<button type="button" class="tu-opt" data-choice="C" data-diagnosis="R 一定，I 与 U 成正比">C. I 与 U 成正比</button>
<button type="button" class="tu-opt" data-choice="D" data-diagnosis="错误">D. I 与 U 无关</button>
</div><div class="tu-fb" hidden></div></div>
<div class="tu-fill"><h3>填空题 1</h3><p>欧姆定律公式：I = ____。</p>
<details><summary>查看答案</summary><p><strong>答案：</strong>U/R</p></details></div>
</section>
<section class="section teachany-upgrade-block" data-interactive="conceptest"><h2>💡 概念检测</h2>
<p>“由 R=U/I 可知电阻与电压成正比”</p><div class="tu-opts tu-concept">
<button type="button" class="tu-opt" data-choice="A" data-correct="false" data-diagnosis="这是计算式误读">A. 正确</button>
<button type="button" class="tu-opt" data-choice="B" data-correct="true" data-diagnosis="R 由导体决定，R=U/I 用于计算">B. 错误</button>
<button type="button" class="tu-opt" data-choice="C" data-correct="false" data-diagnosis="仍错">C. 只在串联时正确</button>
<button type="button" class="tu-opt" data-choice="D" data-correct="false" data-diagnosis="仍错">D. 只在并联时正确</button>
</div><div class="tu-fb" hidden></div></section>
<section class="section teachany-upgrade-block" data-interactive="inquiry"><h2>🔬 探究记录</h2>
<div class="tu-inquiry">
<label>💡 假设<textarea data-inq="h" placeholder="R一定，U增大 I 是否增大？"></textarea></label>
<label>📊 证据<textarea data-inq="e" placeholder="记录 U、I"></textarea></label>
<label>✅ 结论<textarea data-inq="c" placeholder="验证欧姆定律"></textarea></label>
</div>
<button type="button" class="tu-save">保存探究记录（本机）</button>
<div class="tu-fb" data-inq-fb hidden></div></section>
""",
        "fingerprint": "电压升高，灯为什么更亮",
    },
    "phy-m-series-parallel": {
        "subtitle": "彩灯怎样连接？串联和并联到底差在哪？",
        "figcaption": "串并联：连接特点、电流电压规律、电路识别",
        "anchors": [
            ("怎样识别串联？", "怎样识别串联？"),
            ("并联有何电流电压特点？", "并联有何电流电压特点？"),
            ("断路时现象有何不同？", "断路时现象有何不同？"),
        ],
        "objectives": [
            "能识别串联与并联电路",
            "掌握串并联的电流、电压基本规律",
            "能分析断路时各灯亮灭情况",
        ],
        "story": """<section class="section" id="story" data-tts="story" data-tsh="真实情境"><div class="lesson-panel"><span class="phase-tag">真实情境</span><h2>一串旧彩灯：一盏坏了全都不亮？</h2>
<p>那往往是<strong>串联</strong>：电流只有一条路径。家里电灯大多是<strong>并联</strong>：互不影响。识别串并联，是分析电路的第一步。</p>
<div class="mini-grid">
<div class="mini-panel"><h3>已有经验</h3><p>开关控制多灯、插座互不影响。</p></div>
<div class="mini-panel"><h3>真正卡点</h3><p>看图分不清串并联；规律记串。</p></div>
<div class="mini-panel"><h3>本课任务</h3><p>识别 → 规律 → 故障分析。</p></div>
</div></div></section>""",
        "checklist": """<section class="section" id="experiment-checklist" data-tts="experiment-checklist" data-bloom-level="analyze" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">实验检查表</span><h2>识别串并联</h2>
<p><strong>电流路径：</strong>只有一条→串联；有分支→并联。</p>
<p><strong>元件关系：</strong>首尾相连为串；并列在两点间为并。</p>
</div></section>""",
        "pretest": """<section class="section" id="pretest" data-tts="pretest" data-bloom-level="remember" data-scaffold="full" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">前测</span><h2>前测</h2>
<p><strong>两灯串联，其中一盏灯丝断了，则</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,true,'pretest')">A. 另一盏也不亮</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">B. 另一盏一定更亮</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">C. 另一盏不受影响</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">D. 电源电压变为原来两倍</button>
<div id="pretest-feedback" class="feedback">串联一条路径，一处断路全灭。</div></div></section>""",
        "core": """<section class="section" id="core" data-tts="core" data-bloom-level="understand" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">核心概念</span><h2>串联 vs 并联</h2>
<div class="mini-grid">
<div class="mini-panel"><h3>串联</h3><p>电流处处相等；总电压等于各部分电压之和。</p></div>
<div class="mini-panel"><h3>并联</h3><p>各支路电压相等；干路电流等于支路电流之和。</p></div>
<div class="mini-panel"><h3>识别</h3><p>看有没有分支，电流是否只有一条路。</p></div>
</div></div></section>""",
        "deep": """<section class="section" id="deep-understanding" data-tts="deep-understanding"><div class="lesson-panel insight-box"><span class="phase-tag">易混辨析</span><h2>断路现象对比</h2>
<ul>
<li>串联：一处断开，全部不工作。</li>
<li>并联：一支路断开，其它支路仍可工作。</li>
</ul>
</div></section>""",
        "worked": """<section class="section" id="worked-example" data-tts="worked-example" data-bloom-level="analyze" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">例题拆解</span><h2>例题</h2>
<p>两灯并联，干路电流 0.5 A，一支路 0.2 A，则另一支路 0.3 A。</p>
</div></section>""",
        "transfer": """<section class="section" id="transfer-task" data-tts="transfer-task" data-bloom-level="create" data-scaffold="none"><div class="lesson-panel"><span class="phase-tag">迁移任务</span><h2>设计：两灯并联且各有开关控制</h2>
</div></section>""",
        "lab_html": """<section class="section" id="interactive-lab" data-tts="interactive-lab" data-bloom-level="apply" data-scaffold="partial" data-interactive="sp-lab"><div class="lesson-panel"><span class="phase-tag">互动实验</span><h2>切换串/并联，看电流路径示意</h2>
<div class="control-row">
<label>0串联 / 1并联<input id="sp-mode" type="range" min="0" max="1" step="1" value="0"></label>
</div>
<div class="canvas-wrap"><canvas id="physics-canvas" class="wide-canvas" width="900" height="430"></canvas></div>
<div id="lab-feedback" class="feedback">看路径条数。</div></div></section>
<script>
(function(){
  const canvas=document.getElementById('physics-canvas'); if(!canvas) return;
  const ctx=canvas.getContext('2d');
  const mode=document.getElementById('sp-mode');
  const fb=document.getElementById('lab-feedback');
  function draw(){
    const parallel=+mode.value===1;
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='#081426'; ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.strokeStyle='#38bdf8'; ctx.lineWidth=5;
    if(!parallel){
      ctx.strokeRect(220,180,460,80);
      ctx.fillStyle='#fbbf24'; ctx.font='28px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
      ctx.fillText('串联：一条路径',80,70);
      fb.textContent='串联：电流只有一条路，一处断开全灭。';
    } else {
      ctx.strokeRect(220,120,460,60); ctx.strokeRect(220,240,460,60);
      ctx.beginPath(); ctx.moveTo(220,150); ctx.lineTo(220,270); ctx.moveTo(680,150); ctx.lineTo(680,270); ctx.stroke();
      ctx.fillStyle='#fbbf24'; ctx.font='28px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif';
      ctx.fillText('并联：有分支',80,70);
      fb.textContent='并联：干路分流到支路；一支路断，其它仍可亮。';
    }
  }
  mode.addEventListener('input',draw); draw();
})();
</script>
<script>const FEEDBACK={pretest:"串联一处断路全灭；并联互不影响。",posttest:"串联电流相等、电压相加；并联电压相等、电流相加。"};
function checkAnswer(btn,ok,target){btn.parentElement.querySelectorAll('.quiz-option').forEach(b=>b.classList.remove('correct','wrong'));btn.classList.add(ok?'correct':'wrong');const box=document.getElementById(target+'-feedback');if(box)box.textContent=ok?('✅ '+FEEDBACK[target]):('❌ 再想想：'+FEEDBACK[target]);}</script>
""",
        "external": """<section class="section" id="external-sim" data-tts="external-sim"><div class="lesson-panel"><span class="phase-tag">实验回放</span><h2>串并联三句话</h2>
<ol><li>先识别有没有分支。</li><li>牢记电流电压规律。</li><li>用断路现象验证。</li></ol>
</div></section>""",
        "posttest": """<section class="section" id="posttest" data-tts="posttest" data-bloom-level="evaluate" data-scaffold="none" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">后测</span><h2>后测</h2>
<p><strong>关于并联电路，正确的是？</strong></p>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">A. 干路电流一定小于任一支路电流</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'posttest')">B. 各支路两端电压相等</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">C. 电流处处相等</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'posttest')">D. 总电压等于各支路电压之和</button>
<div id="posttest-feedback" class="feedback">并联电压相等；干路电流为支路之和。</div></div></section>""",
        "summary": """<section class="section" id="summary" data-tts="summary"><div class="lesson-panel"><span class="phase-tag">一句话带走</span><h2>串并联过关</h2>
<ul><li>会识别。</li><li>会背规律。</li><li>会分析断路。</li></ul>
</div></section>""",
        "upgrade": """<!-- teachany-upgrade-v2 -->
<!-- upgrade topic: 串并联（去套路） -->
<section class="section teachany-upgrade-block"><h2>📝 中考风格真题</h2>
<div class="tu-q" data-answer="A"><h3>选择题 1</h3><p>识别串联电路的关键是</p><div class="tu-opts">
<button type="button" class="tu-opt" data-choice="A" data-diagnosis="电流只有一条路径">A. 电流路径只有一条</button>
<button type="button" class="tu-opt" data-choice="B" data-diagnosis="那是并联特征">B. 一定有支路</button>
<button type="button" class="tu-opt" data-choice="C" data-diagnosis="不是">C. 电压处处相等</button>
<button type="button" class="tu-opt" data-choice="D" data-diagnosis="不是充分条件">D. 有开关就是串联</button>
</div><div class="tu-fb" hidden></div></div>
<div class="tu-fill"><h3>填空题 1</h3><p>并联电路干路电流等于各支路电流之 ____。</p>
<details><summary>查看答案</summary><p><strong>答案：</strong>和</p></details></div>
</section>
<section class="section teachany-upgrade-block" data-interactive="conceptest"><h2>💡 概念检测</h2>
<p>“并联时一盏灯坏了，另一盏一定不亮”</p><div class="tu-opts tu-concept">
<button type="button" class="tu-opt" data-choice="A" data-correct="false" data-diagnosis="那是串联">A. 正确</button>
<button type="button" class="tu-opt" data-choice="B" data-correct="true" data-diagnosis="并联支路相对独立">B. 错误，另一盏通常仍可亮</button>
<button type="button" class="tu-opt" data-choice="C" data-correct="false" data-diagnosis="仍错">C. 正确，因为电源坏了</button>
<button type="button" class="tu-opt" data-choice="D" data-correct="false" data-diagnosis="仍错">D. 正确，因为短路</button>
</div><div class="tu-fb" hidden></div></section>
<section class="section teachany-upgrade-block" data-interactive="inquiry"><h2>🔬 探究记录</h2>
<div class="tu-inquiry">
<label>💡 假设<textarea data-inq="h" placeholder="并联两灯是否互不影响？"></textarea></label>
<label>📊 证据<textarea data-inq="e" placeholder="取下一灯观察另一灯"></textarea></label>
<label>✅ 结论<textarea data-inq="c" placeholder="并联特点"></textarea></label>
</div>
<button type="button" class="tu-save">保存探究记录（本机）</button>
<div class="tu-fb" data-inq-fb hidden></div></section>
""",
        "fingerprint": "一串旧彩灯：一盏坏了全都不亮",
    },
}
