#!/usr/bin/env python3
"""Auto-generate cn course spec JSON from KP + tree node.

Usage:
  python3 kp-to-cn-spec.py --node-id it-h-algorithm-concept
  python3 kp-to-cn-spec.py --node-id hist-m-ancient-china --out scripts/cn-specs/
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
_map_path = SCRIPT_DIR / "cn-map-config.py"
if _map_path.is_file():
    _spec = importlib.util.spec_from_file_location("cn_map_config", _map_path)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    default_map_config = _mod.default_map_config
else:
    def default_map_config(_spec):  # type: ignore
        return None

ROOT = Path(__file__).resolve().parents[1]
KP_ROOT = ROOT / "data" / "kp"
TREE_ROOT = ROOT / "data" / "trees" / "cn"
SPECS_DIR = ROOT / "scripts" / "cn-specs"

SUBJECT_META = {
    "chinese": {"theme": "orange", "label": "语文", "lesson": "text-evidence"},
    "english": {"theme": "blue", "label": "英语", "lesson": "language-practice"},
    "math": {"theme": "blue", "label": "数学", "lesson": "concept-procedure"},
    "history": {"theme": "orange", "label": "历史", "lesson": "historical-inquiry"},
    "geography": {"theme": "green", "label": "地理", "lesson": "spatial-analysis"},
    "science": {"theme": "green", "label": "科学", "lesson": "concept-inquiry"},
    "biology": {"theme": "green", "label": "生物", "lesson": "concept-inquiry"},
    "chemistry": {"theme": "blue", "label": "化学", "lesson": "concept-inquiry"},
    "physics": {"theme": "blue", "label": "物理", "lesson": "concept-inquiry"},
    "info-tech": {"theme": "blue", "label": "信息科技", "lesson": "computational-thinking"},
    "politics": {"theme": "orange", "label": "道德与法治", "lesson": "value-inquiry"},
    "psychology": {"theme": "green", "label": "心理健康", "lesson": "reflection-activity"},
}

STAGE_LABEL = {"elementary": "小学", "middle": "初中", "high": "高中"}


def find_kp(node_id: str) -> dict:
    for sub in KP_ROOT.iterdir():
        p = sub / f"{node_id}.json"
        if p.is_file():
            return json.loads(p.read_text(encoding="utf-8"))
    raise FileNotFoundError(f"No KP file for {node_id}")


def find_tree_node(node_id: str) -> tuple[dict, str, str]:
    for tree_path in TREE_ROOT.rglob("*.json"):
        stage = tree_path.parts[tree_path.parts.index("cn") + 1]
        subject = tree_path.stem
        data = json.loads(tree_path.read_text(encoding="utf-8"))
        found = None

        def walk(obj):
            nonlocal found
            if isinstance(obj, dict):
                if obj.get("id") == node_id:
                    found = obj
                for v in obj.values():
                    if isinstance(v, (dict, list)):
                        walk(v)
            elif isinstance(obj, list):
                for item in obj:
                    walk(item)

        walk(data)
        if found:
            return found, stage, subject
    return {}, "middle", node_id.split("-")[0]


def texts_from_kp(kp: dict) -> list[str]:
    out = []
    for e in kp.get("excerpts", []):
        t = (e.get("text") or "").strip()
        if t and t not in out:
            out.append(t)
    for t in kp.get("curriculum_points", []):
        t = (t or "").strip()
        if t and t not in out:
            out.append(t)
    desc = (kp.get("description") or kp.get("textbook_content", {}).get("summary") or "").strip()
    if desc and desc not in out:
        out.append(desc)
    return out[:6]


def password_for(node_id: str) -> str:
    tail = node_id.split("-")[-1].replace("_", "")[:12]
    return f"{tail}+2026"


def make_drag(subject: str, name: str, texts: list[str]) -> dict:
    """Simple 4-item classification drag from curriculum snippets."""
    zones = [
        {"id": "core", "label": "核心概念"},
        {"id": "method", "label": "方法/技能"},
        {"id": "apply", "label": "应用情境"},
        {"id": "miscon", "label": "常见误区"},
    ]
    labels = [
        f"📌 理解{name}的基本含义",
        f"🔍 用证据分析{name}",
        f"🌍 在真实情境中运用{name}",
        f"⚠️ 只背结论不联系材料",
    ]
    if subject == "english":
        labels = [
            "📖 读懂语篇主旨",
            "📝 归纳语法/词汇规则",
            "💬 在交际中运用表达",
            "⚠️ 脱离语境死记答案",
        ]
    elif subject == "math":
        labels = [
            "📐 掌握定义与公式",
            "✏️ 按步骤规范运算",
            "🧩 解决实际问题",
            "⚠️ 只记答案不验算",
        ]
    elif subject == "history":
        labels = [
            "📜 明确史实与时间",
            "🔗 分析因果与影响",
            "🏛️ 联系史料得出结论",
            "⚠️ 以今律古或空泛议论",
        ]
    items = [
        {"label": labels[0], "zone": "core"},
        {"label": labels[1], "zone": "method"},
        {"label": labels[2], "zone": "apply"},
        {"label": labels[3], "zone": "miscon"},
    ]
    return {
        "title": f"分一分：{name}学习要素归类",
        "instruction": "把卡片拖到<strong>核心概念 / 方法技能 / 应用情境 / 常见误区</strong>。",
        "tsh": "互动 - 概念归类",
        "zone_columns": "repeat(auto-fit,minmax(160px,1fr))",
        "items": items,
        "zones": zones,
        "ok_msg": f"分类正确！学习{name}要概念、方法、应用三位一体，并警惕常见误区。",
        "bad_msg": "再想想：前三项分别对应概念理解、方法运用、情境应用；最后一项是误区。",
        "pending_msg": "拖完 4 项后自动判分。",
    }


def build_spec(node_id: str) -> dict:
    kp = find_kp(node_id)
    tree_node, stage, subject = find_tree_node(node_id)
    meta = SUBJECT_META.get(subject, {"theme": "blue", "label": subject, "lesson": "concept-inquiry"})
    name = kp.get("name") or tree_node.get("name") or node_id
    grade = kp.get("grade") or tree_node.get("grade") or 7
    texts = texts_from_kp(kp)
    t1, t2 = texts[0] if texts else f"{name}是国家课程标准要求掌握的重要内容。", texts[1] if len(texts) > 1 else f"学习{name}要注重理解概念、掌握方法并能在情境中运用。"
    t3 = texts[2] if len(texts) > 2 else f"能把{name}的知识迁移到新情境，才算真正掌握。"

    stage_cn = STAGE_LABEL.get(stage, stage)
    subj_cn = meta["label"]
    curriculum = f"义务教育课程标准（2022年版）· {stage_cn}{subj_cn}"

    choices = [
        f"{name}的核心概念是什么？",
        f"怎样用课标要求的方法学习{name}？",
        f"{name}在考试或生活中如何应用？",
        f"学习{name}时我最容易错在哪里？",
    ]

    objectives = [
        f"能说出{name}的核心概念与课标要求",
        f"能运用所学方法分析{name}相关典型问题",
        f"能在情境中正确应用{name}的知识与技能",
        f"能识别并纠正关于{name}的常见误区",
    ]
    if len(texts) >= 3:
        objectives[0] = f"能复述课标要点：{texts[0][:60]}…" if len(texts[0]) > 60 else f"能复述课标要点：{texts[0]}"

    pwd = password_for(node_id)

    return {
        "node_id": node_id,
        "title": name,
        "subtitle": t1[:120] + ("…" if len(t1) > 120 else ""),
        "name_en": kp.get("name_en") or tree_node.get("name_en") or name,
        "grade": int(grade),
        "stage": stage,
        "subject": subject,
        "theme_color": meta["theme"],
        "lesson_type": meta["lesson"],
        "domain": kp.get("domain_id") or tree_node.get("domain_id") or subject,
        "description": f"{stage_cn}{subj_cn}：{name}互动课件，对齐国家课程标准。",
        "tags": [name, subj_cn, stage_cn],
        "curriculum": curriculum,
        "password_hint": pwd,
        "hero_caption": f"{name}：概念—方法—应用",
        "problem_anchor": {
            "prompt": "今天你最想弄懂哪个问题？",
            "choices": choices,
        },
        "objectives": objectives,
        "pretest": {
            "question": f"学习「{name}」时，第一步最应该做什么？",
            "choices": [
                "明确课标要求，建立概念框架再练习",
                "直接刷题，不用理解概念",
                "只背结论，不做情境分析",
            ],
            "correct": 0,
            "ok_msg": "对了！先建立概念与方法框架，再练习巩固。",
            "bad_msg": "应先理解课标要求与核心概念，再练习与应用。",
        },
        "sections": [
            {
                "id": "concept-core",
                "tts": "concept-core",
                "tsh": f"核心 - {name}",
                "title": f"{name}：课标核心是什么？",
                "paragraphs": [
                    f"<strong>{name}</strong>是{stage_cn}{subj_cn}的重要内容。{t1}",
                    t2,
                ],
                "image": "concept-diagram.svg",
                "caption": f"{name}核心概念示意",
            },
            {
                "id": "example-apply",
                "tts": "example-apply",
                "tsh": f"应用 - {name}",
                "title": f"怎样学好{name}？",
                "paragraphs": [
                    f"学习路径：<strong>明确概念</strong>→<strong>掌握方法</strong>→<strong>情境练习</strong>→<strong>反思纠错</strong>。",
                    t3,
                ],
                "image": "process-diagram.svg",
                "caption": f"{name}方法与应用",
            },
        ],
        "drag_activity": make_drag(subject, name, texts),
        "practice": {
            "title": f"用{name}知识解决问题",
            "explain_prompt": f"请结合课标要点，用2–3句话解释你如何理解「{name}」，并举一个应用例子。",
            "explain_placeholder": "我的理解：……例如：……",
            "hint": "提示：先写核心概念，再写方法或步骤，最后举一个具体情境例子。",
            "extra_prompt": f"关于{name}，你曾犯过什么错误？后来怎样改正？",
            "extra_placeholder": "错误：……改正：……",
        },
        "posttest": {
            "question": f"关于{name}的学习，哪种做法最科学？",
            "choices": [
                "理解课标概念，掌握方法，在情境中练习并反思",
                "只背答案，不做分析",
                "忽略课标，凭感觉答题",
            ],
            "correct": 0,
            "ok_msg": "正确！概念+方法+情境练习是高效学习路径。",
            "bad_msg": "应回到课标概念与方法，结合情境练习。",
        },
        "summary": {
            "items": [
                f"明确了{name}的课标核心要求。",
                f"掌握了学习{name}的基本路径：概念—方法—应用。",
                "能识别常见误区并主动纠错。",
            ],
            "transfer": f"找一道与「{name}」相关的练习题或生活情境，用本课方法完整解答一遍。",
        },
    }
    if subject in ("history", "geography"):
        spec["map_config"] = default_map_config(spec)
    return spec


def agnes_batch(spec: dict) -> list[dict]:
    nid = spec["node_id"]
    subj = spec.get("subject", "course")
    name = spec["title"]
    return [
        {
            "name": f"{nid}-hero",
            "slot": "hero",
            "prompt": (
                f"Educational hero illustration for {subj} lesson {name}, "
                f"grade {spec['grade']}, clean flat style, engaging classroom scene. "
                "STRICTLY NO TEXT no Chinese no letters no labels"
            ),
        },
        {
            "name": "section1",
            "slot": "section1",
            "prompt": (
                f"Concept diagram for {name} core ideas {subj} education visual icons. "
                "STRICTLY NO TEXT no Chinese no letters no labels"
            ),
        },
        {
            "name": "section2",
            "slot": "section2",
            "prompt": (
                f"Application scenario illustration for {name} methods and practice {subj}. "
                "STRICTLY NO TEXT no Chinese no letters no labels"
            ),
        },
    ]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--node-id", required=True)
    ap.add_argument("--out", default=str(SPECS_DIR))
    ap.add_argument("--write-batch", action="store_true")
    args = ap.parse_args()
    spec = build_spec(args.node_id.strip())
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    spec_path = out_dir / f"{spec['node_id']}.json"
    spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✅ spec → {spec_path}")
    if args.write_batch:
        batch_path = out_dir / f"batch-{spec['node_id']}.json"
        batch_path.write_text(json.dumps(agnes_batch(spec), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"✅ batch → {batch_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
