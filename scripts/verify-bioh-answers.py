#!/usr/bin/env python3
"""verify-bioh-answers.py — 抽查 bio-h posttest 答案标注"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ids = sys.argv[1:] or ["bio-h-atp", "bio-h-photosynthesis", "bio-h-mendel-law-1",
                       "bio-h-dna-replication", "bio-h-immune-regulation", "bio-h-ecosystem"]
for cid in ids:
    html = (ROOT / "community" / cid / "index.html").read_text(encoding="utf-8")
    m = re.search(r'id="posttest"[\s\S]*?</section>', html)
    if not m:
        print(cid, "NO posttest")
        continue
    seg = m.group(0)
    q = re.search(r"</h2><p>([\s\S]{0,120}?)</p>", seg)
    btns = re.findall(r'data-a="([ABC])"( data-correct="1")?[^>]*>([^<]{0,45})', seg)
    correct = [b for b in btns if b[1]]
    sm = re.search(r"学习小结：([^<]{0,80})", seg)
    print(f"{cid}")
    print(f"  Q: {q.group(1)[:70] if q else '?'}")
    print(f"  正确项: {correct[0][0]}. {correct[0][2] if correct else '无!'}")
    print(f"  小结: {sm.group(1)[:60] if sm else '无'}")
