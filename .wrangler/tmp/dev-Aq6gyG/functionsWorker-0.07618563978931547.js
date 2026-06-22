var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });

// ../../.wrangler/tmp/pages-cUfSv3/functionsWorker-0.07618563978931547.mjs
var __defProp2 = Object.defineProperty;
var __name2 = /* @__PURE__ */ __name((target, value) => __defProp2(target, "name", { value, configurable: true }), "__name");
var BACKENDS = {
  paratera: {
    name: "\u5E76\u884C\u8D85\u7B97 GLM-4-Flash",
    baseUrl: "https://llmapi.paratera.com/v1",
    defaultModel: "GLM-4-Flash",
    envKey: "PARATERA_KEY",
    free: true
  },
  openrouter: {
    name: "OpenRouter \u514D\u8D39\u6A21\u578B",
    baseUrl: "https://openrouter.ai/api/v1",
    defaultModel: "qwen/qwen3-next-80b-a3b-instruct:free",
    envKey: "OPENROUTER_KEY",
    free: true,
    extraHeaders: {
      "HTTP-Referer": "https://www.teachany.cn",
      "X-Title": "TeachAny-PBL"
    }
  }
};
var CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, X-Backend",
  "Access-Control-Max-Age": "86400"
};
function json(data, status = 200, extra = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json", ...CORS, ...extra }
  });
}
__name(json, "json");
__name2(json, "json");
async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}
__name(onRequestOptions, "onRequestOptions");
__name2(onRequestOptions, "onRequestOptions");
async function onRequestPost(context) {
  const { request, env } = context;
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: "Invalid JSON body" }, 400);
  }
  const backendHint = request.headers.get("X-Backend") || "paratera";
  const backend = BACKENDS[backendHint] || BACKENDS.paratera;
  const apiKey = env[backend.envKey];
  if (!apiKey) {
    return json({ error: `Backend "${backendHint}" not configured` }, 503);
  }
  const model = body.model || backend.defaultModel;
  const forwardBody = { ...body, model };
  const headers = {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${apiKey}`,
    ...backend.extraHeaders || {}
  };
  const endpoint = `${backend.baseUrl}/chat/completions`;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 6e4);
  try {
    const resp = await fetch(endpoint, {
      method: "POST",
      headers,
      body: JSON.stringify(forwardBody),
      signal: controller.signal
    });
    const data = await resp.text();
    if (!resp.ok) {
      console.error(`[LLM Proxy] ${backend.name} ${resp.status}: ${data.slice(0, 300)}`);
      return new Response(data, { status: resp.status, headers: { "Content-Type": "application/json", ...CORS } });
    }
    return new Response(data, {
      status: 200,
      headers: { "Content-Type": "application/json", ...CORS, "X-Backend": backendHint, "X-Model": model }
    });
  } catch (err) {
    if (err.name === "AbortError") {
      return json({ error: `Backend "${backendHint}" timed out (25s)` }, 504);
    }
    return json({ error: err.message }, 502);
  } finally {
    clearTimeout(timeout);
  }
}
__name(onRequestPost, "onRequestPost");
__name2(onRequestPost, "onRequestPost");
async function onRequestGet(context) {
  const models = Object.entries(BACKENDS).map(([id, b]) => ({
    id,
    name: b.name,
    model: b.defaultModel,
    free: b.free
  }));
  return json({ data: models });
}
__name(onRequestGet, "onRequestGet");
__name2(onRequestGet, "onRequestGet");
var CORS2 = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, X-TeachAny-Client",
  "Access-Control-Max-Age": "86400"
};
var AGNES_MODEL = "agnes-image-2.1-flash";
var AGNES_API_URL = "https://apihub.agnes-ai.com/v1/images/generations";
var ALLOWED_SIZES = /* @__PURE__ */ new Set(["512x512", "768x768", "1024x1024", "1024x768", "1280x768", "768x1280"]);
var NO_TEXT_SUFFIX = "\n\nSTRICT: NO TEXT, NO LETTERS, NO NUMBERS, NO WATERMARK, no Chinese characters. Educational illustration only.";
function jsonResponse(data, status = 200, extra = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...CORS2, ...extra }
  });
}
__name(jsonResponse, "jsonResponse");
__name2(jsonResponse, "jsonResponse");
function getDb(env) {
  return env.TEACHANY_DB || env.DB || null;
}
__name(getDb, "getDb");
__name2(getDb, "getDb");
function getPerCourseLimit(env) {
  const n = parseInt(String(env.IMAGE_GEN_PER_COURSE_LIMIT || "3"), 10);
  return Number.isFinite(n) && n > 0 ? Math.min(n, 10) : 3;
}
__name(getPerCourseLimit, "getPerCourseLimit");
__name2(getPerCourseLimit, "getPerCourseLimit");
function getIpRpmLimit(env) {
  const n = parseInt(String(env.IMAGE_GEN_IP_RPM || "10"), 10);
  return Number.isFinite(n) && n > 0 ? Math.min(n, 60) : 10;
}
__name(getIpRpmLimit, "getIpRpmLimit");
__name2(getIpRpmLimit, "getIpRpmLimit");
function normalizeCourseId(raw) {
  const id = String(raw || "").trim().toLowerCase();
  if (!/^[a-z0-9][a-z0-9_-]{2,79}$/.test(id)) return null;
  if (id.startsWith("_") && id !== "_preflight_probe") return null;
  return id;
}
__name(normalizeCourseId, "normalizeCourseId");
__name2(normalizeCourseId, "normalizeCourseId");
async function sha256Hex(text) {
  const data = new TextEncoder().encode(String(text || ""));
  const digest = await crypto.subtle.digest("SHA-256", data);
  return Array.from(new Uint8Array(digest)).map((b) => b.toString(16).padStart(2, "0")).join("");
}
__name(sha256Hex, "sha256Hex");
__name2(sha256Hex, "sha256Hex");
async function hashIp(ip) {
  if (!ip || !crypto?.subtle) return "";
  return (await sha256Hex(ip)).slice(0, 24);
}
__name(hashIp, "hashIp");
__name2(hashIp, "hashIp");
function buildCoursewarePrompt(prompt) {
  const base = String(prompt || "").trim();
  if (!base) return "";
  const max = 1800;
  const clipped = base.length > max ? base.slice(0, max) + "\u2026" : base;
  if (/NO TEXT|no text|无文字|禁止文字/i.test(clipped)) return clipped;
  return clipped + NO_TEXT_SUFFIX;
}
__name(buildCoursewarePrompt, "buildCoursewarePrompt");
__name2(buildCoursewarePrompt, "buildCoursewarePrompt");
function normalizeSize(size) {
  const s = String(size || "1280x768").trim().toLowerCase();
  return ALLOWED_SIZES.has(s) ? s : "1280x768";
}
__name(normalizeSize, "normalizeSize");
__name2(normalizeSize, "normalizeSize");
async function getCourseQuota(db, courseId, limit) {
  const row = await db.prepare(
    "SELECT used_count FROM courseware_image_quota WHERE course_id = ?"
  ).bind(courseId).first();
  const used = Number(row?.used_count || 0);
  return { used, limit, remaining: Math.max(0, limit - used) };
}
__name(getCourseQuota, "getCourseQuota");
__name2(getCourseQuota, "getCourseQuota");
async function getIpUsageLastMinute(db, ipHash, rpmLimit) {
  if (!ipHash) return { count: 0, limit: rpmLimit, exceeded: false };
  const row = await db.prepare(`
    SELECT COUNT(*) AS cnt FROM courseware_image_gen_logs
    WHERE ip_hash = ? AND datetime(created_at) > datetime('now', '-1 minute')
  `).bind(ipHash).first();
  const count = Number(row?.cnt || 0);
  return { count, limit: rpmLimit, exceeded: count >= rpmLimit };
}
__name(getIpUsageLastMinute, "getIpUsageLastMinute");
__name2(getIpUsageLastMinute, "getIpUsageLastMinute");
async function reserveCourseImageSlot(db, courseId, limit) {
  try {
    const ins = await db.prepare(
      "INSERT INTO courseware_image_quota (course_id, used_count) VALUES (?, 1)"
    ).bind(courseId).run();
    if (ins.success) {
      return { reserved: true, used: 1, remaining: limit - 1 };
    }
  } catch (e) {
    if (!String(e?.message || e).includes("UNIQUE")) throw e;
  }
  const upd = await db.prepare(`
    UPDATE courseware_image_quota
    SET used_count = used_count + 1, updated_at = datetime('now')
    WHERE course_id = ? AND used_count < ?
  `).bind(courseId, limit).run();
  if ((upd.meta?.changes || 0) > 0) {
    const q2 = await getCourseQuota(db, courseId, limit);
    return { reserved: true, used: q2.used, remaining: q2.remaining };
  }
  const q = await getCourseQuota(db, courseId, limit);
  return { reserved: false, used: q.used, remaining: q.remaining };
}
__name(reserveCourseImageSlot, "reserveCourseImageSlot");
__name2(reserveCourseImageSlot, "reserveCourseImageSlot");
async function releaseCourseImageSlot(db, courseId) {
  await db.prepare(`
    UPDATE courseware_image_quota
    SET used_count = CASE WHEN used_count > 0 THEN used_count - 1 ELSE 0 END,
        updated_at = datetime('now')
    WHERE course_id = ?
  `).bind(courseId).run();
}
__name(releaseCourseImageSlot, "releaseCourseImageSlot");
__name2(releaseCourseImageSlot, "releaseCourseImageSlot");
async function logImageGen(db, entry) {
  await db.prepare(`
    INSERT INTO courseware_image_gen_logs (
      course_id, slot, prompt, size, remote_url, latency_ms, error, ip_hash, user_agent
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
  `).bind(
    String(entry.courseId || "").slice(0, 80),
    String(entry.slot || "").slice(0, 32),
    String(entry.prompt || "").slice(0, 2e3),
    String(entry.size || "").slice(0, 16),
    String(entry.remoteUrl || "").slice(0, 2e3),
    entry.latencyMs == null ? null : Number(entry.latencyMs),
    String(entry.error || "").slice(0, 500),
    String(entry.ipHash || "").slice(0, 24),
    String(entry.userAgent || "").slice(0, 500)
  ).run();
}
__name(logImageGen, "logImageGen");
__name2(logImageGen, "logImageGen");
async function callAgnesImage(env, prompt, size) {
  const apiKey = String(env.AGNES_API_KEY || "").trim();
  if (!apiKey) {
    const err = new Error("AGNES_API_KEY not configured on server");
    err.status = 503;
    throw err;
  }
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 12e4);
  try {
    const resp = await fetch(AGNES_API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: AGNES_MODEL,
        prompt,
        n: 1,
        size
      }),
      signal: controller.signal
    });
    const data = await resp.json().catch(() => ({}));
    if (!resp.ok) {
      const msg = data?.error?.message || data?.error || JSON.stringify(data).slice(0, 300);
      const err = new Error(`Agnes HTTP ${resp.status}: ${msg}`);
      err.status = resp.status === 429 ? 429 : 502;
      throw err;
    }
    const url = data?.data?.[0]?.url;
    if (!url) {
      const err = new Error("Agnes response missing image url");
      err.status = 502;
      throw err;
    }
    return { url, model: AGNES_MODEL, raw: data };
  } catch (e) {
    if (e?.name === "AbortError") {
      const err = new Error("Agnes image generation timeout (120s)");
      err.status = 504;
      throw err;
    }
    throw e;
  } finally {
    clearTimeout(timeout);
  }
}
__name(callAgnesImage, "callAgnesImage");
__name2(callAgnesImage, "callAgnesImage");
async function onRequestOptions2() {
  return new Response(null, { status: 204, headers: CORS2 });
}
__name(onRequestOptions2, "onRequestOptions2");
__name2(onRequestOptions2, "onRequestOptions");
async function onRequestPost2(context) {
  const { request, env } = context;
  const db = getDb(env);
  if (!db) {
    return jsonResponse({
      ok: false,
      error: "D1_NOT_CONFIGURED",
      message: "\u8BFE\u4EF6\u751F\u56FE\u9700\u8981\u7ED1\u5B9A TEACHANY_DB\uFF0C\u5E76\u6267\u884C migrations/0004_courseware_image_gen.sql"
    }, 503);
  }
  let body;
  try {
    body = await request.json();
  } catch {
    return jsonResponse({ ok: false, error: "INVALID_JSON" }, 400);
  }
  const courseId = normalizeCourseId(body.course_id || body.courseId);
  if (!courseId) {
    return jsonResponse({
      ok: false,
      error: "INVALID_COURSE_ID",
      message: "course_id \u987B\u4E3A 3\u201380 \u4F4D\u5C0F\u5199\u5B57\u6BCD\u6570\u5B57\u4E0E\u8FDE\u5B57\u7B26\uFF08\u5982 math-linear-function\uFF09"
    }, 400);
  }
  const prompt = buildCoursewarePrompt(body.prompt);
  if (!prompt || prompt.length < 8) {
    return jsonResponse({
      ok: false,
      error: "INVALID_PROMPT",
      message: "prompt \u8FC7\u77ED\uFF0C\u8BF7\u63CF\u8FF0\u63D2\u56FE\u573A\u666F\uFF08\u5750\u6807\u7CFB\u3001\u5B9E\u9A8C\u88C5\u7F6E\u3001\u5386\u53F2\u573A\u666F\u7B49\uFF09"
    }, 400);
  }
  const size = normalizeSize(body.size);
  const slot = String(body.slot || "").trim().slice(0, 32);
  const perCourseLimit = getPerCourseLimit(env);
  const ipRpmLimit = getIpRpmLimit(env);
  const ip = request.headers.get("CF-Connecting-IP") || "";
  const ipHash = await hashIp(ip);
  const userAgent = String(request.headers.get("User-Agent") || "").slice(0, 500);
  const ipUsage = await getIpUsageLastMinute(db, ipHash, ipRpmLimit);
  if (ipUsage.exceeded) {
    return jsonResponse({
      ok: false,
      error: "RATE_LIMIT",
      message: `\u8BF7\u6C42\u8FC7\u4E8E\u9891\u7E41\uFF0C\u8BF7 ${60} \u79D2\u540E\u518D\u8BD5\uFF08\u6BCF IP \u6BCF\u5206\u949F\u6700\u591A ${ipRpmLimit} \u6B21\uFF09`,
      ip_rpm: ipUsage
    }, 429);
  }
  const reservation = await reserveCourseImageSlot(db, courseId, perCourseLimit);
  if (!reservation.reserved) {
    return jsonResponse({
      ok: false,
      error: "COURSE_QUOTA_EXCEEDED",
      message: `\u8BFE\u4EF6 ${courseId} \u5DF2\u7528\u5B8C\u751F\u56FE\u989D\u5EA6\uFF08\u6BCF\u8BFE\u4EF6\u6700\u591A ${perCourseLimit} \u5F20\uFF09`,
      course_id: courseId,
      used: reservation.used,
      remaining: 0,
      limit: perCourseLimit
    }, 429);
  }
  const t0 = Date.now();
  try {
    const result = await callAgnesImage(env, prompt, size);
    const latencyMs = Date.now() - t0;
    await logImageGen(db, {
      courseId,
      slot,
      prompt,
      size,
      remoteUrl: result.url,
      latencyMs,
      ipHash,
      userAgent
    });
    return jsonResponse({
      ok: true,
      url: result.url,
      course_id: courseId,
      slot: slot || null,
      used: reservation.used,
      remaining: reservation.remaining,
      limit: perCourseLimit,
      model: AGNES_MODEL,
      latency_ms: latencyMs,
      note: "\u8BF7\u5C3D\u5FEB\u4E0B\u8F7D url \u5230\u8BFE\u4EF6 assets/\uFF1B\u94FE\u63A5\u4E3A Agnes \u4E34\u65F6\u5730\u5740"
    });
  } catch (e) {
    const latencyMs = Date.now() - t0;
    await releaseCourseImageSlot(db, courseId);
    await logImageGen(db, {
      courseId,
      slot,
      prompt,
      size,
      latencyMs,
      error: e?.message || String(e),
      ipHash,
      userAgent
    });
    const status = e?.status && Number.isFinite(e.status) ? e.status : 502;
    return jsonResponse({
      ok: false,
      error: "GENERATION_FAILED",
      message: e?.message || "\u751F\u56FE\u5931\u8D25",
      course_id: courseId,
      latency_ms: latencyMs
    }, status);
  }
}
__name(onRequestPost2, "onRequestPost2");
__name2(onRequestPost2, "onRequestPost");
async function onRequestOptions3() {
  return new Response(null, { status: 204, headers: CORS2 });
}
__name(onRequestOptions3, "onRequestOptions3");
__name2(onRequestOptions3, "onRequestOptions");
async function onRequestGet2(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const rawCourseId = url.searchParams.get("course_id") || url.searchParams.get("courseId") || "";
  const perCourseLimit = getPerCourseLimit(env);
  const ipRpmLimit = getIpRpmLimit(env);
  const agnesConfigured = Boolean(String(env.AGNES_API_KEY || "").trim());
  const db = getDb(env);
  if (!rawCourseId) {
    return jsonResponse({
      ok: true,
      service: "teachany-image-agnes",
      model: AGNES_MODEL,
      per_course_limit: perCourseLimit,
      ip_rpm_limit: ipRpmLimit,
      agnes_configured: agnesConfigured,
      d1_configured: Boolean(db),
      endpoint: "/api/images/agnes",
      usage: "POST { course_id, prompt, size?, slot? } \u2014 \u65E0\u9700\u7528\u6237 API Key"
    });
  }
  if (!db) {
    return jsonResponse({
      ok: false,
      error: "D1_NOT_CONFIGURED",
      message: "\u914D\u989D\u67E5\u8BE2\u9700\u8981 TEACHANY_DB",
      agnes_configured: agnesConfigured
    }, 503);
  }
  const courseId = normalizeCourseId(rawCourseId);
  if (!courseId) {
    return jsonResponse({
      ok: false,
      error: "INVALID_COURSE_ID",
      message: "course_id \u683C\u5F0F\u65E0\u6548"
    }, 400);
  }
  const quota = await getCourseQuota(db, courseId, perCourseLimit);
  return jsonResponse({
    ok: true,
    course_id: courseId,
    used: quota.used,
    remaining: quota.remaining,
    limit: quota.limit,
    model: AGNES_MODEL
  });
}
__name(onRequestGet2, "onRequestGet2");
__name2(onRequestGet2, "onRequestGet");
var BACKENDS2 = {
  siliconflow: {
    name: "\u7845\u57FA\u6D41\u52A8 DeepSeek-V4-Flash",
    baseUrl: "https://api.siliconflow.cn/v1",
    defaultModel: "deepseek-ai/DeepSeek-V4-Flash",
    envKey: "SILICONFLOW_KEY",
    extraHeaders: {}
  },
  paratera: {
    name: "\u5E76\u884C\u8D85\u7B97 GLM-4-Flash",
    baseUrl: "https://llmapi.paratera.com/v1",
    defaultModel: "GLM-4-Flash",
    envKey: "PARATERA_KEY",
    extraHeaders: {}
  },
  openrouter: {
    name: "OpenRouter Qwen3 Next 80B",
    baseUrl: "https://openrouter.ai/api/v1",
    defaultModel: "qwen/qwen3-next-80b-a3b-instruct",
    envKey: "OPENROUTER_KEY",
    extraHeaders: {
      "HTTP-Referer": "https://www.teachany.cn",
      "X-Title": "TeachAny-PBL"
    }
  }
};
function inferBackendIdForModel(model) {
  const m = String(model || "").trim();
  if (!m) return "openrouter";
  if (!m.includes("/")) return "paratera";
  if (/^(qwen|deepseek|google|anthropic|openai|meta-llama|z-ai|tencent|moonshotai|mistralai)\//i.test(m)) {
    return "openrouter";
  }
  if (/^(deepseek-ai|Qwen|THUDM|zai-org|baidu|Pro\/)/i.test(m)) {
    return "siliconflow";
  }
  return "openrouter";
}
__name(inferBackendIdForModel, "inferBackendIdForModel");
__name2(inferBackendIdForModel, "inferBackendIdForModel");
var PBL_PRIMARY_MODEL = "qwen/qwen3-next-80b-a3b-instruct";
var PBL_MODEL_CHAIN = [
  { backendId: "openrouter", model: PBL_PRIMARY_MODEL },
  { backendId: "siliconflow", model: "deepseek-ai/DeepSeek-V4-Flash" },
  { backendId: "paratera", model: "GLM-4-Flash" }
];
var PBL_MATCH_MODEL_CHAIN = [
  { backendId: "openrouter", model: PBL_PRIMARY_MODEL },
  { backendId: "siliconflow", model: "deepseek-ai/DeepSeek-V4-Flash" },
  { backendId: "paratera", model: "GLM-4-Flash" }
];
var PBL_STRONG_STAGES = /* @__PURE__ */ new Set([
  "decompose",
  "match",
  "propose-curriculum",
  "validate-match",
  "verify-relevance",
  "review-curriculum",
  "review-decompose",
  "refine"
]);
function resolvePBLModelChain(env = {}) {
  const override = String(env.PBL_MODEL_OVERRIDE || "").trim();
  if (override) {
    return [{ backendId: inferBackendIdForModel(override), model: override }];
  }
  return PBL_MODEL_CHAIN;
}
__name(resolvePBLModelChain, "resolvePBLModelChain");
__name2(resolvePBLModelChain, "resolvePBLModelChain");
function resolvePBLStageModelChain(env = {}, stage = "") {
  if (!PBL_STRONG_STAGES.has(stage)) return resolvePBLModelChain(env);
  const matchOverride = String(env.PBL_MATCH_MODEL || env.PBL_MODEL_OVERRIDE || "").trim();
  if (matchOverride) {
    return [{ backendId: inferBackendIdForModel(matchOverride), model: matchOverride }];
  }
  return PBL_MATCH_MODEL_CHAIN;
}
__name(resolvePBLStageModelChain, "resolvePBLStageModelChain");
__name2(resolvePBLStageModelChain, "resolvePBLStageModelChain");
var PROVIDER_BACKEND = {
  siliconflow: "siliconflow",
  paratera: "paratera",
  openrouter: "openrouter"
};
function buildUserModelChain(env, userModel, providerId = "") {
  const m = String(userModel || "").trim();
  const pid = String(providerId || "").trim();
  if (!m && !pid) return resolvePBLModelChain(env);
  const forcedBackend = PROVIDER_BACKEND[pid];
  const model = m || BACKENDS2[forcedBackend]?.defaultModel || "";
  if (!model) return resolvePBLModelChain(env);
  const backendId = forcedBackend || inferBackendIdForModel(model);
  const chain = [{ backendId, model }];
  for (const item of resolvePBLModelChain(env)) {
    if (item.model !== model) chain.push(item);
  }
  return chain;
}
__name(buildUserModelChain, "buildUserModelChain");
__name2(buildUserModelChain, "buildUserModelChain");
var CORS3 = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Backend",
  "Access-Control-Max-Age": "86400"
};
function jsonResponse2(data, status = 200, extra = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json", ...CORS3, ...extra }
  });
}
__name(jsonResponse2, "jsonResponse2");
__name2(jsonResponse2, "jsonResponse");
function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}
__name(sleep, "sleep");
__name2(sleep, "sleep");
async function callSingleModel(env, backendId, model, messages, opts) {
  const backend = BACKENDS2[backendId];
  if (!backend) throw new Error(`Unknown backend: ${backendId}`);
  const apiKey = env[backend.envKey];
  if (!apiKey) {
    const err = new Error(`Backend "${backendId}" not configured`);
    err.status = 503;
    throw err;
  }
  const baseUrl = backend.baseUrl.replace(/\/$/, "");
  const endpoint = /\/chat\/completions/.test(baseUrl) ? baseUrl : `${baseUrl}/chat/completions`;
  const body = {
    model,
    messages,
    stream: false,
    temperature: opts.temperature ?? 0.2,
    max_tokens: opts.maxTokens ?? 4500
  };
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), opts.timeoutMs ?? 55e3);
  try {
    const resp = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
        ...backend.extraHeaders || {}
      },
      body: JSON.stringify(body),
      signal: controller.signal
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
    const content = message.content || message.reasoning || message.reasoning_content || "";
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
__name(callSingleModel, "callSingleModel");
__name2(callSingleModel, "callSingleModel");
async function callBackendLLM(env, messages, opts = {}) {
  const chain = opts.modelChain || resolvePBLModelChain(env);
  let lastError;
  for (let i = 0; i < chain.length; i++) {
    const { backendId, model } = chain[i];
    try {
      const content = await callSingleModel(env, backendId, model, messages, opts);
      return { content, model, backendId };
    } catch (e) {
      lastError = e;
      const retryable = e.status === 402 || e.status === 401 || e.status === 429 || e.status === 503 || e.status === 502 || e.name === "AbortError";
      if (retryable && i < chain.length - 1) {
        await sleep(Math.min(4e3 + i * 2e3, 12e3));
        continue;
      }
      if (!retryable) throw e;
    }
  }
  throw lastError || new Error("LLM failed");
}
__name(callBackendLLM, "callBackendLLM");
__name2(callBackendLLM, "callBackendLLM");
function assertToken(request, env) {
  const expected = String(env.PBL_LOG_TOKEN || "").trim();
  if (!expected) return true;
  const url = new URL(request.url);
  return String(url.searchParams.get("token") || request.headers.get("X-PBL-Log-Token") || "").trim() === expected;
}
__name(assertToken, "assertToken");
__name2(assertToken, "assertToken");
async function onRequestOptions4() {
  return new Response(null, { status: 204, headers: CORS3 });
}
__name(onRequestOptions4, "onRequestOptions4");
__name2(onRequestOptions4, "onRequestOptions");
async function onRequestGet3(context) {
  const { request, env } = context;
  if (!assertToken(request, env)) {
    return jsonResponse2({ error: "Forbidden" }, 403);
  }
  const sfKey = env.SILICONFLOW_KEY;
  const orKey = env.OPENROUTER_KEY;
  if (!sfKey && !orKey) {
    return jsonResponse2({ error: "SILICONFLOW_KEY / OPENROUTER_KEY not configured" }, 503);
  }
  const result = {
    ok: false,
    pbl_primary: { provider: "openrouter", model: "qwen/qwen3-next-80b-a3b-instruct" },
    siliconflow: null,
    openrouter: null
  };
  if (sfKey) {
    const sfResp = await fetch("https://api.siliconflow.cn/v1/user/info", {
      headers: { Authorization: `Bearer ${sfKey}` }
    });
    const sf = await sfResp.json().catch(() => ({}));
    const data = sf?.data || sf || {};
    result.siliconflow = {
      status: sfResp.status,
      balance_cny: data.balance ?? data.totalBalance ?? null,
      charge_balance_cny: data.chargeBalance ?? null,
      raw: data
    };
    if (sfResp.ok) result.ok = true;
  }
  if (orKey) {
    const headers = { Authorization: `Bearer ${orKey}` };
    const [keyResp, creditsResp] = await Promise.all([
      fetch("https://openrouter.ai/api/v1/key", { headers }),
      fetch("https://openrouter.ai/api/v1/credits", { headers })
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
      balance_usd: c.total_credits != null && c.total_usage != null ? Number((c.total_credits - c.total_usage).toFixed(4)) : null
    };
  }
  return jsonResponse2(result);
}
__name(onRequestGet3, "onRequestGet3");
__name2(onRequestGet3, "onRequestGet");
var BLOOM_LEVELS = {
  remember: 1,
  understand: 2,
  apply: 3,
  analyze: 4,
  evaluate: 5,
  create: 6
};
var BLOOM_VERB_PATTERNS = [
  { level: "remember", re: /列举|识别|记忆|背诵|默写|说出|写出.*名称|认读|记住/ },
  { level: "understand", re: /理解|解释|说明|描述|举例|概括|归纳|翻译|复述|阐述/ },
  { level: "apply", re: /应用|运用|计算|测量|配制|绘制|操作|实施|完成|制作|搭建|安装|调试|录入|统计|求解|列式/ },
  { level: "analyze", re: /分析|比较|对比|区分|分解|推断|探究|讨论|归因|解读|拆读/ },
  { level: "evaluate", re: /评价|评判|论证|判断|选择.*方案|评估|鉴别|审阅|答辩|反思.*优劣/ },
  { level: "create", re: /设计|创造|发明|创作|构建|开发|策划|编写.*程序|搭建.*系统|原创|编导/ }
];
function inferBloomFromBlueprint(blueprint) {
  const steps = [];
  const scheme = (blueprint?.schemes || []).find((s) => s.id === blueprint?.recommendedSchemeId) || (blueprint?.schemes || [])[0];
  (scheme?.phases || []).forEach((p) => {
    (p.steps || []).forEach((s) => steps.push(String(s)));
  });
  if (!steps.length && blueprint?.deliverable) {
    steps.push(String(blueprint.deliverable));
  }
  let maxLevel = 3;
  const evidence = [];
  const actionVerbs = /* @__PURE__ */ new Set();
  steps.forEach((step) => {
    BLOOM_VERB_PATTERNS.forEach(({ level, re }) => {
      const m = step.match(re);
      if (m) {
        const lv = BLOOM_LEVELS[level];
        if (lv > maxLevel) maxLevel = lv;
        if (evidence.length < 6) evidence.push(step.slice(0, 60));
        m.forEach((v) => actionVerbs.add(v));
      }
    });
  });
  const ceilingLabel = Object.entries(BLOOM_LEVELS).find(([, v]) => v === maxLevel)?.[0] || "apply";
  return {
    ceiling: maxLevel,
    ceilingLabel,
    evidence: evidence.slice(0, 4),
    actionVerbs: [...actionVerbs].slice(0, 8)
  };
}
__name(inferBloomFromBlueprint, "inferBloomFromBlueprint");
__name2(inferBloomFromBlueprint, "inferBloomFromBlueprint");
function bloomCeilingLabel(ceiling) {
  const map = { 1: "\u8BB0\u5FC6", 2: "\u7406\u89E3", 3: "\u5E94\u7528", 4: "\u5206\u6790", 5: "\u8BC4\u4EF7", 6: "\u521B\u9020" };
  return map[ceiling] || "\u5E94\u7528";
}
__name(bloomCeilingLabel, "bloomCeilingLabel");
__name2(bloomCeilingLabel, "bloomCeilingLabel");
function formatBloomHintForMatch(bloomProfile) {
  if (!bloomProfile?.ceiling) return "";
  const label = bloomCeilingLabel(bloomProfile.ceiling);
  const ev = (bloomProfile.evidence || []).map((s) => `\u300C${s}\u300D`).join("\u3001");
  return `
\u3010Bloom \u8BA4\u77E5\u5C42\u7EA7\u7EA6\u675F\u3011
- \u4ECE\u84DD\u56FE\u4EFB\u52A1\u63A8\u65AD\uFF0C\u672C\u9879\u76EE\u8BA4\u77E5\u4E0A\u9650\u7EA6\u4E3A\u300C${label}\u300D\uFF08level ${bloomProfile.ceiling}\uFF09
- \u4F9D\u636E\uFF1A${ev || "\u84DD\u56FE\u9636\u6BB5\u4EFB\u52A1\u52A8\u8BCD"}
- **\u7981\u6B62** matched \u9700\u8981\u300C\u8BC4\u4EF7/\u521B\u9020\u300D\u624D\u80FD\u5B8C\u6210\u7684\u8282\u70B9\uFF0C\u9664\u975E\u84DD\u56FE\u660E\u786E\u51FA\u73B0\u8BBE\u8BA1/\u8BC4\u4EF7/\u521B\u9020\u7C7B\u52A8\u8BCD
- \u4F18\u5148\u9009\u62E9\u300C\u5E94\u7528/\u5206\u6790\u300D\u7EA7\u522B\u7684\u5DE5\u5177\u6027\u8BFE\u6807\u8282\u70B9`;
}
__name(formatBloomHintForMatch, "formatBloomHintForMatch");
__name2(formatBloomHintForMatch, "formatBloomHintForMatch");
function formatBloomHintForFilter(bloomProfile) {
  if (!bloomProfile?.ceiling) return "";
  return `
\u3010Bloom \u9884\u5206\u6790\uFF08\u4F9B\u4F60\u786E\u8BA4\uFF09\u3011
- \u89C4\u5219\u63A8\u65AD\u8BA4\u77E5\u4E0A\u9650\uFF1A${bloomCeilingLabel(bloomProfile.ceiling)}\uFF08${bloomProfile.ceiling}\uFF09
- \u8BF7\u5728 JSON \u4E2D\u8FD4\u56DE bloomCeiling\uFF081-6 \u6574\u6570\uFF09\u3001bloomEvidence\uFF082-4 \u6761\uFF09\u3001actionVerbs\uFF08\u52A8\u8BCD\u5217\u8868\uFF09`;
}
__name(formatBloomHintForFilter, "formatBloomHintForFilter");
__name2(formatBloomHintForFilter, "formatBloomHintForFilter");
var archetypes_default = {
  version: "1.0",
  archetypes: [
    {
      id: "autonomous-vehicle",
      label: "\u81EA\u52A8\u9A7E\u9A76/\u5FAA\u8FF9\u5C0F\u8F66",
      projectType: "engineering",
      matchPatterns: ["\u81EA\u52A8\u9A7E\u9A76", "\u667A\u80FD\u8F66", "\u5FAA\u8FF9\u8F66", "\u5FAA\u8FF9\u5C0F\u8F66", "\u65E0\u4EBA\u8F66", "\u5C0F\u8F66\u5236\u4F5C", "\u5236\u4F5C.*\u5C0F\u8F66", "\u7269\u6D41\u673A\u5668\u4EBA", "\u5DE1\u7EBF\u8F66", "\u907F\u969C\u8F66", "\u673A\u5668\u4EBA.*\u8F66"],
      gradeBand: [7, 12],
      primarySystem: "cn",
      extensionSystems: ["ap"],
      subjects: ["physics", "info-tech", "math", "science", "engineering", "computer-science"],
      minMatched: 6,
      maxMatched: 14,
      minGrade: 6,
      banNamePatterns: [
        "\u98DE\u884C\u63A7\u5236",
        "\u822A\u7A7A",
        "\u822A\u5929",
        "\u65E0\u4EBA\u673A",
        "\u98DE\u63A7",
        "\u5F39\u9053",
        "\u706B\u7BAD",
        "\u5BFC\u5F39",
        "\u4F4E\u7A7A",
        "\u7A7A\u57DF",
        "\u6297\u751F\u7D20",
        "\u8010\u836F",
        "\u7EC6\u80DE",
        "\u5206\u88C2",
        "\u514D\u75AB",
        "\u75C5\u6BD2",
        "\u7EC6\u83CC",
        "DNA",
        "\u57FA\u56E0",
        "\u5149\u5408",
        "\u6B63\u5219\u8868\u8FBE\u5F0F",
        "\u4E0A\u4E0B\u6587\u65E0\u5173",
        "\u5F62\u5F0F\u8BED\u8A00",
        "\u7F16\u8BD1\u539F\u7406",
        "\u671D\u82B1\u5915\u62FE",
        "\u8BD7\u8BCD",
        "\u6587\u8A00",
        "100\u4EE5\u5185",
        "20\u4EE5\u5185",
        "\u8BA4\u8BC6\u56FE\u5F62",
        "\u6709\u673A\u5408\u6210",
        "\u7535\u89E3\u6C60",
        "\u539F\u7535\u6C60"
      ],
      preferNamePatterns: [
        "\u5FAA\u8FF9",
        "\u5DE1\u7EBF",
        "\u4F20\u611F",
        "\u7535\u673A",
        "\u7535\u8DEF",
        "\u63A7\u5236",
        "PID",
        "\u6469\u64E6",
        "\u53D7\u529B",
        "\u8FD0\u52A8",
        "\u81EA\u52A8\u9A7E\u9A76",
        "\u5C0F\u8F66",
        "\u673A\u5668\u4EBA",
        "\u8C03\u8BD5",
        "\u7EA2\u5916",
        "\u8D85\u58F0",
        "\u907F\u969C",
        "\u7A0B\u5E8F",
        "\u7B97\u6CD5"
      ],
      modules: [
        { id: "mechanics", label: "\u7ED3\u6784\u4E0E\u8FD0\u52A8", hints: ["\u7ED3\u6784", "\u6469\u64E6", "\u53D7\u529B", "\u8F6E", "\u7535\u673A", "\u4F20\u52A8", "\u8FD0\u52A8", "\u5E73\u8861"], subjects: ["physics", "science"], topK: 2 },
        { id: "circuit", label: "\u7535\u8DEF\u9A71\u52A8", hints: ["\u7535\u8DEF", "\u7535\u6D41", "\u7535\u538B", "\u7535\u673A", "\u9A71\u52A8", "\u4E32\u8054", "\u5E76\u8054"], subjects: ["physics", "info-tech"], topK: 2 },
        { id: "sense", label: "\u4F20\u611F\u611F\u77E5", hints: ["\u4F20\u611F", "\u7EA2\u5916", "\u8D85\u58F0", "\u5FAA\u8FF9", "\u5DE1\u7EBF", "\u8DDD\u79BB", "\u68C0\u6D4B", "\u4FE1\u53F7"], subjects: ["physics", "info-tech", "engineering"], topK: 2 },
        { id: "control", label: "\u63A7\u5236\u7B97\u6CD5", hints: ["\u63A7\u5236", "\u53CD\u9988", "PID", "\u7F16\u7A0B", "\u7B97\u6CD5", "\u907F\u969C", "\u51B3\u7B56", "\u903B\u8F91"], subjects: ["info-tech", "math", "engineering"], topK: 2 },
        { id: "test", label: "\u8C03\u8BD5\u6D4B\u8BD5", hints: ["\u6D4B\u8BD5", "\u8C03\u8BD5", "\u8BEF\u5DEE", "\u6570\u636E", "\u8BB0\u5F55", "\u5B9E\u9A8C"], subjects: ["math", "science"], topK: 2 }
      ]
    },
    {
      id: "water-rocket",
      label: "\u6C34\u706B\u7BAD/\u6A21\u578B\u706B\u7BAD\u5DE5\u7A0B",
      projectType: "engineering",
      matchPatterns: ["\u6C34\u706B\u7BAD", "\u6A21\u578B\u706B\u7BAD", "\u706B\u7BAD\u8BBE\u8BA1", "\u706B\u7BAD\u5236\u4F5C", "\u706B\u7BAD\u53D1\u5C04", "\u8BBE\u8BA1.*\u706B\u7BAD", "\u5236\u4F5C.*\u706B\u7BAD"],
      gradeBand: [7, 12],
      primarySystem: "cn",
      extensionSystems: ["ap"],
      subjects: ["physics", "chemistry", "math", "info-tech"],
      minMatched: 6,
      maxMatched: 12,
      minGrade: 7,
      banNamePatterns: [
        "100\u4EE5\u5185",
        "20\u4EE5\u5185",
        "\u8BA4\u8BC6\u56FE\u5F62",
        "\u4EBA\u7269\u63CF\u5199",
        "\u8BD7\u8BCD",
        "\u6587\u8A00",
        "\u6709\u673A\u5408\u6210",
        "\u5B98\u80FD\u56E2",
        "\u7535\u89E3\u6C60",
        "\u539F\u7535\u6C60",
        "\u4EBA\u4F53\u5668\u5B98",
        "\u7EC6\u80DE\u7ED3\u6784",
        "\u7535\u6D41\u7684\u6D4B\u91CF",
        "\u7535\u5B66\u5B9E\u9A8C",
        "\u4E32\u8054\u7535\u8DEF",
        "\u5E76\u8054\u7535\u8DEF",
        "\u7A0B\u5E8F\u8BBE\u8BA1",
        "\u53D8\u91CF/\u6570\u636E\u7C7B\u578B",
        "\u7B97\u6CD5",
        "\u7269\u8054\u7F51"
      ],
      chineseBanPatterns: [],
      modules: [
        { id: "propulsion", label: "\u63A8\u8FDB\u4E0E\u53CD\u51B2", hints: ["\u53CD\u51B2", "\u52A8\u91CF", "\u725B\u987F", "\u63A8\u529B", "\u55B7\u5C04", "\u538B\u5F3A"], subjects: ["physics"], topK: 2 },
        { id: "ballistics", label: "\u5F39\u9053\u4E0E\u8FD0\u52A8", hints: ["\u629B\u4F53", "\u8FD0\u52A8", "\u8F68\u8FF9", "\u91CD\u529B", "\u901F\u5EA6", "\u673A\u68B0\u80FD"], subjects: ["physics", "math"], topK: 2 },
        { id: "aerodynamics", label: "\u7ED3\u6784\u4E0E\u6C14\u52A8", hints: ["\u538B\u5F3A", "\u6D41\u4F53", "\u963B\u529B", "\u7ED3\u6784", "\u91CD\u5FC3", "\u7A33\u5B9A"], subjects: ["physics"], topK: 2 },
        { id: "test", label: "\u6D4B\u8BD5\u4E0E\u8FED\u4EE3", hints: ["\u5B9E\u9A8C", "\u6D4B\u91CF", "\u63A7\u5236\u53D8\u91CF", "\u6570\u636E", "\u8BEF\u5DEE", "\u8BB0\u5F55"], subjects: ["physics", "math"], topK: 2 }
      ]
    },
    {
      id: "mixed-solution-chemistry",
      label: "\u6DF7\u5408\u6EB6\u6DB2\u95F4\u63A5\u6D4B\u5B9A",
      projectType: "scientific-inquiry",
      matchPatterns: ["\u98DF\u5802", "\u6C64\u6C34", "\u6DF7\u5408\u6EB6\u6DB2", "\u6EF4\u5B9A", "\u785D\u9178\u94F6", "\u7535\u5BFC\u7387", "\u5364\u6C34", "\u6C64\u6C41"],
      gradeBand: [9, 12],
      primarySystem: "cn",
      extensionSystems: [],
      subjects: ["chemistry", "physics", "math"],
      minMatched: 5,
      maxMatched: 10,
      minGrade: 8,
      banNamePatterns: [
        "100\u4EE5\u5185",
        "20\u4EE5\u5185",
        "\u8BA4\u8BC6\u56FE\u5F62",
        "\u5206\u6570\u7684\u521D\u6B65",
        "\u6570\u636E\u7684\u63CF\u8FF0",
        "\u7EDF\u8BA1\u56FE\u7684\u8BA4\u8BC6",
        "\u7A0B\u5E8F\u8BBE\u8BA1",
        "\u4EBA\u4F53\u5668\u5B98",
        "\u996E\u98DF\u8425\u517B",
        "\u8D28\u91CF\u5206\u6570$",
        "^\u914D\u5236\u6EB6\u6DB2$",
        "\u7535\u89E3\u6C60",
        "\u7535\u89E3",
        "\u6C14\u4F53\u6469\u5C14\u4F53\u79EF",
        "\u539F\u7535\u6C60",
        "\u91D1\u5C5E\u8150\u8680\u4E0E\u9632\u62A4",
        "\u7535\u6D41\u4E0E\u7535\u8DEF",
        "\u7535\u8DEF\u57FA\u672C\u8FDE\u63A5",
        "\u4E32\u8054\u7535\u8DEF",
        "\u5E76\u8054\u7535\u8DEF",
        "\u5E73\u884C\u4E0E\u5782\u76F4",
        "\u76F8\u4EA4\u7EBF\u4E0E\u5E73\u884C\u7EBF",
        "\u7A7A\u95F4\u5411\u91CF",
        "\u7ACB\u4F53\u51E0\u4F55",
        "\u7EDF\u8BA1\u63A8\u65AD",
        "\u56DE\u5F52",
        "\u72EC\u7ACB\u6027\u68C0\u9A8C"
      ],
      preferNamePatterns: [
        "\u6EF4\u5B9A",
        "\u785D\u9178\u94F6",
        "\u79BB\u5B50\u53CD\u5E94",
        "\u7269\u8D28\u7684\u91CF",
        "\u6469\u5C14",
        "\u6C89\u6DC0",
        "\u6C2F\u79BB\u5B50",
        "\u7535\u5BFC",
        "\u7535\u89E3\u8D28",
        "\u7535\u79BB",
        "\u5316\u5B66\u65B9\u7A0B\u5F0F"
      ],
      modules: [
        { id: "constraint", label: "\u6D4B\u5B9A\u7EA6\u675F", hints: ["\u6DF7\u5408\u6EB6\u6DB2", "\u79BB\u5B50", "\u95F4\u63A5", "\u53D6\u6837", "\u7A00\u91CA"], subjects: ["chemistry"], topK: 2 },
        { id: "titration", label: "\u6EF4\u5B9A\u6CD5", hints: ["\u6EF4\u5B9A", "\u785D\u9178\u94F6", "\u6C89\u6DC0", "\u6807\u51C6\u6EB6\u6DB2", "\u7269\u8D28\u7684\u91CF\u6D53\u5EA6"], subjects: ["chemistry"], topK: 2 },
        { id: "conductivity", label: "\u7535\u5BFC\u7387\u6CD5", hints: ["\u7535\u5BFC", "\u7535\u89E3\u8D28", "\u7535\u79BB", "\u79BB\u5B50\u6D53\u5EA6", "\u5BFC\u7535"], subjects: ["chemistry"], topK: 2 },
        { id: "calc", label: "\u6570\u636E\u5904\u7406", hints: ["\u8BA1\u7B97", "\u8BEF\u5DEE", "\u7EDF\u8BA1", "\u6362\u7B97", "\u5E73\u884C"], subjects: ["math", "chemistry"], topK: 2 }
      ]
    },
    {
      id: "consumer-decision",
      label: "\u6D88\u8D39\u51B3\u7B56/\u65B9\u6848\u5BF9\u6BD4",
      projectType: "consumer-decision",
      matchPatterns: ["\u7814\u7A76\u8D2D\u8F66", "\u7814\u7A76.*\u8D2D\u8F66", "\u8D2D\u8F66", "\u4E70\u8F66", "\u9009\u8F66", "\u7528\u8F66\u65B9\u6848", "\u65B0\u80FD\u6E90", "\u71C3\u6CB9\u8F66", "\u6210\u672C\u6548\u76CA", "\u6210\u672C\u5BF9\u6BD4", "\u6BD4\u9009", "\u6027\u4EF7\u6BD4", "\u7528\u8F66\u6210\u672C"],
      gradeBand: [7, 12],
      primarySystem: "cn",
      extensionSystems: [],
      subjects: ["math", "physics", "chemistry", "geography", "chinese"],
      minMatched: 6,
      maxMatched: 12,
      minGrade: 7,
      banNamePatterns: [
        "\u7535\u89E3\u6C60",
        "\u539F\u7535\u6C60",
        "\u7A0B\u5E8F\u63A7\u5236",
        "\u4F20\u611F\u5668",
        "\u7535\u78C1\u611F\u5E94",
        "\u7EC6\u80DE",
        "\u5149\u5408\u4F5C\u7528",
        "\u4EBA\u7269\u63CF\u5199",
        "\u6027\u683C\u5206\u6790",
        "\u8BD7\u8BCD",
        "\u6587\u8A00",
        "\u8BB0\u53D9\u6587",
        "\u6563\u6587\u6B23\u8D4F",
        "\u540D\u8457\u5BFC\u8BFB",
        "\u8499\u53E4",
        "\u5143\u671D",
        "\u5B8B\u671D",
        "\u5B8B\u4EE3",
        "\u5510\u671D",
        "\u968B\u5510",
        "\u660E\u6E05",
        "\u897F\u6C49",
        "\u4E1D\u7EF8\u4E4B\u8DEF",
        "\u4E16\u754C\u5927\u6218",
        "\u8D44\u4EA7\u9636\u7EA7",
        "\u9769\u547D",
        "\u6539\u9769\u5F00\u653E",
        "\u5386\u53F2\u80CC\u666F",
        "\u53E4\u4EE3\u53F2",
        "\u8FD1\u4EE3\u53F2",
        "100\u4EE5\u5185",
        "20\u4EE5\u5185",
        "\u8BA4\u8BC6\u56FE\u5F62",
        "\u903B\u8F91\u7528\u8BED",
        "\u7EDF\u8BA1\u63A8\u65AD",
        "\u56DE\u5F52",
        "\u72EC\u7ACB\u6027\u68C0\u9A8C",
        "\u7EBF\u6027\u89C4\u5212",
        "\u7A7A\u95F4\u5411\u91CF",
        "\u4E09\u89D2\u6052\u7B49",
        "\u6052\u7B49\u53D8\u6362",
        "\u6392\u5217\u7EC4\u5408",
        "\u4E8C\u9879\u5F0F",
        "\u7B49\u6BD4\u6570\u5217",
        "\u7B49\u5DEE\u6570\u5217"
      ],
      chineseAllowPatterns: ["\u8BF4\u660E\u6587", "\u975E\u8FDE\u7EED", "\u8C03\u67E5\u62A5\u544A", "\u8BBA\u8BC1", "\u5B9E\u7528", "\u5E94\u7528\u6587", "\u5EFA\u8BAE\u4E66", "\u5021\u8BAE\u4E66", "\u8BF4\u660E\u6587\u9605\u8BFB"],
      chineseBanPatterns: ["\u4EBA\u7269", "\u6027\u683C", "\u8BD7\u8BCD", "\u6587\u8A00", "\u8BB0\u53D9", "\u6563\u6587", "\u5C0F\u8BF4", "\u620F\u5267", "\u6717\u8BF5", "\u540D\u8457", "\u73B0\u4EE3\u8BD7"],
      modules: [
        { id: "needs", label: "\u9700\u6C42\u8C03\u7814", hints: ["\u7EDF\u8BA1", "\u6570\u636E", "\u8C03\u67E5", "\u95EE\u5377", "\u56FE\u8868", "\u6574\u7406"], subjects: ["math", "chinese"], topK: 2 },
        { id: "cost", label: "\u6210\u672C\u6D4B\u7B97", hints: ["\u51FD\u6570", "\u8BA1\u7B97", "\u767E\u5206\u6BD4", "\u7EDF\u8BA1", "\u8D39\u7528", "\u6210\u672C"], subjects: ["math"], topK: 2 },
        { id: "energy", label: "\u52A8\u529B\u4E0E\u80FD\u8017", hints: ["\u5185\u71C3\u673A", "\u70ED\u673A", "\u6548\u7387", "\u7535\u80FD", "\u5316\u5B66\u80FD", "\u80FD\u91CF", "\u505A\u529F"], subjects: ["physics", "chemistry"], topK: 2 },
        { id: "environment", label: "\u73AF\u4FDD\u6392\u653E", hints: ["\u73AF\u5883", "\u6C61\u67D3", "\u6392\u653E", "\u78B3", "\u6C14\u5019", "\u8D44\u6E90"], subjects: ["geography", "chemistry"], topK: 2 },
        { id: "decision", label: "\u51B3\u7B56\u62A5\u544A", hints: ["\u8BF4\u660E\u6587", "\u62A5\u544A", "\u8BBA\u8BC1", "\u5199\u4F5C", "\u6BD4\u8F83", "\u5EFA\u8BAE"], subjects: ["chinese", "math"], topK: 2 }
      ]
    },
    {
      id: "social-inquiry",
      label: "\u793E\u4F1A\u8C03\u67E5",
      projectType: "social-inquiry",
      matchPatterns: ["\u95EE\u5377", "\u8BBF\u8C08", "\u793E\u4F1A\u8C03\u67E5", "\u8C03\u7814\u62A5\u544A", "\u793E\u533A", "\u6C11\u4FD7", "\u53E3\u8FF0\u53F2", "\u5783\u573E\u5206\u7C7B", "\u5783\u573E\u6CBB\u7406", "\u73AF\u4FDD", "\u5E9F\u5F03\u7269", "\u5021\u8BAE"],
      gradeBand: [1, 12],
      primarySystem: "cn",
      subjects: ["chinese", "math", "geography", "history", "science", "politics", "psychology"],
      minMatched: 5,
      maxMatched: 10,
      minGrade: 1,
      banNamePatterns: ["\u7535\u89E3\u6C60", "\u539F\u7535\u6C60", "\u725B\u987F\u5B9A\u5F8B", "\u5316\u5B66\u65B9\u7A0B\u5F0F", "\u7EC6\u80DE\u7ED3\u6784", "\u7EC6\u80DE\u5206\u88C2", "\u6297\u751F\u7D20", "100\u4EE5\u5185", "\u98DE\u884C\u63A7\u5236", "\u822A\u7A7A"],
      chineseAllowPatterns: ["\u8BF4\u660E\u6587", "\u8C03\u67E5", "\u62A5\u544A", "\u975E\u8FDE\u7EED", "\u5B9E\u7528"],
      chineseBanPatterns: ["\u4EBA\u7269\u63CF\u5199", "\u8BD7\u8BCD", "\u6587\u8A00\u6B23\u8D4F"],
      modules: [
        { id: "topic", label: "\u9009\u9898\u8BBE\u8BA1", hints: ["\u8C03\u67E5", "\u95EE\u5377", "\u8BBF\u8C08", "\u62BD\u6837", "\u9009\u9898", "\u793E\u533A"], subjects: ["chinese", "math", "politics", "psychology"], topK: 2 },
        { id: "collect", label: "\u8D44\u6599\u6536\u96C6", hints: ["\u8D44\u6599", "\u6570\u636E", "\u6536\u96C6", "\u5B9E\u5730", "\u6587\u732E", "\u5783\u573E", "\u5206\u7C7B"], subjects: ["geography", "history", "chinese", "science", "politics", "psychology"], topK: 2 },
        { id: "analyze", label: "\u7EDF\u8BA1\u5206\u6790", hints: ["\u7EDF\u8BA1", "\u56FE\u8868", "\u5E73\u5747\u6570", "\u767E\u5206\u6BD4", "\u6574\u7406", "\u73AF\u5883"], subjects: ["math", "science", "psychology"], topK: 2 },
        { id: "report", label: "\u62A5\u544A\u4E0E\u7B56\u5212", hints: ["\u62A5\u544A", "\u8BF4\u660E\u6587", "\u8BBA\u8BC1", "\u5EFA\u8BAE", "\u5199\u4F5C", "\u5BA3\u4F20", "\u5021\u8BAE", "\u7B56\u5212"], subjects: ["chinese", "politics"], topK: 2 }
      ]
    },
    {
      id: "direct-chemistry",
      label: "\u6EB6\u6DB2\u6D53\u5EA6\u76F4\u63A5\u63A2\u7A76",
      projectType: "scientific-inquiry",
      matchPatterns: ["\u98DF\u76D0\u6D53\u5EA6", "\u53A8\u623F.*\u76D0", "\u914D\u5236\u6EB6\u6DB2", "\u8D28\u91CF\u5206\u6570", "\u6EB6\u8D28.*\u6EB6\u5242"],
      gradeBand: [6, 10],
      primarySystem: "cn",
      subjects: ["chemistry", "science", "math"],
      minMatched: 4,
      maxMatched: 8,
      minGrade: 6,
      banNamePatterns: ["\u6EF4\u5B9A", "\u785D\u9178\u94F6", "\u7535\u5BFC\u7387", "\u7A0B\u5E8F\u8BBE\u8BA1", "100\u4EE5\u5185", "\u539F\u5B50\u7ED3\u6784"],
      preferNamePatterns: ["\u6EB6\u6DB2", "\u6EB6\u8D28", "\u6EB6\u5242", "\u8D28\u91CF\u5206\u6570", "\u6EB6\u89E3", "\u914D\u5236", "\u6C2F\u5316\u94A0"],
      modules: [
        { id: "concept", label: "\u6EB6\u6DB2\u6982\u5FF5", hints: ["\u6EB6\u6DB2", "\u6EB6\u8D28", "\u6EB6\u5242", "\u6EB6\u89E3", "\u6D53\u5EA6"], subjects: ["chemistry", "science"], topK: 2 },
        { id: "experiment", label: "\u5B9E\u9A8C\u6D4B\u91CF", hints: ["\u5B9E\u9A8C", "\u79F0\u91CF", "\u91CF\u53D6", "\u914D\u5236", "\u6D4B\u91CF"], subjects: ["chemistry", "science"], topK: 2 },
        { id: "calc", label: "\u8BA1\u7B97\u5206\u6790", hints: ["\u8D28\u91CF\u5206\u6570", "\u8BA1\u7B97", "\u6570\u636E", "\u7EDF\u8BA1", "\u8BEF\u5DEE"], subjects: ["math", "chemistry"], topK: 2 }
      ]
    },
    {
      id: "humanities-writing",
      label: "\u4EBA\u6587\u5199\u4F5C/\u6587\u5B66\u521B\u4F5C",
      projectType: "humanities-literary",
      matchPatterns: ["\u5199\u8BD7|\u8BD7\u6B4C|\u8BD7\u96C6|\u73B0\u4EE3\u8BD7|\u4F5C\u6587|\u5F81\u6587|\u5C0F\u8BF4|\u5267\u672C|\u6563\u6587|\u8BFB\u540E\u611F|\u4E66\u8BC4"],
      gradeBand: [6, 12],
      primarySystem: "cn",
      subjects: ["chinese", "english", "history"],
      minMatched: 4,
      maxMatched: 10,
      minGrade: 6,
      banNamePatterns: ["100\u4EE5\u5185", "\u725B\u987F", "\u5316\u5B66\u65B9\u7A0B\u5F0F", "\u7535\u89E3\u6C60", "\u51FD\u6570\u6A21\u578B", "\u7EDF\u8BA1\u63A8\u65AD"],
      modules: [
        { id: "theme", label: "\u7ACB\u610F\u9009\u6750", hints: ["\u7ACB\u610F", "\u4E3B\u9898", "\u9009\u6750", "\u6784\u601D"], subjects: ["chinese"], topK: 2 },
        { id: "read", label: "\u9605\u8BFB\u79EF\u7D2F", hints: ["\u9605\u8BFB", "\u540D\u8457", "\u7D20\u6750", "\u9274\u8D4F", "\u79EF\u7D2F"], subjects: ["chinese", "history"], topK: 2 },
        { id: "express", label: "\u7ED3\u6784\u8868\u8FBE", hints: ["\u7ED3\u6784", "\u8868\u8FBE", "\u4FEE\u8F9E", "\u8BED\u8A00", "\u5199\u4F5C"], subjects: ["chinese"], topK: 2 },
        { id: "revise", label: "\u4FEE\u6539\u5C55\u793A", hints: ["\u4FEE\u6539", "\u8BC4\u8BAE", "\u6717\u8BF5", "\u5C55\u793A", "\u6F14\u8BB2"], subjects: ["chinese"], topK: 2 }
      ]
    },
    {
      id: "application-writing",
      label: "\u5E94\u7528\u6587\u5199\u4F5C",
      projectType: "humanities-literary",
      matchPatterns: ["\u5E94\u7528\u6587|\u5021\u8BAE\u4E66|\u5EFA\u8BAE\u4E66|\u901A\u77E5|\u4E66\u4FE1|\u6F14\u8BB2\u7A3F|\u53D1\u8A00\u7A3F|\u5BA3\u4F20\u7A3F"],
      gradeBand: [6, 12],
      primarySystem: "cn",
      subjects: ["chinese"],
      minMatched: 4,
      maxMatched: 8,
      minGrade: 6,
      banNamePatterns: ["100\u4EE5\u5185", "\u8BD7\u8BCD\u6B23\u8D4F", "\u6587\u8A00\u9605\u8BFB", "\u4EBA\u7269\u63CF\u5199", "\u725B\u987F", "\u5316\u5B66\u65B9\u7A0B\u5F0F"],
      chineseAllowPatterns: ["\u5E94\u7528\u6587", "\u8BF4\u660E\u6587", "\u5B9E\u7528", "\u5021\u8BAE", "\u5EFA\u8BAE", "\u901A\u77E5", "\u6F14\u8BB2", "\u53D1\u8A00"],
      chineseBanPatterns: ["\u8BD7\u8BCD", "\u6587\u8A00", "\u5C0F\u8BF4", "\u620F\u5267", "\u4EBA\u7269\u63CF\u5199"],
      modules: [
        { id: "format", label: "\u6587\u4F53\u683C\u5F0F", hints: ["\u5E94\u7528\u6587", "\u683C\u5F0F", "\u8BF4\u660E\u6587", "\u5B9E\u7528", "\u6587\u4F53"], subjects: ["chinese"], topK: 2 },
        { id: "content", label: "\u5185\u5BB9\u4E0E\u8BBA\u8BC1", hints: ["\u8BBA\u8BC1", "\u6750\u6599", "\u89C2\u70B9", "\u7406\u7531", "\u5EFA\u8BAE"], subjects: ["chinese"], topK: 2 },
        { id: "revise", label: "\u4FEE\u6539\u5B9A\u7A3F", hints: ["\u4FEE\u6539", "\u8BED\u8A00", "\u8868\u8FBE", "\u5C55\u793A"], subjects: ["chinese"], topK: 2 }
      ]
    },
    {
      id: "study-trip",
      label: "\u7814\u5B66\u65C5\u884C/\u4EBA\u6587\u5730\u7406\u8003\u5BDF",
      projectType: "study-trip",
      matchPatterns: ["\u7814\u5B66|\u6E38\u5B66|\u7814\u5B66\u65C5\u884C|\u7814\u5B66\u8DEF\u7EBF|\u7EA2\u8272\u7814\u5B66|\u6587\u5316\u7814\u5B66|\u6587\u5316\u8003\u5BDF|\u5B9E\u5730\u8003\u5BDF|field.?trip|\u9057\u5740|\u535A\u7269\u9986|\u4EBA\u6587\u53F2\u8FF9|\u53E4\u8FF9|\u53E4\u6751|\u4E16\u754C\u9057\u4EA7"],
      gradeBand: [6, 12],
      primarySystem: "cn",
      subjects: ["chinese", "math", "geography", "history"],
      minMatched: 6,
      maxMatched: 12,
      minGrade: 6,
      banNamePatterns: ["\u7535\u89E3\u6C60", "\u725B\u987F\u5B9A\u5F8B", "\u5316\u5B66\u65B9\u7A0B\u5F0F", "\u7EC6\u80DE", "100\u4EE5\u5185", "\u8BD7\u8BCD\u6B23\u8D4F", "\u4E09\u89D2\u51FD\u6570", "\u7535\u5B66\u5B9E\u9A8C"],
      preferNamePatterns: ["\u5730\u7406", "\u5386\u53F2", "\u533A\u57DF", "\u5730\u56FE", "\u5730\u5F62", "\u6C14\u5019", "\u8D44\u6E90", "\u4EBA\u6587", "\u6587\u7269", "\u9057\u5740", "\u535A\u7269\u9986", "\u9769\u547D", "\u671D\u4EE3", "\u9057\u4EA7", "\u7EDF\u8BA1", "\u8C03\u67E5", "\u8BF4\u660E", "\u767E\u5206", "\u56FE\u8868", "\u65B9\u6848", "\u8DEF\u7EBF"],
      modules: [
        { id: "destination", label: "\u76EE\u7684\u5730\u8C03\u7814", hints: ["\u76EE\u7684\u5730", "\u8C03\u7814", "\u533A\u57DF", "\u5730\u56FE", "\u5730\u5F62", "\u6C14\u5019", "\u8D44\u6E90", "\u533A\u4F4D", "\u4EA4\u901A"], subjects: ["geography", "history"], topK: 2 },
        { id: "heritage", label: "\u4EBA\u6587\u53F2\u8FF9", hints: ["\u5386\u53F2", "\u6587\u7269", "\u9057\u5740", "\u535A\u7269\u9986", "\u9769\u547D", "\u671D\u4EE3", "\u9057\u4EA7", "\u4EBA\u6587", "\u53E4\u8FF9", "\u6587\u5316"], subjects: ["history", "chinese"], topK: 2 },
        { id: "route", label: "\u8DEF\u7EBF\u9884\u7B97", hints: ["\u8DEF\u7EBF", "\u65E5\u7A0B", "\u884C\u7A0B", "\u9884\u7B97", "\u8D39\u7528", "\u7EDF\u8BA1", "\u6210\u672C", "\u5206\u5DE5", "\u5B89\u5168"], subjects: ["math", "geography", "chinese"], topK: 2 },
        { id: "report", label: "\u7814\u5B66\u62A5\u544A", hints: ["\u62A5\u544A", "\u603B\u7ED3", "\u8BB0\u5F55", "\u8BF4\u660E", "\u5C55\u793A", "\u590D\u76D8", "\u89C2\u5BDF", "\u65E5\u8BB0"], subjects: ["chinese", "history", "geography"], topK: 2 }
      ]
    },
    {
      id: "life-planning",
      label: "\u6D3B\u52A8\u7B56\u5212/\u751F\u6D3B\u89C4\u5212",
      projectType: "life-planning",
      matchPatterns: ["\u6D3B\u52A8\u7B56\u5212|\u8054\u6B22|\u665A\u4F1A|\u51FA\u6E38|\u65C5\u884C\u8DEF\u7EBF|\u9884\u7B97|\u65E5\u7A0B"],
      gradeBand: [6, 12],
      primarySystem: "cn",
      subjects: ["chinese", "math", "geography", "politics", "psychology"],
      minMatched: 5,
      maxMatched: 10,
      minGrade: 6,
      banNamePatterns: ["\u7535\u89E3\u6C60", "\u725B\u987F\u5B9A\u5F8B", "\u5316\u5B66\u65B9\u7A0B\u5F0F", "\u7EC6\u80DE", "100\u4EE5\u5185", "\u8BD7\u8BCD\u6B23\u8D4F"],
      modules: [
        { id: "goal", label: "\u9700\u6C42\u76EE\u6807", hints: ["\u9700\u6C42", "\u76EE\u6807", "\u8C03\u67E5", "\u573A\u666F", "\u4EBA\u6570"], subjects: ["chinese", "math"], topK: 2 },
        { id: "plan", label: "\u65B9\u6848\u65E5\u7A0B", hints: ["\u65B9\u6848", "\u65E5\u7A0B", "\u8DEF\u7EBF", "\u5B89\u6392", "\u6D41\u7A0B"], subjects: ["chinese", "geography"], topK: 2 },
        { id: "budget", label: "\u9884\u7B97\u5206\u5DE5", hints: ["\u9884\u7B97", "\u6210\u672C", "\u8D39\u7528", "\u7EDF\u8BA1", "\u5206\u5DE5"], subjects: ["math"], topK: 2 },
        { id: "review", label: "\u6267\u884C\u590D\u76D8", hints: ["\u6267\u884C", "\u8BB0\u5F55", "\u590D\u76D8", "\u603B\u7ED3", "\u62A5\u544A"], subjects: ["chinese"], topK: 2 }
      ]
    },
    {
      id: "primary-shopping",
      label: "\u5C0F\u5B66\u8D2D\u7269/\u8BB0\u8D26",
      projectType: "business-economics",
      matchPatterns: ["\u5C0F\u5356\u90E8|\u8D2D\u7269\u627E\u96F6|\u8D2D\u7269\u573A\u666F|\u4EBA\u6C11\u5E01\u5B66\u5177|\u8D2D\u7269\u5C0F\u7968|\u6A21\u62DF.*\u8D2D\u7269|\u627E\u96F6|\u8BB0\u8D26\u8868|\u4E49\u5356.*\u8BB0\u8D26|\u4E49\u5356.*\u6536\u5165"],
      gradeBand: [1, 6],
      primarySystem: "cn",
      subjects: ["math", "chinese"],
      minMatched: 5,
      maxMatched: 8,
      minGrade: 1,
      banNamePatterns: ["\u78C1\u94C1", "\u63A8\u62C9", "\u52A8\u7269", "\u6865\u6881", "\u7EC6\u80DE", "\u98DF\u7269\u94FE", "\u6708\u76F8", "\u5CA9\u77F3", "\u6C49\u5B57\u7ED3\u6784", "\u4FEE\u8F9E", "\u4F53\u79EF", "\u65B9\u7A0B", "\u5206\u6570\u56DB\u5219", "\u7535\u89E3\u6C60", "\u725B\u987F"],
      preferNamePatterns: ["\u4EBA\u6C11\u5E01", "\u52A0\u51CF", "\u4E58", "\u7EDF\u8BA1", "\u8C61\u5F62", "\u6761\u5F62", "\u6298\u7EBF", "\u8BA4\u8BC6.*\u6570", "\u5E94\u7528\u6587", "\u8BF4\u660E\u6587"],
      modules: [
        { id: "money", label: "\u4EBA\u6C11\u5E01\u8BA4\u8BC6", hints: ["\u4EBA\u6C11\u5E01", "\u9762\u989D", "\u5143\u89D2\u5206", "\u8BA4\u8BC6"], subjects: ["math"], topK: 2 },
        { id: "calc", label: "\u4ED8\u6B3E\u627E\u96F6", hints: ["\u52A0\u51CF", "\u4E58", "\u8BA1\u7B97", "\u627E\u96F6", "\u4ED8\u6B3E"], subjects: ["math"], topK: 2 },
        { id: "record", label: "\u8BB0\u5F55\u5C0F\u7968", hints: ["\u8BB0\u5F55", "\u7EDF\u8BA1", "\u56FE\u8868", "\u6570\u636E", "\u5C0F\u7968"], subjects: ["math", "chinese"], topK: 2 },
        { id: "share", label: "\u5C55\u793A\u8BF4\u660E", hints: ["\u8BF4\u660E", "\u5C55\u793A", "\u62A5\u544A", "\u5E94\u7528\u6587"], subjects: ["chinese"], topK: 2 }
      ]
    },
    {
      id: "business-economics",
      label: "\u5546\u4E1A\u5B9E\u8DF5/\u4E49\u5356\u521B\u4E1A",
      projectType: "business-economics",
      matchPatterns: ["\u4E49\u5356|\u521B\u4E1A|\u5546\u4E1A\u8BA1\u5212|\u8425\u9500|\u5B9A\u4EF7|\u5E02\u573A\u8C03\u7814|\u8DF3\u86A4\u5E02\u573A|\u76C8\u5229|\u8BB0\u8D26|\u6536\u5165.*\u56FE\u8868"],
      gradeBand: [6, 12],
      primarySystem: "cn",
      subjects: ["math", "chinese", "info-tech"],
      minMatched: 5,
      maxMatched: 10,
      minGrade: 6,
      banNamePatterns: ["\u7535\u89E3\u6C60", "\u725B\u987F", "\u7EC6\u80DE", "\u8BD7\u8BCD", "100\u4EE5\u5185", "\u7EBF\u6027\u89C4\u5212"],
      chineseAllowPatterns: ["\u8BF4\u660E\u6587", "\u5E94\u7528\u6587", "\u62A5\u544A", "\u7B56\u5212"],
      modules: [
        { id: "research", label: "\u5E02\u573A\u8C03\u7814", hints: ["\u8C03\u67E5", "\u5E02\u573A", "\u9700\u6C42", "\u6570\u636E", "\u7528\u6237"], subjects: ["math", "chinese"], topK: 2 },
        { id: "plan", label: "\u65B9\u6848\u8BBE\u8BA1", hints: ["\u65B9\u6848", "\u4EA7\u54C1", "\u7B56\u5212", "\u521B\u610F"], subjects: ["chinese"], topK: 2 },
        { id: "cost", label: "\u6210\u672C\u5B9A\u4EF7", hints: ["\u6210\u672C", "\u5B9A\u4EF7", "\u5229\u6DA6", "\u9884\u7B97", "\u767E\u5206\u6BD4"], subjects: ["math"], topK: 2 },
        { id: "operate", label: "\u8FD0\u8425\u590D\u76D8", hints: ["\u8FD0\u8425", "\u63A8\u5E7F", "\u590D\u76D8", "\u62A5\u544A"], subjects: ["chinese", "math"], topK: 2 }
      ]
    },
    {
      id: "health-life",
      label: "\u5065\u5EB7\u751F\u6D3B/\u8FD1\u89C6\u9632\u63A7",
      projectType: "health-life",
      matchPatterns: ["\u8FD1\u89C6|\u62A4\u773C|\u89C6\u529B|\u8425\u517B|\u996E\u98DF|\u5065\u8EAB|\u4F5C\u606F|\u5065\u5EB7\u65B9\u6848|\u9632\u63A7"],
      gradeBand: [4, 12],
      primarySystem: "cn",
      subjects: ["biology", "science", "math", "chinese", "psychology", "politics"],
      minMatched: 4,
      maxMatched: 9,
      minGrade: 4,
      banNamePatterns: ["\u7535\u89E3\u6C60", "\u725B\u987F\u5B9A\u5F8B", "\u5316\u5B66\u65B9\u7A0B\u5F0F", "100\u4EE5\u5185", "\u8BD7\u8BCD\u6B23\u8D4F"],
      modules: [
        { id: "status", label: "\u73B0\u72B6\u8C03\u67E5", hints: ["\u8C03\u67E5", "\u7EDF\u8BA1", "\u6570\u636E", "\u8BB0\u5F55", "\u6D4B\u91CF"], subjects: ["math", "science"], topK: 2 },
        { id: "knowledge", label: "\u5065\u5EB7\u77E5\u8BC6", hints: ["\u5065\u5EB7", "\u8425\u517B", "\u4EBA\u4F53", "\u89C6\u529B", "\u8FD0\u52A8"], subjects: ["biology", "science"], topK: 2 },
        { id: "plan", label: "\u8BA1\u5212\u5236\u5B9A", hints: ["\u8BA1\u5212", "\u65B9\u6848", "\u76EE\u6807", "\u4F5C\u606F"], subjects: ["chinese"], topK: 2 },
        { id: "assess", label: "\u5B9E\u8DF5\u8BC4\u4F30", hints: ["\u8BB0\u5F55", "\u8BC4\u4F30", "\u5BF9\u6BD4", "\u62A5\u544A", "\u5021\u8BAE"], subjects: ["chinese", "math"], topK: 2 }
      ]
    },
    {
      id: "planting-cultivation",
      label: "\u79CD\u690D\u517B\u6B96/\u56ED\u827A\u683D\u57F9",
      projectType: "planting-cultivation",
      matchPatterns: ["\u79CD\u690D|\u683D\u57F9|\u6708\u5B63|\u82B1\u5349|\u73AB\u7470|\u852C\u83DC|\u79CD\u83DC|\u76C6\u683D|\u56ED\u827A|\u517B\u6B96|\u517B\u8695|\u82B1\u575B|\u7EFF\u5316|\u9633\u53F0\u79CD|\u6821\u56ED\u79CD"],
      gradeBand: [1, 9],
      primarySystem: "cn",
      subjects: ["science", "biology", "chinese", "math"],
      minMatched: 5,
      maxMatched: 9,
      minGrade: 3,
      banNamePatterns: ["\u6EF4\u5B9A", "\u785D\u9178\u94F6", "\u725B\u987F\u5B9A\u5F8B", "\u5FAE\u79EF\u5206", "\u7EDF\u8BA1\u63A8\u65AD", "\u671D\u82B1\u5915\u62FE", "\u6574\u672C\u4E66\u9605\u8BFB", "\u6587\u8A00", "\u5916\u56FD\u6587\u5B66", "\u673A\u68B0\u73A9\u5177", "\u673A\u5668\u4EBA", "\u7A0B\u5E8F\u8BBE\u8BA1", "\u7535\u89E3\u6C60"],
      preferNamePatterns: ["\u690D\u7269", "\u5149\u5408", "\u79CD\u5B50", "\u840C\u53D1", "\u751F\u957F", "\u7EFF\u8272", "\u6839", "\u84B8\u817E", "\u5206\u7C7B", "\u683D\u57F9", "\u6761\u5F62\u7EDF\u8BA1", "\u6298\u7EBF\u7EDF\u8BA1"],
      modules: [
        { id: "taxonomy", label: "\u690D\u7269\u8BC6\u522B\u4E0E\u5206\u7C7B", hints: ["\u690D\u7269", "\u5206\u7C7B", "\u7279\u5F81", "\u7ED3\u6784", "\u5668\u5B98", "\u7EFF\u8272", "\u88AB\u5B50"], subjects: ["science", "biology"], topK: 2 },
        { id: "growth", label: "\u751F\u957F\u4E0E\u73AF\u5883", hints: ["\u751F\u957F", "\u5149\u5408", "\u547C\u5438", "\u79CD\u5B50", "\u840C\u53D1", "\u6839", "\u84B8\u817E", "\u73AF\u5883", "\u6C34\u5206"], subjects: ["science", "biology"], topK: 2 },
        { id: "cultivate", label: "\u683D\u57F9\u5B9E\u64CD", hints: ["\u79CD\u690D", "\u683D\u57F9", "\u571F\u58E4", "\u6D47\u6C34", "\u65BD\u80A5", "\u79FB\u683D", "\u517B\u62A4", "\u6266\u63D2"], subjects: ["science", "biology"], topK: 2 },
        { id: "observe", label: "\u89C2\u5BDF\u8BB0\u5F55", hints: ["\u89C2\u5BDF", "\u8BB0\u5F55", "\u6D4B\u91CF", "\u6570\u636E", "\u56FE\u8868", "\u53D8\u5316", "\u9AD8\u5EA6"], subjects: ["science", "math"], topK: 2 },
        { id: "share", label: "\u79CD\u690D\u65E5\u8BB0", hints: ["\u65E5\u8BB0", "\u62A5\u544A", "\u603B\u7ED3", "\u5206\u4EAB", "\u8BF4\u660E", "\u5199\u4F5C"], subjects: ["chinese"], topK: 2 }
      ]
    },
    {
      id: "labor-practice",
      label: "\u52B3\u52A8\u5B9E\u8DF5/\u70F9\u996A\u624B\u5DE5",
      projectType: "labor-practice",
      matchPatterns: ["\u70F9\u996A|\u70D8\u7119|\u624B\u5DE5\u5236\u4F5C|\u52B3\u52A8\u5B9E\u8DF5|\u7F16\u7EC7|\u7F1D\u7EAB"],
      gradeBand: [1, 9],
      primarySystem: "cn",
      subjects: ["science", "biology", "chinese", "math"],
      minMatched: 4,
      maxMatched: 8,
      minGrade: 3,
      banNamePatterns: ["\u6EF4\u5B9A", "\u785D\u9178\u94F6", "\u725B\u987F\u5B9A\u5F8B", "\u5FAE\u79EF\u5206", "\u7EDF\u8BA1\u63A8\u65AD", "\u671D\u82B1\u5915\u62FE", "\u6574\u672C\u4E66\u9605\u8BFB", "\u6587\u8A00", "\u5916\u56FD\u6587\u5B66"],
      preferNamePatterns: ["\u690D\u7269", "\u5149\u5408", "\u79CD\u5B50", "\u751F\u957F", "\u7EFF\u8272", "\u683D\u57F9", "\u840C\u53D1"],
      modules: [
        { id: "prepare", label: "\u8BA4\u8BC6\u51C6\u5907", hints: ["\u690D\u7269", "\u79CD\u5B50", "\u5149\u5408", "\u751F\u957F", "\u6750\u6599", "\u5DE5\u5177"], subjects: ["science", "biology"], topK: 2 },
        { id: "practice", label: "\u64CD\u4F5C\u5B9E\u8DF5", hints: ["\u79CD\u690D", "\u683D\u57F9", "\u70F9\u996A", "\u5236\u4F5C", "\u64CD\u4F5C", "\u6B65\u9AA4"], subjects: ["science", "biology"], topK: 2 },
        { id: "record", label: "\u89C2\u5BDF\u8BB0\u5F55", hints: ["\u89C2\u5BDF", "\u8BB0\u5F55", "\u6D4B\u91CF", "\u6570\u636E", "\u53D8\u5316", "\u751F\u957F"], subjects: ["science", "math"], topK: 2 },
        { id: "share", label: "\u6210\u679C\u5206\u4EAB", hints: ["\u6210\u679C", "\u5206\u4EAB", "\u603B\u7ED3", "\u62A5\u544A"], subjects: ["chinese"], topK: 2 }
      ]
    },
    {
      id: "creative-media",
      label: "\u521B\u610F\u5A92\u4F53/\u6D77\u62A5\u89C6\u9891",
      projectType: "creative-media",
      matchPatterns: ["\u6D77\u62A5|\u77ED\u89C6\u9891|\u5FAE\u7535\u5F71|\u52A8\u753B|\u6F2B\u753B|\u6444\u5F71|\u89C6\u89C9\u8BBE\u8BA1|\u6587\u521B"],
      gradeBand: [6, 12],
      primarySystem: "cn",
      subjects: ["chinese", "info-tech", "art"],
      minMatched: 4,
      maxMatched: 9,
      minGrade: 6,
      banNamePatterns: ["100\u4EE5\u5185", "\u725B\u987F\u5B9A\u5F8B", "\u5316\u5B66\u65B9\u7A0B\u5F0F", "\u7535\u89E3\u6C60"],
      modules: [
        { id: "idea", label: "\u521B\u610F\u6784\u601D", hints: ["\u521B\u610F", "\u4E3B\u9898", "\u53D7\u4F17", "\u6784\u601D"], subjects: ["chinese"], topK: 2 },
        { id: "design", label: "\u8BBE\u8BA1\u8349\u6848", hints: ["\u8BBE\u8BA1", "\u8349\u56FE", "\u5206\u955C", "\u6392\u7248", "\u8272\u5F69"], subjects: ["info-tech", "chinese"], topK: 2 },
        { id: "make", label: "\u5236\u4F5C\u5B9E\u73B0", hints: ["\u5236\u4F5C", "\u526A\u8F91", "\u7ED8\u5236", "\u7F16\u8F91"], subjects: ["info-tech"], topK: 2 },
        { id: "show", label: "\u5C55\u793A\u8BC4\u8BAE", hints: ["\u5C55\u793A", "\u8BC4\u8BAE", "\u53D1\u5E03", "\u53CD\u9988"], subjects: ["chinese"], topK: 2 }
      ]
    },
    {
      id: "exhibition-redesign",
      label: "\u5C55\u9648\u7A7A\u95F4/\u573A\u9986\u6539\u9020",
      projectType: "exhibition-redesign",
      matchPatterns: ["\u592A\u7A7A\u9986", "\u5929\u6587\u9986", "\u822A\u5929\u9986", "\u79D1\u6280\u9986", "\u535A\u7269\u9986", "\u5C55\u5385", "\u5C55\u9648", "\u91CD\u5851.*\u9986", "\u6539\u9020.*\u9986", "\u5931\u63A7.*\u9986"],
      gradeBand: [5, 12],
      primarySystem: "cn",
      subjects: ["science", "chinese", "math", "info-tech"],
      minMatched: 5,
      maxMatched: 10,
      minGrade: 5,
      banNamePatterns: ["100\u4EE5\u5185", "20\u4EE5\u5185", "\u62DB\u751F\u7B80\u7AE0", "\u7A0B\u5E8F\u8BBE\u8BA1", "\u7535\u89E3\u6C60", "\u539F\u7535\u6C60", "\u725B\u987F\u5B9A\u5F8B", "\u7EBF\u6027\u89C4\u5212", "\u5916\u56FD\u6587\u5B66", "\u671D\u82B1\u5915\u62FE", "\u8BD7\u8BCD\u6B23\u8D4F"],
      preferNamePatterns: ["\u592A\u9633\u7CFB", "\u5730\u7403", "\u5B87\u5B99", "\u8BF4\u660E", "\u7EDF\u8BA1", "\u8C03\u67E5", "\u8BBE\u8BA1", "\u5929\u6587", "\u592A\u7A7A", "\u6708\u7403"],
      modules: [
        { id: "diagnose", label: "\u73B0\u72B6\u8BCA\u65AD", hints: ["\u8C03\u67E5", "\u7EDF\u8BA1", "\u8BB0\u5F55", "\u95EE\u9898", "\u73B0\u72B6"], subjects: ["chinese", "math"], topK: 2 },
        { id: "theme", label: "\u4E3B\u9898\u7B56\u5212", hints: ["\u592A\u9633\u7CFB", "\u6708\u7403", "\u592A\u7A7A", "\u5929\u6587", "\u5B87\u5B99", "\u79D1\u666E"], subjects: ["science", "chinese"], topK: 2 },
        { id: "design", label: "\u5C55\u9648\u8BBE\u8BA1", hints: ["\u8BBE\u8BA1", "\u5E03\u5C40", "\u5C55\u677F", "\u6A21\u578B", "\u4E92\u52A8"], subjects: ["info-tech", "chinese"], topK: 2 },
        { id: "implement", label: "\u5B9E\u65BD\u6574\u6539", hints: ["\u9884\u7B97", "\u7EDF\u8BA1", "\u5206\u5DE5", "\u5E03\u7F6E", "\u5B89\u5168"], subjects: ["math", "chinese"], topK: 2 },
        { id: "launch", label: "\u5F00\u653E\u9A8C\u6536", hints: ["\u8BF4\u660E", "\u5C55\u793A", "\u8BB2\u89E3", "\u62A5\u544A", "\u5BA3\u4F20"], subjects: ["chinese", "science"], topK: 2 }
      ]
    },
    {
      id: "industry-innovation",
      label: "\u4EA7\u4E1A\u521B\u65B0/\u4F4E\u7A7A\u7ECF\u6D4E\u63A2\u7A76",
      projectType: "industry-innovation",
      matchPatterns: ["\u4F4E\u7A7A\u7ECF\u6D4E", "\u4F4E\u7A7A\u98DE\u884C", "\u4F4E\u7A7A\u7A7A\u57DF", "\u7A7A\u57DF\u7BA1\u7406", "\u901A\u822A\u4EA7\u4E1A", "\u57CE\u5E02\u7A7A\u4E2D\u4EA4\u901A", "eVTOL", "\u4F4E\u7A7A\u7269\u6D41", "\u901A\u7528\u822A\u7A7A", "\u65B0\u5174\u4EA7\u4E1A", "\u4EA7\u4E1A\u521B\u65B0", "\u63A2\u5BFB.*\u521B\u65B0", "\u63A2\u7D22.*\u521B\u65B0"],
      gradeBand: [7, 12],
      primarySystem: "cn",
      subjects: ["geography", "chinese", "math", "physics", "history"],
      minMatched: 5,
      maxMatched: 10,
      minGrade: 7,
      banNamePatterns: ["100\u4EE5\u5185", "20\u4EE5\u5185", "\u73B0\u4EE3\u7269\u6D41\u7BA1\u7406", "\u667A\u6167\u57CE\u5E02", "\u5DE5\u7A0B\u8BBE\u8BA1", "\u7535\u89E3\u6C60", "\u539F\u7535\u6C60", "\u7EC6\u80DE", "\u8BD7\u8BCD\u6B23\u8D4F", "\u4EBA\u7269\u63CF\u5199", "\u7EBF\u6027\u89C4\u5212", "\u7A0B\u5E8F\u8BBE\u8BA1", "\u5916\u56FD\u6587\u5B66"],
      preferNamePatterns: ["\u4EA4\u901A", "\u5730\u7406", "\u7EDF\u8BA1", "\u8C03\u67E5", "\u8BF4\u660E", "\u98DE\u884C", "\u822A\u7A7A", "\u629B\u4F53", "\u725B\u987F", "\u533A\u57DF", "\u7ECF\u6D4E", "\u6570\u636E", "\u56FE\u8868"],
      modules: [
        { id: "background", label: "\u4EA7\u4E1A\u80CC\u666F\u4E0E\u653F\u7B56", hints: ["\u4EA4\u901A", "\u533A\u57DF", "\u7ECF\u6D4E", "\u5730\u7406", "\u4EA7\u4E1A", "\u653F\u7B56", "\u53D1\u5C55", "\u5E03\u5C40"], subjects: ["geography", "history", "chinese"], topK: 2 },
        { id: "scenarios", label: "\u5E94\u7528\u573A\u666F\u8C03\u7814", hints: ["\u8C03\u67E5", "\u7EDF\u8BA1", "\u6570\u636E", "\u95EE\u5377", "\u7269\u6D41", "\u5E94\u6025", "\u914D\u9001", "\u5E94\u7528", "\u573A\u666F"], subjects: ["math", "chinese", "geography"], topK: 2 },
        { id: "tech", label: "\u6280\u672F\u539F\u7406\u652F\u6491", hints: ["\u98DE\u884C", "\u629B\u4F53", "\u725B\u987F", "\u8FD0\u52A8", "\u529B\u5B66", "\u822A\u7A7A", "\u65E0\u4EBA\u673A", "\u5B89\u5168"], subjects: ["physics", "science"], topK: 2 },
        { id: "analysis", label: "\u6570\u636E\u53EF\u884C\u6027\u5206\u6790", hints: ["\u7EDF\u8BA1", "\u56FE\u8868", "\u6BD4\u8F83", "\u5206\u6790", "\u6210\u672C", "\u6548\u76CA", "\u6570\u636E", "\u767E\u5206\u6BD4"], subjects: ["math"], topK: 2 },
        { id: "proposal", label: "\u521B\u65B0\u65B9\u6848\u62A5\u544A", hints: ["\u8BF4\u660E", "\u62A5\u544A", "\u8BBA\u8BC1", "\u5199\u4F5C", "\u65B9\u6848", "\u5EFA\u8BAE", "\u521B\u65B0"], subjects: ["chinese", "geography"], topK: 2 }
      ]
    },
    {
      id: "environmental-filtration",
      label: "\u6C34\u4F53\u51C0\u5316/\u8FC7\u6EE4\u88C5\u7F6E\u5DE5\u7A0B",
      projectType: "engineering",
      matchPatterns: ["\u5FAE\u5851\u6599", "\u8FC7\u6EE4\u88C5\u7F6E", "\u51C0\u6C34", "\u6C61\u6C34\u5904\u7406", "\u5E9F\u6C34\u5904\u7406", "\u6C34\u8D28\u51C0\u5316", "\u8FC7\u6EE4\u7CFB\u7EDF", "\u6EE4\u82AF", "\u6D3B\u6027\u70AD\u8FC7\u6EE4", "\u6C89\u6DC0\u8FC7\u6EE4", "\u819C\u8FC7\u6EE4", "\u51C0\u6C34\u5668", "\u62E6\u622A.*\u5851\u6599", "\u6D17\u8863.*\u5E9F\u6C34", "\u8FC7\u6EE4.*\u6C34"],
      gradeBand: [4, 12],
      primarySystem: "cn",
      extensionSystems: ["ap"],
      subjects: ["science", "chemistry", "physics", "math"],
      minMatched: 5,
      maxMatched: 12,
      minGrade: 4,
      banNamePatterns: [
        "100\u4EE5\u5185",
        "20\u4EE5\u5185",
        "\u8BA4\u8BC6\u56FE\u5F62",
        "\u4EBA\u7269\u63CF\u5199",
        "\u8BD7\u8BCD",
        "\u6587\u8A00",
        "\u706B\u7BAD",
        "\u53CD\u51B2",
        "\u629B\u4F53",
        "\u5F39\u9053",
        "\u53D1\u5C04",
        "\u7A0B\u5E8F\u8BBE\u8BA1",
        "\u53D8\u91CF/\u6570\u636E\u7C7B\u578B",
        "\u7B97\u6CD5",
        "\u7269\u8054\u7F51",
        "\u7535\u89E3\u6C60",
        "\u539F\u7535\u6C60",
        "\u7EC6\u80DE\u7ED3\u6784",
        "\u4EBA\u4F53\u5668\u5B98"
      ],
      preferNamePatterns: ["\u8FC7\u6EE4", "\u6C89\u6DC0", "\u5438\u9644", "\u6EB6\u6DB2", "\u79BB\u5B50", "\u538B\u5F3A", "\u6D41\u4F53", "\u5B9E\u9A8C", "\u6D4B\u91CF", "\u7EDF\u8BA1", "\u73AF\u5883", "\u6C61\u67D3"],
      modules: [
        { id: "scope", label: "\u6307\u6807\u4E0E\u5C40\u9650", hints: ["\u6307\u6807", "\u5C40\u9650", "\u5B89\u5168", "\u5BA3\u79F0", "\u5BF9\u7167", "\u53D8\u91CF", "\u5B9E\u9A8C"], subjects: ["science", "chinese"], topK: 2 },
        { id: "prefilter", label: "\u7C97\u6EE4\u4FDD\u62A4\u5C42", hints: ["\u7C97\u6EE4", "\u6EE4\u7F51", "\u6C89\u6DC0", "\u6CE5\u6C99", "\u9897\u7C92", "\u4FDD\u62A4", "\u6EE4\u7EB8"], subjects: ["science", "physics"], topK: 2 },
        { id: "adsorption", label: "\u5438\u9644\u6539\u5473\u5C42", hints: ["\u5438\u9644", "\u6D3B\u6027\u70AD", "\u5F02\u5473", "\u989C\u8272", "\u6709\u673A\u7269"], subjects: ["chemistry", "science"], topK: 2 },
        { id: "membrane", label: "\u819C\u5B54\u5F84\u6838\u5FC3\u5C42", hints: ["\u819C", "\u5B54\u5F84", "\u6EE4\u82AF", "\u5FAE\u6EE4", "\u8D85\u6EE4", "\u9676\u74F7", "\u62E6\u622A", "\u5FAE\u5851\u6599"], subjects: ["chemistry", "physics", "science"], topK: 2 },
        { id: "test", label: "\u5BF9\u7167\u6D4B\u8BD5\u4E0E\u8BC4\u4EF7", hints: ["\u6D4B\u8BD5", "\u5BF9\u7167", "\u6D41\u901F", "\u6570\u636E", "\u5B9E\u9A8C", "\u8BB0\u5F55", "\u51CF\u5C11\u7387", "\u7EDF\u8BA1"], subjects: ["science", "math", "physics"], topK: 2 }
      ]
    },
    {
      id: "maker-engineering",
      label: "\u901A\u7528\u88C5\u7F6E/\u521B\u5BA2\u5DE5\u7A0B",
      projectType: "engineering",
      matchPatterns: [],
      gradeBand: [6, 12],
      primarySystem: "cn",
      extensionSystems: ["ap"],
      subjects: ["physics", "science", "chemistry", "math", "info-tech"],
      minMatched: 5,
      maxMatched: 12,
      minGrade: 6,
      banNamePatterns: [
        "100\u4EE5\u5185",
        "20\u4EE5\u5185",
        "\u8BA4\u8BC6\u56FE\u5F62",
        "\u4EBA\u7269\u63CF\u5199",
        "\u8BD7\u8BCD",
        "\u6587\u8A00",
        "\u7535\u89E3\u6C60",
        "\u539F\u7535\u6C60",
        "\u7EC6\u80DE\u7ED3\u6784",
        "\u4EBA\u4F53\u5668\u5B98",
        "\u7A0B\u5E8F\u8BBE\u8BA1",
        "\u53D8\u91CF/\u6570\u636E\u7C7B\u578B",
        "\u6709\u673A\u5408\u6210",
        "\u6709\u673A\u5316\u5408\u7269",
        "\u70C3",
        "\u79BB\u5B50\u68C0\u9A8C",
        "\u9187",
        "\u915A",
        "\u919B",
        "\u916E",
        "\u7FA7\u9178",
        "\u7EC6\u80DE\u819C",
        "\u539F\u5B50\u7ED3\u6784",
        "\u5316\u5B66\u5E73\u8861",
        "\u751F\u6001\u7CFB\u7EDF\u7ED3\u6784",
        "\u751F\u7269\u819C",
        "\u7EC6\u80DE\u7ED3\u6784"
      ],
      preferNamePatterns: [
        "\u7ED3\u6784",
        "\u53D7\u529B",
        "\u538B\u5F3A",
        "\u6469\u64E6",
        "\u5E73\u8861",
        "\u6750\u6599",
        "\u6D4B\u91CF",
        "\u5B9E\u9A8C",
        "\u8BBE\u8BA1",
        "\u5236\u4F5C",
        "\u529B",
        "\u6760\u6746",
        "\u7B80\u5355\u673A\u68B0"
      ],
      modules: [
        { id: "requirements", label: "\u9700\u6C42\u4E0E\u6307\u6807", hints: ["\u9700\u6C42", "\u6307\u6807", "\u8C03\u7814", "\u7EA6\u675F", "\u573A\u666F", "\u76EE\u6807"], subjects: ["chinese", "math", "science"], topK: 2 },
        { id: "design", label: "\u65B9\u6848\u4E0E\u7ED3\u6784", hints: ["\u65B9\u6848", "\u8BBE\u8BA1", "\u7ED3\u6784", "\u6750\u6599", "\u539F\u7406", "\u8349\u56FE", "\u53D7\u529B", "\u538B\u5F3A", "\u5E73\u8861"], subjects: ["physics", "science", "math"], topK: 2 },
        { id: "build", label: "\u5236\u4F5C\u4E0E\u7EC4\u88C5", hints: ["\u5236\u4F5C", "\u7EC4\u88C5", "\u52A0\u5DE5", "\u7535\u8DEF", "\u88C5\u914D", "\u642D\u5EFA"], subjects: ["science", "physics", "info-tech"], topK: 2 },
        { id: "test", label: "\u6D4B\u8BD5\u4E0E\u8FED\u4EE3", hints: ["\u6D4B\u8BD5", "\u6D4B\u91CF", "\u6570\u636E", "\u8BEF\u5DEE", "\u6539\u8FDB", "\u8BB0\u5F55", "\u5B9E\u9A8C"], subjects: ["physics", "math", "science"], topK: 2 }
      ]
    },
    {
      id: "general-practice",
      label: "\u7EFC\u5408\u5B9E\u8DF5\uFF08\u901A\u7528\uFF09",
      projectType: "general",
      matchPatterns: [],
      gradeBand: [4, 12],
      primarySystem: "cn",
      subjects: ["chinese", "math", "geography", "history", "politics", "psychology"],
      minMatched: 4,
      maxMatched: 10,
      minGrade: 4,
      banNamePatterns: ["100\u4EE5\u5185", "20\u4EE5\u5185", "\u6279\u5224\u6027\u601D\u7EF4", "\u56E2\u961F\u534F\u4F5C", "\u9879\u76EE\u7BA1\u7406", "\u6838\u5FC3\u7D20\u517B", "\u7EBF\u6027\u89C4\u5212", "\u4E09\u89D2\u51FD\u6570", "\u7535\u5B66\u5B9E\u9A8C", "\u5916\u56FD\u6587\u5B66", "\u671D\u82B1\u5915\u62FE"],
      preferNamePatterns: ["\u8C03\u67E5", "\u7EDF\u8BA1", "\u8BF4\u660E", "\u8BBE\u8BA1", "\u9605\u8BFB", "\u56FE\u4E66"],
      modules: [
        { id: "define", label: "\u8C03\u7814\u5B9A\u4E49", hints: ["\u8C03\u7814", "\u9700\u6C42", "\u8C03\u67E5", "\u9605\u8BFB", "\u56FE\u4E66"], subjects: ["chinese", "math"], topK: 2 },
        { id: "design", label: "\u65B9\u6848\u8BBE\u8BA1", hints: ["\u65B9\u6848", "\u8BBE\u8BA1", "\u89C4\u5212", "\u5E03\u7F6E", "\u5206\u5DE5"], subjects: ["math", "chinese", "geography"], topK: 2 },
        { id: "make", label: "\u5B9E\u65BD\u8868\u8FBE", hints: ["\u5B9E\u65BD", "\u8BB0\u5F55", "\u6267\u884C", "\u8868\u8FBE"], subjects: ["chinese", "math"], topK: 2 },
        { id: "test", label: "\u6D4B\u8BD5\u5C55\u793A", hints: ["\u6D4B\u8BD5", "\u8BC4\u4F30", "\u5C55\u793A", "\u62A5\u544A"], subjects: ["math", "chinese"], topK: 2 }
      ]
    }
  ],
  typeFallback: {
    engineering: "maker-engineering",
    "consumer-decision": "consumer-decision",
    "social-inquiry": "social-inquiry",
    "scientific-inquiry": "direct-chemistry",
    "humanities-literary": "humanities-writing",
    "study-trip": "study-trip",
    "life-planning": "life-planning",
    "business-economics": "business-economics",
    "health-life": "health-life",
    "planting-cultivation": "planting-cultivation",
    "labor-practice": "labor-practice",
    "creative-media": "creative-media",
    "industry-innovation": "industry-innovation",
    "exhibition-redesign": "exhibition-redesign",
    general: "general-practice"
  }
};
var engineering_registry_default = {
  version: "1.0",
  entries: [
    {
      id: "ext-rocket-safety",
      name: "\u6A21\u578B\u706B\u7BAD\u5B89\u5168\u53D1\u5C04\u89C4\u8303",
      archetypes: ["water-rocket"],
      moduleId: "test",
      gradeBand: [7, 12],
      reason: "\u53D1\u5C04\u89D2\u5EA6\u3001\u8B66\u6212\u8DDD\u79BB\u3001\u6CE8\u6C34\u6BD4\u4F8B\u7B49\u5B89\u5168\u64CD\u4F5C\uFF0C\u8BFE\u6807\u65E0\u4E13\u9879\u6761\u76EE\u4F46\u5B9E\u9A8C\u5FC5\u9700",
      taskSnippet: "\u5236\u5B9A\u53D1\u5C04\u5B89\u5168\u68C0\u67E5\u8868\uFF1A\u89D2\u5EA6\u226475\xB0\u3001\u9000\u79BB\u226515m\u3001\u7981\u6B62\u5BF9\u4EBA\u53D1\u5C04",
      prerequisites: ["\u725B\u987F\u8FD0\u52A8\u5B9A\u5F8B", "\u538B\u5F3A"]
    },
    {
      id: "ext-cp-cg",
      name: "\u91CD\u5FC3\u4E0E\u538B\u5FC3\u6D4B\u91CF",
      archetypes: ["water-rocket"],
      moduleId: "aerodynamics",
      gradeBand: [8, 12],
      reason: "\u7BAD\u4F53\u7A33\u5B9A\u6027\u5224\u65AD\u9700\u538B\u5FC3/\u91CD\u5FC3\u76F8\u5BF9\u4F4D\u7F6E\uFF0C\u8BFE\u672C\u8F83\u5C11\u5C55\u5F00\u6D4B\u91CF\u65B9\u6CD5",
      taskSnippet: "\u60AC\u6302\u6CD5\u6D4B\u91CD\u5FC3\uFF0C\u98CE\u6D1E\u6216\u7ECF\u9A8C\u516C\u5F0F\u4F30\u7B97\u538B\u5FC3\u4F4D\u7F6E\u5E76\u6807\u6CE8\u5728\u7BAD\u4F53\u8349\u56FE\u4E0A",
      prerequisites: ["\u529B\u7684\u5E73\u8861"]
    },
    {
      id: "ext-nozzle",
      name: "\u55B7\u5634\u6D41\u91CF\u4E0E\u53CD\u51B2\u63A8\u529B\u4F30\u7B97",
      archetypes: ["water-rocket"],
      moduleId: "propulsion",
      gradeBand: [9, 12],
      reason: "\u8FDE\u63A5\u53CD\u51B2\u8FD0\u52A8\u4E0E\u5B9E\u9645\u55B7\u6C34\u6D41\u91CF\uFF0C\u5DE5\u7A0B\u4F30\u7B97\u8D85\u51FA\u8BFE\u672C",
      taskSnippet: "\u8BB0\u5F55\u74F6\u5185\u6C14\u538B\u3001\u55B7\u53E3\u76F4\u5F84\uFF0C\u7528\u7B80\u5316\u6A21\u578B\u4F30\u7B97\u521D\u59CB\u63A8\u529B\u5CF0\u503C",
      prerequisites: ["\u52A8\u91CF", "\u538B\u5F3A"]
    },
    {
      id: "ext-titration-ware",
      name: "\u6EF4\u5B9A\u7BA1/\u79FB\u6DB2\u7BA1\u64CD\u4F5C\u89C4\u8303",
      archetypes: ["mixed-solution-chemistry"],
      moduleId: "titration",
      gradeBand: [9, 12],
      reason: "\u5B9A\u91CF\u6EF4\u5B9A\u5668\u76BF\u6DA6\u6D17\u4E0E\u8BFB\u6570\u7EC6\u8282\uFF0C\u5B9E\u9A8C\u64CD\u4F5C\u5FC5\u9700",
      taskSnippet: "\u5B8C\u6210\u6EF4\u5B9A\u7BA1\u68C0\u6F0F\u3001\u6DA6\u6D17\u3001\u521D\u8BFB\u6570\u8BB0\u5F55\uFF0C\u9644\u64CD\u4F5C\u7167\u7247",
      prerequisites: ["\u7269\u8D28\u7684\u91CF\u6D53\u5EA6"]
    },
    {
      id: "ext-agno3-prep",
      name: "\u785D\u9178\u94F6\u6807\u51C6\u6EB6\u6DB2\u914D\u5236",
      archetypes: ["mixed-solution-chemistry"],
      moduleId: "titration",
      gradeBand: [10, 12],
      reason: "\u6C89\u6DC0\u6EF4\u5B9A\u5173\u952E\u8BD5\u5242\u51C6\u5907\uFF0C\u9700\u8BFE\u5916\u5B9E\u9A8C\u6307\u5BFC",
      taskSnippet: "\u8BA1\u7B97\u5E76\u914D\u5236\u4E00\u5B9A\u7269\u8D28\u7684\u91CF\u6D53\u5EA6\u7684 AgNO\u2083 \u6EB6\u6DB2\uFF0C\u6CE8\u660E\u907F\u5149\u4FDD\u5B58",
      prerequisites: ["\u7269\u8D28\u7684\u91CF\u6D53\u5EA6", "\u79BB\u5B50\u53CD\u5E94"]
    },
    {
      id: "ext-conductivity-cal",
      name: "\u7535\u5BFC\u7387\u4EEA\u6821\u51C6\u4E0E\u6E29\u5EA6\u8865\u507F",
      archetypes: ["mixed-solution-chemistry"],
      moduleId: "conductivity",
      gradeBand: [10, 12],
      reason: "\u7535\u5BFC\u7387\u6D4B\u5B9A\u987B\u63A7\u5236\u6E29\u5EA6\u5F71\u54CD\uFF0C\u4EEA\u5668\u64CD\u4F5C\u8D85\u51FA\u8BFE\u672C",
      taskSnippet: "\u7528\u6807\u51C6 KCl \u6EB6\u6DB2\u6821\u51C6\u7535\u5BFC\u7387\u4EEA\uFF0C\u8BB0\u5F55\u6E29\u5EA6\u8865\u507F\u8BBE\u7F6E",
      prerequisites: ["\u7535\u89E3\u8D28\u6EB6\u6DB2"]
    },
    {
      id: "ext-sample-prep",
      name: "\u98DF\u5802\u6C64\u6C34\u53D6\u6837\u4E0E\u4EE3\u8868\u6027",
      archetypes: ["mixed-solution-chemistry"],
      moduleId: "constraint",
      gradeBand: [8, 12],
      reason: "\u771F\u5B9E\u6837\u54C1\u53D6\u6837\u89C4\u8303\u4E0E\u4EE3\u8868\u6027\u5224\u65AD\uFF0C\u98DF\u54C1\u5B89\u5168\u76F8\u5173",
      taskSnippet: "\u8BBE\u8BA1\u5E73\u884C\u53D6\u6837\u65B9\u6848\uFF1A\u6F84\u6E05\u3001\u5B9A\u5BB9\u3001\u6807\u6CE8\u53D6\u6837\u65F6\u95F4\u4E0E\u4F4D\u7F6E",
      prerequisites: []
    },
    {
      id: "ext-tco",
      name: "\u5168\u751F\u547D\u5468\u671F\u7528\u8F66\u6210\u672C\uFF08TCO\uFF09",
      archetypes: ["consumer-decision"],
      moduleId: "cost",
      gradeBand: [8, 12],
      reason: "\u8D2D\u8F66\u51B3\u7B56\u9700 5 \u5E74\u603B\u6210\u672C\u6A21\u578B\uFF0C\u8BFE\u6807\u672A\u7CFB\u7EDF\u8BB2\u6388",
      taskSnippet: "\u5EFA\u7ACB TCO \u8868\uFF1A\u8D2D\u7F6E+5\u5E74\u80FD\u8017+\u4FDD\u517B+\u4FDD\u9669\uFF0C\u5BF9\u6BD4\u4E24\u6B3E\u8F66\u578B",
      prerequisites: ["\u7EDF\u8BA1", "\u767E\u5206\u6BD4"]
    },
    {
      id: "ext-ev-policy",
      name: "\u65B0\u80FD\u6E90\u6C7D\u8F66\u8D2D\u7F6E\u8865\u8D34\u4E0E\u7A0E\u8D39",
      archetypes: ["consumer-decision"],
      moduleId: "cost",
      gradeBand: [8, 12],
      reason: "\u653F\u7B56\u76F4\u63A5\u5F71\u54CD\u8D2D\u8F66\u6210\u672C\uFF0C\u9700\u67E5\u9605\u8BFE\u5916\u653F\u7B56\u8D44\u6599",
      taskSnippet: "\u68C0\u7D22\u672C\u5730\u65B0\u80FD\u6E90\u8865\u8D34/\u514D\u8D2D\u7F6E\u7A0E\u653F\u7B56\uFF0C\u8BA1\u5165\u6210\u672C\u5BF9\u6BD4\u8868",
      prerequisites: []
    },
    {
      id: "ext-residual",
      name: "\u8F66\u8F86\u4FDD\u503C\u7387\u4E0E\u6B8B\u503C\u8BC4\u4F30",
      archetypes: ["consumer-decision"],
      moduleId: "decision",
      gradeBand: [9, 12],
      reason: "\u4E8C\u624B\u6B8B\u503C\u662F\u9009\u8F66\u91CD\u8981\u7EF4\u5EA6\uFF0C\u8BFE\u672C\u901A\u5E38\u4E0D\u6D89\u53CA",
      taskSnippet: "\u67E5\u9605\u4E8C\u624B\u8F66\u5E73\u53F0\u6570\u636E\uFF0C\u4F30\u7B97 3 \u5E74\u540E\u6B8B\u503C\u7387\u5E76\u5199\u5165\u51B3\u7B56\u62A5\u544A",
      prerequisites: ["\u7EDF\u8BA1"]
    },
    {
      id: "ext-charging",
      name: "\u5145\u7535\u4FBF\u5229\u6027\u4E0E\u7EED\u822A\u573A\u666F\u8BC4\u4F30",
      archetypes: ["consumer-decision"],
      moduleId: "needs",
      gradeBand: [7, 12],
      reason: "\u65B0\u80FD\u6E90\u7528\u8F66\u9700\u7ED3\u5408\u5BB6\u5EAD\u5145\u7535\u6761\u4EF6\uFF0C\u5C5E\u5B9E\u8DF5\u8C03\u7814",
      taskSnippet: "\u8C03\u67E5\u5BB6\u5EAD/\u5C0F\u533A\u5145\u7535\u6869\u6761\u4EF6\uFF0C\u5339\u914D\u65E5\u5E38\u901A\u52E4\u91CC\u7A0B\u9700\u6C42",
      prerequisites: []
    },
    {
      id: "ext-survey-validity",
      name: "\u95EE\u5377\u4FE1\u6548\u5EA6\u57FA\u672C\u68C0\u9A8C",
      archetypes: ["social-inquiry"],
      moduleId: "topic",
      gradeBand: [8, 12],
      reason: "\u8C03\u67E5\u5DE5\u5177\u8D28\u91CF\u4FDD\u969C\uFF0C\u8BFE\u6807\u63D0\u53CA\u8F83\u5C11",
      taskSnippet: "\u9884\u8C03\u67E5 5 \u4EBA\u540E\u4FEE\u8BA2\u95EE\u5377\uFF0C\u5220\u9664\u8868\u8FF0\u4E0D\u6E05\u7684\u9898\u76EE",
      prerequisites: ["\u6570\u636E\u7684\u6536\u96C6"]
    },
    {
      id: "ext-interview-ethics",
      name: "\u8BBF\u8C08\u4F26\u7406\u4E0E\u77E5\u60C5\u540C\u610F",
      archetypes: ["social-inquiry"],
      moduleId: "collect",
      gradeBand: [7, 12],
      reason: "\u7530\u91CE\u8C03\u67E5\u4F26\u7406\u8981\u6C42\uFF0C\u8BFE\u672C\u901A\u5E38\u4E0D\u5355\u72EC\u8BB2\u6388",
      taskSnippet: "\u8BBE\u8BA1\u8BBF\u8C08\u5F00\u573A\u8BF4\u660E\u4E0E\u533F\u540D\u627F\u8BFA\uFF0C\u53D7\u8BBF\u8005\u7B7E\u5B57\u786E\u8BA4",
      prerequisites: []
    },
    {
      id: "ext-petition-format",
      name: "\u5021\u8BAE\u4E66\u683C\u5F0F\u4E0E\u843D\u6B3E\u89C4\u8303",
      archetypes: ["application-writing"],
      moduleId: "format",
      gradeBand: [6, 12],
      reason: "\u5E94\u7528\u6587\u5199\u4F5C\u683C\u5F0F\u7EC6\u8282\uFF0C\u8BFE\u5802\u5E38\u9700\u4E13\u9879\u63D0\u9192",
      taskSnippet: "\u6309\u6807\u9898\u3001\u79F0\u547C\u3001\u6B63\u6587\u3001\u843D\u6B3E\u3001\u65E5\u671F\u4E94\u90E8\u5206\u6392\u7248\uFF0C\u9644\u8303\u6587\u5BF9\u7167",
      prerequisites: ["\u5E94\u7528\u6587"]
    },
    {
      id: "ext-poetry-workshop",
      name: "\u8BD7\u6B4C\u4FEE\u6539\u5DE5\u4F5C\u574A\u6D41\u7A0B",
      archetypes: ["humanities-writing"],
      moduleId: "revise",
      gradeBand: [6, 12],
      reason: "\u4E92\u8BC4\u4FEE\u6539\u7684\u7EC4\u7EC7\u65B9\u6CD5\uFF0C\u8BFE\u672C\u8F83\u5C11\u7CFB\u7EDF\u8BB2\u6388",
      taskSnippet: "\u4E09\u4EBA\u4E00\u7EC4\u4E92\u8BC4\uFF1A\u6807\u51FA\u610F\u8C61\u3001\u8282\u594F\u3001\u7528\u8BCD\u4E09\u5904\u53EF\u6539\u70B9\u5E76\u4E8C\u7A3F\u4FEE\u8BA2",
      prerequisites: []
    },
    {
      id: "ext-trip-risk",
      name: "\u7814\u5B66\u884C\u7A0B\u98CE\u9669\u8BC4\u4F30\u8868",
      archetypes: ["study-trip", "life-planning"],
      moduleId: "plan",
      gradeBand: [6, 12],
      reason: "\u6D3B\u52A8\u7B56\u5212\u4E2D\u7684\u98CE\u9669\u7BA1\u7406\uFF0C\u8BFE\u6807\u65E0\u4E13\u9879\u6761\u76EE",
      taskSnippet: "\u5217\u51FA\u4EA4\u901A/\u5929\u6C14/\u996E\u98DF\u4E09\u7C7B\u98CE\u9669\u53CA\u5BF9\u5E94\u9884\u6848\uFF0C\u8D1F\u8D23\u4EBA\u7B7E\u5B57\u786E\u8BA4",
      prerequisites: []
    },
    {
      id: "ext-heritage-fieldnotes",
      name: "\u9057\u5740\u535A\u7269\u9986\u7530\u91CE\u89C2\u5BDF\u8BB0\u5F55\u6CD5",
      archetypes: ["study-trip"],
      moduleId: "heritage",
      gradeBand: [6, 12],
      reason: "\u7814\u5B66\u9700\u7ED3\u6784\u5316\u8BB0\u5F55\u6587\u7269\u53F2\u8FF9\u89C2\u5BDF\uFF0C\u8BFE\u6807\u5199\u4F5C\u8F83\u5C11\u4E13\u9879\u8BAD\u7EC3",
      taskSnippet: "\u6309\u65F6\u95F4-\u5730\u70B9-\u89C2\u5BDF\u5BF9\u8C61-\u53F2\u6599\u7EBF\u7D22\u56DB\u680F\u8BB0\u5F55\u81F3\u5C11 3 \u5904\u53F2\u8FF9\uFF0C\u9644\u7B80\u56FE\u6216\u7167\u7247\u7F16\u53F7",
      prerequisites: []
    },
    {
      id: "ext-regional-geo-profile",
      name: "\u76EE\u7684\u5730\u81EA\u7136\u4EBA\u6587\u6982\u51B5\u8C03\u7814\u6846\u67B6",
      archetypes: ["study-trip"],
      moduleId: "destination",
      gradeBand: [6, 12],
      reason: "\u7814\u5B66\u8DEF\u7EBF\u8BBE\u8BA1\u9700\u6574\u5408\u533A\u57DF\u5730\u7406\u4E0E\u4EBA\u6587\u80CC\u666F\uFF0C\u8BFE\u672C\u5206\u6563\u8BB2\u6388",
      taskSnippet: "\u7528\u4E00\u9875\u8868\u6982\u62EC\u76EE\u7684\u5730\u5730\u5F62\u6C14\u5019\u3001\u4EA4\u901A\u533A\u4F4D\u3001\u4EE3\u8868\u6027\u53F2\u8FF9\u4E0E\u6587\u5316\u9057\u4EA7\u5404 2\u20133 \u6761",
      prerequisites: []
    },
    {
      id: "ext-break-even",
      name: "\u4E49\u5356\u76C8\u4E8F\u5E73\u8861\u6D4B\u7B97",
      archetypes: ["business-economics"],
      moduleId: "cost",
      gradeBand: [6, 12],
      reason: "\u7B80\u6613\u5546\u4E1A\u6D4B\u7B97\u6A21\u578B\uFF0C\u8BFE\u672C\u901A\u5E38\u4E0D\u5355\u72EC\u8BB2\u6388",
      taskSnippet: "\u4F30\u7B97\u56FA\u5B9A\u6210\u672C\u4E0E\u5355\u4EF7\uFF0C\u8BA1\u7B97\u81F3\u5C11\u5356\u51FA\u591A\u5C11\u4EF6\u624D\u80FD\u56DE\u672C",
      prerequisites: ["\u767E\u5206\u6BD4", "\u7EDF\u8BA1"]
    },
    {
      id: "ext-screen-time",
      name: "\u5C4F\u5E55\u65F6\u95F4\u4E0E\u7528\u773C\u8DDD\u79BB\u8BB0\u5F55\u6CD5",
      archetypes: ["health-life"],
      moduleId: "status",
      gradeBand: [4, 12],
      reason: "\u8FD1\u89C6\u9632\u63A7\u9700\u53EF\u64CD\u4F5C\u7684\u81EA\u6211\u76D1\u6D4B\u65B9\u6CD5",
      taskSnippet: "\u8FDE\u7EED 7 \u5929\u8BB0\u5F55\u6BCF\u65E5\u5C4F\u5E55\u65F6\u957F\u4E0E\u9605\u8BFB\u8DDD\u79BB\uFF0C\u5236\u8868\u5BF9\u6BD4\u57FA\u7EBF",
      prerequisites: []
    },
    {
      id: "ext-rose-care",
      name: "\u6708\u5B63\u683D\u57F9\u4E0E\u517B\u62A4\u8981\u70B9",
      archetypes: ["planting-cultivation"],
      moduleId: "cultivate",
      gradeBand: [4, 9],
      reason: "\u6708\u5B63\u6266\u63D2\u3001\u6D47\u6C34\u3001\u4FEE\u526A\u3001\u75C5\u866B\u5BB3\u9632\u6CBB\u7B49\u56ED\u827A\u64CD\u4F5C\uFF0C\u8BFE\u672C\u8F83\u5C11\u5C55\u5F00",
      taskSnippet: "\u8BB0\u5F55\u6708\u5B63\u683D\u690D\u6B65\u9AA4\uFF1A\u9009\u82D7\u2192\u6316\u7A74\u2192\u57FA\u80A5\u2192\u5B9A\u690D\u2192\u6D47\u900F\u6C34\uFF1B\u6BCF\u5468\u8BB0\u5F55\u6D47\u6C34\u6B21\u6570\u4E0E\u682A\u9AD8",
      prerequisites: ["\u690D\u7269\u7684\u4E00\u751F\uFF08\u79CD\u5B50\u5230\u679C\u5B9E\uFF09", "\u7EFF\u8272\u690D\u7269\u6574\u4F53\u7ED3\u6784"]
    },
    {
      id: "ext-soil-ph",
      name: "\u683D\u57F9\u571F\u58E4\u4E0E\u6392\u6C34\u68C0\u6D4B",
      archetypes: ["planting-cultivation"],
      moduleId: "cultivate",
      gradeBand: [5, 9],
      reason: "\u571F\u58E4\u758F\u677E\u5EA6\u3001pH\u3001\u6392\u6C34\u6027\u5F71\u54CD\u683D\u57F9\u6210\u6D3B\uFF0C\u52B3\u52A8\u5B9E\u8DF5\u9700\u7B80\u6613\u68C0\u6D4B\u65B9\u6CD5",
      taskSnippet: "\u7528\u7B80\u6613\u65B9\u6CD5\u68C0\u6D4B\u79CD\u690D\u533A\u571F\u58E4\uFF1A\u8BB0\u5F55\u677E\u571F\u6DF1\u5EA6\u3001\u79EF\u6C34\u60C5\u51B5\u3001\u65E5\u7167\u65F6\u957F\u54041\u6B21",
      prerequisites: ["\u690D\u7269\u7684\u5149\u5408\u4F5C\u7528\u4E0E\u547C\u5438\uFF08\u5165\u95E8\uFF09"]
    },
    {
      id: "ext-plant-log",
      name: "\u79CD\u690D\u89C2\u5BDF\u65E5\u5FD7\u6A21\u677F",
      archetypes: ["planting-cultivation", "labor-practice"],
      moduleId: "record",
      gradeBand: [3, 9],
      reason: "\u52B3\u52A8\u5B9E\u8DF5\u4E2D\u7684\u8FC7\u7A0B\u8BB0\u5F55\u89C4\u8303\uFF0C\u9700\u8BFE\u5916\u6A21\u677F\u652F\u6301",
      taskSnippet: "\u6309\u65E5\u671F\u8BB0\u5F55\u682A\u9AD8\u3001\u53F6\u7247\u6570\u3001\u6D47\u6C34\u6B21\u6570\uFF0C\u9644\u7167\u7247\u6216\u7B80\u7B14\u753B",
      prerequisites: []
    },
    {
      id: "ext-storyboard",
      name: "\u77ED\u89C6\u9891\u5206\u955C\u811A\u672C\u89C4\u8303",
      archetypes: ["creative-media"],
      moduleId: "design",
      gradeBand: [6, 12],
      reason: "\u89C6\u542C\u4F5C\u54C1\u524D\u671F\u8BBE\u8BA1\u65B9\u6CD5\uFF0C\u4FE1\u606F\u6280\u672F\u8BFE\u6807\u8F83\u5C11\u6DF1\u5165",
      taskSnippet: "\u7528\u8868\u683C\u5217\u51FA\u955C\u5934\u53F7\u3001\u666F\u522B\u3001\u753B\u9762\u3001\u53F0\u8BCD/\u5B57\u5E55\u3001\u65F6\u957F\u5171 8\u201312 \u955C",
      prerequisites: []
    },
    {
      id: "ext-exhibit-floorplan",
      name: "\u5C55\u9648\u5E73\u9762\u5E03\u5C40\u4E0E\u53C2\u89C2\u52A8\u7EBF\u8BBE\u8BA1",
      archetypes: ["exhibition-redesign"],
      moduleId: "design",
      gradeBand: [6, 12],
      reason: "\u573A\u9986\u6539\u9020\u987B\u89C4\u5212\u52A8\u7EBF\u4E0E\u5C55\u677F\u70B9\u4F4D\uFF0C\u8BFE\u6807\u8F83\u5C11\u7CFB\u7EDF\u8BB2\u6388\u5C55\u9648\u8BBE\u8BA1\u65B9\u6CD5",
      taskSnippet: "\u7528A3\u7EB8\u7ED8\u5236\u5E73\u9762\u56FE\uFF1A\u5165\u53E3\u21923\u4E2A\u5C55\u533A\u2192\u51FA\u53E3\u52A8\u7EBF\uFF0C\u6807\u6CE8\u5404\u5C55\u677F\u5C3A\u5BF8\u4E0E\u4E92\u52A8\u70B9\u4F4D\u7F6E",
      prerequisites: ["\u8BF4\u660E\u6587\u5199\u4F5C"]
    },
    {
      id: "ext-airspace-mgmt",
      name: "\u4F4E\u7A7A\u7A7A\u57DF\u5206\u7C7B\u4E0E\u7BA1\u7406\u8981\u70B9",
      archetypes: ["industry-innovation"],
      moduleId: "background",
      gradeBand: [8, 12],
      reason: "\u7A7A\u57DF\u5212\u8BBE\u3001\u98DE\u884C\u5BA1\u6279\u4E0E\u7981\u98DE\u533A\u662F\u4F4E\u7A7A\u7ECF\u6D4E\u843D\u5730\u524D\u63D0\uFF0C\u8BFE\u6807\u65E0\u4E13\u9879\u6761\u76EE",
      taskSnippet: "\u6574\u7406\u7BA1\u5236\u7A7A\u57DF/\u76D1\u89C6\u7A7A\u57DF/\u62A5\u544A\u7A7A\u57DF\u4E09\u7C7B\u5B9A\u4E49\uFF0C\u6807\u6CE8\u672C\u57301\u5904\u7981\u98DE\u533A\u53CA\u7533\u8BF7\u6D41\u7A0B",
      prerequisites: ["\u4EA4\u901A\u8FD0\u8F93\u5E03\u5C40", "\u4E2D\u56FD\u7684\u7ECF\u6D4E\u53D1\u5C55"]
    },
    {
      id: "ext-lowalt-safety",
      name: "\u65E0\u4EBA\u673A\u98DE\u884C\u5B89\u5168\u64CD\u4F5C\u89C4\u8303",
      archetypes: ["industry-innovation"],
      moduleId: "tech",
      gradeBand: [7, 12],
      reason: "\u573A\u666F\u8C03\u7814\u540E\u987B\u7406\u89E3\u7981\u98DE\u3001\u9650\u9AD8\u3001\u76EE\u89C6\u98DE\u884C\u7B49\u5B89\u5168\u7EA2\u7EBF\uFF0C\u8BFE\u672C\u8F83\u5C11\u7CFB\u7EDF\u8BB2\u6388",
      taskSnippet: "\u5236\u5B9A\u98DE\u884C\u524D\u68C0\u67E5\u8868\uFF1A\u5B9E\u540D\u767B\u8BB0\u3001\u9650\u9AD8120m\u3001\u8FDC\u79BB\u4EBA\u7FA4\u226530m\u3001\u7981\u98DE\u533A\u6838\u67E5",
      prerequisites: ["\u629B\u4F53\u8FD0\u52A8", "\u725B\u987F\u8FD0\u52A8\u5B9A\u5F8B"]
    },
    {
      id: "ext-drone-scenarios",
      name: "\u4F4E\u7A7A\u7ECF\u6D4E\u5178\u578B\u5E94\u7528\u573A\u666F\u56FE\u8C31",
      archetypes: ["industry-innovation"],
      moduleId: "scenarios",
      gradeBand: [7, 12],
      reason: "\u914D\u9001/\u5E94\u6025/\u690D\u4FDD/\u5DE1\u68C0/\u51FA\u884C\u7B49\u573A\u666F\u5206\u7C7B\u662F\u521B\u65B0\u9009\u9898\u57FA\u7840\uFF0C\u8BFE\u6807\u5916\u884C\u4E1A\u77E5\u8BC6",
      taskSnippet: "\u7ED8\u5236\u573A\u666F\u77E9\u9635\uFF1A\u884C=\u573A\u666F\u7C7B\u578B\uFF0C\u5217=\u76EE\u6807\u7528\u6237/\u75DB\u70B9/\u73B0\u6709\u65B9\u6848\uFF0C\u81F3\u5C11\u586B4\u683C",
      prerequisites: ["\u6570\u636E\u7684\u6536\u96C6"]
    },
    {
      id: "ext-filter-efficiency",
      name: "\u8FC7\u6EE4\u5BF9\u7167\u6D4B\u8BD5\u65B9\u6CD5",
      archetypes: ["environmental-filtration"],
      moduleId: "test",
      gradeBand: [4, 12],
      reason: "\u987B\u7528\u5B89\u5168\u6A21\u578B\u9897\u7C92\u505A A/B/C \u5BF9\u7167\uFF0C\u8BB0\u5F55\u6D41\u901F\u4E0E\u53EF\u89C1\u9897\u7C92\u53D8\u5316\uFF0C\u8BFE\u672C\u8F83\u5C11\u7CFB\u7EDF\u8BB2\u6388\u88C5\u7F6E\u9A8C\u6536\u65B9\u6CD5",
      taskSnippet: "A\u539F\u6C34/B\u4EC5\u7C97\u6EE4/C\u5B8C\u6574\u4E09\u7EA7\u5404\u8FC7\u6EE4300mL\uFF0C\u8BB0\u5F55\u7528\u65F6\u5E76\u8BA1\u7B97\u6D41\u901F\uFF1B\u62A5\u544A\u6CE8\u660E\u300C\u6A21\u578B\u9897\u7C92\u51CF\u5C11\u7387\u2260\u771F\u5B9E\u5FAE\u5851\u6599\u53BB\u9664\u7387\u300D",
      prerequisites: ["\u8FC7\u6EE4", "\u5B9E\u9A8C"]
    },
    {
      id: "ext-microplastic-sim",
      name: "\u5B89\u5168\u6A21\u578B\u9897\u7C92\u9009\u7528",
      archetypes: ["environmental-filtration"],
      moduleId: "prefilter",
      gradeBand: [4, 12],
      reason: "\u8BFE\u5802\u987B\u7528\u5B89\u5168\u66FF\u4EE3\u7269\u6A21\u62DF\u6C34\u4E2D\u9897\u7C92\uFF0C\u7981\u6B62\u5236\u9020\u6216\u6269\u6563\u771F\u5B9E\u5851\u6599\u788E\u5C51",
      taskSnippet: "\u9009\u7528\u80E1\u6912\u7C89/\u8336\u53F6\u788E/\u7EC6\u6C99\u7B49\u5B89\u5168\u9897\u7C92\u914D\u5236\u60AC\u6D4A\u6DB2\uFF0C\u5B9E\u9A8C\u540E\u96C6\u4E2D\u6536\u96C6\u5904\u7406\uFF1B\u7981\u6B62\u526A\u5851\u6599\u888B\u3001\u5851\u6599\u5FAE\u73E0\u6216\u4EAE\u7247",
      prerequisites: ["\u8FC7\u6EE4", "\u5B9E\u9A8C"]
    },
    {
      id: "ext-filter-media",
      name: "\u6EE4\u5C42\u6750\u6599\u4E0E\u5B54\u5F84\u9009\u578B",
      archetypes: ["environmental-filtration"],
      moduleId: "membrane",
      gradeBand: [4, 12],
      reason: "\u987B\u533A\u5206\u7C97\u6EE4/\u6D3B\u6027\u70AD/\u819C\u6EE4\u82AF\u804C\u8D23\uFF0C\u819C\u5B54\u5F84\u51B3\u5B9A\u62E6\u622A\u80FD\u529B\uFF0C\u5DE5\u7A0B\u9009\u578B\u8D85\u51FA\u8BFE\u672C",
      taskSnippet: "\u5236\u4F5C\u6EE4\u5C42\u5BF9\u6BD4\u8868\uFF1A\u5C42\u7EA7\u3001\u6750\u6599\u3001\u5B54\u5F84\u6216\u89C4\u683C\u3001\u4E3B\u8981\u4F5C\u7528\u3001\u66F4\u6362\u5468\u671F\uFF1B\u6807\u51FA\u819C/\u9676\u74F7\u6EE4\u82AF\u4E3A\u6838\u5FC3\u5C42",
      prerequisites: ["\u8FC7\u6EE4", "\u6C89\u6DC0"]
    },
    {
      id: "ext-rubric",
      name: "\u9879\u76EE\u6210\u679C\u8BC4\u4EF7\u91CF\u89C4\uFF08Rubric\uFF09",
      archetypes: ["general-practice"],
      moduleId: "test",
      gradeBand: [4, 12],
      reason: "PBL \u5C55\u793A\u8BC4\u4EF7\u9700\u8981\u53EF\u64CD\u4F5C\u7684\u8BC4\u5206\u6807\u51C6",
      taskSnippet: "\u5236\u5B9A 3 \u7EF4\u5EA6 4 \u6863\u91CF\u89C4\uFF1A\u5B8C\u6210\u5EA6\u3001\u5408\u4F5C\u3001\u5C55\u793A\u8868\u8FBE\uFF0C\u5C0F\u7EC4\u81EA\u8BC4\u4E92\u8BC4",
      prerequisites: []
    },
    {
      id: "ext-wifi-protocol",
      name: "Wi-Fi \u65E0\u7EBF\u7EC4\u7F51\u4E0E\u901A\u4FE1\u534F\u8BAE",
      archetypes: [],
      goalPatterns: ["Wi-?Fi", "\u65E0\u7EBF\u7F51\u7EDC", "\u65E0\u7EBF\u7F51", "\u70ED\u70B9", "\u8DEF\u7531\u5668", "TCP/IP", "HTTP", "MQTT"],
      moduleId: "connectivity",
      gradeBand: [7, 12],
      reason: "\u667A\u80FD\u8BBE\u5907\u8054\u7F51\u9700\u7406\u89E3 Wi-Fi \u63A5\u5165\u3001IP \u5BFB\u5740\u4E0E\u5E38\u89C1\u5E94\u7528\u5C42\u534F\u8BAE\uFF0C\u8BFE\u6807\u8F83\u5C11\u5C55\u5F00\u5DE5\u7A0B\u7EC6\u8282",
      taskSnippet: "\u7ED8\u5236\u8BBE\u5907\u8054\u7F51\u62D3\u6251\uFF1ASSID/\u5BC6\u7801\u914D\u7F6E\u3001IP \u83B7\u53D6\u65B9\u5F0F\u3001\u4E0E\u624B\u673A/\u4E91\u7AEF\u7684\u8BF7\u6C42\u8DEF\u5F84\uFF08HTTP \u6216 MQTT\uFF09",
      prerequisites: ["\u7269\u8054\u7F51", "\u7F51\u7EDC"]
    },
    {
      id: "ext-bluetooth-ble",
      name: "\u84DD\u7259/BLE \u8BBE\u5907\u914D\u5BF9\u4E0E\u901A\u4FE1",
      archetypes: [],
      goalPatterns: ["\u84DD\u7259", "BLE", "Bluetooth", "\u4F4E\u529F\u8017\u84DD\u7259", "\u914D\u5BF9", "GATT"],
      moduleId: "connectivity",
      gradeBand: [7, 12],
      reason: "\u8FD1\u573A\u63A7\u5236\u4E0E\u4F20\u611F\u5E38\u8D70\u84DD\u7259\u94FE\u8DEF\uFF0C\u914D\u5BF9\u3001\u670D\u52A1/\u7279\u5F81\u503C\u8BFB\u5199\u8D85\u51FA\u8BFE\u672C\u5B9E\u9A8C",
      taskSnippet: "\u5217\u51FA\u84DD\u7259\u901A\u4FE1\u6B65\u9AA4\uFF1A\u5E7F\u64AD\u2192\u626B\u63CF\u2192\u914D\u5BF9\u2192\u8BFB\u5199\u7279\u5F81\u503C\uFF1B\u6807\u6CE8\u672C\u9879\u76EE\u4E2D\u7528\u5230\u7684\u670D\u52A1 UUID \u4E0E\u6570\u636E\u683C\u5F0F",
      prerequisites: ["\u7269\u8054\u7F51"]
    },
    {
      id: "ext-voice-module",
      name: "\u8BED\u97F3\u8BC6\u522B\u6A21\u5757\u63A5\u5165\u4E0E\u6307\u4EE4\u6620\u5C04",
      archetypes: [],
      goalPatterns: ["\u8BED\u97F3", "\u8BC6\u522B", "\u5524\u9192", "ASR", "\u58F0\u63A7", "\u9EA6\u514B\u98CE", "\u8BED\u97F3\u63A7\u5236"],
      moduleId: "interaction",
      gradeBand: [7, 12],
      reason: "\u8BED\u97F3\u4EA4\u4E92\u9700\u9EA6\u514B\u98CE\u91C7\u96C6\u3001\u5524\u9192\u8BCD/\u6307\u4EE4\u96C6\u4E0E\u52A8\u4F5C\u6620\u5C04\uFF0C\u6A21\u5757\u9009\u578B\u4E0E\u8C03\u8BD5\u4E3A\u5DE5\u7A0B\u5FC5\u5907",
      taskSnippet: "\u8BBE\u8BA1\u6307\u4EE4\u8868\uFF1A\u5524\u9192\u8BCD + 3 \u6761\u63A7\u5236\u6307\u4EE4 \u2192 \u5BF9\u5E94 GPIO/\u573A\u666F\u52A8\u4F5C\uFF1B\u8BB0\u5F55\u8BEF\u8BC6\u522B\u65F6\u7684\u964D\u7EA7\u7B56\u7565",
      prerequisites: ["\u7B97\u6CD5", "\u7269\u8054\u7F51"]
    },
    {
      id: "ext-led-gpio",
      name: "LED/GPIO \u706F\u63A7\u4E0E PWM \u8C03\u5149",
      archetypes: [],
      goalPatterns: ["LED", "\u706F\u63A7", "\u5F69\u706F", "RGB", "GPIO", "\u5F15\u811A", "PWM", "\u8C03\u5149", "\u6307\u793A\u706F"],
      moduleId: "actuation",
      gradeBand: [6, 12],
      reason: "\u72B6\u6001\u6307\u793A\u4E0E\u6C1B\u56F4\u706F\u6548\u9700 GPIO \u8F93\u51FA\u3001\u9650\u6D41\u7535\u963B\u4E0E PWM \u5360\u7A7A\u6BD4\u63A7\u5236\uFF0C\u52A8\u624B\u8C03\u8BD5\u5FC5\u9700",
      taskSnippet: "\u6807\u6CE8 LED \u63A5\u7EBF\u8DEF\u56FE\uFF08VCC/GND/\u9650\u6D41\u7535\u963B/\u63A7\u5236\u5F15\u811A\uFF09\uFF1B\u7F16\u5199\u5F00/\u5173/\u547C\u5438\u706F\u4E09\u6863\u7A0B\u5E8F\u5E76\u6D4B\u7535\u6D41",
      prerequisites: ["\u7535\u8DEF", "\u7A0B\u5E8F\u8BBE\u8BA1"]
    },
    {
      id: "ext-sensor-fusion",
      name: "\u591A\u4F20\u611F\u5668\u6570\u636E\u91C7\u96C6\u4E0E\u878D\u5408",
      archetypes: [],
      goalPatterns: ["\u4F20\u611F\u5668", "\u6E29\u6E7F\u5EA6", "\u5149\u7167", "\u7EA2\u5916", "\u8D85\u58F0", "\u9640\u87BA\u4EEA", "\u52A0\u901F\u5EA6", "\u6570\u636E\u91C7\u96C6"],
      moduleId: "sense",
      gradeBand: [7, 12],
      reason: "\u667A\u80FD\u8BBE\u5907\u5E38\u591A\u8DEF\u4F20\u611F\u5E76\u884C\u91C7\u96C6\uFF0C\u91C7\u6837\u9891\u7387\u3001\u6807\u5B9A\u4E0E\u7B80\u5355\u878D\u5408\u8D85\u51FA\u5355\u70B9\u5B9E\u9A8C",
      taskSnippet: "\u5236\u4F5C\u4F20\u611F\u6E05\u5355\u8868\uFF1A\u7C7B\u578B\u3001\u91CF\u7A0B\u3001\u91C7\u6837\u5468\u671F\u3001\u6821\u51C6\u65B9\u6CD5\uFF1B\u7ED8\u5236\u6570\u636E\u6D41\u4ECE\u91C7\u96C6\u5230\u663E\u793A\u7684\u6846\u56FE",
      prerequisites: ["\u4F20\u611F", "\u6570\u636E\u5206\u6790"]
    },
    {
      id: "ext-embedded-debug",
      name: "\u5D4C\u5165\u5F0F\u7A0B\u5E8F\u70E7\u5F55\u4E0E\u8054\u8C03",
      archetypes: [],
      goalPatterns: ["\u5355\u7247\u673A", "Arduino", "\u6811\u8393\u6D3E", "ESP32", "STM32", "\u5D4C\u5165\u5F0F", "\u70E7\u5F55", "\u4E32\u53E3", "\u8C03\u8BD5"],
      moduleId: "control",
      gradeBand: [8, 12],
      reason: "\u539F\u578B\u843D\u5730\u9700\u70E7\u5F55\u3001\u4E32\u53E3\u65E5\u5FD7\u4E0E\u5206\u6A21\u5757\u8054\u8C03\uFF0C\u8BFE\u672C\u5C11\u8986\u76D6\u5B8C\u6574\u8C03\u8BD5\u6D41\u7A0B",
      taskSnippet: "\u8BB0\u5F55\u8054\u8C03\u65E5\u5FD7\uFF1A\u4F9B\u7535\u68C0\u67E5\u2192\u70E7\u5F55\u6210\u529F\u2192\u4E32\u53E3\u8F93\u51FA\u2192\u5206\u6A21\u5757\uFF08\u4F20\u611F/\u901A\u4FE1/\u6267\u884C\uFF09\u9010\u9879\u9A8C\u6536",
      prerequisites: ["\u7A0B\u5E8F\u8BBE\u8BA1", "\u7B97\u6CD5"]
    },
    {
      id: "ext-pv-yield-model",
      name: "\u5149\u4F0F\u53D1\u7535\u91CF\u4F30\u7B97\u6A21\u578B",
      archetypes: [],
      goalPatterns: ["\u5149\u4F0F", "\u592A\u9633\u80FD\u53D1\u7535", "\u5C4B\u9876\u5149\u4F0F", "\u53D1\u7535\u6F5C\u529B", "\u53D1\u7535\u6536\u76CA", "\u78B3\u51CF\u6392"],
      moduleId: "calc",
      gradeBand: [7, 12],
      reason: "\u9762\u79EF\xD7\u8F6C\u6362\u6548\u7387\xD7\u6709\u6548\u65E5\u7167\u65F6\u6570\u7684\u7B80\u5316\u6A21\u578B\uFF0C\u6536\u76CA\u6D4B\u7B97\u5B9E\u8DF5\u5FC5\u9700",
      taskSnippet: "\u5217\u51FA\u5C4B\u9876\u9762\u79EF\u3001\u7EC4\u4EF6\u6548\u7387\u3001\u5E74\u6709\u6548\u65E5\u7167\u65F6\u6570\uFF0C\u8BA1\u7B97\u5E74\u53D1\u7535\u91CF\u5E76\u6CE8\u660E\u5047\u8BBE\u6761\u4EF6",
      prerequisites: ["\u7535\u529F\u7387", "\u4E00\u6B21\u51FD\u6570"]
    },
    {
      id: "ext-carbon-factor",
      name: "\u7535\u529B\u78B3\u6392\u653E\u56E0\u5B50",
      archetypes: [],
      goalPatterns: ["\u5149\u4F0F", "\u78B3\u51CF\u6392", "\u51CF\u6392\u6548\u76CA", "\u53D1\u7535\u6536\u76CA"],
      moduleId: "carbon",
      gradeBand: [7, 12],
      reason: "\u51CF\u6392\u6548\u76CA\u6D4B\u7B97\u9700\u67E5\u9605\u533A\u57DF\u7535\u7F51\u6392\u653E\u56E0\u5B50\uFF0C\u8BFE\u672C\u901A\u5E38\u4E0D\u5C55\u5F00",
      taskSnippet: "\u67E5\u9605\u672C\u5730\u7535\u7F51\u78B3\u6392\u653E\u56E0\u5B50\uFF0C\u8BA1\u7B97\u5E74\u51CF\u6392\u91CF\u5E76\u4E0E\u6821\u56ED\u7528\u7535\u78B3\u8DB3\u8FF9\u5BF9\u6BD4",
      prerequisites: ["\u7EDF\u8BA1", "\u73AF\u5883"]
    },
    {
      id: "ext-payback-period",
      name: "\u6295\u8D44\u56DE\u6536\u671F\u6D4B\u7B97",
      archetypes: [],
      goalPatterns: ["\u5149\u4F0F", "\u53D1\u7535\u6536\u76CA", "\u53D1\u7535\u6F5C\u529B", "\u5C4B\u9876\u5149\u4F0F"],
      moduleId: "calc",
      gradeBand: [8, 12],
      reason: "\u6536\u76CA\u5206\u6790\u4E2D\u7684\u7B80\u6613\u7ECF\u6D4E\u8BC4\u4EF7\u65B9\u6CD5\uFF0C\u8D85\u51FA\u5E38\u89C4\u8BFE\u6807\u6DF1\u5EA6",
      taskSnippet: "\u4F30\u7B97\u88C5\u673A\u6210\u672C\u4E0E\u5E74\u6536\u76CA\uFF0C\u8BA1\u7B97\u9759\u6001\u6295\u8D44\u56DE\u6536\u671F\u5E76\u8BA8\u8BBA\u654F\u611F\u6027",
      prerequisites: ["\u767E\u5206\u6BD4", "\u7EDF\u8BA1"]
    }
  ]
};
function norm(s) {
  return String(s || "").trim();
}
__name(norm, "norm");
__name2(norm, "norm");
function resolveArchetype(goal, projectType = "", _mixedChemistry = false, archetypeId = null) {
  const list = archetypes_default.archetypes || [];
  if (archetypeId) {
    const byId = list.find((a) => a.id === archetypeId);
    if (byId) return byId;
  }
  const g = norm(goal);
  for (const a of list) {
    for (const p of a.matchPatterns || []) {
      try {
        if (new RegExp(p).test(g)) return a;
      } catch (e) {
        if (g.includes(p)) return a;
      }
    }
  }
  if (projectType) {
    return list.find((a) => a.projectType === projectType || a.id === projectType) || null;
  }
  return null;
}
__name(resolveArchetype, "resolveArchetype");
__name2(resolveArchetype, "resolveArchetype");
function formatArchetypeForMatch(archetype, blueprint) {
  if (!archetype) return "";
  const scheme = (blueprint?.schemes || []).find((s) => s.id === blueprint?.recommendedSchemeId) || (blueprint?.schemes || [])[0];
  const phaseModules = (scheme?.phases || []).map((p, i) => {
    const mid = p.subsystemIds?.[0] || "";
    const mod = (archetype.modules || []).find((m) => m.id === mid);
    return `  ${i + 1}. \u6A21\u5757\u3010${mod?.label || mid || p.phase}\u3011\u68C0\u7D22\u8BCD\uFF1A${(p.knowledgeHints || []).join("\u3001")}`;
  }).join("\n");
  const bans = (archetype.banNamePatterns || []).slice(0, 8).join("\u3001");
  const chinese = archetype.chineseAllowPatterns?.length ? `\u8BED\u6587\u4EC5\u5141\u8BB8\uFF1A${archetype.chineseAllowPatterns.join("\u3001")}` : "";
  return `
\u3010\u9879\u76EE\u539F\u578B\uFF1A${archetype.label}\uFF08${archetype.id}\uFF09\u2014 \u786C\u6027\u7EA6\u675F\u3011
- \u4E3B\u8BFE\u6807\u4F53\u7CFB\uFF1A${archetype.primarySystem || "cn"}\uFF08\u4F18\u5148 CN \u8282\u70B9\uFF0CAP/IB \u4EC5\u4F5C\u62D3\u5C55\uFF09
- \u5B66\u6BB5\uFF1A${(archetype.gradeBand || []).join("-")}\uFF0C\u6700\u4F4E grade ${archetype.minGrade || 7}
- \u5B66\u79D1\u53C2\u8003\uFF08\u975E\u786C\u6027\u9650\u5236\uFF0C\u6309\u9898\u76EE\u5EF6\u5C55\u9009\u53D6\uFF09\uFF1A${(archetype.subjects || []).join("\u3001") || "\u4E0D\u9650"}
- \u7981\u6B62 matched \u540D\u79F0\u542B\uFF1A${bans}
${chinese ? `- ${chinese}` : ""}
- \u6BCF\u4E2A\u6A21\u5757\u81F3\u5C11 1 \u4E2A matched\uFF0Creason \u5FC5\u987B\u4EE5\u672C\u539F\u578B\u6A21\u5757\u540D\u5F00\u5934\uFF08\u5982\u300C\u6A21\u5757\uFF1A\u6210\u672C\u6D4B\u7B97\u3002\u300D\uFF09\uFF0C**\u7981\u6B62**\u7528\u79D1\u5B66\u63A2\u7A76\u5957\u8BDD\uFF08\u95EE\u9898\u4E0E\u5047\u8BBE/\u53D8\u91CF\u8BBE\u8BA1\uFF09
- matched \u603B\u6570 ${archetype.minMatched || 5}-${archetype.maxMatched || 12}\uFF0C\u7981\u6B62\u4E3A\u51D1\u5B66\u79D1\u9009\u65E0\u5173\u8282\u70B9
${phaseModules ? `\u84DD\u56FE\u6A21\u5757\u5BF9\u9F50\uFF1A
${phaseModules}` : ""}`;
}
__name(formatArchetypeForMatch, "formatArchetypeForMatch");
__name2(formatArchetypeForMatch, "formatArchetypeForMatch");
function getRegistryEntries(archetypeId, moduleIds = []) {
  return (engineering_registry_default.entries || []).filter(
    (e) => (e.archetypes || []).includes(archetypeId) && (!moduleIds.length || !e.moduleId || moduleIds.includes(e.moduleId))
  );
}
__name(getRegistryEntries, "getRegistryEntries");
__name2(getRegistryEntries, "getRegistryEntries");
function formatRegistryForMatch(archetypeId) {
  const entries = getRegistryEntries(archetypeId);
  if (!entries.length) return "";
  const lines = entries.slice(0, 6).map(
    (e) => `- [${e.moduleId}] ${e.name}\uFF1A${e.reason}`
  ).join("\n");
  return `
\u3010\u63A8\u8350\u8BFE\u6807\u5916\u8865\u5145\uFF08\u4F18\u5148\u4ECE\u4E0B\u5217\u9009\u7528\uFF0C\u987B\u7ED1\u5B9A\u6A21\u5757\uFF09\u3011
${lines}`;
}
__name(formatRegistryForMatch, "formatRegistryForMatch");
__name2(formatRegistryForMatch, "formatRegistryForMatch");
function normalizeGradeDetails(projectSpec) {
  if (!projectSpec) return [];
  if (Array.isArray(projectSpec.gradeDetails) && projectSpec.gradeDetails.length) {
    return projectSpec.gradeDetails.map((g) => parseInt(g, 10)).filter((g) => g >= 1 && g <= 12);
  }
  const single = parseInt(projectSpec.gradeDetail, 10);
  return single >= 1 && single <= 12 ? [single] : [];
}
__name(normalizeGradeDetails, "normalizeGradeDetails");
__name2(normalizeGradeDetails, "normalizeGradeDetails");
function formatGradeConstraint(projectSpec) {
  if (!projectSpec?.gradeLevel || projectSpec.gradeLevel === "any") return "";
  const maps = {
    primary: "\u5C0F\u5B66",
    junior: "\u521D\u4E2D",
    senior: "\u9AD8\u4E2D",
    university: "\u5927\u5B66",
    adult: "\u6210\u4EBA"
  };
  const base = maps[projectSpec.gradeLevel] || projectSpec.gradeLevel;
  const details = normalizeGradeDetails(projectSpec);
  const lock = projectSpec.lockGradeBand !== false ? "\uFF5C\u9501\u5B66\u6BB5" : "";
  if (details.length === 1) return `G${details[0]}${lock}`;
  if (details.length > 1) {
    const sorted = [...details].sort((a, b) => a - b);
    return `G${sorted.join("/")}(${base})${lock}`;
  }
  return `${base}${lock}`;
}
__name(formatGradeConstraint, "formatGradeConstraint");
__name2(formatGradeConstraint, "formatGradeConstraint");
var SUBJECT_ID_ZH = {
  math: "\u6570\u5B66",
  physics: "\u7269\u7406",
  chemistry: "\u5316\u5B66",
  biology: "\u751F\u7269",
  science: "\u79D1\u5B66",
  chinese: "\u8BED\u6587",
  english: "\u82F1\u8BED",
  history: "\u5386\u53F2",
  geography: "\u5730\u7406",
  "info-tech": "\u4FE1\u606F\u6280\u672F",
  art: "\u827A\u672F",
  politics: "\u9053\u6CD5",
  psychology: "\u5FC3\u7406"
};
function formatSubjectConstraint(projectSpec) {
  if (!projectSpec) return "";
  if (Array.isArray(projectSpec.subjects) && projectSpec.subjects.length) {
    const ids = projectSpec.subjects.filter((id) => id && id !== "cross");
    if (ids.length) return ids.map((id) => SUBJECT_ID_ZH[id] || id).join("+");
  }
  if (projectSpec.subject && projectSpec.subject !== "cross") {
    return SUBJECT_ID_ZH[projectSpec.subject] || projectSpec.subject;
  }
  return "";
}
__name(formatSubjectConstraint, "formatSubjectConstraint");
__name2(formatSubjectConstraint, "formatSubjectConstraint");
var SUBJECT_LABELS = /* @__PURE__ */ new Set([
  "\u8DE8\u5B66\u79D1",
  "\u6570\u5B66",
  "\u7269\u7406",
  "\u5316\u5B66",
  "\u751F\u7269",
  "\u79D1\u5B66",
  "\u8BED\u6587",
  "\u82F1\u8BED",
  "\u5386\u53F2",
  "\u5730\u7406",
  "\u4FE1\u606F\u6280\u672F",
  "\u827A\u672F",
  "\u9053\u6CD5",
  "\u5FC3\u7406"
]);
function stripStructuredGoal(goal) {
  const g = String(goal || "").trim();
  const tagged = g.match(/【任务】\s*([^\n]+)/);
  if (tagged) return tagged[1].trim();
  if (g.includes("\uFF5C")) {
    const parts = g.split("\uFF5C").map((s) => s.trim()).filter(Boolean);
    const taskParts = parts.filter((p) => !/^(产出|场景|周期|约束):/.test(p));
    while (taskParts.length && (/^(小学|初中|高中|大学|成人)/.test(taskParts[0]) || SUBJECT_LABELS.has(taskParts[0]) || /年级/.test(taskParts[0]))) {
      taskParts.shift();
    }
    if (taskParts.length) return taskParts.join("\uFF5C");
  }
  return g.replace(/【[^】]+】[^\n]*/g, "").trim() || g;
}
__name(stripStructuredGoal, "stripStructuredGoal");
__name2(stripStructuredGoal, "stripStructuredGoal");
function extractDeliverableFromGoal(goal) {
  const m = String(goal || "").match(/(?:【产出】|产出:)\s*([^\n｜]+)/);
  return m ? m[1].trim() : "";
}
__name(extractDeliverableFromGoal, "extractDeliverableFromGoal");
__name2(extractDeliverableFromGoal, "extractDeliverableFromGoal");
function compactBlueprintPhases(blueprint, maxPhases = 5) {
  if (!blueprint) return "";
  const scheme = (blueprint.schemes || []).find((s) => s.id === blueprint.recommendedSchemeId) || (blueprint.schemes || [])[0];
  if (!scheme?.phases?.length) return "";
  return scheme.phases.slice(0, maxPhases).map((p, i) => {
    const hints = (p.knowledgeHints || []).slice(0, 4).join("\u3001");
    return `${i + 1}.${p.phase || "\u9636\u6BB5"}${hints ? `(${hints})` : ""}`;
  }).join(" ");
}
__name(compactBlueprintPhases, "compactBlueprintPhases");
__name2(compactBlueprintPhases, "compactBlueprintPhases");
function compactBlueprintHeader(blueprint) {
  if (!blueprint) return "";
  const parts = [];
  if (blueprint.projectSummary) parts.push(blueprint.projectSummary);
  if (blueprint.deliverable) parts.push(`\u4EA4\u4ED8:${blueprint.deliverable}`);
  const phases = compactBlueprintPhases(blueprint);
  if (phases) parts.push(phases);
  return parts.join("\uFF5C");
}
__name(compactBlueprintHeader, "compactBlueprintHeader");
__name2(compactBlueprintHeader, "compactBlueprintHeader");
function buildCompactUserContext({
  goal = "",
  projectSpec = null,
  projectBlueprint = null,
  deliverable = "",
  includeBlueprint = true
} = {}) {
  const task = stripStructuredGoal(goal);
  const deliv = deliverable || projectBlueprint?.deliverable || extractDeliverableFromGoal(goal) || "";
  const grade = formatGradeConstraint(projectSpec);
  const subject = formatSubjectConstraint(projectSpec);
  const lines = [`\u76EE\u6807:${task}`];
  if (deliv) lines.push(`\u4EA4\u4ED8:${deliv}`);
  if (grade) lines.push(`\u5B66\u6BB5:${grade}`);
  if (subject) lines.push(`\u5B66\u79D1:${subject}`);
  if (includeBlueprint && projectBlueprint) {
    const bp = compactBlueprintHeader(projectBlueprint);
    if (bp) lines.push(`\u84DD\u56FE:${bp}`);
  }
  return lines.join("\n");
}
__name(buildCompactUserContext, "buildCompactUserContext");
__name2(buildCompactUserContext, "buildCompactUserContext");
var PLACE_LEX = [
  { keys: /英国|英格兰|英伦|伦敦|剑桥|牛津|大不列颠/, id: "uk", label: "\u82F1\u56FD", terms: ["\u82F1\u56FD", "\u82F1\u683C\u5170", "\u5927\u4E0D\u5217\u98A0", "\u82F1\u4F26", "\u897F\u6B27", "\u6B27\u6D32"], subjects: ["geography", "history", "english"], geoTerms: ["\u56FD\u5BB6", "\u5730\u5F62", "\u6C14\u5019", "\u4EBA\u6587\u5730\u7406", "\u7EAC\u5EA6", "\u6D77\u9646", "\u4E16\u754C\u5730\u5F62", "\u81EA\u7136\u73AF\u5883"] },
  { keys: /法国|法兰西|巴黎|卢浮宫/, id: "fr", label: "\u6CD5\u56FD", terms: ["\u6CD5\u56FD", "\u6CD5\u5170\u897F", "\u897F\u6B27", "\u6B27\u6D32"], subjects: ["geography", "history"], geoTerms: ["\u56FD\u5BB6", "\u5730\u5F62", "\u6C14\u5019", "\u4EBA\u6587\u5730\u7406"] },
  { keys: /美国|北美|纽约|华盛顿|波士顿/, id: "us", label: "\u7F8E\u56FD", terms: ["\u7F8E\u56FD", "\u5317\u7F8E", "\u7F8E\u6D32", "\u7F8E\u5229\u575A"], subjects: ["geography", "history"], geoTerms: ["\u56FD\u5BB6", "\u5730\u5F62", "\u6C14\u5019", "\u4EBA\u6587\u5730\u7406"] },
  { keys: /日本|东京|京都|大阪/, id: "jp", label: "\u65E5\u672C", terms: ["\u65E5\u672C", "\u4E1C\u4E9A", "\u5C9B\u56FD", "\u548C\u670D"], subjects: ["geography", "history"], geoTerms: ["\u56FD\u5BB6", "\u5730\u5F62", "\u6C14\u5019", "\u677F\u5757", "\u5B63\u98CE"] },
  { keys: /德国|柏林|慕尼黑/, id: "de", label: "\u5FB7\u56FD", terms: ["\u5FB7\u56FD", "\u5FB7\u610F\u5FD7", "\u6B27\u6D32"], subjects: ["geography", "history"], geoTerms: ["\u56FD\u5BB6", "\u5730\u5F62", "\u6C14\u5019"] },
  { keys: /意大利|罗马|威尼斯|佛罗伦萨/, id: "it", label: "\u610F\u5927\u5229", terms: ["\u610F\u5927\u5229", "\u7F57\u9A6C", "\u6B27\u6D32", "\u5730\u4E2D\u6D77"], subjects: ["geography", "history"], geoTerms: ["\u56FD\u5BB6", "\u5730\u5F62", "\u6C14\u5019", "\u5730\u4E2D\u6D77"] },
  { keys: /埃及|金字塔|尼罗河|开罗/, id: "eg", label: "\u57C3\u53CA", terms: ["\u57C3\u53CA", "\u5C3C\u7F57\u6CB3", "\u975E\u6D32", "\u91D1\u5B57\u5854", "\u6587\u660E"], subjects: ["geography", "history"], geoTerms: ["\u6CB3\u6D41", "\u5730\u5F62", "\u6C14\u5019", "\u6C99\u6F20"] },
  { keys: /印度|恒河|泰姬陵/, id: "in", label: "\u5370\u5EA6", terms: ["\u5370\u5EA6", "\u5357\u4E9A", "\u6052\u6CB3", "\u6587\u660E"], subjects: ["geography", "history"], geoTerms: ["\u56FD\u5BB6", "\u5730\u5F62", "\u6C14\u5019", "\u5B63\u98CE"] },
  { keys: /澳大利亚|悉尼|袋鼠/, id: "au", label: "\u6FB3\u5927\u5229\u4E9A", terms: ["\u6FB3\u5927\u5229\u4E9A", "\u6FB3\u6D32", "\u5927\u6D0B\u6D32"], subjects: ["geography", "history", "biology"], geoTerms: ["\u56FD\u5BB6", "\u5730\u5F62", "\u6C14\u5019", "\u5927\u9646"] },
  { keys: /俄罗斯|莫斯科|西伯利亚/, id: "ru", label: "\u4FC4\u7F57\u65AF", terms: ["\u4FC4\u7F57\u65AF", "\u897F\u4F2F\u5229\u4E9A", "\u6B27\u6D32", "\u4E9A\u6D32"], subjects: ["geography", "history"], geoTerms: ["\u56FD\u5BB6", "\u5730\u5F62", "\u6C14\u5019", "\u7EAC\u5EA6"] },
  { keys: /中国|华夏|北京|西安|江南|丝绸之路|长安|洛阳|故宫/, id: "cn", label: "\u4E2D\u56FD", terms: ["\u4E2D\u56FD", "\u534E\u590F", "\u4E2D\u539F", "\u6C5F\u5357", "\u9EC4\u6CB3", "\u957F\u6C5F"], subjects: ["geography", "history", "chinese"], geoTerms: ["\u5730\u5F62", "\u6C14\u5019", "\u533A\u57DF", "\u4EBA\u6587", "\u6CB3\u6D41"] },
  { keys: /欧洲|欧盟|地中海|北欧|南欧|西欧|东欧/, id: "europe", label: "\u6B27\u6D32", terms: ["\u6B27\u6D32", "\u897F\u6B27", "\u4E1C\u6B27", "\u5317\u6B27", "\u5357\u6B27", "\u5730\u4E2D\u6D77"], subjects: ["geography", "history"], geoTerms: ["\u5730\u5F62", "\u6C14\u5019", "\u4E16\u754C\u5730\u5F62"] },
  { keys: /非洲|撒哈拉|东非|西非/, id: "africa", label: "\u975E\u6D32", terms: ["\u975E\u6D32", "\u6492\u54C8\u62C9", "\u5C3C\u7F57\u6CB3", "\u521A\u679C"], subjects: ["geography", "history"], geoTerms: ["\u5730\u5F62", "\u6C14\u5019", "\u70ED\u5E26"] },
  { keys: /东南亚|新加坡|泰国|越南|马来西亚/, id: "sea", label: "\u4E1C\u5357\u4E9A", terms: ["\u4E1C\u5357\u4E9A", "\u70ED\u5E26", "\u5B63\u98CE", "\u9A6C\u6765"], subjects: ["geography", "history"], geoTerms: ["\u56FD\u5BB6", "\u5730\u5F62", "\u6C14\u5019"] }
];
var PERIOD_LEX = [
  { keys: /中世纪|中古时期|中古时代|封建时代/, id: "medieval", label: "\u4E2D\u4E16\u7EAA", terms: ["\u4E2D\u4E16\u7EAA", "\u4E2D\u53E4", "\u5C01\u5EFA", "\u9A91\u58EB", "\u5E84\u56ED", "\u6559\u4F1A", "\u9886\u4E3B", "\u6B27\u6D32", "\u5E84\u56ED\u7ECF\u6D4E"], subjects: ["history"] },
  { keys: /文艺复兴/, id: "renaissance", label: "\u6587\u827A\u590D\u5174", terms: ["\u6587\u827A\u590D\u5174", "\u4EBA\u6587\u4E3B\u4E49", "\u5B97\u6559\u6539\u9769", "\u827A\u672F", "\u79D1\u5B66\u9769\u547D"], subjects: ["history", "chinese"] },
  { keys: /古代|先秦|秦汉|唐宋|明清|朝代|王朝|青铜|甲骨文/, id: "ancient", label: "\u53E4\u4EE3", terms: ["\u53E4\u4EE3", "\u671D\u4EE3", "\u738B\u671D", "\u6587\u660E", "\u8003\u53E4", "\u53F2\u6599", "\u5206\u5C01", "\u90E1\u53BF"], subjects: ["history", "chinese"] },
  { keys: /近代|工业革命|殖民|新航路|资本主义/, id: "modern", label: "\u8FD1\u4EE3", terms: ["\u8FD1\u4EE3", "\u5DE5\u4E1A", "\u9769\u547D", "\u6B96\u6C11", "\u8D44\u672C\u4E3B\u4E49", "\u8D44\u4EA7\u9636\u7EA7"], subjects: ["history", "geography"] },
  { keys: /世界大战|二战|一战|冷战/, id: "ww", label: "\u8FD1\u73B0\u4EE3\u6218\u4E89", terms: ["\u6218\u4E89", "\u4E16\u754C", "\u51B7\u6218", "\u53CD\u6CD5\u897F\u65AF"], subjects: ["history"] },
  { keys: /改革开放|新中国|社会主义建设/, id: "cn-contemporary", label: "\u5F53\u4EE3\u4E2D\u56FD", terms: ["\u6539\u9769\u5F00\u653E", "\u65B0\u4E2D\u56FD", "\u793E\u4F1A\u4E3B\u4E49", "\u73B0\u4EE3\u5316"], subjects: ["history", "geography", "chinese"] }
];
var THEME_LEX = [
  { keys: /研学|游学|考察|旅行|路线|目的地|field\s*trip/i, subjects: ["geography", "history", "chinese"], terms: ["\u533A\u57DF", "\u4EBA\u6587", "\u9057\u5740", "\u535A\u7269\u9986", "\u5730\u5F62", "\u6C14\u5019", "\u53F2\u8FF9", "\u4EA4\u901A"] },
  { keys: /博物馆|遗址|文物|古迹|遗产|史迹|考古/, subjects: ["history", "chinese"], terms: ["\u6587\u7269", "\u8003\u53E4", "\u6587\u732E", "\u53F2\u6599", "\u9057\u4EA7", "\u4FDD\u62A4"] },
  { keys: /地形|气候|地貌|区位|地图|自然环境|地理景观/, subjects: ["geography"], terms: ["\u5730\u5F62", "\u6C14\u5019", "\u5730\u56FE", "\u533A\u57DF", "\u7B49\u9AD8\u7EBF", "\u666F\u89C2"] },
  { keys: /莎士比亚|文学|戏剧|诗歌|诗人/, subjects: ["english", "chinese", "history"], terms: ["\u6587\u5B66", "\u620F\u5267", "\u8BD7\u6B4C", "\u4F5C\u5BB6", "\u4F5C\u54C1"] },
  { keys: /经济|贸易|市场|产业|商业/, subjects: ["math", "geography", "history", "chinese"], terms: ["\u7ECF\u6D4E", "\u8D38\u6613", "\u5E02\u573A", "\u4EA7\u4E1A", "\u7EDF\u8BA1"] },
  { keys: /生态|环境|污染|可持续|碳中和/, subjects: ["geography", "biology", "science", "chemistry"], terms: ["\u751F\u6001", "\u73AF\u5883", "\u6C61\u67D3", "\u8D44\u6E90", "\u5FAA\u73AF"] },
  { keys: /物联网|IoT|智能设备|智能家居|智能硬件|嵌入式|单片机|Arduino|树莓派|ESP32|传感|控制板/, subjects: ["info-tech", "physics", "science", "engineering"], terms: ["\u7269\u8054\u7F51", "\u4F20\u611F", "\u63A7\u5236", "\u7A0B\u5E8F\u8BBE\u8BA1", "\u7B97\u6CD5", "\u7F51\u7EDC", "\u667A\u80FD", "\u6A21\u5757", "\u63A5\u53E3"] },
  { keys: /Wi-?Fi|无线网络|蓝牙|BLE|无线通信|MQTT|TCP/i, subjects: ["info-tech", "physics"], terms: ["\u7F51\u7EDC", "\u65E0\u7EBF", "\u901A\u4FE1", "\u534F\u8BAE", "\u7269\u8054\u7F51", "\u6570\u636E\u4F20\u8F93", "\u8FDE\u63A5"] },
  { keys: /语音|识别|声控|麦克风|唤醒词|ASR/i, subjects: ["info-tech", "physics"], terms: ["\u8BED\u97F3", "\u8BC6\u522B", "\u4FE1\u53F7", "\u7B97\u6CD5", "\u4F20\u611F", "\u4EA4\u4E92", "\u63A7\u5236"] },
  { keys: /LED|灯控|RGB|彩灯|GPIO|PWM|调光|指示灯/i, subjects: ["physics", "info-tech", "science"], terms: ["\u7535\u8DEF", "\u7535\u6D41", "\u7535\u538B", "\u63A7\u5236", "\u7A0B\u5E8F\u8BBE\u8BA1", "\u8F93\u51FA", "\u5F15\u811A"] },
  { keys: /光伏|太阳能发电|屋顶.*光伏|发电潜力|发电收益|碳减排|光电|日照|用电数据/, subjects: ["physics", "math", "science"], terms: ["\u5149\u4F0F", "\u592A\u9633\u80FD", "\u5149\u7535", "\u7535\u529F\u7387", "\u80FD\u91CF\u8F6C\u5316", "\u80FD\u91CF\u5B88\u6052", "\u4E00\u6B21\u51FD\u6570", "\u7EDF\u8BA1", "\u767E\u5206\u6BD4", "\u78B3\u6392\u653E", "\u65E5\u7167", "\u53D1\u7535", "\u7535\u8DEF", "\u7535\u6D41", "\u7535\u538B"] }
];
function uniq(arr) {
  return [...new Set((arr || []).filter(Boolean))];
}
__name(uniq, "uniq");
__name2(uniq, "uniq");
function inferTopicKnowledgeAnchors(goal) {
  const g = String(goal || "").trim();
  const recallTerms = /* @__PURE__ */ new Set();
  const subjects = /* @__PURE__ */ new Set();
  const places = [];
  const periods = [];
  const hintParts = [];
  PLACE_LEX.forEach((entry) => {
    if (!entry.keys.test(g)) return;
    places.push(entry.label);
    entry.terms.forEach((t) => recallTerms.add(t));
    entry.subjects.forEach((s) => subjects.add(s));
    if (entry.geoTerms) entry.geoTerms.forEach((t) => recallTerms.add(t));
    hintParts.push(`${entry.label}\u2192${entry.subjects.join("/")}`);
  });
  PERIOD_LEX.forEach((entry) => {
    if (!entry.keys.test(g)) return;
    periods.push(entry.label);
    entry.terms.forEach((t) => recallTerms.add(t));
    entry.subjects.forEach((s) => subjects.add(s));
    hintParts.push(`${entry.label}\u53F2`);
  });
  THEME_LEX.forEach((entry) => {
    if (!entry.keys.test(g)) return;
    (entry.terms || []).forEach((t) => recallTerms.add(t));
    (entry.subjects || []).forEach((s) => subjects.add(s));
  });
  const cjk = g.match(/[\u4e00-\u9fa5]{2,6}/g) || [];
  cjk.forEach((w) => {
    if (!/^(设计|制作|开发|一个|关于|围绕|项目|方案|报告|策划|探究|调查)$/.test(w)) recallTerms.add(w);
  });
  const techHit = /物联网|IoT|智能设备|Wi-?Fi|蓝牙|BLE|语音|LED|GPIO|传感|单片机|Arduino|树莓派|ESP32|嵌入式|无线通信/i.test(g);
  const recallList = uniq([...recallTerms]).slice(0, 40);
  const subjectList = uniq([...subjects]);
  const strong = places.length > 0 || periods.length > 0 || techHit || recallList.length >= 4;
  return {
    recallTerms: recallList,
    subjects: subjectList,
    places,
    periods,
    hints: hintParts.length ? hintParts.join("\uFF1B") : "",
    strong
  };
}
__name(inferTopicKnowledgeAnchors, "inferTopicKnowledgeAnchors");
__name2(inferTopicKnowledgeAnchors, "inferTopicKnowledgeAnchors");
function formatTopicAnchorHint(goal) {
  const a = inferTopicKnowledgeAnchors(goal);
  if (!a.strong) return "";
  const subj = a.subjects.length ? a.subjects.join("\u3001") : "\u6309\u9898\u610F";
  const terms = a.recallTerms.slice(0, 10).join("\u3001");
  const hint = a.hints ? `\uFF5C\u8BED\u4E49\uFF1A${a.hints}` : "";
  return `\u77E5\u8BC6\u53EC\u56DE\uFF1A\u4F18\u5148\u5339\u914D\u4E0E\u300C${terms}\u300D\u76F8\u5173\u7684${subj}\u8BFE\u6807\u8282\u70B9${hint}`;
}
__name(formatTopicAnchorHint, "formatTopicAnchorHint");
__name2(formatTopicAnchorHint, "formatTopicAnchorHint");
function scoreNodeAgainstAnchors(node, anchors, nodeTextFn) {
  if (!anchors?.recallTerms?.length || !node) return 0;
  const text = typeof nodeTextFn === "function" ? nodeTextFn(node) : `${node.name || ""} ${node.definition || node.description || ""}`;
  const name = String(node.name || "");
  let score = 0;
  anchors.recallTerms.forEach((t) => {
    if (!t || t.length < 2) return;
    if (name.includes(t)) score += 8;
    else if (text.includes(t)) score += 4;
  });
  if (anchors.subjects?.includes(node.subject)) {
    const hit = anchors.recallTerms.some((t) => t.length >= 2 && (name.includes(t) || text.includes(t)));
    if (hit) score += 6;
  }
  (anchors.places || []).forEach((place) => {
    if (place.length >= 2 && (name.includes(place) || text.includes(place))) score += 10;
  });
  (anchors.periods || []).forEach((period) => {
    if (period === "\u4E2D\u4E16\u7EAA" && /中世纪|中古/.test(name + text)) score += 14;
    if (period === "\u6587\u827A\u590D\u5174" && /文艺复兴|人文主义/.test(name + text)) score += 14;
    if (period === "\u53E4\u4EE3" && /古代|朝代|文明/.test(name)) score += 10;
    if (period === "\u8FD1\u4EE3" && /近代|工业|资产/.test(name)) score += 10;
  });
  if ((anchors.periods || []).includes("\u4E2D\u4E16\u7EAA") && /工业革命|资产阶级革命|新民主主义|世界大战/.test(name)) score -= 12;
  return score;
}
__name(scoreNodeAgainstAnchors, "scoreNodeAgainstAnchors");
__name2(scoreNodeAgainstAnchors, "scoreNodeAgainstAnchors");
var PBLTopicAnchors = {
  inferTopicKnowledgeAnchors,
  formatTopicAnchorHint,
  scoreNodeAgainstAnchors
};
if (typeof globalThis !== "undefined") {
  globalThis.PBLTopicAnchors = PBLTopicAnchors;
}
var PBL_MAX_MATCHED_COMPLEX = 12;
var PBL_MAX_MATCHED_NORMAL = 18;
function classifyProjectType(goal) {
  const g = String(goal || "");
  if (/购车|买车|选车|消费决策|方案比选|比选|选型|性价比/.test(g) || /对比|比较/.test(g) && /购|买|选|家用|家庭/.test(g) && /新能源|燃油|电动|混动/.test(g) || /哪个更|哪种更|怎么选|如何选择/.test(g) && /车|新能源|电动|手机|电器|产品/.test(g)) {
    return "consumer-decision";
  }
  if (/馆|展厅|展览|展陈/.test(g) && /重塑|改造|整治|升级|策展|布展|翻新|重建|优化|设计/.test(g)) return "exhibition-redesign";
  if (/海报|短视频|微电影|动画|漫画|插画|绘画|策展|广告|品牌|视觉|游戏设计|作曲|音乐创作|手工艺|表演|舞台|摄影|logo|标志设计|文创|周边设计/.test(g)) return "creative-media";
  if (/诗歌|诗集|现代诗|诗词|写诗|小说|剧本|散文|绘本|故事集|演讲|辩论|文学|翻译|双语|新闻稿|采访稿|写一[篇组]|作文|征文|朗诵|文集|杂志|读后感|书评|话剧|文章|诗人|文学家|历史人物|人物研究|名人传记/.test(g)) return "humanities-literary";
  if (/创业|商业计划|营销|市场推广|运营|理财|零花钱|压岁钱|市场调研|义卖|跳蚤市场|店铺|定价|商业模式|盈利|众筹|记账|模拟.*购物/.test(g)) return "business-economics";
  if (/健康|营养|饮食|食谱|减脂|减肥|健身|锻炼|运动会?|近视|视力|护眼|睡眠|作息|心理|情绪|压力|安全|急救|防溺水|防火|卫生|疾病|人体|体重|身高/.test(g)) return "health-life";
  if (/种植|栽培|养花|花卉|蔬菜|种菜|盆栽|园艺|养殖|养蚕|花坛|绿化|阳台种/.test(g)) return "planting-cultivation";
  if (/烹饪|烘焙|美食|菜谱|料理|手工|编织|缝纫|收纳|整理|维修|清洁|打扫|劳动/.test(g)) return "labor-practice";
  if (/研学|游学|研学旅行|研学路线|红色研学|文化研学|文化考察|实地考察|field.?trip|遗址|博物馆|人文史迹|古迹|古村|世界遗产/.test(g)) return "study-trip";
  if (/活动策划|策划.{0,6}(活动|晚会|联欢|运动会|典礼|节|比赛)|联欢会|晚会|文艺汇演|毕业典礼|生日会|出游|旅行|路线规划|时间管理|班级布置|嘉年华|游园/.test(g)) return "life-planning";
  if (/田野|问卷|访谈|社区|民俗|传统文化|非遗|人口|城乡|社会现象|调研报告|居民|乡土|口述史|垃圾分类|垃圾治理|环保.*调查|城市|发展史|对比|比较|典型|区域|案例/.test(g)) return "social-inquiry";
  if (/低空经济|通航产业|新兴产业|产业创新/.test(g) || /探寻|探索|研究|调研/.test(g) && /创新|产业|经济|行业/.test(g)) return "industry-innovation";
  if (/工坊|鲁班|榫卯|古典.*风格|木结构|建筑模型|微缩|传统建筑|斗拱|飞檐/.test(g)) return "maker-workshop";
  if (/光伏|太阳能发电|屋顶.*光伏|发电潜力|发电收益|碳减排/.test(g) && /测算|估算|调查|分析|收益|减排|用电|日照|潜力|效益/.test(g) && !/接线|原型|传感器|水泵|搭建|制作|组装|烧录|GPIO/.test(g)) return "energy-analysis";
  if (/算力中心|数据中心|太空算力|云计算|边缘计算|计算中心|服务器集群|卫星计算|轨道计算/.test(g)) return "engineering";
  if (/火箭|导弹|发射|机器人|电路|机械|硬件|装置|App|应用程序|小程序|网站|系统开发|3D打印|传感|智能|温控|储能|光伏|发电|搭建|制作|工程|发明|物联网|编程实现|循迹|小车|无人机|过滤|净水/.test(g) && /设计|制作|研发|装置|系统|搭建|开发|探究|实验/.test(g)) return "engineering";
  if (/探究|实验|观察|测量|验证|影响因素|变量|检测|成分|对照实验|科学问题|浓度|溶液|溶解|滴定|电导率/.test(g)) return "scientific-inquiry";
  return "general";
}
__name(classifyProjectType, "classifyProjectType");
__name2(classifyProjectType, "classifyProjectType");
var OPEN_SUBJECTS_HINT = "\u6309\u9898\u76EE\u4E0E\u4EA4\u4ED8\u7269\u5EF6\u5C55\u601D\u8003\u540E\u81EA\u7136\u9009\u53D6\uFF0C\u53EF\u8DE8\u5404\u5B66\u79D1\uFF1B\u7981\u4E3A\u51D1\u5B66\u79D1\u5F15\u5165\u65E0\u5173\u8282\u70B9";
var TYPE_PROFILES = {
  "engineering": { label: "\u5DE5\u7A0B\u7814\u53D1/\u5236\u4F5C", moduleWord: "\u5DE5\u7A0B\u5B50\u7CFB\u7EDF\uFF08\u539F\u7406 / \u88C5\u7F6E\u7ED3\u6784 / \u63A7\u5236\u5B9E\u73B0 / \u6D4B\u8BD5\u8FED\u4EE3\uFF09", subjectsHint: OPEN_SUBJECTS_HINT, redlines: "\u8986\u76D6\u539F\u7406\u2192\u88C5\u7F6E\u2192\u5B9E\u9A8C\u2192\u5FC5\u8981\u5B9A\u91CF\uFF1B\u5B9A\u91CF\u8BA1\u7B97\u8282\u70B9\u226420%" },
  "scientific-inquiry": { label: "\u79D1\u5B66\u63A2\u7A76/\u5B9E\u9A8C", moduleWord: "\u63A2\u7A76\u73AF\u8282\uFF08\u95EE\u9898\u5047\u8BBE / \u53D8\u91CF\u8BBE\u8BA1 / \u6570\u636E\u91C7\u96C6 / \u5206\u6790\u7ED3\u8BBA\uFF09", subjectsHint: OPEN_SUBJECTS_HINT, redlines: "\u5FC5\u987B\u542B\u5B9E\u9A8C\u8BBE\u8BA1\u4E0E\u6570\u636E\u5206\u6790\u7C7B\u8282\u70B9\uFF1B\u7406\u8BBA\u4E0E\u5B9E\u9A8C\u5E76\u91CD" },
  "consumer-decision": { label: "\u6D88\u8D39\u51B3\u7B56/\u65B9\u6848\u5BF9\u6BD4", moduleWord: "\u51B3\u7B56\u73AF\u8282\uFF08\u9700\u6C42\u8C03\u7814 / \u6280\u672F\u539F\u7406\u5BF9\u6BD4 / \u6210\u672C\u6D4B\u7B97 / \u51B3\u7B56\u62A5\u544A\uFF09", subjectsHint: OPEN_SUBJECTS_HINT, redlines: "\u4EA4\u4ED8\u7269\u662F\u51B3\u7B56\u62A5\u544A/\u5BF9\u6BD4\u8868\uFF1B\u987B\u542B\u4E0E\u5BF9\u8C61\u76F8\u5173\u7684\u539F\u7406/\u6D4B\u7B97\u8282\u70B9\uFF1B\u7981\u6B62\u5DE5\u4E1A\u7814\u53D1\u8282\u70B9" },
  "social-inquiry": { label: "\u793E\u4F1A\u8C03\u67E5/\u7530\u91CE\u7814\u7A76", moduleWord: "\u8C03\u67E5\u73AF\u8282\uFF08\u9009\u9898\u62BD\u6837 / \u8D44\u6599\u6536\u96C6 / \u6574\u7406\u7EDF\u8BA1 / \u7ED3\u8BBA\u62A5\u544A\uFF09", subjectsHint: OPEN_SUBJECTS_HINT, redlines: "\u6838\u5FC3\u662F\u8C03\u67E5\u65B9\u6CD5\u3001\u6570\u636E\u7EDF\u8BA1\u4E0E\u62A5\u544A\u5199\u4F5C\uFF1B\u8282\u70B9\u987B\u670D\u52A1\u4EA4\u4ED8\u7269" },
  "humanities-literary": { label: "\u4EBA\u6587/\u6587\u5B66/\u8BED\u8A00", moduleWord: "\u521B\u4F5C\u73AF\u8282\uFF08\u7ACB\u610F\u9009\u6750 / \u9605\u8BFB\u79EF\u7D2F / \u7ED3\u6784\u8868\u8FBE / \u4FEE\u6539\u5C55\u793A\uFF09", subjectsHint: OPEN_SUBJECTS_HINT, redlines: "\u56F4\u7ED5\u9605\u8BFB\u3001\u5199\u4F5C\u3001\u8868\u8FBE\u3001\u6587\u5316\u7406\u89E3\uFF1B\u9898\u76EE\u6D89\u53CA\u65F6\u53EF\u81EA\u7136\u5F15\u5165\u76F8\u5173\u5B66\u79D1" },
  "creative-media": { label: "\u521B\u610F\u8BBE\u8BA1/\u5A92\u4F53/\u827A\u672F", moduleWord: "\u521B\u4F5C\u73AF\u8282\uFF08\u521B\u610F\u6784\u601D / \u8BBE\u8BA1\u8349\u6848 / \u5236\u4F5C\u5B9E\u73B0 / \u5C55\u793A\u8BC4\u8BAE\uFF09", subjectsHint: OPEN_SUBJECTS_HINT, redlines: "\u56F4\u7ED5\u521B\u610F\u8868\u8FBE\u4E0E\u5236\u4F5C\uFF1B\u6309\u5B9E\u73B0\u9700\u8981\u81EA\u7136\u5F15\u5165\u76F8\u5173\u5B66\u79D1" },
  "business-economics": { label: "\u5546\u4E1A/\u521B\u4E1A/\u7ECF\u6D4E\u5B9E\u8DF5", moduleWord: "\u8FD0\u8425\u73AF\u8282\uFF08\u9700\u6C42\u8C03\u7814 / \u65B9\u6848\u8BBE\u8BA1 / \u6210\u672C\u5B9A\u4EF7 / \u8FD0\u8425\u590D\u76D8\uFF09", subjectsHint: OPEN_SUBJECTS_HINT, redlines: "\u56F4\u7ED5\u8C03\u7814\u3001\u6D4B\u7B97\u3001\u65B9\u6848\u4E0E\u8868\u8FBE" },
  "study-trip": { label: "\u7814\u5B66\u65C5\u884C/\u4EBA\u6587\u5730\u7406\u8003\u5BDF", moduleWord: "\u7814\u5B66\u73AF\u8282\uFF08\u76EE\u7684\u5730\u8C03\u7814 / \u4EBA\u6587\u53F2\u8FF9 / \u8DEF\u7EBF\u9884\u7B97 / \u7814\u5B66\u62A5\u544A\uFF09", subjectsHint: OPEN_SUBJECTS_HINT, redlines: "\u56F4\u7ED5\u76EE\u7684\u5730\u3001\u53F2\u8FF9\u3001\u8DEF\u7EBF\u9884\u7B97\u4E0E\u7814\u5B66\u62A5\u544A\uFF1B\u9898\u76EE\u63D0\u53CA\u53F2\u5730\u5219\u4F18\u5148\u5339\u914D\uFF0C\u4F46\u4E0D\u9650\u5B66\u79D1" },
  "life-planning": { label: "\u751F\u6D3B\u89C4\u5212/\u6D3B\u52A8\u7B56\u5212", moduleWord: "\u7B56\u5212\u73AF\u8282\uFF08\u9700\u6C42\u76EE\u6807 / \u65B9\u6848\u65E5\u7A0B / \u9884\u7B97\u5206\u5DE5 / \u6267\u884C\u590D\u76D8\uFF09", subjectsHint: OPEN_SUBJECTS_HINT, redlines: "\u56F4\u7ED5\u76EE\u6807\u3001\u65B9\u6848\u3001\u9884\u7B97\u5206\u5DE5\u4E0E\u6267\u884C\u590D\u76D8" },
  "health-life": { label: "\u5065\u5EB7\u751F\u6D3B/\u8FD0\u52A8\u5B89\u5168", moduleWord: "\u5065\u5EB7\u73AF\u8282\uFF08\u73B0\u72B6\u8C03\u67E5 / \u79D1\u5B66\u539F\u7406\u4E0E\u751F\u7406\u673A\u5236 / \u9884\u9632\u5E72\u9884\u539F\u7406 / \u65B9\u6848\u5236\u5B9A / \u5B9E\u8DF5\u8BC4\u4F30\uFF09", subjectsHint: OPEN_SUBJECTS_HINT, redlines: "\u987B\u8986\u76D6\u4E0E\u4E3B\u9898\u76F8\u5173\u7684\u79D1\u5B66\u539F\u7406\u5C42\uFF0C\u4E0D\u80FD\u53EA\u6709\u8C03\u67E5\u7EDF\u8BA1\u4E0E\u884C\u4E3A\u516C\u7EA6" },
  "planting-cultivation": { label: "\u79CD\u690D\u517B\u6B96/\u56ED\u827A\u683D\u57F9", moduleWord: "\u73AF\u8282\uFF08\u690D\u7269\u8BC6\u522B\u5206\u7C7B / \u751F\u957F\u4E0E\u73AF\u5883 / \u683D\u57F9\u5B9E\u64CD / \u89C2\u5BDF\u8BB0\u5F55 / \u79CD\u690D\u65E5\u8BB0\uFF09", subjectsHint: OPEN_SUBJECTS_HINT, redlines: "\u4EA4\u4ED8\u7269\u662F\u79CD\u690D\u89C2\u5BDF\u65E5\u8BB0\uFF1B\u987B\u542B\u751F\u957F\u539F\u7406\u4E0E\u683D\u57F9\u6B65\u9AA4" },
  "labor-practice": { label: "\u52B3\u52A8\u5B9E\u8DF5/\u5236\u4F5C", moduleWord: "\u5B9E\u8DF5\u73AF\u8282\uFF08\u8BA4\u8BC6\u51C6\u5907 / \u64CD\u4F5C\u5B9E\u8DF5 / \u89C2\u5BDF\u8BB0\u5F55 / \u6210\u679C\u5206\u4EAB\uFF09", subjectsHint: OPEN_SUBJECTS_HINT, redlines: "\u56F4\u7ED5\u52A8\u624B\u64CD\u4F5C\u3001\u89C2\u5BDF\u8BB0\u5F55\u4E0E\u6210\u679C\u5206\u4EAB" },
  "maker-workshop": { label: "\u5DE5\u574A/\u6728\u4F5C/\u5EFA\u7B51\u6A21\u578B", moduleWord: "\u5DE5\u5E8F\uFF08\u73B0\u573A\u8C03\u7814 / \u98CE\u683C\u65B9\u6848 / \u6750\u6599BOM / \u642D\u5EFA\u88C5\u9970 / \u9A8C\u6536\u5C55\u793A\uFF09", subjectsHint: OPEN_SUBJECTS_HINT, redlines: "\u4EA4\u4ED8\u7269\u662F\u5B9E\u4F53\u6A21\u578B+\u56FE\u518C+BOM\uFF1B\u987B\u6709\u5C3A\u5BF8\u3001\u5DE5\u5177\u3001\u7167\u7247\u3001\u68C0\u67E5\u8868" },
  "industry-innovation": { label: "\u4EA7\u4E1A\u521B\u65B0/\u65B0\u5174\u7ECF\u6D4E\u63A2\u7A76", moduleWord: "\u73AF\u8282\uFF08\u4EA7\u4E1A\u80CC\u666F\u4E0E\u653F\u7B56 / \u5E94\u7528\u573A\u666F\u8C03\u7814 / \u6280\u672F\u539F\u7406\u652F\u6491 / \u6570\u636E\u53EF\u884C\u6027 / \u521B\u65B0\u65B9\u6848\u62A5\u544A\uFF09", subjectsHint: OPEN_SUBJECTS_HINT, redlines: "\u4EA4\u4ED8\u7269\u662F\u4E3B\u9898\u4EA7\u4E1A\u521B\u65B0\u65B9\u6848/\u8C03\u7814\u62A5\u544A\uFF1B\u7981\u6B62\u4E0E\u4E3B\u9898\u65E0\u5173\u7684\u6A21\u5757" },
  "exhibition-redesign": { label: "\u5C55\u9648\u7A7A\u95F4/\u573A\u9986\u6539\u9020", moduleWord: "\u73AF\u8282\uFF08\u73B0\u72B6\u8BCA\u65AD / \u4E3B\u9898\u7B56\u5212 / \u5C55\u9648\u8BBE\u8BA1 / \u5B9E\u65BD\u6574\u6539 / \u5F00\u653E\u9A8C\u6536\uFF09", subjectsHint: OPEN_SUBJECTS_HINT, redlines: "\u4EA4\u4ED8\u7269\u662F\u573A\u9986\u6539\u9020\u65B9\u6848\u518C+\u5C55\u9648\u8BBE\u8BA1\u56FE\uFF1B\u7981\u6B62\u4E0E\u5C55\u9648\u65E0\u5173\u7684\u8282\u70B9" },
  "energy-analysis": { label: "\u80FD\u6E90/\u73AF\u5883\u6570\u636E\u6D4B\u7B97", moduleWord: "\u73AF\u8282\uFF08\u8D44\u6E90\u8C03\u67E5 / \u6570\u636E\u91C7\u96C6 / \u6A21\u578B\u6D4B\u7B97 / \u6548\u76CA\u5206\u6790 / \u65B9\u6848\u8BBA\u8BC1\uFF09", subjectsHint: "\u7269\u7406\u3001\u6570\u5B66\u3001\u5730\u7406/\u79D1\u5B66\u3001\u8BED\u6587\uFF08\u62A5\u544A\uFF09\uFF1B\u7981\u6B62\u751F\u7269\u5B66", redlines: "\u4EA4\u4ED8\u7269\u662F\u6D4B\u7B97\u8868+\u5206\u6790\u56FE\u8868+\u8BBA\u8BC1\u62A5\u544A\uFF1B\u7981\u6B62\u63A5\u7EBF/\u539F\u578B/\u786C\u4EF6\u5DE5\u7A0B\u6B65\u9AA4\uFF1B\u7981\u6B62\u7EC6\u80DE/\u7EC6\u80DE\u819C/\u7EC6\u80DE\u547C\u5438/\u5149\u5408\u4F5C\u7528\u7B49\u751F\u7269\u5B66\u8282\u70B9\uFF08\u80FD\u91CF\u6307\u7269\u7406\u7535\u80FD\u975E\u7EC6\u80DE\u4EE3\u8C22\uFF09" },
  "general": { label: "\u7EFC\u5408\u5B9E\u8DF5", moduleWord: "\u9879\u76EE\u6A21\u5757\uFF08\u987B\u6309\u9898\u76EE\u81EA\u5B9A\u4E49\uFF0C\u7981\u6B62\u5957\u7528\u901A\u7528\u6A21\u5757\u540D\uFF09", subjectsHint: OPEN_SUBJECTS_HINT, redlines: "\u6BCF\u4E2A\u8282\u70B9\u90FD\u8981\u670D\u52A1\u4E8E\u9898\u76EE\u4EA4\u4ED8\u7269" }
};
function projectTypeProfile(goal) {
  return TYPE_PROFILES[classifyProjectType(goal)] || TYPE_PROFILES.general;
}
__name(projectTypeProfile, "projectTypeProfile");
__name2(projectTypeProfile, "projectTypeProfile");
function typeGuardrailBlock(goal) {
  const p = projectTypeProfile(goal);
  return `\u7C7B\u578B\uFF1A${p.label}\uFF5C\u6A21\u5757\uFF1A${p.moduleWord}\uFF5C\u5B66\u79D1\uFF1A${p.subjectsHint}\uFF5C\u7EA2\u7EBF\uFF1A${p.redlines}`;
}
__name(typeGuardrailBlock, "typeGuardrailBlock");
__name2(typeGuardrailBlock, "typeGuardrailBlock");
function parseGoalSubject(goal) {
  const g = String(goal || "").trim();
  let subject = g;
  const m = g.match(/^(?:设计|制作|开发|建造|完成|策划|撰写|探究|调查|分析|探寻|探索|研究|调研|重塑|改造|优化|重建|更新|升级|整治|组织|开展|修复|翻新)(?:一个|一款|一份|一组|一次)?\s*(.+)$/);
  if (m) subject = m[1].trim();
  subject = subject.replace(/^(?:关于|围绕|有关)\s*/, "").replace(/[，。；].*$/, "").slice(0, 36);
  return subject || g.slice(0, 36);
}
__name(parseGoalSubject, "parseGoalSubject");
__name2(parseGoalSubject, "parseGoalSubject");
function buildTopicKeywords(goal, subject) {
  const g = String(goal || "");
  const base = [subject];
  for (let i = 0; i < subject.length - 1; i++) {
    const w = subject.slice(i, i + 2);
    if (w.length === 2 && !/[的与及了在]$/.test(w)) base.push(w);
  }
  const extra = g.match(/[\u4e00-\u9fa5]{2,4}/g) || [];
  for (const w of extra.slice(0, 8)) {
    if (!base.includes(w) && !/^(设计|制作|开发|一个|关于|围绕|项目|方案|报告)$/.test(w)) base.push(w);
  }
  const anchors = inferTopicKnowledgeAnchors(g);
  (anchors.recallTerms || []).slice(0, 12).forEach((t) => base.push(t));
  return [...new Set(base)].slice(0, 20);
}
__name(buildTopicKeywords, "buildTopicKeywords");
__name2(buildTopicKeywords, "buildTopicKeywords");
function inferDeliverableHint(goal, subject, kind) {
  const g = String(goal || "");
  if (kind === "exhibition-redesign") return `\u300C${subject}\u300D\u6539\u9020\u65B9\u6848\u518C\uFF08\u73B0\u72B6\u8BCA\u65AD+\u5C55\u9648\u8BBE\u8BA1+\u6574\u6539\u5B9E\u65BD+\u9A8C\u6536\uFF09`;
  if (kind === "industry-innovation") return `\u300C${subject}\u300D\u521B\u65B0\u65B9\u6848\u62A5\u544A\uFF08\u573A\u666F\u8C03\u7814+\u653F\u7B56\u8981\u70B9+\u53EF\u884C\u6027\u8BBA\u8BC1\uFF09`;
  if (kind === "planting-cultivation") return `\u300C${subject}\u300D\u79CD\u690D\u89C2\u5BDF\u65E5\u8BB0\uFF08\u5206\u7C7B\u7B14\u8BB0+\u683D\u57F9\u8BB0\u5F55+\u751F\u957F\u6570\u636E+\u603B\u7ED3\uFF09`;
  if (kind === "study-trip") return `\u300C${subject}\u300D\u7814\u5B66\u65B9\u6848\u518C\uFF08\u533A\u57DF\u5730\u7406\u8C03\u7814+\u4EBA\u6587\u53F2\u8FF9\u8BB0\u5F55+\u8DEF\u7EBF\u9884\u7B97+\u5B89\u5168\u9884\u6848+\u7814\u5B66\u62A5\u544A\uFF09`;
  if (/报告|调查|论文|倡议|方案/.test(g)) return `\u300C${subject}\u300D\u4E13\u9898\u62A5\u544A\uFF08\u542B\u8C03\u7814\u6570\u636E\u4E0E\u53EF\u68C0\u67E5\u7ED3\u8BBA\uFF09`;
  if (/设计|制作|开发|建造/.test(g)) return `\u53EF\u5C55\u793A\u7684\u300C${subject}\u300D\u4F5C\u54C1+\u8FC7\u7A0B\u8BB0\u5F55+\u8BF4\u660E\u6587\u6863`;
  return `\u300C${subject}\u300D\u9879\u76EE\u6210\u679C\u5305\uFF08\u53EF\u5C55\u793A\u4EA4\u4ED8\u7269+\u8FC7\u7A0B\u8BB0\u5F55+\u8BF4\u660E\uFF09`;
}
__name(inferDeliverableHint, "inferDeliverableHint");
__name2(inferDeliverableHint, "inferDeliverableHint");
function extractTopicProfile(goal) {
  const g = String(goal || "").trim();
  const subject = parseGoalSubject(g);
  const kind = classifyProjectType(g);
  const banCommon = ["\u539F\u578B\u9A71\u52A8\u8FED\u4EE3", "MVP", "\u5FEB\u901F\u539F\u578B", "\u9012\u8FDB\u5F0F\u5B9E\u65BD", "\u6D78\u6DA6\u5F0F\u573A\u666F", "\u786C\u4EF6\u51C6\u5907", "\u73AF\u5883\u642D\u5EFA", "\u5DE5\u7A0B\u8BBE\u8BA1\u601D\u7EF4"];
  return {
    rawGoal: g,
    matched: true,
    coreTopic: subject,
    definition: `\u672C\u9879\u76EE\u5FC5\u987B\u56F4\u7ED5\u7528\u6237\u6307\u5B9A\u7684\u300C${subject}\u300D\u5C55\u5F00\uFF0C\u4E0D\u5F97\u66FF\u6362\u4E3A\u5176\u4ED6\u4E3B\u9898\u6216\u5957\u7528\u65E0\u5173\u6A21\u677F`,
    keywords: buildTopicKeywords(g, subject),
    banInSteps: banCommon,
    deliverableHint: inferDeliverableHint(g, subject, kind),
    kind
  };
}
__name(extractTopicProfile, "extractTopicProfile");
__name2(extractTopicProfile, "extractTopicProfile");
function formatTopicAnchorBlock(goal) {
  const t = extractTopicProfile(goal);
  const anchorHint = formatTopicAnchorHint(goal);
  const anchorPart = anchorHint ? `\uFF5C${anchorHint}` : "";
  return `\u951A\u70B9\uFF1A\u300C${t.coreTopic}\u300D\uFF5C\u68C0\u7D22\u8BCD\uFF1A${t.keywords.slice(0, 10).join("\u3001")}\uFF5C\u4EA4\u4ED8\u53C2\u8003\uFF1A${t.deliverableHint}${anchorPart}\uFF5C\u7981\u5957\u6A21\u677F/MVP/\u73AF\u5883\u642D\u5EFA`;
}
__name(formatTopicAnchorBlock, "formatTopicAnchorBlock");
__name2(formatTopicAnchorBlock, "formatTopicAnchorBlock");
function genericDomainsForType(id, goal = "") {
  const g = String(goal || "");
  if (/算力中心|数据中心|太空算力|云计算|边缘计算|计算中心|服务器集群|卫星计算|轨道计算/.test(g)) {
    return [
      { id: "requirements", label: "\u9700\u6C42\u4E0E\u7EA6\u675F\u5B9A\u4E49", keywords: ["\u7B97\u529B", "\u4EFB\u52A1\u8D1F\u8F7D", "\u8F68\u9053\u73AF\u5883", "\u529F\u8017", "\u6563\u70ED", "\u901A\u4FE1\u94FE\u8DEF", "\u8F90\u5C04", "\u9700\u6C42"], subjects: ["computer-science", "engineering", "physics"] },
      { id: "architecture", label: "\u7CFB\u7EDF\u67B6\u6784\u8BBE\u8BA1", keywords: ["\u7CFB\u7EDF\u67B6\u6784", "\u8BA1\u7B97\u8282\u70B9", "\u7535\u6E90", "\u70ED\u63A7", "\u901A\u4FE1", "\u5197\u4F59", "\u6A21\u5757\u5316", "\u63A5\u53E3"], subjects: ["computer-science", "engineering"] },
      { id: "operations", label: "\u8C03\u5EA6\u4E0E\u8FD0\u884C\u63A7\u5236", keywords: ["\u4EFB\u52A1\u8C03\u5EA6", "\u9065\u6D4B", "\u5BB9\u9519", "\u6545\u969C\u5207\u6362", "\u8D44\u6E90\u5206\u914D", "\u76D1\u63A7", "\u63A7\u5236\u6D41\u7A0B"], subjects: ["computer-science", "engineering"] },
      { id: "verification", label: "\u4EFF\u771F\u6D4B\u8BD5\u4E0E\u8FED\u4EE3", keywords: ["\u4EFF\u771F", "\u6307\u6807", "\u5EF6\u8FDF", "\u5E26\u5BBD", "\u80FD\u8017", "\u70ED\u5E73\u8861", "\u53EF\u9760\u6027", "\u6D4B\u8BD5"], subjects: ["computer-science", "engineering", "physics"] }
    ];
  }
  const map = {
    "scientific-inquiry": [
      { id: "question", label: "\u95EE\u9898\u4E0E\u5047\u8BBE", keywords: ["\u95EE\u9898", "\u5047\u8BBE", "\u731C\u60F3", "\u73B0\u8C61", "\u539F\u7406"], subjects: ["science", "physics", "chemistry", "biology"] },
      { id: "design", label: "\u53D8\u91CF\u4E0E\u5B9E\u9A8C\u8BBE\u8BA1", keywords: ["\u53D8\u91CF", "\u5B9E\u9A8C", "\u63A7\u5236\u53D8\u91CF", "\u5BF9\u7167", "\u65B9\u6848", "\u6D4B\u91CF"], subjects: ["physics", "chemistry", "biology", "science"] },
      { id: "data", label: "\u6570\u636E\u91C7\u96C6\u4E0E\u5904\u7406", keywords: ["\u6570\u636E", "\u6D4B\u91CF", "\u8BB0\u5F55", "\u7EDF\u8BA1", "\u8BEF\u5DEE", "\u56FE\u8868"], subjects: ["math", "info-tech", "science"] },
      { id: "conclusion", label: "\u5206\u6790\u4E0E\u7ED3\u8BBA", keywords: ["\u5206\u6790", "\u7ED3\u8BBA", "\u89E3\u91CA", "\u89C4\u5F8B", "\u62A5\u544A"], subjects: ["science", "math", "chinese"] }
    ],
    "social-inquiry": [
      { id: "topic", label: "\u9009\u9898\u4E0E\u8C03\u67E5\u8BBE\u8BA1", keywords: ["\u9009\u9898", "\u8C03\u67E5", "\u95EE\u5377", "\u8BBF\u8C08", "\u62BD\u6837", "\u6837\u672C", "\u7EF4\u5EA6", "\u6307\u6807"], subjects: ["chinese", "math", "politics", "psychology"] },
      { id: "collect", label: "\u8D44\u6599\u4E0E\u6570\u636E\u6536\u96C6", keywords: ["\u8D44\u6599", "\u6570\u636E", "\u6536\u96C6", "\u8BB0\u5F55", "\u6587\u732E", "\u5B9E\u5730", "\u53F2\u6599", "\u6848\u4F8B"], subjects: ["geography", "history", "chinese", "politics", "psychology"] },
      { id: "analyze", label: "\u6574\u7406\u4E0E\u7EDF\u8BA1\u5206\u6790", keywords: ["\u7EDF\u8BA1", "\u6574\u7406", "\u56FE\u8868", "\u5206\u6790", "\u767E\u5206\u6BD4", "\u5E73\u5747\u6570", "\u5BF9\u6BD4"], subjects: ["math", "psychology"] },
      { id: "report", label: "\u7ED3\u8BBA\u4E0E\u62A5\u544A", keywords: ["\u7ED3\u8BBA", "\u62A5\u544A", "\u5EFA\u8BAE", "\u8BBA\u8BC1", "\u5199\u4F5C", "\u8BF4\u660E"], subjects: ["chinese", "politics"] }
    ],
    "humanities-literary": [
      { id: "theme", label: "\u7ACB\u610F\u4E0E\u9009\u6750", keywords: ["\u7ACB\u610F", "\u4E3B\u9898", "\u9009\u6750", "\u6784\u601D", "\u89C2\u70B9"], subjects: ["chinese", "english"] },
      { id: "read", label: "\u9605\u8BFB\u4E0E\u7D20\u6750\u79EF\u7D2F", keywords: ["\u9605\u8BFB", "\u7D20\u6750", "\u6587\u672C", "\u540D\u8457", "\u79EF\u7D2F", "\u9274\u8D4F"], subjects: ["chinese", "english", "history"] },
      { id: "express", label: "\u7ED3\u6784\u4E0E\u8868\u8FBE", keywords: ["\u7ED3\u6784", "\u8868\u8FBE", "\u4FEE\u8F9E", "\u8BED\u8A00", "\u5199\u4F5C", "\u53D9\u8FF0"], subjects: ["chinese", "english"] },
      { id: "revise", label: "\u4FEE\u6539\u4E0E\u5C55\u793A", keywords: ["\u4FEE\u6539", "\u8BC4\u8BAE", "\u6717\u8BF5", "\u5C55\u793A", "\u6F14\u8BB2", "\u53D1\u8868"], subjects: ["chinese"] }
    ],
    "creative-media": [
      { id: "idea", label: "\u521B\u610F\u6784\u601D", keywords: ["\u521B\u610F", "\u6784\u601D", "\u4E3B\u9898", "\u7075\u611F", "\u53D7\u4F17"], subjects: ["chinese", "info-tech"] },
      { id: "design", label: "\u8BBE\u8BA1\u4E0E\u8349\u6848", keywords: ["\u8BBE\u8BA1", "\u8349\u56FE", "\u5206\u955C", "\u6392\u7248", "\u8272\u5F69", "\u6784\u56FE"], subjects: ["info-tech", "chinese"] },
      { id: "make", label: "\u5236\u4F5C\u4E0E\u5B9E\u73B0", keywords: ["\u5236\u4F5C", "\u526A\u8F91", "\u7ED8\u5236", "\u7F16\u8F91", "\u5DE5\u5177", "\u6280\u672F"], subjects: ["info-tech"] },
      { id: "show", label: "\u5C55\u793A\u4E0E\u8BC4\u8BAE", keywords: ["\u5C55\u793A", "\u8BC4\u8BAE", "\u53CD\u9988", "\u53D1\u5E03", "\u4F18\u5316"], subjects: ["chinese"] }
    ],
    "business-economics": [
      { id: "research", label: "\u9700\u6C42\u4E0E\u5E02\u573A\u8C03\u7814", keywords: ["\u9700\u6C42", "\u5E02\u573A", "\u8C03\u7814", "\u8C03\u67E5", "\u6570\u636E", "\u7528\u6237"], subjects: ["math", "chinese"] },
      { id: "plan", label: "\u65B9\u6848\u4E0E\u4EA7\u54C1\u8BBE\u8BA1", keywords: ["\u65B9\u6848", "\u4EA7\u54C1", "\u8BBE\u8BA1", "\u7B56\u5212", "\u521B\u610F"], subjects: ["chinese", "info-tech"] },
      { id: "cost", label: "\u6210\u672C\u4E0E\u5B9A\u4EF7\u6D4B\u7B97", keywords: ["\u6210\u672C", "\u5B9A\u4EF7", "\u5229\u6DA6", "\u9884\u7B97", "\u51FD\u6570", "\u767E\u5206\u6BD4", "\u7EDF\u8BA1"], subjects: ["math"] },
      { id: "operate", label: "\u8FD0\u8425\u4E0E\u590D\u76D8", keywords: ["\u8FD0\u8425", "\u63A8\u5E7F", "\u590D\u76D8", "\u53CD\u9988", "\u62A5\u544A"], subjects: ["chinese", "math"] }
    ],
    "study-trip": [
      { id: "destination", label: "\u76EE\u7684\u5730\u8C03\u7814", keywords: ["\u76EE\u7684\u5730", "\u8C03\u7814", "\u533A\u57DF", "\u5730\u56FE", "\u5730\u5F62", "\u6C14\u5019", "\u8D44\u6E90", "\u533A\u4F4D", "\u4EA4\u901A", "\u5730\u7406"], subjects: ["geography", "history"] },
      { id: "heritage", label: "\u4EBA\u6587\u53F2\u8FF9", keywords: ["\u5386\u53F2", "\u6587\u7269", "\u9057\u5740", "\u535A\u7269\u9986", "\u9769\u547D", "\u671D\u4EE3", "\u9057\u4EA7", "\u4EBA\u6587", "\u53E4\u8FF9", "\u6587\u5316"], subjects: ["history", "chinese"] },
      { id: "route", label: "\u8DEF\u7EBF\u9884\u7B97", keywords: ["\u8DEF\u7EBF", "\u65E5\u7A0B", "\u884C\u7A0B", "\u9884\u7B97", "\u8D39\u7528", "\u7EDF\u8BA1", "\u6210\u672C", "\u5206\u5DE5", "\u5B89\u5168"], subjects: ["math", "geography", "chinese"] },
      { id: "report", label: "\u7814\u5B66\u62A5\u544A", keywords: ["\u62A5\u544A", "\u603B\u7ED3", "\u8BB0\u5F55", "\u8BF4\u660E", "\u5C55\u793A", "\u590D\u76D8", "\u89C2\u5BDF", "\u65E5\u8BB0"], subjects: ["chinese", "history", "geography"] }
    ],
    "life-planning": [
      { id: "goal", label: "\u9700\u6C42\u4E0E\u76EE\u6807", keywords: ["\u9700\u6C42", "\u76EE\u6807", "\u8C03\u67E5", "\u95EE\u5377", "\u573A\u666F", "\u4EBA\u6570"], subjects: ["chinese", "math"] },
      { id: "plan", label: "\u65B9\u6848\u4E0E\u65E5\u7A0B", keywords: ["\u65B9\u6848", "\u8BA1\u5212", "\u65E5\u7A0B", "\u5B89\u6392", "\u8DEF\u7EBF", "\u6D41\u7A0B"], subjects: ["chinese", "geography", "math"] },
      { id: "budget", label: "\u9884\u7B97\u4E0E\u5206\u5DE5", keywords: ["\u9884\u7B97", "\u6210\u672C", "\u8D39\u7528", "\u7EDF\u8BA1", "\u51FD\u6570", "\u5206\u5DE5", "\u767E\u5206\u6BD4"], subjects: ["math"] },
      { id: "review", label: "\u6267\u884C\u4E0E\u590D\u76D8", keywords: ["\u6267\u884C", "\u8BB0\u5F55", "\u53CD\u9988", "\u590D\u76D8", "\u603B\u7ED3", "\u62A5\u544A"], subjects: ["chinese"] }
    ],
    "health-life": [
      { id: "status", label: "\u73B0\u72B6\u8C03\u67E5\u4E0E\u6570\u636E", keywords: ["\u73B0\u72B6", "\u8C03\u67E5", "\u95EE\u5377", "\u7EDF\u8BA1", "\u6570\u636E", "\u6D4B\u91CF", "\u8BB0\u5F55", "\u6BD4\u4F8B", "\u56FE\u8868"], subjects: ["math", "biology", "science"] },
      { id: "mechanism", label: "\u79D1\u5B66\u539F\u7406\u4E0E\u751F\u7406\u673A\u5236", keywords: ["\u539F\u7406", "\u673A\u5236", "\u7ED3\u6784", "\u6210\u56E0", "\u51F8\u900F\u955C", "\u6676\u72B6\u4F53", "\u89C6\u7F51\u819C", "\u776B\u72B6\u808C", "\u5149\u5B66", "\u6210\u50CF", "\u6298\u5C04", "\u6D88\u5316", "\u5438\u6536", "\u4EE3\u8C22", "\u5FAA\u73AF", "\u547C\u5438", "\u7EC6\u80DE", "\u795E\u7ECF", "\u808C\u8089", "\u9AA8\u9ABC"], subjects: ["physics", "biology", "chemistry", "science"] },
      { id: "prevention", label: "\u9884\u9632/\u5E72\u9884\u539F\u7406\u4E0E\u65B9\u6CD5", keywords: ["\u9884\u9632", "\u77EB\u6B63", "\u51F9\u900F\u955C", "\u7126\u8DDD", "\u5C48\u5149", "\u8425\u517B\u7D20", "\u81B3\u98DF", "\u8BAD\u7EC3", "\u6062\u590D", "\u4FDD\u62A4", "\u9632\u62A4", "\u5E72\u9884", "\u6CBB\u7597"], subjects: ["biology", "physics", "chemistry", "science"] },
      { id: "plan", label: "\u65B9\u6848\u5236\u5B9A\u4E0E\u5BA3\u4F20", keywords: ["\u8BA1\u5212", "\u65B9\u6848", "\u76EE\u6807", "\u516C\u7EA6", "\u6807\u51C6", "\u5021\u8BAE", "\u5BA3\u4F20", "\u6D77\u62A5", "\u8BF4\u660E\u6587"], subjects: ["chinese", "math", "politics", "psychology"] },
      { id: "assess", label: "\u5B9E\u8DF5\u8BB0\u5F55\u4E0E\u8BC4\u4F30", keywords: ["\u8BB0\u5F55", "\u8BC4\u4F30", "\u5BF9\u6BD4", "\u53CD\u9988", "\u6539\u8FDB", "\u62A5\u544A", "\u6570\u636E\u8DDF\u8E2A"], subjects: ["chinese", "math", "science", "psychology"] }
    ],
    "planting-cultivation": [
      { id: "taxonomy", label: "\u690D\u7269\u8BC6\u522B\u4E0E\u5206\u7C7B", keywords: ["\u690D\u7269", "\u5206\u7C7B", "\u7279\u5F81", "\u7ED3\u6784", "\u5668\u5B98"], subjects: ["science", "biology"] },
      { id: "growth", label: "\u751F\u957F\u4E0E\u73AF\u5883", keywords: ["\u751F\u957F", "\u5149\u5408", "\u547C\u5438", "\u79CD\u5B50", "\u840C\u53D1", "\u73AF\u5883"], subjects: ["science", "biology"] },
      { id: "cultivate", label: "\u683D\u57F9\u5B9E\u64CD", keywords: ["\u79CD\u690D", "\u683D\u57F9", "\u571F\u58E4", "\u6D47\u6C34", "\u65BD\u80A5", "\u517B\u62A4"], subjects: ["science", "biology"] },
      { id: "observe", label: "\u89C2\u5BDF\u8BB0\u5F55", keywords: ["\u89C2\u5BDF", "\u8BB0\u5F55", "\u6D4B\u91CF", "\u6570\u636E", "\u56FE\u8868", "\u53D8\u5316"], subjects: ["science", "math", "biology"] },
      { id: "share", label: "\u79CD\u690D\u65E5\u8BB0", keywords: ["\u65E5\u8BB0", "\u62A5\u544A", "\u603B\u7ED3", "\u5206\u4EAB", "\u8BF4\u660E"], subjects: ["chinese"] }
    ],
    "labor-practice": [
      { id: "prepare", label: "\u8BA4\u8BC6\u4E0E\u51C6\u5907", keywords: ["\u8BA4\u8BC6", "\u51C6\u5907", "\u6750\u6599", "\u5DE5\u5177", "\u539F\u7406", "\u6B65\u9AA4"], subjects: ["science", "biology", "chinese"] },
      { id: "practice", label: "\u64CD\u4F5C\u5B9E\u8DF5", keywords: ["\u64CD\u4F5C", "\u5236\u4F5C", "\u79CD\u690D", "\u517B\u62A4", "\u70F9\u996A", "\u6B65\u9AA4"], subjects: ["science", "biology"] },
      { id: "record", label: "\u89C2\u5BDF\u4E0E\u8BB0\u5F55", keywords: ["\u89C2\u5BDF", "\u8BB0\u5F55", "\u6D4B\u91CF", "\u6570\u636E", "\u53D8\u5316", "\u7EDF\u8BA1"], subjects: ["science", "math", "biology"] },
      { id: "share", label: "\u6210\u679C\u4E0E\u5206\u4EAB", keywords: ["\u6210\u679C", "\u5206\u4EAB", "\u5C55\u793A", "\u603B\u7ED3", "\u62A5\u544A", "\u6539\u8FDB"], subjects: ["chinese"] }
    ],
    "engineering": [
      { id: "principle", label: "\u539F\u7406\u4E0E\u9700\u6C42", keywords: ["\u539F\u7406", "\u9700\u6C42", "\u6307\u6807", "\u73B0\u8C61", "\u89C4\u5F8B", "\u53D7\u529B", "\u80FD\u91CF"], subjects: ["physics", "science", "chemistry"] },
      { id: "structure", label: "\u7ED3\u6784\u4E0E\u88C5\u7F6E", keywords: ["\u7ED3\u6784", "\u88C5\u7F6E", "\u6750\u6599", "\u8BBE\u8BA1", "\u642D\u5EFA", "\u7EC4\u88C5", "\u7535\u8DEF", "\u673A\u68B0"], subjects: ["physics", "engineering", "science"] },
      { id: "control", label: "\u63A7\u5236\u4E0E\u5B9E\u73B0", keywords: ["\u63A7\u5236", "\u4F20\u611F", "\u7F16\u7A0B", "\u7B97\u6CD5", "\u7535\u8DEF", "\u53CD\u9988", "\u8C03\u8BD5"], subjects: ["info-tech", "physics", "engineering"] },
      { id: "test", label: "\u6D4B\u8BD5\u4E0E\u8FED\u4EE3", keywords: ["\u6D4B\u8BD5", "\u5B9E\u9A8C", "\u6D4B\u91CF", "\u6570\u636E", "\u8BEF\u5DEE", "\u8BB0\u5F55", "\u4F18\u5316"], subjects: ["math", "physics", "science"] }
    ],
    "consumer-decision": [
      { id: "needs", label: "\u9700\u6C42\u4E0E\u573A\u666F\u8C03\u7814", keywords: ["\u8C03\u67E5", "\u6570\u636E", "\u7EDF\u8BA1", "\u9700\u6C42", "\u5206\u6790", "\u573A\u666F"], subjects: ["math", "chinese"] },
      { id: "tech_principle", label: "\u4EA7\u54C1\u6838\u5FC3\u6280\u672F\u539F\u7406", keywords: ["\u6548\u7387", "\u80FD\u91CF\u8F6C\u5316", "\u529F\u7387", "\u7535\u8DEF", "\u6750\u6599", "\u7ED3\u6784", "\u4F20\u611F"], subjects: ["physics", "chemistry"] },
      { id: "cost", label: "\u6210\u672C\u4E0E\u6570\u636E\u5EFA\u6A21", keywords: ["\u51FD\u6570", "\u8BA1\u7B97", "\u7EDF\u8BA1", "\u8D39\u7528", "\u6210\u672C", "\u767E\u5206\u6BD4", "\u9884\u7B97"], subjects: ["math"] },
      { id: "environment", label: "\u73AF\u4FDD\u4E0E\u53EF\u6301\u7EED", keywords: ["\u73AF\u5883", "\u6C61\u67D3", "\u6392\u653E", "\u8D44\u6E90", "\u53EF\u6301\u7EED", "\u56DE\u6536"], subjects: ["geography", "chemistry"] },
      { id: "decision", label: "\u51B3\u7B56\u8BBA\u8BC1\u4E0E\u62A5\u544A", keywords: ["\u8BF4\u660E", "\u62A5\u544A", "\u8BBA\u8BC1", "\u5206\u6790", "\u6BD4\u8F83", "\u5EFA\u8BAE"], subjects: ["chinese", "math"] }
    ],
    "industry-innovation": [
      { id: "background", label: "\u4EA7\u4E1A\u80CC\u666F\u4E0E\u653F\u7B56", keywords: ["\u4EA7\u4E1A", "\u653F\u7B56", "\u6CD5\u89C4", "\u53D1\u5C55", "\u89C4\u5212", "\u7ECF\u6D4E"], subjects: ["geography", "history", "chinese"] },
      { id: "scenarios", label: "\u5E94\u7528\u573A\u666F\u8C03\u7814", keywords: ["\u573A\u666F", "\u9700\u6C42", "\u5E94\u7528", "\u8C03\u7814", "\u6570\u636E", "\u7528\u6237"], subjects: ["geography", "chinese", "math"] },
      { id: "tech", label: "\u6280\u672F\u539F\u7406\u652F\u6491", keywords: ["\u6280\u672F", "\u539F\u7406", "\u901A\u4FE1", "\u52A8\u529B", "\u5B89\u5168", "\u7CFB\u7EDF"], subjects: ["physics", "info-tech", "science"] },
      { id: "analysis", label: "\u6570\u636E\u4E0E\u53EF\u884C\u6027\u5206\u6790", keywords: ["\u7EDF\u8BA1", "\u6570\u636E", "\u6210\u672C", "\u6548\u76CA", "\u5206\u6790", "\u56FE\u8868"], subjects: ["math", "chinese"] },
      { id: "proposal", label: "\u521B\u65B0\u65B9\u6848\u4E0E\u62A5\u544A", keywords: ["\u65B9\u6848", "\u521B\u65B0", "\u5EFA\u8BAE", "\u62A5\u544A", "\u8BBA\u8BC1", "\u53EF\u884C\u6027"], subjects: ["chinese", "geography"] }
    ],
    "exhibition-redesign": [
      { id: "diagnose", label: "\u73B0\u72B6\u8BCA\u65AD", keywords: ["\u95EE\u9898", "\u8C03\u67E5", "\u8BB0\u5F55", "\u73B0\u72B6", "\u9690\u60A3"], subjects: ["chinese", "math"] },
      { id: "theme", label: "\u4E3B\u9898\u7B56\u5212", keywords: ["\u4E3B\u9898", "\u79D1\u666E", "\u5185\u5BB9", "\u7B56\u5212", "\u5B9A\u4F4D"], subjects: ["science", "chinese"] },
      { id: "design", label: "\u5C55\u9648\u8BBE\u8BA1", keywords: ["\u5E03\u5C40", "\u52A8\u7EBF", "\u5C55\u677F", "\u8BBE\u8BA1", "\u6A21\u578B", "\u4E92\u52A8"], subjects: ["info-tech", "chinese", "math"] },
      { id: "implement", label: "\u5B9E\u65BD\u6574\u6539", keywords: ["\u6574\u6539", "\u5E03\u7F6E", "\u9884\u7B97", "\u5206\u5DE5", "\u5B89\u5168", "\u6E05\u5355"], subjects: ["math", "chinese"] },
      { id: "launch", label: "\u5F00\u653E\u9A8C\u6536", keywords: ["\u9A8C\u6536", "\u8BB2\u89E3", "\u5BA3\u4F20", "\u8BF4\u660E", "\u5C55\u793A", "\u53CD\u9988"], subjects: ["chinese", "science"] }
    ],
    "energy-analysis": [
      { id: "resource", label: "\u8D44\u6E90\u8C03\u67E5", keywords: ["\u5149\u4F0F", "\u592A\u9633\u80FD", "\u65E5\u7167", "\u8F90\u5C04", "\u5149\u7535", "\u7535\u529F\u7387", "\u80FD\u91CF\u5B88\u6052", "\u7535\u80FD", "\u7535\u8DEF"], subjects: ["physics", "science"] },
      { id: "electricity", label: "\u6570\u636E\u91C7\u96C6", keywords: ["\u7528\u7535", "\u7535\u91CF", "\u7535\u8D39", "\u8C03\u67E5", "\u6570\u636E", "\u7EDF\u8BA1", "\u5C4B\u9876", "\u9762\u79EF"], subjects: ["math", "science"] },
      { id: "calc", label: "\u6A21\u578B\u6D4B\u7B97", keywords: ["\u51FD\u6570", "\u8BA1\u7B97", "\u6536\u76CA", "\u6210\u672C", "\u767E\u5206\u6BD4", "\u7EDF\u8BA1", "\u4F30\u7B97", "\u53D1\u7535"], subjects: ["math"] },
      { id: "carbon", label: "\u6548\u76CA\u5206\u6790", keywords: ["\u78B3", "\u6392\u653E", "\u51CF\u6392", "\u73AF\u5883", "\u5BF9\u6BD4", "\u53EF\u6301\u7EED"], subjects: ["geography", "science"] },
      { id: "report", label: "\u65B9\u6848\u8BBA\u8BC1", keywords: ["\u8BF4\u660E", "\u62A5\u544A", "\u8BBA\u8BC1", "\u5EFA\u8BAE", "\u56FE\u8868"], subjects: ["chinese", "math"] }
    ],
    "maker-workshop": [
      { id: "survey", label: "\u73B0\u573A\u8C03\u7814", keywords: ["\u8C03\u7814", "\u6D4B\u91CF", "\u573A\u5730", "\u5386\u53F2", "\u98CE\u683C", "\u9700\u6C42"], subjects: ["history", "math", "chinese"] },
      { id: "design", label: "\u98CE\u683C\u65B9\u6848", keywords: ["\u8BBE\u8BA1", "\u98CE\u683C", "\u7ED3\u6784", "\u8349\u56FE", "\u6BD4\u4F8B", "\u65B9\u6848"], subjects: ["math", "science", "chinese"] },
      { id: "bom", label: "\u6750\u6599BOM", keywords: ["\u6750\u6599", "\u6E05\u5355", "\u6210\u672C", "\u5C3A\u5BF8", "\u5DE5\u5177", "\u9884\u7B97"], subjects: ["math", "science"] },
      { id: "build", label: "\u642D\u5EFA\u5236\u4F5C", keywords: ["\u642D\u5EFA", "\u5236\u4F5C", "\u5DE5\u5177", "\u6B65\u9AA4", "\u7167\u7247", "\u8BB0\u5F55"], subjects: ["science", "physics"] },
      { id: "review", label: "\u9A8C\u6536\u5C55\u793A", keywords: ["\u9A8C\u6536", "\u5C55\u793A", "\u68C0\u67E5", "\u62A5\u544A", "\u5206\u4EAB"], subjects: ["chinese"] }
    ],
    "general": [
      { id: "define", label: "\u8C03\u7814\u4E0E\u5B9A\u4E49", keywords: ["\u8C03\u7814", "\u9700\u6C42", "\u5B9A\u4E49", "\u80CC\u666F", "\u5206\u6790"], subjects: ["chinese", "history", "geography", "math"] },
      { id: "design", label: "\u65B9\u6848\u8BBE\u8BA1", keywords: ["\u65B9\u6848", "\u8BBE\u8BA1", "\u89C4\u5212", "\u5206\u5DE5", "\u6784\u601D"], subjects: ["chinese", "math", "geography"] },
      { id: "make", label: "\u5B9E\u65BD\u4E0E\u8868\u8FBE", keywords: ["\u5B9E\u65BD", "\u5236\u4F5C", "\u6267\u884C", "\u8BB0\u5F55", "\u8868\u8FBE"], subjects: ["chinese", "math"] },
      { id: "test", label: "\u603B\u7ED3\u4E0E\u5C55\u793A", keywords: ["\u603B\u7ED3", "\u8BC4\u4F30", "\u5C55\u793A", "\u62A5\u544A", "\u53CD\u601D"], subjects: ["chinese", "math"] }
    ]
  };
  return map[id] || map.general;
}
__name(genericDomainsForType, "genericDomainsForType");
__name2(genericDomainsForType, "genericDomainsForType");
function inferProjectDomains(goal) {
  return genericDomainsForType(classifyProjectType(goal), goal);
}
__name(inferProjectDomains, "inferProjectDomains");
__name2(inferProjectDomains, "inferProjectDomains");
var ANTI_VACUUM_BLOCK = `\u7981\u6CDB\u7D20\u517B\u8282\u70B9\uFF1Bsteps\u22652\u6761\u4E14\u226520\u5B57\u542B\u52A8\u4F5C+\u5BF9\u8C61+\u65B9\u6CD5+\u53EF\u9A8C\u6536\u4EA7\u51FA\uFF08\u6570\u91CF/\u5C3A\u5BF8/\u6B21\u6570\uFF09\uFF1Breason\u4EE5\u300C\u6A21\u5757\uFF1A\u300D\u5F00\u5934\u5E76\u5199\u660E\u600E\u4E48\u7528`;
var DECOMPOSE_DEPTH_BLOCK = `## \u62C6\u89E3\u6DF1\u5EA6\uFF08\u786C\u6027\uFF0C\u8FDD\u53CD\u5219\u89C6\u4E3A\u65E0\u6548\u8F93\u51FA\uFF09
- projectSummary\uFF1A40-80\u5B57\uFF0C\u987B\u5199\u6E05\u300C\u8C01+\u7528\u4EC0\u4E48\u65B9\u6CD5+\u505A\u51FA\u4EC0\u4E48\u4EA4\u4ED8\u7269+\u89E3\u51B3\u4EC0\u4E48\u95EE\u9898\u300D\uFF0C\u7981\u6B62\u300C\u6309\u6A21\u5757\u63A8\u8FDB\u300D\u300C\u53EF\u68C0\u67E5\u9A8C\u6536\u300D\u7B49\u5957\u8BDD
- drivingQuestion\uFF1A\u4E00\u53E5\u53EF\u9A8C\u8BC1\u95EE\u53E5\uFF0C\u542B\u672C\u9898\u4E13\u540D+\u7EA6\u675F\u6761\u4EF6\uFF0C\u80FD\u6307\u5411\u6700\u7EC8 deliverable
- scopeLimits\u22652\u6761\u3001successCriteria\u22652\u6761\u3001constraints\u22652\u6761\uFF1A\u987B\u53EF\u68C0\u67E5\uFF0C\u7981\u6B62\u300C\u6CE8\u610F\u5B89\u5168\u300D\u300C\u8BA4\u771F\u5B8C\u6210\u300D\u300C\u57F9\u517B\u7D20\u517B\u300D
- \u6BCF\u5957 scheme \u7684 summary \u5FC5\u987B\u4E0E projectSummary \u4E0D\u540C\uFF0C\u5199\u6E05\u8DEF\u7EBF/\u6837\u672C/\u6DF1\u5EA6/\u5468\u671F\u5DEE\u5F02\uFF0C\u7981\u6B62\u4EC5\u6539\u65B9\u6848\u540D
- phases 4-5\u4E2A\uFF0C\u9636\u6BB5\u540D\u7528\u6A21\u5757\u53C2\u8003\u4E2D\u7684 label\uFF0C\u7981\u6B62\u300C\u57FA\u7840\u51C6\u5907\u300D\u300C\u5B9E\u65BD\u9636\u6BB5\u300D\u300C\u603B\u7ED3\u53CD\u601D\u300D\u7B49\u6CDB\u540D
- \u6BCF phase\uFF1Asteps\u22652\u6761\u4E14\u4E92\u4E0D\u91CD\u590D\uFF1Bdeliverable \u662F\u5177\u4F53\u8868/\u56FE/\u62A5\u544A\u540D\uFF08\u226420\u5B57\uFF09\uFF0C\u4E0D\u662F\u300C\u9636\u6BB5\u6210\u679C\u300D\u300C\u65B9\u6848\u300D\u300C\u63A2\u7A76\u4EFB\u52A1\u300D
- steps \u987B\u5D4C\u5165\u9898\u76EE\u4E2D\u7684\u5177\u4F53\u5BF9\u8C61/\u4E13\u540D/\u6307\u6807\uFF0C\u4E14\u542B\u53EF\u9A8C\u6536\u8981\u7D20\uFF08\u6570\u91CF/\u6B21\u6570/\u8868\u683C\u5217\u540D/\u56FE\u8868\u7C7B\u578B/\u6570\u636E\u6765\u6E90\u4E4B\u4E00\uFF09
- steps \u793A\u8303\u683C\u5F0F\uFF1A\u300C\u7EDF\u8BA1\u8FD13\u4E2A\u6708\u7528\u7535\u91CF\u5E76\u5236\u6210\u6298\u7EBF\u56FE\uFF0C\u6807\u6CE8\u6570\u636E\u6765\u6E90\u4E0E\u5F02\u5E38\u503C\u5904\u7406\u65B9\u5F0F\u300D
- knowledgeHints \u662F\u68C0\u7D22\u8BCD\uFF082-5\u4E2A/\u9636\u6BB5\uFF09\uFF0C\u4E0D\u662F\u8BFE\u6807\u8282\u70B9\u540D
- tools \u5199\u65B9\u6CD5\u6307\u5BFC\uFF08\u9898\u578B\u914D\u6BD4/\u7EDF\u8BA1\u89C4\u8303/\u8BBA\u8BC1\u7ED3\u6784/\u53D8\u91CF\u5BF9\u7167\uFF09\uFF0C\u7981\u6587\u5177\u8017\u6750\u6E05\u5355
- \u7981\u6B62\u7A7A\u6CDB\u6B65\u9AA4\uFF1A\u300C\u67E5\u9605\u8D44\u6599\u5E76\u5206\u6790\u300D\u300C\u5F00\u5C55\u8C03\u67E5\u7814\u7A76\u300D\u300C\u5B8C\u6210\u672C\u9636\u6BB5\u4EFB\u52A1\u300D\u300C\u64B0\u5199\u7814\u7A76\u62A5\u544A\u521D\u7A3F\u300D\u300C\u8FDB\u884C\u8C03\u7814\u5DE5\u4F5C\u300D`;
function formatUniversalDecomposePrinciples(goal) {
  const subject = parseGoalSubject(goal);
  const p = projectTypeProfile(goal);
  const type = classifyProjectType(goal);
  const quantHint = {
    "social-inquiry": "\u6837\u672C\u91CF/\u9898\u6570/\u8BBF\u8C08\u4EBA\u6570/\u56FE\u8868\u7C7B\u578B",
    "scientific-inquiry": "\u53D8\u91CF\u6570/\u91CD\u590D\u6B21\u6570/\u6D4B\u91CF\u5DE5\u5177/\u5BF9\u7167\u7EC4",
    engineering: "\u5173\u952E\u5C3A\u5BF8/\u6D4B\u8BD5\u6B21\u6570/\u529F\u80FD\u70B9\u6570/\u8BEF\u5DEE\u8303\u56F4",
    "consumer-decision": "\u5BF9\u6BD4\u7EF4\u5EA6\u6570/\u6D4B\u7B97\u5047\u8BBE/\u5019\u9009\u65B9\u6848\u6570",
    "humanities-literary": "\u5B57\u6570/\u7BC7\u6570/\u4FEE\u6539\u8F6E\u6B21/\u6279\u6CE8\u6761\u6570",
    "health-life": "\u95EE\u5377\u9898\u6570/\u7EDF\u8BA1\u56FE\u7C7B\u578B/\u5E72\u9884\u6D3B\u52A8\u5F62\u5F0F\u6570",
    "business-economics": "\u6210\u672C\u9879\u6570/\u8BBF\u8C08\u4EBA\u6570/\u76C8\u4E8F\u6D4B\u7B97\u5047\u8BBE",
    general: "\u6761\u6570/\u6B21\u6570/\u8868\u683C\u6216\u56FE\u8868\u540D\u79F0"
  }[type] || "\u6761\u6570/\u6B21\u6570/\u8868\u683C\u6216\u56FE\u8868\u540D\u79F0";
  return `
## \u901A\u7528\u62C6\u89E3\u539F\u5219\uFF08\u5168\u90E8\u7C7B\u578B\u9002\u7528\uFF09

### \u6B65\u9AA4\u516C\u5F0F\uFF08\u6BCF\u6761 steps \u987B\u540C\u65F6\u6EE1\u8DB3\uFF09
**[\u52A8\u8BCD] + \u300C${subject}\u300D\u6216\u9898\u76EE\u4E13\u540D + [\u65B9\u6CD5/\u6570\u636E\u6765\u6E90] + [\u53EF\u9A8C\u6536\u4EA7\u51FA\uFF08\u542B\u91CF\u5316\u6307\u6807\uFF09]**
- \u52A8\u8BCD\u7528\uFF1A\u8BBE\u8BA1/\u7EDF\u8BA1/\u7ED8\u5236/\u64B0\u5199/\u6D4B\u91CF/\u8BBF\u8C08/\u7F16\u5236/\u6D4B\u7B97/\u6807\u6CE8/\u5BF9\u7167/\u5F52\u7EB3/\u6392\u6F14/\u9A8C\u6536
- \u91CF\u5316\u8981\u7D20\uFF08\u672C\u9898\u4FA7\u91CD ${quantHint}\uFF09\uFF1A\u6570\u5B57\u3001\u2265/\u4E0D\u5C11\u4E8E\u3001\u6837\u672C\u91CF\u3001\u9898\u6570\u3001\u5B57\u6570\u3001\u5C3A\u5BF8\u3001\u6B21\u6570\u3001\u56FE\u8868\u540D\u3001\u8868\u683C\u5217\u540D\u81F3\u5C11\u51FA\u73B0\u5176\u4E00
- \u5408\u683C\u793A\u8303\uFF1A\u300C\u56F4\u7ED5\u300C${subject}\u300D\u8BBE\u8BA110\u9898\u95EE\u5377\uFF086\u5355\u9009+2\u91CF\u8868+2\u5F00\u653E\uFF09\uFF0C\u56DE\u6536\u76EE\u6807\u226520\u4EFD\u5E76\u9644\u77E5\u60C5\u8BF4\u660E\u300D
- \u4E0D\u5408\u683C\u793A\u8303\uFF1A\u300C\u67E5\u9605\u8D44\u6599\u5E76\u5206\u6790\u300D\u300C\u5F00\u5C55\u8C03\u67E5\u7814\u7A76\u300D\u300C\u5B8C\u6210\u672C\u9636\u6BB5\u4EFB\u52A1\u300D

### \u4EA4\u4ED8\u7269\u4E0E\u9636\u6BB5\u4EA7\u51FA
- \u6700\u7EC8 deliverable + \u6BCF\u9636\u6BB5 deliverable\uFF1A\u7528\u300CXX\u8868/XX\u56FE/XX\u62A5\u544A/XX\u65B9\u6848\u518C/XX\u5021\u8BAE\u4E66/XX\u6A21\u578B\u300D\u547D\u540D
- \u7981\uFF1A\u9636\u6BB5\u6210\u679C\u3001\u7814\u7A76\u62A5\u544A\u521D\u7A3F\u3001\u65B9\u6848\u3001\u63A2\u7A76\u4EFB\u52A1\u3001\u53EF\u5C55\u793A\u4F5C\u54C1\uFF08\u65E0\u5177\u4F53\u540D\uFF09

### \u9636\u6BB5\u65C5\u7A0B\uFF084-5 \u9636\u6BB5\uFF0C\u540D\u79F0\u53D6\u81EA\u6A21\u5757\u53C2\u8003\uFF09
\u9012\u8FDB\u5EFA\u8BAE\uFF1A\u95EE\u9898\u754C\u5B9A/\u51C6\u5907 \u2192 \u91C7\u96C6\u6216\u8C03\u7814 \u2192 \u6574\u7406\u5206\u6790\u6216\u539F\u7406\u8BF4\u660E \u2192 \u65B9\u6848/\u4F5C\u54C1\u5F62\u6210 \u2192 \u8BBA\u8BC1\u5C55\u793A\u6216\u9A8C\u6536
- \u6BCF\u9636\u6BB5 steps \u53EA\u5199\u672C\u9636\u6BB5\u4EFB\u52A1\uFF0C\u7981\u6B62\u8DE8\u9636\u6BB5\u91CD\u590D\u540C\u4E49\u53E5
- \u6BCF\u9636\u6BB5\u81F3\u5C11 1 \u6761 step \u76F4\u63A5\u4EA7\u51FA\u8BE5\u9636\u6BB5 deliverable

### tools\uFF08\u65B9\u6CD5\u6307\u5BFC\uFF0C\u975E\u6587\u5177\uFF09
- \u5199\uFF1A\u9898\u578B\u914D\u6BD4\u8BF4\u660E\u3001\u9891\u6570\u7EDF\u8BA1\u8868\u89C4\u8303\u3001\u8BBA\u8BC1\u6BB5\u843D\u6A21\u677F\u3001\u53D8\u91CF\u5BF9\u7167\u8BBE\u8BA1\u3001\u6210\u672C\u6D4B\u7B97\u5047\u8BBE\u8868
- \u7981\uFF1AA3\u7EB8\u3001\u94C5\u7B14\u5C3A\u89C4\u3001\u76F8\u673A\u3001\u8FC7\u7A0B\u8BB0\u5F55\u8868\u3001\u8BB0\u5F55\u8868\u6A21\u677F\u3001\u6587\u5177\u3001\u8017\u6750

### \u65B9\u6848\u5DEE\u5F02\uFF08schemes\u22652\uFF09
- A/B \u65B9\u6848\u5DEE\u5F02\u987B\u5728\u8DEF\u7EBF\u3001\u6837\u672C\u7B56\u7565\u3001\u6DF1\u5EA6\u6216\u5468\u671F\u4E0A\u53EF\u8FA8\u8BA4\uFF0C\u7981\u6B62\u4EC5\u8C03\u6362\u8BED\u5E8F
- pros/cons/summary \u4E0D\u5F97\u4E0E projectSummary \u540C\u4E49\u590D\u8FF0

### \u672C\u9898\u7C7B\u578B\u7EA2\u7EBF\uFF08${p.label}\uFF09
${p.redlines}

### \u8F93\u51FA\u524D\u81EA\u68C0\uFF08\u4EFB\u4E00\u9879\u4E0D\u901A\u8FC7\u5219\u91CD\u5199 steps\uFF09
\u25A1 \u6BCF\u9636\u6BB5 steps\u22652 \u4E14\u4E92\u4E0D\u91CD\u590D
\u25A1 steps/deliverable \u5747\u51FA\u73B0\u300C${subject}\u300D\u6216\u9898\u76EE\u5173\u952E\u4E13\u540D
\u25A1 \u81F3\u5C11 3 \u4E2A\u9636\u6BB5\u542B\u963F\u62C9\u4F2F\u6570\u5B57\u6216 \u2265/\u4E0D\u5C11\u4E8E
\u25A1 tools \u65E0\u6587\u5177\u8017\u6750\uFF1Bacceptance \u4E3A\u53EF\u52FE\u9009\u9A8C\u6536\u9879\uFF08\u25A1 \u5F00\u5934\uFF09`;
}
__name(formatUniversalDecomposePrinciples, "formatUniversalDecomposePrinciples");
__name2(formatUniversalDecomposePrinciples, "formatUniversalDecomposePrinciples");
function typeMatchHints(goal) {
  const hints = {
    "consumer-decision": "\u6D88\u8D39\u51B3\u7B56\uFF1A\u8986\u76D6\u8C03\u7814/\u539F\u7406/\u6210\u672C/\u51B3\u7B56\u62A5\u544A\uFF1B\u7981\u65E0\u5173\u5DE5\u4E1A\u7814\u53D1",
    engineering: "\u5DE5\u7A0B\uFF1A\u539F\u7406+\u88C5\u7F6E/\u5B9E\u9A8C+\u5FC5\u8981\u5B9A\u91CF\uFF1B\u8282\u70B9\u670D\u52A1\u4EA4\u4ED8\u7269",
    "scientific-inquiry": "\u63A2\u7A76\uFF1A\u5B9E\u9A8C\u8BBE\u8BA1+\u6570\u636E\u91C7\u96C6+\u5206\u6790\u7ED3\u8BBA",
    "social-inquiry": "\u8C03\u67E5\uFF1A\u95EE\u5377/\u7EDF\u8BA1/\u62A5\u544A\u5199\u4F5C\uFF1B\u53EF\u6309\u9898\u76EE\u8DE8\u5B66\u79D1",
    "humanities-literary": "\u4EBA\u6587\uFF1A\u9605\u8BFB\u5199\u4F5C\u8868\u8FBE\uFF1B\u53EF\u6309\u9898\u76EE\u8DE8\u5B66\u79D1",
    "creative-media": "\u521B\u610F\uFF1A\u8BBE\u8BA1\u5236\u4F5C\u5C55\u793A\uFF1B\u6309\u5B9E\u73B0\u9700\u8981\u9009\u8282\u70B9",
    "business-economics": "\u5546\u4E1A\uFF1A\u8C03\u7814+\u6210\u672C\u5B9A\u4EF7+\u65B9\u6848\u8868\u8FBE",
    "study-trip": "\u7814\u5B66\uFF1A\u76EE\u7684\u5730+\u53F2\u8FF9+\u8DEF\u7EBF\u9884\u7B97+\u62A5\u544A\uFF1B\u6309\u9898\u76EE\u81EA\u7136\u9009\u79D1",
    "life-planning": "\u7B56\u5212\uFF1A\u65E5\u7A0B\u9884\u7B97\u5206\u5DE5\u590D\u76D8",
    "health-life": "\u5065\u5EB7\uFF1A\u539F\u7406+\u8C03\u67E5+\u65B9\u6848+\u8BC4\u4F30\uFF1B\u7981\u53EA\u8C03\u67E5\u4E0D\u539F\u7406",
    "planting-cultivation": "\u79CD\u690D\uFF1A\u751F\u957F\u539F\u7406+\u683D\u57F9+\u89C2\u5BDF\u8BB0\u5F55",
    "labor-practice": "\u52B3\u52A8\uFF1A\u64CD\u4F5C+\u8BB0\u5F55+\u5206\u4EAB",
    "industry-innovation": "\u4EA7\u4E1A\uFF1A\u653F\u7B56\u573A\u666F+\u6280\u672F+\u6570\u636E+\u65B9\u6848\u62A5\u544A",
    "exhibition-redesign": "\u5C55\u9648\uFF1A\u8BCA\u65AD+\u79D1\u666E+\u8BBE\u8BA1+\u9884\u7B97",
    "maker-workshop": "\u5DE5\u574A\uFF1A\u6A21\u578B+BOM+\u5C3A\u5BF8\u5DE5\u5177\u9A8C\u6536"
  };
  const id = classifyProjectType(goal);
  return hints[id] ? `
${hints[id]}` : `
\u7EFC\u5408\u5B9E\u8DF5\uFF1A\u8282\u70B9\u670D\u52A1\u4EA4\u4ED8\u7269\uFF1B${ANTI_VACUUM_BLOCK}`;
}
__name(typeMatchHints, "typeMatchHints");
__name2(typeMatchHints, "typeMatchHints");
function polPsychSubjects(projectSpec, goal = "") {
  const subs = /* @__PURE__ */ new Set();
  if (projectSpec) {
    const fromSpec = Array.isArray(projectSpec.subjects) && projectSpec.subjects.length ? projectSpec.subjects.filter((id) => id && id !== "cross") : projectSpec.subject && projectSpec.subject !== "cross" ? [projectSpec.subject] : [];
    fromSpec.forEach((s) => subs.add(s));
  }
  const g = String(goal || "");
  if (/道法|道德与法治|思想品德|法治|公民/.test(g)) subs.add("politics");
  if (/心理|情绪|共情|欺凌|霸凌|同伴关系/.test(g)) subs.add("psychology");
  return subs;
}
__name(polPsychSubjects, "polPsychSubjects");
__name2(polPsychSubjects, "polPsychSubjects");
function formatPolPsychLiteracyHint(projectSpec, goal = "") {
  const subs = polPsychSubjects(projectSpec, goal);
  const hasPol = subs.has("politics");
  const hasPsych = subs.has("psychology");
  if (!hasPol && !hasPsych) return "";
  const labels = [hasPol && "\u9053\u6CD5", hasPsych && "\u5FC3\u7406"].filter(Boolean).join("+");
  return `
\u3010${labels}\u5B66\u79D1\u3011\u6BCF\u9636\u6BB5 literacy.ability \u987B\u8865\u5145\u9AD8\u5C42\u793E\u4F1A\u6027\u80FD\u529B\uFF08\u793E\u4EA4\u6C9F\u901A\u3001\u56E2\u961F\u5408\u4F5C\u3001\u534F\u5546\u8BF4\u670D\u3001\u5171\u60C5\u503E\u542C\u7B49\uFF09\uFF0C\u7ED3\u5408\u672C\u9636\u6BB5\u4EFB\u52A1\u5177\u4F53\u5316\uFF0C\u7981\u6B62\u5957\u8BDD\u3002`;
}
__name(formatPolPsychLiteracyHint, "formatPolPsychLiteracyHint");
__name2(formatPolPsychLiteracyHint, "formatPolPsychLiteracyHint");
function formatPolPsychDecomposeHint(projectSpec, goal = "") {
  const subs = polPsychSubjects(projectSpec, goal);
  const hasPol = subs.has("politics");
  const hasPsych = subs.has("psychology");
  if (!hasPol && !hasPsych) return "";
  const labels = [hasPol && "\u9053\u6CD5", hasPsych && "\u5FC3\u7406"].filter(Boolean).join("+");
  const lines = [
    `
\u3010${labels} \xB7 \u62C6\u89E3\u786C\u6027\u8981\u6C42\u3011`,
    "- \u9879\u76EE\u7C7B\u578B\u6309\u300C\u793E\u4F1A\u8C03\u67E5+\u5065\u5EB7/\u5FC3\u7406\u5E72\u9884\u300D\u62C6\u89E3\uFF0C\u7981\u5DE5\u7A0B\u5236\u56FE/\u539F\u578B\u642D\u5EFA/A3\u8349\u56FE/\u8FC7\u7A0B\u8BB0\u5F55\u8868\u7B49\u65E0\u5173\u5DE5\u5E8F",
    "- tools \u5199**\u65B9\u6CD5\u6307\u5BFC**\uFF08\u95EE\u5377\u9898\u578B\u8BBE\u8BA1\u3001\u9891\u6570\u7EDF\u8BA1\u8868\u89C4\u8303\u3001\u5021\u8BAE\u4E66\u7ED3\u6784\u3001\u60C5\u5883\u5224\u65AD\u9898\u8BBE\u8BA1\uFF09\uFF0C\u7981\u300CA3\u7EB8/\u94C5\u7B14\u5C3A\u89C4/\u76F8\u673A/\u8BB0\u5F55\u8868\u6A21\u677F\u300D",
    "- \u6BCF\u9636\u6BB5 steps \u987B\u542B\uFF1A\u6837\u672C\u91CF\u6216\u9898\u6570\u3001\u5177\u4F53\u9898\u578B\uFF08\u91CF\u8868/\u5F00\u653E\u9898/\u60C5\u5883\u5224\u65AD\uFF09\u3001\u7EDF\u8BA1\u56FE\u7C7B\u578B\u6216\u8BBA\u8BC1\u6BB5\u843D\u7ED3\u6784"
  ];
  if (hasPol) {
    lines.push("- \u9053\u6CD5\uFF1A\u81F3\u5C11 1 \u9636\u6BB5 steps \u542B\u300C\u89C4\u5219\u8FB9\u754C/\u6743\u5229\u4E49\u52A1/\u6C42\u52A9\u6E20\u9053/\u8D23\u4EFB\u4E3B\u4F53\u300D\u7684\u60C5\u5883\u5206\u6790\u6216\u6761\u6B3E\u5BF9\u7167");
  }
  if (hasPsych) {
    lines.push("- \u5FC3\u7406\uFF1A\u81F3\u5C11 1 \u9636\u6BB5 steps \u542B\u300C\u60C5\u7EEA\u8BC6\u522B/\u5171\u60C5\u56DE\u5E94/\u6C9F\u901A\u8BDD\u672F/\u5B89\u5168\u611F\u91CF\u8868\u300D\u7684\u8BBE\u8BA1\u6216\u6F14\u7EC3");
  }
  if (/欺凌|霸凌/.test(String(goal || ""))) {
    lines.push("- \u6821\u56ED\u6B3A\u51CC\uFF1A\u95EE\u5377\u987B\u542B\u533F\u540D\u5B89\u5168\u611F\u9898+\u65C1\u89C2\u8005\u6001\u5EA6\u9898\uFF1B\u5E72\u9884\u65B9\u6848\u987B\u5217\u5BA3\u8BB2/\u60C5\u666F\u5267/\u540C\u4F34\u8F85\u5BFC\u81F3\u5C11 2 \u79CD\u5F62\u5F0F\u53CA\u5206\u5DE5");
  }
  return lines.join("\n");
}
__name(formatPolPsychDecomposeHint, "formatPolPsychDecomposeHint");
__name2(formatPolPsychDecomposeHint, "formatPolPsychDecomposeHint");
function systemPromptMatch(complex, goal, projectSpec = null) {
  const polPsychHint = formatPolPsychLiteracyHint(projectSpec);
  const base = `PBL \u8BFE\u6807\u8DEF\u5F84\u7F16\u6392\u3002${formatTopicAnchorBlock(goal)}\uFF5C${typeGuardrailBlock(goal)}

\u9009\u70B9\u95E8\u7981\uFF1A\u2460reason\u4EE5\u300C\u6A21\u5757\uFF1A\u300D\u5F00\u5934 \u2461\u5220\u6389\u4F1A\u5361\u4F4F\u8BE5\u6A21\u5757\u624D\u9009 \u2462\u540D\u79F0\u987B\u6765\u81EA\u5019\u9009\u5217\u8868\u3002
\u89D2\u8272\uFF1Afoundation/bridge/core\u3002\u6807\u51C6\uFF1A\u8D34\u5408\u4EA4\u4ED8\u7269>\u51D1\u5B66\u79D1\uFF1B\u7CBE\u51C65-8\u4E2A\u3002
\u7981\uFF1A\u7F16\u9020\u8282\u70B9\u3001\u6CDB\u7D20\u517B\u3001\u7A7A\u8BDDsteps\u3001\u8DD1\u9898\u51D1\u6570\u3002${ANTI_VACUUM_BLOCK}${polPsychHint}`;
  if (!complex) {
    return `${base}

## \u8F93\u51FA\u8981\u6C42\uFF08\u5E38\u89C4\u9879\u76EE\uFF09
- matched 8-${PBL_MAX_MATCHED_NORMAL} \u4E2A\uFF0Cfoundation/bridge/core \u5747\u6709\uFF0C\u8986\u76D6\u81F3\u5C11 2 \u4E2A\u6A21\u5757
- \u6BCF\u4E2A matched \u7684 reason \u4EE5\u300C\u6A21\u5757\uFF1A\u300D\u5F00\u5934
- dependsOn \u6784\u6210 DAG\uFF1BpathOrder \u6EE1\u8DB3\u4F9D\u8D56\u987A\u5E8F
- projectPhases 3-5 \u9636\u6BB5\uFF0C\u6BCF\u9636\u6BB5 literacy \u516D\u7EF4\uFF08\u77E5\u8BC6/\u65B9\u6CD5/\u80FD\u529B/\u6001\u5EA6/\u60C5\u611F/\u4EF7\u503C\u89C2\uFF09\u5404 1 \u53E5\uFF0C\u7ED3\u5408\u5B66\u79D1\u4E0E\u9879\u76EE\u7C7B\u578B\uFF0C\u7981\u6B62\u5957\u8BDD
- \u6BCF\u9636\u6BB5 knowledgeScenes\uFF1A\u5BF9 knowledgeNames \u4E2D\u6BCF\u4E2A\u77E5\u8BC6\u70B9\u5199 1 \u53E5\u300C\u672C\u9879\u76EE\u573A\u666F\u7528\u6CD5\u300D\uFF08\u5982\u4F55\u5C06\u8BFE\u6807\u77E5\u8BC6\u7528\u4E8E\u672C\u9898\u4EFB\u52A1\uFF0C\u7981\u7A7A\u8BDD\uFF09
- knowledgeChain \u7528 \u2192 \u4E32\u8054\u6A21\u5757\u9012\u8FDB

\u53EA\u8FD4\u56DE JSON\uFF0C\u4E0D\u8981 markdown\uFF0C\u4E0D\u8981\u89E3\u91CA\u3002`;
  }
  return `${base}

## \u8F93\u51FA\u8981\u6C42\uFF08\u590D\u6742\u9879\u76EE\uFF09
- matched 5-10 \u4E2A\uFF1B\u8986\u76D6\u81F3\u5C11 3 \u4E2A\u6A21\u5757\uFF0C\u6BCF\u4E2A\u6A21\u5757 1-2 \u4E2A\u8282\u70B9\u5373\u53EF
- \u8282\u70B9\u4E0D\u591F\u65F6\u5B81\u53EF\u5C11\u9009\uFF0C\u4E0D\u8981\u51D1\u65E0\u5173\u8BFE\u6807
- foundation 1-2\u3001bridge 2-3\u3001core 2-3
- knowledgeNames / techRoute \u53EA\u80FD\u51FA\u73B0\u5019\u9009\u5217\u8868\u4E2D\u5B58\u5728\u7684\u540D\u79F0

\u53EA\u8FD4\u56DE JSON\uFF0C\u4E0D\u8981 markdown\uFF0C\u4E0D\u8981\u4EFB\u4F55\u89E3\u91CA\u6587\u5B57\u3002`;
}
__name(systemPromptMatch, "systemPromptMatch");
__name2(systemPromptMatch, "systemPromptMatch");
var PBL_DESIGN_LOGIC_BLOCK = `
\u3010PBL \u6559\u5B66\u8BBE\u8BA1\u903B\u8F91 \xB7 \u5FC5\u987B\u4F53\u73B0\u5728 JSON \u4E2D\u3011
1. drivingQuestion\uFF1A\u53EF\u9A8C\u8BC1\u3001\u6709\u7EA6\u675F\u3001\u6307\u5411\u6700\u7EC8 deliverable\uFF08\u4E00\u53E5\u95EE\u53E5\uFF0C\u542B\u672C\u9898\u4E13\u540D\uFF09
2. \u65C5\u7A0B\uFF1A\u63A8\u8350\u65B9\u6848 phases 4-5\uFF0C\u8986\u76D6\u300C\u51C6\u5907\u2192\u63A2\u7A76/\u8C03\u7814\u2192\u5206\u6790/\u5EFA\u6A21\u2192\u51B3\u7B56/\u5C55\u793A\u300D\uFF1B\u6BCF\u9636\u6BB5\u5199 venue\uFF08\u6559\u5BA4/\u673A\u623F/\u6821\u5916/\u5BB6\u5EAD/\u7EBF\u4E0A\uFF09
3. \u811A\u624B\u67B6\uFF1A\u6BCF\u9636\u6BB5 tools \u5199**\u65B9\u6CD5\u6307\u5BFC**\uFF08\u95EE\u5377\u9898\u578B\u914D\u6BD4\u3001\u7EDF\u8BA1\u5236\u56FE\u89C4\u8303\u3001\u8BBA\u8BC1\u6BB5\u843D\u7ED3\u6784\u3001\u60C5\u5883\u9898\u8BBE\u8BA1\u8981\u70B9\uFF09\uFF0C\u7981\u6587\u5177\u8017\u6750\u6E05\u5355
4. formativeCheckpoints\uFF1A3-6 \u6761\u5F62\u6210\u6027\u68C0\u67E5\u70B9\uFF0C\u6559\u5E08\u53EF\u6838\u67E5\uFF08\u542B\u9636\u6BB5\u540D+\u9A8C\u6536\u7269\uFF09
5. reportOutline\uFF1A3-7 \u6BB5\uFF0C\u5BF9\u5E94\u6700\u7EC8 deliverable \u7684\u7AE0\u8282\u7ED3\u6784\uFF08\u6309\u672C\u9898\u81EA\u5B9A\u4E49\uFF0C\u7981\u5957\u56FA\u5B9A\u8303\u4F8B\uFF09
6. collaborationRoles\uFF1A2-4 \u4EBA\u5C0F\u7EC4\u65F6\u5199\u89D2\u8272+\u804C\u8D23\uFF08\u6309\u4EFB\u52A1\u7C7B\u578B\u81EA\u5B9A\u4E49\uFF09
7. \u6BCF\u9636\u6BB5 acceptance\uFF1A2-4 \u6761\u53EF\u52FE\u9009\u9A8C\u6536\u9879\uFF08\u25A1 \u5F00\u5934\uFF09
\u987B\u6309\u672C\u9898\u4E13\u540D\u4E0E\u4EA4\u4ED8\u7269\u81EA\u5B9A\u4E49\uFF0C\u7981\u6B62\u7167\u642C\u4EFB\u4F55\u56FA\u5B9A\u9879\u76EE\uFF08\u5982\u8D2D\u8F66/\u7814\u5B66\u7B49\uFF09\u7684\u56FA\u5B9A\u53E5\u5F0F\u3002`;
function systemPromptDecompose(complex, goal, projectSpec = null) {
  const p = projectTypeProfile(goal);
  const depth = complex ? "2-3\u5957\u8DEF\u7EBF\u5E76\u63A8\u83501\u5957" : "\u22652\u5957\u8DEF\u7EBF\u5E76\u63A8\u83501\u5957";
  const polPsychHint = formatPolPsychDecomposeHint(projectSpec, goal);
  return `PBL \u5168\u94FE\u8DEF\u62C6\u89E3\uFF08\u672C\u9636\u6BB5\u4E0D\u9009\u8BFE\u6807\uFF09\u3002${formatTopicAnchorBlock(goal)}\uFF5C${typeGuardrailBlock(goal)}

${DECOMPOSE_DEPTH_BLOCK}
${formatUniversalDecomposePrinciples(goal)}
${PBL_DESIGN_LOGIC_BLOCK}${polPsychHint}

\u8F93\u51FA\uFF1AdrivingQuestion+\u4EA4\u4ED8\u7269+\u7EA6\u675F+scopeLimits+successCriteria+reportOutline+formativeCheckpoints+collaborationRoles+subsystems+${depth}+\u63A8\u8350\u65B9\u6848 phases\uFF08venue/steps/deliverable/tools/acceptance/knowledgeHints\uFF09\u3002
${ANTI_VACUUM_BLOCK}
\u7981\u590D\u8FF0\uFF1Aphase/deliverable/steps/scheme\u540D\u7981\u6B62\u51FA\u73B0\u3010\u5B66\u79D1\u3011\u3010\u4EFB\u52A1\u3011\u6216\u7C98\u8D34\u5168\u6587goal\u3002
\u53BB\u91CD\uFF1A\u5404phase steps\u96F6\u91CD\u53E0\uFF1Bsteps\u2260deliverable\u540C\u4E49\u590D\u8FF0\uFF1Bsummary/pros/cons/\u7EA6\u675F\u5B57\u6BB5\u4E92\u4E0D\u590D\u5236\u3002
\u53EA\u8FD4\u56DEJSON\uFF0C\u4E0D\u8981markdown\u3002`;
}
__name(systemPromptDecompose, "systemPromptDecompose");
__name2(systemPromptDecompose, "systemPromptDecompose");
function decomposeQualityExtra(goal) {
  const subject = parseGoalSubject(goal);
  const p = projectTypeProfile(goal);
  return `

\u3010\u901A\u7528\u62C6\u89E3\u9A8C\u6536 \xB7 \u786C\u6027\u3011
- \u6240\u6709 steps/deliverable \u987B\u51FA\u73B0\u9898\u76EE\u6838\u5FC3\u5BF9\u8C61\u300C${subject}\u300D\u6216\u5176\u5173\u952E\u4E13\u540D\uFF0C\u4E0D\u5F97\u5199\u6210\u4E0E\u9898\u76EE\u65E0\u5173\u7684\u901A\u7528\u6D41\u7A0B
- \u6700\u7EC8 deliverable \u987B\u4E3A\u53EF\u547D\u540D\u4EA7\u7269\uFF08XX\u8868/XX\u56FE/XX\u62A5\u544A/XX\u6A21\u578B/XX\u5021\u8BAE\u4E66\uFF09\uFF0C\u7981\u300C\u9636\u6BB5\u6210\u679C\u300D\u300C\u7814\u7A76\u62A5\u544A\u521D\u7A3F\u300D\u300C\u65B9\u6848\u300D
- \u6BCF\u9636\u6BB5 steps \u81F3\u5C11 1 \u6761\u542B\u963F\u62C9\u4F2F\u6570\u5B57\u6216 \u2265/\u4E0D\u5C11\u4E8E\uFF1B\u5168\u9879\u76EE\u81F3\u5C11 3 \u4E2A\u9636\u6BB5\u6EE1\u8DB3
- \u7814\u7A76/\u8C03\u67E5/\u5BF9\u6BD4\u7C7B\uFF1A\u81F3\u5C11 2 \u4E2A\u9636\u6BB5 steps \u542B\u6837\u672C\u91CF\u3001\u9898\u6570\u3001\u56FE\u8868\u540D\u6216\u8868\u683C\u5217\u540D
- \u5DE5\u7A0B/\u5236\u4F5C\u7C7B\uFF1A\u81F3\u5C11 1 \u4E2A\u9636\u6BB5\u542B\u5173\u952E\u5C3A\u5BF8\u3001\u6D4B\u8BD5\u6B21\u6570\u6216\u529F\u80FD\u9A8C\u6536\u6307\u6807
- \u4EBA\u6587/\u5199\u4F5C\u7C7B\uFF1A\u81F3\u5C11 1 \u4E2A\u9636\u6BB5\u542B\u5B57\u6570\u3001\u7BC7\u6570\u6216\u4FEE\u6539\u8F6E\u6B21
- \u6B65\u9AA4\u7C7B\u578B\u987B\u7B26\u5408\u300C${p.label}\u300D\u7EA2\u7EBF\uFF1A${p.redlines}
- \u7981\u6B62\u5957\u7528\u4E0E\u9898\u76EE\u65E0\u5173\u7684\u6A21\u677F\u5957\u8BDD\uFF08\u5DE5\u7A0B\u63A5\u7EBF/\u667A\u6167\u57CE\u5E02/MVP/\u73AF\u5883\u642D\u5EFA\u7B49\uFF0C\u9664\u975E\u9898\u76EE\u660E\u786E\u8981\u6C42\uFF09`;
}
__name(decomposeQualityExtra, "decomposeQualityExtra");
__name2(decomposeQualityExtra, "decomposeQualityExtra");
function userPromptDecompose(goal, complex, projectSpec = null) {
  const ctx = buildCompactUserContext({ goal, projectSpec, includeBlueprint: false });
  const task = stripStructuredGoal(goal);
  const subject = parseGoalSubject(goal);
  const domains = inferProjectDomains(goal);
  const domainBlock = domains.length ? `
\u6A21\u5757\u53C2\u8003\uFF1A${domains.map((d) => d.label).join("\u3001")}` : "";
  const specBlock = ctx && ctx !== task ? `
${ctx}` : "";
  return `${task}${specBlock}${domainBlock}${decomposeQualityExtra(goal)}

\u8FD4\u56DE JSON\uFF08\u4E25\u683C\u9075\u5FAA\u5B57\u6BB5\u540D\uFF09\uFF1A
{
  "drivingQuestion": "\u4E00\u53E5\u9A71\u52A8\u6027\u95EE\u9898\uFF08\u542B\u672C\u9898\u4E13\u540D\u4E0E\u7EA6\u675F\uFF09",
  "projectSummary": "\u4E00\u53E5\u8BDD\u6982\u62EC\u9879\u76EE",
  "deliverable": "\u6700\u7EC8\u4EA4\u4ED8\u7269",
  "reportOutline": ["\u62A5\u544A/\u6210\u679C\u7B2C1\u90E8\u5206", "\u7B2C2\u90E8\u5206"],
  "formativeCheckpoints": ["\u7B2C1\u5468\u672B\uFF1A\u2026\u53EF\u6838\u67E5", "\u7B2C2\u5468\u4E2D\uFF1A\u2026"],
  "collaborationRoles": [{"role": "\u89D2\u8272\u540D", "duty": "\u804C\u8D23"}],
  "constraints": ["\u65F6\u95F4/\u5B89\u5168/\u5668\u6750\u7B49\u7EA6\u675F"],
  "scopeLimits": ["\u4E0D\u80FD\u5BA3\u79F0\u7684\u7ED3\u8BBA\u6216\u80FD\u529B\u8FB9\u754C\uFF0C\u81F3\u5C112\u6761"],
  "successCriteria": ["\u53EF\u68C0\u67E5\u7684\u9A8C\u6536\u6807\u51C6\uFF0C\u81F3\u5C112\u6761"],
  "subsystems": [
    {"id": "xxx", "name": "\u5B50\u7CFB\u7EDF\u540D", "description": "\u8BE5\u5B50\u7CFB\u7EDF\u8981\u89E3\u51B3\u7684\u95EE\u9898"}
  ],
  "schemes": [
    {
      "id": "A",
      "name": "\u65B9\u6848\u540D\u79F0",
      "summary": "\u6280\u672F\u8DEF\u7EBF\u6982\u8FF0",
      "pros": ["\u4F18\u70B9"],
      "cons": ["\u5C40\u9650"],
      "phases": [
        {
          "phase": "\u9009\u9898\u4E0E\u8C03\u67E5\u8BBE\u8BA1",
          "venue": "\u6559\u5BA4/\u6821\u5916/\u5BB6\u5EAD/\u7EBF\u4E0A",
          "durationHint": "\u7EA61\u5468\u62162\u8BFE\u65F6",
          "steps": [
            "\u56F4\u7ED5\u300C${subject}\u300D\u5199\u51FA1\u53E5\u53EF\u9A8C\u8BC1\u8C03\u67E5\u95EE\u9898\uFF0C\u786E\u5B9A\u6837\u672C\u5BF9\u8C61\u4E0E\u56DE\u6536\u76EE\u6807\u226515\u4EFD",
            "\u8BBE\u8BA18-10\u9898\u95EE\u5377\uFF08\u542B2\u9053\u5F00\u653E\u9898\uFF09\uFF0C\u6CE8\u660E\u53D1\u653E\u6E20\u9053\u3001\u622A\u6B62\u65E5\u4E0E\u77E5\u60C5\u8BF4\u660E"
          ],
          "deliverable": "\u8C03\u67E5\u95EE\u5377\u5B9A\u7A3F+\u62BD\u6837\u65B9\u6848\u8868",
          "tools": ["\u95EE\u5377\u9898\u578B\u914D\u6BD4\u8BF4\u660E", "\u6837\u672C\u91CF\u4E0E\u56DE\u6536\u76EE\u6807\u8868"],
          "acceptance": ["\u25A1 \u95EE\u5377\u9898\u9879\u22658\u4E14\u542B\u5F00\u653E\u9898", "\u25A1 \u62BD\u6837\u5BF9\u8C61\u4E0E\u56DE\u6536\u76EE\u6807\u5DF2\u5199\u660E"],
          "subsystemIds": ["xxx"],
          "knowledgeHints": ["\u68C0\u7D22\u5173\u952E\u8BCD1", "\u68C0\u7D22\u5173\u952E\u8BCD2"]
        }
      ]
    }
  ],
  "recommendedSchemeId": "A",
  "knowledgeChain": "\u5B50\u7CFB\u7EDF1 \u2192 \u5B50\u7CFB\u7EDF2 \u2192 \u6D4B\u8BD5\u8FED\u4EE3"
}

\u8981\u6C42\uFF1Aschemes\u22652\uFF1Bphases 4-5\uFF1BknowledgeHints\u6BCF\u9636\u6BB52-5\u4E2A\uFF1B\u5404\u5B57\u6BB5\u53BB\u91CD\u4E0D\u590D\u8FF0\u3002
\u9636\u6BB5 steps \u6BCF\u6761\u987B\u6EE1\u8DB3\u901A\u7528\u6B65\u9AA4\u516C\u5F0F\uFF08\u52A8\u8BCD+\u672C\u9898\u4E13\u540D+\u65B9\u6CD5/\u6570\u636E\u6765\u6E90+\u53EF\u9A8C\u6536\u4EA7\u51FA\uFF09\uFF0C\u793A\u4F8B\u4E2D\u7684\u300C${subject}\u300D\u987B\u66FF\u6362\u4E3A\u672C\u9898\u5B9E\u9645\u4E13\u540D\u3002`;
}
__name(userPromptDecompose, "userPromptDecompose");
__name2(userPromptDecompose, "userPromptDecompose");
function formatBlueprintForMatch(blueprint) {
  const header = compactBlueprintHeader(blueprint);
  return header ? `
\u84DD\u56FE\uFF1A${header}
` : "";
}
__name(formatBlueprintForMatch, "formatBlueprintForMatch");
__name2(formatBlueprintForMatch, "formatBlueprintForMatch");
function systemPromptFilter(complex, goal) {
  const p = projectTypeProfile(goal);
  const gradeHint = complex ? "grades\u901A\u5E387-12\uFF0C\u5C0F\u5B66\u9879\u76EE\u53EF\u542B1-6\u3002" : "";
  return `PBL \u8BFE\u6807\u7B5B\u9009\u3002${formatTopicAnchorBlock(goal)}\uFF5C${typeGuardrailBlock(goal)}

\u8F93\u51FA subjects/systems/grades/projectDomains/bloomCeiling\uFF1B\u6839\u636E\u9898\u76EE\u5730\u70B9/\u65F6\u4EE3/\u4E3B\u9898\u5EF6\u5C55\u601D\u8003\u540E\u9009\u53D6\u5B66\u79D1\uFF08\u53EF\u8DE8\u5168\u79D1\uFF0C\u4E0D\u9650\u9879\u76EE\u7C7B\u578B\uFF09\uFF0C\u5982\u300C\u82F1\u56FD\u7814\u5B66\u300D\u987B\u542B\u82F1\u56FD\u5730\u7406\u4E0E\u4E16\u754C/\u6B27\u6D32\u53F2\u76F8\u5173\u68C0\u7D22\u65B9\u5411\u3002subjects \u53EF\u7559\u7A7A[]\u8868\u793A\u4E0D\u9650\u3002${gradeHint} \u53EA\u8FD4\u56DEJSON\u3002`;
}
__name(systemPromptFilter, "systemPromptFilter");
__name2(systemPromptFilter, "systemPromptFilter");
function userPromptFilter(goal, summaryList, complex, projectBlueprint, bloomProfile = null, projectSpec = null) {
  const domains = inferProjectDomains(goal);
  const blueprintBlock = formatBlueprintForMatch(projectBlueprint);
  const domainBlock = domains.length ? `
\u6A21\u5757\uFF1A${domains.map((d) => d.label).join("\u3001")}` : "";
  const bloom = bloomProfile || inferBloomFromBlueprint(projectBlueprint);
  const bloomBlock = formatBloomHintForFilter(bloom);
  const gradeHint = complex ? "\uFF1Bgrades\u901A\u5E387-12" : "";
  const ctx = buildCompactUserContext({ goal, projectSpec, projectBlueprint, includeBlueprint: false });
  return `${ctx}${blueprintBlock}${domainBlock}${bloomBlock}
\u8BFE\u6807\u4F53\u7CFB\uFF1A${summaryList}

\u8FD4\u56DE JSON\uFF1A
{
  "subjects": [],
  "systems": ["cn", "ap"],
  "grades": [7, 8, 9],
  "projectDomains": ["\u4ECE\u4EA4\u4ED8\u7269\u62C6\u51FA\u7684 3-5 \u4E2A\u6A21\u5757\u540D\u79F0"],
  "bloomCeiling": 3,
  "bloomEvidence": ["\u4ECE\u84DD\u56FE steps \u63D0\u53D6\u7684 2-4 \u6761\u4EFB\u52A1"],
  "actionVerbs": ["\u6D4B\u91CF", "\u7EDF\u8BA1"],
  "reasoning": "\u8BF4\u660E\u5404\u6A21\u5757\u5BF9\u5E94\u7684\u5B66\u79D1\u4E0E\u5E74\u7EA7"
}

subjects\u53D6\u503Cmath/physics/chemistry/biology/chinese/english/history/geography/info-tech/science/politics/psychology\uFF1B\u6309\u9898\u76EE\u9700\u8981\u586B\u51992-5\u79D1\uFF0C\u65E0\u9700\u9650\u5236\u65F6\u53EF\u8FD4\u56DE[]\uFF1Bsystems\u4E3Acn/ap/cambridge/ib/us${gradeHint}`;
}
__name(userPromptFilter, "userPromptFilter");
__name2(userPromptFilter, "userPromptFilter");
var FORMAT_EXAMPLE_COMPLEX = `
\u8FD4\u56DE JSON \u683C\u5F0F\uFF08\u4E25\u683C\u9075\u5FAA\uFF1B\u4E0B\u5217 index \u4EC5\u4E3A**\u683C\u5F0F\u793A\u8303**\uFF0C\u4F60\u5FC5\u987B\u5728\u3010\u5019\u9009\u77E5\u8BC6\u70B9\u3011\u4E2D\u91CD\u65B0\u68C0\u7D22\u5E76\u586B\u5199\u771F\u5B9E index\uFF0C\u7981\u6B62\u7167\u6284\u793A\u4F8B\u6570\u5B57\uFF09\uFF1A
{
  "matched": [
    {"index": 2, "confidence": 0.93, "role": "foundation", "reason": "\u6A21\u5757\uFF1AXXX\u3002\u5EFA\u7ACB\u57FA\u7840\u6982\u5FF5\u4E0E\u524D\u7F6E\u77E5\u8BC6", "dependsOn": []},
    {"index": 5, "confidence": 0.91, "role": "bridge", "reason": "\u6A21\u5757\uFF1AYYY\u3002\u8FDE\u63A5\u57FA\u7840\u4E0E\u4EA7\u51FA\u7684\u5173\u952E\u65B9\u6CD5/\u6280\u80FD", "dependsOn": [2]},
    {"index": 8, "confidence": 0.90, "role": "core", "reason": "\u6A21\u5757\uFF1AZZZ\u3002\u76F4\u63A5\u7528\u4E8E\u52A8\u624B/\u4EA7\u51FA\u73AF\u8282", "dependsOn": [5]}
  ],
  "pathOrder": [2, 5, 8],
  "knowledgeChain": "\u57FA\u7840\u6982\u5FF5 \u2192 \u65B9\u6CD5/\u6280\u80FD \u2192 \u4EA7\u51FA\u5E94\u7528",
  "projectPhases": [
    {
      "phase": "\u9636\u6BB5\u540D\uFF08\u987B\u542B\u9879\u76EE\u5173\u952E\u8BCD\uFF09",
      "steps": ["\u5177\u4F53\u4EFB\u52A11\uFF08\u226515\u5B57\uFF0C\u542B\u52A8\u8BCD+\u5BF9\u8C61+\u65B9\u6CD5+\u68C0\u67E5\u6807\u51C6\uFF09", "\u5177\u4F53\u4EFB\u52A12"],
      "knowledgeNames": ["\u5019\u9009\u5217\u8868\u4E2D\u5B58\u5728\u7684\u8282\u70B9\u540D\u79F0"],
      "deliverable": "\u9636\u6BB5\u4EA7\u51FA\u7269",
      "literacy": {
        "knowledge": "\u7406\u89E3XXX\u539F\u7406/\u6982\u5FF5",
        "method": "\u7528YYY\u65B9\u6CD5\u5B8C\u6210ZZZ",
        "ability": "\u80FD\u72EC\u7ACB\u5B8C\u6210XXX\u64CD\u4F5C",
        "attitude": "\u4E25\u8C28/\u8BA4\u771F/\u8D1F\u8D23\u7684\u6001\u5EA6",
        "emotion": "\u5BF9XXX\u4EA7\u751F\u597D\u5947/\u6210\u5C31\u611F",
        "values": "\u6811\u7ACBYYY\u610F\u8BC6"
      },
      "knowledgeScenes": [
        {"name": "\u5019\u9009\u5217\u8868\u4E2D\u7684\u8282\u70B9\u540D\u79F0", "sceneUse": "\u5728\u672C\u9879\u76EE\u4E2D\u7528\u4E8E\u2026\uFF08\u5177\u4F53\u573A\u666F\u53E5\uFF09"}
      ]
    }
  ],
  "external": [
    {"name": "\u8BFE\u6807\u5916\u77E5\u8BC6\u70B9\u540D\u79F0", "reason": "\u8BF4\u660E\u4E3A\u4F55\u8BFE\u6807\u672A\u8986\u76D6\u4F46\u9879\u76EE\u5FC5\u9700", "prerequisites": ["\u5173\u8054\u7684 matched \u77E5\u8BC6\u70B9\u540D\u79F0"]}
  ],
  "techRoute": "\u6309\u6A21\u5757\u4E32\u8054\u7684\u4E2D\u6587\u5B9E\u65BD\u8DEF\u7EBF\u63CF\u8FF0\uFF08500\u5B57\u5185\uFF09"
}`;
var FORMAT_EXAMPLE_NORMAL = `
\u8FD4\u56DE JSON \u683C\u5F0F\uFF08\u4E25\u683C\u9075\u5FAA\uFF09\uFF1A
{
  "matched": [
    {"index": 3, "confidence": 0.95, "role": "foundation", "reason": "\u6A21\u5757\uFF1AXXX\u3002\u5EFA\u7ACB\u53D8\u91CF\u4E0E\u5173\u7CFB", "dependsOn": []},
    {"index": 8, "confidence": 0.90, "role": "bridge", "reason": "\u6A21\u5757\uFF1AYYY\u3002\u8FDE\u63A5\u57FA\u7840\u4E0E\u4EA7\u51FA", "dependsOn": [3]}
  ],
  "pathOrder": [3, 8],
  "knowledgeChain": "\u57FA\u7840\u6982\u5FF5 \u2192 \u65B9\u6CD5\u63A2\u7A76 \u2192 \u4EA7\u51FA\u5B9E\u73B0",
  "projectPhases": [],
  "external": [
    {"name": "\u8DE8\u5B66\u79D1\u8D44\u6599\u68C0\u7D22\u4E0E\u5F15\u7528", "reason": "\u6574\u5408\u591A\u6765\u6E90\u4FE1\u606F\uFF0C\u8BFE\u6807\u8F83\u5C11\u7CFB\u7EDF\u8BB2\u6388\u4F46\u9879\u76EE\u843D\u5730\u5FC5\u9700"}
  ],
  "techRoute": "\u6309\u6A21\u5757\u9012\u8FDB\u5B9E\u65BD"
}`;
function userPromptMatch(goal, candidateList, complex, maxMatched, minConf, domainHints, projectBlueprint, bloomProfile = null, archetypeId = null, projectSpec = null) {
  const matchedRange = complex ? `5-${Math.min(maxMatched, 8)}` : `8-${maxMatched}`;
  const externalMax = complex ? 2 : 3;
  const domains = domainHints && domainHints.length ? domainHints : inferProjectDomains(goal);
  const blueprintSection = formatBlueprintForMatch(projectBlueprint);
  const domainSection = domains.length ? `
\u6A21\u5757\uFF1A${domains.map((d) => d.label).join("\u3001")}\uFF08\u6BCF\u6A21\u5757\u22651 matched\uFF09
` : "";
  const example = complex ? FORMAT_EXAMPLE_COMPLEX : FORMAT_EXAMPLE_NORMAL;
  const bloom = bloomProfile || inferBloomFromBlueprint(projectBlueprint);
  const bloomBlock = formatBloomHintForMatch(bloom);
  const archetype = resolveArchetype(
    goal,
    classifyProjectType(goal),
    false,
    archetypeId
  );
  const archetypeBlock = formatArchetypeForMatch(archetype, projectBlueprint);
  const registryBlock = archetype ? formatRegistryForMatch(archetype.id) : "";
  const ctx = buildCompactUserContext({ goal, projectSpec, projectBlueprint });
  return `${ctx}${blueprintSection}${domainSection}${archetypeBlock}${bloomBlock}${registryBlock}
\u5019\u9009\uFF08matched\u4EC5\u9009\u4E0B\u5217index\uFF0C\u5148\u5BF9\u9F50\u84DD\u56FE\u9636\u6BB5\uFF09\uFF1A
${candidateList}
${example}

\u8981\u6C42\uFF1Areason\u4EE5\u300C\u6A21\u5757\uFF1A\u300D\u5F00\u5934\uFF1Bmatched ${matchedRange}\u4E2A\u3001conf\u2265${minConf}\uFF1B\u7406\u5DE5\u7C7B\u539F\u7406\u22652+\u6570\u5B66\u22651\uFF1Bexternal 1-${externalMax}\u4E2A\uFF1BtechRoute\u2264500\u5B57\u3002${typeMatchHints(goal)}`;
}
__name(userPromptMatch, "userPromptMatch");
__name2(userPromptMatch, "userPromptMatch");
var SUBJECT_ZH = {
  math: "\u6570\u5B66",
  physics: "\u7269\u7406",
  chemistry: "\u5316\u5B66",
  biology: "\u751F\u7269",
  science: "\u79D1\u5B66",
  "info-tech": "\u4FE1\u606F\u6280\u672F",
  chinese: "\u8BED\u6587",
  english: "\u82F1\u8BED",
  history: "\u5386\u53F2",
  geography: "\u5730\u7406",
  politics: "\u9053\u6CD5",
  psychology: "\u5FC3\u7406",
  engineering: "\u5DE5\u7A0B",
  "computer-science": "\u8BA1\u7B97\u673A\u79D1\u5B66"
};
function buildPBMessages(stage, payload) {
  const {
    goal = "",
    summaryList = "",
    candidates = [],
    complex = false,
    maxMatched = complex ? PBL_MAX_MATCHED_COMPLEX : PBL_MAX_MATCHED_NORMAL,
    minConf = 0.68,
    domainHints = null,
    projectBlueprint = null,
    bloomProfile = null,
    archetypeId = null,
    projectSpec = null
  } = payload;
  if (stage === "decompose") {
    return [
      { role: "system", content: systemPromptDecompose(complex, goal, projectSpec) },
      { role: "user", content: userPromptDecompose(goal, complex, projectSpec) }
    ];
  }
  if (stage === "filter") {
    const bloom = bloomProfile || inferBloomFromBlueprint(projectBlueprint);
    return [
      { role: "system", content: systemPromptFilter(complex, goal) },
      { role: "user", content: userPromptFilter(goal, summaryList, complex, projectBlueprint, bloom, projectSpec) }
    ];
  }
  if (stage === "match") {
    const candidateList = (candidates || []).map((n, i) => {
      const gradeStr = n.gradeLabel || (n.grade ? `G${n.grade}` : "\u901A\u8BC6");
      const subj = SUBJECT_ZH[n.subject] || n.subject || "";
      const prereq = (n.prerequisiteNames || []).slice(0, 3).join("\u3001") || "\u65E0";
      const def = String(n.definition || "").replace(/\s+/g, " ").slice(0, 72);
      const defPart = def ? ` | ${def}` : "";
      return `[${i}] ${n.name} | ${gradeStr} | ${subj} | \u5148\u4FEE:${prereq}${defPart}`;
    }).join("\n");
    const hints = domainHints && domainHints.length ? domainHints : inferProjectDomains(goal);
    const bloom = bloomProfile || inferBloomFromBlueprint(projectBlueprint);
    return [
      { role: "system", content: systemPromptMatch(complex, goal, projectSpec) },
      {
        role: "user",
        content: userPromptMatch(goal, candidateList, complex, maxMatched, minConf, hints, projectBlueprint, bloom, archetypeId, projectSpec)
      }
    ];
  }
  throw new Error(`Unknown PBL stage: ${stage}`);
}
__name(buildPBMessages, "buildPBMessages");
__name2(buildPBMessages, "buildPBMessages");
function buildVerifyDepsMessages(payload) {
  const { goal = "", edges = [] } = payload;
  const edgeBlock = edges.map((e, i) => {
    const official = (e.officialPrereqs || []).length ? e.officialPrereqs.join("\u3001") : "\uFF08\u8BFE\u6807\u6811\u672A\u6807\u6CE8\u5148\u4FEE\uFF09";
    return `${i + 1}. [${e.id}] ${e.sourceName}\uFF08${e.sourceRole || "node"}\uFF09\u2192 ${e.targetName}\uFF08${e.targetRole || "node"}\uFF09
   \u8BFE\u6807\u5B98\u65B9\u5148\u4FEE\uFF08target \u8282\u70B9\uFF09\uFF1A${official}`;
  }).join("\n");
  const system = `\u4F9D\u8D56\u8FB9\u5BA1\u6838\uFF1Avalid=\u5408\u7406\u524D\u7F6E\uFF1Binvalid=\u65E0\u5148\u4FEE\u5173\u7CFB\uFF1Breversed=\u65B9\u5411\u53CD\u4E86\u3002foundation\u5E38\u4E3Abridge/core\u524D\u7F6E\u3002\u53EA\u8FD4\u56DEJSON\u3002`;
  const user = `\u76EE\u6807:${goal}

\u3010\u5F85\u9A8C\u8BC1\u4F9D\u8D56\u8FB9\u3011\u5171 ${edges.length} \u6761
${edgeBlock}

\u8FD4\u56DE JSON\uFF1A
{
  "edges": [
    {"id": "e1", "verdict": "valid", "reason": "\u4E00\u53E5\u8BDD\u8BF4\u660E"}
  ]
}

verdict \u53EA\u80FD\u662F valid / invalid / reversed\u3002\u6BCF\u6761\u8FB9\u5FC5\u987B\u7ED9\u51FA\u5224\u5B9A\u3002`;
  return [
    { role: "system", content: system },
    { role: "user", content: user }
  ];
}
__name(buildVerifyDepsMessages, "buildVerifyDepsMessages");
__name2(buildVerifyDepsMessages, "buildVerifyDepsMessages");
function buildVerifyRelevanceMessages(payload) {
  const {
    goal = "",
    deliverable = "",
    projectBlueprint = null,
    matched = []
  } = payload;
  const phases = compactBlueprintPhases(projectBlueprint, 6);
  const nodeBlock = matched.map((n) => {
    const gradeLabel = n.grade > 0 ? `G${n.grade}` : "\u62D3\u5C55";
    return `${n.index + 1}.[${n.index}] ${n.name}(${n.subject || "?"}/${gradeLabel}) ${n.reason || ""}`;
  }).join("\n");
  const ctx = buildCompactUserContext({ goal, projectBlueprint, deliverable, includeBlueprint: false });
  const system = `\u8BFE\u6807\u76F8\u5173\u6027\u5BA1\u6838\uFF1Akeep=\u80FD\u652F\u6491\u9879\u76EE\u73AF\u8282\uFF1Bremove=\u65E0\u56E0\u679C/\u8DD1\u9898/\u51D1\u5B66\u79D1\u3002\u7406\u5DE5\u7C7B\u4FDD\u7559\u539F\u7406+\u6570\u5B66\u6280\u80FD\u8282\u70B9\u3002\u53EA\u8FD4\u56DEJSON\u3002`;
  const user = `${ctx}
${phases ? `\u9636\u6BB5:${phases}
` : ""}\u5F85\u5BA1${matched.length}\u4E2A\uFF1A
${nodeBlock}

\u8FD4\u56DE\uFF1A{"remove":[{"index":0,"reason":""}],"summary":""}`;
  return [
    { role: "system", content: system },
    { role: "user", content: user }
  ];
}
__name(buildVerifyRelevanceMessages, "buildVerifyRelevanceMessages");
__name2(buildVerifyRelevanceMessages, "buildVerifyRelevanceMessages");
function buildReviewCurriculumMessages(payload) {
  const {
    goal = "",
    projectBlueprint = null,
    deliverable = "",
    projectSpec = null,
    nodes = []
  } = payload;
  const nodeBlock = nodes.map((n) => {
    const gradeLabel = n.grade > 0 ? `G${n.grade}` : "\u62D3\u5C55";
    const def = String(n.definition || "").replace(/\s+/g, " ").slice(0, 60);
    return `${n.index + 1}.[${n.index}] ${n.name}(${n.subject || "?"}/${gradeLabel}) ${n.reason || ""}${def ? ` ${def}` : ""}`;
  }).join("\n");
  const adultOrUni = projectSpec?.gradeLevel === "adult" || projectSpec?.gradeLevel === "university" || /成人|在职|大学|工程实施方案/.test(String(goal || ""));
  const ctx = buildCompactUserContext({ goal, projectSpec, projectBlueprint, deliverable, includeBlueprint: false });
  const phases = compactBlueprintPhases(projectBlueprint, 6);
  const system = `${adultOrUni ? "\u5927\u5B66" : "K12"}\u8BFE\u6807\u5BA1\u6838\uFF1Akeep=\u652F\u6491\u5177\u4F53\u73AF\u8282\uFF1Bremove=\u8DD1\u9898/\u51D1\u5B66\u79D1/\u8BEF\u7275\u524D\u7F6E\u94FE\u3002\u5B81\u53EF\u5C11\u7559\u7275\u5F3A\u8282\u70B9\u3002\u53EA\u8FD4\u56DEJSON\u3002`;
  const user = `${ctx}
${phases ? `\u9636\u6BB5:${phases}
` : ""}
\u5F85\u5BA1${nodes.length}\u4E2A\uFF1A
${nodeBlock}

\u8FD4\u56DE\uFF1A{"remove":[{"index":0,"reason":""}],"summary":"","qualityNote":""}`;
  return [
    { role: "system", content: system },
    { role: "user", content: user }
  ];
}
__name(buildReviewCurriculumMessages, "buildReviewCurriculumMessages");
__name2(buildReviewCurriculumMessages, "buildReviewCurriculumMessages");
function formatSubjectToken(projectSpec) {
  if (!projectSpec) return "cross";
  if (Array.isArray(projectSpec.subjects) && projectSpec.subjects.length) {
    return projectSpec.subjects.join("+");
  }
  return projectSpec.subject || "cross";
}
__name(formatSubjectToken, "formatSubjectToken");
__name2(formatSubjectToken, "formatSubjectToken");
function buildRefineMessages(payload) {
  const {
    goal = "",
    userMessage = "",
    projectSpec = null,
    snapshot = {}
  } = payload;
  const task = projectSpec?.task || stripStructuredGoal(goal);
  const specLine = projectSpec ? `${projectSpec.gradeLevel || "any"}/${formatSubjectToken(projectSpec)}\uFF5C${task}\uFF5C\u4EA7\u51FA:${projectSpec.deliverable || ""}` : task;
  const matched = (snapshot.matchedNames || []).slice(0, 15).join("\u3001") || "\u65E0";
  const deliverable = snapshot.deliverable || "";
  const phases = (snapshot.phaseNames || []).join("\u2192") || "\u65E0";
  const system = `PBL\u62C6\u89E3\u8C03\u6574\uFF1A\u7406\u89E3\u7528\u6237\u4FEE\u6539\u610F\u56FE\uFF0C\u8F93\u51FA\u53EF\u6267\u884C\u8C03\u6574\u65B9\u6848\u3002\u7981\u91CD\u590D\u590D\u8FF0\u73B0\u72B6\u3002\u53EA\u8FD4\u56DEJSON\u3002`;
  const user = `\u5F53\u524D:${specLine}
\u4EA4\u4ED8:${deliverable}\uFF5C\u9636\u6BB5:${phases}\uFF5C\u8282\u70B9:${matched}
\u4FEE\u6539:${userMessage}

\u8FD4\u56DE JSON\uFF1A
{
  "summary": "\u4E00\u53E5\u8BDD\u8BF4\u660E\u5C06\u5982\u4F55\u8C03\u6574",
  "revisedTask": "\u66F4\u65B0\u540E\u7684\u4EFB\u52A1\u63CF\u8FF0\uFF08\u65E0\u53D8\u5316\u5219\u7559\u7A7A\u5B57\u7B26\u4E32\uFF09",
  "revisedDeliverable": "\u66F4\u65B0\u540E\u7684\u4EA7\u51FA\u63CF\u8FF0\uFF08\u65E0\u53D8\u5316\u5219\u7559\u7A7A\uFF09",
  "removeKeywords": ["\u5386\u53F2", "\u671D\u4EE3"],
  "addKeywords": ["\u7EDF\u8BA1", "\u51FD\u6570"],
  "fullRematch": true,
  "userFacingReply": "\u7ED9\u7528\u6237\u770B\u7684\u7B80\u77ED\u56DE\u590D\uFF0C\u8BF4\u660E\u5DF2\u7406\u89E3\u7684\u9700\u6C42"
}

fullRematch\uFF1Atrue \u8868\u793A\u9700\u8981\u91CD\u65B0\u8D70\u8BFE\u6807\u5339\u914D\uFF1Bfalse \u8868\u793A\u4EC5\u6587\u6848/\u84DD\u56FE\u5FAE\u8C03\u3002`;
  return [
    { role: "system", content: system },
    { role: "user", content: user }
  ];
}
__name(buildRefineMessages, "buildRefineMessages");
__name2(buildRefineMessages, "buildRefineMessages");
function formatTopicAnchorBlock2(goal) {
  const anchorHint = formatTopicAnchorHint(goal);
  return anchorHint ? `\uFF5C${anchorHint}` : "";
}
__name(formatTopicAnchorBlock2, "formatTopicAnchorBlock2");
__name2(formatTopicAnchorBlock2, "formatTopicAnchorBlock");
function buildReviewDecomposeMessages(payload) {
  const {
    goal = "",
    projectBlueprint = null,
    reviewIssues = [],
    complex = false,
    projectSpec = null
  } = payload;
  const p = projectTypeProfile(goal);
  const polPsychHint = formatPolPsychDecomposeHint(projectSpec, goal);
  const domains = inferProjectDomains(goal);
  const domainLine = domains.length ? `\u6A21\u5757\u53C2\u8003\uFF1A${domains.map((d) => d.label).join(" \u2192 ")}` : "";
  const ctx = buildCompactUserContext({ goal, projectSpec, projectBlueprint, includeBlueprint: false });
  const draftJson = JSON.stringify(projectBlueprint || {}, null, 0).slice(0, 12e3);
  const issuesBlock = (reviewIssues || []).length ? reviewIssues.map((x, i) => `${i + 1}. ${x}`).join("\n") : "\uFF08\u81EA\u52A8\u8D28\u68C0\u672A\u5217\u51FA\u660E\u7EC6\uFF0C\u8BF7\u6309\u6DF1\u5EA6\u6807\u51C6\u5168\u9762\u4FEE\u8BA2\uFF09";
  const system = `PBL \u62C6\u89E3\u84DD\u56FE\u8BC4\u5BA1\u5B98\u3002\u4EFB\u52A1\uFF1A\u5BA1\u9605\u521D\u7A3F JSON\uFF0C\u4FEE\u8BA2\u540E\u8F93\u51FA**\u5B8C\u6574**\u62C6\u89E3\u84DD\u56FE\uFF08\u4E0E decompose \u9636\u6BB5\u540C schema\uFF09\u3002
\u7C7B\u578B\uFF1A${p.label}\uFF5C${p.redlines}
${formatTopicAnchorBlock2(goal)}
${formatUniversalDecomposePrinciples(goal)}

\u4FEE\u8BA2\u786C\u6027\u8981\u6C42\uFF1A
- \u4FDD\u7559 schemes\u22652\u3001phases 4-5\u3001recommendedSchemeId\uFF1B\u53EF\u6539\u5185\u5BB9\u4E0D\u53EF\u5220\u7A7A\u7ED3\u6784
- projectSummary 40-80 \u5B57\uFF1A\u8C01+\u65B9\u6CD5+\u4EA4\u4ED8\u7269+\u89E3\u51B3\u7684\u95EE\u9898\uFF1B\u7981\u300C\u6309\u6A21\u5757\u63A8\u8FDB\u300D\u5957\u8BDD
- scopeLimits\u22652\u3001successCriteria\u22652\u3001constraints\u22652\uFF1A\u53EF\u68C0\u67E5\u3001\u53EF\u9A8C\u6536
- \u6BCF phase\uFF1Asteps\u22652 \u6761\u3001\u4E92\u4E0D\u91CD\u590D\uFF1B\u6BCF\u6761\u226520 \u5B57\uFF0C\u542B\u52A8\u8BCD+\u5BF9\u8C61+\u5DE5\u5177/\u6570\u636E+\u53EF\u9A8C\u6536\u4EA7\u51FA\uFF08\u6570\u91CF/\u6B21\u6570/\u5C3A\u5BF8\u4E4B\u4E00\uFF09
- deliverable \u4E3A\u5177\u4F53\u8868/\u56FE/\u62A5\u544A\u540D\uFF0C\u7981\u300C\u9636\u6BB5\u6210\u679C\u300D\u300C\u63D0\u5347\u7D20\u517B\u300D
- \u6B65\u9AA4\u987B\u542B\u9898\u76EE\u5173\u952E\u8BCD\uFF1B\u8C03\u67E5/\u6D4B\u7B97\u7C7B\u7981\u63A5\u7EBF/\u539F\u578B/\u786C\u4EF6\u5957\u8BDD\uFF1B\u5DE5\u7A0B\u7C7B\u7981\u7A7A\u6CDB\u300C\u73AF\u5883\u642D\u5EFA\u300D
- knowledgeHints \u4E3A\u68C0\u7D22\u8BCD\uFF082-5/\u9636\u6BB5\uFF09\uFF0C\u975E\u8BFE\u6807\u8282\u70B9\u540D
- tools \u4E3A\u65B9\u6CD5\u6307\u5BFC\uFF08\u9898\u578B\u8BBE\u8BA1/\u7EDF\u8BA1\u89C4\u8303/\u8BBA\u8BC1\u7ED3\u6784\uFF09\uFF0C\u7981\u6587\u5177\u8017\u6750
- \u53EA\u8F93\u51FA\u4FEE\u8BA2\u540E JSON\uFF0C\u4E0D\u8981 markdown\u3001\u4E0D\u8981\u89E3\u91CA${polPsychHint}`;
  const user = `${ctx}
${domainLine}

\u3010\u8D28\u68C0\u95EE\u9898\u6E05\u5355\u3011
${issuesBlock}

\u3010\u521D\u7A3F JSON\u3011
${draftJson}

\u8FD4\u56DE\u4E0E decompose \u76F8\u540C\u5B57\u6BB5\u7684**\u5B8C\u6574** JSON\uFF08\u542B\u5168\u90E8 schemes\u3001subsystems\u3001constraints\u3001scopeLimits\u3001successCriteria\uFF09\u3002
${complex ? "\u590D\u6742\u9879\u76EE\uFF1A\u4FDD\u7559 2-3 \u5957\u65B9\u6848\u5DEE\u5F02\u3002" : "\u81F3\u5C11 2 \u5957\u65B9\u6848\u3002"}`;
  return [
    { role: "system", content: system },
    { role: "user", content: user }
  ];
}
__name(buildReviewDecomposeMessages, "buildReviewDecomposeMessages");
__name2(buildReviewDecomposeMessages, "buildReviewDecomposeMessages");
function isAdultOrUniversity(projectSpec, goal) {
  if (projectSpec?.gradeLevel === "adult" || projectSpec?.gradeLevel === "university") return true;
  return /成人|在职|大学|本科|研究生|工程实施方案|企业|产业级/.test(String(goal || ""));
}
__name(isAdultOrUniversity, "isAdultOrUniversity");
__name2(isAdultOrUniversity, "isAdultOrUniversity");
function buildProposeCurriculumMessages(payload) {
  const {
    goal = "",
    projectBlueprint = null,
    projectSpec = null,
    deliverable = "",
    maxProposed = 12
  } = payload;
  const adultOrUni = isAdultOrUniversity(projectSpec, goal);
  const gradeLine = formatGradeConstraint(projectSpec);
  const phases = compactBlueprintPhases(projectBlueprint, 6);
  const ctx = buildCompactUserContext({
    goal,
    projectSpec,
    projectBlueprint,
    deliverable,
    includeBlueprint: false
  });
  const system = `${adultOrUni ? "\u5927\u5B66PBL\u77E5\u8BC6\u70B9\u63D0\u6848" : "K12 PBL\u8BFE\u6807\u63D0\u6848"}\uFF1A\u5217\u5E94\u5B66\u77E5\u8BC6\u70B9\uFF08\u975E\u56FE\u8C31id\uFF09\u3002

\u539F\u5219\uFF1A\u2460\u652F\u6491\u5177\u4F53\u73AF\u8282 \u2461\u6309\u524D\u7F6E\u2192\u65B9\u6CD5\u2192\u6838\u5FC3\u6392\u5E8F(role) \u2462${adultOrUni ? "\u4E13\u4E1A\u8868\u8FF0" : "\u8BFE\u6807\u5E38\u89C1\u8868\u8FF0"} \u2463${gradeLine || (adultOrUni ? "\u6210\u4EBA/\u5927\u5B66" : "K12")} \u2464${Math.max(5, maxProposed - 4)}\u2013${maxProposed}\u4E2A\u5B81\u7CBE\u52FF\u6EE5 \u2465\u7981\u6CDB\u7D20\u517B \u2466\u987B\u4E0E\u76EE\u6807\u6709\u56E0\u679C\u8054\u7CFB \u2467\u7406\u5DE5/\u63A2\u7A76\u7C7B\uFF1A\u539F\u7406\u22652+\u6570\u5B66\u22651\u3002\u53EA\u8FD4\u56DEJSON\u3002`;
  const user = `${ctx}
${phases ? `\u9636\u6BB5:${phases}
` : ""}
\u8FD4\u56DE JSON\uFF1A{"proposed":[{"name":"","subject":"","gradeHint":0,"phase":"","role":"core","reason":""}],"knowledgeChain":"","summary":""}
subject:${adultOrUni ? "computer-science/engineering/physics/info-tech/math" : "math/physics/chemistry/biology/science/chinese/english/history/geography/info-tech"}`;
  return [
    { role: "system", content: system },
    { role: "user", content: user }
  ];
}
__name(buildProposeCurriculumMessages, "buildProposeCurriculumMessages");
__name2(buildProposeCurriculumMessages, "buildProposeCurriculumMessages");
function buildValidateMatchMessages(payload) {
  const {
    goal = "",
    projectBlueprint = null,
    deliverable = "",
    projectSpec = null,
    linked = []
  } = payload;
  const nodeBlock = linked.map((n) => {
    const g = n.grade > 0 ? `G${n.grade}` : "\u62D3\u5C55";
    return `${n.index + 1}.[${n.index}] ${n.name}(${n.subject || "?"}/${g}/${n.role || "core"}) ${n.reason || ""}`;
  }).join("\n");
  const ctx = buildCompactUserContext({ goal, projectSpec, projectBlueprint, deliverable, includeBlueprint: false });
  const phases = compactBlueprintPhases(projectBlueprint, 6);
  const system = `\u8DEF\u5F84\u6821\u9A8C\uFF1A\u5254\u9664\u8DD1\u9898/\u8D85\u9F84\uFF1B\u7F16\u6392pathOrder/dependsOn/projectPhases/external/techRoute\u3002knowledgeNames\u4EC5\u7528\u5DF2\u5BF9\u9F50\u8282\u70B9\u540D\uFF1Bsteps\u22652\u6761\u226515\u5B57\u3002\u53EA\u8FD4\u56DEJSON\u3002`;
  const user = `${ctx}
${phases ? `\u9636\u6BB5:${phases}
` : ""}
\u5DF2\u5BF9\u9F50${linked.length}\u4E2A\uFF1A
${nodeBlock}

\u8FD4\u56DE\uFF1A{"remove":[],"roleUpdates":[],"pathOrder":[],"dependsOn":[],"matched":[],"projectPhases":[],"external":[],"techRoute":"","knowledgeChain":"","summary":""}`;
  return [
    { role: "system", content: system },
    { role: "user", content: user }
  ];
}
__name(buildValidateMatchMessages, "buildValidateMatchMessages");
__name2(buildValidateMatchMessages, "buildValidateMatchMessages");
var MAX_TEXT = 12e4;
function getDb2(env) {
  return env.TEACHANY_DB || env.DB || null;
}
__name(getDb2, "getDb2");
__name2(getDb2, "getDb");
async function sha256Hex2(text) {
  const data = new TextEncoder().encode(String(text || ""));
  const digest = await crypto.subtle.digest("SHA-256", data);
  return Array.from(new Uint8Array(digest)).map((b) => b.toString(16).padStart(2, "0")).join("");
}
__name(sha256Hex2, "sha256Hex2");
__name2(sha256Hex2, "sha256Hex");
async function hashIp2(ip) {
  if (!ip || !crypto?.subtle) return "";
  return (await sha256Hex2(ip)).slice(0, 24);
}
__name(hashIp2, "hashIp2");
__name2(hashIp2, "hashIp");
function clip(text, max = MAX_TEXT) {
  const s = String(text ?? "");
  return s.length > max ? s.slice(0, max) + "\n\u2026[truncated]" : s;
}
__name(clip, "clip");
__name2(clip, "clip");
async function logPBLCall(env, entry) {
  const db = getDb2(env);
  if (!db) {
    console.warn("[PBL Log] D1 not configured, skip persist");
    return null;
  }
  const {
    stage,
    goal,
    model = "",
    backend = "",
    complex = false,
    latencyMs = null,
    error = "",
    messages = [],
    responseText = "",
    request
  } = entry;
  const ipHash = request ? await hashIp2(request.headers.get("CF-Connecting-IP") || "") : "";
  const userAgent = request ? String(request.headers.get("User-Agent") || "").slice(0, 500) : "";
  try {
    const result = await db.prepare(`
      INSERT INTO pbl_llm_logs (
        stage, goal, model, backend, complex, latency_ms, error,
        messages_json, response_text, user_agent, ip_hash
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `).bind(
      String(stage || "").slice(0, 32),
      String(goal || "").slice(0, 2e3),
      String(model || "").slice(0, 120),
      String(backend || "").slice(0, 64),
      complex ? 1 : 0,
      latencyMs == null ? null : Number(latencyMs),
      String(error || "").slice(0, 2e3),
      clip(JSON.stringify(messages)),
      clip(responseText),
      userAgent,
      ipHash
    ).run();
    return result.meta?.last_row_id || null;
  } catch (e) {
    console.error("[PBL Log] insert failed:", e.message);
    return null;
  }
}
__name(logPBLCall, "logPBLCall");
__name2(logPBLCall, "logPBLCall");
function assertLogToken(request, env) {
  const expected = String(env.PBL_LOG_TOKEN || "").trim();
  if (!expected) return { ok: true, protected: false };
  const url = new URL(request.url);
  const provided = String(
    url.searchParams.get("token") || request.headers.get("X-PBL-Log-Token") || ""
  ).trim();
  if (provided !== expected) {
    return { ok: false, status: 403, message: "Invalid or missing PBL log token" };
  }
  return { ok: true, protected: true };
}
__name(assertLogToken, "assertLogToken");
__name2(assertLogToken, "assertLogToken");
async function queryPBLLogs(request, env) {
  const db = getDb2(env);
  if (!db) {
    return {
      status: 503,
      body: {
        ok: false,
        error: "D1_NOT_CONFIGURED",
        message: "PBL \u65E5\u5FD7\u9700\u8981\u7ED1\u5B9A TEACHANY_DB\uFF0C\u5E76\u6267\u884C migrations/0002_pbl_llm_logs.sql"
      }
    };
  }
  const auth = assertLogToken(request, env);
  if (!auth.ok) {
    return { status: auth.status, body: { ok: false, error: "FORBIDDEN", message: auth.message } };
  }
  const url = new URL(request.url);
  const format = url.searchParams.get("format") || "json";
  const limit = Math.min(Math.max(parseInt(url.searchParams.get("limit") || "50", 10), 1), 500);
  const stage = url.searchParams.get("stage") || "";
  const goalLike = url.searchParams.get("goal") || "";
  let query = `SELECT id, created_at, stage, goal, model, backend, complex, latency_ms, error,
    substr(messages_json, 1, 8000) AS messages_json,
    substr(response_text, 1, 8000) AS response_text
    FROM pbl_llm_logs`;
  const binds = [];
  const clauses = [];
  if (stage) {
    clauses.push("stage = ?");
    binds.push(stage);
  }
  if (goalLike) {
    clauses.push("goal LIKE ?");
    binds.push(`%${goalLike}%`);
  }
  if (clauses.length) query += ` WHERE ${clauses.join(" AND ")}`;
  query += " ORDER BY datetime(created_at) DESC LIMIT ?";
  binds.push(limit);
  const result = await db.prepare(query).bind(...binds).all();
  const rows = result.results || [];
  if (format === "ndjson" || format === "jsonl") {
    const lines = rows.map((r) => JSON.stringify(r)).join("\n");
    return {
      status: 200,
      raw: true,
      headers: {
        "Content-Type": "application/x-ndjson; charset=utf-8",
        "Content-Disposition": "attachment; filename=pbl-llm-logs.ndjson"
      },
      body: lines + (lines ? "\n" : "")
    };
  }
  return {
    status: 200,
    body: { ok: true, count: rows.length, rows }
  };
}
__name(queryPBLLogs, "queryPBLLogs");
__name2(queryPBLLogs, "queryPBLLogs");
async function onRequestOptions5() {
  return new Response(null, { status: 204, headers: CORS3 });
}
__name(onRequestOptions5, "onRequestOptions5");
__name2(onRequestOptions5, "onRequestOptions");
async function onRequestPost3(context) {
  const { request, env } = context;
  let body;
  try {
    body = await request.json();
  } catch {
    return jsonResponse2({ error: "Invalid JSON" }, 400);
  }
  const stage = body.stage;
  if (stage !== "decompose" && stage !== "review-decompose" && stage !== "filter" && stage !== "match" && stage !== "propose-curriculum" && stage !== "validate-match" && stage !== "verify-relevance" && stage !== "review-curriculum" && stage !== "verify-deps" && stage !== "refine") {
    return jsonResponse2({ error: "Invalid stage" }, 400);
  }
  const goal = String(body.goal || "").trim();
  if (!goal || goal.length > 2e3) {
    return jsonResponse2({ error: "Invalid goal" }, 400);
  }
  if (stage === "match" && (!Array.isArray(body.candidates) || body.candidates.length === 0)) {
    return jsonResponse2({ error: "candidates required" }, 400);
  }
  if (stage === "match" && body.candidates.length > 50) {
    return jsonResponse2({ error: "Too many candidates" }, 400);
  }
  if (stage === "refine" && !String(body.userMessage || "").trim()) {
    return jsonResponse2({ error: "userMessage required" }, 400);
  }
  if (stage === "review-decompose" && (!body.projectBlueprint || !body.projectBlueprint.schemes?.length)) {
    return jsonResponse2({ error: "projectBlueprint with schemes required" }, 400);
  }
  if (stage === "verify-relevance" && (!Array.isArray(body.matched) || body.matched.length === 0)) {
    return jsonResponse2({ error: "matched required" }, 400);
  }
  if (stage === "verify-relevance" && body.matched.length > 24) {
    return jsonResponse2({ error: "Too many matched" }, 400);
  }
  if (stage === "review-curriculum" && (!Array.isArray(body.nodes) || body.nodes.length === 0)) {
    return jsonResponse2({ error: "nodes required" }, 400);
  }
  if (stage === "review-curriculum" && body.nodes.length > 28) {
    return jsonResponse2({ error: "Too many nodes" }, 400);
  }
  if (stage === "verify-deps" && (!Array.isArray(body.edges) || body.edges.length === 0)) {
    return jsonResponse2({ error: "edges required" }, 400);
  }
  if (stage === "verify-deps" && body.edges.length > 24) {
    return jsonResponse2({ error: "Too many edges" }, 400);
  }
  if (stage === "validate-match" && (!Array.isArray(body.linked) || body.linked.length === 0)) {
    return jsonResponse2({ error: "linked required" }, 400);
  }
  if (stage === "validate-match" && body.linked.length > 24) {
    return jsonResponse2({ error: "Too many linked nodes" }, 400);
  }
  let messages;
  try {
    if (stage === "verify-deps") {
      messages = buildVerifyDepsMessages({ goal, edges: body.edges });
    } else if (stage === "verify-relevance") {
      messages = buildVerifyRelevanceMessages({
        goal,
        deliverable: body.deliverable || "",
        projectBlueprint: body.projectBlueprint || null,
        matched: body.matched || []
      });
    } else if (stage === "review-curriculum") {
      messages = buildReviewCurriculumMessages({
        goal,
        deliverable: body.deliverable || "",
        projectBlueprint: body.projectBlueprint || null,
        projectSpec: body.projectSpec || null,
        nodes: body.nodes || []
      });
    } else if (stage === "propose-curriculum") {
      messages = buildProposeCurriculumMessages({
        goal,
        projectBlueprint: body.projectBlueprint || null,
        projectSpec: body.projectSpec || null,
        deliverable: body.deliverable || "",
        maxProposed: body.maxProposed || (body.complex ? 12 : 14)
      });
    } else if (stage === "validate-match") {
      messages = buildValidateMatchMessages({
        goal,
        projectBlueprint: body.projectBlueprint || null,
        deliverable: body.deliverable || "",
        projectSpec: body.projectSpec || null,
        linked: body.linked || []
      });
    } else if (stage === "refine") {
      messages = buildRefineMessages({
        goal,
        userMessage: body.userMessage || "",
        projectSpec: body.projectSpec || null,
        snapshot: body.snapshot || {}
      });
    } else if (stage === "review-decompose") {
      messages = buildReviewDecomposeMessages({
        goal,
        projectBlueprint: body.projectBlueprint,
        reviewIssues: body.reviewIssues || [],
        complex: !!body.complex,
        projectSpec: body.projectSpec || null
      });
    } else {
      messages = buildPBMessages(stage, {
        goal,
        summaryList: body.summaryList || "",
        candidates: body.candidates || [],
        complex: !!body.complex,
        maxMatched: body.maxMatched || (body.complex ? 12 : 18),
        minConf: body.minConf ?? (body.complex ? 0.68 : 0.52),
        domainHints: body.domainHints || null,
        projectBlueprint: body.projectBlueprint || null,
        bloomProfile: body.bloomProfile || null,
        archetypeId: body.archetypeId || null,
        projectSpec: body.projectSpec || null
      });
    }
  } catch (e) {
    return jsonResponse2({ error: e.message }, 400);
  }
  if (body.messagesOnly) {
    return jsonResponse2({
      messages,
      model: String(body.model || "").trim()
    });
  }
  const llmOpts = {
    maxTokens: stage === "match" ? 8e3 : stage === "validate-match" ? 6e3 : stage === "decompose" || stage === "review-decompose" ? 5e3 : stage === "propose-curriculum" ? 3e3 : stage === "verify-relevance" || stage === "review-curriculum" ? 3500 : stage === "refine" ? 2500 : stage === "verify-deps" ? 2500 : 1200,
    temperature: stage === "match" ? 0.15 : stage === "validate-match" ? 0.1 : stage === "decompose" ? 0.35 : stage === "review-decompose" ? 0.12 : stage === "propose-curriculum" ? 0.25 : stage === "verify-relevance" || stage === "review-curriculum" ? 0.05 : stage === "refine" ? 0.2 : stage === "verify-deps" ? 0.08 : 0.25
  };
  const userModel = String(body.model || "").trim();
  const providerId = String(body.providerId || "").trim();
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
      error: "",
      messages,
      responseText: content,
      request
    });
    return jsonResponse2({ content, model, backend: backendId });
  } catch (e) {
    const latencyMs = Date.now() - t0;
    await logPBLCall(env, {
      stage,
      goal,
      model: "",
      backend: "",
      complex: !!body.complex,
      latencyMs,
      error: e.message || "LLM failed",
      messages,
      responseText: e.body || "",
      request
    });
    const status = e.status && e.status >= 400 && e.status < 600 ? e.status : 502;
    return jsonResponse2({ error: e.message || "LLM failed", detail: e.body || "" }, status);
  }
}
__name(onRequestPost3, "onRequestPost3");
__name2(onRequestPost3, "onRequestPost");
var MAX_PAYLOAD = 48e4;
var TTL_DAYS = 7;
function getDb3(env) {
  return env.TEACHANY_DB || env.DB || null;
}
__name(getDb3, "getDb3");
__name2(getDb3, "getDb");
function clipJson(obj, max = MAX_PAYLOAD) {
  const base = {
    goal: obj.goal,
    spec: obj.spec || null,
    result: {
      goal: obj.result?.goal || obj.goal || "",
      systems: obj.result?.systems || [],
      techRoute: obj.result?.techRoute || "",
      moduleChain: obj.result?.moduleChain || "",
      projectBlueprint: obj.result?.projectBlueprint || null,
      projectPhases: obj.result?.projectPhases || [],
      projectSpec: obj.result?.projectSpec || null,
      pathPlan: obj.result?.pathPlan || null,
      stats: obj.result?.stats || null,
      quality: obj.result?.quality || null,
      relevanceAudit: obj.result?.relevanceAudit || null,
      archetype: obj.result?.archetype || null,
      chatHistory: (obj.result?.chatHistory || []).slice(-12),
      graphData: obj.result?.graphData || { nodes: [], links: [] },
      truncated: false
    }
  };
  let s = JSON.stringify(base);
  if (s.length <= max) return s;
  const gd = base.result.graphData;
  const tiers = [60, 45, 35, 28, 22];
  for (const n of tiers) {
    base.result.graphData = {
      nodes: (gd.nodes || []).slice(0, n),
      links: (gd.links || []).slice(0, Math.min(n * 2, (gd.links || []).length))
    };
    base.result.truncated = true;
    s = JSON.stringify(base);
    if (s.length <= max) return s;
  }
  base.result.chatHistory = [];
  s = JSON.stringify(base);
  if (s.length <= max) return s;
  base.result.graphData = {
    nodes: (gd.nodes || []).slice(0, 15),
    links: (gd.links || []).slice(0, 30)
  };
  return JSON.stringify(base);
}
__name(clipJson, "clipJson");
__name2(clipJson, "clipJson");
function addDaysIso(days) {
  const d = /* @__PURE__ */ new Date();
  d.setUTCDate(d.getUTCDate() + days);
  return d.toISOString().slice(0, 19).replace("T", " ");
}
__name(addDaysIso, "addDaysIso");
__name2(addDaysIso, "addDaysIso");
async function createPBLHandoff(env, payload) {
  const db = getDb3(env);
  if (!db) return { ok: false, status: 503, body: { error: "D1_NOT_CONFIGURED", message: "PBL handoff \u9700\u8981\u7ED1\u5B9A TEACHANY_DB" } };
  const goal = String(payload?.goal || payload?.result?.goal || "").trim();
  if (!goal || !payload?.result) {
    return { ok: false, status: 400, body: { error: "INVALID_PAYLOAD", message: "\u7F3A\u5C11 goal \u6216 result" } };
  }
  const id = crypto.randomUUID();
  const expiresAt = addDaysIso(TTL_DAYS);
  const json3 = clipJson({ goal, result: payload.result, spec: payload.spec || null });
  await db.prepare(
    "INSERT INTO pbl_handoffs (id, expires_at, goal, payload_json) VALUES (?, ?, ?, ?)"
  ).bind(id, expiresAt, goal.slice(0, 2e3), json3).run();
  return { ok: true, status: 200, body: { id, expiresAt, goal, hasBlueprint: !!payload.result?.projectBlueprint?.schemes?.length } };
}
__name(createPBLHandoff, "createPBLHandoff");
__name2(createPBLHandoff, "createPBLHandoff");
async function getPBLHandoff(env, id) {
  const db = getDb3(env);
  if (!db) return { ok: false, status: 503, body: { error: "D1_NOT_CONFIGURED" } };
  const handoffId = String(id || "").trim();
  if (!handoffId) return { ok: false, status: 400, body: { error: "MISSING_ID" } };
  const row = await db.prepare(
    "SELECT id, goal, payload_json, expires_at FROM pbl_handoffs WHERE id = ? AND expires_at > datetime('now')"
  ).bind(handoffId).first();
  if (!row) return { ok: false, status: 404, body: { error: "NOT_FOUND", message: "\u4EA4\u63A5\u8BB0\u5F55\u4E0D\u5B58\u5728\u6216\u5DF2\u8FC7\u671F" } };
  let payload;
  try {
    payload = JSON.parse(row.payload_json);
  } catch {
    return { ok: false, status: 500, body: { error: "CORRUPT_PAYLOAD" } };
  }
  return {
    ok: true,
    status: 200,
    body: {
      id: row.id,
      goal: row.goal,
      expiresAt: row.expires_at,
      result: payload.result,
      spec: payload.spec || null
    }
  };
}
__name(getPBLHandoff, "getPBLHandoff");
__name2(getPBLHandoff, "getPBLHandoff");
async function onRequestOptions6() {
  return new Response(null, { status: 204, headers: CORS3 });
}
__name(onRequestOptions6, "onRequestOptions6");
__name2(onRequestOptions6, "onRequestOptions");
async function onRequestPost4(context) {
  const { request, env } = context;
  let body;
  try {
    body = await request.json();
  } catch {
    return json2({ error: "INVALID_JSON" }, 400);
  }
  const out = await createPBLHandoff(env, body);
  return json2(out.body, out.status);
}
__name(onRequestPost4, "onRequestPost4");
__name2(onRequestPost4, "onRequestPost");
async function onRequestGet4(context) {
  const { request, env } = context;
  const id = new URL(request.url).searchParams.get("id");
  const out = await getPBLHandoff(env, id);
  return json2(out.body, out.status);
}
__name(onRequestGet4, "onRequestGet4");
__name2(onRequestGet4, "onRequestGet");
function json2(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...CORS3 }
  });
}
__name(json2, "json2");
__name2(json2, "json");
async function onRequestOptions7() {
  return new Response(null, { status: 204, headers: CORS3 });
}
__name(onRequestOptions7, "onRequestOptions7");
__name2(onRequestOptions7, "onRequestOptions");
async function onRequestGet5(context) {
  const { request, env } = context;
  const result = await queryPBLLogs(request, env);
  if (result.raw) {
    return new Response(result.body, {
      status: result.status,
      headers: { ...CORS3, ...result.headers }
    });
  }
  return new Response(JSON.stringify(result.body, null, 2), {
    status: result.status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...CORS3 }
  });
}
__name(onRequestGet5, "onRequestGet5");
__name2(onRequestGet5, "onRequestGet");
var CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
  "Cache-Control": "no-store"
};
function jsonResponse3(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: {
      ...CORS_HEADERS,
      "Content-Type": "application/json; charset=utf-8"
    }
  });
}
__name(jsonResponse3, "jsonResponse3");
__name2(jsonResponse3, "jsonResponse");
function csvEscape(value) {
  if (value === null || value === void 0) return "";
  const text = String(value);
  if (/[,"\n\r]/.test(text)) return `"${text.replace(/"/g, '""')}"`;
  return text;
}
__name(csvEscape, "csvEscape");
__name2(csvEscape, "csvEscape");
function getDb4(env) {
  return env.TEACHANY_DB || env.DB || env.FEEDBACK_DB || null;
}
__name(getDb4, "getDb4");
__name2(getDb4, "getDb");
async function sha256Hex3(text) {
  const encoder = new TextEncoder();
  const data = encoder.encode(String(text || ""));
  const digest = await crypto.subtle.digest("SHA-256", data);
  return Array.from(new Uint8Array(digest)).map((b) => b.toString(16).padStart(2, "0")).join("");
}
__name(sha256Hex3, "sha256Hex3");
__name2(sha256Hex3, "sha256Hex");
async function hashIp3(ip) {
  if (!ip || !crypto?.subtle) return "";
  return (await sha256Hex3(ip)).slice(0, 24);
}
__name(hashIp3, "hashIp3");
__name2(hashIp3, "hashIp");
function getFeedbackConfigFromManifest(manifest) {
  const cfg = manifest?.feedback || {};
  return {
    passwordSha256: String(cfg.password_sha256 || manifest?.feedback_password_sha256 || "").trim().toLowerCase(),
    passwordHint: String(cfg.password_hint || manifest?.feedback_password_hint || "").trim(),
    requirePassword: Boolean(cfg.require_password || cfg.password_sha256 || manifest?.feedback_password_sha256)
  };
}
__name(getFeedbackConfigFromManifest, "getFeedbackConfigFromManifest");
__name2(getFeedbackConfigFromManifest, "getFeedbackConfigFromManifest");
async function loadCourseManifest(request, courseId) {
  if (!courseId) return null;
  const origin = new URL(request.url).origin;
  let path = `community/${courseId}`;
  try {
    const regRes = await fetch(`${origin}/registry.json`, { cf: { cacheTtl: 60 } });
    if (regRes.ok) {
      const registry = await regRes.json();
      const course = (registry.courses || []).find((item) => item.id === courseId || item.course_id === courseId);
      if (course && course.path) path = String(course.path).replace(/^\/+|\/+$/g, "");
    }
  } catch (error) {
  }
  try {
    const res = await fetch(`${origin}/${path}/manifest.json`, { cf: { cacheTtl: 60 } });
    if (!res.ok) return null;
    return await res.json();
  } catch (error) {
    return null;
  }
}
__name(loadCourseManifest, "loadCourseManifest");
__name2(loadCourseManifest, "loadCourseManifest");
async function assertFeedbackPassword(request, courseId, body) {
  const manifest = await loadCourseManifest(request, courseId);
  const cfg = getFeedbackConfigFromManifest(manifest);
  if (!cfg.requirePassword || !cfg.passwordSha256) {
    return { ok: true, passwordProtected: false };
  }
  const provided = String(body.feedback_password || body.feedbackPassword || "").trim();
  if (!provided) {
    return {
      ok: false,
      status: 403,
      body: {
        ok: false,
        error: "FEEDBACK_PASSWORD_REQUIRED",
        message: cfg.passwordHint ? `\u672C\u8BFE\u4EF6\u9700\u8981\u53CD\u9988\u5BC6\u7801\u3002\u63D0\u793A\uFF1A${cfg.passwordHint}` : "\u672C\u8BFE\u4EF6\u9700\u8981\u53CD\u9988\u5BC6\u7801\uFF0C\u8BF7\u5411\u8001\u5E08\u83B7\u53D6\u3002",
        password_required: true,
        password_hint: cfg.passwordHint
      }
    };
  }
  const actual = await sha256Hex3(provided);
  if (actual !== cfg.passwordSha256) {
    return {
      ok: false,
      status: 403,
      body: {
        ok: false,
        error: "INVALID_FEEDBACK_PASSWORD",
        message: "\u53CD\u9988\u5BC6\u7801\u4E0D\u6B63\u786E\uFF0C\u8BF7\u5411\u8001\u5E08\u786E\u8BA4\u540E\u518D\u63D0\u4EA4\u3002",
        password_required: true,
        password_hint: cfg.passwordHint
      }
    };
  }
  return { ok: true, passwordProtected: true };
}
__name(assertFeedbackPassword, "assertFeedbackPassword");
__name2(assertFeedbackPassword, "assertFeedbackPassword");
function sanitizeRawBody(body) {
  const copy = { ...body };
  delete copy.feedback_password;
  delete copy.feedbackPassword;
  return copy;
}
__name(sanitizeRawBody, "sanitizeRawBody");
__name2(sanitizeRawBody, "sanitizeRawBody");
async function handlePost(request, env) {
  const db = getDb4(env);
  if (!db) {
    return jsonResponse3({
      ok: false,
      error: "D1_NOT_CONFIGURED",
      message: "TeachAny Feedback API \u5DF2\u90E8\u7F72\uFF0C\u4F46\u8FD8\u6CA1\u6709\u7ED1\u5B9A Cloudflare D1 \u6570\u636E\u5E93\u3002\u8BF7\u5728 Pages \u9879\u76EE\u4E2D\u7ED1\u5B9A\u53D8\u91CF\u540D TEACHANY_DB\u3002"
    }, 503);
  }
  let body;
  try {
    body = await request.json();
  } catch (error) {
    return jsonResponse3({ ok: false, error: "INVALID_JSON", message: "\u8BF7\u6C42\u4F53\u9700\u8981\u662F JSON\u3002" }, 400);
  }
  const courseId = String(body.course_id || body.courseId || "").trim();
  if (!courseId) {
    return jsonResponse3({ ok: false, error: "MISSING_COURSE_ID", message: "\u7F3A\u5C11 course_id\u3002" }, 400);
  }
  const passwordCheck = await assertFeedbackPassword(request, courseId, body);
  if (!passwordCheck.ok) return jsonResponse3(passwordCheck.body, passwordCheck.status);
  const understood = body.understood === true || body.understood === "true" || body.understood === "yes" ? 1 : 0;
  const ipHash = await hashIp3(request.headers.get("CF-Connecting-IP") || "");
  const rawJson = JSON.stringify(sanitizeRawBody(body)).slice(0, 12e3);
  const stmt = db.prepare(`
    INSERT INTO feedback_entries (
      course_id, course_name, node_id, subject, grade,
      learner_name, class_name, understood, difficulty,
      pre_score, post_score, hardest_part, reflection, contact,
      user_agent, ip_hash, raw_json
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `).bind(
    courseId,
    String(body.course_name || body.courseName || "").slice(0, 200),
    String(body.node_id || body.nodeId || "").slice(0, 120),
    String(body.subject || "").slice(0, 80),
    String(body.grade || "").slice(0, 40),
    String(body.learner_name || body.learnerName || "").slice(0, 120),
    String(body.class_name || body.className || "").slice(0, 120),
    understood,
    String(body.difficulty || "").slice(0, 40),
    body.pre_score === "" || body.pre_score === void 0 ? null : Number(body.pre_score),
    body.post_score === "" || body.post_score === void 0 ? null : Number(body.post_score),
    String(body.hardest_part || body.hardestPart || "").slice(0, 1e3),
    String(body.reflection || "").slice(0, 2e3),
    String(body.contact || "").slice(0, 200),
    String(request.headers.get("User-Agent") || "").slice(0, 500),
    ipHash,
    rawJson
  );
  const result = await stmt.run();
  return jsonResponse3({ ok: true, id: result.meta?.last_row_id || null, password_protected: passwordCheck.passwordProtected });
}
__name(handlePost, "handlePost");
__name2(handlePost, "handlePost");
async function handleGet(request, env) {
  const db = getDb4(env);
  if (!db) {
    return jsonResponse3({
      ok: false,
      error: "D1_NOT_CONFIGURED",
      message: "TeachAny Feedback API \u5DF2\u90E8\u7F72\uFF0C\u4F46\u8FD8\u6CA1\u6709\u7ED1\u5B9A Cloudflare D1 \u6570\u636E\u5E93\u3002\u8BF7\u5728 Pages \u9879\u76EE\u4E2D\u7ED1\u5B9A\u53D8\u91CF\u540D TEACHANY_DB\u3002"
    }, 503);
  }
  const url = new URL(request.url);
  const courseId = url.searchParams.get("course_id") || "";
  const format = url.searchParams.get("format") || "json";
  const limit = Math.min(Math.max(parseInt(url.searchParams.get("limit") || "100", 10), 1), 1e3);
  let query = "SELECT id, created_at, course_id, course_name, node_id, subject, grade, learner_name, class_name, understood, difficulty, pre_score, post_score, hardest_part, reflection, contact FROM feedback_entries";
  const binds = [];
  if (courseId) {
    query += " WHERE course_id = ?";
    binds.push(courseId);
  }
  query += " ORDER BY datetime(created_at) DESC LIMIT ?";
  binds.push(limit);
  const result = await db.prepare(query).bind(...binds).all();
  const rows = result.results || [];
  if (format === "csv") {
    const fields = ["id", "created_at", "course_id", "course_name", "node_id", "subject", "grade", "learner_name", "class_name", "understood", "difficulty", "pre_score", "post_score", "hardest_part", "reflection", "contact"];
    const csv = [fields.join(",")].concat(rows.map((row) => fields.map((field) => csvEscape(row[field])).join(","))).join("\n");
    return new Response(csv, {
      headers: {
        ...CORS_HEADERS,
        "Content-Type": "text/csv; charset=utf-8",
        "Content-Disposition": "attachment; filename=teachany-feedback.csv"
      }
    });
  }
  return jsonResponse3({ ok: true, count: rows.length, rows });
}
__name(handleGet, "handleGet");
__name2(handleGet, "handleGet");
async function onRequest(context) {
  const { request, env } = context;
  if (request.method === "OPTIONS") return new Response(null, { headers: CORS_HEADERS });
  if (request.method === "POST") return handlePost(request, env);
  if (request.method === "GET") return handleGet(request, env);
  return jsonResponse3({ ok: false, error: "METHOD_NOT_ALLOWED" }, 405);
}
__name(onRequest, "onRequest");
__name2(onRequest, "onRequest");
var routes = [
  {
    routePath: "/api/llm/chat/completions",
    mountPath: "/api/llm/chat",
    method: "GET",
    middlewares: [],
    modules: [onRequestGet]
  },
  {
    routePath: "/api/llm/chat/completions",
    mountPath: "/api/llm/chat",
    method: "OPTIONS",
    middlewares: [],
    modules: [onRequestOptions]
  },
  {
    routePath: "/api/llm/chat/completions",
    mountPath: "/api/llm/chat",
    method: "POST",
    middlewares: [],
    modules: [onRequestPost]
  },
  {
    routePath: "/api/images/agnes",
    mountPath: "/api/images",
    method: "OPTIONS",
    middlewares: [],
    modules: [onRequestOptions2]
  },
  {
    routePath: "/api/images/agnes",
    mountPath: "/api/images",
    method: "POST",
    middlewares: [],
    modules: [onRequestPost2]
  },
  {
    routePath: "/api/images/quota",
    mountPath: "/api/images",
    method: "GET",
    middlewares: [],
    modules: [onRequestGet2]
  },
  {
    routePath: "/api/images/quota",
    mountPath: "/api/images",
    method: "OPTIONS",
    middlewares: [],
    modules: [onRequestOptions3]
  },
  {
    routePath: "/api/llm/credits",
    mountPath: "/api/llm",
    method: "GET",
    middlewares: [],
    modules: [onRequestGet3]
  },
  {
    routePath: "/api/llm/credits",
    mountPath: "/api/llm",
    method: "OPTIONS",
    middlewares: [],
    modules: [onRequestOptions4]
  },
  {
    routePath: "/api/pbl/analyze",
    mountPath: "/api/pbl",
    method: "OPTIONS",
    middlewares: [],
    modules: [onRequestOptions5]
  },
  {
    routePath: "/api/pbl/analyze",
    mountPath: "/api/pbl",
    method: "POST",
    middlewares: [],
    modules: [onRequestPost3]
  },
  {
    routePath: "/api/pbl/handoff",
    mountPath: "/api/pbl",
    method: "GET",
    middlewares: [],
    modules: [onRequestGet4]
  },
  {
    routePath: "/api/pbl/handoff",
    mountPath: "/api/pbl",
    method: "OPTIONS",
    middlewares: [],
    modules: [onRequestOptions6]
  },
  {
    routePath: "/api/pbl/handoff",
    mountPath: "/api/pbl",
    method: "POST",
    middlewares: [],
    modules: [onRequestPost4]
  },
  {
    routePath: "/api/pbl/logs",
    mountPath: "/api/pbl",
    method: "GET",
    middlewares: [],
    modules: [onRequestGet5]
  },
  {
    routePath: "/api/pbl/logs",
    mountPath: "/api/pbl",
    method: "OPTIONS",
    middlewares: [],
    modules: [onRequestOptions7]
  },
  {
    routePath: "/api/feedback",
    mountPath: "/api/feedback",
    method: "",
    middlewares: [],
    modules: [onRequest]
  }
];
function lexer(str) {
  var tokens = [];
  var i = 0;
  while (i < str.length) {
    var char = str[i];
    if (char === "*" || char === "+" || char === "?") {
      tokens.push({ type: "MODIFIER", index: i, value: str[i++] });
      continue;
    }
    if (char === "\\") {
      tokens.push({ type: "ESCAPED_CHAR", index: i++, value: str[i++] });
      continue;
    }
    if (char === "{") {
      tokens.push({ type: "OPEN", index: i, value: str[i++] });
      continue;
    }
    if (char === "}") {
      tokens.push({ type: "CLOSE", index: i, value: str[i++] });
      continue;
    }
    if (char === ":") {
      var name = "";
      var j = i + 1;
      while (j < str.length) {
        var code = str.charCodeAt(j);
        if (
          // `0-9`
          code >= 48 && code <= 57 || // `A-Z`
          code >= 65 && code <= 90 || // `a-z`
          code >= 97 && code <= 122 || // `_`
          code === 95
        ) {
          name += str[j++];
          continue;
        }
        break;
      }
      if (!name)
        throw new TypeError("Missing parameter name at ".concat(i));
      tokens.push({ type: "NAME", index: i, value: name });
      i = j;
      continue;
    }
    if (char === "(") {
      var count = 1;
      var pattern = "";
      var j = i + 1;
      if (str[j] === "?") {
        throw new TypeError('Pattern cannot start with "?" at '.concat(j));
      }
      while (j < str.length) {
        if (str[j] === "\\") {
          pattern += str[j++] + str[j++];
          continue;
        }
        if (str[j] === ")") {
          count--;
          if (count === 0) {
            j++;
            break;
          }
        } else if (str[j] === "(") {
          count++;
          if (str[j + 1] !== "?") {
            throw new TypeError("Capturing groups are not allowed at ".concat(j));
          }
        }
        pattern += str[j++];
      }
      if (count)
        throw new TypeError("Unbalanced pattern at ".concat(i));
      if (!pattern)
        throw new TypeError("Missing pattern at ".concat(i));
      tokens.push({ type: "PATTERN", index: i, value: pattern });
      i = j;
      continue;
    }
    tokens.push({ type: "CHAR", index: i, value: str[i++] });
  }
  tokens.push({ type: "END", index: i, value: "" });
  return tokens;
}
__name(lexer, "lexer");
__name2(lexer, "lexer");
function parse(str, options) {
  if (options === void 0) {
    options = {};
  }
  var tokens = lexer(str);
  var _a = options.prefixes, prefixes = _a === void 0 ? "./" : _a, _b = options.delimiter, delimiter = _b === void 0 ? "/#?" : _b;
  var result = [];
  var key = 0;
  var i = 0;
  var path = "";
  var tryConsume = /* @__PURE__ */ __name2(function(type) {
    if (i < tokens.length && tokens[i].type === type)
      return tokens[i++].value;
  }, "tryConsume");
  var mustConsume = /* @__PURE__ */ __name2(function(type) {
    var value2 = tryConsume(type);
    if (value2 !== void 0)
      return value2;
    var _a2 = tokens[i], nextType = _a2.type, index = _a2.index;
    throw new TypeError("Unexpected ".concat(nextType, " at ").concat(index, ", expected ").concat(type));
  }, "mustConsume");
  var consumeText = /* @__PURE__ */ __name2(function() {
    var result2 = "";
    var value2;
    while (value2 = tryConsume("CHAR") || tryConsume("ESCAPED_CHAR")) {
      result2 += value2;
    }
    return result2;
  }, "consumeText");
  var isSafe = /* @__PURE__ */ __name2(function(value2) {
    for (var _i = 0, delimiter_1 = delimiter; _i < delimiter_1.length; _i++) {
      var char2 = delimiter_1[_i];
      if (value2.indexOf(char2) > -1)
        return true;
    }
    return false;
  }, "isSafe");
  var safePattern = /* @__PURE__ */ __name2(function(prefix2) {
    var prev = result[result.length - 1];
    var prevText = prefix2 || (prev && typeof prev === "string" ? prev : "");
    if (prev && !prevText) {
      throw new TypeError('Must have text between two parameters, missing text after "'.concat(prev.name, '"'));
    }
    if (!prevText || isSafe(prevText))
      return "[^".concat(escapeString(delimiter), "]+?");
    return "(?:(?!".concat(escapeString(prevText), ")[^").concat(escapeString(delimiter), "])+?");
  }, "safePattern");
  while (i < tokens.length) {
    var char = tryConsume("CHAR");
    var name = tryConsume("NAME");
    var pattern = tryConsume("PATTERN");
    if (name || pattern) {
      var prefix = char || "";
      if (prefixes.indexOf(prefix) === -1) {
        path += prefix;
        prefix = "";
      }
      if (path) {
        result.push(path);
        path = "";
      }
      result.push({
        name: name || key++,
        prefix,
        suffix: "",
        pattern: pattern || safePattern(prefix),
        modifier: tryConsume("MODIFIER") || ""
      });
      continue;
    }
    var value = char || tryConsume("ESCAPED_CHAR");
    if (value) {
      path += value;
      continue;
    }
    if (path) {
      result.push(path);
      path = "";
    }
    var open = tryConsume("OPEN");
    if (open) {
      var prefix = consumeText();
      var name_1 = tryConsume("NAME") || "";
      var pattern_1 = tryConsume("PATTERN") || "";
      var suffix = consumeText();
      mustConsume("CLOSE");
      result.push({
        name: name_1 || (pattern_1 ? key++ : ""),
        pattern: name_1 && !pattern_1 ? safePattern(prefix) : pattern_1,
        prefix,
        suffix,
        modifier: tryConsume("MODIFIER") || ""
      });
      continue;
    }
    mustConsume("END");
  }
  return result;
}
__name(parse, "parse");
__name2(parse, "parse");
function match(str, options) {
  var keys = [];
  var re = pathToRegexp(str, keys, options);
  return regexpToFunction(re, keys, options);
}
__name(match, "match");
__name2(match, "match");
function regexpToFunction(re, keys, options) {
  if (options === void 0) {
    options = {};
  }
  var _a = options.decode, decode = _a === void 0 ? function(x) {
    return x;
  } : _a;
  return function(pathname) {
    var m = re.exec(pathname);
    if (!m)
      return false;
    var path = m[0], index = m.index;
    var params = /* @__PURE__ */ Object.create(null);
    var _loop_1 = /* @__PURE__ */ __name2(function(i2) {
      if (m[i2] === void 0)
        return "continue";
      var key = keys[i2 - 1];
      if (key.modifier === "*" || key.modifier === "+") {
        params[key.name] = m[i2].split(key.prefix + key.suffix).map(function(value) {
          return decode(value, key);
        });
      } else {
        params[key.name] = decode(m[i2], key);
      }
    }, "_loop_1");
    for (var i = 1; i < m.length; i++) {
      _loop_1(i);
    }
    return { path, index, params };
  };
}
__name(regexpToFunction, "regexpToFunction");
__name2(regexpToFunction, "regexpToFunction");
function escapeString(str) {
  return str.replace(/([.+*?=^!:${}()[\]|/\\])/g, "\\$1");
}
__name(escapeString, "escapeString");
__name2(escapeString, "escapeString");
function flags(options) {
  return options && options.sensitive ? "" : "i";
}
__name(flags, "flags");
__name2(flags, "flags");
function regexpToRegexp(path, keys) {
  if (!keys)
    return path;
  var groupsRegex = /\((?:\?<(.*?)>)?(?!\?)/g;
  var index = 0;
  var execResult = groupsRegex.exec(path.source);
  while (execResult) {
    keys.push({
      // Use parenthesized substring match if available, index otherwise
      name: execResult[1] || index++,
      prefix: "",
      suffix: "",
      modifier: "",
      pattern: ""
    });
    execResult = groupsRegex.exec(path.source);
  }
  return path;
}
__name(regexpToRegexp, "regexpToRegexp");
__name2(regexpToRegexp, "regexpToRegexp");
function arrayToRegexp(paths, keys, options) {
  var parts = paths.map(function(path) {
    return pathToRegexp(path, keys, options).source;
  });
  return new RegExp("(?:".concat(parts.join("|"), ")"), flags(options));
}
__name(arrayToRegexp, "arrayToRegexp");
__name2(arrayToRegexp, "arrayToRegexp");
function stringToRegexp(path, keys, options) {
  return tokensToRegexp(parse(path, options), keys, options);
}
__name(stringToRegexp, "stringToRegexp");
__name2(stringToRegexp, "stringToRegexp");
function tokensToRegexp(tokens, keys, options) {
  if (options === void 0) {
    options = {};
  }
  var _a = options.strict, strict = _a === void 0 ? false : _a, _b = options.start, start = _b === void 0 ? true : _b, _c = options.end, end = _c === void 0 ? true : _c, _d = options.encode, encode = _d === void 0 ? function(x) {
    return x;
  } : _d, _e = options.delimiter, delimiter = _e === void 0 ? "/#?" : _e, _f = options.endsWith, endsWith = _f === void 0 ? "" : _f;
  var endsWithRe = "[".concat(escapeString(endsWith), "]|$");
  var delimiterRe = "[".concat(escapeString(delimiter), "]");
  var route = start ? "^" : "";
  for (var _i = 0, tokens_1 = tokens; _i < tokens_1.length; _i++) {
    var token = tokens_1[_i];
    if (typeof token === "string") {
      route += escapeString(encode(token));
    } else {
      var prefix = escapeString(encode(token.prefix));
      var suffix = escapeString(encode(token.suffix));
      if (token.pattern) {
        if (keys)
          keys.push(token);
        if (prefix || suffix) {
          if (token.modifier === "+" || token.modifier === "*") {
            var mod = token.modifier === "*" ? "?" : "";
            route += "(?:".concat(prefix, "((?:").concat(token.pattern, ")(?:").concat(suffix).concat(prefix, "(?:").concat(token.pattern, "))*)").concat(suffix, ")").concat(mod);
          } else {
            route += "(?:".concat(prefix, "(").concat(token.pattern, ")").concat(suffix, ")").concat(token.modifier);
          }
        } else {
          if (token.modifier === "+" || token.modifier === "*") {
            throw new TypeError('Can not repeat "'.concat(token.name, '" without a prefix and suffix'));
          }
          route += "(".concat(token.pattern, ")").concat(token.modifier);
        }
      } else {
        route += "(?:".concat(prefix).concat(suffix, ")").concat(token.modifier);
      }
    }
  }
  if (end) {
    if (!strict)
      route += "".concat(delimiterRe, "?");
    route += !options.endsWith ? "$" : "(?=".concat(endsWithRe, ")");
  } else {
    var endToken = tokens[tokens.length - 1];
    var isEndDelimited = typeof endToken === "string" ? delimiterRe.indexOf(endToken[endToken.length - 1]) > -1 : endToken === void 0;
    if (!strict) {
      route += "(?:".concat(delimiterRe, "(?=").concat(endsWithRe, "))?");
    }
    if (!isEndDelimited) {
      route += "(?=".concat(delimiterRe, "|").concat(endsWithRe, ")");
    }
  }
  return new RegExp(route, flags(options));
}
__name(tokensToRegexp, "tokensToRegexp");
__name2(tokensToRegexp, "tokensToRegexp");
function pathToRegexp(path, keys, options) {
  if (path instanceof RegExp)
    return regexpToRegexp(path, keys);
  if (Array.isArray(path))
    return arrayToRegexp(path, keys, options);
  return stringToRegexp(path, keys, options);
}
__name(pathToRegexp, "pathToRegexp");
__name2(pathToRegexp, "pathToRegexp");
var escapeRegex = /[.+?^${}()|[\]\\]/g;
function* executeRequest(request) {
  const requestPath = new URL(request.url).pathname;
  for (const route of [...routes].reverse()) {
    if (route.method && route.method !== request.method) {
      continue;
    }
    const routeMatcher = match(route.routePath.replace(escapeRegex, "\\$&"), {
      end: false
    });
    const mountMatcher = match(route.mountPath.replace(escapeRegex, "\\$&"), {
      end: false
    });
    const matchResult = routeMatcher(requestPath);
    const mountMatchResult = mountMatcher(requestPath);
    if (matchResult && mountMatchResult) {
      for (const handler of route.middlewares.flat()) {
        yield {
          handler,
          params: matchResult.params,
          path: mountMatchResult.path
        };
      }
    }
  }
  for (const route of routes) {
    if (route.method && route.method !== request.method) {
      continue;
    }
    const routeMatcher = match(route.routePath.replace(escapeRegex, "\\$&"), {
      end: true
    });
    const mountMatcher = match(route.mountPath.replace(escapeRegex, "\\$&"), {
      end: false
    });
    const matchResult = routeMatcher(requestPath);
    const mountMatchResult = mountMatcher(requestPath);
    if (matchResult && mountMatchResult && route.modules.length) {
      for (const handler of route.modules.flat()) {
        yield {
          handler,
          params: matchResult.params,
          path: matchResult.path
        };
      }
      break;
    }
  }
}
__name(executeRequest, "executeRequest");
__name2(executeRequest, "executeRequest");
var pages_template_worker_default = {
  async fetch(originalRequest, env, workerContext) {
    let request = originalRequest;
    const handlerIterator = executeRequest(request);
    let data = {};
    let isFailOpen = false;
    const next = /* @__PURE__ */ __name2(async (input, init) => {
      if (input !== void 0) {
        let url = input;
        if (typeof input === "string") {
          url = new URL(input, request.url).toString();
        }
        request = new Request(url, init);
      }
      const result = handlerIterator.next();
      if (result.done === false) {
        const { handler, params, path } = result.value;
        const context = {
          request: new Request(request.clone()),
          functionPath: path,
          next,
          params,
          get data() {
            return data;
          },
          set data(value) {
            if (typeof value !== "object" || value === null) {
              throw new Error("context.data must be an object");
            }
            data = value;
          },
          env,
          waitUntil: workerContext.waitUntil.bind(workerContext),
          passThroughOnException: /* @__PURE__ */ __name2(() => {
            isFailOpen = true;
          }, "passThroughOnException")
        };
        const response = await handler(context);
        if (!(response instanceof Response)) {
          throw new Error("Your Pages function should return a Response");
        }
        return cloneResponse(response);
      } else if ("ASSETS") {
        const response = await env["ASSETS"].fetch(request);
        return cloneResponse(response);
      } else {
        const response = await fetch(request);
        return cloneResponse(response);
      }
    }, "next");
    try {
      return await next();
    } catch (error) {
      if (isFailOpen) {
        const response = await env["ASSETS"].fetch(request);
        return cloneResponse(response);
      }
      throw error;
    }
  }
};
var cloneResponse = /* @__PURE__ */ __name2((response) => (
  // https://fetch.spec.whatwg.org/#null-body-status
  new Response(
    [101, 204, 205, 304].includes(response.status) ? null : response.body,
    response
  )
), "cloneResponse");
var drainBody = /* @__PURE__ */ __name2(async (request, env, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env);
  } finally {
    try {
      if (request.body !== null && !request.bodyUsed) {
        const reader = request.body.getReader();
        while (!(await reader.read()).done) {
        }
      }
    } catch (e) {
      console.error("Failed to drain the unused request body.", e);
    }
  }
}, "drainBody");
var middleware_ensure_req_body_drained_default = drainBody;
function reduceError(e) {
  return {
    name: e?.name,
    message: e?.message ?? String(e),
    stack: e?.stack,
    cause: e?.cause === void 0 ? void 0 : reduceError(e.cause)
  };
}
__name(reduceError, "reduceError");
__name2(reduceError, "reduceError");
var jsonError = /* @__PURE__ */ __name2(async (request, env, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env);
  } catch (e) {
    const error = reduceError(e);
    return Response.json(error, {
      status: 500,
      headers: { "MF-Experimental-Error-Stack": "true" }
    });
  }
}, "jsonError");
var middleware_miniflare3_json_error_default = jsonError;
var __INTERNAL_WRANGLER_MIDDLEWARE__ = [
  middleware_ensure_req_body_drained_default,
  middleware_miniflare3_json_error_default
];
var middleware_insertion_facade_default = pages_template_worker_default;
var __facade_middleware__ = [];
function __facade_register__(...args) {
  __facade_middleware__.push(...args.flat());
}
__name(__facade_register__, "__facade_register__");
__name2(__facade_register__, "__facade_register__");
function __facade_invokeChain__(request, env, ctx, dispatch, middlewareChain) {
  const [head, ...tail] = middlewareChain;
  const middlewareCtx = {
    dispatch,
    next(newRequest, newEnv) {
      return __facade_invokeChain__(newRequest, newEnv, ctx, dispatch, tail);
    }
  };
  return head(request, env, ctx, middlewareCtx);
}
__name(__facade_invokeChain__, "__facade_invokeChain__");
__name2(__facade_invokeChain__, "__facade_invokeChain__");
function __facade_invoke__(request, env, ctx, dispatch, finalMiddleware) {
  return __facade_invokeChain__(request, env, ctx, dispatch, [
    ...__facade_middleware__,
    finalMiddleware
  ]);
}
__name(__facade_invoke__, "__facade_invoke__");
__name2(__facade_invoke__, "__facade_invoke__");
var __Facade_ScheduledController__ = class ___Facade_ScheduledController__ {
  static {
    __name(this, "___Facade_ScheduledController__");
  }
  constructor(scheduledTime, cron, noRetry) {
    this.scheduledTime = scheduledTime;
    this.cron = cron;
    this.#noRetry = noRetry;
  }
  static {
    __name2(this, "__Facade_ScheduledController__");
  }
  #noRetry;
  noRetry() {
    if (!(this instanceof ___Facade_ScheduledController__)) {
      throw new TypeError("Illegal invocation");
    }
    this.#noRetry();
  }
};
function wrapExportedHandler(worker) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__ === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__.length === 0) {
    return worker;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__) {
    __facade_register__(middleware);
  }
  const fetchDispatcher = /* @__PURE__ */ __name2(function(request, env, ctx) {
    if (worker.fetch === void 0) {
      throw new Error("Handler does not export a fetch() function.");
    }
    return worker.fetch(request, env, ctx);
  }, "fetchDispatcher");
  return {
    ...worker,
    fetch(request, env, ctx) {
      const dispatcher = /* @__PURE__ */ __name2(function(type, init) {
        if (type === "scheduled" && worker.scheduled !== void 0) {
          const controller = new __Facade_ScheduledController__(
            Date.now(),
            init.cron ?? "",
            () => {
            }
          );
          return worker.scheduled(controller, env, ctx);
        }
      }, "dispatcher");
      return __facade_invoke__(request, env, ctx, dispatcher, fetchDispatcher);
    }
  };
}
__name(wrapExportedHandler, "wrapExportedHandler");
__name2(wrapExportedHandler, "wrapExportedHandler");
function wrapWorkerEntrypoint(klass) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__ === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__.length === 0) {
    return klass;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__) {
    __facade_register__(middleware);
  }
  return class extends klass {
    #fetchDispatcher = /* @__PURE__ */ __name2((request, env, ctx) => {
      this.env = env;
      this.ctx = ctx;
      if (super.fetch === void 0) {
        throw new Error("Entrypoint class does not define a fetch() function.");
      }
      return super.fetch(request);
    }, "#fetchDispatcher");
    #dispatcher = /* @__PURE__ */ __name2((type, init) => {
      if (type === "scheduled" && super.scheduled !== void 0) {
        const controller = new __Facade_ScheduledController__(
          Date.now(),
          init.cron ?? "",
          () => {
          }
        );
        return super.scheduled(controller);
      }
    }, "#dispatcher");
    fetch(request) {
      return __facade_invoke__(
        request,
        this.env,
        this.ctx,
        this.#dispatcher,
        this.#fetchDispatcher
      );
    }
  };
}
__name(wrapWorkerEntrypoint, "wrapWorkerEntrypoint");
__name2(wrapWorkerEntrypoint, "wrapWorkerEntrypoint");
var WRAPPED_ENTRY;
if (typeof middleware_insertion_facade_default === "object") {
  WRAPPED_ENTRY = wrapExportedHandler(middleware_insertion_facade_default);
} else if (typeof middleware_insertion_facade_default === "function") {
  WRAPPED_ENTRY = wrapWorkerEntrypoint(middleware_insertion_facade_default);
}
var middleware_loader_entry_default = WRAPPED_ENTRY;

// ../../../../../opt/homebrew/lib/node_modules/wrangler/templates/middleware/middleware-ensure-req-body-drained.ts
var drainBody2 = /* @__PURE__ */ __name(async (request, env, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env);
  } finally {
    try {
      if (request.body !== null && !request.bodyUsed) {
        const reader = request.body.getReader();
        while (!(await reader.read()).done) {
        }
      }
    } catch (e) {
      console.error("Failed to drain the unused request body.", e);
    }
  }
}, "drainBody");
var middleware_ensure_req_body_drained_default2 = drainBody2;

// ../../../../../opt/homebrew/lib/node_modules/wrangler/templates/middleware/middleware-miniflare3-json-error.ts
function reduceError2(e) {
  return {
    name: e?.name,
    message: e?.message ?? String(e),
    stack: e?.stack,
    cause: e?.cause === void 0 ? void 0 : reduceError2(e.cause)
  };
}
__name(reduceError2, "reduceError");
var jsonError2 = /* @__PURE__ */ __name(async (request, env, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env);
  } catch (e) {
    const error = reduceError2(e);
    return Response.json(error, {
      status: 500,
      headers: { "MF-Experimental-Error-Stack": "true" }
    });
  }
}, "jsonError");
var middleware_miniflare3_json_error_default2 = jsonError2;

// .wrangler/tmp/bundle-rJaldm/middleware-insertion-facade.js
var __INTERNAL_WRANGLER_MIDDLEWARE__2 = [
  middleware_ensure_req_body_drained_default2,
  middleware_miniflare3_json_error_default2
];
var middleware_insertion_facade_default2 = middleware_loader_entry_default;

// ../../../../../opt/homebrew/lib/node_modules/wrangler/templates/middleware/common.ts
var __facade_middleware__2 = [];
function __facade_register__2(...args) {
  __facade_middleware__2.push(...args.flat());
}
__name(__facade_register__2, "__facade_register__");
function __facade_invokeChain__2(request, env, ctx, dispatch, middlewareChain) {
  const [head, ...tail] = middlewareChain;
  const middlewareCtx = {
    dispatch,
    next(newRequest, newEnv) {
      return __facade_invokeChain__2(newRequest, newEnv, ctx, dispatch, tail);
    }
  };
  return head(request, env, ctx, middlewareCtx);
}
__name(__facade_invokeChain__2, "__facade_invokeChain__");
function __facade_invoke__2(request, env, ctx, dispatch, finalMiddleware) {
  return __facade_invokeChain__2(request, env, ctx, dispatch, [
    ...__facade_middleware__2,
    finalMiddleware
  ]);
}
__name(__facade_invoke__2, "__facade_invoke__");

// .wrangler/tmp/bundle-rJaldm/middleware-loader.entry.ts
var __Facade_ScheduledController__2 = class ___Facade_ScheduledController__2 {
  constructor(scheduledTime, cron, noRetry) {
    this.scheduledTime = scheduledTime;
    this.cron = cron;
    this.#noRetry = noRetry;
  }
  static {
    __name(this, "__Facade_ScheduledController__");
  }
  #noRetry;
  noRetry() {
    if (!(this instanceof ___Facade_ScheduledController__2)) {
      throw new TypeError("Illegal invocation");
    }
    this.#noRetry();
  }
};
function wrapExportedHandler2(worker) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__2 === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__2.length === 0) {
    return worker;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__2) {
    __facade_register__2(middleware);
  }
  const fetchDispatcher = /* @__PURE__ */ __name(function(request, env, ctx) {
    if (worker.fetch === void 0) {
      throw new Error("Handler does not export a fetch() function.");
    }
    return worker.fetch(request, env, ctx);
  }, "fetchDispatcher");
  return {
    ...worker,
    fetch(request, env, ctx) {
      const dispatcher = /* @__PURE__ */ __name(function(type, init) {
        if (type === "scheduled" && worker.scheduled !== void 0) {
          const controller = new __Facade_ScheduledController__2(
            Date.now(),
            init.cron ?? "",
            () => {
            }
          );
          return worker.scheduled(controller, env, ctx);
        }
      }, "dispatcher");
      return __facade_invoke__2(request, env, ctx, dispatcher, fetchDispatcher);
    }
  };
}
__name(wrapExportedHandler2, "wrapExportedHandler");
function wrapWorkerEntrypoint2(klass) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__2 === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__2.length === 0) {
    return klass;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__2) {
    __facade_register__2(middleware);
  }
  return class extends klass {
    #fetchDispatcher = /* @__PURE__ */ __name((request, env, ctx) => {
      this.env = env;
      this.ctx = ctx;
      if (super.fetch === void 0) {
        throw new Error("Entrypoint class does not define a fetch() function.");
      }
      return super.fetch(request);
    }, "#fetchDispatcher");
    #dispatcher = /* @__PURE__ */ __name((type, init) => {
      if (type === "scheduled" && super.scheduled !== void 0) {
        const controller = new __Facade_ScheduledController__2(
          Date.now(),
          init.cron ?? "",
          () => {
          }
        );
        return super.scheduled(controller);
      }
    }, "#dispatcher");
    fetch(request) {
      return __facade_invoke__2(
        request,
        this.env,
        this.ctx,
        this.#dispatcher,
        this.#fetchDispatcher
      );
    }
  };
}
__name(wrapWorkerEntrypoint2, "wrapWorkerEntrypoint");
var WRAPPED_ENTRY2;
if (typeof middleware_insertion_facade_default2 === "object") {
  WRAPPED_ENTRY2 = wrapExportedHandler2(middleware_insertion_facade_default2);
} else if (typeof middleware_insertion_facade_default2 === "function") {
  WRAPPED_ENTRY2 = wrapWorkerEntrypoint2(middleware_insertion_facade_default2);
}
var middleware_loader_entry_default2 = WRAPPED_ENTRY2;
export {
  __INTERNAL_WRANGLER_MIDDLEWARE__2 as __INTERNAL_WRANGLER_MIDDLEWARE__,
  middleware_loader_entry_default2 as default
};
//# sourceMappingURL=functionsWorker-0.07618563978931547.js.map
