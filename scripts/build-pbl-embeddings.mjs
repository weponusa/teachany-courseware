#!/usr/bin/env node
/**
 * 离线构建 PBL 课标节点 embedding（K12 CN 为主）
 *
 *   OPENROUTER_KEY=sk-... node scripts/build-pbl-embeddings.mjs
 *   node scripts/build-pbl-embeddings.mjs --dry-run
 *   node scripts/build-pbl-embeddings.mjs --limit=200
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, '..');
const OUT = path.join(ROOT, 'data/pbl/node-embeddings.json');
const MODEL = 'openai/text-embedding-3-small';
const LOCAL_MODEL = 'local-hash-v1';
const DIM = 512;
const BATCH = 40;

function localHashEmbed(text, dim = DIM) {
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

function loadKey() {
  if (process.env.OPENROUTER_KEY) return process.env.OPENROUTER_KEY;
  try {
    const s = fs.readFileSync(path.join(ROOT, 'scripts/ai-tutor.js'), 'utf8');
    const m = s.match(/const _k1 = '([^']+)';\s*const _k2 = '([^']+)';\s*const _k3 = '([^']+)';\s*const _k4 = '([^']+)'/);
    return m ? m[1] + m[2] + m[3] + m[4] : '';
  } catch {
    return '';
  }
}

function walkJsonFiles(dir, out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const name of fs.readdirSync(dir)) {
    const p = path.join(dir, name);
    const st = fs.statSync(p);
    if (st.isDirectory()) walkJsonFiles(p, out);
    else if (name.endsWith('.json')) out.push(p);
  }
  return out;
}

function collectNodes() {
  const byId = new Map();
  const add = (n, meta = {}) => {
    if (!n?.id || !n?.name) return;
    const grade = parseInt(n.grade, 10) || 0;
    if (grade < 1 || grade > 12) return;
    const system = meta.system || 'cn';
    if (system !== 'cn') return;
    const name = String(n.name || n.name_zh || '').trim();
    if (!name) return;
    const def = String(n.definition || n.description || '').replace(/\s+/g, ' ').slice(0, 240);
    const cp = (n.curriculum_points || []).slice(0, 5).join(' ');
    const subj = n.subject || meta.subject || '';
    const domain = meta.domain ? `领域:${meta.domain}` : '';
    const text = [name, def, cp, subj ? `学科:${subj}` : '', domain, `G${grade}`].filter(Boolean).join(' | ');
    byId.set(n.id, { id: n.id, name, grade, subject: subj, text });
  };

  walkJsonFiles(path.join(ROOT, 'data/trees/cn')).forEach(file => {
    try {
      const j = JSON.parse(fs.readFileSync(file, 'utf8'));
      const subject = j.subject || '';
      (j.nodes || []).forEach(n => add(n, { subject, system: 'cn' }));
      (j.domains || []).forEach(d => {
        (d.nodes || []).forEach(n => add({ ...n, subject: n.subject || subject }, {
          subject: n.subject || subject,
          domain: d.name || d.id,
          system: 'cn',
        }));
      });
    } catch { /* skip */ }
  });

  const kmPath = path.join(ROOT, 'data/knowledge-map-data.json');
  if (fs.existsSync(kmPath)) {
    const km = JSON.parse(fs.readFileSync(kmPath, 'utf8'));
    (km.nodes || []).forEach(n => add(n, { system: 'cn' }));
  }

  return [...byId.values()];
}

async function embedBatch(key, texts) {
  const resp = await fetch('https://openrouter.ai/api/v1/embeddings', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${key}`,
      'HTTP-Referer': 'https://www.teachany.cn',
      'X-Title': 'TeachAny-PBL-Embed-Build',
    },
    body: JSON.stringify({ model: MODEL, input: texts, dimensions: DIM }),
  });
  const raw = await resp.text();
  if (!resp.ok) throw new Error(`embed ${resp.status}: ${raw.slice(0, 200)}`);
  const data = JSON.parse(raw);
  const items = data?.data || [];
  if (items.length !== texts.length) throw new Error(`embed count mismatch ${items.length}/${texts.length}`);
  return items.sort((a, b) => (a.index ?? 0) - (b.index ?? 0)).map(x => x.embedding.map(Number));
}

async function main() {
  const dryRun = process.argv.includes('--dry-run');
  const useLocal = process.argv.includes('--local');
  const limitArg = process.argv.find(a => a.startsWith('--limit='));
  const limit = limitArg ? parseInt(limitArg.split('=')[1], 10) : 0;

  let nodes = collectNodes();
  console.log(`收集 K12 CN 节点: ${nodes.length}`);
  if (limit > 0) nodes = nodes.slice(0, limit);

  if (dryRun) {
    nodes.slice(0, 5).forEach(n => console.log('-', n.name, '|', n.text.slice(0, 80)));
    return;
  }

  const built = [];

  if (useLocal) {
    console.log('使用本地 hash 向量（无需 API，精度低于 OpenAI embed）');
    nodes.forEach(n => built.push({ id: n.id, e: localHashEmbed(n.text) }));
  } else {
    const key = loadKey();
    if (!key) {
      console.warn('无 OPENROUTER_KEY，回退 --local');
      nodes.forEach(n => built.push({ id: n.id, e: localHashEmbed(n.text) }));
    } else {
      for (let i = 0; i < nodes.length; i += BATCH) {
        const batch = nodes.slice(i, i + BATCH);
        process.stdout.write(`embed ${i + 1}-${i + batch.length}/${nodes.length} ... `);
        try {
          const vecs = await embedBatch(key, batch.map(n => n.text));
          batch.forEach((n, j) => built.push({ id: n.id, e: vecs[j] }));
          console.log('ok');
        } catch (e) {
          console.error('API 失败，对本批使用 local hash:', e.message);
          batch.forEach(n => built.push({ id: n.id, e: localHashEmbed(n.text) }));
        }
        await new Promise(r => setTimeout(r, 300));
      }
    }
  }

  const usedModel = useLocal || !loadKey() ? LOCAL_MODEL : MODEL;
  const out = {
    version: 1,
    model: usedModel,
    dim: DIM,
    builtAt: new Date().toISOString(),
    count: built.length,
    nodes: built,
  };
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, JSON.stringify(out));
  const mb = (fs.statSync(OUT).size / 1024 / 1024).toFixed(2);
  console.log(`✅ wrote ${OUT} (${built.length} nodes, ${mb} MB)`);
}

main().catch(e => {
  console.error(e);
  process.exit(1);
});
