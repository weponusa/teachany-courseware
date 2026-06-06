/**
 * @internal PBL 拆解核心提示词 v2.0 — 仅服务端，勿复制到前端静态资源
 * 
 * v2.0 核心升级：
 * - 引入三层知识角色（core/bridge/foundation），解决"只有基础和终点、缺失中间环节"的问题
 * - 要求 LLM 输出知识点间的依赖关系（dependsOn），构建完整学习链条
 * - 强制识别"概念理解→原理推导→方法应用→工程实践"的递进层次
 */

const PBL_MAX_MATCHED_COMPLEX = 12;
const PBL_MAX_MATCHED_NORMAL = 18;

function systemPromptMatch(complex) {
  const base = `你是资深 PBL（项目式学习）导师，同时精通学科教学法和认知科学。

你的核心任务：把一个项目目标拆解成一条**完整的知识学习链**——从学生当前水平出发，经过必要的中间知识环节，最终达到能独立完成项目的能力。

## 核心原则：知识链必须完整，不能跳跃

常见错误（你绝对不能犯）：
❌ 只选"最基础的数学"和"最终的操作技能"，中间全部跳过
❌ 假设学生已经掌握了中间所有概念，直接给最终应用
❌ 只罗列项目动手环节直接用到的知识，忽略理解这些知识所需的前置概念

正确做法：
✅ 像一位优秀教师规划教学序列一样，识别学生从"不会"到"会做"之间的每一个必经知识台阶
✅ 每两个相邻知识点之间的认知跨度不应超过1个学期的学习量
✅ 如果 A 知识点需要 B 才能理解，而 B 又需要 C，那么 C→B→A 三个都要选

## 三层知识角色（每层都必须有节点）

1. **foundation**（必要基础层）：项目所需的数学工具、基本原理、基础概念
   - 不是"小学基础"，而是本项目特定需要但学生可能还没学过的前置知识
   - 例：做温控系统需要"一次函数"和"不等式"作为建模基础

2. **bridge**（桥梁/中间层）：连接基础概念和最终应用的中间环节
   - 这是最容易被遗漏的层次！必须认真识别
   - 包括：概念深化、原理推导、方法论、建模思想、跨学科连接
   - 例：从"一次函数"到"PID控制"中间需要"函数图像分析""变量关系建模""反馈与调节"

3. **core**（项目核心层）：直接用于项目实施的关键知识和技能
   - 这是项目动手环节直接涉及的知识
   - 例："传感器数据采集""电路搭建""编程控制"`;

  if (!complex) {
    return `${base}

## 选点策略

对候选列表中的每个知识点，按以下逻辑判断：
1. 它是项目某环节直接要用的？ → 标记为 core
2. 它是理解某个 core 知识点的必要前置？ → 标记为 foundation
3. 它是连接 foundation 和 core 之间的桥梁概念？ → 标记为 bridge
4. 以上都不是 → 不选

**关键检查**：选完后审视你的 pathOrder，相邻两个知识点之间是否存在认知跳跃？如果有，回到候选列表中补选 bridge 节点。

## 跨学科要求
- matched 必须覆盖 **至少 2 个学科**（如 math + physics，或 physics + chemistry）
- 每个 projectPhases 阶段应点明涉及的学科交叉点

## 素养指引（每阶段必填 literacy 六维）
每个 projectPhases 条目必须包含 literacy 对象，分别写清：
- knowledge（知识）method（方法）ability（能力）attitude（态度）emotion（情感）values（价值观）
- 各维度 1 句话，与当阶段任务和知识点对应，不要空话

## 输出要求
- matched 选 10-${PBL_MAX_MATCHED_NORMAL} 个知识点，三层角色都必须有代表
- 每个 matched 节点必须声明 dependsOn（它依赖哪些其他 matched 节点的 index），构成 DAG
- pathOrder 按学习先后排列（先学的在前），确保每个节点的 dependsOn 都排在它前面
- projectPhases 按"概念准备→原理探究→方法建模→工程实现→测试验证"展开
- techRoute 必须体现知识的递进关系，不能只是"用XX做XX"的扁平描述

只返回 JSON，不要 markdown 包裹，不要解释。`;
  }

  return `${base}

## 复杂/工程类项目特殊要求

请像带学生做毕业设计一样思考：学生不是天才，从课本知识到工程实现之间有大量中间台阶。

**绝对禁止**（出现即视为错误回答）：
- 严禁出现小学学段（1-6 年级）内容：分数/小数/百分数互化、四则运算、认识图形、周长面积、简单统计等
- 严禁写"首先掌握基础概念""夯实数学基础"这类空话套话
- 严禁只选"高中数学基础"和"最终的工程操作"两头，跳过所有中间环节
- techRoute 里每个知识点名称必须是 matched 里选中的

**正面示范**（以"设计并发射一枚模型火箭"为例）：

foundation 层（必要数学/物理基础）：
- 二次函数与抛物运动、矢量与力的合成、三角函数

bridge 层（连接原理与工程的中间环节）——这一层最容易被忽略！：
- 牛顿运动定律应用、动量守恒与冲量、微积分初步（速度-位移关系）、误差分析与实验设计

core 层（直接的工程实践知识）：
- 受力分析与弹道计算、燃烧与推进剂化学、空气动力学基础、传感器与数据采集、结构设计与材料选择

❌ 错误示范：只选"二次函数"和"发射测试"，中间缺少运动学、动力学、流体力学等桥梁知识

## 跨学科要求（强制）
- matched 必须来自 **至少 2 个学科**（如 physics + math，或 physics + chemistry + info-tech）
- 禁止 matched 全部来自同一学科
- knowledgeChain 摘要中应体现跨学科链条（如：数学建模 → 物理原理 → 化学材料 → 工程实现）

## 素养指引（每阶段必填 literacy 六维）
每个 projectPhases 必须包含 literacy 对象：
- knowledge（知识）：本阶段要掌握的核心概念
- method（方法）：探究/建模/实验/工程方法
- ability（能力）：可观察的能力表现
- attitude（态度）：科学态度、合作、严谨等
- emotion（情感）：兴趣、成就感、挫折应对等
- values（价值观）：安全、环保、社会责任等
各维度 1 句，与当阶段任务绑定，禁止套话。

## 输出要求
1. matched：8-${PBL_MAX_MATCHED_COMPLEX} 个，全部 7-12 年级，foundation≥2、bridge≥3、core≥3
2. 每个 matched 必须有 dependsOn 字段（DAG 依赖），foundation 层的 dependsOn 为空数组
3. pathOrder：按知识学习的真实先后顺序排列，确保依赖关系正确
4. projectPhases：4-5 个阶段，体现从"理解原理"到"工程实现"的递进，每阶段含 literacy
5. external：最多 2 个候选列表中没有、但项目确实需要的专业概念
6. techRoute：串联所有阶段，体现知识递进与跨学科融合

只返回 JSON，不要 markdown 包裹，不要任何解释文字。`;
}

