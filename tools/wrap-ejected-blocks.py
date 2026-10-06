#!/usr/bin/env python3
"""把「被弹出页面的内容块」重新包成独立 slide-page。

病灶
----
历史迁移把一些真实教学块（`<section class="section teachany-upgrade-block">`、
`<section class="section" id="hero-infographic">`、孤立的 `<div class="card">` 等）
留在了 `#slide-container` 里**页面与页面之间**——既不入页、也不成页：
  · 分页浏览时它们跟着页走，版面和顺序都乱；
  · 静态工具（去重/拆页）遇到它们只能跳过。

做法
----
容器内、非 slide-page 的顶层块 → 包一层：
  `<section class="slide-page" data-page-type="…" data-tsh="…"><div class="slide-inner">原始块</div></section>`
页型按内容判定（hero-infographic → interactive；upgrade-block/module → concept；其余 concept）。
保持原位置不动，重排 data-page-index，再过质检闸门与标签平衡检查。

用法:
  python3 tools/wrap-ejected-blocks.py --list-file /tmp/ejc.txt            # 干跑
  python3 tools/wrap-ejected-blocks.py --list-file /tmp/ejc.txt --apply
  python3 tools/wrap-ejected-blocks.py --all-migrated --apply
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from _qa_gate import apply_guarded, imbalance  # noqa: E402

WRAPPABLE = ('section', 'div', 'figure', 'article', 'header', 'table', 'ul', 'ol')
SKIP_TAGS = ('script', 'style', 'link', 'meta', 'template', 'nav')


def balanced(s, start, tag):
    m0 = re.match(r'<%s\b[^>]*>' % tag, s[start:], re.I)
    if not m0:
        return None
    i = start + m0.end()
    d = 1
    for mm in re.finditer(r'<(/?)%s\b[^>]*(/?)>' % tag, s[i:], re.I):
        if mm.group(1):
            d -= 1
        elif not mm.group(2):
            d += 1
        if d == 0:
            return s[start:i + mm.end()]
    return None


def container_region(html):
    c = re.search(r'<div[^>]*class="[^"]*slide-container[^"]*"[^>]*>', html)
    if not c:
        return None
    o = c.end()
    d = 1
    for mm in re.finditer(r'<(/?)div\b[^>]*(/?)>', html[o:], re.I):
        if mm.group(1):
            d -= 1
        elif not mm.group(2):
            d += 1
        if d == 0:
            return o, o + mm.start()
    return o, len(html)


def top_level_blocks(html, o, c):
    """容器内顶层块（跳过 slide-page 与 script/style 等）。"""
    out = []
    i = o
    tag_re = re.compile(r'<(/?)(%s)\b[^>]*(/?)>' % '|'.join(WRAPPABLE + SKIP_TAGS), re.I)
    while i < c:
        m = tag_re.search(html, i)
        if not m or m.start() >= c:
            break
        tag = m.group(2).lower()
        if m.group(1) or m.group(3):     # 闭合/自闭合标签，跳过
            i = m.end()
            continue
        blk = balanced(html, m.start(), tag)
        if not blk:
            i = m.end()
            continue
        end = m.start() + len(blk)
        if end > c:
            break
        inner = html[m.start():end]
        is_page = 'slide-page' in (re.match(r'<%s\b[^>]*>' % tag, inner, re.I).group(0) or '')
        if not is_page and tag not in SKIP_TAGS:
            out.append((m.start(), end, tag, inner))
        i = max(end, m.end())
    return out


def guess_type(block):
    if 'hero-infographic' in block[:200]:
        return 'interactive', '知识结构主图'
    if 'upgrade-block' in block[:200]:
        return 'concept', '知识精讲'
    if re.search(r'真题|练习|习题', block[:400]):
        return 'quiz', '练习'
    return 'concept', '知识模块'


def fix_course(f):
    html = f.read_text(encoding='utf-8')
    reg = container_region(html)
    if not reg:
        return {'cid': f.parent.name, 'skip': 'no-container'}
    o, c = reg
    blocks = top_level_blocks(html, o, c)
    if not blocks:
        return {'cid': f.parent.name, 'skip': 'no-ejected'}
    new = html
    wrapped = 0
    for (s0, e0, tag, blk) in sorted(blocks, key=lambda x: -x[0]):
        ptype, tsh = guess_type(blk)
        page = ('<section class="slide-page" data-page-type="%s" data-page-index="0" data-tsh="%s">'
                '<div class="slide-inner">\n%s\n</div></section>\n' % (ptype, tsh, blk))
        new = new[:s0] + page + new[e0:]
        wrapped += 1
    n = [0]
    new = re.sub(r'data-page-index="\d+"',
                 lambda m: 'data-page-index="%d"' % (n.__setitem__(0, n[0] + 1) or n[0] - 1), new)
    if imbalance(new) > imbalance(html):
        return {'cid': f.parent.name, 'skip': '平衡变差 %d->%d' % (imbalance(html), imbalance(new))}
    if len(re.findall(r'class="[^"]*slide-page', new)) != len(re.findall(r'class="[^"]*slide-page', html)) + wrapped:
        return {'cid': f.parent.name, 'skip': '页数不符预期'}
    return {'cid': f.parent.name, 'wrapped': wrapped, 'new': new}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--list-file', default='')
    ap.add_argument('--all-migrated', action='store_true')
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    if args.list_file:
        cids = [x.strip() for x in Path(args.list_file).read_text(encoding='utf-8').split() if x.strip()]
    else:
        cids = [d.name for d in sorted((ROOT / 'community').iterdir()) if (d / 'index.html').is_file()]
    changed, skipped = [], []
    for cid in cids:
        f = ROOT / 'community' / cid / 'index.html'
        if not f.is_file():
            continue
        r = fix_course(f)
        if r.get('new'):
            if args.apply:
                ok, why = apply_guarded(f, r['new'], cid)
                r['gate'] = why
                if not ok:
                    skipped.append(r); continue
            changed.append(r)
        else:
            skipped.append(r)
    print(f'处理 {len(cids)} 门：包成页 {len(changed)} 门，跳过 {len(skipped)} 门（{"已写入" if args.apply else "干跑"}）')
    tot = sum(r['wrapped'] for r in changed)
    print('共包出 %d 个页面' % tot)
    for r in changed[:12]:
        print('  %-42s +%d 页' % (r['cid'], r['wrapped']))
    for r in skipped[:6]:
        print('  跳过 %s: %s' % (r['cid'], r.get('skip')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
