#!/usr/bin/env python3
"""全库课件质检总览：挂载 / 教学质量 / 22项 / 升级标准 / 基础设施。"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
REPORTS = ROOT / "reports"
SKIP = {"drafts", "pending", "archive", "reading-academy"}


def list_courses() -> list[str]:
    return sorted(
        p.name
        for p in COMMUNITY.iterdir()
        if p.is_dir() and not p.name.startswith(".") and p.name not in SKIP
    )


def run_mount(cid: str) -> list[str]:
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate-courseware.py"), cid],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    out = (r.stdout or "") + (r.stderr or "")
    errs = []
    for ln in out.splitlines():
        ln = ln.strip()
        if ln.startswith("❌") and "错误: 0" not in ln and cid in ln:
            errs.append(ln.replace("❌", "").strip())
    return errs


def run_teaching(cid: str) -> list[str]:
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate-teaching-quality.py"), cid, "--json"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError:
        return ["teaching-quality: parse error"]
    return [i["message"] for i in data.get("issues", []) if i.get("level") == "error"]


def run_22(cid: str) -> list[str]:
    mod = ROOT / "scripts" / "qc-all-py.py"
    # inline minimal check: import checks from qc-all-py
    import importlib.util

    spec = importlib.util.spec_from_file_location("qc_all", mod)
    qc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(qc)
    cdir = str(COMMUNITY / cid)
    hpath = COMMUNITY / cid / "index.html"
    if not hpath.exists():
        return ["no index.html"]
    html = hpath.read_text(encoding="utf-8", errors="ignore")
    meta = qc.get_meta(html)
    return qc.checks(html, meta, cdir)


def infra_issues(cid: str) -> list[str]:
    issues = []
    html_path = COMMUNITY / cid / "index.html"
    if not html_path.exists():
        return ["no_html"]
    html = html_path.read_text(encoding="utf-8", errors="ignore")
    if re.search(r'(?:href|src)=["\'](?:\./|\.\./)?assets/scripts/', html):
        issues.append("local_script_paths")
    if re.search(r'\bL\.map\s*\(', html) and "data-teachany-map" not in html:
        issues.append("handwritten_map")
    return issues


def upgrade_issues(cid: str, html: str) -> list[str]:
    issues = []
    if cid.startswith("phy-m-"):
        if "phet.colorado.edu" not in html or 'id="phet-lab"' not in html:
            issues.append("phy_no_phet")
        if "ta-fig-tag" not in html:
            issues.append("phy_no_labels")
        if not all(x in html for x in ("practice-l1", "practice-l2", "practice-l3")):
            issues.append("phy_no_L123")
    return issues


def audit_one(cid: str) -> dict:
    html = ""
    hpath = COMMUNITY / cid / "index.html"
    if hpath.exists():
        html = hpath.read_text(encoding="utf-8", errors="ignore")
    mount = run_mount(cid)
    teaching = run_teaching(cid)
    checks22 = run_22(cid)
    infra = infra_issues(cid)
    upgrade = upgrade_issues(cid, html)
    all_issues = mount + teaching + checks22 + infra + upgrade
    return {
        "id": cid,
        "ok": not all_issues,
        "mount": mount,
        "teaching": teaching,
        "checks22": checks22,
        "infra": infra,
        "upgrade": upgrade,
        "issue_count": len(all_issues),
    }


def write_html(report: dict, path: Path) -> None:
  rows = []
  for r in report["failed"]:
      tags = []
      if r["mount"]:
          tags.append("挂载")
      if r["teaching"]:
          tags.append("教学")
      if r["checks22"]:
          tags.append("22项")
      if r["infra"]:
          tags.append("基础")
      if r["upgrade"]:
          tags.append("升级")
      rows.append(
          f'<tr><td><a href="/community/{r["id"]}/index.html">{r["id"]}</a></td>'
          f'<td>{", ".join(tags)}</td><td class="dim">{r["issue_count"]}</td></tr>'
      )
  html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><title>全库质检总览</title>
<style>
body{{font-family:system-ui;background:#0b1220;color:#e2e8f0;max-width:960px;margin:32px auto;padding:0 20px}}
h1{{font-size:1.6rem}} .stat{{display:flex;gap:16px;flex-wrap:wrap;margin:16px 0}}
.stat span{{background:rgba(59,130,246,.15);padding:10px 14px;border-radius:10px}}
.ok{{color:#34d399}} .warn{{color:#fbbf24}}
table{{width:100%;border-collapse:collapse;margin-top:20px}}
th,td{{text-align:left;padding:10px;border-bottom:1px solid rgba(148,163,184,.15)}}
a{{color:#93c5fd;text-decoration:none}} .dim{{color:#94a3b8}}
</style></head><body>
<h1>TeachAny 全库课件质检</h1>
<p class="dim">生成于 {report["generated_at"]}</p>
<div class="stat">
  <span>总计 <strong>{report["total"]}</strong></span>
  <span class="ok">通过 <strong>{report["pass"]}</strong></span>
  <span class="warn">待修 <strong>{report["fail"]}</strong></span>
</div>
<h2>分类统计</h2>
<ul>
{"".join(f"<li>{k}: {v}</li>" for k,v in report["category_counts"].items())}
</ul>
<h2>待修课件（{report["fail"]}）</h2>
<table><thead><tr><th>课件</th><th>类别</th><th>项数</th></tr></thead>
<tbody>
{"".join(rows) if rows else '<tr><td colspan="3" class="ok">全部通过</td></tr>'}
</tbody></table>
</body></html>"""
  path.write_text(html, encoding="utf-8")


def main() -> int:
    courses = list_courses()
    print(f"Auditing {len(courses)} courses…")
    results = []
    with ThreadPoolExecutor(max_workers=10) as ex:
        futs = {ex.submit(audit_one, c): c for c in courses}
        done = 0
        for fut in as_completed(futs):
            done += 1
            results.append(fut.result())
            if done % 100 == 0:
                print(f"  {done}/{len(courses)}", flush=True)
    results.sort(key=lambda x: (-x["issue_count"], x["id"]))
    failed = [r for r in results if not r["ok"]]
    from collections import Counter

    cat = Counter()
    for r in failed:
        for k, v in (("mount", r["mount"]), ("teaching", r["teaching"]), ("checks22", r["checks22"]),
                     ("infra", r["infra"]), ("upgrade", r["upgrade"])):
            if v:
                cat[k] += 1
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total": len(courses),
        "pass": len(courses) - len(failed),
        "fail": len(failed),
        "category_counts": dict(cat),
        "failed": failed,
        "courses": results,
    }
    REPORTS.mkdir(exist_ok=True)
    (REPORTS / "qc-master.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_html(report, ROOT / "qc-master.html")
    print(f"PASS {report['pass']} FAIL {report['fail']}")
    for k, v in cat.most_common():
        print(f"  {k}: {v}")
    print("→ reports/qc-master.json, qc-master.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
