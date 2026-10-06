#!/usr/bin/env python3
"""enhance-subject-visuals.py — 各学科通用视觉/互动增强
1. LLM 生成 2-3 张学科概念示意图（内嵌 SVG，矢量精准、零外部依赖）
2. 补 iframe 容器样式（PhET/GeoGebra 可见）
3. 嵌入外部互动（GeoGebra/PhET/国家平台，仅用可信通用链接）
4. 拓展资源卡
5. 删除空白 section
幂等标记：<!-- visuals-v1 -->
用法: python3 enhance-subject-visuals.py <cid>
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
MODEL = os.environ.get("ZH_MODEL", "deepseek/deepseek-chat-v3-0324")

IFRAME_CSS = """.iframe-wrap{position:relative;width:100%;aspect-ratio:16/10;min-height:520px;border-radius:12px;overflow:hidden;border:1px solid rgba(148,163,184,.25);background:rgba(10,21,32,.6)}
.iframe-wrap iframe{position:absolute;inset:0;width:100%;height:100%;border:0;display:block}
.math-fig{display:block;margin:16px auto;max-width:100%;background:rgba(15,29,43,.6);border:1px solid rgba(148,163,184,.2);border-radius:12px}
.external-links{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:14px}
figure.ta-standard-figure{margin:18px 0;text-align:center}figure.ta-standard-figure figcaption{font-size:13px;color:var(--muted);margin-top:8px}"""

# 学科 → 外部互动（仅用经确认的可信通用入口，不编造具体 sim 路径）
LAB = {
    "math": ("https://www.geogebra.org/classic?lang=zh_CN", "GeoGebra 经典版", "GeoGebra：拖动图形验证结论"),
    "phy": ("https://phet.colorado.edu/zh_CN/simulations/physics", "PhET 物理模拟", "PhET：调节参数观察现象"),
    "chem": ("https://phet.colorado.edu/zh_CN/simulations/chemistry", "PhET 化学模拟", "PhET：改变条件看反应"),
    "bio": ("https://phet.colorado.edu/zh_CN/simulations/biology", "PhET 生物模拟", "PhET：观察生命过程"),
    "sci": ("https://phet.colorado.edu/zh_CN/simulations/by-level/elementary-school", "PhET 小学科学", "PhET：动手探究自然现象"),
    "geo": ("https://www.geogebra.org/maps?lang=zh_CN", "GeoGebra 地图", "GeoGebra 地图：空间分布分析"),
    "eng": ("https://basic.smartedu.cn/", "国家中小学智慧教育平台", "平台同步课程与听说资源"),
    "chn": ("https://basic.smartedu.cn/", "国家中小学智慧教育平台", "平台同步课程与阅读资源"),
    "it": ("https://basic.smartedu.cn/", "国家中小学智慧教育平台", "平台信息技术课程资源"),
    "cs": ("https://basic.smartedu.cn/", "国家中小学智慧教育平台", "平台信息科技课程资源"),
}

PROMPT = """你是中国{stage}{subject}教师，也是擅长用 SVG 画教学示意图的设计师。
课件《{title}》需要 3 张内嵌 SVG 概念示意图，帮助学生理解核心概念。

现有精讲内容（据此作图，图示必须与内容一致）：
{current}

严格输出 JSON（不要 markdown 围栏）：
{{
 "figs": [
   {{"caption": "图1 标题（15-25字，说明这张图展示什么）", "svg": "<svg viewBox=\\"0 0 480 320\\" ...>完整SVG代码</svg>"}},
   {{"caption": "图2 标题", "svg": "<svg viewBox=\\"0 0 480 320\\" ...>...</svg>"}},
   {{"caption": "图3 标题", "svg": "<svg viewBox=\\"0 0 480 320\\" ...>...</svg>"}}
 ]
}}

