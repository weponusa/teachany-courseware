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
import {
  stripStructuredGoal,
  buildCompactUserContext,
  compactBlueprintHeader,
} from './pbl-context.js';
import {
  inferTopicKnowledgeAnchors,
  formatTopicAnchorHint,
} from './pbl-topic-anchors.js';

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
 * health-life / planting-cultivation / labor-practice / study-trip / life-planning /
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
  // 研学旅行/人文地理考察
  if (/研学|游学|研学旅行|研学路线|红色研学|文化研学|文化考察|实地考察|field.?trip|遗址|博物馆|人文史迹|古迹|古村|世界遗产/.test(g)) return 'study-trip';
  // 活动策划/生活规划
  if (/活动策划|策划.{0,6}(活动|晚会|联欢|运动会|典礼|节|比赛)|联欢会|晚会|文艺汇演|毕业典礼|生日会|出游|旅行|路线规划|时间管理|班级布置|嘉年华|游园/.test(g)) return 'life-planning';
  // 社会调查
  if (/田野|问卷|访谈|社区|民俗|传统文化|非遗|人口|城乡|社会现象|调研报告|居民|乡土|口述史|垃圾分类|垃圾治理|环保.*调查|城市|发展史|对比|比较|典型|区域|案例/.test(g)) return 'social-inquiry';
  // 产业创新
  if (/低空经济|通航产业|新兴产业|产业创新/.test(g) || (/探寻|探索|研究|调研/.test(g) && /创新|产业|经济|行业/.test(g))) return 'industry-innovation';
  // 工坊/木作
  if (/工坊|鲁班|榫卯|古典.*风格|木结构|建筑模型|微缩|传统建筑|斗拱|飞檐/.test(g)) return 'maker-workshop';
  // 能源收益测算（数据分析报告，非硬件制作）
  if (/光伏|太阳能发电|屋顶.*光伏|发电潜力|发电收益|碳减排/.test(g)
    && /测算|估算|调查|分析|收益|减排|用电|日照|潜力|效益/.test(g)
    && !/接线|原型|传感器|水泵|搭建|制作|组装|烧录|GPIO/.test(g)) return 'energy-analysis';
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

/** 学科不限于项目类型；由题目延展思考后在 filter/match 阶段选取 */
const OPEN_SUBJECTS_HINT = '按题目与交付物延展思考后自然选取，可跨各学科；禁为凑学科引入无关节点';

