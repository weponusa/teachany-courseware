#!/usr/bin/env python3
"""fix-slide-nesting.py — 拆解 slide-page 嵌套（纯移动手术）

损伤模式（141个课件，人工验证 galvanic-cell 等3个后确认主流形态）：
某个 slide-page（通常是开场页）没有在正确位置闭合，把后续若干
独立页整个吞进嵌套。表现为 slide-page 出现在 depth>0 位置。

手术（纯移动，不改内容）：
  对每个嵌套的 slide-page X：剪出 X 的完整区间
  [X开标签, X的配对闭合]，插入到它最近的 slide-page 祖先 A 的
  闭合标签之后。迭代直到无嵌套。

不变量（每个课件验证）：
  - section 开/闭总数不变（纯移动）
  - 栈扫描平衡
  - 嵌套 slide-page 归零
  - 纯文本字符集不变（去标签后文本一致）

用法: python3 scripts/fix-slide-nesting.py <cid> [cid...] [--dry]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
TAG = re.compile(r'<section\b[^>]*>|</section>')


def scan_nested(html):
    """返回 [(X_start, X_end, A_close_end)]：嵌套页区间与祖先闭合末端"""
    out = []
    depth = 0
    stack = []          # (pos, is_slide_page, open_tag)
    for m in TAG.finditer(html):
        if m.group().startswith('<section'):
            is_sp = 'slide-page' in m.group()
            if is_sp and depth > 0:
                # 找 X 的配对闭合
                d2, x_end = depth + 1, None
                for m2 in TAG.finditer(html, m.end()):
                    if m2.group().startswith('<section'):
                        d2 += 1
                    else:
                        d2 -= 1
                        if d2 == depth:
                            x_end = m2.end()
                            break
                if x_end is None:
                    continue
                # 最近的 section 祖先（slide-page 或普通 section 均可：
                # 部分课件的嵌套页被普通 section 吞噬）
                anc = stack[-1] if stack else None
                if anc is None:
                    continue
                # 祖先的配对闭合
                d3, a_close = 0, None
                for m3 in TAG.finditer(html, anc[0]):
                    if m3.group().startswith('<section'):
                        d3 += 1
                    else:
                        d3 -= 1
                        if d3 == 0:
                            a_close = m3.end()
                            break
                if a_close and x_end <= a_close:
                    out.append((m.start(), x_end, a_close))
            stack.append((m.start(), is_sp))
            depth += 1
        else:
            if stack:
                stack.pop()
            depth -= 1
    return out


def fix(html):
    """迭代移出嵌套页，返回 (新html, 移动次数, 长度净增量)

    关键：从文件序最末的嵌套页开始处理。若按文件正序处理，每页都
    插到「祖先闭合后」同一位置，后移出的会插在先移出的前面——
    同一祖先的并列页全部倒序（曾致 116 个课件页序反转，已回滚重做）。
    倒序处理则后移出的先落位、先移出的插到它前面，保持原序。
    """
    moves = 0
    net = 0
    while True:
        nested = scan_nested(html)
        if not nested:
            break
        xs, xe, ac = nested[-1]          # 取最末的嵌套页（见 docstring）
        seg = html[xs:xe]
        # 剪出（连同前导换行，保持整洁）
        cut_s = xs
        lead = re.search(r'\n[ \t]*$', html[:xs])
        if lead and html[xs:xe].lstrip() == seg:
            cut_s = lead.start() + 1
        html = html[:cut_s] + html[xe:]
        # 插入到祖先闭合后（闭合位置前移了 xe-cut_s）
        ac2 = ac - (xe - cut_s)
        nl = '\n\n' if html[ac2 - 1] != '\n' else '\n'
        html = html[:ac2] + nl + seg + html[ac2:]
        net += len(nl) - (xs - cut_s)
        moves += 1
        if moves > 60:
            break
    return html, moves, net


def verify(old, new, net=0):
    errs = []
    for pat in (r'<section\b', r'</section>'):
        if len(re.findall(pat, old)) != len(re.findall(pat, new)):
            errs.append('section数变化')
            break
    # 纯移动手术：长度变化必须精确等于「插入换行 - 删除前导空白」。
    # 不能用去标签文本对比——story 断口的孤立 '<' 会与后续标签组合成
    # 不同的"假标签"被 <[^>]+> 误删，造成假阳性。
    if len(new) - len(old) != net:
        errs.append(f'长度不守恒({len(new)-len(old)}≠{net})')
    depth = 0
    for m in TAG.finditer(new):
        depth += 1 if m.group().startswith('<section') else -1
        if depth < 0:
            errs.append('栈负')
            break
    if depth != 0:
        errs.append('栈不平衡')
    if scan_nested(new):
        errs.append('仍有嵌套')
    return errs


def process(cid, dry=False):
    p = COMMUNITY / cid / 'index.html'
    old = p.read_text(encoding='utf-8', errors='replace')
    if not scan_nested(old):
        return None
    new, moves, net = fix(old)
    errs = verify(old, new, net)
    if errs:
        print(f'  ❌ {cid}: {"; ".join(errs)}（未写入）')
        return False
    print(f'  ✓ {cid}: 移出 {moves} 页')
    if not dry:
        p.write_text(new, encoding='utf-8')
        return True
    return 'dry'


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    dry = '--dry' in sys.argv
    ok = fail = skip = 0
    for cid in args:
        r = process(cid, dry)
        if r is True:
            ok += 1
        elif r is False:
            fail += 1
        else:
            skip += 1
    print(f'\n写入 {ok}，失败 {fail}，跳过 {skip}' + ('（--dry 未写入）' if dry else ''))


if __name__ == '__main__':
    main()
