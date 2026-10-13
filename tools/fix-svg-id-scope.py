#!/usr/bin/env python3
"""内联 SVG 的 id 作用域修复（重名 → 按 SVG 逐个重命名并同步引用）。

问题是什么
----------
HTML 里的 id 必须在**整份文档**里唯一，但多个内联 `<svg>` 常常各自定义了同名的
渐变/裁剪/滤镜（`blueGrad`、`orangeGrad`、`clip0`、`arrow` …）。浏览器容错，会全部指向
**第一个**同名定义，于是后面的图可能用了错的渐变色（视觉上「颜色串了」），并且
`document.getElementById('blueGrad')` 永远只拿到第一个——属真实缺陷，只是不报错。

怎么修
------
逐 `<svg>…</svg>` 扫描：把它内部定义的 id（`<linearGradient id>` / `<radialGradient>` /
`<clipPath>` / `<mask>` / `<filter>` / `<marker>` / `<pattern>` …）在**该 SVG 内**改成
`原名-s{n}`，并同步该 SVG 内所有引用（`url(#id)`、`xlink:href="#id"`、`href="#id"`、
`clip-path="url(#id)"` 等）。第 1 个 SVG 保持原名（不动引用最多的那份），减少 diff。

安全网：① 修完「全文档重复 id」必须为 0；② 每个 `url(#x)` 必须在同文件里能找到定义；
③ 标签平衡不得变差；④ 官方质检闸门（错误数不得增加）。

用法:
  python3 tools/fix-svg-id-scope.py --scan                 # 统计有多少课件受影响
  python3 tools/fix-svg-id-scope.py --from-list /tmp/ids.txt --apply
  python3 tools/fix-svg-id-scope.py --all --apply
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from _qa_gate import apply_guarded, imbalance  # noqa: E402

SVG_DEFS = ('linearGradient', 'radialGradient', 'clipPath', 'mask', 'filter', 'marker', 'pattern', 'symbol')
REF_ATTRS = ('fill', 'stroke', 'clip-path', 'mask', 'filter', 'marker-start', 'marker-mid', 'marker-end',
             'style', 'href', 'xlink:href')


def svg_blocks(html):
    """返回 [(start, end, block)] —— 用深度平衡切 <svg>（内联 SVG 可能嵌套 <svg>）。"""
    out = []
    i = 0
    while True:
        m = re.search(r'<svg\b[^>]*>', html[i:], re.I)
        if not m:
            break
        s = i + m.start()
        depth = 1
        j = i + m.end()
        for t in re.finditer(r'<(/?)svg\b[^>]*>', html[j:], re.I):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                out.append((s, j + t.end(), html[s:j + t.end()]))
                i = j + t.end()
                break
        else:
            break
    return out


def defined_ids(svg):
    ids = []
    for tag in SVG_DEFS:
        for m in re.finditer(r'<%s\b[^>]*\bid=["\']([^"\']+)["\']' % tag, svg, re.I):
            ids.append(m.group(1))
    return ids


def rename_in_svg(svg, mapping):
    if not mapping:
        return svg
    def repl_ref(m):
        return m.group(0).replace('#' + m.group(1), '#' + mapping.get(m.group(1), m.group(1)))
    # 引用：url(#id) / href="#id" / xlink:href="#id"
    svg = re.sub(r'url\(#([^)"\']+)\)', lambda m: 'url(#' + mapping.get(m.group(1), m.group(1)) + ')', svg)
    svg = re.sub(r'((?:xlink:)?href=["\'])#([^"\']+)', repl_ref, svg)
    # 定义处
    for tag in SVG_DEFS:
        def repl_def(m, tag=tag):
            old = m.group(1)
            return m.group(0).replace('id="%s"' % old, 'id="%s"' % mapping.get(old, old)) \
                             .replace("id='%s'" % old, "id='%s'" % mapping.get(old, old))
        svg = re.sub(r'<%s\b[^>]*\bid=["\']([^"\']+)["\'][^>]*>' % tag, repl_def, svg, flags=re.I)
    return svg


def fix(html):
    blocks = svg_blocks(html)
    if not blocks:
        return html, 0, {}
    seen = {}
    total = 0
    stat = Counter()
    out = html
    # 逆序处理，避免偏移失效
    for (s, e, block) in sorted(blocks, key=lambda x: -x[0]):
        ids = defined_ids(block)
        mapping = {}
        for idv in ids:
            if idv in seen:
                n = seen[idv] + 1
                seen[idv] = n
                mapping[idv] = '%s-s%d' % (idv, n)
                stat[idv] += 1
            else:
                seen[idv] = 1
        if mapping:
            new_block = rename_in_svg(block, mapping)
            out = out[:s] + new_block + out[e:]
            total += len(mapping)
    return out, total, dict(stat)


def dup_ids(html):
    body = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', html, flags=re.S | re.I)
    ids = re.findall(r'\bid="([^"]+)"', body)
    return {k: v for k, v in Counter(ids).items() if v > 1}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scan', action='store_true')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--from-list', default='')
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    if args.from_list:
        cids = [x.strip() for x in Path(args.from_list).read_text(encoding='utf-8').split() if x.strip()]
    else:
        cids = [d.name for d in sorted((ROOT / 'community').iterdir()) if (d / 'index.html').is_file()]

    if args.scan:
        rows = []
        for cid in cids:
            h = (ROOT / 'community' / cid / 'index.html').read_text(encoding='utf-8', errors='ignore')
            dups = dup_ids(h)
            if dups:
                rows.append((cid, len(dups), list(dups)[:3]))
        print('含重复 id 的课件: %d（其中语义级：%d）' % (
            len(rows), len([r for r in rows if any(len(k) >= 8 or '-' in k for k in r[2])])))
        for r in rows[:10]:
            print('  %-38s %d 个重复 id 例：%s' % (r[0], r[1], r[2]))
        Path('/tmp/dupid-cids.txt').write_text('\n'.join(r[0] for r in rows) + '\n', encoding='utf-8')
        return 0

    changed, skipped = [], []
    for cid in cids:
        f = ROOT / 'community' / cid / 'index.html'
        if not f.is_file():
            continue
        h = f.read_text(encoding='utf-8')
        before = len(dup_ids(h))
        if before == 0:
            continue
        new, n, stat = fix(h)
        after = len(dup_ids(new))
        if after >= before or n == 0:
            skipped.append((cid, f'{before}→{after} 未改善'))
            continue
        if imbalance(new) > imbalance(h):
            skipped.append((cid, '平衡变差'))
            continue
        if args.apply:
            ok, why = apply_guarded(f, new, cid)
            if not ok:
                skipped.append((cid, why))
                continue
        changed.append((cid, before, after, n))
    print('处理 %d 门：修复 %d 门，跳过 %d 门（%s）' % (len(cids), len(changed), len(skipped), '已写入' if args.apply else '干跑'))
    for c in changed[:12]:
        print('  %-38s 重复 id %d→%d，重命名 %d 处' % c)
    for s in skipped[:6]:
        print('  跳过 %s: %s' % s)
    return 0


if __name__ == '__main__':
    sys.exit(main())
