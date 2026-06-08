#!/usr/bin/env python3
"""将误标为 K12 的大学学科（计算机、工程）统一改为 grade=0 / stage=university。"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TREES_DIR = ROOT / "data" / "trees" / "cn-unified"
MAP_DATA = ROOT / "data" / "knowledge-map-data.json"
METADATA = ROOT / "data" / "nodes-metadata.json"

# 大学层级学科：不应出现在 K12 年级轴上（info-tech 仍为高中课标，不在此列）
UNIVERSITY_SUBJECTS = frozenset({"computer-science", "engineering"})


def fix_tree_file(path: Path) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = 0

    def walk(nodes: list) -> None:
        nonlocal changed
        for n in nodes or []:
            if n.get("id") and n.get("grade") not in (0, None):
                n["grade"] = 0
                n["stage"] = "university"
                changed += 1
            elif n.get("id"):
                n["stage"] = n.get("stage") or "university"
                if n.get("grade") is None:
                    n["grade"] = 0
                    changed += 1

    for dom in data.get("domains") or []:
        walk(dom.get("nodes") or [])

    data["grade_range"] = [0, 0]
    data["stage_coverage"] = ["university"]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


def patch_knowledge_map() -> int:
    payload = json.loads(MAP_DATA.read_text(encoding="utf-8"))
    changed = 0
    for n in payload.get("nodes") or []:
        if n.get("subject") not in UNIVERSITY_SUBJECTS:
            continue
        if n.get("grade") != 0:
            n["grade"] = 0
            changed += 1
        n["stage"] = "university"
    payload["university_grade_fix"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    MAP_DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


def patch_nodes_metadata() -> int:
    if not METADATA.exists():
        return 0
    payload = json.loads(METADATA.read_text(encoding="utf-8"))
    changed = 0
    for n in payload.get("nodes") or []:
        if n.get("subject") not in UNIVERSITY_SUBJECTS:
            continue
        if n.get("grade") != 0:
            n["grade"] = 0
            n["difficulty"] = 0
            changed += 1
    METADATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


def main() -> int:
    tree_changed = 0
    for subj in sorted(UNIVERSITY_SUBJECTS):
        fp = TREES_DIR / f"{subj}.json"
        if not fp.exists():
            print(f"[skip] missing {fp}")
            continue
        n = fix_tree_file(fp)
        tree_changed += n
        print(f"✅ {fp.name}: {n} nodes → grade=0")

    km = patch_knowledge_map()
    print(f"✅ knowledge-map-data.json: {km} nodes patched")

    meta = patch_nodes_metadata()
    print(f"✅ nodes-metadata.json: {meta} nodes patched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
