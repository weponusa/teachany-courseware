#!/usr/bin/env python3
"""打印复杂卡片匹配区域（剔除 script 后）的纯文本与 HTML 开头。"""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cid = sys.argv[1]
html = open(os.path.join(ROOT, 'community', cid, 'index.html'), encoding='utf-8').read()
CARD_RE = re.compile(r'<div[^>]*class="[^"]*card[^"]*"[^>]*>([\s\S]*?)</div>', re.I)
STRIP_RE = re.compile(r'<(script|style|svg|textarea|template)\b[\s\S]*?</\1>', re.I)
for m in CARD_RE.finditer(html):
    inner = m.group(1)
    if '<div' not in inner:
        continue
    t = STRIP_RE.sub('', inner)
    t = re.sub(r'<[^>]+>', '', t)
    t = re.sub(r'\s+', '', t)
    if len(t) > 200:
        print('== len', len(t))
        print('TEXT:', t[:400])
        print('HTML:', inner[:600].replace('\n', ' '))
        print()
