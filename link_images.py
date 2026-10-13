#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TeachAny 图片引用注入（必须在 内容增强 + 图片生成 都完成后运行，单线程改 index.html）。

对每个课件：
  - 找 hero 图（{cid}-hero.png / hero.png / *hero*.png）与章节图（section1/section2.png 等）
  - 若 HTML 无 hero-cover-img 引用且有 hero 图 → 在首个 <section> 前注入 hero 封面块
  - 若 HTML 中 <img src="./assets/"> 引用 < 2 → 在知识图谱模块前注入图片画廊块
幂等：已满足则跳过。
"""
from __future__ import annotations
import re, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMUNITY = ROOT / "community"


def link_one(cid):
    d = COMMUNITY / cid
    html_path = d / "index.html"
    if not html_path.exists():
        return f"{cid}: 跳过(无 index.html)"
    assets = d / "assets"
    if not assets.exists():
        return f"{cid}: 跳过(无 assets)"
    pngs = sorted(assets.glob("*.png"))
    if not pngs:
        return f"{cid}: 跳过(无图)"
    html = html_path.read_text(encoding="utf-8")
    # 仅处理内容增强已完成的课件，避免与正在跑的内容进程并发写 index.html 冲突
    if "<!-- teachany-enhanced -->" not in html:
        return f"{cid}: 跳过(内容增强未完成)"
    hero = None
    for cand in [f"{cid}-hero.png", "hero.png"]:
        if (assets / cand).exists():
            hero = cand
            break
    if hero is None:
        for p in pngs:
            if "hero" in p.name:
                hero = p.name
                break
    sec_imgs = [p.name for p in pngs if p.name != hero]
    changed = False
    # hero 引用
    if hero and "hero-cover-img" not in html:
        hero_block = (f'<section class="hero-cover">'
                      f'<img class="hero-cover-img" src="./assets/{hero}" alt="课程封面"></section>\n')
        m = re.search(r"<section\b", html)
        if m:
            html = html[:m.start()] + hero_block + html[m.start():]
        else:
            html = html.replace("<body>", "<body>\n" + hero_block, 1)
        changed = True
    # 章节图引用计数
    ref_count = len(re.findall(r'<img[^>]+src="\./assets/', html))
    needed = 2 - ref_count
    if needed > 0 and sec_imgs:
        picks = sec_imgs[: needed + 1]
        gallery = '<section class="course-gallery">\n'
        for name in picks:
            gallery += f'  <img src="./assets/{name}" alt="课程插图">\n'
        gallery += '</section>\n'
        anchor = re.search(r"<!--\s*v7\.7\.4 标准知识图谱模块", html)
        if anchor:
            html = html[:anchor.start()] + gallery + html[anchor.start():]
        else:
            html = html.replace("</body>", gallery + "</body>", 1)
        changed = True
    if changed:
        html_path.write_text(html, encoding="utf-8")
        return f"{cid}: 已注入图片引用(hero={'Y' if hero else 'N'})"
    return f"{cid}: 跳过(引用已满足)"


def main():
    cids = sys.argv[1:]
    if not cids:
        cids = [d.name for d in sorted(COMMUNITY.iterdir()) if (d / "index.html").exists()]
    ok = skip = 0
    for cid in cids:
        try:
            res = link_one(cid)
        except Exception as e:
            res = f"{cid}: 异常 - {e}"
        print(res, flush=True)
        if "已注入" in res:
            ok += 1
        elif "跳过" in res:
            skip += 1
        time.sleep(0.1)
    print(f"\n图片引用注入完成：注入={ok} 跳过={skip}")


if __name__ == "__main__":
    main()
