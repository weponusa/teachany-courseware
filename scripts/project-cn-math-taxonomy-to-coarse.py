#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 cn-math-taxonomy 的细粒度数据「投影」到 TeachAny 原有的粗粒度骨架上。

与 import-cn-math-taxonomy.py（细粒度 overlay 图层）不同，本脚本：
- **不新增任何图谱节点**：输出仍以本地 940 个 K12 课标粗节点为键；
- **不搬内容**：只保留结构性事实（课标编号、教材章节、覆盖统计）与深链入口，
  不复制 description / mastery_criteria / reason / 题干等 NC 保护内容；
- **关系投影**：5132 条细粒度先修边按归属粗点聚合为粗粒度先修边，带支持度；
- **能力路由**：每个粗点带外部服务的 explore / diagnose 深链，未来由用户或商业应用
  自行调用对方的「细化图谱 / 调取习题」能力，TeachAny 只做入口。

输出：data/external/cn-math-taxonomy/coarse-enhancement.json
用法：python3 scripts/project-cn-math-taxonomy-to-coarse.py
"""
from __future__ import annotations

import difflib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT.parent / "_research" / "cms-taxonomy"
OUT = ROOT / "data" / "external" / "cn-math-taxonomy" / "coarse-enhancement.json"

SUBJECT_MAP = {
    "math": "math", "english": "english", "chinese": "chinese",
    "physics": "physics", "chemistry": "chemistry", "biology": "biology",
    "history": "history", "geography": "geography", "science": "science",
    "morality": "politics",
}
ID_PREFIX_SUBJECT = {
    "cnm": "math", "cne": "english", "cnc": "chinese", "cnp": "physics",
    "cnd": "morality", "cns": "science", "cnk": "chemistry", "cnh": "history",
    "cnb": "biology", "cng": "geography",
}
GRADE_MAP = {13: 10, 14: 11, 15: 12, 16: 12}
EXPLORE = "https://math.pansgo.com/explore/?target="
DIAGNOSE = "https://math.pansgo.com/diagnose/?target="


def norm(s) -> str:
    return "".join(ch for ch in str(s or "").lower()
                   if ch.isalnum() or "\u4e00" <= ch <= "\u9fff")


def ext_subject(t) -> str:
    return t.get("subject") or ID_PREFIX_SUBJECT.get(t.get("id", "")[:3], "other")


def coarse_subject(t) -> str:
    return SUBJECT_MAP.get(ext_subject(t), "other")


def coarse_grade(t) -> int:
    g = int(t.get("grade") or 0)
    return GRADE_MAP.get(g, min(g, 12)) if g else 0


def main() -> int:
    km = json.loads((ROOT / "data" / "knowledge-map-data.json").read_text(encoding="utf-8"))
    coarse = [n for n in km["nodes"]
              if n.get("curriculum") == "cn-unified"
              and n.get("stage") in ("elementary", "middle", "high")]
    coarse_ids = {n["id"] for n in coarse}
    exact_index: dict[str, list[dict]] = defaultdict(list)
    bucket: dict[tuple[str, int], list[dict]] = defaultdict(list)
    for n in coarse:
        exact_index[norm(n.get("name"))].append(n)
        bucket[(n.get("subject"), int(n.get("grade") or 0))].append(n)

    topics = json.loads((SRC / "topics.json").read_text(encoding="utf-8"))
    deps = json.loads((SRC / "dependencies.json").read_text(encoding="utf-8"))

    def assign(t):
        """返回 (coarse_id, method, score)。宁可低置信也不留空，但会标注 method 供审核。"""
        subj, grade, key = coarse_subject(t), coarse_grade(t), norm(t.get("name"))
        exact = exact_index.get(key)
        if exact:
            same = [n for n in exact if n.get("subject") == subj] or exact
            return same[0]["id"], "exact", 1.0

        for grades, method in (
            ([grade], "bucket-grade"),
            ([g for g in (grade - 1, grade + 1) if 1 <= g <= 12], "bucket-near"),
            (list(range(1, 13)), "bucket-subject"),
        ):
            cands = []
            for g in grades:
                cands.extend(bucket.get((subj, g), []))
            best, score = None, 0.0
            for n in cands:
                nk = norm(n.get("name"))
                r = difflib.SequenceMatcher(None, key, nk).ratio()
                if key and nk and (key in nk or nk in key):
                    r = max(r, 0.72)
                if r > score:
                    best, score = n, r
            if best:
                return best["id"], method, round(score, 3)
        return None, "unassigned", 0.0

    owner: dict[str, str] = {}
    method_of: dict[str, str] = {}
    covered: dict[str, list[dict]] = defaultdict(list)   # coarse_id -> 细点
    for t in topics:
        cid, method, score = assign(t)
        owner[t["id"]] = cid
        method_of[t["id"]] = method
        if cid:
            covered[cid].append(t)

    # ── 关系投影 ────────────────────────────────────────────────
    local_edges = {(e["source"], e["target"]) for e in km["edges"]}
    proj: dict[tuple[str, str], dict] = {}
    skipped = Counter()
    for d in deps:
        a, b = owner.get(d["prerequisiteId"]), owner.get(d["topicId"])
        if not a or not b:
            skipped["unassigned_endpoint"] += 1
            continue
        if a == b:
            skipped["same_coarse_node"] += 1
            continue
        k = (a, b)
        if k not in proj:
            proj[k] = {"source": a, "target": b, "strength": "soft",
                       "support_count": 0, "supporting_edges": [],
                       "is_new": k not in local_edges}
        p = proj[k]
        p["support_count"] += 1
        p["supporting_edges"].append(f"{d['prerequisiteId']}>{d['topicId']}")
        if d.get("strength") == "hard":
            p["strength"] = "hard"
    edges_out = sorted(proj.values(), key=lambda x: -x["support_count"])

    # ── 内容增强（只保留结构性事实 + 入口，不搬原文） ──────────
    nodes_out = []
    for n in coarse:
        ts = covered.get(n["id"], [])
        if not ts:
            continue
        std_ids = sorted({s.get("id") for t in ts for s in (t.get("standards") or []) if s.get("id")})
        chapters = sorted({t.get("chapter") for t in ts if t.get("chapter")})
        nodes_out.append({
            "id": n["id"],
            "name": n.get("name"),
            "subject": n.get("subject"),
            "grade": n.get("grade"),
            "stage": n.get("stage"),
            "coverage_count": len(ts),
            "covered_topic_ids": [t["id"] for t in ts],
            "standard_ids": std_ids,
            "chapters": chapters[:20],
            "mastery_criteria_count": sum(len(t.get("mastery_criteria") or []) for t in ts),
            "diagnostic_question_count": sum(1 for t in ts if t.get("diagnostic_question")),
            "external_capabilities": {
                "provider": "cn-math-taxonomy",
                "license": "CC BY-NC 4.0",
                "access": "user-invoked",       # 用户/商业应用自行调用，本站不代理内容
                "refine_graph": EXPLORE + ts[0]["id"],
                "diagnose": DIAGNOSE + ts[0]["id"],
                "note": "细化图谱与习题由对方服务提供，本站仅保存入口与知识点编号",
            },
        })

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    methods = Counter(method_of.values())
    new_edges = [e for e in edges_out if e["is_new"]]
    meta = {
        "name": "粗粒度图谱增强（外部细粒度数据投影）",
        "generated_at": now,
        "source": "https://github.com/xiaoyang111222/cn-math-taxonomy",
        "license": "CC BY-NC 4.0（本站只存编号/章节/链接，不复制其描述、题干、理由原文）",
        "strategy": "保持本地原有粗粒度节点不变；细点按 学科+年级 归属到粗点，细边聚合为粗边；内容增强只留结构性事实与外部能力入口",
        "counts": {
            "local_coarse_nodes": len(coarse),
            "external_topics": len(topics),
            "external_edges": len(deps),
            "topics_assigned": sum(1 for v in owner.values() if v),
            "topics_unassigned": sum(1 for v in owner.values() if not v),
            "assign_methods": dict(methods),
            "coarse_nodes_enhanced": len(nodes_out),
            "projected_coarse_edges": len(edges_out),
            "projected_new_edges": len(new_edges),
            "projected_existing_edges": len(edges_out) - len(new_edges),
            "hard_edges": sum(1 for e in edges_out if e["strength"] == "hard"),
            "soft_edges": sum(1 for e in edges_out if e["strength"] == "soft"),
            "avg_support": round(sum(e["support_count"] for e in edges_out) / max(1, len(edges_out)), 2),
            "coarse_nodes_with_standard_ids": sum(1 for n in nodes_out if n["standard_ids"]),
            "coarse_nodes_with_chapters": sum(1 for n in nodes_out if n["chapters"]),
            "skipped_edges": dict(skipped),
        },
    }
    OUT.write_text(json.dumps({"meta": meta, "nodes": nodes_out, "edges": edges_out},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(meta["counts"], ensure_ascii=False, indent=2))
    print("\n输出:", OUT, f"{OUT.stat().st_size/1024:.0f} KB")
    print("样例粗边:", json.dumps(edges_out[0], ensure_ascii=False)[:400])
    print("样例粗点:", json.dumps(nodes_out[0], ensure_ascii=False)[:700])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
