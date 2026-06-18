/**
 * @internal PBL 跨阶段紧凑上下文 — 缩写、去重
 */

import { formatGradeConstraint } from './pbl-grade-constraint.js';

const SUBJECT_ID_ZH = {
  math: '数学', physics: '物理', chemistry: '化学', biology: '生物', science: '科学',
  chinese: '语文', english: '英语', history: '历史', geography: '地理',
  'info-tech': '信息技术', art: '艺术', politics: '道法', psychology: '心理',
};

function formatSubjectConstraint(projectSpec) {
  if (!projectSpec) return '';
  if (Array.isArray(projectSpec.subjects) && projectSpec.subjects.length) {
    const ids = projectSpec.subjects.filter(id => id && id !== 'cross');
    if (ids.length) return ids.map(id => SUBJECT_ID_ZH[id] || id).join('+');
  }
  if (projectSpec.subject && projectSpec.subject !== 'cross') {
    return SUBJECT_ID_ZH[projectSpec.subject] || projectSpec.subject;
  }
  return '';
}

const SUBJECT_LABELS = new Set([
  '跨学科', '数学', '物理', '化学', '生物', '科学', '语文', '英语', '历史', '地理', '信息技术', '艺术', '道法', '心理',
]);

/** 从结构化 goal 提取任务正文（兼容【任务】与｜分隔单行格式） */
export function stripStructuredGoal(goal) {
  const g = String(goal || '').trim();
  const tagged = g.match(/【任务】\s*([^\n]+)/);
  if (tagged) return tagged[1].trim();
  if (g.includes('｜')) {
    const parts = g.split('｜').map(s => s.trim()).filter(Boolean);
    const taskParts = parts.filter(p => !/^(产出|场景|周期|约束):/.test(p));
    while (taskParts.length && (
      /^(小学|初中|高中|大学|成人)/.test(taskParts[0])
      || SUBJECT_LABELS.has(taskParts[0])
      || /年级/.test(taskParts[0])
    )) {
      taskParts.shift();
    }
    if (taskParts.length) return taskParts.join('｜');
  }
  return g.replace(/【[^】]+】[^\n]*/g, '').trim() || g;
}

export function extractDeliverableFromGoal(goal) {
  const m = String(goal || '').match(/(?:【产出】|产出:)\s*([^\n｜]+)/);
  return m ? m[1].trim() : '';
}

/** 紧凑蓝图：阶段名 + 检索词 */
export function compactBlueprintPhases(blueprint, maxPhases = 5) {
  if (!blueprint) return '';
  const scheme = (blueprint.schemes || []).find(s => s.id === blueprint.recommendedSchemeId)
    || (blueprint.schemes || [])[0];
  if (!scheme?.phases?.length) return '';
  return scheme.phases.slice(0, maxPhases).map((p, i) => {
    const hints = (p.knowledgeHints || []).slice(0, 4).join('、');
    return `${i + 1}.${p.phase || '阶段'}${hints ? `(${hints})` : ''}`;
  }).join(' ');
}

export function compactBlueprintHeader(blueprint) {
  if (!blueprint) return '';
  const parts = [];
  if (blueprint.projectSummary) parts.push(blueprint.projectSummary);
  if (blueprint.deliverable) parts.push(`交付:${blueprint.deliverable}`);
  const phases = compactBlueprintPhases(blueprint);
  if (phases) parts.push(phases);
  return parts.join('｜');
}

/** 各 LLM 阶段统一的紧凑 user 上下文 */
export function buildCompactUserContext({
  goal = '',
  projectSpec = null,
  projectBlueprint = null,
  deliverable = '',
  includeBlueprint = true,
} = {}) {
  const task = stripStructuredGoal(goal);
  const deliv = deliverable
    || projectBlueprint?.deliverable
    || extractDeliverableFromGoal(goal)
    || '';
  const grade = formatGradeConstraint(projectSpec);
  const subject = formatSubjectConstraint(projectSpec);
  const lines = [`目标:${task}`];
  if (deliv) lines.push(`交付:${deliv}`);
  if (grade) lines.push(`学段:${grade}`);
  if (subject) lines.push(`学科:${subject}`);
  if (includeBlueprint && projectBlueprint) {
    const bp = compactBlueprintHeader(projectBlueprint);
    if (bp) lines.push(`蓝图:${bp}`);
  }
  return lines.join('\n');
}
