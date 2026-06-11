#!/usr/bin/env node
/**
 * PBL 原型层全量 benchmark 自测 — 本地候选检索 + 可选线上 match
 * Usage: node scripts/pbl-self-test.mjs [--live] [--id=water-rocket] [--suite=gold|cross|all]
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { inferTopicKnowledgeAnchors, scoreNodeAgainstAnchors } from '../functions/_lib/pbl-topic-anchors.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, '..');
const LIVE = process.argv.includes('--live');
const ID_FILTER = process.argv.find(a => a.startsWith('--id='))?.split('=')[1];
const SUITE = process.argv.find(a => a.startsWith('--suite='))?.split('=')[1] || 'gold';
const API = 'https://www.teachany.cn/api/pbl/analyze';

function loadJson(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

function walkTrees(dir, system, nodes) {
  if (!fs.existsSync(dir)) return;
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, ent.name);
    if (ent.isDirectory()) walkTrees(full, system, nodes);
    else if (ent.name.endsWith('.json') && ent.name !== '_template.json') {
      try {
        const tree = loadJson(full);
        const subject = tree.subject || 'unknown';
        for (const domain of tree.domains || []) {
          for (const n of domain.nodes || []) {
            nodes.push({
              id: n.id,
              name: n.name,
              subject,
              system,
              grade: n.grade || 0,
              definition: (n.curriculum_points || []).join(' ').slice(0, 200),
              prerequisites: n.prerequisites || [],
            });
          }
        }
      } catch (e) { /* skip */ }
    }
  }
}

function buildCnIndex() {
  const nodes = [];
  walkTrees(path.join(ROOT, 'data/trees/cn'), 'cn', nodes);
  return nodes;
}

function blueprintFixture(c, archetypeData) {
  if (c.blueprint) return c.blueprint;
  const a = (archetypeData.archetypes || []).find(x => x.id === c.archetypeId);
  if (!a?.modules?.length) return { subsystems: [], knowledgeChain: '' };
  return {
    knowledgeChain: a.modules.map(m => m.label).join(' → '),
    subsystems: a.modules.map(m => ({ id: m.id, name: m.label, keywords: m.hints || [] })),
    schemes: [{
      id: 'A',
      phases: a.modules.map(m => ({
        phase: m.label,
        subsystemIds: [m.id],
        knowledgeHints: m.hints || [],
      })),
    }],
    recommendedSchemeId: 'A',
  };
}

function blueprintModules(blueprint) {
  const subs = blueprint?.subsystems || [];
  if (subs.length) {
    return subs.map((s, i) => ({
      id: s.id || `sub-${i}`,
      label: s.name || s.id,
      hints: [...(s.keywords || []), s.name].filter(Boolean),
      subjects: s.subjects || [],
      topK: 2,
    }));
  }
  return [];
}

function isGloballyBanned(node, tagsData) {
  const name = String(node.name || '');
  return (tagsData.globalBanNames || []).some(b => name.includes(b));
}

function isBanned(node, archetype, tagsData) {
  if (isGloballyBanned(node, tagsData)) return true;
  if (!archetype) return false;
  const minG = archetype?.minGrade || 4;
  const t = `${node.name} ${node.definition || ''}`;
  if (minG >= 4) {
    for (const p of tagsData.elementaryBanPatterns || []) {
      if (node.name.includes(p) || t.includes(p)) return true;
    }
  }
  for (const p of archetype.banNamePatterns || []) {
    try {
      if (new RegExp(p).test(node.name) || new RegExp(p).test(t)) return true;
    } catch {
      if (node.name.includes(p)) return true;
    }
  }
  if (node.subject === 'chinese' && archetype.chineseBanPatterns?.length) {
    if (archetype.chineseBanPatterns.some(p => t.includes(p))) return true;
    if (archetype.chineseAllowPatterns?.length) {
      return !archetype.chineseAllowPatterns.some(p => t.includes(p));
    }
  }
  for (const rule of tagsData.writingRules || []) {
    if (!node.name.includes(rule.match)) continue;
    if (rule.banArchetypes?.includes(archetype.id)) return true;
    if (rule.allowArchetypes?.length && !rule.allowArchetypes.includes(archetype.id)) return true;
  }
  return false;
}

