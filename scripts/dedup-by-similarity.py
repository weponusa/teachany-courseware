#!/usr/bin/env python3
"""dedup-by-similarity.py — 按内容相似度去重（不限标题，可跨类型）

背景：课件里常并存两套体系（原课件 card 系列 + 后加的标准模块），同一内容
被讲两遍甚至三遍。例如 math-m-circle-angle：

    学习目标    objectives(59字) 与 card(78字)      —— 标题相同
    圆周角定理  card mod2(519字) / module-1(300字) / lesson-focus(88字)
                —— 标题不同，但讲的都是圆周角定理

此前的去重只比对「标题相同」的模块，捕获不了第二种情况。本脚本直接比对
**正文内容**，不限标题。

判定（保守）：
  - 两模块正文 2-gram Jaccard 相似度 >= 阈值（默认 0.5）
  - 且其中一个字数明显更少（<= 另一个的 0.8 倍）
  → 删除字数少的那个

保留优先级：有 id 的标准模块 > 无 id 模块（同等内容时优先留标准 id），
但若标准模块字数明显更少且内容雷同，仍会被删除（避免留个空壳）。

用法: python3 dedup-by-similarity.py <cid> [cid2 ...] [--dry] [--th 0.5]
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


def process(cid, dry=False, th=0.5):
    P = COMMUNITY / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")
    secs = list(SHELL.sections(html, top_only=True))
    if len(secs) < 2:
        return 0, []

    drop = set()
    info = []
    for i in range(len(secs)):
        if i in drop:
            continue
        for j in range(i + 1, len(secs)):
            if j in drop:
                continue
            a, b = secs[i], secs[j]
            sim = SHELL.similarity(a[3], b[3])
            if sim < th:
                continue
            na, nb = SHELL.text_len(a[3]), SHELL.text_len(b[3])
            if na == 0 or nb == 0:
                continue
            # 字数多的保留
            keep, gone = (a, b) if na >= nb else (b, a)
            nk, ng = max(na, nb), min(na, nb)
            if ng > nk * 0.8:
                continue                      # 篇幅接近，不冒险
            idx_gone = secs.index(gone)
            drop.add(idx_gone)
            sid = (re.search(r'id="([^"]+)"', gone[2]) or [None, "无id"])[1]
            ksid = (re.search(r'id="([^"]+)"', keep[2]) or [None, "无id"])[1]
            info.append(f"删 {sid}({ng}字) 保留 {ksid}({nk}字) 相似度{sim:.2f}")

    if not drop:
        return 0, []
    for idx in sorted(drop, reverse=True):
        s, e = secs[idx][0], secs[idx][1]
        html = html[:s] + html[e:]
    if not dry:
        P.write_text(html, encoding="utf-8")
    return len(drop), info


def main():
    dry = "--dry" in sys.argv
    th = next((float(a.split("=")[1]) for a in sys.argv if a.startswith("--th=")), 0.5)
    cids = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not cids:
        print("用法: python3 dedup-by-similarity.py <cid> [cid2 ...] [--dry] [--th 0.5]")
        return
    tot = 0
    for c in cids:
        try:
            n, info = process(c, dry, th)
            tot += n
            if n:
                print(f"{c}: 删除 {n} 个")
                for x in info:
                    print(f"    {x}")
        except Exception as e:
            print(f"  ❌ {c}: {str(e)[:60]}")
    print(f"合计删除 {tot} 个" + ("（--dry 未写入）" if dry else ""))


if __name__ == "__main__":
    main()
