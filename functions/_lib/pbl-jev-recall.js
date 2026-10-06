/**
 * Catalog recall: independent noul on title + one curriculum line.
 * Drop noul < 0.20. A subject stays only if its best score is >= 0.70.
 * Chunk size stays at 36 so one Worker invocation stays under the subrequest cap.
 */

export const JEV_RECALL_THRESHOLD = 0.20;
export const JEV_SUBJECT_ANCHOR = 0.70;
export const JEV_RECALL_TOP_K = 16;
export const JEV_RECALL_CHUNK = 36;

const ENDPOINT = 'https://api.typesafe.ai/v1/systemone';
const CONCURRENCY = 8;
const PER_CALL_TIMEOUT_MS = 8000;

function knowledgeNeed(task, deliverable) {
  const d = String(deliverable || '').trim();
  return d ? `${String(task || '').trim()}｜交付物：${d}` : String(task || '').trim();
}

export function recallNeed(task, deliverable) {
  return knowledgeNeed(task, deliverable);
}

function recallBody(need, title, point) {
  return {
    model: 'jev-latest',
    state: {
      knowledge_need: need,
      candidate: title,
      candidate_point: point || '',
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

async function scoreOne(apiKey, need, item) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), PER_CALL_TIMEOUT_MS);
  try {
    const resp = await fetch(ENDPOINT, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(recallBody(need, item.name, item.point)),
      signal: controller.signal,
    });
    const text = await resp.text();
    if (!resp.ok) {
      const err = new Error(`TypeSafe ${resp.status}`);
      err.status = resp.status;
      throw err;
    }
    const noul = Number(JSON.parse(text)?.answers?.matches?.noul);
    return Number.isFinite(noul) ? noul : null;
  } finally {
    clearTimeout(timer);
  }
}

async function mapPool(items, limit, fn) {
  const out = new Array(items.length);
  let next = 0;
  async function worker() {
    while (next < items.length) {
      const i = next++;
      out[i] = await fn(items[i], i);
    }
  }
  await Promise.all(Array.from({ length: Math.max(1, Math.min(limit, items.length)) }, worker));
  return out;
}

export function selectJevRecall(scored, { threshold = JEV_RECALL_THRESHOLD, anchor = JEV_SUBJECT_ANCHOR, topK = JEV_RECALL_TOP_K } = {}) {
  const ranked = (scored || [])
    .filter(s => Number.isFinite(Number(s?.noul)))
    .map(s => ({ ...s, noul: Number(s.noul) }))
    .sort((a, b) => b.noul - a.noul);
  const maxBySubject = new Map();
  for (const row of ranked) {
    const subject = String(row.subject || '');
    const prev = maxBySubject.get(subject);
    if (prev == null || row.noul > prev) maxBySubject.set(subject, row.noul);
  }
  const subjects = [...maxBySubject.entries()]
    .filter(([, max]) => max >= anchor)
    .map(([subject]) => subject);
  const kept = ranked
    .filter(s => subjects.includes(String(s.subject || '')) && s.noul >= threshold)
    .slice(0, topK);
  return { kept, subjects, droppedLow: ranked.filter(s => s.noul < threshold).length };
}

/**
 * Score one chunk. Caller chunks to JEV_RECALL_CHUNK.
 */
export async function scoreRecallChunk(env, { task, deliverable, items }) {
  const apiKey = String(env?.TYPESAFE_API_KEY || env?.TYPESAFE_KEY || '').trim();
  const list = Array.isArray(items) ? items.slice(0, JEV_RECALL_CHUNK) : [];
  if (!apiKey) return { fallback: true, reason: 'no-key', scores: [] };
  if (!list.length) return { fallback: true, reason: 'no-items', scores: [] };
  const need = knowledgeNeed(task, deliverable);
  if (!need) return { fallback: true, reason: 'no-need', scores: [] };

  const scores = await mapPool(list, CONCURRENCY, async (item) => {
    const row = {
      id: String(item?.id || ''),
      name: String(item?.name || '').trim(),
      subject: String(item?.subject || ''),
      noul: null,
    };
    if (!row.name) {
      row.error = 'no-title';
      return row;
    }
    try {
      row.noul = await scoreOne(apiKey, need, { name: row.name, point: String(item?.point || '') });
      if (row.noul == null) row.error = 'no-noul';
    } catch (e) {
      row.error = e.name === 'AbortError' ? 'timeout' : (e.message || 'error');
    }
    return row;
  });

  const failed = scores.filter(s => s.noul == null).length;
  if (failed / scores.length >= 0.5) {
    return { fallback: true, reason: 'too-many-failures', scores };
  }
  return { fallback: false, reason: 'ok', scores };
}
