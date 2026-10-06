#!/usr/bin/env python3
"""打印指定课件中最长卡片的原始 HTML（截断展示）。"""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cid = sys.argv[1]
html = open(os.path.join(ROOT, 'community', cid, 'index.html'), encoding='utf-8').read()
CARD_RE = re.compile(r'<div[^>]*class="[^"]*card[^"]*"[^>]*>([\s\S]*?)</div>', re.I)
best, best_len = None, 0
for m in CARD_RE.finditer(html):
    text = re.sub(r'<[^>]+>', '', m.group(1))
    text = re.sub(r'\s+', '', text)
    if len(text) > best_len:
        best_len = len(text)
        best = m
print('maxlen:', best_len)
print('--- raw html (first 1500 chars) ---')
print(best.group(0)[:1500])
