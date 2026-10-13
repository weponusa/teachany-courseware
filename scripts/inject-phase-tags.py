#!/usr/bin/env python3
"""inject-phase-tags.py — 给标准教学模块注入统一的「阶段标签」容器头。

背景
----
全库 1043 门课件的标准教学环节内容层面已基本齐全（2026-10-10 甄别：
「缺知识精讲 140 门 / 深层理解 30 门」全部是 id 与标题命名不同，真缺 0 门）。
真正的缺口是**标识**：同一环节叫 lesson-focus / module-1 / sss / 新课讲授……
学生与教师无法一眼看出「现在处于教学流程的哪一步」。

做法：按 id 与中文标题识别标准模块，在其顶层 section 开标签后注入一枚
.ta-phase 阶段标签（样式在 assets/scripts/courseware-shell.css，全站统一）。
四色相：讲授=蓝、检测=琥珀、易错=红、辅助=紫。

只处理顶层 section（与 apply-courseware-shell.py 同一套栈匹配逻辑），
嵌套的小节不重复打标；外部托管跳转壳整体跳过；已有 .ta-phase 的 section
跳过（幂等，可反复运行）。

用法：
  python3 scripts/inject-phase-tags.py --pilot 3            # 预览
  python3 scripts/inject-phase-tags.py --pilot 3 --apply
  python3 scripts/inject-phase-tags.py --ids a,b --apply
  python3 scripts/inject-phase-tags.py --all --apply
  python3 scripts/inject-phase-tags.py --all --revert
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
TAG_MARK = "ta-phase"

# (标准名, tone, id 关键词小写, 标题关键词)。顺序即优先级：先命中先得。
MODULES = [
    ("学习目标", "aux",  ("objectiv", "goal", "learning-goal"), ("学习目标", "课程目标", "本课目标")),
    ("课前诊断", "aux",  ("pretest", "pre-test"), ("前测", "课前诊断", "课前测")),
    ("深层理解", "aux",  ("deep-understanding", "deep-insight"), ("深层理解", "深度理解", "本质理解")),
    ("易错辨析", "warn", ("error-clinic", "mistake"), ("易错", "错因", "常见误区", "常见错误")),
    ("分层作业", "quiz", ("tiered-practice",), ("作业分层",)),
    ("随堂练习", "quiz", ("practice", "exercise", "drill"), ("随堂练", "巩固练习", "课堂练习")),
    ("达标检测", "quiz", ("posttest", "post-test", "quiz"), ("后测", "达标检测", "课堂检测", "随堂测")),
    ("课堂小结", "aux",  ("summary", "conclusion", "wrap-up"), ("小结", "课堂总结", "总结")),
    ("知识图谱", "aux",  ("knowledge-graph", "knowledge-map", "teachany-kg"), ("知识图谱",)),
    ("AI 学伴", "aux",   ("ai-tutor", "teachany-tutor", "tutor-card"), ("AI 学伴", "AI学伴")),
    ("知识精讲", "main", ("lesson-focus", "core-concept", "knowledge-point", "lesson-method"),
     ("知识精讲", "核心概念", "新课讲授", "知识讲解", "重点解析")),
]

# 结构性容器不打标：slide-page 分页容器、音频播放器、导航、hero 等
SKIP_ID = ("slide-page", "slide-container", "hero", "audio-player", "sidenav",
           "pre-quiz-holder", "teachany-upgrade")

TAG_RE = re.compile(r"<[^>]+>")


def classify(sid: str, title: str) -> tuple[str, str] | None:
    sid_l = sid.lower()
    for name, tone, idk, titlek in MODULES:
        if any(k in sid_l for k in idk):
            return name, tone
        for tk in titlek:
            if tk in title:
                return name, tone
    return None


def top_sections(html: str):
    """[(start, end_of_open_tag, end)] 仅顶层 section。"""
    spans = []
    for m in re.finditer(r"<section\b[^>]*>", html):
        depth = 0
        for mm in re.finditer(r"<section\b|</section>", html[m.start():]):
            depth += -1 if mm.group(0) == "</section>" else 1
            if depth == 0:
                spans.append((m.start(), m.end(), m.start() + mm.end()))
                break
    return [sp for sp in spans
            if not any(sp[0] > s2 and sp[0] < e2 for s2, e2, _ in spans)]


def section_title(attrs: str, body: str) -> str:
    m = re.search(r"<h([1-3])[^>]*>([\s\S]*?)</h\1>", body)
    if not m:
        return ""
    t = TAG_RE.sub("", m.group(2))
    return re.sub(r"\s+", "", t)[:30]


def inject_file(html: str):
    out = html
    n = 0
    # 相邻同名去重：同一环节常被拆成两个 section（如 objectives + goals），
    # 连着打两枚「学习目标」是噪音。上一枚同名标签之后、本节之前的正文
    # 少于 200 字，即视为同环节重复，跳过。
    prev = None          # (name, body_start, body_end)
    marks = []           # (open_end, tag)
    for start, open_end, end in top_sections(html):
        seg = html[open_end:end]
        if TAG_MARK in seg:
            continue
        attrs = html[start:open_end]
        sid_m = re.search(r'id="([^"]+)"', attrs)
        sid = sid_m.group(1) if sid_m else ""
        if any(k in sid for k in SKIP_ID):
            prev = None
            continue
        title = section_title(attrs, seg)
        got = classify(sid, title)
        if not got:
            prev = None
            continue
        name, tone = got
        if prev and prev[0] == name and len(plain_seg(html[prev[2]:start])) < 200:
            prev = (name, start, end)
            continue
        marks.append((open_end, f'<span class="ta-phase" data-tone="{tone}">{name}</span>'))
        prev = (name, start, end)
        n += 1
    for open_end, tag in sorted(marks, reverse=True):
        html = html[:open_end] + tag + html[open_end:]
    return html, n


def plain_seg(s: str) -> str:
    return TAG_RE.sub("", s)


def revert_file(html: str) -> str:
    return re.sub(r'<span class="ta-phase"[^>]*>[^<]*</span>\s*', "", html)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", type=int, default=0)
    ap.add_argument("--ids")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--revert", action="store_true")
    a = ap.parse_args()
    if not any([a.pilot, a.ids, a.all]):
        ap.error("需指定 --pilot / --ids / --all 之一")

    if a.ids:
        dirs = [COMMUNITY / x.strip() for x in a.ids.split(",") if x.strip()]
    else:
        dirs = sorted(p for p in COMMUNITY.iterdir()
                      if p.is_dir() and (p / "index.html").is_file())
    if a.pilot:
        dirs = dirs[: a.pilot]

    mode = "回滚" if a.revert else ("写入" if a.apply else "预览")
    print(f"目标 {len(dirs)} 门 · {mode}", flush=True)
    tot = 0
    for p in dirs:
        f = p / "index.html"
        if not f.is_file():
            continue
        h = f.read_text(encoding="utf-8", errors="ignore")
        if "external-link" in h and "teachany-hosting" in h:
            continue          # 跳转壳豁免
        if a.revert:
            new = revert_file(h)
            if new != h and a.apply:
                f.write_text(new, encoding="utf-8")
                print(f"  ✓ {p.name}: 已移除标签")
            continue
        new, n = inject_file(h)
        if n == 0:
            continue
        if a.apply:
            f.write_text(new, encoding="utf-8")
        tot += n
        print(f"  {'✓' if a.apply else '○'} {p.name}: +{n} 标签")
    print(f"\n完成：共 {mode} {tot} 枚标签")


if __name__ == "__main__":
    main()
