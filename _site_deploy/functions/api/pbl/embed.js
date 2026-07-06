/**
 * PBL 查询向量 — 服务端 embed（Key 不暴露给浏览器）
 * POST /api/pbl/embed  { text: string }
 * → { vector: number[], dim: number, model: string }
 */

import { embedText, jsonResponse, CORS, PBL_EMBED_MODEL, PBL_EMBED_DIM } from '../../_lib/pbl-embeddings.js';

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
  const text = String(body.text || '').trim();
  if (!text || text.length > 12000) {
    return jsonResponse({ error: 'Invalid text' }, 400);
  }
  try {
    const vector = await embedText(env, text);
    return jsonResponse({
      vector,
      dim: vector.length,
      model: PBL_EMBED_MODEL,
    });
  } catch (e) {
    const status = e.status && e.status >= 400 && e.status < 600 ? e.status : 502;
    return jsonResponse({ error: e.message || 'embed failed', detail: e.body || '' }, status);
  }
}
