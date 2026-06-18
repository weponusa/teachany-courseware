/**
 * TeachAny PBL 学习路径构建器 v1.0
 * 输入 PBL 项目目标 → LLM 匹配知识点 → 构建路径图 → D3.js 渲染图谱
 * 支持 5 大课标体系（CN/AP/Cambridge/IB/US）+ 外部知识点补充
 */

class PBLPathBuilder {
  constructor() {
    this.unifiedIndex = new Map();     // 统一知识点索引（所有课标）
    this.systemIndex = new Map();      // system -> Set(nodeIds)
    this.treeData = [];                // 已加载的树数据
    this.loaded = false;
    this._loadPromise = null;

    // 全科图谱增强：跨学科边关系图（与 knowledge-map-data.json 对齐）
    this.graphEdges = [];              // [{source, target}] 全科图谱边
    this.graphNeighbors = new Map();   // nodeId -> { parents: Set, children: Set }
    this.graphLoaded = false;
    this.k12NodeIds = new Set();       // grade 1–12 中国课标节点 ID
    this.universityNodeIds = new Set(); // grade 0 大学层节点 ID

    // Tooltip 延迟隐藏：允许鼠标从节点移动到弹窗内点击课程链接
    this._tooltipHideTimer = null;
    this._tooltipHovered = false;
    this._topicProfileCache = new Map();

    // LLM 服务商：服务端预设 + 可选模型；custom 走客户端自带 Key
    this.providers = [
      {
        id: 'preset',
        name: 'TeachAny 默认（Qwen3 Next 80B）',
        serverPreset: true,
        model: '',
        models: ['', 'qwen/qwen3-next-80b-a3b-instruct', 'deepseek-ai/DeepSeek-V4-Flash', 'deepseek-ai/DeepSeek-V4-Pro', 'GLM-4-Flash', '__custom__'],
      },
      {
        id: 'siliconflow',
        name: '硅基流动',
        serverBacked: true,
        model: 'deepseek-ai/DeepSeek-V4-Flash',
        models: ['deepseek-ai/DeepSeek-V4-Flash', 'deepseek-ai/DeepSeek-V3', 'Qwen/Qwen3-235B-A22B', 'THUDM/GLM-4-9B-0414', '__custom__'],
      },
      {
        id: 'paratera',
        name: '并行超算',
        serverBacked: true,
        model: 'GLM-4-Flash',
        models: ['GLM-4-Flash', 'DeepSeek-V3.2', 'DeepSeek-R1', 'GLM-4.7', 'GLM-5', '__custom__'],
      },
      {
        id: 'openrouter',
        name: 'OpenRouter（可填自有 Key）',
        serverBacked: true,
        clientKeyOk: true,
        baseUrl: 'https://openrouter.ai/api/v1',
        model: 'qwen/qwen3-next-80b-a3b-instruct',
        models: [
          '',
          'qwen/qwen3-next-80b-a3b-instruct',
          'deepseek/deepseek-v4-flash',
          'deepseek/deepseek-v4-pro',
          'deepseek/deepseek-chat-v3.1',
          'deepseek/deepseek-chat-v3-0324',
          'deepseek/deepseek-r1',
          'deepseek/deepseek-r1-0528',
          'deepseek/deepseek-r1-distill-qwen-32b',
          'deepseek/deepseek-r1-distill-llama-70b',
          'anthropic/claude-sonnet-4',
          'openai/gpt-4.1',
          'google/gemini-2.5-pro-preview',
          'qwen/qwen3-next-80b-a3b-instruct:free',
          'meta-llama/llama-3.3-70b-instruct:free',
          '__custom__',
        ],
        modelLabels: {
          'qwen/qwen3-next-80b-a3b-instruct': 'Qwen3 Next 80B（付费，默认）',
          'deepseek/deepseek-v4-pro': 'DeepSeek V4 Pro（付费）',
          'deepseek/deepseek-v4-flash': 'DeepSeek V4 Flash（付费）',
          'deepseek/deepseek-chat-v3.1': 'DeepSeek Chat V3.1（付费）',
          'deepseek/deepseek-chat-v3-0324': 'DeepSeek Chat V3 0324（付费）',
          'deepseek/deepseek-r1': 'DeepSeek R1（付费）',
          'deepseek/deepseek-r1-0528': 'DeepSeek R1 0528（付费）',
          'deepseek/deepseek-r1-distill-qwen-32b': 'DeepSeek R1 Distill Qwen 32B',
          'deepseek/deepseek-r1-distill-llama-70b': 'DeepSeek R1 Distill Llama 70B',
          'anthropic/claude-sonnet-4': 'Claude Sonnet 4（付费）',
          'openai/gpt-4.1': 'GPT-4.1（付费）',
          'google/gemini-2.5-pro-preview': 'Gemini 2.5 Pro（付费）',
          'qwen/qwen3-next-80b-a3b-instruct:free': 'Qwen3 Next 80B（免费）',
          'meta-llama/llama-3.3-70b-instruct:free': 'Llama 3.3 70B（免费）',
        },
      },
      {
        id: 'custom',
        name: '自定义 API（自带 Key）',
        clientLlm: true,
        baseUrl: '',
        model: '',
        models: [],
      },
    ];
    this._loadLLMConfig();

    this._archetypeEngine = null;
    this._resolvedArchetype = null;
    this._activeProjectSpec = null;
    this._refinementContext = null;
  }

  _defaultLLMConfig() {
    return {
      providerId: 'preset',
      model: '',
      apiKey: '',
      baseUrl: '',
      customModel: '',
      configVersion: 2,
    };
  }

  /** 迁移旧版默认（硅基 DeepSeek）到 TeachAny 服务端默认（Qwen3 Next 80B） */
  _migrateLLMConfig(cfg) {
    const c = { ...cfg };
    const pid = String(c.providerId || '');
    const model = String(c.model || '');
    const hasKey = !!(c.apiKey || '').trim();
    if (!hasKey && pid === 'siliconflow') {
      return this._defaultLLMConfig();
    }
    if (!hasKey && pid === 'preset' && /^deepseek-ai\/DeepSeek-V4/i.test(model)) {
      return { ...this._defaultLLMConfig() };
    }
    if (!hasKey && pid === 'openrouter' && !model) {
      return this._defaultLLMConfig();
    }
    c.configVersion = 2;
    return c;
  }

  _loadLLMConfig() {
    try {
      const saved = localStorage.getItem('teachany_pbl_config');
      if (saved) {
        const cfg = JSON.parse(saved);
        if (this.providers.some(p => p.id === cfg.providerId)) {
          const migrated = this._migrateLLMConfig(cfg);
          this._llmConfig = migrated;
          if (migrated !== cfg || cfg.configVersion !== 2) this._saveLLMConfig();
          return;
        }
      }
    } catch (e) { /* ignore */ }
    this._llmConfig = this._defaultLLMConfig();
  }

  _saveLLMConfig() {
    try {
      localStorage.setItem('teachany_pbl_config', JSON.stringify(this._llmConfig));
    } catch (e) { /* ignore */ }
  }

  getLLMConfig() {
    const provider = this.providers.find(p => p.id === this._llmConfig.providerId) || this.providers[0];
    let model = this._llmConfig.model ?? provider.model ?? '';
    if (model === '__custom__') {
      model = String(this._llmConfig.customModel || '').trim();
    }
    const usesServerDefault = !!provider.serverPreset && !model && !(this._llmConfig.apiKey || '').trim();
    return {
      providerId: provider.id,
      providerName: provider.name,
      model,
      displayLabel: usesServerDefault
        ? '服务端默认'
        : (model || (provider.serverPreset ? '服务端默认' : '自动')),
      displayDetail: usesServerDefault ? 'Qwen3 Next 80B（OpenRouter）' : model,
      usesServerDefault,
      apiKey: this._llmConfig.apiKey || '',
      baseUrl: this._llmConfig.baseUrl || provider.baseUrl || '',
      serverBacked: !!provider.serverBacked,
      serverPreset: !!provider.serverPreset,
      clientLlm: !!provider.clientLlm,
    };
  }

  setLLMConfig(cfg) {
    Object.assign(this._llmConfig, cfg);
    this._saveLLMConfig();
  }

  _llmStageOptions(stage) {
    const map = {
      decompose: { maxTokens: 4500, temperature: 0.35 },
      'review-decompose': { maxTokens: 5000, temperature: 0.12 },
      filter: { maxTokens: 1200, temperature: 0.25 },
      'propose-curriculum': { maxTokens: 3000, temperature: 0.25 },
      'validate-match': { maxTokens: 6000, temperature: 0.1 },
      match: { maxTokens: 8000, temperature: 0.15 },
      'verify-relevance': { maxTokens: 3000, temperature: 0.05 },
      'review-curriculum': { maxTokens: 3500, temperature: 0.05 },
      refine: { maxTokens: 2500, temperature: 0.2 },
      'verify-deps': { maxTokens: 2500, temperature: 0.08 },
    };
    return map[stage] || { maxTokens: 4000, temperature: 0.2 };
  }

  async callLLM(messages, options = {}) {
    const cfg = this.getLLMConfig();
    if (!cfg.baseUrl) throw new Error('请先配置 Base URL（点击右上角 ⚙️ 设置）');
    if (!cfg.apiKey) throw new Error('请先配置 API Key（点击右上角 ⚙️ 设置）');
    if (!cfg.model) throw new Error('请先配置模型名称');

    const cleanBaseUrl = String(cfg.baseUrl).replace(/\/$/, '');
    const endpoint = /\/chat\/completions/i.test(cleanBaseUrl)
      ? cleanBaseUrl
      : `${cleanBaseUrl}/chat/completions`;

    const headers = {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${cfg.apiKey}`,
    };
    if (cleanBaseUrl.includes('openrouter.ai')) {
      headers['HTTP-Referer'] = location.origin || 'https://www.teachany.cn';
      headers['X-Title'] = 'TeachAny PBL';
    }

    const body = {
      model: cfg.model,
      messages,
      stream: false,
      temperature: options.temperature ?? 0.2,
      max_tokens: options.maxTokens ?? 4000,
    };

    const ac = new AbortController();
    const timeout = setTimeout(() => ac.abort(), 90000);
    try {
      const resp = await fetch(endpoint, {
        method: 'POST',
        headers,
        signal: ac.signal,
        body: JSON.stringify(body),
      });
      const text = await resp.text();
      if (!resp.ok) {
        let errMsg = text.slice(0, 300);
        try { errMsg = JSON.parse(text)?.error?.message || errMsg; } catch (_e) { /* ignore */ }
        throw new Error(`API ${resp.status}: ${errMsg}`);
      }
      const data = JSON.parse(text);
      const message = data.choices?.[0]?.message || {};
      return message.content || message.reasoning || message.reasoning_content || '';
    } finally {
      clearTimeout(timeout);
    }
  }

  async _fetchPBLMessages(stage, payload) {
    const body = { stage, ...payload, messagesOnly: true };
    const ac = new AbortController();
    const timeout = setTimeout(() => ac.abort(), 60000);
    try {
      const resp = await fetch(this._getPBLAnalyzeUrl(), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        signal: ac.signal,
        body: this._safeStringify(body, 'PBL messages'),
      });
      const data = await resp.json().catch(() => ({}));
      if (!resp.ok) throw new Error(data.error || `PBL API ${resp.status}`);
      if (!Array.isArray(data.messages)) throw new Error('PBL API 未返回 messages');
      return data.messages;
    } finally {
      clearTimeout(timeout);
    }
  }

  async _ensureArchetypeData() {
    if (typeof PBLArchetypeEngine === 'undefined') return null;
    if (!this._archetypeEngine) this._archetypeEngine = new PBLArchetypeEngine();
    try {
      await this._archetypeEngine.load('./data/pbl/');
    } catch (e) {
      console.warn('[PBL] 原型层数据加载失败，将使用规则回退:', e.message);
    }
    return this._archetypeEngine;
  }

  _resolveArchetype(goal) {
    const g = String(goal || '');
    const list = this._archetypeEngine?.archetypeData?.archetypes;
    if (!list?.length) {
      this._resolvedArchetype = null;
      return null;
    }
    for (const a of list) {
      for (const p of a.matchPatterns || []) {
        try {
          if (new RegExp(p).test(g)) {
            this._resolvedArchetype = a;
            return a;
          }
        } catch (e) { /* skip invalid pattern */ }
      }
    }
    this._resolvedArchetype = null;
    return null;
  }

  _isArchetypeBanned(node, archetype) {
    if (!archetype || !this._archetypeEngine) return false;
    if (this._archetypeEngine.isBanned(node, archetype)) return true;
    if (this._isGenericTransversalNode(node.name, '')) return true;
    return false;
  }

  _meetsArchetypeGrade(node, archetype, goal = '') {
    if (!archetype || !this._archetypeEngine) return true;
    if (this._isArchetypeBanned(node, archetype)) return false;
    const band = this._parseExplicitGradeBand(goal);
    if (!band.explicit) return true;
    if (!this._archetypeEngine.meetsGrade(node, archetype)) return false;
    const minG = this._effectiveMinGradeForGoal(goal, archetype);
    const grade = parseInt(node.grade, 10) || 0;
    if (grade > 0 && grade < minG && !this._isPrerequisiteForGoal(node, goal)) return false;
    if (archetype.minGrade >= 7 && band.explicit && this._excludeForComplexProject(node)) return false;
    return true;
  }

  /** 低年级先修节点在明确年级目标下可保留 */
  _isPrerequisiteForGoal(node, goal) {
    if (!node || !this._parseExplicitGradeBand(goal).explicit) return false;
    const name = String(node.name || '');
    return /认识|初步|基础|入门/.test(name) && parseInt(node.grade, 10) > 0;
  }

  _applyArchetypePoolRules(pool, archetype, activeSystems, goal = '') {
    if (!archetype) return pool;
    let out = pool.filter(n => this._meetsArchetypeGrade(n, archetype, goal));
    out = out.filter(n => !this._isArchetypeBanned(n, archetype));
    if (this._archetypeEngine) {
      out = this._archetypeEngine.applySystemLock(out, archetype, activeSystems);
    }
    return out;
  }

  _alignBlueprintModules(blueprint, archetype) {
    if (!blueprint || !archetype?.modules?.length) return blueprint;
    const mods = archetype.modules;
    const schemes = (blueprint.schemes || []).map(s => ({
      ...s,
      phases: (s.phases || []).map((p, i) => {
        const hasIds = (p.subsystemIds || []).length;
        const mod = mods[i % mods.length];
        return hasIds ? p : { ...p, subsystemIds: [mod.id] };
      }),
    }));
    return { ...blueprint, schemes, knowledgeChain: blueprint.knowledgeChain || this._archetypeEngine?.moduleChain(archetype, blueprint) };
  }

  _validateBlueprint(blueprint, goal, archetype) {
    if (this._archetypeEngine?.validateBlueprint) {
      const base = this._archetypeEngine.validateBlueprint(blueprint, archetype);
      if (!base.valid) return base;
    }
    const issues = [];
    if (!blueprint?.schemes?.length) issues.push('缺少可行方案');
    if (!blueprint?.deliverable) issues.push('缺少交付物');
    if (this._isGenericBlueprintText(blueprint?.projectSummary)) issues.push('项目概述过于笼统');
    if (!blueprint?.scopeLimits?.length) issues.push('缺少能力边界说明');
    if (!blueprint?.successCriteria?.length) issues.push('缺少验收标准');
    if (this._blueprintStepDepthScore(blueprint) < 2) issues.push('阶段任务可操作性不足');
    return { valid: issues.length === 0, issues };
  }

  computeQualityScore(payload = {}) {
    const {
      goal = '', matched = [], external = [], projectBlueprint = null,
      archetype = null, graphData = null, pathPlan = null,
    } = payload;
    let score = 100;
    const breakdown = [];

    const minM = this._getMinMatchedFloor(archetype);
    if (matched.length < minM) {
      const pen = Math.min(25, (minM - matched.length) * 6);
      score -= pen;
      breakdown.push({ key: 'matched', label: '课标匹配不足', delta: -pen });
    }

    const domains = this._inferProjectDomains(goal);
    const irrelevant = matched.filter(n => this._getNodeIrrelevanceReason(n, goal, domains, archetype));
    if (irrelevant.length) {
      const pen = Math.min(35, irrelevant.length * 10);
      score -= pen;
      breakdown.push({ key: 'irrelevant', label: `无关节点 ${irrelevant.length} 个`, delta: -pen });
    }

    const fallbackNodes = matched.filter(n => /主线关键词回退|K12全科图谱检索回退/.test(String(n.matchReason || '')));
    if (fallbackNodes.length >= 2) {
      const pen = Math.min(25, fallbackNodes.length * 5);
      score -= pen;
      breakdown.push({ key: 'fallback', label: `检索回退节点 ${fallbackNodes.length} 个`, delta: -pen });
    }

    if (this._shouldPurgeChemistryForGoal(goal)) {
      const chemNodes = matched.filter(n => n.subject === 'chemistry');
      if (chemNodes.length) {
        const pen = Math.min(30, chemNodes.length * 8);
        score -= pen;
        breakdown.push({ key: 'chem', label: `无关化学节点 ${chemNodes.length} 个`, delta: -pen });
      }
    }

    if (this._shouldPurgeGeographyClimateForGoal(goal)) {
      const geoNodes = matched.filter(n => this._isOffTopicGeographyClimateNode(n));
      if (geoNodes.length) {
        const pen = Math.min(25, geoNodes.length * 10);
        score -= pen;
        breakdown.push({ key: 'geo', label: `无关气候地理节点 ${geoNodes.length} 个`, delta: -pen });
      }
    }

    const banned = matched.filter(n => this._isGenericTransversalNode(n.name, goal));
    if (banned.length) {
      const pen = Math.min(15, banned.length * 5);
      score -= pen;
      breakdown.push({ key: 'ban', label: '泛素养节点', delta: -pen });
    }

    const phases = pathPlan?.phases || projectBlueprint?.schemes?.find(s => s.id === projectBlueprint?.recommendedSchemeId)?.phases || [];
    let hollow = 0;
    phases.forEach(p => {
      (p.steps || []).forEach(st => { if (this._isHollowStep(st)) hollow++; });
    });
    if (hollow >= 1) {
      const pen = Math.min(28, hollow * 5);
      score -= pen;
      breakdown.push({ key: 'hollow', label: `空话步骤 ${hollow} 条`, delta: -pen });
    }

    if (projectBlueprint) {
      const substance = this._blueprintSubstanceScore(projectBlueprint, goal);
      if (substance < 3) {
        const pen = Math.min(32, (3 - substance) * 12);
        score -= pen;
        breakdown.push({ key: 'substance', label: '蓝图内容空洞（缺题目锚点/可验收产出）', delta: -pen });
      }
    }

    if (projectBlueprint && this._isGenericBlueprintText(projectBlueprint.projectSummary)) {
      score -= 12;
      breakdown.push({ key: 'summary', label: '项目概述套话', delta: -12 });
    }
    const stepDepth = this._blueprintStepDepthScore(projectBlueprint);
    if (stepDepth > 0 && stepDepth < 2.5) {
      const pen = Math.min(15, Math.round((2.5 - stepDepth) * 8));
      score -= pen;
      breakdown.push({ key: 'depth', label: '任务步骤偏笼统', delta: -pen });
    }

    const bpVal = this._validateBlueprint(projectBlueprint, goal, archetype);
    if (!bpVal.valid) {
      const pen = Math.min(12, bpVal.issues.length * 4);
      score -= pen;
      breakdown.push({ key: 'blueprint', label: '蓝图待完善', delta: -pen });
    }

    if (archetype?.modules?.length) {
      const covered = new Set(matched.map(n => n._moduleId).filter(Boolean));
      const ratio = covered.size / archetype.modules.length;
      if (ratio < 0.5) {
        const pen = Math.round((0.5 - ratio) * 20);
        score -= pen;
        breakdown.push({ key: 'modules', label: '模块覆盖偏低', delta: -pen });
      }
    }

    const extWithTask = (external || []).filter(e => e.taskSnippet || e.matchReason?.includes('任务：'));
    if (!extWithTask.length && external?.length) {
      score -= 5;
      breakdown.push({ key: 'ext', label: '课外缺任务片段', delta: -5 });
    }

    const nodes = graphData?.nodes || [];
    if (nodes.length && matched.length) {
      const mainline = nodes.filter(n => n.pathStep);
      if (mainline.length < Math.min(3, matched.length)) {
        score -= 8;
        breakdown.push({ key: 'path', label: '实施链不完整', delta: -8 });
      }
    }

    if (this._isFiltrationGoal(goal)) {
      if (!projectBlueprint?.scopeLimits?.length) {
        score -= 10;
        breakdown.push({ key: 'scope', label: '缺少局限说明', delta: -10 });
      }
      const unsafeExt = (external || []).some(e =>
        /塑料微珠|聚酯纤维碎屑|剪塑料|剪塑料袋|亮片/.test(`${e.taskSnippet || ''}${e.name || ''}`)
      );
      if (unsafeExt) {
        score -= 15;
        breakdown.push({ key: 'unsafe', label: '不安全实验建议', delta: -15 });
      }
    }

    return {
      score: Math.max(0, Math.min(100, Math.round(score))),
      grade: score >= 85 ? 'A' : score >= 70 ? 'B' : score >= 55 ? 'C' : 'D',
      breakdown,
      blueprintValid: bpVal.valid,
      blueprintIssues: bpVal.issues || [],
    };
  }

  // ─── 多课标知识点索引 ──────────────────────────

  async loadUnifiedIndex() {
    // 先初始化 CoursewareHub，保证 PBL tooltip 能拿到最新 registry 课件链接；
    // 即使统一知识点索引用了缓存，课件覆盖状态也不再过期。
    if (window.TeachAnyHub && typeof TeachAnyHub.init === 'function') {
      try { await TeachAnyHub.init(); } catch (e) { console.warn('[PBL] CoursewareHub init failed:', e.message); }
    }

    if (this.loaded) return this.unifiedIndex;
    if (this._loadPromise) return this._loadPromise;

    const CACHE_KEY = PBLPathBuilder.PBL_INDEX_CACHE_KEY;
    const LEGACY_CACHE_KEYS = ['teachany_pbl_unified_index_v10'];
    const CACHE_TTL = 1800000;
    if (!this._skipIndexCache) {
      try {
        const cached = localStorage.getItem(CACHE_KEY);
        if (cached) {
          const parsed = this._safeJsonParse(cached);
          const { ts, entries, v } = parsed || {};
          if (parsed && v === 11 && Date.now() - ts < CACHE_TTL && Array.isArray(entries)) {
            entries.forEach(([k, vNode]) => {
              if (!k || !vNode) return;
              this.unifiedIndex.set(k, vNode);
              if (vNode.system) {
                if (!this.systemIndex.has(vNode.system)) this.systemIndex.set(vNode.system, new Set());
                this.systemIndex.get(vNode.system).add(k);
              }
            });
            this.loaded = true;
            this._normalizeNodeSourceFlags();
            console.log(`[PBL] ✅ 从缓存恢复: ${this.unifiedIndex.size} 节点, ${this.systemIndex.size} 课标体系`);
            await this._loadKnowledgeGraph();
            return this.unifiedIndex;
          }
        }
      } catch (e) {
        console.warn('[PBL] 索引缓存损坏，将重新加载:', e.message);
        try { localStorage.removeItem(CACHE_KEY); } catch (_e) { /* ignore */ }
      }
    }
    LEGACY_CACHE_KEYS.forEach((k) => {
      try { localStorage.removeItem(k); } catch (_e) { /* ignore */ }
    });

    this._loadPromise = this._doLoad();
    return this._loadPromise;
  }

  async _doLoad() {
    console.log('[PBL] 开始加载多课标知识点索引...');
    const t0 = performance.now();

    // 定义所有课标体系及其树文件路径
    const systems = {
      cn: { path: './data/trees/cn/', label: '中国课标', tag: 'CN' },
      ap: { path: './data/trees/ap/', label: 'AP', tag: 'AP' },
      cambridge: { path: './data/trees/cambridge/', label: 'Cambridge', tag: 'CA' },
      ib: { path: './data/trees/ib/', label: 'IB', tag: 'IB' },
      us: { path: './data/trees/us/', label: 'US CCSS', tag: 'US' }
    };

    // 并行加载所有树目录的文件列表
    const treePromises = Object.entries(systems).map(async ([sysId, sysInfo]) => {
      try {
        const nodes = await this._loadSystemTrees(sysId, sysInfo);
        return { sysId, nodes, tag: sysInfo.tag, label: sysInfo.label };
      } catch (e) {
        console.warn(`[PBL] 加载 ${sysId} 树失败:`, e.message);
        return { sysId, nodes: [], tag: sysInfo.tag, label: sysInfo.label };
      }
    });

    const results = await Promise.all(treePromises);
    let totalNodes = 0;

    results.forEach(({ sysId, nodes, tag, label }) => {
      if (!this.systemIndex.has(sysId)) {
        this.systemIndex.set(sysId, new Set());
      }
      nodes.forEach(node => {
        const normalizedGrade = parseInt(node.grade) || 0;
        const normalizedTreePath = node.treePath || node.graph_path || node.tree_file || '';
        const curriculumLabel = this._inferCurriculumLabel(node, sysId, label, normalizedTreePath);
        const stageLabel = this._inferStageLabel(node, sysId, normalizedTreePath, normalizedGrade);
        // 统一格式，同时保留树节点原始字段（status/courses/domainColor/curriculum_points 等）
        let unified = {
          ...node,                              // 保留所有原始字段
          id: node.id,
          name: node.name || node.name_zh || '',
          name_en: node.name_en || '',
          subject: node.subject || '',
          domain: node.domain || '',
          domainColor: node.domainColor || '#3b82f6',
          grade: normalizedGrade,
          difficulty: node.difficulty || 0,
          definition: node.definition || node.description || '',
          key_concepts: node.key_concepts || [],
          prerequisites: node.prerequisites || [],
          extends: node.extends || [],
          parallel: node.parallel || [],
          status: node.status || '',
          courses: node.courses || [],
          curriculum_points: node.curriculum_points || [],
          system: sysId,
          systemTag: tag,
          systemLabel: label,
          curriculumLabel,
          stageLabel,
          gradeLabel: this._formatGradeLabel(normalizedGrade, sysId, normalizedTreePath, node.stage),
          treePath: normalizedTreePath,
          isExternal: false,
          fromCurriculumTree: true,
          fromK12Graph: false,
        };
        unified = this._normalizeUniversitySubjectNode(unified);
        this.unifiedIndex.set(node.id, unified);
        this.systemIndex.get(sysId).add(node.id);
        totalNodes++;
      });
      console.log(`[PBL] ${label}: ${nodes.length} 节点`);
    });

    this.loaded = true;
    const elapsed = (performance.now() - t0).toFixed(0);
    console.log(`[PBL] ✅ 统一索引就绪: ${totalNodes} 节点, ${elapsed}ms`);

    await this._loadKnowledgeGraph();

    this._persistUnifiedIndexCache();
    return this.unifiedIndex;
  }

  _normalizeNodeSourceFlags() {
    this.unifiedIndex.forEach((node, id) => {
      if (node.fromCurriculumTree == null) {
        const tp = String(node.treePath || '');
        node.fromCurriculumTree = !!(tp && (tp.includes('/trees/') || tp.startsWith('data/trees')));
      }
      if (node.fromK12Graph == null) {
        node.fromK12Graph = this.k12NodeIds?.has(id) || false;
      }
    });
  }

  // ─── 全科图谱增强：加载跨学科边数据 ──────────────────────────

  async _loadKnowledgeGraph() {
    if (this.graphLoaded) return;
    try {
      const t0 = performance.now();
      const resp = await fetch('./data/knowledge-map-data.json?t=' + Date.now());
      const data = await resp.json();

      const neighbors = this.graphNeighbors;
      const k12Ids = new Set();
      const uniIds = new Set();
      let k12Merged = 0;
      let uniAdded = 0;

      (data.nodes || []).forEach(n => {
        const grade = parseInt(n.grade, 10) || 0;
        const isK12 = grade >= 1 && grade <= 12;
        const isUni = grade === 0;
        if (isK12) k12Ids.add(n.id);
        if (isUni) uniIds.add(n.id);

        const base = {
          id: n.id,
          name: n.name || n.id,
          name_en: n.name_en || '',
          subject: n.subject || '',
          domain: n.domain || '',
          domainColor: n.domainColor || '#3b82f6',
          grade,
          difficulty: n.difficulty || 0,
          definition: n.definition || n.description || '',
          key_concepts: n.key_concepts || [],
          prerequisites: n.prerequisites || [],
          extends: n.extends || [],
          parallel: n.parallel || [],
          status: n.status || 'active',
          courses: n.courses || [],
          curriculum_points: n.curriculum_points || [],
          treePath: n.treePath || n.graph_path || '',
          isExternal: false,
          isUniversity: isUni,
          isK12: isK12,
        };

        if (isK12) {
          const prev = this.unifiedIndex.get(n.id);
          const unified = {
            ...(prev || {}),
            ...base,
            system: prev?.system || 'cn',
            systemTag: prev?.systemTag || 'CN',
            systemLabel: prev?.systemLabel || '中国课标',
            curriculumLabel: prev?.curriculumLabel || '中国课标',
            stageLabel: n.stageLabel || prev?.stageLabel || this._inferStageLabel(n, 'cn', base.treePath, grade),
            gradeLabel: prev?.gradeLabel || this._formatGradeLabel(grade, 'cn', base.treePath, n.stage),
            fromCurriculumTree: !!prev?.fromCurriculumTree,
            fromK12Graph: true,
          };
          this.unifiedIndex.set(n.id, unified);
          if (!this.systemIndex.has('cn')) this.systemIndex.set('cn', new Set());
          this.systemIndex.get('cn').add(n.id);
          k12Merged++;
        } else if (isUni && !this.unifiedIndex.has(n.id)) {
          this.unifiedIndex.set(n.id, {
            ...base,
            system: 'cn',
            systemTag: 'CN',
            systemLabel: '大学',
            curriculumLabel: '大学课程',
            stageLabel: '大学',
            gradeLabel: '大学',
          });
          if (!this.systemIndex.has('cn')) this.systemIndex.set('cn', new Set());
          this.systemIndex.get('cn').add(n.id);
          uniAdded++;
        }
      });

      (data.edges || []).forEach(e => {
        const src = e.source;
        const tgt = e.target;
        if (!neighbors.has(src)) neighbors.set(src, { parents: new Set(), children: new Set() });
        if (!neighbors.has(tgt)) neighbors.set(tgt, { parents: new Set(), children: new Set() });
        neighbors.get(src).children.add(tgt);
        neighbors.get(tgt).parents.add(src);
      });

      this.k12NodeIds = k12Ids;
      this.universityNodeIds = uniIds;
      this.graphEdges = data.edges || [];
      this.graphLoaded = true;
      this._normalizeNodeSourceFlags();
      const elapsed = (performance.now() - t0).toFixed(0);
      console.log(`[PBL] 🧬 K12全科图谱就绪: K12=${k12Ids.size}（合并${k12Merged}）, 大学=${uniIds.size}（新增${uniAdded}）, 边=${this.graphEdges.length}, ${elapsed}ms`);
    } catch (e) {
      console.warn('[PBL] 全科图谱加载失败（降级为无跨学科增强）:', e.message);
    }
  }

  _isK12Node(node) {
    if (!node) return false;
    if (node.isK12) return true;
    const g = parseInt(node.grade, 10) || 0;
    return g >= 1 && g <= 12;
  }

  _isUniversityNode(node) {
    if (!node) return false;
    if (node.isUniversity) return true;
    return (parseInt(node.grade, 10) || 0) === 0 && node.system === 'cn' && !node.isExternal;
  }

  /** 表单或目标是否锁定小学学段（1–6 年级） */
  _isPrimarySchoolContext(goal, projectSpec = null) {
    const band = this._parseExplicitGradeBand(goal, projectSpec || this._activeProjectSpec);
    return band.explicit && band.minGrade >= 1 && band.maxGrade <= 6;
  }

  /** 知识来源门控：课标树 / 全科图谱（可多选） */
  _passesKnowledgeSourceGate(node, projectSpec = null) {
    if (!node || node.isExternal || node.layer === 'external') return true;
    const spec = projectSpec || this._activeProjectSpec;
    const src = spec?.knowledgeSources || { curriculum: true, k12Graph: true };
    const wantCurriculum = src.curriculum !== false;
    const wantGraph = src.k12Graph !== false;
    if (wantCurriculum && wantGraph) return true;
    if (!wantCurriculum && !wantGraph) return true;
    if (node.system !== 'cn') return wantCurriculum;
    if (wantCurriculum && node.fromCurriculumTree) return true;
    if (wantGraph && (node.fromK12Graph || this.k12NodeIds?.has(node.id))) return true;
    return false;
  }

  /** 节点是否落在用户选定的学段内（默认锁定学段，不选更低学段课） */
  _passesGradeBandGate(node, goal, projectSpec = null) {
    if (!node || node.isExternal || node.layer === 'external') return true;
    const band = this._parseExplicitGradeBand(goal, projectSpec || this._activeProjectSpec);
    if (!band.explicit) return true;
    const grade = parseInt(node.grade, 10) || 0;
    if (band.minGrade === 0 && band.maxGrade === 0) {
      return !!(this._isUniversityNode(node) || node.isUniversity);
    }
    if (this._isUniversityNode(node) || node.isUniversity) return false;
    if (band.excludePriorBands && band.bandMin > 0 && node.system === 'cn' && grade > 0 && grade < band.bandMin) {
      return false;
    }
    if (band.selectedGrades?.size && node.system === 'cn' && grade > 0) {
      return band.selectedGrades.has(grade);
    }
    if (band.maxGrade <= 6) {
      if (node.system === 'cn') return grade >= band.minGrade && grade <= band.maxGrade;
      return false;
    }
    if (band.minGrade >= 7 && band.maxGrade <= 9) {
      if (node.system === 'cn' && grade > 0) return grade >= band.minGrade && grade <= band.maxGrade;
    }
    if (band.minGrade >= 10 && band.maxGrade <= 12) {
      if (node.system === 'cn' && grade > 0) return grade >= band.minGrade && grade <= band.maxGrade;
    }
    return true;
  }

  /** 成人/大学项目：优先使用大学层工程/计算机节点，避免退回 K12 课标 */
  _isAdultOrUniversityContext(goal, projectSpec = null) {
    const spec = projectSpec || this._activeProjectSpec;
    if (spec?.gradeLevel === 'adult' || spec?.gradeLevel === 'university') return true;
    const g = String(goal || '');
    return /成人|在职|大学|本科|高职|大一|大二|大三|大四|研究生|工程实施方案|企业|产业级/i.test(g);
  }

  /** 用户明确需要大学层拓展（默认 PBL 只匹配 K12 全科图谱子图） */
  _shouldAllowUniversityNodes(goal, projectSpec = null) {
    const spec = projectSpec || this._activeProjectSpec;
    if (this._isAdultOrUniversityContext(goal, spec)) return true;
    if (this._isPrimarySchoolContext(goal, spec)) return false;
    if (spec?.gradeLevel === 'primary' || spec?.gradeLevel === 'junior' || spec?.gradeLevel === 'senior') {
      return false;
    }
    const g = String(goal || '');
    return /竞赛拓展|高等数学|大学物理|大学化学/i.test(g);
  }

  /** 默认匹配池：CN 仅 K12（grade 1–12），国际课标保留；大学层按需开启 */
  _isMatchingPoolNode(node, goal) {
    if (!node || node.isExternal) return false;
    const adultOrUni = this._isAdultOrUniversityContext(goal);
    if (adultOrUni) return !!(this._isUniversityNode(node) || node.isUniversity);
    if (!this._shouldAllowUniversityNodes(goal) && this._isUniversityNode(node)) return false;
    if (!this._passesKnowledgeSourceGate(node)) return false;
    if (!this._passesGradeBandGate(node, goal)) return false;
    if (this._isPrimarySchoolContext(goal)) return node.system === 'cn';
    if (node.system !== 'cn') return true;
    if (this._shouldAllowUniversityNodes(goal)) return true;
    return this._isK12Node(node);
  }

  _getK12Pool(goal, pool = null) {
    const src = pool || [...this.unifiedIndex.values()];
    if (this._isAdultOrUniversityContext(goal)) {
      return src.filter(n => n.system === 'cn' && this._isMatchingPoolNode(n, goal));
    }
    return src.filter(n => n.system === 'cn' && this._isK12Node(n) && this._isMatchingPoolNode(n, goal));
  }

  /** 保底/检索用宽池：窄池不足时并回全科 K12 子图，避免只在 3 个候选里打转 */
  _getBroadCurriculumPool(goal, narrowPool = [], minSize = 50) {
    const archetype = this._resolveArchetype(goal);
    const allowed = this._getAllowedSubjects(goal, archetype);
    const subjectGate = (pool) => (allowed?.size
      ? pool.filter(n => allowed.has(n.subject))
      : pool);
    const full = subjectGate(this._getK12Pool(goal));
    if (!narrowPool?.length) return full;
    if (narrowPool.length >= minSize) return narrowPool;
    return this._unionCandidateNodes([narrowPool, full], Math.max(minSize * 4, 400));
  }

  /**
   * 确定性 K12 图谱检索：按蓝图 module hints + 项目 domain 从全科图谱子图取节点（LLM 失败时的硬保底）
   */
  _rescueFromK12KnowledgeGraph(goal, blueprint, archetype, limit = 8, pool = null, options = {}) {
    const floorMode = !!options.floorMode;
    const domains = this._inferProjectDomains(goal);
    const goalTerms = this._tokenizeGoalTerms(goal);
    const hintBlob = (blueprint?.schemes || [])
      .flatMap(s => (s.phases || []).flatMap(p => [...(p.knowledgeHints || []), p.phase, ...(p.steps || [])]))
      .join(' ');
    const allowed = this._getAllowedSubjects(goal, archetype);
    const basePool = (pool?.length >= 30 ? pool : null) || this._getK12Pool(goal);
    const specSubjects = this._subjectFilterFromProjectSpec(this._activeProjectSpec);
    const primaryCtx = this._isPrimarySchoolContext(goal);
    const k12Pool = basePool
      .filter(n => this._passesHardNodeGate(n, goal, archetype))
      .filter(n => !allowed?.size || allowed.has(n.subject))
      .map(n => ({
        ...n,
        _score: this._scoreUniversalRelevance(n, goal, blueprint, domains, archetype)
          + (hintBlob.split(/[、,，\s]+/).filter(h => h.length >= 2 && this._nodeSearchText(n).includes(h)).length * 2)
          + (primaryCtx && specSubjects?.includes(n.subject) ? 8 : 0)
          + (primaryCtx && goalTerms.some(t => t.length >= 2 && this._nodeSearchText(n).includes(t)) ? 4 : 0),
      }))
      .filter(n => n._score >= this._relevanceKeepThreshold(floorMode))
      .sort((a, b) => b._score - a._score);

    const picked = [];
    const seen = new Set();
    const roles = ['foundation', 'bridge', 'bridge', 'core', 'core', 'core', 'core', 'core'];

    k12Pool.forEach(n => {
      if (picked.length >= limit || seen.has(n.id)) return;
      seen.add(n.id);
      picked.push({
        ...n,
        confidence: Math.max(0.58, 0.85 - picked.length * 0.04),
        matchReason: 'K12全科图谱检索回退',
        pblRole: roles[picked.length] || 'core',
        _rescuedFromK12: true,
      });
    });

    const cleaned = this._purgeCurriculumNoise(picked, goal);
    if (cleaned.length) {
      console.warn('[PBL] K12图谱硬保底匹配:', cleaned.map(n => n.name).join('、'));
    }
    return cleaned.slice(0, limit);
  }

  /**
   * 获取节点的图谱邻居（跨学科前置+后续）
   * @param {string} nodeId
   * @param {number} depth - 遍历深度（1=直接邻居, 2=两层）
   * @returns {{ parents: string[], children: string[], crossSubject: string[] }}
   */
  getGraphNeighbors(nodeId, depth = 1) {
    if (!this.graphLoaded) return { parents: [], children: [], crossSubject: [] };
    const visited = new Set([nodeId]);
    let currentLayer = [nodeId];
    const allParents = new Set();
    const allChildren = new Set();

    for (let d = 0; d < depth; d++) {
      const nextLayer = [];
      currentLayer.forEach(id => {
        const nb = this.graphNeighbors.get(id);
        if (!nb) return;
        nb.parents.forEach(p => { if (!visited.has(p)) { allParents.add(p); nextLayer.push(p); visited.add(p); } });
        nb.children.forEach(c => { if (!visited.has(c)) { allChildren.add(c); nextLayer.push(c); visited.add(c); } });
      });
      currentLayer = nextLayer;
    }

    // 识别跨学科邻居
    const selfNode = this.unifiedIndex.get(nodeId);
    const selfSubject = selfNode ? selfNode.subject : '';
    const crossSubject = [];
    [...allParents, ...allChildren].forEach(id => {
      const n = this.unifiedIndex.get(id);
      if (n && n.subject && n.subject !== selfSubject) crossSubject.push(id);
    });

    return { parents: [...allParents], children: [...allChildren], crossSubject };
  }

  /**
   * 查找 K12 终端节点到大学节点的桥接路径
   * @param {string} k12NodeId - K12 节点 ID
   * @returns {string[]} 可达的大学节点 ID 列表
   */
  getUniversityBridges(k12NodeId) {
    if (!this.graphLoaded) return [];
    const nb = this.graphNeighbors.get(k12NodeId);
    if (!nb) return [];
    const bridges = [];
    nb.children.forEach(childId => {
      const child = this.unifiedIndex.get(childId);
      if (child && (child.grade === 0 || child.isUniversity)) bridges.push(childId);
    });
    return bridges;
  }

  // ─── 原有方法 ──────────────────────────

  async _loadSystemTrees(sysId, sysInfo) {
    // 获取该体系下所有子目录
    const allNodes = [];

    // 用已有数据源
    if (sysId === 'cn') {
      // 中国课标直接从 nodes-metadata 过滤 cn/ 路径，避免旧 fallback 把 IB/AP 等国际节点误标为 CN。
      try {
        const resp = await fetch('./data/nodes-metadata.json?t=' + Date.now());
        const data = await resp.json();
        (data.nodes || [])
          .filter(n => String(n.graph_path || n.tree_file || '').startsWith('cn/'))
          .forEach(n => allNodes.push({
            ...n,
            treePath: n.treePath || n.graph_path || n.tree_file || '',
            subject: n.subject || this._inferSubject(n.id)
          }));
      } catch (e) {
        console.warn(`[PBL] CN nodes-metadata.json 加载失败`);
      }
    } else {
      // 国际课标从各树文件加载
      const treeDirs = await this._discoverTreeDirs(sysInfo.path);
      const treePromises = treeDirs.map(async dir => {
        const files = await this._discoverTreeFiles(dir);
        const filePromises = files.map(async file => {
          try {
            const resp = await fetch(file + '?t=' + Date.now());
            const tree = await resp.json();
            return this._extractNodesFromTree(tree, sysId, file);
          } catch (e) {
            return [];
          }
        });
        const nodeArrays = await Promise.all(filePromises);
        return nodeArrays.flat();
      });
      const results = await Promise.all(treePromises);
      results.forEach(nodes => allNodes.push(...nodes));
    }

    return allNodes;
  }

  async _discoverTreeDirs(basePath) {
    // 静态站点无法列出目录，用真实存在的目录列表，避免对不存在路径发起大量 404 请求。
    const knownDirs = {
      ap: ['./data/trees/ap/high/'],
      cambridge: ['./data/trees/cambridge/al/', './data/trees/cambridge/igcse/', './data/trees/cambridge/lsec/', './data/trees/cambridge/primary/'],
      ib: ['./data/trees/ib/dp/', './data/trees/ib/myp/', './data/trees/ib/pyp/'],
      us: ['./data/trees/us/hs/', './data/trees/us/ms/', './data/trees/us/k5/']
    };
    const sysId = basePath.split('/').filter(Boolean).pop();
    return knownDirs[sysId] || [basePath];
  }

  async _discoverTreeFiles(dirPath) {
    // v7.11.2：按目录返回真实存在的树文件，避免 404 噪声，并覆盖 IB MYP/PYP、AP high、US hs/ms/k5。
    const knownFilesByDir = {
      './data/trees/ap/high/': ['biology','calculus-ab','calculus','chemistry','cs','english','physics-1','physics-c','us-history'],
      './data/trees/cambridge/al/': ['biology','chemistry','economics','english','further-math','math','physics'],
      './data/trees/cambridge/igcse/': ['biology','chemistry','cs','economics','english','global-persp','math','physics'],
      './data/trees/cambridge/lsec/': ['english','humanities','ict','math','science'],
      './data/trees/cambridge/primary/': ['computing','english','math','science'],
      './data/trees/ib/dp/': ['biology','cas','chemistry','economics','ee','english-a','history','math-aa','math-ai','physics','tok'],
      './data/trees/ib/myp/': ['arts','design','individuals-societies','language-acquisition','language-literature','mathematics','pe','sciences'],
      './data/trees/ib/pyp/': ['how-we-express','how-we-organize','how-world-works','sharing-planet','where-we-are','who-we-are'],
      './data/trees/us/hs/': ['algebra','biology','chemistry','ela','geometry','physics','precalc','us-history','world-history'],
      './data/trees/us/ms/': ['ela','math','science','social-studies'],
      './data/trees/us/k5/': ['ela','math','science','social-studies']
    };
    const files = knownFilesByDir[dirPath];
    if (files) return files.map(s => dirPath + s + '.json');
    return [];
  }

  _extractNodesFromTree(tree, sysId, treePath) {
    const nodes = [];
    const subject = tree.subject || '';
    const curriculum = tree.curriculum || '';
    const stage = tree.stage || '';

    const processDomain = (domain) => {
      (domain.nodes || []).forEach(node => {
        nodes.push({
          ...node,                       // 保留原始字段：status, courses, curriculum_points, definition 等
          subject: node.subject || subject,
          domain: node.domain || domain.name || domain.id || '',
          domainColor: domain.color || node.domainColor || '#3b82f6',  // 保留领域颜色
          curriculum: node.curriculum || curriculum,
          stage: node.stage || stage,
          treePath: treePath
        });
      });
    };

    if (tree.domains) {
      tree.domains.forEach(processDomain);
    } else if (tree.nodes) {
      tree.nodes.forEach(node => nodes.push({ ...node, subject, treePath }));
    }

    return nodes;
  }

  _inferSubject(id) {
    if (!id) return '';
    const prefix = id.split('-')[0] || id.split('_')[0];
    const map = { math: 'math', phys: 'physics', chem: 'chemistry', bio: 'biology', chi: 'chinese', eng: 'english', hist: 'history', geo: 'geography', info: 'info-tech', design: 'design' };
    return map[prefix] || '';
  }

  _inferCurriculumLabel(node, sysId, defaultLabel, treePath) {
    const raw = String(node.curriculum || '').toLowerCase();
    const path = String(treePath || '').toLowerCase();
    if (sysId === 'cn') return '中国课标';
    if (sysId === 'ap') return 'AP';
    if (sysId === 'cambridge') {
      if (path.includes('/primary/')) return 'Cambridge Primary';
      if (path.includes('/lsec/')) return 'Cambridge Lower Secondary';
      if (path.includes('/igcse/')) return 'Cambridge IGCSE';
      if (path.includes('/al/')) return 'Cambridge A Level';
      return 'Cambridge';
    }
    if (sysId === 'ib') {
      if (raw.includes('pyp') || path.includes('/pyp/')) return 'IB PYP';
      if (raw.includes('myp') || path.includes('/myp/')) return 'IB MYP';
      if (raw.includes('dp') || path.includes('/dp/')) return 'IB DP';
      return 'IB';
    }
    if (sysId === 'us') {
      if (path.includes('/k5/')) return 'US CCSS K-5';
      if (path.includes('/ms/')) return 'US CCSS Middle School';
      if (path.includes('/hs/')) return 'US CCSS High School';
      return 'US CCSS';
    }
    return defaultLabel || sysId || '';
  }

  _inferStageLabel(node, sysId, treePath, grade) {
    const stage = String(node.stage || '').toLowerCase();
    const path = String(treePath || '').toLowerCase();
    if (sysId === 'cn') {
      if (path.includes('/elementary/') || stage === 'elementary' || (grade >= 1 && grade <= 6)) return '小学';
      if (path.includes('/middle/') || stage === 'middle' || (grade >= 7 && grade <= 9)) return '初中';
      if (path.includes('/high/') || stage === 'high' || grade >= 10) return '高中';
      return '中国 K12';
    }
    if (sysId === 'ap') return '高中 / AP';
    if (sysId === 'cambridge') {
      if (path.includes('/primary/')) return 'Primary';
      if (path.includes('/lsec/')) return 'Lower Secondary';
      if (path.includes('/igcse/')) return 'IGCSE';
      if (path.includes('/al/')) return 'A Level';
    }
    if (sysId === 'ib') {
      if (path.includes('/pyp/') || stage === 'pyp') return 'PYP';
      if (path.includes('/myp/') || stage === 'myp') return 'MYP';
      if (path.includes('/dp/') || stage === 'dp') return 'DP';
    }
    if (sysId === 'us') {
      if (path.includes('/k5/')) return 'K-5';
      if (path.includes('/ms/')) return 'Middle School';
      if (path.includes('/hs/')) return 'High School';
    }
    return stage || '';
  }

  _universityTierSubjects() {
    return new Set(['computer-science', 'engineering']);
  }

  _normalizeUniversitySubjectNode(node) {
    if (!node || !this._universityTierSubjects().has(node.subject)) return node;
    if (node.grade === 0 && node.stage === 'university') return node;
    return {
      ...node,
      grade: 0,
      stage: 'university',
      stageLabel: '大学',
      gradeLabel: '大学',
    };
  }

  _formatGradeLabel(grade, sysId, treePath, stage) {
    const g = parseInt(grade) || 0;
    const path = String(treePath || '').toLowerCase();
    const st = String(stage || '').toLowerCase();
    if (!g || st === 'university') {
      if (st === 'university') return '大学';
      if (sysId === 'ib' && (st || path.includes('/ib/'))) return this._inferStageLabel({ stage }, sysId, treePath, g) || '通识';
      return '通识';
    }
    if (sysId === 'cn') {
      if (g <= 6) return `小学${g}年级`;
      if (g <= 9) return `初中${g - 6}年级`;
      if (g <= 12) return `高中${g - 9}年级`;
    }
    if (sysId === 'ib') {
      if (path.includes('/myp/') || st === 'myp') return `IB MYP · G${g}`;
      if (path.includes('/pyp/') || st === 'pyp') return `IB PYP · G${g}`;
      if (path.includes('/dp/') || st === 'dp') return `IB DP · G${g}`;
    }
    if (sysId === 'ap') return `AP · G${g}`;
    if (sysId === 'cambridge') return `${this._inferStageLabel({ stage }, sysId, treePath, g) || 'Cambridge'} · G${g}`;
    if (sysId === 'us') return `${this._inferStageLabel({ stage }, sysId, treePath, g) || 'US'} · G${g}`;
    return `G${g}`;
  }

  _metaLine(d) {
    return [d.curriculumLabel || d.systemLabel, d.stageLabel, d.gradeLabel, d.subject, d.domain]
      .filter(Boolean)
      .join(' · ');
  }

  _extractJsonObject(text) {
    const raw = String(text || '').replace(/```json\s*/g, '').replace(/```\s*/g, '').trim();
    const start = raw.indexOf('{');
    const end = raw.lastIndexOf('}');
    if (start >= 0 && end > start) return raw.slice(start, end + 1);
    return raw;
  }

  _safeJsonParse(text, fallback = null) {
    try {
      return JSON.parse(text);
    } catch (e) {
      if (/stack/i.test(String(e.message || ''))) {
        console.warn('[PBL] JSON 嵌套过深，已跳过解析:', e.message);
      }
      return fallback;
    }
  }

  static PBL_INDEX_CACHE_KEY = 'teachany_pbl_unified_index_v11';

  _slimNodeForCache(node) {
    if (!node) return node;
    return {
      id: node.id,
      name: node.name,
      name_en: node.name_en,
      subject: node.subject,
      domain: node.domain,
      domainColor: node.domainColor,
      grade: node.grade,
      difficulty: node.difficulty,
      definition: typeof node.definition === 'string' ? node.definition.slice(0, 400) : '',
      key_concepts: (node.key_concepts || []).slice(0, 8),
      prerequisites: (node.prerequisites || []).slice(0, 8),
      extends: (node.extends || []).slice(0, 4),
      parallel: (node.parallel || []).slice(0, 4),
      status: node.status,
      courses: (node.courses || []).slice(0, 3),
      curriculum_points: (node.curriculum_points || []).slice(0, 4),
      system: node.system,
      systemTag: node.systemTag,
      systemLabel: node.systemLabel,
      curriculumLabel: node.curriculumLabel,
      stageLabel: node.stageLabel,
      gradeLabel: node.gradeLabel,
      treePath: node.treePath,
      isExternal: !!node.isExternal,
      fromCurriculumTree: !!node.fromCurriculumTree,
      fromK12Graph: !!node.fromK12Graph,
      isUniversity: !!node.isUniversity,
      isK12: !!node.isK12,
    };
  }

  _safeStringify(value, label = 'payload') {
    try {
      return JSON.stringify(value);
    } catch (e) {
      if (!/stack|too much recursion/i.test(String(e.message || ''))) throw e;
      console.warn(`[PBL] ${label} 序列化栈溢出，已裁剪后重试`);
      const slim = { ...value };
      if (slim.projectBlueprint) slim.projectBlueprint = this._compactBlueprintForReview(slim.projectBlueprint);
      if (Array.isArray(slim.candidates)) slim.candidates = slim.candidates.slice(0, 36).map(n => this._enrichCandidateForMatch(n));
      return JSON.stringify(slim);
    }
  }

  _persistUnifiedIndexCache() {
    if (this._skipIndexCache) return;
    const CACHE_KEY = PBLPathBuilder.PBL_INDEX_CACHE_KEY;
    try {
      const entries = [];
      for (const [k, v] of this.unifiedIndex.entries()) {
        entries.push([k, this._slimNodeForCache(v)]);
        if (entries.length >= 10000) break;
      }
      localStorage.setItem(CACHE_KEY, JSON.stringify({ ts: Date.now(), v: 11, entries }));
    } catch (e) {
      console.warn('[PBL] 索引缓存写入跳过:', e.message);
      try { localStorage.removeItem(CACHE_KEY); } catch (_e) { /* ignore */ }
    }
  }

  /** 浅拷贝蓝图（避免 JSON 深拷贝在大蓝图时栈溢出） */
  _shallowCloneBlueprint(blueprint) {
    if (!blueprint) return blueprint;
    return {
      ...blueprint,
      reportOutline: Array.isArray(blueprint.reportOutline) ? [...blueprint.reportOutline] : blueprint.reportOutline,
      formativeCheckpoints: Array.isArray(blueprint.formativeCheckpoints) ? [...blueprint.formativeCheckpoints] : blueprint.formativeCheckpoints,
      collaborationRoles: Array.isArray(blueprint.collaborationRoles) ? blueprint.collaborationRoles.map(r => ({ ...r })) : blueprint.collaborationRoles,
      constraints: blueprint.constraints ? [...blueprint.constraints] : blueprint.constraints,
      scopeLimits: blueprint.scopeLimits ? [...blueprint.scopeLimits] : blueprint.scopeLimits,
      successCriteria: blueprint.successCriteria ? [...blueprint.successCriteria] : blueprint.successCriteria,
      subsystems: blueprint.subsystems ? blueprint.subsystems.map(s => ({ ...s })) : blueprint.subsystems,
      schemes: (blueprint.schemes || []).map(s => ({
        ...s,
        pros: s.pros ? [...s.pros] : s.pros,
        cons: s.cons ? [...s.cons] : s.cons,
        phases: (s.phases || []).map(p => ({
          ...p,
          steps: [...(p.steps || [])],
          knowledgeHints: p.knowledgeHints ? [...p.knowledgeHints] : p.knowledgeHints,
          tools: Array.isArray(p.tools) ? [...p.tools] : p.tools,
          acceptance: Array.isArray(p.acceptance) ? [...p.acceptance] : p.acceptance,
          knowledgeScenes: Array.isArray(p.knowledgeScenes) ? p.knowledgeScenes.map(x => ({ ...x })) : p.knowledgeScenes,
          subsystemIds: p.subsystemIds ? [...p.subsystemIds] : p.subsystemIds,
        })),
      })),
    };
  }

  _normalizeGraphData(graphData) {
    if (!graphData) return { nodes: [], links: [] };
    return {
      ...graphData,
      nodes: Array.isArray(graphData.nodes) ? graphData.nodes : [],
      links: Array.isArray(graphData.links) ? graphData.links : [],
    };
  }

  _asStringArray(val) {
    return Array.isArray(val) ? val.filter(v => v != null && String(v).trim()) : [];
  }

  _cloneBlueprint(blueprint) {
    if (!blueprint) return blueprint;
    try {
      if (typeof structuredClone === 'function') return structuredClone(blueprint);
      return JSON.parse(JSON.stringify(blueprint));
    } catch (e) {
      console.warn('[PBL] 蓝图深拷贝失败，使用浅拷贝:', e.message);
      return this._shallowCloneBlueprint(blueprint);
    }
  }

  /** 限制 LLM 蓝图体量，避免异常 JSON/重复加厚导致栈溢出 */
  _pruneDecomposeBlueprint(data) {
    if (!data || typeof data !== 'object') return data;
    const bp = { ...data };
    bp.schemes = (bp.schemes || []).slice(0, 3).map(s => ({
      ...s,
      pros: (s.pros || []).slice(0, 4),
      cons: (s.cons || []).slice(0, 4),
      phases: (s.phases || []).slice(0, 6).map(p => ({
        ...p,
        steps: (p.steps || []).slice(0, 5).map(st => String(st).slice(0, 280)),
        knowledgeHints: (p.knowledgeHints || []).slice(0, 6),
      })),
    }));
    if (typeof bp.projectSummary === 'string') bp.projectSummary = bp.projectSummary.slice(0, 320);
    if (typeof bp.deliverable === 'string') bp.deliverable = bp.deliverable.slice(0, 120);
    bp.constraints = (bp.constraints || []).slice(0, 6);
    bp.scopeLimits = (bp.scopeLimits || []).slice(0, 6);
    bp.successCriteria = (bp.successCriteria || []).slice(0, 6);
    bp.reportOutline = this._asStringArray(bp.reportOutline).slice(0, 8);
    bp.formativeCheckpoints = this._asStringArray(bp.formativeCheckpoints).slice(0, 8);
    if (!Array.isArray(bp.collaborationRoles)) bp.collaborationRoles = [];
    return bp;
  }

  /** 中文 PBL 目标分词：无空格时不能用 split，否则候选排序与关键词降级都会失效 */
  _tokenizeGoalTerms(goal) {
    const raw = String(goal || '').trim().toLowerCase();
    const split = raw.split(/[\s,，、;；：:.!?！？\n]+/).filter(w => w.length >= 2);
    if (split.length > 1) return [...new Set(split)];
    const g = split[0] || raw;
    const terms = new Set();
    const lex = [
      '火箭', '导弹', '发射', '抛体', '抛物', '弹道', '空气动力', '推进', '燃料', '推进剂',
      '牛顿', '动量', '力学', '受力', '运动', '加速度', '能量', '守恒', '冲量',
      '传感', '控制', '电路', '编程', '算法', '物联', '智能', '温度', '湿度',
      '函数', '三角', '矢量', '向量', '建模', '实验', '数据', '分析',
      '化学', '燃烧', '氧化', '流体', '压强', '热值', '内能', '气动',
      '材料', '结构', '设计', '制作', '模型', '搭建', '探究', '温室', '天气',
      '新能源', '光伏', '太阳能', '风电', '风能', '储能', '电池', '锂电', '充电',
      '发电', '电能', '电动', '能源', '碳中和', '并网', '逆变', '电磁', '电路',
      '购车', '买车', '选车', '燃油', '油耗', '混动', '对比', '家用', '成本', '预算',
      '垃圾', '分类', '回收', '环保', '社区', '调查', '问卷', '访谈', '废弃物', '治理',
      '自动驾驶', '小车', '循迹', '巡线', '避障', '传感', '电机', '控制', '调试', '机器人'
    ];
    lex.forEach(w => { if (g.includes(w)) terms.add(w); });
    // 领域词典命中足够时不再用二字随机切分，避免「设计并」等噪声匹配无关课标
    if (terms.size < 4) {
      const cjk = g.replace(/[^\u4e00-\u9fff]/g, '');
      for (let i = 0; i < cjk.length - 1; i++) terms.add(cjk.slice(i, i + 2));
    }
    if (typeof PBLTopicAnchors !== 'undefined') {
      (PBLTopicAnchors.inferTopicKnowledgeAnchors(goal).recallTerms || [])
        .slice(0, 20).forEach(t => terms.add(t));
    }
    return [...terms].filter(t => t.length >= 2).slice(0, 40);
  }

  /** 题目语义锚点：地点/时代/主题 → 召回词与学科倾向（不限项目类型） */
  _getTopicAnchors(goal) {
    const key = String(goal || '');
    if (!this._topicAnchorCache) this._topicAnchorCache = new Map();
    if (!this._topicAnchorCache.has(key)) {
      const empty = { recallTerms: [], subjects: [], places: [], periods: [], hints: '', strong: false };
      const anchors = (typeof PBLTopicAnchors !== 'undefined' && PBLTopicAnchors.inferTopicKnowledgeAnchors)
        ? PBLTopicAnchors.inferTopicKnowledgeAnchors(key)
        : empty;
      this._topicAnchorCache.set(key, anchors);
    }
    return this._topicAnchorCache.get(key);
  }

  _scoreTopicAnchorRelevance(node, goal) {
    const anchors = this._getTopicAnchors(goal);
    if (!anchors?.strong) return 0;
    if (typeof PBLTopicAnchors !== 'undefined' && PBLTopicAnchors.scoreNodeAgainstAnchors) {
      return PBLTopicAnchors.scoreNodeAgainstAnchors(node, anchors, (n) => this._nodeSearchText(n));
    }
    return 0;
  }

  _nodeMatchesTopicAnchors(node, goal, minScore = 6) {
    return this._scoreTopicAnchorRelevance(node, goal) >= minScore;
  }

  /** 消费决策/调查对比类（购车选型、方案比选），非工程研发 */
  _isConsumerDecisionGoal(goal) {
    const g = String(goal || '');
    if (/研究.*购车|研究.*买车|研究.*选车|购车.*研究|买车.*研究/.test(g)) return true;
    if (/购车|买车|选车|用车方案|消费决策|方案比选|比选|选型|性价比|家用.*车|家庭.*(购车|买车|选车|用车)/.test(g)) return true;
    if (/对比|比较/.test(g) && /购|买|选|家用|家庭/.test(g) && /新能源|燃油|电动|混动|汽油|柴油/.test(g)) return true;
    if (/哪个更|哪种更|怎么选|如何选择/.test(g) && /车|新能源|燃油|电动/.test(g)) return true;
    if (/新.{0,2}旧.{0,2}能源|油电混合|油电对比|燃油车|电动车|电车|混动车/.test(g) && /车|汽车|选|购|买|方案|对比|比较/.test(g)) return true;
    if (/(车|汽车|轿车|SUV)/.test(g) && /新能源|燃油|电动|混动|油电|汽油|柴油/.test(g) && /选|购|买|对比|比较|方案|推荐|决策|建议/.test(g)) return true;
    if (/选.{0,4}(车|汽车)/.test(g) || /(车|汽车).{0,4}选/.test(g)) return true;
    return false;
  }

  _isEnergyEngineeringGoal(goal) {
    const g = String(goal || '');
    if (this._isEnergyAnalysisGoal(g)) return false;
    if (this._isConsumerDecisionGoal(g)) return false;
    if (/(车|汽车|轿车|SUV|用车)/.test(g) && /新能源|燃油|电动|混动|油电/.test(g) && !/设计|制作|研发|装置|系统开发|搭建|发明|工程化|发电|储能装置/.test(g)) return false;
    if (/对比|比较|选购|购车|买车|选车|家用|家庭/.test(g) && !/设计|制作|研发|装置|系统开发|搭建|发电|储能|并网|逆变/.test(g)) {
      if (/新能源|电动|燃油|混动|光伏|储能/.test(g)) return false;
    }
    return /新能源|光伏|太阳能|风电|风力|储能|电池|锂电|充电|发电|电能|清洁能源|碳中和|能源车|并网|逆变/.test(g)
      && /设计|制作|研发|装置|系统|搭建|工程|发电|储能|模型|实验|探究/.test(g);
  }

  /** 校园建筑能耗调查与节能改造建议（非光伏测算） */
  _isCampusEnergyEfficiencyGoal(goal) {
    const g = String(goal || '');
    return /校园节能|节能建议|建筑能耗|能耗调查|用电调查|节能改造|教学楼.*节能|教室.*节能|空调.*节能|照明.*节能/.test(g)
      || (/节能|能耗/.test(g) && /校园|教学楼|教室|建议|方案|改造|调查|用电|用水|空调|照明/.test(g));
  }

  /** 光伏/能源收益测算类（数据分析报告，非硬件制作） */
  _isEnergyAnalysisGoal(goal) {
    const g = String(goal || '');
    if (this._isCampusEnergyEfficiencyGoal(g)) return false;
    if (/光伏|太阳能|发电潜力|发电收益|屋顶.*光伏|碳减排效益/.test(g)
      && /测算|估算|调查|分析|收益|减排|用电|日照|潜力|效益/.test(g)
      && !/接线|原型|传感器|水泵|搭建|制作|组装|烧录|GPIO/.test(g)) return true;
    return false;
  }

  /** 化学溶液/浓度/厨房化学等探究类（以 chemistry 为主线） */
  _isChemistryInquiryGoal(goal) {
    const g = String(goal || '');
    return /浓度|溶液|溶解度|溶质|溶剂|饱和溶液|质量分数|体积分数|物质的溶解|配制溶液|混合溶液/.test(g)
      || /食盐|盐水|醋酸|苏打|洁厕|电解水|酸碱|中和|化学变化|物质的变化|离子反应/.test(g)
      || /滴定|硝酸银|电导率|莫尔法|沉淀滴定|标准溶液|物质的量浓度/.test(g)
      || /食堂|菜汤|汤水|汤汁|汤品|卤水/.test(g)
      || (/厨房|餐桌|调味|烹饪|汤/.test(g) && /盐|酸|碱|醋|化学|浓度|溶液|溶解|测|含量/.test(g));
  }

  /**
   * 混合溶液/真实样品浓度测定：无法直接称量分离溶质 → 滴定法或电导率法等间接测定
   */
  _getChemistryAnalysisProfile(goal) {
    const g = String(goal || '');
    const mixed = /混合溶液|食堂|菜汤|汤水|汤汁|汤品|卤水|景区水|河水|废水|不能直接|无法.*分离|不能.*称量|不能.*称重/.test(g)
      || (/汤/.test(g) && /食堂|餐厅|厨房|测定|检测|含量|浓度|盐/.test(g))
      || /滴定|硝酸银|电导率|间接测定/.test(g);
    const wantsTitration = /滴定|硝酸银|AgNO|莫尔|沉淀滴定|氯离子|Cl⁻|Cl-/.test(g);
    const wantsConductivity = /电导率|电导|导电率|电解质.*导电/.test(g);
    const methods = [];
    if (wantsTitration) methods.push('titration');
    if (wantsConductivity) methods.push('conductivity');
    if (mixed && !methods.length) methods.push('titration', 'conductivity');
    return {
      mixed,
      methods,
      primary: methods[0] || (mixed ? 'titration' : 'direct'),
      sampleLabel: /食堂|菜汤|汤水/.test(g) ? '食堂汤水' : (/混合溶液/.test(g) ? '混合溶液' : '样品溶液')
    };
  }

  _mixedSolutionChemistryDomains() {
    return [
      {
        id: 'constraint', label: '测定约束与方案选型',
        keywords: ['混合溶液', '无法分离', '间接测定', '取样', '稀释', '方案', '比较', '滴定', '电导率'],
        subjects: ['chemistry']
      },
      {
        id: 'titration', label: '硝酸银滴定法',
        keywords: ['滴定', '硝酸银', '沉淀', '氯离子', '银离子', '物质的量浓度', '标准溶液', '终点'],
        subjects: ['chemistry']
      },
      {
        id: 'conductivity', label: '电导率法',
        keywords: ['电导率', '电解质', '导电', '离子浓度', '标准曲线', '溶液'],
        subjects: ['chemistry', 'physics']
      },
      {
        id: 'calc', label: '数据处理与换算',
        keywords: ['物质的量', '浓度', '计算', '误差', '统计', '平行', '换算', '摩尔'],
        subjects: ['math', 'chemistry']
      },
      {
        id: 'report', label: '结论与应用',
        keywords: ['报告', '分析', '比较', '结论', '安全', '标准', '含量'],
        subjects: ['chemistry', 'chinese', 'math']
      }
    ];
  }

  _directSolutionChemistryDomains() {
    return [
      {
        id: 'solution', label: '溶液与浓度概念',
        keywords: ['溶液', '溶质', '溶剂', '浓度', '质量分数', '溶解', '饱和', '配制', '氯化钠', '溶解度'],
        subjects: ['chemistry']
      },
      {
        id: 'experiment', label: '实验设计与测量',
        keywords: ['实验', '变量', '对照', '量取', '称量', '配制', '测量', '滴定', '观察'],
        subjects: ['chemistry', 'science']
      },
      {
        id: 'data', label: '数据处理与表达',
        keywords: ['数据', '统计', '图表', '计算', '误差', '记录', '百分比', '平均数'],
        subjects: ['math']
      },
      {
        id: 'application', label: '生活情境与结论',
        keywords: ['厨房', '食盐', '应用', '安全', '生活', '结论', '报告', '分析', '比较'],
        subjects: ['chemistry', 'science', 'chinese']
      }
    ];
  }

  /** 历史课标节点（朝代/革命/战争等），消费决策与多数非历史项目须剔除 */
  _isHistoryCurriculumNode(node) {
    const sub = String(node?.subject || '');
    if (['history', 'advanced-history'].includes(sub)) return true;
    const name = String(node?.name || '');
    return /历史背景|朝代|元代|元朝|宋朝|宋代|唐朝|隋唐|明清|西汉|东汉|蒙古|丝绸之路|世界大战|资产阶级|革命|改革开放|秦始皇|工业革命|文艺复兴|冷战|新航路|殖民|封建|帝国|奴隶社会|封建社会|通史|古代史|近代史|现代史/.test(name);
  }

  /** 学科限制：表单显式指定优先；光伏/能源测算等类型锁定物理+数学+地学，避免「能量」误召回生物 */
  _getAllowedSubjects(goal, archetype = null) {
    const specSubjects = this._subjectFilterFromProjectSpec(this._activeProjectSpec);
    if (specSubjects?.length) return new Set(specSubjects);
    if (this._isEnergyAnalysisGoal(goal)) {
      return new Set(['physics', 'math', 'science', 'geography', 'chinese', 'info-tech']);
    }
    return null;
  }

  /** 小学数学/货币情境（购物、义卖记账等） */
  _isPrimaryCommerceGoal(goal) {
    return /小卖部|购物|找零|小票|义卖|记账|人民币|付款|收入.*图表|模拟.*购物/.test(String(goal || ''));
  }

  /** 非 PBL 典型输入（课件生成、单题、纯复习）— 仍允许继续，但收紧学科路由 */
  _detectNonPBLGoal(goal) {
    const g = String(goal || '');
    if (/帮我生成|生成.*课件|制作.*课件|TeachAny.*课件|交互式课件/.test(g)) {
      return { kind: 'courseware', hint: '这更像「课件生成」请求；PBL 拆解请描述可交付的项目任务（调查、制作、报告等）' };
    }
    if (/如图|△|∠|cm\/s|当点.*运动|四边形.*全等|求证|证明题/.test(g)) {
      return { kind: 'math-problem', hint: '这是单道数学题，不是 PBL 项目；请改为「设计…探究…报告」类任务描述' };
    }
    if (/复习|下册|一轮复习|怎么学|教我|帮我理解|教我怎么读/.test(g)
      && !/项目|设计|制作|调查|探究|报告|方案|策划/.test(g)) {
      return { kind: 'tutoring', hint: '这是学科辅导/复习请求，不是 PBL 项目拆解' };
    }
    if (/上册语文|下册语文|上册数学|Unit\s*\d/i.test(g) && !/项目|设计|调查|报告/.test(g)) {
      return { kind: 'curriculum', hint: '这是教材章节名；请补充具体项目任务与交付物' };
    }
    return null;
  }

  _isSubjectAllowedForGoal(node, goal, archetype = null) {
    const allowed = this._getAllowedSubjects(goal, archetype);
    if (!allowed) return true;
    return allowed.has(node.subject);
  }

  _collectBlueprintHints(blueprint, archetype = null) {
    const hints = new Set();
    const add = (s) => {
      const t = String(s || '').trim();
      if (t.length >= 2) hints.add(t);
    };
    if (blueprint?.deliverable) add(blueprint.deliverable);
    if (blueprint?.knowledgeChain) {
      String(blueprint.knowledgeChain).split(/[→、,，\s]+/).forEach(add);
    }
    (blueprint?.schemes || []).forEach(s => (s.phases || []).forEach(p => {
      (p.knowledgeHints || []).forEach(add);
      add(p.phase);
      add(p.deliverable);
      (p.steps || []).forEach(step => {
        String(step).match(/[\u4e00-\u9fff]{2,12}/g)?.forEach(add);
      });
    }));
    if (this._archetypeEngine) {
      this._archetypeEngine.blueprintModules(blueprint).forEach(m => (m.hints || []).forEach(add));
    }
    (archetype?.modules || []).forEach(m => (m.hints || []).forEach(add));
    return [...hints];
  }

  _relevanceKeepThreshold(floorMode = false) {
    return floorMode ? 5 : 7;
  }

  /** 泛化相关性：目标词 + 蓝图线索 + 领域词 + 节点文本重叠 */
  _scoreUniversalRelevance(node, goal, blueprint = null, domains = null, archetype = null) {
    if (!node) return -99;
    const g = String(goal || '');
    const domainsList = domains?.length ? domains : this._inferProjectDomains(g);
    const goalTerms = this._tokenizeGoalTerms(g);
    const anchors = this._getTopicAnchors(g);
    const hints = this._collectBlueprintHints(blueprint, archetype);
    const text = this._nodeSearchText(node);
    const name = String(node.name || '');
    let score = 0;

    score += this._scoreTopicAnchorRelevance(node, g);

    goalTerms.forEach(t => {
      if (t.length < 2) return;
      if (name.includes(t)) score += 5;
      else if (text.includes(t)) score += 2;
    });
    hints.forEach(h => {
      if (name.includes(h)) score += 7;
      else if (text.includes(h)) score += 3;
    });
    score += this._scoreNodeForDomains(node, domainsList);
    if (domainsList.some(d => (d.subjects || []).includes(node.subject))) score += 2;

    if (this._shouldPurgeChemistryForGoal(g) && node.subject === 'chemistry' && this._isOffTopicChemistryNode(node)) score -= 45;
    if (this._isEnergyAnalysisGoal(g)) {
      if (/光伏|太阳能|光电|电功率|电能|能量转化|能量守恒|欧姆|电路|电流|电压|一次函数|函数模型|统计|百分/.test(`${name} ${text}`)) score += 14;
      if (node.subject === 'math' && /函数|统计|百分|计算|数据|方程/.test(name)) score += 8;
      if (node.subject === 'physics' && /能量|电|光|功率|电路|欧姆/.test(name)) score += 8;
      if (this._isOffTopicGeographyClimateNode(node)) score -= 55;
      if (node.subject === 'chemistry' && /热化学|焓变|有机/.test(`${name} ${text}`)) score -= 45;
      if (this._isBiologyHealthNode(node) || node.subject === 'biology') score -= 80;
    }
    if (this._isGenericTransversalNode(name, g)) score -= 40;
    if (!this._shouldAllowUniversityNodes(g) && this._isUniversityNode(node)) score -= 35;
    if (archetype && this._isArchetypeBanned(node, archetype)) score -= 60;
    if (this._isK12Node(node)) score += 2;

    const anchorBlob = (anchors.recallTerms || []).join(' ');
    const contextBlob = `${g} ${hints.join(' ')} ${anchorBlob} ${domainsList.map(d => `${d.label} ${(d.keywords || []).join('')}`).join(' ')}`;
    const subjectExpected = new Set(anchors.subjects || []);
    const subjectSignals = {
      history: /历史|朝代|文物|革命|战争|史|考古|中世纪|中古|欧洲|英国|文明/,
      biology: /生物|细胞|遗传|生态|光合|酶|器官|人体|病毒|细菌/,
      geography: /地理|环境|气候|污染|排放|地图|区域|资源|地形|区位|国家|世界/,
    };
    const sig = subjectSignals[node.subject];
    if (sig && !sig.test(contextBlob) && !sig.test(name) && !sig.test(text)) {
      if (!subjectExpected.has(node.subject) && this._scoreTopicAnchorRelevance(node, g) < 4) score -= 10;
    }
    if (subjectExpected.has(node.subject) && this._nodeMatchesTopicAnchors(node, g, 4)) score += 4;

    if (this._isPrimarySchoolContext(g)) {
      const specSubjects = this._subjectFilterFromProjectSpec(this._activeProjectSpec);
      if (specSubjects?.includes(node.subject)) score += 6;
      if (/购物|找零|人民币|记账|收入|小票/.test(g) && node.subject === 'math'
        && /人民币|加减|乘|除|万以内|数的认识|统计|象形|条形|折线/.test(name)) score += 12;
      if (/购物|找零|人民币|记账/.test(g) && node.subject === 'science'
        && !/测量|数据|记录/.test(name)) score -= 10;
      if (/植物|生长|观察/.test(g) && node.subject === 'science'
        && /植物|生长|种子|测量|记录/.test(name)) score += 10;
      if (/统计|平均|调查|图表/.test(g) && node.subject === 'math'
        && /统计|平均|百分|分数|小数|条形|折线|扇形/.test(name)) score += 8;
    }

    return score;
  }

  _passesHardNodeGate(node, goal, archetype = null) {
    if (!node) return false;
    if (node.isExternal || node.layer === 'external' || String(node.id || '').startsWith('ext-')) return true;
    if (!this._shouldAllowUniversityNodes(goal) && this._isUniversityNode(node)) return false;
    if (!this._passesKnowledgeSourceGate(node)) return false;
    if (!this._passesGradeBandGate(node, goal)) return false;
    if (archetype && this._isArchetypeBanned(node, archetype)) return false;
    if (!this._isSubjectAllowedForGoal(node, goal, archetype)) return false;
    if (this._shouldPurgeBiologyForGoal(goal) && this._isBiologyHealthNode(node)) return false;
    if (this._shouldPurgeOffTopicScienceForGoal(goal) && this._isOffTopicScienceNoiseNode(node)) return false;
    if (this._isGenericTransversalNode(node.name, goal)) return false;
    return true;
  }

  _shouldAttachPrerequisite(preNode, childNode, goal, blueprint, domains, archetype) {
    if (!preNode || !childNode) return false;
    if (!this._passesHardNodeGate(preNode, goal, archetype)) return false;
    const preScore = this._scoreUniversalRelevance(preNode, goal, blueprint, domains, archetype);
    const childScore = this._scoreUniversalRelevance(childNode, goal, blueprint, domains, archetype);
    if (preScore < 5) return false;
    if (preNode.subject !== childNode.subject && preScore < Math.max(6, childScore * 0.45)) return false;
    return true;
  }

  _stripVerbPrefix(text) {
    return String(text || '').trim()
      .replace(/^(?:设计|制作|开发|建造|完成|策划|撰写|探究|调查|分析|探寻|探索|研究|调研|记录|重塑|改造|优化|重建|更新|升级|整治|组织|开展|修复|翻新)(?:一个|一款|一份|一组|一次)?\s*/, '')
      .replace(/^(?:关于|围绕|有关)\s*/, '')
      .replace(/[，。；].*$/, '')
      .trim();
  }

  _parseGoalSubject(goal) {
    const g = String(goal || '').trim();
    const taskMatch = g.match(/【任务】\s*(.+?)(?:\n|【|$)/);
    if (taskMatch) {
      const task = this._stripVerbPrefix(taskMatch[1]);
      return task.slice(0, 36) || g.slice(0, 36);
    }
    if (g.includes('｜')) {
      const parts = g.split('｜').map(s => s.trim()).filter(Boolean);
      const metaRe = /^(产出|场景|周期|约束):/;
      const skipRe = /^(小学|初中|高中|大学|成人|跨学科|数学|物理|化学|生物|科学|语文|英语|历史|地理|信息技术|艺术)$/;
      const taskParts = parts.filter(p => !metaRe.test(p));
      while (taskParts.length && (skipRe.test(taskParts[0]) || /年级/.test(taskParts[0]))) {
        taskParts.shift();
      }
      if (taskParts.length) {
        const task = this._stripVerbPrefix(taskParts.join(' '));
        return task.slice(0, 36) || g.slice(0, 36);
      }
    }
    const subject = this._stripVerbPrefix(g);
    return subject.slice(0, 36) || g.slice(0, 36);
  }

  _containsGoalMarkup(text) {
    return /【[^】]+】/.test(String(text || ''));
  }

  /** 剥离 AI 误注入的【学科】【任务】等结构化标签与 goal 全文回声 */
  _stripGoalMarkup(text, goal = '') {
    let s = String(text || '').trim();
    if (!s) return '';
    s = s.replace(/^【学科】[^】]*【任务】[^」\n]*」?\s*/g, '');
    s = s.replace(/【任务】\s*[^」\n]*」?\s*/g, '');
    s = s.replace(/【[^】]+】\s*/g, '');
    // 短蓝图脚手架（「主题」锚点）勿剥离核心主题词，否则会留下空「 」
    if (s.length <= 96 && /「[^」]{1,28}」/.test(s)) {
      return s.replace(/\s+/g, ' ').trim();
    }
    const task = this._parseGoalSubject(goal);
    if (task && task.length >= 4) {
      const esc = task.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      s = s.replace(new RegExp(esc, 'g'), ' ').trim();
    }
    s = s.replace(/\s+/g, ' ').trim();
    return s;
  }

  _sanitizeBlueprintText(text, goal) {
    const s = this._stripGoalMarkup(text, goal);
    if (!s) return '';
    if (s.length > 42) {
      const tail = s.match(/(?:立意|素材|初稿|批注|清单|素材库|诗集|朗诵|修改|阅读|表达|阶段|报告|方案)[^，。；]{0,16}/);
      if (tail) return tail[0].trim();
      return s.slice(0, 42);
    }
    return s;
  }

  _sanitizeDeliverableTitle(name, goal) {
    const art = this._compactProjectLabel(goal);
    let s = this._stripGoalMarkup(name, goal).replace(/^《+|》+$/g, '').trim();
    if (this._isEnergyAnalysisGoal(goal) && /测算|收益|减排|论证|图表|记录表/.test(s) && s.length >= 8) {
      return s.includes(art) ? s : `${art}：${s}`;
    }
    if (!s || this._containsGoalMarkup(s) || s.length > 24) {
      const hint = s.match(/(?:立意清单|素材库|初稿集|批注集|诗集|朗诵|展示|报告|方案|记录表)/);
      const short = hint ? hint[0] : (this._cleanPhaseName(s) || '阶段产出');
      return `《${art}·${short}》`;
    }
    if (!s.includes(art)) return `《${art}·${s}》`;
    return `《${s}》`;
  }

  _isHumanitiesLiteraryGoal(goal) {
    return this._classifyProjectType(goal) === 'humanities-literary';
  }

  _normalizeGradeDetails(spec) {
    if (!spec) return [];
    if (Array.isArray(spec.gradeDetails) && spec.gradeDetails.length) {
      return spec.gradeDetails.map(g => parseInt(g, 10)).filter(g => g >= 1 && g <= 12);
    }
    const single = parseInt(spec.gradeDetail, 10);
    return single >= 1 && single <= 12 ? [single] : [];
  }

  _gradeBandFromProjectSpec(spec) {
    if (!spec || !spec.gradeLevel || spec.gradeLevel === 'any') {
      return { explicit: false, minGrade: 1, maxGrade: 12, label: null };
    }
    const lockBand = spec.lockGradeBand !== false;
    const details = this._normalizeGradeDetails(spec);
    const maps = {
      primary: { min: 1, max: 6, label: '小学' },
      junior: { min: 7, max: 9, label: '初中' },
      senior: { min: 10, max: 12, label: '高中' },
      university: { min: 0, max: 0, label: '大学' },
      adult: { min: 0, max: 0, label: '成人' },
    };
    const band = maps[spec.gradeLevel];
    if (!band) return { explicit: false, minGrade: 1, maxGrade: 12, label: null };
    const excludePriorBands = lockBand && band.min > 0;
    if (details.length) {
      const inBand = details.filter(g => g >= band.min && g <= band.max);
      const picked = inBand.length ? inBand : details;
      const minGrade = Math.min(...picked);
      const maxGrade = Math.max(...picked);
      const label = picked.length === 1 ? `${picked[0]}年级` : `${picked.join('、')}年级`;
      return {
        explicit: true,
        minGrade,
        maxGrade,
        label,
        bandMin: band.min,
        bandMax: band.max,
        selectedGrades: new Set(picked),
        excludePriorBands,
        lockBand,
      };
    }
    if (spec.gradeLevel === 'primary' && details.length === 0) {
      return {
        explicit: true,
        minGrade: band.min,
        maxGrade: band.max,
        label: band.label,
        bandMin: band.min,
        bandMax: band.max,
        excludePriorBands,
        lockBand,
      };
    }
    return {
      explicit: true,
      minGrade: band.min,
      maxGrade: band.max,
      label: band.label,
      bandMin: band.min,
      bandMax: band.max,
      excludePriorBands,
      lockBand,
    };
  }

  _subjectFilterFromProjectSpec(spec) {
    if (!spec) return null;
    if (Array.isArray(spec.subjects) && spec.subjects.length) {
      const ids = spec.subjects.filter(id => id && id !== 'cross');
      return ids.length ? ids : null;
    }
    if (!spec.subject || spec.subject === 'cross') return null;
    return [spec.subject];
  }

  /** 用户是否在目标中写明年级/学段（未写明则跨学段匹配，仅作理解深度参考） */
  _parseExplicitGradeBand(goal, projectSpec = null) {
    if (projectSpec) {
      const fromSpec = this._gradeBandFromProjectSpec(projectSpec);
      if (fromSpec.explicit) return fromSpec;
    }
    const g = String(goal || '');
    const cnNum = { 一: 1, 二: 2, 三: 3, 四: 4, 五: 5, 六: 6, 七: 7, 八: 8, 九: 9 };
    if (/成人|在职|继续教育|培训/.test(g)) return { explicit: true, minGrade: 0, maxGrade: 0, label: '成人' };
    if (/大学|本科|高职|大一|大二|大三|大四/.test(g)) return { explicit: true, minGrade: 0, maxGrade: 0, label: '大学' };
    if (/高中|高一|高二|高三|十年级|十一年级|十二年级/.test(g)) return { explicit: true, minGrade: 10, maxGrade: 12, label: '高中' };
    if (/初中|初一|初二|初三|七年级|八年级|九年级/.test(g)) return { explicit: true, minGrade: 7, maxGrade: 9, label: '初中' };
    if (/【学段】\s*小学|【受众[\/\\]场景】\s*小学|面向.{0,8}小学|小学\s*食堂/.test(g)) {
      const m = g.match(/([一二三四五六])年级/);
      if (m) {
        const gNum = cnNum[m[1]] || 6;
        return { explicit: true, minGrade: gNum, maxGrade: gNum, label: `小学${gNum}年级` };
      }
      if (/六年级/.test(g)) return { explicit: true, minGrade: 6, maxGrade: 6, label: '小学6年级' };
      if (/五年级/.test(g)) return { explicit: true, minGrade: 5, maxGrade: 5, label: '小学5年级' };
      if (/四年级/.test(g)) return { explicit: true, minGrade: 4, maxGrade: 4, label: '小学4年级' };
      if (/三年级/.test(g)) return { explicit: true, minGrade: 3, maxGrade: 3, label: '小学3年级' };
      if (/二年级/.test(g)) return { explicit: true, minGrade: 2, maxGrade: 2, label: '小学2年级' };
      if (/一年级/.test(g)) return { explicit: true, minGrade: 1, maxGrade: 1, label: '小学1年级' };
      return { explicit: true, minGrade: 1, maxGrade: 6, label: '小学' };
    }
    if (/小学|一年级|二年级|三年级|四年级|五年级|六年级/.test(g)) {
      const m = g.match(/([一二三四五六])年级/);
      const gNum = m ? (cnNum[m[1]] || 6) : (/六年级/.test(g) ? 6 : /五年级/.test(g) ? 5 : /四年级/.test(g) ? 4 : 6);
      return { explicit: true, minGrade: gNum, maxGrade: gNum, label: `小学${gNum}年级` };
    }
    const m = g.match(/(\d{1,2})\s*年级/);
    if (m) {
      const n = parseInt(m[1], 10);
      if (n >= 1 && n <= 12) return { explicit: true, minGrade: n, maxGrade: n, label: `${n}年级` };
    }
    return { explicit: false, minGrade: 1, maxGrade: 12, label: null };
  }

  _effectiveMinGradeForGoal(goal, archetype = null, profile = null) {
    const band = this._parseExplicitGradeBand(goal);
    if (band.explicit) return band.minGrade;
    if (this._isSocialOrCivicInquiryGoal(goal)) return 1;
    return archetype?.minGrade || profile?.minGrade || 1;
  }

  /** 步骤展示用短标签，避免长目标全文重复嵌套 */
  _compactProjectLabel(goal, topic = null) {
    let label = String(topic?.coreTopic || this._parseGoalSubject(goal) || '').trim();
    // 防护：如果 label 仍含【标签】格式（上游未完全剥离），从中提取任务核心
    if (/【/.test(label)) {
      const taskM = label.match(/【任务】\s*(.+?)(?:\s*【|$)/);
      if (taskM) {
        label = taskM[1].trim().replace(/^(?:设计|制作|开发|建造|完成|策划|撰写|探究|调查|分析|探寻|探索|研究|调研|记录|重塑|改造|优化|重建|更新|升级|整治|组织|开展|修复|翻新)(?:一个|一款|一份|一组|一次)?\s*/, '');
      } else {
        label = this._parseGoalSubject(goal);
      }
    }
    label = label
      .replace(/^关于/, '')
      .replace(/现状.*$/, '')
      .replace(/并提出.*$/, '')
      .replace(/(调研|调查|研究|探究|倡议).*$/, '')
      .trim();
    if (/垃圾分类|垃圾治理/.test(String(goal || '')) && !/垃圾/.test(label)) label = '社区垃圾分类';
    if (label.length > 18) label = label.slice(0, 18);
    return label || this._parseGoalSubject(goal).slice(0, 18);
  }

  _unwrapDeliverableName(name) {
    return String(name || '').replace(/^「+/, '').replace(/」+$/, '').trim();
  }

  _stepFingerprint(step) {
    return String(step || '')
      .replace(/^(记录|完成|制作|撰写|测量|绘制|围绕|开展|走访|整理|设计)/, '')
      .replace(/[「」]/g, '')
      .replace(/\s+/g, '')
      .slice(0, 96);
  }

  _stepsNearDuplicate(a, b) {
    if (!a || !b) return false;
    const fa = this._stepFingerprint(a);
    const fb = this._stepFingerprint(b);
    if (!fa || !fb) return false;
    if (fa === fb) return true;
    const shorter = fa.length < fb.length ? fa : fb;
    const longer = fa.length < fb.length ? fb : fa;
    return shorter.length >= 24 && longer.includes(shorter.slice(0, Math.min(40, shorter.length)));
  }

  _inferTopicKind(goal, subject) {
    const g = String(goal || '');
    if (/低空经济|低空飞行|低空空域|空域管理|通航产业|城市空中交通|eVTOL|低空物流|通用航空/.test(g)) return 'industry-innovation';
    if (/太空馆|天文馆|航天馆|科技馆|博物馆|展厅|展陈|太空.*馆|天文.*馆/.test(g) || (/馆|展厅|展览/.test(g + subject) && /重塑|改造|整治|升级|策展|布展|失控|翻新|重建|优化/.test(g))) return 'exhibition-redesign';
    if (/探寻|探索|研究|调研/.test(g) && /创新|产业|经济|行业/.test(g)) return 'industry-innovation';
    if (/种植|栽培|养花|月季|花卉|玫瑰|蔬菜|种菜|盆栽|园艺|养殖|养蚕|花坛|绿化|阳台种/.test(g)) return 'planting-cultivation';
    if (/微塑料|过滤装置|净水|污水处理|废水处理|水质净化|过滤系统|滤芯|膜过滤|拦截.*塑料|洗衣.*废水|过滤.*水/.test(g)) return 'environmental-filtration';
    if (/智能温室|温室温控|气象.*看板|温湿度风速/.test(g)) return 'embedded-iot';
    if (/自动浇花|浇花系统|浇水系统|智能灌溉|土壤湿度|微型水泵|自动灌溉/.test(g)) return 'embedded-iot';
    if (/河流水质|pH.*溶解氧|水质调查/.test(g)) return 'environmental-survey';
    if (/光伏|太阳能发电|碳减排/.test(g)) return 'energy-analysis';
    if (/纸桥|承重.*桥/.test(g)) return 'structure-engineering';
    if (/斗拱|古建.*模型/.test(g)) return 'heritage-maker';
    if (/碳足迹|减排行动/.test(g)) return 'social-civic-survey';
    return 'subject-anchored';
  }

  _blueprintSubstanceScore(blueprint, goal) {
    const blob = [
      blueprint?.projectSummary,
      blueprint?.deliverable,
      ...(blueprint?.schemes || []).flatMap(s => [
        s.name, s.summary,
        ...(s.phases || []).flatMap(p => [p.phase, ...(p.steps || []), p.deliverable, ...(p.knowledgeHints || [])]),
      ]),
    ].join(' ');
    const profile = this._goalProfile(goal, blueprint);
    const anchor = profile.topic?.coreTopic || this._parseGoalSubject(goal);
    const tokens = this._goalTokens(anchor);
    let score = 0;
    const hits = tokens.filter(t => t.length >= 2 && blob.includes(t)).length;
    if (hits >= 2) score += 2;
    else if (hits >= 1) score += 1;
    if (blob.includes(anchor) && anchor.length >= 4) score += 1;
    if (/\d+/.test(blob)) score += 1;
    if (/表|图|轴|清单|附录|柱状|折线|地图|记录|统计|问卷|访谈|对照|维度|指标|样本|时间轴|案例/.test(blob)) score += 2;
    if (/≥|≤|不少于|至少|精确到/.test(blob)) score += 1;
    if (profile.mismatchRes.some(re => re.test(blob))) score -= 3;
    const steps = (blueprint?.schemes || []).flatMap(s => (s.phases || []).flatMap(p => p.steps || []));
    if (steps.length) {
      const vacuous = steps.filter(s => this._isVacuousResearchStep(s)).length;
      if (vacuous / steps.length >= 0.4) score -= 2;
    }
    return score;
  }

  _isVacuousResearchStep(step) {
    const s = String(step || '').trim();
    if (!s) return true;
    if (/^(查阅|收集|整理|对比分析|撰写|研究|探究|了解|梳理|开展).{0,24}(资料|信息|内容|报告|研究|对比|调查)/.test(s)
      && !/\d|表|图|维度|指标|年|条|个|篇|项|节点|样本|问卷|访谈|对照|案例|城市|发展/.test(s)) {
      return true;
    }
    if (/^(完成|进行|落实).{0,12}(本阶段|阶段任务|研究任务|对比任务|调查任务)/.test(s)) return true;
    return false;
  }

  _isFiltrationGoal(goal) {
    return this._inferTopicKind(String(goal || ''), this._parseGoalSubject(goal)) === 'environmental-filtration';
  }

  _campusEnergyEfficiencyDomains(goal) {
    const subject = this._parseGoalSubject(goal) || '校园节能建议';
    return [
      { id: 'audit', label: '能耗调查', keywords: [subject, '用电', '用水', '能耗', '调查', '记录', '数据', '统计', '空调', '照明'], subjects: ['science', 'math'] },
      { id: 'behavior', label: '使用行为', keywords: [subject, '行为', '时段', '空置', '浪费', '观察', '访谈'], subjects: ['chinese', 'science'] },
      { id: 'analysis', label: '问题分析', keywords: [subject, '分析', '图表', '对比', '高耗能', '原因', '函数', '统计'], subjects: ['math', 'science'] },
      { id: 'proposal', label: '节能建议', keywords: [subject, '建议', '改造', '方案', 'LED', '温控', '习惯', '倡议'], subjects: ['science', 'chinese'] },
      { id: 'report', label: '提案论证', keywords: [subject, '报告', '论证', '可行性', '说明', '展示'], subjects: ['chinese', 'math'] },
    ];
  }

  _photovoltaicAnalysisDomains(goal) {
    const subject = this._compactProjectLabel(goal) || '校园光伏发电';
    return [
      { id: 'resource', label: '太阳能资源', keywords: [subject, '光伏', '太阳能', '日照', '辐射', '光电', '电功率', '能量守恒', '电能', '电流', '电压'], subjects: ['physics', 'science'] },
      { id: 'electricity', label: '用电与屋顶', keywords: [subject, '用电', '电量', '电费', '调查', '数据', '统计', '校园', '屋顶'], subjects: ['math', 'science', 'geography'] },
      { id: 'calc', label: '收益测算', keywords: [subject, '函数', '计算', '收益', '成本', '百分比', '统计', '估算', '发电'], subjects: ['math'] },
      { id: 'carbon', label: '减排效益', keywords: [subject, '碳', '排放', '减排', '环境', '对比', '可持续'], subjects: ['geography', 'science'] },
      { id: 'report', label: '方案论证', keywords: [subject, '说明', '报告', '论证', '建议', '图表'], subjects: ['chinese', 'math'] },
    ];
  }

  _embeddedIoTDomains(goal) {
    const subject = this._compactProjectLabel(goal) || '智能装置';
    return [
      { id: 'needs', label: '需求与指标', keywords: [subject, '需求', '指标', '湿度', '阈值', '植物', '浇水', '安全', '局限'], subjects: ['science', 'info-tech', 'chinese'] },
      { id: 'sense', label: '传感与采集', keywords: [subject, '传感', '湿度', '土壤', '信号', '采样', '标定', '数据', '模拟量'], subjects: ['physics', 'info-tech', 'science'] },
      { id: 'control', label: '控制逻辑', keywords: [subject, '控制', '程序', '分支', '循环', '阈值', '逻辑', '算法', '反馈', '判断'], subjects: ['info-tech', 'math'] },
      { id: 'actuation', label: '执行与驱动', keywords: [subject, '水泵', '电路', '驱动', '继电器', '电机', '供电', '接线', '开关'], subjects: ['physics', 'info-tech', 'science'] },
      { id: 'test', label: '测试与迭代', keywords: [subject, '测试', '对照', '记录', '数据', '误差', '优化', '验收', '干湿度'], subjects: ['science', 'math', 'info-tech'] },
    ];
  }

  _filtrationDomains() {
    return [
      { id: 'scope', label: '指标与局限', keywords: ['指标', '局限', '安全', '宣称', '对照', '变量', '实验'], subjects: ['science', 'chinese'] },
      { id: 'prefilter', label: '粗滤保护层', keywords: ['粗滤', '滤网', '沉淀', '泥沙', '颗粒', '保护', '滤纸'], subjects: ['science', 'physics'] },
      { id: 'adsorption', label: '吸附改味层', keywords: ['吸附', '活性炭', '异味', '颜色', '有机物'], subjects: ['chemistry', 'science'] },
      { id: 'membrane', label: '膜孔径核心层', keywords: ['膜', '孔径', '滤芯', '微滤', '超滤', '陶瓷', '拦截', '微塑料'], subjects: ['chemistry', 'physics', 'science'] },
      { id: 'test', label: '对照测试与评价', keywords: ['测试', '对照', '流速', '数据', '实验', '记录', '减少率', '统计'], subjects: ['science', 'math', 'physics'] },
    ];
  }

  _plantingCropLabel(goal) {
    const g = String(goal || '');
    const m = g.match(/月季|玫瑰|番茄|黄瓜|辣椒|白菜|菠菜|多肉|薰衣草|向日葵|郁金香|菊花|荷花|草莓|葡萄|玉米|小麦|蚕|百合|牡丹/);
    return m ? m[0] : '植物';
  }

  _plantingCultivationDomains(goal) {
    const crop = this._plantingCropLabel(goal);
    const subject = this._parseGoalSubject(goal);
    return [
      { id: 'taxonomy', label: '植物识别与分类', keywords: [crop, subject, '植物', '分类', '特征', '结构', '器官', '绿色'], subjects: ['science', 'biology'] },
      { id: 'growth', label: '生长与环境条件', keywords: [crop, '生长', '光合', '呼吸', '种子', '萌发', '根', '蒸腾', '环境', '水分'], subjects: ['science', 'biology'] },
      { id: 'cultivate', label: '栽培实操', keywords: [crop, '种植', '栽培', '土壤', '浇水', '施肥', '扦插', '移栽', '步骤', '养护'], subjects: ['science', 'biology'] },
      { id: 'observe', label: '生长观察记录', keywords: [crop, '观察', '记录', '测量', '数据', '图表', '变化', '高度', '叶片'], subjects: ['science', 'math', 'biology'] },
      { id: 'share', label: '种植日记与分享', keywords: [crop, '日记', '报告', '总结', '分享', '说明', '写作'], subjects: ['chinese'] },
    ];
  }

  _isPlantingCultivationGoal(goal) {
    return this._inferTopicKind(String(goal || ''), this._parseGoalSubject(goal)) === 'planting-cultivation';
  }

  _buildTopicKeywords(goal, subject, kind) {
    const g = String(goal || '');
    const base = [subject];
    if (/太空|天文|航天|行星|月球|宇宙/.test(g + subject)) base.push('太阳系', '天文', '太空', '月球', '科学');
    if (/馆|展厅|展览|展陈/.test(g + subject)) base.push('展览', '展陈', '科普', '布局', '设计');
    if (/低空|空域|通航|无人机/.test(g + subject)) base.push('低空经济', '空域', '无人机', '飞行');
    if (kind === 'exhibition-redesign') base.push('调查', '方案', '说明', '统计', '设计', '展示');
    if (kind === 'industry-innovation') base.push('产业', '创新', '调研', '政策', '可行性');
    if (kind === 'planting-cultivation' || /种植|栽培|月季|花卉|蔬菜|盆栽|园艺|养殖|养蚕/.test(g + subject)) {
      base.push('植物', '分类', '生长', '光合', '种子', '萌发', '栽培', '根系', '蒸腾', '观察', '记录');
    }
    if (kind === 'environmental-filtration' || /微塑料|过滤|净水|废水|滤芯/.test(g + subject)) {
      base.push('过滤', '沉淀', '吸附', '微塑料', '拦截', '对照', '流速', '孔径', '环境', '污染');
    }
    if (kind === 'energy-analysis') {
      base.push('光伏', '太阳能', '光电', '电功率', '能量转化', '一次函数', '统计', '百分比', '碳排放', '日照', '发电', '收益', '减排');
    }
    if (kind === 'energy-efficiency') {
      base.push('节能', '能耗', '用电', '用水', '空调', '照明', '调查', '统计', '数据', '建议', '改造', '环境', '能源');
    }
    for (let i = 0; i < subject.length - 1; i++) {
      const w = subject.slice(i, i + 2);
      if (w.length === 2 && !/[的与及了在]$/.test(w)) base.push(w);
    }
    const anchors = this._getTopicAnchors(g);
    (anchors.recallTerms || []).slice(0, 12).forEach(t => base.push(t));
    return [...new Set(base)].slice(0, 20);
  }

  _inferDeliverableHint(goal, subject, kind) {
    if (kind === 'embedded-iot') {
      return `可运行的「${subject}」装置原型 + 控制逻辑说明 + 测试记录表`;
    }
    if (kind === 'energy-analysis') {
      return `光伏发电测算表 + 收益与减排分析图表 + 方案论证报告`;
    }
    if (kind === 'energy-efficiency') {
      return `校园节能改造提案（能耗调查表+问题分析图表+节能建议清单+可行性说明）`;
    }
    if (kind === 'exhibition-redesign') return `「${subject}」改造方案册（现状诊断表+展陈设计图+整改实施清单+开放验收表）`;
    if (kind === 'industry-innovation') return `「${subject}」创新方案报告（场景调研+政策要点+可行性论证）`;
    if (kind === 'planting-cultivation') return `「${subject}」种植观察日记（植物分类笔记+栽培记录表+生长数据图表+总结）`;
    if (kind === 'environmental-filtration') return `三级过滤装置原型 + A/B/C 对照实验记录表 + 含局限说明的测试报告`;
    if (/垃圾分类|垃圾治理|环保|社区.*环境/.test(goal)) {
      return `社区垃圾分类调查报告（现状记录表+统计图表+改进建议与宣传策划）`;
    }
    if (/报告|调查|论文|倡议|方案|建议|改进/.test(goal)) {
      return `「${this._compactProjectLabel(goal, { coreTopic: subject })}」专题报告（含调研数据、改进建议与宣传策划）`;
    }
    if (/设计|制作|开发|建造/.test(goal)) return `可展示的「${subject}」作品+过程记录+说明文档`;
    return `「${subject}」项目成果包（含策划说明+过程记录+可检查交付物）`;
  }

  /** 从用户目标提取核心主题（与服务端 extractTopicProfile 对齐，任何题目都必须锚定） */
  _extractTopicProfile(goal) {
    const g = String(goal || '').trim();
    if (this._topicProfileCache?.has(g)) return this._topicProfileCache.get(g);
    const presets = [
      {
        test: /校园节能|节能建议|建筑能耗|能耗调查|教学楼.*节能|空调.*节能|照明.*节能/,
        coreTopic: '校园节能建议',
        definition: '调查校园用电用水与空调照明运行数据，分析高能耗时段与空间，提出可落地的节能改造建议',
        keywords: ['节能', '能耗', '用电', '用水', '空调', '照明', '校园', '调查', '数据', '统计', '建议', '改造', '环境', '能源'],
        banInSteps: ['有机合成', '细胞', '原型驱动迭代', 'MVP', '光伏接线', '发电收益'],
        deliverableHint: '校园节能改造提案（能耗调查表+问题分析图表+节能建议清单+可行性说明）',
        kind: 'energy-efficiency',
      },
      {
        test: /垃圾分类|垃圾治理|垃圾处理|废弃物|固体废物|社区.*垃圾|环保.*调查|回收.*调查/,
        coreTopic: '社区垃圾分类',
        definition: '调查社区垃圾分类现状，分析投放与分类问题，提出可落地的改进建议与宣传策划',
        keywords: ['垃圾', '分类', '可回收', '有害', '厨余', '社区', '调查', '问卷', '统计', '环境', '建议', '宣传', '倡议'],
        banInSteps: ['原型驱动迭代', 'MVP', '飞行', '航空', '抗生素', '细胞', '内燃机', '电解池'],
        deliverableHint: '社区垃圾分类调查报告（现状记录表+统计图表+改进建议与宣传策划）',
        kind: 'social-civic-survey',
      },
      {
        test: /智能温室|温室温控|温湿度传感.*(?:通风|补光)|温控系统.*(?:温室|作物)/,
        coreTopic: '智能温室温控系统',
        definition: '用温湿度传感器监测温室环境，自动控制通风与补光，保持适宜作物生长',
        keywords: ['温室', '温湿度', '传感', '控制', '通风', '补光', '程序', '阈值', '节能', '作物', '数据'],
        banInSteps: ['有机合成', '离子检验', '调研报告', '问卷', '原型驱动迭代', 'MVP'],
        deliverableHint: '智能温室温控原型 + 阈值参数表 + 环境测试记录',
        kind: 'embedded-iot',
      },
      {
        test: /自动浇花|浇花系统|浇水系统|智能灌溉|土壤湿度.*(?:传感|检测|判断)|微型水泵|自动灌溉/,
        coreTopic: '自动浇花系统',
        definition: '设计基于土壤湿度传感的自动浇花装置：采集湿度→判断阈值→驱动微型水泵灌溉，并完成接线、控制逻辑与测试验收',
        keywords: ['自动浇花', '土壤湿度', '传感器', '水泵', '灌溉', '控制', '程序', '电路', '阈值', '测试', '数据', '植物', '水分', '物联网', '采集'],
        banInSteps: ['有机合成', '离子检验', '烃', '钠化合物', '调研报告', '问卷调查', '原型驱动迭代', 'MVP', '快速原型'],
        deliverableHint: '自动浇花装置原型 + 湿度阈值控制说明 + 浇水测试记录表',
        kind: 'embedded-iot',
      },
      {
        test: /河流水质|水质调查|pH.*溶解氧|溶解氧.*浊度|水体污染.*治理/,
        coreTopic: '河流水质调查',
        definition: '采集河流 pH、溶解氧、浊度等指标，评估污染程度并提出治理建议',
        keywords: ['河流', '水质', 'pH', '溶解氧', '浊度', '污染', '环境', '采样', '实验', '统计', '治理'],
        banInSteps: ['有机合成', '火箭', '程序设计', '原型驱动迭代', 'MVP'],
        deliverableHint: '水质采样记录表 + 指标分析图表 + 治理建议报告',
        kind: 'environmental-survey',
      },
      {
        test: /光伏|太阳能发电|屋顶.*光伏|发电潜力|发电收益|碳减排效益/,
        coreTopic: '校园光伏发电测算',
        definition: '调查日照与用电数据，估算屋顶光伏发电收益与碳减排效益',
        keywords: ['光伏', '太阳能', '发电', '收益', '碳', '减排', '统计', '函数', '环境', '能源'],
        banInSteps: ['有机合成', '细胞', '诗词', '原型驱动迭代'],
        deliverableHint: '光伏发电测算表 + 收益与减排分析 + 方案论证报告',
        kind: 'energy-analysis',
      },
      {
        test: /纸桥|承重.*桥|桥梁模型.*承载|结构.*承载力/,
        coreTopic: '承重纸桥模型',
        definition: '设计制作纸桥模型，探究结构与材料对承载力的影响并完成加载测试',
        keywords: ['纸桥', '承重', '结构', '受力', '压强', '材料', '平衡', '实验', '测量', '数据'],
        banInSteps: ['有机合成', '离子检验', '细胞', '原型驱动迭代', 'MVP'],
        deliverableHint: '纸桥模型 + 加载测试记录表 + 结构分析说明',
        kind: 'structure-engineering',
      },
      {
        test: /斗拱|古建.*模型|古建.*测绘|木构.*模型|遗产.*研学/,
        coreTopic: '古建斗拱模型',
        definition: '调研古建斗拱结构，测绘关键尺寸比例并制作微缩木构模型，撰写研学报告',
        keywords: ['古建', '斗拱', '历史', '比例', '测绘', '结构', '受力', '模型', '研学', '报告'],
        banInSteps: ['有机合成', '程序设计', '原型驱动迭代', 'MVP'],
        deliverableHint: '斗拱微缩模型 + 测绘记录表 + 研学报告',
        kind: 'heritage-maker',
      },
      {
        test: /气象.*看板|气象数据.*可视化|温湿度风速.*(?:采集|展示)/,
        coreTopic: '校园气象看板',
        definition: '采集校园温度、湿度、风速数据并可视化展示一周变化趋势',
        keywords: ['气象', '温度', '湿度', '风速', '数据', '图表', '采集', '传感', '程序', '统计'],
        banInSteps: ['有机合成', '离子检验', '原型驱动迭代', 'MVP'],
        deliverableHint: '气象数据看板 + 一周趋势图表 + 采集说明文档',
        kind: 'embedded-iot',
      },
      {
        test: /碳足迹|减排行动|用电用水出行.*统计/,
        coreTopic: '班级碳足迹测算',
        definition: '分类统计班级一周用电、用水、出行数据，测算碳足迹并提出减排行动方案',
        keywords: ['碳', '排放', '能源', '统计', '调查', '环境', '数据', '倡议', '减排', '用电'],
        banInSteps: ['有机合成', '牛顿定律', '电解池', '原型驱动迭代'],
        deliverableHint: '碳账本统计表 + 减排倡议方案 + 行动清单',
        kind: 'social-civic-survey',
      },
      {
        test: /微塑料|过滤装置|净水|污水处理|废水处理|水质净化|过滤系统|滤芯|膜过滤|拦截.*塑料|洗衣.*废水/,
        coreTopic: '微塑料过滤装置',
        definition: '设计可测试的三级水体过滤装置：粗滤保护层、活性炭吸附改味层、明确孔径的膜/陶瓷核心层，并通过 A/B/C 对照实验验证模型颗粒变化',
        keywords: ['微塑料', '过滤', '净水', '废水', '滤芯', '沉淀', '吸附', '活性炭', '拦截', '颗粒', '对照', '流速', '孔径', '膜'],
        banInSteps: ['火箭', '反冲', '抛体', '弹道', '发射', '原型驱动迭代', 'MVP', '快速原型', '塑料微珠', '剪塑料', '亮片'],
        deliverableHint: '三级过滤装置原型 + A/B/C 对照实验记录表 + 含局限说明的测试报告',
        kind: 'environmental-filtration',
      },
      {
        test: /低空经济|低空飞行|低空空域|空域管理|通航产业|城市空中交通|UAM|eVTOL|低空物流|通用航空/,
        coreTopic: '低空经济',
        definition: '指在约1000–3000米低空空域内，以无人机物流配送、低空出行、应急救援、农业植保、巡检等飞行活动带动的新兴产业',
        keywords: ['低空经济', '低空', '空域', '通航', '无人机', '低空物流', '飞行', '航空', '交通', '应急救援', '植保', '政策', '法规', '安全', '产业'],
        banInSteps: ['现代物流管理', '智慧城市', '工程设计思维', '环境搭建', '硬件组件', '一般物流', '原型驱动迭代', 'MVP'],
        deliverableHint: '低空经济创新方案报告（场景调研+政策/空域要点+技术可行性+试点建议）',
        kind: 'industry-innovation',
      },
    ];
    for (const p of presets) {
      if (p.test.test(g)) {
        const hit = { ...p, rawGoal: g, matched: true };
        this._topicProfileCache.set(g, hit);
        return hit;
      }
    }
    const subject = this._parseGoalSubject(g) || g.slice(0, 24);
    const kind = this._inferTopicKind(g, subject);
    const banCommon = ['原型驱动迭代', 'MVP', '快速原型', '递进式实施', '浸润式场景', '硬件准备', '环境搭建', '工程设计思维', '招生简章', '现代物流管理', '智慧城市'];
    if (kind === 'industry-innovation') {
      const core = /低空经济/.test(g) ? '低空经济' : (g.match(/(?:.+?经济|.+?产业|.+?行业)/)?.[0]?.slice(0, 24) || subject);
      return {
        rawGoal: g, matched: true, coreTopic: core, kind,
        definition: `围绕「${core}」开展创新探究，须结合真实产业场景、政策或技术应用`,
        keywords: this._buildTopicKeywords(g, core, kind),
        banInSteps: [...banCommon, '硬件组件', '一般物流'],
        deliverableHint: this._inferDeliverableHint(g, core, kind),
      };
    }
    if (kind === 'exhibition-redesign') {
      return {
        rawGoal: g, matched: true, coreTopic: subject, kind,
        definition: `对「${subject}」进行现状诊断、主题策划、展陈设计与整改实施，交付可验收的改造方案`,
        keywords: this._buildTopicKeywords(g, subject, kind),
        banInSteps: [...banCommon, '程序设计', '电解池', '搭建原型'],
        deliverableHint: this._inferDeliverableHint(g, subject, kind),
      };
    }
    if (kind === 'planting-cultivation') {
      const crop = this._plantingCropLabel(g);
      const profile = {
        rawGoal: g, matched: true, coreTopic: subject, kind, crop,
        definition: `围绕「${subject}」学习植物分类与生长原理，完成${crop}栽培并持续观察记录`,
        keywords: this._buildTopicKeywords(g, subject, kind),
        banInSteps: [...banCommon, '程序设计', '牛顿', '化学方程式', '电解池'],
        deliverableHint: this._inferDeliverableHint(g, subject, kind),
      };
      this._topicProfileCache.set(g, profile);
      return profile;
    }
    const profile = {
      rawGoal: g, matched: true, coreTopic: subject, kind: 'subject-anchored',
      definition: `本项目必须围绕「${subject}」展开，不得替换为其他主题`,
      keywords: this._buildTopicKeywords(g, subject, kind),
      banInSteps: banCommon,
      deliverableHint: this._inferDeliverableHint(g, subject, kind),
    };
    this._topicProfileCache.set(g, profile);
    return profile;
  }

  _isIndustryInnovationGoal(goal) {
    return this._extractTopicProfile(goal).kind === 'industry-innovation';
  }

  _isExhibitionRedesignGoal(goal) {
    return this._extractTopicProfile(goal).kind === 'exhibition-redesign';
  }

  _industryInnovationDomains(goal) {
    const t = this._extractTopicProfile(goal);
    const topic = t.coreTopic || '产业创新';
    return [
      { id: 'background', label: `${topic}背景与政策`, keywords: [topic, '产业', '政策', '法规', '空域', '发展', '规划', '经济'], subjects: ['geography', 'history', 'chinese'] },
      { id: 'scenarios', label: '应用场景调研', keywords: [topic, '物流', '出行', '应急', '植保', '巡检', '配送', '应用', '场景', '需求'], subjects: ['geography', 'chinese', 'math'] },
      { id: 'tech', label: '技术原理支撑', keywords: ['飞行', '航空', '无人机', '导航', '通信', '动力', '电池', '抛体', '牛顿', '安全'], subjects: ['physics', 'info-tech', 'science'] },
      { id: 'analysis', label: '数据与可行性分析', keywords: ['统计', '数据', '调查', '成本', '效益', '比较', '分析', '图表', '百分比'], subjects: ['math', 'chinese'] },
      { id: 'proposal', label: '创新方案与报告', keywords: ['方案', '创新', '建议', '报告', '论证', '说明', '可行性', '试点'], subjects: ['chinese', 'geography'] },
    ];
  }

  /** 项目类型分类（与服务端 classifyProjectType 对齐） */
  _classifyProjectType(goal) {
    const g = String(goal || '');
    if (this._isConsumerDecisionGoal(g)) return 'consumer-decision';
    if (/海报|短视频|微电影|动画|漫画|插画|绘画|展览|策展|广告|品牌|视觉|游戏设计|作曲|音乐创作|手工艺|表演|舞台|摄影|logo|标志设计|文创|周边设计/.test(g)) return 'creative-media';
    if (/诗歌|诗集|现代诗|诗词|写诗|小说|剧本|散文|绘本|故事集|演讲|辩论|文学|翻译|双语|新闻稿|采访稿|写一[篇组]|作文|征文|朗诵|文集|杂志|读后感|书评|话剧|文章|苏东坡|苏轼|诗人|文学家|历史人物|人物研究|名人传记|古代诗人/.test(g)) return 'humanities-literary';
    if (/创业|商业计划|营销|市场推广|运营|理财|零花钱|压岁钱|市场调研|义卖|跳蚤市场|店铺|定价|商业模式|经济效益|盈利|众筹|招商|品牌策划|购物|小卖部|找零|小票|记账|人民币学具|模拟.*购物|收入.*图表/.test(g)) return 'business-economics';
    if (/健康|营养|饮食|食谱|减脂|减肥|健身|锻炼|运动会?|近视|视力|护眼|睡眠|作息|心理|情绪|压力|安全|急救|防溺水|防火|防疫|卫生|疾病|人体|体重|身高/.test(g)) return 'health-life';
    if (this._isPlantingCultivationGoal(g)) return 'planting-cultivation';
    if (/烹饪|烘焙|美食|菜谱|料理|手工|编织|缝纫|收纳|整理|维修|清洁|打扫|劳动/.test(g)) return 'labor-practice';
    if (/研学|游学|研学旅行|研学路线|红色研学|文化研学|文化考察|实地考察|field.?trip|遗址|博物馆|人文史迹|古迹|古村|世界遗产/.test(g)) return 'study-trip';
    if (/活动策划|策划.{0,6}(活动|晚会|联欢|运动会|典礼|节|比赛)|联欢会|晚会|文艺汇演|毕业典礼|生日会|出游|旅行|路线规划|时间管理|班级布置|布置教室|嘉年华|游园/.test(g)) return 'life-planning';
    if (/田野|问卷|访谈|社区|民俗|传统文化|非遗|人口|城乡|社会现象|调研报告|公众.{0,4}认知|居民|乡土|口述史|城市|发展史|对比|比较|典型|区域|案例/.test(g)) return 'social-inquiry';
    if (this._isExhibitionRedesignGoal(g)) return 'exhibition-redesign';
    if (this._isIndustryInnovationGoal(g)) return 'industry-innovation';
    if (/工坊|鲁班|榫卯|古典.*风格|木结构|建筑模型|微缩|传统建筑|斗拱|飞檐/.test(g)) return 'maker-workshop';
    if (this._isEnergyAnalysisGoal(g)) return 'energy-analysis';
    if (/算力中心|数据中心|太空算力|云计算|边缘计算|计算中心|服务器集群|卫星计算|轨道计算/.test(g)) return 'engineering';
    if (/火箭|导弹|发射|机器人|物流机器人|医院.*机器人|电路|机械|硬件|装置|App|应用程序|小程序|网站|系统开发|3D打印|传感|智能|温控|储能|光伏|发电|搭建|制作|工程|发明|物联网|编程实现/.test(g)) return 'engineering';
    if (/无人机|原型/.test(g) && /设计|制作|研发|装置|系统|搭建|开发/.test(g)) return 'engineering';
    if (this._isChemistryInquiryGoal(g)) return 'scientific-inquiry';
    if (/探究|实验|观察|测量|验证|影响因素|变量|检测|成分|对照实验|科学问题|浓度|溶液|溶解/.test(g)) return 'scientific-inquiry';
    return 'general';
  }

  /** 非特定 STEM 类型的通用模块（与服务端 genericDomainsForType 对齐） */
  _genericDomainsForType(id) {
    const map = {
      'scientific-inquiry': [
        { id: 'question', label: '问题与假设', keywords: ['问题', '假设', '猜想', '现象', '原理'], subjects: ['science', 'physics', 'chemistry', 'biology'] },
        { id: 'design', label: '变量与实验设计', keywords: ['变量', '实验', '控制变量', '对照', '方案', '测量'], subjects: ['physics', 'chemistry', 'biology', 'science'] },
        { id: 'data', label: '数据采集与处理', keywords: ['数据', '测量', '记录', '统计', '误差', '图表'], subjects: ['math', 'info-tech', 'science'] },
        { id: 'conclusion', label: '分析与结论', keywords: ['分析', '结论', '解释', '规律', '报告'], subjects: ['science', 'math', 'chinese'] },
      ],
      'social-inquiry': [
        { id: 'topic', label: '选题与调查设计', keywords: ['选题', '调查', '问卷', '访谈', '抽样', '样本', '维度', '指标'], subjects: ['chinese', 'math'] },
        { id: 'collect', label: '资料与数据收集', keywords: ['资料', '数据', '收集', '记录', '文献', '实地', '史料', '案例'], subjects: ['geography', 'history', 'chinese'] },
        { id: 'analyze', label: '整理与统计分析', keywords: ['统计', '整理', '图表', '分析', '百分比', '平均数', '对比'], subjects: ['math'] },
        { id: 'report', label: '结论与报告', keywords: ['结论', '报告', '建议', '论证', '写作', '说明'], subjects: ['chinese'] },
      ],
      'humanities-literary': [
        { id: 'theme', label: '立意与选材', keywords: ['立意', '主题', '选材', '构思', '观点'], subjects: ['chinese', 'english'] },
        { id: 'read', label: '阅读与素材积累', keywords: ['阅读', '素材', '文本', '名著', '积累', '鉴赏'], subjects: ['chinese', 'english', 'history'] },
        { id: 'express', label: '结构与表达', keywords: ['结构', '表达', '修辞', '语言', '写作', '叙述', '议论'], subjects: ['chinese', 'english'] },
        { id: 'revise', label: '修改与展示', keywords: ['修改', '评议', '朗诵', '展示', '演讲', '发表'], subjects: ['chinese'] },
      ],
      'creative-media': [
        { id: 'idea', label: '创意构思', keywords: ['创意', '构思', '主题', '灵感', '受众'], subjects: ['chinese', 'info-tech'] },
        { id: 'design', label: '设计与草案', keywords: ['设计', '草图', '分镜', '排版', '色彩', '构图'], subjects: ['info-tech', 'chinese'] },
        { id: 'make', label: '制作与实现', keywords: ['制作', '剪辑', '绘制', '编辑', '工具', '技术'], subjects: ['info-tech'] },
        { id: 'show', label: '展示与评议', keywords: ['展示', '评议', '反馈', '发布', '优化'], subjects: ['chinese'] },
      ],
      'business-economics': [
        { id: 'research', label: '需求与市场调研', keywords: ['需求', '市场', '调研', '调查', '数据', '用户'], subjects: ['math', 'chinese'] },
        { id: 'plan', label: '方案与产品设计', keywords: ['方案', '产品', '设计', '策划', '创意'], subjects: ['chinese', 'info-tech'] },
        { id: 'cost', label: '成本与定价测算', keywords: ['成本', '定价', '利润', '预算', '函数', '百分比', '统计'], subjects: ['math'] },
        { id: 'operate', label: '运营与复盘', keywords: ['运营', '推广', '复盘', '反馈', '报告'], subjects: ['chinese', 'math'] },
      ],
      'study-trip': [
        { id: 'destination', label: '目的地调研', keywords: ['目的地', '调研', '区域', '地图', '地形', '气候', '资源', '区位', '交通', '地理'], subjects: ['geography', 'history'] },
        { id: 'heritage', label: '人文史迹', keywords: ['历史', '文物', '遗址', '博物馆', '革命', '朝代', '遗产', '人文', '古迹', '文化', '史迹'], subjects: ['history', 'chinese'] },
        { id: 'route', label: '路线预算', keywords: ['路线', '日程', '行程', '预算', '费用', '统计', '成本', '分工', '安全', '预案'], subjects: ['math', 'geography', 'chinese'] },
        { id: 'report', label: '研学报告', keywords: ['报告', '总结', '记录', '说明', '展示', '复盘', '观察', '日记', '写作'], subjects: ['chinese', 'history', 'geography'] },
      ],
      'life-planning': [
        { id: 'goal', label: '需求与目标', keywords: ['需求', '目标', '调查', '问卷', '场景', '人数'], subjects: ['chinese', 'math'] },
        { id: 'plan', label: '方案与日程', keywords: ['方案', '计划', '日程', '安排', '路线', '流程', '行程'], subjects: ['chinese', 'geography', 'math'] },
        { id: 'budget', label: '预算与分工', keywords: ['预算', '成本', '费用', '统计', '函数', '分工', '百分比', '比例'], subjects: ['math'] },
        { id: 'review', label: '执行与复盘', keywords: ['执行', '记录', '反馈', '复盘', '总结', '报告', '通知'], subjects: ['chinese'] },
      ],
      'health-life': [
        { id: 'status', label: '现状了解', keywords: ['现状', '调查', '统计', '数据', '测量', '记录'], subjects: ['math', 'biology', 'science'] },
        { id: 'knowledge', label: '健康知识', keywords: ['健康', '营养', '饮食', '运动', '睡眠', '安全', '疾病', '人体', '视力'], subjects: ['biology', 'science'] },
        { id: 'plan', label: '计划制定', keywords: ['计划', '方案', '目标', '食谱', '作息', '锻炼'], subjects: ['chinese', 'math'] },
        { id: 'assess', label: '实践与评估', keywords: ['记录', '评估', '对比', '反馈', '改进', '报告', '宣传', '倡议'], subjects: ['chinese', 'math'] },
      ],
      'planting-cultivation': [
        { id: 'taxonomy', label: '植物识别与分类', keywords: ['植物', '分类', '特征', '结构', '器官', '绿色'], subjects: ['science', 'biology'] },
        { id: 'growth', label: '生长与环境', keywords: ['生长', '光合', '呼吸', '种子', '萌发', '根', '蒸腾'], subjects: ['science', 'biology'] },
        { id: 'cultivate', label: '栽培实操', keywords: ['种植', '栽培', '土壤', '浇水', '施肥', '移栽', '养护'], subjects: ['science', 'biology'] },
        { id: 'observe', label: '观察记录', keywords: ['观察', '记录', '测量', '数据', '图表', '变化'], subjects: ['science', 'math', 'biology'] },
        { id: 'share', label: '种植日记', keywords: ['日记', '报告', '总结', '分享', '说明'], subjects: ['chinese'] },
      ],
      'labor-practice': [
        { id: 'prepare', label: '认识与准备', keywords: ['认识', '准备', '材料', '工具', '原理', '步骤'], subjects: ['science', 'biology', 'chinese'] },
        { id: 'practice', label: '操作实践', keywords: ['操作', '制作', '种植', '养护', '烹饪', '步骤', '工艺'], subjects: ['science', 'biology'] },
        { id: 'record', label: '观察与记录', keywords: ['观察', '记录', '测量', '数据', '变化', '统计'], subjects: ['science', 'math', 'biology'] },
        { id: 'share', label: '成果与分享', keywords: ['成果', '分享', '展示', '总结', '报告', '改进'], subjects: ['chinese'] },
      ],
      'exhibition-redesign': [
        { id: 'diagnose', label: '现状诊断', keywords: ['问题', '调查', '记录', '失控', '隐患', '现状'], subjects: ['chinese', 'math'] },
        { id: 'theme', label: '主题策划', keywords: ['主题', '天文', '太阳系', '月球', '太空', '科普', '内容'], subjects: ['science', 'chinese'] },
        { id: 'design', label: '展陈设计', keywords: ['布局', '动线', '展板', '设计', '模型', '互动', '展陈'], subjects: ['info-tech', 'chinese', 'math'] },
        { id: 'implement', label: '实施整改', keywords: ['整改', '布置', '预算', '分工', '安全', '清单', '实施'], subjects: ['math', 'chinese'] },
        { id: 'launch', label: '开放验收', keywords: ['验收', '讲解', '宣传', '说明', '展示', '反馈', '开放'], subjects: ['chinese', 'science'] },
      ],
      'industry-innovation': [
        { id: 'background', label: '产业背景与政策', keywords: ['产业', '政策', '法规', '空域', '经济', '交通', '区域', '发展'], subjects: ['geography', 'history', 'chinese'] },
        { id: 'scenarios', label: '应用场景调研', keywords: ['调查', '统计', '数据', '问卷', '场景', '应用', '需求', '物流', '应急'], subjects: ['math', 'chinese', 'geography'] },
        { id: 'tech', label: '技术原理支撑', keywords: ['飞行', '航空', '无人机', '抛体', '牛顿', '运动', '安全'], subjects: ['physics', 'science'] },
        { id: 'analysis', label: '数据可行性分析', keywords: ['统计', '图表', '比较', '分析', '成本', '效益', '数据'], subjects: ['math'] },
        { id: 'proposal', label: '创新方案报告', keywords: ['方案', '创新', '报告', '论证', '说明', '建议'], subjects: ['chinese', 'geography'] },
      ],
      'engineering': [
        { id: 'principle', label: '原理与需求', keywords: ['原理', '需求', '指标', '现象', '规律', '受力', '能量'], subjects: ['physics', 'science', 'chemistry'] },
        { id: 'structure', label: '结构与装置', keywords: ['结构', '装置', '材料', '设计', '搭建', '组装', '电路', '机械'], subjects: ['physics', 'engineering', 'science'] },
        { id: 'control', label: '控制与实现', keywords: ['控制', '传感', '编程', '算法', '电路', '反馈', '调试'], subjects: ['info-tech', 'physics', 'engineering'] },
        { id: 'test', label: '测试与迭代', keywords: ['测试', '实验', '测量', '数据', '误差', '记录', '优化'], subjects: ['math', 'physics', 'science'] },
      ],
      'energy-analysis': [
        { id: 'resource', label: '太阳能资源', keywords: ['光伏', '太阳能', '日照', '辐射', '光电', '电功率', '能量'], subjects: ['physics', 'science'] },
        { id: 'electricity', label: '用电与屋顶', keywords: ['用电', '电量', '电费', '调查', '数据', '统计', '屋顶', '面积'], subjects: ['math', 'science'] },
        { id: 'calc', label: '收益测算', keywords: ['函数', '计算', '收益', '成本', '百分比', '统计', '估算', '发电'], subjects: ['math'] },
        { id: 'carbon', label: '减排效益', keywords: ['碳', '排放', '减排', '环境', '能源', '对比'], subjects: ['geography', 'science'] },
        { id: 'report', label: '方案论证', keywords: ['说明', '报告', '论证', '建议', '图表'], subjects: ['chinese', 'math'] },
      ],
      'general': [
        { id: 'define', label: '调研与定义', keywords: ['调研', '需求', '定义', '背景', '分析', '资料'], subjects: ['chinese', 'history', 'geography', 'math'] },
        { id: 'design', label: '方案设计', keywords: ['方案', '设计', '规划', '分工', '构思'], subjects: ['chinese', 'math', 'geography'] },
        { id: 'make', label: '实施与表达', keywords: ['实施', '制作', '执行', '记录', '表达'], subjects: ['chinese', 'math'] },
        { id: 'test', label: '总结与展示', keywords: ['总结', '评估', '展示', '报告', '反思'], subjects: ['chinese', 'math'] },
      ],
    };
    return map[id] || [];
  }

  /** 工程子系统拆解（与服务端 pbl-prompts inferProjectDomains 对齐） */
  _inferProjectDomains(goal) {
    const g = String(goal || '');
    if (this._isChemistryInquiryGoal(g)) {
      return this._getChemistryAnalysisProfile(g).mixed
        ? this._mixedSolutionChemistryDomains()
        : this._directSolutionChemistryDomains();
    }
    if (this._isPlantingCultivationGoal(g)) {
      return this._plantingCultivationDomains(g);
    }
    if (this._isFiltrationGoal(g)) {
      return this._filtrationDomains();
    }
    if (this._isExhibitionRedesignGoal(g)) {
      const subject = this._parseGoalSubject(g);
      return [
        { id: 'diagnose', label: '现状诊断', keywords: [subject, '问题', '调查', '记录', '失控', '隐患', '现状'], subjects: ['chinese', 'math'] },
        { id: 'theme', label: '主题策划', keywords: [subject, '主题', '天文', '太阳系', '月球', '太空', '科普', '内容'], subjects: ['science', 'chinese'] },
        { id: 'design', label: '展陈设计', keywords: [subject, '布局', '动线', '展板', '设计', '模型', '互动', '展陈'], subjects: ['info-tech', 'chinese', 'math'] },
        { id: 'implement', label: '实施整改', keywords: [subject, '整改', '布置', '预算', '分工', '安全', '清单', '实施'], subjects: ['math', 'chinese'] },
        { id: 'launch', label: '开放验收', keywords: [subject, '验收', '讲解', '宣传', '说明', '展示', '反馈', '开放'], subjects: ['chinese', 'science'] },
      ];
    }
    if (this._isIndustryInnovationGoal(g)) {
      return this._industryInnovationDomains(g);
    }
    if (this._isConsumerDecisionGoal(g)) {
      return [
        {
          id: 'needs', label: '需求与场景调研',
          keywords: ['调查', '数据', '统计', '问卷', '需求', '分析', '收集', '整理', '图表'],
          subjects: ['math', 'chinese']
        },
        {
          id: 'cost', label: '成本与数据建模',
          keywords: ['函数', '一次函数', '计算', '统计', '数据', '平均数', '费用', '成本', '百分比', '方程'],
          subjects: ['math']
        },
        {
          id: 'energy_compare', label: '动力与能耗差异（科普）',
          keywords: ['内燃机', '热机', '效率', '电能', '化学能', '能量', '热值', '做功', '机械能', '内能'],
          subjects: ['physics', 'chemistry']
        },
        {
          id: 'environment', label: '环保与可持续',
          keywords: ['环境', '污染', '排放', '碳', '气候', '资源', '可持续', '温室'],
          subjects: ['geography', 'chemistry']
        },
        {
          id: 'decision', label: '决策论证与报告',
          keywords: ['说明', '报告', '论证', '写作', '分析', '比较', '调查', '实用'],
          subjects: ['chinese', 'math']
        }
      ];
    }
    if (/工坊|鲁班|榫卯|古典.*风格|木结构|建筑模型|微缩|传统建筑|斗拱|飞檐/.test(g)) {
      return [
        { id: 'survey', label: '调研与风格定义', keywords: ['调研', '风格', '古典', '建筑', '参考', '测量', '场地'], subjects: ['history', 'chinese', 'art'] },
        { id: 'design', label: '方案与图纸', keywords: ['设计', '草图', '立面', '平面', '尺寸', '比例', 'BOM'], subjects: ['math', 'info-tech', 'art'] },
        { id: 'material', label: '材料与工艺', keywords: ['材料', '木材', '榫卯', '胶合', '工具', '安全', '工艺'], subjects: ['science', 'physics'] },
        { id: 'build', label: '搭建与装饰', keywords: ['搭建', '组装', '切割', '打磨', '装饰', '斗拱', '结构'], subjects: ['science', 'physics'] },
        { id: 'accept', label: '验收与展示', keywords: ['验收', '测试', '展示', '报告', '量规', '改进'], subjects: ['chinese', 'math'] },
      ];
    }
    if (/算力中心|数据中心|太空算力|云计算|边缘计算|计算中心|服务器集群|卫星计算|轨道计算/.test(g)) {
      return [
        { id: 'requirements', label: '需求与约束定义', keywords: ['算力', '任务负载', '轨道环境', '功耗', '散热', '通信链路', '辐射', '需求'], subjects: ['computer-science', 'engineering', 'physics'] },
        { id: 'architecture', label: '系统架构设计', keywords: ['系统架构', '计算节点', '电源', '热控', '通信', '冗余', '模块化', '接口'], subjects: ['computer-science', 'engineering'] },
        { id: 'operations', label: '调度与运行控制', keywords: ['任务调度', '遥测', '容错', '故障切换', '资源分配', '监控', '控制流程'], subjects: ['computer-science', 'engineering'] },
        { id: 'verification', label: '仿真测试与迭代', keywords: ['仿真', '指标', '延迟', '带宽', '能耗', '热平衡', '可靠性', '测试'], subjects: ['computer-science', 'engineering', 'physics'] },
      ];
    }
    if (/火箭|导弹|发射|弹道|模型火箭|航天/.test(g)) {
      return [
        {
          id: 'propulsion', label: '推进与燃料',
          keywords: ['燃烧', '氧化', '燃料', '热值', '内能', '化学能', '能量', '推进', '反应', '热机'],
          subjects: ['chemistry', 'physics']
        },
        {
          id: 'aerodynamics', label: '空气动力与弹道',
          keywords: ['抛体', '流体', '压强', '流速', '气动', '弹道', '抛物', '飞行', '大气'],
          subjects: ['physics', 'math']
        },
        {
          id: 'dynamics', label: '运动学与动力学',
          keywords: ['牛顿', '动量', '冲量', '受力', '加速度', '机械能', '守恒', '运动', '力学'],
          subjects: ['physics', 'math']
        },
        {
          id: 'structure', label: '结构与材料',
          keywords: ['结构', '材料', '强度', '压强', '设计', '稳定'],
          subjects: ['physics', 'chemistry']
        },
        {
          id: 'control', label: '控制、传感与测试',
          keywords: ['控制', '传感', '电路', '编程', '算法', '数据', '实验', '误差', '测试', '采集'],
          subjects: ['info-tech', 'physics']
        }
      ];
    }
    if (/纸桥|承重.*桥|桥梁模型/.test(g)) {
      return [
        { id: 'design', label: '方案与结构', keywords: ['结构', '受力', '压强', '材料', '设计', '平衡', '力'], subjects: ['physics', 'math'] },
        { id: 'build', label: '制作组装', keywords: ['制作', '组装', '材料', '加工', '搭建', '桥'], subjects: ['science', 'physics'] },
        { id: 'test', label: '加载测试', keywords: ['测试', '测量', '数据', '实验', '误差', '记录', '统计'], subjects: ['physics', 'math', 'science'] },
        { id: 'report', label: '分析说明', keywords: ['报告', '分析', '说明', '结论', '改进'], subjects: ['chinese', 'physics'] },
      ];
    }
    if (/河流水质|pH.*溶解氧|水质调查/.test(g)) {
      return [
        { id: 'sample', label: '采样与指标', keywords: ['采样', 'pH', '溶解氧', '浊度', '水质', '测量', '实验'], subjects: ['science', 'chemistry'] },
        { id: 'environment', label: '河流环境', keywords: ['河流', '污染', '环境', '水源', '生态', '地理'], subjects: ['geography', 'science'] },
        { id: 'data', label: '数据处理', keywords: ['统计', '图表', '数据', '分析', '记录'], subjects: ['math', 'science'] },
        { id: 'report', label: '治理建议', keywords: ['报告', '建议', '治理', '环境', '倡议'], subjects: ['chinese', 'geography'] },
      ];
    }
    if (this._isCampusEnergyEfficiencyGoal(g)) {
      return this._campusEnergyEfficiencyDomains(g);
    }
    if (this._isEnergyAnalysisGoal(g)) {
      return this._photovoltaicAnalysisDomains(g);
    }
    if (/斗拱|古建.*模型|古建.*测绘/.test(g)) {
      return [
        { id: 'heritage', label: '古建调研', keywords: ['古建', '斗拱', '历史', '文物', '建筑', '遗产'], subjects: ['history', 'chinese'] },
        { id: 'measure', label: '测绘比例', keywords: ['比例', '测量', '尺寸', '相似', '图形'], subjects: ['math', 'physics'] },
        { id: 'structure', label: '结构受力', keywords: ['结构', '受力', '稳定', '材料', '力', '平衡'], subjects: ['physics', 'science'] },
        { id: 'report', label: '研学报告', keywords: ['报告', '说明', '记录', '展示'], subjects: ['chinese', 'history'] },
      ];
    }
    if (this._isEmbeddedOrIoTGoal(g) && /浇花|浇水|灌溉|土壤湿度|水泵|湿度传感|温室|气象/.test(g)) {
      return this._embeddedIoTDomains(g);
    }
    if (this._isEmbeddedOrIoTGoal(g)) {
      return [
        { id: 'needs', label: '需求与指标', keywords: ['需求', '指标', '场景', '约束', '安全', '功能'], subjects: ['science', 'info-tech', 'chinese'] },
        { id: 'sense', label: '传感与采集', keywords: ['传感', '采集', '信号', '数据', '接口', '标定'], subjects: ['physics', 'info-tech', 'science'] },
        { id: 'control', label: '控制与实现', keywords: ['控制', '程序', '算法', '逻辑', '分支', '循环', '反馈', '调试'], subjects: ['info-tech', 'math', 'engineering'] },
        { id: 'actuation', label: '执行与驱动', keywords: ['电路', '驱动', '电机', '继电器', '供电', '接线', '执行'], subjects: ['physics', 'info-tech', 'science'] },
        { id: 'test', label: '测试与迭代', keywords: ['测试', '记录', '数据', '误差', '优化', '验收', '对照'], subjects: ['science', 'math', 'info-tech'] },
      ];
    }
    if (this._isGroundRoboticsGoal(g)) {
      return [
        { id: 'mechanics', label: '结构与运动', keywords: ['结构', '受力', '摩擦', '轮', '电机', '传动', '力', '平衡', '运动', '速度', '杠杆'], subjects: ['physics', 'science', 'engineering'] },
        { id: 'circuit', label: '电路与驱动', keywords: ['电路', '电流', '电压', '电机', '驱动', '电源', '接线', '开关', '串联', '并联'], subjects: ['physics', 'info-tech'] },
        { id: 'sense', label: '传感与感知', keywords: ['传感', '红外', '超声', '距离', '循迹', '检测', '巡线', '信号', '采集'], subjects: ['physics', 'info-tech', 'engineering'] },
        { id: 'control', label: '控制与算法', keywords: ['控制', '反馈', 'PID', '算法', '编程', '逻辑', '避障', '决策', '调试'], subjects: ['info-tech', 'math', 'computer-science', 'engineering'] },
        { id: 'test', label: '调试与测试', keywords: ['测试', '调试', '误差', '数据', '记录', '实验', '迭代', '验收'], subjects: ['math', 'science', 'engineering'] },
      ];
    }
    if (/温控|温室|温度|加热|散热|PID|闭环/.test(g)) {
      return [
        { id: 'modeling', label: '数学建模', keywords: ['函数', '方程', '建模', '图像'], subjects: ['math'] },
        { id: 'physics', label: '热学原理', keywords: ['热传导', '温度', '内能', '热量'], subjects: ['physics'] },
        { id: 'hardware', label: '传感与电路', keywords: ['传感器', '电路', '采集'], subjects: ['physics', 'info-tech'] },
        { id: 'control', label: '控制算法', keywords: ['控制', '反馈', '编程', '算法'], subjects: ['info-tech', 'math'] }
      ];
    }
    if (this._isEnergyEngineeringGoal(g)) {
      return [
        {
          id: 'energy', label: '能量转换与守恒',
          keywords: ['能量转化', '能量转换', '机械能', '内能', '电能', '化学能', '热值', '效率', '功率', '做功'],
          subjects: ['physics', 'chemistry']
        },
        {
          id: 'electrochem', label: '电化学与电池',
          keywords: ['电池', '原电池', '电解', '电解池', '氧化还原', '电极', '电化学', '充放电', '蓄电', '储能', '燃料电池'],
          subjects: ['chemistry', 'physics']
        },
        {
          id: 'circuit', label: '电路与电磁',
          keywords: ['电路', '电流', '电压', '电阻', '电磁', '感应', '并联', '串联', '磁场', '电磁感应', '发电机'],
          subjects: ['physics']
        },
        {
          id: 'renewable', label: '新能源装置',
          keywords: ['光伏', '太阳能', '风能', '风电', '发电', '新能源', '涡轮', '光能', '光电', '太阳能电池'],
          subjects: ['physics', 'chemistry']
        },
        {
          id: 'system', label: '系统测试与控制',
          keywords: ['控制', '传感', '传感器', '采集', '实验', '测试', '反馈', '调试', '数据采集', '误差'],
          subjects: ['info-tech', 'physics']
        }
      ];
    }
    if (/垃圾分类|垃圾治理|垃圾处理|废弃物|固体废物|社区.*环境|环保.*调查|回收.*调查/.test(g)) {
      return [
        { id: 'survey', label: '现状调查', keywords: ['调查', '问卷', '访谈', '抽样', '社区', '现状', '记录', '实地'], subjects: ['chinese', 'math'] },
        { id: 'sorting', label: '分类标准与流程', keywords: ['分类', '可回收', '有害', '厨余', '其他', '标识', '投放', '垃圾'], subjects: ['geography', 'science'] },
        { id: 'data', label: '数据统计', keywords: ['统计', '图表', '百分比', '整理', '分析', '数据', '平均数'], subjects: ['math'] },
        { id: 'environment', label: '环境与影响', keywords: ['环境', '污染', '资源', '循环', '可持续', '减排', '生态'], subjects: ['geography', 'science'] },
        { id: 'proposal', label: '改进建议与宣传', keywords: ['建议', '方案', '宣传', '倡议', '报告', '写作', '说明'], subjects: ['chinese'] },
      ];
    }
    return this._genericDomainsForType(this._classifyProjectType(g));
  }

  _isEnergyProjectGoal(goal) {
    return this._isEnergyEngineeringGoal(goal);
  }

  /** 地面机器人/自动驾驶小车（非无人机/航空） */
  _isGroundRoboticsGoal(goal) {
    const g = String(goal || '');
    if (/无人机|飞行器|航空|火箭|导弹|低空|eVTOL|飞控|航天/.test(g)) return false;
    return /自动驾驶|智能车|循迹车|循迹小车|无人车|小车制作|制作.*小车|小车|物流机器人|机械臂|机器人车|巡线车|避障车/.test(g)
      || (/机器人|循迹/.test(g) && /制作|搭建|设计|开发|装置|小车|车/.test(g));
  }

  _isAviationRoboticsGoal(goal) {
    const g = String(goal || '');
    return /无人机|飞行器|航空|飞控|低空|eVTOL/.test(g) && /设计|制作|研发|搭建|开发|装置/.test(g);
  }

  _isAviationAerospaceNode(node) {
    if (!node) return false;
    const name = String(node.name || '');
    const text = this._nodeSearchText(node);
    const blob = `${name} ${text}`;
    if (/飞行控制|飞控系统|航空电子|航空航天|无人机|飞行器|弹道|导弹|火箭|低空|UAV|eVTOL|Autopilot|空域|机翼|气动|起降(?!点)/.test(blob)) return true;
    if (/飞行|航空|航天/.test(name) && !/自动驾驶|无人车|智能交通|循迹|小车|地面/.test(blob)) return true;
    const sub = String(node.subject || '');
    if (sub === 'aerospace-engineering') return true;
    if (sub === 'engineering' && /aerial|uav|aero-|flight|aviation/i.test(String(node.id || ''))) return true;
    return false;
  }

  _isBiologyHealthNode(node) {
    if (!node) return false;
    const name = String(node.name || '');
    const text = this._nodeSearchText(node);
    const blob = `${name} ${text}`;
    if (this._isBiologyNodeName(name)) return true;
    if (/抗生素|耐药|免疫|疫苗|病毒|细菌|药物|用药|分裂|分化|人体|器官系统|营养与健康|疾病|病理/.test(blob)) return true;
    if (['biology', 'advanced-biology'].includes(node.subject)) return true;
    return false;
  }

  /** 社会调查/社区议题（垃圾分类、环保治理等）且题目未涉及生命科学 */
  _isSocialOrCivicInquiryGoal(goal) {
    const g = String(goal || '');
    if (/田野|问卷|访谈|社区|民俗|传统文化|非遗|人口|城乡|社会现象|调研报告|居民|乡土|口述史|垃圾分类|垃圾治理|垃圾处理|废弃物|固体废物|环保|治理|倡议/.test(g)) {
      return !/生物|细胞|生态|光合|酶|遗传|植物|动物|种植|栽培|养殖|人体|器官/.test(g);
    }
    return false;
  }

  /** 健康生活类项目（近视防控、营养、运动、睡眠等） */
  _isHealthLifeGoal(goal) {
    const g = String(goal || '');
    return /健康|营养|饮食|食谱|减脂|减肥|健身|锻炼|近视|视力|护眼|睡眠|作息|心理|情绪|安全|急救|防溺水|防火|卫生|疾病|人体|体重|身高|防控|用眼/.test(g);
  }

  _isBiologyNodeName(name) {
    return /细胞|细胞膜|细胞器|细胞核|细胞壁|细胞呼吸|细胞代谢|细胞周期|细胞死亡|细胞分化|细胞衰老|细胞信号|细胞结构|线粒体|叶绿体|有丝分裂|减数分裂|DNA|基因表达|遗传|光合作用|酶|蛋白质合成|生物膜|生命与环境|微生物|植物.*分类|生物分类|抗生素|耐药|免疫|疫苗|病毒|细菌|药物|分裂与分化/.test(String(name || ''));
  }

  /** 非生物项目：硬性剔除生物噪声 */
  _shouldPurgeBiologyForGoal(goal) {
    if (this._isEnergyAnalysisGoal(goal)) return true;
    if (this._isConsumerDecisionGoal(goal)) return true;
    if (this._isSocialOrCivicInquiryGoal(goal)) return true;
    if (this._isGroundRoboticsGoal(goal)) return true;
    const g = String(goal || '');
    const type = this._classifyProjectType(g);
    if (['humanities-literary', 'business-economics', 'study-trip', 'life-planning', 'creative-media'].includes(type)) return true;
    if (type === 'general' && !/生物|细胞|人体|健康|植物|种植|动物|光合|消化|器官/.test(g)) return true;
    if (/(车|汽车)/.test(g) && /新能源|燃油|电动|混动|油电/.test(g) && !/生物|细胞|生态|光合|酶|遗传|植物|动物/.test(g)) return true;
    if (this._isEngineeringGoal(goal) && !/健康|营养|生物|人体|疾病|医学/.test(g)) return true;
    return false;
  }

  /** 商业/人文/调查等非理科项目：剔除磁铁、桥梁、动物外形等泛科学噪声 */
  _isOffTopicScienceNoiseNode(node) {
    if (!node) return false;
    const name = String(node.name || '');
    const blob = `${name} ${this._nodeSearchText(node)}`;
    if (/磁铁|磁现象|推和拉|桥梁|结构.*稳|月相|四季变化|岩石与土壤|动物的外形|人的感官|食物链|食物网|人体器官|有丝分裂/.test(blob)) return true;
    if (node.subject === 'science' && /动物|磁铁|推拉|桥梁|月相|岩石|材料|感官|四季/.test(name)) return true;
    return false;
  }

  _shouldPurgeOffTopicScienceForGoal(goal) {
    if (this._isPlantingCultivationGoal(goal)) return false;
    if (this._isStemProjectGoal(goal) || this._isEngineeringGoal(goal)) return false;
    const g = String(goal || '');
    if (/生物|人体|消化|器官|健康|植物|种植|动物|光合|生态/.test(g)) return false;
    const type = this._classifyProjectType(g);
    if (['business-economics', 'humanities-literary', 'social-inquiry', 'study-trip', 'life-planning', 'creative-media'].includes(type)) return true;
    if (this._isPrimaryCommerceGoal(g)) return true;
    if (type === 'general' && !/实验|工程|制作|搭建|装置|电路|化学|物理|测量|滴定/.test(g)) return true;
    return false;
  }

  _shouldPurgeAviationForGoal(goal) {
    return this._isGroundRoboticsGoal(goal) && !this._isAviationRoboticsGoal(goal);
  }

  _purgeBiologyNoise(nodes, goal) {
    if (!this._shouldPurgeBiologyForGoal(goal) || !Array.isArray(nodes)) return nodes;
    return nodes.filter(n => !this._isBiologyHealthNode(n));
  }

  _purgeOffTopicScienceNoise(nodes, goal) {
    if (!this._shouldPurgeOffTopicScienceForGoal(goal) || !Array.isArray(nodes)) return nodes;
    return nodes.filter(n => !this._isOffTopicScienceNoiseNode(n));
  }

  _shouldPurgeChemistryForGoal(goal) {
    if (this._isChemistryInquiryGoal(goal)) return false;
    if (this._isFiltrationGoal(goal)) return false;
    const g = String(goal || '');
    if (/化学|溶液|滴定|离子|有机|物质的量|电导率|氧化还原|原电池|电解/.test(g)) return false;
    if (this._isEmbeddedOrIoTGoal(g)) return true;
    if (this._isGroundRoboticsGoal(g)) return true;
    if (this._isEnergyAnalysisGoal(g)) return true;
    const type = this._classifyProjectType(g);
    if (type === 'engineering' && !/化学|电池|燃料|电解|氧化|蓄电|储能/.test(g)) return true;
    return false;
  }

  _isOffTopicChemistryNode(node) {
    if (!node || node.subject !== 'chemistry') return false;
    const blob = `${String(node.name || '')} ${this._nodeSearchText(node)}`;
    return /有机合成|有机化合物|烃|离子检验|钠及其化合物|醇|酚|醛|酮|羧酸|酯|胺|硝基|苯|同分异构|官能团|滴定|硝酸银|电导率|物质的量浓度|气体摩尔体积|原电池|电解池|热化学|焓变/.test(blob);
  }

  _isOffTopicGeographyClimateNode(node) {
    if (!node || node.subject !== 'geography') return false;
    const blob = `${String(node.name || '')} ${this._nodeSearchText(node)}`;
    return /大气环流|三圈环流|季风|宇宙环境|洋流|气压带|风带|地球运动|昼夜交替|全球性大气/.test(blob);
  }

  _shouldPurgeGeographyClimateForGoal(goal) {
    return this._isEnergyAnalysisGoal(goal);
  }

  _purgeGeographyClimateNoise(nodes, goal) {
    if (!this._shouldPurgeGeographyClimateForGoal(goal) || !Array.isArray(nodes)) return nodes;
    return nodes.filter(n => !this._isOffTopicGeographyClimateNode(n));
  }

  _purgeChemistryNoise(nodes, goal) {
    if (!this._shouldPurgeChemistryForGoal(goal) || !Array.isArray(nodes)) return nodes;
    return nodes.filter(n => !this._isOffTopicChemistryNode(n));
  }

  _purgeCurriculumNoise(nodes, goal) {
    let list = this._purgeBiologyNoise(nodes, goal);
    list = this._purgeOffTopicScienceNoise(list, goal);
    list = this._purgeChemistryNoise(list, goal);
    list = this._purgeGeographyClimateNoise(list, goal);
    return list;
  }

  _purgeAviationNoise(nodes, goal) {
    if (!this._shouldPurgeAviationForGoal(goal) || !Array.isArray(nodes)) return nodes;
    return nodes.filter(n => !this._isAviationAerospaceNode(n));
  }

  /** 返回无关节点剔除原因；null 表示可保留（硬门禁 + 泛化相关性分） */
  _getNodeIrrelevanceReason(node, goal, domains, archetype) {
    if (!node) return '空节点';
    if (node._manualSelected) return null;
    if (node.isExternal || node.layer === 'external' || String(node.id || '').startsWith('ext-')) return null;
    if (!this._passesHardNodeGate(node, goal, archetype)) {
      if (!this._shouldAllowUniversityNodes(goal) && this._isUniversityNode(node)) return '大学层默认排除';
      if (archetype && this._isArchetypeBanned(node, archetype)) return '原型禁用';
      return '泛素养或硬门禁';
    }
    const blueprint = this._activeBlueprint || null;
    if (this._shouldPurgeChemistryForGoal(goal) && this._isOffTopicChemistryNode(node)) {
      return '工程/IoT目标不宜引入无关化学节点';
    }
    if (this._shouldPurgeGeographyClimateForGoal(goal) && this._isOffTopicGeographyClimateNode(node)) {
      return '光伏测算不宜引入大气环流等气候系统节点';
    }
    if (this._isEnergyAnalysisGoal(goal) && (this._isBiologyHealthNode(node) || node.subject === 'biology')) {
      return '光伏/能源测算不宜引入细胞/生物膜等生物学节点';
    }
    const score = this._scoreUniversalRelevance(node, goal, blueprint, domains, archetype);
    if (score < this._relevanceKeepThreshold(false)) return `相关性不足(${score})`;
    return null;
  }

  /**
   * 统一无关节点核实：拆解入口 / 筛选后 / 输出前均调用
   * @returns {{ kept, removed, stats }}
   */
  _verifyAndPruneNodes(nodes, goal, archetype, phase = '核实') {
    const domains = this._inferProjectDomains(goal);
    const list = Array.isArray(nodes) ? nodes : [];
    const kept = [];
    const removed = [];
    list.forEach(n => {
      const reason = this._getNodeIrrelevanceReason(n, goal, domains, archetype);
      if (reason) removed.push({ id: n.id, name: n.name, reason });
      else kept.push(n);
    });
    if (removed.length) {
      const preview = removed.slice(0, 10).map(r => `${r.name}(${r.reason})`).join('、');
      console.warn(`[PBL] ${phase} 剔除 ${removed.length} 个无关节点: ${preview}${removed.length > 10 ? '…' : ''}`);
    }
    return {
      kept,
      removed,
      stats: { input: list.length, kept: kept.length, removed: removed.length },
    };
  }

  _verifyOutputBundle(bundle, goal, archetype) {
    const { complex, matched = [], external = [], graphData } = bundle;
    const m = this._verifyAndPruneNodes(matched, goal, archetype, '输出核实·matched');
    const e = this._verifyAndPruneNodes(external, goal, archetype, '输出核实·external');
    const g = this._verifyAndPruneNodes(graphData?.nodes || [], goal, archetype, '输出核实·图谱');
    const keptIds = new Set(g.kept.map(n => n.id));
    const links = (graphData?.links || []).filter(l => {
      const src = typeof l.source === 'object' ? l.source.id : l.source;
      const tgt = typeof l.target === 'object' ? l.target.id : l.target;
      return keptIds.has(src) && keptIds.has(tgt);
    });
    const removedAll = [...m.removed, ...e.removed, ...g.removed];
    return {
      complex,
      matched: m.kept,
      external: e.kept,
      graphData: { nodes: g.kept, links },
      relevanceAudit: {
        matched: m.stats,
        external: e.stats,
        graph: g.stats,
        removedTotal: removedAll.length,
        removedSamples: removedAll.slice(0, 20),
      },
    };
  }

  _applyOutputCurriculumFloor(outputAudit, goal, archetype, pool, meta = {}) {
    const min = this._getMinMatchedFloor(archetype);
    const profile = this._getPBLGoalProfile(goal);
    const matched = outputAudit.matched || [];
    const graphNodes = outputAudit.graphData?.nodes || [];
    const curriculumNodes = graphNodes.filter(n => n.layer !== 'external' && !n.isExternal);
    const coreLayer = curriculumNodes.filter(n => n.layer === 'matched').length;
    if (matched.length >= min && coreLayer >= min && curriculumNodes.length >= min) return outputAudit;

    let floor = this._guaranteeCurriculumFloor(
      matched,
      goal,
      this._getBroadCurriculumPool(goal, pool, min * 4),
      archetype,
      profile.maxMatched,
      outputAudit.complex,
      meta.projectBlueprint
    );
    if (floor.length < min) {
      floor = this._guaranteeCurriculumFloor(
        [],
        goal,
        this._getK12Pool(goal),
        archetype,
        profile.maxMatched,
        outputAudit.complex,
        meta.projectBlueprint
      );
    }
    if (floor.length < min) return outputAudit;

    const graphData = this._buildRichMainlineGraph(
      floor,
      meta.pathOrderIds || [],
      goal,
      meta.dependsOnLinks || [],
      outputAudit.external || []
    );
    const capped = this._capGraphNodes(graphData, PBLPathBuilder.PBL_MAX_GRAPH_NODES);
    const mainline = this._getMainlinePath(capped);
    console.warn(`[PBL] 课内知识点不足 ${min}，已保底补齐:`, floor.map(n => n.name).join('、'));
    return {
      ...outputAudit,
      matched: mainline.length ? mainline : floor,
      graphData: capped,
      relevanceAudit: {
        ...outputAudit.relevanceAudit,
        floorApplied: true,
        floorCount: floor.length,
      },
    };
  }

  _nodeSearchText(node) {
    return `${node.name || ''} ${node.definition || node.description || ''} ${(node.key_concepts || []).join(' ')}`.toLowerCase();
  }

  _stemGenericKeywords() {
    return new Set(['能量', '守恒', '定律', '运动', '计算', '函数', '方程']);
  }

  _isQuantitativeCalcNode(node) {
    const t = `${node.name || ''} ${node.definition || node.description || ''}`;
    return /计算|求解|方程式|列式|综合计算|根据化学方程式|定量|数值(计算|求解)|运算求|计算器|求.*大小|求.*值/.test(t);
  }

  _isConservationLawNode(node) {
    return /守恒定律|机械能守恒|能量守恒|动量守恒/.test(String(node.name || ''));
  }

  /** 节点知识形态：用于 STEM 广度均衡，避免全是定律/计算 */
  _stemKnowledgeKind(node) {
    const name = String(node.name || '');
    const text = this._nodeSearchText(node);
    if (this._isQuantitativeCalcNode(node)) return 'calculation';
    if (/守恒定律/.test(name)) return 'law';
    if (/实验|探究|测量|观测|验证|设计实验|控制变量/.test(text)) return 'experiment';
    if (/装置|结构|原理|工作|组成|机制|原电池|发电机|光伏|太阳能电池|电解|电解池|传感器|逆变|并网|电路元件|电磁感应|串联|并联/.test(text)) return 'apparatus';
    if (node.subject === 'math' || /函数|方程|建模|算法|三角函数/.test(name)) return 'modeling';
    return 'principle';
  }

  _stemKindPreference(node, goal) {
    const k = this._stemKnowledgeKind(node);
    if (k === 'calculation') return -4;
    if (k === 'law') return -2;
    if (k === 'apparatus') return 5;
    if (k === 'experiment') return 5;
    if (k === 'principle') return 4;
    if (k === 'modeling') return /建模|控制|算法|数据|App|程序/.test(String(goal || '')) ? 2 : -1;
    return 0;
  }

  _stemBreadthScoreAdjust(node, goal) {
    if (!this._isStemProjectGoal(goal)) return 0;
    let adj = this._stemKindPreference(node, goal) * 2;
    if (node.subject === 'chemistry') adj += 5;
    if (node.subject === 'info-tech') adj += 4;
    if (node.subject === 'physics') adj += 1;
    if (node.subject === 'math') adj -= 3;
    if (this._isQuantitativeCalcNode(node)) adj -= 10;
    if (this._isConservationLawNode(node)) adj -= 3;
    return adj;
  }

  _scoreNodeForDomains(node, domains) {
    if (!domains || !domains.length) return 0;
    let score = 0;
    const text = this._nodeSearchText(node);
    const generic = this._stemGenericKeywords();
    domains.forEach(d => {
      (d.keywords || []).forEach(kw => {
        const k = String(kw).toLowerCase();
        if (!text.includes(k)) return;
        score += generic.has(kw) ? 2 : 6;
      });
      if (d.subjects && d.subjects.includes(node.subject)) score += 2;
    });
    return score;
  }

  _isEngineeringGoal(goal) {
    return this._classifyProjectType(goal) === 'engineering' || this._isEnergyProjectGoal(goal);
  }

  /** STEM 严格门禁仅用于工程/科学探究类（避免把生活化/人文项目当 STEM 过滤） */
  _isStemProjectGoal(goal) {
    return ['engineering', 'scientific-inquiry'].includes(this._classifyProjectType(goal));
  }

  /** 跨学科泛素养节点（批判性思维、团队协作等），除非题目明确要求 */
  _isGenericTransversalNode(name, goal) {
    const n = String(name || '').trim();
    if (!n || !PBLPathBuilder.GENERIC_TRANSVERSAL_RE.test(n)) return false;
    const g = String(goal || '');
    if (/团队|协作|合作|分工|沟通|管理|领导|批判|创新思维|问题解决|生涯|素养培养/.test(g)) return false;
    return true;
  }

  _isHollowStep(step) {
    const s = String(step || '').trim();
    if (!s || s.length < 12) return true;
    if (this._isVacuousResearchStep(s)) return true;
    if (PBLPathBuilder.HOLLOW_STEP_RE.test(s)) return true;
    if (/^运用[①②③④⑤⑥⑦⑧⑨⑩\d]+「/.test(s) && /完成本阶段|探究任务/.test(s)) return true;
    if (/^(选择|确定|调研|了解|学习|掌握|认识|编写基础|配置|安装).{0,12}(组件|框架|逻辑|特点|风格|方案|软件|环境)$/.test(s)) return true;
    if (/进行.{0,6}(测试|调研|研究|探究|活动)$/.test(s)) return true;
    if (this._stepActionabilityScore(s) < 2) return true;
    return false;
  }

  _stepActionabilityScore(step) {
    const s = String(step || '');
    if (!s || s.length < 8) return 0;
    let score = 0;
    if (/\d+(\.\d+)?\s*(cm|mm|m|ml|g|kg|℃|°|分钟|小时|天|日|次|人|题|页|张|帧|行|列|条|份|组|点|字|mw|kwh|度)/i.test(s)) score += 3;
    if (/\d+[\-–~至]\d+/.test(s)) score += 2;
    if (/≥|≤|不少于|不超过|精确到|至少|至多/.test(s)) score += 2;
    if (/表格|清单|记录表|草图|立面|平面|BOM|问卷|提纲|甘特|量规|检查表|数据表|照片|截图|附录|折线图|示意图|柱状|扇形|模型|因子|假设|论证|测算表/.test(s)) score += 2;
    if (/填写|绘制|称量|测量|焊接|切割|打磨|组装|编程|调试|访谈|统计|撰写|标注|拍照|导出|打印|查阅|计算|测绘|调查|分析|整理|录入|估算|对比/.test(s)) score += 1;
    if (/面积×|效率×|日照|用电|减排|碳排放|收益|电价|辐射|光电|屋顶|碳足迹/.test(s)) score += 1;
    if (PBLPathBuilder.HOLLOW_STEP_RE.test(s)) score -= 4;
    if (/^(选择|确定|了解|学习|掌握|认识|编写基础)/.test(s)) score -= 2;
    return score;
  }

  _areHollowSteps(steps) {
    if (!Array.isArray(steps) || !steps.length) return true;
    const hollow = steps.filter(s => this._isHollowStep(s)).length;
    if (hollow >= Math.ceil(steps.length * 0.5)) return true;
    const avg = steps.reduce((a, s) => a + this._stepActionabilityScore(s), 0) / steps.length;
    return avg < 2.5;
  }

  _pickConcreteSteps(llmSteps, bpSteps, contextual) {
    const normalize = (steps) => {
      if (!Array.isArray(steps) || !steps.length) return null;
      const good = steps.filter(s => !this._isHollowStep(s));
      if (!good.length) return null;
      const score = good.reduce((a, s) => a + this._stepActionabilityScore(s), 0);
      return { steps: good.slice(0, 4), score };
    };
    const ranked = [
      { ...normalize(contextual), w: 4, src: contextual },
      { ...normalize(bpSteps), w: 3 },
      { ...normalize(llmSteps), w: 2 },
    ].filter(x => x.steps?.length);
    if (ranked.length) {
      ranked.sort((a, b) => (b.score + b.w * 2) - (a.score + a.w * 2));
      return ranked[0].steps;
    }
    if (contextual?.length) return contextual.slice(0, 4);
    if (bpSteps?.length) return bpSteps.slice(0, 4);
    return (llmSteps || []).slice(0, 4);
  }

  _isGenericBlueprintText(text) {
    const s = String(text || '').trim();
    if (!s || s.length < 16) return true;
    return /按模块推进|阶段产出可检查|可检查验收|主题实施方案|浸润式|递进式|可展示的项目原型|围绕「.+」按模块|紧扣题目关键词|每阶段产出可检查|技术路线概述|方案名称/.test(s);
  }

  _blueprintStepDepthScore(blueprint) {
    const scheme = (blueprint?.schemes || []).find(s => s.id === blueprint?.recommendedSchemeId)
      || blueprint?.schemes?.[0];
    const phases = scheme?.phases || [];
    if (!phases.length) return 0;
    let total = 0;
    let count = 0;
    phases.forEach(p => {
      (p.steps || []).forEach(st => {
        count++;
        total += this._stepActionabilityScore(st);
        if (this._isHollowStep(st)) total -= 3;
      });
    });
    return count ? total / count : 0;
  }

  _inferDefaultScopeLimits(goal) {
    const art = this._compactProjectLabel(goal);
    const type = this._classifyProjectType(goal);
    const common = [
      `不能把课堂/简化模型结论直接等同于真实场景下的专业认证结果`,
      `所有数据须注明来源、假设条件与测量/调查日期，禁止无依据外推`,
    ];
    const byType = {
      'energy-analysis': [`不能把估算发电量写成已并网运行的确定产能`, `减排效益须基于可查碳排放因子，不能宣称「完全零碳」`],
      engineering: [`不能把原型演示等同于产品级可靠性认证`, `涉及用电/加热/切割等操作须有成人指导与安全预案`],
      'scientific-inquiry': [`不能把单次课堂实验结论推广为普遍规律`, `样本量过小时须在报告中写明局限`],
      'social-inquiry': [`不能把班级小样本调查等同于全市/全国结论`, `访谈与问卷须保护受访者隐私`],
      'consumer-decision': [`车型/产品参数须来自公开资料并标注日期`, `成本测算须列出假设（里程、电价/油价等）`],
    };
    return [...(byType[type] || [`不能把「${art}」的初步成果夸大为已规模化落地`]), ...common].slice(0, 4);
  }

  _inferDefaultSuccessCriteria(goal) {
    const art = this._compactProjectLabel(goal);
    const deliverable = this._extractTopicProfile(goal).deliverableHint || art;
    return [
      `最终交付物「${deliverable}」齐全：数据表/图表/说明文字可现场核查`,
      `每阶段至少有 1 份签字或拍照留档的过程记录`,
      `报告或方案中至少 3 处引用本项目原始数据（附表号或图号）`,
      `答辩或展示时能回答「数据怎么来的、假设是什么、局限在哪」`,
    ].slice(0, 4);
  }

  _inferDefaultConstraints(goal) {
    const weeks = this._parseExplicitGradeBand(goal).maxGrade <= 6 ? '2-3' : '3-4';
    return [
      `建议周期 ${weeks} 周，每周有明确阶段产出`,
      `材料与工具限于校园/家庭可获取范围，超预算须说明替代方案`,
      `涉及户外调查、用电、加热、切割等须遵守校方安全规定`,
    ];
  }

  /** 按模块 id 生成可执行步骤模板（全项目类型通用） */
  _domainStepTemplates(dom, artifact, knRef = '本阶段课标知识点') {
    if (!dom) return [];
    const label = dom.label || dom.id;
    const byId = {
      question: [`围绕「${artifact}」写出 1 条可验证问题与 2 条假设，列出将观察的指标≥3项`, `用 ${knRef} 解释问题背后的科学/社会原理，整理 1 页概念笔记`],
      design: [`为「${artifact}」绘制${label}流程图，标注变量/对照/测量工具各≥1项`, `编制${label}实施检查表（步骤/负责人/截止日/产出文件）`],
      data: [`按${label}方案采集原始数据≥10条，录入表格并标注单位与日期`, `用 ${knRef} 绘制≥1种统计图，计算至少 2 项百分比或平均数`],
      analyze: [`整理${label}数据并写出 3 条基于图表的发现（每条对应 1 张图或 1 组数据）`, `讨论${label}中的误差或局限，列出 2 条改进方向`],
      conclusion: [`撰写${label}分析小结（≥300字），含结论、证据与 1 条生活联系`, `对照 successCriteria 完成${label}自评表并勾选验收项`],
      topic: [`确定「${artifact}」调查对象与样本量（如本班/年级抽样≥15人），写出调查问题 1 句`, `设计 8-10 题问卷或访谈提纲（含 2 道开放题），注明发放渠道`],
      collect: [`完成${label}实地走访或资料收集，填写原始记录表并附照片≥3张`, `整理回收数据，标注缺失值与 2 份异常答卷的处理方式`],
      report: [`撰写「${artifact}」${label}报告（≥600字）：摘要/方法/发现/建议四段结构`, `制作 1 页答辩要点清单（3 条结论+2 个图表编号+1 条局限说明）`],
      survey: [`走访≥2处与「${artifact}」相关点位，填写${label}记录表（观察项≥8条）`, `汇总${label}现场照片≥3张并标注时间与地点`],
      test: [`按检查表完成「${artifact}」${label}测试≥3次，记录成功率/误差并求平均`, `整理测试数据表，写出 1 条现象解释与 1 处改进计划`],
      build: [`按方案完成「${artifact}」${label}核心工序，填写过程记录表（时间/工具/问题各≥1条）`, `拍摄制作过程照片≥3张，标注关键尺寸或接线点`],
      principle: [`画出「${artifact}」${label}原理框图，标注输入/输出与关键公式或规律`, `用 ${knRef} 列出器材/工具清单（型号/数量）与 3 项测试指标`],
      structure: [`绘制「${artifact}」${label}结构草图，标注≥5处关键尺寸`, `编制物料清单（名称/规格/数量/单价），合计预算并附安全注意 2 条`],
      control: [`实现「${artifact}」${label}功能点 1 个，附测试用例 3 条（输入/预期/实测）`, `保存调试日志或运行截图，记录 1 次故障与修复过程`],
      resource: [`查阅与「${artifact}」相关的${label}资料≥3条，整理数据来源对照表`, `记录${label}原始数据≥7组，注明采集日期与换算方法`],
      electricity: [`统计「${artifact}」相关用电量或样本数据，制成折线图/柱状图`, `测绘或估算关键面积/尺寸，绘制示意图并标注假设条件`],
      calc: [`建立「${artifact}」${label}计算模型，列出假设并完成测算表`, `用 ${knRef} 完成收益/成本/效率中至少 1 项定量计算`],
      carbon: [`查阅碳排放或环境因子，计算「${artifact}」${label}对比量并制表`, `制作${label}效益对比图表，写出 2 条可核查结论`],
      define: [`收集「${artifact}」背景资料 3 条（各 50 字摘要+来源），制成优先级表`, `明确 1 个可检查交付物与 3 条验收标准（谁检查、看什么）`],
      make: [`执行「${artifact}」${label}核心任务，按阶段记录关键数据与过程证据`, `整理${label}中间产出文件（表/图/照片）并编号归档`],
      theme: [`确定「${artifact}」${label}主题与受众，写 100 字创意/策划简报`, `列出 2 个参考范例并各写 50 字借鉴点`],
      read: [`建立「${artifact}」${label}素材库：摘录≥20条语料并分类标注`, `用 ${knRef} 完成阅读/资料提纲（中心句+3分论点）`],
      express: [`完成「${artifact}」${label}初稿（不少于规定字数/件数），标注待改段落`, `按结构/语言两项自评表修改 1 轮，保留修改对照`],
      revise: [`定稿并排版「${artifact}」${label}成果，附 200 字创作/实施说明`, `准备展示稿与 2 个听众可能提问的回答要点`],
      research: [`描述「${artifact}」目标用户与 3 个痛点，完成 10 人迷你访谈并汇总`, `用 ${knRef} 列出核心功能与竞品差异表`],
      cost: [`制作「${artifact}」${label}成本表，用百分比或函数估算盈亏平衡点`, `列出 3 条成本敏感性假设（价格/销量/耗材变动）`],
      plan: [`制作「${artifact}」${label}日程甘特图或流程表，含物料清单`, `完成关键准备项检查表并勾选负责人与截止日`],
      assess: [`按方案执行并记录签到/照片，当天填写执行日志`, `撰写 500 字复盘：亮点、问题、费用决算与改进建议`],
      status: [`调查「${artifact}」${label}现状，回收有效问卷≥15份或访谈≥5人`, `用表格呈现${label}基线数据，计算至少 1 项统计量`],
      knowledge: [`查阅与「${artifact}」相关的${label}科学资料≥3条并摘录要点`, `制作${label}概念图，标注 5 个关键术语及关系`],
      cultivate: [`完成「${artifact}」${label}实操步骤，填写操作日志（日期/天气/问题各 1 条）`, `拍摄过程照片≥3张，标注工具与安全防护`],
      observe: [`每周 2 次测量「${artifact}」${label}指标，录入表格并绘制折线图（≥4点）`, `对比${label}变化趋势，写出 2 条数据发现`],
      heritage: [`查阅「${artifact}」${label}史料或实地资料≥3条，整理史迹观察表`, `绘制${label}平面示意图，标注尺寸比例与关键构件`],
      measure: [`测量「${artifact}」${label}关键尺寸≥5处，记录工具与误差`, `按相似比例换算${label}模型尺寸，附计算过程`],
      diagnose: [`走访「${artifact}」并填写${label}诊断表：问题点位照片≥5张`, `列出≥8条现状问题并标注整改优先级`],
      implement: [`编制「${artifact}」${label}实施清单（任务/负责人/工期/预算）`, `按清单执行并勾选完成项，附物资表合计`],
      launch: [`按验收表逐项核查「${artifact}」${label}成果并签字`, `录制 3 分钟讲解视频或撰写 300 字宣传稿`],
    };
    if (byId[dom.id]) return byId[dom.id];
    const hint = (dom.keywords || []).slice(0, 3).join('、') || label;
    return [
      `围绕「${artifact}」完成${label}：结合 ${knRef} 与关键词「${hint}」整理资料并产出可核查记录表`,
      `为${label}编制检查表（步骤/数据/产出文件），完成后附照片或签字确认`,
    ];
  }

  _enrichBlueprintMetadata(goal, blueprint) {
    if (!blueprint) return blueprint;
    const bp = blueprint;
    const topic = this._extractTopicProfile(goal);
    const art = this._compactProjectLabel(goal, topic);
    const domains = this._inferProjectDomains(goal);
    const chain = domains.map(d => d.label).join(' → ');

    if (this._isGenericBlueprintText(bp.projectSummary)) {
      bp.projectSummary = topic.definition
        || `围绕「${topic.coreTopic || art}」按「${chain}」推进，最终交付${topic.deliverableHint || '可检查成果包'}`;
    }
    if (!bp.deliverable || /素养|能力|精神|阶段成果/.test(bp.deliverable) || bp.deliverable.length < 8) {
      bp.deliverable = topic.deliverableHint || bp.deliverable;
    }
    if (!Array.isArray(bp.constraints) || bp.constraints.length < 2 || bp.constraints.every(c => this._isGenericBlueprintText(c))) {
      bp.constraints = this._inferDefaultConstraints(goal);
    }
    if (!Array.isArray(bp.scopeLimits) || bp.scopeLimits.length < 2) {
      bp.scopeLimits = this._inferDefaultScopeLimits(goal);
    }
    if (!Array.isArray(bp.successCriteria) || bp.successCriteria.length < 2) {
      bp.successCriteria = this._inferDefaultSuccessCriteria(goal);
    }
    if (!bp.knowledgeChain && chain) bp.knowledgeChain = chain;
    if (!Array.isArray(bp.subsystems) || !bp.subsystems.length) {
      bp.subsystems = domains.map(d => ({
        id: d.id,
        name: d.label,
        description: `围绕「${art}」完成${d.label}相关调查/实验/测算与记录`,
      }));
    }

    (bp.schemes || []).forEach((s, si) => {
      if (this._isGenericBlueprintText(s.summary)) {
        s.summary = si === 0
          ? `推荐路线：按「${chain}」分阶段推进，每阶段有可检查产出`
          : `备选路线 ${s.id}：在材料/周期/深度上与推荐方案形成差异`;
      }
      if (!Array.isArray(s.pros) || s.pros.length < 2) {
        s.pros = ['阶段任务可检查、可评分', '模块与题目关键词对齐', '适合课堂/社团分阶段实施'];
      }
      if (!Array.isArray(s.cons) || !s.cons.length) {
        s.cons = ['需按本校条件微调数据与器材', '部分阶段需校外资料或成人指导'];
      }
      (s.phases || []).forEach((p, pi) => {
        const dom = domains[pi];
        if (dom && (/基础|实施|阶段|准备|探究/.test(String(p.phase || '')) || String(p.phase || '').length < 3)) {
          p.phase = dom.label;
        }
      });
    });
    return this._enrichBlueprintPedagogy(goal, bp);
  }

  /** 通用 PBL 教学设计加厚：驱动性问题、场景 venue、形成性检查、报告结构、协作角色 */
  _enrichBlueprintPedagogy(goal, blueprint) {
    if (!blueprint?.schemes?.length) return blueprint;
    const bp = blueprint;
    const type = this._classifyProjectType(goal);
    const art = this._compactProjectLabel(goal, this._extractTopicProfile(goal));

    if (!bp.drivingQuestion || bp.drivingQuestion.length < 12) {
      bp.drivingQuestion = this._synthesizeDrivingQuestion(goal, bp);
    }
    if (!Array.isArray(bp.reportOutline) || bp.reportOutline.length < 3) {
      bp.reportOutline = this._inferReportOutline(goal, bp, type);
    }
    if (!Array.isArray(bp.formativeCheckpoints) || bp.formativeCheckpoints.length < 3) {
      bp.formativeCheckpoints = this._inferFormativeCheckpoints(goal, bp);
    }
    if ((!Array.isArray(bp.collaborationRoles) || !bp.collaborationRoles.length)
      && this._suggestsGroupCollaboration(goal, type)) {
      bp.collaborationRoles = this._inferCollaborationRoles(goal, type);
    }

    bp.schemes = (bp.schemes || []).map(s => ({
      ...s,
      phases: (s.phases || []).map((p, i, arr) => {
        const role = i === 0 ? 'foundation' : (i < arr.length - 1 ? 'bridge' : 'core');
        const acceptance = Array.isArray(p.acceptance) && p.acceptance.length
          ? p.acceptance
          : (p.steps || []).slice(0, 3).map(st =>
            `□ ${String(st).slice(0, 42)}${String(st).length > 42 ? '…' : ''}（有记录/签字）`);
        return {
          ...p,
          venue: p.venue || this._inferPhaseVenue(goal, p.phase, role, type, i, arr.length),
          durationHint: p.durationHint || this._inferPhaseDurationHint(i, arr.length),
          tools: Array.isArray(p.tools) && p.tools.length ? p.tools : this._inferPhaseTools(goal, p.phase, this._goalProfile(goal, bp)),
          acceptance,
        };
      }),
    }));
    return bp;
  }

  _synthesizeDrivingQuestion(goal, blueprint) {
    const g = String(goal || '').trim();
    const qMatch = g.match(/[^。！？\n]{6,90}[？?]/);
    if (qMatch) return qMatch[0].replace(/^【[^】]+】/g, '').trim();
    const art = this._compactProjectLabel(goal, this._extractTopicProfile(goal));
    const deliv = blueprint?.deliverable || '';
    const constraint = (blueprint?.constraints || [])[0] || '';
    const type = this._classifyProjectType(goal);
    const opener = ({
      'consumer-decision': '在给定约束下，如何用学科方法比较并决策',
      'social-inquiry': '如何通过调查与数据分析回答',
      'scientific-inquiry': '如何通过实验与证据探究',
      'engineering': '如何设计、制作并验证',
      'health-life': '如何基于科学原理制定并评估',
      'life-planning': '如何策划并执行',
      'study-trip': '如何通过实地调研完成',
    })[type] || '如何围绕真实情境完成';
    let q = `${opener}「${art}」`;
    if (deliv && deliv.length >= 4) q += `，并产出${deliv}`;
    q += '？';
    if (constraint && constraint.length >= 4) q += `（须考虑：${constraint.slice(0, 36)}）`;
    return q;
  }

  _inferReportOutline(goal, blueprint, type) {
    const art = this._compactProjectLabel(goal, this._extractTopicProfile(goal));
    const maps = {
      'consumer-decision': [
        `背景与需求（「${art}」情境）`, '约束条件与筛选标准', '方案对比与数据表', '模型测算与假设说明', '推荐结论与理由', '局限与未解决问题',
      ],
      'social-inquiry': [
        `问题与样本设计（「${art}」）`, '调查方法与数据来源', '数据整理与统计发现', '分析与解释', '建议或倡议', '局限说明',
      ],
      'scientific-inquiry': ['问题与假设', '实验设计与变量', '数据记录与处理', '分析与结论', '误差与改进'],
      'engineering': ['需求与指标', '方案与结构设计', '制作与调试记录', '测试数据与分析', '迭代说明与展示'],
      'health-life': ['现状调查', '科学原理说明', '干预/预防方案', '实践记录', '效果评估与宣传'],
      'humanities-literary': ['立意与选材', '结构与表达', '修改过程', '作品定稿', '创作说明'],
    };
    return maps[type] || [
      `背景与任务（「${art}」）`, '过程与方法', '数据/证据', '分析与发现', '结论与建议', '反思',
    ];
  }

  _inferFormativeCheckpoints(goal, blueprint) {
    const scheme = this._getRecommendedScheme(blueprint);
    const phases = scheme?.phases || [];
    const checks = [];
    phases.forEach((p, i) => {
      const week = i + 1;
      const deliv = p.deliverable || p.phase || `阶段${i + 1}`;
      checks.push(`第${week}阶段末：提交「${String(deliv).slice(0, 28)}」并经教师/组长核查`);
    });
    if (blueprint?.deliverable) {
      checks.push(`终稿前：${String(blueprint.deliverable).slice(0, 32)} 同伴互评 1 轮`);
    }
    return checks.slice(0, 6);
  }

  _suggestsGroupCollaboration(goal, type) {
    if (/小组|团队|合作|分工/.test(String(goal || ''))) return true;
    return ['consumer-decision', 'social-inquiry', 'engineering', 'life-planning',
      'exhibition-redesign', 'study-trip', 'business-economics', 'health-life'].includes(type);
  }

  _inferCollaborationRoles(goal, type) {
    const maps = {
      'consumer-decision': [
        { role: '需求调研员', duty: '收集资料、填写数据采集表并标注来源' },
        { role: '建模分析员', duty: '建立对比/测算模型并核对假设' },
        { role: '可视化设计', duty: '制作统计图、对比表与 PPT 图表' },
        { role: '报告与答辩', duty: '整合报告、准备汇报与答辩要点' },
      ],
      'engineering': [
        { role: '调研与需求', duty: '明确指标、记录约束与测试标准' },
        { role: '设计与制作', duty: '方案草图、搭建/编程与过程记录' },
        { role: '测试与数据', duty: '测量、记录数据并分析误差' },
        { role: '文档与展示', duty: '验收表、展示稿与答辩' },
      ],
      'social-inquiry': [
        { role: '调查设计', duty: '问卷/访谈提纲与抽样方案' },
        { role: '数据采集', duty: '发放回收、实地记录与来源标注' },
        { role: '统计分析', duty: '整理表格、制图与发现归纳' },
        { role: '报告撰写', duty: '报告结构与答辩准备' },
      ],
    };
    return maps[type] || [
      { role: '资料采集', duty: '调研、记录与来源标注' },
      { role: '分析建模', duty: '数据处理、计算或实验记录' },
      { role: '成果整合', duty: '报告/作品整合与排版' },
      { role: '展示答辩', duty: '汇报演示与互评' },
    ];
  }

  _inferPhaseVenue(goal, phaseName, role, type, index, total) {
    const phase = String(phaseName || '');
    if (/校外|实地|4S|田野|研学|走访|参观|市场|店铺/.test(phase)) return '校外/实地';
    if (/线上|网络|文献|检索/.test(phase)) return '线上+教室';
    if (/家庭|居家|课后/.test(phase)) return '家庭+教室';
    if (/展示|汇报|答辩|评审/.test(phase) || (role === 'core' && index === total - 1)) return '教室';
    if (/调研|调查|访谈|问卷|采集/.test(phase)) {
      return type === 'study-trip' ? '校外+线上' : '校外/家庭+线上';
    }
    if (role === 'foundation' || /知识|准备|学习|课件/.test(phase)) return '教室/机房';
    if (role === 'bridge') return '教室+家庭';
    return '教室';
  }

  _inferPhaseDurationHint(index, total) {
    if (total <= 3) return `约第 ${index + 1} 阶段（${index === 0 ? '1' : '1–2'} 周）`;
    return `约第 ${index + 1} 周`;
  }

  _inferKnowledgeSceneUse(node, goal) {
    if (!node?.name) return '';
    const name = String(node.name);
    const art = this._compactProjectLabel(goal, this._extractTopicProfile(goal));
    const subj = node.subject || '';
    if (/函数|方程|不等式/.test(name)) {
      return `建立「${art}」中的数量关系或约束条件，用于测算、对比或筛选`;
    }
    if (/统计|数据|平均|方差|百分比|图表/.test(name)) {
      return `整理「${art}」的调研/实验数据并制图对比`;
    }
    if (/说明文|写作|论证|报告/.test(name) || subj === 'chinese') {
      return `撰写「${art}」阶段性或最终说明/论证段落`;
    }
    if (/实验|探究|变量|测量/.test(name)) {
      return `设计并完成与「${art}」相关的实验或观测`;
    }
    if (subj === 'politics') {
      return `从规则、责任或公共议题角度分析「${art}」中的价值判断与行动建议`;
    }
    if (subj === 'psychology') {
      return `运用沟通、共情或自我认知理解「${art}」中的人际与情绪因素`;
    }
    return `将「${name}」应用于「${art}」的本阶段任务`;
  }

  _buildKnowledgeScenes(knowledgeNames, matchedNodes, goal) {
    const byName = new Map((matchedNodes || []).map(n => [n.name, n]));
    return (knowledgeNames || []).filter(Boolean).map(name => {
      const node = byName.get(name);
      return {
        name,
        sceneUse: node ? this._inferKnowledgeSceneUse(node, goal) : `支撑「${this._compactProjectLabel(goal)}」本阶段任务`,
      };
    });
  }

  /** 从用户输入提取交付物锚点 — 一切任务步骤必须围绕此展开，禁止套其他项目模板 */
  _goalProfile(goal, blueprint = null) {
    const g = String(goal || '').trim();
    const topic = this._extractTopicProfile(g);
    const artifact = this._compactProjectLabel(g, topic);
    const shortLabel = artifact;
    const domains = {
      woodwork: /工坊|鲁班|榫卯|木结构|古典|斗拱|飞檐|建筑模型|微缩|木作/.test(g),
      robot: (/机器人|物流机器人|循迹|机械臂|自动驾驶/.test(g) || (/无人机/.test(g) && /设计|制作|研发|搭建|开发|装置/.test(g))) && !topic.matched,
      software: /App|程序|软件|系统开发|小程序|网站|编程|算法/.test(g),
      writing: /作文|倡议|报告|诗|文章|演讲|说明文|创新/.test(g),
      survey: /调查|问卷|访谈|统计|探寻|探索|调研/.test(g),
      lowAltitude: topic.kind === 'industry-innovation' && topic.coreTopic === '低空经济',
      industry: topic.kind === 'industry-innovation',
      exhibition: topic.kind === 'exhibition-redesign',
      planting: topic.kind === 'planting-cultivation',
      energyAnalysis: topic.kind === 'energy-analysis' || this._isEnergyAnalysisGoal(g),
    };

    const mismatchRes = [];
    const type = this._classifyProjectType(g);
    if (['social-inquiry', 'humanities-literary', 'study-trip', 'business-economics'].includes(type)
      && !domains.robot && !domains.software && !/设计|制作|搭建|装置|原型|硬件|编程/.test(g)) {
      mismatchRes.push(/智慧城市|工程设计思维|环境搭建|硬件组件|原型驱动|MVP|程序设计|电解池|焊接|传感器模块|物流配送|烧录|GPIO/);
    }
    if (domains.lowAltitude || domains.industry) {
      mismatchRes.push(/现代物流管理|智慧城市|工程设计思维|环境搭建|硬件组件|编写.*控制|榫卯|斗拱|焊接|搭建原型|MVP|快速原型|程序设计|电解池/);
    }
    if (domains.exhibition) {
      mismatchRes.push(/原型驱动迭代|快速原型|MVP|环境搭建|程序设计|电解池|招生简章|现代物流|智慧城市|工程设计思维/);
    }
    if (domains.planting) {
      mismatchRes.push(/原型驱动迭代|浸润式场景|快速原型|MVP|硬件准备|程序设计|牛顿定律|化学方程式|电解池|机械玩具|机器人/);
    }
    if (domains.energyAnalysis) {
      mismatchRes.push(/稳定性测试|接线|组装|原型驱动|MVP|硬件准备|工程安全|故障排查|用户访谈|装置原型|烧录|GPIO|传感器模块|电机驱动/);
    }
    if (topic.matched) {
      mismatchRes.push(/递进式实施|原型驱动迭代|可展示的项目原型/);
    }
    if (domains.woodwork && !domains.robot && !domains.software) {
      mismatchRes.push(/硬件组件|环境搭建|编写.*控制逻辑|基础控制|配置.*框架|安装.*软件|电机驱动|传感器模块|接口协议|部署上线/);
    }
    if (domains.robot && !domains.woodwork) {
      mismatchRes.push(/斗拱|飞檐|榫卯|木工锯|刨子|古典建筑纹样/);
      if (!domains.lowAltitude && !/无人机|航空|飞行|低空/.test(g)) {
        mismatchRes.push(/飞行控制|航空电子|飞控|航空|航天|无人机|弹道|火箭|导弹|空域|低空|抗生素|耐药|医药|药物|细胞分裂|细胞的分裂|内燃机|购车|科学理论补全|科学原理补课/);
      }
    }
    if (this._isGroundRoboticsGoal(g) && !/无人机|航空|飞行|低空/.test(g)) {
      mismatchRes.push(/飞行|航空|航天|无人机|飞控|抗生素|耐药|医药|药物|细胞|免疫|内燃机|购车|科学理论补全|科学原理补课/);
    }
    if (domains.writing && !domains.robot && !domains.software) {
      mismatchRes.push(/焊接|电路|传感器|电机|BOM表|下料/);
    }

    return {
      raw: g,
      artifact,
      shortLabel,
      domains,
      mismatchRes,
      topic,
      blueprintDeliverable: blueprint?.deliverable || topic?.deliverableHint || '',
      gradeBand: this._parseExplicitGradeBand(g),
    };
  }

  _stepDomainMismatch(step, profile) {
    const s = String(step || '');
    if (!s || !profile?.mismatchRes?.length) return false;
    return profile.mismatchRes.some(re => re.test(s));
  }

  /** 蓝图 knowledgeHints 是否与项目主题无关（用于课标检索前清洗） */
  _isIrrelevantBlueprintHint(hint, goal) {
    const h = String(hint || '').trim();
    if (!h || h.length < 2) return true;
    if (this._isGroundRoboticsGoal(goal)) {
      if (/飞行|航空|航天|无人机|飞控|弹道|火箭|导弹|空域|低空|UAV|eVTOL|机翼|气动|起降|航空电子/.test(h)) return true;
      if (/抗生素|耐药|免疫|疫苗|病毒|细菌|医药|药物|用药|细胞|分裂|分化|人体|器官|病理|疾病|基因|DNA|光合|酶|微生物/.test(h)) return true;
      if (/内燃机|购车|燃油车|电动车|混动|油电|尾气|碳足迹|新能源对比/.test(h) && !this._isConsumerDecisionGoal(goal)) return true;
      if (/电解池|原电池|有机合成|正则表达式|形式语言|编译原理/.test(h)) return true;
    }
    if (this._isConsumerDecisionGoal(goal) && /循迹|巡线|红外传感|电机驱动|PID|避障|小车制作|飞控/.test(h)) return true;
    if (this._isSocialOrCivicInquiryGoal(goal) && /细胞|细胞膜|有丝分裂|减数分裂|抗生素|免疫|基因|DNA|光合|酶|微生物|生物分类/.test(h)) return true;
    if (this._isEnergyAnalysisGoal(goal) && /大气环流|三圈环流|季风|宇宙环境|热化学|焓变|有机合成|接线|原型测试|稳定性测试/.test(h)) return true;
    return false;
  }

  _isIrrelevantBlueprintStep(step, goal) {
    const s = String(step || '');
    if (!s) return true;
    if (this._isGroundRoboticsGoal(goal)) {
      if (/飞行|航空|航天|无人机|抗生素|耐药|免疫|细胞|医药|药物|内燃机|购车|新能源对比|电解池|航空电子|飞控/.test(s)) return true;
    }
    return false;
  }

  _sanitizeSingleBlueprintPhase(p, goal, profile, domains, phaseIndex) {
    const dom = domains[phaseIndex] || domains[domains.length - 1];
    const genericPhaseRe = /科学理论补全|科学原理补课|跨学科素养|素养提升/;
    let phase = String(p.phase || '');
    if (genericPhaseRe.test(phase) && dom) phase = dom.label;
    const steps = (p.steps || []).map(st => String(st)).filter(st =>
      st && !this._stepDomainMismatch(st, profile) && !this._isIrrelevantBlueprintStep(st, goal)
    );
    let hints = (p.knowledgeHints || []).filter(h => !this._isIrrelevantBlueprintHint(h, goal));
    if (hints.length < 2 && dom) {
      hints = [...new Set([...hints, ...dom.keywords.slice(0, 5)])].slice(0, 6);
    }
    return { ...p, phase, steps, knowledgeHints: hints };
  }

  _sanitizeBlueprintStringsInPlace(bp, goal) {
    if (!bp) return bp;
    const clean = (t) => this._sanitizeBlueprintText(t, goal);
    if (bp.projectSummary) bp.projectSummary = clean(bp.projectSummary);
    if (bp.deliverable) bp.deliverable = this._sanitizeDeliverableTitle(bp.deliverable, goal);
    (bp.schemes || []).forEach((s) => {
      if (s.name) s.name = clean(s.name);
      if (s.summary) s.summary = clean(s.summary);
      s.pros = (s.pros || []).map(clean).filter(Boolean);
      s.cons = (s.cons || []).map(clean).filter(Boolean);
      s.phases = (s.phases || []).map((p) => ({
        ...p,
        phase: this._cleanPhaseName(p.phase, goal),
        deliverable: p.deliverable ? this._sanitizeDeliverableTitle(p.deliverable, goal) : p.deliverable,
        steps: (p.steps || []).map(st => this._stripGoalMarkup(st, goal)).filter(Boolean),
      }));
    });
    return bp;
  }

  _sanitizeBlueprintPhasesInPlace(bp, goal) {
    if (!bp?.schemes?.length) return bp;
    this._sanitizeBlueprintStringsInPlace(bp, goal);
    const profile = this._goalProfile(goal, bp);
    const domains = this._inferProjectDomains(goal);
    bp.schemes.forEach(s => {
      s.phases = (s.phases || [])
        .map((p, i) => this._sanitizeSingleBlueprintPhase(p, goal, profile, domains, i))
        .filter(p => (p.steps || []).length > 0 || (p.knowledgeHints || []).length > 0);
    });
    return bp;
  }

  _filterPhaseKnowledgeNames(names, goal) {
    return (names || []).map(n => String(n)).filter(n => n.length >= 2 && !this._isIrrelevantBlueprintHint(n, goal));
  }

  _goalTokens(artifact) {
    const t = String(artifact || '').replace(/\s/g, '');
    const tokens = [];
    if (t.length >= 4) tokens.push(t.slice(0, 4));
    for (let i = 0; i < t.length - 1; i++) {
      const w = t.slice(i, i + 2);
      if (w.length === 2 && !/[的与及了在]$/.test(w)) tokens.push(w);
    }
    return [...new Set(tokens)].slice(0, 8);
  }

  _stepAnchoredToGoal(step, profile) {
    const s = String(step || '');
    if (!s) return false;
    if (s.includes(profile.artifact)) return true;
    const tokens = this._goalTokens(profile.artifact);
    return tokens.some(t => t.length >= 2 && s.includes(t));
  }

  _phaseContext(phase, blueprint, goal = '') {
    const subIds = phase?.subsystemIds || [];
    const subs = (blueprint?.subsystems || []).filter(s => subIds.includes(s.id));
    return {
      phaseName: this._cleanPhaseName(String(phase?.phase || phase?.name || '').trim(), goal),
      deliverable: phase?.deliverable
        ? this._sanitizeDeliverableTitle(phase.deliverable, goal)
        : '',
      hints: (phase?.knowledgeHints || []).slice(0, 4),
      subsystems: subs.map(s => s.name).filter(Boolean),
      subDesc: subs.map(s => s.description).filter(Boolean).join('；'),
    };
  }

  /** 清洗 phaseName：去除 AI 误注入的 goal 前缀与重复冗余 */
  _cleanPhaseName(raw, goal = '') {
    let name = this._stripGoalMarkup(raw, goal);
    const phaseTail = name.match(/(?:立意|选材|阅读|素材|结构|表达|创作|修改|展示|朗诵|调查|测算|测试|验收|策划|调研)[^，。；]{0,10}阶段?/);
    if (phaseTail) name = phaseTail[0];
    else if (name.length > 24) {
      const lastSeg = name.split(/[，,；;、」]/).pop().trim();
      if (lastSeg && lastSeg.length >= 2 && lastSeg.length <= 16) name = lastSeg;
    }
    if (name.length > 16) name = name.slice(0, 16);
    return name || '本阶段';
  }

  _expandStepAnchoredToGoal(rawStep, goal, phase, profile, ctx, stepIdx) {
    const artifact = profile.shortLabel || profile.artifact;
    const hints = ctx.hints.join('、') || '本阶段相关知识';
    const phaseName = ctx.phaseName || `阶段${stepIdx + 1}`;
    const outName = this._unwrapDeliverableName(ctx.deliverable) || `${artifact}·${phaseName}产出`;
    const verbs = ['记录', '完成', '制作', '撰写', '测量', '绘制'];
    const verb = verbs[stepIdx % verbs.length];
    const blob = `${phaseName} ${ctx.subsystems.join(' ')} ${rawStep || ''}`;

    if (profile.domains.planting || /植物|种植|栽培|园艺|光合|萌发|月季|花卉/.test(blob)) {
      const crop = profile.topic?.crop || this._plantingCropLabel(goal);
      if (/分类|识别|特征|结构|器官/.test(blob)) {
        return `辨认「${artifact}」中的${crop}：绘制植物结构简图并标注根/茎/叶/花，填写分类特征表（≥4项可观察特征）`;
      }
      if (/生长|光合|萌发|环境|水分|根|蒸腾/.test(blob)) {
        return `学习${crop}生长原理：查阅资料说明光合/根系吸收/萌发条件，制作「${artifact}」生长条件对照表（光照/水分/温度各1列）`;
      }
      if (/栽培|种植|土壤|浇水|施肥|移栽|扦插|养护/.test(blob)) {
        return `完成「${artifact}」${crop}栽培实操：按步骤记录挖穴→定植→浇透水，填写栽培日志（日期/操作/天气/问题各1条）`;
      }
      if (/观察|记录|测量|数据|图表|变化/.test(blob)) {
        return `每周2次测量「${artifact}」${crop}株高/叶片数，录入表格并绘制折线图（至少4个数据点）`;
      }
      if (/日记|报告|总结|分享/.test(blob)) {
        return `撰写「${artifact}」种植观察日记（≥300字）：含分类认识、栽培过程、生长变化与1条改进建议`;
      }
      return `围绕「${artifact}」完成${phaseName}：结合 ${hints} 整理${crop}种植资料并填写可核查记录表`;
    }
    if (profile.domains.exhibition || /馆|展厅|展陈|太空|天文|科普/.test(blob)) {
      if (/诊断|现状|问题|失控|隐患/.test(blob)) {
        return `走访「${artifact}」并填写现状诊断表：拍摄≥5张问题点位照片，列出≥8条失控/安全隐患（附整改优先级）`;
      }
      if (/主题|策划|内容|天文|太空/.test(blob)) {
        return `为「${artifact}」策划展陈主题：确定1条主线+3个分区主题，各写100字科普文案并标注对应课标知识点`;
      }
      if (/设计|布局|动线|展板|展陈/.test(blob)) {
        return `绘制「${artifact}」展陈平面图（A3）：标注参观动线、3处互动点位尺寸与材料，附展板草图2张`;
      }
      if (/整改|实施|布置|预算/.test(blob)) {
        return `编制「${artifact}」整改实施清单：列10项任务（负责人/工期/预算/安全注意），合计经费并附物资表`;
      }
      if (/验收|开放|讲解|宣传|展示/.test(blob)) {
        return `完成「${artifact}」开放验收：按检查表逐项打勾，录制3分钟讲解视频或撰写300字宣传稿`;
      }
      return `围绕「${artifact}」完成${phaseName}：结合 ${hints} 整理展陈资料并产出可核查记录表`;
    }
    if (profile.domains.energyAnalysis || this._isEnergyAnalysisGoal(goal)) {
      if (/日照|辐射|太阳能|资源|光电/.test(blob)) {
        return `查阅本地日照/辐射资料，记录校园≥7日有效日照时数，整理数据来源与光电转化效率说明`;
      }
      if (/用电|电费|电量|屋顶|面积|调查/.test(blob)) {
        return `统计校园近3个月用电量并制成折线图，测绘教学楼屋顶可用面积并绘制平面示意图（标注朝向与遮挡）`;
      }
      if (/收益|测算|函数|计算|发电|成本/.test(blob)) {
        return `建立年发电量估算模型（面积×转换效率×日照时数），完成发电量与年收益测算表并列明假设条件`;
      }
      if (/碳|减排|排放|环境|效益/.test(blob)) {
        return `查阅电力碳排放因子，计算年减排量并与校园用电碳足迹对比，制作分析图表`;
      }
      if (/报告|论证|建议|答辩|方案/.test(blob)) {
        return `撰写「${artifact}」光伏发电方案论证报告（≥600字）：含数据表、图表与3条可行性建议`;
      }
      return `围绕「${artifact}」完成${phaseName}：结合${hints}整理测算资料并产出可核查数据表`;
    }
    if (profile.domains.lowAltitude || profile.domains.industry || /产业|政策|空域|低空|场景/.test(blob)) {
      if (/政策|背景|产业|空域|法规/.test(blob)) {
        return `围绕「${artifact}」梳理${phaseName}：检索≥3条权威政策/行业资料并摘录要点，制成对照表（来源/日期/与项目关系各1列）`;
      }
      if (/场景|调研|问卷|需求|应用/.test(blob)) {
        return `围绕「${artifact}」开展${phaseName}：选定1个低空应用场景并设计10题问卷，回收≥20份有效答卷并制成统计图表`;
      }
      if (/技术|飞行|安全|原理|参数/.test(blob)) {
        return `为「${artifact}」整理${phaseName}：查阅飞行高度/载重/续航三类参数并制对比表，附起降安全距离估算示意图1张`;
      }
      if (/方案|创新|可行|论证|报告/.test(blob)) {
        return `撰写「${artifact}」${phaseName}：提出1个创新点子（200字场景描述）+成本效益简表+2条落地障碍与对策`;
      }
      return `围绕「${artifact}」完成${phaseName}：结合 ${hints} 整理产业资料并产出可核查记录表（≥5条要点+来源标注）`;
    }
    if (this._isHumanitiesLiteraryGoal(goal) || (profile.domains.writing && /诗|文集|作文|写作|朗诵|文学/.test(String(goal || '')))) {
      if (/立意|选材|主题|构思/.test(blob)) {
        return `确定「${artifact}」创作主题：列出≥8条家乡意象选题并标注情感基调，全班票选定稿≥3条`;
      }
      if (/阅读|素材|积累|语料/.test(blob)) {
        return `建立「${artifact}」素材库：摘录≥30条家乡意象语料（视觉/听觉/触觉分类），注明出处或观察场景`;
      }
      if (/结构|表达|意象|修辞|创作|初稿|写诗/.test(blob)) {
        return `完成「${artifact}」诗歌初稿：每人≥1首（≥8行），用意象检查表核对每首≥3个具象家乡元素`;
      }
      if (/修改|批注|展示|朗诵|定稿/.test(blob)) {
        return `完成「${artifact}」修改与展示：同伴互评≥2轮并保留批注，录制朗诵或编排班级诵读活动`;
      }
      return `围绕「${artifact}」完成${phaseName}：结合${hints}整理创作资料并产出可核查文稿`;
    }
    // 社会/公民调查类模板（仅垃圾分类等明确议题，禁止「分类标签」等误触发）
    const isTrueSocialSurvey = this._isSocialOrCivicInquiryGoal(goal) && !this._isHealthLifeGoal(goal);
    if (isTrueSocialSurvey) {
      if (/现状|调查|问卷|访谈|勘测|实地|走访/.test(blob)) {
        return `走访≥2处相关点位，填写${phaseName}记录表（观察项≥8条+居民访谈≥5条），附现场照片3张并标注时间与地点`;
      }
      if (/垃圾分类|四类垃圾|垃圾投放|厨余|可回收物|有害垃圾/.test(blob)) {
        return `整理四类垃圾投放标准对照表（可回收/有害/厨余/其他），列举本社区常见误投案例≥6条并注明改正做法`;
      }
      if (/统计|数据|图表|整理|分析/.test(blob)) {
        return `将调查数据录入表格并绘制≥2种统计图（条形/扇形任选），计算占比与平均数，写出3条数据结论`;
      }
      if (/建议|改进|宣传|倡议|策划|方案|报告/.test(blob)) {
        return `撰写${artifact}${phaseName}（≥400字）：含问题归纳、3条可执行改进措施与1份宣传策划要点（对象/渠道/口号各1条）`;
      }
      return `完成${artifact}${phaseName}：结合${hints}整理资料并产出可核查记录表（≥5条要点+来源标注）`;
    }
    if (/调研|勘测|现场|需求|资料/.test(blob)) {
      return `开展${phaseName}：列出5条可验证需求并制成优先级表，附3张现场/参考照片（文件命名 P${stepIdx + 1}-01~03）`;
    }
    if (/设计|方案|草图|图纸|规划|风格|定义/.test(blob)) {
      return `为「${artifact}」绘制${phaseName}草图（A3 或 CAD 均可），标注 ≥5 处关键尺寸，并结合 ${hints} 写 150 字方案说明`;
    }
    if (/材料|采购|物料|预算|成本|BOM/.test(blob)) {
      return `编制「${artifact}」${phaseName}物料清单（名称/规格/数量/单价/小计），合计预算并注明 2 条安全注意事项`;
    }
    if (/搭建|制作|组装|加工|实施|原型|开发|结构|装饰|修缮/.test(blob)) {
      return `${verb}「${artifact}」${phaseName}核心工序：按方案操作并填写过程记录表（时间、工具、问题各 ≥1 条），拍照 ≥3 张`;
    }
    if (/软件|编程|控制|算法|电路|调试/.test(blob)) {
      return `实现「${artifact}」${phaseName}功能点 1 个，附测试用例 3 条（输入/预期/实测），保存调试日志截图`;
    }
    if (/测试|验收|交付|展示|复盘|答辩/.test(blob)) {
      return `按检查表验收「${artifact}」${phaseName}成果：逐项打勾，整理交付包（${outName} + 过程记录 + 300 字说明）`;
    }
    if (ctx.subDesc) {
      return `${verb}${artifact}${phaseName}：${ctx.subDesc.slice(0, 80)}，产出「${outName}」并附可核查记录`;
    }
    const domains = this._inferProjectDomains(goal);
    const dom = domains[stepIdx] || domains[domains.length - 1];
    const templated = this._domainStepTemplates(dom, artifact, hints);
    if (templated[stepIdx % templated.length]) {
      return templated[stepIdx % templated.length];
    }
    return `${verb}${artifact}${phaseName}（结合${hints}），交付「${outName}」并附1份签字确认的过程记录表`;
  }

  _phaseStepFillers(goal, phase, profile, ctx, phaseIndex) {
    const domains = this._inferProjectDomains(goal);
    const dom = domains[phaseIndex] || domains[domains.length - 1];
    const label = profile.shortLabel || profile.artifact;
    const phaseName = ctx.phaseName || '本阶段';
    if (!dom) return [];
    const art = profile.shortLabel || profile.artifact;
    const knRef = (phase?.knowledgeHints || ctx.hints || []).slice(0, 2).map(h => `「${h}」`).join('、') || '本阶段课标知识点';

    if (this._isSocialOrCivicInquiryGoal(goal)) {
      const byId = {
        survey: `设计10题${label}调查问卷，明确样本对象与回收目标≥15份`,
        sorting: `整理垃圾分类标准与社区误投案例对照表（每类≥2条）`,
        data: `录入调查数据并绘制1张统计图，计算至少2项百分比或平均数`,
        environment: `查阅本地垃圾处理流程资料≥3条，说明与社区现状的关系`,
        proposal: `列出3条可执行改进建议并附1条宣传口号与投放渠道`,
        topic: `确定调查问题与对象，写出调查提纲（问题≥8条）`,
        collect: `完成实地走访或访谈≥5人，记录原始数据表`,
        analyze: `用表格与图表呈现调查结果，写出2条数据发现`,
        report: `撰写${label}报告初稿（≥300字），含建议与宣传策划要点`,
      };
      const hit = byId[dom.id];
      if (hit) return [hit];
      return [`结合${dom.label}完成${label}${phaseName}记录（要点≥5条+可检查产出）`];
    }
    if (this._isEnergyAnalysisGoal(goal)) {
      const byId = {
        resource: [
          `查阅日照/辐射资料并记录校园7日有效日照时数（数据来源标注）`,
          `结合光电转化原理，说明影响发电效率的2个因素并写入原理笔记`,
        ],
        electricity: [
          `统计近3个月校园用电量并绘制折线图`,
          `测绘教学楼屋顶可用面积，绘制平面示意图并标注朝向与遮挡`,
        ],
        calc: [
          `建立年发电量估算模型（面积×效率×日照时数），完成计算表`,
          `估算年发电收益与电费节约，列明电价/补贴等假设条件`,
        ],
        carbon: [
          `查阅电力碳排放因子，计算年减排量`,
          `制作减排效益对比图表，写出2条环境效益结论`,
        ],
        report: [
          `撰写光伏发电方案论证报告（≥600字）`,
          `整理3分钟答辩要点：关键数据表、图表编号与可行性论证`,
        ],
      };
      const hits = byId[dom.id];
      if (hits?.length) return hits;
      return [`结合${dom.label}完成${label}${phaseName}测算记录（数据表+图表）`];
    }
    return this._domainStepTemplates(dom, art, knRef);
  }

  _concretizePhaseSteps(goal, phase, phaseIndex, totalPhases, archetype, blueprint) {
    const profile = this._goalProfile(goal, blueprint);
    const ctx = this._phaseContext(phase, blueprint, goal);
    const raw = Array.isArray(phase?.steps) ? phase.steps : [];
    const seen = new Set();
    const steps = [];

    raw.forEach((st, i) => {
      const s = this._stripGoalMarkup(st, goal);
      if (!s) return;
      let out = s;
      const energyStepOk = this._isEnergyAnalysisGoal(goal)
        && /日照|辐射|用电|屋顶|发电|收益|减排|碳|报告|论证|测算|统计|函数|图表|模型|假设|因子/.test(s);
      const actionable = this._stepActionabilityScore(s) >= 4;
      const needsRewrite = !energyStepOk && (this._isHollowStep(s) || this._stepDomainMismatch(s, profile)
        || (!actionable && !this._stepAnchoredToGoal(s, profile)));
      if (needsRewrite) {
        out = this._expandStepAnchoredToGoal(s, goal, phase, profile, ctx, i);
      }
      if (!steps.some(ex => this._stepsNearDuplicate(ex, out)) && !seen.has(this._stepFingerprint(out))) {
        seen.add(this._stepFingerprint(out));
        steps.push(out);
      }
    });

    const fillers = this._phaseStepFillers(goal, phase, profile, ctx, phaseIndex);
    fillers.forEach((filler, idx) => {
      if (steps.length >= 2) return;
      const out = filler || this._expandStepAnchoredToGoal('', goal, phase, profile, ctx, steps.length + idx);
      if (!steps.some(ex => this._stepsNearDuplicate(ex, out)) && !seen.has(this._stepFingerprint(out))) {
        seen.add(this._stepFingerprint(out));
        steps.push(out);
      }
    });

    const goodSteps = steps.filter(s => !this._isHollowStep(s));
    const avgScore = goodSteps.length
      ? goodSteps.reduce((a, s) => a + this._stepActionabilityScore(s), 0) / goodSteps.length
      : 0;
    if (goodSteps.length < 2 || avgScore < 2) {
      const role = phaseIndex === 0 ? 'foundation' : (phaseIndex < totalPhases - 1 ? 'bridge' : 'core');
      const suggested = this._suggestPhaseSteps(goal, { role, phase: phase?.phase, nodes: [] }, phase);
      if (suggested.length) return suggested.slice(0, 4);
    }
    return (goodSteps.length ? goodSteps : steps).slice(0, 4);
  }

  _concretizeDeliverable(goal, phaseName, role, fallback, blueprint) {
    const profile = this._goalProfile(goal, blueprint);
    const phase = this._cleanPhaseName(phaseName, goal);
    const art = profile.shortLabel || profile.artifact;
    if (fallback && fallback.length >= 8 && !/阶段成果|探究任务|素养|能力/.test(fallback)
      && !this._containsGoalMarkup(fallback)) {
      return this._sanitizeDeliverableTitle(fallback, goal);
    }
    if (this._isEnergyAnalysisGoal(goal)) {
      if (/资源|日照|太阳能|辐射/.test(phase)) return `「${art}」日照/辐射调查记录表（≥7天数据+来源标注）`;
      if (/用电|屋顶|调查/.test(phase)) return `「${art}」用电量统计表 + 屋顶面积测算示意图`;
      if (/收益|测算|计算|函数/.test(phase)) return `「${art}」年发电量与收益测算表（含假设说明）`;
      if (/减排|碳|环境|效益/.test(phase)) return `${art}碳减排效益分析图表 + 对比说明`;
      if (/论证|报告/.test(phase)) return `${/光伏/.test(art) ? art : art + '光伏'}发电方案论证报告`;
    }
    if (/算力中心|数据中心|太空算力|卫星计算|轨道计算/.test(String(goal || ''))) {
      if (/需求|约束|原理|调研/.test(phase)) return `「${art}」需求与约束定义表（任务负载+轨道环境+性能指标）`;
      if (/架构|结构|装置|设计|方案/.test(phase)) return `「${art}」系统架构图与方案对比表（含电源/热控/通信/冗余）`;
      if (/控制|实现|调度|运行/.test(phase)) return `「${art}」调度控制流程图 + 故障切换策略说明`;
      if (/测试|迭代|验证|验收/.test(phase)) return `「${art}」测试验收表 + 工程实施方案推荐稿`;
    }
    const projType = this._classifyProjectType(goal);
    if (projType === 'social-inquiry' || /研究|对比|发展史|典型|案例|调查|问卷|访谈/.test(String(goal || ''))) {
      if (/脉络|史料|时间|背景|梳理|资料|收集/.test(phase)) return `「${art}」专题资料卡/时间轴（≥5个关键节点+来源标注）`;
      if (/案例|典型|选取|调研|调查|问卷|访谈|样本/.test(phase)) return `「${art}」案例/样本记录表（≥3例+来源标注）`;
      if (/维度|指标|框架|设计|统计|整理/.test(phase)) return `「${art}」对比/分析维度表（≥4项指标+操作定义）`;
      if (/对比|分析|结论|专题/.test(phase)) return `「${art}」对比分析图表（≥2组可比数据）`;
      if (/报告|结论|展示|写作/.test(phase)) return `「${art}」研究报告（含结论与局限说明）`;
    }
    if (/调研|勘测|现场|需求/.test(phase)) return `「${art}」调研记录表（需求清单+照片编号）`;
    if (/设计|方案|草图|图纸|风格/.test(phase)) return `「${art}」${phase}图册（标注尺寸的方案稿）`;
    if (/材料|采购|物料|预算/.test(phase)) return `「${art}」材料/经费清单（含规格与合计）`;
    if (/测试|验收|交付|展示/.test(phase)) return `「${art}」验收检查表 + 展示说明（可现场核查）`;
    if (/搭建|制作|组装|原型|装饰|实施/.test(phase)) return `「${art}」${phase}实物/模型 + 过程照片（≥3 张）`;
    return profile.blueprintDeliverable || `「${art}」阶段成果（可展示、可打分）`;
  }

  _concretizeBlueprint(goal, blueprint, archetype = null) {
    if (!blueprint?.schemes?.length) return blueprint;
    if (blueprint._concretized) return blueprint;
    const profile = this._goalProfile(goal, blueprint);
    let bp = this._shallowCloneBlueprint(blueprint);
    bp = this._enrichBlueprintMetadata(goal, bp);

    if (!bp.deliverable || /素养|能力|精神|阶段成果$/.test(bp.deliverable) || bp.deliverable.length < 8) {
      bp.deliverable = profile.blueprintDeliverable || `可交付的「${profile.artifact}」成果包（作品+记录+说明）`;
    }
    if (this._isEnergyAnalysisGoal(goal) && /测算表|收益|减排|论证报告/.test(bp.deliverable)) {
      bp.deliverable = profile.topic?.deliverableHint || bp.deliverable;
    }

    if (this._isFiltrationGoal(goal) && (!Array.isArray(bp.scopeLimits) || !bp.scopeLimits.length)) {
      bp.scopeLimits = [
        '目标是可验证地减少模型颗粒，不能宣称已去除所有微塑料',
        '不能把课堂/家庭自制装置等同于认证饮水净化系统',
        '模型颗粒减少率不能写成真实微塑料去除率',
      ];
    }
    if (this._isFiltrationGoal(goal) && (!Array.isArray(bp.successCriteria) || !bp.successCriteria.length)) {
      bp.successCriteria = [
        '完成原水/仅粗滤/完整三级三组对照实验',
        '固定水量（如300mL）并记录过滤时间或流速',
        '报告写明各滤层职责与装置局限',
      ];
    }

    bp.schemes = bp.schemes.map(scheme => ({
      ...scheme,
      phases: (scheme.phases || []).map((p, i, arr) => {
        const role = i === 0 ? 'foundation' : (i < arr.length - 1 ? 'bridge' : 'core');
        const steps = this._concretizePhaseSteps(goal, p, i, arr.length, archetype, bp);
        const deliverable = this._concretizeDeliverable(goal, p.phase, role, p.deliverable, bp);
        const tools = p.tools || this._inferPhaseTools(goal, p.phase, profile);
        const acceptance = steps.map((st, j) => `□ ${String(st).slice(0, 48)}${String(st).length > 48 ? '…' : ''}（有记录/照片/签字）`);
        return { ...p, steps, deliverable, tools, acceptance };
      }),
    }));
    bp._concretized = true;
    return bp;
  }

  _inferPhaseTools(goal, phaseName, profileOrType) {
    const phase = String(phaseName || '');
    const profile = profileOrType?.artifact ? profileOrType : this._goalProfile(goal);
    const g = profile.raw || goal;
    const type = this._classifyProjectType(g);
    if (this._isConsumerDecisionGoal(g) || type === 'consumer-decision') {
      if (/调研|需求|收集|资料/.test(phase)) return ['需求清单模板', '数据采集表', '来源标注规范'];
      if (/对比|筛选|约束|比选/.test(phase)) return ['约束条件清单', '方案对比矩阵', '假设说明表'];
      if (/测算|模型|成本|函数|计算|分析/.test(phase)) return ['计算工作表', '假设参数表', '图表模板'];
      if (/报告|决策|建议|论证/.test(phase)) return ['报告提纲', '论证段落模板', '答辩要点清单'];
    }
    if (type === 'social-inquiry') {
      if (/选题|设计|问卷|访谈/.test(phase)) return ['问卷/访谈提纲模板', '抽样方案表', '伦理说明'];
      if (/收集|实地|调查/.test(phase)) return ['数据采集表', '来源标注规范', '照片/录音编号表'];
      if (/统计|整理|分析/.test(phase)) return ['统计表模板', '图表工具', '异常值处理说明'];
      if (/报告|结论/.test(phase)) return ['报告结构模板', '论证检查表', '答辩提纲'];
    }
    if (/算力中心|数据中心|太空算力|卫星计算|轨道计算/.test(String(g || ''))) {
      if (/需求|约束|原理|调研/.test(phase)) return ['需求矩阵模板', '公开技术资料', '指标清单'];
      if (/架构|结构|设计|方案/.test(phase)) return ['系统架构图模板', '方案对比矩阵', '风险清单'];
      if (/控制|实现|调度|运行/.test(phase)) return ['流程图工具', '接口清单模板', '异常场景表'];
      if (/测试|迭代|验证|验收/.test(phase)) return ['测试指标表', '仿真/估算表', '迭代记录表'];
    }
    if (/调研|勘测/.test(phase)) return ['记录表模板', '相机/手机', profile.domains.woodwork ? '卷尺' : '数据来源清单'];
    if (/设计|草图|图纸|风格/.test(phase)) {
      return profile.domains.software ? ['绘图/CAD 或设计工具', '尺寸标注规范'] : ['A3纸或绘图纸', '铅笔尺规', '标注笔'];
    }
    if (/材料|采购|预算/.test(phase)) return ['物料清单模板', '计算器', '询价记录表'];
    if (/搭建|制作|组装|结构|装饰/.test(phase)) {
      if (profile.domains.robot) return ['螺丝刀/扳手', '万用表', '调试线', '安全防护'];
      if (profile.domains.woodwork) return ['手锯/砂纸', '木工胶', '角尺', '护目镜'];
      return ['分工表', '过程记录表', '相机'];
    }
    if (/软件|编程|控制|电路/.test(phase) || profile.domains.software) return ['开发环境', '版本记录', '测试用例表'];
    if (/测试|验收|展示/.test(phase)) return ['验收量规', '展示稿模板', '相机'];
    if (/撰写|报告|作文|倡议/.test(phase) || profile.domains.writing) return ['文稿模板', '修改痕迹记录', '格式规范'];
    return ['过程记录表', '相机'];
  }

  _pickConcreteDeliverable(lp, bp, role, goal) {
    const vague = d => !d || /素养|能力|精神|品格|阶段成果物?$|阶段原型|探究任务/.test(String(d)) || String(d).length < 6;
    const lpD = lp?.deliverable || lp?.output || '';
    const bpD = bp?.deliverable || '';
    if (!vague(lpD)) return lpD;
    if (!vague(bpD)) return bpD;
    return this._defaultDeliverable(role || 'core', goal);
  }

  /** 主线相关性：硬门禁 + 泛化相关性分（不依赖项目类型特化规则） */
  _isMainlineRelevant(node, goal, domains, blueprint = null, archetype = null, floorMode = false) {
    if (!this._passesHardNodeGate(node, goal, archetype)) return false;
    const bp = blueprint || this._activeBlueprint || null;
    const score = this._scoreUniversalRelevance(node, goal, bp, domains, archetype);
    return score >= this._relevanceKeepThreshold(floorMode);
  }

  _filterMainlineNodes(matched, goal, archetype = null) {
    const audit = this._verifyAndPruneNodes(matched, goal, archetype, '主线过滤');
    return audit.kept;
  }

  _scoreNodeForGoal(node, goalTerms, filterSubjects, complex, domains, goal = '') {
    let score = 0;
    const nameLower = (node.name || '').toLowerCase();
    const defLower = (node.definition || node.description || '').toLowerCase();
    const concepts = (node.key_concepts || []).join(' ').toLowerCase();
    (goalTerms || []).forEach(term => {
      if (nameLower.includes(term)) score += 4;
      if (concepts.includes(term)) score += 2;
      if (defLower.includes(term)) score += 1;
    });
    if (domains && domains.length) score += this._scoreNodeForDomains(node, domains);
    if (filterSubjects && filterSubjects.includes(node.subject)) score += 1;
    const grade = parseInt(node.grade, 10) || 0;
    if (!this._shouldAllowUniversityNodes(goal) && this._isUniversityNode(node)) score -= 30;
    if (this._isK12Node(node)) score += 4;
    if (complex && grade >= 7) score += 1;
    if (complex && grade > 0 && grade < 7) score -= 8;
    if (goal && (domains?.length || this._isStemProjectGoal(goal))) {
      score += this._stemBreadthScoreAdjust(node, goal);
    }
    if (goal) {
      score += Math.min(12, this._scoreUniversalRelevance(node, goal, this._activeBlueprint, domains, null) * 0.35);
    }
    return score;
  }

  /** STEM 候选均衡：子系统覆盖 + 学科/形态多样，压制定律/计算堆砌 */
  _pickStemBalancedCandidates(pool, maxCount, domains, goal) {
    const stem = this._isStemProjectGoal(goal) && domains && domains.length;
    if (!stem) {
      return [...pool]
        .sort((a, b) => (b._score || 0) - (a._score || 0))
        .slice(0, maxCount);
    }

    const ranked = pool.map(n => ({
      n,
      score: (n._score || 0) + this._stemBreadthScoreAdjust(n, goal)
    })).sort((a, b) => b.score - a.score);

    const picked = [];
    const seen = new Set();
    const subjectCount = {};
    const kindCount = {};
    const maxMath = Math.max(1, Math.floor(maxCount * 0.22));
    const maxCalc = Math.max(0, Math.floor(maxCount * 0.15));
    const maxLaw = Math.max(1, Math.floor(maxCount * 0.25));

    const canAdd = (n) => {
      if (!n || seen.has(n.id)) return false;
      const subj = n.subject || '';
      if (subj === 'math' && (subjectCount.math || 0) >= maxMath) return false;
      if (this._isQuantitativeCalcNode(n) && (kindCount.calculation || 0) >= maxCalc) return false;
      if (this._isConservationLawNode(n) && (kindCount.law || 0) >= maxLaw) return false;
      return true;
    };
    const add = (n) => {
      if (!canAdd(n)) return false;
      seen.add(n.id);
      picked.push(n);
      subjectCount[n.subject] = (subjectCount[n.subject] || 0) + 1;
      const kind = this._stemKnowledgeKind(n);
      kindCount[kind] = (kindCount[kind] || 0) + 1;
      return true;
    };
    const rankForDomain = (domain) => ranked
      .filter(x => !seen.has(x.n.id) && this._scoreNodeForDomains(x.n, [domain]) > 0)
      .sort((a, b) => (b.score + this._stemKindPreference(b.n, goal) * 3)
        - (a.score + this._stemKindPreference(a.n, goal) * 3));

    domains.forEach(domain => {
      const candidates = rankForDomain(domain);
      const preferred = candidates.find(x => canAdd(x.n) && !this._isQuantitativeCalcNode(x.n));
      if (preferred) add(preferred.n);
      else if (candidates[0]) add(candidates[0].n);
    });

    const mustHave = [
      n => n.subject === 'chemistry',
      n => n.subject === 'info-tech',
      n => this._stemKnowledgeKind(n) === 'experiment',
      n => this._stemKnowledgeKind(n) === 'apparatus'
    ];
    mustHave.forEach(test => {
      if (picked.some(test)) return;
      const hit = ranked.find(x => canAdd(x.n) && test(x.n));
      if (hit) add(hit.n);
    });

    ranked.forEach(x => {
      if (picked.length >= maxCount) return;
      add(x.n);
    });
    return picked.slice(0, maxCount);
  }

  _pickDomainAwareCandidates(scored, maxCount, domains, goal) {
    const relevant = scored.filter(n => this._isMainlineRelevant(n, goal, domains));
    return this._pickStemBalancedCandidates(relevant, maxCount, domains, goal);
  }

  _rebalanceStemMatched(matched, goal, candidatePool, limit) {
    const domains = this._inferProjectDomains(goal);
    if (!domains.length || !this._isStemProjectGoal(goal) || !matched.length) return matched;

    let list = [...matched];
    const maxCalc = Math.max(0, Math.floor(list.length * 0.15));
    const maxLaw = Math.max(1, Math.floor(list.length * 0.25));
    const maxMath = Math.max(1, Math.floor(list.length * 0.22));
    const count = (fn) => list.filter(fn).length;
    const seen = () => new Set(list.map(n => n.id));

    const replaceOne = (predicate) => {
      const idx = list.findIndex(predicate);
      if (idx < 0) return;
      const pool = candidatePool
        .filter(n => !seen().has(n.id))
        .map(n => ({
          ...n,
          _score: this._scoreNodeForGoal(n, this._tokenizeGoalTerms(goal), null, true, domains, goal)
        }));
      const alt = this._pickStemBalancedCandidates(pool, 1, domains, goal)[0];
      if (!alt) return;
      list.splice(idx, 1, alt);
    };

    while (count(n => this._isQuantitativeCalcNode(n)) > maxCalc) {
      replaceOne(n => this._isQuantitativeCalcNode(n));
      if (!candidatePool.length) break;
    }
    while (count(n => this._isConservationLawNode(n)) > maxLaw) {
      replaceOne(n => this._isConservationLawNode(n));
      if (!candidatePool.length) break;
    }
    while (count(n => n.subject === 'math') > maxMath) {
      replaceOne(n => n.subject === 'math');
      if (!candidatePool.length) break;
    }
    ['chemistry', 'info-tech'].forEach(subj => {
      if (list.some(n => n.subject === subj)) return;
      const pool = candidatePool
        .filter(n => !seen().has(n.id) && n.subject === subj)
        .map(n => ({
          ...n,
          _score: this._scoreNodeForGoal(n, this._tokenizeGoalTerms(goal), null, true, domains, goal)
        }));
      const alt = this._pickStemBalancedCandidates(pool, 1, domains, goal)[0];
      if (!alt) return;
      let dropIdx = list.findIndex(n => this._isConservationLawNode(n));
      if (dropIdx < 0) dropIdx = list.findIndex(n => this._isQuantitativeCalcNode(n));
      if (dropIdx < 0 && list.length >= limit) dropIdx = list.length - 1;
      if (dropIdx >= 0) list[dropIdx] = alt;
      else list.push(alt);
    });
    return list.slice(0, limit);
  }

  _pickDiverseCandidates(scored, maxCount, subjects) {
    const sorted = [...scored].sort((a, b) => (b._score || 0) - (a._score || 0));
    const picked = [];
    const seen = new Set();
    const subjList = (subjects || []).filter(Boolean);
    const perSubject = Math.max(4, Math.floor(maxCount / Math.max(subjList.length, 2)));
    subjList.forEach(subj => {
      sorted.filter(n => n.subject === subj).slice(0, perSubject).forEach(n => {
        if (!seen.has(n.id)) { seen.add(n.id); picked.push(n); }
      });
    });
    sorted.forEach(n => {
      if (picked.length >= maxCount) return;
      if (!seen.has(n.id)) { seen.add(n.id); picked.push(n); }
    });
    return picked.slice(0, maxCount);
  }

  _parseMatchIndex(m, candidatesLen) {
    let idx = m.index;
    if (idx == null && m.nodeIndex != null) idx = m.nodeIndex;
    if (typeof idx === 'string' && idx.trim() !== '') idx = parseInt(idx, 10);
    if (!Number.isInteger(idx) || idx < 0 || idx >= candidatesLen) return -1;
    return idx;
  }

  _mapMatchedEntries(result, candidates, complex, minConf, goal = '', archetype = null) {
    const out = [];
    (result.matched || []).forEach(m => {
      if ((m.confidence || 0) < minConf) return;
      const node = this._resolveMatchCandidate(m, candidates);
      if (!node) return;
      if (this._isGenericTransversalNode(node.name, goal)) return;
      if (archetype && this._isArchetypeBanned(node, archetype)) return;
      if (archetype && !this._meetsArchetypeGrade(node, archetype, goal)) return;
      if (!this._isMainlineRelevant(node, goal, this._inferProjectDomains(goal))) return;
      if (!this._isSubjectAllowedForGoal(node, goal, archetype)) return;
      if (complex && this._parseExplicitGradeBand(goal).explicit && this._excludeForComplexProject(node)) return;
      out.push({
        ...node,
        confidence: m.confidence,
        matchReason: m.reason || m.role || '',
        pblRole: m.role || 'core'
      });
    });
    return out;
  }

  _mapExternalEntries(entries) {
    return (entries || [])
      .filter(ext => ext && (ext.name || ext.title))
      .slice(0, PBLPathBuilder.PBL_MAX_EXTERNAL)
      .map((ext, i) => {
        const name = String(ext.name || ext.title || '').trim();
        const reason = String(ext.reason || ext.definition || '课标未单独覆盖，但项目实施必需').trim();
        return {
          id: `ext-${this._hash8(name + i)}`,
          name,
          name_en: '',
          subject: '',
          domain: '',
          grade: 0,
          difficulty: 0,
          definition: reason,
          key_concepts: [],
          prerequisites: [],
          extends: [],
          parallel: [],
          system: 'external',
          systemTag: '💡',
          systemLabel: '课标外补充',
          treePath: '',
          isExternal: true,
          layer: 'external',
          extPrerequisites: ext.prerequisites || [],
          confidence: 0.62,
          matchReason: reason
        };
      });
  }

  /** 按项目类型提供课标外知识点候选池（LLM 未返回时回退） */
  _fallbackExternalPool(goal) {
    if (this._isEnergyAnalysisGoal(goal)) {
      return [
        { name: '光伏发电量估算模型', reason: '面积×转换效率×有效日照时数的简化模型，课本较少系统讲授' },
        { name: '电力碳排放因子', reason: '减排效益测算需查阅区域电网排放因子，课标外常用数据' },
        { name: '投资回收期测算', reason: '收益分析中的简易经济评价方法，超出常规课标深度' },
      ];
    }
    if (this._isChemistryInquiryGoal(goal)) {
      if (this._getChemistryAnalysisProfile(goal).mixed) {
        return [
          { name: '滴定管/移液管读数与润洗规范', reason: '定量滴定操作的器皿使用细节，课标实验较少展开' },
          { name: '硝酸银标准溶液的配制与保存', reason: '沉淀滴定实验的关键试剂准备，需课外实验指导' },
          { name: '电导率仪温度补偿与校准', reason: '电导率法测定须控制温度影响，仪器操作超出课本' },
          { name: '食堂/汤水取样卫生与代表性', reason: '真实样品取样规范，食品安全与数据代表性需额外说明' },
        ];
      }
      return [
        { name: '厨房化学实验安全操作', reason: '加热、称量、取用调味品的安全要点，课标较少单独讲授' },
        { name: '家用电子秤读数与误差', reason: '厨房称量工具的使用与读数规则，实践必需但课标外' },
        { name: '食品包装标签上的钠/盐含量解读', reason: '联系生活情境理解浓度标注，课本通常不展开' },
      ];
    }
    const pools = {
      'consumer-decision': [
        { name: '全生命周期用车成本（TCO）', reason: '课标未系统讲授购车全成本模型，但家庭选车决策必需' },
        { name: '新能源汽车购置补贴与税费政策', reason: '政策直接影响购车成本，需查阅课外政策资料' },
        { name: '车辆保值率与残值评估', reason: '二手残值是选车重要维度，课本通常不涉及' },
      ],
      'engineering': [
        { name: '工程安全与操作规范', reason: '实验/制作环节的安全规程，课标无专项条目但落地必需' },
        { name: '原型测试与故障排查', reason: '工程迭代调试方法超出课本但项目实施必需' },
        { name: '用户需求访谈与场景分析', reason: '以用户为中心的设计方法，课本较少展开' },
      ],
      'scientific-inquiry': [
        { name: '实验伦理与数据真实性', reason: '科学探究中的伦理与记录规范，课标提及较少' },
        { name: '不确定度与误差传播', reason: '测量结果可信度评估，超出常规课标深度' },
        { name: '科学论文式报告结构', reason: '规范撰写探究报告，需课外方法论补充' },
      ],
      'social-inquiry': [
        { name: '问卷信效度检验', reason: '调查工具质量保障，课标较少系统讲授' },
        { name: '访谈伦理与知情同意', reason: '田野调查伦理要求，需课外补充' },
        { name: '数据可视化叙事', reason: '用图表讲故事的技能，超出常规统计课标' },
      ],
      'humanities-literary': [
        { name: '文学批评与互文阅读', reason: '深化文本解读的批评视角，课标外拓展' },
        { name: '朗诵与舞台表现技巧', reason: '口头展示与情感表达，课本较少展开' },
        { name: '版权与引用规范', reason: '创作与发表中的版权意识，需课外补充' },
      ],
      'creative-media': [
        { name: '版式与视觉层次设计', reason: '专业排版原则，课标信息技术较少深入' },
        { name: '受众分析与传播策略', reason: '面向受众的创意传播，课本较少涉及' },
        { name: '数字作品版权与授权', reason: '发布作品时的版权合规，需课外了解' },
      ],
      'business-economics': [
        { name: '市场调研抽样方法', reason: '商业调研中的抽样设计，课标外但实践必需' },
        { name: '盈亏平衡与现金流', reason: '简易商业测算模型，课本通常不单独讲授' },
        { name: '品牌定位与卖点提炼', reason: '营销策划中的定位方法，需课外补充' },
      ],
      'study-trip': [
        { name: '遗址博物馆田野观察记录法', reason: '研学需结构化记录文物史迹观察，课标写作较少专项训练' },
        { name: '目的地自然人文概况调研框架', reason: '研学路线设计需整合区域地理与人文背景，课本分散讲授' },
        { name: '研学行程风险评估表', reason: '研学活动中的风险管理，课标无专项条目' },
      ],
      'life-planning': [
        { name: '行程风险与应急预案', reason: '活动策划中的风险管理，课标无专项条目' },
        { name: '团队协作与分工机制', reason: '项目分工与协作方法，课本较少系统讲授' },
        { name: '时间管理与里程碑', reason: '项目进度管控，课外项目管理常识' },
      ],
      'health-life': [
        { name: '健康行为改变模型', reason: '行为干预的理论框架，超出常规健康课标' },
        { name: '可穿戴设备与健康监测', reason: '数字化健康追踪工具，课本较少涉及' },
        { name: '健康传播与同伴影响', reason: '健康倡议的传播策略，需课外补充' },
      ],
      'labor-practice': [
        { name: '工具安全与操作规范', reason: '劳动实践中的安全要点，需专项课外指导' },
        { name: '过程记录与反思日志', reason: '劳动教育中的反思性记录方法' },
        { name: '成果评价量规（Rubric）', reason: '评价劳动成果的标准化工具，课标外常用' },
      ],
      'general': [
        { name: '跨学科资料检索与引用', reason: '整合多来源信息并规范引用，课标较少系统讲授' },
        { name: '项目迭代与复盘方法', reason: 'PDCA 式改进流程，指导落地但课标外' },
        { name: '成果展示与答辩表达', reason: '公开汇报技巧，PBL 展示必需但课标外' },
      ],
    };
    return pools[this._classifyProjectType(goal)] || pools.general;
  }

  /** 课标外知识点：优先工程注册表按模块绑定，禁止通用套话兜底 */
  _ensureExternalNodes(external, goal, matched, projectBlueprint, archetype = null) {
    const max = this._externalLimit(goal);
    let list = this._mapExternalEntries(external);
    const seen = new Set(list.map(e => String(e.name).toLowerCase()));
    const matchedNames = matched.map(n => n.name);

    const addItem = (item) => {
      if (list.length >= max || !item) return;
      const name = String(item.name || '').trim();
      if (!name || seen.has(name.toLowerCase())) return;
      const mapped = this._mapExternalEntries([{
        name: item.name,
        reason: item.reason || item.definition || '',
        prerequisites: item.prerequisites || [],
        moduleId: item.moduleId,
        taskSnippet: item.taskSnippet,
      }]);
      if (!mapped.length) return;
      const node = mapped[0];
      if (item.moduleId) {
        node.moduleId = item.moduleId;
        node.matchReason = `模块：${item.moduleId}。${item.reason || ''}${item.taskSnippet ? `；任务：${item.taskSnippet}` : ''}`;
      } else if (item._goalTriggered) {
        node.matchReason = `技术节点：${item.reason || ''}${item.taskSnippet ? `；任务：${item.taskSnippet}` : ''}`;
      }
      list.push(node);
      seen.add(name.toLowerCase());
    };

    if (this._archetypeEngine?.getGoalTriggeredExternals) {
      this._archetypeEngine.getGoalTriggeredExternals(goal, matchedNames, max).forEach(addItem);
    }

    if (archetype && this._archetypeEngine) {
      this._archetypeEngine.getRegistryExternals(archetype, projectBlueprint, matchedNames, max)
        .forEach(addItem);
    }

    if (!list.length) {
      this._fallbackExternalPool(goal).forEach(addItem);
    }

    return list.slice(0, max);
  }

  _unionCandidateNodes(lists, maxCount = 50) {
    const out = [];
    const seen = new Set();
    (lists || []).forEach(list => {
      (list || []).forEach(n => {
        if (!n?.id || seen.has(n.id) || out.length >= maxCount) return;
        seen.add(n.id);
        out.push(n);
      });
    });
    return out;
  }

  _retrieveByBlueprintHints(pool, blueprint, archetype, goal, limit = 20) {
    const hints = new Set();
    if (this._archetypeEngine) {
      this._archetypeEngine.blueprintModules(blueprint).forEach(m => (m.hints || []).forEach(h => hints.add(String(h).trim())));
    }
    (archetype?.modules || []).forEach(m => (m.hints || []).forEach(h => hints.add(String(h).trim())));
    (blueprint?.schemes || []).forEach(s => (s.phases || []).forEach(p => (p.knowledgeHints || []).forEach(h => hints.add(String(h).trim()))));
    const hintArr = [...hints].filter(h => h.length >= 2);
    if (!hintArr.length) return [];
    const goalTerms = this._tokenizeGoalTerms(goal);
    return pool
      .map(n => {
        const text = this._nodeSearchText(n);
        const name = String(n.name || '');
        let s = 0;
        hintArr.forEach(h => {
          if (name.includes(h)) s += 10;
          else if (text.includes(h)) s += 5;
        });
        goalTerms.forEach(term => {
          if (term.length >= 2 && (name.includes(term) || text.includes(term))) s += 3;
        });
        return { n, s };
      })
      .filter(x => x.s > 0)
      .sort((a, b) => b.s - a.s)
      .slice(0, limit)
      .map(x => x.n);
  }

  _buildSubjectExemplarSummary(candidates, goal, archetype, perSubject = 4) {
    const goalTerms = this._tokenizeGoalTerms(goal);
    const domains = this._inferProjectDomains(goal);
    const bySubject = {};
    candidates.forEach(n => {
      const subj = n.subject || 'other';
      if (!bySubject[subj]) bySubject[subj] = [];
      bySubject[subj].push({
        n,
        s: this._scoreNodeForGoal(n, goalTerms, null, false, domains, goal),
      });
    });
    return Object.entries(bySubject)
      .map(([subj, arr]) => {
        const names = arr.sort((a, b) => b.s - a.s).slice(0, perSubject).map(x => x.n.name);
        if (!names.length) return '';
        return `${subj}: ${names.join('、')}`;
      })
      .filter(Boolean)
      .join('\n');
  }

  _buildMatchCandidateList(goal, pool, projectBlueprint, archetype, filter, profile, domains, maxCount = 50) {
    const goalTerms = this._tokenizeGoalTerms(goal);
    const scored = pool.map(n => ({
      ...n,
      _score: this._scoreNodeForGoal(n, goalTerms, filter.subjects, profile.complex, domains, goal),
    }));
    const lists = [];

    const hintHits = this._retrieveByBlueprintHints(pool, projectBlueprint, archetype, goal, Math.ceil(maxCount * 0.45));
    if (hintHits.length) lists.push(hintHits);

    if (archetype && this._archetypeEngine) {
      const modulePicks = this._archetypeEngine.pickCandidates(
        scored, archetype, projectBlueprint, Math.ceil(maxCount * 0.55), goalTerms,
        {
          isBanned: n => this._isArchetypeBanned(n, archetype),
          meetsGrade: n => this._meetsArchetypeGrade(n, archetype, goal),
          scoreForModule: (n, m) => this._archetypeEngine.scoreForModule(n, m, goalTerms),
        }
      );
      if (modulePicks.length) lists.push(modulePicks);
    }

    if (domains.length && (profile.complex || this._isConsumerDecisionGoal(goal) || this._isChemistryInquiryGoal(goal))) {
      lists.push(this._pickDomainAwareCandidates(scored, Math.ceil(maxCount * 0.4), domains, goal));
    }

    lists.push([...scored].sort((a, b) => (b._score || 0) - (a._score || 0)).slice(0, maxCount));
    const merged = this._unionCandidateNodes(lists, maxCount);
    if (merged.length >= Math.min(12, maxCount)) return merged;
    return this._unionCandidateNodes([merged, scored.sort((a, b) => (b._score || 0) - (a._score || 0))], maxCount);
  }

  _resolveMatchCandidate(m, candidates) {
    const idx = this._parseMatchIndex(m, candidates.length);
    if (idx >= 0) return candidates[idx];
    const name = String(m.name || m.nodeName || m.knowledgeName || '').trim();
    if (!name) return null;
    const exact = candidates.find(c => c.name === name);
    if (exact) return exact;
    const partial = candidates.find(c => c.name.includes(name) || name.includes(c.name));
    return partial || null;
  }

  /** 提案名与图谱节点的对齐打分 */
  _scoreProposalLink(node, proposal, goal, blueprint, archetype) {
    if (!node || !proposal) return -99;
    const pname = String(proposal.name || '').trim();
    const nname = String(node.name || '').trim();
    let score = this._scoreUniversalRelevance(node, goal, blueprint, null, archetype);
    if (nname === pname) score += 25;
    else if (nname.includes(pname) || pname.includes(nname)) score += 14;
    else {
      const ptokens = pname.split(/[、，,（）()\s]+/).filter(t => t.length >= 2);
      ptokens.forEach(t => {
        if (nname.includes(t)) score += 6;
        else if (this._nodeSearchText(node).includes(t)) score += 2;
      });
    }
    const pSubj = proposal.subject;
    if (pSubj && node.subject === pSubj) score += 5;
    const gHint = parseInt(proposal.gradeHint, 10);
    const gNode = parseInt(node.grade, 10) || 0;
    if (gHint >= 1 && gHint <= 12 && gNode > 0 && Math.abs(gNode - gHint) <= 1) score += 4;
    return score;
  }

  /**
   * 将模型提案的知识点名称对齐到 unifiedIndex / 候选池
   * @returns {{ linked: object[], unlinked: object[] }}
   */
  _linkProposedToGraph(proposals, goal, pool, blueprint, archetype = null) {
    const roles = ['foundation', 'bridge', 'bridge', 'core', 'core', 'core', 'core', 'core'];
    const linked = [];
    const unlinked = [];
    const seen = new Set();
    const searchPool = (pool?.length >= 20 ? pool : null)
      || this._getBroadCurriculumPool(goal, pool || [], 80);
    const minLinkScore = 10;

    (proposals || []).forEach((p, i) => {
      const pname = String(p.name || '').trim();
      if (!pname) return;

      let node = null;
      let linkMethod = '';

      const exact = searchPool.find(c => c.name === pname && this._passesHardNodeGate(c, goal, archetype));
      if (exact) {
        node = exact;
        linkMethod = '精确名匹配';
      }

      if (!node) {
        const partials = searchPool
          .filter(c => this._passesHardNodeGate(c, goal, archetype)
            && (c.name.includes(pname) || pname.includes(c.name)));
        if (partials.length === 1) {
          node = partials[0];
          linkMethod = '子串匹配';
        } else if (partials.length > 1) {
          node = partials
            .map(n => ({ n, s: this._scoreProposalLink(n, p, goal, blueprint, archetype) }))
            .sort((a, b) => b.s - a.s)[0]?.n;
          linkMethod = '子串消歧';
        }
      }

      if (!node) {
        const scored = searchPool
          .filter(n => this._passesHardNodeGate(n, goal, archetype))
          .map(n => ({ n, s: this._scoreProposalLink(n, p, goal, blueprint, archetype) }))
          .filter(x => x.s >= minLinkScore)
          .sort((a, b) => b.s - a.s);
        if (scored.length) {
          node = scored[0].n;
          linkMethod = `语义对齐(${scored[0].s})`;
        }
      }

      if (node && !seen.has(node.id)) {
        seen.add(node.id);
        const role = p.role || roles[linked.length] || 'core';
        linked.push({
          ...node,
          confidence: Math.min(0.94, 0.72 + Math.min(0.2, (parseFloat(p.confidence) || 0.85) * 0.15)),
          matchReason: p.reason ? `提案：${p.reason}` : `知识点提案对齐：${pname}`,
          pblRole: ['foundation', 'bridge', 'core'].includes(role) ? role : 'core',
          _proposedName: pname,
          _linkMethod: linkMethod,
          _proposeIndex: i,
        });
      } else {
        unlinked.push(p);
      }
    });

    return { linked, unlinked };
  }

  async _llmProposeCurriculumStage(goal, projectBlueprint) {
    const profile = this._getPBLGoalProfile(goal);
    const response = await this._callPBLAnalyzeStage('propose-curriculum', {
      goal,
      projectBlueprint,
      projectSpec: this._activeProjectSpec || null,
      deliverable: projectBlueprint?.deliverable || '',
      maxProposed: profile.maxMatched || 14,
      complex: profile.complex,
    });
    const parsed = JSON.parse(this._extractJsonObject(response));
    if (parsed.summary) console.warn('[PBL] propose-curriculum:', parsed.summary);
    return parsed;
  }

  _applyValidateMatchResult(linked, parsed, goal, projectBlueprint, archetype) {
    const removeIdx = new Set(
      (parsed.remove || [])
        .map(r => (typeof r.index === 'number' ? r.index : parseInt(r.index, 10)))
        .filter(i => Number.isInteger(i) && i >= 0 && i < linked.length)
    );
    const roleMap = new Map(
      (parsed.roleUpdates || [])
        .map(r => [typeof r.index === 'number' ? r.index : parseInt(r.index, 10), r.role])
        .filter(([i]) => Number.isInteger(i))
    );

    const indexMap = [];
    const matched = [];
    linked.forEach((n, i) => {
      if (removeIdx.has(i)) return;
      indexMap.push({ oldIdx: i, id: n.id });
      const role = roleMap.get(i) || n.pblRole || 'core';
      matched.push({ ...n, pblRole: role });
    });

    const idByOldIdx = (idx) => {
      const hit = indexMap.find(m => m.oldIdx === idx);
      return hit?.id;
    };

    let pathOrderIds = (parsed.pathOrder || [])
      .map(i => idByOldIdx(typeof i === 'number' ? i : parseInt(i, 10)))
      .filter(id => id && matched.some(m => m.id === id));
    if (!pathOrderIds.length) {
      const byRole = (role) => matched.filter(m => (m.pblRole || 'core') === role).map(m => m.id);
      pathOrderIds = [...byRole('foundation'), ...byRole('bridge'), ...byRole('core')];
    }
    const seenPath = new Set();
    pathOrderIds = pathOrderIds.filter(id => {
      if (seenPath.has(id)) return false;
      seenPath.add(id);
      return true;
    });
    matched.forEach(n => {
      if (!seenPath.has(n.id)) pathOrderIds.push(n.id);
    });

    const dependsOnLinks = [];
    (parsed.dependsOn || []).forEach(d => {
      const src = idByOldIdx(typeof d.source === 'number' ? d.source : parseInt(d.source, 10));
      const tgt = idByOldIdx(typeof d.target === 'number' ? d.target : parseInt(d.target, 10));
      if (src && tgt && src !== tgt) {
        dependsOnLinks.push({ source: src, target: tgt, type: d.type || 'depends-on' });
      }
    });

    const blueprintPhases = this._blueprintProjectPhases(projectBlueprint, goal);
    let projectPhases = (parsed.projectPhases || []).map(p => ({
      phase: p.phase || p.name || '',
      steps: p.steps || [],
      knowledgeNames: this._filterPhaseKnowledgeNames(p.knowledgeNames || [], goal),
      deliverable: p.deliverable || '',
      literacy: p.literacy || {},
    }));
    if (!projectPhases.length && blueprintPhases.length) projectPhases = blueprintPhases;

    const external = this._ensureExternalNodes(
      parsed.external || [], goal, matched, projectBlueprint, archetype
    );

    if (parsed.summary) console.warn('[PBL] validate-match:', parsed.summary);
    if (removeIdx.size) {
      console.warn('[PBL] validate-match 剔除:', [...removeIdx].map(i => linked[i]?.name).filter(Boolean).join('、'));
    }

    return {
      matched,
      external,
      techRoute: (parsed.techRoute || '').trim(),
      knowledgeChain: (parsed.knowledgeChain || '').trim(),
      pathOrderIds,
      dependsOnLinks,
      projectPhases,
      rawMatchResult: parsed,
    };
  }

  async _llmValidateMatchStage(goal, linked, projectBlueprint, bloomProfile, archetype, candidates) {
    const profile = this._getPBLGoalProfile(goal);
    const complex = profile.complex || !!archetype;
    const linkedLite = (linked || []).map((n, index) => ({
      index,
      id: n.id,
      name: n.name,
      subject: n.subject,
      grade: parseInt(n.grade, 10) || 0,
      role: n.pblRole || 'core',
      reason: n.matchReason || '',
      linkMethod: n._linkMethod || '图谱匹配',
    }));

    let parsed = {};
    try {
      const response = await this._callPBLAnalyzeStage('validate-match', {
        goal,
        linked: linkedLite,
        projectBlueprint,
        projectSpec: this._activeProjectSpec || null,
        deliverable: projectBlueprint?.deliverable || '',
        bloomProfile: bloomProfile || this._inferBloomProfile(projectBlueprint),
      });
      parsed = JSON.parse(this._extractJsonObject(response));
    } catch (e) {
      console.warn('[PBL] validate-match 失败，保留提案对齐结果:', e.message);
      parsed = {};
    }

    let stage = this._applyValidateMatchResult(linked, parsed, goal, projectBlueprint, archetype);
    const broadCandidates = this._getBroadCurriculumPool(goal, candidates, 80);
    stage.matched = this._guaranteeCurriculumFloor(
      stage.matched,
      goal,
      broadCandidates,
      archetype,
      profile.maxMatched,
      complex,
      projectBlueprint
    );
    const pruned = this._verifyAndPruneNodes(stage.matched, goal, archetype, '校验后核实').kept;
    if (pruned.length >= this._getMinMatchedFloor(archetype)) {
      stage.matched = pruned;
    }
    stage.matched = this._purgeCurriculumNoise(stage.matched, goal);
    stage.matched = this._rebalanceStemMatched(stage.matched, goal, candidates, profile.maxMatched);
    return stage;
  }

  /** 主路径：提案 → 图谱对齐 → validate-match；不足则回退 index match */
  async _runCurriculumProposeValidatePipeline(goal, candidates, projectBlueprint, bloomProfile, archetype) {
    const minNeed = Math.max(this._getMinMatchedFloor(archetype), archetype?.minMatched || 5);
    const broadPool = this._getBroadCurriculumPool(goal, candidates, 80);

    try {
      const proposed = await this._llmProposeCurriculumStage(goal, projectBlueprint);
      const { linked, unlinked } = this._linkProposedToGraph(
        proposed.proposed || [], goal, broadPool, projectBlueprint, archetype
      );
      if (unlinked.length) {
        console.warn('[PBL] 提案未对齐图谱:', unlinked.map(p => p.name).join('、'));
      }
      if (linked.length >= Math.min(3, minNeed)) {
        console.warn('[PBL] 提案对齐图谱:', linked.map(n => `${n.name}(${n._linkMethod})`).join('、'));
        return this._llmValidateMatchStage(
          goal, linked, projectBlueprint, bloomProfile, archetype, candidates
        );
      }
      console.warn(`[PBL] 提案对齐仅 ${linked.length} 个，回退 index match`);
    } catch (e) {
      console.warn('[PBL] 提案-校验管线失败，回退 index match:', e.message);
    }
    return this._llmMatchStage(goal, candidates, projectBlueprint, bloomProfile, archetype);
  }

  _rescueCandidatesFromPool(goal, candidates, limit, archetype = null, blueprint = null) {
    const goalTerms = this._tokenizeGoalTerms(goal);
    const complex = this._isComplexPBLGoal(goal);
    const domains = this._inferProjectDomains(goal);
    if (archetype && this._archetypeEngine) {
      const pool = candidates.filter(n => {
        if (!this._meetsArchetypeGrade(n, archetype, goal)) return false;
        return this._isMainlineRelevant(n, goal, domains, blueprint, archetype, true);
      });
      const picked = this._archetypeEngine.pickCandidates(
        pool, archetype, blueprint, Math.min(limit, archetype.maxMatched || limit), goalTerms,
        {
          isBanned: n => this._isArchetypeBanned(n, archetype),
          meetsGrade: n => this._meetsArchetypeGrade(n, archetype, goal),
          scoreForModule: (n, m) => this._archetypeEngine.scoreForModule(n, m, goalTerms),
        }
      );
      if (picked.length) {
        return picked.map((n, i) => ({
          ...n,
          confidence: Math.max(0.58, 0.85 - i * 0.04),
          matchReason: n._moduleLabel ? `模块：${n._moduleLabel}。原型层检索匹配` : '原型层模块检索',
          pblRole: i < 1 ? 'foundation' : (i < 3 ? 'bridge' : 'core'),
        }));
      }
    }
    const minScore = archetype ? 3 : (this._isSocialOrCivicInquiryGoal(goal) ? 2 : 4);
    const withScore = candidates
      .filter(n => this._isMainlineRelevant(n, goal, domains))
      .filter(n => !archetype || !this._isArchetypeBanned(n, archetype))
      .map(n => ({
        ...n,
        _score: this._scoreNodeForGoal(n, goalTerms, null, complex, domains, goal)
      }))
      .filter(n => n._score >= minScore);
    const picked = this._pickStemBalancedCandidates(withScore, limit, domains, goal);
    return picked.map((n, i) => ({
      ...n,
      confidence: Math.max(0.55, 0.88 - i * 0.03),
      matchReason: '主线关键词回退匹配',
      pblRole: i < 1 ? 'foundation' : (i < 3 ? 'bridge' : 'core')
    }));
  }

  /** 主线节点不足时，仅按领域得分补齐，不凑跨学科；所有项目类型至少保底 5 个课内节点 */
  _ensureMinimumMatched(matched, goal, candidatePool, limit, complex, archetype = null) {
    const civic = this._isSocialOrCivicInquiryGoal(goal);
    const min = this._getMinMatchedFloor(archetype);
    if (matched.length >= min || !candidatePool.length) {
      return this._assignCoreRoles(matched.slice(0, limit), Math.min(min, matched.length));
    }
    const domains = this._inferProjectDomains(goal);
    const list = [...matched];
    const seen = new Set(list.map(n => n.id));
    const domainMin = (complex || civic) ? (civic ? 2 : 6) : 2;
    const rescued = this._rescueCandidatesFromPool(goal, candidatePool, limit * 2)
      .filter(n => !seen.has(n.id) && !this._excludeForComplexProject(n))
      .filter(n => !domains.length || this._scoreNodeForDomains(n, domains) >= domainMin)
      .sort((a, b) => this._scoreNodeForDomains(b, domains) - this._scoreNodeForDomains(a, domains));
    let roleIdx = 0;
    const roles = ['foundation', 'bridge', 'bridge', 'core', 'core'];
    rescued.forEach(n => {
      if (list.length >= Math.min(min, limit)) return;
      if (seen.has(n.id)) return;
      seen.add(n.id);
      list.push({
        ...n,
        confidence: Math.max(n.confidence || 0.6, 0.62),
        matchReason: n.matchReason || '主线自动补齐',
        pblRole: roles[roleIdx++] || 'core'
      });
    });
    if (list.length < min) {
      this._rescueFromK12KnowledgeGraph(goal, null, archetype, limit, candidatePool).forEach(n => {
        if (list.length >= min || seen.has(n.id)) return;
        seen.add(n.id);
        list.push(n);
      });
    }
    return this._assignCoreRoles(list.slice(0, limit), min);
  }

  _resolvePrerequisiteNames(node) {
    return (node.prerequisites || []).map(pid => {
      const pre = this.unifiedIndex.get(pid);
      return pre?.name || pid;
    }).filter(Boolean);
  }

  _enrichCandidateForMatch(node) {
    return {
      name: node.name,
      grade: node.grade,
      gradeLabel: node.gradeLabel,
      subject: node.subject,
      systemTag: node.systemTag,
      definition: node.definition || (node.curriculum_points || []).join(' ').slice(0, 120),
      prerequisiteNames: this._resolvePrerequisiteNames(node),
    };
  }

  _inferBloomProfile(projectBlueprint) {
    if (typeof PBLBloom !== 'undefined' && PBLBloom.inferBloomFromBlueprint) {
      return PBLBloom.inferBloomFromBlueprint(projectBlueprint);
    }
    return { ceiling: 3, ceilingLabel: 'apply', evidence: [], actionVerbs: [] };
  }

  _isNodeAboveBloomCeiling(node, ceiling) {
    if (typeof PBLBloom !== 'undefined' && PBLBloom.isNodeAboveBloomCeiling) {
      return PBLBloom.isNodeAboveBloomCeiling(node, ceiling);
    }
    return false;
  }

  _mergeBloomProfile(ruleBloom, llmFilter) {
    const ceiling = Math.min(
      ruleBloom?.ceiling || 6,
      parseInt(llmFilter?.bloomCeiling, 10) || ruleBloom?.ceiling || 6
    );
    return {
      ceiling,
      ceilingLabel: ruleBloom?.ceilingLabel || 'apply',
      evidence: [...(ruleBloom?.evidence || []), ...(llmFilter?.bloomEvidence || [])].slice(0, 4),
      actionVerbs: [...new Set([...(ruleBloom?.actionVerbs || []), ...(llmFilter?.actionVerbs || [])])].slice(0, 8),
    };
  }

  _ruleCheckDepEdge(source, target) {
    const srcRole = source.role || source.pblRole || '';
    const tgtRole = target.role || target.pblRole || '';
    if (source.index === target.index) return 'invalid';
    if (tgtRole === 'foundation' && (srcRole === 'core' || srcRole === 'bridge')) return 'reversed';
    if (srcRole === 'core' && tgtRole === 'foundation') return 'invalid';
    const tgtOfficial = target.officialPrereqs || [];
    const srcOfficial = source.officialPrereqs || [];
    if (tgtOfficial.includes(source.name)) return 'valid';
    if (srcOfficial.includes(target.name)) return 'reversed';
    return null;
  }

  _buildDepEdgesForVerify(matchResult, candidates, matched) {
    const idToMatched = new Map();
    matched.forEach((n, i) => idToMatched.set(n.id, { ...n, matchIndex: i }));
    const indexToCandidate = new Map(candidates.map((n, i) => [i, n]));
    const edges = [];
    (matchResult.matched || []).forEach(m => {
      const tgtIdx = this._parseMatchIndex(m, candidates.length);
      if (tgtIdx < 0) return;
      const tgtNode = candidates[tgtIdx];
      const tgtMatched = idToMatched.get(tgtNode.id);
      if (!tgtMatched) return;
      (m.dependsOn || []).forEach(dep => {
        const srcIdx = typeof dep === 'string' ? parseInt(dep, 10) : dep;
        if (!Number.isInteger(srcIdx) || srcIdx < 0 || srcIdx >= candidates.length) return;
        const srcNode = indexToCandidate.get(srcIdx);
        if (!srcNode) return;
        const edgeId = `e${srcIdx}-${tgtIdx}`;
        const srcMatched = matched.find(x => x.id === srcNode.id);
        edges.push({
          id: edgeId,
          sourceIndex: srcIdx,
          targetIndex: tgtIdx,
          sourceName: srcNode.name,
          sourceRole: srcMatched?.pblRole || 'node',
          targetName: tgtNode.name,
          targetRole: m.role || tgtMatched.pblRole || 'node',
          officialPrereqs: this._resolvePrerequisiteNames(tgtNode),
          sourceOfficialPrereqs: this._resolvePrerequisiteNames(srcNode),
        });
      });
    });
    return edges;
  }

  _applyDepVerification(matchResult, verification, candidates) {
    const verdictMap = new Map((verification?.edges || []).map(e => [e.id, e]));
    const patched = (matchResult.matched || []).map(m => ({
      ...m,
      dependsOn: [...(m.dependsOn || [])],
    }));
    patched.forEach(m => {
      const tgtIdx = this._parseMatchIndex(m, candidates.length);
      if (tgtIdx < 0) return;
      const kept = [];
      (m.dependsOn || []).forEach(dep => {
        const srcIdx = typeof dep === 'string' ? parseInt(dep, 10) : dep;
        if (!Number.isInteger(srcIdx)) return;
        const edgeId = `e${srcIdx}-${tgtIdx}`;
        const v = verdictMap.get(edgeId);
        if (!v || v.verdict === 'valid') {
          kept.push(srcIdx);
        } else if (v.verdict === 'reversed') {
          const srcMatch = patched.find(x => this._parseMatchIndex(x, candidates.length) === srcIdx);
          if (srcMatch && !srcMatch.dependsOn.includes(tgtIdx)) {
            srcMatch.dependsOn.push(tgtIdx);
          }
        }
      });
      m.dependsOn = [...new Set(kept)];
    });
    return { ...matchResult, matched: patched };
  }

  _applyRelevanceVerification(stage2, candidates, removeList = []) {
    if (!removeList.length || !stage2?.matched?.length) return stage2;
    const removeIdx = new Set(
      removeList
        .map(r => (typeof r.index === 'number' ? r.index : parseInt(r.index, 10)))
        .filter(i => Number.isInteger(i) && i >= 0)
    );
    if (!removeIdx.size) return stage2;

    const keptMatched = stage2.matched.filter(n => {
      const idx = candidates.findIndex(c => c.id === n.id);
      return idx < 0 || !removeIdx.has(idx);
    });
    const keptIds = new Set(keptMatched.map(n => n.id));
    const raw = stage2.rawMatchResult || {};
    const patchedMatched = (raw.matched || []).filter(m => {
      const idx = this._parseMatchIndex(m, candidates.length);
      return idx >= 0 && !removeIdx.has(idx);
    });
    const pathOrderIds = (stage2.pathOrderIds || []).filter(id => keptIds.has(id));
    console.warn('[PBL] verify-relevance 剔除:', removeList.map(r => r.reason || r.index).join('；'));
    return {
      ...stage2,
      matched: keptMatched,
      pathOrderIds,
      rawMatchResult: { ...raw, matched: patchedMatched },
    };
  }

  async _llmVerifyRelevanceStage(goal, stage2, candidates, archetype = null, projectBlueprint = null) {
    if (!stage2?.matched?.length) return stage2;

    const matchedLite = stage2.matched.map(n => {
      const idx = candidates.findIndex(c => c.id === n.id);
      return {
        index: idx,
        name: n.name,
        subject: n.subject,
        grade: parseInt(n.grade, 10) || 0,
        reason: n.matchReason || '',
        role: n.pblRole || 'core',
      };
    }).filter(n => n.index >= 0);

    const ruleRemoveIdx = new Set();
    matchedLite.forEach(n => {
      const node = candidates[n.index];
      if (!node || this._passesHardNodeGate(node, goal, archetype)) return;
      ruleRemoveIdx.add(n.index);
    });

    let llmRemove = [];
    try {
      const response = await this._callPBLAnalyzeStage('verify-relevance', {
        goal,
        deliverable: projectBlueprint?.deliverable || '',
        projectBlueprint,
        matched: matchedLite,
      });
      const jsonStr = this._extractJsonObject(response);
      const parsed = JSON.parse(jsonStr);
      llmRemove = (parsed.remove || []).map(r => ({
        index: typeof r.index === 'number' ? r.index : parseInt(r.index, 10),
        reason: r.reason || 'LLM审核剔除',
      })).filter(r => Number.isInteger(r.index) && r.index >= 0);
      if (parsed.summary) console.warn('[PBL] verify-relevance:', parsed.summary);
    } catch (e) {
      console.warn('[PBL] verify-relevance 失败，仅使用硬门禁:', e.message);
    }

    const merged = new Map();
    [...ruleRemoveIdx].forEach(idx => merged.set(idx, { index: idx, reason: '硬门禁' }));
    llmRemove.forEach(r => merged.set(r.index, r));
    return this._applyRelevanceVerification(stage2, candidates, [...merged.values()]);
  }

  async _llmReviewCurriculumStage(goal, nodes, projectBlueprint, archetype = null) {
    const curriculum = (nodes || []).filter(n => n && n.layer !== 'external' && !n.isExternal);
    if (!curriculum.length) return { nodes: nodes || [], removed: [], summary: '' };

    const lite = curriculum.map((n, i) => ({
      index: i,
      id: n.id,
      name: n.name,
      subject: n.subject,
      grade: parseInt(n.grade, 10) || 0,
      layer: n.layer || 'matched',
      reason: n.matchReason || '',
      definition: (n.definition || '').slice(0, 100),
    }));

    let removeIdx = new Set();
    let summary = '';
    try {
      const response = await this._callPBLAnalyzeStage('review-curriculum', {
        goal,
        deliverable: projectBlueprint?.deliverable || '',
        projectBlueprint,
        projectSpec: this._activeProjectSpec || null,
        nodes: lite,
      });
      const parsed = JSON.parse(this._extractJsonObject(response));
      (parsed.remove || []).forEach(r => {
        const idx = typeof r.index === 'number' ? r.index : parseInt(r.index, 10);
        if (Number.isInteger(idx) && idx >= 0 && idx < lite.length) removeIdx.add(idx);
      });
      summary = parsed.summary || '';
      if (summary) console.warn('[PBL] review-curriculum:', summary);
    } catch (e) {
      console.warn('[PBL] review-curriculum 失败，保留规则分过滤结果:', e.message);
      return { nodes, removed: [], summary: '' };
    }

    const removeIds = new Set([...removeIdx].map(i => lite[i]?.id).filter(Boolean));
    const removed = lite.filter((n, i) => removeIdx.has(i));
    const kept = (nodes || []).filter(n => !removeIds.has(n.id));
    if (removed.length) {
      console.warn('[PBL] LLM 二次检讨剔除:', removed.map(r => `${r.name}(${r.reason || '无关节点'})`).join('、'));
    }
    return { nodes: kept, removed, summary };
  }

  async _llmVerifyDepsStage(goal, matchResult, candidates, matched) {
    const edges = this._buildDepEdgesForVerify(matchResult, candidates, matched);
    if (!edges.length) return matchResult;

    const ruleResolved = edges.map(e => {
      const rule = this._ruleCheckDepEdge(
        { name: e.sourceName, role: e.sourceRole, index: e.sourceIndex, officialPrereqs: e.sourceOfficialPrereqs },
        { name: e.targetName, role: e.targetRole, index: e.targetIndex, officialPrereqs: e.officialPrereqs }
      );
      return { ...e, ruleVerdict: rule };
    });
    const needLlm = ruleResolved.filter(e => !e.ruleVerdict);
    let llmVerdicts = { edges: [] };

    if (needLlm.length) {
      try {
        const response = await this._callPBLAnalyzeStage('verify-deps', {
          goal,
          edges: needLlm.map(({ id, sourceName, sourceRole, targetName, targetRole, officialPrereqs }) => ({
            id, sourceName, sourceRole, targetName, targetRole, officialPrereqs,
          })),
        });
        const jsonStr = this._extractJsonObject(response);
        llmVerdicts = JSON.parse(jsonStr);
      } catch (e) {
        console.warn('[PBL] verify-deps 失败，保留规则校验结果:', e.message);
      }
    }

    const allVerdicts = [
      ...ruleResolved.filter(e => e.ruleVerdict).map(e => ({
        id: e.id, verdict: e.ruleVerdict, reason: '规则校验',
      })),
      ...(llmVerdicts.edges || []),
    ];
    return this._applyDepVerification(matchResult, { edges: allVerdicts }, candidates);
  }

  _buildDependsOnLinks(result, candidates) {
    const links = [];
    (result.matched || []).forEach(m => {
      const tgtIdx = this._parseMatchIndex(m, candidates.length);
      if (tgtIdx < 0) return;
      const tgtId = candidates[tgtIdx].id;
      (m.dependsOn || []).forEach(dep => {
        let srcIdx = typeof dep === 'string' ? parseInt(dep, 10) : dep;
        if (!Number.isInteger(srcIdx) || srcIdx < 0 || srcIdx >= candidates.length) return;
        links.push({ source: candidates[srcIdx].id, target: tgtId, type: 'prerequisite' });
      });
    });
    return links;
  }

  _applyPathOrderToGraph(graphData, matchedNodes, pathOrderIds = []) {
    const nodeMap = new Map(graphData.nodes.map(n => [n.id, n]));
    const byId = new Map(matchedNodes.map(n => [n.id, n]));
    const ordered = [];
    (pathOrderIds || []).forEach(id => {
      if (byId.has(id) && !ordered.find(o => o.id === id)) ordered.push(byId.get(id));
    });
    matchedNodes.forEach(n => {
      if (!ordered.find(o => o.id === n.id)) ordered.push(n);
    });
    ordered.forEach((n, idx) => {
      const gNode = nodeMap.get(n.id);
      if (gNode) gNode.pathStep = idx + 1;
    });
    const links = [...graphData.links];
    for (let i = 0; i < ordered.length - 1; i++) {
      const a = ordered[i].id;
      const b = ordered[i + 1].id;
      if (nodeMap.has(a) && nodeMap.has(b)) {
        links.push({ source: a, target: b, type: 'path-step' });
      }
    }
    return { nodes: graphData.nodes, links: this._deduplicateLinks(links) };
  }

  static PATH_STEP_CIRCLED = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩', '⑪', '⑫'];

  _pathStepCircled(step) {
    const i = (step || 1) - 1;
    return PBLPathBuilder.PATH_STEP_CIRCLED[i] || String(step);
  }

  /** 图谱主线：带 pathStep 的实施节点（绿/紫/红均算） */
  _getMainlinePath(graphData) {
    return (graphData?.nodes || [])
      .filter(n => n.pathStep)
      .sort((a, b) => a.pathStep - b.pathStep);
  }

  _inferNodeRole(n) {
    if (n.pblRole) return n.pblRole;
    if (n.layer === 'prerequisite') return 'foundation';
    if (n.layer === 'advanced') return 'bridge';
    return 'core';
  }

  _rolePhaseTitle(role, corePart, coreTotal) {
    const map = { foundation: '基础准备', bridge: '原理探究', core: '动手实现' };
    if (role === 'core' && coreTotal > 1) return `动手实现（${corePart === 1 ? '上' : '下'}）`;
    return map[role] || '实施阶段';
  }

  _defaultDeliverable(role, goal = '') {
    if (this._isEnergyAnalysisGoal(goal)) {
      return ({
        foundation: '日照/辐射调查记录表 + 太阳能发电原理笔记',
        bridge: '用电量统计表 + 屋顶面积测算示意图',
        core: '年发电量收益测算表 + 碳减排分析图表 + 方案论证报告',
      })[role] || '光伏发电测算阶段成果';
    }
    if (this._isChemistryInquiryGoal(goal)) {
      const cap = this._getChemistryAnalysisProfile(goal);
      if (cap.mixed) {
        return ({
          foundation: '混合溶液测定约束分析 / 滴定法与电导率法方案比选表',
          bridge: '取样预处理方案 + 硝酸银滴定或电导率标定实验记录表',
          core: '浓度换算结果、平行测定误差分析与结论报告'
        })[role] || '间接测定阶段成果';
      }
      return ({
        foundation: '溶液与浓度概念图 / 公式推导笔记',
        bridge: '厨房食盐溶液探究实验方案与记录表',
        core: '浓度计算结果、对比分析与生活应用小结'
      })[role] || '化学探究阶段成果';
    }
    return ({
      foundation: '概念图 / 知识准备笔记',
      bridge: '原理分析报告或验证实验方案',
      core: '可运行原型、测试数据或阶段作品'
    })[role] || '阶段成果物';
  }

  _suggestPhaseSteps(goal, group, blueprintPhase = null) {
    if (blueprintPhase?.steps?.length && !this._areHollowSteps(blueprintPhase.steps)) {
      return blueprintPhase.steps.slice(0, 4);
    }
    const nodes = group.nodes || [];
    const kn = nodes.map(n => n.name).filter(Boolean);
    const knRef = kn.map(n => `「${n}」`).join('、') || '本阶段课标知识点';
    const shortGoal = String(goal || '').slice(0, 48);
    const role = group.role || 'core';
    const type = this._classifyProjectType(goal);
    const mk = arr => arr.slice(0, 4);

    if (type === 'social-inquiry') {
      const map = {
        foundation: [
          `围绕「${shortGoal}」写出 1 句可验证的调查问题，确定调查对象与样本量（如本班抽样 20 人）`,
          `设计 8–10 题问卷或访谈提纲（3 道选择题 + 2 道开放题），注明发放渠道与回收截止日`,
        ],
        bridge: [
          `回收问卷并整理为统计表，标注缺失值与 2 份异常答卷的处理方式`,
          `用 ${knRef} 绘制至少 2 种统计图，写出 3 条基于数据的发现（附图表编号）`,
        ],
        core: [
          `归纳 2–3 条结论，每条对应 1 张图表或 1 组原始数据`,
          `撰写 800 字调查报告（摘要/方法/发现/建议），准备 3 分钟答辩要点清单`,
        ],
      };
      return mk(map[role] || map.core);
    }
    if (type === 'humanities-literary') {
      const map = {
        foundation: [
          `确定作品主题与读者对象，列出 3 篇参考文本并各写 50 字摘抄+批注`,
          `用 ${knRef} 完成立意提纲：中心句、3 个分论点、2 个生活/阅读例证`,
        ],
        bridge: [
          `完成初稿（不少于 600 字或 12 节诗），标注待改的段落编号`,
          `按结构/语言/修辞三项自评表修改 1 轮，记录修改前后对照`,
        ],
        core: [
          `定稿并排版（标题、作者、目录/分节），附 200 字创作说明`,
          `准备朗诵/展示稿与 2 个听众可能提问的回答要点`,
        ],
      };
      return mk(map[role] || map.core);
    }
    if (type === 'consumer-decision') {
      const map = {
        foundation: [
          `列出家庭用车 5 条真实需求（预算、里程、充电/加油便利性等），制成需求优先级表`,
          `确定 3 个对比维度（5 年总成本、使用场景、环保排放），用 ${knRef} 说明各维度数据来源`,
        ],
        bridge: [
          `收集 2 款候选车型参数，制作 5 年用车成本测算表（购置+能耗+保养）`,
          `用统计图对比两车在目标场景下的关键指标，标注假设条件`,
        ],
        core: [
          `撰写决策报告：推荐车型 + 3 条证据 + 1 条风险与备选方案`,
          `制作 1 页对比海报或答辩幻灯（含图表与结论句）`,
        ],
      };
      return mk(map[role] || map.core);
    }
    if (type === 'business-economics') {
      const map = {
        foundation: [
          `描述目标用户与 3 个痛点，完成 10 人迷你访谈或问卷并汇总`,
          `用 ${knRef} 列出产品/服务核心功能与竞品差异表`,
        ],
        bridge: [
          `制作成本表（材料/人工/推广），用百分比或函数估算盈亏平衡点`,
          `设计 1 页商业计划摘要：定价、渠道、首月运营动作`,
        ],
        core: [
          `模拟运营 1 周并记录收支，更新测算表与改进点`,
          `撰写复盘报告：数据、问题、下一步 3 条行动`,
        ],
      };
      return mk(map[role] || map.core);
    }
    if (type === 'study-trip') {
      const map = {
        foundation: [
          `调研目的地区域地理：地形气候、交通区位，整理 1 页概况表`,
          `查阅 ${knRef} 相关人文史迹资料，列出 3 处必访点及史料线索`,
        ],
        bridge: [
          `绘制研学路线图与日程表，标注各站点史地学习任务`,
          `测算交通食宿门票等费用，制作预算表与安全预案检查表`,
        ],
        core: [
          `按路线完成田野观察记录（史迹+地理现象各≥3条）`,
          `撰写研学报告：区域地理发现、人文史迹收获、费用决算与改进建议`,
        ],
      };
      return mk(map[role] || map.core);
    }
    if (type === 'life-planning') {
      const map = {
        foundation: [
          `明确活动目标、参与人数、日期与场地约束，写成 1 页需求说明`,
          `用 ${knRef} 列出任务分工表（角色/负责人/截止日）`,
        ],
        bridge: [
          `制作日程甘特图或流程表，含物料清单与预算明细`,
          `完成关键物料准备（通知、路线、安全预案）并勾选检查表`,
        ],
        core: [
          `按方案执行并拍照/签到记录，当天填写执行日志`,
          `撰写 500 字总结：亮点、问题、费用决算与改进建议`,
        ],
      };
      return mk(map[role] || map.core);
    }
    if (type === 'creative-media') {
      const map = {
        foundation: [
          `确定作品主题、受众与风格参考（2 个范例），写 100 字创意简报`,
          `用 ${knRef} 完成分镜/草图 3 帧，标注尺寸与配色方案`,
        ],
        bridge: [
          `制作半成品并收集 3 人反馈，记录修改清单`,
          `按反馈迭代 1 轮，导出可展示版本（图片/视频/海报）`,
        ],
        core: [
          `完成终稿并附制作说明（工具、素材来源、时长/尺寸）`,
          `布置展示位或线上发布，准备 1 分钟作品介绍词`,
        ],
      };
      return mk(map[role] || map.core);
    }
    if (type === 'energy-analysis' || this._isEnergyAnalysisGoal(goal)) {
      const phase = String(blueprintPhase?.phase || group.phase || '');
      if (/资源|日照|太阳能|辐射/.test(phase)) return mk([
        `查阅本地日照/辐射资料，整理校园≥7日有效日照时数记录表（标注数据来源）`,
        `结合 ${knRef} 说明光能→电能转化原理，列出屋顶可用面积与遮挡因素`,
      ]);
      if (/用电|屋顶|调查/.test(phase)) return mk([
        `统计校园近3个月用电量，制成月度用电折线图`,
        `测量或估算教学楼屋顶可用铺设面积，绘制平面示意图并标注朝向`,
      ]);
      if (/收益|测算|计算|函数/.test(phase)) return mk([
        `建立年发电量估算模型（面积×转换效率×日照时数），用 ${knRef} 完成计算表`,
        `估算年发电收益与电费节约（含电价、补贴假设），计算投资回收期简表`,
      ]);
      if (/减排|碳|环境|效益/.test(phase)) return mk([
        `查阅电力碳排放因子，计算年减排量并与校园用电碳足迹对比`,
        `制作减排效益对比图表，写出2条环境效益结论`,
      ]);
      if (/论证|报告|方案/.test(phase)) return mk([
        `撰写光伏发电方案论证报告（现状-测算-收益-减排-建议，≥600字）`,
        `准备3分钟答辩要点：关键数据表、图表编号与3条可行性论证`,
      ]);
      const map = {
        foundation: [
          `查阅日照资料并整理校园7日日照/辐射记录表，标注数据来源`,
          `结合 ${knRef} 说明太阳能发电基本原理与光电转化效率影响因素`,
        ],
        bridge: [
          `统计校园月用电量并绘制折线图，测算屋顶可用面积（附平面示意图）`,
          `建立年发电量估算模型，完成发电量与收益测算表（列明假设条件）`,
        ],
        core: [
          `计算碳减排效益并与用电碳足迹对比，制作分析图表`,
          `撰写光伏发电方案论证报告并准备答辩要点清单`,
        ],
      };
      return mk(map[role] || map.core);
    }
    if (type === 'engineering') {
      if (/算力中心|数据中心|太空算力|云计算|边缘计算|计算中心|服务器集群|卫星计算|轨道计算/.test(String(goal || ''))) {
        const phase = String(blueprintPhase?.phase || group.phase || '');
        if (/需求|约束|原理/.test(phase)) return mk([
          '梳理太空算力中心的 3 类任务负载（推理、遥感处理、链路缓存），形成需求矩阵',
          '列出轨道环境、功耗、散热、通信时延、辐射防护 5 类约束并标注数据来源',
        ]);
        if (/架构|结构|方案|装置|设计/.test(phase)) return mk([
          '绘制太空算力中心系统架构图，标注计算节点、电源、热控、通信与冗余链路',
          '完成 2 套架构方案对比表，按功耗、重量、带宽、可靠性四项指标打分',
        ]);
        if (/控制|实现|调度|运行/.test(phase)) return mk([
          '设计任务调度与遥测控制流程图，明确数据上行、计算处理、结果下传三个接口',
          '编写故障切换策略说明，覆盖过热、链路中断、节点失效三种异常场景',
        ]);
        if (/测试|迭代|验证|验收/.test(phase)) return mk([
          '用指标表验证延迟、带宽、能耗、热冗余四项性能，记录至少 2 轮方案调整',
          '整理太空算力中心工程实施方案，附风险清单、测试结论与下一轮迭代建议',
        ]);
      }
      const map = {
        foundation: [
          `画出系统框图，标注输入/输出/关键部件、电源与信号走向`,
          `用 ${knRef} 列出器材清单（型号/数量）、安全注意事项与 3 项测试指标`,
        ],
        bridge: [
          `完成核心模块接线/结构组装，通电前填写线路复查表并签字`,
          `首次功能测试记录日志（时间/现象/故障点），修改 1 处并附对比照片`,
        ],
        core: [
          `稳定性测试 ≥3 次，记录成功率与误差，计算平均值`,
          `撰写工程报告：原理、结构、测试数据表、改进计划（各 1 页）`,
        ],
      };
      return mk(map[role] || map.core);
    }
    if (type === 'general') {
      const map = {
        foundation: [
          `收集「${shortGoal}」相关 3 条背景资料（各 50 字摘要+来源）`,
          `用 ${knRef} 明确 1 个可检查交付物与 3 条验收标准（谁检查、看什么）`,
        ],
        bridge: [
          `绘制实施流程图：步骤、负责人、工具、中间产出文件`,
          `完成 1 次小范围试做/预调查，记录问题清单与修订计划`,
        ],
        core: [
          `执行「${shortGoal}」核心方案，按阶段记录关键数据、过程证据与版本变化`,
          `整理「${shortGoal}」最终成果包，对照验收标准写出自评结论与改进清单`,
        ],
      };
      return mk(map[role] || map.core);
    }
    if (this._isChemistryInquiryGoal(goal)) {
      const cap = this._getChemistryAnalysisProfile(goal);
      if (cap.mixed) {
        const sample = cap.sampleLabel;
        const byRole = {
          foundation: [
            `说明${sample}为何属于混合溶液、无法直接称量分离溶质，比较硝酸银滴定法与电导率法的适用条件`,
            `结合 ${knRef} 理解：沉淀滴定（Ag⁺+Cl⁻→AgCl↓）或电解质导电与离子浓度的关系`,
          ],
          bridge: [
            `设计${sample}取样与预处理（澄清、定容稀释、平行样）方案`,
            cap.methods.includes('titration')
              ? '准备滴定装置：硝酸银标准溶液、滴定管/移液管，确定终点判断方式并设计记录表'
              : '配制系列标准盐溶液，测定电导率并绘制标准曲线',
          ],
          core: [
            cap.methods.includes('titration')
              ? '实施硝酸银滴定，记录消耗体积，换算样品中 Cl⁻/NaCl 含量'
              : '测定样品电导率并由标准曲线读出等效浓度',
            '进行平行测定，计算平均值与相对误差，与另一方法或参考标准对比讨论',
          ],
        };
        return (byRole[group.role] || [`围绕 ${knRef} 完成${sample}间接测定与数据分析`]).slice(0, 3);
      }
      const byRole = {
        foundation: [
          `用 ${knRef} 解释：食盐溶于水时溶质、溶剂、溶液分别是什么`,
          '写出溶质质量分数公式，并举例说明厨房场景下可测量的量',
        ],
        bridge: [
          '设计厨房食盐溶液浓度测定或配制实验：明确变量、对照与数据记录表',
          `结合 ${kn[0] || '溶液'} 列出实验步骤、器材与安全注意事项`,
        ],
        core: [
          '按方案称量、溶解并记录溶质质量与溶液质量（或体积）',
          '计算质量分数，与包装标签或经验浓度对比并分析误差原因',
        ],
      };
      return (byRole[group.role] || [`围绕 ${knRef} 完成探究记录与数据分析`]).slice(0, 3);
    }
    return null;
  }

  _groupMainlineIntoPhases(mainline) {
    if (!mainline?.length) return [];
    const blocks = [];
    let cur = { role: null, nodes: [] };
    mainline.forEach(n => {
      const role = this._inferNodeRole(n);
      if (cur.role && role !== cur.role && cur.nodes.length) {
        blocks.push({ ...cur });
        cur = { role, nodes: [n] };
      } else {
        if (!cur.role) cur.role = role;
        cur.nodes.push(n);
      }
    });
    if (cur.nodes.length) blocks.push(cur);

    const expanded = [];
    blocks.forEach(b => {
      if (b.role === 'core' && b.nodes.length > 3) {
        const mid = Math.ceil(b.nodes.length / 2);
        expanded.push({ role: 'core', nodes: b.nodes.slice(0, mid), part: 1 });
        expanded.push({ role: 'core', nodes: b.nodes.slice(mid), part: 2 });
      } else {
        expanded.push(b);
      }
    });
    while (expanded.length > 5 && expanded.length > 1) {
      const tail = expanded.pop();
      expanded[expanded.length - 1].nodes.push(...tail.nodes);
    }

    const coreBlocks = expanded.filter(b => b.role === 'core');
    let coreSeen = 0;
    return expanded.map((b, i) => {
      if (b.role === 'core') coreSeen += 1;
      return {
        phaseIndex: i + 1,
        role: b.role,
        phase: b.part
          ? this._rolePhaseTitle('core', b.part, coreBlocks.length)
          : this._rolePhaseTitle(b.role, coreSeen, coreBlocks.length),
        nodes: b.nodes,
        pathSteps: b.nodes.map(n => n.pathStep),
        knowledgeNames: b.nodes.map(n => n.name),
        nodeIds: b.nodes.map(n => n.id)
      };
    });
  }

  _literacyFromLlmPhase(p) {
    if (!p) return {};
    if (p.literacy) return p.literacy;
    return {
      knowledge: p.knowledgeLiteracy || p.knowledge || '',
      method: p.methodLiteracy || p.method || '',
      ability: p.abilityLiteracy || p.ability || '',
      attitude: p.attitudeLiteracy || p.attitude || '',
      emotion: p.emotionLiteracy || p.emotion || '',
      values: p.valuesLiteracy || p.values || ''
    };
  }

  _hasPolPsychSubjectSpec() {
    const specSubjects = this._subjectFilterFromProjectSpec(this._activeProjectSpec) || [];
    return specSubjects.includes('politics') || specSubjects.includes('psychology');
  }

  /** 道法/心理学科：在 literacy.ability 层补充社交、合作、说服等高层能力 */
  _supplementPolPsychLiteracy(literacy = {}, ctx = {}) {
    const specSubjects = this._subjectFilterFromProjectSpec(this._activeProjectSpec) || [];
    const hasPol = specSubjects.includes('politics');
    const hasPsych = specSubjects.includes('psychology');
    if (!hasPol && !hasPsych) return literacy || {};

    const lit = { ...(literacy || {}) };
    const role = ctx.role || 'core';
    const supplements = {
      foundation: hasPol && hasPsych
        ? '能倾听他人观点并初步协商分工，觉察自身与他人情绪'
        : (hasPol
          ? '能倾听并尊重不同意见，初步理解他人立场与社会规则'
          : '能觉察自身与他人情绪，建立基本信任与沟通关系'),
      bridge: hasPol && hasPsych
        ? '能与同伴协作完成任务，运用协商沟通化解分歧'
        : (hasPol
          ? '能在团队中分工协作，运用理性论证表达观点'
          : '能与同伴合作探究，运用共情与倾听技巧理解他人'),
      core: hasPol && hasPsych
        ? '能组织小组讨论，运用说服与论证策略推动共识并形成行动倡议'
        : (hasPol
          ? '能撰写倡议或演讲稿，运用说服性表达影响他人'
          : '能开展同伴访谈或小组辅导，运用沟通与引导技巧提供支持'),
    };
    const extra = supplements[role] || supplements.core;
    const existing = String(lit.ability || '').trim();
    if (!existing || PBLPathBuilder.GENERIC_TRANSVERSAL_RE.test(existing)) {
      lit.ability = extra;
    } else if (!/社交|合作|说服|协商|共情|倾听|沟通|团队|协作|影响|讨论/.test(existing)) {
      lit.ability = `${existing}；${extra}`;
    }
    return lit;
  }

  _formatPhaseLiteracy(p) {
    if (!p) return '';
    const lit = p.literacy;
    if (!lit || typeof lit !== 'object') return '';
    const dims = [
      ['知识', lit.knowledge],
      ['方法', lit.method],
      ['能力', lit.ability],
      ['态度', lit.attitude],
      ['情感', lit.emotion],
      ['价值观', lit.values],
    ];
    return dims
      .filter(([, v]) => v && String(v).trim())
      .map(([k, v]) => `${k}：${String(v).trim()}`)
      .join('；');
  }

  /**
   * 路径拆解模式：以图谱 pathStep 为主线，合并 LLM 阶段任务/素养/产出
   */
  _buildPathPlan({ goal, graphData, projectPhases = [], knowledgeChain = '', external = [], blueprintPhases = [] }) {
    const mainline = this._getMainlinePath(graphData);
    const groups = this._groupMainlineIntoPhases(mainline);
    const llm = projectPhases || [];
    const domains = this._inferProjectDomains(goal);
    const archetype = this._resolvedArchetype || null;
    const phases = groups.map((g, i) => {
      const lp = llm[i] || {};
      const bp = blueprintPhases[i] || {};
      const keptNodes = (g.nodes || []).filter(n => !this._getNodeIrrelevanceReason(n, goal, domains, archetype));
      const contextual = this._suggestPhaseSteps(goal, { ...g, nodes: keptNodes.length ? keptNodes : g.nodes }, bp);
      const steps = this._pickConcreteSteps(lp.steps, bp.steps, contextual)
        || contextual
        || keptNodes.map(n => {
          const circ = this._pathStepCircled(n.pathStep);
          return `阅读${circ}「${n.name}」要点，完成 1 份与本阶段产出相关的记录或计算（附数据/例证）`;
        });
      const knNames = keptNodes.map(n => n.name);
      const llmScenes = Array.isArray(lp.knowledgeScenes) ? lp.knowledgeScenes
        : (Array.isArray(bp.knowledgeScenes) ? bp.knowledgeScenes : []);
      const knowledgeScenes = llmScenes.length
        ? llmScenes
        : this._buildKnowledgeScenes(knNames, keptNodes, goal);
      return {
        phaseIndex: g.phaseIndex,
        phase: lp.phase || bp.phase || lp.name || g.phase,
        role: g.role,
        pathSteps: keptNodes.map(n => n.pathStep),
        pathStepLabels: keptNodes.map(n => this._pathStepCircled(n.pathStep)),
        graphRef: keptNodes.map(n => this._pathStepCircled(n.pathStep)).join(''),
        nodeIds: keptNodes.map(n => n.id),
        knowledgeNames: knNames,
        knowledgeScenes,
        venue: lp.venue || bp.venue || '',
        durationHint: lp.durationHint || bp.durationHint || '',
        steps,
        deliverable: this._pickConcreteDeliverable(lp, bp, g.role, goal),
        tools: bp.tools || lp.tools || this._inferPhaseTools(goal, lp.phase || bp.phase || g.phase, this._classifyProjectType(goal)),
        acceptance: bp.acceptance || lp.acceptance || [],
        literacy: this._supplementPolPsychLiteracy(this._literacyFromLlmPhase(lp), { role: g.role, phaseIndex: g.phaseIndex }),
      };
    });
    const chain = knowledgeChain || mainline.map(n => n.name).join(' → ');
    return {
      mode: 'graph-aligned',
      goal: String(goal || ''),
      knowledgeChain: chain,
      mainlineCount: mainline.length,
      phases,
      external: (external || []).map(n => (typeof n === 'string' ? n : n.name)).filter(Boolean)
    };
  }

  buildPathPlanFromResult(result) {
    if (!result) return null;
    if (result.pathPlan?.phases?.length) return result.pathPlan;
    const graphNodes = result.graphData?.nodes?.length || 0;
    if (!graphNodes && result.projectBlueprint) {
      const phases = this._blueprintProjectPhases(result.projectBlueprint, result.goal);
      if (phases.length) {
        return {
          mode: 'blueprint-only',
          goal: String(result.goal || ''),
          knowledgeChain: result.projectBlueprint.knowledgeChain || phases.map(p => p.phase).join(' → '),
          mainlineCount: 0,
          phases: phases.map((p, i) => ({
            phaseIndex: i + 1,
            phase: p.phase,
            role: 'core',
            pathSteps: [],
            pathStepLabels: [],
            graphRef: '',
            nodeIds: [],
            knowledgeNames: p.knowledgeNames || [],
            steps: p.steps || [],
            deliverable: p.deliverable || '',
            literacy: this._supplementPolPsychLiteracy(p.literacy || {}, { role: 'core', phaseIndex: i + 1 })
          })),
          external: []
        };
      }
    }
    return this._buildPathPlan({
      goal: result.goal,
      graphData: result.graphData,
      projectPhases: result.projectPhases,
      blueprintPhases: result.projectBlueprint ? this._blueprintProjectPhases(result.projectBlueprint, result.goal) : [],
      knowledgeChain: result.knowledgeChain,
      external: result.external
    });
  }

  _buildTechRouteFromPathPlan(pathPlan) {
    if (!pathPlan?.phases?.length) return '';
    let text = `围绕「${pathPlan.goal.slice(0, 100)}」的实施路径（阶段与图谱序号一一对应）\n\n`;
    text += `知识链：${pathPlan.knowledgeChain}\n\n`;
    pathPlan.phases.forEach(p => {
      const kn = (p.knowledgeNames || []).map(n => `「${n}」`).join('、');
      text += `【阶段${p.phaseIndex} · 图谱 ${p.graphRef || p.pathStepLabels?.join('') || ''}】${p.phase}\n`;
      text += `知识点：${kn}\n`;
      text += `任务：${(p.steps || []).join('；')}\n`;
      const literacy = this._formatPhaseLiteracy(p);
      if (literacy) text += `素养指引：${literacy}\n`;
      text += `产出：${p.deliverable}\n\n`;
    });
    if (pathPlan.external?.length) {
      text += `拓展参考：${pathPlan.external.map(n => `「${n}」`).join('、')}\n`;
    }
    return this._sanitizeTechRoute(text).slice(0, 1200);
  }

  _subjectLabel(subject) {
    const map = {
      math: '数学', physics: '物理', chemistry: '化学', biology: '生物', science: '科学',
      'info-tech': '信息技术', chinese: '语文', english: '英语', history: '历史', geography: '地理',
      politics: '道法', psychology: '心理',
    };
    return map[subject] || subject || '';
  }

  // ─── PBL 路径分析核心 ──────────────────────────

  static GENERIC_TRANSVERSAL_RE = /批判性思维|创新思维|创新能力|团队协作|团队合作|项目管理|项目管理能力|沟通能力|沟通表达|问题解决|解决问题能力|时间管理|领导力|学习能力|核心素养|综合素养|信息素养|媒体素养|科学精神|人文素养|劳动素养|审辨性思维|审辨思维|元认知|学会学习|责任担当|社会责任|公民素养|国际理解/;
  static HOLLOW_STEP_RE = /^(完成|进行|开展|落实|实施|贯彻|培养|提升|增强|锻炼|学习|掌握|了解|认识|运用|选择|确定|调研|编写|配置|安装).{0,10}(探究|调研|学习|任务|活动|阶段|工作|研究|分析|讨论|探索|实践|制作|设计|总结|反思|课件|练习|组件|框架|逻辑|特点|风格|方案|软件|环境)$|完成本阶段|进行调研|开展研究|完成探究|运用.*完成本阶段|培养.*素养|提升.*能力|环境搭建|编写基础/;
  static PBL_MAX_GRAPH_NODES = 22;
  static PBL_MIN_EXTERNAL = 1;
  static PBL_MAX_EXTERNAL = 3;
  static PBL_MAX_EXTERNAL_IOT = 6;
  static PBL_MAX_MATCHED_COMPLEX = 10;
  static PBL_MIN_MATCHED_COMPLEX = 5;
  static PBL_MIN_CURRICULUM_CORE = 5;
  static PBL_MIN_GRADE_COMPLEX = 7;

  _isEmbeddedOrIoTGoal(goal) {
    return /物联网|IoT|智能设备|智能家居|智能硬件|嵌入式|单片机|Arduino|树莓派|ESP32|STM32|传感|GPIO|Wi-?Fi|蓝牙|BLE|LED|语音识别|语音控制|无线通信|模块|硬件|电路|烧录|串口|自动浇花|浇花系统|浇水系统|智能灌溉|土壤湿度|微型水泵|自动灌溉|湿度传感|智能温室|温室温控|气象.*看板|温湿度/i.test(String(goal || ''));
  }

  _externalLimit(goal) {
    return this._isEmbeddedOrIoTGoal(goal)
      ? PBLPathBuilder.PBL_MAX_EXTERNAL_IOT
      : PBLPathBuilder.PBL_MAX_EXTERNAL;
  }

  _getMinMatchedFloor(archetype) {
    return Math.max(
      PBLPathBuilder.PBL_MIN_CURRICULUM_CORE,
      parseInt(archetype?.minMatched, 10) || 0,
      PBLPathBuilder.PBL_MIN_MATCHED_COMPLEX
    );
  }

  _assignCoreRoles(nodes, minCore) {
    if (!nodes.length) return nodes;
    const floor = Math.min(minCore, nodes.length);
    const sorted = [...nodes].sort((a, b) => (b.confidence || 0) - (a.confidence || 0));
    const coreIds = new Set(sorted.slice(0, floor).map(n => n.id));
    return nodes.map(n => ({
      ...n,
      pblRole: coreIds.has(n.id) ? 'core' : (n.pblRole || 'bridge'),
    }));
  }

  _guaranteeCurriculumFloor(nodes, goal, pool, archetype, limit, complex, blueprint = null, options = {}) {
    const min = this._getMinMatchedFloor(archetype);
    const excludeIds = new Set(options.excludeIds || []);
    let list = Array.isArray(nodes) ? [...nodes] : [];
    const allowed = this._getAllowedSubjects(goal, archetype);
    const effectivePool = this._getBroadCurriculumPool(goal, pool, Math.max(min * 4, 50))
      .filter(n => !excludeIds.has(n.id))
      .filter(n => !allowed?.size || allowed.has(n.subject));
    if (list.length < min && effectivePool.length) {
      list = this._ensureMinimumMatched(list, goal, effectivePool, limit, complex, archetype);
    }
    if (list.length < min && effectivePool.length) {
      const rescued = this._rescueFromK12KnowledgeGraph(goal, blueprint, archetype, limit, effectivePool, { floorMode: true });
      const seen = new Set(list.map(n => n.id));
      rescued.forEach(n => {
        if (list.length >= min || seen.has(n.id)) return;
        seen.add(n.id);
        list.push(n);
      });
    }
    if (list.length < min) {
      const forced = this._rescueFromK12KnowledgeGraph(
        goal, blueprint, archetype, limit,
        this._getK12Pool(goal).filter(n => !excludeIds.has(n.id)),
        { floorMode: true }
      );
      const seen = new Set(list.map(n => n.id));
      forced.forEach(n => {
        if (list.length >= min || seen.has(n.id)) return;
        seen.add(n.id);
        list.push(n);
      });
    }
    const specSubjects = this._subjectFilterFromProjectSpec(this._activeProjectSpec);
    if (this._isPrimarySchoolContext(goal) && specSubjects?.length) {
      list.sort((a, b) => {
        const am = specSubjects.includes(a.subject) ? 1 : 0;
        const bm = specSubjects.includes(b.subject) ? 1 : 0;
        return bm - am;
      });
    }
    list = this._ensureTopicAnchorRecall(list, goal, effectivePool, archetype, limit);
    return this._assignCoreRoles(list.slice(0, limit), min);
  }

  /**
   * 语义锚点保底：题目含明确地点/时代时，召回对应学科课标节点（如英国研学→地理+历史）
   */
  _ensureTopicAnchorRecall(matched, goal, pool, archetype, limit) {
    const anchors = this._getTopicAnchors(goal);
    if (!anchors.strong || !anchors.subjects.length) return matched;

    const list = [...matched];
    const seen = new Set(list.map(n => n.id));
    const basePool = (pool?.length ? pool : this._getK12Pool(goal))
      .filter(n => this._passesHardNodeGate(n, goal, archetype));

    anchors.subjects.forEach(subj => {
      const hasStrong = list.some(n => n.subject === subj && this._nodeMatchesTopicAnchors(n, goal, 6));
      if (hasStrong) return;

      const ranked = basePool
        .filter(n => n.subject === subj)
        .filter(n => !seen.has(n.id))
        .map(n => ({
          ...n,
          _anchorScore: this._scoreTopicAnchorRelevance(n, goal)
            + this._scoreUniversalRelevance(n, goal, null, this._inferProjectDomains(goal), archetype) * 0.3,
        }))
        .filter(n => n._anchorScore >= 6)
        .sort((a, b) => b._anchorScore - a._anchorScore);

      const pick = ranked[0];
      if (!pick) return;
      seen.add(pick.id);
      list.push({
        ...pick,
        confidence: Math.max(0.68, pick.confidence || 0.68),
        matchReason: `语义召回：${(anchors.places || []).join('、') || (anchors.periods || []).join('、') || '主题'}相关${subj}课标`,
        pblRole: 'bridge',
      });
    });

    if (anchors.subjects.length) {
      const recalled = list.filter(n => anchors.subjects.includes(n.subject) && this._nodeMatchesTopicAnchors(n, goal, 4));
      if (recalled.length) {
        console.warn('[PBL] 语义锚点召回:', recalled.map(n => `${n.name}(${n.subject})`).join('、'));
      }
    }
    return list.slice(0, limit);
  }

  _getPBLGoalProfile(goal) {
    const g = String(goal || '').trim();
    const gradeBand = this._parseExplicitGradeBand(g, this._activeProjectSpec);
    const advanced = /系统|平台|模型|算法|传感器|物联网|智能|仿真|优化|数据分析|机器学习|人工智能|开发|App|API|控制|工程|跨学科|综合性|自动化|闭环|原型|调试/i;
    let signals = 0;
    if (g.length >= 60) signals += 1;
    if (advanced.test(g)) signals += 1;
    if (/设计|制作|构建|实现|搭建|部署/.test(g)) signals += 1;
    if ((g.match(/[，,、;；]/g) || []).length >= 2) signals += 1;
    const complex = !this._isSocialOrCivicInquiryGoal(g)
      && (signals >= 2 || (g.length >= 45 && advanced.test(g)));
    const minGrade = gradeBand.explicit
      ? gradeBand.minGrade
      : (complex ? PBLPathBuilder.PBL_MIN_GRADE_COMPLEX : 1);
    return {
      complex,
      explicitGrade: gradeBand.explicit,
      gradeBand,
      minGrade,
      maxMatched: complex ? PBLPathBuilder.PBL_MAX_MATCHED_COMPLEX : 14
    };
  }

  _isComplexPBLGoal(goal) {
    return this._getPBLGoalProfile(goal).complex;
  }

  _basicKnowledgeNamePatterns() {
    return [
      /图形(的认识|与几何)|认识图形|观察物体|平面图形|立体图形|长方体|正方体|圆柱|球的认识|周长|面积(的认识|计算)/,
      /统计|数据的(收集|整理|表示)|分类与整理|象形统计|条形统计|折线统计|扇形统计|平均数|可能性/,
      /数的认识|20以内|100以内|比大小|分与合|数一数|比一比|分数的初步|小数的意义/,
      /认识(毫米|厘米|分米|米|千米|质量|时间|钟表|人民币)/,
      /加(减)法|乘(除)法|混合运算|口算|笔算|运算律|倍的认识/,
      /简单机械|杠杆|滑轮|浮力|磁铁|植物|动物|天气|四季|太阳|月亮|影子|声音的产生|光的传播/,
      /物质的三态|溶解|蒸发|电路元件|简单电路|串联|并联(电路)?$/
    ];
  }

  /** 复杂项目应排除：小学数学/科学/物理启蒙、识图统计、与交付物无关的泛基础 */
  _excludeForComplexProject(node) {
    if (!node) return true;
    const name = String(node.name || '').trim();
    const grade = parseInt(node.grade, 10) || 0;
    const label = `${node.gradeLabel || ''} ${node.stageLabel || ''} ${name}`;
    if (/小学|一年级|二年级|三年级|四年级|五年级|六年级/.test(label)) return true;
    if (grade > 0 && grade < PBLPathBuilder.PBL_MIN_GRADE_COMPLEX) return true;
    const elemSubjects = ['math', 'physics', 'science', 'chemistry', 'biology'];
    if (grade > 0 && grade <= 6 && elemSubjects.includes(node.subject)) return true;
    return this._basicKnowledgeNamePatterns().some(re => re.test(name));
  }

  _isTooBasicKnowledge(node, { complex = false } = {}) {
    if (!node) return false;
    if (complex) return this._excludeForComplexProject(node);
    const name = String(node.name || '').trim();
    if (!name) return false;
    const nameIsBasic = this._basicKnowledgeNamePatterns().some(re => re.test(name));
    const grade = parseInt(node.grade, 10) || 0;
    const layer = node.layer || 'matched';
    if (layer === 'matched' || layer === 'external') {
      return nameIsBasic && grade > 0 && grade <= 6;
    }
    if (grade > 0 && grade <= 5) return true;
    return nameIsBasic;
  }

  _filterMatchedForComplexProject(matched = []) {
    const list = matched
      .filter(n => !this._excludeForComplexProject(n))
      .sort((a, b) => (b.confidence || 0) - (a.confidence || 0));
    return list.slice(0, PBLPathBuilder.PBL_MAX_MATCHED_COMPLEX);
  }

  /** PBL 核心提示词在服务端 /api/pbl/analyze；GitHub Pages 等静态站统一走 teachany.cn */
  _getPBLAnalyzeUrl() {
    const host = typeof location !== 'undefined' ? String(location.hostname || '') : '';
    if (host === 'teachany.cn' || host === 'www.teachany.cn') {
      return `${location.origin}/api/pbl/analyze`;
    }
    return 'https://www.teachany.cn/api/pbl/analyze';
  }

  _getRecommendedScheme(blueprint) {
    if (!blueprint) return null;
    const schemes = blueprint.schemes || [];
    return schemes.find(s => s.id === blueprint.recommendedSchemeId) || schemes[0] || null;
  }

  _blueprintProjectPhases(blueprint, goal = '') {
    const scheme = this._getRecommendedScheme(blueprint);
    if (!scheme) return [];
    const g = String(goal || '');
    return (scheme.phases || []).map(p => ({
      phase: p.phase || p.name || '',
      steps: p.steps || [],
      knowledgeNames: this._filterPhaseKnowledgeNames(p.knowledgeHints || p.knowledgeNames || [], g),
      deliverable: p.deliverable || p.output || '',
      literacy: p.literacy || {},
      subsystemIds: p.subsystemIds || []
    }));
  }

  _buildMixedSolutionChemistryBlueprint(goal) {
    const cap = this._getChemistryAnalysisProfile(goal);
    const sample = cap.sampleLabel;
    return {
      projectSummary: String(goal || '').slice(0, 160),
      deliverable: `${sample}盐/电解质含量测定报告（硝酸银滴定法与电导率法对比分析）`,
      projectType: 'scientific-inquiry',
      constraints: [
        '样品为混合溶液，无法直接称量分离溶质',
        '须说明取样、澄清、稀释与平行测定方案',
        '滴定/电导率操作注意安全与器皿洁净'
      ],
      subsystems: [
        { id: 'constraint', name: '测定约束与方案选型', description: '分析混合溶液为何不能直接测质量分数' },
        { id: 'titration', name: '硝酸银滴定法', description: '利用 Ag⁺ 与 Cl⁻ 沉淀反应间接测定盐含量' },
        { id: 'conductivity', name: '电导率法', description: '通过电导率与离子浓度关系建立标准曲线' },
        { id: 'calc', name: '数据处理', description: '由滴定体积或电导率换算浓度并评估误差' }
      ],
      schemes: [
        {
          id: 'A',
          name: '硝酸银滴定法（推荐）',
          summary: `取样澄清后，用硝酸银标准溶液滴定氯离子，换算${sample}盐分含量`,
          pros: ['化学原理清晰', '适合测 Cl⁻/食盐', '高中实验可操作'],
          cons: ['需配制或标定 AgNO₃ 溶液', '终点判断需练习'],
          phases: [
            { phase: '问题与方案选型', steps: ['说明混合溶液不能直接称量的原因', '比较滴定法与电导率法优劣', '确定取样与稀释方案'], deliverable: '方案论证小结', subsystemIds: ['constraint'], knowledgeHints: ['溶液', '离子', '氯离子', '物质的量浓度', '滴定'] },
            { phase: '滴定原理与准备', steps: ['复习 AgNO₃ 与 Cl⁻ 沉淀反应', '准备滴定管、锥形瓶与终点判断方法'], deliverable: '原理笔记与器材清单', subsystemIds: ['titration'], knowledgeHints: ['硝酸银', '沉淀反应', '离子反应', '化学方程式'] },
            { phase: '取样与滴定', steps: ['取样澄清、定容稀释', '平行滴定并记录读数'], deliverable: '滴定原始记录表', subsystemIds: ['titration'], knowledgeHints: ['滴定', '实验', '测量', '记录'] },
            { phase: '计算与结论', steps: ['由消耗 AgNO₃ 体积换算 n(Cl⁻) 及 c(NaCl)', '与标准或另一方法对比并讨论误差'], deliverable: '测定报告', subsystemIds: ['calc'], knowledgeHints: ['物质的量', '计算', '浓度', '误差', '统计'] }
          ]
        },
        {
          id: 'B',
          name: '电导率法',
          summary: '配制标准盐溶液测电导率建立曲线，再测样品电导率反推浓度',
          pros: ['测定快速', '适合批量筛查'],
          cons: ['受温度与杂质离子干扰', '需标定曲线'],
          phases: [
            { phase: '原理与标定设计', steps: ['理解电解质导电与离子浓度关系', '设计标准溶液系列'], deliverable: '标定方案', subsystemIds: ['conductivity'], knowledgeHints: ['电解质', '电导率', '离子', '溶液'] },
            { phase: '建立标准曲线', steps: ['测定标准溶液电导率并绘图'], deliverable: '标准曲线图', subsystemIds: ['conductivity'], knowledgeHints: ['数据', '图表', '浓度', '函数'] },
            { phase: '样品测定', steps: ['测样品电导率', '由曲线读出等效浓度'], deliverable: '样品数据表', subsystemIds: ['conductivity'], knowledgeHints: ['测量', '电导', '换算'] },
            { phase: '对比分析', steps: ['与滴定结果或参考值对比', '讨论误差来源'], deliverable: '对比分析报告', subsystemIds: ['calc'], knowledgeHints: ['分析', '误差', '报告'] }
          ]
        }
      ],
      recommendedSchemeId: 'A',
      knowledgeChain: '测定约束 → 滴定/电导率原理 → 取样测定 → 浓度换算 → 结论',
      fallback: true
    };
  }

  _sanitizeBlueprintForGoal(blueprint, goal) {
    let bp = blueprint;
    if (bp?.schemes?.length) {
      bp = this._shallowCloneBlueprint(bp);
      this._sanitizeBlueprintPhasesInPlace(bp, goal);
    }
    if (this._isGroundRoboticsGoal(goal)) {
      let grbp = bp;
      if (!grbp?.schemes?.length) {
        const topic = this._extractTopicProfile(goal);
        grbp = this._buildSubjectAnchoredBlueprint(goal, `「${topic.coreTopic}」自动驾驶小车实施方案`);
      } else {
        grbp = this._shallowCloneBlueprint(grbp);
      }
      grbp.projectType = 'engineering';
      const topic = this._extractTopicProfile(goal);
      const engRe = /购车|内燃机|新能源对比|飞行|航空|抗生素|医药|科学理论补全|科学原理补课/;
      if (!grbp.deliverable || engRe.test(grbp.deliverable)) {
        grbp.deliverable = topic.deliverableHint || '可运行的地面小车原型 + 调试测试记录 + 说明文档';
      }
      if (!grbp.projectSummary || grbp.projectSummary.length < 12) {
        grbp.projectSummary = `围绕「${topic.coreTopic}」完成地面小车结构搭建、传感驱动、控制调试与测试验收`;
      }
      this._sanitizeBlueprintPhasesInPlace(grbp, goal);
      return grbp;
    }
    if (this._isEnergyAnalysisGoal(goal)) {
      let eabp = bp;
      const topic = this._extractTopicProfile(goal);
      const label = topic.coreTopic || this._compactProjectLabel(goal);
      if (!eabp?.schemes?.length) {
        eabp = this._buildSubjectAnchoredBlueprint(goal, `「${label}」光伏发电测算方案`);
      } else {
        eabp = this._shallowCloneBlueprint(eabp);
      }
      eabp.projectType = 'energy-analysis';
      const badRe = /调研报告|调查报告|稳定性测试|接线|组装|原型驱动|MVP|硬件|工程报告|装置原型|工程安全|故障排查/;
      if (!eabp.deliverable || badRe.test(eabp.deliverable) || /研究报告|调查报告/.test(eabp.deliverable)) {
        eabp.deliverable = topic.deliverableHint || '光伏发电测算表 + 收益与减排分析图表 + 方案论证报告';
      }
      if (!eabp.projectSummary || eabp.projectSummary.length < 12 || /「\s*」/.test(eabp.projectSummary)) {
        eabp.projectSummary = `围绕「${label}」调查日照与用电数据，估算年发电收益和碳减排效益`;
      }
      eabp.schemes = (eabp.schemes || []).map(s => ({
        ...s,
        name: String(s.name || '').replace(/「\s*」/, `「${label}」`),
        summary: String(s.summary || '').replace(/「\s*」/, `「${label}」`),
      }));
      this._sanitizeBlueprintPhasesInPlace(eabp, goal);
      return eabp;
    }
    if (this._isEmbeddedOrIoTGoal(goal)) {
      let iotbp = bp;
      const topic = this._extractTopicProfile(goal);
      const label = topic.coreTopic || this._compactProjectLabel(goal);
      if (!iotbp?.schemes?.length) {
        iotbp = this._buildSubjectAnchoredBlueprint(goal, `「${label}」智能装置实施方案`);
      } else {
        iotbp = this._shallowCloneBlueprint(iotbp);
      }
      iotbp.projectType = 'engineering';
      const badRe = /调研报告|调查报告|问卷|有机合成|离子检验|原型驱动迭代|MVP|快速原型/;
      if (!iotbp.deliverable || badRe.test(iotbp.deliverable) || /研究报告|调查报告/.test(iotbp.deliverable)) {
        iotbp.deliverable = topic.deliverableHint || `可运行的「${label}」装置原型 + 控制逻辑说明 + 测试记录表`;
      }
      if (!iotbp.projectSummary || iotbp.projectSummary.length < 12 || /「\s*」/.test(iotbp.projectSummary)) {
        iotbp.projectSummary = `围绕「${label}」完成传感采集、控制逻辑、水泵驱动与测试验收`;
      }
      iotbp.schemes = (iotbp.schemes || []).map(s => ({
        ...s,
        name: String(s.name || '').replace(/「\s*」/, `「${label}」`),
        summary: String(s.summary || '').replace(/「\s*」/, `「${label}」`),
      }));
      this._sanitizeBlueprintPhasesInPlace(iotbp, goal);
      return iotbp;
    }
    if (this._isSocialOrCivicInquiryGoal(goal)) {
      let sbp = bp;
      if (!sbp?.schemes?.length) {
        const label = this._compactProjectLabel(goal);
        sbp = this._buildSubjectAnchoredBlueprint(goal, `「${label}」社会调查实施方案`);
      } else {
        sbp = this._shallowCloneBlueprint(sbp);
      }
      sbp.projectType = 'social-inquiry';
      const topic = this._extractTopicProfile(goal);
      if (!sbp.deliverable || sbp.deliverable.length < 10 || /阶段成果|素养/.test(sbp.deliverable)) {
        sbp.deliverable = topic.deliverableHint || '专题调查报告（现状记录表+统计图表+改进建议与宣传策划）';
      }
      if (!sbp.projectSummary || sbp.projectSummary.length < 12) {
        sbp.projectSummary = `围绕「${topic.coreTopic}」开展现状调查、数据分析与改进宣传策划`;
      }
      this._sanitizeBlueprintPhasesInPlace(sbp, goal);
      return sbp;
    }
    if (bp && this._isChemistryInquiryGoal(goal) && this._getChemistryAnalysisProfile(goal).mixed) {
      const cap = this._getChemistryAnalysisProfile(goal);
      const bp = { ...blueprint, schemes: (blueprint.schemes || []).map(s => ({ ...s, phases: (s.phases || []).map(p => ({ ...p })) })) };
      const naiveRe = /称量溶解|直接称量|质量分数.*配制|配制.*盐水|称量.*溶解/;
      if (!bp.deliverable || naiveRe.test(bp.deliverable)) {
        bp.deliverable = `${cap.sampleLabel}盐含量测定报告（硝酸银滴定法/电导率法）`;
      }
      bp.schemes.forEach(s => {
        (s.phases || []).forEach((p, idx) => {
          const blob = [p.phase, ...(p.steps || []), ...(p.knowledgeHints || [])].join(' ');
          if (naiveRe.test(blob) && !/滴定|硝酸银|电导率|间接|AgNO|氯离子/.test(blob)) {
            s.phases[idx] = {
              ...p,
              steps: [
                `说明${cap.sampleLabel}为混合溶液，须间接测定而非直接称量`,
                '比较硝酸银滴定法与电导率法并确定本阶段操作要点',
                ...(p.steps || []).map(st => String(st).replace(/称量溶解|直接称量配制/g, '取样澄清后滴定或测电导率'))
              ].slice(0, 4),
              knowledgeHints: [...new Set([...(p.knowledgeHints || []), '滴定', '硝酸银', '离子反应', '物质的量浓度', '电导率'])].slice(0, 6)
            };
          }
        });
      });
      return bp;
    }
    if (this._isPlantingCultivationGoal(goal)) {
      let pbp = bp ? this._shallowCloneBlueprint(bp) : null;
      if (!pbp?.schemes?.length) pbp = this._buildPlantingCultivationBlueprint(goal);
      pbp.projectType = 'planting-cultivation';
      const topic = this._extractTopicProfile(goal);
      const badRe = /原型驱动迭代|浸润式场景|快速原型|MVP|硬件准备|递进式实施|可展示的项目原型/;
      if (!pbp.deliverable || badRe.test(pbp.deliverable)) pbp.deliverable = topic.deliverableHint;
      if (!pbp.projectSummary || pbp.projectSummary.length < 12) {
        pbp.projectSummary = `围绕「${topic.coreTopic}」开展植物分类学习、${topic.crop || '植物'}栽培与生长观察`;
      }
      pbp.schemes = (pbp.schemes || []).slice(0, 1).map(s => ({
        ...s,
        name: String(s.name || '').replace(/浸润式场景|原型驱动迭代|递进式实施/, `「${topic.coreTopic}」种植`),
        phases: (s.phases || []).map(p => ({
          ...p,
          steps: (p.steps || []).filter(st => !badRe.test(String(st))),
          knowledgeHints: [...new Set([...(p.knowledgeHints || []), '植物', '分类', '光合', '种子', '萌发', '栽培', '生长', topic.crop || '月季'].filter(Boolean))].slice(0, 6),
        })).filter(p => (p.steps || []).length > 0),
      }));
      return pbp;
    }
    if (this._isExhibitionRedesignGoal(goal)) {
      let ebp = bp ? this._shallowCloneBlueprint(bp) : null;
      if (!ebp?.schemes?.length) ebp = this._buildExhibitionRedesignBlueprint(goal);
      ebp.projectType = 'exhibition-redesign';
      const topic = this._extractTopicProfile(goal);
      const engRe = /原型驱动迭代|快速原型|MVP|环境搭建|程序设计|招生简章|递进式实施|可展示的项目原型/;
      if (!ebp.deliverable || engRe.test(ebp.deliverable)) ebp.deliverable = topic.deliverableHint;
      if (!ebp.projectSummary || ebp.projectSummary.length < 12) {
        ebp.projectSummary = `围绕「${topic.coreTopic}」开展展陈空间诊断、主题策划与整改实施`;
      }
      ebp.schemes.forEach(s => {
        s.name = String(s.name || '').replace(/递进式实施|原型驱动迭代/, `「${topic.coreTopic}」改造`);
        s.phases = (s.phases || []).map(p => ({
          ...p,
          steps: (p.steps || []).filter(st => !engRe.test(String(st))),
        })).filter(p => (p.steps || []).length > 0);
      });
      return ebp;
    }
    if (this._isIndustryInnovationGoal(goal)) {
      let ibp = bp ? this._shallowCloneBlueprint(bp) : null;
      if (!ibp?.schemes?.length) ibp = this._buildIndustryInnovationBlueprint(goal);
      ibp.projectType = 'industry-innovation';
      const topic = this._extractTopicProfile(goal);
      const topicName = topic.coreTopic || '低空经济';
      const engRe = /工程设计思维|环境搭建|硬件组件|现代物流管理|智慧城市|搭建原型|MVP|程序设计|电解池|制作实现|快速原型/;
      if (!ibp.deliverable || engRe.test(ibp.deliverable) || /原型|装置|系统开发/.test(ibp.deliverable)) {
        ibp.deliverable = topic.deliverableHint || `${topicName}创新方案报告（场景调研+政策要点+可行性论证）`;
      }
      if (!ibp.projectSummary || ibp.projectSummary.length < 12) {
        ibp.projectSummary = `围绕「${topicName}」开展产业场景调研与创新方案设计：${String(goal).slice(0, 80)}`;
      }
      ibp.schemes.forEach(s => {
        s.phases = (s.phases || []).map(p => {
          const blob = [p.phase, ...(p.steps || []), ...(p.knowledgeHints || [])].join(' ');
          if (engRe.test(blob)) {
            const phase = String(p.phase || '').replace(/工程设计|制作实现|快速原型|搭建/, '创新方案');
            return {
              ...p,
              phase,
              steps: (p.steps || []).filter(st => !engRe.test(String(st))),
              knowledgeHints: [...new Set([...(p.knowledgeHints || []), topicName, '空域', '无人机', '政策', '统计', '说明文'])].slice(0, 6),
            };
          }
          return p;
        }).filter(p => (p.steps || []).length > 0 || (p.phase && !engRe.test(p.phase)));
      });
      return ibp;
    }
    if (!bp || !this._isConsumerDecisionGoal(goal)) {
      return bp || blueprint;
    }
    bp = { ...bp, schemes: (bp.schemes || []).map(s => ({ ...s })) };
    bp.projectType = 'consumer-decision';
    if (!bp.deliverable || /原型|研发|装置|系统开发|数据采集系统|温度控制/.test(bp.deliverable)) {
      bp.deliverable = '家庭/个人消费决策报告（含调研表、对比测算表与推荐结论）';
    }
    const rdRe = /新能源装置|电池温度|电解池|研发|数据采集系统|充放电过程|制作任务|搭建原型/;
    bp.schemes.forEach(s => {
      if (s.phases) {
        s.phases = s.phases.map(p => {
          const phase = String(p.phase || '');
          const steps = (p.steps || []).map(st => String(st));
          if (rdRe.test(phase) || rdRe.test(steps.join(''))) {
            return {
              ...p,
              phase: phase.replace(/新能源装置|电池与新能源装置/, '方案对比'),
              steps: steps.map(st => st
                .replace(/研究电池充放电|学习电解质与离子反应|电池温度控制|程序设计基础/g, '查阅资料并记录对比数据')
                .replace(/实验或制作/g, '调研与测算')),
              knowledgeHints: (p.knowledgeHints || []).filter(h => !/电解池|原电池|程序|比热容|传感器/.test(h))
            };
          }
          return p;
        });
      }
    });
    return bp;
  }

  _applyBlueprintPipeline(goal, blueprint) {
    if (!blueprint?.schemes?.length) return this._fallbackDecomposeBlueprint(goal);
    try {
      const sanitized = this._sanitizeBlueprintForGoal(blueprint, goal);
      return this._concretizeBlueprint(goal, sanitized, this._resolvedArchetype);
    } catch (e) {
      if (/stack|too much recursion/i.test(String(e.message || ''))) {
        console.warn('[PBL] 蓝图加厚栈溢出，返回裁剪蓝图:', e.message);
        const pruned = this._pruneDecomposeBlueprint(this._shallowCloneBlueprint(blueprint));
        if (pruned?.schemes?.length) return pruned;
      }
      throw e;
    }
  }

  _blueprintAnchoredToGoal(blueprint, goal) {
    if (!blueprint?.schemes?.length) return false;
    const topic = this._extractTopicProfile(goal);
    const tokens = this._goalTokens(topic.coreTopic || this._parseGoalSubject(goal));
    const blob = [
      blueprint.projectSummary,
      blueprint.deliverable,
      ...(blueprint.schemes || []).flatMap(s => [
        s.name, s.summary,
        ...(s.phases || []).flatMap(p => [p.phase, ...(p.steps || []), p.deliverable, ...(p.knowledgeHints || [])]),
      ]),
    ].join(' ');
    const genericRe = /递进式实施|原型驱动迭代|浸润式场景|可展示的项目原型|MVP\s*原型|快速原型|硬件准备/;
    if (genericRe.test(blob)) return false;
    const hit = tokens.filter(t => t.length >= 2 && blob.includes(t)).length;
    return hit >= Math.min(2, tokens.length) || blob.includes(topic.coreTopic);
  }

  _buildSubjectAnchoredBlueprint(goal, schemeName) {
    const topic = this._extractTopicProfile(goal);
    const subject = topic.coreTopic || this._compactProjectLabel(goal) || this._parseGoalSubject(goal);
    const domains = this._inferProjectDomains(goal);
    const subsystems = domains.map(d => ({
      id: d.id,
      name: d.label,
      description: `围绕「${subject}」完成${d.label}`,
    }));
    const mkPhase = (dom, i) => {
      const stub = { phase: dom.label, knowledgeHints: dom.keywords.slice(0, 5), subsystemIds: [dom.id] };
      const bpStub = { subsystems, deliverable: topic.deliverableHint || '' };
      return {
        phase: dom.label,
        steps: this._concretizePhaseSteps(goal, stub, i, domains.length, this._resolvedArchetype, bpStub),
        deliverable: this._concretizeDeliverable(goal, dom.label, i === domains.length - 1 ? 'core' : 'bridge', '', bpStub),
        subsystemIds: [dom.id],
        knowledgeHints: dom.keywords.slice(0, 5),
      };
    };
    const chain = domains.map(d => d.label).join(' → ');
    const enriched = this._enrichBlueprintMetadata(goal, {
      projectSummary: topic.definition || `围绕「${subject}」按「${chain}」推进并完成可检查交付物`,
      deliverable: topic.deliverableHint,
      projectType: this._classifyProjectType(goal),
      constraints: this._inferDefaultConstraints(goal),
      scopeLimits: this._inferDefaultScopeLimits(goal),
      successCriteria: this._inferDefaultSuccessCriteria(goal),
      subsystems,
      schemes: [{
        id: 'A',
        name: schemeName || `「${subject}」主题实施方案`,
        summary: `推荐路线：按「${chain}」分阶段完成调查/实验/测算与论证`,
        pros: ['每阶段有可检查产出', '任务含数据表/图表/记录等验收物', '模块名锚定题目关键词'],
        cons: ['需按本校器材与课时微调', '部分数据需查阅公开资料或实地调查'],
        phases: domains.map((d, i) => mkPhase(d, i)),
      }, {
        id: 'B',
        name: `「${subject}」精简路线`,
        summary: `备选：压缩为 3 阶段，适合课时紧张场景（保留核心数据与最终报告）`,
        pros: ['周期更短', '保留核心交付物'],
        cons: ['中间过程记录较少', '数据样本量可能偏小'],
        phases: domains.slice(0, 3).map((d, i) => mkPhase(d, i)),
      }],
      recommendedSchemeId: 'A',
      knowledgeChain: chain,
      fallback: true,
    });
    return enriched;
  }

  _buildExhibitionRedesignBlueprint(goal) {
    return this._buildSubjectAnchoredBlueprint(goal, `「${this._parseGoalSubject(goal)}」展陈改造方案`);
  }

  _buildPlantingCultivationBlueprint(goal) {
    const topic = this._extractTopicProfile(goal);
    const crop = topic.crop || this._plantingCropLabel(goal);
    return this._buildSubjectAnchoredBlueprint(goal, `「${topic.coreTopic}」${crop}种植实施方案`);
  }

  _buildFiltrationBlueprint(goal) {
    const topic = this._extractTopicProfile(goal);
    const subject = topic.coreTopic || '微塑料过滤装置';
    const elem = /小学|家庭|亲子|四|五/.test(String(goal || ''));
    const simulant = elem ? '胡椒粉或茶叶碎' : '茶叶碎/细沙等安全模型颗粒';
    return {
      projectSummary: `设计可测试的「${subject}」，理解粗滤保护、吸附改味与膜孔径拦截的分工`,
      deliverable: '三级过滤装置原型 + A/B/C 对照实验记录表 + 含局限说明的测试报告',
      projectType: 'engineering',
      constraints: ['实验水不入口', '禁止制造或扩散塑料碎屑', '每阶段产出可检查'],
      scopeLimits: [
        '目标是可验证地减少模型颗粒，不能宣称已去除所有微塑料',
        '不能把课堂/家庭自制装置等同于认证饮水净化系统',
        '模型颗粒减少率不能写成真实微塑料去除率',
      ],
      successCriteria: [
        '完成原水/仅粗滤/完整三级三组对照实验',
        '固定水量（如300mL）并记录过滤时间',
        '报告写明各滤层职责与装置局限',
      ],
      subsystems: [
        { id: 'prefilter', name: '粗滤保护层', description: '拦截泥沙与大颗粒，保护后端滤芯' },
        { id: 'adsorption', name: '吸附改味层', description: '活性炭改善异味和颜色，非微塑料过滤核心' },
        { id: 'membrane', name: '膜孔径核心层', description: '明确孔径的膜/陶瓷滤芯承担主要颗粒拦截' },
        { id: 'test', name: '对照测试评价', description: 'A/B/C 对照，记录流速与颗粒变化' },
      ],
      schemes: [
        {
          id: 'A',
          name: '粗滤-活性炭-膜滤芯（推荐）',
          summary: '三级减量结构：粗滤护后级，活性炭改味，膜孔径决定拦截能力',
          pros: ['机理清晰', '可对照验证', '适合课堂或家庭科学项目'],
          cons: ['膜滤芯流速较慢，需检查密封防旁路漏水'],
          phases: [
            {
              phase: '指标与局限界定',
              steps: [
                `列出「${subject}」要验证的指标（模型颗粒变化、流速），并写下2条不能宣称的结论（饮水安全、真实去除率）`,
                `确定实验用水与${simulant}悬浊液配制方案，明确实验水不入口`,
              ],
              deliverable: '指标与局限说明卡',
              subsystemIds: ['test'],
              knowledgeHints: ['过滤', '实验', '安全', '变量', '对照'],
            },
            {
              phase: '滤层选型与组装',
              steps: [
                '制作滤层对比表：粗滤（滤网/滤纸）、活性炭层、膜/陶瓷核心层各写什么孔径或规格、主要作用',
                '按粗滤→活性炭→膜滤芯顺序组装，检查密封与支架稳定，首次出水作冲洗水不饮用',
              ],
              deliverable: '滤层对比表 + 组装检查记录',
              subsystemIds: ['prefilter', 'adsorption', 'membrane'],
              knowledgeHints: ['过滤', '吸附', '沉淀', '孔径', '密封', '材料'],
            },
            {
              phase: 'A/B/C 对照实验',
              steps: [
                'A组原水不过滤、B组仅粗滤、C组完整三级，各过滤300mL，用同一计时方式记录用时',
                `在固定光线与背景下拍照比较三组水的颜色与可见颗粒，记录滤纸残留物`,
              ],
              deliverable: 'A/B/C 对照实验记录表（含照片编号）',
              subsystemIds: ['test'],
              knowledgeHints: ['对照', '实验', '变量', '记录', '观察', '测量'],
            },
            {
              phase: '数据分析与局限说明',
              steps: [
                '计算各组流速（水量÷时间，如300mL÷6min=50mL/min），比较C组是否比B组更慢但更清',
                '在结论中写明：模型颗粒减少率≠真实微塑料去除率，并说明装置不能用于未知野外饮水',
              ],
              deliverable: '测试报告（含数据表+局限段落）',
              subsystemIds: ['test'],
              knowledgeHints: ['统计', '百分', '数据', '计算', '报告', '说明'],
            },
            {
              phase: '改进与展示',
              steps: [
                '根据堵塞或流速下降提出1条改进（如增加粗滤层、先静置再过滤），设计可复测方案',
                '制作展示海报：装置结构图、对照照片、数据表、不能宣称什么',
              ],
              deliverable: '改进方案 + 展示海报',
              subsystemIds: ['prefilter', 'membrane'],
              knowledgeHints: ['改进', '设计', '展示', '说明', '环境'],
            },
          ],
        },
        {
          id: 'B',
          name: '仅粗滤演示版',
          summary: '只用粗滤层演示「能拦什么、拦不住什么」，成本低、便于课堂观察',
          pros: ['材料易得', '现象直观'],
          cons: ['不能代表完整微塑料减量能力'],
          phases: [
            {
              phase: '粗滤演示',
              steps: [
                `用${simulant}配制悬浊液，对比过滤前后照片，记录粗滤能拦截的颗粒类型`,
                '撰写说明：粗滤保护后级滤芯，但不是微塑料过滤核心',
              ],
              deliverable: '粗滤演示记录',
              knowledgeHints: ['过滤', '沉淀', '观察', '记录'],
            },
          ],
        },
      ],
      recommendedSchemeId: 'A',
      knowledgeChain: '指标与局限 → 滤层选型组装 → 对照实验 → 数据分析 → 改进展示',
      fallback: true,
    };
  }

  _buildIndustryInnovationBlueprint(goal) {
    const topic = this._extractTopicProfile(goal);
    const topicName = topic.coreTopic || '低空经济';
    const domains = this._industryInnovationDomains(goal);
    const subsystems = domains.map(d => ({
      id: d.id,
      name: d.label,
      description: `完成「${topicName}」${d.label}相关调研与分析`,
    }));
    const mkPhase = (dom, i) => {
      const stub = { phase: dom.label, knowledgeHints: dom.keywords.slice(0, 5), subsystemIds: [dom.id] };
      const bpStub = { subsystems, deliverable: topic.deliverableHint || '' };
      return {
        phase: dom.label,
        steps: this._concretizePhaseSteps(goal, stub, i, domains.length, this._resolvedArchetype, bpStub),
        deliverable: this._concretizeDeliverable(goal, dom.label, i === domains.length - 1 ? 'core' : 'bridge', '', bpStub),
        subsystemIds: [dom.id],
        knowledgeHints: dom.keywords.slice(0, 5),
      };
    };
    return {
      projectSummary: `围绕「${topicName}」开展产业场景调研与创新方案设计`,
      deliverable: topic.deliverableHint || `${topicName}创新方案报告`,
      projectType: 'industry-innovation',
      constraints: ['资料须标注权威来源', '方案须考虑空域安全与合规', '禁止虚构政策条文'],
      subsystems,
      schemes: [{
        id: 'A',
        name: '政策—场景—原理—方案（推荐）',
        summary: `从${topicName}政策背景入手，调研应用场景，补足技术原理，提出创新方案`,
        pros: ['贴合新兴产业议题', '跨地理/物理/语文/数学', '交付物为可答辩报告'],
        cons: ['需检索行业资料'],
        phases: domains.map((d, i) => mkPhase(d, i)),
      }],
      recommendedSchemeId: 'A',
      knowledgeChain: `${topicName}政策背景 → 应用场景调研 → 技术原理支撑 → 数据可行性 → 创新方案报告`,
      fallback: true,
    };
  }

  _fallbackDecomposeBlueprint(goal) {
    if (this._isPlantingCultivationGoal(goal)) {
      return this._applyBlueprintPipeline(goal, this._buildPlantingCultivationBlueprint(goal));
    }
    if (this._isFiltrationGoal(goal)) {
      return this._applyBlueprintPipeline(goal, this._buildFiltrationBlueprint(goal));
    }
    if (this._isExhibitionRedesignGoal(goal)) {
      return this._applyBlueprintPipeline(goal, this._buildExhibitionRedesignBlueprint(goal));
    }
    if (this._isIndustryInnovationGoal(goal)) {
      return this._applyBlueprintPipeline(goal, this._buildIndustryInnovationBlueprint(goal));
    }
    if (this._isGroundRoboticsGoal(goal)) {
      const topic = this._extractTopicProfile(goal);
      return this._applyBlueprintPipeline(
        goal,
        this._buildSubjectAnchoredBlueprint(goal, `「${topic.coreTopic}」自动驾驶小车实施方案`)
      );
    }
    if (this._isSocialOrCivicInquiryGoal(goal)) {
      const label = this._compactProjectLabel(goal);
      return this._applyBlueprintPipeline(
        goal,
        this._buildSubjectAnchoredBlueprint(goal, `「${label}」社会调查实施方案`)
      );
    }
    if (this._isEnergyAnalysisGoal(goal)) {
      const topic = this._extractTopicProfile(goal);
      const label = topic.coreTopic || this._compactProjectLabel(goal);
      return this._applyBlueprintPipeline(
        goal,
        this._buildSubjectAnchoredBlueprint(goal, `「${label}」光伏发电测算方案`)
      );
    }
    if (this._isConsumerDecisionGoal(goal)) {
      return this._applyBlueprintPipeline(goal, {
        projectSummary: String(goal || '').slice(0, 160),
        deliverable: '家庭购车对比决策报告（含调研表、全成本测算表与推荐结论）',
        projectType: 'consumer-decision',
        constraints: ['基于公开参数与合理假设', '结论需有数据支撑'],
        subsystems: [
          { id: 'needs', name: '家庭需求调研', description: '梳理用车场景、里程、预算、充电/加油条件' },
          { id: 'compare', name: '对比维度设计', description: '确定购置价、能耗、保险维保、残值、环保等政策维度' },
          { id: 'model', name: '全成本测算', description: '用表格与函数估算 3–5 年持有成本' },
          { id: 'science', name: '科学原理支撑', description: '从科普层面理解燃油与电动的能量与排放差异' },
          { id: 'decision', name: '决策与答辩', description: '给出推荐车型及理由，回应家长关切' }
        ],
        schemes: [
          {
            id: 'A',
            name: '问卷调研 + 全成本对比表（推荐）',
            summary: '先调研家庭真实需求，再用数据对比新能源与燃油车全生命周期成本',
            pros: ['贴近生活', '数学物理跨学科', '结论可落地'],
            cons: ['需查阅真实参数'],
            phases: [
              { phase: '家庭需求调研', steps: ['设计简易问卷', '汇总用车场景与预算'], deliverable: '需求调研小结', subsystemIds: ['needs'], knowledgeHints: ['统计', '数据', '调查', '整理'] },
              { phase: '建立对比指标', steps: ['列出购置/能耗/维保/环保维度', '选取两款代表车型'], deliverable: '对比指标表', subsystemIds: ['compare'], knowledgeHints: ['函数', '比较', '分析'] },
              { phase: '科学原理补课', steps: ['了解内燃机效率与电动驱动差异', '了解排放与碳足迹概念'], deliverable: '原理笔记', subsystemIds: ['science'], knowledgeHints: ['内燃机', '效率', '能量', '排放', '环境'] },
              { phase: '全成本测算', steps: ['估算油费/电费与保养', '计算多年总成本'], deliverable: '成本测算表', subsystemIds: ['model'], knowledgeHints: ['一次函数', '计算', '统计', '百分比'] },
              { phase: '购车建议报告', steps: ['撰写对比结论', '班级答辩'], deliverable: '家庭购车建议报告', subsystemIds: ['decision'], knowledgeHints: ['说明文', '报告', '论证'] }
            ]
          },
          {
            id: 'B',
            name: '案例深潜 + 辩论会',
            summary: '选定具体车型案例，从环保政策与使用体验两派立场辩论',
            pros: ['思辨性强', '适合综合实践'],
            cons: ['对资料检索要求高'],
            phases: [
              { phase: '案例资料收集', steps: ['检索车型参数与政策补贴'], deliverable: '案例资料卡', knowledgeHints: ['调查', '数据', '环境'] },
              { phase: '正反观点整理', steps: ['列出燃油/电动各自优劣'], deliverable: '辩论提纲', knowledgeHints: ['比较', '分析', '论证'] },
              { phase: '量化佐证', steps: ['用简单模型估算使用成本'], deliverable: '测算附录', knowledgeHints: ['函数', '统计', '效率'] },
              { phase: '辩论与反思', steps: ['开展辩论', '反思决策依据'], deliverable: '反思日记', knowledgeHints: ['写作', '价值观'] }
            ]
          }
        ],
        recommendedSchemeId: 'A',
        knowledgeChain: '需求调研 → 对比框架 → 科学原理 → 成本测算 → 购车建议',
        fallback: true
      });
    }

    if (this._isChemistryInquiryGoal(goal)) {
      if (this._getChemistryAnalysisProfile(goal).mixed) {
        return this._applyBlueprintPipeline(goal, this._buildMixedSolutionChemistryBlueprint(goal));
      }
      return this._applyBlueprintPipeline(goal, {
        projectSummary: String(goal || '').slice(0, 160),
        deliverable: '厨房食盐溶液浓度探究报告（含实验方案、数据记录表、浓度计算与生活应用分析）',
        projectType: 'scientific-inquiry',
        constraints: ['使用安全可得的厨房材料', '计算需有数据支撑'],
        subsystems: [
          { id: 'solution', name: '溶液与浓度概念', description: '理解溶质/溶剂/溶液与质量分数' },
          { id: 'experiment', name: '实验设计与测量', description: '设计配制或测定食盐溶液浓度的实验' },
          { id: 'data', name: '数据处理', description: '记录数据并用统计图表呈现' },
          { id: 'application', name: '生活应用', description: '联系厨房情境解释结果并撰写报告' }
        ],
        schemes: [{
          id: 'A',
          name: '配制—计算—对比（推荐）',
          summary: '在厨房情境中配制食盐溶液，计算质量分数并与标签/经验值对比',
          pros: ['贴近生活', '化学主线清晰', '兼顾统计表达'],
          cons: ['需规范称量'],
          phases: [
            { phase: '概念准备', steps: ['辨析溶质溶剂溶液', '写出质量分数公式'], deliverable: '概念笔记', knowledgeHints: ['溶液', '溶质', '溶剂', '质量分数', '浓度'] },
            { phase: '实验设计', steps: ['确定称量方案', '设计记录表'], deliverable: '实验方案', knowledgeHints: ['实验', '变量', '测量', '配制'] },
            { phase: '动手探究', steps: ['称量溶解并记录数据'], deliverable: '实验数据表', knowledgeHints: ['溶解', '配制', '数据', '记录'] },
            { phase: '计算与报告', steps: ['计算浓度并制图分析', '撰写生活应用小结'], deliverable: '探究报告', knowledgeHints: ['统计', '图表', '计算', '报告'] }
          ]
        }],
        recommendedSchemeId: 'A',
        knowledgeChain: '溶液概念 → 实验设计 → 数据记录 → 浓度计算 → 生活应用',
        fallback: true
      });
    }

    const topic = this._extractTopicProfile(goal);
    const subject = topic.coreTopic || this._compactProjectLabel(goal) || this._parseGoalSubject(goal);
    const isEng = this._classifyProjectType(goal) === 'engineering' || this._isEnergyProjectGoal(goal) || this._isEmbeddedOrIoTGoal(goal);
    if (!isEng) {
      return this._applyBlueprintPipeline(
        goal,
        this._buildSubjectAnchoredBlueprint(goal, `「${subject}」主题实施方案`)
      );
    }
    const domains = this._inferProjectDomains(goal);
    const subsystems = domains.map(d => ({ id: d.id, name: d.label, description: `完成「${subject}」${d.label}` }));
    const bp = this._buildSubjectAnchoredBlueprint(goal, `「${subject}」工程实施方案`);
    bp.deliverable = `可展示的「${subject}」工程作品+测试数据+说明文档`;
    return this._applyBlueprintPipeline(goal, bp);
  }

  _extractDecomposeData(raw) {
    const jsonStr = this._extractJsonObject(raw);
    const data = this._safeJsonParse(jsonStr);
    if (!data?.schemes?.length) return null;
    const pruned = this._pruneDecomposeBlueprint(data);
    if (!pruned.recommendedSchemeId && pruned.schemes[0]) {
      pruned.recommendedSchemeId = pruned.schemes[0].id;
    }
    return pruned;
  }

  _compactBlueprintForReview(blueprint) {
    const scheme = (blueprint?.schemes || []).find(s => s.id === blueprint?.recommendedSchemeId)
      || blueprint?.schemes?.[0];
    if (!scheme) return blueprint;
    return {
      projectSummary: blueprint.projectSummary,
      deliverable: blueprint.deliverable,
      constraints: blueprint.constraints,
      scopeLimits: blueprint.scopeLimits,
      successCriteria: blueprint.successCriteria,
      subsystems: blueprint.subsystems,
      knowledgeChain: blueprint.knowledgeChain,
      recommendedSchemeId: blueprint.recommendedSchemeId,
      schemes: (blueprint.schemes || []).map(s => ({
        id: s.id,
        name: s.name,
        summary: s.summary,
        pros: s.pros,
        cons: s.cons,
        phases: (s.phases || []).map(p => ({
          phase: p.phase,
          steps: (p.steps || []).slice(0, 4),
          deliverable: p.deliverable,
          subsystemIds: p.subsystemIds,
          knowledgeHints: (p.knowledgeHints || []).slice(0, 5),
        })),
      })),
    };
  }

  _collectDecomposeReviewIssues(goal, blueprint) {
    if (!blueprint?.schemes?.length) return ['缺少可行方案'];
    const issues = [];
    if (this._isGenericBlueprintText(blueprint.projectSummary)) {
      issues.push('projectSummary 过于套话，需写清谁+方法+交付物+要解决的问题');
    }
    if (!blueprint.deliverable || /素养|能力|精神/.test(blueprint.deliverable)) {
      issues.push('最终 deliverable 不具体或含素养空话');
    }
    if (!Array.isArray(blueprint.scopeLimits) || blueprint.scopeLimits.length < 2) {
      issues.push('scopeLimits 不足 2 条，需写明不能宣称的能力边界');
    }
    if (!Array.isArray(blueprint.successCriteria) || blueprint.successCriteria.length < 2) {
      issues.push('successCriteria 不足 2 条，需有可检查验收标准');
    }
    if (!Array.isArray(blueprint.constraints) || blueprint.constraints.length < 2) {
      issues.push('constraints 不足 2 条');
    }
    if ((blueprint.schemes || []).length < 2) issues.push('schemes 不足 2 套');
    if (!this._blueprintAnchoredToGoal(blueprint, goal)) {
      issues.push('未锚定题目关键词，步骤/阶段可能跑题或套用无关模板');
    }
    const substance = this._blueprintSubstanceScore(blueprint, goal);
    if (substance < 3) {
      issues.push('蓝图内容空洞：步骤/交付物缺少题目锚点、数量或可验收表格/图表');
    }
    const profile = this._goalProfile(goal, blueprint);
    const reviewBlob = [
      blueprint.projectSummary,
      ...(blueprint.schemes || []).flatMap(s => (s.phases || []).flatMap(p => p.steps || [])),
    ].join(' ');
    if (profile.mismatchRes.some(re => re.test(reviewBlob))) {
      issues.push('步骤/概述套用与题目不符的通用工程模板，须改为题目对应的任务类型');
    }
    const scheme = (blueprint.schemes || []).find(s => s.id === blueprint.recommendedSchemeId) || blueprint.schemes?.[0];
    if (this._isGenericBlueprintText(scheme?.summary)) {
      issues.push('推荐方案 summary 过于笼统，需写清实施路线差异');
    }
    (scheme?.phases || []).forEach((p) => {
      const steps = p.steps || [];
      if (steps.length < 2) issues.push(`阶段「${p.phase}」steps 不足 2 条`);
      const hollow = steps.filter(s => this._isHollowStep(s)).length;
      if (hollow > 0) issues.push(`阶段「${p.phase}」含 ${hollow} 条空话/笼统步骤，需改为可验收任务`);
      steps.forEach((st, j) => {
        if (this._stepActionabilityScore(st) < 2) {
          issues.push(`阶段「${p.phase}」步骤${j + 1}缺少数量/工具/表格等可验收要素`);
        }
      });
      if (!p.deliverable || /阶段成果|素养|能力/.test(p.deliverable) || String(p.deliverable).length < 6) {
        issues.push(`阶段「${p.phase}」deliverable 不具体`);
      }
    });
    if (this._blueprintStepDepthScore(blueprint) < 2.5) {
      issues.push('整体步骤可操作性偏低，需补充数据表/图表/记录表/测量次数等');
    }
    return [...new Set(issues)].slice(0, 14);
  }

  _shouldReviewDecompose(goal, blueprint) {
    if (!blueprint || blueprint.fallback) return false;
    return this._collectDecomposeReviewIssues(goal, blueprint).length > 0;
  }

  _finalizeDecomposeBlueprint(goal, data) {
    if (!data?.schemes?.length) return this._fallbackDecomposeBlueprint(goal);
    const anchored = this._blueprintAnchoredToGoal(data, goal);
    const depth = this._blueprintStepDepthScore(data);
    const substance = this._blueprintSubstanceScore(data, goal);
    if (substance < 3) {
      console.warn('[PBL] 蓝图内容空洞，使用主题蓝图回退');
      return this._fallbackDecomposeBlueprint(goal);
    }
    if (!anchored && depth < 1.5) {
      console.warn('[PBL] 蓝图未锚定且步骤过浅，使用主题蓝图回退');
      return this._fallbackDecomposeBlueprint(goal);
    }
    if (!anchored) console.warn('[PBL] 蓝图锚定偏弱，客户端加厚 metadata/steps');
    return this._applyBlueprintPipeline(goal, data);
  }

  _parseDecomposeResult(raw, goal) {
    try {
      const data = this._extractDecomposeData(raw);
      if (!data) return this._fallbackDecomposeBlueprint(goal);
      return this._finalizeDecomposeBlueprint(goal, data);
    } catch (e) {
      console.warn('[PBL] decompose JSON 解析失败，使用本地蓝图回退:', e.message);
      return this._fallbackDecomposeBlueprint(goal);
    }
  }

  async _llmReviewDecomposeStage(goal, draftBlueprint, reviewIssues, complex = false) {
    try {
      const response = await this._callPBLAnalyzeStage('review-decompose', {
        goal,
        projectBlueprint: this._compactBlueprintForReview(draftBlueprint),
        reviewIssues,
        complex,
      });
      const data = this._extractDecomposeData(response);
      if (!data) return null;
      const before = this._collectDecomposeReviewIssues(goal, draftBlueprint).length;
      const after = this._collectDecomposeReviewIssues(goal, data).length;
      if (after >= before && this._blueprintStepDepthScore(data) <= this._blueprintStepDepthScore(draftBlueprint)) {
        console.warn('[PBL] review-decompose 未改善质检分，保留初稿');
        return null;
      }
      return data;
    } catch (e) {
      console.warn('[PBL] review-decompose 失败，保留初稿:', e.message);
      return null;
    }
  }

  async _llmDecomposeStage(goal, onStatus = null) {
    const profile = this._getPBLGoalProfile(goal);
    let decomposeGoal = goal;
    const rc = this._refinementContext;
    if (rc?.userMessage) {
      decomposeGoal += `\n\n【本轮调整要求】${rc.userMessage}`;
      if (rc.previousMatched?.length) {
        decomposeGoal += `\n【上轮已匹配课标】${rc.previousMatched.slice(0, 16).join('、')}`;
      }
      if (rc.removeKeywords?.length) decomposeGoal += `\n【须减少】${rc.removeKeywords.join('、')}`;
      if (rc.addKeywords?.length) decomposeGoal += `\n【须加强】${rc.addKeywords.join('、')}`;
    }
    try {
      this._reportPBLStatus(onStatus, '第 1/6 步：生成拆解初稿...');
      const response = await this._callPBLAnalyzeStage('decompose', {
        goal: decomposeGoal,
        complex: profile.complex,
      });
      let data = this._extractDecomposeData(response);
      if (!data) return this._fallbackDecomposeBlueprint(goal);

      const issues = this._collectDecomposeReviewIssues(goal, data);
      if (issues.length) {
        this._reportPBLStatus(onStatus, `第 1/6 步：评审修订蓝图（${issues.length} 项待改）...`);
        const reviewed = await this._llmReviewDecomposeStage(goal, data, issues, profile.complex);
        if (reviewed) {
          data = reviewed;
          console.info('[PBL] review-decompose 已应用修订稿');
        } else {
          console.warn('[PBL] review-decompose 跳过或无效，使用初稿+客户端加厚');
        }
      }

      return this._finalizeDecomposeBlueprint(goal, data);
    } catch (e) {
      console.warn('[PBL] decompose 阶段失败，使用本地蓝图:', e.message);
      return this._fallbackDecomposeBlueprint(goal);
    }
  }

  /**
   * 浏览器直连：自定义 API，或 OpenRouter 填写自有 Key
   * 其余走 TeachAny 服务端中转（Key 在环境变量，用户不可见）
   */
  _usesClientLlm(cfg) {
    return !!(cfg.clientLlm || cfg.providerId === 'custom'
      || (cfg.providerId === 'openrouter' && cfg.apiKey));
  }

  async _callPBLAnalyzeStage(stage, payload) {
    const cfg = this.getLLMConfig();
    const llmOpts = this._llmStageOptions(stage);

    if (this._usesClientLlm(cfg)) {
      if (!cfg.apiKey) {
        throw new Error(cfg.providerId === 'openrouter'
          ? '请先在 ⚙️ API 设置中填写 OpenRouter API Key，或改回 TeachAny 默认走服务端中转'
          : '请先在 ⚙️ API 设置中填写 API Key');
      }
      if (!cfg.model) throw new Error('请先在 ⚙️ API 设置中选择或填写模型名称');
      const messages = await this._fetchPBLMessages(stage, payload);
      return this.callLLM(messages, llmOpts);
    }

    const body = { stage, ...payload };
    if (cfg.model) body.model = cfg.model;
    if (cfg.providerId && cfg.providerId !== 'preset' && cfg.providerId !== 'custom') {
      body.providerId = cfg.providerId;
    }

    const ac = new AbortController();
    const timeout = setTimeout(() => ac.abort(), 180000);
    try {
      const resp = await fetch(this._getPBLAnalyzeUrl(), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        signal: ac.signal,
        body: this._safeStringify(body, `PBL ${stage}`),
      });
      const data = await resp.json().catch(() => ({}));
      if (!resp.ok) {
        throw new Error(data.error || `PBL API ${resp.status}`);
      }
      if (!data.content) throw new Error('PBL API 返回为空');
      return data.content;
    } finally {
      clearTimeout(timeout);
    }
  }

  _basicMentionRegex() {
    return /分数[、，]?小数|百分数互化|四则运算|认识图形|图形的认识|周长(和|与)?面积|圆的周长|简单统计|认识(钟表|人民币|时间)|个位十位|加减乘除|口算|笔算|小学(数学|科学|阶段)/;
  }

  /** 清洗 techRoute：删掉提及小学基础内容的句子，避免出现"先学分数小数"这类内容 */
  _sanitizeTechRoute(text) {
    if (!text) return '';
    const re = this._basicMentionRegex();
    const original = String(text);
    const kept = original
      .split(/\n+/)
      .map(line => line
        .split(/(?<=[。；;])/)
        .filter(seg => !re.test(seg))
        .join(''))
      .filter(line => line.replace(/[【】①②③④⑤\s]/g, '').length > 0);
    const cleaned = kept.join('\n').trim();
    // 避免清洗过猛导致整块「路径说明」消失
    if (cleaned.replace(/\s/g, '').length >= 80) return cleaned;
    if (original.replace(/\s/g, '').length >= 80) return original.slice(0, 600);
    return cleaned;
  }

  /** 解析/重建项目实施路径说明（供 pbl.html 展示与历史恢复） */
  resolveTechRouteText(result) {
    if (!result) return '';
    const pathPlan = this.buildPathPlanFromResult(result);
    if (pathPlan?.phases?.length) {
      return this._buildTechRouteFromPathPlan(pathPlan);
    }

    const nodes = (result.graphData && result.graphData.nodes) ? result.graphData.nodes : [];
    const mainline = this._getMainlinePath(result.graphData);
    const matched = mainline.length ? mainline : (result.matched || nodes.filter(n => n.layer === 'matched'));
    const external = result.external || nodes.filter(n => n.layer === 'external');
    const phases = result.projectPhases || [];
    const goal = result.goal || '';

    let routeText = this._buildTechRouteFromGraph(goal, matched, external, phases);
    if (routeText.replace(/\s/g, '').length < 40) {
      routeText = this._buildFallbackTechRoute(goal, matched, external);
    }
    if (routeText.replace(/\s/g, '').length < 20 && nodes.length) {
      const hint = mainline.length
        ? `按图谱序号 ${mainline.map(n => n.pathStep).join('→')} 推进：${mainline.slice(0, 5).map(n => n.name).join('、')}${mainline.length > 5 ? '…' : ''}。`
        : `共 ${nodes.length} 个节点，请按图谱序号完成各节点课件与动手任务。`;
      routeText = `围绕「${String(goal).slice(0, 80)}」的实施路径：${hint}`;
    }
    return routeText;
  }

  _capGraphNodes(graphData, maxNodes = PBLPathBuilder.PBL_MAX_GRAPH_NODES, goal = '') {
    const normalized = this._normalizeGraphData(graphData);
    const nodes = normalized.nodes;
    if (nodes.length <= maxNodes) return normalized;
    const extCap = this._externalLimit(goal);
    const extKeep = nodes.filter(n => n.layer === 'external').slice(0, extCap);
    const others = nodes.filter(n => n.layer !== 'external');
    const budget = Math.max(maxNodes - extKeep.length, Math.floor(maxNodes * 0.75));
    const layerScore = { matched: 1000, external: 850, advanced: 750, parallel: 400, prerequisite: 600 };
    const roleBonus = { foundation: 100, bridge: 140, core: 80 };
    const scored = others.map(n => ({
      n,
      score: (layerScore[n.layer] || 50) + (n.confidence || 0) * 50
        + (roleBonus[n.pblRole] || 0)
        + (n.pathStep ? 120 : 0)
        - (this._excludeForComplexProject(n) ? 400 : 0)
    }));
    scored.sort((a, b) => b.score - a.score);
    const kept = [...scored.slice(0, budget).map(s => s.n), ...extKeep];
    const keptIds = new Set(kept.map(n => n.id));
    const links = (normalized.links || []).filter(l => {
      const src = typeof l.source === 'object' ? l.source.id : l.source;
      const tgt = typeof l.target === 'object' ? l.target.id : l.target;
      return keptIds.has(src) && keptIds.has(tgt);
    });
    return { nodes: kept, links };
  }

  _finalizePBLGraph(goal, matched, external, activeSystems, meta = {}) {
    const profile = this._getPBLGoalProfile(goal);
    const complex = profile.complex;
    const archetype = meta.archetype || null;
    let core = complex ? this._filterMatchedForComplexProject(matched) : matched;
    core = this._purgeCurriculumNoise(core, goal);
    core = this._filterMainlineNodes(core, goal, archetype);
    if (complex && core.length === 0 && matched.length) {
      core = this._filterMainlineNodes(
        [...matched].sort((a, b) => (b.confidence || 0) - (a.confidence || 0)),
        goal,
        archetype
      );
    }
    if (this._archetypeEngine && meta.projectBlueprint) {
      core = this._archetypeEngine.tagMatchedModules(
        core, null, meta.projectBlueprint,
        (n, m) => this._archetypeEngine.scoreForModule(n, m, this._tokenizeGoalTerms(goal))
      );
    }
    const k12Pool = this._getK12Pool(goal, meta.candidatePool || []);
    const poolForFloor = this._getBroadCurriculumPool(
      goal, k12Pool.length ? k12Pool : (meta.candidatePool || []), 80
    );
    core = this._guaranteeCurriculumFloor(
      core, goal, poolForFloor, archetype, profile.maxMatched, complex, meta.projectBlueprint
    );
    if (complex) {
      core = this._rebalanceStemMatched(core, goal, poolForFloor, profile.maxMatched);
      core = this._guaranteeCurriculumFloor(
        core, goal, poolForFloor, archetype, profile.maxMatched, complex, meta.projectBlueprint
      );
    }
    if (!core.length) {
      core = this._rescueFromK12KnowledgeGraph(goal, meta.projectBlueprint, archetype, profile.maxMatched, k12Pool);
      core = this._assignCoreRoles(core, this._getMinMatchedFloor(archetype));
    }
    if (!core.length && meta.candidatePool?.length) {
      core = this._rescueCandidatesFromPool(goal, k12Pool.length ? k12Pool : meta.candidatePool, profile.maxMatched, meta.archetype, meta.projectBlueprint);
      console.warn('[PBL] 主线为空，已用蓝图模块回退:', core.map(n => n.name).join('、'));
    }
    // 主线 pathStep 链 + 角色分层着色 + 一层主线相关前置（不展开平行/跨学科噪声）
    let graphData = this._buildRichMainlineGraph(
      core,
      meta.pathOrderIds || [],
      goal,
      meta.dependsOnLinks || [],
      external.slice(0, this._externalLimit(goal))
    );
    graphData = this._capGraphNodes(graphData, PBLPathBuilder.PBL_MAX_GRAPH_NODES, goal);
    const mainline = this._getMainlinePath(graphData);
    const extOut = external.slice(0, this._externalLimit(goal));
    return {
      complex,
      matched: mainline.length ? mainline : core,
      external: extOut,
      graphData,
    };
  }

  /**
   * 主线加密图谱：pathStep 实施链 + 角色三色 + 一层课标前置（经主线过滤）
   * - foundation → 绿色 prerequisite
   * - bridge → 紫色 advanced
   * - core → 红色 matched
   */
  _buildRichMainlineGraph(matchedNodes, pathOrderIds, goal, dependsOnLinks, externalNodes) {
    const base = this._buildProjectPathGraph(matchedNodes, externalNodes || [], pathOrderIds || []);
    const nodeMap = new Map(base.nodes.map(n => [n.id, n]));
    const links = [...base.links];
    const domains = this._inferProjectDomains(goal);
    const complex = this._isComplexPBLGoal(goal);

    base.nodes.forEach(n => {
      if (!n.pathStep) return;
      const role = n.pblRole || 'core';
      if (role === 'foundation') n.layer = 'prerequisite';
      else if (role === 'bridge') n.layer = 'advanced';
      else n.layer = 'matched';
    });

    const matchedIds = new Set(matchedNodes.map(n => n.id));
    const blueprint = this._activeBlueprint || null;
    const archetype = this._resolvedArchetype || null;
    matchedNodes.forEach(n => {
      const kg = this.unifiedIndex.get(n.id);
      if (!kg) return;
      (kg.prerequisites || []).slice(0, 2).forEach(preId => {
        if (matchedIds.has(preId) || nodeMap.has(preId)) return;
        const preNode = this.unifiedIndex.get(preId);
        if (!preNode) return;
        if (complex && this._excludeForComplexProject(preNode)) return;
        if (!this._shouldAttachPrerequisite(preNode, n, goal, blueprint, domains, archetype)) return;
        const enriched = { ...preNode, layer: 'prerequisite' };
        base.nodes.push(enriched);
        nodeMap.set(preId, enriched);
        links.push({ source: preId, target: n.id, type: 'prerequisite' });
      });

      const strictGraphExpansion = true;
      if (this.graphLoaded && !strictGraphExpansion) {
        const graphNb = this.graphNeighbors.get(n.id);
        if (graphNb) {
          // 跨学科前置（来自图谱边的 parents，且不在 prerequisites 中）
          const existingPrereqs = new Set(kg.prerequisites || []);
          let crossAdded = 0;
          graphNb.parents.forEach(parentId => {
            if (crossAdded >= 3) return; // 每节点最多 3 个跨学科前置
            if (existingPrereqs.has(parentId) || matchedIds.has(parentId) || nodeMap.has(parentId)) return;
            const parentNode = this.unifiedIndex.get(parentId);
            if (!parentNode) return;
            if (parentNode.subject === kg.subject) return; // 同学科跳过（已由 prerequisites 覆盖）
            if (complex && this._excludeForComplexProject(parentNode)) return;
            if (!this._isMainlineRelevant(parentNode, goal, domains)) return;
            const enriched = { ...parentNode, layer: 'prerequisite', crossSubject: true };
            base.nodes.push(enriched);
            nodeMap.set(parentId, enriched);
            links.push({ source: parentId, target: n.id, type: 'cross-prerequisite' });
            crossAdded++;
          });

          // 大学延伸节点（来自图谱边的 children 中 grade=0 的大学节点）
          let uniAdded = 0;
          graphNb.children.forEach(childId => {
            if (!this._shouldAllowUniversityNodes(goal)) return;
            if (uniAdded >= 2) return; // 每节点最多 2 个大学延伸
            if (matchedIds.has(childId) || nodeMap.has(childId)) return;
            const childNode = this.unifiedIndex.get(childId);
            if (!childNode || childNode.grade !== 0) return;
            if (!this._passesGradeBandGate(childNode, goal)) return;
            if (!this._isMainlineRelevant(childNode, goal, domains)) return;
            const enriched = { ...childNode, layer: 'advanced', isUniversity: true };
            base.nodes.push(enriched);
            nodeMap.set(childId, enriched);
            links.push({ source: n.id, target: childId, type: 'university-bridge' });
            uniAdded++;
          });
        }
      }
    });

    (dependsOnLinks || []).forEach(l => {
      const src = typeof l.source === 'object' ? l.source.id : l.source;
      const tgt = typeof l.target === 'object' ? l.target.id : l.target;
      if (nodeMap.has(src) && nodeMap.has(tgt)) {
        links.push({ source: src, target: tgt, type: l.type || 'depends-on' });
      }
    });

    let nodes = base.nodes;
    if (this._shouldPurgeAviationForGoal(goal) || this._shouldPurgeBiologyForGoal(goal)
      || this._shouldPurgeOffTopicScienceForGoal(goal)) {
      let keptNodes = nodes;
      keptNodes = this._purgeAviationNoise(keptNodes, goal);
      keptNodes = this._purgeCurriculumNoise(keptNodes, goal);
      const kept = new Set(keptNodes.map(n => n.id));
      nodes = nodes.filter(n => kept.has(n.id));
    }
    const keptIds = new Set(nodes.map(n => n.id));
    const prunedLinks = links.filter(l => {
      const src = typeof l.source === 'object' ? l.source.id : l.source;
      const tgt = typeof l.target === 'object' ? l.target.id : l.target;
      return keptIds.has(src) && keptIds.has(tgt);
    });
    return { nodes, links: this._deduplicateLinks(prunedLinks) };
  }

  _buildProjectPathGraph(matchedNodes, externalNodes, pathOrderIds = []) {
    const byId = new Map(matchedNodes.map(n => [n.id, n]));
    const ordered = [];
    (pathOrderIds || []).forEach(id => {
      if (byId.has(id) && !ordered.find(o => o.id === id)) ordered.push(byId.get(id));
    });
    matchedNodes
      .sort((a, b) => (b.confidence || 0) - (a.confidence || 0))
      .forEach(n => {
        if (!ordered.find(o => o.id === n.id)) ordered.push(n);
      });

    const nodes = [];
    const links = [];
    ordered.forEach((n, idx) => {
      nodes.push({ ...n, layer: 'matched', pathStep: idx + 1 });
    });
    for (let i = 0; i < ordered.length - 1; i++) {
      links.push({ source: ordered[i].id, target: ordered[i + 1].id, type: 'path-step' });
    }
    externalNodes.forEach(ext => {
      nodes.push({ ...ext, layer: 'external' });
      const related = this._findMostRelated(ext, ordered);
      if (related) {
        links.push({ source: related.id, target: ext.id, type: 'external-related' });
      }
    });
    return { nodes, links: this._deduplicateLinks(links) };
  }

  _buildTechRouteFromGraph(goal, matched = [], external = [], projectPhases = []) {
    const allNames = [...matched, ...external].map(n => String(n.name || ''));
    const basicRe = this._basicMentionRegex();
    // 只允许引用图谱中真实存在、且非小学基础的节点名
    const validName = (name) => {
      const s = String(name || '').replace(/[「」]/g, '').trim();
      if (!s || basicRe.test(s)) return null;
      const hit = allNames.find(n => n === s || n.includes(s) || s.includes(n));
      return hit ? `「${hit}」` : null;
    };
    const nameList = (arr) => arr.map(n => `「${n.name}」`).filter(x => !basicRe.test(x)).join('、');

    if (!matched.length && !external.length) {
      return '未能匹配到课标知识点，知识图谱无法生成。请检查网络或 LLM 配置后重试；也可尝试把目标写得更具体（学科、年级、交付物）。';
    }

    if (Array.isArray(projectPhases) && projectPhases.length) {
      const subjSet = [...new Set(matched.map(n => n.subject).filter(Boolean))];
      let text = `围绕「${String(goal || '').slice(0, 100)}」的项目实施路线：\n\n`;
      if (subjSet.length >= 2) {
        text += `涉及学科：${subjSet.map(s => this._subjectLabel(s)).filter(Boolean).join('、')}\n\n`;
      }
      projectPhases.slice(0, 5).forEach((p, i) => {
        const steps = (Array.isArray(p.steps) ? p.steps : [p.task || p.desc || ''])
          .filter(s => s && !basicRe.test(s)).join('；');
        let kn = (Array.isArray(p.knowledgeNames) ? p.knowledgeNames : [])
          .map(validName).filter(Boolean).join('、');
        if (!kn) kn = nameList(matched.slice(i * 2, i * 2 + 3)) || '（见图谱核心节点）';
        const literacy = this._formatPhaseLiteracy(p);
        text += `【阶段${i + 1}】${p.phase || p.name || '实施阶段'}\n`;
        text += `任务：${steps || '完成本阶段拆解、建模与实现'}\n`;
        text += `知识支撑：${kn}\n`;
        if (literacy) text += `素养指引：${literacy}\n`;
        text += `产出：${p.deliverable || p.output || '阶段原型/数据/报告'}\n\n`;
      });
      return this._sanitizeTechRoute(text).slice(0, 900);
    }

    const ordered = [...matched].sort((a, b) => (a.pathStep || 99) - (b.pathStep || 99));
    let text = `围绕「${String(goal || '').slice(0, 100)}」，按真实施工顺序推进：\n\n`;
    text += `① 原理理解：${nameList(ordered.slice(0, 2)) || '核心原理节点'}——搞清项目背后的科学/工程原理。\n`;
    text += `② 建模与计算：${nameList(ordered.slice(2, 4)) || '建模相关节点'}——用模型/公式量化关键指标。\n`;
    text += `③ 搭建与实现：${nameList(ordered.slice(4, 7)) || '实现相关节点'}——完成原型、程序或实验装置。\n`;
    text += `④ 测试与迭代：依据指标做对比测试并优化${external.length ? '，可引入 ' + nameList(external) : ''}。\n`;
    text += `\n红色节点上的序号即推荐实施先后，按 pathStep 逐段完成课件与动手任务。`;
    return this._sanitizeTechRoute(text).slice(0, 600);
  }

  _reportPBLStatus(onStatus, msg) {
    if (typeof onStatus === 'function') onStatus(msg);
  }

  _buildRefineSnapshot(result) {
    return {
      deliverable: result?.projectBlueprint?.deliverable || '',
      phaseNames: (result?.pathPlan?.phases || result?.projectPhases || []).map(p => p.phase).filter(Boolean),
      matchedNames: (result?.matched || []).map(n => n.name),
    };
  }

  _compactCandidateNodes(nodes, limit = 120) {
    const seen = new Set();
    return (nodes || [])
      .filter(n => n && n.id && !seen.has(n.id) && (seen.add(n.id) || true))
      .slice(0, limit)
      .map(n => ({
        id: n.id,
        name: n.name,
        subject: n.subject,
        grade: n.grade,
        gradeLabel: n.gradeLabel,
        stage: n.stage,
        system: n.system,
        systemTag: n.systemTag,
        definition: n.definition,
        pblRole: n.pblRole,
        confidence: n.confidence,
      }));
  }

  searchKnowledgeCandidates(query, goal = '', selectedSystems = ['all'], limit = 30) {
    const q = String(query || '').trim();
    if (!q) return [];
    const terms = q.split(/[\s,，、]+/).map(t => t.trim()).filter(Boolean);
    const activeSystems = selectedSystems.includes('all')
      ? Array.from(this.systemIndex.keys())
      : selectedSystems.filter(s => this.systemIndex.has(s));
    const scored = [];
    this.unifiedIndex.forEach((node) => {
      if (!node || node.isExternal) return;
      if (activeSystems.length && !activeSystems.includes(node.system)) return;
      if (goal && !this._isMatchingPoolNode(node, goal)) return;
      const name = String(node.name || '');
      const text = this._nodeSearchText(node);
      let score = 0;
      terms.forEach(t => {
        if (!t) return;
        if (name === t) score += 30;
        else if (name.includes(t)) score += 18;
        else if (text.includes(t)) score += 8;
      });
      if (!score && terms.length) return;
      score += this._scoreUniversalRelevance(node, goal || q, this._activeBlueprint, this._inferProjectDomains(goal || q), this._resolvedArchetype) * 0.25;
      scored.push({ ...node, _score: score });
    });
    scored.sort((a, b) => b._score - a._score);
    return this._compactCandidateNodes(scored, limit);
  }

  redesignPBLWithSelectedKnowledge(previousResult, selectedIds = []) {
    if (!previousResult) throw new Error('请先完成一次项目拆解');
    const ids = [...new Set((selectedIds || []).filter(Boolean))];
    if (!ids.length) throw new Error('请至少选择 1 个知识点');
    const goal = previousResult.goal || '';
    this._activeProjectSpec = previousResult.projectSpec || this._activeProjectSpec || null;
    this._activeBlueprint = previousResult.projectBlueprint || this._activeBlueprint || null;
    const archetype = this._resolveArchetype(goal);
    this._resolvedArchetype = archetype;
    const existing = new Map((previousResult.graphData?.nodes || []).map(n => [n.id, n]));
    const selected = ids.map((id, idx) => {
      const full = this.unifiedIndex.get(id) || existing.get(id);
      if (!full) return null;
      const ratio = ids.length <= 1 ? 1 : idx / (ids.length - 1);
      const role = ratio < 0.34 ? 'foundation' : (ratio < 0.67 ? 'bridge' : 'core');
      return { ...full, pblRole: full.pblRole || role, confidence: full.confidence || 0.95, _manualSelected: true };
    }).filter(Boolean);
    if (!selected.length) throw new Error('所选知识点不在当前图谱索引中');

    const external = (previousResult.external || previousResult.graphData?.nodes?.filter(n => n.layer === 'external') || [])
      .slice(0, this._externalLimit(goal));
    let graphData = this._buildRichMainlineGraph(selected, ids, goal, [], external);
    graphData = this._capGraphNodes(graphData, PBLPathBuilder.PBL_MAX_GRAPH_NODES, goal);
    const matched = this._getMainlinePath(graphData);
    const blueprintPhases = previousResult.projectBlueprint
      ? this._blueprintProjectPhases(previousResult.projectBlueprint, goal)
      : [];
    const pathPlan = this._buildPathPlan({
      goal,
      graphData,
      projectPhases: previousResult.projectPhases || [],
      blueprintPhases,
      knowledgeChain: matched.map(n => n.name).join(' → '),
      external,
    });
    const techRoute = this._buildTechRouteFromPathPlan(pathPlan) || previousResult.techRoute || '';
    const candidateNodes = this._compactCandidateNodes([
      ...(previousResult.candidateNodes || []),
      ...selected,
      ...(previousResult.graphData?.nodes || []),
    ], 160);
    const quality = this.computeQualityScore({
      goal,
      matched,
      external,
      projectBlueprint: previousResult.projectBlueprint,
      archetype,
      graphData,
      pathPlan,
    });
    return {
      ...previousResult,
      matched,
      external,
      graphData,
      pathPlan,
      projectPhases: pathPlan.phases,
      techRoute,
      knowledgeChain: pathPlan.knowledgeChain,
      candidateNodes,
      selectedKnowledgeIds: ids,
      quality,
      stats: {
        ...(previousResult.stats || {}),
        matchedCount: matched.length,
        externalCount: external.length,
        graphNodes: graphData?.nodes?.length || 0,
        graphLinks: graphData?.links?.length || 0,
        qualityScore: quality.score,
        qualityGrade: quality.grade,
      },
    };
  }

  async refinePBLResult(previousResult, userMessage, projectSpec, selectedSystems = ['all'], onStatus = null, chatHistory = []) {
    const msg = String(userMessage || '').trim();
    if (!msg) throw new Error('请输入修改要求');
    if (!previousResult) throw new Error('请先完成一次项目拆解');

    this._reportPBLStatus(onStatus, '理解修改要求...');
    const snapshot = this._buildRefineSnapshot(previousResult);
    let plan = { summary: '', fullRematch: true, userFacingReply: '好的，将按你的要求重新拆解。' };

    try {
      const response = await this._callPBLAnalyzeStage('refine', {
        goal: previousResult.goal,
        userMessage: msg,
        projectSpec,
        snapshot,
      });
      plan = { ...plan, ...JSON.parse(this._extractJsonObject(response)) };
    } catch (e) {
      console.warn('[PBL] refine 阶段失败，将直接带修改要求重拆:', e.message);
    }

    const spec = { ...(projectSpec || previousResult.projectSpec || {}) };
    if (plan.revisedTask) spec.task = plan.revisedTask;
    if (plan.revisedDeliverable) {
      spec.deliverable = 'other';
      spec.deliverableCustom = plan.revisedDeliverable;
    }

    const goal = (typeof PBLProjectForm !== 'undefined' && PBLProjectForm.composeGoalFromSpec)
      ? PBLProjectForm.composeGoalFromSpec(spec)
      : previousResult.goal;

    const refinementContext = {
      userMessage: msg,
      previousMatched: snapshot.matchedNames,
      removeKeywords: plan.removeKeywords || [],
      addKeywords: plan.addKeywords || [],
      summary: plan.summary || '',
    };

    const nextHistory = [
      ...chatHistory,
      { role: 'user', content: msg, ts: Date.now() },
      { role: 'assistant', content: plan.userFacingReply || plan.summary || '已根据你的要求重新拆解。', ts: Date.now() },
    ];

    const result = await this.analyzePBLGoal(goal, selectedSystems, onStatus, {
      projectSpec: spec,
      refinementContext,
      chatHistory: nextHistory,
    });
    return result;
  }

  async analyzePBLGoal(goal, selectedSystems = ['all'], onStatus = null, options = {}) {
    try {
      return await this._analyzePBLGoalBody(goal, selectedSystems, onStatus, options);
    } catch (e) {
      if (/stack|too much recursion/i.test(String(e.message || ''))) {
        console.warn('[PBL] 分析栈溢出，降级关键词模式:', e.message);
        const result = await this.searchByKeywords(goal, selectedSystems);
        result.projectBlueprint = this._fallbackDecomposeBlueprint(goal);
        result.projectSpec = options.projectSpec || null;
        result.goal = goal;
        return result;
      }
      throw e;
    }
  }

  async _analyzePBLGoalBody(goal, selectedSystems = ['all'], onStatus = null, options = {}) {
    this._activeProjectSpec = options.projectSpec || null;
    this._refinementContext = options.refinementContext || null;
    const chatHistory = options.chatHistory || [];
    const nonPblWarning = this._detectNonPBLGoal(goal);
    if (nonPblWarning) {
      console.warn('[PBL] 非典型 PBL 目标:', nonPblWarning.hint);
    }
    // 1. 确保索引已加载
    this._reportPBLStatus(onStatus, '正在加载多课标知识点索引...');
    await this.loadUnifiedIndex();
    await this._loadKnowledgeGraph();
    await this._ensureArchetypeData();

    // 2. 筛选课标体系（表单多选优先）
    const specSystems = this._activeProjectSpec?.curriculumSystems;
    const systemsInput = (Array.isArray(specSystems) && specSystems.length)
      ? specSystems
      : selectedSystems;
    const activeSystems = systemsInput.includes('all')
      ? Array.from(this.systemIndex.keys())
      : systemsInput.filter(s => this.systemIndex.has(s));

    const src = this._activeProjectSpec?.knowledgeSources || { curriculum: true, k12Graph: true };
    if (src.curriculum === false && src.k12Graph === false) {
      throw new Error('请至少选择一种知识来源：课标或全科图谱');
    }

    // 3. 构建候选知识点列表（默认锚定 K12 全科图谱子图，大学层按需开启）
    const rawCandidates = [];
    this.unifiedIndex.forEach((node) => {
      if (!activeSystems.includes(node.system)) return;
      if (this._isMatchingPoolNode(node, goal)) rawCandidates.push(node);
    });

    if (rawCandidates.length === 0) {
      throw new Error('未找到任何知识点，请检查课标体系选择');
    }

    const archetype = this._resolveArchetype(goal);
    this._reportPBLStatus(onStatus, '核实候选池无关节点...');
    const intakeAudit = this._verifyAndPruneNodes(rawCandidates, goal, archetype, '拆解入口·候选池');
    let candidates = intakeAudit.kept;
    if (!candidates.length) {
      console.warn('[PBL] 入口核实后候选池为空，回退原始候选集');
      candidates = rawCandidates;
    }

    // 4. 第零阶段：全链路拆解可行方案（不选课标）
    const projectBlueprint = await this._llmDecomposeStage(goal, onStatus);
    this._activeBlueprint = projectBlueprint;
    const blueprintPhases = this._blueprintProjectPhases(projectBlueprint, goal);
    const bloomProfile = this._inferBloomProfile(projectBlueprint);

    // 5. 第一阶段 LLM：判断学科+学段+课标体系（压缩候选集）
    this._reportPBLStatus(onStatus, '第 2/6 步：按拆解蓝图筛选课标候选（Bloom 层级）...');
    const stage1 = await this._llmFilterStage(goal, candidates, projectBlueprint, bloomProfile, archetype, activeSystems);
    const filterAudit = this._verifyAndPruneNodes(stage1.filteredCandidates, goal, archetype, '拆解入口·课标筛选后');
    const minRecall = this._getMinMatchedFloor(archetype);
    if (filterAudit.kept.length >= minRecall) {
      stage1.filteredCandidates = filterAudit.kept;
    } else {
      stage1.filteredCandidates = this._unionCandidateNodes(
        [filterAudit.kept, stage1.filteredCandidates],
        Math.max(50, minRecall * 6)
      );
      if (filterAudit.kept.length < minRecall) {
        console.warn(`[PBL] 筛选后候选仅 ${filterAudit.kept.length} 个，已并回宽池 ${stage1.filteredCandidates.length} 个`);
      }
    }

    // 6. 知识点提案 → 图谱对齐 → validate-match（失败回退 index match）
    this._reportPBLStatus(onStatus, '第 3/6 步：知识点提案并对齐图谱...');
    let stage2 = await this._runCurriculumProposeValidatePipeline(
      goal, stage1.filteredCandidates, projectBlueprint, stage1.bloomProfile, archetype
    );

    // 6.5 相关性二审：规则白名单 + LLM 剔除幻觉节点
    this._reportPBLStatus(onStatus, '第 4/6 步：核实课标节点相关性...');
    stage2 = await this._llmVerifyRelevanceStage(
      goal, stage2, stage1.filteredCandidates, archetype, projectBlueprint
    );
    const goalProfile = this._getPBLGoalProfile(goal);
    const curriculumPool = this._getBroadCurriculumPool(goal, stage1.filteredCandidates, 80);
    stage2 = {
      ...stage2,
      matched: this._guaranteeCurriculumFloor(
        stage2.matched || [],
        goal,
        curriculumPool,
        archetype,
        goalProfile.maxMatched,
        goalProfile.complex,
        projectBlueprint
      ),
    };

    // 7. 第三阶段：dependsOn 方向性验证
    this._reportPBLStatus(onStatus, '第 5/6 步：校验知识依赖方向...');
    const verifiedResult = await this._llmVerifyDepsStage(goal, stage2.rawMatchResult, stage1.filteredCandidates, stage2.matched);
    const builtLinks = this._buildDependsOnLinks(verifiedResult, stage1.filteredCandidates);
    if (builtLinks.length) {
      stage2.dependsOnLinks = builtLinks;
    } else if (!(stage2.dependsOnLinks || []).length) {
      stage2.dependsOnLinks = builtLinks;
    }

    const finalized = this._finalizePBLGraph(goal, stage2.matched, stage2.external, activeSystems, {
      pathOrderIds: stage2.pathOrderIds,
      dependsOnLinks: stage2.dependsOnLinks || [],
      candidatePool: stage1.filteredCandidates,
      archetype,
      projectBlueprint,
    });
    this._reportPBLStatus(onStatus, '输出前核实无关节点...');
    let outputAudit = this._verifyOutputBundle({
      complex: finalized.complex,
      matched: finalized.matched,
      external: finalized.external,
      graphData: finalized.graphData,
    }, goal, archetype);
    outputAudit = this._applyOutputCurriculumFloor(outputAudit, goal, archetype, curriculumPool, {
      pathOrderIds: stage2.pathOrderIds,
      dependsOnLinks: stage2.dependsOnLinks,
      projectBlueprint,
    });

    this._reportPBLStatus(onStatus, '第 6/6 步：LLM 二次检讨课内节点...');
    const reviewed = await this._llmReviewCurriculumStage(
      goal,
      outputAudit.graphData?.nodes || [],
      projectBlueprint,
      archetype
    );
    if (reviewed.removed?.length) {
      const keptIds = new Set(reviewed.nodes.map(n => n.id));
      const links = (outputAudit.graphData?.links || []).filter(l => {
        const src = typeof l.source === 'object' ? l.source.id : l.source;
        const tgt = typeof l.target === 'object' ? l.target.id : l.target;
        return keptIds.has(src) && keptIds.has(tgt);
      });
      outputAudit.graphData = { nodes: reviewed.nodes, links };
      outputAudit.matched = this._getMainlinePath(outputAudit.graphData).length
        ? this._getMainlinePath(outputAudit.graphData)
        : reviewed.nodes.filter(n => n.layer === 'matched' || (n.pblRole || 'core') === 'core');
      const min = this._getMinMatchedFloor(archetype);
      if (outputAudit.matched.length < min) {
        const reviewRemovedIds = (reviewed.removed || []).map(r => r.id).filter(Boolean);
        const refilled = this._guaranteeCurriculumFloor(
          outputAudit.matched,
          goal,
          curriculumPool,
          archetype,
          this._getPBLGoalProfile(goal).maxMatched,
          outputAudit.complex,
          projectBlueprint,
          { excludeIds: reviewRemovedIds }
        );
        const graphData = this._buildRichMainlineGraph(
          refilled,
          stage2.pathOrderIds || [],
          goal,
          stage2.dependsOnLinks || [],
          outputAudit.external || []
        );
        outputAudit.matched = refilled;
        outputAudit.graphData = this._capGraphNodes(graphData, PBLPathBuilder.PBL_MAX_GRAPH_NODES);
        console.warn('[PBL] 检讨后不足底线，已按泛化分重补:', refilled.map(n => n.name).join('、'));
      }
    }

    const finalMatched = outputAudit.matched || [];
    const finalExternal = outputAudit.external || [];
    const finalGraphData = this._normalizeGraphData(outputAudit.graphData);
    const llmPhases = stage2.projectPhases || [];
    const phaseLen = Math.max(blueprintPhases.length, llmPhases.length);
    const mergedPhases = phaseLen ? Array.from({ length: phaseLen }, (_, i) => {
      const bp = blueprintPhases[i] || {};
      const lp = llmPhases[i] || {};
      const stubGroup = { role: bp.role || 'core', nodes: [] };
      return {
        phase: lp.phase || bp.phase || `阶段 ${i + 1}`,
        steps: this._pickConcreteSteps(lp.steps, bp.steps, this._suggestPhaseSteps(goal, stubGroup, bp)),
        knowledgeNames: this._filterPhaseKnowledgeNames(
          lp.knowledgeNames?.length ? lp.knowledgeNames : bp.knowledgeNames, goal
        ),
        deliverable: this._pickConcreteDeliverable(lp, bp, bp.role, goal),
        literacy: this._supplementPolPsychLiteracy(lp.literacy || bp.literacy || {}, { role: bp.role || 'core', phaseIndex: i + 1 }),
        knowledgeScenes: Array.isArray(lp.knowledgeScenes) ? lp.knowledgeScenes
          : (Array.isArray(bp.knowledgeScenes) ? bp.knowledgeScenes : []),
        venue: lp.venue || bp.venue || '',
      };
    }) : blueprintPhases;
    const moduleChainPre = this._archetypeEngine
      ? this._archetypeEngine.moduleChainFromBlueprint(projectBlueprint)
      : (projectBlueprint.knowledgeChain || '');
    const pathPlan = this._buildPathPlan({
      goal,
      graphData: finalGraphData,
      projectPhases: mergedPhases.length ? mergedPhases : blueprintPhases,
      blueprintPhases,
      knowledgeChain: moduleChainPre || stage2.knowledgeChain || projectBlueprint.knowledgeChain || '',
      external: finalExternal
    });
    const moduleChain = moduleChainPre;
    const techRoute = this._buildTechRouteFromPathPlan(pathPlan)
      || this.resolveTechRouteText({
        goal,
        graphData: finalGraphData,
        matched: finalMatched,
        external: finalExternal,
        projectPhases: pathPlan.phases,
        knowledgeChain: moduleChain || pathPlan.knowledgeChain,
        pathPlan
      });
    const quality = this.computeQualityScore({
      goal,
      matched: finalMatched,
      external: finalExternal,
      projectBlueprint,
      archetype,
      graphData: finalGraphData,
      pathPlan,
    });
    const candidateNodes = this._compactCandidateNodes([
      ...finalMatched,
      ...(stage1.filteredCandidates || []),
      ...(curriculumPool || []),
    ], 160);

    return {
      goal,
      nonPblWarning: nonPblWarning?.hint || null,
      projectSpec: this._activeProjectSpec || options.projectSpec || null,
      chatHistory,
      systems: activeSystems,
      archetype: archetype ? { id: archetype.id, label: archetype.label } : null,
      moduleChain,
      projectBlueprint,
      matched: finalMatched,
      external: finalExternal,
      techRoute,
      projectPhases: pathPlan.phases,
      pathPlan,
      knowledgeChain: moduleChain || pathPlan.knowledgeChain,
      graphData: finalGraphData,
      candidateNodes,
      selectedKnowledgeIds: finalMatched.map(n => n.id),
      complexProject: finalized.complex,
      quality,
      relevanceAudit: {
        intake: intakeAudit.stats,
        postFilter: filterAudit.stats,
        output: outputAudit.relevanceAudit,
      },
      stats: {
        totalCandidates: candidates.length,
        filteredCandidates: stage1.filteredCandidates.length,
        matchedCount: finalMatched.length,
        externalCount: finalExternal.length,
        graphNodes: finalGraphData.nodes.length,
        graphLinks: finalGraphData.links.length,
        qualityScore: quality.score,
        qualityGrade: quality.grade,
        prunedAtIntake: intakeAudit.stats.removed,
        prunedAtFilter: filterAudit.stats.removed,
        prunedAtOutput: outputAudit.relevanceAudit.removedTotal,
      }
    };
  }

  async _llmFilterStage(goal, candidates, projectBlueprint = null, bloomProfile = null, archetype = null, activeSystems = []) {
    const profile = this._getPBLGoalProfile(goal);
    const domains = this._inferProjectDomains(goal);
    const ruleBloom = bloomProfile || this._inferBloomProfile(projectBlueprint);
    if (archetype) {
      profile.maxMatched = archetype.maxMatched || profile.maxMatched;
      if (archetype.minGrade >= 7) profile.complex = true;
    }

    // 按学科+课标体系分组统计
    const subjectSummary = {};
    candidates.forEach(n => {
      const key = `${n.system}|${n.subject}`;
      if (!subjectSummary[key]) {
        subjectSummary[key] = { system: n.system, subject: n.subject, count: 0, tag: n.systemTag };
      }
      subjectSummary[key].count++;
    });

    const countSummary = Object.values(subjectSummary)
      .sort((a, b) => b.count - a.count)
      .map(s => `${s.tag}/${s.subject}: ${s.count}个知识点`)
      .join('\n');
    const exemplarSummary = this._buildSubjectExemplarSummary(candidates, goal, archetype, 4);
    const summaryList = exemplarSummary
      ? `${countSummary}\n\n【各学科高分示例节点】\n${exemplarSummary}`
      : countSummary;

    const response = await this._callPBLAnalyzeStage('filter', {
      goal,
      summaryList,
      complex: profile.complex,
      projectBlueprint,
      bloomProfile: ruleBloom,
      projectSpec: this._activeProjectSpec || null,
    });
    const jsonStr = this._extractJsonObject(response);
    const filter = JSON.parse(jsonStr);
    const mergedBloom = this._mergeBloomProfile(ruleBloom, filter);
    filter.bloomCeiling = mergedBloom.ceiling;
    filter.bloomEvidence = mergedBloom.evidence;
    filter.actionVerbs = mergedBloom.actionVerbs;

    const specSubjects = this._subjectFilterFromProjectSpec(this._activeProjectSpec);
    if (specSubjects?.length) {
      filter.subjects = specSubjects;
    }
    // 其余情况信任 filter 阶段 LLM 返回的 subjects；空数组表示不限学科

    // 根据筛选条件过滤候选集（未写明年级时跨学段，不因年级挡候选）
    const minGrade = profile.explicitGrade ? profile.minGrade : 1;
    const bloomCeiling = mergedBloom.ceiling || 3;
    const minGradeArchetype = profile.explicitGrade
      ? (archetype?.minGrade || profile.minGrade)
      : 1;
    const isPrimaryBand = this._isPrimarySchoolContext(goal);
    const applyElemExclude = !isPrimaryBand
      && (profile.explicitGrade || (profile.complex && this._isStemProjectGoal(goal)));
    const filteredCandidates = candidates.filter(n => {
      const subjectMatch = !filter.subjects || filter.subjects.length === 0 || filter.subjects.includes(n.subject);
      const systemMatch = !filter.systems || filter.systems.length === 0 || filter.systems.includes(n.system);
      const grade = parseInt(n.grade, 10) || 0;
      const gradeMatch = !filter.grades || filter.grades.length === 0
        || filter.grades.some(g => Math.abs(grade - g) <= 2);
      const notElementary = !profile.explicitGrade || grade === 0 || grade >= Math.max(minGrade, minGradeArchetype);
      if (!this._passesGradeBandGate(n, goal)) return false;
      if (applyElemExclude && this._excludeForComplexProject(n)) return false;
      if (archetype && this._isArchetypeBanned(n, archetype)) return false;
      if (this._isNodeAboveBloomCeiling(n, bloomCeiling)) return false;
      return subjectMatch && systemMatch && gradeMatch && notElementary;
    });

    const MAX_STAGE2_CANDIDATES = archetype ? 50 : (profile.complex ? 45 : (this._isSocialOrCivicInquiryGoal(goal) ? 50 : 36));
    let pool = filteredCandidates.length > 0 ? filteredCandidates : candidates.filter(n => {
      if (!this._passesGradeBandGate(n, goal)) return false;
      const g = parseInt(n.grade, 10) || 0;
      if (applyElemExclude) {
        return (g === 0 || g >= minGradeArchetype) && !this._excludeForComplexProject(n);
      }
      return true;
    });
    pool = pool.filter(n => this._isMatchingPoolNode(n, goal));
    pool = this._applyArchetypePoolRules(pool, archetype, activeSystems, goal);
    const poolAudit = this._verifyAndPruneNodes(pool, goal, archetype, '拆解入口·Bloom筛选池');
    if (poolAudit.kept.length >= 6) pool = poolAudit.kept;
    else if (poolAudit.kept.length) pool = poolAudit.kept;
    if (domains.length && (profile.complex || this._isGroundRoboticsGoal(goal)
      || this._isSocialOrCivicInquiryGoal(goal) || this._isConsumerDecisionGoal(goal))) {
      const mainlinePool = pool.filter(n => this._isMainlineRelevant(n, goal, domains));
      if (mainlinePool.length >= 4) {
        pool = this._unionCandidateNodes([mainlinePool, pool], Math.max(pool.length, MAX_STAGE2_CANDIDATES * 2));
      }
    }
    const topCandidates = this._buildMatchCandidateList(
      goal, pool, projectBlueprint, archetype, filter, profile, domains, MAX_STAGE2_CANDIDATES
    );
    if (topCandidates.length) {
      console.log(`[PBL] match 候选召回 ${topCandidates.length} 个:`, topCandidates.slice(0, 8).map(n => n.name).join('、'));
    }
    return { filter, filteredCandidates: topCandidates, domains, bloomProfile: mergedBloom, archetype };
  }

  async _llmMatchStage(goal, candidates, projectBlueprint = null, bloomProfile = null, archetype = null) {
    const profile = this._getPBLGoalProfile(goal);
    const complex = profile.complex || !!archetype;
    const minConf = archetype ? 0.55 : (complex ? 0.58 : 0.52);
    if (archetype) profile.maxMatched = archetype.maxMatched || profile.maxMatched;
    const blueprintPhases = this._blueprintProjectPhases(projectBlueprint, goal);
    const candidatesLite = candidates.map(n => this._enrichCandidateForMatch(n));

    const response = await this._callPBLAnalyzeStage('match', {
      goal,
      candidates: candidatesLite,
      complex,
      maxMatched: profile.maxMatched,
      minConf,
      domainHints: this._inferProjectDomains(goal),
      projectBlueprint,
      bloomProfile: bloomProfile || this._inferBloomProfile(projectBlueprint),
      archetypeId: archetype?.id || null,
      projectSpec: this._activeProjectSpec || null,
    });
    let result = { matched: [], pathOrder: [], projectPhases: [], external: [], techRoute: '' };
    try {
      const jsonStr = this._extractJsonObject(response);
      result = JSON.parse(jsonStr);
    } catch (e) {
      console.warn('[PBL] match JSON 解析失败，将使用关键词回退:', e.message);
    }

    const llmMatched = this._mapMatchedEntries(result, candidates, complex, minConf, goal, archetype)
      .sort((a, b) => (b.confidence || 0) - (a.confidence || 0));
    const llmFallback = llmMatched.length
      ? llmMatched
      : this._mapMatchedEntries(result, candidates, complex, 0.48, goal, archetype)
        .sort((a, b) => (b.confidence || 0) - (a.confidence || 0));

    const retrieved = this._rescueCandidatesFromPool(goal, candidates, profile.maxMatched, archetype, projectBlueprint);
    const minNeed = Math.max(this._getMinMatchedFloor(archetype), archetype?.minMatched || 5);
    let matched = this._unionCandidateNodes(
      [retrieved, llmFallback],
      profile.maxMatched
    );

    if (matched.length < minNeed && candidates.length) {
      const hintRescued = this._retrieveByBlueprintHints(
        candidates, projectBlueprint, archetype, goal, profile.maxMatched
      ).map((n, i) => ({
        ...n,
        confidence: Math.max(0.6, 0.82 - i * 0.03),
        matchReason: '蓝图 hints 检索匹配',
        pblRole: i < 2 ? 'bridge' : 'core',
      }));
      matched = this._unionCandidateNodes([matched, hintRescued], profile.maxMatched);
      if (hintRescued.length) console.warn('[PBL] 蓝图 hints 检索补齐:', hintRescued.map(n => n.name).join('、'));
    }
    if (retrieved.length) console.warn('[PBL] 混合召回课内节点:', matched.map(n => n.name).join('、'));
    const broadCandidates = this._getBroadCurriculumPool(goal, candidates, 80);
    matched = this._guaranteeCurriculumFloor(
      matched, goal, broadCandidates, archetype, profile.maxMatched, complex, projectBlueprint
    );
    const pruned = this._verifyAndPruneNodes(matched, goal, archetype, '匹配后核实').kept;
    if (pruned.length >= this._getMinMatchedFloor(archetype)) {
      matched = pruned;
    }
    if (archetype && this._archetypeEngine) {
      matched = this._archetypeEngine.tagMatchedModules(
        matched, archetype, projectBlueprint,
        (n, m) => this._archetypeEngine.scoreForModule(n, m, this._tokenizeGoalTerms(goal))
      );
    }
    matched = this._guaranteeCurriculumFloor(
      matched, goal, broadCandidates, archetype, profile.maxMatched, complex, projectBlueprint
    );
    matched = this._purgeCurriculumNoise(matched, goal);
    matched = this._rebalanceStemMatched(matched, goal, candidates, profile.maxMatched);
    matched = this._purgeCurriculumNoise(matched, goal);

    let pathOrderIds = (result.pathOrder || result.learningSequence || [])
      .map(i => (typeof i === 'string' ? parseInt(i, 10) : i))
      .filter(i => Number.isInteger(i) && i >= 0 && i < candidates.length)
      .map(i => candidates[i].id)
      .filter(id => matched.some(m => m.id === id));
    if (pathOrderIds.length < matched.length) {
      const byRole = (role) => matched.filter(m => (m.pblRole || 'core') === role).map(m => m.id);
      const synth = [...byRole('foundation'), ...byRole('bridge'), ...byRole('core'),
        ...matched.filter(m => !['foundation', 'bridge', 'core'].includes(m.pblRole)).map(m => m.id)];
      const seen = new Set(pathOrderIds);
      synth.forEach(id => {
        if (!seen.has(id)) {
          seen.add(id);
          pathOrderIds.push(id);
        }
      });
    }

    const dependsOnLinks = this._buildDependsOnLinks(result, candidates);

    let projectPhases = (result.projectPhases || result.phases || []).map((p, i) => ({
      phase: p.phase || p.name || '',
      steps: p.steps || (p.tasks ? (Array.isArray(p.tasks) ? p.tasks : [p.tasks]) : []),
      knowledgeNames: this._filterPhaseKnowledgeNames(p.knowledgeNames || p.knowledge || [], goal),
      knowledgeScenes: p.knowledgeScenes || [],
      venue: p.venue || '',
      deliverable: p.deliverable || p.output || '',
      literacy: this._supplementPolPsychLiteracy(p.literacy || {
        knowledge: p.knowledgeLiteracy || p.knowledge_dim || '',
        method: p.methodLiteracy || p.method || '',
        ability: p.abilityLiteracy || p.ability || '',
        attitude: p.attitudeLiteracy || p.attitude || '',
        emotion: p.emotionLiteracy || p.emotion || '',
        values: p.valuesLiteracy || p.values || ''
      }, { role: p.role || 'core', phaseIndex: i + 1 }),
    }));
    if (!projectPhases.length && blueprintPhases.length) {
      projectPhases = blueprintPhases;
    }

    const external = this._ensureExternalNodes(result.external || [], goal, matched, projectBlueprint, archetype);

    const techRoute = (result.techRoute || '').trim();
    const knowledgeChain = (result.knowledgeChain || '').trim();
    return {
      matched,
      external,
      techRoute,
      pathOrderIds,
      projectPhases,
      dependsOnLinks,
      knowledgeChain,
      rawMatchResult: result,
    };
  }

  _buildFallbackTechRoute(goal, matched = [], external = []) {
    const complex = this._isComplexPBLGoal(goal);
    if (complex) {
      return this._buildTechRouteFromGraph(goal, matched, external, []);
    }
    const basicRe = this._basicMentionRegex();
    const ordered = [...matched].sort((a, b) => (a.pathStep || 99) - (b.pathStep || 99));
    const label = (arr) => arr.map(n => `「${n.name}」`).filter(x => !basicRe.test(x)).join('、') || '相关课标节点';
    let text = `围绕「${String(goal || '').slice(0, 100)}」：\n\n`;
    text += `① 准备：${label(ordered.slice(0, 3))}\n② 探究与实现：${label(ordered.slice(3, 7))}\n`;
    if (external.length) text += `③ 拓展：${label(external)}\n`;
    return this._sanitizeTechRoute(text).slice(0, 500);
  }

  // ─── 路径图构建 ─────────────────────────────────

  _buildPathGraph(matchedNodes, externalNodes, activeSystems, options = {}) {
    const complex = options.complex === true;
    const maxPreDepth = complex ? 3 : 5;
    const maxExtDepth = complex ? 1 : 2;
    const traceOpts = { complex };
    const nodes = new Map();   // id -> node
    const links = [];          // { source, target, type }

    // 1. 加入匹配节点（红色 = 直接匹配）
    matchedNodes.forEach(n => {
      nodes.set(n.id, { ...n, layer: 'matched' });
    });

    // 2. 加入外部节点（虚线 = 外部补充）
    externalNodes.forEach(n => {
      nodes.set(n.id, { ...n, layer: 'external' });
    });

    // 3. 对每个匹配节点，沿 prerequisites 递归溯源（绿色 = 基础前置）
    matchedNodes.forEach(n => {
      this._tracePrerequisites(n.id, nodes, links, 0, maxPreDepth, traceOpts);
    });

    // 4. 对每个匹配节点，沿 extends 前探（紫色 = 扩展高级）
    matchedNodes.forEach(n => {
      this._traceExtends(n.id, nodes, links, 0, maxExtDepth);
    });

    // 5. 沿 parallel 关联（复杂项目跳过，避免图谱膨胀）
    if (!complex) {
      matchedNodes.forEach(n => {
        this._traceParallel(n.id, nodes, links);
      });
    }

    // 6. 外部节点的前置关联（虚线连接）
    externalNodes.forEach(ext => {
      // 尝试匹配外部节点声明的前置知识到已有节点
      if (ext.extPrerequisites) {
        ext.extPrerequisites.forEach(preName => {
          const found = this._findNodeByName(preName, nodes);
          if (found) {
            links.push({ source: found.id, target: ext.id, type: 'external-prereq' });
          }
        });
      }
      // 外部节点连接到最相关的匹配节点
      const related = this._findMostRelated(ext, matchedNodes);
      if (related) {
        links.push({ source: related.id, target: ext.id, type: 'external-related' });
      }
    });

    // 过滤掉引用不存在节点的 link（防止 d3.forceLink 报 node not found）
    const validLinks = this._deduplicateLinks(links).filter(l => {
      const srcId = typeof l.source === 'object' ? l.source.id : l.source;
      const tgtId = typeof l.target === 'object' ? l.target.id : l.target;
      return nodes.has(srcId) && nodes.has(tgtId);
    });

    return {
      nodes: Array.from(nodes.values()),
      links: validLinks
    };
  }

  _tracePrerequisites(nodeId, nodes, links, depth, maxDepth, options = {}) {
    if (depth >= maxDepth) return;
    const node = this.unifiedIndex.get(nodeId);
    if (!node) return;

    (node.prerequisites || []).forEach(preId => {
      const preNode = this.unifiedIndex.get(preId);
      if (!preNode) return;
      if (options.complex && this._excludeForComplexProject({ ...preNode, layer: 'prerequisite' })) return;

      if (!nodes.has(preId)) {
        nodes.set(preId, { ...preNode, layer: 'prerequisite' });
      }

      links.push({ source: preId, target: nodeId, type: 'prerequisite' });
      this._tracePrerequisites(preId, nodes, links, depth + 1, maxDepth, options);
    });
  }

  _traceExtends(nodeId, nodes, links, depth, maxDepth) {
    if (depth >= maxDepth) return;
    const node = this.unifiedIndex.get(nodeId);
    if (!node) return;

    (node.extends || []).forEach(extId => {
      const extNode = this.unifiedIndex.get(extId);
      if (!extNode) return;

      if (!nodes.has(extId)) {
        nodes.set(extId, { ...extNode, layer: 'advanced' });
      }

      links.push({ source: nodeId, target: extId, type: 'extends' });
      this._traceExtends(extId, nodes, links, depth + 1, maxDepth);
    });

    // 也检查谁以当前节点为 extends
    this.unifiedIndex.forEach((other, otherId) => {
      if (other.extends && other.extends.includes(nodeId) && !nodes.has(otherId)) {
        nodes.set(otherId, { ...other, layer: 'advanced' });
        links.push({ source: nodeId, target: otherId, type: 'extends' });
      }
    });
  }

  _traceParallel(nodeId, nodes, links) {
    const node = this.unifiedIndex.get(nodeId);
    if (!node) return;

    (node.parallel || []).forEach(parId => {
      const parNode = this.unifiedIndex.get(parId);
      if (!parNode) return;

      if (!nodes.has(parId)) {
        nodes.set(parId, { ...parNode, layer: 'parallel' });
      }

      links.push({ source: nodeId, target: parId, type: 'parallel' });
    });
  }

  _findNodeByName(name, existingNodes) {
    let best = null;
    let bestScore = 0;
    const q = name.toLowerCase();

    existingNodes.forEach(node => {
      const score = (node.name && node.name.toLowerCase().includes(q)) ? 0.9 :
                    (node.name_en && node.name_en.toLowerCase().includes(q)) ? 0.7 : 0;
      if (score > bestScore) {
        bestScore = score;
        best = node;
      }
    });

    if (!best) {
      this.unifiedIndex.forEach(node => {
        const score = (node.name && node.name.toLowerCase().includes(q)) ? 0.8 :
                      (node.name_en && node.name_en.toLowerCase().includes(q)) ? 0.6 :
                      (node.definition && node.definition.toLowerCase().includes(q)) ? 0.3 : 0;
        if (score > bestScore) {
          bestScore = score;
          best = node;
        }
      });
    }

    return best;
  }

  _findMostRelated(extNode, matchedNodes) {
    let best = null;
    let bestScore = 0;

    matchedNodes.forEach(n => {
      let score = 0;
      if (n.subject && n.subject === extNode.subject) score += 0.3;
      if (n.domain && n.domain === extNode.domain) score += 0.2;
      // 名称关键词重叠
      const extWords = (extNode.name + extNode.definition).toLowerCase().split(/\s+/);
      const nWords = (n.name + n.definition).toLowerCase().split(/\s+/);
      const overlap = extWords.filter(w => w.length > 2 && nWords.includes(w)).length;
      score += overlap * 0.1;
      if (score > bestScore) { bestScore = score; best = n; }
    });

    return best;
  }

  _deduplicateLinks(links) {
    const seen = new Set();
    return links.filter(l => {
      const key = `${l.source}|${l.target}|${l.type}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  // ─── 降级：关键词搜索 ──────────────────────────

  async searchByKeywords(goal, selectedSystems = ['all']) {
    await this.loadUnifiedIndex();
    await this._ensureArchetypeData();

    const activeSystems = selectedSystems.includes('all')
      ? Array.from(this.systemIndex.keys())
      : selectedSystems.filter(s => this.systemIndex.has(s));

    const keywords = this._tokenizeGoalTerms(goal);
    const profile = this._getPBLGoalProfile(goal);
    const matched = [];

    this.unifiedIndex.forEach(node => {
      if (!activeSystems.includes(node.system)) return;
      if (profile.complex && this._excludeForComplexProject(node)) return;
      const score = this._scoreNodeForGoal(node, keywords, null, profile.complex);
      if (score > 0) {
        matched.push({
          ...node,
          confidence: Math.min(score / Math.max(keywords.length, 3), 1),
          matchReason: '关键词匹配'
        });
      }
    });

    matched.sort((a, b) => b.confidence - a.confidence);
    let topMatched = matched.slice(0, 15);
    if (!topMatched.length) {
      const pool = [];
      this.unifiedIndex.forEach(node => {
        if (!activeSystems.includes(node.system)) return;
        if (profile.complex && this._excludeForComplexProject(node)) return;
        pool.push(node);
      });
      topMatched = this._rescueCandidatesFromPool(goal, pool, 15);
    }
    const projectBlueprint = this._fallbackDecomposeBlueprint(goal);
    const external = this._ensureExternalNodes([], goal, topMatched, projectBlueprint);
    const finalized = this._finalizePBLGraph(goal, topMatched, external, activeSystems, {
      candidatePool: topMatched
    });

    const techRoute = this.resolveTechRouteText({
      goal,
      matched: finalized.matched,
      external: finalized.external,
      graphData: finalized.graphData,
      projectBlueprint
    });

    const finalizedGraph = this._normalizeGraphData(finalized.graphData);

    return {
      goal,
      systems: activeSystems,
      projectBlueprint,
      matched: finalized.matched,
      external: finalized.external,
      techRoute,
      graphData: finalizedGraph,
      complexProject: finalized.complex,
      stats: {
        totalCandidates: this.unifiedIndex.size,
        filteredCandidates: this.unifiedIndex.size,
        matchedCount: finalized.matched.length,
        externalCount: finalized.external.length,
        graphNodes: finalizedGraph.nodes.length,
        graphLinks: finalizedGraph.links.length
      },
      fallback: true
    };
  }

  // ─── 工具方法 ────────────────────────────────────

  _hash8(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const c = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + c;
      hash |= 0;
    }
    return Math.abs(hash).toString(16).slice(0, 8);
  }
}

// ─── D3.js 图谱渲染器（复用 tree.html 节点样式） ──────────────────

/** PBL 结果图谱学科亲密度分列（与全科图谱 SUBJECT_LAYOUT_ORDER 对齐） */
const PBL_SUBJECT_LAYOUT_ORDER = [
  'math', 'advanced-math',
  'physics', 'advanced-physics',
  'chemistry', 'advanced-chemistry',
  'biology', 'advanced-biology',
  'science', 'earth-space', 'formal-sciences',
  'engineering', 'civil-engineering', 'chemical-engineering', 'aerospace-engineering',
  'nuclear-engineering', 'naval-engineering', 'hydraulic-engineering', 'agricultural-engineering',
  'computer-science', 'info-tech',
  'chinese', 'english', 'history', 'geography',
];

class PBLGraphRenderer {
  constructor(containerId) {
    this.containerId = containerId;
    this.svg = null;
    this.simulation = null;
    this.width = 0;
    this.height = 600; // render() 中会根据节点数量动态覆盖

    // PBL 层颜色（节点描边用，内部填充用层颜色的半透明）
    this.colors = {
      prerequisite: '#10b981',  // 绿色 - 基础前置
      matched: '#ef4444',       // 红色 - 直接匹配
      advanced: '#8b5cf6',      // 紫色 - 扩展高级
      parallel: '#3b82f6',      // 蓝色 - 平行关联
      external: '#eab308',      // 黄色 - 外部补充
      university: '#6366f1'     // 靛蓝 - 大学延伸
    };

    this.layerLabels = {
      prerequisite: '基础前置',
      matched: '核心必需',
      advanced: '扩展高级',
      parallel: '平行关联',
      external: '外部补充',
      university: '大学延伸'
    };
  }

  _getSubjectX(subject) {
    let idx = PBL_SUBJECT_LAYOUT_ORDER.indexOf(subject);
    let cols = PBL_SUBJECT_LAYOUT_ORDER.length;
    if (idx < 0) {
      idx = PBL_SUBJECT_LAYOUT_ORDER.length;
      cols += 1;
    }
    return (this.width / (cols + 1)) * (idx + 1);
  }

  render(graphData, onNodeClick) {
    const container = document.getElementById(this.containerId);
    if (!container) return;

    this.width = container.clientWidth || 900;
    const nodeCount = (graphData.nodes || []).length || 0;

    // ── 根据节点数量动态计算 SVG 高度和力导向参数 ──
    // 目标：让节点均匀分布在画布上，不挤在一起
    const density = 8000; // 每个节点需要的像素面积（约 90x90 的舒适空间）
    const minH = Math.max(600, window.innerHeight - 320); // 至少 600px 或减去顶部/底部栏
    const calcH = Math.ceil(nodeCount * density / this.width);
    this.height = Math.max(minH, Math.min(calcH, 3000)); // 上限 3000px 防止过高

    // 力导向参数随节点数缩放（v7.9.14：增大排斥力避免节点重叠）
    const baseLinkDist = Math.max(180, Math.min(320, 140 + nodeCount * 0.8));
    const baseCharge   = Math.max(-4000, Math.min(-600, -400 - nodeCount * 5));
    const baseCollide  = Math.max(70, Math.min(100, 55 + nodeCount * 0.2));

    // 清除旧内容
    container.innerHTML = '';

    // 创建图例
    const legend = this._createLegend();
    container.appendChild(legend);

    // 创建 tooltip（与 tree.html 同样式）
    let tooltip = container.querySelector('.pbl-tooltip');
    if (!tooltip) {
      tooltip = document.createElement('div');
      tooltip.className = 'pbl-tooltip';
      tooltip.style.cssText = `
        position:absolute;background:rgba(30,41,59,0.94);backdrop-filter:blur(12px);
        border:1px solid rgba(148,163,184,0.18);border-radius:12px;padding:16px;
        max-width:340px;max-height:70vh;overflow-y:auto;pointer-events:none;
        opacity:0;transition:opacity 0.18s ease;z-index:1000;box-shadow:0 8px 32px rgba(0,0,0,0.4);
        font-family:-apple-system,BlinkMacSystemFont,'Inter','PingFang SC',sans-serif;
        color:#f8fafc;font-size:14px;line-height:1.6;
      `;
      // 关键：弹窗本身可 hover，避免从节点移到弹窗时立即消失，里面的链接才可点击。
      tooltip.addEventListener('mouseenter', () => {
        this._tooltipHovered = true;
        this._cancelTooltipHide();
      });
      tooltip.addEventListener('mouseleave', () => {
        this._tooltipHovered = false;
        this._scheduleTooltipHide(220);
      });
      tooltip.addEventListener('click', (event) => {
        const btn = event.target && event.target.closest ? event.target.closest('[data-pbl-make-course]') : null;
        if (!btn) return;
        event.preventDefault();
        event.stopPropagation();
        const id = btn.getAttribute('data-pbl-make-course');
        const node = (window.PBLPathBuilder && window.PBLPathBuilder.unifiedIndex && window.PBLPathBuilder.unifiedIndex.get(id))
          || (Array.isArray(nodes) ? nodes.find(n => n.id === id) : null);
        if (node && typeof onNodeClick === 'function') onNodeClick(node);
        if (node && window.TeachAnyMakeCourse && typeof window.TeachAnyMakeCourse.open === 'function') {
          window.TeachAnyMakeCourse.open({
            nodeId: node.id,
            nodeName: node.name || node.id,
            source: 'pbl-graph',
            meta: node,
            pblNode: node
          });
        } else if (node && typeof window.generateCourseware === 'function') {
          window.generateCourseware(node.id, node.name || node.id, { pblNode: node, source: 'pbl-graph' });
        }
        this._scheduleTooltipHide(80);
      });
      container.appendChild(tooltip);
    }

    // 创建 SVG
    this.svg = d3.select(container)
      .append('svg')
      .attr('width', this.width)
      .attr('height', this.height)
      .style('background', 'rgba(15, 23, 42, 0.5)')
      .style('border-radius', '12px')
      .style('border', '1px solid rgba(148, 163, 184, 0.15)');

    // 缩放
    const g = this.svg.append('g');
    const zoomBehavior = d3.zoom()
      .scaleExtent([0.1, 4])
      .on('zoom', (event) => g.attr('transform', event.transform));
    this.svg.call(zoomBehavior);

    // 准备数据：历史图谱/旧缓存中的节点可能缺失课标、学段、年级等字段，渲染前用统一索引补齐。
    const enrichNode = (n) => {
      if (!n || n.isExternal) return { ...n };
      const full = window.PBLPathBuilder?.unifiedIndex?.get(n.id);
      if (!full) return { ...n };
      return {
        ...n,
        ...full,
        layer: n.layer || full.layer,
        confidence: n.confidence ?? full.confidence,
        matchReason: n.matchReason ?? full.matchReason,
        isExternal: !!n.isExternal
      };
    };
    const nodes = graphData.nodes.map(n => {
      const enriched = enrichNode(n);
      // 大学延伸节点用独立 layer 颜色
      if (enriched.isUniversity || enriched.grade === 0) enriched.layer = 'university';
      // 跨学科前置节点加标记
      if (enriched.crossSubject) enriched.layerSuffix = '(跨学科)';
      return enriched;
    });
    const links = graphData.links.map(l => ({ ...l }));

    // 箭头标记
    this.svg.append('defs').selectAll('marker')
      .data(['prerequisite', 'extends', 'parallel', 'external-prereq', 'external-related'])
      .join('marker')
      .attr('id', d => `arrow-${d}`)
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 28)
      .attr('refY', 0)
      .attr('markerWidth', 6)
      .attr('markerHeight', 6)
      .attr('orient', 'auto')
      .append('path')
      .attr('d', 'M0,-5L10,0L0,5')
      .attr('fill', d => d.includes('external') ? this.colors.external : d === 'extends' ? this.colors.advanced : d === 'parallel' ? this.colors.parallel : this.colors.prerequisite);

    // 连线（与 tree.html 同样式）
    const link = g.append('g')
      .selectAll('line')
      .data(links)
      .join('line')
      .attr('class', d => `link link-${d.type}`)
      .attr('stroke', d => {
        if (d.type === 'path-step') return this.colors.matched;
        if (d.type === 'university-bridge') return this.colors.university;
        if (d.type === 'cross-prerequisite') return '#f59e0b'; // 琥珀色-跨学科
        if (d.type.includes('external')) return this.colors.external;
        if (d.type === 'extends') return this.colors.advanced;
        if (d.type === 'parallel') return this.colors.parallel;
        return 'rgba(148,163,184,0.3)';
      })
      .attr('stroke-opacity', d => d.type === 'path-step' ? 0.85 : 0.5)
      .attr('stroke-width', d => d.type === 'path-step' ? 2.5 : d.type === 'prerequisite' ? 2 : d.type === 'cross-prerequisite' ? 2 : d.type === 'university-bridge' ? 2 : 1.5)
      .attr('stroke-dasharray', d => {
        if (d.type === 'university-bridge') return '4 2 1 2'; // 点划线
        if (d.type === 'cross-prerequisite') return '8 4'; // 长虚线
        if (d.type.includes('external')) return '6 3';
        if (d.type === 'parallel') return '3 3';
        if (d.type === 'extends') return '6 3';
        return 'none';
      })
      .attr('marker-end', d => `url(#arrow-${d.type})`);

    // 节点组（与 tree.html 同样式：circle + status icon + label + label-en + grade）
    const node = g.append('g')
      .selectAll('g')
      .data(nodes)
      .join('g')
      .attr('class', 'node-group')
      .attr('cursor', 'pointer')
      .call(d3.drag()
        .on('start', this._dragStarted.bind(this))
        .on('drag', this._dragged.bind(this))
        .on('end', this._dragEnded.bind(this)));

    // ─── Circle（与 tree.html renderTree 同逻辑） ───
    node.append('circle')
      .attr('class', 'node-circle')
      .attr('r', d => this._nodeHasAnyCourse(d) ? 22 : 18)
      .attr('fill', d => {
        const layerColor = this.colors[d.layer] || '#64748b';
        if (this._nodeHasAnyCourse(d)) return this._hexToRgba(layerColor, 0.25);
        return this._hexToRgba(layerColor, 0.08);
      })
      .attr('stroke', d => {
        const layerColor = this.colors[d.layer] || '#64748b';
        if (this._nodeHasAnyCourse(d)) return layerColor;
        return this._hexToRgba(layerColor, 0.55);
      })
      .attr('stroke-dasharray', d => this._nodeHasAnyCourse(d) ? 'none' : '4 3')
      .attr('stroke-width', 2.5);

    // ─── Status icon（与 tree.html 同） ───
    node.append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .attr('font-size', '14px')
      .text(d => {
        if (d.isExternal) return '💡';
        if (this._hubResolvableTreeCourses(d.courses)) return '✅';
        if (this._nodeHasAnyCourse(d)) return '📂';
        return '📝';
      });

    // ─── 中文主名（与 tree.html 同） ───
    node.append('text')
      .attr('class', 'node-label')
      .attr('dy', 38)
      .attr('font-size', '12px')
      .attr('font-family', "'PingFang SC', sans-serif")
      .attr('fill', '#f8fafc')
      .attr('text-anchor', 'middle')
      .attr('pointer-events', 'none')
      .text(d => this._truncate(d.name, 12));

    // ─── 英文副标（与 tree.html 同） ───
    node.filter(d => d.name_en)
      .append('text')
      .attr('class', 'node-label-en')
      .attr('dy', 52)
      .attr('font-size', '10px')
      .attr('font-style', 'italic')
      .attr('opacity', 0.55)
      .attr('fill', '#94a3b8')
      .attr('text-anchor', 'middle')
      .attr('pointer-events', 'none')
      .text(d => this._truncate(d.name_en, 16));

    // ─── 年级（与 tree.html 同） ───
    node.append('text')
      .attr('class', 'node-grade')
      .attr('dy', d => d.name_en ? 68 : 52)
      .attr('font-size', '10px')
      .attr('fill', '#64748b')
      .attr('text-anchor', 'middle')
      .attr('pointer-events', 'none')
      .text(d => {
        if (d.gradeLabel) return d.gradeLabel;
        if (!d.grade) return d.stage === 'university' ? '大学' : '';
        if (d.system === 'cn') {
          if (d.grade === 0 || d.stage === 'university') return '大学';
          if (d.grade <= 6) return `小学${d.grade}年级`;
          if (d.grade <= 9) return `初中${d.grade - 6}年级`;
          if (d.grade <= 12) return `高中${d.grade - 9}年级`;
        }
        return 'G' + d.grade;
      });

    // ─── PBL 层颜色角标（小圆点，标在左上） ───
    node.append('circle')
      .attr('cx', -14)
      .attr('cy', -14)
      .attr('r', 5)
      .attr('fill', d => this.colors[d.layer] || '#64748b')
      .attr('stroke', '#0f172a')
      .attr('stroke-width', 1.5);

    // ─── 课标体系角标（CN/AP/CA/IB/US） ───
    node.filter(d => d.systemTag && !d.isExternal)
      .append('text')
      .attr('x', 14)
      .attr('y', -14)
      .attr('text-anchor', 'middle')
      .attr('font-size', '8px')
      .attr('font-weight', '700')
      .attr('fill', d => this.colors[d.layer] || '#94a3b8')
      .text(d => d.systemTag);

    // ─── 实施顺序序号（主线节点） ───
    node.filter(d => d.pathStep)
      .append('text')
      .attr('x', 16)
      .attr('y', 14)
      .attr('text-anchor', 'middle')
      .attr('font-size', '10px')
      .attr('font-weight', '800')
      .attr('fill', d => this.colors.matched)
      .attr('pointer-events', 'none')
      .text(d => d.pathStep);

    // ─── 点击事件 ───
    if (onNodeClick) {
      node.on('click', (event, d) => {
        event.stopPropagation();
        onNodeClick(d);
      });
    }

    // ─── Tooltip 交互 ───
    // 不能在 node mouseleave 时立即隐藏，否则鼠标还没移到 tooltip，课程链接就消失了。
    // 使用短延迟 + tooltip 自身 mouseenter 取消隐藏，保证弹窗内链接可点击。
    node.on('mouseenter', (event, d) => {
      this._cancelTooltipHide();
      this._showTooltip(tooltip, container, event, d);
    }).on('mousemove', (event) => {
      if (!this._tooltipHovered) this._moveTooltip(tooltip, container, event);
    }).on('mouseleave', () => {
      this._scheduleTooltipHide(420);
    });

    // ─── 力导向布局（参数随节点数量动态缩放） ───
    this.simulation = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(links).id(d => d.id).distance(baseLinkDist).strength(0.5))
      .force('charge', d3.forceManyBody().strength(baseCharge))
      .force('center', d3.forceCenter(this.width / 2, this.height / 2))
      .force('collision', d3.forceCollide().radius(baseCollide))
      .force('x', d3.forceX(d => this._getSubjectX(d.subject)).strength(nodeCount > 30 ? 0.18 : 0.12))
      .force('y', d3.forceY(this.height / 2).strength(0.03))
      .on('tick', () => {
        link
          .attr('x1', d => d.source.x)
          .attr('y1', d => d.source.y)
          .attr('x2', d => d.target.x)
          .attr('y2', d => d.target.y);

        node.attr('transform', d => `translate(${d.x},${d.y})`);
      });

    // ── Auto-fit zoom：模拟稳定后自动缩放至全貌可见 ──
    let tickCount = 0;
    const autoFitZoom = () => {
      tickCount++;
      // 等 120+ tick（约 3-4 秒）后执行一次 auto-fit
      if (tickCount === 120) {
        const gEl = g.node();
        if (!gEl) return;
        const bbox = gEl.getBBox();
        if (bbox.width > 0 && bbox.height > 0) {
          const padding = 80;
          const scale = Math.min(
            (this.width - padding * 2) / bbox.width,
            (this.height - padding * 2) / bbox.height,
            1.5 // 最大初始缩放不超过 1.5x
          );
          const tx = this.width / 2 - (bbox.x + bbox.width / 2) * scale;
          const ty = this.height / 2 - (bbox.y + bbox.height / 2) * scale;
          // 使用 d3.zoomIdentity 平滑过渡到 fit 视图
          this.svg.transition()
            .duration(600)
            .call(zoomBehavior.transform, d3.zoomIdentity.translate(tx, ty).scale(scale));
        }
      }
    };
    this.simulation.on('tick.autoFit', autoFitZoom);
  }

  // ─── Tooltip 内容（与 tree.html showTooltip 同结构） ───

  _showTooltip(tooltip, container, event, d) {
    const layerColors = this.colors;
    const layerLabels = this.layerLabels;
    const layerColor = layerColors[d.layer] || '#64748b';
    const layerLabel = layerLabels[d.layer] || '';

    let html = `<h3 style="font-size:15px;margin:0 0 6px;">${d.name}</h3>`;
    html += `<div style="font-size:12px;color:#94a3b8;margin-bottom:8px;">${this._escapeHtml(this._metaLine(d))}</div>`;

    // PBL 层标签
    html += `<span style="display:inline-block;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600;background:${layerColor}22;color:${layerColor};">${layerLabel}</span> `;
    if (d.systemTag && !d.isExternal) {
      html += `<span style="display:inline-block;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600;background:rgba(59,130,246,0.15);color:#3b82f6;">${this._escapeHtml(d.systemTag)} ${this._escapeHtml(d.curriculumLabel || d.systemLabel)}</span> `;
    }
    if ((d.stageLabel || d.gradeLabel) && !d.isExternal) {
      html += `<span style="display:inline-block;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600;background:rgba(148,163,184,0.14);color:#cbd5e1;">${this._escapeHtml([d.stageLabel, d.gradeLabel].filter(Boolean).join(' · '))}</span> `;
    }

    // 状态
    const hasAnyCourse = this._nodeHasAnyCourse(d);
    if (hasAnyCourse) {
      html += `<span style="display:inline-block;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600;background:rgba(16,185,129,0.2);color:#10b981;">✅ 有课件</span>`;
    } else {
      html += `<span style="display:inline-block;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600;background:rgba(239,68,68,0.2);color:#f87171;">📝 待创建</span>`;
    }

    // 课件列表（标准节点 + 外部节点均可展示）
    if (hasAnyCourse) {
      const courses = this._getCoursesForNode(d);
      if (courses.length > 0) {
        html += `<div style="margin-top:8px;padding:6px 8px;background:rgba(16,185,129,0.06);border-radius:6px;">`;
        html += `<div style="font-size:11px;font-weight:600;color:#10b981;margin-bottom:4px;">📖 可用课件</div>`;
        courses.slice(0, 5).forEach(c => {
          const url = c.url || (c.path ? `./community/${c.id}/index.html` : '');
          const name = c.name || c.id;
          if (url) {
            html += `<a href="${url}" target="_blank" style="display:block;padding:3px 6px;margin:2px 0;border-radius:4px;font-size:12px;color:#10b981;text-decoration:none;background:rgba(16,185,129,0.08);">${this._escapeHtml(name)}</a>`;
          } else {
            html += `<div style="padding:3px 6px;margin:2px 0;font-size:12px;color:#94a3b8;">${this._escapeHtml(name)}</div>`;
          }
        });
        html += `</div>`;
      }
    }

    // 匹配置信度
    if (d.confidence) {
      html += `<span style="display:inline-block;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600;background:rgba(245,158,11,0.15);color:#f59e0b;">置信度 ${(d.confidence * 100).toFixed(0)}%</span>`;
    }

    // 匹配理由
    if (d.matchReason) {
      html += `<div style="margin-top:6px;font-size:12px;color:#f59e0b;">匹配理由：${d.matchReason}</div>`;
    }

    // 定义
    if (d.definition) {
      html += `<div style="margin-top:6px;font-size:12px;color:#94a3b8;line-height:1.6;">${d.definition}</div>`;
    }

    // 前置知识
    if (d.prerequisites && d.prerequisites.length) {
      html += `<div style="margin-top:6px;font-size:12px;color:#94a3b8;">前置知识：${d.prerequisites.map(pid => {
        const pn = window.PBLPathBuilder?.unifiedIndex?.get(pid);
        return pn ? pn.name : pid;
      }).join('、')}</div>`;
    }

    // ─── 课标内容（curriculum_points，与 tree.html 同） ───
    const points = Array.isArray(d.curriculum_points) ? d.curriculum_points : [];
    if (points.length) {
      html += `<div style="margin-top:10px;padding:8px 10px;background:rgba(59,130,246,0.08);border-left:3px solid rgba(59,130,246,0.5);border-radius:4px;font-size:12px;">`;
      html += `<div style="font-weight:600;margin-bottom:6px;">📖 课标原文要点</div>`;
      points.forEach(p => {
        html += `<div style="margin:4px 0;padding:4px 6px;border-radius:4px;background:rgba(148,163,184,0.05);color:#94a3b8;line-height:1.5;">${this._escapeHtml(p)}</div>`;
      });
      html += `</div>`;
    }

    // ─── 课件列表（与 tree.html 同） ───
    if (hasAnyCourse) {
      html += `<div style="margin-top:8px;font-size:12px;color:#94a3b8;">已有课件：</div>`;
      html += `<div style="max-height:120px;overflow-y:auto;margin-top:4px;">`;

      // 通过 Hub 或直接 courses 字段
      const hubCourses = (window.TeachAnyHub && typeof TeachAnyHub.getAllCoursesForNode === 'function')
        ? TeachAnyHub.getAllCoursesForNode(d.id) : [];

      if (hubCourses.length > 0) {
        hubCourses.forEach(c => {
          const sourceIcon = { official: '📋', community_registry: '🔖', community_shared: '🌐', user: '📂' }[c.source] || '📚';
          const courseUrl = c.url || (c.path ? `./${c.path}/index.html` : '');
          if (courseUrl) {
            html += `<a href="${courseUrl}" target="_blank" onclick="event.stopPropagation();" style="display:flex;align-items:center;gap:6px;padding:6px 10px;margin:3px 0;border-radius:6px;font-size:13px;color:#f8fafc;text-decoration:none;background:rgba(148,163,184,0.08);pointer-events:auto;">${sourceIcon} 打开课件：${this._escapeHtml(c.name || c.id)}</a>`;
          }
        });
      } else if (window.TeachAnyHub && typeof TeachAnyHub.getResolvableTreeCourses === 'function') {
        const treeCourses = TeachAnyHub.getResolvableTreeCourses(d.courses || []);
        treeCourses.forEach(c => {
          const courseUrl = c.url || (c.path ? `./${c.path}/index.html` : '');
          if (!courseUrl) return;
          html += `<a href="${courseUrl}" target="_blank" onclick="event.stopPropagation();" style="display:flex;align-items:center;gap:6px;padding:6px 10px;margin:3px 0;border-radius:6px;font-size:13px;color:#f8fafc;text-decoration:none;background:rgba(148,163,184,0.08);pointer-events:auto;">📋 打开课件：${this._escapeHtml(c.name || c.id)}</a>`;
        });
      }
      html += `</div>`;
    }

    html += `<button type="button" data-pbl-make-course="${this._escapeHtml(d.id)}" style="display:block;width:100%;margin-top:10px;padding:8px 12px;border:none;border-radius:8px;background:linear-gradient(135deg,#10b981,#059669);color:white;font-size:13px;font-weight:700;cursor:pointer;pointer-events:auto;">✨ 制作新课件${d.isExternal ? '（项目补充）' : ''}</button>`;

    tooltip.innerHTML = html;
    tooltip.classList.add('visible');
    tooltip.style.opacity = '1';
    tooltip.style.pointerEvents = 'auto';

    this._positionTooltip(tooltip, container, event);
  }

  _moveTooltip(tooltip, container, event) {
    this._positionTooltip(tooltip, container, event);
  }

  _cancelTooltipHide() {
    if (this._tooltipHideTimer) {
      clearTimeout(this._tooltipHideTimer);
      this._tooltipHideTimer = null;
    }
  }

  _scheduleTooltipHide(delay = 350) {
    this._cancelTooltipHide();
    this._tooltipHideTimer = setTimeout(() => {
      if (this._tooltipHovered) return;
      const tooltip = document.querySelector('.pbl-tooltip');
      if (tooltip) this._hideTooltip(tooltip);
      this._tooltipHideTimer = null;
    }, delay);
  }

  _hideTooltip(tooltip) {
    this._cancelTooltipHide();
    tooltip.style.opacity = '0';
    tooltip.style.pointerEvents = 'none';
    tooltip.classList.remove('visible');
  }

  _positionTooltip(tooltip, container, event) {
    const rect = container.getBoundingClientRect();
    let x = event.clientX - rect.left + 12;
    let y = event.clientY - rect.top - 20;
    const tw = 290;
    const th = 200;
    if (x + tw > rect.width) x = x - tw - 56;
    if (y + th > rect.height) y = rect.height - th - 10;
    if (y < 10) y = 10;
    tooltip.style.left = x + 'px';
    tooltip.style.top = y + 'px';
  }

  // ─── 图例 ───

  _createLegend() {
    const legend = document.createElement('div');
    legend.style.cssText = 'display:flex;gap:16px;flex-wrap:wrap;padding:12px 16px;margin-bottom:12px;background:rgba(30,41,59,0.8);border-radius:10px;border:1px solid rgba(148,163,184,0.15);';

    const items = [
      { label: '实施顺序', color: this.colors.matched, dash: false, icon: '➡️' },
      { label: '基础前置', color: this.colors.prerequisite, dash: false, icon: '📝' },
      { label: '核心必需', color: this.colors.matched, dash: false, icon: '✅' },
      { label: '扩展高级', color: this.colors.advanced, dash: false, icon: '📝' },
      { label: '平行关联', color: this.colors.parallel, dash: true, icon: '📝' },
      { label: '外部补充', color: this.colors.external, dash: true, icon: '💡' },
      { label: '跨学科', color: '#f59e0b', dash: true, icon: '🔗' },
      { label: '大学延伸', color: this.colors.university, dash: true, icon: '🎓' }
    ];

    items.forEach(item => {
      const span = document.createElement('span');
      span.style.cssText = `display:flex;align-items:center;gap:6px;font-size:12px;color:#94a3b8;`;
      const dot = document.createElement('span');
      dot.style.cssText = `width:12px;height:12px;border-radius:50%;background:${item.color};opacity:0.8;display:flex;align-items:center;justify-content:center;font-size:8px;${item.dash ? 'border:1px dashed ' + item.color + ';background:transparent;' : ''}`;
      span.appendChild(dot);
      span.appendChild(document.createTextNode(item.label));
      legend.appendChild(span);
    });

    // 节点状态图例
    const statusLegend = document.createElement('span');
    statusLegend.style.cssText = 'display:flex;gap:12px;margin-left:16px;padding-left:16px;border-left:1px solid rgba(148,163,184,0.15);font-size:12px;color:#64748b;';
    statusLegend.innerHTML = '节点状态: ✅有课件 📝待创建 💡外部';
    legend.appendChild(statusLegend);

    return legend;
  }

  // ─── 工具方法 ───

  _metaLine(d) {
    return [d.curriculumLabel || d.systemLabel, d.stageLabel, d.gradeLabel, d.subject, d.domain]
      .filter(Boolean)
      .join(' · ');
  }

  _hubResolvableTreeCourses(courses) {
    return !!(window.TeachAnyHub && typeof TeachAnyHub.hasResolvableTreeCourses === 'function'
      && TeachAnyHub.hasResolvableTreeCourses(courses));
  }

  _nodeHasAnyCourse(d) {
    // 1. 标准节点：按 id 精确匹配
    if (!d.isExternal) {
      if (this._hubResolvableTreeCourses(d.courses)) return true;
      if (window.TeachAnyHub && typeof TeachAnyHub.getAllCoursesForNode === 'function') {
        if (TeachAnyHub.getAllCoursesForNode(d.id).length > 0) return true;
      }
      if (window.TeachAnyImporter && typeof TeachAnyImporter.getTopCoursesForTreeNode === 'function') {
        if (TeachAnyImporter.getTopCoursesForTreeNode(d.id).length > 0) return true;
      }
      return false;
    }
    // 2. 外部节点：先按 id 查（可能已挂入 user-generated 虚拟树），再按名称模糊匹配
    if (window.TeachAnyHub && typeof TeachAnyHub.getAllCoursesForNode === 'function') {
      if (TeachAnyHub.getAllCoursesForNode(d.id).length > 0) return true;
    }
    // 按名称搜索（外部节点的 name 可能匹配某个已有课件的标题关键词）
    if (d.name && window.TeachAnyHub && typeof TeachAnyHub.searchByKeyword === 'function') {
      const hits = TeachAnyHub.searchByKeyword(d.name);
      if (hits && hits.length > 0) return true;
    }
    return false;
  }

  /** 获取外部节点关联的课件列表（用于 tooltip 展示） */
  _getCoursesForNode(d) {
    const courses = [];
    if (window.TeachAnyHub && typeof TeachAnyHub.getAllCoursesForNode === 'function') {
      courses.push(...TeachAnyHub.getAllCoursesForNode(d.id));
    }
    // 外部节点：按名称搜索补充
    if (d.isExternal && d.name && window.TeachAnyHub && typeof TeachAnyHub.searchByKeyword === 'function') {
      const hits = TeachAnyHub.searchByKeyword(d.name);
      if (hits) {
        hits.forEach(h => {
          if (!courses.some(c => c.id === h.id)) courses.push(h);
        });
      }
    }
    if (window.TeachAnyImporter && typeof TeachAnyImporter.getTopCoursesForTreeNode === 'function') {
      const userCourses = TeachAnyImporter.getTopCoursesForTreeNode(d.id);
      userCourses.forEach(c => {
        if (!courses.some(ex => ex.id === c.id)) courses.push(c);
      });
    }
    return courses;
  }

  _dragStarted(event) {
    if (!event.active) this.simulation.alphaTarget(0.3).restart();
    event.subject.fx = event.subject.x;
    event.subject.fy = event.subject.y;
  }

  _dragged(event) {
    event.subject.fx = event.x;
    event.subject.fy = event.y;
  }

  _dragEnded(event) {
    if (!event.active) this.simulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
  }

  _truncate(str, maxLen) {
    if (!str) return '';
    return str.length > maxLen ? str.slice(0, maxLen) + '…' : str;
  }

  _hexToRgba(hex, alpha) {
    if (!hex || hex.charAt(0) !== '#') return `rgba(100,116,139,${alpha})`;
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r},${g},${b},${alpha})`;
  }

  _escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  highlightPathSteps(pathSteps) {
    const set = new Set((pathSteps || []).filter(Boolean));
    this._highlightSteps = set;
    if (!this.svg) return;
    const active = set.size > 0;
    this.svg.selectAll('.node-group').select('.node-circle')
      .attr('stroke-width', d => (active && set.has(d.pathStep) ? 4 : 2.5))
      .attr('opacity', d => (!active || set.has(d.pathStep) ? 1 : 0.28));
    this.svg.selectAll('.node-group').select('.node-label')
      .attr('opacity', d => (!active || set.has(d.pathStep) ? 1 : 0.35));
  }

  destroy() {
    if (this.simulation) this.simulation.stop();
    const container = document.getElementById(this.containerId);
    if (container) container.innerHTML = '';
    this.svg = null;
  }
}

// ─── 全局实例 ──────────────────────────────────────

window.PBLPathBuilder = new PBLPathBuilder();
window.PBLGraphRenderer = PBLGraphRenderer;

console.log('[TeachAny] PBL 学习路径构建器 v1.0 已加载');
