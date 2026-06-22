#!/usr/bin/env python3
"""道法/心理 32 门课件质量全检：安全无字插图 + 内容加长 + TTS 同步 + OCR 抽检。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    batch = ROOT / "scripts" / "batch-pol-psych-samples.py"
    print("▶ 质量全检：32 门刷新 + 全量插图 + TTS + 基线")
    r = subprocess.run(
        [sys.executable, str(batch), "--quality-pass"],
        cwd=ROOT,
    )
    if r.returncode != 0:
        return r.returncode
    print("\n▶ OCR 抽检 96 张插图")
    audit = ROOT / "reports" / "pol-psych-agnes-audit-latest.json"
    r2 = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "scan-agnes-image-text.py"), "--out", str(audit)],
        cwd=ROOT,
    )
    return r2.returncode


if __name__ == "__main__":
    raise SystemExit(main())
