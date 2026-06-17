#!/usr/bin/env python3
"""从课标摘录 + 人教版教材目录生成中小学道法/心理知识树（小学+初中+高中）。"""
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "data" / "curriculum-sources" / "cn"
CN = ROOT / "data" / "trees" / "cn"
UNIFIED = ROOT / "data" / "trees" / "cn-unified"

SEMESTER_KEY = {"上": "up", "下": "lo"}

# ── 小学道法课标要点（按年级） ─────────────────────────────────────────
POL_ELEM_BAND = {
    1: [
        "帮助学生适应小学生活，养成良好学习习惯和生活习惯，乐于与老师、同学交往。",
        "懂礼貌、讲诚信，知道感恩，尊重父母师长，爱护集体。",
        "养成良好的卫生、饮食习惯，有安全意识和自我保护意识，遵守交通规则。",
        "知道生活中处处有规则，初步树立规则意识，了解国旗、国歌等国家象征的意义。",
    ],
    2: [
        "礼貌与诚信，克己守礼，自尊自爱，自强自律；感受传统节日与家乡文化。",
        "诚实守信，友善待人，有集体意识和责任感。",
        "掌握基本安全知识和技能，珍爱生命。",
        "了解基本法律常识，树立规则意识和权利意识。",
    ],
    3: [
        "诚实守信，友善待人，尊重他人，有集体意识和责任感。",
        "掌握基本安全知识和技能，学会应对常见安全问题。",
        "感受中华优秀传统文化魅力，增强文化自信。",
        "遵守公共秩序，爱护公共设施，参与力所能及的公益活动。",
    ],
    4: [
        "诚实守信，友善待人，尊重他人，有集体意识和责任感。",
        "掌握基本安全知识和技能，学会应对常见安全问题。",
        "感受中华优秀传统文化魅力，增强文化自信。",
        "遵守公共秩序，爱护公共设施，参与力所能及的公益活动。",
    ],
    5: [
        "自律自强，孝敬长辈，友善待人，有正确的价值取向。",
        "增强自我保护意识，拒绝不良诱惑，珍爱生命。",
        "了解宪法是国家的根本法，知道公民的基本权利和义务，树立法治观念。",
        "了解基本国情，热爱祖国，增强民族自豪感，树立国家认同。",
    ],
    6: [
        "自律自强，孝敬长辈，友善待人，有正确的价值取向。",
        "增强自我保护意识，拒绝不良诱惑，珍爱生命。",
        "了解宪法是国家的根本法，知道公民的基本权利和义务，树立法治观念。",
        "传承中华传统美德，了解革命传统，增强文化自信。",
    ],
}

POL_MID_BAND = {
    7: [
        "正确认识自我，接纳青春期变化，形成积极稳定的情绪情感，养成自尊自信人格。",
        "珍爱生命，具有安全意识、规则意识和法治观念，能够自我保护、自我调控。",
        "具有亲社会态度和行为，懂得维护集体荣誉，构建和谐人际关系。",
        "树立正确人生观、价值观，明确人生目标，努力成为担当民族复兴大任的时代新人。",
    ],
    8: [
        "理解家庭和睦的重要性，学会与同学、老师、父母沟通，构建和谐人际关系。",
        "遵守社会规则，维护公共秩序，热心公益事业，践行社会主义核心价值观。",
        "了解我国基本政治制度、基本经济制度，理解法治是治国理政的基本方式。",
        "具有公共意识、社会责任意识，维护国家利益和国家安全。",
    ],
    9: [
        "了解中国特色社会主义伟大事业的辉煌成就，增强民族自尊心、自信心和自豪感。",
        "理解民主与法治，参与民主生活，树立宪法法律至上观念。",
        "传承中华优秀传统文化，建设美丽中国，坚定文化自信。",
        "了解世界发展趋势，树立人类命运共同体意识，做有国际视野的中国人。",
    ],
}

