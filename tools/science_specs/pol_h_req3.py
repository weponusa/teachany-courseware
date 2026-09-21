# -*- coding: utf-8 -*-
"""高中思想政治 · 政治与法治（必修3）—— 补齐知识树「政治与法治」空缺

学科语气（思想政治）：从「谁带领人民治理国家、人民靠什么制度行使权力、国家靠什么治理」这个
真问题切入，用制度归属与职权对应做骨架，用可核对的真实政治生活情境做证据；
结论落在「这一条表述准不准、依据是什么」，不做口号式抒情、不背条文。

★ 政治表述红线（最高优先级，全课统一口径，任何地方不得含糊）：
  · 规范全称一律写准：中国共产党的领导；人民当家作主；依法治国；人民代表大会制度；
    中国共产党领导的多党合作和政治协商制度；民族区域自治制度；基层群众自治制度；
    人民民主专政的社会主义国家；科学立法、严格执法、公正司法、全民守法。
  · 三者关系必须写准：坚持党的领导、人民当家作主、依法治国有机统一，是我国社会主义政治
    发展道路的核心内容；人民当家作主是社会主义民主政治的本质和核心；中国共产党领导是中国
    特色社会主义最本质的特征。
  · 制度层级不得混写：人民代表大会制度是我国的根本政治制度；中国共产党领导的多党合作和
    政治协商制度、民族区域自治制度、基层群众自治制度是我国的基本政治制度（三项）。
  · 民族区域自治必须写准：在国家统一领导下，在各少数民族聚居的地方实行区域自治，设立
    自治机关，行使自治权。不得写成「完全自治」，不得写成「民族自治」。
  · 不臆造文件名称与编号、不编造会议细节、不涉及敏感时政细节与人物评价；表述庄重、严谨、
    积极正面；插图一律为中性简洁抽象教学示意图，不绘制国旗、国徽、党徽、领导人形象、地图，
    改用天平、法典书本、圆形会场、投票箱、盾牌、抽象人群剪影等中性抽象图形。

内容落点（对应统编必修3《政治与法治》三课）：
  ① 中国共产党的领导：历史和人民的选择；中国共产党的先进性；坚持和加强党的全面领导。
  ② 人民当家作主：人民民主专政的社会主义国家；我国的根本政治制度；我国的基本政治制度。
  ③ 全面依法治国：治国理政的基本方式；法治中国建设；全面依法治国的基本要求。

三个互动台子都能真操作：
  动手一 = 「三者有机统一定位台」（六条情境 → 党的领导 / 人民当家作主 / 依法治国）；
  ★核心模拟 动手二 = 「制度与职权对应台」（六条情境 → 四项政治制度，含最高频易错点）；
  综合任务 = 「依法办事流程台」（六条做法 → 科学立法 / 严格执法 / 公正司法 / 全民守法）。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-h-req3"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "先看两件身边的事。社区里，居民通过居民会议讨论决定小区公共事务；人民代表大会会议上，代表们审议并表决政府工作报告。这两件事看起来不一样，背后却是同一套制度在支撑，那就是人民当家作主。那么，谁带领人民治理国家，人民又通过什么制度行使国家权力，国家靠什么来治理？这节课我们把中国共产党的领导、人民当家作主和依法治国这三件事，以及它们之间的有机统一切实弄明白。",
    "problem-anchor": "开始之前，先选一个你真正想弄清的问题：为什么说中国共产党领导是中国特色社会主义最本质的特征？人民当家作主靠哪些制度来保障？全面依法治国是一场怎样的深刻革命？这三者之间又是什么关系？选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出中国共产党领导是中国特色社会主义最本质的特征，能说出党的领导是历史和人民的选择，并能说清坚持和加强党的全面领导的要求。第二，能说出我国是人民民主专政的社会主义国家，能说出人民代表大会制度是我国的根本政治制度，能说出中国共产党领导的多党合作和政治协商制度、民族区域自治制度、基层群众自治制度是我国的基本政治制度。第三，能说出全面依法治国是国家治理的一场深刻革命，能说出科学立法、严格执法、公正司法、全民守法是全面依法治国的基本要求。第四，能说明党的领导、人民当家作主、依法治国是有机统一的，并能结合具体情境判断它主要体现哪一条。",
    "pretest": "先做三道小题，用你现在的理解选就行。选完马上能看到解释，选得不准也没关系，正好知道要重点听哪里。",
    "module-1": "第一件事，中国共产党的领导。要记住三句话。第一句，中国共产党领导是中国特色社会主义最本质的特征，中国共产党是中国特色社会主义事业的领导核心，党的领导是中国特色社会主义制度的最大优势。第二句，党的领导是历史和人民的选择，中国共产党是中国工人阶级的先锋队，同时是中国人民和中华民族的先锋队，全心全意为人民服务是党的根本宗旨。第三句，必须坚持和加强党的全面领导，增强四个意识、坚定四个自信、做到两个维护，把党的领导落实到国家治理的各领域各方面各环节。这里有一个容易想歪的地方要提醒：坚持党的领导，不是用党的工作代替国家机关依法履行职责，而是党总揽全局、协调各方，支持和保证国家机关依法行使职权。",
    "lab-1": "现在请你亲手做一次定位。下面有六条情境，请你先点一条，再判断它主要体现的是中国共产党的领导、人民当家作主，还是依法治国。判断准确了，我会把依据讲清楚；判断错了，我会告诉你容易搞混在哪里。六条都完成，你会看到三者是怎么有机统一起来的。",
    "module-2": "第二件事，人民当家作主。我国是人民民主专政的社会主义国家，国家一切权力属于人民，人民民主专政的本质是人民当家作主。人民当家作主靠制度来保障。我国的根本政治制度是人民代表大会制度，它是人民行使国家权力的根本途径和最高实现形式，全国人民代表大会是最高国家权力机关；人民代表大会制度的组织和活动原则是民主集中制。我国的基本政治制度有三项：中国共产党领导的多党合作和政治协商制度、民族区域自治制度、基层群众自治制度。多党合作的基本方针是长期共存、互相监督、肝胆相照、荣辱与共；中国人民政治协商会议是中国人民爱国统一战线的组织，是中国共产党领导的多党合作和政治协商的重要机构，是我国政治生活中发扬社会主义民主的重要形式。民族区域自治制度，是在国家统一领导下，在各少数民族聚居的地方实行区域自治，设立自治机关，行使自治权。基层群众自治制度，是村民委员会、居民委员会这类基层群众性自治组织实行自我管理、自我服务、自我教育、自我监督的制度。这里有两个常见错误要避开：一是误认为人民代表大会制度是我国的基本政治制度，其实它是根本政治制度；二是把民族区域自治误认为可以脱离国家统一领导。",
    "lab-2": "接下来是这个模块最重要的一个台子：制度与职权对应台。下面有六条情境，请你先点一条，再判断它主要体现我国四项政治制度中的哪一项。判断准确了，我会把这项制度的职权和作用讲一遍；判断错了，我会告诉你最容易搞混在哪里。",
    "worked-example": "我们一起当一次校对员。有四条表述，请你逐条判断。第一条，中国共产党领导是中国特色社会主义最本质的特征，党的领导是中国特色社会主义制度的最大优势。这一条准确。第二条，人民代表大会制度是我国的基本政治制度。这一条必须改，人民代表大会制度是我国的根本政治制度；中国共产党领导的多党合作和政治协商制度、民族区域自治制度、基层群众自治制度，才是我国的基本政治制度。第三条，全面依法治国是国家治理的一场深刻革命，科学立法、严格执法、公正司法、全民守法是全面依法治国的基本要求。这一条准确。第四条，民族区域自治就是在少数民族聚居的地方实行完全自治。这一条必须改，民族区域自治是在国家统一领导下，在各少数民族聚居的地方实行区域自治，设立自治机关，行使自治权；自治权是在国家统一领导之下行使的，不是完全自治。",
    "conceptest-1": "接下来用三道题考考你，每道题里都藏着一个容易想歪的地方。读一读，选一个你认为准确的，再看解释。",
    "synthesis": "最后一件任务交给你：当一次依法办事流程员。全面依法治国的基本要求是科学立法、严格执法、公正司法、全民守法。下面有六条做法，请你分别判断它落在哪一个环节上。六条都判断完，你会得到一张属于自己的依法办事流程图。",
    "posttest": "最后一轮，换几条新情境来考考你。这次会出现居民会议、法律草案公开征求意见和政协委员的调研建议，看看今天学的东西还用不用得上。",
    "summary": "这节课我们弄清楚四件事。第一，中国共产党领导是中国特色社会主义最本质的特征，党的领导是中国特色社会主义制度的最大优势，党的领导是历史和人民的选择，必须坚持和加强党的全面领导。第二，我国是人民民主专政的社会主义国家，国家一切权力属于人民，人民民主专政的本质是人民当家作主。第三，我国的根本政治制度是人民代表大会制度；我国的基本政治制度包括中国共产党领导的多党合作和政治协商制度、民族区域自治制度、基层群众自治制度三项。第四，全面依法治国是国家治理的一场深刻革命，科学立法、严格执法、公正司法、全民守法是全面依法治国的基本要求；坚持党的领导、人民当家作主、依法治国有机统一，是我国社会主义政治发展道路的核心内容。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出我国的根本政治制度和三项基本政治制度的规范名称，并写出全面依法治国的基本要求。第二层能力应用，动手做：收集三条身边的政治生活情境，分别判断它主要体现党的领导、人民当家作主还是依法治国，并写清依据。第三层迁移挑战，选做：结合一个具体事例，写一段话说明党的领导、人民当家作主、依法治国为什么是有机统一的。",
    "knowledge-graph": "这张图展示了这节课在思想政治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域里的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 中国共产党的领导", "lab-1": "动手一 三者有机统一定位台",
    "module-2": "概念二 人民当家作主与我国的政治制度", "lab-2": "★动手二 制度与职权对应台（核心模拟）",
    "worked-example": "例题示范 四条表述逐条校对", "conceptest-1": "概念测试",
    "synthesis": "综合任务 依法办事流程台", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：三者有机统一定位台（六条情境 × 党的领导 / 人民当家作主 / 依法治国） ──
ORG = [
    {"k": "o1", "t": "某地党组织带领群众推进乡村全面振兴，把党中央的部署落到田间地头。", "ans": "lead",
     "why": "这体现的是中国共产党的领导。中国共产党是中国特色社会主义事业的领导核心，党的领导是中国特色社会主义制度的最大优势，必须坚持和加强党的全面领导。",
     "err": "常见错误：看到「群众」「乡村」就一律判成人民当家作主。判断的时候先问一句——这条情境里起领导作用的组织是哪个？"},
    {"k": "o2", "t": "某市人大代表深入社区听取群众意见，把大家的建议带到人民代表大会会议上。", "ans": "people",
     "why": "这体现的是人民当家作主。人民代表大会制度是我国人民行使国家权力的根本途径和最高实现形式，人大代表由人民选举产生，对人民负责、受人民监督。",
     "err": "容易搞混的地方：把「人大代表听取群众意见」误认为只是党的领导的体现。人大是国家权力机关，这里落点在人民当家作主。"},
    {"k": "o3", "t": "某市中级人民法院依法公开审理案件，裁判文书依法向社会公开。", "ans": "law",
     "why": "这体现的是依法治国。公正司法是全面依法治国的基本要求之一，人民法院依法独立公正行使审判权，让人民群众在每一个司法案件中感受到公平正义。",
     "err": "常见错误：把「依法审理」简单归到人民当家作主。有法律、有司法机关依法行使职权的情境，落点在依法治国。"},
    {"k": "o4", "t": "某社区居民召开居民会议，讨论决定小区公共事务的管理方案。", "ans": "people",
     "why": "这体现的是人民当家作主。基层群众自治制度是我国的基本政治制度，居民委员会是基层群众性自治组织，居民依法实行自我管理、自我服务、自我教育、自我监督。",
     "err": "容易搞混的地方：把居民会议误认为行政机关的会议。居民委员会是基层群众性自治组织，不是国家机关，这里是人民当家作主在基层的生动实践。"},
    {"k": "o5", "t": "某地党员干部深入一线，带领群众解决实际困难，把党的宗旨落实在具体行动上。", "ans": "lead",
     "why": "这体现的是中国共产党的领导。全心全意为人民服务是党的根本宗旨，党的领导要落实到国家治理的各领域各方面各环节。",
     "err": "常见错误：只看到「为群众办事」就判成人民当家作主，忽略了这里的主体是党组织和党员干部。"},
    {"k": "o6", "t": "某企业违法排污，生态环境部门依法对其作出行政处罚。", "ans": "law",
     "why": "这体现的是依法治国。严格执法是全面依法治国的基本要求之一，行政机关必须依法履行职责，严格规范公正文明执法。",
     "err": "常见错误：把「政府处罚企业」误认为只是行政管理，看不到它背后是依法治国、依法行政。",
     },
]

# ── 动手二（★核心模拟）：制度与职权对应台 ──
SYS = [
    {"k": "s1", "t": "全国人民代表大会会议期间，代表们听取并审议政府工作报告，对报告进行表决。", "ans": "A",
     "why": "这体现的是人民代表大会制度。它是我国的根本政治制度，是人民行使国家权力的根本途径和最高实现形式；全国人民代表大会是最高国家权力机关，行使立法权、决定权、任免权、监督权，人大代表依法行使审议权、表决权、提案权、质询权。",
     "err": "最容易搞混的一处：把人民代表大会制度误认为我国的基本政治制度。请记准——人民代表大会制度是根本政治制度，基本政治制度有三项。"},
    {"k": "s2", "t": "各民主党派围绕国家重大决策部署开展调研，提出意见建议，与中国共产党进行政治协商。", "ans": "B",
     "why": "这体现的是中国共产党领导的多党合作和政治协商制度，它是我国的基本政治制度。多党合作的基本方针是长期共存、互相监督、肝胆相照、荣辱与共；中国人民政治协商会议是中国人民爱国统一战线的组织，是中国共产党领导的多党合作和政治协商的重要机构，是我国政治生活中发扬社会主义民主的重要形式。",
     "err": "常见错误：把政治协商误认为与人民代表大会制度是同一项制度。前者是我国的基本政治制度，后者是根本政治制度，二者的地位和作用不同。"},
    {"k": "s3", "t": "某自治区人民代表大会依照宪法和法律规定的权限，结合本地实际制定自治条例和单行条例。", "ans": "C",
     "why": "这体现的是民族区域自治制度，它是我国的基本政治制度。民族区域自治是在国家统一领导下，在各少数民族聚居的地方实行区域自治，设立自治机关，行使自治权；自治机关依法行使自治权，制定自治条例和单行条例是其中一项重要内容。",
     "err": "常见错误：把民族区域自治误认为可以脱离国家统一领导，或者误认为凡是带「自治」字样的制度都属于基层群众自治制度。民族区域自治的前提是国家统一领导。"},
    {"k": "s4", "t": "某社区居民召开居民会议，讨论决定小区公共事务，并对居民委员会的工作提出意见。", "ans": "D",
     "why": "这体现的是基层群众自治制度，它是我国的基本政治制度。村民委员会、居民委员会是基层群众性自治组织，实行自我管理、自我服务、自我教育、自我监督，是人民依法直接行使民主权利的重要方式。",
     "err": "常见错误：把居民委员会误认为基层国家机关。居民委员会是基层群众性自治组织，不是国家机关；这里体现的是基层群众自治制度。"},
    {"k": "s5", "t": "某县人大代表在会议期间就群众关心的饮水安全问题，依法向有关部门提出质询。", "ans": "A",
     "why": "这体现的是人民代表大会制度。人大代表是国家权力机关的组成人员，依法行使审议权、表决权、提案权、质询权，通过行使职权反映人民意愿、维护人民利益。",
     "err": "容易搞混的地方：把人大代表的质询误认为行政机关的内部监督。质询是人大代表依法行使职权的方式，落点在人民代表大会制度。"},
    {"k": "s6", "t": "某村村民通过村民会议选举产生村民委员会，讨论决定村内公共事务和公益事业。", "ans": "D",
     "why": "这体现的是基层群众自治制度。村民委员会是村民自我管理、自我服务、自我教育、自我监督的基层群众性自治组织，村民依法直接行使民主权利。",
     "err": "常见错误：把村民委员会误认为一级政府。它不是国家机关，而是基层群众性自治组织，因此归入基层群众自治制度。",
     },
]

# ── 综合任务：依法办事流程台（六条做法 × 四个基本要求） ──
FLOW = [
    {"k": "f1", "t": "立法机关开展立法调研，把法律草案全文向社会公开征求意见，广泛听取各方面建议。", "ans": "L",
     "why": "这落在科学立法。科学立法要求立法体现客观规律、符合经济社会发展要求，坚持科学立法、民主立法、依法立法。"},
    {"k": "f2", "t": "行政机关依法履行职责，严格规范公正文明执法，对违法行为依法查处。", "ans": "X",
     "why": "这落在严格执法。行政机关是执法的主体，必须依法履行职责，坚持严格规范公正文明执法。"},
    {"k": "f3", "t": "人民法院依法独立公正行使审判权，裁判文书依法向社会公开。", "ans": "S",
     "why": "这落在公正司法。公正司法要求司法机关依法独立公正行使职权，让人民群众在每一个司法案件中感受到公平正义。"},
    {"k": "f4", "t": "公民自觉尊法学法守法用法，遇到纠纷时依法表达诉求、依法维护自身权益。", "ans": "Q",
     "why": "这落在全民守法。全民守法要求全体公民都成为社会主义法治的忠实崇尚者、自觉遵守者、坚定捍卫者。"},
    {"k": "f5", "t": "全国人民代表大会常务委员会审议法律草案，并向社会公开征求意见后依法表决通过。", "ans": "L",
     "why": "这落在科学立法。立法机关依照法定权限和程序制定和修改法律，是全面依法治国的前提和基础。"},
    {"k": "f6", "t": "市场监督管理部门依法对销售不合格食品的商家进行调查处理。", "ans": "X",
     "why": "这落在严格执法。行政机关依法查处违法行为，维护市场秩序和人民群众合法权益，体现的是严格执法。",
     },
]

CUSTOM_JS = r"""
/* ============================================================
   pol-h-req3 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 「三者有机统一定位台」：六条情境 → 党的领导 / 人民当家作主 / 依法治国
   3) ★「制度与职权对应台」：六条情境 → 四项政治制度
   4) 「依法办事流程台」：六条做法 → 科学立法 / 严格执法 / 公正司法 / 全民守法
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

  /* ---------- 2. 三者有机统一定位台 ---------- */
  var ORG = __ORG_JSON__;
  var OLABEL = { lead: '中国共产党的领导', people: '人民当家作主', law: '依法治国' };
  var ocStage = document.getElementById('oc-stage');
  if (ocStage) {
    var selO = null;
    var doneO = {};
    var out1 = document.getElementById('oc-out');
    var list1 = document.getElementById('oc-list');
    var board1 = document.getElementById('oc-board');
    function render1() {
      list1.innerHTML = '';
      ORG.forEach(function (O, i) {
        var b = document.createElement('button');
        b.className = 'choice' + (doneO[O.k] ? ' correct' : (selO === O.k ? ' selected' : ''));
        b.style.textAlign = 'left';
        b.innerHTML = '<strong>' + (i + 1) + '.</strong> ' + O.t +
          (doneO[O.k] ? '<br><span style="color:var(--accent-deep);font-size:14px">已定位：' + OLABEL[O.ans] + ' ✓</span>' : '');
        b.addEventListener('click', function () {
          if (doneO[O.k]) {
            selO = O.k;
            out1.className = 'result';
            out1.innerHTML = '<strong>已定位：' + OLABEL[O.ans] + '</strong><br>' + O.why;
            render1();
            return;
          }
          selO = O.k;
          out1.className = 'result warn';
          out1.innerHTML = '<strong>你选了第 ' + (i + 1) + ' 条情境。</strong>现在到下面判断它主要体现哪一条。';
          render1();
        });
        list1.appendChild(b);
      });
      board1.textContent = '已定位 ' + Object.keys(doneO).length + ' / ' + ORG.length + ' 条情境';
    }
    render1();
    document.querySelectorAll('[data-oc-ans]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (!selO) {
          out1.className = 'result warn';
          out1.innerHTML = '先在上面点一条情境，再判断它主要体现哪一条。' +
            '<br><span style="color:var(--muted)">还可以试试：先问两句话——这条情境里起领导作用的主体是谁？依法行使职权的主体又是谁？</span>';
          return;
        }
        var O = null;
        for (var i = 0; i < ORG.length; i++) { if (ORG[i].k === selO) O = ORG[i]; }
        var pick = btn.dataset.ocAns;
        if (pick === O.ans) {
          doneO[O.k] = true;
          out1.className = 'result';
          out1.innerHTML = '<strong>定位准确：' + OLABEL[O.ans] + '</strong><br>' + O.why;
          if (Object.keys(doneO).length === ORG.length) {
            out1.innerHTML += '<br><br><strong>六条情境都定位完了。</strong>' +
              '把三栏合起来看，你会发现：党的领导是人民当家作主和依法治国的根本保证，' +
              '人民当家作主是社会主义民主政治的本质和核心，依法治国是党领导人民治理国家的基本方式。' +
              '坚持党的领导、人民当家作主、依法治国有机统一，是我国社会主义政治发展道路的核心内容。';
          }
          selO = null;
        } else {
          out1.className = 'result warn';
          out1.innerHTML = '<strong>再想一想：这条情境更可能体现「' + OLABEL[O.ans] + '」。</strong>' +
            (O.err ? O.err : '') +
            '<br><span style="color:var(--muted)">还可以试试：换一个角度读一遍，看它是「谁来领导」还是「谁来行使权力」。</span>';
        }
        render1();
      });
    });
  }

  /* ---------- 3. ★ 制度与职权对应台 ---------- */
  var SYS = __SYS_JSON__;
  var SLABEL = {
    A: '人民代表大会制度（根本政治制度）',
    B: '中国共产党领导的多党合作和政治协商制度',
    C: '民族区域自治制度',
    D: '基层群众自治制度'
  };
  var stStage = document.getElementById('st-stage');
  if (stStage) {
    var selS = null;
    var doneS = {};
    var out2 = document.getElementById('st-out');
    var list2 = document.getElementById('st-list');
    var board2 = document.getElementById('st-board');
    function render2() {
      list2.innerHTML = '';
      SYS.forEach(function (S, i) {
        var b = document.createElement('button');
        b.className = 'choice' + (doneS[S.k] ? ' correct' : (selS === S.k ? ' selected' : ''));
        b.style.textAlign = 'left';
        b.innerHTML = '<strong>' + (i + 1) + '.</strong> ' + S.t +
          (doneS[S.k] ? '<br><span style="color:var(--accent-deep);font-size:14px">已对应：' + SLABEL[S.ans] + ' ✓</span>' : '');
        b.addEventListener('click', function () {
          if (doneS[S.k]) {
            selS = S.k;
            out2.className = 'result';
            out2.innerHTML = '<strong>已对应：' + SLABEL[S.ans] + '</strong><br>' + S.why;
            render2();
            return;
          }
          selS = S.k;
          out2.className = 'result warn';
          out2.innerHTML = '<strong>你选了第 ' + (i + 1) + ' 条情境。</strong>现在到下面判断它主要体现哪一项制度。';
          render2();
        });
        list2.appendChild(b);
      });
      board2.textContent = '已对应 ' + Object.keys(doneS).length + ' / ' + SYS.length + ' 条情境';
    }
    render2();
    document.querySelectorAll('[data-st-ans]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (!selS) {
          out2.className = 'result warn';
          out2.innerHTML = '先在上面点一条情境，再判断它主要体现哪一项制度。' +
            '<br><span style="color:var(--muted)">还可以试试：先问一句——这条情境里行使权力的机关或组织，是权力机关、政协，还是自治机关、群众性自治组织？</span>';
          return;
        }
        var S = null;
        for (var i = 0; i < SYS.length; i++) { if (SYS[i].k === selS) S = SYS[i]; }
        var pick = btn.dataset.stAns;
        if (pick === S.ans) {
          doneS[S.k] = true;
          out2.className = 'result';
          out2.innerHTML = '<strong>对应准确：' + SLABEL[S.ans] + '</strong><br>' + S.why;
          if (Object.keys(doneS).length === SYS.length) {
            out2.innerHTML += '<br><br><strong>六条情境都对应完了，这就是我国政治制度的整体轮廓。</strong>' +
              '我国的根本政治制度是人民代表大会制度；' +
              '我国的基本政治制度包括中国共产党领导的多党合作和政治协商制度、民族区域自治制度、基层群众自治制度三项。' +
              '四项制度共同保障人民当家作主。';
          }
          selS = null;
        } else {
          out2.className = 'result warn';
          out2.innerHTML = '<strong>再想一想：这条情境更可能体现「' + SLABEL[S.ans] + '」。</strong>' + S.err +
            '<br><span style="color:var(--muted)">还可以试试：先定制度层级——根本政治制度只有一项，基本政治制度有三项。</span>';
        }
        render2();
      });
    });
  }

  /* ---------- 4. 依法办事流程台 ---------- */
  var FLOW = __FLOW_JSON__;
  var FLABEL = {
    L: '科学立法',
    X: '严格执法',
    S: '公正司法',
    Q: '全民守法'
  };
  var flStage = document.getElementById('fl-stage');
  if (flStage) {
    var selF = null;
    var doneF = {};
    var out3 = document.getElementById('fl-out');
    var list3 = document.getElementById('fl-list');
    var board3 = document.getElementById('fl-board');
    function render3() {
      list3.innerHTML = '';
      FLOW.forEach(function (F, i) {
        var b = document.createElement('button');
        b.className = 'choice' + (doneF[F.k] ? ' correct' : (selF === F.k ? ' selected' : ''));
        b.style.textAlign = 'left';
        b.innerHTML = '<strong>' + (i + 1) + '.</strong> ' + F.t +
          (doneF[F.k] ? '<br><span style="color:var(--accent-deep);font-size:14px">已归入：' + FLABEL[F.ans] + ' ✓</span>' : '');
        b.addEventListener('click', function () {
          if (doneF[F.k]) {
            selF = F.k;
            out3.className = 'result';
            out3.innerHTML = '<strong>已归入：' + FLABEL[F.ans] + '</strong><br>' + F.why;
            render3();
            return;
          }
          selF = F.k;
          out3.className = 'result warn';
          out3.innerHTML = '<strong>你选了第 ' + (i + 1) + ' 条做法。</strong>现在到下面判断它落在哪一个环节。';
          render3();
        });
        list3.appendChild(b);
      });
      board3.textContent = '已归入 ' + Object.keys(doneF).length + ' / ' + FLOW.length + ' 条做法';
    }
    render3();
    document.querySelectorAll('[data-fl-ans]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (!selF) {
          out3.className = 'result warn';
          out3.innerHTML = '先在上面点一条做法，再判断它落在哪一个环节。' +
            '<br><span style="color:var(--muted)">还可以试试：先看主体——立法机关、行政机关、司法机关，还是普通公民？</span>';
          return;
        }
        var F = null;
        for (var i = 0; i < FLOW.length; i++) { if (FLOW[i].k === selF) F = FLOW[i]; }
        var pick = btn.dataset.flAns;
        if (pick === F.ans) {
          doneF[F.k] = true;
          out3.className = 'result';
          out3.innerHTML = '<strong>归入准确：' + FLABEL[F.ans] + '</strong><br>' + F.why;
          if (Object.keys(doneF).length === FLOW.length) {
            out3.innerHTML += '<br><br><strong>六条做法都归完位了，这就是你的依法办事流程图。</strong>' +
              '全面依法治国是国家治理的一场深刻革命。' +
              '科学立法、严格执法、公正司法、全民守法是全面依法治国的基本要求，四者环环相扣：' +
              '立法是前提，执法是关键，司法是保障，守法是基础。' +
              '建设中国特色社会主义法治体系，建设社会主义法治国家，需要四个方面一起用力。';
          }
          selF = null;
        } else {
          out3.className = 'result warn';
          out3.innerHTML = '<strong>再想一想：这条做法更可能落在「' + FLABEL[F.ans] + '」。</strong>' +
            '常见错误是把「严格执法」和「公正司法」<strong>搞混</strong>：' +
            '行政处罚、行政检查这类由行政机关做的事，落点是严格执法；' +
            '审判、检察这类由司法机关依法独立行使职权的事，落点是公正司法。' +
            '<br><span style="color:var(--muted)">还可以试试：先认主体，再定环节。</span>';
        }
        render3();
      });
    });
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__ORG_JSON__', json.dumps(ORG, ensure_ascii=False))
             .replace('__SYS_JSON__', json.dumps(SYS, ensure_ascii=False))
             .replace('__FLOW_JSON__', json.dumps(FLOW, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：这三条表述准不准？", TTS["pretest"], [
        {"q": "关于中国共产党的领导，下面哪一句表述准确？",
         "options": [("中国共产党领导是中国特色社会主义最本质的特征，党的领导是中国特色社会主义制度的最大优势", True),
                     ("中国共产党领导是我国的一项基本政治制度", False),
                     ("党的领导与依法治国是两件互不相干的事", False)],
         "explain": "中国共产党领导是中国特色社会主义最本质的特征，党的领导是中国特色社会主义制度的最大优势。"
                    "<strong>错因提醒：</strong>常见错误是把党的领导和国家政治制度<strong>搞混</strong>——"
                    "党的领导是中国特色社会主义最本质的特征，不是一项具体的政治制度；"
                    "也有的同学<strong>误认为</strong>党的领导与依法治国彼此分离。",},
        {"q": "我国人民行使国家权力、实现人民当家作主的根本途径是：",
         "options": [("人民代表大会制度", True),
                     ("基层群众自治制度", False),
                     ("民族区域自治制度", False)],
         "explain": "人民代表大会制度是我国的根本政治制度，是人民行使国家权力的根本途径和最高实现形式。"
                    "<strong>错因提醒：</strong>这是这一课最高频的常见错误——把人民代表大会制度与基本政治制度"
                    "<strong>搞混</strong>。请记准：根本政治制度只有一项，就是人民代表大会制度。",},
        {"q": "全面依法治国的基本要求是：",
         "options": [("科学立法、严格执法、公正司法、全民守法", True),
                     ("有法可依、有法必依、执法必严、违法必究", False),
                     ("以德治国、以法治国、依法行政、依法办事", False)],
         "explain": "全面依法治国的基本要求是科学立法、严格执法、公正司法、全民守法，四者环环相扣。"
                    "<strong>错因提醒：</strong>这四句容易与其他提法<strong>搞混</strong>，"
                    "有的同学凭印象随意拼凑，结果表述不完整也不准确。",}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "中国共产党领导是中国特色社会主义最本质的特征", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(251,191,36,.6)">
          <p><strong>为什么要先弄清这一件事？</strong></p>
          <p style="color:var(--muted)">我们已经知道，国家一切权力属于人民，人民要来管理国家事务（And）；但人民通过谁来组织、来带领、来凝聚力量，这件事我们往往只有零散的印象（But）；所以这节课先把中国共产党的领导这一段看清（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:12px 0 12px">先记住第一句话：<strong>中国共产党领导是中国特色社会主义最本质的特征</strong>，中国共产党是中国特色社会主义事业的领导核心，<strong>党的领导是中国特色社会主义制度的最大优势</strong>。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>历史和人民的选择</strong></p>
            <p style="color:var(--muted)">党的领导地位不是自封的，而是在长期奋斗中形成的，是历史和人民的选择。</p>
          </div>
          <div class="inner-card">
            <p><strong>中国共产党的先进性</strong></p>
            <p style="color:var(--muted)">中国共产党是中国工人阶级的先锋队，同时是中国人民和中华民族的先锋队；全心全意为人民服务是党的根本宗旨。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="党的领导、人民当家作主、依法治国有机统一抽象示意图：三个圆形节点对称排列，分别标注中国共产党的领导、人民当家作主、依法治国，用向上的箭头、圆形会场俯视图形、天平与法典书本等中性抽象符号表示，三者之间用等边连接线相连，附中文标注，不含国旗国徽与地图">
          <figcaption>概念图：坚持党的领导、人民当家作主、依法治国有机统一，是我国社会主义政治发展道路的核心内容 · 抽象示意图，不按比例</figcaption>
        </figure>
        <div class="inner-card">
          <p><strong>坚持和加强党的全面领导</strong></p>
          <p style="color:var(--muted)">必须坚持和加强党的全面领导，增强「四个意识」、坚定「四个自信」、做到「两个维护」，把党的领导落实到国家治理的各领域各方面各环节。党的领导是人民当家作主和依法治国的根本保证。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>坚持党的领导就是用党的工作代替国家机关依法履行职责。正确的理解是：党总揽全局、协调各方，支持和保证国家机关依法行使职权，而不是包办代替。也有同学把党的领导<strong>搞混</strong>成一项具体的政治制度——党的领导是中国特色社会主义最本质的特征，这一点要写准。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "社区里居民开会讨论小区事务，人民代表大会会议上代表审议报告，行政处罚决定书上盖着行政机关的公章——这些场景背后，都站着同一套政治逻辑。"},
    {"lens": "拆开它", "text": "判断一条情境落在党的领导、人民当家作主还是依法治国，先问两句：起领导作用的主体是谁？依法行使职权的主体又是谁？两句话问完，落点基本就清楚了。"},
    {"lens": "解释它", "text": "为什么必须三者有机统一？因为没有党的领导，人民当家作主和依法治国就失去根本保证；没有人民当家作主，国家权力就会脱离人民；没有依法治国，国家治理就缺少稳定的制度和程序支撑。三者互为条件、相互支撑。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：三者有机统一定位台——这条情境主要体现哪一条？", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一条<strong>情境</strong>，再判断它主要体现<strong>中国共产党的领导</strong>、<strong>人民当家作主</strong>还是<strong>依法治国</strong>。</p>
        <div class="lab-panel">
          <div id="oc-stage">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">第一步 · 点一条情境</div>
            <div class="grid" id="oc-list"></div>
            <div style="font-weight:700;font-size:14px;margin:16px 0 6px">第二步 · 它主要体现</div>
            <div class="grid grid-3">
              <button class="choice" data-oc-ans="lead" style="text-align:center">中国共产党的领导</button>
              <button class="choice" data-oc-ans="people" style="text-align:center">人民当家作主</button>
              <button class="choice" data-oc-ans="law" style="text-align:center">依法治国</button>
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">定位进度</span><span class="v" id="oc-board">已定位 0 / 6 条情境</span></div>
          </div>
          <p class="result warn" id="oc-out" style="margin-top:12px">先点上面一条情境。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧭</span><div><strong>定位完再想一遍：</strong>三栏里的情境能不能互相替换？如果不能，说明这三件事各有各的位置，谁也代替不了谁——这就是「有机统一」的第一层意思。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "人民当家作主：一项根本政治制度与三项基本政治制度", TTS["module-2"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(251,191,36,.6)">
          <p><strong>为什么要弄清这一段？</strong></p>
          <p style="color:var(--muted)">我们已经知道国家一切权力属于人民（And）；但人民到底通过哪些制度来行使权力、参与管理，这些制度的层级和分工又是什么（But）；所以这节课要看清我国政治制度的整体轮廓（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">我国是<strong>人民民主专政的社会主义国家</strong>，国家一切权力属于人民，人民民主专政的本质是<strong>人民当家作主</strong>。人民当家作主，靠制度来保障。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>根本政治制度（一项）：</strong>人民代表大会制度。它是人民行使国家权力的根本途径和最高实现形式；全国人民代表大会是最高国家权力机关；人民代表大会制度的组织和活动原则是民主集中制。</div></div>
          <div class="step"><span class="n">2</span><div><strong>基本政治制度之一：</strong>中国共产党领导的多党合作和政治协商制度。多党合作的基本方针是长期共存、互相监督、肝胆相照、荣辱与共；中国人民政治协商会议是中国人民爱国统一战线的组织，是中国共产党领导的多党合作和政治协商的重要机构，是我国政治生活中发扬社会主义民主的重要形式。</div></div>
          <div class="step"><span class="n">3</span><div><strong>基本政治制度之二：</strong>民族区域自治制度。在国家统一领导下，在各少数民族聚居的地方实行区域自治，设立自治机关，行使自治权。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>基本政治制度之三：</strong>基层群众自治制度。村民委员会、居民委员会是基层群众性自治组织，实行自我管理、自我服务、自我教育、自我监督。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="我国政治制度结构抽象示意图：上方一个方框代表人民代表大会制度并注明根本政治制度，下方三个方框并排代表三项基本政治制度，图中标签为简写，用圆形会场俯视图形、抽象方块、抽象桥形、抽象人群剪影等中性符号表示，附中文标注，不含国旗国徽与地图">
          <figcaption>概念图：人民代表大会制度是我国的根本政治制度；中国共产党领导的多党合作和政治协商制度、民族区域自治制度、基层群众自治制度是我国的基本政治制度 · 图中标签为简写，抽象示意图，不按比例</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">两个高频错误：一是<strong>误认为</strong>人民代表大会制度是我国的基本政治制度——它是<strong>根本政治制度</strong>，基本政治制度有三项；二是把民族区域自治<strong>误认为</strong>可以脱离国家统一领导，写成「完全自治」「民族自治」。规范的表述是：在国家统一领导下，在各少数民族聚居的地方实行区域自治，设立自治机关，行使自治权。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "同样叫「自治」，含义并不一样：民族区域自治是民族聚居地方依法行使自治权，基层群众自治是村（居）民依法直接管理自己的事务。名字相近，位置不同。"},
    {"lens": "比较它", "text": "把四项制度排成一排看层级：人民代表大会制度在最高一层，直接关系国家权力的产生和行使；另外三项在基本层面，从政党协商、民族事务、基层治理三个方向把人民当家作主落到细处。"},
    {"lens": "迁移它", "text": "遇到一个陌生的政治生活情境，先看行使权力的主体是谁：权力机关、政协、自治机关，还是群众性自治组织？主体认准了，制度归属基本不会错。"},
])}
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "★动手二：制度与职权对应台——它体现了哪一项制度？", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一条<strong>情境</strong>，再判断它主要体现我国<strong>四项政治制度</strong>中的哪一项。判断准确了，我会把这项制度的职权和作用讲一遍。</p>
        <div class="lab-panel">
          <div id="st-stage">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">第一步 · 点一条情境</div>
            <div class="grid" id="st-list"></div>
            <div style="font-weight:700;font-size:14px;margin:16px 0 6px">第二步 · 它体现的是</div>
            <div class="grid grid-2">
              <button class="choice" data-st-ans="A" style="text-align:left">人民代表大会制度（根本政治制度）</button>
              <button class="choice" data-st-ans="B" style="text-align:left">中国共产党领导的多党合作和政治协商制度</button>
              <button class="choice" data-st-ans="C" style="text-align:left">民族区域自治制度</button>
              <button class="choice" data-st-ans="D" style="text-align:left">基层群众自治制度</button>
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">对应进度</span><span class="v" id="st-board">已对应 0 / 6 条情境</span></div>
          </div>
          <p class="result warn" id="st-out" style="margin-top:12px">先点上面一条情境。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🏛️</span><div><strong>对应完再想一遍：</strong>六条情境里，哪一项制度出现了两次？它为什么出现的次数最多？顺着这个问题想下去，你就理解了「根本政治制度」这个说法的分量。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：四条表述，逐条校对讲准", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(251,191,36,.6)">
          <p style="margin:0"><strong>情境：</strong>某校政治学习小组整理出四条表述。请你当一次校对员，判断哪几条准确、哪几条必须改，并说明依据。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>第一条（准确）：</strong>中国共产党领导是中国特色社会主义最本质的特征，党的领导是中国特色社会主义制度的最大优势。</div></div>
          <div class="step"><span class="n">2</span><div><strong>第二条（必须改）：</strong>「人民代表大会制度是我国的基本政治制度。」——人民代表大会制度是我国的<strong>根本政治制度</strong>；中国共产党领导的多党合作和政治协商制度、民族区域自治制度、基层群众自治制度，才是我国的<strong>基本政治制度</strong>。</div></div>
          <div class="step"><span class="n">3</span><div><strong>第三条（准确）：</strong>全面依法治国是国家治理的一场深刻革命，科学立法、严格执法、公正司法、全民守法是全面依法治国的基本要求。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>第四条（必须改）：</strong>「民族区域自治就是在少数民族聚居的地方实行完全自治。」——民族区域自治是在<strong>国家统一领导下</strong>，在各少数民族聚居的地方实行区域自治，设立自治机关，行使自治权。自治权在国家统一领导之下行使，不是完全自治，也不能简写成「民族自治」。</div></div>
        </div>
        <div class="inner-card">
          <p><strong>为什么第二条最容易错？</strong></p>
          <p style="color:var(--muted)">因为四项政治制度经常被并排提起，容易让人以为它们处在同一个层级上。其实层级很清楚：人民代表大会制度是根本政治制度，直接关系国家权力的产生和行使；其余三项是基本政治制度，分别从政党协商、民族事务、基层治理三个方向把人民当家作主落到实处。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">还有两处容易<strong>搞混</strong>：「党的领导」是中国共产党的领导，它<strong>不是</strong>一项具体的政治制度，写制度名称的时候不能把党的领导列进四项政治制度；「基层群众自治」与「民族区域自治」也容易被<strong>误认为</strong>是一回事，前者是村（居）民依法直接管理自己的事务，后者是在少数民族聚居地方依法行使自治权。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三句话，藏着三个容易想歪的地方", TTS["conceptest-1"], [
        {"q": "关于我国的人民代表大会制度，下面哪一句表述准确？",
         "options": [("人民代表大会制度是我国的根本政治制度，保障人民当家作主", True),
                     ("人民代表大会制度是我国的基本政治制度之一", False),
                     ("人民代表大会制度是我国的基本经济制度之一", False)],
         "explain": "人民代表大会制度是我国的根本政治制度，是人民行使国家权力的根本途径和最高实现形式。"
                    "<strong>错因提醒：</strong>这是全课最高频的常见错误——把根本政治制度与基本政治制度"
                    "<strong>搞混</strong>。基本政治制度有三项，不包括人民代表大会制度。",},
        {"q": "某自治区人民代表大会依照宪法和法律规定的权限，结合本地实际制定自治条例。这体现的是：",
         "options": [("民族区域自治制度", True),
                     ("基层群众自治制度", False),
                     ("中国共产党领导的多党合作和政治协商制度", False)],
         "explain": "民族区域自治制度是我国的基本政治制度。在国家统一领导下，在各少数民族聚居的地方实行区域自治，"
                    "设立自治机关，行使自治权，自治机关依法制定自治条例和单行条例是重要内容之一。"
                    "<strong>错因提醒：</strong>常见错误是<strong>误认为</strong>凡是带「自治」二字都属于基层群众自治制度，"
                    "看到「自治区」「自治条例」就应该想到民族区域自治制度。",},
        {"q": "关于党的领导、人民当家作主、依法治国的关系，下面哪一句表述准确？",
         "options": [("三者有机统一，是我国社会主义政治发展道路的核心内容", True),
                     ("三者各自独立，只需要做好其中一项", False),
                     ("党的领导与依法治国之间没有联系", False)],
         "explain": "坚持党的领导、人民当家作主、依法治国有机统一，是我国社会主义政治发展道路的核心内容。"
                    "党的领导是人民当家作主和依法治国的根本保证，人民当家作主是社会主义民主政治的本质和核心，"
                    "依法治国是党领导人民治理国家的基本方式。"
                    "<strong>错因提醒：</strong>把三者<strong>搞混</strong>成互相独立、可以只取其一，是常见的理解偏差；"
                    "三者互为条件、相互支撑，不能割裂。",}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：依法办事流程台——这条做法落在哪个环节？", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一条<strong>做法</strong>，再判断它落在<strong>科学立法</strong>、<strong>严格执法</strong>、<strong>公正司法</strong>还是<strong>全民守法</strong>。六条都归完位，你就得到了一张依法办事流程图。</p>
        <div class="lab-panel">
          <div id="fl-stage">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">第一步 · 点一条做法</div>
            <div class="grid" id="fl-list"></div>
            <div style="font-weight:700;font-size:14px;margin:16px 0 6px">第二步 · 它落在</div>
            <div class="grid grid-2">
              <button class="choice" data-fl-ans="L" style="text-align:center">科学立法</button>
              <button class="choice" data-fl-ans="X" style="text-align:center">严格执法</button>
              <button class="choice" data-fl-ans="S" style="text-align:center">公正司法</button>
              <button class="choice" data-fl-ans="Q" style="text-align:center">全民守法</button>
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">归入进度</span><span class="v" id="fl-board">已归入 0 / 6 条做法</span></div>
          </div>
          <p class="result warn" id="fl-out" style="margin-top:12px">先点上面一条做法。</p>
        </div>
        <div class="inner-card" style="margin-top:14px">
          <p><strong>把你的判断写下来：</strong></p>
          <p style="color:var(--muted)">四个环节里，你认为哪一个最贴近我们学生的日常生活？写一写你能从哪一件小事做起，为什么这样做属于依法办事。</p>
          <textarea id="syn-answer" rows="3" placeholder="我认为最贴近我们的是……我能从……做起，因为……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几条新情境，看看制度与环节还用不用得上", TTS["posttest"], [
        {"q": "某社区居民通过居民会议讨论决定小区公共事务，并对居民委员会的工作提出意见。这体现的是：",
         "options": [("基层群众自治制度", True),
                     ("民族区域自治制度", False),
                     ("人民代表大会制度", False)],
         "explain": "村民委员会、居民委员会是基层群众性自治组织，实行自我管理、自我服务、自我教育、自我监督，"
                    "基层群众自治制度是我国的基本政治制度。"
                    "<strong>错因提醒：</strong>容易把「自治」二字<strong>搞混</strong>——居民委员会不是国家机关，"
                    "这里体现的是基层群众自治制度，不是民族区域自治制度，也不是人民代表大会制度。",},
        {"q": "全国人民代表大会常务委员会审议法律草案，并把草案全文向社会公开征求意见后依法表决通过。这主要体现：",
         "options": [("科学立法", True),
                     ("公正司法", False),
                     ("全民守法", False)],
         "explain": "立法机关依照法定权限和程序制定和修改法律，坚持科学立法、民主立法、依法立法，"
                    "这是全面依法治国的前提和基础。"
                    "<strong>错因提醒：</strong>常见错误是把立法环节<strong>误认为</strong>属于司法环节。"
                    "请看清主体：立法机关制定法律是科学立法，司法机关依法独立公正行使职权才是公正司法。",},
        {"q": "各民主党派围绕国家重大决策部署开展调研、提出意见建议，与中国共产党进行政治协商。这体现的是：",
         "options": [("中国共产党领导的多党合作和政治协商制度", True),
                     ("人民代表大会制度", False),
                     ("基层群众自治制度", False)],
         "explain": "中国共产党领导的多党合作和政治协商制度是我国的基本政治制度。"
                    "中国人民政治协商会议是中国人民爱国统一战线的组织，是中国共产党领导的多党合作和政治协商的重要机构，"
                    "是我国政治生活中发扬社会主义民主的重要形式。"
                    "<strong>错因提醒：</strong>常见错误是把政治协商<strong>误认为</strong>与人民代表大会制度是同一项制度，"
                    "二者一个是基本政治制度，一个是根本政治制度，不能搞混。",}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把三者有机统一说清楚", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>党的领导：</strong>中国共产党领导是中国特色社会主义最本质的特征，党的领导是中国特色社会主义制度的最大优势；党的领导是历史和人民的选择；必须坚持和加强党的全面领导。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>人民当家作主：</strong>我国是人民民主专政的社会主义国家，国家一切权力属于人民；根本政治制度是人民代表大会制度；基本政治制度包括中国共产党领导的多党合作和政治协商制度、民族区域自治制度、基层群众自治制度三项。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>依法治国：</strong>全面依法治国是国家治理的一场深刻革命；科学立法、严格执法、公正司法、全民守法是全面依法治国的基本要求；建设中国特色社会主义法治体系，建设社会主义法治国家。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>三者关系：</strong>坚持党的领导、人民当家作主、依法治国有机统一，是我国社会主义政治发展道路的核心内容。党的领导是根本保证，人民当家作主是本质和核心，依法治国是党领导人民治理国家的基本方式。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(251,191,36,.6)">
          <p style="margin:0"><strong>一句口诀：</strong>党的领导最本质，人民当家作主人；根本制度人代会，基本制度有三项；科学立法到守法，四环相扣治国方；三者有机统一好，政治发展大方向。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「中国共产党的领导」「人民当家作主」「依法治国」这三个词，给家里人讲清楚：我们国家的政治制度是怎么运转的，它和我们每个人的生活有什么关系。</p>
          <p style="color:var(--muted)">再动一动手：<strong>记一记</strong>你身边最近发生的一件公共事务（比如小区改造、村里修路），写清它是通过哪一项制度决定的，连同你的分析一起写进本子里。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层任务，按自己的节奏来", TTS["homework"], [
        [
            "写出我国的根本政治制度的规范名称，并写出我国基本政治制度的三项内容。",
            "写出全面依法治国的基本要求。",
            "写出中国共产党领导在中国特色社会主义中的地位，并写出党的领导是历史和人民的选择这一判断的依据。",
        ],
        [
            "收集三条身边的政治生活情境，分别判断它主要体现党的领导、人民当家作主还是依法治国，并写清依据。",
            "用一段话说明人民代表大会制度与我国基本政治制度在层级上有什么不同，注意把两者区分清楚。",
        ],
        [
            "结合一个具体事例，写一段话说明党的领导、人民当家作主、依法治国为什么是有机统一的。",
            "选取一项你熟悉的公共事务，说明它从提出到决定经过了哪些环节，并指出其中体现了全面依法治国的哪一项基本要求。",
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
    "title": "政治与法治：党的领导、人民当家作主、依法治国有机统一",
    "name_en": "Politics and the Rule of Law",
    "grade": 11,
    "grade_cn": "高二",
    "domain": "politics-law",
    "domain_cn": "政治与法治",
    "lesson_type": "conceptual-inquiry",
    "version": "1.0.0",
    "description": "面向高中二年级的思想政治课，对应统编《思想政治》必修3《政治与法治》。全课沿「中国共产党的领导 → 人民当家作主与我国的政治制度 → 全面依法治国 → 三者有机统一」这条主线展开，落到四件事上。第一件是中国共产党的领导：中国共产党领导是中国特色社会主义最本质的特征，中国共产党是中国特色社会主义事业的领导核心，党的领导是中国特色社会主义制度的最大优势；党的领导是历史和人民的选择；中国共产党是中国工人阶级的先锋队，同时是中国人民和中华民族的先锋队，全心全意为人民服务是党的根本宗旨；必须坚持和加强党的全面领导，把党的领导落实到国家治理的各领域各方面各环节。第二件是人民当家作主：我国是人民民主专政的社会主义国家，国家一切权力属于人民，人民民主专政的本质是人民当家作主；我国的根本政治制度是人民代表大会制度，它是人民行使国家权力的根本途径和最高实现形式，全国人民代表大会是最高国家权力机关，人民代表大会制度的组织和活动原则是民主集中制；我国的基本政治制度包括中国共产党领导的多党合作和政治协商制度、民族区域自治制度、基层群众自治制度三项。第三件是全面依法治国：全面依法治国是国家治理的一场深刻革命；科学立法、严格执法、公正司法、全民守法是全面依法治国的基本要求；建设中国特色社会主义法治体系，建设社会主义法治国家。第四件是三者的关系：坚持党的领导、人民当家作主、依法治国有机统一，是我国社会主义政治发展道路的核心内容；党的领导是人民当家作主和依法治国的根本保证，人民当家作主是社会主义民主政治的本质和核心，依法治国是党领导人民治理国家的基本方式。三个互动台子都能真操作：动手一是「三者有机统一定位台」，六条真实政治生活情境分别定位到党的领导、人民当家作主、依法治国；动手二是本课核心模拟「制度与职权对应台」，六条情境分别对应我国四项政治制度，其中包含「人民代表大会制度是根本政治制度而非基本政治制度」这一最高频易错点；综合任务是「依法办事流程台」，六条做法分别归入科学立法、严格执法、公正司法、全民守法四个环节，归完合成一张依法办事流程图。全课在政治表述上从严把关：一律使用规范全称；党的领导、人民当家作主、依法治国三者有机统一的表述完整准确；根本政治制度与基本政治制度的层级不混写；民族区域自治的表述不含「完全自治」「民族自治」等偏差说法；不臆造文件名称与编号，不编造会议细节，不涉及敏感时政细节与人物评价；表述庄重、严谨、积极正面；插图一律为中性简洁抽象教学示意图，不绘制国旗、国徽、党徽、领导人形象与地图，改用天平、法典书本、圆形会场俯视图、投票箱、盾牌、抽象人群剪影等中性抽象图形。",
    "tags": ["中国共产党的领导", "人民当家作主", "依法治国", "人民代表大会制度", "基本政治制度", "全面依法治国", "高二", "必修3"],
    "standard_ref": "《普通高中思想政治课程标准（2017年版2020年修订）》必修3「政治与法治」——理解中国共产党领导是中国特色社会主义最本质的特征；理解人民当家作主是社会主义民主政治的本质和核心；理解全面依法治国是国家治理的一场深刻革命，建设法治中国。对应统编《思想政治》必修3：中国共产党的领导（历史和人民的选择；中国共产党的先进性；坚持和加强党的全面领导）；人民当家作主（人民民主专政的社会主义国家；我国的根本政治制度；我国的基本政治制度）；全面依法治国（治国理政的基本方式；法治中国建设；全面依法治国的基本要求）。",
    "hero_question": "谁带领人民治理国家，人民又通过哪些制度行使国家权力？",
    "hero_alt": "政治与法治知识结构图：三栏分别为中国共产党的领导、人民当家作主、依法治国，用向上的箭头、圆形会场俯视图形、投票箱、天平、法典书本、盾牌等抽象符号表示，附中文标注，不含国旗国徽党徽与地图",
    "hero_caption": "政治与法治：中国共产党的领导 · 人民当家作主（一项根本政治制度与三项基本政治制度）· 全面依法治国——三者有机统一",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想弄清的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "为什么说中国共产党领导是中国特色社会主义最本质的特征？", "d": "党的领导地位是怎么形成的", "v": "为什么说中国共产党领导是中国特色社会主义最本质的特征"},
        {"t": "人民当家作主靠哪些制度来保障？", "d": "根本政治制度和基本政治制度各是什么", "v": "人民当家作主靠哪些制度来保障"},
        {"t": "全面依法治国是一场怎样的深刻革命？", "d": "全面依法治国的基本要求有哪几条", "v": "全面依法治国是一场怎样的深刻革命"},
        {"t": "党的领导、人民当家作主、依法治国之间是什么关系？", "d": "为什么说三者有机统一", "v": "党的领导人民当家作主依法治国之间是什么关系"},
    ],
    "objectives": [
        "能说出中国共产党领导是中国特色社会主义最本质的特征，能说出党的领导是历史和人民的选择，并能说清坚持和加强党的全面领导的要求",
        "能说出我国是人民民主专政的社会主义国家，能说出人民代表大会制度是我国的根本政治制度",
        "能说出中国共产党领导的多党合作和政治协商制度、民族区域自治制度、基层群众自治制度是我国的基本政治制度，并能结合情境判断制度归属",
        "能说出全面依法治国的基本要求，能说明党的领导、人民当家作主、依法治国是有机统一的",
    ],
    "objectives_plain": [
        "能说出中国共产党领导是中国特色社会主义最本质的特征和坚持党的全面领导的要求",
        "能说出我国的根本政治制度是人民代表大会制度",
        "能说出我国基本政治制度的三项内容，并能结合情境判断制度归属",
        "能说出全面依法治国的基本要求，并能说明三者有机统一",
    ],
    "standards": [
        {"content": "理解中国共产党领导是中国特色社会主义最本质的特征。",
         "source": "《普通高中思想政治课程标准（2017年版2020年修订）》必修3 政治与法治"},
        {"content": "理解人民当家作主是社会主义民主政治的本质和核心。",
         "source": "《普通高中思想政治课程标准（2017年版2020年修订）》必修3 政治与法治"},
        {"content": "理解全面依法治国是国家治理的一场深刻革命，建设法治中国。",
         "source": "《普通高中思想政治课程标准（2017年版2020年修订）》必修3 政治与法治"},
    ],
    "prereqs": ["pol-h-req2"],
    "prereqs_name": "经济与社会",
    "prereqs_meta": "pol-h-req2",
    "leads_to": ["pol-h-req4"],
    "next_meta": "pol-h-req4",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "两条线索：谁带领人民治理国家，人民靠哪些制度行使权力。带着这两个问题开始。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能把党的领导、人民当家作主、依法治国三条各自说准，还能说清它们的关系。",
        "objectives": "看清四件事：党的领导地位、人民当家作主、我国的政治制度、全面依法治国的基本要求与三者有机统一。",
        "pretest": "凭现在的理解选就好，选得不准也不扣分，正好知道要重点听哪里。",
        "module-1": "抓住三句话：最本质的特征、历史和人民的选择、坚持和加强党的全面领导。",
        "lab-1": "先问两句：起领导作用的主体是谁？依法行使职权的主体又是谁？两句话问完，落点就出来了。",
        "module-2": "层级要分清：根本政治制度只有一项，是人民代表大会制度；基本政治制度有三项。",
        "lab-2": "本课最重要的台子：先认行使权力的主体——权力机关、政协、自治机关还是群众性自治组织。",
        "worked-example": "四条表述里两条准确、两条必须改。重点：人民代表大会制度是根本政治制度；民族区域自治在国家统一领导下。",
        "conceptest-1": "三句话里各藏着一个容易想歪的地方，选完把解释读一遍。",
        "synthesis": "先看主体再定环节：立法机关、行政机关、司法机关，还是普通公民？",
        "posttest": "出现了居民会议、法律草案公开征求意见和政协委员的调研建议，看看今天学的还用不用得上。",
        "summary": "四句话：党的领导、人民当家作主、依法治国、三者有机统一。",
        "homework": "三层任务，先做前两层；第二层要把每一条情境的依据写清楚。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是高中思想政治「政治与法治」板块的空缺，对应统编《思想政治》必修3《政治与法治》三课内容。高二学生每天都在经历政治生活，但对「中国共产党领导为什么是最本质的特征」「人民代表大会制度与三项基本政治制度处在什么层级」「民族区域自治和基层群众自治差在哪里」「党的领导、人民当家作主、依法治国为什么必须有机统一」这些问题，往往只有零碎印象，最容易把根本政治制度与基本政治制度搞混、把政治协商与人民代表大会制度搞混、把两种「自治」搞混、把党的领导和国家政治制度搞混。所以全课不讲口号、不背结论，而把内容换成能核对、能判断的制度归属与职权对应。第一层是「中国共产党的领导」：明确中国共产党领导是中国特色社会主义最本质的特征，党的领导是中国特色社会主义制度的最大优势，党的领导是历史和人民的选择，中国共产党是中国工人阶级的先锋队、同时是中国人民和中华民族的先锋队，全心全意为人民服务是党的根本宗旨；坚持和加强党的全面领导，把党的领导落实到国家治理的各领域各方面各环节。第二层是「人民当家作主」：明确我国是人民民主专政的社会主义国家，国家一切权力属于人民，人民民主专政的本质是人民当家作主；我国的根本政治制度是人民代表大会制度，是人民行使国家权力的根本途径和最高实现形式，全国人民代表大会是最高国家权力机关；我国的基本政治制度包括中国共产党领导的多党合作和政治协商制度、民族区域自治制度、基层群众自治制度三项。第三层是「全面依法治国」：明确全面依法治国是国家治理的一场深刻革命；科学立法、严格执法、公正司法、全民守法是全面依法治国的基本要求；建设中国特色社会主义法治体系，建设社会主义法治国家。第四层是三者关系：坚持党的领导、人民当家作主、依法治国有机统一，是我国社会主义政治发展道路的核心内容。三个互动台子都能真操作：动手一是「三者有机统一定位台」，六条真实政治生活情境分别定位到党的领导、人民当家作主、依法治国，定位完给出三者关系的完整表述；动手二是本课核心模拟「制度与职权对应台」，六条情境分别对应人民代表大会制度、中国共产党领导的多党合作和政治协商制度、民族区域自治制度、基层群众自治制度，其中「人民代表大会制度是根本政治制度而非基本政治制度」与「民族区域自治在国家统一领导下」是高频易错点；综合任务是「依法办事流程台」，六条做法分别归入科学立法、严格执法、公正司法、全民守法四个环节，归完合成一张依法办事流程图。全课在政治表述上从严把关：一律使用规范全称；三者有机统一的表述完整准确；根本政治制度与基本政治制度的层级不混写；民族区域自治的表述不含「完全自治」「民族自治」等偏差说法；不臆造文件名称与编号、不编造会议细节、不涉及敏感时政细节与人物评价；表述庄重、严谨、积极正面；插图一律为中性简洁抽象教学示意图，不绘制国旗、国徽、党徽、领导人形象与地图。",
    "plan_table": """| 1 | cover | 政治与法治：党的领导、人民当家作主、依法治国有机统一 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：这三条表述准不准？ | 起·前测（暴露已有印象与混淆点） |
| 5 | concept | 中国共产党领导是中国特色社会主义最本质的特征 | 承·概念一（中国共产党的领导） |
| 6 | interactive | 动手一：三者有机统一定位台——这条情境主要体现哪一条？ | 承·定位台（6 情境 × 3 条） |
| 7 | concept | 人民当家作主：一项根本政治制度与三项基本政治制度 | 承·概念二（我国的政治制度） |
| 8 | interactive | ★动手二：制度与职权对应台——它体现了哪一项制度？ | 承·核心模拟（6 情境 × 4 项制度） |
| 9 | concept | 例题示范：四条表述，逐条校对讲准 | 转·重难点突破（分步校对 + 纠错） |
| 10 | quiz | 概念测试：三句话，藏着三个容易想歪的地方 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：依法办事流程台——这条做法落在哪个环节？ | 合·迁移应用（6 做法 × 4 个基本要求） |
| 12 | quiz | 后测：换几条新情境，看看制度与环节还用不用得上 | 合·后测 |
| 13 | summary | 小结：三句话，把三者有机统一说清楚 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：中国共产党的领导 / 人民当家作主 / 依法治国 三栏，用向上的箭头、圆形会场俯视图形、投票箱、天平、法典书本、盾牌等抽象符号表示，附中文标注\n- P5 三者有机统一抽象示意图（已生成）：党的领导、人民当家作主、依法治国三个圆形节点对称排列，之间用等边连接线相连\n- P7 我国政治制度结构抽象示意图（已生成）：上方标注人民代表大会制度并注明根本政治制度，下方三个方框标注三项基本政治制度，并标注「抽象示意图，不按比例」\n- ★ 全课不绘制国旗、国徽、党徽、领导人形象与地图；涉及国家与制度仅用天平、法典书本、圆形会场俯视图、投票箱、盾牌、抽象人群剪影等中性抽象图形\n- ★ 表述口径统一：规范全称一律写准；党的领导、人民当家作主、依法治国三者有机统一的表述完整；根本政治制度与基本政治制度的层级不混写；民族区域自治不使用「完全自治」「民族自治」等偏差说法\n- 三张图均为中性简洁抽象教学示意图，不使用真人照片风格，不含可识别的真实人物",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
