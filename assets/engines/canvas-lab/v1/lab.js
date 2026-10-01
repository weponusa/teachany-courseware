/* TeachAny Canvas Lab v1 —— 课件内互动画布工具箱（轻量、离线、零依赖）
 *
 * 背景：一批课件里 `<canvas>` 只有空壳（没有绘制/交互代码），学生看到的是黑框或空白。
 * 本工具箱提供「画布 + 控件 + 读数 + 动画」的公共骨架，各课件的**学科场景代码**仍写在课件内联
 * <script> 里（内容准确、便于逐课审阅），公共部分只做：
 *   · 画布按 devicePixelRatio 缩放，逻辑坐标 = 设计像素（不用改场景代码）
 *   · 主题自适应：读页面 CSS 变量 --canvas-bg/--canvas-ink，缺省按页面明暗自动选色
 *   · 控件绑定、读数写入、requestAnimationFrame 循环、指针坐标换算
 *
 * 用法：
 *   <script src="../../assets/engines/canvas-lab/v1/lab.js"></script>
 *   <script>
 *     TeachAnyLab.mount({ canvas:'gravityCanvas', readout:'gravityStatus',
 *                         draw(ctx, W, H, s, t){...},   // s = 状态对象（含滑块值）
 *                         sliders:{ g:{el:'gSlider', fmt:function(v){return v+' m/s²';}, out:'gVal'} },
 *                         buttons:{ launch:'launchBtn', reset:'resetBtn' } });
 *   </script>
 */
