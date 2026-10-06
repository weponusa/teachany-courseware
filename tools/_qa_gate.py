#!/usr/bin/env python3
"""官方质检闸门：改动课件前后跑 scripts/validate-courseware.py，错误变多就回滚。

为什么需要
----------
pre-push 钩子会对**每个变更课件**跑 validate-courseware.py，任何 error 都会拒绝 push。
批量脚本（去重/拆页）一旦把某门课的既有 error 引入出来（或让错误变多），
整批 push 就会被卡住。把这个校验放进脚本里做「逐课闸门」，就能安全批处理。

用法（在工具里）:
    from _qa_gate import qa_errors, apply_guarded
    errs, msgs = qa_errors(cid)
    ok, why = apply_guarded(path, new_html, cid)   # ok=False 时会自动恢复原文件
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / 'scripts' / 'validate-courseware.py'


def qa_errors(cid: str) -> tuple[int, list[str]]:
    """返回 (错误条数, 错误消息列表)。校验器不可用时返回 (-1, [...])。"""
    if not VALIDATOR.is_file():
        return -1, ['validator missing']
    try:
        out = subprocess.run([sys.executable, str(VALIDATOR), cid],
                             cwd=str(ROOT), capture_output=True, text=True, timeout=120)
    except Exception as e:  # noqa: BLE001
        return -1, [str(e)[:80]]
    text = (out.stdout or '') + (out.stderr or '')
    m = re.search(r'❌ 错误:\s*(\d+)', text)
    n = int(m.group(1)) if m else -1
    msgs = []
    if n > 0:
        # 取错误段落里的条目行
        seg = text.split('❌ 错误:', 1)[-1].split('⚠ 警告', 1)[0]
        msgs = [ln.strip() for ln in seg.splitlines() if ln.strip().startswith(cid)]
    return n, msgs


def imbalance(html: str) -> int:
    """标签不平衡度（差值绝对值之和）。用于挡住「插标记插坏结构」这类改动。"""
    bad = 0
    for t in ('section', 'div', 'figure', 'article', 'header', 'footer'):
        o = len(re.findall(r'<%s\b' % t, html))
        c = len(re.findall(r'</%s>' % t, html))
        bad += abs(o - c)
    return bad


def apply_guarded(path: Path, new_html: str, cid: str) -> tuple[bool, str]:
    """写入前先量错误数，写入后复量；不允许错误增加。"""
    before, _ = qa_errors(cid)
    if before < 0:
        return False, 'validator 不可用，拒绝写入'
    orig = path.read_text(encoding='utf-8')
    if imbalance(new_html) > imbalance(orig):
        return False, f'结构平衡变差（{imbalance(orig)}→{imbalance(new_html)}），拒绝写入'
    try:
        path.write_text(new_html, encoding='utf-8')
        after, msgs = qa_errors(cid)
        if after > before:
            path.write_text(orig, encoding='utf-8')
            return False, f'质检错误 {before}→{after}，已回滚（{msgs[:1]}）'
        return True, f'质检 {before}→{after}'
    except Exception as e:  # noqa: BLE001
        path.write_text(orig, encoding='utf-8')
        return False, f'写入异常已回滚: {str(e)[:80]}'
