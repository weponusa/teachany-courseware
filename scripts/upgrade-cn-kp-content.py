#!/usr/bin/env python3
"""全量升级中国课标 KP 卫星内容：课标树同步 + 教材摘录 + 替换模板习题/易错点。

步骤：
  1. 从 data/trees 同步真实 curriculum_points / excerpt_ids
  2. deep-textbook-enrich：本地教材/课标 MD 摘录
  3. 清除 cn-curriculum-common 模板习题/易错点/AI 讲解摘要
  4. 灌入学科化 exercises / errors / real_world（优先结合 deep snippets）

用法：
  python3 scripts/upgrade-cn-kp-content.py --dry-run
  python3 scripts/upgrade-cn-kp-content.py
  python3 scripts/upgrade-cn-kp-content.py --subject math
"""
from __future__ import annotations

import argparse
import glob
import importlib.util
import json
import os
import re
import shutil
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
KP_ROOT = ROOT / "data" / "kp"
KP_INDEX_PATH = KP_ROOT / "_index.json"
NODE_INDEX_PATH = ROOT / "data" / "node-index.json"
UPGRADE_TAG = "kp_content_upgrade_2026-06-22"

GENERIC_CP_RE = re.compile(
    r"学段目标：理解并掌握|学业要求：能在真实情境中识别|活动建议：通过观察、实验"
)
TEMPLATE_EX_ANS = {
    "应答覆盖课标要点，体现掌握与应用。",
    "需写出关键概念、过程或方法，避免只背结论。",
    "须体现区域文明特征与交流，避免西方中心论或简单优劣评判。",
}
AI_SUMMARY_RE = re.compile(r"由课标要点生成|教材化讲解参考")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def collect_tree_nodes() -> dict[str, dict[str, Any]]:
    nodes: dict[str, dict[str, Any]] = {}
    for f in glob.glob(str(ROOT / "data/trees/*/**/*.json"), recursive=True):
        rel = os.path.relpath(f, ROOT)
        parts = rel.split("/")
        if len(parts) < 5 or parts[2] == "other":
            continue
        try:
            d = json.loads(Path(f).read_text(encoding="utf-8"))
        except Exception:
            continue
        for dom in d.get("domains", []):
            for n in dom.get("nodes", []):
                nid = n.get("id")
                if not nid:
                    continue
                nodes[nid] = {
                    "curriculum_points": [str(x).strip() for x in (n.get("curriculum_points") or []) if str(x).strip()],
                    "excerpt_ids": n.get("excerpt_ids") or [],
                    "name": n.get("name", nid),
                }
    return nodes


def cp_needs_tree_sync(data: dict[str, Any], tree: dict[str, Any] | None) -> bool:
    if not tree or not tree.get("curriculum_points"):
        return False
    cps = [str(x) for x in (data.get("curriculum_points") or [])]
    real = [c for c in cps if not GENERIC_CP_RE.search(c) and len(c) >= 12]
    tree_cps = tree["curriculum_points"]
    if not real:
        return True
    if set(real) != set(tree_cps) and len(tree_cps) >= len(real):
        return True
    return False


def sync_from_tree(data: dict[str, Any], tree: dict[str, Any]) -> bool:
    changed = False
    tree_cps = tree["curriculum_points"]
    if tree_cps and cp_needs_tree_sync(data, tree):
        data["curriculum_points"] = tree_cps
        data["excerpts"] = [
            {"id": f"cp-{i}", "text": cp, "source": "国家课标·内容要求", "type": "curriculum_point"}
            for i, cp in enumerate(tree_cps, 1)
        ]
        changed = True
    if tree.get("excerpt_ids"):
        if data.get("excerpt_ids") != tree["excerpt_ids"]:
            data["excerpt_ids"] = tree["excerpt_ids"]
            changed = True
    return changed


