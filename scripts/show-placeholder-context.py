#!/usr/bin/env python3
"""show-placeholder-context.py — 显示占位命中上下文"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDS = ["bio-m-biosphere", "ext-16a14ef", "ext-1a79c832", "physics-ap-1-shm",
       "reading-academy", "sci-e-motion-speed", "sci-e-electricity-basic", "sci-e-3d-printing-blender"]
WORDS = [r"TODO", r"待补充", r"待完善", r"待填写", r"placeholder", r"\{\{[^}]{1,30}\}\}", r"此处省略"]

for cid in IDS:
    html = (ROOT / "community" / cid / "index.html").read_text(encoding="utf-8", errors="replace")
    print(f"========== {cid} ==========")
    for m in list(re.finditer(r"「[a-z][a-z0-9]*(?:-[a-z0-9]+)+」", html))[:3]:
        seg = re.sub(r"<[^>]+>", " ", html[max(0, m.start() - 120):m.end() + 60])
        print("  [「ID」]", re.sub(r"\s+", " ", seg).strip()[:150])
    for w in WORDS:
        for m in list(re.finditer(w, html))[:2]:
            seg = re.sub(r"<[^>]+>", " ", html[max(0, m.start() - 100):m.end() + 60])
            print(f"  [{w}]", re.sub(r"\s+", " ", seg).strip()[:140])
    # h1/title
    h1 = re.search(r"<h1[^>]*>([\s\S]{0,80}?)</h1>", html)
    tm = re.search(r"<title>([^<]{0,80})", html)
    print("  [h1]", re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else "无", "| [title]", tm.group(1).strip() if tm else "无")
