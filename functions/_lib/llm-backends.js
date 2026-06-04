/** @internal TeachAny LLM 后端配置（仅 Pages Functions，不对外暴露） */

export const BACKENDS = {
  paratera: {
    name: '并行超算 GLM-4-Flash',
    baseUrl: 'https://llmapi.paratera.com/v1',
    defaultModel: 'GLM-4-Flash',
    envKey: 'PARATERA_KEY',
    extraHeaders: {},
  },
  openrouter: {
    name: 'OpenRouter',
    baseUrl: 'https://openrouter.ai/api/v1',
    defaultModel: 'z-ai/glm-4.5-air:free',
    envKey: 'OPENROUTER_KEY',
    extraHeaders: {
      'HTTP-Referer': 'https://www.teachany.cn',
      'X-Title': 'TeachAny-PBL',
    },
  },
};

export const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Backend',
  'Access-Control-Max-Age': '86400',
};

export function jsonResponse(data, status = 200, extra = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS, ...extra },
  });
}

/**
 * @param {Record<string,string>} env
 * @param {object[]} messages
 * @param {{ maxTokens?: number, temperature?: number, clientLlm?: object }} opts
 */
export async function callBackendLLM(env, messages, opts = {}) {
  const client = opts.clientLlm;
  let baseUrl;
  let apiKey;
  let model;
  let extraHeaders = {};

  if (client && client.apiKey && !client.noAuth) {
    baseUrl = String(client.baseUrl || '').replace(/\/$/, '');
    apiKey = client.apiKey;
    model = client.model || BACKENDS.paratera.defaultModel;
    if (baseUrl.includes('openrouter.ai')) {
      extraHeaders = { 'HTTP-Referer': 'https://www.teachany.cn', 'X-Title': 'TeachAny-PBL' };
    }
  } else {
    const backend = BACKENDS.paratera;
    apiKey = env[backend.envKey];
    if (!apiKey) throw new Error('LLM backend not configured');
    baseUrl = backend.baseUrl;
    model = backend.defaultModel;
    extraHeaders = backend.extraHeaders || {};
  }

  const endpoint = /\/chat\/completions/.test(baseUrl)
    ? baseUrl
    : `${baseUrl}/chat/completions`;

  const body = {
    model,
    messages,
    stream: false,
    temperature: opts.temperature ?? 0.2,
    max_tokens: opts.maxTokens ?? 4500,
  };

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 60000);
  try {
    const resp = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
        ...extraHeaders,
      },
      body: JSON.stringify(body),
      signal: controller.signal,
    });
    const text = await resp.text();
    if (!resp.ok) {
      const err = new Error(`LLM ${resp.status}`);
      err.status = resp.status;
      err.body = text.slice(0, 400);
      throw err;
    }
    const data = JSON.parse(text);
    const message = data.choices?.[0]?.message || {};
    return message.content || message.reasoning || message.reasoning_content || '';
  } finally {
    clearTimeout(timeout);
  }
}
