import {
  inferBloomFromBlueprint,
  formatBloomHintForFilter,
  formatBloomHintForMatch,
} from './pbl-bloom.js';
import {
  resolveArchetype,
  formatArchetypeForMatch,
  formatRegistryForMatch,
} from './pbl-archetypes.js';

/**
 * @internal PBL 拆解核心提示词 v6.0 — 仅服务端，勿复制到前端静态资源
 *
 * v6.0：泛化重构 — 去掉所有具体案例硬编码（循迹小车/水体过滤/食堂汤水/低空经济/太空馆等），
 *       保留 15 种大类型分类，每种类型给出通用性指导原则，让 AI 根据 goal 文本自行做细节映射。
 * v5.1：Bloom 动词层级 filter + match 约束；候选节点注入先修/定义（RAG lite）
 * v5.0：项目类型自适应
 * v4.0：先全链路拆解可行方案，再匹配课标（decompose → filter → match）
 */

const PBL_MAX_MATCHED_COMPLEX = 12;
const PBL_MAX_MATCHED_NORMAL = 18;

// ============================================================
// 一、项目类型分类（保留 15 种大类型，去掉内部子分支检测函数）
// ============================================================

/**
 * 项目类型分类（自适应多场景）：
 * consumer-decision / creative-media / humanities-literary / business-economics /
 * health-life / planting-cultivation / labor-practice / life-planning /
 * social-inquiry / engineering / scientific-inquiry / industry-innovation /
 * exhibition-redesign / maker-workshop / general
 */
function classifyProjectType(goal) {
  const g = String(goal || '');
  // 消费决策
  if (/购车|买车|选车|消费决策|方案比选|比选|选型|性价比/.test(g)
    || (/对比|比较/.test(g) && /购|买|选|家用|家庭/.test(g) && /新能源|燃油|电动|混动/.test(g))
    || (/哪个更|哪种更|怎么选|如何选择/.test(g) && /车|新能源|电动|手机|电器|产品/.test(g))) {
    return 'consumer-decision';
  }
  // 展陈/场馆改造
  if (/馆|展厅|展览|展陈/.test(g) && /重塑|改造|整治|升级|策展|布展|翻新|重建|优化|设计/.test(g)) return 'exhibition-redesign';
  // 创意媒体
  if (/海报|短视频|微电影|动画|漫画|插画|绘画|策展|广告|品牌|视觉|游戏设计|作曲|音乐创作|手工艺|表演|舞台|摄影|logo|标志设计|文创|周边设计/.test(g)) return 'creative-media';
  // 人文文学
  if (/诗歌|诗集|现代诗|诗词|写诗|小说|剧本|散文|绘本|故事集|演讲|辩论|文学|翻译|双语|新闻稿|采访稿|写一[篇组]|作文|征文|朗诵|文集|杂志|读后感|书评|话剧|文章|诗人|文学家|历史人物|人物研究|名人传记/.test(g)) return 'humanities-literary';
  // 商业经济
  if (/创业|商业计划|营销|市场推广|运营|理财|零花钱|压岁钱|市场调研|义卖|跳蚤市场|店铺|定价|商业模式|盈利|众筹|记账|模拟.*购物/.test(g)) return 'business-economics';
  // 健康生活
  if (/健康|营养|饮食|食谱|减脂|减肥|健身|锻炼|运动会?|近视|视力|护眼|睡眠|作息|心理|情绪|压力|安全|急救|防溺水|防火|卫生|疾病|人体|体重|身高/.test(g)) return 'health-life';
  // 种植养殖
  if (/种植|栽培|养花|花卉|蔬菜|种菜|盆栽|园艺|养殖|养蚕|花坛|绿化|阳台种/.test(g)) return 'planting-cultivation';
  // 劳动实践
  if (/烹饪|烘焙|美食|菜谱|料理|手工|编织|缝纫|收纳|整理|维修|清洁|打扫|劳动/.test(g)) return 'labor-practice';
  // 活动策划/生活规划
  if (/活动策划|策划.{0,6}(活动|晚会|联欢|运动会|典礼|节|比赛)|联欢会|晚会|文艺汇演|毕业典礼|生日会|出游|旅行|研学|游学|路线规划|时间管理|班级布置|嘉年华|游园/.test(g)) return 'life-planning';
  // 社会调查
  if (/田野|问卷|访谈|社区|民俗|传统文化|非遗|人口|城乡|社会现象|调研报告|居民|乡土|口述史|垃圾分类|垃圾治理|环保.*调查/.test(g)) return 'social-inquiry';
  // 产业创新
  if (/低空经济|通航产业|新兴产业|产业创新/.test(g) || (/探寻|探索|研究|调研/.test(g) && /创新|产业|经济|行业/.test(g))) return 'industry-innovation';
  // 工坊/木作
  if (/工坊|鲁班|榫卯|古典.*风格|木结构|建筑模型|微缩|传统建筑|斗拱|飞檐/.test(g)) return 'maker-workshop';
  // 工程/制作
  if (/算力中心|数据中心|太空算力|云计算|边缘计算|计算中心|服务器集群|卫星计算|轨道计算/.test(g)) return 'engineering';
  if (/火箭|导弹|发射|机器人|电路|机械|硬件|装置|App|应用程序|小程序|网站|系统开发|3D打印|传感|智能|温控|储能|光伏|发电|搭建|制作|工程|发明|物联网|编程实现|循迹|小车|无人机|过滤|净水/.test(g)
    && /设计|制作|研发|装置|系统|搭建|开发|探究|实验/.test(g)) return 'engineering';
  // 科学探究
  if (/探究|实验|观察|测量|验证|影响因素|变量|检测|成分|对照实验|科学问题|浓度|溶液|溶解|滴定|电导率/.test(g)) return 'scientific-inquiry';
  return 'general';
}

// ============================================================
// 二、TYPE_PROFILES — 每种大类型的通用描述
// ============================================================

