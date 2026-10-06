#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""知识图谱「后面还堆了一堆东西」的统一修法。

判定
----
知识图谱是**收尾展示模块**：它之后不该再有讲解、练习、前测/后测、小结、易错点、记忆锚点、
深度理解、探究任务这类教学内容。允许留在它后面的只有 AI 学伴入口卡片与收尾媒体块
（动画讲解 / 本课知识动画 / 教学视频 / 微课）。同一页出现 2 个知识图谱模块属于注入残留。

修法
----
① 去重：同一 `data-teachany-kg` 值出现 ≥2 次时，保留最后一个，删掉前面的。
② 归位：把 KG 之后**属于教学内容**的 section 整体前移到 KG 之前（保持相对顺序）。
   净效果 = 知识图谱落到教学内容之后，只剩 AI 学伴 / 收尾媒体在它后面。

实现要点
--------
课件的 section 常常是**嵌套**的（一个外层 wrapper 里塞了 KG 与后续所有模块），
所以不能只看最外层 section：要把所有 section 都列出来，取「在 KG 之后、且不包含 KG」的
**极大块**，再过滤教学内容。

护栏
----
· v2 分页课件（`.slide-container`）的 DOM 顺序就是页序，本工具不动，交 fix-course-dups-order.py。
· 每门过 tools/_qa_gate.apply_guarded（错误数上升或标签失衡即回滚）。

用法:  python3 tools/fix-kg-tail-order.py [--apply] [--from-list f] [--limit N]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from _qa_gate import apply_guarded, imbalance  # noqa: E402

KEEP_AFTER = re.compile(
    r'id="teachany-ai-tutor-card"|data-teachany-tutor-card|AI 学伴|学伴入口|'
    r'动画讲解|教学动画|本课知识动画|教学视频|微课|动画回顾|动画解说|动画模拟|动画探索|动画教学|'
    r'动画视频|视频讲解', re.I)


def all_sections(h: str):
    """列出所有 <section>（含嵌套）的 (start, end, text)，按出现顺序。"""
    out, i = [], 0
    opens = [(m.start(), m.end()) for m in re.finditer(r'<section\b[^>]*>', h)]
    for s, se in opens:
        depth, j = 1, se
        for t in re.finditer(r'<(/?)section\b[^>]*>', h[j:]):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                j = j + t.end()
                break
        else:
            continue
        out.append((s, j, h[s:j]))
    return out


def head_text(seg: str) -> str:
    m = re.search(r'<h[12][^>]*>(.*?)</h[12]>', seg, re.S)
    return re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else ''


def kg_blocks(h: str, secs):
    """返回 [(start, end, text)] —— 每个知识图谱宿主所在的最小 section。"""
    blocks, seen = [], set()
    for m in re.finditer(r'data-teachany-kg\s*=\s*"([^"]*)"', h):
        s = h.rfind('<section', 0, m.start())
        if s == -1:
            continue
        hit = next(((a, b, t) for a, b, t in secs if a == s), None)
        if not hit:
            continue
        key = (hit[0], hit[1])
        if key in seen:
            continue
        seen.add(key)
        blocks.append((hit[0], hit[1], hit[2], m.group(1)))
    return blocks


def plan(cid: str):
    f = ROOT / 'community' / cid / 'index.html'
    if not f.is_file():
        return None, 'no-file'
    h = f.read_text(encoding='utf-8')
    if 'slide-container' in h:
        return None, 'slide-container'
    secs = all_sections(h)
    blocks = kg_blocks(h, secs)
    if not blocks:
        return None, 'no-kg'

    note = []
    out = h
    # ① 去重（同一 kg 值多次出现 → 保留最后一个）
    by_val = {}
    for b in blocks:
        by_val.setdefault(b[3], []).append(b)
    drops = []
    for val, bs in by_val.items():
        for b in bs[:-1]:
            drops.append((b[0], b[1]))
    if drops:
        for a, b in sorted(drops, reverse=True):
            out = out[:a] + out[b:]
        note.append('del-dup%dx' % len(drops))

    # ② 归位
    secs = all_sections(out)
    blocks = kg_blocks(out, secs)
    if not blocks:
        return None, 'kg-lost'
    k = blocks[-1]
    ks, ke = k[0], k[1]
    cands = [x for x in secs if x[0] >= ke]
    # 只保留极大块（去掉被别人包住的），且排除包含 KG 的块
    maximal = [x for x in cands
               if not any((y[0] <= x[0] and x[1] <= y[1] and y != x) for y in cands)]
    movable = []
    for a, b, t in maximal:
        if not head_text(t):
            continue
        if KEEP_AFTER.search(t[:700]):
            continue
        movable.append((a, b, t))
    if movable:
        moved = ''.join(x[2] + '\n' for x in movable)
        # 先摘掉这些块（倒序删除，避免偏移），再在「重算后的 KG 起点」插入
        tmp = out
        for a, b, _ in reversed(movable):
            tmp = tmp[:a] + tmp[b:]
        secs2 = all_sections(tmp)
        bl2 = kg_blocks(tmp, secs2)
        if not bl2:
            return None, 'kg-lost'
        ks2 = bl2[-1][0]
        out = tmp[:ks2] + moved + tmp[ks2:]
        note.append('moved:%d' % len(movable))

    if out == h:
        return None, 'ok'
    return out, '+'.join(note)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--from-list', default='')
    ap.add_argument('--limit', type=int, default=0)
    args = ap.parse_args()

    cids = ([x.strip() for x in Path(args.from_list).read_text(encoding='utf-8').split() if x.strip()]
            if args.from_list else sorted(d.name for d in (ROOT / 'community').iterdir()))
    if args.limit:
        cids = cids[: args.limit]

    changed, skipped = [], []
    for cid in cids:
        new, why = plan(cid)
        if not new:
            if why not in ('ok', 'no-kg', 'no-file'):
                skipped.append((cid, why))
            continue
        f = ROOT / 'community' / cid / 'index.html'
        h = f.read_text(encoding='utf-8')
        if imbalance(new) > imbalance(h):
            skipped.append((cid, '平衡变差'))
            continue
        if not args.apply:
            changed.append((cid, why))
            continue
        ok, why2 = apply_guarded(f, new, cid)
        (changed if ok else skipped).append((cid, why if ok else why2))
    print('%s可改 %d 门' % ('' if args.apply else '干跑：', len(changed)))
    for c in changed[:40]:
        print('   ', c)
    print('跳过 %d 门' % len(skipped))
    for s in skipped[:20]:
        print('    ↷', s)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
