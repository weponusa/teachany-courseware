#!/usr/bin/env python3
"""final-verify-all.py — 51 课件最终全量验证：validator + 假模块复扫 + quiz 结构完整性"""
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
src = (ROOT / "scripts/replace-fake-canvas.py").read_text(encoding="utf-8")
ids = sorted(set(re.findall(r'^\s*"((?:bio|it)-h-[a-z0-9-]+)": dict\(', src, re.M)))
print(f"共 {len(ids)} 个课件")

# 1) validator
fails = []
for cid in ids:
    r = subprocess.run(["node", "scripts/validate-courseware.cjs", f"community/{cid}"],
                       capture_output=True, text=True, cwd=ROOT)
    m = re.search(r"总评：(\d+)/(\d+)", r.stdout)
    if not m or m.group(1) != "22":
        fails.append((cid, m.group(0) if m else "PARSE_FAIL"))
print(f"validator: {len(ids)-len(fails)}/{len(ids)} 个 22/22")
for f in fails:
    print("  ❌", f)

# 2) 假模块特征复扫（精准签名）
FAKE = {
    "canvas假": [r"系统响应曲线", r"function drawModel\(", r"function drawBio\("],
    "课标点": [r">课标点\s*\d<"],
    "五镜头空话": [r"先描述题干现象或数据变化", r"题目给了什么输入和现象？",
                r"变量、规则、结构分别是什么？", r"换一个场景还能不能用？"],
    "前测模板": [r"只背名词就够了", r"记住定义，不用解释过程"],
    "概念模板": [r"只要记住定义，就一定能解决", r"定义就是全部"],
    "后测模板": [r"一个完整答案最应该包含什么", r"只写一段代码",
              r"下面哪一种答案最符合高中生物的科学解释要求"],
    "练习空话": [r"说出本课一个定义", r"分析一个校园系统变量",
              r"用一句话说清\s*\S+\s*的核心机制，必须包含"],
    "示例模板": [r"第一步，识别输入变量", r"第一句写可观察现象，第二句写本课机制"],
    "小结模板": [r"的关键不是记住一个孤立词"],
}
residue = []
for cid in ids:
    html = (ROOT / "community" / cid / "index.html").read_text(encoding="utf-8")
    for name, pats in FAKE.items():
        for pat in pats:
            if re.search(pat, html):
                residue.append((cid, name, pat[:30]))
print(f"假模块残留: {len(residue)}")
for r in residue[:15]:
    print("  ⚠️", r)

# 3) quiz 结构完整性（每课件 pretest/concept/post 三题都有且只有一个 data-correct）
struct_bad = []
for cid in ids:
    html = (ROOT / "community" / cid / "index.html").read_text(encoding="utf-8")
    for sid in ("pretest", "concept-check", "posttest"):
        m = re.search(r'id="' + sid + r'"[\s\S]*?</section>', html)
        if not m:
            struct_bad.append((cid, sid, "缺section"))
            continue
        seg = m.group(0)
        btns = re.findall(r'class="quiz-option"', seg)
        correct = re.findall(r'data-correct="1"', seg)
        if len(btns) < 3 or len(correct) != 1:
            struct_bad.append((cid, sid, f"按钮{len(btns)} 正确标记{len(correct)}"))
print(f"quiz结构: {'全部正常' if not struct_bad else str(len(struct_bad)) + ' 异常'}")
for s in struct_bad[:10]:
    print("  ⚠️", s)
