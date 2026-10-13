/**
 * 策划包加载与预期/实际覆盖对比
 */
(function (global) {
  async function loadPlan(planId) {
    const id = planId || new URLSearchParams(location.search).get('id') || 'g3-our-campus';
    const res = await fetch(`./data/plans/${id}.json`);
    if (!res.ok) throw new Error(`策划包 ${id} 不存在`);
    return res.json();
  }

  async function listPlans() {
    return [
      { id: 'g3-our-campus', title: '三年级 · 我们的校园' },
      { id: 'g5-community-map', title: '五年级 · 社区需求地图' },
    ];
  }

  function summarizeExpectedMatrix(plan) {
    const matrix = plan.expectedCoverageMatrix || {};
    const stats = { core: 0, mention: 0, gap: 0, total: 0 };
    Object.entries(matrix).forEach(([nodeId, entry]) => {
      stats.total += 1;
      if (entry.gap) {
        stats.gap += 1;
        return;
      }
      const levels = Object.values(entry).filter((v) => v === 'core' || v === 'mention');
      if (levels.includes('core')) stats.core += 1;
      else if (levels.includes('mention')) stats.mention += 1;
      else stats.gap += 1;
    });
    stats.coreRate = stats.total ? Math.round((stats.core / stats.total) * 1000) / 10 : 0;
    return stats;
  }

  async function comparePlanToActual(plan, options = {}) {
    const expected = plan.expectedCoverageMatrix || {};
    const actual = await global.PBLCoverage.buildCoverageMatrix({
      gradeBand: plan.gradeBand || 'primary',
      grade: plan.grade,
      ...options,
    });

    const nodeIndex = new Map((await global.PBLCoverage.loadCNK12Nodes({
      grade: plan.grade,
    })).map((n) => [n.id, n]));

    const rows = [];
    Object.keys(expected).forEach((nodeId) => {
      const exp = expected[nodeId];
      const node = nodeIndex.get(nodeId) || { id: nodeId, name: nodeId };
      const act = actual.matrix[nodeId];
      const expLevel = exp.gap ? 'gap' : (Object.values(exp).includes('core') ? 'core' : 'mention');
      const actLevel = act?.bestLevel || 'gap';
      rows.push({
        nodeId,
        nodeName: node.name,
        subject: node.subject,
        expected: expLevel,
        actual: actLevel,
        aligned: expLevel === actLevel || (expLevel === 'mention' && actLevel === 'core'),
      });
    });

    const aligned = rows.filter((r) => r.aligned).length;
    return {
      plan,
      expectedStats: summarizeExpectedMatrix(plan),
      actualStats: actual.stats,
      rows,
      alignmentRate: rows.length ? Math.round((aligned / rows.length) * 1000) / 10 : 0,
      runsAnalyzed: actual.runsAnalyzed,
    };
  }

  function applyThemeToStudentForm(plan) {
    const shell = plan.themeShell || {};
    const set = (id, v) => { const el = document.getElementById(id); if (el) el.value = v; };
    set('student-themeShellId', plan.themeId || plan.id);
    set('student-themeShell', shell.title || plan.title);
    set('student-themeDuration', shell.duration || '6 周');
    set('student-themeConstraints', (shell.constraints || []).join('；'));
    set('student-gradeLevel', plan.gradeBand || 'primary');
  }

  function getPrimaryProject(plan) {
    return plan.project || null;
  }

  function getCoverageAnchors(plan) {
    return plan.coverageAnchors || plan.flagships || [];
  }

  global.PBLPlanLoader = {
    loadPlan,
    listPlans,
    summarizeExpectedMatrix,
    comparePlanToActual,
    applyThemeToStudentForm,
    getPrimaryProject,
    getCoverageAnchors,
  };
})(typeof window !== 'undefined' ? window : globalThis);
