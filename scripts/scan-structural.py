#!/usr/bin/env python3
"""scan-structural.py — 全库结构病灶扫描（只读）

从三个试点课件总结出的病灶模式，全库排查：

S1 图谱嵌 script：`id="knowledge-graph"` 的 section 出现在 <script> 内
   ——图谱不渲染 + 页面 JS 被打断（最严重，两个试点课件均中招）
S2 残缺开标签：`<section ...` 后无 `>`（真残缺，非跨行合法）
   ——grep 数量配平但浏览器忽略，通常伴随病态平衡
S3 孤儿残骸：`id="..."` 开头无 `<section` 的裸文本段
   ——渲染出裸内容（如重复图谱）
S4 任意模块嵌 script：除图谱外的其他 section 嵌在 script 内
S5 病态平衡：grep 的 section 开/闭数量差 ≠ 栈扫描的数量差

输出按严重度排序的课件清单。
用法: python3 scripts/scan-structural.py [limit]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

SCRIPT_OPEN = re.compile(r'<script\b')
SCRIPT_CLOSE = re.compile(r'</script>')
SECTION_ANY = re.compile(r'<section\b|</section>')
SECTION_OPEN = re.compile(r'<section\b')
SECTION_CLOSED = re.compile(r'<section\b[^>]*>')
SECTION_ORPHAN_TEXT = re.compile(r'^\s*id="[^"]*"[^>]*>\s*$', re.M)


def scan(html):
    """返回病灶列表 [(严重度, 描述)]"""
    issues = []

    # script 区间集合
    spans = []
    pos = 0
    while True:
        a = html.find('<script', pos)
        if a < 0:
            break
        b = html.find('</script>', a)
        if b < 0:
            spans.append((a, len(html)))
            break
        spans.append((a, b + len('</script>')))
        pos = b + 9
    in_script = lambda i: any(a <= i < b for a, b in spans)

    # S1/S4: section 开标签在 script 内
    for m in SECTION_OPEN.finditer(html):
        if in_script(m.start()):
            sid = (re.search(r'id="([^"]+)"', html[m.start():m.start() + 200]) or [None, '?'])[1]
            sev = 1 if sid == 'knowledge-graph' else 4
            issues.append((sev, f'S{sev}:{sid}嵌script'))

    # S2: 残缺开标签（行末 <section 无 >，且断点到首个 > 之间非纯属性）
    ATTR_TAIL = re.compile(r'^[\w\-="\'\s/]+>$')
    for m in re.finditer(r'<section\b[^>]*$', html, re.M):
        rest = html[m.end():m.end() + 300]
        gt = rest.find('>')
        if gt < 0 or not ATTR_TAIL.match(rest[:gt + 1]):
            line = html.count('\n', 0, m.start()) + 1
            issues.append((2, f'S2:残缺开标签@{line}'))

    # S3: 孤儿残骸（id=...> 开头的裸文本行）
    for m in SECTION_ORPHAN_TEXT.finditer(html):
        seg = html[m.start():m.start() + 300]
        if '</section>' in seg:
            sid = (re.search(r'id="([^"]+)"', seg) or [None, '?'])[1]
            issues.append((3, f'S3:孤儿残骸({sid})'))

    # S5: 病态平衡
    g_open = len(SECTION_OPEN.findall(html))
    g_close = len(re.findall(r'</section>', html))
    stack = []
    for m in SECTION_ANY.finditer(html):
        if m.group().startswith('<section'):
            stack.append(m)
        elif stack:
            stack.pop()
    if g_open != g_close or stack:
        issues.append((5, f'S5:计数{g_open}/{g_close}栈余{len(stack)}'))

    return issues


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    rows = []
    for d in sorted(COMMUNITY.iterdir()):
        f = d / 'index.html'
        if not f.is_file():
            continue
        try:
            html = f.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        issues = scan(html)
        if issues:
            sev = min(i[0] for i in issues)
            rows.append((sev, d.name, issues))
    rows.sort(key=lambda r: (r[0], r[1]))
    print(f'有结构病灶的课件 {len(rows)} 个（按严重度）：')
    print()
    for sev, name, issues in rows[:limit]:
        tag = {1: 'S1图谱嵌JS', 2: 'S2残缺标签', 3: 'S3孤儿残骸', 4: 'S4模块嵌JS', 5: 'S5配平异常'}[sev]
        print(f'{tag:12} {name}')
        for s, desc in issues[:3]:
            print(f'             - {desc}')
    if len(rows) > limit:
        print(f'... 其余 {len(rows) - limit} 个略')


if __name__ == '__main__':
    main()
