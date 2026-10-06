#!/usr/bin/env python3
"""Pre-generate Edge TTS mp3 for grade-1 reading-academy games."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAMES = ROOT / "reading-academy" / "games"
OUT = ROOT / "reading-academy" / "assets" / "tts" / "g1"
ENGINE = ROOT / "scripts" / "tts-engine.py"
VOICE = "zh-CN-XiaoyiNeural"
DATA_RE = re.compile(r"const DATA=(\{.*?\});\s*(?:const TTS_ID='[^']+';\s*)?let state=", re.DOTALL)


def parse_data(html: str) -> dict | None:
    m = DATA_RE.search(html)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def synthesize(text: str, output: Path) -> bool:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and output.stat().st_size >= 200:
        return True
    r = subprocess.run(
        [
            sys.executable,
            str(ENGINE),
            "--text",
            text.strip(),
            "--voice",
            VOICE,
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
    )
    return r.returncode == 0 and output.exists() and output.stat().st_size >= 200


def main() -> None:
    if not ENGINE.exists():
        print(f"Missing {ENGINE}", file=sys.stderr)
        sys.exit(1)

    tasks: list[tuple[str, int, str, str, Path]] = []
    for path in sorted(GAMES.rglob("g1-*.html")):
        game_id = path.stem
        data = parse_data(path.read_text(encoding="utf-8"))
        if not data:
            print(f"skip (no DATA): {path.relative_to(ROOT)}")
            continue
        for idx, level in enumerate(data.get("levels") or []):
            for kind in ("story", "q"):
                text = (level.get(kind) or "").strip()
                if not text:
                    continue
                out = OUT / game_id / f"{idx}-{kind}.mp3"
                tasks.append((game_id, idx, kind, text, out))

    ok = skip = fail = 0
    manifest: dict[str, list[dict[str, str | int]]] = {}
    workers = min(6, max(1, len(tasks) // 20))

    def run(task: tuple[str, int, str, str, Path]) -> tuple[str, int, str, str, Path, str]:
        game_id, idx, kind, text, out = task
        if out.exists() and out.stat().st_size >= 200:
            return game_id, idx, kind, text, out, "skip"
        return game_id, idx, kind, text, out, "ok" if synthesize(text, out) else "fail"

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(run, t) for t in tasks]
        for fut in as_completed(futures):
            game_id, idx, kind, text, out, status = fut.result()
            if status == "skip":
                skip += 1
            elif status == "ok":
                ok += 1
            else:
                fail += 1
                print(f"FAIL {out.relative_to(ROOT)}")
            manifest.setdefault(game_id, []).append(
                {"level": idx, "kind": kind, "file": out.relative_to(ROOT).as_posix(), "text": text}
            )

    manifest_path = OUT / "manifest.json"
    OUT.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps({"voice": VOICE, "engine": "edge-tts", "games": manifest}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Done: {ok} generated, {skip} skipped, {fail} failed, {len(tasks)} total clips")


if __name__ == "__main__":
    main()
