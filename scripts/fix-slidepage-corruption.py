#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复「开标签被删掉一截、只剩属性尾巴」的课件破损。

破损特征：页面上出现 =":5" data-page-type=… 、on" id="story" data-tts=… 之类的乱码文本，
          后面的模块也因此看不见。原因是某个标签的开头被删掉，剩下的属性串被浏览器当纯文本渲染。

两类破损：
  A. 外层 <div class="slide-page …"> 被删（片段里带 type="content" / data-page-index）
  B. 内层 <section class="section" id="…"> 被删（片段里带 id=" / data-tts / data-bloom-level）
破损时外层开标签与其闭合标签常被一起删掉，所以补完开标签还要补闭合标签。

用法：
    python3 scripts/fix-slidepage-corruption.py                 # 全库
    python3 scripts/fix-slidepage-corruption.py <course-id> ... # 指定课件
"""
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'community')

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
        'link', 'meta', 'param', 'source', 'track', 'wbr'}
TAG = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)([^>]*?)(/?)>')
ATTR_TXT = re.compile(r'\bdata-[a-z-]+\s*=|id="')

# 内层模块：tsh/id 关键词 -> (id, data-tts 值, 其余规范属性)
MODULES = [
    ('前测', 'pretest', 'pretest',
     'data-bloom-level="remember" data-scaffold="full" data-conceptest="true"'),
    ('专属证据', 'knowledge-specific-evidence', 'knowledge-specific-evidence',
     'data-bloom-level="analyze" data-scaffold="partial"'),
    ('真实情境', 'story', 'story', ''),
]
OUTER_TSH_HINT = '前测：你已经知道什么？'   # phy-h 系列外层 slide-page 专用文案


class LeakFinder(HTMLParser):
    """找出「本该是属性、却漏成可见文本」的片段起始位置"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.hits = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self.skip:
            self.skip -= 1

    def handle_data(self, d):
        if self.skip:
            return
        if ATTR_TXT.search(d):
            self.hits.append(self.getpos())   # (lineno, offset)


def noise_ranges(src):
    rs = []
    for pat in (r'<!--[\s\S]*?-->', r'<script\b[\s\S]*?</script>', r'<style\b[\s\S]*?</style>'):
        for m in re.finditer(pat, src, re.I):
            rs.append((m.start(), m.end()))
    return rs


def in_noise(pos, rs):
    return any(a <= pos < b for a, b in rs)


def line_starts(src):
    offs, pos = [0], 0
    for i, ch in enumerate(src):
        if ch == '\n':
            pos = i + 1
            offs.append(pos)
    return offs


def find_fragments(src):
    """返回片段的 (起点偏移, 终点偏移)，已排除 script/style/注释内的误报"""
    rs = noise_ranges(src)
    finder = LeakFinder()
    try:
        finder.feed(src)
        finder.close()
    except Exception:
        pass
    out = []
    for lineno, col in finder.hits:
        offs = line_starts(src)
        start = offs[lineno - 1] + col if lineno - 1 < len(offs) else col
        if in_noise(start, rs):
            continue
        gt = src.find('>', start)
        if gt < 0:
            continue
        out.append((start, gt + 1))
    return out


def scan(src):
    rs = noise_ranges(src)
    stack, bad = [], 0
    for m in TAG.finditer(src):
        if in_noise(m.start(), rs):
            continue
        close, name, selfc = m.group(1), m.group(2).lower(), m.group(4)
        if name in VOID or selfc == '/' or name not in ('div', 'section'):
            continue
        line = src[:m.start()].count('\n') + 1
        if close:
            if stack and stack[-1][0] == name:
                stack.pop()
            else:
                bad += 1
        else:
            stack.append((name, line))
    return stack, bad


def matching_close_end(src, open_m):
    rs = noise_ranges(src)
    name = open_m.group(2).lower()
    depth, pos = 1, open_m.end()
    while True:
        m = TAG.search(src, pos)
        if not m:
            return None
        if not in_noise(m.start(), rs):
            close, nm, selfc = m.group(1), m.group(2).lower(), m.group(4)
            if nm not in VOID and selfc != '/' and nm == name:
                if close:
                    depth -= 1
                    if depth == 0:
                        return m.end()
                else:
                    depth += 1
        pos = m.end()


def tsh_of(frag):
    m = re.search(r'tsh="([^"]*)"', frag)
    return m.group(1) if m else None


