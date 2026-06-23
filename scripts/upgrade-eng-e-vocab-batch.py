#!/usr/bin/env python3
"""Upgrade eng-e-vocab-* elementary English vocabulary courseware batch.

Patches HTML/manifest for TeachAny v7 teaching-quality baseline while preserving
existing game interactions. Then runs finalize (TTS) and knowledge-context emit.

Usage:
  python3 scripts/upgrade-eng-e-vocab-batch.py
  python3 scripts/upgrade-eng-e-vocab-batch.py --no-audio
  python3 scripts/upgrade-eng-e-vocab-batch.py --only eng-e-vocab-600-words
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
TREE = ROOT / "data/trees/cn/elementary/english.json"

COURSE_IDS = [
    "eng-e-vocab-family-school",
    "eng-e-vocab-daily-life",
    "eng-e-vocab-nature-society",
    "eng-e-vocab-600-words",
]

PANELS: dict[str, list[dict]] = {
    "eng-e-vocab-family-school": [
        {
            "after_id": "objectives",
            "html": """
<section class="section" id="vocab-curriculum-guide" data-tts="vocab-curriculum-guide" data-bloom-level="understand" data-scaffold="full">
  <h2 class="section-title">📖 课标导读：家庭与校园词汇怎么学</h2>
  <div class="lesson-panel" style="background:#fff;border-radius:14px;padding:20px;line-height:1.85;box-shadow:0 4px 14px rgba(0,0,0,.08)">
    <p>义务教育英语课标要求词汇学习坚持<strong>音、形、义、用</strong>结合：先听准发音，再认读词形，在图片和语境里理解含义，最后在句子中表达。家庭与校园主题词如 <em>mother, classroom, friend</em> 要在真实对话里反复出现，而不是脱离语境死记。</p>
    <p><strong>学习策略：</strong>看到图片先说英文，再模仿语调；遇到不会读的词，先分音节再整体拼读。常见误区是把中文意思背下来却不会开口——诊断提示：如果你只能说中文释义，说明还没完成“用”的环节。</p>
    <p><strong>迁移任务：</strong>设计一张“My Family & School”海报，至少用 8 个本课词汇写 3 句英语介绍，并说明你为什么选择这些词。</p>
  </div>
</section>""",
        },
        {
            "after_id": "warmup",
            "html": """
<section class="section" id="vocab-practice-guide" data-tts="vocab-practice-guide" data-bloom-level="apply" data-scaffold="partial">
  <h2 class="section-title">🧭 词汇练习策略</h2>
  <div class="lesson-panel" style="background:#f8fffe;border-radius:14px;padding:20px;line-height:1.85">
    <p>分类浏览时，请按<strong>主题—发音—拼写—例句</strong>四步走：先判断词属于家庭还是校园场景，再跟读音标，闭音节/open syllable 影响拼写时要特别留意。错误诊断：把 <em>classroom</em> 写成 <em>classrom</em> 往往是元音字母数量没对齐。</p>
    <p>游戏关卡训练的是<strong>快速识别与拼写自动化</strong>，请在答错时回看词卡上的例句，分析是“义”混淆还是“形”混淆，而不是只记正确答案。</p>
  </div>
</section>""",
        },
    ],
    "eng-e-vocab-daily-life": [
        {
            "after_id": "objectives",
            "html": """
<section class="section" id="vocab-curriculum-guide" data-tts="vocab-curriculum-guide" data-bloom-level="understand" data-scaffold="full">
  <h2 class="section-title">📖 课标导读：日常生活词汇</h2>
  <div class="lesson-panel" style="background:#fff;border-radius:14px;padding:20px;line-height:1.85;box-shadow:0 4px 14px rgba(0,0,0,.08)">
    <p>日常生活主题词汇（食物、衣物、交通、时间等）要在<strong>可观察的情境</strong>中学习。课标强调借助图片、实物和动作理解词义，并在语境中反复再现，避免机械抄写。</p>
    <p>学习时把单词放进问句：<em>What do you eat for breakfast?</em> <em>How do you go to school?</em> 这样能把“认读”升级为“表达”。诊断提示：若你只能中英互译而不能造句，需回到语境练习。</p>
    <p><strong>开放任务：</strong>用 10 个日常词汇写一段 Morning Routine 短文，并解释每个词在生活中的使用场景。</p>
  </div>
</section>""",
        },
        {
            "after_id": "warmup",
            "html": """
<section class="section" id="vocab-practice-guide" data-tts="vocab-practice-guide" data-bloom-level="apply" data-scaffold="partial">
  <h2 class="section-title">🧭 听读拼练要点</h2>
  <div class="lesson-panel" style="background:#f8fffe;border-radius:14px;padding:20px;line-height:1.85">
    <p>Speed Round 训练<strong>听音辨义</strong>，Spelling 训练<strong>形义联结</strong>。遇到近义词（如 <em>big/large</em>）要比较搭配：不是所有同义词都能互换。错因分析：选错往往因为只看中文“大”，没注意英文搭配习惯。</p>
  </div>
