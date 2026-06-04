#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OpenRouter Image2（google/gemini-3.1-flash-image-preview）单张/批量生图。

API Key 分工（勿混用）：
  OPENROUTER_IMAGE_API_KEY  你的付费 OpenRouter 账号 → 仅本脚本 / 课件高质量插图
  batch-hero-openrouter 等  项目内置免费额度 → 批量 hero，不得传给本脚本

本脚本只读 OPENROUTER_IMAGE_API_KEY（或 OPENROUTER_PAID_API_KEY），
不读 OPENROUTER_API_KEY，避免误用免费 Key 导致 401。

用法:
  export OPENROUTER_IMAGE_API_KEY='sk-or-v1-...'   # 本地终端，勿提交仓库
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

STYLE_EDU_INFO = (
    "Educational infographic for Chinese middle/high school literature class, "
    "refined digital illustration, classical Chinese garden motifs (pavilion, plum blossom, scroll), "
    "deep navy and crimson-gold palette, museum-quality, clear layout, no watermark."
)

PRESETS = {
    "dream-red-mansions-3": [
        (
            "hero-infographic.png",
            f"""{STYLE_EDU_INFO}
Poster title area: Dream of the Red Chamber selected reading (《红楼梦》选读).
Three equal panels: 人物关系 (character relations), 细节伏笔 (details and foreshadowing), 主题意蕴 (theme and meaning).
Bottom banner: memory anchor about reading classics from details to themes.
Landscape 16:9, legible simplified Chinese labels in each panel.""",
        ),
        (
            "concept-diagram.png",
            f"""{STYLE_EDU_INFO}
Concept map with three connected nodes labeled in Chinese: 人物关系, 细节伏笔, 主题意蕴.
Central question mood: using textual evidence to explain expression and emotion in Red Chamber excerpts.
Clean arrows between nodes, dark blue background, cyan purple green accent colors.""",
        ),
        (
            "process-diagram.png",
            f"""{STYLE_EDU_INFO}
Three-step horizontal flowchart in Chinese: 圈画证据 → 判断方法 → 组织答案.
Topic: answering questions on Dream of the Red Chamber selected passages.
Subtle Grand View Garden silhouette in background, same color scheme as companion slides.""",
        ),
    ],
    "red-chamber-diagrams": [
        (
            "hero-infographic.png",
            f"""{STYLE_EDU_INFO}
Whole-book reading overview poster: 《红楼梦》整本书阅读 — 感动细节, 四层赏析, 研读研讨.
Four modules: 通读精读, 四层赏析, 研讨追问, 阅读档案; bottom quote about moved-by-details close reading.
Landscape 16:9, legible simplified Chinese labels, crimson-gold classical garden mood.""",
        ),
        (
            "character-relations.png",
            f"""{STYLE_EDU_INFO}
Family relationship diagram for Jia household in Dream of the Red Chamber.
Nodes: 贾母 at top, 贾政 and 王夫人, 贾宝玉 林黛玉 薛宝钗, 王熙凤.
Elegant org-chart with connecting lines on dark burgundy background, Chinese labels, 16:9.""",
        ),
        (
            "plot-timeline.png",
            f"""{STYLE_EDU_INFO}
Horizontal timeline of key plot beats in Dream of the Red Chamber for high school reading:
通读, 葬花, 宝玉挨打, 抄检大观园, 好了歌, 衰败收束.
Chinese labels along a golden timeline, classical ink-wash landscape strip below.""",
        ),
        (
            "appreciation-lens.png",
            f"""{STYLE_EDU_INFO}
Circular four-lens analysis diagram around center 文本证据:
语言品味, 人物形象, 结构照应, 主题意蕴.
Dream of the Red Chamber literary appreciation method, symmetrical layout, Chinese labels.""",
        ),
    ],
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
    for env_name in ("OPENROUTER_IMAGE_API_KEY", "OPENROUTER_PAID_API_KEY"):
        key = os.environ.get(env_name, "").strip()
        if key:
            return key
    if os.environ.get("OPENROUTER_API_KEY", "").strip():
        raise SystemExit(
            "❌ 未设置付费生图 Key。image2 请用 OPENROUTER_IMAGE_API_KEY，"
            "不要用项目免费的 OPENROUTER_API_KEY。\n"
            "  export OPENROUTER_IMAGE_API_KEY='你的付费 sk-or-v1-...'\n"
            "免费批量 hero：scripts/batch-hero-openrouter.py（另一套额度）。"
        )
    raise SystemExit(
        "请设置 OPENROUTER_IMAGE_API_KEY（付费账号，仅本地 export，勿写入仓库）。"
    )


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
    ap.add_argument(
        "--only",
        help="预设模式下只生成指定文件名，逗号分隔，如 appreciation-lens.png,hero-infographic.png",
    )
    args = ap.parse_args()

    api_key = get_api_key()

    jobs: list[tuple[Path, str]] = []
    only_names = None
    if args.only:
        only_names = {x.strip() for x in args.only.split(",") if x.strip()}

    if args.preset and args.course:
        base = ROOT / "community" / args.course / "assets"
        for fname, prompt in PRESETS[args.preset]:
            if only_names and fname not in only_names:
                continue
            jobs.append((base / fname, prompt))
        if only_names and not jobs:
            raise SystemExit(f"❌ --only 未匹配 preset 内任何文件: {only_names}")
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
