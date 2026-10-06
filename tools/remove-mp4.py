#!/usr/bin/env python3
"""全站移除 mp4 视频及其引用（用户指令：去掉所有 mp4 视频和引用）。

处理四类目标：
1. `<section ... id="video-module" ...>...</section>` 整个教学动画模块（video 的标准宿主）
2. 残余的 `<video ...>...</video>` / `<video ... />` 标签
3. `<source src="*.mp4">` 子标签
4. 仓库内所有 `.mp4` 文件（community/ 与 assets/ 下，含 remotion 产物）

不动的内容：
- quiz 选项文本里的「.mp4」字样（如 ext-b849401 的 `data-choice="C"` 文本）——是教学内容

用法：
    python3 tools/remove-mp4.py --dry-run
    python3 tools/remove-mp4.py --apply
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RE_VIDEO_MODULE = re.compile(
    r'\n?[ \t]*<section\b[^>]*\bid="video-module"[^>]*>[\s\S]*?</section>[ \t]*\n?'
)
RE_VIDEO_PAIR = re.compile(r"[ \t]*<video\b[^>]*>[\s\S]*?</video>[ \t]*\n?", re.I)
RE_VIDEO_SELF = re.compile(r"[ \t]*<video\b[^>]*/>[ \t]*\n?", re.I)
RE_SOURCE_MP4 = re.compile(r"[ \t]*<source\b[^>]*\.mp4[^>]*>[ \t]*\n?", re.I)


def clean_html(html: str) -> tuple[str, list[str]]:
    notes = []
    out = html
    for name, pat in (
        ("video-module", RE_VIDEO_MODULE),
        ("video-pair", RE_VIDEO_PAIR),
        ("video-self", RE_VIDEO_SELF),
        ("source-mp4", RE_SOURCE_MP4),
    ):
        out2, n = pat.subn("\n", out)
        if n:
            notes.append(f"{name}x{n}")
            out = out2
    return out, notes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    changed = 0
    total_notes: dict[str, int] = {}
    for p in sorted((ROOT / "community").rglob("index.html")):
        src = p.read_text(encoding="utf-8", errors="replace")
        out, notes = clean_html(src)
        if not notes:
            continue
        changed += 1
        for n in notes:
            k = re.sub(r"\d+$", "N", n)
            total_notes[k] = total_notes.get(k, 0) + 1
        if args.apply and not args.dry_run:
            p.write_text(out, encoding="utf-8")
        rel = p.relative_to(ROOT)
        print(f"  {rel}: {','.join(notes)}")

    print(f"{'写入' if args.apply and not args.dry_run else '计划修改'} {changed} 门 HTML")
    print("汇总:", total_notes)

    if args.apply and not args.dry_run:
        mp4s = subprocess.run(
            ["git", "ls-files", "*.mp4"], cwd=ROOT, capture_output=True, text=True
        ).stdout.split()
        print(f"git rm {len(mp4s)} 个 mp4 …")
        if mp4s:
            r = subprocess.run(["git", "rm", "-q", "--"] + mp4s, cwd=ROOT)
            if r.returncode != 0:
                print("git rm 失败", file=sys.stderr)
                return 1
        # 未跟踪的 mp4 也清掉（构建产物等）
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard", "*.mp4"],
            cwd=ROOT, capture_output=True, text=True,
        ).stdout.split()
        for f in untracked:
            Path(ROOT / f).unlink(missing_ok=True)
        print(f"另删未跟踪 mp4 {len(untracked)} 个")
    else:
        n = subprocess.run(
            ["git", "ls-files", "*.mp4"], cwd=ROOT, capture_output=True, text=True
        ).stdout.count("\n")
        print(f"(dry-run) 跟踪中的 mp4 文件: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
