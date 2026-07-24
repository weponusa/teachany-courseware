#!/usr/bin/env python3
"""
regen-tts.py · 批量重生成低质量/占位 TTS（2026-07 欠账清偿）
=============================================================
对播放列表中"疑似静音/占位"（文件过小）的 mp3：
1. 从 HTML 提取对应 section 的教学文本（strip 标签，截取 600 字内）
2. 调 edge-tts 重新生成
3. 新文件明显更大才覆盖（防退化）

用法：
  python3 scripts/regen-tts.py <course-id> [<course-id> ...]
  python3 scripts/regen-tts.py --file /tmp/tts-courses.txt   # 课件清单文件
  python3 scripts/regen-tts.py --dry-run <course-id>         # 只看不改
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VOICE = "zh-CN-XiaoxiaoNeural"
MIN_SIZE = 30000          # 低于 30KB 视为疑似占位
MAX_CHARS = 600           # 每段截取文本上限
GAIN_RATIO = 1.5          # 新文件至少大 50% 才覆盖

TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")


def strip_html(s: str) -> str:
    s = TAG_RE.sub(" ", s)
    return SPACE_RE.sub(" ", s).strip()


def section_text(html: str, section_id: str) -> str:
    """提取 <section id="xxx"> ... </section> 的纯文本"""
    m = re.search(
        r'<section[^>]*id=["\']' + re.escape(section_id) + r'["\'][^>]*>(.*?)</section>',
        html, re.S)
    if not m:
        return ""
    return strip_html(m.group(1))


def regen_course(course_id: str, dry_run: bool = False) -> dict:
    cdir = REPO / "community" / course_id
    html_path = cdir / "index.html"
    result = {"course": course_id, "regen": [], "skip": [], "missing": []}
    if not html_path.exists():
        result["missing"].append("index.html")
        return result
    html = html_path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r'data-teachany-audio-playlist[^>]*>(.*?)</script>', html, re.S)
    if not m:
        result["missing"].append("playlist")
        return result
    try:
        playlist = json.loads(m.group(1))
    except Exception as e:
        result["missing"].append(f"playlist-json:{e}")
        return result

    for item in playlist:
        src = item.get("src", "")
        section = item.get("section", "")
        label = item.get("label", section)
        mp3 = cdir / src.lstrip("./")
        if not mp3.exists():
            result["missing"].append(src)
            continue
        size = mp3.stat().st_size
        if size >= MIN_SIZE:
            result["skip"].append(f"{src} ({size}B 正常)")
            continue
        # 提取 section 文本
        text = section_text(html, section)[:MAX_CHARS].strip()
        if len(text) < 30:
            # 兜底：用 label + 课程标题
            tm = re.search(r"<title>([^<]+)</title>", html)
            text = f"{label}。{tm.group(1) if tm else course_id}"
        if dry_run:
            result["regen"].append(f"{src} ({size}B) → 将重生成（文本{len(text)}字: {text[:40]}...）")
            continue
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tf:
            tmp = tf.name
        try:
            r = subprocess.run(
                ["edge-tts", "--voice", VOICE, "--text", text, "--write-media", tmp],
                capture_output=True, timeout=120)
            if r.returncode != 0 or not Path(tmp).exists() or Path(tmp).stat().st_size < 5000:
                result["missing"].append(f"{src} 生成失败: {r.stderr.decode()[:80]}")
                continue
            new_size = Path(tmp).stat().st_size
            if new_size > size * GAIN_RATIO:
                Path(tmp).replace(mp3)
                result["regen"].append(f"{src} {size}B → {new_size}B ✓")
            else:
                result["skip"].append(f"{src} 新文件({new_size}B)未显著更大，保留原文件")
        except subprocess.TimeoutExpired:
            result["missing"].append(f"{src} 生成超时")
        finally:
            Path(tmp).unlink(missing_ok=True)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("courses", nargs="*")
    ap.add_argument("--file")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    courses = list(args.courses)
    if args.file:
        courses += [l.strip() for l in open(args.file) if l.strip() and not l.startswith("#")]
    if not courses:
        ap.error("需要课件 id 或 --file 清单")
    for cid in courses:
        r = regen_course(cid, args.dry_run)
        print(f"══ {cid} ══")
        for x in r["regen"]:
            print(f"  ✓ {x}")
        for x in r["skip"]:
            print(f"  - {x}")
        for x in r["missing"]:
            print(f"  ✗ {x}")


if __name__ == "__main__":
    main()