const TYPE_PROFILES = {
  'engineering': { label: '工程研发/制作', moduleWord: '工程子系统（原理 / 装置结构 / 控制实现 / 测试迭代）', subjectsHint: OPEN_SUBJECTS_HINT, redlines: '覆盖原理→装置→实验→必要定量；定量计算节点≤20%' },
  'scientific-inquiry': { label: '科学探究/实验', moduleWord: '探究环节（问题假设 / 变量设计 / 数据采集 / 分析结论）', subjectsHint: OPEN_SUBJECTS_HINT, redlines: '必须含实验设计与数据分析类节点；理论与实验并重' },
  'consumer-decision': { label: '消费决策/方案对比', moduleWord: '决策环节（需求调研 / 技术原理对比 / 成本测算 / 决策报告）', subjectsHint: OPEN_SUBJECTS_HINT, redlines: '交付物是决策报告/对比表；须含与对象相关的原理/测算节点；禁止工业研发节点' },
  'social-inquiry': { label: '社会调查/田野研究', moduleWord: '调查环节（选题抽样 / 资料收集 / 整理统计 / 结论报告）', subjectsHint: OPEN_SUBJECTS_HINT, redlines: '核心是调查方法、数据统计与报告写作；节点须服务交付物' },
  'humanities-literary': { label: '人文/文学/语言', moduleWord: '创作环节（立意选材 / 阅读积累 / 结构表达 / 修改展示）', subjectsHint: OPEN_SUBJECTS_HINT, redlines: '围绕阅读、写作、表达、文化理解；题目涉及时可自然引入相关学科' },
  'creative-media': { label: '创意设计/媒体/艺术', moduleWord: '创作环节（创意构思 / 设计草案 / 制作实现 / 展示评议）', subjectsHint: OPEN_SUBJECTS_HINT, redlines: '围绕创意表达与制作；按实现需要自然引入相关学科' },
  'business-economics': { label: '商业/创业/经济实践', moduleWord: '运营环节（需求调研 / 方案设计 / 成本定价 / 运营复盘）', subjectsHint: OPEN_SUBJECTS_HINT, redlines: '围绕调研、测算、方案与表达' },
  'study-trip': { label: '研学旅行/人文地理考察', moduleWord: '研学环节（目的地调研 / 人文史迹 / 路线预算 / 研学报告）', subjectsHint: OPEN_SUBJECTS_HINT, redlines: '围绕目的地、史迹、路线预算与研学报告；题目提及史地则优先匹配，但不限学科' },
  'life-planning': { label: '生活规划/活动策划', moduleWord: '策划环节（需求目标 / 方案日程 / 预算分工 / 执行复盘）', subjectsHint: OPEN_SUBJECTS_HINT, redlines: '围绕目标、方案、预算分工与执行复盘' },
  'health-life': { label: '健康生活/运动安全', moduleWord: '健康环节（现状调查 / 科学原理与生理机制 / 预防干预原理 / 方案制定 / 实践评估）', subjectsHint: OPEN_SUBJECTS_HINT, redlines: '须覆盖与主题相关的科学原理层，不能只有调查统计与行为公约' },
  'planting-cultivation': { label: '种植养殖/园艺栽培', moduleWord: '环节（植物识别分类 / 生长与环境 / 栽培实操 / 观察记录 / 种植日记）', subjectsHint: OPEN_SUBJECTS_HINT, redlines: '交付物是种植观察日记；须含生长原理与栽培步骤' },
  'labor-practice': { label: '劳动实践/制作', moduleWord: '实践环节（认识准备 / 操作实践 / 观察记录 / 成果分享）', subjectsHint: OPEN_SUBJECTS_HINT, redlines: '围绕动手操作、观察记录与成果分享' },
  'maker-workshop': { label: '工坊/木作/建筑模型', moduleWord: '工序（现场调研 / 风格方案 / 材料BOM / 搭建装饰 / 验收展示）', subjectsHint: OPEN_SUBJECTS_HINT, redlines: '交付物是实体模型+图册+BOM；须有尺寸、工具、照片、检查表' },
  'industry-innovation': { label: '产业创新/新兴经济探究', moduleWord: '环节（产业背景与政策 / 应用场景调研 / 技术原理支撑 / 数据可行性 / 创新方案报告）', subjectsHint: OPEN_SUBJECTS_HINT, redlines: '交付物是主题产业创新方案/调研报告；禁止与主题无关的模块' },
  'exhibition-redesign': { label: '展陈空间/场馆改造', moduleWord: '环节（现状诊断 / 主题策划 / 展陈设计 / 实施整改 / 开放验收）', subjectsHint: OPEN_SUBJECTS_HINT, redlines: '交付物是场馆改造方案册+展陈设计图；禁止与展陈无关的节点' },
  'energy-analysis': { label: '能源/环境数据测算', moduleWord: '环节（资源调查 / 数据采集 / 模型测算 / 效益分析 / 方案论证）', subjectsHint: '物理、数学、地理/科学、语文（报告）；禁止生物学', redlines: '交付物是测算表+分析图表+论证报告；禁止接线/原型/硬件工程步骤；禁止细胞/细胞膜/细胞呼吸/光合作用等生物学节点（能量指物理电能非细胞代谢）' },
  'general': { label: '综合实践', moduleWord: '项目模块（须按题目自定义，禁止套用通用模块名）', subjectsHint: OPEN_SUBJECTS_HINT, redlines: '每个节点都要服务于题目交付物' },
};

function projectTypeProfile(goal) {
  return TYPE_PROFILES[classifyProjectType(goal)] || TYPE_PROFILES.general;
}

function typeGuardrailBlock(goal) {
  const p = projectTypeProfile(goal);
  return `类型：${p.label}｜模块：${p.moduleWord}｜学科：${p.subjectsHint}｜红线：${p.redlines}`;
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
  const anchors = inferTopicKnowledgeAnchors(g);
  (anchors.recallTerms || []).slice(0, 12).forEach(t => base.push(t));
  return [...new Set(base)].slice(0, 20);
}

