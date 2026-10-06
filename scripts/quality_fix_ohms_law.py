#!/usr/bin/env python3
"""Quality pass for phy-m-ohms-law: labeled no-text hero + dense practice, strip junk."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "community/phy-m-ohms-law/index.html"

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

HERO_FIG = """
<section data-scaffold="full" data-bloom-level="apply" class="section" id="hero-infographic" data-tsh="知识结构主图 - 无字生图 + 中文叠标">
  <figure class="ta-standard-figure ta-figure-labeled">
    <div class="ta-figure-wrap">
      <img class="hero-cover-img" src="./assets/phy-m-ohms-law-hero.png" alt="欧姆定律知识结构（无字底图）">
      <div class="ta-figure-tags" aria-hidden="true">
        <span class="ta-fig-tag" style="top:48%;left:50%">欧姆定律 I=U/R</span>
        <span class="ta-fig-tag" style="top:18%;left:18%">伏安法电路</span>
        <span class="ta-fig-tag" style="top:18%;left:82%">I-U 图像</span>
        <span class="ta-fig-tag" style="top:48%;left:12%">控制变量</span>
        <span class="ta-fig-tag" style="top:78%;left:22%">公式变形</span>
        <span class="ta-fig-tag" style="top:78%;left:78%">灯亮暗与电流</span>
        <span class="ta-fig-tag" style="top:52%;left:88%">易错：R≠随U变</span>
      </div>
    </div>
    <figcaption>无字生图 + HTML 中文叠标：实验 · 图像 · 公式 · 易错</figcaption>
  </figure>
