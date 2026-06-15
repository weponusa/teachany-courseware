/**
 * TeachAny 制作课件模块（与 PBL / 全科图谱 / 知识树共用）
 * tree.html / pbl.html / knowledge-map.html 统一调用 TeachAnyMakeCourse.open()
 */
(function (global) {
  'use strict';

  var STYLE_ID = 'teachany-make-course-styles';
  var _metaIndex = null;
  var _metaLoad = null;

  var LAYER_LABELS = {
    prerequisite: '基础前置',
    matched: '核心必需',
    advanced: '扩展高级',
    parallel: '平行关联',
    external: '课标外补充',
    university: '大学延伸'
  };

  function clip(text, max) {
    var s = String(text || '').trim();
    if (!s) return '';
    return s.length > max ? s.slice(0, max) + '…' : s;
  }

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
      layer: node.layer || '',
      isExternal: !!node.isExternal,
      systemLabel: node.systemLabel || node.curriculumLabel || '',
      matchReason: node.matchReason || '',
      taskSnippet: node.taskSnippet || '',
      pblRole: node.pblRole || '',
      _moduleLabel: node._moduleLabel || '',
      confidence: node.confidence
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

  function isExternalNode(nodeId, meta) {
    if (meta && meta.isExternal) return true;
    var id = String(nodeId || '');
    return id.indexOf('ext-') === 0 || (meta && meta.layer === 'external');
  }

  function gradeLabel(grade) {
    var g = parseInt(grade, 10);
    if (!g || g === 0) return '大学';
    if (g <= 6) return '小学' + g + '年级';
    if (g <= 9) return '初中' + (g - 6) + '年级';
    if (g <= 12) return '高中' + (g - 9) + '年级';
    return g + '年级';
  }

  function gatherPBLProjectContext(nodeId, pblNode) {
    var result = null;
    if (global.TeachAnyPBLAutomation && typeof global.TeachAnyPBLAutomation.getResult === 'function') {
      result = global.TeachAnyPBLAutomation.getResult();
    }
    if (!result || !result.graphData) return null;

    var graphNode = pblNode || null;
    if (!graphNode && result.graphData.nodes) {
      graphNode = result.graphData.nodes.find(function (n) { return n && n.id === nodeId; }) || null;
    }

    var spec = result.projectSpec || {};
    var bp = result.projectBlueprint || {};
    var scheme = (bp.schemes || []).find(function (s) { return s.id === bp.recommendedSchemeId; })
      || (bp.schemes || [])[0];

    var links = result.graphData.links || [];
    var prereqOf = [];
    var leadsTo = [];
    links.forEach(function (l) {
      var src = typeof l.source === 'object' ? l.source.id : l.source;
      var tgt = typeof l.target === 'object' ? l.target.id : l.target;
      if (tgt === nodeId) prereqOf.push(src);
      if (src === nodeId) leadsTo.push(tgt);
    });

    function nameOf(id) {
      var n = (global.PBLPathBuilder && global.PBLPathBuilder.unifiedIndex && global.PBLPathBuilder.unifiedIndex.get(id))
        || (result.graphData.nodes || []).find(function (x) { return x && x.id === id; });
      return n ? (n.name || id) : id;
    }

    var phases = (scheme && scheme.phases) || result.projectPhases || [];
    var phaseHints = phases.slice(0, 4).map(function (p, i) {
      return (i + 1) + '. ' + (p.phase || p.name || '阶段' + (i + 1))
        + (p.deliverable ? ' → 交付：' + p.deliverable : '')
        + (p.steps && p.steps[0] ? '；步骤示例：' + p.steps[0] : '');
    });

    return {
      goal: result.goal || '',
      projectSpec: spec,
      techRoute: result.techRoute || '',
      moduleChain: result.moduleChain || '',
      archetype: (result.archetype && (result.archetype.name || result.archetype.id)) || '',
      schemeName: scheme ? scheme.name : '',
      schemeSummary: scheme ? scheme.summary : '',
      phaseHints: phaseHints,
      graphNode: graphNode,
      layerLabel: graphNode ? (LAYER_LABELS[graphNode.layer] || graphNode.layer) : '',
      prereqNames: prereqOf.slice(0, 6).map(nameOf),
      nextNames: leadsTo.slice(0, 6).map(nameOf)
    };
  }

  function buildNodeRegistrySection(nodeId, nodeName, meta, source) {
    var external = isExternalNode(nodeId, meta);
    var lines = [
      '【知识点登记 · 必须与交付物一致】',
      '- 课件标题：「' + (nodeName || meta.name || nodeId) + '」',
      '- node_id：' + nodeId + '（manifest.node_id、<meta name="teachany-node">、知识图谱挂树三者必须相同）'
    ];
    if (external) {
      lines.push('- 节点类型：PBL 课标外补充（ext-*）');
      lines.push('- 挂树位置：仅 data/trees/other/user-generated.json（Gallery「其他知识 / Other Knowledge」）');
      lines.push('- 禁止：不得挂到数学/语文/物理等正式课标树；不得改用课标 node_id；不得用 free_mode 代替 ext 挂树');
      lines.push('- 发布注册：rebuild-index 见 manifest.node_id 为 ext-* 后自动写入「其他知识」树，不会出现在学科课标树');
    } else {
      lines.push('- 节点类型：课标/图谱正式知识点');
      lines.push('- 挂树：用 find_nodes.py / check_node_id.py 校验后挂到对应学科课标树');
    }
    if (source) lines.push('- 发起入口：' + source);
    return lines.join('\n');
  }

  function buildSystemDescSection(meta) {
    var ctx = [];
    var def = clip(meta.definition, 900);
    if (def) ctx.push('定义/描述：' + def);

    var concepts = meta.key_concepts || meta.keyConcepts || [];
    if (concepts.length) ctx.push('核心概念：' + concepts.slice(0, 12).join('、'));

    var points = meta.curriculum_points || [];
    if (points.length) ctx.push('课标要点：' + points.slice(0, 6).join('；'));

    if (meta.subject) ctx.push('学科：' + meta.subject);
    if (meta.grade != null && meta.grade !== '') ctx.push('学段：' + gradeLabel(meta.grade));
    if (meta.domain) ctx.push('知识域：' + meta.domain);
    if (meta.name_en) ctx.push('英文名：' + meta.name_en);

    if (!ctx.length) return '';
    return '【系统中已有知识点描述（对齐教学目标，勿编造矛盾内容）】\n'
      + ctx.map(function (line) { return '- ' + line; }).join('\n');
  }

  function buildPBLSection(nodeId, nodeName, meta, pblCtx) {
    if (!pblCtx) return '';

    var gn = pblCtx.graphNode || {};
    var external = isExternalNode(nodeId, meta) || !!gn.isExternal || gn.layer === 'external';
    var lines = ['【PBL 项目情境 · 本课件必须服务该项目，不是孤立知识点课】'];

    if (pblCtx.goal) lines.push('- 项目总目标：' + clip(pblCtx.goal, 500));
    var spec = pblCtx.projectSpec || {};
    if (spec.task) lines.push('- 项目任务：' + clip(spec.task, 300));
    if (spec.gradeLevel || spec.grade) lines.push('- 项目学段：' + (spec.gradeLevel || spec.grade));
    if (spec.subject) lines.push('- 项目学科：' + spec.subject);
    if (spec.deliverable) lines.push('- 项目交付物：' + spec.deliverable);
    if (pblCtx.archetype) lines.push('- 项目类型：' + pblCtx.archetype);
    if (pblCtx.schemeName) lines.push('- 推荐方案：' + pblCtx.schemeName + (pblCtx.schemeSummary ? '（' + clip(pblCtx.schemeSummary, 120) + '）' : ''));
    if (pblCtx.moduleChain) lines.push('- 模块主线：' + clip(pblCtx.moduleChain, 200));
    if (pblCtx.techRoute) lines.push('- 技术路线提示：' + clip(pblCtx.techRoute, 160));

    lines.push('');
    lines.push('【本节点在路径中的位置】');
    if (pblCtx.layerLabel) lines.push('- 路径角色：' + pblCtx.layerLabel);
    if (meta.pblRole || gn.pblRole) lines.push('- 实施角色：' + (meta.pblRole || gn.pblRole));
    if (meta._moduleLabel || gn._moduleLabel) lines.push('- 所属模块：' + (meta._moduleLabel || gn._moduleLabel));
    if (meta.matchReason || gn.matchReason) lines.push('- 入选理由：' + clip(meta.matchReason || gn.matchReason, 280));
    if (meta.taskSnippet || gn.taskSnippet) lines.push('- 可执行任务片段：' + clip(meta.taskSnippet || gn.taskSnippet, 200));
    if (pblCtx.prereqNames.length) lines.push('- 路径前置节点：' + pblCtx.prereqNames.join(' → ') + ' → 【本节点】');
    if (pblCtx.nextNames.length) lines.push('- 路径后续节点：本节点 → ' + pblCtx.nextNames.join(' → '));

    if (pblCtx.phaseHints.length) {
      lines.push('');
      lines.push('【项目阶段（课件应嵌入哪一步）】');
      pblCtx.phaseHints.forEach(function (h) { lines.push('- ' + h); });
    }

    lines.push('');
    if (external) {
      lines.push('【课标外补充节点 · 专项逻辑（ext-*）】');
      lines.push('- 性质：课标树未单独覆盖，但完成上述 PBL 项目所必需的技能/概念/方法');
      lines.push('- 教学目标：只教「完成项目下一步所需的最小可用知识」，不做无关拓展或百科式铺陈');
      lines.push('- 情境锚定：导入、例题、练习、互动必须引用项目任务与交付物（测什么、算什么、写什么、做什么）');
      lines.push('- 证据产出：课件结束处明确「学完本节后，学生在项目中能完成的具体动作/产出」');
      lines.push('- 挂树：node_id 必须保持 ' + nodeId + '（与 PBL 拆解 hash 一致，禁止另造）');
      lines.push('- 发布注册：发布后只进「其他知识」树，标题可写「' + nodeName + '（项目补充）」');
      lines.push('- 衔接：在总结区写清「回到项目主线的下一步」及与前后路径节点的关系');
    } else if (gn.layer === 'prerequisite') {
      lines.push('【基础前置节点 · 专项逻辑】');
      lines.push('- 侧重：扫清项目入门障碍；少拓展、快上手、能立刻用于项目第一步');
      lines.push('- 练习：用项目情境出题，不要纯习题堆砌');
    } else if (gn.layer === 'matched') {
      lines.push('【核心必需节点 · 专项逻辑】');
      lines.push('- 侧重：项目主线的课标能力落地；互动与评估应对齐项目交付物中的关键指标');
    } else if (gn.layer === 'parallel' || gn.layer === 'advanced') {
      lines.push('【平行/扩展节点 · 专项逻辑】');
      lines.push('- 侧重：加分拓展或跨模块联系；标明「必修/选修」，避免喧宾夺主');
    } else if (gn.layer === 'university') {
      lines.push('【大学延伸节点 · 专项逻辑】');
      lines.push('- 侧重：浅尝辄止的拓展视野；标注与 K12 项目的衔接点，不做超纲考试化内容');
    }

    return lines.join('\n');
  }

  function buildOtherKnowledgePublishSection(nodeId, nodeName, meta, pblCtx) {
    if (!isExternalNode(nodeId, meta)) return '';

    var pblGoal = pblCtx && pblCtx.goal ? clip(pblCtx.goal, 200) : '';
    var lines = [
      '【发布注册 · 必须挂入「其他知识」树（硬性）】',
      '- node_id：' + nodeId + '（manifest.node_id 与 <meta name="teachany-node"> 必须完全相同）',
      '- 树位置：data/trees/other/user-generated.json → 网站知识树「其他知识 / Other Knowledge」入口',
      '- 机制：publish 后 rebuild-index.py 识别 ext-* node_id，自动写入「其他知识」，不会挂到任何正式课标学科树',
      '- 禁止：hang_tree register 到 math/chinese/physics 等课标树；禁止把 node_id 改成 phy-* / math-* 等课标 id',
      '- 禁止：manifest.free_mode 代替 ext 挂树（ext-* 本身即进入其他知识）',
      '',
      'manifest 必填核对：',
      '- "node_id": "' + nodeId + '"',
      '- "name" / "title"：建议含「（项目补充）」便于与课标课区分',
      '- "subject"：可写项目相关学科（展示用），但不影响挂树目标——仍以 ext-* 进「其他知识」',
      pblGoal ? '- 可在 description 注明来源 PBL 项目：' + pblGoal : '',
      '',
      '发布前校验（Phase 3.5c · 避免上传/挂树失败）：',
      '- python3 scripts/set-feedback-password.py --check <课件目录>/manifest.json',
      '- python3 scripts/preflight-publish.py <课件目录>',
      '- python3 scripts/check_node_id.py --node-id ' + nodeId,
      '  （应提示：PBL 外部知识点 → 挂入 other/user-generated.json）',
      '',
      '发布命令（用户确认后）：',
      '- TEACHANY_UPLOAD_CONFIRMED=1 python3 scripts/hang_tree.py publish <course-id> --course-dir <课件目录>',
      '- 发布后验证：知识树打开「其他知识」可见本节点；学科课标树中不应出现 ' + nodeId
    ];
    return lines.filter(function (l) { return l !== ''; }).join('\n');
  }

  function buildDeliverableSection(nodeId, meta, source) {
    var grade = meta.grade;
    var external = isExternalNode(nodeId, meta);
    var stageHint = (grade != null && grade <= 6) ? 'teachany-elementary'
      : (grade != null && grade <= 9) ? 'teachany-middle' : 'teachany-high';

    var phase0 = external
      ? '1. Phase 0：python3 scripts/check_node_id.py --node-id ' + nodeId + '（确认 ext → 其他知识）；preflight-check.py 通过'
      : '1. Phase 0：python3 scripts/find_nodes.py + check_node_id.py 校验课标 node_id；preflight-check.py 通过';

    var phasePublish = external
      ? '9. Phase 3.5：3.5a 反馈密码 → 3.5c preflight-publish.py → 3.5b 用户同意后 hang_tree publish；确认节点在「其他知识」树'
      : '9. Phase 3.5：3.5a 反馈密码 → 3.5c preflight-publish.py → 3.5b 同意后 hang_tree publish，挂课标学科树';

    return [
      '【TeachAny Skill 交付清单 · 完整模式，禁止简版】',
      phase0,
      '2. Phase 1：问题锚点 + ABT 叙事；若来自 PBL，导入必须回扣项目任务与交付物',
      '3. Phase 2：复制 templates/course-skeleton-v2.html + manifest-template.json；body 使用 ' + stageHint,
      '4. Hero：find-hero.py --cdn → agnes-image-gen.py（优先）；仅额度用尽/失败时用 gen-hero-svg.py（v8 知识全景，须从 manifest/学习目标生成，禁止空壳四字卡）',
      '5. 插图：章节情境图用 agnes-image-gen.py；数学/坐标类用 SVG 叠字，避免 AI 乱码',
      '6. 数理化：必读 tech/iframe-resources.md，嵌入 ≥1 个 PhET/GeoGebra/Desmos 等真实互动',
      '7. 五件套：AI 学伴、TTS（≥3 条 mp3）、section hints、知识图谱、导师卡片 + 悬浮坞',
      '8. Phase 3 收尾（强制）：python3 scripts/finalize-courseware.py <课件目录> — 自动补齐 AI 学伴/音频/知识图谱 + 为每个 data-tts 段落生成真实分段 mp3（漏写也会补全）',
      '8b. Phase 3：validate-courseware / 浏览器自测闭环',
      phasePublish,
      '10. 本页不会自动上传；完成后由用户在 AI 助手确认发布到 Gallery',
      '',
      '【本课最低质量】',
      '- 至少 1 个真实可操作互动（非静态图冒充）',
      '- 学习目标、前测、讲解、练习、总结迁移闭环完整',
      '- manifest 与 HTML meta 的 node_id 一致' + (external ? '（ext-* → 仅其他知识树）' : '，学科学段与课标节点一致')
    ].join('\n');
  }

  function buildPrompt(nodeId, nodeName, meta, opts) {
    meta = meta || {};
    opts = opts || {};
    var name = nodeName || meta.name || nodeId || '该知识点';
    var id = nodeId || '';
    var source = opts.source || 'make-course';
    var pblCtx = opts.pblContext || gatherPBLProjectContext(id, opts.pblNode || null);

    var parts = [
      '请使用 TeachAny Skill，为「' + name + '」生成完整交互式课件（HTML + manifest），并在本地验证后询问我是否发布。',
      '',
      buildNodeRegistrySection(id, name, meta, source)
    ];

    var sysDesc = buildSystemDescSection(meta);
    if (sysDesc) {
      parts.push('');
      parts.push(sysDesc);
    }

    var pblSec = buildPBLSection(id, name, meta, pblCtx);
    if (pblSec) {
      parts.push('');
      parts.push(pblSec);
    }

    var publishSec = buildOtherKnowledgePublishSection(id, name, meta, pblCtx);
    if (publishSec) {
      parts.push('');
      parts.push(publishSec);
    }

    parts.push('');
    parts.push(buildDeliverableSection(id, meta, source));

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
      '.tmc-panel{max-width:620px;width:100%;max-height:85vh;overflow:auto;background:#1e293b;border:1px solid rgba(148,163,184,0.2);border-radius:14px;padding:20px 22px;color:#f8fafc;box-shadow:0 12px 40px rgba(0,0,0,0.45);}',
      '.tmc-panel h3{margin:0 0 6px;font-size:18px;}',
      '.tmc-panel .tmc-meta{font-size:12px;color:#94a3b8;margin-bottom:14px;}',
      '.tmc-hint{font-size:12px;color:#94a3b8;line-height:1.7;margin-bottom:8px;}',
      '.tmc-publish-note{font-size:12px;color:#fbbf24;line-height:1.65;margin-bottom:10px;padding:8px 10px;border-radius:8px;background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.25);}',
      '.tmc-publish-note strong{color:#fde68a;}',
      '.tmc-prompt{background:#0f172a;border:1px solid rgba(148,163,184,0.2);border-radius:8px;padding:12px 14px;font-size:12px;line-height:1.65;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;white-space:pre-wrap;word-break:break-word;max-height:42vh;overflow:auto;}',
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
      '  <div class="tmc-hint">推荐在 <b>WorkBuddy</b> 中加载 <b>TeachAny Skill</b>；也兼容 <b>CodeBuddy</b>、<b>Cursor</b>、<b>Claude Code</b>。复制下方提示词粘贴给 AI 即可。</div>',
      '  <div class="tmc-publish-note" id="tmc-publish-note">📌 本页<strong>不会自动上传</strong>。生成后请在 AI 助手里确认发布（或到「我的 → 导入的」提交社区），通过后才会出现在 Gallery。</div>',
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
    var publishNote = overlay.querySelector('#tmc-publish-note');
    if (title) title.textContent = '✨ 制作课件 · ' + (nodeName || nodeId);
    if (metaEl) {
      var bits = ['知识点 ID：' + nodeId];
      if (meta && meta.subject) bits.push(meta.subject);
      if (meta && meta.grade != null && meta.grade !== '') {
        bits.push(meta.grade === 0 ? '大学' : gradeLabel(meta.grade));
      }
      if (meta && meta.layer) bits.push(LAYER_LABELS[meta.layer] || meta.layer);
      if (meta && (meta.isExternal || String(nodeId).indexOf('ext-') === 0)) bits.push('课标外补充');
      if (meta && meta.definition) bits.push('已嵌入系统描述');
      metaEl.textContent = bits.join(' · ');
    }
    if (promptEl) promptEl.textContent = prompt;
    if (publishNote) {
      if (isExternalNode(nodeId, meta)) {
        publishNote.innerHTML = '📌 本课为 <strong>PBL 课标外补充（ext-*）</strong>。发布后由 rebuild-index 自动注册到知识树 <strong>「其他知识」</strong>，不会挂到数学/语文等正式课标树。请在 AI 助手确认 publish 并核对挂树位置。';
      } else {
        publishNote.innerHTML = '📌 本页<strong>不会自动上传</strong>。生成后请在 AI 助手里确认发布（或到「我的 → 导入的」提交社区），通过后才会出现在 Gallery。';
      }
    }
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
      if (opts.pblNode) {
        merged = Object.assign(merged, pickMetaFromNode(opts.pblNode));
      }
      var pblContext = opts.pblContext || gatherPBLProjectContext(nodeId, opts.pblNode || null);
      var prompt = opts.prompt || buildPrompt(nodeId, nodeName, merged, {
        source: opts.source || 'make-course',
        pblNode: opts.pblNode || null,
        pblContext: pblContext
      });
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
    resolveNodeMeta: resolveNodeMetaSync,
    gatherPBLProjectContext: gatherPBLProjectContext
  };

  global.generateCourseware = function (nodeId, nodeName, extraMeta) {
    var pblNode = (extraMeta && extraMeta.pblNode) || null;
    if (!pblNode && global._pblDetailNodeForMake && global._pblDetailNodeForMake.id === nodeId) {
      pblNode = global._pblDetailNodeForMake;
    }
    open({
      nodeId: nodeId,
      nodeName: nodeName,
      source: (extraMeta && extraMeta.source) || (pblNode ? 'pbl-detail' : 'generate'),
      meta: extraMeta || {},
      pblNode: pblNode
    });
  };
})(window);
