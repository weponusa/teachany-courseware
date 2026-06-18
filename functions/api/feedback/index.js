const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
  "Cache-Control": "no-store"
};

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: {
      ...CORS_HEADERS,
      "Content-Type": "application/json; charset=utf-8"
    }
  });
}

function csvEscape(value) {
  if (value === null || value === undefined) return "";
  const text = String(value);
  if (/[,"\n\r]/.test(text)) return `"${text.replace(/"/g, '""')}"`;
  return text;
}

function getDb(env) {
  return env.TEACHANY_DB || env.DB || env.FEEDBACK_DB || null;
}

async function sha256Hex(text) {
  const encoder = new TextEncoder();
  const data = encoder.encode(String(text || ""));
  const digest = await crypto.subtle.digest("SHA-256", data);
  return Array.from(new Uint8Array(digest)).map(b => b.toString(16).padStart(2, "0")).join("");
}

async function hashIp(ip) {
  if (!ip || !crypto?.subtle) return "";
  return (await sha256Hex(ip)).slice(0, 24);
}

function getFeedbackConfigFromManifest(manifest) {
  const cfg = manifest?.feedback || {};
  return {
    passwordSha256: String(cfg.password_sha256 || manifest?.feedback_password_sha256 || "").trim().toLowerCase(),
    passwordHint: String(cfg.password_hint || manifest?.feedback_password_hint || "").trim(),
    requirePassword: Boolean(cfg.require_password || cfg.password_sha256 || manifest?.feedback_password_sha256)
  };
}

async function loadCourseManifest(request, courseId) {
  if (!courseId) return null;
  const origin = new URL(request.url).origin;
  let path = `community/${courseId}`;
  try {
    const regRes = await fetch(`${origin}/registry.json`, { cf: { cacheTtl: 60 } });
    if (regRes.ok) {
      const registry = await regRes.json();
      const course = (registry.courses || []).find(item => item.id === courseId || item.course_id === courseId);
      if (course && course.path) path = String(course.path).replace(/^\/+|\/+$/g, "");
    }
  } catch (error) {
    // registry 不可用时回退到 community/<courseId>
  }
  try {
    const res = await fetch(`${origin}/${path}/manifest.json`, { cf: { cacheTtl: 60 } });
    if (!res.ok) return null;
    return await res.json();
  } catch (error) {
    return null;
  }
}

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
        message: cfg.passwordHint ? `本课件需要反馈密码。提示：${cfg.passwordHint}` : "本课件需要反馈密码，请向老师获取。",
        password_required: true,
        password_hint: cfg.passwordHint
      }
    };
  }
  const actual = await sha256Hex(provided);
  if (actual !== cfg.passwordSha256) {
    return {
      ok: false,
      status: 403,
      body: {
        ok: false,
        error: "INVALID_FEEDBACK_PASSWORD",
        message: "反馈密码不正确，请向老师确认后再提交。",
        password_required: true,
        password_hint: cfg.passwordHint
      }
    };
  }
  return { ok: true, passwordProtected: true };
}

function sanitizeRawBody(body) {
  const copy = { ...body };
  delete copy.feedback_password;
  delete copy.feedbackPassword;
  return copy;
}

async function handlePost(request, env) {
  const db = getDb(env);
  if (!db) {
    return jsonResponse({
      ok: false,
      error: "D1_NOT_CONFIGURED",
      message: "TeachAny Feedback API 已部署，但还没有绑定 Cloudflare D1 数据库。请在 Pages 项目中绑定变量名 TEACHANY_DB。"
    }, 503);
  }

  let body;
  try {
    body = await request.json();
  } catch (error) {
    return jsonResponse({ ok: false, error: "INVALID_JSON", message: "请求体需要是 JSON。" }, 400);
  }

  const courseId = String(body.course_id || body.courseId || "").trim();
  if (!courseId) {
    return jsonResponse({ ok: false, error: "MISSING_COURSE_ID", message: "缺少 course_id。" }, 400);
  }

  const passwordCheck = await assertFeedbackPassword(request, courseId, body);
  if (!passwordCheck.ok) return jsonResponse(passwordCheck.body, passwordCheck.status);

  const understood = body.understood === true || body.understood === "true" || body.understood === "yes" ? 1 : 0;
  const ipHash = await hashIp(request.headers.get("CF-Connecting-IP") || "");
  const rawJson = JSON.stringify(sanitizeRawBody(body)).slice(0, 12000);

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
    body.pre_score === "" || body.pre_score === undefined ? null : Number(body.pre_score),
    body.post_score === "" || body.post_score === undefined ? null : Number(body.post_score),
    String(body.hardest_part || body.hardestPart || "").slice(0, 1000),
    String(body.reflection || "").slice(0, 2000),
    String(body.contact || "").slice(0, 200),
    String(request.headers.get("User-Agent") || "").slice(0, 500),
    ipHash,
    rawJson
  );

  const result = await stmt.run();
  return jsonResponse({ ok: true, id: result.meta?.last_row_id || null, password_protected: passwordCheck.passwordProtected });
}

async function handleGet(request, env) {
  const db = getDb(env);
  if (!db) {
    return jsonResponse({
      ok: false,
      error: "D1_NOT_CONFIGURED",
      message: "TeachAny Feedback API 已部署，但还没有绑定 Cloudflare D1 数据库。请在 Pages 项目中绑定变量名 TEACHANY_DB。"
    }, 503);
  }

  const url = new URL(request.url);
  const courseId = url.searchParams.get("course_id") || "";
  const format = url.searchParams.get("format") || "json";
  const limit = Math.min(Math.max(parseInt(url.searchParams.get("limit") || "100", 10), 1), 1000);

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
    const csv = [fields.join(",")].concat(rows.map(row => fields.map(field => csvEscape(row[field])).join(","))).join("\n");
    return new Response(csv, {
      headers: {
        ...CORS_HEADERS,
        "Content-Type": "text/csv; charset=utf-8",
        "Content-Disposition": "attachment; filename=teachany-feedback.csv"
      }
    });
  }

  return jsonResponse({ ok: true, count: rows.length, rows });
}

export async function onRequest(context) {
  const { request, env } = context;
  if (request.method === "OPTIONS") return new Response(null, { headers: CORS_HEADERS });
  if (request.method === "POST") return handlePost(request, env);
  if (request.method === "GET") return handleGet(request, env);
  return jsonResponse({ ok: false, error: "METHOD_NOT_ALLOWED" }, 405);
}
