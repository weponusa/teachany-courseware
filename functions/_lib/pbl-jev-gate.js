/**
 * Jev independent noul gate for PBL verify-relevance / review-curriculum.
 *
 * Production policy (39-item human truth, 2026-09-21):
 *   - independent noul, T=0.20 (batch scores are not interchangeable)
 *   - drop only when a score is present and < T
 *   - never auto-approve high scores; remaining items still go to the incumbent LLM
 *   - TypeSafe miss / error / timeout → skip gate (original pipeline unchanged)
 *
 * Independent noul prompt matches 旁路影子/shadow/jev_vs_truth.py.
 */

export const JEV_INDEPENDENT_THRESHOLD = 0.20;
export const JEV_PLACE_THRESHOLD = 0.50;
export const JEV_MODEL = 'jev-latest';
export const JEV_ENDPOINT = 'https://api.typesafe.ai/v1/systemone';

const CONCURRENCY = 8;
const PER_CALL_TIMEOUT_MS = 10000;
const GATE_BUDGET_MS = 14000;
const FAIL_RATIO_FALLBACK = 0.5;

function envOn(raw) {
  const v = String(raw || 'on').trim().toLowerCase();
  return v !== '0' && v !== 'false' && v !== 'off' && v !== 'no';
}

function typesafeKey(env) {
  return String(env?.TYPESAFE_API_KEY || env?.TYPESAFE_KEY || '').trim();
}

function knowledgeNeed(goal, deliverable) {
  const g = String(goal || '').trim();
  const d = String(deliverable || '').trim();
  return `${g}｜交付物：${d}`;
}

function candidateTitle(item) {
  return String(item?.name || item?.title || '').trim();
}

/** 校外 POI：只问这个地点能不能看见课题对象。名称里的普通词重合不算。 */
function placeKnowledgeNeed(goal, deliverable, placeLabel) {
  return [
    `课题：${String(goal || '').trim()}`,
    deliverable ? `要带回：${String(deliverable).trim()}` : '',
    placeLabel ? `出发地：${String(placeLabel).trim()}` : '',
    '需求：一次可到场的校外实践。学生要在对外开放区域直接看见课题对象，并说得出带回什么可复核证据。',
    '不要用「未来、科学、生态、能源、生活」这类修饰词去对地名。同城景点、名称沾边、比喻硬凑都不要召回。',
  ].filter(Boolean).join('｜');
}

function placeNoulBody(need, title) {
  return {
    model: JEV_MODEL,
    state: {
      knowledge_need: need,
      candidate: title,
    },
    questions: {
      matches: {
        type: 'noul',
        instructions: '候选地点 `candidate` 是这次校外实践该去的地方吗？只判断学生能否在这里直接看见课题对象。指得出「去这里看什么、带回什么证据」= true。地名里有相同的字、同城、类型沾边或比喻硬凑 = false。课题是氢能时，「未来科学城公园」只因为带了「未来」，必须判 false。',
        criteria: {
          true: '指得出在这个具体地点的开放区域能看见的对象，以及能带回的证据。',
          false: '看不出和课题对象的直接关系，只是地名、同城或硬凑。',
        },
      },
    },
  };
}

/** Independent noul body — identical to 旁路影子/shadow/jev_vs_truth.py. */
function independentNoulBody(need, title) {
  return {
    model: JEV_MODEL,
    state: {
      knowledge_need: need,
      candidate: title,
    },
    questions: {
      matches: {
        type: 'noul',
        instructions: '候选课标条目 `candidate` 会被这个项目的某个具体环节真实用到吗？指得出环节= true；只是主题相近/关键词重合/靠比喻硬凑= false。',
        criteria: {
          true: '指得出必须用到它的具体环节。',
          false: '指不出环节，只是相近或硬凑。',
        },
      },
    },
  };
}

function parseNoul(data) {
  const n = Number(data?.answers?.matches?.noul);
  return Number.isFinite(n) ? n : null;
}

async function scoreOne({ apiKey, need, title, signal, timeoutMs, kind }) {
  const controller = new AbortController();
  const onAbort = () => controller.abort();
  if (signal) {
    if (signal.aborted) throw new Error('aborted');
    signal.addEventListener('abort', onAbort, { once: true });
  }
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  const body = kind === 'place' ? placeNoulBody(need, title) : independentNoulBody(need, title);
  try {
    const resp = await fetch(JEV_ENDPOINT, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      signal: controller.signal,
    });
    const text = await resp.text();
    if (!resp.ok) {
      const err = new Error(`TypeSafe ${resp.status}`);
      err.status = resp.status;
      err.body = text.slice(0, 240);
      throw err;
    }
    return parseNoul(JSON.parse(text));
  } finally {
    clearTimeout(timer);
    if (signal) signal.removeEventListener('abort', onAbort);
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
  const n = Math.max(1, Math.min(limit, items.length));
  await Promise.all(Array.from({ length: n }, worker));
  return out;
}

