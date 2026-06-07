/**
 * @internal Bloom 认知层级推断 — 从 blueprint steps 推断项目上限，从节点名推断节点层级
 * 用于 filter 缩候选池、match 提示词约束
 */

const BLOOM_LEVELS = {
  remember: 1,
  understand: 2,
  apply: 3,
  analyze: 4,
  evaluate: 5,
  create: 6,
};

const BLOOM_VERB_PATTERNS = [
  { level: 'remember', re: /列举|识别|记忆|背诵|默写|说出|写出.*名称|认读|记住/ },
  { level: 'understand', re: /理解|解释|说明|描述|举例|概括|归纳|翻译|复述|阐述/ },
  { level: 'apply', re: /应用|运用|计算|测量|配制|绘制|操作|实施|完成|制作|搭建|安装|调试|录入|统计|求解|列式/ },
  { level: 'analyze', re: /分析|比较|对比|区分|分解|推断|探究|讨论|归因|解读|拆读/ },
  { level: 'evaluate', re: /评价|评判|论证|判断|选择.*方案|评估|鉴别|审阅|答辩|反思.*优劣/ },
  { level: 'create', re: /设计|创造|发明|创作|构建|开发|策划|编写.*程序|搭建.*系统|原创|编导/ },
];

const NODE_BLOOM_PATTERNS = [
  { level: 6, re: /设计|创造|发明|创作|构建|开发|原创|策划/ },
  { level: 5, re: /评价|评判|批判|论证|鉴赏|审美评价/ },
  { level: 4, re: /分析|探究|推理|证明|论证|比较|对比/ },
  { level: 3, re: /应用|运用|计算|测量|实验|操作|配制|求解|建模/ },
  { level: 2, re: /理解|解释|说明|认识|掌握.*概念|体会/ },
  { level: 1, re: /认识|记忆|列举|识记|背诵|了解.*基本/ },
];

/**
 * 从 blueprint 的 steps 推断项目 Bloom 上限
 * @param {object|null} blueprint
 * @returns {{ ceiling: number, ceilingLabel: string, evidence: string[], actionVerbs: string[] }}
 */
export function inferBloomFromBlueprint(blueprint) {
  const steps = [];
  const scheme = (blueprint?.schemes || []).find(s => s.id === blueprint?.recommendedSchemeId)
    || (blueprint?.schemes || [])[0];
  (scheme?.phases || []).forEach(p => {
    (p.steps || []).forEach(s => steps.push(String(s)));
  });
  if (!steps.length && blueprint?.deliverable) {
    steps.push(String(blueprint.deliverable));
  }

  let maxLevel = 3;
  const evidence = [];
  const actionVerbs = new Set();

  steps.forEach(step => {
    BLOOM_VERB_PATTERNS.forEach(({ level, re }) => {
      const m = step.match(re);
      if (m) {
        const lv = BLOOM_LEVELS[level];
        if (lv > maxLevel) maxLevel = lv;
        if (evidence.length < 6) evidence.push(step.slice(0, 60));
        m.forEach(v => actionVerbs.add(v));
      }
    });
  });

  const ceilingLabel = Object.entries(BLOOM_LEVELS).find(([, v]) => v === maxLevel)?.[0] || 'apply';
  return {
    ceiling: maxLevel,
    ceilingLabel,
    evidence: evidence.slice(0, 4),
    actionVerbs: [...actionVerbs].slice(0, 8),
  };
}

/**
 * 估算课标节点的 Bloom 层级（1–6）
 * @param {object} node
 */
export function scoreNodeBloomLevel(node) {
  const text = [node.name, node.definition, ...(node.key_concepts || []), ...(node.curriculum_points || [])]
    .filter(Boolean).join(' ');
  let level = 2;
  NODE_BLOOM_PATTERNS.forEach(({ level: lv, re }) => {
    if (re.test(text) && lv > level) level = lv;
  });
  if (/实验|探究|验证|测量/.test(text)) level = Math.max(level, 3);
  if (/设计.*方案|工程设计|发明/.test(text)) level = Math.max(level, 6);
  return level;
}

/** 节点是否超出项目 Bloom 上限（允许 +1 容差） */
export function isNodeAboveBloomCeiling(node, ceiling) {
  if (!ceiling || ceiling >= 6) return false;
  const nodeLevel = scoreNodeBloomLevel(node);
  return nodeLevel > ceiling + 1;
}

export function bloomCeilingLabel(ceiling) {
  const map = { 1: '记忆', 2: '理解', 3: '应用', 4: '分析', 5: '评价', 6: '创造' };
  return map[ceiling] || '应用';
}

export function formatBloomHintForMatch(bloomProfile) {
  if (!bloomProfile?.ceiling) return '';
  const label = bloomCeilingLabel(bloomProfile.ceiling);
  const ev = (bloomProfile.evidence || []).map(s => `「${s}」`).join('、');
  return `
【Bloom 认知层级约束】
- 从蓝图任务推断，本项目认知上限约为「${label}」（level ${bloomProfile.ceiling}）
- 依据：${ev || '蓝图阶段任务动词'}
- **禁止** matched 需要「评价/创造」才能完成的节点，除非蓝图明确出现设计/评价/创造类动词
- 优先选择「应用/分析」级别的工具性课标节点`;
}

export function formatBloomHintForFilter(bloomProfile) {
  if (!bloomProfile?.ceiling) return '';
  return `
【Bloom 预分析（供你确认）】
- 规则推断认知上限：${bloomCeilingLabel(bloomProfile.ceiling)}（${bloomProfile.ceiling}）
- 请在 JSON 中返回 bloomCeiling（1-6 整数）、bloomEvidence（2-4 条）、actionVerbs（动词列表）`;
}
