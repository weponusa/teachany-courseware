#!/usr/bin/env python3
"""修复迁移后的 AI 学伴重复/错位。

真实现状（实测）
----------------
这类课件里 `[data-teachany-tutor-card]` 容器会出现**两处**：
  ① 迁移时我注入在 ai-tutor 页（第 16 页）内的占位容器 —— 位置正确，在分页内；
  ② **课件自带的** `<section class="ta-standard-section" id="teachany-ai-tutor-card">`
     —— 它在 `#slide-container` **之外**（容器闭合标签后面），既不属于任何一页，
     又会被 `teachany-tutor-card.js` 一起渲染。

`teachany-tutor-card.js` 是**按容器数量渲染**的：两个容器 = 同一张卡片整块显示两遍
（用户看到的就是末页那张"AI 学伴 · 关于…随时问"重复两次）。

正确修法（两次修正才定下来）
--------------------------
不是删我注入的那个（那样 ai-tutor 页会变空壳），而是：
  · 把**课件自带的** tutor 块**搬进** ai-tutor 页内（它的内容更完整）
  · 移除我注入的占位容器与说明段落
  · 结果：ai-tutor 页内恰好 1 个容器，容器外 0 个

⚠️ 计数只能匹配**真容器标签** `<div … data-teachany-tutor-card …>`：
  该字符串还出现在控制器自检数组里（`document.querySelector('[data-teachany-tutor-card]')`），
  按字符串计数会把 641 门里 453 门误报成重复（实际 42 门）。

用法：
  python3 tools/repair-ai-tutor-dup.py --list
  python3 tools/repair-ai-tutor-dup.py --apply
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTAINER = re.compile(r'<div\b[^>]*\bdata-teachany-tutor-card\b[^>]*>', re.I)
OWN_SECTION = re.compile(
    r'<section\b[^>]*\bid="teachany-ai-tutor-card"[^>]*>[\s\S]*?</section>', re.I)
MY_PARA = re.compile(
    r'<p>\s*把还没弄明白的地方写下来问 AI 学伴。[\s\S]{0,300}?</p>\s*', re.I)
MY_H2 = re.compile(r'<h2>\s*AI 学伴[\s\S]{0,40}?</h2>\s*', re.I)
PAGE_OPEN = re.compile(
    r'<section\b(?=[^>]*slide-page)[^>]*data-page-type="ai-tutor"[^>]*>', re.I)


def iter_courses():
    for base in ('community', 'examples'):
        d = ROOT / base
        if not d.is_dir():
            continue
        for c in sorted(d.iterdir()):
            f = c / 'index.html'
            if f.is_file():
                yield c.name, f


def inside_outside(h):
    """返回 (容器内 tutor 容器数, 容器外 tutor 容器数)。"""
    i = h.find('id="slide-container"')
    if i < 0:
        return 0, len(CONTAINER.findall(h))
    i = h.rfind('<', 0, i)
    open_end = h.find('>', i) + 1
    # 容器边界：用 div 配平找；失败则退化为剩下全文
    depth, j = 1, open_end
    tag = re.compile(r'<(/?)div\b[^>]*>', re.I)
    close = -1
    while True:
        m = tag.search(h, j)
        if not m:
            break
        if m.group(1) == '/':
            depth -= 1
            if depth == 0:
                close = m.start()
                break
        else:
            depth += 1
        j = m.end()
    body = h[open_end:close] if close > 0 else h[open_end:]
    tail = h[close:] if close > 0 else ''
    return len(CONTAINER.findall(body)), len(CONTAINER.findall(tail))


def scan():
    """目标 = tutor 容器**跑到 #slide-container 之外**的课件。

    这才是真正的结构缺陷：容器外的那个既不属于任何一页、又会被脚本一起渲染，
    于是同一张卡片在末页显示两遍。只看"总数 ≥2"会漏掉"已删过占位、只剩容器外那个"
    的状态（第一次修复后就是这种），所以按结构判定。
    """
    out = []
    for cid, f in iter_courses():
        h = f.read_text(encoding='utf-8', errors='ignore')
        if 'id="slide-sidenav"' not in h:
            continue
        ins, outs = inside_outside(h)
        if outs > 0:
            out.append((cid, ins + outs, f))
    return out


def repair(cid, f, dry=False):
    h = f.read_text(encoding='utf-8')
    before = len(CONTAINER.findall(h))
    if before < 2:
        return None
    own = OWN_SECTION.search(h)
    ai = PAGE_OPEN.search(h)
    if not ai:
        return (cid, before, before, '无 ai-tutor 页，跳过')

    new = h
    # 1) 移走容器外的课件自带 tutor 块
    own_html = ''
    if own:
        own_html = own.group(0)
        new = new[:own.start()] + new[own.end():]
    # 2) 清掉我注入的占位段落与旧标题（保留位置给搬进来的块）
    new = MY_PARA.sub('', new, count=1)
    new = MY_H2.sub('', new, count=1)
    # 3) 若 ai-tutor 页内已无容器，把课件自带块插入该页
    ai = PAGE_OPEN.search(new)
    if not ai:
        return (cid, before, before, '插入点丢失，放弃')
    seg_end = new.find('</section>', ai.end())
    if seg_end < 0:
        return (cid, before, before, '找不到页结束，放弃')
    if own_html:
        title = '<h2>AI 学伴 · 随时提问</h2>\n' if '<h2' not in new[ai.end():seg_end] else ''
        inject = title + own_html + '\n'
        new = new[:seg_end] + inject + new[seg_end:]

    after = len(CONTAINER.findall(new))
    if dry:
        return (cid, before, after, 'dry-run')
    if after >= before:
        return (cid, before, after, '无改善，未写入')
    f.write_text(new, encoding='utf-8')
    return (cid, before, after, '已把课件自带 tutor 块搬进 ai-tutor 页')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('course_id', nargs='*')
    a = ap.parse_args()
    items = scan()
    if a.course_id:
        want = set(a.course_id)
        items = [x for x in items if x[0] in want]
    if a.list or not a.apply:
        print(f'AI 学伴容器重复（真容器 ≥2）的课件：{len(items)} 门')
        for cid, n, _ in items:
            print(f'   {cid:40s} {n} 个容器')
        if not a.apply:
            print('\n加 --apply 实际修复')
        return 0
    ok = 0
    for cid, n, f in items:
        r = repair(cid, f)
        if r:
            cid, before, after, msg = r
            print(f'   {"✅" if after < before else "⚠️"} {cid:38s} {before} → {after} 个容器  {msg}')
            if after < before:
                ok += 1
    print(f'\n修复 {ok}/{len(items)} 门')
    return 0


if __name__ == '__main__':
    sys.exit(main())
