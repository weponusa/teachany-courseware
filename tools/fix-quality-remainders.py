#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""收尾小类缺口：hero 主图 / <title> 学段年级 / 前测后测 / 核心知识模块计数 /
ConcepTest / Bloom / 脚手架 / 实质 section / 学段徽章 / 声明式历史地图 / 断锚。

每一处改动都过 tools/_qa_gate.apply_guarded（= pre-push 钩子用的同一套校验），
所以任何一门一旦错误数上升会被自动回滚，不会污染 push。

用法:  python3 tools/fix-quality-remainders.py [--only cid1,cid2]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from _qa_gate import apply_guarded  # noqa: E402

# ────────────────────────── 1. <title> 补学段+年级 ──────────────────────────
TITLES = {
    'bio-cell-life': '细胞的生活与能量 · 初中生物 G7 · TeachAny v7.20',
    'chn-e-picture-writing': '看图写话 · 小学语文 G3 · TeachAny v7.20',
    'eng-e-past-simple': '一般过去时 · 小学英语 G5 · TeachAny v7.20',
    'math-m-pythagorean-theorem': '勾股定理 · 初中数学 G8 · TeachAny v7.20',
    'phy-m-heat-engine': '内燃机与热机效率：从可观察现象到可测变量 · 初中物理 G9 · TeachAny v7.20',
}

# ────────────────────────── 2. 学段徽章写错 ──────────────────────────
BADGES = {
    'chn-e-picture-writing': [('>初中语文</span>', '>小学语文</span>')],
    'eng-e-past-simple': [('>初中英语</span>', '>小学英语</span>')],
}

# ────────────────────────── 3. 前测 / 后测 ──────────────────────────
Q = '\n'.join([
    '<div class="tu-q" data-answer="{a}">',
    '<h3>{t}</h3>',
    '<div class="tu-opts">',
    '<button type="button" class="tu-opt" data-choice="A" data-diagnosis="{dA}">A. {A}</button>',
    '<button type="button" class="tu-opt" data-choice="B" data-diagnosis="{dB}">B. {B}</button>',
    '<button type="button" class="tu-opt" data-choice="C" data-diagnosis="{dC}">C. {C}</button>',
    '</div><div class="tu-fb" hidden></div></div>',
])


def q(t, opts, a, dg):
    return Q.format(t=t, a=a, A=opts[0], B=opts[1], C=opts[2], dA=dg[0], dB=dg[1], dC=dg[2])


