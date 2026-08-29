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
MODEL = os.environ.get("FIG_MODEL", "anthropic/claude-3.5-sonnet")

PROMPT = """你是专业的教学插图设计师（中国{stage}{subject}教材插图风格）。
请为课件《{title}》重绘一张**精细的专业教学示意图**，主题：{caption}

参考内容：
{current}

输出：只返回一个 JSON（无 markdown 围栏）：{{"svg": "<svg viewBox=\\"0 0 640 420\\" ...>...</svg>"}}

## 精细度要求（关键，必须达标）
- **图元总数 45~110 个**（rect/circle/ellipse/line/polyline/polygon/path/text 合计），不要画火柴棍简图
- 必须分层：
  1. 背景层：整体底板 rect + 可选浅色分区底色/网格线（rgba(148,163,184,.08)）
  2. 主体层：核心结构，用渐变填充（见下）+ 2px 描边 + 圆角
  3. 细节层：内部构件、纹理、方向箭头（带 marker-end）、关键节点圆点
  4. 标注层：引线（细实线 + 端点小圆点）+ 中文标注 + 必要的数据/公式标注
  5. 图例层：右下角或底部图例框（rect + 小色块 + 说明文字）
- **必须使用渐变**：在 <defs> 中定义 2-4 个 <linearGradient>，用 url(#id) 引用填充
- **必须使用箭头**：<defs><marker id="ar" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#fbbf24"/></marker></defs>，连线用 marker-end="url(#ar)"
- 文字：font-size 12-16，fill #e2e8f0；关键术语用 #fbbf24；数据用 #7dd3fc
- 尺寸：viewBox="0 0 640 420"，元素坐标分布在整个画布，不要挤在一角
- 配色（暗色底 #0a1520）：主色 #3b82f6 蓝 / #34d399 绿 / #f59e0b 橙 / #ef4444 红 / #a78bfa 紫，
  填充用半透明（.25~.35），描边用亮色，文字 #e2e8f0

## 禁止
- 不要写 <style> 标签、不要 class、不要 width/height 属性（只用 viewBox）
- 不要让文字重叠（标注引线要错开）
- 不要简化成 3-5 个图形了事

## 示例结构（仅示意分层思路，图形请按主题原创）
<svg viewBox="0 0 640 420" xmlns="http://www.w3.org/2000/svg">
<defs>
  <linearGradient id="g1" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#3b82f6" stop-opacity=".45"/><stop offset="100%" stop-color="#3b82f6" stop-opacity=".15"/>
  </linearGradient>
  <marker id="ar" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#fbbf24"/></marker>
</defs>
<rect x="0" y="0" width="640" height="420" fill="#0a1520"/>
... 主体、细节、引线标注、图例 ...
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
