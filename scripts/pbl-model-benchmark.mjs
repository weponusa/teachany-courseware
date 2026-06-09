#!/usr/bin/env node
/**
 * OpenRouter / 线上 API PBL 拆解能力对比
 * 用法:
 *   node scripts/pbl-model-benchmark.mjs [--tier=free|paid|all] [--stages=decompose,filter]
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const PBL_API = 'https://www.teachany.cn/api/pbl/analyze';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, '..');

function loadOpenRouterKey() {
  if (process.env.OPENROUTER_KEY) return process.env.OPENROUTER_KEY;
  const s = fs.readFileSync(path.join(ROOT, 'scripts/ai-tutor.js'), 'utf8');
  const m = s.match(/const _k1 = '([^']+)';\s*const _k2 = '([^']+)';\s*const _k3 = '([^']+)';\s*const _k4 = '([^']+)'/);
  return m ? m[1] + m[2] + m[3] + m[4] : '';
}

const OR_KEY = loadOpenRouterKey();
const TIER = (process.argv.find(a => a.startsWith('--tier=')) || '--tier=all').slice(7);
const STAGES = (process.argv.find(a => a.startsWith('--stages=')) || '--stages=decompose,filter')
  .slice(9).split(',').filter(Boolean);

const GOALS = [
  {
    key: 'shopping',
    label: '小学购物·单学科数学',
    goal: '模拟小卖部购物场景，用人民币学具完成付款和找零，制作购物小票',
    complex: false,
    expect: /人民币|找零|加减|购物|小票|价格|元|角/,
    ban: /细胞|磁铁|火箭|滴定|硝酸银/,
  },
  {
    key: 'canteen',
    label: '食堂汤水·化学探究',
    goal: '食堂菜汤的盐含量测定，比较滴定法与电导率法并撰写报告',
    complex: true,
    expect: /盐|滴定|电导率|溶液|浓度|实验|报告/,
    ban: /苏东坡|诗词|购车|细胞分裂/,
  },
];

/** @type {{id:string,label:string,tier:'free'|'paid',provider:'openrouter'|'siliconflow'|'paratera'|'teachany',model:string,priceIn?:number,key?:string}[]} */
const FREE_MODELS = [
  { id: 'qwen3-next', label: '千问3·Qwen3 Next 80B (free)', tier: 'free', provider: 'openrouter', model: 'qwen/qwen3-next-80b-a3b-instruct:free' },
  { id: 'qwen3-coder', label: '千问3·Qwen3 Coder 480B (free)', tier: 'free', provider: 'openrouter', model: 'qwen/qwen3-coder:free' },
  { id: 'gpt-oss-120b', label: 'GPT·gpt-oss-120b (free)', tier: 'free', provider: 'openrouter', model: 'openai/gpt-oss-120b:free' },
  { id: 'gemma4-31b', label: 'Google·Gemma 4 31B (free)', tier: 'free', provider: 'openrouter', model: 'google/gemma-4-31b-it:free' },
  { id: 'llama70b', label: 'Meta·Llama 3.3 70B (free)', tier: 'free', provider: 'openrouter', model: 'meta-llama/llama-3.3-70b-instruct:free' },
  { id: 'glm-air', label: '智谱·GLM-4.5 Air (free)', tier: 'free', provider: 'openrouter', model: 'z-ai/glm-4.5-air:free' },
  { id: 'kimi-k26', label: 'Kimi K2.6 (free)', tier: 'free', provider: 'openrouter', model: 'moonshotai/kimi-k2.6:free' },
];