PRETEST = {
    'ancient-china-h': [
        q('前测 1：西周「分封制」主要解决的是什么问题？',
          ('如何在王畿之外分配土地与统治权', '如何向农民征收赋税', '如何抵御北方游牧民族'),
          'A', ('正确！分封是「授民授疆土」，用血缘与功臣关系维系统治',
                '赋税是分封之后才产生的管理问题，不是分封要解决的核心',
                '抵御外族是分封带来的结果之一，不是制度设计的出发点')),
        q('前测 2：秦朝在地方推行郡县制，与分封制相比最核心的变化是？',
          ('地方长官由中央任免、不世袭', '土地全部归农民所有', '贵族身份被彻底取消'),
          'A', ('正确！任免权上收中央，是中央集权的关键一步',
                '土地制度另有变化，但不足以概括郡县制的要害',
                '贵族并未消失，只是不再靠世袭分割地方治权')),
        q('前测 3：研究中国古代史，下列哪一类属于第一手史料？',
          ('出土青铜器上的铭文', '后世创作的历史小说', '现代学者的研究论文'),
          'A', ('正确！与事件同时代、未经转述的材料才是第一手史料',
                '历史小说含有大量文学加工，属于二手甚至三手材料',
                '研究论文是现代人的解释，属于二手研究')),
    ],
    'chem-h-galvanic-cell': [
        q('前测 1：原电池能把化学能转化为电能，必须满足什么条件？',
          ('形成闭合回路', '两电极材料完全相同', '两杯溶液浓度完全相同'),
          'A', ('正确！有外电路也要有内电路，回路断开就没有持续电流',
                '电极材料相同就没有电势差，反而做不成原电池',
                '浓度是否相同不影响能否形成回路，只影响电动势大小')),
        q('前测 2：锌铜原电池中，锌片的作用是？',
          ('负极，发生氧化反应', '正极，发生还原反应', '只作导电的惰性电极'),
          'A', ('正确！锌比铜活泼，失电子被氧化，作负极',
                '铜才是正极，发生的是还原反应',
                '锌本身参与反应被消耗，不是惰性电极')),
        q('前测 3：盐桥在原电池里的作用是？',
          ('维持电荷平衡、构成内电路', '作为反应物参与放电', '只为加快反应速率'),
          'A', ('正确！盐桥让离子定向迁移，保证两半电池电荷平衡',
                '盐桥中的电解质不参与电极反应',
                '反应速率不是盐桥的主要职能，撤掉盐桥电流会中断')),
    ],
    'hist-h-ancient-civ': [
        q('前测 1：判断一处史前遗址是否进入「文明」阶段，最硬的证据通常是？',
          ('出现城市、文字与礼仪性建筑', '出土大量打制石器', '遗址占地面积大'),
          'A', ('正确！这三者标志公共权力与社会分层的出现',
                '打制石器属于旧石器时代，恰恰是文明之前的证据',
                '面积大小受环境影响，不能单独说明社会组织程度')),
        q('前测 2：中华文明起源的特点，更符合考古发现的是？',
          ('多元起源、逐步汇聚', '单一中心向外扩散', '由外来文明传入'),
          'A', ('正确！辽河、黄河、长江多区域并行发展，后来汇聚为「一体」',
                '各地同时期都有独立发展的文化序列，不是单中心扩散',
                '目前没有证据支持外来传入说')),
        q('前测 3：新石器时代农业出现，最直接的影响是？',
          ('出现定居聚落、人口增长', '开始使用打制石器', '出现铁制农具'),
          'A', ('正确！有了稳定食物来源，定居与人口增长随之而来',
                '打制石器早于农业，时间顺序相反',
                '铁器要到春秋战国才普及，早了数千年')),
    ],
    'hist-h-early-state': [
        q('前测 1：早期国家与部落联盟最大的区别是？',
          ('出现了凌驾于社会之上的公共权力', '人口规模更大', '活动范围更广'),
          'A', ('正确！有了脱离生产的管理者与强制性权力，才叫国家',
                '人口多寡不改变权力性质，部落联盟也可能很大',
                '活动范围只是地域指标，不说明组织形态')),
        q('前测 2：商周时期最能体现王权的物质载体是？',
          ('青铜礼器（如鼎）', '普通陶器', '石制农具'),
          'A', ('正确！鼎的数量与组合标识身份等级，是权力的物化形式',
                '陶器是日常用器，等级标识作用有限',
                '农具属生产工具，与王权象征无关')),
        q('前测 3：研究早期国家，都城遗址为什么特别重要？',
          ('它同时反映权力、礼仪与经济组织', '它的面积一定最大', '它保存得最完整'),
          'A', ('正确！宫殿区、祭祀区、手工业区并存，是一次性读到多重信息的证据',
                '面积受地形限制，不一定最大',
                '保存状况是偶然的，不能作为选材依据')),
    ],
    'chn-e-poetry-rhythm': [
        q('前测 1：读古诗时，一般按什么来划分停顿？',
          ('按诗句的意思和音步', '固定每两个字停一次', '想停就停，没有规律'),
          'A', ('正确！节奏要跟着意思走，同时兼顾读起来顺口',
                '机械两字一停常会把词语切断，读出来别扭',
                '节奏有相对稳定的规律，随意停顿就失去了韵味')),
        q('前测 2：「韵脚」指的是？',
          ('诗句末尾押韵的字', '诗句的第一个字', '句子中间反复出现的字'),
          'A', ('正确！句末押韵的字像脚一样落在同一个音上，所以叫韵脚',
                '句首用字主要影响语气，与押韵无关',
                '句中的重复字属于修辞手法，不是韵脚')),
        q('前测 3：节奏的变化对诗歌有什么作用？',
          ('让情感表达更有起伏', '只是为了方便背诵', '与情感表达没有关系'),
          'A', ('正确！急促与舒缓的节奏，直接对应紧张与舒缓的情绪',
                '好背是副产品，不是节奏存在的理由',
                '节奏与情感密切相关，朗读时最能体会')),
    ],
}

