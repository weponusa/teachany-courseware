/**
 * @internal PBL 拆解核心提示词 v3.0 — 仅服务端，勿复制到前端静态资源
 *
 * v3.0 核心升级（针对「火箭等项目匹配跑偏」）：
 * - 强制「工程子系统拆解」：推进/气动/结构/控制等能力域必须先于选点
 * - 每个 matched 必须映射到具体子系统，禁止选与交付物无关的泛数学/泛控制
 * - 示例 JSON 改为模型火箭（不再用温控，避免模型照抄错误领域）
 * - 引入能力域覆盖硬性约束 + 相关性自检
 */

const PBL_MAX_MATCHED_COMPLEX = 12;
const PBL_MAX_MATCHED_NORMAL = 18;

/** 根据项目目标推断工程子系统（服务端兜底，与前端 domain 逻辑对齐） */
function inferProjectDomains(goal) {
  const g = String(goal || '');
  if (/火箭|导弹|发射|弹道|模型火箭|航天/.test(g)) {
    return [
      {
        id: 'propulsion',
        label: '推进与燃料',
        keywords: ['燃烧', '氧化', '燃料', '热值', '内能', '化学能', '能量转化', '推进', '反应'],
        subjects: ['chemistry', 'physics'],
      },
      {
        id: 'aerodynamics',
        label: '空气动力与弹道',
        keywords: ['抛体', '流体', '压强', '流速', '气动', '弹道', '抛物', '飞行轨迹'],
        subjects: ['physics', 'math'],
      },
      {
        id: 'dynamics',
        label: '运动学与动力学',
        keywords: ['牛顿', '动量', '冲量', '受力', '加速度', '机械能', '守恒', '运动'],
        subjects: ['physics', 'math'],
      },
      {
        id: 'structure',
        label: '结构与材料',
        keywords: ['结构', '材料', '强度', '压强', '设计', '稳定性'],
        subjects: ['physics', 'chemistry'],
      },
      {
        id: 'control',
        label: '控制、传感与测试',
        keywords: ['控制', '传感', '电路', '编程', '算法', '数据采集', '实验', '误差', '测试'],
        subjects: ['info-tech', 'physics'],
      },
    ];
  }
  if (/温控|温室|温度|加热|散热|PID|闭环/.test(g)) {
    return [
      { id: 'modeling', label: '数学建模', keywords: ['函数', '方程', '建模', '图像'], subjects: ['math'] },
      { id: 'physics', label: '热学原理', keywords: ['热传导', '温度', '内能', '热量'], subjects: ['physics'] },
      { id: 'hardware', label: '传感与电路', keywords: ['传感器', '电路', '采集'], subjects: ['physics', 'info-tech'] },
      { id: 'control', label: '控制算法', keywords: ['控制', '反馈', '编程', '算法'], subjects: ['info-tech', 'math'] },
    ];
  }
  return [];
}

function formatDomainHints(domains) {
  if (!domains.length) return '';
  return domains.map((d, i) =>
    `${i + 1}. 【${d.label}】必覆盖。检索候选时请优先匹配名称/课标描述中含：${d.keywords.join('、')}；学科倾向：${(d.subjects || []).join('、')}`
  ).join('\n');
}

