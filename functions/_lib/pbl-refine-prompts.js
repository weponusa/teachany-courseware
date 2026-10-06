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

  const system = `PBL拆解调整助手。理解用户修改意图，输出可执行调整方案。
原则：
- 用户仅增减/替换知识点、微调产出或阶段时，优先局部调整，不要全量重拆
- removeKeywords/addKeywords 用于模糊匹配节点名；knowledgeRemove/knowledgeAdd 用于明确知识点名
- fullRematch=true 仅当项目方向、学段学科、任务本质需整体重做
只返回 JSON，不要 markdown。`;

  const user = `当前:${specLine}
交付:${deliverable}｜阶段:${phases}｜节点:${matched}
修改:${userMessage}

返回 JSON：
{
  "summary": "一句话说明将如何调整",
  "revisedTask": "更新后的任务描述（无变化则留空字符串）",
  "revisedDeliverable": "更新后的产出描述（无变化则留空）",
  "removeKeywords": ["历史"],
  "addKeywords": ["统计", "函数"],
  "knowledgeRemove": ["中国古代史"],
  "knowledgeAdd": ["一次函数", "数据分析"],
  "fullRematch": false,
  "userFacingReply": "给用户看的简短回复，说明已理解的需求"
}

fullRematch：true=六阶段全量重拆；false=在现有图谱上增减知识点并同步路径/蓝图。
仅改知识点时务必 fullRematch=false 并填 add/remove 字段。`;

  return [
    { role: 'system', content: system },
    { role: 'user', content: user },
  ];
}
