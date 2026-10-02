#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描「内联脚本在解析期就去找后面才出现的元素」这类运行时 null 错误。

现象：`const c=document.getElementById('cellCanvas'); c.getContext('2d')` 写在
画布**之前**的内联 <script> 里，解析到那一行时元素还不存在 → TypeError，
整段脚本剩下的绑定（滑块、读数、按钮）全部不执行 —— 页面看着"有交互区，但点了没反应"。

判定：内联脚本里 `getElementById('X')` / `querySelector('#X')` 的 X，
其 id 定义位置在脚本**之后**，且该脚本在引用前没有 DOMContentLoaded / window.onload 兜底。

用法:  python3 tools/scan-script-before-dom.py [--json /tmp/out.json]
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_RE = re.compile(r'<script\b([^>]*)>(.*?)</script>', re.S | re.I)
REF_RE = re.compile(r"getElementById\(\s*['\"]([^'\"]+)['\"]|querySelector\(\s*['\"]#([^'\"]+)['\"]")
WRAP_RE = re.compile(r'DOMContentLoaded|window\.onload|addEventListener\(\s*[\'"]load', re.I)


def brace_depth(s: str) -> int:
    """粗略的花括号净深度（忽略字符串/注释里的括号会有误差，但足以判定
    「引用是否写在某个函数体内部」——函数体内部的引用通常延后执行，不算解析期空引用）。"""
    s = re.sub(r'//[^\n]*', ' ', s)
    s = re.sub(r'/\*.*?\*/', ' ', s, flags=re.S)
    s = re.sub(r"'(?:[^'\\]|\\.)*'", "''", s)
    s = re.sub(r'"(?:[^"\\]|\\.)*"', '""', s)
    s = re.sub(r'`(?:[^`\\]|\\.)*`', '``', s)
    return s.count('{') - s.count('}')


def scan(cid: str):
    f = ROOT / 'community' / cid / 'index.html'
    if not f.is_file():
        return None
    h = f.read_text(encoding='utf-8', errors='ignore')
    bad = []
    for m in SCRIPT_RE.finditer(h):
        attrs, body = m.group(1), m.group(2)
        if 'src=' in attrs or 'type="application/json"' in attrs or "type='application/json'" in attrs:
            continue
        if not body.strip():
            continue
        for r in REF_RE.finditer(body):
            eid = r.group(1) or r.group(2)
            if not eid or eid.startswith('{{'):
                continue
            head = body[: r.start()]
            if WRAP_RE.search(head):          # 已用 DOMContentLoaded 包住
                continue
            if WRAP_RE.search(attrs):
                continue
            if brace_depth(head) > 0:         # 写在函数体里 → 延后执行，不是解析期空引用
                continue
            d = re.search(r'id=[\'"]%s[\'"]' % re.escape(eid), h)
            if d and d.start() > m.start():
                bad.append({'id': eid, 'script_at': m.start(), 'id_at': d.start()})
                break
    return bad or None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', default='')
    args = ap.parse_args()
    hits = {}
    for d in sorted((ROOT / 'community').iterdir()):
        r = scan(d.name)
        if r:
            hits[d.name] = r
    print('解析期空引用的课件：%d 门' % len(hits))
    for cid, items in list(hits.items())[:25]:
        print('  %-38s %s' % (cid, ', '.join(i['id'] for i in items[:4])))
    if args.json:
        Path(args.json).write_text(json.dumps(hits, ensure_ascii=False, indent=1), encoding='utf-8')
        print('→', args.json)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
