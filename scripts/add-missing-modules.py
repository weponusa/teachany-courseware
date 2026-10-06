#!/usr/bin/env python3
"""add-missing-modules.py — 补齐课件缺失的标准模块（本地生成，零外部依赖）

按「先易后难、先大后小」推进，避免一上来就生成需要深度理解的内容：

  1. knowledge-graph  容器由 teachany-knowledge-graph.js 渲染，补齐即生效
  2. objectives       从本课知识点生成具体目标（非「掌握/了解」套话）
  3. pretest          从知识点出诊断题：1 正确项 + 2 典型错误表述
  4. lesson-method    方法要点 + 范例 + 常见误区

共通原则：
  - 课件已有该模块则跳过
  - 内容一律从课件正文提取，绝不写通用套话
  - 插入位置按标准顺序：在既有相邻模块之后，找不到锚点则用兜底

用法: python3 add-missing-modules.py <module> [--dry] [--limit N]
      module ∈ {knowledge-graph, objectives, pretest, lesson-method}
"""
import html as _html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# 复用 gen-figures-local.py 的知识点提取链。
# 该文件名含连字符，无法直接 import，需用 importlib 按路径加载。
import importlib.util as _il  # noqa: E402

_sp = _il.spec_from_file_location(
    "gen_figures_local", Path(__file__).resolve().parent / "gen-figures-local.py")
G = _il.module_from_spec(_sp)
_sp.loader.exec_module(G)

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"


def esc(s):
    return _html.escape(str(s), quote=True)


CONCEPT_HINT = re.compile(r"(概念|结构|功能|类型|特点|特征|方式|阶段|形式|原理|"
                          r"规律|过程|机制|条件|意义|作用|关系|分类|组成|性质)")


def course_title(html, cid):
    """取课程名：截到第一个分隔符，并去掉书名号

    不能写成 <title>([^<·《》]+) —— 标题若以《开头（如「《生物圈》 · 生物…」）
    会被截成空串，导致回退成课件 ID，生成出「能说出 bio-m-biosphere-scope 的…」
    这种病句。
    """
    m = re.search(r"<title>([^<]+)", html)
    if m:
        # 只取主标题：副标题形如「XX：从空间格局到成因机制」，整串用会生成
        # 「关于主要地貌类型：从空间格局到成因机制，下列说法正确的是？」这种病句
        t = re.split(r"[·|｜—\-–—：:》]", m.group(1))[0].strip().strip("《》 　")
        if 2 <= len(t) <= 24:
            return t
    # 兜底：h1
    h1 = re.search(r"<h1[^>]*>([\s\S]*?)</h1>", html)
    if h1:
        t = re.sub(r"<[^>]+>", "", h1.group(1)).strip()
        if 2 <= len(t) <= 24:
            return t
    return cid


# 句子片段的开头词，说明是半句话而非知识点
FRAG_START = re.compile(r"^(已经|即|分布|从|在|把|被|让|使|通过|由于|因此|所以|"
                        r"例如|比如|那么|这样|首先|然后|最后|接着|另外)")


# 人称代词：说明是对话/练习指令，不是知识点
PERSON = re.compile(r"(我|你|他|她|我们|你们|他们|咱)")
# 课件模板的固定措辞，遍布各课件但毫无知识含量，绝不能当知识点。
# 这份清单是**统计得出**的：扫描全库 946 个课件，把出现在 >5% 课件中的
# 提取结果列为套话（手写黑名单是打地鼠，永远补不完）。
JARGON = re.compile(r"^(已有经验|真正卡点|本课任务|学习目标|核心问题|思维实验|"
                    r"探究画板|注意要点|带着问题学|问题锚点|迁移任务|分层任务|"
                    r"知识精讲|方法|范例|总结|小结|课后|课前|课堂|"
                    r"课标锚点|具体案例|前测|易错点辨析|分析方法|即练|避坑提醒|"
                    r"三段式作业|机制解释|And|But|Therefore)")
# 动作序列：讲解步骤（先…再…），不是概念
SEQ = re.compile(r"^(先|再|然后|接着|最后|首先|其次|最终|接下来)")


def usable(p):
    """能否当学习目标的主语

    用「排除噪声」而非「匹配概念词」——后者词表再全也会漏（动脉血、原子序数
    都是合格知识点但不含任何概念后缀），反而误杀好课件。
    """
    if not (3 <= len(p) <= 12):                      # 太短是噪声，太长是整句
        return False
    if re.search(r"[：:，,；;、？?！!]", p):              # 含标点 = 片段
        return False
    if re.search(r"\d", p):                           # 数字（孩子有75 / 1万年前）
        return False
    if re.search(r"[【】\[\]（）()]", p):                 # PBL 模板标记（【And】/【But】）
        return False
    if FRAG_START.match(p) or SEQ.match(p) or JARGON.match(p):
        return False
    if PERSON.search(p):                             # 对话/指令
        return False
    if p.endswith(("的", "了", "和", "与", "或", "等", "着", "过")):
        return False
    return True


