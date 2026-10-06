#!/usr/bin/env python3
"""build-v3-pipeline.py — 通用课件精致重制流水线（wei-jin-tang 模式泛化）
用法: python3 build-v3-pipeline.py <cid> [--dry]
流程:
  1. 提取源课件全部真模块（teachany-upgrade-block/lesson-focus/lesson-method/audio/地图/图谱）
  2. LLM 生成: hero副标题 / ABT / 精讲四卡加厚 / concept总览
  3. 组装 v2 标准骨架（section直排，复用 wei-jin-tang 样式体系）
  4. 标准挂载: quiz-binding/kg/audio-player/tts/ai-tutor/section-hints/navMap/TUTOR_CONFIG
输出: <cid>/index-v3.html（验证后手动替换 index.html）
"""
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
API_KEY = os.environ["OPENROUTER_API_KEY"]
MODEL = os.environ.get("ZH_MODEL", "deepseek/deepseek-chat-v3-0324")
DRY = "--dry" in sys.argv

SUBJECT_MAP = {"bio": "生物", "chem": "化学", "phy": "物理", "math": "数学",
               "chn": "语文", "eng": "英语", "geo": "地理", "sci": "科学",
               "cs": "信息科技", "it": "信息技术"}
GRADE_MAP = {"h": "高中", "m": "初中", "e": "小学"}


def llm_json(body, max_tokens=2000):
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps({"model": MODEL,
                                 "messages": [{"role": "user", "content": body}],
                                 "temperature": 0.5, "max_tokens": max_tokens}).encode(),
                headers={"Authorization": f"Bearer {API_KEY}",
                         "Content-Type": "application/json",
                         "HTTP-Referer": "https://teachany.cn",
                         "X-OpenRouter-Title": "v3-pipeline"})
            with urllib.request.urlopen(req, timeout=150) as r:
                txt = json.load(r)["choices"][0]["message"]["content"]
            t = re.sub(r"```(?:json)?", "", txt)
            start = t.find("{")
            if start < 0:
                raise ValueError("no json")
            b = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", t[start:])
            try:
                obj, _ = json.JSONDecoder().raw_decode(b)
                return obj
            except json.JSONDecodeError:
                return json.loads(re.sub(r",\s*([}\]])", r"\1", b[:b.rfind("}") + 1]))
        except Exception as e:
            last = e
            time.sleep((attempt + 1) * 15)
    raise last


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def extract_section(html, idv):
    m = re.search(r'<section\b[^>]*id="' + re.escape(idv) + r'"[^>]*>', html)
    if not m:
        return None
    depth = 1
    for n in re.finditer(r'<section\b[^>]*>|</section>', html[m.end():]):
        tag = n.group(0)
        if tag.startswith('</'):
            depth -= 1
            if depth == 0:
                return html[m.start():m.end() + n.end()]
        else:
            # 安全边界：嵌套中出现带 id 的新 section ⇒ 外层未闭合，强制截断
            if depth >= 2 and 'id="' in tag:
                seg = html[m.start():m.end() + n.start()]
                inner = len(re.findall(r'<section\b', seg[len(m.group(0)):])) - len(re.findall(r'</section>', seg[len(m.group(0)):]))
                if inner > 0:
                    seg += "</section>" * inner
                return seg
            depth += 1
    # 未闭合兜底：截断到下一个顶层 section 前，并补足内部未闭合
    nxt = re.search(r'<section\b', html[m.end():])
    if nxt:
        seg = html[m.start():m.end() + nxt.start()]
    else:
        seg = html[m.start():]
    inner = len(re.findall(r'<section\b', seg[len(m.group(0)):])) - len(re.findall(r'</section>', seg[len(m.group(0)):]))
    if inner > 0:
        seg += "</section>" * inner
    return seg


def slide_inner_of(html, data_tts=None, data_tsh=None):
    pat = (r'<section\b[^>]*data-tts="' + re.escape(data_tts) + r'"[^>]*>') if data_tts else \
          (r'<section\b[^>]*data-tsh="' + re.escape(data_tsh) + r'"[^>]*>')
    m = re.search(pat, html)
    if not m:
        return None
    depth = 1
    for n in re.finditer(r'<section\b[^>]*>|</section>', html[m.end():]):
        depth += -1 if n.group(0).startswith('</') else 1
        if depth == 0:
            block = html[m.start():m.end() + n.end()]
            inner = re.search(r'<div class="slide-inner">([\s\S]*?)</div>\s*$', block)
            return inner.group(1) if inner else block
    return None


