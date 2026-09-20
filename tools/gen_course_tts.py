#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为小学科学课件批量生成分段 TTS（读取每个 <section data-tts data-tts-script>）

为什么单独做：finalize-courseware.py 见到已写好的 audio-playlist 会判定"作者已有音频"而跳过合成，
但新课件其实还没有 mp3。本脚本按 playlist 的 section → mp3 文件名一一对应落盘，保证连续播放器可用。

用法：python3 tools/gen_course_tts.py community/sci-e-buoyancy [more...]
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

SKILL_SCRIPTS = Path("/Users/wepon/.workbuddy/skills/teachany/scripts")


def load_engine():
    spec = importlib.util.spec_from_file_location("tts_engine", SKILL_SCRIPTS / "tts-engine.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(dirs):
    eng = load_engine()
    for d in dirs:
        d = Path(d)
        html = (d / "index.html").read_text(encoding="utf-8")
        blocks = re.findall(r'<section\b[^>]*?data-tts="([^"]+)"[^>]*?>', html, re.I)
        scripts = {}
        for m in re.finditer(r'<section\b([^>]*?)>', html, re.I | re.S):
            attrs = m.group(1)
            t = re.search(r'data-tts="([^"]+)"', attrs)
            s = re.search(r'data-tts-script="([^"]+)"', attrs)
            if t and s:
                scripts[t.group(1)] = s.group(1)

        if not (d / "tts").is_dir():
            (d / "tts").mkdir(parents=True, exist_ok=True)
        manifest = []
        ok_n = 0
        for i, sec in enumerate(blocks, 1):
            text = scripts.get(sec)
            if not text:
                print(f"  ⚠️  {sec} 缺 data-tts-script，跳过")
                continue
            out = d / "tts" / f"s{i:02d}-{sec}.mp3"
            if out.exists() and out.stat().st_size >= 5 * 1024:
                ok_n += 1
            else:
                ok, engine = eng.synthesize(text=text, voice="zh-CN-XiaoxiaoNeural", output=str(out))
                if not ok:
                    print(f"  ❌ {out.name} 合成失败")
                    continue
                ok_n += 1
            manifest.append({
                "id": f"s{i:02d}-{sec}",
                "section": sec,
                "src": f"./tts/{out.name}",
                "bytes": out.stat().st_size,
            })
        (d / "tts" / "manifest.json").write_text(
            json.dumps({"course_id": d.name, "count": len(manifest), "items": manifest},
                       ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ {d.name}: {ok_n}/{len(blocks)} 段音频就绪，manifest 已写")


if __name__ == "__main__":
    main(sys.argv[1:])
