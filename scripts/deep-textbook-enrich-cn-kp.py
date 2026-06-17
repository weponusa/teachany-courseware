#!/usr/bin/env python3
"""Deep textbook enrichment for CN KP satellites.

Adds traceable textbook/curriculum snippets from existing local sources:
- matched textbook excerpts already present in KP JSON
- `books/课标-整理版/cn/.../*.md`
- selected OpenStax markdown books
- exact `curriculum-standards/<学科>/<学段>/<知识点>.md` files when present

Also backfills thin `curriculum_points` / `excerpts` from existing curriculum text.
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
KP_ROOT = ROOT / "data" / "kp"
KP_INDEX_PATH = KP_ROOT / "_index.json"
NODE_INDEX_PATH = ROOT / "data" / "node-index.json"

SOURCE_TAG = "deep_textbook_enrichment_2026-06-01"
PLACEHOLDER_RE = re.compile(r"\[待补充[^\]]*\]|待补充|TODO|TBD|placeholder", re.I)
GENERIC_RE = re.compile(r"培养什么人、怎样培养人、为谁培养人|修订原则|坚持目标导向|坚持问题导向|课程方案|营造积极的课堂生态|师生关系|课堂氛围|不怕出错|大胆表达|教学建议|实施建议")
CONTENT_MARKER_RE = re.compile(
    r"定义|概念|原理|公式|步骤|例题|解：|实验|现象|规律|性质|应用|证明|推导|分析|阅读|表达|地图|语境|Example|Solution|Figure|definition|function|law|reaction|cell|data",
    re.I,
)

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
    "info-tech": "信息技术",
    "other": "综合",
}
STAGE_ZH = {"elementary": "小学", "middle": "初中", "high": "高中"}

OPENSTAX_SOURCES = {
    "math": [
        "books/math/OpenStax_CollegeAlgebra.md",
        "books/math/OpenStax_Prealgebra_2e.md",
        "books/math/OpenStax_HS_Statistics.md",
    ],
    "physics": [
        "books/science/OpenStax_HighSchool_Physics.md",
        "books/science/OpenStax_HighSchool_Physics_LabManual.md",
    ],
    "chemistry": ["books/science/OpenStax_Chemistry.md"],
    "biology": [
        "books/science/OpenStax_Biology_2e.md",
        "books/science/OpenStax_AP_Biology.md",
    ],
    "history": ["books/social_studies/OpenStax_US_History.md"],
    "science": [
        "books/science/OpenStax_HighSchool_Physics.md",
        "books/science/OpenStax_Biology_2e.md",
        "books/science/OpenStax_Astronomy.md",
    ],
}

CN_SOURCE_NAMES = {
    "math": "math.md",
    "physics": "physics.md",
    "chemistry": "chemistry.md",
    "biology": "biology.md",
    "history": "history.md",
    "geography": "geography.md",
    "chinese": "chinese.md",
    "english": "english.md",
    "science": "science.md",
    "politics": "morality-law-2022-outline.md",
    "psychology": "psychology-2012-outline.md",
}
CN_HIGH_NAMES = {
    "math": "数学.md",
    "physics": "物理.md",
    "chemistry": "化学.md",
    "biology": "生物.md",
    "history": "历史.md",
    "geography": "地理.md",
    "chinese": "语文.md",
    "english": "英语.md",
    "info-tech": "信息技术.md",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean(s: str) -> str:
    s = re.sub(r"\s+", " ", s or "").strip()
    s = s.replace("\u0007", " ")
    return re.sub(r"\s+", " ", s).strip()


def valid_chunk(text: str) -> bool:
    if len(text) < 160:
        return False
    if PLACEHOLDER_RE.search(text) or GENERIC_RE.search(text[:1500]):
        return False
    if not CONTENT_MARKER_RE.search(text):
        return False
    return True


def split_chunks(text: str, max_chars: int = 1800) -> list[str]:
    text = text.replace("\r\n", "\n")
    raw_parts = re.split(r"(?=^#{1,4}\s+)|\n{2,}", text, flags=re.M)
    chunks: list[str] = []
    buf = ""
    for part in raw_parts:
        part = clean(part)
        if len(part) < 80:
            continue
        if len(buf) + len(part) < max_chars:
            buf = (buf + "\n" + part).strip()
        else:
            if valid_chunk(buf):
                chunks.append(buf[:max_chars])
            buf = part
    if valid_chunk(buf):
        chunks.append(buf[:max_chars])
    return chunks


def cn_terms(text: str) -> list[str]:
    text = re.sub(r"[·（）()《》\[\]【】,:：;；/\\-]", " ", text or "")
    terms: list[str] = []
    for token in re.findall(r"[\u4e00-\u9fff]{2,12}", text):
        if token in {"知识点", "基本概念", "学习", "学生", "能够", "理解", "掌握", "运用", "相关"}:
            continue
        terms.append(token)
    out: list[str] = []
    for t in sorted(terms, key=len, reverse=True):
        if t not in out:
            out.append(t)
    return out[:12]


def keywords_for(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    cn: list[str] = []
    en: list[str] = []
    name = str(data.get("name") or "")
    cn.extend(cn_terms(name))
    for cp in data.get("curriculum_points") or []:
        cn.extend(cn_terms(str(cp))[:4])
    name_en = str(data.get("name_en") or "").strip()
    if name_en and name_en.lower() not in {"none", "null"}:
        en.append(name_en.lower())
        en.extend([x.lower() for x in re.findall(r"[A-Za-z][A-Za-z\-']{2,}", name_en)])
    seen_cn: list[str] = []
    for t in cn:
        if t not in seen_cn:
            seen_cn.append(t)
    seen_en: list[str] = []
    for t in en:
        if t not in seen_en:
            seen_en.append(t)
    return seen_cn[:16], seen_en[:8]


def score_chunk(chunk: str, cn_kw: list[str], en_kw: list[str]) -> tuple[int, list[str]]:
    score = 0
    hits: list[str] = []
    lower = chunk.lower()
    head = chunk[:220].lower()
    for kw in cn_kw:
        if len(kw) < 2:
            continue
        count = chunk.count(kw)
        if count:
            score += min(18, count * min(8, len(kw)))
            if kw in chunk[:220]:
                score += 8
            hits.append(kw)
    for kw in en_kw:
        if len(kw) < 3:
            continue
        count = lower.count(kw)
        if count:
            score += min(18, count * (8 if " " in kw else 4))
            if kw in head:
                score += 8
            hits.append(kw)
    score += min(5, len(CONTENT_MARKER_RE.findall(chunk)))
    return score, hits[:10]


def candidate_sources(data: dict[str, Any]) -> list[tuple[Path, str]]:
    subject = data.get("subject") or ""
    stage = data.get("stage") or ""
    name = data.get("name") or ""
    sources: list[tuple[Path, str]] = []

    # Exact curated knowledge-point MD.
    zh_subject = SUBJECT_ZH.get(subject)
    zh_stage = STAGE_ZH.get(stage)
    if zh_subject and zh_stage and name:
        exact = WORKSPACE / "curriculum-standards" / zh_subject / zh_stage / f"{name}.md"
        if exact.is_file():
            sources.append((exact, f"curriculum-standards/{zh_subject}/{zh_stage}/{name}.md"))

    cn_root = WORKSPACE / "books" / "课标-整理版" / "cn"
    fname = CN_SOURCE_NAMES.get(subject)
    if fname:
        for subdir in (stage, "all"):
            p = cn_root / subdir / fname
            if p.is_file():
                sources.append((p, f"books/课标-整理版/cn/{subdir}/{fname}"))
    if stage == "high" and subject in CN_HIGH_NAMES:
        for subdir in ("high", "all"):
            p = cn_root / subdir / CN_HIGH_NAMES[subject]
            if p.is_file():
                sources.append((p, f"books/课标-整理版/cn/{subdir}/{CN_HIGH_NAMES[subject]}"))
    if subject == "info-tech":
        for rel in ("books/课标-整理版/cn/high/信息技术.md", "books/课标-整理版/cn/all/信息技术_high.md"):
            p = WORKSPACE / rel
            if p.is_file():
                sources.append((p, rel))

    for rel in OPENSTAX_SOURCES.get(subject, []):
        p = WORKSPACE / rel
        if p.is_file():
            sources.append((p, rel))

    # Preserve order and de-duplicate.
    out: list[tuple[Path, str]] = []
    seen: set[Path] = set()
    for p, label in sources:
        if p not in seen:
            seen.add(p)
            out.append((p, label))
    return out


def source_chunks(path: Path, cache: dict[Path, list[str]]) -> list[str]:
    if path not in cache:
        cache[path] = split_chunks(path.read_text(encoding="utf-8", errors="replace"))
    return cache[path]


def snippets_from_existing_excerpts(data: dict[str, Any], cn_kw: list[str], en_kw: list[str]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for ex in data.get("excerpts") or []:
        if not isinstance(ex, dict):
            continue
        if ex.get("source_type") != "textbook" and ex.get("type") != "textbook":
            continue
        text = clean(str(ex.get("text") or ""))
        if not valid_chunk(text):
            continue
        score, hits = score_chunk(text, cn_kw, en_kw)
        out.append({
            "source": ex.get("source") or "kp-json#excerpts",
            "text": text[:1600],
            "score": score + 20,
            "match_terms": hits,
            "source_type": "existing_textbook_excerpt",
        })
    return out


def find_snippets(data: dict[str, Any], cache: dict[Path, list[str]], max_items: int = 4) -> list[dict[str, Any]]:
    cn_kw, en_kw = keywords_for(data)
    candidates = snippets_from_existing_excerpts(data, cn_kw, en_kw)
    for path, label in candidate_sources(data):
        for chunk in source_chunks(path, cache):
            score, hits = score_chunk(chunk, cn_kw, en_kw)
            if score < 12:
                continue
            candidates.append({
                "source": label,
                "text": chunk[:1600],
                "score": score,
                "match_terms": hits,
                "source_type": "local_textbook_markdown",
            })
    # De-duplicate by text prefix.
    dedup: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in sorted(candidates, key=lambda x: x["score"], reverse=True):
        key = item["text"][:180]
        if key in seen:
            continue
        seen.add(key)
        dedup.append(item)
        if len(dedup) >= max_items:
            break
    return dedup


def backfill_curriculum(data: dict[str, Any], stats: Counter[str]) -> bool:
    changed = False
    cps = [str(x).strip() for x in data.get("curriculum_points") or [] if str(x).strip()]
    excerpts = [x for x in data.get("excerpts") or [] if isinstance(x, dict) and str(x.get("text") or "").strip()]
    existing_texts = {str(x.get("text") or "").strip() for x in excerpts}

    # First backfill excerpts from existing curriculum_points.
    for cp in cps:
        if len(excerpts) >= 2:
            break
        if cp and cp not in existing_texts:
            excerpts.append({"text": cp, "source": "curriculum_points", "type": "curriculum_point", "id": f"bf-cp-{len(excerpts)+1}"})
            existing_texts.add(cp)
            changed = True
            stats["backfilled_excerpts_from_cp"] += 1

    raw = (data.get("supplements") or {}).get("curriculum_md_raw") or ""
    raw_lines = [clean(x) for x in re.split(r"\n+|[。；;]", raw) if len(clean(x)) >= 30]
    for line in raw_lines:
        if len(excerpts) >= 2 and len(cps) >= 2:
            break
        if GENERIC_RE.search(line) or PLACEHOLDER_RE.search(line):
            continue
        if len(cps) < 2 and line not in cps:
            cps.append(line[:220])
            changed = True
            stats["backfilled_curriculum_points_from_md"] += 1
        if len(excerpts) < 2 and line not in existing_texts:
            excerpts.append({"text": line[:500], "source": "curriculum_md_raw", "type": "curriculum_backfill", "id": f"bf-md-{len(excerpts)+1}"})
            existing_texts.add(line)
            changed = True
            stats["backfilled_excerpts_from_md"] += 1

    if changed:
        data["curriculum_points"] = cps
        data["excerpts"] = excerpts
    return changed


def worked_example(data: dict[str, Any], snippets: list[dict[str, Any]]) -> dict[str, Any]:
    subject = data.get("subject") or ""
    name = data.get("name") or data.get("kp_id") or "本知识点"
    first = snippets[0]["text"][:260] if snippets else ""
    if subject == "math":
        stem = f"根据教材片段，构造一道关于「{name}」的建模或计算题，并说明解题步骤。"
        outline = "先识别变量和数量关系，再建立表达式、图形或方程，最后解释结果在情境中的含义。"
    elif subject in {"physics", "chemistry", "biology", "science"}:
        stem = f"根据教材片段，设计一道关于「{name}」的现象解释或实验探究题。"
        outline = "先描述现象或实验条件，再指出关键概念和证据，最后给出解释或结论。"
    elif subject == "geography":
        stem = f"根据教材片段，设计一道关于「{name}」的读图或区域分析题。"
        outline = "先提取图文资料中的位置、分布或数据，再分析地理联系，最后形成判断。"
    elif subject == "history":
        stem = f"根据教材片段，设计一道关于「{name}」的材料分析题。"
        outline = "先提取材料信息，再联系背景、过程和影响，最后用证据支持历史解释。"
    elif subject == "english":
        stem = f"Based on the textbook snippet, create a context task for {name}."
        outline = "Use the target language point in context; explain form, meaning and use."
    elif subject == "chinese":
        stem = f"根据教材片段，设计一道关于「{name}」的阅读赏析或表达题。"
        outline = "先回到文本材料，再分析语言特点、内容理解和表达效果。"
    else:
        stem = f"根据教材片段，设计一道关于「{name}」的应用题。"
        outline = "先提取材料信息，再说明概念依据和应用过程。"
    return {"stem": stem, "solution_outline": outline, "evidence_excerpt": first, "source": SOURCE_TAG}


def backup_file(path: Path, backup_root: Path) -> None:
    target = backup_root / path.relative_to(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def is_cn(data: dict[str, Any], node: dict[str, Any]) -> bool:
    return (data.get("curriculum") or node.get("curriculum")) == "cn"


def process(args: argparse.Namespace) -> dict[str, Any]:
    kp_index = load_json(KP_INDEX_PATH).get("kps", {})
    node_index = load_json(NODE_INDEX_PATH).get("nodes", {}) if NODE_INDEX_PATH.exists() else {}
    subjects = set(args.subject or [])
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = Path(args.backup_dir) if args.backup_dir else KP_ROOT / "_backups" / f"deep-textbook-cn-{run_id}"
    cache: dict[Path, list[str]] = {}
    stats: Counter[str] = Counter()
    by_subject: dict[str, Counter[str]] = defaultdict(Counter)
    changed_files: list[str] = []

    for kp_id, rel in sorted(kp_index.items()):
        path = ROOT / rel
        if not path.is_file():
            continue
        data = load_json(path)
        node = node_index.get(kp_id, {})
        if not is_cn(data, node):
            continue
        subject = data.get("subject") or node.get("subject") or "other"
        if subjects and subject not in subjects:
            continue
        before = json.dumps(data, ensure_ascii=False, sort_keys=True)
        by_subject[subject]["seen"] += 1

        backfill_curriculum(data, stats)
        snippets = find_snippets(data, cache, args.max_snippets)
        if snippets:
            sup = data.setdefault("supplements", {})
            sup["deep_textbook_snippets"] = snippets
            sup["deep_textbook_source"] = SOURCE_TAG
            sup["deep_textbook_enriched_at"] = utc_now()
            sup["deep_worked_example"] = worked_example(data, snippets)
            tc = data.setdefault("textbook_content", {})
            tc["deep_snippets"] = snippets[:3]
            tc["deep_source"] = SOURCE_TAG
            stats["nodes_with_deep_snippets"] += 1
            stats["deep_snippets_added"] += len(snippets)
            by_subject[subject]["deep"] += 1
        else:
            by_subject[subject]["no_deep_match"] += 1

        after = json.dumps(data, ensure_ascii=False, sort_keys=True)
        if before != after:
            changed_files.append(str(path.relative_to(ROOT)))
            by_subject[subject]["changed"] += 1
            if not args.dry_run:
                backup_file(path, backup_root)
                dump_json(path, data)
                stats["written_files"] += 1
            else:
                stats["would_write_files"] += 1

    report = {
        "run_at": utc_now(),
        "dry_run": args.dry_run,
        "backup_dir": str(backup_root.relative_to(ROOT)) if backup_root.is_relative_to(ROOT) else str(backup_root),
        "stats": dict(stats),
        "by_subject": {k: dict(v) for k, v in sorted(by_subject.items())},
        "changed_files_count": len(changed_files),
        "changed_files_sample": changed_files[:80],
    }
    if not args.dry_run:
        backup_root.mkdir(parents=True, exist_ok=True)
        (backup_root / "deep-textbook-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Deep textbook enrichment for CN KP satellites")
    parser.add_argument("--subject", action="append", help="limit to subject; can repeat")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--backup-dir", default="")
    parser.add_argument("--max-snippets", type=int, default=4)
    args = parser.parse_args()
    print(json.dumps(process(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
