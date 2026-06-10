/**
 * PBL 结构化项目描述 — 学段 / 学科 / 任务 / 产出
 */
(function (global) {
  const SUBJECT_OPTIONS = [
    { id: 'cross', label: '跨学科（默认）' },
    { id: 'math', label: '数学' },
    { id: 'physics', label: '物理' },
    { id: 'chemistry', label: '化学' },
    { id: 'biology', label: '生物' },
    { id: 'science', label: '科学' },
    { id: 'chinese', label: '语文' },
    { id: 'english', label: '英语' },
    { id: 'history', label: '历史' },
    { id: 'geography', label: '地理' },
    { id: 'info-tech', label: '信息技术' },
    { id: 'art', label: '艺术' },
  ];

  const GRADE_OPTIONS = [
    { id: 'any', label: '跨学段（不限）' },
    { id: 'primary', label: '小学' },
    { id: 'junior', label: '初中' },
    { id: 'senior', label: '高中' },
    { id: 'university', label: '大学' },
    { id: 'adult', label: '成人/在职' },
  ];

  const PRIMARY_GRADES = [1, 2, 3, 4, 5, 6].map(n => ({ id: String(n), label: `${n} 年级` }));
  const JUNIOR_GRADES = [7, 8, 9].map(n => ({ id: String(n), label: `${n} 年级` }));
  const SENIOR_GRADES = [10, 11, 12].map(n => ({ id: String(n), label: `高${n - 9}` }));

  const DELIVERABLE_OPTIONS = [
    { id: 'report', label: '研究报告 / 调查报告' },
    { id: 'decision-table', label: '决策对比表 / 方案比选' },
    { id: 'engineering-prototype', label: '工程作品 / 可运行原型' },
    { id: 'experiment-report', label: '实验报告 / 探究记录' },
    { id: 'design-proposal', label: '设计方案 / 策划案' },
    { id: 'presentation', label: '演示文稿 / 展板 / 讲解' },
    { id: 'app-software', label: '应用 / 程序 / 网站' },
    { id: 'handwork-model', label: '手工作品 / 实体模型' },
    { id: 'portfolio', label: '作品集 / 创作集' },
    { id: 'plan-schedule', label: '计划书 / 路线与预算' },
    { id: 'other', label: '其他（自定义）' },
  ];

  const DELIVERABLE_LABELS = Object.fromEntries(DELIVERABLE_OPTIONS.map(o => [o.id, o.label]));

  function normalizeGradeDetails(s) {
    if (Array.isArray(s.gradeDetails) && s.gradeDetails.length) {
      return s.gradeDetails.map(String).filter(Boolean);
    }
    if (s.gradeDetail) return [String(s.gradeDetail)];
    return [];
  }

  function formatGradeLabel(spec) {
    if (!spec || spec.gradeLevel === 'any' || !spec.gradeLevel) return '';
    const base = GRADE_OPTIONS.find(g => g.id === spec.gradeLevel)?.label || spec.gradeLevel;
    const details = normalizeGradeDetails(spec);
    if (details.length === 1) return `${base} · ${details[0]}年级`;
    if (details.length > 1) {
      const sorted = details.map(d => parseInt(d, 10)).filter(n => n >= 1 && n <= 12).sort((a, b) => a - b);
      return `${base} · ${sorted.join('、')}年级`;
    }
    return base;
  }

  function normalizeKnowledgeSources(raw) {
    const src = raw?.knowledgeSources || raw || {};
    return {
      curriculum: src.curriculum !== false,
      k12Graph: src.k12Graph !== false,
    };
  }

  function normalizeProjectSpec(raw) {
    const s = raw || {};
    const gradeDetails = normalizeGradeDetails(s);
    return {
      gradeLevel: s.gradeLevel || 'any',
      gradeDetail: gradeDetails[0] || s.gradeDetail || '',
      gradeDetails,
      lockGradeBand: s.lockGradeBand !== false,
      knowledgeSources: normalizeKnowledgeSources(s),
      curriculumSystems: Array.isArray(s.curriculumSystems) ? s.curriculumSystems : [],
      subject: s.subject || 'cross',
      task: String(s.task || '').trim(),
      deliverable: s.deliverable || 'report',
      deliverableCustom: String(s.deliverableCustom || '').trim(),
      audience: String(s.audience || '').trim(),
      duration: String(s.duration || '').trim(),
      constraints: String(s.constraints || '').trim(),
    };
  }

  function composeGoalFromSpec(spec) {
    const s = normalizeProjectSpec(spec);
    if (!s.task) return '';
    const parts = [];
    const grade = formatGradeLabel(s);
    if (grade) parts.push(grade);
    const subj = s.subject === 'cross'
      ? '跨学科'
      : (SUBJECT_OPTIONS.find(o => o.id === s.subject)?.label || s.subject);
    parts.push(subj);
    parts.push(s.task);
    const deliv = s.deliverable === 'other' && s.deliverableCustom
      ? s.deliverableCustom
      : (DELIVERABLE_LABELS[s.deliverable] || s.deliverable);
    parts.push(`产出:${deliv}`);
    if (s.audience) parts.push(`场景:${s.audience}`);
    if (s.duration) parts.push(`周期:${s.duration}`);
    if (s.constraints) parts.push(`约束:${s.constraints}`);
    return parts.join('｜');
  }

  function readKnowledgeSourcesFromDOM() {
    const tags = document.querySelectorAll('.pbl-src-tag.active');
    const picked = [];
    tags.forEach(t => picked.push(t.dataset.source));
    if (!picked.length || picked.includes('all')) {
      return { curriculum: true, k12Graph: true };
    }
    return {
      curriculum: picked.includes('curriculum'),
      k12Graph: picked.includes('k12Graph'),
    };
  }

  function readCurriculumSystemsFromDOM() {
    if (typeof getSelectedSystems === 'function') return getSelectedSystems();
    return ['all'];
  }

  function readGradeDetailsFromDOM() {
    const boxes = document.querySelectorAll('input[name="pblGradeDetail"]:checked');
    return [...boxes].map(el => el.value).filter(Boolean);
  }

  function readProjectSpecFromDOM() {
    const gradeLevel = document.getElementById('pblGradeLevel')?.value || 'any';
    const gradeDetails = readGradeDetailsFromDOM();
    const lockGradeBand = document.getElementById('pblLockGradeBand')?.checked !== false;
    const subject = document.getElementById('pblSubject')?.value || 'cross';
    const task = document.getElementById('pblTaskInput')?.value?.trim() || '';
    const deliverable = document.getElementById('pblDeliverable')?.value || 'report';
    const deliverableCustom = document.getElementById('pblDeliverableCustom')?.value?.trim() || '';
    const audience = document.getElementById('pblAudience')?.value?.trim() || '';
    const duration = document.getElementById('pblDuration')?.value?.trim() || '';
    const constraints = document.getElementById('pblConstraints')?.value?.trim() || '';
    return normalizeProjectSpec({
      gradeLevel,
      gradeDetails,
      lockGradeBand,
      knowledgeSources: readKnowledgeSourcesFromDOM(),
      curriculumSystems: readCurriculumSystemsFromDOM(),
      subject, task, deliverable,
      deliverableCustom, audience, duration, constraints,
    });
  }

  function fillProjectSpecToDOM(spec) {
    const s = normalizeProjectSpec(spec);
    const set = (id, val) => { const el = document.getElementById(id); if (el) el.value = val; };
    set('pblGradeLevel', s.gradeLevel);
    set('pblSubject', s.subject);
    set('pblTaskInput', s.task);
    set('pblDeliverable', s.deliverable);
    set('pblDeliverableCustom', s.deliverableCustom);
    set('pblAudience', s.audience);
    set('pblDuration', s.duration);
    set('pblConstraints', s.constraints);
    const lockEl = document.getElementById('pblLockGradeBand');
    if (lockEl) lockEl.checked = s.lockGradeBand !== false;
    if (typeof updatePBLGradeDetailOptions === 'function') updatePBLGradeDetailOptions();
    const details = normalizeGradeDetails(s);
    document.querySelectorAll('input[name="pblGradeDetail"]').forEach(el => {
      el.checked = details.includes(el.value);
    });
    if (typeof fillPBLKnowledgeSourceTags === 'function') {
      fillPBLKnowledgeSourceTags(s.knowledgeSources);
    }
    if (typeof fillPBLSystemTags === 'function' && s.curriculumSystems?.length) {
      fillPBLSystemTags(s.curriculumSystems);
    }
    if (typeof togglePBLDeliverableCustom === 'function') togglePBLDeliverableCustom();
  }

  function gradeDetailOptionsFor(level) {
    if (level === 'primary') return PRIMARY_GRADES;
    if (level === 'junior') return JUNIOR_GRADES;
    if (level === 'senior') return SENIOR_GRADES;
    return [];
  }

  global.PBLProjectForm = {
    SUBJECT_OPTIONS,
    GRADE_OPTIONS,
    DELIVERABLE_OPTIONS,
    DELIVERABLE_LABELS,
    formatGradeLabel,
    normalizeGradeDetails,
    normalizeKnowledgeSources,
    normalizeProjectSpec,
    composeGoalFromSpec,
    readProjectSpecFromDOM,
    fillProjectSpecToDOM,
    gradeDetailOptionsFor,
  };
})(typeof window !== 'undefined' ? window : globalThis);
