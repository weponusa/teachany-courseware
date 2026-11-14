#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TeachAny 单一知识层生成器（理想架构）

    data/trees/**  ──(唯一权威源)──►  canonical 节点表 + 统一关系表
                                      │
        ┌─────────────┬───────────────┼───────────────┬──────────────┐
        ▼             ▼               ▼               ▼              ▼
 knowledge-map  nodes-metadata  nodes-selector  node-index  node-enrichment
   -data.json       .json          .json          .json      -overlay.json
        └─────────────┴───────────────┴───────────────┴──────────────┘
                          全部由本脚本按同一份 canonical 生成

取代 rebuild-index.py 步骤 4.5 里 6 个各自读树、字段口径不一的派生脚本，
消除历史漂移：node-index 只有 2533/9679 且含死 ID、metadata 的 next_steps
仅 0.4%、km 节点缺 curriculum_points / prerequisites、selector 与 metadata
学科年级不一致等。

输入（只读）：
  data/trees/**/*.json                        权威节点与先修关系
  data/stage-bridges.json / university-bridges.json   跨学段/跨层桥接
  data/node-index.json                        历史 md/hero 资源信息（按 ID 合并保留）
  data/node-enrichment-overlay.json          历史人工增强内容（按 ID 合并保留）
  data/nodes-selector.json                   历史体系标签（按 ID 合并保留）
  data/knowledge-map-domain-labels.json     历史 domain 中文名（合并保留）

输出（覆盖写，路径与字段保持前端兼容）：
  data/unified/knowledge-layer.json          canonical（节点 + 关系 + 统计）
  data/knowledge-map-data.json
  data/nodes-metadata.json
  data/nodes-selector.json
  data/node-index.json
  data/knowledge-map-domain-labels.json
  data/node-enrichment-overlay.json

