#!/usr/bin/env python3
"""fix-special-interactions.py — 特化交互层：为课程特有的死函数生成真实实现。

与 fix-dead-buttons.py（通用层）衔接：通用层修完后，剩余的是**课程特化**交互
——生长动画、示意图绘制、拖拽判分、流程演示。这些没法通用，必须按该课件的
DOM 与按钮语义单独写。本脚本抽上下文交给 LLM 生成，注入独立 <script> 块。

上下文抽取：每个缺失函数名在 HTML 中的出现位置 ±1200 字符（含所在容器的
id/class、画布、拖拽区结构），让模型看见它要操作的 DOM。

安全约束（写进 prompt）：只实现列出的函数；只操作页面已有 DOM；禁止
document.write/外部请求/新依赖；函数需幂等可重复点击；拿不准的结构做安全降级
（提示文字），不得静默失败。

用法：
  python3 scripts/fix-special-interactions.py --ids bio-asexual-repro --apply
  python3 scripts/fix-special-interactions.py --from-file /tmp/special-ids.txt --apply
  python3 scripts/fix-special-interactions.py --all --apply
  python3 scripts/fix-special-interactions.py --all --revert
"""
from __future__ import annotations

import argparse
import json
import os
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
INVENTORY = Path("/tmp/onclick-missing.json")

OR_URL = "https://openrouter.ai/api/v1/chat/completions"
OR_KEY = os.environ.get("OPENROUTER_API_KEY", "").strip()
MODEL = os.environ.get("SPECIAL_JS_MODEL", "deepseek/deepseek-chat")

MARK = "ta-special-interactions"
SCRIPT_OPEN = "<script data-ta-special=\"" + MARK + "\">"
TAG = re.compile(r"<[^>]+>")


def call_llm(prompt: str) -> str:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

    s = requests.Session()
    s.mount("https://", HTTPAdapter(max_retries=Retry(
        total=5, connect=5, read=5, backoff_factor=2.0,
        status_forcelist=[429, 500, 502, 503, 504], allowed_methods=["POST"])))
    for attempt in range(5):
        r = s.post(OR_URL, headers={"Authorization": f"Bearer {OR_KEY}",
                                    "Content-Type": "application/json"},
                   json={"model": MODEL,
                         "messages": [{"role": "system", "content": SYS},
                                      {"role": "user", "content": prompt}],
                         # 绘图规范升级后代码体积明显增大（分层构图+标注+动画），
                         # 3000 会把输出截断在代码中间导致整块报废（已踩过）。
                         "temperature": 0.2, "max_tokens": 8000},
                   timeout=(30, 180))
        if r.status_code == 429:
            time.sleep(10 * (attempt + 1))
            continue
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    raise RuntimeError("LLM 调用失败")


SYS = ("你是资深前端工程师，为中小学 HTML 课件补写缺失的交互函数。"
       "只输出一个 <script> 标签包裹的 JavaScript 代码，不要解释。")


def build_prompt(cid: str, html: str, fns: list[dict]) -> str:
    ctxs = []
    seen_spans = []
    for x in fns:
        fn = x["fn"]
        for m in re.finditer(re.escape(fn), html):
            s, e = max(0, m.start() - 1200), min(len(html), m.end() + 600)
            if any(s < pe and e > ps for ps, pe in seen_spans):
                continue
            seen_spans.append((s, e))
            seg = html[s:e]
            ctxs.append(f"### 函数 {fn} 出现处上下文：\n```html\n{seg}\n```")
            break                      # 每个函数取第一处即可，控制 token
    title = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    title = TAG.sub("", title.group(1)).strip() if title else cid
    names = ", ".join(x["fn"] for x in fns)
    return f"""课件「{title}」（id: {cid}）的以下交互函数被按钮引用但从未定义：
{names}

以下是这些函数被引用处的 HTML 上下文（能看到它们要操作的画布、容器、拖拽区）：

{chr(10).join(ctxs)}

请补齐这些函数。硬性要求：
1. 只实现列出的函数（以及它们明显需要的私有辅助函数），不定义清单之外的函数；不覆盖可能已存在的同名函数（先 typeof 检查）。
2. 只操作页面已有 DOM（按上下文里的 id/class 查找）；禁止 document.write、外部请求、alert。
3. 每个函数可重复点击（幂等），再次点击重置或重绘而非叠加。
4. 全部函数包在一个 (function(){{ ... }})(); 里，把函数挂到 window 上。
5. 代码总长度控制在 200 行以内，但绘图质量优先于行数。

绘图/动画质量标准（特别重要，此前出过"圆+一根杆"的敷衍版本，被用户否决）：
6. 画布绘图必须**分层构图**：底层环境（土壤色带/水面/天空渐变）、中层主体（植物或装置，有主干、至少 3~5 片叶子或等效部件）、顶层标注。
7. 每个示意图必须画出**教学关键特征**，例如：扦插→枝条剪口 45° 斜面 + 芽点；嫁接→砧木与接穗的接合线 + 接穗在上方；压条→枝条埋土段 + 该段长出的根系；细胞分裂→细胞核先分裂再形成细胞膜分隔。特征必须在视觉上一眼可辨，不能只画个笼统的植物。
8. **中文标注 ≥3 个**，用 fillText 画在对应部位旁边并带引线（如「剪口」「芽」「砧木」「接穗」「生根」），字号 12~14px，深色。
9. 配色用教学主题色系而非纯黑线稿：植物 #2f7d32 / #4caf50，土壤 #795548 / #8d6e63，水 #1976d2，茎 #6d4c41；线条 lineCap/lineJoin = round。
10. 动画用 requestAnimationFrame 实现，分 ≥3 个阶段（如 种子→破土→长出枝叶），总时长 ≥2.5 秒，阶段间有明确视觉差异；动画结束定格在完整形态。
11. 拖拽判分：按上下文中拖拽项与目标区的实际 data/id 约定实现，结果写入反馈容器；给每个项单独标对错颜色，并统计「x/y 正确」。"""