</section>""",
        },
        {
            "after_id": "level2",
            "html": """
<section class="section" id="vocab-core-examples" data-tts="vocab-core-examples" data-bloom-level="analyze" data-scaffold="partial">
  <h2 class="section-title">📝 核心词汇例句库</h2>
  <div class="lesson-panel" style="background:#fff;border-radius:14px;padding:20px;line-height:1.85">
    <p><em>I brush my teeth every morning.</em> — 把 <strong>brush</strong> 放进日常习惯句型。<em>She wears a red coat in winter.</em> — <strong>wear</strong> 强调状态而非动作。<em>We take the bus to the supermarket.</em> — 交通与场所词要同句出现。请为每个例句标注：主题词、动词时态、易错拼写点，并口头复述一次。</p>
    <p>诊断提示：拼写题若把 <em>Wednesday</em> 写成 <em>Wensday</em>，说明未建立“不规则拼写卡片”；应把词拆音节 Wed-nes-day 并跟读三遍。</p>
  </div>
</section>""",
        },
    ],
    "eng-e-vocab-nature-society": [
        {
            "after_id": "objectives",
            "html": """
<section class="section" id="vocab-curriculum-guide" data-tts="vocab-curriculum-guide" data-bloom-level="understand" data-scaffold="full">
  <h2 class="section-title">📖 课标导读：自然与社会词汇</h2>
  <div class="lesson-panel" style="background:#fff;border-radius:14px;padding:20px;line-height:1.85;box-shadow:0 4px 14px rgba(0,0,0,.08)">
    <p>自然与社会词汇连接科学观察与公民意识，如 <em>weather, environment, community, job</em>。课标要求围绕语篇主题组织实践活动，把词汇放入<strong>结构化知识网络</strong>，而不是孤立列表。</p>
    <p>学习时建立主题网：天气—季节—活动—衣着；社区—职业—责任。诊断：若混淆 <em>weather/climate</em>，关键在于是否理解“短期现象 vs 长期模式”。</p>
    <p><strong>探究任务：</strong>选择本地一个环境问题，用 8 个相关词汇写英语海报标语，并说明词汇如何支持你的观点。</p>
  </div>
</section>""",
        },
        {
            "after_id": "warmup",
            "html": """
<section class="section" id="vocab-practice-guide" data-tts="vocab-practice-guide" data-bloom-level="analyze" data-scaffold="partial">
  <h2 class="section-title">🧭 主题词汇网络</h2>
  <div class="lesson-panel" style="background:#f8fffe;border-radius:14px;padding:20px;line-height:1.85">
    <p>分类浏览时请标注词汇的<strong>主题字段</strong>（自然/社会）与<strong>词性</strong>，分析一词多义现象，如 <em>bank</em> 在不同语篇中的含义。游戏关卡中的配对题训练快速提取语义特征——错误时回想：是词义不熟还是主题分类混淆。</p>
  </div>
</section>""",
        },
        {
            "after_id": "level3",
            "html": """
<section class="section" id="vocab-theme-network" data-tts="vocab-theme-network" data-bloom-level="analyze" data-scaffold="partial">
  <h2 class="section-title">🌐 自然与社会主题链</h2>
  <div class="lesson-panel" style="background:#fff;border-radius:14px;padding:20px;line-height:1.85">
    <p>把词汇串成主题链：<strong>sun → weather → season → clothes → activity</strong>；<strong>city → job → hospital → volunteer</strong>。配对关卡要求你在图形与英文间建立快速联结——若混淆 <em>river/lake</em>，请用一句话区分：河流流动，湖泊相对静止。迁移：写 5 句描述你所在社区的自然景观与社会设施。</p>
  </div>
</section>""",
        },
    ],
    "eng-e-vocab-600-words": [
        {
            "after_id": "objectives",
            "html": """
<section class="section" id="vocab-curriculum-guide" data-tts="vocab-curriculum-guide" data-bloom-level="understand" data-scaffold="full">
  <h2 class="section-title">📖 课标导读：小学 600 词累积</h2>
  <div class="lesson-panel" style="background:#fff;border-radius:14px;padding:20px;line-height:1.85;box-shadow:0 4px 14px rgba(0,0,0,.08)">
    <p>六年级课标要求能初步运用约 500 个单词就规定主题交流表达，并拓展三级词汇与固定搭配。总复习不是重新死记硬背，而是把词汇放回<strong>主题、语篇与交际任务</strong>中检验自动化程度。</p>
    <p>本课按主题分类复习：家庭校园、日常生活、自然社会等。策略：先快速筛查“见词能读、听词能义”，再用拼写与配对关卡定位薄弱项。诊断提示：拼写错误若集中在同一字母组合，说明要补语音—拼写规则而非盲目抄写。</p>
    <p><strong>迁移设计：</strong>自选一个毕业演讲主题，从 600 词表中选 15 个词写提纲，并论证它们如何支撑你的表达。</p>
  </div>
