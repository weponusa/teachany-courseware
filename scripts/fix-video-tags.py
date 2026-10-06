#!/usr/bin/env python3
"""给缺 controls/playsinline 的 <video> 标签补齐标准属性。"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
recs = json.load(open(os.path.join(ROOT, 'qc-all-report.json'), encoding='utf-8'))
f21 = [r['id'] for r in recs if any(x.startswith('#21') for x in r['failed'])]

VIDEO_TAG_RE = re.compile(r'<video\b[^>]*>', re.I)

def patch(tag):
    t = tag
    if not re.search(r'\bcontrols\b', t, re.I):
        t = t[:-1].rstrip('/') + ' controls>' if not t.endswith('/>') else t
    # 统一处理：先去掉末尾 >
    body = tag[:-1]
    if body.rstrip().endswith('/'):
        body = body.rstrip()[:-1].rstrip()
        closing = '>'
    else:
        closing = '>'
    add = ''
    if not re.search(r'\bcontrols\b', body, re.I):
        add += ' controls'
    if not re.search(r'\bplaysinline\b', body, re.I):
        add += ' playsinline'
    if not re.search(r'\bpreload\b', body, re.I):
        add += ' preload="metadata"'
    return body + add + closing

total = 0
for cid in f21:
    hpath = os.path.join(ROOT, 'community', cid, 'index.html')
    html_src = open(hpath, encoding='utf-8').read()
    n = 0
    def repl(m):
        global n
        tag = m.group(0)
        if re.search(r'\bcontrols\b', tag, re.I) and re.search(r'\bplaysinline\b', tag, re.I):
            return tag
        n += 1
        return patch(tag)
    html_new = VIDEO_TAG_RE.sub(repl, html_src)
    if n:
        open(hpath, 'w', encoding='utf-8').write(html_new)
    total += n
    print(cid, n)
print('total patched:', total)
