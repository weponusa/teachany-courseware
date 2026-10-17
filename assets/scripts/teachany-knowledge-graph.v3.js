/*! TeachAny Standard Knowledge Graph Module · v2.1
 * --------------------------------------------------
 *  <link rel="stylesheet" href="../../scripts/teachany-knowledge-graph.css">
 *  <div data-teachany-kg="chn-e-compound-vowel">
 *    <canvas class="tkg-fallback-canvas" width="720" height="120"></canvas>
 *  </div>
 *  <script src="../../scripts/teachany-knowledge-graph.js" defer></script>
 *
 *  视觉风格：完全对齐 tree.html 的知识地图
 *  交互：hover 放大 + tooltip；有课件节点点击跳课件，无课件虚线框
 *  v2.1 修复：闪动（增量更新SVG）、蓝底黑字（强制浅色文字）、节点交互（分离聚焦与重绘）
 */
(function () {
  "use strict";
  if (window.TeachAnyKnowledgeGraph && window.TeachAnyKnowledgeGraph.__initialized) return;

  var SVG_NS = "http://www.w3.org/2000/svg";
  var BASE_PATH_CANDIDATES = [
    "/assets/scripts/teachany-kg-manifest.json",
    "./assets/scripts/teachany-kg-manifest.json",
    "assets/scripts/teachany-kg-manifest.json",
    "../../assets/scripts/teachany-kg-manifest.json",
    "../../scripts/teachany-kg-manifest.json",
    "../assets/scripts/teachany-kg-manifest.json",
    "../scripts/teachany-kg-manifest.json",
    "scripts/teachany-kg-manifest.json",
    "/teachany-courseware/assets/scripts/teachany-kg-manifest.json",
    "/teachany/scripts/teachany-kg-manifest.json",
    "/scripts/teachany-kg-manifest.json"
  ];

  var manifestPromise = null;
  function loadManifest() {
    if (manifestPromise) return manifestPromise;
    manifestPromise = (function tryNext(list) {
      if (!list.length) return Promise.reject(new Error("manifest-not-found"));
      return fetch(list[0], { cache: "no-cache" })
        .then(function (r) { if (!r.ok) throw new Error("not-ok"); return r.json(); })
        .catch(function () { return tryNext(list.slice(1)); });
    })(BASE_PATH_CANDIDATES.slice());
    return manifestPromise;
  }

  function hexToRgba(hex, alpha) {
    if (!hex) return "rgba(59,130,246," + alpha + ")";
    var h = hex.replace("#", "");
    if (h.length === 3) h = h.split("").map(function (c) { return c + c; }).join("");
    var r = parseInt(h.substr(0, 2), 16) || 59;
    var g = parseInt(h.substr(2, 2), 16) || 130;
    var b = parseInt(h.substr(4, 2), 16) || 246;
    return "rgba(" + r + "," + g + "," + b + "," + alpha + ")";
  }

  var COURSEWARE_BASE_URL = (typeof location !== 'undefined' && /teachany\.cn$/i.test(String(location.hostname || '')))
    ? location.origin
    : 'https://www.teachany.cn';

  function coursewareUrl(course) {
    if (!course || !course.path) return null;
    if (/^https?:\/\//i.test(course.path)) return course.path;
    return COURSEWARE_BASE_URL + "/" + String(course.path).replace(/^\/+/, "").replace(/\/$/, "") + "/index.html";
  }

  function hasCourse(node) {
    return node && node.courses && node.courses.length > 0;
  }

  function escapeHtml(text) {
    return String(text || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function coursewarePrompt(node) {
    var name = node && (node.name || node.id) || "该知识点";
    var id = node && node.id || "";
    return "帮我生成「" + name + "」的 TeachAny 交互式课件，知识点 ID 为 " + id + "。请按 TeachAny skill 规范输出完整 HTML 课件，包含教学目标、前测、核心讲解、真实互动模块、音频/视频资源、后测、知识图谱和质量校验。";
  }

  function recordMakeCourseIntent(node, prompt) {
    try {
      if (window.TeachAnyHistory && typeof window.TeachAnyHistory.recordCreated === "function" && node) {
        window.TeachAnyHistory.recordCreated("kg-intent-" + node.id, {
          source: "knowledge-graph",
          name: (node.name || node.id) + "（知识图谱制作意图）",
          subject: node.subject || "",
          grade: node.grade ? String(node.grade) : "",
          node: node.id,
          url: "",
          prompt: prompt,
          status: "draft"
        });
      }
    } catch (_e) { /* ignore */ }
  }

  function renderMakeCourseBox(panel, node) {
    if (!panel || !node) return;
    var old = panel.querySelector(".tkg-make-course-box");
    if (old) old.remove();
    var prompt = coursewarePrompt(node);
    var promptEl = h("div", { class: "tkg-prompt", text: prompt });
    var feedback = h("span", { class: "tkg-copy-feedback", text: "已复制" });
    var copyBtn = h("button", {
      class: "tkg-make-course-btn secondary",
      type: "button",
      text: "📋 复制提示词",
      on: {
        click: function () {
          var done = function () {
            feedback.classList.add("visible");
            setTimeout(function () { feedback.classList.remove("visible"); }, 1600);
          };
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(prompt).then(done).catch(done);
          } else {
            var ta = document.createElement("textarea");
            ta.value = prompt;
            document.body.appendChild(ta);
            ta.select();
            document.execCommand("copy");
            document.body.removeChild(ta);
            done();
          }
        }
      }
    });
    var box = h("div", { class: "tkg-make-course-box" }, [
      h("strong", { text: "✨ 制作课件" }),
      h("p", { text: "复制下面提示词，在 CodeBuddy/TeachAny skill 中生成这个知识点的课件。" }),
      promptEl,
      h("div", { class: "tkg-make-actions" }, [copyBtn, feedback])
    ]);
    panel.appendChild(box);
    panel.scrollTop = panel.scrollHeight;
    recordMakeCourseIntent(node, prompt);
  }

  function h(tag, attrs, children) {
    var svgTags = ["svg", "g", "circle", "line", "text", "path", "defs", "marker", "polygon", "rect"];
    var el = svgTags.indexOf(tag) >= 0 ? document.createElementNS(SVG_NS, tag) : document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === "class") el.setAttribute("class", attrs[k]);
        else if (k === "html") el.innerHTML = attrs[k];
        else if (k === "text") el.textContent = attrs[k];
        else if (k === "on" && attrs[k]) {
          Object.keys(attrs[k]).forEach(function (ev) { el.addEventListener(ev, attrs[k][ev]); });
        } else if (attrs[k] !== null && attrs[k] !== undefined) {
          el.setAttribute(k, attrs[k]);
        }
      });
    }
    (children || []).forEach(function (c) { if (c) el.appendChild(c); });
    return el;
  }

  /* ─── 数据准备：中心节点 + 前序 + 后续 + 同域 + 边 ─── */
  function buildNeighborhood(manifest, centerId) {
    var nodes = manifest.nodes || {};
    var center = nodes[centerId];
    if (!center) return null;
    var picked = new Map();
    function push(id, layer) {
      if (!id || !nodes[id] || picked.has(id)) return;
      var n = nodes[id];
      picked.set(id, Object.assign({}, n, { _layer: layer }));
    }
    push(centerId, "self");
    (center.prerequisites || []).forEach(function (id) { push(id, "prereq"); });

    // 增强层：hard/soft 前置进入邻域可视化（soft 仅展示，不改变课标必选逻辑）
    var neo = window.TeachAnyNodeEnrichment;
    var enriched = neo && typeof neo.get === "function" ? neo.get(centerId) : null;
    if (enriched && Array.isArray(enriched.prereqs_enriched)) {
      enriched.prereqs_enriched.forEach(function (e) {
        if (e && e.id) push(e.id, "prereq");
      });
    }

    (center.next || []).forEach(function (id) { push(id, "next"); });
    (center.extends || []).forEach(function (id) { push(id, "extend"); });
    (center.siblings || []).slice(0, 6).forEach(function (id) { push(id, "sibling"); });

    var arr = Array.from(picked.values());
    var links = [];
    var linkKey = {};
    function addLink(source, target, type) {
      var key = source + ">" + target + ">" + type;
      if (linkKey[key]) return;
      linkKey[key] = true;
      links.push({ source: source, target: target, type: type });
    }
    arr.forEach(function (n) {
      (n.prerequisites || []).forEach(function (pid) {
        if (picked.has(pid)) {
          var type = "prereq";
          if (n._layer === "next") type = "next";
          addLink(pid, n.id, type);
        }
      });
    });
    if (enriched && Array.isArray(enriched.prereqs_enriched)) {
      enriched.prereqs_enriched.forEach(function (e) {
        if (e && e.id && picked.has(e.id)) addLink(e.id, centerId, "prereq");
      });
    }
    // center <-> siblings
    arr.forEach(function (n) {
      if (n._layer === "sibling") addLink(centerId, n.id, "sibling");
      if (n._layer === "extend") addLink(centerId, n.id, "extend");
    });
    if (neo && typeof neo.annotateLinks === "function") {
      neo.annotateLinks(centerId, links);
    }
    return { center: center, nodes: arr, links: links };
  }

  /* ─── 文本度量：CJK 按 1em、西文按 0.56em 估算（不依赖 DOM，零重排） ─── */
  var LABEL_FONT = 12;
  var LABEL_LINE = 14;
  var SUB_FONT = 10;
  var SUB_LINE = 12;

  function charUnits(ch) {
    var c = ch.charCodeAt(0);
    return c > 255 ? 1 : 0.56;
  }

  function measureText(text, fontSize) {
    var w = 0;
    for (var i = 0; i < text.length; i++) w += charUnits(text.charAt(i)) * fontSize;
    return w;
  }

  /* 按最大宽度折行，最多 maxLines 行，超出加省略号 */
  function wrapText(text, maxWidth, fontSize, maxLines) {
    text = String(text || "");
    if (!text) return [];
    var out = [], buf = "", w = 0;
    for (var i = 0; i < text.length; i++) {
      var ch = text.charAt(i), cw = charUnits(ch) * fontSize;
      if (w + cw > maxWidth && buf) {
        out.push(buf);
        buf = ""; w = 0;
        if (out.length === maxLines) break;
      }
      buf += ch; w += cw;
    }
    if (out.length < maxLines && buf) out.push(buf);
    var consumed = out.join("").length;
    if (consumed < text.length && out.length) {
      var last = out[out.length - 1];
      while (last.length > 1 && measureText(last + "…", fontSize) > maxWidth) {
        last = last.slice(0, -1);
      }
      out[out.length - 1] = last + "…";
    }
    return out;
  }

  function nodeRadiusOf(n) {
    if (n._layer === "self") return 30;
    return hasCourse(n) ? 24 : 20;
  }

  /* 计算一个节点的标签块：多行文本 + 锚点 + 相对节点的偏移 */
  function buildLabel(n, budget, anchor, baseY) {
    var nameLines = wrapText(n.name || n.id, budget, LABEL_FONT, 2);
    var lines = nameLines.map(function (t) { return { text: t, size: LABEL_FONT, cls: "tkg-node-label" }; });
    if (n.name_en) {
      var en = wrapText(n.name_en, budget, SUB_FONT, 1);
      if (en.length) lines.push({ text: en[0], size: SUB_FONT, cls: "tkg-node-label-en" });
    }
    if (n.grade) {
      var g = n.grade;
      var gradeText = n.stage === "elementary" ? "小" + g
        : n.stage === "middle" ? "初" + (g - 6)
        : n.stage === "high" ? "高" + (g - 9)
        : "G" + g;
      lines.push({ text: gradeText, size: SUB_FONT, cls: "tkg-node-grade" });
    }
    var w = 0, h = 0;
    lines.forEach(function (l) {
      w = Math.max(w, measureText(l.text, l.size));
      h += l.size >= LABEL_FONT ? LABEL_LINE : SUB_LINE;
    });
    return { lines: lines, anchor: anchor, dx: 0, baseY: baseY, w: w, h: h };
  }

  function labelBox(n) {
    var l = n._label, r = nodeRadiusOf(n);
    var x0 = l.anchor === "start" ? n.x + l.dx : l.anchor === "end" ? n.x + l.dx - l.w : n.x + l.dx - l.w / 2;
    var y0 = n.y + l.baseY - LABEL_LINE;
    return { x0: x0, x1: x0 + l.w, y0: y0, y1: y0 + l.h };
  }

  function boxOverlap(a, b) {
    var ox = Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0);
    var oy = Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0);
    return ox > 1 && oy > 1 ? { ox: ox, oy: oy } : null;
  }

  /* 碰撞检测 + 二次避让：不动节点，只沿"朝外"方向推开标签；推不开就缩窄折行宽度 */
  function relaxLabels(nodes, width, height) {
    for (var round = 0; round < 3; round++) {
      var moved = false;
      var boxes = nodes.map(function (n) { return { n: n, b: labelBox(n) }; });
      for (var i = 0; i < boxes.length; i++) {
        for (var j = i + 1; j < boxes.length; j++) {
          var A = boxes[i], B = boxes[j];
          var ov = boxOverlap(A.b, B.b);
          if (!ov) continue;
          moved = true;
          // 谁更靠外谁让路；同向则下层让上层
          var aOut = A.n._layer === "sibling" || A.n._layer === "extend";
          var target = aOut ? B : A;
          var other = aOut ? A : B;
          var lay = target.n._label;
          if (lay.anchor === "middle") {
            // 上下类：整体下移（sibling 在中心上方时下移，extend 在下方时下移）
            lay.baseY += Math.min(ov.oy + 3, 18);
          } else {
            var dir = lay.anchor === "start" ? 1 : -1;
            lay.dx += dir * Math.min(ov.ox + 2, 16);
          }
          // 夹在画布内
          var nb = labelBox(target.n);
          if (nb.x0 < 4) lay.dx += 4 - nb.x0;
          if (nb.x1 > width - 4) lay.dx -= nb.x1 - (width - 4);
          if (nb.y1 > height - 4) lay.baseY -= nb.y1 - (height - 4);
          boxes[i].b = labelBox(A.n);
          boxes[j].b = labelBox(B.n);
        }
      }
      if (!moved) return;
    }
    // 仍有重叠：缩窄宽度重排（最多两轮）
    for (var pass = 0; pass < 2; pass++) {
      var clash = false;
      for (var a = 0; a < nodes.length && !clash; a++) {
        for (var b = a + 1; b < nodes.length; b++) {
          if (boxOverlap(labelBox(nodes[a]), labelBox(nodes[b]))) { clash = true; break; }
        }
      }
      if (!clash) return;
      nodes.forEach(function (n) {
        var l = n._label;
        var budget = Math.max(64, l.w * 0.82);
        var rebuilt = buildLabel(n, budget, l.anchor, l.baseY);
        rebuilt.dx = l.dx;
        n._label = rebuilt;
      });
    }
  }

  /* ─── 布局：分带排布（前序左列 / 后续右列 / 同域上带 / 拓展下带）
   *  · 同域 6 个是库内最常见的形态，环形排布在 650×420 里必然压字，
   *    因此同域/拓展改为按行铺开，行内等距，标签另作碰撞避让
   *  · 所有坐标一次性算好，不做力导向迭代，不会有"先乱后稳"的跳动
   */
  function deterministicLayout(nodes, links, width, height) {
    if (width < 520) { layoutNarrow(nodes, width, height); return; }
    var byLayer = { self: [], prereq: [], next: [], sibling: [], extend: [] };
    nodes.forEach(function (n) { (byLayer[n._layer] || byLayer.sibling).push(n); });

    var PAD = 12;
    var ROW_H = 96;        // 一行：节点圆 + 三行标签 + 与下一行的间隙
    var SLOT_MIN = 104;    // 行内每个节点的最小横向槽宽
    var perRow = Math.max(1, Math.floor((width - PAD * 2) / SLOT_MIN));

    var sib = byLayer.sibling, ext = byLayer.extend;
    var sibRows = sib.length ? Math.ceil(sib.length / perRow) : 0;
    var extRows = ext.length ? Math.ceil(ext.length / perRow) : 0;
    var topH = sibRows ? sibRows * ROW_H + 46 : 0;   // 含顶部提示条与右上统计角标避让
    var botH = extRows ? extRows * ROW_H + 26 : 0;

    var cx = width / 2;
    var midTop = topH + 14;
    var midBot = height - botH - 14;
    if (midBot - midTop < 120) {           // 中部被挤扁时，优先保中部
      midTop = Math.min(midTop, height * 0.32);
      midBot = Math.max(midBot, height * 0.68);
    }
    var cy = (midTop + midBot) / 2;

    // 顶/底带：同域、拓展。行内均衡分配（6 个分两行时是 3+3，不是 5+1）
    function placeBand(group, rows, top) {
      if (!rows) return;
      var base = Math.floor(group.length / rows);
      var extra = group.length % rows;
      var idx = 0;
      for (var r = 0; r < rows; r++) {
        var cnt = base + (r < extra ? 1 : 0);
        if (!cnt) continue;
        var usable = width - PAD * 2 - 40;
        var step = usable / cnt;
        for (var k = 0; k < cnt; k++) {
          var n = group[idx++];
          n.x = PAD + 20 + step * (k + 0.5);
          n.y = top + r * ROW_H + 22;
        }
      }
    }
    // top 从 28 起：避开左上角的操作提示条
    placeBand(sib, sibRows, sibRows ? 44 : 0);
    placeBand(ext, extRows, extRows ? height - botH + 6 : 0);

    // 左右列：前序 / 后续
    function placeColumn(group, side) {
      var n = group.length;
      if (!n) return;
      var reserve = Math.min(140, width * 0.22);          // 给标签留的横向空间
      var x = side === "left" ? Math.max(PAD + reserve + 26, cx - width * 0.3)
                              : Math.min(width - PAD - reserve - 26, cx + width * 0.3);
      var spanTop = midTop + 10, spanBot = midBot - 10;
      // 以 cy 为中心展开：间距上限 118，下限取标签块高度（约 44）+ 8
      var room = (spanBot - spanTop) / Math.max(1, n - 1);
      var gap = n === 1 ? 0 : Math.max(64, Math.min(118, room));
      group.forEach(function (node, i) {
        node.x = x;
        node.y = cy + (i - (n - 1) / 2) * gap;
      });
      group.forEach(function (node) {
        node._colX = x;
        node._side = side;
      });
    }
    placeColumn(byLayer.prereq, "left");
    placeColumn(byLayer.next, "right");

    if (byLayer.self.length) {
      byLayer.self[0].x = cx;
      byLayer.self[0].y = cy;
    }

    // 标签：方向与宽度预算
    var colBudget = Math.max(84, Math.min(150, width * 0.2));
    nodes.forEach(function (n) {
      var r = nodeRadiusOf(n);
      var budget, anchor, baseY;
      if (n._layer === "prereq") {
        budget = colBudget; anchor = "end"; baseY = 4;
        n._label = buildLabel(n, budget, anchor, baseY);
        n._label.dx = -(r + 9);
      } else if (n._layer === "next") {
        budget = colBudget; anchor = "start"; baseY = 4;
        n._label = buildLabel(n, budget, anchor, baseY);
        n._label.dx = r + 9;
      } else if (n._layer === "extend") {
        budget = Math.max(80, (width - PAD * 2) / perRow - 12);
        n._label = buildLabel(n, budget, "middle", r + 14);
      } else if (n._layer === "self") {
        budget = Math.min(170, Math.max(96, width * 0.26));
        n._label = buildLabel(n, budget, "middle", r + 14);
      } else {
        budget = Math.max(80, (width - PAD * 2) / perRow - 12);
        n._label = buildLabel(n, budget, "middle", r + 14);
      }
      // 左右列的标签块垂直居中
      if (n._layer === "prereq" || n._layer === "next") {
        n._label.baseY = -(n._label.h) / 2 + LABEL_LINE - 2;
      }
    });

    // 边界保护
    nodes.forEach(function (n) {
      var r = nodeRadiusOf(n);
      if (n.x < r + 2) n.x = r + 2;
      if (n.x > width - r - 2) n.x = width - r - 2;
      if (n.y < r + 2) n.y = r + 2;
      if (n.y > height - r - 2) n.y = height - r - 2;
    });

    finalizeLayout(nodes, width, height);
  }

  /* 把越界的"节点+标签"整体挪回画布 */
  function clampAllNodes(nodes, width, height) {
    nodes.forEach(function (n) {
      var r = nodeRadiusOf(n);
      var b = labelBox(n);
      var dx = 0, dy = 0;
      if (b.y1 > height - 3) dy -= (b.y1 - (height - 3));
      if (b.y0 < 3) dy += (3 - b.y0);
      if (b.x1 > width - 3) dx -= (b.x1 - (width - 3));
      if (b.x0 < 3) dx += (3 - b.x0);
      n.x += dx; n.y += dy;
      if (n.x < r + 2) n.x = r + 2;
      if (n.x > width - r - 2) n.x = width - r - 2;
      if (n.y < r + 2) n.y = r + 2;
      if (n.y > height - r - 2) n.y = height - r - 2;
      // 避让右上角「N 已有课件」统计角标（约 190×40）
      if (n.y - r < 44 && n.x + 95 > width) n.y = 44 + r;
    });
  }

  function finalizeLayout(nodes, width, height) {
    relaxLabels(nodes, width, height);
    clampAllNodes(nodes, width, height);
    relaxLabels(nodes, width, height);
    clampAllNodes(nodes, width, height);
  }

  /* ─── 窄屏（< 520px）：纵向流。前序 → 本课 → 后续 → 同域 → 拓展，逐行铺开
   *  横向空间不足时左右分列必然压字，改成上下顺序阅读更稳
   */
  function layoutNarrow(nodes, width, height) {
    var PAD = 12, ROW_H = 96;
    var perRow = Math.max(1, Math.floor((width - PAD * 2) / 104));
    var byLayer = { self: [], prereq: [], next: [], sibling: [], extend: [] };
    nodes.forEach(function (n) { (byLayer[n._layer] || byLayer.sibling).push(n); });

    var y = 78;   // 避开顶部提示条（窄屏会折行）
    function band(group) {
      if (!group.length) return;
      var rows = Math.ceil(group.length / perRow);
      var base = Math.floor(group.length / rows);
      var extra = group.length % rows;
      var idx = 0;
      for (var r = 0; r < rows; r++) {
        var cnt = base + (r < extra ? 1 : 0);
        var step = (width - PAD * 2 - 16) / cnt;
        for (var k = 0; k < cnt; k++) {
          var n = group[idx++];
          n.x = PAD + 8 + step * (k + 0.5);
          n.y = y + r * ROW_H + 22;
        }
      }
      y += rows * ROW_H;
    }

    band(byLayer.prereq);
    if (byLayer.self.length) {
      byLayer.self[0].x = width / 2;
      byLayer.self[0].y = y + 40;
    }
    // 本课节点半径 30，标签块最多 58 高，需要整块推进，不能只推 78
    y += 128;
    band(byLayer.next);
    band(byLayer.sibling);
    band(byLayer.extend);

    var budget = Math.max(72, (width - PAD * 2) / perRow - 12);
    nodes.forEach(function (n) {
      n._label = buildLabel(n, budget, "middle", nodeRadiusOf(n) + 14);
    });
    finalizeLayout(nodes, width, height);
  }

  /* ─── 绘制 SVG 图谱（v2.1: 支持增量更新，不再每次全量清除） ─── */
  function renderGraph(svg, graph, handlers, existingGraph) {
    // 如果新旧图谱节点集合一致，只更新高亮和详情面板，不清除重建
    var oldNodeIds = existingGraph ? existingGraph.nodes.map(function(n){ return n.id; }).sort().join(',') : '';
    var newNodeIds = graph.nodes.map(function(n){ return n.id; }).sort().join(',');
    var oldCenterId = existingGraph ? (existingGraph.nodes.find(function(n){ return n._layer === 'self'; }) || {}).id : '';
    var newCenterId = (graph.nodes.find(function(n){ return n._layer === 'self'; }) || {}).id;
    var sameGraph = oldNodeIds && oldNodeIds === newNodeIds && oldCenterId === newCenterId;

    if (sameGraph) {
      // 增量更新：只改高亮状态，不重建SVG
      svg.querySelectorAll(".tkg-node-group").forEach(function (g) {
        var nid = g.getAttribute("data-id");
        var n = graph.nodes.find(function(x){ return x.id === nid; });
        if (!n) return;
        // 更新 _layer 可能变化了
        var isSelf = n._layer === "self";
        var hasCrs = hasCourse(n);
        var radius = hasCrs ? 24 : 20;
        if (isSelf) radius = 30;
        var domainColor = n.domain_color || "#3b82f6";
        var fill, stroke, dash;
        if (isSelf) {
          fill = hexToRgba(domainColor, 0.55);
          stroke = domainColor;
          dash = "none";
        } else if (hasCrs) {
          fill = hexToRgba(domainColor, 0.40);
          stroke = domainColor;
          dash = "none";
        } else {
          fill = hexToRgba(domainColor, 0.15);
          stroke = hexToRgba(domainColor, 0.6);
          dash = "4 3";
        }
        var circle = g.querySelector(".tkg-node-circle");
        if (circle) {
          circle.setAttribute("fill", fill);
          circle.setAttribute("stroke", stroke);
          circle.setAttribute("stroke-dasharray", dash);
          circle.setAttribute("r", radius);
        }
        // 更新 status icon
        var iconEl = g.querySelector(".tkg-node-status-icon");
        if (iconEl) {
          var icon = "📝";
          if (isSelf) icon = "🎯";
          else if (hasCrs) icon = "✅";
          iconEl.textContent = icon;
        }
        // 更新 class
        g.setAttribute("class", "tkg-node-group" + (hasCrs || isSelf ? "" : " no-course"));
      });
      return;
    }

    // 全量重建（中心节点变了，邻居集合不同了）
    // v2.3: 重建期间 SVG 设 visibility:hidden，避免"边建边看"的逐节点闪现
    svg.style.visibility = "hidden";
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    // v2.2: 用 canvas 容器尺寸而不是 svg 自身（svg 在初次未布局时 width 可能为 0）
    var canvasEl = svg.parentElement;
    var bb = (canvasEl || svg).getBoundingClientRect();
    var width = bb.width || 600;
    // 容器异常时给个保底
    if (width < 100) width = 600;
    // 按同域/拓展的行数动态加高画布，给折行标签腾空间
    if (canvasEl && canvasEl.classList && canvasEl.classList.contains("tkg-canvas")) {
      var perRowCalc = Math.max(1, Math.floor((width - 24) / 104));
      var sibN = 0, extN = 0;
      graph.nodes.forEach(function (n) {
        if (n._layer === "sibling") sibN++;
        else if (n._layer === "extend") extN++;
      });
      var preN = 0, nextN = 0;
      graph.nodes.forEach(function (n) {
        if (n._layer === "prereq") preN++;
        else if (n._layer === "next") nextN++;
      });
      var bandRows = Math.ceil(sibN / perRowCalc) + Math.ceil(extN / perRowCalc);
      var colRows = Math.max(preN, nextN);
      // 带行（每行 96）+ 中部核心（120）+ 左右列额外行（每行 52）
      var needH;
      if (width < 520) {
        // 窄屏纵向流：前序/后续/同域/拓展依次铺开，每行 96，中间留 78
        var rowsN = Math.ceil(preN / perRowCalc) + Math.ceil(nextN / perRowCalc) + bandRows;
        needH = Math.max(420, 78 + rowsN * 96 + 128 + 16);
      } else {
        needH = Math.max(420, 46 + bandRows * 96 + 120 + Math.max(0, colRows - 1) * 52);
      }
      if (Math.abs((canvasEl.offsetHeight || 0) - needH) > 2) canvasEl.style.height = needH + "px";
    }
    var height = canvasEl ? canvasEl.getBoundingClientRect().height : (svg.getBoundingClientRect().height || 420);
    if (height < 100) height = 420;
    svg.setAttribute("viewBox", "0 0 " + width + " " + height);
    svg.setAttribute("width", width);
    svg.setAttribute("height", height);

    deterministicLayout(graph.nodes, graph.links, width, height);

    // Arrow markers
    var defs = h("defs");
    [
      { id: "tkg-arrow-prereq", color: "rgba(148,163,184,0.6)" },
      { id: "tkg-arrow-next", color: "rgba(59,130,246,0.7)" },
      { id: "tkg-arrow-sibling", color: "rgba(245,158,11,0.55)" },
      { id: "tkg-arrow-extend", color: "rgba(139,92,246,0.6)" }
    ].forEach(function (m) {
      defs.appendChild(h("marker", {
        id: m.id, viewBox: "0 -5 10 10", refX: 28, refY: 0,
        markerWidth: 6, markerHeight: 6, orient: "auto"
      }, [h("path", { d: "M0,-5L10,0L0,5", fill: m.color })]));
    });
    svg.appendChild(defs);

    // Links
    var linkGroup = h("g", { class: "tkg-links" });
    graph.links.forEach(function (l) {
      var src = graph.nodes.find(function (n) { return n.id === l.source; });
      var tgt = graph.nodes.find(function (n) { return n.id === l.target; });
      if (!src || !tgt) return;
      var soft = l.strength === "soft";
      var line = h("line", {
        class: "tkg-link link-" + l.type + (soft ? " strength-soft" : ""),
        x1: src.x, y1: src.y, x2: tgt.x, y2: tgt.y,
        "marker-end": "url(#tkg-arrow-" + l.type + ")",
        "stroke-dasharray": soft ? "5 4" : undefined
      });
      line.__data = l;
      linkGroup.appendChild(line);
    });
    svg.appendChild(linkGroup);

    // Nodes (tree.html 风格，v2.1: 提高填充不透明度，增强可读性)
    var nodeGroup = h("g", { class: "tkg-nodes" });
    graph.nodes.forEach(function (n) {
      var hasCrs = hasCourse(n);
      var isSelf = n._layer === "self";
      var radius = hasCrs ? 24 : 20;
      if (isSelf) radius = 30;
      var domainColor = n.domain_color || "#3b82f6";
      var fill, stroke, dash;
      if (isSelf) {
        fill = hexToRgba(domainColor, 0.55);
        stroke = domainColor;
        dash = "none";
      } else if (hasCrs) {
        fill = hexToRgba(domainColor, 0.40);
        stroke = domainColor;
        dash = "none";
      } else {
        fill = hexToRgba(domainColor, 0.15);
        stroke = hexToRgba(domainColor, 0.6);
        dash = "4 3";
      }
      var g = h("g", {
        class: "tkg-node-group" + (hasCrs || isSelf ? "" : " no-course"),
        transform: "translate(" + n.x + "," + n.y + ")",
        "data-id": n.id,
        "data-has-course": hasCrs ? "1" : "0",
        on: {
          click: function (ev) {
            ev.stopPropagation();
            handlers.onNodeClick && handlers.onNodeClick(n, ev);
          },
          mouseenter: function (ev) { handlers.onHover && handlers.onHover(n, ev); },
          mousemove: function (ev) { handlers.onMove && handlers.onMove(n, ev); },
          mouseleave: function (ev) { handlers.onLeave && handlers.onLeave(n, ev); }
        }
      });
      g.appendChild(h("circle", {
        class: "tkg-node-circle",
        r: radius,
        fill: fill,
        stroke: stroke,
        "stroke-dasharray": dash
      }));
      // Status icon
      var icon = "📝";
      if (isSelf) icon = "🎯";
      else if (hasCrs) icon = "✅";
      g.appendChild(h("text", {
        class: "tkg-node-status-icon",
        dy: "0.35em",
        text: icon
      }));
      // 标签块：按布局阶段算好的行、锚点、偏移渲染（支持折行与左右分向）
      var lab = n._label;
      if (!lab) {
        lab = buildLabel(n, 120, "middle", radius + 14);
        lab.dx = 0;
      }
      var ly = lab.baseY;
      lab.lines.forEach(function (line) {
        g.appendChild(h("text", {
          class: line.cls,
          x: lab.dx,
          y: ly,
          "text-anchor": lab.anchor,
          text: line.text
        }));
        ly += line.size >= LABEL_FONT ? LABEL_LINE : SUB_LINE;
      });
      nodeGroup.appendChild(g);
    });
    svg.appendChild(nodeGroup);
    // v2.3: 所有节点/连线就位后再显现，避免"边建边看"的闪烁
    if (typeof requestAnimationFrame === "function") {
      requestAnimationFrame(function () { svg.style.visibility = "visible"; });
    } else {
      svg.style.visibility = "visible";
    }
  }

  /* ─── Tooltip ─── */
  function buildTooltipContent(node) {
    var hasCrs = hasCourse(node);
    var stage = node.stage === "elementary" ? "小学" : node.stage === "middle" ? "初中" : node.stage === "high" ? "高中" : (node.stage || "");
    var gradeTxt = node.grade ? "G" + node.grade : "";
    var meta = [stage + gradeTxt, node.domain].filter(Boolean).join(" · ");
    var html = '<h3>' + (node.name || node.id) + (node.name_en ? ' <small style="font-size:12px;opacity:0.6;font-weight:400">' + node.name_en + '</small>' : '') + '</h3>';
    html += '<div class="meta">' + meta + '</div>';
    if (hasCrs) {
      html += '<span class="status-badge badge-active">✅ 已有课件</span>';
    } else {
      html += '<span class="status-badge badge-gap">📝 暂无课件</span>';
    }
    if ((node.prerequisites || []).length) {
      html += '<div style="margin-top:10px;font-size:12px;color:rgba(148,163,184,0.9)">前置：' + node.prerequisites.slice(0, 3).join('、') + '</div>';
    }
    if ((node.curriculum_points || []).length) {
      html += '<div style="margin-top:8px;font-size:12px;line-height:1.55;color:rgba(226,232,240,0.85)">' + (node.curriculum_points[0] || "").slice(0, 80) + '</div>';
    }
    if (hasCrs && node.courses && node.courses[0]) {
      var url = coursewareUrl(node.courses[0]);
      if (url) {
        html += '<a class="course-link" href="' + url + '" target="_top">🚀 打开课件：' + escapeHtml(node.courses[0].name || node.courses[0].id) + '</a>';
      }
    } else {
      html += '<div class="gap-msg">该知识点暂无官方课件，欢迎贡献社区版本。</div>';
    }
    html += '<button type="button" class="course-link tkg-make-course-btn" data-tkg-make-course="' + escapeHtml(node.id) + '">✨ 制作课件</button>';
    return html;
  }

  // v2.4: tooltip 锚定到节点本身而不是鼠标，用户才能安全把鼠标移到 tooltip 上点击链接
  function positionTooltipAtNode(tooltip, root, nodeEl) {
    if (!nodeEl) return;
    var rootRect = root.getBoundingClientRect();
    var nodeRect = nodeEl.getBoundingClientRect();
    // 默认：在节点右侧，垂直居中
    var tw = tooltip.offsetWidth || 280;
    var th = tooltip.offsetHeight || 200;
    var x = nodeRect.right - rootRect.left + 8;
    var y = nodeRect.top - rootRect.top + (nodeRect.height - th) / 2;
    // 如果右侧放不下，放到左侧
    if (x + tw > rootRect.width - 4) {
      x = nodeRect.left - rootRect.left - tw - 8;
    }
    // 如果左侧也放不下（节点在最左），放到下方
    if (x < 4) {
      x = nodeRect.left - rootRect.left + (nodeRect.width - tw) / 2;
      y = nodeRect.bottom - rootRect.top + 8;
    }
    // 垂直边界保护
    if (y < 8) y = 8;
    if (y + th > rootRect.height - 8) y = rootRect.height - th - 8;
    if (x < 4) x = 4;
    tooltip.style.left = x + "px";
    tooltip.style.top = y + "px";
  }

  // 旧接口：退回旧逻辑作兜底（不再用，只保留兼容）
  function positionTooltip(tooltip, root, event) {
    var rootRect = root.getBoundingClientRect();
    var x = event.clientX - rootRect.left + 18;
    var y = event.clientY - rootRect.top + 18;
    var tw = tooltip.offsetWidth;
    var th = tooltip.offsetHeight;
    if (x + tw > rootRect.width) x = event.clientX - rootRect.left - tw - 12;
    if (y + th > rootRect.height) y = rootRect.height - th - 12;
    if (y < 8) y = 8;
    tooltip.style.left = x + "px";
    tooltip.style.top = y + "px";
  }

  /* ─── 详情面板（右侧） ─── */
  function renderDetailPanel(panel, nodeId, manifest, rootEl) {
    var nodes = manifest.nodes;
    var node = nodes[nodeId];
    while (panel.firstChild) panel.removeChild(panel.firstChild);
    if (!node) { panel.appendChild(h("div", { class: "tkg-empty", text: "找不到节点 " + nodeId })); return; }
    var hasCrs = hasCourse(node);
    var stage = node.stage === "elementary" ? "小学" : node.stage === "middle" ? "初中" : node.stage === "high" ? "高中" : (node.stage || "");
    panel.appendChild(h("div", null, [
      h("h3", { text: node.name || node.id }),
      h("div", { class: "meta", text: [stage, node.grade ? "G" + node.grade : "", node.domain].filter(Boolean).join(" · ") })
    ]));
    panel.appendChild(h("div", {
      class: "status-badge " + (hasCrs ? "badge-active" : "badge-gap"),
      text: hasCrs ? "✅ 已有课件" : "📝 暂无课件",
      style: "display:inline-block;padding:3px 10px;border-radius:10px;font-size:11px;font-weight:700;background:" + (hasCrs ? "rgba(16,185,129,0.2)" : "rgba(239,68,68,0.18)") + ";color:" + (hasCrs ? "var(--tkg-success)" : "var(--tkg-danger)") + ";"
    }));

    var tagsWrap = h("div", { class: "tkg-tags" });
    function addTag(id, layer) {
      var target = nodes[id];
      if (!target) return;
      var tgtHasCourse = hasCourse(target);
      var tag = h("a", {
        class: "tkg-tag layer-" + layer + (tgtHasCourse ? " has-course" : " no-course"),
        href: tgtHasCourse && target.courses[0] ? coursewareUrl(target.courses[0]) : "#",
        target: tgtHasCourse ? "_top" : undefined,
        text: target.name || target.id,
        on: {
          click: function (ev) {
            if (!tgtHasCourse) { ev.preventDefault(); }
            rootEl.dispatchEvent(new CustomEvent("tkg:focus", { detail: id }));
          }
        }
      });
      tagsWrap.appendChild(tag);
    }
    (node.prerequisites || []).forEach(function (id) { addTag(id, "prereq"); });
    (node.next || []).forEach(function (id) { addTag(id, "next"); });
    (node.extends || []).forEach(function (id) { addTag(id, "extend"); });
    (node.siblings || []).slice(0, 6).forEach(function (id) { addTag(id, "sibling"); });
    if (tagsWrap.children.length) {
      panel.appendChild(h("div", { class: "meta", text: "前序 / 后续 / 同域（📚 = 已有课件）" }));
      panel.appendChild(tagsWrap);
    }

    if ((node.curriculum_points || []).length) {
      panel.appendChild(h("div", { class: "meta", text: "课标要点" }));
      var ul = h("ul");
      node.curriculum_points.slice(0, 3).forEach(function (t) { ul.appendChild(h("li", { text: t })); });
      panel.appendChild(ul);
    }
    if (node.textbook_chapter) panel.appendChild(h("div", { class: "meta", text: "教材：" + node.textbook_chapter }));

    // 增强层：错因 / 必备前置提示
    try {
      var neoE = window.TeachAnyNodeEnrichment;
      var entry = neoE && typeof neoE.get === "function" ? neoE.get(nodeId) : null;
      if (entry && entry.misconceptions && entry.misconceptions.length) {
        panel.appendChild(h("div", { class: "meta", text: "错因诊断" }));
        var mul = h("ul");
        entry.misconceptions.slice(0, 3).forEach(function (m) {
          mul.appendChild(h("li", { text: (m.cue || "") + (m.diagnosis ? " — " + m.diagnosis : "") }));
        });
        panel.appendChild(mul);
      }
    } catch (_) { /* ignore */ }

    if ((node.courses || []).length) {
      panel.appendChild(h("div", { class: "meta", text: "可跳转课件" }));
      var list = h("div", { class: "tkg-panel-links" });
      node.courses.slice(0, 3).forEach(function (c) {
        var url = coursewareUrl(c);
        if (!url) return;
        list.appendChild(h("a", {
          class: "tkg-link-card", href: url, target: "_top",
          html: "<div><strong>" + escapeHtml(c.name || c.id) + "</strong><br><em>" + escapeHtml(c.source || "") + "</em></div><span>→</span>"
        }));
      });
      if (list.children.length) panel.appendChild(list);
    }
    panel.appendChild(h("button", {
      class: "tkg-make-course-btn",
      type: "button",
      text: "✨ 制作课件",
      on: { click: function () { renderMakeCourseBox(panel, node); } }
    }));
  }

  /* ─── 筛选 / 搜索 ─── */
  function applyFilter(root, filter) {
    var svg = root.querySelector(".tkg-canvas svg");
    if (!svg) return;
    var nodes = svg.__graphNodes || [];
    // Filter links
    svg.querySelectorAll(".tkg-link").forEach(function (line) {
      var t = (line.getAttribute("class") || "").split(/\s+/).find(function (c) { return c.indexOf("link-") === 0 && c !== "tkg-link"; }) || "";
      var lk = t.replace("link-", "");
      line.classList.toggle("dim", !(filter === "all" || lk === filter));
    });
    // Filter nodes
    nodes.forEach(function (n) {
      var g = svg.querySelector('.tkg-node-group[data-id="' + n.id + '"]');
      if (!g) return;
      var show = filter === "all" || n._layer === "self" || n._layer === filter;
      g.classList.toggle("dim", !show);
    });
  }

  function renderSearch(manifest, input, resultBox, root) {
    var nodes = manifest.nodes;
    function search(q) {
      q = (q || "").trim().toLowerCase();
      while (resultBox.firstChild) resultBox.removeChild(resultBox.firstChild);
      if (!q) return;
      var matches = [];
      Object.keys(nodes).forEach(function (id) {
        var n = nodes[id];
        var hay = (n.name || "") + " " + id + " " + (n.name_en || "");
        if (hay.toLowerCase().indexOf(q) !== -1) matches.push(n);
      });
      matches.slice(0, 6).forEach(function (n) {
        resultBox.appendChild(h("a", {
          class: "tkg-link-card", href: "#",
          html: "<div><strong>" + (n.name || n.id) + "</strong><br><em>" + (n.domain || "") + " · " + (n.stage || "") + (hasCourse(n) ? " · 📚" : "") + "</em></div><span>聚焦 →</span>",
          on: {
            click: function (ev) {
              ev.preventDefault();
              root.dispatchEvent(new CustomEvent("tkg:focus", { detail: n.id }));
              input.value = "";
              while (resultBox.firstChild) resultBox.removeChild(resultBox.firstChild);
            }
          }
        }));
      });
      if (!matches.length) resultBox.appendChild(h("div", { class: "tkg-empty", text: "没有匹配节点" }));
    }
    input.addEventListener("input", function () { search(input.value); });
  }

  /* ─── 挂载 ─── */
  function mount(el, manifest) {
    var nodeId = el.getAttribute("data-teachany-kg");
    if (!nodeId || !manifest.nodes[nodeId]) {
      el.innerHTML = '<div class="tkg-empty">无法渲染知识图谱：' + (nodeId ? "节点 " + nodeId + " 不存在于索引" : "缺少 data-teachany-kg 属性") + '</div>';
      return;
    }
    var centerNode = manifest.nodes[nodeId];
    el.classList.add("tkg-root");
    el.innerHTML = "";

    var head = h("div", { class: "tkg-head" });
    head.appendChild(h("h2", { class: "tkg-title", html: "🗺️ 知识图谱 <small>" + (centerNode.name || nodeId) + "</small>" }));
    var tools = h("div", { class: "tkg-tools" });
    var filterAll = h("button", { class: "tkg-filter active", type: "button", "data-filter": "all", text: "全部" });
    var filterPre = h("button", { class: "tkg-filter", type: "button", "data-filter": "prereq", text: "前序" });
    var filterNext = h("button", { class: "tkg-filter", type: "button", "data-filter": "next", text: "后续" });
    var filterSib = h("button", { class: "tkg-filter", type: "button", "data-filter": "sibling", text: "同域" });
    var search = h("input", { type: "search", placeholder: "搜索任意知识点…" });
    [filterAll, filterPre, filterNext, filterSib, search].forEach(function (n) { tools.appendChild(n); });
    head.appendChild(tools);
    el.appendChild(head);

    var body = h("div", { class: "tkg-body" });

    var canvasWrap = h("div", { class: "tkg-canvas" });
    var svg = document.createElementNS(SVG_NS, "svg");
    svg.setAttribute("preserveAspectRatio", "xMidYMid meet");
    canvasWrap.appendChild(svg);
    canvasWrap.appendChild(h("div", { class: "tkg-canvas-hint", text: "悬停看详情 · 点击有课件节点跳转课件 / 无课件节点切换图谱焦点" }));
    var statWrap = h("div", { class: "tkg-canvas-stat" });
    canvasWrap.appendChild(statWrap);
    // Tooltip follows mouse
    var tooltip = h("div", { class: "tkg-tooltip" });
    canvasWrap.appendChild(tooltip);
    body.appendChild(canvasWrap);

    var panel = h("div", { class: "tkg-panel" });
    body.appendChild(panel);

    el.appendChild(body);

    // Search result drawer (independent box)
    var searchBox = h("div", { class: "tkg-panel-links", style: "margin-top:10px;" });
    el.appendChild(searchBox);

    // v7.7.5: 学习足迹模块已移除（教学价值低，且干扰主视觉）

    var footer = h("div", { class: "tkg-footer" });
    var legend = h("div", { class: "tkg-legend" });
    [
      ["🎯 本节", "#f59e0b"],
      ["✅ 已有课件（点击跳转）", "#10b981"],
      ["📝 暂无课件（虚线框）", "#94a3b8"]
    ].forEach(function (p) {
      var span = h("span");
      span.innerHTML = '<span class="tkg-legend-dot" style="background:' + p[1] + ';"></span>' + p[0];
      legend.appendChild(span);
    });
    footer.appendChild(legend);
    footer.appendChild(h("div", { text: "数据：data/trees + skill/assets/image-registry.json · 风格：与 tree.html 一致" }));
    el.appendChild(footer);

    // Render state
    var visited = new Set();
    var currentId = nodeId;
    var currentFilter = "all";
    var currentGraph = null; // v2.1: 保存当前图谱引用，用于增量更新

    // v7.7.5: drawProbe() 已移除（学习足迹模块下线）

    /**
     * v2.1: 聚焦节点 — 如果新焦点已在当前图谱中，仅更新高亮+详情面板
     * 如果新焦点不在当前图谱中，才触发完整重绘
     */
    function focusNode(id) {
      currentId = id;
      visited.add(id);

      // 检查新节点是否在当前图谱中
      var alreadyInGraph = currentGraph && currentGraph.nodes.some(function(n) { return n.id === id; });

      if (alreadyInGraph) {
        // 增量更新：重建邻居关系（中心节点变了，_layer 要变），但不重绘整个SVG
        var newGraph = buildNeighborhood(manifest, id);
        if (!newGraph) return;

        // 用 renderGraph 的增量模式：只更新节点样式/高亮，不重建SVG结构
        renderGraph(svg, newGraph, {
          onNodeClick: onNodeClick,
          onHover: onHover,
          onMove: onMove,
          onLeave: onLeave
        }, currentGraph);

        currentGraph = newGraph;
        svg.__graphNodes = newGraph.nodes;
      } else {
        // 全量重绘：新焦点不在当前图谱中
        var graph = buildNeighborhood(manifest, id);
        if (!graph) return;
        renderGraph(svg, graph, {
          onNodeClick: onNodeClick,
          onHover: onHover,
          onMove: onMove,
          onLeave: onLeave
        }, null);
        currentGraph = graph;
        svg.__graphNodes = graph.nodes;
      }

      // 通用更新：详情面板、高亮、筛选、统计
      renderDetailPanel(panel, id, manifest, el);
      applyFilter(el, currentFilter);

      // Highlight selected
      svg.querySelectorAll(".tkg-node-group").forEach(function (g) {
        g.classList.toggle("selected", g.getAttribute("data-id") === id);
      });
      // Stats
      var total = currentGraph.nodes.length;
      var withCourse = currentGraph.nodes.filter(hasCourse).length;
      statWrap.innerHTML = '<span>' + total + ' 节点</span><span>✅ ' + withCourse + ' 已有课件</span>';
      // v7.7.5: drawProbe() 已移除

      // 更新标题中的当前节点名
      var titleSmall = el.querySelector(".tkg-title small");
      if (titleSmall) {
        var node = manifest.nodes[id];
        titleSmall.textContent = node ? (node.name || id) : id;
      }
    }

    // 事件处理器（提取为命名函数以便复用）
    function onNodeClick(n, ev) {
      // 有课件 → 打开课件；无课件 → 聚焦到详情面板
      if (hasCourse(n) && n.id !== currentId) {
        var url = coursewareUrl(n.courses[0]);
        if (url) { window.open(url, "_top"); return; }
      }
      focusNode(n.id);
    }
    // v2.4: tooltip hover 延迟关闭 + 允许鼠标移入 tooltip 交互（点击"打开课件"按钮）
    var hideTid = null;
    function showTooltip() {
      if (hideTid) { clearTimeout(hideTid); hideTid = null; }
      tooltip.classList.add("visible");
    }
    function scheduleHide() {
      if (hideTid) clearTimeout(hideTid);
      hideTid = setTimeout(function () { tooltip.classList.remove("visible"); hideTid = null; }, 400);
    }
    // 鼠标进入 tooltip 时取消隐藏；离开 tooltip 时立即隐藏
    tooltip.addEventListener("mouseenter", function () { showTooltip(); });
    tooltip.addEventListener("mouseleave", function () { scheduleHide(); });
    tooltip.addEventListener("click", function (ev) {
      var btn = ev.target && ev.target.closest ? ev.target.closest("[data-tkg-make-course]") : null;
      if (!btn) return;
      ev.preventDefault();
      ev.stopPropagation();
      var node = manifest.nodes[btn.getAttribute("data-tkg-make-course")];
      if (node) {
        focusNode(node.id);
        renderMakeCourseBox(panel, node);
        scheduleHide();
      }
    });

    function onHover(n, ev) {
      tooltip.innerHTML = buildTooltipContent(n);
      showTooltip();
      // v2.4: 定位到节点本身而非鼠标位置，方便用户滑到 tooltip 上点按钮
      var nodeEl = svg.querySelector('.tkg-node-group[data-id="' + n.id + '"]');
      if (nodeEl) positionTooltipAtNode(tooltip, canvasWrap, nodeEl);
      else positionTooltip(tooltip, canvasWrap, ev);
    }
    function onMove(n, ev) {
      // v2.4: tooltip 不再随鼠标移动，避免离开节点时被拖远；仅在节点切换时重新定位
      // 没有操作
    }
    function onLeave() { scheduleHide(); }

    [filterAll, filterPre, filterNext, filterSib].forEach(function (btn) {
      btn.addEventListener("click", function () {
        [filterAll, filterPre, filterNext, filterSib].forEach(function (b) { b.classList.remove("active"); });
        btn.classList.add("active");
        currentFilter = btn.getAttribute("data-filter");
        applyFilter(el, currentFilter);
      });
    });
    el.addEventListener("tkg:focus", function (ev) { focusNode(ev.detail); });
    renderSearch(manifest, search, searchBox, el);

    // v2.3 移除拖拽功能：确定性布局下节点位置已合理，拖拽会制造闪动（mousedown 后抖动鼠标即误触发，transform 通过 CSS transition 动画出现肉眼可感的"跳"）；
    // 保留"按下 + 立即抬起 = 点击"逻辑（浏览器自带，无需代码）。

    // 初次渲染（全量）——用 rAF 延后一帧，等待样式 / 字体 / AudioBar 等注入稳定
    if (typeof requestAnimationFrame === "function") {
      requestAnimationFrame(function () { requestAnimationFrame(function () { focusNode(nodeId); }); });
    } else {
      setTimeout(function () { focusNode(nodeId); }, 16);
    }

    // Resize（防抖，全量重绘）——仅响应真实尺寸变化，且有阈值保护
    var lastW = 0, lastH = 0;
    function maybeRelayout() {
      var bb = canvasWrap.getBoundingClientRect();
      var dw = Math.abs(bb.width - lastW), dh = Math.abs(bb.height - lastH);
      if (dw < 8 && dh < 8) return; // 小于 8px 变化忽略，避免 scrollbar/浮条来回
      lastW = bb.width; lastH = bb.height;
      currentGraph = null;
      focusNode(currentId);
    }
    window.addEventListener("resize", (function () {
      var tid = null;
      return function () { clearTimeout(tid); tid = setTimeout(maybeRelayout, 250); };
    })());
    // ResizeObserver 监测容器尺寸（TutorCard/AudioBar 注入后容器宽度可能微调）
    if ("ResizeObserver" in window) {
      var ro = new ResizeObserver((function () {
        var tid = null;
        return function () { clearTimeout(tid); tid = setTimeout(maybeRelayout, 180); };
      })());
      ro.observe(canvasWrap);
    }
  }

  function ensureEnrichment() {
    if (window.TeachAnyNodeEnrichment) return window.TeachAnyNodeEnrichment.load();
    return new Promise(function (resolve) {
      var existing = document.querySelector("script[data-teachany-neo]");
      if (existing) {
        existing.addEventListener("load", function () {
          (window.TeachAnyNodeEnrichment ? window.TeachAnyNodeEnrichment.load() : Promise.resolve(null)).then(resolve);
        });
        return;
      }
      var s = document.createElement("script");
      s.src = "/assets/scripts/teachany-node-enrichment.js?v=neo-1";
      s.async = true;
      s.dataset.teachanyNeo = "1";
      s.onload = function () {
        (window.TeachAnyNodeEnrichment ? window.TeachAnyNodeEnrichment.load() : Promise.resolve(null)).then(resolve);
      };
      s.onerror = function () { resolve(null); };
      document.head.appendChild(s);
    });
  }

  function init() {
    var targets = document.querySelectorAll("[data-teachany-kg]");
    if (!targets.length) return;
    Promise.all([loadManifest(), ensureEnrichment().catch(function () { return null; })]).then(function (pair) {
      var m = pair[0];
      targets.forEach(function (el) { mount(el, m); });
    }).catch(function (err) {
      targets.forEach(function (el) {
        el.innerHTML = '<div class="tkg-empty">知识图谱加载失败：' + (err && err.message || err) + '</div>';
      });
    });
  }

  window.TeachAnyKnowledgeGraph = { __initialized: true, mount: mount, loadManifest: loadManifest };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
