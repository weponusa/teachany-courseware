/**
 * @internal PBL 知识点提案 — 模型先列应学课标，再由客户端对齐图谱
 */

import { formatGradeConstraint } from './pbl-grade-constraint.js';
import { buildCompactUserContext, compactBlueprintPhases } from './pbl-context.js';

function isAdultOrUniversity(projectSpec, goal) {
  if (projectSpec?.gradeLevel === 'adult' || projectSpec?.gradeLevel === 'university') return true;
  return /成人|在职|大学|本科|研究生|工程实施方案|企业|产业级/.test(String(goal || ''));
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
  } = payload;

  const adultOrUni = isAdultOrUniversity(projectSpec, goal);
  const gradeLine = formatGradeConstraint(projectSpec);
  const phases = compactBlueprintPhases(projectBlueprint, 6);
  const ctx = buildCompactUserContext({
    goal,
    projectSpec,
    projectBlueprint,
    deliverable,
    includeBlueprint: false,
  });

  const system = `${adultOrUni ? '大学PBL知识点提案' : 'K12 PBL课标提案'}：列应学知识点（非图谱id）。

原则：①支撑具体环节 ②按前置→方法→核心排序(role) ③${adultOrUni ? '专业表述' : '课标常见表述'} ④${gradeLine || (adultOrUni ? '成人/大学' : 'K12')} ⑤${Math.max(5, maxProposed - 4)}–${maxProposed}个宁精勿滥 ⑥禁泛素养 ⑦须与目标有因果联系 ⑧理工/探究类：原理≥2+数学≥1。只返回JSON。`;

  const user = `${ctx}
${phases ? `阶段:${phases}\n` : ''}
返回 JSON：{"proposed":[{"name":"","subject":"","gradeHint":0,"phase":"","role":"core","reason":""}],"knowledgeChain":"","summary":""}
subject:${adultOrUni ? 'computer-science/engineering/physics/info-tech/math' : 'math/physics/chemistry/biology/science/chinese/english/history/geography/info-tech'}`;

  return [
    { role: 'system', content: system },
    { role: 'user', content: user },
  ];
}
