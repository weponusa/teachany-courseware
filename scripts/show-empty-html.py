#!/usr/bin/env python3
"""show-empty-html.py — 显示空 section 的原始 HTML"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOUNT_IDS = re.compile(r"tutor|kg|knowledge|hint|audio|dock|feedback|progress|nav|hero-infographic|slide-progress|course-version|skill-version")

for cid in ["chem-h-atom-structure-h", "ancient-china-h", "chem-h-biomolecules"]:
    html = (ROOT / "community" / cid / "index.html").read_text(encoding="utf-8", errors="replace")
    print(f"===== {cid} =====")
    n = 0
    for sm in re.finditer(r"<section\b([^>]*)>([\s\S]*?)</section>", html):
        attrs = sm.group(1)
        if MOUNT_IDS.search(attrs):
            continue
        t = re.sub(r"<[^>]+>", "", sm.group(2))
        t = re.sub(r"\s+", "", t)
        if len(t) < 20 and "<img" not in sm.group(2) and "<canvas" not in sm.group(2) \
           and "<video" not in sm.group(2) and "<figure" not in sm.group(2):
            print(f"  原始: <section{attrs[:150]}>{sm.group(2)[:120]!r}")
            n += 1
            if n >= 3:
                break