function systemPromptMatch(complex) {
  const base = `你是资深 PBL（项目式学习）导师，同时精通 K12 课标与工程教育。

## 第一步（必做）：拆解项目工程子系统

在选任何候选 index 之前，先在脑中回答：
「要完成这个项目交付物，学生必须分别解决哪几个**独立子问题**？」

例如「设计并发射模型火箭」必须覆盖：
- 推进与燃料：燃料燃烧、化学能→动能、推进剂选型
- 空气动力与弹道：气流、阻力、飞行轨迹、抛体运动
- 运动学与动力学：牛顿定律、动量、受力与加速度
- 结构与材料：箭体强度、重心、稳定性
- 控制与测试：发射角度、数据采集、实验设计与安全

**禁止**跳过子系统直接选「看起来高级」但与项目无关的知识点（如：与火箭无关的纯代数、无关的语文阅读、无关的生物细胞）。

## 第二步：从候选列表选点（相关性门禁）

对候选列表中每个 index，必须通过以下测试才能入选：
1. **子系统测试**：它能支撑上述哪一个子系统？reason 里必须写明「子系统：XXX」
2. **删除测试**：若删掉该知识点，学生完成该子系统会明显受阻吗？若不会 → 不选
3. **课标测试**：名称必须来自候选列表原文，不得编造候选中没有的知识点当作 matched

## 三层知识角色

- **foundation**：完成某子系统所需的工具性知识（如：矢量分解、氧化还原概念）
- **bridge**：连接 foundation 与工程实现（如：抛体运动分析、流体压强与升力阻力）
- **core**：直接用于动手环节（如：燃料热值计算、发射实验设计、结构强度估算）

常见错误（绝对禁止）：
❌ 只选 PID、一次函数等「泛控制/泛数学」，却没有燃料、气动、推进、抛体等本项目核心知识
❌ 选与项目八竿子打不着的课标节点（如：遗传、古诗词、世界史）凑数量
❌ 候选里有「抛体运动」「内能与热量」「流体压强」却不选，反而选无关内容
❌ reason 写空话「建立基础」「培养能力」，不写对应哪个子系统`;

  if (!complex) {
    return `${base}

## 简单项目输出要求
- matched 10-${PBL_MAX_MATCHED_NORMAL} 个，foundation/bridge/core 均有，且覆盖至少 2 个子系统
- 每个 matched 的 reason 以「子系统：」开头
- dependsOn 构成 DAG；pathOrder 满足依赖顺序
- projectPhases 4-5 阶段，每阶段 literacy 六维（知识/方法/能力/态度/情感/价值观）各 1 句
- knowledgeChain 用 → 串联子系统递进路径

只返回 JSON，不要 markdown，不要解释。`;
  }

  return `${base}

## 复杂/工程类项目（火箭、机器人、温控系统等）

### 能力域硬性覆盖（matched 必须满足）
- 至少覆盖 **3 个不同工程子系统**（用户提示中会列出）
- **每个列出的子系统至少 1 个 matched**；不得全部挤在同一子系统
- matched 来自 **至少 2 个学科**（如 physics + chemistry，或 physics + info-tech）
- foundation≥2、bridge≥3、core≥3

### 火箭类项目选点清单（候选中有近似名称时优先选）
| 子系统 | 应优先在候选中找的课标词 |
| 推进与燃料 | 氧化还原、燃烧、内能、热值、化学能、能量转化 |
| 空气动力与弹道 | 抛体运动、流体压强、流速、大气压、飞行 |
| 运动学与动力学 | 牛顿运动定律、动量、冲量、机械能、受力分析 |
| 结构与材料 | 压强、材料、结构设计（勿选小学「认识图形」） |
| 控制与测试 | 实验设计、数据采集、算法、传感器、电路（勿凭空写 PID 除非候选中有） |

### 绝对禁止
- 小学 1-6 年级内容
- matched 全部来自同一学科
- 用无关知识点凑满 8 个
- techRoute / knowledgeNames 出现候选列表中不存在的名称

只返回 JSON，不要 markdown，不要任何解释文字。`;
}

function systemPromptFilter(complex) {
  const gradeHint = complex
    ? 'grades 必须 7-12，不含小学。复杂工程类项目 subjects 必须含 physics，且至少再加 chemistry 或 info-tech 之一。'
    : '';
  return `你是 PBL 项目与课标对齐专家，擅长把**工程/制作类**项目拆解为可检索的学科与子系统。

## 工作流程
1. 判断项目类型：工程制作 / 科学探究 / 创意设计 / 调查
2. 列出 3-5 个**工程子系统**（如火箭：推进、气动、结构、控制）
3. 为每个子系统映射学科：math / physics / chemistry / biology / info-tech 等
4. 确定适用 grades 与 systems

## 火箭/发射类项目
- subjects 必须包含 physics，并包含 chemistry（推进/燃烧）或 info-tech（控制/采集）至少其一
- 不要只筛 math

${gradeHint}

只返回 JSON。`;
}

function userPromptFilter(goal, summaryList, complex) {
  const domains = inferProjectDomains(goal);
  const domainBlock = domains.length
    ? `\n【本项目工程子系统参考（filter 的 subjects 须能覆盖这些）】\n${formatDomainHints(domains)}\n`
    : '';
  const gradeHint = complex
    ? `\n- grades 必须落在 7-12（初中、高中）`
    : '';
  return `PBL项目目标：${goal}
${domainBlock}
可用的知识体系：
${summaryList}

返回 JSON：
{
  "subjects": ["physics", "chemistry", "math", "info-tech"],
  "systems": ["cn", "ap"],
  "grades": [8, 9, 10],
  "projectDomains": ["推进与燃料", "空气动力与弹道", "运动学与动力学", "结构与材料", "控制与测试"],
  "reasoning": "说明各子系统对应的学科与年级"
}

注意：
- subjects：math/physics/chemistry/biology/chinese/english/history/geography/info-tech/science
- systems：cn/ap/cambridge/ib/us
- projectDomains：从项目交付物拆出的 3-5 个子系统名称
- 工程/制作类 subjects **至少 2 个学科**，火箭类必须含 physics
- 最多 4 个学科${gradeHint}`;
}

