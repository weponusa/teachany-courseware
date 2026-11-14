#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""跨文件一致性校验：确保 6 份派生文件与 canonical 完全对齐。"""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"

def j(p): return json.loads((D / p).read_text(encoding="utf-8")) if (D / p).exists() else json.loads((ROOT / p).read_text(encoding="utf-8"))

def main():
    errs, warns = [], []
    canon = j("unified/knowledge-layer.json")
    km = j("knowledge-map-data.json")
    meta = j("nodes-metadata.json")
    sel = j("nodes-selector.json")
    idx = j("node-index.json")
    ov = j("node-enrichment-overlay.json")
    labels = j("knowledge-map-domain-labels.json")

    cids = set(canon["nodes"])
    km_ids = {n["id"] for n in km["nodes"]}
    m_ids = {n["id"] for n in meta["nodes"]}
    s_ids = {n["id"] for n in sel}
    i_ids = set(idx["nodes"])
    print("节点数 canonical/km/metadata/selector/index:",
          len(cids), len(km_ids), len(m_ids), len(s_ids), len(i_ids))
    for name, s in (("km", km_ids), ("metadata", m_ids), ("selector", s_ids), ("index", i_ids)):
        if s != cids:
            errs.append(f"{name} ID 集合与 canonical 不一致: 多 {len(s-cids)} 少 {len(cids-s)}")

    # 边端点
    dangling = [e for e in km["edges"] if e["source"] not in km_ids or e["target"] not in km_ids]
    if dangling: errs.append(f"km 悬空边 {len(dangling)} 条")
    loops = [e for e in km["edges"] if e["source"] == e["target"]]
    if loops: errs.append(f"km 自环 {len(loops)} 条")
    pairs = [(e["source"], e["target"]) for e in km["edges"]]
    if len(pairs) != len(set(pairs)): errs.append("km 存在重复边")

    # metadata 关系引用
    bad_ref = 0
    for n in meta["nodes"]:
        for f in ("prerequisites", "next_steps", "related_nodes"):
            for r in n.get(f) or []:
                if r not in m_ids: bad_ref += 1
    if bad_ref: errs.append(f"metadata 关系引用悬空 {bad_ref} 处")

    # index 与 metadata 关系一致
    m_by = {n["id"]: n for n in meta["nodes"]}
    mismatch = 0
    for nid, v in idx["nodes"].items():
        if nid in m_by and (v.get("prereq_ids") or []) != (m_by[nid].get("prerequisites") or []):
            mismatch += 1
    if mismatch: errs.append(f"index.prereq_ids 与 metadata 不一致 {mismatch} 条")

    # selector 身份一致
    s_bad = 0
    for n in sel:
        m = m_by.get(n["id"])
        if m and (n["subject"], n["grade"], n["domain"]) != (m["subject"], m["grade"], m["domain"]):
            s_bad += 1
    if s_bad: errs.append(f"selector 与 metadata 身份不一致 {s_bad} 条")

    # overlay 节点有效
    ov_bad = [k for k in ov["nodes"] if k not in cids]
    if ov_bad: errs.append(f"overlay 死 ID {len(ov_bad)} 个")

    # PBL CN 候选池
    pbl_cn = [n for n in meta["nodes"] if str(n.get("graph_path") or "").startswith("cn/")]
    print("PBL CN 候选池(graph_path 以 cn/ 开头):", len(pbl_cn))
    if len(pbl_cn) < 900: errs.append("PBL CN 候选池异常缩小")

    # 统计对比
    stats = {
        "canonical_edges": len(canon["edges"]), "km_edges": len(km["edges"]),
        "metadata_with_prereq": sum(1 for n in meta["nodes"] if n.get("prerequisites")),
        "metadata_with_next": sum(1 for n in meta["nodes"] if n.get("next_steps")),
        "metadata_with_related": sum(1 for n in meta["nodes"] if n.get("related_nodes")),
        "index_total": len(idx["nodes"]), "index_with_prereq": sum(1 for v in idx["nodes"].values() if v.get("prereq_ids")),
        "labels": len(labels.get("labels", {})), "overlay_nodes": len(ov["nodes"]),
        "domain_label_coverage": sum(1 for n in km["nodes"] if n["domain"] in labels.get("labels", {})) ,
        "km_nodes": len(km["nodes"]),
    }
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    if errs:
        print("\n❌ 校验失败:"); [print("  -", e) for e in errs]
        return 1
    print("\n✅ 全部一致性校验通过")
    return 0

if __name__ == "__main__":
    sys.exit(main())
