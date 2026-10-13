#!/usr/bin/env python3
"""Sync locally refined reading games into reading-academy for read.teachany.cn."""
from __future__ import annotations

import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("/Users/wepon/CodeBuddy/小学语文阅读互动助手/阅读互动助手")
DEST = ROOT / "reading-academy"
SCENES_SRC = SOURCE / "assets" / "generated-scenes"
SCENES_DST = DEST / "assets" / "generated-scenes"

# 6/17 批量精修课文（本地已生成，待上线）
REFINED_GAMES = [
    "games/lessons/g1-a-l028-66fb8c36.html",
    "games/lessons/g1-a-l033-dc055a9c.html",
    "games/lessons/g1-b-l024-68146f69.html",
    "games/lessons/g2-b-l028-d5fd3e5b.html",
    "games/lessons/g3-a-l001-dcb1154f.html",
    "games/lessons/g3-a-l017-c98877e0.html",
    "games/lessons/g3-a-l019-d303b09b.html",
    "games/lessons/g3-b-l006-b60f8d32.html",
    "games/lessons/g3-b-l011-3f6794ee.html",
    "games/lessons/g3-b-l016-0fcaf3f1.html",
    "games/lessons/g3-b-l020-6a7eef46.html",
    "games/lessons/g3-b-l023-6080fc4c.html",
    "games/lessons/g4-a-l006-31c685b5.html",
    "games/lessons/g4-a-l018-227df44b.html",
    "games/lessons/g4-b-l009-7cc0452d.html",
    "games/lessons/g4-b-l015-711be642.html",
    "games/lessons/g5-a-l017-541a43da.html",
    "games/lessons/g1-b-l023-24138909.html",
    "games/lessons/g2-a-l012-24138909.html",
    "games/lessons/g2-a-l023-24138909.html",
    "games/lessons/g5-a-l021-047245e5.html",
    "games/lessons/g6-a-l017-41e07cfa.html",
    "games/lessons/g3-b-l027-7959c51b.html",
    "games/lessons/g6-b-l014-fbe6c721.html",
]

STAGE_CSS = (
    ".stage{position:relative;width:100%;aspect-ratio:16/10;border-radius:16px;"
    "overflow:hidden;border:1px solid var(--line);background:#111831;margin-bottom:15px}"
    ".stage img{width:100%;height:100%;object-fit:cover;display:block}"
    ".stage .loading{position:absolute;inset:0;display:grid;place-items:center;"
    "color:var(--muted);background:linear-gradient(135deg,rgba(255,255,255,.04),"
    "rgba(0,0,0,.18));text-align:center;padding:20px}"
)

SCENE_ERR_FN = """
function onSceneImgError(img){
const loading=img.previousElementSibling;
const prompt=decodeURIComponent(img.dataset.imgPrompt||'')||'reading scene';
(async()=>{try{img.src=await agnesImage(prompt)}catch(e){if(loading)loading.textContent='插画加载失败，继续答题吧～'}})();
}
""".strip()

RENDER_LEVEL_IMG = (
    "const hasImg=lv.image||lv.img;"
    "let imgHtml='';"
    "if(hasImg){"
    "const imgSrc=(lv.image||'').replace(/^\\.\\.\\/\\.\\.\\//,'/');"
    "imgHtml='<div class=\"stage\"><div class=\"loading\">正在打开阅读插画…</div>"
    "<img alt=\"场景插画\" src=\"'+imgSrc+'\" data-img-prompt=\"'+encodeURIComponent(lv.img||'')+'\" "
    "onerror=\"onSceneImgError(this)\" onload=\"if(this.previousElementSibling)this.previousElementSibling.remove()\"></div>';"
    "}"
)

RENDER_LEVEL_OLD = re.compile(
    r"function renderLevel\(\)\{renderSteps\(\);scoreBadge\.textContent='积分 '\+state\.score;"
    r"state\.answered=false;const lv=DATA\.levels\[state\.idx\];"
    r"scene\.innerHTML=`"
)

PNG_REF = re.compile(r"generated-scenes/([a-zA-Z0-9_-]+)\.png")


def png_to_webp(png: Path, webp: Path) -> bool:
    webp.parent.mkdir(parents=True, exist_ok=True)
    if shutil.which("cwebp"):
        r = subprocess.run(
            ["cwebp", "-q", "85", "-quiet", str(png), "-o", str(webp)],
            capture_output=True,
            text=True,
        )
        return r.returncode == 0
    try:
        from PIL import Image

        Image.open(png).save(webp, "WEBP", quality=85)
        return True
    except Exception:
        return False


def patch_html(text: str) -> str:
    if ".stage{" not in text:
        text = text.replace(".scene-tag{", STAGE_CSS + ".scene-tag{", 1)

    if "function onSceneImgError(" not in text:
        text = text.replace("function renderSteps()", SCENE_ERR_FN + "\n\nfunction renderSteps()", 1)

    if "const hasImg=lv.image||lv.img" not in text:
        text = RENDER_LEVEL_OLD.sub(
            "function renderLevel(){renderSteps();scoreBadge.textContent='积分 '+state.score;"
            "state.answered=false;const lv=DATA.levels[state.idx];"
            + RENDER_LEVEL_IMG
            + "scene.innerHTML=`",
            text,
            count=1,
        )
        text = text.replace(
            "scene.innerHTML=`<span class=\"scene-tag\">${lv.tag}</span><p class=\"story\">",
            "scene.innerHTML=`<span class=\"scene-tag\">${lv.tag}</span>${imgHtml}<p class=\"story\">",
            1,
        )

    text = re.sub(r"(generated-scenes/[^\"']+)\.png", r"\1.webp", text)
    text = text.replace("../../assets/generated-scenes/", "/assets/generated-scenes/")
    return text


def main() -> None:
    if not SOURCE.is_dir():
        raise SystemExit(f"Source not found: {SOURCE}")

    copied_html = 0
    copied_webp = 0
    missing_png: list[str] = []

    for rel in REFINED_GAMES:
        src_html = SOURCE / rel
        dst_html = DEST / rel
        if not src_html.is_file():
            print(f"⚠️  skip missing source: {rel}")
            continue

        raw = src_html.read_text(encoding="utf-8")
        png_names = sorted(set(PNG_REF.findall(raw)))
        for name in png_names:
            png = SCENES_SRC / f"{name}.png"
            webp = SCENES_DST / f"{name}.webp"
            if not png.is_file():
                missing_png.append(f"{name}.png")
                continue
            if not webp.is_file() or png.stat().st_mtime > webp.stat().st_mtime:
                if png_to_webp(png, webp):
                    copied_webp += 1

        dst_html.parent.mkdir(parents=True, exist_ok=True)
        dst_html.write_text(patch_html(raw), encoding="utf-8")
        copied_html += 1
        print(f"✅ {rel} ({len(png_names)} scenes)")

    print(f"\n📦 Synced {copied_html} games, {copied_webp} new webp images")
    if missing_png:
        print(f"⚠️  missing {len(missing_png)} png files (partial levels may lack art)")


if __name__ == "__main__":
    main()
