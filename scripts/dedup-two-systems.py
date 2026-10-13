#!/usr/bin/env python3
"""dedup-two-systems.py — 两套体系并存课件：保留内容更完整的一套

全库扫描发现仅 40 个课件存在「两套完整体系并存」：

  A 套（原课件正文）class 以 card 开头：card / card mod2 / card success…
  B 套（标准补丁）  class 含 teachany-upgrade-block / mathm-depth，或标准 id
                    （anchor/objectives/pretest/posttest/lesson-focus/…）

同一内容讲两遍，此前字符相似度去重无法捕获（用词差异太大，相似度仅 0.06~0.17）。

处理规则：
  1. B 套字数更多 → 删 A 套（card 系列是残留）
  2. A 套字数更多 → 删 B 套，但保留 B 中的 pretest / posttest——
     A 套 card 系列通常只有正文没有测验，删掉会让课件失去前后测

共用功能模块（knowledge-graph / phet-lab / hero-infographic /
teachany-ai-tutor-card / teachany-audio-player 等）不参与两套之争，一律保留。

用法: python3 dedup-two-systems.py [--dry] [cid...]
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

B_MARK = re.compile(r"teachany-upgrade-block|mathm-depth|core-knowledge-module")
STD = {"anchor", "objectives", "pretest", "posttest", "lesson-focus", "lesson-method",
       "deep-understanding", "error-clinic", "error-watch", "memory-anchor",
       "course-nav-map", "summary", "worked-example"}
SHARED = re.compile(
    r'id="(knowledge-graph|phet-lab|hero-infographic|teachany-ai-tutor-card|'
    r'teachany-audio-player|external-lab|interactive-model|video-demo|micro-video)"')


def classify(a):
    cls = (re.search(r'class="([^"]*)"', a) or [None, ""])[1]
    sid = (re.search(r'id="([^"]+)"', a) or [None, ""])[1]
    if SHARED.search(sid or ""):
        return "shared"
    if re.match(r"card", cls):
        return "A"
    if B_MARK.search(cls) or sid in STD:
        return "B"
    return "other"


def process(cid, dry=False):
    P = COMMUNITY / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")
    secs = list(SHELL.sections(html, top_only=True))
    A = [(i, x) for i, x in enumerate(secs) if classify(x[2]) == "A"]
    B = [(i, x) for i, x in enumerate(secs) if classify(x[2]) == "B"]
    if not A or not B:
        return None
    aw = sum(SHELL.text_len(x[3]) for _, x in A)
    bw = sum(SHELL.text_len(x[3]) for _, x in B)

    drop = []
    if bw > aw:
        # B 更完整 → 删 A 套
        drop = [i for i, _ in A]
        act = f"删A套({aw}字)，保留B套({bw}字)"
    else:
        # A 更完整 → 删 B 套，但保留 pretest/posttest
        for i, x in B:
            sid = (re.search(r'id="([^"]+)"', x[2]) or [None, ""])[1]
            if sid in ("pretest", "posttest"):
                continue
            drop.append(i)
        keep = bw - sum(SHELL.text_len(secs[i][3]) for i in drop)
        act = f"删B套({bw-keep}字)，保留A套({aw}字)+B套测验({keep}字)"

    if not drop:
        return None
    for i in sorted(drop, reverse=True):
        s, e = secs[i][0], secs[i][1]
        html = html[:s] + html[e:]
    if not dry:
        P.write_text(html, encoding="utf-8")
    return act


def main():
    dry = "--dry" in sys.argv
    cids = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not cids:
        cids = sorted(p.name for p in COMMUNITY.iterdir() if (p / "index.html").exists())
    n = 0
    for c in cids:
        try:
            r = process(c, dry)
            if r:
                n += 1
                print(f"  {c}: {r}")
        except Exception as e:
            print(f"  ❌ {c}: {str(e)[:60]}")
    print(f"处理 {n} 个课件" + ("（--dry 未写入）" if dry else ""))


if __name__ == "__main__":
    main()
