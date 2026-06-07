/**
 * TeachAny LLM Proxy — Cloudflare Pages Function
 *
 * 路由：POST /api/llm/chat/completions
 * API Key 存在 Cloudflare Pages 的环境变量中
 */

const BACKENDS = {
  paratera: {
    name: '并行超算 GLM-4-Flash',
    baseUrl: 'https://llmapi.paratera.com/v1',
    defaultModel: 'GLM-4-Flash',
    envKey: 'PARATERA_KEY',
    free: true,
  },
  openrouter: {
    name: 'OpenRouter 免费模型',
    baseUrl: 'https://openrouter.ai/api/v1',
    defaultModel: 'qwen/qwen3-next-80b-a3b-instruct:free',
    envKey: 'OPENROUTER_KEY',
    free: true,
    extraHeaders: {
      'HTTP-Referer': 'https://www.teachany.cn',
      'X-Title': 'TeachAny-PBL',
    },
  },
};

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, X-Backend',
  'Access-Control-Max-Age': '86400',
};

function json(data, status = 200, extra = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS, ...extra },
  });
}

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}

export async function onRequestPost(context) {
  const { request, env } = context;

  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: 'Invalid JSON body' }, 400);
  }

  const backendHint = request.headers.get('X-Backend') || 'paratera';
  const backend = BACKENDS[backendHint] || BACKENDS.paratera;

  const apiKey = env[backend.envKey];
  if (!apiKey) {
    return json({ error: `Backend "${backendHint}" not configured` }, 503);
  }

  const model = body.model || backend.defaultModel;
  const forwardBody = { ...body, model };

  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${apiKey}`,
    ...(backend.extraHeaders || {}),
  };

  const endpoint = `${backend.baseUrl}/chat/completions`;

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 60000);

  try {
    const resp = await fetch(endpoint, {
      method: 'POST',
      headers,
      body: JSON.stringify(forwardBody),
      signal: controller.signal,
    });

    const data = await resp.text();

    if (!resp.ok) {
      console.error(`[LLM Proxy] ${backend.name} ${resp.status}: ${data.slice(0, 300)}`);
      return new Response(data, { status: resp.status, headers: { 'Content-Type': 'application/json', ...CORS } });
    }

    return new Response(data, {
      status: 200,
      headers: { 'Content-Type': 'application/json', ...CORS, 'X-Backend': backendHint, 'X-Model': model },
    });

  } catch (err) {
    if (err.name === 'AbortError') {
      return json({ error: `Backend "${backendHint}" timed out (25s)` }, 504);
    }
    return json({ error: err.message }, 502);
  } finally {
    clearTimeout(timeout);
  }
}

export async function onRequestGet(context) {
  const models = Object.entries(BACKENDS).map(([id, b]) => ({
    id, name: b.name, model: b.defaultModel, free: b.free,
  }));
  return json({ data: models });
}
