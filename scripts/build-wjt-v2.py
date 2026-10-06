#!/usr/bin/env python3
"""build-wjt-v2.py — hist-h-wei-jin-tang 从零新建（skill 标准骨架 + 复用真模块）
骨架：bio-h 22/22 标准课结构（section 直排，无 slide-page 嵌套）
复用：从旧版提取真模块片段组装
备份旧版为 index-v1-backup.html
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "community/hist-h-wei-jin-tang"
OLD = DIR / "index.html"
NEW = DIR / "index-v2.html"


def extract_section(html, idv):
    """按 id 提取 section 整体（配平扫描）"""
    m = re.search(r'<section\b[^>]*id="' + re.escape(idv) + r'"[^>]*>', html)
    if not m:
        return None
    depth = 1
    for n in re.finditer(r'<section\b[^>]*>|</section>', html[m.end():]):
        depth += -1 if n.group(0).startswith('</') else 1
        if depth == 0:
            return html[m.start():m.end() + n.end()]
    return None


def extract_slide_inner(html, tsh):
    """提取 slide-page 内层 slide-inner 内容"""
    m = re.search(r'<section\b[^>]*data-tsh="' + re.escape(tsh) + r'"[^>]*>', html)
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


old = OLD.read_text(encoding="utf-8")

# ---------- 提取可复用片段 ----------
parts = {}
for sid in ["objectives", "anchor", "pretest", "lesson-focus", "lesson-method",
            "module-1", "module-2", "module-3",
            "error-clinic", "memory-anchor", "posttest", "course-nav-map"]:
    parts[sid] = extract_section(old, sid)

# 地图探究：slide-page 的 slide-inner 转普通 section（含 data-teachany-map）
map_inner = extract_slide_inner(old, "地图探究")
parts["map"] = map_inner
# deep-understanding 原文件未闭合（存量缺陷）——手动界定到 card 闭合
du = re.search(
    r'(<section class="section" id="deep-understanding"[^>]*>\s*<h2[^>]*>📚 深度理解</h2>\s*<section class="card">[\s\S]*?</section>)\s*<section class="slide-page"',
    old)
parts["deep-understanding"] = (du.group(1) + "</section>") if du else None

# 概念归类 slide-page → 提取 card 内容转普通 section
drag_inner = extract_slide_inner(old, "互动 - 概念归类")
# 概念检测（无 id 的 conceptest 块）
cc = re.search(r'<section class="section teachany-upgrade-block" data-interactive="conceptest"[\s\S]*?</section>', old)
parts["conceptest"] = cc.group(0) if cc else None
# 大运河探究
inq = re.search(r'<section class="section teachany-upgrade-block" data-interactive="inquiry"[\s\S]*?</section>', old)
parts["inquiry"] = inq.group(0) if inq else None
# 真题练习（第一个无 id 的 evaluate 块）
zt = re.search(r'<section class="section teachany-upgrade-block" data-bloom-level="evaluate"[\s\S]*?<h2>📝 真题练习</h2>[\s\S]*?</section>', old)
parts["zhenti"] = zt.group(0) if zt else None
# AI 多模态
ai = re.search(r'<section class="section"[^>]*id="ai-media-zone"[\s\S]*?</section>', old)
parts["ai"] = ai.group(0) if ai else None
# audio-config
ac = re.search(r'<div id="audio-config"[\s\S]*?</script></div>', old)
parts["audio"] = ac.group(0) if ac else None
# navMap JS（__NAV_NODES__ + 绘制脚本，两段）
navjs = re.findall(r'<script>window\.__NAV_NODES__[\s\S]*?</script>\s*<script>\s*\(function\(\)\{\s*var cv = document\.getElementById\(\'navMapCanvas\'\);[\s\S]*?</script>', old)
parts["navjs"] = navjs[0] if navjs else None
# 拖拽 JS
dragjs = re.search(r'<script>\s*\(function\(\)\{\s*var pool = document\.getElementById\(\'drag-pool\'\);[\s\S]*?</script>', old)
parts["dragjs"] = dragjs.group(0) if dragjs else None
# 全景页时间轴卡（升级时生成的）
tl = re.search(r'<span class="phase-tag">Overview</span>[\s\S]*?</div></div>', old)
parts["timeline"] = tl.group(0) if tl else None
# hero 时间轴（hero-infographic 内四色卡）
ht = re.search(r'<section class="section" id="hero-infographic"[\s\S]*?</section>', old)
parts["hero_timeline"] = ht.group(0) if ht else None

missing = [k for k, v in parts.items() if not v]
print("提取失败:", missing if missing else "无（全部提取成功）")

# ---------- 新骨架 ----------
ABT = """<section class="section" id="abt-why" data-bloom-level="understand" data-scaffold="full" data-tts="abt-why"><div class="panel"><span class="phase-tag">ABT Narrative</span><h2>为什么要学这个？</h2><p><strong>已经知道：</strong>你在初中已学过三国鼎立、隋炀帝开运河、贞观之治等基本史实，能按朝代顺序排列主要王朝。</p><p><strong>但问题是：</strong>这四百年很容易被记成"朝代流水账"——说不清分裂时期为何孕育着统一的因素，也解释不了科举、三省六部这些制度创新为何能影响后世千年。</p><p><strong>所以学：</strong>以"分裂中孕育交融、交融中重建统一、统一中走向鼎盛"为主线，用历史地图、制度对比和真实史料，把这四百年读成一条有逻辑的历史脉络。</p></div></section>"""

HEAD = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>三国两晋南北朝与隋唐 · 高中历史 G10 · TeachAny v7.20</title>
<meta name="description" content="中国课标高中历史互动课件：三国两晋南北朝与隋唐。包含历史地图、知识图谱、真题训练、TTS、AI 学伴。">
<meta name="course-id" content="hist-h-wei-jin-tang">
<meta name="course-title" content="三国两晋南北朝与隋唐">
<meta name="course-subject" content="history">
<meta name="course-grade" content="high-10">
<meta name="course-version" content="2.0.0">
<meta name="teachany-version" content="7.20.0">
<meta name="teachany-node" content="hist-h-wei-jin-tang">
<meta name="teachany-subject" content="history">
<meta name="teachany-grade" content="10">
<meta name="teachany-stage" content="high">
<meta name="teachany-domain" content="中国古代史">
<meta name="teachany-prerequisites" content="初中中国历史, 朝代顺序, 历史地图阅读">
<meta name="teachany-lesson-type" content="new-concept">
<meta name="teachany-free-mode" content="false">
<link rel="stylesheet" href="../../assets/scripts/ai-tutor.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-tutor-card.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-tts-narrator.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-section-hints.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-knowledge-graph.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-audio-player.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-historical-map.css">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<style>
:root{--bg:#0a1520;--panel:#12202e;--card:#16293a;--line:#2a4a63;--text:#f0f7f4;--muted:#a8c4bb;--brand:#34d399;--brand2:#38bdf8;--warn:#f59e0b;--bad:#f87171;}
*{box-sizing:border-box} html,body{margin:0;max-width:100%;overflow-x:hidden;scroll-behavior:smooth} body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC",system-ui,sans-serif;line-height:1.75} a{color:#7dd3fc} button,input,textarea,select{min-height:44px} img,video,canvas,svg{max-width:100%;height:auto}
.teachany-brand-bar{position:sticky;top:0;z-index:50;display:flex;justify-content:space-between;align-items:center;gap:12px;padding:10px 16px;background:rgba(10,21,32,.92);border-bottom:1px solid rgba(148,163,184,.18);backdrop-filter:blur(10px)} .brand-logo{display:flex;align-items:center;gap:8px;color:#f8fafc;text-decoration:none;font-weight:800}.brand-version{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:#cbd5e1;background:rgba(255,255,255,.08);padding:4px 8px;border-radius:999px}
.hero{padding:58px 20px 34px;text-align:center;background:radial-gradient(circle at 15% 0%,rgba(245,158,11,.16),transparent 35%),radial-gradient(circle at 85% 10%,rgba(56,189,248,.16),transparent 32%)} h1{font-size:clamp(30px,6vw,54px);line-height:1.15;margin:0 auto 14px;max-width:980px}.subtitle{color:var(--muted);font-size:clamp(15px,2.5vw,19px);max-width:900px;margin:0 auto}
.section{max-width:1080px;margin:0 auto;padding:30px 20px}.panel{background:linear-gradient(180deg,rgba(22,41,58,.96),rgba(14,29,43,.96));border:1px solid rgba(148,163,184,.18);padding:22px;border-radius:16px;box-shadow:0 16px 40px rgba(0,0,0,.18)}
.card{background:rgba(255,255,255,.045);border:1px solid rgba(148,163,184,.16);border-radius:14px;padding:18px;margin:14px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px}.mini-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px}
.mini-card,.mini-panel{background:rgba(255,255,255,.055);border:1px solid rgba(148,163,184,.16);padding:16px;border-radius:12px}
.mini-panel h3{margin:0 0 8px;font-size:16px}.mini-panel p{margin:0;font-size:14px;opacity:.92}
.phase-tag{display:inline-flex;align-items:center;gap:6px;color:#bbf7d0;background:rgba(52,211,153,.12);border:1px solid rgba(52,211,153,.25);padding:4px 10px;font-size:13px;border-radius:8px}
h2{font-size:clamp(20px,3.6vw,26px);margin:0 0 12px} h3{font-size:17px}
.choice,.quiz-option{width:100%;text-align:left;border:1px solid rgba(52,211,153,.28);background:rgba(52,211,153,.08);color:var(--text);padding:14px 16px;cursor:pointer;border-radius:10px;font-size:15px}
.quiz-option.correct,.choice.selected{border-color:var(--brand);box-shadow:0 0 0 3px rgba(52,211,153,.18)}.quiz-option.wrong{border-color:var(--bad);background:rgba(248,113,113,.12)}
.feedback,.result{margin-top:12px;padding:13px;background:rgba(34,197,94,.10);border:1px solid rgba(34,197,94,.25);color:#dcfce7;border-radius:10px}.warn{background:rgba(245,158,11,.10);border-color:rgba(245,158,11,.28);color:#fde68a}
.ta-standard-figure{margin:20px auto 0;max-width:980px}.ta-standard-figure img{display:block;width:100%;border:1px solid rgba(148,163,184,.18);border-radius:14px}
.ta-standard-figure figcaption{margin-top:10px;color:var(--muted);font-size:14px;text-align:center}
.teachany-upgrade-block{margin:26px 0;padding:22px;border-radius:16px;border:1px solid rgba(148,163,184,.25);background:rgba(21,37,52,.5)}
.tu-q,.tu-fill{margin:14px 0;padding:14px;border-radius:12px;background:rgba(30,48,66,.45)}
.tu-opts{display:grid;gap:10px;margin-top:10px}
.tu-opt{text-align:left;padding:12px 14px;border-radius:10px;border:1px solid rgba(148,163,184,.35);background:rgba(51,65,85,.55);color:inherit;cursor:pointer;font-size:15px;line-height:1.5}
.tu-opt:hover{border-color:#60a5fa}.tu-opt.is-right,.tu-opt.correct{border-color:#34d399;background:rgba(16,185,129,.18)}.tu-opt.is-wrong,.tu-opt.wrong{border-color:#f87171;background:rgba(239,68,68,.15)}
.tu-fb{margin-top:12px;padding:12px;border-radius:10px;background:rgba(245,158,11,.12);border:1px solid rgba(245,158,11,.35);line-height:1.7}
.tu-inquiry{display:grid;gap:12px;margin:14px 0}.tu-inquiry textarea{width:100%;min-height:72px;margin-top:6px;border-radius:8px;padding:10px;border:1px solid rgba(148,163,184,.3);background:rgba(15,23,42,.5);color:inherit}
.tu-save{margin-top:8px;padding:10px 16px;border-radius:10px;border:0;background:#3b82f6;color:#fff;cursor:pointer;font-weight:600}
.drag-pool,.drop-zone{display:flex;flex-wrap:wrap;gap:8px;min-height:56px;padding:10px;border:2px dashed rgba(148,163,184,0.4);border-radius:12px;background:rgba(30,41,59,0.65)}
.drop-zone{border-style:solid;min-height:80px;flex-direction:column;align-items:stretch}
.drag-chip{display:inline-flex;align-items:center;gap:6px;padding:10px 14px;border-radius:10px;background:rgba(51,65,85,0.8);border:2px solid rgba(148,163,184,0.4);cursor:grab;font-size:14px;touch-action:none;user-select:none;color:#e2e8f0}
.drag-chip.dragging{opacity:.55;cursor:grabbing}.drop-zone h4{margin:0 0 8px;font-size:14px;color:#f1f5f9}
.focus-detail{border-left:4px solid var(--brand2)}
.ta-quiz-correct{outline:2px solid #22c55e !important;background:rgba(34,197,94,.16) !important;border-radius:10px}
.ta-quiz-wrong{outline:2px solid #ef4444 !important;background:rgba(239,68,68,.12) !important;border-radius:10px}
.tu-fb.ta-fb-correct{background:rgba(34,197,94,.12);color:#15803d}.tu-fb.ta-fb-wrong{background:rgba(239,68,68,.1);color:#fbbf24}
@media(max-width:640px){.section{padding:22px 14px}.card{padding:15px}.grid{grid-template-columns:1fr}}
</style>
<link rel="stylesheet" href="../../assets/scripts/teachany-floating-dock.css">
</head>
<body>
<div class="teachany-brand-bar"><a class="brand-logo" href="https://www.teachany.cn/"><img src="https://www.teachany.cn/assets/teachany-icon.png" alt="TeachAny" style="height:26px;width:26px;border-radius:7px"><span class="brand-name">TeachAny</span></a><div><a href="https://www.teachany.cn/">Gallery</a> <span class="brand-version">v2.0.0 · skill v7.20</span></div></div>
"""

