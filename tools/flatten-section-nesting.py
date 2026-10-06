#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""拆掉 section 嵌套：把「内部还套着 <section> 的外层 section」改成 <div>。

为什么
------
HTML 里 `<section>` 是可以嵌套的，但 TeachAny 课件里嵌套的成因几乎都是**包裹层**：
  · v2 分页课件的页容器 `<section class="slide-page" data-page-type="..." data-page-index="N">`
    里面装 1~N 个内容 section；
  · 少数课件被注入了一个无 class 的大 wrapper（`<section data-conceptest ...>`）把整页内容
    全包住。
这两种外层都不承载语义，却让所有「按 section 切块」的解析（官方两个校验器的 `extract_sections`、
  以及各课件的 `querySelectorAll('section[id]')` 滚动高亮）全部跑偏。

做法
----
凡「内部还套着别的 `<section>`」的 section，把它的开/闭标签换成 `<div>`，**属性与 class 原样保留**
（`slide-page` / `data-page-type` / `data-page-index` 都在 class/属性上，样式与脚本照旧命中）。
叶子 section（真正的内容块）保持 `<section>` 不变，所以：
  · `.slide-page` 的样式与分页脚本不受影响；
  · `querySelectorAll('section[id]')` 之后只会命中内容块，滚动高亮更准。

跳过条件（会在输出里列出）
--------------------------
· 课件用 `querySelectorAll('section')` 做「隐藏其余、只显示一个」的翻页导航；
· 课件 CSS/JS 里有**标签限定**选择器（`section.section` / `section:not(.hero)` / `section[data-tts=`）；
  改标签会直接失效，宁可不动。

护栏：每门过 tools/_qa_gate.apply_guarded（错误数上升或标签失衡即回滚）。

用法:  python3 tools/flatten-section-nesting.py [--apply] [--from-list f] [--limit N]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from _qa_gate import apply_guarded, imbalance  # noqa: E402

TAG_QUALIFIED = re.compile(
    r"""(?<![\w.\-#])querySelector(?:All)?\(\s*['"]section['"]   # 按标签取全部 section
      | (?<![\w.\-#])getElementsByTagName\(\s*['"]section
      | ['"]section\.[A-Za-z_-][^'"]*['"]                            # 引号里的 section.xxx（标签+类）""",
    re.VERBOSE)
# 纯粹用来打「当前段」标记的 querySelectorAll('section') 不构成障碍：
# 拆平后它只会命中内容 section（包裹层变 div），正是想要的行为。
MARKER_ONLY = re.compile(
    r"""querySelectorAll\(\s*['"]section['"]\s*\)[\s\S]{0,160}?current-section""", re.VERBOSE)


def only_marker_usage(h: str) -> bool:
    n = len(re.findall(r"""querySelectorAll\(\s*['"]section['"]\s*\)""", h, re.VERBOSE))
    if n == 0:
        return True
    return len(MARKER_ONLY.findall(h)) >= n


LAYOUT_RULE = re.compile(r'(?m)(^|[},])\s*section(?![\w-])')


def sections(h: str):
    """所有 <section>（含嵌套）的 (start, end, tag, tag_end)。"""
    out = []
    for m in re.finditer(r'<section\b[^>]*>', h):
        depth, j = 1, m.end()
        for t in re.finditer(r'<(/?)section\b[^>]*>', h[j:]):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                j = j + t.end()
                break
        else:
            continue
        out.append((m.start(), j, m.group(0), m.end()))
    return out


def normalize_tutor_selector(h: str) -> str:
    """AI 学伴上下文取「当前段」用的是 `section.current-section`（标签限定）。
    改成 `.current-section`：拆平嵌套后仍然命中，且不依赖标签。"""
    return h.replace('section.current-section', '.current-section')


FLAT_CLASS = 'ta-flat'


def add_flat_class(tag: str) -> str:
    """给被改成 <div> 的包裹层加一个 ta-flat 标记 class。"""
    m = re.search(r"""\sclass\s*=\s*(['"])(.*?)\1""", tag)
    if m:
        if FLAT_CLASS in m.group(2).split():
            return tag
        return tag[: m.start(2)] + (m.group(2) + ' ' + FLAT_CLASS) + tag[m.end(2):]
    return tag[: len('<div')] + ' class="%s"' % FLAT_CLASS + tag[len('<div'):]


