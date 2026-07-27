#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TeachAny 图片批量生成（与内容增强管线并行安全：只写 assets/*.png，不改 index.html）。

对 community/ 下每个课件：
  1. 解析真实主题（复用 pipeline_enhance_sample.resolve_topic）
  2. 生成 hero + 2 张章节插图 prompt，调用 scripts/agnes-image-gen.py 批量生图到 assets/
  3. 输出文件：{cid}-hero.png / section1.png / section2.png
幂等：assets 已有 >=3 张 png 则跳过。
index.html 的 <img> 引用由后续 link_images.py 统一注入（避免与内容进程并发写冲突）。

用法：
  python3 bulk_image_gen.py            # 全量
  python3 bulk_image_gen.py <cid> ...  # 指定
"""
from __future__ import annotations
import json, subprocess, sys, time
from pathlib import Path

from pipeline_enhance_sample import resolve_topic, COMMUNITY

AGNES = Path(__file__).resolve().parent / "scripts" / "agnes-image-gen.py"
MIN_IMAGES = 3


def gen_one(cid):
    d = COMMUNITY / cid
    html_path = d / "index.html"
    mf_path = d / "manifest.json"
    if not html_path.exists():
        return f"{cid}: 跳过(无 index.html)"
    assets = d / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    existing = list(assets.glob("*.png"))
    if len(existing) >= MIN_IMAGES:
        return f"{cid}: 跳过(已有 {len(existing)} 张图)"
    html = html_path.read_text(encoding="utf-8", errors="ignore")
    manifest = {}
    if mf_path.exists():
        try:
            manifest = json.loads(mf_path.read_text(encoding="utf-8"))
        except Exception:
            manifest = {}
    topic, subj_cn, grade = resolve_topic(manifest, cid, html)
    if not topic:
        return f"{cid}: 跳过(无真实主题)"
    # 强制中文知识点标注（Agnes）；禁止纯装饰无文字图
    prompts = [
        {"name": "hero", "slot": "hero",
         "prompt": (
             f"教育信息图封面，深色背景，扁平矢量，主题《{topic}》（{subj_cn}）。"
             f"图中必须印出清晰中文标注知识点名称与关键术语，禁止英文乱码，禁止水印。"
         )},
        {"name": "section1", "slot": "section1",
         "prompt": (
             f"《{topic}》核心概念结构图，扁平教育插画，深色背景，"
             f"用中文卡片标注关键概念与关系，文字清晰可读。"
         )},
        {"name": "section2", "slot": "section2",
         "prompt": (
             f"《{topic}》生活应用/易错对比示意，扁平教育插画，"
             f"中文标注正确要点与常见误区关键词。"
         )},
    ]
    batch = assets / ".agnes_batch.json"
    batch.write_text(json.dumps(prompts, ensure_ascii=False), encoding="utf-8")
    try:
        r = subprocess.run(
            [sys.executable, str(AGNES), "--course-id", cid,
             "--batch", str(batch), "--out-dir", str(assets)],
            capture_output=True, text=True, timeout=400)
    except Exception as e:
        return f"{cid}: 生图调用异常 - {e}"
    ok = len(list(assets.glob("*.png")))
    if batch.exists():
        batch.unlink()
    if r.returncode != 0 or ok < MIN_IMAGES:
        return f"{cid}: 生图不足(得到 {ok} 张) - {r.stdout.strip()[-200:] or r.stderr.strip()[-200:]}"
    return f"{cid}: 生图成功({ok} 张, 主题={topic})"


def main():
    cids = sys.argv[1:]
    if not cids:
        cids = [d.name for d in sorted(COMMUNITY.iterdir()) if (d / "index.html").exists()]
    ok = skip = fail = 0
    for cid in cids:
        try:
            res = gen_one(cid)
        except Exception as e:
            res = f"{cid}: 异常 - {e}"
        print(res, flush=True)
        if "成功" in res:
            ok += 1
        elif "跳过" in res:
            skip += 1
        else:
            fail += 1
        time.sleep(1)
    print(f"\n图片生成结束：成功={ok} 跳过={skip} 失败={fail}")


if __name__ == "__main__":
    main()
