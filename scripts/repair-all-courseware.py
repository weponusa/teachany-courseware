#!/usr/bin/env python3
"""Full courseware QC + repair pass for all community lessons.

Phases:
  1. Rebuild from cn-specs / sci-e-specs (template + maps + KG slide)
  2. Patch slide courses missing in-flow knowledge graph
  3. Inject maps for history/geography without declarative map module
  4. finalize --no-audio (modules, self-contained scripts)
  5. validate-courseware summary

Usage:
  python3 repair-all-courseware.py
  python3 repair-all-courseware.py --skip-rebuild
  python3 repair-all-courseware.py --limit 50
"""
from __future__ import annotations

import argparse
import html as html_mod
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
COMMUNITY = ROOT / "community"
CN_SPECS = SCRIPTS / "cn-specs"
SCI_SPECS = SCRIPTS / "sci-e-specs"
MAP_MANIFEST = SCRIPTS / "historical-maps-manifest.json"

ORPHAN_KG_RE = re.compile(
    r"\n<!-- v7\.7\.4 标准知识图谱模块 -->\s*"
    r'<section class="section" id="knowledge-graph"[^>]*>[\s\S]*?</section>\s*',
    re.I,
)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(cmd: list[str]) -> int:
    return subprocess.run(cmd, cwd=ROOT).returncode


def parse_grade(manifest: dict) -> int:
    g = manifest.get("grade")
    if isinstance(g, int):
        return g
    if isinstance(g, str) and g.isdigit():
        return int(g)
    stage = (manifest.get("stage") or (g if isinstance(g, str) else "") or "middle").lower()
    if stage in ("high", "senior"):
        return 11
    if stage in ("middle", "junior"):
        return 8
    if stage in ("elementary", "primary"):
        return 5
    return 8


def all_courses() -> list[Path]:
    out = []
    for d in sorted(COMMUNITY.iterdir()):
        if d.is_dir() and (d / "index.html").is_file() and (d / "manifest.json").is_file():
            out.append(d)
    return out


def load_manifest(course_dir: Path) -> dict:
    try:
        return json.loads((course_dir / "manifest.json").read_text(encoding="utf-8"))
    except Exception:
        return {}


def needs_kg_slide(html: str) -> bool:
    return (
        'id="slide-container"' in html
        and 'data-tts="knowledge-graph"' not in html
    )


def patch_kg_slide(html: str, node_id: str, title: str) -> str:
    if not needs_kg_slide(html):
        return html
    if 'data-tts="knowledge-graph"' in html:
        return html
    safe_title = html_mod.escape(title, quote=True)
    safe_nid = html_mod.escape(node_id, quote=True)
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
        close = html.find("</div>", html.find('id="slide-container"'))
        while close != -1:
            tail = html[close : close + 20]
            if "<script" in tail or '<section class="slide-page"' in html[close: close + 200]:
                close = html.find("</div>", close + 6)
                continue
            html = html[:close] + "\n" + slide + html[close:]
            break
    if 'id="knowledge-graph"' in html and 'data-tts="knowledge-graph"' in html:
        html = ORPHAN_KG_RE.sub("\n", html, count=1)
    return html


def map_manifest_cfg(course_dir: Path, hist_manifest: dict) -> dict | None:
    rel = f"community/{course_dir.name}"
    cfg = hist_manifest.get(rel) or hist_manifest.get(f"examples/{course_dir.name}")
    if cfg and cfg.get("skip"):
        return None
    return cfg


def needs_map(subj: str, html: str, course_dir: Path | None = None, hist_manifest: dict | None = None) -> bool:
    if subj not in ("history", "geography"):
        return False
    if course_dir and hist_manifest is not None:
        cfg = map_manifest_cfg(course_dir, hist_manifest)
        if cfg is None and (
            hist_manifest.get(f"community/{course_dir.name}", {}).get("skip")
            or hist_manifest.get(f"examples/{course_dir.name}", {}).get("skip")
        ):
            return False
    if "data-teachany-map" in html:
        return False
    if re.search(r"L\.tileLayer\s*\(", html) and re.search(r"fitBounds|setView", html):
        return False
    return True


