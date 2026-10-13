#!/usr/bin/env python3
"""fix-placeholders-phase1.py — 机械修复占位符（无需LLM）
1. 「course-id」→「课件标题」
2. 叠标/页脚版本串中的裸 ID → 标题
3. bad_title 清洗：嵌套《》、多余段落
幂等：替换后无命中即跳过
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
CN_QUOTE_ID = re.compile(r"「([a-z][a-z0-9]*(?:-[a-z0-9]+)+)」")

# 手动标题映射（h1/meta/title 均无法提取正确标题的课件）
TITLE_OVERRIDE = {
    "chemistry-ext-1a79c832-6a108218": "化学反应的微观本质",
    "ext-1a79c832": "认识多媒体课件",
    "bio-m-biosphere": "生物圈",
    "bio-m-cell-division-junior": "细胞分裂",
}


def extract_title(cid, html):
    """提取课件短标题：手动映射 > h1 > meta course-title > title 清洗"""
    if cid in TITLE_OVERRIDE:
        return TITLE_OVERRIDE[cid]
    h1 = re.search(r"<h1[^>]*>([\s\S]{0,100}?)</h1>", html)
    if h1:
        t = re.sub(r"<[^>]+>", "", h1.group(1)).strip()
        t = re.sub(r"^[\U0001F300-\U0001FAFF☀-➿\s]+", "", t).strip()
        if t and len(t) <= 30:
            return t
    m = re.search(r'<meta name="course-title" content="([^"]+)"', html)
    if m and m.group(1).strip():
        return m.group(1).strip()
    tm = re.search(r"<title>([^<]+)</title>", html)
    if tm:
        t = tm.group(1)
        # 嵌套《《X · Y》· Z》→ X；《X · Y》→ X
        inner = re.findall(r"《([^《》]+)", t)
        if inner:
            first = inner[0].split("·")[0].strip()
            if first and "正在打开" not in first:
                return first
    return None


def rebuild_title_text(h1, old):
    """用 h1 + 学段学科段 + 最新版本段 重组规范 title"""
    vers = re.findall(r"TeachAny (v[\d.]+)", old)
    ver = vers[-1] if vers else ""
    seg = ""
    m = re.search(r"((?:小学|初中|高中)?[\u4e00-\u9fa5]{2,5}\s*G\d+)", old)
    if m:
        seg = m.group(1).strip()
    else:
        m2 = re.search(r"》 · ([\u4e00-\u9fa5]{2,4}) ·", old)
        if m2:
            seg = m2.group(1)
    parts = [h1] if h1 else []
    if seg:
        parts.append(seg)
    if ver:
        parts.append("TeachAny " + ver)
    return " · ".join(parts) if parts else ""


def clean_bad_title(html, h1_title):
    """清洗 <title> 嵌套书名号/占位标题：重组为 h1 · 学段 · TeachAny 版本"""
    tm = re.search(r"(<title>)([^<]+)(</title>)", html)
    if not tm:
        return html, False
    t = tm.group(2)
    is_bad = "《《" in t or "正在打开" in t
    if not is_bad:
        return html, False
    if not h1_title:
        return html, False
    new_t = rebuild_title_text(h1_title, t)
    if not new_t or new_t == t:
        return html, False
    return html[:tm.start(2)] + new_t + html[tm.end(2):], True


def process(cid, dry=False):
    p = COMMUNITY / cid / "index.html"
    html = p.read_text(encoding="utf-8", errors="replace")
    title = extract_title(cid, html)
    actions = []
    # 1. 「course-id」→「标题」（仅当「」内是已知 course-id 形态）
    if title:
        def repl(m):
            return "「" + title + "」"
        html2 = CN_QUOTE_ID.sub(repl, html)
        if html2 != html:
            actions.append(f"「ID」→「{title}」")
            html = html2
        # 2. 叠标/页脚裸 ID（可见文本中 "ID ·" 形式）
        html2 = re.sub(r"(>|·\s*)" + re.escape(cid) + r"(\s*·)", lambda m: m.group(1) + title + m.group(2), html)
        html2 = re.sub(r">(" + re.escape(cid) + r") · 知识结构主图", ">" + title + " · 知识结构主图", html2)
        if html2 != html:
            actions.append("裸ID→标题")
            html = html2
    # 3. bad_title 清洗
    html, cleaned = clean_bad_title(html, title)
    if cleaned:
        actions.append("title重组")
    if not actions:
        return cid, "无命中", False
    if not dry:
        p.write_text(html, encoding="utf-8")
    return cid, "、".join(actions), True


def main():
    rows = json.load(open(ROOT / "scripts" / "placeholder-scan-v2.json", encoding="utf-8"))
    ids = sorted({r["id"] for r in rows if any(k in r["issues"] for k in ("cn_quote_id", "bad_title", "bare_id_visible"))})
    print(f"待处理 {len(ids)} 个课件")
    ok, skip = 0, 0
    for cid in ids:
        c, msg, changed = process(cid)
        if changed:
            ok += 1
            print(f"✅ {c}: {msg}")
        else:
            skip += 1
    print(f"\n修复 {ok}，跳过 {skip}")


if __name__ == "__main__":
    main()
