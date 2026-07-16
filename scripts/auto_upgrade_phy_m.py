#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""phy-m 全面质量升级 · 自动多轮

每轮处理 --limit 门：无字 Agnes 生图 → 专属正文(L1/L2/L3) → PhET → 去 junk → QC。
状态：data/auto-upgrade-state.json
进度：data/upgrade-phy-m-remaining.txt / qc-upgrade.html

用法：
  python3 scripts/auto_upgrade_phy_m.py --limit 3          # 下一轮 3 门
  python3 scripts/auto_upgrade_phy_m.py --batch B          # 指定批次
  python3 scripts/auto_upgrade_phy_m.py --cid phy-m-xxx    # 单课
  python3 scripts/auto_upgrade_phy_m.py --status           # 看进度
  python3 scripts/auto_upgrade_phy_m.py --skip-images      # 仅改 HTML
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
CATALOG = ROOT / "data" / "phy-m-upgrade-catalog.json"
STATE = ROOT / "data" / "auto-upgrade-state.json"
REMAINING = ROOT / "data" / "upgrade-phy-m-remaining.txt"
QC = ROOT / "qc-upgrade.html"
AGNES = Path.home() / ".claude/skills/teachany/scripts/agnes-image-gen.py"
NO_TEXT = (
    ", absolutely no text, no letters, no numbers, no words, no Chinese characters, "
    "no labels, no signage, no captions, no watermarks in the image, illustration only"
)

LABEL_CSS = """
<style id="ta-labeled-figure-css">
.ta-figure-labeled{position:relative}
.ta-figure-wrap{position:relative}
.ta-figure-labeled img{width:100%;border-radius:12px;display:block}
.ta-figure-tags{position:absolute;inset:0;pointer-events:none}
.ta-fig-tag{position:absolute;transform:translate(-50%,-50%);background:rgba(15,23,42,.88);color:#fff;font-size:13px;font-weight:700;padding:5px 11px;border-radius:8px;white-space:nowrap;box-shadow:0 4px 12px rgba(0,0,0,.25);border:1px solid rgba(56,189,248,.35)}
.practice-block{margin:14px 0;padding:14px;border:1px solid rgba(148,163,184,.22);border-radius:12px;background:rgba(15,23,42,.45)}
.practice-block h3{margin:0 0 8px;color:#bae6fd;font-size:16px}
input[type="checkbox"],input[type="radio"]{width:18px!important;height:18px!important;min-height:18px!important;min-width:18px!important;margin:2px 0 0;padding:0;flex:0 0 18px;accent-color:var(--brand,#38bdf8);border:none;background:transparent}
.checklist{display:flex;flex-direction:column;gap:10px;margin-top:12px}
.checklist label{display:flex;gap:12px;align-items:flex-start;margin:0;padding:12px 14px;border:1px solid rgba(148,163,184,.22);border-radius:12px;background:rgba(2,6,23,.45);color:var(--text,#eef6ff);line-height:1.55;cursor:pointer}
.checklist label span{flex:1;min-width:0}
.control-row input[type="range"]{width:100%;min-height:28px;padding:0;background:transparent;border:none}
.iframe-wrap{position:relative;width:100%;padding-top:62.5%;overflow:hidden;background:#0f172a;border-radius:12px;border:1px solid rgba(148,163,184,.18)}
.iframe-wrap iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.lesson-panel{background:linear-gradient(180deg,rgba(20,35,58,.96),rgba(13,27,47,.96));border:1px solid rgba(148,163,184,.18);padding:22px;box-shadow:0 16px 40px rgba(0,0,0,.18)}
.mini-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}
.mini-panel{background:rgba(15,23,42,.68);border:1px solid rgba(148,163,184,.18);padding:16px}
.mini-panel h3{margin:0 0 8px;color:#bae6fd}
.quiz-option{display:block;width:100%;margin:8px 0;border:1px solid rgba(56,189,248,.28);background:#0b1628;color:#eef6ff;padding:12px 14px;text-align:left;cursor:pointer}
.quiz-option.correct{border-color:#22c55e;background:rgba(34,197,94,.14)}
.quiz-option.wrong{border-color:#f97316;background:rgba(249,115,22,.14)}
.feedback{min-height:44px;margin-top:10px;padding:10px 12px;background:rgba(56,189,248,.10);color:#dbeafe}
.control-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;align-items:end;margin:12px 0}
.control-row label{color:#cbd5e1;font-size:14px}
.steps{margin:0;padding-left:1.2em;line-height:1.8}.steps li{margin:6px 0}
</style>
"""