POSTTEST = {
    'ancient-china-h': [
        q('后测 1：从分封制到郡县制，中央与地方关系的变化趋势是？',
          ('中央集权不断加强', '地方权力持续扩大', '两者始终势均力敌'),
          'A', ('正确！地方治权逐步收归中央，是贯穿中国古代史的主线之一',
                '方向恰好相反，分封时的世袭治权被逐步收回',
                '势均力敌只是个别时期的暂时状态')),
        q('后测 2：判断一项制度是否「加强中央集权」，最该看什么？',
          ('地方官员的任免权掌握在谁手里', '全国赋税总额是否增加', '疆域面积是否扩大'),
          'A', ('正确！任免权是集权的开关，抓住它就能判断制度性质',
                '赋税增长可能来自经济发展，不说明权力归属',
                '疆域扩大与权力集中是两件事')),
        q('后测 3：「史料实证」的核心要求是？',
          ('结论必须建立在可核查的史料之上', '尽量引用权威学者的观点', '用传说填补史料空白'),
          'A', ('正确！有一分材料说一分话，是历史解释的底线',
                '权威观点仍需回到材料检验',
                '传说可以作为线索，不能当作证据')),
    ],
    'chem-h-galvanic-cell': [
        q('后测 1：判断原电池的正负极，最可靠的方法是？',
          ('比较电极材料失电子的难易', '背金属活动性顺序口诀', '比较两个电极的质量'),
          'A', ('正确！本质是看谁更容易失电子，口诀只是辅助记忆',
                '口诀在特殊介质中会失效，不能当作判据',
                '质量变化是反应的结果，不是判断依据')),
        q('后测 2：书写电极反应式，最容易出错的一步是？',
          ('电子得失数与电荷守恒没有配平', '忘记标沉淀符号', '忘记注明温度'),
          'A', ('正确！配平电子与电荷是电极反应式的核心，错这一处整题失分',
                '沉淀符号是书写规范，不是最易错处',
                '温度条件通常不影响电极反应式的书写')),
        q('后测 3：若把盐桥拔掉，电流表读数会怎样？',
          ('归零，因为内电路断开', '变大，因为阻力减少', '保持不变'),
          'A', ('正确！内电路一断，离子无法迁移，放电立即停止',
                '拔掉盐桥是断路而不是减阻，读数只会变小',
                '读数不可能保持不变，这正是盐桥作用的直接证据')),
    ],
    'hist-h-ancient-civ': [
        q('后测 1：良渚古城遗址最能说明？',
          ('长江下游距今约 5000 年已出现早期国家形态', '黄河流域最早进入文明', '中国文明始于商朝'),
          'A', ('正确！大型水利工程与高等级墓葬说明当时已有动员能力',
                '考古发现是多个区域并行发展，「最早」的说法不成立',
                '商朝已有成熟文字与国家，文明显然更早')),
        q('后测 2：用考古材料研究史前史，最应注意的是？',
          ('区分证据与推测，说明推理链条', '只采用文献记载', '以传说作为主要依据'),
          'A', ('正确！把「看到了什么」和「推出什么」分开说，才是实证',
                '史前史几乎没有同时期文献，此路不通',
                '传说需要考古印证，不能单独作为依据')),
        q('后测 3：「多元一体」格局的形成过程说明？',
          ('各区域文化长期交流融合', '各区域长期彼此孤立', '只有中原地区产生了文明'),
          'A', ('正确！多支文化在互动中汇聚，才形成后来的中华文明',
                '玉器、陶器等器物的跨区传播说明交流一直存在',
                '辽河、长江流域同样有独立发展的文明因素')),
    ],
    'hist-h-early-state': [
        q('后测 1：从夏商到西周，王权强化的主要手段是？',
          ('垄断青铜礼器与祭祀权', '单纯扩大耕地面积', '单纯增加人口'),
          'A', ('正确！把「通天」的权力收归王室，就从观念上确立了等级秩序',
                '耕地与人口是实力基础，但不能直接说明王权如何被承认',
                '人口增长与权力集中没有必然联系')),
        q('后测 2：「礼器」在早期国家中的核心功能是？',
          ('标识身份等级、维系政治秩序', '用于日常饮食', '作为交换货币'),
          'A', ('正确！鼎簋数量与组合对应等级，礼制是看得见的秩序',
                '礼器脱离日常使用才有神圣性',
                '礼器是身份象征，不作货币流通')),
        q('后测 3：判断一个早期政治体是否形成了国家，关键看？',
          ('是否出现稳定的权力机构与等级秩序', '是否使用青铜器', '是否有文字'),
          'A', ('正确！国家是以公共权力和分层秩序为标志的',
                '青铜器是技术标志，不等于国家形态',
                '文字与国家的出现不必同步，不能反向否决')),
    ],
    'chn-e-poetry-rhythm': [
        q('后测 1：给「白日依山尽」划分停顿，最合适的是？',
          ('白日／依山尽', '白／日依／山尽', '白日依／山尽'),
          'A', ('正确！按意思和音步划，读起来才顺口',
                '这样切会把「白日」这个词语拆开',
                '把「依山尽」拆开，破坏了完整的意思')),
        q('后测 2：两首诗读起来一个舒缓、一个急促，最可能的原因是？',
          ('节奏与用韵不同', '字数不同', '作者年代不同'),
          'A', ('正确！节奏的快慢和韵脚的开合直接带来情绪差异',
                '字数相同也可能读起来完全不同',
                '年代只是背景，不直接决定朗读感受')),
        q('后测 3：要读出诗的节奏，最有效的练习方法是？',
          ('出声朗读、边读边划节奏', '只看注释背意思', '默读一遍就够'),
          'A', ('正确！节奏是听出来的，出声读才能发现问题',
                '理解意思不等于读得出节奏',
                '默读感受不到停顿与韵脚的效果')),
    ],
}
PRETEST_TITLE = '📝 前测：先摸一摸你的起点'
POSTTEST_TITLE = '✅ 后测：学会了吗？达标检测'


