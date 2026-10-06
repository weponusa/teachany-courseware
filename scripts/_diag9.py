#!/usr/bin/env python3
"""临时：分析课件两套体系的结构，确认该删哪一套"""
import importlib.util
import re
from pathlib import Path

spec = importlib.util.spec_from_file_location("s", "scripts/apply-courseware-shell.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

for cid in ["math-m-circle-angle", "bio-circulation", "bio-classification"]:
    h = (Path("community") / cid / "index.html").read_text(encoding="utf-8", errors="replace")
    secs = S.sections(h, top_only=True)
    print("=" * 74)
    print(f"{cid}   顶层 section {len(secs)} 个")
    print()
    print("  类型分布:")
    from collections import Counter
    kinds = Counter()
    for s, e, a, b in secs:
        if "slide-page" in a:
            kinds["slide-page(分页容器)"] += 1
        elif re.search(r'id="([^"]+)"', a):
            kinds["有id(标准模块)"] += 1
        else:
            kinds["无id(内容模块)"] += 1
    for k, v in kinds.most_common():
        print(f"     {k:<22} {v}")
    print()
    print("  明细（class / id / 字数）:")
    for s, e, a, b in secs:
        cls = (re.search(r'class="([^"]*)"', a) or [None, ""])[1][:34]
        sid = (re.search(r'id="([^"]+)"', a) or [None, "·"])[1]
        n = S.text_len(b)
        t = S.title_of(a, b)[:18]
        print(f"     {cls:<34} {sid:<20}{n:>5}字  {t}")
    print()
