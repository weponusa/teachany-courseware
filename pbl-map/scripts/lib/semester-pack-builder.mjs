/**
 * 学期覆盖包构建 — 将学期节点池划分为 K 个子 PBL（无交叠）
 */
export const SUBJECT_LABELS = {
  chinese: '语文', math: '数学', science: '科学', english: '英语',
  politics: '道法', 'info-tech': '信息科技', psychology: '心理',
  physics: '物理', chemistry: '化学', biology: '生物',
  history: '历史', geography: '地理', cs: '计算机',
};

const M_RATIO = 0.45;

export function gradeBand(grade) {
  if (grade <= 6) return 'primary';
  if (grade <= 9) return 'junior';
  return 'senior';
}

export function projectCountForPool(poolSize, band) {
  if (band === 'primary') return poolSize <= 18 ? 2 : 3;
  if (band === 'junior') return poolSize <= 55 ? 4 : 5;
  if (poolSize <= 85) return 6;
  if (poolSize <= 105) return 7;
  return 8;
}

export function weeksForSubProject(band, index, total, isLast) {
  if (band === 'primary') return total <= 2 ? 3 : 2;
  return isLast && total >= 6 ? 3 : 2;
}

const SUBJECT_TITLES = {
  chinese: '表达与读写', math: '数据与建模', science: '探究与实验',
  english: '英语沟通', politics: '公民与规则', 'info-tech': '信息与计算',
  psychology: '心理与成长', physics: '物理世界', chemistry: '物质与变化',
  biology: '生命系统', history: '历史视野', geography: '地理与环境', cs: '算法与程序',
};

function enrichNode(n, masteryLevel, catalogLevel) {
  return {
    id: n.id,
    name: n.name,
    subject: n.subject,
    subjectLabel: SUBJECT_LABELS[n.subject] || n.subject,
    grade: n.grade,
    catalogLevel: catalogLevel || 'core',
    masteryLevel,
  };
}

function dominantSubject(nodes) {
  const c = {};
  nodes.forEach((n) => { c[n.subject] = (c[n.subject] || 0) + 1; });
  return Object.entries(c).sort((a, b) => b[1] - a[1])[0]?.[0] || 'math';
}

function subProjectTitle(sem, subIndex, total, nodes) {
  const sub = dominantSubject(nodes);
  const angle = SUBJECT_TITLES[sub] || '跨学科探究';
  if (total <= 2) return `${sem.themeTitle} · ${angle}`;
  return `${sem.themeTitle} · ${angle} ${subIndex + 1}`;
}

function drivingQuestion(sem, subIndex, total, nodes) {
  const sub = dominantSubject(nodes);
  const templates = {
    chinese: '怎样用证据写出有说服力的说明？',
    math: '如何用数据支撑我们的结论？',
    science: '现象背后有哪些可验证的规律？',
    english: 'How can we present findings clearly in English?',
    politics: '公共决策应如何体现公平？',
    'info-tech': '数字工具如何帮助调查与表达？',
    psychology: '我们如何理解他人与自己的需求？',
    physics: '测量与模型如何解释这一现象？',
    chemistry: '变化过程中有哪些可观测证据？',
    biology: '生命系统如何响应环境变化？',
    history: '历史经验对今天有什么启示？',
    geography: '空间与环境如何影响我们的方案？',
    cs: '算法与程序如何解决问题？',
  };
  if (subIndex === total - 1 && total >= 3) {
    return `${sem.drivingQuestion.replace(/？$/, '')}（综合 ${subIndex + 1}）？`;
  }
  return templates[sub] || sem.drivingQuestion;
}

/**
 * @param {object} sem - 学期元数据 { id, grade, semester, themeTitle, drivingQuestion, planRef }
 * @param {object[]} poolNodes - 带 id name subject grade level 的节点
 * @param {object} options - { planRefMap: { subIndex -> planRef } }
 */
