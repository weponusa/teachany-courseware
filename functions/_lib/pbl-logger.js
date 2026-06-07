/** @internal PBL LLM 调用日志 — 写入 D1，可通过 /api/pbl/logs 查询 */

const MAX_TEXT = 120000;

function getDb(env) {
  return env.TEACHANY_DB || env.DB || null;
}

async function sha256Hex(text) {
  const data = new TextEncoder().encode(String(text || ''));
  const digest = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(digest)).map(b => b.toString(16).padStart(2, '0')).join('');
}

async function hashIp(ip) {
  if (!ip || !crypto?.subtle) return '';
  return (await sha256Hex(ip)).slice(0, 24);
}

function clip(text, max = MAX_TEXT) {
  const s = String(text ?? '');
  return s.length > max ? s.slice(0, max) + '\n…[truncated]' : s;
}

/**
 * @param {object} env
 * @param {object} entry
 */
export async function logPBLCall(env, entry) {
  const db = getDb(env);
  if (!db) {
    console.warn('[PBL Log] D1 not configured, skip persist');
    return null;
  }

  const {
    stage,
    goal,
    model = '',
    backend = '',
    complex = false,
    latencyMs = null,
    error = '',
    messages = [],
    responseText = '',
    request,
  } = entry;

  const ipHash = request ? await hashIp(request.headers.get('CF-Connecting-IP') || '') : '';
  const userAgent = request ? String(request.headers.get('User-Agent') || '').slice(0, 500) : '';

  try {
    const result = await db.prepare(`
      INSERT INTO pbl_llm_logs (
        stage, goal, model, backend, complex, latency_ms, error,
        messages_json, response_text, user_agent, ip_hash
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `).bind(
      String(stage || '').slice(0, 32),
      String(goal || '').slice(0, 2000),
      String(model || '').slice(0, 120),
      String(backend || '').slice(0, 64),
      complex ? 1 : 0,
      latencyMs == null ? null : Number(latencyMs),
      String(error || '').slice(0, 2000),
      clip(JSON.stringify(messages)),
      clip(responseText),
      userAgent,
      ipHash,
    ).run();
    return result.meta?.last_row_id || null;
  } catch (e) {
    console.error('[PBL Log] insert failed:', e.message);
    return null;
  }
}

function assertLogToken(request, env) {
  const expected = String(env.PBL_LOG_TOKEN || '').trim();
  if (!expected) return { ok: true, protected: false };
  const url = new URL(request.url);
  const provided = String(
    url.searchParams.get('token')
    || request.headers.get('X-PBL-Log-Token')
    || ''
  ).trim();
  if (provided !== expected) {
    return { ok: false, status: 403, message: 'Invalid or missing PBL log token' };
  }
  return { ok: true, protected: true };
}

/**
 * @param {Request} request
 * @param {object} env
 */
export async function queryPBLLogs(request, env) {
  const db = getDb(env);
  if (!db) {
    return {
      status: 503,
      body: {
        ok: false,
        error: 'D1_NOT_CONFIGURED',
        message: 'PBL 日志需要绑定 TEACHANY_DB，并执行 migrations/0002_pbl_llm_logs.sql',
      },
    };
  }

  const auth = assertLogToken(request, env);
  if (!auth.ok) {
    return { status: auth.status, body: { ok: false, error: 'FORBIDDEN', message: auth.message } };
  }

  const url = new URL(request.url);
  const format = url.searchParams.get('format') || 'json';
  const limit = Math.min(Math.max(parseInt(url.searchParams.get('limit') || '50', 10), 1), 500);
  const stage = url.searchParams.get('stage') || '';
  const goalLike = url.searchParams.get('goal') || '';

  let query = `SELECT id, created_at, stage, goal, model, backend, complex, latency_ms, error,
    substr(messages_json, 1, 8000) AS messages_json,
    substr(response_text, 1, 8000) AS response_text
    FROM pbl_llm_logs`;
  const binds = [];
  const clauses = [];
  if (stage) {
    clauses.push('stage = ?');
    binds.push(stage);
  }
  if (goalLike) {
    clauses.push('goal LIKE ?');
    binds.push(`%${goalLike}%`);
  }
  if (clauses.length) query += ` WHERE ${clauses.join(' AND ')}`;
  query += ' ORDER BY datetime(created_at) DESC LIMIT ?';
  binds.push(limit);

  const result = await db.prepare(query).bind(...binds).all();
  const rows = result.results || [];

  if (format === 'ndjson' || format === 'jsonl') {
    const lines = rows.map(r => JSON.stringify(r)).join('\n');
    return {
      status: 200,
      raw: true,
      headers: {
        'Content-Type': 'application/x-ndjson; charset=utf-8',
        'Content-Disposition': 'attachment; filename=pbl-llm-logs.ndjson',
      },
      body: lines + (lines ? '\n' : ''),
    };
  }

  return {
    status: 200,
    body: { ok: true, count: rows.length, rows },
  };
}
