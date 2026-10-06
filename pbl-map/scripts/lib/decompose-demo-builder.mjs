/**
 * 从学期覆盖包子项目生成拆解演示数据
 */
export const SUBJECT_LABELS = {
  chinese: '语文', math: '数学', science: '科学', english: '英语',
  politics: '道法', 'info-tech': '信息科技', psychology: '心理',
  physics: '物理', chemistry: '化学', biology: '生物',
  history: '历史', geography: '地理', cs: '计算机',
};

const METHOD_STEPS = [
  {
    step: 1,
    title: '合成拆解目标',
    tool: 'PBLStudentForm.composeGoalFromStudentSpec',
    input: '主题壳 + 子项目驱动问 + mandatory 清单 + 产出意向',
    output: 'TeachAny goal 字符串（驱动问权重最高）',
  },
  {
    step: 2,
    title: '跨学科召回',
    tool: 'TeachAny pbl.html · subject=cross',
    input: 'goal + 年级 + mandatory 约束',
    output: '知识图谱：matched（M）+ prerequisite（C）节点',
  },
  {
    step: 3,
    title: '路径排序',
    tool: 'pbl-path.js pathPlan',
    input: '图谱拓扑 + 子项目周次',
    output: '按调查→分析→产出顺序排列的学习路径',
  },
  {
    step: 4,
    title: '融入检核',
    tool: 'completionGate + 个人台账',
    input: 'mandatoryNodeIds 全部 M 或 C',
    output: '未过关不得进入下一子 PBL',
  },
  {
    step: 5,
    title: '写入覆盖审计',
    tool: 'pbl_runs → personalLedger',
    input: '拆解 graphData + 产出证据',
    output: '学期包内节点状态更新；gap=0 关门',
  },
];

const PHASES = ['ask', 'decompose', 'investigate', 'analyze', 'synthesize', 'present'];

function gradeBand(grade) {
  if (grade <= 6) return 'primary';
  if (grade <= 9) return 'junior';
  return 'senior';
}

function gradeLabel(grade, band) {
  if (band === 'primary') return `小学${grade}年级`;
  if (band === 'junior') return `初中${grade}年级`;
  return `高中${grade}年级`;
}

function phaseForIndex(i, total) {
  const r = (i + 1) / total;
  if (r <= 0.12) return 'ask';
  if (r <= 0.22) return 'decompose';
  if (r <= 0.45) return 'investigate';
  if (r <= 0.65) return 'analyze';
  if (r <= 0.85) return 'synthesize';
  return 'present';
}

function activityForNode(node, project, pack) {
  const theme = pack.themeShell?.title || pack.themeChain;
  return `在「${theme}·${project.title}」中运用「${node.name}」支撑驱动问`;
}

function evidenceForNode(node, masteryLevel) {
  if (masteryLevel === 'M') {
    return `产出物中可核验运用：${node.name}（M 级掌握）`;
  }
  return `micro-block 短测过关：${node.name}（C 级认证）`;
}

function deliverableSlice(node) {
  const map = {
    chinese: '说明/表达切片',
    math: '数据与计算切片',
    science: '探究记录切片',
    english: '英语表达切片',
    politics: '公民议题切片',
    'info-tech': '信息与工具切片',
    psychology: '反思日志切片',
    physics: '实验/测量切片',
    chemistry: '变化证据切片',
    biology: '生命系统切片',
    history: '史料分析切片',
    geography: '空间分析切片',
    cs: '算法实现切片',
  };
  return map[node.subject] || '项目附录';
}

function subjectFloorCheck(mandatory) {
  const subs = new Set(mandatory.map((n) => n.subject));
  const need = ['chinese', 'math', 'science'];
  const check = {};
  need.forEach((s) => { check[s] = subs.has(s); });
  if (gradeBand(mandatory[0]?.grade || 7) === 'senior') {
    check.passed = need.filter((s) => check[s]).length >= 2;
  } else {
    check.passed = need.every((s) => check[s]);
  }
  return check;
}

function buildFeaturedStudent(project, pack) {
  const theme = pack.themeShell?.title || pack.themeChain;
  return {
    name: '示例学生',
    drivingQuestion: project.drivingQuestion,
    outputIntent: project.deliverable || `${theme}检核报告 + 节点过关单`,
    whyCare: `我对「${theme}」主题下的这个问题很好奇，想做出有证据的产出`,
  };
}

