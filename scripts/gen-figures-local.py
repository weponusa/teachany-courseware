#!/usr/bin/env python3
"""gen-figures-local.py — 本地生成教学示意图（零外部模型 / 零成本 / 可复现）

从课件正文提取真实知识点，套用 fig-templates 的模板生成 SVG。
与 add-figures.py 的区别：那个调外部 LLM，这个全部本地生成。

流程：
  1. 提取：从 lesson-focus / core-concept / 各正文 section 抽取结构化知识点
  2. 选题：按课件正文的语义特征挑选模板（循环/层次/对比/组成/阶梯）
  3. 生成：填充模板 → 内联 SVG（含 SMIL 动画）→ 插回对应 section 之后

用法: python3 gen-figures-local.py <cid> [cid2 ...]
      python3 gen-figures-local.py --all            处理全库缺图课件
      python3 gen-figures-local.py --dry <cid>      只打印不写入
      python3 gen-figures-local.py --limit N        每课件最多几张（默认2）
"""
import html as _html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fig_templates as FT  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

# 插图落位 & 取知识点：优先这些 section（按优先级）
# 不同批次课件用的 id 不统一（learn / intro / lesson-focus / core-concept…），
# 这里尽量覆盖各类正文区块，避免漏掉真正有内容的段落。
SLOTS = ["lesson-focus", "core-concept", "learn", "lesson-method", "knowledge",
         "concept", "deep-understanding", "worked-example", "intro", "summary"]

# 模板选题的语义线索
HINT = {
    "cycle": ["循环", "周期", "往复", "冲程", "轮回", "闭环", "再生", "反馈",
              "过程", "流程", "阶段"],
    "compare": ["区别", "对比", "异同", "辨析", "比较", " versus ", "不同",
                "容易混淆", "易错"],
    "composition": ["结构", "组成", "构成", "成分", "部件", "器官", "系统",
                    "要素", "层次"],
    "hierarchy": ["分类", "类型", "体系", "种类", "分支", "框架", "脉络"],
    "steps": ["步骤", "方法", "流程", "顺序", "解题", "策略", "技巧", "路径"],
}

# 正文噪声：这些区块的内容不用于作图
SKIP_SEC = re.compile(
    r'id="(?:course-nav-map|knowledge-graph|teachany-ai-tutor-card|anchor|'
    r'memory-anchor|error-clinic|posttest|pretest|video-demo)"', re.I)

EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u2190-\u21FF\u2700-\u27bf]")


def clean(s):
    """去标签、去 emoji、压空白"""
    s = re.sub(r"<[^>]+>", " ", s)
    s = _html.unescape(s)
    s = EMOJI.sub("", s)
    s = re.sub(r"[\s\u3000]+", " ", s)
    return s.strip(" ·|—-:;,。、，")


def sections(html):
    """拆出 (id, 纯文本) 列表，跳过噪声区块"""
    out = []
    for m in re.finditer(r'<section\b([^>]*)>([\s\S]*?)</section>', html):
        attrs, body = m.group(1), m.group(2)
        if SKIP_SEC.search(attrs):
            continue
        sid = (re.search(r'id="([^"]+)"', attrs) or [None, ""])[1]
        txt = clean(body)
        if len(txt) >= 20:
            out.append((sid, txt))
    return out


NOISE = re.compile(r"(它|这|那)(的)?$|^(拆开|解释|比较|看见|迁移|记住|了解|掌握|说出|判断)"
                   r"|^[\d\.\s、，,：:；;]+$|^第?[一二三四五六七八九十][\.、]?$")

CN = r"[\u4e00-\u9fa5A-Za-z0-9]"
# 顿号/逗号并列的短短语（≥3 连）：如「扦插、嫁接、压条、分株、孢子繁殖」
SERIES = re.compile(rf"({CN}{{2,10}})(?:[、，,]({CN}{{2,10}})){{2,}}")
# 序号分点：一、xxx  1. xxx
ORDERED = re.compile(r"[一二三四五六七八九十\d]{1,2}[、.．]\s*"
                     rf"({CN}{{2,14}})")


