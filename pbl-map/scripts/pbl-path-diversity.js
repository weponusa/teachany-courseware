/**
 * 班级 PBL 路径差异度 — 同主题下节点 Jaccard 相似度
 */
(function (global) {
  function jaccard(setA, setB) {
    if (!setA.size && !setB.size) return 1;
    let inter = 0;
    setA.forEach((x) => { if (setB.has(x)) inter += 1; });
    const union = setA.size + setB.size - inter;
    return union ? inter / union : 0;
  }

  function pathFingerprint(run) {
    const ids = global.PBLPrimaryCoverage?.extractNodeIdsFromRun(run)
      || extractIdsFallback(run);
    const matched = (run?.graphData?.nodes || [])
      .filter((n) => n.layer === 'matched' || (!n.layer && !n.isExternal))
      .map((n) => String(n.id));
    const order = (run?.pathPlan?.steps || run?.implementationPath?.phases || [])
      .map((s) => s.title || s.name || '')
      .join('|');
    const core = [...ids].sort().join(',');
    return { coreIds: ids, hash: `${core}::${order}` };
  }

  function extractIdsFallback(run) {
    const ids = new Set();
    (run?.graphData?.nodes || run?.matched || []).forEach((n) => {
      if (n?.id && n.layer !== 'external' && !n.isExternal) ids.add(String(n.id));
    });
    return ids;
  }

  function filterRunsByTheme(runs, themeShell) {
    const theme = String(themeShell || '').trim();
    if (!theme) return runs;
    return runs.filter((r) => {
      const shell = r.themeShell || r.projectSpec?.audience || '';
      const goal = r.goal || '';
      return shell.includes(theme) || goal.includes(`主题:${theme}`);
    });
  }

  /**
   * 计算班级路径差异度报告
   * diversityScore: 1 - 平均两两 Jaccard（越高越个性化）
   */
  function computeClassDiversity(runs, options = {}) {
    const filtered = filterRunsByTheme(runs, options.themeShell);
    const valid = filtered.filter((r) => pathFingerprint(r).coreIds.size > 0);

    if (valid.length < 2) {
      return {
        studentCount: valid.length,
        pairwiseAvgJaccard: valid.length ? 1 : 0,
        diversityScore: valid.length ? 0 : null,
        students: valid.map((r) => summarizeStudent(r)),
        message: valid.length < 2 ? '至少需要 2 条有效路径才能计算差异度' : '',
      };
    }

    const fps = valid.map((r) => ({ run: r, ...pathFingerprint(r) }));
    let sum = 0;
    let pairs = 0;
    for (let i = 0; i < fps.length; i += 1) {
      for (let j = i + 1; j < fps.length; j += 1) {
        sum += jaccard(fps[i].coreIds, fps[j].coreIds);
        pairs += 1;
      }
    }
    const avgJ = pairs ? sum / pairs : 0;

    return {
      studentCount: valid.length,
      pairwiseAvgJaccard: Math.round(avgJ * 1000) / 1000,
      diversityScore: Math.round((1 - avgJ) * 1000) / 1000,
      overlapRate: Math.round(avgJ * 100),
      students: fps.map(({ run, coreIds, hash }) => ({
        ...summarizeStudent(run),
        coreNodeCount: coreIds.size,
        fingerprint: hash.slice(0, 16),
      })),
    };
  }

  function summarizeStudent(run) {
    return {
      id: run.id,
      name: run.studentName || '匿名',
      drivingQuestion: run.drivingQuestion || run.projectBlueprint?.drivingQuestion || '',
      goal: (run.goal || '').slice(0, 80),
      ts: run.ts || run.createdAt,
    };
  }

  function attachStudentMetaToRun(run, studentSpec) {
    const s = global.PBLStudentForm?.normalizeStudentSpec(studentSpec) || studentSpec || {};
    return {
      ...run,
      studentName: s.studentName,
      drivingQuestion: s.drivingQuestion,
      themeShell: s.themeShell,
      themeShellId: s.themeShellId,
      outputIntent: s.outputIntent,
      whyCare: s.whyCare,
      interestTags: s.interestTags,
    };
  }

  global.PBLPathDiversity = {
    jaccard,
    pathFingerprint,
    computeClassDiversity,
    filterRunsByTheme,
    attachStudentMetaToRun,
  };
})(typeof window !== 'undefined' ? window : globalThis);
