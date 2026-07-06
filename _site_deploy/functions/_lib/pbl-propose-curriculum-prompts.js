/**
 * @internal PBL 知识点提案 — 优先从候选池按 index 选配（对齐图谱节点名）
 */

import { formatGradeConstraint } from './pbl-grade-constraint.js';
import { buildCompactUserContext, compactBlueprintPhases } from './pbl-context.js';

const SUBJECT_ZH = {
  math: '数学', physics: '物理', chemistry: '化学', biology: '生物',
  science: '科学', 'info-tech': '信息技术', chinese: '语文', english: '英语',
  history: '历史', geography: '地理', politics: '道法', psychology: '心理',
  engineering: '工程', 'computer-science': '计算机科学',
};

function isAdultOrUniversity(projectSpec, goal) {
  if (projectSpec?.gradeLevel === 'adult' || projectSpec?.gradeLevel === 'university') return true;
  return /成人|在职|大学|本科|研究生|工程实施方案|企业|产业级/.test(String(goal || ''));
}

function formatCandidateList(candidates) {
  return (candidates || []).map((n, i) => {
    const gradeStr = n.gradeLabel || (n.grade ? `G${n.grade}` : '通识');
    const subj = SUBJECT_ZH[n.subject] || n.subject || '';
    const def = String(n.definition || '').replace(/\s+/g, ' ').slice(0, 72);
    const defPart = def ? ` | ${def}` : '';
    return `[${i}] ${n.name} | ${gradeStr} | ${subj}${defPart}`;
  }).join('\n');
}

/**
 * @param {object} payload
 */
export function buildProposeCurriculumMessages(payload) {
  const {
    goal = '',
    projectBlueprint = null,
    projectSpec = null,
    deliverable = '',
    maxProposed = 12,
    candidates = [],
  } = payload;

  const adultOrUni = isAdultOrUniversity(projectSpec, goal);
  const gradeLine = formatGradeConstraint(projectSpec);
  const phases = compactBlueprintPhases(projectBlueprint, 8);
  const ctx = buildCompactUserContext({
    goal,
    projectSpec,
    projectBlueprint,
    deliverable,
    includeBlueprint: true,
  });
  const minPick = Math.max(5, maxProposed - 4);
  const maxPick = maxProposed;

  if (Array.isArray(candidates) && candidates.length > 0) {
    const candidateList = formatCandidateList(candidates);
    const system = `${adultOrUni ? '大学PBL课标选配' : 'K12 PBL课标选配'}：从下方候选列表选知识点，**只能用 index 引用，禁止编造名称或写候选列表外的节点**。

原则：
① 每个节点须支撑蓝图某一具体阶段/步骤（phase 字段写阶段名）
② 按 foundation→bridge→core 排序（先修/方法→桥梁→核心）
③ 选 ${minPick}–${maxPick} 个，宁精勿滥
④ ${gradeLine || (adultOrUni ? '成人/大学' : 'K12 学段')}
⑤ 禁泛素养、禁与交付物无因果联系的凑数
⑥ 理工/探究类：原理+实验方法+数据处理至少各 1 个（若候选中有）
⑦ reason 以「模块：」开头，写明该知识点在本项目中的具体用法

只返回 JSON，不要 markdown。`;

    const user = `${ctx}
${phases ? `蓝图阶段（选配须覆盖）：\n${phases}\n` : ''}
候选课标节点（只能选下列 index）：
${candidateList}

返回 JSON：
{"proposed":[{"index":0,"phase":"对应阶段名","role":"foundation|bridge|core","reason":"模块：…在本项目中用于…"}],"knowledgeChain":"节点递进链（用→连接候选中的名称）","summary":"选配说明"}`;

    return [
      { role: 'system', content: system },
      { role: 'user', content: user },
    ];
  }

  const system = `${adultOrUni ? '大学PBL知识点提案' : 'K12 PBL课标提案'}：列应学知识点（须用课标常见表述，便于对齐图谱）。

原则：①支撑具体环节 ②按前置→方法→核心排序(role) ③${adultOrUni ? '专业表述' : '课标常见表述'} ④${gradeLine || (adultOrUni ? '成人/大学' : 'K12')} ⑤${minPick}–${maxPick}个宁精勿滥 ⑥禁泛素养 ⑦须与目标有因果联系 ⑧理工/探究类：原理≥2+数学/数据处理≥1。只返回JSON。`;

  const user = `${ctx}
${phases ? `阶段:${phases}\n` : ''}
返回 JSON：{"proposed":[{"name":"","subject":"","gradeHint":0,"phase":"","role":"core","reason":""}],"knowledgeChain":"","summary":""}
subject:${adultOrUni ? 'computer-science/engineering/physics/info-tech/math' : 'math/physics/chemistry/biology/science/chinese/english/history/geography/info-tech/politics/psychology'}`;

  return [
    { role: 'system', content: system },
    { role: 'user', content: user },
  ];
}
