#!/usr/bin/env python3
"""
构建 GitHub 开源知识图谱/题库的公开发布合规增强层。

数据源（全部可公开发布）：
  - Open Knowledge Graph  : CC BY-SA 4.0（内容）— 15,290 概念 / 19 学科 / 70,333 内置题
  - rainewhk/gaokao       : Apache-2.0 — 3,126 道高考九科真题（带解析）
  - CMATH (weitianwen)    : CC BY 4.0 — 1,698 道小学数学应用题

红线（与 data/external/cn-math-taxonomy 一致）：
  1. 只读外部源与本地权威树；绝不修改 data/trees/** / data/kp/** / knowledge-map-data.json
  2. 不写 curriculum_points（课标原文只由检索库逐字带出）
  3. 外部前置关系一律 review=candidate，不做权威边
  4. 输出独立 overlay，带 NOTICE，前端可静默降级
  5. NC 授权源（K12-KGraph / CJEval / cn-math-taxonomy 题库正文）一律不引入

输出：data/external/open-kg/
  topics.json       OKG 概念索引（按中文课标学科过滤）
  questions.json    三源合并题库（统一 schema，带授权字段）
  alignment.json    TeachAny kp ↔ OKG topic 分级对齐
  report.json       统计与质量报告
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OKG_DIR = "/Users/wepon/CodeBuddy/一次函数/_kg-resources/open-knowledge-graph"
GAOKAO_DIR = "/tmp/gaokao-src/dataset"
CMATH_FILES = ["/tmp/cmath_test.jsonl", "/tmp/cmath_dev.jsonl"]
KP_DIR = os.path.join(ROOT, "data", "kp")
OUT_DIR = os.path.join(ROOT, "data", "external", "open-kg")

# 中文课标 10 学科对齐的 OKG domain
DOMAIN_TO_SUBJECT = {
    "mathematics": "math",
    "physics": "physics",
    "chemistry": "chemistry",
    "biology": "biology",
    "earth-and-space-sciences": "geography",
    "history": "history",
    "language-and-communication": "chinese",
    "literature": "chinese",
    "social-sciences": "politics",
    "economics": "politics",
    "formal-sciences-and-logic": "math",
    "computer-science": "info-tech",
    "engineering": "engineering",
    "health-and-human-development": "biology",
    "psychology": "psychology",
    "arts-and-aesthetics": "art",
    "music": "music",
    "philosophy": "politics",
    "practical-life-skills": "science",
}
SUBJECT_TO_DOMAIN = defaultdict(set)
for d, s in DOMAIN_TO_SUBJECT.items():
    SUBJECT_TO_DOMAIN[s].add(d)

# 中文名 → 英文词项锚点（用于 name_en 粗粒度英译的兜底）
CN_TERM_MAP = {
    "数学": ["mathematics", "math", "algebra", "geometry", "calculus", "function", "number", "statistics", "probability"],
    "物理": ["physics", "force", "motion", "energy", "electricity", "magnetism", "wave", "optics", "thermal", "mechanics"],
    "化学": ["chemistry", "atom", "molecule", "bond", "acid", "base", "reaction", "solution", "electrochemistry", "organic"],
    "生物": ["biology", "cell", "genetics", "ecosystem", "photosynthesis", "evolution", "organism", "anatomy", "enzyme"],
    "地理": ["geography", "earth", "climate", "weather", "map", "ocean", "atmosphere", "plate", "tectonic"],
    "历史": ["history", "civilization", "dynasty", "war", "revolution", "empire", "ancient", "medieval"],
    "语文": ["language", "literature", "writing", "reading", "grammar", "composition", "poetry", "vocabulary"],
    "英语": ["language", "english", "grammar", "vocabulary", "reading", "writing"],
    "政治": ["politics", "economics", "society", "government", "philosophy", "ethics", "law", "civics"],
    "科学": ["science", "experimental", "inquiry", "engineering", "technology"],
    "心理健康": ["psychology", "emotion", "behavior", "memory", "cognitive", "development"],
}

STOP = {"the", "a", "an", "of", "and", "or", "to", "in", "for", "with", "on", "at", "is", "are", "basics", "introduction", "overview"}


def parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}
    try:
        fm = yaml.safe_load(m.group(1))
        return fm if isinstance(fm, dict) else {}
    except yaml.YAMLError:
        return {}


def extract_section(text: str, heading: str) -> str:
    m = re.search(rf"^##\s+{re.escape(heading)}\s*\n(.*?)(?=^##\s|\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def parse_okg_questions(topic_id: str, text: str) -> list[dict]:
    block = extract_section(text, "Questions")
    if not block:
        return []
    fm = re.search(r"```ya?ml\s*\n(.*?)\n```", block, re.S)
    if not fm:
        return []
    try:
        qs = yaml.safe_load(fm.group(1))
    except yaml.YAMLError:
        return []
    if not isinstance(qs, list):
        return []
    out = []
    for i, q in enumerate(qs):
        if not isinstance(q, dict) or not q.get("question"):
            continue
        out.append({
            "id": f"okg-{topic_id}-q{i + 1}",
            "topic_id": topic_id,
            "stem": str(q["question"]).strip(),
            "type": str(q.get("type") or "short-answer"),
            "options": q.get("options") if isinstance(q.get("options"), list) else None,
            "answer": q.get("answer"),
            "explanation": str(q.get("explanation") or "").strip(),
            "language": "en",
            "subject": None,
            "stage": None,
            "grade": None,
            "license": "CC BY-SA 4.0",
            "source": "open-knowledge-graph",
            "source_url": "https://github.com/open-knowledge-graph/okg",
        })
    return out


def tokens(s: str) -> set[str]:
    return {w for w in re.sub(r"[^a-z0-9]+", " ", str(s).lower()).split() if w and w not in STOP and len(w) > 2}


def load_kp_index() -> list[dict]:
    out = []
    for path in glob.glob(os.path.join(KP_DIR, "**", "*.json"), recursive=True):
        base = os.path.basename(path)
        if base.startswith("_") or os.sep + "_backups" + os.sep in path:
            continue
        try:
            with open(path, encoding="utf-8") as f:
                d = json.load(f)
        except (OSError, ValueError):
            continue
        if d.get("curriculum") != "cn":
            continue
        out.append({
            "kp_id": d.get("kp_id"),
            "name": d.get("name") or "",
            "name_en": d.get("name_en") or "",
            "subject": d.get("subject") or "",
            "stage": d.get("stage") or "",
            "grade": d.get("grade"),
        })
    return out


def build_alignment(topics: dict, kps: list[dict]) -> list[dict]:
    # domain → topic ids
    by_domain: dict[str, list[str]] = defaultdict(list)
    for tid, t in topics.items():
        by_domain[t["domain"]].append(tid)
    # 全局词项索引
    title_tokens: dict[str, set[str]] = {tid: tokens(t["title"]) for tid, t in topics.items()}

    rows = []
    for kp in kps:
        wanted_domains = SUBJECT_TO_DOMAIN.get(kp["subject"], set())
        if not wanted_domains:
            continue
        # 候选池：同学科 topic
        pool = [tid for d in wanted_domains for tid in by_domain.get(d, [])]
        if not pool:
            continue

        en_tok = tokens(kp["name_en"])
        cn_tok = set()
        for w in CN_TERM_MAP.get(kp["name"], []):
            cn_tok.update(tokens(w))
        # name_en 粗英译本身可能就是学科词（如 "Mass"），补充学科锚点
        subject_anchor = set()
        for w in CN_TERM_MAP.get(CN_SUBJECT.get(kp["subject"], ""), []):
            subject_anchor.update(tokens(w))

        scores = []
        for tid in pool:
            tt = title_tokens[tid]
            if not tt:
                continue
            # 精确词项命中
            exact = len(tt & (en_tok | cn_tok))
            # 学科锚点弱命中（只作为低置信兜底）
            anchor = len(tt & subject_anchor)
            if exact == 0 and anchor == 0:
                continue
            score = exact * 2 + anchor * 0.25
            scores.append((score, tid, exact, anchor))
        scores.sort(reverse=True)
        if not scores:
            continue
        # 取 top5；exact>0 才标 high，否则 candidate-low
        top = scores[:5]
        best_exact = max(s[2] for s in top)
        rows.append({
            "kp_id": kp["kp_id"],
            "kp_name": kp["name"],
            "kp_name_en": kp["name_en"],
            "subject": kp["subject"],
            "stage": kp["stage"],
            "grade": kp.get("grade"),
            "okg_topic_ids": [s[1] for s in top],
            "scores": [round(s[0], 2) for s in top],
            "match_type": "term_overlap" if best_exact > 0 else "subject_anchor_weak",
            "confidence": "high" if best_exact >= 2 else ("medium" if best_exact == 1 else "low"),
            "review": "candidate",
        })
    return rows


CN_SUBJECT = {
    "math": "数学", "physics": "物理", "chemistry": "化学", "biology": "生物",
    "geography": "地理", "history": "历史", "chinese": "语文", "english": "英语",
    "politics": "政治", "science": "科学", "psychology": "心理健康", "info-tech": "科学",
    "engineering": "科学", "art": "语文", "music": "语文",
}


def load_gaokao() -> list[dict]:
    out = []
    subj_map = {
        "数学": "math", "物理": "physics", "化学": "chemistry", "生物": "biology",
        "历史": "history", "地理": "geography", "政治": "politics",
        "语文": "chinese", "英语": "english",
    }
    for path in glob.glob(os.path.join(GAOKAO_DIR, "**", "*.jsonl"), recursive=True):
        # 路径形如 dataset/数学/2013/全国卷/选择题.jsonl → 学科在 dataset/ 下的第一段
        parts = path.replace("\\", "/").split("/")
        dataset_idx = parts.index("dataset") if "dataset" in parts else -1
        subject_cn = parts[dataset_idx + 1] if dataset_idx >= 0 and len(parts) > dataset_idx + 1 else ""
        subject = subj_map.get(subject_cn)
        if not subject:
            continue
        for line in open(path, encoding="utf-8"):
            if not line.strip():
                continue
            try:
                d = json.loads(line)
            except ValueError:
                continue
            q = str(d.get("question") or "").strip()
            if not q:
                continue
            out.append({
                "id": f"gaokao-{d.get('id') or len(out)}",
                "stem": q,
                "type": d.get("question_type") or "选择题",
                "options": None,
                "answer": d.get("answer"),
                "explanation": str(d.get("analysis") or "").strip(),
                "language": "zh",
                "subject": subject,
                "stage": "high",
                "grade": 12,
                "year": d.get("year"),
                "paper_type": d.get("paper_type"),
                "license": "Apache-2.0",
                "source": "rainewhk/gaokao (GAOKAO-Bench)",
                "source_url": "https://github.com/rainewhk/gaokao",
                "license_note": "仓库 Apache-2.0；试题原文版权归命题机构，仅供教学研究",
            })
    return out


def load_cmath() -> list[dict]:
    out = []
    for path in CMATH_FILES:
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                out.append({
                    "id": f"cmath-{len(out) + 1}",
                    "stem": str(d.get("question") or "").strip(),
                    "type": "应用题",
                    "options": None,
                    "answer": d.get("golden"),
                    "explanation": "",
                    "language": "zh",
                    "subject": "math",
                    "stage": "elementary",
                    "grade": d.get("grade"),
                    "license": "CC BY 4.0",
                    "source": "CMATH (weitianwen)",
                    "source_url": "https://huggingface.co/datasets/weitianwen/cmath",
                })
    return out


def main() -> int:
    os.makedirs(OUT_DIR, exist_ok=True)
    files = glob.glob(os.path.join(OKG_DIR, "domains", "**", "*.md"), recursive=True)
    if not files:
        print("ERROR: OKG 源目录为空", file=sys.stderr)
        return 1

    topics = {}
    okg_questions = []
    for path in files:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        fm = parse_frontmatter(text)
        tid = fm.get("id")
        if not tid:
            continue
        domain = str(fm.get("domain") or "")
        prereqs = []
        for p in fm.get("prerequisites") or []:
            if isinstance(p, dict) and p.get("id"):
                prereqs.append({"id": p["id"], "type": p.get("type") or "soft"})
        topics[str(tid)] = {
            "id": str(tid),
            "title": str(fm.get("title") or tid),
            "domain": domain,
            "subject": DOMAIN_TO_SUBJECT.get(domain, "other"),
            "course": str(fm.get("course") or ""),
            "stage": str(fm.get("stage") or ""),
            "status": str(fm.get("status") or ""),
            "prerequisites": prereqs,
            "rel_path": os.path.relpath(path, OKG_DIR),
        }
        okg_questions.extend(parse_okg_questions(str(tid), text))

    kps = load_kp_index()
    alignments = build_alignment(topics, kps)
    aligned_topic_ids = {t for r in alignments for t in r["okg_topic_ids"]}

    gaokao = load_gaokao()
    cmath = load_cmath()
    linked_okg = [q for q in okg_questions if q["topic_id"] in aligned_topic_ids]

    # 主题级题库：把 OKG 题挂到对齐它的 kp（candidate）
    questions = gaokao + cmath + linked_okg

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": [
            {"name": "Open Knowledge Graph", "url": "https://github.com/open-knowledge-graph/okg", "license": "CC BY-SA 4.0 (content) / MIT (tools)"},
            {"name": "rainewhk/gaokao", "url": "https://github.com/rainewhk/gaokao", "license": "Apache-2.0", "note": "试题原文版权归命题机构，仅供教学研究"},
            {"name": "CMATH", "url": "https://huggingface.co/datasets/weitianwen/cmath", "license": "CC BY 4.0"},
        ],
        "excluded_nc_sources": [
            "K12-KGraph (CC BY-NC-SA 4.0)", "CJEval (research only)",
            "cn-math-taxonomy 题库正文 (CC BY-NC 4.0)", "C-Eval dataset (CC BY-NC-SA 4.0)",
        ],
        "counts": {
            "okg_topics": len(topics),
            "okg_questions_total": len(okg_questions),
            "cn_kp_total": len(kps),
            "alignments": len(alignments),
            "alignments_high": sum(1 for r in alignments if r["confidence"] == "high"),
            "alignments_medium": sum(1 for r in alignments if r["confidence"] == "medium"),
            "aligned_topics": len(aligned_topic_ids),
            "questions_total": len(questions),
            "questions_by_source": dict(Counter(q["source"] for q in questions)),
            "questions_zh": sum(1 for q in questions if q["language"] == "zh"),
            "questions_en": sum(1 for q in questions if q["language"] == "en"),
        },
        "topics_by_subject": dict(Counter(t["subject"] for t in topics.values())),
        "review_policy": [
            "外部前置关系一律标 review=candidate，不得当权威边发布",
            "不写 curriculum_points；课标原文只由检索库逐字带出",
            "不修改 data/trees/**、data/kp/**、knowledge-map-data.json",
            "题库为旁挂参考；高考题版权归命题机构，商用前需法务确认边界",
        ],
    }

    def dump(name, data):
        p = os.path.join(OUT_DIR, name)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  {name}: {os.path.getsize(p) / 1024:.1f} KB")

    print("写出开源图谱增强层：")
    dump("topics.json", topics)
    dump("questions.json", questions)
    dump("alignment.json", alignments)
    dump("report.json", report)
    print(json.dumps(report["counts"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