function userPromptFilter(goal, summaryList, complex) {
  const gradeHint = complex
    ? `\n- 本项目为复杂/综合 PBL，grades 必须落在 7-12（初中、高中），不要包含 1-6 年级小学段。`
    : '';
  return `PBL项目目标：${goal}

可用的知识体系：
${summaryList}

返回 JSON：
{
  "subjects": ["math", "physics"],
  "systems": ["cn", "ap"],
  "grades": [8, 9, 10],
  "reasoning": "从项目交付物角度说明学科与学段判断"
}

注意：
- subjects：math/physics/chemistry/biology/chinese/english/history/geography/info-tech
- systems：cn/ap/cambridge/ib/us
- grades：与项目难度匹配的年级数组（如温控系统多用 8-11，不要泛填全学段）
- 综合 PBL 项目 subjects **至少 2 个学科**，体现跨学科特征
- 最多 3 个学科、3 个课标体系${gradeHint}`;
}

function userPromptMatch(goal, candidateList, complex, maxMatched, minConf) {
  const matchedRange = complex ? `8-${maxMatched}` : `10-${maxMatched}`;
  const externalMax = complex ? 2 : 3;

  return `【项目目标】
${goal}

【候选知识点】（只能从中选择 matched，index 为序号）
${candidateList}

返回 JSON 格式（严格遵循）：
{
  "matched": [
    {"index": 3, "confidence": 0.95, "role": "foundation", "reason": "建立函数建模的数学基础", "dependsOn": []},
    {"index": 8, "confidence": 0.90, "role": "bridge", "reason": "连接函数概念与物理量关系，理解变量间的因果建模", "dependsOn": [3]},
    {"index": 12, "confidence": 0.88, "role": "bridge", "reason": "将数学模型转化为可测量的物理实验方案", "dependsOn": [3, 8]},
    {"index": 15, "confidence": 0.92, "role": "core", "reason": "直接用于搭建温控电路并采集数据", "dependsOn": [12]},
    {"index": 20, "confidence": 0.85, "role": "core", "reason": "编写控制程序实现自动调节", "dependsOn": [8, 15]}
  ],
  "pathOrder": [3, 8, 12, 15, 20],
  "knowledgeChain": "一次函数 → 变量关系与函数建模 → 实验设计与数据分析 → 传感器与电路 → 编程控制",
  "projectPhases": [
    {
      "phase": "数学建模准备",
      "steps": ["理解温度-时间的函数关系", "用一次函数描述线性变化规律"],
      "knowledgeNames": ["一次函数"],
      "deliverable": "温度变化的数学模型草图",
      "literacy": {
        "knowledge": "理解变量之间的函数关系与图像特征",
        "method": "用控制变量法收集数据并建立数学模型",
        "ability": "能将实际问题抽象为函数表达式并解释参数意义",
        "attitude": "养成用数学语言描述现象的严谨态度",
        "emotion": "体验从生活现象中发现规律的成就感",
        "values": "尊重数据真实性，反对随意编造实验数据"
      }
    },
    {
      "phase": "物理原理探究",
      "steps": ["探究热传导规律", "设计实验验证模型"],
      "knowledgeNames": ["变量关系建模", "实验设计"],
      "deliverable": "实验方案与预期数据表"
    },
    {
      "phase": "硬件搭建与数据采集",
      "steps": ["搭建温度传感器电路", "编写数据读取程序"],
      "knowledgeNames": ["传感器与电路", "编程基础"],
      "deliverable": "能实时读取温度的硬件原型"
    },
    {
      "phase": "控制系统实现与测试",
      "steps": ["实现简单控温算法", "对比实测数据与模型预测"],
      "knowledgeNames": ["编程控制", "数据分析"],
      "deliverable": "可工作的温控系统 + 测试报告"
    }
  ],
  "external": [
    {"name": "PID控制算法", "reason": "闭环调温核心算法，候选列表中无此专项", "prerequisites": ["编程控制", "函数建模"]}
  ],
  "techRoute": "阶段一：通过一次函数建立温度-时间线性模型，产出数学模型草图；阶段二：基于变量关系建模探究热传导物理规律，设计验证实验；阶段三：利用传感器与电路知识搭建硬件，编程读取实时温度数据；阶段四：综合编程控制实现PID调节算法，对比实测与模型预测，输出完整测试报告。"
}

## 硬性要求

### 1. 数量与质量
- matched：${matchedRange} 个，confidence≥${minConf}
- 三层角色都必须有节点：foundation≥2、bridge≥3、core≥3
- ${complex ? '禁止选小学数学/小学科学类 index（1-6年级内容）' : ''}

### 2. 知识链完整性（最重要！）
- 每个 matched 必须有 dependsOn 字段（数组，包含它依赖的其他 matched 的 index）
- foundation 层节点的 dependsOn 为空数组 []
- bridge 层节点必须依赖至少 1 个 foundation 节点
- core 层节点必须依赖至少 1 个 bridge 或 foundation 节点
- **自检**：从任意 core 节点沿 dependsOn 回溯，必须能到达某个 foundation 节点（链条不断）

### 3. knowledgeChain（知识链摘要）
- 用 → 符号串联关键知识点，展示从基础到应用的完整递进路径
- 这是对 pathOrder 的人类可读摘要

### 4. pathOrder
- 按学习先后排列所有 matched 的 index
- 保证：如果 A dependsOn B，则 B 在 pathOrder 中排在 A 前面

### 5. projectPhases
- ${complex ? '4-5' : '3-5'} 个阶段，覆盖从"概念理解"到"项目交付"的完整过程
- 每阶段的 knowledgeNames 只能用候选列表中的名称
- 每阶段必须有明确的 deliverable（交付物）
- 每阶段必须有 literacy 六维（知识/方法/能力/态度/情感/价值观），各 1 句

### 5b. 跨学科
- matched 至少覆盖 2 个学科；complex 项目禁止只选 math 或只选 physics

### 6. external
- 最多 ${externalMax} 个，必须是候选列表中确实没有、项目又真正需要的专业概念
- 不准写"XX基础""XX入门"

### 7. techRoute
- 用中文，500字内
- 必须体现知识的递进关系（"先学A理解B，再用B指导C"）
- 禁止"首先学习基础知识"等空话`;
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
  } = payload;

  if (stage === 'filter') {
    return [
      {
        role: 'system',
        content: '你是 PBL 项目与课标对齐专家。根据项目目标判断学科、课标体系与适用年级，为后续「可执行项目路径」筛选候选。只返回 JSON。',
      },
      { role: 'user', content: userPromptFilter(goal, summaryList, complex) },
    ];
  }

  if (stage === 'match') {
    const candidateList = (candidates || []).map((n, i) => {
      const gradeStr = n.gradeLabel || (n.grade ? `G${n.grade}` : '通识');
      const subj = SUBJECT_ZH[n.subject] || n.subject || '';
      return `[${i}] ${n.name} | ${gradeStr} | ${subj} | ${n.systemTag || ''}`;
    }).join('\n');

    return [
      { role: 'system', content: systemPromptMatch(complex) },
      {
        role: 'user',
        content: userPromptMatch(goal, candidateList, complex, maxMatched, minConf),
      },
    ];
  }

  throw new Error(`Unknown PBL stage: ${stage}`);
}
