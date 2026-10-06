#!/usr/bin/env python3
"""补 3 个 ext 课件缺失的 teachany-grade meta。"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for cid in ['ext-1a79c832', 'chemistry-ext-1a79c832-6a108218', 'ext-16a14ef']:
    p = os.path.join(ROOT, 'community', cid, 'index.html')
    h = open(p, encoding='utf-8').read()
    if 'name="teachany-grade"' not in h:
        h = h.replace('<meta name="teachany-subject"',
                      '<meta name="teachany-grade" content="跨学段">\n  <meta name="teachany-subject"', 1)
        open(p, 'w', encoding='utf-8').write(h)
        print(cid, 'grade added')
    else:
        print(cid, 'has grade')
