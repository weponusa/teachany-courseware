#!/usr/bin/env python3
"""drop-patch-blocks.py — 清理「补丁式」追加的重复小模块

现象：不少课件在原有完整结构之后，被追加了一串无 id 的小模块，例如
bio-circulation 的正文之后多了 7 个：

    课前诊断(56字) / 达标检测(60字) / 错因诊断(78字) / 迁移挑战(58字)
    真题练习(268字) / 概念检测(63字) / 运动对脉搏(49字)

它们带有 class="teachany-upgrade-block"，是后期统一追加的补丁块，
功能与课件原有的标准模块重复：前面已有 pretest(662字) 又加「课前诊断」，
后面已有 posttest(798字) 又加「达标检测」。堆叠在页面后段，观感杂乱。

清理规则（保守，逐条确认）：
  1. 无 id 的顶层 section（标准模块都有 id）
  2. 纯文本 < 300 字（真内容模块远多于此）
  3. 标题命中「检测/诊断/达标/前测/后测/易错/错因」等重复语义
  4. 不含 iframe / canvas / video / audio / img（有媒体的保留）
  5. 不是 display:none 的功能容器

只删同时满足以上条件的模块；其余一律保留并计入报告。

用法: python3 drop-patch-blocks.py [--dry]
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

# 与已有标准模块功能重复的语义词
REPEAT = re.compile(
    r"课前诊断|达标检测|概念检测|错因诊断|易错诊断|前测|后测|"
    r"诊断|检测|自评|随堂|闯关|挑战|评估")

MEDIA = re.compile(r"<iframe|<canvas|<video|<audio|<img\b")


def is_patch(a, b):
    """判断是否为可清理的补丁块"""
    sid = re.search(r'id="([^"]+)"', a)
    if sid:                                   # 有 id 的标准模块，不动
        return False
    if SHELL.text_len(b) >= 300:              # 内容够多，视为真模块
        return False
    if MEDIA.search(b):                       # 含媒体，保留
        return False
    if "display:none" in b[:400]:             # 功能容器，保留
        return False
    t = SHELL.title_of(a, b)
    if not t:
        return False
    return bool(REPEAT.search(t))


def process(cid, dry=False):
    P = COMMUNITY / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")
    secs = SHELL.sections(html, top_only=True)
    drop = [(s, e, a, b) for s, e, a, b in secs if is_patch(a, b)]
    if not drop:
        return 0, []
    info = [(SHELL.title_of(a, b), SHELL.text_len(b)) for _, _, a, b in drop]
    for s, e, a, b in sorted(drop, reverse=True):
        html = html[:s] + html[e:]
    if not dry:
        P.write_text(html, encoding="utf-8")
    return len(drop), info


def main():
    dry = "--dry" in sys.argv
    cids = [a for a in sys.argv[1:] if not a.startswith("--")]
    tot, files = 0, 0
    sample = []
    targets = ([COMMUNITY / c / "index.html" for c in cids]
               if cids else sorted(COMMUNITY.glob("*/index.html")))
    for p in targets:
        try:
            n, info = process(p.parent.name, dry)
            if n:
                tot += n
                files += 1
                if len(sample) < 6:
                    sample.append((p.parent.name, info))
        except Exception as e:
            print(f"  ❌ {p.parent.name}: {str(e)[:50]}")
    print(f"清理补丁块 {tot} 个（涉及 {files} 个课件）"
          + ("（--dry 未写入）" if dry else ""))
    for c, info in sample:
        print(f"  {c}: " + ", ".join(f"{t}({n}字)" for t, n in info))


if __name__ == "__main__":
    main()