def load_catalog() -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"done": [], "failed": [], "rounds": [], "updated_at": None}


def save_state(state: dict) -> None:
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def tags_html(items: list) -> str:
    out = []
    for it in items:
        if isinstance(it, (list, tuple)) and len(it) >= 3:
            txt, top, left = it[0], it[1], it[2]
        elif isinstance(it, dict):
            txt, top, left = it["t"], it["top"], it["left"]
        else:
            continue
        out.append(f'<span class="ta-fig-tag" style="top:{top};left:{left}">{txt}</span>')
    return "".join(out)


def quiz_html(qid: str, title: str, stem: str, opts: list) -> str:
    btns = []
    for o in opts:
        text, ok = o[0], o[1]
        btns.append(
            f'<button class="quiz-option" onclick="checkAnswer(this,{"true" if ok else "false"},\'{qid}\')">{text}</button>'
        )
    return (
        f'<div class="practice-block"><h3>{title}</h3><p>{stem}</p>\n'
        + "\n".join(btns)
        + f'\n<div id="{qid}-feedback" class="feedback"></div></div>'
    )


def default_lab(cid: str, center: str) -> str:
    return f'''<section class="section" id="interactive-lab" data-tts="interactive-lab" data-interactive="generic-lab"><div class="lesson-panel"><span class="phase-tag">互动实验</span>
<h2>调参数，观察与「{center}」相关的变化</h2>
<div class="control-row">
<label>变量 A<input id="lab-a" type="range" min="1" max="10" value="5"></label>
<label>变量 B<input id="lab-b" type="range" min="1" max="10" value="3"></label>
</div>
<div class="canvas-wrap"><canvas id="physics-canvas" class="wide-canvas" width="900" height="300"></canvas></div>
<div id="lab-feedback" class="feedback">结合下方 PhET 做完整探究。</div></div></section>
<script>
(function(){{
  const c=document.getElementById('physics-canvas'); if(!c) return;
  const ctx=c.getContext('2d');
  const a=document.getElementById('lab-a'), b=document.getElementById('lab-b'), fb=document.getElementById('lab-feedback');
  function draw(){{
    const A=+a.value,B=+b.value;
    ctx.clearRect(0,0,c.width,c.height); ctx.fillStyle='#081426'; ctx.fillRect(0,0,c.width,c.height);
    ctx.fillStyle='#fbbf24'; ctx.font='24px PingFang SC,sans-serif'; ctx.fillText('{center} · 本地示意',60,50);
    ctx.fillStyle='#38bdf8'; ctx.fillRect(80,160,A*40,40); ctx.fillStyle='#a78bfa'; ctx.fillRect(80,220,B*40,40);
    fb.textContent='A='+A+'，B='+B+'。完整操作请用下方 PhET。';
  }}
  a.addEventListener('input',draw); b.addEventListener('input',draw); draw();
}})();
</script>'''