def title_of(html, cid):
    h1 = re.search(r"<h1[^>]*>([\s\S]{0,120}?)</h1>", html)
    if h1:
        t = re.sub(r"<[^>]+>", "", h1.group(1)).strip()
        t = re.sub(r"^[\U0001F300-\U0001FAFF☀-➿\s]+", "", t).strip()
        if t:
            return t[:40]
    tm = re.search(r"<title>([^<·《》]+)", html)
    return tm.group(1).strip()[:40] if tm else cid


def meta_of(html, cid):
    subj = re.search(r'<meta name="course-subject" content="([^"]+)"', html)
    grade = re.search(r'<meta name="teachany-grade" content="([^"]+)"', html)
    stage = re.search(r'<meta name="teachany-stage" content="([^"]+)"', html)
    subject = subj.group(1) if subj else cid.split("-")[0]
    subject_name = SUBJECT_MAP.get(subject, subject)
    stage_name = {"high": "高中", "middle": "初中", "primary": "小学"}.get(stage.group(1) if stage else "", "")
    if not stage_name and grade:
        stage_name = {"10": "高中", "7": "初中", "8": "初中", "9": "初中"}.get(grade.group(1), "初中")
    g = grade.group(1) if grade else ""
    return subject, subject_name, f"{stage_name}{subject_name}", f"G{g}" if g else ""


PROMPT = """你是中国{stage}{subject_name}教师。课件《{title}》现有精讲：
{current}

任务：为课件的"开场"与"核心精讲"生成内容，严格输出 JSON（不要 markdown 围栏）：
{{
 "subtitle": "开场副标题",
 "abt_and": "已经知道",
 "abt_but": "但问题是",
 "abt_therefore": "所以学",
 "overview_title": "本课知识总览标题（如'知识全景：…'）",
 "overview_intro": "总览引言（40-60字，带教学感）",
 "focus": {{
   "essence": "概念本质（90-130字）",
   "process": "结构与过程（110-160字）",
   "example": "实例与证据（90-140字，含具体例子/数据）",
   "pitfall": "易错提醒（60-90字，两三个易混点）"
 }},
 "practice": {{
   "l1": "基础巩固层任务（含1道直接应用题，40-60字）",
   "l2": "能力应用层任务（含1道情境应用题，50-70字）",
   "l3": "迁移挑战层任务（含1道综合/开放题，50-70字）"
 }}
}}
要求：
1. subtitle 30-45字：用一个问题或悬念开场，落到本课核心；
2. abt 三段各 25-50 字：具体前置知识/真实卡点/真实任务情境，严禁空话套话；
3. focus 四段必须与现有精讲一致并按教材常识扩厚，具体到概念名词/步骤/例子；
4. 严禁"具有重要意义""需要掌握"等空话。"""


