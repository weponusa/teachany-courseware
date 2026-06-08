/**
 * @internal PBL 多轮调整 — 基于已有拆解结果理解用户修改意图
 */

/**
 * @param {object} payload
 */
export function buildRefineMessages(payload) {
  const {
    goal = '',
    userMessage = '',
    projectSpec = null,
    snapshot = {},
  } = payload;

  const specBlock = projectSpec
    ? `学段：${projectSpec.gradeLevel || 'any'}
学科：${projectSpec.subject || 'cross'}
任务：${projectSpec.task || ''}
产出：${projectSpec.deliverable || ''}`
    : '（未提供结构化字段）';

  const matched = (snapshot.matchedNames || []).slice(0, 20).join('、') || '（无）';
  const deliverable = snapshot.deliverable || '（见蓝图）';
  const phases = (snapshot.phaseNames || []).join(' → ') || '（无）';

  const system = `你是 PBL 项目拆解调整助手。用户已有一次拆解结果，现提出修改要求。请理解意图并给出可执行的调整方案。

## 原则
- 尊重用户结构化字段（学段/学科/任务/产出）
- 修改要求应落地到：任务表述、产出类型、蓝图阶段、课标匹配倾向
- 若用户要求减少某类噪声（如历史节点），在 addKeywords/removeKeywords 中体现
- 若改动较大，设 fullRematch=true

只返回 JSON，不要 markdown。`;

  const user = `【当前项目目标】
${goal}

【结构化描述】
${specBlock}

【当前交付物】${deliverable}
【当前阶段链】${phases}
【当前 matched 节点】${matched}

【用户本轮修改要求】
${userMessage}

返回 JSON：
{
  "summary": "一句话说明将如何调整",
  "revisedTask": "更新后的任务描述（无变化则留空字符串）",
  "revisedDeliverable": "更新后的产出描述（无变化则留空）",
  "removeKeywords": ["历史", "朝代"],
  "addKeywords": ["统计", "函数"],
  "fullRematch": true,
  "userFacingReply": "给用户看的简短回复，说明已理解的需求"
}

fullRematch：true 表示需要重新走课标匹配；false 表示仅文案/蓝图微调。`;

  return [
    { role: 'system', content: system },
    { role: 'user', content: user },
  ];
}
