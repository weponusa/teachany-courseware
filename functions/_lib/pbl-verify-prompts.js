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

  const system = `你是 K12 课标知识依赖关系审核员。任务：判断 PBL 项目学习路径中，「先修知识点→后续知识点」的依赖方向是否合理。

## 判断标准
1. **valid**：学完 source 是学好 target 的合理前置（符合学科逻辑与 PBL 实施顺序）
2. **invalid**：两者无先修关系，或删掉 source 不影响 target 的学习
3. **reversed**：方向反了，应是 target→source（或官方先修与声称方向矛盾）

## 角色提示
- foundation 通常是 bridge/core 的前置
- 同阶段 parallel 节点一般不应互为先修
- 官方先修列表若包含 source 名称，倾向 valid；若包含 target 而声称 source→target，倾向 reversed

只返回 JSON，不要 markdown。`;

  const user = `【项目目标】${goal}

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
