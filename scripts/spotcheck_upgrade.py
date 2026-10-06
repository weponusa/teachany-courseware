#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""中文课件批量升级 · 每5抽1抽检工具。

用法:
  python3 scripts/spotcheck_upgrade.py <cid> [<cid> ...]   # 抽检指定课件
  python3 scripts/spotcheck_upgrade.py --pending           # 抽检名单中新完成且未检的

检查项:
  1. batch-quality-check.py 单科质检通过
  2. 含 teachany-upgrade-v2 标记, 选择题 .tu-q >= 3
  3. 无 "And 已有经验"/"角色任务:"/"变量A" 等空壳残留
  4. HTML 引用的本地图片文件真实存在

结果追加到 reports/upgrade-zh-spotcheck.md
"""
from __future__ import annotations

import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
REPORT = ROOT / "reports" / "upgrade-zh-spotcheck.md"
SPOT_LIST = ROOT / "data" / "upgrade-zh-spotcheck-list.txt"
MARKER = "teachany-upgrade-v2"


def check_one(cid: str) -> tuple[bool, list[str]]:
    problems: list[str] = []
    html_path = COMMUNITY / cid / "index.html"
    if not html_path.exists():
        return False, ["无 index.html"]
    html = html_path.read_text(encoding="utf-8", errors="ignore")

    if MARKER not in html:
        problems.append("缺 v2 标记(未升级)")
        return False, problems  # 未升级则后续检查无意义

    if html.count('class="tu-q"') < 3:
        problems.append(f"选择题不足3道({html.count('class=\"tu-q\"')})")

    for pat in ["And 已有经验", "角色任务：", "变量A", "变量B"]:
        if pat in html:
            problems.append(f"空壳残留: {pat}")

    # 本地图片存在性
    for src in re.findall(r'<img[^>]+src="([^"]+)"', html):
        if src.startswith(("http://", "https://", "data:", "//")):
            continue
        p = (COMMUNITY / cid / src.lstrip("./")).resolve()
        if not p.exists():
            problems.append(f"图片缺失: {src}")

    # 单科质检
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "batch-quality-check.py"), cid],
        capture_output=True, text=True, timeout=120,
    )
    if "不合格" in r.stdout and f"- {cid}" in r.stdout:
        m = re.search(rf"- {re.escape(cid)}: (.+)", r.stdout)
        problems.append("QC不合格: " + (m.group(1) if m else "").strip())

    return (len(problems) == 0), problems


def already_reported() -> set[str]:
    if not REPORT.exists():
        return set()
    return set(re.findall(r"^\| `([^`]+)`", REPORT.read_text(encoding="utf-8"), re.M))


def append_report(cid: str, ok: bool, problems: list[str]) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    if not REPORT.exists():
        REPORT.write_text(
            "# 中文课件升级抽检报告(每5抽1)\n\n"
            "| 课件 | 时间 | 结果 | 问题 |\n|---|---|---|---|\n",
            encoding="utf-8",
        )
    ts = datetime.now().strftime("%m-%d %H:%M")
    status = "✅ 通过" if ok else "❌ 问题"
    issue = "; ".join(problems) if problems else "-"
    with REPORT.open("a", encoding="utf-8") as f:
        f.write(f"| `{cid}` | {ts} | {status} | {issue} |\n")


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    done = already_reported()
    if args == ["--pending"]:
        cids = []
        for ln in SPOT_LIST.read_text(encoding="utf-8").split():
            if ln in done:
                continue
            html_path = COMMUNITY / ln / "index.html"
            if html_path.exists() and MARKER in html_path.read_text(encoding="utf-8", errors="ignore"):
                cids.append(ln)
        if not cids:
            print("暂无新完成待抽检的样本")
            return
    else:
        cids = [c for c in args if c not in done]
    ok_n = 0
    for cid in cids:
        ok, problems = check_one(cid)
        append_report(cid, ok, problems)
        print(f"{'✅' if ok else '❌'} {cid}" + ("" if ok else " — " + "; ".join(problems)))
        ok_n += ok
    print(f"\n本轮抽检 {len(cids)} 门: 通过 {ok_n}, 问题 {len(cids) - ok_n}")


if __name__ == "__main__":
    main()