def sec_pretest(cid: str) -> str:
    body = '\n'.join(PRETEST[cid])
    return (
        f'\n<section class="section teachany-upgrade-block" id="pretest" data-tts data-tsh="先凭直觉选一选，答错的地方就是本课要补的地方" '
        f'data-bloom-level="remember" data-scaffold="partial">\n'
        f'<h2 class="section-title">{PRETEST_TITLE}</h2>\n'
        f'<p style="opacity:.85;margin-bottom:12px">3 道题，先不看课文，凭印象作答；点选项立刻看到诊断。</p>\n'
        f'{body}\n</section>\n')


def sec_posttest(cid: str) -> str:
    body = '\n'.join(POSTTEST[cid])
    return (
        f'\n<section class="section teachany-upgrade-block" id="posttest" data-tts data-tsh="对照学习目标，检查是否真的学会了" '
        f'data-bloom-level="evaluate" data-scaffold="partial">\n'
        f'<h2 class="section-title">{POSTTEST_TITLE}</h2>\n'
        f'<p style="opacity:.85;margin-bottom:12px">这 3 题对应本课的核心方法，做完再回看易错点。</p>\n'
        f'{body}\n</section>\n')


# ────────────────────────── 4. 补充实质 section（≥120 中文字） ──────────────────────────
EXTRA_SECTION = {
    'chn-m-whole-book-reading': (
        'book-map', '📚 整本书阅读的三条路线',
        '<p>整本书阅读最大的困难不是读不完，而是读完以后脑子里只剩情节。要解决这个问题，可以先给自己三条路线，'
        '读书时沿着任意一条走，都能读出结构来。</p>'
        '<p><strong>第一条是人物线。</strong>把主要人物列成一张表，记下他每一次出场时的处境、选择和变化。'
        '人物的变化往往就是作者想说的话。同一个人物前后两次面对相似的处境，选择不同，这个转折点就是全书的关节。</p>'
        '<p><strong>第二条是情节线。</strong>按「起因—发展—转折—结局」把全书折成四段，找出转折点在哪里。'
        '能准确指出转折点，就说明你读懂了作者的安排，而不是只记住了热闹的部分。</p>'
        '<p><strong>第三条是主题线。</strong>合上书问自己一个问题：如果只能向别人推荐这本书的一个理由，我会说什么？'
        '把这个理由写成一句话，再从书里找两处原文作为证据。证据能站住，主题才算真的读出来。</p>'
        '<p>三条路线不必同时走完。一本书用一条路线读透，比三条都浅尝一遍更有收获。</p>'),
    'math-h-functions-advanced': (
        'function-map', '📈 把单调性、奇偶性、周期性串成一张网',
        '<p>函数进阶部分最容易出现的情况是「每个性质都会，合起来就不会」。原因在于把三个性质当成三块独立知识记，'
        '而它们本来描述的是同一件事的三个侧面：函数图像长什么样。</p>'
        '<p><strong>单调性描述图像的走向。</strong>它回答「随着自变量变大，函数值怎么变」，在解题时决定不等号方向，'
        '也决定最值取在区间的哪一端。判断单调性优先用定义，其次才考虑导数。</p>'
        '<p><strong>奇偶性描述图像的对称。</strong>偶函数关于 y 轴对称，奇函数关于原点对称。它最大的价值是「知一半、知全部」：'
        '只要知道半个区间的图像，另一半就能画出来，求值域、解不等式都可以只做一半再翻折。</p>'
        '<p><strong>周期性描述图像的重复。</strong>它回答「隔多远又长回原样」，用来把大自变量压缩回一个周期内。'
        '周期和对称经常一起出现：有两条对称轴就能推出周期，这一点在选择题里出现频率很高。</p>'
        '<p>把三者合起来看：奇偶性给你半个定义域，周期性给你一个周期，单调性给你这个周期上的走势——'
        '三句话拼在一起，整条曲线就确定了。做题时先问「能不能缩小讨论范围」，比直接硬算更省力。</p>'),
}


