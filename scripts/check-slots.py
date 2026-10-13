#!/usr/bin/env python3
"""check-slots.py — 槽位校验器（顺序约束 + 唯一性约束）

规则（对打了 data-slot 的顶层模块）：
  R1 hero（slot 0）必须是第一个打标模块
  R2 knowledge-graph（slot 140）必须是最后一个打标模块
  R3 slot 序列非降序（乱序即报）
  R4 uniq 槽位在同一课件内不得重复
  R5 同一 id 不得重复

用法:
  python3 check-slots.py [cid...]          校验（无参数则全库）
  python3 check-slots.py --summary         只出汇总
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

_spec2 = importlib.util.spec_from_file_location(
    "slots", ROOT / "scripts" / "module-slots.py")
SLOTS = importlib.util.module_from_spec(_spec2)
_spec2.loader.exec_module(SLOTS)


def check(html):
    """返回违规列表 [(规则, 描述)]"""
    issues = []
    marked = []   # (slot, sid, title)
    for s, e, a, b in SHELL.sections(html, top_only=True):
        m = re.search(r'data-slot="(\d+)"', a)
        if not m:
            continue
        sid = (re.search(r'id="([^"]+)"', a) or [None, ""])[1]
        marked.append((int(m.group(1)), sid, (SHELL.title_of(a, b) or "")[:14]))

    if not marked:
        return issues

    slots = [m[0] for m in marked]

    # R1/R2 存在性约束：hero/图谱若存在必须在首/末；不存在不算违规
    # （全库约 390 课件无 hero、120 课件无图谱，属正常裁剪）
    if SLOTS.FIRST_SLOT in slots and slots[0] != SLOTS.FIRST_SLOT:
        issues.append(("R1", f"hero 存在但首个打标模块 slot={slots[0]}"))
    if SLOTS.LAST_SLOT in slots and slots[-1] != SLOTS.LAST_SLOT:
        issues.append(("R2", f"图谱存在但末尾打标模块 slot={slots[-1]}"))
    for i in range(1, len(slots)):
        if slots[i] < slots[i - 1]:
            issues.append(("R3", f"乱序: [{i-1}]slot{slots[i-1]} > [{i}]slot{slots[i]}"))
            break
    seen = {}
    for slot, sid, t in marked:
        if SLOTS.is_unique(slot):
            if slot in seen:
                issues.append(("R4", f"uniq槽位{slot}({SLOTS.slot_name(slot)})重复"))
            seen[slot] = sid
        if sid:
            dup = sum(1 for _, x, _ in marked if x == sid)
            if dup > 1:
                issues.append(("R5", f"id={sid} 重复×{dup}"))
    return issues


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    summary = "--summary" in sys.argv
    cids = args or [d.name for d in sorted(COMMUNITY.iterdir())
                    if (d / "index.html").is_file()]
    bad = []
    for cid in cids:
        html = (COMMUNITY / cid / "index.html").read_text(
            encoding="utf-8", errors="replace")
        issues = check(html)
        if issues:
            bad.append((cid, issues))
    print(f"校验 {len(cids)} 个课件：合规 {len(cids)-len(bad)}，违规 {len(bad)}")
    if summary:
        from collections import Counter
        cnt = Counter(r for _, iss in bad for r, _ in iss)
        print("违规类型:", dict(cnt))
    for cid, issues in bad[:15]:
        print(f"  ❌ {cid}")
        for r, d in issues[:3]:
            print(f"     {r}: {d}")
    return bad


if __name__ == "__main__":
    main()