def process(cid):
    d = COMMUNITY / cid
    html = (d / "index.html").read_text(encoding="utf-8", errors="replace")
    if "<!-- v3-built -->" in html:
        return cid, "已是v3", None

    subject, subject_name, stage_subject, grade_badge = meta_of(html, cid)
    title = title_of(html, cid)

    # ---- 提取真模块 ----
    parts = {}
    for sid in ["objectives", "anchor", "pretest", "lesson-focus", "lesson-method",
                "deep-understanding", "error-clinic", "memory-anchor", "posttest",
                "course-nav-map", "module-1", "module-2", "module-3", "module-4", "practice-l1", "practice-l2", "practice-l3", "lesson-pitfall", "phet-lab", "hero-infographic"]:
        parts[sid] = extract_section(html, sid)
    # 无 id 的 upgrade 块（概念检测/探究等）按出现序保留
    others = re.findall(r'<section class="section teachany-upgrade-block"(?![^>]*id=)[^>]*>[\s\S]*?</section>', html)
    # audio playlist
    ac = re.search(r'<div id="audio-config"[\s\S]*?</script></div>', html)
    parts["audio"] = ac.group(0) if ac else None
    # 互动地图（如有）
    mapm = re.search(r'(<div class="map-host"[^>]*>[\s\S]*?<script type="application/json" data-teachany-map-config>[\s\S]*?</script>\s*</div>)', html)
    parts["map"] = mapm.group(1) if mapm else None
    # 概念归类（如有）
    drag = slide_inner_of(html, data_tsh="互动 - 概念归类") or \
           (lambda m: m.group(1) if m else None)(re.search(r'(<div class="drag-pool" id="drag-pool"[\s\S]{0,8000}?<p id="drag-readout"[^>]*>[^<]*</p>\s*</div></div>)', html))
    # navMap JS（如有 course-nav-map 内嵌脚本）
    navjs = re.search(r'<script>window\.__NAV_NODES__[\s\S]*?</script>\s*<script>\s*\(function\(\)\{\s*var cv = document\.getElementById\(\'navMapCanvas\'\);[\s\S]*?</script>', html)
    parts["navjs"] = navjs.group(0) if navjs else None

    have = [k for k, v in parts.items() if v]
    for k in ["objectives", "anchor", "pretest", "lesson-focus", "lesson-method", "deep-understanding", "error-clinic", "memory-anchor", "posttest", "course-nav-map", "module-1", "module-2", "module-3", "module-4", "practice-l1", "practice-l2", "practice-l3", "lesson-pitfall", "phet-lab", "hero-infographic", "map"]: parts.setdefault(k, None)
    print(f"[{cid}] 提取: {have}, 其他upgrade块: {len(others)}")

    # ---- LLM 生成 ----
    focus_now = ""
    if parts["lesson-focus"]:
        t = re.sub(r"<[^>]+>", " ", parts["lesson-focus"])
        focus_now = re.sub(r"\s+", " ", t).strip()[:500]
    gen = llm_json(PROMPT.format(stage=stage_subject, subject_name=subject_name,
                               title=title, current=focus_now or "（精讲缺失，请依据课名与学科常识补全）"))

    # ---- 组装 ----
    focus_cards = ""
    f = gen["focus"]
    focus_cards = (
        f'<div class="card focus-detail"><p><strong>概念本质：</strong>{esc(f["essence"])}</p></div>\n'
        f'<div class="card focus-detail"><p><strong>结构与过程：</strong>{esc(f["process"])}</p></div>\n'
        f'<div class="card focus-detail"><p><strong>实例与证据：</strong>{esc(f["example"])}</p></div>\n'
        f'<div class="card focus-detail"><p><strong>易错提醒：</strong>{esc(f["pitfall"])}</p></div>')
    # 原 lesson-focus 保留标题与引入段
    lf_head = ""
    if parts["lesson-focus"]:
        m = re.search(r'([\s\S]*?<h2>[\s\S]*?</h2>\s*<p>[\s\S]*?</p>)', parts["lesson-focus"])
        if m:
            lf_head = m.group(1).replace('id="lesson-focus"', 'id="lesson-focus" data-v3="1"')
    lesson_block = (lf_head + focus_cards + "</section>") if lf_head else \
        f'<section class="section" id="lesson-focus" data-tts="lesson-focus"><div class="panel"><span class="phase-tag">知识精讲</span><h2>{esc(title)}</h2>{focus_cards}</div></section>'

    abt = (f'<section class="section" id="abt-why" data-bloom-level="understand" data-scaffold="full" data-tts="abt-why">'
           f'<div class="panel"><span class="phase-tag">ABT Narrative</span><h2>为什么要学这个？</h2>'
           f'<p><strong>已经知道：</strong>{esc(gen["abt_and"])}</p>'
           f'<p><strong>但问题是：</strong>{esc(gen["abt_but"])}</p>'
           f'<p><strong>所以学：</strong>{esc(gen["abt_therefore"])}</p></div></section>')

    overview = (f'<section class="section" id="concept-overview" data-bloom-level="understand" data-tts="concept-overview" data-tsh="知识总览">'
                f'<div class="panel"><span class="phase-tag">Overview</span><h2>{esc(gen["overview_title"])}</h2>'
                f'<p style="font-size:16px;opacity:.9">{esc(gen["overview_intro"])}</p></div></section>')

    badge = (f'<div class="course-meta-badges" style="display:flex;gap:8px;justify-content:center;margin-top:12px;flex-wrap:wrap;">'
             f'<span style="display:inline-block;padding:4px 14px;border-radius:999px;font-size:13px;background:rgba(56,189,248,.15);border:1px solid rgba(56,189,248,.45);color:#7dd3fc;">{esc(stage_subject)}</span>'
             f'<span style="display:inline-block;padding:4px 14px;border-radius:999px;font-size:13px;background:rgba(52,211,153,.15);border:1px solid rgba(52,211,153,.45);color:#6ee7b7;">{esc(grade_badge)}</span></div>')

    old_metas = "\n".join(re.findall(r'<meta\s+name="teachany-[a-z-]+"\s+content="[^"]*"\s*>', html))
    old_course_metas = "\n".join(re.findall(r'<meta\s+name="course-[a-z-]+"\s+content="[^"]*"\s*>', html))
    # meta 兜底：缺失项按 cid 推断补默认值
    def _has(name):
        return re.search(r'name="' + name + r'"', old_metas)
    defaults = []
    if not _has("teachany-node"):
        defaults.append(f'<meta name="teachany-node" content="{cid}">')
    if not _has("teachany-subject"):
        defaults.append(f'<meta name="teachany-subject" content="{subject}">')
    if not _has("teachany-domain"):
        domain_map = {"bio": "生命科学", "chem": "物质科学", "phy": "物质科学", "sci": "综合科学",
                      "math": "数学", "chn": "人文", "eng": "语言", "geo": " Earth Science", "hist": "人文", "it": "信息技术", "cs": "信息技术"}
        defaults.append(f'<meta name="teachany-domain" content="{domain_map.get(subject, "综合")}">')
    if not _has("teachany-prerequisites"):
        defaults.append(f'<meta name="teachany-prerequisites" content="{GRADE_MAP.get(cid.split("-")[1], "初中")}{subject_name}基础">')
    if defaults:
        old_metas += "\n" + "\n".join(defaults)
    audio_block = parts["audio"]
    if not audio_block:
        import glob as _g
        mp3s = sorted(_g.glob(str(COMMUNITY / cid / "tts" / "*.mp3")))[:10]
        if mp3s:
            items = []
            for i, mp in enumerate(mp3s, 1):
                name = Path(mp).stem
                items.append({"id": f"s{i:02d}", "title": name, "src": f"tts/{name}.mp3", "text": f"{title} · {name}"})
            audio_block = ('<div id="audio-config" data-teachany-audio hidden><script type="application/json" data-teachany-audio-playlist>'
                           + json.dumps(items, ensure_ascii=False) + '</script></div>')

    body = [
        '<div class="teachany-brand-bar"><a class="brand-logo" href="https://www.teachany.cn/"><img src="https://www.teachany.cn/assets/teachany-icon.png" alt="TeachAny" style="height:26px;width:26px;border-radius:7px"><span class="brand-name">TeachAny</span></a><div><a href="https://www.teachany.cn/">Gallery</a> <span class="brand-version">v3.0.0 · skill v7.20</span></div></div>',
        f'<header class="hero" id="hero" data-tts="hero" data-tsh="开场 - 用真实问题建立学习动机"><h1>{esc(title)}</h1><p class="subtitle">{esc(gen["subtitle"])}</p>{badge}</header>',
    ]
    if audio_block:
        body.append(audio_block)
    body.append(abt)
    for k in ["objectives", "anchor", "pretest"]:
        if parts[k]:
            body.append(parts[k])
    body.append(overview)
    body.append(lesson_block)
    if parts["phet-lab"]:
        body.append(parts["phet-lab"])
    if parts["map"]:
        body.append(f'<section class="section" id="map-explore" data-bloom-level="apply" data-tts="map-explore" data-tsh="地图探究"><div class="panel">{parts["map"]}</div></section>')
    for k in ["lesson-method", "module-1", "module-2", "module-3", "module-4"]:
        if parts[k]:
            body.append(parts[k])
    if drag:
        body.append(f'<section class="section" id="drag-activity" data-bloom-level="apply" data-tts="drag-activity" data-tsh="互动 - 概念归类"><div class="panel">{drag}</div></section>')
    if not parts["practice-l1"] and gen.get("practice"):
        pr = gen["practice"]
        practice_block = (
            f'<section class="section" id="tiered-practice" data-bloom-level="apply" data-tts="tiered-practice" data-tsh="分层练习">'
            f'<div class="panel"><span class="phase-tag">Tiered Practice</span><h2>🏋️ 分层练习：三关挑战</h2>'
            f'<div class="grid">'
            f'<div class="mini-card"><h3>⭐ 第一关 · 基础巩固</h3><p>{esc(pr["l1"])}</p></div>'
            f'<div class="mini-card"><h3>⭐⭐ 第二关 · 能力应用</h3><p>{esc(pr["l2"])}</p></div>'
            f'<div class="mini-card"><h3>⭐⭐⭐ 第三关 · 迁移挑战</h3><p>{esc(pr["l3"])}</p></div>'
            f'</div></div></section>')
        body.append(practice_block)
    for k in ["deep-understanding", "lesson-pitfall", "error-clinic", "memory-anchor"]:
        if parts[k]:
            body.append(parts[k])
    for o in others:
        body.append(o)
    body.append(overview) if False else None
    for k in ["posttest", "course-nav-map"]:
        if parts[k]:
            body.append(parts[k])
    if parts["navjs"]:
        body.append(parts["navjs"])
    body.append(f'<section class="section" id="knowledge-graph" data-tsh="知识图谱"><h2>🗺️ 知识图谱：{esc(title)}</h2><div data-teachany-kg="{cid}"><canvas class="tkg-fallback-canvas" width="720" height="120" aria-label="知识图谱互动画布" style="display:block;width:100%;max-height:140px;border-radius:12px;"></canvas></div></section>')
    body.append('<section class="ta-standard-section" id="teachany-ai-tutor-card"><div data-teachany-tutor-card></div></section>')
    body.append(f'<script>window.__TEACHANY_TUTOR_CONFIG__={{courseId:\'{cid}\',subject:\'{subject}\',topic:\'{esc(title)}\'}};</script>')

    tail_scripts = ["ai-tutor", "teachany-tutor-card", "teachany-tts-narrator",
                    "teachany-section-hints", "teachany-knowledge-graph",
                    "teachany-audio-player", "teachany-quiz-binding"]
    if parts["map"]:
        tail_scripts = ["teachany-historical-map"] + tail_scripts
    tail = "".join(f'<script src="../../assets/scripts/{s}.js" defer></script>\n' for s in tail_scripts)
    body.append(tail + "</body>\n</html>")

    css = Path(ROOT / "scripts/v3-skeleton.css")
    head = build_head(title, cid, subject, css.read_text(encoding="utf-8") if css.exists() else "", old_metas + "\n" + old_course_metas)
    out_html = head + "\n".join(body)
    no = len(re.findall(r"<section\b", out_html))
    nc = len(re.findall(r"</section>", out_html))
    if no > nc:
        out_html = out_html.replace("</body>", "</section>\n</body>")
        while len(re.findall(r"<section\b", out_html)) > len(re.findall(r"</section>", out_html)):
            out_html = out_html.replace("</body>", "</section>\n</body>", 1) if "</body>" in out_html else out_html + "</section>"
    outp = d / "index-v3.html"
    if not DRY:
        outp.write_text(out_html, encoding="utf-8")
    return cid, f"v3 生成 {len(out_html)//1024}KB", outp


