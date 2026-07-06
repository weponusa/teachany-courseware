/**
 * TeachAny 课件生图中转 — Agnes 免费生图
 * POST /api/images/agnes
 *
 * Body: {
 *   course_id: string,   // 必填，课件 ID（manifest id / 目录名）
 *   prompt: string,      // 必填，英文或中文场景描述（服务端自动追加无文字约束）
 *   size?: "1280x768" | "1024x1024" | "512x512",
 *   slot?: "hero" | "section1" | "section2" | ...
 * }
 *
 * Response: { ok, url, course_id, used, remaining, limit, model, latency_ms }
 */

import {
  CORS,
  jsonResponse,
  getDb,
  getPerCourseLimit,
  getIpRpmLimit,
  normalizeCourseId,
  normalizeSize,
  buildCoursewarePrompt,
  hashIp,
  reserveCourseImageSlot,
  releaseCourseImageSlot,
  logImageGen,
  getIpUsageLastMinute,
  callAgnesImage,
  AGNES_MODEL,
} from '../../_lib/agnes-image.js';

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}

export async function onRequestPost(context) {
  const { request, env } = context;
  const db = getDb(env);
  if (!db) {
    return jsonResponse({
      ok: false,
      error: 'D1_NOT_CONFIGURED',
      message: '课件生图需要绑定 TEACHANY_DB，并执行 migrations/0004_courseware_image_gen.sql',
    }, 503);
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return jsonResponse({ ok: false, error: 'INVALID_JSON' }, 400);
  }

  const courseId = normalizeCourseId(body.course_id || body.courseId);
  if (!courseId) {
    return jsonResponse({
      ok: false,
      error: 'INVALID_COURSE_ID',
      message: 'course_id 须为 3–80 位小写字母数字与连字符（如 math-linear-function）',
    }, 400);
  }

  const prompt = buildCoursewarePrompt(body.prompt);
  if (!prompt || prompt.length < 8) {
    return jsonResponse({
      ok: false,
      error: 'INVALID_PROMPT',
      message: 'prompt 过短，请描述插图场景（坐标系、实验装置、历史场景等）',
    }, 400);
  }

  const size = normalizeSize(body.size);
  const slot = String(body.slot || '').trim().slice(0, 32);
  const perCourseLimit = getPerCourseLimit(env);
  const ipRpmLimit = getIpRpmLimit(env);
  const ip = request.headers.get('CF-Connecting-IP') || '';
  const ipHash = await hashIp(ip);
  const userAgent = String(request.headers.get('User-Agent') || '').slice(0, 500);

  const ipUsage = await getIpUsageLastMinute(db, ipHash, ipRpmLimit);
  if (ipUsage.exceeded) {
    return jsonResponse({
      ok: false,
      error: 'RATE_LIMIT',
      message: `请求过于频繁，请 ${60} 秒后再试（每 IP 每分钟最多 ${ipRpmLimit} 次）`,
      ip_rpm: ipUsage,
    }, 429);
  }

  const reservation = await reserveCourseImageSlot(db, courseId, perCourseLimit);
  if (!reservation.reserved) {
    return jsonResponse({
      ok: false,
      error: 'COURSE_QUOTA_EXCEEDED',
      message: `课件 ${courseId} 已用完生图额度（每课件最多 ${perCourseLimit} 张）`,
      course_id: courseId,
      used: reservation.used,
      remaining: 0,
      limit: perCourseLimit,
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
      userAgent,
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
      note: '请尽快下载 url 到课件 assets/；链接为 Agnes 临时地址',
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
      userAgent,
    });

    const status = e?.status && Number.isFinite(e.status) ? e.status : 502;
    return jsonResponse({
      ok: false,
      error: 'GENERATION_FAILED',
      message: e?.message || '生图失败',
      course_id: courseId,
      latency_ms: latencyMs,
    }, status);
  }
}
