#!/usr/bin/env python3
"""临时：查看课件里 h2 / .card / .section 的真实 CSS 定义"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
c = sys.argv[1]
h = (ROOT / "community" / c / "index.html").read_text(encoding="utf-8", errors="replace")

# 只看 <style> 块
styles = re.findall(r'<style[^>]*>([\s\S]*?)</style>', h)
css = "\n".join(styles)
print(f"课件 {c}，style 块 {len(styles)} 个，CSS 共 {len(css)} 字符")
print()

for sel in (r'h2[,\s{]', r'\.section\s*\{', r'\.card\s*\{', r'\.section-title', r'\bp\s*\{'):
    print(f"--- 选择器 {sel} ---")
    found = False
    for m in re.finditer(rf'([^{{}}]*{sel}[^{{}}]*)\{{([^}}]*)\}}', css):
        s = re.sub(r'\s+', ' ', m.group(1)).strip()
        b = re.sub(r'\s+', ' ', m.group(2)).strip()
        print(f"   {s} {{ {b[:130]} }}")
        found = True
        if not found:
            pass
    if not found:
        print("   (未定义)")
    print()

print("--- 全局 CSS 变量 ---")
for m in re.finditer(r'(--[\w-]+)\s*:\s*([^;]+);', css):
    print(f"   {m.group(1)}: {m.group(2).strip()[:40]}")
