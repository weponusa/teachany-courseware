#!/usr/bin/env node
/**
 * 生成 G11 下学期学期覆盖包 g11-spring-pack.json
 * 8 个子 PBL · 110 节点划分 · mandatory + certified
 */
import { readFileSync, writeFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dir = dirname(fileURLToPath(import.meta.url));
const root = join(__dir, '..');

const SUBJECT_LABELS = {
  chinese: '语文', math: '数学', science: '科学', english: '英语',
  politics: '道法', 'info-tech': '信息科技', psychology: '心理',
  physics: '物理', chemistry: '化学', biology: '生物',
  history: '历史', geography: '地理', cs: '计算机',
};

const PROJECT_DEFS = [
  {
    id: 'g11-sp-p1',
    title: '算法与计算基础',
    themeAngle: 'AI 系统如何计算：从程序到复杂度',
    drivingQuestion: '推荐算法为什么必须可解释其计算步骤？',
    weeks: 2,
    prioritySubjects: ['cs', 'info-tech'],
  },
  {
    id: 'g11-sp-p2',
    title: '数据、概率与证据',
    themeAngle: '用数据说话：偏见检测与统计推断',
    drivingQuestion: '怎样用样本数据判断 AI 是否存在偏见？',
    weeks: 2,
    prioritySubjects: ['math', 'english'],
  },
  {
    id: 'g11-sp-p3',
    title: '隐私、安全与治理',
    themeAngle: '数字时代的权利、风险与规则',
    drivingQuestion: '收集用户数据时应遵守哪些隐私底线？',
    weeks: 2,
    prioritySubjects: ['politics', 'psychology', 'chinese'],
  },
  {
    id: 'g11-sp-p4',
    title: '生命系统与 AI 医学',
    themeAngle: '生物调控与智能医疗伦理边界',
    drivingQuestion: 'AI 辅助诊断在哪些方面不能替代医生？',
    weeks: 2,
    prioritySubjects: ['biology'],
  },
  {
    id: 'g11-sp-p5',
    title: '化学平衡与风险材料',
    themeAngle: '材料、反应与科技产品的风险沟通',
    drivingQuestion: '化工类 AI 应用如何向公众说明风险？',
    weeks: 2,
    prioritySubjects: ['chemistry'],
  },
  {
    id: 'g11-sp-p6',
    title: '物理世界与智能感知',
    themeAngle: '传感、运动与智能系统物理基础',
    drivingQuestion: '自动驾驶的传感器误差会带来哪些伦理问题？',
    weeks: 2,
    prioritySubjects: ['physics'],
  },
  {
    id: 'g11-sp-p7',
    title: '空间模型与数学结构',
    themeAngle: '几何、向量与 AI 可视化建模',
    drivingQuestion: '如何用数学模型描述 AI 决策边界？',
    weeks: 2,
    prioritySubjects: ['math', 'geography'],
  },
  {
    id: 'g11-sp-p8',
    title: '历史叙事与伦理 capstone',
    themeAngle: '技术革命史与当代 AI 伦理综合答辩',
    drivingQuestion: '历史上有哪些技术伦理教训可指导 AI 治理？',
    weeks: 3,
    prioritySubjects: ['history', 'chinese', 'english'],
  },
];

const TARGET_PER_PROJECT = 14;
const M_RATIO = 0.45;

const curriculum = JSON.parse(readFileSync(join(root, 'data/k12-pbl-curriculum.json'), 'utf8'));
const nodesMeta = JSON.parse(readFileSync(join(root, 'data/cn-k12-nodes.json'), 'utf8'));
const nodeIndex = new Map(nodesMeta.nodes.map((n) => [n.id, n]));

const pool = curriculum.projects
  .find((p) => p.id === 'g11-spring')
  .knowledgePoints.all.map((k) => ({ ...nodeIndex.get(k.id), level: k.level }));

const buckets = PROJECT_DEFS.map((d) => ({ ...d, nodes: [] }));

function smallestBucket() {
  return buckets.reduce((a, b) => (a.nodes.length <= b.nodes.length ? a : b));
}

function assignToBucket(node, bucketId) {
  const b = buckets.find((x) => x.id === bucketId);
  if (b && b.nodes.length < TARGET_PER_PROJECT + 2) b.nodes.push(node);
}

// 1) priority subjects to matching projects
const unassigned = [];
pool.forEach((node) => {
  const targets = buckets.filter((b) => b.prioritySubjects.includes(node.subject) && b.nodes.length < TARGET_PER_PROJECT);
  if (targets.length) {
    targets.sort((a, b) => a.nodes.length - b.nodes.length)[0].nodes.push(node);
  } else {
    unassigned.push(node);
  }
});

// 2) round-robin remainder
unassigned.forEach((node) => {
  const b = smallestBucket();
  if (b.nodes.length < TARGET_PER_PROJECT + 1) b.nodes.push(node);
});

// 3) balance counts
let guard = 0;
while (guard++ < 500) {
  const max = buckets.reduce((a, b) => (a.nodes.length > b.nodes.length ? a : b));
  const min = buckets.reduce((a, b) => (a.nodes.length < b.nodes.length ? a : b));
  if (max.nodes.length - min.nodes.length <= 1) break;
  if (max.nodes.length === 0) break;
  min.nodes.push(max.nodes.pop());
}

function enrichNode(n, masteryLevel) {
  return {
    id: n.id,
    name: n.name,
    subject: n.subject,
    subjectLabel: SUBJECT_LABELS[n.subject] || n.subject,
    grade: n.grade,
    catalogLevel: n.level,
    masteryLevel,
  };
}

const projects = buckets.map((b) => {
  const sorted = [...b.nodes];
  const mCount = Math.max(4, Math.round(sorted.length * M_RATIO));
  const mandatory = sorted.slice(0, mCount).map((n) => enrichNode(n, 'M'));
  const certified = sorted.slice(mCount).map((n) => enrichNode(n, 'C'));
  const allIds = sorted.map((n) => n.id);
  return {
    id: b.id,
    title: b.title,
    themeAngle: b.themeAngle,
    drivingQuestion: b.drivingQuestion,
    weeks: b.weeks,
    projectMode: 'cross-disciplinary',
    teachanySubject: 'cross',
    duration: `${b.weeks} 周`,
    completionGate: {
      rule: 'mandatory-all-M-or-C-certified',
      description: 'mandatory 节点全部达 M 或 C 方可进入下一子项目',
    },
    mandatoryNodeIds: mandatory.map((n) => n.id),
    certifiedNodeIds: certified.map((n) => n.id),
    knowledgePoints: { mandatory, certified, allIds },
    stats: {
      total: sorted.length,
      mandatory: mandatory.length,
      certified: certified.length,
    },
    weeklyRhythm: [
      { week: 1, focus: '驱动问 + 拆解', tasks: ['改写驱动问', 'TeachAny 拆解', '核对 mandatory 清单'] },
      { week: b.weeks, focus: b.weeks === 3 ? '整合 + 答辩' : '产出 + 检核', tasks: ['产出证据', 'micro-block 过关', '台账写入'] },
    ],
    deliverable: `${b.title} · 检核报告 + 节点过关单`,
  };
});

const allAssigned = new Set(projects.flatMap((p) => p.knowledgePoints.allIds));
const poolIds = new Set(pool.map((n) => n.id));
const missing = [...poolIds].filter((id) => !allAssigned.has(id));
const extra = [...allAssigned].filter((id) => !poolIds.has(id));

if (missing.length) {
  const b = smallestBucket();
  missing.forEach((id) => {
    const n = nodeIndex.get(id);
    if (n) {
      b.certifiedNodeIds.push(id);
      b.knowledgePoints.certified.push(enrichNode(n, 'C'));
      b.knowledgePoints.allIds.push(id);
      b.stats.total += 1;
      b.stats.certified += 1;
    }
  });
}

const pack = {
  $schema: '../pbl-semester-pack.schema.json',
  version: '1.0.0',
  model: 'semester-coverage-pack',
  id: 'g11-spring-pack',
  title: '11 年级 · 下学期 · 科技伦理覆盖包',
  grade: 11,
  gradeBand: 'senior',
  semester: 'spring',
  themeChain: '科技伦理',
  tagline: '8 个高强度 PBL · 人人必做 · 节点划分无交叠 · 个人台账关门',
  schoolYear: '2030-2031',
  nodePoolSize: pool.length,
  projectCount: projects.length,
  totalWeeks: projects.reduce((s, p) => s + p.weeks, 0),
  partitionRule: 'disjoint-union-equals-semester-pool',
  completionRule: {
    student: '完成全部 8 子项目且 personalLedger.gapCount === 0',
    project: 'mandatoryNodeIds 全部 M 或 C',
    semester: '∪ mandatoryNodeIds = nodePool',
  },
  themeShell: {
    title: '科技伦理',
    duration: `${projects.reduce((s, p) => s + p.weeks, 0)} 周 PBL 核心时段 + 1 周总检核`,
    constraints: [
      '本学期 8 个子 PBL 人人必做，顺序可按校历微调',
      '驱动问可个性化，每子项目 mandatory 节点清单不变',
      'M = 产出证据掌握；C = 项目内 micro-block + 短测',
      '无分科补课时段：gap 在包内补测闭环',
    ],
    competencies: ['伦理推理', '数据素养', '证据论证', '跨学科整合', '数字公民'],
  },
  personalLedgerSchema: {
    nodeStates: ['gap', 'C', 'M'],
    fields: ['studentId', 'nodeId', 'state', 'projectId', 'evidenceRef', 'assessedAt'],
  },
  projects,
  summary: {
    assignedNodes: projects.reduce((s, p) => s + p.stats.total, 0),
    mandatoryTotal: projects.reduce((s, p) => s + p.stats.mandatory, 0),
    certifiedTotal: projects.reduce((s, p) => s + p.stats.certified, 0),
    missingFromPool: missing.length,
    extraNodes: extra.length,
  },
  generatedAt: new Date().toISOString(),
};

writeFileSync(join(root, 'data/plans/g11-spring-pack.json'), JSON.stringify(pack, null, 2), 'utf8');
console.log('Wrote g11-spring-pack.json');
console.log('Projects:', projects.length);
projects.forEach((p) => console.log(`  ${p.id}: ${p.stats.total} nodes (${p.stats.mandatory}M + ${p.stats.certified}C)`));
console.log('Total assigned:', pack.summary.assignedNodes);