const TYPE_PROFILES = {
  'engineering': { label: '工程研发/制作', moduleWord: '工程子系统（原理 / 装置结构 / 控制实现 / 测试迭代）', subjectsHint: '以 physics、chemistry、math、info-tech 为主，按需含其他', redlines: '覆盖原理→装置→实验→必要定量；定量计算节点≤20%' },
  'scientific-inquiry': { label: '科学探究/实验', moduleWord: '探究环节（问题假设 / 变量设计 / 数据采集 / 分析结论）', subjectsHint: 'physics、chemistry、biology、science、math 为主', redlines: '必须含实验设计与数据分析类节点；理论与实验并重' },
  'consumer-decision': { label: '消费决策/方案对比', moduleWord: '决策环节（需求调研 / 技术原理对比 / 成本测算 / 决策报告）', subjectsHint: '根据对象自然选科：涉及机械/能源用 physics+math，涉及材料/化学品用 chemistry+math，辅以 geography/chinese', redlines: '交付物是决策报告/对比表；必须含与对象相关的技术原理节点（≥2）；禁止工业研发节点' },
  'social-inquiry': { label: '社会调查/田野研究', moduleWord: '调查环节（选题抽样 / 资料收集 / 整理统计 / 结论报告）', subjectsHint: 'chinese、geography、history、math（统计）按需组合', redlines: '核心是调查方法、数据统计与报告写作；不要硬塞物理化学公式' },
  'humanities-literary': { label: '人文/文学/语言', moduleWord: '创作环节（立意选材 / 阅读积累 / 结构表达 / 修改展示）', subjectsHint: 'chinese、english、history 为主', redlines: '围绕阅读、写作、表达、文化理解；不要塞理科公式或工程装置节点' },
  'creative-media': { label: '创意设计/媒体/艺术', moduleWord: '创作环节（创意构思 / 设计草案 / 制作实现 / 展示评议）', subjectsHint: '结合 info-tech、chinese 及相关学科', redlines: '围绕创意表达与制作；只在确需技术实现时引入理科节点' },
  'business-economics': { label: '商业/创业/经济实践', moduleWord: '运营环节（需求调研 / 方案设计 / 成本定价 / 运营复盘）', subjectsHint: 'math（统计/比例/函数）、chinese（策划/表达）为主', redlines: '围绕调研、测算、方案与表达' },
  'life-planning': { label: '生活规划/活动策划', moduleWord: '策划环节（需求目标 / 方案日程 / 预算分工 / 执行复盘）', subjectsHint: 'math（预算/时间/统计）、chinese（策划/通知/总结）、geography（路线）按需', redlines: '围绕目标、方案、预算分工与执行复盘' },
  'health-life': { label: '健康生活/运动安全', moduleWord: '健康环节（现状调查 / 科学原理与生理机制 / 预防干预原理 / 方案制定 / 实践评估）', subjectsHint: 'biology、physics、chemistry、science（原理机制必选≥2）、math（统计监测）、chinese（宣传倡议）', redlines: '必须覆盖科学原理层（生理机制+物理/化学原理），不能只有"调查统计"和"行为公约"两头；理/化/生原理节点≥2' },
  'planting-cultivation': { label: '种植养殖/园艺栽培', moduleWord: '环节（植物识别分类 / 生长与环境 / 栽培实操 / 观察记录 / 种植日记）', subjectsHint: 'science、biology 为主线，辅以 math（数据图表）、chinese（日记）', redlines: '交付物是种植观察日记；必须含生长原理与栽培步骤' },
  'labor-practice': { label: '劳动实践/制作', moduleWord: '实践环节（认识准备 / 操作实践 / 观察记录 / 成果分享）', subjectsHint: 'biology、science、chinese、math 按需', redlines: '围绕动手操作、观察记录与成果分享' },
  'maker-workshop': { label: '工坊/木作/建筑模型', moduleWord: '工序（现场调研 / 风格方案 / 材料BOM / 搭建装饰 / 验收展示）', subjectsHint: 'science、physics、math、history、chinese 按需', redlines: '交付物是实体模型+图册+BOM；须有尺寸、工具、照片、检查表' },
  'industry-innovation': { label: '产业创新/新兴经济探究', moduleWord: '环节（产业背景与政策 / 应用场景调研 / 技术原理支撑 / 数据可行性 / 创新方案报告）', subjectsHint: 'geography、chinese、math、physics、history、info-tech 按需', redlines: '交付物是主题产业创新方案/调研报告；禁止与主题无关的模块' },
  'exhibition-redesign': { label: '展陈空间/场馆改造', moduleWord: '环节（现状诊断 / 主题策划 / 展陈设计 / 实施整改 / 开放验收）', subjectsHint: 'science（科普内容）、chinese（说明/讲解）、math（预算/统计）、info-tech 按需', redlines: '交付物是场馆改造方案册+展陈设计图；禁止程序设计、工程原型等无关节点' },
  'general': { label: '综合实践', moduleWord: '项目模块（须按题目自定义，禁止套用通用模块名）', subjectsHint: '按交付物自然选取所需学科', redlines: '每个节点都要服务于题目交付物' },
};

function projectTypeProfile(goal) {
  return TYPE_PROFILES[classifyProjectType(goal)] || TYPE_PROFILES.general;
}

function typeGuardrailBlock(goal) {
  const p = projectTypeProfile(goal);
  return `\n## 本项目类型识别：${p.label}\n- 模块视角：${p.moduleWord}\n- 学科取向：${p.subjectsHint}\n- 类型红线：${p.redlines}\n`;
}

// ============================================================
// 三、主题锚定（泛化版 — 不再为特定题目硬编码 preset）
// ============================================================

/** 从目标句提取核心对象（动词后的名词短语） */
function parseGoalSubject(goal) {
  const g = String(goal || '').trim();
  let subject = g;
  const m = g.match(/^(?:设计|制作|开发|建造|完成|策划|撰写|探究|调查|分析|探寻|探索|研究|调研|重塑|改造|优化|重建|更新|升级|整治|组织|开展|修复|翻新)(?:一个|一款|一份|一组|一次)?\s*(.+)$/);
  if (m) subject = m[1].trim();
  subject = subject.replace(/^(?:关于|围绕|有关)\s*/, '').replace(/[，。；].*$/, '').slice(0, 36);
  return subject || g.slice(0, 36);
}

function buildTopicKeywords(goal, subject) {
  const g = String(goal || '');
  const base = [subject];
  // 从 goal 中提取 2 字词元
  for (let i = 0; i < subject.length - 1; i++) {
    const w = subject.slice(i, i + 2);
    if (w.length === 2 && !/[的与及了在]$/.test(w)) base.push(w);
  }
  // 从 goal 全文补充关键词
  const extra = g.match(/[\u4e00-\u9fa5]{2,4}/g) || [];
  for (const w of extra.slice(0, 8)) {
    if (!base.includes(w) && !/^(设计|制作|开发|一个|关于|围绕|项目|方案|报告)$/.test(w)) base.push(w);
  }
  return [...new Set(base)].slice(0, 12);
}

function inferDeliverableHint(goal, subject, kind) {
  const g = String(goal || '');
  if (kind === 'exhibition-redesign') return `「${subject}」改造方案册（现状诊断+展陈设计+整改实施+验收）`;
  if (kind === 'industry-innovation') return `「${subject}」创新方案报告（场景调研+政策要点+可行性论证）`;
  if (kind === 'planting-cultivation') return `「${subject}」种植观察日记（分类笔记+栽培记录+生长数据+总结）`;
  if (/报告|调查|论文|倡议|方案/.test(g)) return `「${subject}」专题报告（含调研数据与可检查结论）`;
  if (/设计|制作|开发|建造/.test(g)) return `可展示的「${subject}」作品+过程记录+说明文档`;
  return `「${subject}」项目成果包（可展示交付物+过程记录+说明）`;
}

/** 主题锚定 — 泛化版：从 goal 提取核心主题，生成通用约束 */
function extractTopicProfile(goal) {
  const g = String(goal || '').trim();
  const subject = parseGoalSubject(g);
  const kind = classifyProjectType(g);
  const banCommon = ['原型驱动迭代', 'MVP', '快速原型', '递进式实施', '浸润式场景', '硬件准备', '环境搭建', '工程设计思维'];

  return {
    rawGoal: g,
    matched: true,
    coreTopic: subject,
    definition: `本项目必须围绕用户指定的「${subject}」展开，不得替换为其他主题或套用无关模板`,
    keywords: buildTopicKeywords(g, subject),
    banInSteps: banCommon,
    deliverableHint: inferDeliverableHint(g, subject, kind),
    kind,
  };
}

