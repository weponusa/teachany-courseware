#!/usr/bin/env python3
"""redraw-figures.py — 重绘课件示意图为精细版（分图层/渐变/引线标注/图例）
保留原 caption 主题，替换为更精细的 SVG。
用法: python3 redraw-figures.py <cid> [fig_index...]  不传索引则重绘全部
"""
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_KEY = os.environ["OPENROUTER_API_KEY"]
MODEL = os.environ.get("FIG_MODEL", "anthropic/claude-sonnet-4")

PROMPT = """你是专业的教学插图设计师（中国{stage}{subject}教材插图风格）。
请为课件《{title}》重绘一张**精细的专业教学示意图**，主题：{caption}

参考内容：
{current}

输出：只返回一个 JSON（无 markdown 围栏）：{{"svg": "<svg viewBox=\\"0 0 640 420\\" ...>...</svg>"}}

## 视觉风格规范（严格遵循）
整体风格类似「深色科技风教学信息图」：
- 暗色背景底板（#0a1520），外层有浅灰半透明边框圆角容器
- 用 4~5 种功能色区分不同部件/概念：蓝色系(#3b82f6)结构体、橙色系(#f59e0b)运动件、红色系(#ef4444)热/力源、绿色系(#34d399)控制/阀门、紫色系(#a78bfa)传动/连接
- 每种颜色配一个 linearGradient（上浓下淡，stop-opacity .25→.10），用于填充主要形状
- 描边比填充亮 1~2 级（如 fill=#3b82f6/.25 → stroke=#60a5fa），stroke-width 1.5~2.5
- 引线统一用 rgba(100,116,139,.7) 细实线，端点带小圆点(r=3, fill=#7dd3fc)
- 关键术语文字用 #fbbf24 黄色高亮，普通标注用 #e2e8f0 浅白，数据/数值用 #7dd3fc 青色
- 右下角或底部放半透明图例框（rgba(15,23,42,.7)+#334155 边框），内含小色块+说明

## 分层要求（5 层，每层都要有实质内容）
1. 背景层：<rect x="0" y="0" fill="#0a1520"/> + 外框容器(rect rx=8, fill=rgba(148,163,184,.07), stroke=#334155)
   + 可选极淡网格线辅助定位
2. 主体层：核心大形（矩形/圆形/多边形）用渐变填充+亮色描边+圆角(rx=8~12)，表示主要结构
3. 细节层：内部构件（小矩形/线条/圆点），表示零件、接口、运动方向
   - 运动方向用弧线 path + marker-end 箭头
   - 关键节点用 circle(r=4~6) 高亮
4. 标注层：引线(line + 端点circle) + text 标注，引线从目标指向文字，不交叉
5. 图例/公式层：图例框 + 公式结论文字

## 箭头定义（必须在 defs 中）
<marker id="ar" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto">
  <path d="M0,0 L0,6 L9,3 z" fill="#fbbf24"/>
</marker>
连线用 marker-end="url(#ar)" 或 stroke="#7dd3fc" 的箭头

## 技术约束
- viewBox="0 0 640 420"，元素铺满整个画布（x:20~620, y:20~400），不要挤在左上角
- 图元总数 35~90 个（rect/circle/ellipse/line/polyline/polygon/path/text 合计）
- font-size: 标题14-16 bold, 标注12-13, 图例12
- 不要 <style>, 不要 class(除 math-fig), 不要 width/height, 只要 viewBox
- 文字绝对不能重叠，引线要错开

## 示例（四冲程内燃机图的分层结构参考，请按你的主题原创图形）
<svg viewBox="0 0 640 420" xmlns="http://www.w3.org/2000/svg">
<defs>
  <linearGradient id="g1" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#3b82f6" stop-opacity=".3"/><stop offset="100%" stop-color="#3b82f6" stop-opacity=".1"/>
  </linearGradient>
  <linearGradient id="g2" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#f59e0b" stop-opacity=".3"/><stop offset="100%" stop-color="#f59e0b" stop-opacity=".1"/>
  </linearGradient>
  <linearGradient id="g3" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#ef4444" stop-opacity=".3"/><stop offset="100%" stop-color="#ef4444" stop-opacity=".1"/>
  </linearGradient>
  <marker id="ar" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto">
    <path d="M0,0 L0,6 L9,3 z" fill="#fbbf24"/>
  </marker>
</defs>
<!-- 背景层 -->
<rect x="0" y="0" fill="#0a1520"/>
<rect x="20" y="20" height="380" rx="8" fill="rgba(148,163,184,.08)" stroke="#334155" stroke-width="1"/>
<!-- 主体层 -->
<rect x="100" y="100" width="200" height="200" rx="10" fill="url(#g1)" stroke="#3b82f6" stroke-width="2"/>
<!-- 细节层 -->
<rect x="150" y="120" width="100" height="160" fill="rgba(203,213,225,.1)" stroke="#64748b" stroke-width="1"/>
<rect x="155" y="180" width="90" height="30" rx="4" fill="url(#g2)" stroke="#f59e0b" stroke-width="2"/>
<circle cx="200" cy="250" r="12" fill="url(#g3)" stroke="#ef4444" stroke-width="2"/>
<path d="M200 250 Q 240 270 280 250" stroke="#7dd3fc" stroke-width="2" fill="none" marker-end="url(#ar)"/>
<!-- 标注层 -->
<line x1="80" y1="150" x2="145" y2="150" stroke="#64748b" stroke-width="1"/>
<circle cx="80" cy="150" r="3" fill="#7dd3fc"/>
<text x="60" y="145" font-size="12" fill="#e2e8f0">吸气阀</text>
<!-- 图例层 -->
<rect x="400" y="300" width="180" height="80" rx="5" fill="rgba(30,41,59,.7)" stroke="#334155" stroke-width="1"/>
<text x="420" y="320" font-size="14" fill="#e2e8f0" font-weight="bold">图例标题</text>
<rect x="420" y="330" width="12" height="12" fill="#3b82f6" rx="2"/>
<text x="440" y="340" font-size="12" fill="#e2e8f0">部件名称</text>
</svg>"""


