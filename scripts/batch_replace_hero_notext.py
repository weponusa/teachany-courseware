#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全库 Hero 无字化：Agnes 无字生图 + HTML ta-fig-tag 叠标（对齐 phy-m 标准）。

对图内带字/乱码的 hero（或尚未标记 teachany-hero-notext 的课）重新生图，
写入 community/<id>/assets/<id>-hero.png，并保证 HTML 使用 .ta-figure-labeled 叠中文。

额度：每课 Agnes 限额 3 张 → 使用独立 course_id「{cid}-ntv1」占新槽位。
限流：IP RPM≈10 → 默认每次成功后 sleep 7s。

用法：
  # 仅 OCR 扫描报告
  python3 scripts/batch_replace_hero_notext.py --scan-only

  # 替换（跳过已标记 / OCR clean）
  python3 scripts/batch_replace_hero_notext.py --limit 20
  python3 scripts/batch_replace_hero_notext.py --all
  python3 scripts/batch_replace_hero_notext.py --cid chem-m-neutralization --force

  # 只补叠标不生图
  python3 scripts/batch_replace_hero_notext.py --labels-only --all
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
REPORTS = ROOT / "reports"
STATE = ROOT / "data" / "hero-notext-state.json"
AGNES = ROOT / "scripts" / "agnes-image-gen.py"
SCAN = ROOT / "scripts" / "scan-agnes-image-text.py"

NO_TEXT = (
    ", absolutely no text, no letters, no numbers, no words, no Chinese characters, "
    "no labels, no signage, no captions, no watermarks in the image, illustration only"
)

LABEL_CSS = """
<style id="ta-labeled-figure-css">
.ta-figure-labeled{position:relative}.ta-figure-wrap{position:relative}
.ta-figure-labeled img{width:100%;border-radius:12px;display:block}
.ta-figure-tags{position:absolute;inset:0;pointer-events:none}
.ta-fig-tag{position:absolute;transform:translate(-50%,-50%);background:rgba(15,23,42,.88);color:#fff;font-size:13px;font-weight:700;padding:5px 11px;border-radius:8px;white-space:nowrap;box-shadow:0 4px 12px rgba(0,0,0,.25);border:1px solid rgba(56,189,248,.35)}
</style>
"""

SUBJECT_STYLE = {
    "chemistry": "chemistry lab glassware molecules beakers periodic motifs",
    "physics": "physics lab circuits forces energy waves dark navy",
    "math": "geometry shapes coordinate plane abstract math symbols as pure forms no glyphs",
    "biology": "cells plants animals ecosystems microscope motifs",
    "chinese": "classical books scrolls brush ink without readable characters",
    "english": "abstract language learning icons speech bubbles without letters",
    "history": "maps timelines artifacts silhouettes without readable text",
    "geography": "earth terrain climate icons without place-name text",
    "science": "elementary science experiments nature icons",
    "politics": "civic community icons balanced scales without slogans",
    "psychology": "mind wellness icons calm abstract shapes",
}


def load_scan():
    import importlib.util

    spec = importlib.util.spec_from_file_location("scan_agnes", SCAN)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_state() -> dict:
    if not STATE.exists():
        return {"done": [], "failed": [], "updated_at": None}
    raw = STATE.read_text(encoding="utf-8")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # 并发写可能产生尾部脏数据：只取第一个 JSON 对象
        try:
            obj, _ = json.JSONDecoder().raw_decode(raw)
            if isinstance(obj, dict):
                return obj
        except Exception:
            pass
        return {"done": [], "failed": [], "updated_at": None}


