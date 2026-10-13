#!/usr/bin/env python3
"""审核并合并「链接投稿」——把外链课件正式收进社区库。

背景
----
用户通过 Pages Functions 投稿（POST /api/submit-link）后，会生成一个 PR，
里面只有 `community/pending-links/<course-id>.json` 一个元数据文件。
但社区的 `community/index.json` 由 `scripts/sync-community-index.py` 从
`registry.json` 生成，而 sync 有两个硬条件：

  1. registry.json 里要有该条目
  2. `community/<path>/index.html` 必须存在

纯外链投稿两条都不满足 —— 就算手工塞进 index.json，下次 sync 也会把它冲掉。
所以「审核通过」这个动作必须真正落地为仓库内的一份可寻址资产。

本脚本做的事
------------
对每条待审投稿：

  a. 生成 `community/<course-id>/index.html`  —— 落地页（介绍 + 跳转外链）
  b. 生成 `community/<course-id>/manifest.json` —— 对齐标准课件 manifest 字段
  c. 在 `registry.json` 登记条目（hosting=external-link + source_url 留档）
  d. 删除 `community/pending-links/<course-id>.json`
  e. 刷新 `community/index.json`（跑 sync-community-index.py）

配合 sync 的改动：registry 里 hosting=external-link 的条目，
index.json 的 `download_url` 直接写真实外链（而不是仓库内路径），
Gallery 卡片因此可以直达外部课件页。

用法
----
  python3 scripts/approve-link-submission.py --list
  python3 scripts/approve-link-submission.py <course-id>
  python3 scripts/approve-link-submission.py <course-id> --dry-run
  python3 scripts/approve-link-submission.py --all
  python3 scripts/approve-link-submission.py --all --no-sync
"""
from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry.json"
COMMUNITY = ROOT / "community"
PENDING = COMMUNITY / "pending-links"
SYNC = ROOT / "scripts" / "sync-community-index.py"

# 学科规范名 -> 展示名（与社区索引保持一致）
SUBJECT_LABEL = {
    "math": "数学", "chinese": "语文", "english": "英语",
    "physics": "物理", "chemistry": "化学", "biology": "生物",
    "history": "历史", "geography": "地理", "politics": "政治",
    "science": "科学", "info-tech": "信息技术", "cross": "跨学科",
    "psychology": "心理", "economics": "经济", "humanities": "人文",
    "inquiry": "探究", "misc": "其他",
}

# 学段推断（cn-national）
STAGE_BY_GRADE = [(1, 6, "elementary"), (7, 9, "middle"), (10, 12, "high")]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def save_json(path: Path, data, indent: int = 2) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=indent) + "\n",
        encoding="utf-8",
    )


def stage_of(grade) -> str:
    try:
        g = int(grade)
    except (TypeError, ValueError):
        return ""
    for lo, hi, name in STAGE_BY_GRADE:
        if lo <= g <= hi:
            return name
    return ""


def grade_num(grade) -> int:
    """registry 里的 grade 混杂 int 与 'high'/'middle' 之类字符串，排序时统一成数字。"""
    try:
        return int(grade)
    except (TypeError, ValueError):
        return 0


def pending_files() -> list[Path]:
    if not PENDING.exists():
        return []
    return sorted(p for p in PENDING.glob("*.json") if p.is_file())


# ---------------------------------------------------------------- 落地页模板

