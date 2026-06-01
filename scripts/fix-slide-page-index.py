#!/usr/bin/env python3
"""Renumber data-page-index on slide-page sections in courseware index.html (0..n-1)."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OPEN_TAG = re.compile(
    r'(<section\s+class="slide-page[^"]*")'
    r'(?:\s+data-page-index="[^"]*")?'
    r'(\s+data-page-type="[^"]*")?',
    re.IGNORECASE,
)


def fix_html(text: str) -> tuple[str, int]:
    count = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal count
        idx = count
        count += 1
        rest = m.group(2) or ""
        return f'{m.group(1)} data-page-index="{idx}"{rest}'

    return OPEN_TAG.sub(repl, text), count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="index.html files (default: 3 CN history samples)")
    args = parser.parse_args()

    paths = args.paths or [
        ROOT / "community/ancient-china-h/index.html",
        ROOT / "community/hist-h-ancient-civ/index.html",
        ROOT / "community/hist-h-early-state/index.html",
    ]

    for path in paths:
        if not path.is_file():
            print(f"skip missing: {path}", file=sys.stderr)
            continue
        text = path.read_text(encoding="utf-8")
        new_text, n = fix_html(text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            print(f"{path.relative_to(ROOT)}: renumbered {n} slide pages")
        else:
            print(f"{path.relative_to(ROOT)}: unchanged ({n} pages)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
