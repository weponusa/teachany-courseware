#!/usr/bin/env python3
"""全面检查：优先保证「历史最佳版」在线，不做破坏性升级。

1. 扫描是否仍有被模板覆盖的精细课（可 restore）
2. 结构层 audit（缺图/死链/模块路径）
3. 输出报告，不自动 upgrade

用法：
  python3 scripts/check-cn-best-version.py
  python3 scripts/check-cn-best-version.py --fix-paths
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"


def load_loop():
    spec = importlib.util.spec_from_file_location("loop", ROOT / "scripts/courseware-quality-loop.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix-paths", action="store_true", help="仅修 /assets/scripts/ 路径")
    ap.add_argument("--try-restore", action="store_true", help="恢复仍可找回的精细版")
    args = ap.parse_args()

    if args.try_restore:
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts/restore-rich-cn-courseware.py"), "--all-candidates"],
            cwd=ROOT,
        )
        if r.returncode != 0:
            return r.returncode

    loop = load_loop()
    courses = loop.iter_courses(cn_only=True)
    rows = []
    degraded = 0
    for d in courses:
        html = (d / "index.html").read_text(encoding="utf-8", errors="replace")
        if loop.is_generic_template_html(html) and loop.cn_spec_for_course(d.name):
            # 有 spec 但已是短模板 — 可能是本来就没有精细版
            pass
        if "teachany-brand-bar" not in html and len(html.splitlines()) < 400:
            if loop.cn_spec_for_course(d.name):
                degraded += 1
        if args.fix_paths:
            new, n = loop.rewrite_site_root_script_paths(html)
            if n:
                (d / "index.html").write_text(new, encoding="utf-8")
        row = loop.audit_course(d)
        rows.append(row)

    bad = [r for r in rows if r["issues"]]
    report = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "total": len(rows),
        "with_issues": len(bad),
        "possible_template_only": degraded,
        "courses": rows,
    }
    out = REPORTS / "cn-best-version-check.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"课标课 {len(rows)} 门 · 结构问题 {len(bad)} · 短模板 {degraded}")
    print(f"报告 → {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
