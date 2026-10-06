#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Repair broken local image references in community courseware.

Fixes CN batch mismatch: HTML references {id}-hero.png / section1.png / section2.png
while assets/ only has hero-infographic.svg / concept-diagram.svg / process-diagram.svg.

Usage:
  python3 scripts/repair-image-refs.py
  python3 scripts/repair-image-refs.py --course geo-h-industry-services
  python3 scripts/repair-image-refs.py --dry-run
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
from html import escape as html_escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
IMG_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}

STANDARD_MAP = {
    "section1.png": "concept-diagram.svg",
    "section2.png": "process-diagram.svg",
}


def load_validator():
    spec = importlib.util.spec_from_file_location("val", ROOT / "scripts" / "validate-courseware.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def course_title(course_dir: Path) -> str:
    mf = course_dir / "manifest.json"
    if mf.is_file():
        try:
            data = json.loads(mf.read_text(encoding="utf-8"))
            return data.get("name") or data.get("title") or course_dir.name
        except Exception:
            pass
    html = (course_dir / "index.html").read_text(encoding="utf-8", errors="ignore")
    m = re.search(r'<meta name="course-title"\s+content="([^"]+)"', html)
    return m.group(1) if m else course_dir.name


def simple_svg(title: str, subtitle: str) -> str:
    t = html_escape(title[:40])
    s = html_escape(subtitle[:56])
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 540">'
        f'<defs><linearGradient id="g" x1="0" x2="1"><stop stop-color="#eff6ff"/>'
        f'<stop offset="1" stop-color="#dbeafe"/></linearGradient></defs>'
        f'<rect width="960" height="540" fill="url(#g)"/>'
        f'<text x="48" y="96" fill="#1e3a8a" font-size="34" font-weight="800">{t}</text>'
        f'<text x="48" y="150" fill="#475569" font-size="22">{s}</text>'
        f'<rect x="48" y="200" width="864" height="260" rx="18" fill="#fff" stroke="#93c5fd" stroke-width="3"/>'
        f'<text x="80" y="360" fill="#64748b" font-size="20">TeachAny · 课标互动课件插图</text>'
        f"</svg>"
    )


def list_asset_files(course_dir: Path) -> dict[str, Path]:
    assets = course_dir / "assets"
    out: dict[str, Path] = {}
    if not assets.is_dir():
        return out
    for p in assets.rglob("*"):
        if p.is_file() and p.suffix.lower() in IMG_EXT:
            out[p.name] = p
            rel = p.relative_to(assets).as_posix()
            out.setdefault(rel, p)
    return out


def resolve_ref_path(course_dir: Path, ref: str) -> Path:
    clean = ref.strip().lstrip("./")
    if clean.startswith("assets/"):
        clean = clean[7:]
    return (course_dir / "assets" / clean).resolve()


def pick_fallback(ref_name: str, nid: str, assets: dict[str, Path]) -> str | None:
    if ref_name in STANDARD_MAP and STANDARD_MAP[ref_name] in assets:
        return STANDARD_MAP[ref_name]
    if ref_name == f"{nid}-hero.png" and "hero-infographic.svg" in assets:
        return "hero-infographic.svg"
    if "hero" in ref_name.lower():
        for c in (
            "hero-infographic.svg",
            f"{nid}-hero.png",
            "hero-infographic.png",
            "hero-knowledge-map.png",
            "hero-protein.png",
            "hero-nucleic-acid.png",
        ):
            if c in assets:
                return c
        for name in sorted(assets):
            if "hero" in name.lower() and "/" not in name:
                return name
    if ref_name in ("section1.png",) or "concept" in ref_name:
        for c in ("concept-diagram.svg", "concept-diagram.png"):
            if c in assets:
                return c
    if ref_name in ("section2.png",) or "process" in ref_name:
        for c in ("process-diagram.svg", "process-diagram.png"):
            if c in assets:
                return c
    if "poster" in ref_name:
        for name in sorted(assets):
            if "poster" in name.lower() and "/" not in name:
                return name
        if "hero-infographic.svg" in assets:
            return "hero-infographic.svg"
    for name in sorted(assets):
        if "/" not in name:
            return name
    return None


def ensure_standard_svgs(course_dir: Path, title: str) -> list[str]:
    assets_dir = course_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    created = []
    defaults = {
        "hero-infographic.svg": simple_svg(title, "知识结构图"),
        "concept-diagram.svg": simple_svg(title, "核心概念示意"),
        "process-diagram.svg": simple_svg(title, "过程机制示意"),
    }
    for name, content in defaults.items():
        path = assets_dir / name
        if not path.is_file():
            path.write_text(content, encoding="utf-8")
            created.append(name)
    return created


def is_image_ref(ref: str) -> bool:
    if ref.startswith(("http://", "https://", "data:", "//", "#", "{{")):
        return False
    lower = ref.lower().split("?")[0].split("#")[0]
    return lower.endswith((".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"))


def normalize_asset_ref(ref: str) -> str:
    clean = ref.strip()
    if clean.startswith(("http://", "https://", "data:", "//", "#")):
        return ref
    while clean.startswith("./"):
        clean = clean[2:]
    if clean.startswith("assets/"):
        clean = "./" + clean
    elif clean.startswith("/assets/"):
        clean = "." + clean
    elif not clean.startswith("./"):
        clean = "./" + clean
    return clean


