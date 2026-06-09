/**
 * @internal PBL 对齐结果校验 — 提案节点已映射图谱，本阶段只做审核与路径编排
 */

function formatBlueprintSummary(blueprint) {
  if (!blueprint) return '';
  const scheme = (blueprint.schemes || []).find(s => s.id === blueprint.recommendedSchemeId)
    || (blueprint.schemes || [])[0];
  const lines = [];
  if (blueprint.deliverable) lines.push(`交付物：${blueprint.deliverable}`);
  (scheme?.phases || []).slice(0, 6).forEach((p, i) => {
    lines.push(`${i + 1}. ${p.phase || '阶段'}｜${(p.knowledgeHints || []).slice(0, 4).join('、')}`);
  });
  return lines.join('\n');
}

/**
 * @param {object} payload
 * @param {Array<{index:number,id:string,name:string,subject:string,grade:number,role:string,reason:string,linkMethod:string}>} payload.linked
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
    return `${n.index + 1}. [idx=${n.index}] id=${n.id}
   ${n.name}（${n.subject || '未知'} · ${g} · ${n.role || 'core'}）
   提案理由：${n.reason || '—'}
   对齐方式：${n.linkMethod || '图谱匹配'}`;
  }).join('\n');

  const gradeMaps = {
    primary: '小学（剔除超龄/大学节点）',
    junior: '初中（剔除大学节点）',
    senior: '高中（剔除大学节点）',
    university: '大学/高等教育（保留专业/大学层知识，剔除 K12 凑数节点）',
    adult: '成人/在职（保留专业/大学层知识，剔除 K12 凑数节点）',
  };
  const gradeLine = gradeMaps[projectSpec?.gradeLevel] || '';

  const system = `你是 K12 PBL 学习路径校验员。课内知识点已由「模型提案 + 图谱对齐」产生，你的任务是**校验**而非重新选课标。

## 校验职责
1. **remove**：与目标/交付物无解释关系、明显跑题或超龄的已对齐节点（index 必填）。
2. **保留**：能支撑项目某一环节的节点，即使学科不完全齐全也可保留。
3. **编排**：为保留节点指定 pathOrder、dependsOn（source/target 为 idx）、projectPhases、external（1–3 个课标外补充）、techRoute、knowledgeChain。
4. dependsOn 须符合学科逻辑；foundation 一般为 bridge/core 的前置。
5. projectPhases 每阶段 steps ≥2 条、每条 ≥15 字；knowledgeNames 只能使用【已对齐节点】中的名称原文。
6. 不要输出 literacy/素养/态度/情感/价值观 等泛化字段；阶段只保留 phase、steps、knowledgeNames、deliverable。
7. 不要编造新的课内节点名称；未在列表中的名称不得写入 knowledgeNames。

只返回 JSON，不要 markdown。`;

  const user = `【项目目标】${goal}
${gradeLine ? `【学段约束】${gradeLine}\n` : ''}【交付物】${deliverable || projectBlueprint?.deliverable || '（见蓝图）'}
【拆解蓝图】
${formatBlueprintSummary(projectBlueprint)}

【已对齐课内节点】共 ${linked.length} 个（仅可校验/剔除/编排，不可新增课内名）
${nodeBlock}

返回 JSON：
{
  "remove": [{"index": 0, "reason": "与交付物无关"}],
  "roleUpdates": [{"index": 1, "role": "bridge"}],
  "pathOrder": [0, 1, 2],
  "dependsOn": [{"source": 0, "target": 2}],
  "matched": [],
  "projectPhases": [
    {
      "phase": "阶段名",
      "steps": ["具体任务1", "具体任务2"],
      "knowledgeNames": ["节点名须来自上方列表"],
      "deliverable": "阶段产出"
    }
  ],
  "external": [{"name": "课标外补充", "reason": "为何必需"}],
  "techRoute": "中文路径说明，500字内",
  "knowledgeChain": "A → B → C",
  "summary": "校验结论"
}

remove 中 index 为 idx= 后的整数；pathOrder/dependsOn 仅引用保留后的 idx（剔除前先按原 idx 判断，输出时 pathOrder 用保留节点顺序即可）。`;

  return [
    { role: 'system', content: system },
    { role: 'user', content: user },
  ];
}