# ────────────────────────── 5. 核心知识模块计数 ──────────────────────────
CORE_CLASS = {
    'bio-cell-division': 2,
    'reading-academy': 2,
    'history-sanguo-sui-tang': 1,
    'sci-e-information-tech': 1,
}


# ────────────────────────── 6. ConcepTest 挂到已有的概念检测处 ──────────────────────────
CONCEPTEST = ['bio-cell-life', 'chn-pingze-grade1']


# ────────────────────────── 7. Bloom / 脚手架 ──────────────────────────
BLOOM_ADD = {
    'chem-oxidation-reduction': [
        ('id="module1"', 'apply'), ('id="module2"', 'apply'),
        ('id="module3"', 'analyze'), ('id="module4"', 'analyze'),
        ('id="errors"', 'evaluate'),
    ],
}
SCAFFOLD_ADD = {
    'chem-periodic-table': [
        ('id="module-2"', 'partial'), ('id="module-3"', 'partial'),
        ('id="module-4"', 'partial'), ('id="synthesis"', 'partial'),
    ],
}


# ────────────────────────── 8. 历史地图（声明式标准模块） ──────────────────────────
MAP_CFG = {
    "eras": [
        {"id": "ce-500", "label": "约 500 年 · 古典尾声", "file": "009-ce-500.geojson",
         "fill": "#6366f1", "stroke": "#4f46e5",
         "desc": "<span class=\"thm-year-tag\">500</span><strong>西罗马灭亡前后</strong>：日耳曼诸部在原帝国疆域上建立王国，"
                 "东罗马（拜占庭）延续，法兰克人崛起于高卢。",
         "cities": [[41.90, 12.50, "罗马", "Rome", "西罗马旧都，5 世纪后政治地位衰落"],
                    [41.01, 28.98, "君士坦丁堡", "Constantinople", "东罗马帝国都城，地中海世界的中心"],
                    [48.86, 2.35, "巴黎", "Paris", "法兰克人势力范围的核心城市"]]},
        {"id": "ce-800", "label": "约 800 年 · 加洛林与哈里发", "file": "010-ce-800-caliphate-carolingian.geojson",
         "fill": "#0ea5e9", "stroke": "#0284c7",
         "desc": "<span class=\"thm-year-tag\">800</span><strong>两个大帝国并立</strong>：查理曼加冕为「罗马人的皇帝」，"
                 "阿拔斯哈里发国控制西亚、北非与伊比利亚，地中海两岸形成长期对峙与交流。",
         "cities": [[50.78, 6.08, "亚琛", "Aachen", "查理曼宫廷所在地，加洛林文艺复兴的中心"],
                    [33.31, 44.36, "巴格达", "Baghdad", "阿拔斯王朝都城，知识与贸易枢纽"],
                    [37.39, -5.99, "塞维利亚", "Seville", "安达卢斯地区的重要城市"]]},
        {"id": "ce-1000", "label": "约 1000 年 · 三洲交界", "file": "011-ce-1000.geojson",
         "fill": "#f59e0b", "stroke": "#d97706",
         "desc": "<span class=\"thm-year-tag\">1000</span><strong>封建秩序成形</strong>：西欧采邑与领主制稳定下来，"
                 "拜占庭处于鼎盛期，北欧、东欧相继基督教化，贸易与城市重新活跃。",
         "cities": [[41.01, 28.98, "君士坦丁堡", "Constantinople", "地中海贸易的十字路口"],
                    [51.51, -0.13, "伦敦", "London", "英格兰王国政治与贸易中心"],
                    [55.68, 12.57, "哥本哈根", "Copenhagen", "北欧基督教化与王国形成的枢纽"]]},
        {"id": "ce-1200", "label": "约 1200 年 · 十字军与蒙古", "file": "012-ce-1200-mongol-rise.geojson",
         "fill": "#ef4444", "stroke": "#dc2626",
         "desc": "<span class=\"thm-year-tag\">1200</span><strong>交流被拉长到欧亚大陆两端</strong>：十字军东征带来东西方碰撞，"
                 "蒙古崛起打通草原通道，商路与知识沿欧亚大陆重新流动。",
         "cities": [[41.01, 28.98, "君士坦丁堡", "Constantinople", "1204 年遭第四次十字军攻陷"],
                    [47.0, 10.0, "威尼斯", "Venice", "东地中海贸易的最大受益者"],
                    [47.90, 106.91, "哈拉和林", "Karakorum", "蒙古帝国早期的草原都城"]]},
    ],
    "center": [45, 20],
    "zoom": 4,
    "fitBounds": [[26, -12], [62, 60]],
}

