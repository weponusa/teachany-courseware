#!/usr/bin/env python3
"""找回被误删的标准模块页（ai-tutor / knowledge-graph 等）。

背景
----
`tools/fix-course-dups-order.py` 早期版本的「删空页判定」（页内 <20 汉字即删）误伤
了天生文字少的**标准模块页**：AI 学伴页（0 字）、知识图谱页（~14 字）。
工具已修（PROTECTED 白名单），本脚本负责把已经被删的页从基线版本找回来。

做法
----
1. 用 `git show <baseline>:community/<cid>/index.html` 取基线版本，切出缺失页的整块；
2. 在当前文件中找「基线里紧跟其后的那一页」作为插入锚点（按 data-tsh / 页型匹配）；
   找不到就用「基线里排在它前面的页」之后；
3. 插入后重排 data-page-index，并用官方质检闸门校验（错误数不得增加）。

用法:
  python3 tools/restore-standard-pages.py --from-list /tmp/affected-keypages.txt --baseline ccaff801dd --list
  python3 tools/restore-standard-pages.py --from-list /tmp/affected-keypages.txt --baseline ccaff801dd --apply
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from _qa_gate import imbalance  # noqa: E402

TYPES = ('ai-tutor', 'knowledge-graph', 'homework', 'summary', 'objectives')


def page_items(html):
    """返回 [(start, end, type, tsh, block)]，按文档序。"""
    c = re.search(r'<div[^>]*class="[^"]*slide-container[^"]*"[^>]*>', html)
    if not c:
        return []
    out, j = [], c.end()
    while True:
        m = re.search(r'<section[^>]*class="[^"]*slide-page[^"]*"[^>]*>', html[j:])
        if not m:
            break
        s = j + m.start()
        m0 = re.match(r'<section\b[^>]*>', html[s:], re.I)
        k = s + m0.end()
        d = 1
        e = None
        for mm in re.finditer(r'<(/?)section\b[^>]*(/?)>', html[k:], re.I):
            if mm.group(1):
                d -= 1
            elif not mm.group(2):
                d += 1
            if d == 0:
                e = k + mm.end()
                break
        if e is None:
            break
        block = html[s:e]
        t = (re.search(r'data-page-type="([^"]*)"', block[:220]) or [None, ''])[1]
        tsh = (re.search(r'data-tsh="([^"]*)"', block[:220]) or [None, ''])[1]
        out.append({'start': s, 'end': e, 'type': t, 'tsh': tsh, 'block': block})
        j = e
    return out


def restore(cid, baseline, apply=False):
    f = ROOT / 'community' / cid / 'index.html'
    if not f.is_file():
        return {'cid': cid, 'skip': 'no file'}
    cur = f.read_text(encoding='utf-8')
    old = subprocess.run(['git', 'show', f'{baseline}:community/{cid}/index.html'],
                         cwd=str(ROOT), capture_output=True, text=True).stdout
    if not old:
        return {'cid': cid, 'skip': 'baseline missing'}
    op, cp = page_items(old), page_items(cur)
    have = {(p['type'], p['tsh']) for p in cp}
    missing = [p for p in op if p['type'] in TYPES and (p['type'], p['tsh']) not in have
               and not any(q['type'] == p['type'] and q['tsh'] == p['tsh'] for q in cp)]
    if not missing:
        return {'cid': cid, 'skip': 'no missing'}
    new = cur
    restored = []
    for mp in missing:
        # 锚点：基线里排在它后面的第一页（在当前文件中存在）
        idx = op.index(mp)
        anchor = None
        for nxt in op[idx + 1:]:
            for q in page_items(new):
                if q['type'] == nxt['type'] and q['tsh'] == nxt['tsh']:
                    anchor = q['start']
                    break
            if anchor:
                break
        if anchor is None:
            # 退而求其次：插在最后一个页面前
            items = page_items(new)
            anchor = items[-1]['start'] if items else None
        if anchor is None:
            return {'cid': cid, 'skip': 'no anchor'}
        new = new[:anchor] + mp['block'] + '\n' + new[anchor:]
        restored.append(mp['type'])
    # 重排 index
    n = [0]
    new = re.sub(r'data-page-index="\d+"',
                 lambda m: 'data-page-index="%d"' % (n.__setitem__(0, n[0] + 1) or n[0] - 1), new)
    if imbalance(new) > imbalance(cur):
        return {'cid': cid, 'skip': f'平衡变差 {imbalance(cur)}→{imbalance(new)}'}
    res = {'cid': cid, 'restored': restored, 'pages': len(page_items(new))}
    if apply:
        orig = f.read_text(encoding='utf-8')
        f.write_text(new, encoding='utf-8')
        # 质检闸门
        try:
            out = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'validate-courseware.py'), cid],
                                 cwd=str(ROOT), capture_output=True, text=True, timeout=120)
            txt = (out.stdout or '') + (out.stderr or '')
            before = int(re.search(r'❌ 错误:\s*(\d+)', txt).group(1)) if re.search(r'❌ 错误:\s*(\d+)', txt) else -1
            # 对比改动前的错误数
            f.write_text(orig, encoding='utf-8')
            out2 = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'validate-courseware.py'), cid],
                                  cwd=str(ROOT), capture_output=True, text=True, timeout=120)
            txt2 = (out2.stdout or '') + (out2.stderr or '')
            before2 = int(re.search(r'❌ 错误:\s*(\d+)', txt2).group(1)) if re.search(r'❌ 错误:\s*(\d+)', txt2) else -1
            if before > before2:
                res['skip'] = f'质检错误 {before2}→{before}，已回滚'
                return res
            f.write_text(new, encoding='utf-8')
            res['applied'] = True
        except Exception as e:  # noqa: BLE001
            f.write_text(orig, encoding='utf-8')
            res['skip'] = f'闸门异常: {str(e)[:60]}'
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--from-list', required=True)
    ap.add_argument('--baseline', default='ccaff801dd')
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    cids = [x.strip() for x in Path(args.from_list).read_text(encoding='utf-8').split() if x.strip()]
    ok, skips = [], []
    for cid in cids:
        r = restore(cid, args.baseline, args.apply)
        (ok if (r.get('restored') and (r.get('applied') or not args.apply)) else skips).append(r)
    print(f'处理 {len(cids)} 门：找回 {len(ok)} 门，跳过 {len(skips)} 门（{"已写入" if args.apply else "干跑"}）')
    import collections
    print('找回页型:', collections.Counter(t for r in ok for t in r.get('restored', [])))
    for r in skips[:8]:
        print(f"  跳过 {r['cid']}: {r.get('skip')}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
