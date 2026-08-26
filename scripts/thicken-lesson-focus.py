#!/usr/bin/env python3
"""thicken-lesson-focus.py — 按教材内容加厚课件核心精讲（lesson-focus）
素材：data/kp/<subject>/<cid>.json 的 curriculum_points / excerpts / deep_textbook_snippets
目标：lesson-focus 单段 ~300 字 → 结构化四段（概念本质/结构过程/实例证据/易错提醒）800+字
幂等：<!-- focus-thickened --> 标记
用法: python3 thicken-lesson-focus.py [--only a,b] [--dry]
"""
import json
import os
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
KP_DIR = ROOT / "data" / "kp"
API_KEY = os.environ["OPENROUTER_API_KEY"]
MODEL = os.environ.get("ZH_MODEL", "deepseek/deepseek-chat-v3-0324")
DRY = "--dry" in sys.argv
MARK = "<!-- focus-thickened -->"

PROMPT = """你是中国高中{subject_name}教师，正在按国家课标和教材编写课件核心精讲。
课件《{title}》现有精讲内容：
{current}

课标要求：
{curriculum}

教材内容摘录：
{textbook}

任务：把精讲加厚为结构化四段，严格输出 JSON（不要 markdown 围栏）：
{{
 "essence": "概念本质段",
 "process": "结构与过程段",
 "example": "实例与证据段",
 "pitfall": "易错提醒段"
}}
要求：
1. essence 80-120字：本概念的定义与本质，与课标要求对齐，含核心术语；
2. process 120-180字：展开讲解结构、过程或机制的关键环节，按逻辑顺序写清步骤/层次，必须用到教材摘录中的具体内容；
3. example 100-150字：教材中的经典实例、实验或事实证据（含具体名称/数据），说明它如何支撑概念；
4. pitfall 60-100字：学生最易混的两三个点，给出辨析关键；
5. 全部内容必须与教材摘录一致，禁止编造数据，禁止"非常重要""不容忽视"等空话。"""


def llm_json(body):
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps({
                    "model": MODEL,
                    "messages": [{"role": "user", "content": body}],
                    "temperature": 0.4, "max_tokens": 1600,
                }).encode(),
                headers={"Authorization": f"Bearer {API_KEY}",
                         "Content-Type": "application/json",
                         "HTTP-Referer": "https://teachany.cn",
                         "X-OpenRouter-Title": "focus-thicken"})
            with urllib.request.urlopen(req, timeout=120) as r:
                txt = json.load(r)["choices"][0]["message"]["content"]
            t = re.sub(r"```(?:json)?", "", txt)
            start = t.find("{")
            if start < 0:
                raise ValueError("no json")
            b = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", t[start:])
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


def kp_of(cid):
    for sub in ("biology", "info-tech", "science"):
        p = KP_DIR / sub / f"{cid}.json"
        if p.exists():
            return json.load(open(p, encoding="utf-8"))
    return None


def kp_context(kp):
    cur = "\n".join("- " + c for c in kp.get("curriculum_points", [])[:4])
    if not cur:
        for e in kp.get("excerpts", [])[:4]:
            cur += "- " + str(e.get("text", "")) + "\n"
    snippets = []
    sup = kp.get("supplements") or {}
    for s in (sup.get("deep_textbook_snippets") or [])[:3]:
        t = s.get("text") or s.get("snippet") or ""
        if t:
            snippets.append(t[:700])
    tc = kp.get("textbook_content") or {}
    for s in (tc.get("deep_snippets") or [])[:2]:
        t = s.get("text") or ""
        if t:
            snippets.append(t[:700])
    return cur.strip()[:800], "\n\n".join(snippets)[:1800]


def current_focus(html):
    m = re.search(r'id="lesson-focus"[\s\S]*?</section>', html)
    if not m:
        return "", None
    t = re.sub(r"<[^>]+>", " ", m.group(0))
    return re.sub(r"\s+", " ", t).strip()[:600], m.group(0)


def title_of(html):
    h1 = re.search(r"<h1[^>]*>([\s\S]{0,100}?)</h1>", html)
    if h1:
        return re.sub(r"<[^>]+>", "", h1.group(1)).strip()[:40]
    tm = re.search(r"<title>([^<·]+)", html)
    return tm.group(1).strip()[:40] if tm else ""


def build_new_card(old_sec, d):
    """在 lesson-focus 的 card 中，把首个 <p> 之后替换为四段结构（保留 old_sec 完整开头）"""
    m = re.search(r"(<h2>[\s\S]*?</h2>)([\s\S]*?)(</div>\s*</section>)", old_sec)
    if not m:
        return None
    head = old_sec[:m.start(2)]  # 保留 old_sec 开头到 </h2>（含 id/属性/card 开标签）
    body, tail = m.group(2), m.group(3)
    # 保留原第一段（概念引入），在其后追加结构化段落
    first_p = re.search(r"<p>[\s\S]*?</p>", body)
    intro = first_p.group(0) if first_p else ""
    blocks = (
        f"<p><strong>概念本质：</strong>{esc(d['essence'])}</p>\n"
        f"<p><strong>结构与过程：</strong>{esc(d['process'])}</p>\n"
        f"<p><strong>实例与证据：</strong>{esc(d['example'])}</p>\n"
        f"<p><strong>易错提醒：</strong>{esc(d['pitfall'])}</p>"
    )
    return head + intro + "\n" + blocks + "\n" + tail


def process(cid):
    p = COMMUNITY / cid / "index.html"
    html = p.read_text(encoding="utf-8", errors="replace")
    if MARK in html:
        return cid, "已加厚", False
    kp = kp_of(cid)
    if not kp:
        return cid, "无kp数据", False
    cur, textbook = kp_context(kp)
    if not textbook and not cur:
        return cid, "kp无教材内容", False
    current, old_sec = current_focus(html)
    if not old_sec:
        return cid, "无lesson-focus", False
    title = title_of(html)
    subject_name = "生物" if cid.startswith("bio-") else "信息技术"
    d = llm_json(PROMPT.format(subject_name=subject_name, title=title, current=current,
                               curriculum=cur or "（无）", textbook=textbook or "（无）"))
    if not all(d.get(k) for k in ("essence", "process", "example", "pitfall")):
        raise ValueError("LLM输出字段不全")
    new_sec = build_new_card(old_sec, d)
    if not new_sec:
        return cid, "card结构不匹配", False
    html = html.replace(old_sec, new_sec, 1)
    html = html.replace("</body>", MARK + "\n</body>", 1)
    if not DRY:
        p.write_text(html, encoding="utf-8")
    return cid, "精讲加厚", True


def main():
    only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
    src = (ROOT / "scripts" / "replace-fake-canvas.py").read_text(encoding="utf-8")
    ids = sorted(set(re.findall(r'^\s*"((?:bio|it)-h-[a-z0-9-]+)": dict\(', src, re.M)))
    if only:
        ids = [i for i in ids if i in only]
    print(f"待加厚 {len(ids)} 个课件")
    ok, fails = 0, []
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(process, cid): cid for cid in ids}
        for f in futs:
            cid = futs[f]
            try:
                c, msg, changed = f.result()
                if changed:
                    ok += 1
                    print(f"✅ {c}: {msg}", flush=True)
                else:
                    print(f"⏭️  {c}: {msg}", flush=True)
            except Exception as e:
                fails.append(cid)
                print(f"❌ {cid}: {type(e).__name__} {e}", flush=True)
    print(f"\n加厚 {ok}，失败 {len(fails)}: {','.join(fails) if fails else '无'}")


if __name__ == "__main__":
    main()
