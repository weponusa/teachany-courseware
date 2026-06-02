#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将 data/trees 中节点的 courses[] 同步到 data/node-index.json 的 nodes.*.courses。"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NODE_INDEX = ROOT / "data" / "node-index.json"
TREES_DIR = ROOT / "data" / "trees"
REGISTRY = ROOT / "registry.json"
SITE_BASE = "https://www.teachany.cn"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def collect_tree_courses():
    out: dict[str, list[str]] = {}
    for tf in sorted(TREES_DIR.rglob("*.json")):
        if tf.name.startswith("_"):
            continue
        data = load_json(tf)
        for dom in data.get("domains") or []:
            for node in dom.get("nodes") or []:
                nid = node.get("id")
                if not nid:
                    continue
                cids = list(node.get("courses") or [])
                if cids:
                    out[nid] = sorted(set(out.get(nid, []) + cids))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    registry = {c["id"]: c for c in load_json(REGISTRY).get("courses", [])}
    data = load_json(NODE_INDEX)
    nodes = data.get("nodes") or {}
    tree_map = collect_tree_courses()

    updated = 0
    for nid, cids in tree_map.items():
        if nid not in nodes:
            continue
        courses = []
        for cid in cids:
            r = registry.get(cid, {})
            path = (r.get("path") or f"community/{cid}").strip("/")
            courses.append({
                "id": cid,
                "name_zh": r.get("name") or cid,
                "download_url": f"{SITE_BASE}/{path}/",
            })
        if (nodes[nid].get("courses") or []) != courses:
            nodes[nid]["courses"] = courses
            updated += 1

    data["nodes"] = nodes
    if args.dry_run:
        print(f"[dry-run] 将更新 {updated} 个节点")
        return

    NODE_INDEX.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"✅ node-index courses 已同步: {updated} 个节点更新")


if __name__ == "__main__":
    main()
