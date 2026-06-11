/** @internal PBL 拆解结果交接 — 跨会话/跨设备恢复完整图谱 */

const MAX_PAYLOAD = 480000;
const TTL_DAYS = 7;

function getDb(env) {
  return env.TEACHANY_DB || env.DB || null;
}

function clipJson(obj, max = MAX_PAYLOAD) {
  let s = JSON.stringify(obj);
  if (s.length <= max) return s;
  const trimmed = { ...obj };
  if (trimmed.result?.graphData) {
    const gd = trimmed.result.graphData;
    trimmed.result = {
      ...trimmed.result,
      graphData: {
        nodes: (gd.nodes || []).slice(0, 40),
        links: (gd.links || []).slice(0, 80),
      },
      truncated: true,
    };
    s = JSON.stringify(trimmed);
  }
  if (s.length > max) {
    return JSON.stringify({
      goal: trimmed.goal || '',
      result: { goal: trimmed.goal || '', graphData: trimmed.result?.graphData || { nodes: [], links: [] }, truncated: true },
      spec: trimmed.spec || null,
    });
  }
  return s;
}

function addDaysIso(days) {
  const d = new Date();
  d.setUTCDate(d.getUTCDate() + days);
  return d.toISOString().slice(0, 19).replace('T', ' ');
}

/**
 * @param {object} env
 * @param {{ goal: string, result: object, spec?: object }} payload
 */
export async function createPBLHandoff(env, payload) {
  const db = getDb(env);
  if (!db) return { ok: false, status: 503, body: { error: 'D1_NOT_CONFIGURED', message: 'PBL handoff 需要绑定 TEACHANY_DB' } };

  const goal = String(payload?.goal || payload?.result?.goal || '').trim();
  if (!goal || !payload?.result) {
    return { ok: false, status: 400, body: { error: 'INVALID_PAYLOAD', message: '缺少 goal 或 result' } };
  }

  const id = crypto.randomUUID();
  const expiresAt = addDaysIso(TTL_DAYS);
  const json = clipJson({ goal, result: payload.result, spec: payload.spec || null });

  await db.prepare(
    'INSERT INTO pbl_handoffs (id, expires_at, goal, payload_json) VALUES (?, ?, ?, ?)'
  ).bind(id, expiresAt, goal.slice(0, 2000), json).run();

  return { ok: true, status: 200, body: { id, expiresAt, goal } };
}

/**
 * @param {object} env
 * @param {string} id
 */
export async function getPBLHandoff(env, id) {
  const db = getDb(env);
  if (!db) return { ok: false, status: 503, body: { error: 'D1_NOT_CONFIGURED' } };

  const handoffId = String(id || '').trim();
  if (!handoffId) return { ok: false, status: 400, body: { error: 'MISSING_ID' } };

  const row = await db.prepare(
    'SELECT id, goal, payload_json, expires_at FROM pbl_handoffs WHERE id = ? AND expires_at > datetime(\'now\')'
  ).bind(handoffId).first();

  if (!row) return { ok: false, status: 404, body: { error: 'NOT_FOUND', message: '交接记录不存在或已过期' } };

  let payload;
  try {
    payload = JSON.parse(row.payload_json);
  } catch {
    return { ok: false, status: 500, body: { error: 'CORRUPT_PAYLOAD' } };
  }

  return {
    ok: true,
    status: 200,
    body: {
      id: row.id,
      goal: row.goal,
      expiresAt: row.expires_at,
      result: payload.result,
      spec: payload.spec || null,
    },
  };
}