function formatTopicAnchorBlock(goal) {
  const t = extractTopicProfile(goal);
  return `\n## 本题核心主题（硬性锚点 — 不可替换、不可泛化）\n- 用户目标原文：「${t.rawGoal}」\n- **核心主题：${t.coreTopic}**\n- 主题定义：${t.definition}\n- projectSummary、deliverable、scheme 名称、每个 phase 的名称/steps/deliverable/knowledgeHints **必须直接出现核心主题关键词**\n- knowledgeHints 检索词须含：${t.keywords.join('、')}\n- 建议交付物：${t.deliverableHint}\n- **禁止** scheme 名使用通用模板名（递进式实施、原型驱动迭代等）；禁止交付物写「项目原型」「MVP」「系统演示」等与题目无关的表述\n- **禁止** steps 中出现：${(t.banInSteps || []).join('、')}\n`;
}

// ============================================================
// 四、通用模块（genericDomainsForType）— 统一 domain 来源
// ============================================================

function genericDomainsForType(id, goal = '') {
  const g = String(goal || '');
  if (/算力中心|数据中心|太空算力|云计算|边缘计算|计算中心|服务器集群|卫星计算|轨道计算/.test(g)) {
    return [
      { id: 'requirements', label: '需求与约束定义', keywords: ['算力', '任务负载', '轨道环境', '功耗', '散热', '通信链路', '辐射', '需求'], subjects: ['computer-science', 'engineering', 'physics'] },
      { id: 'architecture', label: '系统架构设计', keywords: ['系统架构', '计算节点', '电源', '热控', '通信', '冗余', '模块化', '接口'], subjects: ['computer-science', 'engineering'] },
      { id: 'operations', label: '调度与运行控制', keywords: ['任务调度', '遥测', '容错', '故障切换', '资源分配', '监控', '控制流程'], subjects: ['computer-science', 'engineering'] },
      { id: 'verification', label: '仿真测试与迭代', keywords: ['仿真', '指标', '延迟', '带宽', '能耗', '热平衡', '可靠性', '测试'], subjects: ['computer-science', 'engineering', 'physics'] },
    ];
  }
  const map = {
    'scientific-inquiry': [
      { id: 'question', label: '问题与假设', keywords: ['问题', '假设', '猜想', '现象', '原理'], subjects: ['science', 'physics', 'chemistry', 'biology'] },
      { id: 'design', label: '变量与实验设计', keywords: ['变量', '实验', '控制变量', '对照', '方案', '测量'], subjects: ['physics', 'chemistry', 'biology', 'science'] },
      { id: 'data', label: '数据采集与处理', keywords: ['数据', '测量', '记录', '统计', '误差', '图表'], subjects: ['math', 'info-tech', 'science'] },
      { id: 'conclusion', label: '分析与结论', keywords: ['分析', '结论', '解释', '规律', '报告'], subjects: ['science', 'math', 'chinese'] },
    ],
    'social-inquiry': [
      { id: 'topic', label: '选题与调查设计', keywords: ['选题', '调查', '问卷', '访谈', '抽样', '样本'], subjects: ['chinese', 'math'] },
      { id: 'collect', label: '资料与数据收集', keywords: ['资料', '数据', '收集', '记录', '文献', '实地'], subjects: ['geography', 'history', 'chinese'] },
      { id: 'analyze', label: '整理与统计分析', keywords: ['统计', '整理', '图表', '分析', '百分比', '平均数'], subjects: ['math'] },
      { id: 'report', label: '结论与报告', keywords: ['结论', '报告', '建议', '论证', '写作', '说明'], subjects: ['chinese'] },
    ],
    'humanities-literary': [
      { id: 'theme', label: '立意与选材', keywords: ['立意', '主题', '选材', '构思', '观点'], subjects: ['chinese', 'english'] },
      { id: 'read', label: '阅读与素材积累', keywords: ['阅读', '素材', '文本', '名著', '积累', '鉴赏'], subjects: ['chinese', 'english', 'history'] },
      { id: 'express', label: '结构与表达', keywords: ['结构', '表达', '修辞', '语言', '写作', '叙述'], subjects: ['chinese', 'english'] },
      { id: 'revise', label: '修改与展示', keywords: ['修改', '评议', '朗诵', '展示', '演讲', '发表'], subjects: ['chinese'] },
    ],
    'creative-media': [
      { id: 'idea', label: '创意构思', keywords: ['创意', '构思', '主题', '灵感', '受众'], subjects: ['chinese', 'info-tech'] },
      { id: 'design', label: '设计与草案', keywords: ['设计', '草图', '分镜', '排版', '色彩', '构图'], subjects: ['info-tech', 'chinese'] },
      { id: 'make', label: '制作与实现', keywords: ['制作', '剪辑', '绘制', '编辑', '工具', '技术'], subjects: ['info-tech'] },
      { id: 'show', label: '展示与评议', keywords: ['展示', '评议', '反馈', '发布', '优化'], subjects: ['chinese'] },
    ],
    'business-economics': [
      { id: 'research', label: '需求与市场调研', keywords: ['需求', '市场', '调研', '调查', '数据', '用户'], subjects: ['math', 'chinese'] },
      { id: 'plan', label: '方案与产品设计', keywords: ['方案', '产品', '设计', '策划', '创意'], subjects: ['chinese', 'info-tech'] },
      { id: 'cost', label: '成本与定价测算', keywords: ['成本', '定价', '利润', '预算', '函数', '百分比', '统计'], subjects: ['math'] },
      { id: 'operate', label: '运营与复盘', keywords: ['运营', '推广', '复盘', '反馈', '报告'], subjects: ['chinese', 'math'] },
    ],
    'life-planning': [
      { id: 'goal', label: '需求与目标', keywords: ['需求', '目标', '调查', '问卷', '场景', '人数'], subjects: ['chinese', 'math'] },
      { id: 'plan', label: '方案与日程', keywords: ['方案', '计划', '日程', '安排', '路线', '流程'], subjects: ['chinese', 'geography', 'math'] },
      { id: 'budget', label: '预算与分工', keywords: ['预算', '成本', '费用', '统计', '函数', '分工', '百分比'], subjects: ['math'] },
      { id: 'review', label: '执行与复盘', keywords: ['执行', '记录', '反馈', '复盘', '总结', '报告'], subjects: ['chinese'] },
    ],
    'health-life': [
      { id: 'status', label: '现状调查与数据', keywords: ['现状', '调查', '问卷', '统计', '数据', '测量', '记录', '比例', '图表'], subjects: ['math', 'biology', 'science'] },
      { id: 'mechanism', label: '科学原理与生理机制', keywords: ['原理', '机制', '结构', '成因', '凸透镜', '晶状体', '视网膜', '睫状肌', '光学', '成像', '折射', '消化', '吸收', '代谢', '循环', '呼吸', '细胞', '神经', '肌肉', '骨骼'], subjects: ['physics', 'biology', 'chemistry', 'science'] },
      { id: 'prevention', label: '预防/干预原理与方法', keywords: ['预防', '矫正', '凹透镜', '焦距', '屈光', '营养素', '膳食', '训练', '恢复', '保护', '防护', '干预', '治疗'], subjects: ['biology', 'physics', 'chemistry', 'science'] },
      { id: 'plan', label: '方案制定与宣传', keywords: ['计划', '方案', '目标', '公约', '标准', '倡议', '宣传', '海报', '说明文'], subjects: ['chinese', 'math'] },
      { id: 'assess', label: '实践记录与评估', keywords: ['记录', '评估', '对比', '反馈', '改进', '报告', '数据跟踪'], subjects: ['chinese', 'math', 'science'] },
    ],
    'planting-cultivation': [
      { id: 'taxonomy', label: '植物识别与分类', keywords: ['植物', '分类', '特征', '结构', '器官'], subjects: ['science', 'biology'] },
      { id: 'growth', label: '生长与环境', keywords: ['生长', '光合', '呼吸', '种子', '萌发', '环境'], subjects: ['science', 'biology'] },
      { id: 'cultivate', label: '栽培实操', keywords: ['种植', '栽培', '土壤', '浇水', '施肥', '养护'], subjects: ['science', 'biology'] },
      { id: 'observe', label: '观察记录', keywords: ['观察', '记录', '测量', '数据', '图表', '变化'], subjects: ['science', 'math', 'biology'] },
      { id: 'share', label: '种植日记', keywords: ['日记', '报告', '总结', '分享', '说明'], subjects: ['chinese'] },
    ],
    'labor-practice': [
      { id: 'prepare', label: '认识与准备', keywords: ['认识', '准备', '材料', '工具', '原理', '步骤'], subjects: ['science', 'biology', 'chinese'] },
      { id: 'practice', label: '操作实践', keywords: ['操作', '制作', '种植', '养护', '烹饪', '步骤'], subjects: ['science', 'biology'] },
      { id: 'record', label: '观察与记录', keywords: ['观察', '记录', '测量', '数据', '变化', '统计'], subjects: ['science', 'math', 'biology'] },
      { id: 'share', label: '成果与分享', keywords: ['成果', '分享', '展示', '总结', '报告', '改进'], subjects: ['chinese'] },
    ],
    'engineering': [
      { id: 'principle', label: '原理与需求', keywords: ['原理', '需求', '指标', '现象', '规律', '受力', '能量'], subjects: ['physics', 'science', 'chemistry'] },
      { id: 'structure', label: '结构与装置', keywords: ['结构', '装置', '材料', '设计', '搭建', '组装', '电路', '机械'], subjects: ['physics', 'engineering', 'science'] },
      { id: 'control', label: '控制与实现', keywords: ['控制', '传感', '编程', '算法', '电路', '反馈', '调试'], subjects: ['info-tech', 'physics', 'engineering'] },
      { id: 'test', label: '测试与迭代', keywords: ['测试', '实验', '测量', '数据', '误差', '记录', '优化'], subjects: ['math', 'physics', 'science'] },
    ],
    'consumer-decision': [
      { id: 'needs', label: '需求与场景调研', keywords: ['调查', '数据', '统计', '需求', '分析', '场景'], subjects: ['math', 'chinese'] },
      { id: 'tech_principle', label: '产品核心技术原理', keywords: ['效率', '能量转化', '功率', '电路', '材料', '结构', '传感'], subjects: ['physics', 'chemistry'] },
      { id: 'cost', label: '成本与数据建模', keywords: ['函数', '计算', '统计', '费用', '成本', '百分比', '预算'], subjects: ['math'] },
      { id: 'environment', label: '环保与可持续', keywords: ['环境', '污染', '排放', '资源', '可持续', '回收'], subjects: ['geography', 'chemistry'] },
      { id: 'decision', label: '决策论证与报告', keywords: ['说明', '报告', '论证', '分析', '比较', '建议'], subjects: ['chinese', 'math'] },
    ],
    'industry-innovation': [
      { id: 'background', label: '产业背景与政策', keywords: ['产业', '政策', '法规', '发展', '规划', '经济'], subjects: ['geography', 'history', 'chinese'] },
      { id: 'scenarios', label: '应用场景调研', keywords: ['场景', '需求', '应用', '调研', '数据', '用户'], subjects: ['geography', 'chinese', 'math'] },
      { id: 'tech', label: '技术原理支撑', keywords: ['技术', '原理', '通信', '动力', '安全', '系统'], subjects: ['physics', 'info-tech', 'science'] },
      { id: 'analysis', label: '数据与可行性分析', keywords: ['统计', '数据', '成本', '效益', '分析', '图表'], subjects: ['math', 'chinese'] },
      { id: 'proposal', label: '创新方案与报告', keywords: ['方案', '创新', '建议', '报告', '论证', '可行性'], subjects: ['chinese', 'geography'] },
    ],
    'exhibition-redesign': [
      { id: 'diagnose', label: '现状诊断', keywords: ['问题', '调查', '记录', '现状', '隐患'], subjects: ['chinese', 'math'] },
      { id: 'theme', label: '主题策划', keywords: ['主题', '科普', '内容', '策划', '定位'], subjects: ['science', 'chinese'] },
      { id: 'design', label: '展陈设计', keywords: ['布局', '动线', '展板', '设计', '模型', '互动'], subjects: ['info-tech', 'chinese', 'math'] },
      { id: 'implement', label: '实施整改', keywords: ['整改', '布置', '预算', '分工', '安全', '清单'], subjects: ['math', 'chinese'] },
      { id: 'launch', label: '开放验收', keywords: ['验收', '讲解', '宣传', '说明', '展示', '反馈'], subjects: ['chinese', 'science'] },
    ],
    'maker-workshop': [
      { id: 'survey', label: '现场调研', keywords: ['调研', '测量', '场地', '历史', '风格', '需求'], subjects: ['history', 'math', 'chinese'] },
      { id: 'design', label: '风格方案', keywords: ['设计', '风格', '结构', '草图', '比例', '方案'], subjects: ['math', 'science', 'chinese'] },
      { id: 'bom', label: '材料BOM', keywords: ['材料', '清单', '成本', '尺寸', '工具', '预算'], subjects: ['math', 'science'] },
      { id: 'build', label: '搭建制作', keywords: ['搭建', '制作', '工具', '步骤', '照片', '记录'], subjects: ['science', 'physics'] },
      { id: 'review', label: '验收展示', keywords: ['验收', '展示', '检查', '报告', '分享'], subjects: ['chinese'] },
    ],
    'general': [
      { id: 'define', label: '调研与定义', keywords: ['调研', '需求', '定义', '背景', '分析'], subjects: ['chinese', 'history', 'geography', 'math'] },
      { id: 'design', label: '方案设计', keywords: ['方案', '设计', '规划', '分工', '构思'], subjects: ['chinese', 'math', 'geography'] },
      { id: 'make', label: '实施与表达', keywords: ['实施', '制作', '执行', '记录', '表达'], subjects: ['chinese', 'math'] },
      { id: 'test', label: '总结与展示', keywords: ['总结', '评估', '展示', '报告', '反思'], subjects: ['chinese', 'math'] },
    ],
  };
  return map[id] || map.general;
}

