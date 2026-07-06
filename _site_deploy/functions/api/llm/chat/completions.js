/**
 * TeachAny LLM Proxy — Cloudflare Pages Function
 *
 * 路由：POST /api/llm/chat/completions
 * API Key 仅存服务端环境变量，供 AI 学伴 / 自定义客户端中转
 */

import {
  BACKENDS,
  CORS,
  inferBackendIdForModel,
  jsonResponse,
} from '../../../_lib/llm-backends.js';

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}

export async function onRequestPost(context) {
  const { request, env } = context;

  let body;
  try {
    body = await request.json();
  } catch {
    return jsonResponse({ error: 'Invalid JSON body' }, 400);
  }

  const model = body.model || '';
  const backendId = request.headers.get('X-Backend')
    || inferBackendIdForModel(model)
    || 'openrouter';
  const backend = BACKENDS[backendId] || BACKENDS.openrouter;

  const apiKey = env[backend.envKey];
  if (!apiKey) {
    return jsonResponse({ error: `Backend "${backendId}" not configured` }, 503);
  }

  const resolvedModel = model || backend.defaultModel;
  const forwardBody = { ...body, model: resolvedModel };
  const endpoint = `${backend.baseUrl.replace(/\/$/, '')}/chat/completions`;

  const headers = {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${apiKey}`,
    ...(backend.extraHeaders || {}),
  };
  const title = request.headers.get('X-Title') || request.headers.get('X-OpenRouter-Title');
  if (title && backendId === 'openrouter') {
    headers['X-Title'] = String(title).slice(0, 100);
    headers['HTTP-Referer'] = headers['HTTP-Referer'] || 'https://www.teachany.cn';
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 60000);

  try {
    const resp = await fetch(endpoint, {
      method: 'POST',
      headers,
      body: JSON.stringify(forwardBody),
      signal: controller.signal,
    });

    const contentType = resp.headers.get('content-type') || 'application/json';

    if (!resp.ok) {
      const data = await resp.text();
      console.error(`[LLM Proxy] ${backend.name} ${resp.status}: ${data.slice(0, 300)}`);
      return new Response(data, {
        status: resp.status,
        headers: { 'Content-Type': contentType, ...CORS },
      });
    }

    if (body.stream && resp.body) {
      return new Response(resp.body, {
        status: resp.status,
        headers: {
          ...CORS,
          'Content-Type': contentType,
          'X-Backend': backendId,
          'X-Model': resolvedModel,
        },
      });
    }

    const data = await resp.text();
    return new Response(data, {
      status: 200,
      headers: {
        'Content-Type': contentType,
        ...CORS,
        'X-Backend': backendId,
        'X-Model': resolvedModel,
      },
    });
  } catch (err) {
    if (err.name === 'AbortError') {
      return jsonResponse({ error: `Backend "${backendId}" timed out (60s)` }, 504);
    }
    return jsonResponse({ error: err.message }, 502);
  } finally {
    clearTimeout(timeout);
  }
}

export async function onRequestGet() {
  const models = Object.entries(BACKENDS).map(([id, b]) => ({
    id, name: b.name, model: b.defaultModel,
  }));
  return jsonResponse({ data: models });
}
