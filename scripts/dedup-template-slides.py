#!/usr/bin/env python3
"""dedup-template-slides.py — 删除与真模块重复的模板 slide 壳
模板壳签名（整页删除）：
1. objectives 壳: "能说出X的核心概念与课标要求"
2. 问题锚点壳: "怎样用课标要求的方法学习"
3. quiz 壳: "学习「X」时，第一步最应该做什么"
4. example 壳: "明确概念→掌握方法→情境练习→反思纠错"
另：清理内部标注行 "**内容来源**: TeachAny 课标知识点卫星文件"
幂等：<!-- slides-deduped --> 标记
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
MARK = "<!-- slides-deduped -->"

SIGNS = [
    r"能说出[^<]{2,40}的核心概念与课标要求",
    r"怎样用课标要求的方法学习",
    r"时，第一步最应该做什么？",
    r"明确概念</strong>\s*→\s*<strong>掌握方法</strong>",
]
SATELLITE_NOTE = re.compile(r"<p>-\s*\*\*内容来源\*\*:\s*TeachAny 课标知识点卫星文件</p>")


def _slide_spans(html):
    """配平扫描所有 slide-page 的 (start, end)，class 属性位置不限，支持嵌套"""
    spans = []
    for m in re.finditer(r'<section\b[^>]*class="slide-page"[^>]*>', html):
        depth = 1
        for n in re.finditer(r'<section\b[^>]*>|</section>', html[m.end():]):
            if n.group(0).startswith('</'):
                depth -= 1
                if depth == 0:
                    spans.append((m.start(), m.end() + n.end()))
                    break
            else:
                depth += 1
    return spans


def find_slide_with(html, pattern):
    """找含指定文本的 slide-page 整体 span（配平版）"""
    for s, e in _slide_spans(html):
        if re.search(pattern, html[s:e]):
            return s, e
    return None


def process(f):
    html = f.read_text(encoding="utf-8", errors="replace")
    actions = []
    for i, sig in enumerate(SIGNS, 1):
        while True:
            m = find_slide_with(html, sig)
            if not m:
                break
            html = html[:m[0]] + html[m[1]:]
            actions.append(f"删壳{i}")
    if SATELLITE_NOTE.search(html):
        html = SATELLITE_NOTE.sub("", html)
        actions.append("清卫星标注")
    if not actions:
        return f.parent.name, "无命中", False
    html = html.replace("</body>", MARK + "\n</body>", 1) if "</body>" in html else html + "\n" + MARK
    f.write_text(html, encoding="utf-8")
    return f.parent.name, "、".join(sorted(set(actions))), True


def main():
    ok, skip = 0, 0
    for f in sorted(COMMUNITY.glob("*/index.html")):
        html = f.read_text(encoding="utf-8", errors="replace")
        if "http-equiv=\"refresh\"" in html[:3000]:
            continue
        if not any(re.search(s, html) for s in SIGNS) and not SATELLITE_NOTE.search(html):
            continue
        cid, msg, changed = process(f)
        if changed:
            ok += 1
            print(f"✅ {cid}: {msg}")
        else:
            skip += 1
    print(f"\n清理 {ok}，跳过 {skip}")


if __name__ == "__main__":
    main()