/** 根据项目目标推断模块 — 统一走 genericDomainsForType */
function inferProjectDomains(goal) {
  return genericDomainsForType(classifyProjectType(goal), goal);
}

function formatDomainHints(domains) {
  if (!domains.length) return '';
  return domains.map((d, i) =>
    `${i + 1}. 【${d.label}】必覆盖。检索候选时请优先匹配名称/课标描述中含：${d.keywords.join('、')}；学科倾向：${(d.subjects || []).join('、')}`
  ).join('\n');
}

// ============================================================
// 五、反空话与红线
// ============================================================

const ANTI_VACUUM_BLOCK = `
### 反空话与反泛素养（硬性）
- **禁止** matched：批判性思维、创新思维、团队协作、项目管理、沟通能力、核心素养等综合素养类节点（除非题目明确要求）
- projectPhases 每阶段 steps 至少 2 条，每条 ≥15 字，须写清：动作 + 对象 + 方法/工具 + 检查标准；禁止「完成探究」「进行调研」「运用知识点」
- reason 除「模块：」外须写明**本阶段怎么用**（例：「模块：数据整理。用条形图对比两方案 5 年成本，附数据来源」）`;

// ============================================================
// 六、typeMatchHints — 泛化版（通用类型指导，不再硬编码具体节点名）
// ============================================================

