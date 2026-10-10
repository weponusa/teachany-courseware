#!/usr/bin/env python3
"""tts-fill-files.py — 补生成「播放列表已引用但 mp3 缺失」的文件（31 门 191 个）。

文本来源优先级：播放列表条目的 section（找 data-tts 或 id 定位）→ 标题本身。
生成文件名严格按播放列表 src 里的文件名（seg01_intro.mp3 / union.mp3 等）。
"""
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path("/Users/wepon/CodeBuddy/一次函数/teachany-courseware")
COMMUNITY = ROOT / "community"
sys.path.insert(0, str(ROOT / "scripts"))
from tts_engine import synthesize  # noqa: E402

TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")
VOICE = "zh-CN-XiaoxiaoNeural"

missing = json.load(open("/tmp/tts-missing-files.json", encoding="utf-8"))


def section_text(html, sec):
    if not sec:
        return ""
    m = (re.search(r'<(section|div)[^>]*data-tts="%s"[^>]*>' % re.escape(sec), html)
         or re.search(r'<section\b[^>]*id="%s"[^>]*>' % re.escape(sec), html, re.I)
         or re.search(r'<(section|div)[^>]*id="%s"[^>]*>' % re.escape(sec), html))
    if not m:
        return ""
    seg = html[m.end():m.end() + 3000]
    return WS.sub(" ", TAG.sub("", seg)).strip()[:450]


ok = fail = 0
fail_list = []
for cid, items in missing.items():
    f = COMMUNITY / cid / "index.html"
    h = f.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r'data-teachany-audio-playlist>([\s\S]*?)</script>', h)
    pl = {e.get("id"): e for e in json.loads(m.group(1))} if m else {}
    tts_dir = COMMUNITY / cid / "tts"
    if not tts_dir.exists():
        tts_dir.mkdir(parents=True)
    for eid, fn in items:
        entry = pl.get(eid, {})
        sec = entry.get("section") or entry.get("sectionId")
        text = section_text(h, sec)
        if len(text) < 40:
            text = entry.get("title", "") + "，本节围绕该主题展开讲解。" * 3
        out = tts_dir / fn
        if out.exists():
            continue
        okk, _ = synthesize(text=text, voice=VOICE, output=str(out))
        if okk:
            ok += 1
        else:
            fail += 1
            fail_list.append((cid, fn))
    print(f"  {cid}: 进度", flush=True)

print(f"\n完成：生成 {ok}，失败 {fail}")
if fail_list:
    print(fail_list[:10])
