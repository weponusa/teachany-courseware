#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TeachAny · finalize-courseware.py (v7.20)

课件「定稿器」——发布前强制补齐三大高频缺失模块，让 AI 漏写也能自动补全：

  ① AI 学伴      ai-tutor.{css,js} + tutor-card + __TEACHANY_TUTOR_CONFIG__
  ② 高质量音频   每个 data-tts 段落生成真实分段 mp3（tts-engine 多引擎）
                 + tts/manifest.json + data-teachany-audio-playlist 配置块
  ③ 知识图谱     data-teachany-kg + teachany-knowledge-graph.{css,js}

设计原则：
  - 幂等：已存在的模块/音频不重复生成
  - 真实音频：调 tts-engine.py（edge-tts→say→pyttsx3→silent），校验 ≥ MIN_MP3
  - 不改业务内容，只补模块与音频接线

用法：
  python3 scripts/finalize-courseware.py <课件目录>
  python3 scripts/finalize-courseware.py <课件目录> --no-audio   # 只补模块，不生成音频
  python3 scripts/finalize-courseware.py <课件目录> --json

退出码：
  0  定稿完成（模块齐全；音频已生成或本就齐全）
  1  存在无法自动修复的问题（如音频引擎全部失败）
  2  输入错误
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
import time
from html import escape as html_escape, unescape
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
MIN_MP3 = 5 * 1024  # 低于 5KB 视为静音/占位
MAX_NARRATION = 320  # 单段朗读文本上限（字符）

VOICE_BY_SUBJECT = {
    "english": "en-US-AriaNeural",
    "chinese": "zh-CN-XiaoyiNeural",
}
DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"


def voice_for_text(subject: str, text: str) -> str:
    """按旁白文本语言选音色，避免英语课中文 hero 段用英文 Neural 语音合成失败。"""
    if re.search(r"[\u4e00-\u9fff]", text):
        return VOICE_BY_SUBJECT.get("chinese", DEFAULT_VOICE)
    subj = (subject or "").lower()
    return VOICE_BY_SUBJECT.get(subj, DEFAULT_VOICE)

# 标准模块文件（self-contained 时复制到课件 assets/scripts/，确保挂树后必可加载）
STANDARD_MODULES = [
    "ai-tutor.css", "ai-tutor.js",
    "teachany-tutor-card.css", "teachany-tutor-card.js",
    "teachany-tts-narrator.css", "teachany-tts-narrator.js",
    "teachany-section-hints.css", "teachany-section-hints.js",
    "teachany-knowledge-graph.css", "teachany-knowledge-graph.js",
    "teachany-audio-player.css", "teachany-audio-player.js",
    "teachany-floating-dock.css",
]
MAP_MODULES = ["teachany-historical-map.css", "teachany-historical-map.js"]
LEAFLET_CSS = '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">'
LEAFLET_JS = '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>'


def modules_for_html(html: str) -> list[str]:
    mods = list(STANDARD_MODULES)
    if "data-teachany-map" in html:
        mods.extend(MAP_MODULES)
    return mods


def ensure_map_assets(html: str) -> tuple[str, list[str]]:
    if "data-teachany-map" not in html:
        return html, []
    actions: list[str] = []
    if "leaflet@1.9.4" not in html and "</head>" in html:
        html = html.replace("</head>", f"{LEAFLET_CSS}\n</head>", 1)
        actions.append("leaflet-css")
    hist_css = "./assets/scripts/teachany-historical-map.css"
    if hist_css not in html and "teachany-historical-map.css" not in html and "</head>" in html:
        html = html.replace("</head>", f'  <link rel="stylesheet" href="{hist_css}">\n</head>', 1)
        actions.append("historical-map-css")
    if "leaflet@1.9.4/dist/leaflet.js" not in html:
        marker = '<script src="./assets/scripts/teachany-knowledge-graph.js"'
        hist_js = f'{LEAFLET_JS}\n<script src="./assets/scripts/teachany-historical-map.js" defer></script>\n'
        if marker in html:
            html = html.replace(marker, hist_js + marker, 1)
            actions.append("historical-map-js")
        elif "</body>" in html:
            html = html.replace("</body>", hist_js + "</body>", 1)
            actions.append("historical-map-js")
    return html, actions


