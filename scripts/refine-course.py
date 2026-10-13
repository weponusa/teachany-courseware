#!/usr/bin/env python3
"""refine-course.py — 课件精修：删空壳、解包分页、去重复、按教学逻辑重排

针对抽查反馈的三类问题：

1. 空壳模块
   - hero-infographic 只有 28 字的标签文字（「概念 方法 易错 迁移 无字生图」），
     没有任何实际内容 → 删
   - 「学习进度 0%」这类纯占位 card（<40 字且无交互）→ 删

2. 残留 slide-page / 重复模块
   - 逐课件调用解包逻辑（unwrap-slide-pages 已验证安全）
   - 「知识结构主图」card 与标准 knowledge-graph 讲同一件事 → 删

3. 顺序乱
   此前多次删模块，留下诸如「前测排在正文之后」「知识精讲卡在综合任务后面」
   「拓展资源在图谱后面」的乱序。按教学逻辑重排：

     开场 → 学习目标 → 带着问题学 → 前测 → 正文模块(一/二/三/四) →
     知识精讲 → 方法 → 范例 → 深层理解 → 综合任务 → 概念检测 →
     后测 → 易错点 → 小结/记忆锚点 → 拓展资源 → 知识图谱 → 仿真 → AI学伴

   实现方式：提取全部顶层 section，按排序键重排后，整块替换原区间。

用法: python3 refine-course.py <cid> [cid...] [--dry]
"""
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

_spec = importlib.util.spec_from_file_location(
    "shell", ROOT / "scripts" / "apply-courseware-shell.py")
SHELL = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(SHELL)

# ---------- 排序键：越小越靠前 ----------
ID_ORDER = {
    "hero-infographic": 0, "hero-cover": 0, "hero": 0,
    "objectives": 10,
    "anchor": 15,
    "pretest": 20,
    "lesson-focus": 60, "lesson-method": 61, "worked-example": 62,
    "deep-understanding": 70,
    "posttest": 90,
    "error-clinic": 95, "error-watch": 95,
    "summary": 97, "memory-anchor": 98,
    "knowledge-graph": 110,
    "phet-lab": 120, "external-lab": 120, "interactive-model": 120,
    "teachany-ai-tutor-card": 130,
    "course-nav-map": 105,
}
TITLE_ORDER = [
    (r"学习目标|学习任务", 10),
    (r"带着问题|问题引入", 15),
    (r"前测|课前诊断", 20),
    (r"模块[一1]", 30),
    (r"模块[二2]", 40),
    (r"模块[三3]", 50),
    (r"模块[四4]", 55),
    (r"知识精讲|核心概念", 60),
    (r"方法", 61),
    (r"范例|worked", 62),
    (r"深层理解|五镜头", 70),
    (r"综合任务|综合练习|拖拽练习", 75),
    (r"概念检测|随堂", 80),
    (r"真题练习", 85),
    (r"后测|达标检测", 90),
    (r"易错", 95),
    (r"小结|总结|记忆锚点|口诀", 98),
    (r"拓展|资源|迁移挑战", 100),
    (r"知识图谱|知识关系|知识结构", 110),
    (r"仿真|GeoGebra|PhET|实验", 120),
]
DROP_TITLE = re.compile(r"学习进度|知识结构主图")
DROP_HERO_EMPTY = 40          # hero 空壳判定：字数少于这个值

# 功能容器：内容由 JS 渲染，纯文本少是正常的，绝不能当空壳删。
# 曾因此误删 knowledge-graph（14字）和 ai-tutor-card（0字）。
FUNC_KEEP = {
    "knowledge-graph", "teachany-ai-tutor-card", "phet-lab",
    "external-lab", "interactive-model", "teachany-audio-player",
    "course-nav-map", "video-module", "teachany-knowledge-graph",
}


def sort_key(a, b):
    sid = (re.search(r'id="([^"]+)"', a) or [None, ""])[1]
    if sid in ID_ORDER:
        return ID_ORDER[sid]
    t = SHELL.title_of(a, b) or ""
    for pat, k in TITLE_ORDER:
        if re.search(pat, t):
            return k
    return 50                     # 未知模块放正文区


