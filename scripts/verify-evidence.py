#!/usr/bin/env python3
"""verify-evidence.py — 验证填充的证据页内容"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ids = sys.argv[1:] or ["chem-h-atom-structure-h", "chn-m-poetry-appreciation"]
for cid in ids:
    html = (ROOT / "community" / cid / "index.html").read_text(encoding="utf-8")
    m = re.search(r'id="knowledge-specific-evidence"[\s\S]*?</section>\s*<!-- evidence-filled -->', html)
    if not m:
        m = re.search(r'id="knowledge-specific-evidence"[\s\S]*?</section>', html)
    if m:
        t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(0))).strip()
        print(f"===== {cid} =====")
        print(t[:500])
        print()