function buildTeachanyGoal(project, pack, featured) {
  const band = pack.gradeBand || gradeBand(pack.grade);
  const parts = [
    gradeLabel(pack.grade, band),
    `主题:${pack.themeShell?.title || pack.themeChain}`,
    `子项目:${project.title}`,
    `驱动问:${featured.drivingQuestion}`,
    `产出意向:${featured.outputIntent}`,
    `mandatory:${(project.mandatoryNodeIds || []).slice(0, 10).join(',')}`,
    `产出:检核报告/研究报告`,
  ];
  return parts.join('｜');
}

function buildSamplePath(project, pack) {
  const mandatory = project.knowledgePoints?.mandatory || [];
  const certified = project.knowledgePoints?.certified || [];
  const sequence = [
    ...mandatory.map((n) => n.id),
    ...certified.map((n) => n.id),
  ];
  const total = sequence.length || 1;
  const nodes = [
    ...mandatory.map((n, i) => ({
      id: n.id,
      layer: 'matched',
      phase: phaseForIndex(i, total),
      activity: activityForNode(n, project, pack),
      evidence: evidenceForNode(n, 'M'),
      deliverable: deliverableSlice(n),
    })),
    ...certified.map((n, i) => ({
      id: n.id,
      layer: 'prerequisite',
      phase: phaseForIndex(mandatory.length + i, total),
      activity: activityForNode(n, project, pack),
      evidence: evidenceForNode(n, 'C'),
      deliverable: deliverableSlice(n),
    })),
  ];
  const subjects = new Set([...mandatory, ...certified].map((n) => n.subject));
  return {
    pathTitle: `${project.title} · 路径（${sequence.length} 节点）`,
    subjectFloorCheck: subjectFloorCheck(mandatory),
    sequence,
    nodes,
    pathStats: {
      totalNodes: sequence.length,
      coreMatched: mandatory.length,
      prerequisite: certified.length,
      subjectsSpanned: subjects.size,
    },
  };
}

function buildDeliverableBlueprint(project, pack) {
  const all = [
    ...(project.knowledgePoints?.mandatory || []),
    ...(project.knowledgePoints?.certified || []),
  ];
  const bySubject = {};
  all.forEach((n) => {
    if (!bySubject[n.subject]) bySubject[n.subject] = [];
    bySubject[n.subject].push(n.id);
  });
  const sections = Object.entries(bySubject).map(([sub, ids]) => ({
    name: `${SUBJECT_LABELS[sub] || sub} · ${project.title}`,
    nodes: ids,
    format: deliverableSlice({ subject: sub }),
  }));
  return {
    title: `${pack.themeChain} — ${project.title} 产出蓝图`,
    sections,
    finalProducts: [
      project.deliverable || '检核报告 + 节点过关单',
      `${project.weeks} 周过程性证据`,
      '课堂答辩（可选）',
    ],
  };
}

function buildExpectedMatrix(project) {
  const matrix = {};
  (project.knowledgePoints?.mandatory || []).forEach((n) => {
    matrix[n.id] = { [project.id]: 'M' };
  });
  (project.knowledgePoints?.certified || []).forEach((n) => {
    matrix[n.id] = { [project.id]: 'C' };
  });
  return matrix;
}

function buildWeeklySchedule(project) {
  const w = project.weeks || 2;
  if (w <= 2) {
    return [
      { week: 1, phase: 'ask', focus: '驱动问 + 拆解', teacher: ['发布 mandatory 清单'], student: ['TeachAny 跨学科拆解', '标注节点用法'] },
      { week: w, phase: 'present', focus: '产出 + 检核', teacher: ['M/C 过关检核'], student: ['提交产出', '台账更新'] },
    ];
  }
  const sched = [
    { week: 1, phase: 'ask', focus: '驱动问 workshop', teacher: ['明确 mandatory'], student: ['改写驱动问'] },
    { week: 2, phase: 'decompose', focus: 'TeachAny 拆解', teacher: ['检核路径覆盖 mandatory'], student: ['生成个人图谱'] },
  ];
  for (let i = 3; i < w; i += 1) {
    sched.push({
      week: i,
      phase: i < w - 1 ? 'investigate' : 'synthesize',
      focus: '探究与产出',
      teacher: ['过程反馈'],
      student: ['收集证据', '草稿产出'],
    });
  }
  sched.push({ week: w, phase: 'present', focus: '检核关门', teacher: ['M/C 检核'], student: ['答辩', '台账关门'] });
  return sched;
}

