#!/usr/bin/env python3
"""拆分超长卡片（质检 #09）：把可见文字 >200 字的简单卡片按句子/段落边界
拆成多张同级卡片。只处理无嵌套 <div> 的简单卡片；复杂卡片跳过并报告。
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARD_RE = re.compile(r'<div[^>]*class="[^"]*card[^"]*"[^>]*>([\s\S]*?)</div>', re.I)
STRIP_RE = re.compile(r'<(script|style|svg|textarea|template)\b[\s\S]*?</\1>', re.I)
BLOCK_RE = re.compile(r'<(h[1-6]|p|li|blockquote)[^>]*>[\s\S]*?</\1>', re.I)
TARGET = 140   # 每张卡目标可见字数
LIMIT = 200

def visible_len(s):
    t = STRIP_RE.sub('', s)
    t = re.sub(r'<[^>]+>', '', t)
    t = re.sub(r'\s+', '', t)
    return len(t)

def split_sentences(html_block):
    """把单个块级元素的纯文本按句号/分号切成更小的 <p>。"""
    m = re.match(r'<(p|li)([^>]*)>([\s\S]*?)</\1>$', html_block.strip())
    if not m:
        return [html_block]
    tag, attrs, inner = m.group(1), m.group(2), m.group(3)
    if '<' in inner:  # 内含标签，不拆
        return [html_block]
    parts = [p for p in re.split(r'(?<=[。；！？])', inner) if p.strip()]
    if len(parts) <= 1:
        return [html_block]
    return [f'<{tag}{attrs}>{p}</{tag}>' for p in parts]

def split_card(m):
    full = m.group(0)
    inner = m.group(1)
    if '<div' in inner:
        return None  # 复杂卡片跳过
    open_tag = full[:full.index('>') + 1]
    # 拆成块级单元
    blocks = []
    pos = 0
    for b in BLOCK_RE.finditer(inner):
        pre = inner[pos:b.start()].strip()
        if pre:
            blocks.append(pre)
        blocks.append(b.group(0))
        pos = b.end()
    tail = inner[pos:].strip()
    if tail:
        blocks.append(tail)
    # 长块按句子再拆
    units = []
    for b in blocks:
        if visible_len(b) > TARGET:
            units.extend(split_sentences(b))
        else:
            units.append(b)
    # 分组
    groups, cur, cur_len = [], [], 0
    for u in units:
        L = visible_len(u)
        if cur and cur_len + L > TARGET:
            groups.append(cur)
            cur, cur_len = [], 0
        cur.append(u)
        cur_len += L
    if cur:
        groups.append(cur)
    if len(groups) <= 1:
        return None  # 拆不出更多
    cards = []
    for i, g in enumerate(groups):
        cls = open_tag
        cards.append(cls + '\n' + '\n'.join(g) + '\n</div>')
    return '\n'.join(cards)

def process(cid):
    hpath = os.path.join(ROOT, 'community', cid, 'index.html')
    html = open(hpath, encoding='utf-8').read()
    out, last, n_split, n_skip = [], 0, 0, 0
    for m in CARD_RE.finditer(html):
        out.append(html[last:m.start()])
        if visible_len(m.group(1)) > LIMIT:
            new = split_card(m)
            if new:
                out.append(new)
                n_split += 1
            else:
                out.append(m.group(0))
                n_skip += 1
        else:
            out.append(m.group(0))
        last = m.end()
    out.append(html[last:])
    if n_split:
        open(hpath, 'w', encoding='utf-8').write(''.join(out))
    return n_split, n_skip

def main():
    recs = json.load(open(os.path.join(ROOT, 'qc-all-report.json'), encoding='utf-8'))
    f09 = [r['id'] for r in recs if any(x.startswith('#09') for x in r['failed'])]
    total_split, total_skip, skipped_courses = 0, 0, []
    for cid in f09:
        try:
            s, k = process(cid)
        except Exception as e:
            s, k = 0, -1
        total_split += s
        total_skip += max(k, 0)
        if k:
            skipped_courses.append(cid)
    print(f'cards split: {total_split}, unsplittable(complex): {total_skip}')
    print('courses with complex cards:', skipped_courses)

if __name__ == '__main__':
    main()
