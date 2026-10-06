#!/usr/bin/env python3
"""中国课标课件 Hero 图质检 + Agnes 首选重生成。

首选模型：agnes-image-2.1-flash（经 https://www.teachany.cn/api/images/agnes 中转，无需用户 Key）

策略（避免 Agnes 中文乱码）：
  - 生图用英文场景描述 + 严格无文字（与 agnes-image-gen.py 一致）
  - 中文标注由 HTML figcaption / alt 承担（课件内）
  - Gallery 缩图用高质量无字知识结构图（课件外）

用法：
  python3 scripts/batch-cn-hero-agnes.py audit
  python3 scripts/batch-cn-hero-agnes.py regen --limit 20
  python3 scripts/batch-cn-hero-agnes.py regen --subject chinese --dry-run
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
REPORTS = ROOT / "reports"
AGNES = ROOT / "scripts" / "agnes-image-gen.py"
PROGRESS = ROOT / "scripts" / "cn-hero-agnes-progress.json"
MIN_GOOD = 50 * 1024
MIN_BYTES = 20 * 1024
DELAY_SEC = 8

SUBJECT_CN = {
    "math": "数学", "chinese": "语文", "english": "英语", "biology": "生物",
    "physics": "物理", "chemistry": "化学", "history": "历史", "geography": "地理",
    "science": "科学", "politics": "道德与法治", "psychology": "心理健康",
}

SUBJECT_PALETTE = {
    "chinese": "warm crimson gold classical Chinese literature palette",
    "math": "cool blue indigo geometric education palette",
    "history": "sepia amber historical map palette",
    "geography": "teal green earth science palette",
    "biology": "green organic life science palette",
    "chemistry": "purple cyan lab science palette",
    "physics": "navy electric orange physics palette",
    "english": "sky blue international language palette",
    "science": "bright green discovery science palette",
    "politics": "warm orange civic education palette",
    "psychology": "soft teal mental health palette",
}


def load_loop():
    spec = importlib.util.spec_from_file_location("loop", ROOT / "scripts/courseware-quality-loop.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_manifest(d: Path) -> dict:
    mf = d / "manifest.json"
    if mf.is_file():
        try:
            return json.loads(mf.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def is_placeholder_svg(path: Path) -> bool:
    if not path.is_file() or path.suffix.lower() != ".svg":
        return False
    txt = path.read_text(encoding="utf-8", errors="replace")
    if "TeachAny · 课标互动课件" in txt:
        return True
    if len(txt) < 8000:
        return True
    return False


def hero_quality(d: Path) -> str:
    """good | placeholder | low | missing"""
    assets = d / "assets"
    if not assets.is_dir():
        return "missing"
    webp = assets / "hero-infographic.webp"
    png = assets / "hero-infographic.png"
    if webp.is_file() and webp.stat().st_size >= MIN_GOOD:
        return "good"
    if png.is_file() and png.stat().st_size >= MIN_GOOD:
        return "good"
    for p in assets.iterdir():
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".webp", ".png", ".jpg", ".jpeg"}:
            continue
        if p.stat().st_size < 80 * 1024:
            continue
        n = p.name.lower()
        if any(k in n for k in ("hero", "cover", "infographic", "panorama")) and "map" not in n:
            return "good"
    svg = assets / "hero-infographic.svg"
    if svg.is_file() and is_placeholder_svg(svg):
        return "placeholder"
    if webp.is_file() or png.is_file():
        return "low"
    return "missing"


def extract_topics(d: Path) -> list[str]:
    html_path = d / "index.html"
    if not html_path.is_file():
        return []
    html = html_path.read_text(encoding="utf-8", errors="replace")[:15000]
    headings = re.findall(r"<h[234][^>]*>(.*?)</h[234]>", html, re.I)
    out = []
    for h in headings:
        t = re.sub(r"<[^>]+>", "", h).strip()
        if 2 <= len(t) <= 24 and t not in out:
            out.append(t)
    return out[:6]


def build_agnes_hero_prompt(d: Path) -> str:
    mf = load_manifest(d)
    title = mf.get("name") or d.name
    subj = str(mf.get("subject") or "").lower()
    subj_cn = SUBJECT_CN.get(subj, subj)
    grade = mf.get("grade", "")
    palette = SUBJECT_PALETTE.get(subj, "soft pastel educational infographic palette")
    topics = extract_topics(d)
    topic_hint = ", ".join(topics[:4]) if topics else title
    return (
        f"Chinese K-12 {subj_cn} course knowledge structure infographic for topic: {title}. "
        f"Grade {grade}. Central hub with six pastel colored module cards radiating outward, "
        f"each card with a distinct icon representing: {topic_hint}. "
        f"Clean white background, {palette}, professional educational poster, "
        f"information-dense layout, museum quality, landscape 16:9. "
        f"No blackboards, no clip art stickers."
    )


def pick_agnes_course_id(course_id: str) -> str:
    """每课件 3 张额度；用尽时尝试 -v2 桶。"""
    for cid in (course_id, f"{course_id}-v2", f"{course_id}-v3"):
        try:
            out = subprocess.run(
                [sys.executable, str(AGNES), "--course-id", cid, "--quota"],
                capture_output=True, text=True, timeout=30,
            )
            data = json.loads(out.stdout)
            rem = data.get("course", {}).get("remaining", 0)
            if data.get("course", {}).get("ok") and rem > 0:
                return cid
        except Exception:
            continue
    return course_id


def png_to_webp(png: Path, webp: Path) -> bool:
    try:
        from PIL import Image
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "-q"])
        from PIL import Image
    img = Image.open(png)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    webp.parent.mkdir(parents=True, exist_ok=True)
    img.save(webp, "WEBP", quality=88, method=6)
    return webp.stat().st_size >= MIN_BYTES


def rewrite_hero_html(d: Path, mf: dict) -> bool:
    html_path = d / "index.html"
    if not html_path.is_file():
        return False
    html = html_path.read_text(encoding="utf-8", errors="replace")
    orig = html
    title = mf.get("name") or d.name
    topics = extract_topics(d)
    cap = f"{title} · 知识结构主图"
    if topics:
        cap += "：" + "、".join(topics[:3])

    for old in ("hero-infographic.svg", "hero-infographic.png", "hero-infographic.jpg"):
        html = html.replace(f"./assets/{old}", "./assets/hero-infographic.webp")
        html = html.replace(f"assets/{old}", "assets/hero-infographic.webp")

    if 'class="hero-cover-img"' in html:
        html = re.sub(
            r'(<img[^>]*class="hero-cover-img"[^>]*alt=")[^"]*(")',
            rf'\1{title}知识结构图\2',
            html,
            count=1,
        )

    if "<figcaption>" in html and "hero-infographic" in html:
        html = re.sub(
            r'(<figure[^>]*class="[^"]*ta-standard-figure[^"]*"[^>]*>.*?<figcaption>)(.*?)(</figcaption>)',
            lambda m: m.group(1) + cap + m.group(3) if "hero" in m.group(0).lower() or "知识结构" in m.group(0) else m.group(0),
            html,
            count=1,
            flags=re.S,
        )

    if html != orig:
        html_path.write_text(html, encoding="utf-8")
        return True
    return False


def update_manifest_hero(d: Path) -> None:
    mf_path = d / "manifest.json"
    if not mf_path.is_file():
        return
    try:
        data = json.loads(mf_path.read_text(encoding="utf-8"))
    except Exception:
        return
    hero = "assets/hero-infographic.webp"
    if not (d / hero).is_file():
        hero = "assets/hero-infographic.png"
    meta = data.setdefault("assets", {})
    if isinstance(meta, dict):
        meta["hero"] = hero
        imgs = list(meta.get("images") or [])
        if hero not in imgs:
            imgs.insert(0, hero)
        meta["images"] = imgs
    data["has_images"] = True
    data["has_hero"] = True
    mf_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def regen_one(d: Path, *, dry_run: bool = False) -> bool:
    cid = d.name
    if dry_run:
        print(f"  [dry-run] {cid}: {build_agnes_hero_prompt(d)[:100]}…")
        return True

    agnes_id = pick_agnes_course_id(cid)
    assets = d / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    png_out = assets / "hero-infographic.png"
    webp_out = assets / "hero-infographic.webp"
    prompt = build_agnes_hero_prompt(d)

    cmd = [
        sys.executable, str(AGNES),
        "--course-id", agnes_id,
        "--prompt", prompt,
        "--out", str(png_out),
        "--slot", "hero",
        "--size", "1280x768",
    ]
    print(f"  📸 Agnes · {cid} (bucket={agnes_id})")
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if r.returncode != 0:
        print(f"  ❌ {r.stdout}\n{r.stderr}")
        return False

    if not png_out.is_file() or png_out.stat().st_size < MIN_BYTES:
        print(f"  ❌ 输出无效")
        return False

    if not png_to_webp(png_out, webp_out):
        print(f"  ⚠️ WebP 转换失败，保留 PNG")
        webp_out = png_out

    mf = load_manifest(d)
    rewrite_hero_html(d, mf)
    update_manifest_hero(d)
    print(f"  ✅ {webp_out.name} ({webp_out.stat().st_size // 1024} KB)")
    return True


def iter_cn_courses(loop, subject: str | None = None, only: list[str] | None = None):
    for d in sorted(COMMUNITY.iterdir()):
        if not d.is_dir() or d.name.startswith("_"):
            continue
        if only and d.name not in only:
            continue
        mf = loop.load_manifest(d)
        if not loop.is_cn_course(d, mf):
            continue
        if subject and str(mf.get("subject") or "").lower() != subject.lower():
            continue
        yield d, mf


def cmd_audit(args) -> int:
    loop = load_loop()
    rows = []
    from collections import Counter
    c = Counter()
    for d, mf in iter_cn_courses(loop, args.subject, args.only):
        q = hero_quality(d)
        c[q] += 1
        if q != "good" or args.all:
            rows.append({
                "course_id": d.name,
                "name": mf.get("name", ""),
                "subject": mf.get("subject", ""),
                "quality": q,
            })
    report = {
        "audited_at": datetime.now(timezone.utc).isoformat(),
        "model_preferred": "agnes-image-2.1-flash",
        "total_cn": sum(c.values()),
        "quality_counts": dict(c),
        "needs_regen": c.get("placeholder", 0) + c.get("low", 0) + c.get("missing", 0),
        "courses": rows,
    }
    out = Path(args.out) if args.out else REPORTS / "cn-hero-agnes-audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"课标课 {report['total_cn']} · good {c.get('good',0)} · "
          f"待重生 {report['needs_regen']} (placeholder {c.get('placeholder',0)}, "
          f"low {c.get('low',0)}, missing {c.get('missing',0)})")
    print(f"报告 → {out}")
    return 0


def cmd_regen(args) -> int:
    if not AGNES.is_file():
        print(f"❌ 未找到 {AGNES}", file=sys.stderr)
        return 2
    loop = load_loop()
    progress = json.loads(PROGRESS.read_text()) if PROGRESS.is_file() else {"done": [], "failed": []}
    done_set = set(progress.get("done", []))

    targets = []
    for d, _ in iter_cn_courses(loop, args.subject, args.only):
        if d.name in done_set and not args.force:
            continue
        q = hero_quality(d)
        if q in ("placeholder", "low", "missing"):
            targets.append(d)

    if args.limit:
        targets = targets[: args.limit]

    print(f"Agnes Hero 重生成 · 待处理 {len(targets)} 门（首选 agnes-image-2.1-flash）")
    ok = fail = 0
    for i, d in enumerate(targets, 1):
        print(f"\n[{i}/{len(targets)}] {d.name}")
        try:
            if regen_one(d, dry_run=args.dry_run):
                ok += 1
                if not args.dry_run:
                    progress.setdefault("done", []).append(d.name)
            else:
                fail += 1
                progress.setdefault("failed", []).append(d.name)
        except Exception as e:
            print(f"  ❌ {e}")
            fail += 1
            progress.setdefault("failed", []).append(d.name)
        if not args.dry_run:
            PROGRESS.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if i < len(targets):
            time.sleep(args.delay)

    print(f"\n完成：成功 {ok}，失败 {fail}")
    if ok and not args.dry_run and not args.no_rebuild:
        print("重建 registry…")
        subprocess.run([sys.executable, str(ROOT / "scripts/rebuild-index.py")], check=False)
    return 0 if fail == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="中国课标 Hero 质检 + Agnes 重生成")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("audit", help="扫描低质量 Hero")
    a.add_argument("--subject")
    a.add_argument("--only", nargs="*")
    a.add_argument("--all", action="store_true", help="列出全部（含 good）")
    a.add_argument("--out", default="")
    a.set_defaults(func=cmd_audit)

    r = sub.add_parser("regen", help="Agnes 重生成占位 Hero")
    r.add_argument("--limit", type=int, default=0)
    r.add_argument("--subject")
    r.add_argument("--only", nargs="*")
    r.add_argument("--delay", type=int, default=DELAY_SEC)
    r.add_argument("--dry-run", action="store_true")
    r.add_argument("--force", action="store_true", help="忽略 progress 已完成的")
    r.add_argument("--no-rebuild", action="store_true")
    r.set_defaults(func=cmd_regen)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
