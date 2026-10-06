#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TeachAny 课件批量升级 v2：真题 + 互动 + Agnes 中文标注图。

重要质量约束（2026-07 修订）：
  - 禁止继续生成/保留 And/But/Therefore、角色任务空壳、变量A/B/C 通用实验。
  - 升级时应改写 #story 为「主题专属真实情境」，不要只在文末贴题。
  - 物理压强样板见 community/phy-m-pressure（去套路重写）；批量默认暂停，
    需显式 --force-batch 才对大批量运行。

在不动课标树的前提下，对 community/ 课件叠加：
  1. 真实题型（选择题/填空，含答案与错因诊断）
  2. 可点击互动（ConcepTest 选择题 + 探究记录）
  3. Agnes 生图（prompt 强制中文知识点标注；有额度才生成）
  4. 注入 <img> 引用（若内容升级成功）
  5. 若存在 ABT 空壳（And 已有经验），改写为专属情境段落

幂等：已含 <!-- teachany-upgrade-v2 --> 则跳过（可用 --force 重写）。

用法：
  python3 pipeline_upgrade_v2.py <cid> [cid ...]
  python3 pipeline_upgrade_v2.py --file=upgrade_priority.txt --limit=20 --force-batch
  python3 pipeline_upgrade_v2.py phy-m-pressure --force --skip-images
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from pipeline_enhance_sample import (
    COMMUNITY,
    OR_URL,
    MODEL,
    extract_json,
    resolve_topic,
)

ROOT = Path(__file__).resolve().parent
AGNES = ROOT / "scripts" / "agnes-image-gen.py"
OR_KEY = os.environ.get("OPENROUTER_API_KEY", "").strip()
MARKER = "<!-- teachany-upgrade-v2 -->"
UPGRADE_CSS_ID = "teachany-upgrade-v2-css"
UPGRADE_JS_ID = "teachany-upgrade-v2-js"


def requests_post(messages, max_tokens=4200, retries=3):
    import requests

    if not OR_KEY:
        raise RuntimeError("缺少 OPENROUTER_API_KEY 环境变量")
    for attempt in range(retries):
        try:
            r = requests.post(
                OR_URL,
                headers={
                    "Authorization": f"Bearer {OR_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": MODEL,
                    "messages": messages,
                    "temperature": 0.55,
                    "max_tokens": max_tokens,
                },
                timeout=180,
            )
            if r.status_code == 429:
                time.sleep(8 * (attempt + 1))
                continue
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except Exception:
            if attempt < retries - 1:
                time.sleep(5 * (attempt + 1))
                continue
            raise


def llm_upgrade_pack(topic, subject_cn, grade, node_id):
    g = grade if isinstance(grade, int) else "未知"
    sys_prompt = (
        "你是中国 K12 一线教研员，擅长命制中考/学业考风格真题与概念检测。"
        "只输出合法 JSON，不要 markdown 代码块，不要解释。"
        "严禁输出 And/But/Therefore、角色任务、物理实验分析师、变量A/变量B 等空壳套话。"
        "JSON 结构必须齐全："
        "{"
        '"story":{"title":"真实情境标题（禁止角色任务）","lead":"80-120字具体生活/实验情境",'
        '"known":"学生已有的具体经验","stuck":"本课真正易混点","task":"本课具体任务"},'
        '"mcqs":[{"stem":"题干","options":["A. …","B. …","C. …","D. …"],'
        '"answer":"B","explain":"正确答案理由","wrong":{"A":"错因","C":"错因","D":"错因"}}],'
        '"fills":[{"stem":"填空题干（用____表示空）","answer":"标准答案","explain":"解析"}],'
        '"conceptest":{"stem":"概念检测题干","options":["A. …","B. …","C. …","D. …"],'
        '"answer":"A","diagnosis":{"A":"正确诊断","B":"错因","C":"错因","D":"错因"}},'
        '"inquiry":{"title":"探究标题","prompt":"探究任务说明",'
        '"hypothesis":"假设提示","evidence":"证据提示","conclusion":"结论提示"},'
        '"image_labels":["中文标注词1","中文标注词2","中文标注词3","中文标注词4"]'
        "}"
        "硬性要求：mcqs 恰好 3 道；fills 恰好 2 道；options 必须 4 个且以 A./B./C./D. 开头；"
        "answer 只能是 A/B/C/D；题目贴近该年级中国课标；story 必须专属本主题。"
    )
    user = (
        f"主题：《{topic}》\n学科：{subject_cn}\n年级：G{g}\n节点：{node_id}\n"
        "请生成：专属真实情境 story + 真题包 + 概念检测 + 探究任务 +"
        "4 个中文知识点短标注（每个≤8字）。"
    )
    raw = requests_post(
        [{"role": "system", "content": sys_prompt}, {"role": "user", "content": user}],
        max_tokens=4800,
    )
    return extract_json(raw)


