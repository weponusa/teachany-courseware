#!/usr/bin/env python3
"""Enrich missing CN deep snippets from local curated subject documents.

This pass is intentionally conservative:
- only fills nodes that currently have no `supplements.deep_textbook_snippets`;
- prefers exact/fuzzy local curated files under `curriculum-standards/<学科>/<学段>`;
- falls back to local curriculum/OER markdown for info-tech and a few sparse subjects;
- marks source_type explicitly as `local_curated_kp_md` or `local_oer_curriculum_md`.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
KP_INDEX_PATH = ROOT / "data" / "kp" / "_index.json"
NODE_INDEX_PATH = ROOT / "data" / "node-index.json"
SOURCE_TAG = "local_curated_enrichment_2026-06-01"

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
}
STAGE_ZH = {"elementary": "小学", "middle": "初中", "high": "高中"}
PLACEHOLDER_RE = re.compile(r"\[待补充[^\]]*\]|待补充|TODO|TBD|placeholder|暂无对应", re.I)
GENERIC_RE = re.compile(r"培养什么人、怎样培养人、为谁培养人|修订原则|坚持目标导向|坚持问题导向|课程方案")

FALLBACK_SOURCES = {
    "info-tech": [
        "books/课标-整理版/cn/high/信息技术.md",
        "books/课标-整理版/cn/all/信息技术_high.md",
        "books/课标-整理版/ap/ap-computer-science-principles.md",
        "books/课标-整理版/ap/ap-computer-science-a.md",
        "books/课标-整理版/cambridge/cambridge-lsec-computing.md",
        "books/课标-整理版/cambridge/cambridge-lsec-ict.md",
    ],
    "geography": [
        "books/课标-整理版/ap/ap-human-geography.md",
        "books/课标-整理版/cambridge/IGCSE/0460_Geography.md",
        "books/06_atmosphere_meteorology.md",
    ],
    "history": [
        "books/课标-整理版/ap/ap-world-history.md",
        "books/课标-整理版/ap/ap-european-history.md",
        "books/social_studies/OpenStax_US_History.md",
    ],
    "english": [
        "books/课标-整理版/cambridge/cambridge-primary-english.md",
        "books/课标-整理版/cambridge/cambridge-lsec-english.md",
        "books/课标-整理版/us/common-core-ela.md",
    ],
    "math": [
        "books/课标-整理版/ap/ap-calculus-ab.md",
        "books/课标-整理版/ap/ap-statistics.md",
        "books/math/OpenStax_HS_Statistics.md",
    ],
    "physics": [
        "books/science/OpenStax_HighSchool_Physics.md",
        "books/science/OpenStax_HighSchool_Physics_LabManual.md",
    ],
    "biology": [
        "books/science/OpenStax_Biology_2e.md",
        "books/science/OpenStax_AP_Biology.md",
    ],
    "chemistry": [
        "books/science/OpenStax_Chemistry.md",
        "books/03_introductory_chemistry.md",
    ],
}

MANUAL_TERMS = {
    "it-h-programming-basics": ["programming", "variable", "data type", "program", "算法", "变量", "数据类型"],
    "it-h-control-structures": ["control structure", "selection", "iteration", "loop", "branch", "分支", "循环"],
    "it-h-functions-modules": ["function", "module", "procedure", "函数", "模块"],
    "it-h-data-structures": ["data structure", "list", "stack", "queue", "tree", "graph", "数据结构", "列表", "栈", "队列"],
    "it-h-algorithm-concept": ["algorithm", "algorithmic", "算法", "复杂度"],
    "it-h-sorting-searching": ["sorting", "searching", "search", "sort", "排序", "查找"],
    "it-h-recursion": ["recursion", "recursive", "递归", "分治"],
    "it-h-network-basics": ["network", "internet", "protocol", "TCP", "IP", "网络", "协议"],
    "it-h-internet-applications": ["internet", "web", "HTTP", "email", "互联网", "应用"],
    "it-h-information-security": ["security", "privacy", "encryption", "cyber", "信息安全", "隐私"],
    "chem-h-galvanic-cell": ["galvanic", "voltaic", "electrochemical cell", "battery", "原电池", "电化学"],
    "chem-m-oxygen-preparation": ["oxygen", "preparation", "decomposition", "氧气", "制取"],
    "phy-m-light-propagation": ["light", "ray", "propagation", "reflection", "refraction", "光", "直线传播"],
    "math-h-derivative-concept": ["derivative", "limit", "tangent", "rate of change", "导数", "切线", "变化率"],
    "math-h-derivative-application": ["derivative", "maximum", "minimum", "optimization", "导数", "极值", "最值"],
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def norm(s: str) -> str:
    return re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]", "", s or "").lower()


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").replace("\u0007", " ")).strip()


def valid_text(text: str) -> bool:
    if len(clean_text(text)) < 120:
        return False
    if PLACEHOLDER_RE.search(text) or GENERIC_RE.search(text[:1600]):
        return False
    return True


def source_candidates(data: dict[str, Any]) -> list[tuple[Path, str, str, int]]:
    subject = data.get("subject") or ""
    stage = data.get("stage") or ""
    name = data.get("name") or ""
    zh_subject = SUBJECT_ZH.get(subject)
    zh_stage = STAGE_ZH.get(stage)
    candidates: list[tuple[Path, str, str, int]] = []
    if zh_subject:
        bases: list[Path] = []
        if zh_stage:
            bases.append(WORKSPACE / "curriculum-standards" / zh_subject / zh_stage)
        bases.append(WORKSPACE / "curriculum-standards" / zh_subject)
        nname = norm(name)
        for base in bases:
            if not base.is_dir():
                continue
            for fp in base.rglob("*.md"):
                stem = fp.stem
                nstem = norm(stem)
                score = 0
                if nstem == nname:
                    score = 100
                elif nname and (nname in nstem or nstem in nname):
                    score = 80
                else:
                    terms = [t for t in re.findall(r"[\u4e00-\u9fff]{2,8}|[A-Za-z]{3,}", name) if len(t) >= 2]
                    hits = sum(1 for t in terms if norm(t) and norm(t) in nstem)
                    if hits:
                        score = 30 + hits * 10
                if score >= 50:
                    candidates.append((fp, str(fp.relative_to(WORKSPACE)), "local_curated_kp_md", score))
    return sorted(candidates, key=lambda x: x[3], reverse=True)


def keywords_for(kp_id: str, data: dict[str, Any]) -> list[str]:
    terms = list(MANUAL_TERMS.get(kp_id, []))
    name = data.get("name") or ""
    name_en = data.get("name_en") or ""
    terms += re.findall(r"[\u4e00-\u9fff]{2,10}", name)
    terms += [x.lower() for x in re.findall(r"[A-Za-z][A-Za-z\-']{2,}", str(name_en))]
    for cp in data.get("curriculum_points") or []:
        terms += re.findall(r"[\u4e00-\u9fff]{3,10}", str(cp))[:5]
    out: list[str] = []
    for t in terms:
        t = t.strip()
        if t and t not in out:
            out.append(t)
    return out[:18]


def split_chunks(text: str) -> list[str]:
    parts = re.split(r"(?=^#{1,4}\s+)|\n{2,}", text.replace("\r\n", "\n"), flags=re.M)
    chunks: list[str] = []
    buf = ""
    for part in parts:
        part = clean_text(part)
        if len(part) < 80:
            continue
        if len(buf) + len(part) < 1700:
            buf = (buf + "\n" + part).strip()
        else:
            if valid_text(buf):
                chunks.append(buf[:1700])
            buf = part
    if valid_text(buf):
        chunks.append(buf[:1700])
    return chunks


def score_chunk(chunk: str, terms: list[str]) -> tuple[int, list[str]]:
    lower = chunk.lower()
    score = 0
    hits: list[str] = []
    for term in terms:
        if not term:
            continue
        target = term.lower()
        count = lower.count(target) if re.search(r"[A-Za-z]", target) else chunk.count(term)
        if count:
            score += min(24, count * (8 if len(term) >= 4 else 4))
            if target in lower[:240] or term in chunk[:240]:
                score += 8
            hits.append(term)
    return score, hits[:10]


def snippets_from_file(path: Path, label: str, source_type: str, base_score: int, terms: list[str], max_items: int) -> list[dict[str, Any]]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    chunks = split_chunks(text)
    items = []
    for chunk in chunks:
        score, hits = score_chunk(chunk, terms)
        if source_type == "local_curated_kp_md" and base_score >= 80:
            score += base_score
        if score < (40 if source_type == "local_curated_kp_md" else 18):
            continue
        items.append({
            "source": label,
            "text": chunk[:1600],
            "score": score,
            "match_terms": hits,
            "source_type": source_type,
        })
    items.sort(key=lambda x: x["score"], reverse=True)
    return items[:max_items]


def fallback_files(subject: str) -> list[tuple[Path, str, str, int]]:
    out = []
    for rel in FALLBACK_SOURCES.get(subject, []):
        p = WORKSPACE / rel
        if p.is_file():
            out.append((p, rel, "local_oer_curriculum_md", 0))
    return out


def worked_example(data: dict[str, Any], snippets: list[dict[str, Any]]) -> dict[str, Any]:
    name = data.get("name") or data.get("kp_id")
    subject = data.get("subject") or ""
    if subject == "info-tech":
        stem = f"根据资料片段，设计一个关于「{name}」的小项目任务，并说明输入、处理和输出。"
        outline = "明确问题目标，选择数据表示，写出算法步骤或代码结构，再用测试用例验证。"
    elif subject == "chinese":
        stem = f"根据资料片段，设计一道关于「{name}」的阅读或表达任务。"
        outline = "回到文本或语言材料，说明依据，再完成赏析、仿写或迁移表达。"
    elif subject == "geography":
        stem = f"根据资料片段，设计一道关于「{name}」的读图或区域分析任务。"
        outline = "提取位置、分布、数据或案例信息，分析地理联系并形成判断。"
    else:
        stem = f"根据资料片段，设计一道关于「{name}」的讲解或应用题。"
        outline = "先提取资料中的核心概念或案例，再说明解题/解释步骤。"
    return {"stem": stem, "solution_outline": outline, "evidence_excerpt": snippets[0]["text"][:260] if snippets else "", "source": SOURCE_TAG}


def backup(path: Path, backup_root: Path) -> None:
    target = backup_root / path.relative_to(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def process(args: argparse.Namespace) -> dict[str, Any]:
    idx = load_json(KP_INDEX_PATH)["kps"]
    node_idx = load_json(NODE_INDEX_PATH).get("nodes", {}) if NODE_INDEX_PATH.exists() else {}
    subjects = set(args.subject or [])
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = ROOT / "data" / "kp" / "_backups" / f"local-curated-cn-{run_id}"
    stats: Counter[str] = Counter()
    by_subject: dict[str, Counter[str]] = defaultdict(Counter)
    changed_files: list[str] = []

    for kp_id, rel in sorted(idx.items()):
        path = ROOT / rel
        if not path.exists():
            continue
        data = load_json(path)
        curriculum = data.get("curriculum") or node_idx.get(kp_id, {}).get("curriculum")
        if curriculum != "cn":
            continue
        subject = data.get("subject") or node_idx.get(kp_id, {}).get("subject") or "unknown"
        if subjects and subject not in subjects:
            continue
        by_subject[subject]["seen"] += 1
        if (data.get("supplements") or {}).get("deep_textbook_snippets"):
            by_subject[subject]["already_deep"] += 1
            continue

        terms = keywords_for(kp_id, data)
        files = source_candidates(data) + fallback_files(subject)
        snippets: list[dict[str, Any]] = []
        for fp, label, source_type, base_score in files[:12]:
            snippets.extend(snippets_from_file(fp, label, source_type, base_score, terms, args.max_snippets))
        # de-dupe
        dedup = []
        seen_text = set()
        for item in sorted(snippets, key=lambda x: x["score"], reverse=True):
            key = item["text"][:180]
            if key in seen_text:
                continue
            seen_text.add(key)
            dedup.append(item)
            if len(dedup) >= args.max_snippets:
                break
        if not dedup:
            by_subject[subject]["no_match"] += 1
            continue

        before = json.dumps(data, ensure_ascii=False, sort_keys=True)
        sup = data.setdefault("supplements", {})
        sup["deep_textbook_snippets"] = dedup
        sup["deep_textbook_source"] = SOURCE_TAG
        sup["deep_textbook_enriched_at"] = utc_now()
        sup["deep_worked_example"] = worked_example(data, dedup)
        tc = data.setdefault("textbook_content", {})
        tc["deep_snippets"] = dedup[:3]
        tc["deep_source"] = SOURCE_TAG
        meta = data.setdefault("_meta", {})
        sources = meta.setdefault("sources", [])
        if isinstance(sources, list) and SOURCE_TAG not in sources:
            sources.append(SOURCE_TAG)
        after = json.dumps(data, ensure_ascii=False, sort_keys=True)
        if before != after:
            by_subject[subject]["changed"] += 1
            stats["nodes_enriched"] += 1
            stats["snippets_added"] += len(dedup)
            changed_files.append(str(path.relative_to(ROOT)))
            if not args.dry_run:
                backup(path, backup_root)
                dump_json(path, data)
                stats["written_files"] += 1
            else:
                stats["would_write_files"] += 1

    report = {
        "run_at": utc_now(),
        "dry_run": args.dry_run,
        "backup_dir": str(backup_root.relative_to(ROOT)),
        "stats": dict(stats),
        "by_subject": {k: dict(v) for k, v in sorted(by_subject.items())},
        "changed_files_count": len(changed_files),
        "changed_files_sample": changed_files[:80],
    }
    if not args.dry_run:
        backup_root.mkdir(parents=True, exist_ok=True)
        (backup_root / "local-curated-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Fill missing CN deep snippets from local curated/OER markdown")
    parser.add_argument("--subject", action="append", help="limit subject; can repeat")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-snippets", type=int, default=3)
    args = parser.parse_args()
    print(json.dumps(process(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
