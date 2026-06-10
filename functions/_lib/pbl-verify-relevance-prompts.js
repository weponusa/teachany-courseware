/**
 * @internal PBL matched 节点相关性二审 — 剔除 match/召回幻觉
 */

import { buildCompactUserContext, compactBlueprintPhases } from './pbl-context.js';

/**
 * @param {object} payload
 */
export function buildVerifyRelevanceMessages(payload) {
  const {
    goal = '',
    deliverable = '',
    projectBlueprint = null,
    matched = [],
  } = payload;

  const phases = compactBlueprintPhases(projectBlueprint, 6);
  const nodeBlock = matched.map((n) => {
    const gradeLabel = n.grade > 0 ? `G${n.grade}` : '拓展';
    return `${n.index + 1}.[${n.index}] ${n.name}(${n.subject || '?'}/${gradeLabel}) ${n.reason || ''}`;
  }).join('\n');

  const ctx = buildCompactUserContext({ goal, projectBlueprint, deliverable, includeBlueprint: false });

  const system = `课标相关性审核：keep=能支撑项目环节；remove=无因果/跑题/凑学科。理工类保留原理+数学技能节点。只返回JSON。`;

  const user = `${ctx}
${phases ? `阶段:${phases}\n` : ''}待审${matched.length}个：
${nodeBlock}

返回：{"remove":[{"index":0,"reason":""}],"summary":""}`;

  return [
    { role: 'system', content: system },
    { role: 'user', content: user },
  ];
}
