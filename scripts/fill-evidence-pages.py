#!/usr/bin/env python3
"""fill-evidence-pages.py — 填充 171 个"专属证据"空页
结构对齐非空样例（phy-m-light-reflection）：
  lesson-panel > phase-tag + h2 + mini-grid 四卡(课标锚点/具体案例/分析方法/避坑提醒) + 课堂任务
内容：LLM 按各课核心知识生成
幂等：<!-- evidence-filled --> 标记
用法: python3 fill-evidence-pages.py [--only a,b] [--dry]
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
MARK = "<!-- evidence-filled -->"

PROMPT = """你是中国中小学教师。课件《{title}》核心知识摘要：
{context}

为课件的"专属证据"页生成四个教学卡片，严格输出 JSON（不要 markdown 围栏）：
{{
 "anchor": "课标锚点",
 "case": "具体案例",
 "method": "分析方法",
 "pitfall": "避坑提醒"
}}
要求：
1. anchor 25-45字：本课对应的课程标准要求或核心素养要求，用"探究/了解/理解/掌握..."句式；
2. case 35-60字：本课最经典的一个实验、事实或文本证据，必须含具体名称/数据/现象（如"拉瓦锡密闭容器实验证明反应前后总质量不变"），禁止空泛；
3. method 25-45字：本学科解决这类问题的标准方法步骤（如"先画光路，再比较入射角与反射角"）；
4. pitfall 30-50字：学生在本课最典型的答题错误提醒；
5. 全部内容必须落到本课具体知识点，严禁"要看清题目"这类通用套话。"""

TEMPLATE = """
<section class="section" id="knowledge-specific-evidence" data-tts="knowledge-specific-evidence" data-tsh="专属证据 - 用本知识点的事实补足理解" data-bloom-level="analyze" data-scaffold="partial">
  <div class="lesson-panel specificity-panel">
    <span class="phase-tag">Specific Evidence</span>
    <h2>{title}：本课专属证据包</h2>
    <div class="mini-grid specificity-table">
      <div class="mini-panel"><h3>课标锚点</h3><p>{anchor}</p></div>
      <div class="mini-panel"><h3>具体案例</h3><p>{case}</p></div>
      <div class="mini-panel"><h3>分析方法</h3><p>{method}</p></div>
      <div class="mini-panel"><h3>避坑提醒</h3><p>{pitfall}</p></div>
    </div>
    <p class="feedback"><strong>课堂任务：</strong>请用“现象/文本/地图/实验数据 → 关键证据 → 学科解释 → 迁移应用”四步，重写一个关于「{title}」的新问题。</p>
  </div>
</section>
"""


def llm_json(body):
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps({
                    "model": MODEL,
                    "messages": [{"role": "user", "content": body}],
                    "temperature": 0.5, "max_tokens": 900,
                }).encode(),
                headers={"Authorization": f"Bearer {API_KEY}",
                         "Content-Type": "application/json",
                         "HTTP-Referer": "https://teachany.cn",
                         "X-OpenRouter-Title": "evidence-fill"})
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


def context_of(html):
    """提取核心知识内容作 LLM 上下文"""
    texts = []
    # 优先 core-knowledge / lesson-focus / 内容 section
    for pat in (r'id="(?:lesson-focus|core-knowledge|core-concept)"[\s\S]*?</section>',
                r'data-tsh="核心知识[^"]*"[\s\S]*?</section>',
                r'data-tsh="精讲[^"]*"[\s\S]*?</section>'):
        m = re.search(pat, html)
        if m:
            t = re.sub(r"<[^>]+>", " ", m.group(0))
            texts.append(re.sub(r"\s+", " ", t).strip()[:600])
            break
    if not texts:
        # 退化：body 可见文本中段
        body = re.sub(r"<script[\s\S]*?</script>", "", html)
        body = re.sub(r"<style[\s\S]*?</style>", "", body)
        t = re.sub(r"<[^>]+>", " ", body)
        t = re.sub(r"\s+", " ", t)
        texts.append(t[300:900])
    return texts[0][:800]


def title_of(cid, html):
    h1 = re.search(r"<h1[^>]*>([\s\S]{0,100}?)</h1>", html)
    if h1:
        t = re.sub(r"<[^>]+>", "", h1.group(1)).strip()
        t = re.sub(r"^[\U0001F300-\U0001FAFF☀-➿\s]+", "", t).strip()
        if t:
            return t[:30]
    m = re.search(r'<meta name="course-title" content="([^"]+)"', html)
    if m:
        return m.group(1).strip()[:30]
    tm = re.search(r"<title>([^<·《》]+)", html)
    return tm.group(1).strip()[:30] if tm else cid


def find_empty_evidence(html):
    """返回空证据页 slide-page 的 span（含整壳），无则 None"""
    m = re.search(
        r'<section class="slide-page"[^>]*data-tsh="专属证据[^"]*"[^>]*>\s*</section>', html)
    return m


def process(cid):
    p = COMMUNITY / cid / "index.html"
    html = p.read_text(encoding="utf-8", errors="replace")
    if MARK in html:
        return cid, "已填充", False
    m = find_empty_evidence(html)
    if not m:
        return cid, "无空证据页", False
    title = title_of(cid, html)
    ctx = context_of(html)
    d = llm_json(PROMPT.format(title=title, context=ctx))
    inner = TEMPLATE.format(title=esc(title), anchor=esc(d.get("anchor", "")),
                            case=esc(d.get("case", "")), method=esc(d.get("method", "")),
                            pitfall=esc(d.get("pitfall", "")))
    new_shell = m.group(0).replace("</section>", inner + "</section>")
    html = html[:m.start()] + new_shell + MARK + html[m.end():]
    if not DRY:
        p.write_text(html, encoding="utf-8")
    return cid, "证据页填充", True


def main():
    only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
    ids = []
    for f in sorted(COMMUNITY.glob("*/index.html")):
        html = f.read_text(encoding="utf-8", errors="replace")
        if MARK not in html and find_empty_evidence(html):
            ids.append(f.parent.name)
    if only:
        ids = [i for i in ids if i in only]
    print(f"待填充 {len(ids)} 个课件")
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
    print(f"\n填充 {ok}，失败 {len(fails)}: {','.join(fails) if fails else '无'}")


if __name__ == "__main__":
    main()
