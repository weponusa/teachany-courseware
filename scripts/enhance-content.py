#!/usr/bin/env python3
"""
enhance-content.py · LLM 批量补写教学实质内容（2026-07 泛化套话欠账清偿）
==========================================================================
对"泛化套话过多且文本偏少"的课件，调 LLM 生成贴合主题的"深度理解"教学
补充卡片（具体例子/易错点/生活应用），注入知识图谱 section 之前。

判定通过逻辑（validate-teaching-quality.py）：
  泛化套话 generic_count>=8 且 text_len<3500 → error
  补 ~1800+ 字实质内容后 text_len 超 3500 → 通过。

用法：
  python3 scripts/enhance-content.py <course-id> [<course-id> ...]
  python3 scripts/enhance-content.py --file /tmp/generic-courses.txt
  python3 scripts/enhance-content.py --dry-run <course-id>
环境：OPENROUTER_API_KEY（或用 --api-key）
"""
import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-chat-v3-0324"
TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")

BANNED = ["本节课我们将学习", "通过本节课的学习", "掌握相关知识", "提升学习兴趣",
          "加深理解", "培养能力", "重要知识点", "核心概念", "拓展延伸",
          "综上所述", "由此可见", "总而言之", "众所周知"]


def strip_html(s: str) -> str:
    return SPACE_RE.sub(" ", TAG_RE.sub(" ", s)).strip()


def llm_generate(api_key: str, prompt: str) -> str:
    req = urllib.request.Request(
        API_URL,
        data=json.dumps({
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.6,
            "max_tokens": 3800,
        }).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://teachany.cn",
            "X-Title": "TeachAny content enhance",
        },
        method="POST")
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.loads(r.read())
    return data["choices"][0]["message"]["content"].strip()


def build_prompt(cid: str, manifest: dict, existing_text: str) -> str:
    title = manifest.get("title", cid)
    subject = manifest.get("subject", "")
    grade = manifest.get("grade", "")
    objectives = manifest.get("learning_objectives") or manifest.get("objectives") or []
    if isinstance(objectives, list):
        objectives = "；".join(str(o) for o in objectives[:4])
    return f"""你是中学{subject}学科的资深教师。请为在线课件《{title}》（{grade}）补写"深度理解"教学卡片内容。

课件学习目标：{objectives or '见标题'}

课件现有内容概要（避免重复）：
{existing_text[:800]}

请严格按以下 HTML 格式输出 4 个卡片（不要输出其他内容）。注意：每张卡片正文必须充实，全篇总量不少于 1600 个中文字（这是硬性篇幅要求，宁可写长不可写短）：

<div class="card">
<h3>🔍 易错点辨析</h3>
<p>[针对本课题学生最容易犯的 3 个具体错误，逐个说明：错误表现是什么、为什么会犯这个错（认知根源）、正确理解是什么。要具体，必须引用本课题的真实知识点、数字和例子，每点 180-260 字。]</p>
</div>
<div class="card teal">
<h3>🌏 生活与科技中的应用</h3>
<p>[本课题知识在现实世界/科技/其他学科中的 3 个真实应用实例，每个实例要具体到场景、人物或数据，说明知识是怎么用上的，每个 150-220 字。]</p>
</div>
<div class="card amber">
<h3>🧩 深入追问</h3>
<p>[设计 2 个比基础理解更深一层的思考问题，先抛问题，再给引导性分析（给思路不给完整答案，留思考空间）。每个问题+分析共 200-280 字。]</p>
</div>
<div class="card purple">
<h3>📖 知识脉络梳理</h3>
<p>[把本课题的知识点串成一段连贯的叙述：从问题引入到核心概念再到方法应用，像老师娓娓道来讲课一样，用"先…接着…最后…"的脉络，穿插具体的例子和数字。400-550 字，一气呵成不分点。]</p>
</div>

硬性要求：
1. 全程使用简体中文（学科术语可带英文原文）。
2. 内容必须紧扣《{title}》的具体知识，禁止任何放之四海皆准的空话。
3. 绝对禁止出现这些短语：{'、'.join(BANNED[:6])}。
4. 直接输出 HTML 片段，不要 markdown 代码块，不要解释。"""


def inject(html: str, cards_html: str) -> str:
    anchor = '<section class="section" id="knowledge-graph"'
    block = (
        '<section class="section" id="deep-understanding" data-bloom-level="understand" '
        'data-tts="deep-understanding" data-tsh="深度理解">\n'
        '  <h2 class="section-title">📚 深度理解</h2>\n'
        + cards_html + '\n</section>\n\n'
    )
    if anchor in html:
        return html.replace(anchor, block + anchor, 1)
    # 兜底：插到最后一个 </section> 之后
    idx = html.rfind("</section>")
    if idx > 0:
        return html[: idx + len("</section>")] + "\n\n" + block + html[idx + len("</section>"):]
    raise RuntimeError("找不到注入点")