def find_module_source(course_dir: Path) -> Path | None:
    """定位标准模块源目录（courseware 仓根 assets/scripts）。"""
    cands = [
        course_dir.parent.parent / "assets" / "scripts",   # community/<id> → repo/assets/scripts
        Path.cwd() / "assets" / "scripts",
        Path.home() / "CodeBuddy" / "一次函数" / "teachany-courseware" / "assets" / "scripts",
    ]
    for c in cands:
        if (c / "ai-tutor.js").is_file():
            return c.resolve()
    return None


def make_self_contained(course_dir: Path, html: str) -> tuple[str, dict]:
    """把标准模块复制进课件 assets/scripts/，并将 ../../assets/scripts/ 引用改为 ./assets/scripts/。

    这是挂树发布后模块「必定可加载」的唯一可靠方式（不依赖仓根相对路径与部署布局）。
    """
    report = {"copied": [], "missing_source": False, "rewrote": 0}
    src = find_module_source(course_dir)
    if not src:
        report["missing_source"] = True
        return html, report

    dest = course_dir / "assets" / "scripts"
    dest.mkdir(parents=True, exist_ok=True)
    import shutil
    for name in modules_for_html(html):
        s = src / name
        d = dest / name
        if not s.is_file():
            continue
        if (not d.exists()) or d.stat().st_size != s.stat().st_size:
            shutil.copy2(s, d)
            report["copied"].append(name)

    # 引用路径：先统一为课件相对路径，再改为 teachany.cn 站点根 /assets/scripts/（CDN 必达）
    new_html, n1 = re.subn(r'(?:\.\./)+assets/scripts/', './assets/scripts/', html)
    new_html, n2 = re.subn(r'(?:\.\./)+scripts/', './assets/scripts/', new_html)
    new_html, n3 = re.subn(r'\./assets/scripts/', '/assets/scripts/', new_html)
    report["rewrote"] = n1 + n2 + n3
    return new_html, report


ORPHAN_KG_RE = re.compile(
    r"\n<!-- v7\.7\.4 标准知识图谱模块 -->\s*"
    r'<section class="section" id="knowledge-graph"[^>]*>[\s\S]*?</section>\s*',
    re.I,
)


def needs_kg_slide(html: str) -> bool:
    return 'id="slide-container"' in html and 'data-tts="knowledge-graph"' not in html


def patch_kg_slide(html: str, node_id: str, title: str) -> tuple[str, bool]:
    if not needs_kg_slide(html) or not node_id:
        return html, False
    safe_title = html_escape(title, quote=True)
    safe_nid = html_escape(node_id, quote=True)
    slide = (
        f'  <section class="slide-page" data-page-type="concept" data-page-index="98" '
        f'data-tts="knowledge-graph" data-tsh="知识图谱" data-bloom-level="2" data-scaffold="full">\n'
        f'    <div class="slide-inner"><div class="card card-glow">'
        f'<section class="section" id="knowledge-graph">'
        f'<h2 class="section-title">🧠 知识图谱：{safe_title}</h2>'
        f'<div data-teachany-kg="{safe_nid}"></div>'
        f'</section></div></div>\n  </section>\n'
    )
    m = re.search(r'<section class="slide-page"[^>]*\bdata-tts="summary"', html)
    if m:
        html = html[: m.start()] + slide + html[m.start() :]
    else:
        anchor = html.find('id="slide-container"')
        close = html.find("</div>", anchor) if anchor != -1 else -1
        while close != -1:
            tail = html[close : close + 200]
            if "<script" in tail[:20] or '<section class="slide-page"' in tail:
                close = html.find("</div>", close + 6)
                continue
            html = html[:close] + "\n" + slide + html[close:]
            break
    if 'data-tts="knowledge-graph"' in html:
        html = ORPHAN_KG_RE.sub("\n", html, count=1)
    return html, True


