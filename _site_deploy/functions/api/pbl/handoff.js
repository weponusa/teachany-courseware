/**
 * PBL 拆解结果交接
 * POST /api/pbl/handoff  { goal, result, spec? } → { id, expiresAt }
 * GET  /api/pbl/handoff?id=UUID → { result, spec, goal }
 */

import { createPBLHandoff, getPBLHandoff } from '../../_lib/pbl-handoff.js';
import { CORS } from '../../_lib/llm-backends.js';

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}

export async function onRequestPost(context) {
  const { request, env } = context;
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: 'INVALID_JSON' }, 400);
  }
  const out = await createPBLHandoff(env, body);
  return json(out.body, out.status);
}

export async function onRequestGet(context) {
  const { request, env } = context;
  const id = new URL(request.url).searchParams.get('id');
  const out = await getPBLHandoff(env, id);
  return json(out.body, out.status);
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', ...CORS },
  });
}
