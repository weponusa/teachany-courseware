/**
 * @internal 服务端项目原型解析（与 data/pbl/*.json 逻辑对齐）
 */
import archetypeData from '../../data/pbl/archetypes.json' with { type: 'json' };
import registryData from '../../data/pbl/engineering-registry.json' with { type: 'json' };

function norm(s) {
  return String(s || '').trim();
}

function textOf(node) {
  return `${node.name || ''} ${node.definition || ''}`;
}

export function resolveArchetype(goal, projectType, isMixedChemistry) {
  const g = norm(goal);
  for (const a of archetypeData.archetypes || []) {
    if ((a.matchPatterns || []).some(p => new RegExp(p, 'i').test(g))) return a;
  }
  if (isMixedChemistry) {
    return archetypeData.archetypes.find(x => x.id === 'mixed-solution-chemistry') || null;
  }
  const fb = archetypeData.typeFallback?.[projectType];
  if (fb) return archetypeData.archetypes.find(x => x.id === fb) || null;
  return null;
}

export function formatArchetypeForMatch(archetype, blueprint) {
  if (!archetype) return '';
  const scheme = (blueprint?.schemes || []).find(s => s.id === blueprint?.recommendedSchemeId)
    || (blueprint?.schemes || [])[0];
  const phaseModules = (scheme?.phases || []).map((p, i) => {
    const mid = p.subsystemIds?.[0] || '';
    const mod = (archetype.modules || []).find(m => m.id === mid);
    return `  ${i + 1}. 模块【${mod?.label || mid || p.phase}】检索词：${(p.knowledgeHints || []).join('、')}`;
  }).join('\n');
  const bans = (archetype.banNamePatterns || []).slice(0, 8).join('、');
  const chinese = archetype.chineseAllowPatterns?.length
    ? `语文仅允许：${archetype.chineseAllowPatterns.join('、')}`
    : '';
  return `
【项目原型：${archetype.label}（${archetype.id}）— 硬性约束】
- 主课标体系：${archetype.primarySystem || 'cn'}（优先 CN 节点，AP/IB 仅作拓展）
- 学段：${(archetype.gradeBand || []).join('-')}，最低 grade ${archetype.minGrade || 7}
- 学科：${(archetype.subjects || []).join('、')}
- 禁止 matched 名称含：${bans}
${chinese ? `- ${chinese}` : ''}
- 每个模块至少 1 个 matched，reason 必须以本原型模块名开头（如「模块：成本测算。」），**禁止**用科学探究套话（问题与假设/变量设计）
- matched 总数 ${archetype.minMatched || 5}-${archetype.maxMatched || 12}，禁止为凑学科选无关节点
${phaseModules ? `蓝图模块对齐：\n${phaseModules}` : ''}`;
}

export function getRegistryEntries(archetypeId, moduleIds = []) {
  return (registryData.entries || []).filter(e =>
    (e.archetypes || []).includes(archetypeId)
    && (!moduleIds.length || !e.moduleId || moduleIds.includes(e.moduleId))
  );
}

export function formatRegistryForMatch(archetypeId) {
  const entries = getRegistryEntries(archetypeId);
  if (!entries.length) return '';
  const lines = entries.slice(0, 6).map(e =>
    `- [${e.moduleId}] ${e.name}：${e.reason}`
  ).join('\n');
  return `\n【推荐课标外补充（优先从下列选用，须绑定模块）】\n${lines}`;
}

export { archetypeData, registryData };
