#!/usr/bin/env python3
"""scan-empty-modules.py — 用 DOM 树精确扫描课件空模块/占位内容/套话
（正确处理嵌套 div，避免正则误判）
用法: python3 scan-empty-modules.py [cid...]  不传则扫全库
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

PLACEHOLDER = [
    r"待补充", r"待完善", r"待定", r"暂无内容", r"敬请期待", r"TODO", r"TBD",
    r"占位符?", r"示例文本", r"示例内容", r"lorem", r"[xX]{3,}",
    r"请(?:在此)?(?:填写|输入)", r"内容(?:待)?(?:补充|生成)中",
]
BOILERPLATE = [
    r"能说出[^。]{0,30}的核心概念与课标要求",
    r"能运用所学方法分析[^。]{0,25}相关典型问题",
    r"能在情境中正确应用[^。]{0,25}的知识与技能",
    r"能识别并纠正关于[^。]{0,25}的常见误区",
    r"理解课标概念，掌握方法，在情境中练习并反思",
    r"忽略课标，凭感觉答题",
]
# 这些容器由 JS 填充，内容为空属正常
DYNAMIC = {"ta-sort-list", "ta-items", "ta-out", "ta-stage", "tkg-fallback-canvas",
           "navMapCanvas", "problem-anchor-choices", "knowledge-graph", "course-nav-map",
           "ai-tutor", "teachany-ai-tutor-card"}
VOID = {"br", "hr", "img", "input", "meta", "link", "source", "canvas", "iframe", "path"}


class Node:
    __slots__ = ("tag", "attrs", "children", "text", "parent")

    def __init__(self, tag, attrs=None, parent=None):
        self.tag = tag
        self.attrs = dict(attrs or [])
        self.children = []
        self.text = ""
        self.parent = parent

    @property
    def cls(self):
        return self.attrs.get("class", "")

    @property
    def ident(self):
        return self.attrs.get("id", "")


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("root")
        self.cur = self.root
        self.all = []

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.children.append(n)
        self.all.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n.parent:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.text += data


def visible_text(n):
    parts = [n.text]
    for c in n.children:
        if c.tag in ("script", "style"):
            continue
        parts.append(visible_text(c))
    return re.sub(r"\s+", " ", "".join(parts)).strip()


def has_media(n):
    for c in n.all if hasattr(n, "all") else []:
        pass
    stack = [n]
    while stack:
        x = stack.pop()
        if x.tag in ("img", "canvas", "svg", "iframe", "video", "picture"):
            return True
        if x.tag in ("ul", "ol") and any(k in x.cls for k in DYNAMIC):
            return True
        if any(k in x.cls or k in x.ident for k in DYNAMIC):
            return True
        stack.extend(x.children)
    return False


def is_dynamic(n):
    return any(k in n.cls or k in n.ident for k in DYNAMIC)


def scan(cid):
    P = COMMUNITY / cid / "index.html"
    if not P.exists():
        return []
    html = P.read_text(encoding="utf-8", errors="replace")
    t = Tree()
    try:
        t.feed(html)
    except Exception:
        return []
    issues = []

    def walk(n, depth=0):
        txt = visible_text(n)
        title = ""
        for c in n.children:
            if c.tag in ("h2", "h3"):
                title = visible_text(c)
                break
        sid = n.ident or title[:22]

        # 内容模块：section / card / slide-page
        def is_card(c):
            cs = c.split()
            return "card" in cs or "card-accent" in cs  # 精确匹配，排除 card-title/card-body

        is_module = (n.tag == "section" and "slide-page" in n.cls) or \
                    (n.tag == "div" and is_card(n.cls)) or \
                    (n.tag == "section" and n.cls.strip() == "section")
        if is_module and not is_dynamic(n) and not has_media(n):
            if len(txt) < 45:
                issues.append(("空模块(%d字)" % len(txt), sid, txt[:60]))

        # 占位词（只在可见文本里找）
        for pat in PLACEHOLDER:
            for m in re.finditer(pat, txt):
                issues.append(("占位内容", sid, m.group(0)[:30]))
        # 套话
        for pat in BOILERPLATE:
            for m in re.finditer(pat, txt):
                issues.append(("模板套话", sid, m.group(0)[:50]))

        for c in n.children:
            walk(c, depth + 1)

    walk(t.root)
    # 去重
    seen, out = set(), []
    for i in issues:
        k = (i[0].split("(")[0], i[1], i[2])
        if k in seen:
            continue
        seen.add(k)
        out.append(i)
    return out


def main():
    cids = sys.argv[1:] or sorted(p.name for p in COMMUNITY.iterdir() if (p / "index.html").exists())
    rows = []
    for cid in cids:
        iss = scan(cid)
        if iss:
            rows.append((cid, iss))
    rows.sort(key=lambda r: -len(r[1]))
    for cid, iss in rows:
        print(f"\n=== {cid} ({len(iss)}) ===")
        for kind, sid, snip in iss:
            print(f"  [{kind}] {sid} :: {snip}")
    print(f"\n扫描 {len(cids)} 个课件，{len(rows)} 个存在问题")


if __name__ == "__main__":
    main()