/** OpenRouter 标价 $/1M input tokens（2026-06） */
const PAID_MODELS = [
  { id: 'prod-api', label: '生产基线·线上 DeepSeek V4 Flash', tier: 'paid', provider: 'teachany', model: 'auto', priceIn: 0 },
  { id: 'prod-sf', label: '硅基·DeepSeek V4 Flash', tier: 'paid', provider: 'siliconflow', model: 'deepseek-ai/DeepSeek-V4-Flash', priceIn: 0.05 },
  { id: 'hy3', label: '腾讯·HY3 preview', tier: 'paid', provider: 'openrouter', model: 'tencent/hy3-preview', priceIn: 0.063 },
  { id: 'qwen35-flash', label: '千问·Qwen3.5 Flash', tier: 'paid', provider: 'openrouter', model: 'qwen/qwen3.5-flash-02-23', priceIn: 0.065 },
  { id: 'qwen3-next-paid', label: '千问·Qwen3 Next 80B (付费)', tier: 'paid', provider: 'openrouter', model: 'qwen/qwen3-next-80b-a3b-instruct', priceIn: 0.09 },
  { id: 'dsv4-or', label: 'DeepSeek·V4 Flash (OR)', tier: 'paid', provider: 'openrouter', model: 'deepseek/deepseek-v4-flash', priceIn: 0.098 },
  { id: 'gemini-flash-lite', label: 'Gemini·2.5 Flash Lite', tier: 'paid', provider: 'openrouter', model: 'google/gemini-2.5-flash-lite', priceIn: 0.1 },
  { id: 'gpt4o-mini', label: 'GPT·4o-mini', tier: 'paid', provider: 'openrouter', model: 'openai/gpt-4o-mini', priceIn: 0.15 },
  { id: 'claude-haiku', label: 'Claude·3 Haiku', tier: 'paid', provider: 'openrouter', model: 'anthropic/claude-3-haiku', priceIn: 0.25 },
  { id: 'gemini-flash', label: 'Gemini·2.5 Flash', tier: 'paid', provider: 'openrouter', model: 'google/gemini-2.5-flash', priceIn: 0.3 },
];

const MODELS = TIER === 'free' ? FREE_MODELS
  : TIER === 'paid' ? PAID_MODELS
    : [...FREE_MODELS, ...PAID_MODELS];

const BACKENDS = {
  openrouter: { baseUrl: 'https://openrouter.ai/api/v1', key: OR_KEY, headers: { 'HTTP-Referer': 'https://www.teachany.cn', 'X-Title': 'TeachAny-PBL-Bench' } },
  siliconflow: { baseUrl: 'https://api.siliconflow.cn/v1', key: process.env.SILICONFLOW_KEY || '', headers: {} },
  paratera: { baseUrl: 'https://llmapi.paratera.com/v1', key: process.env.PARATERA_KEY || '', headers: {} },
};

function extractJsonObject(text) {
  const s = String(text || '');
  const fenced = s.match(/```(?:json)?\s*([\s\S]*?)```/);
  const raw = fenced ? fenced[1] : s;
  const start = raw.indexOf('{');
  const end = raw.lastIndexOf('}');
  if (start < 0 || end <= start) throw new Error('no JSON object');
  return JSON.parse(raw.slice(start, end + 1));
}

function scoreDecompose(parsed, caseDef, raw) {
  const issues = [];
  let score = 0;
  const blob = JSON.stringify(parsed);
  if (parsed?.projectSummary) score += 10;
  if (parsed?.deliverable) score += 15;
  if (Array.isArray(parsed?.schemes) && parsed.schemes.length) score += 15;
  const phases = (parsed?.schemes || []).flatMap(s => s.phases || []);
  if (phases.length >= 3) score += 15;
  const hints = phases.flatMap(p => p.knowledgeHints || []).join(' ');
  const steps = phases.flatMap(p => p.steps || []).join(' ');
  const text = `${blob} ${hints} ${steps}`;
  if (caseDef.expect.test(text)) score += 25; else issues.push('主题词未覆盖');
  if (caseDef.ban.test(text)) { score -= 20; issues.push('出现跑题词'); }
  if (/递进式实施|原型驱动迭代|环境搭建/.test(blob)) { score -= 10; issues.push('模板空话'); }
  if (phases.some(p => (p.steps || []).length < 2)) issues.push('部分阶段步骤不足');
  return { score: Math.max(0, Math.min(100, score)), issues, phaseCount: phases.length };
}

