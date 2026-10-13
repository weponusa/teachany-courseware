#!/usr/bin/env python3
"""fix-kg-position.py — 知识图谱归位：从中间页移到课件最末

病灶：统一外壳手术插入的标准图谱（id="knowledge-graph"）嵌在了
中间 slide-page 页内，学生翻到该页看到图谱后，后面还有多页
（抽查反馈「知识图谱后面还是都有别的模块」）。

手术：
  1. 剪出标准图谱完整段
  2. 栈扫描找最后一个顶层 slide-page 的配对闭合
  3. 图谱插到该闭合之后（课件最末）

验证：配平、栈平衡、图谱唯一、图谱后无 slide-page、长度守恒。
用法: python3 scripts/fix-kg-position.py <cid> [cid...] [--dry]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
TAG = re.compile(r'<section\b[^>]*>|</section>')
KG = re.compile(
    r'<section class="section" id="knowledge-graph" style="max-width:1080px[^"]*">.*?</section>',
    re.S)


def last_slide_page_close(html):
    """最后一个顶层 slide-page 的闭合末端位置"""
    depth = 0
    last_close = None
    cur_start = None
    for m in TAG.finditer(html):
        if m.group().startswith('<section'):
            if depth == 0 and 'slide-page' in m.group():
                cur_start = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0 and cur_start is not None:
                last_close = m.end()
                cur_start = None
    return last_close


def process(cid, dry=False):
    p = COMMUNITY / cid / 'index.html'
    html = p.read_text(encoding='utf-8', errors='replace')
    m = KG.search(html)
    if not m:
        return None
    close = last_slide_page_close(html)
    if close is None:
        print(f'  ❌ {cid}: 找不到顶层slide-page')
        return False
    # 若图谱已在最后页之后，跳过
    if m.start() > close:
        return None
    kg = m.group()
    new = html[:m.start()] + html[m.end():]
    close -= m.end() - m.start() if m.start() < close else 0
    # 若图谱在闭合点之后（在页外但靠前），重算位置
    close = last_slide_page_close(new)
    new = new[:close] + '\n\n' + kg + new[close:]
    # 验证
    errs = []
    for pat in (r'<section\b', r'</section>'):
        if len(re.findall(pat, new)) != len(re.findall(pat, html)):
            errs.append('section数变化')
    depth = 0
    for x in TAG.finditer(new):
        depth += 1 if x.group().startswith('<section') else -1
        if depth < 0:
            errs.append('栈负')
            break
    if depth != 0:
        errs.append('栈不平衡')
    if new.count('id="knowledge-graph"') != 1:
        errs.append('图谱不唯一')
    i = new.find('id="knowledge-graph"')
    if re.search(r'<section\b[^>]*slide-page', new[i:]):
        errs.append('图谱后仍有页')
    if len(new) != len(html) + 2:
        errs.append('长度不守恒')
    if errs:
        print(f'  ❌ {cid}: {"; ".join(errs)}（未写入）')
        return False
    print(f'  ✓ {cid}: 图谱移至末尾')
    if not dry:
        p.write_text(new, encoding='utf-8')
        return True
    return 'dry'


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    dry = '--dry' in sys.argv
    ok = fail = skip = 0
    for cid in args:
        try:
            r = process(cid, dry)
            if r is True:
                ok += 1
            elif r is False:
                fail += 1
            else:
                skip += 1
        except Exception as e:
            print(f'  ❌ {cid}: {str(e)[:60]}')
            fail += 1
    print(f'\n写入 {ok}，失败 {fail}，跳过 {skip}')


if __name__ == '__main__':
    main()
