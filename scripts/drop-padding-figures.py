#!/usr/bin/env python3
"""drop-padding-figures.py — 删除模板拼装的凑数示意图

背景：此前为补齐示意图，用 fig_templates 从课件正文抽取知识点自动生成
SVG。但实际抽到的常常是**页面的模块名**，例如 ancient-china-h：

    要点梳理      → 1.管理机构 / 2.前测 / 3.核心概念结构 / 4.历史分析流程 / 5.后测
    知识结构体系  → 管理机构 / 前测 / 核心概念结构 / 历史分析流程 / 后测 / 微课视频 / 语音导学

「前测」「后测」「微课视频」「语音导学」「即练」都是功能模块名，不是知识点。
据此生成的图看似有内容，实则毫无教学价值，属于凑数。

本脚本删除 figcaption 命中下列模板图题的 figure：
    知识结构体系 / 要点梳理 / 对比辨析 / 组成结构 / 方法步骤 /
    循环过程示意 / 关键环节闭环

只删 <figure class="ta-standard-figure">，其它 figure 一律保留。

用法: python3 drop-padding-figures.py [cid...] [--dry]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

TITLES = ("知识结构体系", "要点梳理", "对比辨析", "组成结构", "方法步骤",
          "循环过程示意", "关键环节闭环")
PAT = re.compile(r"(" + "|".join(re.escape(t) for t in TITLES) + r")")

FIG = re.compile(r'<figure class="ta-standard-figure">[\s\S]*?</figure>')


def process(cid, dry=False):
    P = COMMUNITY / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")
    keep = []
    dropped = 0
    for m in FIG.finditer(html):
        seg = m.group(0)
        cap = re.search(r"<figcaption>([\s\S]*?)</figcaption>", seg)
        if cap and PAT.search(cap.group(1)):
            dropped += 1
        else:
            keep.append(seg)
    if not dropped:
        return 0
    # 用保留下来的片段重建，避免正则删除时误伤嵌套内容
    blocks = []
    last = 0
    for m in FIG.finditer(html):
        seg = m.group(0)
        cap = re.search(r"<figcaption>([\s\S]*?)</figcaption>", seg)
        if cap and PAT.search(cap.group(1)):
            blocks.append(html[last:m.start()])
            last = m.end()
    blocks.append(html[last:])
    new = "".join(blocks)
    if not dry:
        P.write_text(new, encoding="utf-8")
    return dropped


def main():
    dry = "--dry" in sys.argv
    cids = [a for a in sys.argv[1:] if not a.startswith("--")]
    targets = ([COMMUNITY / c / "index.html" for c in cids]
               if cids else sorted(COMMUNITY.glob("*/index.html")))
    tot, files = 0, 0
    for p in targets:
        try:
            n = process(p.parent.name, dry)
            if n:
                tot += n
                files += 1
        except Exception as e:
            print(f"  ❌ {p.parent.name}: {str(e)[:50]}")
    print(f"删除凑数示意图 {tot} 张（涉及 {files} 个课件）"
          + ("（--dry 未写入）" if dry else ""))


if __name__ == "__main__":
    main()