function typeMatchHints(goal) {
  switch (classifyProjectType(goal)) {
    case 'consumer-decision':
      return `\n### 类型要求：消费决策（含技术原理理解）
- 交付物是决策报告/对比测算表
- **技术原理必选**（≥2 个 physics/chemistry 节点）：根据项目具体对象，选取与候选方案**核心技术差异**直接相关的原理节点（如动力原理、能量转换、电路功率、材料特性等）
- 其他优先：统计与函数、环境排放、说明文写作
- 禁止：与项目对象无关的工业研发节点（电解池、原电池等）、history 学科
- reason 须写明该知识点如何帮助理解候选方案的技术差异`;
    case 'engineering':
      return `\n### 类型要求：工程/制作
- **必含科学技术原理**（≥2 个 physics/chemistry/biology/science 节点）：解释项目核心装置/系统"为什么这样做能成功"的学科原理（选取与项目**驱动原理、感知机制、运动力学、材料特性、化学反应**直接相关的节点）
- **必含数学技能**（≥1 个 math 节点）：用于测量、统计、数据分析、计算验证
- matched 须覆盖项目的**核心技术子系统**（从 goal 中提取）
- 覆盖原理→装置→实验→必要定量；含至少 1 个装置/实验类节点
- 数学 index ≤25%；名称含「计算/求解/方程式」的 ≤20%
- 禁止选择与项目交付物**不同物理域**的节点（如地面项目不选航空、化学项目不选生物医疗）
- reason 须写明用于项目哪一子系统`;
    case 'scientific-inquiry':
      return `\n### 类型要求：科学探究
- **必含科学技术原理**（≥2 个 physics/chemistry/biology/science 节点）：与实验核心原理直接相关
- **必含数学技能**（≥1 个 math 节点）：用于数据分析、统计图表、测量计算
- 必含实验设计与数据分析类节点；理论与实验并重
- 根据探究对象选取相应学科：化学类选溶液/反应/滴定，物理类选力/热/电，生物类选生态/遗传/生理
- 禁止选与探究对象无关领域的节点`;
    case 'social-inquiry':
      return `\n### 类型要求：社会调查
- 围绕调查方法、数据统计与报告写作
- 优先：统计图表、调查方法、说明文/报告写作、地理/环境相关（如题目涉及）
- 可用：语文/地理/历史/数学，**不要塞理科公式**
- 禁止：与调查主题无关的理科实验节点、生命科学节点（除非题目明确涉及）
- reason 须写明用于调查哪一环节`;
    case 'humanities-literary':
      return `\n### 类型要求：人文/文学
- 围绕阅读、写作、表达、文化理解（语文/英语/历史）
- **不要塞理科或工程节点**`;
    case 'creative-media':
      return `\n### 类型要求：创意/媒体
- 围绕创意、设计、制作、展示；仅在确需技术实现时引入信息技术/数学`;
    case 'business-economics':
      return `\n### 类型要求：商业/经济
- 围绕调研、成本定价测算、方案与表达（数学/语文/信息技术）`;
    case 'life-planning':
      return `\n### 类型要求：生活规划/活动策划
- 围绕需求目标、方案日程、预算分工、执行复盘（数学/语文/地理）；不要塞工程装置或纯理科公式`;
    case 'health-life':
      return `\n### 类型要求：健康生活（含科学原理理解）
- **科学/技术原理必选**（≥2 个 biology/physics/chemistry/science 节点）：根据项目具体健康主题，选取与该健康问题**生理机制、物理/化学原理**直接相关的学科节点（如近视→凸透镜成像+眼球结构+睫状肌调节；营养→消化吸收+食物成分+化学变化；运动→力学+呼吸循环）
- **禁止只选"调查统计+行为公约"两头**——中间的科学原理层（为什么会近视？晶状体如何变形？凹透镜如何矫正？蓝光对视网膜的影响机制是什么？）必须覆盖
- 其他优先：数据统计图表、健康知识科普写作/宣传
- 禁止：与本健康主题无关的工程装置或纯计算节点
- reason 须写明该知识点如何帮助学生理解该健康问题的**科学本质**`;
    case 'planting-cultivation':
      return `\n### 类型要求：种植养殖/园艺栽培
- 交付物是**种植观察日记**
- matched **必须**覆盖：植物分类/特征、生长原理（光合/萌发/根系等）、栽培相关、数据记录
- 优先：植物生长相关科学/生物节点、统计图表、说明文/日记写作
- 禁止：与种植无关的工程装置、化学方程式、程序设计
- reason 须写明如何用于种植的具体环节`;
    case 'labor-practice':
      return `\n### 类型要求：劳动实践
- 围绕动手操作、观察记录、成果分享（科学/生物/语文/数学）；贴近真实操作，不要拔高成科研论文或工程系统`;
    case 'industry-innovation':
      return `\n### 类型要求：产业创新/新兴经济
- 交付物是**产业创新方案/调研报告**，不是装置制作或软件工程
- matched 须能支撑：产业背景政策、应用场景、技术原理（与产业领域相关）、数据统计、方案论证
- 优先：地理/经济/交通相关、统计调查、说明文/报告写作、与产业技术领域直接相关的物理/信息技术节点
- 禁止：与主题产业无关的模块
- reason 必须写明该知识点如何用于本产业的具体环节`;
    case 'exhibition-redesign':
      return `\n### 类型要求：展陈空间/场馆改造
- 交付物是**改造方案册**（现状诊断+展陈设计+整改清单）
- matched 须支撑：现状调查、科普内容（与展馆主题相关）、展板设计、预算统计、说明文写作
- 禁止：程序设计、工程装置研发等与展陈无关节点
- reason 必须写明如何用于改造的具体环节`;
    case 'maker-workshop':
      return `\n### 类型要求：工坊/木作/建筑模型
- 交付物是实体模型+图册+BOM
- steps 须有尺寸、工具、照片、检查表
- 禁止空话（「选择组件」「环境搭建」等）`;
    default:
      return `\n### 类型要求：综合实践
- 每个节点服务交付物某一步，学科按需自然选取
- 若题目抽象，先落地为 1 个可检查交付物，再选课标；禁止泛素养凑数${ANTI_VACUUM_BLOCK}`;
  }
}

