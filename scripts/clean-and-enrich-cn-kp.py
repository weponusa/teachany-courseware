#!/usr/bin/env python3
"""Clean dirty CN KP satellite data and add subject-aware baseline content.

Safety policy:
- Only edits derived/enrichment fields: exercises, errors, textbook_content, supplements,
  real_world, and _meta.
- Keeps node metadata, curriculum_points, excerpts, and interactive_resources intact.
- Backs up every changed JSON before writing.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
KP_ROOT = ROOT / "data" / "kp"
KP_INDEX_PATH = KP_ROOT / "_index.json"
NODE_INDEX_PATH = ROOT / "data" / "node-index.json"

PLACEHOLDER_RE = re.compile(r"\[待补充[^\]]*\]|待补充|TODO|TBD|placeholder", re.I)
GENERIC_CURRICULUM_RE = re.compile(r"培养什么人、怎样培养人、为谁培养人|修订原则|坚持目标导向|坚持问题导向|课程方案|营造积极的课堂生态|师生关系|课堂氛围|不怕出错|大胆表达|教学建议|实施建议")
TEXTBOOK_REFERENCE_ONLY_RE = re.compile(r"OpenStax 教材资料|配图目录|具体文件待按知识点主题归类|暂无对应教材资料|原文：`|国家中小学智慧教育平台|参考资料|课程标准|教师教学用书")
TEXTBOOK_CONTENT_MARKER_RE = re.compile(r"定义|概念|原理|公式|步骤|例题|解：|实验|现象|规律|性质|应用|证明|推导|分析|阅读|表达|地图|语境")
HISTORY_TEMPLATE_RE = re.compile(r"年代与名词|史料|制度变迁|考古/文献|因果链|制度/经济/思想变化|只记年代")
MATH_TEMPLATE_RE = re.compile(r"学习数学的方法|数学来源于生活|数学思想方法|数学对象|数学探究")

SUBJECT_ZH = {
    "math": "数学",
    "physics": "物理",
    "chemistry": "化学",
    "biology": "生物学",
    "history": "历史",
    "geography": "地理",
    "chinese": "语文",
    "english": "英语",
    "science": "科学",
    "info-tech": "信息科技",
    "other": "综合学习",
}

SOURCE_TAG = "subject_enrichment_2026-06-01"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return json.dumps(value, ensure_ascii=False)


def is_placeholder_or_empty(text: str) -> bool:
    text = (text or "").strip()
    return not text or bool(PLACEHOLDER_RE.fullmatch(text))


def item_text(item: Any) -> str:
    return clean_text(item)


def curriculum_points(data: dict[str, Any]) -> list[str]:
    cps = [str(x).strip() for x in data.get("curriculum_points") or [] if str(x).strip()]
    if cps:
        return cps
    out: list[str] = []
    for ex in data.get("excerpts") or []:
        if isinstance(ex, dict):
            t = str(ex.get("text") or "").strip()
            if t:
                out.append(t)
    return out[:3]


def bad_textbook_text(text: str) -> bool:
    head = (text or "")[:3000]
    if not head.strip():
        return True
    if PLACEHOLDER_RE.search(head):
        return True
    if GENERIC_CURRICULUM_RE.search(head):
        return True
    if TEXTBOOK_REFERENCE_ONLY_RE.search(head) and len(TEXTBOOK_CONTENT_MARKER_RE.findall(head)) < 2:
        return True
    return False


def strip_placeholder_lines(md: str) -> tuple[str, bool]:
    if not md:
        return md, False
    changed = False
    lines: list[str] = []
    for line in md.splitlines():
        if (
            PLACEHOLDER_RE.search(line)
            or "暂无对应教材资料" in line
            or "具体文件待按知识点主题归类" in line
            or "OpenStax 教材资料" in line
            or "以下内容为课件制作时的补充参考资料" in line
        ):
            changed = True
            continue
        lines.append(line.rstrip())
    new = "\n".join(lines).strip() + "\n" if lines else ""
    return new, changed or new != md


def fix_math_template(md: str, subject: str) -> tuple[str, bool]:
    if not md or subject == "math":
        return md, False
    label = SUBJECT_ZH.get(subject, "本学科")
    replacements = {
        "掌握学习数学的方法": f"掌握学习{label}的方法",
        "运用数学思想方法": f"运用{label}学科方法",
        "数学来源于生活又服务于生活": f"{label}与现实生活密切相关",
        "相关的数学对象": "相关的概念、现象或材料",
        "数学探究": f"{label}探究",
        "数学思维和素养": f"{label}思维和素养",
        "学好数学的信心": f"学好{label}的信心",
    }
    new = md
    for old, repl in replacements.items():
        new = new.replace(old, repl)
    return new, new != md


def section_exists(md: str, keywords: tuple[str, ...]) -> bool:
    if not md:
        return False
    sections = re.split(r"(?=^#{2,4}\s+)", md, flags=re.M)
    for sec in sections:
        first = sec.splitlines()[0] if sec.splitlines() else ""
        if any(k in first for k in keywords):
            body = PLACEHOLDER_RE.sub("", sec)
            useful = [ln.strip(" -\t") for ln in body.splitlines() if ln.strip(" -\t") and not ln.startswith("#")]
            if len("\n".join(useful)) >= 40:
                return True
    return False


def teaching_methods(subject: str, name: str, cps: list[str]) -> list[str]:
    first = cps[0] if cps else f"理解{name}的核心概念与方法。"
    if subject == "math":
        return [
            f"从具体情境或图形表征切入，引导学生发现「{name}」中的数量关系，再抽象为符号、公式或模型。",
            "采用“操作体验—表达归纳—变式应用”的路径，帮助学生把直观经验转化为可迁移的数学方法。",
            f"围绕课标要点“{first[:80]}”，设置一题多解、数形结合或实际应用任务。",
        ]
    if subject == "physics":
        return [
            f"以可观察实验或生活现象引入「{name}」，先让学生描述现象，再提出可检验的问题。",
            "强调控制变量、数据记录、图像分析和单位意识，避免只记公式不理解条件。",
            f"围绕课标要点“{first[:80]}”，设计预测—实验—解释—迁移的学习链条。",
        ]
    if subject == "chemistry":
        return [
            f"从实验现象、微观粒子和符号表达三个层面讲解「{name}」，让学生把现象与本质对应起来。",
            "重视实验安全、证据记录、化学用语规范和条件限制，避免只背结论。",
            f"围绕课标要点“{first[:80]}”，安排观察、解释、书写表达和应用判断任务。",
        ]
    if subject == "biology":
        return [
            f"以结构与功能、生命过程或生态关系为主线组织「{name}」教学。",
            "通过图示、模型、实验或真实案例，引导学生解释生命现象背后的机制。",
            f"围绕课标要点“{first[:80]}”，设计观察记录、证据解释和生活应用任务。",
        ]
    if subject == "history":
        return [
            f"围绕时间线、空间位置、关键人物与制度变化组织「{name}」教学。",
            "用史料阅读、因果链分析和多角度评价，避免学生只背年代和事件名称。",
            f"围绕课标要点“{first[:80]}”，设计证据提取、历史解释和观点表达任务。",
        ]
    if subject == "geography":
        return [
            f"以地图、图表、区域案例和现实问题组织「{name}」教学。",
            "引导学生从位置、分布、联系、差异和人地关系角度分析地理现象。",
            f"围绕课标要点“{first[:80]}”，设计读图定位、资料分析和方案评价任务。",
        ]
    if subject == "chinese":
        return [
            f"以真实语篇、朗读体验和表达任务组织「{name}」教学。",
            "引导学生在读、品、说、写中理解语言材料，避免脱离文本空讲技巧。",
            f"围绕课标要点“{first[:80]}”，设计文本理解、语言品析和迁移表达任务。",
        ]
    if subject == "english":
        return [
            f"以真实语境和交际任务组织「{name}」教学，落实形式、意义、使用统一。",
            "通过听说读写综合活动，让学生先理解语境，再操练语言形式，最后完成表达任务。",
            f"围绕课标要点“{first[:80]}”，设计输入理解、控制操练和真实输出任务。",
        ]
    if subject == "info-tech":
        return [
            f"以任务或项目驱动「{name}」教学，让学生在操作中理解概念、流程和规范。",
            "重视算法思维、数据意识、网络安全和数字伦理，避免只会点击不会解释。",
            f"围绕课标要点“{first[:80]}”，设计分析问题、制定方案、实现验证和反思改进任务。",
        ]
    return [
        f"以观察、探究和表达任务组织「{name}」教学。",
        "引导学生基于证据解释现象，并把知识迁移到真实问题。",
        f"围绕课标要点“{first[:80]}”，设计问题驱动的学习活动。",
    ]


def extensions(subject: str, name: str) -> list[str]:
    if subject == "math":
        return [f"与前后知识点建立联系，比较「{name}」在不同题型中的表达方式。", "引入生活建模或跨学科数据问题，训练从实际情境抽象数学模型的能力。"]
    if subject == "physics":
        return [f"联系工程、能源、交通或日常生活中的相关现象，讨论「{name}」的应用边界。", "补充科学史或技术应用案例，帮助学生理解物理规律如何服务真实问题。"]
    if subject == "chemistry":
        return [f"联系材料、环境、医药或食品中的案例，讨论「{name}」的实际价值。", "补充安全实验、绿色化学或定量分析任务，提升证据意识。"]
    if subject == "biology":
        return [f"联系健康、生态、农业或生物技术案例，讨论「{name}」与现实生活的关系。", "通过模型图、显微图或调查资料拓展学生对生命系统的理解。"]
    if subject == "history":
        return [f"联系同一时期中外历史进程，比较「{name}」的背景、过程和影响。", "补充地图、年表、图片史料或人物材料，训练历史解释能力。"]
    if subject == "geography":
        return [f"联系本地案例、时事热点或地图工具，拓展「{name}」的现实应用。", "引导学生开展路线规划、区域比较、环境评价或社会调查。"]
    if subject == "chinese":
        return [f"联系同主题文本、整本书阅读或写作任务，拓展「{name}」的表达价值。", "通过朗读、仿写、比较阅读和生活表达提升语言运用能力。"]
    if subject == "english":
        return [f"联系生活话题、跨文化语境和项目任务，拓展「{name}」的真实使用场景。", "通过角色扮演、信息差任务、短文写作或口头展示提高语言迁移能力。"]
    if subject == "info-tech":
        return [f"联系数字生活、人工智能、数据安全或编程项目，拓展「{name}」的应用场景。", "鼓励学生优化作品、解释算法或反思技术伦理。"]
    return [f"联系生活、社会或跨学科案例，拓展「{name}」的应用场景。", "鼓励学生提出问题、收集证据并表达自己的解释。"]


def real_world_examples(subject: str, name: str) -> list[str]:
    mapping = {
        "math": f"在购物、行程、测量或数据分析中寻找与「{name}」相关的数量关系。",
        "physics": f"观察家用电器、交通工具、运动器材或自然现象中与「{name}」相关的物理规律。",
        "chemistry": f"从厨房、清洁用品、材料变化或环境问题中寻找与「{name}」相关的化学现象。",
        "biology": f"观察人体健康、植物生长、生态环境或食品生产中与「{name}」相关的生命现象。",
        "history": f"用地图、年表、文物图片或人物故事解释「{name}」与社会变化的关系。",
        "geography": f"结合家乡地图、天气资料、交通路线或区域新闻分析「{name}」的地理意义。",
        "chinese": f"在课文、课外阅读、日常交流和写作表达中运用「{name}」。",
        "english": f"围绕校园、家庭、兴趣、出行或节日话题，在真实交流中使用「{name}」。",
        "science": f"从校园、家庭和自然环境中观察与「{name}」相关的现象，并尝试提出解释。",
        "info-tech": f"在数字学习、信息搜索、作品制作或网络安全场景中应用「{name}」。",
    }
    return [mapping.get(subject, f"在真实生活或跨学科任务中应用「{name}」。")]


def generated_content_summary(subject: str, name: str, cps: list[str]) -> str:
    label = SUBJECT_ZH.get(subject, "本学科")
    cp_text = cps[0] if cps else f"理解{name}的基本概念、方法与应用。"
    methods = teaching_methods(subject, name, cps)
    return (
        "## 教材化讲解参考（由课标要点生成）\n\n"
        f"### 核心概念\n{name}是{label}学习中的重要知识点。教学时应围绕课标要点“{cp_text[:160]}”展开，先明确概念边界，再通过例子、图示、实验、语篇或案例帮助学生建立可迁移的理解。\n\n"
        "### 学习路径\n"
        f"1. 情境导入：{methods[0]}\n"
        f"2. 探究建构：{methods[1]}\n"
        f"3. 应用迁移：{methods[2]}\n\n"
        "### 例题设计方向\n可设计一道“识别核心概念”的基础题，一道“解释现象或文本材料”的理解题，一道“迁移到真实情境”的应用题，并要求学生说明依据。\n"
    )


def generated_md(data: dict[str, Any], subject: str, name: str, cps: list[str]) -> str:
    stage = data.get("stage") or ""
    grade = data.get("grade") or ""
    domain = data.get("domain_name") or ""
    cp_lines = "\n".join(f"> {cp}" for cp in cps[:5]) or "> 暂无明确课标点，需后续补充原始课标依据。"
    methods = teaching_methods(subject, name, cps)
    ext = extensions(subject, name)
    return (
        f"# {name}\n\n"
        "## 基本信息\n"
        f"- **学科**: {SUBJECT_ZH.get(subject, subject)}\n"
        f"- **学段**: {stage}\n"
        f"- **年级**: {grade}\n"
        f"- **章节/领域**: {domain}\n"
        "- **内容来源**: TeachAny 课标知识点卫星文件\n\n"
        "## 一、课标原文\n\n"
        "### 1.1 内容要求\n"
        f"{cp_lines}\n\n"
        "## 二、教学目标\n\n"
        f"- 理解「{name}」的核心概念、方法与应用场景。\n"
        f"- 能结合材料、问题或真实情境解释「{name}」相关现象。\n"
        "- 能用规范的学科语言表达思路、依据和结论。\n\n"
        "## 三、教学重难点\n\n"
        f"- 教学重点：建立对「{name}」核心概念和基本方法的准确理解。\n"
        "- 教学难点：把知识迁移到新的问题、材料或真实情境中。\n\n"
        "## 五、教学建议\n\n"
        "### 5.1 教学方法\n"
        + "\n".join(f"- {m}" for m in methods)
        + "\n\n### 5.2 学习活动设计\n"
        + "\n".join(f"{i}. {m}" for i, m in enumerate(methods, 1))
        + "\n\n## 七、课件制作参考\n\n"
        + "\n".join(f"- {m}" for m in methods)
        + "\n\n## 八、相关知识扩展\n\n"
        + "\n".join(f"- {e}" for e in ext)
        + "\n"
    )


def exercise_templates(subject: str, name: str, cps: list[str]) -> list[dict[str, Any]]:
    cp1 = cps[0] if cps else f"理解{name}的核心内容。"
    cp2 = cps[1] if len(cps) > 1 else cp1
    if subject == "math":
        return [
            {"id": "q-1", "stem": f"根据课标要点，说明「{name}」中最关键的数量关系或图形关系是什么。", "answer": f"应围绕：{cp1[:180]}，说明概念、条件和表示方法。", "type": "short_answer", "source": SOURCE_TAG},
            {"id": "q-2", "stem": f"设计一个生活情境，用「{name}」建立模型并解释结果。", "answer": "需写出已知量、未知量、关系式或图形表示，并解释结论含义。", "type": "application", "source": SOURCE_TAG},
        ]
    if subject == "physics":
        return [
            {"id": "q-1", "stem": f"围绕「{name}」，写出一个可观察现象，并说明其中涉及的物理量或规律。", "answer": f"应扣住课标要点：{cp1[:180]}，说明现象、条件和规律。", "type": "short_answer", "source": SOURCE_TAG},
            {"id": "q-2", "stem": f"如果要验证「{name}」相关规律，你会控制哪些变量？记录哪些数据？", "answer": "需说明实验目的、控制变量、测量数据、可能误差和结论依据。", "type": "experiment_design", "source": SOURCE_TAG},
        ]
    if subject == "chemistry":
        return [
            {"id": "q-1", "stem": f"描述一个与「{name}」相关的实验现象，并用化学概念解释原因。", "answer": f"应扣住课标要点：{cp1[:180]}，从现象、微观本质和符号表达三个层面回答。", "type": "short_answer", "source": SOURCE_TAG},
            {"id": "q-2", "stem": f"判断一个生活或实验场景是否体现「{name}」，并说明证据。", "answer": "需写出观察证据、相关概念、判断依据和安全注意事项。", "type": "application", "source": SOURCE_TAG},
        ]
    if subject == "biology":
        return [
            {"id": "q-1", "stem": f"用结构与功能或过程与结果的关系解释「{name}」。", "answer": f"应扣住课标要点：{cp1[:180]}，说明生命现象、结构/过程和功能意义。", "type": "short_answer", "source": SOURCE_TAG},
            {"id": "q-2", "stem": f"举一个生活、健康或生态案例，说明「{name}」的应用价值。", "answer": "需写出案例、涉及的生物学原理以及对生活或环境的意义。", "type": "application", "source": SOURCE_TAG},
        ]
    if subject == "history":
        return [
            {"id": "q-1", "stem": f"说明「{name}」的时间背景、关键变化和历史影响。", "answer": f"应扣住课标要点：{cp1[:180]}，用时间线和证据说明。", "type": "short_answer", "source": SOURCE_TAG},
            {"id": "q-2", "stem": f"选择一则材料或史实，解释它如何帮助理解「{name}」。", "answer": "需区分史实、观点和解释，说明证据与结论的关系。", "type": "evidence_analysis", "source": SOURCE_TAG},
        ]
    if subject == "geography":
        return [
            {"id": "q-1", "stem": f"结合地图或资料，说明「{name}」涉及的位置、分布或联系。", "answer": f"应扣住课标要点：{cp1[:180]}，从位置、分布、差异或人地关系角度回答。", "type": "map_analysis", "source": SOURCE_TAG},
            {"id": "q-2", "stem": f"用一个现实区域案例说明「{name}」的地理意义。", "answer": "需写出区域位置、关键地理要素、相互关系和结论。", "type": "case_analysis", "source": SOURCE_TAG},
        ]
    if subject == "chinese":
        return [
            {"id": "q-1", "stem": f"阅读一段相关文本，说明它如何体现「{name}」的学习要求。", "answer": f"应扣住课标要点：{cp1[:180]}，从内容理解、语言特点和表达效果回答。", "type": "reading_response", "source": SOURCE_TAG},
            {"id": "q-2", "stem": f"围绕「{name}」完成一个仿写、赏析或表达任务。", "answer": "需说明表达对象、语言依据、情感或观点，并做到语句通顺。", "type": "writing_task", "source": SOURCE_TAG},
        ]
    if subject == "english":
        return [
            {"id": "q-1", "stem": f"Create two sentences in a real context to show how to use {name}. Explain the meaning in Chinese.", "answer": f"Sentences should fit the context and reflect: {cp1[:160]}", "type": "language_use", "source": SOURCE_TAG},
            {"id": "q-2", "stem": f"Read a short dialogue and identify how {name} helps express meaning.", "answer": "The answer should explain form, meaning and use in context.", "type": "context_analysis", "source": SOURCE_TAG},
        ]
    return [
        {"id": "q-1", "stem": f"结合课标要点，说明「{name}」的核心含义和学习价值。", "answer": f"应扣住：{cp1[:180]}，说明概念、证据和应用。", "type": "short_answer", "source": SOURCE_TAG},
        {"id": "q-2", "stem": f"举一个真实情境，说明如何应用「{name}」。", "answer": f"需结合情境，并体现：{cp2[:160]}", "type": "application", "source": SOURCE_TAG},
    ]


def error_templates(subject: str, name: str) -> list[dict[str, Any]]:
    if subject == "math":
        return [
            {"id": "err-1", "description": f"只记「{name}」的公式或结论，不理解适用条件和变量含义。", "type": "conceptual", "source": SOURCE_TAG},
            {"id": "err-2", "description": "解题时跳步，未把已知条件、关系式和结论之间的推理写完整。", "type": "procedural", "source": SOURCE_TAG},
        ]
    if subject == "physics":
        return [
            {"id": "err-1", "description": f"只套用「{name}」相关公式，忽略物理情境、单位和适用条件。", "type": "conceptual", "source": SOURCE_TAG},
            {"id": "err-2", "description": "实验分析时没有控制变量，导致无法判断因果关系。", "type": "evidence", "source": SOURCE_TAG},
        ]
    if subject == "chemistry":
        return [
            {"id": "err-1", "description": f"只描述「{name}」的表面现象，不能从微观粒子或化学用语解释本质。", "type": "conceptual", "source": SOURCE_TAG},
            {"id": "err-2", "description": "忽略实验条件、试剂用量或安全规范，导致判断不准确。", "type": "procedural", "source": SOURCE_TAG},
        ]
    if subject == "biology":
        return [
            {"id": "err-1", "description": f"把「{name}」当作孤立事实记忆，不能说明结构、功能和生命过程之间的关系。", "type": "conceptual", "source": SOURCE_TAG},
            {"id": "err-2", "description": "解释生命现象时缺少证据，容易把相关关系误认为因果关系。", "type": "evidence", "source": SOURCE_TAG},
        ]
    if subject == "history":
        return [
            {"id": "err-1", "description": f"只记「{name}」的事件名称或年代，不能说明背景、过程和影响。", "type": "conceptual", "source": SOURCE_TAG},
            {"id": "err-2", "description": "引用材料时未区分史实、观点和解释，导致论证依据不足。", "type": "evidence", "source": SOURCE_TAG},
        ]
    if subject == "geography":
        return [
            {"id": "err-1", "description": f"分析「{name}」时只背名称，忽略位置、分布、联系和区域差异。", "type": "conceptual", "source": SOURCE_TAG},
            {"id": "err-2", "description": "读图时忽略比例尺、方向、图例或数据单位，导致空间判断错误。", "type": "map_reading", "source": SOURCE_TAG},
        ]
    if subject == "chinese":
        return [
            {"id": "err-1", "description": f"学习「{name}」时脱离文本，只背答题模板，不能结合语言材料分析。", "type": "reading", "source": SOURCE_TAG},
            {"id": "err-2", "description": "表达时观点、依据和语言效果脱节，缺少具体文本证据。", "type": "expression", "source": SOURCE_TAG},
        ]
    if subject == "english":
        return [
            {"id": "err-1", "description": f"学习「{name}」时只记形式，不能在真实语境中表达意义。", "type": "usage", "source": SOURCE_TAG},
            {"id": "err-2", "description": "受中文表达影响，忽略英语词序、搭配或语法一致性。", "type": "interlanguage", "source": SOURCE_TAG},
        ]
    if subject == "info-tech":
        return [
            {"id": "err-1", "description": f"只会操作「{name}」相关步骤，不能解释背后的流程、规则或算法。", "type": "conceptual", "source": SOURCE_TAG},
            {"id": "err-2", "description": "忽视数据安全、版权或网络伦理，导致方案不规范。", "type": "digital_ethics", "source": SOURCE_TAG},
        ]
    return [
        {"id": "err-1", "description": f"只记「{name}」的结论，不能解释依据和应用条件。", "type": "conceptual", "source": SOURCE_TAG},
        {"id": "err-2", "description": "回答问题时缺少证据、过程或真实情境。", "type": "evidence", "source": SOURCE_TAG},
    ]


def sanitize_reference_text(text: str) -> str:
    text = PLACEHOLDER_RE.sub("", text or "")
    text = text.replace("暂无对应教材资料", "")
    text = text.replace("待补充与知识点对应的 OpenStax 或国内教材资料", "")
    return text.strip()


def clean_derived_fields(data: dict[str, Any], subject: str, stats: Counter[str]) -> bool:
    changed = False
    if subject != "history":
        for field in ("errors", "exercises"):
            old = data.get(field) or []
            if isinstance(old, list) and old:
                new = [item for item in old if not HISTORY_TEMPLATE_RE.search(item_text(item))]
                if len(new) != len(old):
                    data[field] = new
                    stats[f"removed_history_template_{field}"] += len(old) - len(new)
                    changed = True

    tc = data.get("textbook_content")
    if isinstance(tc, dict):
        old_snippets = tc.get("snippets") or []
        if isinstance(old_snippets, list) and old_snippets:
            new_snippets = [s for s in old_snippets if isinstance(s, str) and not bad_textbook_text(s)]
            if len(new_snippets) != len(old_snippets):
                stats["removed_bad_textbook_snippets"] += len(old_snippets) - len(new_snippets)
                changed = True
                if new_snippets:
                    tc["snippets"] = new_snippets[:3]
                else:
                    tc.pop("snippets", None)
            if not tc.get("snippets") and set(tc.keys()).issubset({"stage7_injected"}):
                data.pop("textbook_content", None)
            else:
                data["textbook_content"] = tc

    sup = data.setdefault("supplements", {})
    refs = list(sup.get("resource_references") or [])
    if refs:
        sanitized_refs: list[dict[str, Any]] = []
        for ref in refs:
            if isinstance(ref, dict):
                new_ref = dict(ref)
                if "text" in new_ref:
                    new_ref["text"] = sanitize_reference_text(str(new_ref.get("text") or ""))[:500]
                sanitized_refs.append(new_ref)
            else:
                sanitized_refs.append({"text": sanitize_reference_text(str(ref))[:500], "source_field": "resource_references"})
        if sanitized_refs != refs:
            refs = sanitized_refs
            changed = True
            stats["cleaned_resource_references"] += 1
    for key in ("openstax_or_curriculum",):
        old = sup.get(key) or []
        if isinstance(old, list) and old:
            good: list[str] = []
            for item in old:
                text = clean_text(item)
                if bad_textbook_text(text):
                    refs.append({"source_field": key, "text": sanitize_reference_text(text)[:500], "moved_at": utc_now(), "reason": "not_usable_as_textbook_content"})
                    stats[f"moved_bad_{key}"] += 1
                    changed = True
                else:
                    good.append(text)
            if good:
                sup[key] = good[:3]
            else:
                sup.pop(key, None)
    summary = sup.get("textbook_summary")
    if isinstance(summary, str) and bad_textbook_text(summary):
        refs.append({"source_field": "textbook_summary", "text": sanitize_reference_text(summary)[:500], "moved_at": utc_now(), "reason": "reference_only_or_generic"})
        sup.pop("textbook_summary", None)
        stats["moved_bad_textbook_summary"] += 1
        changed = True
    if refs:
        sup["resource_references"] = refs[-10:]

    deep = sup.get("deep_textbook_snippets") or []
    if isinstance(deep, list) and deep:
        cleaned_deep: list[dict[str, Any]] = []
        for item in deep:
            if not isinstance(item, dict):
                continue
            text = str(item.get("text") or "")
            if bad_textbook_text(text):
                stats["removed_bad_deep_textbook_snippets"] += 1
                changed = True
                continue
            cleaned_deep.append(item)
        if len(cleaned_deep) != len(deep):
            if cleaned_deep:
                sup["deep_textbook_snippets"] = cleaned_deep[:4]
            else:
                sup.pop("deep_textbook_snippets", None)
                sup.pop("deep_textbook_source", None)
                sup.pop("deep_textbook_enriched_at", None)
                sup.pop("deep_worked_example", None)
            changed = True
    tc2 = data.get("textbook_content") or {}
    deep_tc = tc2.get("deep_snippets") or []
    if isinstance(deep_tc, list) and deep_tc:
        cleaned_tc = [item for item in deep_tc if isinstance(item, dict) and not bad_textbook_text(str(item.get("text") or ""))]
        if len(cleaned_tc) != len(deep_tc):
            if cleaned_tc:
                tc2["deep_snippets"] = cleaned_tc[:3]
                data["textbook_content"] = tc2
            else:
                tc2.pop("deep_snippets", None)
                tc2.pop("deep_source", None)
                if tc2:
                    data["textbook_content"] = tc2
                else:
                    data.pop("textbook_content", None)
            stats["removed_bad_textbook_deep_snippets"] += len(deep_tc) - len(cleaned_tc)
            changed = True

    raw = sup.get("curriculum_md_raw") or ""
    if raw:
        raw2, c1 = strip_placeholder_lines(raw)
        raw3, c2 = fix_math_template(raw2, subject)
        if c1 or c2:
            sup["curriculum_md_raw"] = raw3
            stats["cleaned_curriculum_md_raw"] += 1
            changed = True
    return changed


def enrich_node(data: dict[str, Any], subject: str, stats: Counter[str]) -> bool:
    changed = False
    name = data.get("name") or data.get("kp_id") or "本知识点"
    cps = curriculum_points(data)
    sup = data.setdefault("supplements", {})

    raw = sup.get("curriculum_md_raw") or ""
    if not raw:
        sup["curriculum_md_raw"] = generated_md(data, subject, name, cps)
        sup["curriculum_md_source"] = sup.get("curriculum_md_source") or "generated_from_kp_satellite"
        stats["generated_curriculum_md_raw"] += 1
        changed = True
        raw = sup["curriculum_md_raw"]
    else:
        additions: list[str] = []
        if not section_exists(raw, ("教学方法", "学习活动设计", "教学建议", "教学提示")):
            methods = teaching_methods(subject, name, cps)
            additions.append("\n## 五、教学建议（学科化补灌）\n\n### 5.1 教学方法\n" + "\n".join(f"- {m}" for m in methods) + "\n")
            stats["added_teaching_methods"] += 1
        if not section_exists(raw, ("拓展资源", "拓展延伸", "相关知识", "参考资料")):
            ext = extensions(subject, name)
            additions.append("\n## 八、相关知识扩展（学科化补灌）\n" + "\n".join(f"- {e}" for e in ext) + "\n")
            stats["added_extensions"] += 1
        if additions:
            sup["curriculum_md_raw"] = raw.rstrip() + "\n" + "\n".join(additions)
            changed = True

    if not data.get("exercises"):
        data["exercises"] = exercise_templates(subject, name, cps)
        stats["generated_exercises"] += 1
        changed = True
    if not data.get("errors"):
        data["errors"] = error_templates(subject, name)
        stats["generated_errors"] += 1
        changed = True
    if not data.get("real_world"):
        data["real_world"] = real_world_examples(subject, name)
        stats["generated_real_world"] += 1
        changed = True

    # 仅在没有可用教材化内容时补一段透明标注的“课标生成讲解参考”。
    summary = sup.get("textbook_summary") or ""
    oxc = sup.get("openstax_or_curriculum") or []
    tc = data.get("textbook_content") or {}
    current_text = "\n".join([clean_text(summary), clean_text(oxc), clean_text(tc)])
    if (
        not current_text.strip()
        or len(current_text.strip()) < 120
        or bad_textbook_text(current_text)
        or not TEXTBOOK_CONTENT_MARKER_RE.search(current_text[:3000])
    ):
        sup["textbook_summary"] = generated_content_summary(subject, name, cps)
        sup["textbook_summary_source"] = "generated_from_curriculum_points"
        stats["generated_textbook_summary"] += 1
        changed = True

    if changed:
        meta = data.setdefault("_meta", {})
        meta["clean_enrich_at"] = utc_now()
        sources = meta.setdefault("sources", [])
        if isinstance(sources, list) and SOURCE_TAG not in sources:
            sources.append(SOURCE_TAG)
    return changed


def is_cn(data: dict[str, Any], node: dict[str, Any]) -> bool:
    return (data.get("curriculum") or node.get("curriculum")) == "cn"


def backup_file(path: Path, backup_root: Path) -> None:
    rel = path.relative_to(ROOT)
    target = backup_root / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def process(args: argparse.Namespace) -> dict[str, Any]:
    kp_index = load_json(KP_INDEX_PATH).get("kps", {})
    node_index = load_json(NODE_INDEX_PATH).get("nodes", {}) if NODE_INDEX_PATH.exists() else {}
    subjects = set(args.subject or [])
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = Path(args.backup_dir) if args.backup_dir else KP_ROOT / "_backups" / f"clean-enrich-cn-{run_id}"

    stats: Counter[str] = Counter()
    by_subject: dict[str, Counter[str]] = defaultdict(Counter)
    changed_files: list[str] = []

    for kp_id, rel in sorted(kp_index.items()):
        path = ROOT / rel
        if not path.is_file():
            continue
        data = load_json(path)
        node = node_index.get(kp_id, {})
        if not is_cn(data, node):
            continue
        subject = data.get("subject") or node.get("subject") or "other"
        if subjects and subject not in subjects:
            continue
        before = json.dumps(data, ensure_ascii=False, sort_keys=True)
        clean_derived_fields(data, subject, stats)
        enrich_node(data, subject, stats)
        after = json.dumps(data, ensure_ascii=False, sort_keys=True)
        by_subject[subject]["seen"] += 1
        if before != after:
            by_subject[subject]["changed"] += 1
            changed_files.append(str(path.relative_to(ROOT)))
            if not args.dry_run:
                backup_file(path, backup_root)
                dump_json(path, data)
                stats["written_files"] += 1
            else:
                stats["would_write_files"] += 1

    report = {
        "run_at": utc_now(),
        "dry_run": args.dry_run,
        "backup_dir": str(backup_root.relative_to(ROOT)) if backup_root.is_relative_to(ROOT) else str(backup_root),
        "stats": dict(stats),
        "by_subject": {k: dict(v) for k, v in sorted(by_subject.items())},
        "changed_files_count": len(changed_files),
        "changed_files_sample": changed_files[:80],
    }
    if not args.dry_run:
        report_path = backup_root / "clean-enrich-report.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean dirty CN KP data and enrich subject baseline content")
    parser.add_argument("--subject", action="append", help="limit to subject, can repeat, e.g. --subject math")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--backup-dir", default="")
    args = parser.parse_args()
    report = process(args)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
