#!/usr/bin/env python3
"""Build, illustrate, finalize and preflight a batch of CN gap courseware.

Usage:
  python3 run-cn-gap-batch.py --stage high --subject info-tech
  python3 run-cn-gap-batch.py --node-ids it-h-algorithm-concept,it-h-network-basics
  python3 run-cn-gap-batch.py --stage high --subject math --limit 4 --skip-agnes
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run(cmd: list[str], *, check: bool = True) -> int:
    print(f"\n$ {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=ROOT)
    if check and r.returncode != 0:
        raise SystemExit(r.returncode)
    return r.returncode


def load_gaps(stage: str, subject: str, node_ids: list[str]) -> list[dict]:
    if node_ids:
        out = []
        for nid in node_ids:
            out.append({"node_id": nid.strip()})
        return out
    out = subprocess.check_output(
        [sys.executable, str(SCRIPTS / "list-cn-gaps.py"), "--stage", stage, "--subject", subject],
        cwd=ROOT, text=True,
    )
    # re-import by running export to temp
    tmp = ROOT / "scripts" / ".gap-batch-tmp.json"
    run([sys.executable, str(SCRIPTS / "list-cn-gaps.py"), "--stage", stage, "--subject", subject, "--export", str(tmp)], check=True)
    return json.loads(tmp.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="")
    ap.add_argument("--subject", default="")
    ap.add_argument("--node-ids", default="", help="Comma-separated node ids")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--skip-agnes", action="store_true")
    ap.add_argument("--skip-finalize", action="store_true")
    args = ap.parse_args()

    node_ids = [x.strip() for x in args.node_ids.split(",") if x.strip()]
    if node_ids:
        gaps = [{"node_id": n} for n in node_ids]
    else:
        if not args.stage or not args.subject:
            print("Need --stage and --subject, or --node-ids", file=sys.stderr)
            return 2
        tmp = ROOT / "scripts" / ".gap-batch-tmp.json"
        run([
            sys.executable, str(SCRIPTS / "list-cn-gaps.py"),
            "--stage", args.stage, "--subject", args.subject, "--export", str(tmp),
        ])
        gaps = json.loads(tmp.read_text(encoding="utf-8"))
        tmp.unlink(missing_ok=True)

    if args.limit > 0:
        gaps = gaps[: args.limit]

    if not gaps:
        print("No gaps to process.")
        return 0

    print(f"Processing {len(gaps)} courseware nodes…")
    specs_dir = SCRIPTS / "cn-specs"
    specs_dir.mkdir(parents=True, exist_ok=True)
    ok = 0
    failed = []

    for g in gaps:
        nid = g["node_id"]
        print(f"\n{'='*60}\n=== {nid} ===")
        try:
            run([sys.executable, str(SCRIPTS / "kp-to-cn-spec.py"), "--node-id", nid, "--out", str(specs_dir), "--write-batch"])
            spec = specs_dir / f"{nid}.json"
            run([sys.executable, str(SCRIPTS / "build-cn-course.py"), "--spec", str(spec)])
            if not args.skip_agnes:
                batch = specs_dir / f"batch-{nid}.json"
                run([
                    sys.executable, str(SCRIPTS / "agnes-image-gen.py"),
                    "--course-id", nid,
                    "--batch", str(batch),
                    "--out-dir", f"community/{nid}/assets",
                ])
            if not args.skip_finalize:
                spec_data = json.loads(spec.read_text(encoding="utf-8"))
                pwd = spec_data["password_hint"]
                run([
                    sys.executable, str(SCRIPTS / "set-feedback-password.py"),
                    f"community/{nid}/manifest.json", "--password", pwd, "--hint", pwd,
                ])
                run([sys.executable, str(SCRIPTS / "finalize-courseware.py"), f"community/{nid}"])
                run([
                    sys.executable, str(SCRIPTS / "preflight-publish.py"),
                    f"community/{nid}", "--no-finalize",
                ])
            ok += 1
        except SystemExit:
            failed.append(nid)
            print(f"❌ failed: {nid}")

    if ok and not args.skip_finalize:
        qc_targets = [str(ROOT / "community" / g["node_id"]) for g in gaps if g["node_id"] not in failed]
        if qc_targets:
            print("\n🔍 Running batch QC…")
            qc_cmd = [sys.executable, str(SCRIPTS / "qc-cn-batch.py"), *qc_targets]
            if subprocess.run(qc_cmd, cwd=ROOT).returncode != 0:
                print("❌ Batch QC failed — fix before push")
                return 1

    print(f"\nDone {ok}/{len(gaps)}")
    if failed:
        print("Failed:", ", ".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
