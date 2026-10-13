#!/usr/bin/env python3
"""为缺 TTS 的课件批量补音频（清旧 playlist + finalize + edge-tts）。"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
REPORTS = ROOT / "reports"
FINALIZE = Path.home() / ".claude/skills/teachany/scripts/finalize-courseware.py"
AUDIT = REPORTS / "courseware-quality-audit-r7.json"


def tts_count(d: Path) -> int:
    return len(list(d.glob("tts/*.mp3"))) + len(list(d.glob("assets/tts/*.mp3")))


def regen_tts(out: Path) -> None:
    """删除旧 TTS 与 playlist，强制 finalize 重新生成。"""
    tts_dir = out / "tts"
    if tts_dir.is_dir():
        shutil.rmtree(tts_dir)
    assets_tts = out / "assets" / "tts"
    if assets_tts.is_dir():
        shutil.rmtree(assets_tts)
    html_path = out / "index.html"
    if not html_path.is_file():
        return
    html = html_path.read_text(encoding="utf-8")
    html = re.sub(
        r'<script[^>]*\bid=["\']teachany-audio-playlist["\'][^>]*>.*?</script>\s*',
        "",
        html,
        flags=re.S,
    )
    html_path.write_text(html, encoding="utf-8")


def has_tts_markers(d: Path) -> bool:
    html = (d / "index.html").read_text(encoding="utf-8", errors="replace")
    return "data-tts=" in html


def load_missing(limit: int) -> list[str]:
    if AUDIT.is_file():
        data = json.loads(AUDIT.read_text(encoding="utf-8"))
        ids = [r["course_id"] for r in data["courses"] if "missing_tts" in r["issues"]]
    else:
        ids = [d.name for d in COMMUNITY.iterdir() if d.is_dir() and tts_count(d) < 3]
    ids = [cid for cid in ids if has_tts_markers(COMMUNITY / cid)]
    return ids[:limit] if limit else ids


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not FINALIZE.is_file():
        print(f"❌ 未找到 finalize: {FINALIZE}", file=sys.stderr)
        return 2

    targets = load_missing(args.limit)
    print(f"TTS 补录 {len(targets)} 门…")
    ok = fail = 0
    for i, cid in enumerate(targets, 1):
        d = COMMUNITY / cid
        if not (d / "index.html").is_file():
            continue
        before = tts_count(d)
        if args.dry_run:
            print(f"  [{i}] {cid} (当前 {before} mp3)")
            continue
        regen_tts(d)
        r = subprocess.run(
            [sys.executable, str(FINALIZE), str(d), "--shared"],
            capture_output=True,
            text=True,
        )
        after = tts_count(d)
        if r.returncode == 0 and after >= 3:
            ok += 1
            print(f"  ✅ [{i}] {cid}: {before} → {after} mp3")
        else:
            fail += 1
            err = (r.stderr or r.stdout or "")[-200:]
            print(f"  ❌ [{i}] {cid}: {before} → {after} mp3 · {err.strip()}")
    print(f"\n完成：{ok} 成功，{fail} 失败")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
