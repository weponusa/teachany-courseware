#!/usr/bin/env python3
"""add-figures.py — 为缺少示意图的课件新增高质量 SVG（深色科技风 + SMIL 动画）

与 redraw-figures.py 的区别：后者「重绘」已有 figure，本脚本「新增」——
面向完全无示意图（或示意图不足）的课件，从正文提取真实知识点后生成。

生成 3 张，分别对应教学逻辑的三个层次：
  1. 核心结构图 → 插到 lesson-focus（知识精讲）之后
  2. 机制分解图 → 插到 lesson-method（方法）之后
  3. 典型实例图 → 插到 worked-example / deep-understanding 之后

每张均带 SMIL 动画（<animate>/<animateTransform>），零 JS 依赖即可动，
同时挂 class="math-fig" 以接入 interactive-kit 的分步高亮。

用法: python3 add-figures.py <cid> [cid2 ...]
      python3 add-figures.py --dry <cid>      只生成不写入
      python3 add-figures.py --limit N        限制每课件生成张数（默认3）
"""
import base64
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
MODEL = os.environ.get("FIG_MODEL", "anthropic/claude-sonnet-4")

SLOTS = [
    ("lesson-focus", "核心结构图", "core"),
    ("lesson-method", "机制分解图", "method"),
    ("worked-example", "典型实例图", "example"),
]

PROMPT = """你是专业的教学插图设计师（中国{stage}{subject}教材插图风格）。
请为课件《{title}》绘制一张**精细的专业教学示意图**。

用途：{role}
对应正文内容：
{context}

输出：只返回一个 JSON（无 markdown 围栏）：{{"svg": "<svg viewBox=\\"0 0 640 420\\" ...>...</svg>", "caption": "图题（12-24字，说明这张图展示什么）"}}

## 视觉风格（深色科技风信息图，严格遵循）
- 暗色底板 #0a1520，外层圆角容器：rect rx=8 fill=rgba(148,163,184,.07) stroke=#334155
- 五色功能体系，每种配 linearGradient（上浓 .25 → 下淡 .10）：
    #3b82f6 蓝=结构体   #f59e0b 橙=运动/变化   #ef4444 红=能量/热源
    #34d399 绿=控制/条件 #a78bfa 紫=连接/传动
- 填充用半透明，描边比填充亮 1~2 级（fill #3b82f6/.25 → stroke #60a5fa），stroke-width 1.5~2.5
- 引线：rgba(100,116,139,.7) 细实线 + 端点圆点 (r=3, fill=#7dd3fc)
- 文字：关键术语 #fbbf24，普通标注 #e2e8f0，数据 #7dd3fc；标题 14-16 bold，标注 12-13
- 右下角半透明图例框 rgba(15,23,42,.7) + #334155 边框 + 小色块 + 说明

## 分层（5 层都要有实质内容）
1. 背景：底板 + 外框容器 + 极淡网格
2. 主体：核心大形（渐变填充 + 亮色描边 + rx=8~12 圆角）
3. 细节：内部构件、运动方向（弧线 path + marker-end 箭头）、关键节点 circle
4. 标注：引线 + 中文标注，引线不交叉、文字不重叠
5. 图例：图例框 + 公式/结论

## 动画要求（重要，必须包含）
用 SMIL 让图"活"起来，至少包含 2 类：
1. **流动虚线**（表示方向/流程）：
   <path ... stroke="#7dd3fc" stroke-dasharray="7 5" fill="none">
     <animate attributeName="stroke-dashoffset" from="24" to="0" dur="1.2s" repeatCount="indefinite"/>
   </path>
2. **渐显入场**（元素依次出现，begin 递增如 0s/0.15s/0.3s…）：
   <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.15s" fill="freeze"/>
3. 可选：**呼吸脉动**（关键节点）：
   <animate attributeName="opacity" values="1;0.45;1" dur="1.8s" repeatCount="indefinite"/>
   **往复运动**（活塞/指针等）：
   <animateTransform attributeName="transform" type="translate" values="0 0; 0 -18; 0 0" dur="2.4s" repeatCount="indefinite"/>

## 技术约束
- viewBox="0 0 640 420"；元素铺满画布（x 20~620, y 20~400），不要挤在一角
- 图元总数 35~90（rect/circle/ellipse/line/polyline/polygon/path/text 合计）
- 箭头必须定义 marker：
  <defs><marker id="ar" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto">
  <path d="M0,0 L0,6 L9,3 z" fill="#fbbf24"/></marker></defs>
- 不要 <style>、不要 width/height、不要 class 属性
- 不要简化成 3~5 个图形了事"""


def parse_svg_json(txt):
    """容错解析：优先按 JSON，失败则直接从文本里抠 <svg>

    模型偶尔不按 JSON 返回（直接输出 SVG 或带前后说明文字），
    硬解析 JSON 会导致整张图丢失，故加兜底。
    """
    t = re.sub(r"```(?:json|svg)?", "", txt)
    # 1) JSON 路径
    i = t.find("{")
    if i >= 0:
        b = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", t[i:])
        try:
            obj, _ = json.JSONDecoder().raw_decode(b)
            if obj.get("svg"):
                return obj
        except json.JSONDecodeError:
            try:
                obj = json.loads(re.sub(r",\s*([}\]])", r"\1", b[:b.rfind("}") + 1]))
                if obj.get("svg"):
                    return obj
            except Exception:
                pass
    # 2) 兜底：直接抠 SVG
    m = re.search(r"<svg[\s\S]*?</svg>", t)
    if m:
        cap = re.search(r'"caption"\s*:\s*"([^"]{4,40})"', t)
        return {"svg": m.group(0), "caption": cap.group(1) if cap else ""}
    raise ValueError("响应中未找到 SVG")