def save_state(state: dict) -> None:
    """原子写入 + 合并 done/failed，避免双 worker 互相覆盖/写坏 JSON。"""
    STATE.parent.mkdir(parents=True, exist_ok=True)
    lock_path = STATE.with_suffix(".lock")
    merged = {"done": [], "failed": [], "updated_at": None}
    with open(lock_path, "a+", encoding="utf-8") as lockf:
        try:
            import fcntl

            fcntl.flock(lockf.fileno(), fcntl.LOCK_EX)
        except Exception:
            pass
        try:
            disk = load_state()
            done = set(disk.get("done") or []) | set(state.get("done") or [])
            # failed: keep unique by id, prefer newer detail from `state`
            failed_map = {}
            for src in (disk.get("failed") or [], state.get("failed") or []):
                for f in src:
                    if isinstance(f, dict) and f.get("id"):
                        failed_map[f["id"]] = f
                    elif isinstance(f, str):
                        failed_map[f] = {"id": f, "detail": ""}
            # drop failed if now done
            for cid in list(failed_map):
                if cid in done:
                    failed_map.pop(cid, None)
            merged = {
                "done": sorted(done),
                "failed": list(failed_map.values())[-200:],  # cap bloat
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
            tmp = STATE.with_suffix(".tmp")
            tmp.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
            tmp.replace(STATE)
            # keep caller's view in sync
            state.clear()
            state.update(merged)
        finally:
            try:
                import fcntl

                fcntl.flock(lockf.fileno(), fcntl.LOCK_UN)
            except Exception:
                pass


def load_manifest(d: Path) -> dict:
    try:
        return json.loads((d / "manifest.json").read_text(encoding="utf-8"))
    except Exception:
        return {}


def course_title(d: Path, mf: dict | None = None) -> str:
    mf = mf or load_manifest(d)
    name = str(mf.get("name") or mf.get("title") or d.name).strip() or d.name
    # 去掉「— 七年级生物互动课件」等后缀噪声
    name = re.split(r"\s*[—–\-]\s*(?:七年级|八年级|九年级|高一|高二|高三|初中|高中|小学)", name)[0].strip()
    name = re.sub(r"（[^）]*互动课件[^）]*）|\([^)]*courseware[^)]*\)", "", name, flags=re.I).strip()
    return name or d.name


def pick_hero(d: Path) -> Path | None:
    assets = d / "assets"
    if not assets.is_dir():
        return None
    for pat in (
        f"{d.name}-hero.png",
        f"{d.name}-hero.webp",
        "hero.png",
        "hero-infographic.png",
        "hero-infographic.webp",
    ):
        p = assets / pat
        if p.exists() and p.stat().st_size > 10000:
            return p
    for p in list(assets.glob("*hero*.png")) + list(assets.glob("*hero*.webp")):
        if p.stat().st_size > 10000:
            return p
    return None


def hero_prompt(cid: str, title: str, subject: str) -> str:
    style = SUBJECT_STYLE.get(subject, "educational flat vector icons dark navy cyan amber")
    return (
        f"Educational knowledge-structure infographic for middle/high school course "
        f"about {title}, {style}, central hub with 5-6 illustrated concept panels, "
        f"flat vector, dark navy background, clean composition, museum quality"
        f"{NO_TEXT}"
    )


def ensure_label_css(html: str) -> str:
    if 'id="ta-labeled-figure-css"' in html:
        return html
    if "</head>" in html:
        return html.replace("</head>", LABEL_CSS + "\n</head>", 1)
    return LABEL_CSS + html


def tags_for(title: str) -> list[tuple[str, str, str]]:
    # topic + 4 pedagogic corners
    short = title[:10] if len(title) > 10 else title
    return [
        (short, "48%", "50%"),
        ("概念", "18%", "18%"),
        ("方法", "18%", "82%"),
        ("易错", "82%", "22%"),
        ("迁移", "82%", "78%"),
    ]


def hero_figure_html(cid: str, title: str) -> str:
    tags = "".join(
        f'<span class="ta-fig-tag" style="top:{top};left:{left}">{txt}</span>'
        for txt, top, left in tags_for(title)
    )
    return f"""
<section class="section" id="hero-infographic" data-bloom-level="understand" data-scaffold="full" data-tsh="知识结构主图">
<figure class="ta-standard-figure ta-figure-labeled">
  <div class="ta-figure-wrap">
    <img class="hero-cover-img" src="./assets/{cid}-hero.png" alt="{title}知识结构（无字）" loading="eager">
    <div class="ta-figure-tags" aria-hidden="true">{tags}</div>
  </div>
  <figcaption>无字生图 + HTML 中文叠标</figcaption>
</figure>
</section>
"""


def insert_or_replace_hero(html: str, cid: str, title: str) -> str:
    block = hero_figure_html(cid, title)

    # 1) 优先替换页首裸 cover（phy-m：首屏无字图 + 叠标）
    bare = re.search(
        r'(?:<!--\s*hero-cover\s*-->\s*)?<img[^>]*class=["\'][^"\']*hero-cover-img[^"\']*["\'][^>]*/?>',
        html,
        re.I,
    )
    if bare:
        # 若该 img 已在 ta-figure-labeled 内则跳过裸替换
        before = html[max(0, bare.start() - 200) : bare.start()]
        if "ta-figure-labeled" not in before and "ta-figure-wrap" not in before:
            html = html[: bare.start()] + block.strip() + html[bare.end() :]

    # 2) 同步/替换 hero-infographic 区块
    if re.search(r'id=["\']hero-infographic["\']', html):
        html2, n = re.subn(
            r'<section[^>]*id=["\']hero-infographic["\'][\s\S]*?</section>',
            block.strip(),
            html,
            count=1,
            flags=re.I,
        )
        if n:
            html = html2

    # 3) section.hero-cover
    if re.search(r'<section[^>]*class=["\'][^"\']*hero-cover', html, re.I):
        html2, n = re.subn(
            r'<section[^>]*class=["\'][^"\']*hero-cover[^"\']*["\'][\s\S]*?</section>',
            block.strip(),
            html,
            count=1,
            flags=re.I,
        )
        if n:
            return html2

    # 已有叠标则只校正 src
    if re.search(r'<span[^>]*class=["\'][^"\']*ta-fig-tag', html):
        html = re.sub(
            r'(src=["\'])(?:\./)?assets/[^"\']*hero[^"\']*\.(?:webp|png|jpg|jpeg)(["\'])',
            rf"\1./assets/{cid}-hero.png\2",
            html,
            count=3,
            flags=re.I,
        )
        return html

    # 4) 兜底：改 src 或插入
    if f"{cid}-hero.png" in html or "hero-cover-img" in html:
        html = re.sub(
            r'(<img[^>]+class=["\'][^"\']*hero-cover-img[^"\']*["\'][^>]+src=["\'])([^"\']+)(["\'])',
            rf"\1./assets/{cid}-hero.png\3",
            html,
            count=1,
            flags=re.I,
        )
        for anchor in (
            'id="knowledge-graph"',
            'id="teachany-ai-tutor-card"',
            "</body>",
        ):
            if anchor in html:
                return html.replace(anchor, block + "\n" + anchor, 1)
        return html
    return re.sub(r"(<body[^>]*>)", lambda m: m.group(0) + "\n" + block, html, count=1)


def mark_notext(html: str) -> str:
    if "teachany-hero-notext" in html:
        return html
    html2, n = re.subn(
        r"(<body[^>]*>)",
        r"\1\n<!-- teachany-hero-notext -->\n",
        html,
        count=1,
        flags=re.I,
    )
    if n:
        return html2
    html2, n = re.subn(
        r"(</head>)",
        r"\1\n<!-- teachany-hero-notext -->\n",
        html,
        count=1,
        flags=re.I,
    )
    if n:
        return html2
    return "<!-- teachany-hero-notext -->\n" + html


def apply_labels(d: Path, title: str) -> list[str]:
    path = d / "index.html"
    if not path.exists():
        return ["no-html"]
    html = path.read_text(encoding="utf-8", errors="ignore")
    html = ensure_label_css(html)
    html = insert_or_replace_hero(html, d.name, title)
    html = mark_notext(html)
    path.write_text(html, encoding="utf-8")
    return ["labels"]


def gen_hero_openrouter(cid: str, title: str, subject: str, out: Path) -> tuple[bool, str]:
    """OpenRouter Gemini Flash Image — ~10s/张，无字 prompt。"""
    import base64

    import requests

    key = os.environ.get("OPENROUTER_IMAGE_API_KEY") or os.environ.get("OPENROUTER_API_KEY")
    if not key:
        return False, "missing OPENROUTER_API_KEY"
    model = os.environ.get("HERO_OR_MODEL", "google/gemini-3.1-flash-image-preview")
    prompt = hero_prompt(cid, title, subject)
    try:
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://www.teachany.cn",
                "X-Title": "TeachAny Hero NoText",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "modalities": ["image", "text"],
            },
            timeout=float(os.environ.get("HERO_GEN_TIMEOUT", "120")),
        )
    except Exception as e:
        return False, f"request:{e}"
    if resp.status_code == 429:
        return False, "429 rate limit"
    if resp.status_code != 200:
        return False, f"HTTP {resp.status_code}: {resp.text[:180]}"
    try:
        data = resp.json()
        msg = (data.get("choices") or [{}])[0].get("message") or {}
        images = msg.get("images") or []
        raw = None
        for im in images:
            url = ((im.get("image_url") or {}) if isinstance(im, dict) else {}).get("url") or ""
            if "base64," in url:
                raw = base64.b64decode(url.split("base64,", 1)[1])
                break
        if not raw:
            return False, "no image in response"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(raw)
        return True, f"openrouter {len(raw)}B"
    except Exception as e:
        return False, f"decode:{e}"


