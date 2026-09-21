# -*- coding: utf-8 -*-
"""高中思想政治 · 经济与社会（必修2）—— 补齐知识树「经济与社会」空缺

学科语气（思想政治）：从「我们脚下的经济地基是怎么打牢的」这个真问题切入，用制度归属与
利益分配做骨架，用可核对的经济现象做证据；结论落在「这一条表述准不准、依据是什么」，
不做口号式抒情、不背条文。

★ 政治表述红线（最高优先级，全课统一口径，任何地方不得含糊）：
  · 规范全称一律写准：公有制为主体、多种所有制经济共同发展；按劳分配为主体、多种分配方式
    并存；社会主义市场经济体制；新发展理念；社会保障制度；「两个毫不动摇」。
  · 我国基本经济制度的三项内容必须完整准确：公有制为主体、多种所有制经济共同发展；
    按劳分配为主体、多种分配方式并存；社会主义市场经济体制。
  · 「两个毫不动摇」必须完整：毫不动摇巩固和发展公有制经济，毫不动摇鼓励、支持、引导
    非公有制经济发展。
  · 社会主义市场经济体制的鲜明特征必须写准：坚持中国共产党的领导，这是中国特色社会主义
    最本质的特征，也是社会主义市场经济体制的重要特征；以公有制为主体，这是社会主义市场
    经济体制的根基；以共同富裕为根本目标，这是社会主义的本质要求。
  · 国有经济是国民经济的主导力量；非公有制经济是社会主义市场经济的重要组成部分，是我国
    经济社会发展的重要基础。不得把二者地位混写。
  · 不臆造文件名称与编号、不编造会议细节、不涉及敏感时政细节与人物评价；表述庄重、严谨、
    积极正面；插图一律为中性简洁抽象教学示意图，不绘制国旗、国徽、党徽、领导人形象、地图，
    改用齿轮、天平、楼群剪影、上升曲线、抽象握手等中性抽象图形。

内容落点（对应统编必修2《经济与社会》四课）：
  ① 我国的生产资料所有制：公有制为主体、多种所有制经济共同发展；坚持「两个毫不动摇」。
  ② 我国的社会主义市场经济体制：市场在资源配置中起决定性作用，更好发挥政府作用。
  ③ 我国的经济发展：贯彻创新、协调、绿色、开放、共享的新发展理念，推动高质量发展。
  ④ 我国的个人收入分配与社会保障：按劳分配为主体、多种分配方式并存；社会保障体系。

三个互动台子都能真操作：
  动手一 = 「所有制归类台」（六个经济主体 → 公有制经济 / 非公有制经济）；
  ★核心模拟 动手二 = 「分配方式判断台」（六个收入情境 × 四类分配方式，含最高频易错点）；
  综合任务 = 「经济现象与制度对应台」（五个经济现象 → 五项制度与理念归属，合成经济地基卡）。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-h-req2"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "先看几个身边的事。我们每天用的手机、坐的地铁、买的蔬菜，背后都有一整套经济制度在运转。为什么国有企业要在关系国家安全的重要行业挑大梁，同时民营企业也能发展得红红火火？我们每个月的工资、奖金、存款利息，各自是按什么分配的？国家又会用什么办法，让生病、失业、年老的时候生活有保障？这节课我们把我国的基本经济制度、新发展理念和收入分配与社会保障这几件事弄明白，看清我们脚下的经济地基是怎么打牢的。",
    "problem-anchor": "开始之前，先选一个你真正想弄清的问题：我国的基本经济制度到底包括哪些内容？为什么必须坚持公有制为主体、多种所有制经济共同发展？我们的收入是按什么分配的？国家又怎样为每个人的生活提供保障？选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出我国基本经济制度的三项内容，能说明公有制为主体、多种所有制经济共同发展，并能说清两个毫不动摇的完整要求。第二，能说出国有经济是国民经济的主导力量，与非公有制经济的地位区分清楚。第三，能说出按劳分配为主体、多种分配方式并存的分配制度，能判断一种收入属于按劳分配还是按生产要素分配，并说出社会保障体系的主要形式。第四，能说出创新、协调、绿色、开放、共享的新发展理念，能结合经济现象说明它对应我国哪一项制度或理念。",
    "pretest": "先做三道小题，用你现在的理解选就行。选完马上能看到解释，选得不准也没关系，正好知道要重点听哪里。",
    "module-1": "第一件事，我国的生产资料所有制。先要记住我国基本经济制度的三项内容：公有制为主体、多种所有制经济共同发展；按劳分配为主体、多种分配方式并存；社会主义市场经济体制。这节课先看第一项。公有制经济包括国有经济、集体经济，以及混合所有制经济中的国有成分和集体成分。公有制经济的主体地位主要体现在两个方面：公有资产在社会总资产中占优势；国有经济控制国民经济命脉，对经济发展起主导作用。非公有制经济是社会主义市场经济的重要组成部分，是我国经济社会发展的重要基础。所以必须坚持两个毫不动摇：毫不动摇巩固和发展公有制经济，毫不动摇鼓励、支持、引导非公有制经济发展。这里有一个常见错误要避开：有的同学误认为公有制经济就是国有经济。其实集体经济，以及混合所有制经济中的国有成分和集体成分，同样属于公有制经济。",
    "lab-1": "现在请你亲手做一次归类。下面有六个经济主体，请你先点一个主体，再判断它属于公有制经济还是非公有制经济。判断对了，我会把它的地位讲清楚；判断错了，我会告诉你容易搞混在哪里。六个都归完，你就能看清我国所有制结构的全貌。",
    "module-2": "第二件事，我国的个人收入分配与社会保障。我国实行按劳分配为主体、多种分配方式并存的分配制度，这是我国基本经济制度的第二项内容。按劳分配是社会主义的分配原则，它存在于公有制经济中，多劳多得、少劳少得，是我国分配制度的主体。在公有制经济之外，还有按生产要素分配：劳动、资本、土地、知识、技术、管理、数据等生产要素由市场评价贡献、按贡献决定报酬。所以要特别注意一个容易搞混的地方：按劳分配只在公有制经济中实行，私营企业、外资企业职工的工资属于按生产要素分配中的劳动要素，不能叫做按劳分配。再看居民收入，一般分为工资性收入、经营性收入、财产性收入和转移性收入四类。最后是社会保障，我国的社会保障体系主要包括社会保险、社会救助、社会福利、社会优抚，它是民生的安全网。",
    "lab-2": "接下来是这个模块最重要的一个台子：分配方式判断台。下面有六个收入情境，请你先点一个情境，再判断这笔收入属于按劳分配，还是属于按生产要素分配中的哪一类要素。判断对了，我会把依据讲一遍；判断错了，我会告诉你最容易混在哪里。",
    "worked-example": "我们一起当一次校对员。某校经济兴趣小组整理出五条表述，请你逐条判断。第一条，我国实行公有制为主体、多种所有制经济共同发展的生产资料所有制。这一条准确。第二条，国有经济是国民经济的主导力量，控制国民经济命脉。这一条准确。第三条，市场在资源配置中起决定性作用，同时要更好发挥政府作用。这一条准确。第四条，非公有制经济是我国国民经济的主导力量。这一条必须改。国有经济才是国民经济的主导力量；非公有制经济是社会主义市场经济的重要组成部分，是我国经济社会发展的重要基础。第五条，我国贯彻创新、协调、绿色、开放、共享的新发展理念，推动高质量发展，建设现代化经济体系。这一条准确。创新是引领发展的第一动力，协调是持续健康发展的内在要求，绿色是永续发展的必要条件，开放是国家繁荣发展的必由之路，共享是中国特色社会主义的本质要求。还要说清一件事：社会主义市场经济体制既具有市场经济的共性，又具有自己鲜明的特征。坚持中国共产党的领导，这是中国特色社会主义最本质的特征，也是社会主义市场经济体制的重要特征；以公有制为主体，这是社会主义市场经济体制的根基；以共同富裕为根本目标，这是社会主义的本质要求。",
    "conceptest-1": "接下来用三道题考考你，每道题里都藏着一个容易想歪的地方。读一读，选一个你认为准确的，再看解释。",
    "synthesis": "最后一件任务交给你：做一次经济现象与制度对应。下面有五个经济现象，请你分别判断它主要对应我国经济生活中的哪一项制度或理念。五个都判断完，你会得到一张属于自己的经济地基卡。",
    "posttest": "最后一轮，换几个新情境来考考你。这次会出现失业保险、绿色发展和两个毫不动摇，看看今天学的东西还用不用得上。",
    "summary": "这节课我们弄清楚四件事。第一，我国基本经济制度包括公有制为主体、多种所有制经济共同发展，按劳分配为主体、多种分配方式并存，社会主义市场经济体制三个方面。第二，公有制经济包括国有经济、集体经济和混合所有制经济中的国有成分和集体成分；国有经济是国民经济的主导力量；非公有制经济是社会主义市场经济的重要组成部分；必须坚持两个毫不动摇。第三，按劳分配是社会主义的分配原则，存在于公有制经济中；在公有制经济之外，实行按生产要素分配，劳动、资本、土地、知识、技术、管理、数据等要素由市场评价贡献、按贡献决定报酬；我国的社会保障体系主要包括社会保险、社会救助、社会福利、社会优抚。第四，我国贯彻创新、协调、绿色、开放、共享的新发展理念，推动高质量发展，建设现代化经济体系。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出我国基本经济制度的三项内容，并写出两个毫不动摇的完整要求。第二层能力应用，动手做：收集家里或身边的三笔收入，分别判断它属于按劳分配还是按生产要素分配，并写清依据。第三层迁移挑战，选做：结合身边的一个经济现象，说明它体现了新发展理念中的哪一方面，并写清为什么说我国坚持公有制为主体、多种所有制经济共同发展有利于实现共同富裕。",
    "knowledge-graph": "这张图展示了这节课在思想政治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域里的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 我国的生产资料所有制", "lab-1": "动手一 所有制归类台",
    "module-2": "概念二 个人收入分配与社会保障", "lab-2": "★动手二 分配方式判断台（核心模拟）",
    "worked-example": "例题示范 制度与理念五条表述逐条校对", "conceptest-1": "概念测试",
    "synthesis": "综合任务 经济现象与制度对应台", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：所有制归类台（六个经济主体 × 公有制 / 非公有制） ──
SUBJ = [
    {"k": "s1", "t": "某国有企业，处在关系国家安全和国民经济命脉的重要行业。", "bin": "pub",
     "why": "国有经济是公有制经济的重要组成部分，是国民经济的主导力量，控制国民经济命脉，对经济发展起主导作用。",
     "err": ""},
    {"k": "s2", "t": "某村集体经济组织兴办的农产品加工合作社。", "bin": "pub",
     "why": "集体经济是公有制经济的重要组成部分，体现共同富裕原则。",
     "err": ""},
    {"k": "s3", "t": "某民营企业设立的研发中心。", "bin": "nonpub",
     "why": "非公有制经济是社会主义市场经济的重要组成部分，是我国经济社会发展的重要基础。",
     "err": ""},
    {"k": "s4", "t": "某外商投资企业在我国境内投资设立的工厂。", "bin": "nonpub",
     "why": "外资经济属于非公有制经济。国家毫不动摇鼓励、支持、引导非公有制经济发展。",
     "err": ""},
    {"k": "s5", "t": "某混合所有制企业中的国有成分。", "bin": "pub",
     "why": "混合所有制经济中的国有成分和集体成分，都属于公有制经济。",
     "err": "这是最常见的搞混点：看到「混合所有制」就以为它一定不是公有制。判断标准是这部分资本归谁所有。"},
    {"k": "s6", "t": "某个体工商户经营的一家小餐馆。", "bin": "nonpub",
     "why": "个体经济属于非公有制经济，国家保护个体经济等非公有制经济的合法权益。",
     "err": ""},
]

# ── 动手二（★核心模拟）：分配方式判断台 ──
DIST = [
    {"k": "d1", "t": "国有企业职工小张，每月按岗位和绩效领取工资、奖金。", "ans": "A",
     "why": "公有制经济中，个人消费品实行按劳分配，多劳多得、少劳少得，这是我国分配制度的主体。",
     "err": "容易搞混的地方：看到「工资」两个字就一律判成按劳分配，忽略了它必须发生在公有制经济中。"},
    {"k": "d2", "t": "某外资企业职工小李，按完成的合格产品件数领取计件工资。", "ans": "B",
     "why": "外资企业属于非公有制经济，这里职工的工资属于按生产要素分配中的劳动要素。",
     "err": "最容易搞混的一处：误认为只要叫「工资」就是按劳分配。按劳分配只存在于公有制经济中，非公有制经济中职工的工资属于按劳动要素分配。"},
    {"k": "d3", "t": "老王把自家承包地的经营权流转出去，每年收取流转租金。", "ans": "D",
     "why": "土地是重要的生产要素，土地经营权流转获得的租金属于按土地要素分配。",
     "err": "常见错误：一看到农村、土地就误认为属于按劳分配。这里的租金来自土地要素，不是按劳分配。"},
    {"k": "d4", "t": "小陈把闲置资金存入银行，按期获得存款利息。", "ans": "C",
     "why": "资本是重要的生产要素，存款利息属于按资本要素分配。",
     "err": "常见错误：把利息误认为按劳分配，或者误认为它属于转移性收入。利息来自资本要素，同时它是居民收入中的财产性收入。"},
    {"k": "d5", "t": "小周以自己的技术入股某科技公司，按约定比例获得分红。", "ans": "D",
     "why": "知识、技术、管理、数据等都是生产要素，技术入股获得的分红属于按技术要素分配。",
     "err": "常见错误：把技术分红误认为按劳分配，忘记了技术本身就是生产要素。"},
    {"k": "d6", "t": "某村集体经济组织成员老赵，按劳动贡献参与年终收益分配。", "ans": "A",
     "why": "集体经济属于公有制经济，其中的个人收入分配同样实行按劳分配。",
     "err": "常见错误：误认为只有国有企业才实行按劳分配，忽略了集体经济同样属于公有制经济。"},
]

# ── 综合任务：经济现象与制度对应台 ──
SYSTS = [
    {"k": "y1", "t": "国家毫不动摇鼓励、支持、引导非公有制经济发展，民营经济在创新和就业中发挥着重要作用。",
     "ans": "i1",
     "why": "这体现的是公有制为主体、多种所有制经济共同发展的生产资料所有制，以及坚持两个毫不动摇的要求。"},
    {"k": "y2", "t": "某国有控股企业中，职工按劳取酬，同时企业按技术要素给研发人员分红。",
     "ans": "i2",
     "why": "这体现的是按劳分配为主体、多种分配方式并存的分配制度：公有制经济中实行按劳分配，同时存在按生产要素分配。"},
    {"k": "y3", "t": "某农产品价格主要由市场供求决定，政府同时做好储备调节，防止价格大幅波动。",
     "ans": "i3",
     "why": "这体现的是社会主义市场经济体制：使市场在资源配置中起决定性作用，同时更好发挥政府作用。"},
    {"k": "y4", "t": "某地以光伏发电替代燃煤发电，走生态优先、绿色低碳的发展路子。",
     "ans": "i4",
     "why": "这体现的是创新、协调、绿色、开放、共享的新发展理念，其中绿色发展是永续发展的必要条件。"},
    {"k": "y5", "t": "某职工失业期间按规定领取失业保险金，生病住院时按规定报销医疗费用。",
     "ans": "i5",
     "why": "这体现的是我国的社会保障制度，社会保险是社会保障体系的核心内容，是民生的安全网。"},
]

CUSTOM_JS = r"""
/* ============================================================
   pol-h-req2 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 「所有制归类台」：六个经济主体 → 公有制 / 非公有制
   3) ★「分配方式判断台」：六个收入情境 → 四类分配方式
   4) 「经济现象与制度对应台」：五个现象 → 五项制度与理念归属
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

  /* ---------- 2. 所有制归类台 ---------- */
  var SUBJ = __SUBJ_JSON__;
  var BIN_LABEL = { pub: '公有制经济', nonpub: '非公有制经济' };
  var owStage = document.getElementById('ow-stage');
  if (owStage) {
    var selS = null;
    var doneS = {};
    var out1 = document.getElementById('ow-out');
    var list1 = document.getElementById('ow-list');
    var board1 = document.getElementById('ow-board');
    function render1() {
      list1.innerHTML = '';
      SUBJ.forEach(function (S, i) {
        var b = document.createElement('button');
        b.className = 'choice' + (doneS[S.k] ? ' correct' : (selS === S.k ? ' selected' : ''));
        b.style.textAlign = 'left';
        b.innerHTML = '<strong>' + (i + 1) + '.</strong> ' + S.t +
          (doneS[S.k] ? '<br><span style="color:var(--accent-deep);font-size:14px">已归类：' + BIN_LABEL[S.bin] + ' ✓</span>' : '');
        b.addEventListener('click', function () {
          if (doneS[S.k]) {
            selS = S.k;
            out1.className = 'result';
            out1.innerHTML = '<strong>已归类：' + BIN_LABEL[S.bin] + '</strong><br>' + S.why;
            render1();
            return;
          }
          selS = S.k;
          out1.className = 'result warn';
          out1.innerHTML = '<strong>你选了第 ' + (i + 1) + ' 个主体。</strong>现在到下面判断它属于哪一类。';
          render1();
        });
        list1.appendChild(b);
      });
      board1.textContent = '已归类 ' + Object.keys(doneS).length + ' / ' + SUBJ.length + ' 个主体';
    }
    render1();
    document.querySelectorAll('[data-ow-bin]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (!selS) {
          out1.className = 'result warn';
          out1.innerHTML = '先在上面点一个经济主体，再判断它属于哪一类。' +
            '<br><span style="color:var(--muted)">还可以试试：判断标准只有一条——这部分资本归谁所有。</span>';
          return;
        }
        var S = null;
        for (var i = 0; i < SUBJ.length; i++) { if (SUBJ[i].k === selS) S = SUBJ[i]; }
        var pick = btn.dataset.owBin;
        if (pick === S.bin) {
          doneS[S.k] = true;
          out1.className = 'result';
          out1.innerHTML = '<strong>归类准确：' + BIN_LABEL[S.bin] + '</strong><br>' + S.why;
          if (Object.keys(doneS).length === SUBJ.length) {
            out1.innerHTML += '<br><br><strong>六个主体都归类完了。</strong>' +
              '公有制经济包括国有经济、集体经济以及混合所有制经济中的国有成分和集体成分；' +
              '公有制为主体、多种所有制经济共同发展，是我国基本经济制度的重要内容。' +
              '必须毫不动摇巩固和发展公有制经济，毫不动摇鼓励、支持、引导非公有制经济发展。';
          }
          selS = null;
        } else {
          out1.className = 'result warn';
          out1.innerHTML = '<strong>再想一想：这个主体更可能属于「' + BIN_LABEL[S.bin] + '」。</strong>' +
            (S.err ? S.err : (S.bin === 'pub'
              ? '常见错误：把国有企业之外的经济形式都误认为非公有制经济。集体经济和混合所有制经济中的国有成分、集体成分，同样属于公有制经济。'
              : '常见错误：把非公有制经济误认为公有制经济，或者把「混合所有制」整体归到某一类。判断标准只有一条——这部分资本归谁所有。')) +
            '<br><span style="color:var(--muted)">还可以试试：先问这部分资本归谁所有，再下判断。</span>';
        }
        render1();
      });
    });
  }

  /* ---------- 3. ★ 分配方式判断台 ---------- */
  var DIST = __DIST_JSON__;
  var ALABEL = {
    A: '按劳分配',
    B: '按生产要素分配（劳动要素）',
    C: '按生产要素分配（资本要素）',
    D: '按生产要素分配（土地、技术、管理等要素）'
  };
  var dbStage = document.getElementById('db-stage');
  if (dbStage) {
    var selD = null;
    var doneD = {};
    var out2 = document.getElementById('db-out');
    var list2 = document.getElementById('db-list');
    var board2 = document.getElementById('db-board');
    function render2() {
      list2.innerHTML = '';
      DIST.forEach(function (D, i) {
        var b = document.createElement('button');
        b.className = 'choice' + (doneD[D.k] ? ' correct' : (selD === D.k ? ' selected' : ''));
        b.style.textAlign = 'left';
        b.innerHTML = '<strong>' + (i + 1) + '.</strong> ' + D.t +
          (doneD[D.k] ? '<br><span style="color:var(--accent-deep);font-size:14px">已判断：' + ALABEL[D.ans] + ' ✓</span>' : '');
        b.addEventListener('click', function () {
          if (doneD[D.k]) {
            selD = D.k;
            out2.className = 'result';
            out2.innerHTML = '<strong>已判断：' + ALABEL[D.ans] + '</strong><br>' + D.why;
            render2();
            return;
          }
          selD = D.k;
          out2.className = 'result warn';
          out2.innerHTML = '<strong>你选了第 ' + (i + 1) + ' 个情境。</strong>现在到下面判断这笔收入属于哪一类。';
          render2();
        });
        list2.appendChild(b);
      });
      board2.textContent = '已判断 ' + Object.keys(doneD).length + ' / ' + DIST.length + ' 个情境';
    }
    render2();
    document.querySelectorAll('[data-db-ans]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (!selD) {
          out2.className = 'result warn';
          out2.innerHTML = '先在上面点一个收入情境，再判断它的分配方式。' +
            '<br><span style="color:var(--muted)">还可以试试：先问两句话——这笔收入发生在公有制经济里吗？如果不是，它对应哪一种生产要素？</span>';
          return;
        }
        var D = null;
        for (var i = 0; i < DIST.length; i++) { if (DIST[i].k === selD) D = DIST[i]; }
        var pick = btn.dataset.dbAns;
        if (pick === D.ans) {
          doneD[D.k] = true;
          out2.className = 'result';
          out2.innerHTML = '<strong>判断准确：' + ALABEL[D.ans] + '</strong><br>' + D.why;
          if (Object.keys(doneD).length === DIST.length) {
            out2.innerHTML += '<br><br><strong>六个情境都判断完了。</strong>' +
              '把握一条主线：按劳分配是社会主义的分配原则，存在于公有制经济中；' +
              '在公有制经济之外，劳动、资本、土地、知识、技术、管理、数据等生产要素由市场评价贡献、按贡献决定报酬。' +
              '按劳分配为主体、多种分配方式并存，是我国基本经济制度的重要内容。';
          }
          selD = null;
        } else {
          out2.className = 'result warn';
          out2.innerHTML = '<strong>再想一想：这笔收入更可能属于「' + ALABEL[D.ans] + '」。</strong>' + D.err;
        }
        render2();
      });
    });
  }

  /* ---------- 4. 经济现象与制度对应台 ---------- */
  var SYSTS = __SYSTS_JSON__;
  var SLABEL = {
    i1: '公有制为主体、多种所有制经济共同发展',
    i2: '按劳分配为主体、多种分配方式并存',
    i3: '社会主义市场经济体制',
    i4: '新发展理念',
    i5: '社会保障制度'
  };
  var syStage = document.getElementById('sy-stage');
  if (syStage) {
    var selY = null;
    var doneY = {};
    var out3 = document.getElementById('sy-out');
    var list3 = document.getElementById('sy-list');
    var board3 = document.getElementById('sy-board');
    function render3() {
      list3.innerHTML = '';
      SYSTS.forEach(function (Y, i) {
        var b = document.createElement('button');
        b.className = 'choice' + (doneY[Y.k] ? ' correct' : (selY === Y.k ? ' selected' : ''));
        b.style.textAlign = 'left';
        b.innerHTML = '<strong>' + (i + 1) + '.</strong> ' + Y.t +
          (doneY[Y.k] ? '<br><span style="color:var(--accent-deep);font-size:14px">已对应：' + SLABEL[Y.ans] + ' ✓</span>' : '');
        b.addEventListener('click', function () {
          if (doneY[Y.k]) {
            selY = Y.k;
            out3.className = 'result';
            out3.innerHTML = '<strong>已对应：' + SLABEL[Y.ans] + '</strong><br>' + Y.why;
            render3();
            return;
          }
          selY = Y.k;
          out3.className = 'result warn';
          out3.innerHTML = '<strong>你选了第 ' + (i + 1) + ' 个现象。</strong>现在到下面判断它主要对应哪一项。';
          render3();
        });
        list3.appendChild(b);
      });
      board3.textContent = '已对应 ' + Object.keys(doneY).length + ' / ' + SYSTS.length + ' 个现象';
    }
    render3();
    document.querySelectorAll('[data-sy-ans]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (!selY) {
          out3.className = 'result warn';
          out3.innerHTML = '先在上面点一个经济现象，再判断它对应哪一项。' +
            '<br><span style="color:var(--muted)">还可以试试：先问这句话在讲「谁可以参与生产」「收入怎么分」「价格谁来定」「怎么发展」「生活怎么保障」中的哪一件事。</span>';
          return;
        }
        var Y = null;
        for (var i = 0; i < SYSTS.length; i++) { if (SYSTS[i].k === selY) Y = SYSTS[i]; }
        var pick = btn.dataset.syAns;
        if (pick === Y.ans) {
          doneY[Y.k] = true;
          out3.className = 'result';
          out3.innerHTML = '<strong>对应准确：' + SLABEL[Y.ans] + '</strong><br>' + Y.why;
          if (Object.keys(doneY).length === SYSTS.length) {
            out3.innerHTML += '<br><br><strong>五个现象都对应完了，这就是你的经济地基卡。</strong>' +
              '我国基本经济制度包括公有制为主体、多种所有制经济共同发展，按劳分配为主体、多种分配方式并存，' +
              '社会主义市场经济体制三个方面；再加上创新、协调、绿色、开放、共享的新发展理念，' +
              '以及保障民生的社会保障体系，我们脚下的经济地基就看得清清楚楚了。';
          }
          selY = null;
        } else {
          out3.className = 'result warn';
          out3.innerHTML = '<strong>再想一想：这个现象更可能对应「' + SLABEL[Y.ans] + '」。</strong>' +
            '常见错误：把「收入怎么分配」和「生活怎么保障」<strong>搞混</strong>。' +
            '工资、奖金、分红说的是分配制度；失业保险、医疗报销说的是社会保障制度。' +
            '<br><span style="color:var(--muted)">还可以试试：换个角度读一遍这句话，看它讲的是生产、分配、交换还是保障。</span>';
        }
        render3();
      });
    });
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__SUBJ_JSON__', json.dumps(SUBJ, ensure_ascii=False))
             .replace('__DIST_JSON__', json.dumps(DIST, ensure_ascii=False))
             .replace('__SYSTS_JSON__', json.dumps(SYSTS, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：我们脚下的经济地基由什么构成？", TTS["pretest"], [
        {"q": "我国基本经济制度包括三个方面。下面哪一组表述是准确的？",
         "options": [("公有制为主体、多种所有制经济共同发展；按劳分配为主体、多种分配方式并存；社会主义市场经济体制", True),
                     ("公有制为主体；按需分配；计划经济体制", False),
                     ("多种所有制经济共同发展；平均分配；自由放任的市场经济", False)],
         "explain": "我国基本经济制度包括公有制为主体、多种所有制经济共同发展，按劳分配为主体、多种分配方式并存，"
                    "社会主义市场经济体制三个方面。"
                    "<strong>错因提醒：</strong>常见错误是把「按劳分配为主体」<strong>搞混</strong>成按需分配或平均分配，"
                    "也有的同学误认为我国还实行计划经济体制。",},
        {"q": "国有经济和非公有制经济在国民经济中的地位，下面哪一句表述准确？",
         "options": [("国有经济是国民经济的主导力量，非公有制经济是社会主义市场经济的重要组成部分", True),
                     ("非公有制经济是国民经济的主导力量，国有经济是重要组成部分", False),
                     ("两者地位完全相同，都是国民经济的主导力量", False)],
         "explain": "国有经济是国民经济的主导力量，控制国民经济命脉，对经济发展起主导作用；"
                    "非公有制经济是社会主义市场经济的重要组成部分，是我国经济社会发展的重要基础。"
                    "<strong>错因提醒：</strong>把两种经济的地位<strong>搞混</strong>是这一课最高频的常见错误，"
                    "记住一句话：主导力量说的是国有经济。",},
        {"q": "关于「两个毫不动摇」，下面哪一句表述完整准确？",
         "options": [("毫不动摇巩固和发展公有制经济，毫不动摇鼓励、支持、引导非公有制经济发展", True),
                     ("毫不动摇发展公有制经济，逐步减少非公有制经济", False),
                     ("毫不动摇鼓励非公有制经济，逐步取代公有制经济", False)],
         "explain": "两个毫不动摇的完整表述是：毫不动摇巩固和发展公有制经济，毫不动摇鼓励、支持、引导非公有制经济发展。"
                    "<strong>错因提醒：</strong>有的同学<strong>误认为</strong>发展一种所有制就要削弱另一种，"
                    "这与我国基本经济制度的要求并不一致。",}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "公有制为主体、多种所有制经济共同发展", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(251,191,36,.6)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们已经知道国家要发展经济、人民生活要改善（And）；但经济到底建立在什么样的制度之上，谁可以参与生产经营，这些事我们大多只有零散的印象（But）；所以这节课先把我国的基本经济制度一项一项看清（Therefore）。</p>
        </div>
        <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(167,139,250,.45)">
          <p><strong>我国基本经济制度包括三个方面</strong></p>
          <p style="color:var(--text-secondary);margin:6px 0 0">① 公有制为主体、多种所有制经济共同发展；② 按劳分配为主体、多种分配方式并存；③ 社会主义市场经济体制。</p>
        </div>
        <p style="font-size:17px;margin:12px 0 12px">这节课先看第一项：<strong>公有制为主体、多种所有制经济共同发展的生产资料所有制</strong>。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>公有制经济的构成</strong></p>
            <p style="color:var(--muted)">国有经济、集体经济，以及混合所有制经济中的国有成分和集体成分。</p>
          </div>
          <div class="inner-card">
            <p><strong>公有制主体地位的体现</strong></p>
            <p style="color:var(--muted)">公有资产在社会总资产中占优势；国有经济控制国民经济命脉，对经济发展起主导作用。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="公有制为主体、多种所有制经济共同发展的生产资料所有制结构抽象示意图：中心为公有制经济，分支标出国有经济、集体经济、混合所有制经济中的国有成分和集体成分，另一侧标出个体经济、私营经济、外资经济等非公有制经济，用工厂剪影、齿轮、农田、店铺等抽象符号表示，附中文标注">
          <figcaption>概念图：公有制经济包括国有经济、集体经济和混合所有制经济中的国有成分、集体成分 · 抽象示意图，不按比例</figcaption>
        </figure>
        <div class="inner-card">
          <p><strong>非公有制经济的地位与「两个毫不动摇」</strong></p>
          <p style="color:var(--muted)">非公有制经济是社会主义市场经济的重要组成部分，是我国经济社会发展的重要基础。必须毫不动摇巩固和发展公有制经济，毫不动摇鼓励、支持、引导非公有制经济发展。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>公有制经济就是国有经济；也有的同学把「混合所有制经济」一律当作非公有制经济<strong>搞混</strong>。其实集体经济和混合所有制经济中的国有成分、集体成分，同样属于公有制经济——判断的标准是这部分资本归谁所有。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "地铁、电网、航天这样的领域，投入大、周期长、关系国家安全，需要国有经济挑大梁；而街边的餐馆、手机里的应用，则更多由个体、私营和外资经济来提供。"},
    {"lens": "解释它", "text": "为什么两种所有制要共同发展？因为它们各自擅长的事不同：一个守住命脉和底线，一个激发活力和创新，合在一起才能把经济总量做大、把就业岗位做多。"},
    {"lens": "迁移它", "text": "判断一种经济形式属于哪一类，不要看它名字里有没有「国」字，而要看这部分资本归谁所有——这条标准在任何情境里都管用。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：所有制归类台——判断六个经济主体属于哪一类", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一个<strong>经济主体</strong>，再判断它属于<strong>公有制经济</strong>还是<strong>非公有制经济</strong>。判断依据只有一条：这部分资本归谁所有。</p>
        <div class="lab-panel">
          <div id="ow-stage">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">第一步 · 点一个经济主体</div>
            <div class="grid" id="ow-list"></div>
            <div style="font-weight:700;font-size:14px;margin:16px 0 6px">第二步 · 它属于</div>
            <div class="flex-row" style="margin-top:0">
              <button class="choice" data-ow-bin="pub" style="text-align:center">公有制经济</button>
              <button class="choice" data-ow-bin="nonpub" style="text-align:center">非公有制经济</button>
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">归类进度</span><span class="v" id="ow-board">已归类 0 / 6 个主体</span></div>
          </div>
          <p class="result warn" id="ow-out" style="margin-top:12px">先点上面一个经济主体。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">⚙️</span><div><strong>归完回头看：</strong>六个主体排成两类以后，请你想一句话——为什么必须毫不动摇巩固和发展公有制经济，同时毫不动摇鼓励、支持、引导非公有制经济发展？</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "按劳分配为主体、多种分配方式并存，社会保障守住民生底线", TTS["module-2"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(251,191,36,.6)">
          <p><strong>为什么要弄清这一段？</strong></p>
          <p style="color:var(--muted)">我们已经知道谁可以参与生产经营（And）；但生产出来的成果怎么分到每个人手里，遇到生病、失业、年老又怎么办（But）；所以这节课要看清分配制度和社会保障制度（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">我国实行<strong>按劳分配为主体、多种分配方式并存</strong>的分配制度，这是我国基本经济制度的第二项内容。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>按劳分配：</strong>社会主义的分配原则，存在于公有制经济中，多劳多得、少劳少得，是我国分配制度的主体。</div></div>
          <div class="step"><span class="n">2</span><div><strong>按生产要素分配：</strong>劳动、资本、土地、知识、技术、管理、数据等要素由市场评价贡献、按贡献决定报酬。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>居民收入的四类来源：</strong>工资性收入、经营性收入、财产性收入、转移性收入。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>社会保障体系：</strong>主要包括社会保险、社会救助、社会福利、社会优抚，是民生的安全网。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="个人收入分配与社会保障结构抽象示意图：左侧为按劳分配为主体、多种分配方式并存，用天平、上升曲线、抽象握手等符号表示；右侧为社会保障体系，用盾牌、雨伞、楼群剪影等抽象符号表示社会保险、社会救助、社会福利、社会优抚四类，附中文标注">
          <figcaption>概念图：按劳分配为主体、多种分配方式并存；社会保障体系主要包括社会保险、社会救助、社会福利、社会优抚 · 抽象示意图，不按比例</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">最高频的一个错误是<strong>误认为</strong>凡是「工资」都属于按劳分配。其实按劳分配只存在于公有制经济中；私营企业、外资企业职工的工资属于按生产要素分配中的劳动要素。也有同学把「收入怎么分配」和「生活怎么保障」<strong>搞混</strong>，把失业保险、医疗报销当成分配制度。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "同样是一笔钱，来源可能完全不同：岗位工资来自劳动，存款利息来自资本，土地流转租金来自土地，技术入股分红来自技术。"},
    {"lens": "拆开它", "text": "判断分配方式只要问两句话：这笔收入发生在公有制经济里吗？如果不是，它对应哪一种生产要素？两句话问完，答案基本就出来了。"},
    {"lens": "解释它", "text": "为什么既要按劳分配、又要按要素分配？因为只有让各种生产要素都得到合理回报，才能把劳动、资本、技术、管理、数据的积极性都调动起来，把经济发展的蛋糕做大。"},
])}
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "★动手二：分配方式判断台——这笔收入是按什么分配的？", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一个<strong>收入情境</strong>，再判断这笔收入属于<strong>按劳分配</strong>还是<strong>按生产要素分配</strong>中的哪一类要素。</p>
        <div class="lab-panel">
          <div id="db-stage">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">第一步 · 点一个收入情境</div>
            <div class="grid" id="db-list"></div>
            <div style="font-weight:700;font-size:14px;margin:16px 0 6px">第二步 · 这笔收入属于</div>
            <div class="grid grid-2">
              <button class="choice" data-db-ans="A" style="text-align:center">按劳分配</button>
              <button class="choice" data-db-ans="B" style="text-align:center">按生产要素分配（劳动要素）</button>
              <button class="choice" data-db-ans="C" style="text-align:center">按生产要素分配（资本要素）</button>
              <button class="choice" data-db-ans="D" style="text-align:center">按生产要素分配（土地、技术、管理等要素）</button>
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">判断进度</span><span class="v" id="db-board">已判断 0 / 6 个情境</span></div>
          </div>
          <p class="result warn" id="db-out" style="margin-top:12px">先点上面一个收入情境。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">⚖️</span><div><strong>判断完再想一遍：</strong>六个情境里，哪两个属于按劳分配？它们有什么共同点？把这个共同点说出来，你就抓住了按劳分配最要紧的适用范围。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：五条经济表述，逐条校对讲准", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(251,191,36,.6)">
          <p style="margin:0"><strong>情境：</strong>某校经济兴趣小组整理出五条表述。请你当一次校对员，判断哪几条准确、哪一条必须改，并说明依据。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>第一条（准确）：</strong>我国实行公有制为主体、多种所有制经济共同发展的生产资料所有制。</div></div>
          <div class="step"><span class="n">2</span><div><strong>第二条（准确）：</strong>国有经济是国民经济的主导力量，控制国民经济命脉，对经济发展起主导作用。</div></div>
          <div class="step"><span class="n">3</span><div><strong>第三条（准确）：</strong>使市场在资源配置中起决定性作用，同时更好发挥政府作用。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>第四条（必须改）：</strong>「非公有制经济是我国国民经济的主导力量。」——主导力量说的是国有经济；非公有制经济是社会主义市场经济的重要组成部分，是我国经济社会发展的重要基础。</div></div>
          <div class="step"><span class="n green">5</span><div><strong>第五条（准确）：</strong>我国贯彻创新、协调、绿色、开放、共享的新发展理念，推动高质量发展，建设现代化经济体系。</div></div>
        </div>
        <div class="inner-card">
          <p><strong>新发展理念：五个方面各管什么</strong></p>
          <p style="color:var(--muted)">创新是引领发展的第一动力；协调是持续健康发展的内在要求；绿色是永续发展的必要条件；开放是国家繁荣发展的必由之路；共享是中国特色社会主义的本质要求。</p>
        </div>
        <div class="inner-card">
          <p><strong>社会主义市场经济体制的鲜明特征</strong></p>
          <p style="color:var(--muted)">社会主义市场经济体制既具有市场经济的共性，又具有自己鲜明的特征：坚持中国共产党的领导，这是中国特色社会主义最本质的特征，也是社会主义市场经济体制的重要特征；以公有制为主体，这是社会主义市场经济体制的根基；以共同富裕为根本目标，这是社会主义的本质要求。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">最常见的两个错误：一是把国有经济和非公有制经济的地位<strong>搞混</strong>，<strong>误认为</strong>非公有制经济是国民经济的主导力量；二是把「市场决定作用」和「政府作用」<strong>搞混</strong>，<strong>误认为</strong>二者只能取其一。实际上要使市场在资源配置中起决定性作用，同时更好发挥政府作用。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三句话，藏着三个容易想歪的地方", TTS["conceptest-1"], [
        {"q": "关于我国的生产资料所有制，下面哪一句表述准确？",
         "options": [("公有制为主体、多种所有制经济共同发展", True),
                     ("非公有制经济为主体、公有制经济为补充", False),
                     ("各种所有制经济平均发展、地位完全相同", False)],
         "explain": "我国实行公有制为主体、多种所有制经济共同发展的生产资料所有制。"
                    "<strong>错因提醒：</strong>常见错误是把「主体」和「补充」的位置<strong>搞混</strong>，"
                    "也有的同学<strong>误认为</strong>各种所有制经济的地位完全相同——公有制经济居于主体地位，这一点不能含糊。",},
        {"q": "某私营企业职工按月领取计件工资。这笔收入属于：",
         "options": [("按生产要素分配中的劳动要素", True),
                     ("按劳分配", False),
                     ("按资本要素分配", False)],
         "explain": "按劳分配是社会主义的分配原则，只存在于公有制经济中；私营企业属于非公有制经济，"
                    "这里职工的工资属于按生产要素分配中的劳动要素。"
                    "<strong>错因提醒：</strong>这是全课最高频的常见错误——<strong>误认为</strong>凡「工资」都是按劳分配，"
                    "忽略了按劳分配的适用范围。",},
        {"q": "关于我国的社会保障，下面哪一句表述准确？",
         "options": [("社会保障体系主要包括社会保险、社会救助、社会福利、社会优抚", True),
                     ("社会保障就是给所有人发放相同数额的现金", False),
                     ("失业保险属于按劳分配的一种形式", False)],
         "explain": "我国的社会保障体系主要包括社会保险、社会救助、社会福利、社会优抚，它是民生的安全网。"
                    "<strong>错因提醒：</strong>容易出现两种<strong>搞混</strong>：一是把社会保障当成平均发放现金；"
                    "二是把失业保险<strong>误认为</strong>属于分配制度——社会保障和收入分配是两件不同的事。",}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：经济现象与制度对应台，做出你的经济地基卡", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一个<strong>经济现象</strong>，再判断它主要对应我国经济生活中的哪一项<strong>制度或理念</strong>。五个都判断完，你就有了一张属于自己的经济地基卡。</p>
        <div class="lab-panel">
          <div id="sy-stage">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">第一步 · 点一个经济现象</div>
            <div class="grid" id="sy-list"></div>
            <div style="font-weight:700;font-size:14px;margin:16px 0 6px">第二步 · 它主要对应</div>
            <div class="grid" id="sy-opts">
              <button class="choice" data-sy-ans="i1" style="text-align:left">公有制为主体、多种所有制经济共同发展</button>
              <button class="choice" data-sy-ans="i2" style="text-align:left">按劳分配为主体、多种分配方式并存</button>
              <button class="choice" data-sy-ans="i3" style="text-align:left">社会主义市场经济体制</button>
              <button class="choice" data-sy-ans="i4" style="text-align:left">新发展理念</button>
              <button class="choice" data-sy-ans="i5" style="text-align:left">社会保障制度</button>
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">对应进度</span><span class="v" id="sy-board">已对应 0 / 5 个现象</span></div>
          </div>
          <p class="result warn" id="sy-out" style="margin-top:12px">先点上面一个经济现象。</p>
        </div>
        <div class="inner-card" style="margin-top:14px">
          <p><strong>把你的判断写下来：</strong></p>
          <p style="color:var(--muted)">从五个现象里挑一个你最有感触的，用自己的话写一写：它具体体现了哪一项制度或理念，为什么？</p>
          <textarea id="syn-answer" rows="3" placeholder="我选的现象是……它体现了……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，看看制度与理念还用不用得上", TTS["posttest"], [
        {"q": "某职工失业期间按规定领取失业保险金，这属于我国社会保障体系中的：",
         "options": [("社会保险", True),
                     ("社会优抚", False),
                     ("按劳分配", False)],
         "explain": "我国的社会保障体系主要包括社会保险、社会救助、社会福利、社会优抚，其中社会保险是核心内容，"
                    "失业保险属于社会保险。"
                    "<strong>错因提醒：</strong>容易把社会保障与分配制度<strong>搞混</strong>——失业保险不是按劳分配，"
                    "而是社会保障提供的民生保障。",},
        {"q": "某地把燃煤发电改为光伏发电，同时推动城乡区域协调发展。这最直接体现了：",
         "options": [("创新、协调、绿色、开放、共享的新发展理念", True),
                     ("按劳分配为主体、多种分配方式并存", False),
                     ("毫不动摇巩固和发展公有制经济", False)],
         "explain": "绿色是永续发展的必要条件，协调是持续健康发展的内在要求，二者都属于新发展理念的内容。"
                    "<strong>错因提醒：</strong>常见错误是<strong>误认为</strong>绿色发展只是技术问题，"
                    "其实它首先是一条发展理念，回答的是「实现什么样的发展、怎样发展」。",},
        {"q": "关于「两个毫不动摇」，下面哪一句表述完整准确？",
         "options": [("毫不动摇巩固和发展公有制经济，毫不动摇鼓励、支持、引导非公有制经济发展", True),
                     ("毫不动摇扩大国有企业范围，毫不动摇限制民间投资", False),
                     ("毫不动摇发展非公有制经济，毫不动摇减少公有制经济比重", False)],
         "explain": "两个毫不动摇的完整表述是：毫不动摇巩固和发展公有制经济，毫不动摇鼓励、支持、引导非公有制经济发展。"
                    "<strong>错因提醒：</strong>有的同学<strong>误认为</strong>两种所有制此消彼长，"
                    "这与我国基本经济制度的要求并不一致。公有制经济和非公有制经济都是社会主义市场经济的重要组成部分，"
                    "共同推动我国经济社会发展。",}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：制度、分配、保障、理念，四句话说清楚", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>基本经济制度三项内容：</strong>公有制为主体、多种所有制经济共同发展；按劳分配为主体、多种分配方式并存；社会主义市场经济体制。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>所有制：</strong>公有制经济包括国有经济、集体经济和混合所有制经济中的国有成分、集体成分；国有经济是国民经济的主导力量；非公有制经济是社会主义市场经济的重要组成部分；必须坚持两个毫不动摇。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>分配与保障：</strong>按劳分配是社会主义的分配原则，存在于公有制经济中；公有制经济之外实行按生产要素分配；社会保障体系主要包括社会保险、社会救助、社会福利、社会优抚。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>发展理念：</strong>贯彻创新、协调、绿色、开放、共享的新发展理念，推动高质量发展，建设现代化经济体系。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(251,191,36,.6)">
          <p style="margin:0"><strong>一句口诀：</strong>公为主体多种共发展，两个毫不动摇记心间；按劳分配主体在公有，要素贡献也要算；市场决定政府更好办，五大理念高质量；社保四类守底线，共同富裕是答案。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「基本经济制度」「按劳分配」「新发展理念」这三个词，给家里人讲清楚：我们脚下的经济地基是怎么打牢的，它和我们每个人的生活有什么关系。</p>
          <p style="color:var(--muted)">再动一动手：<strong>记一记</strong>家里这个月的三笔收入，分别写清它属于哪一类分配方式，连同你的分析一起写进本子里。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层任务，按自己的节奏来", TTS["homework"], [
        [
            "写出我国基本经济制度的三项内容。",
            "写出「两个毫不动摇」的完整表述。",
            "写出公有制经济包括哪几个部分，并写出社会保障体系主要包括哪几类。",
        ],
        [
            "收集家里或身边的三笔收入，分别判断它属于按劳分配还是按生产要素分配，并写清依据。",
            "用一段话说明国有经济和非公有制经济在国民经济中各自处于什么地位，注意把两者区分清楚。",
        ],
        [
            "结合身边的一个经济现象，说明它体现了创新、协调、绿色、开放、共享的新发展理念中的哪一方面，并写清理由。",
            "结合一个具体事例，说明为什么坚持公有制为主体、多种所有制经济共同发展有利于实现共同富裕。",
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
    "title": "经济与社会：制度地基、发展理念与民生保障",
    "name_en": "Economy and Society",
    "grade": 10,
    "grade_cn": "高一",
    "domain": "economy",
    "domain_cn": "经济与社会",
    "lesson_type": "conceptual-inquiry",
    "version": "1.0.0",
    "description": "面向高中一年级的思想政治课，对应统编《思想政治》必修2《经济与社会》。全课沿「我国的生产资料所有制 → 个人收入分配与社会保障 → 经济发展与制度定位」这条主线展开，落到四件事上。第一件是生产资料所有制：我国基本经济制度包括公有制为主体、多种所有制经济共同发展，按劳分配为主体、多种分配方式并存，社会主义市场经济体制三个方面；公有制经济包括国有经济、集体经济以及混合所有制经济中的国有成分和集体成分；公有制经济的主体地位主要体现在公有资产在社会总资产中占优势、国有经济控制国民经济命脉并对经济发展起主导作用；非公有制经济是社会主义市场经济的重要组成部分，是我国经济社会发展的重要基础；必须毫不动摇巩固和发展公有制经济，毫不动摇鼓励、支持、引导非公有制经济发展。第二件是个人收入分配与社会保障：按劳分配是社会主义的分配原则，存在于公有制经济中，是我国分配制度的主体；在公有制经济之外，劳动、资本、土地、知识、技术、管理、数据等生产要素由市场评价贡献、按贡献决定报酬；居民收入一般分为工资性收入、经营性收入、财产性收入和转移性收入；我国的社会保障体系主要包括社会保险、社会救助、社会福利、社会优抚，是民生的安全网。第三件是经济发展与体制运行：使市场在资源配置中起决定性作用，同时更好发挥政府作用；社会主义市场经济体制既具有市场经济的共性，又具有自己鲜明的特征——坚持中国共产党的领导，这是中国特色社会主义最本质的特征，也是社会主义市场经济体制的重要特征；以公有制为主体，这是社会主义市场经济体制的根基；以共同富裕为根本目标，这是社会主义的本质要求。第四件是新发展理念：贯彻创新、协调、绿色、开放、共享的新发展理念，推动高质量发展，建设现代化经济体系。三个互动台子都能真操作：动手一是「所有制归类台」，六个经济主体分别归入公有制经济或非公有制经济，归错给出判断标准；动手二是本课核心模拟「分配方式判断台」，六个收入情境判断属于按劳分配还是按生产要素分配中的哪一类要素，其中包含「非公有制经济中职工的工资不属于按劳分配」这一最高频易错点；综合任务是「经济现象与制度对应台」，五个经济现象分别对应公有制为主体多种所有制经济共同发展、按劳分配为主体多种分配方式并存、社会主义市场经济体制、新发展理念、社会保障制度五项，判断完合成一张经济地基卡。全课在政治表述上从严把关：一律使用规范全称；基本经济制度的三项内容与两个毫不动摇完整准确；国有经济与非公有制经济的地位不混写；不臆造文件名称与编号，不编造会议细节，不涉及敏感时政细节与人物评价；表述庄重、严谨、积极正面；插图一律为中性简洁抽象教学示意图，不绘制国旗、国徽、党徽、领导人形象与地图，改用齿轮、天平、楼群剪影、上升曲线、抽象握手等中性抽象图形。",
    "tags": ["基本经济制度", "公有制为主体", "两个毫不动摇", "按劳分配", "按生产要素分配", "社会保障", "新发展理念", "社会主义市场经济体制", "高一", "必修2"],
    "standard_ref": "《普通高中思想政治课程标准（2017年版2020年修订）》必修2「经济与社会」——理解我国生产资料所有制与社会主义市场经济体制，把握两个毫不动摇；贯彻新发展理念，建设现代化经济体系，推动高质量发展；理解个人收入分配与社会保障制度，践行社会责任促进社会进步。对应统编《思想政治》必修2：生产资料所有制与经济体制（我国的生产资料所有制；我国的社会主义市场经济体制）；经济发展与社会进步（我国的经济发展；我国的个人收入分配与社会保障）。",
    "hero_question": "我们脚下的经济地基，是由哪些制度一块一块打牢的？",
    "hero_alt": "经济与社会知识结构图：三栏分别为我国基本经济制度、新发展理念、收入分配与社会保障，用齿轮、天平、上升曲线、楼群剪影、抽象握手等抽象符号表示，附中文标注，不含国旗国徽与地图",
    "hero_caption": "经济与社会：基本经济制度（公有制为主体、多种所有制经济共同发展；按劳分配为主体、多种分配方式并存；社会主义市场经济体制）· 新发展理念 · 收入分配与社会保障",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想弄清的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "我国的基本经济制度到底包括哪些内容？", "d": "三项内容分别管什么", "v": "我国的基本经济制度到底包括哪些内容"},
        {"t": "为什么必须坚持公有制为主体、多种所有制经济共同发展？", "d": "公有制经济和非公有制经济各起什么作用", "v": "为什么必须坚持公有制为主体多种所有制经济共同发展"},
        {"t": "我们的收入是按什么分配的？", "d": "按劳分配和按生产要素分配差在哪里", "v": "我们的收入是按什么分配的"},
        {"t": "国家怎样为每个人的生活提供保障？", "d": "社会保障体系都包括哪些内容", "v": "国家怎样为每个人的生活提供保障"},
    ],
    "objectives": [
        "能说出我国基本经济制度的三项内容，能说明公有制为主体、多种所有制经济共同发展，并能说清两个毫不动摇的完整要求",
        "能说出国有经济是国民经济的主导力量，能说出非公有制经济是社会主义市场经济的重要组成部分，并把两者的地位区分清楚",
        "能说出按劳分配为主体、多种分配方式并存的分配制度，能判断一笔收入属于按劳分配还是按生产要素分配，并说出社会保障体系的主要形式",
        "能说出创新、协调、绿色、开放、共享的新发展理念，能结合经济现象说明它对应我国哪一项制度或理念",
    ],
    "objectives_plain": [
        "能说出我国基本经济制度的三项内容和两个毫不动摇的完整要求",
        "能区分国有经济与非公有制经济在国民经济中的不同地位",
        "能判断一笔收入属于按劳分配还是按生产要素分配，并说出社会保障体系的主要形式",
        "能说出新发展理念的五个方面，并把它与经济现象对应起来",
    ],
    "standards": [
        {"content": "理解我国生产资料所有制与社会主义市场经济体制，把握两个毫不动摇。",
         "source": "《普通高中思想政治课程标准（2017年版2020年修订）》必修2 经济与社会"},
        {"content": "贯彻新发展理念，建设现代化经济体系，推动高质量发展。",
         "source": "《普通高中思想政治课程标准（2017年版2020年修订）》必修2 经济与社会"},
        {"content": "理解个人收入分配与社会保障制度，践行社会责任促进社会进步。",
         "source": "《普通高中思想政治课程标准（2017年版2020年修订）》必修2 经济与社会"},
    ],
    "prereqs": ["pol-h-req1"],
    "prereqs_name": "中国特色社会主义",
    "prereqs_meta": "pol-h-req1",
    "leads_to": ["pol-h-req3"],
    "next_meta": "pol-h-req3",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "一条主线：基本经济制度 → 收入分配与保障 → 新发展理念与高质量发展。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能说清我们脚下的经济地基由哪几块构成。",
        "objectives": "看清四件事：基本经济制度三项内容、两种经济形式的地位、分配方式与社会保障、新发展理念。",
        "pretest": "凭现在的理解选就好，选得不准也不扣分，正好知道要重点听哪里。",
        "module-1": "抓住三个方面：公有制经济包括哪些、公有制主体地位体现在哪、非公有制经济处在什么地位。",
        "lab-1": "判断标准只有一条：这部分资本归谁所有。六个主体归完，再看它的地位表述。",
        "module-2": "两条线：按劳分配只存在于公有制经济中；社会保障是民生的安全网，不要和分配制度混淆。",
        "lab-2": "本课最重要的台子：先问这笔收入是不是发生在公有制经济里，再问它对应哪一种生产要素。",
        "worked-example": "五条表述里四条准确、一条必须改。重点：主导力量说的是国有经济。",
        "conceptest-1": "三句话里各藏着一个容易想歪的地方，选完把解释读一遍。",
        "synthesis": "先点现象，再判断它讲的是「谁参与生产」「收入怎么分」「价格谁来定」「怎么发展」还是「生活怎么保障」。",
        "posttest": "出现了失业保险、绿色发展和两个毫不动摇，看看今天学的还用不用得上。",
        "summary": "四句话：基本经济制度三项内容、所有制、分配与保障、新发展理念。",
        "homework": "三层任务，先做前两层；第二层要把每一笔收入的依据写清楚。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是高中思想政治「经济与社会」板块的空缺，对应统编《思想政治》必修2《经济与社会》四课内容。高一学生每天都在和经济打交道，但对「基本经济制度包括哪三项」「国有企业与民营企业的地位有什么不同」「工资为什么有的是按劳分配、有的不是」「失业保险算不算分配」这些问题，往往只有零碎印象，最容易把国有经济与非公有制经济的地位搞混、把按劳分配与按生产要素分配搞混、把分配制度与社会保障搞混。所以全课不讲口号、不背结论，而把内容换成能核对、能判断的制度归属与分配归属。第一层是「我国的生产资料所有制」：明确我国基本经济制度的三项内容；公有制经济包括国有经济、集体经济以及混合所有制经济中的国有成分和集体成分；公有制经济的主体地位主要体现在公有资产在社会总资产中占优势、国有经济控制国民经济命脉并对经济发展起主导作用；非公有制经济是社会主义市场经济的重要组成部分，是我国经济社会发展的重要基础；必须毫不动摇巩固和发展公有制经济，毫不动摇鼓励、支持、引导非公有制经济发展。第二层是「我国的个人收入分配与社会保障」：按劳分配是社会主义的分配原则，存在于公有制经济中，是我国分配制度的主体；在公有制经济之外，劳动、资本、土地、知识、技术、管理、数据等生产要素由市场评价贡献、按贡献决定报酬；居民收入一般分为工资性收入、经营性收入、财产性收入和转移性收入；我国的社会保障体系主要包括社会保险、社会救助、社会福利、社会优抚，是民生的安全网。第三层是「我国的社会主义市场经济体制与经济发展」：使市场在资源配置中起决定性作用，同时更好发挥政府作用；社会主义市场经济体制既具有市场经济的共性，又具有自己鲜明的特征——坚持中国共产党的领导，这是中国特色社会主义最本质的特征，也是社会主义市场经济体制的重要特征；以公有制为主体，这是社会主义市场经济体制的根基；以共同富裕为根本目标，这是社会主义的本质要求；贯彻创新、协调、绿色、开放、共享的新发展理念，推动高质量发展，建设现代化经济体系。三个互动台子都能真操作：动手一是「所有制归类台」，六个经济主体分别归入公有制经济或非公有制经济，其中混合所有制经济中的国有成分是高频易错点；动手二是本课核心模拟「分配方式判断台」，六个收入情境分别判断属于按劳分配还是按生产要素分配中的劳动、资本、土地、技术等要素，判断错时给出区分方法；综合任务是「经济现象与制度对应台」，五个经济现象分别对应公有制为主体多种所有制经济共同发展、按劳分配为主体多种分配方式并存、社会主义市场经济体制、新发展理念、社会保障制度五项，判断完合成一张经济地基卡。全课在政治表述上从严把关：一律使用规范全称；基本经济制度的三项内容与两个毫不动摇完整准确；国有经济与非公有制经济的地位不混写；不臆造文件名称与编号、不编造会议细节、不涉及敏感时政细节与人物评价；表述庄重、严谨、积极正面；插图一律为中性简洁抽象教学示意图，不绘制国旗、国徽、党徽、领导人形象与地图。",
    "plan_table": """| 1 | cover | 经济与社会：制度地基、发展理念与民生保障 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：我们脚下的经济地基由什么构成？ | 起·前测（暴露已有印象与混淆点） |
| 5 | concept | 公有制为主体、多种所有制经济共同发展 | 承·概念一（生产资料所有制） |
| 6 | interactive | 动手一：所有制归类台——判断六个经济主体属于哪一类 | 承·归类台（6 主体 × 2 类） |
| 7 | concept | 按劳分配为主体、多种分配方式并存，社会保障守住民生底线 | 承·概念二（分配与保障） |
| 8 | interactive | ★动手二：分配方式判断台——这笔收入是按什么分配的？ | 承·核心模拟（6 情境 × 4 类分配方式） |
| 9 | concept | 例题示范：五条经济表述，逐条校对讲准 | 转·重难点突破（分步校对 + 纠错） |
| 10 | quiz | 概念测试：三句话，藏着三个容易想歪的地方 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：经济现象与制度对应台，做出你的经济地基卡 | 合·迁移应用（5 现象 → 5 项归属） |
| 12 | quiz | 后测：换几个新情境，看看制度与理念还用不用得上 | 合·后测 |
| 13 | summary | 小结：制度、分配、保障、理念，四句话说清楚 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：我国基本经济制度 / 新发展理念 / 收入分配与社会保障 三栏，用齿轮、天平、上升曲线、楼群剪影、抽象握手等抽象符号表示，附中文标注\n- P5 生产资料所有制结构抽象示意图（已生成）：中心为公有制经济，标出国有经济、集体经济、混合所有制经济中的国有成分和集体成分；另一侧标出个体经济、私营经济、外资经济等非公有制经济\n- P7 分配与社会保障结构抽象示意图（已生成）：按劳分配为主体、多种分配方式并存；社会保障体系主要包括社会保险、社会救助、社会福利、社会优抚，并标注「抽象示意图，不按比例」\n- ★ 全课不绘制国旗、国徽、党徽、领导人形象与地图；涉及国家与制度仅用齿轮、天平、上升曲线、楼群剪影、抽象握手等中性抽象图形\n- ★ 表述口径统一：规范全称一律写准；基本经济制度的三项内容与两个毫不动摇完整；国有经济与非公有制经济的地位不混写\n- 三张图均为中性简洁抽象教学示意图，不使用真人照片风格，不含可识别的真实人物",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
