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
    primary: '小学',
    junior: '初中',
    senior: '高中',
    university: '大学',
    adult: '成人',
  };
  const base = maps[projectSpec.gradeLevel] || projectSpec.gradeLevel;
  const details = normalizeGradeDetails(projectSpec);
  const lock = projectSpec.lockGradeBand !== false ? '｜锁学段' : '';
  if (details.length === 1) return `G${details[0]}${lock}`;
  if (details.length > 1) {
    const sorted = [...details].sort((a, b) => a - b);
    return `G${sorted.join('/')}(${base})${lock}`;
  }
  return `${base}${lock}`;
}
