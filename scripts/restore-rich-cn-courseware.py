#!/usr/bin/env python3
"""从 git 恢复被 cn-spec 批量升级覆盖的精细课件。

检测：当前 HTML 为短模板（无 brand-bar、<400 行），且 git 历史存在明显更长版本。
恢复：checkout 指定 ref 的 index.html / assets / manifest（可选），并统一 /assets/scripts/ 路径。

用法：
  python3 scripts/restore-rich-cn-courseware.py --dry-run
  python3 scripts/restore-rich-cn-courseware.py --course chn-h-red-chamber
  python3 scripts/restore-rich-cn-courseware.py --ref f7440731
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
DEFAULT_REF = "4cc329f6"  # 批量模板覆盖前（915ae735 之前）


def git_show(ref: str, rel: str) -> bytes | None:
    r = subprocess.run(
        ["git", "show", f"{ref}:{rel}"],
        cwd=ROOT,
        capture_output=True,
    )
    return r.stdout if r.returncode == 0 else None


def line_count(path: Path) -> int:
    if not path.is_file():
        return 0
    return len(path.read_text(encoding="utf-8", errors="replace").splitlines())


def is_generic_template(html: str) -> bool:
    if "teachany-brand-bar" in html:
        return False
    if 'id="slide-container"' in html and "teachany-high-pro" in html:
        return True
    if len(html.splitlines()) < 450 and "data-scaffold=" in html:
        return True
    return False


def rewrite_scripts(html: str) -> str:
    for pat, rep in (
        (r"\./assets/scripts/", "/assets/scripts/"),
        (r"\.\./\./assets/scripts/", "/assets/scripts/"),
        (r"\.\./assets/scripts/", "/assets/scripts/"),
        (r"\.\./\.\./assets/scripts/", "/assets/scripts/"),
    ):
        html = re.sub(pat, rep, html)
    html = re.sub(
        r'((?:href|src)=["\'])assets/scripts/',
        r"\1/assets/scripts/",
        html,
        flags=re.I,
    )
    return html


def list_course_dirs() -> list[Path]:
    out = []
    for d in sorted(COMMUNITY.iterdir()):
        if d.is_dir() and (d / "index.html").is_file():
            out.append(d)
    return out


def restore_course(cid: str, ref: str, *, dry_run: bool = False, assets: bool = True) -> tuple[bool, str]:
    course = COMMUNITY / cid
    html_path = course / "index.html"
    if not html_path.is_file():
        return False, "no index.html"

    cur = html_path.read_text(encoding="utf-8", errors="replace")
    old_bytes = git_show(ref, f"community/{cid}/index.html")
    if not old_bytes:
        return False, "no git history at ref"
    old = old_bytes.decode("utf-8", errors="replace")
    old_lines = len(old.splitlines())
    cur_lines = len(cur.splitlines())

    if old_lines <= cur_lines * 1.3 and not (is_generic_template(cur) and not is_generic_template(old)):
        return False, f"skip (old {old_lines} vs cur {cur_lines})"

    if not dry_run:
        new_html = rewrite_scripts(old)
        html_path.write_text(new_html, encoding="utf-8")
        if assets:
            # 列出 git 中 assets 文件并恢复
            ls = subprocess.run(
                ["git", "ls-tree", "-r", "--name-only", ref, f"community/{cid}/assets"],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            if ls.returncode == 0:
                for rel in ls.stdout.strip().splitlines():
                    if not rel or rel.endswith("/"):
                        continue
                    data = git_show(ref, rel)
                    if data is None:
                        continue
                    dest = ROOT / rel
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(data)
        mf = git_show(ref, f"community/{cid}/manifest.json")
        if mf and not dry_run:
            (course / "manifest.json").write_bytes(mf)

    return True, f"restored {old_lines}L (was {cur_lines}L)"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default=DEFAULT_REF)
    ap.add_argument("--course", default="")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--all-candidates", action="store_true")
    args = ap.parse_args()

    if args.course:
        targets = [args.course]
    else:
        targets = [d.name for d in list_course_dirs()]

    restored = skipped = 0
    for cid in targets:
        ok, msg = restore_course(cid, args.ref, dry_run=args.dry_run, assets=True)
        if ok:
            restored += 1
            print(f"✅ {cid}: {msg}")
        elif args.all_candidates or args.course:
            if "skip" not in msg and "no git" not in msg:
                print(f"⚠️  {cid}: {msg}")
            elif args.course:
                print(f"⏭️  {cid}: {msg}")
            skipped += 1
        else:
            skipped += 1

    print(f"\n{'Would restore' if args.dry_run else 'Restored'} {restored}, skipped {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
