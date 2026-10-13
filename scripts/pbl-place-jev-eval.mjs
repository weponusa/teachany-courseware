#!/usr/bin/env node

import fs from 'node:fs/promises';
import process from 'node:process';

const ROOT = new URL('../', import.meta.url);
const GOALS_PATH = process.argv[2] || '/tmp/pbl-place-100.json';
const OUTPUT_PATH = process.argv[3] || '/tmp/pbl-place-jev-eval.json';
const LLM_URL = 'https://www.teachany.cn/api/llm/chat/completions';
const ANALYZE_URL = 'https://www.teachany.cn/api/pbl/analyze';
const MODEL = 'qwen/qwen3-next-80b-a3b-instruct';
const JEV_THRESHOLD = 0.35;

const CENTERS = [
  { school: '北京市潞河中学（模拟）', city: '北京', lon: 116.64777, lat: 39.89779 },
  { school: '上海市徐汇中学（模拟）', city: '上海', lon: 121.43130, lat: 31.19430 },
  { school: '寿光市第一中学（模拟）', city: '潍坊', lon: 118.75620, lat: 36.88860 },
  { school: '西安市铁一中学（模拟）', city: '西安', lon: 108.96880, lat: 34.24170 },
  { school: '成都市石室中学（模拟）', city: '成都', lon: 104.06650, lat: 30.66920 },
  { school: '广州市执信中学（模拟）', city: '广州', lon: 113.28210, lat: 23.13250 },
  { school: '武汉市第二中学（模拟）', city: '武汉', lon: 114.30450, lat: 30.60060 },
  { school: '杭州市第二中学（模拟）', city: '杭州', lon: 120.16470, lat: 30.24080 },
];

const BAD_NAME = /小学|中学|幼儿园|社区|家园|小区|公寓|宿舍|住宅|超市|饭店|餐厅|便民|管理处|服务处|办事处|综合楼|办公楼/;
const GOOD_TYPE = /博物馆|科技馆|纪念馆|规划馆|展览馆|公园|湿地|水闸|农场|温室|植物园|剧场|市场|充电|遗址|基地|园区/;

function hashNumber(text) {
  let h = 2166136261;
  for (const char of String(text || '')) {
    h ^= char.codePointAt(0);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

function haversineKm(a, b) {
  const rad = Math.PI / 180;
  const dLat = (b.lat - a.lat) * rad;
  const dLon = (b.lon - a.lon) * rad;
  const x = Math.sin(dLat / 2) ** 2
    + Math.cos(a.lat * rad) * Math.cos(b.lat * rad) * Math.sin(dLon / 2) ** 2;
  return 2 * 6371 * Math.asin(Math.min(1, Math.sqrt(x)));
}

function extractJson(text) {
  const source = String(text || '').replace(/```json|```/g, '').trim();
  try { return JSON.parse(source); } catch {}
  const object = source.match(/\{[\s\S]*\}/);
  if (object) {
    try { return JSON.parse(object[0]); } catch {}
  }
  const array = source.match(/\[[\s\S]*\]/);
  if (array) {
    try { return JSON.parse(array[0]); } catch {}
  }
  throw new Error(`No JSON in response: ${source.slice(0, 160)}`);
}

async function fetchJson(url, options = {}, timeoutMs = 30000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(url, { ...options, signal: controller.signal });
    const text = await response.text();
    if (!response.ok) throw new Error(`${response.status}: ${text.slice(0, 240)}`);
    return JSON.parse(text);
  } finally {
    clearTimeout(timer);
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function llm(messages, maxTokens = 700) {
  const data = await fetchJson(LLM_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-Title': 'PBL Place Jev Eval' },
    body: JSON.stringify({
      model: MODEL,
      messages,
      temperature: 0,
      max_tokens: maxTokens,
      stream: false,
    }),
  }, 65000);
  return data.choices?.[0]?.message?.content || '';
}

async function mapLimit(items, limit, worker) {
  const output = new Array(items.length);
  let cursor = 0;
  async function run() {
    while (cursor < items.length) {
      const index = cursor++;
      try {
        output[index] = await worker(items[index], index);
      } catch (error) {
        output[index] = { error: error.message };
      }
    }
  }
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, run));
  return output;
}

async function currentPlanningPrompt() {
  const source = await fs.readFile(new URL('functions/api/pbl/places.js', ROOT), 'utf8');
  const match = source.match(/const PLACE_PLAN_PROMPT = `([\s\S]*?)`;/);
  if (!match) throw new Error('PLACE_PLAN_PROMPT not found');
  return match[1];
}