MAP_SEC = """<section class="section" id="medieval-map" data-tts data-bloom-level="analyze" data-scaffold="partial" data-tsh="同一片地中海，为什么两岸走出了不同的政治道路？">
  <h2 class="section-title">🗺️ 中世纪欧洲地图：八百年间的边界变迁</h2>
  <p style="color:var(--text-dim);margin-bottom:16px">按年代切换，观察西罗马灭亡后地中海两岸如何分化：一边是封建领主与教会，一边是哈里发与商路。换图时留意城市位置的变化。</p>
  <div data-teachany-map="thm-community-history-medieval-europe"
       data-teachany-map-scope="world"
       data-teachany-map-title="中世纪欧洲与地中海世界（500—1200）">
    <script type="application/json" data-teachany-map-config>
%s
    </script>
  </div>
</section>
""" % json.dumps(MAP_CFG, ensure_ascii=False, indent=6)


# ────────────────────────── 9. 补两门缺模块 ──────────────────────────
MODULE_ADD = {
    'bio-h-nervous-regulation': (
        'module-4', '分级调节：低级中枢受高级中枢控制',
        '<p>神经系统并不是「谁大谁说了算」的平级关系，而是分成脊髓、脑干、小脑、大脑皮层等层次。'
        '越靠下的中枢负责越「程序化」的动作，越靠上的中枢负责越复杂的判断与调控。</p>'
        '<p>以排尿反射为例：婴儿的排尿由脊髓的低级中枢直接完成，所以不能自主控制；随着大脑皮层发育，'
        '成年人能够有意识地延迟排尿，说明高级中枢可以对低级中枢施加抑制或促进。</p>'
        '<p>这种「低级中枢受高级中枢调控」的结构叫分级调节，它的意义在于既保证基本反射的快速可靠，'
        '又为行为留出灵活调节的空间。临床上脊髓横断的病人会出现反射亢进，正是失去了高级中枢抑制的结果。</p>'),
    'bio-h-sugar-lipid': (
        'module-5', '能量比较：为什么脂肪是更好的储能物质',
        '<p>糖类和脂质都能提供能量，但两者在储能上的分工不同。相同质量下，脂肪氧化释放的能量约为糖类的两倍多，'
        '所以脂肪是主要的储能物质，而糖类是主要的能源物质。</p>'
        '<p>造成差异的原因在分子结构：脂肪分子中碳氢键比例高、含氧量低，氧化时需要的氧更多、释放的能量也更多；'
        '糖类含氧量高，能量密度相对较低。</p>'
        '<p>此外，糖类可以溶于水，便于运输和快速动员，适合承担日常供能；脂肪不溶于水，可以几乎不含水地紧密堆积，'
        '同等能量占的体积和质量更小，适合长期储存。冬眠动物在入冬前大量积累脂肪，正是这个道理。</p>'),
}


def first_pos(h: str, pats):
    for p in pats:
        m = re.search(p, h)
        if m:
            return m.start()
    return -1


def section_end(h: str, sid: str):
    """返回 id="sid" 那个 section 结束标签之后的位置（用于把新 section 插在它后面）。"""
    m = re.search(r'<section\b[^>]*id="%s"' % re.escape(sid), h)
    if not m:
        return 0
    j = h.find('</section>', m.end())
    return j + len('</section>') if j != -1 else 0


def add_class(h: str, needle: str, cls: str, limit: int = 1) -> str:
    """给含 needle 的 section 开标签补一个 class（不改已有 class）。"""
    done = 0
    out, i = [], 0
    while done < limit:
        k = h.find(needle, i)
        if k == -1:
            out.append(h[i:])
            break
        s = h.rfind('<section', 0, k)
        e = h.find('>', max(k, s))
        if s == -1 or e == -1:
            out.append(h[i:k + len(needle)])
            i = k + len(needle)
            continue
        tag = h[s:e]
        if 'class="' in tag:
            new = tag.replace('class="', 'class="%s ' % cls, 1)
        else:
            new = tag + ' class="%s"' % cls
        out.append(h[i:s])
        out.append(new)
        i = e
        done += 1
    out.append(h[i:])
    return ''.join(out)


def add_attr(h: str, id_marker: str, attr: str) -> str:
    k = h.find(id_marker)
    if k == -1:
        return ''
    s = h.rfind('<section', 0, k)
    e = h.find('>', k)
    if s == -1 or e == -1:
        return ''
    tag = h[s:e]
    if attr.split('=')[0] in tag:
        return h
    return h[:e] + ' ' + attr + h[e:]


