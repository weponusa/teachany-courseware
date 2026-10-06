#!/usr/bin/env python3
"""临时：检查去重逻辑会删掉什么，防止误删"""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply_courseware_shell import sections, title_of, text_len  # noqa

ROOT = Path(__file__).resolve().parents[1]

empty = 0
by_title = {}
samples = []

for p in sorted((ROOT / "community").glob("*/index.html"))[:120]:
    h = p.read_text(encoding="utf-8", errors="replace")
    for s, e, a, b in sections(h):
        t = title_of(a, b)
        if not t:
            empty += 1
            if len(samples) < 5:
                samples.append((p.parent.name, re.sub(r"\s+", " ", a)[:80],
                                re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", b))[:90]))
            continue
        by_title.setdefault(t, []).append((p.parent.name, text_len(b)))

print(f"抽样 120 个课件")
print(f"  无标题 section: {empty} 个  ← 若被当作同一 key 会误判为重复")
print(f"  有标题 section: {sum(len(v) for v in by_title.values())} 个")
print()
print("无标题 section 样例（这些不该参与去重）:")
for c, a, b in samples:
    print(f"  {c}")
    print(f"     attrs: {a}")
    print(f"     body : {b}")
print()
print("被判为「标题相同」最多的 TOP8:")
for t, v in sorted(by_title.items(), key=lambda x: -len(x[1]))[:8]:
    print(f"  「{t}」 {len(v)} 次  例: {v[:3]}")
