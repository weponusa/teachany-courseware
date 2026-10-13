#!/usr/bin/env python3
"""分析并修复 #21 残留：1) video 标签补 controls/playsinline/preload；
2) 引用不存在或 <20KB 的 mp4 → 报告（不删，先修标签）。"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
recs = json.load(open(os.path.join(ROOT, 'qc-all-report.json'), encoding='utf-8'))
f21 = [r['id'] for r in recs if any(x.startswith('#21') for x in r['failed'])]

def analyze(cid):
    cdir = os.path.join(ROOT, 'community', cid)
    html = open(os.path.join(cdir, 'index.html'), encoding='utf-8').read()
    refs = re.findall(r'<(?:video|source)[^>]+src=["\']([^"\']+\.mp4)["\']', html, re.I)
    bad_refs = []
    for r in refs:
        t = r.split('?')[0].split('#')[0]
        p = os.path.join(ROOT, t.lstrip('/')) if t.startswith('/') else os.path.join(cdir, t)
        if not (os.path.exists(p) and os.path.getsize(p) >= 20*1024):
            bad_refs.append(r)
    tags = re.findall(r'<video\b[^>]*>', html, re.I)
    no_ctrl = [t for t in tags if not (re.search(r'controls', t, re.I) and re.search(r'playsinline', t, re.I))]
    return refs, bad_refs, tags, no_ctrl

for cid in f21:
    refs, bad, tags, noctrl = analyze(cid)
    print(f'{cid}: refs={len(refs)} bad={len(bad)} videoTags={len(tags)} noCtrl={len(noctrl)}')