def llm_json(body, max_tokens=6000):
    last = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps({"model": MODEL, "messages": [{"role": "user", "content": body}],
                                 "temperature": 0.55, "max_tokens": max_tokens}).encode(),
                headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json",
                         "HTTP-Referer": "https://teachany.cn", "X-OpenRouter-Title": "add-figures"})
            with urllib.request.urlopen(req, timeout=280) as r:
                txt = json.load(r)["choices"][0]["message"]["content"]
            return parse_svg_json(txt)
        except ValueError as e:
            # 解析类错误：换一次生成（温度不变，重试即可）
            last = e
            time.sleep((attempt + 1) * 8)
        except Exception as e:
            last = e
            time.sleep((attempt + 1) * 12)
    raise last


ELEM = r"<(?:rect|circle|ellipse|line|polyline|polygon|path|text)\b"


def section_text(html, sid):
    """提取指定 id 的 section 内的纯文本"""
    m = re.search(rf'<section\b[^>]*\bid="{re.escape(sid)}"[^>]*>([\s\S]*?)</section>', html)
    if not m:
        return ""
    t = re.sub(r"<[^>]+>", " ", m.group(1))
    return re.sub(r"\s+", " ", t).strip()


def process(cid, dry=False, limit=3, min_figs=2):
    P = COMMUNITY / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")

    # 已有足够示意图则跳过，避免重复生成
    have = len(re.findall(r'<figure class="ta-standard-figure"', html))
    if have >= min_figs:
        print(f"[{cid}] 已有 {have} 张示意图，跳过")
        return 0

    subject = cid.split("-")[0]
    stage = {"h": "高中", "m": "初中", "e": "小学"}.get(cid.split("-")[1], "初中")
    tm = re.search(r"<title>([^<·《》]+)", html)
    title = tm.group(1).strip()[:40] if tm else cid

    added = 0
    # 由后往前插，避免位置偏移
    for sid, role, _key in reversed(SLOTS[:limit]):
        m = re.search(rf'(<section\b[^>]*\bid="{re.escape(sid)}"[^>]*>)', html)
        if not m:
            continue
        # 该 section 的结束位置
        end = html.find("</section>", m.end())
        if end < 0:
            continue
        ctx = section_text(html, sid) or section_text(html, "lesson-focus") or title
        if len(ctx) < 30:
            ctx = title
        print(f"[{cid}] 生成「{role}」…", flush=True)
        try:
            g = llm_json(PROMPT.format(stage=stage, subject=subject, title=title,
                                       role=role, context=ctx[:600]))
            svg = g.get("svg", "")
            caption = (g.get("caption") or role).strip()[:40]
            svg = re.sub(r"<style[\s\S]*?</style>", "", svg)
            if "<svg" not in svg or "</svg>" not in svg:
                print("   输出不完整，跳过")
                continue
            svg = svg[svg.find("<svg"):svg.rfind("</svg>") + 6]
            svg = re.sub(r'^(\s*<svg)(?![^>]*\bclass=)', r'\1 class="math-fig"', svg, count=1)
            n = len(re.findall(ELEM, svg))
            if n < 30:
                print(f"   仅 {n} 图元，未达精细度，跳过")
                continue
            anim = len(re.findall(r"<animate", svg))
            fig = (f'\n<figure class="ta-standard-figure"><figcaption>{caption}</figcaption>'
                   f'{svg}</figure>\n')
            html = html[:end + 10] + fig + html[end + 10:]
            added += 1
            print(f"   ✅ {n} 图元 / {anim} 动画")
        except Exception as e:
            print(f"   失败: {str(e)[:60]}")

    if added and not dry:
        P.write_text(html, encoding="utf-8")
    return added


def main():
    dry = "--dry" in sys.argv
    limit = 3
    for a in sys.argv[1:]:
        if a.startswith("--limit="):
            limit = int(a.split("=", 1)[1])
    cids = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not cids:
        print("用法: python3 add-figures.py <cid> [cid2 ...]")
        return 1
    if not API_KEY:
        print("需要 OPENROUTER_API_KEY 环境变量")
        return 1
    # 多课件并发（每个课件内部仍是串行生成各张图）
    import concurrent.futures as cf
    workers = 6
    for a in sys.argv[1:]:
        if a.startswith("--workers="):
            workers = int(a.split("=", 1)[1])
    tot = 0
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(process, c, dry, limit): c for c in cids}
        for f in cf.as_completed(futs):
            cid = futs[f]
            try:
                tot += f.result()
            except Exception as e:
                print(f"[{cid}] 异常: {str(e)[:80]}")
    print(f"\n共新增 {tot} 张示意图（处理 {len(cids)} 个课件）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
