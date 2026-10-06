/**
 * 学生自主 PBL 表单 — 「主题壳 + 驱动问」双栏，合成 goal 时学生问句优先
 */
(function (global) {
  const WHY_MIN = 4;
  const DQ_PATTERN = /[？?]/;

  function normalizeStudentSpec(raw) {
    const s = raw || {};
    return {
      themeShellId: String(s.themeShellId || '').trim(),
      themeShell: String(s.themeShell || '').trim(),
      themeCompetencies: Array.isArray(s.themeCompetencies) ? s.themeCompetencies : [],
      themeConstraints: String(s.themeConstraints || '').trim(),
      themeDuration: String(s.themeDuration || '').trim(),
      drivingQuestion: String(s.drivingQuestion || '').trim(),
      whyCare: String(s.whyCare || '').trim(),
      outputIntent: String(s.outputIntent || '').trim(),
      studentName: String(s.studentName || '').trim(),
      interestTags: Array.isArray(s.interestTags) ? s.interestTags : [],
      gradeLevel: s.gradeLevel || 'primary',
      gradeDetails: Array.isArray(s.gradeDetails) ? s.gradeDetails.map(String) : [],
      subjects: Array.isArray(s.subjects) ? s.subjects : [],
      deliverable: s.deliverable || 'report',
      deliverableCustom: String(s.deliverableCustom || '').trim(),
    };
  }

  function validateDrivingQuestion(q) {
    const text = String(q || '').trim();
    if (text.length < 8) return { ok: false, msg: '驱动性问题至少 8 个字' };
    if (!DQ_PATTERN.test(text)) return { ok: false, msg: '驱动性问题须以 ？ 或 ? 结尾' };
    return { ok: true };
  }

  function validateStudentSpec(spec) {
    const s = normalizeStudentSpec(spec);
    const errors = [];
    if (!s.themeShell) errors.push('需要教师发布的主题壳');
    const dq = validateDrivingQuestion(s.drivingQuestion);
    if (!dq.ok) errors.push(dq.msg);
    if (s.whyCare.length < WHY_MIN) errors.push('请用 1–2 句话说明「我为什么关心这个」');
    if (!s.outputIntent) errors.push('请描述你想做出的东西');
    return { ok: errors.length === 0, errors, spec: s };
  }

  /**
   * 合成拆解用 goal：学生驱动问权重最高，主题壳定边界
   */
  function composeGoalFromStudentSpec(spec) {
    const s = normalizeStudentSpec(spec);
    const parts = [];

    if (s.gradeLevel === 'primary') {
      const gd = s.gradeDetails?.length ? `${s.gradeDetails.join('、')}年级` : '小学';
      parts.push(gd);
    } else if (s.gradeLevel === 'junior') {
      parts.push(s.gradeDetails?.length ? `初中${s.gradeDetails.join('、')}年级` : '初中');
    } else if (s.gradeLevel === 'senior') {
      parts.push(s.gradeDetails?.length ? `高中${s.gradeDetails.join('、')}年级` : '高中');
    }

    parts.push(`主题:${s.themeShell}`);
    parts.push(`驱动问:${s.drivingQuestion}`);
    parts.push(`产出意向:${s.outputIntent}`);

    if (s.whyCare) parts.push(`兴趣:${s.whyCare}`);
    if (s.interestTags.length) parts.push(`标签:${s.interestTags.join('、')}`);
    if (s.themeConstraints) parts.push(`约束:${s.themeConstraints}`);
    if (s.themeDuration) parts.push(`周期:${s.themeDuration}`);

    const deliv = s.deliverable === 'other' && s.deliverableCustom
      ? s.deliverableCustom
      : (global.PBLProjectForm?.DELIVERABLE_LABELS?.[s.deliverable] || s.deliverable);
    parts.push(`产出:${deliv}`);

    return parts.join('｜');
  }

  /**
   * 转为 TeachAny projectSpec（task 保留学生原话组合，不用教师示例）
   */
  function toProjectSpec(spec) {
    const s = normalizeStudentSpec(spec);
    const task = [s.drivingQuestion, s.outputIntent ? `我想做出：${s.outputIntent}` : '']
      .filter(Boolean)
      .join('；');

    return {
      gradeLevel: s.gradeLevel,
      gradeDetails: s.gradeDetails,
      lockGradeBand: true,
      subject: 'cross',
      subjects: [],
      task,
      deliverable: s.deliverable,
      deliverableCustom: s.deliverableCustom,
      audience: s.themeShell,
      duration: s.themeDuration,
      constraints: s.themeConstraints,
      knowledgeSources: { curriculum: true, k12Graph: true, fullGraph: false },
      curriculumSystems: ['cn'],
    };
  }

  function readStudentFormFromDOM(prefix = 'student') {
    const val = (id) => document.getElementById(`${prefix}-${id}`)?.value?.trim() || '';
    const tagsRaw = document.getElementById(`${prefix}-interestTags`)?.value || '';
    const gradeBoxes = document.querySelectorAll(`input[name="${prefix}-gradeDetail"]:checked`);
    return normalizeStudentSpec({
      themeShellId: val('themeShellId'),
      themeShell: val('themeShell'),
      themeConstraints: val('themeConstraints'),
      themeDuration: val('themeDuration'),
      drivingQuestion: val('drivingQuestion'),
      whyCare: val('whyCare'),
      outputIntent: val('outputIntent'),
      studentName: val('studentName'),
      interestTags: tagsRaw.split(/[,，、\s]+/).filter(Boolean),
      gradeLevel: document.getElementById(`${prefix}-gradeLevel`)?.value || 'primary',
      gradeDetails: [...gradeBoxes].map((el) => el.value),
      deliverable: document.getElementById(`${prefix}-deliverable`)?.value || 'report',
      deliverableCustom: val('deliverableCustom'),
    });
  }

  function fillInspirationChip(chipEl, targetId) {
    const text = chipEl?.dataset?.inspiration || chipEl?.textContent || '';
    const el = document.getElementById(targetId);
    if (el && text) {
      el.value = text;
      el.dispatchEvent(new Event('input', { bubbles: true }));
    }
  }

  function saveThemeShell(shell) {
    const key = global.PBL_MAP_CONFIG?.storageKeys?.themeShells || 'pblmap_theme_shells_v1';
    try {
      const list = JSON.parse(localStorage.getItem(key) || '[]');
      const item = { ...shell, id: shell.id || `shell-${Date.now()}`, createdAt: Date.now() };
      list.unshift(item);
      localStorage.setItem(key, JSON.stringify(list.slice(0, 50)));
      return item;
    } catch (_e) {
      return null;
    }
  }

  function loadThemeShells() {
    const key = global.PBL_MAP_CONFIG?.storageKeys?.themeShells || 'pblmap_theme_shells_v1';
    try {
      return JSON.parse(localStorage.getItem(key) || '[]');
    } catch (_e) {
      return [];
    }
  }

  global.PBLStudentForm = {
    normalizeStudentSpec,
    validateDrivingQuestion,
    validateStudentSpec,
    composeGoalFromStudentSpec,
    toProjectSpec,
    readStudentFormFromDOM,
    fillInspirationChip,
    saveThemeShell,
    loadThemeShells,
  };
})(typeof window !== 'undefined' ? window : globalThis);
