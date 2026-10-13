#!/usr/bin/env python3
"""check-contrast.py — 文字/底色对比度扫描（DOM 继承级，WCAG 4.5:1）

做法：html.parser 遍历 DOM，每个元素计算
  有效背景 = 自己 background ?? 最近祖先 background ?? body 背景
  有效颜色 = 自己 color ?? 继承（这里只看自己/内联，类样式按选择器匹配）
然后算对比度。只报告含可见文字且对比度 < 4.5 的元素。

样式来源：
  1. <style> 里的类/id/标签选择器规则（简单选择器，不含组合/伪类）
  2. 内联 style
  3. CSS 变量 var(--x) 从 :root 解析；rgba 与背景合成

用法:
  python3 check-contrast.py [cid...]     扫描（无参数全库）
  python3 check-contrast.py --summary    汇总
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

NAMES = {
    'white': (255, 255, 255), 'black': (0, 0, 0), 'red': (255, 0, 0),
    'green': (0, 128, 0), 'blue': (0, 0, 255), 'gray': (128, 128, 128),
    'grey': (128, 128, 128), 'yellow': (255, 255, 0), 'orange': (255, 165, 0),
    'purple': (128, 0, 128), 'pink': (255, 192, 203), 'brown': (165, 42, 42),
    'transparent': None,
}


def parse_color(s, variables, base_bg):
    if not s:
        return None
    s = s.strip().lower().rstrip(';')
    # 渐变：取渐变中第一个颜色作为代表（近似）
    if 'gradient' in s:
        m = re.search(r'(#[0-9a-f]{3,8}|rgba?\([^)]+\))', s)
        return parse_color(m.group(1), variables, base_bg) if m else None
    m = re.match(r'var\((--[\w-]+)\)', s)
    if m:
        v = variables.get(m.group(1))
        return parse_color(v, variables, base_bg) if v else None
    m = re.match(r'#([0-9a-f]{3,8})$', s)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = ''.join(c * 2 for c in h)
        if len(h) >= 6:
            return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
        return None
    m = re.match(r'rgba?\(([^)]+)\)', s)
    if m:
        parts = [p.strip() for p in m.group(1).split(',')]
        try:
            r, g, b = (int(float(parts[i])) for i in range(3))
            if len(parts) == 4:
                a = float(parts[3])
                r = round(r * a + base_bg[0] * (1 - a))
                g = round(g * a + base_bg[1] * (1 - a))
                b = round(b * a + base_bg[2] * (1 - a))
            return (r, g, b)
        except (ValueError, IndexError):
            return None
    return NAMES.get(s)


def luminance(rgb):
    def f(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(c1, c2):
    l1, l2 = luminance(c1), luminance(c2)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def style_props(st):
    out = {}
    for m in re.finditer(r'([\w-]+)\s*:\s*([^;]+)', st):
        out[m.group(1).strip().lower()] = m.group(2).strip()
    return out


class Scanner(HTMLParser):
    def __init__(self, rules, variables, body_bg):
        super().__init__(convert_charrefs=True)
        self.rules = rules          # {选择器: props}
        self.variables = variables
        self.body_bg = body_bg
        self.stack = []             # [(tag, 有效bg, 有效color, 描述)]
        self.issues = []
        self.skip = 0

    def props_of(self, tag, attrs):
        """元素的有效样式：标签规则 + 类规则 + id规则 + 内联"""
        props = {}
        ad = dict(attrs)
        for sel, p in self.rules.items():
            if sel == tag:
                props.update(p)
            elif sel.startswith('.') and sel[1:] in (ad.get('class') or '').split():
                props.update(p)
            elif sel.startswith('#') and sel[1:] == ad.get('id'):
                props.update(p)
        if 'style' in ad:
            props.update(style_props(ad['style']))
        return props, ad

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip += 1
            return
        parent_bg = self.stack[-1][1] if self.stack else self.body_bg
        parent_fg = self.stack[-1][2] if self.stack else None
        props, ad = self.props_of(tag, attrs)
        bg = parse_color(props.get('background') or props.get('background-color'),
                         self.variables, parent_bg) or parent_bg
        fg = parse_color(props.get('color'), self.variables, bg) or parent_fg
        op = props.get('opacity')
        if op:
            try:
                a = float(op)
                if a < 1 and fg:
                    fg = tuple(round(f * a + b * (1 - a)) for f, b in zip(fg, bg))
            except ValueError:
                pass
        desc = f"{tag}.{'.'.join((ad.get('class') or '').split())[:30]}"
        self.stack.append([tag, bg, fg, desc])

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = max(0, self.skip - 1)
            return
        # 弹到匹配的 tag
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self.skip or not self.stack:
            return
        text = data.strip()
        if len(text) < 2:
            return
        tag, bg, fg, desc = self.stack[-1]
        if fg is None or bg is None:
            return
        r = contrast(fg, bg)
        if r < 4.5:
            key = (desc, fg, bg)
            if not any(i[0] == key for i in self.issues):
                self.issues.append((key, text[:20], round(r, 2)))


def scan(html):
    # CSS 变量
    variables = {}
    root = re.search(r':root\{([^}]*)\}', html)
    if root:
        for m in re.finditer(r'(--[\w-]+)\s*:\s*([^;]+)', root.group(1)):
            variables[m.group(1)] = m.group(2).strip()
    # body 背景
    body_bg = (255, 255, 255)
    bm = re.search(r'body\s*\{([^}]*)\}', html)
    if bm:
        p = style_props(bm.group(1))
        c = parse_color(p.get('background') or p.get('background-color'),
                        variables, (255, 255, 255))
        if c:
            body_bg = c
    # 简单选择器规则
    rules = {}
    for m in re.finditer(r'([^{}<>@]+)\{([^}]*)\}', html):
        sel = m.group(1).strip()
        if ',' in sel or ' ' in sel or ':' in sel or '<' in sel:
            continue
        if re.match(r'^[.#]?[\w-]+$', sel):
            rules[sel] = style_props(m.group(2))
    sc = Scanner(rules, variables, body_bg)
    sc.feed(html)
    return [(k, t, r) for k, t, r in sc.issues]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    summary = '--summary' in sys.argv
    cids = args or [d.name for d in sorted(COMMUNITY.iterdir())
                    if (d / 'index.html').is_file()]
    total = Counter()
    files = []
    for cid in cids:
        html = (COMMUNITY / cid / 'index.html').read_text(
            encoding='utf-8', errors='replace')
        issues = scan(html)
        if issues:
            files.append((cid, issues))
            for (desc, fg, bg), _, r in issues:
                total[desc] += 1
    print(f'扫描 {len(cids)} 个课件：{len(files)} 个有对比度问题')
    if summary:
        for k, v in total.most_common(10):
            print(f'  {k}: {v}')
    for cid, issues in files[:10]:
        print(f'  ❌ {cid}')
        for (desc, fg, bg), t, r in issues[:3]:
            print(f'     {desc}: rgb{fg} on rgb{bg} = {r} | 「{t}」')


if __name__ == '__main__':
    main()
