#!/usr/bin/env python3
"""向后兼容入口：请使用 build-cn-pol-psych-trees.py。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    script = Path(__file__).resolve().parent / "build-cn-pol-psych-trees.py"
    raise SystemExit(subprocess.call([sys.executable, str(script)]))