def ensure_hist_geo_map(course_dir: Path, html: str, manifest: dict, maps_mod, map_mod) -> tuple[str, str | None]:
    subj = (manifest.get("subject") or "").lower()
    if subj not in ("history", "geography"):
        return html, None
    if "data-teachany-map" in html:
        return html, None
    if re.search(r"L\.tileLayer\s*\(", html) and re.search(r"fitBounds|setView", html):
        return html, None
    hist_manifest_path = SCRIPT_DIR / "historical-maps-manifest.json"
    hist_manifest = {}
    if hist_manifest_path.is_file():
        hist_manifest = json.loads(hist_manifest_path.read_text(encoding="utf-8"))
    rel = f"community/{course_dir.name}"
    cfg = hist_manifest.get(rel) or hist_manifest.get(f"examples/{course_dir.name}")
    if cfg and cfg.get("skip"):
        return html, None
    if not cfg:
        pseudo = {
            "node_id": manifest.get("node_id") or course_dir.name,
            "title": manifest.get("name") or course_dir.name,
            "subject": subj,
            "stage": manifest.get("stage") or "middle",
            "grade": manifest.get("grade") or 8,
        }
        cfg = map_mod.default_map_config(pseudo)
    if not cfg:
        return html, None
    cfg = json.loads(json.dumps(cfg))
    maps_mod.ensure_map_projection_defaults(cfg)
    maps_mod.copy_geojson_files(course_dir, cfg.get("scope", "china"), cfg["eras"])
    maps_mod.copy_overlay_files(course_dir, cfg.get("overlays", []))
    html = maps_mod.inject_head(html)
    html = maps_mod.inject_script_bottom(html)
    block = maps_mod.build_section(rel, cfg)
    injected = False
    if 'id="slide-container"' in html:
        m = re.search(r'<section class="slide-page"[^>]*\bdata-tts="summary"', html)
        if m:
            map_slide = (
                f'  <section class="slide-page" data-page-type="interactive" data-page-index="97" '
                f'data-tts="map-explore" data-tsh="地图探究">\n'
                f'    <div class="slide-inner"><div class="card card-glow">{block.strip()}</div></div>\n'
                f'  </section>\n'
            )
            html = html[: m.start()] + map_slide + html[m.start() :]
            injected = True
    if not injected:
        html, injected = maps_mod.inject_section(html, block)
    if injected:
        return html, "map-injected"
    return html, None