def nearest_outer(src, start):
    """片段之前最近的 slide-page 开标签 -> (tag名, tsh)；没有则 (None, None)"""
    seg = src[:start]
    idx = seg.rfind('class="slide-page')
    if idx < 0:
        return None, None
    lt = seg.rfind('<', 0, idx)
    if lt < 0:
        return None, None
    m = TAG.search(seg, lt)
    if not m:
        return None, None
    t = re.search(r'data-tsh="([^"]*)"', m.group(0))
    return m.group(2).lower(), (t.group(1) if t else None)


def build_replacement(frag, otag, otsh):
    """-> (完整开标签, 需要补的闭合标签名)"""
    tsh = tsh_of(frag) or otsh or ''
    # 先看是不是外层 slide-page：片段常被截在属性名中间（'age-type="content"'、'content" data-tsh=…'），
    # 所以只匹配尾部特征，并加一条 phy-h 系列专用文案提示。
    if ('type="content"' in frag or 'data-page-index' in frag
            or tsh == OUTER_TSH_HINT):                 # A. 外层 slide-page
        return ('<div class="slide-page ta-flat" data-page-index="5" '
                f'data-page-type="content" data-tsh="{tsh or "前测"}" data-slot="35">'), 'div'
    # 再看是不是某个已知内层模块（同样要容忍 id="…" / data-tts="…" 被截断）
    for kw, mid, tts, attrs in MODULES:                # B. 内层 section
        if kw in tsh or f'id="{mid}"' in frag or f'{tts}"' in frag:
            tag = (f'<section class="section" id="{mid}" data-tts="{tts}" '
                   f'data-tsh="{tsh}" {attrs}>').replace('  ', ' ').replace(' >', '>')
            return tag, (otag or 'section')
    return None, None


def repair(path):
    name = os.path.basename(os.path.dirname(path))
    total = 0
    for _ in range(6):
        src = open(path, encoding='utf-8').read()
        frags = find_fragments(src)
        if not frags:
            break
        start, end = frags[-1]                          # 从最后一处开始
        frag = src[start:end]
        otag, otsh = nearest_outer(src, start)
        rep, closer = build_replacement(frag, otag, otsh)
        if rep is None:
            print(f'  ⚠️ {name}: 无法判定模块，跳过 -> {frag.strip()[:70]}')
            break
        src2 = src[:start] + rep + src[end:]

        # 定位刚插入的开标签
        om = None
        for m in TAG.finditer(src2):
            if not m.group(1) and m.start() >= start and m.group(0) == rep:
                om = m
                break
        if om is None:
            print(f'  ❌ {name}: 找不到刚插入的开标签')
            break

        if closer == 'div' and rep.startswith('<div'):
            # A：闭合紧跟在其内层 <section> 的配对闭标签之后
            rs = noise_ranges(src2)
            sm = None
            pos = om.end()
            while True:
                m = TAG.search(src2, pos)
                if not m:
                    break
                if not in_noise(m.start(), rs) and not m.group(1) and m.group(2).lower() == 'section':
                    sm = m
                    break
                pos = m.end()
            if sm is None:
                print(f'  ❌ {name}: 外层 slide-page 内找不到内层 section')
                break
            anchor = matching_close_end(src2, sm)
        else:
            anchor = matching_close_end(src2, om)
        if anchor is None:
            print(f'  ❌ {name}: 找不到配对闭标签 -> {frag.strip()[:60]}')
            break

        stack, bad = scan(src2)
        if stack or bad:                                # 只有确实缺闭合时才补
            src2 = src2[:anchor] + f'\n</{closer}>' + src2[anchor:]
        stack2, bad2 = scan(src2)
        if stack2 or bad2:
            print(f'  ❌ {name}: 补完后仍不平衡 depth={len(stack2)} bad={bad2} {stack2[:3]}')
            break
        open(path, 'w', encoding='utf-8').write(src2)
        total += 1
    return total


def main():
    root = os.path.normpath(ROOT)
    targets = sys.argv[1:] if len(sys.argv) > 1 else sorted(os.listdir(root))
    fixed = 0
    for d in targets:
        p = os.path.join(root, d, 'index.html')
        if not os.path.isfile(p):
            continue
        n = repair(p)
        if n:
            fixed += 1
            print(f'✅ {d}: 修复 {n} 处')
    print(f'\n修复课件数: {fixed}')


if __name__ == '__main__':
    main()
