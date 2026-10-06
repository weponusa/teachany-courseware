#!/usr/bin/env python3
"""module-slots.py — 课件模块槽位目录（标准化核心配置）

设计目标（针对抽查反复出现的顺序/重复问题）：
  每个顶层模块在代码层面标定槽位号 data-slot="NN"：
  - hero 永远 00（第一个）
  - knowledge-graph 永远 140（最后一个）
  - 其余模块按教学逻辑递增排列
  - 同一槽位唯一（重复即报错）

槽位约定：十位一组，组内允许缺号（课件按需选用模块）。
识别规则优先级：id 精确匹配 > id 模式 > class > 标题关键词。

被 tag-slots / check-slots / assemble-modules 三个工具共用。
"""
import re

# ---------- 槽位目录 ----------
# (槽位号, 规范名, 唯一性: 'uniq' 每课件至多一个 / 'multi' 可多个)
SLOTS = {
    0:   ("hero",            "uniq"),   # 开场封面 —— 必须第一
    5:   ("course-nav-map",  "uniq"),   # 课程导览图
    10:  ("objectives",      "multi"),  # 学习目标（可多卡）
    15:  ("anchor",          "multi"),  # 带着问题学 / 问题锚点（多问题并列）
    16:  ("why-learn",       "multi"),  # 为什么学 / 背景引入（可多）
    20:  ("pretest",         "uniq"),   # 前测
    25:  ("story",           "multi"),  # 真实情境（可多情境）
    30:  ("module-1",        "uniq"),   # 正文模块一
    35:  ("content",         "multi"),  # 正文内容（老课件学科内容模块）
    40:  ("module-2",        "uniq"),   # 正文模块二
    50:  ("module-3",        "uniq"),   # 正文模块三
    55:  ("module-4",        "uniq"),   # 正文模块四
    60:  ("lesson-focus",    "uniq"),   # 知识精讲（提纲式）
    61:  ("lesson-method",   "uniq"),   # 方法范例
    62:  ("worked-example",  "uniq"),   # 范例
    70:  ("deep-understanding", "uniq"),  # 深层理解 / 五镜头
    75:  ("synthesis",       "uniq"),   # 综合任务
    76:  ("transfer-task",   "uniq"),   # 迁移任务
    77:  ("interactive-lab", "uniq"),   # 互动实验 / 模型
    80:  ("concept-check",   "uniq"),   # 概念检测
    85:  ("exam-practice",   "multi"),  # 真题练习（可多组）
    90:  ("posttest",        "uniq"),   # 后测
    95:  ("error-clinic",    "multi"),  # 易错点诊所（多误区并列）
    97:  ("summary",         "uniq"),   # 小结
    98:  ("memory-anchor",   "uniq"),   # 记忆锚点
    100: ("external-resources", "multi"), # 拓展资源（可多组）
    105: ("video",           "multi"),  # 视频
    110: ("phet-lab",        "uniq"),   # 仿真
    115: ("tiered-practice", "multi"),  # 分层练习 L1/L2/L3
    120: ("audio",           "uniq"),   # 音频
    125: ("ai-media-zone",   "uniq"),   # AI 多模态互动
    130: ("ai-tutor",        "uniq"),   # AI 学伴
    140: ("knowledge-graph", "uniq"),   # 知识图谱 —— 必须最后
}

FIRST_SLOT = 0
LAST_SLOT = 140

# ---------- 识别规则（优先级见 slot_of docstring） ----------

# id 模式（含 module1 无连字符变体）
ID_PATTERN = [
    (re.compile(r'^module-?(\d+)$'), lambda m: min(30 + (int(m.group(1)) - 1) * 10, 55)),
    (re.compile(r'^practice-l(\d+)$'), lambda m: 115),
    (re.compile(r'^level(\d+)$'), lambda m: 115),
    (re.compile(r'^part(\d+)$'), lambda m: min(30 + (int(m.group(1)) - 1) * 10, 55)),
    # 老课件正文变体：sec-xxx / block-xxx / content-xxx 一律正文区
    (re.compile(r'^sec-'), lambda m: 35),
    (re.compile(r'^block-'), lambda m: 35),
    (re.compile(r'^content-'), lambda m: 35),
    (re.compile(r'^chapter-'), lambda m: 35),
]

