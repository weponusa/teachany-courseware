#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate CN courseware from a JSON spec (all stages/subjects).

Usage:
  python3 build-cn-course.py --spec path/to/spec.json

Output: community/{node_id}/index.html, manifest.json, PLAN.md
Standard modules are NOT injected — run finalize-courseware.py afterward.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import importlib.util
import json
import re
import sys
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
_map_mod = importlib.util.spec_from_file_location("cn_map_config", SCRIPT_DIR / "cn-map-config.py")
_cn_map = importlib.util.module_from_spec(_map_mod)
_map_mod.loader.exec_module(_cn_map)
default_map_config = _cn_map.default_map_config
_maps_spec = importlib.util.spec_from_file_location("apply_maps", SCRIPT_DIR / "apply-historical-maps.py")
_apply_maps = importlib.util.module_from_spec(_maps_spec)
_maps_spec.loader.exec_module(_apply_maps)
REPO_ROOT = SCRIPT_DIR.parent
COMMUNITY = REPO_ROOT / "community"
STAGE_LABEL = {"elementary": "小学", "middle": "初中", "high": "高中"}
SUBJECT_LABEL = {
    "science": "科学", "math": "数学", "chinese": "语文", "english": "英语",
    "history": "历史", "geography": "地理", "biology": "生物", "chemistry": "化学",
    "physics": "物理", "info-tech": "信息科技", "politics": "道德与法治",
    "psychology": "心理健康",
}
TEACHANY_VERSION = "7.20.0"

THEMES = {
    "orange": {
        "bg": "#fff7ed", "text": "#431407", "cover_grad": "#fed7aa", "h1": "#9a3412",
        "card_border": "#fdba74", "accent": "#f97316", "header": "#9a3412",
        "tag_bg": "#ffedd5", "tag_fg": "#c2410c", "obj_bg": "#fffbeb", "choice_border": "#fdba74",
        "choice_bg": "#fffbeb", "input_bg": "#fffbeb", "caption": "#a16207", "num": "#ea580c",
        "canvas_bg": "#fffbeb", "drag_dash": "#fdba74", "drag_chip_bg": "#ffedd5", "shadow": "154,52,18",
    },
    "blue": {
        "bg": "#eff6ff", "text": "#1e293b", "cover_grad": "#bfdbfe", "h1": "#1e3a8a",
        "card_border": "#bfdbfe", "accent": "#3b82f6", "header": "#1e3a8a",
        "tag_bg": "#dbeafe", "tag_fg": "#1d4ed8", "obj_bg": "#f0f7ff", "choice_border": "#93c5fd",
        "choice_bg": "#f0f7ff", "input_bg": "#f8fbff", "caption": "#64748b", "num": "#3b82f6",
        "canvas_bg": "#f8fbff", "drag_dash": "#93c5fd", "drag_chip_bg": "#dbeafe", "shadow": "30,58,138",
    },
    "green": {
        "bg": "#f0fdf4", "text": "#14532d", "cover_grad": "#bbf7d0", "h1": "#166534",
        "card_border": "#86efac", "accent": "#22c55e", "header": "#166534",
        "tag_bg": "#dcfce7", "tag_fg": "#15803d", "obj_bg": "#f0fdf4", "choice_border": "#86efac",
        "choice_bg": "#ecfdf5", "input_bg": "#ecfdf5", "caption": "#047857", "num": "#16a34a",
        "canvas_bg": "#ecfdf5", "drag_dash": "#86efac", "drag_chip_bg": "#dcfce7", "shadow": "22,101,52",
    },
}