export function buildSemesterPack(sem, poolNodes, options = {}) {
  const band = gradeBand(sem.grade);
  const K = projectCountForPool(poolNodes.length, band);
  const buckets = Array.from({ length: K }, (_, i) => ({
    id: `${sem.id}-p${i + 1}`,
    nodes: [],
  }));

  const subjects = [...new Set(poolNodes.map((n) => n.subject))];
  let ui = 0;
  poolNodes.forEach((node) => {
    const targets = buckets.filter((b) => b.nodes.length < Math.ceil(poolNodes.length / K) + 1);
    targets.sort((a, b) => a.nodes.length - b.nodes.length);
    targets[0].nodes.push(node);
    ui += 1;
  });

  // balance
  for (let guard = 0; guard < 200; guard++) {
    const max = buckets.reduce((a, b) => (a.nodes.length > b.nodes.length ? a : b));
    const min = buckets.reduce((a, b) => (a.nodes.length < b.nodes.length ? a : b));
    if (max.nodes.length - min.nodes.length <= 1 || max.nodes.length === 0) break;
    min.nodes.push(max.nodes.pop());
  }

  const planRefByIndex = options.planRefByIndex || {};
  if (sem.planRef && !planRefByIndex[0]) planRefByIndex[0] = sem.planRef;

  const projects = buckets.map((b, i) => {
    const sorted = [...b.nodes];
    const mCount = Math.max(3, Math.round(sorted.length * M_RATIO));
    const mandatory = sorted.slice(0, mCount).map((n) => enrichNode(n, 'M', n.level));
    const certified = sorted.slice(mCount).map((n) => enrichNode(n, 'C', n.level));
    const isLast = i === K - 1;
    const weeks = weeksForSubProject(band, i, K, isLast);
    return {
      id: b.id,
      title: subProjectTitle(sem, i, K, sorted),
      themeAngle: `${sem.themeTitle} — 子项目 ${i + 1}/${K}`,
      drivingQuestion: drivingQuestion(sem, i, K, sorted),
      weeks,
      planRef: planRefByIndex[i] || null,
      projectMode: 'cross-disciplinary',
      teachanySubject: 'cross',
      duration: `${weeks} 周`,
      completionGate: {
        rule: 'mandatory-all-M-or-C',
        description: 'mandatory 节点全部达 M 或 C 方可进入下一子项目',
      },
      mandatoryNodeIds: mandatory.map((n) => n.id),
      certifiedNodeIds: certified.map((n) => n.id),
      knowledgePoints: {
        mandatory,
        certified,
        allIds: sorted.map((n) => n.id),
      },
      stats: {
        total: sorted.length,
        mandatory: mandatory.length,
        certified: certified.length,
      },
      deliverable: `检核报告 + 节点过关单`,
    };
  });

  const totalWeeks = projects.reduce((s, p) => s + p.weeks, 0);
  const packId = `${sem.id}-pack`;

  return {
    $schema: '../pbl-semester-pack.schema.json',
    version: '2.0.0',
    model: 'semester-coverage-pack',
    id: packId,
    semesterId: sem.id,
    title: `${sem.grade} 年级 · ${sem.semester === 'autumn' ? '上' : '下'}学期 · ${sem.themeTitle}覆盖包`,
    grade: sem.grade,
    gradeBand: band,
    gradeBandLabel: band === 'primary' ? '小学' : band === 'junior' ? '初中' : '高中',
    semester: sem.semester,
    themeChain: sem.themeTitle,
    tagline: `${K} 个高强度 PBL · 人人必做 · 个人台账关门`,
    nodePoolSize: poolNodes.length,
    projectCount: K,
    totalWeeks,
    partitionRule: 'disjoint-union-equals-semester-pool',
    completionRule: {
      student: `完成全部 ${K} 子项目且 personalLedger.gapCount === 0`,
      project: 'mandatoryNodeIds 全部 M 或 C',
      semester: '∪ allIds = nodePool',
    },
    themeShell: {
      title: sem.themeTitle,
      featuredDrivingQuestion: sem.drivingQuestion,
      duration: `${totalWeeks} 周 PBL + 1 周检核`,
      constraints: [
        `本学期 ${K} 个子 PBL 人人必做`,
        '驱动问可个性化，每子项目 mandatory 清单不变',
        'M = 产出掌握；C = micro-block + 短测',
        '无分科补课：gap 在包内补测闭环',
      ],
    },
    personalLedgerSchema: {
      nodeStates: ['gap', 'C', 'M'],
      fields: ['studentId', 'nodeId', 'state', 'projectId', 'evidenceRef', 'assessedAt'],
    },
    projects,
    summary: {
      mandatoryTotal: projects.reduce((s, p) => s + p.stats.mandatory, 0),
      certifiedTotal: projects.reduce((s, p) => s + p.stats.certified, 0),
      assignedNodes: poolNodes.length,
    },
  };
}