// ============================================================
// 七、系统提示词 — Match 阶段
// ============================================================

function systemPromptMatch(complex, goal) {
  const base = `你是资深 PBL（项目式学习）导师，精通 K12 各学科课标，能为工程制作、科学探究、社会调查、人文创作、创意设计、商业实践、消费决策、产业创新等多类项目设计学习路径。
${formatTopicAnchorBlock(goal)}
${typeGuardrailBlock(goal)}
## 第一步（必做）：把项目拆成「子任务 / 模块」

在选任何候选 index 之前，先回答：「要做出本项目的交付物，学生必须分别解决哪几个**独立子问题**？」不同类型项目的模块不同：
- 工程/制作：原理 → 装置/结构 → 电路/控制 → 测试迭代
- 科学探究：问题假设 → 变量与实验设计 → 数据采集 → 分析结论
- 社会调查：选题抽样 → 资料/问卷收集 → 整理统计 → 结论报告
- 人文/写作：立意选材 → 阅读积累 → 结构表达 → 修改展示
- 创意/媒体：创意构思 → 设计草案 → 制作实现 → 展示评议
- 商业/经济：需求调研 → 方案设计 → 成本定价 → 运营复盘
- 消费决策：需求调研 → 对比维度 → 成本测算 → 决策报告

## 第二步：从候选列表选点（相关性门禁）

对每个 index，必须通过以下测试才能入选：
1. **模块测试**：它支撑上面哪一个模块？reason 必须以「模块：XXX」开头
2. **删除测试**：若删掉它，学生完成该模块会明显受阻吗？若不会 → 不选
3. **课标测试**：名称必须来自候选列表原文，禁止编造候选中没有的知识点

## 三层知识角色

- **foundation**：完成某模块所需的工具性/前置知识
- **bridge**：连接基础与产出的关键方法
- **core**：直接用于动手/产出环节的知识

## 最高优先级：贴合交付物 > 学科齐全

- 选 matched 的唯一标准：删掉它，项目某一步就做不下去
- **学科按项目类型自然选取**：工程/科学类多用理科；社会/人文/创作/商业类该用语文、历史、地理、英语、信息技术就大胆用——不要硬塞理科，也不要为凑跨学科塞无关节点
- 宁可精准 5-8 个，也不为学科齐全凑数

常见错误（绝对禁止）：
❌ matched 名称不在候选列表里（编造）
❌ 工程/制作类只堆「XX计算」「XX守恒定律」，缺原理/装置/实验（定量节点≤20%）
❌ 人文写作 / 社会调查 / 创意设计类硬塞物理化学公式或工程装置节点
❌ 为凑学科数量选与交付物无关的节点
❌ 用批判性思维/团队协作/项目管理等泛素养节点凑数
❌ projectPhases steps 只有「完成本阶段探究」「进行调研」等空话
${ANTI_VACUUM_BLOCK}`;

  if (!complex) {
    return `${base}

## 输出要求（常规项目）
- matched 8-${PBL_MAX_MATCHED_NORMAL} 个，foundation/bridge/core 均有，覆盖至少 2 个模块
- 每个 matched 的 reason 以「模块：」开头
- dependsOn 构成 DAG；pathOrder 满足依赖顺序
- projectPhases 3-5 阶段，每阶段 literacy 六维（知识/方法/能力/态度/情感/价值观）各 1 句，结合学科与项目类型，禁止套话
- knowledgeChain 用 → 串联模块递进

只返回 JSON，不要 markdown，不要解释。`;
  }

  return `${base}

## 输出要求（复杂项目）
- matched 5-10 个；覆盖至少 3 个模块，每个模块 1-2 个节点即可
- 节点不够时宁可少选，不要凑无关课标
- foundation 1-2、bridge 2-3、core 2-3
- knowledgeNames / techRoute 只能出现候选列表中存在的名称

只返回 JSON，不要 markdown，不要任何解释文字。`;
}

// ============================================================
// 八、系统提示词 — Decompose 阶段（泛化版，去掉特定 hint 函数）
// ============================================================

function systemPromptDecompose(complex, goal) {
  const p = projectTypeProfile(goal);
  const depth = complex
    ? '给出 2-3 套**不同实施路线**并推荐 1 套。'
    : '至少给出 2 套可行思路并推荐 1 套。';
  return `你是资深 PBL 与跨学科课程设计顾问，覆盖工程、科学探究、社会调查、人文创作、创意设计、商业实践、消费决策、产业创新等各类项目。
${formatTopicAnchorBlock(goal)}
## 任务（本阶段**不选课标知识点**）

对用户项目目标做**全链路结构化拆解**：
1. 判断项目类型（已初步识别：${p.label}）
2. 澄清交付物、约束、适用学段
3. 拆出 3-5 个模块（${p.moduleWord}）
4. ${depth}
5. 为推荐方案列出 4-5 个**实施阶段**（任务步骤、产出、knowledgeHints 检索词）

## 可执行任务步骤（硬性）
- 每个 phase 的 steps 至少 2 条，每条 ≥20 字，须同时包含：**动词 + 操作对象 + 工具/数据/方法 + 可检查产出（含数量/尺寸/次数）**
- 禁止空话：「进行调研」「完成探究」「选择硬件组件」「编写基础控制逻辑」「环境搭建」等无验收标准的表述
- **每条 steps 必须出现用户目标中的关键名词**（从【项目目标】原文提取）
- 若题目是口号/品牌/抽象表述，必须**落地为 1 个具体交付物**，steps 写清谁做什么、用什么表/工具、交什么稿

## 去重去冗余（硬性）
- **绝对禁止**同一意思换不同说法重复出现
- 不同 phase 的 steps 内容之间**零重叠**
- **steps 与 deliverable/验收项之间不得同义重复**：deliverable 写「产出物名+数量标准」（如"护眼公约 4 条+全班签字确认"），steps 写「达成该产出物的操作过程」（如"组织全班讨论用眼习惯调查结果，票选出 4 项可量化条款"）——禁止 steps 里直接搬运 deliverable 的验收描述
- **同一操作只出现一次**：若"走访点位"已出现在某 phase 的 steps 中，其他 phase 不得再出现同义表述（"调查走访""实地走访"等）
- summary / projectSummary / constraints / scopeLimits / successCriteria 各字段之间不得互相复制粘贴
- pros 每条 ≤15 字，禁止与 summary 重复

## 原则
- **严格贴合题目类型**：调查/对比类的交付物是报告/对比表，不是研发原型；写作/创作类的交付物是作品，不是实验装置
- knowledgeHints 是**检索关键词**，按项目类型选取（理工类用学科概念，人文/社科类用阅读/写作/统计/调查等），不写课标原文节点名
- deliverable 必须是可检查实物（报告、表格、海报、作品、数据记录表），不能是「提升素养」「增强能力」
- 不跑题、不硬凑学科

只返回 JSON，不要 markdown。`;
}