def is_template_exercise(ex: dict[str, Any]) -> bool:
    src = str(ex.get("source") or "")
    stem = str(ex.get("stem") or "")
    ans = str(ex.get("answer") or "")
    if src.startswith("cn-curriculum"):
        return True
    if ans in TEMPLATE_EX_ANS:
        return True
    if re.search(r"依据课标「|请结合实例说明|比较说明：", stem):
        return True
    if re.search(r"说明「.+」在文明多元格局中的位置", stem):
        return True
    return False


def is_template_error(err: dict[str, Any]) -> bool:
    src = str(err.get("source") or "")
    if src.startswith("cn-curriculum"):
        return True
    if src == "cn-curriculum-pedagogy" and len(str(err.get("description") or "")) < 80:
        return False  # 历史价值观类可保留
    return src in ("cn-curriculum", "cn-curriculum-common")


def fallback_snippets(data: dict[str, Any]) -> list[dict[str, Any]]:
    """课标原文 / 已注入课标摘录 — 无本地教材匹配时的可追溯兜底。"""
    out: list[dict[str, Any]] = []
    tc = data.get("textbook_content")
    if isinstance(tc, dict):
        for key in ("section_excerpt", "content_excerpt", "teaching_guidance"):
            val = tc.get(key)
            texts: list[str] = []
            if isinstance(val, str):
                texts = [val]
            elif isinstance(val, list):
                texts = [str(x) for x in val if isinstance(x, str)]
            for text in texts:
                text = text.strip()
                if len(text) >= 120 and not AI_SUMMARY_RE.search(text):
                    out.append({
                        "source": f"textbook_content.{key}",
                        "text": text[:1600],
                        "score": 30,
                        "match_terms": [],
                        "source_type": "curriculum_standard_excerpt",
                    })
                    break
            if out:
                break
    for cp in data.get("curriculum_points") or []:
        cp = str(cp).strip()
        if len(cp) < 30 or GENERIC_CP_RE.search(cp):
            continue
        out.append({
            "source": "国家课标·内容要求",
            "text": cp[:1600],
            "score": 20,
            "match_terms": [],
            "source_type": "curriculum_standard_excerpt",
        })
        if len(out) >= 4:
            break
    return out[:4]


def exercises_from_deep(clean_mod, deep_mod, data: dict[str, Any], snippets: list[dict]) -> list[dict[str, Any]]:
    subject = data.get("subject") or ""
    name = data.get("name") or data.get("kp_id") or ""
    cps = clean_mod.curriculum_points(data)
    out: list[dict[str, Any]] = []
    if snippets:
        we = deep_mod.worked_example(data, snippets)
        out.append({
            "id": "q-deep-1",
            "stem": we["stem"],
            "answer": we["solution_outline"],
            "type": "application",
            "source": UPGRADE_TAG,
            "evidence_source": snippets[0].get("source", ""),
        })
    templates = clean_mod.exercise_templates(subject, name, cps)
    for i, t in enumerate(templates[:2], start=len(out) + 1):
        out.append({**t, "id": f"q-subj-{i}", "source": UPGRADE_TAG})
    return out[:3]