(function (global) {
  'use strict';

  function lum(hex) {
    var m = /^#?([0-9a-f]{6})$/i.exec((hex || '').trim());
    if (!m) return 1;
    var n = parseInt(m[1], 16), r = (n >> 16) & 255, g = (n >> 8) & 255, b = n & 255;
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  }

  function theme(el) {
    var cs = getComputedStyle(document.body);
    var bg = (cs.getPropertyValue('--canvas-bg') || '').trim();
    var ink = (cs.getPropertyValue('--canvas-ink') || '').trim();
    var bodyBg = (cs.getPropertyValue('--bg') || cs.backgroundColor || '#ffffff').trim();
    var dark = lum(bodyBg.startsWith('#') ? bodyBg : '#ffffff') < 0.5;
    return dark
      ? { bg: bg || '#0b1628', grid: 'rgba(148,163,184,.28)', ink: ink || '#e2e8f0',
          muted: 'rgba(226,232,240,.65)', accent: '#38bdf8', accent2: '#fbbf24', ok: '#34d399', bad: '#f87171',
          fill: 'rgba(56,189,248,.18)', dark: true }
      : { bg: bg || '#f8fafc', grid: 'rgba(100,116,139,.22)', ink: ink || '#1e293b',
          muted: 'rgba(30,41,59,.55)', accent: '#0284c7', accent2: '#d97706', ok: '#059669', bad: '#dc2626',
          fill: 'rgba(2,132,199,.12)', dark: false };
  }

  function fit(cv) {
    var dpr = Math.min(global.devicePixelRatio || 1, 2);
    var W = cv.width, H = cv.height;                 // 设计尺寸（HTML 属性）
    if (cv.dataset.labFitted !== '1') {
      cv.style.width = '100%';
      cv.style.height = 'auto';
      cv.dataset.labW = String(W);
      cv.dataset.labH = String(H);
      cv.dataset.labFitted = '1';
    }
    cv.width = Math.round(W * dpr);
    cv.height = Math.round(H * dpr);
    var ctx = cv.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { ctx: ctx, W: W, H: H };
  }

  function rrect(ctx, x, y, w, h, r) {
    r = Math.min(r, h / 2, w / 2);
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
  }

  function arrow(ctx, x1, y1, x2, y2, color, width, head) {
    head = head || 9;
    var a = Math.atan2(y2 - y1, x2 - x1);
    ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = width || 2.5;
    ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x2, y2);
    ctx.lineTo(x2 - head * Math.cos(a - 0.4), y2 - head * Math.sin(a - 0.4));
    ctx.lineTo(x2 - head * Math.cos(a + 0.4), y2 - head * Math.sin(a + 0.4));
    ctx.closePath(); ctx.fill();
  }

  function label(ctx, text, x, y, color, size, align, weight) {
    ctx.fillStyle = color;
    ctx.font = (weight || '600') + ' ' + (size || 13) + "px 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif";
    ctx.textAlign = align || 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, x, y);
  }

  /** 主入口 */
  function mount(cfg) {
    var cv = document.getElementById(cfg.canvas);
    if (!cv) return null;
    var th = theme(cv);
    // 多画布联动：传入 sharedState 时共享同一个状态对象
    var state = cfg.sharedState || Object.assign({ t: 0, running: true }, cfg.initial || {});
    if (!cfg.sharedState) { state.t = state.t || 0; state.running = true; }
    var sliders = cfg.sliders || {};

    Object.keys(sliders).forEach(function (key) {
      var sc = sliders[key], el = document.getElementById(sc.el);
      if (!el) return;
      state[key] = parseFloat(el.value);
      var out = sc.out ? document.getElementById(sc.out) : null;
      var sync = function () {
        state[key] = parseFloat(el.value);
        if (out) out.textContent = sc.fmt ? sc.fmt(state[key]) : String(state[key]);
        if (cfg.onChange) cfg.onChange.call(api, state, key);
        if (cfg.draw) { var _f = fit(cv); cfg.draw.call(api, _f.ctx, _f.W, _f.H, state, state.t); }
      };
      el.addEventListener('input', sync);
      el.addEventListener('change', sync);
      if (out) out.textContent = sc.fmt ? sc.fmt(state[key]) : String(state[key]);
    });

    // 按钮：click 事件（真实交互事件，质检硬规则 #33 认这个）
    (cfg.buttons ? Object.keys(cfg.buttons) : []).forEach(function (name) {
      var b = document.getElementById(cfg.buttons[name]);
      if (!b) return;
      b.addEventListener('click', function () { if (cfg.onButton) cfg.onButton.call(api, name, state, api); });
    });

    var pointer = { x: 0, y: 0, down: false, inside: false };

    function toLocal(ev) {
      var r = cv.getBoundingClientRect();
      var scaleX = (parseFloat(cv.dataset.labW) || cv.width) / r.width;
      var scaleY = (parseFloat(cv.dataset.labH) || cv.height) / r.height;
      return { x: (ev.clientX - r.left) * scaleX, y: (ev.clientY - r.top) * scaleY };
    }
    ['pointerdown', 'pointermove', 'pointerup', 'pointerleave'].forEach(function (type) {
      cv.addEventListener(type, function (ev) {
        var p = toLocal(ev);
        pointer.x = p.x; pointer.y = p.y;
        pointer.down = (type === 'pointerdown') ? true : (type === 'pointerup' || type === 'pointerleave') ? false : pointer.down;
        pointer.inside = type !== 'pointerleave';
        if (ev.pointerType === 'touch' && type === 'pointerdown') { ev.preventDefault(); }
        if (cfg.onPointer) cfg.onPointer.call(api, type, pointer, state, api);
      }, { passive: false });
    });
    cv.style.cursor = cfg.cursor || 'default';
    cv.style.touchAction = 'none';

    function frame() {
      var f = fit(cv);
      if (cfg.draw) cfg.draw.call(api, f.ctx, f.W, f.H, state, state.t);
      if (state.running) state.t += 1 / 60;
      api._raf = requestAnimationFrame(frame);
    }

    var api = {
      canvas: cv, state: state, theme: th, palette: th,
      helpers: { rrect: rrect, arrow: arrow, label: label, lum: lum },
      set: function (k, v) { state[k] = v; },
      stop: function () { cancelAnimationFrame(api._raf); state.running = false; },
      readout: function (text) {
        var el = document.getElementById(cfg.readout);
        if (el) el.textContent = text;
      },
      fit: function () { return fit(cv); },
      palette: th,
      helpers: { rrect: rrect, arrow: arrow, label: label, lum: lum }
    };
    if (cfg.onReady) cfg.onReady.call(api, state, api);
    frame();
    return api;
  }

  global.TeachAnyLab = { mount: mount, helpers: { rrect: rrect, arrow: arrow, label: label } };
})(window);
