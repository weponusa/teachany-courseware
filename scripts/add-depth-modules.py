#!/usr/bin/env python3
"""add-depth-modules.py — L5/L1 深度补齐：深层理解 / 随堂小测 / 正文加厚。

对应新权重下剩余的三类缺陷（2026-10-10 审计）：
  NO_INSIGHT   51 门  缺深层理解模块（slot 70）            -14 分/门
  NO_QUIZ      24 门  缺随堂测验/选择题（slot 80）         -4 分/门
  THIN_CONTENT 11 门  正文 <1500 中文字（注入补充讲解节）  -8 分/门

复用分层作业那套流程：抽取课件自身骨架 → LLM 生成**针对该课主题**的真内容 →
按 slot 顺序注入统一结构。不做关键词占位。外部托管跳转壳豁免。

随堂小测的判分按钮用 checkAnswer（已随 ta-interactions.js 全库上线），
不再另写判分 JS。

用法：
  python3 scripts/add-depth-modules.py --kind insight --pilot 2 --apply
  python3 scripts/add-depth-modules.py --kind insight --from-file /tmp/no-insight.txt --apply
  python3 scripts/add-depth-modules.py --kind quiz --from-file /tmp/no-quiz.txt --apply
  python3 scripts/add-depth-modules.py --kind thin --from-file /tmp/thin-content.txt --apply
  python3 scripts/add-depth-modules.py --kind insight --all --revert
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import os
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

OR_URL = "https://openrouter.ai/api/v1/chat/completions"
OR_KEY = os.environ.get("OPENROUTER_API_KEY", "").strip()
MODEL = os.environ.get("DEPTH_MODEL", "anthropic/claude-sonnet-4.5")

SKIP_RE = re.compile(r'name=["\']teachany-hosting["\'][^>]*content=["\']external-link|link-shell-1\.0', re.I)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")
SEC_ID_RE = {sid: re.compile(r'<section\b[^>]*\bid=["\']%s["\'][^>]*>(.*?)</section>' % sid, re.S | re.I)
             for sid in ("objectives", "lesson-focus", "deep-understanding", "summary",
                         "error-clinic", "goals", "memory-anchor")}

KIND_META = {
    "insight": {"mark": "data-injected=\"ta-depth-insight\"",
                "already": lambda h: "深层理解" in h or "insight" in h.lower(),
                "slot": 70},
    "quiz":    {"mark": "data-injected=\"ta-depth-quiz\"",
                "already": lambda h: any(m in h for m in ('错因提醒', 'class="choice"', 'data-answer', '选择题')),
                "slot": 80},
    "thin":    {"mark": "data-injected=\"ta-depth-thin\"",
                "already": lambda h: False,
                "slot": 65},
}


def txt(s: str) -> str:
    return WS_RE.sub(" ", TAG_RE.sub("", s or "")).strip()


def context(html: str) -> tuple[str, str]:
    m = re.search(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)', html, re.I) \
        or re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    title = txt(m.group(1)) if m else ""
    parts = []
    for sid, rx in SEC_ID_RE.items():
        mm = rx.search(html)
        if mm:
            t = txt(mm.group(1))
            if t:
                parts.append(f"【{sid}】{t[:500]}")
    heads = [txt(m.group(2)) for m in re.finditer(r"<h([23])[^>]*>(.*?)</h\1>", html, re.S | re.I)]
    heads = [h for h in heads if 2 <= len(h) <= 40]
    seen, uniq = set(), []
    for h in heads:
        if h not in seen:
            seen.add(h)
            uniq.append(h)
    if uniq:
        parts.append("【小节标题】" + " / ".join(uniq[:40]))
    return title, "\n".join(parts)[:2200]


SYS = "你是中国中小学各科的资深教研员。只输出合法 JSON，不要任何解释、不要 Markdown 代码块。"

PROMPTS = {
    "insight": """下面是某门课件的信息。请为它写一节「深层理解」（认知深化）内容。

课件标题：{title}
{ctx}

要求：
1. 写 3 个层次递进的「深层追问」，每个都给出追问与点拨（不是答案全给，是引导学生深入一步）：
   - q1（为什么）：本课核心概念背后的原理层面追问（为什么是这样，不是别的样子）
   - q2（联系）：本课知识与其他知识/真实世界的结构性联系
   - q3（辨异）：最容易混淆的对比辨析，指出分界线在哪
2. 每条追问 15~30 字，点拨 30~80 字，必须紧扣课件具体知识点，禁止通用空话
   （如「联系生活实际思考」「体会知识的价值」）。
3. 学段难度由标题中的 Gx/小学/初中/高中决定。
输出 JSON：{{"q1": "...", "a1": "...", "q2": "...", "a2": "...", "q3": "...", "a3": "..."}}""",

    "quiz": """下面是某门课件的信息。请为它出一组随堂小测（3 道选择题）。

课件标题：{title}
{ctx}