function scoreFilter(parsed, caseDef) {
  const issues = [];
  let score = 0;
  const subs = parsed?.subjects || [];
  if (Array.isArray(subs) && subs.length) score += 30;
  if (caseDef.key === 'shopping' && subs.includes('math') && !subs.includes('biology')) score += 40;
  else if (caseDef.key === 'shopping' && subs.includes('science')) { score -= 15; issues.push('购物不应主选 science'); }
  if (caseDef.key === 'canteen' && (subs.includes('chemistry') || subs.includes('science'))) score += 40;
  if (parsed?.bloomCeiling >= 1 && parsed?.bloomCeiling <= 6) score += 15;
  if (parsed?.grades?.length || parsed?.minGrade) score += 15;
  return { score: Math.max(0, Math.min(100, score)), issues, subjects: subs };
}

async function callTeachany(stage, payload) {
  const t0 = Date.now();
  const resp = await fetch(PBL_API, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ stage, ...payload }),
  });
  const ms = Date.now() - t0;
  const data = await resp.json().catch(() => ({}));
  if (!resp.ok) return { error: data.error || `${resp.status}`, ms };
  return { content: data.content || '', ms, usedModel: data.model, backend: data.backend };
}

async function callModel(provider, model, messages, stage) {
  const b = BACKENDS[provider];
  if (!b?.key) return { error: `missing ${provider} key` };
  const maxTokens = stage === 'decompose' ? 4500 : 1200;
  const temperature = stage === 'decompose' ? 0.35 : 0.25;
  const t0 = Date.now();
  const resp = await fetch(`${b.baseUrl}/chat/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${b.key}`,
      ...b.headers,
    },
    body: JSON.stringify({ model, messages, stream: false, temperature, max_tokens: maxTokens }),
  });
  const ms = Date.now() - t0;
  const text = await resp.text();
  if (!resp.ok) return { error: `${resp.status} ${text.slice(0, 280)}`, ms };
  let content = '';
  try { content = JSON.parse(text).choices?.[0]?.message?.content || ''; } catch { content = text; }
  return { content, ms };
}

async function fetchPBLMessages(stage, payload) {
  const resp = await fetch(PBL_API, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ stage, messagesOnly: true, ...payload }),
  });
  const data = await resp.json().catch(() => ({}));
  if (!resp.ok) throw new Error(data.error || `messagesOnly ${resp.status}`);
  return data.messages;
}

async function runOne(modelDef, caseDef, stage) {
  const payload = {
    goal: caseDef.goal,
    complex: caseDef.complex,
    summaryList: stage === 'filter' ? 'math: 100以内加减法\nchinese: 应用文\nscience: 测量记录' : '',
    projectBlueprint: stage === 'filter' ? {
      deliverable: '项目交付物',
      schemes: [{ phases: [{ phase: '调研', knowledgeHints: ['调查'], steps: ['设计问卷'] }] }],
    } : null,
  };
  let r;
  if (modelDef.provider === 'teachany') {
    r = await callTeachany(stage, payload);
  } else {
    const messages = await fetchPBLMessages(stage, payload);
    r = await callModel(modelDef.provider, modelDef.model, messages, stage);
  }
  if (r.error) return { ok: false, error: r.error, ms: r.ms || 0 };

  try {
    const parsed = extractJsonObject(r.content);
    const scored = stage === 'decompose'
      ? scoreDecompose(parsed, caseDef, r.content)
      : scoreFilter(parsed, caseDef);
    return {
      ok: true, ms: r.ms, score: scored.score, issues: scored.issues,
      usedModel: r.usedModel, backend: r.backend,
      preview: r.content.slice(0, 400),
    };
  } catch (e) {
    return { ok: false, error: `JSON解析失败: ${e.message}`, ms: r.ms, preview: r.content?.slice(0, 300) };
  }
}

