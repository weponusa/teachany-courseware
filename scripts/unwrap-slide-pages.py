#!/usr/bin/env python3
"""unwrap-slide-pages.py — 解包 slide-page 分页容器，转为连续网页

全库有 6629 个 slide-page 分页容器（分布 847 个课件），每个内部还嵌套着
若干 section（共 9118 个）。它们配 CSS 使用：

    .slide-container{height:100dvh;overflow-y:auto;scroll-snap-type:y proximity}
    .slide-page{min-height:100dvh;scroll-snap-align:start}

即「一屏一页、滚动吸附」的分页放映形态。用户要求改为连续网页。

本脚本做的是**解包**而非删除：去掉 <section class="slide-page"> 与其配对的
</section>，把内部内容原地留下。这样既变成连续网页，又不会丢任何内容。

    <section class="slide-page">      ← 删掉这对标签，内容保留
      <section class="section">…</section>
    </section>

用法: python3 unwrap-slide-pages.py <cid> [cid2 ...] [--dry] [--all]
"""
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

_spec = importlib.util.spec_from_file_location(
    "shell", ROOT / "scripts" / "apply-courseware-shell.py")
SHELL = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(SHELL)


def unwrap(html):
    """去掉所有顶层 slide-page 的容器标签，返回 (新html, 解包数)"""
    n = 0
    while True:
        found = None
        for s, e, a, b in SHELL.sections(html, top_only=True):
            if "slide-page" in a:
                found = (s, e, a)
                break
        if not found:
            break
        s, e, a = found
        # 开标签：从 s 起的 <section …> 到第一个 '>' 为止。
        # 不能用 len(a)+2 推算——a 只是属性串，漏算了 "<section" 本身。
        gt = html.find(">", s)
        if gt < 0 or html[s:s + 8].lower() != "<section":
            break
        o_end = gt + 1
        close_start = e - len("</section>")
        if html[close_start:e] != "</section>":
            break
        # 先删闭标签再删开标签，避免索引偏移
        html = html[:close_start] + html[e:]
        html = html[:s] + html[o_end:]
        n += 1
        if n > 400:          # 安全阀
            break
    return html, n


def process(cid, dry=False):
    P = COMMUNITY / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")
    new, n = unwrap(html)
    if not n or new == html:
        return 0
    if not dry:
        P.write_text(new, encoding="utf-8")
    return n


def main():
    dry = "--dry" in sys.argv
    cids = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--all" in sys.argv or not cids:
        cids = sorted(p.name for p in COMMUNITY.iterdir() if (p / "index.html").exists())
    tot, files = 0, 0
    for c in cids:
        try:
            n = process(c, dry)
            if n:
                tot += n
                files += 1
                print(f"  {c}: 解包 {n}")
        except Exception as e:
            print(f"  ❌ {c}: {str(e)[:60]}")
    print(f"解包 slide-page {tot} 个（涉及 {files} 个课件）"
          + ("（--dry 未写入）" if dry else ""))


if __name__ == "__main__":
    main()
