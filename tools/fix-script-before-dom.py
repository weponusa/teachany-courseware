#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修「内联脚本在解析期就去找后面才出现的元素」导致的运行时 TypeError。

症状：`const canvas=document.getElementById('chem-canvas'); const ctx=canvas.getContext('2d');`
写在画布**之前**，解析到该行时元素还不存在 → TypeError，整段脚本其余绑定（滑块、读数、
按钮、绘图函数）全部不执行。页面看着有交互区，实际点了没反应。

修法：把「以该引用开头的那一段顶层语句」用 DOMContentLoaded 包住，延后到 DOM 解析完再跑。
- 只包到脚本里已有的 `document.addEventListener('DOMContentLoaded'` 之前（避免嵌套）；
  没有就包到脚本末尾。
- **安全网**：若被包区间里声明的顶层名字（const/let/var/function）在区间**之外**还有引用
  （典型是 HTML 的 onclick="foo()"），说明这些名字要暴露到全局 → 跳过该课，交人工，
  绝不为了过闸把页面交互改坏。
- 每门都过 tools/_qa_gate（错误数上升即回滚）。

用法:  python3 tools/fix-script-before-dom.py --from-list /tmp/scriptdom.txt [--dry]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from _qa_gate import apply_guarded  # noqa: E402

SCRIPT_RE = re.compile(r'<script\b([^>]*)>(.*?)</script>', re.S | re.I)
REF_RE = re.compile(r"getElementById\(\s*['\"]([^'\"]+)['\"]|querySelector\(\s*['\"]#([^'\"]+)['\"]")
WRAP_RE = re.compile(r'DOMContentLoaded|window\.onload|addEventListener\(\s*[\'"]load', re.I)
DECL_RE = re.compile(r'\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)|\bfunction\s+([A-Za-z_$][\w$]*)')


def brace_depth(s: str) -> int:
    s = re.sub(r'//[^\n]*', ' ', s)
    s = re.sub(r'/\*.*?\*/', ' ', s, flags=re.S)
    s = re.sub(r"'(?:[^'\\]|\\.)*'", "''", s)
    s = re.sub(r'"(?:[^"\\]|\\.)*"', '""', s)
    s = re.sub(r'`(?:[^`\\]|\\.)*`', '``', s)
    return s.count('{') - s.count('}')


def find_target(h: str):
    """返回 (script_start, script_end, ref_pos, elem_id) 或 None。"""
    for m in SCRIPT_RE.finditer(h):
        attrs, body = m.group(1), m.group(2)
        if 'src=' in attrs or 'application/json' in attrs or not body.strip():
            continue
        if WRAP_RE.search(attrs):
            continue
        for r in REF_RE.finditer(body):
            eid = r.group(1) or r.group(2)
            if not eid:
                continue
            if WRAP_RE.search(body[: r.start()]) or brace_depth(body[: r.start()]) > 0:
                continue
            d = re.search(r'id=[\'"]%s[\'"]' % re.escape(eid), h)
            if d and d.start() > m.start():
                return m.start(2), m.end(2), m.start(2) + r.start(), eid
    return None


def stmt_start(body: str, pos: int) -> int:
    """从引用位置往前找到该顶层语句的起点（跨过 ';' 或 '}' 就停）。"""
    i = pos
    while i > 0:
        ch = body[i - 1]
        if ch in ';}' or ch == '\n' and brace_depth(body[:i]) == 0 and body[:i].rstrip().endswith((')', ';')):
            break
        i -= 1
    return i


def wrap_range(body: str, start: int) -> int:
    """包装区间的结束位置：优先停在已有的 DOMContentLoaded 之前。"""
    m = re.search(r'document\.addEventListener\(\s*[\'"]DOMContentLoaded', body[start:])
    return start + m.start() if m else len(body)


def declared_names(chunk: str):
    names = set()
    for m in DECL_RE.finditer(chunk):
        n = m.group(1) or m.group(2)
        if n:
            names.add(n)
    return names


