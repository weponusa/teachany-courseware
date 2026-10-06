#!/usr/bin/env python3
"""为全科图谱节点生成 display_name（中文主显示名），并同步 nodes-metadata。"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "data/knowledge-map-data.json"
META_PATH = ROOT / "data/nodes-metadata.json"


def load_translator():
    import importlib.machinery

    loader = importlib.machinery.SourceFileLoader("translate_local", str(ROOT / "scripts/translate-local.py"))
    mod = __import__("importlib.util").util.module_from_spec(
        __import__("importlib.util").util.spec_from_loader("translate_local", loader)
    )
    loader.exec_module(mod)
    return mod.translate_name


def has_cjk(text: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", text or ""))


def resolve_display_name(node: dict, translate_name) -> str:
    name = str(node.get("name") or "").strip()
    name_en = str(node.get("name_en") or "").strip()
    name_zh = str(node.get("name_zh") or "").strip()

    if has_cjk(name):
        return name
    if has_cjk(name_zh):
        return name_zh
    src = name_en or name
    if src:
        cn = translate_name(src)
        if has_cjk(cn):
            return cn
    return name or name_en or node.get("id", "")


def main() -> int:
    translate_name = load_translator()
    data = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    updated = 0
    for node in data.get("nodes") or []:
        dn = resolve_display_name(node, translate_name)
        if node.get("display_name") != dn:
            node["display_name"] = dn
            updated += 1
        if has_cjk(dn) and not has_cjk(node.get("name", "")):
            if not node.get("name_en"):
                node["name_en"] = node.get("name") or ""
            node["name"] = dn

    MAP_PATH.write_text(json.dumps(data, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"✅ knowledge-map-data.json: display_name 更新 {updated} 节点")

    if META_PATH.is_file():
        meta = json.loads(META_PATH.read_text(encoding="utf-8"))
        nodes_list = meta.get("nodes", []) if isinstance(meta, dict) else meta
        by_id = {n["id"]: n for n in data["nodes"] if n.get("id")}
        meta_updated = 0
        for entry in nodes_list:
            if not isinstance(entry, dict) or not entry.get("id"):
                continue
            src = by_id.get(entry["id"])
            if not src:
                continue
            dn = src.get("display_name") or src.get("name")
            if entry.get("display_name") != dn or entry.get("name") != src.get("name"):
                entry["display_name"] = dn
                if has_cjk(src.get("name", "")):
                    entry["name"] = src["name"]
                    if src.get("name_en"):
                        entry["name_en"] = src["name_en"]
                meta_updated += 1
        META_PATH.write_text(json.dumps(meta, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"✅ nodes-metadata.json: 同步 {meta_updated} 条")

    cn = sum(1 for n in data["nodes"] if has_cjk(n.get("display_name") or n.get("name", "")))
    print(f"   中文可显示名: {cn}/{len(data['nodes'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