</section>""",
        },
        {
            "after_id": "warmup",
            "html": """
<section class="section" id="vocab-practice-guide" data-tts="vocab-practice-guide" data-bloom-level="apply" data-scaffold="partial">
  <h2 class="section-title">🧭 总复习闯关说明</h2>
  <div class="lesson-panel" style="background:#f8fffe;border-radius:14px;padding:20px;line-height:1.85">
    <p>四轮关卡分别训练<strong>速度识别、拼写、图文配对、听音选词</strong>，对应课标“听—说—读—写”的不同侧面。Boss 战是综合迁移：要把词汇放入完整句子判断。若连续失误，请回到对应主题词表做针对性分析，而不是随机重玩。</p>
  </div>
</section>""",
        },
        {
            "after_id": "extension",
            "html": """
<section class="section" id="vocab-transfer-task" data-tts="vocab-transfer-task" data-bloom-level="create" data-scaffold="none">
  <h2 class="section-title">🚀 开放迁移：我的词汇成长档案</h2>
  <div class="lesson-panel" style="background:#fffef5;border-radius:14px;padding:20px;line-height:1.85">
    <p>请根据本课得分与错词记录，设计一份<strong>词汇成长档案</strong>：列出 5 个已掌握的 theme words、3 个仍易混淆的词及错因、2 条你将在下周执行的复习策略（如每天听写 10 词、用新词写日记）。这是课标“学习能力”素养的体现。</p>
  </div>
</section>""",
        },
        {
            "after_id": "level4",
            "html": """
<section class="section" id="vocab-review-map" data-tts="vocab-review-map" data-bloom-level="evaluate" data-scaffold="none">
  <h2 class="section-title">🗂️ 600 词主题地图复盘</h2>
  <div class="lesson-panel" style="background:#fff;border-radius:14px;padding:20px;line-height:1.85">
    <p>按课标附录词汇主题复盘：人物与家庭、学校、日常生活、自然、社会与职业。请用表格列出每个主题你<strong>已自动化</strong>的词（见词能读、听词能写）与<strong>待巩固</strong>的词，并写出对应错因（发音、拼写、义混淆、搭配不熟）。毕业前应能在真实交际中调用至少 500 词，而不是只会做选择题。</p>
  </div>
