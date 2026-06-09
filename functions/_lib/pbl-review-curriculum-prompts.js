/**
 * @internal PBL 课标节点二次检讨 — 输出前全图谱课内节点审核
 */

function formatBlueprintSummary(blueprint) {
  if (!blueprint) return '（无拆解蓝图）';
  const scheme = (blueprint.schemes || []).find(s => s.id === blueprint.recommendedSchemeId)
    || (blueprint.schemes || [])[0];
  const lines = [];
  if (blueprint.deliverable) lines.push(`交付物：${blueprint.deliverable}`);
  if (blueprint.knowledgeChain) lines.push(`知识链：${blueprint.knowledgeChain}`);
  (scheme?.phases || []).slice(0, 8).forEach((p, i) => {
    const hints = (p.knowledgeHints || []).slice(0, 6).join('、');
    lines.push(`${i + 1}. ${p.phase || p.name || '阶段'}${hints ? `｜课标线索：${hints}` : ''}`);
  });
  return lines.join('\n') || '（蓝图无阶段明细）';
}

/**
 * @param {object} payload
 * @param {string} payload.goal
 * @param {object} [payload.projectBlueprint]
 * @param {string} [payload.deliverable]
 * @param {Array<{index:number,id:string,name:string,subject:string,grade:number,layer:string,reason:string,definition:string}>} payload.nodes
 */
function formatGradeConstraint(projectSpec) {
  if (!projectSpec || !projectSpec.gradeLevel || projectSpec.gradeLevel === 'any') return '';
  const maps = {
    primary: '小学（1–6 年级）',
    junior: '初中（7–9 年级）',
    senior: '高中（10–12 年级）',
    university: '大学',
    adult: '成人/在职',
  };
  const base = maps[projectSpec.gradeLevel] || projectSpec.gradeLevel;
  const detail = parseInt(projectSpec.gradeDetail, 10);
  if (detail >= 1 && detail <= 12) return `${detail} 年级`;
  return base;
}

export function buildReviewCurriculumMessages(payload) {
  const {
    goal = '',
    projectBlueprint = null,
    deliverable = '',
    projectSpec = null,
    nodes = [],
  } = payload;

  const blueprintBlock = formatBlueprintSummary(projectBlueprint);
  const nodeBlock = nodes.map((n) => {
    const gradeLabel = n.grade > 0 ? `G${n.grade}` : '拓展';
    const def = String(n.definition || '').replace(/\s+/g, ' ').slice(0, 80);
    return `${n.index + 1}. [idx=${n.index}] id=${n.id}
   ${n.name}（${n.subject || '未知'} · ${gradeLabel} · ${n.layer || 'matched'}）
   入选理由：${n.reason || '（无）'}
   ${def ? `定义片段：${def}` : ''}`;
  }).join('\n');

  const adultOrUni = projectSpec?.gradeLevel === 'adult' || projectSpec?.gradeLevel === 'university' || /成人|在职|大学|工程实施方案/.test(String(goal || ''));
  const system = `${adultOrUni ? '你是成人/大学 PBL 专业知识图谱审核员。' : '你是 K12 PBL 课标图谱审核员。'}根据「项目目标 + 拆解蓝图 + 交付物」审查知识点是否应保留。

## 判定原则（泛化，不按项目类型套模板）
1. **keep**：节点能解释「为何本项目需要学它」——能支撑调研、测算、实验理解、数据表达、论证写作等具体环节之一；与蓝图阶段或课标线索有合理联系。
2. **remove**：与目标/交付物无解释关系；仅为凑学科或图谱前置链误牵入；明显跑题（如非历史项目的朝代战争、非生物项目的细胞分裂、非地图项目的地形判读等）。
3. **审慎**：宁可剔除牵强节点，也不要为了凑满数量保留无关节点。气候变化/排放类地理在能源对比项目中可保留；自然地貌、河流区位等与目标无关的地理应剔除。
4. **学段**：若用户选定小学，必须剔除大学层节点（grade=0/拓展）及明显超龄的初中高中课标；若用户为成人/在职/大学，应优先保留专业工程与计算机节点，剔除二次函数、三角函数、语文句式等 K12 凑数节点。

只返回 JSON，不要 markdown。`;

  const gradeLine = formatGradeConstraint(projectSpec);
  const user = `【项目目标】${goal}
${gradeLine ? `【学段约束】${gradeLine}${adultOrUni ? '（应保留专业/大学层知识，剔除 K12 凑数节点）' : '（超龄/大学节点应剔除）'}\n` : ''}
【交付物】${deliverable || projectBlueprint?.deliverable || '（见蓝图）'}
【拆解蓝图】
${blueprintBlock}

【待检讨课内节点】共 ${nodes.length} 个
${nodeBlock}

返回 JSON：
{
  "remove": [
    {"index": 0, "reason": "与项目交付物无解释关系的自然地理节点"}
  ],
  "summary": "一句话检讨结论",
  "qualityNote": "对召回策略的改进建议（可选）"
}

remove 中 index 必须为各行 idx= 后的整数；只列应剔除节点，未列出视为保留。`;

  return [
    { role: 'system', content: system },
    { role: 'user', content: user },
  ];
}
