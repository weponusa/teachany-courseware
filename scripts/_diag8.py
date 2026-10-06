#!/usr/bin/env python3
"""临时：检查课件末尾模块——找出「凑数模块」"""
import importlib.util
import re
from pathlib import Path

spec = importlib.util.spec_from_file_location("s", "scripts/apply-courseware-shell.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

ROOT = Path(".")

for cid in ["bio-classification", "bio-h-organelles", "bio-circulation"]:
    h = (ROOT / "community" / cid / "index.html").read_text(encoding="utf-8", errors="replace")
    secs = S.sections(h, top_only=True)
    print("=" * 72)
    print(f"{cid}   顶层 section {len(secs)} 个")
    print(f"外壳已引入: {'courseware-shell.css' in h}")
    print()
    print("末尾 10 个模块（id / 标题 / 字数）:")
    for s, e, a, b in secs[-10:]:
        sid = (re.search(r'id="([^"]+)"', a) or [None, "(无id)"])[1]
        t = S.title_of(a, b) or "(无标题)"
        n = S.text_len(b)
        vis = "display:none" in b[:300]
        print(f"   {sid:<22} {n:>5}字  {'隐藏' if vis else '    '}  {t[:26]}")
    print()
