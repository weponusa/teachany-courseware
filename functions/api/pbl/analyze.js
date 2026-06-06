/**
 * PBL 拆解 LLM 网关 — 提示词仅存在于服务端
 * POST /api/pbl/analyze
 *
 * Body: {
 *   stage: 'filter' | 'match',
 *   goal: string,
 *   summaryList?: string,      // filter 阶段
 *   candidates?: object[],     // match 阶段（精简字段即可）
 *   complex?: boolean,
 *   maxMatched?: number,
 *   minConf?: number,
 *   clientLlm?: { baseUrl, apiKey, model, noAuth }  // 可选：用户自带 Key，仍走服务端提示词
 * }
 *
 * Response: { content: string }  // LLM 原始文本（JSON）
 */

import { buildPBMessages } from '../../_lib/pbl-prompts.js';
import { callBackendLLM, jsonResponse, CORS } from '../../_lib/llm-backends.js';

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

  const stage = body.stage;
  if (stage !== 'filter' && stage !== 'match') {
    return jsonResponse({ error: 'Invalid stage' }, 400);
  }

  const goal = String(body.goal || '').trim();
  if (!goal || goal.length > 2000) {
    return jsonResponse({ error: 'Invalid goal' }, 400);
  }

  if (stage === 'match' && (!Array.isArray(body.candidates) || body.candidates.length === 0)) {
    return jsonResponse({ error: 'candidates required' }, 400);
  }

  if (stage === 'match' && body.candidates.length > 50) {
    return jsonResponse({ error: 'Too many candidates' }, 400);
  }

  let messages;
  try {
    messages = buildPBMessages(stage, {
      goal,
      summaryList: body.summaryList || '',
      candidates: body.candidates || [],
      complex: !!body.complex,
      maxMatched: body.maxMatched || (body.complex ? 12 : 18),
      minConf: body.minConf ?? (body.complex ? 0.68 : 0.52),
      domainHints: body.domainHints || null,
    });
  } catch (e) {
    return jsonResponse({ error: e.message }, 400);
  }

  const llmOpts = {
    // v2.0 提示词要求更大的结构化输出（matched+dependsOn+knowledgeChain+projectPhases+techRoute），
    // 提高 match 的 token 上限，避免 JSON 尾部被截断导致解析失败、知识图谱为空。
    maxTokens: stage === 'match' ? 8000 : 1200,
    temperature: stage === 'match' ? 0.15 : 0.25,
    clientLlm: body.clientLlm,
  };

  try {
    const content = await callBackendLLM(env, messages, llmOpts);
    return jsonResponse({ content });
  } catch (e) {
    const status = e.status && e.status >= 400 && e.status < 600 ? e.status : 502;
    return jsonResponse({ error: e.message || 'LLM failed', detail: e.body || '' }, status);
  }
}
