#!/usr/bin/env python3
"""从 cn-unified 课标树提取 domain 中文标签，供 knowledge-map.html 使用。"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TREES_DIR = ROOT / "data" / "trees" / "cn-unified"
OUT = ROOT / "data" / "knowledge-map-domain-labels.json"


def main() -> int:
    labels: dict[str, str] = {}
    for fp in sorted(TREES_DIR.glob("*.json")):
        if fp.name == "_index.json":
            continue
        data = json.loads(fp.read_text("utf-8"))
        for dom in data.get("domains", []) or []:
            did = dom.get("id") or dom.get("slug")
            name = dom.get("name") or dom.get("label")
            if did and name:
                labels[str(did)] = str(name)

    payload = {
        "version": "1.0",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(labels),
        "labels": labels,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ {OUT.name}: {len(labels)} 个 domain 标签")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
