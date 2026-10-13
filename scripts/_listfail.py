#!/usr/bin/env python3
"""输出指定检查项失败的课件清单（含详情需跑 validator，这里先列 id）。"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
recs = json.load(open(os.path.join(ROOT, 'qc-all-report.json'), encoding='utf-8'))
prefix = sys.argv[1]
ids = [r['id'] for r in recs if any(x.startswith(prefix) for x in r['failed'])]
print(len(ids))
for i in ids:
    print(i)
