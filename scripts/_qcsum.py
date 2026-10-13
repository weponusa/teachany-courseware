#!/usr/bin/env python3
"""汇总 8 个 shard 的质检结果，输出统计与残余失败清单。"""
import json, glob, collections, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
recs = []
for f in glob.glob(os.path.join(ROOT, 'qc-shard-*.json')):
    recs += json.load(open(f))
json.dump(recs, open(os.path.join(ROOT, 'qc-all-report.json'), 'w'), ensure_ascii=False, indent=1)
fail = [r for r in recs if r['failed']]
print('total:', len(recs), ' with failures:', len(fail),
      ' full pass:', sum(1 for r in recs if r['passed'] == r['total']))
cnt = collections.Counter()
for r in fail:
    for x in r['failed']:
        cnt[x] += 1
for k, v in cnt.most_common(30):
    print(f'{v:5d}  {k}')
print('--- residual failing courses ---')
for r in fail:
    print(r['id'], '|', '; '.join(r['failed']))
