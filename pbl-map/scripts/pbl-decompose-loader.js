/**
 * 子 PBL 拆解演示加载
 */
(function (global) {
  async function loadDecompose(projectId) {
    const id = projectId
      || new URLSearchParams(location.search).get('project')
      || new URLSearchParams(location.search).get('id');
    if (!id) throw new Error('缺少 project id');
    const res = await fetch(`./data/decompose/${id}.json`);
    if (!res.ok) throw new Error(`拆解数据 ${id} 不存在`);
    const data = await res.json();
    if (data.model !== 'pbl-decompose-demo') {
      throw new Error(`${id} 不是拆解演示数据`);
    }
    return data;
  }

  async function loadIndex() {
    const res = await fetch('./data/decompose/index.json');
    if (!res.ok) throw new Error('拆解索引不存在，请运行 npm run build:decompose');
    return res.json();
  }

  /** 转为 demo.html / plan.html 兼容的 plan 形状 */
  function asPlanShape(record) {
    return {
      id: record.id,
      title: record.title,
      grade: record.grade,
      gradeBand: record.gradeBand,
      semester: record.semester,
      themeShell: {
        title: record.themeShell || record.themeChain,
        duration: `${record.weeks} 周`,
      },
      project: {
        id: record.id,
        title: record.title,
        featuredDrivingQuestion: record.drivingQuestion,
        teachanySubject: 'cross',
      },
      weeklySchedule: record.weeklySchedule || [],
      decomposeDemo: record.decomposeDemo,
      expectedCoverageMatrix: record.expectedCoverageMatrix || {},
      expectedStats: {
        plannedCore: record.expectedStats?.mandatory || 0,
        plannedMention: record.expectedStats?.certified || 0,
        plannedGap: 0,
      },
      packId: record.packId,
      planRef: record.planRef,
    };
  }

  function buildTeachAnyUrl(record) {
    const q = record.decomposeDemo?.teachanyLaunchQuery || {};
    const params = new URLSearchParams({
      goal: q.goal || record.decomposeDemo?.teachanyGoal || '',
      grade: q.grade || record.gradeBand || 'primary',
      subject: q.subject || 'cross',
      deliverable: q.deliverable || 'report',
    });
    return `./engine/pbl.html?${params.toString()}`;
  }

  global.PBLDecomposeLoader = {
    loadDecompose,
    loadIndex,
    asPlanShape,
    buildTeachAnyUrl,
  };
})(typeof window !== 'undefined' ? window : globalThis);
