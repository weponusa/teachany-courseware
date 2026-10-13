#!/usr/bin/env python3
"""Reading games TTS: grade 1 uses Edge mp3; grades 2–6 have no TTS."""
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

TTS_PLAY_FN = """
let _ttsAudio=null;
function ttsPlay(kind,btn){
if(_ttsAudio){try{_ttsAudio.pause()}catch(e){}_ttsAudio=null;}
document.querySelectorAll('.tts-btn.playing').forEach(b=>b.classList.remove('playing'));
const a=new Audio('/assets/tts/g1/'+TTS_ID+'/'+state.idx+'-'+kind+'.mp3');
_ttsAudio=a;
if(btn){btn.classList.add('playing');const done=()=>{btn.classList.remove('playing');if(_ttsAudio===a)_ttsAudio=null};a.onended=done;a.onerror=done;}
a.play().catch(()=>{if(btn)btn.classList.remove('playing')});
}
""".strip()

SPEECH_FN_RE = re.compile(r"function ttsSpeak\(text,btn\)\{.*?\n\}\n", re.DOTALL)
PLAY_FN_RE = re.compile(r"let _ttsAudio=null;\nfunction ttsPlay\(kind,btn\)\{.*?\n\}\n", re.DOTALL)
TTS_CSS_RE = re.compile(
    r"\.tts-btn\{display:inline-flex;.*?\}\s*@keyframes tts-pulse\{0%,100%\{transform:scale\(1\)\}50%\{transform:scale\(1\.15\)\}\}\n?",
    re.DOTALL,
)

STORY_BTN = (
    '<button type="button" class="tts-btn" onclick="ttsPlay(\'story\',this)" title="听故事">🔊</button> '
)
Q_BTN = (
    '<button type="button" class="tts-btn" onclick="ttsPlay(\'q\',this)" title="听题目">🔊</button> '
)
STORY_BTN_OLD = re.compile(
    r'<button[^>]*class="tts-btn"[^>]*onclick="ttsSpeak\([^"]*story[^"]*,this\)"[^>]*>🔊</button>\s*'
)
Q_BTN_OLD = re.compile(
    r'<button[^>]*class="tts-btn"[^>]*onclick="ttsSpeak\([^"]*q[^"]*,this\)"[^>]*>🔊</button>\s*'
)
PLAY_BTN_OLD = re.compile(
    r'<button[^>]*class="tts-btn"[^>]*onclick="ttsPlay\([^"]*\)"[^>]*>🔊</button>\s*'
)


def is_g1(path: Path) -> bool:
    return path.name.startswith("g1-")


def strip_tts(text: str) -> str:
    text = TTS_CSS_RE.sub("", text)
    text = SPEECH_FN_RE.sub("", text)
    text = PLAY_FN_RE.sub("", text)
    text = re.sub(r"const TTS_ID='[^']+';\n?", "", text)
    text = STORY_BTN_OLD.sub("", text)
    text = Q_BTN_OLD.sub("", text)
    text = PLAY_BTN_OLD.sub("", text)
    return text


def apply_g1_tts(text: str, game_id: str) -> str:
    text = strip_tts(text)
    if ".tts-btn{" not in text:
        text = text.replace("</style>", TTS_CSS + "\n</style>", 1)

    tts_decl = f"const TTS_ID='{game_id}';\n"
    if "const TTS_ID=" not in text:
        text = text.replace("let state=", tts_decl + "let state=", 1)

    if "function ttsPlay(" not in text:
        text = text.replace("function renderSteps()", TTS_PLAY_FN + "\n\nfunction renderSteps()", 1)
    else:
        text = PLAY_FN_RE.sub(TTS_PLAY_FN + "\n\n", text, count=1)

    story_plain = '<p class="story">${lv.story}</p>'
    story_tts = f'<p class="story">{STORY_BTN}${{lv.story}}</p>'
    q_plain = '<p class="q">${lv.q}</p>'
    q_tts = f'<p class="q">{Q_BTN}${{lv.q}}</p>'

    if story_tts not in text:
        text = text.replace(story_plain, story_tts)
        text = STORY_BTN_OLD.sub(STORY_BTN, text)
    if q_tts not in text:
        text = text.replace(q_plain, q_tts)
        text = Q_BTN_OLD.sub(Q_BTN, text)

    return text


def main() -> None:
    g1 = other = 0
    for path in sorted(ROOT.rglob("*.html")):
        text = path.read_text(encoding="utf-8")
        orig = text
        if is_g1(path):
            text = apply_g1_tts(text, path.stem)
            if text != orig:
                path.write_text(text, encoding="utf-8")
                g1 += 1
        else:
            text = strip_tts(text)
            if text != orig:
                path.write_text(text, encoding="utf-8")
                other += 1
    print(f"Updated {g1} grade-1 games (Edge mp3), stripped TTS from {other} other games")


if __name__ == "__main__":
    main()