不修改 data/trees/**、registry*.json、community/、data/kp/（题库）。
用法：python3 scripts/build-knowledge-layer.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TREES = ROOT / "data" / "trees"
D = ROOT / "data"

INTL_CURRICULA = ("ap", "cambridge", "ib", "us")
STAGE_BY_PATH = {"elementary": "elementary", "middle": "middle", "high": "high",
                 "primary": "elementary", "lsec": "middle", "igcse": "high", "al": "high",
                 "pyp": "elementary", "myp": "middle", "dp": "high",
                 "k5": "elementary", "ms": "middle", "hs": "high"}
SUBJECT_WHITELIST = {
    "math", "chinese", "physics", "biology", "english", "chemistry", "history",
    "geography", "info-tech", "science", "politics", "psychology", "ela",
}


def j(p: Path, default=None):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return default


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def as_int(v):
    if isinstance(v, str):
        try:
            return int(v)
        except ValueError:
            return 0
    return int(v or 0)


def stage_for(rel_parts, grade, node_stage):
    """统一 stage 口径：只有 elementary / middle / high / university。"""
    if grade == 0:
        return "university"
    for part in rel_parts:
        if part in ("cn-unified", "advanced-math", "advanced-biology", "advanced-physics",
                    "advanced-chemistry", "earth-space", "formal-sciences", "engineering",
                    "computer-science", "civil-engineering"):
            return "university"
    for part in rel_parts:
        if part in STAGE_BY_PATH:
            return STAGE_BY_PATH[part]
    if grade <= 6:
        return "elementary"
    if grade <= 9:
        return "middle"
    return "high"


def curriculum_for(rel_parts):
    first = rel_parts[0] if rel_parts else ""
    if first in ("cn", "cn-unified"):
        return "cn-unified"
    return first if first else "unknown"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    # ── 1. 从所有树收集 canonical 节点（字段级合并，消除重复树漂移） ──
    nodes: dict[str, dict] = {}
    status_by_id: dict[str, str] = {}   # 树里显式 status 优先；缺失一律 placeholder（不伪装成完备节点）
    graph_paths: dict[str, list[str]] = defaultdict(list)
    tree_paths: dict[str, list[str]] = defaultdict(list)
    tree_files = 0

    for fp in sorted(TREES.rglob("*.json")):
        if fp.name.startswith("_") or "nxcyj501" in fp.parts:
            continue
        data = j(fp)
        if not isinstance(data, dict) or not data.get("domains"):
            continue
        rel = fp.relative_to(TREES)
        parts = rel.parts
        if len(parts) < 2:
            continue
        rel_s = str(rel).replace("\\", "/")
        subject = data.get("subject") or fp.stem
        curriculum = curriculum_for(parts)
        tree_files += 1

        for dom in data["domains"]:
            domain_id = dom.get("id") or dom.get("slug") or ""
            for n in dom.get("nodes") or []:
                nid = n.get("id")
                if not nid:
                    continue
                grade = as_int(n.get("grade"))
                key_concepts = list(n.get("curriculum_points") or n.get("key_concepts") or [])
                definition = n.get("definition") or n.get("description") or (
                    key_concepts[0][:200] if key_concepts else "")
                rec = {
                    "id": nid,
                    "name": n.get("name") or n.get("title") or nid,
                    "name_en": n.get("name_en") or "",
                    "subject": n.get("subject") or subject,
                    "grade": grade,
                    "domain": n.get("domain") or domain_id,
                    "difficulty": n.get("difficulty") or 0,
                    "definition": definition,
                    "skills": list(n.get("skills") or []),
                    "stage": stage_for(parts, grade, n.get("stage")),
                    "curriculum": n.get("curriculum") or curriculum,
                    "tree_path": rel_s,
                    "curriculum_points": list(n.get("curriculum_points") or []),
                    "key_concepts": list(n.get("key_concepts") or key_concepts),
                    "courses": list(n.get("courses") or []),
                    "status": n.get("status") or "active",
                    "textbook_chapter": n.get("textbook_chapter") or "",
                    "textbook_semester": n.get("textbook_semester") or "",
                    "excerpt_ids": list(n.get("excerpt_ids") or []),
                    "tags": list(n.get("tags") or []),
                    "prerequisites": list(n.get("prerequisites") or []),
                    "extends": list(n.get("extends") or []),
                    "parallel": list(n.get("parallel") or []),
                }
                st = n.get("status")
                if st:
                    status_by_id[nid] = st
                elif nid not in status_by_id:
                    status_by_id[nid] = "placeholder"
                graph_paths[nid].append(rel_s)
                tree_paths[nid].append(rel_s)
                if nid not in nodes:
                    nodes[nid] = rec
                    continue
                # 字段级合并：cn/{stage}/ 树（权威教材树）优先于 cn-unified/ 派生树；
                # 其余情况保留非空值更完整者。
                cur = nodes[nid]
                prefer_new = (rel_s.startswith("cn/") and not str(cur["tree_path"]).startswith("cn/"))
                for k, v in rec.items():
                    if k in ("id", "tree_path", "stage", "curriculum", "status"):
                        continue
                    old = cur.get(k)
                    if prefer_new and v not in (None, "", [], 0, "active"):
                        cur[k] = v
                    elif not old and v:
                        cur[k] = v
                    elif isinstance(old, list) and isinstance(v, list) and len(v) > len(old):
                        cur[k] = v
                if prefer_new:
                    cur["tree_path"] = rel_s
                    cur["stage"] = rec["stage"]
                    cur["curriculum"] = rec["curriculum"]

    # 统一 status：树里没有显式 status 的节点保持 placeholder（与历史口径一致）
    for nid, rec in nodes.items():
        rec["status"] = status_by_id.get(nid, "placeholder")
    # 统一两个路径口径（历史前端各读一个）
    for nid, rec in nodes.items():
        cands = tree_paths[nid]
        cn = [p for p in cands if p.startswith("cn/")]
        rec["graph_path"] = cn[0] if cn else rec["tree_path"]
        km_path = [p for p in cands if p.startswith("cn-unified/")]
        rec["km_tree_path"] = km_path[0] if km_path else rec["tree_path"]
        rec["tree_path"] = rec["km_tree_path"]   # knowledge-map-data.json 口径
        rec.pop("km_tree_path", None)

    # ── 2. 统一关系表 ───────────────────────────────────────────
    overlay_src = j(D / "node-enrichment-overlay.json", {}) or {}
    overlay_nodes = overlay_src.get("nodes", {}) or {}
    strength_map: dict[tuple[str, str], str] = {}
    for tid, ov in overlay_nodes.items():
        for pr in ov.get("prereqs_enriched") or []:
            if pr.get("id"):
                strength_map[(tid, pr["id"])] = pr.get("strength") or "soft"

    edge_set: set[tuple[str, str, str, str]] = set()   # (source, target, type, strength)
    for nid, rec in nodes.items():
        for pre in rec["prerequisites"]:
            if pre and pre != nid:
                edge_set.add((pre, nid, "prerequisite", strength_map.get((nid, pre), "hard")))
        for ext in rec["extends"]:
            if ext and ext != nid:
                edge_set.add((nid, ext, "extends", "soft"))
        for par in rec["parallel"]:
            if par and par != nid:
                edge_set.add((nid, par, "related", "soft"))
                edge_set.add((par, nid, "related", "soft"))
    for bridge_file in ("stage-bridges.json", "university-bridges.json"):
        payload = j(D / bridge_file, {}) or {}
        for item in payload.get("bridges") or []:
            if "target" in item and "sources" in item:
                for src in item["sources"]:
                    edge_set.add((src, item["target"], "bridge", "hard"))
            elif "source" in item and "target" in item:
                edge_set.add((item["source"], item["target"], "bridge", "hard"))

    ids = set(nodes)
    edges = sorted((s, t, ty, st) for s, t, ty, st in edge_set
                   if s in ids and t in ids and s != t)
    # 去重（同 source/target 保留优先级：prerequisite > bridge > extends > related）
    prio = {"prerequisite": 0, "bridge": 1, "extends": 2, "related": 3}
    dedup: dict[tuple[str, str], tuple[str, str]] = {}
    for s, t, ty, st in edges:
        k = (s, t)
        if k not in dedup or prio[ty] < prio[dedup[k][0]]:
            dedup[k] = (ty, st)
    edges_final = [{"source": s, "target": t, "type": ty, "strength": st}
                   for (s, t), (ty, st) in sorted(dedup.items())]

    prereq_by: dict[str, list[str]] = defaultdict(list)
    next_by: dict[str, list[str]] = defaultdict(list)
    related_by: dict[str, list[str]] = defaultdict(list)
    for e in edges_final:
        if e["type"] == "prerequisite":
            prereq_by[e["target"]].append(e["source"])
            next_by[e["source"]].append(e["target"])
        elif e["type"] == "extends":
            next_by[e["source"]].append(e["target"])
        elif e["type"] == "related":
            related_by[e["source"]].append(e["target"])
    for nid in nodes:
        nodes[nid]["prerequisites"] = sorted(set(prereq_by.get(nid, [])))
        nodes[nid]["next_steps"] = sorted(set(next_by.get(nid, [])))
        nodes[nid]["related_nodes"] = sorted(set(related_by.get(nid, [])))

    # ── 3. 合并历史人工内容（按 ID 保留，不编造） ─────────────────
    idx_src = j(D / "node-index.json", {}) or {}
    idx_old = idx_src.get("nodes", {}) or {}
    sel_src = j(D / "nodes-selector.json", []) or []
    sel_old = {s["id"]: s for s in sel_src} if isinstance(sel_src, list) else {}
    labels_src = j(D / "knowledge-map-domain-labels.json", {}) or {}
    labels = dict(labels_src.get("labels") or {})

    # ── 4. 输出 canonical ────────────────────────────────────────
    by_subject = Counter(n["subject"] for n in nodes.values())
    by_grade = Counter(str(n["grade"]) for n in nodes.values())
    by_stage = Counter(n["stage"] for n in nodes.values())
    meta = {
        "name": "TeachAny canonical knowledge layer",
        "generated_at": now(),
        "authoritative": "data/trees/**/*.json",
        "policy": "所有派生文件由本层统一生成；关系字段由统一边表反向补齐；历史人工内容按 ID 合并保留",
        "counts": {
            "tree_files": tree_files, "nodes": len(nodes), "edges": len(edges_final),
            "by_stage": dict(by_stage),
            "nodes_with_prereq": sum(1 for n in nodes.values() if n["prerequisites"]),
            "nodes_with_next": sum(1 for n in nodes.values() if n["next_steps"]),
            "nodes_with_related": sum(1 for n in nodes.values() if n["related_nodes"]),
            "edge_types": dict(Counter(e["type"] for e in edges_final)),
        },
    }
    canonical = {"meta": meta, "nodes": nodes, "edges": edges_final}

    outputs: dict[Path, object] = {}
    out_canonical = D / "unified" / "knowledge-layer.json"
    outputs[out_canonical] = canonical

    # 4a. knowledge-map-data.json（兼容视图）
    km_nodes = []
    for n in sorted(nodes.values(), key=lambda x: (x["subject"], x["grade"], x["id"])):
        km_nodes.append({k: n.get(k) for k in (
            "id", "name", "name_en", "subject", "grade", "domain", "difficulty",
            "definition", "skills", "stage", "curriculum", "tree_path")})
    outputs[D / "knowledge-map-data.json"] = {
        "nodes": km_nodes,
        "edges": [{"source": e["source"], "target": e["target"]} for e in edges_final],
        "stats": {
            "generated_at": now(), "totalNodes": len(km_nodes), "totalEdges": len(edges_final),
            "cnUnifiedNodes": sum(1 for n in km_nodes if n["curriculum"] == "cn-unified"),
            "internationalNodes": sum(1 for n in km_nodes if n["curriculum"] in INTL_CURRICULA),
            "stageBridgeEdges": sum(1 for e in edges_final if e["type"] == "bridge"),
            "universityBridgeEdges": 0, "sciElementaryNodes": 0, "sciCrossEdges": 0,
            "subjects": sorted(by_subject.keys()), "bySubject": dict(by_subject.most_common()),
            "byGrade": dict(sorted(by_grade.items(), key=lambda kv: int(kv[0]) if kv[0].isdigit() else 99)),
            "edgeTypes": dict(Counter(e["type"] for e in edges_final)),
        },
    }

    # 4b. nodes-metadata.json（PBL 候选池；graph_path 必须保留 cn/ 前缀）
    meta_nodes = []
    for n in sorted(nodes.values(), key=lambda x: x["id"]):
        meta_nodes.append({
            "id": n["id"], "name": n["name"], "subject": n["subject"],
            "domain": n["domain"], "grade": n["grade"], "graph_path": n["graph_path"],
            "definition": n["definition"], "prerequisites": n["prerequisites"],
            "next_steps": n["next_steps"], "related_nodes": n["related_nodes"],
            "key_concepts": n["key_concepts"], "difficulty": n["difficulty"],
            "courses": n["courses"], "status": n["status"],
        })
    outputs[D / "nodes-metadata.json"] = {
        "version": "2.0", "generated_at": now(),
        "source": "data/trees/**/*.json (authoritative) · build-knowledge-layer.py",
        "stats": {"total_graphs": tree_files, "total_nodes": len(meta_nodes),
                  "by_subject": dict(by_subject.most_common()),
                  "by_grade": dict(by_grade.most_common()),
                  "by_domain": dict(Counter(n["domain"] for n in meta_nodes).most_common())},
        "nodes": meta_nodes,
    }

    # 4c. nodes-selector.json（保留历史体系标签，修正身份字段）
    selector = []
    for n in sorted(nodes.values(), key=lambda x: x["id"]):
        old = sel_old.get(n["id"], {})
        selector.append({
            "id": n["id"], "name": n["name"], "subject": n["subject"],
            "grade": n["grade"], "domain": n["domain"],
            "system": old.get("system") or ("cn-unified" if n["curriculum"] == "cn-unified" else n["curriculum"]),
            "curriculumLabel": old.get("curriculumLabel") or "中国课标",
            "gradeLabel": old.get("gradeLabel") or ("通识" if n["grade"] == 0 else f"{n['grade']}年级"),
            "treePath": old.get("treePath") or n["tree_path"],
        })
    outputs[D / "nodes-selector.json"] = selector

    # 4d. node-index.json（完整 9679 条，修死 ID，保留历史 md/hero）
    idx_nodes = {}
    for n in sorted(nodes.values(), key=lambda x: x["id"]):
        old = idx_old.get(n["id"], {})
        idx_nodes[n["id"]] = {
            "node_id": n["id"], "name_zh": old.get("name_zh") or n["name"],
            "name_en": old.get("name_en") or n["name_en"],
            "domain": old.get("domain") or n["domain"],
            "curriculum": old.get("curriculum") or n["curriculum"],
            "stage": old.get("stage") or n["stage"],
            "subject": old.get("subject") or n["subject"],
            "tree_path": old.get("tree_path") or n["graph_path"],
            "courses": n["courses"],
            "md_status": old.get("md_status") or "none",
            "md_path": old.get("md_path"),
            "prereq_ids": n["prerequisites"], "next_ids": n["next_steps"],
            "hero_image": old.get("hero_image"),
        }
    outputs[D / "node-index.json"] = {
        "_meta": {
            "version": "2.0",
            "description": "由 build-knowledge-layer.py 从 canonical 全量重建；死 ID 已剔除，关系与 metadata 一致",
            "total_nodes": len(idx_nodes),
            "with_md": sum(1 for v in idx_nodes.values() if v.get("md_path")),
            "with_hero": sum(1 for v in idx_nodes.values() if v.get("hero_image")),
            "with_prereq": sum(1 for v in idx_nodes.values() if v["prereq_ids"]),
        },
        "nodes": idx_nodes,
    }

    # 4e. knowledge-map-domain-labels.json
    for n in nodes.values():
        if n["domain"] and n["domain"] not in labels:
            labels[n["domain"]] = n["domain"]
    outputs[D / "knowledge-map-domain-labels.json"] = {
        "version": "1.0", "generated_at": now(), "count": len(labels), "labels": labels,
    }

    # 4f. node-enrichment-overlay.json：保留历史人工内容，只刷新关系强度
    ov_out = {}
    hard = soft = 0
    for tid, ov in overlay_nodes.items():
        if tid not in nodes:
            continue
        existing = {p.get("id"): p for p in ov.get("prereqs_enriched") or []}
        enriched = []
        for pid in nodes[tid]["prerequisites"]:
            src = existing.get(pid, {})
            st = strength_map.get((tid, pid), src.get("strength") or "hard")
            hard += st == "hard"
            soft += st == "soft"
            enriched.append({
                "id": pid, "strength": st,
                "reason": src.get("reason", ""), "evidence": src.get("evidence", ""),
                "assessment": src.get("assessment", ""),
            })
        o = dict(ov)
        o["prereqs_enriched"] = enriched
        ov_out[tid] = o
    outputs[D / "node-enrichment-overlay.json"] = {
        "version": "1.0.0", "generated_at": now(),
        "source": overlay_src.get("source", "teachany-cn-trees+seed"),
        "policy": overlay_src.get("policy", "overlay-only; does-not-modify-cn-trees"),
        "stats": {"nodes": len(ov_out), "hard_edges": hard, "soft_edges": soft,
                  "nodes_with_misconceptions": len(ov_out),
                  "seed_nodes": (overlay_src.get("stats") or {}).get("seed_nodes", 0)},
        "nodes": ov_out,
    }

    # ── 5. 写入 ─────────────────────────────────────────────────
    print(json.dumps(meta["counts"], ensure_ascii=False, indent=2))
    if args.dry_run:
        print("\n[dry-run] 未写入任何文件")
        return 0
    for path, payload in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  ✅ {path.relative_to(ROOT)}  {path.stat().st_size/1024:.0f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
