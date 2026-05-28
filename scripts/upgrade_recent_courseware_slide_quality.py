#!/usr/bin/env python3
"""Upgrade recent generated TeachAny courseware with slide-v2 mode and anti-shell evidence sections.

Scope: recent CN batches generated in the last production sprint:
- high chemistry / physics / geography
- middle physics / chinese

This is intentionally a post-processor: it preserves existing standard module wiring,
then adds presentation-mode structure and course-specific evidence content.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"
UPGRADE_TAG = "data-upgrade-20260528"

TARGET_TREES = [
    ("cn/high/chemistry.json", "chemistry"),
    ("cn/high/physics.json", "physics"),
    ("cn/high/geography.json", "geography"),
    ("cn/middle/physics.json", "physics"),
    ("cn/middle/chinese.json", "chinese"),
]

# Existing legacy pages that already predate this batch and fail unrelated old
# quality gates should not be touched by the recent-batch postprocessor.
EXCLUDE_IDS = {"chem-h-aluminum-compounds"}

GENERIC_REPLACEMENTS = {
    "语文不是背模板，而是在具体语言材料中找到证据、方法和效果。": "语文答题要从题干动词进入原文，把可圈画的依据、可命名的方法和可说明的效果连成证据链。",
    "不能只凭印象回答": "要用原文细节回答",
    "先判断任务": "先识别题干动词",
    "任务识别—圈画证据—解释方法—组织答案": "题干动词—原文证据—方法名称—效果表述",
    "从实验现象到变量关系": "从可观察现象到可测变量",
    "先观察现象，再控制变量": "先固定条件，再改变一个变量",
    "用地图、图表和过程证据": "用图例、坐标和区域案例",
    "不是孤立知识点": "需要放进具体区域和尺度",
    "不是单纯换一个题目名称": "不要把新情境当成旧公式替换题",
    "换一个场景，仍然从": "换到新情境时，仍需从",
}


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def load_targets() -> list[dict]:
    targets: list[dict] = []
    seen = set()
    for rel, subject in TARGET_TREES:
        tree_path = ROOT / "data/trees" / rel
        if not tree_path.exists():
            continue
        tree = json.loads(tree_path.read_text(encoding="utf-8"))
        level = rel.split("/")[1]
        for domain in tree.get("domains", []):
            for node in domain.get("nodes", []):
                cid = node.get("id")
                if not cid or cid in seen or cid in EXCLUDE_IDS:
                    continue
                course_dir = ROOT / "community" / cid
                html_path = course_dir / "index.html"
                if html_path.exists():
                    html_text = html_path.read_text(encoding="utf-8", errors="ignore")
                    if 'http-equiv="refresh"' in html_text or "location.replace('../" in html_text:
                        continue
                    seen.add(cid)
                    targets.append({
                        "id": cid,
                        "subject": subject,
                        "level": level,
                        "domain": domain.get("name") or domain.get("id") or "",
                        "domain_id": domain.get("id") or "",
                        "name": node.get("name") or cid,
                        "grade": node.get("grade") or "",
                        "curriculum_points": node.get("curriculum_points") or [],
                    })
    return targets


def detect_topic(name: str, subject: str) -> dict:
    text = name.lower()
    # Concrete examples are compact by design; the point is to stop pure framework-only pages.
    if subject == "chinese":
        if any(k in name for k in ["文言", "古诗", "诗词"]):
            sample = "示例文本：‘明月松间照，清泉石上流’不是只写景，而是用清冷明净的意象承载心境。"
            method = "抓意象、炼字和句式，解释它们怎样共同指向情感。"
        elif any(k in name for k in ["写作", "作文", "描写"]):
            sample = "示例任务：把‘我很感动’改成一个动作、一个细节和一句环境描写，让情绪自己显出来。"
            method = "审题定中心，材料只保留能服务中心的细节。"
        elif any(k in name for k in ["小说", "名著", "整本书", "西游", "红楼", "骆驼", "水浒"]):
            sample = "示例材料：人物在关键冲突中的选择，比单纯复述情节更能说明形象。"
            method = "按人物关系、情节转折和主题线索建立阅读卡片。"
        elif "议论" in name:
            sample = "示例判断：一个论据能否支撑论点，要看它是否回答了‘为什么’而不是只举热闹例子。"
            method = "先找中心论点，再核对论据类型和论证链条。"
        else:
            sample = "示例句：‘他的话像一束光’中的‘光’不是普通名词，而是让抽象影响变得可感。"
            method = "把本义、语境义和表达效果拆开写。"
        return {"case": sample, "method": method, "mistake": "只写术语、不引原文、不说明效果，是最常见失分点。"}

    if subject == "geography":
        if any(k in name for k in ["气候", "大气", "天气", "环流"]):
            case = "区域案例：比较伦敦、北京和新加坡，先读气温降水图，再回到纬度、海陆位置和大气环流。"
            method = "先判水热组合，再解释气压带、风带、季风或地形影响。"
        elif any(k in name for k in ["水", "河", "洋流"]):
            case = "区域案例：黄河流域要同时看补给、径流季节变化、含沙量和人类调水工程。"
            method = "画出水从哪里来、到哪里去、在哪个环节被人类活动改变。"
        elif any(k in name for k in ["城市", "人口", "产业", "工业", "农业", "交通", "服务"]):
            case = "区域案例：长三角城市群的产业分工，要同时看市场、交通、劳动力、技术和政策。"
            method = "先描述空间集聚或扩散，再解释区位因素和区域联系。"
        elif any(k in name for k in ["板块", "地貌", "地壳", "灾害"]):
            case = "区域案例：日本多火山地震，不能只说‘位于板块交界’，还要说明边界类型和防灾体系。"
            method = "从内外力过程、地貌证据和人类风险暴露三层解释。"
        else:
            case = "区域案例：同一个地理规律放到不同尺度，可能出现不同主导因素。"
            method = "先定位区域和尺度，再读图例、指标和时间范围。"
        return {"case": case, "method": method, "mistake": "只描述‘哪里多哪里少’，不解释图层指标和成因链，是典型空答案。"}

    if subject == "physics":
        if any(k in name for k in ["声", "噪声"]):
            case = "实验例子：拨动橡皮筋时纸屑跳动，能把看不见的振动放大成可观察证据。"
            method = "先找振动声源，再判断介质、频率、振幅和听感。"
        elif any(k in name for k in ["光", "镜", "透镜", "视觉", "折射"]):
            case = "实验例子：铅笔插入水中看起来弯折，是光从水进入空气时传播方向改变。"
            method = "先画光路，再比较入射角、反射角或折射角。"
        elif any(k in name for k in ["电", "电路", "电压", "电流", "电阻", "欧姆", "焦耳"]):
            case = "实验例子：同一小灯泡接入不同电压时亮度变化，要用电压、电流和电阻一起解释。"
            method = "先画闭合回路，再区分串并联和电表连接方式。"
        elif any(k in name for k in ["磁", "电动机", "发电", "感应"]):
            case = "实验例子：闭合线圈切割磁感线时出现电流，说明机械运动可以转化为电能。"
            method = "看电流方向、磁场方向和相对运动是否同时满足。"
        elif any(k in name for k in ["热", "温度", "物态", "内能", "比热"]):
            case = "实验例子：同样加热水和沙，温度变化不同，说明比热容决定吸热升温能力。"
            method = "先分清温度、热量和内能，再看吸热放热过程。"
        else:
            case = "实验例子：改变一个变量并保持其他条件不变，才能判断现象变化来自哪里。"
            method = "先画研究对象和受力/能量/运动关系，再代入公式。"
        return {"case": case, "method": method, "mistake": "不说明控制变量和测量证据，直接套公式，是物理题常见空架子。"}

    if subject == "chemistry":
        if any(k in name for k in ["离子", "方程"]):
            case = "实验例子：AgNO₃ 与 NaCl 混合产生白色沉淀，净变化是 Ag⁺ 与 Cl⁻ 生成 AgCl。"
            method = "先拆强电解质，再删旁观离子，最后检查电荷和原子守恒。"
        elif any(k in name for k in ["有机", "官能", "烃"]):
            case = "实验例子：乙烯能使溴水褪色，关键证据是碳碳双键发生加成。"
            method = "先识别碳骨架和官能团，再判断典型反应。"
        elif any(k in name for k in ["平衡", "速率", "勒夏"]):
            case = "实验例子：合成氨条件选择不是只追求高产率，还要折中速率、成本和设备安全。"
            method = "分清速率问题和平衡移动问题，催化剂只改速率不改平衡位置。"
        else:
            case = "实验例子：观察颜色、沉淀、气体或热量变化，要回到微粒、价态和守恒解释。"
            method = "先判物质类别和微粒变化，再写方程或定量关系。"
        return {"case": case, "method": method, "mistake": "只背概念不看实验现象、微粒变化和守恒条件，会导致结论空泛。"}
    return {"case": "本课需要一个具体课堂案例支撑，不接受纯框架描述。", "method": "先找证据，再解释机制。", "mistake": "只写抽象框架会变成空架子。"}


def evidence_section(target: dict) -> str:
    name = target["name"]
    subject = target["subject"]
    topic = detect_topic(name, subject)
    points = target.get("curriculum_points") or []
    cp = points[0] if points else f"围绕{name}形成可迁移的学科理解。"
    if len(cp) > 110:
        cp = cp[:108] + "…"
    return f'''
<section class="section" id="knowledge-specific-evidence" {UPGRADE_TAG}="true" data-tts="knowledge-specific-evidence" data-tsh="专属证据 - 用本知识点的事实补足理解" data-bloom-level="analyze" data-scaffold="partial">
  <div class="lesson-panel specificity-panel">
    <span class="phase-tag">Specific Evidence</span>
    <h2>{esc(name)}：本课专属证据包</h2>
    <div class="mini-grid specificity-table">
      <div class="mini-panel"><h3>课标锚点</h3><p>{esc(cp)}</p></div>
      <div class="mini-panel"><h3>具体案例</h3><p>{esc(topic['case'])}</p></div>
      <div class="mini-panel"><h3>分析方法</h3><p>{esc(topic['method'])}</p></div>
      <div class="mini-panel"><h3>避坑提醒</h3><p>{esc(topic['mistake'])}</p></div>
    </div>
    <p class="feedback"><strong>课堂任务：</strong>请用“现象/文本/地图/实验数据 → 关键证据 → 学科解释 → 迁移应用”四步，重写一个关于「{esc(name)}」的新问题。</p>
  </div>
</section>
'''


def slide_controls() -> str:
    return '''
<div class="slide-progress-bar" id="slide-progress-bar"></div>
<nav class="slide-sidenav" id="slide-sidenav" aria-label="分页导航"></nav>
<button aria-label="切换播放模式" class="play-mode-fab" id="play-mode-fab" title="播放模式 (F)">
  <svg id="fab-icon-play" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"></path></svg>
  <svg id="fab-icon-browse" style="display:none" viewBox="0 0 24 24"><path d="M4 6h16v2H4zM4 11h16v2H4zM4 16h16v2H4z"></path></svg>
</button>
<div class="slide-toolbar" id="slide-toolbar">
  <button class="toolbar-btn" id="tb-prev" type="button" aria-label="上一页">‹</button>
  <div class="toolbar-page-info" id="tb-page-info">1 / 1</div>
  <button class="toolbar-btn" id="tb-next" type="button" aria-label="下一页">›</button>
  <div class="toolbar-progress" id="tb-progress"><div class="toolbar-progress-fill" id="tb-progress-fill"></div></div>
  <button class="toolbar-btn" id="tb-autoplay" type="button" aria-label="自动播放">Auto</button>
  <button class="toolbar-btn" id="tb-fullscreen" type="button" aria-label="全屏">⛶</button>
</div>
'''


def add_slide_assets(text: str) -> str:
    if "teachany-slide-v2.css" not in text:
        text = text.replace("</head>", '<link href="../../assets/teachany-slide-v2.css" rel="stylesheet"/>\n</head>')
    if "teachany-slide-v2.js" not in text:
        text = text.replace("</body>", '<script defer src="../../assets/teachany-slide-v2.js"></script>\n</body>')
    return text


def strip_existing_upgrade(text: str) -> str:
    text = re.sub(r'\n?<section class="section" id="knowledge-specific-evidence"[\s\S]*?</section>\s*', '\n', text)
    text = re.sub(r'\n?<div class="slide-progress-bar" id="slide-progress-bar"></div>[\s\S]*?<div class="slide-toolbar" id="slide-toolbar">[\s\S]*?</div>\s*</div>\s*', '\n', text)
    return text


def insert_evidence(text: str, target: dict) -> str:
    section = evidence_section(target)
    anchors = [
        '<section class="section" id="visual-evidence"',
        '<section class="section" id="interactive-lab"',
        '<section class="section" id="worked-example"',
    ]
    for anchor in anchors:
        idx = text.find(anchor)
        if idx != -1:
            return text[:idx] + section + text[idx:]
    marker = '<script src="../../assets/scripts/ai-tutor.js"'
    idx = text.find(marker)
    if idx != -1:
        return text[:idx] + section + text[idx:]
    return text.replace("</body>", section + "\n</body>")


def replace_generic(text: str) -> str:
    for old, new in GENERIC_REPLACEMENTS.items():
        text = text.replace(old, new)
    return text


def slide_title(block: str, fallback: str) -> str:
    m = re.search(r'data-tsh="([^"]+)"', block)
    if m:
        return m.group(1)[:40]
    m = re.search(r'<h[12][^>]*>(.*?)</h[12]>', block, re.S | re.I)
    if m:
        title = re.sub(r'<[^>]+>', '', m.group(1))
        return re.sub(r'\s+', ' ', title).strip()[:40]
    m = re.search(r'id="([^"]+)"', block)
    return (m.group(1) if m else fallback)[:40]


def ensure_slide_controls(text: str) -> str:
    if all(x in text for x in ['id="play-mode-fab"', 'id="slide-toolbar"', 'id="slide-sidenav"', 'id="slide-progress-bar"']):
        return text
    idx = text.find('<div class="slide-container" id="slide-container">')
    if idx == -1:
        idx = text.find('<div id="slide-container" class="slide-container">')
    if idx != -1:
        return text[:idx] + slide_controls() + text[idx:]
    return text


def wrap_slide_pages(text: str) -> str:
    # If already has slide-container, keep page structure and only ensure controls.
    if 'id="slide-container"' in text or "id='slide-container'" in text:
        return ensure_slide_controls(text)
    pattern = re.compile(r'<(header|section)\b[\s\S]*?</\1>', re.I)
    matches = list(pattern.finditer(text))
    if not matches:
        return text
    first, last = matches[0].start(), matches[-1].end()
    region = text[first:last]
    pieces = []
    pos = 0
    page_idx = 0
    for m in pattern.finditer(region):
        pieces.append(region[pos:m.start()])
        block = m.group(0)
        # Skip controls if any remain.
        title = slide_title(block, f"第{page_idx+1}页")
        pieces.append(f'<section class="slide-page" data-page-index="{page_idx}" data-page-type="content" data-tsh="{esc(title)}">\n{block}\n</section>')
        pos = m.end()
        page_idx += 1
    pieces.append(region[pos:])
    wrapped = slide_controls() + '\n<div class="slide-container" id="slide-container">\n' + ''.join(pieces) + '\n</div>\n'
    return text[:first] + wrapped + text[last:]


def upgrade_one(target: dict) -> dict:
    html_path = ROOT / "community" / target["id"] / "index.html"
    original = html_path.read_text(encoding="utf-8", errors="ignore")
    text = original
    text = strip_existing_upgrade(text)
    text = replace_generic(text)
    text = insert_evidence(text, target)
    text = add_slide_assets(text)
    text = wrap_slide_pages(text)
    if text != original:
        html_path.write_text(text, encoding="utf-8")
    slide_pages = text.count('class="slide-page"')
    return {
        "id": target["id"],
        "subject": target["subject"],
        "level": target["level"],
        "name": target["name"],
        "changed": text != original,
        "slide_pages": slide_pages,
        "has_slide_css": "teachany-slide-v2.css" in text,
        "has_slide_js": "teachany-slide-v2.js" in text,
        "has_evidence": "knowledge-specific-evidence" in text,
    }


def main() -> None:
    targets = load_targets()
    rows = [upgrade_one(t) for t in targets]
    REPORT_DIR.mkdir(exist_ok=True)
    out = REPORT_DIR / "recent-courseware-slide-quality-upgrade-2026-05-28.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"upgraded={sum(r['changed'] for r in rows)} scope={len(rows)} report={out}")
    missing = [r for r in rows if not (r["has_slide_css"] and r["has_slide_js"] and r["slide_pages"] >= 8 and r["has_evidence"])]
    print(f"missing_after_upgrade={len(missing)}")
    for r in missing[:20]:
        print("MISSING", r)


if __name__ == "__main__":
    main()
