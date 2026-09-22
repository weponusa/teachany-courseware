/**
 * POST /api/pbl/recall
 * Body: { task, deliverable, items: [{id, name, subject, point}] }  // max 36
 * Response: { fallback, reason, scores: [{id, name, subject, noul}] }
 */

import { jsonResponse, CORS } from '../../_lib/llm-backends.js';
import { logPBLCall } from '../../_lib/pbl-logger.js';
import { JEV_RECALL_CHUNK, scoreRecallChunk } from '../../_lib/pbl-jev-recall.js';

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}

export async function onRequestPost(context) {
  const { request, env } = context;
  let body;
  try {
    body = await request.json();
  } catch {
    return jsonResponse({ error: 'Invalid JSON' }, 400);
  }

  const task = String(body.task || '').trim();
  const items = Array.isArray(body.items) ? body.items : [];
  if (!task || task.length > 500) return jsonResponse({ error: 'Invalid task' }, 400);
  if (!items.length || items.length > JEV_RECALL_CHUNK) {
    return jsonResponse({ error: `items must be 1..${JEV_RECALL_CHUNK}` }, 400);
  }

  const t0 = Date.now();
  const result = await scoreRecallChunk(env, {
    task,
    deliverable: body.deliverable || '',
    items,
  });
  const elapsedMs = Date.now() - t0;
  await logPBLCall(env, {
    stage: 'jev-recall',
    goal: task,
    model: result.fallback ? '' : 'jev-latest',
    backend: result.fallback ? '' : 'typesafe',
    complex: false,
    latencyMs: elapsedMs,
    error: result.fallback ? result.reason : '',
    messages: [{ role: 'user', content: `召回 ${items.length} 条` }],
    responseText: JSON.stringify({
      reason: result.reason,
      scored: (result.scores || []).filter(s => s.noul != null).length,
    }),
    request,
  });
  return jsonResponse({ ...result, elapsedMs });
}