# 学段视觉：中学/高中不用小学糖果色全屏模板
STAGE_THEMES = {
    "middle": {
        "bg": "#f8fafc", "text": "#1e293b", "cover_grad": "#cbd5e1", "h1": "#1e3a8a",
        "card_border": "#cbd5e1", "accent": "#3b82f6", "header": "#1e3a8a",
        "tag_bg": "#dbeafe", "tag_fg": "#1d4ed8", "obj_bg": "#f1f5f9", "choice_border": "#94a3b8",
        "choice_bg": "#f8fafc", "input_bg": "#ffffff", "caption": "#64748b", "num": "#2563eb",
        "canvas_bg": "#f1f5f9", "drag_dash": "#94a3b8", "drag_chip_bg": "#e2e8f0", "shadow": "30,58,138",
        "radius": "14px", "cover_h1": "clamp(26px,4.8vw,42px)", "body_class_extra": "teachany-middle-pro",
    },
    "high": {
        "bg": "#0f172a", "text": "#e2e8f0", "cover_grad": "#334155", "h1": "#93c5fd",
        "card_border": "rgba(148,163,184,0.25)", "accent": "#60a5fa", "header": "#f1f5f9",
        "tag_bg": "rgba(96,165,250,0.15)", "tag_fg": "#93c5fd", "obj_bg": "rgba(30,41,59,0.55)",
        "choice_border": "rgba(148,163,184,0.35)", "choice_bg": "rgba(30,41,59,0.65)",
        "input_bg": "rgba(15,23,42,0.8)", "caption": "#94a3b8", "num": "#60a5fa",
        "canvas_bg": "rgba(30,41,59,0.55)", "drag_dash": "rgba(148,163,184,0.4)",
        "drag_chip_bg": "rgba(51,65,85,0.8)", "shadow": "15,23,42",
        "radius": "12px", "cover_h1": "clamp(24px,4.2vw,38px)", "body_class_extra": "teachany-high-pro",
    },
}


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def resolve_theme(spec: dict) -> dict:
    stage = spec.get("stage", "elementary")
    if stage in STAGE_THEMES:
        t = dict(STAGE_THEMES[stage])
        accent = THEMES.get(spec.get("theme_color", "blue"), {}).get("accent")
        if accent and stage == "middle":
            t["accent"] = accent
            t["num"] = accent
        return t
    return THEMES[spec.get("theme_color", "blue")]


def css(theme: dict) -> str:
    t = theme
    s = t["shadow"]
    radius = t.get("radius", "18px")
    cover_h1 = t.get("cover_h1", "clamp(28px,5.5vw,48px)")
    card_bg = "#fff" if t.get("bg", "#fff") != "#0f172a" else "rgba(30,41,59,0.65)"
    return f"""<style>
*{{box-sizing:border-box}}html,body{{margin:0}}
body{{background:{t['bg']};color:{t['text']};font-family:-apple-system,"PingFang SC",sans-serif;line-height:1.8}}
.slide-container{{height:100dvh;overflow-y:auto;scroll-snap-type:y proximity}}
.slide-page{{min-height:100dvh;display:flex;flex-direction:column;justify-content:center;align-items:center;padding:24px;scroll-snap-align:start}}
.slide-inner{{max-width:900px;width:100%;margin:0 auto}}
.slide-page[data-page-type=cover]{{text-align:center;background:radial-gradient(ellipse at 30% 20%,{t['cover_grad']},transparent 55%)}}
.slide-page[data-page-type=cover] h1{{font-size:{cover_h1};color:{t['h1']};margin:0 0 14px;font-weight:800}}
.card{{background:{card_bg};border:1px solid {t['card_border']};border-radius:{radius};padding:24px;box-shadow:0 6px 24px rgba({s},.08)}}
.card-accent{{border-top:4px solid {t['accent']}}}.card-glow{{box-shadow:0 6px 30px rgba({s},.18)}}
.section-header{{display:flex;align-items:center;gap:10px;margin-bottom:14px;flex-wrap:wrap}}
.section-header h2{{font-size:clamp(20px,3.6vw,24px);margin:0;color:{t['header']};font-weight:700}}
.phase-tag{{background:{t['tag_bg']};color:{t['tag_fg']};border-radius:999px;padding:4px 12px;font-size:12px;font-weight:700}}
.phase-tag[data-variant=success]{{background:#dcfce7;color:#15803d}}.phase-tag[data-variant=purple]{{background:#ede9fe;color:#6d28d9}}.phase-tag[data-variant=warn]{{background:#fef3c7;color:#b45309}}
.grid{{display:grid;gap:10px}}
.objectives{{list-style:none;padding:0;margin:0;display:grid;gap:10px}}
.objectives li{{background:{t['obj_bg']};border:1px solid {t['card_border']};border-radius:12px;padding:12px 16px}}
.choice{{width:100%;text-align:left;border:1px solid {t['choice_border']};border-radius:12px;background:{t['choice_bg']};color:{t['text']};padding:14px 18px;cursor:pointer;font-size:15px;min-height:44px}}
.choice:hover{{opacity:.92}}.choice.correct{{border-color:#22c55e;background:#dcfce7;color:#14532d}}.choice.wrong{{border-color:#ef4444;background:#fee2e2;color:#7f1d1d}}
input,textarea{{width:100%;border:1px solid {t['choice_border']};border-radius:10px;padding:12px;font-size:15px;background:{t['input_bg']};color:{t['text']};min-height:44px}}
.result{{padding:14px 18px;border-radius:12px;background:#dcfce7;border:1px solid #bbf7d0;margin-top:10px;color:#14532d}}
.result.warn{{background:#fef3c7;border-color:#fde68a;color:#78350f}}
.ta-standard-figure{{margin:18px auto;max-width:640px}}.ta-standard-figure img{{width:100%;border-radius:12px;border:1px solid {t['card_border']}}}
.ta-standard-figure figcaption{{text-align:center;color:{t['caption']};font-size:14px;margin-top:8px}}
.summary-item{{display:flex;gap:10px;padding:12px 16px;border:1px solid {t['card_border']};border-radius:12px;margin-bottom:8px}}
.summary-item .num{{font-weight:800;color:{t['num']}}}
.subtitle{{color:{t['tag_fg']};font-size:clamp(15px,2.8vw,18px);max-width:640px;margin:0 auto}}
.canvas-wrap{{overflow:auto;background:{t['canvas_bg']};border:1px solid {t['card_border']};border-radius:12px;padding:12px;min-height:120px;text-align:center;color:{t['caption']}}}
.phet-wrap{{position:relative;padding-top:62.5%;border-radius:12px;overflow:hidden;background:{t['canvas_bg']};border:1px solid {t['card_border']}}}
.phet-wrap iframe{{position:absolute;top:0;left:0;width:100%;height:100%;border:0}}
.drag-pool,.drop-zone{{display:flex;flex-wrap:wrap;gap:8px;min-height:56px;padding:10px;border:2px dashed {t['drag_dash']};border-radius:12px;background:{t['choice_bg']}}}
.drop-zone{{border-style:solid;min-height:80px;flex-direction:column;align-items:stretch}}
.drag-chip{{display:inline-flex;align-items:center;gap:6px;padding:10px 14px;border-radius:10px;background:{t['drag_chip_bg']};border:2px solid {t['drag_dash']};cursor:grab;font-size:14px;touch-action:none;user-select:none;color:{t['text']}}}
.drag-chip.dragging{{opacity:.55;cursor:grabbing}}.drop-zone h4{{margin:0 0 8px;font-size:14px;color:{t['header']}}}
.map-host{{min-height:360px;border-radius:12px;overflow:hidden;border:1px solid {t['card_border']}}}
#knowledge-graph .section-title{{font-size:clamp(20px,3.6vw,24px);margin:0 0 12px;color:{t['header']}}}
#knowledge-graph [data-teachany-kg]{{min-height:180px}}
</style>"""


