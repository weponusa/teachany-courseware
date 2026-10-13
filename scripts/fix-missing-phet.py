#!/usr/bin/env python3
"""为 phy-m 升级课件补插缺失的 PhET iframe 区块（catalog 配方）。"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
CATALOG = ROOT / "data" / "phy-m-upgrade-catalog.json"


def phet_block(meta: dict) -> str:
    slug = meta["slug"]
    url = f"https://phet.colorado.edu/sims/html/{slug}/latest/{slug}_zh_CN.html"
    title = meta.get("title", "PhET 仿真")
    hint = meta.get("hint", "按提示操作，记录现象与结论。")
    return f'''
<section class="slide-page" data-page-index="9b" data-page-type="content" data-tsh="PhET 网络仿真">
<section class="section" id="phet-lab" data-tts="phet-lab" data-bloom-level="apply" data-scaffold="partial" data-interactive="phet">
  <div class="lesson-panel">
    <span class="phase-tag">网络仿真 · PhET</span>
    <h2>{title}</h2>
    <div class="iframe-wrap">
      <iframe src="{url}" title="{title}" allowfullscreen loading="lazy"
        sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
        referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
    <p class="feedback" style="margin-top:12px">💡 {hint}</p>
    <p style="font-size:12px;color:#64748b;margin:8px 0 0">外链：<a href="{url}" target="_blank" rel="noopener">{url}</a></p>
  </div>
</section>
</section>
'''


def needs_phet(html: str) -> bool:
    return "phet.colorado.edu" not in html or 'id="phet-lab"' not in html


def insert_phet(html: str, block: str) -> tuple[str, bool]:
    if 'id="phet-lab"' in html and "phet.colorado.edu" in html:
        return html, False
    anchor = '<section class="section" id="practice-l1"'
    if anchor not in html:
        anchor = 'id="practice-l1"'
    if anchor not in html:
        return html, False
    return html.replace(anchor, block.strip() + "\n\n" + anchor, 1), True


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    fixed = 0
    skipped = 0
    for cfg in catalog["courses"]:
        cid = cfg["id"]
        path = COMMUNITY / cid / "index.html"
        if not path.exists():
            print(f"SKIP {cid}: no index.html")
            skipped += 1
            continue
        html = path.read_text(encoding="utf-8")
        if not needs_phet(html):
            skipped += 1
            continue
        if "phet" not in cfg:
            print(f"SKIP {cid}: no phet in catalog")
            skipped += 1
            continue
        html2, ok = insert_phet(html, phet_block(cfg["phet"]))
        if not ok:
            print(f"FAIL {cid}: cannot find practice-l1 anchor")
            continue
        path.write_text(html2, encoding="utf-8")
        fixed += 1
        print(f"FIXED {cid}")
    print(f"\nDone: fixed={fixed} skipped={skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
