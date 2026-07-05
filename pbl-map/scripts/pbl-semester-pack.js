/**
 * 学期覆盖包加载 + 个人台账（localStorage 原型）
 */
(function (global) {
  const LEDGER_KEY = 'pblmap_personal_ledger_v1';

  async function loadPack(packId) {
    const id = packId || new URLSearchParams(location.search).get('id') || 'g11-spring-pack';
    const res = await fetch(`./data/plans/${id}.json`);
    if (!res.ok) throw new Error(`覆盖包 ${id} 不存在`);
    const data = await res.json();
    if (data.model !== 'semester-coverage-pack') {
      throw new Error(`${id} 不是学期覆盖包`);
    }
    return data;
  }

  async function listPacks() {
    const res = await fetch('./data/k12-pbl-curriculum.json');
    const curriculum = await res.json();
    return (curriculum.semesterPacks || []).map((p) => ({
      id: p.id,
      title: p.label,
      projects: p.projectCount,
      nodes: p.nodePoolSize,
      grade: p.grade,
      semester: p.semester,
    }));
  }

  function getAllNodeIds(pack) {
    return (pack.projects || []).flatMap((p) => p.knowledgePoints?.allIds || [
      ...(p.mandatoryNodeIds || []),
      ...(p.certifiedNodeIds || []),
    ]);
  }

  function loadLedger(studentId) {
    try {
      const all = JSON.parse(localStorage.getItem(LEDGER_KEY) || '{}');
      return all[studentId] || { entries: {}, packProgress: {} };
    } catch (_e) {
      return { entries: {}, packProgress: {} };
    }
  }

  function saveLedger(studentId, ledger) {
    try {
      const all = JSON.parse(localStorage.getItem(LEDGER_KEY) || '{}');
      all[studentId] = ledger;
      localStorage.setItem(LEDGER_KEY, JSON.stringify(all));
    } catch (_e) { /* ignore */ }
  }

  function summarizeLedger(pack, studentId) {
    const ledger = loadLedger(studentId);
    const allIds = getAllNodeIds(pack);
    let M = 0; let C = 0; let gap = 0;
    allIds.forEach((nodeId) => {
      const st = ledger.entries[nodeId]?.state;
      if (st === 'M') M += 1;
      else if (st === 'C') C += 1;
      else gap += 1;
    });
    const projectsDone = (pack.projects || []).filter((p) => {
      const prog = ledger.packProgress[p.id];
      return prog?.status === 'completed';
    }).length;
    return {
      total: allIds.length,
      M, C, gap,
      touchRate: allIds.length ? Math.round(((M + C) / allIds.length) * 1000) / 10 : 0,
      projectsDone,
      projectsTotal: pack.projectCount || pack.projects?.length || 0,
      semesterClear: gap === 0 && projectsDone === (pack.projects?.length || 0),
    };
  }

  function markNode(studentId, nodeId, state, projectId, evidenceRef) {
    const ledger = loadLedger(studentId);
    ledger.entries[nodeId] = {
      state,
      projectId,
      evidenceRef: evidenceRef || '',
      assessedAt: Date.now(),
    };
    saveLedger(studentId, ledger);
    return ledger;
  }

  function markProjectComplete(studentId, projectId) {
    const ledger = loadLedger(studentId);
    ledger.packProgress[projectId] = { status: 'completed', at: Date.now() };
    saveLedger(studentId, ledger);
    return ledger;
  }

  function buildTeachAnyUrl(project, pack, options = {}) {
    const band = pack.gradeBand || (pack.grade <= 6 ? 'primary' : pack.grade <= 9 ? 'junior' : 'senior');
    const gradeLabel = band === 'primary' ? `小学${pack.grade}年级` : band === 'junior' ? `初中${pack.grade}年级` : `高中${pack.grade}年级`;
    const goal = [
      gradeLabel,
      `主题:${pack.themeShell?.title || pack.themeChain}`,
      `子项目:${project.title}`,
      `驱动问:${project.drivingQuestion}`,
      `mandatory:${(project.mandatoryNodeIds || []).slice(0, 8).join(',')}`,
      `产出:检核报告`,
    ].join('｜');
    const params = new URLSearchParams({
      goal: goal.slice(0, 500),
      grade: band,
      subject: 'cross',
      deliverable: 'report',
    });
    return `./engine/pbl.html?${params.toString()}`;
  }

  global.PBLSemesterPack = {
    loadPack,
    listPacks,
    getAllNodeIds,
    loadLedger,
    saveLedger,
    summarizeLedger,
    markNode,
    markProjectComplete,
    buildTeachAnyUrl,
  };
})(typeof window !== 'undefined' ? window : globalThis);
