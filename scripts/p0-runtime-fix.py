#!/usr/bin/env python3
"""P0 batch fix: sync map geojson paths + self-contained KG manifest via finalize.

Usage:
  python3 p0-runtime-fix.py
  python3 p0-runtime-fix.py --subject history
  python3 p0-runtime-fix.py --limit 20
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
COMMUNITY = ROOT / "community"


def load_maps():
    spec = importlib.util.spec_from_file_location("apply_maps", SCRIPTS / "apply-historical-maps.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_finalize(course_dir: Path) -> int:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "finalize-courseware.py"), str(course_dir), "--no-audio"],
        cwd=ROOT,
    ).returncode


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", default="", help="history|geography|...")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--skip-finalize", action="store_true", help="Only sync map config in HTML")
    args = ap.parse_args()

    maps_mod = load_maps()
    targets = []
    for d in sorted(COMMUNITY.iterdir()):
        if not d.is_dir() or not (d / "index.html").is_file():
            continue
        if args.subject:
            mf = d / "manifest.json"
            if not mf.is_file():
                continue
            m = json.loads(mf.read_text(encoding="utf-8"))
            if (m.get("subject") or "").lower() != args.subject.lower():
                continue
        targets.append(d)
    if args.limit:
        targets = targets[: args.limit]

    map_sync_n = finalize_ok = finalize_fail = 0
    print(f"P0 runtime fix: {len(targets)} course(s)\n")

    for i, course_dir in enumerate(targets, 1):
        html = (course_dir / "index.html").read_text(encoding="utf-8", errors="replace")
        actions = []
        if "data-teachany-map" in html:
            new_html, rep = maps_mod.sync_map_config_in_html(course_dir, html)
            if rep.get("changed"):
                (course_dir / "index.html").write_text(new_html, encoding="utf-8")
                map_sync_n += 1
                actions.append("map-sync")
        if not args.skip_finalize:
            rc = run_finalize(course_dir)
            if rc == 0:
                finalize_ok += 1
                actions.append("finalize")
            else:
                finalize_fail += 1
                actions.append("finalize-fail")
        tag = ", ".join(actions) if actions else "unchanged"
        print(f"[{i}/{len(targets)}] {course_dir.name} ({tag})")

    print(f"\n地图配置同步: {map_sync_n}")
    if not args.skip_finalize:
        print(f"finalize: {finalize_ok} ok, {finalize_fail} failed")
    return 0 if finalize_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