def extract_js(raw: str) -> str | None:
    """从模型输出提取纯 JS。模型常见三种形态：包 <script> 标签、包代码围栏、裸 JS。"""
    raw = raw.strip()
    # 优先提取第一个完整 <script>…</script>（模型可能多个或外层包一层）
    m = re.search(r"<script[^>]*>([\s\S]*?)</script>", raw)
    if m:
        raw = m.group(1).strip()
    else:
        m = re.search(r"```(?:javascript|js)?\s*([\s\S]*?)```", raw)
        if m:
            raw = m.group(1).strip()
    # 容忍模型在 JS 里写注释提到 script 字样，但不能真出现标签或 doc.write 调用
    if re.search(r"<\s*script\b", raw) or re.search(r"document\s*\.\s*write\s*\(", raw):
        Path("/tmp/special-raw-reject.txt").write_text(raw, encoding="utf-8")
        return None
    return raw or None


def process(cid: str, apply: bool) -> tuple[str, str]:
    f = COMMUNITY / cid / "index.html"
    h = f.read_text(encoding="utf-8", errors="ignore")
    if MARK in h:
        return cid, "SKIP(已注入)"
    rec = next((r for r in json.loads(INVENTORY.read_text(encoding="utf-8"))
                if r["id"] == cid), None)
    if not rec:
        return cid, "SKIP(无清单)"
    fns = [x for x in rec["missing"] if not x["fn"].endswith("DepthCheck")
           and x["fn"] not in {"checkAnswer", "answerTF", "answerQ", "answerPre",
                               "answerPost", "answerQuiz", "goTo", "showTab",
                               "selectOpt"}]
    if not fns:
        return cid, "SKIP(无特化)"
    prompt = build_prompt(cid, h, fns)
    js = extract_js(call_llm(prompt))
    if not js:
        return cid, "LLM-FAIL"
    block = ("\n<!-- 教学交互特化实现：由 fix-special-interactions.py 注入 -->\n"
             + SCRIPT_OPEN + "\n" + js + "\n</script>\n")
    if apply:
        i = h.rfind("</body>")
        f.write_text((h[:i] + block + h[i:]) if i >= 0 else h + block,
                     encoding="utf-8")
    return cid, f"OK({len(fns)} 函数, {len(js)}B)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids")
    ap.add_argument("--from-file")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--revert", action="store_true")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    if not any([a.ids, a.from_file, a.all]):
        ap.error("需指定 --ids / --from-file / --all 之一")

    if a.ids:
        ids = [x.strip() for x in a.ids.split(",") if x.strip()]
    elif a.from_file:
        ids = [l.strip() for l in Path(a.from_file).read_text().splitlines()
               if l.strip() and not l.startswith("#")]
    else:
        inv = json.loads(INVENTORY.read_text(encoding="utf-8"))
        gen = set()
        import collections
        for r in inv:
            for x in r["missing"]:
                if x["fn"].endswith("DepthCheck") or x["fn"] in {
                        "checkAnswer", "answerTF", "answerQ", "answerPre",
                        "answerPost", "answerQuiz", "goTo", "showTab",
                        "selectOpt"}:
                    continue
        ids = [r["id"] for r in inv]

    import concurrent.futures as cf
    results = []
    with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(process, cid, a.apply and not a.revert): cid for cid in ids}
        for fu in cf.as_completed(futs):
            r = fu.result()
            results.append(r)
            print(f"  {r[1]:>20s}  {r[0]}", flush=True)

    bad = [r for r in results if r[1].startswith(("LLM", "ERROR"))]
    print(f"\n完成：{len(results)} 门，失败 {len(bad)}")
    if a.revert:
        n = 0
        for cid in ids:
            f = COMMUNITY / cid / "index.html"
            if not f.is_file():
                continue
            h = f.read_text(encoding="utf-8", errors="ignore")
            new = re.sub(
                r'\n<!-- 教学交互特化实现：由 fix-special-interactions\.py 注入 -->\n'
                r'<script data-ta-special="' + MARK + r'">[\s\S]*?</script>\n', "\n", h)
            if new != h:
                f.write_text(new, encoding="utf-8")
                n += 1
        print(f"回滚 {n} 门")


if __name__ == "__main__":
    main()
