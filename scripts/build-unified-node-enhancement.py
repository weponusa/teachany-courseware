#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
构建「统一节点增强索引」—— 把散在多套图谱里的同一节点收敛成一条按 ID 的记录，
供 PBL 拆解与各页面统一消费。目标：PBL 拆解更可靠。

不修改任何现有权威/派生文件，不跑 rebuild-index.py，不导入题库。

输入（全部只读）：
  data/trees/**/*.json                          权威源：身份、prerequisites、courses、curriculum_points、教材章节
  data/knowledge-map-data.json                  全局图：subject/stage/domain/curriculum/tree_path + edges
  data/nodes-metadata.json                      definition/key_concepts/status/graph_path
  data/nodes-selector.json                      curriculumLabel/gradeLabel/system
  data/node-enrichment-overlay.json             prereqs_enriched（hard/soft，仅取强度，不取 reason 原文）
  data/pbl/node-embeddings.json                 向量覆盖标记
  pbl-map/data/cn-k12-nodes.json               PBL Map 覆盖标记
  data/external/cn-math-taxonomy/coarse-enhancement.json   外部投影：候选粗边、课标编号、教材章节、能力入口

输出：
  data/unified/node-enhancement.json           canonical（按 ID 索引，PBL 与知识地图共用）
  data/external/cn-math-taxonomy/coarse-enhancement.json   由 canonical 派生的兼容视图（knowledge-map.html 零改动）

关系模型（关键修复）：
  PBL 运行时 _loadKnowledgeGraph() 会用全局图节点的 base.prerequisites=[] 覆盖掉
  树/metadata 里非空的 prerequisites，导致 994 个 CN 节点仅 5 个有先修。
  本索引把「树 prerequisites + 全局图边 + overlay hard/soft」统一为权威先修，
  「外部投影边」单列为 candidate_prereqs（带 support，标 candidate，绝不混入权威）。