def escape_html(s: str) -> str:
    return (
        str(s or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def rewrite_abt_shell(html: str, topic: str, story: dict | None) -> str:
    """把 And/But/Therefore 空壳改成主题专属情境。"""
    if not story or not isinstance(story, dict):
        return html
    if "And 已有经验" not in html and "角色任务：" not in html:
        return html
    title = escape_html(story.get("title") or f"为什么要学「{topic}」")
    lead = escape_html(story.get("lead") or "")
    known = escape_html(story.get("known") or "")
    stuck = escape_html(story.get("stuck") or "")
    task = escape_html(story.get("task") or "")
    new_story = (
        f'<section class="section" id="story" data-tts="story" data-tsh="真实情境">'
        f'<div class="lesson-panel"><span class="phase-tag">真实情境</span>'
        f'<h2>{title}</h2><p>{lead}</p><div class="mini-grid">'
        f'<div class="mini-panel"><h3>已有经验</h3><p>{known}</p></div>'
        f'<div class="mini-panel"><h3>真正卡点</h3><p>{stuck}</p></div>'
        f'<div class="mini-panel"><h3>本课任务</h3><p>{task}</p></div>'
        f"</div></div></section>"
    )
    html2, n = re.subn(
        r'<section class="section" id="story"[^>]*>.*?</section>',
        new_story,
        html,
        count=1,
        flags=re.S,
    )
    return html2 if n else html


def render_upgrade_html(data: dict, topic: str) -> str:
    mcqs = data.get("mcqs") or []
    fills = data.get("fills") or []
    ct = data.get("conceptest") or {}
    inq = data.get("inquiry") or {}

    parts = [MARKER, f'<!-- upgrade topic: {escape_html(topic)} -->']

    # 真题卷
    parts.append(
        '<section class="section teachany-upgrade-block" data-bloom-level="evaluate" '
        'data-scaffold="partial">'
        "<h2>📝 真题练习</h2>"
        '<p style="opacity:.85;margin-bottom:12px">先独立作答，再点选项查看对错与错因。</p>'
    )
    for i, q in enumerate(mcqs[:3], 1):
        stem = escape_html(q.get("stem", ""))
        ans = str(q.get("answer", "A")).upper()[:1]
        explain = escape_html(q.get("explain", ""))
        wrong = q.get("wrong") or {}
        parts.append(f'<div class="tu-q" data-answer="{ans}">')
        parts.append(f"<h3>选择题 {i}</h3><p>{stem}</p><div class=\"tu-opts\">")
        for opt in q.get("options") or []:
            letter = str(opt).strip()[:1].upper()
            diag = escape_html(wrong.get(letter, explain if letter == ans else "再想想"))
            if letter == ans:
                diag = explain
            parts.append(
                f'<button type="button" class="tu-opt" data-choice="{letter}" '
                f'data-diagnosis="{diag}">{escape_html(opt)}</button>'
            )
        parts.append('</div><div class="tu-fb" hidden></div></div>')
    for i, q in enumerate(fills[:2], 1):
        parts.append(
            f'<div class="tu-fill"><h3>填空题 {i}</h3>'
            f'<p>{escape_html(q.get("stem", ""))}</p>'
            f'<details><summary>查看答案与解析</summary>'
            f'<p><strong>答案：</strong>{escape_html(q.get("answer", ""))}</p>'
            f'<p>{escape_html(q.get("explain", ""))}</p></details></div>'
        )
    parts.append("</section>")

    # ConcepTest 互动
    ct_stem = escape_html(ct.get("stem", "请判断下列说法"))
    ct_ans = str(ct.get("answer", "A")).upper()[:1]
    ct_diag = ct.get("diagnosis") or {}
    parts.append(
        '<section class="section teachany-upgrade-block" data-interactive="conceptest" '
        'data-conceptest="true" data-bloom-level="understand" data-scaffold="full">'
        "<h2>💡 概念检测（互动）</h2>"
        f"<p>{ct_stem}</p><div class=\"tu-opts tu-concept\">"
    )
    for opt in ct.get("options") or []:
        letter = str(opt).strip()[:1].upper()
        diag = escape_html(ct_diag.get(letter, ""))
        correct = "true" if letter == ct_ans else "false"
        parts.append(
            f'<button type="button" class="tu-opt" data-choice="{letter}" '
            f'data-correct="{correct}" data-diagnosis="{diag}">{escape_html(opt)}</button>'
        )
    parts.append('</div><div class="tu-fb" hidden></div></section>')

    # 探究记录互动
    parts.append(
        '<section class="section teachany-upgrade-block" data-interactive="inquiry" '
        'data-bloom-level="create" data-scaffold="partial">'
        f'<h2>🔬 {escape_html(inq.get("title") or "探究记录")}</h2>'
        f'<p>{escape_html(inq.get("prompt") or "写下你的假设、证据与结论。")}</p>'
        '<div class="tu-inquiry">'
        f'<label>💡 我的假设<textarea data-inq="h" placeholder="{escape_html(inq.get("hypothesis", ""))}"></textarea></label>'
        f'<label>📊 我的证据<textarea data-inq="e" placeholder="{escape_html(inq.get("evidence", ""))}"></textarea></label>'
        f'<label>✅ 我的结论<textarea data-inq="c" placeholder="{escape_html(inq.get("conclusion", ""))}"></textarea></label>'
        '</div>'
        '<button type="button" class="tu-save">保存探究记录（本机）</button>'
        '<div class="tu-fb" data-inq-fb hidden></div>'
        "</section>"
    )

    css = (
        f'<style id="{UPGRADE_CSS_ID}">'
        ".teachany-upgrade-block{margin:28px 0;padding:22px;border-radius:16px;"
        "border:1px solid rgba(148,163,184,.25);background:rgba(15,23,42,.35)}"
        ".tu-q,.tu-fill{margin:16px 0;padding:14px;border-radius:12px;background:rgba(30,41,59,.45)}"
        ".tu-opts{display:grid;gap:10px;margin-top:10px}"
        ".tu-opt{text-align:left;padding:12px 14px;border-radius:10px;border:1px solid rgba(148,163,184,.35);"
        "background:rgba(51,65,85,.55);color:inherit;cursor:pointer;font-size:15px;line-height:1.5}"
        ".tu-opt:hover{border-color:#60a5fa}"
        ".tu-opt.is-right{border-color:#34d399;background:rgba(16,185,129,.18)}"
        ".tu-opt.is-wrong{border-color:#f87171;background:rgba(239,68,68,.15)}"
        ".tu-fb{margin-top:12px;padding:12px;border-radius:10px;background:rgba(245,158,11,.12);"
        "border:1px solid rgba(245,158,11,.35);line-height:1.7}"
        ".tu-inquiry{display:grid;gap:12px;margin:14px 0}"
        ".tu-inquiry textarea{width:100%;min-height:72px;margin-top:6px;border-radius:8px;"
        "padding:10px;border:1px solid rgba(148,163,184,.3);background:rgba(15,23,42,.5);color:inherit}"
        ".tu-save{margin-top:8px;padding:10px 16px;border-radius:10px;border:0;background:#3b82f6;"
        "color:#fff;cursor:pointer;font-weight:600}"
        "details{margin-top:8px} summary{cursor:pointer;color:#93c5fd}"
        "</style>"
    )
    js = (
        f'<script id="{UPGRADE_JS_ID}">'
        "(function(){"
        "function bind(root){"
        "root.querySelectorAll('.tu-q,.teachany-upgrade-block[data-interactive=\"conceptest\"]').forEach(function(box){"
        "var ans=box.getAttribute('data-answer');"
        "var fb=box.querySelector('.tu-fb');"
        "box.querySelectorAll('.tu-opt').forEach(function(btn){"
        "btn.addEventListener('click',function(){"
        "var ch=btn.getAttribute('data-choice');"
        "var correct=btn.getAttribute('data-correct');"
        "var ok=(correct==='true')||(ans&&ch===ans);"
        "box.querySelectorAll('.tu-opt').forEach(function(b){b.classList.remove('is-right','is-wrong');});"
        "btn.classList.add(ok?'is-right':'is-wrong');"
        "if(fb){fb.hidden=false;fb.textContent=(ok?'✅ ':'❌ ')+(btn.getAttribute('data-diagnosis')||'');}"
        "});});});"
        "root.querySelectorAll('.tu-save').forEach(function(btn){"
        "btn.addEventListener('click',function(){"
        "var sec=btn.closest('section');"
        "var payload={};"
        "sec.querySelectorAll('[data-inq]').forEach(function(t){payload[t.getAttribute('data-inq')]=t.value;});"
        "try{localStorage.setItem('teachany_inq_'+location.pathname,JSON.stringify(payload));}catch(e){}"
        "var fb=sec.querySelector('[data-inq-fb]');"
        "if(fb){fb.hidden=false;fb.textContent='已保存到本机。继续完善证据会让结论更扎实。';}"
        "});});}"
        "if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){bind(document);});"
        "else bind(document);"
        "})();</script>"
    )
    parts.append(css)
    parts.append(js)
    return "\n".join(parts) + "\n"


def inject_html(html: str, block: str) -> str:
    # 去掉旧 v2 块（若半写入）
    if MARKER in html:
        html = re.sub(
            r"<!-- teachany-upgrade-v2 -->.*?(?=(<!--\s*v7\.7\.4 标准知识图谱模块|</body>))",
            "",
            html,
            flags=re.S,
        )
    if UPGRADE_CSS_ID in html:
        html = re.sub(rf'<style id="{UPGRADE_CSS_ID}">.*?</style>', "", html, flags=re.S)
    if UPGRADE_JS_ID in html:
        html = re.sub(rf'<script id="{UPGRADE_JS_ID}">.*?</script>', "", html, flags=re.S)

    anchor = re.search(r"<!--\s*v7\.7\.4 标准知识图谱模块", html)
    if anchor:
        return html[: anchor.start()] + block + html[anchor.start() :]
    bpos = html.rfind("</body>")
    if bpos >= 0:
        return html[:bpos] + block + html[bpos:]
    return html + block


def agnes_quota_remaining(cid: str) -> int:
    try:
        r = subprocess.run(
            [sys.executable, str(AGNES), "--course-id", cid, "--quota"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        m = re.search(r"\{[\s\S]*\}", r.stdout or "")
        if not m:
            return 0
        data = json.loads(m.group(0))
        course = data.get("course") or data
        return int(course.get("remaining") or 0)
    except Exception:
        return 0


def gen_agnes_images(cid: str, topic: str, labels: list[str], subject_cn: str) -> str:
    assets = COMMUNITY / cid / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    remaining = agnes_quota_remaining(cid)
    if remaining <= 0:
        return "跳过生图(额度用尽)"

    label_str = "、".join([str(x).strip() for x in (labels or []) if str(x).strip()][:4])
    if not label_str:
        label_str = topic

    n = min(3, remaining)
    prompts = []
    specs = [
        (
            "hero",
            "hero",
            f"教育信息图封面，深色背景，扁平矢量，主题《{topic}》（{subject_cn}）。"
            f"图中必须清晰印出中文标注：{label_str}。禁止英文乱码，禁止水印。",
        ),
        (
            "section1",
            "section1",
            f"《{topic}》核心概念结构图，扁平教育插画，深色背景，"
            f"用中文卡片标注：{label_str}。文字清晰可读。",
        ),
        (
            "section2",
            "section2",
            f"《{topic}》易错点对比示意，扁平教育插画，"
            f"中文标注正确/错误对照与关键词：{label_str}。",
        ),
    ]
    for name, slot, prompt in specs[:n]:
        prompts.append({"name": name, "slot": slot, "prompt": prompt})

    batch = assets / ".agnes_upgrade_batch.json"
    batch.write_text(json.dumps(prompts, ensure_ascii=False), encoding="utf-8")
    try:
        r = subprocess.run(
            [
                sys.executable,
                str(AGNES),
                "--course-id",
                cid,
                "--batch",
                str(batch),
                "--out-dir",
                str(assets),
            ],
            capture_output=True,
            text=True,
            timeout=480,
        )
    finally:
        if batch.exists():
            batch.unlink()
    pngs = list(assets.glob("*.png")) + list(assets.glob("*.webp"))
    if r.returncode != 0 and len(pngs) == 0:
        return f"生图失败: {(r.stdout or r.stderr)[-240:]}"
    return f"生图完成(剩余额度曾={remaining}, 现有图={len(pngs)})"


def link_images(cid: str) -> str:
    # 复用 link_images.link_one，但放宽：允许 upgrade-v2 标记
    from link_images import link_one

    d = COMMUNITY / cid
    html_path = d / "index.html"
    html = html_path.read_text(encoding="utf-8")
    if MARKER not in html and "<!-- teachany-enhanced -->" not in html:
        return "跳过链图(内容未升级)"
    # 临时保证 enhanced 标记，便于 link_one 通过
    if "<!-- teachany-enhanced -->" not in html:
        html_path.write_text(html.replace(MARKER, MARKER + "\n<!-- teachany-enhanced -->\n"), encoding="utf-8")
    return link_one(cid)


def upgrade_one(cid: str, skip_images: bool = False, force: bool = False) -> str:
    d = COMMUNITY / cid
    html_path = d / "index.html"
    mf_path = d / "manifest.json"
    if not html_path.exists():
        return f"{cid}: 跳过(无 index.html)"

    html = html_path.read_text(encoding="utf-8")
    if MARKER in html and not force:
        return f"{cid}: 已升级 v2，跳过"

    manifest = {}
    if mf_path.exists():
        try:
            manifest = json.loads(mf_path.read_text(encoding="utf-8"))
        except Exception:
            manifest = {}
    node_id = manifest.get("node_id") or cid
    topic, subj_cn, grade = resolve_topic(manifest, cid, html)
    if not topic:
        return f"{cid}: 跳过(无真实主题)"

    try:
        data = llm_upgrade_pack(topic, subj_cn, grade, node_id)
    except Exception as e:
        return f"{cid}: LLM 失败 - {e}"

    if len(data.get("mcqs") or []) < 2:
        return f"{cid}: 真题不足"

    html = rewrite_abt_shell(html, topic, data.get("story"))
    block = render_upgrade_html(data, topic)
    html2 = inject_html(html, block)
    html_path.write_text(html2, encoding="utf-8")

    img_msg = "跳过生图"
    if not skip_images:
        try:
            img_msg = gen_agnes_images(cid, topic, data.get("image_labels") or [], subj_cn)
        except Exception as e:
            img_msg = f"生图异常:{e}"
        try:
            link_msg = link_images(cid)
        except Exception as e:
            link_msg = f"链图异常:{e}"
    else:
        link_msg = "跳过链图"

    return f"{cid}: 升级成功 | {img_msg} | {link_msg} | 主题={topic}"


def main():
    args = sys.argv[1:]
    skip_images = False
    force = False
    force_batch = False
    limit = None
    cids: list[str] = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--skip-images":
            skip_images = True
        elif a == "--force":
            force = True
        elif a == "--force-batch":
            force_batch = True
        elif a.startswith("--limit="):
            limit = int(a.split("=", 1)[1])
        elif a.startswith("--file="):
            path = a.split("=", 1)[1]
            cids = [ln.strip() for ln in open(path, encoding="utf-8") if ln.strip()]
        elif a.startswith("-"):
            print(f"unknown flag: {a}")
            return
        else:
            cids.append(a)
        i += 1

    if not cids:
        print(
            "usage: pipeline_upgrade_v2.py <cid>... | --file=ids.txt "
            "[--limit=N] [--skip-images] [--force] [--force-batch]"
        )
        return
    if len(cids) >= 5 and not force_batch:
        print(
            f"拒绝批量 {len(cids)} 门：请先单课打磨，或加 --force-batch。"
            "样板：community/phy-m-pressure（已去 And/But/Therefore 空壳）。"
        )
        return
    if limit is not None:
        cids = cids[:limit]

    ok = skip = fail = 0
    for cid in cids:
        try:
            res = upgrade_one(cid, skip_images=skip_images, force=force)
        except Exception as e:
            res = f"{cid}: 异常 - {e}"
        print(res, flush=True)
        if "升级成功" in res:
            ok += 1
        elif "跳过" in res:
            skip += 1
        else:
            fail += 1
        time.sleep(1.5)
    print(f"\n升级结束：成功={ok} 跳过={skip} 失败={fail}")


if __name__ == "__main__":
    main()
