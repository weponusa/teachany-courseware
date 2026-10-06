#!/usr/bin/env python3
"""rewrite-fake-text-modules.py — 把 51 个 shell 课件的假文本模块换真：
1. deep-understanding 五镜头空话（51 个）→ 含本课概念的真内容
2. pretest 模板判断题（46 个 bio-h）→ 暴露真实误区的诊断题
3. concept-check 模板判断题（51 个）→ 真概念辨析题
内容来源：LLM（OpenRouter deepseek-v3），上下文取该课 lesson-focus/lesson-method 真内容。
幂等：替换后写入 <!-- text-modules-fixed --> 标记，已标记则跳过。
用法: python3 rewrite-fake-text-modules.py [--only a,b,c] [--dry]
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
API_KEY = os.environ["OPENROUTER_API_KEY"]  # 必须经环境变量提供，禁止硬编码
MODEL = os.environ.get("ZH_MODEL", "deepseek/deepseek-chat-v3-0324")
DRY = "--dry" in sys.argv
MARK = "<!-- text-modules-fixed -->"

LENS_KEYS = ["看见它", "拆开它", "解释它", "迁移它"]

PROMPT = """你是中国高中《{title}》的资深教师。课件核心知识摘要：
{context}

为互动课件重写三个教学模块，严格输出 JSON（不要 markdown 围栏）：
{{
 "lens": {{"看见它": "...", "拆开它": "...", "解释它": "...", "迁移它": "..."}},
 "pretest": {{"q": "前测题干", "opts": ["A选项", "B选项", "C选项"], "ans": 1, "diag": "解析"}},
 "concept": {{"q": "概念辨析题干", "opts": ["A选项", "B选项", "C选项"], "ans": 0, "diag": "解析"}}
}}
要求：
1. lens 每条 15-35 字，必须落到本课具体概念/事实（如具体结构、过程、数据），严禁"先描述题干现象""区分变量和层级"这类空泛方法论套话；
2. pretest 暴露学生真实误区（如混淆同源与同功、把葡萄糖当直接能源），pretest 与 concept 不能同义；
3. concept 考查容易混淆的概念辨析；
4. 每题 3 个选项，ans 是正确项下标（0/1/2），干扰项必须对应典型错误想法；
5. diag 45 字内，写清"正确项为什么对、干扰项错在哪"，同时用于答对确认与答错提示；
6. 题干和选项不要带"A."前缀。"""


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
                         "X-OpenRouter-Title": "text-modules-fix"})
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
    """提取 lesson-focus/lesson-method 的真内容作为 LLM 上下文"""
    out = []
    for sec in ("lesson-focus", "lesson-method"):
        m = re.search(r'id="' + sec + r'"[\s\S]*?</section>', html)
        if m:
            t = re.sub(r"<[^>]+>", " ", m.group(0))
            t = re.sub(r"\s+", " ", t).strip()
            out.append(t[:500])
    return "\n".join(out)[:900]


def replace_lens(html, lens):
    """替换五镜头 4 张 mini-card 的 p 文本"""
    n = 0
    for key in LENS_KEYS:
        val = lens.get(key)
        if not val:
            continue
        pat = re.compile(r'(<strong>' + re.escape(key) + r'</strong><p>)([\s\S]{0,200}?)(</p>)')
        html, k = pat.subn(lambda m: m.group(1) + esc(val) + m.group(3), html, count=1)
        n += k
    return html, n


def replace_quiz(html, sec_id, quiz, q_prefix):
    """替换 pretest/concept-check 的题干与 3 个选项，重写 data-correct"""
    span = re.search(r'(<section\b[^>]*id="' + sec_id + r'"[^>]*>[\s\S]*?</section>)', html)
    if not span:
        return html, False
    seg = span.group(1)
    # 题干：第一个 <p>（h2 之后）
    seg2, k1 = re.subn(r'(</h2><p>)([\s\S]{0,300}?)(</p>)',
                       lambda m: m.group(1) + esc(quiz["q"]) + m.group(3), seg, count=1)
    # 选项
    btns = list(re.finditer(r'<button class="quiz-option"[^>]*>[\s\S]*?</button>', seg2))
    if k1 == 0 or len(btns) < 3:
        return html, False
    ans = int(quiz["ans"])
    for i, bm in enumerate(btns[:3]):
        old = bm.group(0)
        attrs = 'data-q="' + q_prefix + '" data-a="' + chr(65 + i) + '"'
        if i == ans:
            attrs += ' data-correct="1" data-diag="' + esc(quiz.get("diag", "")) + '"'
        new = '<button class="quiz-option" ' + attrs + '>' + chr(65 + i) + '. ' + esc(quiz["opts"][i]) + '</button>'
        seg2 = seg2.replace(old, new, 1)
    # 删除 feedback 后残留的模板套话段落
    seg2 = re.sub(r'<p>错因诊断：[\s\S]{0,400}?</p>', '', seg2, count=1)
    # 诊断文本进 feedback 前的提示语（保留 feedback 占位，JS 点击后显示）
    seg2, _ = re.subn(r'(<div class="feedback" id="fb-' + q_prefix + r'">)[^<]*(</div>)',
                      lambda m: m.group(1) + "选择后显示错因诊断。" + m.group(2), seg2, count=1)
    return html[:span.start(1)] + seg2 + html[span.end(1):], True


def patch_quiz_js(html):
    """把 quiz JS 里的固定模板反馈改为读 data-diag 真解析（幂等）"""
    html2 = re.sub(r"fb\.textContent='正确。[^']*'",
                   "fb.textContent='✅ '+(o.dataset.diag||'回答正确。')", html)
    html2 = re.sub(r"fb\.textContent='错因诊断：[^']*'",
                   "fb.textContent='❌ 再想想。'+((group.find(function(x){return x.dataset.correct})||{dataset:{}}).dataset.diag||'')", html2)
    return html2, html2 != html


def clean_residual(html):
    """清理 quiz section 内残留的模板套话段落（幂等，独立于 LLM 替换）"""
    n = 0
    for sid in ("pretest", "concept-check"):
        span = re.search(r'(<section\b[^>]*id="' + sid + r'"[^>]*>[\s\S]*?</section>)', html)
        if span:
            seg = span.group(1)
            seg2 = re.sub(r'<p>错因诊断：[\s\S]{0,400}?</p>', '', seg, count=1)
            if seg2 != seg:
                html = html[:span.start(1)] + seg2 + html[span.end(1):]
                n += 1
    return html, n


def process(cid):
    p = COMMUNITY / cid / "index.html"
    html = p.read_text(encoding="utf-8", errors="replace")
    # JS 补丁 + 残留清理对已标记课件也补跑
    html, js_patched = patch_quiz_js(html)
    html, n_resid = clean_residual(html)
    if MARK in html:
        if js_patched or n_resid:
            if not DRY:
                p.write_text(html, encoding="utf-8")
            return cid, f"补漏(JS补丁={js_patched},残留×{n_resid})", True
        return cid, "已修复", False
    ctx = context_of(html)
    title_m = re.search(r"<h1[^>]*>([\s\S]{0,100}?)</h1>", html)
    title = re.sub(r"<[^>]+>", "", title_m.group(1)).strip() if title_m else cid
    if not ctx:
        return cid, "无 lesson-focus 上下文", False

    d = llm_json(PROMPT.format(title=title, context=ctx))
    actions = []

    html, n_lens = replace_lens(html, d.get("lens", {}))
    if n_lens >= 3:
        actions.append(f"五镜头×{n_lens}")

    is_bio = cid.startswith("bio-h-")
    if is_bio and d.get("pretest"):
        html, ok = replace_quiz(html, "pretest", d["pretest"], "pre")
        if ok:
            actions.append("前测真题")
    if d.get("concept"):
        html, ok = replace_quiz(html, "concept-check", d["concept"], "concept")
        if ok:
            actions.append("概念真题")

    if not actions:
        return cid, "无可替换项", False
    html = html.replace("</body>", MARK + "\n</body>", 1)
    if not DRY:
        p.write_text(html, encoding="utf-8")
    return cid, "、".join(actions), True


def main():
    only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
    ids = []
    for f in sorted(COMMUNITY.glob("*/index.html")):
        cid = f.parent.name
        if cid.startswith("bio-h-") or cid.startswith("it-h-"):
            if 'id="deep-understanding"' in f.read_text(encoding="utf-8", errors="replace"):
                ids.append(cid)
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
