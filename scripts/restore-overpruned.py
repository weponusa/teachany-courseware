#!/usr/bin/env python3
"""恢复 7f992072a 过度清理误删的标准教学模块。

策略：对质检未过的课件，从 7f992072a^ (c7e4b5622, 全量 22 项通过版本)
提取被删除的 <section> 块与 upgrade-v2 交互脚本，插回当前工作区文件。
- 跳过纯 figure 配图堆砌块（用户明确要求清除）
- 跳过当前文件中已存在的块（按 id 或正文签名判重）
- 内容模块插到收尾组（音频→图谱→AI学伴）之前，保持原文件相对顺序
- 被删的音频/图谱/学伴块按标准收尾顺序插回
用法: python3 scripts/restore-overpruned.py [--dry] [courseId ...]
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "7f992072a^"

TAIL_IDS = ["teachany-audio-player", "knowledge-graph", "teachany-ai-tutor-card"]


def git_show(path: str) -> str:
    r = subprocess.run(["git", "show", f"{BASE}:{path}"], cwd=ROOT,
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def scan_sections(html: str):
    """返回顶层 <section>...</section> 块列表 [(start, end, text)]，容错深度计数。"""
    blocks = []
    for m in re.finditer(r"<section\b[^>]*>", html, re.I):
        depth = 1
        pos = m.end()
        while depth > 0:
            nxt = re.search(r"<(/?)section\b[^>]*>", html[pos:], re.I)
            if not nxt:
                break
            if nxt.group(1):
                depth -= 1
            else:
                depth += 1
            pos += nxt.end()
        if depth == 0:
            blocks.append((m.start(), pos, html[m.start():pos]))
    return blocks


def sec_id(text: str) -> str:
    m = re.search(r"id=[\"']([^\"']+)[\"']", text[:400])
    return m.group(1) if m else ""


def signature(text: str) -> str:
    body = re.sub(r"<[^>]+>", " ", text)
    body = re.sub(r"\s+", " ", body).strip()
    return body[:100]


def is_figure_spam(text: str) -> bool:
    # 旧版 hero-cover 封面块：当前文件已有新版 hero，不恢复
    if "hero-cover" in text[:300]:
        return True
    # 无标题、无交互的纯配图块（figure 或裸 img）：用户明确要求清除的堆砌
    if ("<h2" not in text and "<h3" not in text
            and "data-interactive" not in text and "tu-q" not in text
            and "data-teachany" not in text
            and ("<figure" in text or "<img" in text)):
        return True
    return False


def find_tail_start(html: str, before: int = None):
    """收尾组（audio/kg/tutor）最早一个 section 的起始位置。"""
    best = None
    for tid in TAIL_IDS:
        for m in re.finditer(rf"id=[\"']{tid}[\"']", html):
            # 回溯到所属 <section 开头
            s = html.rfind("<section", 0, m.start())
            if s == -1:
                continue
            if before is not None and s >= before:
                continue
            if best is None or s < best:
                best = s
    return best


def restore_course(cid: str, dry: bool) -> dict:
    path = ROOT / "community" / cid / "index.html"
    if not path.is_file():
        return {"id": cid, "skipped": "no file"}
    cur = path.read_text(encoding="utf-8")
    old = git_show(f"community/{cid}/index.html")
    if not old:
        return {"id": cid, "skipped": "no old version"}

    cur_norm = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", cur))
    content_blocks, tail_blocks = [], []
    for _, _, text in scan_sections(old):
        sid = sec_id(text)
        if sid and (f'id="{sid}"' in cur or f"id='{sid}'" in cur):
            continue  # 已存在
        if not sid and not signature(text):
            continue  # 空壳占位块（无正文），无教学价值且不恢复
        if not sid and signature(text) in cur_norm:
            continue  # 无 id 块按正文签名判重
        if is_figure_spam(text):
            continue  # 纯配图堆砌不恢复
        if len(text) < 40:
            continue
        if sid in TAIL_IDS:
            tail_blocks.append((sid, text))
        else:
            content_blocks.append(text)

    # upgrade-v2 交互脚本：恢复内容里含 tu-* 交互且当前缺失时补回
    need_v2 = any(("tu-opt" in b or "tu-save" in b or "data-inq" in b)
                  for b in content_blocks)
    v2_script = ""
    if need_v2 and "teachany-upgrade-v2-js" not in cur:
        m = re.search(r"<script id=\"teachany-upgrade-v2-js\">[\s\S]*?</script>", old)
        if m:
            v2_script = m.group(0)

    # 音频播放器 JS 引用
    need_audio_js = any(sid == "teachany-audio-player" for sid, _ in tail_blocks)
    audio_js_missing = need_audio_js and "teachany-audio-player.js" not in cur

    if not content_blocks and not tail_blocks and not v2_script:
        return {"id": cid, "restored": 0}

    new = cur
    # 1) 收尾块先插（保持 audio→kg→tutor 次序），让内容块随后插到收尾组之前
    for sid, text in sorted(tail_blocks, key=lambda x: TAIL_IDS.index(x[0])):
        rank = TAIL_IDS.index(sid)
        # 插入到比它更靠后的收尾块之前；没有则插到 body 末尾脚本之前
        anchor = None
        for later in TAIL_IDS[rank + 1:]:
            pos = find_tail_start(new)
            # find_tail_start 返回最早的；需要找特定 id 的位置
            for m in re.finditer(rf"id=[\"']{later}[\"']", new):
                s = new.rfind("<section", 0, m.start())
                if s != -1 and (anchor is None or s < anchor):
                    anchor = s
        if anchor is None:
            body_end = new.rfind("</body>")
            anchor = body_end if body_end != -1 else len(new)
        new = new[:anchor] + text + "\n\n" + new[anchor:]

    # 2) 内容块插到收尾组起始之前，保持原顺序
    if content_blocks:
        tail_start = find_tail_start(new)
        if tail_start is None:
            body_end = new.rfind("</body>")
            tail_start = body_end if body_end != -1 else len(new)
        bundle = "\n".join(content_blocks) + "\n\n"
        new = new[:tail_start] + bundle + new[tail_start:]

    # 3) upgrade-v2 脚本与音频 JS 引用插到 </body> 前
    tail_inject = ""
    if audio_js_missing:
        tail_inject += '<script src="../../assets/scripts/teachany-audio-player.js" defer></script>\n'
    if v2_script:
        tail_inject += v2_script + "\n"
    if tail_inject:
        body_end = new.rfind("</body>")
        if body_end != -1:
            new = new[:body_end] + tail_inject + new[body_end:]

    if not dry:
        path.write_text(new, encoding="utf-8")
    return {"id": cid, "restored": len(content_blocks) + len(tail_blocks),
            "content": len(content_blocks), "tail": [s for s, _ in tail_blocks],
            "v2": bool(v2_script), "audioJs": audio_js_missing}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry" in sys.argv
    if args:
        courses = args
    else:
        rep = json.loads((ROOT / "qc-all-report.json").read_text(encoding="utf-8"))
        recs = rep if isinstance(rep, list) else rep.get("results", rep.get("items", []))
        courses = [r["id"] for r in recs if r.get("failed")]
    results = [restore_course(c, dry) for c in courses]
    done = [r for r in results if r.get("restored")]
    print(f"处理 {len(results)}，恢复 {len(done)} 个课件")
    for r in done:
        print(f"  {r['id']}: +{r['restored']} 块 (content={r['content']}, tail={r['tail']}"
              f"{', v2脚本' if r.get('v2') else ''}{', audio.js' if r.get('audioJs') else ''})")
    skipped = [r for r in results if r.get("restored") == 0 or r.get("skipped")]
    if skipped:
        print(f"无需恢复/跳过 {len(skipped)}:", [r["id"] for r in skipped][:20])


if __name__ == "__main__":
    main()
