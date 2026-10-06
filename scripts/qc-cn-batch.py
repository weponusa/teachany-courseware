#!/usr/bin/env python3
"""Comprehensive QC for CN gap courseware batch.

Checks per course:
  - PNG hero + sections >= 500KB (Agnes, not placeholder)
  - ./assets/scripts/ai-tutor.js referenced and exists
  - drag-chip interactive present
  - __TEACHANY_TUTOR_CONFIG__ injected
  - TTS mp3 count >= 10
  - preflight-publish --no-finalize
  - validate-courseware.py single course

Usage:
  python3 qc-cn-batch.py community/hist-m-prehistoric community/hist-m-ancient-china
  python3 qc-cn-batch.py --from-log /tmp/cn-batch-hist-m.log
  python3 qc-cn-batch.py --batch-size 5 --stage middle --subject history  # QC latest 5 dirs
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
MIN_PNG = 500 * 1024


def course_dir(path: str) -> Path:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    return p


def qc_one(course: Path, *, deep: bool = True) -> list[str]:
    errors: list[str] = []
    warns: list[str] = []
    nid = course.name
    if not (course / "index.html").is_file():
        return [f"❌ {nid}: missing index.html"]

    html = (course / "index.html").read_text(encoding="utf-8", errors="replace")

    # PNG sizes
    pngs = list(course.glob("assets/*.png"))
    if len(pngs) < 3:
        errors.append(f"❌ {nid}: assets/*.png count {len(pngs)} < 3")
    for png in pngs:
        sz = png.stat().st_size
        if sz < MIN_PNG:
            errors.append(f"❌ {nid}: {png.name} only {sz//1024}KB (<500KB)")

    # Self-contained modules
    if "./assets/scripts/" not in html:
        errors.append(f"❌ {nid}: HTML missing ./assets/scripts/ references")
    tutor = course / "assets/scripts/ai-tutor.js"
    if not tutor.is_file():
        errors.append(f"❌ {nid}: missing assets/scripts/ai-tutor.js")
    if "__TEACHANY_TUTOR_CONFIG__" not in html:
        errors.append(f"❌ {nid}: missing __TEACHANY_TUTOR_CONFIG__")
    if "teachany-audio-player" not in html and "AUDIO_PLAYLIST" not in html:
        warns.append(f"⚠️  {nid}: audio player module not detected in HTML")
    if "knowledge-graph" not in html and "data-teachany-kg" not in html:
        errors.append(f"❌ {nid}: knowledge graph module not detected")

    # Interaction
    if "drag-chip" not in html and "phet-wrap" not in html:
        errors.append(f"❌ {nid}: no drag-chip or PhET interaction")

    # TTS
    mp3s = list((course / "tts").glob("*.mp3")) if (course / "tts").is_dir() else []
    if len(mp3s) < 10:
        errors.append(f"❌ {nid}: TTS mp3 count {len(mp3s)} < 10")

    # Manifest
    mf = course / "manifest.json"
    if mf.is_file():
        import json
        m = json.loads(mf.read_text(encoding="utf-8"))
        if m.get("node_id") != nid and m.get("id") != nid:
            errors.append(f"❌ {nid}: manifest id mismatch")
        if not m.get("feedback", {}).get("password_hint"):
            warns.append(f"⚠️  {nid}: no password hint in manifest")

    if deep:
        r = subprocess.run(
            [sys.executable, str(SCRIPTS / "preflight-publish.py"), str(course), "--no-finalize"],
            cwd=ROOT, capture_output=True, text=True,
        )
        if r.returncode != 0:
            errors.append(f"❌ {nid}: preflight failed\n{r.stdout[-400:]}{r.stderr[-200:]}")
        r2 = subprocess.run(
            [sys.executable, str(SCRIPTS / "validate-courseware.py"), nid],
            cwd=ROOT, capture_output=True, text=True,
        )
        if r2.returncode != 0:
            tail = (r2.stdout + r2.stderr)[-600:]
            errors.append(f"❌ {nid}: validate-courseware failed\n{tail}")

    return errors + warns


def parse_log(log_path: Path) -> list[Path]:
    text = log_path.read_text(encoding="utf-8", errors="replace")
    ids = re.findall(r"^=== ([\w-]+) ===$", text, re.M)
    return [ROOT / "community" / i for i in ids]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("courses", nargs="*", help="community/<id> paths")
    ap.add_argument("--from-log")
    ap.add_argument("--fail-fast", action="store_true")
    args = ap.parse_args()

    targets: list[Path] = []
    if args.from_log:
        targets = parse_log(Path(args.from_log))
    for c in args.courses:
        targets.append(course_dir(c))

    if not targets:
        print("No courses to QC", file=sys.stderr)
        return 2

    print(f"🔍 Comprehensive QC: {len(targets)} course(s)")
    all_errors = 0
    for i, course in enumerate(targets, 1):
        print(f"\n--- [{i}/{len(targets)}] {course.name} ---")
        issues = qc_one(course)
        if not issues:
            print(f"✅ {course.name}: PASS")
        else:
            for line in issues:
                print(line)
                if line.startswith("❌"):
                    all_errors += 1
            if args.fail_fast and all_errors:
                return 1

    # Deep QC on last course (每批第5课)
    if len(targets) >= 1:
        last = targets[-1]
        print(f"\n📋 质检课（本批第 {len(targets)} 课）: {last.name}")
        issues = qc_one(last, deep=True)
        hard = [x for x in issues if x.startswith("❌")]
        if hard:
            print("质检课未通过:")
            for h in hard:
                print(h)
            return 1
        print(f"✅ 质检课 {last.name} 全面通过")

    print(f"\n{'✅ 批次 QC 通过' if all_errors == 0 else f'❌ {all_errors} 项错误'}")
    return 1 if all_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