def gen_hero_agnes(cid: str, title: str, subject: str, out: Path, *, slot_id: str) -> tuple[bool, str]:
    prompt = hero_prompt(cid, title, subject)
    cmd = [
        sys.executable,
        str(AGNES),
        "--course-id",
        slot_id,
        "--slot",
        "hero",
        "--size",
        "1280x768",
        "--prompt",
        prompt,
        "--out",
        str(out),
    ]
    timeout_s = float(os.environ.get("HERO_GEN_TIMEOUT", "100"))
    try:
        r = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_s,
            cwd=str(ROOT),
            start_new_session=True,
        )
        ok = out.exists() and out.stat().st_size > 20000
        msg = (r.stdout or "")[-300:] + (r.stderr or "")[-120:]
        return ok, msg
    except subprocess.TimeoutExpired as e:
        try:
            import signal

            if e.pid:
                os.killpg(e.pid, signal.SIGKILL)
        except Exception:
            pass
        return False, f"timeout>{timeout_s}s"
    except Exception as e:
        return False, str(e)


def gen_hero(cid: str, title: str, subject: str, out: Path, *, slot_id: str) -> tuple[bool, str]:
    backend = os.environ.get("HERO_BACKEND", "agnes").strip().lower()
    if backend in ("openrouter", "or"):
        return gen_hero_openrouter(cid, title, subject, out)
    return gen_hero_agnes(cid, title, subject, out, slot_id=slot_id)


