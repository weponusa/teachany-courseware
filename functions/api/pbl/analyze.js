/**
 * PBL 拆解 LLM 网关 — 提示词与模型仅存在于服务端
 * POST /api/pbl/analyze
 *
 * Body: {
 *   stage: 'decompose' | 'filter' | 'match' | 'verify-deps',
 *   model?: string,          // 可选：用户自选模型（服务端 Key 调用）
 *   providerId?: string,     // 可选：siliconflow | paratera | openrouter（与 model 配合）
 *   messagesOnly?: boolean,  // 可选：仅返回 messages，供自定义 API 客户端直连
 *   goal: string,
 *   summaryList?: string,
 *   candidates?: object[],
 *   complex?: boolean,
 *   maxMatched?: number,
 *   minConf?: number,
 *   domainHints?: object[],
 *   projectBlueprint?: object,
 *   bloomProfile?: object,
 *   archetypeId?: string,
 *   edges?: object[]
 * }
 *
 * Response: { content: string, model: string, backend: string }
 */

import { buildPBMessages } from '../../_lib/pbl-prompts.js';
import { buildVerifyDepsMessages } from '../../_lib/pbl-verify-prompts.js';
import { buildUserModelChain, callBackendLLM, jsonResponse, CORS } from '../../_lib/llm-backends.js';
import { logPBLCall } from '../../_lib/pbl-logger.js';

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
  if (stage !== 'decompose' && stage !== 'filter' && stage !== 'match' && stage !== 'verify-deps') {
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

  if (stage === 'verify-deps' && (!Array.isArray(body.edges) || body.edges.length === 0)) {
    return jsonResponse({ error: 'edges required' }, 400);
  }

  if (stage === 'verify-deps' && body.edges.length > 24) {
    return jsonResponse({ error: 'Too many edges' }, 400);
  }

  let messages;
  try {
    if (stage === 'verify-deps') {
      messages = buildVerifyDepsMessages({ goal, edges: body.edges });
    } else {
      messages = buildPBMessages(stage, {
        goal,
        summaryList: body.summaryList || '',
        candidates: body.candidates || [],
        complex: !!body.complex,
        maxMatched: body.maxMatched || (body.complex ? 12 : 18),
        minConf: body.minConf ?? (body.complex ? 0.68 : 0.52),
        domainHints: body.domainHints || null,
        projectBlueprint: body.projectBlueprint || null,
        bloomProfile: body.bloomProfile || null,
        archetypeId: body.archetypeId || null,
      });
    }
  } catch (e) {
    return jsonResponse({ error: e.message }, 400);
  }

  if (body.messagesOnly) {
    return jsonResponse({
      messages,
      model: String(body.model || '').trim(),
    });
  }

  const llmOpts = {
    maxTokens: stage === 'match' ? 8000
      : (stage === 'decompose' ? 4500
        : (stage === 'verify-deps' ? 2500 : 1200)),
    temperature: stage === 'match' ? 0.15
      : (stage === 'decompose' ? 0.35
        : (stage === 'verify-deps' ? 0.08 : 0.25)),
  };

  const userModel = String(body.model || '').trim();
  const providerId = String(body.providerId || '').trim();
  if (userModel || providerId) {
    llmOpts.modelChain = buildUserModelChain(env, userModel, providerId);
  }

  const t0 = Date.now();
  try {
    const { content, model, backendId } = await callBackendLLM(env, messages, llmOpts);
    const latencyMs = Date.now() - t0;

    await logPBLCall(env, {
      stage,
      goal,
      model,
      backend: backendId,
      complex: !!body.complex,
      latencyMs,
      error: '',
      messages,
      responseText: content,
      request,
    });

    return jsonResponse({ content, model, backend: backendId });
  } catch (e) {
    const latencyMs = Date.now() - t0;
    await logPBLCall(env, {
      stage,
      goal,
      model: '',
      backend: '',
      complex: !!body.complex,
      latencyMs,
      error: e.message || 'LLM failed',
      messages,
      responseText: e.body || '',
      request,
    });

    const status = e.status && e.status >= 400 && e.status < 600 ? e.status : 502;
    return jsonResponse({ error: e.message || 'LLM failed', detail: e.body || '' }, status);
  }
}
