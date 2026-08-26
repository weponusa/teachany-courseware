#!/usr/bin/env python3
"""fix-abt-and-meta.py — 修复 ABT 模板空话 + 补学科年级徽章
1. bio-h 46: ABT 三句全模板 → LLM 真内容（真实前置知识/真实难点/真实任务）
2. it-h 5: ABT 前两句模板 → LLM 重写（保留真实的"所以学"）
3. 51 课件 hero 注入学科年级徽章（从 title 提取）
幂等：<!-- abt-meta-fixed --> 标记
用法: python3 fix-abt-and-meta.py [--only a,b] [--dry]
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
API_KEY = os.environ["OPENROUTER_API_KEY"]
MODEL = os.environ.get("ZH_MODEL", "deepseek/deepseek-chat-v3-0324")
DRY = "--dry" in sys.argv
MARK = "<!-- abt-meta-fixed -->"

PROMPT_BIO = """你是中国高中生物教师。课件《{title}》核心知识摘要：
{context}

重写课件"为什么要学这个"的三段（ABT结构），严格输出 JSON（不要 markdown 围栏）：
{{
 "and": "已经知道部分",
 "but": "但问题是部分",
 "therefore": "所以学部分"
}}
要求：
1. and 30-50字：学生在此前（初中生物/前面章节）学过的与本课直接衔接的具体知识，必须含具体概念名词，严禁"你已经会背一些生物学名词"这类空泛套话；
2. but 30-55字：学生学习本课内容时真实会卡住的具体难点或典型误解，要落到本课概念（如"混淆XX和YY"、"难以理解XX如何导致XX"），严禁"真正考查的是变量机制证据"这类方法论套话；
3. therefore 35-60字：用一个具体的真实任务/情境引出本课学习（如"医生解读体检报告时""分析家族遗传病史时"），含具体场景动词，严禁"先看现象再拆机制最后用证据"这类流程套话；
4. 全部内容必须落到《{title}》的具体知识点。"""

PROMPT_IT = """你是中国高中信息技术教师。课件《{title}》核心知识摘要：
{context}