def rewrite_html_refs(html: str, course_dir: Path, assets: dict[str, Path]) -> tuple[str, list[str]]:
    nid = course_dir.name
    actions: list[str] = []

    def replace_ref(ref: str) -> str:
        nonlocal actions
        if ref.startswith(("http://", "https://", "data:", "//", "#", "{{")):
            return ref
        normalized = normalize_asset_ref(ref)
        target = resolve_ref_path(course_dir, normalized)
        if target.is_file():
            if ref != normalized:
                actions.append(f"normalize {Path(ref).name}")
            return normalized
        name = Path(normalized.replace("./assets/", "").replace("assets/", "")).name
        fb = pick_fallback(name, nid, assets)
        if fb:
            actions.append(f"{name}->{fb}")
            return f"./assets/{fb}"
        return ref

    def attr_repl(m: re.Match) -> str:
        attr, quote, ref = m.group(1), m.group(2), m.group(3)
        if not is_image_ref(ref):
            if attr == "src" and ref.startswith("assets/") and not ref.startswith("./"):
                return f'{attr}={quote}./{ref}{quote}'
            return m.group(0)
        new_ref = replace_ref(ref)
        return f'{attr}={quote}{new_ref}{quote}'

    html = re.sub(
        r'\b(src|href|poster)=(["\'])([^"\']+)\2',
        attr_repl,
        html,
    )

    def onerror_repl(m: re.Match) -> str:
        ref = m.group(1)
        new_ref = replace_ref(ref)
        if new_ref != ref:
            actions.append(f"onerror->{Path(new_ref).name}")
        return f"onerror=\"this.src='{new_ref}'\""

    html = re.sub(
        r"onerror=\"this\.src='([^']+)'\"",
        onerror_repl,
        html,
    )
    return html, actions


def update_manifest(course_dir: Path) -> None:
    mf = course_dir / "manifest.json"
    if not mf.is_file():
        return
    try:
        data = json.loads(mf.read_text(encoding="utf-8"))
    except Exception:
        return
    assets_meta = data.setdefault("assets", {})
    if isinstance(assets_meta, list):
        assets_meta = {}
        data["assets"] = assets_meta
    if (course_dir / "assets" / "hero-infographic.svg").is_file():
        assets_meta["hero"] = "assets/hero-infographic.svg"
    images = []
    for name in ("hero-infographic.svg", "concept-diagram.svg", "process-diagram.svg"):
        if (course_dir / "assets" / name).is_file():
            images.append(f"assets/{name}")
    if images:
        assets_meta["images"] = images
    data["assets"] = assets_meta
    mf.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def missing_images(course_dir: Path, html: str, val) -> list[tuple[str, str]]:
    missing = val.find_missing_local_asset_refs(course_dir, html)
    return [x for x in missing if re.search(r"\.(png|jpe?g|webp|gif|svg)(?:\?|#|$)", x[0], re.I)]


def repair_course(course_dir: Path, val, *, dry_run: bool = False) -> tuple[bool, list[str]]:
    html_path = course_dir / "index.html"
    if not html_path.is_file():
        return True, []
    html = html_path.read_text(encoding="utf-8", errors="ignore")
    before = missing_images(course_dir, html, val)
    if not before:
        return True, []

    title = course_title(course_dir)
    ensure_standard_svgs(course_dir, title)
    assets = list_asset_files(course_dir)
    new_html, actions = rewrite_html_refs(html, course_dir, assets)

    # create stub svg for any remaining missing refs
    for ref, _ in missing_images(course_dir, new_html, val):
        name = Path(ref.lstrip("./").replace("assets/", "")).name
        stub = course_dir / "assets" / name
        if name.endswith(".svg") and not stub.is_file():
            stub.write_text(simple_svg(title, name), encoding="utf-8")
            actions.append(f"created {name}")
        elif name.endswith(".png") and not stub.is_file():
            fb = pick_fallback(name, course_dir.name, list_asset_files(course_dir))
            if fb:
                new_html = new_html.replace(ref, f"./assets/{fb}")
                new_html = new_html.replace(ref.lstrip("./"), f"./assets/{fb}")
                actions.append(f"{name}->{fb}")

    after = missing_images(course_dir, new_html, val)
    if not dry_run and new_html != html:
        html_path.write_text(new_html, encoding="utf-8")
        update_manifest(course_dir)

    ok = len(after) == 0
    if not ok:
        actions.append(f"still: {after[0][0]}")
    return ok, actions


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--course", default="", help="Single course id")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    val = load_validator()
    targets = [COMMUNITY / args.course] if args.course else sorted(p for p in COMMUNITY.iterdir() if p.is_dir())

    ok_n = fail_n = fixed_n = 0
    failed: list[str] = []
    for course_dir in targets:
        if not (course_dir / "index.html").is_file():
            continue
        html = (course_dir / "index.html").read_text(encoding="utf-8", errors="ignore")
        if not missing_images(course_dir, html, val):
            ok_n += 1
            continue
        ok, info = repair_course(course_dir, val, dry_run=args.dry_run)
        if ok:
            fixed_n += 1
            if args.course or len(info) <= 4:
                print(f"✅ {course_dir.name}: {', '.join(info[:5])}")
        else:
            fail_n += 1
            failed.append(course_dir.name)
            print(f"❌ {course_dir.name}: {', '.join(info[:5])}")

    total_ok = ok_n + fixed_n
    print(f"\nDone: {total_ok} ok ({fixed_n} repaired), {fail_n} still broken" + (" (dry-run)" if args.dry_run else ""))
    if failed:
        print("Still broken:", ", ".join(failed[:25]))
    return 0 if fail_n == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