OPS = {}


def op(cid, fn):
    OPS.setdefault(cid, []).append(fn)


for cid, new_title in TITLES.items():
    op(cid, lambda h, c=cid, t=new_title: re.sub(r'<title>.*?</title>', '<title>%s</title>' % t, h, count=1, flags=re.S))

for cid, pairs in BADGES.items():
    def badge(h, pairs=pairs):
        for a, b in pairs:
            if a not in h:
                return ''
            h = h.replace(a, b, 1)
        return h
    op(cid, badge)

for cid in PRETEST:
    def pre(h, c=cid):
        if re.search(r'pretest|前测|课前诊断', h, re.I):
            return ''
        end = section_end(h, 'objectives') or section_end(h, 'anchor')
        if end:
            return h[:end] + sec_pretest(c) + h[end:]
        i = first_pos(h, [r'<section\b[^>]*id="module-1"', r'<section\b[^>]*id="introduction"',
                          r'<section\b[^>]*id="lesson-focus"'])
        if i == -1:
            return ''
        return h[:i] + sec_pretest(c) + h[i:]
    op(cid, pre)
    if cid in POSTTEST:
        def post(h, c=cid):
            if re.search(r'posttest|后测|学习检测|达标检测', h, re.I):
                return ''
            end = section_end(h, 'summary')
            if end:
                return h[:end] + sec_posttest(c) + h[end:]
            i = first_pos(h, [r'<section\b[^>]*id="knowledge-graph"', r'<section\b[^>]*id="summary"'])
            if i == -1:
                return ''
            return h[:i] + sec_posttest(c) + h[i:]
        op(cid, post)

for cid, (sid, title, body) in EXTRA_SECTION.items():
    def extra(h, sid=sid, title=title, body=body):
        if 'id="%s"' % sid in h:
            return ''
        blk = ('\n<section class="section core-knowledge-module text-module" id="%s" data-tts '
               'data-bloom-level="analyze" data-scaffold="partial">\n'
               '<h2 class="section-title">%s</h2>\n%s\n</section>\n') % (sid, title, body)
        i = first_pos(h, [r'<section\b[^>]*id="lesson-focus"', r'<section\b[^>]*id="deep-understanding"',
                          r'<section\b[^>]*id="summary"'])
        if i == -1:
            return ''
        return h[:i] + blk + h[i:]
    op(cid, extra)

for cid, n in CORE_CLASS.items():
    def core(h, n=n):
        return add_class(h, 'class="slide-page"', 'core-knowledge-module', n)
    op(cid, core)

for cid in CONCEPTEST:
    def ce(h):
        if re.search(r'data-conceptest=["\']true["\']', h):
            return ''
        m = re.search(r'<section\b[^>]*(?:class="[^"]*tu-q[^"]*")?[^>]*>[\s\S]{0,1600}?data-answer=', h)
        k = m.start() if m else h.find('<section')
        if k == -1:
            return ''
        e = h.find('>', k)
        return h[:e] + ' data-conceptest="true"' + h[e:]
    op(cid, ce)

for cid, items in BLOOM_ADD.items():
    def bl(h, items=items):
        if len(set(re.findall(r"data-bloom-level=['\"]([^'\"]+)['\"]", h))) >= 3:
            return ''
        for marker, lvl in items:
            h = add_attr(h, marker, 'data-bloom-level="%s"' % lvl) or h
        return h
    op(cid, bl)

for cid, items in SCAFFOLD_ADD.items():
    def sc(h, items=items):
        if len(set(re.findall(r"data-scaffold=['\"]([^'\"]+)['\"]", h))) >= 2:
            return ''
        for marker, lvl in items:
            h = add_attr(h, marker, 'data-scaffold="%s"' % lvl) or h
        return h
    op(cid, sc)


def op_map(h):
    if 'data-teachany-map' in h:
        return ''
    i = first_pos(h, [r'<section\b[^>]*id="module-1"', r'<section\b[^>]*id="anchor"'])
    if i == -1:
        return ''
    return h[:i] + MAP_SEC + h[i:]


# ────────────────────────── 10. hero 主图 ──────────────────────────
HERO_CIDS = ['bio-cell-life', 'chem-m-oxygen-preparation', 'chn-e-picture-writing', 'eng-e-past-simple',
             'it-h-internet-applications', 'math-m-pythagorean-theorem', 'phy-m-heat-engine', 'sci-e-climate']