async function planOne(prompt, goal) {
  const content = await llm([
    { role: 'system', content: prompt },
    { role: 'user', content: `项目目标：${goal.slice(0, 1200)}` },
  ], 500);
  const plan = extractJson(content);
  return {
    object: String(plan.object || ''),
    see: String(plan.see || ''),
    evidence: String(plan.evidence || ''),
    campus_only: Boolean(plan.campus_only),
    queries: [...new Set((plan.queries || []).map(String).map(s => s.trim()).filter(Boolean))].slice(0, 8),
    poi: [...new Set((plan.poi || []).map(String).map(s => s.trim()).filter(Boolean))].slice(0, 4),
    reject_names: [...new Set((plan.reject_names || []).map(String).map(s => s.trim()).filter(Boolean))].slice(0, 8),
  };
}

let nominatimNextAt = 0;
let nominatimQueue = Promise.resolve();

async function boundedMapSearch(center, query) {
  let release;
  const previous = nominatimQueue;
  nominatimQueue = new Promise(resolve => { release = resolve; });
  await previous;
  try {
    const wait = Math.max(0, nominatimNextAt - Date.now());
    if (wait) await sleep(wait);
    nominatimNextAt = Date.now() + 1100;
    const latPad = 30 / 111;
    const lonPad = 30 / (111 * Math.cos(center.lat * Math.PI / 180));
    const params = new URLSearchParams({
      format: 'jsonv2',
      limit: '7',
      bounded: '1',
      viewbox: [
        center.lon - lonPad,
        center.lat + latPad,
        center.lon + lonPad,
        center.lat - latPad,
      ].join(','),
      q: query,
    });
    const rows = await fetchJson(`https://nominatim.openstreetmap.org/search?${params}`, {
      headers: { 'User-Agent': 'TeachAnyPlace-Eval/1.0 contact=teachany.cn' },
    }, 20000);
    return (rows || []).map(row => ({
      type: 'Feature',
      properties: {
        name: String(row.display_name || '').split(',')[0].trim(),
        city: String(row.display_name || '').split(',').slice(-4, -3)[0]?.trim() || '',
        osm_key: row.class || '',
        osm_value: row.type || '',
        type: row.type || row.class || '',
      },
      geometry: { type: 'Point', coordinates: [Number(row.lon), Number(row.lat)] },
    }));
  } finally {
    release();
  }
}

async function candidatesFor(plan, center) {
  if (plan.campus_only || !plan.queries.length) return [];
  const classTerms = [];
  if (plan.poi.includes('museum_named')) classTerms.push('博物馆', '科技馆', ...plan.queries.slice(0, 1).map(term => `${term}博物馆`));
  if (plan.poi.includes('park_named')) classTerms.push('公园', ...plan.queries.slice(0, 1).map(term => `${term}公园`));
  if (plan.poi.includes('farm')) classTerms.push('农场', '农业园', '温室');
  if (plan.poi.includes('recycling')) classTerms.push('回收站', '转运站');
  if (plan.poi.includes('industrial')) classTerms.push('产业园', '工厂');
  if (plan.poi.includes('community')) classTerms.push('社区服务中心');
  if (plan.poi.includes('theatre')) classTerms.push('剧场');
  if (plan.poi.includes('marketplace')) classTerms.push('市场');
  if (plan.poi.includes('historic')) classTerms.push('遗址', '纪念馆');
  if (plan.poi.includes('fuel_named')) classTerms.push('充电站', '加氢站');
  const terms = [...new Set([
    ...plan.queries.slice(0, 2),
    ...classTerms.slice(0, 3),
    ...plan.queries.slice(0, 1).map(term => `${center.city}${term}`),
  ])].slice(0, 3);
  const lists = await mapLimit(terms, 2, term => boundedMapSearch(center, term));
  const byName = new Map();
  for (const features of lists) {
    if (!Array.isArray(features)) continue;
    for (const feature of features) {
      const props = feature.properties || {};
      const coords = feature.geometry?.coordinates || [];
      const name = String(props.name || '').trim();
      if (!name || coords.length < 2 || BAD_NAME.test(name)) continue;
      if (/店$/.test(name) && !/市场/.test(name)) continue;
      if (/(路|街|街道)$/.test(name) && !/公园|博物馆|水闸/.test(name)) continue;
      const distanceKm = haversineKm(center, { lon: coords[0], lat: coords[1] });
      if (!Number.isFinite(distanceKm) || distanceKm > 30) continue;
      const hit = plan.queries.find(term => name.includes(term))
        || classTerms.find(term => name.includes(term));
      if (!hit) continue;
      const candidate = {
        name,
        category: props.osm_value || props.type || props.osm_key || 'place',
        distanceKm: Math.round(distanceKm * 10) / 10,
        city: props.city || props.state || '',
        queryHit: hit,
      };
      const old = byName.get(name);
      if (!old || candidate.distanceKm < old.distanceKm) byName.set(name, candidate);
    }
  }
  return [...byName.values()]
    .sort((a, b) => {
      const aq = GOOD_TYPE.test(a.name) ? 0 : 1;
      const bq = GOOD_TYPE.test(b.name) ? 0 : 1;
      return aq - bq || a.distanceKm - b.distanceKm;
    })
    .slice(0, 4);
}

