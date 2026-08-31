#!/usr/bin/env python3
"""fix-structural.py — 单课件结构手术：删残缺开标签 + 删配对孤儿残骸

病灶模式（在 math-m-linear-equations / bio-m-biosphere 等 5 个课件
人工验证一致）：slide-page 解包手术留下的成对损伤——

  A. 残缺开标签：`<section ... class="section"` 写到行末断掉（无 >），
     下一行直接开新标签。grep 数到它、浏览器忽略它。
  B. 孤儿残骸：`id="knowledge-graph" style="...">` 开头（<section 被切掉）
     的裸段，到 </section> 结束。标题通常是重复拼接的「cid — cid」。

  A + B 数量上抵消 → grep 配平骗过检查器（病态平衡），但浏览器把
  A 之后到 B 的 </section> 之间所有模块吞进幽灵嵌套。

手术（每课件独立执行、独立验证）：
  1. 定位所有真残缺开标签（断点到首个 > 之间非纯属性字符），删除
  2. 定位所有孤儿残骸（id=...> 开头的裸段到 </section>），删除
  3. 验证：标签配平 + 栈扫描平衡 + 无残缺 + 无孤儿 + 图谱在 script 外

用法:
  python3 scripts/fix-structural.py <cid> [--dry]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
ATTR_TAIL = re.compile(r'^[\w\-="\'\s/]+>$')


def find_broken_opens(html):
    """真残缺开标签：行末 <section 无 >，断点到首个 > 之间非纯属性"""
    out = []
    for m in re.finditer(r'<section\b[^>]*$', html, re.M):
        rest = html[m.end():m.end() + 300]
        gt = rest.find('>')
        if gt < 0 or not ATTR_TAIL.match(rest[:gt + 1]):
            out.append(m.span())
    return out


def find_orphans(html):
    """孤儿残骸：id=...> 开头的裸行到 </section>"""
    out = []
    for m in re.finditer(r'^\s*id="[^"]*"[^>]*>\s*$', html, re.M):
        end = html.find('</section>', m.end())
        if 0 <= end <= m.end() + 2000:
            out.append((m.start(), end + len('</section>')))
    return out


def verify(html, cid):
    errs = []
    o, c = len(re.findall(r'<section\b', html)), len(re.findall(r'</section>', html))
    if o != c:
        errs.append(f'计数{o}/{c}')
    stack = []
    for m in re.finditer(r'<section\b|</section>', html):
        if m.group().startswith('<section'):
            stack.append(m)
        elif stack:
            stack.pop()
    if stack:
        errs.append(f'栈余{len(stack)}')
    if find_broken_opens(html):
        errs.append('残缺开标签未清')
    if find_orphans(html):
        errs.append('孤儿残骸未清')
    # 图谱必须在 script 外
    i = html.find('<section class="section" id="knowledge-graph"')
    if i >= 0:
        before = html[:i]
        if before.rfind('<script') > before.rfind('</script>'):
            errs.append('图谱嵌script')
    return errs


def find_stray_closes(html):
    """孤立闭标签：栈空时遇到的 </section>（无配对开标签）"""
    out = []
    stack = 0
    for m in re.finditer(r'<section\b[^>]*>|</section>', html):
        if m.group().startswith('<section'):
            stack += 1
        else:
            stack -= 1
            if stack < 0:
                out.append(m.span())
                stack = 0     # 继续扫描后续
    return out


def process(cid, dry=False):
    p = COMMUNITY / cid / 'index.html'
    html = p.read_text(encoding='utf-8', errors='replace')
    acts = []
    # 删残缺开标签（含行尾换行）
    for s, e in find_broken_opens(html):
        frag = html[s:e]
        assert '\n' not in frag
        tail = html[e:e + 1] == '\n'
        seg = frag + ('\n' if tail else '')
        acts.append(('残缺开标签', frag[-60:]))
        html = html.replace(seg, '', 1)
    # 删孤儿残骸（含前导空行）
    for s, e in find_orphans(html):
        seg = html[s:e]
        head = re.search(r'\n+\s*$', html[:s])
        full = html[head.start():e] if head else seg
        acts.append(('孤儿残骸', seg[:60]))
        html = html.replace(full, '\n', 1) if head else html.replace(seg, '', 1)
    # 删孤立闭标签（栈空时遇到的 </section>，含其行）
    while True:
        strays = find_stray_closes(html)
        if not strays:
            break
        s, e = strays[0]
        line_s = html.rfind('\n', 0, s) + 1
        line_e = html.find('\n', e)
        line_e = line_e + 1 if line_e > 0 else len(html)
        if html[line_s:s].strip() == '' and html[e:line_e].strip() == '':
            seg = html[line_s:line_e]          # 整行删
        else:
            seg = html[s:e]                    # 行内删
        acts.append(('孤立闭标签', seg[:60]))
        html = html.replace(seg, '', 1)
    errs = verify(html, cid)
    status = '❌ ' + '; '.join(errs) if errs else '✓ 验证通过'
    for kind, frag in acts:
        print(f'  删{kind}: ...{frag}')
    print(f'  {status}')
    if not dry and not errs and acts:
        p.write_text(html, encoding='utf-8')
        return True
    return False


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    dry = '--dry' in sys.argv
    if not args:
        print('用法: python3 fix-structural.py <cid> [cid...] [--dry]')
        return
    ok = 0
    for cid in args:
        print(f'== {cid}')
        try:
            if process(cid, dry):
                ok += 1
        except Exception as e:
            print(f'  ❌ 异常: {str(e)[:80]}')
    print(f'\n完成: {ok}/{len(args)} 写入' + ('（--dry 未写入）' if dry else ''))


if __name__ == '__main__':
    main()
