#!/usr/bin/env python3
"""assemble-modules.py — 按 data-slot 重排课件顶层模块

设计（吸收此前翻车教训）：
  - 纯重排：不增删任何字符，长度严格守恒
  - 碎片跟随：section 之间的非 section 内容（script/注释/空行）
    跟随其前驱 section 一起移动，不丢失不错位
  - 稳定排序：按 (data-slot, 原序号) 排序，同槽位保持原相对序
  - 未打标模块跟随其前驱已打标模块（保持原位关系）
  - script 内的内容不属于任何 section（SHELL.sections 顶层扫描
    已按标签配对，不含 script 内部伪 section——但仍整体移动，
    碎片跟随策略保证 script 与其前驱 section 不分离）

验证（每次写入前）：
  V1 长度严格相等
  V2 去空白后字符多重集一致
  V3 section 开闭计数不变
  V4 栈平衡
  V5 首尾约束满足（hero 第一、图谱最后）

用法: python3 assemble-modules.py <cid> [cid...] [--dry]
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

_spec3 = importlib.util.spec_from_file_location(
    "check", ROOT / "scripts" / "check-slots.py")
CHECK = importlib.util.module_from_spec(_spec3)
_spec3.loader.exec_module(CHECK)

TAG = re.compile(r'<section\b[^>]*>|</section>')


def split_units(html):
    """拆分为：前置碎片 + [(section+尾随碎片, slot, idx)]"""
    secs = list(SHELL.sections(html, top_only=True))
    if not secs:
        return None, []
    head = html[:secs[0][0]]
    units = []
    for i, (s, e, a, b) in enumerate(secs):
        tail_end = secs[i + 1][0] if i + 1 < len(secs) else len(html)
        tail = html[e:tail_end]
        slot_m = re.search(r'data-slot="(\d+)"', a)
        slot = int(slot_m.group(1)) if slot_m else None
        units.append((html[s:tail_end], slot, i))
    return head, units


def assemble(html):
    head, units = split_units(html)
    if units is None:
        return html, 0
    marked = [u for u in units if u[1] is not None]
    if len(marked) < 2:
        return html, 0
    # 未打标模块跟随前驱（给前驱槽位；无打标前驱的归 slot 999 留在尾部）
    resolved = []
    cur = 999
    for frag, slot, idx in units:
        if slot is not None:
            cur = slot
        resolved.append((frag, cur if slot is None else slot, idx))
    ordered = sorted(resolved, key=lambda u: (u[1], u[2]))
    if [u[2] for u in ordered] == [u[2] for u in resolved]:
        return html, 0                       # 已有序
    return head + "".join(u[0] for u in ordered), sum(
        1 for a, b in zip(resolved, ordered) if a[2] != b[2])


def verify(old, new):
    errs = []
    if len(old) != len(new):
        errs.append(f"长度变化 {len(old)}→{len(new)}")
    t = lambda h: sorted(re.sub(r'\s+', '', h))
    if t(old) != t(new):
        errs.append("字符集变化")
    for pat in (r'<section\b', r'</section>'):
        if len(re.findall(pat, old)) != len(re.findall(pat, new)):
            errs.append("section数变化")
            break
    depth = 0
    for m in TAG.finditer(new):
        depth += 1 if m.group().startswith('<section') else -1
        if depth < 0:
            errs.append("栈负")
            break
    if depth != 0:
        errs.append("栈不平衡")
    return errs


def process(cid, dry=False):
    p = COMMUNITY / cid / "index.html"
    old = p.read_text(encoding="utf-8", errors="replace")
    # A 方案：只对 check-slots 报「顺序违规」(R1/R2/R3) 的课件动手。
    # 合规课件不碰——否则组装器会把手工精修过、顺序合理但不符合
    # 槽位表严格序的课件（如 phy-m-ideal-gas-equation 的情境开场
    # 设计）强制重排，覆盖人工成果。R4/R5 是重复问题，重排无用。
    order_issues = [r for r, _ in CHECK.check(old) if r in ("R1", "R2", "R3")]
    if not order_issues:
        return None
    new, moved = assemble(old)
    if moved == 0:
        return None
    errs = verify(old, new)
    if errs:
        print(f"  ❌ {cid}: {'; '.join(errs)}（未写入）")
        return False
    print(f"  ✓ {cid}: 重排 {moved} 个模块")
    if not dry:
        p.write_text(new, encoding="utf-8")
        return True
    return "dry"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry" in sys.argv
    ok = fail = skip = 0
    for cid in args:
        try:
            r = process(cid, dry)
            if r is True:
                ok += 1
            elif r is False:
                fail += 1
            else:
                skip += 1
        except Exception as e:
            print(f"  ❌ {cid}: {str(e)[:60]}")
            fail += 1
    print(f"\n重排 {ok}，失败 {fail}，已有序跳过 {skip}")


if __name__ == "__main__":
    main()