HERO = """<header class="hero" id="hero" data-tts="hero" data-tsh="开场 - 用真实问题建立学习动机">
<h1>三国两晋南北朝与隋唐</h1>
<p class="subtitle">四百年，从三国鼎立到盛唐气象：分裂中孕育交融，交融中重建统一，统一中走向鼎盛。</p>
<div class="course-meta-badges" style="display:flex;gap:8px;justify-content:center;margin-top:12px;flex-wrap:wrap;"><span style="display:inline-block;padding:4px 14px;border-radius:999px;font-size:13px;letter-spacing:.5px;background:rgba(56,189,248,.15);border:1px solid rgba(56,189,248,.45);color:#7dd3fc;">高中历史</span><span style="display:inline-block;padding:4px 14px;border-radius:999px;font-size:13px;letter-spacing:.5px;background:rgba(52,211,153,.15);border:1px solid rgba(52,211,153,.45);color:#6ee7b7;">G10</span></div>
<figure class="ta-standard-figure" style="margin:22px auto 0;max-width:980px"><img class="hero-cover-img" src="./assets/hist-h-wei-jin-tang-hero-v2.png" alt="三国战船、魏晋石窟佛像、隋唐长安与丝绸之路历史长卷" loading="eager"></figure>
</header>
"""

TAIL = """
<section class="section" id="knowledge-graph" data-tsh="知识图谱">
  <h2>🗺️ 知识图谱：三国两晋南北朝与隋唐</h2>
  <div data-teachany-kg="hist-h-wei-jin-tang">
    <canvas class="tkg-fallback-canvas" width="720" height="120" aria-label="知识图谱互动画布" style="display:block;width:100%;max-height:140px;border-radius:12px;"></canvas>
  </div>
</section>
<section class="ta-standard-section" id="teachany-ai-tutor-card">
  <div data-teachany-tutor-card></div>
</section>
<script>window.__TEACHANY_TUTOR_CONFIG__={courseId:'hist-h-wei-jin-tang',subject:'history',grade:10,stage:'high',topic:'三国两晋南北朝与隋唐'};</script>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="../../assets/scripts/ai-tutor.js" defer></script>
<script src="../../assets/scripts/teachany-tutor-card.js" defer></script>
<script src="../../assets/scripts/teachany-tts-narrator.js" defer></script>
<script src="../../assets/scripts/teachany-section-hints.js" defer></script>
<script src="../../assets/scripts/teachany-knowledge-graph.js" defer></script>
<script src="../../assets/scripts/teachany-audio-player.js" defer></script>
<script src="../../assets/scripts/teachany-historical-map.js" defer></script>
<script src="../../assets/scripts/teachany-quiz-binding.js" defer></script>
<script src="../../assets/scripts/teachany-floating-dock.js" defer></script>
</body>
</html>
"""

