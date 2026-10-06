#!/usr/bin/env python3
"""临时：统计「同一课件内标题相同」模块，看 2039 从何而来"""
import importlib.util
import re
from collections import Counter
from pathlib import Path

spec = importlib.util.spec_from_file_location("s", "scripts/apply-courseware-shell.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

ROOT = Path(".")
dup_titles = Counter()
dup_examples = {}
n_files = 0

for p in sorted((ROOT / "community").glob("*/index.html"))[:200]:
    h = p.read_text(encoding="utf-8", errors="replace")
    secs = S.sections(h)
    by = {}
    for s, e, a, b in secs:
        t = S.title_of(a, b)
        if t and len(t) >= 2:
            by.setdefault(t, []).append((s, e, a, b, S.text_len(b)))
    got = False
    for t, g in by.items():
        if len(g) >= 2:
            dup_titles[t] += 1
            got = True
            if t not in dup_examples:
                dup_examples[t] = (p.parent.name, [(a[:60], n) for _, _, a, _, n in g])
    if got:
        n_files += 1

print(f"抽样 200 个课件，{n_files} 个存在「同课件内标题相同」的模块")
print()
print("重复标题 TOP12:")
for t, c in dup_titles.most_common(12):
    name, items = dup_examples[t]
    print(f"  「{t}」 出现在 {c} 个课件")
    print(f"      例 {name}: {items[:3]}")
