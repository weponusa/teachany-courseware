/**
 * TeachAny 制作课件模块（与 PBL / 全科图谱 / 知识树共用）
 * tree.html / pbl.html / knowledge-map.html 统一调用 TeachAnyMakeCourse.open()
 */
(function (global) {
  'use strict';

  var STYLE_ID = 'teachany-make-course-styles';
  var _metaIndex = null;
  var _metaLoad = null;

  function loadMetaIndex() {
    if (_metaIndex) return Promise.resolve(_metaIndex);
    if (_metaLoad) return _metaLoad;
    _metaLoad = fetch('./data/nodes-metadata.json?t=' + Date.now())
      .then(function (r) { return r.ok ? r.json() : { nodes: [] }; })
      .then(function (d) {
        _metaIndex = new Map();
        (d.nodes || []).forEach(function (n) {
          if (n && n.id) _metaIndex.set(n.id, n);
        });
        return _metaIndex;
      })
      .catch(function () {
        _metaIndex = new Map();
        return _metaIndex;
      });
    return _metaLoad;
  }

  function pickMetaFromNode(node) {
    if (!node) return {};
    return {
      name: node.name || '',
      definition: node.definition || node.description || '',
      key_concepts: node.key_concepts || node.skills || [],
      curriculum_points: node.curriculum_points || [],
      subject: node.subject || '',
      grade: node.grade,
      domain: node.domain || '',
      name_en: node.name_en || '',
    };
  }

  function resolveNodeMetaSync(nodeId) {
    var node = null;
    if (global.PBLPathBuilder && global.PBLPathBuilder.unifiedIndex) {
      node = global.PBLPathBuilder.unifiedIndex.get(nodeId);
    }
    if (!node && global.KnowledgeMapNodeIndex && typeof global.KnowledgeMapNodeIndex.get === 'function') {
      node = global.KnowledgeMapNodeIndex.get(nodeId);
    }
    if (!node && _metaIndex) node = _metaIndex.get(nodeId);
    return pickMetaFromNode(node);
  }

  function buildPrompt(nodeId, nodeName, meta) {
    meta = meta || {};
    var name = nodeName || meta.name || nodeId || '该知识点';
    var id = nodeId || '';
    var parts = [
      '帮我生成「' + name + '」的 TeachAny 交互式课件 HTML，知识点 ID：' + id + '。',
      '请严格遵循 TeachAny Skill 规范（互动、分层、可课堂使用）。'
    ];

    var ctx = [];
    var def = String(meta.definition || '').trim();
    if (def) ctx.push('定义/描述：' + def.slice(0, 900));

    var concepts = meta.key_concepts || meta.keyConcepts || [];
    if (concepts.length) ctx.push('核心概念：' + concepts.slice(0, 12).join('、'));

    var points = meta.curriculum_points || [];
    if (points.length) ctx.push('课标要点：' + points.slice(0, 6).join('；'));

    if (meta.subject) ctx.push('学科：' + meta.subject);
    if (meta.grade != null && meta.grade !== '') {
      ctx.push('学段：' + (meta.grade === 0 ? '大学' : meta.grade + '年级'));
    }
    if (meta.domain) ctx.push('知识域：' + meta.domain);
    if (meta.name_en) ctx.push('英文名：' + meta.name_en);

    if (ctx.length) {
      parts.push('');
      parts.push('【系统中已有知识点描述（请据此对齐教学目标，勿编造矛盾内容）】');
      ctx.forEach(function (line) { parts.push('- ' + line); });
    }

    return parts.join('\n');
  }

  function recordIntent(nodeId, nodeName, prompt, source, meta) {
    meta = meta || {};
    try {
      if (global.TeachAnyHistory && typeof global.TeachAnyHistory.recordCreated === 'function') {
        global.TeachAnyHistory.recordCreated((source || 'make-course') + '-intent-' + nodeId, {
          source: source || 'make-course',
          name: (nodeName || nodeId) + '（制作课件意图）',
          subject: meta.subject || '',
          grade: meta.grade != null ? String(meta.grade) : (meta.gradeLabel || ''),
          node: nodeId,
          url: '',
          prompt: prompt,
          status: 'draft'
        });
      }
    } catch (_e) { /* ignore */ }
  }

  function injectStyles() {
    if (document.getElementById(STYLE_ID)) return;
    var style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent = [
      '.tmc-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.62);z-index:3000;display:flex;align-items:center;justify-content:center;padding:20px;opacity:0;pointer-events:none;transition:opacity .2s ease;}',
      '.tmc-overlay.visible{opacity:1;pointer-events:auto;}',
      '.tmc-panel{max-width:520px;width:100%;max-height:85vh;overflow:auto;background:#1e293b;border:1px solid rgba(148,163,184,0.2);border-radius:14px;padding:20px 22px;color:#f8fafc;box-shadow:0 12px 40px rgba(0,0,0,0.45);}',
      '.tmc-panel h3{margin:0 0 6px;font-size:18px;}',
      '.tmc-panel .tmc-meta{font-size:12px;color:#94a3b8;margin-bottom:14px;}',
      '.tmc-hint{font-size:12px;color:#94a3b8;line-height:1.7;margin-bottom:10px;}',
      '.tmc-prompt{background:#0f172a;border:1px solid rgba(148,163,184,0.2);border-radius:8px;padding:12px 14px;font-size:13px;line-height:1.7;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;white-space:pre-wrap;word-break:break-word;}',
      '.tmc-actions{display:flex;align-items:center;gap:10px;margin-top:12px;flex-wrap:wrap;}',
      '.tmc-copy{padding:8px 16px;border-radius:6px;background:#f59e0b;color:#fff;border:none;font-size:13px;font-weight:600;cursor:pointer;}',
      '.tmc-copy:hover{filter:brightness(1.08);}',
      '.tmc-pbl-link{font-size:12px;color:#3b82f6;text-decoration:none;}',
      '.tmc-pbl-link:hover{text-decoration:underline;}',
      '.tmc-close{float:right;background:transparent;border:none;color:#94a3b8;font-size:20px;cursor:pointer;line-height:1;padding:0 4px;}',
      '.tmc-feedback{font-size:12px;color:#10b981;opacity:0;transition:opacity .3s;}',
      '.tmc-feedback.visible{opacity:1;}',
      '.tree-make-course-btn,.generate-cw-btn{display:block;width:100%;margin-top:10px;padding:8px 12px;border:none;border-radius:8px;background:linear-gradient(135deg,#10b981,#059669);color:#fff;font-size:13px;font-weight:700;cursor:pointer;pointer-events:auto;text-align:center;}',
      '.tree-make-course-btn:hover,.generate-cw-btn:hover{filter:brightness(1.08);}'
    ].join('');
    document.head.appendChild(style);
  }

  function ensureOverlay() {
    injectStyles();
    var overlay = document.getElementById('teachany-make-course-modal');
    if (overlay) return overlay;

    overlay = document.createElement('div');
    overlay.id = 'teachany-make-course-modal';
    overlay.className = 'tmc-overlay';
    overlay.innerHTML = [
      '<div class="tmc-panel" role="dialog" aria-labelledby="tmc-title">',
      '  <button type="button" class="tmc-close" aria-label="关闭">&times;</button>',
      '  <h3 id="tmc-title">✨ 制作课件</h3>',
      '  <div class="tmc-meta" id="tmc-meta"></div>',
      '  <div class="tmc-hint">推荐在 <b>WorkBuddy</b> 中加载 <b>TeachAny Skill</b>；也兼容 <b>CodeBuddy</b>、<b>Cursor</b>、<b>Claude Code</b> 等 AI 助手。复制下方提示词即可生成课件。</div>',
      '  <div class="tmc-prompt" id="tmc-prompt"></div>',
      '  <div class="tmc-actions">',
      '    <button type="button" class="tmc-copy" id="tmc-copy-btn">📋 复制提示词</button>',
      '    <span class="tmc-feedback" id="tmc-feedback">已复制!</span>',
      '    <a class="tmc-pbl-link" id="tmc-pbl-link" href="./pbl.html" target="_blank" rel="noopener">在 PBL 页面打开 →</a>',
      '  </div>',
      '</div>'
    ].join('');
    document.body.appendChild(overlay);

    overlay.addEventListener('click', function (ev) {
      if (ev.target === overlay) closeModal();
    });
    overlay.querySelector('.tmc-close').addEventListener('click', closeModal);
    overlay.querySelector('#tmc-copy-btn').addEventListener('click', copyPrompt);
    return overlay;
  }

  var currentPrompt = '';

  function copyPrompt() {
    if (!currentPrompt) return;
    var feedback = document.getElementById('tmc-feedback');
    var done = function () {
      if (feedback) {
        feedback.classList.add('visible');
        setTimeout(function () { feedback.classList.remove('visible'); }, 2000);
      }
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(currentPrompt).then(done).catch(done);
      return;
    }
    var ta = document.createElement('textarea');
    ta.value = currentPrompt;
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); } catch (_e) { /* ignore */ }
    document.body.removeChild(ta);
    done();
  }

  function closeModal() {
    var overlay = document.getElementById('teachany-make-course-modal');
    if (overlay) overlay.classList.remove('visible');
  }

  function showModal(nodeId, nodeName, prompt, meta) {
    var overlay = ensureOverlay();
    currentPrompt = prompt;
    var title = overlay.querySelector('#tmc-title');
    var metaEl = overlay.querySelector('#tmc-meta');
    var promptEl = overlay.querySelector('#tmc-prompt');
    var pblLink = overlay.querySelector('#tmc-pbl-link');
    if (title) title.textContent = '✨ 制作课件 · ' + (nodeName || nodeId);
    if (metaEl) {
      var bits = ['知识点 ID：' + nodeId];
      if (meta && meta.subject) bits.push(meta.subject);
      if (meta && meta.grade != null && meta.grade !== '') {
        bits.push(meta.grade === 0 ? '大学' : meta.grade + '年级');
      }
      if (meta && meta.definition) bits.push('已嵌入系统描述');
      metaEl.textContent = bits.join(' · ');
    }
    if (promptEl) promptEl.textContent = prompt;
    if (pblLink) {
      pblLink.href = './pbl.html?make=' + encodeURIComponent(nodeId) + '&name=' + encodeURIComponent(nodeName || nodeId);
    }
    overlay.classList.add('visible');
  }

  function open(opts) {
    opts = opts || {};
    var nodeId = opts.nodeId || opts.id || '';
    var nodeName = opts.nodeName || opts.name || nodeId;
    if (!nodeId) return;

    var finish = function () {
      var merged = Object.assign({}, resolveNodeMetaSync(nodeId), opts.meta || {});
      var prompt = opts.prompt || buildPrompt(nodeId, nodeName, merged);
      recordIntent(nodeId, nodeName, prompt, opts.source || 'make-course', merged);
      showModal(nodeId, nodeName, prompt, merged);
    };

    loadMetaIndex().then(finish).catch(finish);
  }

  global.TeachAnyMakeCourse = {
    buildPrompt: buildPrompt,
    open: open,
    close: closeModal,
    recordIntent: recordIntent,
    resolveNodeMeta: resolveNodeMetaSync
  };

  global.generateCourseware = function (nodeId, nodeName, extraMeta) {
    open({
      nodeId: nodeId,
      nodeName: nodeName,
      source: 'generate',
      meta: extraMeta || {}
    });
  };
})(window);
