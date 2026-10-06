#!/usr/bin/env python3
"""Audit non-history deep_textbook_snippets quality and create a review report."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
KP_INDEX_PATH = ROOT / "data" / "kp" / "_index.json"
NODE_INDEX_PATH = ROOT / "data" / "node-index.json"
REPORT_DIR = ROOT / "reports"

PLACEHOLDER_RE = re.compile(r"\[待补充[^\]]*\]|待补充|TODO|TBD|placeholder", re.I)
GENERIC_RE = re.compile(r"培养什么人|修订原则|课程方案|通用教学原则|资源路径|配图目录")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def score_snippet(item: dict[str, Any], name: str, domain: str) -> tuple[int, list[str]]:
    text = str(item.get("text") or "")
    source_type = str(item.get("source_type") or "")
    source = str(item.get("source") or "")
    terms = [str(x) for x in (item.get("match_terms") or [])]
    score = 100
    flags: list[str] = []
    if len(text) < 120:
        score -= 35
        flags.append("too_short")
    if PLACEHOLDER_RE.search(text):
        score -= 80
        flags.append("placeholder")
    if GENERIC_RE.search(text):
        score -= 50
        flags.append("generic_text")
    if source_type == "curated_subject_pack":
        score -= 5  # 可用，但不是严格教材原文。
        flags.append("curated_pack")
    if not terms:
        score -= 20
        flags.append("no_match_terms")
    if name and name not in text and name not in " ".join(terms):
        score -= 10
        flags.append("name_not_visible")
    if not source:
        score -= 20
        flags.append("missing_source")
    return max(0, score), flags


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit non-history deep snippet quality")
    parser.add_argument("--out", default="")
    args = parser.parse_args()

    idx = load_json(KP_INDEX_PATH).get("kps", {})
    node_idx = load_json(NODE_INDEX_PATH).get("nodes", {}) if NODE_INDEX_PATH.exists() else {}
    by_subject: dict[str, Counter[str]] = defaultdict(Counter)
    rows: list[dict[str, Any]] = []

    for kp_id, rel in sorted(idx.items()):
        path = ROOT / rel
        if not path.exists():
            continue
        data = load_json(path)
        curriculum = data.get("curriculum") or node_idx.get(kp_id, {}).get("curriculum")
        subject = data.get("subject") or node_idx.get(kp_id, {}).get("subject") or "unknown"
        if curriculum != "cn" or subject == "history":
            continue
        deep = (data.get("supplements") or {}).get("deep_textbook_snippets") or []
        if not deep:
            continue
        scores = []
        flags_all: list[str] = []
        for item in deep:
            if not isinstance(item, dict):
                continue
            score, flags = score_snippet(item, data.get("name") or kp_id, data.get("domain_name") or "")
            scores.append(score)
            flags_all.extend(flags)
        avg = round(sum(scores) / len(scores), 1) if scores else 0
        by_subject[subject]["nodes"] += 1
        by_subject[subject]["snippets"] += len(deep)
        if avg < 70:
            by_subject[subject]["review"] += 1
        rows.append({
            "kp_id": kp_id,
            "name": data.get("name") or kp_id,
            "subject": subject,
            "domain": data.get("domain_name") or "",
            "avg_score": avg,
            "snippet_count": len(deep),
            "flags": sorted(set(flags_all)),
            "sample_source": deep[0].get("source") if isinstance(deep[0], dict) else "",
            "sample_text": (deep[0].get("text") if isinstance(deep[0], dict) else "")[:280],
        })

    rows.sort(key=lambda r: (r["avg_score"], r["subject"], r["kp_id"]))
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out = Path(args.out) if args.out else REPORT_DIR / f"non-history-deep-quality-{datetime.now().strftime('%Y-%m-%d')}.md"
    lines = ["# 非历史 deep_textbook_snippets 质量审计", "", f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ""]
    lines.append("## 分学科统计")
    lines.append("")
    lines.append("| 学科 | 节点数 | snippet 数 | 建议复核节点 |")
    lines.append("|---|---:|---:|---:|")
    for subject in sorted(by_subject):
        c = by_subject[subject]
        lines.append(f"| {subject} | {c['nodes']} | {c['snippets']} | {c['review']} |")
    lines.append("")
    lines.append("## 低分/需复核样本（前 80）")
    lines.append("")
    lines.append("| node_id | 名称 | 学科 | 分数 | flags | sample_source |")
    lines.append("|---|---|---|---:|---|---|")
    for r in rows[:80]:
        lines.append(f"| `{r['kp_id']}` | {r['name']} | {r['subject']} | {r['avg_score']} | {', '.join(r['flags'])} | `{r['sample_source']}` |")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out)
    print("subjects", {k: dict(v) for k, v in sorted(by_subject.items())})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
