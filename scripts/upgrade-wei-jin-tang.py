#!/usr/bin/env python3
"""upgrade-wei-jin-tang.py — hist-h-wei-jin-tang 手术升级（理想课件重构试点）
重做：
1. concept 官话页 → 历史脉络全景页（四阶段时间轴卡）
2. lesson-focus 90字 → 四卡加厚（政权脉络/交融开发/制度创新/盛唐气象）
3. 新增 module-2（孝文帝改革与民族交融）、module-3（盛唐繁荣与开放）
4. 地图 desc 占位文本 → 真史实描述
保留：cover/objectives/anchor/pretest/地图/概念归类/module-1/lesson-method
      /易错辨析/概念检测/探究/AI模块/error-clinic/memory-anchor/posttest/course-nav-map
幂等：<!-- ideal-upgrade-v1 -->
用法: python3 upgrade-wei-jin-tang.py [--dry]
"""
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CID = "hist-h-wei-jin-tang"
P = ROOT / "community" / CID / "index.html"
API_KEY = os.environ["OPENROUTER_API_KEY"]
MODEL = os.environ.get("ZH_MODEL", "deepseek/deepseek-chat-v3-0324")
DRY = "--dry" in sys.argv
MARK = "<!-- ideal-upgrade-v1 -->"

PROMPT = """你是中国高中历史教师，按《中外历史纲要（上）》教材体系编写课件内容。
课标要求：通过了解三国两晋南北朝政权更迭的历史脉络、隋唐时期封建社会的高度繁荣，认识这一时期的制度变化与创新、民族交融、区域开发和思想文化新成就。
课件已有真模块（保持呼应、不要重复其内容）：门阀兴衰专题（九品中正到科举、琅琊王氏、寒门比例12%→38%）、易错辨析（三国鼎立时间差/九品中正vs科举/藩镇割据）、概念检测（世说新语清谈）。

生成以下五块内容，严格输出 JSON（不要 markdown 围栏）：
{{
 "timeline": [
   {{"period": "三国两晋（220-316）", "text": "45-65字"}},
   {{"period": "东晋十六国与南北朝（317-589）", "text": "45-65字"}},
   {{"period": "隋朝（581-618）", "text": "45-65字"}},
   {{"period": "唐朝（618-907）", "text": "45-65字"}}
 ],
 "focus": {{
   "vein": "政权脉络段（100-140字）",
   "fusion": "交融开发段（100-140字）",
   "institution": "制度创新段（100-140字）",
   "glory": "盛唐气象段（100-140字）"
 }},
 "module2": {{
   "title": "孝文帝改革与民族交融",
   "and": "20-30字学生已知",
   "but": "25-35字认知冲突",
   "therefore": "20-30字学习目标",
   "explain": "90-130字讲解（含具体史实/措施/影响，如迁都洛阳494年、汉化措施、均田制）",
   "analogy": "50-80字现代类比（🌍开头）",
   "quiz": {{"q": "即练题干", "opts": ["A...","B...","C...","D..."], "ans": 0, "diag": "错因诊断30字内"}}
 }},
 "module3": {{
   "title": "盛唐繁荣与开放",
   "and": "20-30字",
   "but": "25-35字",
   "therefore": "20-30字",
   "explain": "90-130字（贞观之治/开元盛世具体表现、长安国际化、对外交流史实）",
   "analogy": "50-80字（🌍开头）",
   "quiz": {{"q": "题干", "opts": ["A...","B...","C...","D..."], "ans": 1, "diag": "30字内"}}
 }},
 "mapdesc": {{
   "three_kingdoms": "30-50字三国两晋地图史实描述",
   "tang": "30-50字隋唐地图史实描述"
 }}
}}
要求：史实准确（年代/制度名/人物），文字有教学感，严禁"具有重要意义"类空话。"""


def llm_json(body):
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps({"model": MODEL,
                                 "messages": [{"role": "user", "content": body}],
                                 "temperature": 0.5, "max_tokens": 2800}).encode(),
                headers={"Authorization": f"Bearer {API_KEY}",
                         "Content-Type": "application/json",
                         "HTTP-Referer": "https://teachany.cn",
                         "X-OpenRouter-Title": "ideal-upgrade"})
            with urllib.request.urlopen(req, timeout=150) as r:
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