async function main() {
  const needsOR = MODELS.some(m => m.provider === 'openrouter');
  if (needsOR && !OR_KEY) {
    console.error('需要 OPENROUTER_KEY 或 scripts/ai-tutor.js 内置 Key');
    process.exit(1);
  }

  const results = [];
  console.log(`PBL 模型对比 | tier=${TIER} | stages=${STAGES.join(',')} | goals=${GOALS.length}\n`);

  for (const m of MODELS) {
    if (m.provider === 'teachany') { /* 走线上 API，无需 Key */ }
    else if (m.provider !== 'openrouter' && !BACKENDS[m.provider]?.key) {
      console.log(`⏭  跳过 ${m.label}（无 API Key）\n`);
      continue;
    }
    const priceTag = m.priceIn != null ? ` · ~$${m.priceIn}/1M in` : '';
    console.log(`\n━━ ${m.label}${priceTag} ━━`);
    const row = { id: m.id, label: m.label, tier: m.tier, model: m.model, priceIn: m.priceIn, cases: {} };

    for (const c of GOALS) {
      row.cases[c.key] = {};
      for (const stage of STAGES) {
        process.stdout.write(`  ${c.key}/${stage} ... `);
        try {
          const r = await runOne(m, c, stage);
          row.cases[c.key][stage] = r;
          if (r.ok) {
            const extra = r.usedModel ? ` [${r.usedModel}]` : '';
            console.log(`✓ ${r.score}分 ${(r.ms / 1000).toFixed(1)}s${extra} ${r.issues?.length ? '(' + r.issues.join(';') + ')' : ''}`);
          } else {
            console.log(`✗ ${r.error} ${r.ms ? (r.ms / 1000).toFixed(1) + 's' : ''}`);
          }
        } catch (e) {
          row.cases[c.key][stage] = { ok: false, error: e.message };
          console.log(`✗ ${e.message}`);
        }
        await new Promise(res => setTimeout(res, 2500));
      }
    }
    results.push(row);
  }

  const ranked = results.map(r => {
    let total = 0; let n = 0; let ms = 0;
    for (const c of Object.values(r.cases)) {
      for (const s of Object.values(c)) {
        if (s.ok) { total += s.score; n++; ms += s.ms; }
      }
    }
    return { ...r, avg: n ? Math.round(total / n) : 0, avgMs: n ? Math.round(ms / n) : 0, ok: n };
  }).filter(r => r.ok).sort((a, b) => b.avg - a.avg || a.avgMs - b.avgMs);

  console.log('\n\n========== 排名（均分 / 耗时 / 单价）==========');
  ranked.forEach((r, i) => {
    const price = r.priceIn != null ? ` · $${r.priceIn}/1M` : '';
    console.log(`${i + 1}. ${r.label} — ${r.avg}分 · ${(r.avgMs / 1000).toFixed(1)}s/次${price} · ${r.model}`);
  });

  if (TIER === 'free' || TIER === 'all') {
    console.log('\n备注: OpenRouter 无 Claude/Gemini 免费对话模型；HY3 免费档已下线。');
  }
  if (TIER === 'paid' || TIER === 'all') {
    console.log('\n付费档参考: 硅基 DeepSeek V4 Flash 通常最便宜；HY3/Qwen3.5 Flash OR 标价略低但需实测稳定性。');
  }

  const outName = TIER === 'paid' ? 'model-benchmark-paid.json'
    : TIER === 'free' ? 'model-benchmark.json'
      : 'model-benchmark-all.json';
  const out = path.join(ROOT, 'data/pbl-iterate', outName);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, JSON.stringify({
    generatedAt: new Date().toISOString(), tier: TIER,
    stages: STAGES, goals: GOALS.map(g => g.key), ranked, results,
  }, null, 2));
  console.log(`\n详细结果: ${out}`);
}

main().catch(e => { console.error(e); process.exit(1); });