def good(t):
    """过滤噪声短语：只保留能当图节点标签的短名词性短语"""
    t = t.strip()
    # 图节点标签应该短；过长说明是整句，不是知识点
    if not (2 <= len(t) <= 14):
        return False
    if NOISE.search(t):
        return False
    # 问句 / 疑问词 —— 是引导语，不是知识点
    if "?" in t or "？" in t:
        return False
    if any(w in t for w in ("什么", "如何", "为什么", "怎样", "哪些", "是否", "能不能")):
        return False
    # 语法碎片
    if t.startswith(("的", "了", "是", "和", "与", "在", "把", "被", "让", "使")):
        return False
    if t.endswith(("它", "这", "那", "吗", "呢", "的", "了")):
        return False
    # 纯数字/字母
    if re.fullmatch(r"[\dA-Za-z\s\.\-]+", t):
        return False
    return True


def from_text(txt):
    """从纯文本里挖知识点：并列短语 > 序号分点"""
    pts = []
    for m in SERIES.finditer(txt):
        seg = m.group(0)
        parts = [p for p in re.split(r"[、，,]", seg) if good(p)]
        if len(parts) >= 3:
            pts += parts
    for m in ORDERED.finditer(txt):
        t = m.group(1).strip()
        if good(t):
            pts.append(t)
    return pts


# 功能性标题（导航/练习区块），不能当知识点
FUNC_TITLE = re.compile(
    r"课前诊断|学习目标|真题练习|达标检测|互动练习|概念检测|微课讲解|教师追问|"
    r"分层任务|迁移任务|记忆锚点|易错点|课程导览|知识图谱|拓展资源|常见问题|"
    r"小结|总结|想一想|练一练|思考题|课后作业|"
    r"课标导入|问题锚点|错因诊断|选择题|填空题|解答题|判断题|材料分析|"
    r"我的假设|我的证据|我的结论|探究记录|观察记录|外部互动")


def headings(html):
    """提取正文小标题作为知识点

    不少课件的正文 section 没有 id（无法靠 SLOTS 命中），但 h2/h3 标题
    本身就是现成且准确的知识点，如「有丝分裂的四个阶段」「无丝分裂的特殊形式」。
    """
    out = []
    for m in re.finditer(r"<h([23])\b[^>]*>([\s\S]*?)</h\1>", html):
        t = clean(m.group(2))
        if not good(t):
            continue
        if FUNC_TITLE.search(t):
            continue
        out.append(t)
    return out


def bullets(html, sid):
    """取指定 section 内的知识点候选：结构化标签优先，纯文本并列兜底"""
    m = re.search(rf'<section\b[^>]*\bid="{re.escape(sid)}"[^>]*>([\s\S]*?)</section>', html)
    if not m:
        return []
    body = m.group(1)
    items = []
    # 1) 列表项
    for lm in re.finditer(r"<li\b[^>]*>([\s\S]*?)</li>", body):
        t = clean(lm.group(1))
        if good(t) and len(t) <= 60:
            items.append(t)
    # 2) 小标题
    for hm in re.finditer(r"<h[34]\b[^>]*>([\s\S]*?)</h[34]>", body):
        t = clean(hm.group(1))
        if good(t):
            items.append(t)
    # 3) 加粗短语
    for sm in re.finditer(r"<strong\b[^>]*>([\s\S]*?)</strong>", body):
        t = clean(sm.group(1))
        if good(t):
            items.append(t)
    # 4) 纯文本里的并列/序号知识点（很多课件正文没有 li，只有段落）
    items += from_text(clean(body))

    # 去重保序
    seen, out = set(), []
    for t in items:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