def hero_src(cid: str):
    d = ROOT / 'community' / cid / 'assets'
    for name in ('%s-hero.png' % cid, '%s-hero.webp' % cid, 'hero-infographic.png', 'hero-infographic.webp'):
        if (d / name).is_file():
            return './assets/' + name
    cands = sorted(p.name for p in d.glob('*hero*.png')) + sorted(p.name for p in d.glob('*hero*.webp'))
    return './assets/' + cands[0] if cands else ''


def make_hero_op(cid):
    def hero(h):
        if re.search(r'class="[^"]*hero-cover-img', h) or re.search(r'<img[^>]+src="[^"]*hero', h, re.I):
            return ''
        src = hero_src(cid)
        if not src:
            return ''
        title = re.search(r'<title>(.*?)</title>', h, re.S)
        alt = (re.sub(r'\s*·\s*TeachAny.*$', '', title.group(1)).strip() if title else cid) + ' 知识结构主图'
        img = ('\n<img class="hero-cover-img" src="%s" alt="%s" loading="eager" '
               'style="max-width:820px;width:100%%;margin:22px auto 0;display:block;border-radius:16px;'
               'box-shadow:0 10px 34px rgba(0,0,0,.32)">\n') % (src, alt)
        m = re.search(r'<(header|section|div)[^>]*class="[^"]*\bhero\b[^"]*"[^>]*>', h)
        if m:
            close = h.find('</%s>' % m.group(1), m.end())
            if close != -1:
                return h[:close] + img + h[close:]
        i = first_pos(h, [r'<section\b[^>]*id="hero-infographic"'])
        if i != -1:
            j = h.find('</section>', i)
            if j != -1:
                return h[:j] + img + h[j:]
        i = h.rfind('</body>')
        return h[:i] + img + h[i:] if i != -1 else ''
    return hero


for c in HERO_CIDS:
    op(c, make_hero_op(c))

op('history-medieval-europe', op_map)

for cid, (sid, title, body) in MODULE_ADD.items():
    def mod(h, sid=sid, title=title, body=body):
        if 'id="%s"' % sid in h:
            return ''
        blk = ('\n<section class="section core-knowledge-module text-module" id="%s" data-tts '
               'data-bloom-level="understand" data-scaffold="partial">\n'
               '<h2 class="section-title">%s</h2>\n%s\n</section>\n') % (sid, title, body)
        i = first_pos(h, [r'<section\b[^>]*id="deep-understanding"', r'<section\b[^>]*id="synthesis"',
                          r'<section\b[^>]*id="posttest"'])
        if i == -1:
            return ''
        return h[:i] + blk + h[i:]
    op(cid, mod)


def nav_hero_fix(h):
    """nav 里 href="#hero" 但页面只有 hero-infographic → 指向真实存在的锚点。"""
    if re.search(r'\sid="hero"', h) or 'id="hero-infographic"' not in h:
        return ''
    if 'href="#hero"' not in h:
        return ''
    return h.replace('href="#hero"', 'href="#hero-infographic"')


def dispatch(cid, h):
    for fn in OPS.get(cid, []):
        new = fn(h)
        if new:
            h = new
    return h


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', default='')
    args = ap.parse_args()

    # nav 断锚：先算出所有需要修锚点的课件
    nav_cids = []
    for d in sorted((ROOT / 'community').iterdir()):
        f = d / 'index.html'
        if not f.is_file():
            continue
        h = f.read_text(encoding='utf-8', errors='ignore')
        nav = re.search(r'<nav[^>]*>.*?</nav>', h, re.S)
        if not nav:
            continue
        miss = [x for x in re.findall(r'href="#([^"]+)"', nav.group(0))
                if x and not re.search(r'\sid="%s"' % re.escape(x), h)]
        if miss == ['hero']:
            nav_cids.append(d.name)
    print('nav 断锚（仅 #hero）：%d 门' % len(nav_cids))
    for cid in nav_cids:
        op(cid, nav_hero_fix)

    cids = sorted(OPS) if not args.only else [x.strip() for x in args.only.split(',') if x.strip()]
    ok = fail = skip = 0
    for cid in cids:
        f = ROOT / 'community' / cid / 'index.html'
        if not f.is_file():
            print('  ✗ 无文件', cid)
            fail += 1
            continue
        h = f.read_text(encoding='utf-8')
        new = dispatch(cid, h)
        if new == h or not new:
            skip += 1
            print('  ↷ %s: 无需改动' % cid)
            continue
        good, why = apply_guarded(f, new, cid)
        if good:
            ok += 1
        else:
            fail += 1
            print('  ✗ %s: %s' % (cid, why))
    print('完成：写入 %d，跳过 %d，失败 %d' % (ok, skip, fail))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
