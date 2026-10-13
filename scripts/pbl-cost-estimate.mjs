#!/usr/bin/env node
/**
 * 估算单次 PBL 拆解的 OpenRouter token 成本
 * 用法: OPENROUTER_KEY=sk-or-... node scripts/pbl-cost-estimate.mjs [--goal=shopping|canteen]
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const PBL_API = 'https://www.teachany.cn/api/pbl/analyze';
const MODEL = 'qwen/qwen3-next-80b-a3b-instruct';
const PRICE_IN = 0.09 / 1e6;   // $/token
const PRICE_OUT = 0.0011 / 1e6;

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, '..');

function loadKey() {
  if (process.env.OPENROUTER_KEY) return process.env.OPENROUTER_KEY;
  const s = fs.readFileSync(path.join(ROOT, 'scripts/ai-tutor.js'), 'utf8');
  const m = s.match(/const _k1 = '([^']+)';\s*const _k2 = '([^']+)';\s*const _k3 = '([^']+)';\s*const _k4 = '([^']+)'/);
  return m ? m[1] + m[2] + m[3] + m[4] : '';
}

const GOALS = {
  shopping: {
    goal: '模拟小卖部购物场景，用人民币学具完成付款和找零，制作购物小票',
    complex: false,
  },
  canteen: {
    goal: '食堂菜汤的盐含量测定，比较滴定法与电导率法并撰写报告',
    complex: true,
  },
};

const STAGE_OPTS = {
  decompose: { maxTokens: 4500, temperature: 0.35 },
  filter: { maxTokens: 1200, temperature: 0.25 },
  'propose-curriculum': { maxTokens: 3000, temperature: 0.25 },
  'validate-match': { maxTokens: 6000, temperature: 0.1 },
  'verify-relevance': { maxTokens: 3000, temperature: 0.05 },
  'verify-deps': { maxTokens: 2500, temperature: 0.08 },
};

const MOCK_LINKED = [
  { index: 0, id: 'cn-math-g1-add', name: '100以内加减法', subject: 'math', grade: 1, role: 'foundation', reason: '付款找零' },
  { index: 1, id: 'cn-math-g1-money', name: '认识人民币', subject: 'math', grade: 1, role: 'core', reason: '学具付款' },
  { index: 2, id: 'cn-chinese-g2-note', name: '应用文写作', subject: 'chinese', grade: 2, role: 'bridge', reason: '购物小票' },
  { index: 3, id: 'cn-math-g2-chart', name: '象形统计图', subject: 'math', grade: 2, role: 'core', reason: '销售记录' },
  { index: 4, id: 'cn-math-g1-mult', name: '表内乘法', subject: 'math', grade: 2, role: 'foundation', reason: '数量计算' },
];

async function fetchMessages(stage, body) {
  const resp = await fetch(PBL_API, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ stage, messagesOnly: true, ...body }),
  });
  const data = await resp.json();
  if (!resp.ok) throw new Error(data.error || `messagesOnly ${resp.status}`);
  return data.messages;
}

async function callOR(messages, stage) {
  const opts = STAGE_OPTS[stage];
  const resp = await fetch('https://openrouter.ai/api/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${loadKey()}`,
      'HTTP-Referer': 'https://www.teachany.cn',
      'X-Title': 'TeachAny-PBL-Cost',
    },
    body: JSON.stringify({ model: MODEL, messages, stream: false, ...opts }),
  });
  const data = await resp.json().catch(() => ({}));
  if (!resp.ok) throw new Error(`${resp.status} ${JSON.stringify(data).slice(0, 200)}`);
  const content = data.choices?.[0]?.message?.content || '';
  return { usage: data.usage || {}, content };
}

function buildStageBodies(goalDef, blueprint) {
  const { goal, complex } = goalDef;
  const summaryList = 'math: 100以内加减法\nmath: 认识人民币\nchinese: 应用文\nmath: 象形统计图';
  const bloomProfile = { bloomCeiling: 3, subjects: ['math', 'chinese'], grades: [1, 2] };
  const matchedLite = MOCK_LINKED.map(n => ({ id: n.id, name: n.name, subject: n.subject, grade: n.grade, matchReason: n.reason }));
  return {
    decompose: { goal, complex },
    filter: { goal, complex, summaryList, projectBlueprint: blueprint, bloomProfile },
    'propose-curriculum': { goal, complex, projectBlueprint: blueprint, deliverable: blueprint.deliverable, maxProposed: 10 },
    'validate-match': { goal, complex, linked: MOCK_LINKED, projectBlueprint: blueprint, bloomProfile },
    'verify-relevance': { goal, complex, matched: matchedLite, projectBlueprint: blueprint },
    'verify-deps': {
      goal, complex,
      matched: matchedLite,
      edges: MOCK_LINKED.slice(1).map((n, i) => ({ source: MOCK_LINKED[i].id, target: n.id, type: 'depends-on' })),
      rawMatchResult: { pathOrder: [0, 1, 2, 3, 4] },
    },
  };
}

async function main() {
  const key = loadKey();
  if (!key) { console.error('需要 OPENROUTER_KEY'); process.exit(1); }

  const goalKey = (process.argv.find(a => a.startsWith('--goal=')) || '--goal=shopping').slice(7);
  const goalDef = GOALS[goalKey] || GOALS.shopping;

  console.log(`PBL 成本估算 | ${MODEL} | goal=${goalKey}\n`);

  const bodies = buildStageBodies(goalDef, {
    deliverable: '项目交付物',
    schemes: [{ phases: [{ phase: '调研', knowledgeHints: ['调查', '人民币'], steps: ['设计问卷', '收集数据'] }] }],
  });
  const rows = [];
  let totalIn = 0; let totalOut = 0; let totalUsd = 0;

  // 先跑 decompose 拿真实 blueprint，供后续阶段使用
  {
    const stage = 'decompose';
    process.stdout.write(`${stage} ... `);
    const messages = await fetchMessages(stage, bodies[stage]);
    const t0 = Date.now();
    const r = await callOR(messages, stage);
    const ms = Date.now() - t0;
    const pin = r.usage.prompt_tokens || 0;
    const pout = r.usage.completion_tokens || 0;
    const usd = pin * PRICE_IN + pout * PRICE_OUT;
    totalIn += pin; totalOut += pout; totalUsd += usd;
    rows.push({ stage, prompt_tokens: pin, completion_tokens: pout, total_tokens: pin + pout, usd, ms });
    console.log(`in=${pin} out=${pout} $${usd.toFixed(5)} ${(ms / 1000).toFixed(1)}s`);
    try {
      const text = r.content || '';
      const start = text.indexOf('{'); const end = text.lastIndexOf('}');
      const bp = JSON.parse(text.slice(start, end + 1));
      Object.assign(bodies, buildStageBodies(goalDef, bp));
    } catch { /* 保留 mock blueprint */ }
    await new Promise(res => setTimeout(res, 1500));
  }

  for (const stage of Object.keys(STAGE_OPTS).filter(s => s !== 'decompose')) {
    process.stdout.write(`${stage} ... `);
    const messages = await fetchMessages(stage, bodies[stage]);
    const t0 = Date.now();
    const r = await callOR(messages, stage);
    const ms = Date.now() - t0;
    const u = r.usage;
    const pin = u.prompt_tokens || 0;
    const pout = u.completion_tokens || 0;
    const usd = pin * PRICE_IN + pout * PRICE_OUT;
    totalIn += pin; totalOut += pout; totalUsd += usd;
    rows.push({ stage, prompt_tokens: pin, completion_tokens: pout, total_tokens: pin + pout, usd, ms });
    console.log(`in=${pin} out=${pout} $${usd.toFixed(5)} ${(ms / 1000).toFixed(1)}s`);
    await new Promise(res => setTimeout(res, 1500));
  }

  const cny = totalUsd * 7.25;
  console.log('\n========== 单次完整拆解（6 阶段）==========');
  console.log(`Input  合计: ${totalIn.toLocaleString()} tokens`);
  console.log(`Output 合计: ${totalOut.toLocaleString()} tokens`);
  console.log(`Total  合计: ${(totalIn + totalOut).toLocaleString()} tokens`);
  console.log(`成本（USD）: $${totalUsd.toFixed(4)}`);
  console.log(`成本（CNY≈）: ¥${cny.toFixed(3)}（按 7.25 汇率）`);
  console.log(`日均 100 次: ¥${(cny * 100).toFixed(1)}`);
  console.log(`月均 3000 次: ¥${(cny * 3000).toFixed(0)}`);

  const out = path.join(ROOT, 'data/pbl-iterate/pbl-cost-estimate.json');
  fs.writeFileSync(out, JSON.stringify({
    generatedAt: new Date().toISOString(),
    model: MODEL,
    goal: goalKey,
    pricePer1M: { input: 0.09, output: 1.1 },
    stages: rows,
    total: { prompt_tokens: totalIn, completion_tokens: totalOut, usd: totalUsd, cny },
  }, null, 2));
  console.log(`\n详细: ${out}`);
}

main().catch(e => { console.error(e); process.exit(1); });
