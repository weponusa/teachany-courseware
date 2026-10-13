/**
 * PBL recall flow: subject×stage catalog → Jev independent noul (title + one curriculum line)
 * → drop noul < 0.20 → top-K for the incumbent judge.
 *
 * Jev does not approve keeps, does not judge redundancy, and does not override a judge drop.
 * Usage:
 *   source ~/.workbuddy/secrets/typesafe.env
 *   node scripts/pbl-jev-recall-flow.mjs
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const TREE_DIR = path.join(ROOT, 'data/trees/cn/middle');
const ENDPOINT = 'https://api.typesafe.ai/v1/systemone';
const THRESHOLD = 0.20;
const SUBJECT_ANCHOR = 0.70;
const TOP_K = 16;
const CONCURRENCY = 8;

const LIVE_ELEVEN = [
  '数据结构基础（列表/字典）',
  '折射规律应用',
  '网页与在线应用制作',
  '数据分析与可视化',
  '发电机原理',
  '概率',
  '隐私保护与数据安全',
  '变量与函数',
  '主题词汇（校园/家庭/社会/自然）',
  '开源硬件与模块化设计',
  '结构/原子',
];

function knowledgeNeed(task, deliverable) {
  const d = String(deliverable || '').trim();
  return d ? `${task}｜交付物：${d}` : task;
}

export function jevBody(need, title, definition) {
  return {
    model: 'jev-latest',
    state: {
      knowledge_need: need,
      candidate: title,
      candidate_point: definition || '',
    },
    questions: {
      matches: {
        type: 'noul',
        instructions: '候选课标条目 `candidate` 会被这个项目的某个具体环节真实用到吗？课标要求在 `candidate_point`。只根据这条要求判断，不要根据标题里的近义词。指得出环节= true；只是主题相近、关键词重合或靠比喻硬凑= false。',
        criteria: {
          true: '指得出必须用到这条课标要求的具体环节。',
          false: '指不出环节，只是标题相近或硬凑。',
        },
      },
    },
  };
}

export function loadMiddleCatalog(dir = TREE_DIR) {
  const nodes = [];
  for (const file of fs.readdirSync(dir).filter(f => f.endsWith('.json')).sort()) {
    const subject = file.replace(/\.json$/, '');
    const tree = JSON.parse(fs.readFileSync(path.join(dir, file), 'utf8'));
    const walk = (domains) => {
      for (const domain of domains || []) {
        for (const node of domain.nodes || []) {
          const point = String((node.curriculum_points || [])[0] || '').trim();
          nodes.push({
            id: node.id,
            name: node.name,
            subject,
            grade: node.grade || 0,
            point,
          });
        }
        walk(domain.domains || []);
      }
    };
    walk(tree.domains || []);
  }
  return nodes;
}

async function scoreOne(apiKey, need, node) {
  const resp = await fetch(ENDPOINT, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(jevBody(need, node.name, node.point)),
  });
  const text = await resp.text();
  if (!resp.ok) {
    const err = new Error(`TypeSafe ${resp.status}: ${text.slice(0, 180)}`);
    err.status = resp.status;
    throw err;
  }
  const data = JSON.parse(text);
  const noul = Number(data?.answers?.matches?.noul);
  return Number.isFinite(noul) ? noul : null;
}

async function mapPool(items, limit, fn) {
  const out = new Array(items.length);
  let next = 0;
  let done = 0;
  async function worker() {
    while (next < items.length) {
      const i = next++;
      out[i] = await fn(items[i], i);
      done += 1;
      if (done % 40 === 0 || done === items.length) {
        process.stderr.write(`scored ${done}/${items.length}\n`);
      }
    }
  }
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, worker));
  return out;
}

export function selectRecall(scored, { threshold = THRESHOLD, anchor = SUBJECT_ANCHOR, topK = TOP_K } = {}) {
  const ranked = [...scored].filter(s => s.noul != null).sort((a, b) => b.noul - a.noul);
  const droppedLow = ranked.filter(s => s.noul < threshold);
  const maxBySubject = new Map();
  for (const row of ranked) {
    const prev = maxBySubject.get(row.subject);
    if (prev == null || row.noul > prev) maxBySubject.set(row.subject, row.noul);
  }
  const subjects = [...maxBySubject.entries()]
    .filter(([, max]) => max >= anchor)
    .map(([subject]) => subject);
  const kept = ranked
    .filter(s => subjects.includes(s.subject) && s.noul >= threshold)
    .slice(0, topK);
  return { ranked, droppedLow, subjects, maxBySubject: Object.fromEntries(maxBySubject), kept };
}

async function main() {
  const apiKey = String(process.env.TYPESAFE_API_KEY || '').trim();
  if (!apiKey) {
    console.error('missing TYPESAFE_API_KEY');
    process.exit(1);
  }
  const task = process.argv[2] || '做一个交换校服的小程序';
  const deliverable = process.argv[3] || '校服交换小程序可运行原型';
  const need = knowledgeNeed(task, deliverable);
  const catalog = loadMiddleCatalog();
  const t0 = Date.now();
  const scored = await mapPool(catalog, CONCURRENCY, async (node) => {
    let noul = null;
    let error = '';
    for (let attempt = 0; attempt < 2; attempt++) {
      try {
        noul = await scoreOne(apiKey, need, node);
        error = noul == null ? 'no-noul' : '';
        if (noul != null) break;
      } catch (e) {
        error = e.message || 'error';
        if (attempt === 0 && ![401, 403].includes(e.status)) {
          await new Promise(r => setTimeout(r, 500));
          continue;
        }
        break;
      }
    }
    return { ...node, noul, error };
  });
  const { ranked, droppedLow, subjects, maxBySubject, kept } = selectRecall(scored);
  const byName = new Map(ranked.map(s => [s.name, s]));
  const live = LIVE_ELEVEN.map(name => byName.get(name) || { name, noul: null, missing: true });
  const result = {
    need,
    catalog: catalog.length,
    failed: scored.filter(s => s.noul == null).length,
    threshold: THRESHOLD,
    subjectAnchor: SUBJECT_ANCHOR,
    subjects,
    maxBySubject,
    elapsedMs: Date.now() - t0,
    droppedLow: droppedLow.length,
    kept,
    liveRescored: live,
    top30: ranked.slice(0, 30),
    scores: ranked,
  };
  const out = path.join('/tmp', 'pbl-jev-recall-uniform.json');
  fs.writeFileSync(out, JSON.stringify(result, null, 2));
  console.log(JSON.stringify({
    out,
    catalog: result.catalog,
    failed: result.failed,
    droppedLow: result.droppedLow,
    subjects: result.subjects,
    subjectMax: Object.entries(result.maxBySubject)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 8)
      .map(([subject, noul]) => ({ subject, noul: Number(noul.toFixed(2)) })),
    elapsedMs: result.elapsedMs,
    kept: kept.map(s => ({ name: s.name, subject: s.subject, noul: s.noul, point: s.point })),
    live: live.map(s => ({ name: s.name, subject: s.subject, noul: s.noul, missing: !!s.missing })),
  }, null, 2));
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((e) => {
    console.error(e);
    process.exit(1);
  });
}
