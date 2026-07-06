/**
 * TeachAny 课件生图配额查询
 * GET /api/images/quota?course_id=math-linear-function
 * GET /api/images/quota  （服务状态，不扣额度）
 */

import {
  CORS,
  jsonResponse,
  getDb,
  getPerCourseLimit,
  getIpRpmLimit,
  normalizeCourseId,
  getCourseQuota,
  AGNES_MODEL,
} from '../../_lib/agnes-image.js';

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}

export async function onRequestGet(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const rawCourseId = url.searchParams.get('course_id') || url.searchParams.get('courseId') || '';
  const perCourseLimit = getPerCourseLimit(env);
  const ipRpmLimit = getIpRpmLimit(env);
  const agnesConfigured = Boolean(String(env.AGNES_API_KEY || '').trim());
  const db = getDb(env);

  if (!rawCourseId) {
    return jsonResponse({
      ok: true,
      service: 'teachany-image-agnes',
      model: AGNES_MODEL,
      per_course_limit: perCourseLimit,
      ip_rpm_limit: ipRpmLimit,
      agnes_configured: agnesConfigured,
      d1_configured: Boolean(db),
      endpoint: '/api/images/agnes',
      usage: 'POST { course_id, prompt, size?, slot? } — 无需用户 API Key',
    });
  }

  if (!db) {
    return jsonResponse({
      ok: false,
      error: 'D1_NOT_CONFIGURED',
      message: '配额查询需要 TEACHANY_DB',
      agnes_configured: agnesConfigured,
    }, 503);
  }

  const courseId = normalizeCourseId(rawCourseId);
  if (!courseId) {
    return jsonResponse({
      ok: false,
      error: 'INVALID_COURSE_ID',
      message: 'course_id 格式无效',
    }, 400);
  }

  const quota = await getCourseQuota(db, courseId, perCourseLimit);
  return jsonResponse({
    ok: true,
    course_id: courseId,
    used: quota.used,
    remaining: quota.remaining,
    limit: quota.limit,
    model: AGNES_MODEL,
  });
}
