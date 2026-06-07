/**
 * OpenRouter 余额/用量查询（使用服务端 OPENROUTER_KEY）
 * GET /api/llm/credits?token=...  （若配置了 PBL_LOG_TOKEN）
 */

import { jsonResponse, CORS } from '../../_lib/llm-backends.js';

function assertToken(request, env) {
  const expected = String(env.PBL_LOG_TOKEN || '').trim();
  if (!expected) return true;
  const url = new URL(request.url);
  return String(url.searchParams.get('token') || request.headers.get('X-PBL-Log-Token') || '').trim() === expected;
}

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}

export async function onRequestGet(context) {
  const { request, env } = context;
  if (!assertToken(request, env)) {
    return jsonResponse({ error: 'Forbidden' }, 403);
  }

  const key = env.OPENROUTER_KEY;
  if (!key) {
    return jsonResponse({ error: 'OPENROUTER_KEY not configured' }, 503);
  }

  const headers = { Authorization: `Bearer ${key}` };
  const [keyResp, creditsResp] = await Promise.all([
    fetch('https://openrouter.ai/api/v1/key', { headers }),
    fetch('https://openrouter.ai/api/v1/credits', { headers }),
  ]);

  const keyInfo = await keyResp.json().catch(() => ({}));
  const credits = await creditsResp.json().catch(() => ({}));

  const d = keyInfo?.data || {};
  const c = credits?.data || {};

  return jsonResponse({
    ok: keyResp.ok || creditsResp.ok,
    account: {
      total_credits_usd: c.total_credits ?? null,
      total_usage_usd: c.total_usage ?? null,
      balance_usd: (c.total_credits != null && c.total_usage != null)
        ? Number((c.total_credits - c.total_usage).toFixed(4))
        : null,
    },
    api_key: {
      label: d.label || null,
      limit_usd: d.limit ?? null,
      limit_remaining_usd: d.limit_remaining ?? null,
      usage_all_time_usd: d.usage ?? null,
      usage_daily_usd: d.usage_daily ?? null,
      usage_weekly_usd: d.usage_weekly ?? null,
      usage_monthly_usd: d.usage_monthly ?? null,
      is_free_tier: d.is_free_tier ?? null,
    },
    raw: { key_status: keyResp.status, credits_status: creditsResp.status },
  });
}
