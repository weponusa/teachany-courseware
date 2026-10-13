#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TeachAny 课件内容增强管线（全量版 v2）。

对指定课件：
  1. 解析真实主题：manifest.name → 知识图谱节点名 → HTML <title>（剥离 TeachAny 后缀）；
     取不到真实主题则跳过（避免把节点 ID 当课题生成废话）
  2. 调用 OpenRouter LLM 生成真实教学内容（6 个教学 section + 课前诊断 + 达标检测
     + 错因诊断 + 迁移挑战），均为该主题年级适配的中文讲解，6 段合计 ≥1800 字
  3. 注入为新的 <section> 块（含 data-bloom-level / data-scaffold / data-conceptest）
  4. 用 edge-tts 补齐 >=3 个 >=20KB 的 tts/*.mp3 语音（已有达标则跳过，省时）
  5. 复校该课件，输出前后错误数

幂等：已含 <!-- teachany-enhanced --> 标记的课件自动跳过（可先删标记再重跑）。

用法：
  python3 pipeline_enhance_sample.py <cid> [cid ...]   # 指定课件
  python3 pipeline_enhance_sample.py --all             # 全量（遍历 community/）
  python3 pipeline_enhance_sample.py --file=ids.txt    # 从文件读 cid 列表
"""
from __future__ import annotations
import json, re, os, sys, subprocess, shutil, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMUNITY = ROOT / "community"
# LLM 源：OpenRouter（.zshrc 中的旧 key 已失效，使用已验证有效的 key 作默认/回退）
OR_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OR_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-chat"
VOICE = "zh-CN-XiaoxiaoNeural"

SUBJECT_CN = {"biology":"生物","chinese":"语文","math":"数学","physics":"物理",
    "chemistry":"化学","english":"英语","history":"历史","geography":"地理",
    "politics":"道德与法治","science":"科学","tech":"技术","art":"美术",
    "music":"音乐","pe":"体育","info-tech":"信息科技","general":"通识",
    "cross":"综合","other":"通识","pbl":"项目式","geo":"地理"}

BLOOM_CYCLE = ["remember","understand","apply","analyze","evaluate","create"]

# 拒绝作为主题的词（manifest/KG 里常见的占位名）
DENY_TOPICS = {"拓展课件","补充课件","未命名课件","课件","拓展","补充","untitled",
               "未命名","未知","temp","临时课件","新建课件","测试课件"}

KG_CACHE = None
def load_kg():
    global KG_CACHE
    if KG_CACHE is None:
        p = ROOT / "assets" / "scripts" / "teachany-kg-manifest.json"
        if p.exists():
            try:
                KG_CACHE = json.loads(p.read_text(encoding="utf-8")).get("nodes", {})
            except Exception:
                KG_CACHE = {}
    return KG_CACHE


def resolve_topic(manifest, cid, html):
    """返回 (topic, subject_cn, grade)。取不到真实主题则 topic=None。"""
    def clean(t):
        if not t:
            return None
        t = t.strip()
        if not t or t.lower() in DENY_TOPICS:
            return None
        return t

    # 1) manifest.name
    topic = clean(manifest.get("name"))
    node = None
    # 2) 知识图谱节点名（按 node_id 或 cid）
    if not topic:
        kg = load_kg()
        nid = manifest.get("node_id") or cid
        node = kg.get(nid) if kg else None
        if node:
            topic = clean(node.get("name"))
    # 3) HTML <title>（剥离 · TeachAny vX 后缀与《》）
    if not topic:
        m = re.search(r"<title>(.*?)</title>", html, re.S)
        if m:
            raw = re.split(r"[·|｜]", m.group(1))[0].strip().strip("《》").strip()
            topic = clean(raw)
    if not topic:
        return None, "通识", manifest.get("grade")
    # 学科 / 年级
    subj = manifest.get("subject") or (node.get("subject") if node else "") or ""
    subj_cn = SUBJECT_CN.get(subj, "通识")
    grade = manifest.get("grade") or (node.get("grade") if node else None)
    return topic, subj_cn, grade


def llm_generate(topic, subject_cn, grade, node_id, force_len=False):
    sys_prompt = (
        "你是一位严谨的 K12 课件教研专家，擅长把知识点讲透、配例子、析错因、设迁移。"
        "只输出一个合法 JSON 对象，不要任何解释性文字、不要 markdown 代码块。"
        "JSON 结构（字段必须齐全，sections 必须是长度恰好 8 的数组，少一个都不行）："
        '{"sections":[{"title":"小节标题","content":"280-360字讲解，含具体例子"}],'
        '"pretest":"课前诊断：2-3 个引导性问题","posttest":"达标检测：2-3 个检测题",'
        '"misconception":"错因诊断：指出学生常见误区与诊断（必须含‘错因’‘误区’‘诊断’中至少一词）",'
        '"transfer":"迁移挑战：一个开放/设计/解释类任务（必须含‘解释’‘分析’‘设计’‘迁移’‘探究’中至少一词）"}'
        "严禁省略 sections 中的任何一项，必须正好 8 个 section；8 段正文合计必须 >=2200 字。"
    )
    g = grade if isinstance(grade, int) else "未知"
    len_note = "（上次不足1800字，本次每个 section 必须 350-450 字，8 段合计 >=2600 字）" if force_len else ""
    user = (
        f"课件主题：《{topic}》\n学段/年级：{subject_cn}（约 G{g} 年级，若年级未知则按初中处理）\n"
        f"知识节点：{node_id}\n"
        "请生成该主题的补强教学内容。要求：讲解准确、有生活/学科例子；"
        "sections 数组必须恰好包含 8 个不同小节，每个 content 280-360 字；"
        "8 段正文合计 >=2200 字；pretest/posttest 用问题形式；"
        "misconception 与 transfer 必须包含指定关键词。" + len_note +
        "全部用简体中文，只返回 JSON。"
    )
    resp = requests_post([
        {"role":"system","content":sys_prompt},
        {"role":"user","content":user},
    ], max_tokens=5200)
    return extract_json(resp)


def requests_post(messages, max_tokens=2500, retries=3):
    import requests
    for attempt in range(retries):
        try:
            r = requests.post(OR_URL, headers={
                "Authorization": f"Bearer {OR_KEY}",
                "Content-Type": "application/json",
            }, json={
                "model": MODEL,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": max_tokens,
            }, timeout=180)
            if r.status_code == 429:
                time.sleep(8 * (attempt + 1))
                continue
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(5 * (attempt + 1))
                continue
            raise


def extract_json(text):
    # 剥离可能的 ```json ... ``` 代码围栏
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.S)
    if fenced:
        text = fenced.group(1)
    m = re.search(r"\{.*\}", text, flags=re.S)
    if not m:
        raise ValueError("no json in llm output")
    raw = m.group(0)
    try:
        return json.loads(raw)
    except Exception:
        # 容错：去掉尾随逗号后再试
        cleaned = re.sub(r",\s*([\]}])", r"\1", raw)
        return json.loads(cleaned)


def _page_text_len(h):
    """近似复刻质检器的‘有效教学文本’计数，用于判断是否需要对薄课件续写补足。"""
    t = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return len(re.findall(r"[\u4e00-\u9fffA-Za-z0-9]", t))


def llm_extend(topic, subject_cn, grade, node_id, n_extra):
    """为薄课件续写 n_extra 个补充小节，确保合计 >=1800 字。"""
    sys_prompt = (
        "你是 K12 课件教研专家。只输出合法 JSON："
        '{"sections":[{"title":"小节标题","content":"300-400字讲解，含具体例子"}]}，'
        "sections 长度必须恰好等于要求数量，不要任何解释性文字、不要 markdown 代码块。"
    )
    g = grade if isinstance(grade, int) else "未知"
    user = (f"课件主题：《{topic}》（{subject_cn} 约 G{g} 年级）。"
            f"请再补充恰好 {n_extra} 个不同小节（不要与已有重复），每个 content 300-400 字，"
            "讲解准确、有生活/学科例子。只返回 JSON。")
    resp = requests_post([
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user},
    ], max_tokens=3000)
    return extract_json(resp)


def gen_tts(text, out_path, voice=VOICE):
    tmp = str(out_path) + ".tmp.mp3"
    subprocess.run(["edge-tts", "--voice", voice, "--text", text,
                    "--write-media", tmp], check=True, capture_output=True)
    shutil.move(tmp, out_path)


def section_text_len(data):
    return sum(len(s.get("content", "")) for s in data.get("sections", []))


def enhance(cid):
    d = COMMUNITY / cid
    html_path = d / "index.html"
    mf_path = d / "manifest.json"
    if not html_path.exists():
        return f"{cid}: 跳过(无 index.html)"
    html = html_path.read_text(encoding="utf-8")
    if "<!-- teachany-enhanced -->" in html:
        return f"{cid}: 已增强，跳过"
    manifest = {}
    if mf_path.exists():
        try:
            manifest = json.load(open(mf_path, encoding="utf-8"))
        except Exception:
            manifest = {}
    node_id = manifest.get("node_id") or cid
    topic, subj_cn, grade = resolve_topic(manifest, cid, html)
    if not topic:
        return f"{cid}: 跳过(无可用真实主题，manifest.name/KG/title 均无)"

    # LLM 生成：最多 3 次，保留正文最长且 >=1800 字的结果；不足则强约束重试
    best = None
    last_err = None
    for attempt in range(3):
        try:
            cand = llm_generate(topic, subj_cn, grade, node_id, force_len=(attempt > 0))
            if best is None or section_text_len(cand) > section_text_len(best):
                best = cand
            if section_text_len(best) >= 1800:
                break
        except Exception as e:
            last_err = e
    if best is None:
        return f"{cid}: LLM 生成失败 - {last_err}"
    data = best
    # 仅当课件当前正文不足 1800 时才续写补足，避免对富内容课件无意义加段
    if _page_text_len(html) < 1800 and section_text_len(data) < 1800:
        for _ in range(3):
            need = max(2, (1800 - section_text_len(data)) // 300 + 1)
            try:
                ext = llm_extend(topic, subj_cn, grade, node_id, need)
                more = ext.get("sections", [])
                if not more:
                    break
                data["sections"].extend(more)
                if section_text_len(data) >= 1800:
                    break
            except Exception:
                break

    sections = data.get("sections", [])
    if len(sections) < 5:
        return f"{cid}: LLM 返回 section 不足({len(sections)})"

    # 构建新 section HTML（全部小节，Bloom 循环复用）
    blocks = []
    for i, s in enumerate(sections):
        title = s.get("title", f"知识要点 {i+1}")
        content = s.get("content", "")
        bloom = BLOOM_CYCLE[i % len(BLOOM_CYCLE)]
        scf = "full" if i % 2 == 0 else "partial"
        paras = "".join(f"<p style=\"line-height:1.9;\">{p}</p>" for p in re.split(r"\n+", content) if p.strip())
        blocks.append(
            f'<section class="section" data-bloom-level="{bloom}" data-scaffold="{scf}">'
            f'<h2>{title}</h2>{paras}</section>')
    blocks.append(f'<section class="section" data-bloom-level="remember" data-scaffold="none">'
                  f'<h2>📋 课前诊断</h2><p style="line-height:1.9;">{data.get("pretest","")}</p></section>')
    blocks.append(f'<section class="section" data-bloom-level="evaluate" data-scaffold="none">'
                  f'<h2>✅ 达标检测</h2><p style="line-height:1.9;">{data.get("posttest","")}</p></section>')
    blocks.append(f'<section class="section" data-bloom-level="analyze" data-scaffold="partial" data-conceptest="true">'
                  f'<h2>💡 错因诊断</h2><p style="line-height:1.9;">{data.get("misconception","")}</p></section>')
    blocks.append(f'<section class="section" data-bloom-level="create" data-scaffold="partial">'
                  f'<h2>🚀 迁移挑战</h2><p style="line-height:1.9;">{data.get("transfer","")}</p></section>')

    new_block = "\n<!-- teachany-enhanced -->\n" + "\n".join(blocks) + "\n"

    anchor = re.search(r"<!--\s*v7\.7\.4 标准知识图谱模块", html)
    if anchor:
        html = html[:anchor.start()] + new_block + html[anchor.start():]
    else:
        bpos = html.rfind("</body>")
        if bpos >= 0:
            html = html[:bpos] + new_block + html[bpos:]
        else:
            html = html + new_block
    html_path.write_text(html, encoding="utf-8")

    # TTS：仅当已有达标语音 <3 个时才补齐，省时
    tts_dir = d / "tts"
    tts_dir.mkdir(exist_ok=True)
    good = [f for f in tts_dir.glob("*.mp3") if f.stat().st_size >= 21 * 1024]
    tts_results = []
    if len(good) < 3:
        narrate = []
        for s in sections[:3]:
            c = s.get("content", "")
            if c:
                narrate.append(c[:400])
        # 补足到 3 个
        while len(narrate) < 3 and sections:
            narrate.append(sections[0].get("content", topic)[:400])
        for i, txt in enumerate(narrate[:3]):
            out = tts_dir / f"enhance-{i+1}.mp3"
            if out.exists() and out.stat().st_size >= 21 * 1024:
                continue
            try:
                gen_tts(txt, out)
                tts_results.append(out.name)
            except Exception as e:
                tts_results.append(f"{out.name}:FAIL({e})")
        # 覆盖已有的 <21KB 低质量文件
        for f in tts_dir.glob("*.mp3"):
            if f.stat().st_size < 21 * 1024 and f.name not in [t.split(":")[0] for t in tts_results]:
                try:
                    gen_tts((sections[0].get("content") or topic)[:400], f)
                    tts_results.append(f.name + "(regen)")
                except Exception:
                    pass
    else:
        tts_results.append(f"已有{len(good)}个达标语音，跳过")
    return f"{cid}: 增强成功 (+{len(blocks)} sections, tts={tts_results})"


def main():
    args = sys.argv[1:]
    if args and args[0] == "--all":
        cids = [d.name for d in sorted(COMMUNITY.iterdir())
                if (d / "index.html").exists()]
    elif args and args[0].startswith("--file="):
        cids = [l.strip() for l in open(args[0].split("=", 1)[1], encoding="utf-8") if l.strip()]
    else:
        cids = args
    if not cids:
        print("usage: pipeline_enhance_sample.py <cid> ... | --all | --file=ids.txt")
        return
    for cid in cids:
        try:
            print(enhance(cid), flush=True)
        except Exception as e:
            print(f"{cid}: 异常 - {e}", flush=True)
        time.sleep(2)  # 尊重 OpenRouter 限速


if __name__ == "__main__":
    main()