async function jevScoreProject(project) {
  const candidates = project.candidates || [];
  const data = await fetchJson(ANALYZE_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      stage: 'verify-places',
      goal: project.goal,
      deliverable: project.plan.evidence || '可复核的现场记录',
      placeLabel: project.center.school,
      items: candidates.map((candidate, index) => ({
        index,
        name: `${candidate.name}（${candidate.category}，距出发点 ${candidate.distanceKm} 公里）`,
      })),
    }),
  }, 25000);
  const byIndex = new Map((data.scores || []).map(row => [Number(row.index), Number(row.noul)]));
  return candidates.map((candidate, index) => ({
    ...project,
    candidate,
    jev: Number.isFinite(byIndex.get(index)) ? byIndex.get(index) : null,
    jevError: data.fallback ? String(data.reason || 'fallback') : '',
  }));
}

async function truthChunk(rows) {
  const items = rows.map((row, index) => ({
    id: index,
    goal: row.goal,
    object: row.plan.object,
    see: row.plan.see,
    candidate: row.candidate.name,
    category: row.candidate.category,
    distance_km: row.candidate.distanceKm,
  }));
  const content = await llm([
    {
      role: 'system',
      content: `你是校外实践候选点的独立审核员。逐项判断候选地点是否能支持课题。
true 必须满足：仅凭地点名称和类别就能确认，学生在开放区域能直接看到课题对象或其公认载体，并能收集证据。例如充电站对电动车、鲁迅纪念馆对鲁迅、木偶剧院对木偶。
false：仅共享行业词或修饰词；普通公司、销售中心、办公楼、住宅、道路、学校；名称无法确认有相关展陈的普通博物馆、科技馆、剧场、农场、图书馆。
禁止推测“可能有”“常展”“通常有”“或许有”题目所需展品。候选名没明确写出对象，就按 false；不要用外部常识替候选补展览内容。
不要因为距离近而放宽。不要参考任何 Jev 分数。只返回 JSON 数组 [{"id":0,"keep":true,"reason":"不超过20字"}]。`,
    },
    { role: 'user', content: JSON.stringify(items) },
  ], 2200);
  const parsed = extractJson(content);
  const array = Array.isArray(parsed) ? parsed : parsed.items;
  return new Map((array || []).map(item => [Number(item.id), {
    keep: Boolean(item.keep),
    reason: String(item.reason || ''),
  }]));
}

function metrics(rows, predicate) {
  let tp = 0; let fp = 0; let fn = 0; let tn = 0;
  for (const row of rows) {
    const predicted = predicate(row);
    if (predicted && row.truth) tp++;
    else if (predicted) fp++;
    else if (row.truth) fn++;
    else tn++;
  }
  const precision = tp + fp ? tp / (tp + fp) : 0;
  const recall = tp + fn ? tp / (tp + fn) : 0;
  const f1 = precision + recall ? 2 * precision * recall / (precision + recall) : 0;
  return { tp, fp, fn, tn, precision, recall, f1 };
}

