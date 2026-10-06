#!/usr/bin/env python3
"""show-bare-id.py — 提取裸课件ID在可见文本中的命中（排除属性/脚本/「」内）"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDS = ["sci-e-motion-speed", "sci-e-electricity-basic", "sci-e-moon-phases", "sci-e-solid-liquid-gas"]
for cid in IDS:
    html = (ROOT / "community" / cid / "index.html").read_text(encoding="utf-8", errors="replace")
    # 可见文本：去 script/style/注释/标签属性
    body = re.sub(r"<script[\s\S]*?</script>", "", html)
    body = re.sub(r"<style[\s\S]*?</style>", "", body)
    body = re.sub(r"<!--[\s\S]*?-->", "", body)
    # 找标签外文本中的 cid
    hits = []
    for m in re.finditer(re.escape(cid), body):
        # 前一个字符若是「、=、"、'、/ 则跳过（属性或已统计的「」）
        prev = body[m.start() - 1] if m.start() > 0 else ""
        if prev in "「=\"'/":
            continue
        seg = re.sub(r"<[^>]+>", " ", body[max(0, m.start() - 100):m.end() + 50])
        hits.append(re.sub(r"\s+", " ", seg).strip()[:140])
    print(f"===== {cid}: {len(hits)} 处裸ID =====")
    for h in hits[:4]:
        print("  ", h)