</section>
"""

LESSON_HTML = r'''
<style>.lesson-panel{background:linear-gradient(180deg,rgba(20,35,58,.96),rgba(13,27,47,.96));border:1px solid rgba(148,163,184,.18);padding:22px;box-shadow:0 16px 40px rgba(0,0,0,.18)}.mini-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}.mini-panel{background:rgba(15,23,42,.68);border:1px solid rgba(148,163,184,.18);padding:16px}.mini-panel h3{margin:0 0 8px;color:#bae6fd}.quiz-option{display:block;width:100%;margin:8px 0;border:1px solid rgba(56,189,248,.28);background:#0b1628;color:#eef6ff;padding:12px 14px;text-align:left;cursor:pointer}.quiz-option.correct{border-color:#22c55e;background:rgba(34,197,94,.14)}.quiz-option.wrong{border-color:#f97316;background:rgba(249,115,22,.14)}.feedback{min-height:44px;margin-top:10px;padding:10px 12px;background:rgba(56,189,248,.10);color:#dbeafe}.control-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;align-items:end;margin:12px 0}.control-row label{color:#cbd5e1;font-size:14px}.steps{margin:0;padding-left:1.2em;line-height:1.8}.steps li{margin:6px 0}</style>

<section class="slide-page" data-page-index="4" data-page-type="content" data-tsh="真实情境">
<section class="section" id="story" data-tts="story" data-tsh="真实情境"><div class="lesson-panel"><span class="phase-tag">真实情境</span>
<h2>同一盏灯：电压升高为什么更亮？</h2>
<p>课上把小灯泡接到可调电源：电压从 2 V 调到 4 V，灯明显更亮。同学争论：是「电压直接决定亮度」，还是「电压改变电流，电流决定亮度」？</p>
<div class="mini-grid">
<div class="mini-panel"><h3>已有经验</h3><p>电池快没电灯变暗；电阻丝会发热。</p></div>
<div class="mini-panel"><h3>真正卡点</h3><p>背会 I=U/R，却把 R=U/I 读成「电阻跟电压成正比」。</p></div>
<div class="mini-panel"><h3>本课任务</h3><p>定律条件 → 计算与变形 → I-U 图像 → 三级练习。</p></div>
</div></div></section>
</section>

<section class="slide-page" data-page-index="5" data-page-type="content" data-tsh="前测">
<section class="section" id="pretest" data-tts="pretest" data-bloom-level="remember" data-scaffold="full" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">前测 · ConcepTest</span>
<h2>欧姆定律的内容是？</h2>
<p><strong>在导体电阻一定时</strong>，下列说法正确的是：</p>
<button class="quiz-option" onclick="checkAnswer(this,true,'pretest')">A. 电流跟两端电压成正比，跟电阻成反比</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">B. 电流跟电阻成正比</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">C. 电压跟电流成反比</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'pretest')">D. 电阻跟电压成正比</button>
<div id="pretest-feedback" class="feedback">先选再看解析。</div>
</div></section>
</section>

<section class="slide-page" data-page-index="6" data-page-type="content" data-tsh="核心概念">
<section class="section" id="core" data-tts="core" data-bloom-level="understand" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">核心概念</span>
<h2>I = U / R（先讲清条件）</h2>
<div class="mini-grid">
<div class="mini-panel"><h3>定律表述</h3><p>导体中的电流，跟导体两端的电压成正比，跟导体的电阻成反比。</p></div>
<div class="mini-panel"><h3>适用条件</h3><p>同一导体、同一状态（温度等基本不变）；金属导体等线性元件。二极管等非线性元件不能直接套。</p></div>
<div class="mini-panel"><h3>三个公式</h3><p>I=U/R（定律式）；U=IR；R=U/I（某一状态下的<strong>计算式</strong>）。</p></div>
</div>
<figure class="ta-standard-figure ta-figure-labeled" style="margin-top:16px">
  <div class="ta-figure-wrap">
    <img src="./assets/phy-m-ohms-law-section1.png" alt="伏安法电路示意（无字）">
    <div class="ta-figure-tags" aria-hidden="true">
      <span class="ta-fig-tag" style="top:22%;left:30%">电源</span>
      <span class="ta-fig-tag" style="top:55%;left:22%">电流表（串联）</span>
      <span class="ta-fig-tag" style="top:40%;left:72%">电压表（并联）</span>
      <span class="ta-fig-tag" style="top:70%;left:55%">待测电阻</span>
    </div>
  </div>
  <figcaption>实验关键：电流表串联、电压表并联；研究 I-U 时保持 R 不变。</figcaption>
</figure>
</div></section>
</section>

<section class="slide-page" data-page-index="7" data-page-type="content" data-tsh="易混辨析">
<section class="section" id="deep-understanding" data-tts="deep-understanding"><div class="lesson-panel insight-box"><span class="phase-tag">易混辨析</span>
<h2>R=U/I 是计算式，不是「电阻决定律」</h2>
<ul class="steps">
<li>可用某一组 U、I <strong>算出</strong>当时的电阻值。</li>
<li>对欧姆定律适用的导体，R 主要由材料、长度、横截面积、温度决定，<strong>不</strong>因 U 变大就「性质上变大」。</li>
<li>中考高频陷阱：看见 R=U/I 就说「R 与 U 成正比」——错。</li>
</ul>
<figure class="ta-standard-figure ta-figure-labeled" style="margin-top:14px">
  <div class="ta-figure-wrap">
    <img src="./assets/phy-m-ohms-law-section2.png" alt="I-U 图像示意（无字）">
    <div class="ta-figure-tags" aria-hidden="true">
      <span class="ta-fig-tag" style="top:18%;left:55%">I（纵轴）</span>
      <span class="ta-fig-tag" style="top:85%;left:70%">U（横轴）</span>
      <span class="ta-fig-tag" style="top:45%;left:58%">过原点直线</span>
      <span class="ta-fig-tag" style="top:60%;left:30%">斜率与 1/R 有关</span>
    </div>
  </div>
  <figcaption>R 一定时，I-U 图像是过原点的直线；斜率越大，电阻越小。</figcaption>
</figure>
</div></section>
</section>

<section class="slide-page" data-page-index="8" data-page-type="content" data-tsh="例题拆解">
<section class="section" id="worked-example" data-tts="worked-example" data-bloom-level="analyze" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">例题拆解</span>
<h2>例：R=10 Ω，U=6 V，求 I</h2>
<ol class="steps">
<li>确认同一导体、可用欧姆定律：I=U/R。</li>
<li>代入：I=6/10=0.6 A。</li>
<li>单位检查：V、Ω → A。</li>
<li>追问：若 R 加倍、U 不变，I 变为原来的 1/2。</li>
</ol>
</div></section>
</section>

<section class="slide-page" data-page-index="9" data-page-type="content" data-tsh="互动实验">
<section class="section" id="interactive-lab" data-tts="interactive-lab" data-bloom-level="apply" data-scaffold="partial" data-interactive="ohm-lab"><div class="lesson-panel"><span class="phase-tag">互动实验</span>
<h2>调 U 与 R，看 I=U/R</h2>
<div class="control-row">
<label>电压 U（V）<input id="ohm-u" type="range" min="1" max="12" value="6"></label>
<label>电阻 R（Ω）<input id="ohm-r" type="range" min="1" max="20" value="10"></label>
</div>
<div class="canvas-wrap"><canvas id="physics-canvas" class="wide-canvas" width="900" height="430"></canvas></div>
<div id="lab-feedback" class="feedback">拖动滑块，观察 I 的变化规律。</div>
</div></section>
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
    // simple I-U sketch
    ctx.strokeStyle='#64748b'; ctx.beginPath(); ctx.moveTo(80,380); ctx.lineTo(520,380); ctx.moveTo(80,380); ctx.lineTo(80,180); ctx.stroke();
    const x2=80+Math.min(400,U*30), y2=380-Math.min(180,I*80);
    ctx.strokeStyle='#38bdf8'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(80,380); ctx.lineTo(x2,y2); ctx.stroke();
    ctx.fillStyle='#38bdf8'; ctx.fillRect(560,280, Math.min(280,I*120), 40);
    fb.textContent='电流 '+I.toFixed(2)+' A。保持 R：U 加倍 → I 加倍；保持 U：R 加倍 → I 减半。';
  }
  uEl.addEventListener('input',draw); rEl.addEventListener('input',draw); draw();
})();
</script>
</section>

<section class="slide-page" data-page-index="10" data-page-type="content" data-tsh="L1 基础巩固">
<section class="section" id="practice-l1" data-tts="practice-l1" data-bloom-level="remember"><div class="lesson-panel"><span class="phase-tag">练习 L1 · 基础巩固</span>
<h2>先过关再进阶</h2>
<div class="practice-block">
<h3>1. 单位与公式</h3>
<p>电阻 5 Ω、电压 10 V，电流是？</p>
<button class="quiz-option" onclick="checkAnswer(this,false,'l1a')">A. 50 A</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'l1a')">B. 2 A</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'l1a')">C. 0.5 A</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'l1a')">D. 15 A</button>
<div id="l1a-feedback" class="feedback"></div>
</div>
<div class="practice-block">
<h3>2. 图像判断</h3>
<p>R 一定时，正确的 I-U 图像特征是？</p>
<button class="quiz-option" onclick="checkAnswer(this,true,'l1b')">A. 过原点的直线</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'l1b')">B. 不过原点的水平线</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'l1b')">C. 抛物线</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'l1b')">D. 与 U 轴平行</button>
<div id="l1b-feedback" class="feedback"></div>
</div>
</div></section>
</section>

<section class="slide-page" data-page-index="11" data-page-type="content" data-tsh="L2 能力应用">
<section class="section" id="practice-l2" data-tts="practice-l2" data-bloom-level="apply"><div class="lesson-panel"><span class="phase-tag">练习 L2 · 能力应用</span>
<h2>含错因诊断</h2>
<div class="practice-block">
<h3>3. 变形计算</h3>
<p>电流 0.5 A、电阻 40 Ω，两端电压是？</p>
<button class="quiz-option" onclick="checkAnswer(this,false,'l2a')">A. 80 V（误用 U=I/R）</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'l2a')">B. 20 V（U=IR）</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'l2a')">C. 0.0125 V（误用 I/R）</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'l2a')">D. 40.5 V（胡加）</button>
<div id="l2a-feedback" class="feedback"></div>
</div>
<div class="practice-block">
<h3>4. 概念陷阱</h3>
<p>「由 R=U/I 可知，电阻与电压成正比」这句话？</p>
<button class="quiz-option" onclick="checkAnswer(this,false,'l2b')">A. 正确</button>
<button class="quiz-option" onclick="checkAnswer(this,true,'l2b')">B. 错误：R=U/I 是计算式</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'l2b')">C. 只在串联时正确</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'l2b')">D. 只在并联时正确</button>
<div id="l2b-feedback" class="feedback"></div>
</div>
</div></section>
</section>

<section class="slide-page" data-page-index="12" data-page-type="content" data-tsh="L3 迁移挑战">
<section class="section" id="practice-l3" data-tts="practice-l3" data-bloom-level="create"><div class="lesson-panel"><span class="phase-tag">练习 L3 · 迁移</span>
<h2>设计与解释</h2>
<div class="practice-block">
<h3>5. 控制变量实验</h3>
<p>要探究「电流与电阻的关系」，应保持什么不变？</p>
<button class="quiz-option" onclick="checkAnswer(this,true,'l3a')">A. 导体两端电压不变，换不同电阻测电流</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'l3a')">B. 电阻不变，只改变电压</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'l3a')">C. 电压和电阻同时改变</button>
<button class="quiz-option" onclick="checkAnswer(this,false,'l3a')">D. 不需要控制变量</button>
<div id="l3a-feedback" class="feedback"></div>
</div>
<div class="practice-block">
<h3>6. 开放产出</h3>
<p>用三句话解释：为什么「电压升高灯更亮」要用欧姆定律，而不是只说「电压大就亮」？</p>
<textarea id="l3-open" rows="4" style="width:100%;margin-top:8px;padding:10px;border-radius:8px;border:1px solid rgba(148,163,184,.3);background:#0b1628;color:#e2e8f0" placeholder="提示：电压→电流→亮度；R 近似一定…"></textarea>
<button type="button" class="quiz-option" style="margin-top:10px;text-align:center" onclick="showOpenRubric()">对照量规自检</button>
<div id="l3-open-feedback" class="feedback" hidden></div>
</div>
</div></section>
</section>

<section class="slide-page" data-page-index="13" data-page-type="content" data-tsh="小结">
<section class="section" id="summary" data-tts="summary">
  <div class="lesson-panel">
    <span class="phase-tag">小结清单</span>
    <h2>这节课你应能做到</h2>
    <div class="checklist" id="summary-checklist">
      <label><input type="checkbox" class="recap-check"><span>正确表述欧姆定律，并说出适用条件</span></label>
      <label><input type="checkbox" class="recap-check"><span>会用 I=U/R、U=IR、R=U/I，且不误读计算式</span></label>
      <label><input type="checkbox" class="recap-check"><span>能说明 R 一定时 I-U 图像过原点</span></label>
      <label><input type="checkbox" class="recap-check"><span>能设计「研究 I 与 R」时的控制变量方案</span></label>
    </div>
    <p id="summary-feedback" class="feedback" style="margin-top:12px">勾选你已掌握的条目。</p>
  </div>
</section>
</section>

<script>
const FEEDBACK={
  pretest:"I=U/R：电流与电压成正比、与电阻成反比（R 一定时看 U；U 一定时看 R）。",
  l1a:"I=U/R=10/5=2 A。常见错：U×R 或 R/U。",
  l1b:"正比关系 → 过原点直线；斜率与 1/R 相关。",
  l2a:"U=IR=0.5×40=20 V。选项表述以对勾为准：正确答案是 20 V（U=IR）。",
  l2b:"R=U/I 用来算某一状态下的 R，不能推出「R 与 U 成正比」。",
  l3a:"研究 I 与 R：保持 U 不变，改变 R，测 I。"
};
function checkAnswer(btn,ok,target){
  const root=btn.closest('.practice-block, .lesson-panel')||btn.parentElement;
  root.querySelectorAll('.quiz-option').forEach(b=>b.classList.remove('correct','wrong'));
  btn.classList.add(ok?'correct':'wrong');
  const box=document.getElementById(target+'-feedback');
  if(box) box.textContent=(ok?'✅ ':'❌ ')+(FEEDBACK[target]||'');
}
function showOpenRubric(){
  const box=document.getElementById('l3-open-feedback');
  box.hidden=false;
  box.innerHTML='量规自检：①是否提到「电压改变 → 电流改变」；②是否点明 R 近似不变；③是否落到「电流影响灯丝发热/亮度」。缺一条就补一句。';
}
</script>
'''


def main() -> None:
    html = INDEX.read_text(encoding="utf-8")

    if 'id="ta-labeled-figure-css"' not in html:
        html = html.replace("</head>", LABEL_CSS + "\n</head>", 1)

    # Replace hero-infographic block
    html = re.sub(
        r'<section[^>]*id="hero-infographic"[\s\S]*?</section>\s*</section>',
        HERO_FIG + "\n</section>",
        html,
        count=1,
    )

    # Replace from lesson style/story through old feedback script, before empty KG slides
    pattern = re.compile(
        r'<style>\.lesson-panel\{[\s\S]*?</script>\s*\n\s*\n\s*<section class="slide-page" data-page-index="20"',
        re.M,
    )
    if not pattern.search(html):
        # fallback: from story slide to page 20
        pattern = re.compile(
            r'<section class="slide-page" data-page-index="4"[\s\S]*?<section class="slide-page" data-page-index="20"',
            re.M,
        )
        repl = LESSON_HTML + '\n<section class="slide-page" data-page-index="20"'
    else:
        repl = LESSON_HTML + '\n<section class="slide-page" data-page-index="20"'

    html2, n = pattern.subn(repl, html, count=1)
    if n != 1:
        raise SystemExit(f"lesson replace failed n={n}")
    html = html2

    # Strip junk enhanced + upgrade-v2 blocks; keep knowledge-graph section
    html = re.sub(
        r"<!-- teachany-enhanced -->[\s\S]*?(?=<section class=\"section\" id=\"knowledge-graph\")",
        "",
        html,
        count=1,
    )

    # Fix broken L2 option wording (B should be clean)
    html = html.replace(
        'B. 20 V？不对——应是 U=IR=20 V。等等，B 才对：20 V',
        "B. 20 V（U=IR）",
    )
    # remove wrong distractor that said 20V incorrectly
    html = html.replace(
        '<button class="quiz-option" onclick="checkAnswer(this,false,\'l2a\')">A. 20 V（用了 I=U/R 反着代）</button>\n',
        '<button class="quiz-option" onclick="checkAnswer(this,false,\'l2a\')">A. 80 V（误用 U=I/R）</button>\n',
    )

    # Fix problem anchor to be topic-specific
    html = re.sub(
        r'(<div class="grid" id="problem-anchor-choices">)[\s\S]*?(</div>)',
        r"""\1
<button class="choice" data-anchor-choice="怎样用实验验证 I 与 U、R 的关系？">怎样用实验验证 I 与 U、R 的关系？</button>
<button class="choice" data-anchor-choice="为什么 R=U/I 不能说成电阻跟电压成正比？">为什么 R=U/I 不能说成电阻跟电压成正比？</button>
<button class="choice" data-anchor-choice="I-U 图像怎样读出电阻大小？">I-U 图像怎样读出电阻大小？</button>
\2""",
        html,
        count=1,
    )

    INDEX.write_text(html, encoding="utf-8")
    print("OK", INDEX)


if __name__ == "__main__":
    main()
