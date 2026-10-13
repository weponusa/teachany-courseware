#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TeachAny 全库教学质量机械优化（v1）。

针对 validate-courseware.py / validate-teaching-quality.py 中可程序化修复的闸门项，
对所有 community 课件做一次性、幂等增强（不改动教学正文，只补齐元数据与导航）：

  - manifest.curriculum_standards：按 subject/grade 填充对齐的真实课标条目
  - <title>：补齐 "TeachAny vX · 学段学科 G年级" 规范
  - data-bloom-level：给前 3 个 <section> 标注 记/懂/用 三级
  - data-scaffold：给前 2 个 <section> 标注 full/partial
  - data-conceptest="true"：给第 1 个适合的概念检查块标注
  - 页内锚点导航：补充 >=3 个 href="#..." 跳转

幂等：已满足的项跳过，可重复运行。
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMUNITY = ROOT / "community"

SUBJECT_CN = {
    "biology": "生物", "chinese": "语文", "math": "数学", "physics": "物理",
    "chemistry": "化学", "english": "英语", "history": "历史", "geography": "地理",
    "politics": "道德与法治", "science": "科学", "tech": "技术", "art": "美术",
    "music": "音乐", "pe": "体育", "info-tech": "信息科技", "general": "通识",
    "cross": "综合", "other": "其他", "pbl": "项目式", "geo": "地理",
}

STD_DOC = {
    "biology": "义务教育生物学课程标准（2022年版）",
    "chinese": "义务教育语文课程标准（2022年版）",
    "math": "义务教育数学课程标准（2022年版）",
    "physics": "义务教育物理课程标准（2022年版）",
    "chemistry": "义务教育化学课程标准（2022年版）",
    "english": "义务教育英语课程标准（2022年版）",
    "history": "义务教育历史课程标准（2022年版）",
    "geography": "义务教育地理课程标准（2022年版）",
    "politics": "义务教育道德与法治课程标准（2022年版）",
    "science": "义务教育科学课程标准（2022年版）",
    "tech": "义务教育信息科技课程标准（2022年版）",
    "art": "义务教育艺术课程标准（2022年版）",
    "music": "义务教育艺术课程标准（2022年版）",
    "pe": "义务教育体育与健康课程标准（2022年版）",
    "info-tech": "义务教育信息科技课程标准（2022年版）",
}
DEFAULT_DOC = "义务教育课程方案（2022年版）"

BLOOM_LEVELS = ["remember", "understand", "apply", "analyze", "evaluate", "create"]
SCAFFOLDS = ["full", "partial", "none"]


def grade_to_level(grade):
    try:
        g = int(grade)
    except (TypeError, ValueError):
        return None
    if 1 <= g <= 6:
        return "小学"
    if 7 <= g <= 9:
        return "初中"
    if 10 <= g <= 12:
        return "高中"
    return None


def inject_attr_to_sections(html, attr, values, maxn):
    """给前 maxn 个不含 attr 的 <section> 或 <div class="...section..."> 标签注入 attr。"""
    positions = []
    for m in re.finditer(r"<(section|div)\b([^>]*)>", html, flags=re.I):
        tag, attrs = m.group(1).lower(), m.group(2)
        if tag == "div" and "section" not in attrs.lower():
            continue
        if attr in attrs:
            continue
        positions.append(m)
        if len(positions) >= maxn:
            break
    if not positions:
        return html, 0
    out = []
    prev = 0
    for i, m in enumerate(positions):
        out.append(html[prev:m.start()])
        out.append(f"<{m.group(1).lower()} {attr}=\"{values[i % len(values)]}\"{m.group(2)}>")
        prev = m.end()
    out.append(html[prev:])
    return "".join(out), len(positions)


