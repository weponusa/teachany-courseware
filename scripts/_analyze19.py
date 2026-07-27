#!/usr/bin/env python3
"""复刻 validator #19：列出每个失败课件的本地死链。"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
recs = json.load(open(os.path.join(ROOT, 'qc-all-report.json'), encoding='utf-8'))
f19 = [r['id'] for r in recs if any(x.startswith('#19') for x in r['failed'])]

REF_RE = re.compile(r'''(?:\b(?:src|href|poster)\s*=\s*['"]([^'"]+)['"]|url\(\s*['"]?([^'")]+)['"]?\s*\))''', re.I)
SKIP_RE = re.compile(r'^(https?:|data:|blob:|mailto:|tel:|javascript:|about:|chrome:|edge:)', re.I)

def skip(ref):
    t = ref.strip()
    return not t or t.startswith('#') or t.startswith('{{') or SKIP_RE.match(t)

report = {}
for cid in f19:
    cdir = os.path.join(ROOT, 'community', cid)
    html = open(os.path.join(cdir, 'index.html'), encoding='utf-8').read()
    missing = []
    seen = set()
    for m in REF_RE.finditer(html):
        raw = (m.group(1) or m.group(2) or '').strip()
        if skip(raw):
            continue
        clean = raw.split('#')[0].split('?')[0]
        try:
            clean = __import__('urllib.parse', fromlist=['unquote']).unquote(clean)
        except Exception:
            pass
        if not clean:
            continue
        target = os.path.join(ROOT, clean.lstrip('/')) if clean.startswith('/') else os.path.join(cdir, clean)
        key = (raw, target)
        if key in seen:
            continue
        seen.add(key)
        if not os.path.exists(target):
            missing.append(raw)
    report[cid] = missing

import collections
kind = collections.Counter()
for cid, ms in report.items():
    for m in ms:
        ext = os.path.splitext(m)[1].lower() or '(none)'
        kind[ext] += 1
print(kind.most_common())
json.dump(report, open(os.path.join(ROOT, 'qc-19-detail.json'), 'w'), ensure_ascii=False, indent=1)
for cid in list(report)[:12]:
    print(cid, '->', report[cid][:4])
