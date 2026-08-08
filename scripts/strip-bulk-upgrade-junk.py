#!/usr/bin/env python3
"""Strip bulk-upgrade template junk that breaks page order / content.

Removes TeachAny Upgrade #02/#05/#06/#08/#14/#17/#18 blocks, glued generic ABT,
diagnosis patch scripts, and moves <nav> that sits outside <body> back inside.

Usage:
  python3 scripts/strip-bulk-upgrade-junk.py                 # all community/
  python3 scripts/strip-bulk-upgrade-junk.py chn-e-poetry-imagery eng-e-greetings-intro
  python3 scripts/strip-bulk-upgrade-junk.py --dry-run
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

# Ordered: longer / more specific first. Each matches comment + following block.
UPGRADE_BLOCK_RES = [
    # Posttest includes trailing checkPosttest <script>
    # Allow attributes before id=; optional ABT Fix / abt-card glue
    re.compile(
        r"<!--\s*后测\s*-?\s*TeachAny Upgrade\s*#05\s*-->\s*"
        r"(?:<!--\s*ABT Fix\s*-->\s*)?"
        r"(?:<div\b[^>]*class=['\"][^'\"]*abt-card[^'\"]*['\"][\s\S]*?</div>\s*)?"
        r"<section\b[^>]*\bid=['\"]posttest['\"][^>]*>[\s\S]*?</section>\s*"
        r"(?:<script\b[\s\S]*?function\s+checkPosttest[\s\S]*?</script>\s*)?",
        re.I,
    ),
    # Orphan upgrade comment glued onto unrelated next section
    re.compile(r"<!--\s*后测\s*-?\s*TeachAny Upgrade\s*#05\s*-->\s*", re.I),
    re.compile(
        r"<!--\s*前测\s*-?\s*TeachAny Upgrade\s*#02\s*-->\s*"
        r"<section\b[^>]*\bid=['\"]pretest['\"][^>]*>[\s\S]*?</section>\s*",
        re.I,
    ),
    # Orphan pretest comment
    re.compile(r"<!--\s*前测\s*-?\s*TeachAny Upgrade\s*#02\s*-->\s*", re.I),
    re.compile(
        r"<!--\s*ABT 情境引入\s*-?\s*TeachAny Upgrade\s*-->\s*"
        r"<div\b[^>]*class=['\"][^'\"]*abt-card[^'\"]*['\"][\s\S]*?</div>\s*",
        re.I,
    ),
    re.compile(
        r"<!--\s*记忆锚点\s*-?\s*TeachAny Upgrade\s*#17\s*-->\s*"
        r"<div\b[^>]*class=['\"][^'\"]*memory-anchor[^'\"]*['\"][\s\S]*?</div>\s*",
        re.I,
    ),
    # Nested header <div> inside error-points — match through tip <p> + outer </div>
    re.compile(
        r"<!--\s*易错点\s*-?\s*TeachAny Upgrade\s*#18\s*-->\s*"
        r"<div\b[^>]*class=['\"][^'\"]*error-points[^'\"]*['\"][^>]*>\s*"
        r"<div\b[^>]*>[\s\S]*?</div>\s*"
        r"<ul\b[^>]*>[\s\S]*?</ul>\s*"
        r"<p\b[^>]*>[\s\S]*?</p>\s*"
        r"</div>\s*",
        re.I,
    ),
    re.compile(
        r"<!--\s*AI 互动区\s*-?\s*TeachAny Upgrade\s*#14\s*-->\s*"
        r"<section\b[^>]*id=['\"]ai-interaction['\"][\s\S]*?</section>\s*",
        re.I,
    ),
    re.compile(
        r"<!--\s*Bloom层级覆盖\s*-?\s*TeachAny Upgrade\s*#06\s*-->\s*"
        r"<div\b[^>]*class=['\"][^'\"]*bloom-exercises[^'\"]*['\"][\s\S]*?</div>\s*",
        re.I,
    ),
    re.compile(
        r"<!--\s*五镜头深层理解\s*-?\s*TeachAny Upgrade\s*#08\s*-->\s*"
        r"<div\b[^>]*class=['\"][^'\"]*five-lens[^'\"]*['\"][\s\S]*?</div>\s*",
        re.I,
    ),
    # Diagnosis patch glued after phase2
    re.compile(
        r"<!--\s*诊断性反馈\s*#04\s*patch\s*-->\s*"
        r"<script\b[\s\S]*?</script>\s*",
        re.I,
    ),
]

# Generic ABT without upgrade comment (often glued before posttest)
GENERIC_ABT_RE = re.compile(
    r"<div\b[^>]*class=['\"][^'\"]*abt-card[^'\"]*['\"][^>]*>\s*"
    r"<div[^>]*>\s*🎯\s*为什么学这节课？\s*</div>\s*"
    r"<p>[^<]*And（已知）[^<]*你已经掌握了一些基础知识</p>\s*"
    r"<p>[^<]*But（问题）[^<]*遇到更复杂的情况还不够用</p>\s*"
    r"<p>[^<]*Therefore（新知）[^<]*学习今天的内容，让能力更完整、更系统</p>\s*"
    r"</div>\s*",
    re.I,
)

# Orphan generic wrong-error clinic leftovers (chinese template)
WRONG_CHAR_ERRORS = [
    "先竖后横的笔顺错误",
    "混淆会意字和形声字",
    "望文生义，按字面意思理解成语",
]


def fix_nav_outside_body(html: str) -> tuple[str, bool]:
    body_m = re.search(r"<body\b[^>]*>", html, re.I)
    if not body_m:
        return html, False
    # Collect navs that appear before <body>
    before = html[: body_m.start()]
    navs = list(re.finditer(r"<nav\b[\s\S]*?</nav>\s*", before, re.I))
    if not navs:
        return html, False
    chunks = [m.group(0) for m in navs]
    new_before = before
    for m in reversed(navs):
        new_before = new_before[: m.start()] + new_before[m.end() :]
    insert = "".join(chunks)
    # Insert right after <body...>
    pos = body_m.end() - (len(before) - len(new_before))  # recalculate
    # rebuild carefully
    html2 = new_before + body_m.group(0) + "\n" + insert + html[body_m.end() :]
    return html2, True


def ensure_screen_hides_inactive(html: str) -> tuple[str, bool]:
    """If course uses .screen active pattern but forgot display:none, non-active
    screens stack and look like chaos. Only add if pattern exists and missing rule."""
    if "class=\"screen active\"" not in html and "class='screen active'" not in html:
        return html, False
    if re.search(r"\.screen\s*\{[^}]*display\s*:\s*none", html, re.I):
        return html, False
    # Inject rule once into first <style>
    rule = "\n  .screen{display:none!important;}\n  .screen.active{display:flex!important;}\n"
    m = re.search(r"<style\b[^>]*>", html, re.I)
    if not m:
        return html, False
    return html[: m.end()] + rule + html[m.end() :], True


def move_hero_img_into_active_screen(html: str) -> tuple[str, bool]:
    """If hero-cover img sits between screens (always visible / or hidden wrong),
    and first active screen has no img, move a copy into the active hero screen."""
    if "hero-cover-img" not in html:
        return html, False
    if not re.search(r'class=["\']screen active["\']', html):
        return html, False
    # Find first active screen block
    sm = re.search(
        r'(<div\b[^>]*class=["\']screen active["\'][^>]*>)([\s\S]*?)(</div>\s*(?:<!--|$|<div\b[^>]*class=["\']screen))',
        html,
        re.I,
    )
    if not sm:
        return html, False
    screen_inner = sm.group(2)
    if "hero-cover-img" in screen_inner or "<img" in screen_inner:
        return html, False
    img_m = re.search(
        r'<img\b[^>]*class=["\'][^"\']*hero-cover-img[^"\']*["\'][^>]*>',
        html,
        re.I,
    )
    if not img_m:
        return html, False
    img_tag = img_m.group(0)
    # Prefer figure wrapper if present around that img
    fig_m = re.search(
        r"<figure\b[^>]*>[\s\S]*?" + re.escape(img_tag) + r"[\s\S]*?</figure>",
        html,
        re.I,
    )
    insert = fig_m.group(0) if fig_m else img_tag
    # Insert before the closing of active screen's main content — before last button if any
    btn = re.search(r"(<button\b[\s\S]*?</button>\s*)$", screen_inner, re.I)
    if btn:
        new_inner = screen_inner[: btn.start()] + insert + "\n" + screen_inner[btn.start() :]
    else:
        new_inner = screen_inner + "\n" + insert + "\n"
    new_html = html[: sm.start()] + sm.group(1) + new_inner + sm.group(3) + html[sm.end() :]
    return new_html, True


def strip_course(html: str) -> tuple[str, list[str]]:
    actions: list[str] = []
    original = html

    for i, cre in enumerate(UPGRADE_BLOCK_RES):
        html2, n = cre.subn("", html)
        if n:
            actions.append(f"upgrade_block[{i}]x{n}")
            html = html2

    html2, n = GENERIC_ABT_RE.subn("", html)
    if n:
        actions.append(f"generic_abtx{n}")
        html = html2

    # Residual: abt-card with only the three generic lines (compact one-liner variants)
    html2, n = re.subn(
        r"<div\b[^>]*abt-card[^>]*>[\s\S]{0,800}?你已经掌握了一些基础知识[\s\S]{0,400}?遇到更复杂的情况还不够用[\s\S]{0,400}?让能力更完整、更系统[\s\S]{0,200}?</div>\s*",
        "",
        html,
        flags=re.I,
    )
    if n:
        actions.append(f"generic_abt_loose×{n}")
        html = html2

    # ABT Fix wrapper leftovers
    html2, n = re.subn(r"<!--\s*ABT Fix\s*-->\s*", "", html, flags=re.I)
    if n:
        actions.append(f"abt_fix_comment×{n}")
        html = html2

    # Template error clinic that reused literacy stroke/idiom errors on unrelated Chinese courses
    html2, n = re.subn(
        r"<div\b[^>]*class=['\"][^'\"]*error-points[^'\"]*['\"][\s\S]*?"
        r"(?:先竖后横的笔顺错误|混淆会意字和形声字|望文生义)[\s\S]*?</div>\s*",
        "",
        html,
        flags=re.I,
    )
    if n:
        actions.append(f"wrong_char_errors×{n}")
        html = html2

    # Rename harmless CSS comment so residual scanner is clean (keep styles)
    if "/* TeachAny Upgrade:" in html:
        html = html.replace("/* TeachAny Upgrade:", "/* TeachAny UI blocks:")
        actions.append("css_comment_rename")

    html2, changed = fix_nav_outside_body(html)
    if changed:
        actions.append("nav_into_body")
        html = html2

    html2, changed = ensure_screen_hides_inactive(html)
    if changed:
        actions.append("screen_display_none")
        html = html2

    html2, changed = move_hero_img_into_active_screen(html)
    if changed:
        actions.append("hero_img_into_cover")
        html = html2

    # Collapse excessive blank lines created by stripping
    html2 = re.sub(r"\n{4,}", "\n\n\n", html)
    if html2 != html:
        html = html2

    if html == original and not actions:
        return html, []
    return html, actions


def needs_fix(html: str) -> bool:
    if "TeachAny Upgrade" in html:
        return True
    if "你已经掌握了一些基础知识" in html and "遇到更复杂的情况还不够用" in html:
        return True
    if "诊断性反馈 #04 patch" in html:
        return True
    if "<!-- ABT Fix -->" in html:
        return True
    body = re.search(r"<body\b", html, re.I)
    nav = re.search(r"<nav\b", html, re.I)
    if body and nav and nav.start() < body.start():
        return True
    # Mis-templated literacy errors pasted into unrelated Chinese courses
    if any(x in html for x in WRONG_CHAR_ERRORS):
        # keep for stroke-order / char-writing courses where it may be legitimate
        return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*", help="course ids; default=all needing fix")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    if args.ids:
        dirs = [COMMUNITY / i for i in args.ids]
    else:
        dirs = sorted(p for p in COMMUNITY.iterdir() if p.is_dir() and (p / "index.html").exists())

    fixed = skipped = failed = 0
    reports = []
    for d in dirs:
        html_path = d / "index.html"
        if not html_path.exists():
            failed += 1
            continue
        try:
            html = html_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"❌ {d.name}: read fail {e}")
            failed += 1
            continue
        if not needs_fix(html) and "hero-cover-img" not in html:
            skipped += 1
            continue
        # Still try hero/screen fixes even without upgrade junk
        new_html, actions = strip_course(html)
        if not actions:
            skipped += 1
            continue
        if args.dry_run:
            print(f"DRY {d.name}: {', '.join(actions)}")
            fixed += 1
        else:
            # backup once
            bak = d / "index.pre-strip-upgrade.html"
            if not bak.exists():
                bak.write_text(html, encoding="utf-8")
            html_path.write_text(new_html, encoding="utf-8")
            print(f"✅ {d.name}: {', '.join(actions)}  ({len(html)}→{len(new_html)})")
            fixed += 1
        reports.append((d.name, actions))
        if args.limit and fixed >= args.limit:
            break

    print(f"\nDone. fixed={fixed} skipped={skipped} failed={failed}")
    # residual scan
    if not args.dry_run and fixed:
        left = 0
        for d in COMMUNITY.iterdir():
            p = d / "index.html"
            if not p.exists():
                continue
            t = p.read_text(encoding="utf-8", errors="ignore")
            if "TeachAny Upgrade" in t or (
                "你已经掌握了一些基础知识" in t and "遇到更复杂的情况还不够用" in t
            ):
                left += 1
        print(f"Residual still with upgrade/generic-ABT: {left}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
