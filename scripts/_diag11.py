#!/usr/bin/env python3
"""临时：打印指定课件模块两两相似度"""
import importlib.util
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("s", "scripts/apply-courseware-shell.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

h = Path("community/math-m-circle-angle/index.html").read_text(encoding="utf-8", errors="replace")
secs = list(S.sections(h, top_only=True))

pairs = [(1, 4, "学习目标"), (6, 19, "圆周角定理"), (6, 12, "模块二vs精讲"), (12, 19, "精讲vs定理")]
for i, j, name in pairs:
    sim = S.similarity(secs[i][3], secs[j][3])
    ni = S.text_len(secs[i][3])
    nj = S.text_len(secs[j][3])
    print(f"  [{i}] vs [{j}] {name:<14} 相似度={sim:.3f}  ({ni}字 vs {nj}字)")