用法：python3 scripts/build-unified-node-enhancement.py
"""
from __future__ import annotations

import glob
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
OUT = D / "unified" / "node-enhancement.json"
COARSE = D / "external" / "cn-math-taxonomy" / "coarse-enhancement.json"


def j(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    km = j(D / "knowledge-map-data.json")
    meta = j(D / "nodes-metadata.json")
    selector = j(D / "nodes-selector.json")
    overlay = j(D / "node-enrichment-overlay.json")
    coarse = j(COARSE)

    sel_list = selector["nodes"] if isinstance(selector, dict) and "nodes" in selector else selector
    sel_by_id = {n["id"]: n for n in sel_list} if isinstance(sel_list, list) else dict(sel_list)
    meta_by_id = {n["id"]: n for n in meta["nodes"]}
    ov_by_id = overlay.get("nodes", {})
    emb_ids = {n["id"] for n in j(D / "pbl" / "node-embeddings.json")["nodes"]}
    pblmap_ids = {n["id"] for n in j(ROOT / "pbl-map" / "data" / "cn-k12-nodes.json")["nodes"]}

    # ── 1. 权威源：树节点 ────────────────────────────────────────
    tree_by_id: dict[str, dict] = {}
    tree_files = 0
    for f in sorted(glob.glob(str(D / "trees" / "**" / "*.json"), recursive=True)):
        p = Path(f)
        try:
            t = j(p)
        except Exception:
            continue
        if not isinstance(t, dict) or "domains" not in t:
            continue
        tree_files += 1
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        subject = t.get("subject", "")
        for dom in t["domains"]:
            for n in dom.get("nodes", []):
                nid = n.get("id")
                if not nid:
                    continue
                rec = dict(n)
                rec["subject"] = n.get("subject") or subject
                rec["domain"] = n.get("domain") or dom.get("name") or dom.get("id") or ""
                rec["tree_path"] = rel
                # 同一 ID 在 cn 三学段树与 cn-unified 核心树重复；优先保留 cn/ 三学段版本
                if nid not in tree_by_id or (rel.startswith("data/trees/cn/") and "/cn-unified/" not in rel):
                    tree_by_id[nid] = rec

    # ── 2. 统一身份：以全局图节点为全集 ──────────────────────────
    all_ids = set(n["id"] for n in km["nodes"]) | set(meta_by_id)
    records: dict[str, dict] = {}
    for n in km["nodes"]:
        nid = n["id"]
        t = tree_by_id.get(nid, {})
        m = meta_by_id.get(nid, {})
        s = sel_by_id.get(nid, {})
        records[nid] = {
            "id": nid,
            "name": t.get("name") or n.get("name") or m.get("name") or nid,
            "name_en": n.get("name_en") or t.get("name_en") or "",
            "subject": n.get("subject") or t.get("subject") or m.get("subject") or "",
            "stage": n.get("stage") or t.get("stage") or s.get("system") or "",
            "grade": n.get("grade") if n.get("grade") is not None else (t.get("grade") or m.get("grade") or 0),
            "domain": n.get("domain") or t.get("domain") or m.get("domain") or "",
            "curriculum": n.get("curriculum") or "",
            "tree_path": n.get("tree_path") or t.get("tree_path") or m.get("graph_path") or "",
            "curriculum_label": s.get("curriculumLabel") or "",
            "grade_label": s.get("gradeLabel") or "",
            "definition": n.get("definition") or m.get("definition") or t.get("definition") or "",
            "key_concepts": m.get("key_concepts") or t.get("key_concepts") or [],
            "courses": t.get("courses") or m.get("courses") or [],
            "curriculum_points": t.get("curriculum_points") or n.get("curriculum_points") or [],
            "textbook_chapter": t.get("textbook_chapter") or "",
            "textbook_semester": t.get("textbook_semester") or "",
            "status": m.get("status") or t.get("status") or "",
            "skills": n.get("skills") or t.get("skills") or [],
        }
    for nid in all_ids - set(records):   # 12 个 ext-* 只在 metadata 里
        m = meta_by_id[nid]
        records[nid] = {
            "id": nid, "name": m.get("name") or nid, "name_en": "",
            "subject": m.get("subject") or "", "stage": "", "grade": m.get("grade") or 0,
            "domain": m.get("domain") or "", "curriculum": "", "tree_path": m.get("graph_path") or "",
            "curriculum_label": "", "grade_label": "",
            "definition": m.get("definition") or "", "key_concepts": m.get("key_concepts") or [],
            "courses": m.get("courses") or [], "curriculum_points": [], "textbook_chapter": "",
            "textbook_semester": "", "status": m.get("status") or "", "skills": [],
        }

    # ── 3. 统一关系：权威先修 + 反向 next_steps ───────────────────
    auth: dict[str, dict[str, dict]] = defaultdict(dict)   # target -> {prereqId: detail}
    origin_stats = Counter()

    def add_auth(target: str, src: str, strength: str, origin: str):
        if target not in records or src not in records or src == target:
            return
        d = auth[target].setdefault(src, {"id": src, "strength": strength, "origins": []})
        if origin not in d["origins"]:
            d["origins"].append(origin)
            origin_stats[origin] += 1
        if strength == "hard":
            d["strength"] = "hard"

    for nid, t in tree_by_id.items():
        for p in t.get("prerequisites") or []:
            add_auth(nid, p, "hard", "tree")
        for p in t.get("extends") or []:
            add_auth(nid, p, "soft", "tree-extends")
    for e in km["edges"]:
        add_auth(e["target"], e["source"], "hard", "graph")   # 全局图 source=先修
    for nid, ov in ov_by_id.items():
        for pr in ov.get("prereqs_enriched") or []:
            pid = pr.get("id")
            if pid:
                add_auth(nid, pid, pr.get("strength") or "soft", "overlay")

    # 外部投影候选边：单列，绝不混入权威
    candidate: dict[str, list[dict]] = defaultdict(list)
    for e in coarse.get("edges", []):
        candidate[e["target"]].append({
            "id": e["source"],
            "strength": e.get("strength") or "soft",
            "support": e.get("support_count", 1),
            "origin": "projected",
            "review": "candidate",
        })

    # ── 4. 外部内容加厚（只取编号/章节/统计/入口，不搬原文） ──────
    coarse_by_id = {n["id"]: n for n in coarse.get("nodes", [])}
    enhanced = 0
    for nid, rec in records.items():
        c = coarse_by_id.get(nid)
        rec["prerequisites"] = list(auth[nid].keys())
        rec["prereq_details"] = list(auth[nid].values())
        rec["candidate_prereqs"] = candidate.get(nid, [])
        rec["standards"] = sorted({s for s in (c or {}).get("standard_ids", [])})
        rec["chapters"] = (c or {}).get("chapters", [])[:20]
        if not rec["chapters"] and rec["textbook_chapter"]:
            rec["chapters"] = [rec["textbook_chapter"]]
        rec["external_capabilities"] = (c or {}).get("external_capabilities") or None
        rec["coverage_count"] = (c or {}).get("coverage_count", 0)
        rec["mastery_criteria_count"] = (c or {}).get("mastery_criteria_count", 0)
        rec["diagnostic_question_count"] = (c or {}).get("diagnostic_question_count", 0)
        rec["quality"] = {
            "status": rec["status"] or "unknown",
            "has_embedding": nid in emb_ids,
            "in_pbl_map": nid in pblmap_ids,
            "review_status": "authoritative" if rec["prerequisites"] else "no_relation",
            "sources": sorted(set(rec["prereq_details"] and [o for d in rec["prereq_details"] for o in d["origins"]] or [])),
        }
        # 无权威先修的节点：多数是学科/学段入口（root，正常），少数带外部投影建议边
        if rec["prerequisites"]:
            rec["gap_status"] = "ok"
        else:
            sug = [c for c in rec["candidate_prereqs"] if (c.get("support") or 0) >= 2]
            if sug:
                rec["gap_status"] = "candidate_suggestion"
                for c in rec["candidate_prereqs"]:
                    if (c.get("support") or 0) >= 2:
                        c["suggested"] = True
            else:
                rec["gap_status"] = "root"
        if nid not in pblmap_ids and rec["grade"] == 0:
            rec["quality"]["scope_note"] = "cross_grade"
        if c:
            enhanced += 1

    # 反向 next_steps（当前 meta 里只有 42 个节点有值）
    nexts: dict[str, list[str]] = defaultdict(list)
    for nid, rec in records.items():
        for p in rec["prerequisites"]:
            nexts[p].append(nid)
    for nid, rec in records.items():
        rec["next_steps"] = sorted(set(nexts.get(nid, [])))

    # ── 5. 输出 ──────────────────────────────────────────────────
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    cn_k12 = [r for r in records.values()
              if r["curriculum"] == "cn-unified" and r["stage"] in ("elementary", "middle", "high")]
    gaps = {
        "cn_k12_without_embedding": sorted(r["id"] for r in cn_k12 if not r["quality"]["has_embedding"]),
        "cn_k12_not_in_pbl_map": sorted(r["id"] for r in cn_k12 if not r["quality"]["in_pbl_map"]),
        "cn_k12_without_prereq": sorted(r["id"] for r in cn_k12 if not r["prerequisites"]),
        "placeholder_nodes": sum(1 for r in records.values() if r["status"] == "placeholder"),
    }
    meta_out = {
        "name": "TeachAny 统一节点增强索引",
        "generated_at": now,
        "purpose": "把多套图谱的同一节点收敛为一条记录，供 PBL 拆解与各页面统一消费",
        "authoritative": "data/trees/**（身份与先修）、knowledge-map-data.json（边与大学节点）、nodes-metadata.json",
        "external": "cn-math-taxonomy 粗粒度投影（仅候选关系与编号/章节/入口，不搬题干与描述原文）",
        "license_note": "外部数据 CC BY-NC 4.0；本站只存课标编号、教材章节、覆盖统计与用户主动调用的深链",
        "relation_policy": "prerequisites 为权威先修（tree/graph/overlay 合并）；candidate_prereqs 为外部投影候选，带 support 且标 review=candidate，不得直接当权威边",
        "counts": {
            "tree_files": tree_files,
            "total_nodes": len(records),
            "cn_k12_nodes": len(cn_k12),
            "externally_enhanced_nodes": enhanced,
            "authoritative_prereq_links": sum(len(r["prerequisites"]) for r in records.values()),
            "candidate_prereq_links": sum(len(r["candidate_prereqs"]) for r in records.values()),
            "nodes_with_prereq": sum(1 for r in records.values() if r["prerequisites"]),
            "cn_k12_with_prereq": sum(1 for r in cn_k12 if r["prerequisites"]),
            "nodes_with_next_steps": sum(1 for r in records.values() if r["next_steps"]),
            "origin_links": dict(origin_stats),
            "gaps": {k: (len(v) if isinstance(v, list) else v) for k, v in gaps.items()},
        },
        "gaps": gaps,
    }
    # 瘦身：本站只存「关系 + 增强 + 质量 + 身份」；definition/curriculum_points 等
    # 长文本由 PBL 接线时从课标树保留（修复 _loadKnowledgeGraph 的覆盖），不在此重复存储。
    # curriculum_points 保留给 rich 节点：PBL 的 CN 候选池来自 nodes-metadata.json，
    # 该源没有课标要点字段，LLM 提示词因而拿不到依据；统一索引从权威树补齐它。
    drop_all = ["definition", "key_concepts", "courses", "skills",
                "textbook_chapter", "textbook_semester", "curriculum_label", "grade_label"]
    drop_lite = ["prereq_details", "candidate_prereqs", "chapters", "standards", "next_steps",
                 "curriculum_points", "coverage_count", "mastery_criteria_count", "diagnostic_question_count"]
    slimmer = 0
    for r in records.values():
        for k in drop_all:
            r.pop(k, None)
        rich = (r["stage"] in ("elementary", "middle", "high")
                or r["curriculum"] in ("ap", "ib", "cambridge", "us")
                or r["external_capabilities"])
        if not rich:
            for k in drop_lite:
                r.pop(k, None)
            slimmer += 1
    meta_out["counts"]["slimmed_lite_nodes"] = slimmer
    meta_out["counts"]["cn_k12_gap_classification"] = dict(Counter(
        r.get("gap_status", "ok") for r in records.values()
        if r["stage"] in ("elementary", "middle", "high") and r["curriculum"] == "cn-unified"))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"meta": meta_out, "nodes": records},
                              ensure_ascii=False, separators=(",", ":")),
                   encoding="utf-8")

    # 派生兼容视图：knowledge-map.html 继续读 coarse-enhancement.json，但数据由 canonical 生成
    coarse_nodes = []
    for r in records.values():
        if not r["external_capabilities"]:
            continue
        coarse_nodes.append({
            "id": r["id"], "name": r["name"], "subject": r["subject"],
            "grade": r["grade"], "stage": r["stage"],
            "coverage_count": r["coverage_count"],
            "covered_topic_ids": [],  # 统一索引不重复存外部 ID 列表，保留字段兼容前端
            "standard_ids": r["standards"],
            "chapters": r["chapters"],
            "mastery_criteria_count": r["mastery_criteria_count"],
            "diagnostic_question_count": r["diagnostic_question_count"],
            "external_capabilities": r["external_capabilities"],
        })
    coarse_view = dict(coarse)
    coarse_view["nodes"] = coarse_nodes
    coarse_view["meta"] = dict(coarse.get("meta") or {})
    coarse_view["meta"]["derived_from"] = "data/unified/node-enhancement.json"
    coarse_view["meta"]["derived_at"] = now
    COARSE.write_text(json.dumps(coarse_view, ensure_ascii=False, indent=1), encoding="utf-8")

    # ── 6. PBL 专用精简视图（首屏只加载拆解真正需要的节点） ───────
    pbl_view = {}
    for nid, r in records.items():
        rich = (r["stage"] in ("elementary", "middle", "high")
                or r["curriculum"] in ("ap", "ib", "cambridge", "us")
                or r["external_capabilities"])
        if rich:
            pbl_view[nid] = r
        else:
            # 大学/placeholder 节点：PBL 关系靠 graphNeighbors，这里只保留权威先修修复
            pbl_view[nid] = {"id": nid, "prerequisites": r.get("prerequisites", []),
                             "gap_status": r.get("gap_status", "ok"), "quality": r.get("quality")}
    PBL_VIEW = OUT.parent / "node-enhancement-pbl.json"
    PBL_VIEW.write_text(json.dumps({"meta": {**meta_out, "view": "PBL 精简视图（由 canonical 派生）"},
                                    "nodes": pbl_view}, ensure_ascii=False, separators=(",", ":")),
                        encoding="utf-8")

    # ── 7. 候选关系审核表（support>=3，供一线教师逐条核对） ───────
    import csv
    review = []
    for e in coarse.get("edges", []):
        if e.get("support_count", 0) < 3:
            continue
        src, tgt = records.get(e["source"]), records.get(e["target"])
        review.append({
            "source_id": e["source"], "source_name": (src or {}).get("name", ""),
            "target_id": e["target"], "target_name": (tgt or {}).get("name", ""),
            "subject": (tgt or {}).get("subject", ""), "grade": (tgt or {}).get("grade", ""),
            "strength": e.get("strength", ""), "support": e["support_count"],
            "is_new": e.get("is_new", False),
            "supporting_external_edges": ";".join(e.get("supporting_edges", [])[:8]),
            "suggested_action": "待教师审核",
        })
    review.sort(key=lambda r: (-r["support"], r["strength"] != "hard"))
    csv_path = OUT.parent / "review-candidates.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(review[0].keys()))
        w.writeheader(); w.writerows(review)
    by_subject = Counter(r["subject"] for r in review)
    md = ["# 候选粗粒度先修关系 · 教师审核表", "",
          f"共 {len(review)} 条（support >= 3，hard 优先）。完整可编辑版见 review-candidates.csv。", "",
          "来源：cn-math-taxonomy 细粒度先修边投影；AI 判断，未经教师审核，不得直接作为权威先修边。", "",
          "| 学科 | 条数 |", "|---|---:|"]
    md += [f"| {k} | {v} |" for k, v in by_subject.most_common()]
    md += ["", "## 前 30 条（按支持度降序）", "",
           "| 先修 | → | 后继 | 学科 | 强度 | 支持度 | 新增 | 外部细边 |", "|---|---|---|---|---|---|---:|---|---|"]
    for r in review[:30]:
        md.append(f"| {r['source_name']} | → | {r['target_name']} | {r['subject']} | "
                  f"{r['strength']} | {r['support']} | {'是' if r['is_new'] else '否'} | "
                  f"{r['supporting_external_edges'][:60]} |")
    (OUT.parent / "review-candidates.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(json.dumps(meta_out["counts"], ensure_ascii=False, indent=2))
    print("PBL 视图:", PBL_VIEW, f"{PBL_VIEW.stat().st_size/1024:.0f} KB")
    print("审核表:", csv_path, len(review), "条")
    print("\n输出:", OUT, f"{OUT.stat().st_size/1024:.0f} KB")
    print("派生:", COARSE, f"{COARSE.stat().st_size/1024:.0f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