要求：
1. 3 道单选题，每题 4 个选项（A-D），覆盖本课最核心的 3 个知识点。
2. 每题给出：题干、四个选项、正确答案字母、一句话解析（20-40 字，指出为什么对/常见错因）。
3. 题目必须落在课件具体知识点上，选项要有真实的干扰性（错项是典型误区而非凑数）。
4. 难度匹配学段（标题中 Gx/小学/初中/高中）。
输出 JSON：{{"qs": [{{"q": "...", "opts": ["...", "...", "...", "..."], "ans": "A", "why": "..."}}]}}""",

    "thin": """下面是某门课件的信息。它的正文内容偏薄，请为它写一段补充讲解（深入拓展）。

课件标题：{title}
{ctx}

要求：
1. 写 3 个互补的补充小节，各 150~220 字：
   - s1（原理加深）：把核心概念的「为什么」讲透一层
   - s2（细节展开）：挑一个学生最容易忽略的要点展开（含具体例子或数据）
   - s3（应用链接）：一个该知识在真实场景的应用实例
2. 必须紧扣课件具体知识点，禁止通用铺垫（如「这个概念很重要」式凑字）。
3. 语言口语化、面向学生，学段由标题决定。
输出 JSON：{{"s1": "...", "s2": "...", "s3": "..."}}""",
}


def call_llm(prompt: str) -> str:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    s = requests.Session()
    s.mount("https://", HTTPAdapter(max_retries=Retry(
        total=5, connect=5, read=5, backoff_factor=2.0,
        status_forcelist=[429, 500, 502, 503, 504], allowed_methods=["POST"])))
    for attempt in range(6):
        try:
            r = s.post(OR_URL, headers={"Authorization": f"Bearer {OR_KEY}",
                                        "Content-Type": "application/json"},
                       json={"model": MODEL,
                             "messages": [{"role": "system", "content": SYS},
                                          {"role": "user", "content": prompt}],
                             "temperature": 0.4, "max_tokens": 2500},
                       timeout=(30, 180))
            if r.status_code == 429:
                time.sleep(10 * (attempt + 1))
                continue
            r.raise_for_status()
            # OpenRouter 偶发 200 但 body 不含 choices（网关错误页/模型超载提示），
            # 当一次普通失败处理、重试，别让 KeyError 把整批跑挂。
            data = r.json()
            content = (data.get("choices") or [{}])[0].get("message", {}).get("content")
            if not content:
                time.sleep(4 * (attempt + 1))
                continue
            return content
        except Exception:
            time.sleep(6 * (attempt + 1))
    raise RuntimeError("LLM 调用失败")


def parse_json(raw: str) -> dict | None:
    raw = raw.strip()
    m = re.search(r"```(?:json)?\s*([\s\S]*?)```", raw)
    if m:
        raw = m.group(1).strip()
    i, j = raw.find("{"), raw.rfind("}")
    if i < 0 or j <= i:
        return None
    try:
        return json.loads(raw[i:j + 1])
    except Exception:
        return None


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(kind: str, d: dict) -> str:
    if kind == "insight":
        pairs = [(d.get("q1"), d.get("a1")), (d.get("q2"), d.get("a2")), (d.get("q3"), d.get("a3"))]
        if any(not q or not a or len(q) < 8 or len(a) < 15 for q, a in pairs):
            return ""
        items = "".join(
            f'<div class="lhw-card"><strong>{lab}</strong>'
            f"<p><em>{esc(q)}</em></p><p>{esc(a)}</p></div>"
            for (q, a), lab in zip(pairs, ["🤔 为什么", "🔗 联系", "⚖️ 辨异"]))
        return ('<section class="section text-module" id="deep-understanding" '
                'data-slot="70" data-injected="ta-depth-insight">\n'
                '  <div class="lhw-panel"><span class="ta-phase" data-tone="aux">深层理解</span>\n'
                "    <h2>深层理解：往本质再走一步</h2>\n"
                f'    <div class="lhw-grid">{items}</div>\n  </div>\n</section>')
    if kind == "quiz":
        qs = d.get("qs") or []
        if len(qs) < 3 or any(not q.get("q") or not q.get("opts") or not q.get("ans") for q in qs[:3]):
            return ""
        blocks = []
        for i, q in enumerate(qs[:3], 1):
            ans = str(q["ans"]).upper()[0]
            opts = "".join(
                f'<button class="quiz-option choice" '
                f"onclick=\"checkAnswer(this,{str(l == ans).lower()},'tq{i}')\">{esc(o)}</button>"
                for l, o in zip("ABCD", q["opts"][:4]))
            blocks.append(
                f'<div class="practice-block"><h3>{i}. {esc(q["q"])}</h3>'
                f"{opts}"
                f'<div id="tq{i}-feedback" class="feedback"></div>'
                f'<p class="tq-why" style="margin-top:8px;color:#6b7a90;font-size:13px">解析：{esc(q.get("why",""))}</p></div>')
        return ('<section class="section text-module" id="concept-check" data-slot="80" '
                'data-injected="ta-depth-quiz">\n'
                '  <div class="lhw-panel"><span class="ta-phase" data-tone="quiz">随堂小测</span>\n'
                "    <h2>随堂小测：选择题三题自测</h2>\n"
                + "".join(blocks) + "\n  </div>\n</section>")
    if kind == "thin":
        ss = [(d.get("s1"), "原理加深"), (d.get("s2"), "细节展开"), (d.get("s3"), "应用链接")]
        if any(not s or len(s) < 100 for s, _ in ss):
            return ""
        body = "".join(f"<h3>{lab}</h3><p>{esc(s)}</p>" for s, lab in ss)
        return ('<section class="section text-module" id="lesson-extension" data-slot="65" '
                'data-injected="ta-depth-thin">\n'
                '  <div class="lhw-panel"><span class="ta-phase" data-tone="main">深入拓展</span>\n'
                "    <h2>深入拓展</h2>\n" + body + "\n  </div>\n</section>")
    return ""


SLOT_RE = re.compile(r'data-slot=["\'](\d+)["\']')


def insert_pos(html: str, slot: int) -> int:
    secs = list(re.finditer(r"<section\b[^>]*>", html, re.I))
    if not secs:
        return -1

    def close_of(m):
        e = html.find("</section>", m.end())
        return e + len("</section>") if e >= 0 else m.end()

    slots = []
    for m in secs:
        s = SLOT_RE.search(m.group(0))
        slots.append((int(s.group(1)) if s else -1, m))
    cands = [(v, m) for v, m in slots if 0 <= v <= slot]
    if cands:
        return close_of(max(cands, key=lambda x: x[0])[1])
    for v, m in slots:
        if v > slot and v >= 90:
            return m.start()
    return close_of(secs[-1])


def work(cid: str, kind: str, apply: bool) -> tuple[str, str]:
    f = COMMUNITY / cid / "index.html"
    if not f.is_file():
        return cid, "NO-FILE"
    h = f.read_text(encoding="utf-8", errors="ignore")
    meta = KIND_META[kind]
    if meta["mark"] in h:
        return cid, "SKIP(已注入)"
    if kind != "thin" and meta["already"](h):
        return cid, "SKIP(已有)"
    if SKIP_RE.search(h):
        return cid, "SKIP(跳转壳)"
    title, ctx = context(h)
    d = parse_json(call_llm(PROMPTS[kind].format(title=title or cid, ctx=ctx)))
    if not d:
        return cid, "LLM-FAIL"
    block = render(kind, d)
    if not block:
        return cid, "RENDER-FAIL"
    pos = insert_pos(h, meta["slot"])
    if pos < 0:
        return cid, "NO-POS"
    if apply:
        out = h[:pos] + "\n" + block + "\n" + h[pos:]
        # quiz 的判分按钮依赖 ta-interactions.js 的 checkAnswer。
        # 2026-10-10 教训：quiz 注入发生在 fix-dead-buttons 之后时，未引共享库的
        # 课件按钮点下去就是死按钮（bio-h-*/chem-* 21 门曾中招）。注入时同步兜底。
        if kind == "quiz" and "ta-interactions.js" not in out:
            tag = '<script src="../../assets/scripts/ta-interactions.js"></script>'
            i = out.rfind("</body>")
            out = out[:i] + tag + "\n" + out[i:] if i >= 0 else out + tag
        f.write_text(out, encoding="utf-8")
    return cid, "OK"


def load_ids(a) -> list[str]:
    if a.ids:
        return [x.strip() for x in a.ids.split(",") if x.strip()]
    if a.from_file:
        return [l.strip() for l in Path(a.from_file).read_text().splitlines()
                if l.strip() and not l.startswith("#")]
    return [p.name for p in sorted(COMMUNITY.iterdir())
            if (p / "index.html").is_file()][: a.pilot or 2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", choices=["insight", "quiz", "thin"], required=True)
    ap.add_argument("--pilot", type=int, default=0)
    ap.add_argument("--ids")
    ap.add_argument("--from-file")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--revert", action="store_true")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()

    ids = load_ids(a)
    print(f"kind={a.kind} 目标 {len(ids)} 门 apply={a.apply}", flush=True)
    results = []
    with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(work, cid, a.kind, a.apply and not a.revert): cid for cid in ids}
        for fu in cf.as_completed(futs):
            r = fu.result()
            results.append(r)
    ok = sum(1 for _, s in results if s == "OK")
    skips = [r for r in results if r[1].startswith("SKIP")]
    bad = [r for r in results if not r[1].startswith(("OK", "SKIP"))]
    print(f"\n完成：OK {ok}  跳过 {len(skips)}  失败 {len(bad)}")
    for cid, s in bad[:10]:
        print(f"  ✗ {cid}: {s}")


if __name__ == "__main__":
    main()
