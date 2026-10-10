#!/usr/bin/env python3
"""add-slide-shell.py — 给「页面已分好、只缺 v2 外壳控件」的课件补齐外壳。

背景
----
v2 分页判定（audit-quality.py）：html 含 'slide-page' 且含 'sidenav'。
2026-10-10 盘点：NOT_V2_PAGED 431 门中，有一批课件**已经有**
`<div class="slide-container">` + 若干 `class="slide-page"` 分页节，
但缺两类东西，导致播放/翻页功能整体不可用：

  1. 共享资产：assets/teachany-slide-v2.css + teachany-slide-v2.js
  2. 控件四件：slide-progress-bar / slide-sidenav / play-mode-fab / slide-toolbar

本脚本只注入这两类，**不重排页面、不改内容**。页面分页数不足 6 的
（需重排/重写档）不属于本脚本职责，跑了也不会碰。

注入方式与 scripts/upgrade_recent_courseware_slide_quality.py 的
add_slide_assets() / ensure_slide_controls() 完全一致（同一套模板），
已上线课件 phy-m-heat-calculation / psych-m-g8-role-identity 即此写法。

用法
----
  python3 scripts/add-slide-shell.py --pilot 2            # 预览（默认 dry-run）
  python3 scripts/add-slide-shell.py --pilot 2 --apply
  python3 scripts/add-slide-shell.py --ids a,b --apply
  python3 scripts/add-slide-shell.py --from-file f.txt --apply
  python3 scripts/add-slide-shell.py --all --apply        # 自动筛出全部缺外壳课件
  python3 scripts/add-slide-shell.py --all --revert       # 回滚本脚本注入的部分

幂等：四件控件齐全且资产已引 → 跳过。
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

CSS_LINK = '<link rel="stylesheet" href="../../assets/teachany-slide-v2.css">'
JS_TAG = '<script defer src="../../assets/teachany-slide-v2.js"></script>'

CONTROL_IDS = ('id="slide-progress-bar"', 'id="slide-sidenav"',
               'id="play-mode-fab"', 'id="slide-toolbar"')

CONTROLS = '''<div class="slide-progress-bar" id="slide-progress-bar"></div>
<nav class="slide-sidenav" id="slide-sidenav" aria-label="分页导航"></nav>
<button aria-label="切换播放模式" class="play-mode-fab" id="play-mode-fab" title="播放模式 (F)">
  <svg id="fab-icon-play" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"></path></svg>
  <svg id="fab-icon-browse" style="display:none" viewBox="0 0 24 24"><path d="M4 6h16v2H4zM4 11h16v2H4zM4 16h16v2H4z"></path></svg>
</button>
<div class="slide-toolbar" id="slide-toolbar">
  <button class="toolbar-btn" id="tb-prev" type="button" aria-label="上一页">‹</button>
  <div class="toolbar-page-info" id="tb-page-info">1 / 1</div>
  <button class="toolbar-btn" id="tb-next" type="button" aria-label="下一页">›</button>
  <div class="toolbar-progress" id="tb-progress"><div class="toolbar-progress-fill" id="tb-progress-fill"></div></div>
  <button class="toolbar-btn" id="tb-autoplay" type="button" aria-label="自动播放">Auto</button>
  <button class="toolbar-btn" id="tb-fullscreen" type="button" aria-label="全屏">⛶</button>
</div>
'''

INJECT_TAG = 'data-injected="slide-shell"'
CONTAINER_RE = re.compile(r'<div[^>]*id="slide-container"[^>]*>')
# 与盘点脚本口径一致：class 可以是 "slide-page" 也可以是 "slide-page xxx"
PAGE_RE = re.compile(r'class="[^"]*slide-page', re.I)


def is_target(html: str) -> bool:
    """只碰「页面已分好、但 v2 判定未通过（缺控件）」的课件。

    注意：不能只看「缺外部 css/js 资产」。2026-10-10 实测，库里有 237 门
    （chem-m-* / chn-h-* / eng-h-* 等）v2 判定已通过、但没引共享资产 ——
    它们带一整套**内联** slide 样式与脚本（10 个 script 块那种）。给它们
    注入 teachany-slide-v2.css/js 只会两套样式打架。所以目标必须以
    「缺 sidenav（= v2 判定未通过）」为准，缺资产本身不构成注入理由。
    """
    if 'id="slide-container"' not in html:
        return False                      # 没容器 → 属重排/重写档，不归本脚本
    if len(PAGE_RE.findall(html)) < 6:
        return False                      # 分页不足 → 同上
    if 'slide-sidenav' in html:
        return False    # 审计判定已含 sidenav（多为内联实现或已接共享资产）→ 不碰
    return True


def inject(html: str) -> str:
    # 1) 控件四件：插在 slide-container 之前
    if not all(x in html for x in CONTROL_IDS):
        m = CONTAINER_RE.search(html)
        if m:
            html = html[:m.start()] + CONTROLS + '\n' + html[m.start():]

    # 2) 资产：css 进 </head>，js 进 </body>
    if "teachany-slide-v2.css" not in html:
        i = html.rfind("</head>")
        if i >= 0:
            html = html[:i] + CSS_LINK + "\n" + html[i:]
    if "teachany-slide-v2.js" not in html:
        i = html.rfind("</body>")
        if i >= 0:
            html = html[:i] + JS_TAG + "\n" + html[i:]

    # 3) 标记（供 --revert 识别）
    if INJECT_TAG not in html:
        html = html.replace("</head>", f'<!-- {INJECT_TAG} -->\n</head>', 1)
    return html


def revert(html: str) -> str:
    html = re.sub(r'[ \t]*<link rel="stylesheet" href="\.\./\.\./assets/teachany-slide-v2\.css">[ \t]*\n?', '', html)
    html = re.sub(r'[ \t]*<script defer src="\.\./\.\./assets/teachany-slide-v2\.js"></script>[ \t]*\n?', '', html)
    html = re.sub(r'<!-- data-injected="slide-shell" -->[ \t]*\n?', '', html)
    # 只删本脚本注入的完整控件块（从 progress-bar 到 toolbar 结尾）
    html = re.sub(
        r'<div class="slide-progress-bar" id="slide-progress-bar"></div>\s*'
        r'<nav class="slide-sidenav"[\s\S]*?</div>\s*</div>\s*\n?',
        '', html, count=1)
    return html


def load_targets(a):
    if a.ids:
        dirs = [COMMUNITY / x.strip() for x in a.ids.split(",") if x.strip()]
    elif a.from_file:
        dirs = [COMMUNITY / l.strip() for l in Path(a.from_file).read_text().splitlines()
                if l.strip() and not l.startswith("#")]
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
            # 只回滚本脚本注入的：标记在、且控件仍在（避免误删历史自带的）
            if INJECT_TAG in h:
                out.append(p)
        else:
            if is_target(h):
                out.append(p)
    return out[: a.pilot] if a.pilot else out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", type=int, default=0)
    ap.add_argument("--ids")
    ap.add_argument("--from-file")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--revert", action="store_true")
    a = ap.parse_args()

    if not any([a.pilot, a.ids, a.from_file, a.all]):
        ap.error("需指定 --pilot / --ids / --from-file / --all 之一")

    targets = load_targets(a)
    mode = "回滚" if a.revert else ("写入" if a.apply else "预览")
    print(f"目标 {len(targets)} 门 · {mode}", flush=True)
    ok = 0
    for p in targets:
        f = p / "index.html"
        h = f.read_text(encoding="utf-8", errors="ignore")
        new = revert(h) if a.revert else inject(h)
        if new == h:
            print(f"  - {p.name}: 无变化")
            continue
        if a.apply or a.revert:
            f.write_text(new, encoding="utf-8")
            ok += 1
        pages = len(PAGE_RE.findall(new))
        v2 = ("slide-page" in new and "sidenav" in new)
        print(f"  {'✓' if a.apply or a.revert else '○'} {p.name}: pages={pages} v2判定={v2}")
    print(f"\n完成：{mode} {ok} / {len(targets)}")


if __name__ == "__main__":
    main()
