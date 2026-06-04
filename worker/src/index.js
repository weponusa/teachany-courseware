/**
 * TeachAny LLM Proxy — Cloudflare Worker
 *
 * 把前端的 LLM API 调用转发到后端，API Key 存在 Worker Secrets 中。
 * 支持：Paratera GLM-4-Flash（默认）、OpenRouter 免费模型（备用）
 *
 * 路由：
 *   POST /v1/chat/completions   → 转发到后端 LLM API
 *   GET  /v1/models             → 返回可用模型列表
 *   GET  /health                → 健康检查
 */

// ─── 后端配置 ───────────────────────────────────────────
const BACKENDS = {
  paratera: {
    name: '并行超算 GLM-4-Flash',
    baseUrl: 'https://llmapi.paratera.com/v1',
    defaultModel: 'GLM-4-Flash',
    secretKey: 'PARATERA_KEY',     // wrangler secret 名称
    free: true,
  },
  openrouter: {
    name: 'OpenRouter 免费模型',
    baseUrl: 'https://openrouter.ai/api/v1',
    defaultModel: 'z-ai/glm-4.5-air:free',
    secretKey: 'OPENROUTER_KEY',
    free: true,
    extraHeaders: {
      'HTTP-Referer': 'https://www.teachany.cn',
      'X-Title': 'TeachAny-PBL',
    },
  },
};

// ─── CORS ───────────────────────────────────────────────
const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Backend',
  'Access-Control-Max-Age': '86400',
};

function corsResponse(body, status = 200, extraHeaders = {}) {
  return new Response(body, {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS_HEADERS, ...extraHeaders },
  });
}

// ─── 路由 ───────────────────────────────────────────────
export default {
  async fetch(request, env) {
    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    const url = new URL(request.url);
    const path = url.pathname;

    // 健康检查
    if (path === '/health') {
      return corsResponse(JSON.stringify({ ok: true, backends: Object.keys(BACKENDS) }));
    }

    // 模型列表
    if (path === '/v1/models' && request.method === 'GET') {
      const models = Object.entries(BACKENDS).map(([id, b]) => ({
        id,
        name: b.name,
        model: b.defaultModel,
        free: b.free,
      }));
      return corsResponse(JSON.stringify({ data: models }));
    }

    // Chat completions
    if (path === '/v1/chat/completions' && request.method === 'POST') {
      return handleChatCompletions(request, env);
    }

    return corsResponse(JSON.stringify({ error: 'Not found' }), 404);
  },
};

// ─── Chat Completions ──────────────────────────────────
async function handleChatCompletions(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    return corsResponse(JSON.stringify({ error: 'Invalid JSON body' }), 400);
  }

  // 从请求头或 query param 选择后端
  const backendHint = request.headers.get('X-Backend') || new URL(request.url).searchParams.get('backend') || 'paratera';
  const backend = BACKENDS[backendHint] || BACKENDS.paratera;

  // 从 Worker Secrets 获取 API Key（同步访问）
  const apiKey = env[backend.secretKey];
  if (!apiKey) {
    return corsResponse(JSON.stringify({
      error: `Backend "${backendHint}" not configured. Secret "${backend.secretKey}" not set.`,
    }), 503);
  }

  // 构建转发请求
  const model = body.model || backend.defaultModel;
  const forwardBody = { ...body, model };

  const forwardHeaders = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${apiKey}`,
    ...(backend.extraHeaders || {}),
  };

  const endpoint = `${backend.baseUrl}/chat/completions`;

  // 带超时的转发（Cloudflare Worker 上限 30s for free, 900s for paid）
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 60000);

  try {
    const resp = await fetch(endpoint, {
      method: 'POST',
      headers: forwardHeaders,
      body: JSON.stringify(forwardBody),
      signal: controller.signal,
    });

    const data = await resp.text();

    if (!resp.ok) {
      console.error(`[LLM Proxy] ${backend.name} ${resp.status}: ${data.slice(0, 300)}`);
      return corsResponse(data, resp.status);
    }

    return corsResponse(data, 200, { 'X-Backend': backendHint, 'X-Model': model });

  } catch (err) {
    if (err.name === 'AbortError') {
      return corsResponse(JSON.stringify({ error: `Backend "${backendHint}" timed out (25s)` }), 504);
    }
    return corsResponse(JSON.stringify({ error: err.message }), 502);
  } finally {
    clearTimeout(timeout);
  }
}
