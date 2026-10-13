#!/usr/bin/env python3
"""drop-jargon-modules.py — 清理模板化无意义模块

问题：一批课件里存在一个套话版「达标检测」section（id="post-test"，注意与
真实的 id="posttest" 不同）：

    关于「X」的学习，哪种做法最科学？
      A. 理解课标概念，掌握方法，在情境中练习并反思   ← 正确项
      B. 只背答案，不做分析
      C. 忽略课标，凭感觉答题

这是问「学习方法」的元认知题，与学科内容无关，且三个选项是把课件名填进
固定句式的产物，对学习没有任何检测价值。

经核查：受影响的 154 个课件中，153 个**已有**真实的 id="posttest" 达标检测
（含具体题目与诊断），该套话 section 属纯冗余 → 直接删除。
仅 hist-m-opium-war 只有套话版，另行补真实题目，不在此删除。

同时清理学习目标里的三条套话（把课件名填进固定句式）：
    能运用所学方法分析「X」相关典型问题
    能在情境中正确应用「X」的知识与技能
    能识别并纠正关于「X」的常见误区

用法: python3 drop-jargon-modules.py [cid...]
      python3 drop-jargon-modules.py --all
      python3 drop-jargon-modules.py --dry
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

# 套话版达标检测的特征（须全部命中才判定为可删）
JARGON_MARKS = [
    r"理解课标概念，掌握方法，在情境中练习并反思",
    r"忽略课标，凭感觉答题",
]

# 学习目标三条套话
OBJ_JARGON = [
    r"能运用所学方法分析[^<]{0,24}相关典型问题",
    r"能在情境中正确应用[^<]{0,24}的知识与技能",
    r"能识别并纠正关于[^<]{0,24}的常见误区",
]

# 不删除：只有套话版达标检测的课件，需先补真实题目
KEEP = {"hist-m-opium-war"}


def find_section_end(html, start):
    """从 start 处的 <section ...> 起，用栈找到配对的 </section> 后界"""
    depth = 0
    pos = start
    for m in re.finditer(r"<section\b|</section>", html[start:]):
        if m.group(0) == "</section>":
            depth -= 1
            if depth == 0:
                return start + m.end()
        else:
            depth += 1
        pos = start + m.end()
    return -1


def process(cid, dry=False):
    P = COMMUNITY / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")
    orig = html
    acts = []

    # 1) 删除套话版达标检测 section
    if cid not in KEEP:
        m = re.search(r'<section\b[^>]*\bid="post-test"[^>]*>', html)
        if m and all(re.search(k, html) for k in JARGON_MARKS):
            end = find_section_end(html, m.start())
            if end > 0:
                seg = html[m.start():end]
                # 二次确认：该区块确实在讲「哪种做法最科学」这类元认知题
                if re.search(r"哪种做法最科学", seg):
                    html = html[:m.start()] + html[end:]
                    acts.append("删套话达标检测section")

    # 2) 清理学习目标套话条目（整条 <li>，连同其后的换行，避免留空行）
    n_li = 0
    for pat in OBJ_JARGON:
        new, k = re.subn(r"[ \t]*<li[^>]*>[ \t]*" + pat + r"[ \t]*</li>\r?\n?", "", html)
        if k:
            html = new
            n_li += k
    if n_li:
        acts.append(f"删套话学习目标{n_li}条")

    if not acts or html == orig:
        return 0
    if not dry:
        P.write_text(html, encoding="utf-8")
    return len(acts)


def main():
    dry = "--dry" in sys.argv
    cids = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--all" in sys.argv or not cids:
        cids = sorted(p.name for p in COMMUNITY.iterdir() if (p / "index.html").exists())
    n = 0
    for c in cids:
        try:
            k = process(c, dry)
            n += bool(k)
        except Exception as e:
            print(f"  ❌ {c}: {str(e)[:60]}")
    print(f"清理 {n} 个课件" + ("（--dry 未写入）" if dry else ""))


if __name__ == "__main__":
    main()
