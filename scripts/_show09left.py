#!/usr/bin/env python3
"""列出 3 个课件当前仍超长的卡片文本（按最新口径）。"""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARD_RE = re.compile(r'<div[^>]*class="[^"]*card[^"]*"[^>]*>([\s\S]*?)</div>', re.I)
STRIP_RE = re.compile(r'<(script|style|svg|textarea|template|table|details|button)\b[\s\S]*?</\1>', re.I)
for cid in ['bio-h-organelles', 'hist-m-greece-rome', 'hist-m-opium-war']:
    html = open(os.path.join(ROOT, 'community', cid, 'index.html'), encoding='utf-8').read()
    for m in CARD_RE.finditer(html):
        inner_html = re.sub(r'^<div[^>]*>', '', m.group(0), flags=re.I)
        if re.search(r'class="[^"]*card', inner_html, re.I):
            continue
        t = STRIP_RE.sub('', m.group(1))
        t = re.sub(r'<(details|table)\b(?![\s\S]*?</\1>)[\s\S]*$', '', t, flags=re.I)
        t = re.sub(r'<[^>]+>', '', t)
        t = re.sub(r'\s+', '', t)
        cjk = len(re.findall(r'[\u4e00-\u9fff]', t))
        words = len(re.findall(r'[A-Za-z0-9]+', re.sub(r'[\u4e00-\u9fff]', ' ', t)))
        if cjk + words > 200:
            print(f'=== {cid} count={cjk + words}')
            print(t[:260])
            print()
