#!/usr/bin/env python3
"""修复课件 HTML 文档结构缺陷。

三类问题（均会造成浏览器解析进入非标准行为）：

1. ``<!doctype html>`` 之前有内容（典型是一个 `hidden` 的版本号`` div`` + 注释）。
   HTML 解析器遇到doctype 前的非空白字符会切到 quirks 模式，盒模型、
   行高、图片缩放等行为与标准模式不一致。
   → 把doctype 前的那段内容搬到 ``<body>`` 开头（保持 DOM 顺序与可见性不变）。

2. 有 ``<head>`` 但缺 ``</head>``。浏览器会自动闭合，但会让后续注入
   ``</head>`` 之前的脚本/样式判断失效，也让工具（如 add-page-nav）找不到锚点。
   → 在正确的位置补上 ``</head>``：``<body`` 之前。

3. ``</html>`` 之后还有内容（侧边导航、播放模式 FAB 等）。
   浏览器会把它们移回 body 尾部，通常仍可见，但属于非法结构，
   部分校验器/工具会误判页面结束位置。
   → 把 ``</html>`` 之后的内容移回 ``</body>`` 之前。

用法：
    python3 tools/fix-html-structure.py --dry-run
    python3 tools/fix-html-structure.py --apply
    python3 tools/fix-html-structure.py --from-list /tmp/x.txt --apply
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RE_DOCTYPE = re.compile(r"<!\s*doctype", re.I)
RE_HEAD_OPEN = re.compile(r"<head\b[^>]*>", re.I)
RE_HEAD_CLOSE = re.compile(r"</head\s*>", re.I)
RE_BODY_OPEN = re.compile(r"<body\b[^>]*>", re.I)
RE_BODY_CLOSE = re.compile(r"</body\s*>", re.I)
RE_HTML_CLOSE = re.compile(r"</html\s*>", re.I)

# 这些标签允许出现在 <head> 内，遇到它们不算 head 结束
RE_HEAD_OK = re.compile(
    r"<\s*(meta|link|title|style|script|base|noscript)\b[^>]*>|<\s*(meta|link|title|style|script|base|noscript)\b[^>]*/>",
    re.I,
)
RE_ANY_TAG = re.compile(r"<\s*/?\s*([a-zA-Z][a-zA-Z0-9-]*)")

# 残片常见形态：`<section class="section" id="knowledge-graph" ...>` 丢了开标签，
# 只剩下 `id="knowledge-graph" ...>` 这一串属性。识别这种属性串并补回开标签。
RE_LEADING_ATTRS = re.compile(r'^[a-zA-Z-]+\s*=\s*"[^"]*"(?:\s+[a-zA-Z-]+\s*=\s*"[^"]*")*\s*>', re.S)


def repair_leading_fragment(tail: str) -> str | None:
    """把「以属性串开头」的截断残片补回外层开标签。识别不了就返回 None。"""
    m = RE_LEADING_ATTRS.match(tail)
    if not m:
        return None
    attrs = m.group(0).rstrip()
    # 属性里必须带 id/class，否则无法判断该套哪个壳
    if 'id=' not in attrs and 'class=' not in attrs:
        return None
    # 该残片自带闭合结构（尾部已有 </section> 或 </div>）才补开标签
    if not re.search(r"</\s*(section|div)\s*>", tail[m.end():], re.I):
        return None
    return f'<section class="section" {attrs}\n' + tail[m.end():]


def implicit_body_start(html: str) -> int | None:
    """定位浏览器隐式开启 <body> 的位置。

    返回 ``<head>`` 之后第一个「不属于 head 内容」的标签的起始偏移；
    若始终没找到则返回 None。
    """
    mh = RE_HEAD_OPEN.search(html)
    if not mh:
        return None
    pos = mh.end()
    n = len(html)
    while pos < n:
        mt = RE_ANY_TAG.search(html, pos)
        if not mt:
            return None
        name = (mt.group(1) or "").lower()
        if name in ("meta", "link", "title", "style", "script", "base", "noscript"):
            #跳过整个标签（含其闭标签）
            end = html.find(">", mt.start())
            if end == -1:
                return None
            pos = end + 1
            continue
        return mt.start()
    return None


def fix_one(html: str) -> tuple[str, list[str]]:
    notes: list[str] = []
    out = html

    # 1) 先补齐 head/body 边界（隐式 body 需要显式化后才能安全搬运内容）
    if RE_HEAD_OPEN.search(out) and not RE_HEAD_CLOSE.search(out):
        mb = RE_BODY_OPEN.search(out)
        if mb:
            pos = mb.start()
            pre = out[:pos].rstrip()
            out = pre + "\n</head>\n" + out[len(pre):]
            notes.append("head-close-added")
        else:
            bs = implicit_body_start(out)
            if bs is not None:
                pre = out[:bs].rstrip()
                out = pre + "\n</head>\n<body>\n" + out[bs:]
                notes.append("head-close-added")
                notes.append("body-open-added")

    # 2) doctype 前有内容 -> 搬到 <body> 开头
    m = RE_DOCTYPE.search(out)
    if m and out[: m.start()].strip():
        prefix = out[: m.start()].strip()
        out = out[m.start():]
        mb = RE_BODY_OPEN.search(out)
        if mb:
            pos = mb.end()
            out = out[:pos] + "\n" + prefix + out[pos:]
            notes.append("doctype-prefix-moved")
        else:
            notes.append("doctype-prefix-kept")

    # 3) </html> 之后的内容 -> 移回 </body> 之前
    mh = RE_HTML_CLOSE.search(out)
    if mh:
        #关键：`</html>` 及其之后的原始片段要被**替换**掉，只保留 </html> 之前的内容，
        # 否则会造成内容翻倍。
        head_end = mh.start()
        tail = out[mh.end():].strip()
        if tail:
            if not re.match(r"^(<|<!--)", tail):
                # 尾部是被截断的残片：从属性（如 `id="knowledge-graph"`）开始，
                # 说明外层开标签在 </html> 之前被写坏。补一个同款section 开标签再搬。
                fixed = repair_leading_fragment(tail)
                if fixed is None:
                    notes.append("tail-fragment-kept")
                else:
                    tail = fixed
                    notes.append("tail-fragment-repaired")
            else:
                notes.append("tail-after-html-moved")
            if notes and notes[-1] in (
                "tail-fragment-repaired",
                "tail-after-html-moved",
            ):
                mc = RE_BODY_CLOSE.search(out)
                if mc and mc.start() < head_end:
                    pos = mc.start()
                    out = (
                        out[:pos]
                        + tail
                        + "\n"
                        + out[pos:head_end].rstrip()
                        + "\n"
                        + out[mh.start():mh.end()]
                        + "\n"
                    )
                else:
                    notes.append("tail-move-skipped-no-body")

    return (out if notes else html), notes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--from-list")
    args = ap.parse_args()

    if args.from_list:
        cids = [l.strip() for l in open(args.from_list, encoding="utf-8") if l.strip()]
        files = [ROOT / "community" / c / "index.html" for c in cids]
    else:
        files = sorted((ROOT / "community").glob("*/index.html"))

    changed = 0
    tallies: dict[str, int] = {}
    for p in files:
        if not p.exists():
            continue
        src = p.read_text(encoding="utf-8", errors="replace")
        out, notes = fix_one(src)
        for n in notes:
            tallies[n] = tallies.get(n, 0) + 1
        if out == src:
            continue
        changed += 1
        if args.apply and not args.dry_run:
            p.write_text(out, encoding="utf-8")

    print(f"{'写入' if args.apply and not args.dry_run else '计划修改'} {changed} 门")
    print("明细:", tallies or "无")
    return 0


if __name__ == "__main__":
    sys.exit(main())