SVG 作图规范（必须遵守）：
1. viewBox 用 "0 0 480 320" 或 "0 0 480 400"，不要写死 width/height；
2. 只使用基础图元：rect/circle/ellipse/line/polyline/polygon/path/text；
3. 配色（暗色底 #0a1520 上）：填充用半透明 rgba(59,130,246,.28) 蓝 / rgba(52,211,153,.28) 绿 / rgba(245,158,11,.25) 橙 / rgba(239,68,68,.22) 红，描边用 #60a5fa/#34d399/#fbbf24/#f87171，文字用 #e2e8f0；
4. 文字用 <text x="" y="" font-size="15" fill="#e2e8f0">，中文标注简洁（2-6字），字号 13-17；
5. 结构清晰：标注关键部位名称、箭头表示过程方向、用不同色区分不同部分；
6. 三张图分别对应：①核心结构/概念全貌 ②关键过程/机制分解 ③典型实例/应用场景；
7. 不要写 <style> 标签内联 class，直接用属性 fill/stroke；
8. 每张图元素数量 8-25 个，不要过于复杂。"""


def llm_json(body, max_tokens=4000):
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps({"model": MODEL,
                                 "messages": [{"role": "user", "content": body}],
                                 "temperature": 0.5, "max_tokens": max_tokens}).encode(),
                headers={"Authorization": f"Bearer {API_KEY}",
                         "Content-Type": "application/json",
                         "HTTP-Referer": "https://teachany.cn",
                         "X-OpenRouter-Title": "visuals"})
            with urllib.request.urlopen(req, timeout=200) as r:
                txt = json.load(r)["choices"][0]["message"]["content"]
            t = re.sub(r"```(?:json)?", "", txt)
            b = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", t[t.find("{"):])
            try:
                obj, _ = json.JSONDecoder().raw_decode(b)
                return obj
            except json.JSONDecodeError:
                return json.loads(re.sub(r",\s*([}\]])", r"\1", b[:b.rfind("}") + 1]))
        except Exception as e:
            last = e
            time.sleep((attempt + 1) * 15)
    raise last


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def process(cid):
    P = ROOT / "community" / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")
    if "<!-- visuals-v1 -->" in html:
        print(f"[{cid}] 已增强")
        return
    subject = cid.split("-")[0]
    grade_map = {"h": "高中", "m": "初中", "e": "小学"}
    stage = grade_map.get(cid.split("-")[1], "初中")

    tm = re.search(r"<title>([^<·《》]+)", html)
    title = tm.group(1).strip()[:40] if tm else cid
    m = re.search(r'id="lesson-focus"[\s\S]*?</section>', html)
    current = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(0))).strip()[:450] if m else title

    print(f"[{cid}] 生成 {subject} 学科示意图（分3次调用）…")
    figs = []
    roles = ["①核心结构/概念全貌", "②关键过程/机制分解", "③典型实例/应用场景"]
    for fi in range(1, 4):
        p2 = PROMPT.format(stage=stage, subject=subject, title=title, current=current).replace(
            "3 张内嵌 SVG 概念示意图", f"1 张内嵌 SVG 概念示意图").replace(
            "三张图分别对应：①核心结构/概念全貌 ②关键过程/机制分解 ③典型实例/应用场景；",
            f"本次只画：{roles[fi-1]}；")
        try:
            g = llm_json(p2, max_tokens=2500)
            f0 = (g.get("figs") or [None])[0]
            if f0 and "</svg>" in f0.get("svg", ""):
                figs.append(f0)
            else:
                print(f"  第{fi}张不完整，跳过")
        except Exception as e:
            print(f"  第{fi}张失败: {e}")

    # 清理 SVG：只保留 svg 标签本体，去掉内联 style
    blocks = []
    for i, f in enumerate(figs):
        svg = f.get("svg", "")
        svg = re.sub(r"<style[\s\S]*?</style>", "", svg)
        svg = re.sub(r'\s(?:class|width|height)="[^"]*"', "", svg, count=3)
        if "<svg" not in svg or "</svg>" not in svg:
            continue  # 丢弃被截断的 SVG
        svg = svg[:svg.rfind("</svg>") + 6]
        blocks.append(
            f'<figure class="ta-standard-figure"><figcaption>{esc(f.get("caption", f"图{i+1}"))}</figcaption>'
            f'<svg class="math-fig" {svg[svg.find("<svg") + 4:]}')
    if not blocks:
        print(f"[{cid}] SVG 生成失败，跳过")
        return

    actions = []
    if ".iframe-wrap" not in html:
        html = html.replace("</style>", IFRAME_CSS + "\n</style>", 1)
        actions.append("iframe样式")

    # SVG 插到精讲后
    mf = re.search(r'(<div class="card focus-detail"><p><strong>易错提醒：</strong>[\s\S]*?</div>)', html)
    if mf:
        html = html[:mf.end()] + "\n" + "\n".join(blocks) + html[mf.end():]
    else:
        html = html.replace("</body>", "\n".join(blocks) + "\n</body>", 1)
    actions.append(f"SVG×{len(blocks)}")

    # 外部互动
    lab_url, lab_name, lab_desc = LAB.get(subject, LAB["math"])
    if "interactive-lab" not in html:
        lab = (f'<section class="section" id="interactive-lab" data-interactive="sim" data-bloom-level="apply" '
               f'data-tts="interactive-lab" data-tsh="互动实验 - {lab_name}">'
               f'<div class="lesson-panel"><span class="phase-tag">Interactive Lab</span>'
               f'<h2>🔬 {lab_name}：{lab_desc}</h2>'
               f'<div class="iframe-wrap"><iframe src="{lab_url}" title="{lab_name}" allowfullscreen loading="lazy" '
               f'sandbox="allow-scripts allow-same-origin allow-forms allow-popups"></iframe></div>'
               f'<p class="feedback" style="margin-top:12px">💡 {lab_desc}，把结论记录到下面的探究区。</p></div></section>')
        mp = re.search(r'<section\b[^>]*id="posttest"', html)
        html = html[:mp.start()] + lab + "\n" + html[mp.start():] if mp else html.replace("</body>", lab + "\n</body>", 1)
        actions.append("外部互动")

    # 拓展资源
    if "拓展资源" not in html:
        links = "".join(
            f'<a class="mini-card" href="{u}" target="_blank" rel="noopener" style="text-decoration:none;color:inherit">'
            f'<strong>{n}</strong><br><span style="font-size:13px;opacity:.85">{d}</span></a>'
            for u, n, d in [LAB.get(subject, LAB["math"]),
                            ("https://basic.smartedu.cn/", "国家中小学智慧教育平台", "同步课程与拓展资源"),
                            ("https://www.geogebra.org/classic?lang=zh_CN", "GeoGebra 经典版", "在线作图与数学实验")])
        card = (f'<div class="card" style="border-left:4px solid #a78bfa;"><h3 style="margin:0 0 10px;">🔗 拓展资源</h3>'
                f'<div class="external-links">{links}</div></div>')
        mp2 = re.search(r'<section\b[^>]*id="posttest"', html)
        html = html[:mp2.start()] + card + "\n" + html[mp2.start():] if mp2 else html.replace("</body>", card + "\n</body>", 1)
        actions.append("拓展资源")

    # 删空白 section
    parts = re.split(r'(<section\b[^>]*>[\s\S]*?</section>)', html)
    out, ch = [], False
    for seg in parts:
        if re.match(r"^<section\b", seg or ""):
            body = re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", seg))
            if len(body) < 5 and not any(k in seg for k in ("<img", "<canvas", "<svg", "<iframe")):
                ch = True
                continue
        out.append(seg)
    html = "".join(out)
    if ch:
        actions.append("删空白")

    html = html.replace("</body>", "<!-- visuals-v1 -->\n</body>", 1)
    P.write_text(html, encoding="utf-8")
    print(f"[{cid}] 增强完成: {'、'.join(actions)}")


if __name__ == "__main__":
    process(sys.argv[1])