</section>""",
        },
    ],
}

SECTION_ATTRS = {
    "pretest": ('data-tts="pretest" data-bloom-level="remember" data-scaffold="full" data-conceptest="true"'),
    "posttest": ('data-tts="posttest" data-bloom-level="evaluate" data-scaffold="none" data-conceptest="true"'),
    "objectives": ('class="section" data-tts="objectives" data-bloom-level="understand" data-scaffold="full"'),
    "warmup": ('class="section" data-tts="warmup" data-bloom-level="apply" data-scaffold="partial"'),
    "level1": ('class="section" data-tts="level1" data-bloom-level="apply" data-scaffold="partial" data-conceptest="true"'),
    "level2": ('class="section" data-tts="level2" data-bloom-level="apply" data-scaffold="partial"'),
    "level3": ('class="section" data-tts="level3" data-bloom-level="analyze" data-scaffold="partial"'),
    "level4": ('class="section" data-tts="level4" data-bloom-level="analyze" data-scaffold="partial"'),
    "extension": ('class="section" data-tts="extension" data-bloom-level="evaluate" data-scaffold="none"'),
    "knowledge-graph": ('class="section" data-tts="knowledge-graph" data-bloom-level="understand" data-scaffold="full"'),
}


def load_tree_nodes() -> dict[str, dict]:
    data = json.loads(TREE.read_text(encoding="utf-8"))
    out: dict[str, dict] = {}

    def walk(obj):
        if isinstance(obj, dict):
            if obj.get("id") and obj.get("curriculum_points"):
                out[obj["id"]] = obj
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for x in obj:
                walk(x)

    walk(data)
    return out


def patch_html(html: str, course_id: str) -> str:
    html = html.replace('content="eng-e-vocab-600-words">>', 'content="eng-e-vocab-600-words">')
    html = re.sub(r'content="(eng-e-vocab-[^"]+)">>', r'content="\1">', html)
    html = html.replace("知识图谱互动画布占位", "知识图谱互动画布")
    html = html.replace("通过本节课的学习，我们将掌握新知识并能灵活运用",
                        "因此我们要在主题语境中巩固词汇，并能听、认、读、写、用")

    if "teachany-elementary" not in html:
        html = re.sub(r"<body\b", '<body class="teachany-elementary"', html, count=1)
    if "teachany-floating-dock.css" not in html:
        html = html.replace(
            "teachany-tutor-card.css",
            "teachany-tutor-card.css\">\n<link rel=\"stylesheet\" href=\"/assets/scripts/teachany-floating-dock.css",
            1,
        )

    for sid, attrs in SECTION_ATTRS.items():
        pattern = rf'<section\s+id="{sid}"\s+class="section">'
        repl = f'<section id="{sid}" {attrs}>'
        html = html.replace(f'<section id="{sid}" class="section">', repl)
        if sid in ("pretest", "posttest"):
            html = re.sub(
                rf'<section\s+id="{sid}"(?!\s+class="section")',
                f'<section id="{sid}" class="section" {attrs}',
                html,
                count=1,
            )

    for boss_id in ("boss", "report"):
        html = re.sub(
            rf'<section\s+id="{boss_id}"\s*>',
            f'<section id="{boss_id}" class="section" data-tts="{boss_id}" data-bloom-level="apply" data-scaffold="partial">',
            html,
            count=1,
        )

    figures = re.search(
        r"(<section class=\"section course-figures\">.*?</section>)\s*$",
        html,
        flags=re.S,
    )
    if figures:
        block = figures.group(1)
        html = html[: figures.start()] + html[figures.end() :]
        html = html.replace("</body>", block + "\n</body>")

    for panel in PANELS.get(course_id, []):
        marker = f'<section id="{panel["after_id"]}"'
        idx = html.find(marker)
        if idx < 0:
            continue
        end = html.find("</section>", idx)
        if end < 0:
            continue
        insert_at = end + len("</section>")
        if panel["html"].strip() in html:
            continue
        html = html[:insert_at] + "\n" + panel["html"] + html[insert_at:]

    return html


def patch_manifest(manifest: dict, node: dict) -> dict:
    cps = [str(x).strip() for x in (node.get("curriculum_points") or []) if str(x).strip()]
    manifest["curriculum"] = "cn-national"
    manifest["teachany_version"] = "7.18"
    manifest["curriculum_standards"] = [
        {"content": cp, "source": "义务教育英语课程标准（2022年版）"}
        for cp in cps[:6]
    ]
    manifest["grade"] = node.get("grade") or manifest.get("grade")
    return manifest


def sync_kp(course_id: str, node: dict) -> None:
    kp_path = ROOT / "data/kp/english" / f"{course_id}.json"
    if not kp_path.is_file():
        return
    data = json.loads(kp_path.read_text(encoding="utf-8"))
    cps = [str(x).strip() for x in (node.get("curriculum_points") or []) if str(x).strip()]
    cps = [c for c in cps if not c.startswith("- **内容来源")]
    if cps:
        data["curriculum_points"] = cps
        data["excerpts"] = [
            {"id": f"cp-{i+1}", "text": t, "source": "国家课标·内容要求", "type": "curriculum_point"}
            for i, t in enumerate(cps)
        ]
        kp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", action="append", default=[])
    ap.add_argument("--no-audio", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    ids = args.only or COURSE_IDS
    nodes = load_tree_nodes()
    results = []

    for cid in ids:
        d = COMMUNITY / cid
        if not d.is_dir():
            print(f"skip missing {cid}")
            continue
        html_path = d / "index.html"
        manifest_path = d / "manifest.json"
        html = html_path.read_text(encoding="utf-8")
        html2 = patch_html(html, cid)
        node = nodes.get(cid, {})
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest2 = patch_manifest(manifest, node)

        if args.dry_run:
            print(f"[dry-run] {cid}: html {len(html)} -> {len(html2)}")
            continue

        if html2 != html:
            html_path.write_text(html2, encoding="utf-8")
        manifest_path.write_text(json.dumps(manifest2, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        sync_kp(cid, node)

        emit = subprocess.run(
            [sys.executable, str(ROOT / "scripts/batch-emit-knowledge-context.py"), "--node-id", cid],
            capture_output=True,
            text=True,
        )
        fin_cmd = [sys.executable, str(ROOT / "scripts/finalize-courseware.py"), str(d)]
        if args.no_audio:
            fin_cmd.append("--no-audio")
        fin = subprocess.run(fin_cmd, capture_output=True, text=True)
        qual = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate-teaching-quality.py"), str(d)],
            capture_output=True,
            text=True,
        )
        ok = qual.returncode == 0
        results.append((cid, ok, qual.stdout.strip().split("\n")[-3:]))
        print(f"{'✅' if ok else '❌'} {cid}")
        if not ok:
            print(qual.stdout)
        if fin.returncode != 0:
            print(fin.stdout[-500:])

    fails = [r for r in results if not r[1]]
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
