#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 cn-math-taxonomy 的知识点 + 先修关系转换为 TeachAny 知识地图的细粒度 overlay 图层。

⚠️ **Phase 1 离线研究用，站点已不采用该方案**（2026-11-14 起改为「粗粒度骨架 + 外部能力路由」，
见 project-cn-math-taxonomy-to-coarse.py）。本脚本输出的是细粒度 overlay 素材，已移至
_research/cms-taxonomy/overlay-phase1/；**不要把输出放回 data/external/ 或随站点发布**。

只处理 topics / dependencies / standards，**不导入 questions.json（题库暂不动）**。
输出为独立 overlay 数据，不修改 data/trees/**、不触发 rebuild-index.py 派生链。

数据来源：https://github.com/xiaoyang111222/cn-math-taxonomy
许可证：CC BY-NC 4.0（见同目录 NOTICE.md）——仅用于本地非商业研究，未获单独授权前不得发布。

用法：
    python3 scripts/import-cn-math-taxonomy.py
    python3 scripts/import-cn-math-taxonomy.py --src /path/to/snapshot --out /path/to/output
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SRC = ROOT.parent / "_research" / "cms-taxonomy"
DEFAULT_OUT = ROOT / "data" / "external" / "cn-math-taxonomy"

# 外部 subject / ID 前缀 → TeachAny SUBJECT_CONFIG 的 key
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
# 外部 13–16 是高中选择性必修册次；本地 gradeRange 只到 12
GRADE_MAP = {13: 10, 14: 11, 15: 12, 16: 12}
LICENSE = "CC BY-NC 4.0 International"
SOURCE_URL = "https://github.com/xiaoyang111222/cn-math-taxonomy"


def norm(s: str) -> str:
    if not s:
        return ""
    return "".join(ch for ch in str(s).lower() if ch.isalnum() or "\u4e00" <= ch <= "\u9fff")


def external_subject(topic: dict) -> str:
    s = topic.get("subject")
    if s:
        return s
    return ID_PREFIX_SUBJECT.get(topic.get("id", "")[:3], "other")


def local_subject(topic: dict) -> str:
    return SUBJECT_MAP.get(external_subject(topic), "other")


def local_grade(topic: dict) -> int:
    g = int(topic.get("grade") or 0)
    return GRADE_MAP.get(g, min(g, 12)) if g else 0


def local_stage(grade: int) -> str:
    if grade <= 6:
        return "elementary"
    if grade <= 9:
        return "middle"
    return "high"


def tax_node_id(external_id: str) -> str:
    # 不用 ext-<hex>（rebuild-index.py 保留给 PBL 且会从正式树剔除）
    return "tax-" + external_id.replace("_", "-")


def upstream_sha() -> str:
    """取上游 main 的 commit sha，便于固定版本；网络失败时返回 unknown。"""
    try:
        req = urllib.request.Request(
            "https://api.github.com/repos/xiaoyang111222/cn-math-taxonomy/commits/main",
            headers={"User-Agent": "teachany-import", "Accept": "application/vnd.github+json"},
        )
        with urllib.request.urlopen(req, timeout=15) as f:
            return json.load(f)["sha"]
    except Exception:
        return "unknown"


def load_local_index():
    """本地图谱节点名称索引 + 按学科/年级的候选池。"""
    data = json.loads((ROOT / "data" / "knowledge-map-data.json").read_text(encoding="utf-8"))
    by_name: dict[str, list[dict]] = defaultdict(list)
    by_subject_grade: dict[tuple[str, int], list[dict]] = defaultdict(list)
    ids: set[str] = set()
    for n in data["nodes"]:
        ids.add(n["id"])
        by_name[norm(n.get("name"))].append(n)
        by_subject_grade[(n.get("subject"), int(n.get("grade") or 0))].append(n)
    existing_edges = {(e["source"], e["target"]) for e in data["edges"]}
    return data["nodes"], by_name, by_subject_grade, ids, existing_edges


def pick_parent(topic: dict, subj: str, grade: int,
                by_name, by_subject_grade) -> tuple[str | None, str, float]:
    """返回 (local_id, match_type, confidence)。"""
    key = norm(topic.get("name"))
    exact = by_name.get(key)
    if exact:
        # 同名优先取同学科的
        same = [n for n in exact if n.get("subject") == subj]
        n = (same or exact)[0]
        return n["id"], "equivalent", 1.0

    # 同学科、年级相近的候选，按名称相似度取最高
    cands = []
    for dg in range(max(1, grade - 2), min(12, grade + 2) + 1):
        cands.extend(by_subject_grade.get((subj, dg), []))
    if not cands:
        for (s, _g), nodes in by_subject_grade.items():
            if s == subj:
                cands.extend(nodes)
    best, score = None, 0.0
    for n in cands:
        nk = norm(n.get("name"))
        r = difflib.SequenceMatcher(None, key, nk).ratio()
        # 名称包含关系（如「有理数」⊂「有理数的运算」）比纯字面相似度可靠
        if key and nk and (key in nk or nk in key):
            r = max(r, 0.72)
        if r > score:
            best, score = n, r
    # 阈值过低会把「1到5各数的认识」误挂到「小数的初步认识」；宁可 unmapped 也不误导
    if best and score >= 0.45:
        return best["id"], "child_of", round(score, 3)
    return None, "unmapped", round(score, 3)


def has_cycle(edges: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """返回需要剔除的成环边（贪心：加入后成环则剔除）。"""
    graph: dict[str, set[str]] = defaultdict(set)
    kept: list[tuple[str, str]] = []

    def reachable(a: str, b: str, seen: set[str]) -> bool:
        if a == b:
            return True
        if a in seen:
            return False
        seen.add(a)
        return any(reachable(nxt, b, seen) for nxt in graph.get(a, ()))

    dropped = []
    for s, t in edges:
        if s == t or reachable(t, s, set()):
            dropped.append((s, t))
            continue
        graph[s].add(t)
        kept.append((s, t))
    return dropped


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, default=DEFAULT_SRC)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--all-subjects", action="store_true",
                    help="输出全部学科（默认也输出全部；此开关仅影响统计展示）")
    args = ap.parse_args()

    src: Path = args.src
    out: Path = args.out
    for f in ("topics.json", "dependencies.json", "cn-curriculum-standards.json"):
        if not (src / f).exists():
            print(f"❌ 缺少输入文件: {src / f}", file=sys.stderr)
            return 1
    out.mkdir(parents=True, exist_ok=True)

    topics = json.loads((src / "topics.json").read_text(encoding="utf-8"))
    deps = json.loads((src / "dependencies.json").read_text(encoding="utf-8"))
    standards = json.loads((src / "cn-curriculum-standards.json").read_text(encoding="utf-8"))

    local_nodes, by_name, by_subject_grade, local_ids, existing_edges = load_local_index()

    # ── 节点 ──────────────────────────────────────────────────────
    id_of: dict[str, str] = {}       # external_id -> 最终落到图谱里的 id
    mapping_rows = []
    overlay_nodes = []
    by_subject_count: Counter = Counter()

    for t in topics:
        eid = t["id"]
        subj = local_subject(t)
        grade = local_grade(t)
        parent_id, match_type, confidence = pick_parent(t, subj, grade, by_name, by_subject_grade)
        nid = parent_id if match_type == "equivalent" else tax_node_id(eid)
        id_of[eid] = nid
        by_subject_count[subj] += 1

        mapping_rows.append({
            "external_id": eid,
            "name": t.get("name"),
            "subject": subj,
            "external_grade": t.get("grade"),
            "local_grade": grade,
            "local_id": nid,
            "match_type": match_type,
            "confidence": confidence,
            "chapter": t.get("chapter"),
        })

        if match_type == "equivalent":
            # 精确同名：不新建节点，只在详情面板里挂细分信息
            overlay_nodes.append({
                "id": nid,
                "external_id": eid,
                "name": t.get("name"),
                "subject": subj,
                "grade": grade,
                "domain": t.get("domain"),
                "definition": t.get("description"),
                "external": True,
                "merged": True,           # 与本地节点共用 id，不进 nodes 数组
                "mastery_criteria": t.get("mastery_criteria") or [],
                "standards": t.get("standards") or [],
                "chapter": t.get("chapter"),
                "semester": t.get("semester"),
                "source": SOURCE_URL,
                "license": LICENSE,
            })
            continue

        overlay_nodes.append({
            "id": nid,
            "external_id": eid,
            "name": t.get("name"),
            "name_en": t.get("name_en") or "",
            "subject": subj,
            "grade": grade,
            "domain": t.get("domain") or "",
            "definition": t.get("description") or "",
            "stage": local_stage(grade),
            "curriculum": "external-cn-math-taxonomy",
            "tree_path": "external/cn-math-taxonomy",
            "parent_id": parent_id,
            "match_type": match_type,
            "confidence": confidence,
            "external_grade": t.get("grade"),
            "semester": t.get("semester"),
            "chapter": t.get("chapter"),
            "mastery_criteria": t.get("mastery_criteria") or [],
            "standards": t.get("standards") or [],
            "external": True,
            "source": SOURCE_URL,
            "license": LICENSE,
        })

    # 与本地 ID 冲突检查
    new_ids = [n["id"] for n in overlay_nodes if not n.get("merged")]
    conflicts = sorted(set(new_ids) & local_ids)
    if conflicts:
        print(f"❌ ID 冲突 {len(conflicts)} 个: {conflicts[:5]}", file=sys.stderr)
        return 1
    dup = [k for k, v in Counter(new_ids).items() if v > 1]
    if dup:
        print(f"❌ overlay 内部 ID 重复: {dup[:5]}", file=sys.stderr)
        return 1

    # ── 边 ────────────────────────────────────────────────────────
    overlay_edges = []
    skipped_self = skipped_dup = skipped_local = 0
    seen = set()
    pair_candidates = []
    for d in deps:
        s, t = id_of.get(d["prerequisiteId"]), id_of.get(d["topicId"])
        if not s or not t:
            continue
        if s == t:
            skipped_self += 1
            continue
        if (s, t) in seen:
            skipped_dup += 1
            continue
        seen.add((s, t))
        if (s, t) in existing_edges:
            skipped_local += 1
            continue
        pair_candidates.append((s, t))
        overlay_edges.append({
            "source": s,                       # 先修
            "target": t,                       # 后继
            "strength": d.get("strength"),
            "reason": d.get("reason"),
            "external": True,
            "source_dataset": "cn-math-taxonomy",
        })

    dropped = has_cycle(pair_candidates)
    if dropped:
        drop_set = set(dropped)
        overlay_edges = [e for e in overlay_edges if (e["source"], e["target"]) not in drop_set]

    # ── 输出 ──────────────────────────────────────────────────────
    sha = upstream_sha()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    merged_nodes = [n for n in overlay_nodes if not n.get("merged")]
    standalone = [n for n in overlay_nodes if n.get("merged")]

    meta = {
        "name": "cn-math-taxonomy 教材细分图层",
        "source": SOURCE_URL,
        "license": LICENSE,
        "upstream_commit": sha,
        "imported_at": now,
        "usage": "本地非商业研究 / 原型预览；未获作者书面单独授权前不得公开发布或商用",
        "scope": "仅知识点与先修关系，不含题库（questions.json 未导入）",
        "transforms": [
            "字段改名与补全（description→definition 等）",
            "学科映射到 TeachAny SUBJECT_CONFIG",
            "grade 13–16 映射到 10–12",
            "节点 ID 加 tax- 前缀，避免 ext-<hex> 保留命名空间",
            "名称精确匹配者复用本地节点 ID（merged），其余作为细分点挂 parent_id",
            "剔除自环、重复边、与本地已有边重复者、成环边",
        ],
        "counts": {
            "topics": len(topics),
            "new_nodes": len(merged_nodes),
            "merged_into_local": len(standalone),
            "edges": len(overlay_edges),
            "self_loops_dropped": skipped_self,
            "duplicate_edges_dropped": skipped_dup,
            "edges_already_local": skipped_local,
            "cycle_edges_dropped": len(dropped),
            "by_subject": dict(by_subject_count.most_common()),
            "match_types": dict(Counter(r["match_type"] for r in mapping_rows)),
        },
    }

    graph_overlay = {
        "meta": meta,
        "nodes": merged_nodes,
        "merged": standalone,          # 精确同名点的补充信息（不参与图谱节点数组）
        "edges": overlay_edges,
    }
    (out / "graph-overlay.json").write_text(
        json.dumps(graph_overlay, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "mapping.json").write_text(
        json.dumps({"meta": meta, "rows": mapping_rows}, ensure_ascii=False, indent=1), encoding="utf-8")

    # 课标条目（只保留编号与文本，带 verbatim 标记）
    std_items = standards.get("items", [])
    (out / "standards.json").write_text(
        json.dumps({"source": SOURCE_URL, "license": LICENSE, "items": std_items},
                   ensure_ascii=False, indent=1), encoding="utf-8")

    notice = f"""# NOTICE — 第三方数据署名

- **数据来源**：[xiaoyang111222/cn-math-taxonomy]({SOURCE_URL})
- **许可证**：[CC BY-NC 4.0 International](https://creativecommons.org/licenses/by-nc/4.0/)（署名-非商业性使用 4.0 国际）
- **上游 commit**：`{sha}` · **导入时间**：{now}
- **导入范围**：`topics.json` / `dependencies.json` / `cn-curriculum-standards.json`；**未导入** `questions.json`（题库暂不动）
- **用途**：本地非商业研究 / 原型预览。**未获作者书面单独授权前，不得公开发布、不得用于商业用途**（含付费课程、付费 App、机构收费服务、售卖题库）。商业授权联系渠道见上游 README。
- **修改说明**：本目录数据为「改编材料 / Adapted Material」——已做字段重命名、学科与学段映射、名称归一化、ID 前缀 `tax-`、剔除自环/重复/成环边，并新增 `parent_id` 映射；原始题干与题库未引入。
- **免责**：上游数据按 AS-IS 提供，作者声明先修关系 hard/soft 为 AI 主观判断、题目与映射未经一线教师审核；本站点仅作展示预览，不用于教学诊断或学习路径推荐。
- **第三方组件**：上游 `assets/vendor/` 中的 cytoscape / dagre / cytoscape-dagre / qrcode-generator 仍为 MIT，`scripts/vendor/jsQR` 为 Apache-2.0，未被本目录引入。

> 引用要求：保留本 NOTICE、在数据目录与页面显著位置标注来源与 CC BY-NC 4.0、标注「已修改」，不得暗示上游背书。
"""
    (out / "NOTICE.md").write_text(notice, encoding="utf-8")

    print("✅ 生成完成:", out)
    print(json.dumps(meta["counts"], ensure_ascii=False, indent=2))
    print("   文件大小:", {p.name: f"{p.stat().st_size/1024:.0f} KB" for p in sorted(out.iterdir())})
    return 0


if __name__ == "__main__":
    sys.exit(main())