def build_head(title, cid, subject, extra_css="", head_metas=""):
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{title} · TeachAny v7.20</title>
<meta name="course-id" content="{cid}">
{extra_css}
<meta name="course-title" content="{title}">
<meta name="course-subject" content="{subject}">
{head_metas}
<meta name="teachany-version" content="7.20.0">
<link rel="stylesheet" href="../../assets/scripts/ai-tutor.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-tutor-card.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-tts-narrator.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-section-hints.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-knowledge-graph.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-audio-player.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-floating-dock.css">
<style>
:root{{--bg:#0a1520;--panel:#12202e;--card:#16293a;--line:#2a4a63;--text:#f0f7f4;--muted:#a8c4bb;--brand:#34d399;--brand2:#38bdf8;--warn:#f59e0b;--bad:#f87171;}}
*{{box-sizing:border-box}} html,body{{margin:0;max-width:100%;overflow-x:hidden;scroll-behavior:smooth}} body{{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC",system-ui,sans-serif;line-height:1.75}} a{{color:#7dd3fc}}
.teachany-brand-bar{{position:sticky;top:0;z-index:50;display:flex;justify-content:space-between;align-items:center;gap:12px;padding:10px 16px;background:rgba(10,21,32,.92);border-bottom:1px solid rgba(148,163,184,.18);backdrop-filter:blur(10px)}} .brand-logo{{display:flex;align-items:center;gap:8px;color:#f8fafc;text-decoration:none;font-weight:800}}.brand-version{{font-family:ui-monospace,monospace;color:#cbd5e1;background:rgba(255,255,255,.08);padding:4px 8px;border-radius:999px}}
.hero{{padding:56px 20px 32px;text-align:center;background:radial-gradient(circle at 15% 0%,rgba(245,158,11,.14),transparent 35%),radial-gradient(circle at 85% 10%,rgba(56,189,248,.16),transparent 32%)}} h1{{font-size:clamp(28px,5.6vw,52px);line-height:1.15;margin:0 auto 14px;max-width:980px}}.subtitle{{color:var(--muted);font-size:clamp(15px,2.5vw,19px);max-width:900px;margin:0 auto}}
.section{{max-width:1080px;margin:0 auto;padding:28px 20px}}.panel{{background:linear-gradient(180deg,rgba(22,41,58,.96),rgba(14,29,43,.96));border:1px solid rgba(148,163,184,.18);padding:22px;border-radius:16px;box-shadow:0 16px 40px rgba(0,0,0,.18)}}
.card{{background:rgba(255,255,255,.045);border:1px solid rgba(148,163,184,.16);border-radius:14px;padding:18px;margin:14px 0}}.focus-detail{{border-left:4px solid var(--brand2)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px}}.mini-card{{background:rgba(255,255,255,.055);border:1px solid rgba(148,163,184,.16);padding:16px;border-radius:12px}}
.phase-tag{{display:inline-flex;align-items:center;gap:6px;color:#bbf7d0;background:rgba(52,211,153,.12);border:1px solid rgba(52,211,153,.25);padding:4px 10px;font-size:13px;border-radius:8px}}
h2{{font-size:clamp(20px,3.6vw,26px);margin:0 0 12px}}h3{{font-size:17px}}
.choice,.quiz-option{{width:100%;text-align:left;border:1px solid rgba(52,211,153,.28);background:rgba(52,211,153,.08);color:var(--text);padding:14px 16px;cursor:pointer;border-radius:10px;font-size:15px}}.quiz-option.correct{{border-color:var(--brand);box-shadow:0 0 0 3px rgba(52,211,153,.18)}}.quiz-option.wrong{{border-color:var(--bad);background:rgba(248,113,113,.12)}}
.feedback,.result{{margin-top:12px;padding:13px;background:rgba(34,197,94,.10);border:1px solid rgba(34,197,94,.25);color:#dcfce7;border-radius:10px}}.warn{{background:rgba(245,158,11,.10);border-color:rgba(245,158,11,.28);color:#fde68a}}
.teachany-upgrade-block{{margin:26px auto;padding:22px;border-radius:16px;border:1px solid rgba(148,163,184,.25);background:rgba(21,37,52,.5);max-width:1080px}}
.tu-q{{margin:14px 0;padding:14px;border-radius:12px;background:rgba(30,48,66,.45)}}.tu-opts{{display:grid;gap:10px;margin-top:10px}}
.tu-opt{{text-align:left;padding:12px 14px;border-radius:10px;border:1px solid rgba(148,163,184,.35);background:rgba(51,65,85,.55);color:inherit;cursor:pointer;font-size:15px;line-height:1.5}}.tu-opt:hover{{border-color:#60a5fa}}.tu-opt.is-right,.tu-opt.correct{{border-color:#34d399;background:rgba(16,185,129,.18)}}.tu-opt.is-wrong,.tu-opt.wrong{{border-color:#f87171;background:rgba(239,68,68,.15)}}
.tu-fb{{margin-top:12px;padding:12px;border-radius:10px;background:rgba(245,158,11,.12);border:1px solid rgba(245,158,11,.35);line-height:1.7}}.tu-inquiry{{display:grid;gap:12px;margin:14px 0}}.tu-inquiry textarea{{width:100%;min-height:72px;margin-top:6px;border-radius:8px;padding:10px;border:1px solid rgba(148,163,184,.3);background:rgba(15,23,42,.5);color:inherit}}.tu-save{{margin-top:8px;padding:10px 16px;border-radius:10px;border:0;background:#3b82f6;color:#fff;cursor:pointer;font-weight:600}}
.ta-quiz-correct{{outline:2px solid #22c55e !important;background:rgba(34,197,94,.16) !important;border-radius:10px}}.ta-quiz-wrong{{outline:2px solid #ef4444 !important;background:rgba(239,68,68,.12) !important;border-radius:10px}}
.ta-quiz-done{{opacity:.92}}textarea{{width:100%;border:1px solid var(--line);background:#0b1628;color:var(--text);padding:12px 14px;font-size:16px}}
@media(max-width:640px){{.section{{padding:22px 14px}}.card{{padding:15px}}.grid{{grid-template-columns:1fr}}}}
{extra_css}
</style>
</head>
<body>
"""


if __name__ == "__main__":
    process(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "math-m-pythagorean-theorem")
