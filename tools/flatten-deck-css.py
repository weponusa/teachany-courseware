#!/usr/bin/env python3
"""给 v7.22.0 世代课件（未加载 courseware-shell.css）注入 deck 拍平样式。

背景：焦耳定律等页面原本是「100dvh 锁视口 + 容器内滚动 + 侧边导航 + 进度条 +
播放按钮」的整套 deck，用户反馈出现"嵌套"观感。全站 945 门通过
assets/scripts/courseware-shell.css 统一拍平，但仍有 96 门 v7.22.0 页面
（it-*/pol-*/psych-*/sci-e-* 等）根本没加载该 CSS，成为漏网批次。

本脚本给这些页面注入与焦耳定律同款的 <style id="ta-deck-flattened">，
把容器恢复文档流、隐藏放映 UI。纯 CSS 注入，不动 DOM 结构。

用法：
  python3 tools/flatten-deck-css.py --cids it-e-ai-awareness pol-e-g1-u1
  python3 tools/flatten-deck-css.py --all          # 自动扫描漏网批次
  python3 tools/flatten-deck-css.py --all --dry-run
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMM = ROOT / "community"

MARK = 'id="ta-deck-flattened"'

FLATTEN_CSS = """<style id="ta-deck-flattened">
/* deck 已拍平：恢复文档流，去掉内部滚动与 snap */
.slide-container, div[id="slide-container"] { height: auto !important; max-height: none !important; overflow: visible !important; scroll-snap-type: none !important; }
.slide-page, section.slide-page, div.slide-page { min-height: 0 !important; height: auto !important; scroll-snap-align: none !important; scroll-margin-top: 76px; }
html, body { height: auto !important; max-height: none !important; overflow: visible !important; scroll-snap-type: none !important; }
body.play-mode .slide-container { overflow: visible !important; }
.slide-progress-bar, #slide-progress-bar, .slide-sidenav, #slide-sidenav,
.slide-sidenav-toggle, .play-mode-fab, .slide-toolbar, .deck-toolbar { display: none !important; }
</style>
"""


def scan_targets() -> list[str]:
    """扫出「有 slide-container 且未加载 courseware-shell.css」的 cid。"""
    hits = []
    for d in sorted(COMM.iterdir()):
        f = d / "index.html"
        if not f.is_file():
            continue
        try:
            h = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if 'class="slide-container"' not in h:
            continue
        if "courseware-shell.css" in h:
            continue
        hits.append(d.name)
    return hits


def inject(cid: str, dry: bool = False) -> str:
    f = COMM / cid / "index.html"
    if not f.is_file():
        return "missing"
    h = f.read_text(encoding="utf-8", errors="replace")
    if MARK in h:
        return "skip-already"
    if "</head>" not in h:
        return "skip-no-head"
    out = h.replace("</head>", FLATTEN_CSS + "</head>", 1)
    if out == h:
        return "skip-nochange"
    if not dry:
        f.write_text(out, encoding="utf-8")
    return "done"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cids", nargs="*", default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    if args.all:
        cids = scan_targets()
    elif args.cids:
        cids = args.cids
    else:
        ap.error("需要 --cids 或 --all")

    if args.limit:
        cids = cids[: args.limit]

    tally: dict[str, list[str]] = {}
    for cid in cids:
        r = inject(cid, dry=args.dry_run)
        tally.setdefault(r, []).append(cid)
        if r != "done" and r != "skip-already":
            print(f"  ⚠ {cid}: {r}", file=sys.stderr)

    print(f"目标 {len(cids)} 门  (dry_run={args.dry_run})")
    for k in sorted(tally):
        print(f"  {k:16s} {len(tally[k])}")
        if k.startswith("skip-") and k != "skip-already":
            for cid in tally[k][:10]:
                print(f"      - {cid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
