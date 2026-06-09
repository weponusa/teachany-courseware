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
2. **remove**：无法建立上述联系；明显跨题；仅为凑学科数量。跨题典型示例：
   - 历史朝代/文言文/古诗词 用于工程制作项目
   - 地形河流用于非地理项目
   - 细胞分裂用于非生物项目
   - 两个语文节点彼此无关且与项目目标无因果联系
3. 不依赖项目类型标签，只看目标文本、交付物与蓝图阶段是否合理支撑该节点。
4. **重点审查**：工程/制作/探究类项目中出现的文言文、古诗词鉴赏等纯文学节点，需要能说明与项目的因果联系（如交付物涉及写作/报告、或项目主题本身关联该文学内容），否则 remove。不要仅因为"也是语文课标"就保留。
5. **科学/工程/探究类项目的两类必保节点**：
   - **科学技术原理节点**（physics/chemistry/biology/science）：如果该节点解释了项目"为什么能成功"的原理（电路原理、力学、化学反应、生物结构等），即使看起来"太基础"也应 keep，不要轻易 remove。
   - **数学技能节点**（math 中的统计/测量/数据分析类）：如果该节点用于项目中的数据收集、统计图表、测量计算，应 keep。
   - 审核完毕后，在 summary 中报告：当前保留节点是否同时涵盖了"科学原理类"和"数学技能类"。如果缺少任一类，在 summary 中明确指出"警告：缺少 XX 类节点"。

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
