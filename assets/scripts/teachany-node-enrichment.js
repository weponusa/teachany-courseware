/**
 * TeachAny Node Enrichment · 自有增强层运行时
 * -------------------------------------------------
 * 读取 /data/node-enrichment-overlay.json：
 *   - 前置链 hard/soft + reason
 *   - evidence / assessment
 *   - misconceptions（错因诊断）
 *
 * 不修改课标树；仅作运行时叠加。
 */
(function (global) {
  "use strict";

  var OVERLAY_URLS = [
    "/data/node-enrichment-overlay.json",
    "./data/node-enrichment-overlay.json",
    "../data/node-enrichment-overlay.json",
    "../../data/node-enrichment-overlay.json"
  ];

  var state = {
    ready: false,
    loading: null,
    overlay: null,
    error: null
  };

  function fetchFirst(urls) {
    var i = 0;
    function next() {
      if (i >= urls.length) return Promise.reject(new Error("enrichment overlay not found"));
      var url = urls[i++] + (urls[i - 1].indexOf("?") >= 0 ? "&" : "?") + "v=neo-1";
      return fetch(url, { cache: "no-store" }).then(function (r) {
        if (!r.ok) return next();
        return r.json();
      }).catch(function () { return next(); });
    }
    return next();
  }

  function load() {
    if (state.ready && state.overlay) return Promise.resolve(state.overlay);
    if (state.loading) return state.loading;
    state.loading = fetchFirst(OVERLAY_URLS).then(function (data) {
      state.overlay = data || { nodes: {} };
      state.ready = true;
      state.loading = null;
      return state.overlay;
    }).catch(function (err) {
      state.error = err;
      state.overlay = { nodes: {}, version: "empty" };
      state.ready = true;
      state.loading = null;
      console.warn("[TeachAnyNodeEnrichment] overlay load failed:", err && err.message);
      return state.overlay;
    });
    return state.loading;
  }

  function get(nodeId) {
    if (!nodeId || !state.overlay || !state.overlay.nodes) return null;
    return state.overlay.nodes[nodeId] || null;
  }

  function resolveNodeId(hint) {
    if (hint) return String(hint);
    var cfg = global.__TEACHANY_TUTOR_CONFIG__ || {};
    if (cfg.nodeId) return String(cfg.nodeId);
    var meta = document.querySelector('meta[name="teachany-node"]');
    if (meta && meta.content) return meta.content.trim();
    var course = document.querySelector('meta[name="course-id"]');
    if (course && course.content) return course.content.trim();
    return "";
  }

  /** 合并课标前置 ID 列表：hard 优先，再补 soft / 原列表 */
  function mergePrerequisiteIds(nodeId, baseIds) {
    var entry = get(nodeId);
    var base = Array.isArray(baseIds) ? baseIds.slice() : [];
    if (!entry || !Array.isArray(entry.prereqs_enriched) || !entry.prereqs_enriched.length) {
      return { ids: base, enriched: [], hard: base.slice(), soft: [] };
    }
    var hard = [];
    var soft = [];
    var enriched = [];
    entry.prereqs_enriched.forEach(function (e) {
      if (!e || !e.id) return;
      enriched.push(e);
      if (e.strength === "soft") soft.push(e.id);
      else hard.push(e.id);
    });
    var seen = {};
    var ids = [];
    hard.concat(base).concat(soft).forEach(function (id) {
      if (!id || seen[id]) return;
      seen[id] = true;
      ids.push(id);
    });
    return { ids: ids, enriched: enriched, hard: hard, soft: soft };
  }

  function formatTutorBlock(nodeId, lang) {
    var entry = get(nodeId);
    if (!entry) return "";
    lang = lang || "zh";
    var lines = [];
    if (lang === "en") {
      if (entry.misconceptions && entry.misconceptions.length) {
        lines.push("Common misconceptions:");
        entry.misconceptions.slice(0, 3).forEach(function (m) {
          lines.push("- Cue: " + (m.cue || "") + " | Hint: " + (m.tutor_hint || m.diagnosis || ""));
        });
      }
      if (entry.prereqs_enriched && entry.prereqs_enriched.length) {
        lines.push("Prerequisite focus:");
        entry.prereqs_enriched.slice(0, 4).forEach(function (e) {
          lines.push("- [" + (e.strength || "hard") + "] " + e.id + ": " + (e.reason || ""));
        });
      }
      if (entry.assessment && entry.assessment.length) {
        lines.push("Quick checks: " + entry.assessment.slice(0, 2).join(" / "));
      }
      return lines.join("\n");
    }

    if (entry.misconceptions && entry.misconceptions.length) {
      lines.push("【错因诊断优先】");
      entry.misconceptions.slice(0, 3).forEach(function (m) {
        lines.push("- 易错：" + (m.cue || "") + "；应对：" + (m.tutor_hint || m.diagnosis || ""));
      });
    }
    if (entry.prereqs_enriched && entry.prereqs_enriched.length) {
      lines.push("【前置链】");
      entry.prereqs_enriched.slice(0, 4).forEach(function (e) {
        var tag = e.strength === "soft" ? "建议" : "必备";
        lines.push("- [" + tag + "] " + (e.reason || e.id));
      });
    }
    if (entry.assessment && entry.assessment.length) {
      lines.push("【最小检测】" + entry.assessment.slice(0, 2).join("；"));
    }
    if (entry.evidence && entry.evidence.length) {
      lines.push("【掌握证据】" + entry.evidence.slice(0, 2).join("；"));
    }
    return lines.join("\n");
  }

  function pathHintsHtml(nodeId) {
    var entry = get(nodeId);
    if (!entry) return "";
    var parts = [];
    if (entry.prereqs_enriched && entry.prereqs_enriched.length) {
      var soft = entry.prereqs_enriched.filter(function (e) { return e.strength === "soft"; });
      var hard = entry.prereqs_enriched.filter(function (e) { return e.strength !== "soft"; });
      if (hard.length) {
        parts.push('<div class="neo-hint neo-hard"><strong>必备前置</strong><ul>' +
          hard.slice(0, 5).map(function (e) {
            return "<li>" + escapeHtml(e.reason || e.id) + "</li>";
          }).join("") + "</ul></div>");
      }
      if (soft.length) {
        parts.push('<div class="neo-hint neo-soft"><strong>建议复习</strong><ul>' +
          soft.slice(0, 4).map(function (e) {
            return "<li>" + escapeHtml(e.reason || e.id) + "</li>";
          }).join("") + "</ul></div>");
      }
    }
    if (entry.misconceptions && entry.misconceptions.length) {
      parts.push('<div class="neo-hint neo-misc"><strong>错因诊断</strong><ul>' +
        entry.misconceptions.slice(0, 3).map(function (m) {
          return "<li><em>" + escapeHtml(m.cue || "") + "</em> — " + escapeHtml(m.diagnosis || m.tutor_hint || "") + "</li>";
        }).join("") + "</ul></div>");
    }
    if (!parts.length) return "";
    return '<div class="neo-path-panel">' + parts.join("") + "</div>";
  }

  function escapeHtml(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  /** 给知识图谱链路加 strength 标注 */
  function annotateLinks(centerId, links) {
    var entry = get(centerId);
    if (!entry || !links || !links.length) return links;
    var map = {};
    (entry.prereqs_enriched || []).forEach(function (e) {
      if (e && e.id) map[e.id] = e.strength || "hard";
    });
    links.forEach(function (l) {
      var sid = typeof l.source === "object" ? l.source.id : l.source;
      var tid = typeof l.target === "object" ? l.target.id : l.target;
      if (tid === centerId && map[sid]) l.strength = map[sid];
      if (sid === centerId && map[tid]) l.strength = map[tid];
    });
    return links;
  }

  var api = {
    load: load,
    get: get,
    resolveNodeId: resolveNodeId,
    mergePrerequisiteIds: mergePrerequisiteIds,
    formatTutorBlock: formatTutorBlock,
    pathHintsHtml: pathHintsHtml,
    annotateLinks: annotateLinks,
    get ready() { return state.ready; },
    get overlay() { return state.overlay; }
  };

  global.TeachAnyNodeEnrichment = api;
  // 预加载
  load();
})(typeof window !== "undefined" ? window : globalThis);
