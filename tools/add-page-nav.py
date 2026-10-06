#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给没有页内导航的课件补上「可跳转的章节入口」。

背景
----
质检 B-6：`<a href="#…">` 少于 3 个就警告「课件应可前后翻页」。全站 289 门命中，
但它们分两类，处理方式完全不同：

A) **分页 deck**（273 门，`.slide-page` ≥3）：本来就能翻页（滚动吸附 + 侧边导航点），
   只是导航点是 JS 生成的 `<button>`，没有 `href`，所以既不满足 B-6，**也不能分享定位到某一节**。
   做法：给每页补 `id="page-N"`，把导航点由 `<button>` 改成 `<a href="#page-N">`——
   原有 click 行为不变，额外获得原生锚点跳转 + 可分享链接。

B) **平铺页**（16 门）：真的没有翻页能力，注入「本页目录 + 上一节/下一节」，
   行为由共享的 assets/scripts/teachany-page-nav.js 承担（幂等、主题自适应、可键盘操作）。

护栏：逐门过 tools/_qa_gate（质检错误数不得上升）；改动前先 dry 打印计划。

用法:  python3 tools/add-page-nav.py --from-list /tmp/no_nav.txt [--apply]
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from _qa_gate import apply_guarded  # noqa: E402

PAGE_RE = re.compile(r'<section\b([^>]*\bclass="[^"]*\bslide-page\b[^"]*"[^>]*)>', re.I)
DOT_RE = re.compile(r"(const|let|var)\s+(\w+)\s*=\s*document\.createElement\((['\"])button\3\)")
SEC_OPEN = re.compile(r'<section\b([^>]*)>', re.I)
HEAD_RE = re.compile(r'</head>', re.I)
BODY_RE = re.compile(r'</body>', re.I)
H2_RE = re.compile(r'<h([12])\b[^>]*>(.*?)</h\1>', re.S | re.I)
ID_RE = re.compile(r'\bid="([^"]+)"')
SKIP_TITLE = re.compile(r'(语音导学|AI 学伴|学伴入口|知识图谱|返回顶部|版权|致谢)')


def plain_text(s: str) -> str:
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()


def add_page_ids(h: str):
    """给每个 .slide-page 补 id（已有就沿用），返回 (新 html, 目标 id 列表)。"""
    ids, edits = [], []
    for m in PAGE_RE.finditer(h):
        attrs = m.group(1)
        im = ID_RE.search(attrs)
        if im:
            ids.append(im.group(1))
            continue
        nid = f'page-{len(ids) + 1}'
        ids.append(nid)
        edits.append((m.end(1), f' id="{nid}"'))
    for pos, txt in sorted(edits, reverse=True):
        h = h[:pos] + txt + h[pos:]
    return h, ids


def upgrade_dots(h: str) -> tuple[str, bool]:
    """把生成 sidenav-dot 的 <button> 换成 <a href="#…">。"""
    m = DOT_RE.search(h)
    if not m:
        return h, False
    # 必须是导航点（下一行就是 sidenav-dot）
    tail = h[m.end(): m.end() + 400]
    if 'sidenav-dot' not in tail:
        return h, False
    var = m.group(2)
    h = h[:m.start()] + f"{m.group(1)} {var} = document.createElement('a')" + h[m.end():]
    # 在 className 之前插入 href / aria-label
    ins = re.search(rf"{re.escape(var)}\.className\s*=", h[m.end():])
    if not ins:
        return h, False
    at = m.end() + ins.start()
    code = (f"{var}.setAttribute('href', '#' + (page.id || ('page-' + (i + 1))));"
            f"{var}.setAttribute('role', 'button');")
    h = h[:at] + code + h[at:]
    return h, True


def flat_nav(h: str):
    """平铺页：收集有标题的顶层 section，注入目录 + 前后翻页。"""
    secs = []
    for m in SEC_OPEN.finditer(h):
        attrs = m.group(1)
        seg = h[m.end(): m.end() + 1200]
        hd = H2_RE.search(seg)
        if not hd:
            continue
        title = plain_text(hd.group(2))
        if not (2 <= len(title) <= 30) or SKIP_TITLE.search(title):
            continue
        im = ID_RE.search(attrs)
        secs.append({'m': m, 'id': im.group(1) if im else None, 'title': title})
    if len(secs) < 3:
        return h, False
    if len(secs) > 16:                     # 太长就只列前 16 节，避免目录比正文还长
        secs = secs[:16]
    edits = []
    for i, s in enumerate(secs, 1):
        if not s['id']:
            nid = f'sec-{i}'
            s['id'] = nid
            edits.append((s['m'].end(1), f' id="{nid}"'))
    for pos, txt in sorted(edits, reverse=True):
        h = h[:pos] + txt + h[pos:]

    items = ''.join(f'<li><a href="#{s["id"]}">{html.escape(s["title"])}</a></li>' for s in secs)
    nav = (f'\n<nav class="ta-pagenav" data-teachany-page-nav aria-label="本页目录">\n'
           f'  <div class="ta-pagenav-head">📑 本页目录（{len(secs)} 节）</div>\n'
           f'  <ol>{items}</ol>\n'
           f'  <div class="ta-pagenav-move">'
           f'<button type="button" data-pagenav-prev>↑ 上一节</button>'
           f'<span class="ta-pagenav-status" data-pagenav-status></span>'
           f'<button type="button" data-pagenav-next>↓ 下一节</button></div>\n'
           f'</nav>\n')
    # 重新定位（ids 改动后偏移会变）：直接在第一个目标 section 之前插入
    first_id = secs[0]['id']
    fm = re.search(rf'<section\b[^>]*\bid="{re.escape(first_id)}"', h)
    if not fm:
        return h, False
    h = h[:fm.start()] + nav + h[fm.start():]

    if 'teachany-page-nav.css' not in h:
        link = '<link rel="stylesheet" href="../../assets/scripts/teachany-page-nav.css">'
        hm = HEAD_RE.search(h)
        if hm:
            h = h[:hm.start()] + link + '\n' + h[hm.start():]
    if 'teachany-page-nav.js' not in h:
        sc = '<script src="../../assets/scripts/teachany-page-nav.js" defer></script>'
        bm = BODY_RE.search(h)
        if bm:
            h = h[:bm.start()] + sc + '\n' + h[bm.start():]
    return h, True


