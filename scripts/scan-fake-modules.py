#!/usr/bin/env python3
"""扫描 51 个 shell 课件（46 bio-h + 5 it-h）的假模块现状，输出 JSON 供替换器使用。
提取：标题、interactive-model 变量名、deep-understanding 五镜头文本、
pretest/concept-check 是否模板题、TTS playlist 中 interactive-model 段。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

FAKE_QUIZ_MARKERS = [
    "是否只要说出名词定义就够了",
    "只要背出",
    "定义就是答案",
    "定义足够",
]
FIVE_LENS_TEMPLATE = [
    "先描述题干现象或数据变化",
    "区分结构、过程、变量和层级",
    "用机制说明为什么会这样",
    "换情境预测结果并给证据",
]


def scan(cid: str) -> dict:
    p = COMMUNITY / cid / "index.html"
    html = p.read_text(encoding="utf-8", errors="replace")
    m = re.search(r'<h1[^>]*>([\s\S]{0,120}?)</h1>', html)
    title = re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else cid

    # interactive-model 变量名（"拖动滑块模拟 X 的改变"）
    im = re.search(r'id="interactive-model"[\s\S]{0,2000}?拖动滑块模拟\s*([^<]{2,80}?)\s*的改变', html)
    variables = im.group(1).strip() if im else ""
    has_fake_canvas = "bioCanvas" in html or "系统响应曲线" in html

    # 五镜头是否纯模板
    dm = re.search(r'id="deep-understanding"[\s\S]*?</section>', html)
    five_lens_fake = bool(dm) and sum(1 for t in FIVE_LENS_TEMPLATE if t in dm.group(0)) >= 3

    # pretest / concept-check 是否模板判断题
    pm = re.search(r'id="pretest"[\s\S]*?</section>', html)
    cm = re.search(r'id="concept-check"[\s\S]*?</section>', html)
    pretest_fake = bool(pm) and any(t in pm.group(0) for t in FAKE_QUIZ_MARKERS)
    concept_fake = bool(cm) and any(t in cm.group(0) for t in FAKE_QUIZ_MARKERS)

    # core-concept 课标点 + 过程模型假图
    kp = len(re.findall(r'<strong>课标点\s*\d</strong>', html))
    has_fake_fig = bool(re.search(r'ta-standard-figure[^>]*>[\s\S]{0,300}?过程模型', html))

    # lesson-focus 真内容补丁是否已打
    has_depth = 'id="lesson-focus"' in html

    return {
        "cid": cid, "title": title, "variables": variables,
        "fake_canvas": has_fake_canvas, "five_lens_fake": five_lens_fake,
        "pretest_fake": pretest_fake, "concept_fake": concept_fake,
        "kebiaodian_cards": kp, "fake_process_fig": has_fake_fig,
        "has_depth_patch": has_depth,
    }


def main():
    out = {}
    for f in sorted(COMMUNITY.glob("*/index.html")):
        cid = f.parent.name
        if not (cid.startswith("bio-h-") or cid.startswith("it-h-")):
            continue
        html = f.read_text(encoding="utf-8", errors="replace")
        if 'id="interactive-model"' not in html:
            continue
        out[cid] = scan(cid)
    dst = ROOT / "scripts" / "fake-modules-scan.json"
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    # 汇总
    n = len(out)
    agg = {k: sum(1 for v in out.values() if v[k]) for k in
           ("fake_canvas", "five_lens_fake", "pretest_fake", "concept_fake", "fake_process_fig", "has_depth_patch")}
    print(f"扫描 {n} 个课件 → {dst}")
    print(json.dumps(agg, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
