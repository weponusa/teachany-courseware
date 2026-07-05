/**
 * CN 小初高 PBL 覆盖矩阵 — 审计、缺口分析、项目建议
 */
(function (global) {
  const cfg = () => global.PBL_MAP_CONFIG || {};

  const EXCLUDED_SUBJECTS = new Set(['art', 'pe', 'music', 'design', 'physical-education']);

  function gradeBandFromGrade(grade) {
    const g = parseInt(String(grade).replace(/\D/g, ''), 10);
    if (g >= 1 && g <= 6) return 'primary';
    if (g >= 7 && g <= 9) return 'junior';
    if (g >= 10 && g <= 12) return 'senior';
    return 'unknown';
  }

  function loadPBLRuns() {
    const key = cfg().storageKeys?.pblRuns || 'teachany_history_v1_pbl_runs';
    try {
      const raw = localStorage.getItem(key);
      const runs = JSON.parse(raw || '[]');
      return Array.isArray(runs) ? runs : [];
    } catch (_e) {
      return [];
    }
  }

  function extractNodeIdsFromRun(run) {
    const ids = new Set();
    const nodes = run?.graphData?.nodes || run?.matched || [];
    nodes.forEach((n) => {
      if (!n?.id || n.isExternal || n.layer === 'external') return;
      if (n.layer === 'matched' || n.layer === 'prerequisite' || !n.layer) {
        ids.add(String(n.id));
      }
    });
    return ids;
  }

  function classifyNodeLevelInRun(run, nodeId) {
    const nodes = run?.graphData?.nodes || run?.matched || [];
    const hit = nodes.find((n) => String(n.id) === String(nodeId));
    if (!hit) return null;
    if (hit.layer === 'matched' || (!hit.layer && !hit.isExternal)) return 'core';
    if (hit.layer === 'prerequisite') return 'mention';
    return 'mention';
  }

  function isCNK12Node(node) {
    if (!node || EXCLUDED_SUBJECTS.has(node.subject)) return false;
    const gp = String(node.graph_path || node.path || node.treePath || '');
    const isCN = gp.startsWith('cn/') || gp.startsWith('cn-unified/')
      || gp.includes('/elementary/') || gp.includes('/middle/') || gp.includes('/high/');
    if (!isCN && node.source !== 'supplement-tree') return false;
    const grade = node.grade ?? node.grades;
    if (grade == null) return false;
    const g = parseInt(String(grade).replace(/\D/g, ''), 10);
    return g >= 1 && g <= 12;
  }

  /** @deprecated 兼容旧名 */
  function isPrimaryCNNode(node) {
    if (!isCNK12Node(node)) return false;
    return gradeBandFromGrade(node.grade) === 'primary';
  }

  async function loadCNK12Nodes(options = {}) {
    const localPath = `${cfg().localDataBase || './data'}/cn-k12-nodes.json`;
    let nodes = [];
    try {
      const localRes = await fetch(localPath);
      if (localRes.ok) {
        const data = await localRes.json();
        nodes = data.nodes || data;
      }
    } catch (_e) { /* fallback */ }

    if (!nodes.length) {
      const legacy = await fetch(`${cfg().localDataBase || './data'}/primary-cn-nodes.json`);
      if (legacy.ok) {
        const data = await legacy.json();
        nodes = data.nodes || data;
      }
    }

    if (options.gradeBand) {
      nodes = nodes.filter((n) => (n.gradeBand || gradeBandFromGrade(n.grade)) === options.gradeBand);
    }
    if (options.subject) {
      nodes = nodes.filter((n) => n.subject === options.subject);
    }
    if (options.grade) {
      nodes = nodes.filter((n) => String(n.grade) === String(options.grade));
    }
    return nodes.filter((n) => !EXCLUDED_SUBJECTS.has(n.subject));
  }

  /** @deprecated */
  async function loadPrimaryCNNodes() {
    return loadCNK12Nodes({ gradeBand: 'primary' });
  }

  async function loadArchetypes() {
    const res = await fetch(`${cfg().localDataBase || './data'}/pbl-primary-archetypes.json`);
    if (!res.ok) return { flagshipProjects: [] };
    return res.json();
  }

  function filterRuns(runs, options = {}) {
    return runs.filter((r) => {
      const spec = r.projectSpec || {};
      if (options.gradeBand && spec.gradeLevel && spec.gradeLevel !== 'any') {
        if (spec.gradeLevel !== options.gradeBand) return false;
      }
      if (options.themeShellId && r.themeShellId !== options.themeShellId) return false;
      return !!(r?.graphData?.nodes?.length || r?.matched?.length);
    });
  }

  /**
   * 构建 知识点 × 项目 覆盖矩阵（小初高）
   */
  async function buildCoverageMatrix(options = {}) {
    const runs = filterRuns(options.runs || loadPBLRuns(), options);
    const cnNodes = await loadCNK12Nodes({
      gradeBand: options.gradeBand,
      subject: options.subject,
      grade: options.grade,
    });

    const matrix = {};
    const projectMeta = runs.map((run) => ({
      id: run.id || run.goal?.slice(0, 24),
      title: run.goal || run.projectSpec?.task || '未命名项目',
      studentName: run.studentName || '',
      drivingQuestion: run.drivingQuestion || run.projectBlueprint?.drivingQuestion || '',
      gradeLevel: run.projectSpec?.gradeLevel || '',
      nodeCount: extractNodeIdsFromRun(run).size,
      ts: run.ts || run.createdAt,
    }));

    cnNodes.forEach((node) => {
      const nid = String(node.id);
      const projects = {};
      runs.forEach((run) => {
        const pid = run.id || String(run.ts);
        const level = classifyNodeLevelInRun(run, nid);
        if (level) projects[pid] = level;
      });
      const levels = Object.values(projects);
      let bestLevel = 'gap';
      if (levels.includes('core')) bestLevel = 'core';
      else if (levels.includes('mention')) bestLevel = 'mention';

      matrix[nid] = {
        nodeId: nid,
        nodeName: node.name || node.label || nid,
        subject: node.subject || 'unknown',
        grade: node.grade,
        gradeBand: node.gradeBand || gradeBandFromGrade(node.grade),
        projects,
        bestLevel,
      };
    });

    const stats = { totalNodes: cnNodes.length, coreCovered: 0, mentionOnly: 0, gaps: 0 };
    Object.values(matrix).forEach((row) => {
      if (row.bestLevel === 'core') stats.coreCovered += 1;
      else if (row.bestLevel === 'mention') stats.mentionOnly += 1;
      else stats.gaps += 1;
    });
    stats.coverageRate = stats.totalNodes
      ? Math.round((stats.coreCovered / stats.totalNodes) * 1000) / 10
      : 0;

    const gaps = Object.values(matrix)
      .filter((r) => r.bestLevel === 'gap')
      .map((r) => ({
        nodeId: r.nodeId,
        nodeName: r.nodeName,
        subject: r.subject,
        grade: r.grade,
        gradeBand: r.gradeBand,
      }));

    return {
      matrix,
      projects: projectMeta,
      stats,
      gaps,
      runsAnalyzed: runs.length,
      gradeBand: options.gradeBand || 'all',
    };
  }

  /** @deprecated */
  async function buildPrimaryCoverageMatrix(options = {}) {
    return buildCoverageMatrix({ ...options, gradeBand: options.gradeBand || 'primary' });
  }

  async function suggestProjectsForGaps(gaps, options = {}) {
    const archetypes = await loadArchetypes();
    const flagships = archetypes.flagshipProjects || [];
    const limit = options.limit || 20;

    return gaps.slice(0, limit).map((gap) => {
      const g = parseInt(String(gap.grade || '0').replace(/\D/g, ''), 10);
      const band = gap.gradeBand || gradeBandFromGrade(g);
      const sub = gap.subject || 'cross';

      const candidates = flagships.filter((f) => {
        const fBand = f.gradeBand || gradeBandFromGrade(f.grade);
        if (band !== 'unknown' && fBand !== band && fBand !== 'cross') return false;
        if (g >= 1 && g <= 12 && f.grade && f.grade !== g) return false;
        if (sub !== 'unknown' && f.subject !== sub && f.subject !== 'cross') return false;
        return true;
      });

      const best = candidates[0]
        || flagships.find((f) => f.subject === sub && (f.gradeBand || gradeBandFromGrade(f.grade)) === band)
        || flagships.find((f) => f.subject === sub)
        || flagships[0];

      return {
        gap,
        suggestedProject: best
          ? {
              id: best.id,
              title: best.title,
              themeShell: best.themeShell,
              sampleDrivingQuestions: best.sampleDrivingQuestions || [],
              deliverable: best.deliverable,
            }
          : null,
        rationale: best
          ? `匹配 ${best.gradeBand || band} · ${best.subject} 旗舰「${best.title}」`
          : '暂无匹配旗舰模板，建议教研人工策划',
      };
    });
  }

  function saveAuditSnapshot(audit) {
    const key = cfg().storageKeys?.coverageAudit || 'pblmap_coverage_audit_v1';
    try {
      const list = JSON.parse(localStorage.getItem(key) || '[]');
      list.unshift({ ...audit, savedAt: Date.now() });
      localStorage.setItem(key, JSON.stringify(list.slice(0, 20)));
    } catch (_e) { /* ignore */ }
  }

  global.PBLCoverage = {
    gradeBandFromGrade,
    loadPBLRuns,
    extractNodeIdsFromRun,
    loadCNK12Nodes,
    buildCoverageMatrix,
    suggestProjectsForGaps,
    saveAuditSnapshot,
    isCNK12Node,
    EXCLUDED_SUBJECTS,
  };

  global.PBLPrimaryCoverage = {
    ...global.PBLCoverage,
    loadPrimaryCNNodes,
    buildPrimaryCoverageMatrix,
    isPrimaryCNNode,
  };
})(typeof window !== 'undefined' ? window : globalThis);