def short_label(p, title):
    """去掉与主题重复的前缀：主题「生物圈」+「生物圈的功能」→「功能」"""
    if title and p.startswith(title) and len(p) > len(title) + 1:
        return p[len(title):].lstrip("的 ")
    return p


def pick_concepts(pts, title, n=3):
    """优选「概念类」知识点

    直接用排序首位会挑到「含水」「已经知道：」这类噪声——它们确实出现在正文，
    但不适合当学习目标的主语。
    """
    # 与主题同名不算知识点（会生成「运动与速度中运动与速度…」这种重复句）
    cands = [p for p in pts if usable(p) and p != title]
    prefer = [p for p in cands if CONCEPT_HINT.search(p)]
    rest = [p for p in cands if p not in prefer]
    return (prefer + rest)[:n]          # 返回原文，质量判断与去前缀交给调用方


# ----------------------------------------------------------- knowledge-graph
def kg_block(cid, title):
    """知识图谱容器：内容由 teachany-knowledge-graph.js 渲染"""
    return (f'\n<section data-bloom-level="understand" class="section" id="knowledge-graph" '
            f'style="max-width:1080px;margin:24px auto;padding:0 20px;">'
            f'<h2 class="section-title">🗺️ 知识图谱：{esc(title)}</h2>'
            f'<div data-teachany-kg="{esc(cid)}">'
            f'<canvas class="tkg-fallback-canvas" width="720" height="120" '
            f'aria-label="知识图谱互动画布" style="display:block;width:100%;max-height:140px;'
            f'border-radius:12px;"></canvas></div></section>\n')


# --------------------------------------------------------------- objectives
VERB = {
    "说出": ["说出", "列举"],
    "判断": ["判断", "区分"],
    "分析": ["分析", "说明"],
    "应用": ["运用", "迁移"],
}


def objectives_block(pts, title):
    """从知识点生成具体学习目标（避免「了解/掌握」空话）

    刻意不写「能区分A与B的差异」——A、B 常来自不同维度（如「含水」vs「动脉血」），
    强行对比会产出荒谬句子。改为只做列举 + 应用，安全且仍然具体。
    """
    ks = pick_concepts(pts, title, 3)
    # 质量门槛：需要 2 个以上「可用」知识点（usable 已排除对话、动作序列、
    # 句子片段）。否则宁可留空——把「我出5道关联词填空题」写成学习目标是减分的。
    if len(ks) < 2:
        return ""
    lab = [short_label(k, title) for k in ks]
    items = [f"能说出{title}中{lab[0]}、{lab[1]}的含义与要点",
             f"能运用本课概念分析{title}相关的实际问题"]
    if len(lab) >= 3:
        items.append(f"能结合{lab[2]}说明{title}的判断依据")
    items.append("能借助知识图谱说明前置知识和后续联系")
    lis = "".join(f"<li>{esc(t)}</li>" for t in items)
    return (f'\n<section data-scaffold="full" data-bloom-level="apply" id="objectives" '
            f'class="section" data-tts="objectives" data-tsh="学习目标 - 明确这节课结束时能做到什么">'
            f'<div class="panel"><span class="phase-tag">Learning Objectives</span>'
            f'<h2>学习目标</h2><ul class="grid">{lis}</ul></div></section>\n')


# ------------------------------------------------------------------ pretest
def pretest_block(pts, title):
    """诊断题：正确项取自本课知识点，干扰项用典型错误表述

    干扰项不是乱凑，而是教学上真实的误区类型：
      绝对化（所有…都…）/ 否定关联（…与…无关）/ 范围错位（只发生在…）
    """
    ks = pick_concepts(pts, title, 3)
    if len(ks) < 2:
        return ""
    k1 = ks[0]
    k2 = ks[1]
    lab = [short_label(k, title) for k in ks]
    l3 = lab[2] if len(lab) > 2 else lab[1]
    q = f"关于{title}，下列说法正确的是？"
    right = f"{lab[0]}属于{title}的重要内容"
    wrongs = [
        f"{lab[1]}与{title}完全无关",
        f"所有{title}都必然涉及{l3}，没有例外",
    ]
    opts = [("A", right, True), ("B", wrongs[0], False), ("C", wrongs[1], False)]
    btns = ""
    for letter, text, ok in opts:
        corr = ' data-correct="1"' if ok else ""
        diag = (f' data-diag="{esc(k1)}确属{esc(title)}的内容；'
                f'{esc(wrongs[0])}、{esc(wrongs[1])}都犯了绝对化或否定关联的错误"' if ok else "")
        btns += (f'<button class="quiz-option" data-q="pre" data-a="{letter}"'
                 f'{corr}{diag}>{letter}. {esc(text)}</button>')
    return (f'\n<section class="section text-module" id="pretest" data-bloom-level="remember" '
            f'data-scaffold="full" data-tts="pretest"><div class="panel">'
            f'<span class="phase-tag">Pretest</span>'
            f'<h2>📝 课前诊断：先暴露一个误区</h2><p>{esc(q)}</p>{btns}'
            f'<div class="feedback" id="fb-pre">选择后显示错因诊断。</div></div></section>\n')


