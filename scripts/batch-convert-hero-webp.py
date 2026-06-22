#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量把 SVG hero 占位图转为 WebP，并更新 registry.json / community/index.json。

策略：
  1. 遍历 registry.json 中所有课件
  2. 对每个课件检测 community/<cid>/assets/ 下的图片
  3. 优先级：已有 .webp hero > .png hero > .svg hero（需转换）
  4. SVG → rsvg-convert → PNG → cwebp → WebP
  5. 更新 registry.json 的 hero_image 指向 .webp
  6. 同步更新 community/index.json（添加 hero_image 字段）

用法: python3 scripts/batch-convert-hero-webp.py [--dry-run]
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REGISTRY = REPO / "registry.json"
COMMUNITY_INDEX = REPO / "community" / "index.json"

# SVG hero 的标准文件名
SVG_HERO_NAME = "hero-infographic.svg"
WEBP_HERO_NAME = "hero-infographic.webp"


def find_hero_image(course_dir: Path) -> str | None:
    """检测课件目录下正确的 hero 图片，返回相对路径(相对课件目录)。"""
    adir = course_dir / "assets"
    if not adir.is_dir():
        return None
    # 1. 优先 webp
    for name in (WEBP_HERO_NAME,):
        if (adir / name).exists():
            return f"assets/{name}"
    # 其他 hero webp
    for p in sorted(adir.glob("*hero*.webp")):
        return f"assets/{p.name}"
    # 2. png hero
    for p in sorted(adir.glob("*hero*.png")):
        return f"assets/{p.name}"
    # 3. svg（需转换）
    if (adir / SVG_HERO_NAME).exists():
        return f"assets/{SVG_HERO_NAME}"
    # 4. 其他 svg hero
    for p in sorted(adir.glob("*hero*.svg")):
        return f"assets/{p.name}"
    return None


def convert_svg_to_webp(svg_path: Path, webp_path: Path, width: int = 1280) -> bool:
    """SVG → PNG(rsvg-convert) → WebP(cwebp)。"""
    if webp_path.exists() and webp_path.stat().st_size > 5 * 1024:
        return True  # 已存在
    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_png = Path(tmp.name)
        # SVG → PNG
        r = subprocess.run(
            ["rsvg-convert", "-w", str(width), str(svg_path), "-o", str(tmp_png)],
            capture_output=True, text=True, timeout=30,
        )
        if r.returncode != 0:
            print(f"  ❌ rsvg-convert 失败: {svg_path}: {r.stderr[:100]}")
            tmp_png.unlink(missing_ok=True)
            return False
        # PNG → WebP
        r = subprocess.run(
            ["cwebp", "-q", "85", "-quiet", str(tmp_png), "-o", str(webp_path)],
            capture_output=True, text=True, timeout=30,
        )
        tmp_png.unlink(missing_ok=True)
        if r.returncode != 0:
            print(f"  ❌ cwebp 失败: {webp_path}: {r.stderr[:100]}")
            return False
        return webp_path.exists() and webp_path.stat().st_size > 0
    except Exception as e:
        print(f"  ❌ 转换异常 {svg_path}: {e}")
        return False


