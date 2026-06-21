#!/usr/bin/env python3
"""一次性修复 r6 人工队列剩余课件。"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
FINALIZE = Path.home() / ".claude/skills/teachany/scripts/finalize-courseware.py"


def patch_html(cid: str, fn) -> bool:
    p = COMMUNITY / cid / "index.html"
    if not p.is_file():
        return False
    html = p.read_text(encoding="utf-8")
    new = fn(html)
    if new != html:
        p.write_text(new, encoding="utf-8")
        return True
    return False


def fix_history_tracker(cid: str) -> None:
    patch_html(
        cid,
        lambda h: re.sub(
            r'src=["\']\./history-tracker\.js["\']',
            'src="/assets/scripts/history-tracker.js"',
            h,
        ),
    )


def fix_double_slash_scripts(cid: str) -> None:
    patch_html(
        cid,
        lambda h: h.replace("..//assets/scripts/", "/assets/scripts/"),
    )


def fix_cross_nav(cid: str, target: str) -> None:
    url = f"https://www.teachany.cn/community/{target}/"
    patch_html(
        cid,
        lambda h: re.sub(
            r'href=["\'](?:\.\./[^"\']+|/community/[^"\']+)/index\.html["\']',
            f'href="{url}"',
            h,
        ),
    )
    patch_html(
        cid,
        lambda h: h.replace(f'href="/community/{target}/"', f'href="{url}"'),
    )


def strip_missing_video(cid: str) -> None:
    patch_html(
        cid,
        lambda h: re.sub(r"<video[^>]*>.*?</video>\s*", "", h, flags=re.S | re.I),
    )
    patch_html(
        cid,
        lambda h: re.sub(
            r'<source[^>]*teachany-overview\.mp4[^>]*>\s*',
            "",
            h,
            flags=re.I,
        ),
    )
    patch_html(
        cid,
        lambda h: re.sub(
            r'src=["\'][^"\']*teachany-overview\.mp4["\']',
            "",
            h,
            flags=re.I,
        ),
    )


def fix_medieval_europe_map() -> None:
    cid = "history-medieval-europe"
    p = COMMUNITY / cid / "index.html"
    html = p.read_text(encoding="utf-8")
    if "L.tileLayer" in html:
        return
    old = (
        "L.imageOverlay('./assets/maps/hillshade.jpg', [[-90, -180], [90, 180]], "
        "{ opacity: 0.5, interactive: false }).addTo(map);"
    )
    new = (
        "L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', "
        "{ maxZoom: 8, attribution: '© OpenStreetMap' }).addTo(map);"
    )
    if old in html:
        html = html.replace(old, new)
        p.write_text(html, encoding="utf-8")


def ensure_hero_from_svg(cid: str) -> None:
    d = COMMUNITY / cid
    assets = d / "assets"
    heroes = list(assets.glob("*hero*"))
    tiny = [h for h in heroes if h.suffix.lower() != ".svg" and h.stat().st_size < 20 * 1024]
    if not tiny:
        return
    svg = assets / "hero-infographic.svg"
    if not svg.is_file():
        from importlib.util import spec_from_file_location, module_from_spec

        spec = spec_from_file_location("r", ROOT / "scripts/repair-image-refs.py")
        mod = module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.ensure_standard_svgs(d, mod.course_title(d))
    # 若 PNG hero 过小，HTML 改指向 SVG
    for h in tiny:
        patch_html(
            cid,
            lambda html, name=h.name: html.replace(f"./assets/{name}", "./assets/hero-infographic.svg"),
        )


def main() -> int:
    fix_history_tracker("chem-h-galvanic-cell")
    fix_history_tracker("phy-m-light-reflection")
    fix_double_slash_scripts("sci-e-weather-observation")
    fix_cross_nav("hist-h-four-great-inventions", "hist-h-industrial-revolutions")
    strip_missing_video("chn-compound-vowel")
    strip_missing_video("dc-motor-principle")
    fix_medieval_europe_map()
    for cid in (
        "bio-m-animal-diversity",
        "chem-daily-life",
        "chem-m-neutralization",
        "dc-motor-principle",
        "ext-7be00e85",
    ):
        ensure_hero_from_svg(cid)

    if FINALIZE.is_file():
        for cid in ("chn-compound-vowel", "dc-motor-principle", "sci-e-weather-observation"):
            subprocess.run(
                [sys.executable, str(FINALIZE), str(COMMUNITY / cid), "--shared", "--no-audio"],
                check=False,
            )

    print("✅ manual queue patched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
