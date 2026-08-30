#!/usr/bin/env python3
"""临时：量化「重复 / 风格不统一 / 宽度不同」的规模"""
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

# 同类模块语义分组（一个课件里出现多个即视为重复）
GROUPS = {
    "学习目标": ["objectives", "learning-objectives", "goal"],
    "达标检测": ["posttest", "post-test", "posttest2"],
    "课前诊断": ["pretest", "pre-test"],
    "知识图谱": ["knowledge-graph", "knowledge-map"],
    "小结/总结": ["summary", "conclusion", "wrap-up"],
    "范例": ["worked-example", "example"],
    "方法": ["lesson-method", "method"],
    "知识精讲": ["lesson-focus", "core-concept", "learn", "concept"],
    "深层理解": ["deep-understanding", "deep"],
    "练习": ["practice", "exercise", "drill"],
}

dup_stat = Counter()
dup_examples = {}
width_stat = Counter()
css_size = []
var_missing = Counter()

for p in sorted(COMMUNITY.glob("*/index.html")):
    h = p.read_text(encoding="utf-8", errors="replace")
    ids = re.findall(r'<section\b[^>]*\bid="([^"]+)"', h)

    # 1) 重复模块
    for g, keys in GROUPS.items():
        hits = [i for i in ids if any(k in i for k in keys)]
        if len(hits) > 1:
            dup_stat[g] += 1
            dup_examples.setdefault(g, (p.parent.name, hits))

    # 2) 主容器宽度
    ws = set(re.findall(r'max-width\s*:\s*(\d{3,4})px', h))
    for w in ws:
        width_stat[w] += 1

    # 3) CSS 规模与变量
    styles = re.findall(r'<style[^>]*>([\s\S]*?)</style>', h)
    css_size.append(sum(len(s) for s in styles))
    for v in ("--text", "--card", "--border", "--primary"):
        if f"{v}:" not in h:
            var_missing[v] += 1

n = len(list(COMMUNITY.glob("*/index.html")))
print(f"课件总数 {n}")
print()
print("【1】重复模块（同一课件出现多个同类模块）")
for g, c in dup_stat.most_common(10):
    name, hits = dup_examples[g]
    print(f"   {g:<10} {c:>3} 个课件   例: {name} -> {hits[:3]}")
print()
print("【2】max-width 取值分布（前10）")
for w, c in width_stat.most_common(10):
    print(f"   {w}px  {c:>3} 个课件")
print(f"   → 共 {len(width_stat)} 种不同宽度")
print()
print("【3】CSS 规模")
css_size.sort()
print(f"   最小 {css_size[0]} / 中位 {css_size[len(css_size)//2]} / 最大 {css_size[-1]} 字符")
print(f"   → 各课件自带样式量差异达 {css_size[-1]/max(1,css_size[0]):.0f} 倍")
print()
print("【4】缺少关键 CSS 变量的课件数")
for v, c in var_missing.most_common():
    print(f"   {v:<10} 缺 {c:>3} 个课件")