def iter_courses(only: list[str] | None = None) -> list[Path]:
    if only:
        return [COMMUNITY / c for c in only if (COMMUNITY / c).is_dir()]
    out = []
    for d in sorted(COMMUNITY.iterdir()):
        if not d.is_dir() or d.name.startswith(".") or d.name in ("drafts", "pending", "archive"):
            continue
        if (d / "index.html").exists():
            out.append(d)
    return out


def ocr_level(scan, path: Path | None) -> str:
    if not path:
        return "missing"
    try:
        text = scan.ocr_image(path)
        level, _ = scan.classify(text)
        return level
    except Exception:
        return "error"


def cmd_scan(args) -> int:
    scan = load_scan()
    courses = iter_courses(args.cid)
    if args.limit:
        courses = courses[: args.limit]
    print(f"OCR scan {len(courses)} courses…")
    rows = []
    t0 = time.time()

    def one(d: Path):
        h = pick_hero(d)
        level = ocr_level(scan, h)
        return {
            "id": d.name,
            "hero": str(h.relative_to(ROOT)) if h else None,
            "level": level,
            "marked": "teachany-hero-notext" in (d / "index.html").read_text(encoding="utf-8", errors="ignore")
            if (d / "index.html").exists()
            else False,
        }

    # sequential OCR (tesseract not great in many processes on mac sometimes)
    for i, d in enumerate(courses, 1):
        rows.append(one(d))
        if i % 50 == 0:
            print(f"  {i}/{len(courses)} {time.time()-t0:.0f}s", flush=True)

    from collections import Counter

    stats = Counter(r["level"] for r in rows)
    flagged = [r for r in rows if r["level"] in ("cjk", "eng", "noise", "missing", "error")]
    report = {
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "total": len(rows),
        "stats": dict(stats),
        "flagged_count": len(flagged),
        "flagged": flagged,
        "items": rows,
    }
    REPORTS.mkdir(exist_ok=True)
    out = REPORTS / "hero-text-ocr-audit.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"stats={dict(stats)} flagged={len(flagged)}")
    print(f"→ {out}")
    return 0


