#!/usr/bin/env node
/**
 * 生成 K12 学期覆盖包（多 PBL · 人人全覆盖）
 * 输出：
 *   data/k12-pbl-curriculum.json
 *   data/plans/{semester-id}-pack.json  × 24
 *   data/plans/k12-full-roadmap.json
 *   data/plans/primary-6year-roadmap.json
 *   docs/K12-PBL-CURRICULUM.md
 */
import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import {
  SUBJECT_LABELS,
  gradeBand,
  buildSemesterPack,
} from './lib/semester-pack-builder.mjs';

const __dir = dirname(fileURLToPath(import.meta.url));
const root = join(__dir, '..');
const plansDir = join(root, 'data/plans');

const PRIMARY_GAP_PATTERNS = [
  /^chn-e-(initials|simple-vowels|nasal-vowels|syllable|tone|pinyin)/,
  /stroke|笔顺|写字姿势/,
];

function subjectsForGrade(grade) {
  if (grade <= 6) return ['chinese', 'math', 'science', 'english', 'politics', 'info-tech', 'psychology'];
  if (grade <= 9) return ['chinese', 'math', 'english', 'physics', 'chemistry', 'biology', 'history', 'geography', 'politics', 'info-tech', 'psychology'];
  return ['chinese', 'math', 'english', 'physics', 'chemistry', 'biology', 'history', 'geography', 'politics', 'info-tech', 'psychology', 'cs'];
}

function isGapCandidate(node) {
  const name = node.name || '';
  const id = node.id || '';
  if (node.grade === 1 && node.subject === 'chinese' && /韵母|声母|拼音|声调|拼读/.test(name)) return true;
  if (PRIMARY_GAP_PATTERNS.some((re) => re.test(id) || re.test(name))) return true;
  if (node.subject === 'english' && /字母|音标|phonics|alphabet/i.test(name + id)) return true;
  return false;
}

const SEMESTERS = [
  { id: 'g1-autumn', grade: 1, semester: 'autumn', themeTitle: '我们的家', drivingQuestion: '我的家里藏着哪些有趣的秘密？' },
  { id: 'g1-spring', grade: 1, semester: 'spring', themeTitle: '我们的班级', drivingQuestion: '什么规则能让每个人都感到安全？' },
  { id: 'g2-autumn', grade: 2, semester: 'autumn', themeTitle: '我们的校园', drivingQuestion: '校园里哪种东西的数量最多？' },
  { id: 'g2-spring', grade: 2, semester: 'spring', themeTitle: '绿色星球', drivingQuestion: '哪些废品可以变成有用的东西？' },
  { id: 'g3-autumn', grade: 3, semester: 'autumn', themeTitle: '我们的校园', drivingQuestion: '我最想改善校园的哪一点？', planRef: 'g3-our-campus', planRefSubIndex: 0 },
  { id: 'g3-spring', grade: 3, semester: 'spring', themeTitle: '家乡的味道', drivingQuestion: '家乡哪种味道最能代表我们？' },
  { id: 'g4-autumn', grade: 4, semester: 'autumn', themeTitle: '绿色星球', drivingQuestion: '一周天气变化有什么规律？' },
  { id: 'g4-spring', grade: 4, semester: 'spring', themeTitle: '家乡的味道', drivingQuestion: '怎样搭配更均衡的午餐？' },
  { id: 'g5-autumn', grade: 5, semester: 'autumn', themeTitle: '绿色星球', drivingQuestion: '附近河水适合养鱼吗？屋顶能发多少电？' },
  { id: 'g5-spring', grade: 5, semester: 'spring', themeTitle: '社区小管家', drivingQuestion: '居民最需要哪种设施？', planRef: 'g5-community-map', planRefSubIndex: 1 },
  { id: 'g6-autumn', grade: 6, semester: 'autumn', themeTitle: '我们的校园', drivingQuestion: '哪些校园数据值得被看见？' },
  { id: 'g6-spring', grade: 6, semester: 'spring', themeTitle: '社区小管家', drivingQuestion: '我向社区提什么建议最有效？' },
  { id: 'g7-autumn', grade: 7, semester: 'autumn', themeTitle: '走进中学', drivingQuestion: '怎样让新环境更快成为「我们的学校」？' },
  { id: 'g7-spring', grade: 7, semester: 'spring', themeTitle: '身边的科学', drivingQuestion: '教学楼哪里最吵、最亮、最暖？' },
  { id: 'g8-autumn', grade: 8, semester: 'autumn', themeTitle: '健康与生活', drivingQuestion: '我们班怎样吃动更科学？' },
  { id: 'g8-spring', grade: 8, semester: 'spring', themeTitle: '物质与变化', drivingQuestion: '厨房里的变化哪些是化学变化？' },
  { id: 'g9-autumn', grade: 9, semester: 'autumn', themeTitle: '可持续发展', drivingQuestion: '家乡能源结构如何更绿色？' },
  { id: 'g9-spring', grade: 9, semester: 'spring', themeTitle: '社会议题', drivingQuestion: '青少年应如何参与公共决策？' },
  { id: 'g10-autumn', grade: 10, semester: 'autumn', themeTitle: '科学探究', drivingQuestion: '怎样用最少材料承受最大载荷？' },
  { id: 'g10-spring', grade: 10, semester: 'spring', themeTitle: '数据世界', drivingQuestion: '数据能揭示哪些隐藏规律？' },
  { id: 'g11-autumn', grade: 11, semester: 'autumn', themeTitle: '系统思维', drivingQuestion: '一个社会系统如何被建模与预测？' },
  { id: 'g11-spring', grade: 11, semester: 'spring', themeTitle: '科技伦理', drivingQuestion: 'AI 应用应遵守哪些伦理底线？' },
  { id: 'g12-autumn', grade: 12, semester: 'autumn', themeTitle: '升学衔接', drivingQuestion: '我的研究问题如何跨学科回答？' },
  { id: 'g12-spring', grade: 12, semester: 'spring', themeTitle: '未来公民', drivingQuestion: '我能为社区/世界贡献什么解决方案？' },
];