POL_HIGH_BOOK_CP = {
    "req1": [
        "理解社会主义从空想到科学、从理论到实践的发展，坚定中国特色社会主义信念。",
        "理解只有社会主义才能救中国，只有中国特色社会主义才能发展中国。",
        "理解新时代坚持和发展中国特色社会主义的总任务，学习贯彻习近平新时代中国特色社会主义思想。",
    ],
    "req2": [
        "理解我国生产资料所有制与社会主义市场经济体制，把握“两个毫不动摇”。",
        "贯彻新发展理念，建设现代化经济体系，推动高质量发展。",
        "理解个人收入分配与社会保障制度，践行社会责任促进社会进步。",
    ],
    "req3": [
        "理解中国共产党领导是中国特色社会主义最本质的特征。",
        "理解人民当家作主是社会主义民主政治的本质和核心。",
        "理解全面依法治国是国家治理的一场深刻革命，建设法治中国。",
    ],
    "req4": [
        "掌握马克思主义哲学基本原理，坚持唯物辩证法，反对形而上学。",
        "理解社会历史发展规律，坚持历史唯物主义，实现人生价值。",
        "传承发展中华优秀传统文化，坚定文化自信，发展中国特色社会主义文化。",
    ],
    "opt1": [
        "了解国体政体与国家结构形式，理解世界多极化趋势。",
        "理解经济全球化与中国对外开放，了解主要国际组织与中国参与全球治理。",
    ],
    "opt2": [
        "理解民事权利与义务，积极维护人身权利与各类物权。",
        "了解婚姻家庭、就业创业相关法律，学会运用法律解决社会争议。",
    ],
    "opt3": [
        "树立科学思维观念，把握逻辑要义，领会科学思维。",
        "遵循逻辑思维规则，运用辩证思维方法，提高创新思维能力。",
    ],
}

POL_DOMAIN_COLORS = {
    "moral-cultivation": "#f97316",
    "health-safety": "#22c55e",
    "rule-of-law": "#6366f1",
    "tradition-culture": "#a855f7",
    "public-life": "#14b8a6",
    "national-situation": "#ef4444",
    "self-growth": "#f59e0b",
    "interpersonal": "#ec4899",
    "civic-duty": "#0ea5e9",
    "socialism": "#dc2626",
    "economy": "#059669",
    "politics-law": "#2563eb",
    "philosophy-culture": "#7c3aed",
    "intl-relations": "#0891b2",
    "law-life": "#64748b",
    "logic-thinking": "#8b5cf6",
}

POL_ELEM_THEME = {1: "moral-cultivation", 2: "tradition-culture", 3: "health-safety", 4: "rule-of-law"}
POL_MID_THEME = {1: "self-growth", 2: "interpersonal", 3: "health-safety", 4: "civic-duty"}

PSYCH_DOMAIN_META = {
    "life-adaptation": ("生活适应", "#0ea5e9"),
    "learning-support": ("学习辅导", "#3b82f6"),
    "self-awareness": ("认识自我", "#8b5cf6"),
    "interpersonal": ("人际交往", "#ec4899"),
    "emotion-regulation": ("情绪调适", "#f59e0b"),
    "puberty-growth": ("青春期与成长", "#10b981"),
    "career-planning": ("生涯规划", "#14b8a6"),
    "resilience": ("抗挫与适应", "#f97316"),
}

