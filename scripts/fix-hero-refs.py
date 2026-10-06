#!/usr/bin/env python3
"""修复 56 个课件的空 hero 引用：./assets/<id>-hero.png（不存在）
→ ./assets/hero-infographic.webp（已存在、带中文标注的知识结构图），
并移除配对的 HTML 叠标层（ta-figure-tags，避免与图内标注双重叠加）。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMMUNITY = ROOT / "community"

report = json.load(open("/tmp/real_missing.json"))
fails = report
only = sys.argv[1] if len(sys.argv) > 1 else None

fixed = 0
for cid in fails:
    if only and only not in cid:
        continue
    d = COMMUNITY / cid
    f = d / "index.html"
    html = f.read_text(encoding="utf-8", errors="replace")
    missing_ref = f"./assets/{cid}-hero.png"
    if missing_ref not in html:
        print(f"⚠️  {cid}: 引用不存在于html，跳过")
        continue
    # 替代资产优先级：带标注的信息图 > 封面图
    for cand in ("hero-infographic.webp", "hero.webp"):
        if (d / "assets" / cand).is_file():
            replacement = f"./assets/{cand}"
            break
    else:
        print(f"⚠️  {cid}: 无替代 hero 资产，跳过")
        continue
    # 1) 换引用
    html = html.replace(missing_ref, replacement)
    # 2) 移除叠标层（仅 ta-figure-tags，内容是纯 span 无嵌套 div）
    html, n = re.subn(
        r'\s*<div class="ta-figure-tags"[^>]*>[\s\S]*?</div>',
        "",
        html,
    )
    f.write_text(html, encoding="utf-8")
    fixed += 1
    print(f"✏️  {cid}: 引用→{replacement}, 移除叠标层×{n}")

print(f"\n修复 {fixed}/{len(fails)}")
