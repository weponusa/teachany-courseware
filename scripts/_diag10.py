#!/usr/bin/env python3
"""临时：列出指定课件所有顶层模块的内容摘要，用于人工比对重复"""
import importlib.util
import re
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("s", "scripts/apply-courseware-shell.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

for cid in sys.argv[1:]:
    h = (Path("community") / cid / "index.html").read_text(encoding="utf-8", errors="replace")
    secs = S.sections(h, top_only=True)
    print("=" * 76)
    print(f"{cid}   顶层 {len(secs)} 个模块")
    print("=" * 76)
    for i, (s, e, a, b) in enumerate(secs):
        cls = (re.search(r'class="([^"]*)"', a) or [None, ""])[1]
        sid = (re.search(r'id="([^"]+)"', a) or [None, "·"])[1]
        t = S.title_of(a, b)
        n = S.text_len(b)
        body = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", b)).strip()
        print(f"\n[{i}] id={sid}  class={cls[:30]}")
        print(f"    标题: {t[:34]}   {n}字")
        print(f"    正文: {body[:150]}")
    print()
