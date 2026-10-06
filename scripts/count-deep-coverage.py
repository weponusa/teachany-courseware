#!/usr/bin/env python3
"""Count deep_textbook_snippets coverage for TeachAny KP satellites."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
KP_INDEX_PATH = ROOT / "data" / "kp" / "_index.json"
NODE_INDEX_PATH = ROOT / "data" / "node-index.json"
REPORT_DIR = ROOT / "reports"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def pct(n: int, total: int) -> str:
    return f"{n / total * 100:.1f}%" if total else "0.0%"


def main() -> int:
    parser = argparse.ArgumentParser(description="Count deep_textbook_snippets coverage")
    parser.add_argument("--curriculum", default="cn", help="curriculum filter, default cn; use all for all")
    parser.add_argument("--out", default="", help="optional CSV output path")
    args = parser.parse_args()

    idx = load_json(KP_INDEX_PATH).get("kps", {})
    node_idx = load_json(NODE_INDEX_PATH).get("nodes", {}) if NODE_INDEX_PATH.exists() else {}
    by_subject: dict[str, Counter[str]] = defaultdict(Counter)
    missing: list[dict[str, Any]] = []
    total = 0
    deep_total = 0
    snippet_total = 0

    for kp_id, rel in sorted(idx.items()):
        path = ROOT / rel
        if not path.exists():
            continue
        data = load_json(path)
        curriculum = data.get("curriculum") or node_idx.get(kp_id, {}).get("curriculum") or ""
        if args.curriculum != "all" and curriculum != args.curriculum:
            continue
        subject = data.get("subject") or node_idx.get(kp_id, {}).get("subject") or "unknown"
        deep = (data.get("supplements") or {}).get("deep_textbook_snippets") or []
        total += 1
        by_subject[subject]["total"] += 1
        if deep:
            deep_total += 1
            snippet_total += len(deep)
            by_subject[subject]["deep"] += 1
            by_subject[subject]["snippets"] += len(deep)
        else:
            by_subject[subject]["missing"] += 1
            missing.append({
                "kp_id": kp_id,
                "name": data.get("name") or node_idx.get(kp_id, {}).get("name_zh") or "",
                "subject": subject,
                "stage": data.get("stage") or node_idx.get(kp_id, {}).get("stage") or "",
                "domain": data.get("domain_name") or node_idx.get(kp_id, {}).get("domain") or "",
                "path": rel,
            })

    rows = []
    for subject in sorted(by_subject):
        c = by_subject[subject]
        rows.append({
            "subject": subject,
            "total": c["total"],
            "deep": c["deep"],
            "missing": c["total"] - c["deep"],
            "snippets": c["snippets"],
            "coverage": pct(c["deep"], c["total"]),
        })

    print(f"curriculum,total,deep,missing,snippets,coverage")
    print(f"{args.curriculum},{total},{deep_total},{total - deep_total},{snippet_total},{pct(deep_total, total)}")
    print("\nsubject,total,deep,missing,snippets,coverage")
    for r in rows:
        print(f"{r['subject']},{r['total']},{r['deep']},{r['missing']},{r['snippets']},{r['coverage']}")

    if args.out:
        out = Path(args.out)
    else:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        out = REPORT_DIR / f"deep-coverage-{args.curriculum}-{datetime.now().strftime('%Y-%m-%d')}.csv"
    with out.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["subject", "total", "deep", "missing", "snippets", "coverage"])
        writer.writeheader()
        writer.writerows(rows)
    missing_path = out.with_suffix(".missing.json")
    missing_path.write_text(json.dumps(missing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nwritten: {out}")
    print(f"missing: {missing_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
