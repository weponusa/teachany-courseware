#!/usr/bin/env node
/**
 * 本地向量召回烟测 — 不依赖 API / 浏览器
 * node scripts/pbl-vector-recall-test.mjs [--case=car-cost|fungus-dye]
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, '..');
const CASE = process.argv.find(a => a.startsWith('--case='))?.split('=')[1] || 'car-cost';

function loadJson(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

function walkTrees(dir, system, nodes) {
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
            });
          }
        }
      } catch { /* skip */ }
    }
  }
}

function localHashEmbed(text, dim = 512) {
  const vec = new Array(dim).fill(0);
  const tokens = String(text || '').match(/[\u4e00-\u9fa5a-zA-Z0-9]{2,12}/g) || [];
  for (const t of tokens) {
    let h = 2166136261;
    for (let i = 0; i < t.length; i++) {
      h ^= t.charCodeAt(i);
      h = Math.imul(h, 16777619);
    }
    for (let k = 0; k < 5; k++) {
      const idx = Math.abs((h + k * 2654435761) % dim);
      vec[idx] += 1;
    }
  }
  const norm = Math.sqrt(vec.reduce((s, v) => s + v * v, 0)) || 1;
  return vec.map(v => v / norm);
}

function scoreOverlap(node, goal, blueprint) {
  const terms = new Set();
  String(goal || '').match(/[\u4e00-\u9fa5]{2,8}/g)?.forEach(t => terms.add(t));
  (blueprint?.schemes?.[0]?.phases || []).forEach(p => {
    (p.knowledgeHints || []).forEach(h => terms.add(h));
    String(p.phase || '').match(/[\u4e00-\u9fa5]{2,8}/g)?.forEach(t => terms.add(t));
  });
  const text = `${node.name} ${(node.curriculum_points || []).join(' ')}`;
  const name = String(node.name || '');
  let hit = 0;
  let max = 0;
  terms.forEach(t => {
    if (!t || t.length < 2) return;
    max += 3;
    if (name.includes(t)) hit += 3;
    else if (text.includes(t)) hit += 1;
  });
  return max > 0 ? hit / max : 0;
}

function cosine(a, b) {
  let dot = 0;
  let na = 0;
  let nb = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    na += a[i] * a[i];
    nb += b[i] * b[i];
  }
  const d = Math.sqrt(na) * Math.sqrt(nb);
  return d > 0 ? dot / d : -1;
}

function buildVectorQuery(goal, blueprint) {
  const scheme = blueprint?.schemes?.find(s => s.id === blueprint.recommendedSchemeId)
    || blueprint?.schemes?.[0];
  const parts = [`项目目标：${goal}`];
  (scheme?.phases || []).forEach((p, i) => {
    const steps = (p.steps || []).slice(0, 3).join('；');
    const hints = (p.knowledgeHints || []).join('、');
    parts.push(`阶段${i + 1}·${p.phase || ''}：${steps}`);
    if (hints) parts.push(`检索：${hints}`);
  });
  return parts.join('\n');
}

const FIXTURES = {
  'car-cost': {
    goal: '探究新能源汽车与传统燃油汽车的成本效益分析',
    blueprint: {
      recommendedSchemeId: 'A',
      schemes: [{
        id: 'A',
        phases: [
          { phase: '需求调研', steps: ['家庭出行里程与充电条件', '预算与使用场景问卷'], knowledgeHints: ['统计', '调查', '数据收集'] },
          { phase: '对比指标', steps: ['油耗/电耗、保养、保险、残值'], knowledgeHints: ['百分数', '函数', '图表'] },
          { phase: '科学原理', steps: ['内燃机热效率与排放', '电机与电池基础'], knowledgeHints: ['热机', '能量转化', '环境'] },
          { phase: '全成本测算', steps: ['TCO 模型与假设', '五年用车成本对比'], knowledgeHints: ['统计', '运算', '论证'] },
          { phase: '购车建议', steps: ['方案比选与报告'], knowledgeHints: ['说明文', '论证', '决策'] },
        ],
      }],
    },
    expectAny: ['统计', '函数', '百分', '热', '环境', '调查', '说明', '图表', '数据'],
  },
  'fungus-dye': {
    goal: '利用食用菌菌丝体降解染料的对照实验研究',
    blueprint: {
      recommendedSchemeId: 'A',
      schemes: [{
        id: 'A',
        phases: [
          { phase: '问题界定', steps: ['染料污染背景', '菌丝体降解假说'], knowledgeHints: ['环境', '生态'] },
          { phase: '实验设计', steps: ['对照组设置', '变量控制', '重复次数'], knowledgeHints: ['对照实验', '变量', '科学探究'] },
          { phase: '数据采集', steps: ['降解率测定', '记录表设计'], knowledgeHints: ['数据', '图表', '百分'] },
          { phase: '分析与结论', steps: ['误差讨论', '结论与建议'], knowledgeHints: ['论证', '生物', '化学'] },
        ],
      }],
    },
    expectAny: ['实验', '对照', '生物', '化学', '环境', '数据', '探究', '生态'],
  },
};

const fixture = FIXTURES[CASE];
if (!fixture) {
  console.error('Unknown case:', CASE);
  process.exit(1);
}

const emb = loadJson(path.join(ROOT, 'data/pbl/node-embeddings.json'));
const map = new Map((emb.nodes || []).map(({ id, e }) => [id, e]));
const dim = emb.dim || 512;

const allNodes = [];
walkTrees(path.join(ROOT, 'data/trees/cn'), 'cn', allNodes);
const pool = allNodes.filter(n => n.grade >= 7 && n.grade <= 12);

const query = buildVectorQuery(fixture.goal, fixture.blueprint);
const qVec = localHashEmbed(query, dim);

const scored = [];
for (const n of pool) {
  const e = map.get(n.id);
  if (!e || e.length !== qVec.length) continue;
  const cos = cosine(qVec, e);
  const lex = scoreOverlap(n, fixture.goal, fixture.blueprint);
  const s = cos * 0.25 + lex * 0.75;
  if (s > 0.08) scored.push({ ...n, score: s });
}
scored.sort((a, b) => b.score - a.score);
const top = scored.slice(0, 20);

console.log(`\n=== 向量召回烟测: ${CASE} ===`);
console.log(`索引: ${map.size} 节点, model=${emb.model}, pool=${pool.length}`);
console.log(`Query 片段: ${query.slice(0, 120)}…\n`);
console.log('Top 20:');
top.forEach((n, i) => {
  console.log(`  ${String(i + 1).padStart(2)}. [${n.subject} G${n.grade}] ${n.name} (${(n.score * 100).toFixed(1)}%)`);
});

const hit = top.some(n => fixture.expectAny.some(k => n.name.includes(k)));
console.log(`\n期望关键词命中 top20: ${hit ? '✅' : '❌'}`);
process.exit(hit ? 0 : 1);