/**
 * @param {object} project - pack.projects[i]
 * @param {object} pack - semester pack
 * @param {object} [importedDemo] - 手工策划包 decomposeDemo（可选）
 */
export function buildDecomposeRecord(project, pack, importedDemo = null) {
  const featured = importedDemo?.featuredStudent || buildFeaturedStudent(project, pack);
  const samplePath = importedDemo?.samplePath
    ? filterImportedPath(importedDemo.samplePath, project)
    : buildSamplePath(project, pack);

  const decomposeDemo = {
    purpose: `子 PBL「${project.title}」：驱动问 → 跨学科拆解 → mandatory 节点 M/C 过关`,
    featuredStudent: featured,
    teachanyGoal: importedDemo?.teachanyGoal || buildTeachanyGoal(project, pack, featured),
    methodSteps: importedDemo?.methodSteps || METHOD_STEPS,
    samplePath,
    deliverableBlueprint: importedDemo?.deliverableBlueprint || buildDeliverableBlueprint(project, pack),
    outcomes: {
      pathStats: samplePath.pathStats || buildSamplePath(project, pack).pathStats,
      packContext: {
        packId: pack.id,
        projectIndex: (pack.projects || []).findIndex((p) => p.id === project.id) + 1,
        projectTotal: pack.projectCount,
        nodePoolSize: pack.nodePoolSize,
      },
      auditNote: `本子项目覆盖 ${project.stats?.total || 0} 节点（M ${project.stats?.mandatory || 0} · C ${project.stats?.certified || 0}）；并集归属 ${pack.title}`,
    },
    teachanyLaunchQuery: {
      goal: importedDemo?.teachanyLaunchQuery?.goal || buildTeachanyGoal(project, pack, featured),
      grade: pack.gradeBand || gradeBand(pack.grade),
      subject: 'cross',
      deliverable: 'report',
    },
  };

  return {
    version: '1.0.0',
    model: 'pbl-decompose-demo',
    id: project.id,
    packId: pack.id,
    semesterId: pack.semesterId,
    grade: pack.grade,
    gradeBand: pack.gradeBand || gradeBand(pack.grade),
    gradeBandLabel: pack.gradeBandLabel,
    semester: pack.semester,
    title: project.title,
    themeShell: pack.themeShell?.title || pack.themeChain,
    themeChain: pack.themeChain,
    drivingQuestion: project.drivingQuestion,
    weeks: project.weeks,
    planRef: project.planRef || null,
    mandatoryNodeIds: project.mandatoryNodeIds || [],
    certifiedNodeIds: project.certifiedNodeIds || [],
    stats: project.stats,
    weeklySchedule: buildWeeklySchedule(project),
    decomposeDemo,
    expectedCoverageMatrix: buildExpectedMatrix(project),
    expectedStats: {
      mandatory: project.stats?.mandatory || 0,
      certified: project.stats?.certified || 0,
      total: project.stats?.total || 0,
    },
  };
}

function filterImportedPath(samplePath, project) {
  const allowed = new Set([
    ...(project.mandatoryNodeIds || []),
    ...(project.certifiedNodeIds || []),
  ]);
  const sequence = (samplePath.sequence || []).filter((id) => allowed.has(id));
  const nodes = (samplePath.nodes || []).filter((n) => allowed.has(n.id));
  if (sequence.length === 0) return buildSamplePath(project, { themeChain: '', themeShell: {} });
  const mandatoryIds = new Set(project.mandatoryNodeIds || []);
  const rebuilt = sequence.map((id) => {
    const hit = nodes.find((n) => n.id === id);
    if (hit) return hit;
    return {
      id,
      layer: mandatoryIds.has(id) ? 'matched' : 'prerequisite',
      phase: 'investigate',
      activity: '（来自策划包样例）',
      evidence: '产出检核',
      deliverable: '项目切片',
    };
  });
  const mandatory = project.knowledgePoints?.mandatory || [];
  return {
    ...samplePath,
    sequence,
    nodes: rebuilt,
    pathStats: {
      totalNodes: sequence.length,
      coreMatched: mandatory.length,
      prerequisite: (project.certifiedNodeIds || []).length,
      subjectsSpanned: new Set(rebuilt.map((n) => n.id.split('-')[0])).size,
    },
  };
}

export function mergeImportedDemo(imported, project, pack) {
  if (!imported?.decomposeDemo) return null;
  return buildDecomposeRecord(project, pack, imported.decomposeDemo);
}