function userPromptDecompose(goal, complex) {
  const domains = inferProjectDomains(goal);
  const domainBlock = domains.length
    ? `\n【可参考的项目模块】\n${formatDomainHints(domains)}\n`
    : '';
  const topicBlock = formatTopicAnchorBlock(goal);
  return `【项目目标】
${goal}
${topicBlock}${domainBlock}
返回 JSON（严格遵循字段名）：
{
  "projectSummary": "一句话概括项目",
  "deliverable": "最终交付物",
  "constraints": ["时间/安全/器材等约束"],
  "scopeLimits": ["不能宣称的结论或能力边界，至少2条"],
  "successCriteria": ["可检查的验收标准，至少2条"],
  "subsystems": [
    {"id": "xxx", "name": "子系统名", "description": "该子系统要解决的问题"}
  ],
  "schemes": [
    {
      "id": "A",
      "name": "方案名称",
      "summary": "技术路线概述",
      "pros": ["优点"],
      "cons": ["局限"],
      "phases": [
        {
          "phase": "阶段名",
          "steps": ["任务1", "任务2"],
          "deliverable": "阶段产出",
          "subsystemIds": ["xxx"],
          "knowledgeHints": ["检索关键词1", "检索关键词2"]
        }
      ]
    }
  ],
  "recommendedSchemeId": "A",
  "knowledgeChain": "子系统1 → 子系统2 → 测试迭代"
}

要求：
- schemes 至少 2 套，recommendedSchemeId 必须是其中一套的 id
- 推荐方案 phases 4-5 个
- 每个 steps 条目 ≥20 字，须含可操作动词 + 数量/尺寸/次数 + 可检查产出；动词对象必须来自用户目标原文
- phases 的 phase 名称、deliverable、steps 须与【项目目标】同一领域，禁止跨域套模板
- knowledgeHints 每阶段 2-5 个，用于下一步课标检索，勿写课标原文节点名
- **去重**：不同 phase 的 steps、summary、pros、deliverable 之间不得有同义重复段落`;
}

function formatBlueprintForMatch(blueprint) {
  if (!blueprint) return '';
  const scheme = (blueprint.schemes || []).find(s => s.id === blueprint.recommendedSchemeId)
    || (blueprint.schemes || [])[0];
  if (!scheme) return '';
  const subs = (blueprint.subsystems || []).map(s => `${s.id}:${s.name}`).join('；');
  const phases = (scheme.phases || []).map((p, i) => {
    const hints = (p.knowledgeHints || []).join('、');
    const steps = (p.steps || []).join('；');
    return `  ${i + 1}. 【${p.phase}】任务：${steps}；产出：${p.deliverable || '阶段成果'}；知识检索提示：${hints}`;
  }).join('\n');
  const scope = (blueprint.scopeLimits || []).map(s => `  - ${s}`).join('\n');
  const success = (blueprint.successCriteria || []).map(s => `  - ${s}`).join('\n');
  return `
【项目实施蓝图 — matched 必须对齐此结构，禁止跑题】
项目摘要：${blueprint.projectSummary || ''}
交付物：${blueprint.deliverable || ''}
${scope ? `不能宣称：\n${scope}\n` : ''}${success ? `验收标准：\n${success}\n` : ''}推荐方案：${scheme.name}（${scheme.summary || ''}）
子系统：${subs}
实施阶段：
${phases}
知识链：${blueprint.knowledgeChain || ''}
`;
}

// ============================================================
// 九、系统提示词 — Filter 阶段
// ============================================================

function systemPromptFilter(complex, goal) {
  const p = projectTypeProfile(goal);
  const gradeHint = complex
    ? 'grades 一般落在 7-12；若项目明显面向小学，可含 1-6。'
    : '';
  return `你是 PBL 项目与课标对齐专家，能把工程、科学探究、社会调查、人文创作、创意设计、商业实践、消费决策、产业创新等各类项目拆解为可检索的学科与模块。
${formatTopicAnchorBlock(goal)}
${typeGuardrailBlock(goal)}
## 工作流程
1. 判断项目类型（已识别：${p.label}）
2. 列出 3-5 个模块（${p.moduleWord}）
3. 为每个模块映射学科：math / physics / chemistry / biology / science / chinese / english / history / geography / info-tech
4. 确定适用 grades 与 systems
5. 从蓝图任务动词推断 Bloom 认知上限（bloomCeiling 1-6）

## 选学科原则（按类型自适应）
- 学科必须能覆盖上述模块，**按项目类型自然选取**
- 工程/科学类：以 physics/chemistry/math/info-tech 为主
- 消费决策类：以 math（统计/函数）为主，辅以相关科普与说明文写作
- 社会调查/人文/创作类：以 chinese/geography/history/english/info-tech 为主，不强行加理科
- 不要为凑学科数量加入与交付物无关的学科

${gradeHint}

只返回 JSON。`;
}

function userPromptFilter(goal, summaryList, complex, projectBlueprint, bloomProfile = null) {
  const domains = inferProjectDomains(goal);
  const blueprintBlock = formatBlueprintForMatch(projectBlueprint);
  const domainBlock = domains.length
    ? `\n【本项目模块参考（filter 的 subjects 须能覆盖这些）】\n${formatDomainHints(domains)}\n`
    : '';
  const bloom = bloomProfile || inferBloomFromBlueprint(projectBlueprint);
  const bloomBlock = formatBloomHintForFilter(bloom);
  const gradeHint = complex
    ? `\n- grades 一般落在 7-12（初中、高中），除非项目面向小学`
    : '';
  return `PBL项目目标：${goal}
${formatTopicAnchorBlock(goal)}${blueprintBlock}${domainBlock}${bloomBlock}
可用的知识体系：
${summaryList}

返回 JSON：
{
  "subjects": ["math", "chinese", "geography"],
  "systems": ["cn", "ap"],
  "grades": [7, 8, 9],
  "projectDomains": ["从交付物拆出的 3-5 个模块名称"],
  "bloomCeiling": 3,
  "bloomEvidence": ["从蓝图 steps 提取的 2-4 条任务"],
  "actionVerbs": ["测量", "统计"],
  "reasoning": "说明各模块对应的学科与年级"
}

注意：
- subjects 取值：math/physics/chemistry/biology/chinese/english/history/geography/info-tech/science
- systems：cn/ap/cambridge/ib/us
- projectDomains：从项目交付物拆出的 3-5 个模块名称
- **学科按项目类型自然选取**，理工类用理科、社科人文创作类用文科/信息技术，不要硬塞无关学科
- 通常 2-5 个学科即可${gradeHint}`;
}

// ============================================================
// 十、Match 阶段 User Prompt（泛化版 — 统一格式示范）
// ============================================================

const FORMAT_EXAMPLE_COMPLEX = `
返回 JSON 格式（严格遵循；下列 index 仅为**格式示范**，你必须在【候选知识点】中重新检索并填写真实 index，禁止照抄示例数字）：
{
  "matched": [
    {"index": 2, "confidence": 0.93, "role": "foundation", "reason": "模块：XXX。建立基础概念与前置知识", "dependsOn": []},
    {"index": 5, "confidence": 0.91, "role": "bridge", "reason": "模块：YYY。连接基础与产出的关键方法/技能", "dependsOn": [2]},
    {"index": 8, "confidence": 0.90, "role": "core", "reason": "模块：ZZZ。直接用于动手/产出环节", "dependsOn": [5]}
  ],
  "pathOrder": [2, 5, 8],
  "knowledgeChain": "基础概念 → 方法/技能 → 产出应用",
  "projectPhases": [
    {
      "phase": "阶段名（须含项目关键词）",
      "steps": ["具体任务1（≥15字，含动词+对象+方法+检查标准）", "具体任务2"],
      "knowledgeNames": ["候选列表中存在的节点名称"],
      "deliverable": "阶段产出物",
      "literacy": {
        "knowledge": "理解XXX原理/概念",
        "method": "用YYY方法完成ZZZ",
        "ability": "能独立完成XXX操作",
        "attitude": "严谨/认真/负责的态度",
        "emotion": "对XXX产生好奇/成就感",
        "values": "树立YYY意识"
      }
    }
  ],
  "external": [
    {"name": "课标外知识点名称", "reason": "说明为何课标未覆盖但项目必需", "prerequisites": ["关联的 matched 知识点名称"]}
  ],
  "techRoute": "按模块串联的中文实施路线描述（500字内）"
}`;

