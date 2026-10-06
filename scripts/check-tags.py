#!/usr/bin/env python3
"""check-tags.py — 校验课件 HTML 标签完整性

检查三项：
  1. 结构标签配平（section / div / figure）
  2. 是否存在非法闭合标签（如把 class 名 slide-page 误当标签名写成 </slide-page>）
  3. slide-page 是否被错误嵌套

用法: python3 check-tags.py [cid...]   不传则查全库
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

# HTML5 合法标签（用于识别非法闭合）
VALID = {
    "a", "abbr", "address", "article", "aside", "audio", "b", "bdi", "bdo",
    "blockquote", "body", "br", "button", "canvas", "caption", "cite", "code",
    "col", "colgroup", "data", "datalist", "dd", "del", "details", "dfn",
    "dialog", "div", "dl", "dt", "em", "embed", "fieldset", "figcaption",
    "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head",
    "header", "hgroup", "hr", "html", "i", "iframe", "img", "input", "ins",
    "kbd", "label", "legend", "li", "link", "main", "map", "mark", "menu",
    "meta", "meter", "nav", "noscript", "object", "ol", "optgroup", "option",
    "output", "p", "param", "picture", "pre", "progress", "q", "rp", "rt",
    "ruby", "s", "samp", "script", "section", "select", "slot", "small",
    "source", "span", "strong", "style", "sub", "summary", "sup", "table",
    "tbody", "td", "template", "textarea", "tfoot", "th", "thead", "time",
    "title", "tr", "track", "u", "ul", "var", "video", "wbr",
    # SVG
    "svg", "g", "defs", "symbol", "use", "path", "circle", "ellipse", "rect",
    "line", "polyline", "polygon", "text", "tspan", "linearGradient",
    "radialGradient", "stop", "clipPath", "marker", "filter", "foreignObject",
    # SVG 滤镜原语与渐变/图案
    "pattern", "mask", "switch", "desc", "metadata", "style",
    "animate", "animateTransform", "animateMotion", "set", "mpath",
    "feMerge", "feMergeNode", "feGaussianBlur", "feBlend", "feColorMatrix",
    "feOffset", "feFlood", "feComposite", "feDropShadow", "feMorphology",
    "feTurbulence", "feDisplacementMap", "feImage", "feTile",
    "feComponentTransfer", "feFuncR", "feFuncG", "feFuncB", "feFuncA",
    "feDiffuseLighting", "feSpecularLighting", "fePointLight",
    "feDistantLight", "feSpotLight", "feConvolveMatrix",
}
# 比较时统一小写，需补充 SVG 驼峰标签的小写形式
VALID |= {t.lower() for t in VALID}


def check(cid):
    P = COMMUNITY / cid / "index.html"
    h = P.read_text(encoding="utf-8", errors="replace")
    issues = []

    # 1. 配平
    pairs = {}
    for t in ("section", "div", "figure"):
        o = len(re.findall(rf"<{t}\b", h))
        c = len(re.findall(rf"</{t}>", h))
        pairs[t] = f"{o}/{c}"
        if o != c:
            issues.append(f"<{t}> 未配平 {o}/{c}")

    # 2. 非法闭合标签
    bad = {m.group(1) for m in re.finditer(r"</([a-zA-Z][\w:-]*)", h)
           if m.group(1).lower() not in VALID}
    if bad:
        issues.append("非法闭合标签: " + ", ".join(sorted(bad)[:5]))

    # 3. slide-page 嵌套（括号匹配section，看每个slide-page是否独立）
    depth, opens = 0, {}
    lines = h.split("\n")
    nested = 0
    for i, l in enumerate(lines, 1):
        for m in re.finditer(r"<section\b[^>]*>|</section>", l):
            if m.group(0).startswith("</"):
                depth = max(0, depth - 1)
            else:
                if "slide-page" in m.group(0) and depth > 0:
                    nested += 1
                depth += 1
    if nested:
        issues.append(f"slide-page 嵌套 {nested} 处")

    return issues, pairs


def main():
    cids = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not cids:
        cids = sorted(p.name for p in COMMUNITY.iterdir()
                      if (p / "index.html").exists())
    bad_list, ok = [], 0
    for cid in cids:
        try:
            issues, pairs = check(cid)
        except Exception as e:
            bad_list.append((cid, [f"解析失败 {str(e)[:40]}"]))
            continue
        if issues:
            bad_list.append((cid, issues))
        else:
            ok += 1
    print(f"检查 {len(cids)} 个课件：完好 {ok}，有问题 {len(bad_list)}")
    for cid, iss in bad_list[:20]:
        print(f"  ❌ {cid}")
        for i in iss:
            print(f"       {i}")
    if len(bad_list) > 20:
        print(f"  ... 另 {len(bad_list)-20} 个")


if __name__ == "__main__":
    main()