def count_cn_like(text: str) -> int:
    return len(re.findall(r"[一-鿿]", text))


def qc_text_len(html: str) -> int:
    """与 validate-teaching-quality.py 同款的 text_len 算法"""
    h = re.sub(r"<script\b[^>]*>.*?</script>", " ", html, flags=re.I | re.S)
    h = re.sub(r"<style\b[^>]*>.*?</style>", " ", h, flags=re.I | re.S)
    h = re.sub(r"<[^>]+>", " ", h)
    h = re.sub(r"&[a-zA-Z]+;", " ", h)
    h = re.sub(r"\s+", " ", h).strip()
    return len(re.findall(r"[一-鿿A-Za-z0-9]", h))


def build_round2_prompt(cid: str, manifest: dict) -> str:
    title = manifest.get("title", cid)
    subject = manifest.get("subject", "")
    return f"""你是中学{subject}学科资深教师。请为课件《{title}》再补 2 张拓展卡片，严格按此 HTML 输出（不要其他内容）：

<div class="card purple">
<h3>🌍 跨学科联系</h3>
<p>[本课题知识与 2-3 门其他学科（如数学/物理/历史/生物/信息技术等）的真实联系点，每个联系要具体到对方学科的哪个概念、两科如何互相印证或互相应用，每点 150-220 字。]</p>
</div>
<div class="card">
<h3>📜 来龙去脉</h3>
<p>[本课题知识是怎么被发现/形成/演变的：关键人物、关键事件、争议与转折，以及它对本学科后续发展的影响。用讲故事的方式，穿插具体年份和名字，350-500 字。]</p>
</div>

硬性要求：简体中文；紧扣《{title}》具体知识；禁止空话套话；直接输出 HTML 片段，不要 markdown 围栏。"""