# 标题关键词（无 id 模块兜底）
TITLE_RULES = [
    (re.compile(r"学习目标|学习任务"), 10),
    (re.compile(r"带着问题|问题引入|问题锚点"), 15),
    (re.compile(r"为什么学"), 16),
    (re.compile(r"前测|课前诊断"), 20),
    (re.compile(r"真实情境|情境任务"), 25),
    (re.compile(r"核心模块 ?1|模块[一1]"), 30),
    (re.compile(r"核心模块 ?2|模块[二2]"), 40),
    (re.compile(r"核心模块 ?3|模块[三3]"), 50),
    (re.compile(r"核心模块 ?4|模块[四4]|图象法"), 55),
    (re.compile(r"知识精讲|核心概念"), 60),
    (re.compile(r"方法范例|方法与范例|^方法[:：]"), 61),
    (re.compile(r"范例"), 62),
    (re.compile(r"深层理解|深度理解|五镜头"), 70),
    (re.compile(r"综合任务|综合实践|综合练习"), 75),
    (re.compile(r"迁移任务|迁移挑战"), 76),
    (re.compile(r"互动实验|探究实验"), 77),
    (re.compile(r"概念检测|随堂测"), 80),
    (re.compile(r"真题练习"), 85),
    (re.compile(r"后测|达标检测"), 90),
    (re.compile(r"易错|常见误区|错因"), 95),
    (re.compile(r"小结|总结"), 97),
    (re.compile(r"记忆锚点|口诀"), 98),
    (re.compile(r"拓展|资源"), 100),
    (re.compile(r"教学动画|动画|视频"), 105),
    (re.compile(r"图文速览|图集"), 35),
    (re.compile(r"仿真|GeoGebra|PhET|网络仿真"), 110),
    (re.compile(r"基础巩固|能力应用|迁移与产出|先过关|含错因"), 115),
    (re.compile(r"知识全景|学习地图"), 5),
    (re.compile(r"知识图谱|知识结构主图"), 140),
]


# 兜底：无 id 但有实质内容的模块 → 正文内容区 35
CONTENT_MIN_LEN = 30

# 占位/挂件：不打标（跟随前驱）。学习进度条等虽字数达标但不是内容模块。
PLACEHOLDER = re.compile(r"学习进度|进度条|成绩面板")


# 高置信 id：标准外壳模块，语义明确，直接定槽（优先于标题识别）
ID_HIGH = {
    "hero-infographic": 0, "hero-cover": 0,
    "course-nav-map": 5,
    "objectives": 10,
    "pretest": 20,
    "posttest": 90,
    "lesson-focus": 60, "lesson-method": 61, "worked-example": 62,
    "deep-understanding": 70,
    "error-clinic": 95, "summary": 97, "memory-anchor": 98,
    "phet-lab": 110, "teachany-audio-player": 120,
    "interactive-lab": 77, "interactive-model": 77, "concept-overview": 5,
    "teachany-ai-tutor-card": 130, "ai-media-zone": 125,
    "knowledge-graph": 140, "teachany-knowledge-graph": 140,
}

# 低置信 id：可能名不副实（如 intro 内容实为「带着问题学」），
# 仅在标题识别失败后才使用
ID_LOW = {
    "hero": 0,
    "intro": 16,
    "target": 10, "goals": 10,
    "anchor": 15, "problem-anchor": 15, "teacher-question": 15,
    "abt-why": 16, "why-learn": 16,
    "story": 25,
    "core-concept": 30,
    "graph-method": 55,
    "synthesis": 75, "task": 75, "comprehensive-task": 75,
    "transfer-task": 76,
    "interactive-lab": 77, "interactive-model": 77, "inquiry": 77,
    "concept-check": 80, "quiz": 80, "misconception": 80,
    "exam-practice": 85, "practice": 85,
    "error-diagnosis": 95, "errors": 95, "error-watch": 95,
    "external-resources": 100, "resources": 100, "further-reading": 100,
    "video": 105, "video-demo": 105, "video-module": 105,
    "external-lab": 110,
    "practice-l1": 115, "practice-l2": 115, "practice-l3": 115,
    "tiered-practice": 115, "level1": 115, "level2": 115, "level3": 115,
    "audio": 120,
    "ai-interaction": 125,
    "ai-tutor": 130, "ai-tutor-section": 130,
}


def slot_of(sid, cls, title, text_len=0, body_text=""):
    """按优先级识别槽位；未识别返回 None。

    优先级：高置信 id > class 特征 > 标题/phase-tag 关键词 > id 模式
    > 低置信 id > 内容兜底。
    """
    # 内容特判（先于 id）：id=posttest 但标题是「真题练习」的补丁块
    # 名不副实——chn-e 系列约 17 个课件，重打标时会被 ID_HIGH 覆盖回 90
    if title and re.search(r'真题练习', title):
        return 85
    if sid and sid in ID_HIGH:
        return ID_HIGH[sid]
    # class 特征：class="hero" 的 section 是开场封面（可能嵌套
    # hero-infographic 于内层，无 id 只有课题名标题，易被兜底误归 35）
    if cls and re.search(r'\bhero\b', cls) and 'hero-infographic-dup' not in sid:
        return 0
    if PLACEHOLDER.search(title or body_text[:60]):
        return None
    # 标题关键词（仅用 h2 标题——曾尝试并入 body 头部文本，
    # 结果正文叙述里的「小结/方法」等词被大量误判为模块类型，
    # R4 违规从 0 涨到 466，已回退）
    if title:
        for pat, slot in TITLE_RULES:
            if pat.search(title):
                return slot
    if sid:
        for pat, fn in ID_PATTERN:
            m = pat.match(sid)
            if m:
                return fn(m)
        if sid in ID_LOW:
            return ID_LOW[sid]
    # 兜底：有实质内容的模块归正文内容区（占位/垃圾不打标）
    if text_len >= CONTENT_MIN_LEN:
        return 35
    return None


def slot_name(slot):
    return SLOTS.get(slot, ("?", "?"))[0]


def is_unique(slot):
    return SLOTS.get(slot, (None, "uniq"))[1] == "uniq"