# ------------------------------------------------------------- lesson-method
def lesson_method_block(pts, title):
    """方法模块：方法要点 + 范例 + 常见误区"""
    if len(pts) < 2:
        return ""
    joined = "、".join(pts[:4])
    method = (f"按「{pts[0]}→{pts[1]}」的顺序分析：先判断属于哪一类，"
              f"再对应该类的判断依据，最后用{pts[-1] if len(pts)>2 else title}验证结论。")
    example = f"遇到{title}相关情境，先明确{joined}中涉及的是哪一点，再套用对应结论。"
    pitfall = f"常见误区是把{pts[0]}与{pts[1]}混淆，或脱离条件直接套结论。"
    return (f'\n<section class="section core-knowledge-module text-module" id="lesson-method" '
            f'data-bloom-level="apply" data-scaffold="partial" data-tts="lesson-method">'
            f'<div class="card"><span class="phase-tag">方法与范例</span>'
            f'<h2>方法：抓住关键特征</h2><p>{esc(method)}</p>'
            f'<div class="worked-example"><strong>范例：</strong>{esc(example)}</div>'
            f'<p class="bioh-pitfall"><strong>常见误区：</strong>{esc(pitfall)}</p>'
            f'</div></section>\n')


BUILDERS = {
    "knowledge-graph": lambda html, cid, title, pts: kg_block(cid, title),
    "objectives": lambda html, cid, title, pts: objectives_block(pts, title),
    "pretest": lambda html, cid, title, pts: pretest_block(pts, title),
    "lesson-method": lambda html, cid, title, pts: lesson_method_block(pts, title),
}

# 各模块的标准插入位置：优先插到「它前面那个模块」之后
AFTER = {
    "objectives": ["hero-infographic", "abt-why", "problem-anchor"],
    "pretest": ["objectives", "hero-infographic"],
    "lesson-method": ["lesson-focus", "core-concept"],
    "knowledge-graph": ["course-nav-map", "memory-anchor", "posttest", "anchor"],
}


def know_points(html, cid):
    """复用 gen-figures-local 的提取链"""
    secs = G.sections(html)
    pooled = []
    for sid, _ in secs:
        if sid in G.SLOTS:
            pooled += G.bullets(html, sid)
    if len(pooled) < 4:
        for sid, _ in secs[:8]:
            pooled += G.bullets(html, sid)
    if len(pooled) < 4:
        pooled += G.headings(html)
    seen, out = set(), []
    for p in pooled:
        p = G.strip_order(p)
        if p and G.good(p) and p not in seen:
            seen.add(p)
            out.append(p)
    return sorted(out, key=G.quality, reverse=True)[:8]


def insert_after(html, block, anchors):
    """插到第一个存在的锚点模块之后"""
    for sid in anchors:
        m = re.search(rf'<section\b[^>]*\bid="{re.escape(sid)}"[^>]*>', html)
        if m:
            end = html.find("</section>", m.end())
            if end > 0:
                return html[:end + 10] + block + html[end + 10:]
    return None


def process(cid, module, dry=False):
    P = COMMUNITY / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")
    if re.search(rf'<section\b[^>]*\bid="{re.escape(module)}"', html):
        return 0
    pts = know_points(html, cid)
    title = course_title(html, cid)
    block = BUILDERS[module](html, cid, title, pts)
    if not block:
        return 0
    new = insert_after(html, block, AFTER.get(module, []))
    if new is None:
        # 兜底：插到 </body> 前
        m = re.search(r"\s*</body>", html)
        if not m:
            return 0
        new = html[:m.start()] + block + html[m.start():]
    if not dry:
        P.write_text(new, encoding="utf-8")
    return 1


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry" in sys.argv
    limit = next((int(a.split("=")[1]) for a in sys.argv if a.startswith("--limit=")), 0)
    if not args:
        print("用法: python3 add-missing-modules.py <module> [--dry] [--limit N]")
        return 1
    module = args[0]
    if module not in BUILDERS:
        print(f"未知模块 {module}，可选: {', '.join(BUILDERS)}")
        return 1

    cids = [p.name for p in sorted(COMMUNITY.iterdir()) if (p / "index.html").exists()]
    todo = []
    for c in cids:
        try:
            h = (COMMUNITY / c / "index.html").read_text(encoding="utf-8", errors="replace")
            if not re.search(rf'<section\b[^>]*\bid="{re.escape(module)}"', h):
                todo.append(c)
        except Exception:
            pass
    if limit:
        todo = todo[:limit]
    n = 0
    for c in todo:
        try:
            n += process(c, module, dry)
        except Exception as e:
            print(f"  ❌ {c}: {str(e)[:50]}")
    print(f"[{module}] 补齐 {n} 个课件" + ("（--dry 未写入）" if dry else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
