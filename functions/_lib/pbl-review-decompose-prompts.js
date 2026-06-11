/**
 * @internal PBL 拆解蓝图评审修订 — decompose 初稿 → 质检 → 输出完整 JSON
 */

import { buildCompactUserContext } from './pbl-context.js';
import { inferProjectDomains, projectTypeProfile } from './pbl-prompts.js';
import { formatTopicAnchorHint } from './pbl-topic-anchors.js';

function formatTopicAnchorBlock(goal) {
  const anchorHint = formatTopicAnchorHint(goal);
  return anchorHint ? `｜${anchorHint}` : '';
}

/**
 * @param {object} payload
 * @param {string} payload.goal
 * @param {object} payload.projectBlueprint — 初稿（推荐方案）
 * @param {string[]} [payload.reviewIssues]
 * @param {boolean} [payload.complex]
 */
export function buildReviewDecomposeMessages(payload) {
  const {
    goal = '',
    projectBlueprint = null,
    reviewIssues = [],
    complex = false,
  } = payload;

  const p = projectTypeProfile(goal);
  const domains = inferProjectDomains(goal);
  const domainLine = domains.length
    ? `模块参考：${domains.map(d => d.label).join(' → ')}`
    : '';
  const ctx = buildCompactUserContext({ goal, projectBlueprint, includeBlueprint: false });
  const draftJson = JSON.stringify(projectBlueprint || {}, null, 0).slice(0, 12000);
  const issuesBlock = (reviewIssues || []).length
    ? reviewIssues.map((x, i) => `${i + 1}. ${x}`).join('\n')
    : '（自动质检未列出明细，请按深度标准全面修订）';

  const system = `PBL 拆解蓝图评审官。任务：审阅初稿 JSON，修订后输出**完整**拆解蓝图（与 decompose 阶段同 schema）。
类型：${p.label}｜${p.redlines}
${formatTopicAnchorBlock(goal)}

修订硬性要求：
- 保留 schemes≥2、phases 4-5、recommendedSchemeId；可改内容不可删空结构
- projectSummary 40-80 字：谁+方法+交付物+解决的问题；禁「按模块推进」套话
- scopeLimits≥2、successCriteria≥2、constraints≥2：可检查、可验收
- 每 phase：steps≥2 条、互不重复；每条≥20 字，含动词+对象+工具/数据+可验收产出（数量/次数/尺寸之一）
- deliverable 为具体表/图/报告名，禁「阶段成果」「提升素养」
- 步骤须含题目关键词；调查/测算类禁接线/原型/硬件套话；工程类禁空泛「环境搭建」
- knowledgeHints 为检索词（2-5/阶段），非课标节点名
- 只输出修订后 JSON，不要 markdown、不要解释`;

  const user = `${ctx}
${domainLine}

【质检问题清单】
${issuesBlock}

【初稿 JSON】
${draftJson}

返回与 decompose 相同字段的**完整** JSON（含全部 schemes、subsystems、constraints、scopeLimits、successCriteria）。
${complex ? '复杂项目：保留 2-3 套方案差异。' : '至少 2 套方案。'}`;

  return [
    { role: 'system', content: system },
    { role: 'user', content: user },
  ];
}
