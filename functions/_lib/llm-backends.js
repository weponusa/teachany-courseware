/** @internal TeachAny LLM 后端配置（仅 Pages Functions，不对外暴露） */

export const BACKENDS = {
  siliconflow: {
    name: '硅基流动 DeepSeek-V4-Flash',
    baseUrl: 'https://api.siliconflow.cn/v1',
    defaultModel: 'deepseek-ai/DeepSeek-V4-Flash',
    envKey: 'SILICONFLOW_KEY',
    extraHeaders: {},
  },
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

/** @param {string} model */
export function inferBackendIdForModel(model) {
  const m = String(model || '').trim();
  if (!m) return 'siliconflow';
  if (!m.includes('/')) return 'paratera';
  if (/^(deepseek-ai|Qwen|THUDM|zai-org|baidu|tencent|moonshotai|MiniMax|Pro\/)/i.test(m)) {
    return 'siliconflow';
  }
  return 'openrouter';
}

/**
 * PBL 专用模型链（默认链；前端可选模型时用户指定模型优先）
 * 可通过环境变量 PBL_MODEL_OVERRIDE 临时锁定单模型做 A/B
 *
 * 默认顺序：
 * 1. 硅基流动 DeepSeek-V4-Flash — PBL 主模型
 * 2. GLM-4-Flash — 并行超算兜底
 */
export const PBL_MODEL_CHAIN = [
  { backendId: 'siliconflow', model: 'deepseek-ai/DeepSeek-V4-Flash' },
  { backendId: 'paratera', model: 'GLM-4-Flash' },
];

/** match / verify-relevance / refine：默认与主链一致（硅基 Flash），可通过 PBL_MATCH_MODEL 覆盖 */
export const PBL_MATCH_MODEL_CHAIN = [
  { backendId: 'siliconflow', model: 'deepseek-ai/DeepSeek-V4-Flash' },
  { backendId: 'siliconflow', model: 'deepseek-ai/DeepSeek-V4-Pro' },
  { backendId: 'paratera', model: 'GLM-4-Flash' },
];

const PBL_STRONG_STAGES = new Set(['match', 'verify-relevance', 'review-curriculum', 'refine']);

/** @param {Record<string,string>} env */
export function resolvePBLModelChain(env = {}) {
  const override = String(env.PBL_MODEL_OVERRIDE || '').trim();
  if (override) {
    return [{ backendId: inferBackendIdForModel(override), model: override }];
  }
  return PBL_MODEL_CHAIN;
}

/** @param {Record<string,string>} env @param {string} stage */
export function resolvePBLStageModelChain(env = {}, stage = '') {
  if (!PBL_STRONG_STAGES.has(stage)) return resolvePBLModelChain(env);
  const matchOverride = String(env.PBL_MATCH_MODEL || env.PBL_MODEL_OVERRIDE || '').trim();
  if (matchOverride) {
    return [{ backendId: inferBackendIdForModel(matchOverride), model: matchOverride }];
  }
  return PBL_MATCH_MODEL_CHAIN;
}

/** 前端服务商 id → 服务端 backendId（preset/custom 走模型推断） */
const PROVIDER_BACKEND = {
  siliconflow: 'siliconflow',
  paratera: 'paratera',
  openrouter: 'openrouter',
};

/**
 * 用户自选模型优先，再拼接默认兜底链（去重）
 * @param {Record<string,string>} env
 * @param {string} userModel
 * @param {string} [providerId] 用户选择的服务商（非 preset 时优先于模型名推断）
 */
export function buildUserModelChain(env, userModel, providerId = '') {
  const m = String(userModel || '').trim();
  const pid = String(providerId || '').trim();
  if (!m && !pid) return resolvePBLModelChain(env);

  const forcedBackend = PROVIDER_BACKEND[pid];
  const model = m || BACKENDS[forcedBackend]?.defaultModel || '';
  if (!model) return resolvePBLModelChain(env);

  const backendId = forcedBackend || inferBackendIdForModel(model);
  const chain = [{ backendId, model }];
  for (const item of resolvePBLModelChain(env)) {
    if (item.model !== model) chain.push(item);
  }
  return chain;
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