def main():
    dry_run = "--dry-run" in sys.argv

    print("═══════════════════════════════════════════════")
    print("  TeachAny Hero 图 WebP 批量转换")
    print("═══════════════════════════════════════════════")
    if dry_run:
        print("  ⚠️  DRY RUN 模式（不写文件）")

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    courses = registry.get("courses", [])
    print(f"  registry 课件总数: {len(courses)}")

    stats = {"already_webp": 0, "already_png": 0, "converted": 0, "convert_fail": 0, "no_hero": 0}
    updates = []  # (cid, old_hero, new_hero)
    need_convert = []  # (cid, svg_path, webp_path)

    for c in courses:
        cid = c["id"]
        old_hero = c.get("hero_image", "")
        course_dir = REPO / "community" / cid
        hero = find_hero_image(course_dir)

        if not hero:
            stats["no_hero"] += 1
            continue

        if hero.endswith(".webp"):
            if old_hero != hero:
                updates.append((cid, old_hero, hero))
            stats["already_webp"] += 1
        elif hero.endswith(".png"):
            if old_hero != hero:
                updates.append((cid, old_hero, hero))
            stats["already_png"] += 1
        elif hero.endswith(".svg"):
            svg_path = course_dir / hero
            webp_rel = hero.rsplit(".", 1)[0] + ".webp"
            webp_path = course_dir / webp_rel
            # 如果 webp 已存在（之前转换过）
            if webp_path.exists() and webp_path.stat().st_size > 5 * 1024:
                if old_hero != webp_rel:
                    updates.append((cid, old_hero, webp_rel))
                stats["already_webp"] += 1
            else:
                need_convert.append((cid, svg_path, webp_path, webp_rel, old_hero))
        else:
            if old_hero != hero:
                updates.append((cid, old_hero, hero))

    print(f"\n📊 检测结果:")
    print(f"  已有 WebP: {stats['already_webp']}")
    print(f"  已有 PNG:  {stats['already_png']}")
    print(f"  需转换 SVG: {len(need_convert)}")
    print(f"  无 hero:   {stats['no_hero']}")
    print(f"  需更新 registry: {len(updates)}")

    if dry_run:
        print("\n[DRY RUN] 需转换的前10个:")
        for cid, sp, wp, wr, oh in need_convert[:10]:
            print(f"  {cid}: {oh} → {wr}")
        return

    # ── 批量转换 SVG → WebP ──
    if need_convert:
        print(f"\n🔄 开始转换 {len(need_convert)} 个 SVG → WebP ...")
        for i, (cid, svg_path, webp_path, webp_rel, old_hero) in enumerate(need_convert, 1):
            ok = convert_svg_to_webp(svg_path, webp_path)
            if ok:
                updates.append((cid, old_hero, webp_rel))
                stats["converted"] += 1
                if i % 20 == 0:
                    print(f"  进度: {i}/{len(need_convert)}")
            else:
                stats["convert_fail"] += 1
        print(f"  ✅ 转换成功: {stats['converted']}, 失败: {stats['convert_fail']}")

    # ── 更新 registry.json ──
    update_map = {u[0]: u[2] for u in updates}
    for c in courses:
        if c["id"] in update_map:
            c["hero_image"] = update_map[c["id"]]

    registry["courses"] = courses
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ registry.json 已更新（{len(updates)} 处变更）")

    # ── 同步更新 community/index.json（添加 hero_image 字段）──
    if COMMUNITY_INDEX.exists():
        ci = json.loads(COMMUNITY_INDEX.read_text(encoding="utf-8"))
        ci_courses = ci.get("courses", [])
        ci_updated = 0
        for c in ci_courses:
            cid = c["id"]
            if cid in update_map:
                c["hero_image"] = update_map[cid]
                ci_updated += 1
            elif cid not in [u[0] for u in updates]:
                # 从 registry 同步
                for rc in courses:
                    if rc["id"] == cid and rc.get("hero_image"):
                        c["hero_image"] = rc["hero_image"]
                        ci_updated += 1
                        break
        ci["courses"] = ci_courses
        COMMUNITY_INDEX.write_text(json.dumps(ci, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ community/index.json 已同步（{ci_updated} 处）")

    # ── 最终统计 ──
    print("\n═══════════════════════════════════════════════")
    print("  最终统计:")
    print(f"  已有 WebP: {stats['already_webp']}")
    print(f"  本次转换: {stats['converted']}")
    print(f"  已有 PNG:  {stats['already_png']}")
    print(f"  转换失败:  {stats['convert_fail']}")
    print(f"  无 hero:   {stats['no_hero']}")
    print("═══════════════════════════════════════════════")


if __name__ == "__main__":
    main()
