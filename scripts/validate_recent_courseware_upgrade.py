#!/usr/bin/env python3
"""Anti-shell validation for the recent large TeachAny courseware batches.

This complements the legacy completeness gates. It checks the two issues found
in the May 2026 audit:
1) new pages must use teachany-slide-v2 paged/PPT mode;
2) generated lessons must include a knowledge-specific evidence section and not
   rely on repeated generic scaffolding phrases.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET_TREES = [
    ("cn/high/chemistry.json", "chemistry"),
    ("cn/high/physics.json", "physics"),
    ("cn/high/geography.json", "geography"),
    ("cn/middle/physics.json", "physics"),
    ("cn/middle/chinese.json", "chinese"),
]
EXCLUDE_IDS = {"chem-h-aluminum-compounds"}
GENERIC_PHRASES = [
    "学习本课时，先明确",
    "不能只凭印象回答",
    "不是背模板",
    "先判断任务",
    "从实验现象到变量关系",
    "先观察现象，再控制变量",
    "用地图、图表和过程证据",
    "不是孤立知识点",
    "不是单纯换一个题目名称",
    "换一个场景，仍然从",
    "任务识别—圈画证据—解释方法—组织答案",
]


def load_targets() -> list[dict]:
    targets = []
    seen = set()
    for rel, subject in TARGET_TREES:
        p = ROOT / "data/trees" / rel
        data = json.loads(p.read_text(encoding="utf-8"))
        level = rel.split("/")[1]
        for domain in data.get("domains", []):
            for node in domain.get("nodes", []):
                cid = node.get("id")
                if not cid or cid in seen or cid in EXCLUDE_IDS:
                    continue
                html = ROOT / "community" / cid / "index.html"
                if html.exists():
                    html_text = html.read_text(encoding="utf-8", errors="ignore")
                    if 'http-equiv="refresh"' in html_text or "location.replace('../" in html_text:
                        continue
                    seen.add(cid)
                    targets.append({"id": cid, "subject": subject, "level": level, "name": node.get("name") or cid, "html": html})
    return targets


def check(target: dict) -> dict:
    text = target["html"].read_text(encoding="utf-8", errors="ignore")
    generic_hits = sum(text.count(p) for p in GENERIC_PHRASES)
    slide_pages = text.count('class="slide-page"')
    section_count = len(re.findall(r'<section\b', text, re.I))
    has_slide = all(x in text for x in ["teachany-slide-v2.css", "teachany-slide-v2.js", 'id="slide-container"', 'class="slide-page"'])
    has_controls = all(x in text for x in ['id="play-mode-fab"', 'id="slide-toolbar"', 'id="slide-sidenav"', 'id="slide-progress-bar"'])
    has_evidence = all(x in text for x in ["knowledge-specific-evidence", "specificity-table", "课堂任务"])
    has_interaction = bool(re.search(r'<canvas\b|<iframe\b|data-anchor-choice|ai-media-zone', text, re.I))
    errors = []
    if not has_slide:
        errors.append("missing_slide_v2")
    if not has_controls:
        errors.append("missing_slide_controls")
    if slide_pages < 8:
        errors.append(f"too_few_slide_pages:{slide_pages}")
    if not has_evidence:
        errors.append("missing_specific_evidence")
    if generic_hits > 2:
        errors.append(f"generic_phrase_hits:{generic_hits}")
    if not has_interaction:
        errors.append("missing_interaction")
    return {**{k: target[k] for k in ["id", "subject", "level", "name"]}, "slide_pages": slide_pages, "sections": section_count, "generic_hits": generic_hits, "has_slide": has_slide, "has_controls": has_controls, "has_evidence": has_evidence, "has_interaction": has_interaction, "errors": errors}


def main() -> int:
    rows = [check(t) for t in load_targets()]
    failures = [r for r in rows if r["errors"]]
    by_group = defaultdict(list)
    for row in rows:
        by_group[(row["level"], row["subject"])].append(row)
    print(f"checked={len(rows)} failures={len(failures)}")
    for key, arr in sorted(by_group.items()):
        print("GROUP", key, "n=", len(arr), "slide_ok=", sum(r["has_slide"] for r in arr), "evidence_ok=", sum(r["has_evidence"] for r in arr), "avg_generic=", round(sum(r["generic_hits"] for r in arr)/len(arr), 2))
    if failures:
        print("\nFAILURES")
        for row in failures[:80]:
            print(row["id"], row["subject"], row["errors"])
    out = ROOT / "reports/recent-courseware-upgrade-validation-2026-05-28.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print("REPORT_JSON", out)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
