#!/usr/bin/env python3
"""Fill remaining CN deep snippets from curated subject packs.

This pass deliberately avoids political/history nodes. It targets:
- chinese / english / geography
- math / physics / biology tails
- `other` nodes that are clearly Chinese language courseware

Generated snippets are marked as `curated_subject_pack`, not textbook OCR.
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
KP_INDEX_PATH = ROOT / "data" / "kp" / "_index.json"
NODE_INDEX_PATH = ROOT / "data" / "node-index.json"
SOURCE_TAG = "subject_pack_enrichment_2026-06-02"

ALLOWED_SUBJECTS = {"chinese", "english", "geography", "math", "physics", "biology", "other"}
PACK_SOURCE = {
    "chinese": "data/subject-packs/chinese/core-skills-v1.json",
    "english": "data/subject-packs/english/core-skills-v1.json",
    "geography": "data/subject-packs/geography/core-cases-v1.json",
    "math": "data/subject-packs/stem-tail/core-examples-v1.json",
    "physics": "data/subject-packs/stem-tail/core-examples-v1.json",
    "biology": "data/subject-packs/stem-tail/core-examples-v1.json",
    "other": "data/subject-packs/chinese/core-skills-v1.json",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def backup(path: Path, backup_root: Path) -> None:
    target = backup_root / path.relative_to(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def cps(data: dict[str, Any]) -> list[str]:
    out = [str(x).strip() for x in data.get("curriculum_points") or [] if str(x).strip()]
    if out:
        return out[:3]
    for ex in data.get("excerpts") or []:
        if isinstance(ex, dict) and ex.get("text"):
            out.append(str(ex["text"]).strip())
    return out[:3]


def chinese_category(domain: str, name: str) -> str:
    text = domain + name
    if "拼音" in text or "声母" in text or "韵母" in text or "音节" in text:
        return "拼音"
    if "识字" in text or "写字" in text or "汉字" in text or "笔画" in text or "部首" in text or "查字典" in text or "书法" in text:
        return "识字写字"
    if "词" in text or "成语" in text or "谚语" in text or "修辞" in text:
        return "词语修辞"
    if "句" in text or "标点" in text or "病句" in text or "复句" in text:
        return "句子标点"
    if "写作" in text or "作文" in text or "日记" in text or "应用文" in text or "读后感" in text:
        return "写作表达"
    if "口语" in text or "听故事" in text or "讲述" in text or "辩论" in text:
        return "口语交际"
    if "古诗" in text or "文言" in text or "诗" in text or "小古文" in text:
        return "古诗文"
    if "整本书" in text or "名著" in text or "西游记" in text or "朝花夕拾" in text:
        return "整本书阅读"
    return "阅读理解"


def chinese_snippets(name: str, domain: str, cp: list[str]) -> list[str]:
    cat = chinese_category(domain, name)
    base = cp[0] if cp else f"围绕{name}进行语言理解与表达训练。"
    if cat == "拼音":
        return [
            f"【拼音规则资料】{name}的学习应把“听辨音—看清形—拼读音节—迁移到识字阅读”连成一条链。课堂可先让学生听辨教师示范音，再观察口形和发音部位，最后把声母、韵母和声调组合成完整音节。关键不是孤立背表，而是在词语和短句中读准、拼准、写准。课标关联：{base}",
            f"【拼读任务样例】围绕{name}可设计三步任务：第一步给出若干音节，让学生圈出声母、韵母和声调；第二步把音节与图画或汉字配对；第三步读一句含目标音节的短句，并说明哪个音最容易混淆。易错点通常是前后鼻音、平翘舌、复韵母和声调位置。"
        ]
    if cat == "识字写字":
        return [
            f"【识字写字资料】{name}应从字音、字形、字义和用法四个方面建立联系。教学可用“看结构—认部件—说意思—组词造句”的流程，帮助学生把汉字当成有结构的语言符号，而不是孤立图形。课标关联：{base}",
            f"【字词活动样例】围绕{name}可选取一组同部件或同结构汉字，让学生观察左右、上下、包围等结构，标出关键笔画，比较形近字，再放入词语和句子中使用。评价重点是读音准确、结构辨析、书写规范和语境运用。"
        ]
    if cat == "词语修辞":
        return [
            f"【词语修辞资料】{name}的核心是把词语放回语境中理解。学生需要结合上下文、感情色彩、搭配对象和表达效果判断词义，而不是只背词典解释。若涉及比喻、拟人、夸张等修辞，应同时回答“写了什么、像什么、有什么效果”。课标关联：{base}",
            f"【语境练习样例】给出一段描写性文字，让学生找出与{name}相关的词语或修辞，先解释字面意思，再说明在句中表达的人物心情、景物特点或作者态度，最后仿写一句。"
        ]
    if cat == "句子标点":
        return [
            f"【句子标点资料】{name}的学习应关注句子的结构、语气和表达目的。判断句式或标点时，要先读懂句意，再看停顿、语气、逻辑关系和前后照应。课标关联：{base}",
            f"【句式转换任务】围绕{name}可设计“原句—变换—比较”任务：把一句话改成不同句式或补充标点，要求学生说明意思是否改变、语气是否改变、表达是否更清楚。"
        ]
    if cat == "写作表达":
        return [
            f"【写作表达资料】{name}不是套模板，而是围绕对象、目的、材料和结构组织表达。写作前要明确写给谁、为什么写、重点材料是什么；写作中要做到内容具体、顺序清楚、语言得体。课标关联：{base}",
            f"【写作支架样例】围绕{name}可使用“四格支架”：①我要表达的中心；②我选择的材料或事例；③我采用的顺序和段落；④我检查语言是否准确生动。评价时看中心是否明确、材料是否具体、段落是否连贯。"
        ]
    if cat == "口语交际":
        return [
            f"【口语交际资料】{name}强调在真实交流中听清、说明、回应和调整表达。学生不仅要会说，还要会倾听、抓重点、按对象和场合选择合适语气。课标关联：{base}",
            f"【交际活动样例】围绕{name}可设置两人或小组任务：一人讲述经历或观点，另一人复述关键信息并追问。评价重点是信息完整、表达有序、态度礼貌、能根据反馈调整说法。"
        ]
    if cat == "古诗文":
        return [
            f"【古诗文资料】{name}的学习要从诵读入手，在节奏、停顿和关键词中理解诗文大意。学生可先读准字音和节奏，再抓意象、人物、情境和情感，最后用自己的话说出诗文内容。课标关联：{base}",
            f"【赏析任务样例】选择一首或一段古诗文，让学生完成四步：读准节奏，解释关键词，描绘画面，说明情感或道理。若涉及文言虚词和句式，应结合上下文解释，不孤立背义项。"
        ]
    if cat == "整本书阅读":
        return [
            f"【整本书阅读资料】{name}应关注人物、情节、环境、主题和阅读方法。学生需要持续记录阅读线索，比较人物变化，梳理关键事件，并用证据支持自己的评价。课标关联：{base}",
            f"【阅读档案任务】围绕{name}可建立阅读档案：人物关系图、情节时间线、精彩语句摘录、问题清单和读后观点。评价重点不是复述情节多少，而是能否用文本证据说明理解。"
        ]
    return [
        f"【阅读理解资料】{name}的核心是回到文本证据。学生应先整体把握写了什么，再抓关键词句、段落关系、表达方法和作者态度，最后形成有依据的解释。课标关联：{base}",
        f"【阅读任务样例】围绕{name}可设计问题链：①这段主要写什么；②哪些词句最关键；③这些词句表现了什么；④如果换一种说法，表达效果有什么变化。回答时必须引用文本依据。"
    ]


def english_category(domain: str, name: str) -> str:
    text = (domain + name).lower()
    if "拼读" in text or "音" in text or "alphabet" in text or "phonics" in text:
        return "phonics"
    if "词汇" in text or "vocab" in text or "word" in text:
        return "vocabulary"
    if "语法" in text or "句型" in text or "there be" in text or "preposition" in text:
        return "grammar"
    if "写作" in text or "writing" in text:
        return "writing"
    if "听说" in text or "对话" in text or "greeting" in text or "conversation" in text:
        return "speaking"
    return "reading"


def english_snippets(name: str, domain: str, cp: list[str]) -> list[str]:
    cat = english_category(domain, name)
    base = cp[0] if cp else f"Use {name} in meaningful context."
    if cat == "phonics":
        return [
            f"【Phonics pack】{name} should be taught through sound-letter mapping, blending, segmenting, and word reading. Learners first hear the target sound, then identify the spelling pattern, blend it in words, and finally read a short sentence with meaning. Curriculum link: {base}",
            f"【Practice task】For {name}, prepare minimal pairs or word families, ask students to mark the target letters, read aloud, sort words by sound, and create one new sentence. Assessment focuses on accuracy, fluency, and whether students can transfer the rule to unfamiliar words."
        ]
    if cat == "grammar":
        return [
            f"【Grammar pack】{name} should follow the form-meaning-use path. Form shows the structure, meaning explains what idea it expresses, and use places it in a real situation. Students should not only name the grammar point but also choose it to complete a communicative purpose. Curriculum link: {base}",
            f"【Context task】For {name}, give a short dialogue or picture prompt. Students notice examples, complete controlled sentences, then produce two original sentences about school, family, hobbies, or daily life. Feedback should mention both grammar accuracy and meaning."
        ]
    if cat == "vocabulary":
        return [
            f"【Vocabulary pack】{name} works best when words are learned in semantic groups and used in context. Students connect pronunciation, spelling, meaning, collocation, and sentence use rather than memorizing isolated translations. Curriculum link: {base}",
            f"【Word-use task】For {name}, build a small word bank, match words with pictures or situations, classify them by topic, and use at least three words in a meaningful sentence or mini-dialogue."
        ]
    if cat == "writing":
        return [
            f"【Writing pack】{name} should be supported by sentence frames, model texts, and revision checklists. Students first understand the purpose and audience, then organize ideas, draft sentences, and revise for grammar, vocabulary, and coherence. Curriculum link: {base}",
            f"【Writing task】For {name}, provide a picture or situation, list useful words and sentence patterns, ask students to write 4–6 sentences, then check: clear topic, correct tense, logical order, and readable spelling."
        ]
    if cat == "speaking":
        return [
            f"【Speaking pack】{name} requires listening, turn-taking, and purposeful expression. Students should practice useful chunks in a meaningful situation, not recite disconnected sentences. Curriculum link: {base}",
            f"【Role-play task】For {name}, set a classroom, home, travel, or shopping situation. Students work in pairs, use target expressions, ask one follow-up question, and respond appropriately. Assessment focuses on intelligibility, relevance, and interaction."
        ]
    return [
        f"【Reading pack】{name} should train students to get gist, locate details, infer meaning from context, and connect information across sentences. The text should be short enough for close reading and rich enough for questions. Curriculum link: {base}",
        f"【Reading task】For {name}, use a short passage or dialogue. Students answer one gist question, two detail questions, one vocabulary-in-context question, and one personal response question using evidence from the text."
    ]


def geography_category(domain: str, name: str) -> str:
    text = domain + name
    if "地球" in text or "地图" in text or "经纬" in text or "等高线" in text or "四季" in text:
        return "map"
    if "气候" in text or "水" in text or "地貌" in text or "地壳" in text or "河流" in text or "植被" in text or "土壤" in text or "自然" in text:
        return "natural"
    if "人口" in text or "城市" in text or "产业" in text or "工业" in text or "农业" in text or "交通" in text or "服务" in text:
        return "human"
    if "中国" in text or "北方" in text or "南方" in text or "青藏" in text or "珠江" in text or "长江" in text:
        return "china"
    if "世界" in text or "大洲" in text or "国家" in text:
        return "world"
    return "resource"


def geography_snippets(name: str, domain: str, cp: list[str]) -> list[str]:
    cat = geography_category(domain, name)
    base = cp[0] if cp else f"分析{name}相关地理现象。"
    if cat == "map":
        return [
            f"【地图技能资料】{name}的学习应从读图开始：先看图名、比例尺、方向和图例，再定位关键地理事物，最后用经纬度、方位、距离或高度描述空间关系。课标关联：{base}",
            f"【读图任务样例】给出一幅地图或示意图，让学生完成定位、判读、描述和解释四步。评价重点是是否使用地图证据，而不是只背结论。"
        ]
    if cat == "natural":
        return [
            f"【自然地理资料】{name}应按照“要素—过程—结果—影响”的路径理解。学生先识别气候、水文、地貌、植被或土壤等要素，再说明形成过程和空间差异。课标关联：{base}",
            f"【过程分析任务】围绕{name}可设置一张示意图或数据表，让学生描述变化过程，找出主要影响因素，并解释对生产生活或生态环境的影响。"
        ]
    if cat == "human":
        return [
            f"【人文地理资料】{name}要从区位条件、空间分布、区域联系和人地关系分析。学生需要比较自然条件、交通、市场、劳动力、政策和技术等因素如何共同影响地理现象。课标关联：{base}",
            f"【区位分析任务】选择一个真实区域案例，让学生列出有利和不利条件，画出因素关系图，并提出合理的发展或优化建议。"
        ]
    if cat == "china":
        return [
            f"【中国地理资料】{name}应联系中国区域差异和现实发展。分析时先确定区域位置，再比较地形、气候、河流、资源、人口和产业等要素，最后说明区域发展特点。课标关联：{base}",
            f"【区域比较任务】围绕{name}可比较两个区域的自然与人文条件，要求学生用地图和数据说明差异，并解释这些差异如何影响生产生活。"
        ]
    if cat == "world":
        return [
            f"【世界地理资料】{name}强调从全球视角认识区域差异。学生应先定位大洲、海洋或国家，再从纬度位置、海陆位置、地形气候和人类活动分析区域特征。课标关联：{base}",
            f"【世界区域任务】给出世界地图和一个区域材料，让学生描述位置，提取自然和人文特征，并说明该区域与其他地区的联系。"
        ]
    return [
        f"【资源环境资料】{name}需要把资源利用、生态环境和可持续发展联系起来。学生应识别问题表现、形成原因、影响范围和治理措施。课标关联：{base}",
        f"【可持续发展任务】围绕{name}选择一个真实问题，让学生分析利益相关者、资源约束和环境影响，并提出兼顾经济、社会和生态的方案。"
    ]


def stem_snippets(subject: str, name: str, domain: str, cp: list[str]) -> list[str]:
    base = cp[0] if cp else f"理解{name}的核心概念。"
    if subject == "math":
        return [
            f"【数学尾巴资料】{name}应从具体问题、图形或数据出发，抽象出数学对象、关系和方法。教学时先明确条件和目标，再选择合适表示：算式、图形、表格、符号或模型。课标关联：{base}",
            f"【数学任务样例】围绕{name}设计一道“解释方法”的题：学生不仅给答案，还要说明为什么这样建模、为什么该性质成立、结果在原情境中代表什么。"
        ]
    if subject == "physics":
        return [
            f"【物理尾巴资料】{name}应通过可观察现象、实验装置或技术应用建立理解。学生需要描述现象，识别物理量，说明条件，再用规律解释结果。课标关联：{base}",
            f"【物理任务样例】围绕{name}设置预测—实验—解释任务：先预测变化，再说明控制变量和观察量，最后用物理规律解释数据或现象。"
        ]
    return [
        f"【生物尾巴资料】{name}应围绕生命现象中的结构、功能、过程和适应关系展开。学生要用观察、图示、比较或实验资料解释生命活动。课标关联：{base}",
        f"【生物任务样例】围绕{name}给出一幅结构图、流程图或生活案例，让学生说明关键结构/过程、功能意义和证据依据。"
    ]


def make_snippets(data: dict[str, Any], subject: str) -> list[dict[str, Any]]:
    name = data.get("name") or data.get("kp_id")
    domain = data.get("domain_name") or ""
    cp = cps(data)
    if subject == "other" and str(data.get("kp_id", "")).startswith("chn-"):
        subject = "chinese"
    if subject == "chinese":
        texts = chinese_snippets(name, domain, cp)
    elif subject == "english":
        texts = english_snippets(name, domain, cp)
    elif subject == "geography":
        texts = geography_snippets(name, domain, cp)
    elif subject in {"math", "physics", "biology"}:
        texts = stem_snippets(subject, name, domain, cp)
    else:
        return []
    source = PACK_SOURCE.get(subject if subject != "other" else "chinese", "data/subject-packs/stem-tail/core-examples-v1.json")
    return [
        {
            "source": source,
            "text": text,
            "score": 70 - i * 5,
            "match_terms": [name, domain] + cp[:1],
            "source_type": "curated_subject_pack",
            "reason": "domain_and_subject_pack_match"
        }
        for i, text in enumerate(texts)
    ]


def worked_example(data: dict[str, Any], snippets: list[dict[str, Any]]) -> dict[str, Any]:
    name = data.get("name") or data.get("kp_id")
    subject = data.get("subject") or ""
    if subject == "chinese" or (subject == "other" and str(data.get("kp_id", "")).startswith("chn-")):
        stem = f"根据资料包，为「{name}」设计一个文本理解或表达任务。"
        outline = "先给出语言材料或表达情境，再要求学生说明依据，最后完成迁移表达。"
    elif subject == "english":
        stem = f"Use the pack to design a context-based activity for {name}."
        outline = "Follow noticing, controlled practice, and meaningful output."
    elif subject == "geography":
        stem = f"根据资料包，为「{name}」设计一个读图、区域分析或案例解释任务。"
        outline = "先提取空间信息，再分析地理关系，最后形成有证据的解释。"
    else:
        stem = f"根据资料包，为「{name}」设计一个概念解释或应用任务。"
        outline = "先明确核心概念，再设计问题情境，最后要求学生解释依据。"
    return {"stem": stem, "solution_outline": outline, "evidence_excerpt": snippets[0]["text"][:260] if snippets else "", "source": SOURCE_TAG}


def backup(path: Path, backup_root: Path) -> None:
    target = backup_root / path.relative_to(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def process(args: argparse.Namespace) -> dict[str, Any]:
    idx = load_json(KP_INDEX_PATH)["kps"]
    node = load_json(NODE_INDEX_PATH).get("nodes", {}) if NODE_INDEX_PATH.exists() else {}
    subjects = set(args.subject or [])
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = ROOT / "data" / "kp" / "_backups" / f"subject-pack-cn-{run_id}"
    stats: Counter[str] = Counter()
    by_subject: dict[str, Counter[str]] = defaultdict(Counter)
    changed_files: list[str] = []
    for kp, rel in sorted(idx.items()):
        path = ROOT / rel
        if not path.exists():
            continue
        data = load_json(path)
        if (data.get("curriculum") or node.get(kp, {}).get("curriculum")) != "cn":
            continue
        subject = data.get("subject") or node.get(kp, {}).get("subject") or "unknown"
        if subjects and subject not in subjects:
            continue
        if subject not in ALLOWED_SUBJECTS:
            by_subject[subject]["skipped_subject"] += 1
            continue
        by_subject[subject]["seen"] += 1
        if (data.get("supplements") or {}).get("deep_textbook_snippets"):
            by_subject[subject]["already_deep"] += 1
            continue
        snippets = make_snippets(data, subject)
        if not snippets:
            by_subject[subject]["no_pack"] += 1
            continue
        sup = data.setdefault("supplements", {})
        tc = data.setdefault("textbook_content", {})
        sup["deep_textbook_snippets"] = snippets
        sup["deep_textbook_source"] = SOURCE_TAG
        sup["deep_textbook_enriched_at"] = utc_now()
        sup["deep_worked_example"] = worked_example(data, snippets)
        tc["deep_snippets"] = snippets[:3]
        tc["deep_source"] = SOURCE_TAG
        meta = data.setdefault("_meta", {})
        sources = meta.setdefault("sources", [])
        if isinstance(sources, list) and SOURCE_TAG not in sources:
            sources.append(SOURCE_TAG)
        changed_files.append(str(path.relative_to(ROOT)))
        by_subject[subject]["changed"] += 1
        stats["nodes_enriched"] += 1
        stats["snippets_added"] += len(snippets)
        if not args.dry_run:
            backup(path, backup_root)
            dump_json(path, data)
            stats["written_files"] += 1
        else:
            stats["would_write_files"] += 1
    report = {
        "run_at": utc_now(),
        "dry_run": args.dry_run,
        "backup_dir": str(backup_root.relative_to(ROOT)),
        "stats": dict(stats),
        "by_subject": {k: dict(v) for k, v in sorted(by_subject.items())},
        "changed_files_count": len(changed_files),
        "changed_files_sample": changed_files[:80],
    }
    if not args.dry_run:
        backup_root.mkdir(parents=True, exist_ok=True)
        (backup_root / "subject-pack-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Fill remaining CN deep snippets from curated subject packs")
    parser.add_argument("--subject", action="append")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    print(json.dumps(process(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
