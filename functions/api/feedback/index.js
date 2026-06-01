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

async function hashIp(ip) {
  if (!ip || !crypto?.subtle) return "";
  const encoder = new TextEncoder();
  const data = encoder.encode(ip);
  const digest = await crypto.subtle.digest("SHA-256", data);
  return Array.from(new Uint8Array(digest)).slice(0, 12).map(b => b.toString(16).padStart(2, "0")).join("");
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

  const understood = body.understood === true || body.understood === "true" || body.understood === "yes" ? 1 : 0;
  const ipHash = await hashIp(request.headers.get("CF-Connecting-IP") || "");
  const rawJson = JSON.stringify(body).slice(0, 12000);

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
  return jsonResponse({ ok: true, id: result.meta?.last_row_id || null });
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
