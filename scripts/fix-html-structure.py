#!/usr/bin/env python3
"""Repair legacy HTML structure errors in community courseware pages.

Two classes of defects left by earlier bulk-upgrade scripts:

1. Stray closing tags: extra ``</section>`` / ``</div>`` that never had a
   matching opener (browsers silently recover, but slide navigation and
   any DOM-range logic can misbehave).
2. Duplicate ``id`` values (e.g. ``tb-autoplay`` toolbars injected twice).
   ``getElementById`` already resolves to the first node, so renaming later
   occurrences preserves behaviour while restoring document validity.

Idempotent: running twice makes no further changes.
"""
from __future__ import annotations

import collections
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKIP_REGION = re.compile(r"<!--.*?-->|<script\b.*?</script>|<style\b.*?</style>", re.S | re.I)


def masked_spans(source: str) -> list[tuple[int, int]]:
    return [m.span() for m in SKIP_REGION.finditer(source)]


def in_masked(pos: int, spans: list[tuple[int, int]]) -> bool:
    for start, end in spans:
        if start <= pos < end:
            return True
        if start > pos:
            break
    return False


def drop_stray_closers(source: str, tag: str) -> tuple[str, int]:
    spans = masked_spans(source)
    pattern = re.compile(r"<%s[\s>]|</%s>" % (tag, tag), re.I)
    depth = 0
    stray: list[tuple[int, int]] = []
    for m in pattern.finditer(source):
        if in_masked(m.start(), spans):
            continue
        if m.group().startswith("</"):
            if depth == 0:
                stray.append(m.span())
            else:
                depth -= 1
        else:
            depth += 1
    if not stray:
        return source, 0
    out = []
    cursor = 0
    for start, end in stray:
        out.append(source[cursor:start])
        cursor = end
    out.append(source[cursor:])
    return "".join(out), len(stray)


def close_dangling_openers(source: str, tag: str) -> tuple[str, int]:
    """Append missing closers at end of body.

    Browsers already recover by closing the element at document end, so this
    keeps the rendered DOM identical while making the markup well-formed.
    """
    spans = masked_spans(source)
    pattern = re.compile(r"<%s[\s>]|</%s>" % (tag, tag), re.I)
    depth = 0
    for m in pattern.finditer(source):
        if in_masked(m.start(), spans):
            continue
        if m.group().startswith("</"):
            depth = max(0, depth - 1)
        else:
            depth += 1
    if depth == 0:
        return source, 0
    patch = f"</{tag}>" * depth
    idx = source.rfind("</body>")
    if idx < 0:
        return source + patch + "\n", depth
    return source[:idx] + patch + "\n" + source[idx:], depth


def dedupe_ids(source: str) -> tuple[str, int]:
    spans = masked_spans(source)
    seen: collections.Counter[str] = collections.Counter()
    edits: list[tuple[int, int, str]] = []
    for m in re.finditer(r'\sid="([^"]+)"', source):
        if in_masked(m.start(), spans):
            continue
        value = m.group(1)
        seen[value] += 1
        if seen[value] > 1:
            edits.append((m.start(1), m.end(1), f"{value}-dup{seen[value] - 1}"))
    if not edits:
        return source, 0
    out = []
    cursor = 0
    for start, end, replacement in edits:
        out.append(source[cursor:start])
        out.append(replacement)
        cursor = end
    out.append(source[cursor:])
    return "".join(out), len(edits)


def repair(path: Path) -> dict[str, int]:
    source = path.read_text(encoding="utf-8")
    original = source
    counts = {}
    for tag in ("section", "div"):
        source, dropped = drop_stray_closers(source, tag)
        if dropped:
            counts[f"stray_{tag}"] = dropped
        source, closed = close_dangling_openers(source, tag)
        if closed:
            counts[f"unclosed_{tag}"] = closed
    source, renamed = dedupe_ids(source)
    if renamed:
        counts["dup_id"] = renamed
    if source != original:
        path.write_text(source, encoding="utf-8")
    return counts


def main(argv: list[str]) -> int:
    targets = argv[1:]
    if targets:
        files = [ROOT / "community" / t / "index.html" for t in targets]
    else:
        files = sorted(ROOT.glob("community/*/index.html"))
    changed = 0
    totals: collections.Counter[str] = collections.Counter()
    for path in files:
        if not path.exists():
            print(f"MISS {path}")
            continue
        counts = repair(path)
        if counts:
            changed += 1
            totals.update(counts)
            detail = ", ".join(f"{k}={v}" for k, v in sorted(counts.items()))
            print(f"FIX {path.parent.name}: {detail}")
    print(f"done: {changed} files repaired of {len(files)}; totals {dict(totals)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