def phet_block(meta: dict) -> str:
    slug = meta["slug"]
    url = f"https://phet.colorado.edu/sims/html/{slug}/latest/{slug}_zh_CN.html"
    return f'''
<section class="slide-page" data-page-index="9b" data-page-type="content" data-tsh="PhET 网络仿真">
<section class="section" id="phet-lab" data-tts="phet-lab" data-bloom-level="apply" data-scaffold="partial" data-interactive="phet">
  <div class="lesson-panel">
    <span class="phase-tag">网络仿真 · PhET</span>
    <h2>{meta.get("title", "PhET 仿真")}</h2>
    <div class="iframe-wrap">
      <iframe src="{url}" title="{meta.get("title","PhET")}" allowfullscreen loading="lazy"
        sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
        referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
    <p class="feedback" style="margin-top:12px">💡 {meta.get("hint", "按提示操作，记录现象与结论。")}</p>
    <p style="font-size:12px;color:#64748b;margin:8px 0 0">外链：<a href="{url}" target="_blank" rel="noopener">{url}</a></p>
  </div>
</section>
</section>
'''


def build_lesson(cfg: dict) -> str:
    cid = cfg["id"]
    center = cfg["center"]
    lab = cfg.get("lab_html") or default_lab(cid, center)
    fb = json.dumps(cfg["feedback"], ensure_ascii=False)
    summary = cfg["summary"]
    n = len(summary)
    labels = "\n".join(
        f'      <label><input type="checkbox" class="recap-check"><span>{t}</span></label>' for t in summary
    )
    core = "".join(
        f'<div class="mini-panel"><h3>{p["h"]}</h3><p>{p["p"]}</p></div>' for p in cfg["core"]
    )
    deep = "".join(f"<li>{x}</li>" for x in cfg["deep"])
    qs = cfg["quizzes"]
    return f'''
<!-- teachany-quality-v3 fingerprint={cfg.get("fingerprint", center)} -->
{LABEL_CSS}
<section class="slide-page" data-page-index="4" data-page-type="content" data-tsh="真实情境">
<section class="section" id="story" data-tts="story"><div class="lesson-panel"><span class="phase-tag">真实情境</span>
<h2>{cfg["story_h2"]}</h2>
<p>{cfg["story_p"]}</p>
<div class="mini-grid">
<div class="mini-panel"><h3>已有经验</h3><p>{cfg["exp"]}</p></div>
<div class="mini-panel"><h3>真正卡点</h3><p>{cfg["trap"]}</p></div>
<div class="mini-panel"><h3>本课任务</h3><p>{cfg["task"]}</p></div>
</div></div></section></section>

<section class="slide-page" data-page-index="5" data-page-type="content" data-tsh="前测">
<section class="section" id="pretest" data-tts="pretest" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">前测 · ConcepTest</span>
<h2>{qs["pretest"]["title"]}</h2>
<p>{qs["pretest"]["stem"]}</p>
{"".join(f'<button class="quiz-option" onclick="checkAnswer(this,{"true" if o[1] else "false"},\'pretest\')">{o[0]}</button>' for o in qs["pretest"]["opts"])}
<div id="pretest-feedback" class="feedback">先选再看解析。</div>
</div></section></section>

<section class="slide-page" data-page-index="6" data-page-type="content" data-tsh="核心">
<section class="section" id="core" data-tts="core"><div class="lesson-panel"><span class="phase-tag">核心概念</span>
<h2>{cfg.get("core_title", center)}</h2>
<div class="mini-grid">{core}</div>
<figure class="ta-standard-figure ta-figure-labeled" style="margin-top:16px">
  <div class="ta-figure-wrap">
    <img src="./assets/{cid}-section1.png" alt="{center}示意（无字）">
    <div class="ta-figure-tags" aria-hidden="true">{tags_html(cfg.get("section1_tags", []))}</div>
  </div>
  <figcaption>{cfg.get("section1_caption", "核心示意（无字底图 + 中文叠标）")}</figcaption>
</figure>
</div></section></section>

<section class="slide-page" data-page-index="7" data-page-type="content" data-tsh="易混">
<section class="section" id="deep-understanding" data-tts="deep-understanding"><div class="lesson-panel"><span class="phase-tag">易混辨析</span>
<h2>{cfg.get("deep_title", "易错点")}</h2>
<ul class="steps">{deep}</ul>
<figure class="ta-standard-figure ta-figure-labeled" style="margin-top:14px">
  <div class="ta-figure-wrap">
    <img src="./assets/{cid}-section2.png" alt="{center}对比（无字）">
    <div class="ta-figure-tags" aria-hidden="true">{tags_html(cfg.get("section2_tags", []))}</div>
  </div>
  <figcaption>{cfg.get("section2_caption", "对比与迁移（无字底图 + 中文叠标）")}</figcaption>
</figure>
</div></section></section>

<section class="slide-page" data-page-index="8" data-page-type="content" data-tsh="例题">
<section class="section" id="worked-example" data-tts="worked-example"><div class="lesson-panel"><span class="phase-tag">例题拆解</span>
<h2>{cfg["worked_h2"]}</h2>
<ol class="steps">{"".join(f"<li>{s}</li>" for s in cfg["worked_steps"])}</ol>
</div></section></section>

<section class="slide-page" data-page-index="9" data-page-type="content" data-tsh="互动">{lab}</section>
{phet_block(cfg["phet"])}

<section class="slide-page" data-page-index="10" data-page-type="content" data-tsh="L1">
<section class="section" id="practice-l1" data-tts="practice-l1"><div class="lesson-panel"><span class="phase-tag">练习 L1 · 基础巩固</span>
<h2>先过关</h2>
{quiz_html("l1a", qs["l1a"]["title"], qs["l1a"]["stem"], qs["l1a"]["opts"])}
{quiz_html("l1b", qs["l1b"]["title"], qs["l1b"]["stem"], qs["l1b"]["opts"])}
</div></section></section>

<section class="slide-page" data-page-index="11" data-page-type="content" data-tsh="L2">
<section class="section" id="practice-l2" data-tts="practice-l2"><div class="lesson-panel"><span class="phase-tag">练习 L2 · 能力应用</span>
<h2>含错因</h2>
{quiz_html("l2a", qs["l2a"]["title"], qs["l2a"]["stem"], qs["l2a"]["opts"])}
{quiz_html("l2b", qs["l2b"]["title"], qs["l2b"]["stem"], qs["l2b"]["opts"])}
</div></section></section>

<section class="slide-page" data-page-index="12" data-page-type="content" data-tsh="L3">
<section class="section" id="practice-l3" data-tts="practice-l3"><div class="lesson-panel"><span class="phase-tag">练习 L3 · 迁移</span>
<h2>迁移与产出</h2>
{quiz_html("l3a", qs["l3a"]["title"], qs["l3a"]["stem"], qs["l3a"]["opts"])}
<div class="practice-block"><h3>开放产出</h3>
<p>{cfg.get("open_prompt", "用三句话总结本课最关键的一条规律，并举一个生活例子。")}</p>
<textarea id="l3-open" rows="3" style="width:100%;margin-top:8px;padding:10px;border-radius:8px;border:1px solid rgba(148,163,184,.3);background:#0b1628;color:#e2e8f0"></textarea>
<button type="button" class="quiz-option" style="margin-top:10px;text-align:center" onclick="showOpenRubric()">对照量规自检</button>
<div id="l3-open-feedback" class="feedback" hidden></div></div>
</div></section></section>

<section class="slide-page" data-page-index="13" data-page-type="content" data-tsh="小结">
<section class="section" id="summary" data-tts="summary"><div class="lesson-panel">
<span class="phase-tag">小结清单</span>
<h2>这节课你应能做到</h2>
<div class="checklist" id="summary-checklist">
{labels}
</div>
<p id="summary-feedback" class="feedback" style="margin-top:12px">勾选你已掌握的条目。</p>
</div></section></section>
<script>
const FEEDBACK = {fb};
function checkAnswer(btn,ok,target){{
  const root=btn.closest('.practice-block, .lesson-panel')||btn.parentElement;
  root.querySelectorAll('.quiz-option').forEach(b=>b.classList.remove('correct','wrong'));
  btn.classList.add(ok?'correct':'wrong');
  const box=document.getElementById(target+'-feedback');
  if(box) box.textContent=(ok?'✅ ':'❌ ')+(FEEDBACK[target]||'');
}}
function showOpenRubric(){{
  const box=document.getElementById('l3-open-feedback');
  if(!box) return; box.hidden=false; box.innerHTML=FEEDBACK.open||'对照量规补全要点。';
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


def gen_images(cfg: dict, force: bool = False) -> str:
    cid = cfg["id"]
    assets = COMMUNITY / cid / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    agnes = cfg.get("agnes") or {}
    prompts = {
        "hero": agnes.get(
            "hero",
            f"Educational physics concept map about {cfg['center']}, dark navy flat vector, central hub connected to six illustrated panels, science lab mood",
        ),
        "section1": agnes.get(
            "section1",
            f"Middle school physics illustration for {cfg['center']}, dark educational flat style, concrete lab objects",
        ),
        "section2": agnes.get(
            "section2",
            f"Educational contrast diagram for {cfg['center']}, dark navy cyan amber flat vector",
        ),
    }
    results = []
    for slot, prompt in prompts.items():
        out = assets / f"{cid}-{slot}.png"
        if out.exists() and out.stat().st_size > 40000 and not force:
            results.append(f"{slot}:skip")
            continue
        if not AGNES.exists():
            return "agnes-missing"
        cmd = [
            sys.executable,
            str(AGNES),
            "--course-id",
            f"{cid}-r2",
            "--slot",
            slot,
            "--size",
            "1280x768",
            "--prompt",
            prompt + NO_TEXT,
            "--out",
            str(out),
        ]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            ok = out.exists() and out.stat().st_size > 20000
            results.append(f"{slot}:{'ok' if ok else 'fail'}")
            if not ok:
                results.append((r.stdout or r.stderr)[-180:])
        except Exception as e:
            results.append(f"{slot}:err:{e}")
        time.sleep(6)
    return ",".join(results)


def apply_html(cfg: dict) -> str:
    cid = cfg["id"]
    path = COMMUNITY / cid / "index.html"
    if not path.exists():
        return "no-index"
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

    # hero
    hero_tags = tags_html(cfg.get("hero_tags", []))
    hero = f'''
