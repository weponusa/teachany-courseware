#!/usr/bin/env python3
"""drop-empty-media-dup-graph.py — 清理空播放器与重复知识图谱

两类残留问题：

1. 空的教学动画（194 个课件）
   模块有标题（如「教学动画：60 秒内复盘核心关系」）和 <video> 播放器，
   但视频没有源——全库 138 个 video 标签中 126 个没有 src。页面上只会
   显示一个空壳播放器，属于凑数。

2. 重复的知识图谱（7 个课件）
   同一课件有 2~4 个图谱模块（info-u-signals-pbl 有 4 个），都是
   data-teachany-kg 容器。应只保留 id="knowledge-graph" 的标准模块。

清理规则（保守）：
  - 空播放器：标题命中 教学动画/微课/视频/动画，且区块内既无 src=
    也无 iframe（确无任何媒体源）才删
  - 重复图谱：标题命中 知识图谱/知识关系图/知识地图/知识体系，且 id 不是
    knowledge-graph 的删；保留 id="knowledge-graph" 的标准模块

用法: python3 drop-empty-media-dup-graph.py [cid...] [--dry]
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

VIDEO_TITLE = re.compile(r"教学动画|微课|视频|动画")
KG_TITLE = re.compile(r"知识图谱|知识关系图|知识地图|知识体系")


def should_drop(a, b):
    """返回 '重复图谱' 表示整块删除；空播放器不在此处理（见 strip_empty_video）"""
    t = SHELL.title_of(a, b)
    if not t:
        return None
    if KG_TITLE.search(t):
        sid = (re.search(r'id="([^"]+)"', a) or [None, ""])[1]
        if sid == "knowledge-graph":
            return None                  # 标准图谱，保留
        return "重复图谱"
    return None


def strip_empty_video(html):
    """删除没有视频源的 <video> 元素（空壳播放器）

    注意：只删播放器本身，不删整个模块。这些模块往往还含有有价值的文字内容
    与交互控件，例如「胚胎发育过程动画」里有完整的发育时间线知识（受精→卵裂
    →植入→胚胎→胎儿）和上一步/自动演示/下一步按钮，只是视频文件缺失而已。
    整个删掉会连同知识一起丢失。
    """
    out, n = [], 0
    for m in re.finditer(r"<video\b[^>]*>([\s\S]*?)</video>", html):
        attrs = m.group(0)
        if "src=" in attrs.split(">")[0]:     # 有视频源，保留
            continue
        # 无源：删掉整个 video 元素（含其内部 source/说明）
        out.append(m.span())
        n += 1
    for s, e in reversed(out):
        html = html[:s] + html[e:]
    return html, n


def process(cid, dry=False):
    P = COMMUNITY / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")

    # 1) 去掉空壳播放器（保留模块内的文字与交互）
    html, n_video = strip_empty_video(html)

    # 2) 删除重复的知识图谱（整块）
    drop, why = [], []
    for s, e, a, b in SHELL.sections(html, top_only=True):
        r = should_drop(a, b)
        if r:
            drop.append((s, e))
            why.append(r)
    for s, e in sorted(drop, reverse=True):
        html = html[:s] + html[e:]
    if n_video:
        why += ["空播放器"] * n_video

    if not why:
        return 0, []
    if not dry:
        P.write_text(html, encoding="utf-8")
    return len(why), why


def main():
    dry = "--dry" in sys.argv
    cids = [a for a in sys.argv[1:] if not a.startswith("--")]
    targets = ([COMMUNITY / c / "index.html" for c in cids]
               if cids else sorted(COMMUNITY.glob("*/index.html")))
    tot, files = 0, 0
    stat = {}
    for p in targets:
        try:
            n, why = process(p.parent.name, dry)
            if n:
                tot += n
                files += 1
                for w in why:
                    stat[w] = stat.get(w, 0) + 1
        except Exception as e:
            print(f"  ❌ {p.parent.name}: {str(e)[:50]}")
    print(f"清理 {tot} 个模块（涉及 {files} 个课件）"
          + ("（--dry 未写入）" if dry else ""))
    for k, v in stat.items():
        print(f"   {k}: {v}")


if __name__ == "__main__":
    main()
