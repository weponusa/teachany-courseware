#!/usr/bin/env python3
"""全量课件结构顺序审计：hero 置顶 → 内容模块 → 收尾组（音频播放器 → 知识图谱 → AI 学伴）。
识别：①收尾组之后仍有内容块 ②AI 学伴卡在内容中间 ③hero/封面位置异常。
输出 reports/structure-audit.json
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMMUNITY = ROOT / "community"

TAIL_IDS = ("knowledge-graph", "teachany-ai-tutor-card", "teachany-audio-player")

BLOCK_RE = re.compile(r"<(section|header)\b[^>]*>|</(section|header)>", re.I)


def scan_blocks(html: str):
    """扫描顶层 section/header 块，返回 [(tag, start, end, attrs)]。跟踪嵌套深度。"""
    blocks = []
    stack = []
    for m in BLOCK_RE.finditer(html):
        token = m.group(0)
        if token.startswith("</"):
            tag = m.group(2).lower()
            # 弹出到匹配标签
            for i in range(len(stack) - 1, -1, -1):
                if stack[i][0] == tag:
                    start, attrs = stack.pop(i)
                    if not stack or all(s[0] != tag for s in stack):
                        pass
                    if i == len(stack):  # 是栈顶弹出（最内层）
                        pass
                    # 只记录弹出后深度为 0 的块（顶层）
                    if not any(True for _ in stack):
                        blocks.append((tag, start, m.end(), attrs))
                    break
        else:
            tag = m.group(1).lower()
            # 自闭合判断（section/header 一般不会自闭合，忽略）
            stack.append((tag, m.start(), token))
    # 修正：上面的栈逻辑对嵌套弹出记录有误，重新用简洁深度法
    return blocks


def scan_blocks2(html: str):
    """深度法：遇到开标签 depth+1 并记录；遇到闭标签 depth-1，回到 0 时记录完整块。"""
    blocks = []
    depth = 0
    cur = None  # (tag, start, attrs)
    for m in BLOCK_RE.finditer(html):
        token = m.group(0)
        if token.startswith("</"):
            if depth > 0:
                depth -= 1
                if depth == 0 and cur:
                    blocks.append((cur[0], cur[1], m.end(), cur[2]))
                    cur = None
        else:
            if depth == 0:
                cur = (m.group(1).lower(), m.start(), token)
            depth += 1
    return blocks


def classify(tag, attrs, body):
    bid = re.search(r'id="([^"]+)"', attrs)
    bid = bid.group(1) if bid else ""
    if "data-teachany-kg" in body or bid == "knowledge-graph":
        return "kg", bid
    if bid == "teachany-ai-tutor-card":
        return "tutor", bid
    if bid == "teachany-audio-player" or "data-teachany-audio-playlist" in body:
        return "audio", bid
    if tag == "header" and "hero" in attrs:
        return "hero", bid
    if "hero-cover" in attrs:
        return "cover", bid
    return "content", bid


def audit_file(path: Path):
    html = path.read_text(encoding="utf-8", errors="replace")
    # 只扫描 body 区域
    body_m = re.search(r"<body[^>]*>([\s\S]*)</body>", html, re.I)
    scope = body_m.group(1) if body_m else html
    blocks = scan_blocks2(scope)
    seq = []
    for tag, s, e, attrs in blocks:
        kind, bid = classify(tag, attrs, scope[s:e])
        seq.append({"kind": kind, "id": bid, "start": s, "end": e})
    issues = []
    tail_idx = [i for i, b in enumerate(seq) if b["kind"] in ("kg", "tutor", "audio")]
    if tail_idx:
        first_tail = min(tail_idx)
        for i, b in enumerate(seq):
            if i > first_tail and b["kind"] in ("content", "cover", "hero"):
                issues.append(f"content-after-tail:{b['kind']}:{b['id'] or '?'}")
        # 收尾组内部顺序 audio -> kg -> tutor
        order = [b["kind"] for b in seq if b["kind"] in ("kg", "tutor", "audio")]
        rank = {"audio": 0, "kg": 1, "tutor": 2}
        if order != sorted(order, key=lambda k: rank[k]):
            issues.append(f"tail-order:{'|'.join(order)}")
        # tutor/kg 出现在前 60% 视为卡中间
        for i, b in enumerate(seq):
            if b["kind"] in ("tutor", "kg") and i < len(seq) * 0.4 and len(seq) > 5:
                issues.append(f"tail-in-middle:{b['kind']}:{b['id']}")
    # hero 检查（多形态）：header.hero 块 / div.hero / slide cover / hero-cover，
    # 且需跳过顶部固定导航条（约 4KB 内）
    hero_idx = [i for i, b in enumerate(seq) if b["kind"] == "hero"]
    if not hero_idx:
        head_zone = re.sub(
            r"<script\b[\s\S]*?</script>|<style\b[\s\S]*?</style>|<!--[\s\S]*?-->",
            "", scope[:12000], flags=re.I)
        has_hero = bool(
            re.search(r'class="[^"]*hero', head_zone)
            or 'data-page-type="cover"' in head_zone
            or re.search(r'class="[^"]*cover', head_zone)
            or re.search(r'<img[^>]*hero', head_zone, re.I))
        if not has_hero:
            issues.append("no-hero-header")
    return seq, issues


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    dirs = sorted(d for d in COMMUNITY.iterdir() if d.is_dir())
    report = {}
    stats = {"total": 0, "ok": 0, "violations": 0, "issue_kinds": {}}
    for d in dirs:
        f = d / "index.html"
        if not f.is_file():
            continue
        if only and only not in d.name:
            continue
        seq, issues = audit_file(f)
        stats["total"] += 1
        if issues:
            stats["violations"] += 1
            for it in issues:
                k = it.split(":")[0]
                stats["issue_kinds"][k] = stats["issue_kinds"].get(k, 0) + 1
            report[d.name] = {
                "issues": issues,
                "seq": [f"{b['kind']}:{b['id']}" for b in seq],
            }
        else:
            stats["ok"] += 1
    out = ROOT / "reports" / "structure-audit.json"
    out.write_text(json.dumps({"stats": stats, "violations": report}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False, indent=1))
    if only:
        print(json.dumps(report, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
