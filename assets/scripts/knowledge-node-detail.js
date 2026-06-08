/**
 * 知识点属性页（tree / PBL / 全科图谱共用）
 * KnowledgeNodeDetail.render(container, node, options)
 */
(function (global) {
  'use strict';

  const STYLE_ID = 'knowledge-node-detail-styles';

  function escapeHtml(str) {
    if (str == null) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function injectStyles() {
    if (document.getElementById(STYLE_ID)) return;
    const style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent = [
      '.knd-en{font-size:13px;color:#94a3b8;margin:0 0 10px;}',
      '.knd-meta-row{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px;}',
      '.knd-meta-tag{padding:3px 10px;border-radius:6px;font-size:12px;background:rgba(79,143,255,0.1);color:#4f8fff;}',
      '.knd-definition{font-size:14px;color:#94a3b8;line-height:1.75;margin-bottom:14px;}',
      '.knd-section{margin-bottom:14px;}',
      '.knd-section h4{font-size:13px;color:#5a6880;margin:0 0 8px;font-weight:600;}',
      '.knd-tags{display:flex;flex-wrap:wrap;gap:4px;}',
      '.knd-tag{padding:2px 8px;border-radius:10px;font-size:11px;background:rgba(79,143,255,0.1);color:#4f8fff;}',
      '.knd-curriculum-item{margin:4px 0;padding:6px 8px;border-radius:4px;background:rgba(148,163,184,0.06);font-size:12px;color:#94a3b8;line-height:1.5;}',
      '.knd-link-tags{display:flex;flex-wrap:wrap;gap:4px;}',
      '.knd-link-tag{padding:4px 10px;border-radius:6px;font-size:12px;cursor:pointer;transition:background .2s;}',
      '.knd-link-tag.knd-prereq{background:rgba(168,85,247,0.12);color:#c084fc;}',
      '.knd-link-tag.knd-prereq:hover{background:rgba(168,85,247,0.22);}',
      '.knd-link-tag.knd-next{background:rgba(6,182,212,0.12);color:#22d3ee;}',
      '.knd-link-tag.knd-next:hover{background:rgba(6,182,212,0.22);}',
      '.knd-course-list{display:flex;flex-direction:column;gap:4px;max-height:200px;overflow-y:auto;}',
      '.knd-course-link{display:flex;align-items:center;gap:6px;padding:8px 10px;border-radius:6px;font-size:13px;color:#e8ecf4;text-decoration:none;background:rgba(148,163,184,0.08);transition:background .2s;}',
      '.knd-course-link:hover{background:rgba(148,163,184,0.16);}'
    ].join('');
    document.head.appendChild(style);
  }

  function gradeLabel(node) {
    if (node.grade === 0) return '大学';
    if (node.grade) return `${node.grade}年级`;
    return '';
  }

  function buildCoursewareSection(nodeId) {
    const hub = global.TeachAnyHub;
    if (!hub || typeof hub.getAllCoursesForNode !== 'function') return '';
    const courses = hub.getAllCoursesForNode(nodeId) || [];
    if (!courses.length) return '';

    const sourceIcon = {
      official: '📋',
      community_registry: '🔖',
      community_shared: '🌐',
      user: '📂',
    };

    const items = courses.map((c, idx) => {
      const url = c.url || (c.path ? `./${c.path}/index.html` : '');
      if (!url) return '';
      const icon = sourceIcon[c.source] || '📚';
      const likes = c.likes > 0 ? ` <span style="color:#f87171;">❤️${c.likes}</span>` : '';
      const crown = idx === 0 && courses.length > 1 ? ' <span style="color:#f59e0b;">👑</span>' : '';
      return `<a class="knd-course-link" href="${escapeHtml(url)}" target="_blank" rel="noopener">${icon} ${escapeHtml(c.name || c.id)}${likes}${crown}</a>`;
    }).filter(Boolean).join('');

    return items
      ? `<div class="knd-section"><h4>📖 已有课件${courses.length > 1 ? '（按 ❤️ 排序）' : ''}</h4><div class="knd-course-list">${items}</div></div>`
      : '';
  }

  function renderLinkTags(ids, getNodeById) {
    if (!ids || !ids.length) return '';
    return ids.map((id) => {
      const n = getNodeById ? getNodeById(id) : null;
      const name = n ? n.name : id;
      return `<span class="knd-link-tag" data-focus-node="${escapeHtml(id)}" role="button" tabindex="0">${escapeHtml(name)}</span>`;
    }).join('');
  }

  function render(container, node, opts) {
    if (!container || !node) return;
    injectStyles();
    opts = opts || {};

    const cfg = (opts.subjectConfig || {})[node.subject] || { label: node.subject, emoji: '📌', color: '#666' };
    const getDomainLabel = opts.getDomainLabel || ((d) => d);
    const meta = opts.meta || {};
    const hub = global.TeachAnyHub;
    const hasCourse = hub && typeof hub.hasAnyCourseware === 'function' && hub.hasAnyCourseware(node.id);

    const prereqIds = (opts.prerequisiteIds && opts.prerequisiteIds.length)
      ? opts.prerequisiteIds
      : (meta.prerequisites || node.prerequisites || []);
    const nextIds = (opts.nextIds && opts.nextIds.length)
      ? opts.nextIds
      : (meta.next_steps || node.next_steps || []);
    const keyConcepts = meta.key_concepts || node.key_concepts || node.skills || [];
    const points = node.curriculum_points || meta.curriculum_points || [];
    const related = meta.related_nodes || [];

    let html = `<h3>${escapeHtml(node.name)}</h3>`;
    if (node.name_en) html += `<p class="knd-en">${escapeHtml(node.name_en)}</p>`;

    html += '<div class="knd-meta-row">';
    html += `<span class="knd-meta-tag" style="background:${cfg.color}22;color:${cfg.color}">${cfg.emoji} ${escapeHtml(cfg.label)}</span>`;
    const gl = gradeLabel(node);
    if (gl) html += `<span class="knd-meta-tag">${escapeHtml(gl)}</span>`;
    if (node.domain) html += `<span class="knd-meta-tag">${escapeHtml(getDomainLabel(node.domain))}</span>`;
    html += hasCourse
      ? '<span class="knd-meta-tag" style="background:rgba(16,185,129,0.15);color:#10b981">✅ 有课件</span>'
      : '<span class="knd-meta-tag" style="background:rgba(239,68,68,0.15);color:#f87171">📝 待创建</span>';
    html += '</div>';

    const def = node.definition || meta.definition || '';
    if (def) html += `<p class="knd-definition">${escapeHtml(def)}</p>`;

    if (keyConcepts.length) {
      html += '<div class="knd-section"><h4>核心概念</h4><div class="knd-tags">';
      keyConcepts.forEach((k) => { html += `<span class="knd-tag">${escapeHtml(k)}</span>`; });
      html += '</div></div>';
    }

    if (points.length) {
      html += '<div class="knd-section"><h4>📖 课标原文要点</h4>';
      points.slice(0, 6).forEach((p) => { html += `<div class="knd-curriculum-item">${escapeHtml(p)}</div>`; });
      html += '</div>';
    }

    if (prereqIds.length) {
      html += `<div class="knd-section"><h4>📚 先修知识</h4><div class="knd-link-tags knd-prereq">${renderLinkTags(prereqIds, opts.getNodeById)}</div></div>`;
    }
    if (nextIds.length) {
      html += `<div class="knd-section"><h4>🚀 后续知识</h4><div class="knd-link-tags knd-next">${renderLinkTags(nextIds, opts.getNodeById)}</div></div>`;
    }
    if (related.length) {
      html += `<div class="knd-section"><h4>🔗 关联节点</h4><div class="knd-link-tags">${renderLinkTags(related.slice(0, 8), opts.getNodeById)}</div></div>`;
    }

    html += buildCoursewareSection(node.id);
    html += `<button type="button" class="generate-cw-btn knd-make-btn">✨ 制作新课件</button>`;

    container.innerHTML = html;

    container.onclick = (e) => {
      const tag = e.target.closest('[data-focus-node]');
      if (tag && typeof opts.onFocusNode === 'function') {
        opts.onFocusNode(tag.dataset.focusNode);
      }
      const btn = e.target.closest('.knd-make-btn');
      if (btn) {
        e.stopPropagation();
        const id = node.id;
        const name = node.name || id;
        if (typeof global.generateCourseware === 'function') {
          global.generateCourseware(id, name);
        } else if (global.TeachAnyMakeCourse) {
          global.TeachAnyMakeCourse.open({
            nodeId: id,
            nodeName: name,
            source: 'knowledge-map',
            meta: { subject: node.subject, grade: node.grade },
          });
        }
      }
    };
  }

  global.KnowledgeNodeDetail = { render };
})(window);
