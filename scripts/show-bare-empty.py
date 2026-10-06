#!/usr/bin/env python3
"""show-bare-empty.py — 抽查 bare_id_visible 和 empty_sections 命中"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOUNT_IDS = re.compile(r"tutor|kg|knowledge|hint|audio|dock|feedback|progress|nav|hero-infographic|slide-progress|course-version|skill-version")

for cid in ["ancient-china-h", "bio-characteristics", "bio-classification", "bio-m-ecosystem-junior"]:
    html = (ROOT / "community" / cid / "index.html").read_text(encoding="utf-8", errors="replace")
    body = re.sub(r"<script[\s\S]*?</script>", "", html)
    body = re.sub(r"<style[\s\S]*?</style>", "", body)
    body = re.sub(r"<!--[\s\S]*?-->", "", body)
    print(f"===== {cid} bare_id =====")
    n = 0
    for mm in re.finditer(re.escape(cid), body):
        prev = body[mm.start() - 1] if mm.start() > 0 else ""
        if prev in "「=\"'/.:":
            continue
        seg = re.sub(r"<[^>]+>", " ", body[max(0, mm.start() - 80):mm.end() + 40])
        print("  ", re.sub(r"\s+", " ", seg).strip()[:120])
        n += 1
        if n >= 3:
            break

for cid in ["ancient-china-h", "chem-h-atom-structure-h", "chem-h-biomolecules"]:
    html = (ROOT / "community" / cid / "index.html").read_text(encoding="utf-8", errors="replace")
    print(f"===== {cid} empty_sections =====")
    shown = 0
    for sm in re.finditer(r"<section\b([^>]*)>([\s\S]*?)</section>", html):
        attrs = sm.group(1)
        if MOUNT_IDS.search(attrs):
            continue
        t = re.sub(r"<[^>]+>", "", sm.group(2))
        t = re.sub(r"\s+", "", t)
        if len(t) < 20 and "<img" not in sm.group(2) and "<canvas" not in sm.group(2) \
           and "<video" not in sm.group(2) and "<figure" not in sm.group(2):
            idm = re.search(r'id="([^"]+)"', attrs)
            print(f"   id={idm.group(1) if idm else '?'} 文本={len(t)}字 内容={t[:40]!r}")
            shown += 1
            if shown >= 3:
                break