def _attr(k: str, v) -> str:
    if k == "id":
        return f'id="{esc(v)}"'
    name = k[5:].replace("_", "-") if k.startswith("data_") else k.replace("_", "-")
    return f'data-{name}="{esc(v)}"'


def slide(section: str, idx: int, page_type: str, tts: str, tsh: str, inner: str, **attrs) -> str:
    extra = " ".join(_attr(k, v) for k, v in attrs.items())
    return (
        f'  <section class="slide-page" data-page-type="{page_type}" data-page-index="{idx}" '
        f'data-tts="{esc(tts)}" data-tsh="{esc(tsh)}"{(" " + extra) if extra else ""}>\n'
        f'    <div class="slide-inner">{inner}</div>\n  </section>'
    )


def card(inner: str, accent=False, glow=False) -> str:
    cls = "card" + (" card-accent" if accent else "") + (" card-glow" if glow else "")
    return f'<div class="{cls}">{inner}</div>'


def quiz_choices(choices: list, correct: int) -> str:
    lines = []
    for i, c in enumerate(choices):
        attr = ' data-correct="0"' if i == correct else ""
        lines.append(f'        <button class="choice"{attr}>{esc(c)}</button>')
    return "\n".join(lines)


def map_config_for(spec: dict) -> dict | None:
    return spec.get("map_config") or default_map_config(spec)


def build_map_inner(spec: dict, cfg: dict) -> str:
    nid = spec["node_id"]
    map_id = "thm-" + re.sub(r"[^a-z0-9-]+", "-", nid.lower())[:40]
    config_json = json.dumps({
        "eras": cfg["eras"],
        "center": cfg.get("center", [34, 108]),
        "zoom": cfg.get("zoom", 4),
        "fitBounds": cfg.get("fitBounds"),
        "minZoom": cfg.get("minZoom", 2),
        "maxZoom": cfg.get("maxZoom", 8),
        **({"overlays": cfg["overlays"]} if cfg.get("overlays") else {}),
        **({"terrain": cfg.get("terrain", True)} if cfg.get("terrain") is not False else {}),
    }, ensure_ascii=False, indent=2)
    scope = cfg.get("scope", "china")
    hint = "点击时代/图层按钮切换地图；悬停边界，点击城市标记查看说明。" if scope == "china" else "点击时代按钮切换世界格局；结合本课主题观察空间分布。"
    return (
        f'<div class="section-header"><span class="phase-tag" data-variant="success">Map</span>'
        f'<h2>{esc(cfg["title"])}</h2></div>'
        f'<p style="margin:0 0 12px;color:inherit;opacity:.85">{esc(hint)}</p>'
        f'<div class="map-host" data-teachany-map="{map_id}" data-teachany-map-scope="{esc(scope)}" '
        f'data-teachany-map-title="{esc(cfg["title"])}">'
        f'<script type="application/json" data-teachany-map-config>\n{config_json}\n</script>'
        f'</div>'
    )


