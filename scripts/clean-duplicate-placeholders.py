#!/usr/bin/env python3
"""Remove duplicate placeholder media from community/ courseware.

Targets:
- remotion/node_modules/ (accidental installs, not published)
- teachany-overview.mp4 + injected teachany-video-overview HTML blocks
- section1.png / section2.png batch placeholders → concept/process SVG
- zero-byte / tiny stub audio from audit rules
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

OVERVIEW_SECTION_RE = re.compile(
    r'<section\s+class="ta-standard-section"\s+id="teachany-video-overview">.*?</section>',
    re.DOTALL | re.IGNORECASE,
)
SECTION1_REFS = (
    "./assets/section1.png",
    "assets/section1.png",
    "./assets/section1.png",
)
SECTION2_REFS = (
    "./assets/section2.png",
    "assets/section2.png",
)


def load_repair_helpers():
    spec = importlib.util.spec_from_file_location("repair_image_refs", ROOT / "scripts" / "repair-image-refs.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def course_dirs() -> list[Path]:
    skip = {"pending", "drafts", "archive"}
    return sorted(
        p for p in COMMUNITY.iterdir()
        if p.is_dir() and p.name not in skip
    )


def remove_remotion_node_modules(report: dict) -> None:
    for path in sorted(COMMUNITY.rglob("node_modules")):
        if "remotion" not in path.parts:
            continue
        if not path.is_dir():
            continue
        count = sum(1 for _ in path.rglob("*") if _.is_file())
        size = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
        report["remotion_node_modules"].append({
            "path": str(path.relative_to(ROOT)),
            "files": count,
            "bytes": size,
        })
        shutil.rmtree(path)


def strip_teachany_overview(course_dir: Path, report: dict, *, dry_run: bool) -> None:
    html_path = course_dir / "index.html"
    if html_path.is_file():
        html = html_path.read_text(encoding="utf-8", errors="ignore")
        new_html, n = OVERVIEW_SECTION_RE.subn("", html)
        if n:
            report["overview_sections_removed"] += n
            if not dry_run and new_html != html:
                html_path.write_text(new_html, encoding="utf-8")

    mf = course_dir / "manifest.json"
    if mf.is_file():
        try:
            data = json.loads(mf.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = None
        if isinstance(data, dict):
            changed = False
            for key in ("assets",):
                block = data.get(key)
                if isinstance(block, dict) and isinstance(block.get("videos"), list):
                    new_vids = [v for v in block["videos"] if "teachany-overview" not in str(v)]
                    if new_vids != block["videos"]:
                        block["videos"] = new_vids
                        changed = True
            if isinstance(data.get("videos"), list):
                new_vids = [v for v in data["videos"] if "teachany-overview" not in str(v)]
                if new_vids != data["videos"]:
                    data["videos"] = new_vids
                    changed = True
            if changed:
                report["overview_manifest_cleaned"] += 1
                if not dry_run:
                    mf.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for mp4 in course_dir.rglob("teachany-overview.mp4"):
        report["overview_mp4_removed"].append(str(mp4.relative_to(ROOT)))
        if not dry_run:
            mp4.unlink()


def migrate_section_pngs(course_dir: Path, repair, report: dict, *, dry_run: bool) -> None:
    html_path = course_dir / "index.html"
    if not html_path.is_file():
        return
    html = html_path.read_text(encoding="utf-8", errors="ignore")
    if "section1.png" not in html and "section2.png" not in html:
        return

    title = repair.course_title(course_dir)
    if not dry_run:
        repair.ensure_standard_svgs(course_dir, title)

    new_html = html
    for old, new in (
        ("./assets/section1.png", "./assets/concept-diagram.svg"),
        ("assets/section1.png", "./assets/concept-diagram.svg"),
        ("./assets/section2.png", "./assets/process-diagram.svg"),
        ("assets/section2.png", "./assets/process-diagram.svg"),
    ):
        if old in new_html:
            new_html = new_html.replace(old, new)
            report["section_png_refs_replaced"] += html.count(old)

    if new_html != html:
        report["section_courses_updated"] += 1
        if not dry_run:
            html_path.write_text(new_html, encoding="utf-8")
            repair.update_manifest(course_dir)

    for name in ("section1.png", "section2.png"):
        path = course_dir / "assets" / name
        if path.is_file():
            report["section_png_deleted"].append(str(path.relative_to(ROOT)))
            if not dry_run:
                path.unlink()


def remove_tiny_placeholders(report: dict, *, dry_run: bool) -> None:
    stub_hash = "6e8ebfba8299710c9db6da970ea02a4a"

    def md5(path: Path) -> str:
        h = hashlib.md5()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()

    for path in sorted(COMMUNITY.rglob("*")):
        if not path.is_file():
            continue
        ext = path.suffix.lower()
        try:
            size = path.stat().st_size
        except OSError:
            continue
        reason = None
        if ext == ".mp3" and size == 0:
            reason = "zero_mp3"
        elif ext == ".mp3" and size < 2048 and md5(path) == stub_hash:
            reason = "tiny_mp3_stub"
        elif ext == ".mp4" and size < 8192:
            reason = "tiny_mp4"
        elif ext in (".png", ".jpg", ".jpeg", ".webp", ".gif") and size < 1024:
            reason = "tiny_image"
        if reason:
            report[reason].append(str(path.relative_to(ROOT)))
            if not dry_run:
                path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Apply deletions (default: dry-run)")
    parser.add_argument("--json", type=Path, help="Write report JSON")
    args = parser.parse_args()
    dry_run = not args.apply

    repair = load_repair_helpers()
    report: dict = {
        "dry_run": dry_run,
        "remotion_node_modules": [],
        "overview_sections_removed": 0,
        "overview_manifest_cleaned": 0,
        "overview_mp4_removed": [],
        "section_png_refs_replaced": 0,
        "section_courses_updated": 0,
        "section_png_deleted": [],
        "zero_mp3": [],
        "tiny_mp3_stub": [],
        "tiny_mp4": [],
        "tiny_image": [],
    }

    if dry_run:
        # collect node_modules without deleting
        for path in sorted(COMMUNITY.rglob("node_modules")):
            if "remotion" not in path.parts or not path.is_dir():
                continue
            count = sum(1 for _ in path.rglob("*") if _.is_file())
            size = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
            report["remotion_node_modules"].append({
                "path": str(path.relative_to(ROOT)),
                "files": count,
                "bytes": size,
            })
    else:
        remove_remotion_node_modules(report)

    for course_dir in course_dirs():
        strip_teachany_overview(course_dir, report, dry_run=dry_run)
        migrate_section_pngs(course_dir, repair, report, dry_run=dry_run)

    remove_tiny_placeholders(report, dry_run=dry_run)

    summary = {
        "remotion_node_modules_dirs": len(report["remotion_node_modules"]),
        "remotion_node_modules_files": sum(x["files"] for x in report["remotion_node_modules"]),
        "overview_sections_removed": report["overview_sections_removed"],
        "overview_mp4_removed": len(report["overview_mp4_removed"]),
        "section_courses_updated": report["section_courses_updated"],
        "section_png_deleted": len(report["section_png_deleted"]),
        "zero_mp3": len(report["zero_mp3"]),
        "tiny_mp3_stub": len(report["tiny_mp3_stub"]),
        "tiny_mp4": len(report["tiny_mp4"]),
        "tiny_image": len(report["tiny_image"]),
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))

    if args.json:
        args.json.write_text(json.dumps({**report, "summary": summary}, ensure_ascii=False, indent=2), encoding="utf-8")

    if dry_run:
        print("\nDry-run only. Re-run with --apply to delete/replace.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
