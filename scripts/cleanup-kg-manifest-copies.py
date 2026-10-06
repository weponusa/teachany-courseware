#!/usr/bin/env python3
"""Remove per-course teachany-kg-manifest.json copies (use site root CDN instead)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

removed = 0
for p in COMMUNITY.glob("*/assets/scripts/teachany-kg-manifest.json"):
    p.unlink()
    removed += 1
print(f"Removed {removed} per-course teachany-kg-manifest.json copies")
