#!/usr/bin/env python3
"""批量将课件占位 SVG 插图替换为高质量 WebP（Gallery 缩图 + 课内插图）。

首选生图：Agnes（agnes-image-2.1-flash）→ 见 scripts/batch-cn-hero-agnes.py
本脚本 sync 阶段：已有 PNG/JPG 转 WebP；gen 阶段为 OpenRouter 备用（非首选）。

用法：
  python3 scripts/batch-cn-hero-agnes.py audit      # Hero 质检（推荐）
  python3 scripts/batch-cn-hero-agnes.py regen      # Agnes 重生成占位 Hero
  python3 scripts/batch-courseware-webp.py sync       # 栅格图转 WebP
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import time
from io import BytesIO
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
PROGRESS = ROOT / "scripts" / "webp-gen-progress.json"
MIN_BYTES = 20 * 1024
SLOTS = (
    ("hero-infographic", "知识结构全景图", "knowledge panorama infographic with 6 pastel cards"),
    ("concept-diagram", "核心概念关系图", "concept relationship diagram with labeled nodes"),
    ("process-diagram", "过程机制流程图", "step-by-step process flow diagram"),
)

API_KEY = os.environ.get(
    "OPENROUTER_FREE_API_KEY",
    os.environ.get("OPENROUTER_API_KEY", ""),
)
MODEL = os.environ.get("OPENROUTER_IMAGE_MODEL", "google/gemini-2.5-flash-image")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

SUBJECT_CN = {
    "math": "数学", "chinese": "语文", "english": "英语", "biology": "生物",
    "physics": "物理", "chemistry": "化学", "history": "历史", "geography": "地理",
    "science": "科学", "politics": "道德与法治", "psychology": "心理健康",
}


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
    if len(txt) < 6000 and ("linearGradient" in txt or "stop-color=\"#eff6ff\"" in txt):
        return True
    if len(txt) < 8000 and path.name in {
        "hero-infographic.svg", "concept-diagram.svg", "process-diagram.svg",
    }:
        return True
    return False


def best_raster(assets: Path, stem: str) -> Path | None:
    for ext in (".webp", ".png", ".jpg", ".jpeg"):
        p = assets / f"{stem}{ext}"
        if p.is_file() and p.stat().st_size >= MIN_BYTES:
            return p
    return None


def find_slot_raster(assets: Path, stem: str) -> Path | None:
    direct = best_raster(assets, stem)
    if direct:
        return direct
    keywords = {
        "hero-infographic": ("hero", "cover", "infographic", "panorama", "title"),
        "concept-diagram": ("concept", "diagram", "structure", "mind"),
        "process-diagram": ("process", "flow", "timeline", "step", "procedure"),
    }.get(stem, (stem.split("-")[0],))
    cands: list[Path] = []
    for p in assets.iterdir():
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".webp", ".png", ".jpg", ".jpeg"}:
            continue
        if p.stat().st_size < MIN_BYTES:
            continue
        low = p.name.lower()
        if any(k in low for k in keywords):
            cands.append(p)
    if cands:
        return max(cands, key=lambda x: x.stat().st_size)
    if stem == "hero-infographic":
        imgs = [
            p for p in assets.iterdir()
            if p.is_file() and p.suffix.lower() in {".webp", ".png", ".jpg", ".jpeg"}
            and p.stat().st_size >= MIN_BYTES and "map" not in p.name.lower()
        ]
        if imgs:
            return max(imgs, key=lambda x: x.stat().st_size)
    return None


def needs_work(d: Path) -> bool:
    assets = d / "assets"
    if not assets.is_dir():
        return False
    for stem, _, _ in SLOTS:
        webp = assets / f"{stem}.webp"
        if webp.is_file() and webp.stat().st_size >= MIN_BYTES:
            continue
        svg = assets / f"{stem}.svg"
        raster = find_slot_raster(assets, stem)
        if raster or (svg.is_file() and is_placeholder_svg(svg)):
            return True
    return False


def png_to_webp(src: Path, dst: Path, quality: int = 88) -> bool:
    try:
        from PIL import Image
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "-q"])
        from PIL import Image
    img = Image.open(src)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    dst.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst, "WEBP", quality=quality, method=6)
    return dst.stat().st_size >= MIN_BYTES


def save_b64_as_webp(b64_data: str, dst: Path, quality: int = 88) -> bool:
    try:
        from PIL import Image
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "-q"])
        from PIL import Image
    raw = base64.b64decode(b64_data)
    img = Image.open(BytesIO(raw))
    if img.mode in ("RGBA", "P"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        bg.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
        img = bg
    elif img.mode != "RGB":
        img = img.convert("RGB")
    dst.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst, "WEBP", quality=quality, method=6)
    return dst.stat().st_size >= MIN_BYTES


def rewrite_html_images(d: Path) -> int:
    html_path = d / "index.html"
    if not html_path.is_file():
        return 0
    html = html_path.read_text(encoding="utf-8", errors="replace")
    orig = html
    assets = d / "assets"
    for stem, _, _ in SLOTS:
        webp = assets / f"{stem}.webp"
        if not (webp.is_file() and webp.stat().st_size >= MIN_BYTES):
            continue
        for old in (f"{stem}.svg", f"{stem}.png", f"{stem}.jpg", f"{stem}.jpeg"):
            html = html.replace(f"./assets/{old}", f"./assets/{stem}.webp")
            html = html.replace(f"assets/{old}", f"assets/{stem}.webp")
    if html != orig:
        html_path.write_text(html, encoding="utf-8")
        return 1
    return 0


def update_manifest_assets(d: Path) -> None:
    mf = d / "manifest.json"
    if not mf.is_file():
        return
    try:
        data = json.loads(mf.read_text(encoding="utf-8"))
    except Exception:
        return
    assets_dir = d / "assets"
    images: list[str] = []
    hero = ""
    for stem, _, _ in SLOTS:
        webp = assets_dir / f"{stem}.webp"
        if webp.is_file() and webp.stat().st_size >= MIN_BYTES:
            rel = f"assets/{stem}.webp"
            images.append(rel)
            if stem == "hero-infographic":
                hero = rel
    if not images:
        return
    meta = data.setdefault("assets", {})
    if isinstance(meta, dict):
        meta["hero"] = hero or meta.get("hero", "")
        meta["images"] = images
    data["has_images"] = True
    data["has_hero"] = bool(hero)
    mf.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_prompt(d: Path, stem: str, label: str, style_hint: str) -> str:
    mf = load_manifest(d)
    title = mf.get("name") or d.name
    subj = SUBJECT_CN.get(str(mf.get("subject", "")).lower(), mf.get("subject", ""))
    grade = mf.get("grade", "")
    html = (d / "index.html").read_text(encoding="utf-8", errors="replace")[:12000]
    headings = re.findall(r"<h[234][^>]*>(.*?)</h[234]>", html, re.I)[:8]
    headings = [re.sub(r"<[^>]+>", "", h).strip() for h in headings if h.strip()]
    topics = " | ".join(headings[:6]) or title
    return (
        f"Generate a professional Chinese K-12 educational illustration: {label} for 「{title}」 "
        f"({subj}, grade {grade}). Style: {style_hint}. "
        f"Layout: clean white background, soft pastel blocks, readable Simplified Chinese labels. "
        f"Key topics to visualize: {topics}. "
        f"Dense educational infographic, NOT generic clip art. All text in Simplified Chinese."
    )


def generate_webp(prompt: str, dst: Path, retries: int = 3) -> bool:
    if not API_KEY:
        print("    ❌ 未设置 OPENROUTER_FREE_API_KEY / OPENROUTER_API_KEY", file=sys.stderr)
        return False
    for attempt in range(1, retries + 1):
        try:
            resp = requests.post(
                API_URL,
                headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "modalities": ["image", "text"],
                },
                timeout=180,
            )
            if resp.status_code == 429:
                time.sleep(15 * attempt)
                continue
            if resp.status_code != 200:
                print(f"    ❌ HTTP {resp.status_code}: {resp.text[:120]}")
                time.sleep(10 * attempt)
                continue
            msg = resp.json().get("choices", [{}])[0].get("message", {})
            images = msg.get("images") or []
            if not images:
                time.sleep(10 * attempt)
                continue
            url = images[0].get("image_url", {}).get("url", "")
            if not url.startswith("data:"):
                continue
            b64 = url.split(",", 1)[1]
            if save_b64_as_webp(b64, dst):
                print(f"    ✅ {dst.name} ({dst.stat().st_size // 1024} KB)")
                return True
        except Exception as e:
            print(f"    ⚠️ {e}")
            time.sleep(10 * attempt)
    return False


def sync_course(d: Path, *, dry_run: bool = False) -> list[str]:
    assets = d / "assets"
    if not assets.is_dir():
        return []
    done: list[str] = []
    for stem, _, _ in SLOTS:
        dst = assets / f"{stem}.webp"
        if dst.is_file() and dst.stat().st_size >= MIN_BYTES:
            continue
        src = find_slot_raster(assets, stem)
        if not src:
            continue
        if dry_run:
            done.append(f"would_convert:{stem}")
            continue
        if png_to_webp(src, dst):
            done.append(f"converted:{stem}")
    if done and not dry_run:
        rewrite_html_images(d)
        update_manifest_assets(d)
    return done


def gen_course(d: Path, *, dry_run: bool = False, delay: int = 8) -> list[str]:
    assets = d / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    done: list[str] = []
    for stem, label, hint in SLOTS:
        dst = assets / f"{stem}.webp"
        if dst.is_file() and dst.stat().st_size >= MIN_BYTES:
            continue
        if find_slot_raster(assets, stem):
            continue
        svg = assets / f"{stem}.svg"
        if svg.is_file() and not is_placeholder_svg(svg):
            continue
        if dry_run:
            done.append(f"would_gen:{stem}")
            continue
        prompt = build_prompt(d, stem, label, hint)
        print(f"    📸 生成 {stem}.webp …")
        if generate_webp(prompt, dst):
            done.append(f"generated:{stem}")
            time.sleep(delay)
    if done and not dry_run:
        rewrite_html_images(d)
        update_manifest_assets(d)
    return done


def iter_targets(limit: int, subject: str | None, only: list[str] | None) -> list[Path]:
    dirs = sorted(p for p in COMMUNITY.iterdir() if p.is_dir() and not p.name.startswith("_"))
    if only:
        dirs = [p for p in dirs if p.name in only]
    if subject:
        dirs = [p for p in dirs if load_manifest(p).get("subject") == subject]
    dirs = [p for p in dirs if needs_work(p)]
    return dirs[:limit] if limit else dirs


def load_progress() -> dict:
    if PROGRESS.is_file():
        return json.loads(PROGRESS.read_text(encoding="utf-8"))
    return {"synced": [], "generated": [], "failed": []}


def save_progress(p: dict) -> None:
    PROGRESS.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def cmd_sync(args) -> int:
    targets = iter_targets(args.limit, args.subject, args.only)
    print(f"sync WebP：{len(targets)} 门")
    ok = 0
    for i, d in enumerate(targets, 1):
        actions = sync_course(d, dry_run=args.dry_run)
        if actions:
            ok += 1
            print(f"  [{i}] {d.name}: {', '.join(actions)}")
    print(f"完成 sync {ok}/{len(targets)}")
    return 0


def cmd_gen(args) -> int:
    progress = load_progress()
    done_set = set(progress.get("generated", []))
    targets = [p for p in iter_targets(args.limit, args.subject, args.only) if p.name not in done_set]
    print(f"AI 生图 WebP：{len(targets)} 门（model={MODEL}）")
    ok = fail = 0
    for i, d in enumerate(targets, 1):
        print(f"\n[{i}/{len(targets)}] {d.name}")
        actions = gen_course(d, dry_run=args.dry_run, delay=args.delay)
        if actions:
            ok += 1
            progress.setdefault("generated", []).append(d.name)
        else:
            fail += 1
            progress.setdefault("failed", []).append(d.name)
        if not args.dry_run:
            save_progress(progress)
    print(f"\n完成 gen {ok} 成功，{fail} 跳过/失败")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in (("sync", cmd_sync), ("gen", cmd_gen)):
        p = sub.add_parser(name)
        p.add_argument("--limit", type=int, default=0)
        p.add_argument("--subject")
        p.add_argument("--only", nargs="*")
        p.add_argument("--dry-run", action="store_true")
        if name == "gen":
            p.add_argument("--delay", type=int, default=8)
        p.set_defaults(func=fn)
    allp = sub.add_parser("all")
    allp.add_argument("--limit", type=int, default=0)
    allp.add_argument("--subject")
    allp.add_argument("--only", nargs="*")
    allp.add_argument("--dry-run", action="store_true")
    allp.add_argument("--delay", type=int, default=8)

    def cmd_all(args):
        cmd_sync(args)
        return cmd_gen(args)

    allp.set_defaults(func=cmd_all)
    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
