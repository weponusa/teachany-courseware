#!/usr/bin/env python3
"""hide-slide-ui.py — 全库隐藏「分页播放」控件，保留静默页面结构。

背景（2026-10-10 用户决定）：分页播放只是呈现形式，不作为质量门槛，课件界面
上也不再出现这套控件。审计已同步去掉 NOT_V2_PAGED / PAGE_COUNT_OFF 两条
硬性要求（见 audit-quality.py score_rows 注释）。

做法：给含播放 UI 的课件在 </head> 前注入一条隐藏规则，把播放按钮
（play-mode-fab）、工具条（slide-toolbar）、侧导航（slide-sidenav）、进度条
（slide-progress-bar）全部 display:none。slide-page 分页结构与滚动吸附保留
——浏览体验不变，只是不再有「播放模式」这层 UI。

只隐藏、不删除：可一键回滚（--revert 按 CSS 标记识别），也不动各课件的
JS——UI 不可见后，键盘 F 这个隐藏入口对普通用户无感。

用法：
  python3 scripts/hide-slide-ui.py --pilot 2            # 预览
  python3 scripts/hide-slide-ui.py --pilot 2 --apply
  python3 scripts/hide-slide-ui.py --all --apply
  python3 scripts/hide-slide-ui.py --all --revert
幂等：已带标记的课件跳过。
"""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

MARK = 'data-injected-css="hide-slide-ui"'
# 任一控件出现（DOM/JS/CSS 字符串）即视为「有播放 UI」
UI_MARKERS = ('slide-sidenav', 'play-mode-fab', 'slide-toolbar', 'slide-progress-bar')

HIDE_CSS = (
    '<style ' + MARK + '>\n'
    '/* 分页播放控件已按 2026-10-10 决定下线：只保留分页滚动结构，不显示播放 UI */\n'
    '.play-mode-fab,.slide-toolbar,.slide-sidenav,.slide-progress-bar,'
    '#play-mode-fab,#slide-toolbar,#slide-sidenav,#slide-progress-bar'
    '{display:none!important}\n'
    '</style>\n'
)


def has_ui(h: str) -> bool:
    return any(m in h for m in UI_MARKERS)


def load_targets(a):
    if a.ids:
        dirs = [COMMUNITY / x.strip() for x in a.ids.split(",") if x.strip()]
    else:
        dirs = sorted(p for p in COMMUNITY.iterdir()
                      if p.is_dir() and (p / "index.html").is_file())
    out = []
    for p in dirs:
        f = p / "index.html"
        if not f.is_file():
            continue
        h = f.read_text(encoding="utf-8", errors="ignore")
        if a.revert:
            if MARK in h:
                out.append(p)
        else:
            if MARK in h:
                continue            # 幂等
            if has_ui(h):
                out.append(p)
    return out[: a.pilot] if a.pilot else out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", type=int, default=0)
    ap.add_argument("--ids")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--revert", action="store_true")
    a = ap.parse_args()
    if not any([a.pilot, a.ids, a.all]):
        ap.error("需指定 --pilot / --ids / --all 之一")

    targets = load_targets(a)
    mode = "回滚" if a.revert else ("写入" if a.apply else "预览")
    print(f"目标 {len(targets)} 门 · {mode}", flush=True)
    ok = 0
    for p in targets:
        f = p / "index.html"
        h = f.read_text(encoding="utf-8", errors="ignore")
        if a.revert:
            new = h.replace(HIDE_CSS, "")
        else:
            i = h.rfind("</head>")
            new = h if i < 0 else h[:i] + HIDE_CSS + h[i:]
        if new == h:
            continue
        if a.apply or a.revert:
            f.write_text(new, encoding="utf-8")
            ok += 1
        print(f"  {'✓' if a.apply or a.revert else '○'} {p.name}")
    print(f"\n完成：{mode} {ok} / {len(targets)}")


if __name__ == "__main__":
    main()
