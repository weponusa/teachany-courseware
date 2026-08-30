#!/usr/bin/env python3
"""fix-refine-style.py — 修正补写模块的排版

问题：补写模块用了课件里并不存在的 CSS 类。各课件 CSS 差异很大——
  bio-circulation 有 .card 定义（前测就用 <div class="card"><h2>）
  bio-classification 完全没有 .card，p 也没有全局样式
结果是段落无间距、无留白，排版塌陷。

修法：
  1. 改用课件原生结构：<div class="card ta-refine"><h2>（h2 不带 class，
     与「📝 前测」等原生模块一致）
  2. 注入 .ta-refine 兜底样式，全部用 CSS 变量 + fallback，
     深浅主题通吃；课件本身已有 .card 时则继承其外观

用法: python3 fix-refine-style.py [--dry]
"""
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

MARK = "/* ===== TeachAny 补写模块排版 ===== */"
CSS = MARK + """
.ta-refine{max-width:1080px;margin:26px auto;padding:24px 28px;
  border:1px solid var(--border,rgba(148,163,184,.22));
  border-radius:14px;
  background:var(--card,rgba(148,163,184,.07))}
.ta-refine h2{font-size:21px;font-weight:800;margin:0 0 18px;
  line-height:1.45;color:var(--text,inherit)}
.ta-refine p{margin:0 0 14px;line-height:1.95;font-size:15px;
  color:var(--text,inherit)}
.ta-refine p:last-child{margin-bottom:0}
.ta-refine b,.ta-refine strong{color:var(--primary,#3b82f6);font-weight:700}
.ta-refine .ta-ex{margin-top:16px;padding:13px 18px;line-height:1.9;
  border-left:4px solid var(--accent,#f59e0b);
  background:rgba(148,163,184,.10);border-radius:0 8px 8px 0}
@media (max-width:1120px){.ta-refine{max-width:100%;padding:20px 18px}}
""" + "/* ===== /TeachAny 补写模块排版 ===== */"


def ensure_css(html):
    """注入排版样式（幂等）"""
    if MARK in html:
        return html
    m = re.search(r"\s*</head>", html)
    css = f"\n<style>\n{CSS}\n</style>\n"
    if m:
        return html[:m.start()] + css + html[m.start():]
    m = re.search(r"<body[^>]*>", html)
    if m:
        return html[:m.end()] + css + html[m.end():]
    return html


def rebuild(sid, h2_text, paras):
    """用原生结构重建模块"""
    parts = [f'<section class="section" id="{sid}" data-scaffold="full">',
             '<div class="card ta-refine">',
             f'<h2>{h2_text}</h2>']
    for text, is_ex in paras:
        cls = ' class="ta-ex"' if is_ex else ""
        parts.append(f'<p{cls}>{text}</p>')
    parts += ["</div></section>"]
    return "".join(parts)


def process(cid, dry=False):
    P = COMMUNITY / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")
    orig = html
    changed = 0

    for sid in ("worked-example", "summary"):
        m = re.search(
            rf'<section class="section" id="{sid}" data-scaffold="full">'
            rf'<div class="card">([\s\S]*?)</div></section>', html)
        if not m:
            continue
        inner = m.group(1)
        h2 = re.search(r'<h2 class="section-title">([\s\S]*?)</h2>', inner)
        if not h2:
            h2 = re.search(r'<h2[^>]*>([\s\S]*?)</h2>', inner)
        if not h2:
            continue
        h2_text = h2.group(1)
        paras = []
        # 范例块
        for pm in re.finditer(r'<div class="worked-example">([\s\S]*?)</div>', inner):
            paras.append((pm.group(1), True))
        # 误区块
        for pm in re.finditer(r'<p class="bioh-pitfall">([\s\S]*?)</p>', inner):
            paras.append((pm.group(1), True))
        # 普通段落（排除上面两种）
        for pm in re.finditer(r'<p(?![^>]*class="bioh-pitfall")[^>]*>([\s\S]*?)</p>', inner):
            t = pm.group(1)
            if any(t in p[0] for p in paras):
                continue
            paras.append((t, False))
        if not paras:
            continue
        new = rebuild(sid, h2_text, paras)
        html = html[:m.start()] + new + html[m.end():]
        changed += 1

    if not changed:
        return 0
    html = ensure_css(html)
    if html != orig and not dry:
        P.write_text(html, encoding="utf-8")
    return changed


def main():
    dry = "--dry" in sys.argv
    n = tot = 0
    for p in sorted(COMMUNITY.glob("*/index.html")):
        try:
            k = process(p.parent.name, dry)
            if k:
                n += 1
                tot += k
        except Exception as e:
            print(f"  ❌ {p.parent.name}: {str(e)[:50]}")
    print(f"修正排版 {tot} 个模块（{n} 个课件）" + ("（--dry 未写入）" if dry else ""))


if __name__ == "__main__":
    main()
