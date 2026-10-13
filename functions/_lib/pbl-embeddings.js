/** @internal PBL 课标节点向量：embed 查询 + cosine 工具 */

export const PBL_EMBED_MODEL = 'openai/text-embedding-3-small';
export const PBL_EMBED_DIM = 512;

export const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Access-Control-Max-Age': '86400',
};

export function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS },
  });
}

/** @param {number[]} a @param {number[]} b */
export function cosineSimilarity(a, b) {
  if (!a?.length || !b?.length || a.length !== b.length) return -1;
  let dot = 0;
  let na = 0;
  let nb = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    na += a[i] * a[i];
    nb += b[i] * b[i];
  }
  const denom = Math.sqrt(na) * Math.sqrt(nb);
  return denom > 0 ? dot / denom : -1;
}

/**
 * @param {Record<string,string>} env
 * @param {string} text
 * @param {{ model?: string, dimensions?: number }} [opts]
 */
export async function embedText(env, text, opts = {}) {
  const key = env.OPENROUTER_KEY;
  if (!key) {
    const err = new Error('OPENROUTER_KEY not configured');
    err.status = 503;
    throw err;
  }
  const model = opts.model || PBL_EMBED_MODEL;
  const dimensions = opts.dimensions || PBL_EMBED_DIM;
  const input = String(text || '').trim().slice(0, 8000);
  if (!input) {
    const err = new Error('empty text');
    err.status = 400;
    throw err;
  }

  const resp = await fetch('https://openrouter.ai/api/v1/embeddings', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${key}`,
      'HTTP-Referer': 'https://www.teachany.cn',
      'X-Title': 'TeachAny-PBL-Embed',
    },
    body: JSON.stringify({
      model,
      input,
      dimensions,
    }),
  });
  const raw = await resp.text();
  if (!resp.ok) {
    const err = new Error(`embed ${resp.status}`);
    err.status = resp.status;
    err.body = raw.slice(0, 300);
    throw err;
  }
  const data = JSON.parse(raw);
  const vec = data?.data?.[0]?.embedding;
  if (!Array.isArray(vec) || !vec.length) {
    const err = new Error('empty embedding');
    err.status = 502;
    throw err;
  }
  return vec.map(Number);
}

/** @param {number[]} query @param {{ id: string, e: number[] }[]} entries @param {number} k */
export function topKByCosine(query, entries, k = 60) {
  const scored = [];
  for (const item of entries) {
    if (!item?.id || !item?.e?.length) continue;
    const s = cosineSimilarity(query, item.e);
    if (s > 0) scored.push({ id: item.id, score: s });
  }
  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, k);
}
