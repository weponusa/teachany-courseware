/**
 * @internal PBL 多轮调整 — 基于已有拆解结果理解用户修改意图
 */

import { stripStructuredGoal } from './pbl-context.js';

function formatSubjectToken(projectSpec) {
  if (!projectSpec) return 'cross';
  if (Array.isArray(projectSpec.subjects) && projectSpec.subjects.length) {
    return projectSpec.subjects.join('+');
  }
  return projectSpec.subject || 'cross';
}

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

  const task = projectSpec?.task || stripStructuredGoal(goal);
  const specLine = projectSpec
    ? `${projectSpec.gradeLevel || 'any'}/${formatSubjectToken(projectSpec)}｜${task}｜产出:${projectSpec.deliverable || ''}`
    : task;

  const matched = (snapshot.matchedNames || []).slice(0, 15).join('、') || '无';
  const deliverable = snapshot.deliverable || '';
  const phases = (snapshot.phaseNames || []).join('→') || '无';

  const system = `PBL拆解调整：理解用户修改意图，输出可执行调整方案。禁重复复述现状。只返回JSON。`;

  const user = `当前:${specLine}
交付:${deliverable}｜阶段:${phases}｜节点:${matched}
修改:${userMessage}

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