<section data-scaffold="full" data-bloom-level="apply" class="section" id="hero-infographic" data-tsh="知识结构主图">
  <figure class="ta-standard-figure ta-figure-labeled">
    <div class="ta-figure-wrap">
      <img class="hero-cover-img" src="./assets/{cid}-hero.png" alt="{cfg["center"]}知识结构（无字）">
      <div class="ta-figure-tags" aria-hidden="true">
        <span class="ta-fig-tag" style="top:48%;left:50%">{cfg["center"]}</span>
        {hero_tags}
      </div>
    </div>
    <figcaption>无字生图 + HTML 中文叠标</figcaption>
  </figure>
</section>
'''
    if 'id="hero-infographic"' in html:
        html = re.sub(
            r'<section[^>]*id="hero-infographic"[\s\S]*?</section>\s*</section>',
            hero + "\n</section>",
            html,
            count=1,
        )
    else:
        # insert after first hero header slide if possible
        html = html.replace("</header>\n</section>", "</header>\n</section>\n<section class=\"slide-page\" data-page-index=\"1\" data-page-type=\"content\">" + hero + "</section>", 1)

    # anchors / objectives
    if cfg.get("anchors") and 'id="problem-anchor-choices"' in html:
        choices = "\n".join(
            f'<button class="choice" data-anchor-choice="{a}">{a}</button>' for a in cfg["anchors"]
        )
        html = re.sub(
            r'(<div class="grid" id="problem-anchor-choices">)[\s\S]*?(</div>)',
            rf"\1\n{choices}\n\2",
            html,
            count=1,
        )
    if cfg.get("objectives") and 'class="objectives"' in html:
        objs = "\n".join(f"<li>{o}</li>" for o in cfg["objectives"])
        html = re.sub(
            r'(<ul class="objectives">)[\s\S]*?(</ul>)',
            rf"\1\n{objs}\n\2",
            html,
            count=1,
        )

    lesson = build_lesson(cfg)
    pattern = re.compile(
        r'(?:<!-- teachany-quality-v3|<style id="ta-labeled-figure-css">|<style>\.lesson-panel\{|<section class="slide-page" data-page-index="4")[\s\S]*?'
        r'<section class="slide-page" data-page-index="20"',
        re.M,
    )
    html2, n = pattern.subn(lesson + '\n<section class="slide-page" data-page-index="20"', html, count=1)
    if n != 1:
        # broader fallback: from story to page 20
        pattern2 = re.compile(
            r'<section class="slide-page" data-page-index="4"[\s\S]*?<section class="slide-page" data-page-index="20"',
            re.M,
        )
        html2, n = pattern2.subn(lesson + '\n<section class="slide-page" data-page-index="20"', html, count=1)
    if n != 1:
        return f"lesson-replace-fail:{n}"
    html = html2

    # strip junk
    for pat in [
        r"<!-- teachany-enhanced -->[\s\S]*?(?=<section class=\"section\" id=\"knowledge-graph\"|<section class=\"slide-page\" data-page-index=\"20\")",
        r"<!-- teachany-upgrade-v2 -->[\s\S]*?(?=<section class=\"section\" id=\"knowledge-graph\")",
        r"<!-- upgrade topic:[\s\S]*?(?=<section class=\"section\" id=\"knowledge-graph\")",
    ]:
        html = re.sub(pat, "", html, count=1)

    # fix nav/body lightly
    html = re.sub(
        r"</head>\s*<nav[\s\S]*?</nav>\s*<body[^>]*>",
        '</head>\n<body class="teachany-middle">\n',
        html,
        count=1,
    )

    path.write_text(html, encoding="utf-8")
    return "ok"


def qc_course(cid: str) -> dict:
    path = COMMUNITY / cid / "index.html"
    t = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
    hero = COMMUNITY / cid / "assets" / f"{cid}-hero.png"
    return {
        "exists": path.exists(),
        "quality_v3": "teachany-quality-v3" in t,
        "phet": 'id="phet-lab"' in t and "_zh_CN.html" in t,
        "L123": all(x in t for x in ("practice-l1", "practice-l2", "practice-l3")),
        "checklist": "summary-checklist" in t,
        "labels": "ta-fig-tag" in t,
        "no_abt": "And 已有经验" not in t,
        "no_role": "角色任务" not in t,
        "no_junk": "teachany-enhanced" not in t,
        "hero": hero.exists() and hero.stat().st_size > 40000,
    }


def refresh_remaining_and_qc(catalog: dict, state: dict) -> None:
    done = set(state.get("done") or [])
    # also treat already-quality courses as done if marked
    remaining = []
    for c in catalog["courses"]:
        cid = c["id"]
        q = qc_course(cid)
        if all(q.get(k) for k in ("quality_v3", "phet", "L123", "checklist", "no_abt", "hero")):
            if cid not in done:
                done.add(cid)
            continue
        if cid not in done:
            remaining.append(cid)
    state["done"] = sorted(done)
    REMAINING.write_text("\n".join(remaining) + ("\n" if remaining else ""), encoding="utf-8")

    # QC page: last done + next remaining
    links = []
    for cid in list(sorted(done))[-8:] + remaining[:8]:
        name = next((x["center"] for x in catalog["courses"] if x["id"] == cid), cid)
        q = qc_course(cid)
        ok = all(q.get(k) for k in ("quality_v3", "phet", "L123", "no_abt"))
        links.append(f'<a href="/community/{cid}/index.html">{cid} · {name} {"✓" if ok else "…"}</a>')
    QC.write_text(
        f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><title>自动升级进度</title>
<style>body{{font-family:system-ui;background:#0b1220;color:#e2e8f0;max-width:760px;margin:32px auto;padding:0 20px}}a{{display:block;padding:12px;margin:8px 0;border-radius:12px;background:rgba(59,130,246,.2);color:#93c5fd;text-decoration:none;font-weight:700}}.dim{{color:#94a3b8}}.ok{{color:#34d399}}</style></head>
<body>
<h1>phy-m 自动升级进度</h1>
<p class="ok">已完成 {len(done)} 门 · 剩余 {len(remaining)} 门</p>
<p class="dim">标准：无字图+叠标 · PhET · L1/L2/L3 · 小结勾选 · 去 ABT/junk</p>
{''.join(links)}
</body></html>""",
        encoding="utf-8",
    )
    save_state(state)


def pick_courses(catalog: dict, state: dict, *, batch: str | None, limit: int, cids: list[str]) -> list[dict]:
    done = set(state.get("done") or [])
    by_id = {c["id"]: c for c in catalog["courses"]}
    if cids:
        return [by_id[c] for c in cids if c in by_id]
    ordered = catalog["courses"]
    if batch:
        ordered = [c for c in ordered if c.get("batch") == batch]
    out = []
    for c in ordered:
        if c["id"] in done:
            continue
        q = qc_course(c["id"])
        if all(q.get(k) for k in ("quality_v3", "phet", "L123", "checklist", "no_abt", "hero")):
            continue
        out.append(c)
        if len(out) >= limit:
            break
    return out


def process_one(cfg: dict, *, skip_images: bool, force_images: bool) -> dict:
    cid = cfg["id"]
    print(f"\n=== {cid} · {cfg['center']} ===", flush=True)
    img = "skipped"
    if not skip_images:
        img = gen_images(cfg, force=force_images)
        print(f"  images: {img}", flush=True)
    html = apply_html(cfg)
    print(f"  html: {html}", flush=True)
    q = qc_course(cid)
    ok = all(q.get(k) for k in ("quality_v3", "phet", "L123", "checklist", "no_abt", "labels"))
    # hero soft-required
    if not q.get("hero"):
        ok = False
    print(f"  qc: {'PASS' if ok else 'FAIL'} {q}", flush=True)
    return {"id": cid, "ok": ok, "images": img, "html": html, "qc": q}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=3)
    ap.add_argument("--batch", default="")
    ap.add_argument("--cid", action="append", default=[])
    ap.add_argument("--skip-images", action="store_true")
    ap.add_argument("--force-images", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    catalog = load_catalog()
    state = load_state()

    if args.status:
        refresh_remaining_and_qc(catalog, state)
        print(json.dumps({"done": len(state.get("done") or []), "remaining": len(REMAINING.read_text().splitlines()) if REMAINING.exists() else "?"}, ensure_ascii=False))
        return 0

    courses = pick_courses(catalog, state, batch=args.batch or None, limit=args.limit, cids=args.cid)
    if not courses:
        refresh_remaining_and_qc(catalog, state)
        print("NO_WORK remaining=0")
        return 0

    print(f"ROUND pick={[c['id'] for c in courses]}", flush=True)
    results = []
    for cfg in courses:
        try:
            results.append(process_one(cfg, skip_images=args.skip_images, force_images=args.force_images))
        except Exception as e:
            print(f"  EXCEPTION {e}", flush=True)
            results.append({"id": cfg["id"], "ok": False, "error": str(e)})
            state.setdefault("failed", []).append({"id": cfg["id"], "error": str(e)})

    newly = [r["id"] for r in results if r.get("ok")]
    state["done"] = sorted(set(state.get("done") or []) | set(newly))
    state.setdefault("rounds", []).append(
        {
            "at": datetime.now(timezone.utc).isoformat(),
            "ids": [r["id"] for r in results],
            "ok": newly,
            "fail": [r["id"] for r in results if not r.get("ok")],
        }
    )
    refresh_remaining_and_qc(catalog, state)
    print(
        f"\nROUND_DONE ok={len(newly)} fail={len(results)-len(newly)} done_total={len(state['done'])}",
        flush=True,
    )
    return 0 if newly else 1


if __name__ == "__main__":
    raise SystemExit(main())
