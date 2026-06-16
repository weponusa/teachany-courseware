#!/usr/bin/env python3
"""Runtime QC: map geojson files exist + KG manifest has node_id.

Usage:
  python3 qc-runtime-modules.py
  python3 qc-runtime-modules.py community/geo-m-four-regions
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

MAP_CONFIG_RE = re.compile(
    r'<script type="application/json" data-teachany-map-config>\s*([\s\S]*?)\s*</script>',
    re.I,
)
KG_ID_RE = re.compile(r'data-teachany-kg=["\']([^"\']+)["\']', re.I)


def map_file_exists(course_dir: Path, fname: str) -> bool:
    if not fname or fname.startswith("http"):
        return True
    direct = course_dir / "assets" / "maps" / fname
    if direct.is_file():
        return True
    maps_dir = course_dir / "assets" / "maps"
    if not maps_dir.is_dir():
        return False
    return bool(list(maps_dir.rglob(Path(fname).name)))


def check_one(course_dir: Path) -> list[str]:
    errors: list[str] = []
    nid = course_dir.name
    idx = course_dir / "index.html"
    if not idx.is_file():
        return [f"{nid}: missing index.html"]

    html = idx.read_text(encoding="utf-8", errors="replace")

    if "data-teachany-map" in html:
        m = MAP_CONFIG_RE.search(html)
        if not m:
            errors.append(f"{nid}: data-teachany-map but no config JSON")
        else:
            try:
                cfg = json.loads(m.group(1))
            except json.JSONDecodeError:
                errors.append(f"{nid}: invalid map config JSON")
                cfg = {}
            for era in cfg.get("eras", []):
                f = era.get("file", "")
                if f and not map_file_exists(course_dir, f):
                    errors.append(f"{nid}: map era file missing: {f}")
            for ov in cfg.get("overlays", []):
                f = ov.get("file", "")
                if f and not map_file_exists(course_dir, f):
                    errors.append(f"{nid}: map overlay missing: {f}")
        if not (course_dir / "assets/scripts/teachany-historical-map.js").is_file():
            errors.append(f"{nid}: missing teachany-historical-map.js")

    kg_ids = KG_ID_RE.findall(html)
    if kg_ids:
        mf = course_dir / "assets/scripts/teachany-kg-manifest.json"
        uses_cdn_manifest = "/assets/scripts/teachany-knowledge-graph" in html
        if not mf.is_file() and not uses_cdn_manifest:
            errors.append(f"{nid}: missing local teachany-kg-manifest.json and no CDN KG script path")
        elif mf.is_file():
            try:
                manifest = json.loads(mf.read_text(encoding="utf-8"))
                nodes = manifest.get("nodes") or {}
                for kid in set(kg_ids):
                    if kid not in nodes:
                        errors.append(f"{nid}: kg node not in manifest: {kid}")
            except json.JSONDecodeError:
                errors.append(f"{nid}: invalid teachany-kg-manifest.json")
        if not (course_dir / "assets/scripts/teachany-knowledge-graph.js").is_file():
            errors.append(f"{nid}: missing teachany-knowledge-graph.js")

    return errors


def main() -> int:
    if len(sys.argv) > 1:
        targets = []
        for arg in sys.argv[1:]:
            p = Path(arg)
            if not p.is_absolute():
                p = ROOT / p
            targets.append(p)
    else:
        targets = [
            d for d in sorted(COMMUNITY.iterdir())
            if d.is_dir() and (d / "index.html").is_file() and (d / "manifest.json").is_file()
        ]

    all_errors: list[str] = []
    for d in targets:
        all_errors.extend(check_one(d))

    print(f"扫描 {len(targets)} 个课件")
    print(f"❌ 运行时错误: {len(all_errors)}")
    for msg in all_errors[:50]:
        print(f"   {msg}")
    if len(all_errors) > 50:
        print(f"   … 另有 {len(all_errors) - 50} 条")

    if all_errors:
        sys.exit(1)
    print("\n✅ 地图/知识图谱运行时 QC 通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
