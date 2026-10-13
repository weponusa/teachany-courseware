#!/usr/bin/env python3
"""列出长尾失败项（除 #19/#20/#01/#21/#14/#11/#07 外）的课件与失败明细。"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
recs = json.load(open(os.path.join(ROOT, 'qc-all-report.json'), encoding='utf-8'))
DONE = ('#19', '#20', '#01', '#21', '#14', '#11', '#07')
for r in recs:
    rest = [x for x in r['failed'] if not any(x.startswith(d) for d in DONE)]
    if rest:
        print(f"{r['id']}: {'; '.join(rest)}")
