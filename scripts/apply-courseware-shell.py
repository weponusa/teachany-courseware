#!/usr/bin/env python3
"""apply-courseware-shell.py — 引入统一设计系统 + 清理重复模块

做两件事，目标是**从根本上**消除风格不统一与模块重复：

1. 引入 assets/scripts/courseware-shell.css
   ── 一套共享设计令牌与模块容器，改一处全库 946 个课件同时生效。
   课件已有的同名 CSS 变量会被沿用（不覆盖），深浅主题都能适配。

2. 去重：同一课件里「标题实质相同」的模块只保留内容最完整的一个
   ── 典型如两个都叫「学习目标」的 section、两套「前测」。
   判定刻意保守：只有归一化标题完全相同时才自动删除，
   语义相近但标题不同（如「知识全景」与「知识精讲」）只报告不删，
   因为后者可能是合理的并列模块，误删会丢内容。

用法: python3 apply-courseware-shell.py [--dry] [--check]
      --check  只体检不改动，输出各课件重复模块清单
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
SHELL_REL = "../../assets/scripts/courseware-shell.css"
LINK = f'<link rel="stylesheet" href="{SHELL_REL}">'

# 语义分组：一个课件里出现多个同类模块时，值得关注
GROUPS = {
    "学习目标": ["objectives", "learning-objectives", "goal"],
    "达标检测": ["posttest", "post-test"],
    "课前诊断": ["pretest", "pre-test"],
    "知识图谱": ["knowledge-graph", "knowledge-map"],
    "小结": ["summary", "conclusion", "wrap-up"],
    "方法": ["lesson-method", "method"],
    "知识精讲": ["lesson-focus", "core-concept", "learn", "concept"],
    "深层理解": ["deep-understanding", "deep-insight"],
    "范例": ["worked-example", "example"],
    "练习": ["practice", "exercise", "drill"],
}


def norm_title(t):
    """归一化标题：去标签、emoji、序号、标点和空白"""
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F\u2190-\u21FF]", "", t)
    t = re.sub(r"^[0-9０-９\.\s、]+", "", t)
    t = re.sub(r"[\s\u3000：:，,。．、\-—·|｜]+", "", t)
    return t


def sections(html, top_only=True):
    """切出 section 的 (start, end, attrs, body)，用栈匹配避免嵌套截断

    top_only=True 时只保留顶层 section。必须这么做：课件里普遍存在
    「slide-page 分页容器嵌套 section 内容模块」的结构，外层字数必然等于
    内层，若不排除嵌套项，去重会把内层当成外层的重复副本而误删
    （实测一次误删 2039 个）。
    """
    out = []
    for m in re.finditer(r"<section\b([^>]*)>", html):
        depth = 0
        for mm in re.finditer(r"<section\b|</section>", html[m.start():]):
            if mm.group(0) == "</section>":
                depth -= 1
                if depth == 0:
                    out.append((m.start(), m.start() + mm.end(),
                                m.group(1), html[m.end():m.start() + mm.start()]))
                    break
            else:
                depth += 1
    if not top_only:
        return out
    # 排除被其它 section 包住的（起点落在某个区间内的）
    spans = [(s, e) for s, e, _, _ in out]
    return [it for it in out
            if not any(s2 < it[0] < e2 for s2, e2 in spans)]


def title_of(attrs, body):
    m = re.search(r"<h([1-3])[^>]*>([\s\S]*?)</h\1>", body)
    return norm_title(m.group(2)) if m else ""


def text_len(body):
    return len(re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", body)))


def plain(body):
    return re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", body))


def similarity(a, b):
    """字符 2-gram Jaccard 相似度

    仅比对标题会误删：不少课件把「元信息横幅」（必修一 / Grade 10 / 新授课）
    与正文拆成两个同名 section，标题相同但内容完全不同。加上相似度门槛后，
    只有内容真正雷同的才判为重复。
    """
    ga = {plain(a)[i:i + 2] for i in range(len(plain(a)) - 1)}
    gb = {plain(b)[i:i + 2] for i in range(len(plain(b)) - 1)}
    if not ga or not gb:
        return 0.0
    return len(ga & gb) / len(ga | gb)


def ensure_shell(html):
    if SHELL_REL in html:
        return html
    # 常规：插到 </head> 前
    m = re.search(r"\s*</head>", html)
    if m:
        return html[:m.start()] + "\n" + LINK + html[m.start():]
    # 缺 </head> 但有 <body>：插到 <body> 后
    m = re.search(r"<body[^>]*>", html)
    if m:
        return html[:m.end()] + "\n" + LINK + html[m.end():]
    # 35 个物理课件存在结构缺陷：<head> 未闭合且缺 <body> 开标签。
    # link 本身是合法的 head 内容，直接跟在 <head ...> 之后即可被正确解析。
    m = re.search(r"<head[^>]*>", html)
    if m:
        return html[:m.end()] + "\n" + LINK + html[m.end():]
    return html


def process(cid, dry=False, check=False):
    """返回 (去重数, 疑似重复清单)"""
    P = COMMUNITY / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")
    secs = sections(html)

    removed, report = 0, []

    # —— 1) 精确去重：标题实质相同的模块，保留内容最完整的
    #
    # 无标题模块（多为空的 slide-page 分页容器，抽样 120 个课件即有 395 个）
    # 归一化后标题都是空串，若纳入去重会被判为彼此「重复」而遭误删
    # （曾一次误删 2039 个）。因此必须跳过无标题或过短标题的模块。
    by_title = {}
    for s, e, a, b in secs:
        t = title_of(a, b)
        if t and len(t) >= 2:
            by_title.setdefault(t, []).append((s, e, a, b))
    drop = []
    for t, group in by_title.items():
        if len(group) < 2:
            continue
        group_sorted = sorted(group, key=lambda x: -text_len(x[3]))
        keep = group_sorted[0]
        for dup in group_sorted[1:]:
            sim = similarity(keep[3], dup[3])
            # 三重保险：标题相同 + 内容确实雷同 + 篇幅明显更少
            if sim >= 0.45 and text_len(dup[3]) <= text_len(keep[3]) * 0.8:
                drop.append(dup)
                removed += 1
            else:
                why = "内容不雷同" if sim < 0.45 else "篇幅接近"
                report.append(f"同名模块未删（{why}，相似度{sim:.2f}）：「{t}」"
                              f"({text_len(keep[3])}字 vs {text_len(dup[3])}字)")
    for s, e, a, b in sorted(drop, reverse=True):
        html = html[:s] + html[e:]

    # —— 2) 语义分组体检（只报告）
    if drop or True:
        secs2 = sections(html)
        for g, keys in GROUPS.items():
            hits = []
            for s, e, a, b in secs2:
                sid = (re.search(r'id="([^"]+)"', a) or [None, ""])[1]
                if any(k in sid for k in keys):
                    hits.append((sid, title_of(a, b), text_len(b)))
            if len(hits) > 1:
                # 标题各不相同的，视为并列模块，只提示
                titles = {t for _, t, _ in hits}
                if len(titles) == len(hits):
                    report.append(f"[{g}] 存在 {len(hits)} 个（标题不同，视为并列）："
                                  + ", ".join(f"{sid}({n}字)" for sid, _, n in hits))

    if not check and not dry and html != P.read_text(encoding="utf-8", errors="replace"):
        html = ensure_shell(html)
        P.write_text(html, encoding="utf-8")
    elif not check and not dry:
        html2 = ensure_shell(html)
        if html2 != html:
            P.write_text(html2, encoding="utf-8")

    return removed, report


def main():
    dry = "--dry" in sys.argv
    check = "--check" in sys.argv
    cids = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not cids:
        cids = sorted(p.name for p in COMMUNITY.iterdir() if (p / "index.html").exists())

    tot_rm, tot_shell = 0, 0
    reports = []
    for c in cids:
        try:
            rm, rep = process(c, dry, check)
            tot_rm += rm
            if rm:
                tot_shell += 1
            for r in rep:
                reports.append((c, r))
        except Exception as e:
            print(f"  ❌ {c}: {str(e)[:60]}")

    if check:
        print(f"体检 {len(cids)} 个课件，疑似/并列模块 {len(reports)} 条")
        for c, r in reports[:20]:
            print(f"  {c}: {r}")
        if len(reports) > 20:
            print(f"  ... 另 {len(reports)-20} 条")
    else:
        print(f"删除重复模块 {tot_rm} 个（涉及 {tot_shell} 个课件），"
              f"并列提示 {len(reports)} 条" + ("（--dry 未写入）" if dry else ""))


if __name__ == "__main__":
    main()