function moduleNodeOk(archetype, mod, node, goal = '') {
  if (!archetype) return true;
  const t = `${node.name} ${node.definition || ''}`;
  if (archetype.id === 'mixed-solution-chemistry') {
    if (mod.id === 'conductivity' && node.subject === 'physics') return false;
    if (mod.id === 'titration' && node.subject === 'chemistry' && !/滴定|硝酸银|沉淀|物质的量|离子|摩尔/.test(t)) return false;
  }
  if (archetype.id === 'water-rocket' && mod.id === 'test' && node.subject === 'info-tech') return false;
  if (archetype.id === 'environmental-filtration' && /火箭|反冲|抛体|弹道|发射/.test(node.name)) return false;
  if (archetype.id === 'environmental-filtration' && /^(prefilter|membrane|filtration)$/.test(mod.id) && !/过滤|沉淀|吸附|溶液|颗粒|环境|污染|实验|孔径|膜|陶瓷|滤网/.test(t)) return false;
  if (archetype.id === 'application-writing' && /诗词|文言|小说|人物描写/.test(node.name)) return false;
  if (archetype.id === 'labor-practice' && /朝花夕拾|整本书阅读|文言|外国文学|机械玩具|机器人|电学实验|线性规划|三角函数/.test(node.name)) return false;
  if (archetype.id === 'planting-cultivation') {
    if (/朝花夕拾|文言|外国文学|机械玩具|机器人|程序设计|牛顿|化学方程式|电解池/.test(node.name)) return false;
    if (mod.id === 'taxonomy' && !/植物|绿色|分类|种子|动物|生物/.test(t)) return false;
    if (mod.id === 'growth' && !/光合|萌发|生长|种子|根|蒸腾|绿色|植物|呼吸/.test(t)) return false;
  }
  if (archetype.id === 'maker-engineering') {
    if (/有机合成|有机化合物|烃|离子检验|醇|酚|醛|酮|羧酸|细胞膜|原子结构|化学平衡|生态系统结构|生物膜/.test(node.name)) return false;
    if (node.subject === 'biology' && !/纸桥|植物|生物|生态/.test(goal)) return false;
    if (mod.id === 'design' && !/结构|受力|压强|摩擦|平衡|材料|设计|制作|实验|测量|力|杠杆|机械|桥梁|承重/.test(t)) return false;
    if (mod.id === 'build' && !/制作|组装|电路|结构|材料|加工|搭建|实验|机械|桥/.test(t)) return false;
    if (mod.id === 'test' && !/测试|测量|实验|数据|误差|记录|统计|力|压强/.test(t)) return false;
  }
  return true;
}

function scoreModule(node, mod, goal, archetype, caseMinGrade = 1) {
  let s = 0;
  const t = `${node.name} ${node.definition || ''}`.toLowerCase();
  const name = node.name.toLowerCase();
  for (const h of mod.hints || []) {
    const k = h.toLowerCase();
    if (name.includes(k)) s += 8;
    else if (t.includes(k)) s += 4;
  }
  if ((mod.subjects || []).includes(node.subject)) s += 3;
  if (goal.includes('成本') && /成本|费用|统计|百分|函数/.test(t)) s += 3;
  for (const p of archetype?.preferNamePatterns || []) {
    if (node.name.includes(p)) s += 6;
  }
  const anchors = inferTopicKnowledgeAnchors(goal);
  s += scoreNodeAgainstAnchors(node, anchors);
  const minG = Math.max(archetype?.minGrade || 1, caseMinGrade || 1);
  const grade = parseInt(node.grade, 10) || 0;
  if (grade > 0 && grade < minG) s -= 24;
  else if (grade > 0 && grade >= minG) s += Math.min(6, grade - minG);
  return s;
}