function userPromptMatch(goal, candidateList, complex, maxMatched, minConf, domainHints) {
  const matchedRange = complex ? `8-${maxMatched}` : `10-${maxMatched}`;
  const externalMax = complex ? 2 : 3;
  const domains = domainHints && domainHints.length ? domainHints : inferProjectDomains(goal);
  const domainSection = domains.length
    ? `\n【工程子系统 — 每个至少 1 个 matched，reason 必须以「子系统：XXX」开头】\n${formatDomainHints(domains)}\n`
    : '';

  // v3.0：主示例改为模型火箭，避免 LLM 照抄温控导致跑偏
  const rocketExample = complex ? `
返回 JSON 格式（严格遵循；下列 index 仅为**格式示范**，你必须在【候选知识点】中重新检索并填写真实 index，禁止照抄示例数字）：
{
  "matched": [
    {"index": 2, "confidence": 0.93, "role": "foundation", "reason": "子系统：运动学与动力学。建立受力与加速度关系，为弹道分析打基础", "dependsOn": []},
    {"index": 5, "confidence": 0.91, "role": "foundation", "reason": "子系统：推进与燃料。理解燃烧与氧化还原，解释化学能转化为推进动能", "dependsOn": []},
    {"index": 8, "confidence": 0.90, "role": "bridge", "reason": "子系统：空气动力与弹道。将运动分解为水平和竖直分量，分析飞行轨迹", "dependsOn": [2]},
    {"index": 11, "confidence": 0.89, "role": "bridge", "reason": "子系统：空气动力与弹道。理解气流与压强差，解释箭体所受升力与阻力", "dependsOn": [8]},
    {"index": 14, "confidence": 0.88, "role": "bridge", "reason": "子系统：推进与燃料。用热值与内能估算燃料释放能量与推进效率", "dependsOn": [5]},
    {"index": 17, "confidence": 0.92, "role": "core", "reason": "子系统：运动学与动力学。用牛顿定律分析发射瞬间推力与加速度", "dependsOn": [2, 8]},
    {"index": 20, "confidence": 0.87, "role": "core", "reason": "子系统：结构与材料。分析箭体压强与结构强度，确保飞行稳定", "dependsOn": [11]},
    {"index": 23, "confidence": 0.86, "role": "core", "reason": "子系统：控制与测试。设计发射实验、测量飞行高度与落点，完成测试方案", "dependsOn": [17, 20]}
  ],
  "pathOrder": [2, 5, 8, 11, 14, 17, 20, 23],
  "knowledgeChain": "氧化还原与燃烧 → 内能/热值 → 牛顿定律与抛体运动 → 流体压强与阻力 → 结构强度 → 发射实验与数据采集",
  "projectPhases": [
    {
      "phase": "推进原理与燃料选型",
      "steps": ["分析推进剂燃烧反应", "估算化学能转化为动能"],
      "knowledgeNames": ["氧化还原反应概念", "内能与热量"],
      "deliverable": "推进剂方案与能量估算表",
      "literacy": {
        "knowledge": "理解燃烧本质是氧化还原与能量释放",
        "method": "用热值数据估算推进能量",
        "ability": "能比较不同推进方案的化学能输出",
        "attitude": "严谨对待化学品使用与用量计算",
        "emotion": "对「一点燃料推动火箭」的化学反应感到好奇",
        "values": "树立实验安全与环保意识，合规处置残余药剂"
      }
    },
    {
      "phase": "弹道与空气动力分析",
      "steps": ["建立抛体运动模型", "讨论气流对箭体的影响"],
      "knowledgeNames": ["抛体运动", "流体压强与流速关系"],
      "deliverable": "弹道预测草图与关键参数表",
      "literacy": {
        "knowledge": "掌握抛体分解与流体压强基本原理",
        "method": "用物理模型预测轨迹并标注假设条件",
        "ability": "能解释发射角度与射程的关系",
        "attitude": "养成先建模再实验的科学思维",
        "emotion": "体验用公式预测飞行轨迹的成就感",
        "values": "尊重实测数据，不夸大模型精度"
      }
    },
    {
      "phase": "结构设计与制作",
      "steps": ["设计箭体结构", "检查重心与稳定性"],
      "knowledgeNames": ["牛顿运动定律"],
      "deliverable": "模型火箭原型与结构说明",
      "literacy": {
        "knowledge": "理解受力平衡与运动状态改变条件",
        "method": "用工程草图表达结构尺寸与连接方式",
        "ability": "能根据力学分析改进结构设计",
        "attitude": "细致检查每个连接部位",
        "emotion": "享受从图纸到实物的创造过程",
        "values": "强调制作规范与发射安全距离"
      }
    },
    {
      "phase": "发射测试与迭代",
      "steps": ["制定发射与测距方案", "记录数据并对比预测"],
      "knowledgeNames": ["抛体运动"],
      "deliverable": "测试报告（预测 vs 实测）",
      "literacy": {
        "knowledge": "综合运用动力学与弹道知识解释偏差",
        "method": "控制变量法组织对比发射实验",
        "ability": "能根据测试数据提出改进建议",
        "attitude": "客观记录失败发射并分析原因",
        "emotion": "在迭代中保持对科学探究的热情",
        "values": "遵守安全规程，对他人与场地负责"
      }
    }
  ],
  "external": [
    {"name": "模型火箭安全发射规范", "reason": "课标中无专项安全规程，但发射环节必需", "prerequisites": ["发射实验设计"]}
  ],
  "techRoute": "阶段一：从氧化还原与内能/热值理解推进剂能量；阶段二：用抛体运动与流体压强建立弹道模型；阶段三：依据牛顿定律完成结构受力设计与制作；阶段四：实施发射测试，用数据验证并迭代优化。"
}` : `
返回 JSON 格式（严格遵循）：
{
  "matched": [
    {"index": 3, "confidence": 0.95, "role": "foundation", "reason": "子系统：数学建模。建立变量函数关系", "dependsOn": []},
    {"index": 8, "confidence": 0.90, "role": "bridge", "reason": "子系统：原理探究。连接模型与实验", "dependsOn": [3]}
  ],
  "pathOrder": [3, 8],
  "knowledgeChain": "基础概念 → 原理探究 → 工程实现",
  "projectPhases": [],
  "external": [],
  "techRoute": "按子系统递进实施"
}`;

  return `【项目目标】
${goal}
${domainSection}
【候选知识点】（matched 只能选下列 index；先通读全文，按子系统检索关键词再选）
${candidateList}

${rocketExample}

## 硬性要求

### 0. 相关性（最高优先级）
- 每个 matched 的 reason **必须以「子系统：」开头**，写明支撑哪个工程子系统
- 选完后自检：推进/燃料、气动/弹道、控制/测试 是否都有代表？若候选中有「抛体」「内能」「流体」「氧化」「牛顿」等词却未选，必须重新审视
- **禁止**选与项目子系统无关的节点凑数

### 1. 数量与角色
- matched：${matchedRange} 个，confidence≥${minConf}
- foundation≥2、bridge≥3、core≥3（complex 项目）
- ${complex ? '禁止 1-6 年级小学 index' : ''}

### 2. 知识链
- dependsOn 构成 DAG；pathOrder 满足依赖
- knowledgeChain 体现子系统递进（如：燃料能量 → 弹道 → 结构 → 测试）

### 3. projectPhases
- ${complex ? '4-5' : '3-5'} 个阶段，按子系统组织
- knowledgeNames **只能**使用候选列表中出现的名称（字面匹配或明显子串）
- 每阶段 literacy 六维各 1 句，禁止套话

### 4. 跨学科
- matched 至少 2 个学科；火箭类须有 physics + (chemistry 或 info-tech)

### 5. external
- 最多 ${externalMax} 个，候选中确实没有、项目又必需的专业概念

### 6. techRoute
- 中文，500 字内，按子系统串联，体现「先推进原理→再弹道→再结构→再测试」类递进`;
}