const nodesData = JSON.parse(readFileSync(join(root, 'data/cn-k12-nodes.json'), 'utf8'));
const allNodes = nodesData.nodes.filter((n) => n.grade >= 1 && n.grade <= 12);
const nodeIndex = new Map(allNodes.map((n) => [n.id, n]));

const byGradeSubject = {};
allNodes.forEach((n) => {
  const k = `${n.grade}|${n.subject}`;
  if (!byGradeSubject[k]) byGradeSubject[k] = [];
  byGradeSubject[k].push(n);
});

const assignment = new Map();
const gapReasons = new Map();
allNodes.filter(isGapCandidate).forEach((n) => {
  gapReasons.set(n.id, '技能操练：暂保留极薄层（逐步迁入 micro-block）');
});

function pickNodes(grade, count, semesterId) {
  const picked = [];
  const subjects = subjectsForGrade(grade);
  let si = 0;
  let attempts = 0;
  while (picked.length < count && attempts < subjects.length * 25) {
    const sub = subjects[si % subjects.length];
    const pool = (byGradeSubject[`${grade}|${sub}`] || []).filter(
      (n) => !assignment.has(n.id) && !gapReasons.has(n.id),
    );
    if (pool.length) {
      const node = pool.shift();
      assignment.set(node.id, { semesterId, packLevel: 'pool' });
      picked.push({ ...node, level: 'pool' });
    }
    si += 1;
    attempts += 1;
  }
  return picked;
}

function pickAdjacent(grade, count, semesterId) {
  const picked = [];
  for (const off of [1, -1, 2, -2]) {
    if (picked.length >= count) break;
    const g = grade + off;
    if (g < 1 || g > 12) continue;
    picked.push(...pickNodes(g, count - picked.length, semesterId));
  }
  return picked;
}

