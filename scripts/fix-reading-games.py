#!/usr/bin/env python3
"""Fix reading-academy games: webp paths, TTS buttons, and onclick scope."""
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
const prompt=decodeURIComponent(img.dataset.fallbackPrompt||'')||'reading scene';
(async()=>{try{img.src=await agnesImage(prompt)}catch(e){if(loading)loading.textContent='插画加载失败，继续答题吧～'}})();
}
""".strip()


def fix_render_level(text: str) -> str:
    text = re.sub(
        r'onerror="\(async\(\)=>\{try\{this\.src=await agnesImage\(lv\.img\|\|\'reading scene\'\)[^"]*"\)',
        'onerror="onSceneImgError(this)"',
        text,
    )
    text = re.sub(
        r'(data-fallback-prompt="\$\{encodeURIComponent\(lv\.img\|\|\\\'\\\'\'\)\}"\s*)+',
        'data-fallback-prompt="${encodeURIComponent(lv.img||\'\')}" ',
        text,
    )
    if 'data-fallback-prompt="${encodeURIComponent(lv.img' not in text:
        text = re.sub(
            r'(<img alt="场景插画" src="\$\{lv\.image\|\|\'\'\}")',
            r'\1 data-fallback-prompt="${encodeURIComponent(lv.img||\'\')}"',
            text,
        )

    story_plain = '<p class="story">${lv.story}</p>'
    story_tts = (
        '<p class="story"><button type="button" class="tts-btn" '
        'onclick="ttsSpeak(DATA.levels[state.idx].story,this)" title="听故事">🔊</button> ${lv.story}</p>'
    )
    q_plain = '<p class="q">${lv.q}</p>'
    q_tts = (
        '<p class="q"><button type="button" class="tts-btn" '
        'onclick="ttsSpeak(DATA.levels[state.idx].q,this)" title="听题目">🔊</button> ${lv.q}</p>'
    )

    if story_plain in text and story_tts not in text:
        text = text.replace(story_plain, story_tts)
    if q_plain in text and q_tts not in text:
        text = text.replace(q_plain, q_tts)

    text = text.replace(
        'onclick="ttsSpeak(lv.story,this)"',
        'onclick="ttsSpeak(DATA.levels[state.idx].story,this)"',
    )
    text = text.replace(
        'onclick="ttsSpeak(lv.q,this)"',
        'onclick="ttsSpeak(DATA.levels[state.idx].q,this)"',
    )
    return text


def main() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("*.html")):
        text = path.read_text(encoding="utf-8")
        orig = text

        text = text.replace("generated-scenes/", "generated-scenes/")  # noop anchor
        text = re.sub(
            r"(generated-scenes/[^\"']+)\.png",
            r"\1.webp",
            text,
        )

        if ".tts-btn{" not in text:
            text = text.replace("</style>", TTS_CSS + "\n</style>", 1)

        if "function ttsSpeak(" not in text:
            anchor = "function renderSteps()"
            if anchor in text:
                text = text.replace(anchor, TTS_FN + "\n\n" + anchor, 1)
        else:
            text = re.sub(
                r"function ttsSpeak\(text,btn\)\{.*?\n\}\n",
                TTS_FN + "\n\n",
                text,
                count=1,
                flags=re.DOTALL,
            )

        if "function onSceneImgError(" not in text:
            anchor = "function renderSteps()"
            if anchor in text:
                text = text.replace(anchor, SCENE_ERR_FN + "\n\n" + anchor, 1)

        text = fix_render_level(text)

        if text != orig:
            path.write_text(text, encoding="utf-8")
            changed += 1

    print(f"Updated {changed} game HTML files under {ROOT}")


if __name__ == "__main__":
    main()
