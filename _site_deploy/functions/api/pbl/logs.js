/**
 * PBL LLM 调用日志查询
 * GET /api/pbl/logs?limit=50&stage=match&goal=食堂&format=json|ndjson
 * 若配置了环境变量 PBL_LOG_TOKEN，需带 ?token= 或头 X-PBL-Log-Token
 */

import { queryPBLLogs } from '../../_lib/pbl-logger.js';
import { CORS } from '../../_lib/llm-backends.js';

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}

export async function onRequestGet(context) {
  const { request, env } = context;
  const result = await queryPBLLogs(request, env);

  if (result.raw) {
    return new Response(result.body, {
      status: result.status,
      headers: { ...CORS, ...result.headers },
    });
  }

  return new Response(JSON.stringify(result.body, null, 2), {
    status: result.status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', ...CORS },
  });
}