def llm_json(body, max_tokens=6000):
    last = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps({"model": MODEL, "messages": [{"role": "user", "content": body}],
                                 "temperature": 0.55, "max_tokens": max_tokens}).encode(),
                headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json",
                         "HTTP-Referer": "https://teachany.cn", "X-OpenRouter-Title": "figures"})
            with urllib.request.urlopen(req, timeout=280) as r:
                txt = json.load(r)["choices"][0]["message"]["content"]
            t = re.sub(r"```(?:json|svg)?", "", txt)
            b = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", t[t.find("{"):])
            try:
                obj, _ = json.JSONDecoder().raw_decode(b)
                return obj
            except json.JSONDecodeError:
                return json.loads(re.sub(r",\s*([}\]])", r"\1", b[:b.rfind("}") + 1]))
        except Exception as e:
            last = e
            time.sleep((attempt + 1) * 12)
    raise last


ELEM = r"<(?:rect|circle|ellipse|line|polyline|polygon|path|text)\b"


def process(cid, only=None):
    P = ROOT / "community" / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")
    subject = cid.split("-")[0]
    stage = {"h": "高中", "m": "初中", "e": "小学"}.get(cid.split("-")[1], "初中")
    tm = re.search(r"<title>([^<·《》]+)", html)
    title = tm.group(1).strip()[:40] if tm else cid
    m = re.search(r'id="lesson-focus"[\s\S]*?</section>', html)
    current = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(0))).strip()[:400] if m else title

    figs = list(re.finditer(r'(<figure class="ta-standard-figure">\s*<figcaption>)([^<]*)(</figcaption>)(<svg\b[^>]*>[\s\S]*?</svg>)', html))
    if not figs:
        print(f"[{cid}] 无示意图")
        return
    idxs = only or range(len(figs))
    done = 0
    for i in sorted(idxs, reverse=True):
        if i >= len(figs):
            continue
        f = figs[i]
        caption = f.group(2).strip()
        old_svg = f.group(4)
        old_n = len(re.findall(ELEM, old_svg))
        print(f"[{cid}] 重绘图{i+1}「{caption}」(原{old_n}图元)…", flush=True)
        try:
            g = llm_json(PROMPT.format(stage=stage, subject=subject, title=title, caption=caption, current=current))
            svg = g.get("svg", "")
            svg = re.sub(r"<style[\s\S]*?</style>", "", svg)
            svg = re.sub(r'\s(?:class|width|height)="[^"]*"', "", svg, count=3)
            if "<svg" not in svg or "</svg>" not in svg:
                print("   输出不完整，保留原图")
                continue
            svg = svg[:svg.rfind("</svg>") + 6]
            if not svg.strip().startswith("<svg"):
                svg = svg[svg.find("<svg"):]
            # 保留 math-fig class（否则丢失样式与动画挂钩）
            if "math-fig" not in svg[:200]:
                svg = re.sub(r"^(\s*<svg)(?![^>]*\bclass=)", r'\1 class="math-fig"', svg, count=1)
            n = len(re.findall(ELEM, svg))
            if n < 30:
                print(f"   新图仅{n}图元，未达精细度，保留原图")
                continue
            html = html[:f.start(4)] + svg + html[f.end(4):]
            done += 1
            print(f"   ✅ {old_n} → {n} 图元")
        except Exception as e:
            print(f"   失败: {str(e)[:60]}")
    if done:
        P.write_text(html, encoding="utf-8")
        print(f"[{cid}] 重绘完成 {done} 张")
    else:
        print(f"[{cid}] 无图被替换")


if __name__ == "__main__":
    cid = sys.argv[1]
    only = [int(x) - 1 for x in sys.argv[2:]] or None
    process(cid, only)
