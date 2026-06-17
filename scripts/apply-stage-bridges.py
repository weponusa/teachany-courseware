#!/usr/bin/env python3
"""将 data/stage-bridges.json 写入课标树 prerequisites（cn-unified + cn 分学段树）。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAGE_BRIDGES = ROOT / "data" / "stage-bridges.json"
TREES = ROOT / "data" / "trees"

PATCH_DIRS = [
    TREES / "cn-unified",
    TREES / "cn" / "elementary",
    TREES / "cn" / "middle",
    TREES / "cn" / "high",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_all_ids() -> set[str]:
    ids: set[str] = set()
    for fp in TREES.rglob("*.json"):
        if fp.name.startswith("_"):
            continue
        data = load_json(fp)
        for dom in data.get("domains") or []:
            for node in dom.get("nodes") or []:
                nid = node.get("id")
                if nid:
                    ids.add(nid)
    return ids


def patch_tree(data: dict, bridges: list[dict], known_ids: set[str]) -> int:
    changed = 0
    index: dict[str, dict] = {}
    for dom in data.get("domains") or []:
        for node in dom.get("nodes") or []:
            nid = node.get("id")
            if nid:
                index[nid] = node

    for bridge in bridges:
        target_id = bridge["target"]
        node = index.get(target_id)
        if not node:
            continue
        pre = list(node.get("prerequisites") or [])
        before = set(pre)
        for src in bridge.get("sources") or []:
            if src in known_ids and src not in before:
                pre.append(src)
                before.add(src)
        if pre != list(node.get("prerequisites") or []):
            node["prerequisites"] = pre
            changed += 1
    return changed


def main() -> int:
    if not STAGE_BRIDGES.exists():
        print(f"[FATAL] 缺少 {STAGE_BRIDGES}", file=sys.stderr)
        return 2

    bridges = load_json(STAGE_BRIDGES).get("bridges") or []
    known_ids = collect_all_ids()
    total_files = 0
    total_nodes = 0

    for base in PATCH_DIRS:
        if not base.is_dir():
            continue
        for fp in sorted(base.glob("*.json")):
            if fp.name.startswith("_"):
                continue
            data = load_json(fp)
            n = patch_tree(data, bridges, known_ids)
            if n:
                fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                total_files += 1
                total_nodes += n
                print(f"  ✅ {fp.relative_to(ROOT)}: {n} 个节点已桥接")

    print(f"✅ stage-bridges 已应用：{total_nodes} 个节点 · {total_files} 个树文件")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
