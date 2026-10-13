/**
 * @internal PBL 对齐结果校验 — 提案节点已映射图谱，本阶段只做审核与路径编排
 */

import { buildCompactUserContext, compactBlueprintPhases } from './pbl-context.js';

/**
 * @param {object} payload
 */
export function buildValidateMatchMessages(payload) {
  const {
    goal = '',
    projectBlueprint = null,
    deliverable = '',
    projectSpec = null,
    linked = [],
  } = payload;

  const nodeBlock = linked.map((n) => {
    const g = n.grade > 0 ? `G${n.grade}` : '拓展';
    return `${n.index + 1}.[${n.index}] ${n.name}(${n.subject || '?'}/${g}/${n.role || 'core'}) ${n.reason || ''}`;
  }).join('\n');

  const ctx = buildCompactUserContext({ goal, projectSpec, projectBlueprint, deliverable, includeBlueprint: false });
  const phases = compactBlueprintPhases(projectBlueprint, 6);

  const system = `路径校验：剔除跑题/超龄；编排pathOrder/dependsOn/projectPhases/external/techRoute。knowledgeNames仅用已对齐节点名；steps≥2条≥15字。只返回JSON。`;

  const user = `${ctx}
${phases ? `阶段:${phases}\n` : ''}
已对齐${linked.length}个：
${nodeBlock}

返回：{"remove":[],"roleUpdates":[],"pathOrder":[],"dependsOn":[],"matched":[],"projectPhases":[],"external":[],"techRoute":"","knowledgeChain":"","summary":""}`;

  return [
    { role: 'system', content: system },
    { role: 'user', content: user },
  ];
}
