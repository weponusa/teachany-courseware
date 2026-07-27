#!/usr/bin/env python3
"""复刻 validator #09：列出失败课件的超长卡片数与最长字数。"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
recs = json.load(open(os.path.join(ROOT, 'qc-all-report.json'), encoding='utf-8'))
f09 = [r['id'] for r in recs if any(x.startswith('#09') for x in r['failed'])]
CARD_RE = re.compile(r'<div[^>]*class="[^"]*card[^"]*"[^>]*>([\s\S]*?)</div>', re.I)
out = []
for cid in f09:
    html = open(os.path.join(ROOT, 'community', cid, 'index.html'), encoding='utf-8').read()
    long_n, max_len, cards = 0, 0, 0
    for m in CARD_RE.finditer(html):
        cards += 1
        text = re.sub(r'<[^>]+>', '', m.group(1))
        text = re.sub(r'\s+', '', text)
        max_len = max(max_len, len(text))
        if len(text) > 200:
            long_n += 1
    out.append((cid, cards, max_len, long_n))
for cid, cards, max_len, long_n in sorted(out, key=lambda x: -x[2])[:25]:
    print(f'{max_len:5d}  long={long_n:2d} cards={cards:3d}  {cid}')
print('total f09:', len(out))
json.dump(out, open(os.path.join(ROOT, 'qc-09-detail.json'), 'w'), ensure_ascii=False)
