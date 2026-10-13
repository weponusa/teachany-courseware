/* TeachAny 真实地图实验组件 v1.0
 * 底图：Natural Earth 真实国界（political/world/countries.geojson）
 * 太阳辐射层：天文公式精确值（太阳赤纬、正午太阳高度角、大气顶辐照含日地距离修正）
 * 气温/降水层：10°纬带气候平均值（真实气候规律，忽略海陆/地形差异）
 * 用法：window.__TEACHANY_GEO_LAB__ = {topic, task, defaultLayer, lat, month, geojson}
 *       <div id="teachany-geo-lab"></div> + 本脚本 defer
 */
(function () {
  "use strict";

  // ── 纬带气候平均表（0°~80°，每10°一个关键帧，南北纬镜像简化）──
  // 气温：全球纬带年平均（°C），来源性质：气候平均
  var TEMP_TABLE = [[0, 26.2], [10, 26.0], [20, 24.1], [30, 20.4], [40, 14.1], [50, 6.9], [60, -0.7], [70, -10.6], [80, -18.4]];
  // 降水：全球纬带年降水量（mm），赤道低压多雨、副热带高压少雨、西风带较多、极地少雨
  var RAIN_TABLE = [[0, 2150], [10, 1750], [20, 1050], [25, 720], [30, 780], [40, 950], [50, 880], [60, 620], [70, 380], [80, 180]];

  var S0 = 1361; // 太阳常数 W/m²（大气顶）

  function interp(table, lat) {
    var a = Math.min(80, Math.abs(lat));
    for (var i = 1; i < table.length; i++) {
      if (a <= table[i][0]) {
        var t = (a - table[i - 1][0]) / (table[i][0] - table[i - 1][0]);
        return table[i - 1][1] + t * (table[i][1] - table[i - 1][1]);
      }
    }
    return table[table.length - 1][1];
  }

  // 太阳赤纬 δ（度），N 为年内第几天。标准近似式 δ = -23.44·cos(2π(N+10)/365)
  function declination(dayOfYear) {
    return -23.44 * Math.cos((2 * Math.PI * (dayOfYear + 10)) / 365);
  }
  // 日地距离修正因子（平方反比）1/d² = 1 + 0.033·cos(2πN/365)
  function distFactor(dayOfYear) {
    return 1 + 0.033 * Math.cos((2 * Math.PI * dayOfYear) / 365);
  }

  var MONTH_DAYS = [15, 45, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349]; // 每月代表日

  function mount(el, cfg) {
    cfg = cfg || {};
    var topic = cfg.topic || "本课主题";
    var task = cfg.task || ("用纬度 + 月份 + 图层解释" + topic + "。");
    var geojsonUrl = cfg.geojson || "../../assets/maps/political/world/countries.geojson";

    el.innerHTML =
      '<div class="tgl-panel">' +
      '  <div class="tgl-controls">' +
      '    <label>分析图层<select class="tgl-layer">' +
      '      <option value="sun">☀️ 太阳辐射（天文公式）</option>' +
      '      <option value="temp">🌡️ 气温（纬带气候平均）</option>' +
      '      <option value="rain">🌧️ 降水（纬带气候平均）</option>' +
      '    </select></label>' +
      '    <label>纬度 <span class="tgl-lat-v"></span><input class="tgl-lat" type="range" min="-60" max="60" step="1"></label>' +
      '    <label>月份 <span class="tgl-mon-v"></span><input class="tgl-mon" type="range" min="1" max="12" step="1"></label>' +
      "  </div>" +
      '  <div class="tgl-canvas-wrap"><canvas class="tgl-cv" width="960" height="460"></canvas></div>' +
      '  <div class="tgl-readout"></div>' +
      '  <div class="tgl-note"></div>' +
      '  <div class="tgl-task"></div>' +
      "</div>";

    var cv = el.querySelector(".tgl-cv"), ctx = cv.getContext("2d");
    var layerSel = el.querySelector(".tgl-layer"),
        latIn = el.querySelector(".tgl-lat"),
        monIn = el.querySelector(".tgl-mon"),
        latV = el.querySelector(".tgl-lat-v"),
        monV = el.querySelector(".tgl-mon-v"),
        readout = el.querySelector(".tgl-readout"),
        note = el.querySelector(".tgl-note"),
        taskBox = el.querySelector(".tgl-task");

    layerSel.value = cfg.defaultLayer || "sun";
    latIn.value = cfg.lat != null ? cfg.lat : 25;
    monIn.value = cfg.month != null ? cfg.month : 7;
    taskBox.textContent = "🎯 本课任务：" + task;

    var W = cv.width, H = cv.height, PADX = 28, PADY = 24;
    function proj(lon, lat) {
      return [PADX + ((lon + 180) / 360) * (W - 2 * PADX), PADY + ((90 - lat) / 180) * (H - 2 * PADY)];
    }

    var countries = null;
    fetch(geojsonUrl).then(function (r) { return r.json(); }).then(function (g) {
      countries = g.features || [];
      draw();
    }).catch(function () { countries = []; draw(); });

    function drawPoly(coords) {
      ctx.beginPath();
      for (var i = 0; i < coords.length; i++) {
        var p = proj(coords[i][0], coords[i][1]);
        if (i === 0) ctx.moveTo(p[0], p[1]); else ctx.lineTo(p[0], p[1]);
      }
      ctx.closePath();
    }

    function draw() {
      var layer = layerSel.value,
          lat = +latIn.value,
          mon = +monIn.value,
          day = MONTH_DAYS[mon - 1],
          dec = declination(day);

      latV.textContent = (lat > 0 ? lat + "°N" : lat < 0 ? -lat + "°S" : "0°");
      monV.textContent = mon + "月";

      // 背景（海洋）
      ctx.fillStyle = "#0a1628"; ctx.fillRect(0, 0, W, H);

      // 真实国界
      if (countries) {
        ctx.fillStyle = "#16233a"; ctx.strokeStyle = "#2c3e57"; ctx.lineWidth = 0.8;
        countries.forEach(function (f) {
          var geo = f.geometry; if (!geo) return;
          var polys = geo.type === "Polygon" ? [geo.coordinates] : geo.type === "MultiPolygon" ? geo.coordinates : [];
          polys.forEach(function (poly) {
            poly.forEach(function (ring) { drawPoly(ring); ctx.fill(); ctx.stroke(); });
          });
        });
      }

      // 经纬网
      ctx.strokeStyle = "rgba(148,163,184,.18)"; ctx.lineWidth = 1;
      for (var lon = -150; lon <= 150; lon += 30) { var a = proj(lon, 90), b = proj(lon, -90); ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke(); }
      for (var la = -60; la <= 60; la += 30) { var c = proj(-180, la), d = proj(180, la); ctx.beginPath(); ctx.moveTo(c[0], c[1]); ctx.lineTo(d[0], d[1]); ctx.stroke(); }

      // 赤道 / 回归线 / 极圈（虚线）
      ctx.setLineDash([6, 5]); ctx.strokeStyle = "rgba(125,211,252,.45)";
      [[0, "赤道"], [23.44, "北回归线"], [-23.44, "南回归线"], [66.56, "北极圈"], [-66.56, "南极圈"]].forEach(function (ln) {
        var p1 = proj(-180, ln[0]), p2 = proj(180, ln[0]);
        ctx.beginPath(); ctx.moveTo(p1[0], p1[1]); ctx.lineTo(p2[0], p2[1]); ctx.stroke();
        ctx.fillStyle = "rgba(125,211,252,.75)"; ctx.font = "12px -apple-system,PingFang SC,sans-serif";
        ctx.fillText(ln[1], p1[0] + 6, p1[1] - 4);
      });
      ctx.setLineDash([]);

      // 太阳层：昼夜半球（真实公式：sin h = sinφ sinδ + cosφ cosδ cosΔλ，h<0 为夜）
      if (layer === "sun") {
        ctx.fillStyle = "rgba(2,6,20,.55)";
        var rad = Math.PI / 180;
        for (var gx = 0; gx < W; gx += 4) {
          var lonG = (gx - PADX) / (W - 2 * PADX) * 360 - 180;
          for (var gy = 0; gy < H; gy += 4) {
            var latG = 90 - (gy - PADY) / (H - 2 * PADY) * 180;
            var sinH = Math.sin(latG * rad) * Math.sin(dec * rad) + Math.cos(latG * rad) * Math.cos(dec * rad) * Math.cos(lonG * rad);
            if (sinH < 0) ctx.fillRect(gx, gy, 4, 4);
          }
        }
        // 太阳直射点（地图中央经线简化，已注明示意）
        var sp = proj(0, dec);
        ctx.fillStyle = "#fbbf24"; ctx.beginPath(); ctx.arc(sp[0], sp[1], 6, 0, 7); ctx.fill();
        ctx.font = "13px -apple-system,PingFang SC,sans-serif";
        ctx.fillText("☀️ 直射点 " + (dec >= 0 ? dec.toFixed(1) + "°N" : (-dec).toFixed(1) + "°S"), sp[0] + 10, sp[1] + 4);
      }

      // 纬度指示线 + 纬带
      var y = proj(0, lat)[1], y5a = proj(0, Math.min(90, lat + 5))[1], y5b = proj(0, Math.max(-90, lat - 5))[1];
      ctx.fillStyle = "rgba(251,191,36,.10)"; ctx.fillRect(PADX, y5a, W - 2 * PADX, y5b - y5a);
      ctx.strokeStyle = "#fbbf24"; ctx.lineWidth = 2.5;
      ctx.beginPath(); ctx.moveTo(PADX, y); ctx.lineTo(W - PADX, y); ctx.stroke();
      ctx.fillStyle = "#fbbf24"; ctx.font = "bold 15px -apple-system,PingFang SC,sans-serif";
      ctx.fillText(latV.textContent, W - PADX - 58, y - 6);

      // 读数区
      var html = "", noteText = "";
      if (layer === "sun") {
        var noon = 90 - Math.abs(lat - dec);                       // 正午太阳高度角（精确）
        var toa = S0 * distFactor(day) * Math.max(0, Math.sin(noon * Math.PI / 180)); // 大气顶辐照（真实公式）
        var surface = toa * 0.7;                                    // 简化模型估算
        html = metric(dec.toFixed(1) + "°", "太阳赤纬 δ · 天文公式") +
               metric(noon.toFixed(1) + "°", "当地正午太阳高度角 · 精确") +
               metric(toa.toFixed(0) + " W/m²", "大气顶瞬时辐照 · 含日地距离修正") +
               metric("≈" + surface.toFixed(0) + " W/m²", "地面辐照 · 简化模型估算(透过率0.7)");
        noteText = "赤纬与高度角为天文公式精确值；地面辐照为晴天简化估算（未含云量）。昼夜分界由 sin h = sinφ·sinδ + cosφ·cosδ·cosΔλ 计算（直射经线取地图中央，示意）。试试把月份拖到 6/7 月 vs 12/1 月，看直射点南北移动，再解释「" + topic + "」。";
      } else if (layer === "temp") {
        var t = interp(TEMP_TABLE, lat);
        html = metric(t.toFixed(1) + " °C", Math.abs(lat) + "° 纬带年平均气温") +
               metric((26.2 - t).toFixed(1) + " °C", "与赤道纬带温差") +
               metric("10°", "纬带分辨率");
        noteText = "数值为全球纬带气候年平均（真实气候规律，忽略海陆与地形差异，南北纬镜像简化）。规律：气温随纬度升高而下降，源于正午太阳高度角与昼长的纬度差异——这正是「" + topic + "」的能量基础。";
      } else {
        var r = interp(RAIN_TABLE, lat);
        var zone = Math.abs(lat) < 10 ? "赤道低压带（上升气流，多雨）" :
                   Math.abs(lat) < 35 ? "副热带高压带（下沉气流，少雨）" :
                   Math.abs(lat) < 60 ? "盛行西风带（多锋面气旋，较多雨）" : "极地高压带（寒冷干燥，少雨）";
        html = metric(r.toFixed(0) + " mm", Math.abs(lat) + "° 纬带年降水量") +
               metric(zone.split("（")[0], "所在气压/风带") +
               metric("10°", "纬带分辨率");
        noteText = "数值为全球纬带气候年平均（真实气候规律，忽略海陆差异）。机制链：太阳辐射纬度差异 → 气压带风带 → 降水格局：" + zone + "。用这条链解释「" + topic + "」。";
      }
      readout.innerHTML = html;
      note.textContent = "📖 " + noteText;
    }

    function metric(v, label) {
      return '<div class="tgl-metric"><b>' + v + "</b><span>" + label + "</span></div>";
    }

    [layerSel, latIn, monIn].forEach(function (c) { c.addEventListener("input", draw); });
    draw();
  }

  window.TeachAnyGeoLab = { mount: mount };

  function boot() {
    var el = document.getElementById("teachany-geo-lab");
    if (el) mount(el, window.__TEACHANY_GEO_LAB__ || {});
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
