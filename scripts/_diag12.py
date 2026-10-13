#!/usr/bin/env python3
"""临时：人工确认后删除 math-m-circle-angle 的重复模块

字符相似度无法识别这类重复（主题相同但用词不同，相似度仅 0.06~0.17），
故人工判定后删除：
  [1]  objectives(59字 学习目标)   与 [4] card(78字 学习目标) 重复 → 删 [1]
       保留字数更多、表述更完整的 card（4 条：区分/陈述/计算/证明）
  [19] module-1(300字 圆周角定理)  与 [6] card mod2(519字) 重复 → 删 [19]
       保留带 ABT 教学引入、内容更完整的模块二

保留 [12] lesson-focus(88字)：是简洁的核心结论（同弧圆周角=圆心角一半、
半圆所对圆周角是直角），与 [6] 的详细讲解互补，且为标准模块。
"""
import importlib.util
import re
from pathlib import Path

spec = importlib.util.spec_from_file_location("s", "scripts/apply-courseware-shell.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

cid = "math-m-circle-angle"
P = Path("community") / cid / "index.html"
html = P.read_text(encoding="utf-8", errors="replace")
secs = list(S.sections(html, top_only=True))

targets = []
for i, (s, e, a, b) in enumerate(secs):
    sid = (re.search(r'id="([^"]+)"', a) or [None, ""])[1]
    if sid in ("objectives", "module-1"):
        targets.append((i, sid, S.text_len(b)))
print("将删除:", targets)

for i, sid, n in sorted(targets, reverse=True):
    s, e = secs[i][0], secs[i][1]
    html = html[:s] + html[e:]
P.write_text(html, encoding="utf-8")
print("已删除，剩余顶层模块:", len(list(S.sections(html, top_only=True))))
