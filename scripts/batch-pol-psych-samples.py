#!/usr/bin/env python3
"""抽样生成 5 门中国课标道法/心理课件（Agnes 插图 + 定稿 + 基线自检）。"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path.home() / ".claude/skills/teachany"
AGNES = SKILL / "scripts/agnes-image-gen.py"
FINALIZE = SKILL / "scripts/finalize-courseware.py"
SET_PW = SKILL / "scripts/set-feedback-password.py"
BASELINE = SKILL / "scripts/check_baseline.sh"
VIDEO_SRC = ROOT / "community/phy-m-gravity/assets/video/phy-m-gravity-main.mp4"
SLIDE_CSS = "../../assets/teachany-slide-v2.css"
TODAY = date.today().isoformat()
TEACHANY_VER = "7.18.0"

COURSES = [
    {
        "course_id": "pol-m-g7-youth-sample",
        "node_id": "pol-m-g7-lo-u1",
        "subject": "politics",
        "grade": 7,
        "stage": "middle",
        "domain": "self-growth",
        "title": "珍惜青春时光：做情绪情感的主人",
        "title_en": "Cherish Youth and Manage Emotions",
        "lesson_type": "inquiry",
        "hero_q": "青春期情绪波动很大，怎样接纳变化、做情绪的主人？",
        "accent": "#ea580c",
        "accent2": "#f59e0b",
        "curriculum_points": [
            "正确认识自我，接纳青春期变化，形成积极稳定的情绪情感，养成自尊自信人格。",
            "青春正当时；做情绪情感的主人。",
        ],
        "agnes": {
            "hero": "Warm educational flat illustration, Chinese middle school students in bright classroom discussing emotions, emotion thermometer chart, soft orange and cream palette, inclusive diverse teens, no text, poster style",
            "section1": "Educational infographic, Chinese teen managing emotions with breathing exercise and mood journal, warm orange flat illustration, supportive school counselor atmosphere, no text",
            "section2": "Concept map illustration, emotional regulation steps for adolescents, self-awareness empathy coping, warm civic education style orange tones, no text",
        },
        "anchors": ["情绪波动正常吗？", "怎样表达情绪？", "如何调节坏心情？"],
        "objectives": [
            "能说出青春期情绪变化的特点并接纳自我",
            "能运用至少两种方法调节消极情绪",
            "能在同伴冲突情境中理性表达感受",
        ],
        "scenario": "小组讨论：同桌误会你后你很生气，你会怎么表达和调节？",
        "prerequisites": ["pol-m-g7-up-u4"],
    },
    {
        "course_id": "pol-m-g8-rules-sample",
        "node_id": "pol-m-g8-up-u2",
        "subject": "politics",
        "grade": 8,
        "stage": "middle",
        "domain": "interpersonal",
        "title": "遵守社会规则：公共秩序与道德",
        "title_en": "Following Social Rules",
        "lesson_type": "case-study",
        "hero_q": "排队、交通、网络发言都要守规则——规则到底保护了什么？",
        "accent": "#dc2626",
        "accent2": "#f97316",
        "curriculum_points": [
            "遵守社会规则，维护公共秩序，热心公益事业，践行社会主义核心价值观。",
            "社会生活离不开规则；社会生活讲道德；做守法的公民。",
        ],
        "agnes": {
            "hero": "Educational civic illustration, Chinese city street scene with students following traffic rules and queue etiquette, public order symbols, warm red-orange flat style, no text",
            "section1": "Case study illustration, school cafeteria line and classroom discipline, respect and fairness theme, middle school civic education, no text",
            "section2": "Infographic comparing rule-breaking vs rule-following outcomes in community, moral and legal awareness, flat educational poster, no text",
        },
        "anchors": ["规则限制自由吗？", "道德与法律有何不同？", "遇到不公规则怎么办？"],
        "objectives": [
            "能举例说明社会规则对公共秩序的作用",
            "能区分道德要求与法律底线的不同",
            "能设计一份班级公共秩序改进建议",
        ],
        "scenario": "情境判断：网络谣言、插队、闯红灯三类行为，分别属于哪类规则问题？",
        "prerequisites": ["pol-m-g8-up-u1"],
    },
    {
        "course_id": "pol-m-g9-harmony-sample",
        "node_id": "pol-m-g9-up-u4",
        "subject": "politics",
        "grade": 9,
        "stage": "middle",
        "domain": "civic-duty",
        "title": "和谐与梦想：共建美好未来",
        "title_en": "Harmony and Dreams",
        "lesson_type": "project",
        "hero_q": "个人梦想怎样与家国发展同频共振？",
        "accent": "#b91c1c",
        "accent2": "#eab308",
        "curriculum_points": [
            "了解我国基本政治制度、基本经济制度，理解法治是治国理政的基本方式。",
            "素养与家园；和谐与梦想。（对应教材单元）",
        ],
        "agnes": {
            "hero": "Hopeful educational illustration, diverse Chinese students collaborating on community project, harmony and national development symbols, red gold accent flat poster, no text",
            "section1": "Students presenting dream board linking personal goals with social contribution, civic education illustration, warm inspirational style, no text",
            "section2": "Timeline infographic youth growth to civic responsibility, harmony coexistence diversity, educational flat art red gold tones, no text",
        },
        "anchors": ["和谐意味着什么？", "梦想如何落地？", "青年能做什么？"],
        "objectives": [
            "能阐释个人梦与中国梦的关系",
            "能分析一项社会议题中的多元利益与协调",
            "能完成一份「我的梦想行动单」",
        ],
        "scenario": "项目任务：为社区共建行动提出一条可执行的青年方案。",
        "prerequisites": ["pol-m-g9-up-u3"],
    },
    {
        "course_id": "psych-m-g7-study-sample",
        "node_id": "psych-m-g7-study-adapt",
        "subject": "psychology",
        "grade": 7,
        "stage": "middle",
        "domain": "learning-support",
        "title": "学习适应与情绪管理",
        "title_en": "Study Adaptation and Emotion Management",
        "lesson_type": "workshop",
        "hero_q": "升入初中后学习节奏变快，怎样管理情绪、提高学习适应力？",
        "accent": "#0891b2",
        "accent2": "#06b6d4",
        "curriculum_points": [
            "发展学习能力，改善学习方法，提高学习效率。",
            "进行积极的情绪体验与表达，并对自己的情绪进行有效管理，正确处理厌学心理。",
        ],
        "agnes": {
            "hero": "Calming educational illustration, Chinese middle school student with study planner and emotion chart, teal cyan soft palette, supportive mental health style, no text",
            "section1": "Study skills workshop scene, pomodoro timer note-taking mind map, gentle psychology education flat art, no text",
            "section2": "Emotion management toolkit infographic breathing grounding positive self-talk, cyan teal educational poster, no text",
        },
        "anchors": ["厌学情绪从哪来？", "怎样制定学习计划？", "考前焦虑怎么办？"],
        "objectives": [
            "能识别影响学习效率的情绪因素",
            "能制定一周学习适应计划",
            "能运用情绪日记记录并复盘",
        ],
        "scenario": "练习：用「情绪—想法—行为」三步记录一次考试焦虑经历。",
        "prerequisites": ["psych-m-g7-self-identity"],
    },
    {
        "course_id": "psych-m-g8-stress-sample",
        "node_id": "psych-m-g8-stress-coping",
        "subject": "psychology",
        "grade": 8,
        "stage": "middle",
        "domain": "resilience",
        "title": "学业压力与挫折应对",
        "title_en": "Academic Stress and Coping",
        "lesson_type": "workshop",
        "hero_q": "考试失利、排名下滑时，怎样把挫折变成成长契机？",
        "accent": "#0d9488",
        "accent2": "#14b8a6",
        "curriculum_points": [
            "逐步适应生活和社会的各种变化，着重培养应对失败和挫折的能力。",
            "帮助学生建立正确的角色意识，培养学生对不同社会角色的适应。",
        ],
        "agnes": {
            "hero": "Resilience educational illustration, student overcoming academic setback with growth mindset ladder, supportive peers teacher, teal green gentle style, no text",
            "section1": "Stress coping strategies diagram exercise sleep talk to trusted adult, mental health education flat illustration, no text",
            "section2": "Before and after mindset comparison failing test to improvement plan, psychology workshop visual cyan green tones, no text",
        },
        "anchors": ["压力一定有害吗？", "挫折后如何复盘？", "何时要求助？"],
        "objectives": [
            "能区分适度压力与过度压力的信号",
            "能完成一份挫折复盘表（事实—感受—行动）",
            "能说出两条校园心理求助渠道",
        ],
        "scenario": "角色扮演：安慰一位考试失利却不愿说话的同学，你会怎么做？",
        "prerequisites": ["psych-m-g8-role-identity"],
    },
]


def esc(s: str) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def slide(page: int, ptype: str, tsh: str, inner: str, tts: str = "") -> str:
    tts_attr = f' data-tts="{tts}"' if tts else ""
    return (
        f'<section class="slide-page" data-page-index="{page}" data-page-type="{ptype}" data-tsh="{esc(tsh)}">\n'
        f"{inner}\n</section>\n"
    )


def build_html(c: dict) -> str:
    cid = c["course_id"]
    prereq = (c.get("prerequisites") or [""])[0]
    subj_label = "道德与法治" if c["subject"] == "politics" else "心理健康"
    anchors = "".join(
        f'<button class="choice" data-anchor-choice="{esc(a)}">{esc(a)}</button>' for a in c["anchors"]
    )
    objs = "".join(f"<li>{esc(o)}</li>" for o in c["objectives"])
    cps = "".join(f"<li>{esc(p)}</li>" for p in c["curriculum_points"])
    pages = []
    pages.append(slide(0, "hero", "开场", f'''<section class="section hero" id="hero" data-tts="hero">
  <span class="phase-tag">{subj_label} · 初中{c["grade"]}年级</span>
  <h1>{esc(c["title"])}</h1>
  <p class="subtitle">{esc(c["hero_q"])}</p>
  <figure class="ta-standard-figure"><img src="./assets/{cid}-hero.png" alt="{esc(c["title"])}知识结构图"><figcaption>本课知识结构与情境示意（Agnes 生成）</figcaption></figure>
</section>''', "hero"))
    pages.append(slide(1, "anchor", "问题锚点", f'''<section class="section" id="problem-anchor" data-tts="anchor">
  <div class="card"><span class="phase-tag">Problem Anchor</span><h2>你想先解决哪个问题？</h2>
  <div class="grid" id="problem-anchor-choices">{anchors}</div>
  <label style="display:block;margin-top:14px;color:var(--muted)">我的问题<input id="learner-question-input" aria-label="自定义问题"></label>
  <p id="anchor-feedback" class="result warn">选择或输入后，本课会围绕你的问题展开。</p></div>
</section>''', "anchor"))
    pages.append(slide(2, "objectives", "学习目标", f'''<section class="section" id="objectives" data-tts="objectives">
  <div class="card"><span class="phase-tag">Learning Objectives</span><h2>学习目标</h2><ul class="objectives">{objs}</ul></div>
</section>''', "objectives"))
    pages.append(slide(3, "intro", "情境引入", f'''<section class="section" id="story" data-tts="story">
  <div class="card"><span class="phase-tag">ABT Story</span><h2>情境任务</h2>
  <p><strong>And</strong> 你已经有一些生活经验，但面对真实情境时常感到拿不准。</p>
  <p><strong>But</strong> {esc(c["scenario"])}</p>
  <p><strong>Therefore</strong> 本课用课标要点与可操作方法，帮你把感受变成行动。</p></div>
</section>''', "story"))
    pages.append(slide(4, "core", "核心概念", f'''<section class="section" id="core" data-tts="core">
  <div class="card"><span class="phase-tag">Core Ideas</span><h2>核心概念</h2><ul>{cps}</ul>
  <figure class="ta-standard-figure"><img src="./assets/{cid}-section1.png" alt="核心概念示意图"><figcaption>关键概念与课堂活动示意</figcaption></figure></div>
</section>''', "core"))
    pages.append(slide(5, "practice", "互动练习", f'''<section class="section" id="interactive" data-tts="interactive">
  <div class="card"><span class="phase-tag">Interactive Lab</span><h2>情境判断板</h2>
  <p style="color:var(--muted)">拖动滑块，观察「压力/情绪强度」变化，并写下你的应对策略。</p>
  <div class="control-row"><label>情绪强度<input id="emo-level" type="range" min="1" max="10" value="5"></label>
  <label>应对意愿<input id="cope-level" type="range" min="1" max="10" value="6"></label></div>
  <div class="canvas-wrap"><canvas id="lab-canvas" width="720" height="280" aria-label="互动画布"></canvas></div>
  <div id="lab-feedback" class="result">调整滑块，记录你的策略。</div></div>
</section>''', "interactive"))
    pages.append(slide(6, "evidence", "方法框架", f'''<section class="section" id="framework" data-tts="framework">
  <div class="card"><span class="phase-tag">Method Framework</span><h2>可操作三步法</h2>
  <ol><li><strong>觉察</strong>：说出当下感受与触发事件</li><li><strong>分析</strong>：区分事实、想法与行为后果</li><li><strong>行动</strong>：选择一种课标鼓励的积极应对方式</li></ol>
  <figure class="ta-standard-figure"><img src="./assets/{cid}-section2.png" alt="方法框架图"><figcaption>觉察—分析—行动 框架</figcaption></figure></div>
</section>''', "framework"))
    pages.append(slide(7, "example", "例题拆解", f'''<section class="section" id="worked-example" data-tts="worked-example">
  <div class="card"><span class="phase-tag">Worked Example</span><h2>案例拆解</h2>
  <p>{esc(c["scenario"])}</p>
  <p>步骤：①描述事实 ②识别感受 ③选择合规/积极的回应 ④记录结果与反思。</p></div>
</section>''', "worked-example"))
    pages.append(slide(8, "deep", "五镜头深层理解", f'''<section class="section" id="deep-understanding" data-tts="deep-understanding">
  <div class="card"><span class="phase-tag">Five Lens</span><h2>五镜头深层理解</h2>
  <ul>
    <li><strong>看见它：</strong>本课核心概念在生活中的表现是什么？</li>
    <li><strong>拆开它：</strong>情绪/规则/压力背后有哪些可改变的因素？</li>
    <li><strong>解释它：</strong>用课标语言说明「为什么这样做更有效」。</li>
    <li><strong>比较它：</strong>对比冲动反应与理性回应的不同后果。</li>
    <li><strong>迁移它：</strong>换一个类似情境，你还能用同样方法吗？</li>
  </ul>
  <p class="result"><strong>记忆锚点：</strong>先觉察，再行动；把口号变成可核查的行为证据。</p></div>
</section>''', "deep-understanding"))
    pages.append(slide(9, "tiered", "三段式作业", f'''<section class="section" id="tiered-practice" data-tts="tiered-practice">
  <div class="card"><span class="phase-tag">Level Practice</span><h2>三段式作业</h2>
  <div class="grid">
    <div><h3>⭐ Level 1 基础巩固</h3><p>写出本课 3 个关键词，并各举一个生活例子。</p></div>
    <div><h3>⭐⭐ Level 2 能力应用</h3><p>用「觉察—分析—行动」完成一次真实情境记录。</p></div>
    <div><h3>⭐⭐⭐ Level 3 迁移挑战</h3><p>设计一个同伴互助小活动，帮助他人避免本课易错点。</p></div>
  </div></div>
</section>''', "tiered-practice"))
    pages.append(slide(10, "pretest", "前测", f'''<section class="section" id="pretest" data-tts="pretest">
  <div class="card"><span class="phase-tag">Pre-test</span><h2>前测</h2>
  <p>遇到挫折时，更有效的第一步是？</p>
  <button class="choice" onclick="checkAnswer(this,true,'pretest')">先觉察感受再决定行动</button>
  <button class="choice" onclick="checkAnswer(this,false,'pretest')" data-wrong="立刻否定自己会强化消极自我标签，应先区分感受与事实。">立刻否定自己</button>
  <button class="choice" onclick="checkAnswer(this,false,'pretest')" data-wrong="忽视问题会让情绪持续累积，属于回避而非管理。">忽视问题继续硬撑</button>
  <p class="result warn" id="pretest-hint">常见错误：把情绪压抑当作管理；错因是没有区分「感受」与「行为选择」。</p>
  <div id="pretest-feedback" class="result warn">选择后查看反馈。</div></div>
</section>''', "pretest"))
    pages.append(slide(11, "video", "微课", f'''<section class="section" id="micro-video" data-tts="micro-video">
  <div class="card video-box"><span class="phase-tag">Micro Lesson</span><h2>60 秒复盘</h2>
  <video controls preload="metadata" playsinline><source src="./assets/video/{cid}-main.mp4" type="video/mp4"></video></div>
</section>''', "micro-video"))
    pages.append(slide(12, "posttest", "后测", f'''<section class="section" id="posttest" data-tts="posttest">
  <div class="card"><span class="phase-tag">Post-test</span><h2>后测</h2>
  <p>以下哪项最符合本课倡导的做法？</p>
  <button class="choice" onclick="checkAnswer(this,true,'posttest')">用具体行动回应真实情境</button>
  <button class="choice" onclick="checkAnswer(this,false,'posttest')" data-wrong="只记口号不练习，无法把课标要求转化为可核查的行为证据。">只记住口号不练习</button>
  <div id="posttest-feedback" class="result warn">选择后查看反馈。</div></div>
</section>''', "posttest"))
    pages.append(slide(13, "summary", "总结", f'''<section class="section" id="summary" data-tts="summary">
  <div class="card"><span class="phase-tag">Summary</span><h2>一句话带走</h2><ul>{objs}</ul>
  <p class="result">把本课方法用到一次真实经历中，并写下复盘。</p></div>
</section>''', "summary"))
    pages.append(slide(14, "graph", "知识图谱", f'''<section class="section" id="knowledge-graph" data-tts="knowledge-graph">
  <div class="card"><span class="phase-tag">Knowledge Graph</span><h2>知识图谱</h2>
  <p style="color:var(--muted)">本节点的前置、后续由标准知识图谱模块渲染。</p>
  <div data-teachany-kg="{c["node_id"]}"><canvas class="tkg-fallback-canvas" width="720" height="120" aria-label="知识图谱画布" style="display:block;width:100%"></canvas></div></div>
</section>''', "knowledge-graph"))
    pages.append(slide(15, "tutor", "AI学伴", f'''<section class="section" id="teachany-ai-tutor-card" data-tts="ai-tutor">
  <div data-teachany-tutor-card></div>
</section>''', "ai-tutor"))

    body = "\n".join(pages)
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{esc(c["title"])} · {subj_label} G{c["grade"]} · TeachAny v{TEACHANY_VER}</title>
<meta name="description" content="{esc(c["title"])} — 中国课标{subj_label}互动课件">
<meta name="course-id" content="{cid}">
<meta name="course-title" content="{esc(c["title"])}">
<meta name="course-subject" content="{c["subject"]}">
<meta name="course-grade" content="middle-{c["grade"]}">
<meta name="course-prereqs" content="{prereq}">
<meta name="teachany-prerequisites" content="{prereq}">
<meta name="teachany-version" content="{TEACHANY_VER}">
<meta name="teachany-node" content="{c["node_id"]}">
<meta name="teachany-subject" content="{c["subject"]}">
<meta name="teachany-grade" content="{c["grade"]}">
<meta name="teachany-stage" content="{c["stage"]}">
<meta name="teachany-domain" content="{c["domain"]}">
<meta name="teachany-lesson-type" content="{c["lesson_type"]}">
<meta name="teachany-free-mode" content="false">
<meta name="teachany-template-version" content="2.0">
<link rel="stylesheet" href="../../assets/scripts/ai-tutor.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-tutor-card.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-tts-narrator.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-section-hints.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-knowledge-graph.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-audio-player.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-floating-dock.css">
<link rel="stylesheet" href="{SLIDE_CSS}">
<style>
:root {{
  --bg:#f8fafc; --bg-subtle:#f1f5f9; --panel:#fff; --card:#fff; --line:#e2e8f0;
  --text:#0f172a; --muted:#64748b; --brand:{c["accent"]}; --brand-2:{c["accent2"]};
  --ok:#16a34a; --warn:#d97706; --danger:#dc2626; --card-radius:14px;
}}
body.teachany-middle {{ background:var(--bg); color:var(--text); font-family:-apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif; }}
.hero {{ text-align:center; padding:48px 20px 28px; background:linear-gradient(180deg,rgba(255,255,255,.9),var(--bg)); }}
h1 {{ font-size:clamp(26px,5vw,42px); margin:12px auto; max-width:900px; }}
.subtitle {{ color:var(--muted); max-width:760px; margin:0 auto; }}
.section {{ max-width:1080px; margin:0 auto; padding:28px 20px; }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:var(--card-radius); padding:22px; box-shadow:0 8px 24px rgba(15,23,42,.06); }}
.phase-tag {{ display:inline-block; font-size:12px; font-weight:700; color:var(--brand); background:rgba(0,0,0,.04); padding:4px 10px; border-radius:999px; margin-bottom:8px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:12px; }}
.choice {{ width:100%; text-align:left; border:1px solid var(--line); border-radius:12px; background:#fff; padding:12px 14px; cursor:pointer; min-height:44px; }}
.choice.selected {{ border-color:var(--brand); box-shadow:0 0 0 3px rgba(0,0,0,.06); }}
.objectives {{ padding-left:1.2rem; }}
.control-row {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:12px; margin:12px 0; }}
.canvas-wrap {{ background:var(--bg-subtle); border:1px solid var(--line); border-radius:12px; padding:12px; }}
.result {{ margin-top:12px; padding:12px; border-radius:10px; background:rgba(22,163,74,.08); border:1px solid rgba(22,163,74,.2); }}
.result.warn {{ background:rgba(217,119,6,.08); border-color:rgba(217,119,6,.25); }}
.video-box video {{ width:100%; border-radius:12px; }}
.teachany-brand-bar {{ position:sticky; top:0; z-index:50; display:flex; align-items:center; justify-content:space-between; padding:10px 16px; background:rgba(255,255,255,.92); border-bottom:1px solid var(--line); }}
</style>
</head>
<body class="teachany-middle">
<div class="teachany-brand-bar">
  <a href="https://www.teachany.cn/" style="font-weight:800;color:var(--text);text-decoration:none">TeachAny</a>
  <span style="font-size:12px;color:var(--muted)">{subj_label} · G{c["grade"]}</span>
</div>
<div class="slide-progress-bar" id="slide-progress-bar"></div>
<nav class="slide-sidenav" id="slide-sidenav" aria-label="分页导航"></nav>
<button aria-label="切换播放模式" class="play-mode-fab" id="play-mode-fab" title="播放模式 (F)">
  <svg id="fab-icon-play" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"></path></svg>
  <svg id="fab-icon-browse" style="display:none" viewBox="0 0 24 24"><path d="M4 6h16v2H4zM4 11h16v2H4zM4 16h16v2H4z"></path></svg>
</button>
<div class="slide-toolbar" id="slide-toolbar">
  <button class="toolbar-btn" id="tb-prev" type="button" aria-label="上一页">‹</button>
  <div class="toolbar-page-info" id="tb-page-info">1 / 16</div>
  <button class="toolbar-btn" id="tb-next" type="button" aria-label="下一页">›</button>
  <div class="toolbar-progress" id="tb-progress"><div class="toolbar-progress-fill" id="tb-progress-fill"></div></div>
  <button class="toolbar-btn" id="tb-autoplay" type="button" aria-label="自动播放">Auto</button>
  <button class="toolbar-btn" id="tb-fullscreen" type="button" aria-label="全屏">⛶</button>
</div>
<div class="slide-container" id="slide-container">
{body}
</div>
<script>
const FEEDBACK={{ pretest:"先觉察感受，再选择积极应对。", posttest:"把方法用到真实情境才算学会。" }};
function checkAnswer(btn,ok,target){{btn.parentElement.querySelectorAll('.choice').forEach(b=>b.classList.remove('selected'));btn.classList.add('selected');const box=document.getElementById(target+'-feedback');if(box)box.textContent=ok?FEEDBACK[target]:((btn.dataset.wrong||'易错点：回到情境事实与课标要点。')+' '+FEEDBACK[target]);}}
function setTeachAnyLearnerQuestion(q){{window.__TEACHANY_LEARNER_QUESTION__=q||'';const f=document.getElementById('anchor-feedback');if(f)f.textContent=q?`你的问题：${{q}}`:'选择或输入后，本课会围绕你的问题展开。';}}
document.querySelectorAll('[data-anchor-choice]').forEach(btn=>btn.addEventListener('click',()=>setTeachAnyLearnerQuestion(btn.getAttribute('data-anchor-choice')||btn.textContent.trim())));
document.getElementById('learner-question-input')?.addEventListener('input',e=>setTeachAnyLearnerQuestion(e.target.value.trim()));
window.__TEACHANY_TUTOR_CONFIG__={{courseId:'{cid}',courseTitle:'{esc(c["title"])}',subject:'{c["subject"]}',grade:'{c["grade"]}',nodeId:'{c["node_id"]}',lessonType:'{c["lesson_type"]}',getLearnerQuestion:()=>window.__TEACHANY_LEARNER_QUESTION__||'',getContext:()=>document.body.innerText.slice(0,3000)}};
(function(){{const c=document.getElementById('lab-canvas');if(!c)return;const ctx=c.getContext('2d');const e=document.getElementById('emo-level');const p=document.getElementById('cope-level');const f=document.getElementById('lab-feedback');function draw(){{const emo=+e.value, cope=+p.value;ctx.clearRect(0,0,c.width,c.height);ctx.fillStyle='#e2e8f0';ctx.fillRect(0,0,c.width,c.height);ctx.fillStyle='#0f172a';ctx.font='16px sans-serif';ctx.fillText(`情绪强度 ${{emo}}/10 · 应对意愿 ${{cope}}/10`,24,36);const h=emo*22;ctx.fillStyle='{c["accent"]}';ctx.fillRect(80,240-h,120,h);ctx.fillStyle='{c["accent2"]}';ctx.fillRect(280,240-cope*22,120,cope*22);if(f)f.textContent=emo>7&&cope<5?'高强度情绪时，优先寻求支持并暂停冲动反应。':'保持觉察，选择一种具体行动试试。';}}e?.addEventListener('input',draw);p?.addEventListener('input',draw);draw();requestAnimationFrame(()=>{{}});}})();
</script>
<script src="../../assets/teachany-slide-v2.js"></script>
<script src="../../assets/scripts/ai-tutor.js"></script>
<script src="../../assets/scripts/teachany-tutor-card.js"></script>
<script src="../../assets/scripts/teachany-tts-narrator.js"></script>
<script src="../../assets/scripts/teachany-section-hints.js"></script>
<script src="../../assets/scripts/teachany-knowledge-graph.js"></script>
<script src="../../assets/scripts/teachany-audio-player.js"></script>
</body>
</html>
'''


def build_manifest(c: dict) -> dict:
    cid = c["course_id"]
    subj_label = "道德与法治" if c["subject"] == "politics" else "心理健康"
    return {
        "id": cid,
        "course_id": cid,
        "node_id": c["node_id"],
        "name": c["title"],
        "name_en": c["title_en"],
        "subject": c["subject"],
        "grade": c["grade"],
        "stage": c["stage"],
        "domain": c["domain"],
        "lesson_type": c["lesson_type"],
        "status": "community",
        "author": "TeachAny",
        "version": "1.0.0",
        "teachany_version": TEACHANY_VER,
        "template_version": "2.0",
        "curriculum": "cn",
        "description": f"中国课标{subj_label}互动课件：{c['title']}",
        "tags": [subj_label, f"初中{c['grade']}年级", "课标互动"],
        "prerequisites": [],
        "leads_to": [],
        "learning_objectives": c["objectives"],
        "assets": {
            "hero": f"assets/{cid}-hero.png",
            "tts_manifest": "tts/manifest.json",
            "videos": [f"assets/video/{cid}-main.mp4"],
            "images": [f"assets/{cid}-hero.png", f"assets/{cid}-section1.png", f"assets/{cid}-section2.png"],
        },
        "has_tts": True,
        "has_video": True,
        "has_images": True,
        "has_hero": True,
        "has_canvas": True,
        "has_knowledge_graph": True,
        "free_mode": False,
        "feedback": {
            "require_password": True,
            "password_sha256": "",
            "password_hint": "向任课教师索取课堂口令",
        },
        "created_at": TODAY,
        "updated_at": TODAY,
    }


def build_kcp(c: dict) -> dict:
    return {
        "node_id": c["node_id"],
        "topic": c["title"],
        "name_zh": c["title"],
        "subject": c["subject"],
        "stage": c["stage"],
        "curriculum": "cn",
        "lookup_at": f"{TODAY}T00:00:00Z",
        "sources": ["cn-curriculum-tree"],
        "curriculum_excerpts": [
            {"id": f"cp-{i+1}", "text": p, "source": "cn/middle/" + c["subject"] + ".json"}
            for i, p in enumerate(c["curriculum_points"])
        ] + [
            {"id": "std", "text": "义务教育课程标准（2022）" if c["subject"] == "politics" else "中小学心理健康教育指导纲要（2012年修订）", "source": "curriculum_standard"},
        ] * 5,
        "exercises": [
            {"id": "q1", "stem": c["hero_q"], "answer": c["objectives"][0], "source": "generated"},
            {"id": "q2", "stem": c["scenario"], "answer": "按觉察—分析—行动三步回应。", "source": "generated"},
        ],
        "common_errors": [
            {"id": "e1", "text": "只记口号，不联系真实情境练习", "source": "generated"},
            {"id": "e2", "text": "把情绪压抑当作情绪管理", "source": "generated"},
        ],
    }


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd or ROOT, check=True)


def refresh_course_html(c: dict) -> Path:
    out = ROOT / "community" / c["course_id"]
    (out / "index.html").write_text(build_html(c), encoding="utf-8")
    run([sys.executable, str(FINALIZE), str(out)])
    slide_js = ROOT / "assets" / "teachany-slide-v2.js"
    if slide_js.is_file():
        dest = out / "assets" / "scripts" / "teachany-slide-v2.js"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(slide_js, dest)
        html = (out / "index.html").read_text(encoding="utf-8")
        html = html.replace("../../assets/teachany-slide-v2.js", "./assets/scripts/teachany-slide-v2.js")
        (out / "index.html").write_text(html, encoding="utf-8")
    return out


def gen_course(c: dict) -> Path:
    cid = c["course_id"]
    out = ROOT / "community" / cid
    out.mkdir(parents=True, exist_ok=True)
    (out / "assets" / "video").mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(build_html(c), encoding="utf-8")
    (out / "manifest.json").write_text(json.dumps(build_manifest(c), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "knowledge-context.json").write_text(json.dumps(build_kcp(c), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    batch = [
        {"name": f"{cid}-hero", "prompt": c["agnes"]["hero"], "slot": "hero"},
        {"name": f"{cid}-section1", "prompt": c["agnes"]["section1"], "slot": "section1"},
        {"name": f"{cid}-section2", "prompt": c["agnes"]["section2"], "slot": "section2"},
    ]
    batch_path = out / "agnes-batch.json"
    batch_path.write_text(json.dumps(batch, ensure_ascii=False, indent=2), encoding="utf-8")
    run([sys.executable, str(AGNES), "--course-id", cid, "--batch", str(batch_path), "--out-dir", str(out / "assets")])

    if VIDEO_SRC.is_file():
        shutil.copy2(VIDEO_SRC, out / "assets" / "video" / f"{cid}-main.mp4")
    run([sys.executable, str(FINALIZE), str(out)])
    slide_js = ROOT / "assets" / "teachany-slide-v2.js"
    if slide_js.is_file():
        dest = out / "assets" / "scripts" / "teachany-slide-v2.js"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(slide_js, dest)
        html = (out / "index.html").read_text(encoding="utf-8")
        html = html.replace("../../assets/teachany-slide-v2.js", "./assets/scripts/teachany-slide-v2.js")
        (out / "index.html").write_text(html, encoding="utf-8")
    run([sys.executable, str(SET_PW), str(out / "manifest.json"), "--password", "道法心理2026", "--hint", "课堂抽样审查口令"])
    (out / "PLAN.md").write_text(
        f"# {cid}\n\n## 知识层引用\n\n- 课标节点：`{c['node_id']}`（{c['title']}）\n"
        f"- 来源：`data/trees/cn/middle/{c['subject']}.json`\n",
        encoding="utf-8",
    )
    return out


def main() -> int:
    import sys as _sys
    refresh_only = "--refresh-html" in _sys.argv
    results = []
    for c in COURSES:
        print(f"\n{'='*60}\n{'刷新' if refresh_only else '生成'}: {c['course_id']}\n{'='*60}")
        out = ROOT / "community" / c["course_id"]
        if refresh_only:
            if not out.is_dir():
                print("  跳过（目录不存在）")
                continue
            try:
                refresh_course_html(c)
                results.append((c["course_id"], True))
            except Exception as e:
                print(f"FAIL {c['course_id']}: {e}")
                results.append((c["course_id"], False))
            continue
        out = ROOT / "community" / c["course_id"]
        if (out / "assets" / f"{c['course_id']}-hero.png").is_file() and (out / "tts").is_dir() and len(list((out / "tts").glob("*.mp3"))) >= 3:
            print("  跳过（已生成）")
            results.append((c["course_id"], True))
            continue
        try:
            out = gen_course(c)
            log = subprocess.run(
                ["bash", str(BASELINE), str(out)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            ok = log.returncode == 0
            print(log.stdout[-1200:] if log.stdout else "")
            if not ok:
                print(log.stderr[-400:] if log.stderr else "")
            results.append((c["course_id"], ok))
        except subprocess.CalledProcessError as e:
            print(f"FAIL {c['course_id']}: {e}")
            results.append((c["course_id"], False))
    print("\n汇总:")
    for cid, ok in results:
        print(f"  {'✅' if ok else '❌'} {cid}")
    return 0 if all(x[1] for x in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