重写课件"为什么要学这个"的前两段，严格输出 JSON（不要 markdown 围栏）：
{{
 "and": "已经知道部分",
 "but": "但问题是部分"
}}
要求：
1. and 25-45字：学生此前已接触过的与本课直接相关的具体知识或经验（含具体名词），严禁"你见过程序代码"这类空泛套话；
2. but 30-50字：学生学习本课时真实会卡住的具体难点（落到本课概念），严禁"不是背语法而是抽象"这类方法论套话；
3. 必须落到《{title}》的具体知识点。"""

BADGE_STYLE = ("display:inline-block;padding:4px 14px;border-radius:999px;font-size:13px;"
               "letter-spacing:.5px;")


def llm_json(body):
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps({
                    "model": MODEL,
                    "messages": [{"role": "user", "content": body}],
                    "temperature": 0.5, "max_tokens": 700,
                }).encode(),
                headers={"Authorization": f"Bearer {API_KEY}",
                         "Content-Type": "application/json",
                         "HTTP-Referer": "https://teachany.cn",
                         "X-OpenRouter-Title": "abt-meta-fix"})
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


def clean_prefix(s, prefixes):
    """去掉与 strong 标签重复的开头词"""
    s = str(s).strip()
    for p in prefixes:
        if s.startswith(p):
            s = s[len(p):].lstrip("，,：: ")
    return s


def context_of(html):
    for pat in (r'id="(?:lesson-focus|core-knowledge|core-concept)"[\s\S]*?</section>',):
        m = re.search(pat, html)
        if m:
            t = re.sub(r"<[^>]+>", " ", m.group(0))
            return re.sub(r"\s+", " ", t).strip()[:800]
    body = re.sub(r"<script[\s\S]*?</script>", "", html)
    body = re.sub(r"<style[\s\S]*?</style>", "", body)
    t = re.sub(r"<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", t)[300:1100]


def title_of(html):
    h1 = re.search(r"<h1[^>]*>([\s\S]{0,100}?)</h1>", html)
    if h1:
        return re.sub(r"<[^>]+>", "", h1.group(1)).strip()[:40]
    tm = re.search(r"<title>([^<·]+)", html)
    return tm.group(1).strip()[:40] if tm else ""


def replace_abt(html, d, full):
    """替换 abt-why 三句（full=True 三句全换，否则只换前两句）"""
    span = re.search(r'(<section\b[^>]*id="abt-why"[^>]*>[\s\S]*?</section>)', html)
    if not span:
        return html, False
    seg = span.group(1)
    seg2, k1 = re.subn(r"(<strong>已经知道：</strong>)[^<]*(</p>)",
                       lambda m: m.group(1) + esc(clean_prefix(d["and"], ("已经知道", "你已经", "学生已经"))) + m.group(2), seg, count=1)
    seg2, k2 = re.subn(r"(<strong>但问题是：</strong>)[^<]*(</p>)",
                       lambda m: m.group(1) + esc(clean_prefix(d["but"], ("但问题是", "但是", "但"))) + m.group(2), seg2, count=1)
    k3 = 1
    if full and d.get("therefore"):
        seg2, k3 = re.subn(r"(<strong>所以学：</strong>)[^<]*(</p>)",
                           lambda m: m.group(1) + esc(clean_prefix(d["therefore"], ("所以学", "所以", "因此"))) + m.group(2), seg2, count=1)
    if k1 + k2 + k3 < 3:
        return html, False
    return html[:span.start(1)] + seg2 + html[span.end(1):], True


def inject_badge(html):
    """hero subtitle 后注入学科年级徽章"""
    if "course-meta-badges" in html:
        return html, False
    tm = re.search(r"<title>[^<]*? · ([^<·]+?) · TeachAny", html)
    if not tm:
        return html, False
    seg = tm.group(1).strip()  # 如 "高中生物 G10"
    m = re.match(r"(.+?)\s+(G\d+)$", seg)
    parts = [seg] if not m else [m.group(1), m.group(2)]
    colors = [("rgba(56,189,248,.15)", "rgba(56,189,248,.45)", "#7dd3fc"),
              ("rgba(52,211,153,.15)", "rgba(52,211,153,.45)", "#6ee7b7")]
    badges = "".join(
        f'<span style="{BADGE_STYLE}background:{c[0]};border:1px solid {c[1]};color:{c[2]};">{esc(p)}</span>'
        for p, c in zip(parts, colors))
    div = ('<div class="course-meta-badges" style="display:flex;gap:8px;justify-content:center;'
           f'margin-top:12px;flex-wrap:wrap;">{badges}</div>')
    sub = re.search(r"(<p class=\"subtitle\">[\s\S]*?</p>)", html)
    if not sub:
        return html, False
    return html[:sub.end(1)] + div + html[sub.end(1):], True


def process(cid):
    p = COMMUNITY / cid / "index.html"
    html = p.read_text(encoding="utf-8", errors="replace")
    if MARK in html:
        return cid, "已修复", False
    is_bio = cid.startswith("bio-h-")
    title = title_of(html)
    ctx = context_of(html)
    d = llm_json((PROMPT_BIO if is_bio else PROMPT_IT).format(title=title, context=ctx))
    actions = []
    html, ok = replace_abt(html, d, full=is_bio)
    if ok:
        actions.append("ABT真内容")
    html, ok2 = inject_badge(html)
    if ok2:
        actions.append("学科徽章")
    if not actions:
        return cid, "无可替换项", False
    html = html.replace("</body>", MARK + "\n</body>", 1)
    if not DRY:
        p.write_text(html, encoding="utf-8")
    return cid, "、".join(actions), True


def main():
    only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
    src = (ROOT / "scripts" / "replace-fake-canvas.py").read_text(encoding="utf-8")
    ids = sorted(set(re.findall(r'^\s*"((?:bio|it)-h-[a-z0-9-]+)": dict\(', src, re.M)))
    if only:
        ids = [i for i in ids if i in only]
    print(f"待处理 {len(ids)} 个课件")
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
    print(f"\n修复 {ok}，失败 {len(fails)}: {','.join(fails) if fails else '无'}")


if __name__ == "__main__":
    main()