const semesterPools = new Map();
SEMESTERS.forEach((sem) => {
  const gradeNodes = allNodes.filter((n) => n.grade === sem.grade && !gapReasons.has(n.id));
  const perSem = Math.ceil(gradeNodes.length / 2);
  let pool = pickNodes(sem.grade, perSem, sem.id);
  if (pool.length < perSem) pool.push(...pickAdjacent(sem.grade, perSem - pool.length, sem.id));
  semesterPools.set(sem.id, pool);
});

allNodes.forEach((n) => {
  if (!assignment.has(n.id) && !gapReasons.has(n.id)) {
    gapReasons.set(n.id, '未划入任何学期包（需教研补 pack 或并入相邻学期）');
  }
});

const semesterPacks = SEMESTERS.map((sem) => {
  const pool = semesterPools.get(sem.id) || [];
  const planRefByIndex = {};
  if (sem.planRef != null && sem.planRefSubIndex != null) {
    planRefByIndex[sem.planRefSubIndex] = sem.planRef;
  }
  const pack = buildSemesterPack(sem, pool, { planRefByIndex });
  pack.generatedAt = new Date().toISOString();
  return pack;
});

mkdirSync(plansDir, { recursive: true });
semesterPacks.forEach((pack) => {
  writeFileSync(join(plansDir, `${pack.id}.json`), JSON.stringify(pack, null, 2), 'utf8');
});

// 兼容：g11-spring-pack 别名
const g11 = semesterPacks.find((p) => p.semesterId === 'g11-spring');
if (g11) {
  writeFileSync(join(plansDir, 'g11-spring-pack.json'), JSON.stringify(g11, null, 2), 'utf8');
}

function packCatalogEntry(pack) {
  return {
    id: pack.id,
    semesterId: pack.semesterId,
    grade: pack.grade,
    gradeBand: pack.gradeBand,
    gradeBandLabel: pack.gradeBandLabel,
    semester: pack.semester,
    label: pack.title,
    themeChain: pack.themeChain,
    drivingQuestion: pack.themeShell?.featuredDrivingQuestion,
    projectCount: pack.projectCount,
    nodePoolSize: pack.nodePoolSize,
    totalWeeks: pack.totalWeeks,
    packUrl: `pack.html?id=${pack.id}`,
    projects: pack.projects.map((p) => ({
      id: p.id,
      title: p.title,
      weeks: p.weeks,
      planRef: p.planRef,
      stats: p.stats,
      mandatoryNodeIds: p.mandatoryNodeIds,
      certifiedNodeIds: p.certifiedNodeIds,
    })),
  };
}

let touched = 0;
assignment.forEach(() => { touched += 1; });
const finalStats = {
  touched,
  gap: gapReasons.size,
  touchRate: Math.round((touched / allNodes.length) * 1000) / 10,
  totalSubProjects: semesterPacks.reduce((s, p) => s + p.projectCount, 0),
};

const expectedCoverageMatrix = {};
allNodes.forEach((n) => {
  const a = assignment.get(n.id);
  if (a) {
    expectedCoverageMatrix[n.id] = { [`${a.semesterId}-pack`]: 'pool' };
  } else {
    expectedCoverageMatrix[n.id] = { gap: true, reason: gapReasons.get(n.id) || 'gap' };
  }
});

const curriculum = {
  version: '2.0.0',
  model: 'semester-coverage-pack',
  title: 'K12 PBL 课程材料 · 学期覆盖包索引',
  description: '每学期 = 1 覆盖包 = K 个高强度 PBL；节点无交叠；学生个人台账 gap=0 过关',
  generatedAt: new Date().toISOString(),
  nodeInventory: {
    total: allNodes.length,
    byGradeBand: nodesData.byGradeBand,
    excludedSubjects: nodesData.excludedSubjects,
  },
  summary: {
    semesterPacks: semesterPacks.length,
    totalSubProjects: finalStats.totalSubProjects,
    ...finalStats,
    feasibility: finalStats.touchRate >= 90 ? '可行' : '需调整划分',
  },
  semesterPacks: semesterPacks.map(packCatalogEntry),
};

writeFileSync(join(root, 'data/k12-pbl-curriculum.json'), JSON.stringify(curriculum, null, 2), 'utf8');

