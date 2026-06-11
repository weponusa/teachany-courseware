/**
 * PBL 拆解 LLM 网关 — 提示词与模型仅存在于服务端
 * POST /api/pbl/analyze
 *
 * Body: {
 *   stage: 'decompose' | 'review-decompose' | 'filter' | 'propose-curriculum' | 'validate-match' | 'match' | 'verify-relevance' | 'review-curriculum' | 'verify-deps' | 'refine',
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
import { buildVerifyRelevanceMessages } from '../../_lib/pbl-verify-relevance-prompts.js';
import { buildReviewCurriculumMessages } from '../../_lib/pbl-review-curriculum-prompts.js';
import { buildRefineMessages } from '../../_lib/pbl-refine-prompts.js';
import { buildReviewDecomposeMessages } from '../../_lib/pbl-review-decompose-prompts.js';
import { buildProposeCurriculumMessages } from '../../_lib/pbl-propose-curriculum-prompts.js';
import { buildValidateMatchMessages } from '../../_lib/pbl-validate-match-prompts.js';
import {
  buildUserModelChain,
  callBackendLLM,
  jsonResponse,
  CORS,
  resolvePBLStageModelChain,
} from '../../_lib/llm-backends.js';
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
  if (stage !== 'decompose' && stage !== 'review-decompose' && stage !== 'filter' && stage !== 'match'
    && stage !== 'propose-curriculum' && stage !== 'validate-match'
    && stage !== 'verify-relevance' && stage !== 'review-curriculum'
    && stage !== 'verify-deps' && stage !== 'refine') {
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

  if (stage === 'refine' && !String(body.userMessage || '').trim()) {
    return jsonResponse({ error: 'userMessage required' }, 400);
  }

  if (stage === 'review-decompose' && (!body.projectBlueprint || !body.projectBlueprint.schemes?.length)) {
    return jsonResponse({ error: 'projectBlueprint with schemes required' }, 400);
  }

  if (stage === 'verify-relevance' && (!Array.isArray(body.matched) || body.matched.length === 0)) {
    return jsonResponse({ error: 'matched required' }, 400);
  }

  if (stage === 'verify-relevance' && body.matched.length > 24) {
    return jsonResponse({ error: 'Too many matched' }, 400);
  }

  if (stage === 'review-curriculum' && (!Array.isArray(body.nodes) || body.nodes.length === 0)) {
    return jsonResponse({ error: 'nodes required' }, 400);
  }

  if (stage === 'review-curriculum' && body.nodes.length > 28) {
    return jsonResponse({ error: 'Too many nodes' }, 400);
  }

  if (stage === 'verify-deps' && (!Array.isArray(body.edges) || body.edges.length === 0)) {
    return jsonResponse({ error: 'edges required' }, 400);
  }

  if (stage === 'verify-deps' && body.edges.length > 24) {
    return jsonResponse({ error: 'Too many edges' }, 400);
  }

  if (stage === 'validate-match' && (!Array.isArray(body.linked) || body.linked.length === 0)) {
    return jsonResponse({ error: 'linked required' }, 400);
  }

  if (stage === 'validate-match' && body.linked.length > 24) {
    return jsonResponse({ error: 'Too many linked nodes' }, 400);
  }

  let messages;
  try {
    if (stage === 'verify-deps') {
      messages = buildVerifyDepsMessages({ goal, edges: body.edges });
    } else if (stage === 'verify-relevance') {
      messages = buildVerifyRelevanceMessages({
        goal,
        deliverable: body.deliverable || '',
        projectBlueprint: body.projectBlueprint || null,
        matched: body.matched || [],
      });
    } else if (stage === 'review-curriculum') {
      messages = buildReviewCurriculumMessages({
        goal,
        deliverable: body.deliverable || '',
        projectBlueprint: body.projectBlueprint || null,
        projectSpec: body.projectSpec || null,
        nodes: body.nodes || [],
      });
    } else if (stage === 'propose-curriculum') {
      messages = buildProposeCurriculumMessages({
        goal,
        projectBlueprint: body.projectBlueprint || null,
        projectSpec: body.projectSpec || null,
        deliverable: body.deliverable || '',
        maxProposed: body.maxProposed || (body.complex ? 12 : 14),
      });
    } else if (stage === 'validate-match') {
      messages = buildValidateMatchMessages({
        goal,
        projectBlueprint: body.projectBlueprint || null,
        deliverable: body.deliverable || '',
        projectSpec: body.projectSpec || null,
        linked: body.linked || [],
      });
    } else if (stage === 'refine') {
      messages = buildRefineMessages({
        goal,
        userMessage: body.userMessage || '',
        projectSpec: body.projectSpec || null,
        snapshot: body.snapshot || {},
      });
    } else if (stage === 'review-decompose') {
      messages = buildReviewDecomposeMessages({
        goal,
        projectBlueprint: body.projectBlueprint,
        reviewIssues: body.reviewIssues || [],
        complex: !!body.complex,
      });
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
      : (stage === 'validate-match' ? 6000
        : (stage === 'decompose' || stage === 'review-decompose' ? 5000
          : (stage === 'propose-curriculum' ? 3000
            : (stage === 'verify-relevance' || stage === 'review-curriculum' ? 3500
              : (stage === 'refine' ? 2500
                : (stage === 'verify-deps' ? 2500 : 1200)))))),
    temperature: stage === 'match' ? 0.15
      : (stage === 'validate-match' ? 0.1
        : (stage === 'decompose' ? 0.35
          : (stage === 'review-decompose' ? 0.12
            : (stage === 'propose-curriculum' ? 0.25
              : (stage === 'verify-relevance' || stage === 'review-curriculum' ? 0.05
                : (stage === 'refine' ? 0.2
                  : (stage === 'verify-deps' ? 0.08 : 0.25))))))),
  };

  const userModel = String(body.model || '').trim();
  const providerId = String(body.providerId || '').trim();
  if (userModel || providerId) {
    llmOpts.modelChain = buildUserModelChain(env, userModel, providerId);
  } else {
    llmOpts.modelChain = resolvePBLStageModelChain(env, stage);
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