PSYCH_ELEM = [
    ("psych-e-g1-school-adapt", "入学适应与规则意识", "School adaptation & rules", 1, "life-adaptation", [],
     ["帮助学生认识班级、学校、日常学习生活环境和基本规则。",
      "帮助学生适应新环境、新集体和新的学习生活，树立纪律意识、时间意识和规则意识。",
      "使学生有安全感和归属感，初步学会自我控制。"]),
    ("psych-e-g1-learning-habit", "学习习惯与友好交往", "Study habits & friendship", 1, "learning-support",
     ["psych-e-g1-school-adapt"],
     ["初步感受学习知识的乐趣，重点是学习习惯的培养与训练。",
      "培养学生礼貌友好的交往品质，乐于与老师、同学交往，在谦让、友善的交往中感受友情。"]),
    ("psych-e-g2-self-confidence", "自信与集体归属感", "Confidence & belonging", 2, "interpersonal",
     ["psych-e-g1-learning-habit"],
     ["培养学生礼貌友好的交往品质，乐于与老师、同学交往，在谦让、友善的交往中感受友情。",
      "使学生有安全感和归属感，初步学会自我控制。", "树立集体意识，培养自主参与各种活动的能力。"]),
    ("psych-e-g2-emotion-basics", "情绪体验与自我控制", "Emotion awareness & control", 2, "emotion-regulation",
     ["psych-e-g2-self-confidence"],
     ["初步学会体验情绪并表达自己的情绪。", "使学生有安全感和归属感，初步学会自我控制。"]),
    ("psych-e-g3-self-know", "认识自我与学习兴趣", "Self-awareness & interest", 3, "self-awareness",
     ["psych-e-g2-emotion-basics"],
     ["帮助学生了解自我，认识自我。", "初步培养学生的学习能力，激发学习兴趣和探究精神，树立自信，乐于学习。"]),
    ("psych-e-g3-social-role", "角色意识与时间管理", "Role awareness & time management", 3, "life-adaptation",
     ["psych-e-g3-self-know"],
     ["帮助学生建立正确的角色意识，培养学生对不同社会角色的适应。",
      "增强时间管理意识，帮助学生正确处理学习与兴趣、娱乐之间的矛盾。"]),
    ("psych-e-g4-peer-relation", "同伴交往与解决困难", "Peer relations & problem solving", 4, "interpersonal",
     ["psych-e-g3-social-role"],
     ["树立集体意识，善于与同学、老师交往，培养开朗、合群、自立的健康人格。",
      "引导学生在学习生活中感受解决困难的快乐，学会体验情绪并表达自己的情绪。"]),
    ("psych-e-g4-study-motivation", "学习自信与情绪表达", "Study confidence & expression", 4, "learning-support",
     ["psych-e-g4-peer-relation"],
     ["初步培养学生的学习能力，激发学习兴趣和探究精神，树立自信，乐于学习。",
      "学会体验情绪并表达自己的情绪。"]),
    ("psych-e-g5-self-accept", "悦纳自我与学习动机", "Self-acceptance & motivation", 5, "self-awareness",
     ["psych-e-g4-study-motivation"],
     ["帮助学生正确认识自己的优缺点和兴趣爱好，在各种活动中悦纳自己。",
      "着力培养学生的学习兴趣和学习能力，端正学习动机，调整学习心态，正确对待成绩，体验学习成功的乐趣。"]),
    ("psych-e-g5-negative-emotion", "面对挫折与情绪调节", "Coping & emotion regulation", 5, "emotion-regulation",
     ["psych-e-g5-self-accept"],
     ["帮助学生克服学习困难，正确面对厌学等负面情绪，学会恰当地、正确地体验情绪和表达情绪。",
      "开展初步的青春期教育，引导学生进行恰当的异性交往，建立和维持良好的异性同伴关系。"]),
    ("psych-e-g6-puberty", "青春期教育与异性交往", "Puberty & peer relations", 6, "puberty-growth",
     ["psych-e-g5-negative-emotion"],
     ["开展初步的青春期教育，引导学生进行恰当的异性交往，建立和维持良好的异性同伴关系，扩大人际交往的范围。",
      "帮助学生正确认识自己的优缺点和兴趣爱好，在各种活动中悦纳自己。"]),
    ("psych-e-g6-social-citizen", "亲社会行为与问题解决", "Prosocial behavior & citizenship", 6, "life-adaptation",
     ["psych-e-g6-puberty"],
     ["积极促进学生的亲社会行为，逐步认识自己与社会、国家和世界的关系。",
      "培养学生分析问题和解决问题的能力，为初中阶段学习生活做好准备。"]),
]

