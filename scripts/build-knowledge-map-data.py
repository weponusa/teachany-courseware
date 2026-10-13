#!/usr/bin/env python3
"""从课标树 + 跨层桥接重建 data/knowledge-map-data.json（全科学习路径图谱）。"""
from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TREES = ROOT / "data" / "trees"
OUT = ROOT / "data" / "knowledge-map-data.json"
STAGE_BRIDGES = ROOT / "data" / "stage-bridges.json"
UNI_BRIDGES = ROOT / "data" / "university-bridges.json"

CN_UNIFIED = TREES / "cn-unified"
INTL_CURRICULA = ("ap", "cambridge", "ib", "us")


def load_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def infer_stage(node: dict, tree: dict, rel_parts: tuple[str, ...]) -> str:
    stage = node.get("stage") or tree.get("stage") or ""
    if stage:
        return stage
    if len(rel_parts) >= 2:
        return rel_parts[1]
    grade = node.get("grade")
    if isinstance(grade, int):
        if 1 <= grade <= 6:
            return "elementary"
        if 7 <= grade <= 9:
            return "middle"
        if grade >= 10:
            return "high"
    if grade == 0:
        return "university"
    coverage = tree.get("stage_coverage") or []
    if coverage:
        return coverage[0]
    return ""


def collect_from_tree(path: Path, nodes: dict[str, dict], edges: set[tuple[str, str]]) -> None:
    rel = path.relative_to(TREES)
    rel_parts = rel.parts
    curriculum = rel_parts[0] if rel_parts else ""
    data = load_json(path)
    subject = data.get("subject") or path.stem
    tree_stage = data.get("stage") or (rel_parts[1] if len(rel_parts) >= 2 else "")

    for dom in data.get("domains") or []:
        domain_id = dom.get("id") or dom.get("slug") or ""
        for node in dom.get("nodes") or []:
            nid = node.get("id")
            if not nid:
                continue
            grade = node.get("grade")
            if isinstance(grade, str):
                try:
                    grade = int(grade)
                except ValueError:
                    grade = 0
            if grade is None:
                grade = 0

            key_concepts = list(node.get("curriculum_points") or node.get("key_concepts") or [])
            definition = node.get("definition") or (key_concepts[0][:120] if key_concepts else "")

            record = {
                "id": nid,
                "name": node.get("name") or nid,
                "name_en": node.get("name_en") or "",
                "subject": node.get("subject") or subject,
                "grade": grade,
                "domain": node.get("domain") or domain_id,
                "difficulty": node.get("difficulty") or 0,
                "definition": definition,
                "skills": list(node.get("skills") or []),
                "stage": infer_stage(node, data, rel_parts),
                "curriculum": node.get("curriculum") or curriculum,
                "tree_path": str(rel).replace("\\", "/"),
            }
            if nid not in nodes or len(record.get("definition", "")) > len(nodes[nid].get("definition", "")):
                nodes[nid] = record

            for pre in node.get("prerequisites") or []:
                if pre:
                    edges.add((pre, nid))
            for ext in node.get("extends") or []:
                if ext:
                    edges.add((nid, ext))
            for par in node.get("parallel") or []:
                if par:
                    edges.add((nid, par))
                    edges.add((par, nid))


def apply_bridge_file(path: Path, edges: set[tuple[str, str]], nodes: dict[str, dict]) -> int:
    if not path.exists():
        return 0
    payload = load_json(path)
    added = 0
    for item in payload.get("bridges") or []:
        if "target" in item and "sources" in item:
            tgt = item["target"]
            for src in item["sources"]:
                if src in nodes and tgt in nodes:
                    pair = (src, tgt)
                    if pair not in edges:
                        edges.add(pair)
                        added += 1
        elif "source" in item and "target" in item:
            src, tgt = item["source"], item["target"]
            if src in nodes and tgt in nodes:
                pair = (src, tgt)
                if pair not in edges:
                    edges.add(pair)
                    added += 1
    return added


def main() -> int:
    nodes: dict[str, dict] = {}
    edges: set[tuple[str, str]] = set()

    if not CN_UNIFIED.is_dir():
        print(f"[FATAL] 缺少 {CN_UNIFIED}", file=sys.stderr)
        return 2

    for fp in sorted(CN_UNIFIED.glob("*.json")):
        if fp.name.startswith("_"):
            continue
        collect_from_tree(fp, nodes, edges)

    intl_count = 0
    for cur in INTL_CURRICULA:
        base = TREES / cur
        if not base.is_dir():
            continue
        for fp in sorted(base.rglob("*.json")):
            if fp.name.startswith("_"):
                continue
            before = len(nodes)
            collect_from_tree(fp, nodes, edges)
            intl_count += len(nodes) - before

    stage_added = apply_bridge_file(STAGE_BRIDGES, edges, nodes)
    uni_added = apply_bridge_file(UNI_BRIDGES, edges, nodes)

    node_ids = set(nodes.keys())
    clean_edges = sorted(
        (s, t) for s, t in edges if s in node_ids and t in node_ids and s != t
    )

    by_subject = Counter(n["subject"] for n in nodes.values())
    by_grade = Counter(str(n["grade"]) for n in nodes.values())

    sci_e = [n for n in nodes.values() if n["id"].startswith("sci-e-")]
    sci_cross = sum(
        1 for s, t in clean_edges
        if (s.startswith("sci-e-")) != (t.startswith("sci-e-"))
    )

    payload = {
        "nodes": sorted(nodes.values(), key=lambda n: (n.get("subject", ""), n.get("grade", 0), n["id"])),
        "edges": [{"source": s, "target": t} for s, t in clean_edges],
        "stats": {
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "totalNodes": len(nodes),
            "totalEdges": len(clean_edges),
            "cnUnifiedNodes": sum(1 for n in nodes.values() if n.get("curriculum") == "cn-unified"),
            "internationalNodes": intl_count,
            "stageBridgeEdges": stage_added,
            "universityBridgeEdges": uni_added,
            "sciElementaryNodes": len(sci_e),
            "sciCrossEdges": sci_cross,
            "subjects": sorted(by_subject.keys()),
            "bySubject": dict(by_subject.most_common()),
            "byGrade": dict(sorted(by_grade.items(), key=lambda kv: int(kv[0]) if kv[0].isdigit() else 99)),
        },
    }

    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"✅ knowledge-map-data.json: {len(nodes)} 节点 · {len(clean_edges)} 边"
        f" · 国际 +{intl_count} · 小学科学跨层边 {sci_cross}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
