/**
 * PBL 主 Key 余额查询（硅基流动 + 可选 OpenRouter 备用信息）
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

  const sfKey = env.SILICONFLOW_KEY;
  const orKey = env.OPENROUTER_KEY;

  if (!sfKey && !orKey) {
    return jsonResponse({ error: 'SILICONFLOW_KEY / OPENROUTER_KEY not configured' }, 503);
  }

  const result = {
    ok: false,
    pbl_primary: { provider: 'siliconflow', model: 'deepseek-ai/DeepSeek-V4-Flash' },
    siliconflow: null,
    openrouter: null,
  };

  if (sfKey) {
    const sfResp = await fetch('https://api.siliconflow.cn/v1/user/info', {
      headers: { Authorization: `Bearer ${sfKey}` },
    });
    const sf = await sfResp.json().catch(() => ({}));
    const data = sf?.data || sf || {};
    result.siliconflow = {
      status: sfResp.status,
      balance_cny: data.balance ?? data.totalBalance ?? null,
      charge_balance_cny: data.chargeBalance ?? null,
      raw: data,
    };
    if (sfResp.ok) result.ok = true;
  }

  if (orKey) {
    const headers = { Authorization: `Bearer ${orKey}` };
    const [keyResp, creditsResp] = await Promise.all([
      fetch('https://openrouter.ai/api/v1/key', { headers }),
      fetch('https://openrouter.ai/api/v1/credits', { headers }),
    ]);
    const keyInfo = await keyResp.json().catch(() => ({}));
    const credits = await creditsResp.json().catch(() => ({}));
    const d = keyInfo?.data || {};
    const c = credits?.data || {};
    result.openrouter = {
      key_status: keyResp.status,
      credits_status: creditsResp.status,
      limit_remaining_usd: d.limit_remaining ?? null,
      usage_monthly_usd: d.usage_monthly ?? null,
      balance_usd: (c.total_credits != null && c.total_usage != null)
        ? Number((c.total_credits - c.total_usage).toFixed(4))
        : null,
    };
  }

  return jsonResponse(result);
}