writeFileSync(join(plansDir, 'k12-full-roadmap.json'), JSON.stringify({
  ...curriculum,
  title: 'K12 全周期覆盖推演',
  expectedCoverageMatrix,
  gapNodes: [...gapReasons.entries()].map(([nodeId, reason]) => {
    const n = nodeIndex.get(nodeId);
    return { nodeId, nodeName: n?.name, subject: n?.subject, grade: n?.grade, reason };
  }),
}, null, 2), 'utf8');

const primaryNodes = allNodes.filter((n) => n.grade <= 6);
const primaryInv = { byGrade: {}, bySubject: {} };
primaryNodes.forEach((n) => {
  primaryInv.byGrade[n.grade] = (primaryInv.byGrade[n.grade] || 0) + 1;
  primaryInv.bySubject[n.subject] = (primaryInv.bySubject[n.subject] || 0) + 1;
});

const primaryPacks = semesterPacks.filter((p) => p.grade <= 6);
const touchedPrimary = new Set();
const mandatoryPrimary = new Set();
const certifiedPrimary = new Set();

function packNodeIds(pack) {
  const ids = [];
  pack.projects.forEach((proj) => {
    ids.push(...(proj.mandatoryNodeIds || []), ...(proj.certifiedNodeIds || []));
  });
  return ids;
}

const primarySemesters = primaryPacks.map((pack) => {
  const semMeta = SEMESTERS.find((s) => s.id === pack.semesterId);
  const newIds = packNodeIds(pack);
  const newMandatory = pack.projects.reduce((s, p) => s + p.stats.mandatory, 0);
  const newCertified = pack.projects.reduce((s, p) => s + p.stats.certified, 0);
  newIds.forEach((id) => touchedPrimary.add(id));
  pack.projects.forEach((p) => {
    (p.mandatoryNodeIds || []).forEach((id) => mandatoryPrimary.add(id));
    (p.certifiedNodeIds || []).forEach((id) => certifiedPrimary.add(id));
  });
  const gapCount = primaryNodes.filter((n) => !touchedPrimary.has(n.id) || gapReasons.has(n.id)).length;
  const planRefProj = pack.projects.find((p) => p.planRef);
  return {
    id: pack.semesterId,
    label: pack.title.replace(/覆盖包$/, '').trim(),
    themeTitle: pack.themeChain,
    drivingQuestion: pack.themeShell?.featuredDrivingQuestion,
    projectCount: pack.projectCount,
    nodePoolSize: pack.nodePoolSize,
    totalWeeks: pack.totalWeeks,
    packUrl: `pack.html?id=${pack.id}`,
    planRef: planRefProj?.planRef || semMeta?.planRef || null,
    projects: pack.projects.map((p) => ({
      id: p.id, title: p.title, weeks: p.weeks, planRef: p.planRef, stats: p.stats,
    })),
    coverage: {
      newNodesThisSemester: newIds.length,
      mandatory: newMandatory,
      certified: newCertified,
    },
    cumulative: {
      touched: touchedPrimary.size,
      mandatory: mandatoryPrimary.size,
      certified: certifiedPrimary.size,
      gap: gapCount,
      touchRate: Math.round((touchedPrimary.size / primaryNodes.length) * 1000) / 10,
      mandatoryRate: Math.round((mandatoryPrimary.size / primaryNodes.length) * 1000) / 10,
    },
  };
});

const primaryGapNodes = [...gapReasons.entries()]
  .filter(([nodeId]) => {
    const n = nodeIndex.get(nodeId);
    return n && n.grade <= 6;
  })
  .map(([nodeId, reason]) => {
    const n = nodeIndex.get(nodeId);
    return { nodeId, nodeName: n?.name, subject: n?.subject, grade: n?.grade, reason };
  });

