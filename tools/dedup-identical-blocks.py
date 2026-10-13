#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""删除「id 相同且内容逐字相同」的重复块（注入器跑两遍留下的残渣）。

为什么
----
`document.getElementById()` 只返回**第一个**匹配，所以重复块不只是浪费体积：
  · 重复的 `<style id="ta-…-css">` / 音频分段容器 → 后一份永远不生效；
  · 重复的拖拽卡片 / 按钮 / 输入框 → 拖走一个另一个还在，学生看着像坏了。

只删**逐字相同**的那一份（保留第一次出现的），内容不同的绝不碰——那可能是两个
真正不同的模块共用了一个 id，属于要人工判断的另一类问题。

护栏
----
· 候选位置必须在 `<script>` / `<style>` / 注释之外（否则会把 JS 字符串里的片段当 DOM 删掉）；
· 逐门过 tools/_qa_gate（质检错误数上升即回滚）。

用法:  python3 tools/dedup-identical-blocks.py [--apply] [--dry] [--from-list f]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from _qa_gate import apply_guarded, imbalance  # noqa: E402

MASK = re.compile(r'<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<!--.*?-->', re.S | re.I)
OPEN = re.compile(r'<(\w+)([^>]*?)\sid="([^"]+)"')
# 无 id 的 script/style：内容相同就是重复注入（会导致 Identifier already declared / 重复初始化）
BARE = re.compile(r'<script\b([^>]*)>(.*?)</script>|<style\b([^>]*)>(.*?)</style>', re.S | re.I)


def in_mask(pos: int, spans) -> bool:
    return any(a <= pos < b for a, b in spans)


def balanced(h: str, s: int) -> int:
    m = re.match(r'<(\w+)([^>]*)>', h[s:])
    if not m:
        return -1
    tag = m.group(1)
    depth, j = 1, s + m.end()
    for t in re.finditer(r'<(/?)%s\b[^>]*>' % tag, h[j:], re.I):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return j + t.end()
    return -1


def norm(s: str) -> str:
    return re.sub(r'\s+', ' ', s).strip()


def plan(cid: str):
    f = ROOT / 'community' / cid / 'index.html'
    if not f.is_file():
        return None, 0, 'no-file'
    h = f.read_text(encoding='utf-8')
    spans = [(m.start(), m.end()) for m in MASK.finditer(h)]
    first: dict[str, str] = {}
    drops: list[tuple[int, int]] = []
    for m in OPEN.finditer(h):
        if in_mask(m.start(), spans):
            continue
        e = balanced(h, m.start())
        if e == -1:
            continue
        key, body = m.group(3), h[m.start():e]
        if key in first:
            if norm(first[key]) == norm(body):
                drops.append((m.start(), e))
        else:
            first[key] = body
    n = len(drops)
    if not drops:
        out = h
    else:
        out = h
        for a, b in sorted(drops, reverse=True):
            tail = b
            while tail < len(out) and out[tail] in ' \t\r\n':
                tail += 1
            out = out[:a] + out[tail:]

    # ── 再去重「无 id 但内容相同」的 script/style ──────────────────────
    # 注入器跑两遍最典型的后遗症：同一个 <script> 出现两次 →
    #   ① const/let 重名 → 「Identifier 'X' has already been declared」，整段脚本不执行；
    #   ② 即使没报错也会把初始化/事件绑定跑两遍（页面上「渲染了两遍」）。
    bare_seen: dict[str, int] = {}
    bare_drops: list[tuple[int, int]] = []
    for m in BARE.finditer(out):
        if m.group(1) is not None:            # <script ...>…</script>
            body, key = m.group(2), 's:' + norm(m.group(2))
        else:
            body, key = m.group(4), 'c:' + norm(m.group(4))
        if not body.strip():
            continue
        if key in bare_seen:
            bare_drops.append((m.start(), m.end()))
        else:
            bare_seen[key] = m.start()
    for a, b in sorted(bare_drops, reverse=True):
        tail = b
        while tail < len(out) and out[tail] in ' \t\r\n':
            tail += 1
        out = out[:a] + out[tail:]
    n += len(bare_drops)
    if out == h:
        return None, 0, 'no-dup'
    return out, n, 'ok'


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--from-list', default='')
    args = ap.parse_args()

    if args.from_list:
        cids = [x.strip() for x in Path(args.from_list).read_text(encoding='utf-8').split() if x.strip()]
    else:
        cids = sorted(d.name for d in (ROOT / 'community').iterdir() if (d / 'index.html').is_file())

    ok = fail = 0
    for cid in cids:
        new, n, why = plan(cid)
        if not new:
            continue
        f = ROOT / 'community' / cid / 'index.html'
        h = f.read_text(encoding='utf-8')
        if imbalance(new) > imbalance(h):
            print(f'  ↷ {cid}: 标签失衡，跳过')
            continue
        if not args.apply:
            print(f'  (dry) {cid}: 可删 {n} 个重复块')
            ok += 1
            continue
        good, why2 = apply_guarded(f, new, cid)
        if good:
            ok += 1
            print(f'  ✓ {cid}: 删除 {n} 个重复块')
        else:
            fail += 1
            print(f'  ✗ {cid}: {why2}')
    print(f'{"写入" if args.apply else "干跑"}完成：{ok} 门处理，{fail} 门拒绝')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