function pickByBlueprint(pool, blueprint, goal, tagsData, archetype = null, max = 24, caseMinGrade = 1) {
  const modules = blueprintModules(blueprint);
  const picked = [];
  const seen = new Set();
  for (const mod of modules) {
    const floorGrade = Math.max(archetype?.minGrade || 1, caseMinGrade || 1);
    const ranked = pool
      .filter(n => !seen.has(n.id))
      .filter(n => !isBanned(n, archetype, tagsData))
      .filter(n => (parseInt(n.grade, 10) || 0) >= floorGrade || !n.grade)
      .filter(n => !mod.subjects?.length || mod.subjects.includes(n.subject))
      .filter(n => moduleNodeOk(archetype, mod, n, goal))
      .map(n => ({ n, s: scoreModule(n, mod, goal, archetype, caseMinGrade) }))
      .filter(x => x.s > 0)
      .sort((a, b) => b.s - a.s);
    ranked.slice(0, mod.topK || 2).forEach(x => {
      seen.add(x.n.id);
      picked.push({ ...x.n, _module: mod.id, _score: x.s });
    });
  }
  return picked.slice(0, max);
}

async function callApi(stage, body) {
  const resp = await fetch(API, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const text = await resp.text();
  let data;
  try { data = JSON.parse(text); } catch { throw new Error(`HTTP ${resp.status}: ${text.slice(0, 120)}`); }
  if (!resp.ok) throw new Error(data.error || String(resp.status));
  return data.content;
}

function extractJson(text) {
  const m = text.match(/\{[\s\S]*\}/);
  if (!m) throw new Error('no json');
  return JSON.parse(m[0]);
}

function toRegex(arr) {
  return (arr || []).map(s => (s instanceof RegExp ? s : new RegExp(s)));
}

function evaluate(caseDef, picked, archetype) {
  const issues = [];
  const names = picked.map(n => n.name);
  for (const re of toRegex(caseDef.forbidNames)) {
    const hit = names.filter(n => re.test(n));
    if (hit.length) issues.push(`禁止节点命中: ${hit.join('、')}`);
  }
  if (caseDef.requireSubjects) {
    const subs = new Set(picked.map(n => n.subject));
    for (const s of caseDef.requireSubjects) {
      if (!subs.has(s)) issues.push(`缺少学科: ${s}`);
    }
  }
  if (caseDef.requireAnyName) {
    const ok = names.some(n => toRegex(caseDef.requireAnyName).some(re => re.test(n)));
    if (!ok) issues.push('缺少预期关键词节点');
  }
  const minG = caseDef.minGrade || archetype.minGrade || 1;
  const lowGrade = picked.filter(n => (parseInt(n.grade, 10) || 0) > 0 && (parseInt(n.grade, 10) || 0) < minG);
  if (lowGrade.length) issues.push(`学段过低: ${lowGrade.map(n => n.name).join('、')}`);
  const minM = caseDef.minMatched || archetype.minMatched || 4;
  if (picked.length < minM) issues.push(`节点过少: ${picked.length} < ${minM}`);
  return issues;
}

async function liveMatch(caseDef, candidates, archetype) {
  const content = await callApi('match', {
    goal: caseDef.goal,
    candidates: candidates.map(n => ({
      name: n.name, grade: n.grade, subject: n.subject, systemTag: 'CN',
      definition: n.definition, prerequisiteNames: [],
    })),
    complex: true,
    maxMatched: archetype.maxMatched || 12,
    minConf: 0.55,
    archetypeId: archetype.id,
    projectBlueprint: {
      deliverable: '测试交付物',
      schemes: [{ id: 'A', name: 'A', phases: archetype.modules.map(m => ({
        phase: m.label, subsystemIds: [m.id], knowledgeHints: m.hints,
        steps: [`完成${m.label}具体任务：记录数据并提交${m.label}成果`], deliverable: m.label,
      })) }],
      recommendedSchemeId: 'A',
    },
  });
  const result = extractJson(content);
  const matched = (result.matched || []).map(m => {
    const idx = m.index ?? m.nodeIndex;
    return candidates[idx];
  }).filter(Boolean);
  return matched.map(n => n.name);
}

function loadCases() {
  const gold = loadJson(path.join(ROOT, 'data/pbl/benchmark-seed.json')).cases || [];
  const cross = loadJson(path.join(ROOT, 'data/pbl/cross-discipline-seed.json')).cases || [];
  let cases = [];
  if (SUITE === 'cross') cases = cross;
  else if (SUITE === 'all') cases = [...gold, ...cross];
  else cases = gold;
  return cases.filter(c => !ID_FILTER || c.id === ID_FILTER);
}

async function main() {
  const archetypeData = loadJson(path.join(ROOT, 'data/pbl/archetypes.json'));
  const registry = loadJson(path.join(ROOT, 'data/pbl/engineering-registry.json'));
  const tagsData = loadJson(path.join(ROOT, 'data/pbl/node-pbl-tags.json'));
  const cases = loadCases();
  const allNodes = buildCnIndex();

  console.log(`CN 索引: ${allNodes.length} 节点`);
  console.log(`Benchmark[${SUITE}]: ${cases.length} 用例${LIVE ? ' (+线上 match)' : ''}\n`);

  let failCount = 0;
  const summary = [];

  for (const c of cases) {
    const blueprint = blueprintFixture(c, archetypeData);
    const archetype = (archetypeData.archetypes || []).find(x => x.id === c.archetypeId) || null;
    const floorGrade = Math.max(archetype?.minGrade || 1, c.minGrade || 1);
    const pool = allNodes.filter(n => {
      if ((parseInt(n.grade, 10) || 0) > 0 && (parseInt(n.grade, 10) || 0) < floorGrade) return false;
      return !isBanned(n, archetype, tagsData);
    });
    const picked = pickByBlueprint(pool, blueprint, c.goal, tagsData, archetype, 24, c.minGrade || 1);
    const issues = evaluate(c, picked, archetype);
    const ext = archetype
      ? (registry.entries || []).filter(e => e.archetypes?.includes(archetype.id))
      : [];

    console.log(`── ${c.id} ──`);
    console.log(`  蓝图模块: ${blueprintModules(blueprint).map(m => m.label).join(' → ') || '—'}`);
    console.log(`  本地检索(${picked.length}): ${picked.map(n => `${n.name}(${n.subject},G${n.grade})`).join(' | ')}`);
    console.log(`  课外(${ext.length}): ${ext.slice(0, 2).map(e => e.name).join(' | ')}`);

    if (LIVE && picked.length >= 4) {
      try {
        console.log('  (线上 match…)');
        const liveNames = await liveMatch(c, picked, archetype);
        console.log(`  线上match: ${liveNames.join(' | ')}`);
        for (const re of toRegex(c.forbidNames)) {
          const hit = liveNames.filter(n => re.test(n));
          if (hit.length) issues.push(`线上禁止命中: ${hit.join('、')}`);
        }
      } catch (e) {
        issues.push(`线上match失败: ${e.message}`);
      }
    }

    if (issues.length) {
      console.log(`  ❌ ${issues.join('; ')}`);
      failCount++;
      summary.push({ id: c.id, ok: false, issues });
    } else {
      console.log('  ✅ 通过');
      summary.push({ id: c.id, ok: true });
    }
    console.log('');
  }

  const passed = summary.filter(s => s.ok).length;
  console.log(`══ 结果: ${passed}/${cases.length} 通过${failCount ? `, ${failCount} 失败` : ''} ══`);
  process.exit(failCount > 0 ? 1 : 0);
}

main().catch(e => { console.error(e); process.exit(2); });
