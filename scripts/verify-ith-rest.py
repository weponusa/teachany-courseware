#!/usr/bin/env python3
"""verify-ith-rest.py — 提取 it-h 5 课件的 posttest/practice/worked 纯文本验证"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for cid in ["it-h-sorting-searching", "it-h-data-structures"]:
    html = (ROOT / "community" / cid / "index.html").read_text(encoding="utf-8")
    print(f"========== {cid} ==========")
    for sid in ("posttest", "tiered-practice", "worked-example"):
        m = re.search(r'id="' + sid + r'"[\s\S]*?</section>', html)
        if m:
            t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(0))).strip()
            print(f"[{sid}] {t[:330]}")
        else:
            print(f"[{sid}] NOT FOUND")
    print()
