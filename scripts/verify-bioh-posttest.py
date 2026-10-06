#!/usr/bin/env python3
"""verify-bioh-posttest.py — 抽查 bio-h 课件的 posttest/tiered-practice 真伪"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for cid in ["bio-h-evolution-evidence", "bio-h-mitosis", "bio-h-enzyme"]:
    p = ROOT / "community" / cid / "index.html"
    html = p.read_text(encoding="utf-8")
    print(f"========== {cid} ==========")
    for sid in ("posttest", "tiered-practice", "worked-example"):
        m = re.search(r'id="' + sid + r'"[\s\S]*?</section>', html)
        if m:
            t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(0))).strip()
            print(f"[{sid}] {t[:280]}")
        else:
            print(f"[{sid}] NOT FOUND")
    print()
