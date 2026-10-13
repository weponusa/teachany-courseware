#!/usr/bin/env python3
"""临时：判断「重复模块」哪些是真重复、哪些是合理的多种模块"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CASES = [
    ("bio-cell-life", ["concept-overview", "lesson-focus"]),
    ("bio-classification", ["objectives", "goals"]),
    ("chem-h-aluminum-compounds", ["knowledge-map", "knowledge-graph"]),
    ("bio-photosynthesis", ["pretest", "ta-standard-pretest"]),
    ("bio-circulation", ["sec-summary", "summary"]),
]

for cid, ids in CASES:
    h = (ROOT / "community" / cid / "index.html").read_text(encoding="utf-8", errors="replace")
    print("=" * 66)
    print(cid)
    for sid in ids:
        m = re.search(rf'<section\b([^>]*)\bid="{sid}"[^>]*>([\s\S]*?)</section>', h)
        if not m:
            print(f"  [{sid}] 不存在")
            continue
        body = re.sub(r"<[^>]+>", " ", m.group(2))
        body = re.sub(r"\s+", " ", body).strip()
        print(f"  [{sid}] {len(body)} 字")
        print(f"      {body[:190]}")
    print()
