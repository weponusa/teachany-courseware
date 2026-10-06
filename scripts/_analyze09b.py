#!/usr/bin/env python3
"""用修正后的 #09 口径（剔除 script/style/svg/textarea/template）重测。"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
recs = json.load(open(os.path.join(ROOT, 'qc-all-report.json'), encoding='utf-8'))
f09 = [r['id'] for r in recs if any(x.startswith('#09') for x in r['failed'])]
CARD_RE = re.compile(r'<div[^>]*class="[^"]*card[^"]*"[^>]*>([\s\S]*?)</div>', re.I)
STRIP_RE = re.compile(r'<(script|style|svg|textarea|template)\b[\s\S]*?</\1>', re.I)
genuine = []
for cid in f09:
    html = open(os.path.join(ROOT, 'community', cid, 'index.html'), encoding='utf-8').read()
    long_n, max_len = 0, 0
    for m in CARD_RE.finditer(html):
        text = STRIP_RE.sub('', m.group(1))
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\s+', '', text)
        max_len = max(max_len, len(text))
        if len(text) > 200:
            long_n += 1
    if long_n:
        genuine.append((cid, max_len, long_n))
print('genuine long-card courses:', len(genuine))
for cid, mx, n in sorted(genuine, key=lambda x: -x[1]):
    print(f'{mx:5d} long={n:2d}  {cid}')
