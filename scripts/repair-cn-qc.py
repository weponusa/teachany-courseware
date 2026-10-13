#!/usr/bin/env python3
"""Repair auto-generated CN courseware: maps, stage themes, in-slide knowledge graph.

Usage:
  python3 repair-cn-qc.py --subjects history,geography
  python3 repair-cn-qc.py --subjects history,geography,english,chinese --stage middle,high
  python3 repair-cn-qc.py --node-ids geo-m-four-regions,hist-h-ideological-liberation
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
COMMUNITY = ROOT / "community"
SPECS = SCRIPTS / "cn-specs"


def load_apply_maps():
    spec = importlib.util.spec_from_file_location("apply_maps", SCRIPTS / "apply-historical-maps.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_map_config():
    spec = importlib.util.spec_from_file_location("cn_map_config", SCRIPTS / "cn-map-config.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(cmd: list[str]) -> int:
    return subprocess.run(cmd, cwd=ROOT).returncode


PREFIX_SUBJECT = {
    "hist": "history",
    "geo": "geography",
    "eng": "english",
    "chn": "chinese",
    "math": "math",
    "sci": "science",
}
STAGE_CODE = {"e": "elementary", "m": "middle", "h": "high"}


def parse_nid(nid: str) -> tuple[str, str]:
    parts = nid.split("-")
    if len(parts) < 2:
        return "", ""
    return PREFIX_SUBJECT.get(parts[0], parts[0]), STAGE_CODE.get(parts[1], parts[1])


def list_targets(args) -> list[str]:
    if args.node_ids:
        return [x.strip() for x in args.node_ids.split(",") if x.strip()]
    subjects = {s.strip() for s in args.subjects.split(",") if s.strip()}
    stages = {s.strip() for s in args.stage.split(",") if s.strip()}
    out = []
    for d in sorted(COMMUNITY.iterdir()):
        if not d.is_dir() or not (d / "manifest.json").is_file():
            continue
        nid = d.name
        subject, stage = parse_nid(nid)
        if not subject or not stage:
            continue
        if subjects and subject not in subjects:
            continue
        if stages and stage not in stages:
            continue
        if not re.match(r"^(hist|geo|eng|chn)-[emh]-", nid):
            continue
        out.append(nid)
    return out


def ensure_spec(nid: str, map_mod) -> Path:
    spec_path = SPECS / f"{nid}.json"
    if not spec_path.is_file():
        run([sys.executable, str(SCRIPTS / "kp-to-cn-spec.py"), "--node-id", nid, "--out", str(SPECS)])
    if spec_path.is_file():
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        subj = (spec.get("subject") or "").lower()
        if subj in ("history", "geography"):
            spec["map_config"] = map_mod.default_map_config(spec)
            spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return spec_path


def sync_map_assets(course_dir: Path, spec: dict, maps_mod) -> int:
    subj = (spec.get("subject") or "").lower()
    if subj not in ("history", "geography"):
        return 0
    cfg = spec.get("map_config") or load_map_config().default_map_config(spec)
    if not cfg:
        return 0
    cfg = json.loads(json.dumps(cfg))
    maps_mod.ensure_map_projection_defaults(cfg)
    copied = maps_mod.copy_geojson_files(course_dir, cfg.get("scope", "china"), cfg["eras"])
    copied += maps_mod.copy_overlay_files(course_dir, cfg.get("overlays", []))
    return copied


def qc_one(course_dir: Path) -> list[str]:
    errors = []
    html = (course_dir / "index.html").read_text(encoding="utf-8", errors="replace")
    subj = ""
    mf = course_dir / "manifest.json"
    if mf.is_file():
        try:
            subj = (json.loads(mf.read_text(encoding="utf-8")).get("subject") or "").lower()
        except Exception:
            pass
    if "slide-container" in html:
        if 'data-teachany-kg="' not in html:
            errors.append("missing knowledge graph mount")
        elif 'data-tts="knowledge-graph"' not in html:
            errors.append("knowledge graph not in slide flow")
    if subj in ("history", "geography"):
        if "data-teachany-map" not in html:
            errors.append("missing data-teachany-map")
        if "teachany-historical-map.js" not in html:
            errors.append("missing teachany-historical-map.js")
    stage = ""
    m = re.search(r'teachany-stage"\s+content="([^"]+)"', html)
    if m:
        stage = m.group(1)
    if stage == "middle" and "teachany-middle-pro" not in html and "#f8fafc" not in html:
        errors.append("middle stage theme not applied")
    if stage == "high" and "#0f172a" not in html:
        errors.append("high stage theme not applied")
    return errors


def repair_one(nid: str, maps_mod, map_mod, *, skip_finalize: bool) -> tuple[bool, list[str]]:
    course_dir = COMMUNITY / nid
    spec_path = ensure_spec(nid, map_mod)
    if not spec_path.is_file():
        return False, ["no spec"]
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    if run([sys.executable, str(SCRIPTS / "build-cn-course.py"), "--spec", str(spec_path)]) != 0:
        return False, ["build failed"]
    sync_map_assets(course_dir, spec, maps_mod)
    if not skip_finalize:
        if run([sys.executable, str(SCRIPTS / "finalize-courseware.py"), str(course_dir), "--no-audio"]) != 0:
            return False, ["finalize failed"]
    errs = qc_one(course_dir)
    return len(errs) == 0, errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subjects", default="history,geography,english,chinese")
    ap.add_argument("--stage", default="middle,high")
    ap.add_argument("--node-ids", default="")
    ap.add_argument("--skip-finalize", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    maps_mod = load_apply_maps()
    map_mod = load_map_config()
    targets = list_targets(args)
    if args.limit:
        targets = targets[: args.limit]

    ok_n = fail_n = 0
    print(f"Repair {len(targets)} course(s)…\n")
    for i, nid in enumerate(targets, 1):
        ok, errs = repair_one(nid, maps_mod, map_mod, skip_finalize=args.skip_finalize)
        if ok:
            ok_n += 1
            print(f"[{i}/{len(targets)}] ✅ {nid}")
        else:
            fail_n += 1
            print(f"[{i}/{len(targets)}] ❌ {nid}: {', '.join(errs) or 'failed'}")
    print(f"\nDone: {ok_n} ok, {fail_n} failed")
    return 0 if fail_n == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
