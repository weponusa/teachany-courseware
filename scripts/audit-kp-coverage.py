#!/usr/bin/env python3
"""Audit TeachAny knowledge-point satellite coverage.

Outputs JSON, CSV, and Markdown reports for curriculum knowledge content.
No third-party dependencies.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
KP_DIR = ROOT / "data" / "kp"
KP_INDEX_PATH = KP_DIR / "_index.json"
NODE_INDEX_PATH = ROOT / "data" / "node-index.json"
REPORT_DIR = ROOT / "reports"

PLACEHOLDER_RE = re.compile(r"\[待补充[^\]]*\]|待补充|TODO|TBD|placeholder", re.I)
GENERIC_CURRICULUM_RE = re.compile(r"培养什么人、怎样培养人、为谁培养人|修订原则|坚持目标导向|坚持问题导向|课程方案")
TEXTBOOK_REFERENCE_ONLY_RE = re.compile(r"OpenStax 教材资料|配图目录|具体文件待按知识点主题归类|暂无对应教材资料|原文：`|国家中小学智慧教育平台")
TEXTBOOK_CONTENT_MARKER_RE = re.compile(r"定义|概念|原理|公式|步骤|例题|解：|实验|现象|规律|性质|应用|证明|推导|分析")
HISTORY_TEMPLATE_RE = re.compile(r"年代与名词|史料|制度变迁|考古/文献|因果链")
MATH_TEMPLATE_RE = re.compile(r"学习数学的方法|数学来源于生活|数学思想方法")

MIN_TEXTBOOK_CHARS = 120
MIN_METHOD_CHARS = 40
MIN_EXTENSION_CHARS = 40

SUBJECT_ZH = {
    "math": "数学",
    "physics": "物理",
    "chemistry": "化学",
    "biology": "生物",
    "history": "历史",
    "geography": "地理",
    "chinese": "语文",
    "english": "英语",
    "science": "科学",
    "info-tech": "信息科技",
    "other": "其他",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def text_len(value: Any) -> int:
    if value is None:
        return 0
    if isinstance(value, str):
        return len(value.strip())
    return len(json.dumps(value, ensure_ascii=False))


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return json.dumps(value, ensure_ascii=False)


def has_content(value: Any) -> bool:
    text = clean_text(value)
    return bool(text) and not PLACEHOLDER_RE.fullmatch(text)


def non_placeholder_text(value: Any) -> str:
    text = clean_text(value)
    return PLACEHOLDER_RE.sub("", text).strip()


def section_text(md: str, title_keywords: tuple[str, ...]) -> str:
    if not md:
        return ""
    sections = re.split(r"(?=^#{2,4}\s+)", md, flags=re.M)
    hits: list[str] = []
    for sec in sections:
        first = sec.splitlines()[0] if sec.splitlines() else ""
        if any(k in first for k in title_keywords):
            hits.append(sec)
    return "\n".join(hits)


def section_has_real_content(md: str, title_keywords: tuple[str, ...], min_chars: int) -> bool:
    sec = non_placeholder_text(section_text(md, title_keywords))
    lines = [ln.strip(" -\t") for ln in sec.splitlines() if ln.strip(" -\t")]
    useful = [ln for ln in lines if not ln.startswith("#") and not PLACEHOLDER_RE.search(ln)]
    return len("\n".join(useful)) >= min_chars


def usable_textbook_text(data: dict[str, Any]) -> tuple[bool, int, list[str]]:
    flags: list[str] = []
    supplements = data.get("supplements") or {}
    candidates: list[tuple[str, str]] = []

    textbook_content = data.get("textbook_content")
    if textbook_content:
        candidates.append(("textbook_content", clean_text(textbook_content)))
    for key in ("textbook_summary", "openstax_or_curriculum"):
        if supplements.get(key):
            candidates.append((key, clean_text(supplements[key])))
    for item in data.get("excerpts") or []:
        if not isinstance(item, dict):
            continue
        if item.get("source_type") == "textbook" or item.get("type") == "textbook":
            candidates.append(("excerpt_textbook", clean_text(item.get("text") or "")))

    usable_parts: list[str] = []
    for source, text in candidates:
        text = non_placeholder_text(text)
        if not text:
            continue
        head = text[:3000]
        if GENERIC_CURRICULUM_RE.search(head):
            flags.append("generic_curriculum_dump")
            continue
        if TEXTBOOK_REFERENCE_ONLY_RE.search(head) and not TEXTBOOK_CONTENT_MARKER_RE.search(head):
            flags.append("textbook_reference_only")
            continue
        if source in {"textbook_summary", "openstax_or_curriculum"} and TEXTBOOK_REFERENCE_ONLY_RE.search(head):
            # 这类摘要通常只是资料路径，除非同时包含明显的讲解/例题正文。
            if len(TEXTBOOK_CONTENT_MARKER_RE.findall(head)) < 2:
                flags.append("textbook_reference_only")
                continue
        usable_parts.append(text)

    usable_len = len("\n".join(usable_parts))
    return usable_len >= MIN_TEXTBOOK_CHARS, usable_len, sorted(set(flags))


def audit_item(kp_id: str, rel_path: str, data: dict[str, Any], node: dict[str, Any]) -> dict[str, Any]:
    subject = data.get("subject") or node.get("subject") or "unknown"
    supplements = data.get("supplements") or {}
    raw_md = supplements.get("curriculum_md_raw") or ""
    all_text = json.dumps(data, ensure_ascii=False)
    textbook_usable, textbook_chars, textbook_flags = usable_textbook_text(data)

    curriculum_points = data.get("curriculum_points") or []
    excerpts = data.get("excerpts") or []
    exercises = data.get("exercises") or []
    errors = data.get("errors") or []
    interactive = data.get("interactive_resources") or []
    real_world = data.get("real_world") or []

    quality_flags = list(textbook_flags)
    if PLACEHOLDER_RE.search(all_text):
        quality_flags.append("has_placeholder")
    if subject != "history" and HISTORY_TEMPLATE_RE.search(clean_text(errors) + clean_text(exercises)):
        quality_flags.append("cross_subject_history_template")
    if subject != "math" and MATH_TEMPLATE_RE.search(raw_md):
        quality_flags.append("cross_subject_math_template")

    has_teaching_methods = section_has_real_content(raw_md, ("教学方法", "学习活动设计", "教学建议", "教学提示"), MIN_METHOD_CHARS)
    has_extensions = section_has_real_content(raw_md, ("拓展资源", "拓展延伸", "相关知识", "参考资料"), MIN_EXTENSION_CHARS)

    gaps: list[str] = []
    if len(curriculum_points) < 2:
        gaps.append("curriculum_points<2")
    if len(excerpts) < 2:
        gaps.append("excerpts<2")
    if not raw_md:
        gaps.append("missing_curriculum_md_raw")
    if not textbook_usable:
        gaps.append("missing_usable_textbook")
    if len(exercises) < 1:
        gaps.append("exercises<1")
    if len(errors) < 1:
        gaps.append("common_errors<1")
    if not has_teaching_methods:
        gaps.append("missing_teaching_methods")
    if not has_extensions:
        gaps.append("missing_extensions")
    if len(real_world) < 1:
        gaps.append("real_world<1")
    if quality_flags:
        gaps.append("quality_flags")

    return {
        "kp_id": kp_id,
        "name": data.get("name") or node.get("name_zh") or "",
        "subject": subject,
        "subject_zh": SUBJECT_ZH.get(subject, subject),
        "stage": data.get("stage") or node.get("stage") or "",
        "grade": data.get("grade") or node.get("grade") or "",
        "curriculum": data.get("curriculum") or node.get("curriculum") or "",
        "domain": data.get("domain_name") or node.get("domain") or "",
        "path": rel_path,
        "curriculum_points_count": len(curriculum_points),
        "excerpts_count": len(excerpts),
        "curriculum_md_chars": text_len(raw_md),
        "has_curriculum_md": bool(raw_md),
        "textbook_chapter": data.get("textbook_chapter") or "",
        "textbook_chars": textbook_chars,
        "has_usable_textbook": textbook_usable,
        "exercises_count": len(exercises),
        "errors_count": len(errors),
        "interactive_count": len(interactive),
        "real_world_count": len(real_world),
        "has_teaching_methods": has_teaching_methods,
        "has_extensions": has_extensions,
        "quality_flags": quality_flags,
        "gaps": gaps,
        "gap_count": len(gaps),
    }


def load_rows(curriculum: str) -> list[dict[str, Any]]:
    kp_index = load_json(KP_INDEX_PATH)
    node_index = load_json(NODE_INDEX_PATH).get("nodes", {}) if NODE_INDEX_PATH.exists() else {}
    rows: list[dict[str, Any]] = []
    for kp_id, rel_path in sorted((kp_index.get("kps") or {}).items()):
        path = ROOT / rel_path
        if not path.is_file():
            continue
        data = load_json(path)
        node = node_index.get(kp_id, {})
        item_curriculum = data.get("curriculum") or node.get("curriculum") or ""
        if curriculum != "all" and item_curriculum != curriculum:
            continue
        rows.append(audit_item(kp_id, rel_path, data, node))
    return rows


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_subject: dict[str, Counter[str]] = defaultdict(Counter)
    gap_counter: Counter[str] = Counter()
    quality_counter: Counter[str] = Counter()
    stage_counter: Counter[str] = Counter()

    bool_fields = [
        "has_curriculum_md",
        "has_usable_textbook",
        "has_teaching_methods",
        "has_extensions",
    ]
    count_fields = [
        "curriculum_points_count",
        "excerpts_count",
        "exercises_count",
        "errors_count",
        "interactive_count",
        "real_world_count",
    ]

    for row in rows:
        subj = row["subject"]
        by_subject[subj]["total"] += 1
        stage_counter[row.get("stage") or "unknown"] += 1
        for field in bool_fields:
            if row[field]:
                by_subject[subj][field] += 1
        for field in count_fields:
            if row[field] > 0:
                by_subject[subj][field] += 1
        for gap in row["gaps"]:
            gap_counter[gap] += 1
            by_subject[subj][f"gap:{gap}"] += 1
        for flag in row["quality_flags"]:
            quality_counter[flag] += 1
            by_subject[subj][f"flag:{flag}"] += 1

    return {
        "total": len(rows),
        "by_subject": {k: dict(v) for k, v in sorted(by_subject.items())},
        "by_stage": dict(stage_counter),
        "gaps": dict(gap_counter.most_common()),
        "quality_flags": dict(quality_counter.most_common()),
    }


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    fieldnames = [
        "kp_id", "name", "subject", "subject_zh", "stage", "grade", "curriculum", "domain", "path",
        "curriculum_points_count", "excerpts_count", "curriculum_md_chars", "has_curriculum_md",
        "textbook_chapter", "textbook_chars", "has_usable_textbook", "exercises_count", "errors_count",
        "interactive_count", "real_world_count", "has_teaching_methods", "has_extensions",
        "gap_count", "gaps", "quality_flags",
    ]
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            out = {k: row.get(k, "") for k in fieldnames}
            out["gaps"] = ";".join(row.get("gaps") or [])
            out["quality_flags"] = ";".join(row.get("quality_flags") or [])
            writer.writerow(out)


def pct(n: int, total: int) -> str:
    return f"{n / total * 100:.1f}%" if total else "0.0%"


def write_markdown(rows: list[dict[str, Any]], summary: dict[str, Any], path: Path) -> None:
    lines: list[str] = []
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append("# 中国课标知识点预制内容覆盖率审计")
    lines.append("")
    lines.append(f"生成时间：{generated_at}")
    lines.append("")
    total = summary["total"]
    lines.append("## 总览")
    lines.append("")
    lines.append(f"- 中国课标知识点：`{total}` 个")
    for key, label in [
        ("missing_curriculum_md_raw", "缺完整课标 MD"),
        ("missing_usable_textbook", "缺可用教材内容"),
        ("exercises<1", "缺习题/例题"),
        ("common_errors<1", "缺易错点"),
        ("missing_teaching_methods", "缺教学方法"),
        ("missing_extensions", "缺拓展资源"),
        ("quality_flags", "存在质量风险"),
    ]:
        n = summary["gaps"].get(key, 0)
        lines.append(f"- {label}：`{n}` 个（{pct(n, total)}）")
    lines.append("")

    lines.append("## 分学科覆盖")
    lines.append("")
    lines.append("| 学科 | 总数 | 完整课标MD | 可用教材 | 有习题 | 有易错 | 教学方法 | 拓展资源 | 质量风险 |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for subject, stat in summary["by_subject"].items():
        total_s = stat.get("total", 0)
        lines.append(
            "| {name} | {total} | {md} | {tb} | {ex} | {err} | {method} | {ext} | {risk} |".format(
                name=SUBJECT_ZH.get(subject, subject),
                total=total_s,
                md=stat.get("has_curriculum_md", 0),
                tb=stat.get("has_usable_textbook", 0),
                ex=stat.get("exercises_count", 0),
                err=stat.get("errors_count", 0),
                method=stat.get("has_teaching_methods", 0),
                ext=stat.get("has_extensions", 0),
                risk=stat.get("gap:quality_flags", 0),
            )
        )
    lines.append("")

    lines.append("## 主要缺口")
    lines.append("")
    for gap, count in summary["gaps"].items():
        lines.append(f"- `{gap}`：{count}")
    lines.append("")

    lines.append("## 质量风险")
    lines.append("")
    if summary["quality_flags"]:
        for flag, count in summary["quality_flags"].items():
            lines.append(f"- `{flag}`：{count}")
    else:
        lines.append("- 未发现明显风险标记")
    lines.append("")

    lines.append("## 优先处理样例（gap_count 最高）")
    lines.append("")
    lines.append("| node_id | 名称 | 学科 | gap_count | gaps | quality_flags |")
    lines.append("|---|---|---|---:|---|---|")
    for row in sorted(rows, key=lambda r: (-r["gap_count"], r["subject"], r["kp_id"]))[:80]:
        lines.append(
            f"| `{row['kp_id']}` | {row['name']} | {SUBJECT_ZH.get(row['subject'], row['subject'])} | {row['gap_count']} | {', '.join(row['gaps'])} | {', '.join(row['quality_flags'])} |"
        )
    lines.append("")

    lines.append("## 建议")
    lines.append("")
    lines.append("1. 先清理 `cross_subject_*` 与 `generic_curriculum_dump`，避免生成课件误用脏数据。")
    lines.append("2. 先补数学、物理、化学、生物的教材正文与例题，形成稳定模板。")
    lines.append("3. 对语文、英语、地理、科学、信息科技建立专用题型与易错点生成模板，不再套用数理化模板。")
    lines.append("4. 将本报告作为 Stage7 批量补灌的输入清单，按 CSV 中 `gaps` 字段分批处理。")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit TeachAny KP satellite content coverage")
    parser.add_argument("--curriculum", default="cn", help="curriculum filter, default: cn; use all for all curricula")
    parser.add_argument("--out-prefix", default="", help="output prefix without extension")
    args = parser.parse_args()

    if not KP_INDEX_PATH.is_file():
        raise SystemExit(f"Missing KP index: {KP_INDEX_PATH}")

    rows = load_rows(args.curriculum)
    summary = summarize(rows)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    date = datetime.now().strftime("%Y-%m-%d")
    prefix = args.out_prefix or f"kp-coverage-{args.curriculum}-{date}"
    json_path = REPORT_DIR / f"{prefix}.json"
    csv_path = REPORT_DIR / f"{prefix}.csv"
    md_path = REPORT_DIR / f"{prefix}.md"

    json_path.write_text(json.dumps({"summary": summary, "rows": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(rows, csv_path)
    write_markdown(rows, summary, md_path)

    print(f"audited: {summary['total']} knowledge points")
    print(f"json: {json_path.relative_to(ROOT)}")
    print(f"csv:  {csv_path.relative_to(ROOT)}")
    print(f"md:   {md_path.relative_to(ROOT)}")
    print("top gaps:")
    for gap, count in list(summary["gaps"].items())[:10]:
        print(f"  {gap}: {count}")
    if summary["quality_flags"]:
        print("quality flags:")
        for flag, count in summary["quality_flags"].items():
            print(f"  {flag}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