export function extractJsonObject(text) {
  const s = String(text || '');
  const fence = s.match(/```(?:json)?\s*([\s\S]*?)```/);
  const raw = fence ? fence[1] : s;
  const start = raw.indexOf('{');
  const end = raw.lastIndexOf('}');
  if (start < 0 || end <= start) throw new Error('no json object');
  return JSON.parse(raw.slice(start, end + 1));
}

/**
 * Merge Jev drops into the LLM {remove, summary} payload.
 * LLM reason wins when both dropped the same index.
 */
export function mergeJevRemoves(llmJson, jevDrops, jevMeta) {
  const obj = llmJson && typeof llmJson === 'object' ? { ...llmJson } : { remove: [], summary: '' };
  const remove = Array.isArray(obj.remove) ? [...obj.remove] : [];
  const seen = new Set(
    remove
      .map(r => Number(r?.index))
      .filter(n => Number.isFinite(n)),
  );
  for (const drop of jevDrops || []) {
    const idx = Number(drop?.index);
    if (!Number.isFinite(idx) || seen.has(idx)) continue;
    seen.add(idx);
    remove.push({
      index: idx,
      reason: drop.reason || `Jev闸门 noul=${drop.noul} < ${JEV_INDEPENDENT_THRESHOLD}`,
    });
  }
  obj.remove = remove;
  if (jevMeta) obj.jevGate = jevMeta;
  return obj;
}

/**
 * @param {Record<string,string>} env
 * @param {{ goal: string, deliverable?: string, items: {index:number,name?:string,reason?:string}[], threshold?: number }} opts
 * @returns {Promise<{
 *   fallback: boolean,
 *   reason: string,
 *   threshold: number,
 *   scored: number,
 *   failed: number,
 *   drops: {index:number, noul:number, reason:string}[],
 *   scores: {index:number, name:string, noul:number|null, error?:string}[],
 *   elapsedMs: number,
 * }>}
 */
export async function runJevIndependentGate(env, opts) {
  const started = Date.now();
  const kind = opts?.kind === 'place' ? 'place' : 'curriculum';
  const threshold = Number.isFinite(opts?.threshold)
    ? opts.threshold
    : (kind === 'place' ? JEV_PLACE_THRESHOLD : JEV_INDEPENDENT_THRESHOLD);
  const items = Array.isArray(opts?.items) ? opts.items : [];
  const empty = {
    fallback: true,
    reason: 'empty',
    threshold,
    scored: 0,
    failed: 0,
    drops: [],
    scores: [],
    elapsedMs: 0,
  };

  if (!envOn(env?.PBL_JEV_GATE)) {
    return { ...empty, reason: 'disabled', elapsedMs: Date.now() - started };
  }
  const apiKey = typesafeKey(env);
  if (!apiKey) {
    return { ...empty, reason: 'no-key', elapsedMs: Date.now() - started };
  }
  if (!items.length) {
    return { ...empty, reason: 'no-items', fallback: false, elapsedMs: Date.now() - started };
  }

  const need = kind === 'place'
    ? placeKnowledgeNeed(opts.goal, opts.deliverable, opts.placeLabel)
    : knowledgeNeed(opts.goal, opts.deliverable);
  if (!need) {
    return { ...empty, reason: 'no-need', elapsedMs: Date.now() - started };
  }

  const deadline = started + GATE_BUDGET_MS;
  const abort = new AbortController();
  const budgetTimer = setTimeout(() => abort.abort(), GATE_BUDGET_MS);

  try {
    const scores = await mapPool(items, CONCURRENCY, async (item) => {
      const title = candidateTitle(item);
      const index = Number(item?.index);
      const row = { index, name: title, noul: null };
      if (!title) {
        row.error = 'no-title';
        return row;
      }
      const remain = deadline - Date.now();
      if (remain <= 200) {
        row.error = 'budget';
        return row;
      }
      try {
        row.noul = await scoreOne({
          apiKey,
          need,
          title,
          signal: abort.signal,
          timeoutMs: Math.min(PER_CALL_TIMEOUT_MS, remain),
          kind,
        });
        if (row.noul == null) row.error = 'no-noul';
      } catch (e) {
        row.error = e.name === 'AbortError' ? 'timeout' : (e.message || 'error');
      }
      return row;
    });

    const failed = scores.filter(s => s.noul == null).length;
    if (failed / scores.length >= FAIL_RATIO_FALLBACK) {
      return {
        fallback: true,
        reason: 'too-many-failures',
        threshold,
        scored: scores.length - failed,
        failed,
        drops: [],
        scores,
        elapsedMs: Date.now() - started,
      };
    }

    const drops = scores
      .filter(s => s.noul != null && s.noul < threshold)
      .map(s => ({
        index: s.index,
        noul: s.noul,
        reason: `Jev闸门 noul=${s.noul.toFixed(2)} < ${threshold.toFixed(2)}`,
      }));

    return {
      fallback: false,
      reason: 'ok',
      threshold,
      scored: scores.length - failed,
      failed,
      drops,
      scores,
      elapsedMs: Date.now() - started,
    };
  } catch (e) {
    return {
      ...empty,
      reason: e.message || 'gate-error',
      elapsedMs: Date.now() - started,
    };
  } finally {
    clearTimeout(budgetTimer);
  }
}