MARK = ("\n// 目标元素在本脚本之后才出现，延后到 DOM 解析完再绑定\n"
        "document.addEventListener('DOMContentLoaded',function(){\n")


def revert_html(h: str):
    """撤掉本工具插入的包装（保留原语句内容）。"""
    i = h.find(MARK)
    if i == -1:
        return None
    j = i + len(MARK)
    depth, k = 1, j
    while k < len(h):
        c = h[k]
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                break
        k += 1
    if k >= len(h):
        return None
    end = k + 1
    if h[end:end + 1] == ')':
        end += 1
    if h[end:end + 1] == ';':
        end += 1
    while h[end:end + 1] == '\n':
        end += 1
    return h[:i] + h[j:k] + h[end:]


def find_leak(h: str, s_start: int, s_end: int, a: int, b: int, names):
    """只在「会真的坏掉」的地方找泄漏：

    - 同一 <script> 里 chunk **之后**的部分如果还调用这个名字 → 包起来就找不到定义了；
    - HTML 的 on*= 内联处理器里引用这个名字 → 必须留在全局。

    刻意不扫全文档：`ctx`/`p`/`t` 这类短名在别处到处出现，全扫会全部误判成泄漏。
    """
    tail = h[s_start + b: s_end]
    other = h[:s_start] + h[s_end:]
    handlers = ' '.join(
        re.findall(r'on\w+\s*=\s*"([^"]*)"', other, re.I)
        + re.findall(r"on\w+\s*=\s*'([^']*)'", other, re.I)
    )
    for n in sorted(names):
        if len(n) < 3:            # 单双字母名（ctx/p/t/x…）在别处到处出现，不参与判断
            continue
        pat = r'\b%s\b' % re.escape(n)
        if re.search(pat + r'\s*\(', tail) or re.search(pat, handlers):
            return n
    return None


def fix_html(h: str):
    t = find_target(h)
    if not t:
        return None, 'no-target'
    s_start, s_end, ref, eid = t
    body = h[s_start:s_end]
    a = stmt_start(body, ref - s_start)
    b = wrap_range(body, a)
    chunk = body[a:b]
    if not chunk.strip():
        return None, 'empty-chunk'

    leak = find_leak(h, s_start, s_end, a, b, declared_names(chunk))
    if leak:
        return None, 'name-leak:' + leak

    new_body = (body[:a]
                + "\n// 目标元素在本脚本之后才出现，延后到 DOM 解析完再绑定\n"
                + "document.addEventListener('DOMContentLoaded',function(){\n"
                + chunk + "\n});\n"
                + body[b:])
    return h[:s_start] + new_body + h[s_end:], eid


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--from-list', required=True)
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--revert', action='store_true', help='撤掉本工具插入的包装')
    args = ap.parse_args()
    cids = [x.strip() for x in Path(args.from_list).read_text(encoding='utf-8').split() if x.strip()]

    if args.revert:
        n = 0
        for cid in cids:
            f = ROOT / 'community' / cid / 'index.html'
            if not f.is_file():
                continue
            h = f.read_text(encoding='utf-8')
            new = revert_html(h)
            if not new or new == h:
                continue
            ok, why = apply_guarded(f, new, cid)
            n += 1 if ok else 0
            if not ok:
                print('  ✗ revert %s: %s' % (cid, why))
        print('已撤销 %d 门' % n)
        return 0

    ok = skip = fail = 0
    for cid in cids:
        f = ROOT / 'community' / cid / 'index.html'
        if not f.is_file():
            continue
        h = f.read_text(encoding='utf-8')
        new, info = fix_html(h)
        if not new:
            skip += 1
            print('  ↷ %s: %s' % (cid, info))
            continue
        if args.dry:
            ok += 1
            continue
        good, why = apply_guarded(f, new, cid)
        if good:
            ok += 1
        else:
            fail += 1
            print('  ✗ %s: %s' % (cid, why))
    print('%s 可修 %d，跳过 %d，失败 %d' % ('干跑：' if args.dry else '写入：', ok, skip, fail))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