def needs_replace(d: Path, scan, state: dict, *, force: bool, skip_clean: bool) -> tuple[bool, str]:
    html_path = d / "index.html"
    html = html_path.read_text(encoding="utf-8", errors="ignore") if html_path.exists() else ""
    out = d / "assets" / f"{d.name}-hero.png"
    marked = "teachany-hero-notext" in html
    has_new = out.exists() and out.stat().st_size > 40000
    if not force:
        if marked and has_new:
            return False, "already-done" if d.name in (state.get("done") or []) else "marked"
    # 默认不跑 OCR（太慢）；仅 --ocr-gate 才用 clean 跳过
    if not force and skip_clean and scan is not None and os.environ.get("HERO_OCR_GATE") == "1":
        level = ocr_level(scan, pick_hero(d))
        if level == "clean" and re.search(r'<span[^>]*class=["\'][^"\']*ta-fig-tag', html):
            return False, "ocr-clean"
    return True, "replace"


def process_one(
    d: Path,
    *,
    force: bool,
    skip_clean: bool,
    labels_only: bool,
    sleep_s: float,
    state: dict,
    scan=None,
) -> dict:
    cid = d.name
    mf = load_manifest(d)
    title = course_title(d, mf)
    subject = str(mf.get("subject") or "").lower()
    actions = []

    if labels_only:
        actions += apply_labels(d, title)
        return {"id": cid, "ok": True, "actions": actions, "title": title}

    need, reason = needs_replace(d, scan, state, force=force, skip_clean=skip_clean)
    if not need:
        return {"id": cid, "ok": True, "actions": [f"skip:{reason}"], "title": title}

    assets = d / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    out = assets / f"{cid}-hero.png"
    # backup old
    old = pick_hero(d)
    if old and old.resolve() != out.resolve() and old.exists():
        bak = assets / f"{old.stem}.pre-notext{old.suffix}"
        if not bak.exists():
            try:
                bak.write_bytes(old.read_bytes())
            except Exception:
                pass

    slots = [s.strip() for s in os.environ.get("HERO_NTV_SLOTS", "ntv1,ntv2,ntv3").split(",") if s.strip()]
    ok, msg, slot_id = False, "", ""
    for tag in slots:
        slot_id = f"{cid}-{tag}"
        ok, msg = gen_hero(cid, title, subject, out, slot_id=slot_id)
        if ok:
            break
    if not ok:
        return {"id": cid, "ok": False, "actions": ["gen-fail"], "detail": msg[-200:], "title": title}
    actions.append("gen")
    actions += apply_labels(d, title)
    # also update common hero refs in html to new file
    html_path = d / "index.html"
    html = html_path.read_text(encoding="utf-8", errors="ignore")
    html = re.sub(
        r'(src=["\'])(?:\./)?assets/[^"\']*hero[^"\']*(webp|png|jpg|jpeg)(["\'])',
        rf"\1./assets/{cid}-hero.png\3",
        html,
        count=3,
        flags=re.I,
    )
    html_path.write_text(html, encoding="utf-8")
    if sleep_s > 0:
        time.sleep(sleep_s)
    return {"id": cid, "ok": True, "actions": actions, "title": title, "slot": slot_id}


