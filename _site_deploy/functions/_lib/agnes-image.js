/** @internal TeachAny 课件生图 — Agnes API 服务端中转 + 配额 */

export const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, X-TeachAny-Client',
  'Access-Control-Max-Age': '86400',
};

export const AGNES_MODEL = 'agnes-image-2.1-flash';
export const AGNES_API_URL = 'https://apihub.agnes-ai.com/v1/images/generations';

const ALLOWED_SIZES = new Set(['512x512', '768x768', '1024x1024', '1024x768', '1280x768', '768x1280']);
const NO_TEXT_SUFFIX = '\n\nSTRICT: NO TEXT, NO LETTERS, NO NUMBERS, NO WATERMARK, no Chinese characters. Educational illustration only.';

export function jsonResponse(data, status = 200, extra = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', ...CORS, ...extra },
  });
}

export function getDb(env) {
  return env.TEACHANY_DB || env.DB || null;
}

export function getPerCourseLimit(env) {
  const n = parseInt(String(env.IMAGE_GEN_PER_COURSE_LIMIT || '3'), 10);
  return Number.isFinite(n) && n > 0 ? Math.min(n, 10) : 3;
}

export function getIpRpmLimit(env) {
  const n = parseInt(String(env.IMAGE_GEN_IP_RPM || '10'), 10);
  return Number.isFinite(n) && n > 0 ? Math.min(n, 60) : 10;
}

/** @param {string} raw */
export function normalizeCourseId(raw) {
  const id = String(raw || '').trim().toLowerCase();
  if (!/^[a-z0-9][a-z0-9_-]{2,79}$/.test(id)) return null;
  if (id.startsWith('_') && id !== '_preflight_probe') return null;
  return id;
}

async function sha256Hex(text) {
  const data = new TextEncoder().encode(String(text || ''));
  const digest = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(digest)).map(b => b.toString(16).padStart(2, '0')).join('');
}

/** @param {string} ip */
export async function hashIp(ip) {
  if (!ip || !crypto?.subtle) return '';
  return (await sha256Hex(ip)).slice(0, 24);
}

/** @param {string} prompt */
export function buildCoursewarePrompt(prompt) {
  const base = String(prompt || '').trim();
  if (!base) return '';
  const max = 1800;
  const clipped = base.length > max ? base.slice(0, max) + '…' : base;
  if (/NO TEXT|no text|无文字|禁止文字/i.test(clipped)) return clipped;
  return clipped + NO_TEXT_SUFFIX;
}

/** @param {string} size */
export function normalizeSize(size) {
  const s = String(size || '1280x768').trim().toLowerCase();
  return ALLOWED_SIZES.has(s) ? s : '1280x768';
}

/**
 * @param {import('@cloudflare/workers-types').D1Database} db
 * @param {string} courseId
 * @param {number} limit
 */
export async function getCourseQuota(db, courseId, limit) {
  const row = await db.prepare(
    'SELECT used_count FROM courseware_image_quota WHERE course_id = ?'
  ).bind(courseId).first();
  const used = Number(row?.used_count || 0);
  return { used, limit, remaining: Math.max(0, limit - used) };
}

/**
 * @param {import('@cloudflare/workers-types').D1Database} db
 * @param {string} ipHash
 * @param {number} rpmLimit
 */
export async function getIpUsageLastMinute(db, ipHash, rpmLimit) {
  if (!ipHash) return { count: 0, limit: rpmLimit, exceeded: false };
  const row = await db.prepare(`
    SELECT COUNT(*) AS cnt FROM courseware_image_gen_logs
    WHERE ip_hash = ? AND datetime(created_at) > datetime('now', '-1 minute')
  `).bind(ipHash).first();
  const count = Number(row?.cnt || 0);
  return { count, limit: rpmLimit, exceeded: count >= rpmLimit };
}

/**
 * @param {import('@cloudflare/workers-types').D1Database} db
 * @param {string} courseId
 * @param {number} limit
 */
export async function reserveCourseImageSlot(db, courseId, limit) {
  try {
    const ins = await db.prepare(
      'INSERT INTO courseware_image_quota (course_id, used_count) VALUES (?, 1)'
    ).bind(courseId).run();
    if (ins.success) {
      return { reserved: true, used: 1, remaining: limit - 1 };
    }
  } catch (e) {
    if (!String(e?.message || e).includes('UNIQUE')) throw e;
  }

  const upd = await db.prepare(`
    UPDATE courseware_image_quota
    SET used_count = used_count + 1, updated_at = datetime('now')
    WHERE course_id = ? AND used_count < ?
  `).bind(courseId, limit).run();

  if ((upd.meta?.changes || 0) > 0) {
    const q = await getCourseQuota(db, courseId, limit);
    return { reserved: true, used: q.used, remaining: q.remaining };
  }

  const q = await getCourseQuota(db, courseId, limit);
  return { reserved: false, used: q.used, remaining: q.remaining };
}

/** @param {import('@cloudflare/workers-types').D1Database} db @param {string} courseId */
export async function releaseCourseImageSlot(db, courseId) {
  await db.prepare(`
    UPDATE courseware_image_quota
    SET used_count = CASE WHEN used_count > 0 THEN used_count - 1 ELSE 0 END,
        updated_at = datetime('now')
    WHERE course_id = ?
  `).bind(courseId).run();
}

/**
 * @param {import('@cloudflare/workers-types').D1Database} db
 * @param {object} entry
 */
export async function logImageGen(db, entry) {
  await db.prepare(`
    INSERT INTO courseware_image_gen_logs (
      course_id, slot, prompt, size, remote_url, latency_ms, error, ip_hash, user_agent
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
  `).bind(
    String(entry.courseId || '').slice(0, 80),
    String(entry.slot || '').slice(0, 32),
    String(entry.prompt || '').slice(0, 2000),
    String(entry.size || '').slice(0, 16),
    String(entry.remoteUrl || '').slice(0, 2000),
    entry.latencyMs == null ? null : Number(entry.latencyMs),
    String(entry.error || '').slice(0, 500),
    String(entry.ipHash || '').slice(0, 24),
    String(entry.userAgent || '').slice(0, 500),
  ).run();
}

/**
 * @param {Record<string,string>} env
 * @param {string} prompt
 * @param {string} size
 */
export async function callAgnesImage(env, prompt, size) {
  const apiKey = String(env.AGNES_API_KEY || '').trim();
  if (!apiKey) {
    const err = new Error('AGNES_API_KEY not configured on server');
    err.status = 503;
    throw err;
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 120000);

  try {
    const resp = await fetch(AGNES_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model: AGNES_MODEL,
        prompt,
        n: 1,
        size,
      }),
      signal: controller.signal,
    });

    const data = await resp.json().catch(() => ({}));
    if (!resp.ok) {
      const msg = data?.error?.message || data?.error || JSON.stringify(data).slice(0, 300);
      const err = new Error(`Agnes HTTP ${resp.status}: ${msg}`);
      err.status = resp.status === 429 ? 429 : 502;
      throw err;
    }

    const url = data?.data?.[0]?.url;
    if (!url) {
      const err = new Error('Agnes response missing image url');
      err.status = 502;
      throw err;
    }

    return { url, model: AGNES_MODEL, raw: data };
  } catch (e) {
    if (e?.name === 'AbortError') {
      const err = new Error('Agnes image generation timeout (120s)');
      err.status = 504;
      throw err;
    }
    throw e;
  } finally {
    clearTimeout(timeout);
  }
}
