#!/usr/bin/env python3
"""临时：对两套并存的课件逐个输出 A/B 字数与保留建议"""
import importlib.util
import re
from pathlib import Path

spec = importlib.util.spec_from_file_location("s", "scripts/apply-courseware-shell.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

B_MARK = re.compile(r"teachany-upgrade-block|mathm-depth|core-knowledge-module")
STD = {"anchor", "objectives", "pretest", "posttest", "lesson-focus", "lesson-method",
       "deep-understanding", "error-clinic", "error-watch", "memory-anchor",
       "course-nav-map", "summary", "worked-example"}
SHARED = re.compile(r'id="(knowledge-graph|phet-lab|hero-infographic|'
                    r'teachany-ai-tutor-card|teachany-audio-player|external-lab|'
                    r'interactive-model|video-demo|micro-video)"')


def course_stat(cid):
    h = (Path("community") / cid / "index.html").read_text(encoding="utf-8", errors="replace")
    A = [0, 0]   # 模块数, 字数
    B = [0, 0]
    for s, e, a, b in S.sections(h, top_only=True):
        cls = (re.search(r'class="([^"]*)"', a) or [None, ""])[1]
        sid = (re.search(r'id="([^"]+)"', a) or [None, ""])[1]
        if SHARED.search(sid or ""):
            continue
        n = S.text_len(b)
        if re.match(r"card", cls):
            A[0] += 1
            A[1] += n
        elif B_MARK.search(cls) or sid in STD:
            B[0] += 1
            B[1] += n
    return A, B


rows = []
for p in sorted(Path("community").glob("*/index.html")):
    cid = p.parent.name
    A, B = course_stat(cid)
    if A[0] == 0 or B[0] == 0:
        continue
    win = "A" if A[1] > B[1] else "B"
    rows.append((cid, A, B, win))

print(f"两套并存 {len(rows)} 个课件：")
print(f"{'课件':<38}{'A套(card)':>12}{'B套(标准)':>12}   保留")
print("-" * 74)
for cid, A, B, win in rows:
    print(f"{cid:<38}{A[1]:>8}字/{A[0]}个{B[1]:>8}字/{B[0]}个   → {win}")
