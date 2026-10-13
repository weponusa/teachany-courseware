#!/usr/bin/env python3
"""Fix unreadable text in slide-v2 dark cards.

Some legacy pages wrapped old sections into slide-page containers. Their top
ABT cards use inline `background:#1e293b`, while paragraph text still inherits
`--text:#1e293b`; the result is dark text on a dark card. This patch injects a
small compatibility CSS block for those legacy slide pages.
"""
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIX_ID = "teachany-slide-dark-card-fix"
FIX_CSS = f"""
<style id="{FIX_ID}">
/* Compatibility fix for legacy sections wrapped by slide-v2. */
.slide-container [style*="background:#1e293b"],
.slide-container [style*="background: #1e293b"],
.slide-container [style*="background:#0f172a"],
.slide-container [style*="background: #0f172a"] {{
  color: #e5edf8 !important;
}}
.slide-container [style*="background:#1e293b"] p,
.slide-container [style*="background: #1e293b"] p,
.slide-container [style*="background:#0f172a"] p,
.slide-container [style*="background: #0f172a"] p,
.slide-container [style*="background:#1e293b"] li,
.slide-container [style*="background: #1e293b"] li,
.slide-container [style*="background:#0f172a"] li,
.slide-container [style*="background: #0f172a"] li {{
  color: #e5edf8 !important;
}}
.slide-container [style*="background:#1e293b"] strong,
.slide-container [style*="background: #1e293b"] strong,
.slide-container [style*="background:#0f172a"] strong,
.slide-container [style*="background: #0f172a"] strong {{
  color: #ffffff !important;
}}
.slide-container .slide-page > .section p,
.slide-container .slide-page > section p {{
  color: inherit;
}}
</style>
""".strip()


def needs_fix(text: str) -> bool:
    return "slide-container" in text and ("background:#1e293b" in text or "background: #1e293b" in text or "background:#0f172a" in text or "background: #0f172a" in text)


def apply(path: pathlib.Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not needs_fix(text):
        return False
    if FIX_ID in text:
        return False
    if "</head>" in text:
        text = text.replace("</head>", FIX_CSS + "\n</head>", 1)
    else:
        text = FIX_CSS + "\n" + text
    path.write_text(text, encoding="utf-8")
    return True


def main() -> None:
    changed = []
    for path in sorted((ROOT / "community").glob("*/index.html")):
        if apply(path):
            changed.append(path.parent.name)
    print(f"changed={len(changed)}")
    for cid in changed:
        print(cid)


if __name__ == "__main__":
    main()
