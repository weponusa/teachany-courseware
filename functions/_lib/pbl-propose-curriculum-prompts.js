/**
 * @internal PBL 知识点提案 — 模型先列应学课标，再由客户端对齐图谱
 */

function formatBlueprintPhases(blueprint) {
  if (!blueprint) return '（无拆解蓝图）';
  const scheme = (blueprint.schemes || []).find(s => s.id === blueprint.recommendedSchemeId)
    || (blueprint.schemes || [])[0];
  return (scheme?.phases || []).slice(0, 6).map((p, i) => {
    const hints = (p.knowledgeHints || []).slice(0, 5).join('、');
    return `  ${i + 1}. ${p.phase || '阶段'}｜产出：${p.deliverable || '—'}${hints ? `｜线索：${hints}` : ''}`;
  }).join('\n');
}

function formatGradeConstraint(projectSpec) {
  if (!projectSpec?.gradeLevel || projectSpec.gradeLevel === 'any') return '';
  const maps = { primary: '小学 1–6 年级', junior: '初中 7–9 年级', senior: '高中 10–12 年级' };
  const detail = parseInt(projectSpec.gradeDetail, 10);
  if (detail >= 1 && detail <= 12) return `${detail} 年级`;
  return maps[projectSpec.gradeLevel] || projectSpec.gradeLevel;
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

  const system = `你是 K12 PBL 课程设计专家。根据项目目标与拆解蓝图，列出学生完成本项目**应学的课内知识点**（用中国课标常见表述，不必输出图谱 id）。

## 原则
1. 每个知识点须能回答：学它如何支撑项目的某一具体环节（调研、测算、实验、写作、制作等）。
2. 名称用课标常见说法（如「条形统计图与折线统计图」「植物的一生（种子到果实）」），可近似但不要编造课标里没有的概念。
3. 按教学逻辑排序：前置 → 方法 → 核心应用；标注 role：foundation / bridge / core。
4. ${gradeLine ? `学段约束：${gradeLine}，禁止列出明显超龄或大学层知识点。` : '未指定学段时可跨 K12，但不要写大学专业课。'}
5. 数量 ${Math.max(6, maxProposed - 2)}–${maxProposed} 个，宁精勿滥，不要为凑学科堆无关节点。
6. 禁止：批判性思维、团队协作、核心素养等泛素养条目。

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

subject 取值：math/physics/chemistry/biology/science/chinese/english/history/geography/info-tech
gradeHint：1–12 的整数，不确定可省略`;

  return [
    { role: 'system', content: system },
    { role: 'user', content: user },
  ];
}