const primaryTouched = primaryNodes.filter((n) => touchedPrimary.has(n.id)).length;
const primaryGap = primaryNodes.length - primaryTouched + primaryGapNodes.filter((g) => touchedPrimary.has(g.nodeId)).length;
// simpler: gap = nodes not in touchedPrimary OR in gapReasons among primary
const primaryGapFinal = primaryNodes.filter((n) => !touchedPrimary.has(n.id) || gapReasons.has(n.id)).length;

writeFileSync(join(plansDir, 'primary-6year-roadmap.json'), JSON.stringify({
  version: '2.0.0',
  model: 'semester-coverage-pack',
  title: '小学 6 年 PBL 覆盖推演',
  projectMode: 'multi-pbl-per-semester',
  modelMeta: {
    totalPrimaryNodes: primaryNodes.length,
    semesterPacks: primaryPacks.length,
    subProjects: primaryPacks.reduce((s, p) => s + p.projectCount, 0),
    rule: '每学期 K 个子 PBL · 节点无交叠 · 个人台账 gap=0',
  },
  nodeInventory: primaryInv,
  semesters: primarySemesters,
  gapNodes: primaryGapNodes,
  summary: {
    after6Years: {
      mandatory: mandatoryPrimary.size,
      certified: certifiedPrimary.size,
      touched: touchedPrimary.size,
      gap: primaryGapFinal,
      touchRate: Math.round((touchedPrimary.size / primaryNodes.length) * 1000) / 10,
      mandatoryRate: Math.round((mandatoryPrimary.size / primaryNodes.length) * 1000) / 10,
      feasibility: touchedPrimary.size / primaryNodes.length >= 0.9 ? '可行' : '需调整',
      mathCheck: `${primaryPacks.length} 学期包 · ${primaryPacks.reduce((s, p) => s + p.projectCount, 0)} 子 PBL · 池 ${primaryPacks.reduce((s, p) => s + p.nodePoolSize, 0)} 节点 ≥ ${primaryNodes.length} 课标`,
    },
  },
  generatedAt: new Date().toISOString(),
}, null, 2), 'utf8');

function mdEscape(s) {
  return String(s).replace(/\|/g, '\\|');
}

let md = `# K12 PBL 课程材料 · 学期覆盖包

> 模型 v2.0 · ${new Date().toISOString().slice(0, 10)}  
> **每学期 = 1 覆盖包 = K 个子 PBL** · 人人必做 · 个人台账 gap=0  
> 课标 ${allNodes.length} 节点 · ${semesterPacks.length} 学期包 · ${finalStats.totalSubProjects} 子项目 · 触达率 ${finalStats.touchRate}%

## 规则

- **M**：产出掌握（mandatory） · **C**：micro-block 过关（certified）
- 子项目节点**无交叠**；并集 = 本学期节点池
- 无分科补课；逐步撤分科，gap 在包内补测
- 交互目录：\`catalog.html\` · 单包：\`pack.html?id={pack-id}\`

---

`;

semesterPacks.forEach((pack) => {
  md += `## ${pack.title}\n\n`;
  md += `- **节点池**：${pack.nodePoolSize} · **子项目**：${pack.projectCount} · **周数**：${pack.totalWeeks}+\n`;
  md += `- **驱动问**：${pack.themeShell?.featuredDrivingQuestion}\n`;
  md += `- **打开**：[pack.html?id=${pack.id}](../pack.html?id=${pack.id})\n\n`;
  md += `| # | 子 PBL | 周 | M | C | 节点 |\n|---|--------|---:|---:|---:|---:|\n`;
  pack.projects.forEach((p, i) => {
    md += `| ${i + 1} | ${mdEscape(p.title)} | ${p.weeks} | ${p.stats.mandatory} | ${p.stats.certified} | ${p.stats.total} |\n`;
  });
  md += `\n---\n\n`;
});

writeFileSync(join(root, 'docs/K12-PBL-CURRICULUM.md'), md, 'utf8');

console.log('Wrote k12-pbl-curriculum.json v2');
console.log('Wrote', semesterPacks.length, 'pack files to data/plans/');
console.log('Sub-projects:', finalStats.totalSubProjects);
console.log('Touch rate:', finalStats.touchRate + '%');
