#!/usr/bin/env python3
"""scan-thin-courseware.py — 课件知识厚度扫描
度量：
1. 可见中文文本总量（去 script/style/标签）
2. 核心知识区文本量（lesson-focus/core-knowledge/精讲 section）
3. section 数量
输出：按文本量升序的分布 + 薄课件名单
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

CORE_PATTERNS = [
    r'id="lesson-focus"[\s\S]*?</section>',
    r'id="core-knowledge"[\s\S]*?</section>',
    r'id="core-concept"[\s\S]*?</section>',
    r'data-tsh="精讲[^"]*"[\s\S]*?</section>',
    r'data-tsh="核心知识[^"]*"[\s\S]*?</section>',
]


def measure(html):
    body = re.sub(r"<script[\s\S]*?</script>", "", html)
    body = re.sub(r"<style[\s\S]*?</style>", "", body)
    body = re.sub(r"<!--[\s\S]*?-->", "", body)
    text = re.sub(r"<[^>]+>", " ", body)
    cn = len(re.findall(r"[\u4e00-\u9fff]", text))
    core = ""
    for pat in CORE_PATTERNS:
        m = re.search(pat, html)
        if m:
            core += m.group(0) + "\n"
    core_cn = len(re.findall(r"[\u4e00-\u9fff]", re.sub(r"<[^>]+>", " ", core))) if core else 0
    n_sec = len(re.findall(r"<section\b", html))
    return cn, core_cn, n_sec


def main():
    rows = []
    for f in sorted(COMMUNITY.glob("*/index.html")):
        cid = f.parent.name
        html = f.read_text(encoding="utf-8", errors="replace")
        # 跳过重定向壳
        if 'http-equiv="refresh"' in html[:3000]:
            continue
        cn, core_cn, n_sec = measure(html)
        rows.append({"id": cid, "cn_chars": cn, "core_cn": core_cn, "sections": n_sec})
    rows.sort(key=lambda r: r["cn_chars"])
    out = ROOT / "scripts" / "thickness-scan.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    n = len(rows)
    print(f"{n} 个课件文本量分布：")
    for pct in (5, 10, 25, 50, 75, 95):
        r = rows[int(n * pct / 100)]
        print(f"  P{pct}: {r['cn_chars']} 字 ({r['id']})")
    print(f"\n最薄 30 个：")
    for r in rows[:30]:
        print(f"  {r['id']:44s} {r['cn_chars']:6d} 字 | 核心区 {r['core_cn']:5d} 字 | {r['sections']} sections")
    print(f"\n明细 → {out}")


if __name__ == "__main__":
    main()
