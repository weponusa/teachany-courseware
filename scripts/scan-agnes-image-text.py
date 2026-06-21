#!/usr/bin/env python3
"""OCR 抽检 Agnes 课件插图是否含乱码/中文/英文文字（应无字，中文由 HTML 叠加）。"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image
import pytesseract

ROOT = Path(__file__).resolve().parents[1]
CJK = re.compile(r"[\u4e00-\u9fff]")
ENG = re.compile(r"[A-Za-z]{4,}")
ENG_STOP = {"http", "https", "that", "this", "with", "from", "your", "image", "png"}


def ocr_image(path: Path) -> str:
    img = Image.open(path)
    w, h = img.size
    if max(w, h) < 900:
        img = img.resize((w * 2, h * 2), Image.Resampling.LANCZOS)
    return pytesseract.image_to_string(img, lang="chi_sim+eng", config="--psm 6").strip()


def classify(text: str) -> tuple[str, str]:
    cjk = "".join(CJK.findall(text))
    if len(cjk) >= 2:
        return "cjk", cjk[:60]
    eng = [w for w in ENG.findall(text) if w.lower() not in ENG_STOP]
    if len(eng) >= 3:
        return "eng", " ".join(eng[:6])
    alnum = re.sub(r"[\s\W_]+", "", text)
    if len(alnum) >= 8:
        return "noise", text.replace("\n", " ")[:80]
    return "clean", ""


def collect_images(course_glob: str) -> list[Path]:
    paths: list[Path] = []
    for base in (ROOT / "community").glob(course_glob):
        assets = base / "assets"
        if not assets.is_dir():
            continue
        for ext in ("*.webp", "*.png"):
            for p in sorted(assets.glob(ext)):
                if re.search(r"-(hero|section1|section2)\.(webp|png)$", p.name):
                    paths.append(p)
    return sorted(paths)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", default="pol-m-*", help="community 子目录 glob，可多次传入")
    ap.add_argument("--also-psych", action="store_true", default=True)
    ap.add_argument("--out", type=Path, help="写出 JSON 报告")
    ap.add_argument("--fail-on-cjk", action="store_true", help="存在 CJK 文字则 exit 1")
    args = ap.parse_args()

    globs = [args.glob]
    if args.also_psych:
        globs.append("psych-m-*")

    images: list[Path] = []
    for g in globs:
        images.extend(collect_images(g))
    images = sorted(set(images))

    rows = []
    stats = {"clean": 0, "noise": 0, "eng": 0, "cjk": 0}
    for p in images:
        rel = str(p.relative_to(ROOT))
        cid = p.parent.parent.name
        slot = p.stem.rsplit("-", 1)[-1] if "-" in p.stem else p.stem
        try:
            text = ocr_image(p)
            level, snippet = classify(text)
        except Exception as e:
            level, snippet = "error", str(e)
        stats[level] = stats.get(level, 0) + 1
        rows.append({"course_id": cid, "file": rel, "slot": slot, "level": level, "snippet": snippet})

    report = {
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "total": len(images),
        "stats": stats,
        "flagged": [r for r in rows if r["level"] in ("cjk", "eng")],
        "items": rows,
    }

    out = args.out or ROOT / "reports" / "pol-psych-agnes-text-audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"扫描 {len(images)} 张：clean={stats.get('clean',0)} cjk={stats.get('cjk',0)} eng={stats.get('eng',0)} noise={stats.get('noise',0)}")
    print(f"报告 → {out}")
    for r in report["flagged"][:12]:
        print(f"  [{r['level']}] {r['file']} → {r['snippet']}")
    if len(report["flagged"]) > 12:
        print(f"  … 另有 {len(report['flagged']) - 12} 张")

    if args.fail_on_cjk and stats.get("cjk", 0) > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
