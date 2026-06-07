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
    defaultModel: 'qwen/qwen3-next-80b-a3b-instruct:free',
    envKey: 'OPENROUTER_KEY',
    extraHeaders: {
      'HTTP-Referer': 'https://www.teachany.cn',
      'X-Title': 'TeachAny-PBL',
    },
  },
};

/**
 * PBL 专用模型链（服务端预设，前端不可改）
 * 可通过环境变量 PBL_MODEL_OVERRIDE 临时锁定单模型做 A/B（如 deepseek/deepseek-v4-flash）
 *
 * 默认顺序：
 * 1. DeepSeek V4 Flash — 中文 + 结构化 JSON 强，速度/成本均衡（OpenRouter 付费）
 * 2. GLM-4-Flash — 稳定快速兜底
 * 3. Qwen3 Next 80B / Llama 3.3 70B — 免费备选
 */
export const PBL_MODEL_CHAIN = [
  { backendId: 'openrouter', model: 'deepseek/deepseek-v4-flash' },
  { backendId: 'paratera', model: 'GLM-4-Flash' },
  { backendId: 'openrouter', model: 'qwen/qwen3-next-80b-a3b-instruct:free' },
  { backendId: 'openrouter', model: 'meta-llama/llama-3.3-70b-instruct:free' },
];

/** @param {Record<string,string>} env */
export function resolvePBLModelChain(env = {}) {
  const override = String(env.PBL_MODEL_OVERRIDE || '').trim();
  if (override) {
    const backendId = override.includes('/') ? 'openrouter' : 'paratera';
    return [{ backendId, model: override }];
  }
  return PBL_MODEL_CHAIN;
}

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

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function callSingleModel(env, backendId, model, messages, opts) {
  const backend = BACKENDS[backendId];
  if (!backend) throw new Error(`Unknown backend: ${backendId}`);

  const apiKey = env[backend.envKey];
  if (!apiKey) {
    const err = new Error(`Backend "${backendId}" not configured`);
    err.status = 503;
    throw err;
  }

  const baseUrl = backend.baseUrl.replace(/\/$/, '');
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
  const timeout = setTimeout(() => controller.abort(), opts.timeoutMs ?? 55000);
  try {
    const resp = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
        ...(backend.extraHeaders || {}),
      },
      body: JSON.stringify(body),
      signal: controller.signal,
    });
    const text = await resp.text();
    if (!resp.ok) {
      const err = new Error(`LLM ${resp.status} (${backendId}/${model})`);
      err.status = resp.status;
      err.body = text.slice(0, 400);
      throw err;
    }
    const data = JSON.parse(text);
    const message = data.choices?.[0]?.message || {};
    const content = message.content || message.reasoning || message.reasoning_content || '';
    if (!content) {
      const err = new Error(`LLM empty response (${backendId}/${model})`);
      err.status = 502;
      throw err;
    }
    return content;
  } finally {
    clearTimeout(timeout);
  }
}

/**
 * @param {Record<string,string>} env
 * @param {object[]} messages
 * @param {{ maxTokens?: number, temperature?: number, modelChain?: {backendId:string,model:string}[], timeoutMs?: number }} opts
 * @returns {Promise<{ content: string, model: string, backendId: string }>}
 */
export async function callBackendLLM(env, messages, opts = {}) {
  const chain = opts.modelChain || resolvePBLModelChain(env);
  let lastError;

  for (let i = 0; i < chain.length; i++) {
    const { backendId, model } = chain[i];
    try {
      const content = await callSingleModel(env, backendId, model, messages, opts);
      return { content, model, backendId };
    } catch (e) {
      lastError = e;
      const retryable = e.status === 429 || e.status === 503 || e.status === 502 || e.name === 'AbortError';
      if (retryable && i < chain.length - 1) {
        await sleep(Math.min(4000 + i * 2000, 12000));
        continue;
      }
      if (!retryable) throw e;
    }
  }

  throw lastError || new Error('LLM failed');
}
