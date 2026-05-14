#!/usr/bin/env python3
"""
方案 Y+ 合并：把 data/excerpts 的课标原文全量灌入 skill/data/kp-md/*.md
的「课标原文」小节，使 MD 成为唯一真相源。

匹配策略：
- excerpts kp_id 格式多样（旧：kp-{curriculum}-{stage}-{subject}-{node_id}，
  新：kp-{node_id}），统一用"以 MD 的 node_id 为尾部"做匹配。
- MD 的 node_id 通过头部 HTML 注释或元数据表提取。
"""
import json, re, sys, glob, os
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(__file__).resolve().parent.parent
EXCERPTS_DIR = ROOT / "data" / "excerpts"
MD_DIR = ROOT / "skill" / "data" / "kp-md"

DRY_RUN = "--apply" not in sys.argv


def load_all_excerpts():
    """返回 [(kp_id_raw, excerpt), ...]"""
    items = []
    files = 0
    for fp in EXCERPTS_DIR.rglob("*.json"):
        try:
            d = json.load(open(fp))
        except Exception:
            continue
        files += 1
        exs = d.get("excerpts", []) if isinstance(d, dict) else d if isinstance(d, list) else []
        for ex in exs:
            if not isinstance(ex, dict): continue
            kp = ex.get("kp_id")
            if not kp: continue
            items.append((kp, ex))
    print(f"[scan] 读取 {files} 个 excerpts 文件, 共 {len(items)} 条")
    return items


def build_excerpts_by_node(items, target_node_ids):
    """把 excerpts 聚合到 node_id（endswith 匹配）"""
    # 按 node_id 长度降序，先匹配最长的（更具体）
    sorted_nodes = sorted(target_node_ids, key=len, reverse=True)
    by_node = defaultdict(list)
    unmatched = 0

    for kp_id, ex in items:
        body = kp_id[3:] if kp_id.startswith("kp-") else kp_id
        # 找一个 node_id，使得 body endswith node_id 或 body == node_id
        matched = None
        for nid in sorted_nodes:
            if body == nid or body.endswith("-" + nid):
                matched = nid
                break
        if matched:
            by_node[matched].append(ex)
        else:
            unmatched += 1

    print(f"[match] excerpts 条目成功归位 node 数: {len(by_node)}, 未匹配条数: {unmatched}")
    return by_node


def parse_md_node_id(md_text):
    m = re.search(r'node_id[:=]\s*`?([\w-]+)`?', md_text)
    if m: return m.group(1)
    m = re.search(r'kp_id[:=]\s*`?([\w-]+)`?', md_text)
    if m:
        kp = m.group(1)
        return kp[3:] if kp.startswith("kp-") else kp
    return None


def build_curriculum_section(excerpts):
    by_source = defaultdict(list)
    seen = set()
    for ex in excerpts:
        src = ex.get("source", "其他")
        txt = (ex.get("text") or "").strip()
        if txt and txt not in seen:
            by_source[src].append(txt)
            seen.add(txt)

    SOURCE_ORDER = ["内容要求", "学业要求", "学业质量标准", "教学提示"]
    lines = []
    for src in SOURCE_ORDER:
        if src not in by_source: continue
        lines.append(f"### {src}\n")
        for t in by_source[src]:
            lines.append(f"> {t}\n")
        lines.append("")
    # 非标准 source 放「其他」
    other = {k: v for k, v in by_source.items() if k not in SOURCE_ORDER}
    if other:
        lines.append("### 其他原文\n")
        for src, texts in other.items():
            for t in texts:
                lines.append(f"> **[{src}]** {t}\n")
        lines.append("")
    return "\n".join(lines).strip()


def replace_or_insert_section(md_text, new_section_body, section_title="课标原文"):
    # 匹配 ## 课标原文... 到下个 ## 之前
    pattern = re.compile(
        r'^##\s+' + section_title + r'[^\n]*\n.*?(?=^##\s|\Z)',
        re.M | re.S
    )
    new_block = f"## {section_title}（2022年版）\n\n{new_section_body}\n\n"
    if pattern.search(md_text):
        return pattern.sub(new_block, md_text, count=1), "replaced"
    # 插入到「元数据」小节之后
    meta_match = re.search(r'^##\s+元数据[^\n]*\n.*?(?=^##\s|\Z)', md_text, re.M | re.S)
    if meta_match:
        end = meta_match.end()
        return md_text[:end] + "\n" + new_block + md_text[end:], "inserted_after_meta"
    # 兜底：插到第一个 ## 之前
    first_h2 = re.search(r'^##\s', md_text, re.M)
    if first_h2:
        pos = first_h2.start()
        return md_text[:pos] + new_block + md_text[pos:], "inserted_before_first_h2"
    return md_text.rstrip() + "\n\n" + new_block, "appended"


def main():
    md_files = list(MD_DIR.glob("*.md"))
    # 先收集所有 MD 的 node_id
    md_to_node = {}
    for mf in md_files:
        nid = parse_md_node_id(mf.read_text(encoding='utf-8'))
        if nid: md_to_node[mf] = nid
    target_nodes = set(md_to_node.values())
    print(f"[scan] MD 文件 {len(md_files)}, 带 node_id 的: {len(md_to_node)}, 唯一 node_id: {len(target_nodes)}")

    items = load_all_excerpts()
    by_node = build_excerpts_by_node(items, target_nodes)

    actions = Counter()
    touched = []

    for mf, nid in md_to_node.items():
        exs = by_node.get(nid)
        if not exs:
            actions["no_excerpts"] += 1
            continue
        md = mf.read_text(encoding='utf-8')
        # 已完整吸收？
        texts = [(ex.get("text") or "").strip() for ex in exs if ex.get("text")]
        if texts and all(t[:30] in md for t in texts):
            actions["already_complete"] += 1
            continue
        new_section = build_curriculum_section(exs)
        new_md, kind = replace_or_insert_section(md, new_section)
        if new_md == md:
            actions["no_change"] += 1
            continue
        actions[kind] += 1
        touched.append((mf, new_md))

    # 没 node_id 的 MD
    missing = len(md_files) - len(md_to_node)

    print("\n[stats]")
    print(f"  缺失 node_id 的 MD: {missing}")
    for k, v in actions.most_common():
        print(f"  {k}: {v}")
    print(f"  待写入: {len(touched)}")

    if DRY_RUN:
        print("\n(干跑模式，加 --apply 写入)")
        if touched:
            mf, new_md = touched[0]
            print(f"\n--- 示例 {mf.name} ---")
            m = re.search(r'^##\s+课标原文.*?(?=^##\s|\Z)', new_md, re.M | re.S)
            if m: print(m.group(0)[:700])
        return

    for mf, new_md in touched:
        mf.write_text(new_md, encoding='utf-8')
    print(f"\n[apply] 已写入 {len(touched)} 个文件")


if __name__ == "__main__":
    main()
