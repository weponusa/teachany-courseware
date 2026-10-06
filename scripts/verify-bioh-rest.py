#!/usr/bin/env python3
"""verify-bioh-rest.py — 验证 bio-h 修复后内容"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ids = sys.argv[1:] or ["bio-h-enzyme", "bio-h-mitosis"]
for cid in ids:
    html = (ROOT / "community" / cid / "index.html").read_text(encoding="utf-8")
    print(f"========== {cid} ==========")
    for sid in ("posttest", "tiered-practice", "worked-example"):
        m = re.search(r'id="' + sid + r'"[\s\S]*?</section>', html)
        if m:
            t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(0))).strip()
            print(f"[{sid}] {t[:340]}")
    print()
