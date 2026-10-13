#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量升级老引擎课件（teachany_version <= 5.99）：
1. 规范化 manifest 元信息（基于 index.html 真实内容回填 lines/interactions/theories/duration/updated/title）
2. 升级 teachany_version -> 7.14.1，version 递增
仅修改 manifest.json，绝不改动 index.html（保证不破坏页面结构）。
"""
import json, os, re, sys
from datetime import date

ROOT = "/Users/wepon/CodeBuddy/一次函数/teachany-courseware/community"
TODAY = date.today().isoformat()
TARGET_TV = "7.14.1"

def load_manifest(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"  [WARN] manifest 解析失败 {path}: {e}")
        return {}

def scan_index(html):
    lines = html.count("\n") + 1
    sections = html.count("<section")
    quiz_cards = len(re.findall(r'class="quiz-card"', html))
    onclick = len(re.findall(r'onclick=', html))
    # 交互特征探测
    feats = ["chain-builder", "drag", "drop", "simulat", "interactive", "slider",
             "flip", "match", "sort", "paint", "draw", "quiz", "fill", "tab-"]
    extra = sum(1 for ft in feats if ft in html.lower())
    interactions = max(quiz_cards, onclick // 2) + (1 if extra > 0 else 0)
    # 理论/拓展深度标记
    deep_marks = ["拓展", "深入", "本质", "为什么", "思考", "启示", "规律", "原理"]
    theories = sum(1 for m in deep_marks if m in html)
    # 估算时长（分钟）
    duration = max(8, sections * 3 + quiz_cards)
    return dict(lines=lines, sections=sections, quiz=quiz_cards,
                interactions=interactions, theories=theories, duration=duration)

def bump_version(v):
    if not v:
        return "2.0.0"
    parts = re.findall(r"\d+", v)
    if len(parts) >= 3:
        parts[2] = str(int(parts[2]) + 1)
    elif len(parts) == 2:
        parts.append("0")
    elif len(parts) == 1:
        parts = [parts[0], "0", "1"]
    else:
        return "2.0.0"
    return ".".join(parts)

def main():
    done, skip = 0, 0
    for d in sorted(os.listdir(ROOT)):
        dp = os.path.join(ROOT, d)
        mpath = os.path.join(dp, "manifest.json")
        ipath = os.path.join(dp, "index.html")
        if not os.path.isdir(dp) or not os.path.isfile(mpath):
            continue
        m = load_manifest(mpath)
        tv = str(m.get("teachany_version", ""))
        # 判定为老引擎：数值 <=6.99 或显式 6.x/v6 等旧标识
        legacy = False
        try:
            tvf = float(tv)
            legacy = tvf <= 6.99
        except Exception:
            if re.search(r"6\.", tv) or tv.strip().lower() in ("6.x", "v6", "6", ""):
                legacy = True
        if not legacy:
            continue  # 仅处理老引擎
        if not os.path.isfile(ipath):
            print(f"[SKIP] {d}: 无 index.html")
            skip += 1
            continue
        with open(ipath, encoding="utf-8") as f:
            html = f.read()
        metrics = scan_index(html)
        # 回填元信息
        m["teachany_version"] = TARGET_TV
        m["version"] = bump_version(m.get("version"))
        m["lines"] = metrics["lines"]
        m["interactions"] = metrics["interactions"]
        m["theories"] = metrics["theories"]
        m["duration"] = f"约 {metrics['duration']} 分钟"
        m["updated"] = TODAY
        # 缺 title 时从 index.html <title> 提取
        if not m.get("title"):
            mt = re.search(r"<title>(.*?)</title>", html)
            if mt:
                m["title"] = mt.group(1).split(" · ")[0].strip()
        # 写回（保持缩进）
        with open(mpath, "w", encoding="utf-8") as f:
            json.dump(m, f, ensure_ascii=False, indent=2)
        done += 1
        if done % 30 == 0:
            print(f"  ... 已处理 {done} 个")
    print(f"\n完成：升级 {done} 个老引擎课件，跳过 {skip} 个。")

if __name__ == "__main__":
    main()