PSYCH_MID = [
    ("psych-m-g7-self-identity", "自我认识与青春期适应", "Self-identity & puberty", 7, "self-awareness", [],
     ["加强自我认识，客观评价自己，认识青春期的生理特征和心理特征。",
      "适应中学阶段的学习环境和学习要求，培养正确的学习观念。"]),
    ("psych-m-g7-study-adapt", "学习适应与情绪管理", "Study adaptation & emotions", 7, "learning-support",
     ["psych-m-g7-self-identity"],
     ["发展学习能力，改善学习方法，提高学习效率。",
      "进行积极的情绪体验与表达，并对自己的情绪进行有效管理，正确处理厌学心理。"]),
    ("psych-m-g7-interpersonal", "亲子师生与同伴交往", "Family, teacher & peer relations", 7, "interpersonal",
     ["psych-m-g7-study-adapt"],
     ["积极与老师及父母进行沟通，把握与异性交往的尺度，建立良好的人际关系。"]),
    ("psych-m-g8-role-identity", "角色认同与社会适应", "Role identity & social adaptation", 8, "life-adaptation",
     ["psych-m-g7-interpersonal"],
     ["帮助学生建立正确的角色意识，培养学生对不同社会角色的适应。",
      "逐步适应生活和社会的各种变化，着重培养应对失败和挫折的能力。"]),
    ("psych-m-g8-puberty-relation", "青春期交往与情绪调适", "Puberty relations & emotions", 8, "puberty-growth",
     ["psych-m-g8-role-identity"],
     ["认识青春期生理和心理特征，把握与异性交往的尺度。",
      "抑制冲动行为，学会恰当地体验情绪和表达情绪。"]),
    ("psych-m-g8-stress-coping", "学业压力与挫折应对", "Academic stress & resilience", 8, "resilience",
     ["psych-m-g8-puberty-relation"],
     ["正确处理厌学心理，克服学习困难。",
      "着重培养应对失败和挫折的能力，形成良好意志品质。"]),
    ("psych-m-g9-career-explore", "升学择业与生涯探索", "Career exploration", 9, "career-planning",
     ["psych-m-g8-stress-coping"],
     ["把握升学选择的方向，培养职业规划意识，树立早期职业发展目标。",
      "在充分了解兴趣、能力、性格、特长和社会需要的基础上进行升学准备。"]),
    ("psych-m-g9-social-adapt", "社会适应与责任意识", "Social adaptation & responsibility", 9, "life-adaptation",
     ["psych-m-g9-career-explore"],
     ["逐步适应生活和社会各种变化，培养担当意识和社会责任感。",
      "积极促进亲社会行为，认识自己与社会、国家和世界的关系。"]),
    ("psych-m-g9-mental-health", "心理健康素养与求助", "Mental health literacy", 9, "resilience",
     ["psych-m-g9-social-adapt"],
     ["了解心理健康基本知识，树立求助意识，掌握基本心理调适方法。",
      "为高中阶段学习生活做好心理适应准备。"]),
]

PSYCH_HIGH = [
    ("psych-h-g10-self-concept", "自我认同与理想信念", "Self-concept & ideals", 10, "self-awareness", [],
     ["帮助学生确立正确的自我意识，树立人生理想和信念，形成正确的世界观、人生观和价值观。"]),
    ("psych-h-g10-learning-strategy", "学习策略与考试适应", "Learning strategies & exams", 10, "learning-support",
     ["psych-h-g10-self-concept"],
     ["培养创新精神和创新能力，掌握学习策略，开发学习潜能，提高学习效率。",
      "积极应对考试压力，克服考试焦虑。"]),
    ("psych-h-g10-relationship", "人际关系与沟通", "Relationships & communication", 10, "interpersonal",
     ["psych-h-g10-learning-strategy"],
     ["正确认识人际关系状况，培养人际沟通能力，促进积极情感反应和体验。",
      "正确对待和异性同伴的交往，知道友谊和爱情的界限。"]),
    ("psych-h-g11-emotion-resilience", "情绪管理与抗挫力", "Emotion management & resilience", 11, "emotion-regulation",
     ["psych-h-g10-relationship"],
     ["进一步提高承受失败和应对挫折的能力，形成良好的意志品质。",
      "学会恰当地、正确地体验情绪和表达情绪。"]),
    ("psych-h-g11-exam-wellness", "考试心理与身心健康", "Exam wellness", 11, "resilience",
     ["psych-h-g11-emotion-resilience"],
     ["积极应对考试压力，克服考试焦虑，保持身心健康。",
      "掌握科学减压与情绪调适方法。"]),
    ("psych-h-g11-peer-support", "同伴支持与合作学习", "Peer support & collaboration", 11, "interpersonal",
     ["psych-h-g11-exam-wellness"],
     ["培养人际沟通能力，在合作学习中建立支持性同伴关系。",
      "促进积极情感反应和体验。"]),
    ("psych-h-g12-career-choice", "生涯规划与升学择业", "Career planning & choices", 12, "career-planning",
     ["psych-h-g11-peer-support"],
     ["充分了解兴趣、能力、性格、特长和社会需要，确立职业志向，培养职业道德意识。",
      "进行升学就业的选择和准备，培养担当意识和社会责任感。"]),
    ("psych-h-g12-life-transition", "人生过渡与社会适应", "Life transition & adaptation", 12, "life-adaptation",
     ["psych-h-g12-career-choice"],
     ["逐步适应生活和社会的各种变化，为走向社会做好心理准备。",
      "树立远大理想，培养社会责任意识。"]),
    ("psych-h-g12-mental-literacy", "心理素养与终身发展", "Mental health literacy", 12, "resilience",
     ["psych-h-g12-life-transition"],
     ["形成积极心理品质，掌握心理保健常识和技能。",
      "具备自主自助维护心理健康的能力，促进终身发展。"]),
]