def _load_apply_maps():
    path = SCRIPT_DIR / "apply-historical-maps.py"
    spec = importlib.util.spec_from_file_location("apply_maps", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


FALLBACK_KG_NODES = {
    "sci-e-3d-printing-blender": "sci-e-design-process",
}


def normalize_kg_node_id(course_dir: Path, html: str, manifest: dict) -> tuple[str, str | None]:
    """Align all data-teachany-kg ids with manifest node_id when missing from KG manifest."""
    ids = re.findall(r'data-teachany-kg=["\']([^"\']+)["\']', html, re.I)
    if not ids:
        return html, None
    src_root = find_module_source(course_dir)
    if not src_root:
        return html, None
    mf = src_root / "teachany-kg-manifest.json"
    if not mf.is_file():
        return html, None
    try:
        kg = json.loads(mf.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return html, None
    nodes = kg.get("nodes") or {}
    if all(i in nodes for i in set(ids)):
        return html, None

    target = manifest.get("node_id") or manifest.get("id") or manifest.get("courseId")
    if not target or target not in nodes:
        cid = course_dir.name
        for nid, node in nodes.items():
            for c in node.get("courses") or []:
                if c.get("id") == cid or c.get("path", "").endswith(cid):
                    target = nid
                    break
            if target and target in nodes:
                break
    if not target or target not in nodes:
        fb = FALLBACK_KG_NODES.get(course_dir.name)
        if fb and fb in nodes:
            target = fb
    if not target or target not in nodes:
        return html, None

    fixes = []
    for kid in sorted(set(ids)):
        if kid in nodes:
            continue
        html = html.replace(f'data-teachany-kg="{kid}"', f'data-teachany-kg="{target}"')
        html = html.replace(f"data-teachany-kg='{kid}'", f"data-teachany-kg='{target}'")
        fixes.append(f"{kid}->{target}")
    return html, ", ".join(fixes) if fixes else None


def _load_cn_map_config():
    path = SCRIPT_DIR / "cn-map-config.py"
    spec = importlib.util.spec_from_file_location("cn_map_config", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ensure_kg_manifest(course_dir: Path, html: str) -> tuple[str, list[str]]:
    """KG manifest 走站点根 /assets/scripts/（CDN），不再复制 300KB+ 副本进每课目录。"""
    return html, []


def _load_apply_modules():
    """以 importlib 加载 apply-standard-modules.py（文件名带连字符，不能直接 import）。"""
    path = SCRIPT_DIR / "apply-standard-modules.py"
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location("apply_standard_modules", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def strip_tags(html: str) -> str:
    html = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<[^>]+>", " ", html)
    html = unescape(html)
    return re.sub(r"\s+", " ", html).strip()


def find_tts_sections(html: str) -> list[dict]:
    """返回每个 data-tts 段落：{tts, label, text}。"""
    sections = []
    for m in re.finditer(r'<section\b[^>]*\bdata-tts=["\']([^"\']+)["\'][^>]*>', html, re.I):
        open_tag = m.group(0)
        tts_id = m.group(1)
        # 优先 data-tts-script（作者手写朗读稿），其次 data-tsh（情境提示）
        script_m = re.search(r'data-tts-script=["\']([^"\']+)["\']', open_tag, re.I)
        tsh_m = re.search(r'data-tsh=["\']([^"\']+)["\']', open_tag, re.I)
        # 抓 section 内容
        start = m.end()
        depth = 1
        i = start
        body_end = len(html)
        open_re = re.compile(r"<section\b", re.I)
        close_re = re.compile(r"</section>", re.I)
        while i < len(html):
            om = open_re.search(html, i)
            cm = close_re.search(html, i)
            if not cm:
                break
            if om and om.start() < cm.start():
                depth += 1
                i = om.end()
            else:
                depth -= 1
                if depth == 0:
                    body_end = cm.start()
                    break
                i = cm.end()
        inner = html[start:body_end]

        if script_m:
            text = unescape(script_m.group(1)).strip()
        else:
            heading = ""
            hm = re.search(r"<h[12][^>]*>(.*?)</h[12]>", inner, re.I | re.S)
            if hm:
                heading = strip_tags(hm.group(1))
            body_text = strip_tags(inner)
            text = (heading + "。" + body_text) if heading and heading not in body_text[:40] else body_text
            if tsh_m and len(text) < 30:
                text = unescape(tsh_m.group(1)).strip()
        text = re.sub(r"\s+", "", text)[:MAX_NARRATION] if text else ""
        label = ""
        if tsh_m:
            label = unescape(tsh_m.group(1)).split(" - ")[0].strip()
        sections.append({"tts": tts_id, "label": label or tts_id, "text": text})
    return sections


def section_mp3_path(tts_dir: Path, idx: int, sec: dict) -> Path:
    slug = re.sub(r"[^a-z0-9]+", "-", sec["tts"].lower()).strip("-") or f"sec{idx}"
    return tts_dir / f"s{idx:02d}-{slug}.mp3"


def sections_audio_complete(course_dir: Path, html: str) -> bool:
    sections = find_tts_sections(html)
    if not sections:
        return count_real_mp3(course_dir) >= 3
    tts_dir = course_dir / "tts"
    for idx, sec in enumerate(sections, 1):
        out = section_mp3_path(tts_dir, idx, sec)
        if not out.is_file() or out.stat().st_size < MIN_MP3:
            return False
    return True


def synthesize_mp3(text: str, voice: str, out_path: Path, *, retries: int = 3) -> tuple[bool, str]:
    engine = SCRIPT_DIR / "tts-engine.py"
    if not engine.exists():
        return False, "tts-engine.py 不存在"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    msg = ""
    for attempt in range(retries):
        if out_path.exists() and out_path.stat().st_size < MIN_MP3:
            out_path.unlink()
        try:
            r = subprocess.run(
                [sys.executable, str(engine), "--text", text, "--voice", voice,
                 "--output", str(out_path)],
                capture_output=True, text=True, timeout=120,
            )
        except subprocess.TimeoutExpired:
            msg = "tts 超时"
        else:
            msg = (r.stdout or r.stderr or "").strip()[:120]
        if out_path.exists() and out_path.stat().st_size >= MIN_MP3:
            return True, msg
        if attempt < retries - 1:
            time.sleep(2 * (attempt + 1))
    return False, msg


def count_real_mp3(course_dir: Path) -> int:
    n = 0
    for sub in ("tts", "assets/tts"):
        d = course_dir / sub
        if d.is_dir():
            n += sum(1 for p in d.glob("*.mp3") if p.stat().st_size >= MIN_MP3)
    return n


def generate_audio(course_dir: Path, manifest: dict, html: str) -> dict:
    """为每个 data-tts 段落生成 mp3，写 tts/manifest.json。返回报告。

    重要：仅当每个 data-tts 段落都有有效 mp3（≥ MIN_MP3）时才跳过生成，
    避免 playlist 已注入但部分音频失败时被误判为齐全。
    """
    report = {"generated": [], "reused": [], "failed": [], "sections": 0, "skipped": False}

    sections = find_tts_sections(html)
    if sections_audio_complete(course_dir, html):
        report["skipped"] = True
        existing = count_real_mp3(course_dir)
        report["reused"] = [f"已有完整音频（sections={len(sections) or 'n/a'}, mp3={existing}），跳过生成"]
        return report

    report["sections"] = len(sections)
    if not sections:
        return report

    subject = (manifest.get("subject") or "").lower()
    tts_dir = course_dir / "tts"
    tts_dir.mkdir(parents=True, exist_ok=True)

    manifest_entries = []
    for idx, sec in enumerate(sections, 1):
        out = section_mp3_path(tts_dir, idx, sec)
        fname = out.name
        if out.exists() and out.stat().st_size >= MIN_MP3:
            report["reused"].append(fname)
        else:
            text = sec["text"]
            if len(text) < 10:
                text = f"{manifest.get('name') or '本节'}。{sec['label']}。"
            voice = voice_for_text(subject, text)
            ok, msg = synthesize_mp3(text, voice, out)
            if ok:
                report["generated"].append(fname)
            else:
                report["failed"].append(f"{fname}: {msg}")
                continue
        manifest_entries.append({
            "id": out.stem,
            "file": fname,
            "section": sec["tts"],
            "label": sec["label"],
            "bytes": out.stat().st_size if out.exists() else 0,
        })

    if manifest_entries:
        voices = sorted({voice_for_text(subject, sec["text"]) for sec in sections})
        (tts_dir / "manifest.json").write_text(
            json.dumps({
                "tts_files": manifest_entries,
                "engine": "tts-engine (multi)",
                "voice": voices[0] if len(voices) == 1 else voices,
            }, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return report


def finalize(course_dir: Path, do_audio: bool = True, self_contained: bool = True) -> dict:
    index = course_dir / "index.html"
    if not index.exists():
        return {"ok": False, "error": "缺少 index.html"}
    manifest = {}
    mf = course_dir / "manifest.json"
    if mf.exists():
        try:
            manifest = json.loads(mf.read_text(encoding="utf-8"))
        except Exception:
            manifest = {}

    asm = _load_apply_modules()
    if asm is None:
        return {"ok": False, "error": "apply-standard-modules.py 不可用"}

    html = index.read_text(encoding="utf-8")
    original = html
    actions = {}

    node_id = manifest.get("node_id")
    heading = manifest.get("name") or course_dir.name

    maps_mod = _load_apply_maps()
    map_mod = _load_cn_map_config()

    if node_id:
        html, kg_patched = patch_kg_slide(html, node_id, heading)
        if kg_patched:
            actions["kg_slide"] = True

    if maps_mod and map_mod:
        html, map_inj = ensure_hist_geo_map(course_dir, html, manifest, maps_mod, map_mod)
        if map_inj:
            actions["map_inject"] = map_inj

    html, links = asm.ensure_head_links(html)
    html, scripts = asm.ensure_tail_scripts(html)
    html, card = asm.ensure_tutor_card_section(html)
    html, cfg = asm.ensure_tutor_config(html, manifest, course_dir.name, node_id)
    actions.update(links_added=links, scripts_added=scripts, tutor_card=card, tutor_config=cfg)

    if node_id:
        html, kg = asm.ensure_kg_section(html, node_id, heading)
        actions["kg"] = kg
    else:
        actions["kg"] = "skipped-no-node-id"

    html, map_actions = ensure_map_assets(html)
    if map_actions:
        actions["map_modules"] = map_actions

    if maps_mod and "data-teachany-map" in html:
        html, map_sync = maps_mod.sync_map_config_in_html(course_dir, html)
        if map_sync.get("changed"):
            actions["map_config_sync"] = map_sync

    html, kg_norm = normalize_kg_node_id(course_dir, html, manifest)
    if kg_norm:
        actions["kg_node_id"] = kg_norm

    _, kg_manifest_actions = ensure_kg_manifest(course_dir, html)
    if kg_manifest_actions:
        actions["kg_manifest"] = kg_manifest_actions

    audio_report = {"sections": 0, "generated": [], "reused": [], "failed": []}
    if do_audio:
        audio_report = generate_audio(course_dir, manifest, html)

    # 音频接线（在生成 mp3 后注入 playlist）
    html, audio_action = asm.ensure_audio_config(html, course_dir)
    actions["audio_config"] = audio_action

    # self-contained：复制模块副本进课件目录 + 把 ../../assets/scripts/ 改为 ./assets/scripts/
    sc_report = {"copied": [], "missing_source": False, "rewrote": 0}
    if self_contained:
        html, sc_report = make_self_contained(course_dir, html)
    actions["self_contained"] = sc_report

    changed = html != original
    if changed:
        index.write_text(html, encoding="utf-8")

    ok = not audio_report["failed"] and not (self_contained and sc_report["missing_source"])
    return {
        "ok": ok,
        "course": course_dir.name,
        "changed": changed,
        "actions": actions,
        "audio": audio_report,
        "self_contained": sc_report,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("course_dir")
    ap.add_argument("--no-audio", action="store_true", help="只补模块，不生成音频")
    ap.add_argument("--shared", action="store_true",
                    help="用共享根 assets（../../assets/scripts/），不复制副本（不推荐，挂树后易失效）")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    course = Path(args.course_dir)
    if not course.is_dir():
        print(f"❌ 课件目录不存在: {course}", file=sys.stderr)
        return 2

    report = finalize(course, do_audio=not args.no_audio, self_contained=not args.shared)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report.get("ok") else 1

    if not report.get("ok") and report.get("error"):
        print(f"❌ {report['error']}")
        return 2

    print(f"TeachAny finalize · {report['course']}")
    a = report["actions"]
    if a.get("links_added"):
        print(f"  ✚ 补 CSS：{', '.join(a['links_added'])}")
    if a.get("scripts_added"):
        print(f"  ✚ 补 JS：{', '.join(a['scripts_added'])}")
    if a.get("tutor_card"):
        print("  ✚ AI 学伴入口卡片")
    if a.get("tutor_config"):
        print("  ✚ AI 学伴配置 __TEACHANY_TUTOR_CONFIG__")
    if a.get("kg") and a["kg"] not in ("unchanged",):
        print(f"  ✚ 知识图谱：{a['kg']}")
    if a.get("kg_slide"):
        print("  ✚ 知识图谱页插入幻灯片流")
    if a.get("map_inject"):
        print(f"  ✚ 历史/地理地图：{a['map_inject']}")
    if a.get("map_config_sync") and a["map_config_sync"].get("changed"):
        ms = a["map_config_sync"]
        print(f"  ✚ 地图配置同步：eras={ms.get('copied_eras', 0)} overlays={ms.get('copied_overlays', 0)}")
    if a.get("kg_node_id"):
        print(f"  ✚ 知识图谱 node_id 对齐：{a['kg_node_id']}")
    if a.get("kg_manifest"):
        print("  ✚ 知识图谱 manifest 自包含复制")
    au = report["audio"]
    if au.get("skipped"):
        print("  🔊 音频：已有 playlist/mp3，保留作者原音频（未重新生成）")
    elif au["sections"]:
        print(f"  🔊 音频段落 {au['sections']}：生成 {len(au['generated'])} / 复用 {len(au['reused'])} / 失败 {len(au['failed'])}")
        for f in au["failed"]:
            print(f"     ❌ {f}")
    if a.get("audio_config") and a["audio_config"] != "unchanged":
        print(f"  ✚ 音频播放列表：{a['audio_config']}")
    sc = report.get("self_contained") or {}
    if sc.get("missing_source"):
        print("  ⚠️  未找到模块源（仓根 assets/scripts），无法 self-contained — 模块挂树后可能失效")
    elif sc.get("copied") or sc.get("rewrote"):
        print(f"  📦 self-contained：复制 {len(sc.get('copied', []))} 个模块副本，重写 {sc.get('rewrote', 0)} 处引用为 ./assets/scripts/")
    print()
    if report["ok"]:
        print("✅ 定稿完成：AI 学伴 / 音频 / 知识图谱 三模块齐全")
    else:
        print("⚠️  定稿完成但音频部分失败，请检查 tts-engine（edge-tts/say）后重跑")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