def backup_file(path: Path, backup_root: Path) -> None:
    target = backup_root / path.relative_to(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def process(args: argparse.Namespace) -> dict[str, Any]:
    clean = load_module("clean_enrich", ROOT / "scripts/clean-and-enrich-cn-kp.py")
    deep = load_module("deep_enrich", ROOT / "scripts/deep-textbook-enrich-cn-kp.py")

    kp_index = load_json(KP_INDEX_PATH).get("kps", {})
    node_index = load_json(NODE_INDEX_PATH).get("nodes", {}) if NODE_INDEX_PATH.exists() else {}
    tree_nodes = collect_tree_nodes()
    subjects = set(args.subject or [])
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = Path(args.backup_dir) if args.backup_dir else KP_ROOT / "_backups" / f"upgrade-cn-kp-{run_id}"
    cache: dict[Path, list[str]] = {}
    stats: Counter[str] = Counter()
    by_subject: dict[str, Counter[str]] = defaultdict(Counter)

    for kp_id, rel in sorted(kp_index.items()):
        if "_backups" in rel:
            continue
        path = ROOT / rel
        if not path.is_file():
            continue
        data = load_json(path)
        node = node_index.get(kp_id, {})
        if (data.get("curriculum") or node.get("curriculum")) != "cn":
            continue
        subject = data.get("subject") or node.get("subject") or "other"
        if subjects and subject not in subjects:
            continue
        by_subject[subject]["seen"] += 1
        before = json.dumps(data, ensure_ascii=False, sort_keys=True)
        changed = False

        if sync_from_tree(data, tree_nodes.get(kp_id, {})):
            stats["synced_cp_from_tree"] += 1
            changed = True

        deep.backfill_curriculum(data, stats)
        snippets = deep.find_snippets(data, cache, args.max_snippets)
        if not snippets:
            snippets = fallback_snippets(data)
            if snippets:
                stats["fallback_curriculum_snippets"] += 1
        sup = data.setdefault("supplements", {})

        if snippets:
            sup["deep_textbook_snippets"] = snippets
            sup["deep_textbook_source"] = deep.SOURCE_TAG
            sup["deep_textbook_enriched_at"] = deep.utc_now()
            sup["deep_worked_example"] = deep.worked_example(data, snippets)
            tc = data.setdefault("textbook_content", {})
            if isinstance(tc, dict):
                tc["deep_snippets"] = snippets[:3]
                tc["deep_source"] = deep.SOURCE_TAG
            stats["nodes_with_deep_snippets"] += 1
            by_subject[subject]["deep"] += 1

        # 清除 AI 占位摘要
        summary = sup.get("textbook_summary")
        if isinstance(summary, str) and (AI_SUMMARY_RE.search(summary) or clean.bad_textbook_text(summary)):
            sup.pop("textbook_summary", None)
            sup.pop("textbook_summary_source", None)
            stats["removed_ai_textbook_summary"] += 1
            changed = True

        clean.clean_derived_fields(data, subject, stats)

        exercises = data.get("exercises") or []
        needs_ex = (
            not exercises
            or all(isinstance(e, dict) and is_template_exercise(e) for e in exercises)
            or (snippets and not any(str(e.get("id") or "") == "q-deep-1" for e in exercises if isinstance(e, dict)))
        )
        if needs_ex and snippets:
            data["exercises"] = exercises_from_deep(clean, deep, data, snippets)
            stats["replaced_exercises"] += 1
            changed = True
        elif needs_ex:
            data["exercises"] = exercises_from_deep(clean, deep, data, [])
            stats["replaced_exercises"] += 1
            changed = True

        errors = data.get("errors") or []
        if not errors or all(isinstance(e, dict) and is_template_error(e) for e in errors):
            name = data.get("name") or kp_id
            data["errors"] = clean.error_templates(subject, name)
            for e in data["errors"]:
                if isinstance(e, dict):
                    e["source"] = UPGRADE_TAG
            stats["replaced_errors"] += 1
            changed = True

        if not data.get("real_world"):
            data["real_world"] = clean.real_world_examples(subject, data.get("name") or kp_id)
            stats["added_real_world"] += 1
            changed = True

        meta = data.setdefault("_meta", {})
        sources = list(meta.get("sources") or [])
        if UPGRADE_TAG not in sources:
            sources.append(UPGRADE_TAG)
        meta["sources"] = sources
        meta["kp_content_upgrade_at"] = utc_now()

        after = json.dumps(data, ensure_ascii=False, sort_keys=True)
        if before != after or changed:
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
    }
    if not args.dry_run:
        backup_root.mkdir(parents=True, exist_ok=True)
        (backup_root / "upgrade-report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description="全量升级 CN KP 内容")
    ap.add_argument("--subject", action="append")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--backup-dir", default="")
    ap.add_argument("--max-snippets", type=int, default=4)
    args = ap.parse_args()
    report = process(args)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
