/**
 * PBL Map — 指向 TeachAny 引擎与课标数据
 * 本地开发默认 symlink: ./engine → ../一次函数/teachany-courseware
 */
(function (global) {
  const loc = global.location;
  const pathname = loc?.pathname || '';
  /** 发布在 teachany.cn/pbl-map/ 时，引擎在站点根目录 */
  const underPblMap = /\/pbl-map(?:\/|$)/.test(pathname);
  const isFileProtocol = loc?.protocol === 'file:';
  const base = underPblMap && !isFileProtocol
    ? '..'
    : isFileProtocol
      ? new URL('./engine/', loc.href).pathname.replace(/\/+$/, '')
      : './engine';

  global.PBL_MAP_CONFIG = {
    engineBase: base,
    dataBase: `${base}/data`,
    scriptsBase: `${base}/scripts`,
    assetsBase: `${base}/assets/scripts`,
    localDataBase: './data',
    storageKeys: {
      pblRuns: 'teachany_history_v1_pbl_runs',
      themeShells: 'pblmap_theme_shells_v1',
      classRoster: 'pblmap_class_roster_v1',
      coverageAudit: 'pblmap_coverage_audit_v1',
    },
    coverage: {
      minCoreNodesPerProject: 5,
      targetCoreNodesPerProject: 8,
      maxCoreNodesPerProject: 15,
      gradeBands: {
        primary: { label: '小学', grades: [1, 2, 3, 4, 5, 6] },
        junior: { label: '初中', grades: [7, 8, 9] },
        senior: { label: '高中', grades: [10, 11, 12] },
      },
      /** 纳入覆盖审计的学科（不含音体美） */
      includedSubjects: [
        'chinese', 'math', 'science', 'english', 'politics', 'psychology',
        'biology', 'physics', 'chemistry', 'history', 'geography', 'info-tech', 'cs',
      ],
      excludedSubjects: ['art', 'pe', 'music', 'design', 'physical-education'],
    },
  };

  global.resolveEngineScript = function resolveEngineScript(name) {
    return `${global.PBL_MAP_CONFIG.scriptsBase}/${name}`;
  };
})(typeof window !== 'undefined' ? window : globalThis);
