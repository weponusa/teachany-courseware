/**
 * PBL 通用支撑模块：评价量规、学习旅程、知识工具包、学生手册骨架
 * 不绑定单一项目类型，由拆解结果（goal / pathPlan / 图谱主线）动态填充
 */
(function (global) {
  'use strict';

  const TEMPLATE_URL = './data/pbl/modules/support-pack.json';
  const SUBJECT_LABELS = {
    math: '数学', physics: '物理', chemistry: '化学', biology: '生物', science: '科学',
    chinese: '语文', english: '英语', history: '历史', geography: '地理',
    politics: '道法', psychology: '心理', 'info-tech': '信息技术',
  };

  function esc(s) {
    const d = document.createElement('div');
    d.textContent = String(s ?? '');
    return d.innerHTML;
  }

  function fill(tpl, vars) {
    return String(tpl || '').replace(/\{\{(\w+)\}\}/g, (_, k) => vars[k] ?? '');
  }

  function inferPracticeLabel(goal, template) {
    const g = String(goal || '');
    for (const sig of template.practiceSignals || []) {
      if (new RegExp(sig.pattern, 'i').test(g)) {
        return (template.practiceLabels || {})[sig.labelKey] || template.practiceLabels?.default || '探究与实践';
      }
    }
    return template.practiceLabels?.default || '探究与实践';
  }

  function inferDeliverable(result) {
    const bp = result?.projectBlueprint;
    const spec = result?.projectSpec;
    if (spec?.deliverableCustom) return String(spec.deliverableCustom).trim();
    if (bp?.deliverable) return String(bp.deliverable).trim();
    const phases = bp?.schemes?.[0]?.phases || result?.pathPlan?.phases || [];
    const last = phases[phases.length - 1];
    if (last?.deliverable) return String(last.deliverable).trim();
    return '项目成果报告';
  }

  function inferWeekCount(result) {
    const dur = String(result?.projectSpec?.duration || '').trim();
    const m = dur.match(/(\d+)\s*周/);
    if (m) return Math.max(2, parseInt(m[1], 10));
    const phaseCount = result?.pathPlan?.phases?.length
      || bpPhaseCount(result)
      || 4;
    return Math.max(phaseCount, 3);
  }

  function bpPhaseCount(result) {
    const s = result?.projectBlueprint?.schemes?.find(x => x.id === result.projectBlueprint.recommendedSchemeId)
      || result?.projectBlueprint?.schemes?.[0];
    return s?.phases?.length || 0;
  }

  function inferDrivingQuestion(result) {
    const bp = result?.projectBlueprint;
    if (bp?.drivingQuestion) return String(bp.drivingQuestion).trim();
    const goal = String(result?.goal || '').replace(/^[^｜|]+[｜|]\s*/, '').trim();
    return goal ? `如何围绕「${goal.slice(0, 60)}」完成可核查的项目成果？` : '';
  }

  function gradeLabel(node) {
    if (!node) return '';
    if (node.gradeLabel) return node.gradeLabel;
    const g = parseInt(node.grade, 10);
    if (!g) return '';
    if (g <= 6) return `小学${g}年级`;
    if (g <= 9) return `初中${g - 6}年级`;
    if (g <= 12) return `高中${g - 9}年级`;
    return `G${g}`;
  }

  function sceneForNode(node, pathPlan) {
    if (!node) return '';
    for (const p of pathPlan?.phases || []) {
      const scenes = p.knowledgeScenes || [];
      const hit = scenes.find(s => s.name === node.name);
      if (hit?.sceneUse) return hit.sceneUse;
    }
    return node.matchReason || node.definition || node.taskSnippet || '';
  }

  function courseUrl(course) {
    if (!course) return '';
    if (course.url) return course.url;
    if (course.path) return `./community/${course.id}/index.html`;
    if (course.id) return `./community/${course.id}/index.html`;
    return '';
  }

  function resolveCourses(node) {
    const out = [];
    const seen = new Set();
    const push = (c) => {
      if (!c?.id || seen.has(c.id)) return;
      seen.add(c.id);
      out.push({ id: c.id, title: c.title || c.name || c.id, url: courseUrl(c) });
    };
    (node.courses || []).forEach(c => push(c));
    if (global.TeachAnyHub && typeof global.TeachAnyHub.getAllCoursesForNode === 'function') {
      try { global.TeachAnyHub.getAllCoursesForNode(node.id).forEach(push); } catch (_e) { /* skip */ }
    }
    return out.slice(0, 3);
  }

  class PBLSupportModules {
    constructor() {
      this._template = null;
      this._loadPromise = null;
    }

    async loadTemplate() {
      if (this._template) return this._template;
      if (this._loadPromise) return this._loadPromise;
      this._loadPromise = fetch(`${TEMPLATE_URL}?t=${Date.now()}`)
        .then(r => {
          if (!r.ok) throw new Error(`support-pack ${r.status}`);
          return r.json();
        })
        .then(j => {
          this._template = j;
          return j;
        })
        .catch(e => {
          console.warn('[PBL] 支撑模块模板加载失败，使用内置兜底:', e.message);
          this._template = this._fallbackTemplate();
          return this._template;
        });
      return this._loadPromise;
    }

    _fallbackTemplate() {
      return {
        version: 1,
        rubric: { grades: ['A', 'B', 'C', 'D'], gradeLabels: {}, dimensions: [] },
        roles: [],
        handbook: { progressChecks: [], reportSections: [], dataLogColumns: [], peerReviewCriteria: [] },
        practiceLabels: { default: '探究与实践' },
        practiceSignals: [],
      };
    }

    buildPack(result, options = {}) {
      const template = options.template || this._template;
      if (!template || !result) return null;

      const goal = String(result.goal || '').trim();
      const goalShort = goal.replace(/^[^｜|]+[｜|]\s*/, '').slice(0, 80);
      const deliverable = inferDeliverable(result);
      const practiceLabel = inferPracticeLabel(goal, template);
      const vars = { goal, goalShort, deliverable, practiceLabel, phaseCount: String(result.pathPlan?.phases?.length || 0) };

      const pathPlan = result.pathPlan
        || (global.PBLPathBuilder?.buildPathPlanFromResult?.(result) ?? null);
      const mainline = this._mainlineNodes(result);
      const weeks = inferWeekCount({ ...result, pathPlan });

      return {
        version: template.version,
        goal,
        deliverable,
        drivingQuestion: inferDrivingQuestion(result),
        practiceLabel,
        timeline: this._buildTimeline(pathPlan, weeks, vars),
        formativeChecks: this._buildFormativeChecks(pathPlan, deliverable),
        knowledgeToolkit: this._buildKnowledgeToolkit(mainline, pathPlan, goal),
        rubric: this._buildRubric(template, vars),
        roles: this._buildRoles(template, vars),
        handbook: this._buildHandbook(template, pathPlan, vars),
        meta: {
          weekCount: weeks,
          phaseCount: pathPlan?.phases?.length || 0,
          mainlineCount: mainline.length,
        },
      };
    }

    _mainlineNodes(result) {
      const nodes = result?.graphData?.nodes || [];
      return nodes.filter(n => n?.pathStep).sort((a, b) => (a.pathStep || 99) - (b.pathStep || 99));
    }

    _buildTimeline(pathPlan, weeks, vars) {
      const phases = pathPlan?.phases || [];
      if (!phases.length) {
        return [{ week: 1, label: '项目启动', summary: `明确目标：${vars.goalShort}` }];
      }
      const items = [];
      phases.forEach((p, i) => {
        const weekStart = Math.floor((i * weeks) / phases.length) + 1;
        const weekEnd = Math.floor(((i + 1) * weeks) / phases.length) || weekStart;
        const weekLabel = weekStart === weekEnd ? `第 ${weekStart} 周` : `第 ${weekStart}–${weekEnd} 周`;
        const steps = (p.pathSteps || []).filter(Boolean);
        const stepRef = steps.length ? `（图谱 ${steps.join('、')}）` : '';
        items.push({
          week: weekStart,
          weekRange: weekLabel,
          phaseIndex: p.phaseIndex || i + 1,
          phase: p.phase || `阶段 ${i + 1}`,
          summary: `${p.phase || ''}${stepRef}`,
          deliverable: p.deliverable || '',
          tasks: (p.steps || []).slice(0, 4),
        });
      });
      return items;
    }

    _buildFormativeChecks(pathPlan, deliverable) {
      const phases = pathPlan?.phases || [];
      const checks = [{ when: '项目启动', item: '确认驱动性问题、分工与数据采集计划' }];
      phases.forEach((p, i) => {
        const acc = (p.acceptance || [])[0];
        checks.push({
          when: `阶段 ${p.phaseIndex || i + 1} 结束 · ${p.phase || ''}`,
          item: acc || `提交本阶段产出：${p.deliverable || deliverable}`,
        });
      });
      checks.push({ when: '终期展示前', item: `交付物「${deliverable}」定稿 + 同伴互评 + 答辩彩排` });
      return checks;
    }

    _buildKnowledgeToolkit(mainline, pathPlan, goal) {
      return mainline.map((n, i) => ({
        index: n.pathStep || i + 1,
        id: n.id,
        name: n.name,
        subject: SUBJECT_LABELS[n.subject] || n.subject || '',
        grade: gradeLabel(n),
        scene: sceneForNode(n, pathPlan),
        courses: resolveCourses(n),
      }));
    }

    _buildRubric(template, vars) {
      const dims = (template.rubric?.dimensions || []).map(d => ({
        id: d.id,
        name: fill(d.name, vars),
        weight: d.weight,
        levels: Object.fromEntries(
          (template.rubric?.grades || ['A', 'B', 'C', 'D']).map(g => [g, fill(d.levels?.[g] || '', vars)])
        ),
      }));
      return {
        grades: template.rubric?.grades || ['A', 'B', 'C', 'D'],
        gradeLabels: template.rubric?.gradeLabels || {},
        dimensions: dims,
        totalWeight: dims.reduce((s, d) => s + (d.weight || 0), 0),
      };
    }

    _buildRoles(template, vars) {
      return (template.roles || []).map(r => ({
        icon: r.icon,
        title: r.title,
        duty: fill(r.duty, vars),
      }));
    }

    _buildHandbook(template, pathPlan, vars) {
      const hb = template.handbook || {};
      const phaseChecks = (pathPlan?.phases || []).map((p, i) =>
        `阶段 ${p.phaseIndex || i + 1}「${p.phase || ''}」产出已达标：${p.deliverable || '—'}`
      );
      return {
        progressChecks: [...(hb.progressChecks || []).slice(0, 2), ...phaseChecks, ...(hb.progressChecks || []).slice(4)],
        reportSections: hb.reportSections || [],
        dataLogColumns: hb.dataLogColumns || [],
        peerReviewCriteria: hb.peerReviewCriteria || [],
        goals: [
          `能运用项目相关知识解决「${vars.goalShort}」中的真实问题`,
          '能收集、整理过程证据并用课标方法分析',
          `能完成交付物「${vars.deliverable}」并做有依据的展示`,
        ],
      };
    }

    renderHTML(pack) {
      if (!pack) return '';
      const parts = [];
      parts.push(this._renderSectionNav());
      parts.push(this._renderToolkit(pack));
      parts.push(this._renderTimeline(pack));
      parts.push(this._renderRubric(pack));
      parts.push(this._renderHandbook(pack));
      return `<div class="pbl-support-pack">${parts.join('')}</div>`;
    }

    _renderSectionNav() {
      const items = [
        { id: 'pbl-sp-toolkit', label: '📚 知识工具包' },
        { id: 'pbl-sp-journey', label: '🗓️ 学习旅程' },
        { id: 'pbl-sp-rubric', label: '📋 评价量规' },
        { id: 'pbl-sp-handbook', label: '📘 学生手册' },
      ];
      const links = items.map(i => `<a href="#${i.id}">${i.label}</a>`).join('');
      return `<nav class="pbl-sp-nav" aria-label="项目支撑模块">${links}</nav>`;
    }

    _renderToolkit(pack) {
      const items = pack.knowledgeToolkit || [];
      if (!items.length) {
        return `<section class="pbl-sp-section" id="pbl-sp-toolkit"><h3>📚 知识工具包</h3>
          <p class="pbl-sp-hint">完成课标匹配后，图谱主线节点（角标 1、2、3…）将在此列出，并附上场景说明与 TeachAny 课件链接。</p></section>`;
      }
      let cards = items.map(k => {
        const courseBtns = (k.courses || []).map(c =>
          c.url ? `<a class="pbl-sp-course" href="${esc(c.url)}" target="_blank" rel="noopener">📖 ${esc(c.title)}</a>` : ''
        ).join('');
        return `<article class="pbl-sp-tool-card">
          <div class="pbl-sp-tool-head"><span class="pbl-sp-tool-idx">${k.index}</span>
            <div><strong>${esc(k.name)}</strong>
            <div class="pbl-sp-tool-meta">${esc([k.grade, k.subject].filter(Boolean).join(' · '))}</div></div></div>
          ${k.scene ? `<p class="pbl-sp-tool-scene">${esc(k.scene)}</p>` : ''}
          ${courseBtns ? `<div class="pbl-sp-tool-courses">${courseBtns}</div>` : ''}
        </article>`;
      }).join('');
      return `<section class="pbl-sp-section" id="pbl-sp-toolkit"><h3>📚 知识工具包</h3>
        <p class="pbl-sp-hint">序号与图谱节点角标一致；优先通过 TeachAny 课件完成各知识点学习。</p>
        <div class="pbl-sp-tool-grid">${cards}</div></section>`;
    }

    _renderTimeline(pack) {
      const tl = pack.timeline || [];
      const checks = pack.formativeChecks || [];
      if (!tl.length) {
        return `<section class="pbl-sp-section" id="pbl-sp-journey"><h3>🗓️ 学习旅程与形成性评价</h3>
          <p class="pbl-sp-hint">拆解完成后将按项目阶段自动生成周次时间线与形成性评价检查点。</p></section>`;
      }
      const rows = tl.map(t => `<li class="pbl-sp-timeline-item">
        <span class="pbl-sp-week">${esc(t.weekRange)}</span>
        <div><strong>阶段 ${t.phaseIndex} · ${esc(t.phase)}</strong>
        ${t.deliverable ? `<div class="pbl-sp-dim">产出：${esc(t.deliverable)}</div>` : ''}
        <ul class="pbl-sp-task-list">${(t.tasks || []).map(x => `<li>${esc(x)}</li>`).join('')}</ul></div>
      </li>`).join('');
      const checkRows = checks.map(c => `<li><strong>${esc(c.when)}</strong> — ${esc(c.item)}</li>`).join('');
      return `<section class="pbl-sp-section" id="pbl-sp-journey"><h3>🗓️ 学习旅程与形成性评价</h3>
        ${pack.drivingQuestion ? `<p class="pbl-sp-dq"><strong>驱动性问题：</strong>${esc(pack.drivingQuestion)}</p>` : ''}
        <ol class="pbl-sp-timeline">${rows}</ol>
        <h4>形成性评价节点</h4><ul class="pbl-sp-checks">${checkRows}</ul></section>`;
    }

    _renderRubric(pack) {
      const r = pack.rubric;
      if (!r?.dimensions?.length) {
        return `<section class="pbl-sp-section" id="pbl-sp-rubric"><h3>📋 多维度项目评价量规</h3>
          <p class="pbl-sp-hint">量规模板加载中或暂不可用，请刷新页面后重试。</p></section>`;
      }
      const gradeHead = (r.grades || []).map(g =>
        `<th>${esc(r.gradeLabels?.[g] || g)}</th>`
      ).join('');
      const rows = r.dimensions.map(d => `<tr>
        <td><strong>${esc(d.name)}</strong><div class="pbl-sp-dim">${d.weight}%</div></td>
        ${(r.grades || []).map(g => `<td>${esc(d.levels?.[g] || '')}</td>`).join('')}
      </tr>`).join('');
      const scoreRows = r.dimensions.map(d =>
        `<tr><td>${esc(d.name)}</td><td>____ / ${d.weight}</td></tr>`
      ).join('');
      return `<section class="pbl-sp-section" id="pbl-sp-rubric"><h3>📋 多维度项目评价量规</h3>
        <p class="pbl-sp-hint">适用于各类 PBL；教师可按项目微调权重。实践维度当前为：${esc(pack.practiceLabel)}。</p>
        <div class="pbl-sp-table-wrap"><table class="pbl-sp-rubric-table">
          <thead><tr><th>维度</th>${gradeHead}</tr></thead><tbody>${rows}</tbody></table></div>
        <h4>评分汇总卡</h4>
        <table class="pbl-sp-score-card"><tbody>${scoreRows}
        <tr class="pbl-sp-total"><td><strong>总分</strong></td><td>____ / ${r.totalWeight || 100}</td></tr></tbody></table></section>`;
    }

    _renderHandbook(pack) {
      const hb = pack.handbook || {};
      const roles = (pack.roles || []).map(r =>
        `<tr><td>${r.icon} ${esc(r.title)}</td><td>${esc(r.duty)}</td><td class="pbl-sp-fill">________</td></tr>`
      ).join('');
      const checks = (hb.progressChecks || []).map(c =>
        `<label class="pbl-sp-check"><input type="checkbox" disabled /> ${esc(c)}</label>`
      ).join('');
      const sections = (hb.reportSections || []).map(s =>
        `<div class="pbl-sp-report-sec"><strong>${esc(s.title)}</strong>
        <div class="pbl-sp-dim">${esc(s.hint)}</div>
        <div class="pbl-sp-textarea" contenteditable="true" data-placeholder="在此撰写…"></div></div>`
      ).join('');
      const cols = hb.dataLogColumns || [];
      const dataHead = cols.map(c => `<th>${esc(c)}</th>`).join('');
      const dataRows = [1, 2, 3, 4, 5].map(() =>
        `<tr>${cols.map(() => `<td class="pbl-sp-fill">&nbsp;</td>`).join('')}</tr>`
      ).join('');
      const peerHead = (hb.peerReviewCriteria || []).map(c => `<th>${esc(c.name)} (/${c.max})</th>`).join('');
      const peerRow = `<tr><td class="pbl-sp-fill">被评成员</td>${(hb.peerReviewCriteria || []).map(() => `<td class="pbl-sp-fill"></td>`).join('')}<td class="pbl-sp-fill">总分</td><td class="pbl-sp-fill">评语</td></tr>`;

      return `<section class="pbl-sp-section" id="pbl-sp-handbook"><h3>📘 学生项目手册（可填写骨架）</h3>
        <p class="pbl-sp-hint">导出网页后可打印；文本框支持直接填写（浏览器本地保存需自行复制）。</p>
        <h4>项目目标</h4><ul>${(hb.goals || []).map(g => `<li>${esc(g)}</li>`).join('')}</ul>
        <h4>小组分工</h4>
        <table class="pbl-sp-role-table"><thead><tr><th>角色</th><th>职责</th><th>负责人</th></tr></thead><tbody>${roles}</tbody></table>
        <h4>进度自检</h4><div class="pbl-sp-check-grid">${checks}</div>
        <h4>过程数据采集表</h4>
        <table class="pbl-sp-data-table"><thead><tr>${dataHead}</tr></thead><tbody>${dataRows}</tbody></table>
        <h4>报告撰写区</h4>${sections}
        <h4>同伴互评</h4>
        <table class="pbl-sp-peer-table"><thead><tr><th>成员</th>${peerHead}<th>总分/100</th><th>评语</th></tr></thead><tbody>${peerRow}${peerRow}${peerRow}</tbody></table>
      </section>`;
    }

    async buildAndRender(result) {
      await this.loadTemplate();
      const pack = this.buildPack(result);
      return { pack, html: this.renderHTML(pack) };
    }
  }

  global.PBLSupportModules = new PBLSupportModules();
})(typeof window !== 'undefined' ? window : globalThis);
