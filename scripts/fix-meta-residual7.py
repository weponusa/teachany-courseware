#!/usr/bin/env python3
"""定向修复 7 个残余 #07/#13 课件：补 manifest.node_id 与 teachany-node 等 meta。"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMUNITY = os.path.join(ROOT, 'community')

TARGETS = {
    'sci-e-motion-speed':               {'node_id': 'sci-e-motion-speed', 'subject': 'science', 'grade': '4'},
    'bio-m-biosphere':                  {'node_id': 'bio-m-biosphere', 'subject': 'biology', 'grade': '7'},
    'bio-m-cell-division-junior':       {'node_id': 'bio-m-cell-division-junior', 'subject': 'biology', 'grade': '7'},
    'ext-1a79c832':                     {'node_id': 'ext-1a79c832', 'subject': 'cross', 'grade': ''},
    'chemistry-ext-1a79c832-6a108218':  {'node_id': 'chemistry-ext-1a79c832-6a108218', 'subject': 'chemistry', 'grade': ''},
    'ext-16a14ef':                      {'node_id': 'ext-16a14ef', 'subject': 'cross', 'grade': ''},
    'reading-academy':                  {'node_id': 'reading-academy', 'subject': 'chinese', 'grade': 'elementary'},
}

META_RE = re.compile(r'<meta\s+name=["\'](teachany-[a-z-]+)["\'][^>]*>', re.I)

for cid, info in TARGETS.items():
    cdir = os.path.join(COMMUNITY, cid)
    mpath = os.path.join(cdir, 'manifest.json')
    hpath = os.path.join(cdir, 'index.html')
    # manifest
    manifest = {}
    if os.path.exists(mpath):
        manifest = json.load(open(mpath, encoding='utf-8'))
    changed_m = False
    for k, v in (('node_id', info['node_id']), ('subject', info['subject'])):
        if not manifest.get(k):
            manifest[k] = info[k]; changed_m = True
    if not manifest.get('grade') and info['grade']:
        manifest['grade'] = info['grade']; changed_m = True
    if not manifest.get('id'):
        manifest['id'] = cid; changed_m = True
    if changed_m:
        json.dump(manifest, open(mpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    # html
    html = open(hpath, encoding='utf-8').read()
    have = set(m.group(1).lower() for m in META_RE.finditer(html))
    want = {
        'teachany-node': info['node_id'],
        'teachany-subject': info['subject'],
        'teachany-grade': info['grade'],
        'teachany-version': 'v7.14.1',
    }
    to_add = [(k, v) for k, v in want.items() if k not in have and v]
    if to_add:
        block = ''.join(f'  <meta name="{k}" content="{v}">\n' for k, v in to_add)
        matches = list(META_RE.finditer(html))
        if matches:
            pos = matches[-1].end()
            html = html[:pos] + '\n' + block.rstrip('\n') + html[pos:]
        else:
            html = html.replace('</head>', block + '</head>', 1)
        open(hpath, 'w', encoding='utf-8').write(html)
    print(cid, 'manifest+meta updated', to_add)
