#!/usr/bin/env python3
"""
修复 hero 主图未放在 <header class="hero"> 内的问题。

扫描社区课件：如果课件有 header.hero，但 hero 资产（assets/<course-id>-hero.*
或 assets/hero.webp|png）的引用在 hero 外部，并且该引用位于一个包裹
section#hero-infographic 的 slide-page 内，则把 section 块移入 header.hero
并删除被搬空的 slide-page。

同时写入最小 CSS 覆盖，避免内嵌 section/figure 的默认 padding 破坏 hero 排版。
"""
import argparse
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "community"

HERO_INFO_RE = re.compile(
    r'(<div\b[^>]*class="slide-page[^"]*"[^>]*>\s*)'
    r'(<section\b[^>]*\bid="hero-infographic"[^>]*>.*?</section>)\s*'
    r'</div>',
    re.S,
)
# 第二类形态：hero-infographic 是独立顶层块（前面可能只跟一行注释），
# 没有被 slide-page 包裹，直接紧跟或靠近 header 之后。
HERO_INFO_STANDALONE_RE = re.compile(
    r'(?P<comment><!--[^>]*-->\s*)?'
    r'(?P<section><section\b[^>]*\bid="hero-infographic"[^>]*>.*?</section>)',
    re.S,
)
HERO_ASSET_RE = re.compile(r'<img\b[^>]*src="([^"]+)"')


def hero_assets_for(course_dir: Path, cid: str):
    assets_dir = course_dir / "assets"
    if not assets_dir.is_dir():
        return []
    out = []
    for f in assets_dir.iterdir():
        name = f.name
        if name.startswith(f"{cid}-hero") or name in ("hero.webp", "hero.png"):
            out.append(name)
    return out


def hero_header_span(src: str):
    hs = re.search(r'<header\b[^>]*class="hero"[^>]*>', src)
    he = re.search(r'</header>', src)
    if not (hs and he):
        return None
    return hs.start(), he.end(), hs.end(), he.start()


def find_hero_img_in_header(src: str, hero_span, strict_assets):
    _, _, hstart, hend = hero_span
    for m in HERO_ASSET_RE.finditer(src):
        if not (hstart <= m.start() <= hend):
            continue
        fn = m.group(1).split("/")[-1]
        if fn in strict_assets:
            return fn
    return None


def find_out_of_hero_hero_img(src: str, hero_span, strict_assets):
    _, _, hstart, hend = hero_span
    for m in HERO_ASSET_RE.finditer(src):
        if hstart <= m.start() <= hend:
            continue
        fn = m.group(1).split("/")[-1]
        if fn in strict_assets:
            return m
    return None


def add_hero_css_override(src: str):
    # 如果已经有 hero-inner/hero-grid，说明已经采用左右布局，不需要额外覆盖
    if re.search(r'\.hero-inner\b|\.hero-grid\b|\.hero-visual\b', src):
        return src
    # 在第一个 </header> 之前找最后一个顶层的 .hero { ... }
    header_pos = src.find('<header class="hero"')
    if header_pos < 0:
        return src
    # 找到第一个 <header 之前的最后一个 .hero { 块
    hero_css_pat = re.compile(r'\.hero\s*\{[^}]*\}')
    last = None
    for m in hero_css_pat.finditer(src[:header_pos]):
        last = m
    if not last:
        return src
    override = "\n.hero .section { padding: 0; max-width: 980px; }\n.hero .ta-standard-figure { margin-top: 26px; }"
    # 避免重复写入
    if ".hero .section { padding: 0" in src:
        return src
    return src[: last.end()] + override + src[last.end() :]


def try_fix_course(course_dir: Path, dry_run: bool = False):
    idx = course_dir / "index.html"
    if not idx.is_file():
        return {"status": "no_index", "cid": course_dir.name}
    src = io.open(idx, encoding="utf-8").read()
    cid = course_dir.name
    strict_assets = hero_assets_for(course_dir, cid)
    if not strict_assets:
        return {"status": "no_hero_asset", "cid": cid}

    hero_span = hero_header_span(src)
    if not hero_span:
        return {"status": "no_hero_header", "cid": cid}

    if find_hero_img_in_header(src, hero_span, strict_assets):
        return {"status": "already_ok", "cid": cid}

    # 寻找 slide-page -> section#hero-infographic 块；找不到再试独立顶层块
    m = HERO_INFO_RE.search(src)
    mode = "wrapped"
    if not m:
        m = HERO_INFO_STANDALONE_RE.search(src)
        mode = "standalone"
    if not m:
        return {"status": "no_infographic_slide", "cid": cid}

    # 确认 block 内的 img 引用了 strict hero 资产
    section_block = m.group(2) if mode == "wrapped" else m.group("section")
    imgs = HERO_ASSET_RE.findall(section_block)
    if not any(img.split("/")[-1] in strict_assets for img in imgs):
        return {"status": "infographic_not_hero_asset", "cid": cid}

    if dry_run:
        return {"status": "would_fix", "cid": cid, "img": imgs, "mode": mode}

    # 1) 取出 section block 并移入 header
    if mode == "wrapped":
        new_src = src[: m.start()] + src[m.end() :]
    else:
        comment = m.group("comment")
        # 只有当紧邻的注释确实属于 hero 图时才一并移走，避免误删别的段落注释
        start = (
            m.start("comment")
            if comment and re.search(r"hero|Hero|知识结构", comment)
            else m.start("section")
        )
        new_src = src[:start] + src[m.end("section") :]
    # 重新计算 hero span
    hero_span2 = hero_header_span(new_src)
    if not hero_span2:
        return {"status": "lost_header", "cid": cid}
    _, _, hstart, hend = hero_span2
    # 在 </header> 前插入
    insert_pos = hend
    new_src = new_src[:insert_pos] + "\n" + section_block + "\n" + new_src[insert_pos:]

    # 2) 补 CSS
    new_src = add_hero_css_override(new_src)

    # 3) 验证：移动后 hero 内有了图
    new_span = hero_header_span(new_src)
    if not find_hero_img_in_header(new_src, new_span, strict_assets):
        return {"status": "fix_verify_failed", "cid": cid}

    io.open(idx, "w", encoding="utf-8").write(new_src)
    return {"status": "fixed", "cid": cid, "img": imgs}


def main():
    parser = argparse.ArgumentParser(description="修复 hero 图位置")
    parser.add_argument("--course", help="只处理指定课件目录名")
    parser.add_argument("--dry-run", action="store_true", help="只扫描不写入")
    parser.add_argument("--sample", type=int, help="仅处理前 N 个可修复的课件")
    args = parser.parse_args()

    dirs = [ROOT / args.course] if args.course else sorted(ROOT.iterdir())
    results = []
    for d in dirs:
        r = try_fix_course(d, dry_run=args.dry_run)
        results.append(r)
        if r["status"] in ("fixed", "would_fix"):
            print(f"{r['status']:15} {r['cid']}")

    summary = {}
    for r in results:
        summary[r["status"]] = summary.get(r["status"], 0) + 1
    print("\n=== 统计 ===")
    for k, v in sorted(summary.items()):
        print(f"{k:25} {v}")

    if args.sample:
        to_fix = [r for r in results if r["status"] == "would_fix"][: args.sample]
        for r in to_fix:
            rr = try_fix_course(ROOT / r["cid"], dry_run=False)
            print(f"sample fixed: {rr['cid']} -> {rr.get('status')}")


if __name__ == "__main__":
    main()