def quality(p):
    """知识点质量分：短、完整、名词性的优先

    排序很关键——提取结果里混杂了句子片段（"理解各方式的原理和应"）与
    序号前缀（"一、无性生殖的概念"），直接按顺序取会把垃圾放进图里。
    """
    s, L = 0, len(p)
    if 2 <= L <= 6:
        s += 5
    elif L <= 9:
        s += 3
    elif L <= 14:
        s += 0
    else:
        s -= 4
    if re.match(r"^[一二三四五六七八九十\d]+[、.．]", p):
        s -= 5                                   # 序号前缀
    if p.endswith(("等", "和", "与", "或", "及", "中的", "上", "下", "中")):
        s -= 4                                   # 断尾/悬空
    if re.search(r"[，,；;]", p):
        s -= 3                                   # 句子片段
    if p.startswith(("一、", "二、", "三、", "四、", "五、")):
        s -= 5
    if re.search(r"(的|了|是|在|把|被)", p) and L > 8:
        s -= 1
    return s


def strip_order(p):
    """去掉序号前缀：一、xxx / 1. xxx → xxx"""
    return re.sub(r"^[一二三四五六七八九十\d]{1,2}[、.．]\s*", "", p).strip()


def split_label(item, max_label=6):
    """把一条知识点拆成 (短标签, 说明)"""
    t = item.strip()
    for sep in ("：", ":", "——", "--", "－", "、"):
        if sep in t and 2 <= len(t.split(sep)[0]) <= max_label + 2:
            a, b = t.split(sep, 1)
            return a.strip(), b.strip() or a.strip()
    if len(t) > max_label + 4:
        # 无分隔符时按长度切：前段做标签，整句做说明
        cut = min(len(t), max_label + 3)
        return t[:cut], t
    return t, t


def choose_template(html, secs):
    """按正文语义线索选模板"""
    blob = " ".join(t for _, t in secs)[:4000].lower()
    score = {k: sum(blob.count(w) for w in ws) for k, ws in HINT.items()}
    best = max(score, key=lambda k: score[k])
    return best if score[best] > 0 else "steps"


