#!/usr/bin/env python3
"""临时：列出将被去重删除的模块，人工确认是否真重复"""
import importlib.util
import re
from pathlib import Path

spec = importlib.util.spec_from_file_location("s", "scripts/apply-courseware-shell.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

ROOT = Path(".")
shown = 0

for p in sorted((ROOT / "community").glob("*/index.html")):
    if shown >= 8:
        break
    h = p.read_text(encoding="utf-8", errors="replace")
    secs = S.sections(h, top_only=True)
    by = {}
    for s, e, a, b in secs:
        t = S.title_of(a, b)
        if t and len(t) >= 2:
            by.setdefault(t, []).append((s, e, a, b))
    for t, g in by.items():
        if len(g) < 2:
            continue
        gs = sorted(g, key=lambda x: -S.text_len(x[3]))
        keep, dups = gs[0], gs[1:]
        to_del = [d for d in dups if S.text_len(d[3]) <= S.text_len(keep[3]) * 0.75]
        if not to_del:
            continue
        print(f"=== {p.parent.name}  标题「{t}」")
        print(f"  保留 {S.text_len(keep[3])} 字 | {re.sub(r'\\s+', ' ', keep[2])[:70]}")
        for d in to_del:
            print(f"  删除 {S.text_len(d[3])} 字 | {re.sub(r'\\s+', ' ', d[2])[:70]}")
            body = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", d[3])).strip()
            print(f"       内容: {body[:110]}")
        print()
        shown += 1
        break
