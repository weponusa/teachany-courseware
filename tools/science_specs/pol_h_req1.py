# -*- coding: utf-8 -*-
"""高中思想政治 · 中国特色社会主义（必修1）—— 补齐知识树「中国特色社会主义」空缺

学科语气（思想政治）：从「中国为什么能走到今天」这个大问题切入，用人类社会发展的基本规律
做骨架，用史料与制度定位做证据；结论落在「为什么这样说、依据是什么」，不做口号式抒情、不背条文。

★ 政治表述红线（最高优先级，全课统一口径，任何地方不得含糊）：
  · 规范全称一律写准：习近平新时代中国特色社会主义思想、中国共产党领导是中国特色社会主义
    最本质的特征、中国特色社会主义制度、中国特色社会主义道路、社会主义初级阶段。
  · 必须明确：坚持中国共产党的领导，坚持中国特色社会主义道路；坚定道路自信、理论自信、
    制度自信、文化自信。
  · 我国社会主要矛盾的表述必须完整准确：人民日益增长的美好生活需要和不平衡不充分的发展
    之间的矛盾；同时明确我国仍处于并将长期处于社会主义初级阶段的基本国情没有变。
  · 经典著作只写规范名称与公认的发表时间（《共产党宣言》1848年发表），不臆造文件编号、
    不编造会议细节、不涉及敏感时政细节与人物评价。
  · 表述庄重、严谨、积极正面；插图不绘制国旗、国徽、党徽、领导人形象、地图，改用齿轮、
    上升阶梯、道路延伸、楼群剪影、火炬抽象符号等中性抽象图形。

内容落点（对应统编必修1《中国特色社会主义》四课）：
  ① 社会主义从空想到科学、从理论到实践的发展：生产力与生产关系、经济基础与上层建筑的
     矛盾运动是人类社会发展的基本规律；人类社会形态由低级向高级更替；唯物史观和剩余价值
     学说使社会主义由空想变为科学。
  ② 只有社会主义才能救中国：新民主主义革命的胜利；社会主义制度在中国的确立。
  ③ 只有中国特色社会主义才能发展中国：伟大的改革开放；中国特色社会主义的创立和发展。
  ④ 只有坚持和发展中国特色社会主义才能实现中华民族伟大复兴：中国特色社会主义进入新时代；
     实现中华民族伟大复兴的中国梦；习近平新时代中国特色社会主义思想。

三个互动台子都能真操作：
  动手一 = 「社会发展阶段时间轴」（按时间先后依次点出五个社会形态节点，点错给顺序提示）；
  ★核心模拟 动手二 = 「概念辨析台」（六个易混概念 × 六条准确表述）；
  综合任务 = 「社会主要矛盾判断台」（四个现象判断归属哪一方面，合成方位卡）。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-h-req1"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "先看一个问题。今天我们用着手机、坐着高铁、住着高楼，可一百多年前的中国，还在为能不能活下去、能不能站起来而苦苦挣扎。这中间到底发生了什么？为什么说只有社会主义才能救中国，又为什么必须走中国特色社会主义道路？这节课我们沿着人类社会发展的基本规律一路看下来，把中国特色社会主义从哪里来、现在在哪里、要往哪里去弄清楚。",
    "problem-anchor": "开始之前，先选一个你真正想弄清的问题：人类社会为什么会一步一步往前走？社会主义是怎样从一种设想变成科学的？中国为什么选择了社会主义道路？还是今天的中国正处在一个什么样的历史方位？选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出生产力与生产关系、经济基础与上层建筑的矛盾运动是人类社会发展的基本规律，能按时间先后说出人类社会形态的更替。第二，能说出唯物史观和剩余价值学说使社会主义由空想变为科学，知道《共产党宣言》的发表标志着科学社会主义的诞生。第三，能说明只有社会主义才能救中国、只有中国特色社会主义才能发展中国，明确中国共产党领导是中国特色社会主义最本质的特征，必须坚持中国共产党的领导、坚持中国特色社会主义道路。第四，能说出我国社会主要矛盾已经转化为人民日益增长的美好生活需要和不平衡不充分的发展之间的矛盾，知道新时代坚持和发展中国特色社会主义的总任务。",
    "pretest": "先做三道小题，用你现在的理解选就行。选完马上能看到解释，选得不准也没关系，正好知道要重点听哪里。",
    "module-1": "第一件事，人类社会发展的基本规律。生产力与生产关系、经济基础与上层建筑的矛盾运动，是人类社会发展的基本规律。把它拆成两层看。第一层，生产力决定生产关系：生产力是最活跃、最革命的因素，有什么样的生产力，就要求有什么样的生产关系与之相适应。第二层，生产关系反作用于生产力：生产关系适合生产力状况的时候，就会促进生产力发展；不适合的时候，就会阻碍生产力发展。由此得出两条客观规律：生产关系一定要适应生产力状况，上层建筑一定要适应经济基础状况。也正因为如此，人类社会才由原始社会、奴隶社会、封建社会、资本主义社会一路走到社会主义社会，由低级向高级不断发展。这里有一个常见错误要避开：有的同学误认为社会形态的更替可以随意跳过、由谁想出来就能定下来，其实它是由生产力发展水平决定的客观过程，不以人的主观意志为转移。",
    "lab-1": "现在请你亲手排一条时间轴。下面有五个社会形态的节点，顺序被打乱了。请按时间先后，从最早的社会形态开始点。点对了，会告诉你这个阶段的生产力状况和生产关系特点；点错了，我会提醒你顺序的问题。五个都点出来以后，你会看到一条完整的社会形态更替路线。",
    "module-2": "第二件事，科学社会主义的创立与实践。空想社会主义者看到了资本主义的弊病，也提出了许多美好的设想，但他们没有找到实现理想社会的现实道路和依靠力量。马克思、恩格斯创立了唯物史观和剩余价值学说，揭示了人类社会发展的一般规律和资本主义运行的特殊规律，使社会主义由空想变为科学。一八四八年《共产党宣言》发表，标志着科学社会主义的诞生。一九一七年十月革命建立了世界上第一个社会主义国家，实现了科学社会主义从理论到现实的历史性飞跃。再看中国：一九二一年中国共产党成立，一经成立就把实现共产主义作为最高理想和最终目标；一九四九年中华人民共和国成立，实现了民族独立、人民解放；一九五六年社会主义改造基本完成，确立了社会主义基本制度，完成了中国历史上最深刻最伟大的社会变革。结论就是那句话：只有社会主义才能救中国。",
    "lab-2": "接下来是这个模块最重要的一个台子：概念辨析台。左边是六个容易混在一起的概念，右边是六条准确的表述，顺序被打乱了。先点一个概念，再点你认为对应的那条表述。配对了，我会把这条表述的准确意思和依据讲一遍；配错了，我会告诉你容易混在哪里，还可以怎么区分。",
    "worked-example": "我们一起当一次校对员。某校时事小组整理出四条关于新时代的表述，请你判断。第一条，中国特色社会主义进入新时代，这是我国发展新的历史方位。这一条准确。第二条，我国社会主要矛盾已经转化为人民日益增长的美好生活需要和不平衡不充分的发展之间的矛盾。这一条准确。第三条，新时代坚持和发展中国特色社会主义的总任务是实现社会主义现代化和中华民族伟大复兴。这一条准确。第四条，进入新时代意味着我国已经不再处于社会主义初级阶段。这一条必须改。进入新时代，我国仍处于并将长期处于社会主义初级阶段的基本国情没有变，我国是世界最大发展中国家的国际地位没有变。这里还有一个必须说清楚的要点：中国共产党领导是中国特色社会主义最本质的特征，中国共产党是最高政治领导力量。坚持和发展中国特色社会主义，必须坚持中国共产党的领导，必须坚持中国特色社会主义道路。",
    "conceptest-1": "接下来用三道题考考你，每道题里都藏着一个容易想歪的地方。读一读，选一个你认为准确的，再看解释。",
    "synthesis": "最后一件任务交给你：做一次社会主要矛盾的判断练习。下面有四个现象，请你分别判断它主要说明的是人民日益增长的美好生活需要，还是不平衡不充分的发展。四个都判断完，你会得到一张属于自己的方位卡。",
    "posttest": "最后一轮，换几个新情境来考考你。这次会出现社会主义制度的确立、改革开放和中国梦，看看今天学的东西还用不用得上。",
    "summary": "这节课我们弄清楚四件事。第一，生产力与生产关系、经济基础与上层建筑的矛盾运动，是人类社会发展的基本规律；生产关系一定要适应生产力状况，上层建筑一定要适应经济基础状况。第二，唯物史观和剩余价值学说使社会主义由空想变为科学，《共产党宣言》的发表标志着科学社会主义的诞生；只有社会主义才能救中国。第三，改革开放是党和人民大踏步赶上时代的重要法宝，只有中国特色社会主义才能发展中国；中国共产党领导是中国特色社会主义最本质的特征，必须坚持中国共产党的领导、坚持中国特色社会主义道路。第四，中国特色社会主义进入新时代，这是我国发展新的历史方位；我国社会主要矛盾已经转化为人民日益增长的美好生活需要和不平衡不充分的发展之间的矛盾，新时代坚持和发展中国特色社会主义的总任务是实现社会主义现代化和中华民族伟大复兴。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出人类社会发展的两条客观规律，并按时间先后写出人类社会形态的更替。第二层能力应用，动手做：用一段话说明为什么说只有社会主义才能救中国，把新民主主义革命的胜利和社会主义制度在中国的确立这两件事写进去。第三层迁移挑战，选做：结合自己的生活观察，举一个例子说明我国社会主要矛盾已经转化的表现，并写清楚为什么说我国仍处于并将长期处于社会主义初级阶段。",
    "knowledge-graph": "这张图展示了这节课在思想政治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域里的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 人类社会发展的基本规律", "lab-1": "动手一 社会发展阶段时间轴",
    "module-2": "概念二 科学社会主义的创立与实践", "lab-2": "动手二 概念辨析台（核心模拟）",
    "worked-example": "例题示范 新时代的历史方位与总任务", "conceptest-1": "概念测试",
    "synthesis": "综合任务 社会主要矛盾判断台", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：社会发展阶段时间轴（五个社会形态，必须按时间先后点出） ──
NODES = [
    {"k": "n1", "n": "原始社会",
     "detail": "<p style=\"margin:6px 0 0\"><strong>生产力状况：</strong>生产力水平极为低下，人们主要使用石器，以采集和狩猎为生。</p>"
               "<p style=\"margin:6px 0 0\"><strong>生产关系特点：</strong>生产资料归氏族公有，人们共同劳动、共同占有生产资料、平均分配劳动产品，没有剥削，也没有阶级。</p>"
               "<p style=\"margin:6px 0 0\"><strong>历史地位：</strong>这是人类社会发展的最初阶段。</p>"},
    {"k": "n2", "n": "奴隶社会",
     "detail": "<p style=\"margin:6px 0 0\"><strong>生产力状况：</strong>金属工具得到广泛使用，生产力有了较大发展，脑力劳动和体力劳动开始分工。</p>"
               "<p style=\"margin:6px 0 0\"><strong>生产关系特点：</strong>生产资料由氏族公有变为奴隶主私有，奴隶主占有全部生产资料并完全占有奴隶，奴隶毫无人身自由。</p>"
               "<p style=\"margin:6px 0 0\"><strong>历史地位：</strong>奴隶社会是人类历史上第一个阶级社会，也是人类文明的开端。</p>"},
    {"k": "n3", "n": "封建社会",
     "detail": "<p style=\"margin:6px 0 0\"><strong>生产力状况：</strong>铁制农具得到广泛使用，耕作技术提高，生产力进一步发展。</p>"
               "<p style=\"margin:6px 0 0\"><strong>生产关系特点：</strong>在封建土地所有制下，地主阶级占有绝大部分土地，农民有一定的人身自由，但被束缚在土地上，地主通过收取地租等方式剥削农民。</p>"
               "<p style=\"margin:6px 0 0\"><strong>历史地位：</strong>封建制生产关系代替奴隶制生产关系，适应了当时生产力发展的要求。</p>"},
    {"k": "n4", "n": "资本主义社会",
     "detail": "<p style=\"margin:6px 0 0\"><strong>生产力状况：</strong>机器大工业的出现带来了生产力的巨大飞跃，社会化大生产迅速发展。</p>"
               "<p style=\"margin:6px 0 0\"><strong>生产关系特点：</strong>资本家占有生产资料，工人靠出卖劳动力获得工资，资本家占有工人创造的剩余价值。</p>"
               "<p style=\"margin:6px 0 0\"><strong>历史地位：</strong>资本主义社会创造了以往任何时代都无法比拟的生产力，但生产社会化和生产资料资本主义私人占有之间的矛盾无法克服。</p>"},
    {"k": "n5", "n": "社会主义社会",
     "detail": "<p style=\"margin:6px 0 0\"><strong>生产力状况：</strong>社会化大生产的发展，要求生产资料由社会共同占有与之相适应。</p>"
               "<p style=\"margin:6px 0 0\"><strong>生产关系特点：</strong>劳动者共同占有生产资料，实行按劳分配；社会主义生产关系更能适应社会化大生产的要求。</p>"
               "<p style=\"margin:6px 0 0\"><strong>历史地位：</strong>社会主义终将代替资本主义，这是历史发展的必然趋势；在中国，社会主义制度的确立完成了中国历史上最深刻最伟大的社会变革。</p>"},
]

# ── 动手二（★核心模拟）：概念辨析台（六个易混概念 × 六条准确表述） ──
CONCEPTS = [
    {"k": "c1", "n": "空想社会主义", "hook": "最早的一批设想者",
     "def": "看到了资本主义的弊病，但没有找到实现理想社会的现实道路和依靠力量。",
     "why": "空想社会主义者对未来社会提出了许多美好的设想，但没有揭示社会发展的客观规律，"
            "也没有找到变革社会的正确道路和依靠力量，所以只能停留在空想。",
     "tip": "还可以试试：把它和科学社会主义在「理论基础」和「依靠力量」两方面各比一句。"},
    {"k": "c2", "n": "科学社会主义", "hook": "从空想到科学的飞跃",
     "def": "以唯物史观和剩余价值学说为理论基石，揭示了人类社会发展的一般规律和资本主义运行的特殊规律，使社会主义由空想变为科学。",
     "why": "有了唯物史观和剩余价值学说这两块理论基石，社会主义才有了科学依据；"
            "一八四八年《共产党宣言》发表，标志着科学社会主义的诞生。",
     "tip": "还可以试试：分别用一句话说清唯物史观、剩余价值学说各自揭示了什么。"},
    {"k": "c3", "n": "新民主主义革命", "hook": "救中国的第一步",
     "def": "在中国共产党领导下，推翻帝国主义、封建主义、官僚资本主义的统治，实现民族独立、人民解放。",
     "why": "一九四九年中华人民共和国成立，标志着新民主主义革命取得了伟大胜利，"
            "中国人民从此站起来了，为走上社会主义道路创造了前提。",
     "tip": "还可以试试：把「民族独立、人民解放」这八个字背后解决了什么问题讲一遍。"},
    {"k": "c4", "n": "社会主义制度在中国的确立", "hook": "最深刻最伟大的社会变革",
     "def": "一九五六年社会主义改造基本完成，确立了社会主义基本制度，完成了中国历史上最深刻最伟大的社会变革。",
     "why": "社会主义制度的确立，使中国走上了社会主义道路，为当代中国一切发展进步"
            "奠定了根本政治前提和制度基础。",
     "tip": "还可以试试：把它和新民主主义革命的胜利分开说——一件事解决「站起来」，一件事确立制度。"},
    {"k": "c5", "n": "改革开放", "hook": "赶上时代的重要法宝",
     "def": "党的十一届三中全会开启了改革开放和社会主义现代化建设新时期；改革开放是党和人民大踏步赶上时代的重要法宝，是坚持和发展中国特色社会主义的必由之路。",
     "why": "改革开放极大解放和发展了社会生产力，使中国大踏步赶上了时代；"
            "中国特色社会主义正是在改革开放中创立、发展和完善起来的。",
     "tip": "还可以试试：想一想改革开放以来，你家里哪一件东西的变化最能说明问题。"},
    {"k": "c6", "n": "中国特色社会主义进入新时代", "hook": "我国发展新的历史方位",
     "def": "党的十八大以来，中国特色社会主义进入新时代，这是我国发展新的历史方位；我国社会主要矛盾已经转化为人民日益增长的美好生活需要和不平衡不充分的发展之间的矛盾。",
     "why": "进入新时代，我国仍处于并将长期处于社会主义初级阶段的基本国情没有变，"
            "我国是世界最大发展中国家的国际地位没有变。",
     "tip": "还可以试试：把「主要矛盾变了」和「基本国情没变」这两句话放在一起，说清它们的区别。"},
]

# ── 综合任务：社会主要矛盾判断台 ──
PHEN = [
    {"k": "p1", "t": "人们对更好的教育、更稳定的工作、更满意的收入、更可靠的社会保障有了新的期待。",
     "ans": "need",
     "why": "这是人民对美好生活的需要在不断增长、不断提升，说明我们的发展要更好地回应人民的期待。"},
    {"k": "p2", "t": "城乡之间、区域之间的发展水平还存在明显差距。",
     "ans": "dev",
     "why": "差距说明发展还不平衡，这正是「不平衡不充分的发展」这一方面要着力解决的问题。"},
    {"k": "p3", "t": "优质医疗资源集中在少数大城市，基层医疗服务还比较薄弱。",
     "ans": "dev",
     "why": "资源分布不均衡、基层供给不充分，属于发展不平衡不充分的表现。"},
    {"k": "p4", "t": "人们希望天更蓝、水更清、空气更清新，对优美生态环境的需要日益增长。",
     "ans": "need",
     "why": "优美的生态环境是美好生活需要的重要内容，反映出人民对生活质量的新期待。"},
]

CUSTOM_JS = r"""
/* ============================================================
   pol-h-req1 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 「社会发展阶段时间轴」：五个社会形态按时间先后依次点出
   3) ★「概念辨析台」：六个易混概念 × 六条准确表述
   4) 「社会主要矛盾判断台」：四个现象 → 归属哪一方面 → 合成方位卡
   ============================================================ */