def load_json(name: str) -> dict:
    return json.loads((SOURCES / name).read_text(encoding="utf-8"))


def make_node(
    *,
    nid: str,
    name: str,
    name_en: str,
    grade: int,
    domain: str,
    prerequisites: list[str],
    curriculum_points: list[str],
    stage: str,
    extra: dict | None = None,
) -> dict:
    node = {
        "id": nid,
        "name": name,
        "name_en": name_en,
        "grade": grade,
        "domain": domain,
        "difficulty": min(4, 1 + max(0, grade - 1) // 3),
        "status": "active",
        "prerequisites": prerequisites,
        "extends": [],
        "parallel": [],
        "courses": [nid],
        "curriculum_points": curriculum_points,
        "stage": stage,
    }
    if extra:
        node.update(extra)
    return node


def politics_elem_nodes(tb: dict) -> list[dict]:
    nodes: list[dict] = []
    for g_str, meta in tb["grades"].items():
        grade = int(g_str)
        band = POL_ELEM_BAND[grade]
        for i, unit in enumerate(meta["units"], 1):
            dom = POL_ELEM_THEME.get(i, "public-life")
            if grade >= 5 and i >= 3:
                dom = "national-situation" if i == 3 else "tradition-culture"
            pre = []
            if i > 1:
                pre = [f"pol-e-g{grade}-u{i - 1}"]
            elif grade > 1:
                pre = [f"pol-e-g{grade - 1}-u4"]
            nodes.append(make_node(
                nid=f"pol-e-g{grade}-u{i}",
                name=unit["title"],
                name_en=re.sub(r"[^\w]+", "-", unit["title"]).strip("-").lower()[:40],
                grade=grade,
                domain=dom,
                prerequisites=pre,
                curriculum_points=[
                    f"【课标】{band[min(i - 1, len(band) - 1)]}",
                    f"【教材·{unit['title']}】" + "；".join(unit["lessons"]),
                ],
                stage="elementary",
                extra={
                    "textbook_chapter": f"第{i}单元 {unit['title']}",
                    "textbook_semester": meta.get("semester", "上"),
                    "textbook_edition": meta.get("edition", "统编版"),
                    "chapter_source": "pep-politics-textbooks.json",
                },
            ))
    return nodes


def politics_mid_nodes(tb: dict) -> list[dict]:
    nodes: list[dict] = []
    prev_last: str | None = None
    for g_str in sorted(tb["grades"], key=int):
        grade = int(g_str)
        band = POL_MID_BAND[grade]
        for sem_idx, (sem, meta) in enumerate(sorted(tb["grades"][g_str].items()), 1):
            sk = SEMESTER_KEY.get(sem, sem)
            for i, unit in enumerate(meta["units"], 1):
                dom = POL_MID_THEME.get(i, "civic-duty")
                if grade >= 9:
                    dom = "national-situation" if i <= 2 else "civic-duty"
                nid = f"pol-m-g{grade}-{sk}-u{i}"
                pre: list[str] = []
                if i > 1:
                    pre = [f"pol-m-g{grade}-{sk}-u{i - 1}"]
                elif prev_last:
                    pre = [prev_last]
                nodes.append(make_node(
                    nid=nid,
                    name=unit["title"],
                    name_en=re.sub(r"[^\w]+", "-", unit["title"]).strip("-").lower()[:40],
                    grade=grade,
                    domain=dom,
                    prerequisites=pre,
                    curriculum_points=[
                        f"【课标】{band[min(i - 1, len(band) - 1)]}",
                        f"【教材·{sem}·{unit['title']}】" + "；".join(unit["lessons"]),
                    ],
                    stage="middle",
                    extra={
                        "textbook_chapter": f"第{i}单元 {unit['title']}",
                        "textbook_semester": sem,
                        "textbook_edition": meta.get("edition", "统编版"),
                        "chapter_source": "pep-politics-textbooks-middle.json",
                    },
                ))
                prev_last = nid
    return nodes


def politics_high_nodes(tb: dict) -> list[dict]:
    dom_map = {
        "req1": "socialism",
        "req2": "economy",
        "req3": "politics-law",
        "req4": "philosophy-culture",
        "opt1": "intl-relations",
        "opt2": "law-life",
        "opt3": "logic-thinking",
    }
    nodes: list[dict] = []
    prev: str | None = None
    for book in tb["books"]:
        bid = book["id"]
        lessons = []
        for u in book["units"]:
            lessons.append(f"{u['title']}（" + "；".join(u["lessons"]) + "）")
        cps = [f"【课标】{cp}" for cp in POL_HIGH_BOOK_CP[bid]]
        cps.append(f"【教材·{book['title']}】" + " | ".join(lessons))
        nid = f"pol-h-{bid}"
        pre = [prev] if prev else []
        nodes.append(make_node(
            nid=nid,
            name=book["title"],
            name_en=book["title"],
            grade=book["grade"],
            domain=dom_map[bid],
            prerequisites=pre,
            curriculum_points=cps,
            stage="high",
            extra={
                "textbook_chapter": book["title"],
                "textbook_type": book["type"],
                "textbook_edition": "统编版2019",
                "chapter_source": "pep-politics-textbooks-high.json",
                "curriculum_standard": "普通高中思想政治课程标准（2017年版2020年修订）",
            },
        ))
        prev = nid
    return nodes


def group_politics_nodes(nodes: list[dict], labels: dict[str, str]) -> list[dict]:
    by_dom: dict[str, list] = {}
    for n in nodes:
        by_dom.setdefault(n.pop("domain", "moral-cultivation"), []).append(n)
    order = list(labels.keys())
    domains = []
    for did in order:
        if did not in by_dom:
            continue
        domains.append({
            "id": did,
            "name": labels[did],
            "name_en": did,
            "color": POL_DOMAIN_COLORS.get(did, "#666"),
            "nodes": sorted(by_dom[did], key=lambda x: (x["grade"], x["id"])),
        })
    for did, ns in by_dom.items():
        if did in labels:
            continue
        domains.append({
            "id": did,
            "name": did,
            "name_en": did,
            "color": POL_DOMAIN_COLORS.get(did, "#666"),
            "nodes": sorted(ns, key=lambda x: (x["grade"], x["id"])),
        })
    return domains


def psych_nodes(specs: list, stage: str) -> list[dict]:
    out = []
    for row in specs:
        nid, name, name_en, grade, domain, pre, cps = row
        out.append(make_node(
            nid=nid, name=name, name_en=name_en, grade=grade, domain=domain,
            prerequisites=pre, curriculum_points=cps, stage=stage,
            extra={"chapter_source": "psychology-2012-outline.md",
                   "curriculum_standard": "中小学心理健康教育指导纲要（2012年修订）"},
        ))
    return out


def group_psych_nodes(nodes: list[dict]) -> list[dict]:
    by_dom: dict[str, list] = {}
    for n in nodes:
        by_dom.setdefault(n.pop("domain"), []).append(n)
    domains = []
    for did, (label, color) in PSYCH_DOMAIN_META.items():
        if did not in by_dom:
            continue
        domains.append({
            "id": did,
            "name": label,
            "name_en": did,
            "color": color,
            "nodes": sorted(by_dom[did], key=lambda x: (x["grade"], x["id"])),
        })
    return domains


def politics_tree(nodes: list[dict], stage: str, name: str, grade_range: list[int], unified: bool) -> dict:
    if stage == "elementary":
        labels = {
            "moral-cultivation": "道德修养",
            "health-safety": "生命安全与健康",
            "rule-of-law": "法治启蒙",
            "tradition-culture": "中华优秀传统文化",
            "public-life": "公共生活与规则",
            "national-situation": "国情与公民意识",
        }
        std = "义务教育道德与法治课程标准（2022年版）"
        textbook = "义务教育教科书·道德与法治（统编·人教版）"
    elif stage == "middle":
        labels = {
            "self-growth": "成长中的我",
            "interpersonal": "我与他人和集体",
            "health-safety": "珍爱生命与健康",
            "civic-duty": "我与国家和社会",
            "national-situation": "国情与世界视野",
        }
        std = "义务教育道德与法治课程标准（2022年版）"
        textbook = "义务教育教科书·道德与法治（统编·人教版）"
    else:
        labels = {
            "socialism": "中国特色社会主义",
            "economy": "经济与社会",
            "politics-law": "政治与法治",
            "philosophy-culture": "哲学与文化",
            "intl-relations": "当代国际政治与经济",
            "law-life": "法律与生活",
            "logic-thinking": "逻辑与思维",
        }
        std = "普通高中思想政治课程标准（2017年版2020年修订）"
        textbook = "普通高中教科书·思想政治（统编·人教版）"

    tree = {
        "subject": "politics",
        "name": name,
        "name_en": f"{stage.title()} Politics",
        "grade_range": grade_range,
        "curriculum_standard": std,
        "textbook": textbook,
        "total_nodes": len(nodes),
        "domains": group_politics_nodes(deepcopy(nodes), labels),
    }
    if unified:
        tree["stage_coverage"] = [stage]
    return tree


def psychology_tree(nodes: list[dict], stage: str, name: str, grade_range: list[int], unified: bool) -> dict:
    tree = {
        "subject": "psychology",
        "name": name,
        "name_en": f"{stage.title()} Psychology",
        "grade_range": grade_range,
        "curriculum_standard": "中小学心理健康教育指导纲要（2012年修订）",
        "total_nodes": len(nodes),
        "domains": group_psych_nodes(deepcopy(nodes)),
    }
    if unified:
        tree["stage_coverage"] = [stage]
    return tree


def merge_trees(trees: list[dict], subject: str, name: str, grade_range: list[int]) -> dict:
    all_domains: dict[str, dict] = {}
    total = 0
    for t in trees:
        for dom in t["domains"]:
            did = dom["id"]
            if did not in all_domains:
                all_domains[did] = {**dom, "nodes": []}
            all_domains[did]["nodes"].extend(dom["nodes"])
            total += len(dom["nodes"])
    return {
        "subject": subject,
        "name": name,
        "name_en": "K12 Politics" if subject == "politics" else "K12 Psychology",
        "grade_range": grade_range,
        "stage_coverage": ["elementary", "middle", "high"],
        "total_nodes": total,
        "domains": sorted(all_domains.values(), key=lambda d: d["id"]),
    }


def write_tree(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  ✅ {path.relative_to(ROOT)} ({data.get('total_nodes', '?')} nodes)")


def main() -> int:
    elem_tb = load_json("pep-politics-textbooks.json")
    mid_tb = load_json("pep-politics-textbooks-middle.json")
    high_tb = load_json("pep-politics-textbooks-high.json")

    pol_e = politics_elem_nodes(elem_tb)
    pol_m = politics_mid_nodes(mid_tb)
    pol_h = politics_high_nodes(high_tb)

    psych_e = psych_nodes(PSYCH_ELEM, "elementary")
    psych_m = psych_nodes(PSYCH_MID, "middle")
    psych_h = psych_nodes(PSYCH_HIGH, "high")

    pe = politics_tree(pol_e, "elementary", "小学道德与法治", [1, 6], False)
    pm = politics_tree(pol_m, "middle", "初中道德与法治", [7, 9], False)
    ph = politics_tree(pol_h, "high", "高中思想政治", [10, 12], False)
    p_unified = merge_trees(
        [politics_tree(pol_e, "elementary", "", [1, 6], True),
         politics_tree(pol_m, "middle", "", [7, 9], True),
         politics_tree(pol_h, "high", "", [10, 12], True)],
        "politics", "道德与法治", [1, 12],
    )

    se = psychology_tree(psych_e, "elementary", "小学心理健康教育", [1, 6], False)
    sm = psychology_tree(psych_m, "middle", "初中心理健康教育", [7, 9], False)
    sh = psychology_tree(psych_h, "high", "高中心理健康教育", [10, 12], False)
    s_unified = merge_trees(
        [psychology_tree(psych_e, "elementary", "", [1, 6], True),
         psychology_tree(psych_m, "middle", "", [7, 9], True),
         psychology_tree(psych_h, "high", "", [10, 12], True)],
        "psychology", "心理健康教育", [1, 12],
    )

    write_tree(CN / "elementary" / "politics.json", pe)
    write_tree(CN / "middle" / "politics.json", pm)
    write_tree(CN / "high" / "politics.json", ph)
    write_tree(UNIFIED / "politics.json", p_unified)

    write_tree(CN / "elementary" / "psychology.json", se)
    write_tree(CN / "middle" / "psychology.json", sm)
    write_tree(CN / "high" / "psychology.json", sh)
    write_tree(UNIFIED / "psychology.json", s_unified)

    print(
        f"Done: politics elem={len(pol_e)} mid={len(pol_m)} high={len(pol_h)} total={p_unified['total_nodes']}; "
        f"psych elem={len(psych_e)} mid={len(psych_m)} high={len(psych_h)} total={s_unified['total_nodes']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
