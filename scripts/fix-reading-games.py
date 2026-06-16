#!/usr/bin/env python3
"""Fix reading-academy games: asset paths, TTS, and renderLevel image markup."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "reading-academy" / "games"

TTS_CSS = (
    ".tts-btn{display:inline-flex;align-items:center;justify-content:center;width:32px;height:32px;"
    "border-radius:50%;border:1.5px solid var(--gold);background:rgba(231,198,107,.12);color:var(--gold);"
    "cursor:pointer;font-size:16px;vertical-align:middle;margin-left:6px;transition:all .2s;flex-shrink:0}"
    ".tts-btn:hover{background:rgba(231,198,107,.25);transform:scale(1.1)}"
    ".tts-btn.playing{animation:tts-pulse 1s infinite;background:rgba(231,198,107,.3)}"
    "@keyframes tts-pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.15)}}"
)

TTS_FN = """
function ttsSpeak(text,btn){
if(!window.speechSynthesis)return;
window.speechSynthesis.cancel();
document.querySelectorAll('.tts-btn.playing').forEach(b=>b.classList.remove('playing'));
const u=new SpeechSynthesisUtterance(text);
u.lang='zh-CN';u.rate=0.82;u.pitch=1.1;
const pick=()=>{const zh=speechSynthesis.getVoices().filter(v=>v.lang.startsWith('zh'));if(zh.length)u.voice=zh[0];};
pick();if(!speechSynthesis.getVoices().length)speechSynthesis.onvoiceschanged=pick;
if(btn){btn.classList.add('playing');u.onend=()=>btn.classList.remove('playing');u.onerror=()=>btn.classList.remove('playing')}
speechSynthesis.speak(u);
}
""".strip()

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

    story_plain = "<p class=\"story\">${lv.story}</p>"
    story_tts = (
        '<p class="story"><button type="button" class="tts-btn" '
        'onclick="ttsSpeak(DATA.levels[state.idx].story,this)" title="听故事">🔊</button> ${lv.story}</p>'
    )
    q_plain = "<p class=\"q\">${lv.q}</p>"
    q_tts = (
        '<p class="q"><button type="button" class="tts-btn" '
        'onclick="ttsSpeak(DATA.levels[state.idx].q,this)" title="听题目">🔊</button> ${lv.q}</p>'
    )

    if story_plain in text and story_tts not in text:
        text = text.replace(story_plain, story_tts)
    if q_plain in text and q_tts not in text:
        text = text.replace(q_plain, q_tts)

    text = text.replace('onclick="ttsSpeak(lv.story,this)"', 'onclick="ttsSpeak(DATA.levels[state.idx].story,this)"')
    text = text.replace('onclick="ttsSpeak(lv.q,this)"', 'onclick="ttsSpeak(DATA.levels[state.idx].q,this)"')
    return text


def main() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("*.html")):
        text = path.read_text(encoding="utf-8")
        orig = text

        text = re.sub(r"(generated-scenes/[^\"']+)\.png", r"\1.webp", text)
        text = text.replace("../../assets/generated-scenes/", "/assets/generated-scenes/")

        if ".tts-btn{" not in text:
            text = text.replace("</style>", TTS_CSS + "\n</style>", 1)

        if "function ttsSpeak(" not in text:
            text = text.replace("function renderSteps()", TTS_FN + "\n\nfunction renderSteps()", 1)
        else:
            text = re.sub(r"function ttsSpeak\(text,btn\)\{.*?\n\}\n", TTS_FN + "\n\n", text, count=1, flags=re.DOTALL)

        if "function onSceneImgError(" not in text:
            text = text.replace("function renderSteps()", SCENE_ERR_FN + "\n\nfunction renderSteps()", 1)

        text = fix_render_level(text)

        if text != orig:
            path.write_text(text, encoding="utf-8")
            changed += 1

    print(f"Updated {changed} game HTML files under {ROOT}")


if __name__ == "__main__":
    main()
