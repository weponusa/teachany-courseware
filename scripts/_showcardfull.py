#!/usr/bin/env python3
"""打印指定课件指定 class 卡片的完整匹配区域，供手工拆分参考。"""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cid, cls = sys.argv[1], sys.argv[2]
html = open(os.path.join(ROOT, 'community', cid, 'index.html'), encoding='utf-8').read()
i = html.find(cls)
start = html.rfind('<div', 0, i)
# 找这个 div 的匹配结束（深度计数）
depth = 0
pos = start
while True:
    m = re.compile(r'<div\b|</div>').search(html, pos)
    if not m:
        break
    depth += 1 if m.group(0) == '<div' else -1
    pos = m.end()
    if depth == 0:
        break
print('span:', start, pos, 'len:', pos - start)
print(html[start:pos][:4000])
