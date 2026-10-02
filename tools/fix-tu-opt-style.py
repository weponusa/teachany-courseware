#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补齐 .tu-opt 类随堂题的样式（370 门）。

现象：大批课件用了 TeachAny 标准随堂题标记
  <div class="tu-q" data-answer="B"> … <button class="tu-opt" data-choice="A">
但页面里没有对应的 CSS 选择器，选项退化成「贴着文字排成一行的裸按钮」，
看起来像版面错乱。选项样式在仓库里本来就是各课件内联定义（共享 CSS 里没有），
所以按仓库既有写法补一块主题自适应的规则即可。

为什么用中性灰 rgba + color:inherit：
  370 门里 154 门是浅色主题（--bg:#fffbf0）、134 门是深色（#0b1120）、
  34 门近白（#f8fafc）。硬编码深色底会毁掉浅色主题，所以用半透明中性灰
  ——浅底上显灰、深底上显亮；文字色继承主题，正误反馈保留语义红绿。

用:  python3 tools/fix-tu-opt-style.py [--limit N] [--dry]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))

from _qa_gate import apply_guarded  # noqa: E402

CSS_ID = 'ta-tu-opt-css'
CSS = """<style id="ta-tu-opt-css">
/* TeachAny 标准随堂题样式（主题自适应：中性半透明底 + 继承文字色） */
.tu-q,.tu-fill{margin:16px 0;padding:14px;border-radius:12px;background:rgba(127,127,127,.10)}
.tu-q h3{font-size:1.05rem;margin:0 0 6px}
.tu-opts{display:grid;gap:10px;margin-top:10px}
.tu-opt{display:block;width:100%;text-align:left;padding:12px 14px;border-radius:10px;
  border:1px solid rgba(127,127,127,.40);background:rgba(127,127,127,.10);
  color:inherit;font:inherit;font-size:15px;line-height:1.6;cursor:pointer;
  transition:border-color .15s,background .15s}
.tu-opt:hover{border-color:rgba(96,165,250,.90);background:rgba(96,165,250,.12)}
.tu-opt.is-right,.tu-opt.correct{border-color:#10b981;background:rgba(16,185,129,.18)}
.tu-opt.is-wrong,.tu-opt.wrong{border-color:#ef4444;background:rgba(239,68,68,.15)}
.tu-opt:disabled{cursor:default}
.tu-fb{margin-top:12px;padding:12px;border-radius:10px;border:1px solid rgba(245,158,11,.40);
  background:rgba(245,158,11,.12);line-height:1.7}
.tu-inquiry label{display:block;margin:10px 0}
.tu-inquiry textarea{width:100%;border-radius:10px;padding:10px;background:rgba(127,127,127,.10);
  color:inherit;border:1px solid rgba(127,127,127,.35);font:inherit;box-sizing:border-box}
.tu-save{margin-top:10px;padding:10px 16px;border-radius:10px;border:1px solid rgba(127,127,127,.40);
  background:rgba(127,127,127,.12);color:inherit;cursor:pointer;font:inherit}
</style>
"""

HAS_RULE = re.compile(r'\.tu-opt[^{};]*\{')


def needs_css(html: str) -> bool:
    if 'class="tu-opt' not in html and "class='tu-opt" not in html:
        return False
    if CSS_ID in html:
        return False
    return not HAS_RULE.search(html)


def inject(html: str) -> str:
    m = re.search(r'</head>', html, re.IGNORECASE)
    if not m:
        return ''
    return html[:m.start()] + CSS + html[m.start():]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--dry', action='store_true')
    args = ap.parse_args()

    targets = []
    for d in sorted((ROOT / 'community').iterdir()):
        f = d / 'index.html'
        if not f.is_file():
            continue
        if needs_css(f.read_text(encoding='utf-8', errors='ignore')):
            targets.append(d.name)
    print(f'待补样式课件：{len(targets)}')
    if args.limit:
        targets = targets[: args.limit]
    if args.dry:
        print('\n'.join(targets))
        return 0

    ok_n = fail_n = 0
    for cid in targets:
        f = ROOT / 'community' / cid / 'index.html'
        html = f.read_text(encoding='utf-8')
        new = inject(html)
        if not new:
            print(f'  ✗ {cid}: 无 </head>')
            fail_n += 1
            continue
        ok, why = apply_guarded(f, new, cid)
        if ok:
            ok_n += 1
        else:
            fail_n += 1
            print(f'  ✗ {cid}: {why}')
    print(f'写入 {ok_n} 门，拒绝 {fail_n} 门')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
