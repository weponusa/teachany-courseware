#!/usr/bin/env python3
"""
build-node-enrichment-overlay.py

在**不修改** data/trees/cn/** 课标树结构的前提下，生成自有增强层：
  data/node-enrichment-overlay.json

用途：
  - 给前置边补齐 strength(hard/soft) + reason
  - 给节点补齐 evidence / assessment / misconceptions（错因诊断）
  - 供 AI 学伴、学习路径、课件知识图谱在运行时合并

种子（可选）：
  data/node-enrichment-seed.json — 人工精校字段优先覆盖自动推断

设计约束：
  - 不写入课标树
  - 不引入/署名任何外部 taxonomy
  - 仅基于本仓库 trees + seed 生成
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TREES = ROOT / "data" / "trees" / "cn"
SEED = ROOT / "data" / "node-enrichment-seed.json"
OUT = ROOT / "data" / "node-enrichment-overlay.json"

# 常见中文错因模板（按学科关键字命中，再交 seed 精修）
SUBJECT_MISCONCEPTION_TEMPLATES = {
    "math": [
        {
            "id": "mc-sign",
            "cue": "符号判断错误（正负、不等号方向）",
            "diagnosis": "先让学生标出符号来源，再代入验算",
            "tutor_hint": "先问：符号由谁决定？再用一个特例检验",
        },
        {
            "id": "mc-formula-plug",
            "cue": "套公式却不检查适用条件",
            "diagnosis": "让学生先写出适用条件，再谈计算",
            "tutor_hint": "先条件、后计算；缺条件时不要直接给答案",
        },
    ],
    "physics": [
        {
            "id": "mc-unit",
            "cue": "单位不统一或温度未换成热力学温度",
            "diagnosis": "逐项核对接量和国际单位",
            "tutor_hint": "先统一单位再谈公式，温度相关必问是否用 K",
        },
        {
            "id": "mc-cause-effect",
            "cue": "把相关关系误当成因果关系",
            "diagnosis": "区分相关与因果，明确控制变量",
            "tutor_hint": "问：哪个量变了？哪些量必须保持不变？",
        },
    ],
    "chinese": [
        {
            "id": "mc-literal",
            "cue": "只做字面理解，忽略文意/语境",
            "diagnosis": "要求回到原文找证据句",
            "tutor_hint": "先问证据在哪一句，再谈概括",
        }
    ],
    "science": [
        {
            "id": "mc-observation",
            "cue": "把观察现象直接当结论",
            "diagnosis": "要求补全“现象→证据→解释”三步",
            "tutor_hint": "先让学生描述现象，再追问证据和解释",
        }
    ],
    "english": [
        {
            "id": "mc-translate-literal",
            "cue": "逐字对译导致语法/搭配错误",
            "diagnosis": "对比中英表达差异，给出正确搭配",
            "tutor_hint": "先问完整句子目标，再纠正关键结构",
        }
    ],
}


def load_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def iter_cn_nodes():
    if not TREES.exists():
        return
    for f in sorted(TREES.rglob("*.json")):
        if "other" in f.parts:
            continue
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(data, dict) or "domains" not in data:
            continue
        subject = data.get("subject") or f.stem
        stage = data.get("stage") or next((p for p in f.parts if p in ("elementary", "middle", "high")), "")
        for domain in data.get("domains") or []:
            domain_id = domain.get("id") or ""
            domain_name = domain.get("name") or domain_id
            for node in domain.get("nodes") or []:
                nid = node.get("id")
                if not nid:
                    continue
                yield {
                    "id": nid,
                    "name": node.get("name") or nid,
                    "subject": subject,
                    "stage": stage,
                    "grade": node.get("grade"),
                    "domain": domain_id,
                    "domain_name": domain_name,
                    "prerequisites": list(node.get("prerequisites") or []),
                    "extends": list(node.get("extends") or []),
                    "curriculum_points": list(node.get("curriculum_points") or []),
                }


def infer_strength(node, pre, by_id) -> str:
    p = by_id.get(pre)
    if not p:
        return "soft"
    # 同学科且年级差 ≤ 1 → hard；跨学科或跨很大年级 → soft
    try:
        g1 = int(node.get("grade") or 0)
        g2 = int(p.get("grade") or 0)
    except Exception:
        g1 = g2 = 0
    same_subject = (node.get("subject") == p.get("subject"))
    same_domain = (node.get("domain") == p.get("domain")) and bool(node.get("domain"))
    if same_subject and abs(g1 - g2) <= 1:
        return "hard"
    if same_subject and same_domain:
        return "hard"
    return "soft"


def reason_for(node, pre, by_id) -> str:
    p = by_id.get(pre)
    pname = (p or {}).get("name") or pre
    nname = node.get("name") or node["id"]
    if (p or {}).get("subject") == node.get("subject"):
        return f"学习「{nname}」前应先掌握「{pname}」的核心概念与方法。"
    return f"「{pname}」能为理解「{nname}」提供关键基础（跨领域关联）。"


def evidence_from_node(node) -> list[str]:
    cps = [re.sub(r"\s+", " ", str(c)).strip() for c in (node.get("curriculum_points") or [])]
    out = []
    for c in cps:
        if not c:
            continue
        out.append(c[:160] + ("…" if len(c) > 160 else ""))
        if len(out) >= 2:
            break
    if not out:
        out.append(f"能说明「{node.get('name')}」的含义、适用条件，并用一例解释。")
    return out


def assessment_from_node(node) -> list[str]:
    name = node.get("name") or node["id"]
    return [
        f"用自己的话解释什么是「{name}」，并指出一个适用条件。",
        f"给出一个与「{name}」相关的反例或易错点，说明错在哪里。",
    ]


def misconceptions_for(node) -> list[dict]:
    subj = (node.get("subject") or "").lower()
    templates = SUBJECT_MISCONCEPTION_TEMPLATES.get(subj) or SUBJECT_MISCONCEPTION_TEMPLATES.get("science") or []
    # 浅拷贝，避免共享可变对象
    return [dict(x) for x in templates[:2]]


def build_overlay(seed: dict | None) -> dict:
    nodes = list(iter_cn_nodes())
    by_id = {n["id"]: n for n in nodes}
    seed_nodes = (seed or {}).get("nodes") or {}

    out_nodes: dict = {}
    hard_edges = soft_edges = 0
    with_misc = 0

    for node in nodes:
        nid = node["id"]
        seed_entry = seed_nodes.get(nid) or {}
        prereqs_enriched = []
        seen = set()

        # seed 优先
        for e in seed_entry.get("prereqs_enriched") or []:
            pid = e.get("id")
            if not pid or pid in seen:
                continue
            seen.add(pid)
            strength = e.get("strength") or infer_strength(node, pid, by_id)
            item = {
                "id": pid,
                "strength": strength,
                "reason": e.get("reason") or reason_for(node, pid, by_id),
                "evidence": e.get("evidence") or "",
                "assessment": e.get("assessment") or "",
            }
            prereqs_enriched.append(item)
            hard_edges += 1 if strength == "hard" else 0
            soft_edges += 1 if strength == "soft" else 0

        for pid in node.get("prerequisites") or []:
            if pid in seen:
                continue
            seen.add(pid)
            strength = infer_strength(node, pid, by_id)
            prereqs_enriched.append(
                {
                    "id": pid,
                    "strength": strength,
                    "reason": reason_for(node, pid, by_id),
                    "evidence": "",
                    "assessment": "",
                }
            )
            hard_edges += 1 if strength == "hard" else 0
            soft_edges += 1 if strength == "soft" else 0

        misconceptions = seed_entry.get("misconceptions")
        if not misconceptions:
            misconceptions = misconceptions_for(node)
        if misconceptions:
            with_misc += 1

        evidence = seed_entry.get("evidence") or evidence_from_node(node)
        assessment = seed_entry.get("assessment") or assessment_from_node(node)

        # 无前置、无错因、无 seed 时也保留证据/测评，便于学伴
        out_nodes[nid] = {
            "name": node.get("name"),
            "subject": node.get("subject"),
            "stage": node.get("stage"),
            "grade": node.get("grade"),
            "prereqs_enriched": prereqs_enriched,
            "evidence": evidence,
            "assessment": assessment,
            "misconceptions": misconceptions,
        }

    return {
        "version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "teachany-cn-trees+seed",
        "policy": "overlay-only; does-not-modify-cn-trees",
        "stats": {
            "nodes": len(out_nodes),
            "hard_edges": hard_edges,
            "soft_edges": soft_edges,
            "nodes_with_misconceptions": with_misc,
            "seed_nodes": len(seed_nodes),
        },
        "nodes": out_nodes,
    }


def main() -> int:
    seed = load_json(SEED) or {"nodes": {}}
    overlay = build_overlay(seed)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(overlay, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✅ wrote {OUT}")
    print(json.dumps(overlay["stats"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
