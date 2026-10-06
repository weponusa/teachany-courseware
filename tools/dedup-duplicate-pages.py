#!/usr/bin/env python3
"""删除「同类型 + 同标题」的重复页（保留内容更全的那一份）。

适用：老式课件里同一页出现两份（例如 legacy `content|知识图谱` 与 v2 `graph|知识图谱`）。
安全网：受保护页型（知识图谱/学伴等）删后必须仍存在；标签平衡不得变差；官方质检闸门。

用法:
  python3 tools/dedup-duplicate-pages.py --from-list /tmp/dup-pages.txt --list
  python3 tools/dedup-duplicate-pages.py --from-list /tmp/dup-pages.txt --apply
"""
import argparse, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from _qa_gate import apply_guarded, imbalance  # noqa: E402

def strip_js(h): return re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', h, flags=re.S | re.I)

def pages_of(h):
    out, j = [], 0
    while True:
        m = re.search(r'<section[^>]*class="[^"]*slide-page[^"]*"[^>]*>', h[j:])
        if not m: break
        s = j + m.start()
        m0 = re.match(r'<section\b[^>]*>', h[s:], re.I)
        k = s + m0.end(); d = 1; e = None
        for mm in re.finditer(r'<(/?)section\b[^>]*(/?)>', h[k:], re.I):
            if mm.group(1): d -= 1
            elif not mm.group(2): d += 1
            if d == 0: e = k + mm.end(); break
        if e is None: break
        blk = h[s:e]
        t = (re.search(r'data-page-type="([^"]*)"', blk[:220]) or [None,''])[1]
        tsh = (re.search(r'data-tsh="([^"]*)"', blk[:220]) or [None,''])[1]
        out.append({'s': s, 'e': e, 'type': t, 'tsh': tsh, 'blk': blk})
        j = e
    return out

def score(p):
    b = strip_js(p['blk'])
    txt = re.sub(r'<[^>]+>', '', b)
    s = len(re.findall(r'[一-鿿]', txt))
    if 'data-teachany-kg' in b: s += 500          # 带图谱容器优先
    if 'data-teachany-tutor-card' in b: s += 500
    if re.search(r'<canvas|<svg', b): s += 50     # 有可视化优先
    return s

def fix(f):
    h = f.read_text(encoding='utf-8')
    ps = pages_of(h)
    groups = {}
    for i, p in enumerate(ps):
        if not p['tsh'] or p['type'] in ('', 'cover'):
            continue
        groups.setdefault((p['type'], p['tsh']), []).append(i)
    dup = {k: v for k, v in groups.items() if len(v) > 1}
    if not dup:
        return {'cid': f.parent.name, 'skip': 'no-dup-page'}
    dels = []
    for k, idxs in dup.items():
        best = max(idxs, key=lambda i: score(ps[i]))
        for i in idxs:
            if i != best:
                dels.append(ps[i])
    if not dels:
        return {'cid': f.parent.name, 'skip': 'nothing-to-delete'}
    new = h
    for p in sorted(dels, key=lambda x: -x['s']):
        new = new[:p['s']] + new[p['e']:]
    # 受保护模块必须仍存在
    b0, b1 = strip_js(h), strip_js(new)
    for attr in ('data-teachany-kg', 'data-teachany-tutor-card'):
        if b0.count(attr) > 0 and b1.count(attr) == 0:
            return {'cid': f.parent.name, 'skip': '%s 被删光' % attr}
    if imbalance(new) > imbalance(h):
        return {'cid': f.parent.name, 'skip': '平衡变差'}
    n = [0]
    new = re.sub(r'data-page-index="\d+"', lambda m: 'data-page-index="%d"' % (n.__setitem__(0, n[0]+1) or n[0]-1), new)
    return {'cid': f.parent.name, 'deleted': len(dels), 'groups': len(dup), 'new': new}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--from-list', required=True)
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    cids = [x.strip() for x in Path(args.from_list).read_text(encoding='utf-8').split() if x.strip()]
    ch, sk = [], []
    for cid in cids:
        f = ROOT / 'community' / cid / 'index.html'
        if not f.is_file(): continue
        r = fix(f)
        if r.get('new'):
            if args.apply:
                ok, why = apply_guarded(f, r['new'], cid)
                r['gate'] = why
                if not ok: sk.append(r); continue
            ch.append(r)
        else: sk.append(r)
    print('处理 %d 门：删除重复页 %d 门，跳过 %d 门（%s）' % (len(cids), len(ch), len(sk), '已写入' if args.apply else '干跑'))
    for r in ch[:12]: print('  %-32s 删 %d 页 / %d 组' % (r['cid'], r['deleted'], r['groups']))
    for r in sk[:8]: print('  跳过 %s: %s' % (r['cid'], r.get('skip')))
    return 0

if __name__ == '__main__': sys.exit(main())