const SUBJECT_ZH = {
  math: '数学', physics: '物理', chemistry: '化学', biology: '生物',
  science: '科学', 'info-tech': '信息技术', chinese: '语文', english: '英语',
  history: '历史', geography: '地理',
};

/**
 * @param {'filter'|'match'} stage
 * @param {object} payload
 * @returns {{ role: string, content: string }[]}
 */
export function buildPBMessages(stage, payload) {
  const {
    goal = '',
    summaryList = '',
    candidates = [],
    complex = false,
    maxMatched = complex ? PBL_MAX_MATCHED_COMPLEX : PBL_MAX_MATCHED_NORMAL,
    minConf = 0.68,
    domainHints = null,
  } = payload;

  if (stage === 'filter') {
    return [
      { role: 'system', content: systemPromptFilter(complex) },
      { role: 'user', content: userPromptFilter(goal, summaryList, complex) },
    ];
  }

  if (stage === 'match') {
    const candidateList = (candidates || []).map((n, i) => {
      const gradeStr = n.gradeLabel || (n.grade ? `G${n.grade}` : '通识');
      const subj = SUBJECT_ZH[n.subject] || n.subject || '';
      return `[${i}] ${n.name} | ${gradeStr} | ${subj} | ${n.systemTag || ''}`;
    }).join('\n');

    const hints = domainHints && domainHints.length ? domainHints : inferProjectDomains(goal);

    return [
      { role: 'system', content: systemPromptMatch(complex) },
      {
        role: 'user',
        content: userPromptMatch(goal, candidateList, complex, maxMatched, minConf, hints),
      },
    ];
  }

  throw new Error(`Unknown PBL stage: ${stage}`);
}

export { inferProjectDomains };