def css_add_flat(css: str) -> str:
    """把以 `section` 元素开头的选择器补一个 `.ta-flat` 孪生：
        section{…}            → section, .ta-flat{…}
        section.hero{…}       → section.hero, .ta-flat.hero{…}
        section .intro{…}     → section .intro, .ta-flat .intro{…}
        section:last-of-type{…} → section:last-of-type, .ta-flat:last-of-type{…}
    否则包裹层由 <section> 改成 <div> 后会丢掉这些样式（实测内容变宽、内边距消失）。"""
    out, i = [], 0
    while True:
        b = css.find('{', i)
        if b == -1:
            out.append(css[i:])
            break
        s = max(css.rfind('}', 0, b), css.rfind('{', 0, b)) + 1
        sel = css[s:b]
        out.append(css[i:s])
        clean = re.sub(r'/\*.*?\*/', ' ', sel, flags=re.S)
        if FLAT_CLASS not in clean and not clean.strip().startswith('@'):
            parts = [x.strip() for x in clean.split(',')]
            twins = ['.' + FLAT_CLASS + x[len('section'):] for x in parts
                     if re.match(r'section(?![\w-])', x)]
            if twins:
                sel = sel.rstrip() + ', ' + ', '.join(twins) + ' '
        out.append(sel)
        out.append('{')
        i = b + 1
    return ''.join(out)


def rewrite_css(h: str) -> str:
    res, pos = [], 0
    for sm in re.finditer(r'(<style\b[^>]*>)(.*?)(</style>)', h, re.S):
        res.append(h[pos:sm.start()])
        res.append(sm.group(1) + css_add_flat(sm.group(2)) + sm.group(3))
        pos = sm.end()
    res.append(h[pos:])
    return ''.join(res)


def plan(cid: str):
    f = ROOT / 'community' / cid / 'index.html'
    if not f.is_file():
        return None, 'no-file'
    h = f.read_text(encoding='utf-8')
    base = normalize_tutor_selector(h)
    normalized = base != h
    h = base
    secs = sections(h)
    if len(secs) < 2:
        return (h, 'tutor-selector') if normalized else (None, 'ok')
    # 找出所有「内部还有别的 section」的 section
    idx = [(a, b, tag, te) for a, b, tag, te in secs]
    nested_outer = []
    for i, (a, b, tag, te) in enumerate(idx):
        for j, (c, d, _t2, _e2) in enumerate(idx):
            if i != j and a < c and d <= b:
                nested_outer.append(i)
                break
    if not nested_outer:
        out = h
        note = []
        if normalized:
            note.append('tutor-selector')
        if FLAT_CLASS in h and LAYOUT_RULE.search(h):
            out2 = rewrite_css(out)
            if out2 != out:
                out = out2
                note.append('css-twins')
        return (out, '+'.join(note)) if out != h else (None, 'ok')

    for pat, why in ((TAG_QUALIFIED, 'tag-qualified-selector'),):
        if pat.search(h) and not only_marker_usage(h):
            return (h, 'tutor-selector+skip:' + why) if normalized else (None, why)

    edits = []
    for i in sorted(set(nested_outer), reverse=True):
        a, b, tag, te = idx[i]
        new_tag = add_flat_class('<div' + tag[len('<section'):])
        edits.append((a, te, tag, new_tag))
        # 结尾标签（b 往前找最后一个 </section>）
        cs = h.rfind('</section>', a, b)
        if cs == -1:
            return None, 'close-not-found'
        edits.append((cs, cs + len('</section>'), '</section>', '</div>'))
    new = h
    for s, e, old, rep in sorted(edits, reverse=True):
        assert new[s:e] == old, (cid, old, new[s:e][:24])
        new = new[:s] + rep + new[e:]

    note = 'flatten:%d' % (len(set(nested_outer)))
    if LAYOUT_RULE.search(h):
        new = rewrite_css(new)
        note += '+css'
    if normalized:
        note = 'tutor-selector+' + note
    return new, note


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--from-list', default='')
    ap.add_argument('--limit', type=int, default=0)
    args = ap.parse_args()

    cids = ([x.strip() for x in Path(args.from_list).read_text(encoding='utf-8').split() if x.strip()]
            if args.from_list else sorted(d.name for d in (ROOT / 'community').iterdir()))
    if args.limit:
        cids = cids[: args.limit]

    changed, skipped = [], []
    for cid in cids:
        new, why = plan(cid)
        if not new:
            if why != 'ok':
                skipped.append((cid, why))
            continue
        f = ROOT / 'community' / cid / 'index.html'
        h = f.read_text(encoding='utf-8')
        if imbalance(new) > imbalance(h):
            skipped.append((cid, '平衡变差'))
            continue
        if not args.apply:
            changed.append((cid, why))
            continue
        ok, why2 = apply_guarded(f, new, cid)
        (changed if ok else skipped).append((cid, why if ok else why2))
    print('%s可改 %d 门' % ('' if args.apply else '干跑：', len(changed)))
    for c in changed[:15]:
        print('   ', c)
    if len(changed) > 15:
        print('    …其余 %d 门' % (len(changed) - 15))
    print('跳过 %d 门' % len(skipped))
    for s in skipped[:20]:
        print('    ↷', s)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