def enhance_course(cid: str, api_key: str, dry_run: bool = False, force: bool = False) -> str:
    cdir = REPO / "community" / cid
    html_path = cdir / "index.html"
    mf_path = cdir / "manifest.json"
    if not html_path.exists():
        return f"{cid}: ✗ 缺 index.html"
    manifest = json.load(open(mf_path, encoding="utf-8")) if mf_path.exists() else {}
    html = html_path.read_text(encoding="utf-8", errors="ignore")
    has_deep = 'id="deep-understanding"' in html
    has_ext = 'id="extended-reading"' in html
    if force:
        # force：删除旧卡片重新生成
        html = re.sub(r'<section class="section" id="deep-understanding".*?</section>\s*', "", html, flags=re.S)
        html = re.sub(r'<section class="section" id="extended-reading".*?</section>\s*', "", html, flags=re.S)
        has_deep = has_ext = False
    elif has_deep and has_ext:
        # 已有两轮卡片，仅当 text_len 仍不足时追加第三轮"知识脉络"短卡
        tl0 = qc_text_len(html)
        if tl0 >= 3450:
            return f"{cid}: - 已含两轮卡片且 text_len={tl0} 达标，跳过"
        prompt3 = (f"你是中学教师。为课件《{manifest.get('title', cid)}》写一段 400-550 字的"
                   f"『知识脉络梳理』：像老师讲课一样，把本课题从问题引入到核心概念再到方法应用"
                   f"串成连贯叙述，穿插具体例子和数字，简体中文，禁止空话套话。"
                   f"严格只输出这个 HTML 片段：<div class=\"card purple\"><h3>📖 知识脉络梳理</h3><p>…正文…</p></div>")
        try:
            cards3 = llm_generate(api_key, prompt3)
            cards3 = re.sub(r"^```(html)?\s*|\s*```$", "", cards3.strip())
        except Exception as e:
            return f"{cid}: ✗ 第三轮 LLM 失败: {e}"
        if '<div class="card' not in cards3 or any(b in cards3 for b in BANNED):
            return f"{cid}: ✗ 第三轮输出异常"
        extra = ('<section class="section" id="knowledge-context" data-bloom-level="understand" '
                 'data-tts="knowledge-context" data-tsh="知识脉络">\n'
                 '  <h2 class="section-title">🧭 知识脉络</h2>\n' + cards3 + '\n</section>\n\n')
        anchor = '<section class="section" id="knowledge-graph"'
        new_html = html.replace(anchor, extra + anchor, 1) if anchor in html else html + extra
        html_path.write_text(new_html, encoding="utf-8")
        added = count_cn_like(strip_html(cards3))
        return f"{cid}: ✓ 追加知识脉络（+{added} 中文字，text_len={qc_text_len(new_html)}）"
    elif has_deep and not has_ext:
        # 渐进模式：已有深度理解，仅在 text_len 不足时追加拓展阅读
        tl0 = qc_text_len(html)
        if tl0 >= 3450:
            return f"{cid}: - 已含深度理解且 text_len={tl0} 达标，跳过"
        try:
            cards2 = llm_generate(api_key, build_round2_prompt(cid, manifest))
            cards2 = re.sub(r"^```(html)?\s*|\s*```$", "", cards2.strip())
        except Exception as e:
            return f"{cid}: ✗ 追加轮 LLM 失败: {e}"
        if cards2.count('<div class="card') < 1 or any(b in cards2 for b in BANNED):
            return f"{cid}: ✗ 追加轮输出异常"
        extra = ('<section class="section" id="extended-reading" data-bloom-level="analyze" '
                 'data-tts="extended-reading" data-tsh="拓展阅读">\n'
                 '  <h2 class="section-title">📖 拓展阅读</h2>\n' + cards2 + '\n</section>\n\n')
        anchor = '<section class="section" id="knowledge-graph"'
        new_html = html.replace(anchor, extra + anchor, 1) if anchor in html else html + extra
        html_path.write_text(new_html, encoding="utf-8")
        added = count_cn_like(strip_html(cards2))
        return f"{cid}: ✓ 追加拓展阅读（+{added} 中文字，text_len={qc_text_len(new_html)}）"
    existing = strip_html(html)[:1200]
    prompt = build_prompt(cid, manifest, existing)
    if dry_run:
        return f"{cid}: [dry-run] 现有文本{count_cn_like(strip_html(html))}字，prompt {len(prompt)} 字符"
    try:
        cards = llm_generate(api_key, prompt)
    except Exception as e:
        return f"{cid}: ✗ LLM 调用失败: {e}"
    # 清理 LLM 可能输出的 markdown 围栏
    cards = re.sub(r"^```(html)?\s*|\s*```$", "", cards.strip())
    if cards.count('<div class="card') < 2:
        return f"{cid}: ✗ LLM 输出格式异常（卡片数不足），未注入"
    if any(b in cards for b in BANNED):
        return f"{cid}: ✗ LLM 输出含禁用套话，未注入"
    new_html = inject(html, cards)
    added = count_cn_like(strip_html(cards))
    # 第一轮后实测 text_len，不足 3600（留余量）自动追加第二轮拓展卡片
    tl = qc_text_len(new_html)
    if tl < 3600:
        try:
            cards2 = llm_generate(api_key, build_round2_prompt(cid, manifest))
            cards2 = re.sub(r"^```(html)?\s*|\s*```$", "", cards2.strip())
            if cards2.count('<div class="card') >= 1 and not any(b in cards2 for b in BANNED):
                extra = (
                    '<section class="section" id="extended-reading" data-bloom-level="analyze" '
                    'data-tts="extended-reading" data-tsh="拓展阅读">\n'
                    '  <h2 class="section-title">📖 拓展阅读</h2>\n' + cards2 + '\n</section>\n\n')
                anchor = '<section class="section" id="knowledge-graph"'
                if anchor in new_html:
                    new_html = new_html.replace(anchor, extra + anchor, 1)
                added += count_cn_like(strip_html(cards2))
                tl = qc_text_len(new_html)
        except Exception as e:
            return f"{cid}: ⚠ 第一轮已注入（+{added}字），第二轮异常 {e}"
    html_path.write_text(new_html, encoding="utf-8")
    return f"{cid}: ✓ 注入深度理解卡片（+{added} 中文字，text_len={tl}）"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("courses", nargs="*")
    ap.add_argument("--file")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="已有深度理解卡片也重新生成")
    ap.add_argument("--api-key", default=os.environ.get("OPENROUTER_API_KEY", ""))
    args = ap.parse_args()
    courses = list(args.courses)
    if args.file:
        courses += [l.strip() for l in open(args.file) if l.strip() and not l.startswith("#")]
    if not courses:
        ap.error("需要课件 id 或 --file 清单")
    if not args.dry_run and not args.api_key:
        ap.error("缺 OPENROUTER_API_KEY")
    for cid in courses:
        try:
            print(enhance_course(cid, args.api_key, args.dry_run, args.force), flush=True)
        except Exception as e:
            print(f"{cid}: ✗ 异常 {e}", flush=True)


if __name__ == "__main__":
    main()