def cmd_replace(args) -> int:
    state = load_state()
    # OCR 仅扫描模式需要；替换默认不加载（避免每课 OCR 卡死）
    scan = None
    if args.labels_only:
        scan = None
    elif os.environ.get("HERO_OCR_GATE") == "1":
        scan = load_scan()
    courses = iter_courses(args.cid)
    if getattr(args, "reverse", False) or os.environ.get("HERO_REPLACE_REVERSE") == "1":
        courses = list(reversed(courses))
    if not args.force and not args.labels_only:
        # prefer flagged from prior audit if present
        audit = REPORTS / "hero-text-ocr-audit.json"
        if audit.exists() and not args.cid:
            data = json.loads(audit.read_text(encoding="utf-8"))
            flagged_ids = {r["id"] for r in data.get("flagged") or []}
            if flagged_ids:
                courses = [
                    d
                    for d in courses
                    if d.name in flagged_ids
                    or "teachany-hero-notext"
                    not in (d / "index.html").read_text(encoding="utf-8", errors="ignore")
                ]
    # also always include unmarked
    if args.limit:
        courses = courses[: args.limit]

    print(
        f"replace candidates={len(courses)} labels_only={args.labels_only} "
        f"force={args.force} reverse={getattr(args, 'reverse', False)}",
        flush=True,
    )
    results = []
    ok_n = fail_n = 0
    for i, d in enumerate(courses, 1):
        # 多 worker：每次读最新 state，避免重复生图
        state = load_state()
        print(f"[{i}/{len(courses)}] … {d.name}", flush=True)
        r = process_one(
            d,
            force=args.force,
            skip_clean=not args.force,
            labels_only=args.labels_only,
            sleep_s=args.sleep,
            state=state,
            scan=scan,
        )
        results.append(r)
        state = load_state()
        if r["ok"]:
            ok_n += 1
            # labels-only 不计入 done（done = 已无字生图）
            if "gen" in r.get("actions", []):
                state.setdefault("done", [])
                if d.name not in state["done"]:
                    state["done"].append(d.name)
        else:
            fail_n += 1
            state.setdefault("failed", []).append({"id": d.name, "detail": r.get("detail", "")[:200]})
        print(f"[{i}/{len(courses)}] {'OK' if r['ok'] else 'FAIL'} {r['id']} {r.get('actions')} {r.get('title','')[:20]}", flush=True)
        save_state(state)

    save_state(state)
    REPORTS.mkdir(exist_ok=True)
    (REPORTS / "hero-notext-replace.json").write_text(
        json.dumps(
            {
                "at": datetime.now(timezone.utc).isoformat(),
                "ok": ok_n,
                "fail": fail_n,
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"DONE ok={ok_n} fail={fail_n} done_total={len(state.get('done') or [])}")
    return 1 if fail_n else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan-only", action="store_true")
    ap.add_argument("--labels-only", action="store_true")
    ap.add_argument("--all", action="store_true", help="处理全部（配合 --limit 0）")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--cid", action="append", default=[])
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--sleep", type=float, default=7.0, help="每课生图后休眠秒数（限流）")
    ap.add_argument("--reverse", action="store_true", help="从目录末尾向前处理（便于双 worker 并行）")
    ap.add_argument("--retry-failed", action="store_true", help="仅重试 state.failed 中的课程")
    args = ap.parse_args()
    if args.retry_failed and not args.cid:
        state = load_state()
        ids = []
        for f in state.get("failed") or []:
            cid = f.get("id") if isinstance(f, dict) else str(f)
            if cid and cid not in ids:
                ids.append(cid)
        args.cid = ids
        # 清 failed，避免重复堆积；成功会进 done
        state["failed"] = []
        save_state(state)
        print(f"retry-failed queue={len(ids)}", flush=True)
        if not ids:
            print("no failed ids")
            return 0
    if args.all and not args.cid:
        args.limit = 0  # 0 means no truncate in our code — fix
    if args.cid and args.limit == 20:
        # 显式传了 --cid 时默认不截断（避免只跑前 20）
        args.limit = 0
    # interpret limit 0 as no limit
    if args.limit == 0:
        args.limit = 10**9

    if args.scan_only:
        return cmd_scan(args)
    # patch courses order for reverse workers
    if args.reverse:
        # monkey via env consumed in cmd_replace
        os.environ["HERO_REPLACE_REVERSE"] = "1"
    return cmd_replace(args)


if __name__ == "__main__":
    sys.exit(main())
