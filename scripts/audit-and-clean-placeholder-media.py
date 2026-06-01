#!/usr/bin/env python3
"""Audit and optionally remove placeholder media in community/ courseware.

Placeholders: zero-byte audio, tiny mp4 (<8KB), tiny images (<1KB),
and identical 1292-byte mp3 stubs (edge-tts silence template).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
MEDIA_EXTS = {".mp3", ".mp4", ".png", ".jpg", ".jpeg", ".webp", ".gif"}


def file_kind(path: Path) -> str | None:
    ext = path.suffix.lower()
    return ext if ext in MEDIA_EXTS else None


def classify(path: Path) -> str | None:
    ext = path.suffix.lower()
    try:
        size = path.stat().st_size
    except OSError:
        return None
    if ext == ".mp3" and size == 0:
        return "zero_mp3"
    if ext == ".mp4" and size < 8192:
        return "tiny_mp4"
    if ext in (".png", ".jpg", ".jpeg", ".webp", ".gif") and size < 1024:
        return "tiny_image"
    if ext == ".mp3" and size < 2048:
        return "tiny_mp3"
    return None


def md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def collect() -> tuple[list[Path], dict[str, list[Path]]]:
    remove: list[Path] = []
    by_reason: dict[str, list[Path]] = {
        "zero_mp3": [],
        "tiny_mp4": [],
        "tiny_image": [],
        "tiny_mp3_stub": [],
    }
    stub_hash = "6e8ebfba8299710c9db6da970ea02a4a"  # known 1292B template

    for path in sorted(COMMUNITY.rglob("*")):
        if not path.is_file() or file_kind(path) is None:
            continue
        reason = classify(path)
        if reason == "tiny_mp3":
            if md5(path) == stub_hash:
                by_reason["tiny_mp3_stub"].append(path)
                remove.append(path)
            continue
        if reason:
            by_reason[reason].append(path)
            remove.append(path)
    return remove, by_reason


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Delete matched files (default: dry-run report only)",
    )
    parser.add_argument(
        "--json",
        type=Path,
        help="Write audit report JSON to this path",
    )
    args = parser.parse_args()

    remove, by_reason = collect()
    report = {
        "root": str(COMMUNITY),
        "counts": {k: len(v) for k, v in by_reason.items()},
        "total_remove": len(remove),
        "files": {k: [str(p.relative_to(ROOT)) for p in v] for k, v in by_reason.items()},
    }

    print(json.dumps(report["counts"], indent=2))
    for reason, paths in by_reason.items():
        if not paths:
            continue
        print(f"\n## {reason} ({len(paths)})")
        for p in paths[:20]:
            print(f"  {p.relative_to(ROOT)}")
        if len(paths) > 20:
            print(f"  ... +{len(paths) - 20} more")

    if args.json:
        args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nWrote {args.json}")

    if not remove:
        print("\nNo placeholder files to remove.")
        return 0

    if not args.apply:
        print(f"\nDry-run: would remove {len(remove)} files. Re-run with --apply to delete.")
        return 0

    for path in remove:
        path.unlink()
        print(f"removed {path.relative_to(ROOT)}")
    print(f"\nRemoved {len(remove)} placeholder files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
