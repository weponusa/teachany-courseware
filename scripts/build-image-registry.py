#!/usr/bin/env python3
"""从 registry.json + CDN 命名规则生成 skill/assets/image-registry.json。

供 find-hero.py L1 与 image_resolver.py audit 使用。
可重复运行；合并 match_nodes，不删除已有手工条目。

用法:
  python3 scripts/build-image-registry.py
  python3 scripts/build-image-registry.py --write-opensource
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "skill" / "assets" / "image-registry.json"
COURSE_REGISTRY_PATH = ROOT / "registry.json"
CDN_BASE = "https://cdn.jsdelivr.net/gh/weponusa/teachany-images@main"

SUBJECT_TO_DIR = {
    "math": "math",
    "chinese": "chinese",
    "english": "english",
    "biology": "biology",
    "physics": "physics",
    "chemistry": "chemistry",
    "history": "history",
    "geography": "geography",
    "science": "science",
    "politics": "politics",
    "info-tech": "info-tech",
    "cs": "cs",
}

# CDN 上有图但课件用了别的 hero 文件名 — 显式挂 node_id
CDN_EXTRA: List[Tuple[str, str, str, str]] = [
    # (cdn_file, node_id, course_id, subject)
    ("biology/cell-membrane-hero.png", "bio-h-cell-membrane", "bio-h-cell-membrane", "biology"),
    ("biology/cell-metabolism-hero.png", "bio-h-cell-metabolism", "bio-h-cell-metabolism", "biology"),
    ("biology/elements-compounds-hero.png", "bio-h-elements-compounds", "bio-h-elements-compounds", "biology"),
    ("biology/endomembrane-system-hero.png", "bio-h-endomembrane-system", "bio-h-endomembrane-system", "biology"),
    ("biology/nucleus-hero.png", "bio-h-nucleus", "bio-h-nucleus", "biology"),
    ("biology/organelles-hero.png", "bio-h-organelles", "bio-h-organelles", "biology"),
    ("biology/photosynthesis-m-hero.png", "bio-m-photosynthesis-m", "bio-m-photosynthesis-m", "biology"),
    ("biology/prokaryote-eukaryote-hero.png", "bio-h-prokaryote-eukaryote", "bio-h-prokaryote-eukaryote", "biology"),
    ("chemistry/aluminum-compounds-hero.png", "chem-h-aluminum-compounds", "chem-h-aluminum-compounds", "chemistry"),
    ("chemistry/ib-dp-periodic-table-hero.png", "chem-ib-dp-periodic-table", "chem-ib-dp-periodic-table", "chemistry"),
    ("chemistry/oxidation-reduction-hero.png", "chem-h-oxidation-reduction", "chem-oxidation-reduction", "chemistry"),
    ("chemistry/periodic-table-hero.png", "chem-m-periodic-table", "chem-periodic-table", "chemistry"),
    ("geography/monsoon-system-hero.png", "geo-h-monsoon-system", "geo-h-monsoon-system", "geography"),
    ("science/plant-life-cycle-hero.png", "sci-e-plant-life-cycle", "sci-e-plant-life-cycle", "science"),
]


def resolve_subject(subject: Optional[str]) -> str:
    if not subject:
        return "science"
    s = subject.lower().strip()
    return SUBJECT_TO_DIR.get(s, s)


def _extract_tags(node_id: str) -> List[str]:
    parts = re.split(r"[-_]", node_id)
    skip = {"math", "bio", "chem", "phy", "geo", "hist", "chn", "eng", "sci", "m", "h", "e"}
    tags = [p for p in parts if len(p) >= 3 and p not in skip]
    tags.append("hero")
    return tags


def _today() -> str:
    return date.today().isoformat()


def _entry_key(file_path: str, slot: str) -> str:
    return f"{file_path}::{slot}"


def upsert(
    by_key: Dict[str, Dict[str, Any]],
    file_path: str,
    node_id: str,
    course_id: str,
    subject: str,
    grade: Optional[int],
    generator: str = "batch-openrouter",
) -> None:
    slot = "hero"
    key = _entry_key(file_path, slot)
    nodes = {node_id}
    if course_id and course_id != node_id:
        nodes.add(course_id)

    stem = Path(file_path).stem
    image_id = stem if stem.startswith(subject) else f"{subject}-{stem}"

    if key in by_key:
        existing = by_key[key]
        merged = set(existing.get("match_nodes", [])) | nodes
        existing["match_nodes"] = sorted(merged)
        return

    entry: Dict[str, Any] = {
        "id": image_id,
        "file": file_path,
        "url": f"{CDN_BASE}/{file_path}",
        "subject": subject,
        "tags": _extract_tags(node_id),
        "slot": slot,
        "match_nodes": sorted(nodes),
        "size": "1024x1024",
        "quality": "medium",
        "style": "natural",
        "generator": generator,
        "generated": True,
        "created": _today(),
    }
    if grade is not None:
        entry["grade"] = grade
    by_key[key] = entry


def build_from_courses(courses: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    by_key: Dict[str, Dict[str, Any]] = {}

    for c in courses:
        hid = (c.get("hero_image") or "").strip()
        if not hid or not re.search(r"-hero\.(png|webp|jpg|jpeg)$", hid, re.I):
            continue

        basename = Path(hid).name
        subject = resolve_subject(c.get("subject"))
        subj_dir = SUBJECT_TO_DIR.get(subject, subject)
        node_id = c.get("node_id") or c["id"]
        course_id = c["id"]
        grade = c.get("grade")
        if isinstance(grade, str) and grade.isdigit():
            grade = int(grade)

        file_path = f"{subj_dir}/{basename}"
        upsert(by_key, file_path, node_id, course_id, subject, grade)

    for file_path, node_id, course_id, subject in CDN_EXTRA:
        c = next((x for x in courses if x["id"] == course_id), {})
        grade = c.get("grade")
        if isinstance(grade, str) and grade.isdigit():
            grade = int(grade)
        upsert(by_key, file_path, node_id, course_id, subject, grade)

    return by_key


def merge_existing(by_key: Dict[str, Dict[str, Any]], existing: Dict[str, Any]) -> None:
    for img in existing.get("images", []):
        fp = img.get("file", "")
        slot = img.get("slot", "hero")
        if not fp:
            continue
        key = _entry_key(fp, slot)
        if key not in by_key:
            by_key[key] = img
        else:
            merged_nodes = set(by_key[key].get("match_nodes", [])) | set(img.get("match_nodes", []))
            by_key[key]["match_nodes"] = sorted(merged_nodes)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write-opensource",
        action="store_true",
        help="同步到 teachany-opensource/teachany/skill/assets/",
    )
    args = parser.parse_args()

    with COURSE_REGISTRY_PATH.open(encoding="utf-8") as f:
        data = json.load(f)
    courses = data.get("courses", data) if isinstance(data, dict) else data

    existing: Dict[str, Any] = {"version": "3.0", "images": []}
    if REGISTRY_PATH.exists():
        existing = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    by_key = build_from_courses(courses)
    merge_existing(by_key, existing)

    out = {
        "version": "3.0",
        "cdn_base": CDN_BASE,
        "updated": _today(),
        "description": "TeachAny CDN hero 图索引；由 build-image-registry.py 从 registry.json 生成",
        "images": sorted(by_key.values(), key=lambda x: x.get("file", "")),
    }

    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"✅ wrote {REGISTRY_PATH}")
    print(f"   entries: {len(out['images'])}")

    if args.write_opensource:
        oss = ROOT.parent / "teachany-opensource" / "teachany" / "skill" / "assets" / "image-registry.json"
        orphans_doc = REGISTRY_PATH.parent / "HERO_CDN_ORPHANS.md"
        oss.parent.mkdir(parents=True, exist_ok=True)
        oss.write_text(REGISTRY_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"✅ synced {oss}")
        if orphans_doc.exists():
            oss_orphan = oss.parent / "HERO_CDN_ORPHANS.md"
            oss_orphan.write_text(orphans_doc.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"✅ synced {oss_orphan}")

    # quick audit hint
    hero_slots = sum(1 for i in out["images"] if i.get("slot") == "hero")
    print(f"   slot=hero: {hero_slots}")


if __name__ == "__main__":
    main()
