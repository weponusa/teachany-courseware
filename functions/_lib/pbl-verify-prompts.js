/**
 * @internal PBL dependsOn 方向性验证 — 批量校验 match 输出的依赖边
 */

/**
 * @param {object} payload
 * @param {string} payload.goal
 * @param {Array<{id:string, sourceName:string, sourceRole:string, targetName:string, targetRole:string, officialPrereqs:string[]}>} payload.edges
 */
export function buildVerifyDepsMessages(payload) {
  const { goal = '', edges = [] } = payload;
  const edgeBlock = edges.map((e, i) => {
    const official = (e.officialPrereqs || []).length
      ? e.officialPrereqs.join('、')
      : '（课标树未标注先修）';
    return `${i + 1}. [${e.id}] ${e.sourceName}（${e.sourceRole || 'node'}）→ ${e.targetName}（${e.targetRole || 'node'}）
   课标官方先修（target 节点）：${official}`;
  }).join('\n');

  const system = `依赖边审核：valid=合理前置；invalid=无先修关系；reversed=方向反了。foundation常为bridge/core前置。只返回JSON。`;

  const user = `目标:${goal}

【待验证依赖边】共 ${edges.length} 条
${edgeBlock}

返回 JSON：
{
  "edges": [
    {"id": "e1", "verdict": "valid", "reason": "一句话说明"}
  ]
}

verdict 只能是 valid / invalid / reversed。每条边必须给出判定。`;

  return [
    { role: 'system', content: system },
    { role: 'user', content: user },
  ];
}
