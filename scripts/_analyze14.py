#!/usr/bin/env python3
import json, re, collections, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
recs = json.load(open(os.path.join(ROOT, 'qc-all-report.json'), encoding='utf-8'))
f14 = [r['id'] for r in recs if any(x.startswith('#14') for x in r['failed'])]
anchor = collections.Counter()
for cid in f14:
    html = open(os.path.join(ROOT, 'community', cid, 'index.html'), encoding='utf-8').read()
    feats = []
    for pat, name in [(r'class="slide-container"', 'slide-container'), (r'class="main"', 'div.main'), (r'<main', 'main-tag'), (r'id="summary"', 'summary'), (r'id="posttest"', 'posttest'), (r'class="slide-page"', 'slide-page')]:
        if re.search(pat, html): feats.append(name)
    anchor[tuple(feats)] += 1
for k, v in anchor.most_common():
    print(v, k)
