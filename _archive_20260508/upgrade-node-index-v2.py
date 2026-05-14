#!/usr/bin/env python3
"""
方案 Y+ 步骤 2：把 data/node-index.json 升级为 v2.0 聚合查询入口。

v1 字段（保留）:
  node_id, name_zh, name_en, domain, curriculum, stage, subject,
  tree_path, courses

v2 新增字段:
  md_path          : skill/data/kp-md/kp-{node_id}.md (若存在)
  md_status        : ready / basic / pending / none
  hero_image       : image-registry 反查的图片路径 (若存在)
  prereq_ids       : MD 里解析出的前驱 node_id 列表
  next_ids         : MD 里解析出的后续 node_id 列表
  has_excerpts     : bool (现在 MD 已吸收，仅作历史标记)

v2 废弃字段:
  excerpts_path   → 删（MD 已吸收）
  kp_id           → 删（重复，kp-{node_id} 可动态拼）
  excerpt_count   → 删（MD 已吸收）
"""
import json, re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "data" / "node-index.json"
MANIFEST_PATH = ROOT / "skill" / "data" / "kp-md-manifest.json"
MD_DIR = ROOT / "skill" / "data" / "kp-md"
REGISTRY_PATH = ROOT / "skill" / "assets" / "image-registry.json"


def build_hero_map():
    """从 image-registry 构建 node_id → hero_file 映射"""
    if not REGISTRY_PATH.exists():
        return {}
    reg = json.load(open(REGISTRY_PATH, encoding='utf-8'))
    images = reg.get("images") if isinstance(reg, dict) else None
    if not isinstance(images, list):
        return {}
    m = {}
    for img in images:
        slot = img.get("slot") or ""
        file_ = img.get("file") or ""
        for nid in img.get("match_nodes") or []:
            cur = m.get(nid)
            # 优先 hero slot
            if cur is None or (slot == "hero" and cur[0] != "hero"):
                m[nid] = (slot, file_)
    return {k: v[1] for k, v in m.items()}


def build_md_map():
    """从 kp-md-manifest 构建 node_id → {md_file, md_status}"""
    if not MANIFEST_PATH.exists():
        return {}
    km = json.load(open(MANIFEST_PATH, encoding='utf-8'))
    m = {}
    for e in km.get("entries", []):
        nid = e.get("node_id")
        if not nid: continue
        m[nid] = {
            "md_file": e.get("md_file"),
            "md_status": e.get("md_status", "none"),
        }
    return m


def parse_md_relations(md_path):
    """从 MD 文件解析 prereq / next 关系"""
    try:
        md = Path(md_path).read_text(encoding='utf-8')
    except Exception:
        return [], []
    prereq, nxt = [], []
    # 形如: ## 前驱知识 / ## 前置知识 \n - `node_id` 或 - node_id
    def extract_block(section_titles):
        for title in section_titles:
            m = re.search(
                r'^##+\s+(?:' + title + r')[^\n]*\n(.*?)(?=^##\s|\Z)',
                md, re.M | re.S
            )
            if m:
                block = m.group(1)
                ids = re.findall(r'[`\-\*]\s*`?([a-z][\w-]+-[\w-]+)`?', block)
                return ids
        return []
    prereq = extract_block(["前驱知识", "前置知识", "前置"])
    nxt = extract_block(["后续延伸", "后续知识", "并行知识", "扩展知识"])
    return prereq, nxt


def main():
    print("[load] node-index.json v1")
    idx = json.load(open(INDEX_PATH, encoding='utf-8'))
    print(f"  nodes: {len(idx['nodes'])}")

    hero_map = build_hero_map()
    print(f"[load] hero 映射: {len(hero_map)}")

    md_map = build_md_map()
    print(f"[load] md 映射: {len(md_map)}")

    upgraded = 0
    with_md = 0
    with_hero = 0
    with_prereq = 0

    for nid, node in idx["nodes"].items():
        # 清除废弃字段
        for k in ("excerpts_path", "kp_id", "excerpt_count"):
            node.pop(k, None)

        # 加 md_path / md_status
        md_info = md_map.get(nid, {})
        if md_info.get("md_file"):
            node["md_path"] = f"skill/data/kp-md/{md_info['md_file']}"
            node["md_status"] = md_info.get("md_status") or "unknown"
            with_md += 1
            # 解析 MD 关系
            abs_md = ROOT / node["md_path"]
            prereq, nxt = parse_md_relations(abs_md)
            if prereq: node["prereq_ids"] = prereq
            if nxt: node["next_ids"] = nxt
            if prereq: with_prereq += 1
        else:
            node["md_status"] = "none"

        # 加 hero_image
        hero = hero_map.get(nid)
        if hero:
            node["hero_image"] = hero
            with_hero += 1

        upgraded += 1

    # 更新 meta
    idx["_meta"] = {
        "version": "2.0",
        "description": "统一节点索引 v2.0：node_id → (tree/md/hero/relations) 聚合入口；方案 Y+ 起 MD 为唯一真相源",
        "total_nodes": upgraded,
        "with_md": with_md,
        "with_hero": with_hero,
        "with_prereq": with_prereq,
        "schema_notes": "excerpts 已并入 MD 的「课标原文」小节；excerpts_path/kp_id/excerpt_count 字段在 v2.0 已废弃。",
    }

    # 写回
    with open(INDEX_PATH, "w", encoding='utf-8') as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)

    print(f"\n[write] {INDEX_PATH.relative_to(ROOT)}")
    print(f"  total: {upgraded}")
    print(f"  with_md: {with_md}")
    print(f"  with_hero: {with_hero}")
    print(f"  with_prereq: {with_prereq}")

    # 打印一个样例
    sample_nid = next((nid for nid in idx["nodes"]
                       if idx["nodes"][nid].get("md_status") == "ready"
                       and idx["nodes"][nid].get("hero_image")), None)
    if sample_nid:
        print(f"\n示例 {sample_nid}:")
        print(json.dumps(idx["nodes"][sample_nid], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
