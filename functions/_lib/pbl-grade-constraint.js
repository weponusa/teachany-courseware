/**
 * @internal 共享：从 projectSpec 格式化年级/学段约束（支持多年级多选）
 */

export function normalizeGradeDetails(projectSpec) {
  if (!projectSpec) return [];
  if (Array.isArray(projectSpec.gradeDetails) && projectSpec.gradeDetails.length) {
    return projectSpec.gradeDetails.map(g => parseInt(g, 10)).filter(g => g >= 1 && g <= 12);
  }
  const single = parseInt(projectSpec.gradeDetail, 10);
  return single >= 1 && single <= 12 ? [single] : [];
}

export function formatGradeConstraint(projectSpec) {
  if (!projectSpec?.gradeLevel || projectSpec.gradeLevel === 'any') return '';
  const maps = {
    primary: '小学（1–6 年级）',
    junior: '初中（7–9 年级）',
    senior: '高中（10–12 年级）',
    university: '大学/高等教育',
    adult: '成人/在职学习者',
  };
  const base = maps[projectSpec.gradeLevel] || projectSpec.gradeLevel;
  const details = normalizeGradeDetails(projectSpec);
  if (details.length === 1) {
    return `${details[0]} 年级（锁定当前学段，不选更低学段课）`;
  }
  if (details.length > 1) {
    const sorted = [...details].sort((a, b) => a - b);
    return `${sorted.join('、')} 年级（锁定当前学段，不选更低学段课）`;
  }
  const lock = projectSpec.lockGradeBand !== false ? '（锁定学段，不跨学段、不选更低学段课）' : '';
  return `${base}${lock}`;
}
