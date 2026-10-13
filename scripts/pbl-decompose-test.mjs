#!/usr/bin/env node
/**
 * PBL 拆解质量实测：本地提示词 + OpenRouter 多模型对比
 * node scripts/pbl-decompose-test.mjs [--models=qwen3-next,dsv4-flash,dsv4-pro,gpt4o-mini]
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { buildPBMessages } from '../functions/_lib/pbl-prompts.js';
import { buildReviewDecomposeMessages } from '../functions/_lib/pbl-review-decompose-prompts.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, '..');

function loadOpenRouterKey() {
  if (process.env.OPENROUTER_KEY) return process.env.OPENROUTER_KEY;
  const s = fs.readFileSync(path.join(ROOT, 'scripts/ai-tutor.js'), 'utf8');
  const m = s.match(/const _k1 = '([^']+)';\s*const _k2 = '([^']+)';\s*const _k3 = '([^']+)';\s*const _k4 = '([^']+)'/);
  return m ? m[1] + m[2] + m[3] + m[4] : '';
}

const OR_KEY = loadOpenRouterKey();

const CASE = {
  label: '道法+心理·校园反欺凌',
  goal: '【道法+心理】设计校园反欺凌宣传行动：调查同伴感受，运用规则与情绪知识制定干预方案并撰写倡议书',
  projectSpec: {
    gradeLevel: 'junior',
    gradeDetail: '8',
    subjects: ['politics', 'psychology'],
    subject: 'cross',
    task: '反欺凌宣传',
    deliverable: 'report',
  },
  complex: false,
  expect: /欺凌|霸凌|问卷|情绪|规则|权利|倡议|宣传|访谈|统计|图表|同伴/,
  ban: /A3纸|铅笔尺规|标注笔|过程记录表|查阅资料并分析|开展调查研究|完成本阶段|环境搭建|原型驱动/,
};

const MODEL_PRESETS = {
  'qwen3-next': { label: 'Qwen3 Next 80B', model: 'qwen/qwen3-next-80b-a3b-instruct' },
  'dsv4-flash': { label: 'DeepSeek V4 Flash', model: 'deepseek/deepseek-v4-flash' },
  'dsv4-pro': { label: 'DeepSeek V4 Pro', model: 'deepseek/deepseek-v4-pro' },
  'gpt4o-mini': { label: 'GPT-4o-mini', model: 'openai/gpt-4o-mini' },
};

function parseModelsArg() {
  const raw = (process.argv.find(a => a.startsWith('--models=')) || '--models=qwen3-next,dsv4-flash,dsv4-pro,gpt4o-mini').slice(9);
  return raw.split(',').map(s => s.trim()).filter(Boolean);
}

function extractJson(text) {
  const s = String(text || '');
  const fenced = s.match(/```(?:json)?\s*([\s\S]*?)```/);
  const raw = fenced ? fenced[1] : s;
  const start = raw.indexOf('{');
  const end = raw.lastIndexOf('}');
  if (start < 0 || end <= start) throw new Error('no JSON');
  return JSON.parse(raw.slice(start, end + 1));
}

function isHollowStep(step) {
  const s = String(step || '').trim();
  if (!s || s.length < 12) return true;
  if (/查阅资料并分析|开展调查研究|完成本阶段|撰写研究报告初稿|进行调研工作/.test(s)) return true;
  if (/^(完成|进行|开展|落实).{0,12}(本阶段|阶段任务|调查任务)/.test(s)) return true;
  if (!/\d|≥|不少于|至少|表|图|问卷|访谈|倡议|统计|样本|题|人|次|字数/.test(s)) return true;
  return false;
}

function scoreBlueprint(bp, caseDef) {
  const issues = [];
  let score = 0;
  const scheme = (bp?.schemes || []).find(s => s.id === bp.recommendedSchemeId) || bp?.schemes?.[0];
  const phases = scheme?.phases || [];
  const allSteps = phases.flatMap(p => p.steps || []);
  const blob = JSON.stringify(bp);

  if (bp?.drivingQuestion && /[？?]/.test(bp.drivingQuestion)) score += 8;
  else issues.push('缺 drivingQuestion 问句');

  if (bp?.deliverable && !/阶段成果|方案$|探究任务/.test(bp.deliverable)) score += 10;
  else issues.push('deliverable 不具体');

  if ((bp?.schemes || []).length >= 2) score += 8;
  if (phases.length >= 4) score += 10;

  if (caseDef.expect.test(blob)) score += 15;
  else issues.push('未覆盖主题词');

  if (caseDef.ban.test(blob)) { score -= 15; issues.push('含禁词/文具套话'); }

  const hollow = allSteps.filter(isHollowStep).length;
  if (hollow === 0 && allSteps.length >= 8) score += 20;
  else if (hollow <= 2) score += 10;
  else issues.push(`空话步骤 ${hollow}/${allSteps.length}`);

  let quantPhases = 0;
  phases.forEach(p => {
    if ((p.steps || []).some(st => /\d|≥|不少于|至少/.test(String(st)))) quantPhases += 1;
    const badTools = (p.tools || []).filter(t => /A3|铅笔|尺规|相机|过程记录表|记录表模板/.test(String(t)));
    if (badTools.length) issues.push(`tools文具: ${badTools.join('、')}`);
  });
  if (quantPhases >= 3) score += 12;
  else issues.push(`仅 ${quantPhases} 阶段含量化`);

  const samples = allSteps.slice(0, 4).map((s, i) => `  ${i + 1}. ${String(s).slice(0, 80)}${String(s).length > 80 ? '…' : ''}`);
  return { score: Math.max(0, Math.min(100, score)), issues, phaseCount: phases.length, stepCount: allSteps.length, samples };
}

async function callOpenRouter(model, messages, maxTokens = 5000) {
  const t0 = Date.now();
  const resp = await fetch('https://openrouter.ai/api/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${OR_KEY}`,
      'HTTP-Referer': 'https://www.teachany.cn',
      'X-Title': 'TeachAny-PBL-Test',
    },
    body: JSON.stringify({
      model,
      messages,
      stream: false,
      temperature: 0.35,
      max_tokens: maxTokens,
    }),
  });
  const ms = Date.now() - t0;
  const text = await resp.text();
  if (!resp.ok) return { error: `${resp.status} ${text.slice(0, 200)}`, ms };
  let content = '';
  try { content = JSON.parse(text).choices?.[0]?.message?.content || ''; } catch { content = text; }
  return { content, ms, model };
}

async function runDecompose(modelKey) {
  const preset = MODEL_PRESETS[modelKey];
  if (!preset) throw new Error(`unknown: ${modelKey}`);

  const messages = buildPBMessages('decompose', {
    goal: CASE.goal,
    complex: CASE.complex,
    projectSpec: CASE.projectSpec,
  });

  const r = await callOpenRouter(preset.model, messages);
  if (r.error) return { ok: false, label: preset.label, modelKey, error: r.error, ms: r.ms };

  try {
    const bp = extractJson(r.content);
    const scored = scoreBlueprint(bp, CASE);
    return {
      ok: true,
      label: preset.label,
      modelKey,
      usedModel: preset.model,
      ms: r.ms,
      bp,
      ...scored,
      deliverable: bp.deliverable,
      drivingQuestion: bp.drivingQuestion,
    };
  } catch (e) {
    return { ok: false, label: preset.label, error: `JSON: ${e.message}`, ms: r.ms, preview: r.content?.slice(0, 280) };
  }
}

async function runReview(draft) {
  const messages = buildReviewDecomposeMessages({
    goal: CASE.goal,
    projectBlueprint: draft,
    reviewIssues: ['步骤须含量化指标与可验收产出', 'tools 禁文具', 'deliverable 用具体表/图/报告名'],
    complex: CASE.complex,
    projectSpec: CASE.projectSpec,
  });
  const r = await callOpenRouter('qwen/qwen3-next-80b-a3b-instruct', messages, 5500);
  if (r.error) return null;
  try {
    return { bp: extractJson(r.content), ms: r.ms };
  } catch {
    return null;
  }
}

async function main() {
  if (!OR_KEY) {
    console.error('需要 OPENROUTER_KEY');
    process.exit(1);
  }

  const models = parseModelsArg();
  console.log(`PBL 拆解实测（本地提示词 v6 + OpenRouter）`);
  console.log(`案例: ${CASE.label}\n`);

  const rows = [];
  for (const key of models) {
    process.stdout.write(`▶ ${MODEL_PRESETS[key]?.label || key} ... `);
    try {
      const r = await runDecompose(key);
      if (!r.ok) {
        console.log(`✗ ${r.error} (${((r.ms || 0) / 1000).toFixed(1)}s)`);
        rows.push(r);
        continue;
      }
      console.log(`✓ ${r.score}分 | ${r.phaseCount}阶段 ${r.stepCount}步 | ${(r.ms / 1000).toFixed(1)}s`);
      if (r.issues.length) console.log(`   ⚠ ${r.issues.join('; ')}`);
      rows.push(r);
    } catch (e) {
      console.log(`✗ ${e.message}`);
      rows.push({ ok: false, label: key, error: e.message });
    }
  }

  const best = [...rows].filter(r => r.ok).sort((a, b) => b.score - a.score)[0];
  if (best?.bp) {
    console.log(`\n▶ review-decompose（用 Qwen3 修订 ${best.label} 初稿 ${best.score}分）...`);
    const reviewed = await runReview(best.bp);
    if (reviewed?.bp) {
      const scored = scoreBlueprint(reviewed.bp, CASE);
      console.log(`  修订后: ${scored.score}分 (Δ${scored.score - best.score >= 0 ? '+' : ''}${scored.score - best.score}) | ${(reviewed.ms / 1000).toFixed(1)}s`);
      if (scored.issues.length) console.log(`  ⚠ ${scored.issues.join('; ')}`);
      console.log('  修订后步骤样例:');
      scored.samples.forEach(s => console.log(s));
      rows.push({ ok: true, label: `${best.label}+review`, modelKey: 'review', usedModel: 'qwen3-next+review', ...scored, deliverable: reviewed.bp.deliverable });
    } else {
      console.log('  修订失败');
    }
  }

  console.log('\n══ 排名 ══');
  for (const r of [...rows].filter(x => x.ok).sort((a, b) => b.score - a.score)) {
    console.log(`${String(r.score).padStart(3)}分  ${r.label.padEnd(28)}  ${r.phaseCount || '-'}阶段 ${r.stepCount || '-'}步  ${r.issues?.length ? r.issues.join('; ') : 'OK'}`);
  }

  if (best?.ok) {
    console.log(`\n── 最佳初稿: ${best.label} ──`);
    console.log(`Q: ${best.drivingQuestion || '—'}`);
    console.log(`交付: ${best.deliverable || '—'}`);
    best.samples?.forEach(s => console.log(s));
  }

  const out = path.join(ROOT, 'data/pbl-iterate/decompose-test-latest.json');
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, JSON.stringify({
    at: new Date().toISOString(),
    mode: 'local-prompts+openrouter',
    case: CASE,
    results: rows.map(({ bp, ...rest }) => rest),
  }, null, 2));
  console.log(`\n结果已保存: ${out}`);
}

main().catch(e => { console.error(e); process.exit(1); });