def inject_map(course_dir: Path, manifest: dict, maps_mod, map_mod, hist_manifest: dict) -> bool:
    rel = f"community/{course_dir.name}"
    cfg = map_manifest_cfg(course_dir, hist_manifest)
    if cfg is None and (
        hist_manifest.get(rel, {}).get("skip")
        or hist_manifest.get(f"examples/{course_dir.name}", {}).get("skip")
    ):
        return False
    if not cfg:
        pseudo = {
            "node_id": course_dir.name,
            "title": manifest.get("name") or course_dir.name,
            "subject": manifest.get("subject") or "history",
            "stage": manifest.get("stage") or "middle",
            "grade": parse_grade(manifest),
        }
        cfg = map_mod.default_map_config(pseudo)
    if not cfg:
        return False
    idx = course_dir / "index.html"
    html = idx.read_text(encoding="utf-8")
    if "data-teachany-map" in html:
        return False
    cfg_copy = json.loads(json.dumps(cfg))
    maps_mod.ensure_map_projection_defaults(cfg_copy)
    maps_mod.copy_geojson_files(course_dir, cfg_copy.get("scope", "china"), cfg_copy["eras"])
    maps_mod.copy_overlay_files(course_dir, cfg_copy.get("overlays", []))
    html = maps_mod.inject_head(html)
    html = maps_mod.inject_script_bottom(html)
    block = maps_mod.build_section(rel, cfg_copy)
    html, injected = maps_mod.inject_section(html, block)
    if not injected and 'id="slide-container"' in html:
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
    if html != idx.read_text(encoding="utf-8"):
        idx.write_text(html, encoding="utf-8")
        return True
    return False


def needs_modules(course_dir: Path, html: str) -> bool:
    tutor_local = (course_dir / "assets/scripts/ai-tutor.js").is_file()
    tutor_linked = "ai-tutor.js" in html
    kg_ok = "data-teachany-kg" in html or (
        "knowledge-graph" in html and "teachany-knowledge-graph" in html
    )
    self_contained = "./assets/scripts/ai-tutor.js" in html or "./assets/scripts/" in html
    if tutor_local and tutor_linked and kg_ok:
        return not self_contained
    return not (tutor_local and tutor_linked and kg_ok)


def qc_issues(course_dir: Path, html: str, manifest: dict, hist_manifest: dict) -> list[str]:
    issues = []
    subj = (manifest.get("subject") or "").lower()
    stage = (manifest.get("stage") or "").lower()
    if needs_kg_slide(html):
        issues.append("kg-slide")
    if needs_map(subj, html, course_dir, hist_manifest):
        issues.append("map")
    if needs_modules(course_dir, html):
        issues.append("modules")
    if stage == "high" and 'id="slide-container"' in html and "#0f172a" not in html:
        spec = CN_SPECS / f"{course_dir.name}.json"
        if spec.is_file():
            issues.append("high-theme")
    return issues


def rebuild_cn(nid: str, maps_mod, map_mod) -> bool:
    spec_path = CN_SPECS / f"{nid}.json"
    if not spec_path.is_file():
        return False
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    if (spec.get("subject") or "").lower() in ("history", "geography"):
        spec["map_config"] = map_mod.default_map_config(spec)
        spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if run([sys.executable, str(SCRIPTS / "build-cn-course.py"), "--spec", str(spec_path)]) != 0:
        return False
    course_dir = COMMUNITY / nid
    cfg = spec.get("map_config") or map_mod.default_map_config(spec)
    if cfg:
        cfg = json.loads(json.dumps(cfg))
        maps_mod.ensure_map_projection_defaults(cfg)
        maps_mod.copy_geojson_files(course_dir, cfg.get("scope", "china"), cfg["eras"])
        maps_mod.copy_overlay_files(course_dir, cfg.get("overlays", []))
    return True


