/**
 * @internal PBL matched 节点相关性二审 — 剔除 match/召回幻觉
 */

function formatBlueprintSummary(blueprint) {
  if (!blueprint) return '';
  const scheme = (blueprint.schemes || []).find(s => s.id === blueprint.recommendedSchemeId)
    || (blueprint.schemes || [])[0];
  return (scheme?.phases || []).slice(0, 6).map((p, i) => {
    const hints = (p.knowledgeHints || []).slice(0, 5).join('、');
    return `  ${i + 1}. ${p.phase || '阶段'}${hints ? ` → ${hints}` : ''}`;
  }).join('\n');
}

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

  const blueprintBlock = formatBlueprintSummary(projectBlueprint);
  const nodeBlock = matched.map((n) => {
    const gradeLabel = n.grade > 0 ? `G${n.grade}` : '拓展';
    return `${n.index + 1}. [idx=${n.index}] ${n.name}（${n.subject || '未知'} · ${gradeLabel}）
   role=${n.role || 'core'} | 召回理由：${n.reason || '（无）'}`;
  }).join('\n');

  const system = `你是 K12 PBL 课标匹配审核员。审查已召回知识点是否真正服务于项目目标与交付物。

## 泛化判定标准
1. **keep**：能回答「学这个知识点如何帮助完成本项目某一环节」；与目标、蓝图阶段或课标线索有具体联系。
2. **remove**：无法建立上述联系；明显跨题（历史朝代用于购车、地形河流用于非地理项目、细胞分裂用于非生物项目等）；仅为凑学科数量。
3. 不依赖项目类型标签，只看目标文本、交付物与蓝图阶段是否合理支撑该节点。

只返回 JSON，不要 markdown。`;

  const user = `【项目目标】${goal}
【交付物】${deliverable || projectBlueprint?.deliverable || '（见蓝图）'}
${blueprintBlock ? `【蓝图阶段与课标线索】\n${blueprintBlock}\n` : ''}
【待审核节点】共 ${matched.length} 个
${nodeBlock}

返回 JSON：
{
  "remove": [
    {"index": 0, "reason": "与项目目标无解释关系的节点"}
  ],
  "summary": "一句话审核结论"
}

remove 中 index 必须为候选数组下标 idx=；只列应剔除项。`;

  return [
    { role: 'system', content: system },
    { role: 'user', content: user },
  ];
}
