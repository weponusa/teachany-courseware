#!/usr/bin/env python3
"""scan-placeholders-v2.py — 精确版占位/缺失扫描
1. cn_quote_id: 「course-id」占位
2. bare_id_visible: 可见文本裸课件ID（排除属性/script/style/「」内）
3. placeholder_visible: 可见文本占位词（排除 placeholder= 属性）
4. empty_sections: 排除挂载容器后的空 section
5. bad_title: title 嵌套《》、标题占位文本
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

MOUNT_IDS = re.compile(r"tutor|kg|knowledge|hint|audio|dock|feedback|progress|nav|hero-infographic|slide-progress|course-version|skill-version")
WORDS = [r"TODO", r"待补充", r"待完善", r"待填写", r"此处省略", r"内容待定", r"敬请期待"]
CN_QUOTE_ID = re.compile(r"「([a-z][a-z0-9]*(?:-[a-z0-9]+)+)」")


def visible_text(html):
    body = re.sub(r"<script[\s\S]*?</script>", "", html)
    body = re.sub(r"<style[\s\S]*?</style>", "", body)
    body = re.sub(r"<!--[\s\S]*?-->", "", body)
    return body


def scan(cid, html):
    issues = {}
    body = visible_text(html)
    # 1
    m = [x for x in CN_QUOTE_ID.findall(body) if "-" in x]
    if m:
        issues["cn_quote_id"] = len(m)
    # 2
    if cid and "-" in cid:
        n = 0
        for mm in re.finditer(re.escape(cid), body):
            prev = body[mm.start() - 1] if mm.start() > 0 else ""
            if prev in "「=\"'/.:":
                continue
            n += 1
        if n:
            issues["bare_id_visible"] = n
    # 3：占位词，只算标签外文本
    text_only = re.sub(r"<[^>]+>", " ", body)
    for w in WORDS:
        n = len(re.findall(w, text_only))
        if n:
            issues.setdefault("placeholder_visible", 0)
            issues["placeholder_visible"] += n
    # 4：空 section（排除挂载容器和 slide-page 封面）
    empty = 0
    for sm in re.finditer(r"<section\b([^>]*)>([\s\S]*?)</section>", html):
        attrs = sm.group(1)
        if MOUNT_IDS.search(attrs):
            continue
        t = re.sub(r"<[^>]+>", "", sm.group(2))
        t = re.sub(r"\s+", "", t)
        if len(t) < 20 and "<img" not in sm.group(2) and "<canvas" not in sm.group(2) \
           and "<video" not in sm.group(2) and "<figure" not in sm.group(2):
            empty += 1
    if empty:
        issues["empty_sections"] = empty
    # 5：title 异常
    tm = re.search(r"<title>([^<]+)</title>", html)
    if tm:
        t = tm.group(1)
        if "《《" in t or "正在打开" in t or t.count("TeachAny") > 1 and "《" in t and t.startswith("《《"):
            issues["bad_title"] = 1
    return issues


def main():
    rows = []
    by_issue = Counter()
    for f in sorted(COMMUNITY.glob("*/index.html")):
        cid = f.parent.name
        html = f.read_text(encoding="utf-8", errors="replace")
        issues = scan(cid, html)
        if issues:
            rows.append({"id": cid, "issues": issues})
            for k in issues:
                by_issue[k] += 1
    print(f"扫描 {len(list(COMMUNITY.glob('*/index.html')))} 个课件，{len(rows)} 个含问题")
    for k, v in by_issue.most_common():
        print(f"  {k}: {v} 个课件")
    out = ROOT / "scripts" / "placeholder-scan-v2.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"明细 → {out}")
    # 各问题课件示例
    for k in by_issue:
        ids = [r["id"] for r in rows if k in r["issues"]][:6]
        print(f"  [{k}] 例: {', '.join(ids)}")


if __name__ == "__main__":
    main()
