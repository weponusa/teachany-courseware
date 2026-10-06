#!/usr/bin/env python3
"""Fix reading-academy games: asset paths, TTS, and renderLevel image markup."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "reading-academy" / "games"

SCENE_ERR_FN = """
function onSceneImgError(img){
const loading=img.previousElementSibling;
const prompt=decodeURIComponent(img.dataset.imgPrompt||'')||'reading scene';
(async()=>{try{img.src=await agnesImage(prompt)}catch(e){if(loading)loading.textContent='插画加载失败，继续答题吧～'}})();
}
""".strip()

# Safe renderLevel image block (no nested template literals — avoids SyntaxError in HTML)
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

RENDER_LEVEL_IMG_RE = re.compile(
    r"const hasImg=lv\.image\|\|lv\.img;const imgHtml=hasImg\?`[^`]*`:'';",
)


def fix_render_level(text: str) -> str:
    text = RENDER_LEVEL_IMG_RE.sub(RENDER_LEVEL_IMG, text)

    return text


def main() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("*.html")):
        text = path.read_text(encoding="utf-8")
        orig = text

        text = re.sub(r"(generated-scenes/[^\"']+)\.png", r"\1.webp", text)
        text = text.replace("../../assets/generated-scenes/", "/assets/generated-scenes/")

        if "function onSceneImgError(" not in text:
            text = text.replace("function renderSteps()", SCENE_ERR_FN + "\n\nfunction renderSteps()", 1)

        text = fix_render_level(text)

        if text != orig:
            path.write_text(text, encoding="utf-8")
            changed += 1

    print(f"Updated {changed} game HTML files under {ROOT}")


if __name__ == "__main__":
    main()
