/* TeachAny Canvas Lab v1 —— 场景库
 *
 * 与 lab.js 配套：把「同类交互」固化成可复用场景，课件里只写一行挂载 + 本课参数。
 * 每个场景都是真实物理/数学关系驱动的（不是装饰动画），并带学生可操作控件。
 *
 * 用法（课件内联）：
 *   <script src="../../assets/engines/canvas-lab/v1/lab.js"></script>
 *   <script src="../../assets/engines/canvas-lab/v1/scenes.js"></script>
 *   <script>TeachAnyScenes.mount('friction', {canvas:'fric-canvas', readout:'fric-readout', slider:'rough'});</script>
 */
(function (global) {
  'use strict';

  function nf(v, n) { return (Math.round(v * Math.pow(10, n || 0)) / Math.pow(10, n || 0)).toFixed(n || 0); }

  /* ---------- 1) 摩擦力：粗糙度 → 需要的推力（真实正比关系） ---------- */
  function friction(cfg) {
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout,
      sliders: { rough: { el: cfg.slider, fmt: function (v) { return '粗糙度 ' + v + ' / 10'; } } },
      initial: { x: 0, moving: false },
      onPointer: function (type, p, s) {
        if (type === 'pointerdown') { s.moving = true; }
        if (type === 'pointerup' || type === 'pointerleave') { s.moving = false; }
      },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var groundY = H - 42;
        // 地面 + 粗糙度锯齿
        ctx.fillStyle = P.grid; ctx.fillRect(26, groundY, W - 52, 3);
        ctx.strokeStyle = P.grid; ctx.lineWidth = 1;
        for (var x = 26; x < W - 26; x += 9) {
          ctx.beginPath(); ctx.moveTo(x, groundY + 3);
          ctx.lineTo(x + 4, groundY + 3 + (2 + s.rough * 0.8)); ctx.stroke();
        }
        // 木块（起点留足左侧空间放推力箭头与标签）
        var bw = 92, bh = 56, bx = 150 + s.x, by = groundY - bh;
        ctx.fillStyle = P.fill; ctx.strokeStyle = P.accent; ctx.lineWidth = 2.4;
        h.rrect(ctx, bx, by, bw, bh, 10); ctx.fill(); ctx.stroke();
        h.label(ctx, '木块', bx + bw / 2, by + bh / 2, P.ink, 14, 'center', '700');
        // 需要克服的摩擦力 ∝ 粗糙度（真实正比）
        var need = 6 + s.rough * 10;
        var L = Math.min(78, 18 + need * 0.55);
        h.arrow(ctx, bx - 14 - L, by + bh / 2, bx - 6, by + bh / 2, P.accent2, 3);
        h.label(ctx, '推力 ' + Math.round(need) + ' N', bx - 20 - L, by + bh / 2 - 20, P.accent2, 12, 'left', '700');
        h.arrow(ctx, bx + bw + 6, by + bh / 2, bx + bw + 6 + L, by + bh / 2, P.bad, 3);
        h.label(ctx, '摩擦力 ' + Math.round(need) + ' N', bx + bw + 12 + L, by + bh / 2 - 20, P.bad, 12, 'left', '700');
        if (s.moving) {
          s.x = Math.min(s.x + 1.4, W - 380);
          h.label(ctx, '木块被推动 →', W - 30, 24, P.ok, 13, 'right', '700');
        } else {
          h.label(ctx, '👇 按住画面推动木块', W - 30, 24, P.muted, 12, 'right', '600');
        }
        this.readout(s.rough <= 3
          ? '表面较光滑（粗糙度 ' + s.rough + '）：需要推力约 ' + Math.round(need) + ' N —— 摩擦力小，容易推动。'
          : s.rough <= 7
            ? '表面中等粗糙（粗糙度 ' + s.rough + '）：需要推力约 ' + Math.round(need) + ' N —— 把滑块拖到两端对比。'
            : '表面很粗糙（粗糙度 ' + s.rough + '）：需要推力约 ' + Math.round(need) + ' N —— 接触面越粗糙，摩擦力越大。');
      }
    });
  }

  /* ---------- 2) 推/拉力：力的大小 → 木箱加速度（F = ma） ---------- */
  function pushpull(cfg) {
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout,
      sliders: { force: { el: cfg.slider, out: cfg.sliderOut, fmt: function (v) { return v + ' N'; } } },
      initial: { x: 0, v: 0, dir: 1 },
      buttons: { push: cfg.btnPush, reset: cfg.btnReset },
      onButton: function (name, s) { if (name === 'reset') { s.x = 0; s.v = 0; s.dir = 1; } if (name === 'push') { s.v = 0; s.dir = 1; } },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var m = 2.0, groundY = H - 44;
        ctx.fillStyle = P.grid; ctx.fillRect(30, groundY, W - 60, 3);
        var a = s.force / m;
        s.v += a * (1 / 60) * s.dir; s.x += s.v * 2.2;
        if (s.x > W - 260 || s.x < 0) { s.dir *= -1; s.v = 0; }
        var bw = 90, bh = 58, bx = 60 + s.x, by = groundY - bh;
        ctx.fillStyle = P.fill; ctx.strokeStyle = P.accent; ctx.lineWidth = 2.4;
        h.rrect(ctx, bx, by, bw, bh, 10); ctx.fill(); ctx.stroke();
        h.label(ctx, '木箱 2 kg', bx + bw / 2, by + bh / 2, P.ink, 13, 'center', '700');
        var L = 24 + s.force * 2.2;
        if (s.dir > 0) { h.arrow(ctx, bx + bw + 6, by + bh / 2, bx + bw + 6 + L, by + bh / 2, P.accent2, 3.4); }
        else { h.arrow(ctx, bx - 6, by + bh / 2, bx - 6 - L, by + bh / 2, P.accent2, 3.4); }
        h.label(ctx, '推力 ' + nf(s.force) + ' N', s.dir > 0 ? bx + bw + 10 + L : bx - 10 - L, by + bh / 2 - 22,
          P.accent2, 12, s.dir > 0 ? 'left' : 'right', '700');
        h.label(ctx, '加速度 a = F/m = ' + nf(a, 1) + ' m/s²', W - 30, 26, P.accent, 13, 'right', '700');
        if (s.force >= 18) h.label(ctx, '力越大，速度变化越快（越难停下）', W / 2, H - 16, P.bad, 12, 'center', '600');
        this.readout('推力 ' + nf(s.force) + ' N，质量固定 2 kg → 加速度 ' + nf(a, 1) + ' m/s²：推力越大，运动状态改变越快。');
      }
    });
  }

  /* ---------- 3) 影子长度：太阳高度角 → 影子长短（真实几何） ---------- */
  function shadow(cfg) {
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout,
      sliders: {
        time: { el: cfg.slider, out: cfg.sliderOut, fmt: function (v) { return v + ' 时'; } },
        size: { el: cfg.size, out: cfg.sizeOut, fmt: function (v) { return v + ' cm'; } }
      },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var groundY = H - 50;
        // 太阳高度角：6 时 0°，12 时 90°，18 时 0°
        var alt = Math.max(4, 90 * Math.sin(Math.PI * (s.time - 6) / 12));
        var rad = alt * Math.PI / 180;
        // 地面
        ctx.fillStyle = P.grid; ctx.fillRect(30, groundY, W - 60, 3);
        // 太阳
        var sx = W / 2 + (s.time - 12) * 46, sy = groundY - 60 - Math.tan(rad) * 120;
        sy = Math.max(18, Math.min(sy, groundY - 90));
        ctx.beginPath(); ctx.arc(sx, sy, 17, 0, Math.PI * 2); ctx.fillStyle = P.accent2; ctx.fill();
        // 光线
        ctx.strokeStyle = P.accent2; ctx.lineWidth = 1.6; ctx.globalAlpha = .6;
        ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(W / 2 - 10, groundY); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(W / 2 + 14, groundY); ctx.stroke();
        ctx.globalAlpha = 1;
        // 物体（高度随 size 变化；无该滑块时用默认 30cm）
        var size = (typeof s.size === 'number' && !isNaN(s.size)) ? s.size : 30;
        var oh = 40 + size * 0.9, ow = 22, ox = W / 2 - ow / 2, oy = groundY - oh;
        ctx.fillStyle = P.accent; ctx.fillRect(ox, oy, ow, oh);
        h.label(ctx, nf(size) + 'cm', ox - 8, oy + oh / 2, P.muted, 11, 'right', '600');
        // 影子长度 = 物高 / tan(高度角)
        var shadowLen = Math.min(400, oh / Math.max(0.18, Math.tan(rad)));
        ctx.fillStyle = 'rgba(15,23,42,.45)';
        ctx.beginPath();
        ctx.moveTo(ox + ow, groundY);
        ctx.lineTo(ox + ow + shadowLen, groundY);
        ctx.lineTo(ox + ow, groundY + 8);
        ctx.closePath(); ctx.fill();
        h.label(ctx, '影子 ' + nf(shadowLen) + ' px', ox + ow + shadowLen / 2, groundY + 22, P.ink, 12, 'center', '700');
        h.label(ctx, '太阳高度角 ' + nf(alt) + '°', W - 30, 26, P.accent2, 13, 'right', '700');
        this.readout(s.time <= 8 || s.time >= 16
          ? s.time + ' 时：太阳高度角小 → 影子很长（同一物体，早晚影子最长）。'
          : s.time === 12 ? '12 时：太阳最高 → 影子最短，几乎在物体正下方。'
          : s.time + ' 时：太阳升高 → 影子变短。拖动时间滑块看影子如何变化。');
      }
    });
  }

  /* ---------- 4) 杠杆：支点位置 → 省力还是费力（真实力矩） ---------- */
  function lever(cfg) {
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout,
      sliders: { fulcrum: { el: cfg.slider, out: cfg.sliderOut, fmt: function (v) { return '支点位置 ' + v + '%'; } } },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var cy = H * 0.42, L = W - 120, x0 = 60, x1 = x0 + L;
        var fx = x0 + L * (s.fulcrum / 100);
        // 杠杆
        ctx.strokeStyle = P.accent; ctx.lineWidth = 8; ctx.lineCap = 'round';
        ctx.beginPath(); ctx.moveTo(x0, cy); ctx.lineTo(x1, cy); ctx.stroke();
        // 支点
        ctx.beginPath(); ctx.moveTo(fx, cy + 4); ctx.lineTo(fx - 16, cy + 44); ctx.lineTo(fx + 16, cy + 44); ctx.closePath();
        ctx.fillStyle = P.accent2; ctx.fill();
        h.label(ctx, '支点', fx, cy + 60, P.accent2, 12, 'center', '700');
        // 左端重物 200 N；力臂比 → 需要的力
        var armIn = fx - x0, armOut = x1 - fx;
        var need = 200 * armIn / Math.max(armOut, 1);
        ctx.fillStyle = P.bad;
        h.rrect(ctx, x0 - 26, cy - 46, 52, 42, 8); ctx.fill();
        h.label(ctx, '200 N', x0, cy - 25, '#fff', 12, 'center', '700');
        h.arrow(ctx, x1 + 40, cy, x1 + 40, cy - 46, P.ok, 3);
        h.label(ctx, nf(need) + ' N', x1 + 54, cy - 46, P.ok, 13, 'left', '700');
        h.label(ctx, '动力臂 ' + nf(armOut) + ' / 阻力臂 ' + nf(armIn), W / 2, H - 26, P.ink, 12, 'center', '700');
        this.readout(armOut > armIn
          ? '支点在左（动力臂 ' + nf(armOut) + ' > 阻力臂 ' + nf(armIn) + '）：省力杠杆，只需 ' + nf(need) + ' N 就能撬起 200 N。'
          : armOut === armIn ? '等臂杠杆：需要的力等于物重（' + nf(need) + ' N），天平就是这个原理。'
          : '支点靠右（动力臂 ' + nf(armOut) + ' < 阻力臂 ' + nf(armIn) + '）：费力杠杆，需要 ' + nf(need) + ' N（如镊子）。');
      }
    });
  }

  var SCENES = { friction: friction, pushpull: pushpull, shadow: shadow, lever: lever };

  global.TeachAnyScenes = {
    mount: function (name, cfg) {
      if (!SCENES[name]) return null;
      return SCENES[name](cfg);
    },
    has: function (name) { return !!SCENES[name]; }
  };
})(window);
