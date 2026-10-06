#!/usr/bin/env python3
"""classify-svg-refs.py — 定性 appscene_svg 命中的 SVG 是通用占位还是真学科图"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
rows = json.load(open(ROOT / "scripts/fake-modules-scan-v2.json", encoding="utf-8"))
svg_ids = [r["id"] for r in rows if "appscene_svg" in r["hits"]]
GENERIC = ["观察现象", "建立模型", "解释机制", "预测结果", "先看变量", "再看规则",
           "输入变量", "输出指标", "变量、规则、结果"]
generic, real, missing = [], [], []
for cid in svg_ids:
    d = ROOT / "community" / cid / "assets"
    texts = ""
    for svg in d.glob("*.svg") if d.exists() else []:
        if svg.name in ("process-diagram.svg", "application-scene.svg"):
            texts += svg.read_text(encoding="utf-8", errors="replace")
    if not texts:
        missing.append(cid)
    elif any(g in texts for g in GENERIC):
        generic.append(cid)
    else:
        real.append(cid)
print("通用占位SVG:", len(generic))
for c in generic:
    print("  ", c)
print("真学科SVG:", len(real))
for c in real[:8]:
    print("  ", c)
print("SVG缺失:", len(missing), missing)
