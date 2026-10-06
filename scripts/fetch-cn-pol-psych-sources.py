#!/usr/bin/env python3
"""下载并落盘中国小学道法/心理课标与教材目录资料。"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "curriculum-sources" / "cn"
WEB_FETCH = Path.home() / ".claude/skills/web-fetch/SKILL.md"

SOURCES = [
    {
        "url": "http://www.moe.gov.cn/srcsite/A06/s3325/201212/t20121211_145679.html",
        "out": OUT / "psychology-2012-moe.html",
        "note": "中小学心理健康教育指导纲要（2012年修订）",
    },
]


def utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch_url(url: str, dest: Path) -> bool:
    try:
        r = subprocess.run(
            ["curl", "-fsSL", "-A", "TeachAny-curriculum-bot/1.0", url],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if r.returncode == 0 and r.stdout.strip():
            dest.write_text(r.stdout, encoding="utf-8")
            return True
    except Exception as e:
        print(f"  [WARN] curl failed {url}: {e}")
    return False


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "generated_at": utc(),
        "files": [
            "morality-law-2022-outline.md",
            "psychology-2012-outline.md",
            "pep-politics-textbooks.json",
            "pep-politics-textbooks-middle.json",
            "pep-politics-textbooks-high.json",
        ],
        "fetched": [],
    }

    for item in SOURCES:
        dest = item["out"]
        print(f"Fetching {item['note']} …")
        if fetch_url(item["url"], dest):
            manifest["fetched"].append({"url": item["url"], "path": str(dest.relative_to(ROOT))})
            print(f"  ✅ {dest.name}")
        else:
            print(f"  ⚠️  skip (use local outline.md)")

    (OUT / "_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"✅ curriculum sources ready under {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