def build(cid, html, limit=2):
    """生成该课件的示意图列表 [(figcaption, svg)]"""
    secs = sections(html)
    if not secs:
        return []
    title_m = re.search(r"<title>([^<·《》]+)", html)
    title = (title_m.group(1).strip() if title_m else cid)[:24]

    # 收集知识点：结构化内容 → 正文小标题 → 段落首句（逐级兜底）
    pooled = []
    for sid, _ in secs:
        if sid in SLOTS:
            pooled += bullets(html, sid)
    if len(pooled) < 4:
        for sid, _ in secs[:8]:
            pooled += bullets(html, sid)
    if len(pooled) < 4:
        pooled += headings(html)
    if len(pooled) < 3:
        # 最后兜底：段落首句，取标点前的短主干
        for _, txt in secs[:6]:
            for sent in re.split(r"[。；;]", txt):
                s = sent.strip()
                for cut in re.split(r"[，,：:]", s):
                    if 4 <= len(cut.strip()) <= 14 and good(cut.strip()):
                        pooled.append(cut.strip())
                        break
    # 去重保序（顺带清洗序号前缀）
    seen, out = set(), []
    for p in pooled:
        p = strip_order(p)
        if p and good(p) and p not in seen and not re.match(r"^[\d\.\s]+$", p):
            seen.add(p)
            out.append(p)
    # 质量排序：短、名词性、无序号前缀的优先，保证两张图都用到最好的知识点
    pooled = sorted(out, key=quality, reverse=True)[:10]
    if len(pooled) < 3:
        return []

    tpl = choose_template(html, secs)
    pairs = [split_label(p) for p in pooled]
    figs = []

    if tpl == "cycle":
        n = min(max(3, len(pairs)), 6)
        figs.append((f"{title}：循环过程示意",
                     FT.cycle(pairs[:n], title=title)))
    elif tpl == "hierarchy":
        groups, per = [], max(1, len(pairs) // 3)
        for i in range(0, min(len(pairs), 9), per + 1):
            head, desc = pairs[i]
            subs = [p[0] for p in pairs[i + 1:i + 1 + per]]
            groups.append((head, subs or [desc]))
        figs.append((f"{title}：知识结构体系",
                     FT.hierarchy(title, groups[:4], subtitle="按分支展开")))
    elif tpl == "compare":
        mid = len(pairs) // 2
        figs.append((f"{title}：对比辨析",
                     FT.compare([p[0] for p in pairs[:mid]] or ["—"],
                                [p[0] for p in pairs[mid:]] or ["—"],
                                "方面一", "方面二", subtitle="左右对照看差异")))
    elif tpl == "composition":
        center = pairs[0][0] if pairs else title
        figs.append((f"{title}：组成结构",
                     FT.composition(center, pairs[1:7], subtitle="主要组成部分")))
    else:
        figs.append((f"{title}：方法步骤",
                     FT.steps(pairs[:5], subtitle="按顺序推进")))

    # 第二张：用另一种视角补充（阶梯图通用性强，作为补充）
    if limit >= 2 and len(pairs) >= 4:
        alt = "steps" if tpl != "steps" else "cycle"
        if alt == "cycle" and len(pairs) >= 3:
            figs.append((f"{title}：关键环节闭环",
                         FT.cycle(pairs[:min(6, len(pairs))], title=title)))
        else:
            # 用排序后的前排知识点，避免把句子片段排进图里
            figs.append((f"{title}：要点梳理",
                         FT.steps(pairs[:5], subtitle="核心要点")))
    return figs[:limit]


def process(cid, dry=False, limit=2, min_figs=2):
    P = COMMUNITY / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")
    if len(re.findall(r'<figure class="ta-standard-figure"', html)) >= min_figs:
        return 0
    figs = build(cid, html, limit)
    if not figs:
        return 0

    # 落位：优先插到 SLOTS 中存在的 section 之后
    added = 0
    for idx, (cap, svg) in enumerate(figs):
        target = None
        for sid in SLOTS:
            m = re.search(rf'<section\b[^>]*\bid="{re.escape(sid)}"[^>]*>', html)
            if m:
                end = html.find("</section>", m.end())
                if end > 0:
                    target = end + len("</section>")
                    break
        if target is None:
            # 兜底1：第一个 class="section" 的区块之后
            for m in re.finditer(r'<section\b[^>]*class="section[^"]*"[^>]*>', html):
                end = html.find("</section>", m.end())
                if end > 0:
                    target = end + len("</section>")
                    break
        if target is None:
            # 兜底2：主容器内的首个位置
            m = re.search(r'<div\b[^>]*class="slide-container"[^>]*>', html)
            if m:
                target = m.end()
        if target is None:
            # 兜底3：body 结束前
            m = re.search(r"\s*</body>", html)
            if m:
                target = m.start()
        if target is None:
            break
        block = (f'\n<figure class="ta-standard-figure"><figcaption>{cap}</figcaption>'
                 f'{svg}</figure>\n')
        html = html[:target] + block + html[target:]
        added += 1
    if added and not dry:
        P.write_text(html, encoding="utf-8")
    return added


def main():
    dry = "--dry" in sys.argv
    limit = 2
    for a in sys.argv[1:]:
        if a.startswith("--limit="):
            limit = int(a.split("=", 1)[1])
    cids = [a for a in sys.argv[1:] if not a.startswith("--")]

    if "--all" in sys.argv or not cids:
        cids = []
        for p in sorted(COMMUNITY.iterdir()):
            f = p / "index.html"
            if not f.exists():
                continue
            h = f.read_text(encoding="utf-8", errors="replace")
            if len(re.findall(r'<figure class="ta-standard-figure"', h)) < 2:
                cids.append(p.name)

    tot = 0
    for c in cids:
        try:
            n = process(c, dry, limit)
            tot += n
            if n:
                print(f"  {c}: +{n}")
        except Exception as e:
            print(f"  ❌ {c}: {str(e)[:60]}")
    print(f"\n共新增 {tot} 张（处理 {len(cids)} 个课件）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
