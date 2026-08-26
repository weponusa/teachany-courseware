#!/usr/bin/env python3
"""fix-ith-rest-modules.py — 修复 it-h 5 课件剩余假模块：
1. posttest 模板题 → 真后测题
2. tiered-practice 空话三卡 → 分级真任务
3. worked-example 通用三步 → 含学科内容的示例推理
幂等：<!-- ith-rest-fixed --> 标记。
用法: python3 fix-ith-rest-modules.py [--dry]
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
MARK = "<!-- ith-rest-fixed -->"

IDS = ["it-h-control-structures", "it-h-data-structures", "it-h-functions-modules",
       "it-h-programming-basics", "it-h-sorting-searching"]

PROMPT = """你是中国高中信息技术教师。课件《{title}》核心知识：
{context}

为互动课件重写三个教学模块，严格输出 JSON（不要 markdown 围栏）：
{{
 "posttest": {{"q": "后测题干", "opts": ["A选项", "B选项", "C选项"], "ans": 1, "diag": "解析"}},
 "practice": {{"基础巩固": "...", "能力应用": "...", "迁移挑战": "..."}},
 "worked": "示例推理段落"
}}
要求：
1. posttest 综合考查本课核心概念的实际应用，3 个选项，ans 是正确项下标（0/1/2），干扰项对应典型错误；diag 45 字内写清"正确项为什么对、干扰项错在哪"；选项不带"A."前缀；
2. practice 三条分别是：基础巩固（15-30字，可直接作答的回忆/辨析任务）、能力应用（20-35字，用本课知识分析具体场景的任务）、迁移挑战（20-35字，设计/解决新问题的任务）——必须含本课具体概念名词，严禁"说出本课一个定义"这类空话；
3. worked 90-130 字，用一个具体例子完整演示本课方法的推理过程，要有具体数据/代码/步骤和结论，禁止"第一步识别变量"这类通用方法论；
4. 所有内容必须落到本课知识点，禁止通用模板话。"""


def llm_json(body):
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps({
                    "model": MODEL,
                    "messages": [{"role": "user", "content": body}],
                    "temperature": 0.5, "max_tokens": 1500,
                }).encode(),
                headers={"Authorization": f"Bearer {API_KEY}",
                         "Content-Type": "application/json",
                         "HTTP-Referer": "https://teachany.cn",
                         "X-OpenRouter-Title": "ith-rest-fix"})
            with urllib.request.urlopen(req, timeout=120) as r:
                txt = json.load(r)["choices"][0]["message"]["content"]
            t = re.sub(r"```(?:json)?", "", txt)
            m = re.search(r"\{[\s\S]*\}", t)
            if not m:
                raise ValueError("no json")
            b = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", m.group(0))
            try:
                return json.loads(b)
            except json.JSONDecodeError:
                return json.loads(re.sub(r",\s*([}\]])", r"\1", b))
        except Exception as e:
            last = e
            time.sleep((attempt + 1) * 15)
    raise last


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def context_of(html):
    out = []
    for sec in ("lesson-focus", "lesson-method", "deep-understanding"):
        m = re.search(r'id="' + sec + r'"[\s\S]*?</section>', html)
        if m:
            t = re.sub(r"<[^>]+>", " ", m.group(0))
            out.append(re.sub(r"\s+", " ", t).strip()[:400])
    return "\n".join(out)[:1000]


def replace_posttest(html, quiz):
    span = re.search(r'(<section\b[^>]*id="posttest"[^>]*>[\s\S]*?</section>)', html)
    if not span:
        return html, False
    seg = span.group(1)
    seg2, k1 = re.subn(r'(</h2><p>)([\s\S]{0,300}?)(</p>)',
                       lambda m: m.group(1) + esc(quiz["q"]) + m.group(3), seg, count=1)
    btns = list(re.finditer(r'<button class="quiz-option"[^>]*>[\s\S]*?</button>', seg2))
    if k1 == 0 or len(btns) < 3:
        return html, False
    ans = int(quiz["ans"])
    for i, bm in enumerate(btns[:3]):
        attrs = 'data-q="post" data-a="' + chr(65 + i) + '"'
        if i == ans:
            attrs += ' data-correct="1" data-diag="' + esc(quiz.get("diag", "")) + '"'
        new = '<button class="quiz-option" ' + attrs + '>' + chr(65 + i) + '. ' + esc(quiz["opts"][i]) + '</button>'
        seg2 = seg2.replace(bm.group(0), new, 1)
    return html[:span.start(1)] + seg2 + html[span.end(1):], True


def replace_practice(html, practice):
    span = re.search(r'(<section\b[^>]*id="tiered-practice"[^>]*>[\s\S]*?</section>)', html)
    if not span:
        return html, False
    seg = span.group(1)
    n = 0
    for key in ("基础巩固", "能力应用", "迁移挑战"):
        val = practice.get(key)
        if not val:
            continue
        seg, k = re.subn(r'(<strong>' + key + r'</strong><p>)([\s\S]{0,200}?)(</p>)',
                         lambda m: m.group(1) + esc(val) + m.group(3), seg, count=1)
        n += k
    if n < 2:
        return html, False
    return html[:span.start(1)] + seg + html[span.end(1):], True


def replace_worked(html, worked):
    span = re.search(r'(<section\b[^>]*id="worked-example"[^>]*>[\s\S]*?</section>)', html)
    if not span:
        return html, False
    seg = span.group(1)
    seg2, k = re.subn(r'(</h2><p>)([\s\S]{0,600}?)(</p>)',
                      lambda m: m.group(1) + esc(worked) + m.group(3), seg, count=1)
    # figcaption 空话换一句真说明
    seg2 = re.sub(r'(<figcaption>)[^<]*(</figcaption>)',
                  r'\1过程图：对照示例，把方法的每一步落到实处。\2', seg2, count=1)
    if k == 0:
        return html, False
    return html[:span.start(1)] + seg2 + html[span.end(1):], True


def process(cid):
    p = COMMUNITY / cid / "index.html"
    html = p.read_text(encoding="utf-8", errors="replace")
    if MARK in html:
        return cid, "已修复", False
    ctx = context_of(html)
    title_m = re.search(r"<h1[^>]*>([\s\S]{0,100}?)</h1>", html)
    title = re.sub(r"<[^>]+>", "", title_m.group(1)).strip() if title_m else cid
    d = llm_json(PROMPT.format(title=title, context=ctx))
    actions = []
    html, ok = replace_posttest(html, d.get("posttest", {}))
    if ok:
        actions.append("后测真题")
    html, ok = replace_practice(html, d.get("practice", {}))
    if ok:
        actions.append("分层真任务")
    html, ok = replace_worked(html, d.get("worked", ""))
    if ok:
        actions.append("示例推理")
    if not actions:
        return cid, "无可替换项", False
    html = html.replace("</body>", MARK + "\n</body>", 1)
    if not DRY:
        p.write_text(html, encoding="utf-8")
    return cid, "、".join(actions), True


def main():
    print(f"待处理 {len(IDS)} 个课件")
    ok, fails = 0, []
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(process, cid): cid for cid in IDS}
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