def prepare_map_assets(course_dir: Path, cfg: dict) -> dict:
    """Resolve geojson paths and copy map assets before embedding config in HTML."""
    cfg = json.loads(json.dumps(cfg))
    _apply_maps.ensure_map_projection_defaults(cfg)
    _apply_maps.copy_geojson_files(course_dir, cfg.get("scope", "china"), cfg["eras"])
    _apply_maps.copy_overlay_files(course_dir, cfg.get("overlays", []))
    return cfg


def build_html(spec: dict) -> str:
    nid = spec["node_id"]
    grade = spec["grade"]
    theme = resolve_theme(spec)
    hero = "./assets/hero-infographic.svg"
    pages: list[str] = []
    idx = 0

    # cover
    pages.append(slide("cover", idx, "cover", "hero", f"开场 - {spec['title']}",
        card(f'<h1>{esc(spec["title"])}</h1><p class="subtitle">{esc(spec["subtitle"])}</p>'
             f'<figure class="ta-standard-figure" style="margin-top:28px">'
             f'<img class="hero-cover-img" src="{hero}" alt="{esc(spec["title"])}">'
             f'<figcaption>{esc(spec.get("hero_caption", spec["title"] + "知识全景"))}</figcaption></figure>', glow=True)))
    idx += 1

    # problem anchor (4 choices)
    pa = spec["problem_anchor"]
    choices_html = "\n".join(
        f'          <button class="choice" data-anchor-choice="{esc(c)}">{esc(c)}</button>'
        for c in pa["choices"]
    )
    pages.append(slide("anchor", idx, "interactive", "problem-anchor", "问题锚点",
        card(f'<div class="section-header"><span class="phase-tag">Problem Anchor</span>'
             f'<h2>{esc(pa.get("prompt", "今天你最想弄懂哪个问题？"))}</h2></div>'
             f'<div class="grid" id="problem-anchor-choices">\n{choices_html}\n      </div>'
             f'<label style="display:block;margin-top:16px;color:{theme["caption"]};font-size:14px">或者写下你自己的问题'
             f'<input id="learner-question-input" placeholder="把你的疑问写在这里"></label>'
             f'<p id="anchor-feedback" class="result warn" style="margin-top:14px">选择或输入后，这节课会围绕你的问题展开。</p>',
             accent=True)))
    idx += 1

    # objectives
    obj_li = "\n".join(f'          <li data-bloom-level="{i+1}">{esc(o)}</li>' for i, o in enumerate(spec["objectives"]))
    pages.append(slide("obj", idx, "objectives", "objectives", "学习目标",
        card(f'<div class="section-header"><span class="phase-tag" data-variant="success">Objectives</span><h2>学习目标</h2></div>'
             f'<ul class="objectives">\n{obj_li}\n      </ul>')))
    idx += 1

    # pretest
    pre = spec["pretest"]
    pages.append(slide("pre", idx, "quiz", "pretest", "前测",
        card(f'<div class="section-header"><span class="phase-tag" data-variant="warn">Pretest</span><h2>课前小诊断</h2></div>'
             f'<p style="margin:0 0 14px">{esc(pre["question"])}</p>'
             f'<div class="grid" id="pre-choices">\n{quiz_choices(pre["choices"], pre["correct"])}\n      </div>'
             f'<p id="pre-fb" class="result warn" style="margin-top:14px">先选一个，错了正好暴露你的前概念，我们一起纠正。</p>',
             accent=True), id="pre-test", data_bloom_level="1", data_scaffold="full", data_conceptest="true"))
    idx += 1

    # concept sections (first = concept, rest = examples)
    sections = spec["sections"]
    for si, sec in enumerate(sections):
        ptype = "concept" if si == 0 else "concept"
        tag = "Concept" if si == 0 else "Examples"
        paras = "".join(f"<p>{p}</p>" for p in sec["paragraphs"])
        img_block = ""
        if sec.get("image"):
            img_block = (f'<figure class="ta-standard-figure"><img src="./assets/{esc(sec["image"])}" '
                         f'alt="{esc(sec.get("caption", sec["title"]))}">'
                         f'<figcaption>{esc(sec.get("caption", ""))}</figcaption></figure>')
        page_type = "concept" if si == 0 else "concept"
        pages.append(slide(f"sec{si}", idx, page_type, sec.get("tts", f"section-{si}"), sec.get("tsh", sec["title"]),
            card(f'<div class="section-header"><span class="phase-tag">{tag if si == 0 else "Examples"}</span>'
                 f'<h2>{esc(sec["title"])}</h2></div>{paras}{img_block}',
                 accent=(si == 0)), data_bloom_level=str(min(si + 2, 4)), data_scaffold="full" if si == 0 else "partial"))
        idx += 1

    map_cfg = map_config_for(spec)
    if map_cfg:
        pages.append(slide("map", idx, "interactive", "map-explore", "地图探究",
            card(build_map_inner(spec, map_cfg), glow=True),
            data_bloom_level="3", data_scaffold="partial"))
        idx += 1

    # PhET
    if spec.get("phet_slug"):
        slug = spec["phet_slug"]
        pages.append(slide("phet", idx, "interactive", f"phet-{slug}", f"PhET - {spec.get('phet_title', slug)}",
            card(f'<div class="section-header"><span class="phase-tag" data-variant="success">🔬 PhET 模拟</span>'
                 f'<h2>{esc(spec.get("phet_title", slug))}</h2></div>'
                 f'<p style="margin:0 0 12px">{esc(spec.get("phet_intro", "在模拟中动手探索，联系本课核心概念。"))}</p>'
                 f'<div class="phet-wrap"><iframe src="https://phet.colorado.edu/sims/html/{slug}/latest/{slug}_zh_CN.html" '
                 f'allowfullscreen loading="lazy" sandbox="allow-scripts allow-same-origin allow-forms allow-popups" '
                 f'title="PhET {esc(spec.get("phet_title", slug))}"></iframe></div>'
                 f'<p style="font-size:13px;color:{theme["caption"]};margin-top:8px">💡 {esc(spec.get("phet_hint", ""))}</p>',
                 glow=True), data_bloom_level="3", data_scaffold="partial", data_conceptest="true"))
        idx += 1

    # drag activity or canvas placeholder
    drag = spec.get("drag_activity")
    if drag:
        items_html = "\n".join(
            f'        <span class="drag-chip" draggable="true" data-zone="{esc(it["zone"])}">{esc(it["label"])}</span>'
            for it in drag["items"]
        )
        cols = drag.get("zone_columns", "repeat(auto-fit,minmax(180px,1fr))")
        zones_html = "\n".join(
            f'        <div class="drop-zone" data-accept="{esc(z["id"])}"><h4>{esc(z["label"])}</h4></div>'
            for z in drag["zones"]
        )
        pages.append(slide("drag", idx, "interactive", "drag-activity", drag.get("tsh", "拖拽互动"),
            card(f'<div class="section-header"><span class="phase-tag" data-variant="success">Interactive</span>'
                 f'<h2>{esc(drag["title"])}</h2></div>'
                 f'<p style="margin:0 0 12px">{drag.get("instruction", "把卡片拖到正确位置。")}</p>'
                 f'<div class="drag-pool" id="drag-pool" aria-label="待拖动项">\n{items_html}\n      </div>'
                 f'<div class="grid" style="grid-template-columns:{cols};gap:10px;margin-top:14px">\n{zones_html}\n      </div>'
                 f'<p id="drag-readout" class="result warn" style="margin-top:12px">{esc(drag.get("pending_msg", "全部拖完后自动判分。"))}</p>',
                 glow=True), data_bloom_level="3", data_scaffold="partial"))
        idx += 1
    elif not spec.get("phet_slug"):
        pages.append(slide("canvas", idx, "interactive", "interactive-canvas", "互动探究",
            card(f'<div class="section-header"><span class="phase-tag" data-variant="success">Interactive</span>'
                 f'<h2>{esc(spec.get("canvas_title", "动手探究"))}</h2></div>'
                 f'<p style="margin:0 0 12px">{esc(spec.get("canvas_hint", "此处可嵌入 Canvas 探究动画。"))}</p>'
                 f'<div class="canvas-wrap"><p>🎨 Canvas 互动占位 — 待 agnes / 后续注入</p></div>',
                 glow=True), data_bloom_level="3", data_scaffold="partial"))
        idx += 1

    # practice
    pr = spec["practice"]
    pages.append(slide("practice", idx, "quiz", "practice", "练习",
        card(f'<div class="section-header"><span class="phase-tag" data-variant="purple">Practice</span>'
             f'<h2>{esc(pr.get("title", "用学到的知识解释"))}</h2></div>'
             f'<p style="margin:0 0 10px"><strong>解释题：</strong>{esc(pr["explain_prompt"])}</p>'
             f'<textarea id="explain" placeholder="{esc(pr.get("explain_placeholder", "写下你的解释…"))}"></textarea>'
             f'<button class="choice" id="show-fb" style="margin-top:10px">看看老师的提示</button>'
             f'<p id="practice-fb" class="result" style="margin-top:12px;display:none">{pr["hint"]}</p>'
             + (f'<p style="margin:14px 0 6px"><strong>拓展题：</strong>{esc(pr["extra_prompt"])}</p>'
                f'<textarea id="design" placeholder="{esc(pr.get("extra_placeholder", ""))}"></textarea>' if pr.get("extra_prompt") else ""),
             accent=True), data_bloom_level="4", data_scaffold="none"))
    idx += 1

    # posttest
    post = spec["posttest"]
    pages.append(slide("post", idx, "quiz", "posttest", "后测",
        card(f'<div class="section-header"><span class="phase-tag" data-variant="warn">Posttest</span><h2>达标检测</h2></div>'
             f'<p style="margin:0 0 12px">{esc(post["question"])}</p>'
             f'<div class="grid" id="post-choices">\n{quiz_choices(post["choices"], post["correct"])}\n      </div>'
             f'<p id="post-fb" class="result" style="margin-top:12px">选一个并查看反馈。</p>'),
        id="post-test", data_bloom_level="3", data_scaffold="none", data_conceptest="true"))
    idx += 1

    # summary
    sm = spec["summary"]
    items = "".join(f'      <div class="summary-item"><span class="num">{i+1}</span><div>{s}</div></div>\n'
                    for i, s in enumerate(sm["items"]))

    pages.append(slide("kg", idx, "concept", "knowledge-graph", "知识图谱",
        card(
            f'<section class="section" id="knowledge-graph">'
            f'<h2 class="section-title">🧠 知识图谱：{esc(spec["title"])}</h2>'
            f'<div data-teachany-kg="{esc(nid)}"></div></section>',
            glow=True),
        data_bloom_level="2", data_scaffold="full"))
    idx += 1

    pages.append(slide("sum", idx, "summary", "summary", "总结迁移",
        card(f'<div class="section-header"><span class="phase-tag" data-variant="success">Summary</span>'
             f'<h2>这节课我们学会了</h2></div>\n{items}'
             f'<p style="margin-top:16px"><strong>迁移任务：</strong>{esc(sm["transfer"])}</p>', glow=True),
        data_bloom_level="2", data_scaffold="full"))

    # JS
    pre_fb = spec["pretest"]
    post_fb = spec["posttest"]
    drag_js = ""
    if drag:
        total = len(drag["items"])
        drag_js = f"""
  var pool=document.getElementById('drag-pool'), dragOut=document.getElementById('drag-readout');
  var placed=0, total={total};
  function scoreDrag(){{
    if(placed<total) return;
    var wrong=document.querySelectorAll('.drop-zone .drag-chip.wrong').length;
    if(!dragOut) return;
    if(wrong===0){{dragOut.textContent={json.dumps(drag.get("ok_msg", "全部正确！"), ensure_ascii=False)}; dragOut.className='result'}}
    else{{dragOut.textContent={json.dumps(drag.get("bad_msg", "还有放错的，再想想。"), ensure_ascii=False)}; dragOut.className='result warn'}}
  }}
  document.querySelectorAll('.drag-chip[draggable]').forEach(function(chip){{
    chip.addEventListener('dragstart',function(e){{e.dataTransfer.setData('text/plain',chip.getAttribute('data-zone')); chip.classList.add('dragging')}});
    chip.addEventListener('dragend',function(){{chip.classList.remove('dragging')}});
    chip.addEventListener('click',function(){{document.querySelectorAll('.drag-chip').forEach(function(c){{c.classList.remove('selected')}}); chip.classList.add('selected'); window._selectedChip=chip}});
  }});
  document.querySelectorAll('.drop-zone').forEach(function(zone){{
    zone.addEventListener('dragover',function(e){{e.preventDefault(); zone.style.opacity='0.85'}});
    zone.addEventListener('dragleave',function(){{zone.style.opacity=''}});
    zone.addEventListener('drop',function(e){{
      e.preventDefault(); zone.style.opacity='';
      var type=e.dataTransfer.getData('text/plain');
      var chip=document.querySelector('.drag-chip.dragging')||document.querySelector('.drag-chip[data-zone="'+type+'"]:not(.placed)');
      if(!chip||chip.parentElement===zone) return;
      if(chip.parentElement.classList.contains('drop-zone')) placed--;
      zone.appendChild(chip); chip.classList.add('placed');
      chip.classList.toggle('wrong', type!==zone.getAttribute('data-accept'));
      chip.classList.toggle('correct', type===zone.getAttribute('data-accept'));
      if(chip.parentElement===zone && !chip.dataset.counted){{placed++; chip.dataset.counted='1'}}
      scoreDrag();
    }});
    zone.addEventListener('click',function(){{
      if(!window._selectedChip) return;
      var chip=window._selectedChip, type=chip.getAttribute('data-zone');
      if(chip.parentElement.classList.contains('drop-zone')) placed--;
      zone.appendChild(chip); chip.classList.add('placed');
      chip.classList.toggle('wrong', type!==zone.getAttribute('data-accept'));
      chip.classList.toggle('correct', type===zone.getAttribute('data-accept'));
      if(chip.parentElement===zone && !chip.dataset.counted){{placed++; chip.dataset.counted='1'}}
      window._selectedChip=null; document.querySelectorAll('.drag-chip').forEach(function(c){{c.classList.remove('selected')}});
      scoreDrag();
    }});
  }});"""

    body_js = f"""<script>
(function(){{
  function wire(group, fbId, okMsg, badMsg){{
    var box=document.getElementById(group); if(!box) return;
    box.querySelectorAll('.choice').forEach(function(b){{
      b.addEventListener('click',function(){{
        box.querySelectorAll('.choice').forEach(function(x){{x.classList.remove('correct','wrong')}});
        var ok=b.hasAttribute('data-correct'); b.classList.add(ok?'correct':'wrong');
        var fb=document.getElementById(fbId); if(fb){{fb.textContent=ok?okMsg:badMsg; fb.className='result'+(ok?'':' warn')}}
      }});
    }});
  }}
  wire('pre-choices','pre-fb',{json.dumps(pre_fb.get("ok_msg",""), ensure_ascii=False)},{json.dumps(pre_fb.get("bad_msg",""), ensure_ascii=False)});
  wire('post-choices','post-fb',{json.dumps(post_fb.get("ok_msg",""), ensure_ascii=False)},{json.dumps(post_fb.get("bad_msg",""), ensure_ascii=False)});
  var sf=document.getElementById('show-fb'),pf=document.getElementById('practice-fb');
  if(sf&&pf) sf.addEventListener('click',function(){{pf.style.display='block'}});
{drag_js}
  window.__TEACHANY_LEARNER_QUESTION__='';
  document.querySelectorAll('[data-anchor-choice]').forEach(function(b){{
    b.addEventListener('click',function(){{
      document.querySelectorAll('[data-anchor-choice]').forEach(function(x){{x.classList.remove('correct')}});
      b.classList.add('correct');
      window.__TEACHANY_LEARNER_QUESTION__=b.getAttribute('data-anchor-choice');
      var fb=document.getElementById('anchor-feedback'); if(fb) fb.textContent='你的问题：'+window.__TEACHANY_LEARNER_QUESTION__;
    }});
  }});
  var inp=document.getElementById('learner-question-input');
  if(inp) inp.addEventListener('input',function(e){{window.__TEACHANY_LEARNER_QUESTION__=e.target.value}});
}})();
</script>"""

    desc = spec.get("description", spec["subtitle"])
    subject = spec.get("subject", "science")
    stage = spec.get("stage", "elementary")
    stage_cn = STAGE_LABEL.get(stage, stage)
    subj_cn = SUBJECT_LABEL.get(subject, subject)
    lesson = spec.get("lesson_type", "concept-inquiry")
    body_cls = f"teachany-{stage}"
    if theme.get("body_class_extra"):
        body_cls += f" {theme['body_class_extra']}"
    head_map = ""
    if map_cfg:
        head_map = '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">\n'
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{esc(spec["title"])} · {stage_cn}{subj_cn} G{grade} · TeachAny v7.20</title>
<meta name="description" content="{esc(desc)}">
<meta name="course-id" content="{esc(nid)}">
<meta name="course-title" content="{esc(spec["title"])}">
<meta name="course-subject" content="{esc(subject)}">
<meta name="course-grade" content="{esc(stage)}-{grade}">
<meta name="teachany-node" content="{esc(nid)}">
<meta name="teachany-subject" content="{esc(subject)}">
<meta name="teachany-grade" content="{grade}">
<meta name="teachany-stage" content="{esc(stage)}">
<meta name="teachany-lesson-type" content="{esc(lesson)}">
<meta name="teachany-version" content="{TEACHANY_VERSION}">
<meta name="teachany-template-version" content="2.1">
{css(theme)}
{head_map}</head>
<body class="{body_cls}">
<div class="slide-container" id="slide-container">
{chr(10).join(pages)}
</div>
{body_js}
</body>
</html>
"""


def build_manifest(spec: dict) -> dict:
    nid = spec["node_id"]
    pwd = spec["password_hint"]
    images = ["assets/hero-infographic.svg", "assets/concept-diagram.svg", "assets/process-diagram.svg"]
    return {
        "id": nid, "course_id": nid, "node_id": nid,
        "name": spec["title"], "name_en": spec.get("name_en", spec["title"]),
        "subject": spec.get("subject", "science"), "grade": str(spec["grade"]),
        "stage": spec.get("stage", "elementary"),
        "domain": spec.get("domain", spec.get("subject", "general")),
        "lesson_type": spec.get("lesson_type", "concept-inquiry"), "status": "community", "author": "TeachAny",
        "version": "1.0.0", "teachany_version": TEACHANY_VERSION, "template_version": "2.0",
        "curriculum": spec.get("curriculum", "义务教育科学课程标准（2022年版）"),
        "description": spec.get("description", spec["subtitle"]),
        "tags": spec.get("tags", []),
        "learning_objectives": spec["objectives"],
        "assets": {"hero": "assets/hero-infographic.svg", "images": images},
        "has_tts": False, "has_phet": bool(spec.get("phet_slug")),
        "has_drag": bool(spec.get("drag_activity")),
        "feedback": {
            "require_password": True,
            "password_sha256": hashlib.sha256(pwd.encode()).hexdigest(),
            "password_hint": pwd,
        },
        "created_at": str(date.today()), "updated_at": str(date.today()),
    }


def build_plan(spec: dict) -> str:
    nid = spec["node_id"]
    parts = ["问题锚点", "前测"] + [s["title"] for s in spec["sections"]]
    if spec.get("phet_slug"):
        parts.append(f"PhET({spec['phet_slug']})")
    if spec.get("drag_activity"):
        parts.append("拖拽互动")
    parts += ["练习", "后测", "总结迁移"]
    chain = "→".join(parts)
    interact = spec.get("drag_activity", {}).get("title") or spec.get("phet_title") or "Canvas占位"
    stage = spec.get("stage", "elementary")
    subj = SUBJECT_LABEL.get(spec.get("subject", "science"), spec.get("subject", ""))
    stage_cn = STAGE_LABEL.get(stage, stage)
    return f"""# {nid} · {spec["title"]}（{stage_cn}{subj} G{spec["grade"]}）