def build_timeline_page(timeline):
    cards = "".join(
        f'<div class="mini-panel"><h3>{esc(t["period"])}</h3><p>{esc(t["text"])}</p></div>'
        for t in timeline)
    return (f'<div class="slide-inner"><div class="card">'
            f'<span class="phase-tag">Overview</span>'
            f'<h2>历史脉络全景：从分裂到再统一的四百年</h2>'
            f'<div class="mini-grid">{cards}</div>'
            f'<p class="feedback"><strong>看脉络：</strong>把四百年读成一条线——分裂中孕育交融，交融中重建统一，统一中走向鼎盛。</p>'
            f'</div></div>')


def build_focus_cards(focus):
    return (
        f'<div class="card focus-detail"><p><strong>政权脉络：</strong>{esc(focus["vein"])}</p></div>\n'
        f'<div class="card focus-detail"><p><strong>交融与开发：</strong>{esc(focus["fusion"])}</p></div>\n'
        f'<div class="card focus-detail"><p><strong>制度创新：</strong>{esc(focus["institution"])}</p></div>\n'
        f'<div class="card focus-detail"><p><strong>盛唐气象：</strong>{esc(focus["glory"])}</p></div>')


def build_module(mid, m):
    opts = "".join(
        f'<button type="button" class="tu-opt" data-choice="{chr(65+i)}" data-diagnosis="{esc(m["quiz"]["diag"])}">{chr(65+i)}. {esc(o)}</button>'
        for i, o in enumerate(m["quiz"]["opts"]))
    return (
        f'<section class="section teachany-upgrade-block" data-bloom-level="understand" data-scaffold="partial" id="{mid}">'
        f'<h2>📖 {esc(m["title"])}</h2>'
        f'<div class="tu-q"><p><strong>And：</strong>{esc(m["and"])}</p>'
        f'<p><strong>But：</strong>{esc(m["but"])}</p>'
        f'<p><strong>Therefore：</strong>{esc(m["therefore"])}</p></div>'
        f'<div class="tu-q"><p>{esc(m["explain"])}</p></div>'
        f'<div class="tu-q"><p>{esc(m["analogy"])}</p></div>'
        f'<div class="tu-q" data-answer="{chr(65+int(m["quiz"]["ans"]))}"><h3>🏋️ 即练</h3><p>{esc(m["quiz"]["q"])}</p>'
        f'<div class="tu-opts">{opts}</div><div class="tu-fb" hidden></div></div>'
        f'</section>')


def main():
    html = P.read_text(encoding="utf-8")
    if MARK in html:
        print("已升级")
        return
    d = llm_json(PROMPT)
    (ROOT / "scripts" / "wei-jin-tang-upgrade-content.json").write_text(
        json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    actions = []

    # 1) concept 官话页 → 全景页（替换 slide-inner 内容）
    m = re.search(
        r'(<section class="slide-page"[^>]*data-tsh="核心 - 三国两晋南北朝与隋唐"[^>]*>)[\s\S]*?(</section>)',
        html)
    if m:
        html = html[:m.start()] + m.group(1) + build_timeline_page(d["timeline"]) + m.group(2) + html[m.end():]
        actions.append("全景页")

    # 2) lesson-focus 加厚（原 p 后追加四卡）
    m2 = re.search(r'(id="lesson-focus"[\s\S]*?</div>)(\s*</section>)', html)
    if m2:
        html = html[:m2.start()] + m2.group(1) + "\n" + build_focus_cards(d["focus"]) + m2.group(2) + html[m2.end():]
        actions.append("精讲加厚")

    # 3) module-2/3 插到 module-1 之后
    m3 = re.search(r'(<section class="section teachany-upgrade-block"[^>]*id="module-1">[\s\S]*?</section>)', html)
    if m3:
        mods = build_module("module-2", d["module2"]) + "\n" + build_module("module-3", d["module3"])
        html = html[:m3.end(1)] + "\n" + mods + html[m3.end(1):]
        actions.append("模块+2")

    # 4) 地图 desc 占位 → 真史实
    html2 = re.sub(r'"desc": "[^"]*三国两晋[^"]*相关史实地图[^"]*"',
                   '"desc": "' + d["mapdesc"]["three_kingdoms"] + '"', html)
    html2 = re.sub(r'"desc": "[^"]*隋唐[^"]*相关史实地图[^"]*"',
                   '"desc": "' + d["mapdesc"]["tang"] + '"', html2)
    if html2 != html:
        html = html2
        actions.append("地图desc")

    if not actions:
        print("无可升级项")
        return
    html = html.replace("</body>", MARK + "\n</body>", 1)
    if not DRY:
        P.write_text(html, encoding="utf-8")
    print(f"升级完成: {'、'.join(actions)}")


if __name__ == "__main__":
    main()