function inferDeliverableHint(goal, subject, kind) {
  const g = String(goal || '');
  if (kind === 'exhibition-redesign') return `「${subject}」改造方案册（现状诊断+展陈设计+整改实施+验收）`;
  if (kind === 'industry-innovation') return `「${subject}」创新方案报告（场景调研+政策要点+可行性论证）`;
  if (kind === 'planting-cultivation') return `「${subject}」种植观察日记（分类笔记+栽培记录+生长数据+总结）`;
  if (kind === 'study-trip') return `「${subject}」研学方案册（区域地理调研+人文史迹记录+路线预算+安全预案+研学报告）`;
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
  const anchorHint = formatTopicAnchorHint(goal);
  const anchorPart = anchorHint ? `｜${anchorHint}` : '';
  return `锚点：「${t.coreTopic}」｜检索词：${t.keywords.slice(0, 10).join('、')}｜交付参考：${t.deliverableHint}${anchorPart}｜禁套模板/MVP/环境搭建`;
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
      { id: 'topic', label: '选题与调查设计', keywords: ['选题', '调查', '问卷', '访谈', '抽样', '样本', '维度', '指标'], subjects: ['chinese', 'math'] },
      { id: 'collect', label: '资料与数据收集', keywords: ['资料', '数据', '收集', '记录', '文献', '实地', '史料', '案例'], subjects: ['geography', 'history', 'chinese'] },
      { id: 'analyze', label: '整理与统计分析', keywords: ['统计', '整理', '图表', '分析', '百分比', '平均数', '对比'], subjects: ['math'] },
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
    'study-trip': [
      { id: 'destination', label: '目的地调研', keywords: ['目的地', '调研', '区域', '地图', '地形', '气候', '资源', '区位', '交通', '地理'], subjects: ['geography', 'history'] },
      { id: 'heritage', label: '人文史迹', keywords: ['历史', '文物', '遗址', '博物馆', '革命', '朝代', '遗产', '人文', '古迹', '文化'], subjects: ['history', 'chinese'] },
      { id: 'route', label: '路线预算', keywords: ['路线', '日程', '行程', '预算', '费用', '统计', '成本', '分工', '安全'], subjects: ['math', 'geography', 'chinese'] },
      { id: 'report', label: '研学报告', keywords: ['报告', '总结', '记录', '说明', '展示', '复盘', '观察', '日记'], subjects: ['chinese', 'history', 'geography'] },
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
    'energy-analysis': [
      { id: 'resource', label: '资源调查', keywords: ['光伏', '太阳能', '日照', '辐射', '光电', '电功率', '能量守恒', '电能', '电路'], subjects: ['physics', 'science'] },
      { id: 'electricity', label: '数据采集', keywords: ['用电', '电量', '电费', '调查', '数据', '统计', '屋顶', '面积'], subjects: ['math', 'science'] },
      { id: 'calc', label: '模型测算', keywords: ['函数', '计算', '收益', '成本', '百分比', '统计', '估算', '发电'], subjects: ['math'] },
      { id: 'carbon', label: '效益分析', keywords: ['碳', '排放', '减排', '环境', '对比', '可持续'], subjects: ['geography', 'science'] },
      { id: 'report', label: '方案论证', keywords: ['说明', '报告', '论证', '建议', '图表'], subjects: ['chinese', 'math'] },
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
    `${i + 1}. 【${d.label}】必覆盖。检索候选时请优先匹配名称/课标描述中含：${d.keywords.join('、')}；模块参考学科（非限制）：${(d.subjects || []).join('、') || '不限'}`
  ).join('\n');
}

// ============================================================
// 五、反空话与红线
// ============================================================

const ANTI_VACUUM_BLOCK = `禁泛素养节点；steps≥2条且≥20字含动作+对象+方法+可验收产出（数量/尺寸/次数）；reason以「模块：」开头并写明怎么用`;

const DECOMPOSE_DEPTH_BLOCK = `## 拆解深度（硬性，违反则视为无效输出）
- projectSummary：40-80字，须写清「谁+用什么方法+做出什么交付物+解决什么问题」，禁止「按模块推进」「可检查验收」等套话
- scopeLimits≥2条、successCriteria≥2条、constraints≥2条：须可检查，禁止「注意安全」「认真完成」
- 每套 scheme 的 summary 必须与 projectSummary 不同，写技术/实施路线差异
- phases 4-5个，阶段名用模块参考中的 label，禁止「基础准备」「实施阶段」等泛名
- 每 phase：steps≥2条且互不重复；deliverable 是具体表/图/报告名（≤20字），不是「阶段成果」「方案」
- steps 须嵌入题目中的具体对象/专名/指标，且含可验收要素（数量/次数/表格/图表/数据来源之一）
- steps 示范格式：「统计近3个月用电量并制成折线图，标注数据来源与异常值处理方式」
- knowledgeHints 是检索词（2-5个/阶段），不是课标节点名
- 禁止空泛步骤：「查阅资料并分析」「开展调查研究」「完成本阶段任务」「撰写研究报告初稿」`;

// ============================================================
// 六、typeMatchHints — 泛化版（通用类型指导，不再硬编码具体节点名）
// ============================================================

function typeMatchHints(goal) {
  const hints = {
    'consumer-decision': '消费决策：覆盖调研/原理/成本/决策报告；禁无关工业研发',
    engineering: '工程：原理+装置/实验+必要定量；节点服务交付物',
    'scientific-inquiry': '探究：实验设计+数据采集+分析结论',
    'social-inquiry': '调查：问卷/统计/报告写作；可按题目跨学科',
    'humanities-literary': '人文：阅读写作表达；可按题目跨学科',
    'creative-media': '创意：设计制作展示；按实现需要选节点',
    'business-economics': '商业：调研+成本定价+方案表达',
    'study-trip': '研学：目的地+史迹+路线预算+报告；按题目自然选科',
    'life-planning': '策划：日程预算分工复盘',
    'health-life': '健康：原理+调查+方案+评估；禁只调查不原理',
    'planting-cultivation': '种植：生长原理+栽培+观察记录',
    'labor-practice': '劳动：操作+记录+分享',
    'industry-innovation': '产业：政策场景+技术+数据+方案报告',
    'exhibition-redesign': '展陈：诊断+科普+设计+预算',
    'maker-workshop': '工坊：模型+BOM+尺寸工具验收',
  };
  const id = classifyProjectType(goal);
  return hints[id] ? `\n${hints[id]}` : `\n综合实践：节点服务交付物；${ANTI_VACUUM_BLOCK}`;
}

// ============================================================
// 七、系统提示词 — Match 阶段
// ============================================================

function systemPromptMatch(complex, goal) {
  const base = `PBL 课标路径编排。${formatTopicAnchorBlock(goal)}｜${typeGuardrailBlock(goal)}

选点门禁：①reason以「模块：」开头 ②删掉会卡住该模块才选 ③名称须来自候选列表。
角色：foundation/bridge/core。标准：贴合交付物>凑学科；精准5-8个。
禁：编造节点、泛素养、空话steps、跑题凑数。${ANTI_VACUUM_BLOCK}`;

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
  const depth = complex ? '2-3套路线并推荐1套' : '≥2套路线并推荐1套';
  return `PBL 全链路拆解（本阶段不选课标）。${formatTopicAnchorBlock(goal)}｜${typeGuardrailBlock(goal)}

${DECOMPOSE_DEPTH_BLOCK}

输出：交付物+约束+scopeLimits+successCriteria+subsystems+${depth}+推荐方案 phases（steps/deliverable/knowledgeHints）。
${ANTI_VACUUM_BLOCK}
禁复述：phase/deliverable/steps/scheme名禁止出现【学科】【任务】或粘贴全文goal。
去重：各phase steps零重叠；steps≠deliverable同义复述；summary/pros/cons/约束字段互不复制。
只返回JSON，不要markdown。`;
}

function decomposeQualityExtra(goal) {
  const subject = parseGoalSubject(goal);
  return `

【通用拆解验收 · 硬性】
- 所有 steps/deliverable 须出现题目核心对象「${subject}」或其关键专名，不得写成与题目无关的通用流程
- 最终 deliverable 须为可命名产物（XX表/XX图/XX报告/XX模型），禁「阶段成果」「研究报告初稿」「方案」
- 研究/调查/对比类：至少 2 个阶段 steps 含数字、条数、样本量或表格/图表名称
- 步骤类型须与项目类型红线一致，禁止套用工程/智慧城市/原型迭代套话（除非题目明确要求）`;
}

function userPromptDecompose(goal, complex) {
  const task = stripStructuredGoal(goal);
  const domains = inferProjectDomains(goal);
  const domainBlock = domains.length
    ? `\n模块参考：${domains.map(d => d.label).join('、')}`
    : '';
  return `${task}${domainBlock}${decomposeQualityExtra(goal)}

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

要求：schemes≥2；phases 4-5；knowledgeHints每阶段2-5个；各字段去重不复述。
阶段 steps 每条须含：动词+操作对象+工具/数据来源+可验收产出（含数量/次数/尺寸之一）。`;
}

function formatBlueprintForMatch(blueprint) {
  const header = compactBlueprintHeader(blueprint);
  return header ? `\n蓝图：${header}\n` : '';
}

// ============================================================
// 九、系统提示词 — Filter 阶段
// ============================================================

function systemPromptFilter(complex, goal) {
  const p = projectTypeProfile(goal);
  const gradeHint = complex ? 'grades通常7-12，小学项目可含1-6。' : '';
  return `PBL 课标筛选。${formatTopicAnchorBlock(goal)}｜${typeGuardrailBlock(goal)}

输出 subjects/systems/grades/projectDomains/bloomCeiling；根据题目地点/时代/主题延展思考后选取学科（可跨全科，不限项目类型），如「英国研学」须含英国地理与世界/欧洲史相关检索方向。subjects 可留空[]表示不限。${gradeHint} 只返回JSON。`;
}

function userPromptFilter(goal, summaryList, complex, projectBlueprint, bloomProfile = null) {
  const domains = inferProjectDomains(goal);
  const blueprintBlock = formatBlueprintForMatch(projectBlueprint);
  const domainBlock = domains.length
    ? `\n模块：${domains.map(d => d.label).join('、')}`
    : '';
  const bloom = bloomProfile || inferBloomFromBlueprint(projectBlueprint);
  const bloomBlock = formatBloomHintForFilter(bloom);
  const gradeHint = complex ? '；grades通常7-12' : '';
  const ctx = buildCompactUserContext({ goal, projectBlueprint, includeBlueprint: false });
  return `${ctx}${blueprintBlock}${domainBlock}${bloomBlock}
课标体系：${summaryList}

返回 JSON：
{
  "subjects": [],
  "systems": ["cn", "ap"],
  "grades": [7, 8, 9],
  "projectDomains": ["从交付物拆出的 3-5 个模块名称"],
  "bloomCeiling": 3,
  "bloomEvidence": ["从蓝图 steps 提取的 2-4 条任务"],
  "actionVerbs": ["测量", "统计"],
  "reasoning": "说明各模块对应的学科与年级"
}

subjects取值math/physics/chemistry/biology/chinese/english/history/geography/info-tech/science；按题目需要填写2-5科，无需限制时可返回[]；systems为cn/ap/cambridge/ib/us${gradeHint}`;
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
    ? `\n模块：${domains.map(d => d.label).join('、')}（每模块≥1 matched）\n`
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

  const ctx = buildCompactUserContext({ goal, projectBlueprint });
  return `${ctx}${blueprintSection}${domainSection}${archetypeBlock}${bloomBlock}${registryBlock}
候选（matched仅选下列index，先对齐蓝图阶段）：
${candidateList}
${example}

要求：reason以「模块：」开头；matched ${matchedRange}个、conf≥${minConf}；理工类原理≥2+数学≥1；external 1-${externalMax}个；techRoute≤500字。${typeMatchHints(goal)}`;
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

export { inferProjectDomains, projectTypeProfile };