- 课型：概念探究
- 闭环：{chain}
- 互动：{interact}
- 三模块由 finalize-courseware.py self-contained 注入
- 反馈密码：{spec["password_hint"]}
"""


def ensure_cn_svgs(out: Path, spec: dict) -> None:
    """Ensure standard SVG illustrations exist (idempotent)."""
    assets = out / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    title = spec.get("title", spec.get("node_id", "课件"))

    def svg(subtitle: str) -> str:
        t = html.escape(title[:40])
        s = html.escape(subtitle[:56])
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 540">'
            f'<rect width="960" height="540" fill="#eff6ff"/>'
            f'<text x="48" y="96" fill="#1e3a8a" font-size="34" font-weight="800">{t}</text>'
            f'<text x="48" y="150" fill="#475569" font-size="22">{s}</text>'
            f"</svg>"
        )

    defaults = {
        "hero-infographic.svg": svg("知识结构图"),
        "concept-diagram.svg": svg("核心概念示意"),
        "process-diagram.svg": svg("过程机制示意"),
    }
    for name, content in defaults.items():
        path = assets / name
        if not path.is_file():
            path.write_text(content, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Build CN courseware from JSON spec")
    ap.add_argument("--spec", required=True, help="Path to spec JSON")
    args = ap.parse_args()
    spec_path = Path(args.spec).resolve()
    if not spec_path.is_file():
        print(f"Spec not found: {spec_path}", file=sys.stderr)
        return 2
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    nid = spec["node_id"]
    out = COMMUNITY / nid
    out.mkdir(parents=True, exist_ok=True)
    map_cfg = map_config_for(spec)
    if map_cfg:
        spec["map_config"] = prepare_map_assets(out, map_cfg)
    (out / "index.html").write_text(build_html(spec), encoding="utf-8")
    (out / "manifest.json").write_text(json.dumps(build_manifest(spec), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "PLAN.md").write_text(build_plan(spec), encoding="utf-8")
    ensure_cn_svgs(out, spec)
    print(f"Built {out}/")
    print(f"  index.html  manifest.json  PLAN.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
