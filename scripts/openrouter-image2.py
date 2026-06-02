#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OpenRouter Image2（google/gemini-3.1-flash-image-preview）单张/批量生图。

API Key 仅从环境变量读取，禁止写入仓库：
  export OPENROUTER_API_KEY='sk-or-v1-...'

用法:
  python3 scripts/openrouter-image2.py --prompt "..." --out assets/foo.png
  python3 scripts/openrouter-image2.py --course chn-h-red-chamber --preset red-chamber-3
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "google/gemini-3.1-flash-image-preview"

PRESETS = {
    "red-chamber-3": [
        (
            "illustration-daiyu-burying-flowers.png",
            """High-quality educational illustration for Chinese literature class.
Scene: Daiyu burying fallen flowers in Grand View Garden (黛玉葬花), Qing dynasty costume,
delicate sorrowful mood, soft morning light, peach blossoms, classical Chinese garden pavilion.
Style: refined digital gouache, museum-quality, no text, no watermark, 16:9 landscape.""",
        ),
        (
            "illustration-baoyu-and-garden.png",
            """High-quality educational illustration: Jia Baoyu in Grand View Garden (大观园),
elegant Ming-Qing style architecture, scholars and maidens in distance, warm golden afternoon.
Style: historical drama concept art, rich detail, cinematic composition, no text, 16:9.""",
        ),
        (
            "illustration-red-chamber-themes.png",
            """Educational infographic-style painting (not diagram): symbols of Dream of the Red Chamber —
jade, flower, scroll, incense, falling petals, metaphor of family rise and fall.
Style: Chinese aesthetic, deep crimson and gold accents on dark ink wash background, artistic not cartoon, no text.""",
        ),
    ],
}


def get_api_key() -> str:
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        raise SystemExit(
            "请设置环境变量 OPENROUTER_API_KEY（勿写入代码库）。"
            "  export OPENROUTER_API_KEY='sk-or-v1-...'"
        )
    return key


def generate_image(prompt: str, out_path: Path, model: str, api_key: str) -> bool:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(1, 4):
        try:
            resp = requests.post(
                API_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://www.teachany.cn",
                    "X-Title": "TeachAny Courseware",
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "modalities": ["image", "text"],
                },
                timeout=180,
            )
            if resp.status_code == 429:
                wait = 15 * attempt
                print(f"  429 限流，{wait}s 后重试…")
                time.sleep(wait)
                continue
            if resp.status_code != 200:
                print(f"  HTTP {resp.status_code}: {resp.text[:300]}")
                time.sleep(10 * attempt)
                continue

            data = resp.json()
            images = data.get("choices", [{}])[0].get("message", {}).get("images", [])
            if not images:
                print(f"  无 images 字段: {json.dumps(data)[:400]}")
                time.sleep(10 * attempt)
                continue

            url = images[0].get("image_url", {}).get("url", "")
            if not url.startswith("data:image"):
                print(f"  非 data URL: {url[:80]}")
                return False

            raw = base64.b64decode(url.split(",", 1)[1])
            if len(raw) < 20 * 1024:
                print(f"  文件过小 ({len(raw)} B)，可能无效")
                return False

            out_path.write_bytes(raw)
            print(f"  ✅ {out_path.name} ({len(raw)//1024} KB)")
            return True
        except requests.Timeout:
            print(f"  超时 attempt {attempt}")
            time.sleep(12 * attempt)
        except Exception as e:
            print(f"  错误: {e}")
            time.sleep(8 * attempt)
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", "-p", help="生图 prompt（英文效果更好）")
    ap.add_argument("--out", "-o", help="输出路径")
    ap.add_argument("--course", help="课件目录名，如 chn-h-red-chamber")
    ap.add_argument("--preset", choices=list(PRESETS.keys()), help="预设组图")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--delay", type=float, default=8.0, help="张间间隔秒")
    args = ap.parse_args()

    api_key = get_api_key()

    jobs: list[tuple[Path, str]] = []

    if args.preset and args.course:
        base = ROOT / "community" / args.course / "assets"
        for fname, prompt in PRESETS[args.preset]:
            jobs.append((base / fname, prompt))
    elif args.prompt and args.out:
        jobs.append((Path(args.out), args.prompt))
    else:
        ap.print_help()
        sys.exit(1)

    ok = 0
    for i, (path, prompt) in enumerate(jobs):
        if not path.is_absolute():
            path = ROOT / path
        print(f"[{i+1}/{len(jobs)}] {path.name}")
        if generate_image(prompt, path, args.model, api_key):
            ok += 1
        if i < len(jobs) - 1:
            time.sleep(args.delay)

    print(f"\n完成 {ok}/{len(jobs)}")
    sys.exit(0 if ok == len(jobs) else 1)


if __name__ == "__main__":
    main()