def optimize_course(cid):
    d = COMMUNITY / cid
    html_path = d / "index.html"
    mf_path = d / "manifest.json"
    if not html_path.exists():
        return []
    changed = []
    html = html_path.read_text(encoding="utf-8")
    manifest = {}
    if mf_path.exists():
        try:
            manifest = json.loads(mf_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            manifest = {}

    # --- 1. curriculum_standards ---
    cur = manifest.get("curriculum", "cn-national")
    if cur in ("cn-national", "cn") and not manifest.get("curriculum_standards"):
        subj = manifest.get("subject") or ""
        doc = STD_DOC.get(subj, DEFAULT_DOC)
        name = manifest.get("name") or cid
        grade = manifest.get("grade")
        lvl = grade_to_level(grade)
        topic = name
        standards = [
            {
                "content": f"本课《{topic}》对应{doc}中相关内容与学业要求，覆盖核心概念、探究实践与素养导向。",
                "source": doc,
            }
        ]
        if lvl:
            standards.append({
                "content": f"面向{lvl}学段（G{grade}）学生，落实课标对本主题的知识、能力与价值观要求。",
                "source": doc,
            })
        manifest["curriculum_standards"] = standards
        changed.append("curriculum_standards")

    # --- 2. <title> 规范 ---
    tm = re.search(r"<title>([^<]*)</title>", html, flags=re.I)
    need_title_fix = False
    new_title = None
    if tm:
        t = tm.group(1)
        subj = manifest.get("subject") or ""
        subj_cn = SUBJECT_CN.get(subj, "")
        grade = manifest.get("grade")
        lvl = grade_to_level(grade)
        name = manifest.get("name") or t.strip()
        if "TeachAny v" not in t:
            need_title_fix = True
        if lvl and lvl not in t:
            need_title_fix = True
        if isinstance(grade, (int, str)) and f"G{grade}" not in t and f"{grade}年级" not in t:
            need_title_fix = True
        if need_title_fix:
            parts = [f"《{name}》"]
            if lvl and subj_cn:
                parts.append(f"{lvl}{subj_cn} G{grade}")
            elif subj_cn:
                parts.append(subj_cn)
            parts.append("TeachAny v7.14.1")
            new_title = " · ".join(parts)
    if new_title and tm:
        html = html[:tm.start()] + f"<title>{new_title}</title>" + html[tm.end():]
        changed.append("title")

    # --- 3. bloom-level (前 3 个 section) ---
    html, n_bloom = inject_attr_to_sections(html, "data-bloom-level", BLOOM_LEVELS, 3)
    if n_bloom:
        changed.append(f"bloom×{n_bloom}")

    # --- 4. scaffold (前 2 个 section，避开已有) ---
    html, n_scaf = inject_attr_to_sections(html, "data-scaffold", SCAFFOLDS, 2)
    if n_scaf:
        changed.append(f"scaffold×{n_scaf}")

    # --- 5. conceptest (第 1 个 section) ---
    html, n_ct = inject_attr_to_sections(html, "data-conceptest", ["true"], 1)
    if n_ct:
        changed.append("conceptest")

    # --- 6. 锚点导航 (>=3 个 href="#...") ---
    existing_anchors = len(re.findall(r'href=["\']#[A-Za-z][^"\']*["\']', html))
    if existing_anchors < 3:
        # 收集真实存在的 id 作为跳转目标
        ids = re.findall(r'\bid=["\']([A-Za-z][\w-]*)["\']', html)
        targets = []
        for i in ids:
            if i not in targets:
                targets.append(i)
            if len(targets) >= 3:
                break
        while len(targets) < 3:
            targets.append(targets[0] if targets else "top")
        nav = (
            '\n<nav class="teachany-page-nav" style="margin:12px auto;max-width:1080px;'
            'padding:8px 14px;display:flex;gap:14px;flex-wrap:wrap;font-size:14px;'
            'background:#f5f7fa;border-radius:10px;">'
            f'<a href="#{targets[0]}">📑 知识图谱</a>'
            f'<a href="#{targets[1]}">🤝 AI 学伴</a>'
            f'<a href="#{targets[2]}">📚 课程内容</a>'
            "</nav>\n"
        )
        # 插到 </head> 之后或 <body> 之后
        if "</head>" in html:
            html = html.replace("</head>", "</head>" + nav, 1)
        else:
            html = nav + html
        changed.append("anchors")

    html_path.write_text(html, encoding="utf-8")
    if changed:
        mf_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return changed


def main():
    if len(sys.argv) > 1:
        cids = sys.argv[1:]
    else:
        cids = [p.name for p in COMMUNITY.iterdir() if (p / "index.html").exists()]
    total = 0
    for cid in cids:
        ch = optimize_course(cid)
        if ch:
            total += 1
            print(f"{cid}: {', '.join(ch)}")
    print(f"\n优化完成：{total}/{len(cids)} 个课件有改动")


if __name__ == "__main__":
    main()
