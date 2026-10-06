#!/usr/bin/env python3
"""全量课件结构重排：hero 置顶 → 内容模块保持原序 → 收尾组（音频 → 知识图谱 → AI 学伴）。

规则：
1. 收尾组块（teachany-audio-player / knowledge-graph(含data-teachany-kg) / teachany-ai-tutor-card）
   一律移到内容流末尾，顺序 audio → kg → tutor（对齐 course-skeleton-v2 模板）。
2. hero-cover 裸图 section 不在 hero 紧邻位置时，移到 hero header 之后（不删除资产引用）。
3. 分页模式（slide-page）同样适用：kg/tutor 页移到容器末尾，并重排 data-page-index。
4. 幂等：已符合规范的文件不产生改动。

用法：
  python3 scripts/fix-structure-order.py            # 全量
  python3 scripts/fix-structure-order.py --only hist-m-greece-rome --dry
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMMUNITY = ROOT / "community"

BLOCK_RE = re.compile(r"<(section|header)\b[^>]*>|</(section|header)>", re.I)
MASK_RE = re.compile(r"<script\b[\s\S]*?</script>|<style\b[\s\S]*?</style>|<!--[\s\S]*?-->", re.I)


def mask(html: str) -> str:
    """把 script/style/注释区域替换为等长空格，避免误扫其中的 section 标签。"""
    return MASK_RE.sub(lambda m: " " * (m.end() - m.start()), html)


def scan_blocks(masked: str):
    """深度法扫描顶层 section/header 块，返回 [(tag, start, end, open_tag_text)]。"""
    blocks = []
    depth = 0
    cur = None
    for m in BLOCK_RE.finditer(masked):
        token = m.group(0)
        if token.startswith("</"):
            if depth > 0:
                depth -= 1
                if depth == 0 and cur:
                    blocks.append((cur[0], cur[1], m.end(), cur[2]))
                    cur = None
        else:
            if depth == 0:
                cur = (m.group(1).lower(), m.start(), token)
            depth += 1
    return blocks


def classify(tag: str, attrs: str, body: str) -> str:
    bid = re.search(r'id="([^"]+)"', attrs)
    bid = bid.group(1) if bid else ""
    if "data-teachany-kg" in body or bid == "knowledge-graph":
        return "kg"
    if bid == "teachany-ai-tutor-card":
        return "tutor"
    if bid == "teachany-audio-player" or "data-teachany-audio-playlist" in body:
        return "audio"
    if "hero-cover" in attrs:
        return "cover"
    if tag == "header" and "hero" in attrs:
        return "hero"
    return "content"


TAIL_RANK = {"audio": 0, "kg": 1, "tutor": 2}


def fix_html(html: str):
    """返回 (new_html, changed, moves描述)。"""
    masked = mask(html)
    blocks = scan_blocks(masked)
    if len(blocks) < 3:
        return html, False, []

    infos = []
    for tag, s, e, attrs in blocks:
        kind = classify(tag, attrs, html[s:e])
        infos.append({"tag": tag, "s": s, "e": e, "attrs": attrs, "kind": kind, "text": html[s:e]})

    tail_idx = [i for i, b in enumerate(infos) if b["kind"] in TAIL_RANK]
    hero_idx = next((i for i, b in enumerate(infos) if b["kind"] == "hero"), None)

    # ── 判定需要移动的块 ──
    moves = []  # (block_index, target)  target: 'tail' 或 hero 块索引之后
    # 1) 收尾组：应位于最后 K 个且按 audio→kg→tutor 排序
    if tail_idx:
        cur = [infos[i]["kind"] for i in tail_idx]
        want_tail_positions = list(range(len(infos) - len(tail_idx), len(infos)))
        already = tail_idx == want_tail_positions and cur == sorted(cur, key=lambda k: TAIL_RANK[k])
        if not already:
            for i in tail_idx:
                moves.append((i, "tail"))
    # 2) hero-cover：应紧跟 hero 块（hero 存在时）
    for i, b in enumerate(infos):
        if b["kind"] == "cover":
            if hero_idx is not None:
                if i != hero_idx + 1:
                    moves.append((i, "after-hero"))
            elif i > 1:
                moves.append((i, "front"))

    if not moves:
        return html, False, []

    moved_idx = {i for i, _ in moves}

    # ── 重建：gap 保留原位，被移动块挖掉 ──
    parts = []
    last = 0
    for i, b in enumerate(infos):
        parts.append(("gap", html[last:b["s"]]))
        if i not in moved_idx:
            parts.append(("block", i, b["text"]))
        last = b["e"]
    parts.append(("gap", html[last:]))
    base = "".join(p[1] if p[0] == "gap" else p[2] for p in parts)

    # ── 计算插入 ──
    tail_blocks = sorted((infos[i] for i, t in moves if t == "tail"), key=lambda b: TAIL_RANK[b["kind"]])
    cover_blocks = [infos[i] for i, t in moves if t in ("after-hero", "front")]

    def insert_after(base: str, anchor_text: str, payloads: list[str]):
        pos = base.find(anchor_text[:80])
        if pos < 0:
            return base, False
        end = pos + len(anchor_text)
        return base[:end] + "\n\n" + "\n\n".join(payloads) + base[end:], True

    # cover → hero 之后
    if cover_blocks:
        payloads = [b["text"] for b in cover_blocks]
        if hero_idx is not None and infos[hero_idx]["text"][:80] in base:
            base, _ = insert_after(base, infos[hero_idx]["text"], payloads)
        else:
            # 没有 hero header：插到第一个保留块之后
            first_kept = next((infos[i] for i in range(len(infos)) if i not in moved_idx), None)
            if first_kept:
                base, _ = insert_after(base, first_kept["text"], payloads)

    # tail → 最后一个保留块之后
    if tail_blocks:
        kept = [infos[i] for i in range(len(infos)) if i not in moved_idx]
        # 找重建后文本中最后一个保留块的结束位置
        anchor = None
        for b in reversed(kept):
            pos = base.rfind(b["text"][:80])
            if pos >= 0:
                anchor = pos + len(b["text"])
                break
        payloads = "\n\n" + "\n\n".join(b["text"] for b in tail_blocks)
        if anchor is not None:
            base = base[:anchor] + payloads + base[anchor:]
        else:
            base = base + payloads

    # ── 分页模式：重排 data-page-index ──
    if "slide-page" in base:
        counter = {"n": 0}

        def renum(m):
            v = counter["n"]
            counter["n"] += 1
            return f'data-page-index="{v}"'

        # 只重排 slide-page section 上的索引：逐块处理，避免误改脚本数字
        masked2 = mask(base)
        blocks2 = scan_blocks(masked2)
        pieces = []
        last = 0
        for tag, s, e, attrs in blocks2:
            seg = base[s:e]
            if "slide-page" in attrs:
                seg_new = re.sub(r'data-page-index="\d+"', renum, seg, count=1)
            else:
                seg_new = seg
            pieces.append(base[last:s])
            pieces.append(seg_new)
            last = e
        pieces.append(base[last:])
        base = "".join(pieces)

    desc = [f"{infos[i]['kind']}:{(re.search(r'id=\"([^\"]+)\"', infos[i]['attrs']) or [None,'?'])[1] if 'id=' in infos[i]['attrs'] else infos[i]['kind']}→{t}" for i, t in moves]
    return base, True, desc


def main():
    only = None
    dry = False
    args = sys.argv[1:]
    if "--only" in args:
        only = args[args.index("--only") + 1]
    if "--dry" in args:
        dry = True

    changed_files = 0
    scanned = 0
    for d in sorted(COMMUNITY.iterdir()):
        if not d.is_dir():
            continue
        if only and only not in d.name:
            continue
        f = d / "index.html"
        if not f.is_file():
            continue
        html = f.read_text(encoding="utf-8", errors="replace")
        new, changed, desc = fix_html(html)
        scanned += 1
        if changed:
            changed_files += 1
            print(f"{'[DRY] ' if dry else ''}✏️  {d.name} ({len(desc)} moves)")
            if only:
                for x in desc:
                    print(f"     - {x}")
            if not dry:
                f.write_text(new, encoding="utf-8")
    print(f"\n扫描 {scanned}，改动 {changed_files}{'（dry-run 未写入）' if dry else ''}")


if __name__ == "__main__":
    main()
