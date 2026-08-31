#!/usr/bin/env python3
"""tag-slots.py — 给课件顶层模块打 data-slot 标签

对每个顶层 section：按 module-slots 识别规则确定槽位，
在开标签上写入 data-slot="NN"（已有则更新）。
未识别的模块原样保留并报告。

用法:
  python3 tag-slots.py <cid> [cid...]      打标
  python3 tag-slots.py --audit [limit]     只审计（报告未识别，不写入）
"""
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

_spec = importlib.util.spec_from_file_location(
    "shell", ROOT / "scripts" / "apply-courseware-shell.py")
SHELL = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(SHELL)

_spec2 = importlib.util.spec_from_file_location(
    "slots", ROOT / "scripts" / "module-slots.py")
SLOTS = importlib.util.module_from_spec(_spec2)
_spec2.loader.exec_module(SLOTS)


def analyze(html):
    """返回 [(slot, open_tag_start, open_tag_end, sid, title, new_tag)]"""
    out = []
    for s, e, a, b in SHELL.sections(html, top_only=True):
        sid = (re.search(r'id="([^"]+)"', a) or [None, ""])[1]
        cls = (re.search(r'class="([^"]+)"', a) or [None, ""])[1]
        title = SHELL.title_of(a, b) or ""
        text_len = SHELL.text_len(b)
        body_text = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', b))[:60]
        slot = SLOTS.slot_of(sid, cls, title, text_len, body_text)
        if slot is None:
            # 归 None 的模块若已有 data-slot（规则更新前的旧标），移除之
            if re.search(r'\sdata-slot="[^"]*"', a):
                new_tag = '<section' + re.sub(r'\sdata-slot="[^"]*"', '', a) + '>'
                gt = html.find(">", s) + 1
                out.append(('REMOVE', s, gt, sid, title[:20], new_tag))
            else:
                out.append((None, None, None, sid, title[:20], None))
            continue
        # 构造新开标签。注意：SHELL.sections 返回的 a 只是「属性部分」
        # （<section 与 > 之间的内容），不含前缀 <section 与后缀 > ——
        # 曾误用 a[:-1] 拼标签，导致全库开标签被截断（已回滚）。
        if re.search(r'\sdata-slot="[^"]*"', a):
            new_tag = '<section' + re.sub(
                r'\sdata-slot="[^"]*"', f' data-slot="{slot}"', a) + '>'
        else:
            new_tag = f'<section{a} data-slot="{slot}">'
        gt = html.find(">", s) + 1      # 开标签结束位置
        out.append((slot, s, gt, sid, title[:20], new_tag))
    return out


def process(cid, audit=False):
    p = COMMUNITY / cid / "index.html"
    html = p.read_text(encoding="utf-8", errors="replace")
    mods = analyze(html)
    unknown = [(sid, t) for s, _, _, sid, t, _ in mods if s is None]
    if audit:
        return len(mods) - len(unknown), len(unknown), unknown
    changed = 0
    # 逆序替换避免位置偏移
    for slot, s, gt, sid, t, new_tag in reversed(mods):
        if slot is None or new_tag is None:
            continue
        old_tag = html[s:gt]
        if old_tag != new_tag:
            html = html[:s] + new_tag + html[gt:]
            changed += 1
    if changed:
        p.write_text(html, encoding="utf-8")
    return changed, len(unknown), unknown


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    audit = "--audit" in sys.argv
    limit = int(args[0]) if audit and args else 20

    if audit:
        total_u = 0
        samples = []
        files = sorted(COMMUNITY.iterdir())
        for d in files:
            if not (d / "index.html").is_file():
                continue
            _, n, unk = process(d.name, audit=True)
            total_u += n
            if unk and len(samples) < limit:
                samples.append((d.name, unk))
        print(f"未识别模块共 {total_u} 个。样本:")
        for cid, unk in samples:
            for sid, t in unk[:2]:
                print(f"  {cid}: id={sid or '·'} 标题={t}")
        return

    if not args:
        print("用法: python3 tag-slots.py <cid> [cid...] | --audit [limit]")
        return
    for cid in args:
        try:
            changed, nu, unk = process(cid)
            mark = f"打标{changed}个" if changed else "已标齐"
            warn = f" ⚠️未识别{nu}个" if nu else ""
            print(f"{cid}: {mark}{warn}")
        except Exception as e:
            print(f"  ❌ {cid}: {str(e)[:70]}")


if __name__ == "__main__":
    main()