async function main() {
  const goals = JSON.parse(await fs.readFile(GOALS_PATH, 'utf8')).slice(0, 100);
  const prompt = await currentPlanningPrompt();
  console.log(`Planning ${goals.length} production goals...`);
  let plans;
  if (process.env.EVAL_REUSE_PLANS === '1') {
    plans = JSON.parse(await fs.readFile('/tmp/pbl-place-jev-plans.json', 'utf8'));
  } else {
    plans = await mapLimit(goals, 5, async (entry, index) => ({
      ...entry,
      index,
      goal: entry.goal,
      center: CENTERS[hashNumber(entry.ip_hash) % CENTERS.length],
      plan: await planOne(prompt, entry.goal),
    }));
  }
  const validPlans = plans.filter(row => !row.error);
  await fs.writeFile('/tmp/pbl-place-jev-plans.json', JSON.stringify(validPlans, null, 2));
  console.log(`Plans: ${validPlans.length}, campus-only: ${validPlans.filter(r => r.plan.campus_only).length}`);
  if (process.env.EVAL_PLAN_ONLY === '1') return;

  console.log('Retrieving map candidates...');
  let projects;
  if (process.env.EVAL_REUSE_PROJECTS === '1') {
    const cached = JSON.parse(await fs.readFile(OUTPUT_PATH, 'utf8'));
    projects = cached.projects || [];
  } else {
    projects = await mapLimit(validPlans, 4, async row => ({
      ...row,
      candidates: await candidatesFor(row.plan, row.center),
    }));
  }
  const pairs = projects.flatMap(project => (project.candidates || []).map(candidate => ({
    ...project,
    candidate,
  })));
  console.log(`Candidate pairs: ${pairs.length} from ${projects.filter(r => r.candidates?.length).length} projects`);

  console.log('Scoring with Jev...');
  const scoredProjects = await mapLimit(projects.filter(row => row.candidates?.length), 4, async project => {
    try {
      return await jevScoreProject(project);
    } catch (error) {
      return project.candidates.map(candidate => ({
        ...project,
        candidate,
        jev: null,
        jevError: error.message,
      }));
    }
  });
  const scored = scoredProjects.flatMap(row => Array.isArray(row) ? row : []);
  await fs.writeFile('/tmp/pbl-place-jev-scored.json', JSON.stringify(scored, null, 2));

  console.log('Building independent Qwen truth...');
  const judged = [];
  for (let start = 0; start < scored.length; start += 20) {
    const chunk = scored.slice(start, start + 20);
    const truth = await truthChunk(chunk);
    chunk.forEach((row, index) => {
      const label = truth.get(index) || { keep: false, reason: 'judge missing' };
      judged.push({ ...row, truth: label.keep, truthReason: label.reason });
    });
    console.log(`Truth ${Math.min(start + 20, scored.length)}/${scored.length}`);
  }

  const baseline = metrics(judged, () => true);
  const jev = metrics(judged, row => row.jev != null && row.jev >= JEV_THRESHOLD);
  const falseCaught = judged.filter(row => !row.truth && row.jev < JEV_THRESHOLD);
  const trueKilled = judged.filter(row => row.truth && row.jev < JEV_THRESHOLD);
  const falseLeaked = judged.filter(row => !row.truth && row.jev >= JEV_THRESHOLD);
  const trueKept = judged.filter(row => row.truth && row.jev >= JEV_THRESHOLD);
  const projectRawHit = new Set(judged.filter(row => row.truth).map(row => row.index)).size;
  const projectJevHit = new Set(trueKept.map(row => row.index)).size;
  const thresholdMetrics = [];
  for (let threshold = 0; threshold <= 0.8; threshold += 0.05) {
    thresholdMetrics.push({
      threshold: Math.round(threshold * 100) / 100,
      ...metrics(judged, row => row.jev != null && row.jev >= threshold),
    });
  }

  const result = {
    generatedAt: new Date().toISOString(),
    goalCount: goals.length,
    plannedCount: validPlans.length,
    campusOnlyCount: validPlans.filter(row => row.plan.campus_only).length,
    mappedProjectCount: projects.filter(row => row.candidates?.length).length,
    candidateCount: judged.length,
    truthPositiveCount: judged.filter(row => row.truth).length,
    projectRawHit,
    projectJevHit,
    threshold: JEV_THRESHOLD,
    thresholdMetrics,
    baseline,
    jev,
    deltas: {
      precision: jev.precision - baseline.precision,
      recall: jev.recall - baseline.recall,
      f1: jev.f1 - baseline.f1,
    },
    falseCaughtCount: falseCaught.length,
    trueKilledCount: trueKilled.length,
    falseLeakedCount: falseLeaked.length,
    samples: {
      trueKilled: trueKilled.slice(0, 30),
      falseLeaked: falseLeaked.slice(0, 30),
      falseCaught: falseCaught.slice(0, 20),
      trueKept: trueKept.slice(0, 20),
    },
    judged,
    projects,
  };
  await fs.writeFile(OUTPUT_PATH, JSON.stringify(result, null, 2));
  console.log(JSON.stringify({
    goalCount: result.goalCount,
    campusOnlyCount: result.campusOnlyCount,
    mappedProjectCount: result.mappedProjectCount,
    candidateCount: result.candidateCount,
    baseline,
    jev,
    deltas: result.deltas,
    projectRawHit,
    projectJevHit,
    falseCaught: falseCaught.length,
    trueKilled: trueKilled.length,
    falseLeaked: falseLeaked.length,
    output: OUTPUT_PATH,
  }, null, 2));
}

await main();