SHELL_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="teachany-template-version" content="link-shell-1.0">
<meta name="teachany-hosting" content="external-link">
<title>{name} · {subject_label} · TeachAny</title>
<meta name="description" content="{name} —— {subject_label}{grade_text} 社区课件（外部托管）">
<style>
  :root {{
    --bg:#f6f8fb; --card:#fff; --ink:#12212f; --dim:#5b6b7c;
    --line:#e3e9f0; --brand:#0b64c8; --brand-dark:#084e9e; --warn:#b8860b;
  }}
  * {{ box-sizing:border-box; }}
  body {{
    margin:0; min-height:100vh; background:var(--bg); color:var(--ink);
    font:15px/1.7 -apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
    display:flex; align-items:center; justify-content:center; padding:32px 18px;
  }}
  .card {{
    width:100%; max-width:560px; background:var(--card); border:1px solid var(--line);
    border-radius:16px; padding:34px 30px 28px; box-shadow:0 8px 30px rgba(18,33,47,.06);
  }}
  .badge {{
    display:inline-flex; align-items:center; gap:6px; font-size:12px; color:var(--dim);
    background:#eef3f9; border-radius:999px; padding:4px 11px; margin-bottom:16px;
  }}
  .dot {{ width:6px; height:6px; border-radius:50%; background:#2e9e5b; display:inline-block; }}
  h1 {{ font-size:23px; line-height:1.4; margin:0 0 10px; letter-spacing:.2px; }}
  .meta {{ color:var(--dim); font-size:13.5px; margin-bottom:20px; }}
  .meta span + span::before {{ content:"·"; margin:0 8px; color:#c3ccd6; }}
  .desc {{
    color:#33475b; font-size:14px; background:#fafcfe; border:1px solid var(--line);
    border-radius:10px; padding:13px 15px; margin-bottom:22px; white-space:pre-wrap;
  }}
  .desc:empty {{ display:none; }}
  .btn {{
    display:block; width:100%; text-align:center; text-decoration:none;
    background:var(--brand); color:#fff; font-size:15.5px; font-weight:600;
    padding:14px 18px; border-radius:10px; transition:background .15s;
  }}
  .btn:hover {{ background:var(--brand-dark); }}
  .url {{
    margin-top:12px; font-size:12px; color:var(--dim); word-break:break-all;
    text-align:center; line-height:1.6;
  }}
  .url a {{ color:var(--dim); }}
  .tip {{
    margin-top:20px; padding-top:16px; border-top:1px solid var(--line);
    font-size:12.5px; color:var(--dim); line-height:1.75;
  }}
  .countdown {{ font-variant-numeric:tabular-nums; color:var(--warn); font-weight:600; }}
</style>
</head>
<body>
  <main class="card">
    <div class="badge"><span class="dot"></span>社区课件 · 外部托管</div>
    <h1>{name}</h1>
    <div class="meta">{meta_html}</div>
    <div class="desc">{description}</div>
    <a class="btn" id="go" href="{url}" rel="noopener">打开课件 →</a>
    <div class="url">来源：<a href="{url}" rel="noopener">{url_display}</a></div>
    <div class="tip">
      <span id="tip">本课件由投稿者托管在外部站点，<span class="countdown" id="cd">{delay}</span> 秒后自动跳转。</span>
      <br>如长时间未跳转，请手动点击上方按钮。版权与内容责任归原托管方。
    </div>
  </main>
<script>
(function () {{
  var url = {url_js};
  var cd = document.getElementById('cd');
  var left = {delay};
  document.getElementById('go').addEventListener('click', function () {{
    if (cd) cd.textContent = '0';
  }});
  var t = setInterval(function () {{
    left -= 1;
    if (cd) cd.textContent = String(left > 0 ? left : 0);
    if (left <= 0) {{ clearInterval(t); location.replace(url); }}
  }}, 1000);
}})();
</script>
</body>
</html>
"""


def render_shell(meta: dict, delay: int = 5) -> str:
    subject = meta.get("subject") or "misc"
    subject_label = SUBJECT_LABEL.get(subject, subject)
    grade = meta.get("grade")
    grade_text = f" · G{grade}" if grade not in (None, "", 0) else ""

    bits = [f"{subject_label}{grade_text}".strip()]
    if meta.get("author"):
        bits.append(f"作者：{meta['author']}")
    if meta.get("submitted_at"):
        bits.append("投稿：" + str(meta["submitted_at"])[:10])
    meta_html = "".join(f"<span>{html.escape(str(b))}</span>" for b in bits if b)

    url = meta.get("source_url") or meta.get("download_url") or ""
    return SHELL_TEMPLATE.format(
        name=html.escape(str(meta.get("name") or meta.get("id") or "未命名课件")),
        subject_label=html.escape(subject_label),
        grade_text=html.escape(grade_text),
        meta_html=meta_html,
        description=html.escape(str(meta.get("description") or "")),
        url=html.escape(url, quote=True),
        url_display=html.escape(url),
        url_js=json.dumps(url),
        delay=delay,
    )


def build_manifest(meta: dict, course_id: str) -> dict:
    subject = meta.get("subject") or "misc"
    grade = meta.get("grade", 0)
    tags = meta.get("tags") or []
    if not tags:
        label = SUBJECT_LABEL.get(subject, subject)
        tags = [f"{label}G{grade}" if grade else label, str(meta.get("name") or course_id)]
    return {
        "id": course_id,
        "course_id": course_id,
        "node_id": meta.get("node_id") or course_id,
        "name": meta.get("name") or course_id,
        "name_en": meta.get("name_en", ""),
        "subject": subject,
        "grade": grade,
        "stage": stage_of(grade),
        "status": "community",
        "author": meta.get("author") or "匿名用户",
        "version": "1.0.0",
        "license": meta.get("license", "MIT"),
        "description": meta.get("description") or "",
        "tags": tags,
        "hosting": "external-link",
        "source_url": meta.get("source_url") or meta.get("download_url") or "",
        "page_title": meta.get("page_title", ""),
        "link_status": meta.get("link_status"),
        "link_reachable": meta.get("link_reachable"),
        "looks_like_courseware": meta.get("looks_like_courseware"),
        "submit_channel": meta.get("submit_channel", ""),
        "submitted_at": meta.get("submitted_at", ""),
        "curriculum_standards": [
            {
                "source": meta.get("curriculum_source")
                or "投稿者自述 / 待人工核对课标对应关系",
                "content": f"本课《{meta.get('name') or course_id}》由社区用户投稿，"
                           f"经审核后收进社区库；课标对应关系以原托管页说明为准。",
            }
        ],
        "assets": {},
        "prerequisites": [],
        "leads_to": [],
    }


def build_registry_entry(meta: dict, course_id: str) -> dict:
    subject = meta.get("subject") or "misc"
    grade = meta.get("grade", 0)
    entry = {
        "id": course_id,
        "name": meta.get("name") or course_id,
        "name_en": meta.get("name_en", ""),
        "subject": subject,
        "grade": grade,
        "node_id": meta.get("node_id") or course_id,
        "domain": "",
        "description": meta.get("description") or "",
        "description_zh": meta.get("description") or "",
        "emoji": "🔗",
        "tags": meta.get("tags") or [],
        "difficulty": 1,
        "duration": "",
        "lines": "",
        "created": meta.get("submitted_at", ""),
        "version": "1.0.0",
        "license": meta.get("license", "MIT"),
        "status": "community",
        "path": f"community/{course_id}",
        "has_tts": False,
        "has_video": False,
        "has_en": False,
        "author": meta.get("author") or "匿名用户",
        "teachany_version": "",
        "curriculum": "cn-national",
        "hero_image": "",
        "scene_image": "",
        "variant": "",
        "overridden": False,
        # 外链投稿专有字段
        "hosting": "external-link",
        "source_url": meta.get("source_url") or meta.get("download_url") or "",
        "submit_channel": meta.get("submit_channel", ""),
    }
    return entry


# ------------------------------------------------------------------ 主流程

def approve(path: Path, dry_run: bool = False, force: bool = False) -> dict:
    meta = load_json(path, None)
    if not isinstance(meta, dict):
        return {"file": path.name, "ok": False, "reason": "JSON 解析失败"}

    course_id = meta.get("id") or path.stem
    url = meta.get("source_url") or meta.get("download_url") or ""

    if not url:
        return {"file": path.name, "ok": False, "reason": "缺少 source_url / download_url"}
    if not re.match(r"^https?://", url):
        return {"file": path.name, "ok": False, "reason": f"链接协议不合法：{url}"}
    if meta.get("link_reachable") is False:
        return {"file": path.name, "ok": False, "reason": "投稿时连通性检查未通过，需人工确认"}

    target_dir = COMMUNITY / course_id

    reg = load_json(REGISTRY, {"courses": []})
    if any(c.get("id") == course_id for c in reg.get("courses", [])):
        return {"file": path.name, "ok": False, "reason": f"registry 中已存在 id={course_id}"}

    # 同一条外链重复投稿：落地页 id 带时间戳永不撞车，所以只靠 id 判重会放进重复条目。
    # 同一 node_id + 同一 source_url 已入库时默认拦下，除非显式 --force。
    node = meta.get("node_id") or course_id
    dup = [
        c for c in reg.get("courses", [])
        if c.get("hosting") == "external-link"
        and c.get("node_id") == node
        and (c.get("source_url") or "") == url
    ]
    if dup and not force:
        return {
            "file": path.name, "ok": False,
            "reason": f"同一外链已入库：{dup[0]['id']}（确认要重投请加 --force）",
        }

    # 目录已存在视为重跑（上一次可能中途失败），允许覆盖落地页
    overwrite = target_dir.exists()

    if dry_run:
        return {
            "file": path.name, "ok": True, "dry_run": True, "id": course_id,
            "url": url,
            "would_create": [f"community/{course_id}/index.html",
                             f"community/{course_id}/manifest.json"],
            "would_register": course_id,
            "would_delete": f"community/pending-links/{path.name}",
            "overwrite": overwrite,
        }

    # a. 落地页
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "index.html").write_text(render_shell(meta), encoding="utf-8")

    # b. manifest
    save_json(target_dir / "manifest.json", build_manifest(meta, course_id))

    # c. registry 登记（按 subject/grade/name 排序插入，保持文件可读）
    courses = reg.get("courses", [])
    courses.append(build_registry_entry(meta, course_id))
    courses.sort(key=lambda c: (str(c.get("subject", "")), grade_num(c.get("grade")),
                                str(c.get("id", ""))))
    reg["courses"] = courses
    reg["total"] = len(courses)
    reg["updated"] = now_iso().replace("+00:00", "Z")
    save_json(REGISTRY, reg)

    # d. 删除 pending
    path.unlink()

    return {"file": path.name, "ok": True, "id": course_id, "url": url,
            "registry_total": len(courses)}


def main() -> int:
    ap = argparse.ArgumentParser(description="审核并合并链接投稿")
    ap.add_argument("course_id", nargs="?", help="待审投稿的 course-id（文件名去 .json）")
    ap.add_argument("--all", action="store_true", help="处理全部待审投稿")
    ap.add_argument("--list", action="store_true", help="只列出待审投稿")
    ap.add_argument("--dry-run", action="store_true", help="只预览，不写任何文件")
    ap.add_argument("--force", action="store_true", help="同一条外链重复投稿时允许强制入库")
    ap.add_argument("--no-sync", action="store_true", help="不自动刷新 community/index.json")
    args = ap.parse_args()

    files = pending_files()

    if args.list:
        if not files:
            print("community/pending-links/ 下没有待审投稿。")
            return 0
        print(f"待审投稿 {len(files)} 条：")
        for p in files:
            m = load_json(p, {})
            print(f"  - {p.stem}")
            print(f"      名称: {m.get('name')} | 学科: {m.get('subject')} | 年级: {m.get('grade')}")
            print(f"      链接: {m.get('source_url') or m.get('download_url')}")
            print(f"      连通: {m.get('link_status')} / 可达={m.get('link_reachable')} / 像课件={m.get('looks_like_courseware')}")
        return 0

    if args.all:
        targets = files
    elif args.course_id:
        targets = [PENDING / f"{args.course_id}.json"]
    else:
        ap.print_help()
        return 2

    if not targets:
        print("没有需要处理的投稿。")
        return 0

    results = []
    for p in targets:
        if not p.exists():
            results.append({"file": p.name, "ok": False, "reason": "文件不存在"})
            continue
        results.append(approve(p, dry_run=args.dry_run, force=args.force))

    ok = [r for r in results if r.get("ok")]
    bad = [r for r in results if not r.get("ok")]

    print(f"{'[dry-run] ' if args.dry_run else ''}合并结果：成功 {len(ok)} / 失败 {len(bad)}")
    for r in ok:
        if r.get("dry_run"):
            print(f"  ✓ {r['file']} → {r['id']}")
            print(f"      将创建: {', '.join(r['would_create'])}")
            print(f"      将登记 registry，并删除 {r['would_delete']}")
        else:
            print(f"  ✓ {r['file']} → community/{r['id']}/   registry 现有 {r['registry_total']} 条")
            print(f"      外链: {r['url']}")
    for r in bad:
        print(f"  ✗ {r['file']}：{r.get('reason')}")

    if ok and not args.dry_run and not args.no_sync:
        print("\n刷新 community/index.json ...")
        proc = subprocess.run([sys.executable, str(SYNC)], capture_output=True, text=True)
        print(proc.stdout.strip() or "(无输出)")
        if proc.returncode != 0:
            print("sync 失败：", proc.stderr.strip())
            return 1

    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
