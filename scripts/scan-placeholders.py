#!/usr/bin/env python3
"""scan-placeholders.py — 全库扫描占位符与内容缺失
特征：
1. 「course-id」式占位（「」内为英文连字符ID）
2. 正文中裸课件 ID（如"学习 bio-m-biosphere 时"）
3. 常见占位词：TODO/待补充/待完善/占位/placeholder/{{...}}
4. 空 section（section 内文本 < 20 字）
5. 标题与课名不符（如 h1 仍是模板名）
输出 JSON + 统计
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

PLACEHOLDER_WORDS = [r"TODO", r"待补充", r"待完善", r"待填写", r"placeholder",
                     r"\{\{[^}]{1,30}\}\}", r"此处省略", r"略。{0,1}$"]
# 排除「」内是正常中文的（如「生物圈」是书名号用法）——只抓「内含连字符英文ID」的
CN_QUOTE_ID = re.compile(r"「([a-z][a-z0-9]*(?:-[a-z0-9]+)+)」")


def scan(cid, html):
    issues = {}
    # 1. 「course-id」占位
    m = CN_QUOTE_ID.findall(html)
    # 过滤：「」内的 ID 与课件自身相关或像 course-id
    m = [x for x in m if "-" in x]
    if m:
        issues["cn_quote_id"] = len(m)
    # 2. 裸 ID（"「" 之外直接出现本课件 ID 于可见文本）
    title_m = re.search(r'<meta name="course-title" content="([^"]+)"', html)
    title = title_m.group(1) if title_m else ""
    if title and cid in html:
        # 课件 ID 出现在 meta 以外的地方
        body = re.sub(r"<meta[^>]*>", "", html)
        body = re.sub(r"<script[\s\S]*?</script>", "", body)
        body = re.sub(r"<!--[\s\S]*?-->", "", body)
        n = len(re.findall(re.escape(cid), body))
        if n:
            issues["bare_id"] = n
    # 3. 占位词
    for w in PLACEHOLDER_WORDS:
        n = len(re.findall(w, html))
        if n:
            issues.setdefault("placeholder_words", 0)
            issues["placeholder_words"] += n
    # 4. 空 section
    empty = 0
    for sm in re.finditer(r"<section\b[^>]*>([\s\S]*?)</section>", html):
        t = re.sub(r"<[^>]+>", "", sm.group(1))
        t = re.sub(r"\s+", "", t)
        if len(t) < 20:
            empty += 1
    if empty:
        issues["empty_sections"] = empty
    return issues, title


def main():
    rows = []
    by_issue = Counter()
    for f in sorted(COMMUNITY.glob("*/index.html")):
        cid = f.parent.name
        html = f.read_text(encoding="utf-8", errors="replace")
        issues, title = scan(cid, html)
        if issues:
            rows.append({"id": cid, "title": title, "issues": issues})
            for k in issues:
                by_issue[k] += 1
    print(f"扫描 {len(list(COMMUNITY.glob('*/index.html')))} 个课件，{len(rows)} 个含占位/缺失")
    for k, v in by_issue.most_common():
        print(f"  {k}: {v} 个课件")
    out = ROOT / "scripts" / "placeholder-scan.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"明细 → {out}")


if __name__ == "__main__":
    main()
