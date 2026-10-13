#!/usr/bin/env python3
"""drop-dup-sections.py — 删除 id 带 -dupN 后缀的重复 section

扫描发现 526 个 -dupN 后缀的 id，但分布在不同标签上，不能一刀切：

    <button>  352  → 工具栏按钮（tb-autoplay / tb-fullscreen），
                      每个课件 2 个，属正常功能，**不能删**
    <section> 153  → 真正的重复模块副本（hero-infographic-dupN 占 109 个），
                      是生成时重复渲染留下的，**应删**
    <div>      19  → 多为习题容器，保留
    <audio>     2  → 播放器，保留

本脚本只处理 <section>：删除整个 section（用栈匹配闭合位置）。
带 -dupN 后缀本身即表示 duplicate，删除风险可控。

用法: python3 drop-dup-sections.py [cid...] [--dry]
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

DUP = re.compile(r'id="[^"]*-dup\d+"')


def process(cid, dry=False):
    P = COMMUNITY / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")
    drop = []
    for s, e, a, b in SHELL.sections(html, top_only=True):
        if DUP.search(a):
            drop.append((s, e, a))
    if not drop:
        return 0, []
    info = []
    for s, e, a in sorted(drop, reverse=True):
        info.append(re.search(r'id="([^"]+)"', a).group(1))
        html = html[:s] + html[e:]
    if not dry:
        P.write_text(html, encoding="utf-8")
    return len(drop), info


def main():
    dry = "--dry" in sys.argv
    cids = [a for a in sys.argv[1:] if not a.startswith("--")]
    targets = ([COMMUNITY / c / "index.html" for c in cids]
               if cids else sorted(COMMUNITY.glob("*/index.html")))
    tot, files, sample = 0, 0, []
    for p in targets:
        try:
            n, info = process(p.parent.name, dry)
            if n:
                tot += n
                files += 1
                if len(sample) < 5:
                    sample.append((p.parent.name, info))
        except Exception as e:
            print(f"  ❌ {p.parent.name}: {str(e)[:50]}")
    print(f"删除重复 section {tot} 个（涉及 {files} 个课件）"
          + ("（--dry 未写入）" if dry else ""))
    for c, info in sample:
        print(f"  {c}: {', '.join(info)}")


if __name__ == "__main__":
    main()