def is_empty_shell(a, b):
    """无实质内容的模块：占位进度条 / 空壳 hero / 重复的知识结构图"""
    sid = (re.search(r'id="([^"]+)"', a) or [None, ""])[1]
    if sid in FUNC_KEEP:
        return False
    t = SHELL.title_of(a, b) or ""
    n = SHELL.text_len(b)
    if DROP_TITLE.search(t):
        return True
    if sid == "hero-infographic" and n < DROP_HERO_EMPTY:
        return True
    if n < 15 and not re.search(r"<iframe|<canvas|<video|<audio|<button", b):
        return True
    return False


def unwrap_slide_pages(html):
    n = 0
    while True:
        found = None
        for s, e, a, b in SHELL.sections(html, top_only=True):
            if "slide-page" in a:
                found = (s, e)
                break
        if not found:
            break
        s, e = found
        gt = html.find(">", s)
        if gt < 0:
            break
        o_end = gt + 1
        cs = e - len("</section>")
        if html[cs:e] != "</section>":
            break
        html = html[:cs] + html[e:]
        html = html[:s] + html[o_end:]
        n += 1
        if n > 200:
            break
    return html, n


def process(cid, dry=False):
    P = COMMUNITY / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")
    acts = []

    # 1) 解包 slide-page
    html, n = unwrap_slide_pages(html)
    if n:
        acts.append(f"解包slide-page {n}")

    # 2) 收集顶层 section，过滤空壳
    secs = list(SHELL.sections(html, top_only=True))
    kept, dropped = [], []
    for x in secs:
        if is_empty_shell(x[2], x[3]):
            dropped.append(SHELL.title_of(x[2], x[3]) or x[2][:30])
        else:
            kept.append(x)
    if dropped:
        acts.append("删空壳: " + ", ".join(dropped[:4]))

    # 3) 按教学逻辑重排（保守版：整块替换）
    #
    # 此前尝试「提取全部 section 重排后拼接」，结果切断了跨越 section 边界的
    # 标签（外层包裹 div 的闭合标签落在区间之外），造成 <div> 不配平。
    # 改为：整个 section 区间（从原始最前到最后）整体替换为按序拼接的模块。
    # 这依然要求区间内只有 section——若区间内混有其他内容会被丢弃，
    # 因此先把区间内的非 section 片段（注释/空白之外的实质内容）检出并保留原序。
    kept.sort(key=lambda x: sort_key(x[2], x[3]))
    if not kept:
        return []
    first = min(s for s, e, _, _ in kept)
    last = max(e for s, e, _, _ in kept)
    # 按原始顺序收集区间内的非 section 碎片，重排后统一放回区间末尾之前
    pieces, pos = [], first
    for s, e, _, _ in sorted(kept, key=lambda x: x[0]):
        if s > pos:
            piece = html[pos:s]
            if re.sub(r"[\s<!\-]+", "", piece):     # 非纯空白/注释才保留
                pieces.append(piece)
        pos = e
    if last > pos:
        piece = html[pos:last]
        if re.sub(r"[\s<!\-]+", "", piece):
            pieces.append(piece)
    frag = "".join(html[s:e] for s, e, _, _ in kept) + "".join(pieces)
    html = html[:first] + frag + html[last:]
    acts.append(f"重排 {len(kept)} 个模块（保留碎片 {len(pieces)}）")

    if not dry:
        P.write_text(html, encoding="utf-8")
    return acts


def main():
    dry = "--dry" in sys.argv
    cids = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not cids:
        print("用法: python3 refine-course.py <cid> [cid...] [--dry]")
        return
    for c in cids:
        try:
            acts = process(c, dry)
            print(f"{c}:")
            for x in acts:
                print(f"    {x}")
        except Exception as e:
            print(f"  ❌ {c}: {str(e)[:70]}")
    print("完成" + ("（--dry 未写入）" if dry else ""))


if __name__ == "__main__":
    main()
