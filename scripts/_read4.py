#!/usr/bin/env python3
"""临时：读取指定课件的核心正文，供人工撰写模块参考"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

for c in sys.argv[1:]:
    h = (ROOT / "community" / c / "index.html").read_text(encoding="utf-8", errors="replace")
    t = re.search(r"<title>([^<]+)", h)
    nm = re.split(r"[·|｜]", t.group(1))[0].strip() if t else c
    body = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", h)
    body = re.sub(r"<[^>]+>", " ", body)
    body = re.sub(r"\s+", " ", body)
    i = body.find("学习目标")
    seg = body[i:i + 300].strip() if i > 0 else body[180:460].strip()
    print("###", c, "|", nm)
    print("  ", seg)
    print()
