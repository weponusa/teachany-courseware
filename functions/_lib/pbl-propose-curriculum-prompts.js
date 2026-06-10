/**
 * @internal PBL 知识点提案 — 模型先列应学课标，再由客户端对齐图谱
 */

import { formatGradeConstraint } from './pbl-grade-constraint.js';

function formatBlueprintPhases(blueprint) {
  if (!blueprint) return '（无拆解蓝图）';
  const scheme = (blueprint.schemes || []).find(s => s.id === blueprint.recommendedSchemeId)
    || (blueprint.schemes || [])[0];
  return (scheme?.phases || []).slice(0, 6).map((p, i) => {
    const hints = (p.knowledgeHints || []).slice(0, 5).join('、');
    return `  ${i + 1}. ${p.phase || '阶段'}｜产出：${p.deliverable || '—'}${hints ? `｜线索：${hints}` : ''}`;
  }).join('\n');
}

function isAdultOrUniversity(projectSpec, goal) {
  if (projectSpec?.gradeLevel === 'adult' || projectSpec?.gradeLevel === 'university') return true;
  return /成人|在职|大学|本科|研究生|工程实施方案|企业|产业级/.test(String(goal || ''));
}

/**
 * @param {object} payload
 */
export function buildProposeCurriculumMessages(payload) {
  const {
    goal = '',
    projectBlueprint = null,
    projectSpec = null,
    deliverable = '',
    maxProposed = 12,
  } = payload;

  const gradeLine = formatGradeConstraint(projectSpec);
  const phases = formatBlueprintPhases(projectBlueprint);
  const adultOrUni = isAdultOrUniversity(projectSpec, goal);

  const system = `${adultOrUni ? '你是成人/大学 PBL 工程课程设计专家。根据项目目标与拆解蓝图，列出学习者完成本项目应掌握的专业知识点（优先使用工程、计算机、航天系统、系统设计等专业表述，不输出 K12 课标节点）。' : '你是 K12 PBL 课程设计专家。根据项目目标与拆解蓝图，列出学生完成本项目**应学的课内知识点**（用中国课标常见表述，不必输出图谱 id）。'}

## 原则
1. 每个知识点须能回答：学它如何支撑项目的某一具体环节（调研、测算、实验、写作、制作等）。
2. ${adultOrUni ? '名称用专业常见说法（如「空间数据中心系统架构」「任务调度与资源编排」「热控与功耗约束」「通信链路预算」），不要写中小学课标节点。' : '名称用课标常见说法（如「条形统计图与折线统计图」「植物的一生（种子到果实）」），可近似但不要编造课标里没有的概念。'}
3. 按教学逻辑排序：前置 → 方法 → 核心应用；标注 role：foundation / bridge / core。
4. ${adultOrUni ? `学段约束：${gradeLine || '成人/大学'}，允许专业/大学层知识点，禁止用二次函数、三角函数、语文表达等 K12 节点凑数。` : (gradeLine ? `学段约束：${gradeLine}，禁止列出明显超龄或大学层知识点。` : '未指定学段时可跨 K12，但不要写大学专业课。')}
5. 数量 ${Math.max(5, maxProposed - 4)}–${maxProposed} 个，宁精勿滥，不要为凑学科堆无关节点。
6. 禁止：批判性思维、团队协作、核心素养等泛素养条目。
7. **学科相关性**：每个知识点必须与项目目标有**直接因果联系**（能说清"学了它才能完成项目哪个环节"），不能仅凭"课标里有"或"学科能凑上"就选入。工程/制作/探究类项目中，文言文、古诗词鉴赏等纯文学节点通常与项目无因果联系，除非交付物明确涉及写作或文学创作——请据实判断，不要盲目排除也不要盲目选入。
8. **科学/工程类项目的两类必选节点（硬性）**：
   - **科学技术原理类**（≥2 个）：物理/化学/生物/科学中与项目直接相关的原理节点（如电路原理、力与运动、化学反应、溶液配制、生物结构等）。这类节点解释"为什么这样做能成功"。
   - **数学技能类**（≥1 个）：统计分析、数据记录与图表、测量与计算、函数关系等数学方法节点。这类节点解释"如何量化验证与优化"。
   - 判断依据：如果项目涉及动手制作/实验/测量/对比/数据收集，则上述两类缺一不可。只有纯人文/文学/策划类项目可以不含理科原理。

只返回 JSON，不要 markdown。`;

  const user = `【项目目标】${goal}
【交付物】${deliverable || projectBlueprint?.deliverable || '（见蓝图）'}
${gradeLine ? `【学段】${gradeLine}\n` : ''}【拆解蓝图阶段】
${phases}

返回 JSON：
{
  "proposed": [
    {
      "name": "条形统计图与折线统计图",
      "subject": "math",
      "gradeHint": 4,
      "phase": "数据统计",
      "role": "core",
      "reason": "用于汇总义卖收入并画趋势图"
    }
  ],
  "knowledgeChain": "模块A → 模块B → 模块C",
  "summary": "一句话说明知识链设计思路"
}

subject 取值：${adultOrUni ? 'computer-science/engineering/physics/info-tech/math' : 'math/physics/chemistry/biology/science/chinese/english/history/geography/info-tech'}
gradeHint：${adultOrUni ? '成人/大学项目可省略或填 0' : '1–12 的整数，不确定可省略'}`;

  return [
    { role: 'system', content: system },
    { role: 'user', content: user },
  ];
}
