#!/usr/bin/env python3
"""临时：分析课件「两套体系」的字数分布，验证保留策略

A 套（原课件正文）: class 以 card 开头的模块（card / card mod2 / card success…）
B 套（标准补丁）  : class 含 teachany-upgrade-block 或 mathm-depth 等
共用功能模块      : knowledge-graph / phet-lab / hero-infographic 等不参与两套之争
"""
import importlib.util
import re
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("s", "scripts/apply-courseware-shell.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

B_MARK = re.compile(r"teachany-upgrade-block|mathm-depth|core-knowledge-module")
SHARED = re.compile(r'id="(knowledge-graph|phet-lab|hero-infographic|'
                    r'teachany-ai-tutor-card|teachany-audio-player)"')


def classify(a):
    cls = (re.search(r'class="([^"]*)"', a) or [None, ""])[1]
    sid = (re.search(r'id="([^"]+)"', a) or [None, ""])[1]
    if SHARED.search(sid or ""):
        return "shared"
    if B_MARK.search(cls):
        return "B"
    if re.match(r"card", cls):
        return "A"
    if sid in ("anchor", "objectives", "pretest", "posttest", "lesson-focus",
               "lesson-method", "deep-understanding", "error-clinic",
               "error-watch", "memory-anchor", "course-nav-map", "summary",
               "worked-example"):
        return "B"          # 标准 id 也归 B（后加的标准模块）
    return "other"


for cid in sys.argv[1:]:
    h = (Path("community") / cid / "index.html").read_text(encoding="utf-8", errors="replace")
    secs = S.sections(h, top_only=True)
    stat = {"A": [0, 0], "B": [0, 0], "shared": [0, 0], "other": [0, 0]}
    for s, e, a, b in secs:
        k = classify(a)
        stat[k][0] += 1
        stat[k][1] += S.text_len(b)
    print(f"{cid}")
    print(f"   A套(card正文)   {stat['A'][0]:>2} 个模块  {stat['A'][1]:>5} 字")
    print(f"   B套(标准补丁)   {stat['B'][0]:>2} 个模块  {stat['B'][1]:>5} 字")
    print(f"   共用功能       {stat['shared'][0]:>2} 个模块  {stat['shared'][1]:>5} 字")
    print(f"   其他           {stat['other'][0]:>2} 个模块  {stat['other'][1]:>5} 字")
    if stat["A"][1] and stat["B"][1]:
        win = "A" if stat["A"][1] > stat["B"][1] else "B"
        print(f"   → 内容更完整: {win} 套（{max(stat['A'][1],stat['B'][1])} 字）")
    print()
