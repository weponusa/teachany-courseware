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

  function formatGradeLabel(spec) {
    if (!spec || spec.gradeLevel === 'any' || !spec.gradeLevel) return '';
    const base = GRADE_OPTIONS.find(g => g.id === spec.gradeLevel)?.label || spec.gradeLevel;
    if (spec.gradeDetail) return `${base} · ${spec.gradeDetail}年级`;
    return base;
  }

  function normalizeProjectSpec(raw) {
    const s = raw || {};
    return {
      gradeLevel: s.gradeLevel || 'any',
      gradeDetail: s.gradeDetail || '',
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
    const lines = [];
    const grade = formatGradeLabel(s);
    if (grade) lines.push(`【学段】${grade}`);
    const subj = s.subject === 'cross'
      ? '跨学科'
      : (SUBJECT_OPTIONS.find(o => o.id === s.subject)?.label || s.subject);
    lines.push(`【学科】${subj}`);
    lines.push(`【任务】${s.task}`);
    const deliv = s.deliverable === 'other' && s.deliverableCustom
      ? s.deliverableCustom
      : (DELIVERABLE_LABELS[s.deliverable] || s.deliverable);
    lines.push(`【产出】${deliv}`);
    if (s.audience) lines.push(`【受众/场景】${s.audience}`);
    if (s.duration) lines.push(`【周期】${s.duration}`);
    if (s.constraints) lines.push(`【约束】${s.constraints}`);
    return lines.join('\n');
  }

  function readProjectSpecFromDOM() {
    const gradeLevel = document.getElementById('pblGradeLevel')?.value || 'any';
    const gradeDetail = document.getElementById('pblGradeDetail')?.value || '';
    const subject = document.getElementById('pblSubject')?.value || 'cross';
    const task = document.getElementById('pblTaskInput')?.value?.trim() || '';
    const deliverable = document.getElementById('pblDeliverable')?.value || 'report';
    const deliverableCustom = document.getElementById('pblDeliverableCustom')?.value?.trim() || '';
    const audience = document.getElementById('pblAudience')?.value?.trim() || '';
    const duration = document.getElementById('pblDuration')?.value?.trim() || '';
    const constraints = document.getElementById('pblConstraints')?.value?.trim() || '';
    return normalizeProjectSpec({
      gradeLevel, gradeDetail, subject, task, deliverable,
      deliverableCustom, audience, duration, constraints,
    });
  }

  function fillProjectSpecToDOM(spec) {
    const s = normalizeProjectSpec(spec);
    const set = (id, val) => { const el = document.getElementById(id); if (el) el.value = val; };
    set('pblGradeLevel', s.gradeLevel);
    set('pblGradeDetail', s.gradeDetail);
    set('pblSubject', s.subject);
    set('pblTaskInput', s.task);
    set('pblDeliverable', s.deliverable);
    set('pblDeliverableCustom', s.deliverableCustom);
    set('pblAudience', s.audience);
    set('pblDuration', s.duration);
    set('pblConstraints', s.constraints);
    if (typeof updatePBLGradeDetailOptions === 'function') updatePBLGradeDetailOptions();
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
    normalizeProjectSpec,
    composeGoalFromSpec,
    readProjectSpecFromDOM,
    fillProjectSpecToDOM,
    gradeDetailOptionsFor,
  };
})(typeof window !== 'undefined' ? window : globalThis);
