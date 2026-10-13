#!/usr/bin/env node
/**
 * 生成小学 6 年 × 12 学期跨学科 PBL 覆盖推演
 * 输出 data/plans/primary-6year-roadmap.json
 */
import { readFileSync, writeFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dir = dirname(fileURLToPath(import.meta.url));
const root = join(__dir, '..');
const nodesData = JSON.parse(readFileSync(join(root, 'data/cn-k12-nodes.json'), 'utf8'));
const archetypes = JSON.parse(readFileSync(join(root, 'data/pbl-primary-archetypes.json'), 'utf8'));

const SUBJECT_LABELS = {
  chinese: '语文', math: '数学', science: '科学', english: '英语',
  politics: '道法', 'info-tech': '信息科技', psychology: '心理',
};

const CORE_PER_SEMESTER = 10;
const MENTION_PER_SEMESTER = 14;

/** 常规课保留：低段拼音/笔顺等不适合作为 PBL 核心 */
const GAP_PATTERNS = [
  /^chn-e-(initials|simple-vowels|nasal-vowels|syllable|tone|pinyin)/,
  /stroke|笔顺|写字姿势/,
];

function isGapCandidate(node) {
  const name = node.name || '';
  const id = node.id || '';
  if (node.grade === 1 && node.subject === 'chinese' && /韵母|声母|拼音|声调|拼读/.test(name)) return true;
  if (GAP_PATTERNS.some((re) => re.test(id) || re.test(name))) return true;
  return false;
}

const SEMESTERS = [
  { id: 'g1-autumn', grade: 1, semester: 'autumn', themeId: 'our-family', themeTitle: '我们的家', projectTitle: '我家的小世界', drivingQuestion: '我的家里藏着哪些有趣的秘密？' },
  { id: 'g1-spring', grade: 1, semester: 'spring', themeId: 'our-class', themeTitle: '我们的班级', projectTitle: '班级公约诞生记', drivingQuestion: '什么规则能让每个人都感到安全？' },
  { id: 'g2-autumn', grade: 2, semester: 'autumn', themeId: 'our-campus', themeTitle: '我们的校园', projectTitle: '数一数我的校园', drivingQuestion: '校园里哪种东西的数量最多？' },
  { id: 'g2-spring', grade: 2, semester: 'spring', themeId: 'green-planet', themeTitle: '绿色星球', projectTitle: '变废为宝创意展', drivingQuestion: '哪些废品可以变成有用的东西？' },
  { id: 'g3-autumn', grade: 3, semester: 'autumn', themeId: 'our-campus', themeTitle: '我们的校园', projectTitle: '我们的校园——我的探究', drivingQuestion: '我最想改善校园的哪一点？', planRef: 'g3-our-campus' },
  { id: 'g3-spring', grade: 3, semester: 'spring', themeId: 'hometown-taste', themeTitle: '家乡的味道', projectTitle: '味道地图', drivingQuestion: '家乡哪种味道最能代表我们？' },
  { id: 'g4-autumn', grade: 4, semester: 'autumn', themeId: 'green-planet', themeTitle: '绿色星球', projectTitle: '班级气象站', drivingQuestion: '一周天气变化有什么规律？' },
  { id: 'g4-spring', grade: 4, semester: 'spring', themeId: 'hometown-taste', themeTitle: '家乡的味道', projectTitle: '午餐营养调查', drivingQuestion: '怎样搭配更均衡的午餐？' },
  { id: 'g5-autumn', grade: 5, semester: 'autumn', themeId: 'green-planet', themeTitle: '绿色星球', projectTitle: '河水与能源', drivingQuestion: '附近河水适合养鱼吗？屋顶能发多少电？' },
  { id: 'g5-spring', grade: 5, semester: 'spring', themeId: 'community-helper', themeTitle: '社区小管家', projectTitle: '社区需求地图', drivingQuestion: '居民最需要哪种设施？' },
  { id: 'g6-autumn', grade: 6, semester: 'autumn', themeId: 'our-campus', themeTitle: '我们的校园', projectTitle: '校园数据看板', drivingQuestion: '哪些校园数据值得被看见？' },
  { id: 'g6-spring', grade: 6, semester: 'spring', themeId: 'community-helper', themeTitle: '社区小管家', projectTitle: '毕业 capstone：少年提案', drivingQuestion: '我向社区提什么建议最有效？' },
];

const primaryNodes = nodesData.nodes.filter((n) => {
  const g = n.grade;
  return (n.gradeBand === 'primary' || (g >= 1 && g <= 6)) && g >= 1 && g <= 6;
});

const byGradeSubject = {};
primaryNodes.forEach((n) => {
  const k = `${n.grade}|${n.subject}`;
  if (!byGradeSubject[k]) byGradeSubject[k] = [];
  byGradeSubject[k].push(n);
});

const assignment = new Map(); // nodeId -> { level, semesterId }
const gapReasons = new Map();

primaryNodes.filter(isGapCandidate).forEach((n) => {
  gapReasons.set(n.id, '常规课：基础技能操练（拼音/笔顺等）');
});

function pickNodes(grade, count, level, semesterId, subjectsRoundRobin = true) {
  const picked = [];
  const subjects = ['chinese', 'math', 'science', 'english', 'politics', 'info-tech', 'psychology'];
  let si = 0;
  while (picked.length < count && si < subjects.length * 3) {
    const sub = subjects[si % subjects.length];
    const pool = (byGradeSubject[`${grade}|${sub}`] || []).filter((n) => !assignment.has(n.id) && !gapReasons.has(n.id));
    if (pool.length) {
      const node = pool.shift();
      assignment.set(node.id, { level, semesterId });
      picked.push(node.id);
    }
    si += 1;
  }
  return picked;
}

SEMESTERS.forEach((sem) => {
  const core = pickNodes(sem.grade, CORE_PER_SEMESTER, 'core', sem.id);
  const mention = pickNodes(sem.grade, MENTION_PER_SEMESTER, 'mention', sem.id);
  // 螺旋：若本年级节点不足，从相邻年级补 mention
  if (mention.length < MENTION_PER_SEMESTER) {
    const adj = [sem.grade - 1, sem.grade + 1].filter((g) => g >= 1 && g <= 6);
    for (const g of adj) {
      if (mention.length >= MENTION_PER_SEMESTER) break;
      const extra = pickNodes(g, MENTION_PER_SEMESTER - mention.length, 'mention', sem.id);
      mention.push(...extra);
    }
  }
  sem.coreNodeIds = core;
  sem.mentionNodeIds = mention;
});

// 未分配 → gap
primaryNodes.forEach((n) => {
  if (!assignment.has(n.id) && !gapReasons.has(n.id)) {
    gapReasons.set(n.id, '常规课：本推演留待单元教学/复习课覆盖');
  }
});

function statsAt(semesterIndex) {
  const allowed = new Set(SEMESTERS.slice(0, semesterIndex + 1).flatMap((s) => [...s.coreNodeIds, ...s.mentionNodeIds]));
  let core = 0; let mention = 0; let gap = 0;
  primaryNodes.forEach((n) => {
    const a = assignment.get(n.id);
    if (a && allowed.has(n.id)) {
      if (a.level === 'core') core += 1;
      else mention += 1;
    } else if (gapReasons.has(n.id)) gap += 1;
    else if (!a) gap += 1;
  });
  const touched = core + mention;
  return {
    core, mention, gap, touched,
    touchRate: Math.round((touched / primaryNodes.length) * 1000) / 10,
    coreRate: Math.round((core / primaryNodes.length) * 1000) / 10,
  };
}

function subjectBreakdown(nodeIds) {
  const out = {};
  nodeIds.forEach((id) => {
    const n = primaryNodes.find((x) => x.id === id);
    if (!n) return;
    out[n.subject] = (out[n.subject] || 0) + 1;
  });
  return out;
}

const cumulative = SEMESTERS.map((sem, i) => ({
  semesterId: sem.id,
  ...statsAt(i),
}));

const finalStats = statsAt(SEMESTERS.length - 1);
const explicitGap = primaryNodes.filter((n) => gapReasons.has(n.id)).length;

const roadmap = {
  $schema: '../pbl-primary-coverage.schema.json',
  version: '1.0.0',
  title: '小学 6 年 PBL 课标覆盖推演',
  description: '12 个跨学科学期项目 + 覆盖矩阵推演（非实施承诺，供教研规划参考）',
  projectMode: 'cross-disciplinary',
  model: {
    totalPrimaryNodes: primaryNodes.length,
    semesters: 12,
    projectsPerSemester: 1,
    corePerProject: { target: CORE_PER_SEMESTER, range: [8, 12] },
    mentionPerProject: { target: MENTION_PER_SEMESTER, range: [5, 15] },
    excludedFromAudit: nodesData.excludedSubjects || ['art', 'pe', 'music', 'design'],
    assumptions: [
      '每学期 1 个跨学科 PBL（全班共享主题壳，学生各提驱动问）',
      '单次拆解路径核心嵌入约 8–12 节点，拓展提及 5–15 节点',
      '拼音/笔顺等基础技能节点标注为 gap，由常规课承担',
      '同一节点可在多年度螺旋复现（本推演按首次分配计）',
    ],
  },
  nodeInventory: {
    byGrade: Object.fromEntries([1, 2, 3, 4, 5, 6].map((g) => [g, primaryNodes.filter((n) => n.grade === g).length])),
    bySubject: Object.fromEntries(
      [...new Set(primaryNodes.map((n) => n.subject))].map((s) => [s, primaryNodes.filter((n) => n.subject === s).length]),
    ),
  },
  semesters: SEMESTERS.map((sem, i) => {
    const archetype = archetypes.flagshipProjects?.find((f) => f.grade === sem.grade && f.subject === 'cross')
      || archetypes.flagshipProjects?.find((f) => f.grade === sem.grade);
    return {
      ...sem,
      label: `${sem.grade} 年级 · ${sem.semester === 'autumn' ? '上' : '下'}学期`,
      duration: '6 周 · 约 24 课时',
      teachanySubject: 'cross',
      subjectFloor: {
        chinese: { minCore: 1, label: '语文' },
        math: { minCore: 1, label: '数学' },
        science: { minCore: 1, label: '科学' },
      },
      referenceArchetype: archetype?.id || null,
      coverage: {
        core: sem.coreNodeIds.length,
        mention: sem.mentionNodeIds.length,
        newNodesThisSemester: sem.coreNodeIds.length + sem.mentionNodeIds.length,
        bySubjectCore: subjectBreakdown(sem.coreNodeIds),
        bySubjectMention: subjectBreakdown(sem.mentionNodeIds),
      },
      cumulative: cumulative[i],
    };
  }),
  expectedCoverageMatrix: {},
  gapNodes: [...gapReasons.entries()].map(([nodeId, reason]) => {
    const n = primaryNodes.find((x) => x.id === nodeId);
    return { nodeId, nodeName: n?.name, subject: n?.subject, grade: n?.grade, reason };
  }),
  summary: {
    after6Years: {
      ...finalStats,
      explicitGapNodes: explicitGap,
      implicitGapNodes: finalStats.gap - explicitGap,
      feasibility: finalStats.touchRate >= 95 ? '可行' : '需增补项目或压缩 gap',
      mathCheck: `${SEMESTERS.length} 学期 × ~${CORE_PER_SEMESTER + MENTION_PER_SEMESTER} 节点/学期 ≈ ${SEMESTERS.length * (CORE_PER_SEMESTER + MENTION_PER_SEMESTER)} 槽位 ≥ ${primaryNodes.length} 课标节点`,
    },
  },
  generatedAt: new Date().toISOString(),
};

// 合并为 expectedCoverageMatrix（全周期）
primaryNodes.forEach((n) => {
  const a = assignment.get(n.id);
  if (a) {
    roadmap.expectedCoverageMatrix[n.id] = { [a.semesterId]: a.level };
  } else {
    roadmap.expectedCoverageMatrix[n.id] = { gap: true, reason: gapReasons.get(n.id) || '常规课' };
  }
});

const outPath = join(root, 'data/plans/primary-6year-roadmap.json');
writeFileSync(outPath, JSON.stringify(roadmap, null, 2), 'utf8');

console.log('Wrote', outPath);
console.log('Nodes:', primaryNodes.length);
console.log('Final touch rate:', finalStats.touchRate + '%');
console.log('Final core rate:', finalStats.coreRate + '%');
console.log('Gap nodes:', finalStats.gap);
