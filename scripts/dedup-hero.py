#!/usr/bin/env python3
"""dedup-hero.py — 每个课件只保留一个开场（hero）模块

同一课件里常有两个甚至三个开场信息图，例如 bio-classification：

    hero-cover(94字)  生物分类 — 八年级生物互动课件 + 知识结构主图
    hero(63字)        🦁 生物分类 + 界门纲目科属种 + 学段/时长/课型

两者都是「课程标题 + 元信息」的开场页，重复展示。

保留规则（按优先级）：
  1. 优先保留 id 为 hero-infographic 的（注册表里的标准 id）
  2. 都没有则保留内容最完整的（字数最多）
删除其余顶层 hero 模块。

安全约束：
  - 只处理顶层 section，不动嵌套的
  - 只删 id 含 hero 的模块，其余一律不动
  - 至少保留一个（若只剩一个则不删）

用法: python3 dedup-hero.py [cid...] [--dry]
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

HERO = re.compile(r'id="[^"]*hero[^"]*"', re.I)
STD_HERO = re.compile(r'id="hero-infographic"')


def process(cid, dry=False):
    P = COMMUNITY / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")
    heroes = [(s, e, a, b) for s, e, a, b in SHELL.sections(html, top_only=True)
              if HERO.search(a)]
    if len(heroes) < 2:
        return 0, []

    std = [x for x in heroes if STD_HERO.search(x[2])]
    keep = std[0] if std else max(heroes, key=lambda x: SHELL.text_len(x[3]))
    drop = [x for x in heroes if x is not keep]
    if not drop:
        return 0, []

    info = [re.search(r'id="([^"]+)"', x[2]).group(1) for x in drop]
    for s, e, a, b in sorted(drop, reverse=True):
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
                if len(sample) < 6:
                    sample.append((p.parent.name, info))
        except Exception as e:
            print(f"  ❌ {p.parent.name}: {str(e)[:50]}")
    print(f"删除重复开场 {tot} 个（涉及 {files} 个课件）"
          + ("（--dry 未写入）" if dry else ""))
    for c, info in sample:
        print(f"  {c}: 删 {', '.join(info)}")


if __name__ == "__main__":
    main()