# ---------- 组装 ----------
body = [HEAD, HERO]
if parts["hero_timeline"]:
    body.append(parts["hero_timeline"])
if parts["audio"]:
    body.append(parts["audio"])
body.append(ABT)
for key in ["objectives", "anchor", "pretest"]:
    if parts[key]:
        body.append(parts[key])
# 历史脉络全景（concept 页）
if parts["timeline"]:
    body.append('<section class="section" id="concept-overview" data-bloom-level="understand" data-scaffold="full" data-tts="concept-overview" data-tsh="历史脉络全景"><div class="panel">'
                + parts["timeline"] + "</div></section>")
for key in ["lesson-focus"]:
    if parts[key]:
        body.append(parts[key])
# 地图探究
if parts["map"]:
    body.append('<section class="section" id="map-explore" data-bloom-level="apply" data-scaffold="partial" data-tts="map-explore" data-tsh="地图探究"><div class="panel">'
                + parts["map"] + "</div></section>")
for key in ["module-1", "module-2", "module-3", "lesson-method"]:
    if parts[key]:
        body.append(parts[key])
# 概念归类
if drag_inner:
    body.append('<section class="section" id="drag-activity" data-bloom-level="apply" data-scaffold="partial" data-tts="drag-activity" data-tsh="互动 - 概念归类"><div class="panel">'
                + drag_inner + "</div></section>")
for key in ["deep-understanding", "conceptest", "inquiry", "zhenti", "error-clinic", "memory-anchor", "ai", "posttest", "course-nav-map"]:
    if parts[key]:
        body.append(parts[key])
if parts["navjs"]:
    body.append(parts["navjs"])
if parts["dragjs"]:
    body.append(parts["dragjs"])
body.append(TAIL)

html = "\n".join(body)
NEW.write_text(html, encoding="utf-8")
print(f"新课件已生成: {NEW.name} ({len(html)//1024} KB)")