const FORMAT_EXAMPLE_NORMAL = `
返回 JSON 格式（严格遵循）：
{
  "matched": [
    {"index": 3, "confidence": 0.95, "role": "foundation", "reason": "模块：XXX。建立变量与关系", "dependsOn": []},
    {"index": 8, "confidence": 0.90, "role": "bridge", "reason": "模块：YYY。连接基础与产出", "dependsOn": [3]}
  ],
  "pathOrder": [3, 8],
  "knowledgeChain": "基础概念 → 方法探究 → 产出实现",
  "projectPhases": [],
  "external": [
    {"name": "跨学科资料检索与引用", "reason": "整合多来源信息，课标较少系统讲授但项目落地必需"}
  ],
  "techRoute": "按模块递进实施"
}`;

function userPromptMatch(goal, candidateList, complex, maxMatched, minConf, domainHints, projectBlueprint, bloomProfile = null, archetypeId = null) {
  const matchedRange = complex ? `5-${Math.min(maxMatched, 8)}` : `8-${maxMatched}`;
  const externalMax = complex ? 2 : 3;
  const domains = domainHints && domainHints.length ? domainHints : inferProjectDomains(goal);
  const blueprintSection = formatBlueprintForMatch(projectBlueprint);
  const domainSection = domains.length
    ? `\n【项目模块 — 每个至少 1 个 matched，reason 必须以「模块：XXX」开头】\n${formatDomainHints(domains)}\n`
    : '';

  const example = complex ? FORMAT_EXAMPLE_COMPLEX : FORMAT_EXAMPLE_NORMAL;

  const bloom = bloomProfile || inferBloomFromBlueprint(projectBlueprint);
  const bloomBlock = formatBloomHintForMatch(bloom);
  const archetype = resolveArchetype(
    goal,
    classifyProjectType(goal),
    false,
    archetypeId
  );
  const archetypeBlock = formatArchetypeForMatch(archetype, projectBlueprint);
  const registryBlock = archetype ? formatRegistryForMatch(archetype.id) : '';

  return `【项目目标】
${goal}
${formatTopicAnchorBlock(goal)}${blueprintSection}${domainSection}${archetypeBlock}${bloomBlock}${registryBlock}
【候选知识点】（matched 只能选下列 index；**先对齐上方蓝图阶段与 knowledgeHints**，再按模块检索选 index）
${candidateList}

${example}

## 硬性要求

### 0. 贴合交付物（最高优先级）
- 每个 matched 的 reason **必须以「模块：」开头**
- **5-8 个精准节点**即可；不要为了学科齐全凑数
- **严禁**选与交付物无关的 index（编造、凑数、跑题）
- 学科按项目类型自然选取，理工类用理科、社科人文创作类用文科/信息技术
- **科学/工程/探究类项目必须同时含两类节点**：①科学技术原理（physics/chemistry/biology/science ≥2 个，解释"为什么能成功"）②数学技能（math ≥1 个，用于测量/统计/计算验证）
${typeMatchHints(goal)}

### 1. 数量与角色
- matched：${matchedRange} 个，confidence≥${minConf}
- ${complex ? 'foundation 1-2、bridge 2-3、core 2-3；避免与交付物无关的 index' : '覆盖至少 2 个模块'}

### 2. 知识链
- dependsOn 构成 DAG；pathOrder 满足依赖
- knowledgeChain 体现模块递进（按项目类型）

### 3. projectPhases
- ${complex ? '4-5' : '3-5'} 个阶段，按模块组织
- knowledgeNames **只能**使用候选列表中出现的名称（字面匹配或明显子串）
- 每阶段 literacy 六维各 1 句，结合学科与项目类型，禁止套话

### 4. 跨学科（可选，不强制）
- 围绕交付物自然跨学科即可；**禁止**为凑学科引入与项目无关的节点

### 5. external（课标外，硬性要求）
- **必须**输出 1-${externalMax} 个课标外知识点，不可为空数组
- 填写候选列表中**没有**、但完成本项目**确实需要**的专业/实践概念
- 每个 external 须有 name + reason；可选 prerequisites

### 6. techRoute
- 中文，500 字内，按模块串联，体现项目实施的递进逻辑`;
}

// ============================================================
// 十一、SUBJECT_ZH 与 buildPBMessages 主入口
// ============================================================

const SUBJECT_ZH = {
  math: '数学', physics: '物理', chemistry: '化学', biology: '生物',
  science: '科学', 'info-tech': '信息技术', chinese: '语文', english: '英语',
  history: '历史', geography: '地理',
  engineering: '工程', 'computer-science': '计算机科学',
};

/**
 * @param {'decompose'|'filter'|'match'} stage
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
    projectBlueprint = null,
    bloomProfile = null,
    archetypeId = null,
  } = payload;

  if (stage === 'decompose') {
    return [
      { role: 'system', content: systemPromptDecompose(complex, goal) },
      { role: 'user', content: userPromptDecompose(goal, complex) },
    ];
  }

  if (stage === 'filter') {
    const bloom = bloomProfile || inferBloomFromBlueprint(projectBlueprint);
    return [
      { role: 'system', content: systemPromptFilter(complex, goal) },
      { role: 'user', content: userPromptFilter(goal, summaryList, complex, projectBlueprint, bloom) },
    ];
  }

  if (stage === 'match') {
    const candidateList = (candidates || []).map((n, i) => {
      const gradeStr = n.gradeLabel || (n.grade ? `G${n.grade}` : '通识');
      const subj = SUBJECT_ZH[n.subject] || n.subject || '';
      const prereq = (n.prerequisiteNames || []).slice(0, 3).join('、') || '无';
      const def = String(n.definition || '').replace(/\s+/g, ' ').slice(0, 72);
      const defPart = def ? ` | ${def}` : '';
      return `[${i}] ${n.name} | ${gradeStr} | ${subj} | 先修:${prereq}${defPart}`;
    }).join('\n');

    const hints = domainHints && domainHints.length ? domainHints : inferProjectDomains(goal);
    const bloom = bloomProfile || inferBloomFromBlueprint(projectBlueprint);

    return [
      { role: 'system', content: systemPromptMatch(complex, goal) },
      {
        role: 'user',
        content: userPromptMatch(goal, candidateList, complex, maxMatched, minConf, hints, projectBlueprint, bloom, archetypeId),
      },
    ];
  }

  throw new Error(`Unknown PBL stage: ${stage}`);
}

export { inferProjectDomains };