def rebuild_sci(nid: str) -> bool:
    spec_path = SCI_SPECS / f"{nid}.json"
    if not spec_path.is_file():
        return False
    return run([sys.executable, str(SCRIPTS / "build-sci-e-course.py"), "--spec", str(spec_path)]) == 0


def repair_course(course_dir: Path, maps_mod, map_mod, hist_manifest: dict, *, skip_rebuild: bool) -> tuple[bool, list[str]]:
    nid = course_dir.name
    manifest = load_manifest(course_dir)
    actions: list[str] = []

    if not skip_rebuild:
        if (CN_SPECS / f"{nid}.json").is_file():
            if rebuild_cn(nid, maps_mod, map_mod):
                actions.append("rebuild-cn")
        elif (SCI_SPECS / f"{nid}.json").is_file():
            if rebuild_sci(nid):
                actions.append("rebuild-sci")

    html = (course_dir / "index.html").read_text(encoding="utf-8", errors="replace")
    node_id = manifest.get("node_id") or nid
    title = manifest.get("name") or nid

    if needs_kg_slide(html):
        new_html = patch_kg_slide(html, node_id, title)
        if new_html != html:
            (course_dir / "index.html").write_text(new_html, encoding="utf-8")
            html = new_html
            actions.append("kg-slide")

    subj = (manifest.get("subject") or "").lower()
    if needs_map(subj, html, course_dir, hist_manifest):
        if inject_map(course_dir, manifest, maps_mod, map_mod, hist_manifest):
            actions.append("map")
            html = (course_dir / "index.html").read_text(encoding="utf-8", errors="replace")

    if needs_modules(course_dir, html) or actions:
        if run([sys.executable, str(SCRIPTS / "finalize-courseware.py"), str(course_dir), "--no-audio"]) != 0:
            return False, actions + ["finalize-failed"]

    html = (course_dir / "index.html").read_text(encoding="utf-8", errors="replace")
    left = qc_issues(course_dir, html, manifest, hist_manifest)
    return len(left) == 0, actions + ([f"left:{','.join(left)}"] if left else [])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-rebuild", action="store_true", help="Only patch/finalize, no spec rebuild")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--node-ids", default="")
    ap.add_argument("--skip-validate", action="store_true")
    args = ap.parse_args()

    maps_mod = load_module("apply_maps", SCRIPTS / "apply-historical-maps.py")
    map_mod = load_module("cn_map_config", SCRIPTS / "cn-map-config.py")
    hist_manifest = {}
    if MAP_MANIFEST.is_file():
        hist_manifest = json.loads(MAP_MANIFEST.read_text(encoding="utf-8"))

    if args.node_ids:
        targets = [COMMUNITY / x.strip() for x in args.node_ids.split(",") if x.strip()]
    else:
        targets = all_courses()
    if args.limit:
        targets = targets[: args.limit]

    ok_n = fail_n = 0
    print(f"Repair-all: {len(targets)} course(s)\n")
    for i, course_dir in enumerate(targets, 1):
        ok, info = repair_course(course_dir, maps_mod, map_mod, hist_manifest, skip_rebuild=args.skip_rebuild)
        tag = ", ".join(info) if info else "unchanged"
        if ok:
            ok_n += 1
            print(f"[{i}/{len(targets)}] ✅ {course_dir.name} ({tag})")
        else:
            fail_n += 1
            print(f"[{i}/{len(targets)}] ❌ {course_dir.name} ({tag})")

    print(f"\nDone: {ok_n} ok, {fail_n} need attention")

    # validate summary
    if args.skip_validate:
        return 0 if fail_n == 0 else 1
    print("\nRunning validate-courseware.py …")
    rc = run([sys.executable, str(SCRIPTS / "validate-courseware.py")])
    return 0 if fail_n == 0 and rc == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
