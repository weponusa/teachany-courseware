/**
 * @internal PBL matched 节点相关性二审 — 剔除 LLM match 幻觉
 */

/**
 * @param {object} payload
 * @param {string} payload.goal
 * @param {string} [payload.archetypeId]
 * @param {string} [payload.projectType]
 * @param {string[]} [payload.allowedSubjects]
 * @param {string} [payload.deliverable]
 * @param {Array<{index:number,name:string,subject:string,grade:number,reason:string,role:string}>} payload.matched
 */
export function buildVerifyRelevanceMessages(payload) {
  const {
    goal = '',
    archetypeId = '',
    projectType = '',
    allowedSubjects = [],
    deliverable = '',
    matched = [],
  } = payload;

  const subjectHint = allowedSubjects.length
    ? `允许学科白名单：${allowedSubjects.join('、')}`
    : '无硬性学科白名单，但节点须直接服务交付物';

  const nodeBlock = matched.map((n, i) => {
    const gradeLabel = n.grade > 0 ? `G${n.grade}` : '拓展';
    return `${i + 1}. [idx=${n.index}] ${n.name}（${n.subject || '未知'} · ${gradeLabel}）
   role=${n.role || 'core'} | match理由：${n.reason || '（无）'}`;
  }).join('\n');

  const system = `你是 K12 PBL 课标匹配审核员。任务：审查「match 阶段」已选知识点是否真正服务于项目目标与交付物，剔除幻觉/跑题节点。

## 判定标准
1. **keep**：节点能支撑项目实施链中的某一具体环节（调研、测算、科普理解、写作论证等）
2. **remove**：与项目主题/交付物无关；仅为凑学科；历史朝代/革命战争类节点用于购车/工程/科学探究等非历史项目；生物/航空/编程等明显跑题

## 硬性规则
- 消费决策/购车比选类：**禁止** history 及一切历史课标（朝代、战争、革命、丝绸之路等）
- 节点学科须在白名单内（若提供）
- 宁可少留，不可凑数

只返回 JSON，不要 markdown。`;

  const user = `【项目目标】${goal}
【项目类型】${projectType || 'general'}${archetypeId ? `（原型：${archetypeId}）` : ''}
【交付物】${deliverable || '（见蓝图）'}
${subjectHint}

【待审核 matched 节点】共 ${matched.length} 个
${nodeBlock}

返回 JSON：
{
  "remove": [
    {"index": 0, "reason": "与购车决策无关的历史节点"}
  ],
  "summary": "一句话说明审核结论"
}

remove 中 index 必须为各行方括号 idx= 后的候选数组下标；只列出应剔除的节点，未列出视为保留。`;

  return [
    { role: 'system', content: system },
    { role: 'user', content: user },
  ];
}
