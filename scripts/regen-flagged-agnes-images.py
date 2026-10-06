#!/usr/bin/env python3
"""定向重生成 OCR/目视 flagged 的 Agnes 插图（使用 -v3 配额桶）。"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGNES = ROOT / "scripts" / "agnes-image-gen.py"
DELAY = 8

# 额外强无字 prompt（避免 infographics 带标题/书法伪字）
PROMPT_OVERRIDES: dict[str, str] = {
    "pol-m-g7-lo-u1-hero": (
        "Chinese seventh graders and young counselor sitting in circle on sunny school courtyard, "
        "talking about emotions, trees and orange school building background, "
        "no blackboards no posters no signs, warm orange flat illustration, empty surfaces only, "
        "NO text NO letters NO numbers NO Chinese characters NO labels"
    ),
    "pol-m-g7-lo-u2-section2": (
        "Three Chinese teens in school uniforms showing confidence and teamwork, "
        "abstract icons for growth and support, warm orange flat illustration, "
        "NO text NO letters NO numbers NO Chinese characters NO labels NO captions NO typography"
    ),
    "pol-m-g7-lo-u3-hero": (
        "Chinese seventh graders enjoying traditional culture festival: music dance paper cutting, "
        "warm courtyard scene, NO calligraphy NO brush writing NO characters on paper, "
        "NO text NO letters NO numbers NO labels flat educational illustration"
    ),
    "pol-m-g7-up-u1-section2": (
        "Teens taking small daily steps toward dreams, stepping stones path metaphor, "
        "warm orange civic education flat art, purely visual NO text NO letters NO words NO labels"
    ),
    "psych-m-g9-mental-health-section2": (
        "School mental health support network: counselor student peers helping, "
        "teal friendly flat illustration, NO headlines NO banners NO text NO letters NO words"
    ),
}
TARGETS: list[tuple[str, str]] = [
    ("pol-m-g7-lo-u2", "section2"),
    ("pol-m-g7-lo-u3", "hero"),
    ("pol-m-g7-up-u1", "section2"),
    ("psych-m-g9-mental-health", "section2"),
]

# 首轮已处理 12 张（见 git 历史 / audit-before → after）
_LEGACY_TARGETS: list[tuple[str, str]] = [
    ("pol-m-g7-lo-u1", "section2"),
    ("pol-m-g7-lo-u2", "section2"),
    ("pol-m-g7-lo-u3", "hero"),
    ("pol-m-g7-up-u1", "section2"),
    ("pol-m-g7-up-u3", "section2"),
    ("pol-m-g8-up-u2", "section2"),
    ("pol-m-g9-up-u3", "section2"),
    ("psych-m-g8-puberty-relation", "section2"),
    ("psych-m-g8-stress-coping", "section1"),
    ("psych-m-g8-stress-coping", "section2"),
    ("psych-m-g9-mental-health", "section1"),
    ("psych-m-g9-mental-health", "section2"),
]


def load_batch():
    spec = importlib.util.spec_from_file_location("batch", ROOT / "scripts/batch-pol-psych-samples.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def pick_v3(course_id: str) -> str:
    for n in range(3, 12):
        aid = f"{course_id}-v{n + 1}"
        proc = subprocess.run(
            [sys.executable, str(AGNES), "--course-id", aid, "--quota"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        try:
            rem = int(json.loads(proc.stdout)["course"].get("remaining", 0))
            if rem > 0:
                return aid
        except Exception:
            pass
    return f"{course_id}-v10"


def main() -> int:
    batch = load_batch()
    courses = {c["course_id"]: c for c in batch.load_all_tree_courses()}
    ok = fail = 0
    for i, (cid, slot) in enumerate(TARGETS):
        c = courses.get(cid)
        if not c:
            print(f"SKIP {cid}: no course def")
            fail += 1
            continue
        agnes_id = pick_v3(cid)
        key = f"{cid}-{slot}"
        if key in PROMPT_OVERRIDES:
            prompt = PROMPT_OVERRIDES[key] + batch.AGNES_NO_TEXT
        else:
            prompt = batch.agnes_prompt(c["agnes"][slot])
        out = ROOT / "community" / cid / "assets" / f"{cid}-{slot}.png"
        print(f"\n[{i+1}/{len(TARGETS)}] {cid}-{slot} via {agnes_id}")
        if i > 0:
            time.sleep(DELAY)
        r = subprocess.run(
            [
                sys.executable,
                str(AGNES),
                "--course-id",
                agnes_id,
                "--prompt",
                prompt,
                "--out",
                str(out),
                "--slot",
                slot,
            ]
        )
        if r.returncode == 0:
            ok += 1
            print(f"  ✅ {out.name}")
        else:
            fail += 1
            print(f"  ❌ failed")
    print(f"\n完成 ok={ok} fail={fail}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
