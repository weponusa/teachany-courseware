#!/usr/bin/env python3
"""List CN curriculum leaf nodes missing courseware.

Usage:
  python3 list-cn-gaps.py
  python3 list-cn-gaps.py --stage high --subject info-tech
  python3 list-cn-gaps.py --export gaps.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KP_ROOT = ROOT / "data" / "kp"
TREE_ROOT = ROOT / "data" / "trees" / "cn"


def load_registry() -> set[str]:
    reg = json.loads((ROOT / "registry.json").read_text(encoding="utf-8"))
    ids = {c["id"] for c in reg if isinstance(c, dict) and c.get("id")}
    ids |= {p.name for p in (ROOT / "community").iterdir() if p.is_dir()}
    return ids


def has_course(node: dict, known: set[str]) -> bool:
    nid = node.get("id", "")
    if nid in known:
        return True
    return any(cid in known for cid in (node.get("courses") or []))


def is_leaf(node: dict) -> bool:
    nid = node.get("id", "")
    if not nid or nid.startswith("ext-"):
        return False
    if node.get("grade") is None and not any(
        nid.startswith(p)
        for p in ("chn-", "math-", "eng-", "sci-", "bio-", "chem-", "phys-", "hist-", "geo-", "pol-", "info-", "it-")
    ):
        return False
    return True


def find_kp(node_id: str) -> Path | None:
    for sub in KP_ROOT.iterdir():
        p = sub / f"{node_id}.json"
        if p.is_file():
            return p
    return None


def collect_gaps(stage: str = "", subject: str = "") -> list[dict]:
    known = load_registry()
    gaps = []
    for tree_path in sorted(TREE_ROOT.rglob("*.json")):
        st = tree_path.parts[tree_path.parts.index("cn") + 1]
        subj = tree_path.stem
        if stage and st != stage:
            continue
        if subject and subj != subject:
            continue
        data = json.loads(tree_path.read_text(encoding="utf-8"))

        def walk(obj):
            if isinstance(obj, dict):
                if is_leaf(obj) and not has_course(obj, known):
                    kp = find_kp(obj["id"])
                    gaps.append({
                        "node_id": obj["id"],
                        "name": obj.get("name", ""),
                        "name_en": obj.get("name_en", ""),
                        "stage": st,
                        "subject": subj,
                        "grade": obj.get("grade"),
                        "kp_path": str(kp.relative_to(ROOT)) if kp else None,
                    })
                for v in obj.values():
                    if isinstance(v, (dict, list)):
                        walk(v)
            elif isinstance(obj, list):
                for item in obj:
                    walk(item)

        walk(data)
    return gaps


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="", help="elementary|middle|high")
    ap.add_argument("--subject", default="", help="e.g. history, english")
    ap.add_argument("--export", help="Write JSON array to file")
    args = ap.parse_args()
    gaps = collect_gaps(args.stage, args.subject)
    if args.export:
        Path(args.export).write_text(json.dumps(gaps, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Exported {len(gaps)} gaps → {args.export}")
    else:
        from collections import Counter

        c = Counter((g["stage"], g["subject"]) for g in gaps)
        print(f"Total missing leaf nodes: {len(gaps)}")
        for k, n in c.most_common():
            print(f"  {k[0]:8s} {k[1]:12s} {n}")
        if args.stage or args.subject:
            for g in gaps:
                print(f"  {g['node_id']:40s} {g['name']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
