#!/usr/bin/env python3
"""临时：对比「课件原有模块」与「我补写模块」的 HTML 结构与样式类"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
c = sys.argv[1]
h = (ROOT / "community" / c / "index.html").read_text(encoding="utf-8", errors="replace")

print("=" * 70)
print("【1】课件中已有的正文模块（取第一个含 h2 的 section）")
for m in re.finditer(r'<section\b([^>]*)>([\s\S]*?)</section>', h):
    a, body = m.group(1), m.group(2)
    if 'knowledge-graph' in a:
        continue
    if '<h2' not in body:
        continue
    print("  section 属性:", re.sub(r'\s+', ' ', a)[:150])
    print("  前 700 字符:")
    print("   ", re.sub(r'\s+', ' ', body)[:700])
    break

print()
print("=" * 70)
print("【2】我补写的模块")
for sid in ("worked-example", "summary"):
    m = re.search(rf'<section\b([^>]*)\bid="{sid}"[\s\S]*?(?=</section>)', h)
    if m:
        print(f"  --- {sid} ---")
        print("  ", re.sub(r'\s+', ' ', m.group(0))[:600])

print()
print("=" * 70)
print("【3】CSS 里是否定义了这些类")
for cls in ("card", "section-title", "worked-example", "bioh-pitfall", "panel", "section"):
    n = len(re.findall(rf'\.{cls}\b', h))
    print(f"  .{cls:<16} 出现 {n} 次", "  ← 无定义!" if n == 0 else "")

print()
print("【4】是否有统一呈现基线")
print("  ", "统一呈现基线" in h)
