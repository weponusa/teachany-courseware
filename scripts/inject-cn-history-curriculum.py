#!/usr/bin/env python3
"""
中国史课标知识灌注（国家课标 + 统编口径）。

  python3 scripts/inject-cn-history-curriculum.py
  python3 scripts/inject-cn-history-curriculum.py --node-id hist-h-ancient-civ
  python3 scripts/inject-cn-history-curriculum.py --re-emit-kcp
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from cn_history_curriculum import enrich_kp_satellite, load_junior_parser  # noqa: E402

KP_HISTORY = ROOT / "data" / "kp" / "history"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--node-id", action="append")
    ap.add_argument("--re-emit-kcp", action="store_true")
    ap.add_argument("--force", action="store_true", help="Rewrite all cn history satellites")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    junior = load_junior_parser()
    if junior:
        print(f"义教课标已解析：中国古代史小节 {len(junior.sections)} 个，学业要求 {len(junior.academic_requirements_ancient)} 条")
    else:
        print("WARN: 未找到义教 history.md，仅使用节点课标点与内置价值观框架")

    changed = 0
    for fp in sorted(KP_HISTORY.glob("*.json")):
        nid = fp.stem
        if args.node_id and nid not in args.node_id:
            continue
        import json as _json

        data = _json.loads(fp.read_text(encoding="utf-8"))
        if enrich_kp_satellite(data, junior, force=args.force):
            changed += 1
            if not args.dry_run:
                fp.write_text(
                    _json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                print(f"OK  {nid}")
            else:
                print(f"DRY {nid}")

    print(f"updated {changed} satellites")
    if args.re_emit_kcp and not args.dry_run:
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "batch-emit-knowledge-context.py"), "--subject", "history"],
            cwd=ROOT,
            check=False,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
