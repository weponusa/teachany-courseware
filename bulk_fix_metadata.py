#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TeachAny 元数据批量修复（与内容增强管线并行安全：只改 manifest.json，不碰 index.html）。

对 community/ 下每个课件：
  1. 补 teachany_version（从 HTML <title> 的 TeachAny vX.Y.Z 提取，缺省 7.14.1）
  2. 补 feedback：批量初始化以“教师暂缓启用”方式写入合法对象
     （require_password=false, teacher_declined=true），不伪造真实课堂口令；
     教师后续可用 set-feedback-password.py 设置真实口令。
幂等：已满足则跳过。
"""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMUNITY = ROOT / "community"
DEFAULT_VERSION = "7.14.1"


def main():
    n_ver = 0; n_fb = 0; n_skip = 0; n_total = 0
    for d in sorted(COMMUNITY.iterdir()):
        mf = d / "manifest.json"
        if not mf.exists():
            continue
        n_total += 1
        try:
            m = json.loads(mf.read_text(encoding="utf-8"))
        except Exception:
            continue
        changed = False
        # teachany_version
        if not m.get("teachany_version"):
            ver = DEFAULT_VERSION
            hp = d / "index.html"
            if hp.exists():
                t = re.search(r"TeachAny\s*v([\d.]+)", hp.read_text(encoding="utf-8", errors="ignore"))
                if t:
                    ver = t.group(1)
            m["teachany_version"] = ver
            n_ver += 1; changed = True
        # feedback
        fb = m.get("feedback")
        valid = isinstance(fb, dict) and (
            (fb.get("teacher_declined") is True and fb.get("require_password") is False)
            or (isinstance(fb.get("password_sha256"), str)
                and re.fullmatch(r"[a-f0-9]{64}", fb["password_sha256"])
                and fb.get("require_password") is True)
        )
        if not valid:
            m["feedback"] = {
                "require_password": False,
                "teacher_declined": True,
                "note": "批量初始化：教师可后续用 set-feedback-password.py 设置真实课堂口令",
            }
            n_fb += 1; changed = True
        if changed:
            mf.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        else:
            n_skip += 1
    print(f"元数据批量修复完成：total={n_total} 补teachany_version={n_ver} 补feedback={n_fb} 已满足跳过={n_skip}")


if __name__ == "__main__":
    main()
