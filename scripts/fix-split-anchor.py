#!/usr/bin/env python3
"""按锚点拆分指定课件中的长叙事卡片：在 </p> 边界拆成多张同级卡片，
每张可见计字（CJK+拉丁词）≤180。非 <p> 的尾部元素（图片/盒子）随最后一组。
用法: python3 fix-split-anchor.py <course-id> <anchor1> [anchor2 ...]
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STRIP_RE = re.compile(r'<(script|style|svg|textarea|template|table|details|button)\b[\s\S]*?</\1>', re.I)
TARGET = 180

def visible(t):
    t = STRIP_RE.sub('', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = re.sub(r'\s+', '', t)
    cjk = len(re.findall(r'[\u4e00-\u9fff]', t))
    words = len(re.findall(r'[A-Za-z0-9]+', re.sub(r'[\u4e00-\u9fff]', ' ', t)))
    return cjk + words

def find_card(html, anchor):
    i = html.find(anchor)
    if i < 0:
        return None
    # 向上找最近的 <div ... card ...>
    starts = [m.start() for m in re.finditer(r'<div\b[^>]*>', html[:i])]
    for s in reversed(starts):
        tag_end = html.index('>', s) + 1
        tag = html[s:tag_end]
        if 'card' not in tag:
            continue
        # 深度匹配找结束
        depth, pos = 0, s
        while True:
            m = re.search(r'<div\b|</div>', html[pos:])
            if not m:
                return None
            depth += 1 if m.group(0) == '<div' else -1
            pos += m.end()
            if depth == 0:
                if pos > i:
                    return (s, pos)
                break
    return None

def split_card(html, span):
    s, e = span
    full = html[s:e]
    open_end = full.index('>') + 1
    open_tag = full[:open_end]
    inner = full[open_end:full.rfind('</div>')]
    # 切成 <p> 单元与其他元素
    units = []
    pos = 0
    for m in re.finditer(r'<p\b[\s\S]*?</p>', inner):
        pre = inner[pos:m.start()]
        if pre.strip():
            units.append(pre)
        units.append(m.group(0))
        pos = m.end()
    tail = inner[pos:]
    if tail.strip():
        units.append(tail)
    if len(units) < 2:
        return None
    groups, cur, cur_len = [], [], 0
    for u in units:
        L = visible(u)
        if cur and cur_len + L > TARGET:
            groups.append(cur)
            cur, cur_len = [], 0
        cur.append(u)
        cur_len += L
    if cur:
        groups.append(cur)
    if len(groups) < 2:
        # 单段落卡：在句子边界把段落切成两半，分成两张卡
        if len(units) == 1:
            m = re.match(r'(<p\b[^>]*>)([\s\S]*?)(</p>)', units[0])
            if m:
                body = m.group(2)
                sentences = [x for x in re.split(r'(?<=[。；！？])', body) if x]
                if len(sentences) >= 2:
                    half, acc, cut = visible(body) / 2, 0, 1
                    for idx, s_ in enumerate(sentences):
                        acc += visible(s_)
                        if acc >= half:
                            cut = idx + 1
                            break
                    cut = max(1, min(cut, len(sentences) - 1))
                    p1 = m.group(1) + ''.join(sentences[:cut]) + m.group(3)
                    p2 = m.group(1) + ''.join(sentences[cut:]) + m.group(3)
                    return html[:s] + open_tag + p1 + '</div>\n' + open_tag + p2 + '</div>' + html[e:]
        return None
    cards = []
    for g in groups:
        cards.append(open_tag + ''.join(g) + '</div>')
    return html[:s] + '\n'.join(cards) + html[e:]

def main():
    cid = sys.argv[1]
    anchors = sys.argv[2:]
    hpath = os.path.join(ROOT, 'community', cid, 'index.html')
    html = open(hpath, encoding='utf-8').read()
    n = 0
    for a in anchors:
        span = find_card(html, a)
        if not span:
            print(f'anchor not found: {a[:30]}')
            continue
        new = split_card(html, span)
        if new:
            html = new
            n += 1
        else:
            print(f'cannot split: {a[:30]}')
    if n:
        open(hpath, 'w', encoding='utf-8').write(html)
    print(cid, 'split', n, 'cards')

if __name__ == '__main__':
    main()