def _page_title(h: str, i: int) -> str:
    """取第 i 个 slide-page 的标题（data-tsh / 首个 h1、h2）。"""
    pages = list(PAGE_RE.finditer(h))
    if not (0 < i <= len(pages)):
        return f'第 {i} 节'
    m = pages[i - 1]
    seg = h[m.end(): m.end() + 1500]
    tsh = re.search(r'data-tsh="([^"]*)"', m.group(1))
    label = (tsh.group(1) if tsh else '') or plain_text(
        (H2_RE.search(seg).group(2) if H2_RE.search(seg) else ''))
    label = re.sub(r'^(开场|精讲|方法范例|范例|例析|概念|互动|探究|真题练习|分层作业|小结|总结迁移)\s*[·\-]\s*', '', label)
    return (label or f'第 {i} 节')[:24]


def plan(cid: str):
    f = ROOT / 'community' / cid / 'index.html'
    if not f.is_file():
        return None, 'no-file', ''
    h = f.read_text(encoding='utf-8')
    if 'data-teachany-page-nav' in h or 'teachany-page-nav' in h:
        return None, 'already', ''
    pages = PAGE_RE.findall(h)
    if len(pages) >= 3:
        h2, ids = add_page_ids(h)
        h2, ok = upgrade_dots(h2)
        if not ok:
            return None, 'dot-pattern-unknown', ''
        # 静态章节跳转（deck 的导航点由 JS 生成，校验器只数静态 href，所以必须再给一份静态目录）
        links = ''.join(f'<li><a href="#{ids[i - 1]}">{i}. {_page_title(h2, i)}</a></li>'
                        for i in range(1, len(ids) + 1))
        nav = ('\n<details class="ta-pagenav" data-teachany-page-nav data-ta-pagenav-float>'
               f'<summary class="ta-pagenav-head">📑 目录（{len(ids)} 节）</summary>'
               f'<ol>{links}</ol>'
               '<div class="ta-pagenav-move">'
               '<button type="button" data-pagenav-prev>↑ 上一节</button>'
               '<span class="ta-pagenav-status" data-pagenav-status></span>'
               '<button type="button" data-pagenav-next>↓ 下一节</button></div>'
               '</details>\n')
        bm0 = BODY_RE.search(h2)
        if not bm0:
            return None, 'no-body', ''
        bstart = h2.find('<body', 0, bm0.start())
        at = h2.find('>', bstart) + 1 if bstart != -1 else bm0.start()
        h2 = h2[:at] + nav + h2[at:]

        style = ('<style id="ta-pagenav-deck-css">'
                 '.sidenav-dot{text-decoration:none}'
                 '.slide-page{scroll-margin-top:76px}</style>')
        hm = HEAD_RE.search(h2)
        if not hm:
            return None, 'no-head', ''
        h2 = h2[:hm.start()] + style + '\n' + h2[hm.start():]
        if 'teachany-page-nav.css' not in h2:
            h2 = h2[:hm.start()] + '<link rel="stylesheet" href="../../assets/scripts/teachany-page-nav.css">\n' + h2[hm.start():]
        if 'teachany-page-nav.js' not in h2:
            bme = BODY_RE.search(h2)
            h2 = h2[:bme.start()] + '<script src="../../assets/scripts/teachany-page-nav.js" defer></script>\n' + h2[bme.start():]
        return h2, f'deck:{len(ids)}页', 'deck'
    h2, ok = flat_nav(h)
    if not ok:
        return None, 'flat-too-few', ''
    return h2, 'flat', 'flat'


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--from-list', required=True)
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--limit', type=int, default=0)
    args = ap.parse_args()
    cids = [x.strip() for x in Path(args.from_list).read_text(encoding='utf-8').split() if x.strip()]
    if args.limit:
        cids = cids[: args.limit]
    ok = 0
    skip: dict[str, int] = {}
    for cid in cids:
        new, why, kind = plan(cid)
        if not new:
            skip[why] = skip.get(why, 0) + 1
            continue
        if not args.apply:
            print(f'  (dry) {cid:38} {why}')
            ok += 1
            continue
        good, why2 = apply_guarded(ROOT / 'community' / cid / 'index.html', new, cid)
        if good:
            ok += 1
        else:
            skip[why2] = skip.get(why2, 0) + 1
    print(f'{"写入" if args.apply else "干跑"}完成：{ok} 门；跳过 {skip}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
