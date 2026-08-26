#!/usr/bin/env python3
"""scan-fake-modules-v2.py — 全库假模块/无信息量模块扫描器（v2）
在 v1（canvas/课标点/假图/五镜头/前测/概念/后测）基础上新增：
- worked-example 通用步骤空话（"第一步，识别输入变量"等）
- tiered-practice 空话（"说出本课一个定义"）
- transfer-task 通用脚手架
- error-diagnosis 通用错因模板
- application-scene 通用 SVG 图
输出：JSON 明细 + 按问题类型的课件分布统计
用法: python3 scan-fake-modules-v2.py [--verbose]
"""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

SIGNATURES = {
    # 假 canvas：通用正弦曲线
    "canvas_fake": [r"系统响应曲线", r"输出指标", r"function drawModel\(", r"function drawBio\(",
                    r"getElementById\('bioCanvas'\)", r"getElementById\('modelCanvas'\)"],
    # 课标点（教材目录复制）
    "kebiaodian": [r">课标点\s*\d<"],
    # 假过程模型四步图
    "process_fig": [r"ta-standard-figure[\s\S]{0,1500}?观察现象[\s\S]{0,500}?建立模型"],
    # 五镜头空话（两种模板）
    "lens_fake": [r"先描述题干现象或数据变化", r"题目给了什么输入和现象？",
                  r"变量、规则、结构分别是什么？", r"换一个场景还能不能用？"],
    # 前测/概念/后测模板题
    "pretest_fake": [r"只背名词就够了", r"记住定义，不用解释过程", r"结论与证据无关也行"],
    "concept_fake": [r"只要记住定义，就一定能解决", r"定义就是全部", r"只要代码能运行就行"],
    "posttest_fake": [r"一个完整答案最应该包含什么", r"只写一段代码"],
    # worked-example 通用步骤空话
    "worked_fake": [r"第一步，识别输入变量", r"第一步，把现象拆成变量",
                    r"第二步，写出处理规则，说明程序如何把输入转化成",
                    r"第三步，用一个具体数据检验结果是否合理"],
    # tiered-practice 空话
    "practice_fake": [r"说出本课一个定义", r"分析一个校园系统变量", r"设计并验证一个方案",
                      r"画出一个变量关系", r"解释一个真实案例"],
    # transfer-task 通用脚手架（关键词计数检查器）
    "transfer_fake": [r"至少写出三个部分：数据从哪里来，规则如何处理",
                      r"提交后会检查是否包含变量、规则和结果"],
    # error-diagnosis 通用错因（无任何学科内容的模板句）
    "error_fake": [r"只看表面现象，没有追问机制和证据链", r"把定义换成变量、机制和证据链"],
    # application-scene 通用 SVG 插图（process-diagram/application-scene.svg 占位）
    "appscene_svg": [r"assets/process-diagram\.svg", r"assets/application-scene\.svg"],
}

# 五镜头真内容标记（已修复课件含此标记，避免误报）
FIXED_MARK = "<!-- text-modules-fixed -->"
CANVAS_FIXED = "TeachAnyModelLab"


def scan(cid, html):
    hits = {}
    for key, pats in SIGNATURES.items():
        n = 0
        for pat in pats:
            n += len(re.findall(pat, html))
        if n:
            hits[key] = n
    # 已修复标记：假 canvas 已换真引擎后 drawModel 等不应再出现；五镜头已换后不应有空话
    return hits


def main():
    rows = []
    by_issue = defaultdict(list)
    for f in sorted(COMMUNITY.glob("*/index.html")):
        cid = f.parent.name
        html = f.read_text(encoding="utf-8", errors="replace")
        hits = scan(cid, html)
        if hits:
            rows.append({"id": cid, "hits": hits,
                         "canvas_fixed": CANVAS_FIXED in html, "text_fixed": FIXED_MARK in html})
            for k in hits:
                by_issue[k].append(cid)
    print(f"扫描 {len(list(COMMUNITY.glob('*/index.html')))} 个课件，{len(rows)} 个含疑似假模块\n")
    print("=== 按问题类型分布 ===")
    for k, ids in sorted(by_issue.items(), key=lambda x: -len(x[1])):
        print(f"{k:16s} {len(ids):4d} 个课件")
    out = ROOT / "scripts" / "fake-modules-scan-v2.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n明细 → {out}")
    # 学科前缀分布
    pref = defaultdict(int)
    for r in rows:
        pref[r["id"].split("-")[0] + "-" + (r["id"].split("-")[1] if "-" in r["id"] else "")] += 1
    print("\n=== 课件前缀分布（前 15）===")
    for k, v in sorted(pref.items(), key=lambda x: -x[1])[:15]:
        print(f"{k:14s} {v}")


if __name__ == "__main__":
    main()
