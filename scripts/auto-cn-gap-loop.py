#!/usr/bin/env python3
"""Auto-continue CN gap courseware generation with QC between batches.

Usage:
  python3 auto-cn-gap-loop.py --batches 3          # 3 batches × 5 = 15 courses
  python3 auto-cn-gap-loop.py --until-empty        # until all gaps filled (long!)
  python3 auto-cn-gap-loop.py --batches 2 --stage middle --subject history
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

# Largest gaps first
DEFAULT_QUEUE = [
    ("middle", "history"),
    ("high", "history"),
    ("middle", "geography"),
    ("high", "chinese"),
    ("high", "english"),
    ("middle", "english"),
]


def gap_count(stage: str, subject: str) -> int:
    tmp = SCRIPTS / ".gap-loop-tmp.json"
    subprocess.run(
        [sys.executable, str(SCRIPTS / "list-cn-gaps.py"), "--stage", stage, "--subject", subject, "--export", str(tmp)],
        cwd=ROOT, check=True,
    )
    n = len(json.loads(tmp.read_text(encoding="utf-8")))
    tmp.unlink(missing_ok=True)
    return n


def run(cmd: list[str]) -> int:
    print(f"\n$ {' '.join(cmd)}", flush=True)
    return subprocess.run(cmd, cwd=ROOT).returncode


def commit_batch(msg: str) -> int:
    run([sys.executable, str(SCRIPTS / "rebuild-index.py")])
    run(["git", "add", "community/", "scripts/cn-specs/", "scripts/cn-gaps.json",
         "registry.json", "registry-v2.json", "community/index.json", "data/"])
    return run(["git", "commit", "-m", msg])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batches", type=int, default=1, help="Number of 5-course batches")
    ap.add_argument("--batch-size", type=int, default=5)
    ap.add_argument("--until-empty", action="store_true")
    ap.add_argument("--stage", default="")
    ap.add_argument("--subject", default="")
    ap.add_argument("--no-commit", action="store_true")
    ap.add_argument("--no-push", action="store_true")
    args = ap.parse_args()

    queue = [(args.stage, args.subject)] if args.stage and args.subject else DEFAULT_QUEUE
    batches_done = 0
    target = 9999 if args.until_empty else args.batches

    while batches_done < target:
        progressed = False
        for stage, subject in queue:
            if batches_done >= target:
                break
            n = gap_count(stage, subject)
            if n == 0:
                continue
            limit = min(args.batch_size, n)
            print(f"\n{'='*70}\n📦 Batch {batches_done+1}: {stage}/{subject} ({n} gaps, taking {limit})")
            rc = run([
                sys.executable, str(SCRIPTS / "run-cn-gap-batch.py"),
                "--stage", stage, "--subject", subject, "--limit", str(limit),
            ])
            if rc != 0:
                print(f"❌ Batch failed for {stage}/{subject}")
                return rc
            batches_done += 1
            progressed = True
            # refresh gap manifest
            run([sys.executable, str(SCRIPTS / "list-cn-gaps.py"), "--export", str(SCRIPTS / "cn-gaps.json")])
            if not args.no_commit:
                ts = datetime.now().strftime("%Y-%m-%d")
                msg = f"Add CN {stage} {subject} courseware batch {batches_done} ({limit} lessons with QC)."
                if commit_batch(msg) != 0:
                    print("⚠️  Nothing to commit or commit failed")
                elif not args.no_push:
                    run(["git", "push", "origin", "main"])
            if batches_done >= target:
                break
        if not progressed:
            print("\n✅ No more gaps in queue.")
            break

    run([sys.executable, str(SCRIPTS / "list-cn-gaps.py")])
    print(f"\nFinished {batches_done} batch(es).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
