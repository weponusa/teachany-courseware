/**
 * @internal PBL 课标节点二次检讨 — 输出前全图谱课内节点审核
 */

import { buildCompactUserContext, compactBlueprintPhases } from './pbl-context.js';

/**
 * @param {object} payload
 */
export function buildReviewCurriculumMessages(payload) {
  const {
    goal = '',
    projectBlueprint = null,
    deliverable = '',
    projectSpec = null,
    nodes = [],
  } = payload;

  const nodeBlock = nodes.map((n) => {
    const gradeLabel = n.grade > 0 ? `G${n.grade}` : '拓展';
    const def = String(n.definition || '').replace(/\s+/g, ' ').slice(0, 60);
    return `${n.index + 1}.[${n.index}] ${n.name}(${n.subject || '?'}/${gradeLabel}) ${n.reason || ''}${def ? ` ${def}` : ''}`;
  }).join('\n');

  const adultOrUni = projectSpec?.gradeLevel === 'adult' || projectSpec?.gradeLevel === 'university' || /成人|在职|大学|工程实施方案/.test(String(goal || ''));
  const ctx = buildCompactUserContext({ goal, projectSpec, projectBlueprint, deliverable, includeBlueprint: false });
  const phases = compactBlueprintPhases(projectBlueprint, 6);

  const system = `${adultOrUni ? '大学' : 'K12'}课标审核：keep=支撑具体环节；remove=跑题/凑学科/误牵前置链。宁可少留牵强节点。只返回JSON。`;

  const user = `${ctx}
${phases ? `阶段:${phases}\n` : ''}
待审${nodes.length}个：
${nodeBlock}

返回：{"remove":[{"index":0,"reason":""}],"summary":"","qualityNote":""}`;

  return [
    { role: 'system', content: system },
    { role: 'user', content: user },
  ];
}
