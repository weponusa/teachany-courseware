#!/usr/bin/env python3
"""standardize-knowledge-graph.py — 知识图谱模块统一为标准嵌入

现状：946 个课件都有图谱，内部结构（h2 > div[kg] > canvas）已经统一，
但外围五花八门：
  - section 属性：有无 data-bloom-level / data-scaffold / style 各不相同
  - h2 文案：有的把标题重复三遍
      「🗺️ 知识图谱：生物分类 — 生物分类 — 八年级生物互动课件」
    有的直接用了课件 ID
      「🗺️ 知识图谱：math-m-linear-equation」

统一为唯一标准形态（只保留 data-teachany-kg 的节点 ID 为差异项）：

<section class="section" id="knowledge-graph"
         style="max-width:1080px;margin:24px auto;padding:0 20px;">
  <h2 class="section-title">🗺️ 知识图谱：{课程名}</h2>
  <div data-teachany-kg="{nodeId}">
    <canvas class="tkg-fallback-canvas" width="720" height="120"
            aria-label="知识图谱互动画布"
            style="display:block;width:100%;max-height:140px;
                   border-radius:12px;"></canvas>
  </div>
</section>

课程名取 <title> 的主标题，去掉「— 八年级生物互动课件」这类后缀；
若取不到则退回 meta course-title，再退回课件 ID。

用法: python3 standardize-knowledge-graph.py [--dry] [--all]
"""
import html as _html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

CANVAS = ('<canvas class="tkg-fallback-canvas" width="720" height="120" '
          'aria-label="知识图谱互动画布" '
          'style="display:block;width:100%;max-height:140px;'
          'border-radius:12px;"></canvas>')


def esc(s):
    return _html.escape(str(s), quote=True)


def clean_name(t):
    """去掉括号及其内容，只留主名

    「情态动词（can/may/must/should）」这类标题，括号里的英文会让长度超限
    （25 字）而回退成课件 ID；去掉括号即可得到干净的「情态动词」。
    """
    t = re.sub(r"[（(【\[][^）)】\]]*[）)】\]]", "", t)
    t = re.sub(r"[（(【\[）)】\]]", "", t)
    return t.strip()


def course_name(html, cid):
    """取干净的课程名：截到第一个分隔符，去书名号、去括号内容

    下限设为 1 而非 2——「酶」「烃」这类单字课程名是合法且常见的。
    """
    m = re.search(r"<title>([^<]+)", html)
    if m:
        t = re.split(r"[·|｜—\-–—：:》]", m.group(1))[0].strip().strip("《》 　")
        t = clean_name(t)
        if 1 <= len(t) <= 24:
            return t
    m = re.search(r'name="course-title" content="([^"]*)"', html)
    if m:
        t = clean_name(re.split(r"[·|｜—\-–—：:]", m.group(1))[0].strip())
        if 1 <= len(t) <= 24:
            return t
    m = re.search(r"<h1[^>]*>([\s\S]*?)</h1>", html)
    if m:
        t = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        t = clean_name(re.split(r"[·|｜—\-–—：:]", t)[0].strip())
        if 1 <= len(t) <= 24:
            return t
    return cid


def build(node_id, name):
    return (
        f'<section class="section" id="knowledge-graph" '
        f'style="max-width:1080px;margin:24px auto;padding:0 20px;">'
        f'<h2 class="section-title">🗺️ 知识图谱：{esc(name)}</h2>'
        f'<div data-teachany-kg="{esc(node_id)}">{CANVAS}</div>'
        f'</section>')


def section_span(html):
    """返回 knowledge-graph section 的 (start, end)，用栈匹配避免嵌套截断"""
    m = re.search(r'<section\b[^>]*\bid="knowledge-graph"[^>]*>', html)
    if not m:
        return None
    depth, pos = 0, m.start()
    for mm in re.finditer(r"<section\b|</section>", html[m.start():]):
        if mm.group(0) == "</section>":
            depth -= 1
            if depth == 0:
                return (m.start(), m.start() + mm.end())
        else:
            depth += 1
    return None


def process(cid, dry=False):
    P = COMMUNITY / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")
    span = section_span(html)
    if not span:
        return 0
    s, e = span
    old = html[s:e]
    m = re.search(r'data-teachany-kg="([^"]*)"', old)
    if not m:
        return 0
    node_id = m.group(1)
    new = build(node_id, course_name(html, cid))
    if new == old:
        return 0
    if not dry:
        P.write_text(html[:s] + new + html[e:], encoding="utf-8")
    return 1


def main():
    dry = "--dry" in sys.argv
    cids = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--all" in sys.argv or not cids:
        cids = sorted(p.name for p in COMMUNITY.iterdir() if (p / "index.html").exists())
    n = 0
    for c in cids:
        try:
            n += process(c, dry)
        except Exception as e:
            print(f"  ❌ {c}: {str(e)[:60]}")
    print(f"图谱模块标准化：{n} 个课件" + ("（--dry 未写入）" if dry else ""))


if __name__ == "__main__":
    main()
