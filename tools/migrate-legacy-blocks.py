#!/usr/bin/env python3
"""把「旧版双层结构」课件重建为规范 16 页（v2）。

背景（实测结构）
----------------
这些课件是**两层**结构：
  外层 6 个左右 `<section class="slide-page">`，
  里面嵌着十几块 `<section class="section ..." id="X">`（hero-infographic /
  objectives / anchor / pretest / lesson-focus / lesson-method / module-1 /
  deep-understanding / ai-media-zone / posttest / error-clinic / memory-anchor /
  knowledge-graph），末尾还有几块散落在外的同名块。

外层页里往往只有标题，**真正的内容都在子块里**，所以必须把两层展平成 16 页。

⚠️ 两个踩过的坑（改这个脚本前务必看）
  1. 用非贪婪正则抽 `<section>…</section>` 会因**嵌套**提前截断 —— 实测丢掉
     80 个真实文本块（168 → 101）。必须用标签配平（见 section_spans）。
  2. 只取"顶层"section 会漏掉 9 块（它们嵌在外层 slide-page 里）。

内容策略
--------
每个内容块**只用一次**（靠 id 去重）。本课没有的页从它自己的前测/后测/易错点
重组，不新编知识。**写入前必须开 --verify**（保留率 < 98% 就拒绝写入）。
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

AI_TUTOR_HTML = (
    '<h2>AI 学伴 · 随时提问</h2>\n'
    '<p>把还没弄明白的地方写下来问 AI 学伴。它会先帮你找到卡住的地方，'
    '再给你一个小小的提示，让你自己往前走一步。</p>\n'
    '<div data-teachany-tutor-card></div>')

SPEC = [
    # (页型, 导航提示, [候选源...]) —— 一页可给多个候选 id，**按顺序取第一个未用的**。
    # 不同学科的内容块词汇不同（语文是 anchor/lesson-focus/…，
    # 物理还有 story / worked-example / module-1..4 / interactive-lab / phet-lab /
    # practice-l1..l3 / core / summary），用候选列表让同一份映射跨学科通用。
    ('cover',           '开场 · 本课概览',          ['hero-infographic', 'cover', '开场']),
    ('interactive',     '情境导入 · 带着问题学',     ['story', 'anchor']),
    ('objectives',      '学习目标',                ['objectives']),
    ('quiz',            '前测 · 起点诊断',          ['pretest']),
    ('concept',         '概念一 · 核心知识',        ['核心', 'core', 'module-1', 'lesson-focus']),
    ('interactive',     '互动一 · 概念应用',        ['互动 - 概念归类', '地图探究', 'interactive-lab', 'module-2']),
    ('concept',         '概念二 · 深层理解',        ['module-3', 'deep-understanding']),
    ('interactive',     '互动二 · AI 多模态',       ['module-4', 'ai-media-zone', 'phet-lab', '历史地图']),
    ('concept',         '例析 · 方法与范例',        ['worked-example', 'lesson-method']),
    ('quiz',            '概念测 · 即时检验',        ['practice-l2']),
    ('interactive',     '综合任务 · 迁移应用',      ['lesson-focus', '精讲']),
    ('quiz',            '后测 · 达标检测与易错点',   ['posttest', 'error-clinic']),
    ('summary',         '小结 · 迁移与记忆锚点',     ['summary', '小结', '总结迁移', 'memory-anchor']),
    ('homework',        '分层作业 · 基础/应用/挑战',  ['practice-l1', 'practice-l3', 'gen:homework']),
    ('knowledge-graph', '知识图谱 · 本课节点位置',    ['knowledge-graph']),
    ('ai-tutor',        'AI 学伴 · 随时提问',       ['const:ai-tutor']),
]


def section_spans(h):
    """按标签配平列出所有 <section> 的 (start, end, attrs, inner)。"""
    tag = re.compile(r'<section\b([^>]*)>|</section\s*>', re.I)
    stack, out = [], []
    for m in tag.finditer(h):
        if m.group(1) is not None:
            stack.append((m.start(), m.group(1), m.end()))
        else:
            if not stack:
                continue
            start, attrs, inner_start = stack.pop()
            out.append((start, m.end(), attrs, h[inner_start:m.start()]))
    return out


def parse(h):
    """展平出全部有内容的块，保持文档顺序。

    ★ 关键：先决定哪些 span 会成为"内容块"，再算每个块的"直接部分"时
      **只减掉那些确实成为块的子节点**。
      否则会踩这个坑：无 id 且直接文本短的嵌套 <section>（如「知识脉络梳理」）
      既不进 units、又被从父块里减掉 —— 内容两头落空直接丢失
      （实测丢 13 块，保留率掉到 89-97%）。
    """
    spans = section_spans(h)

    def judge(start, end, attrs, inner):
        cls = (re.search(r'class="([^"]*)"', attrs) or [None, ''])[1]
        bid = (re.search(r'id="([^"]+)"', attrs) or [None, ''])[1]
        direct = inner
        for st2, en2, a2, i2 in spans:
            if st2 > start and en2 <= end:
                direct = direct.replace(i2, '')
        text = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', direct)).strip()
        has_cn = len(re.findall(r'[\u4e00-\u9fff]', text)) >= 4
        interesting = (bid or 'upgrade-block' in cls or 'core-knowledge-module' in cls
                       or 'ta-standard-section' in cls or 'slide-page' in cls)
        return (interesting and (bid or has_cn)), cls, bid

    ordered = sorted(spans, key=lambda x: (x[0], -x[1]))
    keep = []
    for sp in ordered:
        ok, cls, bid = judge(*sp)
        if ok:
            keep.append(sp)

    keep_spans = [(k[0], k[1], k[3]) for k in keep]
    units = []
    for start, end, attrs, inner in keep:
        cls = (re.search(r'class="([^"]*)"', attrs) or [None, ''])[1]
        bid = (re.search(r'id="([^"]+)"', attrs) or [None, ''])[1]
        tsh = (re.search(r'data-tsh="([^"]*)"', attrs) or [None, ''])[1]
        direct = inner
        for st2, en2, i2 in keep_spans:
            if st2 > start and en2 <= end:
                direct = direct.replace(i2, '')
        text = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', direct)).strip()
        key = bid or (tsh or ('anon-%d' % start))
        units.append({'key': key, 'cls': cls, 'text': text,
                      'inner': direct if direct.strip() else inner,
                      'full': inner, 'order': start})
    return units


def strip_tags(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s)).strip()


# 课件自带的 AI 学伴块（内容比占位完整）
OWN_TUTOR = re.compile(r'<section\b[^>]*\bid="teachany-ai-tutor-card"[^>]*>[\s\S]*?</section>', re.I)


def harvest_own_tutor(h):
    """取出课件自带的 AI 学伴块并从原位置摘除。

    ★ 不摘除会导致**同一张卡片渲染两遍**：`teachany-tutor-card.js` 按容器数量渲染，
      课件自带的块原先在 `#slide-container` **之外**（不属于任何一页，但脚本照样渲染），
      再加我注入的占位就是两个容器 —— 用户看到末页那张卡片整块重复。
    """
    m = OWN_TUTOR.search(h)
    if not m:
        return h, ''
    return h[:m.start()] + h[m.end():], m.group(0)



MIN_PAGE_CJK = 40   # 一页少于这么多汉字就认为"没有内容"，不建该页


def cjk_len(s):
    return len(re.findall(r'[\u4e00-\u9fff]', re.sub(r'<[^>]+>', ' ', re.sub(r'<script[\s\S]*?</script>', '', s))))


def page_has_content(body):
    """这一页是否有真实内容。

    ★ 用户明确说"没有什么 16 页限制" —— 源课件缺哪个模块就不建那一页，
      不要为了凑页数造空页（实测 phy-m-lens 原版没有前测，硬造出来的空页
      在用户眼里就是"缺模块 + 内容太少"）。
    """
    return cjk_len(body) >= MIN_PAGE_CJK


def inner_wrap(body):
    b = body.strip()
    if 'slide-inner' in b[:400]:
        return b
    return '<div class="slide-inner">\n' + b + '\n</div>'


def item_list(unit):
    t = unit.get('inner', '') if unit else ''
    qs = re.findall(r'(<div class="tu-q">[\s\S]*?</div>)', t)
    if qs:
        return qs
    return re.findall(r'(<li[^>]*>[\s\S]*?</li>)', t)


def gen_conceptest(by_key):
    pre = item_list(by_key.get('pretest'))
    picked = pre[:2]
    body = '<h2>概念测 · 即时检验</h2>\n<p>刚学完两个概念，先自己想，再点开看反馈里的错因。</p>\n'
    body += '\n'.join(picked) if picked else '<p>用自己的话说出本课两个核心概念的区别。</p>'
    return body


def gen_synthesis(extra_html=''):
    body = ('<h2>综合任务 · 迁移应用</h2>\n'
            '<p>选一个身边的例子，用本课的概念解释它，并说明这个解释在什么范围内成立。</p>\n')
    if extra_html:
        body += extra_html
    return body


def gen_homework(by_key):
    pre = item_list(by_key.get('pretest'))
    post = item_list(by_key.get('posttest'))
    errs = re.findall(r'([^\u2705<]{6,80})', '')
    raw = by_key.get('error-clinic', {}).get('inner', '')
    errs = [e.strip() for e in re.findall(r'\u274c\s*([^\u2705<]{4,80})', raw)]
    t1 = '\n'.join(pre[:2]) or '<p>复述本课两个核心概念的定义。</p>'
    t2 = '\n'.join(post[:2]) or '<p>用本课方法分析一个新例子。</p>'
    if errs:
        t3 = '\n'.join('<p>有同学认为：%s —— 请说明错在哪里。</p>' % e for e in errs[:2])
    else:
        t3 = '<p>自选一个现象，用本课概念解释它并说明适用边界。</p>'
    return ('<h2>分层作业</h2>\n'
            '<h3>⭐ 基础巩固（必做）</h3>\n' + t1 + '\n'
            '<h3>⭐⭐ 能力应用</h3>\n' + t2 + '\n'
            '<h3>⭐⭐⭐ 迁移挑战（选做）</h3>\n' + t3)


def matching_div_end(h, pos):
    depth, i = 1, pos
    tag = re.compile(r'<(/?)div\b[^>]*>', re.I)
    while True:
        m = tag.search(h, i)
        if not m:
            return -1
        if m.group(1) == '/':
            depth -= 1
            if depth == 0:
                return m.start()
        else:
            depth += 1
        i = m.end()


def texts_of(h):
    body = re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>', '', h, flags=re.I)
    out = set()
    for t in re.findall(r'>([^<>]{4,400})<', body):
        s = re.sub(r'\s+', '', t).strip()
        if len(re.findall(r'[\u4e00-\u9fff]', s)) >= 4:
            out.add(s)
    return out


SHELL_ONLY_DROPS = {'📑知识图谱', '📚课程内容', '🤝 AI 学伴', '🧭 导航'}


def build(cid, dry=False, verify=False):
    p = None
    for base in ('community', 'examples'):
        q = ROOT / base / cid / 'index.html'
        if q.exists():
            p = q
            break
    if not p:
        print("找不到 %s" % cid)
        return 1
    h = p.read_text(encoding='utf-8')
    if 'id="slide-container"' not in h:
        print("%s 未注入分页外壳，先跑 tools/migrate-to-v2-shell.py" % cid)
        return 1
    orig = h
    h, own_tutor = harvest_own_tutor(h)   # 摘出自带 AI 学伴块，避免重复渲染
    units = parse(h)
    by_key = {u['key']: u for u in units}
    print("📄 %s：展平出 %d 个内容块" % (cid, len(units)))
    for u in units:
        print("     - %-26s %s" % (u['key'][:26], u['text'][:42]))

    used, built = set(), []
    for idx, (ptype, tsh, sources) in enumerate(SPEC):
        parts, gen = [], None
        for src in sources:
            if src.startswith('gen:'):
                gen = src.split(':', 1)[1]
                continue
            if src.startswith('const:'):
                parts.append(own_tutor if own_tutor else AI_TUTOR_HTML)
                continue
            # ★ 取**全部匹配**而不是只取第一个：
            #   同一页可以有多个来源（如 cover = hero-infographic + 开场，
            #   summary = 小结 + 总结迁移 + memory-anchor）。只取第一个会把其余
            #   同类内容挤进"兜底页"，浪费了本该合并的版面。
            hits = []
            for k in [src]:                      # 精确
                if k in by_key and k not in used:
                    hits.append(k)
            if not hits:                          # 前缀（外层页的 key 是完整 data-tsh）
                for k in by_key:
                    if k.startswith(src) and k not in used and k not in hits:
                        hits.append(k)
            for k in hits:
                u = by_key[k]
                if strip_tags(u['inner']):
                    parts.append(u['inner'])
                    used.add(k)
        if gen == 'homework':
            parts.append(gen_homework(by_key))
        elif gen == 'conceptest':
            parts.append(gen_conceptest(by_key))
        elif gen == 'synthesis':
            parts.append(gen_synthesis())
        built.append([idx, ptype, tsh, '\n'.join(parts)])

    leftover = [u for u in units if u['key'] not in used and strip_tags(u['inner'])]
    # ★ 剩余块自动填给空页：不依赖课程相关的位置型 id（anon-<offset> 每门都不同），
    #   保证内容 100% 有归属，同时把空页补上真实内容而不是占位。
    empties = [b for b in built if not b[3]]
    pool = list(leftover)
    for b in empties:
        if not pool:
            break
        take = []
        # 尽量给 quiz 页配带题目特征的块、interactive 页配带互动特征的块
        if b[1] == 'quiz':
            take = [u for u in pool if ('题' in u['text'] or 'choice' in u['inner'])]
        elif b[1] == 'interactive':
            take = [u for u in pool if ('探究' in u['text'] or '检测' in u['text'] or '互动' in u['text'])]
        if not take:
            take = [pool[0]]
        for u in take[:2]:
            b[3] = (b[3] + '\n' + u['inner']) if b[3] else u['inner']
            pool.remove(u)
            leftover_used_marker = True
        print("   ➕ 剩余块 %s → 第 %d 页「%s」" % ([u['key'][:16] for u in take[:2]], b[0], b[2]))
    if pool:
        extra = '\n'.join(u['inner'] for u in pool)
        print("   ℹ️ 仍有 %d 块并入「综合任务」页兜底：%s" % (len(pool), [u['key'][:18] for u in pool][:6]))
        for b in built:
            if '综合任务' in b[2]:
                b[3] = (b[3] or '') + '\n' + extra
                break

    # ★ 最后一道兜底：容器里**不属于任何已抽取 <section> 块**的内容（实测这些课件
    #   还有一批 <div> 形式的深度模块，如「知识脉络梳理 / 易错点辨析 / 深入追问」），
    #   原样保留并追加到「综合任务」页，确保一个字都不丢。
    #   （文本比对曾因此丢 13 块，靠这一步兜住。）
    for b in built:
        if not b[3]:
            print("   ⚠️ [%d] %s 无内容源，占位待补" % (b[0], b[2]))
            b[3] = '<h2>%s</h2>\n<p>本页内容请结合本课知识与课堂活动展开。</p>' % b[2]

    # 容器内的"残留内容"（非 <section> 形式的模块）→ 追加到综合任务页
    _c_start = h.find('id="slide-container"')
    _c_start = h.rfind('<', 0, _c_start)
    _c_open_end = h.find('>', _c_start) + 1
    _c_close = matching_div_end(h, _c_open_end)
    residue = h[_c_open_end:_c_close] if _c_close > 0 else ''
    for u in units:
        # ★ 必须用 full（含子块）来减：若只减 direct，子块 HTML 会残留在兜底里，
        #   导致它们被重复插入 → 实测页数从 16 涨到 22–23。
        residue = residue.replace(u['full'], '')
    residue = re.sub(r'<!--[\s\S]*?-->', '', residue)
    # ★ 残留里可能还带着旧的 <section class="slide-page">（它们已被重新编排过），
    #   直接插入会让分页器把它们当成额外页 → 实测某门页数正确但导航点变成 22 个。
    #   这里把残留中的 slide-page 标签中和成普通 div，避免产生幻影页。
    # 把残留里**所有** <section> 标签都换成 div：哪怕只剩一个未配平的 section，
    # 也会把后面生成的页面解析成嵌套，导致"页数对但导航点错乱"（实测 11 页/17 点）。
    residue = re.sub(r'<section\b[^>]*>', '<div class="residue-block">', residue)
    residue = re.sub(r'</section\s*>', '</div>', residue)
    # ★ 残留里的 <div> 可能不配平（原文档被切开导致）——不补齐会把**后面生成的页面吞进它里面**，
    #   症状是"页数比 16 少、导航点却是 16"（实测某门只剩 7 页 / 16 点）。这里补齐闭合标签。
    # 双向配平：多开就补闭合；**多闭合也要补开头**——多出来的 </div> 会提前关闭
    # 我生成的页面，症状同样是"页数少于 16、导航点却是 16"。
    _o = len(re.findall(r'<div\b[^>]*>', residue))
    _c = len(re.findall(r'</div\s*>', residue))
    if _o > _c:
        residue += '\n' + '</div>' * (_o - _c)
        print(f"   🔧 残留 div 多开 {_o - _c} 个，已补 </div>")
    elif _c > _o:
        residue = '<div class="residue-pad">' * (_c - _o) + residue
        print(f"   🔧 残留 div 多闭 {_c - _o} 个，已在开头补 <div>")
    # 同样处理 section 之外可能残留的其它容器标签：span/p 等不影响分页，忽略。
    # 最后统一包一层，确保残留不泄漏到相邻页面。
    residue = '<div class="residue-wrap">' + residue + '</div>'
    if len(re.findall(r'[\u4e00-\u9fff]', re.sub(r'<[^>]+>', ' ', residue))) >= 20:
        # ★ 残留必须放到**容器内的最后一页**，不能放中间页。
        #   残留是"原文档被切开后剩下的碎片"，标签未必配平；一旦它多一个未闭合标签，
        #   就会把**它后面的所有页面吞进去**，症状是"页数少于 16、导航点却是 16"
        #   （实测 11 页 / 19 点）。放到最后一页则后面没有页面可被吞。
        built[-1][3] = (built[-1][3] or '') + '\n' + residue
        print("   ➕ 容器残留内容（非 section 模块）已保留到末页「%s」（%d 字节）"
              % (built[-1][2], len(residue)))

    # ★ 逐页做 div 配平（关键）。
    #   内容块来自"原文档被切开"的片段，可能自带宽余的 </div>；
    #   一旦某页多一个 </div>，浏览器会**提前关闭 #slide-container**，
    #   它后面的页面就被"弹出"成 BODY 的兄弟节点 —— 症状是"直属子节点只有 11 个、
    #   导航点却是 17 个，且缺失的页正好是后几页"（实测 hist-m-qin-han-unification）。
    #   逐页配平后，每页自己闭合，容器不会被提前关掉。
    # ★ 只保留有内容的页（cover 永远保留，它是入口）
    kept = []
    skipped = []
    for i, pt, t, bd in built:
        # cover 是入口；knowledge-graph / ai-tutor 是 **JS 渲染**的模块，
        # 内容在脚本里，用纯文本判断会误杀（用户已决定补脚本引用，这两页必须留）
        js_module = pt in ('knowledge-graph', 'ai-tutor')
        if pt == 'cover' or js_module or page_has_content(bd):
            kept.append((i, pt, t, bd))
        else:
            skipped.append(t)
    if skipped:
        print("   ✂️ 跳过无内容页 %d 个（源课件本就没有该模块）：%s"
              % (len(skipped), '、'.join(s.split(' · ')[0] for s in skipped)))
    # 重新编号 page-index
    built = [(k, pt, t, bd) for k, (_, pt, t, bd) in enumerate(kept)]

    balanced = []
    fixed = 0
    for i, pt, t, bd in built:
        body = inner_wrap(bd)
        _o = len(re.findall(r'<div\b[^>]*>', body))
        _c = len(re.findall(r'</div\s*>', body))
        if _o > _c:
            body += '\n' + '</div>' * (_o - _c)
            fixed += 1
        elif _c > _o:
            body = '<div class="page-pad">' * (_c - _o) + body
            fixed += 1
        # ★ <section> 也要配平！内容块本身很多就是 <section class="section" id="…">，
        #   嵌进本页的 <section class="slide-page"> 里；只要有一个未闭合，
        #   浏览器就会把**后面的页吞进来**，症状是某页只剩一个残缺 section、
        #   可见字数为 0（实测 phy-m-lens 第 4 页前测变成空壳，用户看到就是"缺模块"）。
        _so = len(re.findall(r'<section\b[^>]*>', body))
        _sc = len(re.findall(r'</section\s*>', body))
        if _so > _sc:
            body += '\n' + '</section>' * (_so - _sc)
            fixed += 1
        elif _sc > _so:
            body = '<section class="page-pad">' * (_sc - _so) + body
            fixed += 1
        balanced.append((i, pt, t, body))
    if fixed:
        print(f"   🔧 逐页 div 配平：{fixed} 页有失衡已修正")

    sections = '\n'.join(
        '<section class="slide-page" data-page-type="%s" data-page-index="%d" data-tsh="%s">%s</section>'
        % (pt, i, t, bd) for i, pt, t, bd in balanced)

    start = h.find('id="slide-container"')
    start = h.rfind('<', 0, start)
    open_end = h.find('>', start) + 1
    close = matching_div_end(h, open_end)
    if close < 0:
        # ★ 回退：原文档里可能有**未闭合的 <div>**，导致配平算法永远到不了 depth 0。
        #   此时用"最后一个分页节的 </section> 之后"作为容器内容边界 ——
        #   容器本来就是装分页节的。实测 geo-m-climate-basics（20 页）就是这种。
        SP_OPEN = r'<section\b(?=[^>]*\bslide-page\b)[^>]*>'
        last_sec = None
        for m in re.finditer(SP_OPEN, h):
            e = h.find('</section>', m.end())
            if e > 0 and (last_sec is None or e > last_sec):
                last_sec = e
        if last_sec is None:
            print("❌ 容器标签未配平且找不到分页节，放弃（不破坏文件）")
            return 1
        close = last_sec + len('</section>')
        print("   ⚠️ 容器 div 未配平（原文档有未闭合标签），已按「最后一个分页节之后」作为边界回退")
    # ★ 容器**之外**可能还残留原始的 <section class="slide-page">：
    #   有些课件的容器只包住一部分分页节，其余散落在容器外面。
    #   我的替换只动容器内部，于是这些散落的原始页会留下来 → 导航点变成 19 个、
    #   而容器直属子节点只有 11 个（实测 hist-m-qin-han-unification）。
    #   它们的内容已经作为"内容块"进入我重建的 16 页，所以这里直接清掉。
    tail_part = h[close:]
    # ★ 不能只匹配 `<section class="slide-page"`：有课件的 class **不在第一位**
    #   （写成 `<section data-conceptest="true" … class="slide-page">`），会漏掉，
    #   症状是"页数 16 正确、导航点却 17 个"（实测 hist-m-qin-han-unification）。
    SP_OPEN = r'<section\b(?=[^>]*\bslide-page\b)[^>]*>'
    n_out = len(re.findall(SP_OPEN, tail_part))
    if n_out:
        tail_part = re.sub(SP_OPEN + r'[\s\S]*?</section>', '', tail_part)
        print(f"   🔧 清掉容器外残留的 {n_out} 个原始分页节")
    h2 = h[:open_end] + '\n' + sections + '\n' + tail_part

    if dry:
        print("   (--dry-run) 将重建为 %d 页" % len(built))
        return 0

    if verify:
        b_txt, a_txt = texts_of(orig), texts_of(h2)
        lost = [t for t in b_txt if t not in a_txt and t not in SHELL_ONLY_DROPS]
        ratio = 1 - len(lost) / max(1, len(b_txt))
        print("   🔍 内容比对：原文 %d 块 → 新文 %d 块 · 丢失 %d · 保留率 %.1f%%"
              % (len(b_txt), len(a_txt), len(lost), ratio * 100))
        for t in lost[:15]:
            print("      ✗ %s" % t[:70])
        if ratio < 0.98:
            print("   ❌ 保留率 < 98%，**拒绝写入**")
            return 2

    # ★ 收尾：去掉重复的内联脚本。
    #   有些 <script>（如 const knowledgeGraphData=…）位于 <section> **之外**，
    #   既被原位置保留、又随"残留"兜底进来一份 → 重复声明，
    #   报 "Identifier 'xxx' has already been declared" 导致后一份整段不执行。
    #   处理：同内容的（归一化后）脚本块只保留第一份。
    seen_scripts = {}
    def dedupe_scripts(m):
        body = re.sub(r'\s+', ' ', m.group(1)).strip()
        if len(body) < 80:
            return m.group(0)
        if body in seen_scripts:
            return '<!-- 重复脚本已移除（同一段内联脚本出现两次，会导致 Identifier 重复声明） -->'
        seen_scripts[body] = True
        return m.group(0)

    h2_before = h2
    h2 = re.sub(r'<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>', dedupe_scripts, h2)
    if h2 != h2_before:
        print(f"   🔧 移除了重复内联脚本，减少 {len(h2_before) - len(h2)} 字节")

    p.write_text(h2, encoding='utf-8')
    print("   ✅ 已重建为 %d 页 · %d → %d 字节" % (len(built), len(orig), len(h2)))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('course_id', nargs='+')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--verify', action='store_true',
                    help='写入前比对内容保留率，<98%% 拒绝写入（强烈建议开启）')
    a = ap.parse_args()
    rc = 0
    for cid in a.course_id:
        rc |= build(cid, a.dry_run, a.verify)
    sys.exit(rc)


if __name__ == '__main__':
    main()