(function () {
  'use strict';

  /* ---------- 1. 选择题 ---------- */
  document.querySelectorAll('[data-quiz-block]').forEach(function (block) {
    block.querySelectorAll('.choice').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (block.dataset.answered === '1') return;
        block.dataset.answered = '1';
        var ok = btn.dataset.correct === '1';
        btn.classList.add(ok ? 'correct' : 'wrong');
        block.querySelectorAll('.choice').forEach(function (b) {
          if (b.dataset.correct === '1') b.classList.add('correct');
          b.disabled = true;
        });
        var ex = block.querySelector('[data-explain]');
        if (ex) ex.style.display = 'block';
      });
    });
  });

  /* ---------- 2. 社会发展阶段时间轴 ---------- */
  var NODES = __NODES_JSON__;
  var tlStage = document.getElementById('tl-stage');
  if (tlStage) {
    var done = 0;
    var out1 = document.getElementById('tl-out');
    var nodesBox = document.getElementById('tl-nodes');
    var board1 = document.getElementById('tl-board');
    function render1() {
      nodesBox.innerHTML = '';
      NODES.forEach(function (N, i) {
        var b = document.createElement('button');
        b.className = 'choice' + (i < done ? ' correct' : '');
        b.style.textAlign = 'center';
        b.style.flex = '0 0 auto';
        b.style.minWidth = '112px';
        b.innerHTML = '<strong>' + (i + 1) + '. ' + N.n + '</strong>' +
          (i < done ? '<br><span style="color:var(--accent-deep);font-size:13px">已点出 ✓</span>' : '');
        b.addEventListener('click', function () {
          if (i < done) {
            out1.className = 'result';
            out1.innerHTML = '<strong>' + N.n + '（第 ' + (i + 1) + ' 个阶段）</strong>' + N.detail;
            return;
          }
          if (i > done) {
            out1.className = 'result warn';
            out1.innerHTML = '<strong>顺序不对。</strong>人类社会形态的更替有先后次序，' +
              '请按时间先后、从最早的社会形态开始点。' +
              '<br><span style="color:var(--muted)">常见错误：把顺序记乱，或者<strong>误认为</strong>社会形态可以跳过中间环节随意更替。</span>';
            return;
          }
          done = i + 1;
          out1.className = 'result';
          out1.innerHTML = '<strong>' + N.n + '</strong>' + N.detail;
          if (done === NODES.length) {
            out1.innerHTML += '<br><p style="margin:10px 0 0"><strong>五个阶段都点出来了。</strong>' +
              '从原始社会到社会主义社会，每一次更替的背后都是生产力发展的推动：' +
              '生产关系一定要适应生产力状况，上层建筑一定要适应经济基础状况。' +
              '这就是人类社会发展的基本规律，它不以人的主观意志为转移。</p>';
          }
          render1();
        });
        nodesBox.appendChild(b);
      });
      board1.textContent = '已经点出 ' + done + ' / ' + NODES.length + ' 个阶段';
    }
    render1();
  }

  /* ---------- 3. ★ 概念辨析台 ---------- */
  var CON = __CONCEPTS_JSON__;
  var MATCH = __MATCHES_JSON__;
  var cpStage = document.getElementById('cp-stage');
  if (cpStage) {
    var selC = null;
    var paired = {};
    var out2 = document.getElementById('cp-out');
    var conBox = document.getElementById('cp-left');
    var matBox = document.getElementById('cp-right');
    var board2 = document.getElementById('cp-board');
    function conByKey(k) {
      for (var i = 0; i < CON.length; i++) { if (CON[i].k === k) return CON[i]; }
      return null;
    }
    function render2() {
      conBox.innerHTML = '';
      CON.forEach(function (C) {
        var b = document.createElement('button');
        b.className = 'choice' + (paired[C.k] ? ' correct' : (selC === C.k ? ' selected' : ''));
        b.style.textAlign = 'left';
        b.innerHTML = '<strong>' + C.n + '</strong><br><span style="color:var(--muted);font-size:14px">' + C.hook + '</span>' +
          (paired[C.k] ? '<br><span style="color:var(--accent-deep);font-size:14px">已配上准确表述 ✓</span>' : '');
        b.addEventListener('click', function () {
          if (paired[C.k]) return;
          selC = C.k;
          out2.className = 'result warn';
          out2.innerHTML = '<strong>你选了「' + C.n + '」。</strong>现在到右边点一条你认为对应的准确表述。';
          render2();
        });
        conBox.appendChild(b);
      });
      matBox.innerHTML = '';
      MATCH.forEach(function (M) {
        var b = document.createElement('button');
        b.className = 'choice' + (paired[M.k] ? ' correct' : '');
        b.style.textAlign = 'left';
        b.innerHTML = M.def + (paired[M.k] ? '<br><span style="color:var(--accent-deep);font-size:14px">配对成功 ✓</span>' : '');
        b.addEventListener('click', function () {
          if (paired[M.k]) return;
          if (!selC) {
            out2.className = 'result warn';
            out2.innerHTML = '先到左边点一个概念，再回到右边点表述。' +
              '<br><span style="color:var(--muted)">还可以试试：先想这个概念最关键的一件事是什么，再去找写着这件事的那条表述。</span>';
            return;
          }
          if (selC === M.k) {
            var C0 = conByKey(selC);
            paired[M.k] = true;
            selC = null;
            out2.className = 'result';
            out2.innerHTML = '<strong>配对成功：' + C0.n + '</strong>' + M.why +
              '<br><span style="color:var(--muted)">' + C0.tip + '</span>';
            if (Object.keys(paired).length === MATCH.length) {
              out2.innerHTML += '<br><br><strong>六组都配对了。</strong>' +
                '从空想到科学、从理论到实践，从救中国到发展中国，再到进入新时代——' +
                '这几个概念连起来，就是中国特色社会主义从哪里来、现在在哪里的完整线索。';
            }
          } else {
            var C1 = conByKey(selC);
            out2.className = 'result warn';
            out2.innerHTML = '<strong>这条表述说的不是「' + C1.n + '」。</strong>' +
              '这样可能会：把几个概念<strong>搞混</strong>，考试时写串。' + C1.tip +
              '<br><span style="color:var(--muted)">你选的概念是：' + C1.n + '。</span>';
          }
          render2();
        });
        matBox.appendChild(b);
      });
      board2.textContent = '辨析进度 ' + Object.keys(paired).length + ' / ' + MATCH.length + ' 组';
    }
    render2();
  }

  /* ---------- 4. 社会主要矛盾判断台 ---------- */
  var PHEN = __PHEN_JSON__;
  var pmStage = document.getElementById('pm-stage');
  if (pmStage) {
    var selP = null;
    var judged = {};
    var out3 = document.getElementById('pm-out');
    var phenBox = document.getElementById('pm-list');
    var board3 = document.getElementById('pm-board');
    var LABEL = { need: '人民日益增长的美好生活需要', dev: '不平衡不充分的发展' };
    function render3() {
      phenBox.innerHTML = '';
      PHEN.forEach(function (P, i) {
        var b = document.createElement('button');
        b.className = 'choice' + (judged[P.k] ? ' correct' : (selP === P.k ? ' selected' : ''));
        b.style.textAlign = 'left';
        b.innerHTML = '<strong>' + (i + 1) + '.</strong> ' + P.t +
          (judged[P.k] ? '<br><span style="color:var(--accent-deep);font-size:14px">已判断：' + LABEL[P.ans] + ' ✓</span>' : '');
        b.addEventListener('click', function () {
          if (judged[P.k]) { selP = P.k; render3(); return; }
          selP = P.k;
          out3.className = 'result warn';
          out3.innerHTML = '<strong>你选了第 ' + (i + 1) + ' 个现象。</strong>现在到下面选它主要说明的是哪一方面。';
          render3();
        });
        phenBox.appendChild(b);
      });
      board3.textContent = '已判断 ' + Object.keys(judged).length + ' / ' + PHEN.length + ' 个现象';
    }
    render3();
    document.querySelectorAll('[data-pm-ans]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (!selP) {
          out3.className = 'result warn';
          out3.innerHTML = '先在上面点一个现象，再判断它属于哪一方面。' +
            '<br><span style="color:var(--muted)">还可以试试：先问自己一句，这句话说的是「人们想要什么」，还是「发展还有哪些短板」。</span>';
          return;
        }
        var P = null;
        for (var i = 0; i < PHEN.length; i++) { if (PHEN[i].k === selP) P = PHEN[i]; }
        var pick = btn.dataset.pmAns;
        if (pick === P.ans) {
          judged[P.k] = true;
          out3.className = 'result';
          out3.innerHTML = '<strong>判断准确：' + LABEL[P.ans] + '。</strong>' + P.why;
          if (Object.keys(judged).length === PHEN.length) {
            out3.innerHTML += '<br><br><strong>四个现象都判断完了，这就是你的方位卡。</strong>' +
              '我国社会主要矛盾已经转化为人民日益增长的美好生活需要和不平衡不充分的发展之间的矛盾。' +
              '同时要记住：主要矛盾的变化，并没有改变我国仍处于并将长期处于社会主义初级阶段的基本国情，' +
              '我国是世界最大发展中国家的国际地位也没有变。';
          }
          selP = null;
        } else {
          out3.className = 'result warn';
          out3.innerHTML = '<strong>再想一想：这个现象更说明「' + LABEL[P.ans] + '」。</strong>' +
            '常见错误：把「人民的需要」和「发展的短板」<strong>搞混</strong>。' +
            '人们想要什么，指向的是需要那一面；供给还不够好、分布还不够均衡，指向的是发展那一面。';
        }
        render3();
      });
    });
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__NODES_JSON__', json.dumps(NODES, ensure_ascii=False))
             .replace('__CONCEPTS_JSON__', json.dumps(CONCEPTS, ensure_ascii=False))
             .replace('__MATCHES_JSON__', json.dumps(
                 [CONCEPTS[3], CONCEPTS[0], CONCEPTS[5], CONCEPTS[1], CONCEPTS[4], CONCEPTS[2]],
                 ensure_ascii=False))
             .replace('__PHEN_JSON__', json.dumps(PHEN, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：人类社会为什么会往前走？", TTS["pretest"], [
        {"q": "推动人类社会形态由低级向高级不断发展的根本原因是：",
         "options": [("生产力的发展以及生产力与生产关系的矛盾运动", True),
                     ("少数人物的主观愿望", False),
                     ("自然环境的偶然变化", False)],
         "explain": "生产力与生产关系、经济基础与上层建筑的矛盾运动，是人类社会发展的基本规律。"
                    "<strong>错因提醒：</strong>常见错误是<strong>误认为</strong>社会形态更替由人的主观意愿决定。"
                    "其实生产关系一定要适应生产力状况、上层建筑一定要适应经济基础状况，是不以人的意志为转移的客观规律。",},
        {"q": "使社会主义由空想变为科学的两块理论基石是：",
         "options": [("唯物史观和剩余价值学说", True),
                     ("空想社会主义和平均主义", False),
                     ("地理环境决定论和人口理论", False)],
         "explain": "马克思、恩格斯创立了唯物史观和剩余价值学说，揭示了人类社会发展的一般规律和资本主义运行的特殊规律，"
                    "从而使社会主义由空想变为科学。"
                    "<strong>错因提醒：</strong>有的同学把空想社会主义也当成理论基础，这是<strong>搞混</strong>了"
                    "「空想」与「科学」的分界——空想社会主义没有找到现实道路和依靠力量。",},
        {"q": "关于今天的中国，下面哪一句表述是准确的？",
         "options": [("中国特色社会主义进入新时代，我国社会主要矛盾已经转化为人民日益增长的美好生活需要和不平衡不充分的发展之间的矛盾", True),
                     ("进入新时代，我国已经不再处于社会主义初级阶段", False),
                     ("新时代坚持和发展中国特色社会主义的总任务是全面深化改革", False)],
         "explain": "中国特色社会主义进入新时代，这是我国发展新的历史方位；我国社会主要矛盾已经转化为"
                    "人民日益增长的美好生活需要和不平衡不充分的发展之间的矛盾。"
                    "<strong>错因提醒：</strong>常见的<strong>误认为</strong>是「进入新时代就等于跨越了社会主义初级阶段」。"
                    "事实上，我国仍处于并将长期处于社会主义初级阶段的基本国情没有变。",}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "人类社会发展的基本规律：生产力与生产关系的矛盾运动", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(251,191,36,.6)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们已经知道人类社会经历过不同的社会形态（And）；但为什么会这样一步一步变化、背后有没有规律可循（But）；所以这节课先弄清人类社会发展的基本规律，再来看中国特色社会主义从哪里来（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px"><strong>生产力与生产关系、经济基础与上层建筑的矛盾运动，是人类社会发展的基本规律。</strong></p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>生产力决定生产关系：</strong>生产力是最活跃、最革命的因素，有什么样的生产力，就要求有什么样的生产关系与之相适应。</div></div>
          <div class="step"><span class="n">2</span><div><strong>生产关系反作用于生产力：</strong>生产关系适合生产力状况时促进生产力发展，不适合时阻碍生产力发展。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>两条客观规律：</strong>生产关系一定要适应生产力状况，上层建筑一定要适应经济基础状况。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="人类社会形态更替时间轴抽象示意图：原始社会、奴隶社会、封建社会、资本主义社会、社会主义社会五个阶段自左向右逐级上升，每一级标注生产力状况与生产关系特点要点，用齿轮、上升阶梯等抽象符号表示，附中文标注">
          <figcaption>概念图：随着生产力发展，人类社会形态由低级向高级不断发展 · 抽象示意图，不按比例</figcaption>
        </figure>
        <div class="inner-card">
          <p><strong>一条主线串起来</strong></p>
          <p style="color:var(--muted)">原始社会 → 奴隶社会 → 封建社会 → 资本主义社会 → 社会主义社会。每一次更替都不是谁规定的，而是生产力发展到一定程度、旧的生产关系再也装不下新的生产力之后的结果。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>社会形态的更替可以随意跳过、由谁想出来就能定下来；也有的同学把「社会形态更替」与「同一社会形态内部的调整」<strong>搞混</strong>。前者是根本性质的变革，后者不改变社会形态的性质。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "同一块土地上，用石器种地和用铁犁种地，能养活的人完全不同——工具的每一次进步，都会把旧的生产关系顶得松动。"},
    {"lens": "解释它", "text": "为什么生产关系落后了就必须变？因为它束缚了劳动者的积极性，也容纳不下新的生产工具。装不下的东西，最后一定会被换掉。"},
    {"lens": "迁移它", "text": "这条规律不只属于过去。今天的新技术、新产业不断出现，我们的制度也在不断完善——道理是同一个：让制度跟上生产力的脚步。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：社会发展阶段时间轴，按时间先后点出来", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">下面是五个社会形态的节点，<strong>顺序被打乱了</strong>。请按时间先后，从最早的社会形态开始点。</p>
        <div class="lab-panel">
          <div id="tl-stage">
            <div style="font-weight:700;font-size:14px;margin-bottom:8px">点击节点排出时间轴（点错顺序会给提示）</div>
            <div class="flex-row" id="tl-nodes" style="margin-top:0"></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">时间轴进度</span><span class="v" id="tl-board">已经点出 0 / 5 个阶段</span></div>
          </div>
          <p class="result warn" id="tl-out" style="margin-top:12px">从最早的社会形态开始点。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">⚙️</span><div><strong>点完回头看：</strong>五个阶段排成一条线以后，请你想一句话——把这条线连起来的力量，究竟是什么？答案就是前面那条基本规律。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "科学社会主义的创立与实践：只有社会主义才能救中国", TTS["module-2"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(251,191,36,.6)">
          <p><strong>为什么要弄清这一段？</strong></p>
          <p style="color:var(--muted)">我们已经知道社会发展有规律（And）；但社会主义是怎样从一种美好的设想变成科学的，又是怎样在中国落地生根的（But）；所以这节课要把「从空想到科学、从理论到实践」这条线索理清（Therefore）。</p>
        </div>
        <div class="inner-card">
          <p><strong>从空想到科学</strong></p>
          <p style="color:var(--muted)">空想社会主义者看到了资本主义的弊病，却没有找到实现理想社会的现实道路和依靠力量。唯物史观和剩余价值学说的创立，使社会主义由空想变为科学。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>理论诞生：</strong>一八四八年《共产党宣言》发表，标志着科学社会主义的诞生。</div></div>
          <div class="step"><span class="n">2</span><div><strong>理论到现实：</strong>一九一七年十月革命建立了世界上第一个社会主义国家，实现了科学社会主义从理论到现实的历史性飞跃。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>中国道路：</strong>一九二一年中国共产党成立，一经成立就把实现共产主义作为最高理想和最终目标；一九四九年中华人民共和国成立，实现了民族独立、人民解放。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>制度确立：</strong>一九五六年社会主义改造基本完成，确立了社会主义基本制度，完成了中国历史上最深刻最伟大的社会变革。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="「只有社会主义才能救中国、只有中国特色社会主义才能发展中国」两段式进程抽象示意图：左侧用上升阶梯与火炬抽象符号表示从空想到科学、从理论到实践，右侧用延伸道路与楼群剪影表示改革开放与现代化建设，各阶段附中文标注，不含国旗国徽与地图">
          <figcaption>示意：从科学社会主义的创立，到社会主义制度在中国的确立，再到中国特色社会主义的开创与发展 · 抽象示意图，不按比例</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>社会主义只是一种美好愿望、没有现实依据；也有的同学把《共产党宣言》的发表与十月革命<strong>搞混</strong>——前者标志着科学社会主义的诞生，后者实现了从理论到现实的历史性飞跃。</p>
        </div>
{insight_box([
    {"lens": "比较它", "text": "空想社会主义者和马克思、恩格斯看到的都是同一件坏事，区别在于：一个只说了「不应该这样」，另一个说清了「为什么会这样、靠谁去改变」。"},
    {"lens": "解释它", "text": "为什么说只有社会主义才能救中国？因为近代以来各种救国方案都没能改变旧中国的命运，而新民主主义革命的胜利和社会主义制度的确立，真正实现了民族独立、人民解放。"},
    {"lens": "迁移它", "text": "这个道理今天仍然成立：判断一条道路行不行，不看它听起来多漂亮，而看它能不能解决这个国家当时最要紧的问题。"},
])}
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "★动手二：概念辨析台——把易混概念配到准确表述", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点左边一个<strong>概念</strong>，再点右边一条你认为对应的<strong>准确表述</strong>。配对了会给出依据，配错了会告诉你容易混在哪里。</p>
        <div class="lab-panel">
          <div id="cp-stage">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">点击左侧概念，再点右侧准确表述进行配对</div>
            <div class="grid grid-2">
              <div id="cp-left"></div>
              <div id="cp-right"></div>
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">辨析进度</span><span class="v" id="cp-board">辨析进度 0 / 6 组</span></div>
          </div>
          <p class="result warn" id="cp-out" style="margin-top:12px">先点左边一个概念。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧭</span><div><strong>辨析完再连一遍：</strong>空想社会主义 → 科学社会主义 → 新民主主义革命 → 社会主义制度的确立 → 改革开放 → 进入新时代。这条线就是本课的主干，也是中国特色社会主义从哪里来的答案。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：新时代的历史方位与总任务，四条表述逐条校对", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(251,191,36,.6)">
          <p style="margin:0"><strong>情境：</strong>某校时事小组整理出四条关于新时代的表述。请你当一次校对员，判断哪一条准确、哪一条必须改，并说明依据。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>第一条（准确）：</strong>中国特色社会主义进入新时代，这是我国发展新的历史方位。</div></div>
          <div class="step"><span class="n">2</span><div><strong>第二条（准确）：</strong>我国社会主要矛盾已经转化为人民日益增长的美好生活需要和不平衡不充分的发展之间的矛盾。</div></div>
          <div class="step"><span class="n">3</span><div><strong>第三条（准确）：</strong>新时代坚持和发展中国特色社会主义的总任务是实现社会主义现代化和中华民族伟大复兴。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>第四条（必须改）：</strong>「进入新时代意味着我国已经不再处于社会主义初级阶段。」——我国仍处于并将长期处于社会主义初级阶段的基本国情没有变，我国是世界最大发展中国家的国际地位没有变。</div></div>
        </div>
        <div class="inner-card">
          <p><strong>两条必须站得住的结论</strong></p>
          <p style="color:var(--muted)">中国共产党领导是中国特色社会主义最本质的特征，中国共产党是最高政治领导力量。坚持和发展中国特色社会主义，必须坚持中国共产党的领导，必须坚持中国特色社会主义道路。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">最常见的两个错误：一是<strong>误认为</strong>进入新时代就跨越了社会主义初级阶段；二是把「社会主要矛盾的变化」和「基本国情的变化」<strong>搞混</strong>——主要矛盾变了，基本国情没有变，这两句话必须同时说清楚。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三句话，藏着三个容易想歪的地方", TTS["conceptest-1"], [
        {"q": "关于人类社会发展的基本规律，下面哪一句表述准确？",
         "options": [("生产关系一定要适应生产力状况，上层建筑一定要适应经济基础状况", True),
                     ("社会形态的更替取决于人的主观愿望", False),
                     ("生产力越发展，社会形态就越落后", False)],
         "explain": "生产关系一定要适应生产力状况、上层建筑一定要适应经济基础状况，是社会发展的客观规律。"
                    "<strong>错因提醒：</strong>常见错误是<strong>误认为</strong>社会形态更替可以随意选择。"
                    "其实它由生产力发展水平决定，生产力是最活跃、最革命的因素。",},
        {"q": "关于科学社会主义，下面哪一句表述准确？",
         "options": [("唯物史观和剩余价值学说使社会主义由空想变为科学", True),
                     ("空想社会主义已经找到了实现理想社会的现实道路", False),
                     ("《共产党宣言》的发表标志着世界上第一个社会主义国家建立", False)],
         "explain": "唯物史观和剩余价值学说的创立，使社会主义由空想变为科学；一八四八年《共产党宣言》发表，"
                    "标志着科学社会主义的诞生。"
                    "<strong>错因提醒：</strong>有的同学把《共产党宣言》的发表和十月革命<strong>搞混</strong>了——"
                    "后者实现了科学社会主义从理论到现实的历史性飞跃。",},
        {"q": "关于中国特色社会主义进入新时代，下面哪一句表述准确？",
         "options": [("我国社会主要矛盾已经转化为人民日益增长的美好生活需要和不平衡不充分的发展之间的矛盾", True),
                     ("进入新时代意味着我国已经跨越社会主义初级阶段", False),
                     ("新时代坚持和发展中国特色社会主义的总任务是全面建成小康社会", False)],
         "explain": "中国特色社会主义进入新时代，这是我国发展新的历史方位；我国社会主要矛盾已经转化为"
                    "人民日益增长的美好生活需要和不平衡不充分的发展之间的矛盾；总任务是实现社会主义现代化和中华民族伟大复兴。"
                    "<strong>错因提醒：</strong>要小心「主要矛盾变了」被<strong>误认为</strong>「基本国情变了」。"
                    "我国仍处于并将长期处于社会主义初级阶段的基本国情没有变。",}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：社会主要矛盾判断台，做出你的方位卡", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一个<strong>现象</strong>，再判断它主要说明的是哪一方面。四个都判断完，你就有了一张属于自己的方位卡。</p>
        <div class="lab-panel">
          <div id="pm-stage">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">第一步 · 点一个现象</div>
            <div class="grid" id="pm-list"></div>
            <div style="font-weight:700;font-size:14px;margin:16px 0 6px">第二步 · 它主要说明的是</div>
            <div class="flex-row" style="margin-top:0">
              <button class="choice" data-pm-ans="need" style="text-align:center">人民日益增长的美好生活需要</button>
              <button class="choice" data-pm-ans="dev" style="text-align:center">不平衡不充分的发展</button>
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">判断进度</span><span class="v" id="pm-board">已判断 0 / 4 个现象</span></div>
          </div>
          <p class="result warn" id="pm-out" style="margin-top:12px">先点上面一个现象。</p>
        </div>
        <div class="inner-card" style="margin-top:14px">
          <p><strong>把你的判断写下来：</strong></p>
          <p style="color:var(--muted)">从四个现象里挑一个你最有感触的，用自己的话写一写：它为什么能说明我国社会主要矛盾已经转化？</p>
          <textarea id="syn-answer" rows="3" placeholder="我选的现象是……它说明……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，看看规律还在不在", TTS["posttest"], [
        {"q": "下列事件中，标志着我国确立社会主义基本制度、完成中国历史上最深刻最伟大的社会变革的是：",
         "options": [("一九五六年社会主义改造基本完成", True),
                     ("一九四九年中华人民共和国成立", False),
                     ("一九二一年中国共产党成立", False)],
         "explain": "一九五六年社会主义改造基本完成，确立了社会主义基本制度，完成了中国历史上最深刻最伟大的社会变革。"
                    "<strong>错因提醒：</strong>容易把「站起来」和「制度确立」<strong>搞混</strong>——"
                    "一九四九年中华人民共和国成立实现了民族独立、人民解放，为走上社会主义道路创造了前提。",},
        {"q": "关于改革开放，下面哪一句表述准确？",
         "options": [("改革开放是党和人民大踏步赶上时代的重要法宝，是坚持和发展中国特色社会主义的必由之路", True),
                     ("改革开放解决的是民族独立、人民解放的问题", False),
                     ("改革开放意味着可以照搬别国的发展道路", False)],
         "explain": "改革开放极大解放和发展了社会生产力，使中国大踏步赶上了时代；中国特色社会主义正是在改革开放中"
                    "创立、发展和完善起来的。"
                    "<strong>错因提醒：</strong>常见的<strong>误认为</strong>是「现代化就是照搬别国道路」。"
                    "必须坚持中国特色社会主义道路，坚定道路自信、理论自信、制度自信、文化自信。",},
        {"q": "关于实现中华民族伟大复兴的中国梦，下面哪一句表述准确？",
         "options": [("必须走中国道路、弘扬中国精神、凝聚中国力量，中国梦的本质是国家富强、民族振兴、人民幸福", True),
                     ("中国梦只要靠少数人努力就能实现", False),
                     ("实现中国梦不需要坚持中国共产党的领导", False)],
         "explain": "实现中华民族伟大复兴是中华民族近代以来最伟大的梦想，必须走中国道路、弘扬中国精神、凝聚中国力量；"
                    "中国梦的本质是国家富强、民族振兴、人民幸福。"
                    "<strong>错因提醒：</strong>要注意一个根本立场：中国共产党领导是中国特色社会主义最本质的特征，"
                    "实现中华民族伟大复兴必须坚持中国共产党的领导。",}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：规律、道路、方位，四句话讲清楚", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>基本规律：</strong>生产力与生产关系、经济基础与上层建筑的矛盾运动，是人类社会发展的基本规律；生产关系一定要适应生产力状况，上层建筑一定要适应经济基础状况。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>从空想到科学：</strong>唯物史观和剩余价值学说使社会主义由空想变为科学，《共产党宣言》的发表标志着科学社会主义的诞生；只有社会主义才能救中国。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>只有中国特色社会主义才能发展中国：</strong>改革开放是党和人民大踏步赶上时代的重要法宝；中国共产党领导是中国特色社会主义最本质的特征，必须坚持中国共产党的领导、坚持中国特色社会主义道路。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>新时代的历史方位：</strong>我国社会主要矛盾已经转化为人民日益增长的美好生活需要和不平衡不充分的发展之间的矛盾；总任务是实现社会主义现代化和中华民族伟大复兴。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(251,191,36,.6)">
          <p style="margin:0"><strong>一句口诀：</strong>社会形态步步高，两条规律要记牢；空想变科学、理论到实践，救中国靠社会主义；改革开放开新局，特色道路上大道；主要矛盾已转化，初级阶段没有变。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「基本规律」「社会主义」「中国特色社会主义」这三个词，给家里人讲清楚：中国为什么会走上社会主义道路，又为什么必须坚持走中国特色社会主义道路。</p>
          <p style="color:var(--muted)">再动一动手：<strong>写一写</strong>你身边最能说明「社会主要矛盾已经转化」的一个现象，连同你的分析一起收进本子里。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层任务，按自己的节奏来", TTS["homework"], [
        [
            "写出人类社会发展的两条客观规律，并各用一句话解释它的意思。",
            "按时间先后写出人类社会形态的更替顺序，并在每个阶段后面写出它的生产资料归谁所有。",
            "写出使社会主义由空想变为科学的两块理论基石，以及《共产党宣言》发表的标志性意义。",
        ],
        [
            "用一段话说明为什么说只有社会主义才能救中国，要把新民主主义革命的胜利和社会主义制度在中国的确立这两件事写进去。",
            "用一段话说明为什么说只有中国特色社会主义才能发展中国，要把改革开放的地位写清楚。",
        ],
        [
            "结合自己的生活观察，举一个例子说明我国社会主要矛盾已经转化的表现，并写清楚为什么说我国仍处于并将长期处于社会主义初级阶段。",
            "查一查我国国家制度和国家治理体系的相关公开表述，用三句话写清「中国特色社会主义制度」为什么是我们的根本制度保障。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": ID,
    "node_id": ID,
    "subject": "politics",
    "subject_cn": "思想政治",
    "stage": "high",
    "stage_cn": "高中",
    "curriculum": "普通高中思想政治课程标准（2017年版2020年修订）· 高中",
    "title": "中国特色社会主义：从科学社会主义到新时代",
    "name_en": "Socialism with Chinese Characteristics",
    "grade": 10,
    "grade_cn": "高一",
    "domain": "socialism",
    "domain_cn": "中国特色社会主义",
    "lesson_type": "conceptual-inquiry",
    "version": "1.0.0",
    "description": "面向高中一年级的思想政治课，对应统编《思想政治》必修1《中国特色社会主义》。全课沿「人类社会发展的基本规律 → 科学社会主义的创立与实践 → 中国特色社会主义的开创与发展 → 新时代的历史方位」这条主线展开，落到四件事上。第一件是人类社会发展的基本规律：生产力与生产关系、经济基础与上层建筑的矛盾运动是人类社会发展的基本规律；生产力决定生产关系，生产关系反作用于生产力；生产关系一定要适应生产力状况、上层建筑一定要适应经济基础状况，人类社会由原始社会、奴隶社会、封建社会、资本主义社会一路发展到社会主义社会，由低级向高级不断发展。第二件是科学社会主义的创立与实践：空想社会主义看到了资本主义的弊病却没有找到现实道路和依靠力量；唯物史观和剩余价值学说使社会主义由空想变为科学，一八四八年《共产党宣言》发表标志着科学社会主义的诞生；一九一七年十月革命建立了世界上第一个社会主义国家，实现了从理论到现实的历史性飞跃；在中国，一九二一年中国共产党成立，一九四九年中华人民共和国成立实现了民族独立、人民解放，一九五六年社会主义改造基本完成、确立了社会主义基本制度——只有社会主义才能救中国。第三件是只有中国特色社会主义才能发展中国：党的十一届三中全会开启了改革开放和社会主义现代化建设新时期，改革开放是党和人民大踏步赶上时代的重要法宝；中国共产党领导是中国特色社会主义最本质的特征，中国共产党是最高政治领导力量，必须坚持中国共产党的领导、坚持中国特色社会主义道路，坚定道路自信、理论自信、制度自信、文化自信。第四件是新时代的历史方位：中国特色社会主义进入新时代，这是我国发展新的历史方位；我国社会主要矛盾已经转化为人民日益增长的美好生活需要和不平衡不充分的发展之间的矛盾；新时代坚持和发展中国特色社会主义的总任务是实现社会主义现代化和中华民族伟大复兴；实现中国梦必须走中国道路、弘扬中国精神、凝聚中国力量，中国梦的本质是国家富强、民族振兴、人民幸福。三个互动台子都能真操作：动手一是「社会发展阶段时间轴」，按时间先后依次点出五个社会形态节点，点错顺序给出顺序提示；动手二是本课核心模拟「概念辨析台」，六个易混概念与六条准确表述配对，配错给出区分方法；综合任务是「社会主要矛盾判断台」，四个现象分别判断归属哪一方面，最后合成一张方位卡。全课在政治表述上从严把关：一律使用规范全称，社会主要矛盾的表述完整准确，同时明确我国仍处于并将长期处于社会主义初级阶段的基本国情没有变、我国是世界最大发展中国家的国际地位没有变；经典著作只写规范名称与公认的发表时间，不臆造文件编号，不编造会议细节，不涉及敏感时政细节与人物评价；插图一律为中性简洁抽象教学示意图，不绘制国旗、国徽、党徽、领导人形象与地图，改用齿轮、上升阶梯、道路延伸、楼群剪影、火炬抽象符号等图形。",
    "tags": ["中国特色社会主义", "人类社会发展的基本规律", "科学社会主义", "改革开放", "新时代", "社会主要矛盾", "高一", "必修1"],
    "standard_ref": "《普通高中思想政治课程标准（2017年版2020年修订）》必修1「中国特色社会主义」——理解社会主义从空想到科学、从理论到实践的发展，坚定中国特色社会主义信念；理解只有社会主义才能救中国，只有中国特色社会主义才能发展中国；理解新时代坚持和发展中国特色社会主义的总任务，学习贯彻习近平新时代中国特色社会主义思想。对应统编《思想政治》必修1：社会主义从空想到科学、从理论到实践的发展；只有社会主义才能救中国；只有中国特色社会主义才能发展中国；只有坚持和发展中国特色社会主义才能实现中华民族伟大复兴。",
    "hero_question": "中国特色社会主义是从哪里来的？今天的中国又处在什么样的历史方位？",
    "hero_alt": "中国特色社会主义知识结构图：三栏分别为人类社会发展的基本规律、科学社会主义的创立与实践、中国特色社会主义与新时代，用齿轮、上升阶梯、延伸道路、楼群剪影等抽象符号表示，附中文标注，不含国旗国徽与地图",
    "hero_caption": "中国特色社会主义：基本规律（生产力与生产关系的矛盾运动）· 从空想到科学、从理论到实践 · 只有中国特色社会主义才能发展中国",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想弄清的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "人类社会为什么会一步一步往前走？", "d": "背后是不是有一条基本规律在起作用", "v": "人类社会为什么会一步一步往前走"},
        {"t": "社会主义是怎么从设想变成科学的？", "d": "空想社会主义和科学社会主义差在哪里", "v": "社会主义是怎么从设想变成科学的"},
        {"t": "中国为什么会走上社会主义道路？", "d": "只有社会主义才能救中国，只有中国特色社会主义才能发展中国", "v": "中国为什么会走上社会主义道路"},
        {"t": "今天的中国处在什么样的历史方位？", "d": "新时代、社会主要矛盾、总任务都说了什么", "v": "今天的中国处在什么样的历史方位"},
    ],
    "objectives": [
        "能说出生产力与生产关系、经济基础与上层建筑的矛盾运动是人类社会发展的基本规律，能按时间先后说出人类社会形态的更替",
        "能说出唯物史观和剩余价值学说使社会主义由空想变为科学，知道《共产党宣言》的发表标志着科学社会主义的诞生",
        "能说明只有社会主义才能救中国、只有中国特色社会主义才能发展中国，明确中国共产党领导是中国特色社会主义最本质的特征，必须坚持中国共产党的领导、坚持中国特色社会主义道路",
        "能说出我国社会主要矛盾已经转化为人民日益增长的美好生活需要和不平衡不充分的发展之间的矛盾，知道新时代坚持和发展中国特色社会主义的总任务",
    ],
    "objectives_plain": [
        "能说出人类社会发展的基本规律，并按时间先后说出社会形态的更替",
        "能说出科学社会主义是怎样创立起来的，以及它怎样从理论走向现实",
        "能说明为什么只有社会主义才能救中国、只有中国特色社会主义才能发展中国",
        "能说出新时代的历史方位、我国社会主要矛盾的变化和新时代的总任务",
    ],
    "standards": [
        {"content": "理解社会主义从空想到科学、从理论到实践的发展，坚定中国特色社会主义信念。",
         "source": "《普通高中思想政治课程标准（2017年版2020年修订）》必修1 中国特色社会主义"},
        {"content": "理解只有社会主义才能救中国，只有中国特色社会主义才能发展中国。",
         "source": "《普通高中思想政治课程标准（2017年版2020年修订）》必修1 中国特色社会主义"},
        {"content": "理解新时代坚持和发展中国特色社会主义的总任务，学习贯彻习近平新时代中国特色社会主义思想。",
         "source": "《普通高中思想政治课程标准（2017年版2020年修订）》必修1 中国特色社会主义"},
    ],
    "prereqs": [],
    "prereqs_name": "本课为高中思想政治必修模块的起点，无前置节点",
    "prereqs_meta": "",
    "leads_to": ["pol-h-req2"],
    "next_meta": "pol-h-req2",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "一条主线：人类社会发展的基本规律 → 科学社会主义 → 中国特色社会主义 → 新时代。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能把「中国特色社会主义从哪里来」讲清楚。",
        "objectives": "看清四件事：基本规律、从空想到科学、只有中国特色社会主义才能发展中国、新时代的方位与总任务。",
        "pretest": "凭现在的理解选就好，选得不准也不扣分，正好知道要重点听哪里。",
        "module-1": "抓住两层关系：生产力决定生产关系，生产关系反作用于生产力；由此得出两条客观规律。",
        "lab-1": "五个节点顺序被打乱了，按时间先后从最早的社会形态开始点，点错会提示顺序问题。",
        "module-2": "两条线索：从空想到科学（唯物史观与剩余价值学说）→ 从理论到实践（十月革命）→ 中国（新民主主义革命的胜利、社会主义制度的确立）。",
        "lab-2": "本课最重要的台子：先点概念，再点表述。想一想这个概念最关键的一件事是什么。",
        "worked-example": "四条表述里三条准确、一条必须改。重点：主要矛盾变了，基本国情没有变。",
        "conceptest-1": "三句话里各藏着一个容易想歪的地方，选完把解释读一遍。",
        "synthesis": "先点现象，再判断它说明的是「人民的需要」还是「发展的短板」。",
        "posttest": "出现了制度确立、改革开放和中国梦，看看今天学的还用不用得上。",
        "summary": "四句话：基本规律、从空想到科学、只有中国特色社会主义才能发展中国、新时代的历史方位。",
        "homework": "三层任务，先做前两层；第二层要把两件事分开写清楚。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是高中思想政治「中国特色社会主义」板块的空缺，对应统编《思想政治》必修1《中国特色社会主义》四课内容。高一学生已经在初中接触过改革开放、新时代等概念，也听说过「社会主义」「中国特色社会主义」这些词，但对「人类社会为什么会这样发展」「社会主义凭什么从空想变成科学」「中国为什么必然走上社会主义道路」「今天的中国处在什么历史方位」往往只有零碎印象，甚至会把「主要矛盾变了」误认为「基本国情变了」。所以全课不讲口号、不背结论，而把内容换成能核对、能复述的规律与事件链条。第一层是「人类社会发展的基本规律」：明确生产力与生产关系、经济基础与上层建筑的矛盾运动是人类社会发展的基本规律；生产力决定生产关系，生产关系反作用于生产力；生产关系一定要适应生产力状况、上层建筑一定要适应经济基础状况；人类社会由原始社会、奴隶社会、封建社会、资本主义社会发展到社会主义社会，由低级向高级不断发展，社会主义终将代替资本主义是历史发展的必然趋势。第二层是「科学社会主义的创立与实践」：空想社会主义看到了资本主义的弊病却没有找到现实道路和依靠力量；唯物史观和剩余价值学说的创立使社会主义由空想变为科学，一八四八年《共产党宣言》发表标志着科学社会主义的诞生；一九一七年十月革命建立了世界上第一个社会主义国家，实现了从理论到现实的历史性飞跃；在中国，一九二一年中国共产党成立、一九四九年中华人民共和国成立实现了民族独立和人民解放、一九五六年社会主义改造基本完成确立了社会主义基本制度——只有社会主义才能救中国。第三层是「只有中国特色社会主义才能发展中国」：党的十一届三中全会开启了改革开放和社会主义现代化建设新时期，改革开放是党和人民大踏步赶上时代的重要法宝，是坚持和发展中国特色社会主义的必由之路；必须明确坚持中国共产党的领导、坚持中国特色社会主义道路，坚定道路自信、理论自信、制度自信、文化自信——中国共产党领导是中国特色社会主义最本质的特征，中国共产党是最高政治领导力量。第四层是「新时代的历史方位」：中国特色社会主义进入新时代，这是我国发展新的历史方位；我国社会主要矛盾已经转化为人民日益增长的美好生活需要和不平衡不充分的发展之间的矛盾；新时代坚持和发展中国特色社会主义的总任务是实现社会主义现代化和中华民族伟大复兴；实现中华民族伟大复兴的中国梦必须走中国道路、弘扬中国精神、凝聚中国力量，中国梦的本质是国家富强、民族振兴、人民幸福。三个互动台子都能真操作：动手一是「社会发展阶段时间轴」，五个社会形态节点顺序打乱，学生按时间先后依次点出，点错给顺序提示、点对给出该阶段的生产力状况与生产关系特点；动手二是本课核心模拟「概念辨析台」，把空想社会主义、科学社会主义、新民主主义革命、社会主义制度在中国的确立、改革开放、中国特色社会主义进入新时代六个易混概念与六条准确表述配对，配错给出区分方法；综合任务是「社会主要矛盾判断台」，四个现象分别判断主要说明的是人民日益增长的美好生活需要还是不平衡不充分的发展，判断完合成一张方位卡。全课在政治表述上从严把关：一律使用规范全称；社会主要矛盾的表述完整准确，并同时明确我国仍处于并将长期处于社会主义初级阶段的基本国情没有变、我国是世界最大发展中国家的国际地位没有变；经典著作只写规范名称与公认的发表时间，不臆造文件编号与会议细节，不涉及敏感时政细节与人物评价；表述庄重、严谨、积极正面；插图一律为中性简洁抽象教学示意图，不绘制国旗、国徽、党徽、领导人形象与地图。",
    "plan_table": """| 1 | cover | 中国特色社会主义：从科学社会主义到新时代 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：人类社会为什么会往前走？ | 起·前测（暴露已有印象与混淆点） |
| 5 | concept | 人类社会发展的基本规律：生产力与生产关系的矛盾运动 | 承·概念一（基本规律） |
| 6 | interactive | 动手一：社会发展阶段时间轴，按时间先后点出来 | 承·时间轴（5 个社会形态顺序点出） |
| 7 | concept | 科学社会主义的创立与实践：只有社会主义才能救中国 | 承·概念二（从空想到科学、从理论到实践） |
| 8 | interactive | ★动手二：概念辨析台——把易混概念配到准确表述 | 承·核心模拟（6 概念 × 6 条表述） |
| 9 | concept | 例题示范：新时代的历史方位与总任务，四条表述逐条校对 | 转·重难点突破（分步校对 + 纠错） |
| 10 | quiz | 概念测试：三句话，藏着三个容易想歪的地方 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：社会主要矛盾判断台，做出你的方位卡 | 合·迁移应用（4 现象判断 → 方位卡） |
| 12 | quiz | 后测：换几个新情境，看看规律还在不在 | 合·后测 |
| 13 | summary | 小结：规律、道路、方位，四句话讲清楚 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：人类社会发展的基本规律 / 科学社会主义的创立与实践 / 中国特色社会主义与新时代 三栏，用齿轮、上升阶梯、延伸道路、楼群剪影等抽象符号表示，附中文标注\n- P5 社会形态更替时间轴抽象示意图（已生成）：原始社会、奴隶社会、封建社会、资本主义社会、社会主义社会五个阶段自左向右逐级上升，各级标注生产力状况与生产关系特点要点\n- P7 两段式进程抽象示意图（已生成）：从空想到科学、从理论到实践；只有社会主义才能救中国、只有中国特色社会主义才能发展中国，并标注「抽象示意图，不按比例」\n- ★ 全课不绘制国旗、国徽、党徽、领导人形象与地图；涉及国家与制度仅用齿轮、上升阶梯、道路延伸、楼群剪影、火炬抽象符号等中性图形\n- ★ 表述口径统一：规范全称一律写准；社会主要矛盾的表述完整；不臆造文件编号与会议细节，不涉及敏感时政细节与人物评价\n- 三张图均为中性简洁抽象教学示意图，不使用真人照片风格，不含可识别的真实人物",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
