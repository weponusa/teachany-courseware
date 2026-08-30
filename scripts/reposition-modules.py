#!/usr/bin/env python3
"""reposition-modules.py — 把补写的模块放到教学逻辑正确的位置

补写模块时若找不到 lesson-focus / lesson-method 这类锚点，会退回到
「插到 posttest 或 knowledge-graph 之后」，结果范例(worked-example)跑到了
页面末尾的检测模块后面，教学顺序变成：

    正文 → 练习 → 后测 → 小结 → 深层理解 → 范例      ← 范例在最后，不对

正确顺序应是：正文 → 范例 → 练习 → 后测 → 小结。

本脚本把 worked-example 移到「第一个练习/检测类模块」之前；
summary 移到 posttest 之后。只调整位置，不动内容。

用法: python3 reposition-modules.py [cid...] [--dry]
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

# 练习/检测类：范例应排在它们之前。
# 用包含匹配而非完全相等——实际 id 常带前缀（sec-quiz、module-practice 等），
# 若要求全等会漏掉前面真正的练习模块，反而匹配到范例之后的 error-watch，
# 导致误判「已在正确位置」而不移动。
BEFORE = re.compile(
    r'id="[^"]*(practice|exercise|drill|posttest|post-test|quiz|'
    r'error-clinic|error-watch|concept-check|assessment)[^"]*"')


def find_sec(secs, pattern):
    for s, e, a, b in secs:
        if pattern.search(a):
            return (s, e, a, b)
    return None


def process(cid, dry=False):
    P = COMMUNITY / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")
    acts = []

    # 1) worked-example 移到第一个练习/检测模块之前
    for _ in range(1):
        secs = SHELL.sections(html, top_only=True)
        we = next((x for x in secs if 'id="worked-example"' in x[2]), None)
        if not we:
            break
        target = find_sec(secs, BEFORE)
        if not target or target[0] > we[0]:
            break                       # 已经在正确位置
        frag = html[we[0]:we[1]]
        html = html[:we[0]] + html[we[1]:]     # 先摘除
        # 重新定位插入点（摘除后偏移变了）
        secs2 = SHELL.sections(html, top_only=True)
        tgt2 = find_sec(secs2, BEFORE)
        if not tgt2:
            html = html[:we[0]] + frag + html[we[0]:]
            break
        html = html[:tgt2[0]] + frag + html[tgt2[0]:]
        acts.append(f"worked-example 移到 {re.search(r'id=.([^\"]+)', tgt2[2]).group(1)} 之前")

    # 2) summary 移到 posttest 之后
    secs = SHELL.sections(html, top_only=True)
    sm = next((x for x in secs if re.search(r'id="summary"', x[2])), None)
    pt = find_sec(secs, re.compile(r'id="(posttest|post-test)"'))
    if sm and pt and sm[0] < pt[0]:
        frag = html[sm[0]:sm[1]]
        html = html[:sm[0]] + html[sm[1]:]
        secs2 = SHELL.sections(html, top_only=True)
        pt2 = find_sec(secs2, re.compile(r'id="(posttest|post-test)"'))
        if pt2:
            html = html[:pt2[1]] + frag + html[pt2[1]:]
            acts.append("summary 移到 posttest 之后")

    if not acts or dry:
        return acts
    P.write_text(html, encoding="utf-8")
    return acts


def main():
    dry = "--dry" in sys.argv
    cids = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not cids:
        cids = sorted(p.name for p in COMMUNITY.iterdir() if (p / "index.html").exists())
    n = 0
    for c in cids:
        try:
            acts = process(c, dry)
            if acts:
                n += 1
                print(f"  {c}: {'; '.join(acts)}")
        except Exception as e:
            print(f"  ❌ {c}: {str(e)[:50]}")
    print(f"调整 {n} 个课件" + ("（--dry 未写入）" if dry else ""))


if __name__ == "__main__":
    main()
