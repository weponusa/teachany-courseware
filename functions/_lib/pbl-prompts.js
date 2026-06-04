/**
 * @internal PBL 拆解核心提示词 — 仅服务端，勿复制到前端静态资源
 */

const PBL_MAX_MATCHED_COMPLEX = 10;

function systemPromptMatch(complex) {
  const base = `你是资深 PBL（项目式学习）导师兼工程师。任务：把一个项目目标，转化成"一个真正能动手做出来的项目实施路线"，而不是罗列课标知识点。

判断每个知识点是否入选，只问一个问题：
「不学它，这个项目的某个具体环节就做不出来吗？」——是，才选；只是"打基础/有帮助"，一律不选。`;

  if (!complex) {
    return `${base}

要求：
- matched 选 8-14 个与项目动手环节直接相关的知识点。
- techRoute 按"准备→探究→实现→验证"写，每段点明用到哪个知识点、产出什么。
- 只返回 JSON，不要 markdown 包裹，不要解释。`;
  }

  return `${base}

【这是一个复杂/工程类项目】请像带学生做毕业设计一样思考，给出"工程师视角"的路线，而不是"小学补课清单"。

绝对禁止（出现即视为错误回答）：
- 严禁出现小学学段（1-6 年级）内容：分数/小数/百分数互化、四则运算、认识图形、周长面积、简单统计、认识钟表人民币、简单电路、磁铁、植物动物常识等。
- 严禁写"首先掌握数学基础概念""为后续计算提供基础"这类空话套话。
- techRoute 里出现的每一个知识点名称，必须是 matched 里真实选中的那些；不准临时编造或塞入基础概念。

正面示范（以"设计并发射一枚模型火箭"为例，体会颗粒度）：
- 该选：牛顿运动定律、动量与冲量、受力分析、二次函数/抛物运动、燃烧与氧化反应、空气阻力与流体、传感器与数据采集、基础电路与控制。
- 不该选：分数小数百分数互化、圆的周长和面积、认识图形——这些是小学内容，工程项目默认已具备，不进路线。

要求：
1. matched：6-${PBL_MAX_MATCHED_COMPLEX} 个，全部 7-12 年级、直接服务于建模/实验/搭建/编程/测试环节。
2. pathOrder：按"先理解原理→再建模计算→后搭建测试"的真实施工顺序排列 matched 的 index。
3. projectPhases：3-4 个真实工程阶段（如：原理与受力分析 / 结构与弹道建模 / 动力与控制系统 / 制作与发射测试）。每阶段写：steps（具体动手任务）、knowledgeNames（只能用 matched 里的名称）、deliverable（该阶段交付物，如计算表/CAD图/原型/测试报告）。
4. external：最多 2 个候选列表里没有、但工程实现确实要用的专业概念（如"齐奥尔科夫斯基火箭方程""PID控制"），禁止写"XX基础"。
5. techRoute：把 projectPhases 串成一段可执行说明，具体到知识点与产出物，禁止任何小学基础内容与套话。

只返回 JSON，不要 markdown 包裹，不要任何解释文字。`;
}

function userPromptFilter(goal, summaryList, complex) {
  const gradeHint = complex
    ? `\n- 本项目为复杂/综合 PBL，grades 必须落在 7-12（初中、高中），不要包含 1-6 年级小学段。`
    : '';
  return `PBL项目目标：${goal}

可用的知识体系：
${summaryList}

返回 JSON：
{
  "subjects": ["math", "physics"],
  "systems": ["cn", "ap"],
  "grades": [8, 9, 10],
  "reasoning": "从项目交付物角度说明学科与学段判断"
}

注意：
- subjects：math/physics/chemistry/biology/chinese/english/history/geography/info-tech
- systems：cn/ap/cambridge/ib/us
- grades：与项目难度匹配的年级数组（如温控系统多用 8-11，不要泛填全学段）
- 最多 3 个学科、3 个课标体系${gradeHint}`;
}

function userPromptMatch(goal, candidateList, complex, maxMatched, minConf) {
  return `【项目目标】
${goal}

【候选知识点】（只能从中选择 matched，index 为序号）
${candidateList}

返回 JSON 示例结构：
{
  "matched": [
    {"index": 2, "confidence": 0.92, "role": "core", "reason": "用于建立温控数学模型"},
    {"index": 7, "confidence": 0.85, "role": "support", "reason": "用于传感器数据处理"}
  ],
  "pathOrder": [2, 7, 4],
  "projectPhases": [
    {
      "phase": "需求与方案",
      "steps": ["明确控制指标", "选型传感器与执行器"],
      "knowledgeNames": ["一次函数", "传感器原理"],
      "deliverable": "需求说明与方案草图"
    }
  ],
  "external": [
    {"name": "PID控制", "reason": "闭环调温核心算法", "prerequisites": []}
  ],
  "techRoute": "分阶段、写清任务与知识点、写清每阶段产出物的实施路线，500字内"
}

硬性要求：
- matched：${complex ? `6-${maxMatched} 个` : '8-14 个'}，confidence≥${minConf}，且必须能对应到项目实施环节
- ${complex ? '禁止选小学数学/小学科学/小学物理启蒙类 index；不要选「认识图形、统计表、简单电路、四则运算」等' : ''}
- pathOrder：按项目实施先后顺序排列 matched 的 index，长度与 matched 一致或更短
- projectPhases：3-4 个阶段，每阶段写 steps、knowledgeNames（用候选中的名称）、deliverable
- external：最多 ${complex ? 2 : 3} 个，且必须是候选列表中没有、项目又确实需要的专业概念
- techRoute：与 projectPhases 一致，用中文，具体到知识点名称，禁止「首先学习基础知识」等空话`;
}

const SUBJECT_ZH = {
  math: '数学', physics: '物理', chemistry: '化学', biology: '生物',
  science: '科学', 'info-tech': '信息技术', chinese: '语文', english: '英语',
  history: '历史', geography: '地理',
};

/**
 * @param {'filter'|'match'} stage
 * @param {object} payload
 * @returns {{ role: string, content: string }[]}
 */
export function buildPBMessages(stage, payload) {
  const {
    goal = '',
    summaryList = '',
    candidates = [],
    complex = false,
    maxMatched = PBL_MAX_MATCHED_COMPLEX,
    minConf = 0.68,
  } = payload;

  if (stage === 'filter') {
    return [
      {
        role: 'system',
        content: '你是 PBL 项目与课标对齐专家。根据项目目标判断学科、课标体系与适用年级，为后续「可执行项目路径」筛选候选。只返回 JSON。',
      },
      { role: 'user', content: userPromptFilter(goal, summaryList, complex) },
    ];
  }

  if (stage === 'match') {
    const candidateList = (candidates || []).map((n, i) => {
      const gradeStr = n.gradeLabel || (n.grade ? `G${n.grade}` : '通识');
      const subj = SUBJECT_ZH[n.subject] || n.subject || '';
      return `[${i}] ${n.name} | ${gradeStr} | ${subj} | ${n.systemTag || ''}`;
    }).join('\n');

    return [
      { role: 'system', content: systemPromptMatch(complex) },
      {
        role: 'user',
        content: userPromptMatch(goal, candidateList, complex, maxMatched, minConf),
      },
    ];
  }

  throw new Error(`Unknown PBL stage: ${stage}`);
}
